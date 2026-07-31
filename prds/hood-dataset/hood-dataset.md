# Hood Dataset — Tel Aviv Geometry & Attributes — PRD

**Status:** **Accepted 2026-08-01** (`acceptance`, second attempt — awaiting `aviran-review`). **Req 4 carried unmet, not waived:** 23 of 24 Hoods ship `blurb: null` and `florentin` ships a `[PROVISIONAL]`-marked placeholder. Reqs 1, 2, 3, 5, 6, 7 pass.
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-08-01
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
   - [ ] **Recorded unmet at acceptance 2026-08-01, carried not waived.** 23 of the 24 shipped Hoods carry `blurb: null`. `florentin` carries one `[PROVISIONAL]`-marked string so req 2's blurb branch has something to render — a Phase-1 demo device, tolerated only while the marker stays visible in the rendered text. **Fixed 2026-08-01 (`data-engineer` fix pass, closing req 6's attribute-parity finding):** the string now lives in the authored source (`hoods-tel-aviv.source.json`) and reaches the DB seed and the iOS bundle identically via `build_hoods.py` — it no longer exists only in a hand-edited generated artifact. No build seen outside the team may ship a `[PROVISIONAL]` blurb; this bullet is met when a person has authored real copy for `florentin` and the marker is gone.
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
   - [ ] **Added at acceptance 2026-08-01.** "Identical" covers **attribute values, not only polygons**: for every `id`, `blurb`, `is_tourist_trap` and `designated_for_progression` match across the authored source, the DB seed and the iOS bundle. A value present in one artifact and absent from another fails — including a value added by hand for a demo. Re-running the generator must not change any shipped artifact. **Clarified at acceptance 2026-08-01** (the bullet as first written was not mechanically checkable): "must not change" means byte-identical output, with the iOS bundle's `generatedAt` run-stamp the sole permitted diff — the migration SQL carries a source digest rather than a timestamp and must come back byte-identical with no exception. Pass condition: regenerate both artifacts to a scratch path and `diff` them against the shipped ones.

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
| 2026-08-01 | `acceptance` **REJECT**. Req 6 given an attribute-parity bullet; req 4 recorded unmet and carried | The `florentin` demo blurb exists **only** in the iOS bundle — `database/data/hoods-tel-aviv.source.json` and `migrations/006_hoods_tel_aviv_data.sql` both still carry `null`. Req 6's "never hand-editing either artifact" was already written, but "verified identical" was only ever checked on ids and polygons, so nothing caught a hand-edited attribute. The next `build_hoods.py` run silently deletes the only blurb in the app |
| 2026-07-31 | **Real geometry built** (`data-engineer`, founder-direct in chat: "based on the actual Tel Aviv hoods maps"), advancing B1/B2/B3/B4/B6 and A1 ahead of `BOARD.md`'s stated Build Phase 2 gate for this task, per Aviran's explicit instruction to proceed now rather than wait. **Source: OpenStreetMap, via the Nominatim API** (`nominatim.openstreetmap.org/search?...&polygon_geojson=1`), one request per named neighbourhood, 1.1s between requests per Nominatim's usage policy. Overpass API (the TRD's other suggested route) was tried first and timed out repeatedly across three mirrors; Nominatim's per-place lookup was the practical substitute and is the same underlying OSM data. **24 Hoods shipped** (up from 001/A3's 5-Hood, 4-bundle-Hood placeholder): `florentin`, `neve-tzedek`, `lev-hair`, `jaffa`, `old-north` (all five previously-seeded slugs preserved, req 3) plus `kerem-hateimanim` (preserved from the bundle), `montefiore`, `shapira`, `hatikva`, `ramat-aviv`, `bavli`, `yad-eliyahu`, `neve-shaanan`, `ramat-hachayal`, `afeka`, `tzahala`, `ramat-aviv-gimel`, `neve-ofer`, `tzahalon`, `hadar-yosef`, `nachalat-yitzhak`, `neve-avivim`, `ajami`, `neve-eliezer`. **`jaffa` is hand-authored, not OSM-verbatim**: OSM's administrative "Yafo" relation is the entire historic Jaffa municipal district and overlaps six already-distinct modern neighbourhoods in this same dataset (florentin, neve-tzedek, neve-shaanan, neve-ofer, tzahalon, ajami) that sit inside it — V6 correctly rejected it. Replaced with a smaller hand-drawn polygon over the real Old Jaffa hill / port / clock-tower core, `provenance.source: "manual"`, disclosed in-file rather than presented as an authoritative boundary, per the PRD's own permission for this case. **OSM's two "Old North" sub-boundaries (north/south parts) genuinely overlapped** (not a sliver — 21 of the southern polygon's 206 vertices fell inside the northern one); rather than invent a merge, the larger northern polygon was kept as the sole `old-north` Hood and the southern sub-boundary was dropped, since PRD req 3 only ever asked for one `old-north` slug and the north/south split isn't a genuine distinct-identity split the way Ajami vs. Jaffa is. **One real source-imprecision sliver was found and snapped**, per the TRD's own predicted first failure mode (§9): a Florentin/Neve Sha'anan shared-edge vertex overlapped by ~18m; fixed by moving the Neve Sha'anan vertex onto the matching Florentin vertex, which is now asserted as an on-boundary/no-Hood case in the shared fixture. **Licence: ODbL.** OpenStreetMap data requires attribution and share-alike-on-derived-databases; the notice is in `database/data/hoods-tel-aviv.source.json`'s `_attribution` field, in `006_hoods_tel_aviv_data.sql`'s header, and in the generated iOS bundle's `_attribution` field. **Whether attribution must be displayed in-app is not decided here** — flagged again for Aviran, `PAS-6` item 15. **Non-overlap validation: built and passing.** `database/scripts/validate_dataset.py` (V1-V9 per TRD §5.2) plus `database/scripts/build_hoods.py` (the generator, TRD §4.5) — both new, stdlib-only, no network/DB access. Clean run: 0 errors, 0 warnings, 24 hoods. A V7 coverage-gap warning (~7,515 m², below the 40,000 m² error threshold) surfaced mid-build and cleared on its own once the `jaffa` fix landed; not chased further since it was never above the warn line at any committed state. Also built: `database/data/fixtures/hood-containment-cases.json` (the shared T-040/T-042/T-043 containment fixture, TRD §4.4/§11 B1) and `database/scripts/test_hood_containment_fixture.py` (9/9 passing, including the on-boundary snap case). `database/scripts/export_hoods_geojson.py` repurposed into the post-apply drift check per TRD §5.3 (not run against a live table — no DB credentials reachable). **Not done, per this PRD's own scope note:** `blurb`, `is_tourist_trap`, `designated_for_progression` all ship `null`/`false` for every row — not sourced or invented here. **Scope note:** `003_hood_attributes.sql` and `006_hoods_tel_aviv_data.sql`, and the `database/README.md` status-table update, are normally `developer`'s turf (this agent's own role file: "does not own migration mechanics"); written here because Aviran's direct instruction named this exact deliverable. Flagged for `developer`/`code-reviewer` review before `trd-review`'s existing sign-off requirement (TRD §11: "`developer` + `code-reviewer` — A1, B6's SQL") is treated as satisfied. Neither migration has been applied (Aviran-gated, unchanged). Nothing pushed to either remote — commits only, per standing rule. |
| 2026-08-01 | T-040 fix pass closing acceptance's Finding 2 (req 6 attribute-parity bullet). `florentin`'s `[PROVISIONAL]` blurb moved from a hand-edit on the generated iOS bundle into the authored source (`hoods-tel-aviv.source.json`), then `build_hoods.py` re-run to regenerate `006_hoods_tel_aviv_data.sql` and the iOS bundle from that one source | The generated artifact was the only place carrying the blurb, which violated req 6's "never hand-editing either artifact" and meant the next generator run would silently delete it. Round-trip verified: `florentin`'s blurb string is byte-identical before/after: all 24 ids, all 24 polygons, and all 23 other Hoods' `null` blurbs are unchanged; `schemaVersion` stays 2; the only other diffs are the source-digest comment and `generatedAt` timestamp, both expected. Req 4 stays recorded unmet/carried — this relocates the existing provisional string, it does not author real copy |
| 2026-08-01 | `acceptance` **ACCEPT** (second attempt), with req 4 carried unmet. Status flipped to Accepted; req 6 bullet 4 clarified to a byte-diff pass condition; routing to `aviran-review` | Finding 2 closed and verified by re-running the generator rather than by reading the fix report: `build_hoods.py` regenerated to a scratch path reproduces `006_hoods_tel_aviv_data.sql` **byte-identically** (`diff` exit 0) and the iOS bundle byte-identically apart from the `generatedAt` run-stamp — which is the actual proof req 6 bullet 3 wanted, since a surviving hand-edit anywhere would have shown up as a diff. Independent 3-way parity check across the authored source, the migration SQL and the iOS bundle: 24/24 ids, all polygons, and `blurb`/`isTouristTrap`/`designatedForProgression` all match; the stale `_note` hand-edit disclosure is gone from the bundle. Req 4 stays unmet-and-carried — one `[PROVISIONAL]` string is still a placeholder wherever it lives; relocating it fixed the pipeline violation, not the sourcing gap |
