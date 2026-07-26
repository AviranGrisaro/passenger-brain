---
name: phase-strategy
description: "RETIRED 2026-07-11 — do not invoke. The per-phase strategy doc layer was archived and consolidated into 06-execution/TASKS.md, which was itself superseded by Linear on 2026-07-12. See CLAUDE.md's Doc hierarchy section. Kept on disk for historical reference only."
disable-model-invocation: true
user-invocable: false
---

# /phase-strategy — RETIRED 2026-07-11, DO NOT USE

**This skill is dead. Do not write a new `04-strategy/phases/<phase-slug>/phase-strategy.md`.** Aviran archived all five per-phase docs on 2026-07-11 (`99-archive/2026-07-11-phase-strategy-docs/`), consolidating them into `06-execution/TASKS.md`; `TASKS.md` was itself superseded by Linear the next day (2026-07-12). Feature PRDs now link straight from the master strategy's phasing table to the PRD (see `CLAUDE.md`'s Doc hierarchy, entry dated 2026-07-22). If you were routed here by a stale reference in another file (a skill, an agent, `CLAUDE.md` itself), fix that reference instead of running this skill — see the 2026-07-22 PROGRESS.md worklog entries for the full incident and what was already fixed.

The content below is kept only so the doc structure it used to produce is visible for historical/archival purposes. **Everything past this point is inert.**

# /phase-strategy — Per-Phase Strategy Doc (historical, inert)

One phase, one small doc. This sits between the master strategy (`04-strategy/locali-strategy.md`) and the feature PRDs (`03-prds/<phase-slug>/`) in the Locali doc hierarchy — see `CLAUDE.md` "Doc hierarchy" for the full ladder.

## Before writing

1. **Check it doesn't already exist** — look in `04-strategy/phases/<phase-slug>/phase-strategy.md`. If found, update it, don't duplicate.
2. **Read the master strategy's phasing table** (`04-strategy/locali-strategy.md`, "Strategic phasing" section) — pull this phase's strategic question and its gate from there. Don't restate the reasoning for why the phase exists in this order; link to it instead.
3. **Check what already exists for this phase** — feature PRDs in `03-prds/<phase-slug>/`, marketing plan in `17-marketing-acquisition/<phase-slug>/`. Link out to real docs; don't invent features or channels that haven't been discussed.

## Doc structure

```markdown
# Phase <N> Strategy — <phase name>

**Status:** <Draft / Active / Complete>
**Strategic question:** <pulled verbatim from locali-strategy.md's phasing table>
**Gate to enter this phase:** <what had to be true from the prior phase — link to that gate>
**Gate to exit this phase:** <the measurable condition that greenlights the next phase>

## What has to be true

Not a restatement of the master strategy — the concrete, phase-specific plan across three tracks:

### Features
<Bulleted list of the features this phase needs, each linking to its PRD once one exists: `[feature-name](../../../03-prds/<phase-slug>/<feature-name>/PRD.md)`. If a PRD doesn't exist yet, say so plainly — don't fake a link.>

### Marketing & acquisition
<What has to be true on the GTM side this phase — link to `17-marketing-acquisition/<phase-slug>/marketing-acquisition-plan.md` once it exists, otherwise summarize in 2-3 bullets and flag that the full plan is pending `/marketing-plan`.>

### Dev architecture
<What has to be built or decided at the infra/architecture level to support this phase's features — cite the master strategy's "Technical architecture strategy" section for anything already decided; only add what's specific to this phase.>

## Success criteria for this phase

<The measurable bar, from the master strategy's "Success criteria" section if one exists there — don't invent a new number.>

## Risks specific to this phase

<Only risks that are phase-specific. Cross-phase risks belong in the master strategy's "Key risks" section — link there instead of repeating.>
```

## Output

- Save as `04-strategy/phases/<phase-slug>/phase-strategy.md` + render the HTML twin with `python3 scripts/md-to-html.py 04-strategy/phases/<phase-slug>/phase-strategy.md`.
- Add a row to `INDEX.md`'s "Where to find specific things" table if this is the first phase doc.
- Commit + push the `.md` in the same turn (standing repo rule — see `CLAUDE.md` "Doc output rule"). The `.html` is gitignored, local-only.

## Quality check before saving

- [ ] Every claim traces to the master strategy or is explicitly marked **[ASSUMPTION]** — no invented numbers or features.
- [ ] Feature/marketing links point to real files, or are explicitly flagged as "not yet written."
- [ ] Doesn't repeat the master strategy's phasing rationale — links instead.
- [ ] Under ~1 page. If it's growing past that, something belongs in a feature PRD or the marketing plan instead.
