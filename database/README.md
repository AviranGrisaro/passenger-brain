# database

Supabase Postgres schema for Passenger — migrations, RLS policies, scheduled functions. Owned by the `developer` agent; the `data-engineer` agent requests capabilities here rather than editing directly.

## Rules

- Migrations are `migrations/NNN_short_name.sql`, sequential, never renumbered and never edited once applied.
- Every table gets RLS. A table shipped without a policy is a bug, not a follow-up.
- **Applying a migration is Aviran-gated** — he holds the DB credentials. Write the migration, hand it off, don't apply it.
- No secrets in SQL. Config comes from Supabase project settings.
- Location data is sensitive: don't store more precision or history than the feature needs.

## Status

Empty. Passenger starts at `001`, written from the first approved TRD.

The previous schema — 26 migrations — is frozen in the archive repo (`github.com/AviranGrisaro/locali`, branch `brain`, `06-database/`). `../SALVAGE.md` has a per-group verdict. The short version: the places table and Tel Aviv seed, the neighborhoods/localness tables, and the place-sourcing pipeline are worth carrying over; the friends graph, location shares, and explored cells are not.

Also worth pulling before writing `001`: `06-database/gen_heat.py` and `tel-aviv-places-heat.json` from the archive — the synthetic density generator and its output. The strategy still calls for a synthetic density feed in V1.
