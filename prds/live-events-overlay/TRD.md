# Live Events Overlay (client UI) — TRD

**Task:** T-034 · **Linear:** `PAS-25` · **Status:** v1 — ready for `trd-review`
**Owner:** architect · **Date:** 2026-08-02
**PRD:** [`live-events-overlay.md`](./live-events-overlay.md) (Draft v2)
**Design reference:** none. The pre-code design gate was retired 2026-08-02 and no spec had been drafted for this feature at retirement time (`BOARD.md`), so this TRD is written from the PRD plus the two locked rendering docs it cites (`design/map-rendering-spec.md`, `design/ux-flows.md`). Every UX call this document had to make itself is tagged **[ASSUMPTION]** and named in §8.
**Builds on:** [`map-hoods-heat/TRD.md`](../map-hoods-heat/TRD.md) (T-031, shipped/accepted) · [`hood-place-detail/TRD.md`](../hood-place-detail/TRD.md) (T-033, accepted) · [`time-slider/TRD.md`](../time-slider/TRD.md) (T-032, v2 at `trd-review`)
**Server contract consumed:** [`live-events-pipeline/TRD.md`](../live-events-pipeline/TRD.md) §4.2 (T-043, Build Phase 3, `build`-ready)

---

## 1. Context

Read the PRD first. Nothing here restates it. This document decides what it leaves open, closes the fixture gap the PRD itself named as unowned, and pins the contracts `ios-developer` builds against.

**Surface: iOS-only. Confirmed against shipped code and against T-043's TRD, not assumed.** Checked three ways:

- **No new backend artifact is needed.** Everything the client reads is already pinned in `live-events-pipeline/TRD.md` §4.2's `events_public` view — `id, name, start_at, end_at, lat, lng, venue_name, hood_id, category, rank, source_name`. That TRD passed `trd-review` unanimously (4/4) and is `build`-ready. No new table, column, view, RPC, index or RLS policy falls out of anything below.
- **Build Phase 1 makes no request at all.** A bundled fake event set drives reqs 1–4 and 6; req 5's empty case is a state to verify, not the only state (PRD Dependencies).
- **The one contract edit is a query-string amendment with no server-side change** (§4.2, D1). It drops a filter the client sends; the view already enforces everything that filter was doing on the safety side.

**§11 therefore contains no `[Backend]` and no `[Algo/Data]` step.** `trd-review` sign-off routes to **`ios-developer` + `ios-code-reviewer`**, plus one targeted confirmation from **`data-engineer`** on §4.2's amendment — it adds no build step and no SQL, but it edits a request shape T-043's TRD documented, and that belongs acknowledged now rather than discovered in Phase 3.

**What this feature is, architecturally.** A third map layer that owns no data logic. It fetches (later), filters by hour, sorts by a number the server computed, truncates, and draws. The parts with consequences are the three seams it touches in already-accepted code: `MapScreen`'s tap resolution, `DetailRouter`'s destination set, and T-032's heat modal.

**Open items resolved here:**

| # | Open item | Source | Call | Where |
|---|---|---|---|---|
| 1 | Is an event bound to its **start** hour or to every hour it **spans**? | PRD req 1 bullet 1 vs. req 5 bullet 2 | **Overlap.** An event renders at every hour bucket its `[start_at, end_at)` interval intersects. Start-hour-only would hide a running concert from "now" | §4.3, **D1** |
| 2 | Refresh cadence | PRD Open technical questions | **No timer.** Once per session + on `scenePhase → .active`, piggybacking T-031's existing hook. Staleness is a render-time predicate, not a fetch | §4.6, **D11** |
| 3 | Is `rank` absolute or per-hour? | PRD Open technical questions | **Already answered by T-043** — absolute, time-invariant, `[0,1]`. Closed; the client sorts and does nothing else | §4.4 |
| 4 | The on-screen marker cap | PRD Open technical questions / req 3 bullet 3 | **12**, one constant, one call site, **[ASSUMPTION]** with a stated derivation | §4.4, **D3** |
| 5 | Do event markers cluster? | PRD req 2 bullet 2 | **Not in this task.** Clustering is `T-041`'s, unbuilt and unowned. The cap is Phase 1's density bound. **Req 2's second bullet is not verifiable here and this TRD does not pretend otherwise** | §9, **D4** |
| 6 | At what zoom do event markers render? | not raised by any doc — found by reading `MapScreen` | **Every zoom**, unlike place pins. A deliberate, stated divergence from `map-rendering-spec.md` §2's pin row, made safe by the cap | §4.5, **D2** |
| 7 | Where does the event detail sheet live? | PRD req 4 | **A third depth-1 destination on the shipped `DetailRouter`**, mutually exclusive with Hood and Place. Not a second `.sheet` | §4.7, **D6** |
| 8 | Nothing renders in Build Phase 1 without a fixture | PRD Dependencies (named as unowned) / `BOARD.md` T-034 row | **A bundled fake event set ships in this task**, with an authoring rule strong enough that the tests below cannot pass vacuously | §3.4, **D10** |
| 9 | A tap on an event marker is also claimed by the map's own tap gesture | not raised by any doc — found by reading `MapScreen.swift:113-122` | **`EventHitTester` + event-first precedence in `handleTap`**, mirroring the shipped `PlaceLayer` pattern. Without it the Hood sheet wins the race | §4.5, **D7** |

---

## 2. Architecture

### 2.1 Module layout — additions to the shipped tree

```
Passenger/
  Events/
    LiveEvent.swift          new — the model. One struct, value type, Sendable
    EventsAPI.swift          new — PostgREST GET; built, inert until Phase 3 (§4.2)
    EventSeed.swift          new — bundled fixture → [LiveEvent] (§3.4)
    EventStore.swift         new — @Observable: load, source, events, layer visibility
    EventSelection.swift     new — PURE: hour overlap + stale drop + sort + cap (§4.4)
    EventHitTester.swift     new — PURE: mirrors the shipped PlaceHitTester (§4.5)
    EventDetailRows.swift    new — PURE: which rows the sheet renders (§4.7)
  Map/
    EventLayer.swift         new — one marker; mirrors PlaceLayer exactly
    MapScreen.swift          MODIFIED — third layer, tap precedence, one .task (§4.5)
  Detail/
    EventDetailModal.swift   new — the sheet
    DetailRouter.swift       MODIFIED — a third depth-1 destination (§4.7)
  HeatModal/
    EventsLayerToggle.swift  new — the row that lands in T-032's HeatModalCard (§4.8)
    HeatModalCard.swift      MODIFIED (T-032's file) — hosts that one row
  Support/
    BuildPhase.swift         MODIFIED — a second constant (§7, D9)
Resources/
  events-tel-aviv-seed.json  new — Build Phase 1 fake data (§3.4)
Assets.xcassets/
  EventMarker                new colour set (§4.5)
```

