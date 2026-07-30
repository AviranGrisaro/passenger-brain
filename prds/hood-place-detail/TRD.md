# Hood & Place Detail — TRD

**Task:** T-033 · **Linear:** `PAS-13` · **Status:** held at `trd` (separate nav-row question, `BOARD.md` T-033 row) · ready for `trd-review` when that clears
**Owner:** architect · **Date:** 2026-07-30 · **Amended:** 2026-07-31 — §3.1 schema ownership handed to T-042 / T-040; see §3.1, §8 D7, §11
**PRD:** [`hood-place-detail.md`](./hood-place-detail.md) (Draft v1) · **Design spec:** [`design/phase-1/hood-place-detail-design.md`](../../design/phase-1/hood-place-detail-design.md) (revised post-REJECT, `design-approval` PASS, `design-review` cleared on Aviran's approval)
**Mockup:** https://claude.ai/code/artifact/06f8a49b-7de4-430f-a701-96279db74611 — reference only. Where this TRD and the mockup disagree, this TRD wins.
**Builds on:** [`map-hoods-heat/TRD.md`](../map-hoods-heat/TRD.md) (T-031, built and accepted). Every module boundary, naming convention, and concurrency rule there applies here unchanged; this document extends that layout, it does not restate it.

---

## 1. Context

Read the PRD and the design spec first. This document resolves what they left open, pins the contracts the build agents work against, and records three scope facts neither document knew.

### 1.1 The four open items, resolved

| # | Open item (design spec §8) | Call | Where |
|---|---|---|---|
| 1 | Sheet-over-sheet presentation — does the entry path need different handling? | **Yes, and it is structural.** Two presentation sites, one modal view, one router. Depth is derived state, not a flag passed in. | §4.1, §4.2 |
| 2 | Route: action sheet vs. direct open, walking mode on both branches | **Direct open, no chooser, Apple Maps only in V1.** Waze cannot honour walking mode — escalated to `product`, §8 D3. | §4.6, §8 D3 |
| 3 | Category enum enforced in Postgres or client-side; display text or stable key | **Both: a Postgres `CHECK`, and a stable key (`eat-drink` / `things-to-do`).** Display strings exist only in the client. | §3.1, §4.3 |
| 4 | Does a place-row tap need a fresh fetch, or read the Hood sheet's payload? | **Neither fetches.** One session-scoped catalog, loaded once, read by both sheets and the pin layer. | §3.3, §4.4 |

### 1.2 Three things this feature turns out to need that nobody has built

Found by reading `passenger-code/` against the PRD's P0 bullets, not assumed:

- **There is no `places` table and no `blurb` column.** Migration `001` ships `hoods(id, name, city, polygon, updated_at)` and `hood_density` only. The PRD's technical-design section names both as if they exist. ~~**This feature is not iOS-only** — it needs migration `003`.~~ **Amended 2026-07-31: still true as a finding, no longer this task's to fix.** Two later TRDs written specifically to own this schema now define both — `places-dataset` (T-042) owns `places`, `hood-dataset` (T-040) owns `hoods.blurb`. **T-033 is now iOS-only in practice**: it depends on their migrations landing and creates neither. See §3.1.
- **There is no place pin layer.** T-031's PRD excludes place detail entirely and its shipped `MapScreen` renders Hood polygons and nothing else. `places-been-saved` (T-036) lists "`map-hoods-heat` (pins, ring channel)" as a dependency — that dependency is unmet. PRD req 3's "opens directly on one tap of a pin" is a P0 that cannot be satisfied without it, so **T-033 builds the minimal pin layer** (§4.5). Clustering (`map-rendering-spec.md` §5) and the personal-place ring (§6) are explicitly **not** built here — the ring is T-036's; clustering has no PRD and no owner, flagged in §10.
- **There is no Hood button.** PRD req 1 requires "the Hood button when it is showing" as a second door. T-031's PRD lists only near-me as chrome, and no such control exists in the code. **T-033 builds it** (§4.7) — it is ~30 lines and the alternative is a P0 satisfied only by hitting a polygon edge. Its *visual* treatment is undesigned; §8 D4 records how that gap is handled.

### 1.3 The mechanism this task exists to get right

`.presentationBackgroundInteraction(.enabled(upThrough: .medium))` is the named mechanism behind PRD req 1's "the map stays visible and interactive behind the sheet." It broke the design-approval gate once already (the mockup's full-surface backdrop swallowed every tap over the map). It is now documented in `design/ux-flows.md` §2.1 as a cross-feature rule; Linear **`PAS-16`** asks for it to be centralised into `design/design-principles.md` for T-038's benefit. That is not this TRD's deliverable — but **§4.2 below is the canonical technical statement of it**, and T-038's TRD should build against §4.2 rather than re-derive it.

---

## 2. Architecture

### 2.1 Module layout — added to `passenger-code/Passenger/`

```
Places/                        (new — pure data + domain, no SwiftUI)
  Place.swift                  value type: id, name, category, hoodID, coordinate
  PlaceCategory.swift          enum — stable keys, display names, SF Symbol glyph
  PlaceCatalog.swift           @MainActor @Observable — one session load; places(in:), place(id:), blurb(for:)
  PlacesAPI.swift              URLSession + PostgREST, one embedded GET
  PlacesCache.swift            last-good payload on disk (actor, mirrors DensityCache)
  PlaceHitTester.swift         pure geometry: point → Place?, nearest-within-tolerance
  SavedPlacesStore.swift       @MainActor @Observable — device-local saved ids
Detail/                        (new — the only place this feature knows SwiftUI, besides Map/)
  DetailRouter.swift           the two-level presentation state machine
  HoodSheet.swift              header, blurb, place list, empty/error states, the row
  PlaceDetailModal.swift       header, save toggle, category row, flag slot, route button
Map/
  PlaceLayer.swift             (new) pin annotations, category glyph, ≥44pt target
  HoodButton.swift             (new) conditional second door to the Hood sheet
  MapScreen.swift              (modified) composition, hit-test priority, presentation site A
Support/
  DirectionsService.swift      (new) route hand-off, walking mode, availability
Resources/
  places-tel-aviv.json         (new) bundled seed floor — see §3.4
```

Xcode synchronized file groups are on; adding a file to the folder is enough.

### 2.2 Boundaries — the T-031 rules, extended

