# Hood & Place Detail + Hood Dataset — QA Test Plan (Build Phase 1)

**Tasks:** T-033/`PAS-13` (hood-place-detail) and T-040/`PAS-17` (hood-dataset), tested jointly — T-040's Build-Phase-1 slice (C1/C2/C2a) has no UI of its own and is only exercised through T-033's two sheets.
**Scope:** Build Phase 1 only — bundled seed authoritative (`BuildPhase.seedIsAuthoritative == true`), live Supabase fetch built but deliberately unexercised. Phase-1 acceptance covers `hood-place-detail.md` reqs 1–7 against the fixture; it does not cover the live path (TRD §4.3, §7).
**Checkout:** `passenger-code` HEAD `23dd6d5` (T-040's real geometry `72f4fc7` + T-033's full build `473f325` + fix pass `307e5af` + florentin blurb hand-edit `23dd6d5`, all landed together). Note: the dispatch brief named `a5351ed` as the pinned commit — that hash is actually a `passenger-brain` commit (the ios-code-reviewer fast-re-review record), not a `passenger-code` commit. `23dd6d5` is the tree that record approved (see report).
**Written before execution**, per L-018.

Each case traces to a PRD requirement (`PD-<feature>-<req>`) or a TRD contract/decision (`TRD-<feature>-<section>`). Verdict recorded per case at the end of the run.

---

## 1. Build-Phase-1 source pin (TRD-hpd-§3.4.1, §4.3)

| # | Case | Trace | Method |
|---|---|---|---|
| 1.1 | `PlaceCatalogTests` 3 determinism assertions pass (source==.seed; zero fetch attempts via spy; still .seed with populated plist fixture) | TRD-hpd-§3.4.1 | Unit test run |
| 1.2 | App launched fresh in simulator makes **zero** network requests during cold open + opening both sheets | TRD-hpd-§3.4.1, §4.3 | Network Link Conditioner / Instruments-equivalent (see report for method used) — behavioral, not just the unit test |
| 1.3 | Hood sheet and place modal render real bundled content with airplane mode / no network reachable | TRD-hpd-§7 "ships independently of the backend" | Manual, airplane mode |

## 2. Hood sheet blurb branch (PD-hpd-req2, TRD-hpd-§4.8)

| # | Case | Trace | Method |
|---|---|---|---|
| 2.1 | Open `florentin`'s Hood sheet — blurb text renders, no crash | PD-hpd-req2 bullet 1 | Manual |
| 2.2 | Open `kerem-hateimanim`'s Hood sheet — no blurb section, no placeholder copy, no gap artifact | PD-hpd-req2 bullet 3, TRD §4.8 row 1 | Manual |
| 2.3 | Open `neve-tzedek`'s Hood sheet — same, second no-blurb Hood | PD-hpd-req2 bullet 3 | Manual |
| 2.4 | `florentin`'s blurb is the only non-null blurb among all 24 bundled Hoods | TRD-hd-§8-D10, hand-edit scope | Static check (already independently verified by ios-code-reviewer; QA re-confirms) |

## 3. Place pins render inside real Hood boundary; tap resolves correctly (PD-hpd-req1/req3, TRD-hpd-§4.5, §4.3)

| # | Case | Trace | Method |
|---|---|---|---|
| 3.1 | All 9 bundled places' coordinates fall inside their stated `hood_id`'s real polygon | TRD-hpd-§3.4.1 quality floor | Independent point-in-polygon script (not trusting prior claims) |
| 3.2 | Visually, all 9 pins render inside their Hood's coloured shape on the map at appropriate zoom | PD-hpd-req1 (map stays visible), design spec §4 | Manual, simulator |
| 3.3 | Tap a pin in `florentin` → opens that place's detail modal directly (no two-step preview) | PD-hpd-req3 bullet 3 | Manual |
| 3.4 | Tap a pin in `kerem-hateimanim` → correct place modal | PD-hpd-req3 | Manual |
| 3.5 | Tap a pin in `neve-tzedek` → correct place modal | PD-hpd-req3 | Manual |
| 3.6 | Tap a Hood-sheet row → opens that place's modal at depth 2 | PD-hpd-req2 bullet 5 | Manual |

