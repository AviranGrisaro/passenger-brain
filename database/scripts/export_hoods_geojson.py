#!/usr/bin/env python3
"""
export_hoods_geojson.py -- REPURPOSED at T-040 (hood-dataset) step B3.

**No longer the primary path.** Originally T-031's export (DB -> bundle),
it has never run against live data (no DATABASE_URL reachable by any agent
in this pipeline -- see database/README.md). `hood-dataset/TRD.md` sec 2.1
inverted the pipeline for exactly that reason: the authored source is now
`database/data/hoods-tel-aviv.source.json`, and `build_hoods.py` is the
generator that produces both `Resources/hoods-tel-aviv.json` (this script's
old job) and the data migration, offline, with no database access.

**This script's new job: the post-apply drift check (TRD sec 5.3).** Once
the schema (`003_hood_attributes.sql`) and data
(`006_hoods_tel_aviv_data.sql`) migrations are applied -- Aviran-gated,
database/README.md -- `--check` mode exports the *live* `hoods` table and
diffs it against the committed bundle (`Resources/hoods-tel-aviv.json`).
A non-empty diff means someone edited the database out of band (a manual
`update`, a hand-applied fix that skipped the source-file pipeline). It is
the one check in this pipeline that only a live DB connection can perform,
and the only one of the three tripwires named in TRD sec 5.1/9 that this
script still owns -- `HoodCatalogTests` (iOS) and `build_hoods.py --check`
(offline validation) cover the other two.

Format: `hoods.polygon` and `Resources/hoods-tel-aviv.json` both use the
flattened single-ring shape `[[lng, lat], [lng, lat], ...]`, WGS84, closed
(first point == last point) -- pinned at T-031 B3, unchanged here. This
script still ratifies that shape; it does not translate it.

Usage:
    DATABASE_URL=postgres://... python3 export_hoods_geojson.py --check
        [--bundle ../../../passenger-code/Passenger/Resources/hoods-tel-aviv.json]
        [--city tel-aviv]

    # Old export-only mode still works (e.g. to inspect live state without
    # diffing), but is no longer how the bundle gets produced:
    DATABASE_URL=postgres://... python3 export_hoods_geojson.py --out /tmp/live.json

Requires psycopg2 and a reachable Postgres connection string. Never
hardcode credentials -- DATABASE_URL comes from the environment only, per
database/README.md ("no secrets in SQL, config comes from Supabase project
settings").

Not run against live data in this session (T-040 build, 2026-07-31): no
DATABASE_URL/Supabase credentials are available in this sandbox, and
neither `003_hood_attributes.sql` nor `006_hoods_tel_aviv_data.sql` has
been applied yet (applying migrations is Aviran-gated). `--check` cannot
be exercised for real until both are applied; its logic is exercised here
only by inspection and by diffing two in-memory bundles built from the
same source, not against a live table.
"""
import argparse
import datetime
import json
import os
import sys
from pathlib import Path

SCHEMA_VERSION = 2  # bumped from 1 at T-040: adds centroid + the three attribute fields
DEFAULT_BUNDLE = (
    Path(__file__).resolve().parents[3]
    / "passenger-code" / "Passenger" / "Resources" / "hoods-tel-aviv.json"
)


def fetch_hoods(database_url: str):
    try:
        import psycopg2
        import psycopg2.extras
    except ImportError as exc:
        sys.exit(f"psycopg2 is required to run this script: {exc}")

    conn = psycopg2.connect(database_url)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "select id, name, polygon, blurb, is_tourist_trap, "
                "designated_for_progression from public.hoods order by id;"
            )
            return cur.fetchall()
    finally:
        conn.close()


def validate_ring(ring, hood_id: str):
    """`ring` is expected to already be the flattened [[lng,lat],...] shape
    (see module docstring) -- validate it, don't translate it."""
    if not isinstance(ring, list) or len(ring) < 4:
        raise ValueError(
            f"hood {hood_id!r}: polygon is not a ring with >= 4 points: {ring!r}"
        )
    for point in ring:
        if not (isinstance(point, list) and len(point) == 2):
            raise ValueError(f"hood {hood_id!r}: malformed point {point!r} in ring")
        lng, lat = point
        if not (-180 <= lng <= 180 and -90 <= lat <= 90):
            raise ValueError(
                f"hood {hood_id!r}: point {point!r} out of lng/lat range -- "
                f"check for a swapped lat/lng pair"
            )
    if ring[0] != ring[-1]:
        raise ValueError(f"hood {hood_id!r}: ring is not closed (first point != last point)")
    return ring


