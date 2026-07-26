---
name: daily-summary
description: Generate end-of-day summary of Slack and Jira activity, tailored by role
disable-model-invocation: false
user-invocable: true
---

## Quick Start

**What to provide:** Nothing required. Just run it.

```
/daily-summary              → Generate today's activity summary
/daily-summary yesterday    → Generate yesterday's summary
/daily-summary 2026-03-15   → Generate summary for a specific date
```

**What you get:** A role-aware summary of what happened today across Slack (DMs + channels) and Jira (design board + dev pipeline), formatted for your specific role and delivered via Telegram + saved to the dashboard.

**Time:** 1-3 minutes.

---

## How It Works

### Step 0: Authentication

Check for the `PRODUCT_OS_TOKEN` environment variable. If present, include it as a Bearer token on **all** Product OS API calls:

```
Authorization: Bearer $PRODUCT_OS_TOKEN
```

If not present, the API relies on the browser session cookie (interactive use only). Set the auth header on every API call in steps 1, 3, and 6.

### Step 1: Identify the User

Read the user's config from the Product OS server to determine their role:

```
GET http://localhost:5174/api/user/settings
Authorization: Bearer $PRODUCT_OS_TOKEN   (if env var is set)
```

Extract: `role` (pm | designer | design-lead), `name`, `email`

If no role is set, use `pm` as the default.

### Step 2: Gather Slack Activity

Use the **Slack MCP** tool `slack_search_public_and_private` to search for messages involving the user today.

**Search queries to run:**
1. `from:@{user_name}` with date filter for today — messages the user sent
2. `to:@{user_name}` OR `@{user_name}` with date filter — messages mentioning the user

**Group results into:**
- **DMs**: Direct messages (channel type = "im" or "mpim")
- **Channel mentions**: Messages in public/private channels where the user was mentioned or participated

For each message, extract: sender name, channel name, message preview (first 100 chars), permalink, timestamp.

If Slack MCP is not available, note this in the summary and skip the Slack section.

### Step 3: Gather Jira Activity

Fetch today's Jira activity from the server API:

```
GET http://localhost:5174/api/jira/today-activity?role={role}
```

The response structure depends on role:

**Design Lead** returns:
- `pdBoard.updated` — ALL PD tickets updated today
- `pdBoard.created` — PD tickets created today
- `pdBoard.statusChanges` — PD tickets with status changes
- `swDesignRelated.updated` — SW tickets linked to design, updated today
- `swDesignRelated.statusChanges` — SW design-related status changes

**Designer** returns:
- `myDesignTickets.updated` — User's assigned PD tickets updated today
- `myDesignTickets.statusChanges` — Status changes on user's tickets
- `linkedDev.updated` — Linked SW/QA tickets updated today
- `linkedDev.statusChanges` — Status changes on linked dev tickets

**PM** returns:
- `reportedTickets.updated` — Tickets reported by user, updated today
- `reportedTickets.statusChanges` — Status changes on reported tickets
- `reportedTickets.byProject` — Grouped by project (SW, PD, AFW)

### Step 4: Format the Summary

Format based on role:

#### Design Lead Template
```markdown
# Daily Summary — {date}

## Slack Highlights
### DMs ({count})
- **{sender}**: {preview}...

### Channel Activity ({count} channels)
- **#{channel}** ({messageCount} messages): {highlight}

## PD Board Activity ({total} tickets updated)
### Status Changes
| Ticket | Summary | Status | Assignee |
|--------|---------|--------|----------|

### New Tickets Created
| Ticket | Summary | Assignee |
|--------|---------|----------|

## Dev Pipeline (Design-Related)
### SW Tickets Updated ({count})
| Ticket | Summary | Status | Source Design |
|--------|---------|--------|---------------|

## Highlights
- {auto-generated highlights based on the data}
```

#### Designer Template
```markdown
# Daily Summary — {date}

## Slack Highlights
{same as above}

## My Design Tickets ({count} updated)
| Ticket | Summary | Status |
|--------|---------|--------|

## Dev Status on My Designs ({count})
| Dev Ticket | Summary | Status | My Design Ticket |
|------------|---------|--------|-------------------|

## Highlights
- {highlights}
```

#### PM Template
```markdown
# Daily Summary — {date}

## Slack Highlights
{same as above}

## My Tickets Updated ({count})
### By Project
**SW ({count}):** ...
**PD ({count}):** ...

| Ticket | Summary | Status | Project |
|--------|---------|--------|---------|

## Highlights
- {highlights}
```

### Step 5: Generate Highlights

Based on the data, generate 3-5 bullet-point highlights:
- Tickets that moved to "Done" today
- Tickets that are blocked or stuck
- New tickets created
- Notable Slack conversations (high activity channels, important DMs)
- Handoff status (for design roles: designs waiting on dev, or dev tickets blocked on design)

### Step 6: Save the Summary

POST the structured summary to the Product OS server:

```
POST http://localhost:5174/api/daily-summary
Content-Type: application/json

{
  "date": "YYYY-MM-DD",
  "generatedAt": "{ISO timestamp}",
  "role": "{role}",
  "slack": {
    "dms": [...],
    "channels": [...],
    "totalMessages": {count}
  },
  "jira": {
    // role-specific fields as returned by /api/jira/today-activity
  },
  "highlights": [...]
}
```

### Step 7: Send via Telegram (if configured)

Check if the user has Telegram configured in their settings. If yes, format a compact version of the summary and send it.

Use the Telegram MCP or call the Product OS API to send the message. Format for Telegram (4096 char limit):

```
📊 Daily Summary — {date}

💬 Slack: {dm_count} DMs, {channel_count} channels
📋 Jira: {ticket_count} tickets updated

🔑 Highlights:
• {highlight 1}
• {highlight 2}
• {highlight 3}

Full summary → Dashboard > Summary tab
```

---

## Output

The skill produces:
1. **Saved JSON** at `data/users/{userId}/summaries/{date}.json` (via POST API)
2. **Telegram message** (if configured) with compact summary
3. **Console output** showing the formatted summary to the user

---

## Notes

- The skill uses the Product OS server API (localhost:5174) for Jira data — the server must be running
- Slack data comes from the Slack MCP tool — if not connected, the Slack section is skipped
- The Jira `/today-activity` endpoint handles all role-based filtering server-side
- Summaries are idempotent — running twice for the same date overwrites the previous summary
