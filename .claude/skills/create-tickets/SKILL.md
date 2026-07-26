---
name: create-tickets
description: Create tickets via Linear/Jira MCP or generate formatted ticket text
---

# Create Tickets Skill

Generate **experience tickets** from PRDs, feature specs, or task lists. Supports direct creation via Linear/Jira MCP or formatted text output.

## Durable rule 0 — Experience tickets only (overrides everything below)

**The PM writes only user-facing experience tickets. Never create backend, API, data, or infrastructure tickets.**

- Every ticket describes what the **member sees, taps, hears, or gets back** — not how it's built.
- Do NOT create `[API]`, `[DB]`, `[Backend]`, `[DevOps]`, "Ranking service", "Create X table", or "Add endpoint" tickets. Instead create "I want to see other users' ranking", "I want a rest timer between sets".
- The **iOS developer / tech lead** reads the experience ticket and opens their own backend tickets. That split is theirs to make, not the PM's.
- If an experience depends on backend work, name it in **one** `## Backend Dependency` line inside the experience ticket (e.g., "Requires a ranked-users feed — dev opens their own SW ticket") and stop. Never spec the contract, schema, or service.
- No Frontend-vs-Backend categorization, no "[DB] migration" tickets, no API-contract Technical Notes, no "Sprint 1 = database + API" grouping. Where the legacy guidance below conflicts, **this rule wins.**

## Quick Start

1. Point me to the source: PRD, feature spec, meeting action items, or describe the work
2. I break it down into well-structured tickets with acceptance criteria
3. Each ticket gets an effort estimate, dependencies, and component label
4. If Linear/Jira MCP is connected, I create tickets directly; otherwise, I generate copy-paste text
5. I provide a dependency summary and sprint assignment suggestion

**Example:** "Create tickets from content/prds/checkout-redesign.md targeting a March 15 launch"

**Output:** Tickets created in Linear/Jira, or saved to `content/10-outputs/analyses/[feature]-tickets.md`

**Time:** 15-30 minutes depending on PRD complexity

## SW project (Reflect team) — durable rules

These rules override the generic ticket-body template below for any ticket created in the **SW** Jira project.

### Keep stories short — only the essentials

A SW Story has **three sections** and that's it:

1. `## User Story` — one sentence: `As a <role>, I want <thing>, so that <outcome>.`
2. `## Requirements` — bulleted, one bullet per outcome the engineer must produce. No nested explanations of obvious things.
3. `## Definition of Done` — bulleted, the verifiable end state. 2–4 bullets.

**Do NOT include** these sections in SW Stories unless they carry real, non-obvious information:

- `## Assumptions` — drop unless there's a genuine open question the engineer needs flagged.
- `## Technical Notes` / `## Dependencies` / `## Resources` / `## Testing Requirements` — drop. QA goes in `customfield_10567`. Dependencies belong in Jira's link types, not the body.
- VoiceOver / a11y bullets — implied by "matches Figma 1:1". Only add an a11y bullet when the design omits an a11y detail and the engineer must invent it.
- `## Context` block at the top — the Figma smart-card (see below) and the User Story are the context.

