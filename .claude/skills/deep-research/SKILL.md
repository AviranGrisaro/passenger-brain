---
name: deep-research
description: Multi-phase deep research with memory-first retrieval, then web + Slack + Gmail + Atlassian + content/ scans, ending in evidence-graded synthesis. Use when a question needs sourcing across multiple internal and external systems. Triggers - "research X", "what do we know about Y", "find everything about Z", "give me a brief on", "pre-meeting research", "deep dive on", "/deep-research".
---

# Deep Research

Multi-phase research campaign that pulls findings from memory, then external sources, then synthesizes.

## When to use

You have a real question that needs sourcing across multiple systems before you can answer it. Examples:

- "What did engineering decide about firmware-side dynamic QR rendering?"
- "What's the full picture on Hyrox as a competitor?"
- "Has anyone discussed periodical training adherence drop-off?"
- "Why did we deprecate the old auth middleware — what was the legal context?"

If the answer is a single grep or single MCP call, just do it. This skill is for questions that need cross-referencing.

If you have a **seed entity** (not a question) and want to expand outward, use `dossier-collect` instead.

## Steps

### 1. Define research scope
Break the question into **3–7 sub-questions**. State them at the top of your response. For each, mark which sources are most relevant.

### 2. Estimate depth
- **Quick** (2–3 min): memory + 1–2 web queries
- **Standard** (5–10 min): memory + web + content/ scan
- **Deep** (15–30 min): all sources + cross-reference + persist
- **Exhaustive** (30 min+): deep + spawn `deep-researcher` agent for parallel sub-questions

### 3. Memory-first retrieval (cheap, always first)

Run in **parallel**:
- `mcp__gbrain__search` and `mcp__gbrain__recall`
- `mcp__plugin_claude-mem_mcp-search__smart_search`
- `Grep` over `content/prds/`, `content/strategy/`, `content/08-feedback/`, `content/10-outputs/decisions/`, `content/11-competitors/`
- Read relevant auto-memory entries from `/Users/avirang/.claude/projects/-Users-avirang-Documents-amp/memory/`

If memory answers the question completely, stop and synthesize. Don't burn API time on the web.

### 4. Active research (only if memory came up short)

Per sub-question type:

| Sub-question | Source(s) |
|---|---|
| "What did people say internally?" | Slack search (channels + public + threads), Gmail search |
| "What's in flight?" | Jira JQL, Confluence CQL, Monday boards |
| "What's the customer signal?" | Common Room (account + contact research skills) |
| "What's public/competitive?" | WebSearch, WebFetch on competitor URLs |
| "What does the data say?" | Invoke `/analytics` or `/quick-analysis` skill |
| "What's the codebase view?" | Grep over product-os-server/, GitHub MCP |

Batch parallel queries. Don't serialize what can run in parallel.

### 5. Cross-reference
Compare findings. Newer supersedes older. Disagreement = signal. Note contradictions explicitly.

### 6. Evidence-grade every finding
- **High** — multiple independent sources agree, directly observed, recent
- **Medium** — single credible source, indirectly supported
- **Low** — anecdotal, single unverified, speculative

### 7. Synthesize

```markdown
# [Question] — Research Report
**Date:** YYYY-MM-DD
**Depth:** quick | standard | deep | exhaustive

## Summary
[2–3 sentence direct answer]

## Sub-questions
1. [Q1] → [A1, evidence: H/M/L]
2. [Q2] → [A2, evidence: H/M/L]
...

## Key findings
1. [Finding] — Evidence: H/M/L — [source citations with dates]
2. ...

## Contradictions
- [Claim A] vs [Claim B]: [resolution or "unresolved"]

## Open questions
- [What this research couldn't answer]

## Recommended next steps
- [Concrete actions]

## Sources scanned
- gbrain: N hits
- Slack: [channels searched]
- Gmail: [query]
- Atlassian: [JQL / CQL used]
- content/: [paths grepped]
- Web: [queries + URLs]

## Sources NOT scanned (gaps)
- [What was deliberately skipped or unreachable]
```

### 8. Persist

- Write report to `content/08-feedback/research/YYYY-MM-DD-<slug>.md`
- If the question was competitor-focused: also save under `content/11-competitors/<competitor>/research-<date>.md`
- If a non-obvious durable fact emerged: save to auto-memory (`reference` or `project` type)
- Update `content/08-feedback/research/INDEX.md` with one line

## Principles

- Memory first, web last
- Always cite sources with dates
- Always state what you DIDN'T check
- Stop when the answer is clear — depth-match the question stakes
- Contradiction is signal, not noise

## Output discipline

Always include:
- Date stamp
- Source citations per claim
- Confidence (H/M/L)
- Explicit gaps (what wasn't checked)
