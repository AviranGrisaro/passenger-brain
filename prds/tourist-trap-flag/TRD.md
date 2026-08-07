# Tourist-Trap Flag & Local QA — TRD

**Task:** T-035 · Linear `PAS-26`
**PRD:** [`tourist-trap-flag.md`](./tourist-trap-flag.md) (Draft v1, 2026-07-30)
**Design reference (informational, not a gate — pre-code design gate retired 2026-08-02):** [`design/phase-1/tourist-trap-flag-design.md`](../../design/phase-1/tourist-trap-flag-design.md), mockup `https://claude.ai/code/artifact/40b9ec94-b831-4d20-a334-fb95bf5f4cbd`
**Author:** architect · **Date:** 2026-08-02 · **Revised:** 2026-08-02 (v2) · **Status:** v2 — ready for `trd-review` re-run (C1–C14 only)
**Build phase:** 1 (`BOARD.md` V1 Build Phases) — with two steps explicitly held for later phases, named as such in §11.

**What changed at v2 (2026-08-02).** `trd-review` on the C1–C14 `[iOS]` bulk came back **REQUEST CHANGES from both required signoffs** — `ios-code-reviewer` (`passenger-brain 4a96756`) and `ios-developer` (`passenger-brain 96b293b`, independently re-derived from source rather than co-signed) — unanimous on the same three findings. This revision resolves exactly those, plus one accuracy fix carried from the A1 review. **No contract, flow or build step is redesigned; D1–D8 all stand as written at v1.** Step **A1 already CLEARED** review (`code-reviewer` `passenger-brain 864b8ea` + `data-engineer`, both APPROVE WITH MINORS) and **B1 remains HELD** for Build Phase 2 — neither is reopened here.

| # | Finding | Raised by | Fix in v2 |
|---|---|---|---|
| 1 | **Blocking.** §3.3's `InstallIdentity` is a separately-generated UUID living only in `local-qa.json`, while `analytics/EVENTS.md` line 13 — committed a day earlier (`passenger-brain 2e38e4b`) — states as a load-bearing identity constraint that every table keys on *"the same identifier `local_qa_answers` already uses"*, defined at `app_installs.install_id`. Two independent generation paths cannot produce one value. The TRD never mentioned `EVENTS.md`, so the conflict was silent: either the two ids diverge and break the join `EVENTS.md` promises, or someone "fixes" it by unifying them and destroys §3.3's own minimisation without anyone deciding to | `ios-code-reviewer`, independently re-derived by `ios-developer` | **New §8 D9** — a real decision, made, with the tradeoff accepted explicitly: the two ids stay **deliberately separate**. §3.3 rewritten to say so and to point at D9; the type is renamed **`LocalQAInstallIdentity`** so the distinction is visible at every call site; §4.4 pins "no FK to `app_installs`, ever"; §2.1/C9 follow the rename. **`EVENTS.md` line 13 is named as needing its own correction by `analytics-engineer`** (§10, D9) — not silently contradicted |
| 2 | **Blocking.** §2.2's "no type holds a reference to both `LocalQAAnswerStore` and either catalog" is **false against the shipped composition root.** `MapScreen.swift:43,60` already holds `hoods: [Hood]` and `placeCatalog`, and per C11/C12 `LocalQACoordinator` has no other plausible owner — so the TRD's own intended architecture trips the blocking review finding §9 row 9(a) told `ios-code-reviewer` to raise | `ios-code-reviewer`, independently re-derived by `ios-developer` | §2.2's third bullet is rewritten to the invariant that actually holds and is actually checkable — a **render-function-signature** rule: `FlagStroke.treatment(for:band:)` and `HoodSpeech.label(name:band:flag:)` never take answer-store data as an input. §9 row 9(a) restated to check signatures. `MapScreen` co-owning both is named as **expected and not a finding**, so the next reviewer neither false-positives on it nor narrows the rule off-record |
| 3 | **Blocking.** §10's risk row claimed "§9 row 8 has `qa` confirm focus is not stolen" for D4's new `UIWindow`. Row 8's five sub-checks (a)–(e) — gate precedence, appears-once, auto-dismiss timing, presenter count, queue state — contain nothing about VoiceOver focus. §10 cited a check that does not exist, on D4's own highest-stated-risk surface | `ios-code-reviewer`, independently re-derived by `ios-developer` | **§9 row 8 gains a real sub-check (f)** with an observable and a falsifiable pass condition (`UIAccessibility.focusedElement` unchanged across toast appearance; `.announcement` posted, `.screenChanged` never). §10's row rewritten to cite 8(f) accurately. **C12 now also pins the window-presentation mechanics** — never made key, `accessibilityViewIsModal` false — since a new `UIWindow` can pull focus through UIKit's own hierarchy scan regardless of which notification is posted (`ios-code-reviewer`'s addendum to finding 3) |
| 4 | Accuracy fix, **not** from the C1–C14 reviews — carried from the **A1** review, where both signoffs confirmed it independently (`code-reviewer` `864b8ea` finding 1, `data-engineer` concurring). §10's round-trip risk row described `qa`'s check as "byte-identical", but `build_hoods.py`'s `build_bundle()` stamps `generatedAt` from wall-clock time, so the **JSON bundle is never** byte-identical across two runs even with zero content change (the SQL migration is, and that half was true) | `code-reviewer` + `data-engineer` (A1 pass) | §10's row now says byte-identical **excluding `generatedAt`**, and names normalising that field as the precondition for `qa`'s check. **Wording only — A1's build step is untouched and its clearance is not reopened.** Left standing, `qa` would have written a check that fails on every run and trained its reader to eyeball past the diff — the exact L-024 failure mode |

**One non-blocking nit from `ios-developer`'s pass, fixed outside this file:** the v1 delivery entry in `PROGRESS.md` self-cited its commit as `a671373`, an orphaned object left by that pass's own self-reported `read-tree` recovery. Verified here (`git merge-base --is-ancestor` → unreachable from `HEAD`) and corrected to `a6c1c73` in that entry, disclosed in this pass's own worklog entry rather than left as a silent edit to history.

---

## 1. Context

Read the PRD first; nothing here restates it. Rendering rules come from `design/map-rendering-spec.md` §§2–4/§7 and `design/ux-flows.md` §6, which the PRD references rather than re-derives — this TRD does the same.

**Surfaces this task touches, and who builds them:**

| Surface | Repo | Tag |
|---|---|---|
| Hood outline stroke + centroid flag label, VoiceOver | `passenger-code` | **[iOS]** |
| Place-detail-modal flag line (fills the reserved `touristTrapSlot`) | `passenger-code` | **[iOS]** |
| Hood-sheet flag line (**new — see D5, an architect call**) | `passenger-code` | **[iOS]** |
| Local-QA toast, ask-once gate, answer store | `passenger-code` | **[iOS]** |
| Plausible fake Hood flag values for the Phase-1 demo | `passenger-brain/database/data/` | **[Algo/Data]** |
| `local_qa_answers` table — **HELD, Build Phase 2** | `passenger-brain/database/migrations/` | **[Backend]** |

**Mostly iOS, but not iOS-only.** The Hood flag values cannot be seeded client-side: `Passenger/Resources/hoods-tel-aviv.json` is a *generated* artifact — `database/scripts/build_hoods.py` emits it and `006_hoods_tel_aviv_data.sql` from `database/data/hoods-tel-aviv.source.json` in one run. Hand-editing the bundle is exactly the failure L-024 records (a hand-edited generated artifact survived code-review and two QA rounds). Seeding goes through the source and a regeneration — step **A1**, `[Algo/Data]`.

`Passenger/Resources/places-tel-aviv.json` is different and is safe to hand-edit in Phase 1: `hood-place-detail/TRD.md` C3a hand-authored it as an explicitly provisional fixture, and T-042's `export_places.py` only becomes its sole emitter at Build Phase 2 (that TRD's D4/B2). So place flag values are an `[iOS]` step (**C6**).

**What is real in Build Phase 1 and what is not — stated up front, not discovered at `qa`:**

