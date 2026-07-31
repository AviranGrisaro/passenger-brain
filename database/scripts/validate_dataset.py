#!/usr/bin/env python3
"""
validate_dataset.py -- the shared polygon-math module named in
`hood-dataset/TRD.md` section 4.4 (`C-HOOD-1` clause 4) and
`places-dataset/TRD.md` section 4.1. Stdlib only (TRD section 2.3 -- Shapely
and PostGIS are both rejected there; nothing here imports either).

Two invariants, one shared file:
  - T-040 (hood-dataset)'s half: ring validation, non-overlap (V1-V9 below),
    the area-weighted centroid, and `resolve_hood` (point -> containing
    Hood id).
  - T-042 (places-dataset)'s half: calling `resolve_hood` to attribute every
    place to exactly one Hood (`C-HOOD-1` clause 2). Whichever task's build
    lands first writes this module; T-040 landed first, so this is that
    module. T-042's build should import from here rather than reimplementing
    the ray cast.

Algorithm spec, stated identically across `hood-dataset/TRD.md`,
`places-dataset/TRD.md` and `live-events-pipeline/TRD.md` (section 2.2 of
the first): closed single-ring WGS84 [[lng,lat], ...], even-odd ray cast,
bbox prefilter, on-boundary -> not contained (`False`). T-043's live
`hood_for_point()` plpgsql implementation is a *separate* implementation
held to the same spec and the same fixture
(`database/data/fixtures/hood-containment-cases.json`) -- not this file,
because it runs inside Postgres against the live table, not offline against
the authored source (TRD section 2.2).

No network access, no database access, by design.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

Point = tuple  # (lng, lat)

# Tel Aviv-Yafo bounding box (V5) -- deliberately loose. Matches
# `hood-dataset/TRD.md` section 5.2 V5 exactly: this is the only reliable
# catch for a swapped lat/lng pair, because Tel Aviv's latitude (~32) is
# coincidentally inside longitude's valid numeric range and vice versa, so
# a bare range check (V4) is not sufficient on its own.
TEL_AVIV_BBOX = (34.72, 32.01, 34.86, 32.14)  # (min_lng, min_lat, max_lng, max_lat)

VALID_PROVENANCE_SOURCES = {"osm", "municipal", "manual"}

# V7 thresholds (section 8 D9): sampled coverage-gap check.
COVERAGE_SAMPLE_GRID_METERS = 50
COVERAGE_GAP_ERROR_M2 = 40_000
COVERAGE_GAP_WARN_M2 = 5_000


class Violation(Exception):
    """A single dataset violation. Collected, not raised individually, so a
    dataset with six problems takes one run to find all six (TRD section
    4.5)."""

    def __init__(self, code: str, message: str, level: str = "error"):
        self.code = code
        self.message = message
        self.level = level  # "error" or "warning"
        super().__init__(f"[{level.upper()} {code}] {message}")

    def __repr__(self):
        return f"Violation({self.code!r}, {self.message!r}, level={self.level!r})"


@dataclass
class HoodRecord:
    id: str
    name: str
    polygon: list  # closed ring, [[lng, lat], ...]
    blurb: Optional[str]
    is_tourist_trap: Optional[bool]
    designated_for_progression: bool
    provenance: dict
    raw: dict = field(default_factory=dict, repr=False)


@dataclass
class HoodDataset:
    city: str
    hoods: list  # list[HoodRecord]


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_hood_source(path) -> HoodDataset:
    import json

    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    hoods = []
    for entry in raw.get("hoods", []):
        hoods.append(
            HoodRecord(
                id=entry.get("id"),
                name=entry.get("name"),
                polygon=entry.get("polygon"),
                blurb=entry.get("blurb"),
                is_tourist_trap=entry.get("isTouristTrap"),
                designated_for_progression=entry.get("designatedForProgression"),
                provenance=entry.get("provenance") or {},
                raw=entry,
            )
        )
    return HoodDataset(city=raw.get("city", "tel-aviv"), hoods=hoods)


# ---------------------------------------------------------------------------
# Shared geometry predicates (TRD section 2.3)
# ---------------------------------------------------------------------------

def _bbox_of(ring):
    lngs = [p[0] for p in ring]
    lats = [p[1] for p in ring]
    return (min(lngs), min(lats), max(lngs), max(lats))


def _bboxes_overlap(a, b) -> bool:
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


def point_strictly_inside(p, ring) -> bool:
    """Even-odd ray cast. On-boundary returns False (TRD section 2.3
    predicate 1 / section 2.2's algorithm spec)."""
    x, y = p
    n = len(ring)
    inside = False
    # ring is closed (ring[0] == ring[-1]); iterate n-1 edges.
    j = n - 2
    for i in range(n - 1):
        xi, yi = ring[i]
        xj, yj = ring[j]

        # On-boundary check: point exactly on this segment -> not strictly inside.
        if _point_on_segment(p, (xi, yi), (xj, yj)):
            return False

        if (yi > y) != (yj > y):
            x_intersect = xi + (y - yi) * (xj - xi) / (yj - yi)
            if x < x_intersect:
                inside = not inside
        j = i
    return inside


def _point_on_segment(p, a, b, eps=1e-12) -> bool:
    px, py = p
    ax, ay = a
    bx, by = b
    cross = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
    if abs(cross) > eps:
        return False
    dot = (px - ax) * (bx - ax) + (py - ay) * (by - ay)
    if dot < -eps:
        return False
    sq_len = (bx - ax) ** 2 + (by - ay) ** 2
    if dot > sq_len + eps:
        return False
    return True


def _orientation(a, b, c) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def segments_properly_cross(a1, a2, b1, b2) -> bool:
    """A transversal crossing only -- strict orientation sign changes on
    both segments. Collinear overlap and endpoint contact deliberately
    return False (TRD section 2.3 predicate 2)."""
    d1 = _orientation(b1, b2, a1)
    d2 = _orientation(b1, b2, a2)
    d3 = _orientation(a1, a2, b1)
    d4 = _orientation(a1, a2, b2)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and (
        (d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)
    ):
        return True
    return False


def ring_self_intersects(ring) -> bool:
    """Predicate 2 applied to a ring against itself (V3)."""
    n = len(ring) - 1  # closed ring -> n distinct edges
    if n < 3:
        return False
    for i in range(n):
        a1, a2 = ring[i], ring[i + 1]
        for j in range(i + 1, n):
            # Skip adjacent edges (they legitimately share an endpoint) and
            # the wraparound pair.
            if j == i or j == i + 1:
                continue
            if i == 0 and j == n - 1:
                continue
            b1, b2 = ring[j], ring[j + 1]
            if segments_properly_cross(a1, a2, b1, b2):
                return True
    return False


def polygons_overlap(ring_a, ring_b) -> bool:
    """Any vertex of A strictly inside B, or any vertex of B strictly
    inside A, or any edge pair properly crossing (TRD section 2.3
    predicate 3). Shared edges/vertices are legal and return False."""
    for p in ring_a[:-1]:
        if point_strictly_inside(p, ring_b):
            return True
    for p in ring_b[:-1]:
        if point_strictly_inside(p, ring_a):
            return True

    na, nb = len(ring_a) - 1, len(ring_b) - 1
    for i in range(na):
        a1, a2 = ring_a[i], ring_a[i + 1]
        for j in range(nb):
            b1, b2 = ring_b[j], ring_b[j + 1]
            if segments_properly_cross(a1, a2, b1, b2):
                return True
    return False


def area_centroid(ring):
    """Shoelace area-weighted centroid (TRD section 2.3 / section 8 D5).
    ~15 stdlib lines, robust to a duplicated closing point."""
    pts = ring[:-1] if ring[0] == ring[-1] else ring
    n = len(pts)
    a_sum = 0.0
    cx = 0.0
    cy = 0.0
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        cross = x0 * y1 - x1 * y0
        a_sum += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    a_sum *= 0.5
    if abs(a_sum) < 1e-15:
        # Degenerate ring -- fall back to a plain vertex average rather than
        # dividing by ~zero.
        avg_x = sum(p[0] for p in pts) / n
        avg_y = sum(p[1] for p in pts) / n
        return (avg_x, avg_y)
    cx /= 6 * a_sum
    cy /= 6 * a_sum
    return (round(cx, 6), round(cy, 6))


def _ring_area_m2(ring) -> float:
    """Approximate planar area in square meters via an equirectangular
    projection local to Tel Aviv's latitude -- good enough for the V7
    gap-size threshold, not a survey-grade area."""
    pts = ring[:-1] if ring[0] == ring[-1] else ring
    lat0 = sum(p[1] for p in pts) / len(pts)
    m_per_deg_lat = 111_320.0
    m_per_deg_lng = 111_320.0 * math.cos(math.radians(lat0))
    proj = [(p[0] * m_per_deg_lng, p[1] * m_per_deg_lat) for p in pts]
    a = 0.0
    n = len(proj)
    for i in range(n):
        x0, y0 = proj[i]
        x1, y1 = proj[(i + 1) % n]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2.0


def resolve_hood(dataset: HoodDataset, lng: float, lat: float) -> Optional[str]:
    """Point -> containing Hood id, or None if the point is in no Hood
    (`C-HOOD-1` clause 2, shared with T-042). On-boundary -> None (no
    Hood), per the algorithm spec shared with T-043's SQL implementation."""
    p = (lng, lat)
    hits = []
    for hood in dataset.hoods:
        bbox = _bbox_of(hood.polygon)
        if not (bbox[0] <= lng <= bbox[2] and bbox[1] <= lat <= bbox[3]):
            continue
        if point_strictly_inside(p, hood.polygon):
            hits.append(hood.id)
    if len(hits) == 1:
        return hits[0]
    return None  # zero or multiple containing Hoods are both "no resolution"


# ---------------------------------------------------------------------------
# V1-V9 validation (TRD section 5.2)
# ---------------------------------------------------------------------------

import re

_SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_hoods(dataset: HoodDataset) -> list:
    violations: list[Violation] = []
    seen_ids = set()

    for hood in dataset.hoods:
        # V1 -- slug format, uniqueness, non-empty name
        if not hood.id or not _SLUG_RE.match(hood.id):
            violations.append(Violation("V1", f"hood id {hood.id!r} is not a valid lowercase slug"))
        if hood.id in seen_ids:
            violations.append(Violation("V1", f"duplicate hood id {hood.id!r}"))
        seen_ids.add(hood.id)
        if not hood.name or not hood.name.strip():
            violations.append(Violation("V1", f"hood {hood.id!r}: empty name"))

        # V2 -- polygon is exactly [[lng, lat], ...], a third nesting level is an error
        ring = hood.polygon
        if not isinstance(ring, list) or len(ring) == 0:
            violations.append(Violation("V2", f"hood {hood.id!r}: polygon missing or not a list"))
            continue
        if not all(isinstance(pt, list) and len(pt) == 2 and all(isinstance(v, (int, float)) for v in pt) for pt in ring):
            violations.append(Violation("V2", f"hood {hood.id!r}: polygon is not a flat [[lng,lat], ...] ring -- nested/multi-ring input is rejected, not unwrapped"))
            continue

        # V3 -- closed, >=4 points, >=3 distinct points, not self-intersecting
        if ring[0] != ring[-1]:
            violations.append(Violation("V3", f"hood {hood.id!r}: ring is not closed (first point != last point)"))
        if len(ring) < 4:
            violations.append(Violation("V3", f"hood {hood.id!r}: ring has fewer than 4 points"))
        distinct = {tuple(p) for p in ring}
        if len(distinct) < 3:
            violations.append(Violation("V3", f"hood {hood.id!r}: ring has fewer than 3 distinct points"))
        if len(ring) >= 4 and ring[0] == ring[-1] and ring_self_intersects(ring):
            violations.append(Violation("V3", f"hood {hood.id!r}: ring is self-intersecting"))

        # V4 -- every coordinate in valid lng/lat range
        for pt in ring:
            lng, lat = pt
            if not (-180 <= lng <= 180 and -90 <= lat <= 90):
                violations.append(Violation("V4", f"hood {hood.id!r}: point {pt} out of lng/lat range -- check for a swapped lat/lng pair"))
                break

        # V5 -- every coordinate inside the Tel Aviv-Yafo bounding box
        min_lng, min_lat, max_lng, max_lat = TEL_AVIV_BBOX
        for pt in ring:
            lng, lat = pt
            if not (min_lng <= lng <= max_lng and min_lat <= lat <= max_lat):
                violations.append(Violation("V5", f"hood {hood.id!r}: point {pt} outside the Tel Aviv-Yafo bounding box {TEL_AVIV_BBOX}"))
                break

        # V8 -- blurb null or non-blank
        if hood.blurb is not None and not hood.blurb.strip():
            violations.append(Violation("V8", f"hood {hood.id!r}: blurb is empty/whitespace-only -- use null, not \"\""))

        # V9 -- isTouristTrap in {true,false,null}; designatedForProgression in {true,false}, never null
        if hood.is_tourist_trap is not None and not isinstance(hood.is_tourist_trap, bool):
            violations.append(Violation("V9", f"hood {hood.id!r}: isTouristTrap must be true/false/null"))
        if not isinstance(hood.designated_for_progression, bool):
            violations.append(Violation("V9", f"hood {hood.id!r}: designatedForProgression must be true/false, never null"))
        prov = hood.provenance or {}
        if prov.get("source") not in VALID_PROVENANCE_SOURCES:
            violations.append(Violation("V9", f"hood {hood.id!r}: provenance.source {prov.get('source')!r} not in {VALID_PROVENANCE_SOURCES}"))
        if not prov.get("sourceRef"):
            violations.append(Violation("V9", f"hood {hood.id!r}: provenance.sourceRef missing"))
        if not prov.get("retrievedAt"):
            violations.append(Violation("V9", f"hood {hood.id!r}: provenance.retrievedAt missing"))

    # V6 -- non-overlap, bbox-prefiltered. The check the whole task exists for.
    violations.extend(non_overlap_report(dataset, as_violations=True))

    # V7 -- sampled interior coverage gaps.
    violations.extend(coverage_gaps(dataset, as_violations=True))

    return violations


def non_overlap_report(dataset: HoodDataset, as_violations: bool = False):
    """V6. Returns list[OverlapPair] (id_a, id_b) by default, or
    list[Violation] if as_violations=True."""
    results = []
    hoods = [h for h in dataset.hoods if isinstance(h.polygon, list) and len(h.polygon) >= 4]
    bboxes = {h.id: _bbox_of(h.polygon) for h in hoods}
    for i in range(len(hoods)):
        for j in range(i + 1, len(hoods)):
            a, b = hoods[i], hoods[j]
            if not _bboxes_overlap(bboxes[a.id], bboxes[b.id]):
                continue
            if polygons_overlap(a.polygon, b.polygon):
                if as_violations:
                    results.append(Violation("V6", f"hoods {a.id!r} and {b.id!r} have overlapping interiors"))
                else:
                    results.append((a.id, b.id))
    return results


def coverage_gaps(dataset: HoodDataset, as_violations: bool = False):
    """V7. Sampled interior-hole check over a 50m grid within the V5
    bounding box (TRD section 8 D9). Clusters touching the sampled region's
    edge are exterior, not interior, and are skipped."""
    min_lng, min_lat, max_lng, max_lat = TEL_AVIV_BBOX
    lat0 = (min_lat + max_lat) / 2
    m_per_deg_lat = 111_320.0
    m_per_deg_lng = 111_320.0 * math.cos(math.radians(lat0))
    step_lat = COVERAGE_SAMPLE_GRID_METERS / m_per_deg_lat
    step_lng = COVERAGE_SAMPLE_GRID_METERS / m_per_deg_lng

    hoods = [h for h in dataset.hoods if isinstance(h.polygon, list) and len(h.polygon) >= 4]
    bboxes = [(_bbox_of(h.polygon), h.polygon) for h in hoods]

    n_lat = max(1, int((max_lat - min_lat) / step_lat))
    n_lng = max(1, int((max_lng - min_lng) / step_lng))

    # Cap grid size so this stays fast for a "dozens of Hoods" dataset in CI/CLI use.
    max_cells = 400 * 400
    if n_lat * n_lng > max_cells:
        scale = math.sqrt((n_lat * n_lng) / max_cells)
        n_lat = max(1, int(n_lat / scale))
        n_lng = max(1, int(n_lng / scale))

    covered = [[False] * n_lng for _ in range(n_lat)]
    for i in range(n_lat):
        lat = min_lat + (i + 0.5) * (max_lat - min_lat) / n_lat
        for j in range(n_lng):
            lng = min_lng + (j + 0.5) * (max_lng - min_lng) / n_lng
            for bbox, ring in bboxes:
                if bbox[0] <= lng <= bbox[2] and bbox[1] <= lat <= bbox[3]:
                    if point_strictly_inside((lng, lat), ring):
                        covered[i][j] = True
                        break

    cell_area_m2 = (step_lat * n_lat and (max_lat - min_lat) / n_lat * m_per_deg_lat) * (
        (max_lng - min_lng) / n_lng * m_per_deg_lng
    )

    visited = [[False] * n_lng for _ in range(n_lat)]
    clusters = []
    for i in range(n_lat):
        for j in range(n_lng):
            if covered[i][j] or visited[i][j]:
                continue
            # BFS this uncovered component
            stack = [(i, j)]
            visited[i][j] = True
            cells = []
            touches_edge = False
            while stack:
                ci, cj = stack.pop()
                cells.append((ci, cj))
                if ci == 0 or cj == 0 or ci == n_lat - 1 or cj == n_lng - 1:
                    touches_edge = True
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ni, nj = ci + di, cj + dj
                    if 0 <= ni < n_lat and 0 <= nj < n_lng and not covered[ni][nj] and not visited[ni][nj]:
                        visited[ni][nj] = True
                        stack.append((ni, nj))
            if touches_edge:
                continue  # exterior, not interior -- skipped per section 8 D9
            clusters.append(cells)

    results = []
    for cells in clusters:
        area = len(cells) * cell_area_m2
        if area > COVERAGE_GAP_ERROR_M2:
            results.append(("error", area, cells))
        elif area > COVERAGE_GAP_WARN_M2:
            results.append(("warn", area, cells))

    if not as_violations:
        return results

    violations = []
    for level, area, cells in results:
        v_level = "error" if level == "error" else "warning"
        violations.append(
            Violation(
                "V7",
                f"interior coverage gap of ~{area:.0f} m^2 found (sampled grid, {len(cells)} cells)",
                level=v_level,
            )
        )
    return violations


def slug_preservation_warning(dataset: HoodDataset, required_slugs) -> list:
    """PRD req 3's third bullet: warn (not error) if a previously-seeded
    slug disappears."""
    ids = {h.id for h in dataset.hoods}
    warnings = []
    for slug in required_slugs:
        if slug not in ids:
            warnings.append(
                Violation("SLUG-PRESERVE", f"previously-seeded slug {slug!r} is missing from this dataset", level="warning")
            )
    return warnings


PREVIOUSLY_SEEDED_SLUGS = ["florentin", "neve-tzedek", "lev-hair", "old-north", "jaffa"]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        sys.exit("usage: validate_dataset.py <source.json>")
    ds = load_hood_source(sys.argv[1])
    violations = validate_hoods(ds)
    warnings = slug_preservation_warning(ds, PREVIOUSLY_SEEDED_SLUGS)
    for w in warnings:
        print(w)
    errors = [v for v in violations if v.level == "error"]
    warns = [v for v in violations if v.level == "warning"]
    for v in violations:
        print(v)
    print(f"\n{len(errors)} error(s), {len(warns)} warning(s), {len(ds.hoods)} hoods")
    sys.exit(1 if errors else 0)
