# Feasibility note — Scenic Walk / fastest-route mode

**Owner:** data-engineer
**Date:** 2026-07-30
**Status:** Scoping complete. PRD-writing still held on Aviran, not on this note — see Recommendation.
**Authorizing line:** `strategy/passenger-strategy.md` V1 scope — `"Navigation — 'Scenic Walk' (walking only) and a fastest-route mode... Each street segment carries an Attractiveness weight; Scenic Walk routes A→B maximizing high-weight streets passed"` (decision #32).
**Source:** This note ports the findings of `passenger-brain/data-eng/scenic-walk-tiktok-feasibility.md` §1 (Linear `PAS-7`, closed 2026-07-30) into the PRD-gate location `product` reads before writing PRDs. It is not new research — read the source doc for full derivation; this is the feature-scoped summary plus the go/no-go/slip call.

## What decision #32 actually asks for vs. what's already locked

Two different things share the name "Scenic Walk":

1. **Already locked (decision #19, 2026-07-27):** a route-preview only — draw a scenic route and a fast route as two comparison polylines, hand off to native Maps/Waze for the actual walk. No custom routing engine.
2. **Decision #32 (2026-07-29, applied 2026-07-30):** a real weighted-routing problem — every street segment carries an Attractiveness weight, and Scenic Walk maximizes high-weight streets passed A→B. Categorically heavier than #1.

## Recommended approach for V1

Ship version 1 (the already-locked comparison-polyline preview), with "scenic" approximated by routing through 1–2 via-waypoints picked from nearby tagged/local Hoods, using Apple's/Google's own walking-directions APIs. Not version 2.

Reasoning: version 2 requires a genuine Attractiveness *signal*, and neither available source is good enough for V1:
- **Derived from places data** (heat + tourist-trap flag, spatially joined to street segments) is cheap once the places/Hoods schema exists, but it's a proxy for "near good places," not "pleasant to walk down" — it doesn't know greenery, shade, sidewalk width, or noise, which is what "Attractiveness" means as a walking-route concept.
- **A real street-level scoring pass** (hand-curated, or OSM tags like `leisure=park`/`natural=tree`, or computer-vision over street imagery) is either a return to the staffing model decision #22 explicitly moved away from, or a genuine research project — not a Phase 1 task.

The routing algorithm itself (reweight each edge as `cost = distance − λ·attractiveness`, run Dijkstra/A*) is a solved problem and not the blocker. The blocker is the missing input, plus the fact that Apple/Google's own walking-directions APIs don't expose custom per-street weighting — a real version-2 build means self-hosting a routing engine (GraphHopper/Valhalla/OSRM) on an OSM extract, not calling MapKit/Google Directions.

## Effort estimate

- **Version 1 (recommended for V1):** not separately estimated in hours — it reuses the native-hand-off pattern V1 already assumes and needs no new backend infra, only a via-waypoint heuristic and two-polyline UI. Meaningfully smaller than version 2; no numeric estimate is sourced, so none is given here rather than inventing one.
- **Version 2 (weighted routing, not recommended for V1):** ~3–5 weeks of dedicated data/backend effort — self-hosted routing engine setup, an attractiveness-proxy pipeline sequenced *after* the places/Hoods schema (which doesn't exist yet — schema is empty, starts at migration `001`), and field-tuning so "scenic" feels distinct from "fastest," before any iOS integration on top.

## Key risks / unknowns

- Version 2's attractiveness signal is a real gap, not an engineering-hours problem — even the cheap option (Option A above) only ships after Epic C's places table lands, which isn't sequenced yet.
- Version 1's via-waypoint heuristic is untested against real Tel Aviv streets — "does it actually feel different from fastest" needs field-testing once built, same caveat PAS-7 raised for version 2.
- Decision #32's literal text describes version 2. Shipping version 1 for V1 launch is a scope reduction from what's currently written in the strategy doc and needs Aviran's explicit sign-off, not an assumption `product` or `data-engineer` can make unilaterally.

## Recommendation: SLIP the heavier version, GO on the lighter version — pending Aviran's scope call

**Not buildable in the Phase 1 window as genuinely weighted routing** (version 2). **Buildable now** as the already-locked comparison-polyline preview (version 1), which is what V1 should ship. Treat version 2 as a fast-follow once the places/heat schema and a real attractiveness signal both exist.

This is a recommendation, not a resolution — Linear `PAS-6` item 8 ("ship the lighter locked version now, or slip V1 for weighted routing?") is still open and is Aviran's call, not data-engineer's or product's. `product` should not write a PRD assuming either answer until that lands; this note gives the technical basis for that decision, it doesn't make it.

---

## Data/schema needs — addendum by `product`, 2026-07-30

Added under the standing data/schema rule (founder-direct 2026-07-30, `agent-os/PROGRESS.md`). **This is not a PRD and does not resolve `PAS-6` item 8** — it records what each version would need from the data layer, so whoever writes the PRD after Aviran's call doesn't re-derive it. `data-engineer`'s text above is unchanged.

**Version 1 (comparison polylines + via-waypoint heuristic) — the existing schema covers it. No supporting PRD needed.**

- "Nearby tagged/local Hoods" resolves to fields already spec'd: `hoods.polygon` (for a centroid to route via) and `hoods.is_tourist_trap` — both [`prds/hood-dataset/`](../hood-dataset/hood-dataset.md) req 5. Candidate waypoints inside a Hood come from `places` coordinates ([`prds/places-dataset/`](../places-dataset/places-dataset.md) req 1).
- One caveat worth writing into the eventual PRD rather than discovering at QA: `is_tourist_trap` is **nullable**, and a Hood that has never been rated ships `null`. A "route via non-touristy Hoods" heuristic that treats `null` as `false` will happily route through unrated Hoods and call them local. That is a pass/fail criterion the PRD owes, not an implementation detail.
- Nothing here is a new table, a new field, or a sourcing job. It is a read over data two other PRDs already deliver.

**Version 2 (weighted routing) — needs a supporting PRD of its own, and it is exactly the founder's own example.**

- A **street graph** (segments with geometry and topology) and a per-segment **Attractiveness weight** are two datasets that do not exist in any form, in any PRD, in any migration. The standing rule's own illustration is *"if Scenic Walk needs a street-graph + attractiveness signal."*
- Per §"Recommended approach" above, the weight has no adequate source: the cheap proxy is not what "attractiveness" means as a walking concept, and the real version is hand-curation (the staffing model decision #22 exited) or a research project.
- If Aviran chooses version 2, that data need is its own deliverable and gets its own PRD **before** any routing PRD — the routing algorithm is solved, the input is what is missing.
