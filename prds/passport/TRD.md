# Passport — TRD

**Task:** T-037 · **Linear:** `PAS-28` · **Status:** v1 — ready for `trd-review`
**Owner:** architect · **Date:** 2026-08-03
**PRD:** [`passport.md`](./passport.md) (Draft v1)
**Design reference:** none. The pre-code design gate was retired 2026-08-02 (`BOARD.md` lifecycle section) and no Passport design spec was ever drafted, so nothing is lost by skipping it. `design/ux-flows.md` §2/§2.1/§5/§7 and `design/design-principles.md` are the standing references this TRD builds against; every visual call not covered there is tagged **[ASSUMPTION]** and is one line for the post-ship `designer` pass to overturn.
**Builds on:** [`prds/places-been-saved/TRD.md`](../places-been-saved/TRD.md) (T-036 — `VisitSourcing`, `VisitedPlacesStore`, `VisitKind`, the `Place` amendment pattern), [`prds/time-slider/TRD.md`](../time-slider/TRD.md) (T-032 — `MapChromeState`, `MapNavRow`, the z-order table), [`prds/hood-place-detail/TRD.md`](../hood-place-detail/TRD.md) (T-033 — `Place`, `PlaceCatalog`, `PlacesAPI`, `PlacesCache`, `BuildPhase`). None is restated.
**Adjacent, not built here:** [`prds/places-dataset/TRD.md`](../places-dataset/TRD.md) (T-042) owns `public.place_types`, `places.place_type` and migration `004_places.sql`. [`prds/hood-dataset/TRD.md`](../hood-dataset/TRD.md) (T-040) owns `hoods.designated_for_progression` and migration `003`/`006`.

---

## 1. Context

Read the PRD first. Nothing here restates it. This document decides what it leaves open and pins the contracts the build agents work against.

**What this feature is, architecturally: a read-only view with no store of its own.** Passport persists nothing, fetches nothing, and observes nothing. Every pixel it renders is a pure function of three things that are already loaded before the Profile button can be tapped — `PlaceCatalog.allPlaces`, `MapScreen`'s `[Hood]`, and T-036's `VisitedPlacesStore.visits`. That is not a simplification for Build Phase 1; it is the design, and it is what makes the PRD's *"stickers are derived from the Been rows — no second store of truth"* true by construction rather than by discipline.

**Surface: two agents, not one. Confirmed, not assumed.**

- **`[iOS]`** — C1–C13, the bulk.
- **`[Algo/Data]`** — **A1** (the `place_type` → sticker-shape mapping) and **A2** (which Hoods are designated for progression). Both are dataset content, not client code that happens to live in a JSON file: A1's value set is explicitly T-042's step B1 (*"Propose the initial `place_type` enumeration and its `sticker_shape` mapping, for Aviran's ratification. Not invented by whoever writes A1"* — the same rule applies to whoever writes the Swift), and A2 must go through `database/data/hoods-tel-aviv.source.json` + a `build_hoods.py` regeneration rather than a hand-edit of the generated client bundle (**L-024**). This is the same shape as T-035's own A1 step and is routed the same way.
- **No `[Backend]` step.** This TRD writes no SQL by hand, adds no column, no RLS policy and no endpoint. A2 *regenerates* the already-unapplied `006_hoods_tel_aviv_data.sql` as a side effect of re-running the generator; that file stays unapplied and Aviran-gated exactly as it is today.

**`trd-review` routes to `ios-developer` + `ios-code-reviewer` (C1–C13) and `data-engineer` + `code-reviewer` (A1, A2)** — see §10.

**Open items resolved here:**

| # | Open item | Source | Call | Where |
|---|---|---|---|---|
| 1 | `place_type` does not exist on the `Place` model | T-042 §2.2 amendment table (`place_type` → T-037) | Added as a **non-optional `String`, not a Swift enum**, threaded through all three `PlaceCatalog` source paths | §3.2, **D2** |
| 2 | Nothing maps a `place_type` to a sticker shape on the client | T-042 §4.2 "client half, built by T-037" | Closed `StickerShape` enum + a **bundled, never-fetched** registry + a build-time totality test | §3.3, **D3**, **D4** |
| 3 | The Local threshold is a number nobody has stated | PRD Open questions ("cannot ship without them") | One app-wide constant, `LocalStatus.threshold`, **provisional value 2 [ASSUMPTION]**, flagged for Aviran. Not per-Hood, not a view constant | §4.2, **D6** |
| 4 | Which Hoods are designated is a number nobody has stated | PRD Open questions | Provisional Phase-1 set = the three Hoods that have curated places, seeded through the generator, flagged for Aviran | §3.4, **D7** |
| 5 | How a Been place is attributed to a Hood | PRD Open technical questions | `place.hoodID`, read from the dataset. **Never a client-side polygon ray-cast** | §3.5, **D5** |
| 6 | Whether progress computes on device or server | PRD Open technical questions | On device, always, in V1 — there is no user identity to compute it against on a server | §3.1 |
| 7 | Whether earning a sticker surfaces in the moment | PRD req 6 bullet 2; `ux-flows.md` §9 Q13 | **Nothing ships.** Stickers are derived on read, so req 6's other two bullets are satisfied by there being no event to fire | §4.5, **D8** |
| 8 | Whether the "city page" needs a `city` field | PRD req 3 last bullet | **No.** One city, one header, no grouping axis built. Adding `city` to `Place` would break T-042's one-field-per-task rule for a feature V1 does not have | §4.4, **D11** |
| 9 | Req 7's *"VoiceOver label naming the place and its type"* vs. T-042 §4.4's *"no user-facing surface renders `place_type`"* | found by reading the two documents against each other | The label names **what the sticker depicts**, from a client-side `StickerShape.spokenName` — never the raw `place_type`. **Flagged for `product`**, this is a deviation from the PRD's literal wording | §4.7, **D12** |

---

## 2. Architecture

### 2.1 Module layout

```
Passenger/
  Passport/
    PassportComposition.swift   new — pure stickers/progress functions (§4.1, D1)
    LocalStatus.swift           new — the one threshold + the Local predicate (§4.2, D6)
    PassportSurface.swift       new — the z5 modal card + dismissal paths (§4.5)
    PassportAlbum.swift         new — sticker grid + empty state (§4.4)
    PassportStickerView.swift   new — one sticker (§4.4)
    PassportProgressList.swift  new — per-Hood rows + overall line (§4.3)
    PassportLabels.swift        new — pure VoiceOver string composition (§4.7)
  Places/
    Place.swift                 MODIFIED — + placeType (D2)
    PlaceCatalog.swift          MODIFIED — decode placeType on all three paths (registry is not its job)
    PlacesAPI.swift             MODIFIED — select= and PlaceRow gain place_type
    PlacesCache.swift           MODIFIED — CachedPlace gains placeType
    StickerShape.swift          new — closed shape enum, .generic fallback, spokenName (D3, D12)
    PlaceTypeRegistry.swift     new — place_type → StickerShape, bundled, sync (D4)
  Map/
    MapScreen.swift             MODIFIED — hosts the .profile surface and the button
    MapNavRow.swift             MODIFIED — + ProfileButton (T-032's container; C7 is blocked on its C2)
    ProfileButton.swift         new — nav-row button, icon-only (D9)
    MapChromeState.swift        NOT MODIFIED — T-032's type (§2.2)
Resources/
  place-types-tel-aviv.json     new — the provisional shape registry (A1, [Algo/Data])
  hoods-tel-aviv.json           REGENERATED by build_hoods.py — designated flags (A2, [Algo/Data])
database/data/
  hoods-tel-aviv.source.json    MODIFIED — designatedForProgression on three Hoods (A2)
database/migrations/
  006_hoods_tel_aviv_data.sql   REGENERATED as a side effect of A2. Still unapplied, still Aviran-gated
```

