---
name: user-research-synthesis
description: Aggregate UXR findings across sources into actionable insights. Synthesizes research from HeyMarvin, local markdown, and meeting notes.
disable-model-invocation: false
user-invocable: true
---

<!-- filename-convention-block -->
## Filename Convention

**Save the output as `[feature-name-kebab]_[doc-type].md`** inside the project folder (`Projects/<feature-slug>/` or `content/<numbered>/<feature-slug>/`).

- **Never use generic names** like `prd.md`, `design-ticket.md`, `README.md`, `direction.md`, `dev-story.md`, `notes.md`. Always prefix with the feature/initiative name so the filename is self-describing out of context.
- **No date prefix.** Use git/mtime for chronology.
- **Approved doc-types** (extend as needed): `prd`, `prd-draft`, `prd-team-kickoff`, `prd-planning-review`, `prd-xfn-kickoff`, `prd-solution-review`, `prd-launch-readiness`, `design-ticket`, `dev-story`, `kickoff-agenda`, `project-notes`, `decision`, `experiment`, `launch-checklist`, `meeting-notes`, `release-notes`, `competitor-analysis`, `retention-analysis`, `status-update`, `roadmap`, `uxr-synthesis`, `impact-sizing`, `strategy-direction`, `risks-and-decisions`, `eng-validation`, `readme`.

**Examples:** `visible-consistency_prd-draft.md`, `device-lock_kickoff-agenda.md`, `consistency-leaderboard_design-brief.md`, `external-activities-home_design-ticket.md`.

---


# User Research Synthesis

## Quick Start

```
/user-research-synthesis
```

Then provide:
1. **Research topic or feature area** (e.g., "onboarding", "workout completion", "social features")
2. **Sources to check** (optional — defaults to all available)

I'll gather findings from all available research sources, identify patterns, and produce an actionable synthesis.

**Output:** Saved to `content/10-outputs/uxr-synthesis/[topic]-[date].md`
**Time:** ~10-15 min

**When to use:** Before writing a PRD, during discovery, or when you need a research-backed perspective on a feature area.

## Context Routing Logic (Internal - for Claude)

### Step 1: Gather Research Sources
Search for relevant research across:
- `content/01-discovery/` — user context, preferences
- `content/prds/*/` — PRDs that reference research findings
- `content/11-competitors/` — competitor UX analysis
- `content/10-outputs/` — previous analyses
- Google Drive (if accessible via MCP) — UXR reports, interview transcripts
- HeyMarvin (if accessible via MCP) — tagged findings
- Meeting notes — insights from customer calls, design reviews

### Step 2: Extract Findings
For each source, extract:
- **Finding**: What was observed or learned
- **Evidence**: Quote, data point, or reference
- **Confidence**: High (multiple sources), Medium (single strong source), Low (anecdotal)
- **Relevance**: How directly this relates to the topic

### Step 3: Pattern Identification
Group findings into themes:
- What do users consistently say/do?
- Where are the contradictions?
- What's the strongest signal vs. noise?
- What gaps exist in our understanding?

### Step 4: Synthesize & Recommend

## Output Format

```markdown
# UXR Synthesis: [Topic]
_Generated [date] | Sources: [count]_

## Executive Summary
[2-3 sentences — the key takeaway]

## Key Findings

### Theme 1: [Name]
**Confidence: High/Medium/Low**
- Finding: [what we learned]
- Evidence: [supporting data/quotes]
- Implication: [what this means for the product]

### Theme 2: [Name]
...

## Contradictions & Nuances
- [Where findings conflict and how to interpret]

## Research Gaps
- [What we don't know yet and how to find out]

## Recommendations
1. [Action] — Supported by: [findings]
2. [Action] — Supported by: [findings]

## Appendix: Sources
| Source | Type | Date | Key Insight |
|--------|------|------|-------------|
```

## Tone
Be evidence-driven. Always cite sources. Distinguish between strong signals (multiple corroborating sources) and weak signals (single anecdote). Flag when sample size is too small to draw conclusions.
