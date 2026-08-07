# Passenger UI/UX Design Principles (shared reference)

**Owner:** shared — used by the `designer` agent (when writing specs) and the `ios-code-reviewer` agent (when reviewing built UI).
**Source:** distilled from the CandleKeep book *"UI/UX Design Principles for AI Agents"* (16 pp, 15 chapters synthesizing Refactoring UI, Don't Make Me Think, Laws of UX, Hooked, Influence, and 5 others). Page citations `(bk pN)` point back to that book.
**Adaptation note:** the source is web/CSS-centric. The *universal laws* below transfer verbatim to any platform. The *iOS translation* column converts CSS-specific rules (px scales, HSL, selectors, viewport) into SwiftUI/HIG equivalents — cite the law, not the CSS mechanism, when applying to Passenger.

How to use this doc: it's a **lookup table, not a read-through**. Jump to the section that matches the decision or the diff in front of you. Thresholds are deliberately concrete so they're checkable — a spec or a PR either meets `< 400ms` or it doesn't.

---

## 1. The precedence rule (settle every trade-off with this first)

**Maslow's Hierarchy for Interfaces:** Functional > Reliable > Usable > Pleasurable, in that order `(bk p9)`. A delightful screen that crashes is worse than a boring one that works. When two principles below conflict, the higher tier wins. For Passenger specifically this means: *the map answers "where is it busy right now" correctly and reliably* before it is beautiful.

**Tesler's Law:** complexity can't be deleted, only moved. Move it from the user to the system — auto-detect, default, compute `(bk p9)`. (Passenger: infer location/time context; don't make the user configure it.)

---

## 2. Universal laws (apply on every platform — designer specs *to* these, reviewer checks *against* them)

| Law | Rule | Concrete threshold | Cite |
|---|---|---|---|
| **Hick's Law** | Decision time grows with number of options | 3–5 choices per decision, 7 max before you must categorize | `bk p9` |
| **Miller's Law** | Working memory is small (corrected from 7±2) | Chunk into **4 ± 1** items | `bk p9` |
| **Doherty Threshold** | Responsiveness is a feature | < 400ms feels instant · spinner past 400ms · progress bar past 1s | `bk p9` |
| **Von Restorff** | One thing stands out | Primary action = unique color **and** ≥1.5× secondary; only **one** "special" element per view | `bk p9` |
| **Goal Gradient / Zeigarnik** | Momentum drives completion | Show progress; pre-fill 10–20% so step one isn't a cliff | `bk p9` |
| **Fitts's Law (targets)** | Big, close targets are faster | ≥44pt touch targets; destructive kept ≥24pt away from constructive | `bk p12` |
| **Satisficing** | Users pick the first *reasonable* option, not the best | Put the recommended choice first and make it visually dominant | `bk p8` |

**Visual hierarchy** `(bk p3)`
- Every element is Primary / Secondary / Tertiary — signalled by **size + weight + color together**, never size alone.
- **Emphasize by de-emphasizing**: soften the competitors instead of inflating the target.
- **Design in greyscale first**; color can hide a broken hierarchy. Add color only after it reads in grey.
- One primary action per view. A 3-tier action hierarchy (filled / tinted / plain).

**Cognitive load & copy** `(bk p8)`
- Omit needless words: cut 50%, then cut 50% again.
- Every screen needs a visible next step — "users don't go backward."

**Persuasion & ethics** `(bk p10–11)`
- **B = MAT** (Fogg): raise **Ability** (reduce friction) before Motivation — cheaper and more durable than persuasion `(bk p10)`.
- The single ethical test: *"Would I be comfortable if my family knew exactly how this works?"* `(bk p11)`. No dark patterns (confirmshaming, roach-motel cancel, fake scarcity, hidden costs) — the book catalogs 13 `(bk p11)`.

**Error prevention over error handling** `(bk p12)`
- **Poka-Yoke**: constrain at the control (picker, slider, stepper) so the bad input is impossible — "every error message represents a failure to prevent the error."
- Validate on blur/commit, not per keystroke. Error copy must **identify + explain + fix**, and blame the system, never the user.
- **Undo over confirmation** for reversible actions (confirmation dialogs breed reflexive "OK"). Reserve confirm for the genuinely irreversible.

---

## 3. iOS / SwiftUI translation (what the web rules become on our platform)

| Book rule (web) | Passenger / SwiftUI equivalent | Cite |
|---|---|---|
| Fixed 12–72px type scale, never `em`, root `100%` | Use **semantic text styles** (`.largeTitle`…`.caption`) + **Dynamic Type**; never hardcode point sizes that don't scale | `bk p4` |
| Body text never < 16px | Respect Dynamic Type; never ship a fixed body font that can't grow. Test at largest accessibility sizes | `bk p4,13` |
| Line length 45–75 chars | Same target for readable text blocks; constrain width on iPad / large text | `bk p4` |
| Author color in HSL, 5–10 shades per role | Define a **semantic color set** in the asset catalog (Primary / Neutral / Accent), each with light+dark variants | `bk p5` |
| Temper contrast (near-black on near-white, not #000/#fff) | Use system label/background colors; they already temper. Don't hardcode pure black/white | `bk p5` |
| Never rely on color alone | Heatmap intensity + friend states need icon/shape/label too — **critical for Passenger's map** and color-blind users | `bk p5,14` |
| 5-level shadow elevation, one light source | Use consistent SwiftUI `.shadow` elevation tiers / materials; don't invent per-view shadows | `bk p6` |
| Thumb Zone = bottom third | Primary map actions belong in the **bottom third** (80%+ of use is one-handed) | `bk p13` |
| Never disable pinch-to-zoom | Never suppress the map's native zoom/gestures | `bk p13` |
| `active:scale(0.96)`, ~100ms | Press feedback via scale/opacity, ~100ms, never below 0.95 | `bk p7` |
| Respect `prefers-reduced-motion` | Honor **Reduce Motion**; never animate unconditionally | `bk p14` |
| Placeholder-as-label is banned | Never use a `TextField` placeholder as the only label — breaks VoiceOver + disappears on input | `bk p12` |
| Posture: Sovereign vs Transient vs Daemonic | The map is **Sovereign** (max density, learnable); permission/paywall sheets are **Transient** (big controls, zero learning curve) | `bk p13` |

---

## 4. State & empty-screen completeness `(bk p6)`
Never neglect a state. Every screen specs/handles: **loading, empty, error, permission-denied, offline.** Empty states are illustration + one-line description + a CTA — not a blank view. (This is already Passenger house rule; the book is the *why*.)

---

## 5. Accessibility — scope, not polish `(bk p14)`
Affects 15–20% of users directly.
- Contrast: **4.5:1** normal text, **3:1** large text / UI components (WCAG AA).
- Semantic first: real `Button`/`Label`/headings before manual accessibility hacks (SwiftUI's analog to "semantic HTML before ARIA").
- VoiceOver labels on **every map annotation** and control; nothing interactive left unlabeled.
- Highly visible focus/selection states; honor Reduce Motion.
- **Audit by component, not by principle**: one finding per broken component (a filed ticket / PR comment), not fragmented per-WCAG-rule notes that lead to over-patched code.

---

## 6. Presentation exclusivity — never stack two modal surfaces

**Rule:** A system `.sheet`, a custom overlay "card" (e.g. a `ZStack`-based list/detail overlay), an `.alert`, or any other surface that claims the user's full attention never ends up co-presented with another **independently-reachable** one by accident. Opening a new top-level surface always **replaces or dismisses** whatever other top-level surface was presented — never adds to it. Two modal-like surfaces stacked simultaneously reads as a broken transition, not a broken feature, so it can pass a casual look while still being wrong — see the carve-out immediately below for the one shape that's exempt.

**Carve-out — a modal opened *from within* a surface it doesn't need to dismiss is not a violation.** If surface B is opened by an action on surface A (e.g. tapping a row inside an open list), and A stays presented underneath, and dismissing B simply reveals A unchanged, that is not two independent surfaces competing for the user's attention — it's a parent/child pair with one entry point and one exit, which reads as a single coherent transition rather than a broken one. What this rule actually forbids is two surfaces that are each independently reachable/dismissable ending up live at the same time by accident (an orphaned sheet nothing closes, or a wrong-order open that buries one surface under another). See `prds/places-been-saved/TRD.md` §4.6's `router.placeDepth == 1` derivation: T-036's `DetailRouter` place sheet, opened by a row tap inside the open Places-list `NavSurface`, is designed to render *above* the still-presented list — "the modal renders above the list; dismissing it reveals the list unchanged" (§4.6) — and that is the carve-out case, not a D8 breach.

**Corrected 2026-08-03 — this section previously cited `PAS-36` as an evidencing violation; that diagnosis didn't hold up.** `PAS-36` reported exactly the shipped-as-designed state above (list visible behind an open place-detail sheet, opened via a row tap) and was filed as a bug on the assumption that any two-surfaces-visible-at-once state is automatically a D8 breach. Re-reading T-036's TRD directly shows §4.6 designs for precisely that state on purpose — it isn't an accidental orphan, since leaving `.places` by any other path (`router.closePlace()`) still tears the sheet down structurally. **No other confirmed evidencing example exists in this codebase as of this correction.** The general rule below is kept anyway — it's still sound guidance, independently supported by T-036 D8's own reasoning about *unintended* co-presentation (an opened-then-abandoned sheet, or opening one surface without closing another first) — but a future edit that adds a real evidencing example should replace this note rather than stack alongside it.

**The reusable mechanism — this codebase already has it, use it rather than re-deriving:**
- `DetailRouter` — one system `.sheet` modifier whose content switches between Hood / place / event, never multiple independent `.sheet` calls competing to be on top.
- `MapChromeState`'s `NavSurface` — a single `presented: NavSurface?`; `toggle()` swaps that one value rather than layering a second surface over the first.
- T-036's TRD (`prds/places-been-saved/TRD.md`) already named the specific case as **D8**: "a `NavSurface` and a system sheet are never co-presented in either direction" — meaning never *orphaned* co-presence (opening one without closing the other first, or leaving one without tearing the other down), not "never simultaneously on screen at all." A parent-opened, depth-1 child sheet is exempt by the carve-out above. This entry generalizes D8's *unintended*-co-presentation reasoning from a one-off TRD decision into a standing rule for every future screen: the answer to "what's on screen right now, independent of anything opened from inside it" must live in exactly one place.

**Checkable at spec/review time:** any screen with more than one *independently* presentable surface (i.e. not a parent/child pair covered by the carve-out) needs exactly one piece of state answering "what's currently presented" — an enum/optional with mutually-exclusive setters, not N independent booleans or overlays that can each be true at once. If a screen can't name that single source of truth, it can stack. Before filing a stacked-surfaces finding, check whether the second surface was opened from within the first (carve-out — not a finding) or independently of it (a real D8-class breach).

---

## 8. Modal shape — full-width, bottom-anchored, one shared treatment

**Rule (Aviran-direct, 2026-08-07, T-079/`PAS-73`):** every modal-like surface in the app — system `.sheet()` and custom `ZStack` overlay alike — renders full device width (no horizontal inset) and flush to the bottom edge (no gap, no floating), with rounded corners on the **top two corners only**. Never centered, never inset on all sides, never floating above the screen edge with all-four-corner rounding.

**Why this is one rule and not per-surface taste:** a system `.sheet()` already does this by default (full width, bottom-anchored, top-corners-only) — that's the platform convention, not a custom design. Any custom `ZStack`-based overlay built instead of a system sheet (typically because a sheet would cover chrome that needs to stay hit-testable, e.g. Passenger's nav row) must still match that same shape by construction: no `.padding(.horizontal, ...)` on the card, no bottom padding pulling it off the true edge, `UnevenRoundedRectangle`/a top-corners-only clip rather than a uniform `RoundedRectangle`. See `design/phase-1/modal-shape-standard.md` for the full derivation and the specific fix applied to Passenger's 4 custom-overlay surfaces (`PlacesListOverlay`, `PassportSurface`, `SearchOverlay`, `HeatModalCard`) versus its 3 already-correct system sheets (`EventDetailModal`, `PlaceDetailModal`, `HoodSheet`).

**Checkable at spec/review time:** any new modal-like surface's background modifier gets checked for (a) no horizontal padding/inset on the card itself, (b) no bottom padding pulling it off the safe-area edge, (c) corner radius applied only to the top two corners. A surface that fails any of the three needs a stated reason (e.g. a deliberate non-modal floating chip, which isn't a "modal" under this rule at all) or it's a finding.

---

## 9. Agent-specific usage

**Designer** — spec *to* these thresholds. When you write a spec's components/states/accessibility sections, the numeric targets above (targets, contrast, Doherty timings, Hick option counts, thumb-zone placement) are the defaults you design against. Cite this doc rather than re-deriving.

**iOS code reviewer** — add a **UX/HIG conformance pass** using §2, §3, §5, §6, §8 as the checklist: color-only signalling on the map, missing state handling, placeholder-as-label, targets < 44pt, fixed non-scaling type, response paths that block the main thread past the Doherty budget, unlabeled annotations, (§6) any screen that can present two modal-like surfaces at once — check for a single "what's presented" state rather than independent flags/overlays — and (§8) any modal-like surface inset from the screen edges or rounded on all four corners instead of matching the full-width/bottom-anchored/top-corners-only standard. File findings **by component** (§5). These are `APPROVE with minors` unless they cause an accessibility failure or a functional/reliability break (§1), which escalates per the Maslow precedence — a §6 stacked-modal finding or a §8 shape finding that breaks nav-row hit-testability is a functional break, so it escalates past minor.

---

*Derived from CandleKeep: "UI/UX Design Principles for AI Agents." Full chapter set: hierarchy (p3), typography (p4), color (p5), spacing/depth (p6), components (p7), navigation/IA (p8), cognitive load (p9), behavioral triggers (p10), persuasion/trust (p11), forms (p12), responsive (p13), accessibility (p14), anti-patterns (p15).*