Xcode synchronized file groups are on; dropping files in the folder is enough, no `project.pbxproj` edit.

### 2.2 Shared files — who owns what

Four files in §2.1 are shared with in-flight tasks. None is co-authored here.

**Tree state as of 2026-08-03, read rather than assumed.** T-036's build is live and **uncommitted** in the shared `passenger-code` working tree: `Passenger/Map/MapChromeState.swift`, `Passenger/Places/VisitedPlacesStore.swift`, `BundledVisitSource.swift`, `PlaceProvenance.swift`, `place-visits-tel-aviv.json` are all present as untracked files, and `Place.swift` already declares `let permanentlyClosed: Bool`. `MapNavRow.swift` does **not** exist — T-032's C2 has not landed. The conditional clauses below are written so they hold whether or not that in-flight work commits.

| File | Owner | T-037's rule |
|---|---|---|
| `MapChromeState.swift` | **T-032 §4.1** | Consume only. `.profile` is already a member of `NavSurface`. **Verified present in the working tree on 2026-08-03**, created by T-036's build, four cases, contents matching T-032 §4.1. **If it is there, add nothing. If T-036's work never lands, create it exactly per T-032 §4.1 — all four cases, all four conformances, verbatim** (reproduced at §4.6). T-036's C6 clause word for word, and for the same reason |
| `MapNavRow.swift` | **T-032 C2/D1** | Add one button to an existing container. **Do not create this file** — its layout rules (separate side-by-side buttons, no shared capsule/bar/divider, icon-only) are T-032's D1/D6 and are not re-derived here. **Confirmed absent on 2026-08-03, so C7 is blocked on T-032's C2**; every other step builds regardless |
| `Place.swift` / `PlaceCatalog.swift` / `PlacesAPI.swift` / `PlacesCache.swift` | T-033, amended one field per reading task (T-042 §2.2, D5) | T-036 has already added `permanentlyClosed` to all four in the working tree. T-037 adds `placeType` beside it. **The two amendments are additive and independent** — different field, same three decode paths, and the `select=` string accumulates both columns. **C1 adds its field to whatever is in the tree; it never re-derives the file from `HEAD`**, which would silently revert T-036's uncommitted work. §9 row 3(b) asserts both fields decode together, not just this task's |
| `Assets.xcassets/MutedOnSurface.colorset` | T-032 C9 / T-036 C13 | Reuse. **Present in the working tree on 2026-08-03** (T-036's build). Do not create a second token with a different value (§4.8) |

### 2.3 Boundaries — who is allowed to know what

- **`Passport/` knows no persistence, no network, and no `CoreLocation`.** There is no store, no cache file, no fetch and no authorization read anywhere in this feature. §9 rows 1 and 8 check that as an absence in the diff, not as a promise.
- **`PassportComposition` is a free function over value types** — it takes `[Place]`, `[Hood]` and `[Place.ID: VisitKind]`, never a store, never an environment object. Same construction and same reason as T-036's `PlacesListComposition` (its D3): a derived `@Observable` store computed from three other stores has an invalidation problem; a function cannot go stale.
- **`Places/` still knows no SwiftUI.** `StickerShape.symbolName` is a `String`, exactly as `PlaceCategory.symbolName` already is.
- **`Passport/` does not know map geometry.** It never imports `MapKit`, never touches `HoodHitTester`, and attributes a place to a Hood by reading `place.hoodID` (D5).
- **Nothing in `Passport/` reads or writes `camera` or `selectedHour`.** That is what makes PRD req 2's last bullet structural rather than tested behaviour.

### 2.4 Chrome placement — Profile *is* a nav-row button

`ux-flows.md` §2's Primary table: *"Profile button (added 2026-07-30) — Chrome icon, **the 3rd of the 3 side-by-side nav buttons**."* So unlike Places (T-036's D7 correction), Profile sits exactly where T-032's D1 anticipated. T-032's z-order table applies unchanged:

| z | Layer | T-037's contribution |
|---|---|---|
| 0–4 | Map, edge zones, scrim, bucket-2 chrome | **Nothing.** No map-layer change of any kind — Passport draws nothing on the map |
| 5 | Modal card | `PassportSurface` |
| 7 | `MapNavRow` | **`ProfileButton` joins the row.** Stays visible and hit-testable while Passport is open, so a direct switch to search or heat needs no dismiss-first step |

Because the button lives at z7 it does *not* fade under its own surface, so `toggle(.profile)` on the open surface is reachable by tap — a fourth dismissal path T-036's Places list does not have. That asymmetry is `ux-flows.md`'s, not this TRD's.

**Icon-only, no caption** — `ux-flows.md`'s 2026-08-02 founder-direct addendum covers all four nav icons, and T-032's D6 states it for the heat button. Build it icon-only from the start; the `accessibilityLabel` still names it.

---

## 3. Data model

### 3.1 Passport stores nothing. That is the data model.

There is no Passport table, no Passport JSON file, no Passport `UserDefaults` key, and no Passport field on any existing record. Stickers and progress are computed at render time from data three other features already own:

| Input | Owner | Read as |
|---|---|---|
| `[Place]` (incl. `hoodID`, `placeType`) | `PlaceCatalog` (T-033, amended here) | `allPlaces` |
| `[Hood]` (incl. `designatedForProgression`) | `HoodCatalog` (T-040, already shipped) | `MapScreen`'s `hoods` |
| `[Place.ID: VisitKind]` | `VisitedPlacesStore` (T-036) | `visits` |

**PRD open technical question answered: progress computes on device, in V1, always.** Not because on-device is cheaper, but because there is no user identity on the server to compute it against — the app has no accounts, and creating one to hold a progression counter would be a new PRD with its own scope-gate pass. This also settles a privacy question that the PRD does not raise: per-Hood Been counts uploaded per device would be a coarse movement log, which is exactly what T-036 §3.4 forbids for the provenance rows they derive from.

**Consequence, stated rather than discovered:** three of the PRD's requirements are satisfied by *absence of code* rather than by behaviour, and §9 says so per row instead of dressing them up as runtime checks — req 1 (no social surface), req 6 bullet 3 (a sticker earned while the app was closed is simply there), and req 8 (degraded permission and offline both open the screen).

### 3.2 `placeType` — one field, three source paths (D2)

`Place` gains `let placeType: String`. The threading is identical in shape to T-036's `permanentlyClosed` (its §3.2 / D1) and identical in reasoning: adding it to the seed path alone would compile, pass every Phase-1 test, and ship a wrong value the moment `BuildPhase.seedIsAuthoritative` flips.

| Path | Change | If the field is absent |
|---|---|---|
| Bundled seed (`SeedFile.Entry`) | declare `place_type`, non-optional | File fails to decode → `.unavailable`, empty catalog. Loud, and C1's shipped-bundle decode test makes it a build-time failure |
| Live (`PlacesAPI.PlaceRow` + the `select=` string) | add the column to both | Payload decode throws → existing cache → seed. Already-designed fallback, nothing new |
| Disk cache (`PlacesCache.CachedPlace`) | add, non-optional | An older cache file fails to decode → `loadIfPresent()` returns `nil` → seed. Correct, and needs no migration or schema version — Build Phase 1 never writes that file at all |