- **`Places/` knows no SwiftUI and no map view types.** It fetches, caches, and answers "which places are in this Hood," "which place is at this point," and "is this saved." `PlaceHitTester` takes `MKMapPoint` and returns a `Place` — the same purity `HoodHitTester` has, testable without a map or a simulator.
- **`Detail/` knows SwiftUI and the catalog, never the network or the camera.** The two sheets read from `PlaceCatalog` and `SavedPlacesStore` and write through `DetailRouter`. They never own a fetch and never own a copy of saved state (§4.4 — this is the fix for the REJECT's B2 defect, expressed as a boundary rather than as a reminder).
- **`Map/` remains the only layer that composes everything.** `MapScreen` owns the camera, the tap-resolution order, and presentation site A. `PlaceLayer` is a content builder handed what to draw, exactly as `HoodLayer` is.
- **`Hoods/` and `Density/` are untouched.** This feature adds no reason for either to learn about places.

### 2.3 Third-party dependencies: none added

| Candidate | Call |
|---|---|
| `supabase-swift` SPM package | **No**, unchanged from T-031 §2.3. This feature adds one more unauthenticated GET against a public-read table. The existing ~60-line PostgREST pattern covers it. |
| SwiftData / Core Data for saved places | **No, not yet.** §8 D2 — a JSON payload behind a three-method store is smaller, matches the shipped `DensityCache` idiom, and T-036's migration to a provenance model costs a ~15-line one-time import. |
| A clustering library | **No.** Out of scope (§1.2), and MapKit's own clustering would come with it if it were in scope. |
| MapKit `MKMapItem` for the route hand-off | **Yes — first-party, already linked.** No dependency added. |

`passenger-code/README.md`'s "no third-party packages until a TRD justifies one" holds: this TRD justifies none.

---

## 3. Data model

### 3.1 Backend — **this task writes no migration** (amended 2026-07-31)

> **Amendment, 2026-07-31.** This section originally defined its own migration `003_places_and_hood_blurb.sql`, creating `public.places` and adding `hoods.blurb`. **Both are struck.** Two newer TRDs, written specifically to own this schema, now define them — and a column or table specified in two TRDs is a column that acquires two different nullability rules eventually. **T-033 now depends on those migrations rather than building either.** The struck DDL is not reproduced here; read the owning TRDs.

| What this feature reads | Owned by | Authoritative spec |
|---|---|---|
| `public.places` (+ `public.place_types`, its FK target) | **T-042** `places-dataset` (TRD delivered, commit `4d126f1`) | [`places-dataset/TRD.md`](../places-dataset/TRD.md) §3.1–§3.3 |
| `hoods.blurb` | **T-040** `hood-dataset` (TRD in flight) | [`hood-dataset/TRD.md`](../hood-dataset/TRD.md) §3.1 |

Both reconciliations are those TRDs' explicit decisions, not this TRD's reinterpretation of them: `places-dataset/TRD.md` **D1** (§2.1) and `hood-dataset/TRD.md` **D7** (§8). Ratifying them is `trd-review`'s job for all three tasks.

**The iOS track is not blocked by any of this.** §3.4's bundled seed floor is exactly the mechanism that makes that true: the client builds, demos, reviews and QAs against a local fixture with no backend reachable at all. Only this task's two backend steps move (§11 A1/A2 below); C1–C12 are untouched and un-resequenced.

#### What survives the strike, and what does not

- **The category resolution survives, and T-042 inherited it verbatim.** A Postgres `CHECK` on `text` with the stable keys `eat-drink` / `things-to-do`, display strings client-only in `PlaceCategory.displayName` (`places-dataset/TRD.md` §3.2, first bullet, cites this TRD by name). Design spec §8 item 3 and PRD req 6 stay resolved exactly as §4.3 and D4 describe. This TRD's §3.2 client enum and §4.3 boundary rule are unchanged.
- **The `blurb` nullability rule survives, and T-040 inherited it verbatim.** Nullable, `null` means "not curated," `''` is not a permitted value, the client normalises `""`/whitespace to `nil` at the boundary (`hood-dataset/TRD.md` §3.1 and its validator rule V8 state both halves). PRD req 2's ban on placeholder copy is unaffected.
- **The no-write-policy call survives.** T-042 §3.3 writes public-read `select` only, no insert/update/delete policy, absence-is-denial — the same shape this section specified and the same shape `001` established. There is still no client write path in this feature; saved state remains device-local (§3.5).
- **The "`permanently_closed` and a keyword column are deliberately absent" call is obsolete.** It was correct on the grounds given — "adding them speculatively would put two unowned fields in a shipped schema" — and that reason has expired: both fields now have an owner (T-042 req 4/5), so T-042's `places` ships them, plus `place_type`, `closed_checked_at` and `is_tourist_trap`. See "consequences" below.
- **`on delete cascade` → `on delete restrict`, accepted.** The struck DDL wrote `hood_id … on delete cascade`; T-042 §3.2 deliberately uses `restrict`, so that a Hood-geometry revision which drops a Hood row fails loudly instead of silently deleting the curated places attached to it. **Confirmed for T-033: nothing in this feature depends on cascade behaviour** — verified against every place-reading path here, not assumed. `PlaceCatalog` is read-only, no client code path deletes a Hood or a place, and §4.3's boundary table already specifies the only orphan case this client can observe (a `hood_id` absent from the bundled catalog → **keep** the place; it renders as a pin and appears in no Hood sheet). That rule is a client-side tolerance, not a database behaviour, and it is unchanged by the FK's delete action. `restrict` is strictly safer here and this TRD ratifies it.
- **The seed-data gap paragraph is superseded, not resolved.** The placeholder seed this section promised is now T-042's step **A4** (explicitly-labelled placeholder `place_types` rows plus a handful of real Tel Aviv places inside `001`'s five placeholder Hoods, `on conflict do nothing`) and the real curated dataset is T-042's step **B5**, blocked on T-040's real geometry and on Aviran (`PAS-6` item 11). Same gap, now owned. §9's "placeholder place data makes the Hood sheet look toy-sized" risk stands unchanged.

#### Consequences this task must absorb

T-042's `places` is a superset of what was struck, and two of its added columns are `not null` with no default. Named here so they cannot fall through the floor between tasks — `places-dataset/TRD.md` §2.2 assigns both to T-033:

| Consequence | Where it lands | Status |
|---|---|---|
| `places-tel-aviv.json` (§3.4) gains `place_type`, `keywords`, `permanently_closed`, `is_tourist_trap` | §11 step B2 | **Accepted.** The fixture must round-trip whatever the export produces, and `place_type`/`keywords` are `not null` at source. |
| `Place` (§3.2) gains the four fields | §3.2, §11 step C2 | **Flagged, not accepted — see §8 D7.** A model field with no reader in this task contradicts this TRD's own "don't build for a feature that isn't specced yet" (D2's reasoning). |

**Fetch contract unaffected.** §4.3's embedded `GET` still works verbatim — T-042's §4.5 states the same request with a wider `select` list, and the FK it relies on is declared in T-042's `places` exactly as it was here.

