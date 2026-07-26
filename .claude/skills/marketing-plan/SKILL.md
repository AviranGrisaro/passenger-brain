---
name: marketing-plan
description: Write or update the per-phase marketing & acquisition plan for Passenger — positioning, channels, acquisition funnel, and GTM metrics for a single roadmap phase. Sibling track to that phase's feature PRDs, not folded into them.
disable-model-invocation: false
user-invocable: true
---

# /marketing-plan — Per-Phase Marketing & Acquisition Doc

One phase, one small GTM doc. Parallel to the feature PRDs, not nested inside them — see `CLAUDE.md` "Doc hierarchy."

## Before writing

1. **Check it doesn't already exist** — `marketing/<phase-slug>/marketing-acquisition-plan.md`. Update in place if found.
2. **Pull this phase's context from the master strategy** (`strategy/passenger-strategy.md`'s "Strategic phasing" table and "Notes on specific phases") as the starting point, then expand it here. (The per-phase `phase-strategy.md` layer is retired — see `CLAUDE.md`'s Doc hierarchy — don't look for one.)
3. **Pull positioning from the master strategy** (`strategy/passenger-strategy.md`, "Positioning and differentiation") — don't re-derive positioning per phase, apply it.

## Doc structure

```markdown
# Phase <N> Marketing & Acquisition — <phase name>

**Status:** <Draft / Active / Complete>
**Phase:** [<phase name>](../../strategy/passenger-strategy.md#strategic-phasing)

## Audience for this phase
<Who specifically, for this phase (e.g., "tourists visiting Tel Aviv," not "travelers" broadly). Narrower than the master strategy's general positioning.>

## Positioning
<Applies the master strategy's positioning to this phase's audience/channels. Link back rather than re-deriving "not a guide, not a social feed" from scratch.>

## Channels & tactics
<Bulleted list. Each channel: what it is, why it fits this audience/phase, and what "trying it" costs (time/money). Don't list channels with no plan to execute them — that's a wishlist, not a plan.>

## Acquisition funnel
<Awareness → install → activation → (paid unlock, for Phase 1) → retention. What's the plan at each step, and what's the expected drop-off if known. Mark anything unmeasured as **[ASSUMPTION]**.>

## Budget / resourcing
<What this actually costs — time, money, or both. "Free" is a valid answer if that's the real plan, but say so explicitly rather than leaving it blank.>

## Metrics
<How you'll know the GTM motion is working for this phase. Should connect to the phase's exit gate in the master strategy's "Success criteria" section — e.g., if the gate is "paywall conversion ≥8%," this section covers how you'll get enough installs to measure that.>

## Open questions and risks
<Label assumptions inline with **[ASSUMPTION]**.>
```

## Output

- Save as `marketing/<phase-slug>/marketing-acquisition-plan.md` + render the HTML twin: `python3 scripts/md-to-html.py marketing/<phase-slug>/marketing-acquisition-plan.md`.
- Add a row to `INDEX.md`'s "Where to find specific things" table if this is the first marketing doc.
- Commit + push the `.md` in the same turn (standing repo rule — see `CLAUDE.md` "Doc output rule"). The `.html` is gitignored, local-only.

## Quality check before saving

- [ ] Doesn't restate positioning already settled in the master strategy — links instead.
- [ ] Every channel listed has an actual plan to execute it, not just a name.
- [ ] Metrics tie back to this phase's exit gate, not a generic vanity metric.
- [ ] Under ~1 page.
