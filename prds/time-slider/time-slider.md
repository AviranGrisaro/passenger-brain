# Time Slider — now → +12h — PRD

**Status:** Draft v3
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-31
**Scope note:** the feature is unchanged by the 2026-07-30 founders-meeting lock — the one V1 item strategy marks "Unchanged." **v2 and v3 change how the control is reached and moved, not what it does** (founder-direct, 2026-07-31; verbatim quotes in the two FOUNDER-DIRECT STUBs of that date in `agent-os/PROGRESS.md`). v3 corrects v2's gesture model and closes two of its four open calls; the delivered design spec and [`TRD.md`](./TRD.md) (`2f955fe`) turn out **less superseded than v2 assumed**.

## Description

- A single control that moves the whole map forward in time, from now to +12 hours.
- Snaps to whole hours; there is no sub-hour position.
- **Two ways to reach it, not one.** The heat button opens it, exactly as the delivered design has it. Alongside that, a finger touching down on either screen edge and sliding up or down moves the hour directly — one continuous motion, no separate reveal step (founder-direct, 2026-07-31). The edge control is not permanent chrome; it comes with the slide and goes again.
- Every hour-bound layer on the map repaints for the selected hour; the map otherwise stays exactly where it is.
- Resets to "now" on every app launch.
- **Not in scope:** the heat layer's own rendering rules (see the map PRD); the layer toggles sharing that surface — each belongs to the layer it toggles; the rest of the nav row and its other buttons; anything past +12h or before now; scheduling, reminders, or notifications tied to a future hour.

## Motivation

- Strategy, verbatim: "Time slider, now → +12 hours. A place's relevance changes by the hour; the map knows that. Unchanged." A map fixed to "now" answers where to go this second, not where to go after dinner.
- **Re-checked at v2 and v3:** that line names the control and its range, not how a finger reaches it, so it still authorizes the feature after a gesture change. No strategy edit needed, and none was made.
- It is the only V1 control that makes the map a planning tool as well as a live read — [Phase 1](../../strategy/passenger-strategy.md#rollout-sequence) needs both the tourist who just landed and the resident planning tonight.
- The behaviour is already worked out in the old codebase (`SALVAGE.md`: `HeatmapControlsSheet.swift`, REFERENCE) — this PRD exists to pin the contract, not to invent it.

## Requirements

### Must-have (P0)

1. **Range is now → +12 hours, hour-snapped.**
   - [ ] Exactly 13 selectable positions: now, +1h … +12h.
   - [ ] The control cannot be moved past "now" at one end or "+12h" at the other — no wrap, no elastic overshoot past the ends.
   - [ ] Releasing a drag lands on a whole hour, never between two.
   - [ ] All 13 positions are reachable in one continuous edge slide, at the largest supported Dynamic Type size and **wherever on the edge the finger lands** — a slide starting near the bottom or the top of the edge still reaches every stop without lifting. *(Added at v2; widened at v3, since the slide now starts at an arbitrary touch-down point and an hour mapped to absolute screen position would put some out of reach.)*

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
   - [ ] Dismissing the control and reaching it again within one session restores the hour the user left it at — by either edge, and by the heat button.
   - [ ] Opening and closing any other nav surface in between does not reset the hour (`design/ux-flows.md` §2.1, exclusivity rule).
   - [ ] The hour survives every dismissal path the design defines, not only the primary one.

5. **The selected hour is readable as a number, not only as a position.**
   - [ ] A visible numeral or label states the selected hour at all times while the control is on screen.
   - [ ] An explicit "now" mark is drawn on the track as a fixed anchor, at the range end the control treats as "now".
   - [ ] Meaning is never carried by colour alone (`design/design-principles.md` §3).

6. **Accessibility.**
   - [ ] VoiceOver exposes a discrete, announceable step — each step announces the hour it lands on; the control is not continuous-drag-only.
   - [ ] **With VoiceOver or Switch Control on, all 13 hours are selectable without performing the edge slide.** VoiceOver claims the screen's swipe gestures and Switch Control users may not be able to produce an edge drag at all. *(Added at v2; simplified at v3 — the heat-button path is confirmed permanent and satisfies this, so removing that path is what would put the bullet back at risk.)*
   - [ ] The control's touch target is ≥44pt (`design/design-principles.md` §2, Fitts's Law).
   - [ ] The control remains usable and legible at the largest supported Dynamic Type size.
   - [ ] **Every** text label rendered on the surface housing this control meets 4.5:1 against the background it sits on, in **both** light and dark — the numeral, the "now" mark's label, the end-of-track labels, the "next day" flag, and that surface's own section headers included. There is no enumeration exception: a label no design pass happened to list is still covered.
   - [ ] The non-text parts that carry the control's state — the thumb, the boundary between filled and unfilled track, and the "now" mark — meet 3:1 against their adjacent colours in both themes. The inactive track rail is **not** held to 3:1 *while the control is a platform-drawn one rendering it low-contrast by default*; a custom-drawn control loses that exemption and the rail is back inside the bar (`design/design-principles.md` §5, WCAG AA). **The new design spec must state which case applies to each path** — the two paths may not draw the same control (Q5).
   - *Both contrast bullets were added and then corrected at `design-approval` 2026-07-30 — req 6 originally had no contrast criterion at all, so no gate could fail a design that asserted the bar and missed it (L-009). Full history in the Decisions log.*