- **Real:** the entire render side (Hood stroke, label, VoiceOver, place-modal line, Hood-sheet line); the toast surface and its states; the binary answer capture; the ask-once ledger; the daily-cap and notifications-denied suppression logic; the device-local answer queue; the install identity.
- **Stubbed / not built here:** the **geofence dwell detector and the local notification that carries the ask**. Neither exists in the codebase and neither is this task's to build — the PRD assigns the detector to `data-engineer` as *"one detector, three consumers"* (T-035/T-036/T-037), `LocationStore` deliberately holds authorization status and never a `CLLocation`, the project declares no `NSLocationAlwaysAndWhenInUseUsageDescription` and no background modes, and T-036's design flagged the same absence independently. Phase 1 ships the consumer side against a `VisitSource` seam driven by a launch argument (**C11**), the same construction `MapScreen`'s existing `-uiTestZoomedIn` uses.
- **Stubbed:** the answer **sync target**. Nothing consumes an answer in Phase 1; `local_qa_answers` is written as a migration (**B1**) and held for Phase 2. The Phase-1 sync implementation is a no-op, and the toast's confirmation copy says so rather than claiming a share that did not happen (**D6**).

**Cross-task dependency, real and one-directional:** the busy+flagged treatment (PRD req 5) reads `HeatBand.busy`, and in Build Phase 1 `DensityStore` has **no seed path at all** — `load()` is live → cache → `.unavailable`, so `band(for:hour:)` is `nil` for every Hood at every hour. T-032's TRD folds a bundled density seed into its own scope (its D10/C10). **Until C10 lands, req 5's states are built but unobservable.** This TRD does not duplicate that seed; §9 row 5 names C10 as its precondition and §11 states the build-order consequence.

---

## 2. Architecture

### 2.1 Module layout — additions to the shipped tree

```
Passenger/
  Flag/                       (new — the flag's vocabulary, no SwiftUI, no map types)
    TouristFlag.swift           Bool? -> flag state; (state, band) -> stroke treatment
    FlagCopy.swift              every user-facing and spoken string, one file
    HoodSpeech.swift            (name, band, flag) -> one VoiceOver sentence
  LocalQA/                    (new — the ask loop; knows nothing about the map)
    VisitEvent.swift            the event + the VisitSource protocol
    DebugVisitSource.swift      Phase-1 launch-argument trigger
    LocalQAGate.swift           pure: offer or suppress, with a reason
    LocalQAAnswerStore.swift    ledger + queue + lastAskedAt, device-local
    LocalQAInstallIdentity.swift  one per-install UUID, NOT the analytics one (D9)
    LocalQASync.swift           the sync seam + the Phase-1 no-op
    LocalQACoordinator.swift    @MainActor @Observable — the one pending ask
    LocalQAToast.swift          the toast view
    LocalQAPresenter.swift      the passthrough window that hosts it (D4)
  Map/
    MapZoomTier.swift           (new) span -> .cityWide / .neighborhood / .close
    HoodLayer.swift             (changed) stroke + second label line + speech
    MapScreen.swift             (changed) tier derivation, coordinator wiring
  Detail/
    PlaceDetailModal.swift      (changed) touristTrapSlot filled
    HoodSheet.swift             (changed) three-state flag line (D5)
  Places/
    Place.swift                 (changed) + isTouristTrap
    PlaceCatalog.swift          (changed) decode the field on all three paths
  Resources/places-tel-aviv.json (changed) seeded flag values
  Assets.xcassets/Flag.colorset  (new)
```

### 2.2 Boundaries — who is allowed to know what

- **`Flag/` is pure vocabulary.** No SwiftUI, no MapKit, no store. It answers "given a `Bool?` and a `HeatBand?`, what treatment and what words." Every P0 rendering rule is decided inside it, which is what makes reqs 1–5 and 7 unit-testable without a simulator.
- **`LocalQA/` never imports `Hoods/` or `Map/`.** It knows a `Place.ID` and nothing about geometry. It never reads or writes `PlaceCatalog`/`HoodCatalog`.
- **The req-9 invariant is a function-signature rule, and that is the only form of it that is true.** There is exactly one direction of data flow: catalogs → render; toast → answer store. The checkable guarantee is at the two functions that decide what renders:

  > **`FlagStroke.treatment(for:band:)` and `HoodSpeech.label(name:band:flag:)` never take `LocalQAAnswerStore`, a `LocalQARecord`, or any value sourced from `LocalQA/` as an input.** Their signatures are pinned verbatim in §4.1 and §4.2. Adding such a parameter — or a stored property on either type that reaches one — is the blocking review finding.

  An answer therefore cannot change what renders, for this viewer or any other, because the functions that decide rendering cannot see an answer. Two supporting rules, both greppable: `LocalQA/` imports neither `Hoods/` nor `Map/`, and touches `Places/` only for `Place.ID`; nothing in `LocalQA/` reads or writes `PlaceCatalog`/`HoodCatalog`.

  **`MapScreen` will hold both a catalog and — transitively, through `LocalQACoordinator` (C11) — `LocalQAAnswerStore`. That is expected and is not a finding.** It is the composition root and already holds `hoods: [Hood]` and `placeCatalog` (`MapScreen.swift:43,60`) alongside `densityStore`/`locationStore`/`savedPlacesStore` in exactly this pattern. **v1 stated this invariant as "no type holds a reference to both `LocalQAAnswerStore` and either catalog", which the shipped code already falsifies** — that phrasing would have made `ios-code-reviewer` block on this TRD's own intended wiring (`trd-review` finding 2). Holding both is harmless; *passing one into a render function* is not, and that is what is checked.
- **The map never asks the flag a question it can answer two ways.** `MapZoomTier` is the single derivation of zoom from span; `showsNames` becomes `tier == .close` rather than a second independently-computed boolean (same discipline T-032 applied to `selectedHour`).

### 2.3 The three zoom tiers, and why the existing threshold is not enough

`map-rendering-spec.md` §2's table needs three tiers; the app has one boolean. `MapScreen.nameLabelSpanThreshold` (0.06) today gates the Hood name label, the pin layer, `HoodButton`, *and* tap resolution together — that boundary is the **Close** tier, since pins appear there. The flag needs a second, coarser boundary above it:

| Tier | Span | Flag stroke | Flag label | Pins (unchanged) |
|---|---|---|---|---|
| `.cityWide` | `span >= neighborhoodSpanThreshold` | none | none | none |
| `.neighborhood` | `closeSpanThreshold <= span < neighborhoodSpanThreshold` | yes, flagged only | **yes, flagged only** | none |
| `.close` | `span < closeSpanThreshold` | yes, flagged only | none | yes |

`closeSpanThreshold` **is** today's `nameLabelSpanThreshold` (0.06), renamed in place, so no existing behaviour moves. `neighborhoodSpanThreshold` is new and must sit strictly between 0.06 and the cold-open span (0.14) — the exact value is `ios-developer`'s, the same carve-out T-031 made for heat-band thresholds. `MapZoomTier.tier(forLatitudeDelta:)` is a pure function with a boundary-value test; nothing else in the app may re-derive a tier from a span.

**Correction to the design reference, stated rather than silently diverged from:** `tourist-trap-flag-design.md` §2 says the flag *stroke* can reuse the existing `showsNames` threshold and only the label needs a new tier. That is wrong by one tier — `showsNames` is the Close boundary, so a stroke gated on it would first appear at the same instant pins do, and the Neighborhood tier (stroke, label, no pins) would not exist. Both the stroke and the label need the new threshold; they differ in which side of the Close boundary they survive. The design's *intent* (stroke persists at Close, label drops) is built exactly as written.

---

## 3. Data model

### 3.1 The flag — three stored states, two rendered

`Hood.isTouristTrap: Bool?` already exists and already decodes (`Hoods/Hood.swift:32`, `HoodCatalog.swift:31`). Nothing changes there.

`Place` gains one field:

```swift
/// `nil` == not yet rated — three states, not a boolean, matching `Hood`.
let isTouristTrap: Bool?
```

