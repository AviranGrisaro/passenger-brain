# Places — Been & Saved — TRD

**Task:** T-036 · **Linear:** `PAS-27` · **Status:** Accepted 2026-08-04 — shipped through `passenger-code 5e1f72f`, at `aviran-review`. v2.1 is a documentation-only amendment (T-058)
**Owner:** architect · **Date:** 2026-08-02 · **Revised:** 2026-08-04 (v2.1)
**PRD:** [`places-been-saved.md`](./places-been-saved.md) (Draft v1)
**Design reference:** [`design/phase-1/places-been-saved-design.md`](../../design/phase-1/places-been-saved-design.md) + its mockup — **informational input, not a gate.** The pre-code design gate was retired 2026-08-02 (`BOARD.md` lifecycle section). Where this TRD and that spec disagree, this TRD wins and says so (§8).
**Builds on:** [`prds/hood-place-detail/TRD.md`](../hood-place-detail/TRD.md) (T-033, shipped and accepted — `Place`, `PlaceCatalog`, `SavedPlacesStore`, `PlaceLayer`, `DetailRouter`) and [`prds/time-slider/TRD.md`](../time-slider/TRD.md) (T-032, `trd-review` — the chrome layering rule this feature's container sits inside). Neither is restated.
**Adjacent, not built here:** [`prds/places-dataset/TRD.md`](../places-dataset/TRD.md) (T-042) owns the `places.permanently_closed` column and migration `004_places.sql`.

**What changed at v2.1 (2026-08-04, T-058) — documentation only.** D7's and D8's *rationale* prose had gone stale against shipped code. §1 row 10, §2.1, §2.4, §4.5, §4.6, §5, D7, D8 and §10's fade risk row are rewritten to describe the system as built. **No requirement, contract, schema, test expectation or build step changes** — §9's verification table and §11's steps are untouched, and T-036 (ACCEPTed 2026-08-04, at `aviran-review`) is not reopened. Two independent causes:

1. **PAS-42** (`passenger-code 0e3b3dc`, founder-direct) moved `PlacesButton` into the always-visible `MapNavRow`. It never fades, and the re-tap protection D7 attributed to the fade now lives as `guard chrome.presented != .places else { return }` in `MapScreen.openPlacesList`.
2. **`qa`'s round-8 measurement** (2026-08-04, from a live xcresult accessibility snapshot) disproved D8's premise that `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` makes covered chrome tappable *through* a sheet. At `.medium` the depth-1 sheet occupies y 415–866 and `MapNavRow`'s buttons sit at y 700–744, entirely inside it. Pre-existing, not a PAS-42 regression — the same geometry held at the old bucket-2 position. D8's rule, its two enforcing calls, and the shipped behaviour are all unaffected.

**Deliberately not corrected here: §11 C7**, which still describes building the button with a fade. Build steps are the record of what was specified and built, and this pass's scope excludes them; carried on `BOARD.md` under T-058 rather than dropped.

**What changed at v2 (2026-08-02).** `trd-review` came back **REQUEST CHANGES** from both signoffs — `ios-developer` (`passenger-brain 1002595`) and `ios-code-reviewer` (`passenger-brain 158a5f3`…`d3fa249`) — on the same blocking finding, independently derived. This revision resolves exactly those findings and nothing else. No decision, contract or build step is redesigned; D1–D9 all stand as written at v1.

| # | Finding | Raised by | Fix in v2 |
|---|---|---|---|
| 1 | **Blocking.** §4.5 declared `enum NavSurface: Equatable { case heat, places }` and §2.2 claimed an "identical contract, either build order" with T-032. **The two documents specified different types.** T-032's real, live §4.1 is `enum NavSurface: String, CaseIterable, Sendable, Identifiable { case search, heat, places, profile }`, built **unconditionally** at its C1 with no "skip if it exists" clause anywhere in its text — it ships the full four-member set up front precisely to stop T-036/T-037/T-038 each inventing a private type (`ux-flows.md` §2.1's lock; T-032 §7's dependency-direction line). So in the live ordering (T-036 could land first) T-036's own C6 would create a narrower 2-case stub that T-032's C1 then has to restructure — 2→4 cases, three added conformances, a changed raw representation. That is exactly the restructuring §2.2 promised would not happen, promised unilaterally: there is **no reciprocal "whoever builds second doesn't restructure" language on T-032's side** | `ios-developer`, concurred independently by `ios-code-reviewer` | §4.5 now declares T-032 §4.1's contract **verbatim** — all four cases, real conformances. §2.2 is rewritten to state the dependency as it actually is (T-036 is a consumer of a type T-032 owns and fully specifies, not a co-author of it). C6's conditional now reads "if the file doesn't exist yet, create it exactly per T-032 §4.1; otherwise add nothing — `.places` is already there." §10's risk row restated to match |
| 2 | Should-fix, non-blocking. §3.4's "constraint the real detector inherits" list pinned the record *shape* but not the **update** invariant — keep-the-higher-kind on a revisit — which today exists only as a Phase-1 fixture-authoring rule (§4.2, tested by C4). PRD req 3 bullet 4 ("revisiting a Been place changes no label") depends on that invariant surviving into the real detector's write path at Phase 2 | `ios-code-reviewer` | One line added to §3.4 |

**Not fixed here, and why.** `ios-code-reviewer` also asked for a one-line correction to **T-032's own D1** prose ("the rest" slot into `MapNavRow` → Search and Profile only; Places is bucket-2 chrome, per D7) and `ios-developer` recommended a symmetric no-op note on **T-032's C1**. Both are edits to `prds/time-slider/TRD.md`, which **has another session's uncommitted v3 work in the shared working tree right now** — staging it would sweep in that session's in-flight text and attribute it to this pass (`CLAUDE.md` rule 2, the exact 2026-07-31 `0dd3d21` failure). Left for T-032's in-flight v3 pass to fold in; named in §10 and in this pass's worklog entry so it is owned, not dropped. **Superseded at v2.1 (2026-08-04): do not make the D1 edit.** PAS-42 moved Places into `MapNavRow`, so T-032's D1 prose is correct as written and correcting it would introduce the error (§2.4, D7). The `ios-developer` no-op note on T-032's C1 is unaffected and still owed. **T-036 does not depend on either edit landing** — after this revision T-036 declares T-032's type verbatim and creates nothing that T-032 would have to restructure, in either build order.

---

## 1. Context

Read the PRD first. Nothing here restates it. This document decides what it leaves open and pins the contracts `ios-developer` builds against.

**Surface: iOS-only. Confirmed, not assumed.** Checked three ways rather than inferred from the PRD's "device-local" line:

1. The PRD's Technical design says the list is device-local SwiftData/Core Data, *"writes nothing server-side in V1."* No per-user table, no RLS surface, no endpoint.
2. The one server-side field this feature reads — `places.permanently_closed` — **already has an owner and an approved TRD**: T-042's §3 schema (`permanently_closed boolean not null default false`, plus `closed_checked_at` and the `places_closed_has_source` constraint) and its §4 widened select. T-042 passed `trd-review` 3/3 and is held for Build Phase 2. This task adds no column and writes no SQL.
3. The Build-Phase-1 data for both halves already exists or is authored here in the client bundle: `places-tel-aviv.json` already carries `permanently_closed` on all 9 rows, and Been/Visited ships as a bundled fixture (§3.3).

**§10 contains no `[Backend]` and no `[Algo/Data]` step. `trd-review` routes to `ios-developer` + `ios-code-reviewer` only** (§10).

**What this feature is, architecturally.** Three things, only one of which is a screen:

1. **A second provenance source alongside `SavedPlacesStore`,** and a *pure read-time merge* over both. The PRD's "one row per (place, provenance), precedence applied at read time rather than by overwriting" is the whole data design; getting it wrong means a manual save destroying the record that a dwell happened.
2. **A field threaded end to end.** `permanentlyClosed` has to reach the client through all three of `PlaceCatalog`'s sources (seed, live, disk cache), or Build Phase 2 silently ships `false` for every place while the column says otherwise (§3.2).
3. **The second consumer of T-032's chrome layer** — the first task to prove that layer takes a second surface without being rewritten.

**Open items resolved here:**

| # | Open item | Source | Call | Where |
|---|---|---|---|---|
| 1 | `Place.permanentlyClosed` missing from the model | design §8.1; `Place.swift`'s own comment | Added, **non-optional `Bool`**, decoded on all three source paths, not just the seed | §3.2, **D1** |
| 2 | Been/Visited has no store and no detector in Build Phase 1 | design §8.2; PRD tech design | Bundled read-only fixture behind a new `BuildPhase.visitsAreSeeded`; **no persistence, no location code path built** | §3.3, **D2** |
| 3 | The read-time precedence merge needs a class/actor home | design §8.3 | **None** — it is a pure `enum PlacesListComposition` over two stores, not a third store | §4.3, **D3** |
| 4 | Row sort order unspecified | design §8.4 | **Name-ascending, id-tiebroken.** Recency is deliberately rejected here because it would force a payload migration on shipped, accepted `SavedPlacesStore` state | §4.4, **D4** |
| 5 | "An offline save… syncs later" describes an operation this feature does not perform | design §8.5 | Confirmed inherited boilerplate. No sync path, **and no offline banner ships** | §4.7, **D5** |
| 6 | Closed-state refresh is ownerless (T-044) | PRD risks; design §8.6 | Not resolved — but req 4's last bullet is satisfied *architecturally* by never copying closed state into a saved entry (§3.2) | §3.2, §9 row 4 |
| 7 | Where Apple Maps closed state is read | PRD open technical questions | The `places` column, server-refreshed. **Never a client-side `MKMapItem` lookup** | §3.2, **D6** |
| 8 | Whether provenance rows need a server copy for the localness pipeline | PRD open technical questions | **No, and not in V1.** A Been/Visited set is a movement log; putting one on a server is a new PRD with its own privacy review | §3.4 |
| 9 | What happens to a listed place dropped from the dataset | PRD open technical questions | The row disappears; the record is **not** deleted, so it returns if the place returns. Falls out of read-time composition for free | §4.3 |
| 10 | Which chrome bucket the Places button is in | found by reading `ux-flows.md` §2 against T-032's D1 | **The nav row.** v1–v2 called it bucket 2 off `ux-flows.md`'s "4th icon, separate from the 3 nav buttons," and it shipped that way; **PAS-42 reversed it** — the button is a permanent, never-fading member of `MapNavRow` | §2.4, **D7** |
| 11 | A nav surface and a system sheet could be co-presented | found by reading the shipped `.presentationBackgroundInteraction` | Forbidden in both directions, structurally: opening `.places` calls `closeHood()`; leaving `.places` calls `closePlace()`. (The premise that made this look urgent was wrong — see §4.6 — but the rule and its two calls stand) | §4.6, **D8** |

---

## 2. Architecture

### 2.1 Module layout — additions to T-033's tree

```
Passenger/
  Places/
    Place.swift                 MODIFIED — + permanentlyClosed (D1)
    PlaceCatalog.swift          MODIFIED — decode the field on all three paths
    PlacesAPI.swift             MODIFIED — select + PlaceRow gain permanently_closed
    PlacesCache.swift           MODIFIED — CachedPlace gains permanentlyClosed
    SavedPlacesStore.swift      MODIFIED — one added read accessor, nothing else (§4.2)
    PlaceProvenance.swift       new — PlaceProvenance + VisitKind (§4.1)
    VisitedPlacesStore.swift    new — Been/Visited source + VisitSourcing seam (§4.2)
    BundledVisitSource.swift    new — Build-Phase-1 fixture reader (§3.3)
    PlacesListComposition.swift new — pure merge + isListed (§4.3)
  PlacesList/
    PlacesListOverlay.swift     new — the z5 container: handle, ✕, scrim-aware (§4.5)
    PlacesListRow.swift         new — glyph, name, provenance word, closed badge (§4.4)
    PlacesListEmptyState.swift  new — icon + line + "Explore the map" CTA
    PlacesRowLabel.swift        new — pure VoiceOver string composition (§4.8)
  Map/
    MapScreen.swift             MODIFIED — hosts the surface, the button, the teardown rule
    PlaceLayer.swift            MODIFIED — isListed → dashed ring + a11y clause (§4.9)
    PlacesButton.swift          new — nav-row button, never fades (D7, as amended by PAS-42)
    MapChromeState.swift        NOT MODIFIED — T-032's type (its C1/§4.1). Created verbatim only if T-036 builds first; see §2.2
  Support/
    BuildPhase.swift            MODIFIED — + visitsAreSeeded (D2)
Resources/
  places-tel-aviv.json          MODIFIED — two rows flipped to permanently_closed: true
  place-visits-tel-aviv.json    new — Build-Phase-1 Been/Visited fixture (§3.3)
Assets.xcassets/
  BadgeSurface · BadgeOnSurface · MutedOnSurface   new colour sets (§4.10)
```

Xcode synchronized file groups are on — dropping files in the folder is enough, no `project.pbxproj` edit.

### 2.2 The one shared file with T-032 — T-032 owns it, T-036 consumes it (corrected at v2)

`MapChromeState.swift` (holding `NavSurface` and the one-surface-at-a-time rule) is **T-032's C1 and T-032's contract**, specified in full at its §4.1. T-036 is a **consumer**, not a co-author: it adds no case, no conformance and no method to that file, because T-032's type already contains `.places`.

That is not a courtesy reading of T-032's TRD, it is what the document says. T-032's C1 is unconditional and its §4.1 ships the whole four-member set (`search, heat, places, profile`) up front, deliberately — `ux-flows.md` §2.1 locks the set, and T-032's own commentary says the four members exist "to stop T-036/T-037/T-038 each inventing a private boolean." Its §7 dependency-direction line says the same from the other end: the downstream tasks add their own *views*, not their own state type.

So the build-order rule is one-directional, not a negotiation:

- **T-032's C1 has landed when T-036 builds (the expected order):** T-036 imports and reads `MapChromeState`. **Zero edits to that file.** `.places` already exists.
- **T-036 builds first:** it creates `MapChromeState.swift` **exactly per T-032 §4.1 — all four cases, all four conformances, verbatim** (reproduced at §4.5 so `ios-developer` does not have to open the other TRD to get it right). T-032's C1 then finds the file already correct and adds nothing to it.

Either way nobody restructures anything, because there is only ever one shape of this type in the tree. **v1 got this wrong** — it specified a narrower 2-case `Equatable` enum and promised, on T-032's behalf, that whoever built second wouldn't restructure it. T-032 never made that promise and its C1 would have had to break it. `ios-developer` and `ios-code-reviewer` both caught it at `trd-review`; the fix is to state T-032's real contract, not to negotiate a new one.

This is the only file the two tasks share; every other file in §2.1 is T-036's alone. **If T-032's §4.1 changes before either task builds, this section and §4.5 are stale by definition** — T-032 is the source, and a `trd-review` re-run on T-036 should diff the two before approving.

### 2.3 Boundaries — who is allowed to know what

- **`Places/` still knows no SwiftUI and no map view types.** `Place` gains a `Bool`, not a view concern. `PlacesListComposition` is a free function over value types — it takes `[Place]`, a `Set<Place.ID>` and a `[Place.ID: VisitKind]`, never a store, never an environment.
- **`VisitedPlacesStore` knows no CoreLocation.** In Build Phase 1 there is deliberately no import of `CoreLocation` anywhere in this feature's new files, and §9 row 5 makes that a reviewable check rather than a promise.
- **`PlacesList/` knows no fetching, no persistence, and no router internals.** It renders `[PlacesListEntry]` and reports a tapped `Place.ID`.
- **`Map/` remains the only layer that composes the two**, and the only layer that knows z-order — unchanged from T-031/T-032.
- **`PlaceLayer` gains one `Bool`, not a store.** It must not learn what "saved" means; it draws a ring when told to (§4.9).

### 2.4 Chrome placement — the Places button is a nav-row button (corrected 2026-08-04, PAS-42)

**What v1–v2 said, and what shipped.** This section originally placed the button in bucket 2, reading `ux-flows.md` §2's Primary table — *"Saved-places icon (4th icon) — Persistent icon, **separate from the 3 nav buttons**"* — together with that doc's 2026-07-30 stacking addendum, which names "near-me (L44) and the Places icon (L46)" as **bucket 2**: chrome that fades while a nav-row modal covers its position. It was built that way and then reversed by **PAS-42** (`passenger-code 0e3b3dc`, founder-direct): `PlacesButton` and `NearMeButton` were merged into `MapNavRow`, so all five icon buttons obey one visibility rule instead of two rows obeying two.

The merge had to resolve toward T-032's D1 ("always visible, always hit-testable, never covered") rather than toward D7's fade, and `MapNavRow`'s own header comment gives the reason: D7's rule applied to the whole row would fade `HeatButton` and `ProfileButton` while *their* modals are open, breaking already-shipped, already-tested re-tap-to-close behaviour.

So the button and its surface still sit in two different layers of T-032's z-order table — just not the two this section originally named:

| z | Layer | T-036's contribution |
|---|---|---|
| 0 | `Map` + `HoodLayer` + `PlaceLayer` | `PlaceLayer` gains the dashed ring (§4.9) — the only map-layer change |
| 3 | Scrim | Unchanged; presented whenever any `NavSurface` is, including `.places` |
| 4 | Bucket-2 chrome (`HoodButton`, `SettingsHint`) | **None.** `PlacesButton` was specced into this cluster and shipped there; PAS-42 moved it to z7, taking `NearMeButton` with it |
| 5 | Modal card | `PlacesListOverlay` |
| 7 | `MapNavRow` | **`PlacesButton` lives here** — permanently, with no fade and no visibility condition |

**T-032's D1 needed no correction after all.** This section previously corrected it for T-036 only; PAS-42 restored its original expectation that "T-036/T-037/T-038 add their own buttons to `MapNavRow`," which is now true of all three.

**What replaced the fade, stated rather than discovered (D7):** a button that never fades can be tapped while its own surface is open, and `chrome.toggle(.places)` on an open list would dismiss it — a fourth dismissal path this feature deliberately does not offer. `MapScreen.openPlacesList` therefore opens with `guard chrome.presented != .places else { return }`, so a re-tap is a true no-op that returns before either `closeHood()` or `toggle(.places)` runs. The three dismissal paths the list itself owns — drag handle, ✕, scrim tap — are unchanged and remain the only ways to close it, which is the set the design spec §1 asserts deliberately.

---

## 3. Data model

### 3.1 Two sources, one derived view — never one overwritten field

There is no `provenance` column, field, or stored property anywhere in this feature. There are two independent sources and a function:

| Source | Owns | Persists | Phase 1 content |
|---|---|---|---|
| `SavedPlacesStore` (shipped) | Saved | `saved-places.json`, slugs only | Whatever the user taps |
| `VisitedPlacesStore` (new) | Been, Visited | **nothing** | Bundled fixture (§3.3) |

A manual save writes only to the first; it cannot destroy the record that a dwell happened, because the two never touch the same storage. Un-saving removes an ID from the first, and the row either falls to the next word down or disappears — with **no second write** anywhere. That is the PRD's read-time-precedence requirement satisfied structurally rather than by discipline.

### 3.2 `permanentlyClosed` — one field, three source paths, one place it must never be copied to

`Place` gains `let permanentlyClosed: Bool`. Threading it is the actual work, and skipping any of the three paths produces a silent wrong answer rather than an error:

| Path | Change | If the field is absent |
|---|---|---|
| Bundled seed (`SeedFile.Entry`) | declare `permanently_closed`, non-optional | The file fails to decode → `.unavailable`, empty catalog. Loud, and a shipped-bundle decode test (C1) makes it a build-time failure instead |
| Live (`PlacesAPI.PlaceRow` + the `select=` string) | add the column to both | Payload decode throws → existing cache → seed. The already-designed fallback; nothing new |
| Disk cache (`PlacesCache.CachedPlace`) | add, non-optional | An older cache file fails to decode → `loadIfPresent()` returns `nil` → seed. **This is correct, and needs no migration or schema version** |

**Three consequences worth stating:**

- **No cache migration.** Build Phase 1 never writes `places-cache.json` at all (`BuildPhase.seedIsAuthoritative` short-circuits before the fetch), so no shipped device holds one. A stale cache decoding to `nil` and falling through to the seed is the behaviour `PlaceCatalog` was already built for. C1 includes a test that proves it rather than assuming it.
- **The field is never copied into a saved or visited record.** `saved-places.json` holds slugs; the visit fixture holds slugs and a kind. Closed state is read from `PlaceCatalog` at every render. This is what makes PRD req 4's fourth bullet — *"a place that closes after being saved shows the badge next time the list renders"* — true by construction, whatever the freshness of the underlying column. **The freshness itself is T-044's, still ownerless**; this TRD does not claim to fix that and §9 row 4 says exactly which half is checkable here.
- **`is_tourist_trap`, `place_type` and `keywords` stay out.** T-042's amendment table assigns one field per reading task; this is the task for `permanently_closed` and only that one. The row's tourist-heavy line therefore ships as a reserved empty slot, exactly as `PlaceDetailModal.touristTrapSlot` already does (§4.4).

**D6 — the client never does an `MKMapItem` lookup for closed state.** Per-place lookups in a scrolling list would be a network round trip per row, would defeat the sub-400ms open, and would hand Apple the identity of every place in a user's personal list — a location-adjacent leak this feature has no reason to create. The column is the single source; refreshing it is server-side work.

### 3.3 Build Phase 1 — the Been/Visited fixture

There is no dwell/geofence detector in this codebase, and building one here would violate the PRD's own instruction that **one detector serves three consumers** (`data-engineer`'s, shared with T-035 and T-037, *"must not be built three times"*) as well as Build Phase 1's "fake/hardcoded data" scope.

