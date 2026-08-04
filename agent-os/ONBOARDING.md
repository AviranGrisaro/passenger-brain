# Multi-Founder Onboarding — Passenger Agent OS

The agent OS (`README.md` in this folder) was built for one operator. This doc extends it to four founders working async, meeting at most once a week, each running their own Claude Code session against the same brain. Read this once per founder before your first session; re-read the "Every session" section until it's habit.

## The four founders and their domains

| Founder | Domain | Maps to |
|---|---|---|
| Aviran | Product | drives `product`, `chief-of-staff`; one half of the `design-review` gate; final `aviran-review` sign-off |
| Serge | Design | drives `designer`; the other half of the `design-review` gate |
| Yeari | Algo & Data | drives `data-engineer` — the heatmap/presence algorithm and the data-sourcing/ingestion pipeline |
| Gilad | Dev | drives `developer` (backend) and `ios-developer` (client) — the build side |

Nothing stops any founder from running any role through `chief-of-staff` — this table is "who naturally owns what," not a hard lock. The one real gate right now is `design-review`, and it needs both Serge and Aviran specifically (see below) — everything else in the pipeline runs automatically, no other human approval required at this stage.

### What each founder actually does

**Aviran — Product.** Decides what gets built next (drives `product`, which reads strategy against what's already shipped and generates the next tasks) and runs the day-to-day operator loop (`chief-of-staff`, "run the company"). Three things only Aviran can do right now: half of the `design-review` gate (the product-fit read on a mockup, alongside Serge's craft read); the final `aviran-review` sign-off — nothing reaches `done` without it; and holding the actual Supabase DB credentials, so every migration `developer`/`data-engineer` write still needs Aviran to apply it by hand. Everything labeled `blocked-on-aviran` — scope/strategy calls, money, App Store and other external accounts, credentials, destructive git ops — is his to clear. The nightly/weekly automation also runs on his Claude Code, his responsibility (see Infrastructure below).

**Serge — Design.** Owns UX and visual craft (drives `designer` — flows, specs, Figma mockups) and is the other half of `design-review`: no code gets written against a design he hasn't personally looked at. Where `designer`'s output needs a taste call the spec doesn't settle — visual language, interaction pattern, whether something reads as "on brand" — that's Serge's judgment to make, not the agent's.