Reference template: [SW-11191](https://amp-fit.atlassian.net/browse/SW-11191) — short version of the User Story / Requirements / DoD shape.

### Updating an existing ticket (anti-rot)

The description is the *current spec*, not a *changelog*. When requirements change:

- **Edit in place** and delete the superseded text. Never append a `vN change (date)` block, stack dated blockquotes, or leave `(was X)` / `(v12: …)` parentheticals.
- **If the ticket hasn't been started yet** (To Do / Backlog — no branch, no work logged, no one tracking against it), skip the changelog *entirely*. Don't add a dated note, don't add a pinned comment — just change the requirements. A "changed 10-9-26: …" line on a ticket nobody has read yet is pure noise. Dated history only earns its place once work is in flight and someone is reconciling against the old text.
- For tickets already in progress: history → git + at most **one** pinned comment.
- **Update the QA field (`customfield_10567`) in the same pass.** A QA step that contradicts a requirement is a bug.

### Epics — lean body (SW)

An epic body is Goal + scope + current behavior — **not** a retelling of its children:

1. `## Goal` — one or two lines + the success metric.
2. `## In scope` / `## Out of scope` — bullets; route out-of-scope items to the epic/PRD that owns them.
3. `## Current behavior` — present-tense rules, current only (same anti-rot rule as stories).
4. `## Dependencies` — firmware / design / other-epic links.
5. A one-line **source-of-truth** pointer (SOURCES.md or PRD path).

**Do NOT** re-narrate child stories with `### SW-xxxx — What/Why` blocks. The linked-issues panel *is* the child list; prose copies drift the moment a child is retitled, re-scoped, or re-parented. If build order matters, a bare list of keys grouped P0/P1 is enough.

### Attach the Figma board (smart-card render)

When a Figma URL is in scope, **put the bare URL on its own line at the very top of the description**, above the User Story. Jira's smart-link engine auto-renders it as a Figma preview tile, which is what "attaching the Figma board" actually means in this team's workflow — there's no separate Figma upload step, and `addRemoteIssueLink` is not exposed by the Atlassian MCP.

Format:

```
https://www.figma.com/design/<fileKey>/<file>?node-id=<frame-id>

## User Story
…
```

Use the deep-link to the **specific frame** (e.g., `node-id=10845-22063`), not the file root. The smart-card thumbnail comes from the frame.

Do NOT also put the Figma URL inside a `## Resources` section — that turns it into a plain link instead of a smart card.

### Link documents via Google Drive (not repo paths)

When a ticket references a document — the PRD, a design brief, a spec, an event-spec sheet, anything that isn't a Figma frame — link the **Google Drive copy**. Engineers open tickets in Jira; a `prds/…` path or an attached `.md` is useless to them, a Drive link opens in one click. This is the document equivalent of the Figma smart-card rule: frames get the smart-card URL, documents get the Drive link.

- **If the document is already in Drive**, link its `viewUrl`. PRDs live in the Shared Drive `0ACX6QAZMVEYNUk9PVA` ("Drive"), with **one folder per feature named by slug** (e.g. `social-profile` = `1Ol8yZvRDetkbBsPzmoTx2CP4t0jFrm6N`, `amp-connect` = `1E6teLTpuheVTgDwrmNj6l-BN610xHHdT`). Find the folder with Drive MCP `search_files` (`parentId = '0ACX6QAZMVEYNUk9PVA' and title = '<slug>'`), then locate the doc inside it.
- **If it isn't in Drive yet, upload it first, then link it.** Put it in the feature's folder under that Shared Drive — create the folder if missing (`create_file` with `mimeType: application/vnd.google-apps.folder`, `parentId: '0ACX6QAZMVEYNUk9PVA'`, `title: '<slug>'`). Upload markdown **raw** so it stays readable text, not a converted Google Doc: `create_file` with `textContent` = the file contents, `contentMimeType: 'text/markdown'`, `disableConversionToGoogleType: true`, `parentId: <feature-folder-id>`, `title: '<doc-name>.md'`. Then put the returned `viewUrl` in the ticket.
- Don't link a document twice (once as a Drive link, once as a repo path). The Drive link is the one engineers use.

## When to Use This Skill

- Breaking down PRDs into implementation tickets
- Converting feature specs into actionable tasks
- Batch ticket creation from roadmap items
- Generating ticket text for manual entry

## Prerequisites

**Optional but Recommended:**
- Linear MCP configured (for direct ticket creation)
- Jira MCP configured (for direct ticket creation)

**Fallback:**
- Generates formatted ticket text for manual copy-paste

## Workflow

### Step 1: Gather Context

Ask the PM:
1. **Source document:** PRD, feature spec, or task list?
2. **Target system:** Linear, Jira, or text output?
3. **Project/Team:** Which project/team should receive tickets?
4. **Ticket type:** Story, Task, Bug, Epic?
5. **Priority level:** High, Medium, Low?

### Step 2: Analyze Source Material

Read the source document and identify the **user-facing experiences** to ticket — what the member sees, taps, and gets back. One experience = one story.

Do **not** categorize work into frontend/backend/data/infra and ticket each layer. Backend, API, data-migration, and infra work are the developer's to open. If an experience clearly needs backend work, capture it as a single `## Backend Dependency` line on the experience ticket and move on.

### Step 3: Create Ticket Structure

For each ticket, generate:

**Title Format:** short, experience-framed, action-first. No `[API]`/`[DB]`/`[Backend]` component tags.

Examples:
- `Show user preferences screen with saved selections`
- `Let members pick and save a workout reminder time`
- `Show other users' ranking on the leaderboard`

**Ticket Body:**

```markdown
## Context
[Link to PRD or parent epic]

## Objective
[What this ticket accomplishes]

## Acceptance Criteria
- [ ] Specific outcome 1
- [ ] Specific outcome 2
- [ ] Specific outcome 3

## Backend Dependency
[One line only — names what backend work the developer opens as their own ticket. Omit if none. Never spec the contract or schema.]

## QA Instructions
1. [Start from a specific state]
2. [Single action]
3. [Expected result]

## Resources
- Design: [Figma link]
- Related PRD: [Link]
```

### Step 4: Create or Output Tickets

**If Linear MCP available:**
```
Use Linear MCP to create tickets directly
Set project, team, priority, labels
Link related tickets
```

**If Jira MCP available:**
```
Use Jira MCP to create tickets
Set epic, sprint, story points
Add components and labels
```

**Fallback - Text Output:**
```
Generate formatted ticket text
Number tickets sequentially
Provide copy-paste instructions
```

## Bulk Creation

When creating 5+ tickets:

1. **Create Epic first** (if applicable)
2. **Group by component** (Frontend, Backend, Data, etc.)
3. **Order by dependency** (foundation tickets first)
4. **Add estimates** (if PM provides sizing)
5. **Link tickets** (blockers, related work)

## Effort Estimation Framework

For each ticket, include an effort estimate using T-shirt sizing:

| Size | Time | Description | Example |
|------|------|-------------|---------|
| **XS** | <2 hours | Config change, copy update, simple fix | Update error message text |
| **S** | Half day | Single-file change, straightforward logic | Add input validation to a form |
| **M** | 1-2 days | Multi-file change, moderate complexity | Build a new API endpoint with tests |
| **L** | 3-5 days | Cross-component work, integration needed | Build complete CRUD feature with UI |
| **XL** | 1-2 weeks | Large scope, multiple systems involved | New authentication system |

**Estimation rules:**
- If the PM provides estimates, use them. If not, suggest one based on typical complexity for the work type.
- Always flag **XL tickets as candidates for splitting.** Suggest how to break them down: "This XL ticket could be split into [DB migration (M)] + [API layer (M)] + [Frontend (L)]."
- Include estimate in the ticket metadata, not buried in the body.
- When in doubt, round up. Underestimates erode trust; overestimates create buffer.

### Alternative: Story Points

Some teams prefer story points over T-shirt sizes. If the team uses story points:

| Points | Complexity | Roughly Equivalent To |
|--------|-----------|----------------------|
| 1 | Trivial change, well-understood | XS (few hours) |
| 2 | Small change, minimal unknowns | S (half day - 1 day) |
| 3 | Medium change, some unknowns | M (1-2 days) |
| 5 | Significant change, moderate unknowns | L (3-5 days) |
| 8 | Large change, many unknowns | XL (1-2 weeks) |
| 13 | Very large, high uncertainty | Split this ticket |

**Which to use:** Ask the PM or check existing tickets in the project management tool. Default to T-shirt sizes if unknown -- they're more intuitive for non-engineers.

**Ticket format with estimate:**
```
=== TICKET 1 ===
Title: Show user preferences screen with saved selections
Estimate: M (1-2 days)
...
```

## Sprint/Milestone Assignment

If the PM has a target launch date, work backwards from the deadline to suggest sprint assignments.

**Sprint grouping logic:**

```
Sprint 1 (Core experience):
- The primary user flow working end-to-end (happy path)
- The experiences that unblock other experiences

Sprint 2 (States & secondary flows):
- Empty / loading / error states
- Secondary or edge-case experiences

Sprint 3 (Polish):
- Accessibility and copy refinements
- Help / onboarding content
```
Sequencing is by member-visible experience, not by build layer. The developer sequences their own backend work behind these.

**Capacity check:**
- Assume 6-8 productive hours per developer per day
- Assume 80% utilization (meetings, reviews, context-switching)
- Sum ticket estimates per sprint and compare to available developer-days
- If estimated effort exceeds sprint capacity, flag: "Sprint 2 is overloaded by ~3 days. Consider moving [ticket X] to Sprint 3 or adding capacity."

## Handling Early-Stage or Partial PRDs

When the PRD is at Team Kickoff or Planning Review stage (requirements are still fuzzy):

**Adjust ticket creation:**
- Create "Spike" tickets for areas with high uncertainty: "[Spike] Investigate feasibility of [unclear requirement] -- Timebox: 2 days"
- Mark fuzzy requirements with a [TBD] tag: "Acceptance criteria TBD pending design review"
- Use wider T-shirt size ranges: "M-L (1-5 days) -- depends on API complexity once spike is complete"
- Add a "Requirements Checkpoint" ticket: "Review updated PRD with engineering before starting implementation"

**What NOT to do:**
- Don't create detailed acceptance criteria for fuzzy requirements (they'll change)
- Don't estimate with false precision (don't say "3 days" when you mean "1-2 weeks, maybe")
- Don't skip the tickets entirely -- even fuzzy work needs tracking