Xcode synchronized file groups are on — dropping files in the folder is enough, no `project.pbxproj` edit.

### 2.2 Boundaries — who is allowed to know what

- **`Events/` knows no map and no geometry.** It holds a list, filters it, and sorts it. `EventSelection`, `EventHitTester` and `EventDetailRows` are pure functions with injected `now` — the three places this feature can actually be wrong are the three that unit-test with no simulator, no network and no camera.
- **`Events/` knows nothing about the user.** No `LocationStore` import, no device identifier, no request parameter that could carry one. This is checkable by grep and §9 makes it a check (req 3 bullet 4).
- **`Events/` stores no hour.** It is handed `anchorHour` and `selectedHour` by the caller. T-032 §4.3's invariant — exactly one storage location for the hour in the entire app — extends to this task unchanged (**D12**).
- **`Map/` remains the only layer that composes.** `EventLayer` draws what it is handed, exactly as `PlaceLayer` does; `MapScreen` is the only file that knows all three layers exist and what order they draw in.
- **The client derives no ranking.** `rank` is read for exactly one purpose — a sort key — and nowhere else (§4.4, a blocking review finding if violated).

### 2.3 Where the layer sits

`MapScreen`'s `Map` content, draw order:

| Order | Content | Note |
|---|---|---|
| 1 | `HoodLayer` polygons + centroid annotations | Unchanged. Heat owns fill and the area channel, always. |
| 2 | `PlaceLayer` pins | Unchanged, still gated on `showsNames`. |
| 3 | **`EventLayer` markers** | **New. Not gated on zoom** (D2). Drawn after place pins, so an event marker sitting on a place pin is the one the eye and the finger reach. |
| 4 | `UserAnnotation` | Unchanged. |

`EventLayer`'s body contains **`Annotation` only** — no `MapPolygon`, no `foregroundStyle` over an area, no stroke on a Hood boundary. That is req 2's first bullet made structural rather than promised: the layer has no way to occupy the area channel because it never emits area content. `ios-code-reviewer` treats any `MapPolygon` or Hood-boundary stroke inside `Events/` or `EventLayer.swift` as a blocking finding.

---

## 3. Data model

### 3.1 `LiveEvent` — one struct, mirroring `events_public` exactly

```swift
struct LiveEvent: Identifiable, Equatable, Sendable {
    let id: String                  // uuid string from the server; stable across fetches
    let name: String
    let startAt: Date
    let endAt: Date
    let coordinate: CLLocationCoordinate2D
    let venueName: String?          // nil == not supplied; never "" (§4.1)
    let hoodID: String?
    let category: String?
    let rank: Double                // sort key only (§4.4)
    let sourceName: String?         // decoded, deliberately not rendered in V1 (D5 note)
}
```

Nullable-in-the-view columns are `Optional` here and `""`/whitespace normalises to `nil` at the boundary, the same rule `PlaceCatalog.normalizedBlurb` already applies to Hood blurbs. That is what makes req 4's "omitted, not shown as a blank row" a property of the data rather than a check every future row has to remember (§4.7).

`sourceName` is decoded but not displayed: T-043 §8 F4 leaves "must the sheet credit the source?" open as a per-source ToS question nobody has answered. Decoding it now means the answer is a view change, not a model change. **Flagged for `product`, not decided here.**

### 3.2 Nothing persists

`EventStore` is session-scoped and in memory. No `UserDefaults`, no `AppStorage`, no disk cache (D8). The layer-visibility toggle is likewise in-memory — PRD req 6 asks for persistence "across a modal close and reopen within the session," which is what a plain stored property on a `@State`-owned `@Observable` gives, with no persistence layer to build or reset.

### 3.3 Location and privacy

Nothing in this feature touches user location. Event coordinates are venue coordinates published by a third party; they are not personal data and are not derived from anyone's position. The request (Phase 3) carries no location, no device id and nothing user-specific — byte-identical for every device, the property T-031 §3.3 established and T-043 §4.2 preserves. No coordinate is logged. `Events/` imports `CoreLocation` for `CLLocationCoordinate2D` and must not import or reference `LocationStore`; §9 makes that a check, because req 3 bullet 4's "no per-user input" is only credible if the module has no way to obtain one.

### 3.4 Build Phase 1 — the bundled event set **[D10]**

**The gap, as the PRD and `BOARD.md` both state it:** with an empty feed only, reqs 1–4 and 6 have nothing to exercise. This TRD folds the fixture into this task's own build scope as a named step (C2), the same pattern T-033 shipped for places and T-032's TRD adopted for the density seed (its D10).

**Shape — relative offsets, not absolute timestamps**, for the reason T-032 §3.4 gives and which is sharper here: an events file of absolute timestamps is not merely stale after a day, it is *empty*, because every row fails the `end_at > now` filter. The seed is authored against the launch's own `anchorHour`.

```jsonc
// Resources/events-tel-aviv-seed.json
{
  "schemaVersion": 1,
  "events": [
    { "id": "seed-0001", "name": "Rooftop set, Levinsky",
      "start_offset_minutes": 120, "duration_minutes": 240,
      "lat": 32.0578, "lng": 34.7726,
      "venue_name": "A rooftop", "hood_id": "florentin",
      "category": "music", "rank": 0.91, "source_name": "Seeded fixture" }
  ]
}
```

`EventSeed.events(anchorHour:)` resolves `startAt = anchorHour + start_offset_minutes` and `endAt = startAt + duration_minutes`, so the fixture is correct at any launch on any date and flows through the identical `LiveEvent` values the live path produces — the seed exercises the real code, not a parallel one.

**Authoring rule, so the fixture can falsify something.** Every clause below is asserted by a test (C2), because a fixture that cannot fail a check is a fixture that makes §9 pass vacuously:

