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
- Zone and spot detail: neighborhood blurb, tagged spots, five vibe tags, two categories
- Scenic View: in-app routing that favors interesting streets over the fastest path
- Saved and Visited places
- Places + localness pipeline: sourcing, the algorithm, and the in-app local-QA loop that corrects it

Events are a live overlay on the time slider, not a third category — fold them into the map PRD unless they earn their own.
