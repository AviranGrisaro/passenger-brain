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
- Commit and push your own doc work the same turn. Don't rely on any hook to do it.

## Writing rules (every output)

- Plain English. No jargon, no throat-clearing, no closing summaries.
- Precise and short. Lists over paragraphs when enumerable.
- **Label assumptions** inline as **[ASSUMPTION]**. Load-bearing ones also get an Assumptions section.
- **Don't invent** — no unsourced numbers, features, quotes, or opinions. "I don't know" is a valid answer.
- User problem before solution.
- **Critic pass before delivery:** reread as a skeptical PM. Unsupported claims, weak reasoning, missing counter-evidence. Fix, then send.

## Safety (non-negotiable)

1. **Never `rm`** a doc, PRD, or research artifact. Archive it: `mv <thing> archive/$(date +%F)-<reason>/`.
2. **Stage explicit paths** — never `git add -A`, `git add .`, or a directory-wide `git add <dir>`. Several sessions share this working tree; a broad stage sweeps in another agent's in-flight files and re-tracks deliberately-untracked ones.
3. **Secrets** are env vars or gitignored local config only. Never committed, never echoed into chat. Treat every tracked file as remote-visible.
4. **Destructive git ops** (force-push, history rewrite, `reset --hard`) — ask first.
5. **Live↔mirror sync.** The workspace-root `.claude/agents/` is not in any git repo. Its only backup is `agent-os/agents-mirror/`. Edit a live agent file → copy the identical change to the mirror **the same turn**, and to `passenger-code/.claude/agents/` if that snapshot exists. An unmirrored edit is an edit that will be lost.
6. **A rename isn't done when files move — it's done when every reference resolves.** Before committing a path-changing sweep, resolve references against the actual old→new mapping and re-check them. Enumerate the surfaces you can't grep from here: Linear issue and project descriptions, agent files and their mirrors, skill files, PRD-internal relative links, the sibling repo.
7. **Branch names are explicit** in every `git pull`/`push`/`fetch`. Passenger uses two separate GitHub repos, so the shared-remote ambiguity that bit Locali is gone — the habit stays anyway.

## The company

Founders: **Aviran** (product), **Serge** (design), **Yeari** (algo & data), **Gilad** (dev). The agent fleet does the work. Linear holds task state — workspace `passenger`, team `PAS`, one project **Passenger V1**. `BOARD.md` and `PROGRESS.md` are shared memory. `chief-of-staff` is the only agent that writes to Linear and the only one with a hilos presence; its own file is the operating contract for both.

## Keeping this file current

Change process — new skill, new hook, moved folder — and update this file in the same turn. Don't start a process log here; `PROGRESS.md` is the worklog and `LESSONS.md` is the learning log. The previous workspace's 130-entry process log is in the archive repo (`github.com/AviranGrisaro/locali`, branch `brain`, `CLAUDE.md`) if you need the history.
