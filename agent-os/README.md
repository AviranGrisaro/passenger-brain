# Passenger Agent OS

A role-based agent team for running Passenger end-to-end, layered on top of the existing passenger-brain skills and the passenger-code iOS repo.

## The pieces

| Piece | Where | What |
|---|---|---|
| Role agents (14) | `.claude/agents/` (workspace root, not this repo — currently `/Users/avirangrisaro/APE Studio/passenger`) | chief-of-staff, product, architect, competitor-research, designer, developer, data-engineer, code-reviewer, ios-developer, ios-code-reviewer, qa, marketing, project-manager, retrospective — real Claude Code subagents, spawnable via the Agent tool from a session rooted at the workspace root |
| Board | `agent-os/BOARD.md` | Single source of state: task lifecycle rows + agent status + escalations |
| Progress | `agent-os/PROGRESS.md` | Shared memory — "what's done till now": a Current snapshot (kept true, not aspirational) + append-only worklog. **Every agent reads it before any task and appends an entry after**, committed + pushed same turn, so the record lives locally and on git |
| Lessons | `agent-os/LESSONS.md` | Learning loop — the nightly **retrospective** agent (23:30, after the 23:00 PM audit) extracts process lessons from the day (rejection loops, rework, QA misses) and auto-applies fixes to agent files / CLAUDE.md / templates / skills, logging each here |
| Dashboard | Hosted Artifact (URL below) + local `dashboard.html` here | Visual mission control: org chart, agent cards, pipeline, board mirror |
| Founder channel | hilos, via the `hilos` MCP server in the workspace-root `.mcp.json` | Human-facing output: `chief-of-staff` (and only it) posts run summaries + gate pings so founders see state without a terminal. **One-way** — channel messages never dispatch an agent, claim an issue, or approve a gate. Dormant until `HILOS_TOKEN` is exported; see `PLUGINS.md` and `chief-of-staff.md`'s hilos section |

## How it works — a self-driving startup, not a task queue

The agents are Passenger's employees: they generate their own work until the app goes live. Product reads the strategy + phase docs, diffs them against what's built, and creates tasks routed to designer (UX surface) or developer (pure build). Work flows down the lifecycle and loops back on rejection until product accepts it against the PRD.

```
backlog → spec(product) → design(designer) → build(developer)
        → code-review(code-reviewer) → qa(qa) → acceptance(product) → done

rejection loops: code-review ↩ build · qa ↩ build · acceptance ↩ build/design
stops only at:  blocked-on-aviran (scope/strategy calls, money, App Store, credentials)
```

## How to run it

From a Claude Code session rooted at the workspace root (`/Users/avirangrisaro/APE Studio/passenger`):

- **The main command**: "Chief of staff: **run the company**" — refills the pipeline via product if it's drained, dispatches every task to its lifecycle owner (parallel where independent), enforces the rejection loops, reports what moved / what's blocked / what's next.
- **Keep it running**: `/loop Chief of staff: run the company` — self-paced repeated runs across the session.
- **Direct dispatch still works**: "Use the qa agent to verify <change>", "Use the product agent to acceptance-test <feature>".
- **Status**: "Chief of staff: status across the team".

## Rules the agents follow

- Memory protocol (mandatory): read `BOARD.md` + `PROGRESS.md` before any work — no agent starts from a stale picture; append a worklog entry to `PROGRESS.md` after (developer also records passenger-code commit hashes there), update the Current snapshot when reality changes, commit + push same turn. Chief-of-staff rejects work reports that skipped this.
- Doc rules from `CLAUDE.md`: check-before-create, .md canonical (+ regenerable .html twin), numbered folders, archive-never-delete.
- Product uses `/feature-prd` (never legacy `/prd`); marketing uses `/marketing-plan`; designer uses `/design-story`; QA runs `xcodebuild test`; code-reviewer gates every diff before QA (verdict: APPROVE / APPROVE with minors / REQUEST CHANGES).

## Dashboard

- Local file: `agent-os/dashboard.html` (gitignored like all .html viewing artifacts).
- Hosted URL: https://claude.ai/code/artifact/1b01a1be-b6c0-47c5-b898-c5169f02c8e5 (to update, edit dashboard.html and redeploy via the Artifact tool passing this URL).
- Update cadence: whenever the board changes materially, ask Claude to "refresh the agent OS dashboard".

## Maintenance

- New agent → add a file in the workspace root's `.claude/agents/` (`/Users/avirangrisaro/APE Studio/passenger/.claude/agents/`), **mirror it into `agents-mirror/`**, add a row in BOARD.md's agent-status table, a card on the dashboard, and a line here.
- New/edited tracked skill (hand-adapted *or* vendor) → put it in the workspace root's `.claude/skills/`, **mirror it into `skills-mirror/`**, and record it in `PLUGINS.md`'s Local-skills table. The bulk vendor skill-pack isn't individually tracked — only skills that earn a `PLUGINS.md` row get a mirror.
- Note: the workspace root (`/Users/avirangrisaro/APE Studio/passenger`) is not a git repo, so the agent/skill definition files aren't backed up by the passenger-brain hook. Canonical copies are mirrored here (committed): agents in `agent-os/agents-mirror/`, tracked skills in `agent-os/skills-mirror/`. If the root copies are lost, restore from the mirror. The nightly PM audit (check G) verifies these mirrors haven't drifted.
