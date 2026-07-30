# Places Dataset — Tel Aviv Curated Places — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Why this is a PRD and not a line item:** standing rule, founder-direct 2026-07-30 (`agent-os/PROGRESS.md`, FOUNDER-DIRECT STUB). Six V1 PRDs read the `places` table; three of them name a field on it that does not exist. Nobody owns authoring it.

## Description

- The curated Tel Aviv places dataset — the rows every other V1 feature reads, plus the fields three of them need and `places` does not have.
- One authored dataset, one schema, public-read. Not a user-generated surface.
- Adds the two fields currently specified as gaps in the PRDs that need them: `place_type` (Passport's sticker shapes) and a searchable keyword field (search's "hummus" / "rooftop bar").
- Ships attribute **values**; the pipelines that later change them are not this PRD's.
- **Not in scope:** the Hood polygons places are attributed to (`prds/hood-dataset/`); the device-local Saved/Been/Visited store (`places-been-saved` — that is per-install state, not dataset); the tourist-trap proposing algorithm (`data-eng/discovery-engine-spec.md`); TikTok-extracted places (held, `PAS-6` item 9); any place outside Tel Aviv; any UI.

## Motivation

- Strategy, verbatim: *"Tap a place → detail modal (name, category, save, routing)."*
- Strategy, verbatim: *"each gets a sticker in your **Passport** shaped to match the place type (coffee cup for a café, etc.)"* — the field this requires does not exist.
- Strategy, verbatim: *"Covers place names, keywords ("hummus", "rooftop bar"), and Hoods"* — the field this requires does not exist.
- The schema is empty. `database/migrations/` holds `001` (hoods, density) and `002` (synthetic generator). There is no `places` table at all yet.

## Requirements

### Must-have (P0)

1. **Every place resolves to exactly one Hood, and the stored value matches.**
   - [ ] `hood_id` is a foreign key to `hoods.id` (`prds/hood-dataset/`), not free text.
   - [ ] The stored `hood_id` equals the Hood whose polygon contains the place's coordinates — verified at authoring time, not assumed.
   - [ ] A place whose coordinates fall in no Hood fails validation rather than shipping unattributed.

