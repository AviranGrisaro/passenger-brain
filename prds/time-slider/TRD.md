# Time Slider — now → +12h — TRD

**Task:** T-032 · **Linear:** `PAS-15` · **Status:** ready for `trd-review`
**Owner:** architect · **Date:** 2026-07-30
**PRD:** [`time-slider.md`](./time-slider.md) (Draft v1) · **Design spec:** [`design/phase-1/time-slider-design.md`](../../design/phase-1/time-slider-design.md) (`design-approval` PASS after one REJECT/fix cycle; `design-review` cleared on Aviran's approval, 2026-07-30)
**Mockup:** https://claude.ai/code/artifact/a31d3b48-5500-4eab-b962-f0e12d9f0eea — reference only. Where this TRD and the mockup disagree, this TRD wins (§8 D1–D4).
**Builds on:** [`prds/map-hoods-heat/TRD.md`](../map-hoods-heat/TRD.md) (T-031, shipped and accepted). This TRD extends that module layout; it does not restate it.

---

## 1. Context

Read the PRD and the design spec first — nothing here restates them. This document decides what they left open and pins the contracts `ios-developer` builds against.

**Surface: iOS-only. Confirmed, not assumed.** Checked against the design spec §0/§2 and the PRD's Technical design: no new table, no new column, no new endpoint, no change to any existing one. T-031's `DensityAPI` already fetches the full `[anchorHour, anchorHour + 12h]` window in one request (`DensityAPI.fetchDensity(from:)`, `hour_bucket=gte./lte.`), and `hood_density` already keys on absolute UTC hour. Everything this feature needs from the backend is already in the shipped contract. **No `[Backend]` and no `[Algo/Data]` step exists in §11.**

**What this feature is, architecturally:** the app's first piece of *chrome above the map*. T-031 built one screen with four floating overlays and one system sheet. T-032 introduces the persistent nav row, the modal layer that hangs off it, and the layering rule that decides what covers what. That layering — not the slider — is the part with real consequences, because T-034/T-036/T-037/T-038 all land in the same bottom band.

**Open items resolved here:**

| # | Open item | Source | Call | Where |
|---|---|---|---|---|
| 1 | Heat modal construction — not a `.sheet()` | design §8.1 | `ZStack` overlay inside `MapScreen`, below the nav row's layer, above the map and its scrim | §2.3, §4.2, D2 |
| 2 | `selectedHour` write-path / binding shape | design §8.2 | Already settled by T-031 §4.4 — plain `var selectedHour: Int` on `@Observable DensityStore`. Confirmed against the shipped file; **not redesigned.** A `Double` bridge lives in `HourSlider`, not in the store | §4.3 |
| 3 | "Now" re-resolving while foregrounded across an hour boundary | PRD Open technical questions; design §8.3 | Re-anchor on modal **open** (in addition to T-031's existing `scenePhase → .active` hook). No timer | §4.5, D3 |
| 4 | Day-boundary bucket keying | PRD risks; design §8.4 | **Already resolved by T-031 §3.1** — `hour_bucket` is an absolute UTC timestamp, and `DensityStore` keys on epoch-hour. Closed, not re-flagged. The "next day" pill is display-only on top of it | §3.2 |
| 5 | Native `Slider` vs. fully custom control | design §8.5 | **Native `Slider(value:in:step:)`.** The custom overlay is decorative and non-interactive | §4.4, §8 D5 |
| 6 | Which nav-row buttons exist in this build | not raised by any doc — found by reading the shipped code | The nav row does not exist yet. T-032 builds the container plus **the heat button only** | §2.3, D1 |
| 7 | Verifying "repaints on hour change" and "<400ms" | `product`'s T-031 acceptance carry-forward | Both get an executable hook built in this task, named in §9 | §4.7, §9 |

---

## 2. Architecture

### 2.1 Module layout — additions to T-031's tree

```
Passenger/
  Map/
    MapScreen.swift            MODIFIED — hosts the chrome ZStack; near-me moves (D1)
    MapChromeState.swift       new — NavSurface + the one-modal-at-a-time rule
    MapNavRow.swift            new — persistent nav row; heat button only in this task
  HeatModal/
    HeatModalCard.swift        new — the overlay card: scrim, transitions, dismissals
    HourSlider.swift           new — native Slider + decorative tick overlay + a11y
    HourReadout.swift          new — numeral + "next day" pill
    HourFormat.swift           new — pure offset → (numeral, clock time, isNextDay)
  Density/
    DensityStore.swift         MODIFIED — one narrow guard in refreshIfHourRolled() (§4.5)
    HeatComposition.swift      new — pure hoods × hour → [HoodFill] (§4.7)
  Support/
    HeatRepaintSignpost.swift  new — the HourRepaint interval (§4.7)
Assets.xcassets/
  MutedOnSurface.colorset      new · PillSurface.colorset new · SliderFill.colorset new · NowTick.colorset new
```

Xcode synchronized file groups are on — dropping files in the folder is enough, no `project.pbxproj` edit.

### 2.2 Boundaries — who is allowed to know what

- **`HeatModal/` knows no map, no geometry, no network.** It reads and writes one `Int` and formats a date. `HourFormat` is pure and takes its calendar and its clock as parameters, so every label string is unit-testable with no simulator and no fixed timezone.
- **`MapChromeState` knows no view.** It holds "which nav surface is presented" and nothing else. It does not own `selectedHour` — that is the whole point of PRD req 4 (§4.1).
- **`Density/` still knows no geometry.** `HeatComposition` is the one new type that pairs a Hood with a band, and it lives on the composition seam T-031 already put in `Map/` — it takes a lookup closure, never a `DensityStore`, so it is testable without one.
- **`Map/` remains the only layer that knows both** and the only layer that knows the z-order.

### 2.3 The chrome layering rule (the real content of this TRD)

`MapScreen`'s body becomes an explicit `ZStack`, top of list = furthest back:

| z | Layer | Behaviour when a nav surface is presented |
|---|---|---|
| 0 | `Map` + `HoodLayer` + `UserAnnotation`, `ColdOpenTitle`, `CachedDataIndicator` | Unchanged. Title/indicator sit at the top of the screen, outside the modal's footprint. |
| 1 | **Scrim** — `Color.black.opacity(…)`, `.contentShape(Rectangle())`, tap → dismiss | Present only while a surface is presented. This is what makes tap-outside work and what prevents a map tap from opening a Hood sheet underneath an open modal. |
| 2 | **Bucket-2 chrome** — the near-me cluster (`NearMeButton` + `SettingsHint`) | `.opacity(0)` + `.allowsHitTesting(false)` while presented, per `ux-flows.md` §2.1's stacking rule, bucket (2). Reduce Motion honoured. |
| 3 | **Modal card** — `HeatModalCard`, `.transition(.move(edge: .bottom).combined(with: .opacity))` | The presented surface's content. Anchored a fixed distance above the nav row, sized to content — never `bottom: 0`. |
| 4 | **`MapNavRow`** | Always visible, always hit-testable, never covered. This is what makes direct nav-switching work without a dismiss-first step (`ux-flows.md` §2.1, bucket (1)). |

Two consequences worth stating rather than discovering:

- **`.presentationBackgroundInteraction` is not involved here and must not be reached for.** That modifier is T-033's mechanism for system sheets. This is a custom overlay in the app's own hierarchy; the scrim at z1 is the equivalent mechanism, and the map is deliberately *not* interactive while the modal is open (design §1 makes tap-outside an exit path, which requires the scrim to receive the tap).
- **The heat modal and a system `.sheet` are never co-presented** — see D4. A `.sheet` presents above the entire hierarchy including z4, so a Hood sheet covers the nav row and the heat button while it is up; and while the modal is up, the scrim blocks the map taps that would open a sheet. Mutually exclusive by construction, in both directions.

**The near-me cluster moves.** T-031 anchors it at `.bottom` with 32pt padding — the band the nav row now occupies. It moves above the nav row, per the mockup's own arrangement. This is a change to accepted, shipped T-031 layout; it is named here rather than left as an implementation surprise (D1).

---

## 3. Data model

### 3.1 No new persisted state, on either side

The slider owns nothing. `selectedHour` is a plain `Int` on `DensityStore`, in memory, session-scoped, **never written to `UserDefaults`/`AppStorage`/disk** — PRD req 3's cold-launch reset is a property of where the value lives, not of a reset routine that could be forgotten. `DensityCache` persists density rows only; it has never held an hour selection and must not gain one. `MapChromeState` is likewise in-memory and resets on launch.

No migration, no schema change, no new query parameter. Nothing in this feature carries a location, a device id, or a user id — the request surface is untouched, so T-031 §3.3's "location cannot leak through a query that never had a place to put it" holds unchanged.

### 3.2 Time — how an offset becomes a label

`anchorHour` (UTC hour floor, T-031) + `offset × 3600s` = the selected absolute instant. Everything the user reads is derived from that instant in the **current** calendar and timezone:

- numeral: `"Now"` for offset 0, `"+\(offset)h"` otherwise — offset is the primary channel, never a bare clock time
- clock time (`"21:00"`, PRD P1): `DateFormatter`/`Date.FormatStyle` in `.current` timezone
- `isNextDay`: `!Calendar.current.isDate(selectedInstant, inSameDayAs: now)`, compared against the real clock, not against `anchorHour`

**[ASSUMPTION]** every supported timezone is a whole-hour offset from UTC, so a UTC hour floor lands on a local hour boundary and "+3h" reads as a clean o'clock. True for Tel Aviv (UTC+2/+3) and for V1's only city; false in e.g. India (+5:30). The failure mode is cosmetic — the P1 clock label would read `20:30` — and it does not affect bucket lookup, which never leaves epoch-hour arithmetic. Recorded in §10 rather than engineered around for a city V1 does not ship in.

---

## 4. Contracts

All of §4 is `[iOS]`. There is no second build surface to hand a contract to.

### 4.1 Nav-surface state

```swift
enum NavSurface: String, CaseIterable, Sendable, Identifiable {
    case search, heat, places, profile
    var id: String { rawValue }
}

@MainActor @Observable
final class MapChromeState {
    private(set) var presented: NavSurface?
    var isPresenting: Bool { presented != nil }

    /// Exclusivity (`ux-flows.md` §2.1): presenting a surface replaces whatever
    /// was open — it never stacks. Presenting the already-open surface closes it.
    func toggle(_ surface: NavSurface)
    func dismiss()
}
```

Four cases, one view. That is deliberate and it is the narrowest thing that makes PRD req 4 testable: "switching to a different nav modal and back does not reset the hour" cannot be exercised at this task's own `qa` if the type can only express one surface. The four-member set is not invented here — `ux-flows.md` §2.1 locks it ("only one of {search sheet, heat modal, Places list, Profile tab} is ever open"). A case with no view costs nothing, ships nothing, and stops T-036/T-037/T-038 from each inventing a private boolean and quietly breaking exclusivity. **This is a state type mirroring a locked spec, not a hook for an unbuilt feature** — `ios-code-reviewer` should read it as such, and should reject any *view* work for the other three cases in this task's diff.

`toggle` closing the already-open surface is an architect call filling a gap: the design spec lists three exits (swipe-down, tap-outside, nav-switch) and does not say what a second tap on the lit heat button does. Doing nothing there reads as broken. Flagged for `designer` to overturn cheaply if wrong — it is one method.

### 4.2 The modal card

```swift
struct HeatModalCard: View {
    let onDismiss: () -> Void
    // content: section header + HourReadout + HourSlider. Nothing else in V1 (D4).
}
```

- Background: opaque `Color("Surface")` (T-031's existing token), rounded, sized to content. **Not `.ultraThinMaterial`** — the same reasoning T-031 §8 D1 settled: a contrast ratio against a translucent layer over a live map is not a number anyone can verify, and PRD req 6 demands a verifiable one.
- Dismissals: (a) drag handle + `DragGesture`, dismiss past a threshold with a velocity/distance rule; (b) scrim tap; (c) `MapNavRow` tapping another surface. All three route to `MapChromeState`, none to a private `@State` bool.
- Transition `.move(edge: .bottom).combined(with: .opacity)`; under `\.accessibilityReduceMotion` it cross-fades with no movement.
- **`HeatModalCard` composes rows, not a bare slider.** T-034's live-events toggle lands as a second row. That is a layout fact about the card, not a hook: no toggle, no placeholder, and no "always on" stub row ships in this task (D4).

### 4.3 The binding — T-031's seam, unchanged

```swift
// In HourSlider, not in the store:
Slider(
    value: Binding(
        get: { Double(selectedHour) },
        set: { selectedHour = Int($0.rounded()) }
    ),
    in: 0...12,
    step: 1
)
```

`selectedHour` stays `var selectedHour: Int` on `@Observable DensityStore` — verified against the shipped `Density/DensityStore.swift`, exactly as T-031 §4.4 promised T-032 it would be. **No wrapper type, no publisher, no `@Binding` chain through three views:** `MapScreen` passes `Binding(get:set:)` onto the store's property, one hop. The `Double` bridge is an artifact of `Slider`'s API and is confined to the one file that owns the control.

Range clamping and hour snapping are structural — `in: 0...12, step: 1` makes an off-hour or out-of-range value unrepresentable, satisfying PRD req 1's three bullets without a rounding pass anywhere else. `ios-code-reviewer` should treat a hand-rolled clamp/round outside this binding as a finding: it means the invariant moved out of the type and into a routine someone can forget.

### 4.4 The slider view

```swift
struct HourSlider: View {
    @Binding var selectedHour: Int    // 0...12
    let readout: HourFormat.Readout
}
```

- `.frame(minHeight: 44)` on the control itself, regardless of how slim the drawn track is (design §2, §4; Fitts's Law). The visible thumb may render smaller.
- The tick/hairline overlay is drawn in a `GeometryReader` **with `.allowsHitTesting(false)`** — it must never intercept the drag, or the native gesture and the VoiceOver adjustable action both degrade.
- `.tint(Color("SliderFill"))`, `.accessibilityLabel("Map hour")`, `.accessibilityValue(HourFormat.voiceOverValue(readout))`, `.accessibilityIdentifier("hourSlider")`. The identifier is not cosmetic — §9's UI test drives the control through `XCUIElement.adjust(toNormalizedSliderPosition:)` and needs it.
- VoiceOver's discrete stepping comes from `step: 1` on a real `Slider` and is not reimplemented (design §2, §7).

```swift
enum HourFormat {
    struct Readout: Equatable, Sendable {
        let offsetLabel: String    // "Now", "+1h" … "+12h"
        let clockLabel: String     // "21:00" — P1 surface, always computed
        let isNextDay: Bool
    }
    static func readout(offset: Int, anchorHour: Date, now: Date, calendar: Calendar) -> Readout
    static func voiceOverValue(_ readout: Readout) -> String   // "+3 hours, 21:00, next day"
}
```

Pure, injectable clock and calendar. Its unit tests must include a midnight crossing and an offset of 0 and 12.

### 4.5 The one change to T-031's store

Two lines, both in `DensityStore.refreshIfHourRolled()`, plus one new call site:

1. **New call site:** `MapScreen` calls `refreshIfHourRolled()` when the heat modal opens, in addition to T-031's existing `scenePhase → .active` hook. This is the resolution of the PRD's own open technical question (D3). The method already early-returns when the hour has not rolled, so the common case costs a comparison.
2. **New guard:** the method reads `selectedHour` before an `await` and writes a remapped value after it. If the user moved the slider during that await, the write clobbers their input. Capture `selectedHour` before the await and apply the remap **only if it is unchanged**; otherwise leave the user's value alone.

This touches code that already passed `code-review`, `qa` and `acceptance` under T-031. It is named here rather than slipped in, it is scoped to one method, and `ios-code-reviewer` should confirm T-031's existing `DensityStoreTests` still pass unmodified alongside the new case.

### 4.6 Colour tokens and the contrast rule

PRD req 6 says "**every** text label rendered inside the heat modal… There is no enumeration exception." A test cannot enumerate labels that do not exist yet. So the invariant is moved into the construction:

> **Every text label inside the heat modal renders with exactly one foreground token, `MutedOnSurface`, on exactly one of two backgrounds: `Surface` or `PillSurface`.** Hierarchy inside the card comes from type size and weight, never from a second colour.

That turns an unenumerable claim into four executable assertions ({token} × {2 backgrounds} × {light, dark} ≥ 4.5:1), and any future label added to this card is covered the day it is written. `ios-code-reviewer` treats a second foreground colour inside `HeatModal/` as a blocking finding.

- **`PillSurface` is an opaque colour set, not the mockup's `color-mix(--heat 14%, transparent)`.** Same reasoning as T-031 §8 D1: a translucent background has no verifiable ratio. The token is the pre-flattened equivalent (D3 in the design spec's own numbers: ~5.09:1 light / ~6.01:1 dark).
- **Non-text (3:1):** assert `NowTick` vs `Surface` and `SliderFill` vs `Surface`. Both are drawn by this app.
- **Explicitly not asserted:** the native `Slider`'s thumb and its inactive rail. The PRD already exempts the rail; the thumb is the same category — an unmodified platform-drawn part, which is where WCAG 1.4.11's author-modification boundary falls. Going custom to control those pixels would cost the discrete VoiceOver adjustable action that PRD req 6 depends on (design §8.5). **The test must not be "helpfully" extended to those two pairs** — it would fail against a control the PRD requires.
- Tokens are new colour sets, not literals lifted from the mockup, and `SliderFill` is deliberately **not** `HeatFill`: reusing the heat hue would couple the slider's contrast tuning to the heat palette T-031 req 4 locks.

Test lives beside T-031's, reusing `Support/ContrastRatio.swift` and the same resolve-against-the-real-catalog pattern (`UIColor(named:in:compatibleWith:)` under both `UIUserInterfaceStyle`s) — never hardcoded hex.

### 4.7 Repaint composition and its measurement

```swift
struct HoodFill: Equatable, Sendable { let hood: Hood; let band: HeatBand? }

enum HeatComposition {
    /// Pure. Takes a lookup closure, not a store — testable with no DensityStore,
    /// no network, no simulator.
    static func fills(hoods: [Hood], hour: Int, band: (String, Int) -> HeatBand?) -> [HoodFill]
}
```

`MapScreen`'s body resolves fills **once per pass** through this function and iterates the result, instead of calling `densityStore.band(...)` inline per Hood. Two reasons, both load-bearing: it gives the repaint a single, nameable completion point, and it gives §9 a pure function to measure.

```swift
enum HeatRepaintSignpost {   // mirrors Support/ColdOpenSignpost.swift exactly
    // interval name "HourRepaint", category "HeatRepaint"
    @MainActor static func begin()        // from the slider binding's setter, only on a real change
    @MainActor static func endIfPending() // immediately after HeatComposition.fills(...) returns
}
```

**Honest scope of the measurement, stated the way T-031 stated its cold-open one:** `HourRepaint` brackets *"`selectedHour` written → every Hood's band resolved for the new hour."* It excludes MapKit's own frame commit, which app code cannot observe. The <400ms budget is held structurally first — T-031 §4.4's contract that **no code path fetches on an hour change** is what makes it real — and measured second. `qa` additionally confirms perceptually that dragging produces no lag, no spinner, and no intermediate state.

---

## 5. Flow

```
Heat button tap
  → MapChromeState.toggle(.heat)
      → refreshIfHourRolled()            re-anchor if the wall clock rolled (§4.5)
      → scrim fades in; near-me cluster fades out; nav row stays lit and hit-testable
      → HeatModalCard slides in above the nav row, showing this session's hour
  → drag / tap track / VoiceOver swipe / arrow key
      → Slider(step: 1) writes selectedHour  ── the only writer
          → HeatRepaintSignpost.begin()
          → @Observable invalidation → MapScreen body
              → HeatComposition.fills(hoods:hour:band:) → HeatRepaintSignpost.endIfPending()
              → HoodLayer re-evaluates foregroundStyle per polygon
          → HourReadout numeral + "next day" pill update from the same value
      camera, zoom, geometry, polygon identity: untouched. No fetch. No sheet involved (D4).
  → exit: swipe down · scrim tap · another nav button
      → MapChromeState mutates; selectedHour untouched (PRD req 4)
```

Cold launch: `DensityStore()` initialises `selectedHour = 0` and `anchorHour` from the real clock. Nothing is read from disk, so "now" cannot be stale (PRD req 3).

Empty / offline hours are a non-event for the slider: `band(for:hour:)` returns `nil`, `HoodLayer` applies no fill, and no banner or modal appears anywhere. That is T-031's rendering rule, inherited, not re-implemented (design §3).

---

## 6. Third-party / dependencies

**None added.** No package, no account, no cost, nothing Aviran-gated. `Slider`, `GeometryReader`, `os_signpost`, and `Calendar` are all platform. This keeps `passenger-code/README.md`'s "no third-party packages until a TRD justifies one" intact.

**Salvage:** `SALVAGE.md` marks `Models/HeatTimeWindow.swift` REUSE and `Features/Map/HeatmapControlsSheet.swift` REFERENCE (1,069 lines — "extract the model, not the view"). The archive is **not reachable from this workspace** (`~/APE Studio/locali` is absent here; same access gap T-031 hit for `ContrastRatio.swift`). It is also largely moot: the hour-windowing model REUSE points at is already re-derived and shipped in `DensityStore` (`anchorHour` + `0...12` offset over absolute UTC hours), which is a stricter design than an hour-of-day window. `ios-developer` should not block on salvage access; whoever can reach the archive may diff `HeatTimeWindow` against §3.2 afterwards.

---

## 7. Rollout & migration

- **No feature flag.** The control is reachable only from a button this same task adds; the off-state of a flag would be a nav row with nothing in it.
- **No migration, no backend deploy, no Aviran-gated apply step.** Nothing in §11 touches `database/`.
- **No backward compatibility surface.** No persisted state exists to read forward or backward, by design (§3.1).
- **Ships independently of the backend, like T-031.** With no `SupabaseConfig.plist` and no density rows, the modal still opens, the slider still moves, and every hour renders empty — which is exactly PRD req 2's silent-empty state. The feature is demoable and testable before migration `001` is ever applied.
- **Dependency direction:** T-034 (live events) reads `selectedHour` and adds a row to `HeatModalCard`. T-036/T-037/T-038 add their own `NavSurface` views and their own buttons to `MapNavRow`. None of them need to change anything this task writes.

---

## 8. Decisions and ratified deviations from the approved mockup

T-031 set the precedent for this section: a deviation from an approved mockup is recorded and justified here, not silently built (T-031 §8 D1, the `ColdOpenTitle` opaque backdrop). Four apply.

### D1 — The nav row ships with one button, not three

The mockup and `ux-flows.md` §2 both show three side-by-side nav buttons (search, heat, profile) plus a fourth Places icon. **None of them exist in the shipped app**, and neither search (T-038) nor Profile (T-037) nor Places (T-036) has a TRD, let alone a screen. This task builds `MapNavRow` as the container plus **the heat button only**.

A rendered button that opens nothing is a broken control — it fails at the Functional tier before it can be judged on anything else (`design-principles.md` §1) — and a disabled-looking button in shipped chrome invites exactly the "is the app broken?" read this map cannot afford. The row is laid out so the remaining buttons slot in without re-layout, and each is added by the task that owns its destination. If Aviran or `designer` wants three visible buttons before those screens exist, that is a product call, not an engineering one, and it is a small change here.

**Consequence, also a deviation:** the near-me cluster moves up out of the band the nav row now occupies (§2.3). The Places icon that `ux-flows.md` §2.1 names as the other bucket-2 control does not exist yet; T-036 attaches it to the same `isPresenting`-driven fade rather than re-deriving the rule.

### D2 — Custom `ZStack` overlay, not `.sheet()` — construction pinned

The design spec flagged this (§8.1) and this TRD settles the shape: a plain SwiftUI layer inside `MapScreen`'s `ZStack` at z3, below `MapNavRow` at z4, with an explicit scrim at z1 (§2.3). Not `.sheet`, not `.fullScreenCover`, not a `UIViewControllerRepresentable`, and not `.presentationBackgroundInteraction` (which cannot apply — there is no presentation). The nav row must remain hit-testable at all times or `ux-flows.md` §2.1's direct nav-switch requirement fails, and that is the entire reason this deviation exists.

### D3 — "Now" re-resolves on modal open, not on a timer

The PRD left open what happens when the app sits foregrounded across an hour boundary. Call: re-anchor on **modal open**, reusing T-031's existing `refreshIfHourRolled()` (§4.5), with no repeating timer anywhere.

The staleness only becomes visible when the user looks at the slider, and the only way to look at it is to open the modal — so the check placed exactly there is both sufficient and free. A wall-clock timer would burn a scheduled wake to correct a label nobody is reading, and would risk moving the thumb under a live finger. Combined with T-031's `scenePhase → .active` hook, the two triggers cover every path by which a user can observe the value.

### D4 — The shipped modal contains the slider only

The mockup renders stub toggle rows (a "baseline / always on, no toggle in V1" heat row, a T-034 live-events row) and a repaint-timing pill. The design spec labels all of them as mockup instrumentation. Making that explicit for the build: **none of them ship.** The heat layer has no on/off toggle in V1 at all, so a row saying so is chrome that explains an absent feature; the live-events toggle is T-034's to add to this card; the timing pill becomes the `HourRepaint` signpost (§4.7), which has no UI.

### D5 — Native `Slider`, and the contrast bar drawn around it

Native `Slider(step:)` plus a non-interactive overlay (§4.4). The consequence is recorded in §4.6 and matters: the thumb and the inactive rail are platform-drawn and are outside this app's authored contrast surface. Going custom to control them would trade a P0 (discrete VoiceOver stepping, req 6) for a bar the PRD itself already exempts the rail from. This TRD does not leave that as a preference — it is the reason the contrast test asserts the pairs it asserts and no others.

---

## 9. Verification hooks — including T-031's carry-forward

**Why this section exists.** `product`'s T-031 acceptance pass found that PRD req 5's bullets 2–3 (*repaints on hour change*, *repaint completes in <400ms*) had **zero traced test cases** — correctly, since nothing in T-031 changes the selected hour — and assigned them to T-032's own `qa`/`acceptance` (T-031 PRD, `BOARD.md` T-032 row, `PROGRESS.md` 2026-07-30). The same two behaviours are this PRD's req 2 bullets 1 and 3. They are the same two behaviours; this task is the only one that can exercise them; and a testability gap is much cheaper to close in a TRD than at acceptance. Each hook below is a build step in §11, not a suggestion to `qa`.

| Behaviour to verify | Hook built in this task | Step |
|---|---|---|
| Map repaints on hour change | `HeatComposition.fills(hoods:hour:band:)` is pure — a unit test asserts that a fixture snapshot yields **different** `[HoodFill]` for two different hours, and identical output for the same hour. No simulator needed. | C6 |
| Repaint completes <400ms | `XCTOSSignpostMetric` over the `HourRepaint` interval in a UI test that drives `app.sliders["hourSlider"].adjust(toNormalizedSliderPosition:)`, plus a `measure` unit test over `HeatComposition.fills` at catalog scale. Same instrument pattern as `ColdOpenPerformanceTests`. | C7 |
| Hour change leaves camera/zoom untouched | Nothing in the hour path writes `camera` — assert by construction in review, and by observation at `qa` (drag across the full range, camera unmoved). | review + qa |
| Session persistence across a nav switch (req 4) | `MapChromeState` unit test: `toggle(.heat)` → `toggle(.search)` → `toggle(.heat)` leaves `selectedHour` untouched. This is why `NavSurface` has four cases (§4.1). | C2 |
| Cold-launch reset (req 3) | `DensityStore` unit test — a fresh instance with an injected clock starts at `0`; extends T-031's existing `DensityStoreTests`. | C8 |
| Hour-snapping and clamping (req 1) | Structural via `in: 0...12, step: 1`; asserted at the binding's `set` in a unit test (fractional input rounds to a whole hour; out-of-range cannot be produced). | C4 |
| Contrast, every modal label (req 6) | The token-level test in §4.6 — four assertions that cover labels not yet written. | C9 |
| VoiceOver value strings, incl. midnight crossing (req 5, 6) | `HourFormat` unit tests with an injected clock and calendar. | C3 |

`qa` writes `prds/time-slider/TEST-PLAN.md` with a traced case per P0 bullet — and the two carried-forward bullets above must appear in the trace column with a real case behind them, not a "PASS by construction" note. That distinction is precisely what `product` caught at T-031's acceptance.

---

## 10. Risks and alternatives

| Risk | Mitigation / decision |
|---|---|
| SwiftUI re-renders every polygon on an hour change and misses 400ms | Polygons keep stable `Hood.id` identity; only `foregroundStyle` re-evaluates, over dozens of shapes. Measured, not assumed (§9). If it misses, the fallback is caching resolved `ShapeStyle` per band — local, not architectural (T-031 §10 already names this). |
| The `HourRepaint` signpost measures resolution, not pixels | Stated plainly in §4.7 rather than claimed as end-to-end. Backed by the structural guarantee (no fetch on hour change) and by a perceptual check at `qa`. Same honesty posture T-031 took on `XCTApplicationLaunchMetric`. |
| Custom overlay reimplements sheet behaviours (drag-to-dismiss, transitions) badly | The behaviours are small and enumerated (§4.2), and the alternative is unusable: `.sheet` covers the nav row and breaks §2.1's nav-switch rule. This is the one place a platform primitive is deliberately declined, and D2 records why. |
| The nav row ships with one button and reads as unfinished | D1 — deliberate, reversible, and preferable to a dead control. Named for `product`/`designer` at `trd-review`. |
| PRD req 2's "any open sheet is unchanged by an hour change" is unexercisable | Because the two can never be co-presented (D4/§2.3), the bullet is satisfied structurally rather than behaviourally. **Flagged rather than quietly passed**: if `product` intended the slider and a Hood sheet to coexist, that is a product/design change, not something this TRD should invent. Cross-check against T-033's TRD at `trd-review`. |
| Non-whole-hour timezones render a `:30` clock label | Cosmetic, P1 surface only, and out of V1's single city. §3.2 `[ASSUMPTION]`. |
| Touching accepted T-031 code (`DensityStore`) | One method, two lines, named in §4.5 with the reason. T-031's existing tests must pass unmodified. |
| Synthetic density makes every future hour a simulation, not a forecast | Named in the PRD and strategy; unchanged by this TRD. Nothing here should be read as making the control more truthful than the data behind it. |

**Alternatives considered and rejected:** `.sheet(isPresented:)` for the modal (covers the nav row — D2); a fully custom slider (loses free discrete VoiceOver stepping, a P0 — D5); a repeating timer to re-resolve "now" (D3); persisting `selectedHour` across launches (contradicts req 3, and T-031 §10 already rejected it); a per-hour network fetch (would make the 400ms budget unachievable — T-031 §4.4 made no-fetch-on-hour-change a contract precisely to prevent it); rendering three nav buttons with two inert (D1); asserting contrast on the platform-drawn thumb and rail (§4.6 — would fail against the control the PRD requires).

---

## 11. Build breakdown

Ordered. **Every step is `[iOS]`.** No `[Backend]`, no `[Algo/Data]` — see §1.

| # | Step | Tag |
|---|---|---|
| C1 | `MapChromeState` + `NavSurface` (§4.1) | **[iOS]** |
| C2 | `MapNavRow` with the heat button only (D1); wire into `MapScreen`'s `ZStack` at z4; move the near-me cluster above it; bucket-2 fade driven by `isPresenting` (§2.3). Exclusivity unit test incl. the selected-hour-survives-a-switch case (§9) | **[iOS]** |
| C3 | `HourFormat` + tests — numeral, clock label, `isNextDay`, VoiceOver string; injected clock/calendar; midnight-crossing and 0/12 cases | **[iOS]** |
| C4 | `HourSlider` — native `Slider(in:step:)`, the `Double` bridge, ≥44pt frame, non-hit-testing tick overlay, a11y label/value/identifier (§4.3, §4.4) | **[iOS]** |
| C5 | `HeatModalCard` + scrim + three dismissal paths + Reduce-Motion-aware transition (§4.2); `HourReadout` (numeral + "next day" pill) | **[iOS]** |
| C6 | `HeatComposition.fills` + switch `MapScreen` to one resolution per pass; the differs-across-hours unit test (§9) | **[iOS]** |
| C7 | `HeatRepaintSignpost` + the `XCTOSSignpostMetric` UI test and the `measure` unit test against the 400ms budget (§4.7, §9) | **[iOS]** |
| C8 | `DensityStore`: modal-open `refreshIfHourRolled()` call site + the mid-await guard (§4.5); cold-launch-reset test | **[iOS]** |
| C9 | The four colour sets + the token-level contrast test, light and dark (§4.6) | **[iOS]** |

**`trd-review` sign-off needed from: `ios-developer` + `ios-code-reviewer` only.** `developer`, `code-reviewer` and `data-engineer` have no step to review — this TRD writes no SQL, no RLS, no pipeline, and no algorithm. Worth one explicit cross-check at review, though: **T-033's TRD** should be read against §2.3/D4 (chrome layering and the modal-vs-sheet exclusion), since both tasks are in `trd` at the same time and both put something in the bottom of the screen.