### 3.2 Client types

```swift
enum PlaceCategory: String, Sendable, CaseIterable, Codable {
    case eatDrink   = "eat-drink"
    case thingsToDo = "things-to-do"

    /// The only place a user-facing category string exists (PRD req 6, decision #33).
    var displayName: String { ... }        // "Eat & Drink" / "Things to do"
    /// One glyph vocabulary across pin, place row, and category row
    /// (`map-rendering-spec.md` §4). Never a generic map pin for `thingsToDo`.
    var symbolName: String { ... }         // "fork.knife" / "building.columns"
}

struct Place: Identifiable, Sendable {
    let id: String
    let name: String
    let category: PlaceCategory
    let hoodID: String
    let coordinate: CLLocationCoordinate2D
}

extension Place: Hashable {
    // Same reason as `Hood`: CLLocationCoordinate2D is not Hashable.
    static func == (lhs: Place, rhs: Place) -> Bool { lhs.id == rhs.id }
    func hash(into hasher: inout Hasher) { hasher.combine(id) }
}
```

`PlaceCategory` has exactly two cases and no `other`/`unknown` case, by construction. A row carrying a third value is dropped at the boundary (§4.3) — the type system then carries PRD req 6's "no third value, no null, no 'other'" for free, the same way `HeatBand?` carries T-031's no-data distinction.

### 3.3 Fetched, not bundled — and why the opposite call from T-031

T-031 bundles Hood geometry because a launch-time network fetch would put an unbounded cellular round trip inside the 3s cold-open budget. **Places are fetched**, and the reasoning does not contradict that:

- Places are **not on the interactivity path.** Pins render at close zoom only, and both sheets are reachable only by a tap — hundreds of milliseconds after first frame at the earliest. Nothing in §7 of T-031's budget is touched.
- Place curation is **continuous**; Hood geometry is authored once (T-040) and bounded at dozens by decision #12. Bundling places would mean an App Store release per curated restaurant.

One request, once per session, at the same lifecycle point as the density load.

### 3.4 The bundled seed floor — `Resources/places-tel-aviv.json`

Precedence when the catalog loads: **live fetch → last-good disk cache → bundled seed → empty.**

The seed is a build-time export of the `places` table, committed to `passenger-code/`, same drift rule as `hoods-tel-aviv.json` (whoever changes the data re-exports in the same change). It exists for two reasons, one of them non-obvious:

1. **First-run offline has real content** instead of an error banner on a device that has never had a successful fetch.
2. **It closes the root-cause gap `product` named at T-031's acceptance** — "no backend has ever been reachable in this whole pipeline, so nobody has actually *seen* heat render." Every visual bullet in this feature would inherit that same fate: unobservable until Aviran applies a migration. With a seed floor, `ios-developer`, `ios-code-reviewer`, and `qa` all see the real Hood sheet with real rows, on a device with no credentials and no network, and the acceptance gate reads observed behaviour rather than construction.

The seed is a **floor, never a cache**: a successful fetch always wins, and the seed is never written to, refreshed, or merged. `PlaceCatalog.Source` gains a `.seed` case so `qa` and the code reviewers can tell which path produced what they are looking at.

**Amended 2026-07-31 — this file carries places only, not Hood blurbs.** It originally exported "the `places` table plus each Hood's blurb." `hood-dataset/TRD.md` **D7** (amendment 2 of 2) moves the bundled blurb to `hoods-tel-aviv.json`, which T-040 already extends to `schemaVersion` 2 with `blurb`, `isTouristTrap` and `designatedForProgression` (its §3.5, §4.3). Accepted: one field, one bundled home — a field with two homes drifts. **Precise wiring consequence for C3/C7, so it isn't discovered at build time:** `PlaceCatalog.blurb(for:)` (§4.4) keeps its signature and keeps returning the *live* blurb from §4.3's embedded `GET`, which still selects `hoods.blurb`. Only the **fallback** changes — when `source` is `.seed`, the blurb comes from `HoodCatalog`'s bundled Hood record, not from this file, because this file no longer carries one. `HoodSheet` still reads exactly one accessor and still cannot tell the difference. **Consequence for the fixture's column set:** it gains `place_type`, `keywords`, `permanently_closed` and `is_tourist_trap` per §3.1's consequences table.

### 3.5 Saved state — device-local, per-place, durable

`SAVED_STATE` in the mockup is a `[PlaceID: Bool]` dictionary in JS. In the app it is:

- A `Set<Place.ID>` in memory, the single read source for every save affordance.
- Persisted to **`saved-places.json` in Application Support** — a payload, not a preference, exactly the `DensityCache` precedent (`passenger-code/CLAUDE.md` and T-031 §3.4 both draw that line; `UserDefaults` is for preferences).
- **Device-local, no server row, no identity.** This follows from the no-accounts lock and matches `places-been-saved`'s own storage call. Stated rather than hidden, same as that PRD does: **it does not survive reinstall or a new device.** That consequence is already flagged for Aviran under T-037; this TRD does not re-open it.
- **It contains only place slugs.** No coordinates, no timestamps of presence, no location of any kind — a saved-places file is the one artifact in this feature that could plausibly leak where somebody goes, and the minimal shape is the mitigation.

`created_at` is deliberately absent: T-036 owns provenance and ordering, and a timestamp written here would be a field with no reader and a second opinion about a model T-036 has not built yet.

---

## 4. Contracts

`ios-developer` needs §4.1–§4.8. `developer` needs §3.1 (which, since the 2026-07-31 amendment, points at T-042's and T-040's schema rather than defining any) and §4.3's response shape. Neither needs the other's code.

### 4.1 Presentation — `DetailRouter`, the depth-2 state machine

```swift
@MainActor @Observable
final class DetailRouter {
    private(set) var hood: Hood?
    private(set) var place: Place?

    func openHood(_ hood: Hood)      // hood = hood; place = nil
    func openPlace(_ place: Place)   // place = place; hood unchanged
    func closePlace()                // place = nil
    func closeHood()                 // hood = nil; place = nil

    /// nil when no modal is open. Never returns a value greater than 2.
    var placeDepth: Int? { place == nil ? nil : (hood == nil ? 1 : 2) }
}
```

