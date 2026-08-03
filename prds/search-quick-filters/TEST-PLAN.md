# Search & Quick Filters — Test Plan

**Traces to:** [`search-quick-filters.md`](./search-quick-filters.md) (PRD, Draft v1) requirements 1-8, via [`TRD.md`](./TRD.md) §9's verification table (one row per P0 requirement) and §11's build breakdown (C1-C14).
**Built from:** TRD §9 directly — each row below is that table's Observable/Pass-condition pair turned into an executable case, not a re-derived criterion (per L-018).
**Commit under test:** `passenger-code 3d8e3b8` ("T-038/PAS-29: Search & quick filters, Build Phase 1 (C1-C14)").

Status column is filled in at QA time: **PASS** / **FAIL** / **BLOCKED** (dependency not in tree) / **NOT CHECKABLE IN PHASE 1** (TRD says so explicitly, not a QA judgment call).

---

## Row 1 — One door, one sheet, never a destination (PRD req 1)

| Case | Check | Layer | Status |
|---|---|---|---|
| 1a | `grep -rn "fullScreenCover\|NavigationStack\|NavigationLink" Passenger/Search Passenger/SearchSheet` → 0 hits | static/grep | |
| 1b | `camera` and `densityStore.selectedHour` byte-identical across open→dismiss (3 samples) | unit/manual | |
| 1c | `chrome.presented == .search` after `toggle(.search)` with `.heat` presented (chrome never stacks) | unit (`MapScreenSearchWiringTests`) | |
| 1d | `router.hood == nil` after opening `.search` with a Hood sheet already open | unit (`MapScreenSearchWiringTests.openSearchClosesOpenHood`) | |

## Row 2 — One field matches three kinds of things (PRD req 2)

| Case | Check | Layer | Status |
|---|---|---|---|
| 2a | `SearchQuery.run("suzan", .all, seedIndex)` → exactly `["Suzana Yemenite Kitchen", "Suzanne Restaurant"]`, in order, zero Hood results | unit (`SearchShippedSeedTests`) | |
| 2b | `run("shakshuka", …)` → exactly `["Dr. Shakshuka"]`, `matchedKeyword` set — **TRD-flagged staleness**: this is actually a name match by §4.4 rule 4 (place name contains "shakshuka"), not a keyword match. Assert the real algorithmic behavior (name match wins), not the TRD's literal row 2b text — confirmed spec staleness, not a defect, by `ios-code-reviewer` 2026-08-03, `architect`/`product` owe a one-line TRD correction | unit (`SearchShippedSeedTests`) | |
| 2c | `run("coffee", …)` → exactly `["HaMakolet"]`, `matchedKeyword` set | unit (`SearchShippedSeedTests`) | |
| 2d | `run("Florentin", …)` → **TRD-flagged staleness**: real seed returns 2 rows (Hood "Florentin" + place "Florentin Street Art Walk," name also contains "Florentin," per D7 ordering), not the TRD's literal "exactly one, kind == .hood." Assert 2, per the same staleness finding | unit (`SearchShippedSeedTests`) | |
| 2e | Wall time of `run` at a synthetic 2,000-place index ≤16ms/call, index build ≤250ms | unit (`SearchQueryTests`/perf) | |
| 2f | A static `Text` "Search" label exists, distinct from the `TextField`'s prompt | UI test (new — closes C13 gap) | |
| 2g | **Not checkable in Phase 1**: strategy's probe words "hummus"/"rooftop bar" appear in neither shipped seed — owner T-042 step B4, Build Phase 2 | — | NOT CHECKABLE IN PHASE 1 |

## Row 3 — Two chips, quick filters and nothing more (PRD req 3)

