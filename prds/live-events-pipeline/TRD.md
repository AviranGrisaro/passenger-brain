# Live Events Ingestion Pipeline — TRD

**Task:** T-043 · **Status:** ready for `trd-review`
**Owner:** architect · **Date:** 2026-07-31
**PRD:** [`live-events-pipeline.md`](./live-events-pipeline.md) (Draft v1)
**No design spec — pure-build/data, no UX surface.** The client half is [`live-events-overlay`](../live-events-overlay/live-events-overlay.md) (T-034), a separate task with its own design pass.
**Upstream:** [`hood-dataset`](../hood-dataset/hood-dataset.md) (T-040) · **Soft upstream:** [`places-dataset`](../places-dataset/places-dataset.md) (T-042) · **Feasibility:** [`data-eng/live-events-feasibility.md`](../../data-eng/live-events-feasibility.md) (`PAS-5`)

---

## 1. Context

Read the PRD first; nothing here restates it. This document decides the seven things it left open and pins the one contract T-034's client builds against.

**Which source(s) ship is still Aviran's (`PAS-6` item 10) and this TRD does not pre-decide it.** Every structure below is vendor-neutral by construction: exactly one directory in this design is allowed to know a vendor's name (§2.2), and nothing in the schema, the dedup rule, the expiry rule, the ranker, or the client contract mentions one. Adding, swapping, or dropping a feed is an adapter file plus a row in `event_sources`.

**Open calls resolved here:**

| # | Open item (PRD §Technical design / §Assumptions) | Call | Where |
|---|---|---|---|
| 1 | Is `rank` absolute or per-hour? | **Absolute, and time-invariant.** Time fit is a filter, never a rank term — `discovery-engine-spec.md` R1 | §4.3 |
| 2 | Does the ranker run at ingest or at read? | **At ingest**, as a pass after the run's rows land. Read-time ranking is unreproducible and puts unbounded work on the client's cold-open path | §4.3 |
| 3 | Ingest cadence (PRD req 7, `[ASSUMPTION]`) | **Hourly at `:20`.** But the requirement is made true by the *fetch horizon exceeding the serve horizon*, not by the cadence | §4.4, §5.1 |
| 4 | Retention period on expired rows (PRD req 5, `[ASSUMPTION]`) | **90 days past `end_at`**, then hard-deleted. `events` holds no user data of any kind, so this is hygiene, not privacy | §3.5 |
| 5 | Where ingest runs | **Supabase Edge Function on a `pg_cron` schedule.** Migration `002`'s own comment pre-authorizes exactly this case | §2.1, §6 |
| 6 | Event→Hood attribution with no PostGIS | **A SQL `hood_for_point()`, owned here.** `places-dataset` needs the same predicate offline in Python and keeps its own — two implementations, held to **one algorithm spec and one shared fixture**, not unified | §4.1 |
| 7 | Whether the client ever sees an unservable row | **No — the served set is a database view, not a client query with filters** | §4.2 |

**Three things the PRD does not name that this design has to handle** (detail in §8): an event **cancelled or withdrawn at source** is a staleness case distinct from expiry; **`end_at` is absent from many real feeds**, which turns req 2's strict drop into a silent majority-discard; and req 6's allowed input list includes **"proximity"**, which contradicts its own same-order-for-every-device bullet unless proximity means something static.

---

## 2. Architecture

### 2.1 Where each piece runs

```
Supabase Edge Function  "ingest-events"     ← the only component that talks to the outside world
  ├─ adapters/<source>.ts   one per feed. The ONLY vendor-aware code in the system.
  ├─ canonical.ts           CanonicalEvent, required-field validation, dedup key
  └─ index.ts               orchestrate: fetch → normalize → validate → upsert → reconcile → log

Postgres (migrations, database/)
  ├─ events, event_source_links, event_sources, event_ingest_runs      §3
  ├─ hood_for_point() / reattribute_events()                           attribution  §4.1
  ├─ event_rank_score() / recompute_event_ranks()                      ranking      §4.3
  ├─ events_public (view)                                              THE contract §4.2
  └─ pg_cron → pg_net → the Edge Function, hourly                      §4.4

iOS client (T-034, not this TRD)  — reads events_public. Sorts. Truncates. Nothing else.
```

Three boundaries, and they are the whole design:

- **The adapter boundary.** An adapter's only job is `raw source payload → CanonicalEvent[]`. It knows a vendor's URL, auth header, field names, and pagination. It knows nothing about Hoods, dedup, ranking, or the client. Every requirement downstream of `canonical.ts` is written against `CanonicalEvent` and is therefore true for a feed nobody has chosen yet.
- **The database boundary.** Attribution, dedup collapse, expiry, withdrawal, ranking, and the served-set filter are all **in Postgres**, not in the Edge Function. The Edge Function is a fetcher and a normalizer. This is what makes a second source cost an adapter rather than a second copy of the business rules — and it is what lets `data-engineer` retune the ranker in SQL without redeploying anything, the same property migration `002` bought for density thresholds.
- **The `events_public` boundary.** The client cannot query a row this pipeline has not decided to serve, because the base table denies it. "The client applies no business logic" (PRD §Technical design) is structural here, not a convention T-034 has to honour.

### 2.2 What is allowed to know a vendor's name

Exactly two places: `functions/ingest-events/adapters/*.ts`, and rows in `event_sources`. Nowhere else — not a column name, not a CHECK constraint, not the view, not the ranker, not a migration comment beyond a factual note. `trd-review` should treat a vendor name appearing outside those two places as a blocking finding; that is the mechanical form of "written source-agnostically."

### 2.3 Repo placement

`passenger-brain/database/functions/ingest-events/`. `database/README.md` already declares "scheduled functions" in scope for this directory, and the pipeline's SQL and its fetcher are one deliverable that must version together. **`database/README.md` needs a `functions/` row in its Layout section** — `developer`'s to add with A1. Reviewers may overturn the location; nothing else in this TRD depends on it.

