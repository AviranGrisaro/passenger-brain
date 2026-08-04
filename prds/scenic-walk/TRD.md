# Scenic Walk (lighter version) — TRD

**Task:** T-057 · **Linear:** `PAS-46` · **Status:** `build` — `trd-review` cleared 2026-08-04 with all four sign-offs AGREE (`ios-developer` `8a006f7`, `ios-code-reviewer` `dd68110`, `data-engineer` `5bfee4d`, `code-reviewer` `0a457d4`; all `passenger-brain`), moved to `build` at `3e19897`, split at step granularity: `ios-developer` C1–C9, `data-engineer` A1
**Owner:** architect · **Date:** 2026-08-04 · **Amended:** 2026-08-04 (see Amendments below)
**PRD:** [`scenic-walk.md`](./scenic-walk.md) (Draft v1, `product`, 2026-08-04) · **Feasibility:** [`feasibility.md`](./feasibility.md) (`PAS-7`)
**Scope ruling:** decision #44 (lighter version). Decision #32's weighted per-segment routing is explicitly not what this builds.
**Builds on:** [`hood-place-detail/TRD.md`](../hood-place-detail/TRD.md) (T-033, accepted) — every module boundary, naming rule and concurrency rule there applies here unchanged. This document extends that layout; it does not restate it. `Support/DirectionsService.swift`, `Detail/PlaceDetailModal.swift`, `Detail/DetailRouter.swift` and `Location/LocationStore.swift` are all its output and are read, not re-derived, below.

**Grilling gate:** skipped — dispatched autonomously via chief-of-staff with no interactive founder in the loop (`architect.md`, "When running autonomously"). Every call that would have gone to Aviran is carried as **[ASSUMPTION]** and listed in §12.

**Amendments — 2026-08-04, documentation-only, no re-review cycle owed** (same treatment as the T-036/T-034 precedent). Both resolve `ios-developer`'s two pre-C3 findings from its AGREE (`passenger-brain 8a006f7`); neither changes a requirement, a bound, or the privacy contract.

| # | Finding | Resolution | Sections touched |
|---|---|---|---|
| **A1** | §4.1's `WalkingRouteProvider` passed `MKMapItem` — **not `Sendable`** — across the `@MainActor`→provider hop and, harder, across §4.6's concurrent two-leg fan-out. Under `SWIFT_STRICT_CONCURRENCY = complete` that either fails to build or pressures the implementer toward `@unchecked Sendable`, which `passenger-code/CLAUDE.md` bans. | The protocol now takes a `RouteEndpoint` — a `Sendable` value type carrying a `CLLocationCoordinate2D` or the symbolic `.currentLocation`. **`MKMapItem` is constructed inside the conformer's own async body and never crosses a boundary.** D3's privacy contract is unchanged and slightly strengthened: `.currentLocation` is a *case*, not a coordinate. | §2.1, §2.2, §3.2, §3.3, §4.1, §4.2, §4.3, §4.6, §9 row 13, §10 C1/C3, D15 |
| **A2** | §4.4 (`RoutePreviewModel` "torn down on dismiss") and §4.7 (a 5-minute memo whose whole purpose is surviving re-presentation) contradicted each other. The memo is what §9 row 10's "+0 requests on re-open within TTL" pass condition rests on, so the contradiction was load-bearing, not cosmetic. | The memo moves out of the model into **`RouteMemoStore`** — one instance owned by `MapScreen`, environment-injected, outliving every `RoutePreviewModel`. The model keeps its per-presentation lifetime and now holds **no** cross-place state at all. | §2.1, §2.2, §3.3, §4.4, §4.7, §5, §9 rows 10/11/14, §10 C1/C3/C6, D11/D16 |

---

## 1. Context

Read the PRD first. This document resolves the four open technical questions it left, ratifies or refines its four **[ASSUMPTION]**s, and pins the contracts `ios-developer` and `data-engineer` build against.

### 1.1 The PRD's open technical questions, resolved

| # | Open question (PRD "Open technical questions" + the dispatch brief) | Call | Where |
|---|---|---|---|
| 1 | `MKDirections.Request` carries one source and one destination — chain requests, or switch to Google Directions for native waypoint support? | **Chain MapKit.** One waypoint in V1 → 2 legs, concatenated. Google Directions is rejected on cost, credential surface, and a display restriction that bites a MapKit-rendered app. | §6, §11 D1, D2 |
| 2 | Request volume and caching per modal open | **≤ 3 `MKDirections` calls per modal open, 0 per route-control tap, 0 on re-open of the same place within 5 minutes.** Resolution happens once on modal appear; tapping a control is pure local selection. | §4.4, §4.7, §11 D5, D11 |
| 3 | Whether any hand-off can carry the waypoints (req 5) | **It cannot.** No public API carries an intermediate stop into Apple Maps. So req 5's disclosure line is unconditional whenever Scenic is the selection — static copy, shown before the tap, not an alert after. | §4.8, §11 D12 |
| 4 | Req 8's Phase-1 fixture — what exactly has to be authored | Three mutually non-adjacent `false`-flagged Hoods on one documented corridor, authored in `hoods-tel-aviv.source.json` and regenerated. **No `places` change** — the curated-place waypoint path is covered by unit fixtures instead, for a reason worth reading. | §3.4, §11 D13, §10 A1 |

### 1.2 Three things this feature turns out to need that the PRD did not know

Found by reading `passenger-code/` against the PRD's P0 bullets, not assumed:

- **`LocationStore` holds no coordinates, by design.** Its own doc comment: *"Authorization status only — no coordinates, ever … `Location/` never sees a `CLLocation`, never calls `startUpdatingLocation`."* A route needs an origin. Resolving that without breaking the privacy boundary is §4.3 and §11 D3, and it is the single most load-bearing decision in this TRD.
- **The waypoint heuristic's ranking input barely exists.** The PRD proposes ranking candidate Hoods by *count of curated places inside*. The shipped `places-tel-aviv.json` holds **9 places in exactly 3 Hoods** (`florentin` 3, `kerem-hateimanim` 3, `neve-tzedek` 3), and **not one of them is a `false`-flagged Hood**. Ranking by a count that is 0 for every eligible candidate is not a ranking. §4.5 keeps the count as the primary sort key (it is right for real data) and adds a second key that is non-degenerate today, plus a waypoint fallback for a Hood with no curated place.
- **"Draws its polyline inside the modal's own space" resolves to the main map, not a mini-map** — and the PRD's own next bullet proves it: *"A route polyline is distinguishable from a Hood's tourist-trap outline stroke at neighborhood zoom."* Hood outlines are drawn by `Map/HoodLayer.swift` on the main map and nowhere else. A second `Map` instance inside the sheet would have no Hood outlines to be confused with. §4.9, §11 D9.

---

## 2. Architecture

### 2.1 Module layout — added to `passenger-code/Passenger/`

```
Routing/                        (new — pure domain + one service, no SwiftUI)
  RoutePlan.swift               value type: kind, coordinates, distance, travelTime, viaHoodName?
  RouteEndpoint.swift           Sendable value: .currentLocation | .coordinate(_, name:) — the
                                only thing that crosses into the provider (§4.1, A1)
  RoutePreview.swift            the resolved state: fast, scenic-or-a-stated-reason, selection
  WalkingRouteProvider.swift    protocol + MKDirections conformer; chains legs, concatenates
  ScenicWaypointPlanner.swift   pure: (fast polyline, hoods, places) -> ranked [WaypointCandidate]
  RouteCorridor.swift           pure geometry: point→polyline distance, divergence run, seam dedup
  RouteBounds.swift             the detour constants + the accept/reject predicates
  RoutePreviewModel.swift       @MainActor @Observable — owns resolve + selection for ONE modal
                                presentation. Owns no memo (A2).
  RouteMemoStore.swift          (new) @MainActor @Observable — the 5-minute session memo, one
                                instance for the app's lifetime, outlives every model (§4.7, A2)
Detail/
  RouteControls.swift           (new) the two controls, durations, disabled line, disclosure line
  PlaceDetailModal.swift        (modified) hosts RouteControls in place of the bare route button
Map/
  RouteLayer.swift              (new) the two polylines — weight, dash, casing, selection dominance
  MapScreen.swift               (modified) renders RouteLayer, fits the camera with a bottom inset,
                                owns RouteMemoStore and clears it on scenePhase == .background
Support/
  DirectionsService.swift       (modified) one added method: hand-off already knows walking mode
```

Xcode synchronized file groups are on; adding a file to the folder is enough.

### 2.2 Boundaries