**The field is a `String`, not a Swift enum (D2).** T-042 deliberately made `place_types` a *table* rather than a Postgres enum so that adding a value is an insert, not a migration (its §8). A closed Swift enum on `Place` would undo that on the client: the first server-side insert of a new type would drop every row carrying it at the decode boundary. The closed set lives one hop later, on `StickerShape`, where an unknown value degrades to a generic shape instead of deleting a place.

**The shipped bundle already carries this field** on all nine rows (`place_type`: `bar`, `cafe`, `landmark`, `restaurant`, `market`, `museum` — verified against `Passenger/Resources/places-tel-aviv.json`, not assumed from T-042's text). No fixture authoring is needed for C1.

### 3.3 Sticker shapes — a closed client enum behind an open server vocabulary

```
places.place_type (String, open, server-owned)
        │  PlaceTypeRegistry — bundled JSON, A1's content
        ▼
   StickerShape (closed Swift enum, .generic fallback)
        │  symbolName / spokenName
        ▼
      one sticker
```

Two guarantees, one on each hop, together satisfying PRD req 3's last two bullets:

- **Every registered `place_type` resolves to a real shape** — C2's totality test walks every key in the shipped registry and asserts it maps to a non-`.generic` `StickerShape` case whose `symbolName` resolves to a real symbol. This is the build-time gate; the enum alone is not, because the key is a `String`.
- **Every `place_type` present in the shipped places bundle is in the registry** — C12's invariant test. Without this, a place could earn a generic sticker while the registry still passed its own totality check.
- **An unregistered value renders `.generic`, never nothing.** Defence in depth against a data/app skew, not a contract: the two tests above make it unreachable in a shipped pair.

### 3.4 The registry is bundled and never fetched (D4)

T-042 §4.5 offers `GET /rest/v1/place_types?select=id,sticker_shape`. **This client does not call it, in Phase 1 or Phase 2.**

The reason is not Build Phase 1 scope — it holds permanently for V1. A `sticker_shape` key is only useful if the app binary contains something to draw for it. A new key arriving over the wire that the shipped binary has never heard of renders `.generic` no matter how it arrived, so fetching the mapping buys a key the app cannot draw. Bundling it means the shape vocabulary and the shape assets ship in the same artifact, always in sync, and the totality test becomes a real build gate instead of a runtime hope. `places.place_type` still arrives per place over the wire at Phase 2 — that part must be live, because it is per-row data. Only the mapping is frozen into the build.

**This is a deviation from T-042 §4.2/§4.5's implied client fetch and is flagged for T-042's reviewers.** It removes a request, a cache field and a skew class from that task's contract and adds nothing to it. If it is overruled, the change is one loader conformance and one `PlacesAPI` method; nothing else in this TRD moves.

`Resources/place-types-tel-aviv.json` — **A1's content, `data-engineer`'s to author, provisional until Aviran ratifies T-042 B1**:

```json
{
  "schemaVersion": 1,
  "_note": "PROVISIONAL Build-Phase-1 mapping. The ratified vocabulary is places-dataset (T-042) step B1, Aviran-gated. Regenerate/replace, do not extend by hand.",
  "types": { "<place_type>": "<sticker_shape>" }
}
```

The Phase-1 file must cover exactly the six `place_type` values in the shipped places bundle, and no more — a key for a type no place carries is untestable and invites drift.

**It loads synchronously and belongs to nobody else.** `PlaceTypeRegistry` decodes a few hundred bytes on first access via a `static let`, not through `PlaceCatalog.load()` and not through a `.task`. Two reasons: it is bundled in every build phase, so hanging it off `PlaceCatalog`'s seed branch would leave it unloaded the moment `seedIsAuthoritative` flips to `false`; and an async load would add a launch-path dependency to a screen that is not on the launch path. A missing or corrupt file yields an empty map, never a crash — and C2's totality test means that cannot reach a shipped build.

### 3.5 Hood attribution and the designated set

**Attribution is `place.hoodID` (D5).** T-042's C-HOOD-1 makes "each place is contained by exactly one Hood" a dataset invariant enforced by `validate_dataset.py`, and the column is the result of that check. The client re-running a ray-cast would be a second, weaker implementation of a predicate that already has three (`hood-dataset`'s Python, T-043's `plpgsql`, `HoodHitTester`'s tap test) — and the two could disagree, which is the class of bug T-042 §4.1 spends a paragraph warning about.

This also answers the PRD's open question *"how a Been place is re-attributed if a Hood polygon later changes"*: it is re-attributed **server-side, at dataset export**, and arrives already attributed. The client never recomputes it, so there is no migration and no stale-attribution state to design.

**The designated set (A2, D7).** `Hood.designatedForProgression: Bool` already exists on the shipped model and already decodes from the bundle — **and is `false` on all 24 Hoods**, because T-040's PRD explicitly scoped populating it out (*"not this task's to populate"*). Nobody owns it today. Left as-is, Passport's entire progression half renders empty on device, and PRD req 4 has nothing to check.

A2 seeds a provisional Phase-1 set: **`florentin`, `kerem-hateimanim`, `neve-tzedek`** — derived, not invented. They are the only three Hoods with curated places in the shipped dataset, so they are the only three where progress is expressible at all, and each holds three places, which keeps them above the provisional threshold of 2 (§4.2). Every other Hood stays `false`.

**The edit goes into `database/data/hoods-tel-aviv.source.json` and `build_hoods.py` is re-run** — never a hand-edit of `Passenger/Resources/hoods-tel-aviv.json`, which is generated (L-024, and T-035's A1 hit exactly this). The re-run also rewrites the unapplied `006_hoods_tel_aviv_data.sql`; that file stays unapplied and Aviran-gated. **`build_hoods.py` stamps `generatedAt` from the wall clock**, so the regenerated bundle never diffs clean against the committed one — reviewers and `qa` must normalise that field before comparing (T-035's TRD §10 found this; it is not re-derived here).

**A2 is the second task to edit this source file, and must not clobber the first.** T-035's A1 landed on 2026-08-03 and set `isTouristTrap` on three Hoods (`florentin: true`, `kerem-hateimanim: true`, `ramat-aviv: false`), regenerating both the bundle and `006` from the same source. A2 touches a **different field on the same rows**, so it is additive — but it must edit the *current* source and re-run the generator against it, never regenerate from a copy taken before A1. Two of A2's three designated Hoods are also A1's two flagged Hoods; that overlap is coincidental (both sets were derived from where the curated places are) and carries no coupling. Verify after regeneration that the diff shows only `designatedForProgression` lines plus `generatedAt` plus the migration's source-digest comment.

### 3.6 Location & privacy

Passport is the most sensitive *view* in the app — it is a legible summary of where a person has physically been — while holding none of the underlying data. Three properties keep it that way, and each is checkable:

- **It writes nothing, anywhere.** No file, no key, no column. §9 row 1 greps for it.
- **It transmits nothing.** No network call exists in this feature, so there is no path by which a Been set, a Hood count, or a Local status could leave the device. This is also what makes req 1's "no social surface" structural: there is no wire over which another person's Passport could arrive.
- **It reads T-036's record and adds nothing to it.** The device-local shape stays `{place_id, kind, first_observed_at}` (T-036 §3.4). Passport needs no coordinate, no dwell duration, no second timestamp — and this TRD deliberately does not ask for any, so the real detector inherits the same minimal shape T-036 pinned. **`first_observed_at` is not read by this feature either**, which is why the album's ordering is deterministic-by-name rather than chronological (§4.4).

---

## 4. Contracts

### 4.1 The composition — pure functions, no store (D1)