1. At least **6 distinct hour buckets** in `0…12` contain at least one event, so an hour change visibly changes the marker set.
2. At least **one bucket contains zero** events, so req 5's per-hour empty case is exercised on purpose rather than by accident.
3. At least one bucket contains **`markerCap + 2`** events with **distinct** ranks, so the truncation in §4.4 is exercised and the ordering is unambiguous.
4. At least one event **spans ≥3 buckets**, so D1's overlap rule is exercised rather than assumed.
5. At least one event has `venue_name: null` and one has `category: null`, so req 4's omit-don't-blank rule has a case.
6. At least one event has already **ended** at launch (negative `start_offset_minutes`, short duration), so req 5's stale rule is deterministically checkable.
7. Every coordinate falls inside a real polygon in the shipped `hoods-tel-aviv.json`, and every `hood_id` resolves.
8. **Event and venue names are plainly fictional.** A demo fixture must not assert that a real Tel Aviv business is hosting a real event tonight; that is a fabricated listing, not test data.
9. **Within any one hour bucket, no two events share a coordinate, and no event name is templated** — no stem-plus-index name (`Fixture event 1…14`, `Event A`), each name distinct and readable as a real event. Structural validity is not plausibility: the shipped seed's `+5` bucket held 14 events all named `Fixture event N` at one identical point, satisfied clauses 1–8, and still rendered as 12 stacked identical markers. **Clause 3's `markerCap + 2` bucket is where this bites** — the bucket that exists to exercise truncation is the same one a demo is most likely to be opened on, so its events need distinct coordinates and real-sounding names, not just distinct ranks.

*Clause 9 was added by `product` at T-034's acceptance, 2026-08-03 (PRD Technical design → Dependencies; Decisions-log row "D10 CONFIRMED — the fixture is T-034's, with a plausibility clause added"). It changes no requirement, schema, or contract. Fixing the already-shipped `+5` bucket to satisfy it is tracked at **T-051**, not here.*

**Flagged for `product` at `trd-review`:** the PRD names this fixture as a real, unowned data need. This TRD claims it for T-034 and gives it an authoring rule. `product` should confirm the claim and confirm that Phase-3 acceptance re-runs reqs 1–5 against the live feed with the constant flipped (§7) — Phase-1 acceptance covers them against the fixture only, and nothing here claims otherwise.

---

## 4. Contracts

All of §4 is `[iOS]`. There is no second build surface to hand a contract to.

### 4.1 The store

```swift
@MainActor @Observable
final class EventStore {
    enum Source: Sendable { case live, seed, unavailable }

    private(set) var source: Source = .unavailable
    private(set) var events: [LiveEvent] = []      // the whole fetched window, unfiltered
    /// PRD req 6. Session-scoped, in memory, default `true` — the layer ships on.
    var isLayerVisible: Bool = true

    init(api: any EventsFetching = EventsAPI(), seedResourceName: String = "events-tel-aviv-seed",
         bundle: Bundle = .main)

    func load(anchorHour: Date) async
    func refresh(anchorHour: Date) async
}
```

The `init` seam is protocol-plus-default-argument, identical to the shipped `DensityStore.init(api:cache:now:)` and `PlaceCatalog.init(api:cache:…)`. A malformed seed or a malformed row is dropped one row at a time and never fails the load — the boundary-validation rule `passenger-code/CLAUDE.md` states and `PlaceCatalog.apply(hoodRows:)` already implements.

### 4.2 The request (Phase 3, built and inert before then)

```
GET {supabase_url}/rest/v1/events_public
    ?select=id,name,start_at,end_at,lat,lng,venue_name,hood_id,category,rank,source_name
    &start_at=lt.{anchorHour + 13h, ISO8601 UTC}
    &order=rank.desc
Headers: apikey: <anon>, Authorization: Bearer <anon>
```

**Amendment to `live-events-pipeline/TRD.md` §4.2, and the only contract edit in this document: the `start_at=gte.{anchorHour}` lower bound is dropped.** It is a client-side filter that silently deletes the most valuable rows in the feature. An event that began at 18:00 and runs to 23:00 is exactly "what's happening" when a user opens the app at 20:00, and the lower bound excludes it from the payload entirely, at every hour — the overlap rule in D1 could then never fire for anything already in progress.

Dropping it is safe and costs the pipeline nothing, because the view is the boundary and already enforces the floor that matters: `events_public` filters `withdrawn_at is null and hood_id is not null and end_at > now() and rank >= event_rank_floor()`. The set the amended query returns is exactly "everything currently servable that starts before the window ends" — bounded above by the 13h clause, bounded below by the view's own expiry filter. No SQL, no view, no index and no RLS policy changes. **`data-engineer` to confirm at review** (§11).