## 4. ✕ dismiss control, both sheets (PD-hpd-req1/req3, TRD-hpd-§4.1, §4.8)

| # | Case | Trace | Method |
|---|---|---|---|
| 4.1 | `HoodSheet` ✕ tap → `router.closeHood()` → sheet closes, map restored, camera/hour unchanged | PD-hpd-req1 bullet 3; regression from `6d0f157` review | Manual |
| 4.2 | `PlaceDetailModal` ✕ tap at depth 1 (opened from pin) → closes fully to map | TRD-hpd-§4.1 closePlace at depth1==full dismiss | Manual |
| 4.3 | `PlaceDetailModal` ✕ tap at depth 2 (opened from Hood-sheet row) → closes place modal only, Hood sheet still standing | TRD-hpd-§4.1, "exactly one level up" | Manual |

## 5. Swipe-to-dismiss, both sheets, no desync (TRD-hpd-§4.1 D9-item2, §11 C5)

| # | Case | Trace | Method |
|---|---|---|---|
| 5.1 | Swipe down `HoodSheet` → dismisses, `router.hood`/`place` both cleared (not just visually gone) | TRD-hpd-§4.1 isDepth1Presented.set(false)→closeHood() | Manual, then re-tap same Hood to confirm no stale state |
| 5.2 | Swipe down `PlaceDetailModal` at depth 2 → dismisses place only, Hood sheet still standing and interactive | TRD-hpd-§4.1 isDepth2Presented.set(false)→closePlace() | Manual |
| 5.3 | After a swipe-dismiss, tapping the same or a different Hood/pin immediately opens correctly (no stuck state, no double-open, no failure to reopen) | Regression class the two-way-binding fix targets | Manual — the actual behavioral risk beyond the unit test |
| 5.4 | Swipe-dismiss the Hood sheet while a place modal (depth 2) is open — confirm both close and state is fully clear (`placeDepth == nil` behaviorally) | TRD-hpd-§4.1 closeHood clears both fields | Manual |

## 6. Empty Hood (PD-hpd-req2 bullet 4, TRD-hpd-§4.8)

| # | Case | Trace | Method |
|---|---|---|---|
| 6.1 | Open a real Hood with zero demo places (e.g. `lev-hair`, or any of the 21 empty real Hoods) — sheet opens cleanly, plain empty state, no crash, no error banner (source is `.seed`, not `.unavailable`) | PD-hpd-req2 bullet 4; TRD §4.8 row 2 vs row 3 distinction | Manual |
| 6.2 | Empty-state CTA "Explore another Hood" is tappable (≥44pt) and calls `closeHood()` | TRD-hpd-§4.8 row 2 | Manual |

## 7. Accessibility (design spec §4, TRD-hpd-§11 C11)

| # | Case | Trace | Method |
|---|---|---|---|
| 7.1 | VoiceOver on `HoodSheet` ✕ — announces "Close", activatable | TRD-hpd-§4.8 accessibilityLabel | Manual, VoiceOver on |
| 7.2 | VoiceOver on `PlaceDetailModal` ✕ — announces "Close", activatable | Same pattern | Manual, VoiceOver on |
| 7.3 | VoiceOver on place rows — announces "Name, Category" | TRD-hpd-§4.8 | Manual, VoiceOver on |
| 7.4 | VoiceOver on Save button — announces "Save"/"Saved", never a checkmark state | TRD-hpd-§4.4, §4.8 | Manual, VoiceOver on |

## 8. Regression / full-suite

