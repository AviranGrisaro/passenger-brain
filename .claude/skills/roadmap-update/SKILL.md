---
name: roadmap-update
description: Update the product roadmap based on completed work, new priorities, and strategic shifts.
disable-model-invocation: false
user-invocable: true
---

# Roadmap Update

## Quick Start

```
/roadmap-update
```

I'll review the current state of all projects, Jira tickets, and strategic priorities, then produce an updated roadmap view.

**Output:** Updated `content/strategy/roadmap.md` + summary of changes
**Time:** ~10 min

**When to use:** Weekly/biweekly, after major milestone completions, or when priorities shift.

## Process

### Step 1: Current State Assessment
Read and analyze:
- `content/strategy/roadmap.md` — current roadmap
- `content/strategy/` — strategic docs, OKRs
- `prds/<feature-slug>/<feature-slug>.md` — all active PRDs and their stages
- `content/06-execution/tasks/TASKS.md` — active task list
- Jira MCP — current sprint status, epic progress
- `content/07-analytics/metrics.json` — latest metrics (if available)

### Step 2: Progress Check
For each roadmap item:
- What's the current stage? (Discovery / Spec / Design / Dev / QA / Shipped)
- Has the timeline shifted? (On track / Delayed / Ahead)
- Are there new blockers?
- Has scope changed?

### Step 3: Priority Reassessment
Based on:
- Metric movements (what's working, what's not)
- Stakeholder feedback or requests
- Competitive moves
- Resource availability changes
- New information or research findings

### Step 4: Update & Communicate

## Output Format

```markdown
# Product Roadmap — Updated [Date]

## This Sprint (Sprint [N])
| Initiative | Stage | Owner | Status | Notes |
|-----------|-------|-------|--------|-------|

## Next Sprint
| Initiative | Stage | Owner | Priority | Depends On |
|-----------|-------|-------|----------|-----------|

## This Quarter (Q[N])
| Initiative | Target Sprint | Stage | Confidence |
|-----------|--------------|-------|------------|

## Next Quarter
| Initiative | Why | Priority |
|-----------|-----|----------|

## Recently Completed
| Initiative | Shipped | Key Metric Impact |
|-----------|---------|------------------|

## Changes Since Last Update
- **Added**: [new items and why]
- **Reprioritized**: [what moved up/down and why]
- **Removed/Deferred**: [what was cut and why]
- **Scope Changed**: [what was adjusted]

## Open Questions
- [Decision needed that affects roadmap]
```

## Tone
Be honest about status. If something is delayed, say so and explain why. Roadmaps are communication tools — clarity builds trust with stakeholders.