- **Entry path is derived, never passed.** "Reached via the Hood sheet" *is* `hood != nil`. There is no `entryPath` parameter to keep in sync with reality, and the design spec's depth-1-vs-depth-2 distinction becomes a property of state rather than a convention a caller has to remember.
- **The depth-2 ceiling is structural** (`ux-flows.md` §5, design spec §1). A place at depth 2 requires a Hood; nothing can open a third level because there is no third field. Unit-test it directly: no call sequence produces `placeDepth > 2`.
- **`openPlace` never clears `hood`.** A pin tap on the exposed map while the Hood sheet is open therefore lands at depth 2 — correct, since the user is still inside that Hood's context.
- **`openHood` clears `place`.** Tapping a different Hood while a place modal is open at depth 1 swaps the depth-1 destination in place rather than stacking. One tap, one destination.
- **`openPlace`/`openHood` are idempotent for the same value** — assigning the already-current place is a no-op. §4.5 depends on this.

### 4.2 The two presentation sites — the canonical statement of the mechanism

**Site A — on `MapScreen`, one `.sheet` modifier, presenting the depth-1 destination.**

```swift
.sheet(isPresented: router.isDepth1Presented) {
    Group {
        if let hood = router.hood {
            HoodSheet(hood: hood)                    // .presentationDetents([.medium, .large])
        } else if let place = router.place {
            PlaceDetailModal(place: place)           // .presentationDetents([.medium])
        }
    }
    .presentationBackgroundInteraction(.enabled(upThrough: .medium))
    .presentationDragIndicator(.visible)
}
```

**Site B — inside `HoodSheet`'s own body, presenting the depth-2 place modal.**

```swift
.sheet(isPresented: router.isDepth2Presented) {
    PlaceDetailModal(place: place)
        .presentationDetents([.medium])
        .presentationDragIndicator(.visible)
        // No .presentationBackgroundInteraction — deliberate. See below.
}
```

Five rules, each load-bearing:

1. **One `.sheet` modifier per view.** Attaching two `.sheet` modifiers to the same view is unreliable in SwiftUI; the single-site-with-switched-content shape above avoids the question entirely rather than depending on which one wins. Site B lives in a different view, so there is no conflict.
2. **Background interaction is enabled up through `.medium` at depth 1 and absent at depth 2.** At depth 2 the thing "behind" the modal is the Hood sheet, not the map — the map is two layers down and covered regardless. Enabling it there would make the Hood sheet's rows tappable underneath an open modal, which nothing asks for and which would let a user open a place modal from behind an open place modal. The conservative default (dimmed, non-interactive) is correct, and the design spec's call is confirmed as buildable exactly as written.
3. **`upThrough: .medium`, not unconditional.** At `.large` there is negligible exposed map, and background interaction over an area the user cannot see is a way to lose a tap, not to keep one.
4. **There is no backdrop view, at any depth.** The REJECT's B1 defect was a full-surface tap-swallowing backdrop. A tap on the exposed map reaches the map and does *not* dismiss the sheet. Dismissal is the drag handle or the ✕ only (design spec §1). `ios-code-reviewer` should treat any full-surface overlay behind these sheets as a blocking finding.
5. **Bottom chrome is covered while a sheet is open, and that is correct.** At `.medium` the sheet covers the near-me button, the Hood button, and (once T-032 lands) the nav row. The exposed map *above* the sheet stays interactive; the chrome underneath does not need to be, and no requirement says otherwise. Dismissing restores it.

**Cross-task contract with T-032.** T-032's heat modal is a custom `ZStack` overlay in the map's own hierarchy, not a `.sheet` (`time-slider-design.md` §2). A system sheet presented over it covers it completely, including the nav row that overlay is carefully positioned to preserve. **Rule: opening a Hood sheet or place modal from the map closes any open nav-row modal first.** This is lossless — `selectedHour` is session state living above the modal, so reopening the heat modal later shows the same hour. Whichever of T-032/T-033 builds second wires the call; both TRDs must agree on it, so this is flagged for T-032's `trd-review` as well.

### 4.3 Places API — one embedded GET

```
GET {supabase_url}/rest/v1/hoods
    ?select=id,blurb,places(id,name,category,latitude,longitude)
    &city=eq.tel-aviv
Headers: apikey: <anon>, Authorization: Bearer <anon>, Accept: application/json
```

One round trip returns exactly the shape both sheets read: each Hood with its blurb and its places. PostgREST resource embedding works because `places.hood_id` has the FK declared in §3.1. If embedding proves awkward at build time, the fallback is two flat GETs (`hoods?select=id,blurb` and `places?select=...`) merged client-side — a change inside `PlacesAPI`, invisible to every caller.

Once per session, alongside `DensityStore.load()`. No pagination (dozens of Hoods, low hundreds of places). **No query parameter carries anything user-specific** — the request is byte-identical for every user, the same property T-031 §3.3 establishes and for the same reason.

**Boundary validation, per row, one row at a time** (`passenger-code/CLAUDE.md`):

| Condition | Handling |
|---|---|
| `category` is not one of the two keys | Drop that place. Never map to a default — PRD req 6 forbids a third value existing anywhere, and a silent default is how it would. |
| latitude/longitude missing or out of range | Drop that place. It cannot be drawn or routed to. |
| `blurb` is `""` or whitespace | Treated as null — "not curated" (§3.1). |
| `hood_id` not present in the bundled Hood catalog | **Keep the place.** It renders as a pin and appears in no Hood sheet. Dropping curated content because the *bundled geometry* is stale would hide real places for a reason the user cannot see; T-040 closes the underlying mismatch. |
| Any of the above | Never fails the whole payload, never crashes. |

Config from `SupabaseConfig.plist`, same as `DensityAPI`. **A missing plist is a valid state**: the fetch reports unconfigured, the catalog falls through to cache, then to the bundled seed (§3.4), and the app builds and runs for a developer with no credentials.

### 4.4 `PlaceCatalog` and `SavedPlacesStore`

```swift
@MainActor @Observable
final class PlaceCatalog {
    enum Source: Sendable { case live, cache, seed, unavailable }
    private(set) var source: Source

    func places(in hoodID: String) -> [Place]   // name-ordered; [] is a real answer
    func place(id: Place.ID) -> Place?
    func blurb(for hoodID: String) -> String?   // nil == not curated, never a placeholder
    var allPlaces: [Place] { get }              // PlaceLayer + PlaceHitTester source
    func load() async
}

@MainActor @Observable
final class SavedPlacesStore {
    func isSaved(_ id: Place.ID) -> Bool
    func toggle(_ id: Place.ID)                 // synchronous in memory; disk write is fire-and-forget
    func load() async
}
```

