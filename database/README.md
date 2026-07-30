# database

Supabase Postgres schema for Passenger — migrations, RLS policies, scheduled functions. Owned by the `developer` agent; the `data-engineer` agent requests capabilities here rather than editing directly.

## Rules

- Migrations are `migrations/NNN_short_name.sql`, sequential, never renumbered and never edited once applied.
- Every table gets RLS. A table shipped without a policy is a bug, not a follow-up.
- **Applying a migration is Aviran-gated** — he holds the DB credentials. Write the migration, hand it off, don't apply it.
- No secrets in SQL. Config comes from Supabase project settings.
- Location data is sensitive: don't store more precision or history than the feature needs.

## Layout

- `migrations/` — sequential SQL migrations, see Rules above.
- `scripts/` — operational tooling that isn't a migration: exports, backfills, ad-hoc queries. Not applied automatically or Aviran-gated the way migrations are; run by hand with an explicit connection string from the environment, never a hardcoded one. **[ASSUMPTION — data-engineer, T-031 B3]:** proposed convention, not yet ratified anywhere else. Revisit if a later TRD needs a different shape.

## Status

| File | Task | Applied? | Contents |
|---|---|---|---|
| `001_hoods_and_density.sql` | T-031 (Map — Hoods & heat area), TRD §3.1/§11 steps A1-A3 | **Not applied — blocked-on-aviran.** Written and ready; Aviran holds the DB credentials, applying is his call. | `hoods` + `hood_density` tables with FK and both check constraints (A1); RLS enabled on both with one public `select` policy each, no write policy (A2); a **placeholder** seed of 5 named Tel Aviv Hoods with rough rectangular rings, not surveyed boundaries — real geometry is data-engineer's B3 export, not reachable from this session (A3). Uses `check (band > 0)` rather than the TRD's illustrative `between 1 and 3`, so the migration doesn't need reissuing if `data-engineer`'s B1 band-count call lands on anything but 3 — see the file's own header comment. |
| `002_synthetic_density_generator.sql` | T-031, TRD §11 steps B1-B2 | **Not applied — blocked-on-aviran**, and additionally needs the `pg_cron` extension enabled on the Supabase project (Database → Extensions) before it applies cleanly. Written and ready. | B1: `density_band_for_score()` — the quiet/moderate/busy score cutoffs (0.40, 0.70), documented with reasoning in the file. B2: `generate_synthetic_density()` — upserts 13 rolling absolute-UTC-hour buckets per Hood off a Tel Aviv-local diurnal curve (explicit transaction-scoped timezone pin, not a session-default assumption) times a deterministic per-Hood vibrancy weight; prunes rows older than a trailing buffer past "now" (closes `code-reviewer`'s retention finding). Scheduled hourly via `pg_cron` calling the function directly — no Edge Function, since there's no external API call to justify one; see the file's own comment for why. |

`database/scripts/export_hoods_geojson.py` (T-031 B3): exports the seeded `hoods` table into the flattened-ring bundle format the iOS client reads (`Resources/hoods-tel-aviv.json`, TRD §3.2). Resolves the §3.1/§3.2 polygon-shape ambiguity by ratifying what migration 001 already committed to — `hoods.polygon` stores the flattened ring directly, not a full GeoJSON envelope — so the export is a validated passthrough, not a translation. Not run against live data this session: no DB credentials available, and `hoods` currently holds only 001's placeholder seed, not real boundaries.

The previous schema — 26 migrations — is frozen in the archive repo (`github.com/AviranGrisaro/locali`, branch `brain`, `06-database/`). `../SALVAGE.md` has a per-group verdict. The short version: the places table and Tel Aviv seed, the neighborhoods/localness tables, and the place-sourcing pipeline are worth carrying over; the friends graph, location shares, and explored cells are not.

Also worth pulling for `hood_density`'s real feed: `06-database/gen_heat.py` and `tel-aviv-places-heat.json` from the archive — the synthetic density generator and its output (data-engineer's B2). **Confirmed still unreachable this session** (checked directly: `../locali/` does not exist anywhere under the workspace root, and `github.com/AviranGrisaro/locali` returns 404 from here — no local checkout, no authenticated remote access). Proceeded without the salvage shortcut per the TRD's own build-note; the generator above was written from the TRD's requirements and the diurnal-pattern reasoning in `PROGRESS.md`'s trd-review entry, not ported from the old file. Flagged again for whoever next has real environment access to `github.com/AviranGrisaro/locali` to check whether the old `gen_heat.py` has a materially different approach worth reconciling.
