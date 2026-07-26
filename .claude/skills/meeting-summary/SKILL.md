---
name: meeting-summary
description: Summarize a meeting from Gmail (Zoom recap, Fireflies, Fathom, Granola, manual notes) or pasted text into a tight decisions + action items + open questions output, and append owner-assigned action items to TASKS.md and dashboard.html in sync. Trigger when the user says "summarize this meeting", "to-do list from meeting notes", "action items from yesterday's meeting", "recap the [X] sync", or references a Gmail thread / meeting recap.
---

## Purpose

Turn a meeting (or its recap email / transcript / notes) into:
1. A tight chat summary — **decisions, action items with owners, open questions**. No fluff.
2. Owner-assigned action items appended to `content/06-execution/tasks/TASKS.md` AND synced into the `EMBEDDED_TASKS_MD` constant in `content/06-execution/tasks/dashboard.html` (per CLAUDE.md sync rule).

This is **not** `meeting-notes` (that skill scores meeting effectiveness 1–5). This is for synthesis + action capture.

## When to Use

- After a Zoom/Fireflies/Fathom/Granola recap arrives in Gmail
- When the user pastes raw meeting notes and wants structure
- When the user says "what was the to-do list from [meeting]"
- When a meeting just happened and needs to be turned into trackable work

## Quick Start

Ask the user upfront (use AskUserQuestion):

1. **Source** — Gmail (search broadly / specific thread / paste notes)
2. **Output destination** — Append to TASKS.md (default), standalone meeting note in `content/09-meetings/prep/`, or both
3. **Depth** — Tight (decisions + actions only) or Full recap (topics + context + actions)

Defaults if user just says "do it":
- Source: search Gmail for the relevant thread
- Output: Append to TASKS.md + sync dashboard.html
- Depth: Tight

## Prior Learnings (load first)

Surface prior learnings about this team / meeting series before summarizing:

```bash
bash /Users/avirang/Documents/amp/scripts/learnings-search.sh --skill meeting-summary --limit 10
```

If the meeting is a recurring sync (e.g., "Reflect sync", "Device Lock sync"), search by name:
```bash
bash /Users/avirang/Documents/amp/scripts/learnings-search.sh --query "<meeting-name>" --limit 5
```

If a returned learning matches a recurring pattern (same attendee always has the same blocker; same topic keeps getting deferred), note it inline: **"Prior learning applied: [key] (confidence N/10)"**.

---

## Workflow

### 1. Locate the meeting
- If user names attendees → Gmail `search_threads` with `from:` or to: filters, plus `newer_than:30d`
- Prefer recap emails from `no-reply@zoom.us`, `no-reply@fathom.video`, `fireflies.ai`, `granola.ai` over calendar invites
- A Zoom calendar invite is **not** a recap — only use it to confirm date/attendees
- If multiple candidates, ask user to disambiguate

### 2. Pull the recap content
- `get_thread` with `messageFormat: FULL_CONTENT`
- Parse the HTML body — Zoom recaps embed structured sections: `Quick recap`, `Next steps` (per person), `Summary` (per topic)
- Fathom recaps have: `Meeting Purpose`, `Key Takeaways`, `Topics`, `Action Items`
- If recap is in another language (Zoom sometimes auto-detects Polish/Hebrew), still parse it — translate to English for the chat summary

### 3. Extract structure
Map content to four buckets:
- **Decisions** — explicit choices made ("agreed to remove rep counting for paying users")
- **Action items** — owner + verb + outcome (use `@people(Name)` annotation)
- **Open questions** — things that weren't resolved
- **Context** (Full depth only) — short topic-by-topic recap

### 4. Reframe for PM tracking
The recap lists action items by speaker (often dev-heavy). As PM, Aviran's job is to:
- File / verify dev tickets exist for each implementation item
- Track owners and follow up
- Test critical flows
- Share notes

When appending to TASKS.md, frame items as **PM follow-ups**, not raw dev tasks. Example:
- Recap says: "Gabriel: Implement loading state/spinner"
- TASKS.md entry: `- [ ] **Confirm dev ticket exists for loading state/spinner** - From May 18 Device Lock sync w/ Gabriel @people(Gabriel)`

