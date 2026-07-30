# Time Slider — now → +12h — Design Spec

**Task:** T-032 · **PRD:** [`prds/time-slider/time-slider.md`](../../prds/time-slider/time-slider.md) (Draft v1)
**Mockup:** https://claude.ai/code/artifact/a31d3b48-5500-4eab-b962-f0e12d9f0eea — interactive HTML/CSS/JS, click-through, no build step
**Owner:** designer · **Date:** 2026-07-30 · **Status:** ready for `design-approval`
**Consistency check:** builds directly on `design/phase-1/map-hoods-heat-design.md` (T-031, resubmitted-and-approved-pending-Serge state) — does not restate or contradict its rendering rules (stepped bands, no gradients, uniform opacity at every zoom). Reads the T-031 spec's §2 "Density feed client" row and §8 item 2, which flag the exact `selectedHour` seam this task attaches to. Cross-checked against `design/ux-flows.md`'s 2026-07-29/30 nav-model addenda (§1 addendum, §2.1) for where the heat modal lives in the 3-button (search/heat/profile) chrome.
**Design-principles grounding:** built against `design/design-principles.md` throughout, not cited in passing — every control decision below (slider mechanics, discrete-step affordance, modal chrome, its anchor point relative to the persistent nav row) is checked against §2 Universal laws, §3 iOS translation, and §5 Accessibility as the mockup was built, using the `/ui-design-review` checklist directly rather than writing the spec first and back-filling citations. §7 records the specific citation for each call.
**Research note:** Mobbin MCP was not queried this pass — the connector requires a paid plan, unauthorized on this workspace (same gap T-031 hit). Per the standing "don't block" rule, proceeded from the PRD, `map-hoods-heat-design.md`, `ux-flows.md`, and `design-principles.md` instead. Figma was not attempted — the 2026-07-22 founder ruling makes the HTML artifact the default, and this task didn't request Figma output.

---

## 0. Scope discipline

This spec covers exactly the four components the PRD/board hand-off names, no more:

1. **Hour slider control** — 13 hour-snapped positions (now → +12h), a fixed "now" tick, a visible numeral
2. **Heat modal container** — the chrome that houses the slider, opened from the heat button in the 3-button nav row
3. **Selected-hour store** — the single in-memory source of truth every hour-bound layer reads
4. **VoiceOver step behavior** — discrete, announceable steps, not a continuous-drag-only gesture