- **`Routing/` knows no SwiftUI and no map view types.** `RoutePlan` is coordinates and two scalars. `ScenicWaypointPlanner`, `RouteCorridor` and `RouteBounds` are pure functions over `MKMapPoint`/`CLLocationCoordinate2D` — the same purity `HoodHitTester` and `PlaceHitTester` have, and the reason §9's hardest rows are unit rows rather than manual ones.
- **`WalkingRouteProvider` is the only type in the app that touches `MKDirections`.** It is a protocol so `RoutePreviewModel` can be tested against a scripted provider with zero network. Every request in this feature is issued from exactly one method on it.
- **No MapKit reference type crosses a concurrency boundary (A1).** `MKMapItem`, `MKDirections`, `MKDirections.Request` and `MKRoute` are constructed, used and discarded **inside a single async function body in the `MKDirections` conformer**. What crosses in is `RouteEndpoint`; what crosses out is `RouteLeg`. Both are `Sendable` structs/enums over `CLLocationCoordinate2D`, `String`, `Double` — the same value-only discipline `Hood` and `Place` already hold. `@unchecked Sendable` appears nowhere in this feature; `passenger-code/CLAUDE.md`'s engineering pillars ban it, and after this amendment nothing in the design asks for it.
- **`Routing/` never reads `LocationStore` for a coordinate, because there is none to read.** It reads `authorizationStatus` and nothing else (§4.3).
- **Two lifetimes, named apart (A2).** `RoutePreviewModel` lives for **one place-modal presentation**; `RouteMemoStore` lives for the **app session**. The model reads and writes the store; the store knows nothing about the model. Everything that must survive a dismissal lives in the store, and nothing else does — which is the whole content of the fix, because the previous draft put a cross-presentation memo inside a per-presentation object.
- **`Detail/` renders state; it never resolves.** `RouteControls` reads `RoutePreviewModel` and writes only the selection.
- **`Map/` remains the only layer that composes.** `RouteLayer` is handed what to draw, exactly as `HoodLayer` and `PlaceLayer` are.
- **`Hoods/`, `Places/`, `Density/`, `Flag/`, `LocalQA/` are untouched.** This feature adds no reason for any of them to learn about routing.

### 2.3 Third-party dependencies: none added

| Candidate | Call |
|---|---|
| Google Directions API | **No** — §6, §11 D1. Costs money and needs an account (both Aviran-gated), puts an API key in the client, and its platform terms restrict displaying Directions content on a non-Google map. |
| A polyline/geometry package (Turf-style) | **No.** Three functions are needed — point-to-segment distance, a divergence run, a seam dedup — and all three are ≤ 20 lines over `MKMapPoint`'s flat projected plane. `HoodHitTester` set this precedent. |
| `MapKit` / `CoreLocation` | Already linked. No new framework. |

---

## 3. Data model

### 3.1 Nothing persists. Nothing is added to the schema.

No new table, column, index, RPC or RLS surface. No migration is written **by the iOS half** of this feature. The one data change (§3.4) is an attribute-value edit to an existing authored source, not a schema change.

### 3.2 The types

```swift
enum RouteKind: Sendable, CaseIterable { case fast, scenic }

/// The only thing that crosses into `WalkingRouteProvider` (A1). A value type,
/// so a `MKMapItem` — which is not `Sendable` — never has to.
/// `.currentLocation` is symbolic: it names the device position without the
/// app ever holding it, which is D3's privacy contract expressed in the type
/// system rather than in a comment.
enum RouteEndpoint: Sendable, Equatable {
    case currentLocation
    case coordinate(CLLocationCoordinate2D, name: String?)
}

struct RoutePlan: Sendable, Equatable {
    let kind: RouteKind
    let coordinates: [CLLocationCoordinate2D]   // seam-deduped, ordered origin → destination
    let distance: CLLocationDistance            // metres, summed over legs
    let travelTime: TimeInterval                // seconds, summed over legs
    let viaHoodName: String?                    // scenic only; nil for .fast
}

/// Why no scenic route exists. Every case is a *stated* state (PRD req 4),
/// never a silent nil — `RouteControls` renders one line per case.
enum ScenicUnavailable: Sendable, Equatable {
    case originAndDestinationShareAHood
    case walkTooShort            // fast route under RouteBounds.minimumFastTravelTime
    case noQualifyingHood        // no `false`-flagged Hood in the corridor
    case detourTooLong           // every attempt failed RouteBounds
    case notDistinct             // the returned route did not diverge from fast (req 4, bullet 3)
    case routingFailed           // MKDirections error on a scenic leg only
}

enum RoutePreview: Sendable, Equatable {
    case idle
    case resolving
    case noOrigin                                  // PRD req 6
    case failed                                    // the *fast* route could not be resolved
    case resolved(fast: RoutePlan, scenic: Result<RoutePlan, ScenicUnavailable>)
}
```

`ScenicUnavailable` is an enum and not a `Bool?` for the same reason `TouristFlag` is: req 4 requires the reason be renderable, and a type that can only say "no" cannot say "no, because you are already in this neighborhood."

**Two conformance notes, named here so C1 does not discover them mid-file.** (a) `CLLocationCoordinate2D` is **not `Equatable`** in the SDK, so `RoutePlan`'s and `RouteEndpoint`'s `Equatable` conformances are hand-written `==` implementations comparing `latitude`/`longitude`, not synthesised ones. This is true of the original draft too; it is written down now because A1 added a second type with the same shape. (b) `CLLocationCoordinate2D`'s `Sendable`-ness comes from being an imported C struct of two `Double`s, not from an explicit conformance — if the iOS 26 SDK disagrees at build time, `ios-developer` says so at C1 rather than reaching for `@unchecked Sendable`; the fallback is a two-`Double` struct of our own inside `RouteEndpoint`, which costs one initializer.

### 3.3 Location data — the privacy contract

- **The app never asks CoreLocation for a coordinate.** The route origin is `RouteEndpoint.currentLocation`, which the provider's conformer turns into `MKMapItem.forCurrentLocation()` in the same function that issues the request (§4.1, §4.3). MapKit resolves the device position internally; `Routing/` receives route geometry, not a fix. **A1 tightened this rather than loosening it:** the origin is now a case with no payload, so there is no place in the design a user coordinate *could* be stored even by accident.
- **Route geometry is in-memory only.** It lives for one place-modal presentation in `RoutePreviewModel`, and for at most 5 minutes in `RouteMemoStore` (§4.7). No `UserDefaults`, no file, no `Codable` conformance on `RoutePlan`, no analytics event carrying a coordinate. `RouteMemoStore` is deliberately **not** the `SavedPlacesStore` shape in one respect: it has no disk seam at all, so there is nothing to persist by mistake.
- **No cache key contains a coordinate.** The session memo (§4.7) is keyed on `Place.id` alone.
- **Nothing is logged.** `Routing/` contains no `print`, no `os_log`, no `Logger`. §9 row 11 greps for it.

This is stricter than "don't over-retain": the feature never holds a user position at all, only a path that happens to start at one — in RAM, for one open sheet, plus a 5-minute memo that is dropped on background. A2 moved the memo to a longer-lived object, so the retention window is stated exactly rather than implied by an object's lifetime: **≤ 5 minutes, or until the app backgrounds, whichever comes first.**

### 3.4 The Build-Phase-1 fixture (PRD req 8) — what has to be authored

**The problem, measured, not assumed.** `passenger-brain/database/data/hoods-tel-aviv.source.json` carries 24 Hoods: `isTouristTrap` is `true` for 2 (`florentin`, `kerem-hateimanim`), `false` for 1 (`ramat-aviv`), `null` for the other 21. `ramat-aviv` is 5 km north of every curated place, so as shipped there is no A→B in the app for which a scenic route can exist. Reqs 2–4 are undemonstrable on device.

**What the fixture must satisfy** — these are the acceptance conditions for step A1, and `data-engineer` owns meeting them:

