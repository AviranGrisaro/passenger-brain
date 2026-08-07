-- 009_hoods_aliases.sql
-- Task: unowned finding, `data-engineer`'s 2026-08-07 Tel Aviv Hood coverage-gap
-- follow-up (BOARD.md Unowned findings; prds/hood-dataset/hood-dataset.md
-- Decisions log, 2026-08-07 "Groups 4/5" entry).
--
-- Problem: Tel Aviv has 59 official neighbourhoods (city plan TA/5500);
-- `public.hoods` has 44 distinct geometric polygons. The remaining names are
-- legitimately NOT separate geometries -- they're OSM-identical duplicates of
-- an already-shipped Hood's polygon, or fully contained inside one. A user
-- searching one of those names today gets no match at all, because nothing
-- on `hoods` records the alternate name. data-engineer flagged this and
-- confirmed by grep that no alias/alt-name mechanism exists anywhere in the
-- schema, the source-data contract, or either generated artifact.
--
-- Fix: one additive column. `aliases text[]` -- not a separate
-- `hood_aliases` table, because every case identified so far is a plain
-- alternate name in the same script/locale as `hoods.name` (no per-alias
-- provenance, no distinct-row metadata need). A join table is the right
-- call the day an alias needs its own locale/script/provenance -- not yet,
-- and this column doesn't foreclose adding one later (a table can still be
-- introduced alongside it; nothing here is exclusive).
--
-- `search-quick-filters/TRD.md` sec 3.3/4.2 is the one existing consumer of
-- Hood names for lookup today, and it is entirely client-side (`SearchIndex`
-- folds `Hood.name`, no server-side text search exists) -- so this column's
-- job is just to make alias data available to whatever reads `hoods`
-- (the table directly, and the generated iOS bundle via `build_hoods.py`,
-- which this same change teaches to emit an `aliases` array per Hood).
-- `resolve_hood()` (point -> Hood id, geometric containment) is a different
-- function entirely and has no reason to consult aliases -- it never took a
-- name as input.
--
-- Idempotent per database/README.md convention: `if not exists`-guarded.
-- Additive only -- does not touch id/name/city/polygon/blurb/is_tourist_trap/
-- designated_for_progression on any of the existing 44 rows.

alter table public.hoods
  add column if not exists aliases text[] not null default '{}';

-- No RLS change: `aliases` is just another column on `public.hoods`, which
-- already has RLS enabled with one public `select … using (true)` policy
-- (001 A2) and no write policy. The existing policy is column-agnostic and
-- covers this column with no edit needed.

comment on column public.hoods.aliases is
  'Alternate names that should resolve to this Hood (e.g. "Kfar Shalem" -> neve-eliezer, because Kfar Shalem is OSM-identical to / fully contained inside neve-eliezer''s shipped polygon, not a separate geometry). Empty array = no known aliases. Populated by data-engineer via database/data/hoods-tel-aviv.source.json''s optional per-hood `aliases` field and database/scripts/build_hoods.py -- see hood-dataset/TRD.md sec 3.2/3.3 for the generator contract. Not free text: every entry should be a real neighbourhood/place name a user might search, not a keyword.';
