# Places Dataset — Tel Aviv Curated Places — TRD

**Task:** T-042
**PRD:** [`places-dataset.md`](./places-dataset.md) (Draft v1)
**Design spec:** none — pure data/schema deliverable, no UX surface. Routed `spec → trd`, skipping `design`.
**Author:** `architect`, 2026-07-31
**Status:** ready for `trd-review`

---

## 1. Context

This is the schema spec for a table that six V1 PRDs already read and no migration has ever created. `database/migrations/` holds `001` (`hoods`, `hood_density`) and `002` (synthetic density generator). There is no `places` table.

Read alongside, not restated here:

- [`places-dataset.md`](./places-dataset.md) — the requirements this document builds against. Req numbers below refer to it.
- [`hood-dataset.md`](../hood-dataset/hood-dataset.md) — T-040, the Hood geometry this dataset is attributed against. The one shared contract is [§4.1](#41-c-hood-1--the-places--hoods-contract).
- [`map-hoods-heat/TRD.md`](../map-hoods-heat/TRD.md) — the established idioms this extends: migration shape, RLS shape, static-reference-data caching, `[ASSUMPTION]` labelling.
- [`hood-place-detail/TRD.md`](../hood-place-detail/TRD.md) §3.1 — **already specifies a `places` table**, in a migration `003` that does not exist as a file yet. Reconciled in [§2.1](#21-migration-ownership--the-t-033-collision). That reconciliation is the single most important thing for `trd-review` to ratify.

**One-line summary of the shape:** one public-read table plus one small lookup table, no write path, no user identity, populated by an offline authoring pipeline whose validator — not Postgres — enforces the geometric and editorial invariants Postgres cannot express.

---

## 2. Architecture

Nothing new is introduced on the client by this task. The whole deliverable is:

| Piece | Where | New? |
|---|---|---|
| `public.places` | `database/migrations/004_places.sql` | new |
| `public.place_types` | same migration | new |
| Dataset validator | `database/scripts/validate_dataset.py` | new, **shared with T-040** |
| Places export | `database/scripts/export_places.py` | new |
| Authored source | `database/data/places-tel-aviv.source.json` | new |

`database/README.md`'s `scripts/` convention (run by hand, connection string from the environment, never hardcoded) is followed unchanged. Migrations remain `developer`'s turf; `scripts/` and the authored source are `data-engineer`'s.

### 2.1 Migration ownership — the T-033 collision

Three unbuilt tasks each claim DDL that overlaps:

| Task | Claims | State |
|---|---|---|
| T-033 (`hood-place-detail`) | `003_places_and_hood_blurb.sql` — `hoods.blurb` **and a minimal `places` table** | TRD written, **held at `trd`**, not built, file does not exist |
| T-040 (`hood-dataset`) | `hoods.blurb`, `hoods.is_tourist_trap`, `hoods.designated_for_progression` | TRD in flight in parallel |
| T-042 (this) | `places`, `place_types` | this document |

**Decision D1 — `places` is defined once, here.** T-033's `places` block is deleted from its migration; its A1/A2 backend steps are struck and replaced by a dependency on this task's migration. T-033's `hoods.blurb` line moves to T-040, which already claims that column plus two more.

Why this way round rather than letting T-033 create a minimal table and this task alter it:

- T-033's own TRD deliberately excluded `permanently_closed` and a keyword column on the grounds that "adding them speculatively would put two unowned fields in a shipped schema." Both fields now have an owner — this PRD — so the reason for the split has expired.
- A minimal-then-alter split makes `place_type` and `keywords` (both `not null`, no sensible default) arrive *after* rows exist, which forces the nullable→backfill→`set not null` dance in [§7.2](#72-migration-safety) for no benefit.
- T-033's iOS track is **not** blocked by this. Its own §3.4 bundled seed floor means the client builds and demos with no backend at all; only its two backend steps move.

**Migration number: `004_places.sql`. Settled, not contingent.** Numbering across the four in-flight TRDs is resolved workspace-wide — `003` = `hood-dataset` (T-040), **`004` = this task**, `005` = `live-events-pipeline` (T-043); T-033's planned `003` has nothing left in it (its `places` block moves here, its `hoods.blurb` line to T-040) and is removed rather than renumbered. Ratified independently by `developer`, `code-reviewer`, and T-043's own numbering resolution. Write `004_places.sql`; do not take "the next free number."

Nothing in this migration's SQL references `003`'s contents — it needs only `public.hoods` from `001` — and the file stays written order-independently regardless ([§7.2](#72-migration-safety)), so a build-order accident cannot silently ship a half-defined table. That is belt-and-braces now, not the numbering policy.

### 2.2 Not built here

Named explicitly so they do not fall through the floor between tasks. Each is an amendment another task's build must absorb, flagged for that task's `trd-review`:

| Amendment | Owning task |
|---|---|
| `places-tel-aviv.json` bundled fixture gains `place_type`, `keywords`, `permanently_closed`, `is_tourist_trap` — **emitted by this task's `export_places.py` ([§9](#9-build-breakdown) B3)**, see D4 below | **T-042 (this task), B3** |
| Drift check only: assert T-033's bundled copy still matches what B3 last emitted | T-033 |
| `Place` Swift model gains **one field per reading task, not all four at once** — `is_tourist_trap`→T-035, `permanently_closed`→T-036, `place_type`→T-037, `keywords`→T-038. `PlaceCategory` unchanged | T-035 / T-036 / T-037 / T-038, see D5 below |
| Sticker-shape totality test — every `sticker_shape` in the shipped export resolves to a real asset | T-037 (Passport) |
| Client-side keyword matching per [§4.3](#43-keyword-matching-is-client-side) | T-038 (Search) |
| Closed-state **refresh** pipeline (cadence, owner, mechanism) | **nobody — escalated and unmet, see [§8](#8-risks--alternatives)** |

**Decision D4 — `export_places.py` ([§9](#9-build-breakdown) B3) is the sole emitter of `places-tel-aviv.json`. T-033 never produces it.** An earlier draft of this table left the export with T-033's step B2 while [§5](#5-flow) step 3 and [§9](#9-build-breakdown) B3 both had `export_places.py` writing the same file — two claimed emitters of one artifact inside one document, which is either a conflicting second exporter or, worse, each task assuming the other ships one and neither doing it. B3 owns it because B3 already holds the validated source, which is the entire reason it exists. T-033's step is reduced to a **drift check** — assert its bundled copy round-trips against B3's output — the same relationship `export_hoods_geojson.py` has to the Hood bundle it does not author (`hood-dataset/TRD.md` §2.1). A second emitter is a second chance to drift.

**Decision D5 — the fixture carries all four new fields; the Swift model gains them one task at a time.** These are separable and were previously bundled onto T-033 as one amendment. The **fixture** must carry all four regardless: `place_type` and `keywords` are `not null` at the source and B3 round-trips the validated row, so there is no version of the export that omits them. The **`Place` Swift model** is different — none of the four has a reader inside T-033's own scope, and building all four in now is exactly what T-033's own D2 rule ("don't build for a feature that isn't specced yet," the rule that keeps `created_at` out of its model) forbids. `Decodable` ignores unknown JSON keys, so a fixture wider than the model is an already-supported, costless state, and each field lands in the task that first reads it. Adopted from T-033's own recommendation, confirmed independently by `developer` and `code-reviewer` at `trd-review`.

---

## 3. Data model

### 3.1 `public.place_types` — the sticker-shape registry

```sql
create table if not exists public.place_types (
  id            text primary key,   -- stable slug: 'cafe', 'bar', 'restaurant', 'museum', 'park', ...
  sticker_shape text not null       -- stable key the client maps to an asset, e.g. 'coffee-cup'
);
```

**Decision D2 — a lookup table, not a Postgres `enum` and not a bare `CHECK`.** This is the PRD's own open technical question, resolved in favour of the option it flagged as making req 3 checkable in SQL:

- `places.place_type` is a FK into it, so a place cannot carry an unregistered type. Req 3's closed enumeration is structural.
- `sticker_shape not null` means a registered type without a shape **cannot exist as a row**. Req 3's "adding a `place_type` value without a sticker shape fails validation" stops being a script that someone has to remember to run.
- No `ALTER TYPE` to add a value — matching `001`'s preference for `CHECK`-over-native-enum on `category`, for the same reason (a native enum would need a migration per new place type).
- `place_types` is not user-facing (req 3: internal, never a third category, never a chip). It carries no display string on purpose — a display string is the thing that would tempt a surface into rendering it.

The DB cannot verify that a `sticker_shape` key corresponds to a real iOS asset. That half of the guarantee is the client-side totality test in [§4.2](#42-c-sticker-1--place_type--sticker-shape).

### 3.2 `public.places`

```sql
create table if not exists public.places (
  id                 text primary key
                     check (id ~ '^[a-z0-9]+(-[a-z0-9]+)*$'),      -- stable kebab slug, as hoods.id
  name               text not null check (length(btrim(name)) > 0),
  category           text not null
                     check (category in ('eat-drink', 'things-to-do')),
  place_type         text not null references public.place_types(id) on delete restrict,
  hood_id            text not null references public.hoods(id)      on delete restrict,
  latitude           double precision not null check (latitude  between -90  and 90),
  longitude          double precision not null check (longitude between -180 and 180),
  keywords           text[] not null check (cardinality(keywords) > 0),
  permanently_closed boolean not null default false,
  closed_checked_at  timestamptz,
  is_tourist_trap    boolean,                                       -- tri-state, NO default
  updated_at         timestamptz not null default now(),
  constraint places_closed_has_source
    check (not permanently_closed or closed_checked_at is not null)
);

create index if not exists places_hood_idx on public.places (hood_id);
```

Six decisions inside that schema:

- **`category` is inherited from T-033's TRD §3.1 verbatim, not re-derived** — a `CHECK` on `text` with stable keys `eat-drink` / `things-to-do`, display strings client-only in `PlaceCategory.displayName`. That resolution already satisfies req 2 (Postgres-enforced, exactly two values, no `null`, no third value) and PRD req 2's "no string reading 'Food & drinks' survives anywhere in the data." Decision #33 and #41 are not reopened. **No third category is introduced anywhere in this document** — `place_type` is a separate axis ([§4.4](#44-place_type-does-not-touch-the-two-category-split)).
- **`is_tourist_trap` has no default and is nullable.** Req 6 requires unknown to ship as `null`, never `false`. A `default false` would make "not yet rated" unrepresentable on insert, which is precisely the state `tourist-trap-flag` req 4/7 need stored and VoiceOver announces differently. This is the one column where the absence of a default is the requirement.
- **`permanently_closed` is `not null default false`, and `places_closed_has_source` makes a closed flag prove it was checked.** Req 5 asks that staleness be visible rather than assumed. `closed_checked_at` stays nullable for rows never checked (honest: unknown, not "checked and open").
- **`keywords` is `text[]` with `cardinality > 0`**, satisfying req 4's "every row carries at least one keyword" in Postgres. Shape rationale in [§4.3](#43-keyword-matching-is-client-side).
- **Both FKs are `on delete restrict`, not `cascade`.** This is a deliberate deviation from T-033's TRD §3.1, which wrote `hood_id ... on delete cascade`. Cascade means a Hood geometry revision that drops a Hood row silently deletes its curated places — the most expensive data in the project, gone without an error. `restrict` makes exactly that operation fail loudly, which is what `hood-dataset` req 7 asks for ("a geometry revision that orphans a place fails validation rather than shipping a place with a dangling `hood_id`"). Flagged for T-033's reviewers.
- **The `id` regex is cheap and worth it.** Slugs are the join key between the DB, the bundled fixture, and the device-local saved-places file. A slug with a space or capital in it is a bug that surfaces three layers away.

### 3.3 RLS — the established public-read shape, not a new one

```sql
alter table public.places      enable row level security;
alter table public.place_types enable row level security;

drop policy if exists places_public_read on public.places;
create policy places_public_read
  on public.places for select to anon, authenticated using (true);

drop policy if exists place_types_public_read on public.place_types;
create policy place_types_public_read
  on public.place_types for select to anon, authenticated using (true);
```

Identical in shape to `001`'s `hoods_public_read` / `hood_density_public_read`. **No insert/update/delete policy is written at all** — absence of a policy is the denial, and there is no client write path to authorize. Whoever authors or updates the dataset writes with the service role, out of band, which bypasses RLS by construction.

This satisfies req 8 and is not a new pattern: `002`'s generator writes the same way. Nothing here needs an identity, an auth surface, or a write rule to reason about.

### 3.4 Location & privacy

Places are **public reference data about businesses, not about people**. Nothing in this table is derived from, or identifies, any individual (req 8):

- The only coordinates stored are a curated place's own published location. No user coordinate, no visit, no dwell, no timestamp of anybody's presence, ever enters this table.
- `keywords` are hand-authored editorial (req 4, PRD Assumptions), not mined from user behaviour or third-party review text.
- The containment validator ([§4.1](#41-c-hood-1--the-places--hoods-contract)) runs **offline over authored files**. It never sees a user location.
- The fetch is byte-identical for every user — no query parameter carries anything user-specific, the property T-031 §3.3 establishes and for the same reason.

The one artifact in the wider feature set that could leak where somebody goes is the device-local saved-places file, and that is T-033/T-036's, deliberately holding slugs only. This task adds nothing to it.

---

## 4. Contracts

### 4.1 C-HOOD-1 — the `places` ↔ `hoods` contract

**This is the only contract this dataset and `hood-dataset` (T-040) share. Both TRDs must state it in these terms so they cannot drift.** Stated as four clauses, each independently falsifiable:

1. **Referential.** `places.hood_id` is a foreign key to `hoods.id`, `on delete restrict`. Free text is not acceptable (req 1). `restrict`, not `cascade` — see [§3.2](#32-publicplaces).
2. **Geometric.** For every place, ray-casting `(longitude, latitude)` against the single-ring WGS84 `[[lng,lat], …]` polygons (`001`'s committed format, ratified by `export_hoods_geojson.py`) yields **exactly one** containing Hood, and `places.hood_id` equals that Hood's `id`. Zero containing Hoods → **fail**, never ship unattributed (req 1). Two or more → **fail**, and the failure is also a live counter-example to `hood-dataset` req 2's non-overlap invariant, so it is reported against both datasets.
3. **Enforcement site.** The geometric clause is enforced by `validate_dataset.py`, **not by Postgres.** There is no PostGIS on this project and `hoods.polygon` is `jsonb`, not `geometry`; a DB-level containment constraint would mean adding a spatial extension for one authoring-time check. The FK gives referential integrity; the validator gives geometric correctness. A place is never written to the DB or the export without the validator passing.
4. **Single implementation, shared.** `database/scripts/validate_dataset.py` owns **both** invariants — T-040's non-overlap check and this task's containment check — because they are the same ray-cast over the same rings, and two implementations would disagree eventually. T-040's build calls it; T-042's build calls it. Whoever builds it first writes it; the second task consumes it.

**Ordering consequence:** the validator reads the **authored Hood source**, not the database, so this task's *schema* has no dependency on T-040. Only this task's *data* does — real places cannot be validated until real Hood geometry exists. Build sequencing in [§9](#9-build-breakdown) reflects that split.

**Boundary case, pinned to a value, not just to "deterministic":** `point_strictly_inside` returns **`false` for a point exactly on a ring edge or vertex** (`hood-dataset/TRD.md` §2.3 predicate 1). So a place sitting exactly on a shared Hood edge is contained by **neither** adjacent Hood, clause 2's "exactly one" fails, and the dataset is rejected until the author moves the coordinate or the boundary — never resolved by file order (the failure mode `HoodHitTester.swift` has today) and never silently assigned to whichever Hood was parsed first. Because clause 2 also fails on two containing Hoods and `hood-dataset` req 2 forbids overlap, no coordinate can ever be claimed twice either.

**Cross-language conformance — clause 4 covers the two Python consumers only, and a third implementation exists.** Clause 4's single shared file is correct for T-040's non-overlap check and this task's containment check: both are offline stdlib Python over authored files. `live-events-pipeline` (T-043) needs the *same predicate* at a different seam entirely — a `plpgsql` `hood_for_point()` running live inside Postgres against the `hoods` table, attributing externally-sourced events at ingest. **That is a second, genuinely necessary implementation and clause 4 does not absorb it** — see `live-events-pipeline/TRD.md` §4.1 for why no bridge exists in either direction. What the two share instead is stated in [§9](#9-build-breakdown) B2: an identical **algorithm spec** (closed single-ring WGS84 `[[lng,lat],…]`, even-odd ray cast, bbox prefilter, on-boundary → `false`) and **one checked-in fixture file** of point→expected-`hood_id` cases asserted against both. If the SQL function and this validator disagree on an edge case, a place and an event at the identical coordinate land in different Hoods — a bug nobody would find by inspection.

### 4.2 C-STICKER-1 — `place_type` → sticker shape

Two halves, one on each side of the wire, together satisfying req 3's "every place yields a sticker, no place earns a shapeless sticker":

- **Server half (built here):** `place_types.sticker_shape` is `not null`, and `places.place_type` FKs into it. A type without a shape cannot exist; a place with an unregistered type cannot exist.
- **Client half (built by T-037, named in [§2.2](#22-not-built-here)):** a `StickerShape` Swift enum over the known shape keys, plus a test asserting **every** `sticker_shape` present in the shipped `place-types.json` export resolves to a real asset. The test is the falsifiable pass condition; the enum alone is not, because the key arrives from the server as a `String`.
- **Runtime fallback, defence-in-depth not contract:** an unknown shape key renders a generic shape rather than nothing. This exists so a data/app version skew degrades instead of blanking a sticker; the export validator failing the build is what makes it unreachable in a shipped pair.

### 4.3 Keyword matching is client-side

**Decision D3 — `text[]` shipped in the payload and matched on device. No Postgres full-text, no `tsvector`, no GIN index.** This resolves the PRD's open technical question. It is forced, not preferred:

- `search-quick-filters` req 4: *"Search reads the same cached place and Hood data the map reads — no search-only dataset."* A server-side FTS query is a second dataset by definition.
- Same PRD req 6: *"Offline: matching runs on cached data only."* A server-side match cannot run offline.
- Same PRD req 2: *"Matches update as the user types, rendering under 400ms of a keystroke pause."* A per-keystroke round trip does not make that budget on cellular.

No index is added, because no server-side query filters on `keywords`. An index nothing queries is cost with no reader.

The matching rules the client must implement (T-038's build, contract stated here so it is not re-derived):

- Case- and diacritic-insensitive, via `String.folding(options: [.caseInsensitive, .diacriticInsensitive])`. Tel Aviv keywords may be Hebrew or English; both fold.
- Match is **substring-of-keyword**, not token equality, so `"roof"` hits `"rooftop bar"` mid-type. Req 4's probe list is written against this behaviour.
- Authoring rules the validator enforces, not the client: keywords are lowercased, trimmed, de-duplicated within a row, and **at least one keyword per row is not a substring of the place's own name** (req 4's "authored, not derived from the place name" — name matching is already covered separately by `search-quick-filters` req 2).

### 4.4 `place_type` does not touch the two-category split

Stated as a contract because three PRDs depend on it holding (req 3, `hood-place-detail` req 6, `search-quick-filters` req 3):

- `category` and `place_type` are independent columns. Neither derives from the other, and no code path infers one from the other.
- No user-facing surface renders `place_type` as a category, a chip, or a filter axis. `search-quick-filters` req 3 caps the sheet at exactly two chips; this task ships nothing that could become a third.
- The only user-visible consequence of `place_type` in V1 is a sticker's **shape** in Passport.
- **[ASSUMPTION]** carried unchanged from the PRD: that `place_type` is internal-only is `passport`'s proposed reading and Aviran has not confirmed it. If he wants it user-facing, this contract breaks and `hood-place-detail` req 6 + `search-quick-filters` req 3 both reopen. Nothing in this schema blocks that later — it would be a client change, not a migration.

### 4.5 Fetch contract

Unchanged from T-033's TRD §4 — this task adds columns to an existing embedded select, not a new endpoint:

```
GET /rest/v1/hoods?select=id,blurb,places(id,name,category,place_type,latitude,longitude,keywords,permanently_closed,is_tourist_trap)
GET /rest/v1/place_types?select=id,sticker_shape
```

One extra small GET for `place_types` (dozens of rows), fetched once per session alongside the places load. No pagination. No query parameter carries anything user-specific.

**Payload ceiling — answering the PRD's open "at what row count does the whole-payload cache stop fitting."** **[ASSUMPTION]** at ~400–450 bytes of uncompressed JSON per row (measured against the column set above with ~6 keywords), the design is comfortable to **~2,000 places** (≈850KB raw, ≈200KB gzipped) and should be re-examined past **~5,000** (≈2MB raw). V1 Tel Aviv curation is expected in the low hundreds, so this is headroom, not a live constraint. The number is falsifiable the moment a real row count exists — measure the export, do not re-estimate. Past the ceiling, the escape is Hood-scoped fetching, which changes `PlaceCatalog`'s loading strategy but no contract in this section.

---

## 5. Flow

**Authoring → ship (the only flow this task has):**

1. A person authors/edits `database/data/places-tel-aviv.source.json` — one object per place, all columns of [§3.2](#32-publicplaces) plus nothing else.
2. `validate_dataset.py` runs against that file **and** T-040's authored Hood source. It fails, loudly and per-row, on: a place in zero Hoods or two Hoods (C-HOOD-1 clause 2); a `hood_id` that disagrees with the ray-cast; a `place_type` not in `place_types`; a `place_type` whose `sticker_shape` is empty; zero keywords; a keyword set entirely derivable from the name; a `category` outside the two; `is_tourist_trap = false` where the author meant unknown (see [§9](#9-build-breakdown) B2's explicit-`null` rule); `permanently_closed = true` with no `closed_checked_at`; a slug failing the `id` regex; a Hood with zero places not on the accepted exception list (req 7); a `designated_for_progression` Hood below the Local threshold (req 7, **skips loudly** while the threshold is unknown — see [§8](#8-risks--alternatives)).
3. `export_places.py` writes two artifacts from the same validated source in one run: the DB seed statements and `passenger-code/Passenger/Resources/places-tel-aviv.json` (T-033's bundled seed floor, extended per [§2.2](#22-not-built-here)). Same one-source-two-artifacts rule `hood-dataset` req 6 sets for Hoods; the two can never disagree because neither is hand-edited.
4. The seed is applied by whoever holds credentials — **Aviran-gated**, like every migration in this repo.

**Runtime flow is entirely T-033's** and unchanged by this task: one session-scoped fetch → `PlaceCatalog` → `places(in:)` / `place(id:)` dictionary reads, live → cache → bundled seed → empty. This task adds fields to that payload and changes no step of it.

**Edge/error paths, all pre-existing and deliberately untouched:** a `hood_id` absent from the bundled Hood catalog keeps the place (T-033's §3.1 call — it renders as a pin and appears in no Hood sheet); a Hood with no places renders `hood-place-detail` req 2's specified empty state, which is a state, not a failure; `is_tourist_trap = null` renders exactly as `false` and announces differently in VoiceOver (`tourist-trap-flag` req 4/7).

---

## 6. Third-party / dependencies

**None added.** No new SDK, no new service, no account, nothing that costs money.

The validator's point-in-polygon is ~30 lines of ray-casting over a list of `[lng, lat]` pairs. Alternatives rejected: **Shapely/GEOS** (a C dependency and a build story for one function, on a project whose only existing script is stdlib Python); **PostGIS** (a database extension, an Aviran-gated project change, and a per-tap round trip if it ever leaked into runtime — T-031 §10 rejected server-side point-in-polygon for exactly that reason); **Apple Maps / Google Places as a live source** (this PRD ships authored values, not an ingestion pipeline, and a live source is a licence and cost decision that is Aviran's, not an implementation detail).

---

## 7. Rollout & migration

### 7.1 No feature flag

This is reference data behind features that are themselves unshipped. There is no prior version to gate against and no A/B surface. Backward compatibility required: none — the schema is empty, `001` is not applied, and no client has ever read this table.

### 7.2 Migration safety

The migration is written to be **correct under either build order**, because [§2.1](#21-migration-ownership--the-t-033-collision)'s reallocation may or may not have landed in T-033 by the time someone writes SQL:

- `create table if not exists public.places (…)` with the **full** column set from [§3.2](#32-publicplaces), **followed by explicit `alter table ... add column if not exists` for every column beyond the minimal set T-033 specified** (`place_type`, `keywords`, `permanently_closed`, `closed_checked_at`, `is_tourist_trap`). This matters: `create table if not exists` against an already-existing minimal table is a silent no-op that would ship a `places` table with no `place_type` and no `keywords` — exactly the drift this whole task exists to end. The `alter` block is the belt to the `create`'s braces.
- Adding `place_type` / `keywords` as `not null` fails if placeholder rows already exist, so both are added **nullable, backfilled, then `set not null`** in the same migration. The backfill uses the placeholder values in step A4 below.
- `CHECK` constraints have no `if not exists` in Postgres; each is added inside a `do $$ … $$` guard testing `pg_constraint`, so re-running is safe.
- Idempotent overall, per `database/README.md`'s convention and `001`'s precedent. Never edited once applied.

### 7.3 Apply gate

Applying is **Aviran-gated** — he holds the credentials, and `001` and `002` are both still unapplied. This migration joins that queue; write it and hand it off, do not apply it. The real curated seed is separately gated on Aviran deciding who authors it and how many rows (Linear `PAS-6` item 11) — see [§8](#8-risks--alternatives).

---

## 8. Risks & alternatives

| Risk | Mitigation / decision |
|---|---|
| **Nobody has decided who authors the dataset or how many rows.** Linear `PAS-6` item 11. Every requirement in the PRD is about shape and validity; none produces a row. | Not solvable here — Aviran's. The schema, validator, and export are all buildable and testable now against a placeholder seed ([§9](#9-build-breakdown) A4), exactly as `001` did for Hoods. **This is the largest unspecified input in V1 and this TRD does not close it.** |
| **The Local threshold is unknown, so req 7's designated-Hood check cannot run.** | The validator implements the check and **reports `SKIPPED — threshold unset` loudly**, never a silent pass. Threshold is read from a config file; the check becomes live the day the number lands. A silent pass here would let a Hood ship where `passport` req 4 is unreachable by construction. |
| **`place_type` and `keywords` value sets have no decision record.** Both trace to verbatim strategy lines, so the scope gate clears, but neither enumeration is fixed. | `place_types` being a table rather than an enum means adding a value is an insert, not a migration. The initial set is `data-engineer`'s proposal at B1, ratified by Aviran, not invented by whoever writes the SQL. |
| **Closed-state refresh has no owner and no cadence.** `places-been-saved` req 4 needs a place that closes *after* being saved to show the badge next render; a one-time author-time read cannot deliver that. | **Escalated, unowned, and unmet — not fenced out.** Stated precisely because an earlier draft of this row got it wrong: `places-dataset.md` req 5's third bullet ("a refresh path exists and runs on a stated cadence") is a **live P0 acceptance criterion**, sitting in the PRD's Open questions & risks, *not* in its `Not in scope` list. This TRD does not build the pipeline — nothing in V1 specs one and no task owns one — but that is an unmet requirement with an escalation attached, not a requirement the PRD released us from. `closed_checked_at` is the mitigation that ships: staleness becomes **visible** instead of assumed, which is not the same as refreshed. Ownership gap tracked as **T-044 / Linear `PAS-22`**; `product` still needs to either move req 5's bullet to Not-in-scope or land a follow-on PRD, or req 5 sits permanently unmet against its own document. Flagged for `chief-of-staff` in [§10](#10-left-for-the-board). |
| Payload outgrows the whole-dataset client cache | Ceiling estimated in [§4.5](#45-fetch-contract) with the escape named (Hood-scoped fetch). Measure the real export rather than re-estimating. |
| T-033 ships its own `places` table before D1 is ratified, and the two diverge | [§7.2](#72-migration-safety)'s `create`-then-`alter` makes the divergence self-healing rather than silent. Ratifying D1 at `trd-review` is the actual fix. |
| A Hood boundary correction orphans curated places | `on delete restrict` makes it fail loudly; `validate_dataset.py` catches it before anything reaches the DB. `hood-dataset` req 7's own requirement, enforced here. |
| Keyword authoring is per-place editorial load on top of per-Hood blurbs | Named in the PRD as Aviran's read before sizing. Not an architecture problem — flagging it as one would be pretending it is solvable here. |

**Alternatives considered and rejected:** Postgres `enum` for `place_type` (needs `ALTER TYPE` per value, and cannot express "every value has a shape" — [§3.1](#31-publicplace_types)); a bare `CHECK` list for `place_type` (same, minus the FK guarantee); Postgres full-text / `tsvector` for keywords ([§4.3](#43-keyword-matching-is-client-side) — breaks offline and the no-second-dataset rule); PostGIS containment constraint ([§4.1](#41-c-hood-1--the-places--hoods-contract) clause 3); `on delete cascade` on `hood_id` ([§3.2](#32-publicplaces)); merging this into `hood-dataset` as one "reference data" migration (the PRD's own decisions log rejects it — different sourcing jobs, different failure modes, one shared contract); a `place_type` display-name column ([§3.1](#31-publicplace_types) — a display string invites a surface to render it, reopening decision #33).

---

## 9. Build breakdown

Ordered. Tags name the agent(s) each step dispatches to. **No `[iOS]` step exists in this task** — every client-side consequence is another task's amendment, listed in [§2.2](#22-not-built-here).

**Schema track — buildable now, no dependency on T-040 or on the data existing.**

| # | Step | Tag |
|---|---|---|
| A1 | Migration: `place_types` per [§3.1](#31-publicplace_types), with `sticker_shape not null` | **[Backend]** |
| A2 | Same migration: `places` per [§3.2](#32-publicplaces) — all constraints, both FKs `on delete restrict`, the `places_closed_has_source` check, the `places_hood_idx` index. Written per [§7.2](#72-migration-safety)'s `create`-then-`alter`-then-`set not null` shape | **[Backend]** |
| A3 | Same migration: RLS per [§3.3](#33-rls--the-established-public-read-shape-not-a-new-one) — enable on both, one public `select` each, **no write policy** | **[Backend]** |
| A4 | Same migration: an **explicitly-labelled placeholder** seed — the initial `place_types` rows plus a handful of real Tel Aviv places inside `001`'s five placeholder Hoods, so RLS and the client contract are verifiable before real curation exists. `on conflict do nothing`, so the real seed supersedes it by id without reissuing the migration. Follows `001`'s A3 precedent exactly, including saying so in the file header | **[Backend]** + **[Algo/Data]** |
| A5 | Delete the `places` block from T-033's planned migration `003`; move its `hoods.blurb` line to T-040's. **Blocked on D1's ratification at `trd-review`** | **[Backend]** |

**Data track — A4 unblocks everything below it that does not need real geometry.**

| # | Step | Tag |
|---|---|---|
| B1 | Propose the initial `place_type` enumeration and its `sticker_shape` mapping, for Aviran's ratification. Not invented by whoever writes A1 | **[Algo/Data]** |
| B2 | `validate_dataset.py` — ray-cast point-in-polygon, plus every rule in [§5](#5-flow) step 2. Owns **both** C-HOOD-1 invariants, shared with T-040 (clause 4). Includes the req-7 threshold check that reports `SKIPPED` loudly. **Authoring rule this step encodes: unknown tourist-trap ships explicit `null`, never `false`** (req 6) | **[Algo/Data]** |
| B2a | **`database/data/fixtures/hood-containment-cases.json`** — the shared cross-language conformance fixture ([§4.1](#41-c-hood-1--the-places--hoods-contract)). Point→expected-`hood_id` cases covering: strictly inside; outside; **on a ring edge and on a vertex (expected: no Hood — `false`/`null`, matching `hood-dataset` §2.3 predicate 1)**; inside the bbox but outside the ring; inside a concave notch; on an edge shared by two adjacent Hoods (expected: **neither**); a swapped lat/lng pair. **Asserted against both implementations** — this validator, and T-043's SQL `hood_for_point()` (`live-events-pipeline/TRD.md` §9 A3). Whichever task builds first writes the file; the other adds its assertion against the same cases and adds none of its own without adding them for both | **[Algo/Data]** |
| B3 | `export_places.py` — one validated source → DB seed + `places-tel-aviv.json`, in one run. Fails the export on any validator failure | **[Algo/Data]** |
| B4 | The keyword probe list (req 4's pass condition), including strategy's own `"hummus"` and `"rooftop bar"`, committed alongside the source. A probe returning zero is a **dataset** defect, not a search defect | **[Algo/Data]** |
| B5 | **The real curated Tel Aviv dataset.** **Blocked on T-040's real Hood geometry** (C-HOOD-1 clause 2 cannot run without it) **and on Aviran** (who authors, how many rows — `PAS-6` item 11) | **[Algo/Data]** |

**`trd-review` sign-off needed from:** `developer` + `code-reviewer` (A1–A5), `data-engineer` + `code-reviewer` (B1–B5). **No iOS pair** — this task builds no client code.

**Cross-task review, needed before A5 is actionable:** T-033's reviewers must ratify D1 ([§2.1](#21-migration-ownership--the-t-033-collision)) and the `cascade`→`restrict` change; T-040's TRD must state C-HOOD-1 ([§4.1](#41-c-hood-1--the-places--hoods-contract)) in these terms and claim B2's validator on the same side of the seam.

---

## 10. Left for the board

Not mine to write to `BOARD.md` or Linear; surfaced for `chief-of-staff`:

1. **D1 is a change to an already-written TRD** (T-033's migration `003`) and to T-040's TRD, which is being written in parallel right now. Both need to see it before either builds SQL.
2. **Closed-state refresh remains unowned, and it is an unmet P0 — not out of scope.** `places-dataset` req 5's refresh-path bullet lives in the PRD's Open questions & risks, not its `Not in scope` list, so nothing has released this requirement; this TRD simply does not build it, and `places-been-saved` req 4 depends on it. Flagged by `product`, by T-036's PRD, and by this TRD before it acquired an owner — now tracked as **T-044 / Linear `PAS-22`**. `product` still owes the disposition: move the bullet to Not-in-scope, or open the follow-on PRD.
3. **B5 is blocked on Aviran** (`PAS-6` item 11), and it is the step that produces the actual dataset. Everything above it is scaffolding for rows nobody has been asked to write.
4. **The Local threshold** gates req 7's validation, not just Passport's UI. B2 ships the check disabled-and-loud until the number exists.
