# Passenger Agent OS — Board

Single source of state for the agent team. Every agent reads this **and `PROGRESS.md`** before starting, and updates its rows + appends a PROGRESS.md worklog entry after finishing — committed and pushed the same turn. `chief-of-staff` is the runtime: each "run the company" pass moves every task as far down the lifecycle as it can and refills the pipeline via `product` when it drains.

## Scope gate (added 2026-07-26 — read before opening any task)

Passenger exists because the previous board ran 27 PRDs through this exact lifecycle, ten of them building features the strategy forbids. Every gate passed. Nobody read the strategy.

**A task may not leave `spec` unless its PRD quotes the line in `strategy/passenger-strategy.md` that authorizes it.** `product` enforces this and rejects PRDs that can't. Standing prohibitions:

- No social features of any kind — friends, following, posting, presence, profiles, avatars.
- No onboarding — the app opens straight to the map plus location permission.
- Phase 2 (proximity intelligence, **Scenic View**, **Live Events**) and Phase 3 (AI guide, shake-to-decide) are parked. Don't build toward them or leave hooks. Points is retired — replaced by the Phase 2 stamp collection system (see `strategy/passenger-strategy.md`), not a separate parked item.
- **Scenic View and Live Events moved out of V1 on 2026-07-27** (decisions #19, #20). V1 tap-a-spot hands off to native Maps/Waze; the V1 map is heat + tag only. Both existed in the Locali client, so watch for them returning through `SALVAGE.md` rather than through a PRD.

## Task lifecycle (state → owner)

```
backlog → spec(product) → design(designer) → trd(architect) → build(ios-developer and/or developer)
        → code-review(ios-code-reviewer and/or code-reviewer) → qa(qa) → acceptance(product) → done
```

- **iOS vs backend split:** `build`/`code-review` fan out by surface — `ios-developer`/`ios-code-reviewer` for the Swift/SwiftUI client (`passenger-code/`), `developer`/`code-reviewer` for the Supabase backend (`passenger-brain/database/`), both pairs when a task spans both. The architect's TRD build breakdown tags each step **[iOS]**/**[Backend]**.
- Pure-build tasks (no UX surface) skip `design`.
- Marketing/research tasks: `backlog → in-progress(owner) → acceptance(product) → done`.
- Rejection loops (backward only): code-review REQUEST CHANGES → `build` · qa FAIL → `build` · acceptance REJECT → `build` or `design`. The rejecting agent writes concrete findings; the fixing agent addresses exactly those.
- `blocked-on-aviran`: strategy/scope decisions, money, external accounts (App Store, credentials), destructive ops — including every Supabase migration apply step (Aviran holds the DB credentials). Nothing else stops the loop.
- A task is `done` only after `product` ACCEPTs it against the PRD.

Task rows: `| id | task | state | owner | updated | notes / findings / output |`

## Active phase

**Phase 1 — ship one map to real strangers in Tel Aviv.** Per `strategy/passenger-strategy.md`: nothing downstream matters until a real person reopens the app within a week, unprompted.

## Tasks

| id | task | state | owner | updated | notes / output |
|---|---|---|---|---|---|
| — | _empty — awaiting first `product` pass over the strategy doc_ | — | — | 2026-07-26 | Fresh start. See PROGRESS.md entry for 2026-07-26. |
| M1 | Phase 1 marketing & acquisition plan (grassroots, zero-spend, Tel Aviv) | in-progress | marketing | 2026-07-28 | `marketing/phase-1/marketing-acquisition-plan.md`. **REJECTED by `product`** (PROGRESS.md, commit `e5339ea`) — back to `in-progress(marketing)` per rejection-loop rule. Blocking findings F1–F3: (F1) the "2–8 day" reopen window silently answers strategy's open "within a week" question with no [ASSUMPTION] label; (F2) "unprompted" is defined against a factually wrong claim that V1 ships no notifications — decision #24 puts a local notification in V1, so a notification-tap reopen would wrongly count as unprompted, and tracking needs a launch-source field (cold launch vs. notification tap); (F3) "confirmed by Aviran" zero-budget claim is unsourced (no such decision exists anywhere) and self-contradicts the plan's own ask for Aviran to approve QR-card print costs. Should-fix, non-blocking: restate the 20%/30-install gate as existence/repeatability (20% of 30 is only 6 people — too noisy for a rate reading), remove or escalate the unauthorized native share-sheet "invite a friend" idea (no strategy line permits in-app share/invite, adjacent to no-social-features), fix the plan's stale "Phase 4"/"friends & family beta" Open-questions residual (role-file itself already fixed in `8b19a5e`). Full verdict in PROGRESS.md. |

## Linear

Workspace `passenger`, team **Passenger** (`PAS`), one project — **Passenger V1**. Features are issues inside that project, not projects of their own; the previous workspace fragmented into 13 projects and lost the thread. `chief-of-staff` is the only agent that writes to Linear.
