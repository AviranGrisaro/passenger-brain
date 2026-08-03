# Places — Been & Saved — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Closed-place case resolved:** decision #38 — a permanently-closed place can still be saved and carries a distinct badge, unrelated to the tourist-trap flag. That was the item holding this PRD at PAS-10.

## Description

- One list, named **Places**, opened from a persistent icon in map chrome (decision #26, `design/ux-flows.md` §2).
- Three ways in: manual **Saved**, dwell-triggered **Been** (20+ verified minutes), plain geofence **Visited**.
- Each row carries one provenance word, so a deliberate choice never reads identically to one that saved itself (#30).
- A place Apple Maps marks permanently closed **can still be saved**, with a distinct "permanently closed" badge on its row (#38).
- Places in the list also render as a ring accent on the existing pin, close zoom only (`design/map-rendering-spec.md` §6).
- **Not in scope:** Passport stickers and per-Hood status (own PRD, consuming the Been signal from here); the local-QA toast (tourist-trap PRD, same detector); the place modal's own contents (`hood-place-detail`); TikTok import as a fourth entry path (PAS-6 item 9); the badge's exact visual and copy (designer's, per #38); any share or export affordance.

## Motivation

- Strategy, verbatim: *"**"Been" and "Saved" places, visually/functionally distinct** (decision #26, extended 2026-07-30)."*
- Strategy, verbatim: *"a place Apple Maps marks permanently closed can still be saved — the UI shows a distinct "permanently closed" badge, unrelated to and not folded into the tourist-trap flag."*
- It is the only V1 surface that survives a session — the return path for someone who already chose (`ux-flows.md` Journey 3).
- Business model names it inside the permanently-free core.

## Requirements

### Must-have (P0)

1. **One list, three provenance states, one word per row.**
   - [ ] The list is titled **Places** (`ux-flows.md` §9 Q11).
   - [ ] Every row shows exactly one of **Saved / Been / Visited** — never two, never none.
   - [ ] Precedence when several apply: Saved beats Been beats Visited.
   - [ ] One place produces exactly one row, however many paths touched it.
   - [ ] Saved and Been are distinguishable by word, not colour alone (#30, `design-principles.md` §3).

2. **Manual save responds instantly and persists.**
   - [ ] Saving from the place modal adds a Saved row and shows the saved state in under 400ms, before any network round trip (`design-principles.md` §2).
   - [ ] Reopening the place shows it as saved.
   - [ ] Un-saving drops the Saved label; if Been or Visited also applies, the row remains with the next word down. **[ASSUMPTION]**

3. **Been requires a verified 20-minute dwell at a place Passenger already knows.**
   - [ ] Auto-save fires only for places already in Passenger's places table — a home, office, or friend's flat never enters the list at any dwell length (#26's load-bearing guard).
   - [ ] The threshold is 20 minutes; verified presence below it logs **Visited**.
   - [ ] A Been row appears without the user acting, and never asks for confirmation.
   - [ ] Revisiting a Been place adds no row and changes no label.

4. **Permanently-closed places save, and say so on the row.**
   - [ ] Saving a permanently-closed place succeeds — no block, no dialog that prevents it (#38).
   - [ ] Its row renders a distinct "permanently closed" badge, readable from the list without opening the place.
   - [ ] The badge is visually distinct from the tourist-heavy line and never substitutes for it — the two are independent (#38). **The two are never compared on a Places row**: the tourist-heavy line lives in the place detail modal "and nowhere else" (`tourist-trap-flag` req 6, `map-rendering-spec.md` §4), so this bullet is verified in the modal, and a Places row renders the closed badge only. *(Ruled at acceptance 2026-08-03 — the two PRDs contradicted each other and the build reserved a permanently-empty slot on the row to satisfy both.)*
   - [ ] A place that closes *after* being saved shows the badge next time the list renders, not only at save time.
   - [ ] The badge never removes the row and never disables the route action.

5. **Degraded permission degrades this feature, never breaks it.**
   - [ ] With Location Always denied, manual Saved works fully; Been and Visited never populate, with no error copy.
   - [ ] With location denied entirely, the list still opens and shows saved rows.
   - [ ] No path here re-asks a permission already denied (`ux-flows.md` §3).

6. **Empty and offline states are plain, not errors.**
   - [ ] An empty list shows a plain empty state naming what would fill it (`design-principles.md` §4) — its copy must state the three ways a place gets here (save one, or spend time at one), not only that the list is empty. *(Pass condition sharpened at acceptance 2026-08-03: the TRD's §9 row 6 dropped "naming what would fill it" and checked only icon + line + CTA, so no gate could fail the shipped "Nothing here yet." With no onboarding in V1, this empty state is the only place the feature can explain itself. L-009.)*
   - [ ] Offline: existing rows render from device, and an offline save appears immediately. ~~and syncs later~~ — **struck at acceptance 2026-08-03**: V1 writes nothing server-side (see Technical design), so there is no sync to perform and no offline banner ships (TRD D5, confirmed). Restore this clause only when a server copy of provenance exists.
   - [ ] A row whose place has no current-hour density still opens; the heat readout says so rather than blocking (Journey 3).

7. **The map accent is binary** — rendering per `map-rendering-spec.md` §6.
   - [ ] A listed place gets a ring accent on its pin at close zoom only, and the accent never encodes which provenance — that is list-only.
   - [ ] It pairs with a shape or icon difference, so it isn't colour-only (`ux-flows.md` §2.1).
   - [ ] The pin's touch target stays ≥44pt with the ring applied; cluster markers never indicate a personal place is inside (§5).

8. **A row is a shortcut straight to the place.**
   - [ ] Tapping a row opens that place's detail modal, skipping the Hood sheet (Journey 3).
   - [ ] Places is one of the mutually exclusive nav modals — search, heat, or Passport closes it, and vice versa (§2.1).
   - [ ] Dismissing returns to the map with camera and selected hour unchanged.

### Nice-to-have (P1)

- Filtering or sectioning by provenance; a per-city section once a second city exists.
- Opening hours on the row where the curated dataset carries them.

## Technical design

- **Data model:** one row per (place, provenance), precedence applied at read time rather than by overwriting — so a manual save never destroys the record that a dwell happened. Fields: place_id, provenance enum {saved, been, visited}, created_at.
- **Data model:** closed state belongs to the place, not the entry — `places.permanently_closed`, refreshed from Apple Maps, so no two surfaces disagree.
- **Data sourcing (added 2026-07-30, standing rule).** The `places` table does not exist and this PRD does not author it — rows, coordinates, categories and `permanently_closed` are [`prds/places-dataset/`](../places-dataset/places-dataset.md)'s deliverable (its req 5 carries the closed-state field, its source, a `closed_checked_at` staleness stamp, and the refresh cadence). **Req 4's fourth bullet needs that refresh to exist:** a place that closes *after* being saved cannot show the badge on next render if closed state is only read once at authoring time. That refresh currently has no owner and no cadence — raised below.
- **Storage — the load-bearing call.** V1 adds no accounts (strategy: *"no accounts/login added"*), so the list is **device-local** (SwiftData/Core Data): no per-user server table, no RLS surface. Consequence, stated rather than hidden: **it does not survive reinstall or a new device.**
- **APIs / contract:** reads the shared static `places` payload for name, category, coordinates, closed state. Writes nothing server-side in V1.
- **Architecture notes:** `SALVAGE.md` marks `Models/VisitedPlace.swift`, `Services/SavedPlacesStore.swift`, `Features/Places/SavedPlacesSheet.swift`, `PlaceDetailCard.swift` REUSE; `VisitedPlacesStore.swift`, `VisitDetectionService.swift`, `CityGeofenceMonitor.swift` REFERENCE only — entangled with logic the old repo scoped to Phase 3. `AuthService.swift` is BURN: *"spec it fresh — anonymous-first."*
- **Dependencies:** `map-hoods-heat` (pins, ring channel) and `hood-place-detail` (the save affordance) first. **One dwell/geofence detector serves three consumers** — this list, the local-QA ask, Passport's stickers. `data-engineer` owns it; it must not be built three times.
- **Open technical questions:** where Apple Maps closed state is read (client `MKMapItem` lookup vs. a refreshed column) and how stale it may be; whether provenance rows need a server copy for the localness pipeline; what happens to a listed place later dropped from the dataset.

## Assumptions

- **[ASSUMPTION]** Device-local storage with no anonymous server identity, so the list is lost on reinstall. This follows from "no accounts," but nobody confirmed the loss is acceptable.
- **[ASSUMPTION]** Closed state is cached from Apple Maps, so a newly-closed place may show the badge late.
- **[ASSUMPTION]** Un-save behaviour (req 2) — chosen for consistency with precedence, not specified upstream.

## Open questions & risks

- **Reinstall loses everything collected.** Places and Passport both vanish on device change. The alternative is anonymous server identity, which strategy parks until Phase 3 — Aviran's call, not a build decision.
- **Background Location Always reliability** is load-bearing for Been and Visited both (`ux-flows.md` §9 Q4); needs the architect's read.
- **Permission sequence is a proposal, not a decision** (§9 Q10) — three system permissions for a product whose #8 rules out a permission gate.
- ~~**Row density risk:** a row can carry a provenance word, a closed badge, and a tourist-heavy line at once~~ — **resolved at acceptance 2026-08-03**: the row never carries a tourist-heavy line (req 4 bullet 3 above), so the worst case is a provenance word plus a closed badge — one special element, within `design-principles.md` §2.
- **The closed-state refresh has no owner and no cadence.** Req 4 requires a place that closes after being saved to badge on next render; nothing schedules the check that would make that true. Spec'd as a field in `places-dataset` req 5, but the job that runs it is unassigned. `data-engineer`'s or `developer`'s — needs assigning before this feature's req 4 can be QA'd honestly.
- **Visited is the weakest of the three** — a row the user never chose, for somewhere they walked past. No upstream decision addresses pruning it.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | Decision #38 resolved the closed-place case held at PAS-10 (PAS-6 item 2) |
| 2026-07-30 | Closed state spec'd on the place, not the saved entry | #38: "a factual state about the place, not a judgment about its character" |
| 2026-07-30 | Badge visual and copy deliberately unspecified | #38 assigns both to `designer` |
| 2026-07-30 | Device-local storage spec'd, reinstall consequence raised as an open question | Strategy locks "no accounts/login added"; the data loss is Aviran's to accept or reject |
| 2026-07-30 | Data-sourcing bullet added; closed-state refresh promoted from an open *technical* question to a named ownerless job | Standing rule, founder-direct 2026-07-30. "Refreshed from Apple Maps" was stated as a property of the column, with nothing scheduled to do the refreshing — req 4's fourth bullet silently depended on it |
| 2026-08-03 | **Acceptance REJECT** — req 6 bullet 1 fails; back to `build` | Shipped empty state reads "Nothing here yet" + "Explore the map" and names nothing that would fill the list. One string. Full findings in `agent-os/PROGRESS.md`, this date |
| 2026-08-03 | **D4 CONFIRMED** — name-ascending sort, recency rejected | The PRD specifies no order at all, so this is the architect filling a gap, not deviating. Recency would force a versioned-payload migration on already-shipped accepted state to store a timestamp nothing else needs. Name-ascending is stable, scannable, and the only order the current record shape can produce without a migration. If Aviran wants recency, it is a schema change, not a sort change |
| 2026-08-03 | **D5 CONFIRMED** — no offline banner ships, and req 6 bullet 2 corrected to match | Not a silent gap: a banner in V1 would announce a sync the app never performs. The PRD's own Technical design already said "Writes nothing server-side in V1" — the requirement contradicted it |
| 2026-08-03 | **D7 CONFIRMED** — Places is bucket-2 chrome, not a nav-row button; T-032's D1 was wrong | `ux-flows.md` line 46 is explicit: "Saved-places icon (4th icon) — persistent icon, **separate from the 3 nav buttons**." Checked against the doc, not against D7's citation of it. Accepted cost: the icon fades and stops hit-testing while any surface is presented, so it cannot dismiss its own list and cannot be reached from an open heat/search/Passport surface. Acceptable — the list carries three dismissal paths (scrim tap, drag-down, ✕) and req 8 bullet 2 asks only for mutual exclusivity. The "can't reach Places without first closing another surface" wrinkle goes to the post-ship designer pass |
| 2026-08-03 | **§9 row 5's framing CONFIRMED as honest** — with one PRD correction owed | Req 5's Been/Visited bullets are checked in Build Phase 1 as the absence of any location code path in the feature (verified independently: zero `LocationStore` references and no `CoreLocation` use in `Places/` beyond `CLLocationCoordinate2D` types). This is genuinely what the requirement protects — no location-derived row can appear when permission is denied, because no row is location-derived at all. It is **not** the runtime behaviour the bullet describes: the bundled fixture populates Been/Visited regardless of permission. That is Build Phase 1's declared fake-data scope, not a gap, and it is re-verified as runtime behaviour when the real detector lands (`T-046`/`PAS-33`) |

