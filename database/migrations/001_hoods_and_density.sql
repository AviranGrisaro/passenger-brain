-- 001_hoods_and_density.sql
-- Task: T-031 (Map — Hoods & heat area)
-- TRD:  passenger-brain/prds/map-hoods-heat/TRD.md §3.1, §11 (steps A1-A3)
--
-- First migration in this project. Idempotent (safe to re-run) per
-- database/README.md's convention — every DDL/DML statement below guards
-- against already having been applied.
--
-- Contents:
--   A1 — hoods + hood_density tables, per §3.1, with both check constraints and the FK.
--   A2 — RLS: enabled on both, one public `select` policy each, no write policy.
--   A3 — seed `hoods` with a PLACEHOLDER Tel Aviv polygon set (see note below).
--
-- Forward-compat note (developer's trd-review call, carried into this build):
-- §3.1's illustrative SQL uses `check (band between 1 and 3)`. This migration
-- uses `check (band > 0)` instead. Band *count* is still nominally open per
-- the TRD's §1 framing (an architect amendment to lock it at 3 was queued at
-- trd-review but had not landed as of this build) — a hardcoded upper bound
-- would force a new migration (applied migrations are never edited) the
-- moment data-engineer's B1 call lands on anything but 3 bands. `band > 0`
-- is strictly safer and costs nothing: the client already reads `HeatBand?`
-- off an integer and is indifferent to how many values it can take (§4.1).
--
-- A3 seed-data note:
-- The TRD's real Tel Aviv Hood boundary set is data-engineer's B3 output,
-- salvaged/exported from the old Locali schema (022_create_neighborhoods /
-- 024a_seed_neighborhoods_placeholder per SALVAGE.md). That source is not
-- reachable from this session — the old repo isn't checked out under this
-- workspace and the remote isn't authenticated here (the same access gap
-- data-engineer already flagged in PROGRESS.md for B3). Rather than block
-- A3 entirely or invent precise boundary data and present it as real, this
-- migration seeds a small, explicitly-labeled PLACEHOLDER set — five named,
-- real Tel Aviv neighborhoods with deliberately rough/simplified rectangular
-- rings around their well-known approximate centers, not surveyed polygons.
-- This unblocks C1 (iOS can already build against a hand-authored fixture
-- per §11) and A2/RLS verification without waiting on B3. data-engineer's
-- real export supersedes these rows by id (upsert-shaped, see below) — this
-- migration does not need reissuing when that lands.

-- ---------------------------------------------------------------------------
-- A1: schema
-- ---------------------------------------------------------------------------

create table if not exists public.hoods (
  id          text primary key,             -- stable slug, e.g. 'florentin'
  name        text not null,
  city        text not null default 'tel-aviv',
  polygon     jsonb not null,               -- GeoJSON-flavored ring: [[lng,lat], ...], WGS84, single ring (§3.2 format; §3.1's full-GeoJSON-object framing is B3's to reconcile)
  updated_at  timestamptz not null default now()
);

create table if not exists public.hood_density (
  hood_id     text        not null references public.hoods(id) on delete cascade,
  hour_bucket timestamptz not null check (hour_bucket = date_trunc('hour', hour_bucket)),
  band        smallint    not null check (band > 0),  -- see forward-compat note above; §3.1 illustrates `between 1 and 3`
  primary key (hood_id, hour_bucket)
);

create index if not exists hood_density_hour_idx on public.hood_density (hour_bucket);

-- ---------------------------------------------------------------------------
-- A2: RLS — default-deny, one public read policy each, no write policy at all.
-- The synthetic generator (B2) writes with the service role, which bypasses
-- RLS by construction — no insert/update/delete policy is written on purpose.
-- ---------------------------------------------------------------------------

alter table public.hoods enable row level security;
alter table public.hood_density enable row level security;

drop policy if exists hoods_public_read on public.hoods;
create policy hoods_public_read
  on public.hoods
  for select
  to anon, authenticated
  using (true);

drop policy if exists hood_density_public_read on public.hood_density;
create policy hood_density_public_read
  on public.hood_density
  for select
  to anon, authenticated
  using (true);

-- ---------------------------------------------------------------------------
-- A3: seed `hoods` — PLACEHOLDER set, see note above. Five real, named Tel
-- Aviv neighborhoods; rough rectangular rings around each one's well-known
-- approximate center, not a surveyed boundary. `on conflict do nothing` so
-- this migration stays idempotent and does not clobber rows a later, real
-- seed (data-engineer's B3 export) has already replaced.
-- ---------------------------------------------------------------------------

insert into public.hoods (id, name, city, polygon) values
  ('florentin', 'Florentin', 'tel-aviv',
    '[[34.763,32.053],[34.769,32.053],[34.769,32.059],[34.763,32.059],[34.763,32.053]]'::jsonb),
  ('neve-tzedek', 'Neve Tzedek', 'tel-aviv',
    '[[34.762,32.057],[34.768,32.057],[34.768,32.062],[34.762,32.062],[34.762,32.057]]'::jsonb),
  ('lev-hair', 'Lev HaIr', 'tel-aviv',
    '[[34.771,32.062],[34.778,32.062],[34.778,32.067],[34.771,32.067],[34.771,32.062]]'::jsonb),
  ('old-north', 'Old North', 'tel-aviv',
    '[[34.771,32.085],[34.778,32.085],[34.778,32.091],[34.771,32.091],[34.771,32.085]]'::jsonb),
  ('jaffa', 'Jaffa', 'tel-aviv',
    '[[34.746,32.050],[34.753,32.050],[34.753,32.056],[34.746,32.056],[34.746,32.050]]'::jsonb)
on conflict (id) do nothing;
