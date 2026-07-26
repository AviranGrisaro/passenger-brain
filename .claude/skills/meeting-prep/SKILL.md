---
name: meeting-prep
description: Prepare contextual briefing notes for an upcoming meeting. Gathers Slack messages, Jira tickets, PRDs, Gmail meeting notes (1 month back), and completed tasks, then synthesizes a rich prep note you can scan before walking in.
---

# Meeting Prep

Prepare me for an upcoming meeting by gathering all relevant context and writing a concise briefing.

## Inputs

- **Meeting title** (required): The calendar event summary
- **Attendees** (optional): List of people on the invite
- **Meeting time** (optional): When the meeting is scheduled

## What to gather

### 0. Attendee profiling (do this FIRST — it shapes everything else)
When attendees are provided, identify who each person is before gathering other context. This determines what to emphasize in the prep.

**How to identify attendees:**
1. Extract first names / display names from attendee emails (e.g., `serg@company.com` → search "Serg")
2. Use `slack_search_users` to look up each attendee — get their title, department, and role
3. Cross-reference with Jira: search `assignee = "Name"` to see what they're actively working on
4. Check `content/01-discovery/` for any saved notes about recurring collaborators

**Classify each attendee by function:**
- **Engineering** (backend, iOS, Android, web, QA) — focus on technical blockers, ticket status, code reviews
- **Design** (UX, UI, product design) — focus on Figma updates, design reviews, naming decisions, open design questions
- **Product** (PM, PO, analyst) — focus on PRD status, metrics, prioritization, roadmap alignment
- **Leadership** (VP, Director, C-level) — focus on high-level status, risks, decisions needed, timeline
- **Cross-functional** (marketing, ops, legal, data) — focus on their domain: launch plans, compliance, data requests

**How this shapes the prep:**
- If meeting is mostly engineers → lead with ticket status, blockers, PR reviews, technical decisions
- If meeting includes designers → add Design Updates section, mention any open Figma links or naming discussions
- If meeting has leadership → lead with summary/status, highlight risks and decisions needed, skip granular ticket details
- If it's a 1:1 → focus on the shared work between you and that person, their recent activity, and open threads between you two
- If attendees span multiple functions → balance the sections, but organize by what each group cares about

**Add to the output:** Include a brief "Who's in the room" line at the top of Key Context so you remember each person's role at a glance.

### 1. Slack messages (most important for context)
Search recent Slack messages (last 7 days) related to the meeting subject:
- Use `slack_search_public` with the meeting title keywords and attendee names
- Look for recap messages, status updates, blockers, decisions
- Extract key discussion points, open questions, and action items
- Pay special attention to messages from today and yesterday — they set the immediate context
- Search multiple queries if needed (topic keywords, attendee names, project names)
- **Search for messages FROM each attendee** about the meeting topic — their recent messages reveal what they'll likely bring up
- **Search for DM threads or channels where attendees are active** — look for side discussions that set context

### 2. Jira tickets
Find related Jira tickets using the Jira MCP tools:
- Search for tickets matching the meeting topic keywords
- **For each attendee**, search `assignee = "Name"` to find their active tickets — this shows what they're working on and what they'll likely bring up
- **Categorize tickets by status**: Stuck/Blocked, In Progress, Ready for QA, New/Not Started
- Flag tickets that haven't moved recently or have blockers
- Focus on PD (design), SW (dev), and AFW (QA) projects
- **Tag tickets with the attendee** who owns them — in the output, note "(Assignee: Name)" so you know who to ask about what

### 3. Related PRDs
Look in `content/prds/` for PRDs related to the meeting topic:
- Search PRD filenames and content for matching keywords
- Note the current state — draft, in review, approved
- Pull out any open questions or pending decisions

### 4. Gmail meeting notes and threads (1 month lookback)
Search Gmail for meeting-related context from the past 30 days:
- Use `gmail_search_messages` with queries like: `{meeting topic} meeting notes`, `{meeting topic} recap`, `{meeting topic} summary`
- Also search for threads with key attendees: `from:{attendee} {topic keywords}`
- Look for meeting recaps, decision logs, action items, and follow-up threads
- Extract decisions, commitments, and open items that the meeting audience should know about
- Pay special attention to release plans, rollout strategies, and cross-team alignment decisions
- These often contain context that isn't in Slack or Jira — like stakeholder alignment, legal decisions, or phased rollout plans agreed in smaller meetings

### 5. Done tasks
Check `content/06-execution/tasks/TASKS.md` for recently completed tasks related to the topic:
- Look in the `## Done` section for relevant items completed in the last 2 weeks

## Output format

Write a structured meeting prep note in **markdown**. The prep should read like a briefing, not a data dump. Synthesize the raw data into actionable context.

Use this structure (skip sections that have no content):

```markdown
### Who's in the Room
- **Name** — Role/Title (e.g., "iOS Engineer", "Design Lead"). 1 line per person.
- Note what each person is currently working on if you found relevant Jira tickets or Slack activity.
- For 1:1s, just note the person's role and recent focus areas.

### Key Context
- 2-4 bullet points summarizing the current state of the project/topic
- Pull from Slack recaps, recent decisions, blockers
- Use **bold** for key names, statuses, and decisions
- This is the "here's what's happening right now" section
- **Tailor emphasis based on who's in the room** — if it's engineers, lead with technical state; if leadership, lead with status and risks

### Stuck / Blocked Tickets
| Ticket | Summary | Assignee | Status |
|--------|---------|----------|--------|
| SW-XXX | ... | ... | **Stuck** |

Only include tickets that are actually stuck, blocked, or overdue. If none, skip this section.

### In Progress
- SW-XXX — Brief summary (Assignee)

### Ready for QA / Review
- SW-XXX — Brief summary (Assignee)

### New / Not Started
- SW-XXX — Brief summary

### Design Updates
- Any design-related context from Slack or Jira (Figma updates, design reviews, naming changes)

### Your Action Items Going In
1. **Item** — what you need to do or prepare for
2. ...

Based on Slack context + Jira state, list things YOU specifically need to address or bring up.

### Questions to Raise
- What's blocking X?
- Timeline check: are we on track for Y?
- Any unresolved decisions from Slack threads?

Based on stuck tickets and open threads, suggest 2-4 questions to bring up.
```

## How to save

After generating the prep note, save it to `content/09-meetings/prep/<slug>.md` where `<slug>` is the meeting title slugified (lowercase, hyphens, no special chars).

Example: "Subscription technical talk" → `content/09-meetings/prep/subscription-technical-talk.md`

The file should contain only the raw markdown content (no frontmatter, no top-level heading). The dashboard will pick it up and render it automatically.

Create the directory if it doesn't exist: `mkdir -p content/09-meetings/prep/`

## Usage

When a user clicks a meeting in the Calendar or Tasks tab, the dashboard checks for a saved prep file. If none exists, it shows a prompt to generate one. The user can trigger this skill by saying "prep me for [meeting name]" or clicking a meeting and asking for prep.

The prep note should be concise and scannable — it's meant to be glanced at 5 minutes before the meeting starts. Don't pad with fluff. Lead with the most important context.