```swift
struct PassportSticker: Identifiable, Sendable, Equatable {
    let place: Place
    let shape: StickerShape
    var id: Place.ID { place.id }
}

struct HoodProgress: Identifiable, Sendable, Equatable {
    let hood: Hood
    let beenCount: Int
    var id: Hood.ID { hood.id }
    var isLocal: Bool { LocalStatus.isLocal(beenCount: beenCount) }
}

enum PassportComposition {
    /// One sticker per Been place (PRD req 3). `.visited` yields none — the
    /// filter is on `VisitKind`, so "a Visited place earns no sticker" has no
    /// branch anyone can get backwards. `visits` is keyed by place id, so
    /// "one Been place, exactly one sticker, revisits add none" is structural.
    /// A visit id with no matching `Place` is skipped, not defaulted.
    /// Name-ascending, id-tiebroken (§4.4).
    static func stickers(places: [Place], visits: [Place.ID: VisitKind], registry: PlaceTypeRegistry) -> [PassportSticker]

    /// Designated Hoods only (PRD req 4). Undesignated Hoods are absent from
    /// the output entirely, not present with a zero — the [ASSUMPTION] the PRD
    /// carries, made structural so no view can accidentally render them.
    /// Name-ascending.
    static func progress(hoods: [Hood], places: [Place], visits: [Place.ID: VisitKind]) -> [HoodProgress]

    /// PRD req 4 bullet 2. `false` when the designated set is empty — an empty
    /// `allSatisfy` is `true`, and "Local everywhere" with nowhere designated
    /// is the one answer that must never render.
    static func isOverallLocal(_ progress: [HoodProgress]) -> Bool
}
```

`beenCount` is `places.filter { $0.hoodID == hood.id && visits[$0.id] == .been }.count`. Nine places in Phase 1, a few hundred at Phase 2 scale, run once per render of a screen that opens on an explicit tap — this does not need memoising, and if it ever does the seam is one function.

### 4.2 The Local threshold (D6)

```swift
/// PRD req 4: "read from configuration, not hardcoded per Hood." One value,
/// one declaration site, app-wide. There is no per-Hood override and no code
/// path that can introduce one.
enum LocalStatus {
    /// **[ASSUMPTION] — provisional. Aviran's or `data-engineer`'s to set.**
    static let threshold = 2
    static func isLocal(beenCount: Int) -> Bool { beenCount >= threshold }
}
```

**"Configuration" here means one Swift constant, not a plist or a server value, and that is a deliberate narrowing of the requirement.** A server-side config table does not exist and building one would be a `[Backend]` step for a number that changes at most a handful of times before launch; a plist would put a launch-blocking product number in a file `AppConfig` documents as developer-local and gitignored. One constant in one file satisfies what req 4's bullet is actually guarding against — a threshold smeared across Hood records or view code — and is one line to move if it later needs to be remote.

**Why 2, provisionally.** Not a product judgement: it is the value that makes the most states observable against the data that actually ships. With T-036's fixture (two `been` places, both in `kerem-hateimanim`) and A2's three designated Hoods, a threshold of 2 puts `kerem-hateimanim` at Local, the other two at a plain zero state, and overall Local at not-reached — the Local, partial-zero and overall-not-reached states all reachable on a real device, with only overall-Local-reached left to unit tests (§9 row 4). It is also at or below the curated place count of every designated Hood (3 each), so no Hood is Local-unreachable by construction, which is the condition `validate_dataset.py` checks and currently skips while the threshold is unknown. **Flagged for Aviran, one line to change.**

### 4.3 The progress list

| Element | Contract |
|---|---|
| Row, per designated Hood | `hood.name`, then progress **as numerals against the threshold** — `"2 of 2"` — never a bar alone and never colour alone (`design-principles.md` §3, PRD req 5) |
| Local state | A word plus a glyph, both present: the row reads Local in text. No colour-only, no badge-only |
| Zero state | `"0 of 2"`, plain. **Never a lock glyph, never an error tone, never a teaser** (PRD req 5 bullet 2) |
| Overall line | One line stating whether Local is reached everywhere. Renders only when at least one Hood is designated |
| Undesignated Hoods | Absent. Not rendered at zero (§4.1) |
| Retired tier names | **None exists to render.** `Tourist`/`Wanderer`/`Regular`/`Insider`/`Native`/`Legend` appear in no type, no string and no asset in this task; §9 row 4 greps the whole client for them, not just the diff |

No progress bar is built. A bar would be the colour/shape-only failure mode req 5 exists to prevent, and adding one beside the numerals is a post-ship `designer` call, not a build-time one.

### 4.4 The album

One sticker per Been place, laid out in a `LazyVGrid`, filed under a single city header (D11).

| Element | Contract |
|---|---|
| Sticker | `Image(systemName: shape.symbolName)` in a filled shape container, sized ≥44pt. Not independently tappable in V1 — the whole grid is a static display, so nothing inside it can become a sub-44pt target |
| Sticker label | `PassportLabels.sticker(...)` (§4.7). **Never image-only** (PRD req 7) |
| City header | One static string. **[ASSUMPTION]** `"Tel Aviv"` |
| Empty state | Icon + one line naming what earns a sticker + no CTA that leaves the screen. Plain, never an error, never a spinner (`design-principles.md` §4, PRD req 5 bullet 3) |
| Order | **Name-ascending, id-tiebroken** |

**Why not chronological order,** which is what a real album would want: T-036's device-local record carries `first_observed_at`, but its Build-Phase-1 fixture does not populate it and `VisitedPlacesStore.visits` is a `[Place.ID: VisitKind]` — the timestamp is not on the seam Passport reads. Asking T-036 to widen that seam would change a contract that has already cleared `trd-review`, for an ordering no P0 requirement names. Name-ascending is deterministic, which is what makes §9 row 3 a falsifiable check at all, and it is one line to change when the real detector makes the timestamp available. **Flagged for `product`.**

**D11 — no `city` field is added to any model.** `Place` and `Hood` carry no `city` today; the bundles carry it only as a file-level key. V1 has exactly one city, so the album renders under exactly one header from one constant and no grouping axis is built. Adding `city` to `Place` would also break T-042's one-field-per-reading-task rule (§2.2), which this task is already spending on `place_type`. When a second city exists, that task adds the field and the grouping; §9 row 3 checks that nothing here pretends otherwise.

### 4.5 In-the-moment surfacing does not ship (D8)

`ux-flows.md` §9 Q13 is open — whether a sticker or milestone surfaces in the moment, and whether it exists at all — and PRD req 6 bullet 2 explicitly leaves it as a design call. **Nothing ships.**

This is not a deferral, it is what makes req 6 pass. Stickers are *derived on read*: there is no moment at which one is "earned," because no code runs when a visit is recorded — there is only a dictionary that is larger the next time the screen opens. So req 6 bullet 1 ("no modal, full-screen takeover, or blocking celebration fires") and bullet 3 ("a sticker earned while the app was closed is present next time Passport opens, with no catch-up animation") are both true because there is no event and no animation in the system at all. Building a toast would mean building the event first, which is the thing req 6 is protecting the map from.

**Flagged for `product` as a deliberate non-build**, same posture as T-036's D5. If Q13 later resolves toward a toast, it needs the local-QA toast's presenter and belongs in the task that owns the detector, not here.

### 4.6 The container

`PassportSurface` is a `ZStack` layer at T-032's z5 — **not `.sheet()`**, same reason and same construction as T-032's D2 and T-036's §4.5: a system sheet covers the nav row and breaks `ux-flows.md` §2.1's direct-switch rule.

