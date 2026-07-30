# Founder Workflow — Passenger

**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Status:** Active process. Supersedes the "How it gets built" section formerly in `strategy/passenger-strategy.md` — that section now points here.
**Related:** [Strategy](../strategy/passenger-strategy.md) · [Agent OS README](README.md) · [Multi-founder onboarding](ONBOARDING.md) · [Board](BOARD.md)

## The four founders

| Founder | Role | Owns |
|---|---|---|
| Aviran | Product | Strategy, scope, PRD approval, final sign-off |
| Serge | Design | UX/visual craft, component refinement pass on the vibe-coded app |
| Yeari | Data & AI | Heatmap/presence algorithm, data-sourcing/ingestion pipeline |
| Gilad | Dev | Build — backend/DB architecture decision, iOS client |

Each founder has a favorite agent they naturally work through for their own domain (Serge ↔ `designer`, Yeari ↔ `data-engineer`, Gilad ↔ `developer`/`ios-developer`, Aviran ↔ `product`). That's fine and expected — it's how each founder reviews the work closest to them. It does not replace the single interface below: nobody dispatches their favorite agent directly. Every request still goes through `chief-of-staff`, which dispatches the right agent and reports back.

## The build model: vibe-coded first, then refined

1. **Phase 0 — vibe-coded MVP.** The team builds a fully working iOS app fast, agent-driven, no formal design pass, no database. State lives in-memory / hardcoded in the client. Nothing is blocked on a backend decision.
2. **No DB until Gilad decides.** Backend/persistence architecture is Gilad's call, made once there's a real app to hang it off of — not decided upfront. Until then, `developer`'s Supabase/backend work stays paused; `ios-developer` builds against local/mock data.
3. **Serge refines component by component.** Once a component exists (vibe-coded, working, ugly-fine), Serge takes it, fixes it to real design craft, and it goes back into the app. Refinement is incremental and per-component, not a big-bang redesign pass.

**Note:** the strategy doc's existing "Technical architecture" section already names Supabase as the backend. That predates this process and needs reconciling once Gilad actually makes the DB call — flagging it, not resolving it here.

## Every feature's lifecycle

No feature skips this. No code gets written without both a PRD and a Linear task.

```
idea → PRD (product, /feature-prd) → Linear task created → design/build → review → qa → aviran-review → done
```

- **PRD first.** Every feature gets a PRD via the `feature-prd` skill/template before anything is built. No PRD, no build.
- **Linear task, always.** Every feature lives as a Linear issue. `chief-of-staff` is the only agent that writes to Linear. No task in Linear means no code gets pushed for it — this is a hard gate, not a guideline.
- **Vibe-coded components still get a PRD once they're claimed for refinement.** Serge's refinement pass on a component is itself a task — same gate applies, it doesn't skip the process just because the first version was fast.

## Human in the loop: where a founder must approve

The pipeline runs itself end to end except at these stops:

- **`design-review`** — Serge and Aviran, both, independently. No component/screen ships without both sign-offs.
- **`aviran-review`** — final gate before anything reaches `done`. Nothing ships without it.
- **`blocked-on-aviran`** — scope/strategy calls, money, App Store, credentials, destructive git ops. Always stops for Aviran, no exceptions.
- **Gilad's DB call** — when it happens, it's a `blocked-on-aviran`-style stop scoped to Gilad: nothing backend-architectural proceeds until he decides.
- **Yeari's algorithm/data-quality calls** — any `[ASSUMPTION]` `data-engineer` surfaces about the presence algorithm or a data source's trustworthiness is Yeari's to resolve, same pattern as the other domain gates.

## Single interface: talk to chief, not the team

All four founders talk only to `chief-of-staff`. It dispatches every other agent, enforces the PRD-then-Linear gate above, runs the rejection loops (code-review ↩ build, qa ↩ build, acceptance ↩ build/design), and reports status back. Nobody DMs `designer`, `developer`, `data-engineer`, or `ios-developer` directly to get work done — favorite-agent affinity (above) is about whose output you personally care about and review, not a side channel around chief.

## Open items

- Gilad's backend/DB decision is unscoped — no timeline, no candidate shortlist yet.
- No dedicated Linear gate exists yet for Yeari's or Gilad's domains the way `design-review` does for Serge/Aviran — they ship through the normal code-review + QA gates today.
- Strategy doc's Technical architecture section (Supabase) needs an explicit update once Gilad's DB call lands — not done as part of this doc.