### 5. Append to TASKS.md
- Add a new subsection under `## Active` titled: `### [Meeting Name] — [Date] (w/ [Attendees])`
- Each item: `- [ ] **[Short title]** - [Context]. From [meeting] @people(Owner)`
- Preserve all existing content. Insert the new subsection at the end of `## Active`, before `## Waiting On`.

### 6. Sync dashboard.html
- Open `content/06-execution/tasks/dashboard.html`
- Find the `EMBEDDED_TASKS_MD` constant (around line 1884)
- The embedded version may be stale — that's OK, just add the same new subsection block to it. Do NOT try to reconcile the rest of the drift unless user asks.
- Use Edit, not Write — preserve everything else.

### 7. Report back
In chat, deliver the summary in this format:

```
# [Meeting Name] — [Date]
**Attendees:** [Names]
**Source:** [Gmail thread / Zoom recap link if available]

## Decisions
- [Decision 1]
- [Decision 2]

## Action Items
| # | Owner | Item | Due |
|---|-------|------|-----|
| 1 | Gabriel | Implement loading state | — |
| 2 | Aviran | Test flow w/ Shalom | — |

## Open Questions
- [Question 1]

## What I did
- Appended N action items to TASKS.md under "### [Subsection]"
- Synced dashboard.html EMBEDDED_TASKS_MD
```

## Rules

- **Tight by default.** Decisions + action items + open questions. Skip narrative unless user asked for Full depth.
- **Every action item has an owner.** If recap doesn't say, mark `@people(?)` and flag it as a question.
- **No invented context.** If the recap is sparse or in a foreign language with minimal content, say so — don't fabricate.
- **Preserve TASKS.md and dashboard.html.** Append, don't overwrite. Use Edit, not Write.
- **Both files always.** Per CLAUDE.md: every task change updates BOTH TASKS.md and dashboard.html EMBEDDED_TASKS_MD.
- **Date format:** Use the meeting date, not today's date, for the subsection title.

## Common Sources & How to Parse Them

| Source | Sender | Where the gold is |
|--------|--------|-------------------|
| Zoom AI Companion | `no-reply@zoom.us`, subject "Meeting assets for [name] are ready!" | `<h2>Quick recap</h2>`, `<h2>Next steps</h2>` (with `<h3>` per person), `<h2>Summary</h2>` |
| Fathom | `no-reply@fathom.video`, subject "Recap of your meeting with [team]" | "Meeting Purpose", "Key Takeaways", "Action Items" |
| Fireflies | `fred@fireflies.ai` or `notes@fireflies.ai` | Action items list, transcript link |
| Granola | `notes@granola.ai` | Markdown body — already structured |
| Manual notes | User paste / Apple Notes | Free-form — apply the structure yourself |

## Edge Cases

- **Empty / minimal recap:** Some Zoom AI summaries fail when the meeting had little speech. Report this honestly: "Recap was too sparse to summarize. View the Zoom recap directly: [link]"
- **Multiple meetings in the thread:** Zoom sometimes sends 2 recaps in one thread (e.g., retry after empty transcript). Use the one with substantive content.
- **No clear Mike/owner:** If user said "meeting with X and Y" but only X appears as a speaker, note this and proceed with what's available.

## Capture Learnings (run at skill end)

After producing the summary, log any pattern about this meeting series, attendee, or topic that would save 5+ minutes next time. Schema: `content/01-discovery/learnings-schema.md`.

```bash
bash /Users/avirang/Documents/amp/scripts/learnings-log.sh \
  --skill meeting-summary \
  --type <pattern|pitfall|operational> \
  --key <meeting-or-attendee-slug> \
  --insight "1-2 sentence pattern — recurring blocker, attendee preference, topic that keeps stalling." \
  --confidence <1-10> \
  --source observed
```

Good things to log: an attendee who always says yes in the meeting but never delivers; a topic that always slips on this sync (consider escalation pattern); a meeting series whose actual decisions take 2-3 sessions, not 1 (plan accordingly). **Skip:** specific action items — those go to TASKS.md, not learnings.

---

## Integration

- **Before:** `/meeting-prep` (briefing before the call)
- **After:** This skill (summary + actions)
- **Then:** `/meeting-notes` (effectiveness scoring) and `/meeting-cleanup` (batch processing)
