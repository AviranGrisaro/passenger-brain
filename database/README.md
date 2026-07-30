# database

Supabase Postgres schema for Passenger — migrations, RLS policies, scheduled functions. Owned by the `developer` agent; the `data-engineer` agent requests capabilities here rather than editing directly.

## Rules

- Migrations are `migrations/NNN_short_name.sql`, sequential, never renumbered and never edited once applied.
- Every table gets RLS. A table shipped without a policy is a bug, not a follow-up.
- **Applying a migration is Aviran-gated** — he holds the DB credentials. Write the migration, hand it off, don't apply it.
- No secrets in SQL. Config comes from Supabase project settings.
- Location data is sensitive: don't store more precision or history than the feature needs.

## Status

| File | Task | Applied? | Contents |
|---|---|---|---|
| `001_hoods_and_density.sql` | T-031 (Map — Hoods & heat area), TRD §3.1/§11 steps A1-A3 | **Not applied — blocked-on-aviran.** Written and ready; Aviran holds the DB credentials, applying is his call. | `hoods` + `hood_density` tables with FK and both check constraints (A1); RLS enabled on both with one public `select` policy each, no write policy (A2); a **placeholder** seed of 5 named Tel Aviv Hoods with rough rectangular rings, not surveyed boundaries — real geometry is data-engineer's B3 export, not reachable from this session (A3). Uses `check (band > 0)` rather than the TRD's illustrative `between 1 and 3`, so the migration doesn't need reissuing if `data-engineer`'s B1 band-count call lands on anything but 3 — see the file's own header comment. |

The previous schema — 26 migrations — is frozen in the archive repo (`github.com/AviranGrisaro/locali`, branch `brain`, `06-database/`). `../SALVAGE.md` has a per-group verdict. The short version: the places table and Tel Aviv seed, the neighborhoods/localness tables, and the place-sourcing pipeline are worth carrying over; the friends graph, location shares, and explored cells are not.

Also worth pulling for `hood_density`'s real feed: `06-database/gen_heat.py` and `tel-aviv-places-heat.json` from the archive — the synthetic density generator and its output (data-engineer's B2). Not reachable from this session (old repo not checked out here, remote unauthenticated) — flagged for whoever builds B2 with real environment access.
