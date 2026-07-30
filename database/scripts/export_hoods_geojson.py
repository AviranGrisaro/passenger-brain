#!/usr/bin/env python3
"""
export_hoods_geojson.py -- T-031 step B3: exports the seeded `hoods` table
into the bundled resource format the iOS client reads (TRD §3.2,
`Resources/hoods-tel-aviv.json`).

Format ambiguity this script pins (data-engineer's finding at trd-review):
TRD §3.1 illustrates `hoods.polygon` as a full GeoJSON Polygon geometry
object (`{"type": "Polygon", "coordinates": [[[lng, lat], ...]]}`), while
§3.2's client sample shows a flattened bare ring
(`[[lng, lat], [lng, lat], ...]`) -- one nesting level shallower, no
envelope. Migration 001 (`developer`, landed concurrently with this script)
already resolved this at the schema level: `hoods.polygon` stores the
flattened ring directly, matching §3.2, and explicitly punted full
reconciliation to B3.

This script ratifies that call rather than re-litigating it: nothing in
this TRD does a spatial query against `hoods.polygon` in Postgres (no
PostGIS, no `ST_Contains` -- hit-testing is entirely client-side, §4.3), so
full-GeoJSON-envelope compliance in the DB would buy no actual capability,
only an unwrap step this script would have to perform on every run. Pinned,
end to end: `hoods.polygon` (DB) and `Resources/hoods-tel-aviv.json`
(client bundle) both use the same shape --
`[[lng, lat], [lng, lat], ...]`, WGS84, one ring, no holes, closed
(first point == last point). Export is a validated passthrough, not a
translation.

Usage:
    DATABASE_URL=postgres://... python3 export_hoods_geojson.py \
        [--out ../../../passenger-code/Passenger/Resources/hoods-tel-aviv.json] \
        [--city tel-aviv]

Requires psycopg2 and a reachable Postgres connection string. Never
hardcode credentials -- DATABASE_URL comes from the environment only, per
database/README.md ("no secrets in SQL, config comes from Supabase project
settings").

Not run against live data in this session: no DATABASE_URL/Supabase
credentials are available in this sandbox (applying migrations and issuing
credentials are both Aviran-gated, per database/README.md), and `hoods`
currently holds only migration 001's explicitly-labeled PLACEHOLDER seed,
not a real Tel Aviv boundary set. Whoever runs this for real should confirm
the seed has been replaced with real boundaries first -- this script does
not know the difference and will happily export placeholder rectangles.
"""
import argparse
import datetime
import json
import os
import sys
from pathlib import Path

SCHEMA_VERSION = 1
DEFAULT_OUT = (
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
            cur.execute("select id, name, polygon from public.hoods order by id;")
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


def build_bundle(rows, city: str):
    hoods = []
    for row in rows:
        ring = validate_ring(row["polygon"], row["id"])
        hoods.append({"id": row["id"], "name": row["name"], "polygon": ring})
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "city": city,
        "hoods": hoods,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output path for the bundled JSON")
    parser.add_argument("--city", default="tel-aviv")
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
            "`hoods` table returned zero rows -- refusing to write an empty bundle. "
            "Seed the table first (TRD §11 step A3) or check DATABASE_URL."
        )

    bundle = build_bundle(rows, args.city)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {len(bundle['hoods'])} hoods to {args.out}")


if __name__ == "__main__":
    main()