decoded from the already-authored `is_tourist_trap` key on all three `PlaceCatalog` paths (seed / live / cache). The seed file already carries the key on every place, currently `null`; `PlacesAPI.PlaceRow` and `PlacesCache.CachedPlace` gain it too, so a cached place does not silently lose its flag.

`TouristFlag` is the read model, so no view branches on a `Bool?` directly:

```swift
enum TouristFlag { case flagged, notFlagged, unrated }        // from Bool?
enum FlagStroke  { case none, plain, busyWarning }            // from (TouristFlag, HeatBand?)
```

`FlagStroke.treatment(for:band:)` is total over 3 × 4 inputs and returns exactly one case — **`.plain` and `.busyWarning` are cases of one enum, so "replaces, never stacks" (req 5) is guaranteed by the type, not by an `if/else` a future edit could turn into two conditions.**

### 3.2 Build Phase 1 — plausible fake flag values

Checked directly, not assumed: **all 24 bundled Hoods ship `isTouristTrap: null` and all 9 bundled places ship `is_tourist_trap: null`.** That is the real cold-start state the PRD names as a risk, not a bug — but it means every flagged, not-flagged and busy+flagged rendering path in this task is unobservable in the Phase-1 demo, and five of nine P0s would have nothing to check.

Precedent for seeding fake values in-task is settled: `BOARD.md`'s Build Phase 1 definition ("fake/hardcoded data baked into the app — just enough to demo interactions"), T-033's C3a fixture, T-034's bundled fake event set, T-032's density seed (D10).

**Hoods — step A1, `[Algo/Data]`, in `passenger-brain`.** Edit `database/data/hoods-tel-aviv.source.json` and re-run `build_hoods.py --migration-number 006`, which rewrites both `Passenger/Resources/hoods-tel-aviv.json` and `migrations/006_hoods_tel_aviv_data.sql` from one validated source. The migration stays **unapplied** (Aviran-gated). `validate_dataset.py` already accepts `Optional[bool]`, so no validator change is needed.