| Case | Check | Layer | Status |
|---|---|---|---|
| 3a | Exactly 2 chips render; `PlaceCategory.allCases.count == 2` | unit (`CategoryFilterTests`) | |
| 3b | `run("", .only(.eatDrink), seedIndex)` → exactly the six `eat-drink` seed places, name-ascending, zero Hoods | unit (`SearchQueryTests`) | |
| 3c | `run("b", .only(.eatDrink))` result ⊆ `run("b", .all)` place results, all `.eatDrink`; Hood results of `run("b", .all)` all still present (chip narrows, doesn't replace; Hoods survive a chip per D8) | unit (`SearchQueryTests`) | |
| 3d | Fresh `SearchSession()` → `filter == .all`, both chips render selected | unit (`SearchSessionTests`) | |
| 3e | Selected chip carries a `checkmark` glyph, unselected carries none — distinguishable in greyscale | manual (live pass) + code read | |
| 3f | `grep -rn "CategoryChipRow(" Passenger` → exactly one call site | static/grep | |

## Row 4 — Search filters the map at the selected hour; no second view of the data (PRD req 4)

| Case | Check | Layer | Status |
|---|---|---|---|
| 4a | `SearchDim.emphasis` for a query matching one place in one Hood → that place's id and that Hood's id are the only members; every other layer receives `isDimmed == true` | unit (`SearchDimTests`) | |
| 4b | `emphasis` is `nil` after selection and after dismissal | unit (`SearchDimTests`) | |
| 4c | `grep -rn "URLSession\|PlacesAPI\|DensityAPI\|fetch" Passenger/Search Passenger/SearchSheet` → 0 hits | static/grep | |
| 4d | Place-result tap and pin tap both call `router.openPlace(p)` with an identical `Place` | unit | |
| 4e | `grep -rn "selectedHour" Passenger/Search Passenger/SearchSheet` → 0 hits (hour is session-scoped per T-032 §3.1) | static/grep | |
| 4f | A result whose Hood has `band == nil` at the selected hour → `HoodLayer.fillColor == .clear`, no alert, no error copy | unit/manual | |
| 4g | `grep -rn "isTouristTrap\|tourist\|Flag" Passenger/SearchSheet` → 0 hits (no per-row flag line) | static/grep | |
| 4h | **Live visual dim** — Hood fills/pins at 0.25x opacity when results narrow the view; MapKit base tiles remain undimmed (§4.10's stated, accepted limitation) | manual (live pass) | |

## Row 5 — A result goes where the map would have gone (PRD req 5)

| Case | Check | Layer | Status |
|---|---|---|---|
| 5a | Place result tap → `router.place == the tapped place` | unit | |
| 5b | Hood result tap → `router.hood == the tapped hood`, camera centre within 200m of `hood.centroid` | unit/manual | |
| 5c | `grep -rn "\.sheet(isPresented:" Passenger` → exactly 2 call sites in view code (`MapScreen`, `HoodSheet`); `router.placeDepth ?? 0 <= 2` in every case | static/grep + unit — **C14 gap, no committed test locked this in before this pass** | |
| 5d | `grep -rn "openURL\|DirectionsService\|UIApplication.shared" Passenger/Search Passenger/SearchSheet` → 0 hits | static/grep | |

## Row 6 — Every state specified, none a dead end (PRD req 6)

| Case | Check | Layer | Status |
|---|---|---|---|
| 6a | Empty field, `.all` → `results.isEmpty`, UI shows two chips, no list rows, no suggestion rows | unit/UI | |
| 6b | Query `"zzzz"` → one line containing `"zzzz"` verbatim, field retains focus and text | UI (manual/new test) | |
| 6c | Offline → discharged by 4c (nothing fetches); staleness label itself **not observable in Phase 1** (`CachedDataIndicator` unreachable while `seedIsAuthoritative == true`) | — | NOT CHECKABLE IN PHASE 1 |
| 6d | Selecting Hood `Lev HaIr` from search → shipped `HoodSheet` empty state (null blurb, zero places), unchanged | manual | |
| 6e | `grep -rn "CoreLocation\|LocationStore\|CLLocation" Passenger/Search Passenger/SearchSheet` → 0 hits | static/grep | |

## Row 7 — In-progress state survives an interruption, not a completion (PRD req 7)

| Case | Check | Layer | Status |
|---|---|---|---|
| 7a | Type "flor", tap a chip, `toggle(.heat)`, `toggle(.search)` → `session.text == "flor"`, `session.filter == .only(...)` | unit (`MapScreenSearchWiringTests`/`SearchSessionTests`) | |
| 7b | Tap a result → `session.text == ""`, `session.filter == .all` | unit (`MapScreenSearchWiringTests.dismissSearchClearsEverything`) | |
| 7c | Each of the four manual-dismiss paths (✕, drag-past-threshold, z3 tap-outside, re-tap search button) independently clears session — 4 separate assertions | unit + manual (drag gesture needs a live pass) | |
| 7d | `grep -rn "UserDefaults\|AppStorage\|FileManager\|\.write(to:" Passenger/Search Passenger/SearchSheet` → 0 hits | static/grep | |

## Row 8 — Reach and accessibility (PRD req 8)

| Case | Check | Layer | Status |
|---|---|---|---|
| 8a | Search button, both chips, every row report `frame.height >= 44` and `frame.width >= 44` | UI test (new — closes C13 gap) | |
| 8b | VoiceOver labels of one Hood row and one place row → exactly `"Florentin, Hood"` and `"Anna Loulou Bar, place, Eat & Drink"` | UI test (new — closes C13 gap) | |
| 8c | Rows grow rather than truncate at the largest accessibility size | unit/structural (new — closes C13 gap; live content-size override tried and confirmed non-functional in this simulator session, see note below) | |
| 8d | Search-match pin vs. Places-list pin differ by shape (T-036's dashed ring), not colour alone — **BLOCKED unless T-036's ring is in the tree at build time**, record as unrun if absent | manual/code read | |
| 8e | z3 tap-catcher (opacity-0, full-screen) is excluded from the accessibility tree — `.accessibilityHidden(true)` at `MapScreen.swift:259` — and VoiceOver users dismiss via ✕ or two-finger scrub, not the invisible catcher | code read + manual VoiceOver pass | |

---

## Coverage gap closed this pass (C13/C14)

TRD §11 C13 ("accessibility checks as real tests: 44pt frames, exact VoiceOver strings, Dynamic Type growth") and C14 ("grep-backed assertion that exactly two `.sheet(` sites exist app-wide, and `router.placeDepth ?? 0 <= 2`") were flagged by `ios-code-reviewer` (2026-08-03, APPROVE WITH MINORS) as specified but not shipped. Closed by `qa` this pass:

- **`PassengerUITests/SearchAccessibilityTests.swift`** (new) — 44pt frames for the search button, both chips, and a result row; exact VoiceOver labels against real seed data, `"Florentin, Hood"` and `"Anna Loulou Bar, place, Eat & Drink"`.
- **`PassengerTests/SearchRowGrowthGuardTests.swift`** (new) — row 8(c)'s Dynamic Type growth, verified structurally rather than via a live content-size override. Two standard simulator mechanisms were tried live during this pass — the `-UIPreferredContentSizeCategoryName` launch argument, and `xcrun simctl ui <udid> content_size accessibility-extra-extra-extra-large` — and neither actually changed rendered text size on this session's Simulator runtime (confirmed by a plain SpringBoard screenshot after the override: default text size throughout, even after an app relaunch and a full simulator reboot, and even though `simctl`'s own getter echoed the override back as stored). That is a tooling limitation, not a Passenger behavior, so the test asserts the structural property TRD §4.8 itself names as the mechanism instead — no `.lineLimit` anywhere in the search feature's views, `.fixedSize(horizontal: false, vertical: true)` on every `Text` run in `SearchResultRow` — deterministic, and independent of whether simulator content-size propagation works.
- **`PassengerTests/SearchStructuralGuardTests.swift`** (new) — row 5(c)/C14: grep-backed assertion that exactly two real `.sheet(isPresented:` call sites exist app-wide (excludes `DetailRouter`'s own doc-comment mentions of the pattern by content, not by file), plus the depth-ceiling invariant driven through this task's own search-selection flow.

All three run in the full suite alongside the shipped C1-C12 tests (see Evidence in the PROGRESS.md worklog entry for counts).

## Not this task's to fix (carried forward, not re-litigated here)

- D2's two-height drag gesture is an `[ASSUMPTION]` — behavior confirmed live, not re-argued.
- §4.10's MapKit-base-tile dim limitation is accepted and flagged for `product`, not a defect.
- §9 row 2b/2c's literal expected-value text is stale against the real seed (confirmed independently by `ios-code-reviewer`) — the shipped `SearchShippedSeedTests.swift` asserts the algorithmically-correct behavior, and this test plan's rows 2b/2d follow the same reading.