1. **≥ 3 Hoods carry `isTouristTrap: false`**, in addition to `ramat-aviv`.
2. **They are mutually non-adjacent**, defined falsifiably as: no vertex of one polygon within **50 m** of any vertex of another (today's adjacent Hoods share vertices exactly, at 0 m), **and** centroids ≥ **800 m** apart.
3. **A documented demo corridor** — one origin coordinate (settable in the Simulator) and one destination `Place.id` from the shipped `places-tel-aviv.json` — for which **at least one** of them is a qualifying candidate under §4.5: its polygon comes within `corridorBuffer` (800 m) of the fast route, and its waypoint lands **250–1200 m** off the fast route.
4. **The corridor and the expected outcome are written into the source file's own header note**, so a reader of the fixture can reproduce the demo without this TRD.
5. **A test asserts the count against the shipped bundle** (§9 row 8), in the style of `PassportBundleInvariantTests` — read from `Bundle.main`, not from a test fixture.
6. **Every flag added is marked provisional**, following the `florentin` blurb precedent (`"[PROVISIONAL] …"`) — carried in the source row's `provenance`, so Build Phase 2's real local-QA values overwrite demo values and not curated ones.

**Computed candidate proposal — geometry only, substance is `data-engineer`'s and Aviran's call. [ASSUMPTION].**
`old-north`, `montefiore`, `shapira`. Measured against the committed source polygons: pairwise **minimum vertex separations 1136 m / 2865 m / 428 m** (all ≫ 50 m — no shared boundary) and **centroid separations 2830 m / 4454 m / 2290 m** — condition 2 holds. All three also clear both thresholds against the pre-existing `ramat-aviv`, so the full `false` set of 4 gives 6 qualifying pairs. Demo corridor: origin `32.0945, 34.7981` (Bavli, a Simulator custom location) → destination `florentin-anna-loulou-bar`; straight-line 4.73 km, with `montefiore`'s centroid 715 m and `shapira`'s 1102 m off that line — both inside the 250–1200 m waypoint band, so condition 3 holds with a spare candidate. **Two caveats stated rather than buried:** straight-line geometry is not walking-route geometry, so `data-engineer` must re-measure against a real `MKDirections` fast route on device before committing the fixture; and whether these three Tel Aviv neighbourhoods *are* "not tourist-heavy" is a data claim this TRD has no standing to make — see §8 R4, which is the sharper version of the same worry.

**Authoring path, non-negotiable (L-024).** `hoods-tel-aviv.json` in `passenger-code/Passenger/Resources/` is **generated**. The edit goes into `database/data/hoods-tel-aviv.source.json` and both artifacts are regenerated with `database/scripts/build_hoods.py`. A hand-edit to the bundle survives every reviewer and dies at the next generator run. **Contrast, so nobody over-applies the rule:** `places-tel-aviv.json` is *not* generated — its own `_note` says "Hand-authored, NOT an export_places.py output — that emitter does not exist until T-042 step B3." Editing it by hand is sanctioned. This TRD does not ask anyone to.

**Migration artifact.** `build_hoods.py` emits a SQL seed alongside the bundle. `006_` and `007_hoods_tel_aviv_data.sql` both already exist and **neither has been applied** (`database/README.md`). Recommendation: **regenerate `007` in place** with `--migration-number 007`, rather than adding an `008` that seeds the same table a third time — the "never edit an applied migration" rule does not bind an unapplied one. `code-reviewer` overrules this if the backend convention says otherwise; it is a one-flag change either way.

---

## 4. Contracts

### 4.1 `WalkingRouteProvider` — the only `MKDirections` surface

```swift
protocol WalkingRouteProvider: Sendable {
    /// One leg. `MKDirections.Request` carries exactly one source and one
    /// destination — this signature is that limitation made explicit rather
    /// than hidden behind a waypoint parameter the API cannot honour.
    ///
    /// Takes `RouteEndpoint`, never `MKMapItem` (A1). `MKMapItem` is not
    /// `Sendable`, and this method is called from a `@MainActor` model and
    /// from §4.6's concurrent two-leg fan-out — under
    /// `SWIFT_STRICT_CONCURRENCY = complete` an `MKMapItem` parameter is a
    /// build failure or an `@unchecked Sendable`, and the second is banned.
    func leg(from: RouteEndpoint, to: RouteEndpoint) async throws -> RouteLeg
}

struct RouteLeg: Sendable {
    let coordinates: [CLLocationCoordinate2D]
    let distance: CLLocationDistance
    let travelTime: TimeInterval
}

enum RouteError: Error, Equatable { case throttled, notFound, transport }
```

**The conformer owns every MapKit type, start to finish, inside one function body:**

```swift
struct MapKitWalkingRouteProvider: WalkingRouteProvider {
    func leg(from: RouteEndpoint, to: RouteEndpoint) async throws -> RouteLeg {
        // Constructed here, used here, discarded here. No MapKit reference
        // type is a parameter, a return value, or a stored property anywhere
        // in `Routing/`.
        let request = MKDirections.Request()
        request.source = mapItem(for: from)
        request.destination = mapItem(for: to)
        request.transportType = .walking
        request.requestsAlternateRoutes = false
        // … await MKDirections(request:).calculate(), map to RouteLeg …
    }

    private func mapItem(for endpoint: RouteEndpoint) -> MKMapItem {
        switch endpoint {
        case .currentLocation:
            return .forCurrentLocation()
        case let .coordinate(coordinate, name):
            let item = MKMapItem(location: CLLocation(latitude: coordinate.latitude,
                                                      longitude: coordinate.longitude),
                                 address: nil)
            item.name = name
            return item
        }
    }
}
```

`transportType = .walking` and `requestsAlternateRoutes = false` are set in this one place. The conformer takes `response.routes.first` and maps `MKError` codes: `.loadingThrottled` → `.throttled`, `.directionsNotFound`/`.placemarkNotFound` → `.notFound`, everything else → `.transport`. Boundary validation, not defensive programming: an empty `routes` array is `.notFound`, never a zero-length route.

**Consequence for the scripted test provider, stated because it is the point of the protocol:** a scripted `WalkingRouteProvider` now scripts on `RouteEndpoint`, a value type it can pattern-match and compare — so §9 rows 3, 4, 7 and 10 script and assert against endpoints rather than against MapKit objects a test cannot construct cheaply.

### 4.2 Concatenation — the seam

`RoutePlan` for a scenic route is built from 2 legs — `.currentLocation` → `.coordinate(waypoint)` and `.coordinate(waypoint)` → `.coordinate(destination)`, the same `RouteEndpoint` value passed to both calls (A1):

- `distance` = Σ leg distances. `travelTime` = Σ leg travel times.
- `coordinates` = leg 1's coordinates ++ leg 2's, **dropping leg 2's first coordinate when it is within 5 m of leg 1's last**. Both legs' endpoints derive from the same requested waypoint, but MapKit snaps each independently to the pedestrian network, so byte-equality at the seam is not guaranteed and an undeduped seam draws a visible one-point spur.
- No re-ordering, no simplification. The polyline is what MapKit returned.
- **Known and accepted:** a chained route can walk past the waypoint and double back, because leg 2 is optimised without knowledge of leg 1's approach. Real, visible, and out of scope to fix — §8 R2.

### 4.3 The origin — how a route starts without the app holding a location

Everything above the provider speaks in `RouteEndpoint` (A1). `RoutePreviewModel` asks for:

```swift
// Routing/ never constructs a CLLocationCoordinate2D for the user.
// The origin is a case with no payload; the destination is the place's own
// already-public coordinate, read, not derived.
try await provider.leg(from: .currentLocation,
                       to: .coordinate(place.coordinate, name: place.name))
```

and the conformer turns `.currentLocation` into `MKMapItem.forCurrentLocation()` (§4.1). `forCurrentLocation()` is MapKit's own handle on the device position. It preserves `LocationStore`'s boundary exactly: the app never calls `startUpdatingLocation`, never receives a `CLLocation`, and never stores one.

**Confirmed at `trd-review`, not left open:** `ios-developer` verified against current Apple documentation (`passenger-brain 8a006f7`) that `MKMapItem.forCurrentLocation()` is live and still the recommended way to hand `MKDirections` an origin on the iOS 26 SDK. §12 item 1 is therefore **resolved**, and the fallback below is retained only as a build-time contingency, not as an expected path.

The gate is authorization, read from the existing store:

```swift
guard locationStore.authorizationStatus == .authorizedWhenInUse
   || locationStore.authorizationStatus == .authorizedAlways
else { return .noOrigin }   // PRD req 6 — no polyline, no duration claimed
```

**Build note, named so it does not become a surprise:** the iOS 26 SDK deprecated MapKit's `MKPlacemark`-based `MKMapItem` initializers (`DirectionsService.swift` already carries that migration). `forCurrentLocation()` must be confirmed available at build time. **If it is not**, the fallback is a single `CLLocationManager.requestLocation()` **confined to the conformer's `mapItem(for:)`** (§4.1), its `CLLocation` used to build one `MKMapItem` and released in the same function — never stored, never logged, never keyed on, and never returned across the protocol, which still speaks only `RouteEndpoint`. `ios-developer` reports which path it took; §9 row 11 checks either one against the same greps.

### 4.4 `RoutePreviewModel` — the per-presentation state owner

```swift
@MainActor @Observable
final class RoutePreviewModel {
    private(set) var preview: RoutePreview = .idle
    private(set) var selection: RouteKind = .fast

    /// Both collaborators are injected, neither is created here: the provider
    /// so tests can script it, the memo store because it must outlive this
    /// object (A2).
    init(provider: any WalkingRouteProvider, memo: RouteMemoStore)

    func resolve(for place: Place, hoods: [Hood], places: [Place]) async
    func select(_ kind: RouteKind)      // pure local state; never triggers a request
    func reset()                        // called on closePlace(); clears geometry
}
```

- **One instance per place-modal presentation.** Created by `PlaceDetailModal`'s `.task(id: place.id)`, torn down on dismiss. It is not an app-level singleton, and — **corrected by A2** — it holds **no** state across places whatsoever. The earlier draft said "no state across places except the memo," which could not be true of an object that is destroyed on dismiss; the memo now lives in `RouteMemoStore` (§4.7), which is not destroyed on dismiss. This mattered: §9 row 10's "+0 requests on re-opening the same place within the TTL" is unimplementable if the only thing holding the memo has already been deallocated.
- `resolve` is idempotent per `place.id`: a second call while `.resolving` is a no-op. Its first act is a memo lookup, its last act on a terminal `.resolved` is a memo write (§4.7).
- `select` is the *entire* work of a route-control tap. No network, no recomputation. PRD req 7's 400 ms is met structurally, not by optimisation.
- `reset()` clears **this presentation's** geometry only. It never touches the memo — a dismissal is not an invalidation, and treating it as one would re-issue 3 requests on every re-open.

### 4.5 `ScenicWaypointPlanner` — the heuristic, refined

The PRD's proposal, restated: *corridor around the straight A→B line → keep Hoods flagged `false` → rank by curated-place count → use the Hood's nearest curated place as the waypoint.* Refined on three points, each with its reason:

**(a) The corridor is the fast route's own polyline, not the straight A→B line.** The straight line in Tel Aviv crosses the sea, the Ayalon, and the rail corridor; the fast route is the actual walkable path. It also removes the need for an origin coordinate of our own — the fast polyline starts at the origin MapKit resolved. Buffer: **800 m**. *Measured, not guessed:* on an Old North → Neve Tzedek corridor a 500 m buffer catches only Hoods the route already runs through (`kerem-hateimanim` 3 m, `lev-hair` 5 m, `old-north` 25 m); the first genuinely off-route Hood is 433 m and the next 611 m. 500 m would make the candidate set empty by construction on typical corridors.

**(b) The waypoint is the candidate Hood's curated place nearest the fast polyline; where the Hood has no curated place, `Hood.centroid`.** The PRD is right that a centroid can land somewhere unwalkable — but three gates already catch that outcome: `MKDirections` snaps a waypoint to the pedestrian network, `RouteBounds` (§4.6) rejects a resulting detour that is too long, and the distinctness test rejects one that collapsed back onto the fast route. The worst case of a bad centroid is "no scenic alternative," which is a specified state. Excluding place-less Hoods instead would eliminate **every** eligible candidate in today's data (§1.2) and would make the feature's availability depend on curation density rather than on geography.

**(c) Ranking gets a second key, because the first one is 0 for every candidate today.** Sort by (1) curated-place count descending — correct for real data, kept; (2) waypoint distance to the fast polyline ascending — nearer waypoint, smaller detour, and non-degenerate on the shipped bundle; (3) `Hood.id` ascending, so the ranking is total and the tests are deterministic.

Full contract:

```swift
struct WaypointCandidate: Sendable, Equatable {
    let hood: Hood
    let coordinate: CLLocationCoordinate2D
    let curatedPlaceCount: Int
    let offRouteDistance: CLLocationDistance
}

enum ScenicWaypointPlanner {
    static func candidates(
        alongFastRoute route: [CLLocationCoordinate2D],
        destinationHoodID: String,
        hoods: [Hood],
        places: [Place]
    ) -> [WaypointCandidate]
}
```

Filter chain, in order, each one falsifiable on its own:

1. `hood.isTouristTrap == false`. **`nil` is never eligible** — PRD req 2's pass/fail bullet, and the trap `feasibility.md` named by name. Written as `== false` against a `Bool?`, never as `!= true`, never as a `Bool` coerced upstream.
2. `hood.id != destinationHoodID`, and `hood` does not contain the fast route's **first** coordinate (the origin's Hood). Routing "through" either is meaningless.
3. `hood.boundingRect`/ring comes within `corridorBuffer` = 800 m of the fast polyline.
4. Its waypoint's distance to the fast polyline is within `[minimumOffRoute 250 m, maximumOffRoute 1200 m]`. Below 250 m the scenic route would be the fast route with extra steps; above 1200 m it cannot survive §4.6's time bound on any realistic walk, and rejecting it here saves two directions requests.
5. Sort by the three keys above.

