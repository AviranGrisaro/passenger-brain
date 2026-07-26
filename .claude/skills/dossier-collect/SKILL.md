---
name: dossier-collect
description: Build a graph-structured dossier on a seed entity via parallel fan-out + recursive expansion across Slack, Gmail, Atlassian, Notion, Common Room, gbrain, web, and content/. Each claim carries source provenance. Use for stakeholder briefings, account dossiers, competitor deep-dives, feature archaeology. Triggers - "dossier on", "build a dossier", "deep dive on this person", "everything about Y", "pre-meeting brief on", "/dossier-collect".
---

# Dossier Collect

Recursive parallel investigation that builds a graph dossier on a **seed entity** (not a question).

## When to use

You have a **seed** — a person, company, feature, ticket id, or concept — and want to expand outward, discovering connected entities with provenance per claim.

Examples:
- Stakeholder briefing (seed: a person's name or email) before a quarterly review or hard conversation
- Account dossier (seed: a customer/account) before an account check-in
- Competitor deep-dive (seed: company name) ahead of strategy work
- Feature archaeology (seed: feature slug or Jira epic) before scoping the next phase
- Person-of-interest pre-meeting prep (seed: name from calendar invite)

For specific questions, use `deep-research`. For multi-step planning, use `goal-plan`.

## Inputs

- `seed` (required) — examples: `"Periodical Training"`, `"natalie.benderly@ampfit.com"`, `"AFW-1234"`, `"hyrox"`, `"amp Connect"`
- `--max-depth N` (default 2) — recursion levels from seed
- `--max-breadth N` (default 8) — max new entities pursued per round per source
- `--sources s1,s2,...` — subset; defaults to all applicable for detected seed type
- `--budget-minutes N` — abort cleanly when hit
- `--exact` — disable embedding-similarity dedup (useful for entity-identity-sensitive runs)

## Source matrix (pick by seed type)

| Source | Tool | Best for |
|---|---|---|
| Slack | `slack_search_*` (channels, public, threads) | Internal discussion, mentions, decisions in chat |
| Gmail | `gmail_search_emails` | Email threads, external comms, meeting recaps |
| Calendar | `list_events` | Past/upcoming meetings about the entity |
| Jira | `searchJiraIssuesUsingJql` | Tickets, epics by JQL |
| Confluence | `searchConfluenceUsingCql` | Wiki pages, docs |
| Notion | `notion:search` | PRDs and pages in Notion |
| Monday | `monday:search` / `get_full_board_data` | Project boards |
| Common Room | `common-room:account-research`, `common-room:contact-research` skills | Account + person signals |
| gbrain | `gbrain:search`, `gbrain:recall`, `gbrain:get_backlinks` | Pre-synthesized facts, graph edges |
| claude-mem | `plugin_claude-mem_mcp-search:smart_search` | Past session memory |
| Web | `WebSearch`, `WebFetch` | Public web |
| Content dir | `Grep`, `Glob`, `Read` over `content/` | Internal PRDs, UXR, decision docs, competitor analysis |

## Steps

### 1. Detect seed type
Classify: `person` (name/email), `account` (company), `feature` (slug or PRD slug), `ticket` (Jira id), `concept` (free text), `url`.

### 2. Pick sources
Match to detected type. If no `--sources` flag, default to all applicable.

### 3. Round 0 fan-out
Issue ALL source queries in **ONE message**. Examples:

- For `person`: Slack search by name + email, Gmail search "from:X" + "to:X", Calendar list, Common Room contact research, gbrain search, content/ grep
- For `ticket`: Jira getJiraIssue + linked issues, Confluence CQL "AFW-1234", Slack search id, gbrain search
- For `concept`: gbrain + claude-mem + content/ grep + WebSearch

### 4. Extract entities
From each hit, surface entities (people, accounts, tickets, PRDs, URLs, terms). Lightweight regex + heuristics; only invoke LLM extraction if the source is unstructured prose.

### 5. De-dup
Drop entities already in the dossier. Default cosine-similarity threshold 0.92 (drop near-dupes). With `--exact`, disable similarity dedup.

### 6. Round k recursion
For each new entity (capped at `--max-breadth` per source), recurse to step 3 until depth ≥ `--max-depth` OR budget exhausted.

### 7. Aggregate
Build `{ nodes, edges }` graph. Each node: `{ id, type, attrs, sources: [...] }`. Each edge: `{ from, to, kind, source, confidence }`.

### 8. Render artifacts
Write to `content/08-feedback/dossiers/<slug>/`:

- **`<slug>.md`**:
  ```markdown
  # Dossier — <seed>
  **Generated:** YYYY-MM-DD
  **Depth:** N
  **Truncated:** yes | no

  ## Executive summary
  [3–5 sentences]

  ## Top entities
  | ID | Type | Sources | Notes |
  |----|------|---------|-------|
  | ... | person | slack, gmail | ... |

  ## Graph
  ```mermaid
  graph LR
    seed --> ...
  ```

  ## Findings by source
  ### Slack
  - [Finding with date and link]
  ### Gmail
  - ...

  ## Open threads
  - [What this dossier didn't cover]

  ## Sources scanned
  - [List]
  ```

- **`<slug>.json`** — machine-readable graph (see schema in dossier-investigator agent doc)

### 9. Persist as gbrain page
If seed is a durable entity (account, person, competitor), also create/update a gbrain page with the dossier summary so future sessions can recall it.

## Budget discipline

- If `--budget-minutes` hit, emit partial dossier with `truncated: true` and note the entities still queued
- BFS expansion — finish round *k* before round *k+1*
- Never silently truncate; always mark and record what was skipped

## Example invocations

```
/dossier-collect "Periodical Training"
/dossier-collect "natalie.benderly@ampfit.com" --max-depth 1
/dossier-collect "hyrox"
/dossier-collect "AFW-1234" --sources jira,confluence,slack
/dossier-collect "amp Connect" --max-breadth 5 --budget-minutes 15
```

## Principles

- **Seed-driven** (not question-driven) — for questions use `deep-research`
- **Provenance per claim** — every node/edge cites its source
- **De-dup, don't merge** — two sources naming same entity = same node with both sources, not a synthesized claim
- **Honor the budget** — partial dossier > runaway cost
- **BFS** — complete each round before the next
- **PII discipline** — surface what's PM-relevant; don't dump personal data
