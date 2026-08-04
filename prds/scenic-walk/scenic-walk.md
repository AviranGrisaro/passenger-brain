# Scenic Walk — lighter version (route-preview comparison) — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#strategic-phasing)
**Build phase:** 1 — client-side only, no backend (`agent-os/BOARD.md` § V1 Build Phases). Req 8 is the one Phase-1 fixture it needs.
**Owner:** Aviran Grisaro
**Linear:** [PAS-46](https://linear.app/passenger-app/issue/PAS-46/scenic-walk-lighter-version-route-preview-comparison) · **Board:** T-057
**Last updated:** 2026-08-04
**Scope ruling:** decision #44 picks the *lighter* version; decision #32's weighted street-segment routing is explicitly not what this specs.

## Description

- Two walking routes for the same A→B, shown for comparison: **Fast route** and **Scenic route**.
- Both come from the platform's own walking-directions API. Passenger computes no route.
- "Scenic" is that same request through 1–2 waypoints biased toward Hoods not flagged tourist-heavy.
- Preview only: "Go" hands off to native Maps or Waze for the walk itself (decision #19, unchanged).
- **Not in scope:** in-app turn-by-turn, voice, or rerouting; a custom routing engine, OSM extract, or self-hosted GraphHopper/Valhalla/OSRM; per-street Attractiveness weights (decision #32's heavier version, declined by #44); a dedicated routing screen or a third in-app depth; Hood-to-Hood or multi-stop routing; any non-walking travel mode.

## Motivation

- Strategy, verbatim: "V1 now ships a route preview only — polyline comparison of scenic vs. fast, then hand-off to native Maps/Waze for the actual walk (see V1 scope, added 2026-07-29)."
- Strategy, verbatim: "**Navigation — \"Scenic Walk\"** (walking only) and a **fastest-route mode**, user's choice."
- The place modal already routes you somewhere, but only the shortest way — the one thing every other map already does.
- `data-eng/scenic-walk-tiktok-feasibility.md` §1 recommends exactly this shape and rules out the weighted version for Phase 1.

## Requirements

### Must-have (P0)

1. **Two routes, one surface, walking only.**
   - [ ] The place detail modal offers **Fast route** and **Scenic route**; tapping either draws its polyline inside the modal's own space — no new screen, in-app depth stays at 2 (`design/ux-flows.md` §7).
   - [ ] Both requests are walking mode; no other mode is reachable.
   - [ ] When both exist, both polylines render at once and the selected one is visually dominant.
   - [ ] The two are told apart by weight or dash, not colour alone (`design/design-principles.md` §3).
   - [ ] A route polyline is distinguishable from a Hood's tourist-trap outline stroke at neighborhood zoom (`design/map-rendering-spec.md` §3) — the line channel now carries two unrelated meanings.

2. **Scenic is the same API plus waypoints — nothing custom.**
   - [ ] The scenic route is a platform walking-directions result through 1–2 waypoints. No routing engine, graph, or street-weight data ships.
   - [ ] A waypoint is only drawn from a Hood whose tourist-trap flag is explicitly `false`.
   - [ ] **A `null`-flagged Hood is never a waypoint.** Pass/fail: with every candidate Hood `null`, no scenic route is offered (req 4) — unrated Hoods are never presented as good.

3. **The detour is bounded, and its cost is shown before committing.**
   - [ ] Scenic is offered only if its duration is ≤ 1.5× the fast route **and** ≤ fast + 15 minutes. **[ASSUMPTION]** — proposed constants, not founder-set.
   - [ ] Each offered route shows its own duration and distance before Go.
   - [ ] A candidate over either bound is treated as no scenic route (req 4), never shown with a hidden cost.

4. **"No scenic route" is a stated state, not a silent one.**
   - [ ] When no waypoint qualifies, the detour exceeds req 3, or the API returns nothing, the Scenic control renders **disabled with a plain line** ("No scenic alternative for this walk") — not hidden, not a crash.
   - [ ] Reproducible: origin and destination inside the same Hood produces that disabled state.
   - [ ] If the scenic polyline comes back identical to the fast one, it is treated as no scenic route — never two identical lines under two names.

5. **Go hands off; Passenger never navigates.**
   - [ ] Go opens native Maps or Waze, destination pre-filled, walking mode. Strategy: "No in-app turn-by-turn, voice, or rerouting in V1."
   - [ ] If Scenic was selected and the target app cannot carry the waypoints, the modal says the external app receives the destination only, **before** leaving Passenger.
   - [ ] With no route app available, the action is disabled with a plain explanation (inherits `hood-place-detail` req 5).

6. **No origin means no preview, not a broken one.**
   - [ ] With location denied or unavailable, neither polyline is drawn and neither control claims a duration.
   - [ ] The route action still hands straight off to native Maps with the destination pre-filled — shipped behaviour, unchanged.

7. **Responsiveness.**
   - [ ] Tapping a route control gives visible feedback within 400ms (`design/design-principles.md` §2).
   - [ ] A polyline, or req 4's disabled state, resolves within 3s of the tap. **[ASSUMPTION]** — proposed, not founder-set.

8. **Build Phase 1 must be able to demonstrate this.**
   - [ ] The bundled Hood seed carries at least **three** non-adjacent Hoods flagged `false` along a documented demo corridor, so reqs 2–4 each have a positive and a negative case on device.
   - [ ] A test asserts that count against the shipped bundle, in the seed-authoring style T-031/T-032 already use.
   - [ ] Today's bundle ships 21 of 24 Hoods `null` and one `false`; as-is the scenic path is undemonstrable. Authoring, not a schema change.

### Nice-to-have (P1)

- Name the detour on the scenic control — "via Florentin" — so the bias is legible rather than mysterious.
- Remember the last route mode chosen and preselect it on the next place.

## Technical design

- **Data model:** no new table, column, or ingestion job. Reads `hoods.polygon` and the tourist-trap flag ([`hood-dataset`](../hood-dataset/hood-dataset.md) req 5) plus `places` coordinates ([`places-dataset`](../places-dataset/places-dataset.md) req 1) — both already delivered, so no supporting data PRD is owed. The heavier version's street graph and Attractiveness weight, which would have needed one, are out of scope.
- **Build-phase check:** Phase 1 reads the bundled `hoods-tel-aviv.json` / `places-tel-aviv.json` seeds, so nothing waits on Build Phase 2 **provided req 8's fixture is authored**. Real-data flag *quality* improves in Phase 2; the feature doesn't depend on it. Per L-024 the fixture is authored in `database/data/hoods-tel-aviv.source.json` and regenerated, never hand-edited in the bundle.
- **APIs / contract:** client-side only. No Passenger backend call, no new endpoint, no RLS surface.
- **Architecture notes:** the place detail modal (T-033) owns the controls; `SALVAGE.md` marks `Services/DirectionsService.swift` reusable. Proposed heuristic, **[ASSUMPTION]**: take Hoods intersecting a corridor around the straight A→B line, keep only those flagged `false`, rank by count of curated places inside, and use the Hood's nearest curated place as the waypoint — a centroid can land somewhere unwalkable.
- **Dependencies:** [`hood-place-detail`](../hood-place-detail/hood-place-detail.md) (accepted) — this extends its existing route action. Blocks nothing.
- **Open technical questions:** `MKDirections.Request` carries one source and one destination, so a waypointed route is likely 2–3 chained requests — confirm, and choose chaining vs. Google Directions (native waypoint support). Whether any hand-off can carry waypoints (req 5). Request volume and caching per modal open.

## Assumptions

- **[ASSUMPTION]** The waypoint heuristic is `product`'s proposal. Aviran specified the shape ("1–2 waypoints toward good Hoods"), not the algorithm.
- **[ASSUMPTION]** "Good Hood" reads as *tourist-trap flag explicitly `false`* — no other localness signal exists in V1 since decision #37 retired the graduated tag.
- **[ASSUMPTION]** The 1.5×/15-minute bounds and 3s budget are proposed. Wrong numbers make scenic either never offered or absurd; both retune cheaply.
- **[ASSUMPTION]** The place detail modal is the only entry point, per `design/ux-flows.md` §8a. Hood detail gets no route action.

## Open questions & risks

- **The strategy doc still describes the heavier version.** Its V1-scope navigation bullet still reads as weighted per-segment routing, with its own `[FLAGGED]` note. Decision #44 supersedes it, but the doc is Aviran-gated. **For Aviran:** replace that bullet with the #44 shape, or the source of truth contradicts what we build.
- **The scenic route may not survive the hand-off** (req 5) — the user could preview one walk and take another. Disclosure is specced; whether that's acceptable is Aviran's call.
- **Untested premise:** nobody has checked whether a waypointed route through an unflagged Hood actually *feels* scenic on real Tel Aviv streets (`PAS-7`, unresolved). Field-test before launch.
- The flag is sparse for real reasons — it's fed by the local-QA loop, whose proposing algorithm has no owner (`tourist-trap-flag` risks). If it stays sparse in production, req 4's disabled state becomes the common case.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-27 | Route preview only; hand off to native Maps/Waze; no in-app turn-by-turn in V1 | Decision #19, Aviran-direct |
| 2026-07-30 | Weighted per-segment routing (#32) found not buildable in the Phase 1 window | `PAS-7` feasibility — MapKit/Google walking APIs expose no custom per-street weighting |
| 2026-08-04 | Ship the lighter version: two comparison routes, biased via 1–2 waypoints. Heavier version declined | Decision #44, Aviran-direct, resolving `PAS-6` item 8 |
| 2026-08-04 | PRD written; waypoint heuristic, detour bounds, and entry point proposed as **[ASSUMPTION]** | Aviran specified the shape, not the algorithm |