**Authoring rule, stated as pass/fail so no check can pass vacuously:**
1. ≥1 Hood `true` that reaches `.busy` for ≥1 hour in T-032's density seed — this is the only way req 5's busy+flagged state is ever observed;
2. ≥1 Hood `true` that never reaches `.busy` at any of the 13 hours — the plain flagged stroke;
3. ≥1 Hood explicitly `false`;
4. ≥1 Hood left `null` — reqs 4 and 7's unrated state;
5. total flagged ≤ 4 of 24, so the map still reads as "a handful of exceptions" (`map-rendering-spec.md` §3's density bound).

Rules 1 and 2 require the flagged Hood ids to be coordinated with T-032's `density-seed-tel-aviv.json`. Whichever of the two lands second owns the reconciliation; §11 states it.

**Places — step C6, `[iOS]`.** Set `is_tourist_trap` on the existing 9-place fixture: ≥1 `true`, ≥1 `false`, ≥1 left `null`, and the `true` one in a Hood that is itself flagged — so the Hood-vs-place disagreement case the PRD lists as an open question is at least *not* the only case a demo shows.

### 3.3 Local-QA state — device-local, minimised on purpose

One file, `local-qa.json`, in Application Support, following `SavedPlacesPersistence`'s actor shape exactly:

```swift
struct LocalQARecord: Codable, Sendable {
    let placeID: String      // slug, never a coordinate
    let answer: Bool
    let answeredAtHour: Date // truncated to the UTC hour
}
struct LocalQAFile: Codable {
    let installID: UUID
    let lastAskedAt: Date?   // for the cadence cap only
    let records: [LocalQARecord]
}
```

**Location privacy is a data-model constraint here, not a review note.** Unlike `saved-places.json` (which records intent), this file records that a person was *physically present* at a named place at a time. Three minimisations, each of which is a build step, not a principle:

- **No coordinates, ever** — a place slug only. The coordinate is already in the bundle; storing it again in a per-user file would add nothing and leak more.
- **Timestamp truncated to the UTC hour.** Hour precision is all the eventual signal needs; minute precision would be a movement log.
- **Excluded from device backup** (`URLResourceValues.isExcludedFromBackup = true`) and written with `.completeUntilFirstUserAuthentication` file protection. `SavedPlacesPersistence` does neither; this file is a stronger artifact and gets stronger handling. **[ASSUMPTION]** that `saved-places.json` should get the same treatment — flagged to `ios-code-reviewer` as a possible sibling finding, deliberately not changed here (surgical-changes rule).

**Install identity:** `LocalQAInstallIdentity` — one `UUID` generated on first write and stored in this same file. **Not the IDFV, not the IDFA, not the Keychain.** The Keychain would survive a reinstall, which would make "install id" a lie and create a more durable identifier than the feature needs; a file in Application Support dies with the app, which is exactly the intended lifetime.

**It is also deliberately not the analytics `app_installs.install_id`, and that is a decision, not an oversight — see D9.** The type is named `LocalQAInstallIdentity` rather than `InstallIdentity` precisely so a future edit cannot quietly point it at the analytics id under the impression it is consolidating a duplicate. Anything that wants to unify the two must go through D9 first.

---

## 4. Contracts

### 4.1 `TouristFlag` / `FlagStroke` — the whole rendering decision (`[iOS]`)

```swift
extension TouristFlag { init(_ raw: Bool?) }                          // true/false/nil
enum FlagStroke {
    static func treatment(for flag: TouristFlag, band: HeatBand?) -> FlagStroke
}
```
Total table (`.notFlagged` and `.unrated` are identical in every column — req 4):

| flag \ band | nil | quiet | moderate | busy |
|---|---|---|---|---|
| `.flagged` | `.plain` | `.plain` | `.plain` | `.busyWarning` |
| `.notFlagged` | `.none` | `.none` | `.none` | `.none` |
| `.unrated` | `.none` | `.none` | `.none` | `.none` |

Rendered values (from the design reference, adopted unchanged):
`.none` → today's `.stroke(.secondary.opacity(0.35), lineWidth: 0.5)`, byte-identical to what `HoodLayer` draws now on every Hood;
`.plain` → `.stroke(Color("Flag"), lineWidth: 2.5)`;
`.busyWarning` → `.stroke(Color("Flag"), style: StrokeStyle(lineWidth: 3, dash: [6, 4]))`.

The `.none` case keeping the existing constant is not a violation of req 4's "renders no stroke": the 0.5pt neutral boundary is drawn identically on *every* Hood regardless of flag, so it carries zero flag information. Req 4's observable is "carries no flag signal", and the check in §9 is a greyscale/weight comparison, not "no line is drawn".

### 4.2 `FlagCopy` — every string, in one file (`[iOS]`)

| Where | Flagged | Not flagged | Unrated |
|---|---|---|---|
| Hood centroid label (`.neighborhood` only) | "Tourist-heavy spot" · busy: "Busy and tourist-heavy" | — (no label) | — (no label) |
| Place modal line | `camera.fill` + "Tourist-heavy spot" | — (nothing renders) | — (nothing renders) |
| **Hood sheet line (D5)** | "Tourist-heavy spot" | "Not a tourist-heavy spot" | "No local rating yet" |
| Toast question | "Does this feel like a tourist-heavy spot?" · buttons "Yes" / "No" | | |

`HoodSpeech.label(name:band:flag:)` composes one sentence, total over 3 × 4 inputs:

- `.flagged` + `.busy` → `"Kerem HaTeimanim, busy and tourist-heavy — worth a second look"` (its own combined form, req 7 bullet 2 — never two clauses)
- `.flagged`, other bands → `"Florentin, quiet, tourist-heavy spot"`
- `.notFlagged` → `"Neve Tzedek, busy, not a tourist-heavy spot"`
- `.unrated` → `"Bavli, quiet, no local rating yet"`
- band `nil` → `"…, no data right now, "` + the same flag clause (extends the shipped `voiceOverLabel`'s existing no-data branch rather than replacing it)

**Every string in this file is checked by a test that greps the type's own outputs for the substring "tourist trap", case-insensitively, across all 12 inputs.** `map-rendering-spec.md` §7's own example text violates decision #42 ("not a tourist trap"); the design reference flagged it and this TRD does not reproduce it. That doc's correction is not this task's to make — carried forward in §10.

### 4.3 Local-QA (`[iOS]`)

```swift
struct VisitEvent: Sendable {
    enum Trigger: Sendable { case notificationTap, foregroundArrival, debug }
    let placeID: Place.ID
    let occurredAt: Date
    let trigger: Trigger
}
protocol VisitSource: Sendable { var events: AsyncStream<VisitEvent> { get } }
```

**This protocol is the contract the future dwell detector must satisfy, and the only thing this task requires of it.** The detector, the Always-authorization prompt, the `NSLocationAlwaysAndWhenInUseUsageDescription` string, the background mode, the `UNUserNotificationCenter` request and the notification payload are all outside this task (§1, §10).

```swift
enum LocalQAGate {
    enum Suppressed: Equatable { case alreadyAnswered, notificationsDenied, dailyCapReached }
    enum Decision: Equatable { case offer, suppress(Suppressed) }

    static func decide(
        placeID: Place.ID,
        trigger: VisitEvent.Trigger,
        notificationAuthorization: NotificationAuthorization,   // .notDetermined/.authorized/.denied
        answeredPlaceIDs: Set<Place.ID>,
        lastAskedAt: Date?,
        now: Date
    ) -> Decision
}
```

Precedence, in order (the order is itself the contract — it is what makes the reason deterministic):
1. `answeredPlaceIDs.contains(placeID)` → `.suppress(.alreadyAnswered)` — holds for **every** trigger, including `.debug` (req 8 bullet 4).
2. `trigger != .debug && notificationAuthorization == .denied` → `.suppress(.notificationsDenied)` (req 8 bullet 6 — and there is no other ask anywhere in the app, by construction: `LocalQAToast` has exactly one presenter).
3. `lastAskedAt` within 24h of `now` → `.suppress(.dailyCapReached)`.
4. else `.offer`.

**Rolling 24h, not calendar day. [ASSUMPTION]**, refining the PRD's own — "one per day" is unratified (`ux-flows.md` §9 Q1); a rolling window avoids a burst at local midnight and needs no timezone reasoning. One constant, trivially changed.

```swift
protocol LocalQASyncing: Sendable {
    var state: SyncState { get }        // .disabled / .online / .offline
    func flush(_ records: [LocalQARecord], installID: UUID) async -> Int  // records accepted
}
```
Phase 1 ships `DisabledLocalQASync` — `state == .disabled`, `flush` accepts nothing, the queue simply grows. The confirmation copy is a pure mapping off `state` (D6), so the app never claims a share that did not happen.

### 4.4 `local_qa_answers` — pinned now, built at Phase 2 (`[Backend]`, HELD)

Pinned here so the client's queued payload cannot drift from the eventual table:

```sql
-- migrations/007_local_qa_answers.sql   (number assigned here: 003 hoods attrs,
-- 004 places, 005 events, 006 hoods data are all claimed. chief-of-staff
-- sequences; the number is passed in, never scanned — hood-dataset TRD §3.)
create table public.local_qa_answers (
  place_id    text        not null references public.places(id) on delete cascade,
  -- NOT a foreign key to app_installs, and must never become one. This is the
  -- LocalQA-only install id (D9), a different UUID from app_installs.install_id
  -- by design. An FK here would both fail (the values never match) and, if
  -- "fixed" by unifying the two, create exactly the correlation surface D9
  -- exists to prevent. `analytics/EVENTS.md` line 13 currently claims otherwise
  -- and needs its own correction — see D9 and §10.
  install_id  uuid        not null,
  answer      boolean     not null,
  answered_at timestamptz not null,
  primary key (place_id, install_id)          -- enforces ask-once server-side too
);
alter table public.local_qa_answers enable row level security;
create policy anon_insert_only on public.local_qa_answers
  for insert to anon with check (true);
-- No select policy, for any role. No update, no delete. Insert-only and
-- never client-readable (PRD Technical design). `revoke select` explicitly,
-- rather than relying on the absence of a policy.
```
Client payload, one row per queued answer: `{"place_id":…, "install_id":…, "answer":true|false, "answered_at":"…T19:00:00Z"}` — `answered_at` at hour precision (§3.3).

---

## 5. Flow

**Render (every launch, no trigger):** `HoodCatalog.load()` → `Hood.isTouristTrap` → `TouristFlag` → `FlagStroke.treatment(for:band:)` with the band `HoodLayer` is already handed → stroke. In parallel, `MapZoomTier` from the camera span decides whether the centroid label's second line renders. Moving the time slider changes `band`, which can change a flagged Hood's treatment from `.plain` to `.busyWarning` and back — **and can never change which Hoods have a stroke at all** (§8 D3).

**Place / Hood sheet:** unchanged navigation. `PlaceDetailModal.touristTrapSlot` renders the line when `place.isTouristTrap == true`, nothing otherwise. `HoodSheet` renders its three-state line always (D5).

**Ask loop (Phase 1, debug trigger; Phase 2+, the real detector):**
```
VisitSource emits VisitEvent(placeID, trigger)
  → LocalQACoordinator asks LocalQAGate.decide(...)
      .suppress(reason) → nothing renders, ever; reason is logged at debug level only,
                          never with a coordinate, never in release logging
      .offer            → coordinator sets `pendingAsk`, records lastAskedAt,
                          LocalQAPresenter shows the toast in its passthrough window,
                          posts UIAccessibility .announcement (not .screenChanged — no focus steal)
  → user taps Yes / No  → LocalQAAnswerStore.record(placeID:answer:) (in-memory instant,
                          persistence fire-and-forget with the same generation guard
                          SavedPlacesStore uses) → confirmation line for ~1.6s → dismiss
  → user ignores        → auto-dismiss after 5s; nothing recorded; the place is NOT
                          added to the ledger, so a future visit may ask again — but
                          lastAskedAt was already written, so the cap still applies
  → offline / Phase 1   → identical rendering; the record queues; sync state drives the copy
```
**The ignored case is a real decision, not an oversight:** req 8 bullet 3 says ignoring means no reminder *for that visit*, and req 8 bullet 4 scopes never-again to a place *already answered*. Ignoring is not answering, so the ledger is not written.

---

## 6. Third-party / dependencies

**None added. Nothing Aviran-gated in Phase 1.** `MapPolygon`, `StrokeStyle`, `UIWindow`, `UIAccessibility`, `FileManager`, `AsyncStream` are all platform. `passenger-code/README.md`'s "no third-party packages until a TRD justifies one" stays intact. `UserNotifications` and `CoreLocation` region monitoring are **not** linked by this task — they belong to the detector task (§10).

**Salvage:** `SALVAGE.md` marks `Features/Map/LocalnessBadge.swift` REUSE and the PRD explicitly overrides that to **must not** — it renders the five superseded vibe tags. Nothing is salvaged here. The archive is not reachable from this workspace anyway (same gap T-031/T-032 hit).

---

## 7. Rollout & migration

- **No feature flag on the render side, and none needed.** With every value `null`, the feature renders nothing — the data *is* the off switch, which is also the PRD's own named cold-start risk made literal.
- **No feature flag on the toast either.** It is unreachable without a `VisitSource` emitting, and Phase 1's only source requires a launch argument that no real launch carries.
- **Phase 1 → Phase 2 is three things, all named:** flip `BuildPhase.seedIsAuthoritative` (already the app-wide switch), apply `007_local_qa_answers.sql`, and substitute `DisabledLocalQASync` for the real one. Substituting a real `VisitSource` is the detector task's, not a wiring change here.
- **Migration `006` is regenerated by A1 and stays unapplied.** Applying it is Aviran-gated. Its `on conflict do update` shape means a later apply is idempotent whether or not an earlier version ever landed.
- **Phase-1 acceptance does not cover:** the geofence, the notification, or any server write. §9 marks those rows explicitly rather than letting a green Phase-1 pass imply them.
- **Backward compatibility:** `local-qa.json` absent is a valid first-launch state (empty ledger, no `lastAskedAt`, a fresh install id). A corrupt file degrades to the same, never a crash — matching `SavedPlacesStore.load()`.

---

## 8. Decisions

### D1 — `MapZoomTier` replaces a second boolean
Three tiers are required by `map-rendering-spec.md` §2 and the app has one threshold. One pure derivation, with `showsNames` redefined as `tier == .close`, so pins/name/flag-label/tap-resolution cannot silently disagree. Corrects the design reference's own stroke-threshold claim (§2.3). Existing T-031/T-033 behaviour and tests are unchanged by construction.

### D2 — `FlagStroke` is an enum, so "replaces, never stacks" is a type guarantee
Req 5's real failure mode is a future edit turning one `if/else` into two conditions that both fire. A single-value enum makes that unrepresentable rather than merely tested.

### D3 — Req 2 bullet 3 and req 5 contradict each other as written; this is the reconciliation, and `product` should confirm it
Req 2 bullet 3: *"Moving the time slider repaints heat and changes no stroke: the flag is not time-variant."* Req 5: a flagged Hood **above the busy threshold for the selected hour** gets a distinct stroke. Busy is per-hour, so for a flagged Hood the stroke *does* change with the slider. Both cannot hold literally. `map-rendering-spec.md` §3 and `ux-flows.md` §6 both describe the busy+flagged form as hour-dependent, and both also say the flag itself is not time-variant — so the intended reading is almost certainly about the *value*, not the *form*.

**Built reading, and the falsifiable restatement §9 uses:** for every hour 0…12, the **set of Hoods rendering any flag stroke is identical**; only the stroke *style* of an already-flagged Hood may differ. A not-flagged Hood never acquires a stroke at any hour. **Flagged for `product` at `trd-review`** — if the intent was that the stroke is fully hour-invariant, then req 5 is the requirement that changes, and that is product's call, not something a TRD should decide by picking a favourite.

### D4 — The toast lives in a passthrough `UIWindow`, not a `ZStack` overlay
The design reference specifies a root `ZStack` overlay rendering *over* an open sheet. That does not work: SwiftUI presents `.sheet` in its own presentation host, above the presenting view's overlays — an overlay in `MapScreen` would be hidden behind any open Hood or place sheet, and the notification-tap path foregrounds the app to whatever it was last showing, which can be a sheet. The alternatives are duplicating the toast inside every sheet's content (two live instances, two dismissal timers) or accepting an invisible toast.

**Call:** `LocalQAPresenter` attaches a `UIWindow` at `.normal + 1` to the foreground-active `UIWindowScene`, hosting the toast, with `hitTest` returning `nil` for every point outside the toast's own bounds. Non-blocking (req 8 bullet 1) is then structural — the rest of the screen is not merely undimmed, it never receives the window at all. The window is torn down on dismiss. **Cost, stated:** one UIKit bridge in an otherwise pure-SwiftUI app, and a second window that must be confirmed not to disturb VoiceOver focus — **§9 row 8 sub-check (f)**, added at v2 because v1's §10 cited a focus check that §9 did not actually contain (`trd-review` finding 3). The announcement uses `.announcement`, never `.screenChanged` — **but the notification type is not sufficient on its own.** A `UIWindow` can capture VoiceOver focus through UIKit's own hierarchy-change scanning whatever is posted, so the presentation mechanics are pinned in C12 as build requirements: shown via `isHidden = false`, **never `makeKeyAndVisible`**, `accessibilityViewIsModal` left false, level `.normal + 1`.

### D5 — `HoodSheet` gains a three-state flag line; an architect call, flagged
Req 4 bullet 2: a not-yet-rated Hood *"renders identically to not-flagged, **resolved on tap by the Hood sheet**."* Checked directly: `HoodSheet.swift` has no flag surface of any kind, the PRD's req 6 covers the **place** modal only, and the design reference's §0 explicitly scopes the Hood sheet out. As things stand, req 4 bullet 2 is unsatisfiable — the tap resolves nothing — and it would have shipped as prose no gate could fail (exactly L-018's shape).

**Call:** one line in `HoodSheet`, below the header, always present, three states (§4.2). It is the smallest surface that makes the requirement true and it is the surface the requirement names. **Flagged for `product` and `designer` at `trd-review`**: this is new UI no design doc covers, and the "Not a tourist-heavy spot" string is a copy decision (decision #42-compliant, but nobody has approved this phrasing). Trivially reversible — one `@ViewBuilder` property.

### D6 — The confirmation copy is derived from the sync state, not hardcoded
The design reference gives two strings: "Thanks — shared with other travelers" (online) and "Saved on device — will sync once you're back online" (offline). In Build Phase 1 **neither is true** — there is no server and no eventual sync. Shipping either would be a false claim in the one surface that asks a user for a favour. A third case, `.disabled` → **"Saved on this device."**, and a pure `state → String` mapping. **[ASSUMPTION]** on that third string's wording — `designer`'s to overturn, one line.

### D7 — Phase 1's `VisitSource` is a launch argument, not a hidden gesture
`-simulateLocalQAVisit <place-id>` emits one `VisitEvent(trigger: .debug)` shortly after launch. Same construction as the shipped `-uiTestZoomedIn`, invisible to any real launch, and it makes the whole loop UI-testable and demoable. Rejected: a debug shake gesture (shake-to-decide is a parked Phase-3 concept and a hidden gesture is worse than a hidden argument); an in-sheet debug button (req 8 bullet 6 forbids any in-sheet ask — the code must not contain one even behind a flag, or a future edit un-hides it).

### D8 — The ledger stores answers only; `lastAskedAt` is written on offer
Two different clocks: "never ask about this place again" (answers) and "don't ask more than once a day" (offers). Conflating them into one timestamp would make an ignored toast either silently permanent or silently free. Both are one field each; the split is what makes §9 rows 8's four cases separable.

### D9 — `LocalQAInstallIdentity` stays deliberately separate from `app_installs.install_id`; `EVENTS.md` line 13 is the doc that needs correcting

**The conflict, stated before the call.** `analytics/EVENTS.md` (`passenger-brain 2e38e4b`, 2026-08-01 — one day before this TRD) opens its "Identity constraint (load-bearing)" section with: *"Every table keys on an anonymous `install_id` — **the same identifier `local_qa_answers` already uses** (`prds/tourist-trap-flag/tourist-trap-flag.md`)"*, and defines that identifier at `app_installs.install_id` as *"Client-generated, persisted in SwiftData."* §3.3 of this TRD generates its own UUID into `local-qa.json`. Two independent generation paths cannot yield one value. v1 never mentioned `EVENTS.md`, so nothing in either document forced the question — `trd-review` did.

**Call: the two identifiers are different values, on purpose. `local_qa_answers.install_id` is not `app_installs.install_id` and carries no foreign key to it (§4.4).**

**Why, in the order the reasoning actually runs:**

1. **Unifying them creates a correlation surface neither table has alone.** `app_installs.install_id` is the FK on every row of `app_events` — every screen, search, session and tap in the catalog. `local_qa_answers` is a record that a specific person was *physically present* at a named place at a named hour. Sharing one id would let anyone with backend access join a person's complete in-app behavioural stream to their real-world visit history. That is materially more than either table exposes on its own, and it is the precise thing §3.3's slug-only / hour-truncated / no-Keychain / no-IDFV design is built to avoid. Minimisation that a single join defeats is not minimisation.

2. **Nothing in `EVENTS.md` actually needs the join.** Checked directly against its own KPI list rather than assumed: **Local-QA health** is defined as `local_qa_toast_answered / (local_qa_toast_answered + local_qa_toast_ignored)` — both are rows in **`app_events`**, keyed on the analytics id, carrying `place_id` and `answer` as properties. Participation rate, the one local-QA number `EVENTS.md` says it cares about, is computed entirely inside the analytics tables and never reads `local_qa_answers`. No other rollup in that document touches the table either. So the shared id buys a join that no stated metric consumes.

3. **`local_qa_answers.install_id` is a dedup key, not an analytics key.** Its whole job is the composite PK `(place_id, install_id)` that enforces ask-once server-side (§4.4, and the PRD's own Data model line). Any value stable per install satisfies that. It is never selected — the table has no select policy for any role — so it cannot be joined by the client and is only ever joinable by whoever holds a service-role credential, which is exactly the party point 1 is about.

4. **The PRD does not require unification.** `tourist-trap-flag.md` line 88 asks only for *"an anonymous install id."* Staying separate satisfies the PRD as written; only `EVENTS.md`'s stronger reading is contradicted.

5. **The upstream source of `EVENTS.md`'s own claim is weaker than the claim.** `.claude/agents/analytics-engineer.md` (mirrored at `agent-os/agents-mirror/analytics-engineer.md:30`) says every table keys on an anonymous install id, *"the same **pattern** `local_qa_answers` already uses."* **Pattern**, not identifier. `EVENTS.md` line 13 tightened "pattern" into "the same identifier" while citing the PRD, which never said it. That reads as a drafting slip rather than a considered identity decision — which is one more reason to correct the line rather than build to it.

**What this costs, stated rather than buried:** you cannot ask "did the installs that answer local-QA prompts retain better?" by joining `local_qa_answers` to `app_events`. If that question ever becomes worth answering, the answer is **not** to merge the ids — it is to log the already-specified `local_qa_toast_answered` event into `app_events` (it is in the catalog today) and analyse it there, which yields the same behavioural insight without ever putting the visit record and the behavioural stream under one key. That path is available now and needs no schema change.

**Two corrections this decision owes to other documents. Named here, not made here — neither is `architect`'s file:**

- **`analytics/EVENTS.md` line 13 is wrong as written** and must be corrected by its owner, `analytics-engineer`. Suggested replacement, offered as text rather than an edit: *"Every analytics table keys on an anonymous `install_id`, the same **pattern** `local_qa_answers` uses. The two are **different values on purpose** — `local_qa_answers` carries its own install-scoped id and no FK to `app_installs`, so a physical-visit record can never be joined to the behavioural stream (`prds/tourist-trap-flag/TRD.md` D9)."*
- **`EVENTS.md` line 22's "persisted in SwiftData" is also unbacked**, found while checking the above: `grep -rn "SwiftData\|@Model" passenger-code/Passenger/` returns **zero hits** — the app uses no SwiftData anywhere, and every shipped store (`SavedPlacesPersistence`) is an actor over Application Support JSON. Flagged for the same owner as a separate, smaller correction. It does not affect this TRD, which specifies its own storage in §3.3.

**Reversibility:** if `product` or `analytics-engineer` overturns this and wants the ids unified, the change is one type and one call site on the client plus an FK in `007` — cheap. It is the *correlation consequence* that is not reversible once real answers are collected under a shared key, which is why the default here is the separating one. **Flagged for `analytics-engineer` at `trd-review`** as the owner of the doc being contradicted.

---

## 9. Verification — one row per P0 requirement

Per `architect.md` (L-018): every P0 names an observable, a pass condition, and the layer. `qa` builds `prds/tourist-trap-flag/TEST-PLAN.md` from this table. **No row's pass condition is "looks right."**

**Standing rule, ratified workspace-wide 2026-08-07 — a check sequenced behind a known-failing sibling is unrun, not passed.** (`product` at T-077/`PAS-51` acceptance; `architect` ratification; canonical text in `architect.md` §9, lifted in here because `qa` reads this table on its own.) Under `continueAfterFailure = false` — set by eight of this repo's ten `PassengerUITests` classes — and equally under `try #require`, `XCTUnwrap`, or an early `return` inside a shared assertion helper, the *first* failing assertion aborts every assertion after it in that method, while `xcodebuild` still reports **one** failure line for the whole method. A gate that counts failure lines reads that silence as a pass. **So no check in this table may share a test method with an assertion that is known to fail and is owned by another ticket** — move the known failure into its own method, where it stays visibly red and tracked while its siblings still execute. Any report on this table states, per sub-check, *that it executed*; a sub-check whose execution cannot be shown in the result bundle is **unrun**, exactly like a BLOCKED row. **`XCTExpectFailure` is not the fix** — it turns the method green and buries the tracked gap. **Audited against this rule in the same pass:** no row here is currently discharged in a test method carrying a disclosed known-failing assertion, so no row moves; the rule binds any future one.

| P0 | Observable | Pass condition | Layer | Step |
|---|---|---|---|---|
| **1** One boolean per Hood/place; no graduated value; no banned strings; Hood flag never aggregated | (a) `TouristFlag`/`FlagStroke` case counts; (b) every output of `FlagCopy` + `HoodSpeech` over all 12 inputs; (c) a grep of the diff | (a) `FlagStroke` has exactly 3 cases and `treatment` is total; (b) zero case-insensitive matches for "tourist trap", "local", "mix", "touristy", "super local" as a *tag value*; (c) no function anywhere takes `[Place]` and returns a Hood flag | unit + review | C2, C3 |
| **2** Flag never shares a channel with heat; readable without hue; not time-variant | (a) `HoodLayer`'s fill vs. stroke arguments; (b) the three stroke treatments with the colour catalog forced to greyscale; (c) the set of Hoods with a non-`.none` treatment, computed at all 13 hours | (a) fill is `HeatPalette` only, stroke is `Color("Flag")` only, in one file, no shared expression; (b) all three distinguishable by weight and dash alone; (c) **identical set at every hour** — the D3 restatement; only `.plain`↔`.busyWarning` may differ | unit + manual | C2, C5 |
| **3** Zoom disclosure matches `map-rendering-spec.md` §2 row for row; no pin carries the flag | (a) `MapZoomTier.tier(forLatitudeDelta:)` swept across both boundaries incl. exact-threshold values; (b) `HoodLayer` render at each tier; (c) `PlaceLayer`'s diff | (a) three distinct tiers, boundaries exclusive/inclusive as specified, no fourth outcome; (b) cityWide → no stroke and no label on *any* Hood; neighborhood → stroke+label on flagged only; close → stroke, no label; (c) `PlaceLayer.swift` unmodified by this task | unit + UI test + review | C1, C5 |
| **4** Not-flagged and not-yet-rated both render blank; storage still distinguishes them | (a) `FlagStroke.treatment` rows for `.notFlagged` vs `.unrated`; (b) `HoodSpeech` for the same two; (c) `HoodSheet`'s line for the same two | (a) identical in all 4 band columns; (b) **different** strings; (c) **different** strings ("Not a tourist-heavy spot" vs "No local rating yet") — this is the "resolved on tap" check, and it fails outright without D5 | unit + UI test | C2, C3, C8 |
| **5** Busy+flagged replaces, never stacks; its own label; busy-not-flagged gets nothing | (a) the return type of `treatment`; (b) a flagged Hood at a `.busy` seed hour vs. an adjacent non-busy hour; (c) a not-flagged Hood at a `.busy` hour | (a) one value, not a set/option-set — stacking is unrepresentable; (b) dashed 3pt vs solid 2.5pt, and the label reads "Busy and tourist-heavy" as one string; (c) `.none`, no warning of any kind | unit + manual | C2, C5, **needs T-032 C10** |
| **6** One line in the place modal, nowhere else; independent of the closed badge | (a) `touristTrapSlot` with `true`/`false`/`nil`; (b) a grep for `FlagCopy.placeLine` call sites | (a) one line with icon+text / nothing / nothing, and the modal's height is unchanged in the two absent cases; (b) exactly one call site; `permanentlyClosed` (T-036) is referenced nowhere in this task's diff | unit + UI test + review | C7 |
| **7** VoiceOver states the flag even when nothing renders; unrated says so distinctly; busy+flagged has its own label; pins never announce it | (a) `HoodSpeech` over all 12 (flag × band) inputs; (b) the `.cityWide` annotation element; (c) `PlaceLayer`/`PlaceHitTester` accessibility labels | (a) 12 non-empty outputs, one flag clause each, `.flagged`+`.busy` is a single combined sentence and not a concatenation of the two other forms; (b) the 1×1 clear element still carries the full label at city-wide zoom, where no stroke renders; (c) unchanged — "name, category" only | unit + manual | C3, C5 |
| **8** Binary, post-visit, asked once; ignore auto-dismisses with no reminder; answered place never fires again; offline still renders and queues; denied has no fallback anywhere; daily cap; **the toast never steals VoiceOver focus** | (a) `LocalQAGate.decide` over the full input matrix (3 triggers × 3 auth × answered/not × cap/not); (b) launch with `-simulateLocalQAVisit`, answer Yes, relaunch same place; (c) launch, ignore, wait; (d) a grep for toast presenters; (e) the queue after an answer with `DisabledLocalQASync`; **(f)** `UIAccessibility.focusedElement(using: nil)` sampled immediately before the toast is presented and again ~1s after, with VoiceOver on, plus a grep of `LocalQA/`'s diff for the notification and window-presentation calls | (a) matches §4.3's precedence table exactly, every row, incl. `.alreadyAnswered` winning over `.debug`; (b) toast appears the first time, never the second, and `.suppress(.alreadyAnswered)` is the recorded reason; (c) toast gone after ~5s, no record written, `lastAskedAt` **is** written, no second toast; (d) exactly one `LocalQAToast` presenter in the app and zero references to it from `Detail/`; (e) exactly one queued record, unsent; **(f) the focused element is the same object before and after** — focus does not move to the toast or anywhere else, and the element that had focus is still focused and still traversable; **exactly one `UIAccessibility.post` call in `LocalQA/`, with `notification: .announcement`; zero occurrences of `.screenChanged`, `.layoutChanged`, `makeKeyAndVisible`, or `accessibilityViewIsModal = true` anywhere in the presenter (D4, C12).** Run in both the no-sheet and open-sheet cases, since the sheet is the reason D4 needs a window at all | unit + UI test + **manual (VoiceOver on, Accessibility Inspector)** + review | C9–C13, **C12** |
| **8-trigger** *(the geofence/notification leg)* | — | **Not verifiable in Build Phase 1 — not built here** (§1). Carried to the shared dwell-detector task; Phase-1 acceptance must not be read as covering it | — | — |
| **9** An answer is a signal, not a write; recorded even when it agrees | (a) the **declared signatures and stored properties** of `FlagStroke.treatment(for:band:)` and `HoodSpeech.label(name:band:flag:)`, plus `LocalQA/`'s import list; (b) answer Yes on a place whose flag is already `true`; (c) the rendered flag before/after any answer | (a) **neither render function takes `LocalQAAnswerStore`, `LocalQARecord`, nor any type declared in `LocalQA/` as a parameter, and neither owning type stores a reference that reaches one — signatures byte-identical to §4.1/§4.2. `LocalQA/` imports neither `Hoods/` nor `Map/`, and references `Places/` only for `Place.ID`.** A blocking review finding for any violation of *those* rules. **`MapScreen` holding both a catalog and (via `LocalQACoordinator`) the answer store is expected composition-root wiring and is explicitly NOT a finding** — see §2.2; v1's broader "no type holds both" phrasing was false against `MapScreen.swift:43,60` and is not what this row checks; (b) a record exists with `answer == true`; (c) byte-identical `FlagStroke`/modal line before and after | review + unit | C9, C10 |

---

## 10. Risks and alternatives

| Risk | Mitigation / decision |
|---|---|
| **The proposing algorithm does not exist, so every real flag value is `null`** — the PRD's own headline risk | Not solved here and not solvable here. A1's fake seed makes the *feature* demonstrable in Phase 1; it does not make the *signal* real, and this TRD does not claim otherwise. Aviran's call, already on `PAS-6` item 13. |
| A fake seed makes the feature look verified when only the seed path is | §7 states plainly that Phase-2 acceptance re-runs reqs 1–7 against real values. The seed is named in A1, in the source file, and in `qa`'s plan — never invisible. Same posture T-032's D10 took. |
| **Req 5 is unobservable until T-032's density seed lands** | Named, not worked around. §9 row 5 lists C10 as its precondition; §11 states the build-order consequence. Duplicating a density seed in this task was rejected — two seeds is two chances to disagree. |
| Hand-editing `hoods-tel-aviv.json` instead of the source (L-024) | A1 is written as "edit the source, re-run the generator", and `qa`'s check is a regeneration round-trip to a scratch path — the exact check that caught L-024. **Precision fix at v2, from the A1 review (`code-reviewer` `passenger-brain 864b8ea`, concurred by `data-engineer`): the round-trip is byte-identical for `006_hoods_tel_aviv_data.sql` but NEVER for the JSON bundle**, because `build_hoods.py`'s `build_bundle()` stamps `generatedAt` from wall-clock time rather than source content. `qa` must normalise or exclude that one field; a literal full-file diff fails on every run, which either cries wolf or trains its reader to eyeball past exactly the kind of drift L-024 was. Fixing the generator to derive `generatedAt` from the source digest is the cleaner option and is `data-engineer`'s call, not made here. |
| Regenerating `006` changes an unapplied migration under T-040's feet | `006` is unapplied and its insert is `on conflict do update`; the regeneration is deterministic from the source. Cross-check with T-040's owner at `trd-review`. |
| **Req 2 bullet 3 vs req 5 contradiction** | D3 — reconciled reading built, restated falsifiably, flagged to `product` rather than resolved unilaterally. |
| **Req 4 bullet 2 has no surface** | D5 — the smallest surface that makes it true, flagged to `product`/`designer` as new UI no design doc covers. |
| A second `UIWindow` disturbs VoiceOver focus or the status bar | D4's cost, stated — and now actually checked. **§9 row 8 sub-check (f)** samples `UIAccessibility.focusedElement` before and after the toast appears with VoiceOver on and requires it unchanged, and greps for the mechanics that would move it. The notification type is only half of it: a new window can pull focus through UIKit's own hierarchy scan regardless of what is posted, so **C12 pins the presentation mechanics too** — window shown via `isHidden = false`, **never `makeKeyAndVisible`**, `accessibilityViewIsModal` left false, level `.normal + 1`. **v1's version of this row cited a check in §9 row 8 that row 8 did not contain** (`trd-review` finding 3); (f) is that check, now real. If it proves troublesome the fallback is an overlay that renders under sheets — a visible regression, not a silent one. |
| **The local-QA install id and the analytics install id are silently assumed to be the same value** | **D9** — they are deliberately different, and the reasoning, the accepted cost, and the reason unification is the dangerous direction are all written down rather than left implicit. `analytics/EVENTS.md` line 13 states the opposite and **is named as needing its own correction by `analytics-engineer`**, with suggested replacement text in D9; line 22's "persisted in SwiftData" is separately unbacked (zero SwiftData in `passenger-code`) and flagged to the same owner. §4.4's SQL carries an inline comment so the no-FK rule survives contact with whoever writes `007` at Phase 2. |
| The local-QA file is a record of where a person physically was | §3.3 — slug only, hour-truncated, backup-excluded, file-protected, install-scoped UUID that dies with the app. The minimisations are build steps, not principles. |
| **Always-authorization + background location is an App Store and privacy surface nobody owns yet** | Explicitly out of this task. The detector needs a new Info.plist usage string, a background mode, a permission moment (and the strategy forbids onboarding, so *when* to ask is an open product question), and `UNUserNotificationCenter` authorization. Recommended as its own board row with `data-engineer` as owner — it is named in three PRDs (T-035/T-036/T-037) and owned in none. |
| Nothing rewards answering, so the loop may simply not run | The PRD's own open question, Aviran's. Unchanged here. |
| `map-rendering-spec.md` §7's example text still violates decision #42 | Not this task's doc. This TRD's own strings are compliant and §4.2's grep test proves it. Carried forward for that doc's owner (also flagged by the design reference, §2.3 issue 1 — two flags, still no owner). |
| Notification-denied users are never asked, ever | Named coverage gap in the PRD (`ux-flows.md` §9 Q8). Req 8 bullet 6 forbids a fallback, so the gate enforces it and §9 row 8(d) proves no second ask surface exists. |

**Alternatives considered and rejected:** a `ZStack` overlay for the toast (invisible behind sheets — D4); duplicating the toast into every sheet's content (two live instances, two timers); reusing `showsNames` for the flag stroke (collapses the Neighborhood tier — D1/§2.3); an options-set or two booleans for the stroke state (lets busy+flagged stack — D2); a Keychain-backed install id (survives reinstall, a stronger identifier than the feature needs — §3.3); IDFV/IDFA (same, plus a privacy-manifest surface); **sharing `app_installs.install_id` with the analytics stream (D9 — it would let a physical-visit record be joined to a person's entire in-app behaviour, and no KPI in `EVENTS.md` needs the join, so the cost buys nothing);** minute-precision timestamps (a movement log — §3.3); a debug shake gesture or an in-sheet debug ask (D7); hardcoding the online/offline confirmation copy in Phase 1 (claims a share that never happens — D6); seeding Hood flags by hand-editing the bundled JSON (L-024 — A1); a second density seed in this task (T-032 owns it); building a real geofence detector inside T-035 (forks a component the PRD assigns to one owner across three consumers).

---

## 11. Build breakdown

Ordered. Tags are the dispatch instruction.

| # | Step | Tag |
|---|---|---|
| **A1** | **Seed plausible fake Hood flags.** Edit `database/data/hoods-tel-aviv.source.json` to §3.2's authoring rule (≥1 flagged-and-busy-in-T-032's-seed, ≥1 flagged-never-busy, ≥1 explicit `false`, ≥1 `null`, ≤4 flagged of 24), then `build_hoods.py --migration-number 006`. **Never hand-edit `hoods-tel-aviv.json`.** Migration stays unapplied. Coordinate the flagged ids with T-032's `density-seed-tel-aviv.json`; whichever lands second reconciles | **[Algo/Data]** |
| **B1** | `007_local_qa_answers.sql` — §4.4 verbatim: composite PK, RLS on, insert-only `anon` policy, **no** select policy and an explicit `revoke select`. **HELD — Build Phase 2, do not dispatch in Phase 1** | **[Backend]** |
| C1 | `MapZoomTier` + boundary-value tests; rename `nameLabelSpanThreshold` → `closeSpanThreshold`; add `neighborhoodSpanThreshold`; redefine `showsNames` as `tier == .close`. No behaviour change to T-031/T-033 paths — their tests must pass unmodified | **[iOS]** |
| C2 | `Flag/TouristFlag.swift` — `TouristFlag`, `FlagStroke`, `treatment(for:band:)`; the full 3×4 matrix test (§9 rows 1, 2, 4, 5) | **[iOS]** |
| C3 | `Flag/FlagCopy.swift` + `Flag/HoodSpeech.swift` — every string in one place; the 12-input speech test and the banned-substring grep test (§9 rows 1, 7) | **[iOS]** |
| C4 | `Flag.colorset` (light `#A15C00`, dark `#F0B429`) + a `ContrastRatio` test in both `UIUserInterfaceStyle`s: label text ≥4.5:1 over `Surface` and over the app background, stroke ≥3:1 | **[iOS]** |
| C5 | `HoodLayer` — stroke from `FlagStroke`, the second capsule line at `.neighborhood` only, `voiceOverLabel` → `HoodSpeech`. The city-wide 1×1 accessibility element keeps its full label (§9 row 7b) | **[iOS]** |
| C6 | `Place.isTouristTrap` + decode on all three `PlaceCatalog` paths (seed/live/cache, incl. `PlacesCache.CachedPlace`) + seed values in `Resources/places-tel-aviv.json` per §3.2 | **[iOS]** |
| C7 | Fill `PlaceDetailModal.touristTrapSlot` — `camera.fill` + "Tourist-heavy spot", conditioned on `== true`; nothing rendered and zero height otherwise (§9 row 6) | **[iOS]** |
| C8 | **`HoodSheet` three-state flag line (D5)** — flagged / not flagged / no local rating yet, always present, below the header | **[iOS]** |
| C9 | `LocalQAInstallIdentity` (**named that way on purpose — it is not `app_installs.install_id`, D9**) + `LocalQAAnswerStore` + its actor persistence — ledger, queue, `lastAskedAt`, generation guard, backup exclusion, file protection, hour truncation; missing/corrupt file degrades to empty (§3.3) | **[iOS]** |
| C10 | `LocalQAGate` — pure, plus the **full** input-matrix test (3 triggers × 3 auth states × answered/not × cap/not), precedence order asserted (§4.3, §9 row 8a) | **[iOS]** |
| C11 | `VisitEvent`/`VisitSource` + `DebugVisitSource` + the `-simulateLocalQAVisit` launch argument + `LocalQACoordinator` (one pending ask, never two) | **[iOS]** |
| C12 | `LocalQAToast` + `LocalQAPresenter` passthrough window (D4) — top-anchored, safe-area-respecting, ≥44pt equal-weight Yes/No, Reduce-Motion cross-fade, 5s auto-dismiss, 1.6s confirmation then dismiss. **VoiceOver-focus mechanics are part of this step, not a review note (§9 row 8f):** window level `.normal + 1`, shown with `isHidden = false` and **never `makeKeyAndVisible`** (a key window pulls VoiceOver focus regardless of what notification is posted), `accessibilityViewIsModal` left **false** on the hosting view, and exactly one `UIAccessibility.post(notification: .announcement, ...)` — `.screenChanged`/`.layoutChanged` appear nowhere in this file. **Not done until 8(f) passes** | **[iOS]** |
| C13 | `LocalQASyncing` + `DisabledLocalQASync` + the `state → confirmation string` mapping and its test (D6) | **[iOS]** |
| C14 | UI test end-to-end: `-simulateLocalQAVisit` → toast → Yes → relaunch same place → no toast; and a second launch that ignores it → auto-dismiss, no record, cap written (§9 row 8b/8c) | **[iOS]** |

**Order:** C1→C5 (render), C6→C8 (sheets), C9→C14 (ask loop). A1 any time, but **before** `qa` — every render check is vacuous against an all-`null` bundle. C2 and C10 first within their groups: they are the two pure types that hold every rule, and both are testable with no simulator.

**`trd-review` sign-off needed from:**
- **`ios-developer` + `ios-code-reviewer`** — C1–C14 (the bulk of the task). **At v2 this is a re-review of the three fixes (D9 / §2.2+§9 row 9a / §9 row 8f + C12), not of the whole TRD again** — nothing else was redesigned.
- **`analytics-engineer`** — **new at v2. D9** contradicts `analytics/EVENTS.md` line 13, which that agent owns. The TRD does not edit that file; it states the conflict, makes its own call, and offers replacement text. If `analytics-engineer` disagrees with D9's direction, that is the moment to say so — not after real answers are collected.
- **`data-engineer` + `code-reviewer`** — A1 (dataset authoring + generator round-trip). **Already CLEARED** (`passenger-brain 864b8ea` + `data-engineer`, both APPROVE WITH MINORS); v2 reopens nothing in A1 and only corrects §10's description of `qa`'s round-trip check per that review's own finding 1.
- **`developer` + `code-reviewer`** — B1 (the held migration and its RLS; worth `security-auditor`'s eye too, since insert-only-never-readable is the whole protection and a missing `revoke select` would expose a visit log).
- **`product`** — three architect calls that touch scope, none of them decided unilaterally: **D3** (req 2 bullet 3 vs req 5 contradiction), **D5** (the new Hood-sheet surface req 4 bullet 2 requires and no doc specifies), and **§1's Phase-1 boundary** (the geofence/notification leg is not built here, so Phase-1 acceptance does not cover req 8's first bullet).
- **Two cross-checks worth one explicit pass:** **T-032's TRD** §3.4/C10 (the density seed A1's flagged-and-busy Hood depends on) and **T-040's** owner (regenerating `006`).
