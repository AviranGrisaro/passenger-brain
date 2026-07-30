# Live Events Overlay — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Launch-blocking:** V1 does not ship until `data-engineer` has a working ingestion pipeline (Linear PAS-5, scoping in flight). This PRD specs the client surface and the data contract it needs; it does not assume the pipeline exists.

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
   - [ ] An event with a start time inside the selected hour renders as a marker at its location.
   - [ ] Changing the selected hour changes which events render, inside the 400ms budget (`design/design-principles.md` §2).
   - [ ] An event outside the now → +12h window never renders.
   - [ ] Event markers are distinguishable from place pins by shape or glyph, not colour alone (`design/design-principles.md` §3).

2. **The layer never competes with heat.**
   - [ ] Event markers do not use the heat bands' fill treatment or occupy the area channel — heat owns fill, always (`design/map-rendering-spec.md` §2).
   - [ ] Event markers cluster by the same screen-distance rule as place pins, and clusters stay neutral-coloured (`design/map-rendering-spec.md` §5).

3. **The set is selected, not exhaustive.**
   - [ ] The layer shows a ranked subset, not every event the pipeline ingested — strategy: "algorithmically selected as likely-interesting to the user (not just a raw feed of every event)."
   - [ ] The client renders the order and inclusion the backend gives it; ranking is not re-derived on device.
   - [ ] The number of markers on screen at once is bounded, so a busy Friday night does not bury the heat layer underneath event pins.
   - [ ] Selection uses no per-user profile, preference store, or interest history — V1 has no identity (see Open questions).

4. **Event detail.**
   - [ ] Tapping a marker opens a sheet with name, time, and location, one tap, map still visible behind it.
   - [ ] The sheet offers the same route hand-off contract as a place — native Maps/Waze, walking, no in-app navigation.
   - [ ] Any field the pipeline did not supply is omitted, not shown as a blank row or placeholder.

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
- **APIs / client-server contract:** one fetch for the whole now → +12h window alongside the map's density load, re-filtered locally per hour rather than re-fetched per slider step. Realtime is not required — periodic refresh is enough for events known in advance.
- **Architecture notes:** `SALVAGE.md` marks `Models/LiveEvent.swift`, `EventMarker.swift`, `EventDetailCard.swift`, `Services/EventsService.swift` REUSE. **Check before reusing:** `prds/INDEX.md` warns the Locali overlay shipped as an unflagged raw feed; the ranked-subset requirement is new and the salvaged service has no notion of it.
- **Dependencies:** the map and time-slider PRDs land first. Hard upstream dependency on PAS-5 for any real data.
- **Open technical questions:** refresh cadence; whether rank is absolute or per-hour; the on-screen marker cap, once real Tel Aviv event volume is known.

## Assumptions

- **[ASSUMPTION]** Events are known in advance, so the layer needs periodic refresh rather than Realtime. If PAS-5 finds the useful events are same-hour and unpredictable, the contract changes.

## Open questions & risks

- **PAS-5 is launch-blocking and unresolved.** Strategy: "V1 does not ship until data-engineer has a working live-events ingestion pipeline." Requirement 5 exists so the client is shippable with an empty layer, but that does not clear the launch gate — it only means the client is not what blocks it. Do not read this PRD as evidence the pipeline will be ready.
- **"Likely-interesting to the user" cannot mean personalized in V1, and that needs Aviran's confirmation.** V1 has no accounts, no preference tracking, and no interest history — strategy puts personalization in Phase 3 precisely because it "needs identity and preference tracking neither V1 nor Phase 2 requires." This PRD therefore reads the phrase as *generically* interesting — ranked by quality, popularity, and locality signals, the same for every viewer. If Aviran meant per-user, that is a scope change with an identity dependency behind it, not a ranking tweak.
- Three launch-blocking feasibility questions now stack — events (PAS-5), Scenic Walk routing and TikTok import (PAS-7). Strategy's own Key risks flag this: any one can slip the launch date.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | First PRD pass over the 2026-07-30 V1 lock (PAS-10); events confirmed V1 scope 2026-07-29 and again at the founders meeting |
| 2026-07-30 | "Likely-interesting" spec'd as non-personalized ranking, flagged for Aviran | V1 has no identity or preference tracking; a per-user reading would be a Phase 3 dependency |
