---
name: update-context
description: Capture the current conversation's product thinking into the active project's working doc. Updates locked decisions, open questions, risks, and next steps without overwriting existing content. Use when the PM has been iterating on a product direction in chat and wants to persist the state before context is lost. Trigger with "/update-context", "update the context", "save what we've discussed", "capture this into the project", or "persist this thinking".
disable-model-invocation: false
user-invocable: true
---

<!-- filename-convention-block -->
## Filename Convention

**Save the output as `[feature-name-kebab]_working-doc.md`** inside the project folder (`content/13-projects/<feature-slug>/`).

- **Never use generic names** like `notes.md`, `working.md`, `context.md`. Always prefix with the feature/initiative name.
- **No date prefix.** Use git/mtime for chronology.
- Working docs are pre-PRD scratch. Once direction is locked, promote to `prd-draft` via `/prd-draft`.

---

# /update-context — Persist Conversation Thinking into Project Files

When the PM types `/update-context`, capture the iterative thinking from the current chat into the active project's working doc. **Merge, don't overwrite.** The goal is to make conversation state durable without losing prior structure.

## When to Use

- Mid-iteration on a product direction, before context is lost or the chat session ends.
- After a critique-and-respond loop where decisions are getting locked piece by piece.
- When the PM says "update the context" or describes wanting to "save this thinking" before moving on.

## When NOT to Use

- For finalized decisions with sign-off → use `/decision-doc`.
- For a polished PRD → use `/prd-draft`.
- For meeting recaps → use `/meeting-summary`.
- For a one-off note or single fact → just write the file directly.

---

## Inputs (ask only if missing)

- **Project slug** (required) — derive from conversation topic. If ambiguous between 2+ projects, ask.
- **Folder location** — default `content/13-projects/<slug>/`. Create if missing.
- **Anything to explicitly exclude** — optional; ask only if the conversation covered multiple topics.

If the project folder doesn't exist:
1. Confirm the slug with the PM.
2. Create `content/13-projects/<slug>/`.
3. Initialize the working doc with the standard structure (below).

---

## How It Works

