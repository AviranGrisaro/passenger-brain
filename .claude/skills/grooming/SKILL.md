---
name: grooming
description: Sprint grooming — assess ticket readiness, estimate effort, map dependencies, and produce a sprint readiness report for the dev team
user-invocable: true
---

# Sprint Grooming Skill

Groom the next sprint for the **Reflect** team: fetch all tickets, assess readiness, group by engineer, estimate effort, map dependencies, and produce a structured grooming prep report.

## Quick Start

1. I discover the next sprint and pull **all** Reflect team tickets (handling pagination)
2. I fetch full details for each ticket
3. I group tickets by engineer and assess spec quality
4. I identify risks: underspecced tickets, overloaded engineers, priority conflicts
5. I generate a grooming prep report with a suggested agenda

**Usage:** `/grooming`

**Output:** Saved to `content/10-outputs/analyses/YYYY-MM-DD-grooming-sprint-NN.md`

## When to Use This Skill

- Before sprint planning to ensure tickets are well-defined
- Mid-sprint to assess incoming tickets for the next sprint
- After `/create-tickets` to verify ticket quality before the grooming meeting
- When the dev team reports unclear requirements or missing context

## Context Routing

**Check these sources:**
1. **Jira sprint data** — via MCP `searchJiraIssuesUsingJql` (primary) or cached `content/06-execution/jira/tickets.json` (fallback)
2. **PRDs** — `prds/<feature-slug>/<feature-slug>.md` for feature context and acceptance criteria
3. **Strategy** — `content/strategy/` for priority alignment with quarter goals
4. **Previous grooming reports** — `content/10-outputs/analyses/*-grooming-*.md` for continuity

**MCP tools used:**
- `searchJiraIssuesUsingJql` — query sprint tickets (cloudId: `amp-fit.atlassian.net`)
- `getJiraIssue` — fetch full ticket details (description, AC, links)
- `editJiraIssue` — optional: update fields after PM confirmation
- `getTransitionsForJiraIssue` — check available status transitions

**Graceful degradation:** If Jira MCP is unavailable, fall back to `content/06-execution/jira/tickets.json`. The cached data has: key, summary, status, statusCategory, priority, assignee, reporter, issueType, dueDate, sprint, version, labels, url, linkedTickets, epicKey, team. Note: cached data lacks full descriptions — flag this limitation in the report.

---

## Workflow

### Step 1: Discover the Next Sprint and Fetch ALL Reflect Team Tickets

**IMPORTANT: The Jira `team` JQL keyword does NOT work for our instance. Team is stored in `customfield_10001`. You MUST filter by team client-side after fetching results.**

1. **Find the next (future) sprint tickets** using JQL via `searchJiraIssuesUsingJql`:
   ```
   JQL: sprint in futureSprints() AND project = SW ORDER BY rank ASC
   cloudId: amp-fit.atlassian.net
   maxResults: 100
   fields: summary, description, status, issuetype, priority, assignee, labels, parent, customfield_10016, customfield_10001, customfield_10020
   responseContentFormat: markdown
   ```

   **Field reference:**
   - `customfield_10001` = **Team** (e.g., `{name: "Reflect"}`)
   - `customfield_10016` = **Story Points**
   - `customfield_10020` = **Sprint** (contains sprint id, name, state, dates)

2. **Handle large result sets:** If the result is saved to a file (too large for inline), use `jq` to extract and filter:
   ```bash
   cat <result-file> | jq -r '.[0].text' | jq '[.issues[] | select(.fields.customfield_10001.name == "Reflect") | {key, summary: .fields.summary, type: .fields.issuetype.name, status: .fields.status.name, priority: .fields.priority.name, assignee: (.fields.assignee.displayName // "Unassigned"), points: .fields.customfield_10016, parent: (.fields.parent.key // null), labels: .fields.labels}]'
   ```

3. **Handle pagination:** If `nextPageToken` is present in the response, make additional queries with that token until all results are fetched. Always verify total count.

4. **Extract sprint metadata** from the first ticket's `customfield_10020` field:
   - Sprint name (e.g., "Sprint 16")
   - Sprint ID
   - Start date and end date
   - Sprint state (should be "future")

5. **If `futureSprints()` returns empty**, fall back to finding the next sprint by ID:
   - Query current sprint: `sprint in openSprints() AND project = SW`
   - Read the sprint field to get the current sprint ID
   - Query: `Sprint = <currentSprintId + 1>` (sprint IDs are sequential on the same board)

**Output of this step:** Complete list of Reflect team ticket keys, sprint name/number/dates.

---

### Step 2: Fetch Full Ticket Details

For each Reflect team ticket, call `getJiraIssue` with:
- `issueIdOrKey`: the ticket key (e.g., SW-123)
- `cloudId`: `amp-fit.atlassian.net`
- `responseContentFormat`: `"markdown"`
- `fields`: `["summary", "description", "status", "priority", "assignee", "customfield_10016", "parent"]`

Extract and store for each ticket:
- **summary** — ticket title
- **description** — full description in markdown
- **acceptance criteria** — look for checkbox lists (`- [ ]`) or "Definition of Done" sections
- **priority** — Highest/High/Medium/Low
- **assignee** — who's assigned (or unassigned)
- **issueType** — Story/Bug
- **parent** — epic key
- **story points** — from customfield_10016

**Parallel fetching:** Fetch up to 5-6 tickets concurrently using parallel tool calls to save time.