**`data-engineer` confirmation, 2026-08-03 (T-034/PAS-25, dispatched as the one outstanding item from `product`'s acceptance pass):** confirmed correct as written, no amendment needed. The query's only job is to hand §4.3's per-bucket overlap predicate a candidate superset that omits nothing it could legitimately render; §4.3 does the actual overlap filtering client-side. Derivation: for an event to render at *any* bucket `k ∈ 0…12`, it must satisfy `startAt < bucketEnd(k)` and `endAt > bucketStart(k)` for that `k`. Taking the union over all 13 buckets, the necessary-and-sufficient superset condition collapses to exactly two bounds — `startAt < anchorHour + 13h` (from `k=12`'s `bucketEnd`) and `endAt > anchorHour` (from `k=0`'s `bucketStart`). The amended query supplies precisely this: the query's own `start_at=lt.{anchorHour+13h}` matches the upper bound term for term, and the view's standing `end_at > now()` matches the lower bound given `anchorHour ≈ now()` at fetch time (session load or hour-roll refresh per §4.6/D11 — the two are never more than seconds apart, immaterial at hour granularity). The dropped `start_at=gte.{anchorHour}` clause was strictly tighter than this derived lower bound — it constrained `startAt`, not `endAt`, so it excluded exactly the in-progress-at-open-time events the amendment's own rationale names, confirming the drop was necessary, not merely harmless. No under-fetch: every event that could satisfy the overlap predicate at some `k` survives the fetch. Any extra rows the query returns beyond what a given `k` needs are trimmed by §4.3's predicate on the client, which is correctness-neutral. No SQL, view, index, or RLS change follows from this confirmation.

`AppConfig.supabase == nil` throws `.unconfigured`, exactly as `DensityAPI` does — a missing plist is a valid state, not a crash.

### 4.3 Hour binding — overlap, not start-hour **[D1]**

An event belongs to hour offset `k` (`0…12`) when its interval intersects that bucket:

```
bucketStart = anchorHour + k·3600
bucketEnd   = bucketStart + 3600
renders(k)  ⟺ event.startAt < bucketEnd && event.endAt > bucketStart && event.endAt > now
```

This satisfies every PRD bullet at once, which is why it wins over the literal start-hour reading:

- req 1 bullet 1 — "start time inside the selected hour renders" — is implied by overlap, since an event starting inside the bucket always intersects it. The PRD states a **sufficient** condition; it does not state an exclusive one.
- req 1 bullet 3 — "an event outside the now → +12h window never renders" — holds: an interval disjoint from `[anchorHour, anchorHour + 13h)` intersects no bucket.
- req 5 bullet 2 — "stale events never render" — is the `endAt > now` clause, and it is the *same* clause, not a second rule bolted on.

**Named as an architect call widening req 1's literal criterion, flagged for `product` at review.** It is one predicate in one pure function and trivially reversible. The reason to make it: start-hour-only binding makes a four-hour rooftop party visible for exactly one of the four hours it is happening, which is a renderer that answers a different question than the one the strategy asked.

### 4.4 Selection — the whole of req 3, in one pure function

```swift
enum EventSelection {
    /// [ASSUMPTION] §8 D3. One constant, one call site.
    static let markerCap = 12

    /// Pure. No store, no clock of its own, no network.
    static func selected(
        from events: [LiveEvent],
        anchorHour: Date,
        offset: Int,
        now: Date,
        cap: Int = markerCap
    ) -> [LiveEvent]
}
```

Three steps, in order, and nothing else: **filter** by §4.3's predicate → **sort** by `(rank descending, startAt ascending, id ascending)` → **`prefix(cap)`**.

- **The sort is a total order.** Rank ties are broken by start time then by id, so the rendered set cannot churn between two renders of the same data. `id` is a server uuid, stable across fetches (T-043 §3.2), so identity is stable too.
- **The client re-derives nothing.** `rank` is read here and nowhere else in the app. `ios-code-reviewer` findings, both blocking: any use of `rank` outside this sort, and any arithmetic on it at all — a computed score, a normalisation, a per-Hood re-scope. That is req 3 bullet 2 made structural.
- **The cap is 12. [ASSUMPTION]** Derivation, stated so it can be argued with: Tel Aviv is a couple of dozen Hoods (decision #12), so 12 markers is on the order of one per two Hoods at city-wide zoom — punctuation over a fill layer rather than a second surface competing with it. The PRD's own open question defers the real number to real event volume, which does not exist yet; this is the placeholder that keeps req 3 bullet 3 testable in the meantime. One constant, one call site, overturned in a line.
- **`selected` is called once per render pass**, from the same one-resolution-per-pass seam T-032 introduces for heat (`HeatComposition.fills`), never per marker.

### 4.5 The marker, its zoom rule, and the tap it must not lose

```swift
struct EventLayer: MapContent {
    let event: LiveEvent
    let action: () -> Void
}
```

Built as a near-copy of the shipped `PlaceLayer`: an `Annotation` holding a real `Button` (VoiceOver needs an activatable element), `.annotationTitles(.hidden)`, `.accessibilityLabel("\(event.name), event, \(timeLabel)")`, `.accessibilityIdentifier("eventMarker-\(event.id)")`, and a ≥44pt frame regardless of the drawn glyph size.

**Silhouette — req 1 bullet 4, "shape or glyph, not colour alone."** Place pins are a `Circle` filled `Color.accentColor` carrying a category glyph. Event markers are a **rounded rectangle** (continuous corner radius) filled `Color("EventMarker")` carrying **`Image(systemName: "sparkles")`**. The distinction is carried by the container's silhouette, so it survives greyscale — which is how §9 checks it, rather than by inspection. **[ASSUMPTION] on the glyph specifically:** `sparkles` reads "something is happening here" and is category-agnostic, which the P1 category-glyph line requires it to stay in V1; it collides with nothing already in the app's vocabulary (`flame.fill` heat, `location.fill` near-me, `bookmark` save, category symbols on pins). One line, and the post-ship `designer` redesign pass is exactly the gate that should overturn it if it is wrong — the same posture T-032's D6 held before `designer` pinned `flame.fill`.

`Color("EventMarker")` gets its own colour set and a test asserting it differs from `HeatPalette.fill(for:)` at **every** `HeatBand` case and clears 3:1 against them. That is req 2's first bullet checked at the token level, not argued.

**Zoom: every zoom [D2].** Place pins are gated on `showsNames` because there are dozens per Hood; there are at most 12 events in the entire city (§4.4), and a layer the strategy puts "alongside heat + tag" cannot be invisible at the zoom a cold open shows. This is a stated divergence from `map-rendering-spec.md` §2's "Pins: none at city-wide" row — that row exists to solve place-pin density, and the cap is the mechanism that makes the divergence safe. The cap and the zoom rule are one decision; overturning either without the other is wrong. **Flagged for `designer`/`product` at review.**

**Tap resolution — the finding from the shipped code [D7].** `MapScreen.swift:113-122` attaches a greedy `SpatialTapGesture` via `.simultaneousGesture` (the FB19394663 workaround). A tap on an event marker therefore fires **both** the marker's `Button` *and* `handleTap`, and `handleTap` today resolves to a Place or a Hood and calls `openHood`/`openPlace` — which would clear the event that was just set and open the wrong sheet. `PlaceLayer` survives this only because both paths land on the same place and `DetailRouter.openPlace` is idempotent.

So events take the identical route rather than a new one: an `EventHitTester` mirroring the shipped `PlaceHitTester`, and an **event-first precedence** in `handleTap`:

```
event (ungated) → place (gated on showsNames) → hood
```

Event before place before hood, because a marker drawn on top must be the one a tap reaches. `openEvent` is idempotent, so both paths landing is safe.

**The gate rule, stated because this codebase has already been bitten by it.** T-033's acceptance REJECT was a hit-test branch running at a zoom where the thing it resolved was not drawn — an ~700m tolerance at city-wide zoom opening a modal for a pin nobody could see. The rule that fixed it is *tap resolution and rendering must share one gate*. Events honour it in the other direction: the markers render at every zoom, so the event branch is hit-tested at every zoom, and the live 22-screen-point tolerance is a finger-sized tolerance around a marker that is actually on screen. `ios-code-reviewer` should confirm the two gates match — not that the branch is ungated.

### 4.6 Loading and refresh **[D11]**

- **Once per session.** A fifth `.task { await eventStore.load(anchorHour: densityStore.anchorHour) }` in `MapScreen`, alongside the four already there.
- **On `scenePhase → .active`**, inside the existing `onChange` block that already calls `densityStore.refreshIfHourRolled()`. Refresh only when the hour rolled, reusing that same signal, so an app foregrounded twice in a minute makes no second request.
- **No timer, ever.** Same reasoning as T-032's D3: events are known in advance (the PRD's own `[ASSUMPTION]`), the payload covers 13 hours, and a scheduled wake to refresh a layer nobody is looking at buys nothing.
- **Staleness is not handled by fetching.** `endAt > now` is evaluated inside `EventSelection.selected` on every render pass, against a `now` passed in. This is what actually satisfies req 5 bullet 2, and it works with no network at all. **Honest limit, stated rather than glossed:** an event that ends while the user stares at an untouched map lingers until the next body invalidation — an hour change, a toggle, a foreground, a camera move. There is no timer to tighten that and adding one to correct a marker nobody is interacting with is the wrong trade. `qa` checks the rule after an hour change and after a foreground, which is what §9 asks for.

### 4.7 The detail sheet **[D6]**

`DetailRouter` gains a third depth-1 destination rather than a second `.sheet` — T-033 §4.2 settled that a single `.sheet` with switched content is this app's shape, and a second `.sheet` on the same view is the anti-pattern it rejected.

```swift
// Detail/DetailRouter.swift — additions
private(set) var event: LiveEvent?

/// Always depth 1, and mutually exclusive with both other destinations.
func openEvent(_ event: LiveEvent) { self.event = event; self.hood = nil; self.place = nil }
func closeEvent() { event = nil }

// isDepth1Presented's getter gains `|| event != nil`; its false-write path
// still routes to closeHood(), which must now also clear `event`.
```

An event replaces whatever was open rather than stacking on it — the same swap-in-place `openHood` already does. The alternative (an event as a depth-2 destination under a Hood sheet) would add a third level to a state machine whose whole design is that it cannot express one. `placeDepth` is untouched and keeps meaning what it means; events do not participate in it.

The sheet itself mirrors `PlaceDetailModal`: `.presentationDetents([.medium])`, `.presentationDragIndicator(.visible)`, map visible behind it via the `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` already on the shipped `.sheet`, and it is handed a `LiveEvent` by value, so it needs no new environment injection (which is what T-033's environment-propagation bug makes worth checking rather than assuming).

**Req 4 bullet 3 — "omitted, not blank" — is made unit-testable rather than eyeballed:**

```swift
enum EventDetailRows {
    enum Row: Equatable { case name, time, venue, hood, category }
    /// Pure. The rows this event actually renders, in order.
    static func rows(for event: LiveEvent) -> [Row]
}
```

The view iterates that array. A `nil` field cannot produce a row, because the row is not in the list. Any `if let` inline in the view body instead of a case in this function is a review finding — the point of the type is that the requirement is checkable without rendering anything.

**Directions** reuse the shipped `DirectionsService` unchanged: `router.closeEvent()` first, then `open(.appleMaps, to: RouteDestination(name: event.name, coordinate: event.coordinate))`, walking mode set in the one place the service sets it. **Named honestly:** PRD req 4 says "native Maps/Waze," and the shipped service builds Apple Maps only — T-033's D3 established that Waze's deep-link scheme exposes no walking parameter and that a PRD requirement is not the architect's to trade away. Events inherit that same decision and that same open item; this task neither widens nor re-litigates it.

### 4.8 The toggle **[req 6]**

One row, `EventsLayerToggle`, added to T-032's `HeatModalCard` — the seam T-032 §4.2 explicitly left for this task ("T-034's live-events toggle lands as a second row"). It binds directly to `EventStore.isLayerVisible`; there is no `@State` mirror, and the visibility value has exactly one storage location, the same rule §2.2 applies to the hour.

Off ⇒ `EventLayer` is not in the map content at all, and `handleTap`'s event branch is skipped. Heat and place pins are untouched by construction: neither reads `isLayerVisible`, and §9 checks that the composed fills and the pin set are identical before and after a toggle.

**Named dependency:** the PRD says the toggle sits "with the other layer toggles." There are none — T-032's D4 ships the modal with the slider only, because the heat layer has no on/off toggle in V1. This row will be alone in its section. That is a consequence of an already-made decision, not a new one, and it is stated here so nobody reads the singular row as a missing build.

**This is the one step in §11 with an unshipped dependency:** `HeatModalCard` does not exist until T-032 builds it (C5 there). Everything else in this task builds against already-shipped code.

---

## 5. Flow

```
Launch
  MapScreen .task → eventStore.load(anchorHour: densityStore.anchorHour)
      Phase 1 (BuildPhase.eventSeedIsAuthoritative == true):
          EventSeed.events(anchorHour:) → [LiveEvent], source = .seed, NO fetch attempted
      Phase 3 (constant false):
          EventsAPI.fetch(anchorHour:) → rows → [LiveEvent], source = .live
          on throw → events = [], source = .unavailable   ── never the seed (D8)

Every render pass
  EventSelection.selected(from: eventStore.events,
                          anchorHour: densityStore.anchorHour,
                          offset:     densityStore.selectedHour,      ← the one hour, D12
                          now:        Date())
      → overlap filter (§4.3) → stale drop → rank sort → prefix(12)
      → EventLayer per surviving event

Hour changes (slider or edge drag, T-032)
  selectedHour written → @Observable invalidation → the same body pass above
      → heat repaints AND the event set repaints, from one invalidation, no fetch

Tap an event marker
  Annotation Button → router.openEvent(e)
  ...and the map's SpatialTapGesture → handleTap → EventHitTester hits the same e
      → router.openEvent(e) again, idempotent → one sheet, the right one (D7)
  → EventDetailModal: EventDetailRows.rows(for: e), Directions → closeEvent() → Apple Maps

Toggle off (heat modal)
  eventStore.isLayerVisible = false
      → EventLayer leaves the map content; handleTap skips its event branch
      → HoodLayer fills and PlaceLayer pins: byte-identical, nothing read them

Empty / unreachable
  events == [] → selected returns [] → no markers, no banner, no modal, no indicator.
  The map is heat + pins exactly as it is today. This is the ship state if T-043 slips.
```

---

## 6. Third-party / dependencies

**None added.** No package, no account, no cost, nothing Aviran-gated. `MapKit`, `URLSession`, `Calendar`, `Date.FormatStyle` and SF Symbols are all platform, and the app's "no third-party packages until a TRD justifies one" rule (`passenger-code/README.md`) stays intact.

**Salvage.** `SALVAGE.md` marks `Models/LiveEvent.swift`, `Features/Map/EventMarker.swift`, `Features/Map/EventDetailCard.swift` and `Services/EventsService.swift` REUSE. Two things about that verdict:

- The archive is **not reachable from this workspace** (`~/APE Studio/locali` is absent — the same access gap T-031 and T-032 hit). `ios-developer` should not block on it.
- `prds/INDEX.md` already warns that the Locali overlay shipped as an unflagged raw feed. `EventsService` therefore has no notion of a ranked subset, a cap, or a served-set view, which is most of §4.4 — and view hierarchies and state management are never salvaged in this repo by rule. The REUSE verdict is worth at most the model's field list, which T-043's `events_public` supersedes anyway.

**Task dependencies:** T-031 (shipped) for the map and `DensityStore`; T-033 (accepted) for `DetailRouter` and `DirectionsService`; **T-032 for `HeatModalCard`** — the toggle step only (§4.8); T-043 for real data in Phase 3, and for nothing at all in Phase 1.

---

## 7. Rollout & migration

- **No feature flag.** The layer's kill switch is req 6's own toggle, and its ship-with-nothing state is req 5's own requirement. A flag would be a third mechanism for something two requirements already cover.
- **No migration, no backend deploy, no Aviran-gated apply step.** Nothing in §11 touches `database/`.
- **A second build-phase constant [D9].** `BuildPhase.eventSeedIsAuthoritative`, alongside the existing `seedIsAuthoritative`, both runtime constants for the reason that file already states (both branches stay compiled and reviewable). They are separate because the phases genuinely differ: places and density go live in **Build Phase 2**, events in **Build Phase 3** (`BOARD.md`). One shared constant would switch the events fetch on at Phase 2, against an `events_public` view that does not exist yet.
- **Once the constant is off, the seed is never a fallback [D8].** Precedence is `live → empty`, not `live → seed → empty`. A failed fetch in Phase 3 must render an honest empty layer — which req 5 explicitly blesses as a shippable state — not fake events sitting alongside real places and real heat. This is a deliberate divergence from `PlaceCatalog`'s seed-as-final-fallback, and the reason is that a stale place is still a real place while a fabricated event is a lie about tonight.
- **No disk cache [D8].** `DensityStore` and `PlaceCatalog` both cache; events do not. An events cache is mostly expired by the time it is read, it would need its own staleness policy, and req 5 makes an absent layer a first-class state rather than a degradation to explain. `CachedDataIndicator` stays a density-only affordance.
- **Phase 3 acceptance must re-run reqs 1–5 against the live feed** with the constant flipped. Phase-1 acceptance covers them against the fixture only.
- **Dependency direction:** nothing else needs to change what this task writes. T-036/T-037/T-038 add their own `NavSurface` views; the P1 per-Hood event count would read `EventSelection.selected(...)` and group by `hoodID`, with no change to anything here.

---

## 8. Decisions

### D1 — An event renders at every hour it overlaps, not only at its start hour
§4.3. Satisfies req 1 bullets 1 and 3 and req 5 bullet 2 with one predicate. Widens req 1 bullet 1's literal wording from a sufficient condition into an inclusive one; **flagged for `product`**. Carries §4.2's query amendment with it, which is the only reason the widening is reachable at all.

### D2 — Event markers render at every zoom
§4.5. A stated divergence from `map-rendering-spec.md` §2's pin row, whose density reasoning is about dozens of place pins per Hood, not about a capped city-wide set of 12. Made safe by D3 and inseparable from it. **Flagged for `designer`/`product`.**

### D3 — The marker cap is 12 **[ASSUMPTION]**
§4.4. One constant, one call site. Derivation stated (≈1 marker per 2 Hoods at city-wide zoom); the PRD defers the real number to real event volume, which does not exist. Trivially overturned.

### D4 — This task builds no clustering
Req 2 bullet 2 requires event markers to cluster by the same screen-distance rule as place pins. **That rule is not implemented anywhere in the shipped app.** `map-rendering-spec.md` §5 fully specifies the behaviour, and `T-041`/`PAS-30` is the board row tracking that no PRD owns building it — Build Phase 2, still unclaimed. Building a private clustering implementation inside `Events/` would duplicate work T-041 owns, over ≤12 markers, for a problem that does not exist at Phase-1 volumes. The cap is Phase 1's density bound; event markers join the shared cluster rule when T-041 lands. **§9 records this bullet as not verifiable in this task rather than inventing a pass condition for it** (`architect.md`, L-018), and it is named for `product` at review.

### D5 — Rounded-rect silhouette, `sparkles` glyph, own colour token
§4.5. Shape carries the place-pin distinction so it survives greyscale (req 1 bullet 4). Colour token asserted distinct from every heat fill (req 2 bullet 1). Glyph is **[ASSUMPTION]** with no design spec upstream — one line, and the post-ship redesign pass is the right gate for it. `sourceName` decoded and not rendered pending T-043 §8 F4.

### D6 — The event sheet is a third depth-1 destination on `DetailRouter`
§4.7. Not a second `.sheet` (T-033 §4.2 settled that), not a depth-2 destination (the state machine deliberately cannot express a third level). An event replaces whatever was open, matching `openHood`'s existing swap-in-place behaviour.

### D7 — `EventHitTester` plus event-first tap precedence
§4.5. Found by reading `MapScreen.swift:113-122`, not raised by any doc: the greedy `SpatialTapGesture` would otherwise fire after the marker's own `Button` and open a Hood sheet over the event the user tapped. Mirrors the shipped `PlaceLayer` two-path idempotent pattern rather than inventing a third mechanism. Rendering and hit-testing share one gate, which is the rule T-033's acceptance REJECT produced.

### D8 — No disk cache, and the seed is never a fallback once the constant is off
§7. A cached event set is mostly expired on read; an absent layer is a required, tested state. And a Phase-3 fetch failure must degrade to empty rather than to fabricated events shown beside real data.

### D9 — A second build-phase constant
§7. Events go live one build phase later than places and density; one shared constant would turn the events fetch on against a view that does not exist yet.

### D10 — The bundled fake event set ships in this task
§3.4. Closes the PRD's own named, unowned gap, with an authoring rule strong enough that §9's checks cannot pass vacuously. Same pattern T-033 shipped and T-032's TRD adopted. **Flagged for `product`.**

### D11 — No refresh timer; staleness is a render-time predicate
§4.6, and the same reasoning as T-032's D3. The honest residual (an event ending under an idle, untouched map) is stated rather than engineered around.

### D12 — No second hour property
§2.2. `Events/` is handed `anchorHour` and `selectedHour` and stores neither. T-032 §4.3's "exactly one storage location for the hour in the entire app" extends here unchanged; any stored hour inside `Events/` is a blocking review finding, which is what makes "repaints on the same hour changes heat does" structural rather than a convention.

---

## 9. Verification — one row per P0 requirement

Per `architect.md` (L-018): every P0 names a falsifiable check with an observable, a pass condition and the layer it is checked at. `qa` builds `prds/live-events-overlay/TEST-PLAN.md` from this table. **No row's pass condition is "looks right."**

| P0 | Observable | Pass condition | Layer | Step |
|---|---|---|---|---|
| **1** Renders in the current hour; hour change re-selects <400ms; nothing outside the window; distinguishable from a place pin | (a) `EventSelection.selected` over the fixture at each `offset` 0…12 with an injected `now`; (b) the `HourRepaint` signpost (T-032 §4.7) with the events layer on; (c) a fixture event whose interval is disjoint from `[anchor, anchor+13h)`; (d) a rendered marker and a rendered place pin with the colour catalog forced to greyscale | (a) the returned set for each `k` equals exactly the fixture events overlapping bucket `k` — computed independently in the test, not read back from the same function; the sets differ across at least 6 adjacent pairs; (b) p90 < 400ms driving the slider through `adjust(toNormalizedSliderPosition:)`; (c) returned for no `k`; (d) the two silhouettes differ with zero colour information | unit + UI test + manual | C3, C6, C8 |
| **2** Never competes with heat: no fill/area channel; neutral clustering | (a) `EventLayer`'s emitted `MapContent`; (b) `Color("EventMarker")` vs. `HeatPalette.fill(for:)` at every `HeatBand`; (c) **clustering — see below** | (a) `Annotation` only; a `MapPolygon`, a Hood stroke, or any area `foregroundStyle` inside `Events/`/`EventLayer.swift` fails review; (b) distinct from every band fill and ≥3:1 against each, in both `UIUserInterfaceStyle`s; (c) **no pass condition — not verifiable in this task** | unit + review | C5, C8 |
| **3** Ranked subset; order not re-derived; bounded; no per-user input | (a) `selected` over the fixture bucket holding `cap+2` events; (b) the same call with the input array shuffled; (c) the URL `EventsAPI` builds; (d) a grep of the diff | (a) exactly `markerCap` returned, and they are the top `cap` under `(rank desc, startAt asc, id asc)`; (b) byte-identical output — sort stability is not input-order-dependent; (c) identical for any two devices, carrying no location, device id or user field; (d) no `LocationStore` reference in `Events/`, and no use of `rank` anywhere but the sort comparator | unit + review | C4, C7 |
| **4** Tap opens a sheet with name/time/location in one tap, map visible; route hand-off; absent fields omitted | (a) tap an `eventMarker-<id>` in a UI test; (b) `EventDetailRows.rows(for:)` on a fixture event with `venue_name` and `category` null; (c) the Directions button's call path | (a) the sheet appears from one tap, `eventDetailTitle` carries that event's name, the sheet is `.medium` and the map is visible behind it, **and no Hood sheet appears** (D7's race); (b) the returned array contains no `.venue`/`.category` case and the rendered sheet has no empty row — asserted on the array, not by screenshot; (c) `closeEvent()` runs before `DirectionsService.open`, walking mode, `RouteDestination` carries the event's own name and coordinate | UI test + unit | C9, C10 |
| **5** Degrades to absent, never broken; stale never renders; usable permanently empty | (a) `EventStore.load` with a throwing fake API and the constant off; (b) the fixture's already-ended event, sampled after an hour change and after a `scenePhase` cycle; (c) the shipped T-031/T-033 UI test suites with `events == []` | (a) `events == []`, `source == .unavailable`, no banner/modal/indicator view is constructed anywhere in the diff for this state, and the map still renders heat and pins; (b) returned for no `k`, at any time sampled; (c) all pass unmodified | unit + UI test + manual | C1, C3, C11 |
| **6** Toggle in the heat modal; heat and pins untouched; state survives close/reopen | (a) `isLayerVisible` toggled off; (b) `HeatComposition.fills` output and `placeCatalog.allPlaces` before and after; (c) `MapChromeState.toggle(.heat)` → `.search` → `.heat` | (a) no `EventLayer` in the map content and the event tap branch skipped; (b) both byte-identical across the toggle; (c) `isLayerVisible` unchanged across the switch | unit + manual | C12 |

**Req 2's second bullet — event markers cluster by the same screen-distance rule as place pins — has no pass condition in this table, deliberately.** The rule it points at is unimplemented anywhere in the app (`T-041`/`PAS-30`, unowned, Build Phase 2). Writing a check for it here would either test a private duplicate implementation this TRD refuses to build (D4), or be a "looks right" row that no gate can fail — the exact failure L-018 exists to stop. **`product` decides at `trd-review`** whether to (a) accept the cap as Phase 1's bound and move this bullet to T-041, or (b) give T-041 an owner ahead of T-034's build. `architect` recommends (a): at ≤12 markers there is nothing to cluster, and (b) blocks a Phase-1 task on a Phase-2 one for no observable gain.

---

## 10. Risks and alternatives

| Risk | Mitigation / decision |
|---|---|
| The overlap rule (D1) is a wider reading of req 1 than its literal words | Flagged for `product` at review, with the reasoning stated. One predicate in one pure function. The literal reading is worse and §4.3 says why. |
| §4.2's query amendment edits a contract another TRD documented | No SQL, no view, no RLS, no build step — the view already enforces the floor the dropped filter was standing in for. `data-engineer` confirms at review (§11) rather than finding out in Phase 3. |
| The cap of 12 is a guess | Named **[ASSUMPTION]** with its derivation, one constant, and the PRD's own open question already defers the real number to real volume. §9 checks that the cap *binds*, not that 12 is correct. |
| Req 2's clustering bullet ships unverified | Named as unverifiable rather than waved through (§9, D4), with a decision put to `product`. Not silently satisfied "by construction." |
| Markers at every zoom (D2) bury the heat layer | The cap is the bound and the two are one decision. `qa` checks the city-wide view with the fixture's busiest hour loaded. Reversible in a line if it reads badly. |
| The `SpatialTapGesture` race opens a Hood sheet over the tapped event | D7 makes both paths land on the same idempotent call, the pattern already shipping for places. §9 row 4 checks it explicitly — this is a *confirm*, not an *assume*. |
| A stale event lingers on an idle map until the next invalidation | Stated plainly in §4.6 rather than claimed away. No timer. `qa` checks the rule after an hour change and after a foreground, which is what the requirement can actually promise. |
| The fixture makes the feature look verified when only the fixture path is | §7 states Phase-3 acceptance re-runs reqs 1–5 against the live feed. The fixture is named in §3.4, in `Source.seed`, and in its own build step — never invisible. |
| The fixture is authored without variation and §9 passes vacuously | §3.4's eight-clause authoring rule is asserted by a test in C2, not left to the author's care. |
| Touching accepted T-033 code (`DetailRouter`, `MapScreen`) | Three named changes (§4.5, §4.7), each with its reason. The shipped `DetailRouterTests` must pass unmodified alongside the new cases. |
| The toggle step is blocked on T-032, which is not built | Isolated to one step (C12). Everything else builds against shipped code. Named in §4.8 and in §11's ordering. |
| "Likely-interesting" may yet mean personalized | That question is open with Aviran and is `product`'s (PRD Open questions). It changes nothing in this document: the client sorts by whatever `rank` means and has no way to obtain a per-user input (§3.3). If the answer changes, it changes T-043, not T-034. |
| A demo fixture that names real venues reads as a real listing | §3.4 clause 8 requires plainly fictional names. |

**Alternatives considered and rejected:** start-hour-only binding (D1 — hides a running event from "now"); keeping T-043's `start_at=gte` lower bound (§4.2 — deletes exactly the rows the feature exists to show); a second `.sheet` for events (T-033 §4.2's settled anti-pattern); an event as a depth-2 destination under a Hood sheet (D6 — a third level the router deliberately cannot express); a private clustering implementation inside `Events/` (D4 — duplicates T-041 over 12 markers); a disk cache for events (D8 — expired on read, and absence is already a required state); falling back to the seed after a failed live fetch (D8 — fabricated events beside real data); a refresh timer (D11); one shared `BuildPhase` constant (D9 — fires the events fetch a phase early); gating markers on `showsNames` like place pins (D2 — makes the layer invisible at the zoom a cold open shows); re-deriving or re-scoping `rank` on device (§4.4 — req 3 bullet 2 forbids it and the sort is the only use).

---

## 11. Build breakdown

Ordered. **Every step is `[iOS]`.** No `[Backend]`, no `[Algo/Data]` — see §1.

| # | Step | Tag |
|---|---|---|
| C1 | `LiveEvent` + `EventStore` skeleton (`load`, `source`, `events`, `isLayerVisible`) with the `EventsFetching` protocol seam; the unreachable-API → empty path and its test (§9 row 5a) | **[iOS]** |
| C2 | **`EventSeed` + `events-tel-aviv-seed.json` + the `BuildPhase.eventSeedIsAuthoritative` branch** (§3.4, D9/D10). The eight-clause authoring rule is enforced by a test over the shipped fixture, not by the author's care. **Do C2 before C3–C6** — none of them are verifiable without it | **[iOS]** |
| C3 | **`EventSelection` — pure, with its full unit matrix**: overlap at every offset 0…12, out-of-window, already-ended, spanning event, empty bucket (§4.3, §4.6, §9 rows 1a/1c/5b). No view work in this step; the hardest thing in the feature lands first and tests with no simulator | **[iOS]** |
| C4 | `EventSelection`'s sort and cap: total order, shuffle-invariance, `cap+2` truncation (§4.4, §9 row 3a/3b) | **[iOS]** |
| C5 | `EventLayer` + the `EventMarker` colour set + the distinct-from-every-heat-fill and 3:1 contrast test, both styles (§4.5, §9 row 2b). Reuses `Support/ContrastRatio.swift` and the resolve-against-the-real-catalog pattern — never hardcoded hex | **[iOS]** |
| C6 | Wire the layer into `MapScreen`: one `.task`, one selection per render pass off `densityStore.anchorHour`/`.selectedHour`, ungated by zoom (§4.5, §4.6, D2/D12) | **[iOS]** |
| C7 | `EventsAPI` — the PostgREST GET of §4.2, built and inert. Test asserts the built URL's exact shape and that it carries nothing user-specific (§9 row 3c) | **[iOS]** |
| C8 | The greyscale silhouette check against a place pin, and the `EventLayer`-emits-only-`Annotation` review gate (§9 rows 1d, 2a) | **[iOS]** |
| C9 | `DetailRouter` — `event`, `openEvent`, `closeEvent`, `isDepth1Presented`, `closeHood` clearing `event`; extend the shipped `DetailRouterTests`, which must otherwise pass unmodified (§4.7, D6) | **[iOS]** |
| C10 | `EventDetailRows` + `EventDetailModal` + the Directions hand-off through the shipped `DirectionsService`; the omitted-row unit test (§4.7, §9 row 4b/4c) | **[iOS]** |
| C11 | **`EventHitTester` + event-first precedence in `MapScreen.handleTap`** (§4.5, D7). Verify: tapping a marker opens the event sheet and never a Hood sheet; a tap on empty map still resolves to a Hood exactly as today; the shipped `DetailSheetInteractionTests` pass unmodified (§9 row 4a) | **[iOS]** |
| C12 | **`EventsLayerToggle` in T-032's `HeatModalCard`** (§4.8) + the heat/pins-untouched and survives-a-nav-switch tests (§9 row 6). **Blocked on T-032's C5** — the only step in this task with an unshipped dependency; build C1–C11 first regardless of T-032's state | **[iOS]** |

**`trd-review` sign-off needed from: `ios-developer` + `ios-code-reviewer`.** `developer` and `code-reviewer` have no step to review — this TRD writes no SQL, no RLS and no migration.

Three targeted confirmations, none of them a full review pass:

- **`data-engineer`** on §4.2's query amendment (D1) — it changes no SQL and adds no build step, but it edits a client request `live-events-pipeline/TRD.md` §4.2 documented, and that TRD is already approved. **CONFIRMED correct as written, 2026-08-03** — see the confirmation note under §4.2.
- **`product`** on four calls that touch scope: D1's widened hour binding, **D4's clustering decision** (§9's open recommendation), D10's fixture claim, and D2's every-zoom rendering.
- **Cross-check against T-032's TRD** on §4.8 (the modal row seam) and §4.6 (the shared `scenePhase` refresh hook), and against **T-033's TRD** on §4.5/§4.7 (tap precedence and the router's destination set) — both are files this task modifies rather than only reads.