```swift
// T-032 §4.1, verbatim. T-037 does not modify this type.
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

**Diff this block against T-032's live §4.1 at review** — a mismatch here is what sent T-036's v1 back.

- **Dismissal paths:** drag handle past a threshold, a 44×44pt ✕, scrim tap, and (unlike Places) a second tap on the Profile button, which stays live at z7 (§2.4).
- **On open, `router.closeHood()`; on leave, `router.closePlace()`** — T-036's D8, inherited rather than re-derived. The shipped `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` makes a nav-row tap reachable while a Hood sheet is up, so a `NavSurface` presented under a system sheet is a reachable state unless it is closed structurally. **`DetailRouter` is not modified by this task.**
- **Passport opens no sheets.** No sticker and no Hood row is tappable in V1, so unlike T-036 there is no path from this surface into a depth-1 modal. That is a deliberate omission, not an oversight — PRD req 4 asks the screen to *show* progress, and a tappable Hood row would need a destination no requirement names.
- Entrance/exit honours Reduce Motion by collapsing to 0 duration, never by skipping the state change.
- **Transient state survives a nav switch** (`ux-flows.md` §2.1): trivially true here — Passport has no transient state. Scroll position is not persisted and no requirement asks for it.

### 4.7 VoiceOver (D12)

```swift
enum PassportLabels {
    /// "Dr Shakshuka, restaurant sticker"  ← shape word, never the raw place_type
    static func sticker(placeName: String, shape: StickerShape) -> String

    /// "Kerem HaTeimanim, 2 of 2 places, Local reached"
    /// "Florentin, 0 of 2 places, not yet Local"
    static func hoodProgress(hoodName: String, beenCount: Int, threshold: Int, isLocal: Bool) -> String

