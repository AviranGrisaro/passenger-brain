# Live Events Overlay — PRD

**Status:** Accepted (Build Phase 1) 2026-08-03 — reqs 1–5 only. **Req 6 (layer toggle) is unbuilt and explicitly not accepted**, deferred to T-050; see the Decisions log.
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Build phase:** 1 — client ships with fake/empty data, no backend (`agent-os/BOARD.md` § V1 Build Phases)
**Owner:** Aviran Grisaro
**Last updated:** 2026-08-07
**Launch-blocking — what it attaches to.** Strategy, unchanged: "V1 does not ship until data-engineer has a working live-events ingestion pipeline." That gate is real, and it attaches to **the pipeline** — `T-043` / [`live-events-pipeline`](../live-events-pipeline/live-events-pipeline.md), Build Phase 3. **It does not block the work this PRD specs.** The client layer here is Build Phase 1: it renders whatever set it is handed, including none (req 5), so it can be built, demoed, and QA'd against a bundled fake event set while the pipeline is still Phase-3 work. Only *real* event data waits on the pipeline. Phase 1 therefore needs that fixture, not merely an empty feed — reqs 1–4 and 6 have nothing to exercise otherwise.

## Description

- A third map layer alongside heat and tag: events happening in Tel Aviv, drawn on the same map.
- Events are bound to the selected hour — the slider carries both "how packed" and "what's happening".
- The layer is a **selected** set, not a raw feed: something decides which events are worth surfacing.
- Tapping an event marker opens its detail.
- **Not in scope:** ticketing, booking, promoter placement, or any business-facing monetization (Phase 2 at the earliest, and strategy fences B2B outright); user-submitted events; any list or feed view off the map; push notifications; the pipeline's sourcing and freshness design, which is PAS-5's deliverable.

## Motivation

- Strategy: "Live Events overlay ships in V1 as a third map layer alongside heat + tag."
- Heat says a Hood is packed; events say *why* — the one signal that explains what density can only report.
- Strategy, on the slider: "the time slider carries both kinds of information again, how packed and what's happening."

## Requirements

### Must-have (P0)

1. **Events render on the map, in the current hour.**
   - [ ] An event renders as a marker at its location **at every hour its interval overlaps**, not only at its start hour — an event running 18:00–23:00 renders at 18:00, 19:00, 20:00, 21:00 and 22:00 (corrected at acceptance 2026-08-03, TRD D1; the original wording stated a sufficient condition and was read by an implementer as an exclusive one).
   - [ ] Changing the selected hour changes which events render, inside the 400ms budget (`design/design-principles.md` §2).
   - [ ] An event outside the now → +12h window never renders.
   - [ ] Event markers are distinguishable from place pins by shape or glyph, not colour alone (`design/design-principles.md` §3).
   - [ ] Where a Hood's centroid name label overlaps an event marker, at least half the marker's drawn area still shows on screen — compare marker pixels at that coordinate against the same marker rendered clear of **any** label, pin or other map annotation, **and confirm the reference itself is unclipped before dividing by it** (its drawn area symmetric left-to-right within ~2%). *(Added at acceptance 2026-08-04, T-062/PAS-58. The post-ship redesign shrank the drawn mark to 18pt and the centroid label pill then covers it entirely: **0** marker pixels at the seeded Florentin event, against **43pt** of visible marker for the pre-redesign build at the identical coordinate, camera and zoom. No earlier gate had anything to fail it on — "distinguishable from place pins" presumes the marker renders at all. L-009. **Reference clause tightened at round-4 acceptance 2026-08-04:** "clear of any label" let two consecutive rounds displace the event onto an Apple Maps POI pin, which clipped the reference and silently inflated the ratio — the divisor, not the numerator, was wrong. L-009.)*

