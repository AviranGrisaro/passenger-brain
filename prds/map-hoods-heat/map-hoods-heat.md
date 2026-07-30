# Map — Hoods & Heat Area — PRD

**Status:** Accepted (T-031, 2026-07-30) — two named data gaps carried past acceptance, see the Decisions log
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Scope note (rewritten at `design-approval`, 2026-07-30):** the tourist-trap layer is still **excluded** from this PRD, but **not because it is blocked** — decision #37 resolved PAS-6 item 1 the same day this PRD was first written, and the layer now has its own PRD (`prds/tourist-trap-flag/tourist-trap-flag.md`). The split is by rendering channel, per `design/map-rendering-spec.md` §2: **heat owns the Hood's area fill, the flag owns the Hood's outline stroke, and they never share a channel at any zoom.** This PRD specs the base map, Hoods, and the fill.

## Description

- The single map screen the whole product lives on. Tel Aviv only.
- Base MapKit layer, opening city-wide, straight from the app icon.
- The city is divided into **Hoods** — the product-facing name for zone/neighborhood granularity (decision #27, granularity itself unchanged from decision #12).
- Each Hood carries a **heat area**: crowd density for the currently selected hour, drawn as stepped bands, never a gradient (decision #17).
- Density is a synthetic feed in V1, time-bound to the selected hour.
- Location permission is asked lazily and never blocks the map.
- **Not in scope:** the tourist-trap layer and its rendering — a sibling PRD, `prds/tourist-trap-flag/tourist-trap-flag.md`, which owns the Hood outline stroke and the centroid word label; the time slider and heat modal; Hood and place detail sheets; search and quick filters; the live-events layer; Places, Passport, routing, TikTok import; any city other than Tel Aviv.

## Motivation

- The map *is* the product — [strategy](../../strategy/passenger-strategy.md): "V1 is a single map, and the whole product lives on it."
- Nothing else in V1 can be built or tested until the base map, Hood geometry, and the density contract exist.
- Phase 1's question — does a stranger reopen within a week — is asked of this screen, not of any feature layered on it.

## Requirements

### Must-have (P0)

1. **Cold open goes straight to the map.** Strategy: "No onboarding. Straight to the map + location permission."
   - [ ] First frame after the app icon is the map. No splash, no carousel, no sign-in, no permission gate.
   - [ ] The map is pannable, zoomable and tappable before any permission is answered.
   - [ ] A "Tel Aviv, right now" title fades in and out within ~2s and leaves no persistent chrome (decision #8).
   - [ ] Cold launch to an interactive map completes under 3s on the oldest supported device.

2. **Tel Aviv only.**
   - [ ] Default camera is a city-wide Tel Aviv view.
   - [ ] No city picker exists in the UI and no second city exists in the shipped data.
   - [ ] Panning outside Tel Aviv shows plain base map with no Hoods and no heat — no error, no crash, no empty-state takeover.

3. **Hoods.**
   - [ ] Each Hood is a named polygon; Tel Aviv ships dozens of them, not thousands (decision #12's bound).
     - **Unmet at `acceptance` 2026-07-30 — carried, not waived.** The shipped artifact holds 4 hand-authored rectangles in the client bundle (`Resources/hoods-tel-aviv.json`) and 5 rough placeholders in migration `001`'s seed. That is not "dozens." No gate failed it because every gate correctly read it as placeholder data pending B3, and B3 shipped an export *script* with no real dataset to export. **Real Tel Aviv Hood geometry needs its own board row and its own review; this bullet is satisfied there, not by T-031.**
   - [ ] Hood polygons do not overlap: any coordinate resolves to at most one Hood.
     - **Pass condition (added at `acceptance` 2026-07-30 — the bullet had none, so no gate could fail it).** With the shipped geometry loaded, no coordinate in Tel Aviv opens two different Hood sheets on repeat taps, and no Hood's fill paints over a neighbour's. **Nothing enforces this today** — `HoodHitTester` documents non-overlap as a premise it relies on and resolves any overlap silently to file order (`hoods.first(where:)`), and no test asserts the invariant. The geometry must therefore be overlap-validated *before* it is bundled, and a violation must fail that validation loudly rather than render. Latent while the fixture is 4 disjoint rectangles; live the moment real municipal boundaries land.
   - [ ] One tap inside a Hood opens that Hood's sheet — never a two-step "tap to preview, tap again to open".

4. **Heat area rendering.**
   - [ ] Heat renders as a stepped-band fill over the Hood area. Zero gradients anywhere in the layer (decision #17).
   - [ ] **No blur, feather, or soft edge is applied to the fill at any zoom.** Band boundaries follow Hood boundaries exactly. `map-rendering-spec.md` §2 calls city-wide heat "neighborhood-scale blobs, stepped bands" — "blob" is the coarseness of the *shape*, never a softened edge; a blurred band is a gradient and fails decision #17. *(Added at `design-approval` 2026-07-30 — the original bullet was read as permitting a city-wide blur.)*
   - [ ] Heat is visible at 0 taps on cold open; no control gates it.
   - [ ] The same band always means the same density value, at every zoom. **The band→appearance mapping is one fixed table: no zoom-dependent opacity clamp, no per-zoom recolouring, no compression of the gap between adjacent bands.** *(Second sentence added at `design-approval` 2026-07-30.)*
   - [ ] Heat encodes crowd density and nothing else — no blended "is it good" score is ever computed or drawn (`SALVAGE.md`: `DensityContract.swift`).

5. **Heat is bound to one hour at a time.**
   - [ ] The map reads "now" until something changes the selected hour.
   - [ ] Changing the selected hour repaints heat for that hour and leaves every other layer untouched.
   - [ ] Repaint completes inside the Doherty budget — under 400ms (`design/design-principles.md` §2).
   - **Verification split (added at `acceptance` 2026-07-30).** Only bullet 1 is exercisable inside this PRD's scope — nothing here changes the selected hour (the slider is T-032), so `qa` traced no behavioral case to this requirement at all and no gate had anything to fail. Bullet 1 is met by `DensityStoreTests` (`selectedHour` starts at the current hour; `band(for:hour:)` never triggers a fetch, so an hour change is a pure repaint). **Bullets 2 and 3 transfer to T-032's acceptance** and must be verified there against a real slider drag with real density data. They are not satisfied by T-031.

6. **Lazy location permission.**
   - [ ] The When-In-Use system prompt appears only after the map is on screen.
   - [ ] Granted: the map recenters on the user and shows a "you are here" marker.
   - [ ] Denied: the map stays city-wide, stays fully usable, and is never re-prompted in the same install.

7. **Degraded data is silent, not broken.**
   - [ ] A Hood with no density value for the selected hour renders with no fill and no error copy.
   - [ ] **No on-map text of any kind announces the gap** — not "no data", not "not rated", at any zoom. On the map surface a gapped Hood is indistinguishable from a not-yet-curated one; the sentence lives in the Hood sheet (T-033), which is reached by tapping. Same convention as `map-rendering-spec.md` §3: the map never pre-announces absence. *(Added at `design-approval` 2026-07-30 — "no error copy" was read as permitting a neutral "no data yet" label.)*
   - [ ] If the density feed is unreachable, the base map and Hood geometry still render and remain interactive.

### Nice-to-have (P1)

- Near-me recenter button (`design/ux-flows.md` §2 lists it as Primary chrome).
- Hood name label at neighborhood zoom. **The name and nothing else** — heat may not put a word at a Hood centroid. That channel is reserved: `map-rendering-spec.md` §2/§3 assign the centroid word label to the tourist-trap flag ("Tourist-heavy spot" / "busy and tourist-heavy"), and `prds/tourist-trap-flag/` req 3 builds it there. A density word beside the name would put two word labels on one centroid — the stacked-signal density Aviran rejected verbatim (`map-rendering-spec.md` §1). Density's non-visual channel is the VoiceOver label, per §7 of that doc. *(Added at `design-approval` 2026-07-30.)*

## Technical design

- **Data model:** new `hoods` (id, name, city, polygon) and `hood_density` (hood_id, hour_bucket, band) tables. Public-read, no per-user rows, so RLS is read-only-for-all; this feature adds no identity and no writes.
- **APIs / client-server contract:** Hood polygons fetch once per session and cache — static reference data. Density fetches as 13 hour buckets (now → +12h) so the slider never round-trips per drag. No Realtime in V1; the feed is synthetic (decision #4).
- **Architecture notes:** MapKit overlays per the master strategy's stack. `SALVAGE.md` marks `DensityMark.swift`, `DensityPlaceMark.swift`, `DensityContract.swift`, `HeatPlace`/`HeatState` REUSE; `MapScreen.swift` is REFERENCE only — mine its clustering and camera handling, discard the 940-line view.
- **Dependencies:** none upstream. Blocks the time-slider, Hood/place-detail, and live-events PRDs.
- **Open technical questions — all resolved in [`TRD.md`](./TRD.md) (2026-07-30):** Hood polygons ship **bundled** (§2.2, §8 D3); hour-bucket keys on an **absolute UTC timestamp** (§3.1). **Band count and names are locked at three — `quiet` / `moderate` / `busy`** (TRD §1); only the numeric thresholds remain a `data-engineer` call.

## Assumptions

- **[ASSUMPTION]** Hood polygons are authored once and change rarely, so caching them for the session is safe. If curation turns out to be continuous, this needs a refresh path.

## Open questions & risks

- **The second layer is no longer blocked, only separate — and that changes the risk's shape.** Decision #37 (2026-07-30) resolved PAS-6 item 1: the tourist-trap boolean fully replaces decision #18's Local/Mix/Tourist tag. The layer is now specced in `prds/tourist-trap-flag/tourist-trap-flag.md`, whose Dependencies put this PRD first (it needs Hood geometry and the stroke channel). The residual risk is **sequencing, not scope**: `map-rendering-spec.md` §1 is explicit that heat alone is the half of this product anyone already gets from Google Maps, so shipping this feature is not shipping a product. Nothing built here may consume the outline stroke or the centroid word label (reqs 4, 7, P1) — those are the flag's channels, and a design that borrows them forces a redesign when the flag lands.
- **This feature was accepted without anyone ever seeing heat render.** No backend was reachable at any point in the pipeline — migrations `001`/`002` are unapplied, so every observation from `build` through `qa` was of the permanent no-data state. Every heat bullet (req 4, req 5, req 7's first bullet) passed *by construction* — code read, unit test, single-argument palette signature — not by observation. Three of the five acknowledged gaps (live RPC 401/403, offline-with-cache indicator, toy geometry) are one root cause wearing three hats. **The first time the map is seen painted will be after Aviran applies the migrations and enables `pg_cron`; treat that as a real verification event, not a formality.** *(Added at `acceptance` 2026-07-30.)*
- Density is synthetic at launch, so "right now" is simulated until a live popular-times source lands (strategy, Key risks).
- ~~`agent-os/BOARD.md`'s scope-gate section still says Live Events and Scenic View are out of V1 (2026-07-27).~~ **Resolved 2026-07-30** — the board's scope-gate section now carries the reversal struck-through and explicitly says not to read it as a prohibition. No longer a live risk.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created, covering base map + Hoods + heat only | First PRD pass over the 2026-07-30 founders-meeting V1 lock (PAS-10) |
| 2026-07-30 | Localness / tourist-trap layer excluded rather than spec'd with a guess | Decision #28 flagged unconfirmed; scope gate forbids specing against an unconfirmed line (PAS-6 item 1) |
| 2026-07-30 | Draft v2. Exclusion of the tourist-trap layer **kept**, reasoning replaced: no longer "blocked on PAS-6 item 1" (decision #37 resolved it hours after v1 was written) but "owned by a sibling PRD, split by rendering channel — fill here, stroke there" | Called at `design-approval` on T-031. Reopening this PRD's scope would duplicate `prds/tourist-trap-flag/` and stall the three PRDs that depend on this one; the channel split is already locked in `map-rendering-spec.md` §2 |
| 2026-07-30 | Three requirement bullets tightened and one P1 constrained (reqs 4, 7, P1 — blur/feather, per-zoom band mapping, on-map gap text, centroid word label) | T-031's design read each original bullet the permissive way. The bullets were falsifiable enough to reject the design; they were not specific enough to have prevented it (L-009 shape, applied at design rather than acceptance) |
| 2026-07-30 | **ACCEPTED at `acceptance`.** Status flipped to Accepted (L-006). Two P0 bullets carried past acceptance as named gaps rather than waived: req 3's "dozens of Hoods" (shipped data is 4+5 placeholders — needs its own board row) and every heat-rendering bullet (verified by construction only, never observed with data) | `qa`'s 24 traced cases cover every P0 that this task's scope can exercise; the two carried gaps are data-availability, not build defects, and no rejection loop to `build` or `design` could close either — both need Aviran (migrations, `pg_cron`) or a separate geometry deliverable |
| 2026-07-30 | Two missing pass/fail criteria written in at `acceptance` (L-009): req 3's non-overlap bullet gained a rendered-consequence pass condition + the note that nothing enforces it; req 5 gained a verification split assigning bullets 2-3 to T-032 | Neither bullet was falsifiable against anything this task produces — `qa` traced zero cases to req 5 and no case to the non-overlap invariant, so no gate could have failed either. `HoodHitTester` relies on non-overlap as an unchecked premise, which becomes a live defect the moment real municipal boundaries replace the 4 disjoint fixture rectangles |
| 2026-07-30 | Open-technical-questions line rewritten: all three resolved in the TRD. **Band count and names locked at three (`quiet`/`moderate`/`busy`); the open `data-engineer` call narrows to thresholds only** | `trd-review` — `code-reviewer`, `developer`, and `data-engineer` each independently caught that the TRD's schema and `HeatBand` enum already hardcoded 3 bands while this line still called the count open. `data-engineer` added the decisive reason: `map-rendering-spec.md` L42 already keys the tourist-trap flag's warning stroke to a band named "busy," so a sibling PRD couples the count and naming regardless (TRD §1) |