---

## 3. Data model

Four new tables. No table here holds, derives from, or can be joined to any user — there is no identity in V1 and this pipeline introduces none. **All four `create table` and every `create index` below use `if not exists`**, matching migrations `001`/`002`'s idempotency convention — a bare `create table`/`create index` would fail on re-run and this TRD's earlier drafts omitted the guard. Migration number: **do not hardcode.** `003` is already claimed by T-033's TRD, and T-040/T-042 have TRDs in flight that will claim more; `developer` takes the next unclaimed number at write time and records it in `database/README.md`'s Status table (§9, and see the board note in §8).

### 3.1 `event_sources` — the recorded decision, in data

```sql
create table if not exists public.event_sources (
  key                      text primary key,          -- 'some-feed'
  display_name             text not null,
  enabled                  boolean not null default false,
  tier                     smallint not null default 2 check (tier > 0),
  default_duration_minutes int null,                  -- see §8 F2. null = source always supplies end time
  coverage_note            text not null,             -- what this feed does and does not cover (PRD req 1)
  terms_verified_at        timestamptz null,
  terms_note               text null,
  last_success_at          timestamptz null,
  created_at               timestamptz not null default now(),
  constraint enabled_requires_verified_terms
    check (not enabled or terms_verified_at is not null)
);
```

Two of PRD req 1's three bullets are enforced rather than asserted. **A source cannot be pulling data without its terms having been verified** — the CHECK makes "no source is integrated on an unverified access assumption" a constraint, not a promise in a doc. `enabled` defaults to `false`, so a source never starts ingesting merely by existing. `coverage_note` is `not null`, so req 1's "the coverage each one does and does not give" has a mandatory home; the ticketed-skew disclosure lands there and in the `trd-review` hand-off, not at launch.

### 3.2 `events` — one row per real-world event

```sql
create table if not exists public.events (
  id                uuid primary key default gen_random_uuid(),
  dedup_key         text not null unique,                          -- §4.5
  name              text not null,
  start_at          timestamptz not null,
  end_at            timestamptz not null,
  end_at_estimated  boolean not null default false,                -- §8 F2
  lat               double precision not null,
  lng               double precision not null,
  venue_name        text null,
  hood_id           text null references public.hoods(id) on delete set null,
  category          text null,
  rank              real not null default 0,
  primary_source    text not null references public.event_sources(key),
  first_ingested_at timestamptz not null default now(),
  ingested_at       timestamptz not null default now(),            -- last time a source confirmed this row
  withdrawn_at      timestamptz null,
  constraint end_after_start check (end_at > start_at)
);

create index if not exists events_start_at_idx on public.events (start_at) where withdrawn_at is null;
create index if not exists events_end_at_idx   on public.events (end_at);
create index if not exists events_hood_idx     on public.events (hood_id);
```

Six decisions inside that schema:

