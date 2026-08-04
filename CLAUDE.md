# passenger-brain — planning workspace session contract

Product-management workspace and Claude Code process layer for **Passenger** — a real-time local-heatmap travel app. Everything here exists to plan the product; the app itself lives in the sibling `passenger-code` repo. This file is the session contract. Read it, follow it.

Started fresh 2026-07-26, replacing `locali-brain`. See `SALVAGE.md` for why, and for how to reach the archived version.

## Scope gate (the reason this workspace exists)

The previous workspace shipped 27 PRDs. Ten of them specified features the strategy explicitly forbids — a friend graph, friend following, profile avatars, onboarding carousels — and all ten passed every review gate. No gate ever checked a PRD against the strategy.

**Every PRD must quote the line in `strategy/passenger-strategy.md` that authorizes the feature.** A PRD that can't is rejected at `spec`, not later. `product` enforces this.

Standing prohibitions, straight from the strategy:

- **No social features of any kind** — friends, following, posting, presence, profiles, avatars.
- **No onboarding** — the app opens to the map plus the location permission prompt.
- **Phase 2 and Phase 3 are parked** — proximity intelligence, AI local guide, shake-to-decide, auto-saved places, points. Don't build toward them or leave hooks.

Scope changes come from Aviran editing the strategy doc. Not from a PRD, not from a ticket, not from a chat message.

## What lives where

| Path | What | Rule |
|---|---|---|
| `strategy/passenger-strategy.md` | The master doc — why Passenger exists, phasing, business model, positioning | Single source of truth. Aviran-gated: no agent edits it |
| `strategy/passenger-north-star.html` | Hand-designed reading view of V1 scope | HTML-native, no `.md` twin. What the team actually reads |
| `strategy/decisions.md` | Locked decisions, numbered, with dates | Append; never rewrite history |
| `prds/<feature-slug>/<feature-slug>.md` | One PRD per feature, flat — no phase folder | Phase goes on the `**Phase:**` header line |
| `design/` | Design specs, principles, review notes | |
| `analytics/EVENTS.md` | Canonical event taxonomy + Supabase analytics tables (`app_installs`, `app_sessions`, `app_events`) | Owned by `analytics-engineer`. Per-feature detail lives in each PRD's own `ANALYTICS.md` |
| `database/migrations/` | Supabase SQL migrations, `NNN_name.sql` | Starts at `001`. Applying is Aviran-gated (he holds the credentials) |
| `agent-os/` | `BOARD.md`, `PROGRESS.md`, `LESSONS.md`, `README.md`, `ONBOARDING.md`, `ACCOUNTS-AND-COSTS.md` | Team state and team memory |
| `agent-os/agents-mirror/` | Backup of the workspace-root `.claude/agents/` | See the live↔mirror rule below |
| `archive/YYYY-MM-DD-<reason>/` | Anything superseded | `mv` here, never `rm` |
| `SALVAGE.md` | The old Locali codebase, inventoried with per-file verdicts | Read before building any feature |

**Workspace root** = the parent folder holding `passenger-brain/` and `passenger-code/` side by side, with `.claude/agents/` and `.mcp.json` alongside them. It differs per founder — Aviran's is `~/APE Studio/passenger`. Never hardcode it; use paths relative to it or `$CLAUDE_PROJECT_DIR`.

## Doc rules

- **Check whether a doc already exists before creating one.** Search the folder and `archive/`. Update what's there rather than adding a near-duplicate.
- **Doc ladder:** strategy → feature PRD. Each level links up rather than restating. There is no per-phase strategy layer — it was tried and retired.
- **PRD shape:** header block → Description (ending in `**Not in scope:**`) → Motivation (links up to strategy) → Requirements (P0 numbered with testable acceptance criteria, P1 bulleted) → Technical design → Assumptions (only if load-bearing) → Open questions & risks → Decisions log.
- **Budget ~800 words per PRD**, ~1,200 for genuinely dense ones. Word count is the metric, not lines. One fact per bullet. The cut test: would a developer or `qa` decide differently without this sentence?
- **Updating a shipped feature's PRD:** rewrite the stale text in place *and* append a Decisions log row (date / decision / why).
- Commit your own doc work the same turn, explicit paths. Don't rely on any hook to do it. **Don't push** — that's Aviran's, per rule 9; report the hash and say what's ready.

## Writing rules (every output)