7. **Reached from either screen edge by one continuous vertical slide.** *(New at v2, gesture model corrected at v3 — founder-direct, 2026-07-31. The "one continuous motion, no reveal step" reading of that correction is inference, not the founder's words — see Open questions, Q4.)*
   - [ ] A finger touching down on a screen edge and sliding up or down changes the hour, and does so from the start of the slide. There is no separate reveal step and no second gesture — one finger down, one slide, the hour tracking it throughout.
   - [ ] The control is on screen for the length of the slide, showing the hour it is currently on (req 5).
   - [ ] Only vertical movement changes the hour; horizontal movement during the slide does not.
   - [ ] One direction consistently means later and the other earlier, identically from both edges. *(Which direction is "later" is the design's call to make and state — it is not in the founder's instruction.)*
   - [ ] The hour under the finger when it lifts is the selected hour, and it holds for the session (req 4). No further gesture is needed to commit it or to clear the control off the map.
   - [ ] Both edges drive one value — the same hour, not one per edge. **[ASSUMPTION]**, see Q3.
   - [ ] The edge slide and the heat button drive that one value too: change the hour by one path, then reach it by the other, and it shows the new hour.
   - [ ] The slide does not fire during ordinary map use — a pan or pinch starting away from the edge never brings the control up.
   - [ ] While any sheet is presented, the edge slide is unavailable and the heat button is how the hour changes. An edge drag over a presented sheet moves the sheet, as it does today. *(Product call made at v3 — see Q6.)*
   - [ ] Which edges are live is stated per device idiom rather than as one global rule: both edges on iPhone; on iPad the right edge is OS-reserved (Slide Over), so the design says what happens there instead of assuming both. *(Replaces the conditional left-edge bullet v2 carried — see Q2.)*

### Nice-to-have (P1)

- Haptic tick on each hour crossing.
- Absolute clock time alongside the relative offset ("+3h · 21:00").

## Technical design

- **Data model:** none new, and neither gesture change adds one — no new table, column, endpoint, or query parameter, and nothing to source or author. The control reads the `hood_density` hour buckets already shipped by `prds/map-hoods-heat/` and owns no persisted state; its position is in-memory session state only.
- **APIs / client-server contract:** all 13 hour buckets are fetched with the map's initial density load, so dragging the slider is a local re-read, not a network round trip. This is what makes the 400ms budget achievable; a per-hour fetch would not.
- **Architecture notes:** the selected hour is a single source of truth held above the map view and read by every hour-bound layer, so a layer added later (live events) subscribes to it rather than owning its own copy. `SALVAGE.md` marks `HeatmapControlsSheet.swift` REFERENCE — extract the hour-windowing model, discard the 1,069-line view; `Models/HeatTimeWindow.swift` is REUSE.
- **Dependencies:** the map PRD (heat area, density contract) must land first. The live-events PRD depends on this control existing.
- **How much of the TRD is superseded — narrowed at v3:** [`TRD.md`](./TRD.md) (`2f955fe`) builds a `ZStack` card opened by a nav-row heat button around a horizontal `Slider(in: 0...12, step: 1)`. With "supplement" confirmed, that card and its invocation are **no longer superseded** — they are the primary path, and the new TRD adds the edge slide beside them. Two parts still need re-examining, both of which assumed the modal was the only way to change the hour: §2.3's chrome layering, and D4's "the heat modal and a system `.sheet` are never co-presented". D4 is what made req 2's "any open sheet is unchanged" satisfied structurally rather than behaviourally; the Q6 call (no edge slide while a sheet is up) keeps that guarantee deliberately rather than by luck, and if Q6 is ever overturned the bullet becomes a behaviour QA has to exercise. Unchanged throughout: no new data, no fetch on an hour change (what makes 400ms real), `selectedHour` as a plain `Int` on `DensityStore`, the hour-format and contrast work.
- **Open technical questions:** (a) whether "now" re-resolves while the app sits foregrounded across an hour boundary, or only on launch and invocation; (b) what a reliable edge strip costs in map surface, now that `architect` has priced the OS-gesture side of it — see Q2.

## Open questions & risks

*Q-numbers are carried over from v2 so `BOARD.md`'s T-032 row and Linear `PAS-15` still resolve against them.*

**Resolved at v3.** Q1 and Q4 are founder-direct, 2026-07-31 — both quotes verbatim from the FOUNDER-DIRECT STUB of that date in `agent-os/PROGRESS.md`, with anything inferred from them marked as inferred. Q6 is a product call and says so.

- **Q1 — replace or supplement the heat-button invocation? — SUPPLEMENT.** Verbatim: **"Supplement (recommended)"** — Aviran accepting the recommendation v2 made. The heat-button/modal path stays exactly as designed; the edge slide is a second way to the same value. Still not the same question as the separately-open "separate icons side by side" nav-row ask on `BOARD.md` T-032 — don't fold them together.
- **Q4 — one continuous gesture, or a reveal then a drag? — one continuous motion.** Verbatim: **"both edges. its not swipe from left to right..you slide the you finder from up to down on one of the edges"**. **The "single continuous motion, no separate reveal step" reading is inference, not his words** — he did not say "one motion" or "no reveal step"; it is read by contrast with the two-step model v2 was written against, and is recorded that way in the stub. Req 7 is written to that reading; if the reading is wrong, req 7's first and fifth bullets are what change.
- **Q6 (new at v3) — is the edge slide available while a sheet is presented? No.** Not a founder answer — a **product call, made here**. `architect`'s read (`f2920fe`) found this is the real gesture collision, not the back-gesture one, and asked `product` for the call rather than invent a workaround: an edge drag over a presented sheet (`HoodStubSheet` ships today, T-033/T-038 add more) drags the sheet. **Call: the gesture is simply unavailable while a sheet is up, and the heat button covers that state.** Because Q1's "supplement" guarantees a working fallback in exactly that state; because a gesture that beat the sheet's own drag would make every edge drag near a sheet ambiguous; and because it keeps the TRD's D4 guarantee behind req 2 intact rather than reopening it. One behaviour, not an architecture — cheap for `designer` or Aviran to overturn.

**Still open — v3 does not answer these. None gets resolved inside a design or a TRD without the named owner's call.**

- **Q2 — which edges are actually available.** The left-edge/back-gesture collision this question was opened for is **answered and closed**: `architect`'s feasibility read (`f2920fe`) found the app has no navigation stack to pop, and a vertical slide is off the system recognizer's left-to-right axis — both edges stay, no right-edge-only fallback. What stays open is what that read surfaced instead: **on iPadOS the *right* edge is the reserved Slide Over gesture** (the app ships iPhone+iPad), so edge availability needs a per-idiom answer; both edges are squeezed top and bottom by Control/Notification Center and the home indicator, against an already-tight vertical track (req 1); and MapKit's gesture-swallowing bug (FB19394663) means an edge strip that reliably beats a map pan permanently claims a band of map near each edge. **`designer` states the per-idiom answer; `architect` prices the claimed band at the new TRD.** Not to be designed around silently.
- **Q3 — does "either screen edge" mean one value from both sides, or two sliders?** "12h slider(s)" is ambiguous on its face, and this was **not** re-confirmed either way when Aviran answered the other two. Nothing contradicts one shared hour with a redundant entry per side, which is why it stays an **[ASSUMPTION]** rather than a confirmation. Req 7 is written to it and changes if it's wrong. **Aviran's call.**
- **Q5 (new at v3) — which axis does the button/modal control use, now that it stays?** *A direct consequence of "supplement".* The founder's correction is about the edge gesture and says nothing about the control the heat button opens; that one may keep its delivered horizontal `Slider` or go vertical to match. **Designer's call, stated explicitly in the new design spec.** It decides whether req 1's reachability bullet binds one path or both, and whether req 6's inactive-rail exemption — premised on a platform-drawn control — survives on the button path.

Also open, smaller:

- The approved design spec and mockup (`design/phase-1/time-slider-design.md`) are **less superseded than v2 assumed**: with the button path confirmed, their modal architecture and exit paths stand. What they lack is the edge slide and the axis call — the new design pass is additive, not a re-do.
- Synthetic density means every future hour is a simulation, not a forecast (strategy, Key risks). The control will feel precise before the data behind it is. Nothing in V1 tells the user that; worth an explicit call before launch.
- Hour buckets past midnight cross a day boundary — confirm the data model keys on absolute time, not hour-of-day, or +12h from 8pm silently reads the wrong day.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | First PRD pass over the 2026-07-30 V1 lock (PAS-10); slider is the one item strategy marks unchanged |
| 2026-07-30 | Req 6 gains an explicit contrast bullet (4.5:1 text / 3:1 non-text, both themes) | `design-approval` found the design spec asserting that bar and the mockup missing it at 3.22:1 light / 3.61:1 dark on the end-of-track and "now"-tick labels. The PRD had no contrast bullet at all, so no gate — QA included — had anything objective to fail it on. Adds a testable criterion; does not change scope (L-009, applied at design-approval rather than acceptance) |
| 2026-07-30 | That bullet split in two and corrected at the second `design-approval` pass | Two defects in my own criterion, found by re-checking the fixed artifact against it. (1) It enumerated three labels, so `.sheet-eyebrow` — the modal's own "Time" header, 10.5px on `--fg-faint`, 3.22:1 light / 3.61:1 dark — sat outside a bar it plainly belongs inside. Now stated as "every text label in the modal," no enumeration. (2) It held "the track line" to 3:1; the inactive rail computes to 1.29:1 light / 1.28:1 dark and cannot clear 3:1 on the native `Slider` req 6's VoiceOver bullet depends on. WCAG's non-text bar applies to what identifies the component and its state — thumb (3.93:1 / 6.62:1), filled-vs-unfilled boundary (3.05:1 / 5.16:1) and the "now" tick (17.99:1 / 14.57:1), all of which clear it. Rejecting a design against an infeasible criterion would have been rejecting against a stale spec |
| 2026-07-31 | **v2 — swipe in from either screen edge, vertical drag.** Description and reqs 1/3/4/5/6 rewritten off the heat-button/modal + horizontal-drag model; new req 7 (edge invocation, vertical axis, dismissal); new req 1 bullet (13 stops fit one vertical drag at max Dynamic Type); new req 6 bullet (operable without the edge gesture, for VoiceOver/Switch Control); req 6's contrast bullets made surface-neutral, rail exemption re-conditioned on a platform-drawn control | Founder-direct, live `chief-of-staff` chat, 2026-07-31 — verbatim quote in `agent-os/PROGRESS.md`'s FOUNDER-DIRECT STUB that date. The feature, range, 400ms budget and data contract are unchanged; only how a finger reaches and moves it. Strategy's authorizing line re-checked and still covers it — it names the control, not the gesture. Three calls deliberately left open, not answered here (replace-vs-supplement, the iOS left-edge collision, one-slider-vs-two). Supersedes the design spec and `TRD.md` (`2f955fe`) on invocation and manipulation only |
| 2026-07-31 | **v3 — gesture model corrected, 2 of the 4 open calls closed.** Req 7 rewritten to one continuous motion (touch down on either edge, slide up/down, the hour moving from the start — no reveal step, no second gesture); req 1's reachability bullet widened to any touch-down point on the edge; req 4 and req 7 gained two-entry-path consistency bullets; req 6's VoiceOver bullet simplified now the button path is permanent; Technical design narrowed what the TRD supersedes; two new questions surfaced, one answered — **Q5** (which axis the button/modal control uses, designer's) and **Q6** (no edge slide while a sheet is presented, product's own call, made here at `architect`'s request) | Founder-direct, live chat, 2026-07-31. "Supplement (recommended)" resolves replace-vs-supplement, so the heat-button path is permanent and v2's premise that the whole design spec was dead is wrong. "both edges. its not swipe from left to right..you slide the you finder from up to down on one of the edges" corrects the two-step gesture v2 was written against. **The "one continuous motion" reading of that quote is `chief-of-staff`'s inference, labelled as such in Open questions rather than presented as his words.** Q3 (one value vs two) stays open and stays **[ASSUMPTION]**, not confirmed — Aviran did not re-confirm it when asked. Q2 was narrowed rather than closed: `architect`'s read (`f2920fe`) landed mid-pass and retired the left-edge/back-gesture worry outright, leaving the iPad right edge, the top/bottom inset squeeze and MapKit's gesture-swallowing bug in its place |