2. **The layer never competes with heat.**
   - [ ] Event markers do not use the heat bands' fill treatment or occupy the area channel — heat owns fill, always (`design/map-rendering-spec.md` §2).
   - [ ] ~~Event markers cluster by the same screen-distance rule as place pins, and clusters stay neutral-coloured (`design/map-rendering-spec.md` §5).~~ **Moved to `T-041`/`PAS-30` at acceptance, 2026-08-03** (TRD D4). The shared screen-distance rule is unimplemented anywhere in the app and owned by no PRD; the on-screen marker cap (req 3 bullet 3) is Phase 1's density bound. Event markers join the shared rule when T-041 builds it — this requirement is not waived, it has a different owner.

3. **The set is selected, not exhaustive.**
   - [ ] The layer shows a ranked subset, not every event the pipeline ingested — strategy: "algorithmically selected as likely-interesting to the user (not just a raw feed of every event)."
   - [ ] The client renders the order and inclusion the backend gives it; ranking is not re-derived on device.
   - [ ] The number of markers on screen at once is bounded, so a busy Friday night does not bury the heat layer underneath event pins.
   - [ ] Selection uses no per-user profile, preference store, or interest history — V1 has no identity (see Open questions).

4. **Event detail.**
   - [ ] Tapping a marker opens a sheet with name, time, and location, one tap, map still visible behind it.
   - [ ] **Every visible part of the marker opens that event when tapped** — tap the topmost and the bottommost pixel of the marker's drawn ink; both open the event sheet, neither opens a Hood or place sheet. *(Added at acceptance 2026-08-04, T-062/PAS-58 round 2. The label-occlusion fix grew the drawn mark to 82pt tall while the hit region stayed at 44pt (`EventLayer.swift`'s `Button` frame) / a 22-point tap tolerance (`MapScreen.handleTap`), so at the seeded Florentin event the only ink a user can see falls entirely outside both, and tapping it opens the **Florentin Hood sheet** instead. No earlier gate had anything to fail it on — "tapping a marker" presumed the mark and the target were the same region, which was true until the mark outgrew it. L-009.)*
   - [ ] The sheet offers the same route hand-off contract as a place — native Maps/Waze, walking, no in-app navigation.
   - [ ] Any field the pipeline did not supply is omitted, not shown as a blank row or placeholder.
   - [ ] Every field the sheet renders reads as human text, never an internal identifier — a Hood renders its display name ("Florentin"), never its slug (`kerem-hateimanim`); a category renders its display word, never its raw enum value. *(Added at acceptance 2026-08-03: the shipped sheet renders both raw. No earlier gate had a criterion to fail it on — the requirement existed only as an implicit reading of "location". L-009.)*
   - [ ] **A Hood slug the client cannot resolve to a display name shows no hood row at all** — the sheet renders its other fields normally and nothing appears in the hood row's place: no slug, no blank row, no placeholder, no "Unknown". This is a third case, distinct from the two bullets above it: the pipeline *did* supply a hood field, but the client's loaded Hood set has no match for it (unknown slug, or the Hood set not yet loaded). *(Added at acceptance 2026-08-07, T-052/PAS-40. The shipped fix resolves `hoodID` against the already-loaded Hood list and omits the row on failure — a defensible call, but one no gate could have failed or passed, since "did not supply" and "never a slug" between them left this state unspecified. L-009.)*
   - [ ] **Data dependency, stated so it is not inferred:** the hood row is only renderable because the client already carries the Hood set that maps slug → display name (`hoods-tel-aviv.json`, the same dataset the heat and Hood-sheet surfaces read). This sheet adds no new table, field, or fetch of its own — it reads an existing one. If that dataset is ever fetched lazily rather than bundled, the bullet above becomes the app's normal cold-open behaviour rather than an edge case, and this requirement needs re-deciding, not re-implementing.

5. **The layer degrades to absent, never to broken.**
   - [ ] If the events feed is unreachable or empty, the map renders heat and places normally with no error banner over the map surface.
   - [ ] Stale events — end time already past — never render.
   - [ ] The app is fully usable with the events layer permanently empty. This is the state it ships in if PAS-5 slips.