- **`places(in:)` and `blurb(for:)` are dictionary reads against already-fetched data.** No code path fetches when a sheet opens or a row is tapped. This is what makes the design spec's sub-400ms, no-spinner open real, and it is a contract, not an optimisation — design spec §8 item 4, resolved.
- **`toggle` is instant in memory.** The 400ms budget is met by construction because nothing awaits. Disk persistence is a fire-and-forget write to a `SavedPlacesPersisting` actor (mirroring `DensityCaching`), carrying a monotonically increasing generation number so a reordered pair of unstructured writes cannot land the older set last. Without that counter, two fast taps can persist the wrong final state — a race that is invisible until it isn't.
- **No view may hold its own copy of saved state.** The REJECT's B2 defect — `saved = false` on every open — is prevented structurally: `PlaceDetailModal` has no `@State private var isSaved`; the button renders `savedPlaces.isSaved(place.id)` directly off the observable store. This also makes the load race benign: if `SavedPlacesStore.load()` resolves after a modal is already on screen, the button re-renders correctly instead of lying. `ios-code-reviewer` should treat any local mirror of saved state in a view as a blocking finding.
- **`PlaceCatalog.load()` and `SavedPlacesStore.load()` both run in `.task` on `MapScreen`**, after first frame, never awaited on the launch path.

### 4.5 Tap resolution — one tap, one destination, deterministic priority

```swift
struct PlaceHitTester: Sendable {
    init(places: [Place])
    /// Nearest place whose coordinate lies within `tolerance` of `point`.
    func place(at point: MKMapPoint, tolerance: Double) -> Place?
}
```

Pure, takes no MapKit view type, unit-testable without a map — the same seam discipline as `HoodHitTester`. `MapScreen.handleTap` becomes:

```
tap → proxy.convert → MKMapPoint
  1. PlaceHitTester.place(at:tolerance: 22pt-equivalent)  → router.openPlace(place)
  2. else HoodHitTester.hood(at:tolerance:)               → router.openHood(hood)
  3. else nothing (never a dismiss — rule 4 in §4.2)
```

Place wins over Hood: a pin always sits inside a Hood, so the reverse order would make a pin unreachable. The existing `mapPointTolerance(forScreenPoints:at:proxy:)` supplies the 22pt-equivalent distance and is reused unchanged — which also delivers the ≥44pt touch target (`map-rendering-spec.md` §4) without dilating the drawn glyph.

**Pins stay real `Button`s inside their annotations, and that is safe because the router is idempotent.** VoiceOver needs an activatable element; making the annotation non-interactive would leave a VoiceOver user unable to open any place modal from the map. So both paths can fire for one tap — the annotation's button and the map's `SpatialTapGesture` — and both call `router.openPlace` with the *same* place, which by §4.1 is a no-op the second time. The idempotency is the thing that makes the double path safe; it is a requirement, not an incidental property.

`SpatialTapGesture` via `.simultaneousGesture` stays as T-031 built it (FB19394663 — `.onTapGesture` does not fire on `Map` under iOS 26). Nothing here changes that workaround.

### 4.6 Route hand-off — `DirectionsService`

```swift
struct RouteDestination: Sendable {
    let name: String
    let coordinate: CLLocationCoordinate2D
}

enum RouteApp: String, Sendable, CaseIterable { case appleMaps }

struct DirectionsService: Sendable {
    /// Apps installed on this device that can honour a walking destination.
    func availableApps() -> [RouteApp]
    func open(_ app: RouteApp, to destination: RouteDestination)
}
```

- **Apple Maps, walking, direct open.** `MKMapItem(placemark:)` with `name` set, opened via `openInMaps(launchOptions: [MKLaunchOptionsDirectionsModeKey: MKLaunchOptionsDirectionsModeWalking])`. Walking mode is set in exactly one place, so no branch can drop it — the failure the design spec's REJECT should-fix #6 was about.
- **No action sheet in V1.** With one available app the chooser is a tap that asks a question with one answer. Design spec §8 item 2 is resolved as direct open; the action-sheet branch returns only if Waze is authorised (§8 D3), and `RouteApp` is an enum precisely so adding a case is a compile-checked change rather than a rewrite.
- **The disabled branch is still built.** `availableApps().isEmpty` renders the button disabled with the inline explanation (PRD req 5, design spec §3). Apple Maps cannot be uninstalled, so this is unreachable in production — it is built because the PRD requires it be handled, not assumed impossible.
- **Returning from the hand-off restores map state with sheets closed** (PRD req 5). The hand-off calls `router.closeHood()` before opening the external app; camera and `selectedHour` are untouched because nothing in this feature writes to either.

### 4.7 `HoodButton` — the second door

Conditional chrome, visible at Hood zoom and closer, naming the Hood nearest the map's centre; tapping calls `router.openHood`. It reuses `MapScreen`'s existing `nameLabelSpanThreshold` (0.06) so the button appears exactly when Hood name labels do — one zoom concept, not two that can drift. Resolution is `HoodHitTester.hood(at:tolerance:)` against the camera centre point, so no new geometry code exists.

### 4.8 Sheet content contracts

**`HoodSheet(hood:)`** — reads `PlaceCatalog`, `DetailRouter` from the environment.

| Condition | Rendering |
|---|---|
| `blurb(for:) == nil` | Blurb section omitted entirely. No placeholder copy, no gap (PRD req 2). |
| `source != .unavailable`, `places(in:).isEmpty` | Empty state: icon + "No places curated here yet." + the "Explore another Hood" CTA calling `router.closeHood()`, ≥44pt hit area via invisible padding. |
| `source == .unavailable`, no places | **Error, not empty:** the banner "Couldn't load this Hood's details right now" replaces the blurb region; the list renders whatever is cached. The empty/error distinction is derived from `source` — it is never a guess. |
| Otherwise | Name (`.title2.bold()`), blurb (`.body`), name-ordered flat list of rows ≥44pt, each with category glyph + name + category word, VoiceOver "Port Said, Eat & Drink". Tapping a row calls `router.openPlace`. |

Detents `[.medium, .large]`. P1 grouping-by-category is not built (design spec §5 — layers on without changing any P0 structure).

**`PlaceDetailModal(place:)`** — reads `PlaceCatalog`, `SavedPlacesStore`, `DetailRouter`, `DirectionsService`.

Header: name, ✕ (32pt visual glyph in a 44×44pt target), Save toggle (44×44pt, `bookmark`/`bookmark.fill`, accessibility label "Save"/"Saved" tracking state, never a checkmark). Body: category row (glyph + `displayName`), then **one reserved line for T-035's tourist-heavy flag** — this modal renders exactly the string "Tourist-heavy spot" when flagged and nothing when not, and owns neither the icon nor the animation nor the busy+flagged phrasing. Bottom: the full-width `.borderedProminent` Route button, the modal's only primary action. Detent `[.medium]`.

Nothing else in this modal navigates anywhere (PRD req 3). No closed-place badge, no provenance word, no Places-list row — all T-036's.

---