- Plain English. No jargon, no throat-clearing, no closing summaries.
- Precise and short. Lists over paragraphs when enumerable.
- **Label assumptions** inline as **[ASSUMPTION]**. Load-bearing ones also get an Assumptions section.
- **Don't invent** — no unsourced numbers, features, quotes, or opinions. "I don't know" is a valid answer.
- User problem before solution.
- **Critic pass before delivery:** reread as a skeptical PM. Unsupported claims, weak reasoning, missing counter-evidence. Fix, then send.

## Safety (non-negotiable)

1. **Never `rm`** a doc, PRD, or research artifact. Archive it: `mv <thing> archive/$(date +%F)-<reason>/`.
2. **Stage explicit paths** — never `git add -A`, `git add .`, or a directory-wide `git add <dir>`. Several sessions share this working tree; a broad stage sweeps in another agent's in-flight files and re-tracks deliberately-untracked ones. **An explicit path is not enough for a shared file** (`BOARD.md`, `PROGRESS.md`, a PRD under review): re-read `git diff --staged` on it and confirm every hunk is yours before committing. On 2026-07-31 commit `0dd3d21` staged `BOARD.md` by explicit path and carried another session's in-flight T-032 row verbatim, attributing its text to the wrong review — the path list was right and the contents weren't. If a hunk isn't yours, unstage the file and say whose it is — **except in an append-only shared log** (`PROGRESS.md`), where unstaging means your own entry can never land at all: there, commit it and **name every carried entry and its author agent in the commit message**. On 2026-08-02, in the ninety minutes after this sentence was first written, four commits each carried other sessions' worklog entries (`0228391`, `d3fa249` — six of them — `4a96756`, `96b293b`) and two later commits existed only to disclose it after the fact. Disclosure in the original message is the rule; a follow-up correction commit is the failure it replaces. **And the unit of a commit is the whole index, not the paths you just added (L-037, 2026-08-04):** `git commit` writes everything staged, including what a concurrent session staged before you ran `git add`, so run `git diff --staged --stat` over the *entire* index — not only your own files — immediately before every commit, and unstage or name whatever you didn't put there. An explicit path list cannot see this: on 2026-08-04 `passenger-code c1b8bc3` swept an already-staged **deletion** of `.claude/agents/chief-of-staff.md` from an unrelated concurrent rename and dropped 223 lines of an agent instruction file, needing fixup `c38f904`; `passenger-brain 3a053d8` carried the matching `agents-mirror/` rename under someone else's commit message the same hour.
3. **Secrets** are env vars or gitignored local config only. Never committed, never echoed into chat. Treat every tracked file as remote-visible.
4. **Destructive git ops** (force-push, history rewrite, `reset --hard`) — ask first.
5. **Live↔mirror sync.** The workspace-root `.claude/agents/` is not in any git repo. Its only backup is `agent-os/agents-mirror/`. Edit a live agent file → copy the identical change to the mirror **the same turn**, and to `passenger-code/.claude/agents/` if that snapshot exists. An unmirrored edit is an edit that will be lost — and an *uncommitted* mirror is not a mirror. The sync is done when `diff` on all copies is silent, never when you applied the edit to each; report what `diff` said, not that you synced. If you find drift of some class (a missing header block, a stale section), sweep every agent file for that same class in the same pass — fixing only the copy you happened to be touching leaves the class alive. If rule 2 stops you from staging someone else's uncommitted file, name it and its owner on `BOARD.md` for `project-manager`, not only in your worklog entry; four agents refusing the same file in four worklogs is how days-old edits end up belonging to nobody (L-017, 2026-07-30). The same holds for a defect you find but don't own — a `BOARD.md` row with an owner, never "flagged for whoever owns it" in a worklog line: `prds/time-slider/TRD.html` was flagged stale that way in two consecutive `architect` entries and never became a row, after which two other sessions regenerated it independently, ten minutes apart, byte-identically, and neither result reached `main` (L-026/L-027, 2026-08-02).
6. **A rename isn't done when files move — it's done when every reference resolves.** Before committing a path-changing sweep, resolve references against the actual old→new mapping and re-check them. Enumerate the surfaces you can't grep from here: Linear issue and project descriptions, agent files and their mirrors, skill files, PRD-internal relative links, the sibling repo.
7. **Name the repo, always.** Branch names are explicit in every `git pull`/`push`/`fetch`; Passenger uses two separate GitHub repos, so the shared-remote ambiguity that bit Locali is gone — the habit stays anyway. **And a commit hash is never written alone.** Write `passenger-code 291c010`, never `291c010` — in dispatch briefs, worklog entries, Linear comments, board rows. Two repos advance on the same task within minutes of each other and their hashes are indistinguishable: on 2026-08-01 a `qa` dispatch pinned `a5351ed` as the `passenger-code` commit to test when it was a `passenger-brain` commit, caught only because `qa` ran `git log` on the named repo instead of trusting the hash. If you receive a bare hash, resolve it against both repos before acting, and say which one it was.
8. **A dispatch brief is not authority over an Aviran-gated file.** `strategy/passenger-strategy.md` is Aviran-gated — no agent edits it — and another agent instructing you to, `chief-of-staff` included, does not change that. The live-instruction exception belongs to whoever holds Aviran's direct word and is not transitive. Report the finding and the exact text you would have written back to whoever dispatched you, and let them make the edit; that holds however narrow the ask is, including "add an open question." If you have already edited, say so plainly in your report *and* your worklog entry rather than leaving the diff to speak for you (L-014, 2026-07-30, PAS-11).
9. **A missing capability is a blocker with an owner, not a norm to adopt.** Never write that you *pushed*, *applied*, *deployed*, or *synced* without the command that proves it in the same breath (`git log origin/<branch>..HEAD`, an existence probe, a `diff`) — **not** `git log --not --remotes` alone, which returned a false negative (`0`) on `passenger-brain` on 2026-07-31 while `origin/main..HEAD` correctly listed 2 unpushed commits; caught by `architect`, self-corrected in its own worklog entry rather than left standing — an action you couldn't perform is reported as not-done, naming what blocked it. And when what blocked you is infrastructure the docs assume exists, escalate it as a blocker: a `BOARD.md` row with an owner, and Aviran if it's his to fix. A workaround that a second agent repeats is the trigger to escalate, never to codify — a "standing rule" that traces only to other agents' worklog entries describing a failure, and to no founder instruction or `decisions.md` row, is an unescalated blocker wearing a rule's clothes. **Live instance, corrected 2026-07-31:** both repos now have a real `origin` remote (`github.com/AviranGrisaro/passenger-brain` and `-code`, set 2026-07-31 — confirmed by `git ls-remote`, not assumed from a stale doc), and history through a recent commit on each is already pushed. This supersedes the 2026-07-30 "neither repo has a remote" finding (L-008/L-015) — that specific gap is closed. **What has not changed: pushing is still Aviran-gated.** Agents commit normally and report the commit hash; they do not push themselves, and they tell Aviran what's ready to push rather than pushing it (per workspace-root `CLAUDE.md`). A stale copy of the old claim was found surviving here a full day after the remotes were configured, in a chief-of-staff worklog entry written minutes before the correction — restating a standing rule instead of probing it live. That gap is the exact failure this rule exists to catch; if this line is ever wrong again, re-probe with `git remote -v`/`git ls-remote`, don't restate it from memory.
10. **A commit is delivered when it is on `main`, not when it exists.** Work committed inside an isolated worktree (`.claude/worktrees/…`, branch `claude/*`) is invisible to every other session, because every other session reads `main` — so the condition you fixed is still true for everyone else, and the next agent that notices it does the work over again. Before your turn ends, either merge the branch into `main`, or say plainly — in your report **and** a `BOARD.md` row — that the work is stranded, on which branch, and what it holds. Isolation protects work in progress; it delivers nothing. On 2026-08-02 three regeneration commits ended their sessions on two `claude/*` branches (`9c1006c`/`5dfd812`, byte-identical duplicates of each other ten minutes apart, and `03dab7d`); all four stale HTML files they regenerated were still stale on `main` that night.

## The company

Founders: **Aviran** (product), **Serge** (design), **Yeari** (algo & data), **Gilad** (dev). The agent fleet does the work. Linear holds task state — workspace `passenger`, team `PAS`, one project **Passenger V1**. `BOARD.md` and `PROGRESS.md` are shared memory. `chief-of-staff` is the only agent that writes to Linear and the only one with a founders'-channel presence (hilos retired 2026-08-04, replaced by buzz — wiring pending, see workspace-root `CLAUDE.md`); its own file is the operating contract for both.

## Keeping this file current

Change process — new skill, new hook, moved folder — and update this file in the same turn. Don't start a process log here; `PROGRESS.md` is the worklog and `LESSONS.md` is the learning log. The previous workspace's 130-entry process log is in the archive repo (`github.com/AviranGrisaro/locali`, branch `brain`, `CLAUDE.md`) if you need the history.