6. **The layer can be switched off.**
   - [ ] An events toggle sits with the other layer toggles in the heat modal (`design/ux-flows.md` §2, locked 2026-07-29).
   - [ ] Toggling it off leaves heat and place pins untouched.
   - [ ] The toggle state persists across a modal close and reopen within the session.

### Nice-to-have (P1)

- A count on a Hood showing how many surfaced events fall inside it for the selected hour.
- Event category glyphs, if the pipeline supplies a category worth trusting.

## Technical design

- **Data model:** new `events` table — id, name, start/end time, coordinates, hood_id, source, plus a rank column the pipeline writes. Public-read, no user-scoped rows. That rank column is the contract boundary: `data-engineer` owns how it is computed, the client only sorts and truncates by it.
- **Data sourcing (added 2026-07-30, standing rule).** The pipeline that fills this table now has a PRD: [`prds/live-events-pipeline/`](../live-events-pipeline/live-events-pipeline.md). It carries the ingest-side fields this sketch omits (`source_event_id` for dedup, `ingested_at` for freshness), the required-field drop rule, event→Hood attribution, expiry, and the non-personalized rank contract. **`PAS-5` delivered a feasibility read, not a spec** — that gap is what the pipeline PRD closes. Which feed(s) ship is still Aviran's (`PAS-6` item 10); the pipeline PRD is written source-agnostically so it does not pre-decide it.
- **APIs / client-server contract:** one fetch for the whole now → +12h window alongside the map's density load, re-filtered locally per hour rather than re-fetched per slider step. Realtime is not required — periodic refresh is enough for events known in advance.
- **Architecture notes:** `SALVAGE.md` marks `Models/LiveEvent.swift`, `EventMarker.swift`, `EventDetailCard.swift`, `Services/EventsService.swift` REUSE. **Check before reusing:** `prds/INDEX.md` warns the Locali overlay shipped as an unflagged raw feed; the ranked-subset requirement is new and the salvaged service has no notion of it.
- **Dependencies:** the map and time-slider PRDs land first. Hard upstream dependency on [`live-events-pipeline`](../live-events-pipeline/live-events-pipeline.md) for any **real** data, which in turn needs [`hood-dataset`](../hood-dataset/hood-dataset.md) — event→Hood attribution is impossible against placeholder rectangles. **Build Phase 1 needs no backend at all:** a bundled fake event set, carrying the same fields as the `events` table above, drives reqs 1–4 and 6; the empty case (req 5) is a state to verify, not the only Phase-1 state. Authoring that fixture is a named Phase-1 data need — small enough to live here rather than in its own PRD. **Claimed by T-034 and shipped** (`events-tel-aviv-seed.json`, TRD §3.4/D10, confirmed at acceptance 2026-08-03). **The fixture must also be plausible, not merely structurally valid** — added at acceptance: within any one hour bucket, no two events may share a coordinate, and no event may carry a templated name ("Fixture event 1"). The shipped bucket at offset +5 violates both — 14 events named "Fixture event 1…14" at one identical point — which passes the structural authoring rule and still renders as 12 stacked identical markers to anyone opening the demo at that hour. Tracked at T-051.
- **Open technical questions:** refresh cadence; whether rank is absolute or per-hour; the on-screen marker cap, once real Tel Aviv event volume is known.

## Assumptions

- **[ASSUMPTION]** Events are known in advance, so the layer needs periodic refresh rather than Realtime. If PAS-5 finds the useful events are same-hour and unpredictable, the contract changes.

## Open questions & risks