## 5. Flow

```
Map (depth 0)
 ├─ tap Hood polygon ─────────┐
 ├─ tap Hood button ──────────┤→ router.openHood → site A → HoodSheet (depth 1)
 │                            │    ├─ tap row → router.openPlace → site B → PlaceDetailModal (depth 2)
 │                            │    │     └─ ✕ / drag → closePlace → back to HoodSheet
 │                            │    ├─ tap exposed map (Hood) → openHood → content swaps in place
 │                            │    ├─ tap exposed map (pin)  → openPlace → depth 2
 │                            │    └─ ✕ / drag → closeHood → map
 └─ tap pin ─────────────────────→ router.openPlace → site A → PlaceDetailModal (depth 1)
                                     ├─ tap exposed map (Hood) → openHood → swaps to HoodSheet
                                     └─ ✕ / drag → closePlace → map

Inside PlaceDetailModal, either depth:
  Save  → savedPlaces.toggle → button re-renders off the store; modal stays open
  Route → closeHood() → DirectionsService.open(.appleMaps, walking) → app exits
          → return: same camera, same selectedHour, all sheets closed
```

**Cold open is untouched.** `PlaceCatalog.load()` and `SavedPlacesStore.load()` are `.task`s that resolve after first frame; neither is awaited before the map is interactive, so T-031 §7's budget is unaffected. `ios-developer` re-runs the launch metric anyway (§11 step C8) — a budget nobody re-measures is a budget that regresses.

**States** beyond §4.8's table: loading shows no spinner under 400ms (the catalog is in memory or on disk in every case after the first launch); offline renders from cache or seed with Save and Route both fully functional — the Maps deep link needs the destination app's connectivity, not Passenger's.

---

## 6. Salvage

Per `SALVAGE.md`, leaf code only, read line by line and adapted to Swift 6:

- `Models/Place.swift` (REUSE, 79 lines) — read for field naming; §3.2's type is smaller and carries the two-value category the old model predates.
- `Services/SavedPlacesStore.swift` (REUSE, 55 lines) — the closest prior art to §3.5. Read before writing; do not carry its storage choice on trust.
- `Features/Places/PlaceDetailCard.swift` (REUSE, 85 lines) — layout reference for the modal only. **Not** its action hierarchy: the design spec's Route-primary/Save-demoted split (§2.2 there) is a decision made *against* the three-equal-buttons anti-pattern the old card and `ux-flows.md` §8a both carry.
- `Features/Map/PlacePin.swift` (REUSE, 18 lines) — pin rendering.
- ~~`002_seed_tel_aviv_places` — the Tel Aviv place seed, for §11 step B1, **if the archive becomes reachable**.~~ **Amended 2026-07-31:** no longer this task's — the curated dataset is `places-dataset` (T-042) step **B5**. The salvage lead itself is still live and worth carrying: `SALVAGE.md` marks the old seed REUSE and calls it "the most expensive data to recreate," and the old repo was not reachable from these sessions (migration `001`'s note records the same access wall). **Flagged for T-042's `trd-review`** — its B5 should try the archive before authoring from scratch.

---

## 7. Rollout & migration

- **No feature flag.** The off-state of a flag here is a map whose taps do nothing — a regression, not a safe default.
- ~~**Migration `003` applying is Aviran-gated.**~~ **Amended 2026-07-31 — this task hands off no migration at all** (§3.1). It **depends on** T-042's `places` migration and T-040's `hoods.blurb` migration. Both are still Aviran-gated to apply (he holds the credentials), and both are written and handed off by their own tasks; no agent applies either.
- **The client ships independently of the backend.** The bundled seed floor (§3.4) means the iOS build is demoable, reviewable, and QA-able before either migration is applied or a single row exists — and unlike T-031, the feature's primary visual output is *observed* rather than passed by construction. **This is why the §3.1 amendment delays no C-track work:** the iOS build never waited on a migration in the first place.
- **Backward compatibility:** both depended-on migrations are purely additive (`add column if not exists`, `create table if not exists`) and their authors state so. No existing row, policy, or client contract changes. T-031's app build keeps working against a database with either applied, and vice versa.
- **Forward compatibility:** ~~T-036 adds `places.permanently_closed`; T-038 adds a keyword field~~ — **amended: both now arrive with T-042's `places`, not later**, so the forward-compatibility case they described no longer exists. The client tolerates them regardless (unknown JSON keys are ignored by `Decodable`), which is what makes the amendment cost this task nothing. T-036's migration off `saved-places.json` is §8 D2's named import path and is unchanged.

---

## 8. Decisions

### D1 — Two presentation sites, one modal view (design spec §8 item 1, resolved)

Confirmed buildable exactly as the design spec describes, with the mechanism named in §4.2. The alternatives were considered and rejected:

- **Always present the place modal from the map at depth 1**, dismissing the Hood sheet first — uniform background interaction, but "back" from the modal would land on the map instead of the Hood sheet, breaking design spec §1's "dismissing returns exactly one level up."
- **Push the place detail inside a `NavigationStack` in the Hood sheet** — one presentation site, but a place reached from a pin and a place reached from a row would then be two different surfaces with two different dismiss gestures, which is exactly the divergence design spec §8 item 1 asked to prevent.
- **A single sheet whose content and background-interaction modifier both vary** — mutating `.presentationBackgroundInteraction` on a presented sheet is the one place SwiftUI's behaviour is least predictable, and this design puts the load-bearing mechanism inside it. Two sites means each modifier value is constant for the life of its sheet.

### D2 — Saved state persists as JSON, not SwiftData (§3.5)

T-036 will need `(place_id, provenance, created_at)` rows, and SwiftData is where that ends up. Building it now would mean a `@Model`, a `ModelContainer` on the launch path, and strict-concurrency care, for a feature whose entire need is a set of strings — against `passenger-code/CLAUDE.md`'s "the smaller solution wins" and "don't build for a feature that isn't specced yet."

The migration cost is bounded and named: T-036 reads `saved-places.json` once, inserts each id as a `.saved` provenance row, and deletes the file. Roughly fifteen lines and directly testable. Everything above the store's three-method surface is unaffected, because no view or sheet knows where the bytes live.

### D3 — Waze cannot honour walking mode: escalated to `product`, not decided around

PRD req 5 requires the route action to open "native Maps or Waze… walking mode." **Waze is a driving navigation product and its deep-link scheme (`waze://?ll=…&navigate=yes`) exposes no walking parameter** — **[ASSUMPTION]**, based on the documented scheme; `ios-developer` should confirm against Waze's current URL-scheme documentation before building anything Waze-shaped. If it holds, offering Waze means either handing a walker driving directions or dropping the walking-mode guarantee — and a PRD requirement is not the architect's to trade away.