**Origin-and-destination-in-the-same-Hood (PRD req 4, bullet 2) is checked before any of this**, in `RoutePreviewModel`: resolve the fast route's first coordinate with the existing `HoodHitTester`; if it equals `place.hoodID`, the result is `.originAndDestinationShareAHood` and no candidate search runs. Structural, reproducible, and it costs one hit-test.

### 4.6 `RouteBounds` — the detour is bounded, and so is the search

```swift
enum RouteBounds {
    static let detourTimeMultiplier = 1.5           // PRD req 3 — ratified
    static let detourTimeCeiling: TimeInterval = 900 // +15 min — ratified
    static let minimumFastTravelTime: TimeInterval = 300   // 5 min — added, [ASSUMPTION]
    static let resolveBudget: TimeInterval = 2.5    // wall clock, whole resolve
    static let maximumCandidateAttempts = 2

    static func accepts(scenic: TimeInterval, fast: TimeInterval) -> Bool {
        scenic <= min(fast * detourTimeMultiplier, fast + detourTimeCeiling)
    }
}
```

- The PRD's "≤ 1.5× **and** ≤ +15 min" is a `min`, which is what the predicate above computes. On a 20-minute walk the binding bound is 30 minutes; on a 60-minute walk it is 75.
- **`minimumFastTravelTime` is added by this TRD. [ASSUMPTION].** A 4-minute walk has no room for a scenic alternative; 1.5× of it is two extra minutes, which is noise offered as a choice. Below the floor the answer is `.walkTooShort` — a stated state, not a hidden filter.
- **`resolveBudget` and `maximumCandidateAttempts` together make PRD req 7's 3 s structural.** Candidates are attempted in rank order; the loop stops at the first accepted plan, at 2 attempts, or when 2.5 s have elapsed since resolve began — whichever comes first. Worst case: 1 fast request + 2 attempts × 2 legs = **5 requests**, but the two legs of an attempt run concurrently and the budget cuts the second attempt off before it can breach 3 s. **The concurrent pair is the reason A1 exists:** an `async let`/`TaskGroup` fan-out of two `leg(from:to:)` calls sends both endpoints across an isolation boundary, and `RouteEndpoint` can make that crossing where `MKMapItem` cannot (§4.1, §2.2). **Typical case is 3 requests** (fast + one accepted attempt). §9 row 10 counts them.

### 4.7 Request volume and the session memo (the PRD's open question 2)

| Event | `MKDirections` requests |
|---|---|
| Place modal opens, location authorized, first time this session | 3 typical, 5 worst case (§4.6) |
| Tapping Fast or Scenic, any number of times | **0** |
| Re-opening the same place within 5 minutes | **0** — memo hit |
| Place modal opens, location denied | **0** — `.noOrigin` short-circuits before any request |
| App backgrounded and returned | memo cleared; next open re-resolves |

**Who owns the memo: `RouteMemoStore`, not `RoutePreviewModel` (A2).** The memo has to survive a modal dismissal — that is its entire purpose, and it is what the "0 on re-open" row above asserts — so it cannot live in an object that is torn down on dismissal (§4.4).

```swift
@MainActor @Observable
final class RouteMemoStore {
    /// Returns nil when absent OR expired. Expiry is evaluated on read, so no
    /// timer exists and a stale entry can never be observed.
    func preview(for id: Place.ID, now: Date = .now) -> RoutePreview?

    /// Stores `.resolved` only. `.failed`, `.noOrigin`, `.resolving` and
    /// `.idle` are never memoised — a transient failure or a permission state
    /// must be retried on the next open, not cached for five minutes.
    func store(_ preview: RoutePreview, for id: Place.ID, now: Date = .now)

    func clearAll()      // scenePhase == .background
}
```

- **Lifetime:** one instance, `@State` on `MapScreen` and injected with `.environment(routeMemoStore)` on the same `Group` that already carries `placeCatalog`/`detailRouter`/`savedPlacesStore` — that call site documents in its own comment why the sheet's content closure does not inherit environment values applied elsewhere, and `RouteMemoStore` is subject to the same trap. It outlives every `RoutePreviewModel`, and dies with the app.
- **Storage:** `[Place.ID: (RoutePreview, Date)]`, in memory. **Key is `Place.id` alone** — no coordinate, per §3.3.
- **TTL 5 minutes, evaluated on read**, so there is no timer, no invalidation callback, and nothing to leak. The TTL exists because the origin can move while the memo cannot see that it did; five minutes of walking is far enough to make a cached duration wrong, and short enough that browsing several places in a Hood costs one resolve each rather than one per tap.
- **Cleared on `scenePhase == .background`**, from `MapScreen`'s existing `.onChange(of: scenePhase)` — the same hook `densityStore`/`eventStore` already use, not a second observer.
- **`clearAll()` is the only invalidation.** There is deliberately no per-entry eviction API: nothing in this feature knows better than the TTL when a route went stale.
- **Not persisted, not `Codable`, no disk seam** (§3.3). `SavedPlacesStore` is the shape it borrows, minus persistence.

Resolution is serialized: `RoutePreviewModel` runs at most one `resolve` at a time and cancels a superseded one when the modal switches places, so rapid modal-hopping cannot fan out into concurrent request storms and trip `MKError.loadingThrottled`.

### 4.8 Hand-off (PRD req 5)

`DirectionsService` gains exactly one thing — a disclosure the modal can render — and keeps its single walking-mode call site:

```swift
extension DirectionsService {
    /// Apple Maps takes a destination, not an itinerary. There is no public
    /// API that carries an intermediate stop into it, so a scenic selection
    /// is always disclosed before the user leaves (PRD req 5).
    static let waypointDisclosure =
        "Maps gets the destination only — the scenic detour stays here."
}
```

- Go continues to call `router.closeHood()` then `directionsService.open(_:to:)` with walking mode, unchanged from T-033.
- When `selection == .scenic`, the disclosure line is rendered **in the modal, above the Go button, before the tap** — never an alert after. Req 5's "before leaving Passenger" is then a rendering fact, not a timing hope.
- The `availableApps().isEmpty` disabled branch is inherited unchanged.

### 4.9 Rendering — `RouteLayer` and the line channel (PRD req 1)

Drawn on the main map behind the sheet (§1.2, §11 D9). Both polylines render whenever both exist; the selected one is dominant.

| Element | Style |
|---|---|
| Selected route, casing | `lineWidth 8`, `Color(.systemBackground)`, drawn first |
| Selected route | `lineWidth 5`, `Color.accentColor`, `lineCap .round` |
| Unselected route | `lineWidth 3`, `Color.accentColor.opacity(0.4)` |
| Scenic route (either state) | same widths, `StrokeStyle(dash: [2, 8], lineCap: .round)` — a dotted line |
| Fast route (either state) | solid |

**Against the Hood channel** (`HoodLayer.swift`, read directly): unflagged Hood stroke is `lineWidth 0.5`; flagged plain is `2.5`; flagged + busy is `3` with `dash: [6, 4]`; all three use `Color("Flag")`. A selected route is `5 pt` — **≥ 1.67× the widest Hood stroke** — carries an 8 pt casing no Hood stroke has, and uses `accentColor`, not `Color("Flag")`. The scenic dash `[2, 8]` (round dots, 8 pt gaps) is not confusable with `[6, 4]` (long dashes, 4 pt gaps) at any zoom. Fast vs scenic is solid-vs-dotted, so the pair survives greyscale — `design-principles.md` §3, "never rely on colour alone."

