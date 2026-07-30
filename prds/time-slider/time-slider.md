# Time Slider — now → +12h — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Scope note:** unchanged by the 2026-07-30 founders-meeting lock — this is the one V1 item strategy marks "Unchanged."

## Description

- A single control that moves the whole map forward in time, from now to +12 hours.
- Snaps to whole hours; there is no sub-hour position.
- Lives inside the **heat modal**, opened by the heat button in map chrome (`design/ux-flows.md` §2, locked 2026-07-29) — it is not permanent map chrome.
- Every hour-bound layer on the map repaints for the selected hour; the map otherwise stays exactly where it is.
- Resets to "now" on every app launch.
- **Not in scope:** the heat layer's own rendering rules (see the map PRD); the layer toggles that share the heat modal — each belongs to the layer it toggles; anything past +12h or before now; scheduling, reminders, or notifications tied to a future hour.

## Motivation

- Strategy: "A place's relevance changes by the hour; the map knows that." A map fixed to "now" answers where to go this second, not where to go after dinner.
- It is the only V1 control that makes the map a planning tool as well as a live read — [Phase 1](../../strategy/passenger-strategy.md#rollout-sequence) needs both the tourist who just landed and the resident planning tonight.
- The behaviour is already worked out in the old codebase (`SALVAGE.md`: `HeatmapControlsSheet.swift`, REFERENCE) — this PRD exists to pin the contract, not to invent it.

## Requirements

### Must-have (P0)

1. **Range is now → +12 hours, hour-snapped.**
   - [ ] Exactly 13 selectable positions: now, +1h … +12h.
   - [ ] The control cannot be dragged below "now" or above "+12h" — no wrap, no elastic overshoot past the ends.
   - [ ] Releasing a drag lands on a whole hour, never between two.

2. **The map repaints for the selected hour.**
   - [ ] Changing the hour repaints every hour-bound layer for that hour.
   - [ ] Camera position, zoom, and any open sheet are unchanged by an hour change.
   - [ ] Repaint completes under 400ms (`design/design-principles.md` §2, Doherty Threshold).
   - [ ] With no data for the selected hour, affected areas render empty — no error banner, no modal.

3. **"Now" is the default, every launch.**
   - [ ] On every cold launch the selected hour is "now", regardless of where it was left last session.
   - [ ] "Now" re-resolves against the actual clock at launch, not against a cached value from the previous session.
   - [ ] Opening the heat modal shows the slider at "now" unless the current session has already moved it.

4. **Session persistence inside the modal.**
   - [ ] Closing and reopening the heat modal within one session restores the hour the user left it at (`design/ux-flows.md` §2.1, modal-exclusivity rule).
   - [ ] Switching to a different nav modal and back does not reset the hour.

5. **The selected hour is readable as a number, not only as a position.**
   - [ ] A visible numeral or label states the selected hour at all times while the control is on screen.
   - [ ] An explicit "now" tick is drawn on the track as a fixed anchor.
   - [ ] Meaning is never carried by colour alone (`design/design-principles.md` §3).

6. **Accessibility.**
   - [ ] VoiceOver exposes a discrete, announceable step — each step announces the hour it lands on; the control is not continuous-drag-only.
   - [ ] The control's touch target is ≥44pt (`design/design-principles.md` §2, Fitts's Law).
   - [ ] The control remains usable and legible at the largest supported Dynamic Type size.
   - [ ] **Every** text label rendered inside the heat modal meets 4.5:1 against the surface it sits on, in **both** light and dark — the numeral, the "now" tick label, the end-of-track labels, the "next day" flag, and the modal's own section headers included. There is no enumeration exception: a label no design pass happened to list is still covered.
   - [ ] The non-text parts that carry the control's state — the thumb, the boundary between filled and unfilled track, and the "now" tick — meet 3:1 against their adjacent colours in both themes. The inactive track rail is explicitly **not** held to 3:1: it carries no state, and the native `Slider` this feature is specified to use renders it low-contrast by platform default (`design/design-principles.md` §5, WCAG AA).
   - *Both bullets added/corrected at `design-approval`, 2026-07-30. Req 6 originally had no contrast criterion at all, so no gate could objectively fail a design that asserted the bar and missed it (L-009, applied early rather than at acceptance). The first version enumerated three labels and held the whole track line to 3:1 — both wrong: the enumeration let an unlisted label through, and a 3:1 inactive rail is unachievable with the native control req 6's own VoiceOver bullet depends on.*

### Nice-to-have (P1)

- Haptic tick on each hour crossing.
- Absolute clock time alongside the relative offset ("+3h · 21:00").

## Technical design

- **Data model:** none new. Consumes the `hood_density` hour buckets defined in the map PRD; the slider owns no persisted state — its position is in-memory session state only.
- **APIs / client-server contract:** all 13 hour buckets are fetched with the map's initial density load, so dragging the slider is a local re-read, not a network round trip. This is what makes the 400ms budget achievable; a per-hour fetch would not.
- **Architecture notes:** the selected hour is a single source of truth held above the map view and read by every hour-bound layer, so a layer added later (live events) subscribes to it rather than owning its own copy. `SALVAGE.md` marks `HeatmapControlsSheet.swift` REFERENCE — extract the hour-windowing model, discard the 1,069-line view; `Models/HeatTimeWindow.swift` is REUSE.
- **Dependencies:** the map PRD (heat area, density contract) must land first. The live-events PRD depends on this control existing.
- **Open technical questions:** whether "now" re-resolves while the app sits foregrounded across an hour boundary, or only on launch and modal-open.

## Open questions & risks

- **[ASSUMPTION]** The heat modal is the slider's only home. This was locked in the 2026-07-29 design pass, not in the strategy doc; if Aviran wants the slider back on permanent map chrome, requirement 4 changes shape.
- Synthetic density means every future hour is a simulation, not a forecast (strategy, Key risks). The control will feel precise before the data behind it is. Nothing in V1 tells the user that; worth an explicit call before launch.
- Hour buckets past midnight cross a day boundary — confirm the data model keys on absolute time, not hour-of-day, or +12h from 8pm silently reads the wrong day.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | First PRD pass over the 2026-07-30 V1 lock (PAS-10); slider is the one item strategy marks unchanged |
| 2026-07-30 | Req 6 gains an explicit contrast bullet (4.5:1 text / 3:1 non-text, both themes) | `design-approval` found the design spec asserting that bar and the mockup missing it at 3.22:1 light / 3.61:1 dark on the end-of-track and "now"-tick labels. The PRD had no contrast bullet at all, so no gate — QA included — had anything objective to fail it on. Adds a testable criterion; does not change scope (L-009, applied at design-approval rather than acceptance) |
| 2026-07-30 | That bullet split in two and corrected at the second `design-approval` pass | Two defects in my own criterion, found by re-checking the fixed artifact against it. (1) It enumerated three labels, so `.sheet-eyebrow` — the modal's own "Time" header, 10.5px on `--fg-faint`, 3.22:1 light / 3.61:1 dark — sat outside a bar it plainly belongs inside. Now stated as "every text label in the modal," no enumeration. (2) It held "the track line" to 3:1; the inactive rail computes to 1.29:1 light / 1.28:1 dark and cannot clear 3:1 on the native `Slider` req 6's VoiceOver bullet depends on. WCAG's non-text bar applies to what identifies the component and its state — thumb (3.93:1 / 6.62:1), filled-vs-unfilled boundary (3.05:1 / 5.16:1) and the "now" tick (17.99:1 / 14.57:1), all of which clear it. Rejecting a design against an infeasible criterion would have been rejecting against a stale spec |