- **`hood_id` is nullable, and an unattributed event is stored, not dropped.** PRD req 3's second bullet says an event in no Hood "is not ingested." The *observable* requirement — it never reaches the map — is met by the view (§4.2). Storing it with `hood_id = null` is what makes req 3's **third** bullet ("attribution is re-resolvable: a Hood boundary correction re-attributes existing events") actually possible; a dropped row cannot be re-attributed by anything. Same reasoning as req 5's own no-hard-delete-on-expiry rule. **Deliberate deviation from the PRD's literal wording, flagged for `trd-review`.**
- **`on delete set null`, not `restrict` — a stated divergence from `places.hood_id`, not a silent one, and the more correct choice here rather than a defect.** `hood-dataset/TRD.md` (T-040, §8 risk table) expects `events.hood_id` to follow `places.hood_id`'s `restrict` rule; here it does not, deliberately. `places.hood_id` must be `restrict` because a place silently losing its Hood is data loss — curated, hand-authored rows meant to always resolve to exactly one Hood. `events` rows are the opposite in kind: numerous, machine-ingested, ephemeral (90-day retention, §3.5), and already re-attachable by design — `hood_id = null` is a normal, expected state from the moment of ingest (the bullet above), not a failure state a constraint should guard. Concretely, `restrict` here would **break T-040's own build step**: `hood-dataset/TRD.md` §3.3 prunes stale Hood rows with a scoped `delete from public.hoods where city = 'tel-aviv' and id not in (...)` whenever the real dataset replaces placeholder rows; any placeholder Hood with attributed events would make that `delete` fail outright under `restrict`, wherever `hood_density` cascades cleanly today. `reattribute_events()` (§4.1) is the designed repair path regardless of cause — a Hood-row deletion nulls the affected rows exactly as a boundary revision would, and the next pass resolves what it can.
- **No `place_id` column in this migration.** PRD says `places-dataset` is needed "only if venue matching is wanted; no P0 here requires it." Adding a nullable FK to a table that does not exist yet would make this migration depend on T-042 for no P0 benefit. It is additive later (§4.3's venue-corroboration rank term degrades to zero without it).
- **`id` is a uuid, not a slug.** Hoods and places are hand-curated and get stable slugs; events are machine-ingested and numerous. The uuid is stable across runs because the row survives upsert-on-`dedup_key` — T-034's marker identity does not churn between fetches.
- **`ingested_at` means "last confirmed by a source,"** which is what req 7's freshness bound needs; `first_ingested_at` is kept separately so "how long have we known about this" stays answerable.
- **`primary_source` is a FK, not free text.** A row cannot name a source that was never registered and terms-checked.

### 3.3 `event_source_links` — dedup, and req 4's uniqueness

```sql
create table if not exists public.event_source_links (
  source          text not null references public.event_sources(key),
  source_event_id text not null,
  event_id        uuid not null references public.events(id) on delete cascade,
  last_seen_at    timestamptz not null default now(),
  primary key (source, source_event_id)
);
create index if not exists event_source_links_event_idx on public.event_source_links (event_id);
```

This is the whole of req 4. `(source, source_event_id)` is the primary key, so re-ingesting a source can never duplicate. Two sources carrying the same real event produce **two link rows pointing at one `events` row**, so the client sees one marker and provenance is not lost. `last_seen_at` is what the withdrawal reconcile reads (§5.3).

No raw source payload is stored. Debugging belongs in the function's logs, not in a table that would then need a retention and PII policy of its own for third-party organiser data we have no reason to hold.

### 3.4 `event_ingest_runs` — req 8's second bullet, and P1's health readout

```sql
create table if not exists public.event_ingest_runs (
  id           bigint generated always as identity primary key,
  source       text not null references public.event_sources(key),
  started_at   timestamptz not null default now(),
  finished_at  timestamptz null,
  outcome      text not null default 'running'
               check (outcome in ('running','success','partial','failed','skipped')),
  window_start timestamptz null,
  window_end   timestamptz null,
  rows_fetched int not null default 0,
  rows_written int not null default 0,
  rows_dropped int not null default 0,
  drop_reasons jsonb not null default '{}'::jsonb,   -- {"missing_end_at": 12, "no_hood": 3, ...}
  error        text null
);
```

This table is **P0, not the PRD's P1**, because req 2 ("dropped at ingest **and counted**") and req 8 ("a source that has returned nothing for a full day is logged, not silently absorbed") are both unsatisfiable without it. The P1 health readout is then a `select`, not new work. `outcome` is also the safety interlock for withdrawal (§5.3): only `'success'` — a complete fetch — may mark anything withdrawn.

### 3.5 Retention

The same scheduled job deletes `events` rows whose `end_at` is more than **90 days** past, cascading their links. `event_ingest_runs` keeps 180 days. **[ASSUMPTION]** — the PRD leaves the period unstated; 90 days keeps the health and dedup-quality window meaningful and is product's to override. Worth stating plainly: nothing in this feature stores a user coordinate, a device id, or anything derived from one, so retention here is cost and hygiene, not the location-minimisation rule that governs the client.

---

## 4. Contracts

`developer` and `data-engineer` build against this section and do not need each other's code. T-034's `ios-developer` needs **only §4.2**.

### 4.1 Hood attribution — one algorithm spec and one fixture shared with `places-dataset`, two implementations

```sql
-- Even-odd ray casting over hoods.polygon's flattened ring, bbox prefilter.
-- STABLE (depends on table contents), not IMMUTABLE.
create function public.hood_for_point(p_lng double precision, p_lat double precision)
  returns text language plpgsql stable;

-- Re-runs attribution. Called after any Hood geometry revision. Returns rows changed.
create function public.reattribute_events(p_hood_id text default null) returns int;

revoke execute on function public.hood_for_point(double precision, double precision),
                          public.reattribute_events(text)
  from public, anon, authenticated;
```

The `revoke` is not optional, same reasoning as §4.3's: Postgres grants EXECUTE to PUBLIC on every new function and Supabase auto-exposes each as a PostgREST RPC — the exact HIGH finding `security-auditor` raised on migration `002`. `reattribute_events()` is the sharper of the two exploits: it performs a bulk `update` across `events` and, without this revoke, would be callable as `rpc/reattribute_events` with the app's public anon key — an unauthenticated write-amplification endpoint. It is currently blunted only *implicitly*, by `events`' own RLS (§4.2) denying the row-level write the function would otherwise perform — exactly the kind of accidental protection §4.3 already warns against relying on: if any future migration ever grants `authenticated` a narrower write on `events`, this reopens silently with nothing here having changed. `hood_for_point()` is read-only and lower-risk on its own, but gets the identical treatment for the same reason nothing in §4.3 was left ungated: a reviewer should never have to reason about which of a file's functions "happen to be" safe.

**PostGIS stays disabled.** T-031's TRD §2.3 turned it down and said enabling it later is additive; this is the first server-side spatial need, and it still does not justify it. Ray casting over dozens of single-ring polygons is trivial at this scale, and enabling an extension is an Aviran-gated dashboard action (migration `002`'s `pg_cron` note is the precedent for that friction). Rejecting PostGIS also keeps `hoods.polygon`'s stored shape exactly as migration `001` committed it.

**`places-dataset` req 1 needs the identical predicate** ("the stored `hood_id` equals the Hood whose polygon contains the place's coordinates — verified at authoring time"). An earlier draft of this TRD called that "one implementation, two consumers," with whichever task built first owning the function. **That was wrong, and `trd-review` corrected it** — `developer`, `data-engineer` and `code-reviewer` all reached the same reading independently across T-040's, T-042's and this task's reviews. The resolution:

**Two implementations. Both necessary. Neither unifiable.**

| | T-040 / T-042 | T-043 (this task) |
|---|---|---|
| Where | `database/scripts/validate_dataset.py` | `public.hood_for_point()` |
| Language | stdlib Python | `plpgsql`, inside Postgres |
| When | offline, authoring time, once per dataset edit | live, at ingest, per event, hourly |
| Reads | the checked-in authored Hood source file | the live `hoods` table |
| DB credentials | **none, by design** (`hood-dataset/TRD.md` §2.1) | runs inside the database |

No bridge exists in either direction, and none is proposed anywhere: a cron-triggered Deno Edge Function shelling out to a Python subprocess per ingested event does not belong in a hot path, and pointing the offline validator at a live database reintroduces exactly the Aviran-gated `DATABASE_URL` dependency T-040 inverted its whole pipeline to escape. Forcing one implementation would break one of the two consumers.

**What is actually shared, and is binding on both sides:**