**Flag it:** Start the ticket breakdown with: "Note: PRD is at [Stage] stage. Some tickets have [TBD] acceptance criteria that will be refined as requirements solidify."

## Dependency Mapping

Identify and mark dependencies between tickets. Use explicit notation in each ticket:

```
## Dependencies
- **Blocked by:** TICKET-3 (DB schema must exist before API can be built)
- **Blocks:** TICKET-7 (Frontend needs this API to integrate)
```

**After generating all tickets, provide a dependency summary:**

```
## Dependency Summary

TICKET-1 [DB Schema] --> TICKET-3 [API Endpoints] --> TICKET-5 [Frontend Integration]
TICKET-2 [Auth Setup] --> TICKET-4 [Protected Routes] --> TICKET-5 [Frontend Integration]
TICKET-5 [Frontend Integration] --> TICKET-6 [E2E Tests]

Critical path: TICKET-1 --> TICKET-3 --> TICKET-5 --> TICKET-6
Estimated critical path duration: 7-10 days

Independent tickets (can be done in parallel):
- TICKET-7 [Documentation] -- no blockers
- TICKET-8 [Analytics instrumentation] -- no blockers
```

**Dependency rules:**
- Every ticket should state its dependencies (even if "None")
- Circular dependencies are a red flag -- restructure the tickets
- If a ticket has 3+ blockers, consider whether it should be split

