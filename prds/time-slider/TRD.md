# Time Slider — now → +12h — TRD

**Task:** T-032 · **Linear:** `PAS-15` · **Status:** v4 — §9 amendment only, no `trd-review` re-run owed
**Owner:** architect · **Date:** 2026-07-30 · **Revised:** 2026-08-03 (v4)
**PRD:** [`time-slider.md`](./time-slider.md) (Draft v9 — req 5's rendered-legibility bullet added at acceptance 2026-08-03)
**Design reference:** [`design/phase-1/time-slider-design.md`](../../design/phase-1/time-slider-design.md) (v4) + its mockup — **informational input, not a gate.** The pre-code design gate was retired 2026-08-02 (`BOARD.md` lifecycle section). Where this TRD and the design spec disagree, this TRD wins and says so (§8).
**Builds on:** [`prds/map-hoods-heat/TRD.md`](../map-hoods-heat/TRD.md) (T-031, shipped and accepted). Extends that module layout; does not restate it.

**What changed at v4 (2026-08-03) — T-055.** One thing: **§9 gains row 5b**, the verification row §2.3's z5 layout rule never had. Nothing else in this document changes — no contract, no decision, no build step, no scope. **§2.3's z5 rule itself is unchanged**; it was correct as written and the build deviated from it. This is a documentation fix to the *gate*, not to the *design*, so **no `trd-review` re-run is owed and nothing here blocks `ios-developer`'s in-flight T-032 rebuild** — the rebuild's correctness is already fully specified by §2.3 z5 and by PRD v9's req 5 bullet, both of which predate this revision. Same shape as T-053's §9 amendment to the `search-quick-filters` TRD.

Why the row was missing, stated plainly because it is the third instance of one failure shape (L-009; T-046, then T-053/`PAS-43`, now this): §2.3 stated the layering rule as *architecture* and §9 never turned it into a *check*. `product`'s acceptance pass found `MapNavRow` drawing on top of `HeatModalCard`'s readout at the **default** text size — the "next day" flag truncated to "…t day", which at +12h/11:00 makes the readout state the wrong hour — after `code-review` and `qa` had both passed the build. Neither gate could have caught it: `XCUIElement.exists` returns `true` for a fully occluded label, and no source read sees an overlap. A rule with no row is a rule no gate can fail.

**What changed at v3 (2026-08-02).** `trd-review` came back split — `ios-developer` APPROVE WITH MINORS, `ios-code-reviewer` REQUEST CHANGES — so this revision resolves exactly those findings and nothing else. No decision, contract, or build step is redesigned; D1–D10 all stand as written at v2.

| # | Finding | Raised by | Fix in v3 |
|---|---|---|---|
| 1 | **Blocking.** §9 row 7 and C13 verified camera-immutability only for an inert horizontal drag (7b) and a pan starting outside the band (7c) — never for a normal, **in-band, vertical** edge slide, the one gesture this task exists to ship. D7/§2.4's central claim ("MapKit's pan recognizer is never in that touch's recognizer chain") therefore shipped on hit-test reasoning alone, with no on-device check — while §4.8 applies "confirm it, do not assume it" to a *less* central claim | `ios-code-reviewer` | §9 row 7 gains sub-check **(e)**; C13's verify-list gains the matching line; §2.4 and D7 restate the claim as a prediction this TRD requires confirmed, not as settled fact |
| 2 | Minor. §9 row 7d / C13's sheet check collapsed to one flat rule, but `MapScreen.swift:186`'s `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` makes "as it does today" two different behaviours — background-interactive at `.medium`, not at `.large` | `ios-code-reviewer` | Row 7d and C13 now exercise **both detents** explicitly, and both touch targets (sheet content, still-exposed map) |
| 3 | Minor. §4.8's `DragGesture(coordinateSpace: .named("map"))` named a coordinate space **no view in this TRD or in the shipped codebase declares** — grep confirms zero `.coordinateSpace` usages anywhere. `EdgeGeometry`'s `band`/`hour(atY:)` are documented in "this view's own coordinates," which is `.local` | `ios-developer` | Corrected to the default `.local`, with the reason stated so it isn't re-invented at build time |
| 4 | Minor. §9 row 6's Step column cited `C9, C12` for the ≥44pt button-path frame assertion, which is actually built in `C4` | `ios-developer` | Step column corrected to `C4, C9, C12` |
| 5 | Found while fixing 1–4, raised by neither review: the TRD named the shipped sheet **`HoodStubSheet`** in three places. **No such type exists** — `Detail/HoodSheet.swift:7` declares `HoodSheet`, and grep finds `HoodStubSheet` nowhere in `passenger-code`. Left standing, C13's and §9 row 7's sheet checks point `ios-developer` and `qa` at a type they cannot find | `architect` (v3 pass) | Renamed to `HoodSheet` at all three sites (§1, §9 row 7, §11 footer). Name only — no behaviour, no scope, no decision changes |

**Two things a re-reviewer should check rather than take on trust.** (1) The header, the four rows above, and the §2.4 / §4.8 / D7 / §9 edits were **already present in the shared working tree, uncommitted, when this `architect` pass opened the file** — several sessions share this tree (`CLAUDE.md` rule 2). They are not this pass's writing. Each was re-read against `27faac4` and `7a1f99c` and against source before being allowed to stand, and the gaps found are what this pass actually wrote: §4.10's detent note, C13's verify-list (which the changelog above promised and the body had not received), §10's new risk row, §2.4's forward pointer, and finding 5. (2) D6's **founder-direct icon-only paragraph** ("remove the name from the icons in the nav bar, show only icons") is `chief-of-staff`'s work, not this pass's — it was uncommitted in the tree while this revision was being written and that session has since committed it separately (`passenger-brain 5220c1f`). It is not part of the v3 review scope and no v3 edit touches it.

**What changed at v2.** v1 (2026-07-30/31) designed one entry path: a heat button opening a modal card around a horizontal `Slider`. The PRD has since added a second, structurally different path — a vertical drag on either live screen edge (req 7) — and Aviran has ratified its three open questions. v2 keeps every v1 decision that survives (D1–D6 stand), adds the edge-gesture architecture (§2.4, §4.8–§4.10, D7–D9), settles the two items the design spec explicitly handed to `architect` (gesture construction, inset geometry), and adds two things v1 could not have: a **Build Phase 1 data seed** without which nothing in this feature is observable (§3.4, D10) and a **§9 verification table with one row per P0 requirement** (`architect.md`, L-018).

---

## 1. Context

Read the PRD first. Nothing here restates it. This document decides what it leaves open and pins the contracts `ios-developer` builds against.

**Surface: iOS-only. Confirmed, not assumed.** Re-checked at v2 against the PRD's Technical design and the shipped code: no new table, no new column, no new endpoint, no change to an existing one. `DensityAPI.fetchDensity(from:)` already fetches the whole `[anchorHour, anchorHour + 12h]` window in one request (`hour_bucket=gte./lte.`), and `hood_density` already keys on an absolute UTC timestamp. Everything this feature needs from the backend is in the shipped contract. **§11 contains no `[Backend]` and no `[Algo/Data]` step.** `trd-review` routes to **`ios-developer` + `ios-code-reviewer` only** (§11).

**What this feature is, architecturally.** Two things, not one:

1. **The app's first chrome above the map** — the persistent nav row, the modal layer hanging off it, and the layering rule deciding what covers what. That layering, not the slider, is what has consequences: T-034/T-036/T-037/T-038 all land in the same bottom band.
2. **The app's first custom gesture surface** — a hit-testable overlay claiming a permanent strip of the map. This is the part that can regress already-shipped behaviour (`HoodSheet`'s drag-to-dismiss, MapKit pan, T-031's tap-to-open-Hood), so it gets the most explicit construction rules in this document.

**Open items resolved here:**

| # | Open item | Source | Call | Where |
|---|---|---|---|---|
| 1 | Heat modal construction — not a `.sheet()` | design §8.1 | `ZStack` overlay in `MapScreen`, below the nav row's layer | §2.3, D2 |
| 2 | `selectedHour` write-path | design §8.2 | Settled by T-031 — plain `var selectedHour: Int` on `@Observable DensityStore`. Confirmed against the shipped file; **not redesigned** | §4.3 |
| 3 | "Now" re-resolving while foregrounded across an hour boundary | PRD Open technical questions (a); design §8.3 | Re-anchor on modal **open** and on **edge touch-down**, on top of T-031's existing `scenePhase → .active` hook. No timer | §4.5, D3 |
| 4 | Day-boundary bucket keying | PRD risks; design §8.4 | **Already resolved by T-031** — `hour_bucket` is an absolute UTC timestamp and `DensityStore` keys on epoch-hour. Closed. The "next day" pill is display-only on top of it | §3.2 |
| 5 | Native `Slider` vs. custom control (button path) | design §8.5 | **Native `Slider(value:in:step:)`.** The tick overlay is decorative and non-interactive | §4.4, D5 |
| 6 | **Edge gesture recognizer construction** | design §8.6; PRD Open technical questions (b) | **SwiftUI `DragGesture` on a dedicated hit-testable overlay above `Map`** — not a `UIGestureRecognizer`, and not a gesture-arbitration problem at all | §4.8, **D7** |
| 7 | **Confirming the 64pt/40pt insets against real device geometry** | design §8.7; PRD Open technical questions (b) | Numbers **confirmed correct** for the reference device and re-derived as `max(designFloor, safeAreaInset + clearance)` so they hold on every device instead of only that one | §4.9, **D8** |
| 8 | Which nav-row buttons exist in this build | found by reading the shipped code | The nav row does not exist yet. T-032 builds the container plus **the heat button only**, glyph `flame.fill` | §2.3, D1/D6 |
| 9 | Landscape and per-idiom edge availability | not raised by any doc — found at v2 | **Edge path is portrait-only on iPhone**; iPad left edge only; right edge never on iPad. One pure function decides | §4.10, **D9** |
| 10 | Nothing in this feature is observable in Build Phase 1 | not raised by any doc — found at v2 by reading `DensityStore` | A **bundled relative density seed** ships in this task, behind the existing `BuildPhase.seedIsAuthoritative` constant | §3.4, **D10** |

---

## 2. Architecture

### 2.1 Module layout — additions to T-031's tree

```
Passenger/
  Map/
    MapScreen.swift            MODIFIED — hosts the chrome ZStack; near-me moves (D1)
    MapChromeState.swift       new — NavSurface + the one-surface-at-a-time rule
    MapNavRow.swift            new — separate side-by-side buttons; heat button only (D1/D6)
  HeatModal/
    HeatModalCard.swift        new — the overlay card: scrim, transitions, dismissals
    HourSlider.swift           new — native Slider + decorative tick overlay + a11y
    HourReadout.swift          new — numeral + "next day" pill
    HourFormat.swift           new — pure offset → (numeral, clock time, isNextDay)
  EdgeHour/
    EdgeHourZone.swift         new — the 24pt capture overlay + DragGesture (§4.8)
    EdgeHourTrack.swift        new — active track + floating readout chip
    EdgeHint.swift             new — the 5pt × 56pt idle capsule (Q8)
    EdgeGeometry.swift         new — pure: insets, usable band, y → hour (§4.9)
    EdgeAvailability.swift     new — pure: which edges are live (§4.10)
  Density/
    DensityStore.swift         MODIFIED — seed path (§3.4) + one guard (§4.5)
    DensitySeed.swift          new — bundled relative seed → rows (§3.4)
  Map/
    HeatComposition.swift      new — pure hoods × hour → [HoodFill] (§4.7)
  Support/
    HeatRepaintSignpost.swift  new — the HourRepaint interval (§4.7)
Resources/
  density-seed-tel-aviv.json   new — Build Phase 1 fake data (§3.4)
Assets.xcassets/
  MutedOnSurface · PillSurface · SliderFill · NowTick · EdgeRail   new colour sets
```

Xcode synchronized file groups are on — dropping files in the folder is enough, no `project.pbxproj` edit.

### 2.2 Boundaries — who is allowed to know what

- **`HeatModal/` knows no map, no geometry, no network.** It reads and writes one `Int` and formats a date. `HourFormat` is pure and takes its calendar and its clock as parameters, so every label string is unit-testable with no simulator and no fixed timezone.
- **`EdgeHour/` knows no map and no density.** It converts a touch position into an `Int` and writes it. `EdgeGeometry` and `EdgeAvailability` are pure functions over `CGSize`/`EdgeInsets`/`UIUserInterfaceIdiom` — the two hardest things in this feature to get right are therefore the two easiest to unit-test, with no simulator and no gesture.
- **`MapChromeState` knows no view.** It holds which nav surface is presented and nothing else. It does not own `selectedHour` — that is the whole point of PRD req 4.
- **`Density/` still knows no geometry.** `HeatComposition` pairs a Hood with a band and lives on the composition seam T-031 already put in `Map/`; it takes a lookup closure, never a `DensityStore`.
- **`Map/` remains the only layer that knows both**, and the only layer that knows the z-order.

### 2.3 The chrome layering rule

`MapScreen`'s body becomes an explicit `ZStack`, top of list = furthest back:

| z | Layer | Behaviour when a nav surface is presented |
|---|---|---|
| 0 | `Map` + `HoodLayer` + `PlaceLayer` + `UserAnnotation`, `ColdOpenTitle`, `CachedDataIndicator` | Unchanged. |
| 1 | **`EdgeHint`** (per live edge) | Hidden — see §4.10's availability rule. Non-hit-testing at all times. |
| 2 | **`EdgeHourZone`** (per live edge, 24pt) | **Not in the hierarchy at all** while a surface or a sheet is presented (D7 rule c). |
| 3 | **Scrim** — `Color.black.opacity(…)`, `.contentShape(Rectangle())`, tap → dismiss | Present only while a nav surface is presented. Makes tap-outside work; stops a map tap opening a Hood sheet under an open modal. |
| 4 | **Bucket-2 chrome** — `NearMeButton`, `HoodButton`, `SettingsHint` | `.opacity(0)` + `.allowsHitTesting(false)` while presented (`ux-flows.md` §2.1 bucket 2). Reduce Motion honoured. |
| 5 | **Modal card** — `HeatModalCard` | Anchored a fixed distance above the nav row, sized to content — never `bottom: 0`. |
| 6 | **`EdgeHourTrack`** | Only during an active edge drag, which can only happen when nothing else is presented. Mutually exclusive with z5 by construction. |
| 7 | **`MapNavRow`** | Always visible, always hit-testable, never covered — this is what makes direct nav-switching work with no dismiss-first step. |

Two consequences worth stating rather than discovering:

- **`.presentationBackgroundInteraction` is not involved and must not be reached for.** That is T-033's mechanism for system sheets. This is a custom overlay in the app's own hierarchy; the scrim at z3 is the equivalent, and the map is deliberately *not* interactive while the modal is open.
- **The heat modal and a system `.sheet` are never co-presented** (D4). A `.sheet` presents above the entire hierarchy including z7; while the modal is up, the scrim blocks the map taps that would open a sheet. Mutually exclusive in both directions.

**`MapNavRow` is a layout container, not a visual one** (D6, founder-direct). The icons render as separate, independent buttons side by side, each its own tap target with its own background — no shared capsule, bar, divider, or segmented control. The heat button's glyph is **`Image(systemName: "flame.fill")`**, pinned by `designer` 2026-08-02 (design spec §2, §8 item 8) and adopted here as the build target, closing D6's own flagged gap.

**The near-me cluster moves.** T-031 anchors `NearMeButton`/`HoodButton`/`SettingsHint` at `.bottom` with 32pt padding — the band the nav row now occupies. They move above the nav row. This is a change to accepted, shipped T-031 layout, named here rather than left as an implementation surprise (D1).

### 2.4 The edge surface, and why it is not a gesture-arbitration problem

The design spec (§2, §7, §8 item 6) frames the 24pt capture zone as needing to be "wide enough to reliably win gesture-initiation against MapKit's own pan recognizer," citing T-031's FB19394663 workaround as precedent. **That framing does not apply to this construction, and the difference matters enough to state.**

FB19394663 is about a gesture attached *to the `Map` view itself* — `MapScreen.swift:113-122` uses `.simultaneousGesture(SpatialTapGesture())` precisely because a gesture in `Map`'s own subtree has to coexist with MapKit's internal recognizers. The edge zone is not in that subtree. It is a **sibling view drawn above the map**, and UIKit hit-testing runs front-to-back before any recognizer arbitration happens: a touch inside the zone resolves to the zone's view, so MapKit's pan recognizer is never in that touch's recognizer chain and never competes. On that reasoning there is nothing to win — **and the next paragraph is why this TRD treats that as a prediction to confirm rather than a fact to build on.**

Three things follow, all load-bearing:

- **The 24pt number is not doing the job the design spec assigns it.** Its arbitration justification is void; its *acquisition* justification (§7 there — an edge-anchored target cannot be overshot past the bezel; the ~708pt gesture axis gives large correction margin; req 6 keeps a fully conforming fallback) stands untouched, and that is the argument Aviran ratified at Q7. **The number is unchanged at 24pt and Q7 is not reopened** — only its stated mechanism is corrected.
- **The zone is a genuine dead strip.** 24pt at each live edge cannot be panned, pinched, or tapped through. On a 393pt-wide iPhone that is 48pt, ~12% of the width, permanently unavailable to the map. The design spec priced this ("narrow enough to minimize the permanently-unpannable map band"); §10 names it as the accepted cost it is, and §9 gives `qa` a check for it.
- **Requirement (c) from design §8 item 6 — never claim a touch while a sheet is presented — is satisfied structurally, not by a flag.** The zone is *removed from the view hierarchy* in that state (z2 above), so there is no recognizer to claim anything. This is exactly the "genuine non-engagement, not deferred no-op" the design spec required, and it is the strongest available form of it.

**The paragraph above is a prediction, and this TRD requires it confirmed before C13 is done — it is not a settled fact [added at v3, `ios-code-reviewer`].** Everything in this section rests on one claim: that MapKit's pan recognizer is never in the recognizer chain of a touch that lands in the zone. That claim is derived from documented UIKit hit-test ordering, and it is the strongest reasoning available — but this document cites `FB19394663` two paragraphs up precisely because SwiftUI's `Map` has already been observed not to behave the way plain recognizer-chain reasoning predicts. Reasoning of the same kind therefore cannot be the last word on the most load-bearing claim in the feature, when §4.8 already applies "confirm it, do not assume it" to a narrower one.

**What that means concretely.** If the prediction is wrong — if MapKit's pan recognizer does receive the touch simultaneously under the sibling overlay — the map jumps or drifts under the finger during *every ordinary edge slide*, a visible regression against T-031's shipped camera behaviour on this feature's primary gesture. Nothing in the v2 verification set would have caught it: an inert horizontal drag and a pan starting outside the band are both cases where the camera is *expected* to be untouched or expected to move, so both pass either way. **§9 row 7(e) and C13 now check the in-band vertical case directly, on device or in a UI test.** If that check fails, D7's construction is what changes (the remaining option is a `UIViewRepresentable` recognizer that arbitrates against nothing, since `Map` exposes no recognizer to defer to — meaning the real fallback is a product conversation about the edge path, not a quiet code fix), and it should fail at C13 rather than at `qa` or after ship.

---

## 3. Data model

### 3.1 No new persisted state, on either side

The control owns nothing. `selectedHour` is a plain `Int` on `DensityStore`, in memory, session-scoped, **never written to `UserDefaults`/`AppStorage`/disk**. PRD req 3's cold-launch reset is therefore a property of where the value lives, not of a reset routine someone could forget to call (§4.6). `DensityCache` persists density rows only; it has never held an hour selection and must not gain one. `MapChromeState` is likewise in-memory.

No migration, no schema change, no new query parameter. Nothing here carries a location, a device id, or a user id — the request surface is untouched, so T-031's "location cannot leak through a query that never had a place to put it" holds unchanged. The edge gesture reads a touch's `y` inside a view's own bounds and converts it to an integer; **no touch coordinate is stored, logged, or sent anywhere.**

### 3.2 Time — how an offset becomes a label

`anchorHour` (UTC hour floor, T-031) + `offset × 3600s` = the selected absolute instant. Everything the user reads derives from that instant in the **current** calendar and timezone:

- numeral: `"Now"` for offset 0, `"+\(offset)h"` otherwise — offset is the primary channel, never a bare clock time
- clock time (`"21:00"`, PRD P1): `Date.FormatStyle` in `.current` timezone
- `isNextDay`: `!Calendar.current.isDate(selectedInstant, inSameDayAs: now)`, compared against the real clock, not against `anchorHour`

**[ASSUMPTION]** every supported timezone is a whole-hour offset from UTC, so a UTC hour floor lands on a local hour boundary and "+3h" reads as a clean o'clock. True for Tel Aviv (UTC+2/+3) and for V1's only city; false in e.g. India (+5:30). The failure mode is cosmetic — the P1 clock label would read `20:30` — and it never affects bucket lookup, which stays in epoch-hour arithmetic. Recorded in §10 rather than engineered around for a city V1 does not ship in.

### 3.3 Edge geometry is derived, never stored

`EdgeGeometry` computes from the live `GeometryProxy` on every layout pass. Nothing about the band, the stop spacing, or the last touch position persists between drags. A drag is stateless apart from one `@GestureState` for "is this drag live and vertical-dominant" (§4.8).

### 3.4 Build Phase 1 — the density seed **[new at v2, D10]**

**The finding.** `DensityStore.load()` (read directly, `Density/DensityStore.swift:56-72`) has exactly three outcomes: live fetch → `DensityCache` → `.unavailable`. There is **no seed path**. In Build Phase 1 there is no `SupabaseConfig.plist`, so `DensityAPI.fetchDensity` throws `.unconfigured`, the cache is empty on a fresh install, and `snapshot` is `.empty`. `band(for:hour:)` returns `nil` for every Hood at every hour, and `HoodLayer.fillColor` returns `.clear`. **Shipped as-is, T-032 would be a control that visibly does nothing at every one of its 13 positions**, and three of PRD req 2's four bullets would have no observable to check.

This is not a defect in T-031 — that task's own acceptance carried "heat never observed live" forward as a named gap, correctly, because T-031 could not change the hour. T-032 is the only task that can exercise the repaint, so the data it needs to be exercised against belongs here. `BOARD.md`'s own Build Phase 1 definition names this feature explicitly: *"Fake/hardcoded data baked into the app — just enough to demo interactions (saving places, the 12h time slider, browsing Hoods/places)."* T-034's PRD took the same call for the same reason (a bundled fake event set folded into its own build scope), and T-033 shipped the pattern.

**The shape.** Follow `PlaceCatalog` exactly — the same `BuildPhase.seedIsAuthoritative` constant, the same `Source` enum extension, the same injectable resource name and bundle:

```swift
// Resources/density-seed-tel-aviv.json — relative, not absolute
{ "hoods": [ { "hood_id": "florentin", "bands": [2,2,3,3,4,4,4,3,3,2,1,1,1] } ] }
```

`bands` is 13 entries, index = hour offset 0…12; a `null` entry means **no row for that hour**, which is how the seed exercises req 2's silent-empty bullet on purpose rather than by accident.

**Why relative and not the wire shape.** `DensityAPI.Row.hourBucket` is an absolute ISO timestamp. A bundled file of absolute timestamps is stale the moment it is authored and would make every Phase-1 launch a different demo. `DensitySeed.rows(anchorHour:)` synthesises `DensitySnapshot` input against the live `anchorHour` at load time, so the seed is correct at any launch on any date, and it flows through the same `DensitySnapshot` epoch-hour keying the live path uses — the seed exercises the real code, not a parallel one.

**Authoring rule, so the seed can actually falsify something:** at least three Hoods must change band between at least four adjacent hour pairs, and at least one Hood must have `null` for at least one hour. Without variation, C6's "differs across hours" test and `qa`'s perceptual repaint check both pass vacuously.

**Flagged for `product` at `trd-review`, not decided unilaterally:** this adds a bundled data artifact to a PRD whose Technical design says "nothing to source or author." It is a Build-Phase-1 sequencing consequence, not a scope change to the control — but `product` should confirm it rather than discover it, and confirm that Phase-2 acceptance re-tests the same requirements against the live feed with the constant flipped (§7).

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

Four cases, one view. Deliberate, and the narrowest thing that makes PRD req 4 testable: "switching to a different nav modal and back does not reset the hour" cannot be exercised at this task's own `qa` if the type can only express one surface. The four-member set is not invented here — `ux-flows.md` §2.1 locks it. A case with no view costs nothing, ships nothing, and stops T-036/T-037/T-038 each inventing a private boolean and quietly breaking exclusivity. **This is a state type mirroring a locked spec, not a hook for an unbuilt feature** — `ios-code-reviewer` should read it as such and reject any *view* work for the other three cases in this task's diff.

`toggle` closing the already-open surface is an architect call filling a gap: the design lists three exits and does not say what a second tap on the lit heat button does. Doing nothing there reads as broken.

### 4.2 The modal card

```swift
struct HeatModalCard: View {
    let onDismiss: () -> Void
    // content: section header + HourReadout + HourSlider. Nothing else in V1 (D4).
}
```

- Background: opaque `Color("Surface")` (T-031's token), rounded, sized to content. **Not `.ultraThinMaterial`** — same reasoning as T-031 §8 D1: a contrast ratio against a translucent layer over a live map is not a number anyone can verify, and PRD req 6 demands a verifiable one.
- Dismissals: (a) drag handle + `DragGesture` past a distance/velocity threshold; (b) scrim tap; (c) `MapNavRow` tapping another surface. All three route to `MapChromeState`, none to a private `@State` bool.
- Transition `.move(edge: .bottom).combined(with: .opacity)`; under `\.accessibilityReduceMotion` it cross-fades with no movement.
- **Composes rows, not a bare slider.** T-034's live-events toggle lands as a second row. That is a layout fact, not a hook: no toggle, no placeholder, no "always on" stub row ships in this task (D4).

### 4.3 The one value — Q3, structurally

`selectedHour` stays `var selectedHour: Int` on `@Observable DensityStore`, verified against the shipped file. **There is exactly one storage location for the hour in the entire app.** Q3 ("one shared value across both edges and the heat button") is ratified, and this is what makes it a fact rather than a convention: there is no second property that could desync.

```swift
// In HourSlider — the Double bridge lives in the one file that owns the control:
Slider(
    value: Binding(get: { Double(selectedHour) }, set: { selectedHour = Int($0.rounded()) }),
    in: 0...12, step: 1
)
```

Range clamping and hour snapping are structural on this path — `in: 0...12, step: 1` makes an off-hour or out-of-range value unrepresentable. On the edge path the same invariant is held by `EdgeGeometry.hour(atY:in:)`'s own clamp (§4.9), which is the only other writer.

**`ios-code-reviewer` findings, both blocking:** (1) any second stored hour — an `@State var hour`, a mirror on `MapChromeState`, a per-edge value — anywhere in the diff; (2) a hand-rolled clamp or rounding pass outside those two sites, which means the invariant moved out of the type and into a routine someone can forget.

### 4.4 The slider view (button path)

```swift
struct HourSlider: View {
    @Binding var selectedHour: Int    // 0...12
    let readout: HourFormat.Readout
}
```

- `.frame(minHeight: 44)` on the control itself regardless of how slim the drawn track is (Fitts's Law). The visible thumb may render smaller.
- The tick/hairline overlay is drawn in a `GeometryReader` **with `.allowsHitTesting(false)`** — it must never intercept the drag, or both the native gesture and the VoiceOver adjustable action degrade.
- `.tint(Color("SliderFill"))`, `.accessibilityLabel("Map hour")`, `.accessibilityValue(HourFormat.voiceOverValue(readout))`, `.accessibilityIdentifier("hourSlider")`. The identifier is not cosmetic — §9 drives the control through `XCUIElement.adjust(toNormalizedSliderPosition:)`.
- VoiceOver's discrete stepping comes from `step: 1` on a real `Slider` and is not reimplemented.

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

Pure, injectable clock and calendar. Its tests must include a midnight crossing and offsets 0 and 12.

### 4.5 Changes to T-031's store

Three, all named rather than slipped in. `ios-code-reviewer` should confirm T-031's existing `DensityStoreTests` still pass unmodified alongside the new cases.

1. **Seed path in `load()`** (§3.4). Mirrors `PlaceCatalog.load()`: when `BuildPhase.seedIsAuthoritative` is `true`, load `DensitySeed` and attempt no fetch; otherwise the existing live → cache → unavailable precedence, unchanged, with the seed as a final fallback below cache. `Source` gains a `.seed` case. Both branches stay compiled and type-checked, per `BuildPhase.swift`'s own stated reason for being a runtime constant and not `#if`.
2. **New call sites for `refreshIfHourRolled()`** — on heat-modal open *and* on edge touch-down, in addition to T-031's existing `scenePhase → .active` hook (D3). The method already early-returns when the hour has not rolled, so the common case costs one comparison.
3. **A mid-`await` guard in `refreshIfHourRolled()`.** The method reads `selectedHour` before an `await` and writes a remapped value after it (`DensityStore.swift:82-85`). If the user moves the slider or drags an edge during that await, the write clobbers their input. Capture `selectedHour` before the await and apply the remap **only if it is unchanged**; otherwise leave the user's value alone. This becomes reachable the moment call site 2 exists — a modal-open refresh now overlaps a user who is already dragging.

### 4.6 Cold-launch reset (req 3) — by absence, not by routine

**No reset-on-launch code is written, and none should be.** The guarantee is structural, in three parts:

- `DensityStore.selectedHour` is declared `var selectedHour: Int = 0` — a fresh instance is at "now" before anything runs.
- `MapScreen` holds it as `@State private var densityStore = DensityStore()`, constructed once per process. A cold launch is a new process, so it is a new store.
- `anchorHour` is set in `init` from the injected `now()` closure, so "now" re-resolves against the real clock at launch (req 3 bullet 2) with no cached value anywhere to be stale.

The existing cold-open pattern (`ColdOpenSignpost.begin()` in `PassengerApp.init()`, `endIfNeeded()` on `MapScreen`'s `.onAppear`) is a measurement hook and is deliberately *not* extended — hanging a reset off it would replace a structural guarantee with a call someone can delete. **`ios-code-reviewer` treats any `@AppStorage`/`UserDefaults`/file write of the selected hour as a blocking finding**, and §9's C8 asserts a fresh store starts at 0 with an injected clock.

**Warm launch is deliberately different and is not a bug:** resuming from background keeps the session's hour, and `scenePhase → .active` remaps it against the new wall clock (§4.5). Req 3 says *cold* launch. `qa` should test both and expect different answers.

### 4.7 Repaint composition and its measurement

```swift
struct HoodFill: Equatable, Sendable { let hood: Hood; let band: HeatBand? }

enum HeatComposition {
    /// Pure. Takes a lookup closure, not a store — testable with no DensityStore,
    /// no network, no simulator.
    static func fills(hoods: [Hood], hour: Int, band: (String, Int) -> HeatBand?) -> [HoodFill]
}
```

`MapScreen`'s body resolves fills **once per pass** through this function and iterates the result, instead of calling `densityStore.band(...)` inline per Hood as it does today (`MapScreen.swift:79`). Two load-bearing reasons: it gives the repaint a single nameable completion point, and it gives §9 a pure function to measure.

`HoodLayer` is the only hour-bound layer that exists (verified: `PlaceLayer` takes no band and no hour). "Every hour-bound layer" is therefore a set of one today; T-034 joins it by reading the same `selectedHour`.

```swift
enum HeatRepaintSignpost {   // mirrors Support/ColdOpenSignpost.swift exactly
    // interval name "HourRepaint", category "HeatRepaint"
    @MainActor static func begin()        // on a real change, from either writer
    @MainActor static func endIfPending() // immediately after HeatComposition.fills(...) returns
}
```

**Honest scope of the measurement**, stated the way T-031 stated its cold-open one: `HourRepaint` brackets *"`selectedHour` written → every Hood's band resolved for the new hour."* It excludes MapKit's own frame commit, which app code cannot observe. The <400ms budget is held structurally first — T-031's contract that **no code path fetches on an hour change**, now reinforced by the seed being in memory — and measured second. `qa` additionally confirms perceptually that dragging produces no lag, no spinner, and no intermediate state.

### 4.8 Edge gesture construction **[D7]**

```swift
struct EdgeHourZone: View {
    let edge: HorizontalEdge          // .leading / .trailing
    let band: ClosedRange<CGFloat>    // usable y range in this view's coordinates
    @Binding var selectedHour: Int
    @Binding var activeDrag: EdgeDragState?
}

struct EdgeDragState: Equatable {
    let edge: HorizontalEdge
    let y: CGFloat            // clamped to `band`, drives the track + chip position
    let hour: Int
}
```

**Construction: a SwiftUI `DragGesture(minimumDistance: 4)` on a `Color.clear.contentShape(Rectangle())` overlay of fixed 24pt width, aligned to the edge, at z2.** Not a `UIGestureRecognizer` subclass, not a `UIViewRepresentable`, not `.simultaneousGesture`, not `.highPriorityGesture`.

**Coordinate space: the default `.local`, deliberately — corrected at v3 [`ios-developer`].** v2 wrote `coordinateSpace: .named("map")`, which named a space **nothing declares** — no view in §2.1's layout attaches `.coordinateSpace(.named("map"))`, and grep finds no `.coordinateSpace` modifier anywhere in `passenger-code` today. Left as written, `ios-developer` would have had to invent an owner for it at build time, and the obvious candidate is `Map` itself — the one view §2.4 goes out of its way to keep the zone *out of*. The failure mode is silent, not a crash: `value.location.y` measured in one frame, compared against a `band` computed in another, giving a wrong-but-plausible hour. `.local` is correct and needs no declaration: `EdgeGeometry.band(in:safeArea:)` and `hour(atY:in:)` are both documented as operating in **this view's own coordinates** (§3.3, §4.9), which is exactly what `DragGesture`'s default gives, and each zone is sized by its own `GeometryReader` so the two edges never need a shared frame of reference. **If a future step genuinely needs a shared named space, it must name the declaring view in this TRD first** — a named space with no declared owner is not a contract.

Why this and not UIKit — the reasoning, since design §8 item 6 posed it as an open choice:

- **The UIKit option cannot do the thing it would be chosen for.** Its only real advantage would be arbitrating against MapKit's pan via `require(toFail:)` or a delegate. SwiftUI's `Map` exposes no `MKMapView` and no access to its recognizers, so that relationship cannot be established at all. What remains of the UIKit option is a representable wrapper around a recognizer that behaves like the SwiftUI one, with more code and a `@MainActor`/`Sendable` bridging surface Swift 6 strict concurrency will make us justify.
- **Hit-test order already gives us priority** (§2.4). The mechanism the UIKit route would exist to provide is provided for free by being a sibling above the map.
- **It keeps the whole feature in one concurrency domain.** Everything here is `@MainActor` SwiftUI; no bridge, no `nonisolated(unsafe)`, nothing to argue with the compiler about.

Three rules the construction must satisfy, each mapped to its mechanism:

| Rule (design §8 item 6) | Mechanism here |
|---|---|
| (a) Claim the touch before MapKit | Sibling overlay above `Map` in the `ZStack`; UIKit hit-testing resolves to it first. Nothing to arbitrate. **Predicted, not assumed — C13 and §9 row 7(e) confirm it on the in-band vertical drag (§2.4, v3).** |
| (b) Require a vertical-dominant initial displacement | On the first `onChanged` where `hypot(dx,dy) ≥ 4`, latch `isVerticalDominant = abs(dy) > abs(dx)` into `@GestureState` for the whole drag. If `false`, the drag is **inert for its lifetime** — no track, no hour write, no hint change. |
| (c) Never claim a touch while a sheet is presented | The zone is **not in the view hierarchy** in that state (§2.4, §4.10). Strictly stronger than an `isEnabled` flag or a `.gesture` no-op. |

**Honest limit of rule (b), stated rather than glossed:** a horizontal-dominant drag starting inside the band is consumed by the overlay, so the map does not pan under it. (b) guarantees *no false hour change*; it cannot hand the touch back, because SwiftUI has already routed it. Handing it back is not achievable in either construction without a reference to MapKit's recognizer, which does not exist. The residual cost is the dead strip §2.4 names and §10 accepts. `qa` should check that such a drag leaves the hour and the camera both unchanged — that is the checkable promise.

**Rule (a) is checked directly, on the drag that matters [v3, `ios-code-reviewer`].** The inert-horizontal case above and the pan-starting-outside case (§9 row 7c) both leave rule (a) untested: the first expects no camera movement whether or not MapKit saw the touch, the second is a touch the zone never claimed. The case that actually exercises (a) is a **vertical, in-band drag** — the normal gesture — where the hour is expected to change and the camera is expected not to. C13 and §9 row 7(e) require `camera`/`MKCoordinateRegion` to be byte-identical from touch-down through `onEnded`, sampled at least at the drag's start, mid-point and end, using the same comparison §9 row 2c already uses for the button path. Not a "the map looked still" observation — the same recorded-value comparison, on device or in a UI test.

**Also consumed: taps inside the strip.** `minimumDistance: 4` means a tap never becomes a drag, and the overlay swallows it, so a Hood or pin whose only visible part is inside the 24pt strip cannot be tapped there. `qa` verification: a drag in the band must not also fire `MapScreen.handleTap` and open a Hood sheet mid-drag (`SpatialTapGesture` via `.simultaneousGesture` is greedy; it is attached to `Map`'s own subtree, which the overlay is not part of, so this should hold by construction — confirm it, do not assume it).

On `onEnded`: clear `activeDrag`, leave `selectedHour` where it landed, restore the hint. **No commit gesture, per req 7.**

Haptics (P1): `.sensoryFeedback(.selection, trigger: selectedHour)` on the zone — one line, fires on every hour crossing from either path. Ship it if it costs nothing; drop it without a second thought if it complicates anything.

### 4.9 Edge geometry — the 64pt/40pt insets, confirmed **[D8]**

```swift
enum EdgeGeometry {
    static let captureWidth: CGFloat = 24     // Q7, ratified 2026-08-02
    static let topFloor: CGFloat = 64
    static let bottomFloor: CGFloat = 40
    static let hintSize = CGSize(width: 5, height: 56)

    static func band(in size: CGSize, safeArea: EdgeInsets) -> ClosedRange<CGFloat>
    static func hour(atY y: CGFloat, in band: ClosedRange<CGFloat>) -> Int   // clamped 0...12
    static func y(forHour hour: Int, in band: ClosedRange<CGFloat>) -> CGFloat
}
```

**The design's numbers are confirmed, and the construction is changed so they stay correct off the reference device.** Checked against real iOS geometry rather than accepted from the spec, which is what design §8 item 7 asked for:

- Top: the largest top safe-area inset on any current iPhone is **59pt** (Dynamic Island, iPhone 14 Pro family onward); notch devices are 47pt or 44pt. Notification Center and Control Center are pulled from within that same top region. `64 = 59 + 5pt` clearance — the design's number is exactly right for the worst current case, with a small margin.
- Bottom: the home-indicator safe-area inset is **34pt** on every Face ID iPhone. `40 = 34 + 6pt` clearance. Also right.

Because both numbers are the worst-case inset plus a clearance, hardcoding them is correct today and silently wrong on any future device with a larger inset. So `band(in:safeArea:)` computes:

```
top    = max(topFloor,    safeArea.top    + 5)
bottom = max(bottomFloor, safeArea.bottom + 6)
band   = top ... (size.height - bottom)
```

On an 812pt reference device this yields exactly the design's 708pt band and ~59pt per stop, so every arithmetic figure in the design spec and the mockup remains valid. On a device with a smaller inset (iPhone SE, 20pt top) the floors hold the band identical to the design. On a larger one it grows automatically.

`hour(atY:in:)` maps **absolute position, not delta** — this is what makes req 1's widened bullet ("all 13 reachable wherever the finger lands") true by construction rather than by tuning. Up is later: `hour = round((band.upperBound - y) / band.length × 12)`, clamped to `0...12`. One function, called by both edges against their own bounds, so req 7's "identical from both edges" is structural (design §7's own argument, adopted). The value clamp lives here; the track's drawn extent and the readout chip's position are clamped separately to the band so the chip stays pinned at the end rather than floating past it.

**Dynamic Type:** the band and stop spacing are pure geometry and do not reflow with type size, so req 1's "at the largest supported Dynamic Type size" is satisfied structurally on this path. Only the readout chip's text scales; its container is sized to content so it cannot clip. Req 1's Dynamic Type bullet on the *button* path was already verified in the design's own v1 pass.

**Smallest supported band, checked:** the shortest current iPhone in portrait is 667pt (SE). `667 - 64 - 40 = 563pt`, ~47pt per stop — still above the 44pt reference the design used. No device in portrait falls below it.

### 4.10 Which edges are live **[D9]**

```swift
enum EdgeAvailability {
    static func liveEdges(
        idiom: UIUserInterfaceIdiom,
        isPortrait: Bool,
        isAnySurfacePresented: Bool,
        isAnySheetPresented: Bool
    ) -> Set<HorizontalEdge>
}
```

Pure, exhaustively unit-testable, and the single place this policy lives — no view re-derives it.

| Condition | Live edges |
|---|---|
| iPhone, portrait, nothing presented | `[.leading, .trailing]` (Q2) |
| **iPhone, landscape** | `[]` — **new call at v2, D9** |
| iPad, nothing presented | `[.leading]` — right edge is system Slide Over, permanently excluded (Q2) |
| Any sheet presented (`detailRouter.isDepth1Presented`) | `[]` (Q6 — zone leaves the hierarchy, §2.4) |
| Any nav surface presented (`MapChromeState.isPresenting`) | `[]` |

**The sheet row is one flat rule, but the behaviour it falls back to is not one behaviour [added at v3, `ios-code-reviewer`].** Collapsing *any* presented sheet to `[]` is correct and is Q6's call — the zone leaves the hierarchy regardless of detent, and nothing here changes that. What is not single-valued is what the touch then does instead, and PRD req 7's "an edge drag over a presented sheet moves the sheet, as it does today" reads as one behaviour when the shipped code has two. Verified at source, not inferred:

- `MapScreen.swift:186` — `.presentationBackgroundInteraction(.enabled(upThrough: .medium))`. The still-exposed map above the sheet is interactive at `.medium` and **inert at `.large`**.
- `HoodSheet.swift:26` — `.presentationDetents([.medium, .large])`, so both states are reachable.
- `PlaceDetailModal.swift:22` — `.presentationDetents([.medium])` only, so `.large` is reachable through the Hood sheet alone.

So "as it does today" covers four combinations, not one: {`.medium`, `.large`} × {touch on sheet content, touch on the still-exposed map}. §9 row 7(d) and C13 exercise all four explicitly. **No code in this feature changes as a result** — this is verification granularity, not a design change, and `EdgeAvailability` keeps its one flat rule.

**Why landscape is excluded, since no upstream doc considered it.** The app supports all three orientations (`project.pbxproj:367`), and the design reasoned entirely about an 812pt-tall portrait reference device. In landscape:

- The sensor housing sits on a *long* screen edge. On a Dynamic Island iPhone in landscape the horizontal safe-area inset on that side is 59pt — the physical edge where the capture zone would live is under the housing, unreachable and partly invisible. The "an edge-anchored target cannot be overshot past the bezel" argument that Aviran ratified at Q7 does not survive there.
- The usable band drops to roughly 289pt (393 − 64 − 40), about 24pt per stop — below every figure the design and this TRD reason from.
- Nothing is lost: req 6's own bullet already guarantees all 13 hours from the heat button, which works identically in any orientation.

Hiding the hint (rather than drawing the iPad ghost mark) is right here because the *whole gesture* is off in landscape, not one edge of two — a ghost mark on both edges would explain an absence the user has no reason to expect. **Cheap for `designer` or `product` to overturn**: it is one row in one pure function, and `qa` can check it in a rotation.

### 4.11 The idle hint and the active track **[Q8]**

```swift
struct EdgeHint: View { let edge: HorizontalEdge; let band: ClosedRange<CGFloat> }
struct EdgeHourTrack: View { let state: EdgeDragState; let band: ClosedRange<CGFloat>; let readout: HourFormat.Readout }
```

Q8 is ratified: the hint is deliberately persistent chrome, an explicit exception to the PRD's "not permanent chrome" line. Build it as specced and do not treat the tension as unresolved.

- **`EdgeHint`** — 5pt × 56pt capsule, vertically centred in the band, **opacity 1.0**, opaque `Color("Surface")` with a 1pt inner mark in `Color("MutedOnSurface")`. Opaque, never translucent over a live map, for the same reason T-031 §8 D1 gave: a ratio against unknown map pixels is not a number anyone can verify. Rendered once per live edge; hidden while a drag is active (the track replaces it), and absent whenever `liveEdges` excludes that edge. `.allowsHitTesting(false)` — the 24pt zone owns every touch; the 5pt hint is purely visual. Fade honours Reduce Motion.
- **iPad right edge** draws a faint neutral ghost mark instead of a hint, so the absence reads as "OS-reserved" rather than as a missed build (design §3).
- **`EdgeHourTrack`** — custom-drawn vertical control: 13 stops, a "now" tick at the range end that means now, and the floating readout chip beside the finger. It draws its **own opaque `Surface`-backed panel**, so every contrast figure is priced against a background this app actually draws.
- **Both are `.accessibilityHidden(true)`.** The edge path is a supplementary raw-pixel gesture; narrating it would be worse than not exposing it, and req 6's assistive-tech bullet is satisfied entirely by the button path (design §4). This is a deliberate exception to the app's semantic-first default and is stated here so `ios-code-reviewer` does not read it as an omission.

### 4.12 Colour tokens and the contrast rule

PRD req 6 says "**every** text label rendered on the surface housing this control… There is no enumeration exception." A test cannot enumerate labels that do not exist yet, so the invariant moves into the construction:

> **Every text label inside `HeatModal/` and `EdgeHour/` renders with exactly one foreground token, `MutedOnSurface`, on exactly one of two backgrounds: `Surface` or `PillSurface`.** Hierarchy comes from type size and weight, never from a second colour.

That turns an unenumerable claim into four executable assertions ({token} × {2 backgrounds} × {light, dark} ≥ 4.5:1), covering any future label on these surfaces the day it is written. `ios-code-reviewer` treats a second foreground colour in either folder as a blocking finding.

- **`PillSurface` is an opaque colour set**, not the mockup's `color-mix(--heat 14%, transparent)` — the pre-flattened equivalent of the design's own ~5.09:1 light / ~6.01:1 dark figures.
- **Non-text (3:1), asserted:** `NowTick` vs `Surface`, `SliderFill` vs `Surface`, and — new at v2 — **`EdgeRail` vs `Surface`**. The edge track is custom-drawn, so req 6's inactive-rail exemption does not transfer to it (PRD Q5's consequence, design §4). `EdgeRail` exists as its own token precisely so the exempted native rail and the non-exempt custom rail cannot accidentally be the same colour — which is the exact defect the design's own fix pass found (`--surface-3` on both, 1.29:1).
- **Explicitly not asserted:** the native `Slider`'s thumb and inactive rail. The PRD exempts the rail; the thumb is the same category — an unmodified platform-drawn part, where WCAG 1.4.11's author-modification boundary falls. Going custom to control those pixels would cost the discrete VoiceOver adjustable action req 6 depends on (D5). **The test must not be "helpfully" extended to those two pairs** — it would fail against the control the PRD requires.
- `SliderFill` is deliberately **not** `HeatFill`: reusing the heat hue would couple the slider's contrast tuning to the heat palette T-031 req 4 locks.

Test lives beside T-031's, reusing `Support/ContrastRatio.swift` and the same resolve-against-the-real-catalog pattern (`UIColor(named:in:compatibleWith:)` under both `UIUserInterfaceStyle`s) — never hardcoded hex.

---

## 5. Flow

```
Path A — heat button
  tap → MapChromeState.toggle(.heat)
      → refreshIfHourRolled()          re-anchor if the wall clock rolled (§4.5)
      → edge zones + hints leave the hierarchy (§4.10)
      → scrim in; bucket-2 chrome out; nav row stays lit and hit-testable
      → HeatModalCard slides in above the nav row, at this session's hour

Path B — edge slide (portrait iPhone / iPad left; nothing presented)
  touch down inside the 24pt zone
      → refreshIfHourRolled()          same re-anchor (§4.5)
      → first movement ≥4pt latches vertical-dominance; horizontal → inert drag, no write
      → hint hides, EdgeHourTrack + readout chip appear
      → every move: EdgeGeometry.hour(atY:) → selectedHour           ── absolute, clamped
  lift → track and chip disappear; hour holds for the session. No commit gesture.

Both paths converge on the one write:
  selectedHour set
      → HeatRepaintSignpost.begin()
      → @Observable invalidation → MapScreen body
          → HeatComposition.fills(hoods:hour:band:) → HeatRepaintSignpost.endIfPending()
          → HoodLayer re-evaluates foregroundStyle per polygon
      → the readout (numeral + "next day" pill) updates from the same value
  camera, zoom, geometry, polygon identity: untouched. No fetch. No sheet involved (D4).

Exit (path A): swipe down · scrim tap · another nav button
      → MapChromeState mutates; selectedHour untouched (PRD req 4)
```

Cold launch: `DensityStore()` initialises `selectedHour = 0` and `anchorHour` from the real clock. Nothing is read from disk, so "now" cannot be stale (req 3, §4.6).

Empty / offline hours are a non-event: `band(for:hour:)` returns `nil`, `HoodLayer` applies no fill, and no banner or modal appears. That is T-031's rendering rule, inherited, not re-implemented.

---

## 6. Third-party / dependencies

**None added.** No package, no account, no cost, nothing Aviran-gated. `Slider`, `DragGesture`, `GeometryReader`, `os_signpost`, `Calendar` and `.sensoryFeedback` are all platform. `passenger-code/README.md`'s "no third-party packages until a TRD justifies one" stays intact.

**Salvage:** `SALVAGE.md` marks `Models/HeatTimeWindow.swift` REUSE and `Features/Map/HeatmapControlsSheet.swift` REFERENCE. The archive is **not reachable from this workspace** (`~/APE Studio/locali` is absent — the same access gap T-031 hit). It is also largely moot: the hour-windowing model REUSE points at is already re-derived and shipped in `DensityStore` (`anchorHour` + `0...12` offset over absolute UTC hours), a stricter design than an hour-of-day window. `ios-developer` should not block on salvage access.

---

## 7. Rollout & migration

- **No feature flag.** The button is reachable only from chrome this same task adds; the off-state of a flag would be a nav row with nothing in it. The edge path's own kill switch already exists and is better than a flag: one row in `EdgeAvailability.liveEdges`.
- **No migration, no backend deploy, no Aviran-gated apply step.** Nothing in §11 touches `database/`.
- **No backward compatibility surface.** No persisted state exists to read forward or backward, by design (§3.1).
- **Build Phase 1 → Phase 2 is one constant.** Flipping `BuildPhase.seedIsAuthoritative` to `false` is the entire wiring change (§3.4), exactly as `BuildPhase.swift`'s own comment describes for `PlaceCatalog`. Both branches stay compiled and reviewable through Phase 1. **Phase 2 must re-run req 2's three data-dependent bullets against the live feed** — Phase-1 acceptance covers them against the seed only, and this TRD does not claim otherwise.
- **Ships independently of the backend.** With no `SupabaseConfig.plist`, the modal opens, both paths move the hour, and the map repaints against the seed. Demoable and testable before migration `001` is ever applied.
- **Dependency direction:** T-034 reads `selectedHour` and adds a row to `HeatModalCard`. T-036/T-037/T-038 add their own `NavSurface` views and their own buttons to `MapNavRow`. None of them need to change anything this task writes.

---

## 8. Decisions and ratified deviations

T-031 set the precedent: a deviation from an approved artifact is recorded and justified here, not silently built. D1–D6 are v1's and stand unchanged; D7–D10 are new at v2.

### D1 — The nav row ships with one button, not three
`ux-flows.md` §2 and the mockup show three or four nav buttons. **None exist in the shipped app**, and neither search (T-038) nor Profile (T-037) nor Places (T-036) has a TRD. This task builds `MapNavRow` as the container plus **the heat button only**. A rendered button that opens nothing fails at the Functional tier before it can be judged on anything else (`design-principles.md` §1), and a dead control in shipped chrome invites exactly the "is the app broken?" read this map cannot afford. The row is laid out so **Search and Profile** slot in without re-layout — **Places is bucket-2 chrome, separate from the nav row, per T-036's D7** (`ux-flows.md` §2/§2.1, confirmed word-for-word by two independent `trd-review` reads); this line previously named "the rest" ambiguously and was corrected 2026-08-02 once T-036's TRD made the distinction concrete. **Consequence:** the near-me cluster moves up out of the nav row's band (§2.3).

### D2 — Custom `ZStack` overlay, not `.sheet()`
Settled shape: a SwiftUI layer inside `MapScreen`'s `ZStack` at z5, below `MapNavRow` at z7, with an explicit scrim at z3. Not `.sheet`, not `.fullScreenCover`, not a `UIViewControllerRepresentable`, and not `.presentationBackgroundInteraction` (there is no presentation). The nav row must stay hit-testable or `ux-flows.md` §2.1's direct nav-switch requirement fails; that is the entire reason for the deviation.

### D3 — "Now" re-resolves on invocation, not on a timer
Re-anchor on modal open **and on edge touch-down**, reusing T-031's `refreshIfHourRolled()`, with no repeating timer. Staleness only becomes visible when the user reaches for the control, and there are now exactly two ways to reach it — a check at each is both sufficient and free. A wall-clock timer would burn a scheduled wake to correct a label nobody is reading and could move the thumb under a live finger. With T-031's `scenePhase → .active` hook, the three triggers cover every path by which a user can observe the value.

### D4 — The shipped modal contains the slider only
The mockup renders stub toggle rows and a repaint-timing pill; the design spec labels them mockup instrumentation. **None ship.** The heat layer has no on/off toggle in V1, so a row saying so explains an absent feature; the live-events toggle is T-034's; the timing pill becomes the `HourRepaint` signpost (§4.7), which has no UI.

### D5 — Native `Slider` on the button path, custom control on the edge path
Native `Slider(step:)` plus a non-interactive overlay for the modal; a fully custom vertical control for the edge (no native vertical `Slider` exists). The consequence is §4.12's: the native thumb and inactive rail are platform-drawn and outside this app's authored contrast surface, while the custom edge rail is inside it and gets its own `EdgeRail` token. Going custom on the button path too would trade a P0 (discrete VoiceOver stepping) for a bar the PRD already exempts the native rail from.

### D6 — Separate side-by-side icons, glyph `flame.fill`, icon-only (no text caption)
Each nav icon is its own independent button, side by side, no shared container chrome. Provenance: Aviran, verbatim *"yes, separate icons, same switching behavior,"* relayed via `chief-of-staff` (`PROGRESS.md`, 2026-07-31), reconfirming his earlier *"I don't want a nav row. I want separate icons side by side."* Two relays of that answer exist and are deliberately not merged into one quote (L-013); the decision above is the part both support.

**Icon-only, added 2026-08-02, founder-direct:** the heat button renders `Image(systemName: "flame.fill")` alone — **no `Label`, no visible text string beside or beneath the glyph.** Aviran, live hilos `@chief` chat, verbatim *"remove the name from the icons in the nav bar, show only icons"* (`PROGRESS.md`, 2026-08-02 FOUNDER-DIRECT STUB). Carries no behavior change and touches no accessibility surface — `.accessibilityLabel` still names the button for VoiceOver exactly as any icon-only control in this codebase already does (`NearMeButton`'s precedent, cited above). `ios-developer`: build this button as icon-only from the start; this is not a strip-the-caption-later instruction, there was never a caption in the build target to begin with. Search (T-038) and Profile (T-037) inherit the same icon-only rule for their own buttons in this same `MapNavRow` container once they're built — recorded centrally in `design/ux-flows.md`'s 2026-08-02 addendum, not duplicated per-task.

**Visual only; no behaviour is touched** — exclusivity, the z-order table, the never-covered guarantee, and the three dismissal paths all stand.

**Glyph, closed at v2:** `Image(systemName: "flame.fill")`, pinned by `designer` 2026-08-02 (founder-direct *"change the heat icon to flame"*), reasoned against the app's own vocabulary — `NearMeButton` rests at `location.fill`, the same default-to-`.fill` precedent for a circular chrome button, and "modal open" is already carried by the button's background so a glyph swap would be a redundant second channel. This closes the gap v1's D6 flagged. **Still open and still an engineering default: [ASSUMPTION]** background shape, material and spacing follow the existing `NearMeButton` floating-chrome idiom (`.frame(44×44)`, `.background(.thinMaterial, in: Circle())`) — the only bottom-chrome idiom the shipped app has. Cheap to overturn: one button, one file.

### D7 — Edge gesture is a SwiftUI `DragGesture` on a hit-testable overlay **[new, v2]**
Settles design §8 item 6 and PRD open technical question (b). Full reasoning in §2.4 and §4.8. The short version: the UIKit route would exist to arbitrate against MapKit's pan recognizer, SwiftUI's `Map` gives no access to that recognizer, so the arbitration cannot be established — and hit-test order makes it unnecessary anyway. **This corrects the design spec's stated mechanism** (§2, §7, §8 there describe the 24pt zone as needing to win arbitration). The 24pt number is unchanged and Q7 is not reopened: its acquisition argument, which is what Aviran ratified, is untouched. Two costs are accepted rather than hidden: the strip is undraggable and untappable map (§2.4), and a horizontal drag starting in the strip is consumed without panning (§4.8). The gesture uses `DragGesture`'s **default `.local` coordinate space**, not a named one (§4.8, corrected at v3).

**This decision ships with a required confirmation, not on reasoning alone [v3].** "MapKit's pan recognizer is never in that touch's recognizer chain" is a prediction from documented hit-test ordering, and `FB19394663` — cited in this same TRD — is a filed case of SwiftUI `Map` not matching that class of reasoning. **§9 row 7(e) and C13 make it falsifiable on the in-band vertical drag**, the only case that exercises it: `camera`/`MKCoordinateRegion` byte-identical throughout, on device or in a UI test. If it fails, D7's construction is what changes and the fallback is a product conversation about the edge path (there is no third construction that arbitrates, because there is no recognizer to arbitrate against) — which is precisely why it must fail at C13 rather than in the field.

### D8 — 64pt / 40pt confirmed, and re-derived so they hold off the reference device **[new, v2]**
Settles design §8 item 7. Both numbers are correct: 64 = 59pt (largest current top safe-area inset, Dynamic Island) + 5pt; 40 = 34pt (home indicator) + 6pt. They are hardcoded worst-case values, so `EdgeGeometry.band(in:safeArea:)` computes `max(floor, safeAreaInset + clearance)` instead — identical output on every current device, automatically correct on a future one. The design's 708pt / ~59pt-per-stop arithmetic is preserved exactly on an 812pt device, and the shortest current portrait iPhone (667pt) still gives ~47pt per stop.

### D9 — The edge path is portrait-only on iPhone **[new, v2]**
No upstream doc considered orientation; the app ships all three (`project.pbxproj:367`). In landscape the sensor housing occupies a long screen edge (59pt horizontal safe-area inset on Dynamic Island devices), so the capture zone would sit under the housing and Q7's "cannot overshoot past the bezel" argument does not hold; the band also drops to ~24pt per stop. The button path is unaffected and req 6 already guarantees every hour through it, so nothing is lost. One row in one pure function (§4.10) — cheap for `product` or `designer` to overturn, and `qa` can check it with a rotation.

### D10 — A bundled density seed ships in this task **[new, v2]**
Full reasoning in §3.4. Without it, Build Phase 1 renders every Hood empty at every hour and three of PRD req 2's four bullets have nothing to observe. Follows T-033's shipped `BuildPhase.seedIsAuthoritative` pattern exactly rather than inventing a second mechanism, and stores **relative** offsets so the demo is correct at any launch date. **Flagged for `product` at `trd-review`** — it adds a data artifact to a PRD whose Technical design says "nothing to source or author," and that confirmation should be explicit.

---

## 9. Verification — one row per P0 requirement

Per `architect.md` (L-018): every P0 requirement names a falsifiable check with an observable, a pass condition, and the layer it is checked at. `qa` builds `prds/time-slider/TEST-PLAN.md` from this table. **No row's pass condition is "looks right."**

**And no row's pass condition is a value handed to the renderer.** A requirement is verified at the layer the user perceives it. `HeatModalCard`'s padding constant is an *input* to layout; the check belongs on what the two views' frames actually did — which is the whole of row 5b below.

**Three standing rules for this table.** The first two are lifted verbatim in substance from the `search-quick-filters` TRD §9 (T-053, 2026-08-03), where they were written after a row passed while its requirement failed; they are restated here rather than cross-referenced because `qa` reads this table on its own. Both are about conditions that are *true for the wrong reason*:

- **No pass condition may be satisfiable over an empty set.** "Every X has property P" is worthless without a stated non-zero count of X, because the failure being guarded against is usually "no X was produced at all." A geometric non-intersection check is the sharpest case: two frames that never rendered do not intersect either.
- **Every negative-existence check needs a positive control.** "No overlap", "no truncation", "grep → 0 hits" all pass identically when the thing under test was never produced. Each such check names, alongside it, something that **must** be present; if the positive control is absent, the row is **unrun, not passed**.
- **Rendered-result rows are run on a rendered app.** Rows 5b and 6(c) cannot be discharged by a source read, by `XCUIElement.exists`, or by a "PASS by construction" note — `exists` is `true` for a fully occluded element. If the environment blocks the run, the row is **BLOCKED**, and BLOCKED is reported as unrun.

**Scope note, so this is not read as more than it is.** Rows 1–7 were written at v2/v3 and have **not** been re-audited against the three rules above in this v4 pass — the pass added row 5b only. Whether these rules become workspace-wide (`architect.md`) rather than per-TRD is `retrospective`'s call, not settled here.

| P0 | Observable | Pass condition | Layer | Step |
|---|---|---|---|---|
| **1** Range now → +12h, hour-snapped, clamped, reachable from any touch-down point | `EdgeGeometry.hour(atY:in:)` over a swept `y`; `Slider` binding's `set` | Exactly 13 distinct outputs across the band; `y` above/below the band returns 12/0, never 13 or −1; every output is an `Int`; sweeping from any start `y` to either band end reaches 0 and 12 | unit | C4, C11 |
| **2** Map repaints for the hour; camera/zoom unchanged; <400ms; silent-empty | (a) `HeatComposition.fills` output for two hours over the seed; (b) `XCTOSSignpostMetric` on `HourRepaint`; (c) `camera` after a full-range drag; (d) a Hood with a `null` seed hour | (a) `[HoodFill]` differs for two hours and is identical for the same hour; (b) p90 < 400ms driving `hourSlider` through `adjust(toNormalizedSliderPosition:)`; (c) `MKCoordinateRegion` byte-identical before/after; (d) `band == nil` → `.clear` fill, no banner, no modal | unit + UI test + manual | C6, C7, C10 |
| **3** "Now" every cold launch, re-resolved against the real clock | A fresh `DensityStore(now:)` with an injected clock | `selectedHour == 0` and `anchorHour == hourFloor(injectedNow)`; grep of the diff finds no `UserDefaults`/`AppStorage`/file write of the hour | unit + review | C8 |
| **4** Session persistence across every dismissal path | `MapChromeState.toggle(.heat)` → `toggle(.search)` → `toggle(.heat)`; and set-by-edge → read-by-button | `selectedHour` unchanged across the switch; the value set by an edge drag is the value the modal shows, and vice versa | unit + manual | C2, C11 |
| **5** Hour readable as a number; explicit "now" mark; never colour alone | `HourFormat.readout` strings; the rendered "now" mark | `offsetLabel` is non-empty at all 13 offsets; "Now" at 0; a midnight-crossing case sets `isNextDay`; the "now" mark differs from an ordinary stop in **shape**, verified with the colour catalog forced to greyscale | unit + manual | C3, C5 |
| **5b** The readout renders **unoccluded** — §2.3's z5 rule made checkable. PRD v9 req 5's rendered-legibility bullet; **new at v4, T-055** | With the heat modal presented: (a) at the **default** text size, the rendered frames of `HeatModalCard`, of `MapNavRow`, and of the three readout elements individually — offset numeral, clock label, "next day" pill; (b) the identical capture at **AX5** (`UICTContentSizeCategoryAccessibilityExtraExtraExtraLarge`) — the card is *sized to content* (§2.3 z5), so its height is a function of text size and a default-size gap says nothing about the AX5 one; (c) the rendered `label` of the pill and of the numeral in each capture, at an hour where `HourFormat.isNextDay` is `true` (e.g. +12h from 23:00) | **Counts and non-emptiness first, then the geometry.** All five elements exist and each reports `frame.width > 0` **and** `frame.height > 0`, with the values recorded — two frames that never rendered satisfy every non-intersection claim below, and that is the exact way this row could pass while the requirement fails. Any zero-sized frame → the row is **unrun, not passed**. Then, **in each of the two captures independently**: (i) `HeatModalCard.frame.intersects(MapNavRow.frame) == false`, and stronger, `MapNavRow.frame.minY − HeatModalCard.frame.maxY ≥ 8pt` — a separation a person can see, not a hairline; (ii) the same non-intersection asserted **separately for each of the three readout elements** against `MapNavRow.frame`, because the card can clear the nav row while a pill drawn at its edge does not; (iii) `HeatModalCard.frame.maxY` is strictly less than the safe-area bottom — `bottom: 0` is what §2.3 forbids by name, so it is falsified directly rather than inferred from the gap. **Positive control** (standing rule 2): in the same capture the pill's `label` reads `"next day"` in full and the numeral reads `"+12h"` in full. **This control does not detect the occlusion and must not be read as if it did** — `XCUIElement.label` returns the whole string for a fully covered `Text`, which is precisely why F1 survived `qa`. Its only job is to prove the elements rendered at all, so that (i)–(iii) are claims about something. If the pill is missing at an hour where `isNextDay` is `true`, the row is unrun. **[ASSUMPTION] on the 8pt floor:** §2.3 requires the anchor distance be *fixed and non-zero* and names no number; the constant is `ios-developer`'s at build. If a different fixed distance is chosen deliberately, this floor moves to it — what may not move is that the gap is fixed, positive, and asserted | **UI test on a rendered app** (or on-device with frames read from the accessibility hierarchy). **Not** unit, **not** source review, **not** `exists` — none of the three can see an overlap, and all three passed this build. Blocked environment → **BLOCKED**, reported as unrun | **C2, C5** — C2 wires `MapNavRow` in at z7, C5 builds the card and readout; each owns half of a relationship neither one alone can check, which is why no build step caught it. Build note, not a contract change: both views need an `.accessibilityIdentifier` for their frames to be queryable — add it in whichever step lacks it |
| **6** VoiceOver discrete steps; ≥44pt on the button path; Dynamic Type; contrast | (a) VoiceOver swipe on `hourSlider`; (b) the `Slider`'s frame height; (c) rendered readout at `AX5`; (d) `ContrastRatio` over the token pairs | (a) one hour per swipe, value spoken; (b) ≥44pt; (c) no clipping or truncation; (d) `MutedOnSurface` on `Surface` and on `PillSurface` ≥4.5:1, and `NowTick`/`SliderFill`/`EdgeRail` on `Surface` ≥3:1, all in both `UIUserInterfaceStyle`s — and the native thumb/rail are **not** asserted (§4.12) | unit + manual | **C4** (the ≥44pt frame), C9, C12 |
| **7** Edge slide: both live edges, vertical-only, one shared value, no false fire, **camera untouched by the normal drag**, inert under a sheet | (a) `EdgeAvailability.liveEdges` over the full input matrix; (b) a horizontal-dominant drag inside the band; (c) a pan starting outside the band; **(e) a normal vertical, in-band drag on each live edge, full band travel — `camera` sampled at touch-down, mid-drag and `onEnded`**; (d1) an edge drag with `HoodSheet` at `.medium`, on sheet content **and** on the still-exposed map; (d2) the same at `.large` | (a) matches §4.10's table exactly, every row; (b) `selectedHour` and `camera` both unchanged; (c) the map pans normally, no track appears; **(e) `selectedHour` moves across all 13 stops and `camera`/`MKCoordinateRegion` is byte-identical at all three samples — same comparison method as row 2c. This is the check for D7/§2.4's central claim; a drift or jump here fails the row, and no other sub-check can substitute for it**; (d1)/(d2) no track appears and `selectedHour` is unchanged in both, and the sheet behaves exactly as it does today for that detent — noting `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` (`MapScreen.swift:186`) means "as today" is **two** behaviours: at `.medium` the exposed map is background-interactive, at `.large` it is not | unit + **UI test or on-device for (e)** + manual | C11, C13 |

**Two carried-forward bullets, called out.** `product`'s T-031 acceptance found req 2's *repaints on hour change* and *<400ms* had zero traced test cases and assigned them to T-032's `qa`/`acceptance`. Row 2 above is that assignment discharged — with the seed (D10) as the precondition that makes either checkable at all. `qa` must show a real case in the trace column for both, not a "PASS by construction" note; that distinction is precisely what `product` caught at T-031.

---

## 10. Risks and alternatives

| Risk | Mitigation / decision |
|---|---|
| The 24pt strip at each edge is undraggable, untappable map — ~12% of an iPhone's width | Accepted, and now stated with its real mechanism (§2.4, D7) rather than as an arbitration cost. `qa` checks that a pan starting outside the band behaves normally. If it proves intolerable in use, the lever is the width constant, and widening or narrowing it re-opens Q7 with Aviran, not in a build. |
| **D7's hit-test prediction is wrong and MapKit pans under every ordinary edge slide** — the map jumps or drifts under the finger on this feature's primary gesture, a visible regression against T-031's shipped camera behaviour **[added at v3, `ios-code-reviewer`]** | The claim is now labelled a prediction, not a settled fact (§2.4, D7), and made falsifiable at the earliest point it can be: **§9 row 7(e) / C13 item 1** check `MKCoordinateRegion` byte-identity through an in-band *vertical* drag, on device or in a UI test. v2's checks could not have caught this — an inert horizontal drag and a pan outside the band both pass whether or not MapKit saw the touch. If it fails, there is no third construction to fall back to (`Map` exposes no recognizer to arbitrate against), so the fallback is a product conversation about the edge path — which is why C13 is defined as not-done until this passes, rather than leaving it to `qa`. |
| A horizontal drag starting in the strip is consumed without panning the map | Named honestly (§4.8). (b)'s vertical-dominance latch guarantees no false hour change, which is the checkable promise; handing the touch back is not achievable in either construction, since SwiftUI's `Map` exposes no recognizer to defer to. |
| `SpatialTapGesture` on `Map` also fires during an edge drag and opens a Hood sheet | Should hold by construction (the gesture is in `Map`'s subtree, the overlay is not) — **confirm, do not assume**; C13 and §9 row 7. |
| The Build-Phase-1 seed makes the feature look verified when only the seed path is | §7 states plainly that Phase-2 acceptance must re-run req 2's data-dependent bullets against the live feed. The seed is named in §3.4, in `Source.seed`, and in the build step — never invisible. |
| The seed is authored without hour-to-hour variation, so C6 and `qa` pass vacuously | §3.4 states the authoring rule as a requirement (≥3 Hoods changing band across ≥4 adjacent hour pairs, ≥1 `null`), and C10 is the step that owns it. |
| SwiftUI re-renders every polygon on an hour change and misses 400ms | Polygons keep stable `Hood.id` identity; only `foregroundStyle` re-evaluates, over dozens of shapes. Measured, not assumed (§9). Fallback is caching resolved `ShapeStyle` per band — local, not architectural. |
| The `HourRepaint` signpost measures resolution, not pixels | Stated plainly in §4.7 rather than claimed as end-to-end, backed by the structural no-fetch guarantee and a perceptual check at `qa`. Same posture T-031 took on `XCTApplicationLaunchMetric`. |
| Custom overlay reimplements sheet behaviours badly | The behaviours are small and enumerated (§4.2); the alternative is unusable, since `.sheet` covers the nav row and breaks the nav-switch rule (D2). |
| Landscape exclusion (D9) is an architect call no upstream doc made | Flagged as such, with its reasoning, and made trivially reversible (one row, §4.10). Named for `product`/`designer` at `trd-review`. |
| The nav row ships with one button and reads as unfinished | D1 — deliberate, reversible, preferable to a dead control. |
| Req 2's "any open sheet is unchanged by an hour change" is unexercisable | The two can never be co-presented (D4, Q6, §2.3), so the bullet is satisfied structurally rather than behaviourally. **Flagged rather than quietly passed** — if `product` intended them to coexist, that is a product change, not something this TRD should invent. Cross-check against T-033's TRD at `trd-review`. |
| Non-whole-hour timezones render a `:30` clock label | Cosmetic, P1 surface only, outside V1's single city. §3.2 `[ASSUMPTION]`. |
| Touching accepted T-031 code (`DensityStore`) | Three named changes in §4.5, each with its reason. T-031's existing tests must pass unmodified. |
| **A layering rule stated in §2.3 is not a rule any gate can fail** — the build bottom-anchors the card, the nav row draws over the readout, and `code-review`/`qa` both pass because neither renders the app **[added at v4, T-055, after it happened]** | Row 5b is that rule made falsifiable, on rendered frames, at both text sizes, with a positive control. The residual risk it does *not* cover: **the other four z5-shaped surfaces share the pattern** — `PassportSurface`, `PlacesListOverlay` (`.padding(.bottom, 8)`) and `SearchOverlay` (`.padding(.bottom, 4)`) all sit under the same 96pt nav row, found by source read at `product`'s acceptance and filed as **T-054** (`ios-developer`). Row 5b binds this TRD only; it does not and cannot verify three other PRDs' surfaces, two of them already accepted. |
| Synthetic density makes every future hour a simulation, not a forecast | Named in the PRD and strategy; unchanged here. Nothing in this TRD should be read as making the control more truthful than the data behind it — least of all the seed. |

**Alternatives considered and rejected:** a `UIGestureRecognizer` subclass for the edge path (D7 — the arbitration it would buy is unreachable); `.sheet(isPresented:)` for the modal (covers the nav row — D2); a fully custom horizontal slider (loses free discrete VoiceOver stepping, a P0 — D5); a repeating timer to re-resolve "now" (D3); persisting `selectedHour` across launches (contradicts req 3); a per-hour network fetch (would make the 400ms budget unachievable); hardcoding 64/40 as literals (D8); enabling the edge path in landscape against a housing-occluded edge (D9); shipping Phase 1 with no density data and calling req 2 satisfied by construction (D10); rendering three nav buttons with two inert (D1); asserting contrast on the platform-drawn thumb and rail (§4.12).

---

## 11. Build breakdown

Ordered. **Every step is `[iOS]`.** No `[Backend]`, no `[Algo/Data]` — see §1. C1–C9 are v1's, unchanged in scope; C10–C14 are new at v2.

| # | Step | Tag |
|---|---|---|
| C1 | `MapChromeState` + `NavSurface` (§4.1) | **[iOS]** |
| C2 | `MapNavRow` — heat button only (D1), `flame.fill`, separate side-by-side buttons with no shared container chrome (D6); wire into `MapScreen`'s `ZStack` at z7; move the near-me cluster above it; bucket-2 fade driven by `isPresenting` (§2.3). Exclusivity unit test incl. hour-survives-a-switch (§9 row 4) | **[iOS]** |
| C3 | `HourFormat` + tests — numeral, clock label, `isNextDay`, VoiceOver string; injected clock/calendar; midnight-crossing and 0/12 cases (§9 row 5) | **[iOS]** |
| C4 | `HourSlider` — native `Slider(in:step:)`, the `Double` bridge, ≥44pt frame, non-hit-testing tick overlay, a11y label/value/identifier (§4.3, §4.4) | **[iOS]** |
| C5 | `HeatModalCard` + scrim + three dismissal paths + Reduce-Motion-aware transition (§4.2); `HourReadout` (numeral + "next day" pill) | **[iOS]** |
| C6 | `HeatComposition.fills` + switch `MapScreen` to one resolution per pass; the differs-across-hours unit test (§9 row 2a) | **[iOS]** |
| C7 | `HeatRepaintSignpost` + the `XCTOSSignpostMetric` UI test and a `measure` unit test against the 400ms budget (§4.7, §9 row 2b) | **[iOS]** |
| C8 | `DensityStore`: the two new `refreshIfHourRolled()` call sites + the mid-`await` guard (§4.5 items 2–3); cold-launch-reset test (§9 row 3) | **[iOS]** |
| C9 | The five colour sets + the token-level contrast test, light and dark (§4.12, §9 row 6d) | **[iOS]** |
| **C10** | **`DensitySeed` + `density-seed-tel-aviv.json` + the `BuildPhase.seedIsAuthoritative` branch in `DensityStore.load()` and `Source.seed` (§3.4, §4.5 item 1).** Authoring rule enforced by a test: ≥3 Hoods change band across ≥4 adjacent hour pairs, ≥1 `null` hour exists. **Do C10 before C6/C7** — both are unverifiable without it | **[iOS]** |
| **C11** | **`EdgeGeometry` + `EdgeAvailability`, pure, with their full unit-test matrices** (§4.9, §4.10, §9 rows 1 and 7a). No view work in this step — the two hardest things to get right land first, testable with no simulator | **[iOS]** |
| **C12** | **`EdgeHint` + the iPad ghost mark** (§4.11); `.allowsHitTesting(false)`, `.accessibilityHidden(true)`, Reduce-Motion fade | **[iOS]** |
| **C13** | **`EdgeHourZone` — the 24pt overlay, `DragGesture` in the default `.local` coordinate space (§4.8, corrected at v3), the vertical-dominance latch, hierarchy-level removal under a sheet or a presented surface (§4.8, D7).** Verify, and **this step is not done until the first item passes** (§9 row 7): **(1) [v3, blocking] a normal vertical, in-band drag on each live edge, travelling the full band — `selectedHour` moves across all 13 stops while `camera`/`MKCoordinateRegion` stays byte-identical, sampled at touch-down, mid-drag and `onEnded`, compared the same way §9 row 2c compares it, on device or in a UI test rather than by observation.** This is the only check that exercises D7/§2.4's central hit-test claim; if it fails, stop and re-open D7 rather than working around it. (2) a horizontal drag in the band changes neither hour nor camera; (3) a pan starting outside the band pans normally; (4) a drag does not also fire `MapScreen.handleTap`; **(5) [v3] an edge drag with `HoodSheet` up, at `.medium` and again at `.large`, on sheet content and on the still-exposed map — four combinations, not one: no track appears and `selectedHour` is unchanged in all four, and the sheet behaves as it does today for that detent** (`.presentationBackgroundInteraction(.enabled(upThrough: .medium))`, `MapScreen.swift:186`, makes the exposed map interactive at `.medium` and inert at `.large`; `.large` is reachable via `HoodSheet` only — `PlaceDetailModal` is `.medium`-only) | **[iOS]** |
| **C14** | **`EdgeHourTrack` + the floating readout chip** — 13 stops, "now" tick, opaque `Surface` panel, chip position clamped to the drawn extent (§4.11); `.sensoryFeedback(.selection, trigger:)` for the P1 haptic | **[iOS]** |

**`trd-review` sign-off needed from: `ios-developer` + `ios-code-reviewer` only.** `developer`, `code-reviewer` and `data-engineer` have no step to review — this TRD writes no SQL, no RLS, no pipeline, and no algorithm. Two cross-checks worth one explicit pass at review: **T-033's TRD** against §2.3/§4.10/D4 (chrome layering, and the edge zone's interaction with `HoodSheet`'s drag-to-dismiss), and **`product`** on D10's seed and D9's landscape exclusion, both of which are architect calls that touch scope.