1. **One algorithm spec, stated identically in all three TRDs** — closed single-ring WGS84 `[[lng,lat],…]` (migration `001`'s committed format), even-odd ray cast, bbox prefilter, and **on-boundary → no Hood**. `hood_for_point()` returns `null` for a point exactly on a ring edge or vertex, matching `point_strictly_inside`'s `False` (`hood-dataset/TRD.md` §2.3 predicate 1). This is pinned as a value, not left to each implementation's rounding: without it, a place and an event at the identical coordinate on a shared Hood edge attribute differently, which is the precise bug this section exists to prevent and the one nobody would find by inspection.
2. **One checked-in fixture file** — `database/data/fixtures/hood-containment-cases.json`, point→expected-`hood_id` cases (strictly inside, outside, on-edge, on-vertex, in-bbox-outside-ring, concave notch, shared edge between two adjacent Hoods, swapped lat/lng), **asserted against both implementations** (§9 A3 here; `places-dataset/TRD.md` §9 B2a; `hood-dataset/TRD.md` §9 B1). Whichever task builds first writes the file; neither side adds a case without adding it for both. A boundary-case fix in one language cannot then silently stay wrong in the other.

Flagged for both `trd-review`s (§8 F7).

A third implementation of this predicate already ships — `HoodHitTester.swift`, client-side, for tap targets. That is a different job (44pt tolerance, screen space), is not a candidate for consolidation, and is **not** held to the fixture above. The database is authoritative for attribution; the client never re-attributes anything.

### 4.2 `events_public` — the only thing the client may read

**`with (security_invoker = false)` requires Postgres 15+** (the `security_invoker` view option was added in that release; on an older server this clause is a syntax error, not a silent no-op). **Needs confirming against this project's actual Supabase Postgres version before A2 is built** — Supabase's default tier has shipped 15+ for a while, but no TRD in this project has stated the confirmed version, and this is the first clause anywhere in the schema that depends on one. If the project is on an older version, the fallback is a `security definer` function wrapping the same `select` instead of the view option — same access boundary, different syntax — not a redesign.

```sql
create view public.events_public
with (security_invoker = false) as
select e.id, e.name, e.start_at, e.end_at, e.lat, e.lng,
       e.venue_name, e.hood_id, e.category, e.rank,
       s.display_name as source_name
from public.events e
join public.event_sources s on s.key = e.primary_source
where e.withdrawn_at is null
  and e.hood_id is not null
  and e.end_at > now()
  and e.rank >= public.event_rank_floor();

revoke all on public.events, public.event_source_links,
               public.event_sources, public.event_ingest_runs
  from anon, authenticated;
grant select on public.events_public to anon, authenticated;
```

RLS is enabled on all four base tables with **no policy of any kind** — denial by absence, the same idiom migration `001` used for writes. The view is the access-control boundary and is therefore deliberately `security_invoker = false`. **This inverts `001`'s public-read-policy pattern and reviewers should expect the Supabase linter to flag `security definer view`.** It is the right shape here because the filter *is* the contract: expiry, withdrawal, attribution and the selection floor cannot be forgotten by a caller, and the columns the client has no business seeing (`dedup_key`, `primary_source`, `ingested_at`, `end_at_estimated`) are not projected. It exposes no user-scoped data because none exists. `security-auditor` should confirm the base-table revokes independently — migration `002`'s HIGH finding was exactly a default grant nobody revoked.

**Required build-time check, not just stated intent:** the four tables are `events`, `event_sources`, `event_source_links`, `event_ingest_runs`. A1/A2's migration must issue `alter table ... enable row level security` on **all four individually**, and `code-review`/`security-auditor` must confirm all four — not three-of-four — by querying `pg_class.relrowsecurity` (or the Supabase dashboard's RLS column) for each table name explicitly before sign-off. A table that quietly ships without its own `enable row level security` line is invisible until something queries it directly through PostgREST, the same silent-until-probed failure mode as an unrevoked function.