**Camera.** On first resolve, fit the camera to the union of both polylines' bounding rects, with a **bottom inset equal to the presented sheet's height** at `.medium`. This is not decoration: `qa` measured (2026-08-04, T-036) that the depth-1 sheet at `.medium` occupies y 415–866 on an iPhone 17 — more than half the screen. A fit without the inset centres the route under the sheet. Selecting the other route does **not** re-fit; the camera moves once, on resolve.

### 4.10 `RouteControls` — the states (PRD reqs 3, 4, 6, 7)

One control per route, each rendering exactly one of:

| Model state | Fast control | Scenic control |
|---|---|---|
| `.resolving` | title + progress indicator, disabled | title + progress indicator, disabled |
| `.noOrigin` | not rendered — the plain Directions button of T-033 stands in its place | not rendered |
| `.failed` | not rendered — same fallback as `.noOrigin` | not rendered |
| `.resolved(fast, .success)` | duration + distance, selectable | duration + distance, `via <Hood name>`, selectable |
| `.resolved(fast, .failure(reason))` | duration + distance, selectable | **disabled, with a plain line** |

Disabled copy, one per `ScenicUnavailable` case, all rendered in the same slot:

| Case | Line |
|---|---|
| `originAndDestinationShareAHood` | "You're already in this neighborhood." |
| `walkTooShort` | "Too short for a scenic detour." |
| `noQualifyingHood`, `notDistinct`, `detourTooLong`, `routingFailed` | "No scenic alternative for this walk." |

The last four collapse to the PRD's own literal string because the distinction between them is diagnostic, not user-facing. The enum keeps them apart anyway so tests can tell which fired — §9 rows 4 and 12.

The **P1** "via Florentin" naming is implemented (`viaHoodName` is already carried on `RoutePlan` and it costs one `Text`). The **P1** last-mode memory is **not** — it needs a persistence surface §3.1 says this feature does not add.

---

## 5. Flow

**Main path.** Place modal appears → `.task(id: place.id)` → `routeMemoStore.preview(for: place.id)` non-nil? render it, 0 requests → else `.resolving` → authorization gate; unauthorized ⇒ `.noOrigin`, stop, **nothing written to the memo** → fast leg: `.currentLocation` → `.coordinate(place.coordinate)` ⇒ `RoutePlan(.fast)`; failure ⇒ `.failed`, stop, **nothing written to the memo** → hit-test the fast polyline's first coordinate; same Hood as `place.hoodID` ⇒ `.originAndDestinationShareAHood` → `fast.travelTime < 300 s` ⇒ `.walkTooShort` → `ScenicWaypointPlanner.candidates(...)`; empty ⇒ `.noQualifyingHood` → for each of the first 2 candidates, while under the 2.5 s budget: two legs concurrently → concatenate → `RouteBounds.accepts` ⇒ else next candidate → divergence test (leaves the fast route's 25 m corridor for a contiguous ≥ 100 m run) ⇒ else next candidate → accepted ⇒ `.resolved(fast, .success(scenic))` → **written to `routeMemoStore` under `place.id`** (every terminal `.resolved` is memoised, success or stated-failure alike — a `.noQualifyingHood` answer is as expensive to recompute as a successful one and just as stable for five minutes) → both polylines drawn, camera fitted once, Fast selected by default → tap Scenic ⇒ local selection flip, dominance swaps, disclosure line appears → Go ⇒ `closeHood()` + Apple Maps, walking, destination only.

**Exhausted candidates** ⇒ the reason from the *last* attempt (`detourTooLong` or `notDistinct`), not a generic failure — the enum carries which.

**Edge and error paths, each landing in a named state:** location denied or restricted ⇒ `.noOrigin`, no request issued, T-033's plain Directions button unchanged (req 6). Fast leg throttled or not found ⇒ `.failed`, same fallback. Scenic leg throttled or not found ⇒ `.routingFailed`, fast route still offered. Modal dismissed mid-resolve ⇒ the task is cancelled, `reset()` clears geometry, `RouteLayer` draws nothing, **and nothing is written to the memo** — a cancelled resolve leaves no partial entry to be served on the next open. A second place opened mid-resolve ⇒ first resolve cancelled, no partial state leaks (`RoutePreviewModel` is per-presentation; the memo it shares with the next model is keyed on `Place.id`, so the two presentations cannot see each other's route).

**Why the divergence test exists.** Req 4's third bullet — "if the scenic polyline comes back identical to the fast one, treat it as no scenic route" — cannot be implemented as polyline equality: MapKit returns different point counts for the same path across requests, so an equality check would never fire and the requirement would pass by never being tested. `RouteCorridor.diverges(_:from:minimumRun: 100, tolerance: 25)` is the falsifiable form: sample the scenic polyline every 20 m, compute each sample's distance to the nearest fast-route segment, require a contiguous run of ≥ 5 samples beyond 25 m.

---

## 6. Third-party / dependencies

**MapKit `MKDirections`, chained. Google Directions rejected.**

| | MapKit `MKDirections` | Google Directions API |
|---|---|---|
| Waypoints | **None.** 1 waypoint = 2 chained requests | Native, one request |
| Cost | Free, no account | Paid per request, needs a billing account — **Aviran-gated on two counts** |
| Credentials | None | An API key shipped in the client, plus a restriction/rotation story neither this repo nor `ACCOUNTS-AND-COSTS.md` has |
| Rendering | Already the app's map | Google's platform terms restrict displaying Directions content on a non-Google map. **[ASSUMPTION] — stated from recollection of the Maps Platform terms, not re-read this session; it must be verified before Google is ever adopted, and it is not load-bearing here because the three rows above already decide it** |
| In the codebase | `Support/DirectionsService.swift` already imports MapKit and hands off walking mode | Nothing |

The cost of chaining is one extra network request per scenic attempt and one seam to dedup (§4.2). The cost of Google is money, an account, a key in the client, and a legal question — for a Phase-1 preview feature whose own PRD says "Passenger computes no route."

**Upstream data dependencies:** `hoods-tel-aviv.json` (`hood-dataset`, T-040, shipped) and `places-tel-aviv.json` (`places-dataset` Phase-1 fixture, shipped). Both already deliver every field this feature reads. No supporting data PRD is owed.

---

## 7. Rollout & migration

- **No feature flag.** The feature is inert wherever it cannot produce a result: no location authorization, no qualifying Hood, or a detour over bounds all render specified states, and the shipped Directions button behaviour of T-033 is preserved on every one of them. A flag would add a branch with nothing behind it. `BuildPhase` gains **no fourth constant** — this feature reads bundled data in Phase 1 and bundled-or-fetched data in Phase 2 through `HoodCatalog`/`PlaceCatalog`, whose own constants already carry that switch.
- **No schema migration.** §3.1. The one regenerated SQL artifact (§3.4) is a re-seed of an existing unapplied migration, not a schema change, and stays Aviran-gated like every other apply.
- **Backward compatibility:** `Hood`, `Place`, `DetailRouter`, `LocationStore` and `DirectionsService` gain no required field and no changed signature. `PlaceDetailModal`'s route button is replaced by `RouteControls`, which renders that same button verbatim in `.noOrigin`/`.failed`.
- **Build Phase 2 changes nothing here.** Real flag values arriving from Supabase improve candidate quality; the code path is identical. The only Phase-2 action is that the provisional flags from §3.4 must be overwritten, which is why condition 6 requires them marked.

---

## 8. Risks & alternatives

