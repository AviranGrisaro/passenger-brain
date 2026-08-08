-- 011_density_band_cast_fix.sql
-- Task: follow-up defect fix on 002_synthetic_density_generator.sql (T-031 B2).
--
-- Found 2026-08-08 by actually running generate_synthetic_density() immediately
-- after applying 002 for the first time. 002 had passed code-review and a
-- security-auditor pass, but had never been executed against a live database
-- until now -- this is a runtime type-resolution error, not something a read of
-- the SQL surfaces.
--
-- The failure:
--   ERROR: 42883: function public.density_band_for_score(double precision)
--          does not exist
--
-- Why: the score expression in 002's insert is
--     v_curve[...] * public.hood_vibrancy_weight(h.id) + (random() - 0.5) * 0.08
-- v_curve is numeric[] and hood_vibrancy_weight() returns numeric, so the first
-- term is numeric -- but random() returns double precision, and numeric + double
-- precision resolves to double precision. least()/greatest() then carry that
-- through, so the argument handed to density_band_for_score() is double
-- precision while the function is declared (p_score numeric). Postgres does not
-- implicitly cast double precision -> numeric when resolving a function call, so
-- the whole insert raises. Verified live: pg_typeof() on the expression returns
-- `double precision`, and pg_proc has exactly one overload, `p_score numeric`.
--
-- Impact if left unfixed: generate_synthetic_density() raises on every call, so
-- the pg_cron job 002 schedules ('5 * * * *') fails every hour, hood_density
-- stays permanently empty, and the whole heat/density feature has no data --
-- silently, since a failing cron job does not surface in the app.
--
-- The fix: one explicit ::numeric cast on the argument. Chosen over widening
-- density_band_for_score() to double precision, or adding an overload, because
-- the cutoffs (0.40 / 0.70) are exact decimal comparisons and numeric is the
-- right type for them -- the float is an artifact of random(), not a deliberate
-- choice. Nothing else in 002 changes.
--
-- 002 is not edited: it has now been applied (2026-08-08), and applied
-- migrations are never edited per database/README.md's rules. This file is the
-- forward fix. `create or replace` preserves the existing revoke on the
-- function, but the revoke is restated below so a fresh apply of this file
-- against a database that never ran 002's revoke still lands in the safe state.

create or replace function public.generate_synthetic_density(
  p_horizon_hours int default 13,
  p_retention_buffer_hours int default 2
)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  v_anchor_utc timestamptz;
  v_horizon_hours int;
  v_retention_buffer_hours int;
  v_curve numeric[] := array[
    0.05,0.03,0.02,0.02,0.03,0.05,0.10,0.20,
    0.30,0.35,0.40,0.45,0.55,0.60,0.55,0.50,
    0.48,0.50,0.58,0.68,0.78,0.85,0.80,0.55
  ];
begin
  v_horizon_hours := greatest(1, least(p_horizon_hours, 24));
  v_retention_buffer_hours := greatest(0, least(p_retention_buffer_hours, 24));

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
          + ((random() - 0.5) * 0.08)::numeric   -- 011: cast fix, see header
      ))::numeric                                 -- 011: cast fix, see header
    )
  from public.hoods h
  cross join generate_series(0, v_horizon_hours - 1) as n
  on conflict (hood_id, hour_bucket)
  do update set band = excluded.band;

  delete from public.hood_density
  where hour_bucket < v_anchor_utc - (v_retention_buffer_hours * interval '1 hour');
end;
$$;

revoke execute on function public.generate_synthetic_density(int, int) from public, anon, authenticated;
