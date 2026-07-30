-- 002_synthetic_density_generator.sql
-- Task: T-031 (Map — Hoods & heat area)
-- TRD:  passenger-brain/prds/map-hoods-heat/TRD.md §11 (step B1, B2)
-- Owner: data-engineer. Depends on migration 001 (public.hoods, public.hood_density)
-- landing first — both were authored in parallel per T-031's build-track split.
--
-- Contents:
--   B1 — band thresholds (documented here; count/names are locked at 3 per
--        the TRD's §1 amendment — quiet/moderate/busy. Only the numeric
--        score-to-band cutoffs below are data-engineer's open call).
--   B2 — synthetic density generator: writes 13 rolling absolute-UTC-hour
--        buckets per Hood, diurnal curve computed in Tel Aviv LOCAL time,
--        closes the retention/pruning gap code-reviewer flagged, and is
--        scheduled to actually keep rolling as time advances (a gap the
--        TRD itself didn't specify a mechanism for — data-engineer's own
--        automation call, see the scheduling section at the bottom).
--
-- Idempotent: every object uses `create or replace` / `if not exists` /
-- `on conflict`, safe to re-run, per database/README.md's convention.

-- ---------------------------------------------------------------------------
-- B1: band thresholds
-- ---------------------------------------------------------------------------
--
-- The generator computes a continuous synthetic "activity score" in [0, 1]
-- per Hood-hour (diurnal base curve x per-Hood vibrancy weight + noise, see
-- below) and maps it to one of the three locked bands via these cutoffs:
--
--   score <  0.40                -> 1 (quiet)
--   0.40 <= score <  0.70        -> 2 (moderate)
--   score >= 0.70                -> 3 (busy)
--
-- Reasoning: "busy" is meant to be a genuinely notable state, not a coin
-- flip at a place's own evening peak — `design/map-rendering-spec.md` L42
-- already keys the tourist-trap flag's warning stroke on heat crossing the
-- busy threshold (a sibling PRD is coupled to this being meaningful, not
-- just frequent). Setting the busy cutoff at the top 30% of the score range
-- means only the more "vibrant" Hoods (see hood_vibrancy_weight below) at
-- their actual peak hours (evening, per the diurnal curve) cross it — most
-- Hood-hours land quiet or moderate, matching real foot-traffic shape more
-- than an even three-way split would. Thresholds are stored only here, in
-- SQL, never in the client (TRD §3.1's "band is stored, not computed
-- client-side" contract) — retunable without an app release.

create or replace function public.density_band_for_score(p_score numeric)
returns smallint
language sql
immutable
as $$
  select case
    when p_score >= 0.70 then 3  -- busy
    when p_score >= 0.40 then 2  -- moderate
    else 1                        -- quiet
  end;
$$;

comment on function public.density_band_for_score is
  'B1: score-to-band cutoffs (quiet/moderate/busy locked at 3 bands, TRD §1). Busy pinned at the top 30% of [0,1] deliberately -- it is a warning-worthy state for tourist-trap-flag (map-rendering-spec.md L42), not a default outcome of an even split.';

-- ---------------------------------------------------------------------------
-- B2a: deterministic per-Hood "vibrancy" weight
-- ---------------------------------------------------------------------------
--
-- No schema change requested for this (data-engineer does not own hoods'
-- columns) -- derived instead from a hash of hood_id, deterministic and
-- immutable, so the same Hood always gets the same weight across runs
-- without a new column. Range [0.65, 1.20]: below 1.0 means a Hood's curve
-- never reaches the busy cutoff even at its own peak hour; above 1.0 means
-- it can. Gives the synthetic city a mix of quieter residential Hoods and
-- livelier ones without hand-authoring per-Hood data that would just be
-- invented.

create or replace function public.hood_vibrancy_weight(p_hood_id text)
returns numeric
language sql
immutable
as $$
  select 0.65 + (
    ('x' || substr(md5(p_hood_id), 1, 8))::bit(32)::bigint::numeric / 4294967295.0
  ) * 0.55;
$$;

comment on function public.hood_vibrancy_weight is
  'Deterministic per-Hood multiplier in [0.65, 1.20], hashed from hood_id. Not a real signal -- a synthetic stand-in so the diurnal curve varies by Hood without inventing per-Hood data or requesting a schema column.';

-- ---------------------------------------------------------------------------
-- B2b: the generator itself
-- ---------------------------------------------------------------------------
--
-- Tel Aviv LOCAL time, tz-aware, explicitly pinned (not relying on
-- date_trunc's session-timezone dependency):
--   - `perform set_config('timezone', 'Asia/Jerusalem', true)` pins the
--     session timezone for THIS TRANSACTION ONLY (the `true` third argument
--     is is_local -- it does not leak to the caller's session or any other
--     connection). This makes date_trunc('hour', now()) deterministic
--     regardless of whatever timezone the invoking session/role happens to
--     carry, rather than accidentally relying on Israel's whole-hour DST
--     offset making UTC-vs-local truncation coincide (true today, but a
--     coincidence, not a guarantee -- see the trd-review worklog entry).
--   - The diurnal base curve below is indexed by LOCAL hour-of-day
--     (`... at time zone 'Asia/Jerusalem'`), explicit at the point of use
--     as a second, belt-and-suspenders guarantee independent of the
--     session-level pin above.
--
-- Diurnal base curve (24 values, index 0 = midnight local): low overnight,
-- morning ramp, a lunchtime bump, an afternoon lull, and the real peak in
-- the evening (19:00-22:00) -- a believable, not measured, shape; this is
-- a synthetic feed, not real presence data (TRD §1, strategy's synthetic
-- density call for V1).

create or replace function public.generate_synthetic_density(
  p_horizon_hours int default 13,          -- now .. +12h inclusive = 13 buckets, matches §4.5's query window
  p_retention_buffer_hours int default 2    -- trailing buffer past "now" before a row is pruned
)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  v_anchor_utc timestamptz;
  v_curve numeric[] := array[
    0.05,0.03,0.02,0.02,0.03,0.05,0.10,0.20,   -- 00:00-07:00
    0.30,0.35,0.40,0.45,0.55,0.60,0.55,0.50,   -- 08:00-15:00
    0.48,0.50,0.58,0.68,0.78,0.85,0.80,0.55    -- 16:00-23:00
  ];
begin
  -- Pin this transaction's timezone explicitly -- does not affect the
  -- caller's session (set_config's third argument, is_local, scopes it here).
  perform set_config('timezone', 'Asia/Jerusalem', true);

  v_anchor_utc := date_trunc('hour', now());

  insert into public.hood_density (hood_id, hour_bucket, band)
  select
    h.id,
    v_anchor_utc + (n * interval '1 hour') as hour_bucket,
    public.density_band_for_score(
      least(1.0, greatest(0.0,
        v_curve[ extract(hour from ((v_anchor_utc + (n * interval '1 hour')) at time zone 'Asia/Jerusalem'))::int + 1 ]
          * public.hood_vibrancy_weight(h.id)
          + (random() - 0.5) * 0.08   -- +/- 4% noise so it doesn't look like a pure lookup table
      ))
    )
  from public.hoods h
  cross join generate_series(0, p_horizon_hours - 1) as n
  on conflict (hood_id, hour_bucket)
  do update set band = excluded.band;

  -- Retention/pruning (code-reviewer's trd-review finding, closed here):
  -- rows more than the trailing buffer behind "now" are no longer inside
  -- any client's [now, now+12h] window (TRD §3.4/§4.5) and are deleted
  -- rather than accumulating indefinitely -- location/presence-adjacent
  -- data doesn't get kept past what the feature needs, even synthetic
  -- aggregate rows (passenger-code/CLAUDE.md's minimization rule, applied
  -- here too).
  delete from public.hood_density
  where hour_bucket < v_anchor_utc - (p_retention_buffer_hours * interval '1 hour');
end;
$$;

comment on function public.generate_synthetic_density is
  'B2: synthetic density feed. Upserts 13 rolling absolute-UTC-hour buckets per Hood; diurnal shape computed in Asia/Jerusalem local time via an explicit, transaction-scoped timezone pin (not a session-default assumption). Prunes rows older than the retention buffer trailing "now". Scheduled hourly -- see below.';

-- ---------------------------------------------------------------------------
-- B2c: scheduling -- the gap not specified anywhere else in the TRD
-- ---------------------------------------------------------------------------
--
-- Nothing in §11 (or anywhere else in the TRD) names a mechanism for
-- actually re-running the generator as time advances -- without one, the
-- 13 rolling buckets would be written once and then age out of the
-- [now, now+12h] window with nothing refilling the far end. This is
-- data-engineer's own automation call (not an architect gap): pg_cron
-- scheduling the SQL function directly, not a Supabase Edge Function.
--
-- Why pg_cron over an Edge Function: the generator is pure SQL with no
-- external API call and no ingestion source (it is synthetic, self-
-- contained data) -- an Edge Function would add a network hop, a
-- deployment artifact, and a service-role secret to manage for no benefit
-- over calling the function in-process on a schedule. Revisit this call
-- if/when the synthetic generator is replaced by a real ingestion pipeline
-- that has to call an external feed (database/README.md already flags
-- "scheduled functions" as in-scope for this directory) -- that would
-- justify an Edge Function; this generator does not need one.
--
-- Runs at 5 minutes past every hour (not on the hour) -- gives clear space
-- after the top-of-the-hour boundary so a client's cold-open request never
-- races the write.
--
-- pg_cron must be enabled on the Supabase project (Database -> Extensions
-- in the dashboard) before this applies cleanly -- same Aviran-gated
-- pattern as applying the migration itself; noted here rather than
-- assumed.

create extension if not exists pg_cron;

do $$
begin
  if exists (select 1 from cron.job where jobname = 'generate-synthetic-density-hourly') then
    perform cron.unschedule('generate-synthetic-density-hourly');
  end if;

  perform cron.schedule(
    'generate-synthetic-density-hourly',
    '5 * * * *',
    $cron$select public.generate_synthetic_density();$cron$
  );
end;
$$;