**V1 builds Apple Maps only**, which satisfies req 5 as literally written ("opens native Maps *or* Waze", walking mode honoured, no in-app navigation), and adds `LSApplicationQueriesSchemes` to `Info.plist` for nothing, since no `canOpenURL` check is needed. If `product` decides driving-mode Waze is acceptable, adding it is one `RouteApp` case plus the action-sheet branch the design spec already describes — the enum exists for that reason. **This needs `product`'s answer; it does not block the build.**

### D4 — Category rename enforced at three layers

PRD req 6's "no string reading 'Food & drinks' survives anywhere in the shipped app or data" gets three enforcement points, not a promise: the Postgres `CHECK` (only two keys can be stored), the two-case Swift enum with no default (a third key is dropped at the boundary), and `displayName` as the single source of user-facing text. A test asserts both display strings; a grep for the retired string is part of the build report.

### D5 — Pin layer scope

Built: single pins at close zoom, category glyph, ≥44pt target, VoiceOver name + category, tap → modal. Not built: **clustering** (`map-rendering-spec.md` §5 — no PRD, no design spec, no owner; see §10) and the **personal-place ring** (§6 — T-036's, and its channel must not be borrowed here, same discipline T-031 applied to the tourist-trap stroke). The pin's close-zoom span threshold is **[ASSUMPTION]** ~0.02 latitude delta; `ios-developer` tunes it against the real dataset once **T-042 step B5** lands (was this task's B1 before the 2026-07-31 amendment), since a threshold picked against five placeholder rectangles proves nothing.

### D6 — The Hood button's visual treatment is undesigned

§1.2 and §4.7: the button is required by PRD req 1 and specified nowhere. This TRD specifies its **behaviour and trigger condition** and directs `ios-developer` to build it to the existing `NearMeButton` chrome idiom — a floating capsule in the same bottom band, same materials, same Reduce Motion handling. That is an engineering default standing in for a design call, flagged rather than presented as designed. If `designer` wants a different treatment, it is a swap inside one file, not a re-architecture.

### D7 — Schema ownership handed to T-042 and T-040; `Place`'s four new fields flagged, not accepted (added 2026-07-31)

The substance is in §3.1. Recorded here because it changes what this task builds, and because one half of it is a **question for `trd-review`, not a resolved call**.

**Accepted without reservation:** `places` is defined once, in T-042 (`places-dataset/TRD.md` D1); `hoods.blurb` is defined once, in T-040 (`hood-dataset/TRD.md` D7); `on delete cascade` becomes `on delete restrict` (§3.1 — confirmed no path in this feature depends on cascade); the bundled fixture drops Hood blurbs and gains T-042's four columns (§3.4). Each of those is another TRD's decision that this task's own reasoning independently supports, and the alternative — two TRDs defining one table — is the failure this reconciliation exists to prevent.

**Flagged, not accepted: `Place` (§3.2) gaining `placeType`, `keywords`, `permanentlyClosed`, `isTouristTrap`.** `places-dataset/TRD.md` §2.2 assigns this amendment to T-033. It is in genuine tension with this TRD's own standing rule — D2's "don't build for a feature that isn't specced yet," which is the reason `created_at` is absent from §3.5 and the reason §3.1 originally excluded these very columns. In this task none of the four has a reader: `permanentlyClosed` is T-036's badge, `isTouristTrap` is T-035's flag line (§4.8 reserves the line and deliberately owns neither the value nor the phrasing), `placeType` is T-037's sticker shape, `keywords` is T-038's matching. Adding all four to `Place` now ships four fields with no reader and pre-empts four downstream design calls.

**Recommendation, for T-033's and T-042's reviewers to settle together:** the *fixture* carries all four (it must — it round-trips the export, and `place_type`/`keywords` are `not null` at source), and the *Swift model* gains each field in the task that first reads it. `Decodable` ignores unknown JSON keys, so a fixture wider than the model is already a supported state and costs nothing. If reviewers prefer the model to mirror the fixture in one step, that is a defensible call — it is just not one this TRD should make silently on T-035/T-036/T-037/T-038's behalf.

---

## 9. Risks & alternatives

| Risk | Mitigation / decision |
|---|---|
| `.presentationBackgroundInteraction` does not actually deliver taps to `Map`'s `SpatialTapGesture` under iOS 26 — the whole feature's most load-bearing mechanism, and the one that already failed once | **Verified first, before any sheet content is built** (§11 step C1). If it fails, the fallback is presenting the Hood sheet as a custom bottom overlay in the map's own hierarchy — the exact pattern T-032 already uses for the heat modal, so it is proven in this app rather than speculative. Discovering this at C7 instead of C1 is the expensive version. |
| Sheet content swapping in place (Hood A → Hood B, or place modal → Hood sheet) animates badly or drops detents | Both content views declare their own detents; `qa` exercises the swap explicitly. Fallback is a brief dismiss/re-present, which is worse UX but not a re-architecture. |
| Two rapid Save taps persist the wrong final state | The generation counter in §4.4. Cheap, and the alternative is a bug that only appears under fast taps. |
| Placeholder place data makes the Hood sheet look toy-sized in testing | Expected, same root as T-040's placeholder Hood geometry. The sheet's structure, empty states, and error states are all verifiable against placeholder rows; only visual density is not. Named here so `qa` doesn't file it as a defect. |
| The curated Tel Aviv place dataset does not exist and the archive holding the old seed is unreachable | §3.1, §6, §10. **Amended 2026-07-31: now owned** — `places-dataset` (T-042) step B5, itself blocked on T-040's real geometry and on Aviran (`PAS-6` item 11). Still a real launch-readiness gap; still not a build blocker here, because the client contract is identical either way. |
| A place whose `hood_id` is missing from the bundled catalog renders as a pin in no Hood sheet | Deliberate (§4.3). Dropping it would hide curated content for an invisible reason. T-040's real geometry closes the mismatch. |
| Saved places lost on reinstall | Follows from the no-accounts lock, already flagged for Aviran under T-037. Not re-opened here. |
| T-032 and T-033 both modify `MapScreen` | §4.2's cross-task rule, flagged for both `trd-review`s. The surfaces barely overlap — T-032 owns an overlay and `selectedHour`, T-033 owns sheets and tap resolution. |

**Alternatives considered and rejected:** bundling the whole place dataset like Hood geometry (§3.3 — an App Store release per curated restaurant); SwiftData now (D2); a nested `NavigationStack` inside the Hood sheet (D1); an action-sheet route chooser in V1 (D3 — a question with one answer); MapKit clustering (§1.2 — no design, no PRD, no owner); making pins non-interactive annotations to avoid the double-tap path (§4.5 — it would leave VoiceOver users unable to open any place modal); storing display text in `category` (D4).

---

## 10. Flagged for `chief-of-staff` — not this TRD's to create

1. **Pin clustering has no owner.** `map-rendering-spec.md` §5 specifies it in full (screen-distance threshold, neutral count badge, zoom-on-tap, never heat- or tag-coloured) and no PRD claims it. It is not needed for correctness — §4.5's nearest-within-tolerance resolution works at any density — but it is needed for legibility once a real Tel Aviv dataset lands. Sibling in shape to T-040.
2. ~~**The curated Tel Aviv place dataset does not exist** (§3.1).~~ **Resolved as an ownership gap, 2026-07-31 — now `places-dataset` (T-042) step B5.** The *data* still does not exist, and B5 is blocked on T-040's real geometry and on Aviran (`PAS-6` item 11). Still blocks real V1 launch readiness; still does not block this build.
3. **`places-been-saved` (T-036) has a stale dependency line** — it lists "`map-hoods-heat` (pins, ring channel)" as satisfied. Pins arrive in T-033, not T-031; its ring accent depends on §4.5's `PlaceLayer`.
4. **D3 needs `product`'s answer on Waze.** Not blocking.

---

## 11. Build breakdown

Ordered. Tags name the agent(s) each step dispatches to.

**Backend / data track — amended 2026-07-31. This task no longer builds schema or seeds data; it confirms two other tasks' migrations have landed and reads their output.** Independent of the iOS track throughout, and the iOS track is not blocked by any of it (§3.1, §7).

| # | Step | Tag |
|---|---|---|
| A1 | ~~Migration `003`: `hoods.blurb`, `places` table, checks, FK, index~~ → **Confirm T-042's `places` migration and T-040's `hoods.blurb` migration have landed** as written in `places-dataset/TRD.md` §3.2 and `hood-dataset/TRD.md` §3.1. **This task's iOS build reads that schema; it does not create it.** Nothing here writes SQL. | **[Backend]** |
| A2 | ~~RLS on `places`~~ → **Confirm T-042's RLS is as specified** (`places-dataset/TRD.md` §3.3: enabled on `places` and `place_types`, one public `select` each, **no write policy**) and that §4.3's embedded `GET` returns the expected shape against it. A verification step, not a change. | **[Backend]** |
| ~~A3~~ | ~~Seed a small placeholder place set + Hood blurbs~~ → **struck.** Now T-042 step **A4** (placeholder seed, `on conflict do nothing`) and T-040 step **B5** (blurbs). | — |
| ~~B1~~ | ~~The real curated Tel Aviv place dataset and Hood blurbs~~ → **struck.** Now T-042 step **B5** (places, blocked on T-040's geometry and on Aviran, `PAS-6` item 11) and T-040 step **B5** (blurbs). The salvage lead moves with it (§6). | — |
| B2 | Export `places-tel-aviv.json` — the §3.4 seed floor. **Amended:** places only, no Hood blurbs (§3.4); columns per §3.1's consequences table. Same drift rule as `hoods-tel-aviv.json`. **Ownership needs one line settling at `trd-review`** — `places-dataset/TRD.md` §2.2 leaves this file with T-033 ("owns the export, its step B2") while its own step **B3** has `export_places.py` producing `places-tel-aviv.json` in the same run as the DB seed. Both cannot own the emitter. **Recommendation: T-042's B3 emits it** (it already holds the validated source and the DB seed, and a second emitter is a second chance to drift); T-033 keeps only the drift rule and the fixture's use. | **[Algo/Data]** + **[iOS]** |

**iOS track.**

| # | Step | Tag |
|---|---|---|
| C1 | **Prove `.presentationBackgroundInteraction` first** (§4.2, §9): a throwaway sheet over the existing map, verifying a tap on the exposed map still reaches `SpatialTapGesture` under iOS 26. Nothing else starts until this is answered. | **[iOS]** |
| C2 | `Place`, `PlaceCategory`, `PlaceHitTester` + geometry/boundary unit tests (§3.2, §4.5). Buildable against a hand-authored fixture before any backend exists. | **[iOS]** |
| C3 | `PlacesAPI`, `PlacesCache`, `PlaceCatalog` against the §4.3 contract, boundary-validated, with the live→cache→seed→empty precedence and the `.seed` source case (§3.4) | **[iOS]** |
| C4 | `SavedPlacesStore` + its persistence actor, including the generation counter and a reordered-write test (§4.4, §3.5) | **[iOS]** |
| C5 | `DetailRouter` + unit tests: depth ceiling never exceeds 2, `openHood` clears `place`, `openPlace` preserves `hood`, both idempotent (§4.1) | **[iOS]** |
| C6 | `PlaceLayer` + `MapScreen` tap-resolution priority (place before Hood), replacing the T-031 stub sheet wiring (§4.5, D5) | **[iOS]** |
| C7 | `HoodSheet` — header, blurb-when-present, place list, both empty states with the ≥44pt CTA, the error banner, presentation site A (§4.8, §4.2) | **[iOS]** |
| C8 | `PlaceDetailModal` + presentation site B — save toggle reading straight off the store, category row, the reserved T-035 flag line, ✕ in a 44pt target (§4.8, §4.2) | **[iOS]** |
| C9 | `DirectionsService` + the Route button, walking mode, the disabled branch, sheet-close-before-hand-off (§4.6, D3) | **[iOS]** |
| C10 | `HoodButton` at the existing zoom threshold, built to the `NearMeButton` chrome idiom (§4.7, D6) | **[iOS]** |
| C11 | VoiceOver pass: rows and pins announce "Name, Category"; Save announces "Save"/"Saved"; Dynamic Type at the largest accessibility sizes wraps rather than truncates (design spec §4) | **[iOS]** |
| C12 | Re-run the launch metric to confirm the two new `.task` loads didn't touch T-031 §7's cold-open budget; grep the shipped app and data for "Food & drinks" (D4). Numbers in the build report. | **[iOS]** |

**`trd-review` sign-off needed from:** `ios-developer` + `ios-code-reviewer` (C1–C12, now the whole build), `developer` + `code-reviewer` (A1–A2, now confirmation steps rather than schema authorship), `data-engineer` + `code-reviewer` (B2). §4.2's cross-task rule should also be put in front of whoever holds T-032's TRD.

**Cross-task ratification this amendment needs** (2026-07-31): T-042's and T-040's reviewers should confirm §3.1 and D7 match their own D1/D7 — and settle the two items this TRD flags rather than decides, **D7's `Place` model question** and **B2's export ownership**.
