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

## 6. Agent-specific usage

**Designer** — spec *to* these thresholds. When you write a spec's components/states/accessibility sections, the numeric targets above (targets, contrast, Doherty timings, Hick option counts, thumb-zone placement) are the defaults you design against. Cite this doc rather than re-deriving.

**iOS code reviewer** — add a **UX/HIG conformance pass** using §2, §3, §5 as the checklist: color-only signalling on the map, missing state handling, placeholder-as-label, targets < 44pt, fixed non-scaling type, response paths that block the main thread past the Doherty budget, unlabeled annotations. File findings **by component** (§5). These are `APPROVE with minors` unless they cause an accessibility failure or a functional/reliability break (§1), which escalates per the Maslow precedence.

---

*Derived from CandleKeep: "UI/UX Design Principles for AI Agents." Full chapter set: hierarchy (p3), typography (p4), color (p5), spacing/depth (p6), components (p7), navigation/IA (p8), cognitive load (p9), behavioral triggers (p10), persuasion/trust (p11), forms (p12), responsive (p13), accessibility (p14), anti-patterns (p15).*
