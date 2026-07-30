# Map — Hoods & Heat Area — TRD

**Task:** T-031 · **Linear:** `PAS-12` · **Status:** ready for `trd-review`
**Owner:** architect · **Date:** 2026-07-30
**PRD:** [`map-hoods-heat.md`](./map-hoods-heat.md) (Draft v2) · **Design spec:** [`design/phase-1/map-hoods-heat-design.md`](../../design/phase-1/map-hoods-heat-design.md) (Draft v2, `design-approval` PASS, `design-review` cleared on Aviran's approval)
**Mockup:** https://claude.ai/code/artifact/967ade63-ea5b-46c9-89a8-d606ed11a819 — reference only. Where this TRD and the mockup disagree, this TRD wins (see §8 D1, D2).

---

## 1. Context

Read the PRD and the design spec first; nothing here restates them. This document decides the six things they left open, and pins the contracts the build agents work against.

**What this feature is, architecturally:** the app's first and only screen, built from an empty `ContentView`. `passenger-code/` has no app code — this TRD establishes the module layout every later PRD extends. `passenger-brain/database/migrations/` is empty — this TRD writes `001`.

**Six open calls resolved here** (design spec §8 items 1–5, plus the two carry-forwards `product` handed to `chief-of-staff` at the `design-approval` PASS):

| # | Open item | Call | Where |
|---|---|---|---|
| 1 | Hood tap hit-testing | `MapReader` + projected-plane ray casting behind a pure, testable seam. No `UIViewRepresentable` fallback. | §4.3 |
| 2 | `selectedHour` seam for T-032 | Offset index `0...12` on `DensityStore`; storage keys on **absolute UTC hour**, not offset | §4.4, §3 |
| 3 | Bundled vs. fetched Hood polygons (drives <3s cold open) | **Bundled.** Supabase is the authoring source; the client never fetches geometry at launch | §2.2, §8 D3 |
| 4 | Permission-prompt delay | Event-driven off the title's fade completion + 200ms (≈3.4s under standard motion), never a raw launch timer | §5.2 |
| 5 | Dark-mode Settings-hint link contrast | Semantic asset-catalog color set + underline + a contrast unit test. No mockup hex. | §8 D1 |
| 6 | Near-me in the "not asked" state | Marker is bound to authorization status, never to a tap. The mockup's unconditional marker is a mockup bug. | §8 D2 |

Band count and thresholds stay a `data-engineer` call (PRD Technical design). This TRD makes the client indifferent to it: the client reads an integer band and never computes a threshold.

---

## 2. Architecture

### 2.1 Module layout (new, `passenger-code/Passenger/`)

```
Passenger/
  PassengerApp.swift          entry point — hosts MapScreen
  Map/
    MapScreen.swift           the single screen; owns camera + composition
    HoodLayer.swift           MapPolygon content builder (fill + name label)
    ColdOpenTitle.swift       "Tel Aviv, right now" state machine
    NearMeButton.swift        recenter control + disabled state
    SettingsHint.swift        denied-state inline copy
    CachedDataIndicator.swift offline pill
  Hoods/
    Hood.swift                value type — slug, name, projected ring, bbox, centroid
    HoodCatalog.swift         bundled-resource load + id lookup
    HoodHitTester.swift       pure geometry: point → Hood?, with 44pt tolerance
  Density/
    HeatBand.swift            enum quiet/moderate/busy — no "none" case
    DensitySnapshot.swift     immutable [hoodID: [absoluteHour: HeatBand]]
    DensityStore.swift        @MainActor @Observable — the selectedHour seam
    DensityAPI.swift          URLSession + PostgREST, no SDK
    DensityCache.swift        last-good snapshot on disk
  Location/
    LocationStore.swift       authorization status only — no coordinates
    PermissionPrompt.swift    scheduling + non-overlap constraint
  Support/
    HeatPalette.swift         band → opacity. One table, no zoom parameter.
    ContrastRatio.swift       salvaged (SALVAGE.md REUSE)
    AppConfig.swift           SupabaseConfig.plist reader
Resources/
  hoods-tel-aviv.json         build-time export of the hoods table
```

Xcode synchronized file groups are on — adding a file to the folder is enough, no `project.pbxproj` edit (`passenger-code/README.md`).

### 2.2 Boundaries — who is allowed to know what

- **`Hoods/` knows no network and no density.** It loads a bundled file and answers "which Hood is at this point." Pure enough to unit-test without a map, a simulator, or a server.
- **`Density/` knows no geometry.** It maps a Hood *id* to a band for an hour. It never sees a polygon, a coordinate, or a camera.
- **`Map/` is the only layer that knows both**, and it is the only layer that knows SwiftUI. It composes: `HoodCatalog.hoods` × `DensityStore.band(for:hour:)` → `MapPolygon` + `foregroundStyle`.
- **`Location/` knows only an authorization enum.** It never handles a `CLLocation`. See §3.3 — this is a privacy decision, not an accident.

The cross product of those four boxes is the whole feature. Nothing in this feature writes to the backend, so there is no write path, no identity, and no auth to design.

### 2.3 Third-party dependencies: none added

| Candidate | Call |
|---|---|
| **MapKit** vs. Mapbox / MapLibre | **MapKit.** It is the strategy's stack, it is free, it needs no account, and `MapPolygon` + a fixed `foregroundStyle` is precisely the "stepped bands, never a gradient" primitive decision #17 requires. Mapbox buys vector-style control this feature does not need and costs money + an account — Aviran-gated, and rejected before it gets there. |
| **`supabase-swift` SPM package** vs. `URLSession` | **`URLSession`.** V1 needs one unauthenticated GET against a public-read table. No auth, no Realtime (PRD: "No Realtime in V1"), no Storage. A ~60-line PostgREST client is smaller than the SDK's transitive graph and keeps Swift 6 strict concurrency trivially clean. Revisit when auth or Realtime lands — both are parked. |
| PostGIS | **Not enabled.** No server-side spatial query exists in V1; hit-testing is client-side. Geometry stores as `jsonb`. Enabling PostGIS later is additive. |

This satisfies `passenger-code/README.md`'s "no third-party packages until a TRD justifies one" — this TRD justifies none.

---

## 3. Data model

### 3.1 Backend — migration `001`

```sql
create table public.hoods (
  id          text primary key,             -- stable slug, e.g. 'florentin'
  name        text not null,
  city        text not null default 'tel-aviv',
  polygon     jsonb not null,               -- GeoJSON Polygon, WGS84, single ring
  updated_at  timestamptz not null default now()
);

create table public.hood_density (
  hood_id     text        not null references public.hoods(id) on delete cascade,
  hour_bucket timestamptz not null check (hour_bucket = date_trunc('hour', hour_bucket)),
  band        smallint    not null check (band between 1 and 3),
  primary key (hood_id, hour_bucket)
);
create index hood_density_hour_idx on public.hood_density (hour_bucket);
```

RLS: enabled on both. One `select` policy each, `to anon, authenticated using (true)`. **No insert/update/delete policy is written at all** — absence of a policy is the denial, and there is no client write path to authorize. The synthetic generator writes with the service role, out of band.

Three decisions inside that schema:

- **`hour_bucket` is an absolute UTC timestamp, not an offset and not an hour-of-day.** This resolves the PRD's open key-shape question and T-032 §8 item 4. Offsets rot the moment the clock crosses an hour; hour-of-day cannot express "tomorrow 01:00," which the +12h window reaches every evening. Absolute keying is also what makes the offline path in §3.4 correct rather than approximately correct.
- **No `band = 0`.** "No data" is the *absence of a row*, not a band value. The client type is `HeatBand?`, so the compiler carries the distinction the map has to render silently (PRD req 7).
- **Band is stored, not computed client-side.** Thresholds stay entirely server-side, so `data-engineer` can retune them without an app release. If a raw score is later wanted for the pipeline's own use, it is an additive column that does not touch the client contract.

### 3.2 Client — bundled Hood geometry

`Resources/hoods-tel-aviv.json` is a **build-time export of the `hoods` table**, committed to `passenger-code/`:

```json
{ "schemaVersion": 1, "generatedAt": "2026-07-30T00:00:00Z", "city": "tel-aviv",
  "hoods": [ { "id": "florentin", "name": "Florentin",
               "polygon": [[34.7661, 32.0553], [34.7690, 32.0561], ...] } ] }
```

At load, each ring is projected once into `[MKMapPoint]` and a bounding `MKMapRect` is precomputed. `Hood` is a `Sendable` value type; the catalog is immutable after load.

Dozens of polygons for one city (decision #12's bound), changing rarely (the PRD's own labelled assumption). Decoding a bundled file is bounded, offline-safe, and unaffected by a cold cellular connection — which is why this is the call that makes §7's cold-open budget achievable. The `hoods` table still ships in `001`: it is the authoring surface the export comes from and the FK target `hood_density` needs. **[ASSUMPTION]** curation is not continuous; if it becomes so, a refresh path is additive (fetch, compare `schemaVersion`, replace the catalog) and does not change any contract below.

### 3.3 Location data — minimized by construction

The app never holds a user coordinate:

- Recenter uses `MapCameraPosition.userLocation(fallback: .region(telAvivCityWide))` — MapKit reads the location, the app does not.
- The "you are here" marker is `UserAnnotation()` — again MapKit's, not ours.
- `LocationStore` wraps `CLLocationManager` for **`authorizationStatus` and `requestWhenInUseAuthorization()` only**. No `startUpdatingLocation`, no `didUpdateLocations` handling, no stored `CLLocation`, nothing persisted.
- **The density request carries no location, no device id, and no user id** — it is byte-identical for every user of the app (§4.5). Location cannot leak through a query that never had a place to put it.

Nothing to log means nothing to leak (`passenger-code/CLAUDE.md`, Safety). `NSLocationWhenInUseUsageDescription` states exactly this and nothing more, per the design spec's F8 fix: *"Passenger uses your location to center the map on you and show a 'you are here' marker."*

### 3.4 Cached density

Last successful snapshot is written to Application Support as JSON (a payload, not a preference — not `UserDefaults`). It contains Hood-level synthetic bands and no personal data. Because rows key on absolute hour, a cache read at a later clock time stays correct: rows still inside `[now, now+12h]` render; rows that fell out of the window are simply absent, and an absent row is already the silent no-data state. No staleness heuristic is needed — the key does the work.

---

## 4. Contracts

Both build surfaces work against this section. `ios-developer` and `developer` do not need each other's code, only §4.5 and §3.1.

### 4.1 Heat band and palette

```swift
enum HeatBand: Int, Sendable, CaseIterable, Codable {
    case quiet = 1, moderate = 2, busy = 3
}

enum HeatPalette {
    /// The single band→opacity table. There is no zoom parameter, by design (PRD req 4).
    static func opacity(for band: HeatBand) -> Double
    /// One hue, light/dark asset variants. Steps differ by opacity, never by hue.
    static var hue: Color { Color("HeatFill") }
}
```

`opacity(for:)` takes one argument and returns from a `switch`. Any future signature carrying a zoom, camera, or altitude term is a PRD req-4 violation — `ios-code-reviewer` should treat an added parameter as a blocking finding. No `blur`, `.shadow`, `saturation`, or material is applied to the fill anywhere. Illustrative defaults from the approved mockup: quiet 0.16, moderate 0.38, busy 0.62.

### 4.2 Hood catalog

```swift
struct Hood: Identifiable, Sendable, Hashable {
    let id: String                     // stable slug
    let name: String
    let ring: [MKMapPoint]             // projected once at decode
    let boundingRect: MKMapRect
    let centroid: CLLocationCoordinate2D
    var coordinates: [CLLocationCoordinate2D] { get }   // for MapPolygon
}

enum HoodCatalog {
    static func load() throws -> [Hood]   // bundled resource; throws on malformed input
}
```

`load()` throws rather than returning `[]` — a corrupt bundled resource is a build defect, not a runtime empty state (`passenger-code/CLAUDE.md`, fail fast). Called off the main actor; the map renders before it resolves.

### 4.3 Hit-testing — design spec §8 item 1, resolved

```swift
struct HoodHitTester: Sendable {
    init(hoods: [Hood])
    /// - Parameter tolerance: map-point distance equivalent to 22pt at the current camera.
    func hood(at point: MKMapPoint, tolerance: Double) -> Hood?
}
```

Two-pass, in a projected plane (`MKMapPoint`), never in raw degrees — ray casting on lat/long degrees distorts with longitude and would misresolve thin north–south Hoods:

1. Bounding-rect prefilter, then even-odd ray casting against the containing candidates. Polygons do not overlap (PRD req 3), so at most one hit.
2. On a miss, the nearest Hood whose edge lies within `tolerance` wins. This is how the 44pt minimum (design §4) is met without dilating the drawn shape — the *hit area* extends past the boundary, the *fill* does not.

`MapReader` supplies the screen→coordinate conversion; the geometry above is pure and takes no MapKit view type. If MapKit's SwiftUI conversion proves imprecise on device, the fix is swapping the host in `MapScreen.swift` — `HoodHitTester` is untouched. That is why this TRD does not pre-build an `MKPolygonRenderer`/`UIViewRepresentable` fallback: the risk is isolated behind one seam, and building the fallback speculatively costs a `UIViewRepresentable` in the app's first screen for a problem that may not exist. Unit tests must cover a point inside, a point outside, a point in the bbox but outside the ring, a concave notch, and a within-tolerance near-miss.

### 4.4 Density store — the T-032 seam

```swift
@MainActor @Observable
final class DensityStore {
    /// UTC hour floor captured when the current snapshot was fetched.
    private(set) var anchorHour: Date
    /// 0...12 offset from anchorHour. T-032's slider is the only writer. Never persisted.
    var selectedHour: Int
    private(set) var source: Source        // .live, .cache, .unavailable

    func band(for hoodID: String, hour: Int) -> HeatBand?   // nil == no data
    func load() async
    func refreshIfHourRolled() async       // called on scenePhase → .active
}
```

- `selectedHour` is a plain `Int` on an `@Observable` class — T-032 §8 item 2 asked for the binding shape confirmed before either side builds. **Confirmed: a plain observable `Int`, no wrapper type, no publisher.** `Slider(value:in:step:)` binds to it through a `Double` bridge in T-032's own view.
- `band(for:hour:)` is a dictionary read against already-fetched data. **No code path fetches on an hour change** — that is what makes T-032's 400ms repaint budget real, and it is a contract, not an optimization.
- The store is session-scoped and in-memory. `selectedHour` is never written to `UserDefaults`/`AppStorage` (T-032's cold-launch requirement).
- `refreshIfHourRolled()`: on foreground, if `date_trunc('hour', now)` no longer equals `anchorHour`, re-fetch and remap `selectedHour` so the *absolute* hour the user chose is preserved where it is still inside `[now, now+12]`, clamped to `0` otherwise. This closes the foreground-across-an-hour-boundary gap T-032 flagged. Cold launch always starts at `selectedHour == 0`.

### 4.5 Density API

```
GET {supabase_url}/rest/v1/hood_density
    ?select=hood_id,hour_bucket,band
    &hour_bucket=gte.{anchorHour ISO8601 UTC}
    &hour_bucket=lte.{anchorHour + 12h ISO8601 UTC}
Headers: apikey: <anon>, Authorization: Bearer <anon>, Accept: application/json
```

Once per session. No pagination (dozens of Hoods × 13 buckets). No query parameter carries anything user-specific — §3.3. Response rows are validated at the boundary: an unknown `band` integer or an unparseable timestamp drops that row, it does not fail the whole snapshot and it does not crash (`passenger-code/CLAUDE.md`, boundary validation).

Config from `SupabaseConfig.plist` (gitignored, per `passenger-code/CLAUDE.md`). **A missing plist is a valid state**: `DensityAPI` reports unavailable, the map renders with no fill, and the app builds and runs for a developer with no credentials.

### 4.6 Location

```swift
@MainActor @Observable
final class LocationStore {
    private(set) var authorizationStatus: CLAuthorizationStatus
    func requestWhenInUseIfNeeded()   // no-op unless .notDetermined
}
```

`requestWhenInUseIfNeeded()` is idempotent and guarded on `.notDetermined`, so a denied user is never re-prompted in the install (PRD req 6) and a double call cannot double-prompt.

---

## 5. Flow

### 5.1 Cold open

```
launch → PassengerApp → MapScreen.body
  ├─ Map(position: .region(telAvivCityWide))            renders immediately, interactive
  ├─ .task  HoodCatalog.load() off-main → hoods         polygons appear, unfilled
  ├─ .task  DensityStore.load()                         fill paints when it resolves
  └─ ColdOpenTitle: .hidden → .visible(120ms) → .fadingOut(2200ms) → .done(~3200ms)
                                                        └→ PermissionPrompt after +200ms
```

Nothing on that path `await`s before the first frame. The map is pannable, zoomable, and tappable from frame one, before geometry, before density, before permission — PRD req 1.

**Hood tap:** `MapReader` → coordinate → `MKMapPoint` → `HoodHitTester.hood(at:tolerance:)` → open sheet with that `Hood`. One tap, no preview step (PRD req 3). T-031 ships the stub destination; T-033 owns its contents.

**Hour change (T-032, wired but unexercised here):** `selectedHour` write → `@Observable` invalidation → `HoodLayer` recomputes `foregroundStyle` per polygon. Camera, geometry, sheet state, and the polygon identities are all untouched — only the style closure re-evaluates.

### 5.2 Permission prompt — design spec §8 item 4, resolved

**The trigger is an event, not a timer from launch.** `ColdOpenTitle` publishes a `.done` transition when its fade-out completes; `PermissionPrompt` fires 200ms after that, and only while `scenePhase == .active`.

- Under standard motion this lands at **≈3.4s after the map's first frame** (title opaque ~1.12s, fully invisible ~3.2s, +200ms) — the number the approved mockup demonstrates.
- Under Reduce Motion the fade is near-instant, so `.done` arrives earlier and the prompt follows it. The non-overlap constraint — the locked half of §8 item 4 — holds automatically, because the constraint is expressed in the control flow rather than re-asserted in a second hardcoded constant that can drift from the first. The mockup needed the same number in three call sites and once had them out of sync; this shape makes that class of bug unrepresentable.
- If the app is backgrounded during the window, the prompt is deferred to the next `.active`, never fired at a user who cannot see it.
- Tapping near-me while `.notDetermined` **cancels the pending scheduled prompt and requests immediately** — one prompt, ever, from either path.

### 5.3 States

Per design spec §3, with the mechanism named for each:

| State | Mechanism |
|---|---|
| Loading | No spinner, no gate. Fill is simply absent until `DensityStore.load()` resolves. |
| Empty (Hood has no row) | `band(for:hour:) == nil` → no `foregroundStyle` fill applied. No text anywhere on the map (PRD req 7). |
| Error / feed unreachable | Identical rendering to Empty. `source == .unavailable`. No banner, no retry control. |
| Offline with cache | `source == .cache` → `CachedDataIndicator` in the top corner, non-blocking, subordinate to the map. |
| Permission denied | Near-me disabled; on tap, `SettingsHint` (§8 D1). Zero effect on Hoods or heat — neither ever depended on location. |
| Outside Tel Aviv | No mechanism. No Hood polygons exist outside the city, so nothing renders and nothing is checked. `MunicipalBoundary.swift` is **not** salvaged — a boundary test would be code whose only job is to produce the behaviour that already happens. |

---

## 6. Salvage

Per `SALVAGE.md`, read line by line and adapted to Swift 6 before landing — leaf code only:

- `Support/ContrastRatio.swift` (REUSE) — becomes the test harness for §8 D1's contrast assertion.
- `Models/DensityContract.swift` (REUSE, "the single best file in the old codebase") — read for the never-one-blended-score type discipline; `HeatBand` is that idea, reduced.
- `Features/Map/DensityMark.swift`, `DensityPlaceMark.swift` (REUSE) — mark rendering, adapted to `MapPolygon`.
- `Features/Map/MapScreen.swift` (REFERENCE, 940 lines) — mine camera handling only. **Do not copy its structure.**
- `06-database/gen_heat.py` + `tel-aviv-places-heat.json` — the synthetic generator, for step B3.

---

## 7. Cold-open performance — design spec §8 item 5, resolved

Oldest device supporting the app's iOS 26 minimum: **iPhone 11 / iPhone SE (2nd gen), A13** **[ASSUMPTION]** — `ios-developer` verifies against Apple's iOS 26 device list before measuring.

"Interactive map" = first frame in which `Map` accepts a pan gesture. Budget against the PRD's 3s:

| Segment | Budget | How it is held |
|---|---|---|
| Process launch → first SwiftUI frame | ≤1.5s | No third-party packages (§2.3). No network client constructed before first frame. |
| `Map` first render | ≤0.5s | Static `MapCameraPosition.region`, no async seed. |
| Hood decode + projection | ≤0.2s, **off the interactivity path** | Bundled file (§3.2), decoded off-main; polygons attach after. |
| Density fetch | unbounded, **off the interactivity path** | Async, never awaited before first frame. |

Total to interactive: ≤2.0s, with the two unbounded items structurally excluded. **The bundled-geometry decision is what buys the margin** — a launch-time network fetch for polygons would put an unbounded cellular round trip inside the 3s, which is the specific failure the design flagged and could not resolve.

Verification is required, not assumed: an `XCTApplicationLaunchMetric` performance test on a physical A13 device, cold, airplane mode on and off. Numbers go in the build report. `qa` re-runs it before acceptance.

---

## 8. Decisions carried in from the `design-approval` PASS

### D1 — Settings-hint link contrast (`product`'s carry-forward 1)

The mockup's `--focus` `#1E66E0` measures 5.21:1 on the light surface and **3.28:1 on dark `#1A1C1F`** — a real WCAG AA failure against the 4.5:1 bar the design spec's own §4 and §7 claim for this element. **The mockup hex binds nothing here.** Build:

- A semantic asset-catalog color set **`LinkOnSurface`** with light and dark variants — the pattern `design-principles.md` §5 already prescribes ("each with light+dark variants"), not a literal from a mockup. Light `#1E66E0` (5.21:1, verified by `product`). Dark **`#6EA8FF`** — computed 7.08:1 against `#1A1C1F` by WCAG relative luminance; `ios-developer` recomputes against the app's actual dark surface token rather than inheriting this number on trust.
- **The "Settings" run is underlined as well as coloured**, so the affordance survives never-color-alone (`design-principles.md` §3) and does not depend on the token being right.
- **The hint renders on an opaque surface-token background, not directly over the map.** A contrast ratio against a map is not a number anyone can verify — this applies equally to `ColdOpenTitle`, whose §4 claim of "4.5:1 against the map background" is otherwise unmeasurable. Not `.ultraThinMaterial`: its effective luminance varies with whatever the map draws underneath, which reintroduces the same unverifiability.
- **A unit test asserts ≥4.5:1 in both appearances**, using the salvaged `ContrastRatio.swift`. A contrast claim that is not executable is a claim that regresses silently — this is the second time this exact defect has appeared in this feature's artifacts.
- Tapping the run opens `UIApplication.openSettingsURLString` (design §4 calls it a deep link). It never re-invokes the system dialog, which iOS would ignore anyway.

### D2 — Near-me in the "not asked" state (`product`'s carry-forward 2)

The mockup adds the you-are-here marker unconditionally on a near-me tap while `.notDetermined` (mockup L530-532). The real app cannot do that. Build it as:

```
near-me tapped:
  .notDetermined            → cancel pending scheduled prompt; requestWhenInUseIfNeeded()
                              → recenter and show the marker only after the callback returns authorized
  .authorizedWhenInUse/.always → recenter
  .denied / .restricted     → present SettingsHint. Never request.
```

`UserAnnotation()` is included in the map content **only** when `LocationStore.authorizationStatus` is authorized — its presence is bound to the status, never to a tap. This also closes `product`'s first-verdict minor about near-me having undefined behaviour in the not-asked state.

### D3 — Bundled geometry, Supabase-authored

`Resources/hoods-tel-aviv.json` is generated from the `hoods` table and committed. The two must not drift: whoever changes `hoods` re-exports in the same change. `schemaVersion` exists so a future fetch-and-refresh path can be added without a contract change. The client does not verify against the server in V1 — a version check needs a network call on the launch path, which is the thing §7 exists to prevent.

### D4 — Not relitigated

Stepped bands, no gradients, uniform opacity at every zoom, no on-map "no data" text, and the `selectedHour` seam are normative in the PRD and design spec, and T-032/T-033 already build against them. This TRD implements them (§4.1, §4.4, §5.3) and does not reopen them.

---

## 9. Rollout & migration

- **No feature flag.** This is the app's only screen; there is no prior version to gate against and no A/B surface. A flag here would be a toggle whose off-state is a blank window.
- **Migration `001` applying is Aviran-gated** (he holds the credentials — `database/README.md`, `BOARD.md`). `developer` writes it and hands it off; it is not applied by any agent.
- **The client ships independently of the backend.** Bundled geometry plus a silent-empty density state means the iOS build is testable and demoable before `001` is applied or a single density row exists. This is the deliberate benefit of the §4.5 contract: the two build tracks do not block each other.
- **Backward compatibility:** none required. First release, empty schema, empty app.

---

## 10. Risks & alternatives

| Risk | Mitigation / decision |
|---|---|
| `MapReader`'s screen→coordinate conversion is imprecise on small or thin Hoods | The 22pt tolerance pass (§4.3) absorbs ordinary imprecision. If it does not, the geometry seam is pure and the host swaps in one file. Measured on device before `qa`, not assumed. |
| SwiftUI `Map` re-renders every polygon on an hour change, blowing the 400ms budget | Polygons are keyed by stable `Hood.id`; only `foregroundStyle` re-evaluates. Dozens of shapes, not thousands (decision #12's bound). If it misses, the fallback is caching resolved `ShapeStyle`s per band — a local change, not an architectural one. |
| Bundled geometry drifts from the `hoods` table | D3's same-change re-export rule, plus `schemaVersion`. Accepted cost of the §7 margin; the alternative fails the 3s target outright. |
| Density thresholds unresolved (`data-engineer`'s call) | Client is indifferent by construction — it reads an integer band. Thresholds can change server-side after ship with no client release. |
| Synthetic feed makes "right now" simulated | Named in the PRD and strategy; out of this TRD's scope. The contract is identical when a live source replaces the generator — same table, same key, same band. |
| App Store review on `NSLocationWhenInUseUsageDescription` | The purpose string is accurate to what V1 does and no more (§3.3). Normalise its straight/curly quotes when the copy is locked (`product`'s nit 3). |

**Alternatives considered and rejected:** Mapbox/MapLibre (§2.3 — cost, account, capability not needed); `supabase-swift` (§2.3 — dependency weight for one GET); PostGIS + server-side point-in-polygon (network round trip per tap, defeats the whole interaction); a `UIViewRepresentable` + `MKPolygonRenderer` map built up front (§4.3 — pre-paying for a risk that is already isolated); persisting `selectedHour` across launches (contradicts T-032's cold-launch requirement); a boundary-polygon check for the outside-Tel-Aviv state (§5.3 — code to cause behaviour that already happens).

---

## 11. Build breakdown

Ordered. Tags name the agent(s) each step dispatches to.

**Backend track — independent of the iOS track after step A0.**

| # | Step | Tag |
|---|---|---|
| A1 | Migration `001`: `hoods` + `hood_density` per §3.1, with both check constraints and the FK | **[Backend]** |
| A2 | RLS: enable on both, one public `select` policy each, no write policy | **[Backend]** |
| A3 | Seed `hoods` with the Tel Aviv polygon set (salvage `022_create_neighborhoods` / `024a_seed_neighborhoods_placeholder` as reference) | **[Backend]** + **[Algo/Data]** |
| B1 | Band count and thresholds — the PRD's open `data-engineer` call. Does not block the client. | **[Algo/Data]** |
| B2 | Synthetic density generator writing 13 rolling absolute-hour buckets per Hood (salvage `gen_heat.py`) | **[Algo/Data]** |
| B3 | Export `hoods-tel-aviv.json` from the seeded table, hand to the iOS track (D3) | **[Algo/Data]** + **[iOS]** |

**iOS track.**

| # | Step | Tag |
|---|---|---|
| C1 | `Hood`, `HoodCatalog`, `HoodHitTester` + geometry unit tests (§4.2, §4.3). Buildable before any backend exists — use a hand-authored fixture until B3 lands. | **[iOS]** |
| C2 | `HeatBand`, `HeatPalette`, `DensitySnapshot` (§4.1) | **[iOS]** |
| C3 | `MapScreen` + `HoodLayer`: city-wide camera, polygons, band fill, zoom-gated name label, tap → stub sheet (§5.1) | **[iOS]** |
| C4 | `ColdOpenTitle` state machine on a surface-token background (§5.1, D1) | **[iOS]** |
| C5 | `LocationStore` + `PermissionPrompt` event-driven scheduling (§4.6, §5.2) | **[iOS]** |
| C6 | `NearMeButton` with the full authorization switch, `UserAnnotation` bound to status (D2) | **[iOS]** |
| C7 | `SettingsHint` + `LinkOnSurface` asset color set + the contrast unit test (D1) | **[iOS]** |
| C8 | `AppConfig` + `DensityAPI` + `DensityStore` against the §4.5 contract, boundary-validated | **[iOS]** |
| C9 | `DensityCache` + `CachedDataIndicator`; `refreshIfHourRolled()` on `scenePhase` (§3.4, §4.4) | **[iOS]** |
| C10 | VoiceOver labels per Hood, always stating density in speech including "no data right now" (design §4) | **[iOS]** |
| C11 | Launch performance test on a physical A13 device; numbers in the build report (§7) | **[iOS]** |

**`trd-review` sign-off needed from:** `ios-developer` + `ios-code-reviewer` (C1–C11, the bulk), `developer` + `code-reviewer` (A1–A3), `data-engineer` + `code-reviewer` (B1–B3).