`Resources/place-visits-tel-aviv.json`, read once per session, never written:

```json
{
  "schemaVersion": 1,
  "_note": "Build-Phase-1 demo fixture. Not detector output. No real user movement.",
  "visits": [
    { "place_id": "kerem-dr-shakshuka",           "kind": "been" },
    { "place_id": "kerem-carmel-spice-corner",    "kind": "been" },
    { "place_id": "florentin-street-art-walk",    "kind": "visited" },
    { "place_id": "neve-nachum-gutman-museum",    "kind": "visited" }
  ]
}
```

Those four IDs exist in `places-tel-aviv.json` today (verified against the shipped file, not copied from the design spec's suggestion) and are the same four the design mockup exercises, so design and build test the same rows. `kerem-carmel-spice-corner` and `neve-nachum-gutman-museum` are also the two rows C2 flips to `permanently_closed: true`, which makes `neve-nachum-gutman-museum` the worst-case row (Visited + closed) the design spec's §2.2 density resolution was written against.

**Authoring rule, enforced by a test (C4):** the fixture must contain at least one `been` and at least one `visited`, at least one entry that is also savable to exercise precedence, and at least one place that appears in *no* provenance source. Without that last one the "not every place is listed" half of the ring accent is unobservable.

**`BuildPhase.visitsAreSeeded`** is a second constant next to `seedIsAuthoritative`, not a reuse of it, because it names a different axis: `seedIsAuthoritative` is *bundled data vs. the server*, this is *fixture vs. a device sensor*. Collapsing them would make the Phase-2 flip turn on a real detector that does not exist. Both are runtime constants, not `#if`, for the reason `BuildPhase.swift`'s own comment already gives.

### 3.4 Location & privacy — what this feature is allowed to hold, now and later

A Been/Visited set **is** location history: the list of real places a person physically stood in for 20 minutes. It is the most sensitive artifact this app can produce, and Build Phase 1 is the cheapest moment to fix its shape.

- **Phase 1 stores nothing derived from the device's location.** The fixture is read-only bundle content; `VisitedPlacesStore` has no write path, no persistence file, and no `CoreLocation` import. §9 row 5 checks this at review, and it is the strongest form of "degraded permission never breaks this feature": there is no permission-dependent code path to degrade.
- **`saved-places.json` stays exactly as shipped** — slugs, no coordinates, no timestamps. This task adds nothing to it (D4 is chosen partly to keep that true).
- **The constraint the real detector inherits, written down now so it is not re-litigated later:** when the shared detector lands, the device-local record is `{place_id, kind, first_observed_at}` and nothing more — never a coordinate, never a dwell track, never a second visit's timestamp. Anything richer is a movement log, and this feature has no requirement that needs one.
- **The update invariant it inherits with it (added at v2):** on a repeat observation of a `place_id` already held, **keep the higher `VisitKind` and drop the other — never overwrite, never append a second row.** In Build Phase 1 this is a fixture-authoring rule enforced at load (§4.2, tested by C4); at Phase 2 it becomes the detector's write path, and PRD req 3 bullet 4 ("revisiting a Been place changes no label") is satisfied by nothing else. Written here rather than only in §4.2 so it survives the fixture being swapped out.
- **PRD open question answered: no server copy of provenance in V1.** Uploading a per-device Been set would create exactly the per-user movement log the strategy's no-accounts posture avoids by accident today. If the localness pipeline later needs this signal, that is a new PRD with its own privacy review — not a field quietly added here.

---

## 4. Contracts

### 4.1 Provenance — precedence is the type, not an if-chain

```swift
/// Ordered lowest → highest. Precedence (PRD req 1) is `max`, structurally:
/// there is no branch anyone can get backwards.
enum PlaceProvenance: Int, Comparable, Sendable, CaseIterable {
    case visited = 0
    case been    = 1
    case saved   = 2

    /// The one user-facing word. Nothing else in the app spells these out.
    var word: String { switch self { case .saved: "Saved"; case .been: "Been"; case .visited: "Visited" } }

    static func < (lhs: Self, rhs: Self) -> Bool { lhs.rawValue < rhs.rawValue }
}

/// What a detector (or, in Phase 1, the fixture) can produce. Deliberately a
/// separate type from `PlaceProvenance`: the visit source **cannot** claim
/// `.saved`, because that value does not exist in this enum.
enum VisitKind: String, Codable, Sendable {
    case been, visited
    var provenance: PlaceProvenance { self == .been ? .been : .visited }
}
```

"Every row shows exactly one of Saved/Been/Visited — never two, never none" is then a property of `PlaceProvenance` being a single non-optional value on the entry type, not a rule a view has to honour.

### 4.2 The two stores

`SavedPlacesStore` gets **one** addition and no other change:

```swift
/// Read-only view of the saved set, for `PlacesListComposition` (T-036 §4.3).
/// Computed off the same `@Observable`-instrumented stored property `isSaved(_:)`
/// reads, so a list rendered from it re-renders on toggle with no new plumbing.
var savedPlaceIDs: Set<Place.ID> { savedIDs }
```

Nothing about its toggle path, generation guard, persistence format or tests moves. Req 2's sub-400ms save is already met by the shipped implementation and this task does not re-derive it.

```swift
protocol VisitSourcing: Sendable {
    func loadVisits() async -> [Place.ID: VisitKind]
}

/// Build Phase 1: bundled fixture (§3.3). Phase 2+ swaps the conforming type
/// for the shared detector's store — this protocol is the whole seam, mirroring
/// `PlacesFetching`/`PlacesCaching`/`SavedPlacesPersisting`.
struct BundledVisitSource: VisitSourcing { init(resourceName: String = "place-visits-tel-aviv", bundle: Bundle = .main) }

@MainActor @Observable
final class VisitedPlacesStore {
    private(set) var visits: [Place.ID: VisitKind] = [:]
    init(source: any VisitSourcing = BundledVisitSource())
    /// Once per session, on `MapScreen`'s `.task`, alongside the other three loads.
    /// A missing or malformed fixture is an empty dictionary, never a crash —
    /// same posture as `PlaceCatalog.loadFromBundledSeed()`.
    func load() async
}
```

A duplicate `place_id` in the fixture is a boundary error: keep the **higher** kind (`been` over `visited`) and drop the other, so the file cannot produce two rows for one place.

### 4.3 The merge — a pure function, not a third store (D3)

```swift
struct PlacesListEntry: Identifiable, Sendable, Equatable {
    let place: Place
    let provenance: PlaceProvenance
    var id: Place.ID { place.id }
}

enum PlacesListComposition {
    /// Read-time precedence (PRD req 1). One entry per place, whatever touched it.
    /// A saved or visited id with no matching `Place` is **skipped, not deleted** —
    /// there is nothing to render without a name and category, and the underlying
    /// record survives so the row returns if the place returns to the dataset.
    static func entries(
        places: [Place],
        saved: Set<Place.ID>,
        visits: [Place.ID: VisitKind]
    ) -> [PlacesListEntry]

    /// The map ring's predicate (PRD req 7) — binary, provenance-blind, O(1).
    static func isListed(_ id: Place.ID, saved: Set<Place.ID>, visits: [Place.ID: VisitKind]) -> Bool
}
```

The design spec asked for "some function or store." It is the function. A third `@Observable` store would hold state derived from two other stores and would therefore have an invalidation problem — the exact class of bug the PRD's read-time-precedence rule exists to avoid. `entries` runs over 9 places in Phase 1 and a few hundred at Phase 2 scale; it is a dictionary lookup per place and does not need memoising. If it ever does, the seam is one function, not a rewrite.

`isListed` is called once per rendered pin per camera change. It must be a `Set`/dictionary lookup — never a linear scan over `entries` — and C12's test asserts it agrees with `entries` on every place.

### 4.4 The row

Order, top to bottom, per the design spec's §2.2 density resolution (adopted unchanged — it resolves the PRD's own flagged risk and this TRD has no reason to reopen it):

