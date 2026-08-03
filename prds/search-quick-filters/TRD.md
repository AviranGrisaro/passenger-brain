# Search & Quick Filters — TRD

**Task:** T-038 · Linear `PAS-29`
**Status:** **v2**, 2026-08-03 (v1 2026-08-03) — verification amendment only. No contract, decision or build step is re-opened; **no `trd-review` re-run is owed.**
**Author:** `architect` · **Amended:** 2026-08-03 — T-053/`PAS-43`: [§9](#9-verification--one-row-per-p0-requirement) rows 2, 3, 4, 8 and the §9 preamble; [§4.10](#410-the-dim) brought in line with the system as built; **D14** (`PAS-43` corrects an original mislabel of `PAS-41`, which is an unrelated `ios-developer` CI-workflow task — `chief-of-staff`, 2026-08-03)
**Build phase:** 1 (client-only, bundled seed data)
**Routes to `trd-review`:** **`ios-developer` + `ios-code-reviewer` only.** Every step in [§10](#10-build-breakdown) is **[iOS]**. There is no `[Backend]` and no `[Algo/Data]` step — verified three ways in [§10](#10-build-breakdown), not inferred from the PRD.

**What changed at v2 (2026-08-03) — T-053/`PAS-43`.** `product`'s acceptance REJECT (round 8) failed PRD req 4 with **every §9 check green**, because row 4(a)'s pass condition asserted the emphasis *set* and the `isDimmed` value handed to each layer — both correct in the failing case. That is L-009's own failure shape, second occurrence after T-046/LOC-104. This revision rewrites the pass conditions that share it and **sweeps the rest of the table for the same pattern** rather than fixing the one row that was reported. **The shipped code is not changed and does not need to change** — `passenger-code d537ca5` already satisfies every amended condition; see D14 for the trace.

| # | Row | The pattern | Fix in v2 |
|---|---|---|---|
| 1 | **4(a)** — *reported* | "every other `PlaceLayer`/`HoodLayer` receives `isDimmed == true`" is **vacuously true over an empty set**: at `.cityWide`/`.neighborhood` no `PlaceLayer` is constructed at all, so the sentence held in exactly the case the requirement failed | Rewritten as a **rendered-result** condition with a non-emptiness anchor, checked **at both zoom tiers**, on the resolved fill alpha rather than on the flag |
| 2 | **4(b)** | `emphasis == nil` after selection/dismissal asserts the input to the dim, never that the dim lifted | Adds the rendered readback — the previously-dimmed Hood's resolved fill alpha returns to its undimmed value |
| 3 | **3(c)** | "result ⊆ the `.all` results **and** every place in it is `.eatDrink`" — both clauses hold over `[]`, so a matcher returning nothing passes | Adds the exact expected array; subset and ∀ become confirmations, not the whole check |
| 4 | **8(a)** | "**every one** reports `frame.height >= 44`" — vacuous if the query finds zero elements | Adds an exact element count before the ∀ |
| 5 | **8(c)** | Names **result rows only** and never the chip row — the surface that actually truncates — and its ∀ is vacuous over zero rows | Splits into 8(c-i) rows and **8(c-ii) chips**, both with count anchors |
| 6 | **2(d)** | "≤ 16ms per call" is trivially met by a matcher that returns `[]` | Pins the expected result count the timed call must return |
| 7 | **§9 preamble** | Eleven sub-checks are `grep → 0 hits`, which also passes if the grep covered nothing | Adds the standing positive-control rule for every negative-existence check in the table |

---

## 1. Context

- **PRD:** [`search-quick-filters.md`](./search-quick-filters.md), Draft v1, approved at `spec`. Not restated here.
- **Upstream design:** none, and none is required — the pre-code design gate was retired 2026-08-02 (`BOARD.md` lifecycle section). No design spec or mockup for this feature exists. Where the PRD leaves an interaction detail unspecified this document makes the call and labels it **[ASSUMPTION]**.
- **Cross-task inputs, all read directly rather than summarised:**
  - `prds/time-slider/TRD.md` (T-032) — owns `NavSurface`/`MapChromeState` (§4.1), `MapNavRow` (D1/D6), the `MapScreen` `ZStack` z-order (§2.3), and D2's "custom overlay, not `.sheet`".
  - `prds/places-been-saved/TRD.md` (T-036) — owns the second nav-surface precedent, and D8/§4.6's presentation-exclusivity calls, which this task reuses verbatim.
  - `prds/places-dataset/TRD.md` (T-042) — owns `places.keywords` (§3.2) and the client-side matching rules (§4.3), which this task adopts rather than re-deriving.
  - `prds/hood-place-detail/TRD.md` (T-033) — shipped. Owns `DetailRouter`, both destination sheets, and `.presentationBackgroundInteraction(.enabled(upThrough: .medium))`.
- **Shipped code read before writing:** `MapScreen.swift`, `DetailRouter.swift`, `Place.swift`, `PlaceCatalog.swift`, `PlacesAPI.swift`, `PlacesCache.swift`, `PlaceCategory.swift`, `PlaceLayer.swift`, `HoodLayer.swift`, `Hood.swift`, `DensityStore.swift`, `BuildPhase.swift`, `HoodSheet.swift`, `PlaceDetailModal.swift`, and both bundled seeds.

**State of the tree this was written against — re-checked mid-draft, and it had moved.** `passenger-code 9608617`, plus a **large uncommitted working tree belonging to other sessions**: T-036's Places build and T-034's events build are both live in it (11 modified files, 15 untracked paths). None of it is this agent's to stage. What that changes for T-038, verified by reading the files rather than the board:

| Thing | State as of this draft |
|---|---|
| `Map/MapChromeState.swift` | **Exists** (untracked, created by T-036's build). Read and compared against T-032 §4.1 — matches, four cases, four conformances, `toggle`/`dismiss` implemented. C5 is therefore a no-op in this tree. |
| `Map/MapNavRow.swift` | **Does not exist.** T-032's C2 owns it and has not landed. C6 still has to create it. |
| `Map/PlacesButton.swift` | Exists — bucket-2 chrome, *not* in the nav row (T-036 D7). Not a precedent for the search button. |
| A z3 scrim / tap-catcher | **Does not exist.** T-036 renders `PlacesListOverlay` from a bare `.overlay {}` with no scrim; the scrim is T-032's C-step and has not landed. C9 must create the `.search` tap-catcher itself. |
| `Place` | **Six fields now, not five** — T-036 added `permanentlyClosed`. `keywords` is still absent and still T-038's (`Place.swift`'s own comment names T-038 for it). |
| `PlacesAPI` `select=` | Already widened once, to `…,latitude,longitude,permanently_closed`, with a comment saying `keywords` "stays out; each lands with its reader." T-038 is that reader. |
| `PlaceLayer` | Now `(place, isListed, action)` — T-036's dashed personal-place ring has landed. Relevant to D12 and §9 row 8(d). |
| `MapScreen` body | Still `.overlay {}` chain, not the explicit `ZStack` T-032 §2.3 specifies. T-032's build converts it. |

Both build orders stay safe: C5/C6/C9 are create-if-absent against T-032's own contract, and C1 threads `keywords` through the same three source paths T-036 has just threaded `permanentlyClosed` through, in the same files.

---

## 2. Architecture

### 2.1 Files

```
Passenger/
  Search/                          # pure logic, no SwiftUI, no map types
    SearchIndex.swift              new — folded index over [Place] + [Hood] (§4.2)
    SearchResult.swift             new — one result row's data (§4.3)
    SearchQuery.swift              new — pure (index, text, filter) -> [SearchResult] (§4.4)
    CategoryFilter.swift           new — .all / .only(PlaceCategory) (§4.5, D8)
    SearchSession.swift            new — @Observable: the surviving query + filter (§4.6, D10)
  SearchSheet/                     # views only
    SearchOverlay.swift            new — the z5 container: heights, handle, ✕ (§4.7, D2)
    SearchFieldRow.swift           new — labelled TextField (§4.8)
    CategoryChipRow.swift          new — exactly two chips (§4.8)
    SearchResultRow.swift          new — one row + its VoiceOver string (§4.8)
    SearchEmptyStates.swift        new — empty-field and no-match lines (§4.8)
  Map/
    MapScreen.swift                MODIFIED — z5 surface, dim inputs, wiring (§4.9)
    MapChromeState.swift           UNCHANGED — already correct in-tree; C5 verifies only
    MapNavRow.swift                create-if-absent per T-032 D1/D6; + search button (C6)
    SearchButton.swift             new — icon-only `magnifyingglass` (C6)
    HoodLayer.swift                MODIFIED — one `isDimmed: Bool` input (§4.10)
    PlaceLayer.swift               MODIFIED — one `isDimmed: Bool` input beside `isListed` (§4.10)
  Places/
    Place.swift                    MODIFIED — + `keywords: [String]` (D6)
    PlaceCatalog.swift             MODIFIED — decode keywords on all three paths (D6)
    PlacesAPI.swift                MODIFIED — `select=` + `PlaceRow.keywords` (D6)
    PlacesCache.swift              MODIFIED — `CachedPlace.keywords` (D6)
```

The four `Places/` files are the **same four T-036 has just edited** for `permanentlyClosed`, in the same four places. If T-038 builds while T-036's diff is still uncommitted, C1 extends that work rather than racing it — `ios-developer` should read each file's current contents first, not the version quoted in any TRD.

Xcode synchronized file groups are on; dropping files in the folder is enough, no `project.pbxproj` edit (T-032 §2.1, confirmed against the shipped project).

### 2.2 Boundaries — who is allowed to know what

- **`Search/` knows no SwiftUI, no MapKit, no network, no `DensityStore`.** It is four value types and one small `@Observable` holding two properties. Every matching rule in this feature is therefore unit-testable with no simulator, no gesture and no fixture bundle. `import Foundation` only.
- **`SearchSheet/` knows no map and no router.** It renders `[SearchResult]` and reports a selection upward by closure. It never calls `DetailRouter` itself.
- **`Map/` stays the only layer that knows the z-order, the router, and the composition of `Places/`+`Hoods/` data into map content** — unchanged from T-031/T-033.
- **`MapChromeState` is T-032's contract and T-038 is a consumer, not a co-author.** `.search` is already a member of T-032's four-case `NavSurface`; this task adds **no case, no conformance, no method** to that file. Reproduced verbatim at [§4.1](#41-nav-surface-state-t-032s-contract-reproduced-verbatim) so `ios-developer` need not open the other TRD to get it right — and, per T-036's own re-review note, **if T-032's §4.1 changes before either task builds, §4.1 here is stale by definition and `trd-review` should diff the two.**

### 2.3 Where the surface sits — T-032's z-order, one row changed

T-032 §2.3's table is the layering contract. Search occupies the same z5 slot the heat modal does, and changes exactly one row's behaviour:

| z | Layer | Behaviour while `.search` is presented |
|---|---|---|
| 0 | `Map` + `HoodLayer` + `PlaceLayer` + `UserAnnotation` | **Changed by this task:** non-matching Hood fills and pins dim (§4.10). Everything else unchanged. |
| 1 | `EdgeHint` | Hidden — T-032 §4.10's availability rule, unchanged. |
| 2 | `EdgeHourZone` | Not in the hierarchy — T-032 D7 rule (c), unchanged. |
| 3 | Tap-catcher (T-032's "scrim") | **Changed by this task:** for `.search` it renders at **opacity 0** and still hit-tests; tap → dismiss (D3). No such layer exists in the tree today — C9 creates it if T-032's has not landed. |
| 4 | Bucket-2 chrome (`NearMeButton`, `HoodButton`, `SettingsHint`, `PlacesButton`) | `.opacity(0)` + `.allowsHitTesting(false)`, unchanged — and already driven by `chrome.isPresenting` in the tree (`PlacesButton(isFaded:)`), so `.search` inherits it with no new code. |
| 5 | `SearchOverlay` | The surface. Two heights (D2). |
| 6 | `EdgeHourTrack` | Cannot be active while a surface is presented — unchanged. |
| 7 | `MapNavRow` (incl. the new search button) | Always visible, always hit-testable, never covered — unchanged, and the reason D1 is what it is. |

**Why z3 changes.** PRD req 4 requires the map to dim *everything except matching pins and Hoods*. A uniform scrim across the whole map is the opposite of that requirement: it would darken the matches too, and the selective dim underneath it would be invisible. So for `.search` the z3 layer keeps its two structural jobs — tap-outside dismissal, and stopping a stray map tap opening a Hood sheet underneath the surface — and gives up its only visual one. The visual separation is carried by the selective dim at z0, which is what the requirement actually asks for.

---

## 3. Data model

### 3.1 No new persisted state, anywhere

Nothing in this feature is written to disk, `UserDefaults`, `@AppStorage`, or a cache. The query text and the chip selection live in one in-memory `@Observable` owned by `MapScreen` for the life of the process (§4.6). PRD req 7's "nothing persists across launches" is therefore a property of where the value lives, not of a reset routine someone could forget to call — the same construction T-032 §3.1 uses for `selectedHour`.

No location, device id, or user id is read, derived, or stored by any file in this feature. `grep` for `CoreLocation`/`LocationStore` over `Search/` and `SearchSheet/` returning zero hits is a §9 pass condition, not a claim — which is also how PRD req 6's "location denied changes nothing" is discharged.

No schema change, no migration, no new request. **This feature makes no network call at all**, in any build phase: matching runs against catalogs the map has already loaded.

### 3.2 `Place` gains one field: `keywords`

T-042 §3 D5 (adopted from T-033's own recommendation, confirmed by `developer` and `code-reviewer` at `trd-review`) assigns each of the four wider `places` columns to the task that first reads it, and names **`keywords` → T-038**. This is that task. `Place.swift`'s own live comment says the same thing by name, so nothing here is a reinterpretation.

```swift
struct Place: Identifiable, Sendable {
    let id: String
    let name: String
    let category: PlaceCategory
    let hoodID: String
    let coordinate: CLLocationCoordinate2D
    let permanentlyClosed: Bool   // T-036's, already in the tree — not touched here
    let keywords: [String]        // this task's one addition
}
```

**Field name confirmed against the owning spec, not assumed** (dispatch brief's explicit ask): `prds/places-dataset/TRD.md` §3.2 declares the column as

```sql
keywords           text[] not null check (cardinality(keywords) > 0),
```

and §4.4's contracted `GET` lists it as `keywords`. The Phase-1 bundled seed already carries the same key — `Passenger/Resources/places-tel-aviv.json`, verified by reading it: all nine rows have a `"keywords": [...]` array (`["nightlife","cocktails"]`, `["shakshuka","north-african"]`, …). So the wire name, the column name and the bundle key are one word, `keywords`, and nothing about it is being invented here.

**Boundary rule — non-optional, matching the field beside it.** `keywords` is declared **non-optional** in `SeedFile.Entry`, `PlacesAPI.PlaceRow` and `PlacesCache.CachedPlace`, so an absent key is a decode failure with the shipped designed fallback, not a silent `[]`. This is deliberately the same policy `permanentlyClosed` was given four lines above it in the same struct (T-036 §3.2, D1): two adjacent fields in one `Decodable` with two different tolerance policies is a thing a reader has to reverse-engineer, and there is no reason for the difference here — T-042's column is `text[] not null`, so an absent array is a malformed bundle, i.e. a build defect, which is exactly what `passenger-code/CLAUDE.md`'s fail-fast rule covers.

**But an *empty* array decodes fine and is a real value.** `[]` means "this place matches no keyword," which is degraded search on one row, not a broken bundle. T-042's `cardinality(keywords) > 0` is enforced by `validate_dataset.py` at authoring time (§8 there) and by the column constraint at Phase 2 — re-enforcing it in the client would only convert a dataset defect into an empty map. The accepted cost of the non-optional choice is stated so it is not discovered later: a seed missing the key entirely fails the whole file and `PlaceCatalog` reports `.unavailable`. C1's test is what catches that, at build time, on the nine rows that ship.

### 3.3 The search index is derived, never stored

`SearchIndex` is a value type built once from `[Place]` + `[Hood]` after both catalogs resolve, and rebuilt only if either catalog changes identity. It holds case- and diacritic-folded copies of every searchable string so that a keystroke costs a `contains` scan and not thousands of `String.folding` calls (§4.2). It is not persisted, not cached, and not observable — it is an input to a pure function.

### 3.4 Build Phase 1 — the data is the shipped seed, and one probe is not checkable here

Phase 1 reads `places-tel-aviv.json` (9 places, 3 Hoods populated) and `hoods-tel-aviv.json` (24 Hoods) via the shipped `PlaceCatalog`/`HoodCatalog`. **No new bundled artifact is added by this task** — unlike T-032 (density seed) and T-034 (event fixture), the data this feature needs already ships.

**Named rather than papered over:** strategy's own probe words — *"hummus"*, *"rooftop bar"* — appear in **neither** seed. The Phase-1 keyword values are placeholder demo values by the seed's own `_note`, and the real probe list is T-042 step **B4**, Build Phase 2. So §9's keyword row is checked against the keywords that actually ship (`"shakshuka"`, `"coffee"`, `"brunch"`), and the strategy probe list is recorded as **not checkable in Phase 1**. A zero-result probe against the real dataset is a dataset defect, not a search defect — the PRD's Technical design says so already, and §9 keeps that distinction rather than letting `qa` judge this feature on data it does not own.

---

## 4. Contracts

All of §4 is **[iOS]**. There is no second build surface to hand a contract to.

### 4.1 Nav-surface state — T-032's contract, reproduced verbatim

Copied character-for-character from `prds/time-slider/TRD.md` §4.1 as of `passenger-brain 908aa6d`, and **checked against the file now sitting in the `passenger-code` working tree** (`Map/MapChromeState.swift`, untracked, written by T-036's build): same four cases, same four conformances, `toggle` implemented as `presented = (presented == surface) ? nil : surface`, `dismiss` as `presented = nil`. T-038 **consumes** this and adds nothing to it.

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

`.search` is already a member. PRD req 1's fourth bullet ("opening search closes whichever of {heat modal, Places list, Profile} is open") is satisfied by `toggle`'s existing exclusivity, with no code in this feature.

### 4.2 `SearchIndex` — fold once, scan many

```swift
struct SearchIndex: Sendable {
    struct PlaceEntry: Sendable {
        let place: Place
        let foldedName: String
        let foldedKeywords: [String]     // parallel to place.keywords, same order
        let foldedHoodName: String       // for the row's Hood label only, not matched
    }
    struct HoodEntry: Sendable {
        let hood: Hood
        let foldedName: String
    }

    let places: [PlaceEntry]
    let hoods: [HoodEntry]

    static let empty = SearchIndex(places: [], hoods: [])
    static func build(places: [Place], hoods: [Hood]) -> SearchIndex

    /// The single folding rule, used for both index entries and the live query.
    static func fold(_ s: String) -> String    // s.folding(options: [.caseInsensitive, .diacriticInsensitive], locale: nil)
}
```

**The folding rule is T-042 §4.3's, adopted unchanged, not re-derived:** `String.folding(options: [.caseInsensitive, .diacriticInsensitive])`, because Tel Aviv keywords may be Hebrew or English and both fold. `locale: nil` is explicit so the result does not vary with device locale — a search index whose contents depend on the user's region setting is a bug nobody would find. T-042 specifies the rule for keywords; this TRD extends the identical rule to place names and Hood names, so one query string never matches one field and misses another for a reason the user cannot see.

### 4.3 `SearchResult` — what a row is

```swift
enum SearchResultKind: Sendable, Equatable {
    case hood(Hood)
    case place(Place, matchedKeyword: String?)   // nil == matched on name
}

struct SearchResult: Identifiable, Sendable, Equatable {
    let kind: SearchResultKind
    var id: String                 // "hood:\(id)" / "place:\(id)" — never collides
    var displayName: String        // hood.name / place.name
    var typeWord: String           // "Hood" / "Place"  (D9)
    var voiceOverLabel: String     // §4.8
}
```

`matchedKeyword` is carried because the matcher knows it for free and a later pass (P1 sectioning, or a "matched on: hummus" line) would otherwise need the matcher rewritten. **Nothing renders it in V1** — see D9.

### 4.4 `SearchQuery` — the pure matcher

```swift
enum SearchQuery {
    /// Synchronous, pure, total. No `async`, no `Task`, no debounce.
    static func run(_ rawText: String, filter: CategoryFilter, in index: SearchIndex) -> [SearchResult]
}
```

Rules, in order:

1. `let q = SearchIndex.fold(rawText.trimmingCharacters(in: .whitespacesAndNewlines))`.
2. **If `q.isEmpty` and `filter == .all` → `[]`.** This *is* PRD req 6's empty-field state; it is not an error branch.
3. **If `q.isEmpty` and `filter == .only(c)` → every place of category `c`, name-ascending, no Hoods.** This is PRD req 3's "a chip with an empty field produces a category-scoped result set."
4. Otherwise: a Hood matches when `foldedName.contains(q)`. A place matches when `foldedName.contains(q)` (→ `matchedKeyword: nil`) **or** any `foldedKeywords` element contains `q` (→ that keyword, first match in authored order). Name match wins over keyword match for the same place; a place is never returned twice.
5. Apply `filter` to **places only** (D8).
6. Order (D7): Hood name matches, then place name matches, then keyword-only place matches; **case-insensitive `<` on the unfolded display name within each group.** Deterministic, so `qa` can assert an exact array.

**Substring, not prefix, not fuzzy** — T-042 §4.3 pins this ("`"roof"` hits `"rooftop bar"` mid-type") and the PRD's open technical question is answered by adopting the owning spec's answer rather than inventing a second one.

**Why there is no debounce and no `async`.** `run` is a synchronous scan of pre-folded strings. At T-042's own stated ceiling (~2,000 places, ~6 keywords each) that is ~14,000 `String.contains` calls on short strings — sub-millisecond, well inside one frame, let alone req 2's 400ms. Introducing a debounce or a `Task` would buy nothing and would create the one bug class this design has none of: an out-of-order result set rendering after a newer keystroke. §9 row 2 makes the performance claim falsifiable at 2,000 rows rather than asserting it.

### 4.5 `CategoryFilter` — two chips, no dead state

```swift
enum CategoryFilter: Sendable, Equatable {
    case all
    case only(PlaceCategory)

    static let fresh = CategoryFilter.all           // PRD req 3: both active on fresh open
    func isActive(_ c: PlaceCategory) -> Bool       // .all -> true for both
    func toggling(_ c: PlaceCategory) -> CategoryFilter   // .all -> .only(c); .only(c) -> .all; .only(other) -> .only(c)
}
```

Exactly two chips exist because `PlaceCategory` has exactly two cases and no `.other` (shipped, `PlaceCategory.swift`). `CategoryChipRow` iterates `PlaceCategory.allCases` — adding a third chip would require adding a case to an enum whose own doc comment forbids it, which is the strongest available form of PRD req 3's "no third chip ships."

Deselecting into an empty set is **unrepresentable**, not merely prevented: there is no `.none`. Tapping the single lit chip returns to `.all`. This is Poka-Yoke at the control (`design-principles.md` §2) and removes a state — "no categories selected, therefore no results, for a reason the user cannot see" — that no requirement asks for.

### 4.6 `SearchSession` — the state that survives an interruption

```swift
@MainActor @Observable
final class SearchSession {
    var text: String = ""
    var filter: CategoryFilter = .fresh

    /// The ONLY mutation that resets both. Called from exactly three paths (D10).
    func clear() { text = ""; filter = .fresh }
}
```

Owned by `MapScreen` as `@State`, not by `SearchOverlay`. A view that leaves the hierarchy takes its `@State` with it, so query text held inside the overlay would die on every nav switch — which is precisely what PRD req 7 forbids. One storage location, so there is no second property to desync (T-032 §3.1's discipline, applied to a different value).

`clear()` is called on, and only on:

| Path | Clears? | Why |
|---|---|---|
| Result tapped | **yes** | Completion (PRD req 7 bullet 2) |
| `SearchOverlay`'s ✕ | **yes** | Manual dismissal |
| Drag-down past threshold | **yes** | Manual dismissal |
| z3 tap-outside | **yes** | Manual dismissal |
| Search button tapped while `.search` is presented | **yes** | Manual dismissal — `toggle` closes it, and the user aimed at the control |
| `toggle(.heat)` / `.places` / `.profile` | **no** | Interruption (PRD req 7 bullet 1) |
| `MapChromeState.dismiss()` from any other cause | **no** | Not a user dismissal of *search* |

This table is the whole of PRD req 7, and it is why `clear()` is not wired to a `MapChromeState` observer: "the surface closed" and "the user finished with it" are different events, and only the second one clears. `ux-flows.md` §6's 2026-07-29 reconciliation is the source, and it is still flagged there as needing Aviran's confirmation — carried forward unresolved (§8, D10).

### 4.7 `SearchOverlay` — the container

```swift
struct SearchOverlay: View {
    @Bindable var session: SearchSession
    let results: [SearchResult]
    let onSelect: (SearchResult) -> Void
    let onDismiss: () -> Void            // routes to clear() + chrome.dismiss()
}
```

- **Two heights, not system detents** (D2): `compact` = 0.45 × container height, `expanded` = 0.92. Compact is the fresh-open height. A drag on the handle past a distance/velocity threshold moves between them; a drag below compact dismisses. Same three dismissal routes T-032's modal card has (handle drag, z3 tap, another nav button), all routed through `MapChromeState`, none through a private `@State` bool.
- Background: opaque `Color("Surface")` (T-031's token, reused). **Not `.ultraThinMaterial`** — same reasoning T-031 §8 D1 and T-032 §4.2 both give: a contrast ratio against a translucent layer over a live map is not a number anyone can verify.
- Transition `.move(edge: .bottom).combined(with: .opacity)`; under `\.accessibilityReduceMotion` it cross-fades with no movement.
- The result list is a `ScrollView` + `LazyVStack`, not a `List` — a `List`'s own separators and insets fight the container, and nothing here needs swipe actions or selection chrome.

### 4.8 The row-level views

```swift
struct SearchFieldRow: View {           // visible Text label ABOVE the field (PRD req 2 bullet 4)
    @Binding var text: String           // `design-principles.md` §3: placeholder-as-label is banned
}
struct CategoryChipRow: View {
    let filter: CategoryFilter
    let onToggle: (PlaceCategory) -> Void
}
struct SearchResultRow: View {
    let result: SearchResult
}
```

- **Chip selected state without colour** (PRD req 3 bullet 5): a selected chip renders a leading `Image(systemName: "checkmark")` and `.font(.subheadline.weight(.semibold))`; an unselected one renders neither. The distinction survives a greyscale screenshot, which is how §9 checks it.
- **Row content** (PRD req 4 bullet 7): name, then a secondary line reading `"\(typeWord) · \(category.displayName) · \(hoodName)"` for a place and `"Hood"` for a Hood. **No tourist-trap line, ever** — the flag has one home (T-035 req 6), and `SearchResultRow` referencing `isTouristTrap` at all is a §9 failure.
- **VoiceOver strings, pinned exactly** (PRD req 8 bullet 2): `"Florentin, Hood"` and `"Anna Loulou Bar, place, Eat & Drink"`. Note the PRD's own casing — the type word renders capitalised (`"Hood"` / `"Place"`) and speaks lowercase for a place (`"place"`), matching req 8's literal example. Pinned here because a string nobody wrote down is a string that drifts.
- **Dynamic Type:** no `.lineLimit` anywhere in these three views, and `.fixedSize(horizontal: false, vertical: true)` on every text run, so rows grow rather than truncate (PRD req 8 bullet 3).
- Every chip and every row has a ≥44pt height via `.frame(minHeight: 44)` (PRD req 8 bullet 1, `design-principles.md` §2).

### 4.9 Wiring in `MapScreen`

New state, three properties:

```swift
@State private var chrome = MapChromeState()          // shared with T-032/T-036; created once
@State private var searchSession = SearchSession()
@State private var searchIndex = SearchIndex.empty
```

`searchIndex` is rebuilt in the existing `.task`s once `placeCatalog.load()` and `loadHoods()` have both resolved — off the cold-open path, so T-031's "nothing awaits before the first frame" is untouched. Results are a computed property, not stored state:

```swift
private var searchResults: [SearchResult] {
    SearchQuery.run(searchSession.text, filter: searchSession.filter, in: searchIndex)
}
```

**Presentation exclusivity — T-036 D8/§4.6's two calls, reused unchanged:**

- **Opening `.search` calls `router.closeHood()` first.** Otherwise tapping the search button with a Hood sheet already open presents the overlay *underneath* a system sheet, in a layer that can never be reached.
- **Leaving `.search` by any path calls `router.closeHood()`.** `closeHood()` clears both fields, which is the correct call here (unlike T-036's `closePlace()`) because search can produce *either* destination, and neither should outlive the surface it was opened from.

**Result selection** is the existing depth-1 sheet site — no new `.sheet` modifier, no new presentation mechanism, no `DetailRouter` change:

```
place result  -> searchSession.clear(); router.openPlace(place)
hood  result  -> searchSession.clear(); camera = .region(regionFitting(hood)); router.openHood(hood)
```

`regionFitting(hood)` is `MKCoordinateRegion(hood.boundingRect)` with a small padding factor — `boundingRect` already ships on `Hood`, so no new geometry is introduced. The pan is issued *before* `openHood` so the camera move is committed under the sheet rather than fighting it.

**On the depth ladder, so nobody "fixes" it later.** `ux-flows.md` §5 counts search as level 1 and the destination as level 2; `DetailRouter.placeDepth` counts *sheet* depth only and reports 1 for a place opened from search. These are two different rulers measuring the same stack, both correct. PRD req 5 bullet 3's ceiling is enforced by there being exactly two `.sheet(` sites in the whole app (§9 row 5), not by `placeDepth`.

### 4.10 The dim

`HoodLayer` and `PlaceLayer` each gain one input:

```swift
struct HoodLayer: MapContent {  let hood: Hood; let band: HeatBand?; let showsName: Bool; let isDimmed: Bool }
struct PlaceLayer: MapContent { let place: Place; let isListed: Bool; let isDimmed: Bool; let action: () -> Void }
```

`PlaceLayer.isListed` is T-036's, already in the tree, and is **not** touched: dimming and the personal-place ring are independent axes, and a dimmed pin keeps its ring at the same reduced opacity as the rest of it. Collapsing the two into one "emphasis" enum would make a listed place's ring depend on whether a search is open, which no requirement asks for.

`isDimmed` multiplies the layer's own opacity by `0.25`; when `false` the rendering is byte-identical to what ships today, so the non-search path cannot regress. **"Every visible element" includes the Hood polygon's heat fill, and that is the element the requirement is actually about** — the fill dominates a 0.5pt stroke and a centroid capsule, so a dim that reaches only the stroke and the label is not a dim a user sees (PRD req 4 bullet 2). The fill's dim is therefore a *numeric* composition, `HeatPalette.fillOpacity(for:dimmedBy:) == opacity(for: band) * dimOpacity`, not a view modifier: it makes "does the dim reach the heat fill" a unit-testable question about two `Double`s instead of a fact about a SwiftUI modifier chain no test can observe. A `nil` band stays `.clear` either way — dimming a fully transparent fill has nothing to multiply.

The dim set is computed in `MapScreen` from one pure function:

```swift
enum SearchDim {
    /// nil == no dimming at all (no surface, or no results).
    /// A place match emphasises BOTH the place and its own Hood.
    static func emphasis(results: [SearchResult]) -> (places: Set<Place.ID>, hoods: Set<Hood.ID>)?
}
```

**A place match emphasises `place.hoodID` as well as `place.id`, and that is load-bearing, not incidental.** `MapScreen` gates its `PlaceLayer` `ForEach` on `showsNames` (`zoomTier == .close`, span < 0.06), while the shipped cold-open camera is `telAvivCityWide` at span **0.14**. So at the cold-open zoom — and at every zoom with span ≥ 0.06, which is also the permanent state for a location-denied user (PRD req 6 bullet 5) — **there is no place pin on screen to emphasise.** Emphasising the matched place's own Hood gives the requirement a surface that exists at every zoom, because `HoodLayer` has no zoom gate (only its name label does). The accepted cost: a Hood match and a place match inside that Hood produce the same dim set. That is acceptable because the requirement is that *something* is emphasised, not that the emphasis set proves which kind of match caused it.

**A stated limit, narrow but real — routed to `product`, not decided here.** The emphasis is carried by the matched Hood's fill staying at full strength while the others drop to 0.25. If the matched place's Hood has **`band == nil` at the selected hour**, its fill is `.clear` and there is no full-strength fill to contrast — the map still changes visibly (the other 23 fills dim), so PRD req 4 bullet 3's literal test ("a screen where opening search and typing a match changed nothing a user can see is a fail") is still met, but the emphasis is carried entirely by the *absence* of dimming elsewhere rather than by any positive mark on the match. §9 row 4(a) requires the fixture's matched Hood to carry a non-`nil` band and records the `nil`-band case as a **named limit**, not as a passing check.

`nil` whenever `.search` is not presented **or** `results.isEmpty` — so an empty field dims nothing (there is nothing to emphasise) and the map reads normally, and the instant a result is tapped or the surface closes, `emphasis` returns `nil` and the dim is gone (PRD req 4 bullet 2). Because `emphasis` is derived from `searchResults` on every render pass, there is no dim state to leave stale.

**One stated limit, not discovered at `qa`.** "Dims everything except matching pins and Hoods" is implemented over the layers Passenger draws — Hood polygon fills, Hood name labels, place pins. **MapKit's own base tiles are not dimmed**, because SwiftUI's `Map` exposes no layer between the tiles and the annotations to insert one into, and a full-screen scrim above the tiles would also darken the matches (§2.3). The accepted reading is that all *Passenger-authored* content except the matches is de-emphasised, which is the channel the requirement is about (`ux-flows.md` §6: "search filters what's visually prominent"). Flagged for `product` at review rather than assumed.

---

## 5. Flow

**Open.** Tap the search button in `MapNavRow` → `router.closeHood()` → `chrome.toggle(.search)` → z3 tap-catcher becomes hit-testable at opacity 0, bucket-2 chrome fades at z4, `SearchOverlay` slides in at z5 at compact height, nav row stays live at z7. `searchSession` is whatever it was (empty on first open, restored if a previous session was interrupted). `searchResults` recomputes; with an empty field and `.all` it is `[]`, so no dim and no list.

**Type.** Each keystroke writes `searchSession.text`; `searchResults` recomputes synchronously on the same render pass; the list and the map dim update together, never out of step, because both read the same computed array.

**Chip.** Tap "Eat & Drink" → `filter = filter.toggling(.eatDrink)` → same recompute. With an empty field this produces the category-scoped set; with a typed query it narrows it. Hood results are unaffected (D8).

**Select a place.** `clear()` → `router.openPlace(place)` → the shipped depth-1 `.sheet` presents `PlaceDetailModal` above the overlay, carrying `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` exactly as it does for a pin tap. The dim is gone the same frame, because `searchResults` is now `[]`. Dismissing the modal reveals the overlay in its empty state.

**Select a Hood.** `clear()` → camera moves to the Hood → `router.openHood(hood)` → the shipped `HoodSheet` presents. Same sheet three doors already reach (`ux-flows.md` §5).

**Interrupt.** Tap the heat button → `chrome.toggle(.heat)` → `router.closeHood()` (leave-search call) → overlay leaves, `searchSession` untouched. Tap search again → the query and chip come back.

**Dismiss.** ✕ / drag past threshold / tap the map / re-tap the search button → `clear()` → `router.closeHood()` → `chrome.dismiss()`. Camera and `selectedHour` are untouched by every path above; no file in this feature reads or writes either, except the one deliberate camera write on a Hood result.

**Edge and error paths.** No match → one line naming the query, field keeps focus. Offline → structurally identical, because nothing here fetches. Location denied → structurally identical, because nothing here imports `CoreLocation`. A Hood with no blurb → the shipped `HoodSheet` empty state, unchanged. A result whose Hood has no density at the selected hour → the shipped no-fill treatment, which is silence, not an error.

---

## 6. Third-party / dependencies

**None.** No new SDK, no new service, no account, no cost. Everything is Foundation, SwiftUI and MapKit types already in the project.

`SALVAGE.md` marks `Services/PlaceSearchService.swift` REUSE and the PRD says "start there." **This TRD deliberately does not salvage it.** The shape specified above is four small value types and one pure function over already-loaded catalogs; a service class implies fetching, lifecycle and injection that this feature has none of, and `passenger-code/CLAUDE.md` permits salvaging leaf code only, adapted line by line. There is less code here than the adaptation would cost. Named so the reviewer sees a decision rather than an oversight.

---

## 7. Rollout & migration

- **No feature flag.** The feature is inert until its button is tapped and it reads no server surface, so there is nothing a flag would protect.
- **No migration, client or server.** `places.keywords` already exists in T-042's approved migration `004` with the full column set; nothing is added to it here.
- **`PlacesCache` compatibility.** `CachedPlace` gains a non-optional `keywords: [String]`. A cache file written before this change fails to decode → `loadIfPresent()` returns `nil` → `PlaceCatalog.load()` falls through to the bundled seed. That is the already-shipped failure path, not a new one, and **it cannot fire in Phase 1** because `BuildPhase.seedIsAuthoritative` means the cache is never written. Same call and same reasoning T-036 D1 made for `permanentlyClosed`; a unit test pins it.
- **Build Phase 2 is a one-line diff for this feature.** `PlacesAPI`'s `select=` gains `keywords` at C1 (built now, unexercised now — the same "built and unexercised" posture `PlacesAPI` already ships in). When `seedIsAuthoritative` flips, the live payload carries keywords and nothing else in this feature moves. T-042's own §4.4 `GET` already lists `keywords`, so the two contracts agree today.
- **Backward compatibility.** `HoodLayer`/`PlaceLayer` gain a parameter with `isDimmed: false` semantics identical to today's rendering; no other caller changes behaviour.

---

## 8. Risks & alternatives

| Risk | Handling |
|---|---|
| **Sheet layout is Aviran's open call** (PRD Open questions). Built as two heights, compact default (D2). | Trivially reversible: two constants and one gesture. If Aviran holds to a literal 50/50 split, `compact = 0.5`, `expanded` removed, handle drag becomes dismiss-only. No architectural change. Flagged for `product`. |
| **Req 2 bullet 2's "which of the three it is" has two readings** (D9). Built as a two-word vocabulary. | `matchedKeyword` is carried through `SearchResult` unrendered, so the other reading is a view change, not a matcher change. Flagged for `product`. |
| **Req 7's interrupted-vs-completed rule is unconfirmed** — `ux-flows.md` §6 flags its own reconciliation as needing Aviran, and §9 Q17 is open. | §4.6's table is the single place the rule lives; changing it is editing one table and its tests. Carried forward unresolved. |
| **The keyword probe list cannot be exercised in Phase 1** (§3.4). | Stated in §9 as not-checkable rather than checked against placeholder data. Discharged at T-042 B4, Phase 2. |
| **`MapChromeState`/`MapNavRow` may be created twice** by T-032, T-036 and T-038 in an unknown order. | C5/C6 are create-if-absent against T-032's verbatim contract; T-038 adds a case to neither. Residual risk is T-032 §4.1 changing after §4.1 here was copied — `trd-review` should diff the two, exactly as T-036 §2.2 requires of itself. |
| **MapKit base tiles are not dimmed** (§4.10). | Stated as an accepted limit with the reason, flagged for `product`. |
| **Search-result-pin vs Places-list-pin distinction depends on T-036** (D12). | §9 row 8 records the check as blocked, not passed, if T-036's dashed ring has not landed. |
| The dim reads as "the map broke" to a user who does not connect it to the open sheet. | Mitigated by the dim only existing while results exist, and clearing on the same frame as selection. Worth a look in the post-ship `designer` pass; not worth a pre-build gate. |

**Alternatives considered and rejected:**

- **A system `.sheet` with `.medium`/`.large` detents + `.presentationBackgroundInteraction`** — the PRD's own Technical design line, `ux-flows.md` §2.1's instruction to T-038, and the dispatch brief's ask. Rejected; full reasoning in **D1**. It is the single largest deviation in this document and it is argued, not assumed.
- **A `NavigationStack` or `.fullScreenCover`** — violates PRD req 1 outright.
- **A debounce / `Task`-based matcher** — §4.4; buys nothing, adds an ordering bug class.
- **Prefix or fuzzy matching** — T-042 §4.3 already pinned substring; a second matching rule in the same product is how "why didn't that match?" becomes unanswerable.
- **A `SearchService` salvaged from Locali** — §6.
- **Sectioned results (places, then Hoods)** — PRD P1, deliberately not built; D7's ordering makes it a pure presentation change later.
- **A third chip / a "hide tourist-heavy spots" filter** — forbidden by PRD req 3 and structurally impossible per §4.5.
- **Dimming via a full-screen scrim above the tiles** — §2.3; darkens the matches, defeating the requirement.
- **Storing `searchResults` in `@State`** — invites a stale render and a second source of truth; a computed property cannot desync.

---

## 9. Verification — one row per P0 requirement

Per L-018 and `architect.md`. `qa` builds `TEST-PLAN.md` from this table. Where a bullet has no runnable check in Phase 1 it says so explicitly and names the owner — it is never marked passing by construction.

**Two standing rules for this table, added at v2 after row 4(a) passed while its requirement failed (L-009, T-053/`PAS-43`).** Both are about conditions that are *true for the wrong reason*:

- **No pass condition may be satisfiable over an empty set.** A condition of the form "every X has property P" is worthless without a stated non-zero count of X, because the failure mode being guarded against is usually "no X was produced at all." Every ∀ in this table is paired with an exact count or an exact expected array.
- **Every negative-existence check needs a positive control.** Eleven sub-checks below are `grep … → 0 hits`, which passes identically whether the forbidden symbol is absent or the grep covered nothing. Each one is run alongside a second grep over the same paths for a symbol that **must** be present (`SearchQuery`, `SearchResultRow`) returning **> 0 hits**; a zero there means the path list is wrong and the whole row is unrun, not passed.

And the reason both exist: **a requirement is verified at the layer the user perceives it, never at the value handed to that layer.** `isDimmed == true` is an input to rendering; the check belongs on what rendered.

| # | P0 requirement | Observable | Pass condition | Layer | Step |
|---|---|---|---|---|---|
| **1** | One door, one sheet, never a destination | (a) presentation sites in the app; (b) `camera` + `densityStore.selectedHour` across open→dismiss; (c) `chrome` after `toggle(.search)` with `.heat` presented; (d) `router.hood` after opening `.search` with a Hood sheet up | (a) `grep -rn "fullScreenCover\|NavigationStack\|NavigationLink" Passenger/Search Passenger/SearchSheet` → **0 hits**; (b) `MKCoordinateRegion`'s four components byte-identical across three samples and `selectedHour` unchanged; (c) `presented == .search`; (d) `router.hood == nil` | unit + UI test | C9, C11 |
| **2** | One field matches three kinds | (a) `SearchQuery.run("suzan", .all, seedIndex)`; (b) `run("shakshuka", …)` and `run("coffee", …)`; (c) `run("Florentin", …)`; (d) wall time of `run` at a synthetic 2,000-place index; (e) the field's visible label | (a) exactly `["Suzana Yemenite Kitchen", "Suzanne Restaurant"]` in that order — two place results, both name matches, drawn from two different Hoods, zero Hood results; (b) exactly `["Dr. Shakshuka"]` and `["HaMakolet"]`, each with `matchedKeyword` set; (c) exactly one result, `kind == .hood`; (d) **≤ 16ms** (one frame) per call, index build ≤ 250ms — **and the timed call must return a stated non-zero result count** (a query chosen to match ≥ 100 of the 2,000 synthetic rows, asserted before the timing is read). A matcher that returns `[]` instantly satisfies a bare time bound, so the bound alone proves nothing; (e) a `Text` label element exists **and** is not the `TextField`'s prompt — UI test finds both a static text "Search" and a text field. **Not checkable in Phase 1: strategy's own probe words "hummus"/"rooftop bar" are in neither seed** (§3.4) — owner T-042 step B4, Build Phase 2 | unit + UI test | C2, C3, C7 |
| **3** | Two chips, quick filters and nothing more | (a) chips rendered; (b) `run("", .only(.eatDrink), seedIndex)`; (c) `run("b", .only(.eatDrink))` vs `run("b", .all)`; (d) `SearchSession()` fresh; (e) a selected chip in greyscale; (f) chip construction sites | (a) exactly 2, and `PlaceCategory.allCases.count == 2`; (b) exactly the six `eat-drink` seed places, name-ascending, zero Hoods; (c) **the exact array first, the ∀ clauses second** — `run("b", .only(.eatDrink))` is exactly `["Bavli" (Hood), "Anna Loulou Bar", "HaMakolet", "Suzanne Restaurant"]` in that order (one Hood match; one place name match; two keyword-only matches on `"brunch"`, name-ascending), against `run("b", .all)`'s exactly `["Bavli" (Hood), "Anna Loulou Bar", "Carmel Market Spice Corner", "HaMakolet", "Suzanne Restaurant"]` — so the chip removes exactly `Carmel Market Spice Corner` (`things-to-do`) and **keeps the Hood**, which is D8 made falsifiable. Both arrays are **non-empty**, and only then do the two v1 clauses run as confirmations: result ⊆ the `.all` results, and every *place* in it is `.eatDrink`. **They cannot carry this row alone — both hold over `[]`**, which is exactly how a matcher returning nothing would have passed. Values derived from the shipped seed at v2; if they and `SearchShippedSeedTests` ever disagree, the test's real output wins and this cell is stale (the §9 row 2 precedent); (d) `filter == .all`, both chips render selected; (e) selected chip carries a `checkmark` symbol, unselected carries none — distinguishable with colour removed; (f) `grep -rn "CategoryChipRow(" Passenger` → exactly one call site | unit + UI test | C3, C7 |
| **4** | Search filters the map at the selected hour; no second view of the data | (a) **the map's rendered heat fills**, at a place-only query matching one place in one Hood whose band is **not** `nil` at the selected hour, run at **both** `.cityWide` (span 0.14, the cold-open camera) and `.close` (span < 0.06); (b) the **same rendered fills** after a result is selected and after the sheet is dismissed; (c) fetch surface of the feature; (d) the call made on a place-result tap vs a pin tap; (e) hour surface of the feature; (f) a result whose Hood has `band == nil` at the selected hour; (g) `SearchResultRow`'s content | (a) **at each of the two tiers, and stated as counts before any ∀:** all 24 `HoodLayer`s are constructed; **exactly one** is undimmed and it is the matched place's own Hood; that Hood's **resolved fill alpha** (`HoodLayer.fillColor` → `UIColor.cgColor.alpha`) is **unchanged** from its no-search value, and **every one of the other 23** resolves to an alpha **strictly less** than its own no-search value at the same band — i.e. the assertion is on the fill channel, not on `isDimmed`, not on the stroke, and not on the centroid label. **At `.cityWide` the `PlaceLayer` count is asserted to be `0`** — that is the zoom tier this row's v1 condition was vacuously true at, so it is now the tier the check is *required* to cover, and the emphasis must be carried entirely by Hood fills there. Sanity-anchor the fixture first: the matched Hood's band is non-`nil`, otherwise the run is **BLOCKED, not passed** (the `nil`-band limit is named in §4.10 and flagged for `product`); (b) the previously-dimmed 23 Hoods' resolved fill alphas are **back at their no-search values** in both cases — `emphasis == nil` is checked too, but as the cause, never as the evidence; (c) `grep -rn "URLSession\|PlacesAPI\|DensityAPI\|fetch" Passenger/Search Passenger/SearchSheet` → **0 hits**; (d) both are `router.openPlace(p)` with an identical `Place` — assert `router.place == p`; (e) `grep -rn "selectedHour" Passenger/Search Passenger/SearchSheet` → **0 hits** (the hour is session-scoped per T-032 §3.1, so "never an hour cached from a past session" holds structurally); (f) `HoodLayer.fillColor == .clear`, no alert, no error copy; (g) `grep -rn "isTouristTrap\|tourist\|Flag" Passenger/SearchSheet` → **0 hits** | unit + UI test + manual (visual dim) | C10, C11, C8 |
| **5** | A result goes where the map would have gone | (a) place result tap; (b) Hood result tap; (c) presentation-site count; (d) exit surface | (a) `router.place == the tapped place`; (b) `router.hood == the tapped hood` **and** the camera's centre lands within 200m of `hood.centroid`; (c) `grep -rn "\.sheet(isPresented:" Passenger` → **exactly 2 call sites in view code** (`MapScreen` site A, `HoodSheet` site B — doc-comment mentions in `DetailRouter` don't count and don't match this pattern) and `router.placeDepth ?? 0 <= 2` in every case; (d) `grep -rn "openURL\|DirectionsService\|UIApplication.shared" Passenger/Search Passenger/SearchSheet` → **0 hits** | unit + UI test | C11, C14 |
| **6** | Every state specified, none a dead end | (a) empty field, `.all`; (b) query `"zzzz"`; (c) offline; (d) selecting the Hood `Lev HaIr` from search; (e) location surface | (a) `results.isEmpty` **and** the UI shows two chips, no list rows, no suggestion rows; (b) exactly one line whose text contains `"zzzz"` verbatim, the text field still holds keyboard focus and still contains `"zzzz"`; (c) discharged by row 4(c) — nothing fetches, so offline is the only mode. **The staleness label itself is not observable in Phase 1**: `CachedDataIndicator` is driven by `densityStore.source == .cache`, unreachable while `BuildPhase.seedIsAuthoritative` is `true` — named, owner T-032/T-042 at Phase 2; (d) the shipped `HoodSheet` renders its own null-blurb + zero-places empty state, unchanged (`lev-hair` is seeded for exactly this); (e) `grep -rn "CoreLocation\|LocationStore\|CLLocation" Passenger/Search Passenger/SearchSheet` → **0 hits** | unit + UI test | C12 |
| **7** | In-progress state survives an interruption, not a completion | (a) type `"flor"`, tap a chip, `toggle(.heat)`, `toggle(.search)`; (b) tap a result; (c) each of the four manual-dismiss paths; (d) persistence surface | (a) `session.text == "flor"` **and** `session.filter == .only(...)`; (b) `session.text == ""` **and** `session.filter == .all`; (c) the same cleared state after **each** of ✕, drag-past-threshold, z3 tap, re-tap of the search button — four separate assertions, not one; (d) `grep -rn "UserDefaults\|AppStorage\|FileManager\|\.write(to:" Passenger/Search Passenger/SearchSheet` → **0 hits** | unit + UI test | C4, C9, C11 |
| **8** | Reach and accessibility | (a) frames of the search button, both chips, every row; (b) VoiceOver labels of one Hood row and one place row; **(c-i)** result **rows** at `UICTContentSizeCategoryAccessibilityExtraExtraExtraLarge`; **(c-ii)** the **chip row** at that same size — the surface that actually overflows, and the one v1 never named; (d) a search-match pin beside a Places-list pin | (a) **the element counts are asserted first** — 1 search button, exactly 2 chips, and the row count of a query with a known non-empty result set — **and only then** does every one of them report `frame.height >= 44` and `frame.width >= 44`. Without the counts the ∀ passes on a screen that rendered nothing; (b) exactly `"Florentin, Hood"` and `"Anna Loulou Bar, place, Eat & Drink"`; **(c-i)** with the row count asserted non-zero, each row's rendered height is strictly greater than at the default size **and** no row's label renders an ellipsis; **(c-ii)** **both chip labels render in full** — `"Eat & Drink"` and `"Things to do"` each read back complete, with no ellipsis and no clipping, and each chip's rendered height is strictly greater than at the default size. The two chips sit in a fixed, non-wrapping `HStack`, so at this text size they must wrap, scroll, stack, or grow vertically rather than compress. **`grep` for `.lineLimit` does not check this** — `.lineLimit` is not what truncates inside an overflowing `HStack`; `.fixedSize(horizontal: false, vertical: true)` on each chip's `Text` is, and a structural guard that greps only for the absence of `.lineLimit` passes while the chips truncate (PRD req 8's bullet added at acceptance 2026-08-03); (d) the two differ by T-036's **dashed ring** (`StrokeStyle(lineWidth: 2.5, dash: [4, 3])`, in the tree today) in a greyscale screenshot — search adds no pin treatment of its own (D12). **If that diff is not present at build time, this sub-check is BLOCKED, not passed** — record it as unrun | UI test + manual | C6, C7, C8, C13 |

---

## 10. Build breakdown

**Every step is `[iOS]`. There is no `[Backend]` and no `[Algo/Data]` step**, verified three ways rather than inferred from the PRD's "no new tables" line:

1. **The one server field this feature reads already has an owner and an approved artifact.** `places.keywords text[] not null check (cardinality(keywords) > 0)` is in T-042's TRD §3.2, in migration `004_places.sql`, `trd-review`-approved and `security-auditor`-PASS. Nothing is added to it, altered in it, or newly indexed — T-042 §4.3 states outright that no server-side query filters on keywords, so no index is owed either.
2. **Phase 1 makes no request at all.** `BuildPhase.seedIsAuthoritative == true`, so `PlaceCatalog.load()` short-circuits to the bundled seed and `PlacesAPI.fetchPlaces()` is never called. The `select=` widening at C1 ships built and unexercised, exactly as `PlacesAPI` already does.
3. **No server-side artifact changes shape.** T-042 §4.4's contracted `GET` **already lists `keywords`** in its column set — so this task's client edit brings the client up to a contract the backend TRD wrote first, rather than asking the backend for anything. `hoods.name`, the other matched field, is shipped and unchanged.

No `[Algo/Data]` step either: the seeds this feature reads exist and are unchanged, and the one dataset deliverable it depends on (the keyword probe list) is already T-042 step **B4**, not a new job (§3.4).

| # | Step | Tag |
|---|---|---|
| **C1** | `Place.keywords` threaded through **all three** source paths — seed `SeedFile.Entry`, `PlacesAPI.PlaceRow` **and** its `select=` string, `PlacesCache.CachedPlace` — **non-optional in all three**, matching the `permanentlyClosed` field already beside it (§3.2). Tests: the shipped nine seed rows decode their authored keywords; a row carrying `"keywords": []` keeps the place and matches nothing; a seed with the key absent fails the file and reports `.unavailable`; a pre-change cache payload fails decode and falls through to seed (§7) | **[iOS]** |
| **C2** | `SearchIndex` — `fold` (T-042 §4.3's rule, `locale: nil`), `build`, `empty`. Unit tests incl. a diacritic and a Hebrew string | **[iOS]** |
| **C3** | `CategoryFilter` + `SearchResult` + `SearchQuery.run` — all five rules of §4.4, D7's ordering, D8's places-only filtering. Unit tests are §9 rows 2 and 3, incl. the **2,000-row synthetic performance assertion** | **[iOS]** |
| **C4** | `SearchSession` + `clear()`; the §4.6 table's seven paths as seven assertions (§9 row 7) | **[iOS]** |
| **C5** | `MapChromeState.swift`: **as of this draft the file exists and is already correct — verify it against §4.1 and add nothing. If it has gone from the tree by build time, create it exactly per §4.1, all four cases and all four conformances, verbatim.** Either way `.search` is already a member and this task modifies that file in neither direction. The exclusivity unit test (`toggle` swaps rather than stacks; `toggle` on the presented surface dismisses) is T-038's regardless of who wrote the type | **[iOS]** |
| **C6** | `MapNavRow.swift` — **does not exist as of this draft.** If absent, create it per T-032 D1/D6: separate side-by-side buttons, no shared container chrome, carrying the search button only. If T-032's C2 has landed first, add the search button and change nothing else. `SearchButton`: icon-only `Image(systemName: "magnifyingglass")`, no caption (`ux-flows.md` 2026-08-02 founder-direct addendum), `.accessibilityLabel("Search")`, 44×44 in the `NearMeButton` floating-chrome idiom. **`PlacesButton` is not the precedent** — it is bucket-2 chrome outside the row (T-036 D7) | **[iOS]** |
| **C7** | `SearchFieldRow` (visible `Text` label, never placeholder-as-label) + `CategoryChipRow` (two chips, checkmark selected state, ≥44pt) | **[iOS]** |
| **C8** | `SearchResultRow` — name, secondary line, pinned VoiceOver strings, no `.lineLimit`, no flag line | **[iOS]** |
| **C9** | `SearchOverlay` at z5 — two heights (D2), drag handle, 44×44 ✕, Reduce-Motion-aware transition, opaque `Color("Surface")`; the **opacity-0 hit-testing z3 tap-catcher** for `.search` (D3). **No z3 layer exists in the tree** — if T-032's scrim has landed by build time, give it a per-surface opacity rather than adding a second layer | **[iOS]** |
| **C10** | `SearchDim.emphasis` + the `isDimmed` input on `HoodLayer`/`PlaceLayer` (alongside `PlaceLayer.isListed`, untouched); `isDimmed == false` must render byte-identically to today (§9 row 4) | **[iOS]** |
| **C11** | Wire into `MapScreen`: `chrome`/`searchSession`/`searchIndex` state, index build in the existing `.task`s, `router.closeHood()` on open **and** on leave (§4.9), result selection incl. the Hood camera move, `clear()` on the three completing paths | **[iOS]** |
| **C12** | The four specified states — empty field, no match (query echoed, focus retained), no-blurb Hood destination, no-density destination (§9 row 6) | **[iOS]** |
| **C13** | The accessibility checks as real tests: 44pt frames, exact VoiceOver strings, Dynamic Type growth at the largest accessibility size (§9 row 8 a–c) | **[iOS]** |
| **C14** | The two structural guards: `grep`-backed assertion that exactly two `.sheet(` sites exist app-wide, and `router.placeDepth ?? 0 <= 2` (§9 row 5c) | **[iOS]** |

**Order.** C1–C4 first (pure, no UI, no dependency on T-032). C5–C6 next, and they are the only steps whose diff depends on whether T-032 has landed. C7–C9, then C10–C12, then C13–C14.

**What this task does not build:** pin clustering (T-041), the tourist-trap line (T-035), the Places-list dashed ring (T-036), search history across launches (PRD P1/out of scope), sectioned results (PRD P1), voice search, and any third filter axis.

---

## 11. Decisions

### D1 — Search is a custom overlay in `MapScreen`'s `ZStack`, **not** a system `.sheet`

This contradicts three upstream texts, so it is argued rather than asserted:

- the PRD's Technical design line, *"Native sheet presentation (`ux-flows.md` §2.1), subject to the open layout call"*;
- `ux-flows.md` §2.1's 2026-07-30 note, *"Whoever specs T-038 (Search sheet) should build the same mechanism [`.presentationBackgroundInteraction`] against this row's claim rather than leaving it as an unspecified aspiration a second time"*;
- this task's own dispatch brief, which asked for T-033's `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` to be reused for this surface.

**Why it changes anyway.** All three predate T-032's TRD (2026-08-02), which settled how a *nav surface* is presented and said so explicitly — T-032 **D2**: *"a SwiftUI layer inside `MapScreen`'s `ZStack` at z5, below `MapNavRow` at z7, with an explicit scrim at z3. Not `.sheet`, not `.fullScreenCover`, not a `UIViewControllerRepresentable`, and not `.presentationBackgroundInteraction` (there is no presentation). The nav row must stay hit-testable or `ux-flows.md` §2.1's direct nav-switch requirement fails."* T-036 followed it for the second nav surface and recorded `.sheet()` for its list container as an explicitly rejected alternative. Three independent reasons make search the same case:

1. **A `.sheet` covers the nav row.** `ux-flows.md` §2.1's exclusivity rule requires switching *directly* from one surface to another with no dismiss-first step, and PRD req 1 bullet 4 restates it. A sheet presents above the whole hierarchy including z7, so the search button and the heat button both go under it. That is the same failure T-032 D2 exists to avoid.
2. **`MapScreen`'s one `.sheet` slot is already occupied and PRD req 5 needs it.** The shipped depth-1 site presents `HoodSheet`/`PlaceDetailModal`. Two `.sheet` modifiers on the same view cannot both present. If search took that slot, every destination it opens would have to be nested inside the search sheet as a third presentation site — a new mechanism, for a surface T-033 already ships.
3. **Req 4's selective dim and a sheet's own dimming are different things.** A `.sheet` at a detent brings its own system chrome and background treatment; the requirement asks for a per-feature dim on the map's own content.

**What is reused unchanged, and where.** `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` is T-033's mechanism *for system sheets*, and this task reuses it exactly — on the destination sheet a search result opens, which is the shipped site A modifier, untouched (§4.9). Nothing is reinvented; the pattern is applied where it belongs and not where T-032 D2 forbids it.

**Owed to `PAS-16`** (the open, unclaimed "centralize map background-interaction pattern" task): the centralisation should record the **split**, not one rule — *system sheets* (Hood/place detail) use `.presentationBackgroundInteraction`; *nav surfaces* (heat, Places, search, Profile) use the z-layered overlay with a z3 tap-catcher. `ux-flows.md` §2.1's note as written points T-038 at the wrong half, and this TRD is the third task to hit that seam. Flagged for `designer`/`product` at review; not edited here — `ux-flows.md` is Locked and not this agent's to amend.

### D2 — Two heights, compact by default — the detent recommendation, not the literal 50/50 split **[ASSUMPTION]**

The PRD leaves this open and calls it Aviran's (`ux-flows.md` §9 Q15). It is a required build input, so: **compact = 0.45 × container height (fresh open), expanded = 0.92, handle-draggable between them, drag below compact dismisses.** Behaviourally this is design review's `.medium`/`.large` detent recommendation; it is not literally system detents, because D1 makes this an overlay rather than a sheet.

Reasoning: (a) design review's ergonomics objection to a literal split stands on its own — a fixed half-screen map lands in the worst thumb-reach zone and invents gesture affordances iOS users do not already know (`design-principles.md` §3, Thumb Zone); (b) PRD req 4 needs the map *visible*, and compact leaves ~55% of it; (c) a fixed 50/50 makes the result list uncollapsible, which fights PRD req 8's Dynamic Type requirement at the largest sizes — three rows at accessibility-XXXL do not fit half a screen.

**Reversibility, stated so `product` can price it:** if Aviran holds to the literal split, `compact = 0.5`, delete `expanded`, and the handle drag becomes dismiss-only. Two constants and one gesture. No file moves and no contract changes.

### D3 — For `.search`, T-032's z3 scrim renders at opacity 0 and still hit-tests

§2.3's reasoning. The layer keeps tap-outside dismissal and keeps a map tap from opening a Hood sheet under the surface; the visual channel is handed to the selective dim, which is what PRD req 4 asks for. This is a per-surface opacity, not a removal of the layer — T-032's heat modal keeps its visible scrim unchanged.

### D4 — The dim is an input to the existing layers, not a new overlay

`isDimmed` on `HoodLayer`/`PlaceLayer`, computed by a pure function from the current result set (§4.10). No new map content, no second render path, and `isDimmed == false` is byte-identical to shipped rendering. The accepted limit — MapKit's base tiles are not dimmed — is stated in §4.10 and flagged for `product`.

### D5 — Matching rules are adopted from T-042 §4.3, not re-derived

Case- and diacritic-insensitive folding, **substring** match, applied to place names and Hood names as well as keywords. This answers the PRD's open technical question ("prefix vs. substring vs. fuzzy") by taking the owning spec's already-approved answer. `locale: nil` is added here so the index does not vary by device region — a detail T-042 did not need to state for a server-side validator.

### D6 — `Place` gains `keywords` and it is threaded through all three source paths at once

Seed decode, `PlacesAPI` (row + `select=`), and `PlacesCache`. Seed-only would compile, pass every Phase-1 test, and ship a silent `[]` the moment `BuildPhase.seedIsAuthoritative` flips — every place would stop matching its keywords in Phase 2 with no test failing. This is T-036 D1's finding for `permanentlyClosed`, applied to the field this task owns; the same three-path test set is C1's.

**This is not a hypothetical pattern to copy — it is already half-done in the tree.** `PlacesAPI`'s live `select=` reads `id,blurb,places(id,name,category,latitude,longitude,permanently_closed)` with the comment *"T-042's `is_tourist_trap`/`place_type`/`keywords` stay out; each lands with its reader."* T-038 is that reader, so C1 adds exactly one column to that string and one field to each of three structs. Declaration policy is non-optional throughout, matching `permanentlyClosed` — §3.2.

### D7 — One flat, deterministic result order; sectioning stays P1

Hood name matches, then place name matches, then keyword-only place matches; case-insensitive name-ascending within each group. Reasoning: Hoods are few (24) and coarse, so a Hood name typed in full should not sit below nine places; name-ascending is already this codebase's sort convention (`PlaceCatalog.commit`, T-036 D4); and a total order lets `qa` assert an exact array instead of a set. The PRD's P1 sectioning becomes a `SearchResultRow` grouping later with no matcher change.

### D8 — Chips filter places only; Hood results are never removed by a chip **[ASSUMPTION]**

PRD req 3 says a chip "narrows a typed query rather than replacing it," and does not say whether a Hood match survives an active category chip. Built as: it does. Reasoning — the chips' own copy names *place* categories (`PlaceCategory.displayName`), a Hood carries no category and cannot be classified into one, and dropping Hoods would make "narrow" mean "delete an entire result kind." Flagged for `product`; if the other reading is intended it is one line in `SearchQuery.run` step 5.

Also settled here: there is no "no categories selected" state, because `CategoryFilter` cannot express one (§4.5).

### D9 — Row type vocabulary is two words, "Hood" and "Place" **[ASSUMPTION]**

PRD req 2 bullet 2 says "every row states which of the three it is, in a word," and req 8's own VoiceOver examples give only two forms — `"Florentin, Hood"` and `"Port Said, place, Eat & Drink"`. The bullet's own justification clause is *"a Hood is never mistakable for a place,"* which is a two-way distinction. Built accordingly: a keyword match is a **place** row; the third "kind" is a match *route*, not a row type. `SearchResult.matchedKeyword` carries the keyword through unrendered, so surfacing it later ("matched: hummus") is a view change. Flagged for `product` — if a third word is meant, req 4 bullet 7's enumeration of row content ("name, category and Hood") also needs reopening.

### D10 — `clear()` is wired to three completing paths, never to "the surface closed"

§4.6's table. "The surface closed" and "the user finished with it" are different events; only the second resets. Observing `MapChromeState` would conflate them and break PRD req 7 bullet 1 the first time someone tapped the heat button. Note that the underlying product rule is itself unconfirmed — `ux-flows.md` §6's 2026-07-29 reconciliation is flagged there as *"my own reconciliation of two decisions made in different sessions, not a call he made explicitly either way,"* and §9 Q17 is still open. Carried forward, not resolved here.

### D11 — Presentation exclusivity reuses T-036 §4.6's two calls, with `closeHood()` on both

`router.closeHood()` on opening `.search` and on leaving it by any path. T-036 uses `closePlace()` on leave because `.places` can only produce a place modal; search can produce either destination, and `closeHood()` clears both fields in one call. No `DetailRouter` change, no `entryPath` field, no new sheet site — the same conclusion T-036 reached for the same reason.

**One cross-check for T-036's reviewers, raised and not resolved here:** T-036 §4.6 states that bucket-2 chrome "*is* reachable while a Hood sheet or place modal is up" because of `.presentationBackgroundInteraction`. That modifier governs *interaction*, not occlusion, and bucket-2 chrome plus the nav row both sit in the bottom band a `.medium` detent covers — so they may be un-tappable for a plainer reason than the one that sentence addresses. It does not change either task's structural calls (both close things explicitly rather than relying on reachability), and it is not this TRD's to fix. Named per `CLAUDE.md` rule 5 rather than left in a worklog line.

### D12 — Search adds no pin treatment of its own

PRD req 8 bullet 4 requires search-result pins to differ from Places-list pins by shape or icon, never colour alone. `ux-flows.md` §2.1 assigns that fix to the **Places-list** pin, and `map-rendering-spec.md` §6's 2026-08-02 addendum has already delivered it: a **dashed** ring, 2.5pt, 6pt offset — a shape difference, not a hue. So a search match renders as the plain shipped pin (circle + category glyph, full opacity while everything else dims) and a Places-list pin renders with the dashed ring. The requirement is met by the difference already specced, and this task adds no second treatment that would collide with it on a place that is both saved and matched.

**Dependency, re-checked:** T-036's ring **has landed** — `PlaceLayer.ring` is in the working tree, `StrokeStyle(lineWidth: 2.5, dash: [4, 3])`, 56pt frame, `.allowsHitTesting(false)`, exactly as `map-rendering-spec.md` §6's addendum specifies. So §9 row 8(d) is runnable, provided that diff is still present when T-038 builds. If it has been reverted or is not yet committed at build time, the row is recorded as blocked, not passed.

### D13 — `MapChromeState` and `MapNavRow` are create-if-absent against T-032's contract

Re-checked against the live tree mid-draft, and the answer changed once already: **`MapChromeState.swift` now exists** (T-036's build created it, untracked), byte-checked against T-032 §4.1 and correct — so C5 is a verify-only step in this tree. **`MapNavRow.swift` still does not exist**, so C6 creates it per T-032 D1/D6 carrying the search button only.

The rule, not the snapshot, is what `ios-developer` should follow: create each file *exactly* per T-032's own text if it is missing, add only the search button if it is present, and **re-check before writing rather than trusting this paragraph** — it was accurate for about forty minutes. T-038 adds no `NavSurface` case, no conformance and no method, in either order. This is the shape T-036 v1 was sent back to adopt; adopted here from the start.

### D14 — v2's §9 amendment is a verification fix, not a behaviour change; the shipped code already satisfies it

Recorded so nobody re-opens `build` over a documentation catch-up, and so the claim is traceable rather than asserted. **Traced by direct read of `passenger-code d537ca5`, not from `BOARD.md`'s verdict:**

| Amended condition | What the shipped code does |
|---|---|
| 4(a) — the dim must reach the **heat fill** | `HoodLayer.fillColor` = `HeatPalette.hue.opacity(HeatPalette.fillOpacity(for: band, dimmedBy: dimOpacity))`, and `fillOpacity` is `opacity(for: band) * dimOpacity`. The dim reaches the fill as a number. `HoodLayerFillDimTests` + `HeatPaletteTests` assert the resolved alpha, which is what the amended row asks for |
| 4(a) — something emphasised at `.cityWide`, where no pin renders | `SearchDim.emphasis` inserts `place.hoodID` alongside `place.id` for a `.place` result. `MapScreen`'s `PlaceLayer` `ForEach` is still gated on `showsNames`, correctly — the fix works *around* the zoom gate rather than removing it, so pin density at wide zoom is unchanged |
| 8(c-ii) — chip labels must not truncate | `CategoryChip`'s `Text(category.displayName)` carries `.fixedSize(horizontal: false, vertical: true)`, matching `SearchResultRow`'s already-shipped pattern |

So v2 changes **what `qa` must prove**, not what the code must do. The one thing it genuinely adds is coverage, not behaviour: `grep -rn isDimmed PassengerTests/ PassengerUITests/` returned **0** at the acceptance REJECT — every gate passed a requirement no test could fail. The amended rows are written so that the same code, checked properly, is provably correct; if a run of them fails, that is a real defect and not a wording artifact.

**Open and routed to `product`, not decided here:** §4.10's `nil`-band limit — a matched place whose Hood has no density at the selected hour is emphasised only by the *absence* of dimming on it, with no full-strength fill to carry the emphasis. Narrow, and it meets PRD req 4 bullet 3 as literally written; named rather than left for a fourth acceptance pass to find.

---

## 12. What `trd-review` should check first

- **§4.1 against T-032's live §4.1, character by character.** That mismatch is what sent T-036 v1 back. If T-032's v3 moved it after `passenger-brain 908aa6d`, this document is stale by definition.
- **D1.** It contradicts the PRD's own Technical design line, `ux-flows.md` §2.1's explicit instruction to T-038, and the dispatch brief. If the argument does not hold, everything from §2.3 down changes shape.
- **§9 row 2's "not checkable in Phase 1" line** — confirm that recording the strategy probe list as T-042's B4 rather than checking it against placeholder keywords is the right call, and not a requirement being quietly waived.
- **The four items flagged for `product`, none decided unilaterally:** D2 (sheet layout, Aviran's), D8 (chips vs. Hood results), D9 (two-word row vocabulary), and §4.10's undimmed base tiles. D10 additionally carries a product rule that `ux-flows.md` itself flags as unconfirmed.
- **D11's cross-check** on T-036 §4.6's reachability claim.
- **§1's tree-state table, re-run rather than read.** It was written twice in one sitting because the answer changed underneath it: `MapChromeState.swift`, `Place.permanentlyClosed`, the widened `select=` and `PlaceLayer`'s dashed ring all arrived mid-draft as **uncommitted work from other sessions** (T-034's and T-036's builds). None of it was staged by this agent, per `CLAUDE.md` rule 2. Anything in this TRD that describes the tree is a snapshot with a short shelf life; anything that describes a *contract* (§4.1, T-032 D2, T-036 D8, T-042 §3.2/§4.3) is not.