---

### Step 3: Cross-Reference with PRDs

For each ticket, attempt to match it to a PRD:

1. **Epic match:** Check parent epic key — match epic name against folder names in `content/prds/`
2. **Label match:** Check `labels` — labels often contain feature slugs that match PRD directories
3. **Keyword match:** Search ticket `summary` terms against PRD directory names

When a PRD match is found, read the PRD and extract:
- **Feature context** — what is this ticket part of?
- **Acceptance criteria from PRD** — AC that should be reflected in the ticket but isn't

If no PRD match is found, note it — orphan tickets without PRD context may indicate missing specs.

---

### Step 4: Per-Ticket Assessment

For each ticket, evaluate:

| Criterion | ✅ Pass | ⚠️ Partial | ❌ Fail |
|-----------|---------|------------|---------|
| **Description** | 3+ sentences with context | Thin (1-2 sentences) | Empty or placeholder |
| **Acceptance criteria / DoD** | 3+ testable items | 1-2 items | None |
| **Assignee** | Developer assigned | Team but no individual | Unassigned |
| **Story points** | Points set | — | No estimate |
| **Design spec linked** | Figma/PD ticket referenced | Mentioned but no link | None when needed |
| **QA instructions** | Step-by-step QA plan | Brief notes | None |

**Spec quality rating:**
- ✅ **Well-specced** — has description + AC/DoD + assignee. Ready for grooming discussion.
- ⚠️ **Partially specced** — missing some elements but intent is clear. Needs minor updates.
- ❌ **Underspecced** — missing description, no AC, or placeholder text. Needs work before sprint.

---

### Step 5: Generate Grooming Prep Report

Group tickets by engineer and produce a practical grooming prep document.

**Report structure:**

```markdown
# Sprint NN — Reflect Team Grooming Prep

**Sprint:** [start date] – [end date]
**Team:** Reflect
**Engineers:** [list from assignees]
**Tickets:** N | **Estimated:** X/N

---

## All Tickets

| # | Ticket | Summary | Type | Status | Pri | Assignee | Specced? |
|---|--------|---------|------|--------|-----|----------|----------|
| ... | ... | ... | ... | ... | ... | ... | ✅/⚠️/❌ |

---

## Grouped by Engineer

### [Engineer Name] (N tickets)

**[Theme/Epic group]:**
- **SW-XXXX** — [Summary]. [1-2 sentence assessment]. **Question:** [grooming question if any]

**Bugs:**
- **SW-XXXX** — [Summary]. **Question:** [still reproducible?]

**Tech debt:**
- **SW-XXXX** — [Summary]. **Question:** [scope?]

[Repeat for each engineer]

---

## Issues to Resolve in Grooming

### 1. Underspecced tickets
| Ticket | Issue | Action needed |
|--------|-------|---------------|
| ... | ... | ... |

### 2. Missing estimates
[Count and list]

### 3. Status updates needed
[Tickets stuck in wrong status]

### 4. Prioritization conflicts
[Engineer overload, competing initiatives]

---

## Suggested Grooming Agenda (~NN min)

1. **Triage underspecced tickets** (N min) — [list]. Spec now or defer?
2. **[Engineer]'s tickets** (N min) — [key decisions]
3. **[Engineer]'s tickets** (N min) — [key decisions]
4. **Capacity check** (N min) — must-haves vs nice-to-haves

---

## Risks
- [Key risk 1]
- [Key risk 2]
- [Key risk 3]
```

Save the report to:
```
content/10-outputs/analyses/YYYY-MM-DD-grooming-sprint-NN.md
```

---

### Step 6: Offer to Update Jira

After presenting the report, ask the PM:
> "I found N tickets that need updates (missing AC, estimates, descriptions). Should I update them in Jira?"

This requires **explicit PM confirmation** before making any changes. If confirmed, use `editJiraIssue` via MCP to:
- Add acceptance criteria templates to tickets missing AC
- Improve thin descriptions with context from PRDs
- Add dependency links between related tickets

**Never auto-update Jira without asking first.**

---

## Output Quality Self-Check

Before delivering the report, verify:
- [ ] ALL Reflect team tickets are included (pagination handled, client-side team filter applied)
- [ ] Every ticket has been individually fetched for full description
- [ ] Tickets are grouped by engineer with practical grooming questions
- [ ] Underspecced tickets are flagged with specific missing elements
- [ ] Engineer workload balance is assessed (flag if anyone has >7 tickets)
- [ ] Priority conflicts are identified (competing initiatives for same engineer)
- [ ] Sequential dependencies within epics are noted
- [ ] Suggested grooming agenda has time estimates
- [ ] Report saved to `content/10-outputs/analyses/YYYY-MM-DD-grooming-sprint-NN.md`

---

## Integration with Other Skills

**Before `/grooming`:**
- `/create-tickets` — populate the backlog with well-structured tickets from PRDs
- `/prd-draft` — ensure PRDs exist for features being groomed

**After `/grooming`:**
- `/daily-plan` — surfaces grooming action items in daily planning
- Sprint planning meeting — use the grooming report as the input artifact
- `editJiraIssue` via MCP — apply approved updates to Jira tickets

**Complementary:**
- `.claude/agents/sprint-planner.md` — handles capacity analysis and sprint scope recommendations. Grooming ensures ticket quality; sprint planning ensures sprint scope. They are sequential: groom first, then plan.
