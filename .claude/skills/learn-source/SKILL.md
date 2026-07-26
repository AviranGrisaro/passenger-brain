---
name: learn-source
description: Distill a large external source (book, paper, research, long article) into a reusable 1-page cheat-sheet in my-brain's 02-frameworks/, so /prd and other skills can apply its principles without ever loading the whole source into context. Use when the user uploads or points to a book/paper/research/article and wants it "added to my brain", "learned", "ingested", or "digested". Triggers include "/learn-source", "learn this book", "ingest this paper", "add this to my frameworks", "digest this source".
user-invocable: true
allowed-tools: Bash, Read, Write, Glob, Grep, Task
argument-hint: <path-to-source-file>
---

# Learn Source → Cheat-Sheet

Turn a big external source (book / paper / research / long article) into a small, faithful cheat-sheet stored in `02-frameworks/`, so the PRD writer and other skills can use its wisdom **without loading the whole source** (which would wreck the context window).

**Architecture — this is the whole point:** this skill is the orchestrator. The heavy reading happens inside the `source-distiller` sub-agent, which reads the full source in its OWN context window and returns only a short summary. The big source never enters this conversation.

```
raw source (14-references/)  ->  source-distiller sub-agent  ->  cheat-sheet (02-frameworks/)  ->  /prd reads it
```

## Convention (matches the my-brain layout)

- **Raw sources** live in `/Users/avirangrisaro/Documents/my-brain/14-references/` (the big files).
- **Distilled cheat-sheets** live in `/Users/avirangrisaro/Documents/my-brain/02-frameworks/` (3–8KB each).
- Every cheat-sheet is registered in `/Users/avirangrisaro/Documents/my-brain/02-frameworks/INDEX.md`.

## Workflow

### Step 1: Resolve the source

Get the source path from `$ARGUMENTS`. If none was given, ask the user which file, and check likely spots:
```bash
ls -la "/Users/avirangrisaro/Documents/my-brain/14-references/" 2>/dev/null
ls -lat "/Users/avirang/Downloads/" 2>/dev/null | head -20
```
Confirm the file exists. If it's a book/paper that lives outside `14-references/`, offer to copy it in first (raw sources belong there):
```bash
cp "<source>" "/Users/avirangrisaro/Documents/my-brain/14-references/"
```

### Step 2: Choose title + output path

Pick a clear title and a kebab-case slug. Output path:
`/Users/avirangrisaro/Documents/my-brain/02-frameworks/<slug>.md`
If a cheat-sheet with that slug already exists, ask whether to update it or pick a new name.

### Step 3: Distill (sub-agent — the context firewall)

Dispatch the **`source-distiller`** sub-agent with the Task tool:
- `subagent_type: "source-distiller"`
- prompt: the **source path** and the **output path**, plus a reminder to follow the house format and return only a short summary.

If `source-distiller` is not available as an agent type (e.g. just created this session), fall back to `subagent_type: "general-purpose"` and paste the distiller's instructions from `~/.claude/agents/source-distiller.md` into the prompt.

**Do NOT read the raw source yourself** — that would defeat the purpose. Let the sub-agent do it.

### Step 4: Review with the user (human check)

When the sub-agent returns, READ the produced cheat-sheet and show it to the user. Ask:
> "Here's the distilled cheat-sheet. Does this match the source? Want me to adjust anything before I file it?"

Make any requested edits.

### Step 5: Register it in the index

Add a row to `/Users/avirangrisaro/Documents/my-brain/02-frameworks/INDEX.md`:
`| [<slug>.md](<slug>.md) | <when to use> | <which skills it feeds> | <source> |`

### Step 6: Backup (workspace policy)

Per the my-brain policy, files changed → back up locally:
```bash
tar -czf "/Users/avirangrisaro/Documents/amp-backups/my-brain-$(date +%Y%m%d-%H%M%S).tgz" -C "/Users/avirangrisaro/Documents" my-brain
```
(Drive backup, if wanted, via the user's existing sync — ask before uploading externally.)

### Step 7: Report

Tell the user:
- what was learned + cheat-sheet path
- the 5 headline takeaways (from the sub-agent)
- which skills will now use it (e.g. `/prd` reads it during context-gathering)
- suggested next step: "Run `/prd <feature>` and it'll apply this automatically."

## Notes

- **One source → one cheat-sheet.** For an anthology or a source covering several distinct frameworks, produce more than one — dispatch the sub-agent once per framework.
- **Good sources for this skill:** product, strategy, psychology, user behavior, research, design, growth (e.g. *The Mom Test*, *Hooked*, *Inspired*, JTBD papers, behavioral-economics texts).
- **Format reference:** the sibling files in `02-frameworks/` (e.g. `jtbd-canvas.md`) are the gold standard for tone and length.