2. **Exactly two user-facing categories, with the locked names.**
   - [ ] `category` is constrained to exactly **"Things to do"** and **"Eat & Drink"** (decision #33).
   - [ ] Every row carries one — **no third value, no null, no "other"** (`hood-place-detail` req 6).
   - [ ] The constraint is enforced in Postgres, not only client-side, so the dataset cannot drift.
   - [ ] No string reading "Food & drinks" survives anywhere in the data (`hood-place-detail` req 6).

3. **`place_type` is a separate, finer, internal field — it does not touch the two-category split.**
   - [ ] `place_type` is a closed enumerated value (café, bar, restaurant, museum, park, …), stored per place, distinct from `category`.
   - [ ] It is **internal**: no user-facing surface renders it as a third category, and it never appears in the search chips or any filter (`search-quick-filters` req 3 caps the sheet at two chips).
   - [ ] Every enumerated value maps to exactly one sticker shape, and every place therefore yields a sticker (`passport` req 3; decision #29).
   - [ ] Adding a `place_type` value without a sticker shape fails validation — a place must never earn a shapeless sticker.
   - [ ] Every row carries a non-null `place_type`. Without this field V1 ships two sticker shapes and decision #29 is not met (`passport` Open questions).

4. **Keyword search has a field behind it.**
   - [ ] Each place carries a searchable keyword/tag set beyond its name — the field `search-quick-filters` req 2 matches against ("hummus", "rooftop bar").
   - [ ] Every row carries at least one keyword; a place with none fails validation.
   - [ ] Pass condition: a documented probe list, including strategy's own two examples, each returns at least one correct Tel Aviv place. A probe returning zero is a dataset defect, not a search defect.
   - [ ] Keywords are authored, not derived from the place name — matching the name is already covered by name matching.

5. **Permanently-closed state lives on the place and has a stated source.**
   - [ ] `permanently_closed` is a boolean on the place, not on any saved entry (`places-been-saved` technical design, decision #38).
   - [ ] The value's source is Apple Maps, and the dataset records **when** it was last checked, so staleness is visible rather than assumed.
   - [ ] A refresh path exists and runs on a stated cadence — `places-been-saved` req 4 requires a place that closes *after* being saved to show the badge next render, which a one-time author-time read cannot deliver.
   - [ ] **[ASSUMPTION]** Cadence is unspecified upstream. Until stated, a place may show the badge late; `places-been-saved` already carries this as an assumption.

6. **Tourist-trap flag ships as a nullable boolean, seeded per place.**
   - [ ] `is_tourist_trap` — `null` not yet rated, `false` not flagged, `true` flagged (`tourist-trap-flag` technical design).
   - [ ] A place whose value is unknown ships `null`, never `false`.
   - [ ] It is independent of `permanently_closed`: a place may carry both, either, or neither (`tourist-trap-flag` req 6).

7. **Volume is sufficient for the surfaces that consume it.**
   - [ ] No Hood ships with zero curated places unless it appears on a written, accepted exception list — an empty Hood sheet is a specified state (`hood-place-detail` req 2), not a default.
   - [ ] Every Hood marked `designated_for_progression` contains **at least the Local threshold count** of places. Below that, Local status is mathematically unreachable in that Hood and `passport` req 4 can never pass. Blocked on the threshold number (`passport` Open questions).

8. **The dataset is public reference data with no identity surface.**
   - [ ] Public-read RLS, no per-user rows, no writes from the client — matching `hoods` (migration `001`).
   - [ ] No field on a place identifies, or is derived from, any individual user.

### Nice-to-have (P1)

- Opening hours, where the source carries them (`hood-place-detail` P1, `places-been-saved` P1).
- One photo per place (`hood-place-detail` P1).
- Provenance per row — which source each place came from — for the second city.

## Technical design

- **Data model:** new `public.places` — `id` (stable slug), `name`, `category` (enum/CHECK, exactly two values), `place_type` (enum), `keywords` (text[] or tsvector), `lat`, `lng`, `hood_id` (FK → `hoods.id`), `permanently_closed` (boolean, default false), `closed_checked_at` (timestamptz), `is_tourist_trap` (boolean null). New migration; does not edit `001`/`002`.
- **APIs / contract:** one static payload fetched with the map's initial load and cached, same pattern as `hoods`. `search-quick-filters` matches client-side against that cache — which is what makes its 400ms and offline requirements achievable, and only holds while the whole payload fits. **Open:** at what row count it stops fitting.
- **Architecture notes:** `SALVAGE.md` marks `Models/Place.swift` REUSE — check it against `place_type` and `keywords`, neither of which Locali had.
- **Dependencies:** `hood-dataset` first (req 1's FK and containment check). **Blocks** `hood-place-detail`, `places-been-saved`, `passport`, `search-quick-filters`, and `tourist-trap-flag`'s place-level half.
- **Open technical questions:** whether keyword matching is `text[]` + client filter or Postgres full-text; whether `place_type` is a Postgres enum or a lookup table (a lookup table makes req 3's "every value has a shape" checkable in SQL); where the closed-state refresh runs (client `MKMapItem` lookup vs. a scheduled server job — `places-been-saved`'s own open question).

## Assumptions

- **[ASSUMPTION]** `place_type` is internal-only and does not reopen decision #33's two-category lock. This is the reading `passport` proposed; it has not been confirmed by Aviran. If he wants place type user-facing, `hood-place-detail` req 6 and `search-quick-filters` req 3 both change.
- **[ASSUMPTION]** Keywords are hand-authored. No source states who writes them, and nothing upstream authorizes deriving them from third-party review text.

## Open questions & risks

- **Nobody has said how many places V1 ships with, or who authors them.** Every requirement here is about shape and validity. This is the largest unspecified input in V1 — six PRDs read this table and none creates a row in it. Aviran's.
- **`place_type` and `keywords` each trace to a verbatim strategy line, so the scope gate clears — but neither has a decision record fixing its enumerated values.** Both value sets are open.
- **Keyword authoring is per-place editorial load on top of per-Hood blurbs** — the staffing shape decision #22 exited for localness. Worth Aviran's read before the dataset is sized.
- **Closed-state refresh has no owner.** `places-been-saved` req 4 requires it; nothing schedules it.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | Standing rule, founder-direct 2026-07-30. Six PRDs read `places`; three name a missing field; no PRD authored the dataset |
| 2026-07-30 | `place_type` spec'd here rather than inside `passport` | It is a dataset field with its own enumeration and validation, not a Passport rendering detail — `passport`'s own Open questions call it "a dependency on the dataset, not a rendering detail" |
| 2026-07-30 | Kept separate from `hood-dataset` | Different sourcing job and different failure modes; they share one FK contract, stated in both |
| 2026-07-30 | Req 7's designated-Hood/threshold cross-check written even though the threshold number is unknown | The check is falsifiable the moment the number lands, and without it a Hood can ship where `passport` req 4 is unreachable by construction |