| Element | Contract |
|---|---|
| Glyph | `place.category.symbolName` — the shipped two-glyph vocabulary, no new set |
| Name | `place.name`, semantic style |
| Provenance word | `entry.provenance.word`, plain text, `MutedOnSurface` — never a pill, present on every row |
| Closed badge | Rendered **iff** `place.permanentlyClosed`. `Capsule()` + `BadgeSurface`/`BadgeOnSurface`, glyph `Image(systemName: "nosign")` **[ASSUMPTION]** — the design spec deferred the exact symbol; this pins one so `ios-developer` does not have to invent it. Never red, never an alarm tone (decision #38) |
| Tourist-heavy line | **Reserved empty slot.** `Place` carries no `isTouristTrap` in this task (§3.2), so there is nothing to condition on. Built exactly like `PlaceDetailModal.touristTrapSlot`: an `@ViewBuilder` returning `EmptyView()`, with the same comment forbidding a fabricated placeholder value. T-035 fills it |

The whole row is one tap target (`min-height` 64pt); nothing inside it is independently tappable, so the badge and the flag line can never become sub-44pt targets.

**D4 — sort is `name` ascending, `id` as tiebreak.** Recency-first is the better product answer and is deliberately not built: `SavedPlacesStore` persists a `Set<String>` with no timestamps, so recency would require a versioned payload plus a migration path in `SavedPlacesPersistence` — real cost on shipped, accepted state, for an ordering no P0 requirement names. Name-ascending is deterministic (which makes §9 row 1 checkable at all), matches `PlaceCatalog`'s existing name-sort idiom, and is one line to change once timestamps exist for another reason. Flagged for `product` at review.

### 4.5 The container

`PlacesListOverlay` is a `ZStack` layer at T-032's z5, **not** `.sheet()` — same reason and same construction as T-032's D2, reused rather than re-derived: a system sheet covers the nav row and breaks `ux-flows.md` §2.1's direct-switch rule.

The chrome state this container hangs off is **T-032's, reproduced verbatim from its §4.1** (`prds/time-slider/TRD.md`) so `ios-developer` builds against one shape whichever task lands first. T-036 adds nothing to it — `.places` is already a member (§2.2):

```swift
// T-032 §4.1, verbatim. T-036 does not modify this type.
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

`.search` and `.profile` are T-038's and T-037's and have no view in this task's diff — same rule T-032 states for its own build: a case with no view ships nothing, and `ios-code-reviewer` should reject *view* work for any surface other than `.places` in T-036's diff. `toggle(.places)` on the already-open list dismisses it, and that path is unreachable by tap in this feature — but after PAS-42 for a different reason than D7 originally gave. The button no longer fades; instead `MapScreen.openPlacesList` guards the re-tap explicitly (`guard chrome.presented != .places else { return }`) and never reaches the toggle (§2.4, D7). The toggle's dismiss semantic is still correct and is what a programmatic switch between surfaces relies on.

Dismissal paths: drag handle (downward `DragGesture` past a threshold), a 44×44pt ✕, and the z3 scrim tap. Entrance/exit transition honours Reduce Motion by collapsing to 0 duration, never by skipping the state change.

### 4.6 Presentation exclusivity — a nav surface and a system sheet are never co-presented (D8)

A `NavSurface` and a system sheet are never both up. The rule is enforced by two explicit calls — not by a flag, and not by anything the presentation API guarantees on its own:

- **Opening `.places` calls `router.closeHood()` first.** Without it, opening the list with a Hood sheet up would present it *underneath* a system sheet, in a layer that can never be reached. **Measured caveat (2026-08-04):** that ordering is not tap-reachable today. At `.medium` the depth-1 sheet occupies y 415–866 and `MapNavRow`'s buttons sit at y 700–744 — entirely inside it — so a tap aimed at a nav button lands on the sheet instead. The call is therefore a one-line structural guarantee that survives a detent, layout or row-position change, not a fix for a live defect.
- **Leaving `.places` (any path, including a switch to another surface) calls `router.closePlace()`.** While `.places` is presented the scrim blocks map taps, so a depth-1 place modal can only have been opened from a list row; closing the list must not strand it. `router.placeDepth == 1` is the condition, derived — no `entryPath` field is added to `DetailRouter`, and `DetailRouter` itself is not modified by this task. **This is the tap-reachable direction and the one that matters:** the stacked modal's own controls sit above the list, so a user dismisses it and then taps another nav button. Verified live by `PlacesListInteractionTests.testDismissingStackedPlaceModalRevealsListThenLeavingPlacesOpensHeat` (passing at `passenger-code 5e1f72f`).

**What `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` does and does not buy (corrected at v2.1).** It keeps the state underneath a `.medium` sheet interactive rather than inert — the buttons still exist, still respond, and are reachable once the sheet is out of the way. It does **not** make a visually covered button tappable *through* the sheet; hit-testing still resolves to whatever is on top. v1–v2 read it the stronger way and used that reading as D8's justification, which is what `qa` measured and disproved. The rule above, its two calls and the shipped behaviour are unchanged by the correction.

Row tap is therefore just `router.openPlace(place)` against the **existing** depth-1 sheet site. No second `.sheet` modifier, no new presentation mechanism, no `DetailRouter` change. The modal renders above the list; dismissing it reveals the list unchanged; dismissing the list returns to the map with camera and `selectedHour` untouched (neither is read or written anywhere in this feature).

### 4.7 States — and the one the design spec specs that does not ship (D5)

| State | Contract |
|---|---|
| Loading | None. `PlaceCatalog`, `SavedPlacesStore` and `VisitedPlacesStore` all resolve on `MapScreen`'s `.task` at launch; opening the list is a dictionary read. No spinner exists to design |
| Empty | Icon + one line + an "Explore the map" CTA that dismisses the list. Built from the start, not after a review finding |
| Degraded permission | **Nothing to build.** No code path in this feature reads authorization status, and none populates from a sensor (§3.3, §3.4). Req 5 is satisfied by absence; §9 row 5 checks it as absence |
| Offline | Every row renders from device. **No offline banner ships** |
| Place fails to resolve for a listed id | The row is not rendered (§4.3). No error surface |

**D5 — the offline banner is not built.** In Build Phase 1 no code path in this feature touches the network, so a banner could never appear on a real device; and per the PRD's own *"writes nothing server-side in V1"* there is nothing for an offline save to sync to, so the banner would also be describing a pending-upload state that does not exist. Shipping UI that can never render is the same failure T-032's D1 and D4 avoid — a dead control that invites "is this broken?" and that no test can exercise. The PRD's *"an offline save appears immediately and syncs later"* is read as inherited boilerplate; **flagged for `product` to correct the wording or overrule this**, not reinterpreted silently.

### 4.8 VoiceOver

One announcement per row, clauses appended in a fixed order — `map-rendering-spec.md` §7's established construction, extended:

```swift
enum PlacesRowLabel {
    /// "Nachum Gutman Museum, Things to do, Visited, permanently closed"
    static func label(name: String, category: PlaceCategory, provenance: PlaceProvenance, isClosed: Bool) -> String
}
```

Pure and unit-tested over the full 3 × 2 matrix — no simulator, no VoiceOver session needed to prove the strings. The tourist-heavy clause is T-035's to append when it fills the slot.

### 4.9 The ring accent

`PlaceLayer` gains `let isListed: Bool` and, when true, an overlay on the existing 44pt circle:

- **Dashed** `Circle().strokeBorder(style: StrokeStyle(lineWidth: 2.5, dash: [...]))`, inset −6pt, `Color.accentColor` — the shape pairing `map-rendering-spec.md` §6's 2026-08-02 addendum specifies, so it is not colour-alone.
- `.allowsHitTesting(false)`. The ring draws outside the button's frame and must not become part of the tap target; the 44pt frame is unchanged, satisfying req 7's touch-target bullet by construction.
- Accessibility label gains `", in your Places"` — the clause `map-rendering-spec.md` §7 already defines.
- **Close-zoom-only needs no new threshold.** `MapScreen` already gates the entire `PlaceLayer` `ForEach` on `showsNames`; a ring on a pin that isn't drawn cannot render. No second zoom constant is introduced, and §9 row 7 checks the gate rather than a new number.
- **Provenance-blind, per `map-rendering-spec.md` §6** — `isListed` is a `Bool`, so there is no channel through which provenance could leak onto the map.

Clustering (`map-rendering-spec.md` §5, T-041) is unowned and out of scope here, exactly as T-033 left it; nothing in this task makes it more or less needed.

### 4.10 Colour tokens

Three sets: `MutedOnSurface` (provenance word, ≥4.5:1 on `Surface`), `BadgeSurface` + `BadgeOnSurface` (the closed pill, ≥4.5:1 against each other). **`MutedOnSurface` is also declared by T-032's C9** — whichever task lands first creates it; the second reuses it and does not create a second token with a different value. `Color("Flag")` is T-035's and is not created here. The ring reuses the shipped `AccentColor` and is checked at the 3:1 graphical-object bar, not the 4.5:1 text bar.

---

## 5. Flow

**Cold launch.** `MapScreen.task` fans out four independent loads — hoods, density, `PlaceCatalog`, `SavedPlacesStore`, plus `VisitedPlacesStore` (new, fifth). None blocks the first frame; the map is interactive before any of them resolve. `PlaceLayer` renders rings as soon as both the catalog and the two provenance sources have landed, with no explicit ordering between them — a pin drawn before the stores resolve simply has `isListed == false` and gains its ring on the next render, because `@Observable` drives it.

**Open the list.** Tap `PlacesButton` (in the nav row at z7) → the `guard chrome.presented != .places` no-op check (D7) → `router.closeHood()` (D8) → `chrome.toggle(.places)` → scrim at z3, the remaining bucket-2 chrome (`HoodButton`, `SettingsHint`) fades at z4, overlay slides in at z5, the whole nav row — `PlacesButton` included — stays live at z7. `PlacesListComposition.entries` runs once per render pass over already-loaded data.

**Open a place.** Tap row → `router.openPlace(place)` → the existing depth-1 sheet presents above everything. Dismiss → back to the list, unchanged.

**Un-save from that modal.** `savedPlaces.toggle(id)` → `savedPlaceIDs` changes → the list re-renders → the row either drops to the next word down (if the fixture has a Been/Visited entry for it) or disappears. **No write happens to any visit record**, which is the whole point of §3.1.

**Switch surfaces.** Tap the heat button while the list is open → `chrome.toggle(.heat)` → leaving `.places` runs `router.closePlace()` (D8) → the list and any stacked place modal both go, the heat modal opens, no intermediate empty frame.

**Error paths.** Missing/corrupt visit fixture → empty dictionary → the list shows Saved rows only, or the empty state. Missing/corrupt seed → `PlaceCatalog` reports `.unavailable` → no places resolve → the list is empty and no row can be rendered for an unresolvable id. Neither crashes; neither shows an error surface.

---

## 6. Third-party / dependencies

**None added.** No package, no account, no cost, nothing Aviran-gated. `Capsule`, `StrokeStyle`, `DragGesture`, `JSONDecoder` and `@Observable` are all platform. `passenger-code/README.md`'s "no third-party packages until a TRD justifies one" stays intact.

**Salvage.** `SALVAGE.md` marks `Services/SavedPlacesStore.swift` and `Features/Places/SavedPlacesSheet.swift` REUSE, and `VisitedPlacesStore.swift`/`VisitDetectionService.swift`/`CityGeofenceMonitor.swift` REFERENCE-only (entangled with Phase-3 logic). Two things make this moot: the archive is **not reachable from this workspace** (`~/APE Studio/locali` is absent — the same gap T-031/T-032 hit), and the REUSE half is already re-derived and shipped as the current `SavedPlacesStore`. The REFERENCE half is detector code this task deliberately does not build (§3.3). **`ios-developer` should not block on salvage access.**

**Task dependencies:** T-032's C1 (`MapChromeState`), per §2.2 — the only build-order coupling. T-042's migration `004` is *not* a dependency of this task's build; it is the Phase-2 source for a field this task reads from the bundled seed today.

---

## 7. Rollout & migration

- **No feature flag.** The button and its surface arrive together; the off-state of a flag would be a list with no door.
- **No migration, no backend deploy, no Aviran-gated apply step.** Nothing in §10 touches `database/`.
- **No persisted-state migration.** `saved-places.json` is untouched (§4.2, D4). `places-cache.json` gains a field and an older file simply fails to decode and falls through to the seed — the designed behaviour, never written in Phase 1 anyway (§3.2).
- **Build Phase 1 → 2 is two constants and one conforming type.** `BuildPhase.seedIsAuthoritative → false` moves the catalog (including `permanentlyClosed`) onto T-042's column. `BuildPhase.visitsAreSeeded → false` plus a `VisitSourcing` conformer backed by the shared detector moves Been/Visited onto real signal. **Phase 2 must re-verify PRD req 3 and req 5's Been/Visited bullets against that detector** — Phase-1 acceptance covers them against a fixture only, and §9 says so per row rather than letting it be inferred.
- **Ships independently of the backend.** With no `SupabaseConfig.plist` the list opens, rows render, the badge renders, saving works, and the ring draws.
- **Dependency direction.** T-037 (Passport) consumes the Been signal: it reads `VisitedPlacesStore.visits`, and the `VisitSourcing` seam is deliberately shaped so Passport needs no change when the detector replaces the fixture. T-035 fills the row's reserved flag slot and adds `Place.isTouristTrap`. Neither needs to change anything this task writes.

---

## 8. Decisions and deviations

### D1 — `permanentlyClosed` is threaded through all three source paths, non-optional
Adding it to `Place` and the seed alone would compile, pass Phase-1 tests, and ship a silent `false` for every place the moment Phase 2 flips the constant — the failure mode is invisible precisely where the data starts mattering. Non-optional on all three paths turns a missing field into a decode failure with a designed fallback instead of a wrong answer.

### D2 — Been/Visited is a bundled fixture, with no persistence and no `CoreLocation`
Build Phase 1's scope, and the PRD's own "one detector, three consumers, `data-engineer`'s" rule. The stronger reason is §3.4's: the first version of a location-history store is the one whose shape everything later inherits, and the safest shape at this stage is "there isn't one." Second constant, not a reuse of `seedIsAuthoritative`, because the axes differ (§3.3).

### D3 — The precedence merge is a pure function, not a third store
Settles design §8.3. A derived `@Observable` store would hold state computed from two other stores and would need invalidation; a function cannot go stale. `PlaceProvenance: Comparable` makes precedence a `max`, so "Saved beats Been beats Visited" has no branch to get backwards.

### D4 — Sort is name-ascending, not recency
Settles design §8.4. Recency would force a versioned payload and a migration on shipped, accepted `SavedPlacesStore` state for an ordering no P0 names. Deterministic ordering is also what makes §9 row 1 a falsifiable check. One line to change later. **Flagged for `product`.**

### D5 — No offline banner ships
Settles design §8.5 in the direction the design spec itself flagged. It could never render in Phase 1 and would describe a sync that does not exist in V1 at all. **Flagged for `product`** — this is a deliberate non-build of a specced element, not an omission.

### D6 — Closed state is read from the `places` column, never a client `MKMapItem` lookup
Settles the PRD's open technical question. Per-row lookups would cost a round trip inside a list scroll and would disclose a user's personal place list to a third party. The staleness question is real and is T-044's; the answer to *where it's read* is not contingent on it.

### D7 — The Places button is a nav-row button; re-tap is blocked by a guard, not by a fade
**Amended 2026-08-04 (PAS-42, `passenger-code 0e3b3dc`) — the original call and the reason it was reversed are in §2.4.** v1–v2 read `ux-flows.md` §2 ("4th icon, separate from the 3 nav buttons") and its stacking addendum as putting this button in bucket 2, and accepted that it would fade under its own surface. It shipped that way and was then reversed by founder direction: `PlacesButton` is a permanent member of `MapNavRow`, beside `NearMeButton`, and never fades.

The one thing the fade protected — the list not being dismissible by re-tapping its own icon — now lives in `MapScreen.openPlacesList` as `guard chrome.presented != .places else { return }`. That is a stricter guarantee than the fade was: a fade is a visibility state a layout change can undo, a guard is a branch. The list's own three dismissal paths (drag handle, ✕, scrim tap) are unchanged, and T-032's D1 needs no correction from this task.

### D8 — A `NavSurface` and a system sheet are never co-presented, in either direction
**The rule, its two enforcing calls and the shipped behaviour are unchanged; only the rationale is corrected (v2.1, T-058).** Enforced by two calls (§4.6) rather than a flag, and it needs no `DetailRouter` change: `placeDepth == 1` under a presented `.places` already means "opened from a row," because the scrim blocks every other route to it.

**Of the two orderings, only one is tap-reachable, and the enforcement is what makes the decision sound — not the reachability.** Leaving `.places` with a place modal stacked on top is reachable and routine: `handlePresentedSurfaceChange` closing that modal on the way out is what stops it being stranded, verified live by `PlacesListInteractionTests.testDismissingStackedPlaceModalRevealsListThenLeavingPlacesOpensHeat` (passing at `passenger-code 5e1f72f`). The other ordering — a nav button tapped while a depth-1 sheet is up — is not reachable by tap, because at `.medium` the sheet covers the nav row's buttons outright (§4.6), so `router.closeHood()` in `openPlacesList` is a cheap structural guarantee rather than a fix for a live defect.

v1–v2 justified this decision by asserting that `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` makes the chrome underneath tappable *through* the sheet, so "both orderings are reachable states." `qa` measured otherwise from a live xcresult accessibility snapshot (round 8, 2026-08-04) and the claim does not survive real sheet geometry. It was wrong at the old bucket-2 position too — this is a pre-existing error in the reasoning, not a PAS-42 regression.

### D9 — The row's tourist-heavy line ships as a reserved empty slot
Same construction and same comment as the shipped `PlaceDetailModal.touristTrapSlot`. `Place` gains one field in this task, not four (T-042's amendment table). **Consequence, stated rather than discovered:** the design spec's §2.2 worst-case row (provenance + badge + flag) cannot be exercised until T-035 lands, so §9 row 4 checks the two-element case and names the third as carried forward.

---

## 9. Verification — one row per P0 requirement

Per `architect.md` (L-018): every P0 names a falsifiable check with an observable, a pass condition, and the layer. `qa` builds `prds/places-been-saved/TEST-PLAN.md` from this table. **No row's pass condition is "looks right."**

**Standing rule, ratified workspace-wide 2026-08-07 — a check sequenced behind a known-failing sibling is unrun, not passed.** (`product` at T-077/`PAS-51` acceptance; `architect` ratification; canonical text in `architect.md` §9, lifted in here because `qa` reads this table on its own.) Under `continueAfterFailure = false` — set by eight of this repo's ten `PassengerUITests` classes — and equally under `try #require`, `XCTUnwrap`, or an early `return` inside a shared assertion helper, the *first* failing assertion aborts every assertion after it in that method, while `xcodebuild` still reports **one** failure line for the whole method. A gate that counts failure lines reads that silence as a pass. **So no check in this table may share a test method with an assertion that is known to fail and is owned by another ticket** — move the known failure into its own method, where it stays visibly red and tracked while its siblings still execute. Any report on this table states, per sub-check, *that it executed*; a sub-check whose execution cannot be shown in the result bundle is **unrun**, exactly like a BLOCKED row. **`XCTExpectFailure` is not the fix** — it turns the method green and buries the tracked gap. **Audited against this rule in the same pass:** no row here is currently discharged in a test method carrying a disclosed known-failing assertion, so no row moves; the rule binds any future one.

| P0 | Observable | Pass condition | Layer | Step |
|---|---|---|---|---|
| **1** One list, three provenance states, one word per row, precedence Saved>Been>Visited, one row per place | `PlacesListComposition.entries` over a fixture where one place carries all three, one carries two, one carries each alone | Output count == distinct place count; the all-three place appears once with `.saved`; the Been+Visited place appears once with `.been`; `provenance` is non-optional so "never none" is structural; output order is name-ascending and identical across runs | unit | C3 |
| **2** Manual save <400ms, persists, reopen shows saved; un-save falls to the next word or removes the row | Shipped `SavedPlacesStoreTests` (unchanged) + a new composition test: toggle a saved id off with, and without, a fixture visit entry | Shipped tests still pass unmodified; with a `been` entry present the entry survives with `.been`; without one the entry disappears; **the visit dictionary is byte-identical before and after** — the check that no un-save writes through to the other source | unit | C3, C5 |
| **3** Been fires only for known places, 20-min threshold, silent, revisit is a no-op | (a) a fixture entry whose `place_id` matches no `Place`; (b) a duplicate `place_id` with both kinds; (c) grep of the diff | (a) no row rendered, no crash; (b) exactly one entry, `.been` kept; (c) no confirmation UI and no user-facing prompt exists anywhere in this feature. **The 20-minute threshold and the "already-known place" guard are NOT verified in Phase 1 — there is no detector. Carried forward to the detector's own task and re-run at Phase 2** (§7) | unit + review | C4 |
| **4** Closed places save; badge distinct; never substitutes for the flag; updates on next render; never blocks the route action | (a) `Place` decoded from the shipped seed; (b) the row rendered for `neve-nachum-gutman-museum`; (c) `saved-places.json` + the visit fixture contents; (d) contrast of `BadgeOnSurface` on `BadgeSurface` | (a) exactly the two flipped ids decode `permanentlyClosed == true`, the other seven `false`; (b) the badge renders and the row still opens the modal, whose Directions button is enabled; (c) **neither persisted artifact contains any closed-state field** — this is what makes "updates on next render" true regardless of T-044; (d) ≥4.5:1 in both interface styles. **Not verified: the three-element worst-case row** (D9) and **the freshness of the column itself** (T-044, ownerless) | unit + UI test + manual | C1, C2, C9, C13 |
| **5** Degraded permission degrades, never breaks; no re-ask; no error copy | (a) grep of every new file in §2.1; (b) the app run on a simulator with location denied | (a) **no `CoreLocation` import, no authorization read, no permission request** anywhere in this feature's new files, and `VisitedPlacesStore` has no write path; (b) list opens, Saved rows render and save, no error copy, no system prompt. **Stated honestly: in Phase 1 the fixture populates regardless of permission, so "Been never populates when denied" is checked as the absence of any sensor path, not as runtime behaviour** — flagged for `product`, and re-run against the real detector at Phase 2 | review + manual | C4, C6 |
| **6** Empty and offline states are plain, not errors | (a) empty saved set + empty fixture; (b) the app in airplane mode | (a) the empty state renders with icon, line, and a CTA that dismisses the list — not an error string, not a spinner — **and its copy names what would fill the list** (how a place gets here: save one, or spend time at one), not only that the list is empty. **A string that states emptiness alone — "Nothing here yet." — FAILS this row**; (b) every row renders identically and a save made offline appears immediately. **No offline banner is asserted — none ships (D5)** | unit + manual | C10 |
| **7** Map accent binary, close zoom only, shape not colour alone, ≥44pt target preserved | (a) `isListed` vs. `entries` over the full fixture; (b) `PlaceLayer` rendered at both zoom sides of `showsNames`; (c) the annotation's button frame; (d) a greyscale render | (a) agree on every place, including the one in no source; (b) no ring at any zoom where no pin renders — same single gate, no second constant; (c) frame is exactly 44×44 with the ring applied and the ring is `.allowsHitTesting(false)`; (d) ringed and unringed pins are distinguishable with colour removed | unit + UI test + manual | C12 |
| **8** Row opens the place modal directly; nav-modal exclusivity; dismiss returns to an unchanged map | (a) row tap with no Hood sheet involved; (b) `chrome.toggle(.places)` with a Hood sheet open; (c) `toggle(.heat)` with the list open and a place modal stacked; (d) camera + `selectedHour` before/after a full open→row→dismiss→dismiss cycle | (a) `router.place` set, `router.hood == nil` — the Hood sheet is skipped; (b) `router.hood == nil` after the call; (c) both the list and the place modal are gone and `.heat` is presented, in one transition; (d) `MKCoordinateRegion` and `selectedHour` identical — neither is read or written by this feature | unit + manual | C11 |

*Row 6's "names what would fill the list" clause was restored by `product` at T-036's acceptance, 2026-08-03: this table had dropped it from PRD req 6 bullet 1, so `qa` tested the weaker bar and had nothing to fail against a shipped empty state that names nothing (L-009, L-018). It changes no requirement, schema, or contract — the PRD always said it. Fixing the shipped copy is `ios-developer`'s at T-036's rejection, not here.*

---

## 10. Risks and alternatives

| Risk | Mitigation / decision |
|---|---|
| `permanentlyClosed` lands on the seed path only and Phase 2 ships `false` everywhere | D1 — all three paths, non-optional, with a decode test per path (C1). The failure becomes a decode error with a designed fallback, not a wrong boolean |
| The fixture makes Been/Visited look verified when no detector exists | Named in §3.3, in `BuildPhase.visitsAreSeeded`, in the fixture's own `_note`, and in §9 rows 3 and 5, which say which bullets are *not* covered and where they get re-run. Not claimed as satisfied |
| Req 5 read literally is violated in Phase 1 — fixture rows appear on a denied-permission device | Stated openly (§9 row 5) rather than papered over. Gating the fixture on authorization was considered and rejected: it fakes a dependency the fixture does not have and breaks the demo on a denied simulator. **Flagged for `product`** |
| Un-save silently destroys a Been record | Structurally impossible — two storage locations, one write path each (§3.1), and §9 row 2 asserts the visit dictionary is unchanged across a toggle |
| A third derived store drifts from its two sources | Avoided by construction (D3). A function cannot be stale |
| `isListed` degrades pin rendering at Phase 2 scale | Contracted as an O(1) lookup, never a scan over `entries` (§4.3), with a test that the two agree. At a few hundred places this is not a measurable cost; if it ever is, the seam is one function |
| Adding a field to `PlacesCache` orphans an existing cache file | It cannot — Phase 1 never writes that file, and the decode-failure path already falls through to the seed. Proven by a test (C1), not assumed (§3.2) |
| `MapChromeState` is built twice, or differently, by T-032 and T-036 | **Restated at v2, after `trd-review` found v1's version of this row was false.** There is one owner (T-032 §4.1) and one shape; §4.5 reproduces it verbatim and C6 makes T-036's step a create-if-absent of *that exact type*, never a narrower one. T-036 adds no case, so there is nothing for T-032's unconditional C1 to restructure in either order. Residual risk: T-032's §4.1 changing after this was copied — §2.2 names diffing the two as a re-review step |
| The Places icon fading under its own surface reads as broken | **Retired 2026-08-04 (PAS-42).** The button no longer fades — it is a permanent nav-row member — so this risk has no subject. Its replacement is narrower: a never-fading button invites a re-tap that would dismiss the list, which `MapScreen.openPlacesList`'s `guard chrome.presented != .places` makes a no-op (D7). The list's three dismissal paths are unchanged |
| The row's density design can't be fully exercised until T-035 lands | D9, and §9 row 4 names the untested combination rather than passing it by construction |
| Row sort is not the sort anyone would choose | D4 — deliberate, reasoned against a real migration cost, flagged for `product`, one line to change |
| Req 4's "badge updates on next render" depends on a refresh nobody owns | Split honestly: the *architecture* half (never copy closed state into a personal record) is satisfied and checked (§9 row 4c); the *freshness* half is T-044's and is not claimed here |
| Device-local data is lost on reinstall | The PRD's own open question for Aviran, unchanged. This TRD does not create an anonymous server identity to solve it, and §3.4 says why the provenance half in particular should not become server state without its own review |

**Alternatives considered and rejected:** a single merged store owning all three provenances (destroys the record-preservation property the PRD requires, and would mean rewriting shipped accepted code — §3.1); a derived `@Observable` merge store (D3); `.sheet()` for the list container (covers the nav row — T-032 D2, reused); a swipe-to-unsave row action (design spec §2.1's Poka-Yoke reasoning — a gesture that sometimes deletes and sometimes relabels, adopted unchanged); recency sort with a versioned saved payload (D4); a client-side `MKMapItem` closed-state lookup (D6); building a real dwell detector in this task (D2, and the PRD's one-detector rule); reusing `BuildPhase.seedIsAuthoritative` for the fixture (§3.3 — different axis); a second zoom threshold for the ring (§4.9 — `showsNames` already gates it); shipping the offline banner (D5); adding `entryPath` to `DetailRouter` (D8 — derivable).

---

## 11. Build breakdown

Ordered. **Every step is `[iOS]`.** No `[Backend]`, no `[Algo/Data]` — see §1. C1–C5 carry no view work and are testable with no simulator; do them first.

| # | Step | Tag |
|---|---|---|
| C1 | `Place.permanentlyClosed` + decode on **all three** paths — `SeedFile.Entry`, `PlacesAPI.PlaceRow` and the `select=` string, `PlacesCache.CachedPlace` (§3.2, D1). Tests: shipped bundle decodes with 9 places and the right two flags; a live payload missing the column throws and falls back; an older cache payload fails to decode and falls through to the seed | **[iOS]** |
| C2 | `places-tel-aviv.json` — flip `kerem-carmel-spice-corner` and `neve-nachum-gutman-museum` to `permanently_closed: true`. Data only; leave every other field alone (T-042's `export_places.py` overwrites this file wholesale at Phase 2) | **[iOS]** |
| C3 | `PlaceProvenance` + `VisitKind` + `PlacesListComposition` (§4.1, §4.3) with the full test matrix: precedence, one-row-per-place, unresolvable-id skip, `isListed` agreement, deterministic sort (§9 rows 1, 2) | **[iOS]** |
| C4 | `VisitSourcing` + `BundledVisitSource` + `VisitedPlacesStore` + `place-visits-tel-aviv.json` + `BuildPhase.visitsAreSeeded` (§3.3, §4.2). Fixture authoring rule enforced by a test: ≥1 `been`, ≥1 `visited`, ≥1 place in no source; duplicate id keeps the higher kind; missing/corrupt file yields `[:]`, never a crash | **[iOS]** |
| C5 | `SavedPlacesStore.savedPlaceIDs` — the **only** change to that file. Shipped tests must pass unmodified (§4.2) | **[iOS]** |
| C6 | `MapChromeState` (§2.2, §4.5). **If `MapChromeState.swift` does not exist yet, create it exactly per T-032 §4.1 — all four cases, all four conformances, verbatim. If it already exists, add nothing: `.places` is already a member and this task modifies that file in neither direction.** Exclusivity unit test (`toggle` swaps rather than stacks; `toggle` on the presented surface dismisses) — the test is T-036's regardless of who wrote the type | **[iOS]** |
| C7 | `PlacesButton` in the bucket-2 chrome cluster beside `NearMeButton`; fade + `.allowsHitTesting(false)` driven by `chrome.isPresenting` (§2.4, D7) | **[iOS]** |
| C8 | `PlacesListOverlay` at z5 — drag handle, 44×44pt ✕, scrim tap, Reduce-Motion-aware transition (§4.5) | **[iOS]** |
| C9 | `PlacesListRow` — glyph, name, provenance word, closed badge with `nosign`; the reserved empty tourist-heavy slot with T-035's comment (§4.4, D9) | **[iOS]** |
| C10 | `PlacesListEmptyState` — icon + line + "Explore the map" CTA that dismisses (§4.7, §9 row 6) | **[iOS]** |
| C11 | Wire the surface into `MapScreen`: row tap → `router.openPlace`; `closeHood()` on open and `closePlace()` on leave (§4.6, D8); `VisitedPlacesStore.load()` as a fifth `.task`. Tests for §9 row 8 | **[iOS]** |
| C12 | `PlaceLayer.isListed` → dashed ring, `.allowsHitTesting(false)`, `", in your Places"` clause; 44pt-frame and greyscale checks (§4.9, §9 row 7) | **[iOS]** |
| C13 | `MutedOnSurface` (or reuse T-032's), `BadgeSurface`, `BadgeOnSurface` + token contrast tests, light and dark (§4.10, §9 row 4d) | **[iOS]** |
| C14 | `PlacesRowLabel` + its 3 × 2 matrix test (§4.8) | **[iOS]** |

**`trd-review` sign-off needed from: `ios-developer` + `ios-code-reviewer` only.** `developer`, `code-reviewer` and `data-engineer` have no step to review — this TRD writes no SQL, no RLS, no pipeline, and no algorithm.

**Three cross-checks worth one explicit pass at review:**
- **T-032's TRD** against §2.2/§4.5 and §2.4 — **diff §4.5's reproduced block against T-032's live §4.1 character by character** (that mismatch is what sent v1 back), and re-read D7 on which chrome bucket this button lives in (**v2.1: it is the nav row — D7 no longer corrects T-032's D1**). **One edit is owed to T-032's own TRD and is not made here** — its C1 would read better with a symmetric "no-op if `MapChromeState.swift` already exists with this exact shape." (A second edit was listed at v2 — correcting T-032's D1 prose so "the rest" excluded Places. **Withdrawn at v2.1:** PAS-42 put Places in `MapNavRow`, so D1 is right as written and that edit would introduce the error.) It belongs to T-032's in-flight v3 pass; that file had another session's uncommitted work in the shared tree when this revision was written, so touching it would have violated `CLAUDE.md` rule 2. **Not a blocker for T-036** — after v2, T-036 creates nothing T-032 would restructure.
- **T-042's TRD** against §3.2 — this task widens `PlacesAPI`'s `select=` to include `permanently_closed` and only that column; T-042's §4 shows the fully-widened select and its own reviewers should confirm the split is as its amendment table intends.
- **`product`** on D4 (sort), D5 (no offline banner), D7 (button placement and the fade consequence), and §9 row 5's honest statement that req 5's Been/Visited bullets are checked as absence-of-a-sensor-path in Phase 1, not as runtime behaviour.