    /// "Local in every neighbourhood" / "Local in 1 of 3 neighbourhoods"
    static func overall(localCount: Int, designatedCount: Int) -> String
}
```

Pure and unit-tested over the full matrix — no simulator, no VoiceOver session needed to prove the strings. Clause order follows `map-rendering-spec.md` §7's established construction.

**D12 — the sticker label names what the sticker depicts, not the `place_type`.** PRD req 7 bullet 1 asks for *"a VoiceOver label naming the place and its type."* T-042 §4.4 states that no user-facing surface renders `place_type` and that its only user-visible consequence in V1 is a sticker's shape — and a VoiceOver label is a user-facing surface. The two cannot both be satisfied literally.

Resolved toward parity: a sighted user sees a *shape*, so a screen-reader user should hear what that shape is. `StickerShape.spokenName` is a client-side word per case — the same idiom as `PlaceCategory.displayName`, which is documented as *"the only place a user-facing category string exists."* The word lives on the client enum and **not** in the registry file or in `place_types`, so T-042 §3.1's "no display string on the server, because a display string invites a surface to render it" stays intact. Because C2's totality test guarantees every registry key resolves to a `StickerShape` case, every sticker has a spoken word by construction.

**Flagged for `product`** — this is a stated deviation from req 7's literal wording, not a silent reinterpretation, and it is the only reading found that does not break one of the two documents.

Per-Hood status is announced as text including the count and whether Local is reached (req 7 bullet 2) — that is `hoodProgress` above, and it is the same string the row renders visually, not a separate one that could drift.

### 4.8 Colour tokens

**None are created.** The surface reuses `Surface`, `MutedOnSurface` (declared by T-032's C9 / T-036's C13 — reuse whichever landed, do not create a third) and the shipped `AccentColor`. Sticker fills use `AccentColor` at a tint; the Local/not-Local distinction is carried by **text plus glyph**, never by colour, so no new pair needs a contrast token. §9 row 5 checks the greyscale render.

---

## 5. Flow

**Cold launch.** Nothing new. `MapScreen.task` already fans out its loads and T-036 adds `VisitedPlacesStore` to them. **Passport adds no `.task` and no launch cost at all** — its only new input, `PlaceTypeRegistry`, is a synchronous `static let` decoded on first access, which happens the first time a sticker renders (§3.4).

**Open Passport.** Tap `ProfileButton` → `router.closeHood()` → `chrome.toggle(.profile)` → scrim at z3, bucket-2 chrome fades at z4, `PassportSurface` slides in at z5, nav row stays live at z7. `PassportComposition.stickers` and `.progress` run once per render pass over already-loaded data. No fetch, no spinner, no loading state exists to design.

**Dismiss.** Any of the four paths → `chrome.dismiss()` → `router.closePlace()` on leave → the map is exactly as it was. `camera` and `selectedHour` are neither read nor written anywhere in this feature.

**Switch surfaces.** Tap heat or search while Passport is open → `chrome.toggle(...)` → one transition, no intermediate empty frame, no state to preserve.

**Error paths.** Missing or corrupt registry → empty map → every sticker renders `.generic`, the screen still opens (and C2's build-time test means this cannot reach a shipped build). Missing or corrupt visit fixture → T-036's empty dictionary → no stickers, every Hood at zero, the plain empty state. `PlaceCatalog` `.unavailable` → no places → no stickers and no progress rows; the empty state renders. **None of these crash and none shows an error surface.**

---

## 6. Third-party / dependencies

**None added.** No package, no account, no cost, nothing Aviran-gated at the dependency level. `LazyVGrid`, `Image(systemName:)`, `JSONDecoder` and `@Observable` are all platform. `passenger-code/README.md`'s "no third-party packages until a TRD justifies one" stays intact.

**Salvage.** `SALVAGE.md` has nothing reusable here (the PRD says so, and the archive at `~/APE Studio/locali` is not reachable from this workspace anyway — the same gap T-031/T-032/T-036 hit). `Services/AuthService.swift` is BURN and nothing here reopens it. **`ios-developer` should not block on salvage access.**

**Task dependencies:**

| Depends on | For | If it has not landed |
|---|---|---|
| T-036's C3/C4 (`VisitKind`, `VisitedPlacesStore`) | The whole Been signal | **Hard block on C4 onward.** Present in the working tree on 2026-08-03 but uncommitted. No fallback is designed and none should be — a private visit fixture here would be the second detector T-035 and T-036 both refuse to build |
| T-036's C1 (`Place` amendment) | Nothing. Independent field on the same files | Already landed in the tree; C1 adds beside it (§2.2) |
| T-032's C1 (`MapChromeState`) | C6 | Already present via T-036's build; create-if-absent otherwise (§4.6) |
| T-032's C2 (`MapNavRow`) | **C7 only** | **Confirmed absent 2026-08-03 — C7 waits.** C1–C6 and C8–C13 build regardless |
| T-035's A1 (`hoods-tel-aviv.source.json`) | A2 edits the same file | Already landed. A2 edits a different field on top of it, never a stale copy (§3.5) |
| T-042 A1/B1 (`place_types`, ratified vocabulary) | Phase 2 correctness of A1's provisional file | Phase 1 ships A1's provisional mapping, labelled as such |

---

## 7. Rollout & migration

- **No feature flag.** The button and its surface arrive together; the off-state of a flag would be a nav button that opens nothing, which is exactly the dead control T-032's D1 refuses to ship.
- **No new `BuildPhase` constant.** `placeType` rides `seedIsAuthoritative` because it is the same axis (bundled catalog data vs. the server) and flips at the same moment. This is a deliberate contrast with T-036's `visitsAreSeeded` and T-034's `eventSeedIsAuthoritative`, both of which needed their own constant because their axis genuinely differed (fixture-vs-sensor, events-vs-places phase). Adding a third here would be cargo-culting the pattern past its reason.
- **No persisted-state migration.** This feature writes nothing. `places-cache.json` gains a field and an older file simply fails to decode and falls through to the seed — the designed behaviour, and never written in Phase 1 anyway.
- **No backend deploy and no Aviran-gated apply step is created.** A2 regenerates the already-unapplied `006`; it does not apply it and does not change its applied/unapplied status.
- **Ships independently of the backend.** With no `SupabaseConfig.plist` the screen opens, stickers render and progress computes.
- **Build Phase 1 → 2 is one constant, already shared.** `seedIsAuthoritative → false` moves `place_type` onto T-042's column. `visitsAreSeeded → false` (T-036's) moves the Been signal onto the real detector. **Passport itself needs no change at either flip** — that is the point of T-036's `VisitSourcing` seam, and this TRD is the first consumer to prove it.
- **What Phase 2 must re-verify:** everything §9 marks as checked against a fixture. Passport's own logic is fixture-independent, but its *inputs* are not.

---

## 8. Decisions

### D1 — Passport adds no store; composition is pure functions
Mirrors T-036's D3 and for the same reason: a derived `@Observable` store computed from three other stores has an invalidation problem, and a function cannot go stale. It is also what makes the PRD's "no second store of truth" structural rather than a rule someone has to keep.

### D2 — `Place.placeType` is a non-optional `String`, not a Swift enum
Non-optional on all three decode paths for T-036 D1's reason (a missing field must be a loud decode failure with a designed fallback, not a silent wrong value). A `String` rather than an enum because T-042 chose a *table* over a Postgres enum precisely so adding a type is an insert — a closed client enum would turn every such insert into a dropped row. The closed set lives on `StickerShape`, one hop later, where the failure mode is a generic glyph instead of a missing place.

### D3 — `StickerShape` is a closed enum with a `.generic` fallback and a build-time totality test
T-042 §4.2 asks for exactly this and says why the enum alone is not the guarantee: the key arrives as a `String`. The test is the falsifiable half.

### D4 — The shape registry is bundled and never fetched, permanently in V1
A shape key the binary cannot draw is useless however it arrives, so fetching the mapping buys nothing while adding a request, a cache field and a skew class. Bundling keeps vocabulary and assets in the same artifact. **Deviation from T-042 §4.5's implied client fetch — flagged for its reviewers**, reversible in one loader conformance.

### D5 — Hood attribution reads `place.hoodID`; the client never ray-casts
T-042's C-HOOD-1 already enforces exactly-one-Hood containment at dataset validation. A fourth implementation of that predicate on the client could disagree with the three that exist. Also answers the PRD's polygon-change question: re-attribution happens at export.

### D6 — The Local threshold is one Swift constant, provisionally 2
Req 4's "read from configuration, not hardcoded per Hood" is satisfied by one declaration site. A server config table does not exist and is not built for a number that changes a handful of times before launch. **The value is [ASSUMPTION] and flagged for Aviran**; the reasoning behind 2 is observability against the data that actually ships (§4.2), not a product judgement.

### D7 — Three Hoods are provisionally designated, seeded through the generator
Derived from the dataset (the only three Hoods with curated places), not invented. Goes through `hoods-tel-aviv.source.json` + `build_hoods.py`, never a hand-edit of the generated bundle (L-024). **Flagged for Aviran** — the real set is his or `data-engineer`'s, and the PRD says so.

### D8 — No in-the-moment surfacing ships
`ux-flows.md` Q13 stays open and req 6 passes anyway, because deriving stickers on read means there is no event to fire and no animation to skip. Building a toast would mean building the event first. **Flagged for `product`** as a deliberate non-build.

### D9 — Profile is a nav-row button at z7, icon-only
`ux-flows.md` §2 names it the 3rd of the 3 nav buttons, so T-032's D1 expectation holds here (unlike Places, which T-036's D7 corrected). **[ASSUMPTION]** glyph `person.fill`, chosen as the conventional profile-tab glyph. **Guard worth writing down given this feature's standing naming-drift risk:** it is a static system symbol, carries no user-supplied imagery, and must never become one — req 1's avatar ban is enforced by §9 row 1's grep, not by the glyph choice. One line for the post-ship `designer` pass to change.

### D10 — No sticker and no Hood row is tappable
V1 builds a display, not a navigation surface. A tappable row would need a destination no requirement names, and every tappable element added here is another element req 1's no-social-surface check has to reason about. It also keeps the ≥44pt guarantee trivially true: the only interactive elements on the screen are the ✕ and the drag handle.

### D11 — No `city` field is added to any model
One city, one header, one constant. Adding `city` to `Place` would spend T-042's one-field-per-task budget twice in the same task for a multi-city feature V1 does not have.

### D12 — The sticker's VoiceOver label names the shape, not the `place_type`
Resolves a genuine contradiction between PRD req 7 bullet 1 and T-042 §4.4. The spoken word lives on the client `StickerShape` enum, mirroring `PlaceCategory.displayName`, so no display string is added to the server side that T-042 §3.1 deliberately keeps free of them. **Flagged for `product`** as a stated deviation from the requirement's literal wording.

---

## 9. Verification — one row per P0 requirement

Per `architect.md` (L-018): every P0 names a falsifiable check with an observable, a pass condition, and the layer. `qa` builds `prds/passport/TEST-PLAN.md` from this table. **No row's pass condition is "looks right," and where a bullet cannot be checked this task says so instead of inventing a check.**

| P0 | Observable | Pass condition | Layer | Step |
|---|---|---|---|---|
| **1** Private, single-user, no social surface, no avatar, no account | (a) grep of every file in §2.1 for `ShareLink`, `UIActivityViewController`, `AuthenticationServices`, `ASAuthorization`, `SignInWith`, `URLSession`, `PhotosUI`, `UIImagePickerController`; (b) grep for any `Image(` bound to a non-literal, non-`systemName` source; (c) the rendered screen | (a) **zero hits, all nine symbols** — no network client means no wire over which another person's data could arrive, which is the structural form of this requirement; (b) zero — every image in the feature is a system symbol from a closed enum; (c) no share, invite, compare, follow, follower-count, leaderboard, login or sign-up control renders | review + manual | C13 |
| **2** One tap from map chrome; mutually exclusive with the other nav modals; never blocks the core loop; dismiss leaves camera and hour unchanged | (a) `ProfileButton` present in `MapNavRow` and hit-testable while `.profile` is presented; (b) `chrome.toggle(.heat)` with Passport open; (c) `chrome.toggle(.profile)` with a Hood sheet open; (d) `MKCoordinateRegion` + `selectedHour` sampled before and after a full open→dismiss cycle; (e) grep of §2.1 for `camera`/`selectedHour` | (a) button renders at z7 and a tap while presented dismisses; (b) `.heat` presented, `.profile` gone, one transition, no stacked state; (c) `router.hood == nil` after the call; (d) **byte-identical**; (e) **zero reads and zero writes** in this feature — which is why (d) cannot regress | unit + UI test | C11 |
| **3** One sticker per Been place, off the existing signal; Visited earns none; Saved-alone earns none; revisit adds none; shape matches type; every type has a shape; filed under the city page | (a) `PassportComposition.stickers` over a fixture with a Been place, a Visited place, a Saved-only place, a place in no source, and a visit id matching no `Place`; (b) the shipped `places-tel-aviv.json` decoded through `PlaceCatalog`; (c) C2's registry totality walk; (d) C12's bundle-coverage walk; (e) grep for a `city` field on `Place`/`Hood` | (a) exactly one sticker, for the Been place; the Visited, Saved-only and unsourced places yield none; the unresolvable id is skipped without a crash; output is name-ascending and identical across runs; (b) all nine places decode with a non-empty `placeType` **and** T-036's `permanentlyClosed` together (§2.2); (c) every registry key maps to a non-`.generic` case whose `symbolName` resolves; (d) every `place_type` in the places bundle is a registry key; (e) zero — exactly one header renders, from one constant (D11). **Not verified here: the 20-minute dwell threshold and the known-place guard — no detector exists.** Inherited from T-036 §9 row 3, re-run at Phase 2 against the real detector | unit + review | C1, C2, C4, C12 |
| **4** Per-Hood Local is the whole progression; overall Local needs every designated Hood; no retired tier name; no global point total or rank; undesignated Hoods absent; threshold from configuration | (a) `progress`/`isOverallLocal` over a fixture with a designated-and-Local Hood, a designated-not-Local Hood, an undesignated Hood, and (separately) an empty designated set; (b) every **user-facing string literal and asset name** in this feature, plus every case name in any type it declares; (c) grep for total/level/rank/score/points across §2.1; (d) grep for `threshold` | (a) the undesignated Hood is **absent from the output**, not present at zero; overall is `true` only when every designated Hood is Local; **overall is `false`, never `true`, when the designated set is empty**; (b) none of `Wanderer`, `Insider`, `Legend`, `Native`, `Regular` or `Tourist` appears as a status word — case-sensitive, whole-word, scoped to strings/asset names/case names so ordinary code identifiers do not produce noise, and `isTouristTrap`/`is_tourist_trap` is T-035's flag field and is out of scope; (c) zero; (d) exactly one declaration, in `LocalStatus`, and no second literal compared against a Been count anywhere. **Not verified on device: overall-Local-reached** — with A2's three designated Hoods and T-036's shipped fixture only one Hood reaches Local, so the positive case is unit-only. Named rather than engineered around, because changing T-036's fixture to make it observable would edit a contract that has already cleared `trd-review` | unit + review | C3, C4, C12 |
| **5** Progress legible without arithmetic or colour; zero renders plain; empty Passport is a plain empty state | (a) a rendered progress row at Local, at partial and at zero; (b) the same three in a greyscale render; (c) the album with an empty sticker set | (a) each row states **numerals against the threshold** (`"2 of 2"`) as text — no bar, and the Local state carries a word, not only a glyph or colour; (b) all three rows remain distinguishable with colour removed; (c) icon + one line naming what earns a sticker, no error string, no spinner, no lock, no teaser | UI test + manual | C9, C10 |
| **6** Nothing interrupts the map on a sticker or a milestone; anything that does surface is non-blocking; a sticker earned while closed is simply present | (a) grep of §2.1 for `.alert`, `.fullScreenCover`, `.sheet`, `.confirmationDialog`, any toast/banner presenter, and any `withAnimation` keyed on a count change; (b) the app relaunched with a fixture that gained an entry while it was closed | (a) **zero** — there is no code path that observes a visit being added, so no celebration can fire (D8); (b) the new sticker is present on the next open with no animation and no catch-up state. **Nothing is verified for "any in-the-moment surfacing that does ship," because none ships** — `ux-flows.md` Q13 stays open and is not answered by this build | review + manual | C13 |
| **7** Every sticker has a VoiceOver label naming the place and what it is; per-Hood status announced as text with count and Local state; every interactive target ≥44pt | (a) `PassportLabels` over the full shape × (Local, partial, zero) matrix; (b) the accessibility tree of the rendered screen; (c) the frame of every interactive element | (a) every string names the place and a shape word, and every Hood string carries both numerals and the Local state — asserted against expected strings, not merely non-empty; (b) no sticker exposes an image-only element and no Hood row exposes a value-only element; (c) the ✕ and the drag handle are the **only** interactive elements (D10) and both are ≥44×44pt. **Stated deviation, not a gap: the sticker label names the sticker's shape, not the raw `place_type`** (D12) — `product` must confirm this satisfies req 7 bullet 1 | unit + UI test | C5, C8, C13 |
| **8** Location Always denied opens the screen with no nagging and no re-prompt; offline renders fully from device | (a) grep of every file in §2.1 for `CoreLocation`, `CLLocationManager`, any authorization read, and any network symbol; (b) the app run with location denied; (c) the app run in airplane mode | (a) **zero hits** — there is no permission-dependent or network-dependent code path in this feature to degrade; (b) Passport opens, renders whatever is earned, shows no re-prompt and no nagging copy; (c) identical render. **Inherited caveat, not re-flagged as new:** in Build Phase 1 T-036's fixture populates regardless of permission, so "Been reflects only what was actually detected" is checked as the absence of a sensor path, exactly as T-036 §9 row 5 already states, and re-runs against the real detector at Phase 2 | review + manual | C13 |

---

## 10. Risks and alternatives

| Risk | Mitigation / decision |
|---|---|
| **The whole progression half is empty on a shipped device** — all 24 Hoods currently carry `designated_for_progression = false` and no task owns populating it | A2 seeds a provisional set (D7) **and** C12 makes "at least one designated Hood in the shipped bundle" a build-time assertion, so the empty-section state cannot ship silently. Deliberately **no placeholder UI is designed for it** — a state the build must not ship is a gate, not a screen |
| The Local threshold ships as an invented number and nobody notices it was never ratified | One constant, one site, tagged **[ASSUMPTION]** in the source and in D6, with the reasoning stated as observability rather than product judgement. Named in this TRD's review routing for Aviran |
| A1's provisional shape mapping hardens into the ratified vocabulary by default | The file's own `_note` says PROVISIONAL and names T-042 B1 as the owner; A1 is routed to `data-engineer`, not to whoever writes the Swift, precisely so the value set is not invented at build time |
| `place_type` and `permanentlyClosed` collide in the same four files while both tasks are in flight | §2.2 states the amendments are additive and independent, and §9 row 3(b) asserts **both** fields decode from the shipped bundle together — so a merge that drops one fails a test rather than shipping quietly |
| Passport is read as permission for accounts, avatars or a social surface, because the tab is called "Profile" | The PRD's own standing risk. Made checkable here: §9 row 1 greps nine specific symbols across the whole feature, and D9 writes the "static system glyph, never user imagery" guard into the button's own decision |
| Device-local data is lost on reinstall | The PRD's open question for Aviran, unchanged and not resolved here. Passport inherits it from T-036 and adds nothing recoverable of its own — there is nothing to back up that the Been set does not already imply |
| Deriving stickers on every render is slow | Nine places in Phase 1, a few hundred at Phase 2, on a screen that opens on an explicit tap. If it ever measures, the seam is one function, not a rewrite (§4.1) |
| The registry and the shipped assets drift | D4 puts them in the same artifact, and C2 + C12 make both halves of the coverage a build-time test |
| A regenerated `hoods-tel-aviv.json` looks like a diff nobody intended | `build_hoods.py` stamps `generatedAt` from the wall clock, so it never diffs clean (§3.5). Named here because T-035's TRD found it the hard way; reviewers and `qa` normalise that field before comparing |
| **Nothing rewards answering local-QA** — the pipeline's named incentive risk | Carried forward from the PRD unchanged. **Not this task's to fix and not fixed here**: stickers are tied to Been places by decision #29, and #40 retired the ladder that carried the rest. Restated so it is not silently absorbed into "Passport shipped, incentives are handled" |

**Alternatives considered and rejected:** a persisted sticker record per Been place (a second store of truth the PRD forbids, and a second copy of location history §3.6 exists to avoid); a derived `@Observable` Passport store (D1); a closed Swift enum for `place_type` (D2 — turns a server insert into dropped rows); fetching `place_types` at runtime (D4); a client-side polygon ray-cast for attribution (D5); a per-Hood threshold column (D6 — req 4 forbids it by name); a plist or server-side threshold (D6); hand-editing the generated `hoods-tel-aviv.json` for the designated set (L-024, D7); a "you earned a sticker" toast (D8); progress bars beside the numerals (§4.3 — the colour/shape-only failure req 5 exists to prevent); tappable sticker and Hood rows (D10); a `city` field on `Place` and a per-city grouping (D11); chronological album order (§4.4 — the timestamp is not on the seam T-036 exposes, and widening it would reopen a cleared contract); a private visit fixture in this task (the second detector T-035 and T-036 both refuse to build); a third `BuildPhase` constant (§7 — same axis as `seedIsAuthoritative`).

---

## 11. Build breakdown

Ordered. A1 must land before C2's totality test is meaningful; A2 before C12's bundle assertion. C1–C5 carry no view work and are testable with no simulator.

| # | Step | Tag |
|---|---|---|
| **A1** | Author `Passenger/Resources/place-types-tel-aviv.json` — the `place_type` → `sticker_shape` mapping for exactly the six values in the shipped places bundle (`bar`, `cafe`, `landmark`, `market`, `museum`, `restaurant`), with the PROVISIONAL `_note` naming T-042 B1 as the ratifying owner (§3.4). **Not invented by whoever writes the Swift** | **[Algo/Data]** |
| **A2** | Set `designatedForProgression: true` on `florentin`, `kerem-hateimanim`, `neve-tzedek` in `database/data/hoods-tel-aviv.source.json` — **on top of T-035's A1 `isTouristTrap` edits already in that file, never a pre-A1 copy** — and **re-run `build_hoods.py`** to regenerate `Passenger/Resources/hoods-tel-aviv.json` and `database/migrations/006_hoods_tel_aviv_data.sql`. **Never hand-edit either generated file** (L-024). `006` stays unapplied and Aviran-gated (§3.5, D7). Normalise `generatedAt` when diffing; confirm the diff shows only `designatedForProgression`, `generatedAt` and the migration's source digest | **[Algo/Data]** |
| C1 | `Place.placeType` + decode on **all three** paths — `SeedFile.Entry`, `PlacesAPI.PlaceRow` and the `select=` string, `PlacesCache.CachedPlace` (§3.2, D2). Tests: the shipped bundle decodes nine places each with a non-empty `placeType`; a live payload missing the column throws and falls back; an older cache payload fails to decode and falls through to the seed. **Add beside T-036's `permanentlyClosed`, which is already in these four files — never re-derive them from `HEAD`** (§2.2) | **[iOS]** |
| C2 | `StickerShape` (closed enum, `.generic` fallback, `symbolName`, `spokenName`) + `PlaceTypeRegistry` — bundled, synchronous `static let`, **not** wired into `PlaceCatalog.load()` or any `.task` (§3.3, §3.4, D3, D12). **Totality test:** every key in the shipped registry maps to a non-`.generic` case whose `symbolName` resolves to a real symbol. Missing/corrupt registry → empty map, never a crash | **[iOS]** |
| C3 | `LocalStatus` — the single threshold constant and `isLocal(beenCount:)`, with the **[ASSUMPTION]** comment naming Aviran as the owner of the value (§4.2, D6) | **[iOS]** |
| C4 | `PassportComposition` — `stickers`, `progress`, `isOverallLocal` (§4.1, D1) with the full test matrix from §9 rows 3 and 4, **including the empty-designated-set case returning `false`** | **[iOS]** |
| C5 | `PassportLabels` + its full matrix test (§4.7, D12) | **[iOS]** |
| C6 | `MapChromeState` (§4.6). **If `MapChromeState.swift` does not exist yet, create it exactly per T-032 §4.1 — all four cases, all four conformances, verbatim. If it exists, add nothing: `.profile` is already a member.** Exclusivity unit test | **[iOS]** |
| C7 | `ProfileButton` added to T-032's `MapNavRow` — icon-only, `accessibilityLabel`, ≥44pt, stays hit-testable at z7 while presented (§2.4, D9). **Blocked on T-032's C2; do not create `MapNavRow`** | **[iOS]** |
| C8 | `PassportSurface` at z5 — drag handle, 44×44pt ✕, scrim tap, `toggle(.profile)`, Reduce-Motion-aware transition (§4.6) | **[iOS]** |
| C9 | `PassportAlbum` + `PassportStickerView` — grid, single city header, empty state (§4.4, §9 row 5) | **[iOS]** |
| C10 | `PassportProgressList` — per-Hood rows with numerals-against-threshold, plain zero state, overall line; undesignated Hoods never rendered (§4.3) | **[iOS]** |
| C11 | Wire into `MapScreen`: the `.profile` case, `closeHood()` on open and `closePlace()` on leave (§4.6), pass `hoods` / `placeCatalog.allPlaces` / `visitedPlacesStore.visits` in. Tests for §9 row 2 | **[iOS]** |
| C12 | **Shipped-bundle invariant tests** (§9 rows 3, 4): at least one Hood carries `designatedForProgression == true`; every designated Hood holds at least `LocalStatus.threshold` curated places; every `place_type` in the places bundle is a registry key. These are the assertions that stop A1/A2 being quietly forgotten | **[iOS]** |
| C13 | The absence gates (§9 rows 1, 6, 8): the nine-symbol social/network grep, the presenter/celebration grep, the `CoreLocation`/authorization grep, and the ≥44pt check over the two interactive elements. Failing any of these fails the build step, not `qa` | **[iOS]** |

**`trd-review` sign-off needed from two pairs:**

- **`ios-developer` + `ios-code-reviewer`** — C1–C13.
- **`data-engineer` + `code-reviewer`** — **A1 and A2 only.** `developer` is deliberately not on this list: this TRD writes no hand-authored SQL, and `006` is a *generated* artifact regenerated by a script `data-engineer` owns. That is T-035's A1 routing precedent applied unchanged. If `code-reviewer` reads the `006` regeneration as needing `developer` too, that is a one-line routing add, not a TRD change.

**Cross-checks worth one explicit pass at review:**

- **T-032's TRD** — diff §4.6's reproduced `NavSurface`/`MapChromeState` block against its live §4.1 character by character (that exact mismatch sent T-036's v1 back), and confirm `MapNavRow`'s container contract before C7 adds a button to it.
- **T-036's TRD** — confirm `VisitKind`/`VisitedPlacesStore.visits` still have the shape §4.1 reads, and that its C1 amendment to the four `Places/` files is additive with C1's (§2.2).
- **T-042's TRD and its reviewers** — **D4** (the registry is bundled, never fetched — this removes `GET /place_types` from the client contract), **D12** (`StickerShape.spokenName` lives on the client, so §3.1's no-display-string-on-the-server rule stays intact), and confirmation that A1's provisional mapping is understood as provisional against its own B1.
- **`product` and Aviran** — the three PRD findings carried forward untouched (`place_type` user-facing or not; nothing rewards answering local-QA; device-local loss on reinstall), plus **D6's threshold value**, **D7's designated set**, **D8** (no in-the-moment surfacing, `ux-flows.md` Q13 left open), **D12** (req 7's literal wording), and §4.4's name-ascending album order.
- **`chief-of-staff`, for `BOARD.md` rows this TRD cannot create** — the shared dwell/geofence detector is still ownerless (named by T-035 and T-036 and now T-037, no row); `hoods.designated_for_progression` has no owner for its real values; the Local threshold has no owner. Per `CLAUDE.md` rule 5, each needs a row with an owner rather than another worklog line saying "flagged for whoever owns it."
