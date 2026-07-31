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

---

## Re-pass results (executed 2026-08-01, checkout `passenger-code` `291c010`)

**Checkout independently verified before testing** (per the discipline that caught last round's wrong hash): `git log -1` on `passenger-code` confirmed HEAD is `291c010` verbatim, `git show --stat` confirmed the diff matches the dispatch's description (`MapScreen.swift`, `PlaceLayer.swift`, `HoodButton.swift`, `HoodSheet.swift`, `PlaceDetailModal.swift`, `DetailSheetInteractionTests.swift`, no unrelated files). Fresh clean build (deleted DerivedData) + fresh `simctl install` on `iPhone 17 Pro` (iOS 26.5), same device class as last round.

**Overall verdict: PASS.** Both prior Blocker/Major findings are fixed and independently confirmed; every case blocked last round is now reachable and passes. One environment/tooling note below, no product defect.

| # | Case | Verdict | Note |
|---|---|---|---|
| 1.1 | `PlaceCatalogTests` 3 determinism assertions | PASS | Full suite run (see 8.1), all green |
| 1.2 | Zero network requests, observed behaviorally | PASS | `lsof -p <Passenger PID> -i` empty — zero TCP/UDP sockets for the app process, checked after ~20 min of continuous interaction (pin taps, Hood taps, sheet open/close, Save toggles) |
| 1.3 | Sheets render with no network reachable | PASS | Every sheet opened during this pass rendered full bundled content while the app held zero network sockets throughout (see 1.2) — not a separate airplane-mode run, but behaviorally equivalent since the app never had a socket to lose |
| 2.1 | `florentin` blurb renders | PASS | Blurb text renders above the place list, no crash, no layout artifact |
| 2.2 | `kerem-hateimanim` no-blurb branch | PASS | No blurb section, no gap, no placeholder — title goes straight to the 3-place list |
| 2.3 | `neve-tzedek` no-blurb branch | PASS | Same, second no-blurb Hood confirmed independently |
| 2.4 | Only `florentin` has non-null blurb | PASS | Unchanged since last round's static check; re-confirmed by the 3 live Hood-sheet opens above (2 no-blurb, 1 blurb) |
| 3.1 | 9/9 places inside real Hood polygon | PASS | Unchanged; static finding from last round, not re-derived (no geometry touched by this diff) |
| 3.2 | Pins render inside Hood's coloured shape, close zoom only | PASS | **Zoom gate confirmed behaviorally both directions**: zero pins visible at cold-open (multiple screenshots, full Tel Aviv south in view, nothing rendered); zoomed to Florentin/Kerem HaTeimanim/Neve Tzedek (span crossing the 0.06 threshold) — all pins and Hood name labels appeared together, exactly the `showsNames` gate `PlaceLayer` now shares with `HoodLayer`. Hood polygon *fill color* itself is `.clear` at every zoom in this run — traced to `DensityStore` (live-fetch-only, no bundled seed, falls back to `.unavailable` offline) via source read, not a regression from this diff and not in T-033's scope; flagged as context, not a finding |
| 3.3 | Tap a pin in `florentin` → opens that place's modal directly | PASS | Tapped HaMakolet's pin, modal opened directly, no crash, no two-step preview |
| 3.4 | Tap a pin in `kerem-hateimanim` → correct place modal | PASS | Tapped Suzana Yemenite Kitchen's pin directly (not via row) — correct modal, no crash |
| 3.5 | Tap a pin in `neve-tzedek` → correct place modal | PASS | Tapped Nachum Gutman Museum's pin directly — correct modal, no crash |
| 3.6 | Tap a Hood-sheet row → opens that place's modal at depth 2 | PASS | Tapped "Dr. Shakshuka" row inside Kerem HaTeimanim's sheet — depth-2 modal opened correctly |
| 4.1 | `HoodSheet` ✕ → closes, map restored | PASS | Confirmed via Lev HaIr and Kerem HaTeimanim sheets — closes fully, camera/zoom unchanged |
| 4.2 | `PlaceDetailModal` ✕ at depth 1 → closes fully to map | PASS | Tapped HaMakolet's modal ✕ — full dismiss to map |
| 4.3 | `PlaceDetailModal` ✕ at depth 2 → closes place only, Hood sheet stands | PASS | Closed Dr. Shakshuka at depth 2 — Kerem HaTeimanim sheet still standing underneath, list intact |
| 5.1 | Swipe down `HoodSheet` → dismisses, state cleared; re-tap reopens cleanly | PASS | Swiped Kerem HaTeimanim closed, re-tapped same Hood — reopened correctly, all 3 rows intact, no stale/stuck state |
| 5.2 | Swipe down `PlaceDetailModal` at depth 2 → dismisses place only | PASS | Swiped Dr. Shakshuka closed at depth 2 — Kerem HaTeimanim sheet still standing, interactive |
| 5.3 | Re-tap after swipe-dismiss opens correctly, no stuck/double-open state | PASS | Same evidence as 5.1 |
| 5.4 | Swipe-dismiss the Hood sheet while a place modal is open → both close | **PASS (unit-test level only)** | Not reachable via a manual gesture: the depth-2 modal fully covers the depth-1 sheet's own drag handle/dismiss affordance, so there is no user-operable path to swipe the parent while the child is on top — by design, each swipe dismisses one level (confirmed 5.2). The invariant this case actually protects (`closeHood()` clearing both `hood` and `place` fields together) is directly covered by `DetailRouterTests`' `"closeHood clears both fields"`, part of the green 80-test run (8.1). Flagging the method gap honestly rather than claiming a manual repro that didn't happen |
| 6.1 | Empty Hood — clean sheet, no crash, no error banner | PASS | Hit twice independently (`Neve Ofer` via a background map tap, `Lev HaIr` via direct Hood-area tap) — both show "No places curated here yet." with the mappin.slash icon, no error banner (source is `.seed`, correctly distinguished from `.unavailable`) |
| 6.2 | Empty-state CTA "Explore another Hood" tappable, calls `closeHood()` | PASS | Tapped the CTA on `Lev HaIr`'s empty sheet — dismissed cleanly to map |
| 7.1 | VoiceOver on `HoodSheet` ✕ — "Close" | PASS (source-verified) | `HoodSheet.swift` closeButton: `.accessibilityLabel("Close")`. Full live-VoiceOver pass not practical in this automation environment (screenshot/tap-driven, no VoiceOver gesture layer); verified the modifier directly in source plus indirectly via the accessibility-identifier-driven UI tests (`DetailSheetInteractionTests`) passing, which proves the accessibility tree resolves correctly for these exact elements |
| 7.2 | VoiceOver on `PlaceDetailModal` ✕ — "Close" | PASS (source-verified) | `PlaceDetailModal.swift` closeButton: `.accessibilityLabel("Close")`, same method note as 7.1 |
| 7.3 | VoiceOver on place rows — "Name, Category" | PASS (source-verified) | `HoodSheet.swift` place row: `.accessibilityLabel("\(place.name), \(place.category.displayName)")` — exact format |
| 7.4 | VoiceOver on Save button — "Save"/"Saved", never a checkmark | PASS (source-verified) | `PlaceDetailModal.swift` saveButton: `.accessibilityLabel(isSaved ? "Saved" : "Save")`, glyph pair is `bookmark`/`bookmark.fill`, never a checkmark. Behaviorally exercised too: toggled Save on Suzana Yemenite Kitchen (reached via HoodSheet → depth 2, the exact nested-environment path the fix targeted) — bookmark filled correctly, `SavedPlacesStore` resolved with no crash |
| 8.1 | Full suite, one invocation | PASS | `PassengerTests` (Swift Testing, 80 tests/15 suites) + `PassengerUITests` (3 tests: `ColdOpenPerformanceTests` + 2 new `DetailSheetInteractionTests`) — **83 tests total, 0 failures**, single `xcodebuild test` invocation, not scoped |
| 8.2 | Cold-open budget with real geometry | PASS | `ColdOpenToInteractive` avg 0.465s (5 iterations, rel. std dev 2.56%), same as developer's reported figure, within the 2.0s budget, no regression |

**Zero app crashes observed** across this entire pass — extensive manual interaction (pin taps across all 3 populated Hoods, empty-Hood taps, row taps, ✕ at both depths, swipe-dismiss at both depths, Save toggles, repeated re-opens) plus the 3 automated UI tests. Cross-checked `~/Library/Logs/DiagnosticReports` for `Passenger-*.ips` crash reports: the only ones present (`00:13`–`00:40`) predate this session's build (started `01:06`) — no new crash reports during or after this pass.

**Tooling note, not a product finding:** the iOS Simulator control tool's screenshot pixel space is ~2.28x the device's point space (402×874pt); early taps in this pass used unconverted coordinates and silently missed small targets (system permission alert, sheet ✕/CTA buttons) while large-target gestures (the map itself) still "worked" by landing somewhere valid, masking the mismatch initially. Calibrated using the ✕ button as a known target once the pattern was noticed; all coordinates after that point used the corrected scale. Recorded here so a future QA pass on this same tooling doesn't re-lose the same time.

**Confirmed unchanged, as expected:**
- `BuildPhase.seedIsAuthoritative == true` (`Passenger/Support/BuildPhase.swift:17`) — unchanged by this diff, re-read directly from source.
- Zero-network property — re-verified behaviorally post-fix (1.2), not just assumed carried over.

---

## Round 3 results (executed 2026-08-01, checkout `passenger-code` `165fd7f`)

**Checkout independently verified before testing:** `git log -1` confirmed HEAD is `165fd7f`, `git log --oneline -3` confirmed the chain (`165fd7f` → `37c402f` → `291c010`) matches the dispatch's description exactly. `git show --stat 165fd7f` confirmed the diff touches only `MapScreen.swift` and `DetailSheetInteractionTests.swift`, matching `ios-code-reviewer`'s `1f233a3` re-review record. Fresh clean build (deleted DerivedData) on `iPhone 17 Pro` (iOS 26.5).

**Scope:** re-verify the acceptance REJECT's exact bug, the pin-tap regression check, the blurb round-trip, a full regression sweep of round 2's plan, plus the optional case-5.4 upgrade (Directions from depth 2).

**Overall verdict: PASS.** Every case below confirmed, several by direct manual gesture in the simulator (not just automated-test evidence) — screenshots taken at each step.

| # | Case | Verdict | Note |
|---|---|---|---|
| — | Full suite, one invocation (8.1/8.2) | PASS | `xcodebuild test`, unscoped, clean DerivedData: Swift Testing reports "Test run with 80 tests in 15 suites passed"; XCUITest reports 3/3 (`ColdOpenPerformanceTests` avg 0.463s + both `DetailSheetInteractionTests`). **83/83 green**, matching the developer's and reviewer's reported counts exactly. |
| **REJECT bug — florentin** | Tap inside `florentin`'s real boundary at cold-open zoom (no pins/HoodButton visible) | **PASS** | Manual tap in the live simulator (not just the automated test) landed inside `florentin`'s polygon and opened `florentin`'s own Hood sheet directly — title "Florentin", blurb rendered, 3 places listed. No place modal appeared. Screenshot captured. |
| **REJECT bug — kerem-hateimanim** | Tap inside `kerem-hateimanim`'s real boundary at cold-open zoom | **PASS** | Manual tap at the same normalized offset the fixed UI test uses (`kerem-suzana-yemenite-kitchen`'s coordinate) opened `kerem-hateimanim`'s Hood sheet ("Kerem HaTeimanim", 3 places) with no place modal. Screenshot captured. Matches `testTappingPopulatedHoodAtColdOpenOpensHoodSheet`, which also passed in the automated run. |
| Pin-tap path once zoomed in | Zoom in past the `showsNames` threshold (manual pinch gesture, not the `-uiTestZoomedIn` backdoor), tap a genuinely visible pin | **PASS** | Pinch-zoomed into Florentin manually; pins became visible (fork/knife and museum icons). Tapped `HaMakolet`'s pin directly — `PlaceDetailModal` opened immediately with correct content ("HaMakolet", "Eat & Drink"), no crash, no regression on the unchanged rendering-gate half of the code path. Also confirmed via `testTappingPlacePinOpensPopulatedPlaceDetailModalWhenZoomedIn` passing in the automated run (opens "Suzana Yemenite Kitchen" correctly). |
| Blurb branch round-trip | Open `florentin`'s Hood sheet, confirm blurb renders and the relocated/regenerated data loaded correctly | **PASS** | Blurb rendered in the live app exactly as expected: "[PROVISIONAL] Tel Aviv's street-art-and-nightlife district — graffiti-covered walls, converted warehouses, and bars that fill up late." Independently diffed the bundled `hoods-tel-aviv.json` against `hoods-tel-aviv.source.json` with a script (not eyeballed) — `florentin.blurb` byte-identical across both, no `_note` field surviving in the bundle (confirms `37c402f`'s cleanup landed), all 24 hoods' `blurb`/`isTouristTrap`/`designatedForProgression` otherwise unchanged. |
| 4.1–4.3 | ✕ dismiss, both depths | PASS | Depth-1 ✕ (tapped from `HaMakolet`'s pin-opened modal) closed fully to map. HoodSheet ✕ (tapped from both `Kerem HaTeimanim` and `Florentin`) closed fully to map, confirmed multiple times as a side effect of navigating between cases. |
| 6.1–6.2 | Empty Hood, CTA | PASS | Hit three times incidentally while calibrating tap coordinates (`Lev HaIr` twice, `Montefiore` once) — every time: clean "No places curated here yet." empty state, no crash, no error banner; "Explore another Hood" CTA dismissed cleanly to the map. |
| 3.6 / depth-2 stacking | Tap a Hood-sheet row → place modal at depth 2, Hood sheet still standing underneath | PASS | Opened `Kerem HaTeimanim`'s sheet, tapped "Suzana Yemenite Kitchen" row → `PlaceDetailModal` opened at depth 2 with the Hood pin still visible peeking behind the modal in the screenshot. |
| **Optional (product's case-5.4 upgrade)** | Tap Directions from depth-2 (`PlaceDetailModal` opened via a Hood-sheet row) — confirm `router.closeHood()` fires before the Maps hand-off and both sheets are gone on return | **PASS — exercised behaviorally, not just at unit-test level** | From the depth-2 "Suzana Yemenite Kitchen" modal, tapped "Directions". The app genuinely handed off to Apple Maps (`◀ Passenger` back-button appeared, Maps' own location-permission and notification prompts fired, "Choose Start" screen showed with the correct destination pre-filled). Returned to Passenger via the back button — **the map was showing with no sheet of any kind open**, confirming `closeHood()` cleared both `hood` and `place` fields before the hand-off, exactly as `PlaceDetailModal.swift:96`'s comment describes. This is the full round-trip `qa`'s round-2 pass could only cover via `DetailRouterTests`' unit-level assertion — now confirmed end-to-end with a real app-switch. Not added as a new automated UI test this round (a `UIApplication.open` hand-off mid-XCUITest is a flaky, environment-dependent thing to automate reliably — background/foreground timing, Maps' own first-launch prompts); flagging as a good candidate for a future dedicated pass if the team wants it automated rather than manually re-verified each time. |
| 7.1–7.4 | VoiceOver labels | PASS (source-verified) | `HoodSheet.swift`/`PlaceDetailModal.swift` untouched by `165fd7f` (diff only touches `MapScreen.swift` and the UI test file) — re-grepped both files directly: `HoodSheet.swift:69` `.accessibilityLabel("Close")`, `:143` `"\(place.name), \(place.category.displayName)"`; `PlaceDetailModal.swift`'s close/save buttons unchanged from round 2's verified text. No regression possible since the files didn't move. |

**Zero app crashes observed** across this pass — extensive manual interaction (cold-open taps into 2 populated Hoods + 3 empty Hoods, pinch-zoom, pin taps, Hood-sheet row taps, ✕ at both depths, the full Directions→Maps→back round trip) plus the 83-test automated run. Cross-checked `~/Library/Logs/DiagnosticReports` for `Passenger-*.ips`: all present reports (00:13–00:40) predate this session's build; none generated during or after.

**Verdict: PASS.** Both REJECT findings confirmed fixed by direct re-derivation (not trusted from the commit message or the reviewer's report) — florentin and kerem-hateimanim taps at cold-open zoom now open their Hood sheets, never an invisible pin's modal. The pin-tap path (the other half of the same gate) is unregressed. The blurb round-trip is clean. Every round-2 case re-confirmed, several incidentally through natural navigation during this pass. The optional case-5.4 upgrade was exercised for real, not just unit-tested.
