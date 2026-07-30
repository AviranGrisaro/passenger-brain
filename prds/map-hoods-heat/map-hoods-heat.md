# Map — Hoods & Heat Area — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Scope note:** the localness / tourist-trap layer is deliberately **excluded** from this PRD — decision #28 is flagged unconfirmed (Linear PAS-6 item 1). This PRD specs the base map, Hoods, and heat only.

## Description

- The single map screen the whole product lives on. Tel Aviv only.
- Base MapKit layer, opening city-wide, straight from the app icon.
- The city is divided into **Hoods** — the product-facing name for zone/neighborhood granularity (decision #27, granularity itself unchanged from decision #12).
- Each Hood carries a **heat area**: crowd density for the currently selected hour, drawn as stepped bands, never a gradient (decision #17).
- Density is a synthetic feed in V1, time-bound to the selected hour.
- Location permission is asked lazily and never blocks the map.
- **Not in scope:** the localness / tourist-trap layer and its rendering (PAS-6 item 1); the time slider and heat modal; Hood and place detail sheets; search and quick filters; the live-events layer; Places, Passport, routing, TikTok import; any city other than Tel Aviv.

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
   - [ ] Hood polygons do not overlap: any coordinate resolves to at most one Hood.
   - [ ] One tap inside a Hood opens that Hood's sheet — never a two-step "tap to preview, tap again to open".

4. **Heat area rendering.**
   - [ ] Heat renders as a stepped-band fill over the Hood area. Zero gradients anywhere in the layer (decision #17).
   - [ ] Heat is visible at 0 taps on cold open; no control gates it.
   - [ ] The same band always means the same density value, at every zoom.
   - [ ] Heat encodes crowd density and nothing else — no blended "is it good" score is ever computed or drawn (`SALVAGE.md`: `DensityContract.swift`).

5. **Heat is bound to one hour at a time.**
   - [ ] The map reads "now" until something changes the selected hour.
   - [ ] Changing the selected hour repaints heat for that hour and leaves every other layer untouched.
   - [ ] Repaint completes inside the Doherty budget — under 400ms (`design/design-principles.md` §2).

6. **Lazy location permission.**
   - [ ] The When-In-Use system prompt appears only after the map is on screen.
   - [ ] Granted: the map recenters on the user and shows a "you are here" marker.
   - [ ] Denied: the map stays city-wide, stays fully usable, and is never re-prompted in the same install.

7. **Degraded data is silent, not broken.**
   - [ ] A Hood with no density value for the selected hour renders with no fill and no error copy.
   - [ ] If the density feed is unreachable, the base map and Hood geometry still render and remain interactive.

### Nice-to-have (P1)

- Near-me recenter button (`design/ux-flows.md` §2 lists it as Primary chrome).
- Hood name label at neighborhood zoom.

## Technical design

- **Data model:** new `hoods` (id, name, city, polygon) and `hood_density` (hood_id, hour_bucket, band) tables. Public-read, no per-user rows, so RLS is read-only-for-all; this feature adds no identity and no writes.
- **APIs / client-server contract:** Hood polygons fetch once per session and cache — static reference data. Density fetches as 13 hour buckets (now → +12h) so the slider never round-trips per drag. No Realtime in V1; the feed is synthetic (decision #4).
- **Architecture notes:** MapKit overlays per the master strategy's stack. `SALVAGE.md` marks `DensityMark.swift`, `DensityPlaceMark.swift`, `DensityContract.swift`, `HeatPlace`/`HeatState` REUSE; `MapScreen.swift` is REFERENCE only — mine its clustering and camera handling, discard the 940-line view.
- **Dependencies:** none upstream. Blocks the time-slider, Hood/place-detail, and live-events PRDs.
- **Open technical questions:** whether Hood polygons ship bundled or come from Supabase; hour-bucket key shape (absolute timestamp vs. offset); band count and thresholds — a `data-engineer` call.

## Assumptions

- **[ASSUMPTION]** Hood polygons are authored once and change rarely, so caching them for the session is safe. If curation turns out to be continuous, this needs a refresh path.

## Open questions & risks

- **The second layer is missing and this is the main risk.** Decision #28 (tourist-trap boolean vs. decision #18's Local/Mix/Tourist tag) is unconfirmed — PAS-6 item 1 — so no localness signal is spec'd here. `design/map-rendering-spec.md` §1 makes the cost explicit: heat alone is the half of this product anyone already gets from Google Maps. This PRD is buildable without it; the product is not shippable without it.
- Density is synthetic at launch, so "right now" is simulated until a live popular-times source lands (strategy, Key risks).
- `agent-os/BOARD.md`'s scope-gate section still says Live Events and Scenic View are out of V1 (2026-07-27). Strategy reversed both; the board text is stale and should not be read as a prohibition.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created, covering base map + Hoods + heat only | First PRD pass over the 2026-07-30 founders-meeting V1 lock (PAS-10) |
| 2026-07-30 | Localness / tourist-trap layer excluded rather than spec'd with a guess | Decision #28 flagged unconfirmed; scope gate forbids specing against an unconfirmed line (PAS-6 item 1) |
