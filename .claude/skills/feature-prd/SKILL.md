---
name: feature-prd
description: Write or update a small, single-feature PRD for Passenger — product spec plus a Technical Design section, in its own folder under prds/. Use instead of the legacy /prd-draft and /prd skills, which carry Ares Fitness-specific rules.
disable-model-invocation: false
user-invocable: true
---

# /feature-prd — Single-Feature PRD (Passenger)

One feature, one small doc, including the technical design. This is the leaf of the Passenger doc hierarchy — see `CLAUDE.md` "Doc hierarchy": Investor deck → Strategy → **Feature PRD** (the middle "Phase strategy" rung was retired 2026-07-11 — PRDs link straight up to the master strategy's phasing table now).

**Why this skill exists instead of `/prd-draft` or `/prd`:** those two were inherited from a different project (Ares Fitness / "amp") and carry that product's rules — banned sections tuned to a team with a dedicated analytics pipeline, an "iOS only, never mention Android" rule for reasons specific to that product, file paths under a different user's home directory, and scripts that don't exist in this repo. Passenger is a four-founder project with its own conventions; use this skill for Passenger feature PRDs instead.

## Before writing

1. **Check it doesn't already exist** — look in `prds/<feature-slug>/<feature-slug>.md` and `prds/INDEX.md`. Update in place if found.
2. **Confirm the phase** this feature belongs to against `strategy/passenger-strategy.md`'s "Strategic phasing" table — the feature should trace to something that phase's row names. (The per-phase `phase-strategy.md` layer is retired — see `CLAUDE.md`'s Doc hierarchy — don't look for one.) If it doesn't trace to anything there, flag that explicitly rather than silently inventing a justification.
3. **Pull constraints from the master strategy** (`strategy/passenger-strategy.md`) — tech stack (native iOS/SwiftUI, Firebase/Firestore, MapKit/Google Maps, RevenueCat), platform (iOS only), pricing model — don't re-decide these per feature, just apply them.

## Folder convention

**Flattened 2026-07-25 (Aviran-direct, second restructure pass).** One folder per feature, directly under `prds/` — no phase-slug level. Everything for a feature lives together: `prds/<feature-slug>/<feature-slug>.md` (the PRD, named after its own folder) plus `TRD.md`, `TEST-PLAN.md`, `review-synthesis.md`, and any dated variants (`TRD-<variant>.md`, `TEST-PLAN-<variant>.md`) alongside it. Phase is metadata on the PRD's own `**Phase:**` header line, not a directory. Two cross-feature docs sit at the top level as siblings, not inside any feature folder: `prds/decisions.md` and `prds/INDEX.md`.

## Doc structure

**Restructured 2026-07-25 (Aviran-direct).** Every PRD in this repo follows this exact 7-section shape, in this order. See `archive/2026-07-25-prd-restructure/README.md` for the full ruling set behind the shape if you need the reasoning; this section is the operative spec going forward.

**Word budget (second restructure pass, 2026-07-25):** ~800 words per PRD; ~1,200 for the genuinely dense ones (irreducible decisions/thresholds, not verbosity — don't self-grant this, it's for docs like `visited-places` or `tel-aviv-heatmap` that carry real settled-decision weight). Word count is the metric that matters, not line count — a doc can hit a line budget while still burying 25-word facts inside 100-word paragraphs. **One fact per bullet, max ~25 words** does most of the compression work: if a bullet needs a sub-clause to hold a constraint, that constraint is a Requirement, not a modifier — move it to Requirements as its own numbered item. **Motivation caps at 4 bullets / ~100 words** — it answers only "what's broken today" and "why it matters now"; link up to the strategy doc for the rest, don't restate it. Never cut a falsifiable threshold, kill criterion, `Not in scope:` line, Decisions-log row, or `[ASSUMPTION]` label to hit a budget — compress the prose around them, not the facts themselves. Test for any cut: would a developer or `qa` make a different decision without this sentence? If no, delete it; if yes, it's a Requirement, not prose.

```markdown
# <Feature Name> — PRD

**Status:** <Draft / In Review / Approved / Shipped>
**Phase:** [<phase name>](../../strategy/passenger-strategy.md#strategic-phasing)
**Owner:** Aviran Grisaro
**Last updated:** <date>
<any phase-placement ruling / priority / naming decision as one more metadata line here — don't give these their own section>

## Description
<Bullets: what this feature is.>
- Last bullet is always: `**Not in scope:** X, Y, Z.` — this is where non-goals live now (demoted from their own section, but never dropped — a reader must still be able to tell what's fenced off).

## Motivation
<Bullets: why we need it. Link UP to the master strategy's phasing table (`strategy/passenger-strategy.md#strategic-phasing`) for the strategic "why" — don't restate it here.>

## Requirements

### Must-have (P0)
<Numbered list. Each item gets acceptance criteria as a checklist. This is where falsifiable thresholds, kill criteria, and acceptance bars live — see "No Success Metrics section" below.>

### Nice-to-have (P1)
<Bulleted. Things that ship only if time allows.>

## Technical design
- **Data model:** <new/changed Supabase tables, columns, RLS, relationships>
- **APIs / client-server contract:** <what the client reads/writes, Realtime behavior if relevant>
- **Architecture notes:** <anything non-obvious about how this fits the existing native iOS/Supabase/MapKit stack — cite the master strategy for anything already decided, only add what's new>
- **Dependencies:** <other features/infra this needs first, or blocks>
- **Open technical questions:** <things the developer still needs to decide>

## Assumptions
<Load-bearing assumptions only — CLAUDE.md's non-negotiable rule. Omit this section entirely if there are none. Keep inline **[ASSUMPTION]** labels wherever they appear in the doc too.>

## Open questions & risks
<Anything unresolved, escalations for Aviran, risks. Label assumptions inline with **[ASSUMPTION]**.>

## Decisions log
| Date | Decision / change | Why |
|---|---|---|
<Every dated decision or change, oldest or newest first — match whatever order the doc already used before restructure, just be consistent. This replaces both "Recent changes"/"Changelog" AND is where you log any review-panel event (see prd-review-panel skill's Step 5.5) or founder-direct amendment. Add a `Why` for every row when recoverable; use `—` only when it's genuinely not.>
```

**What's gone and why (don't reintroduce these as sections):**
- **KPIs** — deleted outright, no analytics pipeline exists yet.
- **Success Metrics** — deleted as a section, but not as content. A vanity metric ("users engage more") gets dropped. A falsifiable threshold, kill criterion, or acceptance bar (e.g. "Spearman ρ ≥ 0.7", "cold launch ≤3s", "zero tourist-trap inversions") is a Requirement, not a metric — it MOVES into Requirements as a numbered P0 with a checklist, never deleted.
- **Problem / Goals** — replaced by Description / Motivation, same content, less ceremony.
- **User stories** — killed. Requirements are the contract `qa` tests against and `product`'s acceptance gate rejects on; user stories were redundant with that.
- **Non-goals** as its own section — demoted to the `**Not in scope:**` bullet at the end of Description. Content survives, heading doesn't.
- **Review Panel Verdict / Per-reviewer verdicts / Severity totals / Prior reviews** — never lived in the PRD body under the new shape; that's the sibling `review-synthesis.md`'s job (see `prd-review-panel` skill). At most the PRD gets a one-line pointer in `Open questions & risks`.

## Updating an existing PRD (shipped/built components, or any amendment)

When you're **updating** an existing PRD — not drafting a new one — a component that changed in `passenger-code` **must** be reflected here in the same turn as the code change (standing policy, Aviran-direct 2026-07-18, unchanged by the 2026-07-25 restructure):

1. **Rewrite the specific stale component description in place** — the Requirement / Technical Design / wherever the component is described must state what it *now actually does*, not what it originally specced. Surgical: fix the wrong lines; don't just append a contradicting new paragraph and leave the old one to compete.
2. **Append a row to the bottom `Decisions log` table** — `| <date> | <what changed, one line> | <why> |`. This replaced the old top-of-doc `## Recent changes` section (retired 2026-07-25) — **do not** recreate a `## Recent changes` section; the Decisions log at the bottom is the single place a change gets logged now.
3. Bump **Last updated**, re-render the `.html` twin, and update the `prds/INDEX.md` Notes cell if its status/summary text is now misleading.

The failure this guards against: a shipped-component description left stale, so a reader learns the current behaviour only from the code because the PRD still describes the old one.

## Output

- Save as `prds/<feature-slug>/<feature-slug>.md` + render the HTML twin: `python3 scripts/md-to-html.py prds/<feature-slug>/<feature-slug>.md`.
- Add a row to `prds/INDEX.md`.
- Commit + push the `.md` in the same turn (standing repo rule — see `CLAUDE.md` "Doc output rule"). The `.html` is gitignored, local-only.
- If the feature is significant enough to warrant multi-perspective review, follow with `/prd-review-panel`.

## Quality check before saving

- [ ] Technical Design section is filled in, not a placeholder — a developer could start from it.
- [ ] Traces to a named item in the master strategy's phasing table, or explicitly flags that it doesn't.
- [ ] No invented tech-stack choices that contradict the master strategy (native iOS, Supabase, MapKit, RevenueCat).
- [ ] ~800 words — the ~1,200-word exemption is reserved for PRDs with genuinely irreducible decision/threshold content (see `archive/2026-07-25-prd-restructure/README.md`); don't self-grant it. Word count, not line count — a doc can look short and still be full of 100-word paragraphs. If it's ballooning past the exemption too, it's probably two features.
- [ ] One fact per bullet (~25 words max); Motivation is ≤4 bullets / ~100 words and links up to strategy instead of restating it.
- [ ] No `## Recent changes`, `## Problem`, `## Goals`, `## User stories`, `## Success metrics`, `## Non-goals`, or `## Review Panel Verdict` section reintroduced — see "What's gone and why" above.
- [ ] Every falsifiable threshold/acceptance bar is a numbered Requirement with a checklist, not buried in prose.
- [ ] Non-goals content is present as the `**Not in scope:**` bullet at the end of Description, not silently dropped.