**Yeari — Algo & Data.** Owns the thing that actually makes Passenger a heatmap app and not just a map with pins: drives `data-engineer`, which owns the presence/heatmap algorithm (aggregation, decay, the privacy floor) and the data-sourcing/ingestion pipeline that feeds it (Phase 3's "data-sourcing automation"). Any `[ASSUMPTION]`-tagged call `data-engineer` surfaces about how the algorithm should actually behave, or whether a data source is good enough to trust, is Yeari's to resolve. No dedicated Linear gate exists for this domain yet (unlike Serge/Aviran's `design-review`) — it ships through the normal Code Reviewer + QA gates like everything else.

**Gilad — Dev.** Owns getting features actually built: drives `developer` (backend — Supabase schema, RLS, migrations) and `ios-developer` (the Swift client). "In charge of the dev process" means Gilad is the point of escalation for engineering judgment calls — architecture pushback at `trd-review`, whether a TRD is right-sized, build-order tradeoffs — not that every commit currently waits on him. There's no PR-approval gate today (commits go straight to `main`, see "Every session" below); Gilad can add one later if the team decides it's needed.

## Why the existing design already mostly works

Two things make this safe for multiple people without a chat app in the middle:

1. **The brain is git, not a person's memory.** `passenger-brain` (`origin/brain`) and `passenger-code` (`origin/main`) are the only source of truth. Whoever pulls last sees everything everyone else committed — PRDs, TRDs, `BOARD.md`, `PROGRESS.md`, code.
2. **State lives in Linear, and only `chief` writes to it.** Task claiming is "read the issue's current state fresh at the moment of claiming, then immediately label `owner:<role>` and move to `In Progress`" (`.claude/agents/chief.md`, single-writer protocol). That rule doesn't know or care how many humans are behind it — it's what stops two of you from claiming the same issue.

**Two IDs, one task — don't let the mismatched numbers confuse you.** Every task has both a `T-xxx` id (its row in `BOARD.md`) and a `PAS-xxx` id (its Linear issue) — the same feature, two labels, for two different audiences. `T-xxx` is the fleet's own working memory: every agent (not just `chief-of-staff`) reads and writes `BOARD.md` directly as a plain-text file, no Linear API or auth needed, and it's where the dense technical narrative lives (design rejections, TRD findings, security fixes — the stuff that would be unreadable as a pile of Linear comments). `PAS-xxx` is the human-facing view — the thing you actually look at, with notifications and a UI you already know, and the one place `chief-of-staff` has a founders'-channel presence for `@chief` (buzz, pending setup — see "Communication" below). The numbers won't match (`T-031` might be `PAS-12`) — that's expected, not a bug; each `BOARD.md` row cites its Linear id in parentheses so you can always cross-reference. `chief-of-staff` keeps both in sync by hand as it processes work; it isn't automatic, so occasional drift is possible (this workspace has already caught and fixed a couple of instances — a stale board summary, a duplicate Linear issue). If something in Linear looks stale or off, checking `BOARD.md`/`PROGRESS.md` for the fuller picture — or just asking Chief to reconcile — is normal, not a sign anything is broken.

What's missing is founder-specific plumbing (repo access, local file mirrors, Linear seats) and a couple of habits that make the single-writer rule actually hold across four separate machines instead of one.

## One-time setup, per founder

1. **GitHub access** — get added as a collaborator on the repo backing both `passenger-brain` (branch `brain`) and `passenger-code` (branch `main`, same `origin`). Clone both locally as siblings, same as the existing layout.
2. **Claude Code** — install and authenticate the CLI. Each founder has their own personal account (Aviran's decision) — this isn't a shared login.
3. **Workspace-root `.claude/`** — `.claude/agents/` and `.claude/skills/` at the workspace root are **not git-tracked**; their only backup is the mirror committed inside `passenger-brain` (`agent-os/agents-mirror/`, `.../skills-mirror/`). After cloning, copy those mirrors into your local workspace root's `.claude/agents/` and `.claude/skills/` — otherwise your session has no role agents to spawn.
4. **Linear seat** — get added to the Linear workspace/project with the same access level as everyone else. Authorize the Linear MCP connector in your own session (`/mcp`, interactive) so your Claude Code can read/write issues.
5. **buzz — pending setup.** hilos retired 2026-08-04; the founders' channel is moving to buzz (Aviran's call) but the bridge isn't wired yet — no relay, no agent identity, no allowlist. Once it's live, join whatever channel replaces `#general` and get your buzz pubkey onto the allowlist in `chief.md`; ask Aviran to add it, same as before. Until then, `@chief` has no chat presence — reach Chief through a session or Linear.
6. **Xcode + the app's local config** — required for anyone running `ios-developer` or `qa` (`qa` runs `xcodebuild test`), optional if you only ever touch planning docs. Install Xcode, open it once, and check `xcode-select -p` points at it. Then create the two gitignored plists the app needs to launch — `Passenger/SupabaseConfig.plist` and `Passenger/GoogleSignInConfig.plist` — reading your own values off the Supabase and Google consoles once Aviran has added you. **Never paste those values into chat and never commit them**; if one genuinely has to move between people, use a password manager. Full detail in `passenger-code/README.md`.
7. **Figma access** — Serge needs edit on the shared file (`figma.com/design/45siCO8UGQivJEBhAqAH08/locali`, one page per feature); everyone else needs at least view, because `design-review` is literally "two people look at the mockup." The `designer` agent is under standing orders never to create a second file.
8. **Read before touching anything**: `passenger-brain/CLAUDE.md`, this folder's `README.md`, `BOARD.md`'s current state, and `PROGRESS.md`'s Current Snapshot section (short on purpose — the worklog below it is a recent window, not the full history; older entries are archived under `archive/`). This is the same "read before any task" rule every agent already follows; it applies to you too before your first manual action.

## Infrastructure & accounts: what's already there, what's missing

**Seats, costs, open money decisions, and the offboarding/key-rotation checklist live in `ACCOUNTS-AND-COSTS.md`** (this folder) — that's the single table of every external account and who still needs adding. What follows here is the architectural picture.

"Which server do we need" has a short answer for the app itself and one deliberate simplification for the automation. Broken down:

### Already provisioned — just needs the other founders added

- **Supabase** (Postgres, Auth, Realtime, Edge Functions) is the entire backend. It's already a hosted cloud project (linked — see `passenger-brain/supabase/.temp/project-ref`), not something you stand up. There is no separate app server: the iOS client talks to Supabase directly. **Gap:** only Aviran's account is a project member — add the other three as members of the Supabase org/project (pick roles: full Admin if they'll run migrations, a lighter role if not).
- **GitHub** (`github.com/AviranGrisaro/locali`) hosts both repos already. **Gap:** add the other three as collaborators with write access.
- **CI** — `passenger-code/.github/workflows/ios-build.yml` exists (added 2026-08-03, PAS-41) and triggers on every push/PR to `main`, on GitHub's free macOS runners. It's build-only (`CODE_SIGNING_ALLOWED=NO`, `xcodebuild build` against the `Passenger` scheme) — signing gets added later, see below. **Verification status: the file is committed and the equivalent `xcodebuild` command was confirmed to build successfully locally, but no agent session in this workspace can observe a live GitHub Actions run** (no `gh`/API access to this repo's Actions tab from here) — so "it's live and green" has not actually been watched happen on GitHub's infrastructure. First push/PR to `main` after this file lands is the real test; if you're the one who sees it run, update this line to say so plainly rather than leaving it as an assumption.
- **Linear** — covered above, just needs three more seats.

### Real gaps

- **Apple Developer Program account — doesn't exist yet.** `passenger-code/README.md` says Sign in with Apple is "deferred pending the Apple Developer Program account," and the roadmap's Phase 2 is literally "feature buildout + **App Store signing**" — this blocks that phase. For four founders, enroll as an **Organization** account (not an Individual tied to one person's Apple ID) — that's what lets more than one of you hold Admin/App Manager roles in App Store Connect, add TestFlight testers, and manage signing certs without funneling everything through one person's personal account. This is a paid ($99/yr), Aviran-gated decision (money + an org D-U-N-S lookup) — flagging it, not doing it.

### Decided, not open anymore

- **Claude Code access**: each founder runs their own personal Claude Code account. No shared login.
- **The nightly/weekly automation stays on Aviran's Claude Code, his responsibility.** `nightly-pm-audit`, `nightly-retro`, and `weekly-pm-rollup` are real, currently running (`mcp__scheduled-tasks`), living at `/Users/avirangrisaro/.claude/scheduled-tasks/`. The tool's actual contract: **"scheduled tasks run while this app is open; if closed when due, they run on next launch."** That means this is deliberately *not* a true always-on server — it's tied to Aviran's laptop having Claude Code open around 23:00–23:37 his local time, and a closed laptop just delays the run to next launch rather than losing it. Aviran chose to keep it this way rather than move to a dedicated always-on runner (a small VPS running the CLI headless on a system cron was the alternative, if this ever stops being good enough). **The other three founders should not separately schedule these same tasks on their own machines** — that would produce duplicate concurrent runs racing each other against the same Linear issues; this is Aviran's alone to run.

### Not a gap

- No web server, no container host, no load balancer — this is a native iOS app backed entirely by Supabase's managed services. Resist the urge to provision anything beyond what's above; there's nothing else to run.

## Every session: the discipline that prevents collisions

This is the part that actually answers "what if two of us work on the same thing" — it's not a new mechanism, it's making sure all four of you actually follow the one that exists:

- **Pull before you start, every time.** `git pull --rebase origin brain` in `passenger-brain`, `git pull --rebase origin main` in `passenger-code` — always the explicit branch name, never a bare `origin`. `passenger-brain` and `passenger-code` share the same `origin` remote with unrelated-looking histories; a bare pull can rebase onto the wrong repo's history (documented incident in `passenger-brain/CLAUDE.md`).
- **Both repos are direct-push-with-rebase, no branch/PR ceremony, for now.** A branch+PR model for `passenger-code` was tried and deliberately reverted the same day — Aviran's call: no PR approval for now, changes go straight to `main`. This is a real, accepted tradeoff: with four people (or four agent sessions) potentially touching the same Swift files, a direct push has no safety net if two people's work overlaps in the same file — the first push wins, the second person's `git pull --rebase` either replays cleanly or surfaces a conflict to resolve by hand. Gilad may want to add PR review back later; until then, the mitigation is the claim discipline below, not git structure.
- **Don't hand-edit Linear state.** Even though you *can* drag a card or add a label yourself, don't — it breaks the single-writer invariant chief-of-staff relies on. Instead run "chief-of-staff: run the company" (or dispatch a specific role through it) and let it do the claim-at-the-moment-of-claiming read/write. If you want to hand-pick what gets worked on next, tell chief-of-staff what to prioritize rather than editing the board directly.
- **Task-level collisions are already handled — that's what the claim mechanism is for, not something you manage by hand.** The moment `chief-of-staff` claims a task, it changes that Linear issue's status to `In Progress` and adds an `owner:<role>` label. Any other loop — yours, a co-founder's, doesn't matter — reads that fresh before touching anything, sees the task is taken, and skips it automatically. You don't need to check who's working on what before starting a run; the status change *is* the lock. The one gap this doesn't close: two loops racing to claim the *same still-unclaimed* task in the same instant — the read-then-write isn't atomic, so near-simultaneous claims on a task that's free the moment before both read it could both go through. That needs genuinely simultaneous loop starts to actually happen; it isn't a reason to coordinate before every ordinary run, just a reason not to deliberately start a second loop at the exact moment you know a first one is already claiming things.
- **Your runs will be visible to everyone once the channel's back — that's the point.** Each founder's `chief-of-staff` is meant to post its run summary to the founders' channel under that founder's own name, so the channel doubles as a log of who ran the loop and when. Glance at it before starting a run, once buzz is wired — if someone's summary landed two minutes ago, the board is already fresh and a second run mostly re-reads what they just moved. Not a rule, just the cheapest way to avoid four loops chasing the same three tasks.
- **Commit + push in the same turn you finish anything**, same rule the agents already follow — don't leave doc or board work sitting locally overnight; the other three founders' sessions are only as current as the last push.
- **If you edit an agent or skill file**, copy the same change into `agents-mirror/`/`skills-mirror/` in the same turn. This is the only way a change you make on your machine reaches the others — skip it and it's silently lost the moment someone else's session overwrites their local copy from a stale mirror.

## Communication: buzz to read, Linear to record

**2026-08-04: hilos retired, replaced by buzz** (Aviran's call). The section below describes the *intended* shape once buzz is wired — it isn't live. No daemon, no channel, no allowlist yet; `@chief` currently has no chat presence at all. Talk to Chief through a Claude Code session or Linear until this is set up. What follows is the target design, ported from the retired hilos contract:

Two layers, doing different jobs — don't collapse them.

- **buzz will be the founders' channel, and `chief-of-staff` posts there — one-way.** It posts a short run summary after every "run the company" pass, and pings whichever of you a gate is actually waiting on by name instead of a generic "check Linear" nudge. No other agent posts; chief-of-staff is the single voice there, same reasoning as it being the single Linear writer. It answers to **`@chief`**.
- **Working with `@chief`, once live — the same habits that applied under hilos should carry over:**
  1. **Start the thread, then mention.** Reply where you mentioned it: ask at the top level and the answer lands at the top level; ask inside a thread and the feature's whole life stays in one place.
  2. **Give it time.** Every mention spawns a fresh Claude Code process — a real cold start before any thinking. Quick questions come back fast, real work takes longer.
  3. **Say `@chief` explicitly.** Ambient conversation is never an instruction — two founders agreeing something is broken is a discussion, not a request.
  4. **Ask, don't hand it paths.** It searches both repos. "Show me the strategy doc" is enough.
  5. **Silence may mean offline, not idle.** Whatever machine hosts the daemon has to be awake for Chief to answer.
- **Channel layout, ported from hilos, not yet re-created in buzz.** A `general`-equivalent for founders to talk to Chief (threads do the grouping: a new request or feature is the thread root, everything else — the ticket, product's questions, the mockup, verdicts, the ship notice — replies inside it), a `build-log`-equivalent as the narrated work feed, and a `weekly-trending`-equivalent for the once-a-week GitHub Trending post. Per-feature channels were considered and rejected under hilos for the same reasons that would still apply: threads are finer-grained, features end while channels linger, and Linear already groups by feature.
- **Chief-of-staff is the only agent you talk to.** You never dispatch `designer` or `ios-developer` yourself — you tell chief-of-staff what you want, in your own Claude Code session, and it directs the rest of the team. One voice out, one voice in.
- **You will not be able to dispatch agents from buzz.** Typing "run the company" or "mark this done" in the channel does nothing: the agents have repo and Linear write access, and chat is an untrusted input surface into that. Whatever exception hilos carried for design-review approval no longer applies — that gate is retired anyway (2026-08-02). Anything you ask for in the channel gets surfaced to Aviran as an unactioned request until a real protocol is defined for buzz.
- **The Linear comment on the issue is still the record.** Task state, handoff detail, decisions — that's what chief-of-staff's reconciliation step actually reads (comment trail, commit hashes), and it's what lets any of you catch up on a task cold without scrolling chat history. Discuss in buzz once it's live; the thing that actually happened still gets written to the issue.

**Setup — pending, Aviran's machine.** Needs: a buzz relay URL, an owner-approved agent identity for Chief (`buzz agents draft-create` in Buzz Desktop), a daemon to watch `@chief` and shell out to `claude -p` (buzz ships no `hilos-agent`-equivalent binary — this has to be built), and the founders' buzz pubkeys for the allowlist in `chief.md`. None of this exists yet.

## The weekly meeting

With the loop running daily on its own, the meeting stops being a status sync (`PROGRESS.md` + Linear already answer "what happened") and becomes the checkpoint for the one thing the async loop can't do: clearing `blocked-on-aviran`-style items — scope calls, spend, App Store/credentials, anything that needs a human decision none of the agents are allowed to make. How that governance works day to day beyond the one `design-review` gate is Aviran's call to make directly, not something this doc resolves.

## Open items

- Mobbin/Lance MCP servers in `.mcp.json` are keyed to whoever's account is signed in — if design research needs Mobbin, that's a shared-seat decision, not something this doc resolves.
- `BOARD.md`/`PROGRESS.md` were cleaned up 2026-07-21 (846KB→105KB, 2.47MB→789KB, full history archived under `archive/`) and `project-manager`'s nightly audit now owns keeping them small — worth checking in a few weeks that the recurring check is actually holding at 4x the write volume.
- Gilad may want to add PR review back for `passenger-code` once the team's actually hit a real collision — see the "Every session" note above.
- **hilos retired 2026-08-04, replaced by buzz — not wired up yet.** See "Communication: buzz to read, Linear to record" above for what's outstanding. The old hilos daemon, plist, and `~/.hilos` config were removed the same day; the superseded `hilos-poll` scheduled-task skill was removed with them rather than repurposed.
- **The single point of failure will still be whichever Mac hosts the daemon**, once one exists. No daemon, no Chief — and a sleeping laptop looks identical to an idle one from inside the channel. Work will run under whoever's credentials host the daemon, so a commit made on Serge's request could be authored by someone else. A small VPS fixes both; still unbuilt.