- **The pipeline is launch-blocking; this client is not.** Strategy: "V1 does not ship until data-engineer has a working live-events ingestion pipeline." Requirement 5 exists so the client is shippable with an empty layer, but that does not clear the launch gate — it only means the client is not what blocks it. The gate is `T-043`'s to clear in Build Phase 3. Do not read this PRD as evidence the pipeline will be ready, and do not read the correction above as the gate being softened — it is unchanged, just correctly attributed. **Update 2026-07-30:** `PAS-5` closed with a feasibility verdict of **conditional** — a thin ticketed-only feed is buildable in Phase 1, the version that makes the promise feel true is a data-access gap. The pipeline now has a spec (`live-events-pipeline`); it does not have a chosen source or a confirmed answer to whether thin is acceptable (`PAS-6` item 10).
- **"Likely-interesting to the user" cannot mean personalized in V1, and that needs Aviran's confirmation.** V1 has no accounts, no preference tracking, and no interest history — strategy puts personalization in Phase 3 precisely because it "needs identity and preference tracking neither V1 nor Phase 2 requires." This PRD therefore reads the phrase as *generically* interesting — ranked by quality, popularity, and locality signals, the same for every viewer. If Aviran meant per-user, that is a scope change with an identity dependency behind it, not a ranking tweak.
- Three launch-blocking feasibility questions now stack — events (PAS-5), Scenic Walk routing and TikTok import (PAS-7). Strategy's own Key risks flag this: any one can slip the launch date.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | First PRD pass over the 2026-07-30 V1 lock (PAS-10); events confirmed V1 scope 2026-07-29 and again at the founders meeting |
| 2026-07-30 | "Likely-interesting" spec'd as non-personalized ranking, flagged for Aviran | V1 has no identity or preference tracking; a per-user reading would be a Phase 3 dependency |
| 2026-07-30 | Ingestion pipeline given its own PRD rather than staying fenced out with no spec behind the fence | Standing rule, founder-direct 2026-07-30. Fencing it out was right; leaving the launch-blocking half with only a feasibility note and no requirements was not |
| 2026-07-31 | Launch-blocking header re-attributed to the pipeline (`T-043`, Build Phase 3); this client marked Build Phase 1, unblocked. Strategy's gate itself untouched | The header conflated two things and read as if the client were blocked. Per `BOARD.md` § V1 Build Phases (Aviran, 2026-07-31), the client renders fake/empty data and needs no backend to ship, demo, or QA. The strategy line is Aviran-gated and was not edited, softened, or dropped — only correctly attributed |
| 2026-07-31 | Phase-1 fake event fixture named as a real, unowned data need | Consequence of the above, surfaced by this fix: with an empty feed only, reqs 1–4 and 6 have nothing to test against, so "unblocked for Phase 1" is only true if the fixture exists |
| 2026-08-03 | **D1 CONCUR** — req 1 bullet 1 rewritten from start-hour to overlap | The literal reading makes a four-hour event visible for one of its four hours, which answers a different question than strategy's "what's happening" at the selected hour. The bullet stated a sufficient condition, not an exclusive one. Carries TRD §4.2's drop of `start_at=gte` — `data-engineer` still owes that confirmation |
| 2026-08-03 | **D4 RULED** — req 2 bullet 2 (clustering) moves to `T-041`/`PAS-30`, not waived | The screen-distance rule is unimplemented app-wide and owned by no PRD; blocking a Phase-1 task on an unowned Phase-2 one buys nothing at ≤12 markers. The cap is Phase 1's bound. T-041's board row now carries this requirement |
| 2026-08-03 | **D2 CONFIRMED** — event markers render at every zoom, diverging from `map-rendering-spec.md` §2's "Pins: none at city-wide" | That row solves place-pin density (dozens per Hood); a capped 12-marker city-wide set is a different problem. The spec's own §1 argues *for* it: a non-heat signal invisible at cold-open zoom leaves "heat alone at cold open, the half anyone already gets from Google Maps." **The cap and the zoom rule are one decision** — overturning the cap reopens this. `map-rendering-spec.md` has no events row at all; filed for `designer` at T-052 |
| 2026-08-03 | **D10 CONFIRMED** — the fixture is T-034's, with a plausibility clause added | Phase-1 acceptance covers reqs 1–5 against the fixture only; Phase-3 acceptance re-runs them against the live feed with the constant flipped |
| 2026-08-03 | **Req 6 (toggle) not accepted — deferred to T-050** | Build step C12 is blocked on T-032's `HeatModalCard`, which does not exist. No toggle UI ships; `isLayerVisible` exists as state and the layer and hit-tester both honour it, but nothing user-reachable sets it. Not a build defect — nobody can fix it until T-032 lands |
| 2026-08-03 | **Req 1 bullet 2's 400ms hour-change budget is unverified, not passed** | `qa`'s TEST-PLAN row 1b cites `ColdOpenPerformanceTests`, which measures cold-open-to-interactive, a different milestone. No `HourRepaint` signpost exists in the committed tree and no hour control ships (both T-032's). Re-verify at T-050 |
| 2026-08-04 | **Req 1 gains a marker-legibility bullet** (label occlusion), added at acceptance of T-062/PAS-58's marker redesign | The redesign met every stated requirement and still produced a marker a user cannot see, because no bullet required the marker to survive an overlapping Hood centroid label. Marker size was never floored. The bullet states the rendered consequence, so QA can fail it by pixel count rather than by taste. Does not re-open reqs 1–5's 2026-08-03 acceptance — the shipped marker at that date passed this bullet |
| 2026-08-04 | **Req 4 gains a tappable-ink bullet**, added at T-062/PAS-58's second acceptance | The legibility bullet above floored how much of the marker a user can *see* and said nothing about whether that ink does anything. The fix satisfied it by growing the drawn mark past the hit region, so the visible ink became dead pixels that fall through to `HoodLayer`. Legibility and reachability are two requirements; only one of them existed. Stated as the rendered consequence (which sheet opens), not as a geometry constraint, so a future fix may shrink the mark or grow the target |
| 2026-08-04 | **T-062/PAS-58 round 3 ACCEPTED** at round-4 acceptance (`passenger-code f6ee513`); req 1's legibility bullet gains a reference-integrity clause | Both bars that drove rounds 1–2 pass on independent live measurement: **90.5%** marker visibility at the seeded Florentin fixture (2,914px occluded / 3,220px clean reference, floor is ≥50%), and topmost *and* bottommost visible ink both open the event sheet, with a negative-control tap 60pt clear opening the Hood sheet to prove the test discriminates. The clause was added because the bullet's stated method produced an inflated number twice: displacing the event "clear of any label" landed it on an Apple Maps POI pin that clipped the **reference**, so the divisor was too small (designer's 92.5%, and this pass's own first attempt at 92.6%, both against a clipped reference). Requirement text unchanged in substance — only the measurement procedure is now falsifiable on the reference as well as the subject. PRD `Status:` deliberately unchanged: this is a post-ship redesign against reqs already accepted 2026-08-03, not a new acceptance |
| 2026-08-07 | **T-052/PAS-40 ACCEPTED** (`passenger-code 174a5bb`, `passenger-brain eea8a23`); req 4 gains an unresolved-slug bullet and an explicit data-dependency line | The fix satisfies the 2026-08-03 "never an internal identifier" bullet — `MapScreen` resolves `hoodID` off the loaded Hood list and hands the name in by value; `EventDetailRows.displayCategory` humanizes the raw pipeline category, which has no enum to key a `displayName` off of the way `PlaceCategory` does. Verified by reading source at HEAD, not by trusting the commit message. But the fix also **introduced a third rendering state no bullet covered** — a hood field the pipeline *did* supply that the client cannot resolve — and chose to omit the row. Right call, but it shipped unspecified, so no gate could have passed or failed it. Bullet added stating the rendered consequence (nothing appears where the row would be), plus the standing data-need rule made explicit: the hood row is renderable only because the client already carries `hoods-tel-aviv.json`; this sheet adds no data of its own. `map-rendering-spec.md` §2 now carries the Event markers column with D2's cap and every-zoom rule stated together, matching TRD §4.5 word for word on the "one decision, not two" point. PRD `Status:` unchanged — this is a defect fix against reqs already accepted 2026-08-03, not a new acceptance |