## Ticket Quality Checklist

Before creating tickets, verify:
- ✅ Title is clear and specific
- ✅ Acceptance criteria are testable
- ✅ The member-facing experience is fully described
- ✅ Dependencies are identified
- ✅ Edge cases are documented
- ✅ Testing requirements are clear
- ✅ Links to designs/specs included

## Common Ticket Patterns

### Feature Work (experience stories only)
```
Epic: User Preferences
  ├── Show the preferences screen with current selections
  ├── Let members change and save a preference
  └── Show a confirmation after saving
```
The developer opens any backend/data tickets they need behind these — the PM does not.

### Bug Fixes
```
Title: [Component] Fix: Description of bug
Body:
  - Current behavior: [What's broken]
  - Expected behavior: [What should happen]
  - Repro steps: [How to reproduce]
  - Root cause: [If known]
```

### Backend dependency (not a PM ticket)
Infrastructure, DevOps, migrations, and API work are **not** PM tickets. If an experience needs them, add one `## Backend Dependency` line to the experience ticket; the developer opens the build ticket themselves.

## Integration Examples

### Linear MCP
```python
# Create epic
epic = linear.create_issue({
  "title": "User Preferences System",
  "description": "[Epic description]",
  "teamId": "team_id",
  "priority": 1
})

# Create child tickets
for ticket in tickets:
  linear.create_issue({
    "title": ticket.title,
    "description": ticket.body,
    "teamId": "team_id",
    "parentId": epic.id,
    "priority": ticket.priority
  })
```

### Jira MCP
```python
# Create epic
epic = jira.create_issue({
  "project": "PROJ",
  "issuetype": "Epic",
  "summary": "User Preferences System",
  "description": "[Epic description]"
})

# Create stories
for ticket in tickets:
  jira.create_issue({
    "project": "PROJ",
    "issuetype": "Story",
    "summary": ticket.title,
    "description": ticket.body,
    "epic_link": epic.key
  })
```

## Pro Tips

1. **One ticket, one thing:** Avoid "also do X" tickets
2. **Size appropriately:** 1-3 days ideal, split if larger
3. **Clear acceptance criteria:** Engineers know when done
4. **Link liberally:** PRDs, designs, related tickets
5. **Front-load context:** Engineers shouldn't hunt for info
6. **Call out edge cases:** "What happens if X?"
7. **Include examples:** API requests, UI states, data samples