**R1 — "Not a tourist trap" is being used as a proxy for "worth walking through," and it is not one.** The only V1 signal is `isTouristTrap == false` (decision #37 retired the graduated tag). A Hood can be entirely un-touristy and still be a place you would not route a visitor through after dark — `neve-shaanan` (the old central bus station) is `null` today, but nothing in this design would stop a `false` flag there from becoming a recommended detour. **This is the single biggest product risk in the feature and it is not solvable in the architecture.** Mitigations available now: the Phase-1 fixture is a curated allow-list, not an inference (§3.4); and the flag's Phase-2 source is the local-QA loop, whose proposing algorithm the PRD already notes has no owner. **For Aviran / `product`:** either accept that "not flagged tourist-heavy" is the whole basis of the recommendation in V1, or add a second gate before real data drives it.

**R2 — Chained legs can double back.** Leg 2 is planned without knowledge of leg 1's approach, so a route can pass the waypoint, continue, and turn around. Real and visible. Not fixable without per-segment control, which is exactly what decision #44 declined. Accepted; the detour bound caps how bad it can get in time terms.

**R3 — "No scenic alternative" may be the common state.** Three independent causes: the flag is sparse (PRD's own risk), the 800 m corridor is narrow relative to Tel Aviv's Hood scale, and short urban walks trip `minimumFastTravelTime`. This is why req 4's disabled state is specified and rendered rather than hidden — but if it fires on most walks in real use, the feature is a disabled button most of the time. The tunable knobs are `corridorBuffer`, `maximumOffRoute`, and `minimumFastTravelTime`, all constants in one file for exactly that reason.

**R4 — The fixture is a demo, and a demo can be mistaken for data.** Three Hoods flagged `false` to make a build phase demonstrable are an authoring act, not a finding. Condition 6's provisional marking is the whole defence. If it is skipped, Phase 2 has no way to tell a demo flag from a curated one.

**R5 — `MKDirections` throttling under test.** A UI test that opens several place modals in sequence issues real directions requests and can trip `MKError.loadingThrottled`, turning a correctness test into a flaky one. Mitigation: every automated assertion below the UI layer runs against a scripted `WalkingRouteProvider`; UI tests assert states, and where they need real routing they are the small minority and are named as such in §9.

**Alternatives considered and rejected:** Google Directions (§6). A mini-map inside the modal (§1.2 — the PRD's own Hood-outline bullet rules it out, and it doubles map instances). Excluding Hoods with no curated place (§4.5b — it empties the candidate set on today's data). Polyline equality for req 4's identical-route rule (§5 — it would never fire). Two waypoints in V1 (§11 D2). A persisted route cache (§3.3 — it would put a location-derived path on disk for a preview).

---

## 9. Verification — one row per P0 requirement, and one per normative rule

Per L-018, L-032 and `architect.md`. `qa` builds `TEST-PLAN.md` from this table.

**Three standing rules bind every row.** (a) **No pass condition is satisfiable over an empty set** — every ∀ below is preceded by an exact count. (b) **Every negative-existence check carries a positive control** — each `grep … → 0 hits` is run alongside a second grep over the *same paths* for a symbol that must be present, returning > 0; a zero there means the path list is wrong and the row is **unrun**, not passed. (c) **A requirement about what the user sees is checked on rendered output** — `XCUIElement.exists` is `true` for a fully occluded element and `.label` returns the whole string regardless of truncation, so rows about visibility assert frames and rendered geometry, and assert those frames are non-empty first. A rendered row that cannot be run is **BLOCKED**, never passed.

| # | Requirement | Observable | Pass condition | Layer | Step |
|---|---|---|---|---|---|
| **1** | Two routes, one surface, walking only (req 1) | (a) presentation surfaces added by the feature; (b) `transportType` set anywhere in the app; (c) both polylines rendered with both plans present; (d) rendered widths/dashes of the two routes and of a flagged Hood in the same frame; (e) route line vs Hood stroke at neighborhood zoom, greyscale | (a) `grep -rn "NavigationStack\|NavigationLink\|fullScreenCover" Passenger/Routing Passenger/Map/RouteLayer.swift Passenger/Detail/RouteControls.swift` → **0 hits**, positive control `grep -rn "RoutePlan" <same paths>` → **> 0**; and `router.placeDepth ?? 0 <= 2` after every route interaction; (b) exactly **one** occurrence of `.walking` in `Passenger/Routing`, in `WalkingRouteProvider`'s MKDirections conformer, and `grep -rn "\.automobile\|\.transit\|\.any" Passenger/Routing` → **0 hits**; (c) `RouteLayer` constructs exactly **2** `MapPolyline`s (plus 1 casing) when `scenic` is `.success`, and exactly **1** (plus 1 casing) otherwise; (d) asserted as numbers, not by eye: selected route `lineWidth == 5`, casing `== 8`, unselected `== 3`, scenic `dash == [2, 8]`, fast dash `== nil`, and the widest Hood stroke in the same render `== 3` with `dash == [6, 4]` — so selected ÷ widest-Hood **≥ 1.6** and the two dash arrays are unequal; (e) in a greyscale screenshot at span < 0.06 with **≥ 1 flagged Hood and both routes present** (counts asserted first), the two route lines and the Hood outline are three visually distinct strokes | unit + UI test + manual (greyscale) | C4, C6, C8 |
| **2** | Scenic is the same API plus waypoints; `null` is never a waypoint (req 2) | (a) routing engine surface; (b) `candidates(...)` over a hood set of **8**: 3 `null`, 2 `true`, 3 `false`, all in corridor; (c) the same call with **all 8** `null`; (d) the same with all 8 `false` but all out of corridor; (e) the eligibility expression in source | (a) `grep -rn "graph\|Dijkstra\|A\*\|segment\|weight" Passenger/Routing` → **0 hits**, positive control `grep -rn "MKDirections" Passenger/Routing` → **exactly 1 file**; and no new file under `Resources/` (b) result count is **exactly 3**, and every element's `hood.isTouristTrap == false` — the count assertion first, so the ∀ cannot carry the row; (c) result is `[]` **and** `RoutePreviewModel` lands on `.noQualifyingHood`, i.e. an all-`null` world offers no scenic route; (d) `[]` — proves the corridor filter fires independently of the flag filter; (e) `grep -n "isTouristTrap == false" Passenger/Routing/ScenicWaypointPlanner.swift` → **exactly 1 hit**, and `grep -n "isTouristTrap != true\|isTouristTrap ?? " Passenger/Routing` → **0 hits** | unit | C2 |
| **3** | The detour is bounded and its cost is shown (req 3) | (a) `RouteBounds.accepts` at four points; (b) a scripted provider returning a scenic leg pair over bound; (c) the rendered Fast and Scenic controls with both plans present; (d) the constants | (a) `accepts(scenic: 1799, fast: 1200) == true`, `accepts(1801, 1200) == false` (the 1.5× bound binds), `accepts(4499, 3600) == true`, `accepts(4501, 3600) == false` (the +900 s ceiling binds) — four distinct assertions, two on each side of each bound; (b) preview is `.resolved(fast, .failure(.detourTooLong))`, never `.success` — a scenic plan is **not** reachable over bound by any code path; (c) with **both** controls asserted present first, each renders a non-empty duration string **and** a non-empty distance string, and the two duration strings differ; (d) `detourTimeMultiplier == 1.5`, `detourTimeCeiling == 900` | unit + UI test | C3, C5 |
| **4** | "No scenic route" is a stated state (req 4) | (a) each of the 6 `ScenicUnavailable` cases driven through `RouteControls`; (b) origin and destination in the same Hood, on device, on the documented demo corridor; (c) a scripted provider whose scenic legs return the fast route's own coordinates; (d) hidden-vs-disabled | (a) **all 6** cases render: the control **exists**, `isEnabled == false`, and a non-empty explanatory `Text` is present in the same slot — asserted per case, six assertions, and the case→copy mapping matches §4.10 exactly; (b) preview is `.originAndDestinationShareAHood` and **zero** `MKDirections` requests were issued for a scenic leg (scripted provider call count `== 1`, the fast leg only); (c) preview is `.notDistinct` — and a positive control on the same test class proves the divergence test *can* return `true`, so the row is not passing because the test always says "not distinct"; (d) in every one of the 6 cases the Scenic control's rendered `frame` is **non-empty** (it is disabled, not hidden) — checked on frames, not `.exists` | unit + UI test | C3, C5 |
| **5** | Go hands off; Passenger never navigates (req 5) | (a) navigation surface; (b) the launch options used; (c) the disclosure line with `selection == .scenic`; (d) the same with `selection == .fast`; (e) `availableApps().isEmpty` | (a) `grep -rn "MKRoute.steps\|instructions\|AVSpeech\|rerout" Passenger` → **0 hits**, positive control `grep -rn "MKDirections" Passenger` → **> 0**; (b) exactly one `openInMaps` call site in the app, carrying `MKLaunchOptionsDirectionsModeWalking` — unchanged from T-033; (c) the disclosure `Text` is rendered **and its frame is non-empty and not covered by the Go button's frame**, and it is present *before* any tap on Go (asserted on the pre-tap snapshot); (d) that same `Text` is absent; (e) Go is disabled and the T-033 explanation line renders — inherited behaviour re-asserted, not assumed | unit + UI test | C7 |
| **6** | No origin means no preview, not a broken one (req 6) | (a) `authorizationStatus == .denied`; (b) the same, request count; (c) the same, the surviving control | (a) preview is `.noOrigin`; **no** duration or distance string is rendered anywhere in the modal (assert the two controls' count is **0**); `RouteLayer` constructs **0** polylines; (b) scripted provider call count is **exactly 0** — nothing is requested without an origin; (c) T-033's plain Directions button is present, enabled, and its tap still calls `openInMaps` with walking mode — the shipped behaviour, re-asserted | unit + UI test | C5, C7 |
| **7** | Responsiveness (req 7) | (a) the work done by a route-control tap; (b) wall clock from `resolve` start to a terminal state, scripted provider with a 400 ms per-leg delay; (c) the same against **real** `MKDirections` on the demo corridor; (d) the `.resolving` control state | (a) `select(_:)` performs no `await` and touches no provider — `grep -n "await\|provider" ` in `select`'s body → **0 hits**, and provider call count is unchanged across 5 taps; the tap therefore cannot exceed one frame; (b) terminal state reached in **< 3 s**, and the state is asserted to be a *specific* one (`.resolved` with `.success`) — a fast `.failed` would satisfy a bare time bound and prove nothing; (c) 5 runs, median < 3 s, **each run's state asserted non-`.failed`**; if `MKError.loadingThrottled` appears the row is **BLOCKED, not passed**, and re-run on a cold app; (d) while `.resolving`, both controls render a progress indicator and `isEnabled == false` | unit + manual (device) | C3, C5 |
| **8** | Build Phase 1 can demonstrate this (req 8) | (a) `isTouristTrap` values in `Bundle.main`'s `hoods-tel-aviv.json`; (b) pairwise geometry of the `false` set; (c) generator determinism; (d) the demo corridor, on device | (a) count of `false` is **≥ 4** (`ramat-aviv` + the three authored) and count of Hoods total is **24** — both exact, read from `Bundle.main` like `PassportBundleInvariantTests`, not from a test fixture; (b) for **every pair** in the `false` set (pair count asserted `≥ 6` first): min vertex-to-vertex distance **> 50 m** and centroid separation **≥ 800 m**; (c) re-run `build_hoods.py` to a scratch path and `diff` — SQL byte-identical, JSON identical modulo `generatedAt`. **This is the only check that proves no hand-edit survived (L-024); reading the bundle proves nothing**; (d) on the documented corridor, the Scenic control resolves to `.success` with a named `viaHoodName`, **and** a second documented A→B on the same fixture resolves to a disabled Scenic control — a positive and a negative case, both run | unit + manual (device) | A1, C9 |
| **9** | *(normative, §4.5)* The corridor is derived from the fast route, and every filter fires independently | (a) `candidates(...)` with a fast polyline that bends far off the straight A→B line, and a Hood placed near the *straight line* but > 800 m from the polyline; (b) a Hood 100 m off the polyline; (c) a Hood 1500 m off | (a) that Hood is **absent** from the result, and a second Hood 400 m off the polyline is **present** — proves the corridor follows the route, not the chord; (b) absent (`minimumOffRoute`); (c) absent (`maximumOffRoute`); and a control candidate at 500 m is present in all three runs, so no run is passing on an empty result | unit | C2 |
| **10** | *(normative, §4.4/§4.6/§4.7)* Request volume is capped and taps cost nothing | scripted provider call counts across a scripted session. **Every "re-open" below destroys the `RoutePreviewModel` and builds a new one against the same `RouteMemoStore`** — reusing a live model would make the memo rows pass without a memo existing at all, which is precisely the defect A2 fixed | modal open with an accepted first candidate → **exactly 3**; with both candidates rejected → **exactly 5**, never more; 5 route-control taps after resolve → **+0**; re-open the same place on a **new model instance** within TTL → **+0**; re-open on a new model after TTL expiry (injected `now`, not a real wait) → **+3**; open with authorization denied → **+0**. Six exact counts, no ranges | unit | C3 |
| **11** | *(normative, §3.3)* The app never holds or persists a user location | (a) CoreLocation surface in `Routing/`; (b) persistence surface; (c) logging surface; (d) memo key type | (a) either `grep -rn "startUpdatingLocation\|CLLocationCoordinate2D(" Passenger/Routing` → **0 hits**, or — if §4.3's fallback was taken — exactly one `requestLocation()` whose `CLLocation` is not assigned to any stored property (`grep -rn "var .*CLLocation\|let .*CLLocation" Passenger/Routing` → **0 hits**); positive control `grep -rn "MKMapItem" Passenger/Routing` → **> 0**. *Note for whoever runs this:* the conformer's `CLLocation(latitude:longitude:)` on the **destination** (§4.1) is not a hit on either pattern and is not a violation — the destination is a place's already-public coordinate, and the rule is about the *user's* position; (b) `grep -rn "UserDefaults\|AppStorage\|FileManager\|\.write(to:\|Codable" Passenger/Routing` → **0 hits**; (c) `grep -rn "print(\|os_log\|Logger(" Passenger/Routing` → **0 hits**; (d) `RouteMemoStore`'s dictionary key type is `Place.ID` — asserted in source, and `grep -n "latitude\|longitude" Passenger/Routing/RouteMemoStore.swift` → **0 hits**, positive control `grep -n "Place.ID" Passenger/Routing/RouteMemoStore.swift` → **> 0** | unit (static) | C1, C3 |
| **12** | *(normative, §4.9)* The camera fits the route without hiding it under the sheet | rendered camera region after resolve, with the sheet presented at `.medium` | both polylines' bounding rect is contained in the visible map region **and** the route's rect centre lies **above** the sheet's top edge (y < the sheet's `frame.minY`, measured from the rendered sheet, not assumed) — and the polyline count is asserted `≥ 1` first. Selecting the other route leaves the region's four components **byte-identical** (the camera moves once) | UI test | C6 |
| **13** | *(normative, §2.2/§4.1 — added by amendment A1)* No non-`Sendable` MapKit type crosses a concurrency boundary, and nothing is `@unchecked Sendable` | (a) the protocol's signature; (b) MapKit reference types anywhere outside the conformer; (c) the escape hatch; (d) the compiler | (a) `grep -n "func leg(" Passenger/Routing/WalkingRouteProvider.swift` → **exactly 1 hit**, and it contains `RouteEndpoint` **twice** and `MKMapItem` **zero** times; (b) `grep -rn "MKMapItem\|MKDirections\|MKRoute" Passenger/Routing` → hits in **exactly 1 file** (`WalkingRouteProvider.swift`), positive control: that same grep returns **> 0** overall, so an empty result means the path list is wrong and the row is **unrun**; and `grep -rn "MKMapItem" Passenger/Routing/RoutePreviewModel.swift Passenger/Routing/RouteEndpoint.swift Passenger/Routing/RoutePlan.swift Passenger/Routing/RouteMemoStore.swift` → **0 hits**; (c) `grep -rn "@unchecked Sendable\|nonisolated(unsafe)" Passenger/Routing` → **0 hits**, positive control `grep -rn "Sendable" Passenger/Routing` → **> 0**; (d) the target builds clean at `SWIFT_STRICT_CONCURRENCY = complete` with **0 concurrency warnings** in `Passenger/Routing` — a warning here is the defect A1 exists to prevent, so warnings are failures for these files, not noise | unit (static) + build | C1, C3, C8 |
| **14** | *(normative, §4.4/§4.7 — added by amendment A2)* The memo outlives the model, and only settled answers are memoised | (a) lifetime; (b) what gets stored; (c) expiry; (d) background clear; (e) cross-place isolation | (a) resolve on model instance **A**, discard A, create instance **B** against the same store, resolve the same `place.id` → B reaches `.resolved` with **+0** provider calls, **and** a control run with a *fresh* store makes **3** calls, so the row cannot pass on a provider that never gets called at all; (b) drive `.failed` and a cancelled mid-resolve, then re-open each on a new model → each issues its requests again, **+3** and **+3**, proving neither was memoised; and for `.noOrigin`, assert `store.preview(for: id) == nil` directly — its `+0` on re-open is a permission short-circuit, not a memo hit, and only the store read tells those two apart; (c) with an injected `now` past the TTL, `preview(for:)` returns `nil` — and returns non-`nil` 1 second before the boundary, both sides asserted; (d) after `clearAll()`, `preview(for:)` is `nil` for **every** id previously stored (id count asserted **≥ 2** first, so the sweep isn't passing over an empty store); (e) resolve two different places, then read both back — each returns its own plan, and the two plans' `coordinates` differ | unit | C3, C6 |

**Not checkable in Phase 1, named rather than waved through:** nothing. Every row above has a runnable check. Rows 7(c) and 8(d) require a device/Simulator and real MapKit; both are marked manual and both have a stated BLOCKED condition.

---

## 10. Build breakdown

Ordered. Tags per `BOARD.md`'s lifecycle section.

| Step | Tag | Work |
|---|---|---|
| **A1** | **[Algo/Data]** | Author the req 8 fixture in `database/data/hoods-tel-aviv.source.json` per §3.4's six conditions — three `false` flags, provisional-marked with provenance, plus the demo corridor written into the file's header note. Re-measure the candidate proposal against a real `MKDirections` fast route before committing. Regenerate with `build_hoods.py --migration-number 007` (§3.4's migration note) — this writes **both** `passenger-brain/database/migrations/007_hoods_tel_aviv_data.sql` **and** `passenger-code/Passenger/Resources/hoods-tel-aviv.json`, so the step lands in both repos. Verify by re-running the generator to a scratch path and diffing (§9 row 8c). **Blocks C9 only; C1–C8 do not wait on it.** |
| **C1** | **[iOS]** | `Routing/RoutePlan.swift`, `RouteEndpoint.swift`, `RoutePreview.swift`, `RouteBounds.swift` — the value types and constants, all `Sendable`, with the hand-written `==` implementations §3.2 names. No behaviour. Confirm at this step that the target still builds clean at `SWIFT_STRICT_CONCURRENCY = complete` (§9 row 13d) — the cheapest point in the build to find out otherwise. |
| **C2** | **[iOS]** | `Routing/RouteCorridor.swift` + `ScenicWaypointPlanner.swift` — pure geometry and the ranked candidate filter (§4.5). Unit tests first; this is the feature's algorithm and it needs no simulator. |
| **C3** | **[iOS]** | `Routing/WalkingRouteProvider.swift` (protocol taking `RouteEndpoint` + `MKDirections` conformer that builds every `MKMapItem` locally + concatenation, §4.1/§4.2), `RouteMemoStore.swift` (§4.7), and `RoutePreviewModel.swift` (resolve loop, budget, attempt cap, memo read/write, §4.4/§4.6/§4.7). Tested against a scripted provider. **Both amendments land here** — this is the step they were written for. |
| **C4** | **[iOS]** | `Map/RouteLayer.swift` — the two polylines, casing, weights, dashes (§4.9). |
| **C5** | **[iOS]** | `Detail/RouteControls.swift` — the five model states, the six disabled lines, durations and distances (§4.10). |
| **C6** | **[iOS]** | `Map/MapScreen.swift` — render `RouteLayer`, fit the camera once with the sheet-height bottom inset (§4.9), own `RouteMemoStore` as `@State` and inject it on the same `Group` as `placeCatalog`/`detailRouter`/`savedPlacesStore` (the call site whose comment explains why the sheet's content closure doesn't inherit environment values applied elsewhere), and call `clearAll()` from the existing `.onChange(of: scenePhase)` on `.background` (§4.7). |
| **C7** | **[iOS]** | `Detail/PlaceDetailModal.swift` + `Support/DirectionsService.swift` — host `RouteControls`, add the waypoint disclosure line, preserve T-033's Go behaviour and its `availableApps().isEmpty` branch verbatim (§4.8). |
| **C8** | **[iOS]** | Test pass: §9 rows 1–7 and 9–14. Scripted provider throughout; UI tests assert rendered frames, never `.exists` alone. |
| **C9** | **[iOS]** | The bundle-invariant test for §9 row 8(a)(b), plus the device run of 8(d) on A1's documented corridor. Depends on A1. |

**Surface split:** **[iOS]** for C1–C9, **[Algo/Data]** for A1. **No [Backend] step** — no schema, no RLS, no endpoint, no Passenger backend call (§3.1). A1 does regenerate an unapplied SQL seed as a side effect of the generator, which is why `code-reviewer` is on the review list below despite there being no backend work.

---

## 11. Decisions

| # | Decision | Why |
|---|---|---|
| **D1** | **MapKit `MKDirections`, not Google Directions** | §6. Free, no account, no key in the client, already imported. Google costs money and needs an account — both Aviran-gated — and carries a non-Google-map display restriction that would bite a MapKit app. |
| **D2** | **Exactly one waypoint in V1** (the PRD allows 1–2) | Each extra waypoint is another leg, another request, another seam, another failure mode. The detour bound rarely survives two on an urban walk. `WaypointCandidate` selection returns a list and `RoutePlan` is built from an array of legs, so two is a loop bound change, not a rewrite. |
| **D3** | **Origin is `MKMapItem.forCurrentLocation()`; the app never receives a coordinate** | `LocationStore` was built with "no coordinates, ever" as a deliberate privacy boundary. This preserves it exactly. Fallback path named in §4.3 if the iOS 26 SDK has moved the API. |
| **D4** | **The corridor is the fast route's polyline, not the straight A→B line** | Measured: a 500 m straight-line corridor on a real Tel Aviv A→B catches only Hoods the route already traverses. The route polyline is the walkable truth, and it removes the need for an origin coordinate of our own. |
| **D5** | **Resolve on modal appear; a route-control tap is pure local selection** | Reqs 3 and 4 require durations and the disabled state to be known *before* a tap — a disabled control cannot be tapped. Resolve-on-tap cannot satisfy them. This also makes req 7's 400 ms structural. |
| **D6** | **Waypoint = nearest curated place, else `Hood.centroid`** | Refines the PRD's assumption. Excluding place-less Hoods would empty the candidate set on today's data (§1.2). Three existing gates already catch a bad centroid, and the worst outcome is a specified state. |
| **D7** | **Detour bounds ratified as the PRD proposed, plus a 5-minute floor** | 1.5× and +15 min stand. The floor is new and is an **[ASSUMPTION]**: a 4-minute walk has no scenic alternative worth offering, and offering one is noise. |
| **D8** | **Req 4's "identical route" rule is a divergence test, not equality** | MapKit returns different point counts for the same path; an equality check would never fire, and the requirement would pass by never being exercised. §5 states the falsifiable form. |
| **D9** | **Polylines render on the main map behind the sheet, not in a mini-map** | The PRD's own req 1 bullet asks that a route line be distinguishable from a Hood's outline at neighborhood zoom — Hood outlines exist only on the main map. **[ASSUMPTION]** on the reading of "inside the modal's own space" as "without leaving the modal"; flagged in §12. |
| **D10** | **Line channel: casing + weight + dash, not colour** | `design-principles.md` §3. Numbers in §4.9, derived from `HoodLayer`'s actual stroke constants read from source, not from the spec's prose. |
| **D11** | **Session memo keyed on `Place.id`, TTL 5 min, cleared on background** | Caps request volume without putting a coordinate in a key (§3.3) and without letting a stale duration outlive the walk that would invalidate it. **Amended (A2):** the memo lives in `RouteMemoStore`, not in `RoutePreviewModel` — see D16. |
| **D12** | **The hand-off disclosure is unconditional and pre-tap** | No public API carries an intermediate stop into Apple Maps, so the capability never varies and a probe would be theatre. Rendering it before the tap makes req 5's "before leaving Passenger" a rendering fact. |
| **D13** | **The fixture changes Hoods only; the curated-place waypoint path is covered by unit fixtures** | Adding a place to `places-tel-aviv.json` would change the shipped seed that `SearchShippedSeedTests` and `search-quick-filters/TRD.md` §9 row 3 assert *exact arrays* against — real breakage in another feature's passing tests, for coverage a pure unit test gives for free. Consequence stated rather than hidden: the on-device Phase-1 demo exercises the centroid fallback, and §9 row 8(d) says so. |
| **D14** | **No feature flag, no new `BuildPhase` constant** | §7. Every degraded path is already a specified state, and the shipped T-033 behaviour is the floor. |
| **D15** | **`WalkingRouteProvider` speaks `RouteEndpoint`, never `MKMapItem`** *(amendment A1, 2026-08-04)* | `MKMapItem` is not `Sendable`, and the provider is called from a `@MainActor` model and from a concurrent two-leg fan-out. At `SWIFT_STRICT_CONCURRENCY = complete` the original signature is a build failure or an `@unchecked Sendable` — and `passenger-code/CLAUDE.md` bans the latter, so "make it compile" would have meant breaking a standing engineering rule at C3, under build pressure, by whoever hit it first. Moving MapKit construction inside the conformer costs one private helper and strengthens D3: the origin becomes a case with no payload. Raised by `ios-developer` at `trd-review` (`passenger-brain 8a006f7`). |
| **D16** | **The 5-minute memo lives in `RouteMemoStore`, owned by `MapScreen`; `RoutePreviewModel` stays per-presentation** *(amendment A2, 2026-08-04)* | The original draft asked one object to be both destroyed on dismissal and to remember across dismissals. The memo is the basis of §4.7's whole request-volume table and of §9 row 10's "+0 on re-open," so this was load-bearing, not a wording slip — implemented literally, either the model would have leaked into a singleton (losing per-presentation cancellation) or the memo would have silently never hit (3 requests per open, forever, with the test passing because it reused a live model). Splitting the two lifetimes keeps both properties and makes each testable on its own. Raised by `ios-developer` at `trd-review` (`passenger-brain 8a006f7`). |

---

## 12. What `trd-review` should check first

**Review pairs:** `ios-developer` + `ios-code-reviewer` (C1–C9, the whole client). `data-engineer` + `code-reviewer` (A1 — the fixture and the regenerated migration artifact).

**Outcome, 2026-08-04: all four AGREE.** `ios-developer` (`passenger-brain 8a006f7`), `ios-code-reviewer` (`dd68110`, five non-blocking build findings), `data-engineer` (`5bfee4d`, one authoring-detail ambiguity), `code-reviewer` (A1's migration path). `ios-developer`'s two pre-C3 findings are resolved in this document as amendments A1 and A2 (see the header) — documentation-only, no re-review owed. Item 1 below is **resolved**; the rest stand.

Six things, in order of how much they would cost to get wrong:

1. ~~**D3 / §4.3 — `MKMapItem.forCurrentLocation()` on the iOS 26 SDK.**~~ **Resolved at review.** `ios-developer` verified against current Apple documentation that `forCurrentLocation()` is live and still the recommended pattern; §4.3's fallback is retained as a build-time contingency only. It also confirmed that `MKDirections.Request` still carries exactly one source and one destination after WWDC25's MapKit additions — so D1/D2's chained-legs approach is the only option, not a workaround.
2. **D9 / §1.2 — the reading of "draws its polyline inside the modal's own space."** This TRD reads it as the main map behind the sheet, argued from the PRD's own Hood-outline bullet. If `product` meant a map *inside* the modal, §4.9, §9 rows 1 and 12, and step C6 all change. Cheapest question in the document to ask and the most expensive to get wrong.
3. **§8 R1 — "not a tourist trap" is not "worth walking through."** Not an architecture question; it needs `product`/Aviran. Named here because this TRD's design would happily route a visitor through a `false`-flagged Hood that nobody would recommend.
4. **§3.4 — the fixture's substance.** The three candidate Hoods are a geometric proposal only. `data-engineer` owns whether those specific Tel Aviv neighbourhoods should carry `isTouristTrap: false`, and must re-measure the corridor against a real walking route before committing.
5. **§3.4's migration note** — regenerate `007` in place, or add an `008`? `code-reviewer`'s call; `006` and `007` already seed the same table and neither is applied.
6. **§4.6's constants** — `minimumFastTravelTime` 300 s, `corridorBuffer` 800 m, `minimumOffRoute` 250 m, `maximumOffRoute` 1200 m, `resolveBudget` 2.5 s, `maximumCandidateAttempts` 2. All **[ASSUMPTION]**, all in one file, all retunable. If `ios-developer` thinks any of them makes §8 R3 worse, say so before C2.

**Open for Aviran, carried forward from the PRD and not resolvable here:**

- The strategy doc's V1-scope navigation bullet still describes decision #32's weighted per-segment routing. Decision #44 supersedes it in `decisions.md`; the source of truth still contradicts what this TRD specifies. Aviran-gated file, reported not edited (`CLAUDE.md` rule 8).
- Req 5's disclosed gap: the scenic detour cannot survive the hand-off, so a user can preview one walk and take another. §4.8 makes the disclosure unconditional and pre-tap; whether that is acceptable is Aviran's call, unchanged.
- §8 R1, above — the one this TRD adds.
