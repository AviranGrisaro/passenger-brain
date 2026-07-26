---
name: weekly-trending
description: Scan GitHub Trending and surface only the repos relevant to what Passenger is actively building right now. Use weekly, or whenever Aviran asks "what's trending", "anything on GitHub trending worth a look", or wants a GitHub Trending check.
disable-model-invocation: false
user-invocable: true
---

# /weekly-trending — GitHub Trending, filtered by what we're actually building

GitHub Trending shows what the whole world is excited about. That's mostly noise for any one project. This skill closes the loop the other way: read Trending, then keep only what's relevant to Passenger's *current* work, and say why.

Don't produce a bookmark list. Bookmarks don't get revisited — a short, opinionated briefing does.

## Instructions

1. **Read GitHub Trending.**
   Fetch `https://github.com/trending` (WebFetch). If it's thin, also check `https://github.com/trending?since=weekly` for a wider weekly window. Pull repo name, one-line description, primary language, and stars-this-week for each entry.

2. **Build "what we're working on right now."** Pull from, in order:
   - `strategy/passenger-strategy.md` — phasing table, to know which phase is active, its strategic question, and its dev-architecture notes (the per-phase `phase-strategy.md` layer is retired — see `CLAUDE.md`'s Doc hierarchy — don't look for one).
   - `agent-os/PROGRESS.md` — current snapshot + recent worklog entries (what the agent team actually touched lately).
   - `git log --since="7 days ago" --oneline` in both `passenger-code` and `passenger-brain` — real recent activity, not stated intent.
   Don't ask Aviran to restate this — derive it from the repo. Only ask if the phase docs are genuinely silent on what's active.

3. **Rank relevance, don't summarize everything.** Score each trending repo against the context from step 2 (matches a technology Passenger uses or is evaluating, solves a problem an active feature/PRD names, unblocks something in the current phase's dev-architecture plan). Discard anything with no real tie — "cool AI thing" is not a tie.

4. **Check `strategy/weekly-trending-log.md` for repeats.** Don't resurface a repo already logged there in the last 6 weeks unless something material changed (major version, newly relevant to a feature that didn't exist before).

5. **Output the top 3 (fewer is fine, never pad to 3).** For each: repo name + link, one line on what it does, one line on *why it matters to Passenger right now* (name the specific phase/feature/PRD it connects to). If genuinely nothing is relevant this week, say so in one line — don't force matches.

6. **Log it.** Append an entry to `strategy/weekly-trending-log.md` (create it from the template below if it doesn't exist yet), newest first. Commit + push in the same turn per the repo's doc output rule (`CLAUDE.md`).

7. **Post it to hilos `#weekly-trending`** (channel ID `d81abef5-6289-485a-be16-67ceeef42258`) via `mcp__hilos__post_message`. One message per week, all three repos in it. Per repo, exactly three short lines:

   ```
   **[owner/repo](https://github.com/owner/repo)**
   <what it is — one line, under 15 words>
   Why us: <the specific active task/PRD/agent it ties to — one line>
   ```

   Rules:
   - **Repo link is mandatory** and must be the real `https://github.com/owner/repo` URL. No link, no post.
   - Keep it tight. The log file carries the long reasoning; the channel gets the short form.
   - Nothing relevant this week → post one line saying so. Don't skip the post; silence reads as "the schedule broke."
   - GitHub Trending unreachable → say that in the channel instead of posting repos. Never fabricate.
   - **Close the post with the intake line**, verbatim: `To look into one of these, reply @chief in this thread naming the repo — I'll open a backlog issue on my next run.`
   - **Never file a Linear issue off this skill on your own.** The skill surfaces; a founder decides. A ticket exists only when a founder asks for one — protocol in `chief-of-staff.md` § "`weekly-trending` — the adopt request".
   - If the `hilos` MCP tools aren't in the toolset, say the bridge isn't connected and skip the post — never claim you posted.

8. **Scheduling.** Already on a schedule: the `weekly-trending` scheduled task fires Sundays at 09:00 local. Don't suggest setting one up; if it's clearly not firing, say so rather than creating a duplicate.

## Log file template

If `strategy/weekly-trending-log.md` doesn't exist, create it as:

```markdown
# Weekly GitHub Trending log

Repos surfaced by `/weekly-trending` as relevant to active Passenger work. Newest first. Not a bookmark dump — only entries that were actually judged relevant when logged.

## Format

\`\`\`
## YYYY-MM-DD
- **[repo-name](url)** — <one-line what it does>. Relevant because: <tie to active phase/feature/PRD>.
\`\`\`

## Entries

(none yet)
```

## Notes

- This is a research/signal skill, not a build trigger. Never install, clone, or add a dependency based on what it surfaces — flag it in the log and let PRD/roadmap triage decide, same as `feature-inspiration.md`.
- If GitHub Trending is unreachable, say so and stop — don't fabricate trending repos.
