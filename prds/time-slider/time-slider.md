# Time Slider — now → +12h — PRD

**Status:** Draft v2
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-31
**Scope note:** the feature is unchanged by the 2026-07-30 founders-meeting lock — the one V1 item strategy marks "Unchanged." **v2 changes how the control is invoked and dragged, not what it does** (founder-direct, 2026-07-31; verbatim quote in `agent-os/PROGRESS.md`'s FOUNDER-DIRECT STUB that date). The delivered design spec and [`TRD.md`](./TRD.md) (`2f955fe`) describe the superseded heat-button/modal + horizontal-`Slider` model; both need re-issuing.

## Description

- A single control that moves the whole map forward in time, from now to +12 hours.
- Snaps to whole hours; there is no sub-hour position.
- **Invoked by a swipe inward from either screen edge, and moved by a vertical (up/down) drag, not a horizontal one** (founder-direct, 2026-07-31). It is not permanent map chrome; it appears on the gesture and goes away again. Whether the gesture is the *only* way in, or sits alongside the heat button the earlier design used, is open — see Open questions.
- Every hour-bound layer on the map repaints for the selected hour; the map otherwise stays exactly where it is.
- Resets to "now" on every app launch.
- **Not in scope:** the heat layer's own rendering rules (see the map PRD); the layer toggles that share whatever surface houses the heat controls — each belongs to the layer it toggles; the rest of the nav row and its other buttons; anything past +12h or before now; scheduling, reminders, or notifications tied to a future hour.

## Motivation

- Strategy, verbatim: "Time slider, now → +12 hours. A place's relevance changes by the hour; the map knows that. Unchanged." A map fixed to "now" answers where to go this second, not where to go after dinner.
- **Re-checked at v2:** that line names the control and its range, not how a finger reaches it, so it still authorizes the feature after the gesture change. No strategy edit needed, and none was made — scope changes stay Aviran's.
- It is the only V1 control that makes the map a planning tool as well as a live read — [Phase 1](../../strategy/passenger-strategy.md#rollout-sequence) needs both the tourist who just landed and the resident planning tonight.
- The behaviour is already worked out in the old codebase (`SALVAGE.md`: `HeatmapControlsSheet.swift`, REFERENCE) — this PRD exists to pin the contract, not to invent it.

## Requirements

### Must-have (P0)

1. **Range is now → +12 hours, hour-snapped.**
   - [ ] Exactly 13 selectable positions: now, +1h … +12h.
   - [ ] The control cannot be moved past "now" at one end or "+12h" at the other — no wrap, no elastic overshoot past the ends.
   - [ ] Releasing a drag lands on a whole hour, never between two.
   - [ ] All 13 positions are reachable in one vertical drag at the largest supported Dynamic Type size, without a second gesture. *(Added at v2 — a phone's vertical axis is shorter than the horizontal one this was written against, so "13 positions fit" stopped being free.)*

2. **The map repaints for the selected hour.**
   - [ ] Changing the hour repaints every hour-bound layer for that hour.
   - [ ] Camera position, zoom, and any open sheet are unchanged by an hour change.
   - [ ] Repaint completes under 400ms (`design/design-principles.md` §2, Doherty Threshold).
   - [ ] With no data for the selected hour, affected areas render empty — no error banner, no modal.

3. **"Now" is the default, every launch.**
   - [ ] On every cold launch the selected hour is "now", regardless of where it was left last session.
   - [ ] "Now" re-resolves against the actual clock at launch, not against a cached value from the previous session.
   - [ ] The first invocation of the control in a session shows it at "now".

4. **Session persistence across dismissals.**
   - [ ] Dismissing the control and invoking it again within one session restores the hour the user left it at — from either edge.
   - [ ] Opening and closing any other nav surface in between does not reset the hour (`design/ux-flows.md` §2.1, exclusivity rule).
   - [ ] The hour survives every dismissal path the design defines, not only the primary one.

5. **The selected hour is readable as a number, not only as a position.**
   - [ ] A visible numeral or label states the selected hour at all times while the control is on screen.
   - [ ] An explicit "now" mark is drawn on the track as a fixed anchor, at the range end the control treats as "now".
   - [ ] Meaning is never carried by colour alone (`design/design-principles.md` §3).

6. **Accessibility.**
   - [ ] VoiceOver exposes a discrete, announceable step — each step announces the hour it lands on; the control is not continuous-drag-only.
   - [ ] **With VoiceOver on, the control is reachable and all 13 hours are selectable without performing the edge swipe.** VoiceOver claims the screen's swipe gestures, and Switch Control users may not be able to produce an edge drag at all — a gesture-only entry path makes the feature unreachable for them, not merely awkward. *(Added at v2. A bar every invocation model must clear; it does not decide which one ships — see Open questions.)*
   - [ ] The control's touch target is ≥44pt (`design/design-principles.md` §2, Fitts's Law).
   - [ ] The control remains usable and legible at the largest supported Dynamic Type size.
   - [ ] **Every** text label rendered on the surface housing this control meets 4.5:1 against the background it sits on, in **both** light and dark — the numeral, the "now" mark's label, the end-of-track labels, the "next day" flag, and that surface's own section headers included. There is no enumeration exception: a label no design pass happened to list is still covered.
   - [ ] The non-text parts that carry the control's state — the thumb, the boundary between filled and unfilled track, and the "now" mark — meet 3:1 against their adjacent colours in both themes. The inactive track rail is **not** held to 3:1 *while the control is a platform-drawn one rendering it low-contrast by default*; if v2's vertical axis means a custom-drawn control, that exemption's premise is gone and the rail is back inside the bar (`design/design-principles.md` §5, WCAG AA). Whoever writes the new design spec must state which case applies.
   - *Both bullets added at `design-approval` 2026-07-30 (req 6 had no contrast criterion at all, so no gate could fail a design that asserted the bar and missed it — L-009), corrected there once (an enumeration let an unlisted label through; a 3:1 inactive rail was unachievable on the native control), and made surface-neutral at v2.*

7. **Invoked from a screen edge, moved vertically.** *(New at the v2 amendment — founder-direct, 2026-07-31.)*
   - [ ] A swipe inward from the left screen edge brings the control up; a swipe inward from the right screen edge does the same. *(States the instruction as given. The left edge may not survive the OS-gesture question in Open questions — if it resolves to right-edge-only, this bullet changes with it rather than being failed at QA.)*
   - [ ] The hour changes on an up/down drag. A horizontal drag does not change the hour.
   - [ ] One drag direction consistently increases the hour and the other decreases it, and the mapping is identical from both edges. *(Which direction is "later" is the design's call to make and state — it is not in the founder's instruction.)*
   - [ ] Invoking from either edge shows the same hour and writes to the same value — one hour selection exists per session, not one per edge. **[ASSUMPTION]**, see Open questions.
   - [ ] The control can be dismissed and the map returned to its plain state; every dismissal path is enumerated in the design spec and each one preserves the hour (req 4).
   - [ ] The gesture does not fire during ordinary map use: panning or pinching the map from a start point away from the edge never brings the control up.

### Nice-to-have (P1)

- Haptic tick on each hour crossing.
- Absolute clock time alongside the relative offset ("+3h · 21:00").

## Technical design

- **Data model:** none new, and the v2 interaction change adds none — no new table, column, endpoint, or query parameter, and nothing to source or author. The control consumes the `hood_density` hour buckets defined in the map PRD and owns no persisted state; its position is in-memory session state only. Every data need this feature has is already met by a shipped contract (`prds/map-hoods-heat/`).
- **APIs / client-server contract:** all 13 hour buckets are fetched with the map's initial density load, so dragging the slider is a local re-read, not a network round trip. This is what makes the 400ms budget achievable; a per-hour fetch would not.
- **Architecture notes:** the selected hour is a single source of truth held above the map view and read by every hour-bound layer, so a layer added later (live events) subscribes to it rather than owning its own copy. `SALVAGE.md` marks `HeatmapControlsSheet.swift` REFERENCE — extract the hour-windowing model, discard the 1,069-line view; `Models/HeatTimeWindow.swift` is REUSE.
- **Dependencies:** the map PRD (heat area, density contract) must land first. The live-events PRD depends on this control existing.
- **Superseded by v2:** [`TRD.md`](./TRD.md) (`2f955fe`) builds a `ZStack` card opened by a nav-row heat button around a horizontal `Slider(in: 0...12, step: 1)`. Its §2.3 chrome layering, §4.1–4.4 contracts and D4 are all reasoned from that invocation model and don't carry over unexamined. What does carry over: no new data, no fetch on an hour change (what makes 400ms real), `selectedHour` as a plain `Int` on `DensityStore`, the hour-format and contrast work.
- **Open technical questions:** (a) whether "now" re-resolves while the app sits foregrounded across an hour boundary, or only on launch and invocation; (b) how a custom edge gesture coexists with the OS's own — the amendment's largest unknown, see Open questions.

## Open questions & risks

**The three below are open by intent — v2 records them and does not answer them. None gets resolved inside a design or a TRD without the named owner's call.**

1. **Does the edge swipe replace the heat-button invocation, or supplement it?** Unstated — the instruction says where the slider comes from and nothing about the button. **Replaces:** one way in; the heat button loses its only destination. **Supplements:** two entry paths to one value — gesture for speed, button for discoverability and for req 6's accessibility bar. *Product recommends supplement, and does not decide it:* an invisible gesture is undiscoverable and strategy forbids onboarding ("No onboarding. Straight to the map + location permission"), so nothing can teach it. **Aviran's call.** Not the same question as the still-open "separate icons side by side" nav-row ask on `BOARD.md` T-032 — don't fold them together.
2. **The left-edge swipe collides with an OS-reserved gesture.** iOS owns the left edge for interactive back-navigation; bottom and right are claimed too (home indicator, Control Center). A custom edge drag can be shadowed, delayed or swallowed. This may force right-edge-only, an inset activation zone, a deeper drag threshold, or a different mechanism — any of which changes what "from either screen edge" can mean. **`architect` + `ios-developer` weigh in before a design is locked.** Not to be silently designed around or assumed away.
3. **Does "either screen edge" mean one value reachable from both sides, or two sliders?** "12h slider(s)" is ambiguous on its face. **[ASSUMPTION]** one shared hour with a redundant entry point per side — same reading as the founder-direct stub, since nothing else here has two of anything and a second independent hour would contradict req 2. Req 7 is written to that reading and changes if it's wrong. **Aviran's call.**

Also open, smaller:

- **[ASSUMPTION]** The gesture reads as: swipe in, control appears, drag vertically. Whether that is one continuous finger movement or two gestures is unstated, and it decides whether the control persists after the finger lifts — which decides what "dismiss" means in req 7.
- The approved design spec and mockup (`design/phase-1/time-slider-design.md`) describe the superseded model. What is still true — 13 stops, "now" anchor, numeral, contrast tokens, silent-empty, Reduce Motion — should be carried forward, not re-derived.
- The TRD's D4 made req 2's "any open sheet is unchanged" structurally satisfied by ruling out co-presentation. A gesture available over the plain map may reopen that; re-check at the new TRD rather than inheriting the conclusion.
- Synthetic density means every future hour is a simulation, not a forecast (strategy, Key risks). The control will feel precise before the data behind it is. Nothing in V1 tells the user that; worth an explicit call before launch.
- Hour buckets past midnight cross a day boundary — confirm the data model keys on absolute time, not hour-of-day, or +12h from 8pm silently reads the wrong day.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | First PRD pass over the 2026-07-30 V1 lock (PAS-10); slider is the one item strategy marks unchanged |
| 2026-07-30 | Req 6 gains an explicit contrast bullet (4.5:1 text / 3:1 non-text, both themes) | `design-approval` found the design spec asserting that bar and the mockup missing it at 3.22:1 light / 3.61:1 dark on the end-of-track and "now"-tick labels. The PRD had no contrast bullet at all, so no gate — QA included — had anything objective to fail it on. Adds a testable criterion; does not change scope (L-009, applied at design-approval rather than acceptance) |
| 2026-07-30 | That bullet split in two and corrected at the second `design-approval` pass | Two defects in my own criterion, found by re-checking the fixed artifact against it. (1) It enumerated three labels, so `.sheet-eyebrow` — the modal's own "Time" header, 10.5px on `--fg-faint`, 3.22:1 light / 3.61:1 dark — sat outside a bar it plainly belongs inside. Now stated as "every text label in the modal," no enumeration. (2) It held "the track line" to 3:1; the inactive rail computes to 1.29:1 light / 1.28:1 dark and cannot clear 3:1 on the native `Slider` req 6's VoiceOver bullet depends on. WCAG's non-text bar applies to what identifies the component and its state — thumb (3.93:1 / 6.62:1), filled-vs-unfilled boundary (3.05:1 / 5.16:1) and the "now" tick (17.99:1 / 14.57:1), all of which clear it. Rejecting a design against an infeasible criterion would have been rejecting against a stale spec |
| 2026-07-31 | **v2 — swipe in from either screen edge, vertical drag.** Description and reqs 1/3/4/5/6 rewritten off the heat-button/modal + horizontal-drag model; new req 7 (edge invocation, vertical axis, dismissal); new req 1 bullet (13 stops fit one vertical drag at max Dynamic Type); new req 6 bullet (operable without the edge gesture, for VoiceOver/Switch Control); req 6's contrast bullets made surface-neutral, rail exemption re-conditioned on a platform-drawn control | Founder-direct, live `chief-of-staff` chat, 2026-07-31 — verbatim quote in `agent-os/PROGRESS.md`'s FOUNDER-DIRECT STUB that date. The feature, range, 400ms budget and data contract are unchanged; only how a finger reaches and moves it. Strategy's authorizing line re-checked and still covers it — it names the control, not the gesture. Three calls deliberately left open, not answered here (replace-vs-supplement, the iOS left-edge collision, one-slider-vs-two). Supersedes the design spec and `TRD.md` (`2f955fe`) on invocation and manipulation only |