**Deliberately absent, per the PRD's own "Not in scope" line:** the heat layer's own rendering rules (bands, opacity, zoom behavior — T-031's territory, untouched here); the layer toggles that share the heat modal's chrome (each toggle belongs to the layer it switches — heat's own on/off is T-031's, the live-events toggle is T-034's); anything past +12h or before now; scheduling/reminders tied to a future hour. Where the mockup has to show a toggle row to prove the modal's layout, it renders a locked/stubbed row labeled with its owning task, exactly as T-031's mockup stubbed the Hood sheet.

---

## 1. Flow

**Entry point:** the heat button, one of the 3 side-by-side nav buttons in persistent map chrome (`ux-flows.md` §2, §2.1). There is no other way to reach the slider — it is not permanent map chrome.

```
Heat button tap
  → Heat modal opens as a floating card, anchored just above the persistent nav row
      (not flush to the screen edge — see §2's architecture note on why)
      → Slider shows the hour this session left it at — "now" on a fresh cold launch,
        otherwise wherever the user last set it this session
      → Drag the thumb, tap a point on the track, or step via VoiceOver/keyboard
          → Thumb snaps live to the nearest of 13 whole-hour stops — never rests between two
          → Cannot pass "now" on the left or "+12h" on the right — no wrap, no overshoot
          → Every hour-bound layer on the map repaints for that hour; camera, zoom, and any
            other open sheet are untouched
      → Exit paths, all returning to the plain map with the hour retained:
          → Swipe the card down
          → Tap the dimmed map area behind it (tap-outside)
          → Tap a different nav button (search or profile) — closes this modal and opens
            the other; never stacks (`ux-flows.md` §2.1)
```

**Modal exclusivity + persistence (§2.1's rule, this is where it's built):** only one of {search sheet, heat modal, Profile screen, Places list} is ever open. Switching to a different one closes the heat modal but does **not** reset the selected hour — the hour is session state living above the modal, not state owned by the modal's own lifecycle. Reopening the heat modal later in the same session shows the hour exactly where it was left.

**Cold launch (every app relaunch):** the selected hour re-resolves to "now" against the real clock, regardless of where the previous session left it (PRD req. 3). This does not force the heat modal open — cold launch returns to the plain map, same as any other launch; the slider only shows "now" the next time the modal is opened.

**Exits:** there is no exit *from* the map here — this is a preview/adjustment control, not a hand-off. Swipe-down, tap-outside, and nav-button-switch are the only three ways out, and all three preserve the session's selected hour.

---

## 2. Screens & components

| Component | What it is | SwiftUI-native pattern |
|---|---|---|
| **Heat modal container** | Small floating card holding the slider (+ each layer's own toggle, stubbed here), opened by the heat nav button | **Architecture note, not a system `.sheet()`:** building this as a literal `.sheet(isPresented:)` would present above the *entire* screen, including the persistent nav row underneath — which breaks the direct nav-button-switch requirement in `ux-flows.md` §2.1 (tapping Search or Profile while the heat modal is open must close it and open the other, without the user dismissing first). The mockup proved this out concretely: an early build anchored the card flush to the screen bottom and it visually swallowed the nav row. The fix, carried into this spec: the card is a **custom overlay** in the map's own view hierarchy — a `ZStack` layer above the map content but *below* the nav row's own layer — anchored a fixed distance above the nav row (not `bottom:0` of the screen), sized to its content, sliding in with `.transition(.move(edge: .bottom)).combined(with: .opacity)`. This keeps the nav row reachable and visible at all times, satisfying the exclusivity rule without a dismiss-first step. Flagging this explicitly for `architect` (§8) since it's a real deviation from "just use `.sheet()`," the default assumption a TRD might otherwise reach for. |
| **Hour slider control** | 13 discrete stops: now, +1h … +12h | SwiftUI `Slider(value: Binding<Double>, in: 0...12, step: 1)` bound to the store's `selectedHour`, **not** a freeform continuous slider with rounding applied after the fact — the `step:` parameter is what makes the invalid (off-hour) state structurally impossible rather than corrected post-hoc (Poka-Yoke, §7). A custom `GeometryReader`-driven track overlay adds the fixed "now" tick mark and per-stop hairlines the native `Slider` doesn't render on its own — the native control still owns the drag gesture, value clamping, and accessibility semantics; the overlay is purely decorative on top of it. **Touch target note for `ios-developer`:** the visible thumb graphic can be drawn smaller than 44pt for visual weight (this spec's mockup uses a 28pt dot), but the *tappable/draggable* area — the full `Slider` control's frame — must not be shrunk to match; keep the control's own frame height at ≥44pt regardless of how slim the visible track/thumb render (Fitts's Law, §7). |
| **"Now" tick + numeral** | A fixed visual anchor at the left end of the track, plus a always-visible numeral stating the selected hour | The tick is a distinct **shape** (a short vertical bar, taller than the round per-stop hairlines), not a color difference — so it reads in grayscale and for colorblind users exactly as it does in full color (§3, "never rely on color alone"). The numeral (`Text`, semantic style, tabular-figure rendering for the digit) sits beside the track, updating live on every step; it is the non-positional channel for "how far forward am I looking," since thumb position alone isn't legible enough at a glance for every user (PRD req. 5). |
| **Selected-hour store** | The in-memory `selectedHour` this control writes to and every hour-bound layer reads | This is T-031's `DensityStore.selectedHour` seam, flagged explicitly in that spec's §2 Density feed client row and §8 item 2 — T-032 is the first (and so far only) writer. No new data model: the store already fetched all 13 hour buckets with the map's initial load (PRD's Technical design), so moving the slider is a local re-read against already-cached data, never a network round trip — this is what makes the <400ms repaint budget realistic. The store itself is session-scoped, in-memory only — **never written to `UserDefaults`/`AppStorage` or any other persisted store**, since PRD req. 3 requires "now" to re-resolve against the real clock on every cold launch, not against a cached value from the prior session. A fresh `DensityStore` instance on launch always initializes `selectedHour` to the index representing "now," recomputed against the system clock at that moment — never a stored index carried over. |
| **VoiceOver step behavior** | Every step is discrete and announced; the control is not continuous-drag-only | Because the underlying control is a native `Slider` with `step: 1`, VoiceOver's built-in adjustable action (swipe up/down while focused) already moves exactly one step per gesture and speaks the new value automatically — this is semantic-first (§5: "real `Button`/`Label`/native controls before manual accessibility hacks"), not a custom gesture recognizer reimplementing what the platform already does correctly. The one thing this spec adds on top: `.accessibilityValue()` is overridden to speak the human string ("+3 hours, 9 PM") instead of the raw slider value ("3 of 12"), so the same "now" + absolute-time framing sighted users see is what VoiceOver users hear. Hardware keyboard (external keyboard / Full Keyboard Access) gets the same discrete behavior via arrow-key increments on the focused control, at no extra engineering cost — it's the same `step`-driven semantics, not a second implementation. |
| Layer toggle row (stub, not this task) | Placeholder rows for Heat layer / Live events layer switches | Rendered locked/dimmed in the mockup, labeled with the owning task (T-031 for heat, T-034 for live events) — proving the modal's layout without designing either toggle's behavior. |

---

## 3. Every state

Per `design-principles.md` §4 and the PRD's own P0 requirements 2, 3, 4:

| State | Behavior |
|---|---|
| **Modal closed (default)** | The slider doesn't exist on screen at all — no persistent chrome for it, matching `ux-flows.md`'s "time slider itself isn't on screen at cold open" rule. The map reads whatever hour is currently selected in the store (defaulting to "now"), with zero indication on the map surface of *why* — that's the modal's job when opened, not the map's. |
| **Modal open, at rest** | Numeral, "now" tick, and thumb position all agree with the store's current value. No loading state exists here — all 13 buckets are already in memory (PRD's API contract), so there is nothing to wait for between opening the modal and it being fully interactive. |
| **Mid-drag** | The thumb tracks the pointer live, snapping to the nearest whole-hour stop continuously (not just on release) — this is the Poka-Yoke choice: the control is never observably in an invalid, off-hour state, even transiently, rather than allowing a free-floating position that gets corrected only when the finger lifts. The map's heat layer repaints on every snap-to-a-new-stop, not only on release, so dragging *is* the live preview, matching the PRD's "map repaints for the selected hour" requirement rather than treating drag and commit as separate steps. |
| **Hour has no data (empty)** | This is T-031's rendering rule, inherited unchanged: the affected Hood(s) render with no fill, no error copy, on the map underneath — the modal itself shows nothing different when the selected hour happens to be a gap; the slider has no awareness of "does this hour have data," it only holds a value. (PRD req. 2's silent-empty requirement is satisfied at the rendering layer, not duplicated here.) |
| **Feed unreachable / offline** | Same non-event for the slider: all 13 buckets were fetched once at map load, so being offline afterward doesn't change what the slider can do — dragging still works, still repaints instantly, against whatever was last cached (T-031's offline state owns the "showing cached data" indicator; the slider doesn't add a second one). |
| **Closing via nav-button switch** | Per §2.1's exclusivity rule: the modal closes, but `selectedHour` is untouched — a different nav surface (search sheet, Profile) opens in its place. Reopening the heat modal shows the same hour, not "now." |
| **Cold launch** | `selectedHour` resets to "now," resolved against the real clock at that moment — not a value carried over from the prior session, not the hour the app happened to be showing when last backgrounded (PRD req. 3, and the PRD's own flagged open technical question about foregrounding across an hour boundary — see §8). |

---

## 4. Accessibility notes

- **Discrete, announceable steps (PRD req. 6):** VoiceOver's adjustable action on the native `Slider` speaks each new stop as the user swipes up/down — this is a structural property of using `step: 1` on a real `Slider`, not a bolt-on. The control is never continuous-drag-only for VoiceOver users; every step lands on and announces a whole hour, exactly as it does visually for sighted users.
- **Touch target ≥44pt (Fitts's Law, `design-principles.md` §2):** the `Slider` control's own frame — not just its visible thumb graphic — must stay at or above 44pt tall. This is called out explicitly in §2's Hour slider control row so `ios-developer` doesn't ship a visually-slim 28pt track with a matching 28pt tap area.
- **Never color alone (`design-principles.md` §3):** the "now" tick is a distinct shape (a bar, taller than the ordinary per-hour hairlines), and the selected hour is always readable as a printed numeral — meaning is carried by shape and text, with color as a reinforcing (not sole) channel. This directly satisfies PRD req. 5's "meaning is never carried by color alone."
- **Dynamic Type:** the numeral and the "now"/"+12h" end labels use semantic text styles (not fixed point sizes), tested at the largest accessibility sizes — the track and its tick marks are decorative and don't need to reflow with type size, but the numeral's container must not clip or truncate as it grows.
- **Reduce Motion:** the modal's open/close transition and the thumb's snap-to-stop animation both honor Reduce Motion — cross-fade or resolve near-instantly rather than sliding/animating, consistent with T-031's same commitment for its own cold-open title and location marker.
- **Contrast:** the numeral and end-of-track labels meet 4.5:1 against the modal's surface color (WCAG AA normal text, `design-principles.md` §5); the track line and "now" tick meet the 3:1 large-graphics bar as non-text UI components.

---

## 5. PRD traceability

| PRD requirement | Where this design satisfies it |
|---|---|
| P0-1 13 hour-snapped positions, clamped at both ends, release always lands on a whole hour | §2 Hour slider control row (native `Slider` with `step: 1`, Poka-Yoke framing); §3 Mid-drag state |
| P0-2 Map repaints for the selected hour; camera/zoom/open sheet unchanged; <400ms; silent-empty | §1 Flow; §3 Mid-drag and Empty states; §2 Selected-hour store row (cached buckets = no network round trip, what makes <400ms realistic) |
| P0-3 "Now" is the default every launch, re-resolved against the real clock | §1 Flow's cold-launch branch; §2 Selected-hour store row; §3 Cold launch state |
| P0-4 Session persistence inside the modal; switching nav modals doesn't reset the hour | §1 Flow's modal exclusivity + persistence paragraph; §3 "Closing via nav-button switch" state |
| P0-5 Selected hour readable as a number; explicit "now" tick; never color alone | §2 "Now" tick + numeral row; §4 accessibility notes |
| P0-6 VoiceOver discrete steps; ≥44pt touch target; Dynamic Type at largest sizes | §2 VoiceOver step behavior row; §4 accessibility notes |
| P1 Haptic tick on hour crossing | Demonstrated in the mockup as a visual pulse standing in for haptics (toggle-able); not a P0 commitment |
| P1 Absolute clock time alongside the offset | Demonstrated in the mockup as a toggle-able "+3h · 21:00" format; not a P0 commitment |

---

## 6. Mockup

Interactive HTML/CSS/JS artifact, published as a Claude Artifact: **https://claude.ai/code/artifact/a31d3b48-5500-4eab-b962-f0e12d9f0eea**

What it demonstrates, live:
- The heat modal opening as a floating card anchored above the persistent (search / heat / profile) nav row — proving the nav row stays reachable and visible the entire time the modal is open, which is what makes direct nav-switching possible without a dismiss-first step.
- Dragging or clicking the track — the thumb snaps live to the nearest of 13 whole-hour stops, clamped at "now" and "+12h" with no overshoot; a handful of abstract Hood shapes on the map underneath repaint immediately, with a small "repainted · Nms" indicator nodding at the <400ms budget.
- A fixed "now" tick (a distinct bar shape, not just a color) and a live numeral ("Now" / "+3h") that update together.
- A "VoiceOver preview" toggle that surfaces the exact announced string per step (e.g. *"+3 hours, 00:00. Swipe up or down to adjust, one hour per step."*) — including a deliberate midnight-crossing example, since the demo's reference clock is set so +2h already lands on the next calendar day, visually nodding at the PRD's own flagged day-boundary risk (§8 below) without resolving it.
- Keyboard/adjustable-action stepping (arrow keys on the focused control) as the non-drag equivalent VoiceOver and Full Keyboard Access use.
- Modal exclusivity: switching to the Search or Profile nav button closes the heat modal and opens a labeled stub for that surface (each explicitly marked "owned by T-038 / T-037, placeholder only"); returning to Heat shows the same hour that was left, not "now."
- A "Cold launch" scenario button — resets the selected hour to "now" and closes any open modal, distinct from an ordinary modal close (which preserves the hour).
- A "no data" toggle on one Hood, rendering with no fill and no error copy — the same silent-gap convention T-031 already established, shown here only to prove the slider doesn't interfere with it.
- Reduce Motion, Haptic-tick (P1 preview), Absolute-time (P1 preview), and light/dark theme toggles.

Deliberately **not** in the mockup: the heat layer's own band/opacity rendering logic (T-031's, reused as-is, simplified here into a few illustrative Hood shapes); the actual contents of the layer-toggle rows (stubbed and labeled by owning task); the Search sheet and Profile/Passport screen's real content (stubbed, same convention T-031 used for its Hood-sheet stub).

---

## 7. Principles conformance

Built against `passenger-brain/design/design-principles.md` using the `/ui-design-review` checklist directly while constructing the mockup, not cited after the fact:

| Call this spec makes | Citation |
|---|---|
| The slider's invalid states (off-hour rest position, below "now," above "+12h") are structurally impossible via the control itself (`step: 1`, bounded range), not corrected after an out-of-range drag | `design-principles.md` §2, Poka-Yoke ("constrain at the control... every error message represents a failure to prevent the error") |
| **13 stops on one control does not trigger Hick's Law's "categorize past 7" threshold** — addressed explicitly rather than left silent: Hick's Law governs decision time across a *discrete choice list* (a menu, a set of buttons a user picks between); a bounded, ordered, single-axis slider is a different interaction class where the user is narrowing a continuous-feeling range, not evaluating N independent options each requiring separate consideration. The "now" tick and live numeral keep the *cost of any one stop* near-zero regardless of how many stops exist. Flagging this reasoning explicitly, per the instruction that a Hick's-adjacent number needs a stated call, not a silent pass. | `design-principles.md` §2, Hick's Law (the 7-max-before-categorize threshold, addressed rather than mechanically applied) |
| Slider control's tappable frame stays ≥44pt even though the visible thumb graphic renders smaller | `design-principles.md` §2, Fitts's Law |
| Hour repaint targeted under 400ms, achieved by reading already-cached buckets rather than a per-drag fetch | `design-principles.md` §2, Doherty Threshold |
| "Now" tick differs from ordinary stops by shape, not color; numeral is a second, non-positional channel for the same value | `design-principles.md` §3 iOS translation row ("never rely on color alone... critical for Passenger's map") |
| VoiceOver step behavior comes from the native `Slider`'s built-in adjustable action, not a custom gesture recognizer standing in for it | `design-principles.md` §5 ("semantic first: real controls before manual accessibility hacks") |
| Only one nav-surface modal open at a time; the heat button shows a single active/filled state while its modal is open, nothing else competes for that "currently selected" read | `design-principles.md` §2, Von Restorff (one "special" element per view) |
| Heat modal anchored above the persistent nav row, itself in the bottom third of the screen | `design-principles.md` §3, Thumb Zone |
| Modal open/close transition and thumb snap-animation both honor Reduce Motion | `design-principles.md` §3 (`prefers-reduced-motion` equivalent) |
| Numeral/label contrast 4.5:1; track line and "now" tick 3:1 as non-text UI | `design-principles.md` §5, WCAG AA |
| Nav row + heat modal classified **Sovereign** (dense, learnable, used many times a session), not over-explained for a first-run user | `ux-flows.md` §2.1's explicit framing, itself citing `design-principles.md`'s Sovereign/Transient posture row (§3) |
| Miller's Law | Not applicable — 13 sequential hour-stops on one slider axis aren't a set the user needs to *chunk into groups* to hold in working memory (that's what Miller's Law addresses); there's no list here to chunk. Recorded rather than silently skipped. |

No Section 2/3/5 area relevant to this feature was left unaddressed: Miller's Law is the only row without a live decision to cite against, and that's recorded above rather than silently omitted, matching the standard T-031's spec already set for this section.

---

## 8. Open items handed to `architect` / `ios-developer`

Not blocking `design-approval`, but real enough to flag rather than silently assume:

1. **The heat modal is a custom overlay anchored above the nav row, not a system `.sheet()`.** This is the single real architectural deviation this spec makes from the obvious default — flagged in detail in §2's Heat modal container row, discovered by building and testing the interactive mockup (an early flush-to-bottom version visually broke the direct-nav-switch requirement). `architect` needs to settle the exact construction: a `ZStack`-layered custom view with its own transition versus some other native-primitive combination — but it cannot be a plain `.sheet(isPresented:)` covering the full screen, or the nav row becomes unreachable while the modal is open.
2. **`selectedHour` write-path onto T-031's `DensityStore`.** T-031 already flagged the read-side seam; this spec is the first writer. `architect` should confirm the binding shape (a plain `@Observable var selectedHour: Int` versus something more elaborate) before `ios-developer` builds both T-032 and the eventual T-034 live-events reader against it.
3. **"Now" re-resolution while foregrounded across an hour boundary — inherited directly from the PRD's own open technical question, not resolved here.** If a user opens the modal at 8:59pm and it's still open at 9:01pm, does "now" silently become the old +0h bucket's neighbor, or does the app need to actively re-anchor? This is a real product/technical call the PRD deliberately left open; this spec doesn't invent an answer, consistent with T-031's own precedent of flagging rather than guessing at build-time performance targets.
4. **Day-boundary hour bucket keying — inherited from the PRD's Open questions & risks.** The mockup's demo deliberately sets its reference clock so +2h crosses midnight, to keep this risk visible rather than accidentally hidden by a benign demo clock — but the actual fix (confirm the data model keys on absolute timestamp, not hour-of-day) is `data-engineer`/`architect` territory, not resolved by this design pass.
5. **Native `Slider` vs. fully custom control.** This spec's default is a native `Slider(step:)` plus a decorative tick/numeral overlay, specifically because the native control gives VoiceOver's discrete adjustable-action behavior for free (§2, §7). If `ios-developer` finds the native `Slider`'s visual customization too constrained for the "now" tick or per-stop hairlines, a fully custom control is possible — but it must reimplement the same discrete-step VoiceOver semantics manually rather than losing them, since that's a PRD P0 (req. 6), not a nice-to-have.