Client request (T-034, mirroring T-031 §4.5's shape — one fetch alongside the density load, re-filtered locally per hour):

```
GET {supabase_url}/rest/v1/events_public
    ?select=id,name,start_at,end_at,lat,lng,venue_name,hood_id,category,rank,source_name
    &start_at=gte.{anchorHour ISO8601 UTC}
    &start_at=lt.{anchorHour + 13h ISO8601 UTC}
    &order=rank.desc
Headers: apikey: <anon>, Authorization: Bearer <anon>
```

Byte-identical for every device. No parameter carries a location, a device id, or anything user-specific — the same property T-031 §3.3 established, preserved here.

**Three obligations this contract puts on T-034, which it must build and this TRD cannot:**
1. Re-filter the cached payload on `end_at > now()` before every render (PRD req 5, second bullet). The view cannot protect a payload the client already holds.
2. Apply the on-screen marker cap by truncating the `rank`-sorted list. The cap is T-034's number; this pipeline does not enforce one.
3. `source_name` is projected **so attribution is possible without a schema change**. Whether the sheet must display it is a per-source ToS question nobody has answered — see §8 F4.

### 4.3 `rank` — what it is, at a level the client can trust

**Definition, normative:** `rank` is a `real` in `[0, 1]`. Higher means "surface this sooner." It is **comparable across the entire served window and across every Hood** — one scale, no scoping.

Four guarantees the client may rely on without knowing anything about the algorithm:

- **Deterministic.** Same stored inputs, same value. No randomness, no clock term, no per-request computation. Two devices requesting the same hour receive the same order (PRD req 6).
- **No per-user input exists.** There is no identity, no profile store, and no request parameter that could carry one. Non-personalization is structural, not a policy the ranker chooses to honour.
- **Time-invariant.** `rank` contains no recency, imminence, or decay term. *Time fit is a hard filter, not a weight* — `discovery-engine-spec.md` R1, verbatim. This is what resolves the PRD's absolute-vs-per-hour question: rank is **absolute**, and the per-hour behaviour the overlay wants falls out entirely of the window filter plus the client's hour bucketing. A per-hour ordinal would need a row per (event, hour) for any multi-hour event, for no gain.
- **Selection happens before the client sees anything.** `event_rank_floor()` removes the long tail inside the view. PRD req 6's pass condition — the top set for a busy Friday must not be "everything ingested, in time order" — is a property of the pipeline, and the client truncating to a marker cap is a second, independent bound on top of it.

The seam, mirroring `density_band_for_score()` in migration `002` — weights live in SQL, retunable without an app release or a function redeploy:

```sql
-- Pure. IMMUTABLE. No now(), no random(), no table reads. data-engineer owns the weights.
create function public.event_rank_score(p_features jsonb) returns real language sql immutable;

-- The pass. Recomputes rank for every non-withdrawn, unexpired row, every cycle,
-- so a weight change propagates without a backfill migration.
create function public.recompute_event_ranks() returns int;

-- The selection floor. One value, one place, changed by migration.
create function public.event_rank_floor() returns real language sql immutable;

revoke execute on function public.event_rank_score(jsonb),
                          public.recompute_event_ranks(),
                          public.event_rank_floor()
  from public, anon, authenticated;
```

The `revoke`s are not optional: Postgres grants EXECUTE to PUBLIC on every new function and Supabase auto-exposes each as a PostgREST RPC — the exact HIGH finding `security-auditor` raised on migration `002`. A callable `recompute_event_ranks()` is an unauthenticated write-amplification endpoint.

**Permitted feature inputs to `p_features` (all generic, all static):** source tier; record completeness (has venue, has category, has description); category weight; source-supplied popularity where the feed carries one, normalized; venue corroboration against curated `places` once T-042 lands; whether the event's Hood is `designated_for_progression`. **Never raw mention or ticket volume as a ranking input** — `discovery-engine-spec.md` R2 ("that rebuilds TripAdvisor and surfaces tourist traps"). The coefficients are `data-engineer`'s call (B4), exactly as T-031 left band thresholds to B1.

**"Proximity" is not a viewer-relative term.** PRD req 6 lists proximity among allowed inputs and, two bullets later, requires every device to receive the same order. Both cannot hold if proximity means distance-to-viewer. Resolved: proximity may only mean **static** centrality — distance to the Hood centroid, or Hood designation. Flagged as a finding, not decided silently (§8 F3).

### 4.4 The scheduled run

```
pg_cron  '20 * * * *'   →  pg_net POST  {project}/functions/v1/ingest-events
                            Authorization: Bearer <service key read from Vault>
```

At `:20`, not `:05` — migration `002`'s density generator already owns `:05`, and the two should not contend. Hourly is the **[ASSUMPTION]**; req 7's real guarantee does not depend on it (§5.1).

The service key is read from `supabase_vault` at cron-schedule time and **never inlined into the `cron.job` command**, which is a readable table. `pg_net` and Vault both need enabling on the project — the same Aviran-gated dashboard step `002` already flagged for `pg_cron`, and it must be named in the hand-off, not discovered at apply time.

**`pg_net`'s own internal tables need the identical check as the `cron.job` table, and this TRD did not previously say so.** `pg_net` logs every outbound call it makes — request included — into its own schema (`net.http_request_queue`, `net._http_response`). The call this section describes carries the service-role Bearer token as a request header; if `anon` or `authenticated` ever had `select` on those tables, the same secret this paragraph protects by routing through Vault would leak straight back out through a different table entirely. **Required build-time check for A4:** confirm neither `anon` nor `authenticated` holds any grant on the `net` schema or its tables. `pg_net`'s default install does not grant them, but that must be verified against the actual project after enabling — not assumed from the extension's documentation — the same discipline §4.2 requires for the four event tables' RLS.

**Concurrency:** each run takes a per-source advisory lock. An invocation that finds the lock held exits immediately and writes an `outcome='skipped'` row. A slow feed can therefore never produce two interleaved runs against the same source, which is what would make the withdrawal reconcile unsafe.

### 4.5 `CanonicalEvent` and the dedup key

```ts
// canonical.ts — the vendor-neutral core. Every adapter returns this and nothing else.
type CanonicalEvent = {
  sourceEventId: string;
  name: string;
  startAt: string;          // ISO 8601, absolute, with offset. Never a local hour-of-day.
  endAt: string | null;     // null → §8 F2's per-source fallback, or drop
  lat: number; lng: number;
  venueName?: string;
  category?: string;
  popularity?: number;      // normalized 0..1 by the adapter, or omitted
};
```

Validation runs **once, in `canonical.ts`**, not per adapter: a record missing `name`, `startAt`, resolved `endAt`, `lat`, `lng`, or `sourceEventId` is dropped, and its reason is incremented in the run's `drop_reasons`. Never written with a placeholder (PRD req 2).

**Dedup key**, computed at ingest, deterministic and re-derivable:

```
dedup_key = sha256(
    lower(strip_punctuation(collapse_whitespace(name)))
  + '|' + to_char(start_at rounded to nearest 30 min, 'YYYYMMDDHH24MI')
  + '|' + geohash(lat, lng, precision 7)        -- ~150m cell, i.e. "same venue"
)
```

Upsert is `on conflict (dedup_key)`. Two sources carrying one event collapse; the second source adds a link row and, if its `tier` is better, may take over `primary_source`.

This catches same-name/same-time/same-venue duplicates and **misses** rewordings — "DJ X @ Club Y" against "Club Y presents DJ X". That is a stated limit, not a hidden one; req 4's pass condition is a human check across two overlapping sources and will find them. The upgrade path is a `pg_trgm` similarity pass that merges rows, which is purely additive because the link table already models many-sources-to-one-event. Rejected for V1: it needs an extension, a threshold nobody can tune before real Tel Aviv data exists, and a merge that is far harder to undo than a missed merge is to live with.

---

## 5. Flow

### 5.1 The main path, one cycle

```
pg_cron :20 → pg_net → ingest-events
  for each event_sources row where enabled:
    advisory lock (held? → log 'skipped', next source)
    open event_ingest_runs row (outcome='running', window = [now, now + 7 days])
    adapter.fetch(window)            → raw payloads, paginated
    canonical.normalize()            → CanonicalEvent[]
    validate()                       → drops counted into drop_reasons
    upsert on dedup_key              → events row + event_source_links row, ingested_at = now()
    hood_for_point(lng, lat)         → events.hood_id (null is stored, not dropped — §3.2)
    reconcile withdrawals            → ONLY if the fetch completed (§5.3)
    close run (outcome, counts); event_sources.last_success_at = now() on success
  recompute_event_ranks()            → one pass, after every source has landed
  prune retention (§3.5)
```

**The fetch horizon is `now → +7 days`; the serve horizon is `now → +12h`.** That gap is the actual mechanism behind req 7, and it is stronger than any cadence: an event published by a source before its start time is already in the table long before the map's window reaches its hour, so the "present when the map reaches that hour" bullet holds even if a cycle is missed entirely. The hourly cadence only bounds how quickly a *newly published* or *withdrawn* event is reflected.

Ranks are recomputed after **all** sources land, not per source, so cross-source terms (corroboration, source-tier takeover) see the complete picture.

### 5.2 Expiry — four layers, none of them a scheduled job

An expired listing being "worse than an empty shelf" is the failure this feature is most likely to have, so it is defended in depth and never by a job that could fail to run:

| Layer | Mechanism | Catches |
|---|---|---|
| 1 | `end_at` is `not null`, `check (end_at > start_at)` | An event with no knowable end never enters |
| 2 | `events_public` filters `end_at > now()` | Everything served, continuously. **Nothing runs; nothing can be forgotten** |
| 3 | Client re-filters its cached payload on `end_at` (T-034's build) | A stale cache resurrecting a finished event |
| 4 | `withdrawn_at` set by reconcile (§5.3) | Cancelled or pulled at source — not an expiry case at all |

Layer 2 is the important one and it is why the served set is a view: expiry is a property of the query, not of a job's last successful run.

### 5.3 Withdrawal — the case the PRD does not name

An event cancelled or removed at source does not expire; its `end_at` is still in the future. Without handling, the map advertises a cancelled event until its scheduled end.

After a **complete, successful** fetch for one source over window `W`, any `event_source_links` row for that source whose linked event starts inside `W` and whose `last_seen_at` predates this run is withdrawn: the link is deleted, and if the event has no links left, `events.withdrawn_at = now()`.

**The `outcome='success'` gate is load-bearing.** A partial page, a timeout, or an auth failure returns fewer events and would otherwise withdraw the entire feed in one cycle — turning a transient source outage into a wiped map. `'partial'` and `'failed'` runs upsert what they got and reconcile nothing. Nothing is hard-deleted (PRD req 5); a re-appearing event un-withdraws on its next sighting.

### 5.4 Degraded and empty paths — every one of them is a valid empty set

| Condition | Behaviour |
|---|---|
| Source unreachable / auth fails | Run `outcome='failed'`, error logged, no withdrawal. Existing rows keep serving. |
| Source returns zero rows | Run `outcome='success'`, `rows_fetched=0`. Reconcile *does* run — a genuinely emptied feed is a real withdrawal. |
| No source enabled at all | View returns zero rows. Valid. The state V1 ships in if `PAS-6` item 10 does not land (PRD req 8, `live-events-overlay` req 5). |
| Every event ranked below the floor | View returns zero rows. Valid — a ranker that rejects everything is a tuning problem, visible in the review artifact (§9 B5), never an error the client renders. |
| Hood geometry is still placeholder | Nearly every event gets `hood_id = null` and is not served. **Not a silent failure** — it shows as a `no_hood` spike in `drop_reasons`. See §8 R1. |
| Source enabled but silent for 24h | `last_success_at` stale → the health check (§9 B6) raises it. The map does not blank. |

A source outage never blanks the served set. The accepted degradation is that **withdrawals stop being detected** while a source is down, which is why the health check is a P0 build step rather than a nicety.

---

## 6. Third-party & dependencies

| Candidate | Call |
|---|---|
| **Supabase Edge Function** vs. pure SQL + `pg_net` | **Edge Function.** Migration `002`'s own comment already made this call in advance: *"Revisit this call if/when the synthetic generator is replaced by a real ingestion pipeline that has to call an external feed... that would justify an Edge Function."* This is that case. `pg_net` is fire-and-forget with responses landing in a table you poll — no retry ergonomics, no pagination, JSON reshaping in plpgsql, and source API keys living in the database. `pg_net` is still used, but only as cron's outbound trigger. |
| **Edge Function** vs. GitHub Actions / an external worker | **Edge Function.** No CI-based option is available: neither repo has a git remote (L-015), so there is no runner to schedule anything from. An external worker means a new host, a new account, and a new secret store — all Aviran-gated for no capability gain. |
| **PostGIS** | **Still not enabled** (§4.1). |
| **`pg_trgm`** fuzzy dedup | **Not in V1** (§4.5). Additive later. |
| The event feed itself | **Aviran's, not this TRD's** — `PAS-6` item 10. Any paid tier, account, or credential is Aviran-gated by standing rule. |

**Nothing here adds a vendor.** Edge Functions are part of the existing Supabase project **[ASSUMPTION]** — `ios-developer`/`developer` should confirm against the project's plan before A4, since it is the one item that could quietly become a cost.

**Needs enabling on the Supabase project before this applies cleanly** (Aviran-gated, same shape as `002`'s `pg_cron` note — name it in the hand-off, do not discover it at apply time): `pg_net`, `supabase_vault`, and `pg_cron` (already required by `002`). Plus one Edge Function secret per enabled source, set through the Supabase dashboard or CLI — **never committed, never echoed** (`CLAUDE.md`).

**Task dependencies:** `hood-dataset` (T-040) is a hard upstream — attribution against `001`'s five placeholder rectangles drops nearly everything (§5.4). `places-dataset` (T-042) is soft: only §4.3's venue-corroboration term wants it, and that term degrades to zero. This pipeline **blocks** `live-events-overlay`'s real-data path; T-034 remains independently buildable against an empty set by its own req 5.

---

## 7. Rollout & migration

- **No feature flag is built, because `event_sources.enabled` already is one.** Per-source, in data, flipped with an `update` — no deploy, no release, no migration. The whole-layer off switch is "no source enabled," and its behaviour is the specified empty state.
- **Applying the migration is Aviran-gated** (`database/README.md`). `developer` writes and hands off, and the hand-off must name the three extensions and the per-source secret.
- **Deploying the Edge Function is also Aviran-gated** — it needs the Supabase CLI and project credentials no agent holds. This is a second gate `002` did not have; do not report the pipeline as running until both have happened (`CLAUDE.md` Safety 9).
- **Ship order:** schema and view first, with zero sources enabled. The view returning an empty set is a correct, servable state, so T-034 can integrate against a real endpoint before any feed exists. First source enabled only after its terms are verified — the CHECK enforces it.
- **Backward compatibility:** none required. New tables, new view, nothing existing changes. A second source is additive: one adapter file, one row, no schema change, no client release.

---

## 8. Risks, findings & alternatives

**Findings — things the PRD does not resolve, surfaced rather than decided around:**

- **F1 — Storing unattributed events deviates from req 3's literal wording.** §3.2. The observable requirement (never served) holds; the deviation is what makes req 3's own re-attribution bullet achievable. Needs `trd-review` ratification.
- **F2 — Req 2's strict drop on a missing end time may silently discard most of a real feed.** Many listing feeds publish a start and no end. As written, every such record is dropped and counted, and a source could ingest near-zero rows while every requirement passes. The schema carries the fix — `event_sources.default_duration_minutes` plus `events.end_at_estimated`, so a derived end is never mistaken for source truth — but **whether to use it is product's call, not architecture's.** This TRD builds strict-drop as specified and leaves the columns in place. Escalating rather than quietly relaxing a P0.
- **F3 — Req 6's "proximity" contradicts its own same-order-for-every-device bullet.** Resolved as static centrality only (§4.3). If Aviran meant viewer-relative, that is the personalization question `live-events-overlay` already escalated, not a ranking tweak.
- **F4 — Source attribution may be a ToS obligation with no surface.** Some feeds require visible "powered by" credit. T-034's sheet renders name, time, location, route — no source line. `source_name` is projected so the client *can* comply without a schema change, but whether it must is unanswered and depends on which source lands. **Product's, alongside `PAS-6` item 10.**
- **F5 — A long-running event only ever renders in its start hour.** `live-events-overlay` req 1 buckets on start time, so a six-hour festival vanishes from the map an hour after it begins while still running. That is T-034's specified behaviour and not this TRD's to change; the data supports either reading (`start_at` and `end_at` are both served). Worth product's read.
- **F6 — Migration numbering is contended.** Four TRDs (T-033, T-040, T-042, this one) are in flight and each needs a migration. `003` is claimed by T-033. Numbers are assigned at write time and recorded in `database/README.md`; **for `chief-of-staff`'s board, not mine to sequence.**
- **F7 — `hood_for_point()` is needed identically by `places-dataset`, and it is *not* the same implementation. Resolved at `trd-review`, correcting this TRD's own earlier claim.** This document originally said "one implementation, two consumers — whichever builds first owns it." `developer`, `data-engineer` and `code-reviewer` independently found that unbuildable: T-040/T-042's check is stdlib Python running offline over authored files with no DB credentials by design, and this task's is `plpgsql` running live inside Postgres against the `hoods` table. **Both are kept.** What is shared is one algorithm spec (including **on-boundary → no Hood**) and one checked-in point→expected-`hood_id` fixture asserted against both implementations — see §4.1. `hood-dataset/TRD.md` §2.2 carried the mirror-image error ("`validate_dataset.py` is called by T-043's build") and is corrected in step. **No longer open; A3 builds against §4.1's two-implementation wording.**

**Risks:**

| Risk | Mitigation / decision |
|---|---|
| **R1** — Placeholder Hood geometry makes this pipeline unverifiable end to end | Hard dependency on T-040, stated in the PRD and here. Visible as a `no_hood` spike in `drop_reasons`, not a silent zero. Do not read a green ingest run against `001`'s five rectangles as validation. |
| **R2** — Commercial/ticketed skew if only a ticketing feed lands | Not an engineering problem and not fixable here (`PAS-5`: a data-access gap, not a build-hours gap). `coverage_note` is `not null` so the skew is recorded per source; disclosure to Aviran is `PAS-6` item 10 and precedes build. |
| **R3** — The dedup key misses reworded titles | Stated limit (§4.5). Req 4's human pass condition is the detector. `pg_trgm` upgrade is additive. |
| **R4** — A source outage silently stops withdrawal detection | Accepted, and the reason the 24h health check (B6) is P0 rather than P1. The map degrades to slightly-stale, never to blank. |
| **R5** — `security definer` view will be flagged by the Supabase linter and looks like `002`'s HIGH finding | Deliberate and documented (§4.2): the view *is* the access boundary, base tables are revoked, no user data exists in any of them. `security-auditor` verifies the revokes independently rather than trusting the view. |
| **R6** — A ranker tuned before real data degrades to "show everything" | Req 6's pass condition is a build step with an artifact (B5), not a review opinion. The floor is one value in one function, changeable by migration. |
| **R7** — The Python validator and this SQL function drift apart on boundary cases, so a place and an event at the same coordinate attribute to different Hoods | Two implementations is now the ratified design (F7, §4.1), so the risk is **divergence, not duplication**. Mitigated by the two binding shared artifacts: one algorithm spec with **on-boundary → no Hood** pinned as a value, and one checked-in fixture asserted against both. A case added to one side must be added to both — that rule is the actual control; the fixture is only its evidence. |
| **R8** — Source ToS or access turns out not to permit the use | The `enabled_requires_verified_terms` CHECK makes this fail closed rather than at launch. |

**Alternatives considered and rejected:** pure SQL + `pg_net` ingestion (§6 — no retry, no pagination, secrets in the DB); GitHub Actions or an external worker (§6 — no git remote exists, new account, new secret store); PostGIS for attribution (§4.1 — an Aviran-gated extension for a predicate that is 30 lines at this scale); `pg_trgm` fuzzy dedup in V1 (§4.5 — untunable before real data, and a bad merge is harder to undo than a missed one); a `duplicate_of` self-FK instead of a link table (§3.3 — leaves duplicate rows visible to any query that forgets the join); per-hour rank ordinals (§4.3 — a row per event-hour for no gain once time is a filter); RLS-policy-as-filter on `events` instead of a view (splits one contract across a policy and a column grant — harder for a reviewer to verify as a single rule); dropping unattributed events outright (§3.2 — makes req 3's own re-attribution bullet impossible).

---

## 9. Build breakdown

Ordered. **No `[iOS]` step exists in this TRD, and that was confirmed rather than assumed** — the PRD's Description fences the client surface out ("markers, detail sheet, and toggle"), `live-events-overlay` owns all of it as T-034, and the only client-side obligations this pipeline creates (§4.2's three items) are T-034's build steps against a contract that is now pinned. The work splits **[Backend]** (schema, RLS, view, scheduling — `developer`) and **[Algo/Data]** (adapters, normalization, dedup, ranking — `data-engineer`), which is the honest tagging; it is not backend-only.

**Track A — schema and access. Independent of Track B after A1.**

| # | Step | Tag |
|---|---|---|
| A1 | Migration: `event_sources`, `events`, `event_source_links`, `event_ingest_runs`, all CHECKs, FKs and indexes (§3). Take the next unclaimed number (F6); add a `functions/` row to `database/README.md`'s Layout (§2.3) | **[Backend]** |
| A2 | RLS enabled on all four (`events`, `event_sources`, `event_source_links`, `event_ingest_runs`) — **verify each individually via `pg_class.relrowsecurity`, not three-of-four**; **no policy on any**; `events_public` view; `revoke all` on base tables; `grant select` on the view (§4.2) | **[Backend]** |
| A3 | `hood_for_point()` + `reattribute_events()`, both with `revoke execute` (§4.1) — same non-optional treatment B4 gives the ranking functions — **This is a second, deliberate implementation of the containment predicate — build it (§4.1, F7); do not try to call T-042's offline Python validator, and do not treat it as a duplicate to be removed.** Assert it against the **shared** fixture `database/data/fixtures/hood-containment-cases.json` (`places-dataset/TRD.md` §9 B2a) rather than a private case list: strictly inside, outside, in-bbox-outside-ring, concave notch, **on-edge and on-vertex (expected `null` — no Hood)**, **a shared edge between two adjacent Hoods (expected `null`, not either Hood)**, swapped lat/lng. Whichever of the three tasks builds first writes the fixture; a case added here is added on the Python side too | **[Backend]** |
| A4 | `pg_cron` → `pg_net` → Edge Function, service key from Vault, `'20 * * * *'`; retention prune (§3.5). Hand-off names `pg_net` + Vault + per-source secret as Aviran-gated (§7). **Verify `anon`/`authenticated` hold no grant on the `net` schema's request/response log tables** (§4.4) — those tables carry the outbound Bearer token in stored request headers | **[Backend]** |

**Track B — the pipeline itself.**

| # | Step | Tag |
|---|---|---|
| B1 | `canonical.ts`: `CanonicalEvent`, required-field validation with counted drop reasons, `dedup_key` (§4.5). **Vendor-neutral — buildable and testable before a source is chosen**, against a fixture | **[Algo/Data]** |
| B2 | `index.ts` orchestrator: advisory lock, run row, upsert-on-`dedup_key` + link row, `hood_for_point` attribution, run close (§5.1) | **[Algo/Data]** |
| B3 | Withdrawal reconcile, gated on `outcome='success'` (§5.3). Test the outage case explicitly: a `failed` run must withdraw nothing | **[Algo/Data]** |
| B4 | `event_rank_score()` weights, `recompute_event_ranks()`, `event_rank_floor()`, all with `revoke execute` (§4.3). Weights and floor are `data-engineer`'s call, the way B1 band thresholds were in T-031 | **[Algo/Data]** |
| B5 | `database/scripts/rank_review.sql` — top-N for a given hour with score components, for the **human review pass req 6's pass condition requires**. Without an artifact that check is an opinion | **[Algo/Data]** |
| B6 | Health check: a source with `last_success_at` older than 24h, or zero rows written for a full day, surfaces to the team (req 8). P0, not P1 — it is what makes R4 survivable | **[Algo/Data]** |
| B7 | The first source adapter + its `event_sources` row with `coverage_note` and `terms_verified_at`. **Blocked on `PAS-6` item 10** — everything above ships and is testable without it | **[Algo/Data]** |

**`trd-review` sign-off needed from:** `developer` + `code-reviewer` (A1–A4) and `data-engineer` + `code-reviewer` (B1–B7). **`security-auditor` is worth adding** (`chief-of-staff`'s dispatch call, not mine): the `security definer` view, the base-table revokes, the function-grant surface `002` already failed once, and an outbound service key in cron all land in one change.
