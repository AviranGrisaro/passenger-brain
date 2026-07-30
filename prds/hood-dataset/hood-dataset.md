# Hood Dataset — Tel Aviv Geometry & Attributes — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Why this is a PRD and not a line item:** standing rule, founder-direct 2026-07-30 (`agent-os/PROGRESS.md`, FOUNDER-DIRECT STUB) — a data need substantial enough to be its own deliverable gets its own PRD. This one is the board's existing T-040 / Linear `PAS-17`, which had a row and no spec.

## Description

- The real Tel Aviv Hood dataset: polygons, names, hand-curated blurbs, and the three attribute fields other V1 features read off a Hood.
- Replaces the placeholder T-031 shipped — 4 hand-authored rectangles in `passenger-code/Passenger/Resources/hoods-tel-aviv.json`, 5 rough rows in migration `001`'s seed.
- One authored source produces both artifacts (DB seed + bundled iOS fixture) through the existing `export_hoods_geojson.py`, same `id` slugs, so the two can never disagree.
- Sourcing method is open (OSM / municipal open data / manual authoring) — this states what the output must satisfy, not how to get it.
- Ships attribute **values**; the pipelines that later *change* them are not this PRD's.
- **Not in scope:** `hood_density` and the synthetic generator (built, `map-hoods-heat` + migrations `001`/`002`); the tourist-trap algorithm that proposes a flag value (`data-eng/discovery-engine-spec.md`); the curated places that sit inside Hoods (`prds/places-dataset/`); any city other than Tel Aviv; map rendering of any kind.

## Motivation

- Strategy, verbatim: *"the map is organized into **Hoods** — this is now the standing product-facing term for what earlier docs called "zone"/"neighborhood"."*
- Strategy, verbatim: *"Tap a Hood → hand-curated blurb + tagged spots."*
- `map-hoods-heat` req 3 ("dozens of Hoods, not thousands") was recorded **unmet at acceptance** — the shipped data is placeholder. That bullet is satisfied here, not there.
- Four V1 PRDs read Hood fields that do not exist in migration `001`: blurb, tourist-trap flag, progression designation.

## Requirements

### Must-have (P0)

