# PRDs

One folder per feature, flat — `prds/<feature-slug>/<feature-slug>.md`. Phase goes on the PRD's `**Phase:**` header line, never in the path. Add a row here whenever you add a PRD.

**Before writing one:** it must quote the line in `../strategy/passenger-strategy.md` that authorizes the feature. A PRD that can't cite one doesn't leave `spec`. See the scope gate in `../CLAUDE.md`.

| Feature | Phase | Status | PRD |
|---|---|---|---|
| _empty_ | — | — | Awaiting the first `product` pass over the strategy doc |

## Expected V1 shape

Roughly six PRDs cover Phase 1, per the strategy's V1 scope — not twenty-seven. As a sanity check on the first pass:

- The map itself: cold open, two orthogonal layers (heat, tag), Tel Aviv only
- Time slider: now → +12h, hour snapping
- Zone and spot detail: neighborhood blurb, tagged spots, three vibe tags (Local · Mix · Tourist), two categories, hand-off to native Maps/Waze
- Saved and Visited places — Visited populates automatically from geofence detection, no manual mark action
- Search: icon in the map chrome opening a sheet; place names, keywords, and neighborhoods, with results carrying heat + tag and honoring the slider hour (decision #23). The keyword half needs a field the places pipeline doesn't have yet — coordinate with the pipeline PRD rather than assuming it exists.
- Places + localness pipeline: sourcing, the algorithm, and the in-app local-QA loop that corrects it

**Not V1, do not write PRDs for these** (moved to Phase 2 on 2026-07-27, decisions #19 and #20): **Scenic View** — V1 hands off to native Maps/Waze instead of routing in-app — and the **Live Events overlay**. Both are subscription-gated when they ship. The Locali client had an events overlay shipping unflagged, so a salvage-driven PRD is the likely way this comes back in by accident.

Cross-feature UX reference for all of the above: `../design/ux-flows.md` (reading view: `../design/ux-flows.html`).
