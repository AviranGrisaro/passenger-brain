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
| T-030 | Scope live-events ingestion pipeline — new V1 launch-blocking dependency (Linear `PAS-5`) | backlog | data-engineer | 2026-07-30 | Founder-direct, live chat, 2026-07-29 (PROGRESS.md). Aviran moved the live events layer from a Phase 2 candidate into V1, alongside heat + tag — **but launch-blocking**: V1 doesn't ship until this pipeline works. Redline applied to `strategy/passenger-strategy.md` (now reads as locked V1 scope). Design side already updated in `design/ux-flows.md` §8a. `data-engineer` scoping ask: sourcing options + realistic freshness/coverage, rough build-cost/timeline, and an explicit call on whether this fits the current Phase 1 timeline. **Project now exists** — `PAS-5` attached to Linear project **Passenger V1** (created 2026-07-30). |
| PAS-6 | Confirm 2026-07-30 founders-meeting V1 scope ambiguities | blocked-on-aviran | — | 2026-07-30 | Seven flagged items from the 2026-07-29 founders-meeting scope lock, none resolved: tourist-trap boolean flag vs. decision #18's three-tag system; closed-place (Apple Maps) save treatment; softer "tourist trap" copy; "Profile tab" naming vs. no-profiles gate; Passport per-Hood status vs. the existing seven-tier ladder; "quick filters" chrome-vs-sheet placement; Google Maps import (explicitly exploration-only). Full detail: `strategy/passenger-strategy.md` Open questions, `strategy/decisions.md` #27-36. Do not dispatch build/PRD work against any of these until Aviran answers here or in hilos. |
| PAS-7 | Scope Scenic Walk weighted-routing + TikTok import feasibility | in-progress | data-engineer | 2026-07-30 | **Scoping done, awaiting `chief-of-staff` state transition (single-writer rule).** Full writeup: `passenger-brain/data-eng/scenic-walk-tiktok-feasibility.md` (PROGRESS.md worklog entry, same date). Calls: (1) Scenic Walk weighted routing — **not buildable in Phase 1 window** (needs a self-hosted routing engine + street-graph ingestion + an attractiveness signal that's only a weak proxy until the places schema ships); recommend shipping the already-locked lighter polyline-comparison version instead. (2) TikTok place extraction — **buildable in Phase 1 window** (~2-4 weeks, OCR+ASR+LLM extraction+geocoding, mandatory confirm-before-save step); one non-technical blocker flagged — TikTok video-fetch ToS/access needs Aviran's sign-off before a TRD. (3) Google Maps saved-list import — feasibility read only, per decision #35, not scoped as a build. Linear comment posted with findings + commit hash. |
| PAS-8 | Reconcile UX docs (`ux-flows.md`, `map-rendering-spec.md`) against 2026-07-30 scope lock | in-progress | designer | 2026-07-30 | Confirmed items to reconcile: Hoods terminology, Been-place Passport stickers, Saved-vs-Been distinction, Passport promoted from Phase-2-preview (Journey 7) into real V1 scope, category rename. Flagged items (PAS-6) explicitly held open, not resolved. Dispatched, in flight. |
| PAS-9 | Revise "tourist trap" copy in Phase 1 marketing plan | in-progress | marketing | 2026-07-30 | Aviran flagged current "tourist trap" framing as risking alienating place owners (decision #36). Marketing's own plan uses the phrase verbatim in its external pitch line — needs a softer replacement term. Dispatched, in flight. |
| PAS-10 | Draft V1 PRDs for confirmed 2026-07-30 scope items | in-progress | product | 2026-07-30 | First real PRD pass — `prds/INDEX.md` was empty. Spec-ready now: map/Hoods, time slider, Hood/place detail + category rename, live events. Held back pending PAS-6/PAS-7: tourist-trap pipeline, Places closed-place edge case, Passport, Scenic Walk, TikTok import. Google Maps import excluded entirely (exploration-only). Dispatched, in flight. |

## Linear

Workspace `passenger`, team **Passenger** (`PAS`), one project — **Passenger V1**. Features are issues inside that project, not projects of their own; the previous workspace fragmented into 13 projects and lost the thread. `chief-of-staff` is the only agent that writes to Linear.