1. **Coverage and granularity.**
   - [ ] The dataset holds **dozens of Hoods, not thousands** (decision #12's bound; `map-hoods-heat` req 3).
   - [ ] Hoods cover the Tel Aviv-Yafo area a user opening the app city-wide sees, with no unnamed interior hole large enough to read as a rendering bug.
   - [ ] No Hood exists for any city other than Tel Aviv (`map-hoods-heat` req 2).

2. **Non-overlap is validated before the data ships, and a violation fails loudly.**
   - [ ] No coordinate in Tel Aviv falls inside two Hood polygons.
   - [ ] A validation step runs over the authored source **before** export and **fails the build** on any overlap — it never silently resolves to file order the way `HoodHitTester.swift` does today (`map-hoods-heat` req 3, pass condition added at acceptance).
   - [ ] Loading the shipped dataset, no coordinate opens two different Hood sheets on repeat taps, and no Hood's fill paints over a neighbour's.

3. **Every Hood carries a stable slug and a display name.**
   - [ ] `id` is a stable lowercase slug that survives a geometry revision — a Hood's boundary may be corrected without changing its id.
   - [ ] `name` is the name a Tel Aviv resident would use out loud, not a municipal statistical-area code.
   - [ ] Slugs already seeded (`florentin`, `neve-tzedek`, `lev-hair`, `old-north`, `jaffa`) are preserved where the same Hood survives, so the swap is additive rather than a rename sweep.

4. **Hand-curated blurb, authored per Hood.**
   - [ ] Each Hood carries a `blurb` text field — the "local read" decision #10 makes load-bearing.
   - [ ] A blurb is written by a person, not generated from place names or density.
   - [ ] Blurb may be `null`; `hood-place-detail` req 2 already renders that case with no placeholder copy. Shipping nulls is allowed, shipping a placeholder string is not.
   - [ ] **[ASSUMPTION]** No length bound is specified upstream; the sheet is a native detent, so a blurb must read fully within one `.medium` detent without scrolling. Designer's to confirm at `design-review`.

5. **The three attribute fields other PRDs depend on exist and ship populated.**
   - [ ] `is_tourist_trap` — **nullable** boolean. `null` = not yet rated, `false` = not flagged, `true` = flagged (`tourist-trap-flag` technical design; reqs 4 and 7 need all three states stored).
   - [ ] A Hood whose value is not yet known ships `null`, never `false` — the two render identically but VoiceOver announces them differently (`tourist-trap-flag` req 7).
   - [ ] `designated_for_progression` — boolean, marking the Hoods Passport counts toward Local status (`passport` req 4). Undesignated Hoods carry `false`.
   - [ ] `blurb` — nullable text (req 4).
   - [ ] Every field is public-read with no per-user rows, matching the existing `hoods` RLS.

6. **One authored source, two artifacts, verified identical.**
   - [ ] The DB seed and the bundled iOS fixture are generated from the same source file in one export run.
   - [ ] Every `id` present in one artifact is present in the other, with the same polygon.
   - [ ] The export is re-runnable: correcting geometry means editing the source and re-exporting, never hand-editing either artifact.

7. **Places resolve cleanly against it.**
   - [ ] Every place in `prds/places-dataset/` resolves to exactly one Hood by coordinate, and its stored `hood_id` matches that resolution.
   - [ ] A geometry revision that orphans a place fails validation rather than shipping a place with a dangling `hood_id`.

### Nice-to-have (P1)

- A precomputed centroid per Hood, so the label channel does not recompute one per frame.
- Provenance recorded per Hood (which source the boundary came from), for the next city.

## Technical design

- **Data model:** extends `public.hoods` (migration `001`) with `blurb text null`, `is_tourist_trap boolean null`, `designated_for_progression boolean not null default false`. New migration — `001` is reviewed and pending Aviran's apply.
- **Polygon format:** unchanged from `001` — single-ring WGS84 `[[lng,lat], …]` in `jsonb`. **Open:** a real municipal boundary may need multi-ring or a hole, which is a schema decision, not a data detail.
- **APIs / contract:** unchanged — static reference data, fetched once per session and cached. Three columns add no round trip.
- **Architecture notes:** `export_hoods_geojson.py` (T-031's B3) is the export path and has never run against a real dataset. Req 2's non-overlap validator does not exist and is new work.
- **Dependencies:** nothing upstream. **Blocks** `places-dataset` (`hood_id` resolution), `passport` (designation + attribution), `tourist-trap-flag` (the stroke's source value), `live-events-pipeline` (event→Hood mapping), and the real-geometry half of `map-hoods-heat` req 3.
- **Open technical questions:** whether the sourced geometry needs multi-ring/hole support; whether the non-overlap validator runs in the export script or as a separate CI step; how a Been place is re-attributed when a Hood boundary is corrected (`passport`'s own open question).

## Assumptions

- **[ASSUMPTION]** Hood boundaries change rarely once authored, which is what makes session-long client caching safe (`map-hoods-heat`'s own assumption, inherited here).
- **[ASSUMPTION]** Blurbs are authored by the founders, not contracted out — decision #22 exited the staffing model for localness, and nothing states blurbs followed it. Blurb authoring is V1's remaining editorial load.

## Open questions & risks

- **Two numbers Passport needs are not here and are not inventable:** the Local threshold, and which Hoods are designated. This PRD provides the *field*; the values are Aviran's or `data-engineer`'s.
- **Seeding `is_tourist_trap` needs a proposing algorithm that does not exist yet** (`data-eng/discovery-engine-spec.md`). If it never lands, every Hood ships `null` — renders correctly per `tourist-trap-flag` req 4, but the product's second signal is empty at launch. Escalation, not a build detail.
- **The sourcing options differ in licence, not just effort.** OSM carries ODbL attribution obligations; municipal open data carries its own terms. Check before deriving from either.
- Blurb authoring scales per city — Tel Aviv is tractable, the second city repeats it.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created for T-040 / `PAS-17`, which had a board row and no spec | Standing rule, founder-direct 2026-07-30: a substantial data need is its own deliverable with its own PRD |
| 2026-07-30 | Kept separate from `places-dataset` rather than merged into one "reference data" PRD | Different sourcing jobs, different tooling, different failure modes — a geospatial boundary extraction with an overlap invariant vs. per-place attribute authoring. They share one schema contract (`places.hood_id` → `hoods.id`), stated in both |
| 2026-07-30 | Three attribute columns spec'd here rather than inside each consuming PRD | Four PRDs read Hood fields migration `001` does not have; specifying them once stops three PRDs each inventing a column |