1. **Detect active project** from conversation. If unclear, ask one question.
2. **Read existing working doc** if present at `content/13-projects/<slug>/<slug>_working-doc.md`.
3. **Extract from current chat:**
   - Locked decisions (things the PM said "yes" to or stated as direction)
   - Open questions (things flagged as "open", "TBD", "to decide", or where I gave a recommendation awaiting confirmation)
   - Risks to manage (problems surfaced that aren't fully resolved)
   - Decisions made in this turn vs. prior turns (use existing doc for diff)
   - Items killed or descoped from prior plans
   - Next steps
4. **Merge into the doc** — append new items with date, mark superseded items as such (don't delete), update the recommended default for open questions if it changed.
5. **Run critic pass** (per CLAUDE.md writing rules).
6. **Save + backup** (per CLAUDE.md per-turn backup rule).
7. **Return** file path + 1-paragraph summary of what changed.

---

## Working Doc Structure

```markdown
# <Feature Name> — Working Doc

**Status:** Pre-PRD scratch. Iterating direction.
**Owner:** Aviran
**Last updated:** <YYYY-MM-DD>
**Source thread:** This doc reflects iterative product thinking. Promote to PRD via `/prd-draft` when direction locks.

---

## Product Framing

<1–3 sentences describing what this product actually is, in plain language. Update when framing changes. Mark prior framings as superseded — don't delete.>

---

## Locked Decisions

Append-only log. Each entry: short title, the decision in plain English, date.

- **<YYYY-MM-DD> — <Decision title>:** <Decision.>
- **<YYYY-MM-DD> — <Decision title>:** <Decision.>

---

## Open Questions

Numbered list. For each, give the question, current recommended default, and what blocks the decision.

1. **<Question>** — Recommended default: <answer>. Blocked on: <person/data/conversation>.
2. **<Question>** — Recommended default: <answer>. Blocked on: <person/data/conversation>.

When a question gets answered, move it to Locked Decisions (don't delete from history — annotate as resolved).

---

## Risks to Manage

Risks surfaced but not yet designed for. Each one needs an owner + a plan target.

- **<Risk>** — Plan to address in: <PRD section / decision / next conversation>.

---

## Killed / Descoped

What was previously planned that this direction kills. Cross-link to the doc that originally proposed it.

- **<Item>** — Replaced by <new direction>. Original: <file path>.

---

## Reconciliations Needed

Other docs in the workspace that need updating because of this direction shift. List the file + what needs updating + who needs to be informed.

- **<File path>** — needs <change>. Inform: <person>.

---

## Next Steps

Numbered, with owner and target.

1. <Action> — @<Owner> — by <date or trigger>.

---

## Change Log

Append at every `/update-context` run. One line per run.

- **<YYYY-MM-DD>** — <what changed in this update, ~1 sentence>.
```

---

## Merge Rules

**Locked Decisions:** Append-only. Never remove. If a prior decision is reversed, add the new decision with date, and append `(supersedes <date of original>)` to the new entry. Mark the original `(superseded <new date>)`.

**Open Questions:** Update the recommended default if the conversation changed it. If a question becomes resolved, move it to Locked Decisions with the resolution. Keep the question text intact for audit trail.

**Product Framing:** If framing shifted in this conversation, write the new framing at the top and move the prior framing to a `### Prior framing (superseded YYYY-MM-DD)` subsection below.

**Risks / Killed / Reconciliations / Next Steps:** Merge by deduping. If a risk has been addressed, move it to Locked Decisions with a note.

**Change Log:** Append a new line at the bottom describing what this run changed. Single sentence. No fluff.

---

## What to Extract from the Conversation

Be precise. Don't paraphrase loosely. Lift the PM's actual words for decisions where possible.

**Locked decision signals:**
- PM says "yes", "agreed", "lock that", "we will [do X]", "[X] is the call", "go with [X]".
- PM accepts a recommendation without pushback after I named it.
- PM corrects a prior decision and states the new one.

**Open question signals:**
- PM says "open question", "TBD", "decide later", "mark it as open", "not sure yet".
- I gave a recommendation that the PM hasn't accepted or rejected.
- A question was raised but no answer was given.

**Risk signals:**
- PM says "we'll need to figure out", "this could break", "watch for", "mention it in the PRD".
- Problem flagged in critique that wasn't fully resolved by a decision.

**Killed signals:**
- PM says "we are removing X", "kill X", "stop X", "don't ship X".
- Direction reversal where a prior plan is now invalid.

---

## Critic Pass (run before save)

Per CLAUDE.md writing rules, before saving the doc:

- [ ] **Every locked decision is grounded in the conversation.** If I can't point to where the PM agreed, it goes in Open Questions, not Locked Decisions.
- [ ] **No invented decisions.** If the PM didn't say it, it's not locked.
- [ ] **Plain English.** No consultant-speak. No "leverage", "synergize", "ladder up".
- [ ] **Assumptions marked.** Any inference about PM intent labeled [ASSUMPTION].
- [ ] **Superseded items preserved.** Nothing deleted; old framings and decisions remain in the file with `(superseded YYYY-MM-DD)`.
- [ ] **Change Log entry is honest.** Describes what actually changed, not what was discussed.

---

## How to Save

1. Confirm the project folder exists at `content/13-projects/<slug>/`. Create if missing.
2. Read the existing `<slug>_working-doc.md` if present.
3. Write the merged version to `content/13-projects/<slug>/<slug>_working-doc.md`.
4. Run the per-turn backup (CLAUDE.md mandatory rule):
   ```bash
   tar -czf /Users/avirangrisaro/Documents/amp-backups/content-$(date +%Y%m%d-%H%M%S).tar.gz \
     --exclude='content/12-codebase/snapshots' \
     --exclude='*/12-codebase/snapshots' \
     -C /Users/avirang/Documents/amp content product-os-server/data/users \
     && cp /Users/avirangrisaro/Documents/amp-backups/content-*.tar.gz \
        "/Users/avirang/Library/CloudStorage/GoogleDrive-avirang@ampfit.com/My Drive/amp-content-backups/"
   ```
5. Return to the PM:
   - File path (absolute).
   - 1-paragraph summary: what was added, what was updated, what was moved to Locked Decisions, what's still open.

---

## Output to PM

After saving, respond with this exact shape:

```
Updated: content/13-projects/<slug>/<slug>_working-doc.md

Added: <N> locked decisions, <N> open questions, <N> risks.
Updated: <list of changed sections>.
Resolved → Locked: <questions that became decisions this run>.
Still open: <count> questions awaiting your call.

Next decision blocking progress: <the one question that matters most right now>.
```

Keep it under 8 lines. The PM reads the doc for detail; this summary is just the navigation.

---

## Pro Tips

### 1. Don't pollute Locked Decisions with weak signals
If the PM said "probably" or "lean toward", that's an Open Question with a recommended default — not a Locked Decision. Be strict.

### 2. Preserve the audit trail
Working docs become the institutional memory of why a PRD looks the way it does. Don't delete superseded framing or reversed decisions. Annotate them.

### 3. One file per project, not per conversation
If multiple chats touch the same project, they all update the same working doc. The Change Log shows the chronology.

### 4. Don't promote to PRD prematurely
When the PM says "draft the PRD" — that's `/prd-draft`, which reads this working doc as a primary input. Until then, keep iterating here.

### 5. Flag reconciliations honestly
If this direction kills something that's mid-build elsewhere (e.g., another PRD in flight), put it in the Reconciliations Needed section with the file path. Don't quietly let the workspace contradict itself.

---

## Output Quality Self-Check

Before presenting output, verify:

- [ ] **File saved to correct location** — `content/13-projects/<slug>/<slug>_working-doc.md`.
- [ ] **Merge preserved prior content** — nothing deleted; superseded items annotated.
- [ ] **Locked Decisions are grounded** — every entry traces to PM agreement in the conversation.
- [ ] **Open Questions have recommended defaults** — not just questions, but my recommended answer + what's blocking the call.
- [ ] **Change Log appended** — one honest sentence describing this run's changes.
- [ ] **Backup ran** — per-turn backup executed per CLAUDE.md rule.
- [ ] **Summary to PM is ≤8 lines** — points at the doc for detail; doesn't restate it.