## Output Format (Text Fallback)

```
=== TICKET 1 ===
Title: [Component] Action: Description
Project: [Project Name]
Type: Story
Priority: Medium

[Full ticket body]

=== TICKET 2 ===
...
```

## Common Mistakes to Avoid

❌ Vague titles: "Fix preferences"
✅ Specific titles: "[API] Fix: Preferences endpoint returns 500 on missing user"

❌ No acceptance criteria
✅ Clear checklist of outcomes

❌ Missing dependencies
✅ "Blocked by PROJ-123, Blocks PROJ-125"

❌ Backend-framed ticket: "[API] Add ranked-users endpoint"
✅ Experience-framed ticket: "Show other users' ranking" + a one-line Backend Dependency

❌ Orphan tickets (no epic/parent)
✅ Linked to parent epic or PRD

## Questions to Ask Before Creating

1. **Scope clarity:** Is this ticket too big/small?
2. **Dependencies clear:** What must happen first?
3. **Edge cases documented:** What could go wrong?
4. **Testing defined:** How will we verify this works?
5. **Rollback plan:** Can we undo if needed?

Remember: Great tickets save engineering hours. Invest time upfront to create clear, actionable work items.

---

## Context Routing Strategy

When the PM uses `/create-tickets`, I automatically:

### 1. Extract Source Material Understanding
**Source:** PRDs in `content/prds/`, or uploaded documents
- **What I look for:** Acceptance criteria, technical requirements, design context
- **How I use it:** Generate detailed tickets with full context
- **Example:** "PRD says 'mobile-first', I'll frame each experience ticket for the member on mobile"

### 2. Query Project Management MCPs
**Source:** Linear MCP, Jira MCP (if connected)
- **What I look for:** Existing epics, project structure, team assignments
- **How I use it:** Auto-link tickets to correct epic, assign to right teams
- **Example:** "Epic 'Voice Feature' exists, I'll link all tickets to it automatically"

### 3. Check Dependencies Across Roadmap
**Source:** `content/prds/`, related PRDs
- **What I look for:** What else is being built that might block this
- **How I use it:** Surface dependency tickets
- **Example:** "Notification system ships next sprint, Voice Feature depends on it"

### 4. Extract Acceptance Criteria from Success Metrics
**Source:** PRDs, `/feature-metrics` or `/impact-sizing` outputs
- **What I look for:** Testable success criteria
- **How I use it:** Convert metrics into ticket acceptance criteria
- **Example:** "Success metric 'adoption >60%' → AC: Feature instrumented to track adoption"

### 5. Route to Task/Ticket System
**Routing logic:**
- **Linear connected:** Create tickets directly in Linear
- **Jira connected:** Create tickets directly in Jira
- **Neither connected:** Generate formatted ticket text for manual entry
- **Complex dependencies:** Suggest ticket structure first before creation

---

## Output Quality Self-Check

Before delivering tickets, verify:

- [ ] **Every ticket has a clear, specific title** -- "[Component] Action: Description" format, no vague titles like "Fix stuff"
- [ ] **Every ticket has testable acceptance criteria** -- At least 2-3 checkboxes that define "done"
- [ ] **Every ticket has an effort estimate** -- T-shirt size (XS/S/M/L/XL) assigned to each
- [ ] **XL tickets flagged for splitting** -- Any ticket estimated at 1-2 weeks has a suggested breakdown
- [ ] **Dependencies mapped** -- "Blocked by" and "Blocks" noted; dependency summary provided at the end
- [ ] **Sprint/milestone assignment suggested** -- If launch date provided, tickets grouped into Sprint 1/2/3
- [ ] **Capacity checked** -- If sprint assignments given, total effort compared to available developer-days
- [ ] **Critical path identified** -- Longest dependency chain highlighted with duration estimate
- [ ] **PRD requirements fully covered** -- Every PRD acceptance criterion maps to at least one ticket
- [ ] **No orphan tickets** -- All tickets linked to parent epic or PRD
- [ ] **Experience fully described** -- A QA engineer can verify it yes/no; any backend need is a single Backend Dependency line, not a spec

If any check fails, fix it before delivering. Bad tickets slow engineering down more than no tickets at all.
