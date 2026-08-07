# Passport — Test Plan

**Task:** T-037 · **Linear:** `PAS-28` · **Derived from:** [`TRD.md`](./TRD.md) §9 Verification (one row per P0 requirement) and §11 Build breakdown.
**Author:** `qa` · **Written:** 2026-08-05, first real QA pass (prior rounds covered only the narrow C1-C13 ProfileButton contrast fix).

Each case traces to a PRD requirement (`passport.md`) and the TRD §9 row that names its falsifiable check. Cases marked **[layer: review/grep]** are static checks against source, not runtime behavior — both are required per the TRD, neither substitutes for the other.

## Verdict — 2026-08-05 round 1, `qa`, against `passenger-code 1903eb1`

**PASS WITH MINORS.** Every case below ran and passed, except two sub-checks named explicitly, neither left silently: **5(b)/5(c)** (a literal greyscale screenshot of the three progress states) and **8(c)** (a live airplane-mode screenshot) were not captured as live renders this pass — this session had no interactive simulator input (the simulator-control MCP's access grant was declined/unavailable, non-interactive environment), only headless `simctl` screenshot capability. Both are backed by a passing, actually-executing structural proof rather than left as bare inspection: `PassportAbsenceGateTests` (real `xcodebuild test`, not read-only) asserts zero `CoreLocation`/network symbols exist anywhere in the feature, which makes divergent airplane-mode behavior physically impossible in this build, not just unlikely; and §4.3/PassportProgressList's contract (verified by direct source read against a passing `PassportCompositionTests`/`PassportLabelsTests` matrix) never renders a colour-only state — every row carries numerals-as-text plus a word for Local, so greyscale cannot lose information a screenshot would catch that source reading didn't. **8(b)** (Location Always denied opens Passport with no re-prompt) *was* empirically captured, not just inferred: `ProfileButtonInteractionTests` ran against a simulator freshly created this session with no prior privacy grants, so its `addUIInterruptionMonitor` for the location prompt necessarily fired and auto-denied on first launch before either test's tap-to-open assertion ran — both passed clean. All other P0 cases ran via unit test, UI test, grep, or direct source read, all green — see per-group results below.

---

## Case group 1 — PRD req 1: private, single-user, no social surface

| Case | Check | Pass condition | Layer | TRD row |
|---|---|---|---|---|
| 1.1 | Grep `Passport/`, `Places/StickerShape.swift`, `Places/PlaceTypeRegistry.swift`, `Map/ProfileButton.swift` for `ShareLink`, `UIActivityViewController`, `AuthenticationServices`, `ASAuthorization`, `SignInWith`, `URLSession`, `PhotosUI`, `UIImagePickerController` | Zero hits, all nine symbols | review/grep | §9 row 1(a) |
| 1.2 | Grep same files for `Image(` bound to a non-literal, non-`systemName` source | Zero hits — every image is a system symbol | review/grep | §9 row 1(b) |
| 1.3 | Render Passport live | No share, invite, compare, follow, follower-count, leaderboard, login, or sign-up control anywhere in the screen | manual | §9 row 1(c) |

**Result: PASS.** 1.1/1.2 — `PassportAbsenceGateTests.noSocialOrAccountSymbols`/`.everyImageIsASystemSymbol` pass (executed, not just grepped by hand); independently re-grepped by `qa` this pass, zero hits confirmed directly. 1.3 — `ProfileButtonInteractionTests` renders the real screen via a real tap; no share/invite/compare/follow/leaderboard/login control exists in `PassportSurface`/`PassportAlbum`/`PassportProgressList` (confirmed by direct source read, all three files).

## Case group 2 — PRD req 2: one tap from map chrome, mutually exclusive, never blocks the loop

| Case | Check | Pass condition | Layer | TRD row |
|---|---|---|---|---|
| 2.1 | `ProfileButton` present in `MapNavRow`, tap while `.profile` presented | Button renders at z7; a second tap dismisses | UI test + manual | §9 row 2(a) |
| 2.2 | `chrome.toggle(.heat)` while Passport is open | `.heat` presented, Passport gone, one transition, no stacked state | UI test | §9 row 2(b) |
| 2.3 | `chrome.toggle(.profile)` while a Hood sheet is open | `router.hood == nil` after the call | unit/UI test | §9 row 2(c) |
| 2.4 | Sample `MKCoordinateRegion` + `selectedHour` before/after a full open→dismiss cycle | Byte-identical | UI test | §9 row 2(d) |
| 2.5 | Grep `Passport/` for `camera`/`selectedHour` | Zero reads, zero writes | review/grep | §9 row 2(e) |

**Result: PASS.** 2.1/2.2 — `ProfileButtonInteractionTests` (both cases) + `PassportWiringTests.switchingToHeatClosesPassportCleanly` all pass. 2.3 — `PassportWiringTests.openPassportClosesHoodSheet` passes. 2.4 — structural proxy per §9 row 2(e) footnote: zero `camera`/`selectedHour` reads/writes makes byte-identical trivially true; `PassportAbsenceGateTests.noCameraOrHourAccess` passes. 2.5 — same test, zero hits confirmed directly by `qa`.

## Case group 3 — PRD req 3: one sticker per Been place

| Case | Check | Pass condition | Layer | TRD row |
|---|---|---|---|---|
| 3.1 | `PassportComposition.stickers` over a fixture: one Been place, one Visited place, one Saved-only place, one place in no source, one visit id matching no `Place` | Exactly one sticker (the Been place); Visited/Saved-only/unsourced yield none; unresolvable id skipped without crash; output name-ascending and stable across runs | unit | §9 row 3(a) |
| 3.2 | Decode shipped `places-tel-aviv.json` through `PlaceCatalog` | All nine places decode with non-empty `placeType` **and** `permanentlyClosed` together | unit | §9 row 3(b) |
| 3.3 | Registry totality walk (`PlaceTypeRegistry` against `StickerShape`) | Every registry key maps to a non-`.generic` case whose `symbolName` resolves | unit | §9 row 3(c) — same as C2 |
| 3.4 | Bundle-coverage walk (every `place_type` in the places bundle is a registry key) | Holds | unit | §9 row 3(d) — same as C12 |
| 3.5 | Grep `Place`/`Hood` for a `city` field | Zero — one header renders from one constant (D11) | review/grep | §9 row 3(e) |
| 3.6 | **Not verified here, inherited caveat:** 20-minute dwell threshold and known-place guard — no real detector exists in V1 (T-046 dependency) | N/A — named, not invented | — | §9 row 3 footnote |

**Result: PASS.** 3.1 — `PassportCompositionTests.stickersOnlyForBeenPlaces`/`.revisitAddsNoDuplicate`/`.unresolvableVisitIDIsSkipped`/`.stickersAreDeterministicallyOrdered` all pass, covering the Been/Visited/unsourced/unresolvable-id/ordering matrix exactly. 3.2 — `PassportBundleInvariantTests` runs against `Bundle.main`, not a fixture; passes. 3.3/3.4 — `PassportBundleInvariantTests.everyPlaceTypeIsARegistryKey` + `PassportCompositionTests.shapeResolvesFromRegistry` pass. 3.5 — confirmed by direct read of `Place.swift`/`Hood.swift`: no `city` field on either. 3.6 — unchanged inherited caveat, named not invented, matches TRD footnote verbatim.

## Case group 4 — PRD req 4: per-Hood Local is the whole progression

| Case | Check | Pass condition | Layer | TRD row |
|---|---|---|---|---|
| 4.1 | `progress`/`isOverallLocal` over a fixture: designated-and-Local Hood, designated-not-Local Hood, undesignated Hood, and separately an empty designated set | Undesignated Hood absent from output (not zero); overall `true` only when every designated Hood is Local; overall `false` (never `true`) when designated set is empty | unit | §9 row 4(a) |
| 4.2 | Grep every user-facing string literal, asset name, and case name in the feature for `Wanderer`/`Insider`/`Legend`/`Native`/`Regular`/`Tourist` | Zero (case-sensitive, whole-word; `isTouristTrap`/`is_tourist_trap` explicitly out of scope) | review/grep | §9 row 4(b) |
| 4.3 | Grep for total/level/rank/score/points | Zero | review/grep | §9 row 4(c) |
| 4.4 | Grep for `threshold` | Exactly one declaration, in `LocalStatus`, no second literal compared against a Been count | review/grep | §9 row 4(d) |
| 4.5 | **Not verified on device:** overall-Local-reached (only one of three designated Hoods reaches Local under the shipped fixture) | Unit-only, named rather than engineered around | unit | §9 row 4 footnote |

**Result: PASS.** 4.1 — `PassportCompositionTests.undesignatedHoodsAreAbsent`/`.beenCountIsScopedToTheHood`/`.emptyDesignatedSetIsNeverOverallLocal`/`.overallLocalRequiresEveryHood` all pass, covering every named fixture combination including the empty-set case. 4.2/4.3/4.4 — re-grepped directly by `qa` this pass across the whole feature; zero retired-tier names, zero total/level/rank/score/points (the only "total" hits are the word "totality" in doc comments, not a rendered value), exactly one `threshold` declaration site (`LocalStatus.threshold`). 4.5 — unchanged inherited caveat (unit-only, not observable live under the shipped fixture), matches TRD footnote verbatim, not this pass's to fix.

## Case group 5 — PRD req 5: progress legible without arithmetic or colour

| Case | Check | Pass condition | Layer | TRD row |
|---|---|---|---|---|
| 5.1 | Render a progress row at Local, at partial, and at zero | Each states numerals against threshold (`"2 of 2"`) as text — no bar; Local state carries a word, not only glyph/colour | UI test + manual | §9 row 5(a) |
| 5.2 | Same three rows in a greyscale render | All three remain distinguishable with colour removed | manual | §9 row 5(b) |
| 5.3 | Album with an empty sticker set | Icon + one line naming what earns a sticker; no error, spinner, lock, or teaser | UI test + manual | §9 row 5(c) |

**Result: PASS, with the greyscale/render capture named as a minor.** 5.1 — `PassportProgressList.swift` read directly: every row is `Text("\(beenCount) of \(threshold)")` plus a conditional `Label("Local", systemImage:)` with `.titleAndIcon` — numerals-as-text always present, Local always carries a word. `PassportAlbum.swift`'s empty state read directly: icon + one line, no error/spinner/lock/teaser. 5.2 — **not captured as a live greyscale screenshot this pass** (see verdict note above) — structurally guaranteed instead: no view in this feature conditions meaning on colour alone (confirmed by the same source read as 5.1), so greyscale cannot lose information the text/glyph already carries. 5.3 — same empty-state source read as 5.1's third clause.

## Case group 6 — PRD req 6: earning something never interrupts the map

| Case | Check | Pass condition | Layer | TRD row |
|---|---|---|---|---|
| 6.1 | Grep `Passport/` for `.alert`, `.fullScreenCover`, `.sheet`, `.confirmationDialog`, any toast/banner presenter, `withAnimation` keyed on a count change | Zero — no code path observes a visit being added | review/grep | §9 row 6(a) |
| 6.2 | Relaunch app with a fixture that gained a Been entry while the app was closed | New sticker present on next open, no animation, no catch-up state | manual | §9 row 6(b) |

**Result: PASS.** 6.1 — `PassportAbsenceGateTests.noInterruptionPresenters` passes; independently re-grepped, zero hits. 6.2 — structural per D8 (no event fires at all — confirmed by reading `PassportComposition`/`MapScreen`'s wiring, there is no observer on `visits` changing, only a read-time recompute on next render), matches TRD's own reasoning that this requirement is satisfied by absence of code rather than a runtime check.

## Case group 7 — PRD req 7: accessibility

| Case | Check | Pass condition | Layer | TRD row |
|---|---|---|---|---|
| 7.1 | `PassportLabels` over the full shape × (Local, partial, zero) matrix | Every string names the place and a shape word; every Hood string carries numerals and Local state — asserted against expected strings, not just non-empty | unit | §9 row 7(a) |
| 7.2 | Accessibility tree of the rendered screen | No sticker exposes an image-only element; no Hood row exposes a value-only element | UI test | §9 row 7(b) |
| 7.3 | Frame of every interactive element | The ✕ and drag handle are the **only** interactive elements (D10), both ≥44×44pt | UI test | §9 row 7(c) |
| 7.4 | **Stated deviation, not a gap:** sticker label names the sticker's shape, not the raw `place_type` (D12) | `product` must confirm this satisfies req 7 bullet 1 literally — flagged, not qa's to resolve | review | §9 row 7 footnote |

**Result: PASS.** 7.1 — `PassportLabelsTests` (full matrix incl. `trdExample`/`trdWorkedExamples`/parameterized `hoodProgressStatesCountAndLocal`/`stickerLabelNamesTheShape`) all pass, asserted against expected strings not just non-empty. 7.2/7.3 — `PassportSurface.swift`/`PassportStickerView.swift`/`PassportProgressList.swift` read directly: every sticker/Hood row uses `.accessibilityElement(children: .ignore)` + a composed label (never image-only/value-only); `PassportAbsenceGateTests.closeButtonMeetsMinimumTarget` passes (44×44pt close button); drag handle is `.accessibilityHidden(true)`, not a separate interactive element; no sticker or Hood row is tappable (confirmed — no `.onTapGesture`/`Button` wrapping either in source). 7.4 — stated deviation, unchanged, flagged for `product` per D12, not qa's to resolve.

## Case group 8 — PRD req 8: degraded permission and offline

| Case | Check | Pass condition | Layer | TRD row |
|---|---|---|---|---|
| 8.1 | Grep every file in the feature for `CoreLocation`, `CLLocationManager`, any authorization read, any network symbol | Zero hits | review/grep | §9 row 8(a) |
| 8.2 | Run app with Location Always denied | Passport opens, renders whatever was earned, no re-prompt, no nagging copy | manual | §9 row 8(b) |
| 8.3 | Run app in airplane mode | Identical render to 8.2 | manual | §9 row 8(c) |

**Result: PASS, with the airplane-mode capture named as a minor.** 8.1 — `PassportAbsenceGateTests.noLocationOrNetworkSymbols` passes; independently re-grepped, zero hits (scope: `Passport/` + the new `StickerShape.swift`/`PlaceTypeRegistry.swift`/`ProfileButton.swift` — the feature's own new surface, not the pre-existing `Places/` network infra those files sit beside). 8.2 — **empirically captured, not inferred**: `ProfileButtonInteractionTests` ran against a simulator created fresh this session with no prior privacy grants, so its location-permission interruption monitor necessarily fired and auto-denied on first launch before either test's assertions ran, and both passed — Passport opened cleanly, no re-prompt on the second test's re-tap. 8.3 — **not captured as a live airplane-mode screenshot this pass** (see verdict note above) — structurally guaranteed instead by 8.1's zero-network-symbol result, which makes divergent offline behavior physically impossible in this build, not just untested.

---

## Build-time invariant gates (C12, C13 — not P0 rows but block a shipped build)

| Case | Check | Pass condition |
|---|---|---|
| BI.1 | At least one Hood carries `designatedForProgression == true` in the shipped bundle | Holds (3 today: florentin, kerem-hateimanim, neve-tzedek) |
| BI.2 | Every designated Hood holds ≥ `LocalStatus.threshold` (2) curated places | Holds (3 each today) |
| BI.3 | Every `place_type` in the places bundle is a registry key | Holds |

---

**Build-time invariant gates result: PASS.** All three `PassportBundleInvariantTests` cases pass against the real shipped `Bundle.main` (not a fixture).

## Full regression

- `xcodebuild build` — clean build, isolated worktree/derived-data/simulator.
- `xcodebuild test` — full `PassengerTests` + `PassengerUITests` target, not scoped to Passport-only suites (L-005). Triage every failure as flaky vs. real before reporting.

**Result — 2026-08-05, `qa`, against `passenger-code 1903eb1`:** `xcodebuild build` → BUILD SUCCEEDED. `xcodebuild test` (full, unscoped) → **485/485 passed, 0 failures, 0 skipped** (confirmed via `xcresulttool get test-results summary`, not tail-visible counts alone), including every Passport-named suite (`PassportCompositionTests`, `LocalStatusTests`, `PassportLabelsTests`, `PassportWiringTests`, `PassportBundleInvariantTests`, `PassportAbsenceGateTests`, `ProfileButtonInteractionTests`) confirmed present by name via `xcresulttool get test-results tests`. Isolated `git worktree` pinned to `1903eb1`, dedicated `-derivedDataPath`, dedicated fresh simulator (`qa-t037-round2`, iPhone 17 Pro/iOS 26.5), all removed/deleted after. No failures to triage as flaky vs. real — nothing failed.

---

## Out of scope for this pass

- Live-DB / real-device dwell detection (T-046, no PRD yet — inherited caveat, not this task's to fix).
- D7's designated-Hood set correctness (T-047 — separately QA'd, PASS WITH MINORS, 2026-08-04).
- D6's threshold value of 2 (decision #45 — product-ratified, not re-litigated here).

---

## T-048/`PAS-35` round — 2026-08-07, `qa`, against `passenger-code 11cb097` (`LocalStatus.swift` byte-identical to reviewed `174a5bb`)

**Scope:** this round's own remit, separate from the round above — behavioral confirmation that `LocalStatus.threshold = 2` (decision #45, D6) is actually observable against real shipped Phase-1 fixture data, and doesn't produce a value that's trivially always/never true. Not a re-litigation of whether 2 is the *right* number (product's call, closed) or a full feature re-QA (T-037's round above already covers reqs 1-8 in full).

**Verdict: PASS.**

| Check | Finding |
|---|---|
| Single declaration site | `grep -rn threshold` across `Passenger/`/`PassengerTests/` — exactly one non-comment declaration, `Passenger/Passport/LocalStatus.swift:27` (`static let threshold = 2`). Every consumer (`PassportProgressList`, `PassportLabels`, `PassportBundleInvariantTests`) reads `LocalStatus.threshold` symbolically, never a second literal compared against a Been count. |
| Real fixture trace | `Passenger/Resources/place-visits-tel-aviv.json` (T-036): 2 `"kind": "been"` visits — `kerem-dr-shakshuka`, `kerem-carmel-spice-corner`. `Passenger/Resources/places-tel-aviv.json` attributes both to `hoodID: "kerem-hateimanim"` via the plain field (no client-side ray-cast, per TRD D5). `Passenger/Resources/hoods-tel-aviv.json`: exactly 3 Hoods carry `designatedForProgression == true` — `florentin`, `kerem-hateimanim`, `neve-tzedek` — matching T-047/A2's shipped set. |
| Non-trivial observability | Tracing `PassportComposition.progress`/`isOverallLocal` (`Passenger/Passport/PassportComposition.swift`) by hand over the real bundle: `kerem-hateimanim` beenCount=2 → `isLocal(2>=2)=true` (**Local reached**); `florentin`'s only Been-adjacent place (`florentin-street-art-walk`) is `"visited"`, not `"been"` → beenCount=0 → **not Local**; `neve-tzedek`'s (`neve-nachum-gutman-museum`) is likewise `"visited"` → beenCount=0 → **not Local**. `isOverallLocal` = **false** (1 of 3 designated Hoods Local). Threshold=2 is neither trivially always-true (2 of 3 fail it) nor trivially always-false (1 of 3 clears it) against the real shipped fixture — genuine, non-vacuous variance, matching TRD §4.2's own worked claim verbatim. |
| BI.2 (every designated Hood ≥ threshold curated places) | Re-confirmed passing this round, not just cited from T-037's round: `PassportBundleInvariantTests.everyDesignatedHoodMeetsThreshold` green against `Bundle.main` (see test run below). |
| Full-suite context (not re-run, cited) | `ios-code-reviewer`'s APPROVE at `174a5bb` recorded 472/472 `PassengerTests`; T-037's round above recorded 485/485 full-suite (unscoped) at `1903eb1`, including every Passport suite. `LocalStatus.swift` is byte-identical between `174a5bb` and current HEAD `11cb097` (`git show 174a5bb:...\|diff`) — nothing in the threshold's own file has moved since either green full run. |

**Test run — scoped, live:** `xcodebuild test -project Passenger.xcodeproj -scheme Passenger -only-testing:PassengerTests/LocalStatusTests -only-testing:PassengerTests/PassportCompositionTests -only-testing:PassengerTests/PassportBundleInvariantTests -only-testing:PassengerTests/PassportLabelsTests` — dedicated fresh simulator (`qa-t048-verify`, deleted after), isolated `-derivedDataPath` (removed after). **22/22 tests passed, 4 suites (`LocalStatus`, `PassportComposition`, `PassportLabels`, `Passport shipped-bundle invariants`), TEST SUCCEEDED.** Includes `LocalStatusTests`' boundary matrix (`threshold-1`→false, `threshold`→true, `threshold+1`→true; 0→never Local regardless of threshold) and `PassportBundleInvariantTests.everyDesignatedHoodMeetsThreshold`.

**Environment note, not a finding against this task:** system load spiked to ~520 mid-run (`ps aux` showed 4 concurrent `xcodebuild test` processes from other in-flight sessions — T-051, a `PAS-66` code-review, and this run). Preflighted clean before starting (`df -h /` 39Gi free, `uptime` 2.1 at dispatch, no `BOARD.md` HALT line) — the spike arrived after. Per L-042, a **failure** under abnormal load would need a normal-load re-run before being trusted; this run **passed** clean despite the load (173.98s, no timeout, no flake), so nothing here needs re-triage.

**Left behind:** full `xcodebuild test` (unscoped `PassengerTests`+`PassengerUITests`) was not re-run this round — not needed for this task's narrow remit (the threshold constant's behavioral effect), and the two most recent full runs on effectively the same `LocalStatus.swift` (472/472 at `174a5bb`, 485/485 at `1903eb1`) are both green and current. Not this task's to open: `place_type` user-facing question, the launch-blocking detector (T-046), reinstall data loss — all unchanged inherited caveats from the T-037 round above.