| # | Case | Trace | Method |
|---|---|---|---|
| 8.1 | Full `PassengerTests` + `PassengerUITests` target run together (not scoped/per-class) — green | Standing QA rule (L-005) | `xcodebuild test`, both targets, one invocation |
| 8.2 | `ColdOpenPerformanceTests` still within budget (≤2.0s / T-031's cold-open budget) with real 24-Hood geometry + 9-place fixture | TRD-hd-§8-D9, TRD-hpd-§5 | Part of the same full-suite run |

---

---

## Results (executed 2026-08-01, checkout `passenger-code` `23dd6d5`)

**Overall verdict: FAIL — Blocker.** A crash reproduces on every path that opens either sheet (pin tap → `PlaceDetailModal`, Hood-button tap → `HoodSheet`), on a clean rebuild (deleted DerivedData, `clean build`, fresh uninstall/install). This blocks nearly every case below — marked BLOCKED where the sheet never renders. See main QA report for the full writeup; summarized per-case here.

| # | Case | Verdict | Note |
|---|---|---|---|
| 1.1 | `PlaceCatalogTests` 3 determinism assertions | PASS | Part of full-suite run, 80/80 green |
| 1.2 | Zero network requests, observed behaviorally | PASS | `lsof -p <Passenger PID> -i` empty at every checkpoint (launch, mid-session, post-crash-relaunch) |
| 1.3 | Sheets render with no network reachable | BLOCKED | Sheets never render — crash, see Blocker below |
| 2.1 | `florentin` blurb renders | BLOCKED | Crash before sheet appears |
| 2.2 | `kerem-hateimanim` no-blurb branch | BLOCKED | Crash before sheet appears |
| 2.3 | `neve-tzedek` no-blurb branch | BLOCKED | Crash before sheet appears |
| 2.4 | Only `florentin` has non-null blurb | PASS | Confirmed by direct JSON read, 24/24 Hoods checked |
| 3.1 | 9/9 places inside real Hood polygon | PASS | Independent ray-casting script, all 9 confirmed inside their `hood_id`'s real polygon |
| 3.2 | Pins render inside Hood's coloured shape | FAIL (new finding) | `PlaceLayer` has no zoom gate at all — pins render at every zoom including cold-open city-wide view, contradicting TRD §3.3/§4.5/D5 ("pins render at close zoom only"). See Major finding below |
| 3.3–3.6 | Pin/row tap opens correct place modal | BLOCKED | Crash before modal appears |
| 4.1–4.3 | ✕ dismiss, both sheets, both depths | BLOCKED | Sheets never render |
| 5.1–5.4 | Swipe-to-dismiss, both sheets, no desync | BLOCKED | Sheets never render |
| 6.1–6.2 | Empty Hood clean sheet + CTA | BLOCKED | Sheets never render |
| 7.1–7.4 | VoiceOver on sheet controls | BLOCKED | Sheets never render |
| 8.1 | Full suite, one invocation | PASS | 80 tests, 15 suites, all green + `ColdOpenPerformanceTests` avg 0.460s |
| 8.2 | Cold-open budget with real geometry | PASS | Same run as 8.1 |

## Bugs found

### Bug 1 (Blocker) — App crashes on every tap that opens the Hood sheet or the place detail modal

**Repro (100% reproducible, confirmed on a from-scratch clean build):**
1. `rm -rf ~/Library/Developer/Xcode/DerivedData/Passenger-*`, `xcodebuild -scheme Passenger -destination 'platform=iOS Simulator,name=iPhone 17 Pro' clean build` (BUILD SUCCEEDED).
2. `xcrun simctl uninstall <device> com.avirangrisaro.passenger`, fresh `simctl install`, `simctl launch`.
3. Dismiss the location prompt (any choice).
4. Tap any place pin on the map (e.g. one of the florentin pins visible at cold-open zoom — see Bug 2, they render everywhere) → app crashes to the Home Screen.
5. Separately, relaunch and tap the `HoodButton` pill (e.g. "Kerem HaTeimanim") instead of a pin → app crashes identically.

**Evidence:** both crashes are `EXC_BREAKPOINT`/`SIGTRAP`, `_assertionFailure` inside `SwiftUICore/Environment+Objects.swift:34`, with a full stack trace that never reaches into the `Passenger` binary itself (the app's own code never gets a chance to run — the crash happens while SwiftUI is building the presented view's `@Environment` property wrappers, before `body` executes). Console fatal-error text, captured via `log show`:
- Pin tap → `Fatal error: No Observable object of type SavedPlacesStore found. A View.environmentObject(_:) for SavedPlacesStore may be missing as an ancestor of this view.`
- HoodButton tap → `Fatal error: No Observable object of type PlaceCatalog found. A View.environmentObject(_:) for PlaceCatalog may be missing as an ancestor of this view.`

Both crash sites are Site A (`MapScreen`'s own `.sheet(isPresented: detailRouter.isDepth1Presented)`, `MapScreen.swift:129`), presenting either `HoodSheet` or `PlaceDetailModal` directly. `MapScreen.swift:126-129` applies `.environment(placeCatalog)` / `.environment(detailRouter)` / `.environment(savedPlacesStore)` immediately before `.sheet(...)` in the modifier chain — textbook-correct SwiftUI ordering — yet the presented sheet content cannot see any of them. Not a race: reproduces identically whether the tap happens immediately after launch or 5+ seconds later. Since both `HoodSheet` (reads `PlaceCatalog`) and `PlaceDetailModal` (reads `SavedPlacesStore` first, declared before `DetailRouter`) crash on the *first*-declared `@Environment(Type.self)` property they read, this looks like the entire `.environment()` chain fails to reach the sheet's content in this specific `Map` + `.sheet` + `@Observable`-environment construction, not a single missing call — worth investigating as a SwiftUI/iOS 26.5 interaction (the codebase already carries one other flagged iOS 26 Map quirk, FB19394663, in `MapScreen.swift`'s tap-gesture comment).

**Impact:** every P0 in `hood-place-detail.md` reqs 1–7 is unreachable in the running app — the Hood sheet, the place detail modal, the blurb branch, the empty state, the ✕ controls, and swipe-to-dismiss are all untestable and, more importantly, unusable by an actual user on this build. This is not a demo-polish gap; the feature as shipped does not open.

**Why the test suite didn't catch it:** `DetailRouterTests` exercises `DetailRouter`'s state machine directly (`openHood`/`openPlace`/bindings) as plain method calls — it never renders `HoodSheet`/`PlaceDetailModal` inside the live `MapScreen` environment chain. No XCUITest taps a pin or a Hood and asserts a sheet appears; `PassengerUITests` only has `ColdOpenPerformanceTests` (launch timing, no interaction). Recommend the fix pass add at least one UI test that taps a pin (or drives `DetailRouter` through the full `MapScreen` environment) and asserts the sheet's content actually renders — this exact regression would have failed on the first run of such a test.

### Bug 2 (Major) — Place pins render at every zoom level, not "close zoom only"

**Repro:** cold-launch the app (dismiss the location prompt), don't zoom or pan at all. All 9 bundled place pins are already visible, clustered by Hood (3 overlapping circular pins per Hood with places, rendered as a merged blob at this zoom since the underlying markers are ≥44pt each and the 3 places per Hood sit only meters apart on screen).

**Evidence:** `Passenger/Map/PlaceLayer.swift` has no zoom-based visibility condition at all — it's an unconditional `Annotation`. `Passenger/Map/MapScreen.swift:66-68` renders `ForEach(placeCatalog.allPlaces) { PlaceLayer(...) }` with no wrapping `if` on `context.region.span`, unlike `HoodLayer`'s `showsName` gate (`MapScreen.swift:79`, driven by `nameLabelSpanThreshold`). Compare to `hood-place-detail/TRD.md` §3.3 ("Pins render at close zoom only") and §8 D5 ("The pin's close-zoom span threshold is [ASSUMPTION] ~0.02 latitude delta; `ios-developer` tunes it against the real dataset") — the TRD describes this as decided behavior with only the numeric threshold left open, but no threshold of any kind is implemented.

**Impact:** at the Build-Phase-1 fixture's current density (9 places, 3 per Hood) this reads as a cluttered blob rather than a broken map, but it contradicts the TRD's stated design and the quality-floor language in §3.4.1 about coordinates needing to "render inside the coloured shapes" (implicitly assuming zoom-gated pins) — at real dataset scale (T-042's eventual curated set) this would place hundreds of pins on the city-wide cold-open view. Also relevant because it's what made Bug 1 trivially reachable on the very first tap after cold open, before any zoom or deliberate navigation to a Hood.

## Out of scope for this pass (Phase-1 acceptance explicitly does not cover)

- Live Supabase fetch path, `PlacesAPI`/`PlacesCache` disk round trip, `.live`/`.cache`/`.unavailable` states — built and unexercised per TRD-hpd-§4.3, §7.
- Route hand-off to Apple Maps app-switch round trip (device-dependent, out of this session's simulator reach beyond confirming the button/disabled-state logic).
- Save-state persistence across app relaunch (not named in this dispatch; flagged only if found broken incidentally).