def _area_centroid(ring):
    """Local copy of validate_dataset.area_centroid so this script has no
    import-order dependency on the generator path -- kept in sync by hand;
    both are ~15 lines and covered by the same shoelace formula (TRD sec
    2.3 / sec 8 D5)."""
    pts = ring[:-1] if ring[0] == ring[-1] else ring
    n = len(pts)
    a_sum = cx = cy = 0.0
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        cross = x0 * y1 - x1 * y0
        a_sum += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    a_sum *= 0.5
    if abs(a_sum) < 1e-15:
        return (round(sum(p[0] for p in pts) / n, 6), round(sum(p[1] for p in pts) / n, 6))
    return (round(cx / (6 * a_sum), 6), round(cy / (6 * a_sum), 6))


def build_bundle(rows, city: str):
    hoods = []
    for row in rows:
        ring = validate_ring(row["polygon"], row["id"])
        centroid = _area_centroid(ring)
        hoods.append({
            "id": row["id"],
            "name": row["name"],
            "polygon": ring,
            "centroid": [centroid[0], centroid[1]],
            "blurb": row.get("blurb"),
            "isTouristTrap": row.get("is_tourist_trap"),
            "designatedForProgression": row.get("designated_for_progression", False),
        })
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "city": city,
        "hoods": hoods,
    }


def diff_bundles(live: dict, committed: dict):
    """Returns a list of human-readable diff lines; empty means no drift.
    Ignores `generatedAt` (expected to differ on every run)."""
    lines = []
    live_by_id = {h["id"]: h for h in live["hoods"]}
    committed_by_id = {h["id"]: h for h in committed["hoods"]}

    only_live = set(live_by_id) - set(committed_by_id)
    only_committed = set(committed_by_id) - set(live_by_id)
    for hid in sorted(only_live):
        lines.append(f"DB has {hid!r}, committed bundle does not")
    for hid in sorted(only_committed):
        lines.append(f"committed bundle has {hid!r}, DB does not")

    for hid in sorted(set(live_by_id) & set(committed_by_id)):
        a, b = dict(live_by_id[hid]), dict(committed_by_id[hid])
        for key in ("name", "polygon", "blurb", "isTouristTrap", "designatedForProgression"):
            if a.get(key) != b.get(key):
                lines.append(f"{hid!r}.{key} differs: DB={a.get(key)!r} committed={b.get(key)!r}")
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE, help="Committed bundle to diff against in --check mode")
    parser.add_argument("--out", type=Path, default=None, help="Export-only mode: write the live table's export here instead of diffing")
    parser.add_argument("--city", default="tel-aviv")
    parser.add_argument("--check", action="store_true", help="Export the live table and diff against --bundle; non-zero exit on drift")
    args = parser.parse_args()

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        sys.exit(
            "DATABASE_URL is not set. This script reads live from Supabase Postgres; "
            "no credentials are hardcoded here (database/README.md rule)."
        )

    rows = fetch_hoods(database_url)
    if not rows:
        sys.exit(
            "`hoods` table returned zero rows -- refusing to proceed. "
            "Apply 006_hoods_tel_aviv_data.sql first, or check DATABASE_URL."
        )

    live_bundle = build_bundle(rows, args.city)

    if args.check:
        if not args.bundle.exists():
            sys.exit(f"--check: committed bundle not found at {args.bundle}")
        committed_bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
        diffs = diff_bundles(live_bundle, committed_bundle)
        if diffs:
            print(f"DRIFT DETECTED between live DB and {args.bundle}:", file=sys.stderr)
            for line in diffs:
                print(f"  - {line}", file=sys.stderr)
            sys.exit(1)
        print(f"No drift: live DB matches {args.bundle} ({len(live_bundle['hoods'])} hoods)")
        return

    out = args.out or DEFAULT_BUNDLE
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(live_bundle, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {len(live_bundle['hoods'])} hoods to {out}")


if __name__ == "__main__":
    main()
