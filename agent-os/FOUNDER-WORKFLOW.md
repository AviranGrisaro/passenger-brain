# Agentic Flow Development — Passenger

**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Status:** Active process. Supersedes the "How it gets built" section formerly in `strategy/passenger-strategy.md` — that section now points here.
**Related:** [Strategy](../strategy/passenger-strategy.md) · [Agent OS README](README.md) · [Multi-founder onboarding](ONBOARDING.md) · [Board](BOARD.md)

## The four founders

| Founder | Role | Owns |
|---|---|---|
| Aviran | Product | Strategy, scope, PRD approval, final sign-off |
| Serge | Design | UX/visual craft, component refinement pass on the vibe-coded app |
| Yeari | Data & AI | Algorithm design — scraping, video/location extraction, street-weight generation, routing-algorithm spec |
| Gilad | Dev | Execution — backend process, database, scaling, iOS client. Builds against Yeari's algorithm specs |

Every algorithm feature (TikTok import, Scenic Walk weights, the presence algorithm) is a two-hop handoff: Yeari designs the spec, Gilad builds against it — same shape as design-review's Serge-designs/Gilad-builds pattern, just without a named gate (see below).

Each founder has a favorite agent they naturally work through for their own domain (Serge ↔ `designer`, Yeari ↔ `data-engineer`, Gilad ↔ `developer`/`ios-developer`, Aviran ↔ `product`). That's fine and expected — it's how each founder reviews the work closest to them. It does not replace the single interface below: favorite-agent affinity is about whose output you personally review, not a side channel for getting work done.

## The build model: vibe-coded first, then refined

1. **Phase 0 — vibe-coded MVP.** The team builds a fully working iOS app fast, agent-driven, no formal design pass, no database. State lives in-memory / hardcoded in the client. Nothing is blocked on a backend decision.
2. **No DB until Gilad decides.** Backend/persistence architecture is Gilad's call, made once there's a real app to hang it off of — not decided upfront. Until then, `developer`'s Supabase/backend work stays paused; `ios-developer` builds against local/mock data.
3. **Serge refines component by component.** Once a component exists (vibe-coded, working, ugly-fine), Serge takes it, fixes it to real design craft, and it goes back into the app. Refinement is incremental and per-component, not a big-bang redesign pass.

**Note:** the strategy doc's existing "Technical architecture" section already names Supabase as the backend. That predates this process and needs reconciling once Gilad actually makes the DB call — flagging it, not resolving it here.

## Every feature's lifecycle

No feature skips this, including Phase 0 itself. No code gets written without both a PRD and a Linear task.

```
idea → PRD (product, /feature-prd) → Linear task created → design/build → review → qa → aviran-review → done
```

- **PRD first, even for Phase 0.** The vibe-coded MVP gets one umbrella PRD + Linear epic — loose, fast to write, doesn't slow the "ship fast" goal down. There's no "the first version doesn't count" exception to remember later.
- **Linear task, always.** Every feature lives as a Linear issue. `chief` is the only agent that writes to Linear. No task in Linear means no code gets pushed for it — this is a hard gate, not a guideline.
- **Vibe-coded components still get a PRD once they're claimed for refinement.** Serge's refinement pass on a component is an ordinary sub-task under the same epic — same gate applies, it doesn't skip the process just because the first version was fast.

## Human in the loop: where a founder must approve

The pipeline runs itself end to end except at these stops:

- **`design-review`** — Serge and Aviran, both, independently. No component/screen ships without both sign-offs.
- **`aviran-review`** — final gate before anything reaches `done`. Nothing ships without it.
- **`blocked-on-aviran`** — scope/strategy calls, money, App Store, credentials, destructive git ops. Always stops for Aviran, no exceptions.
- **Gilad's DB call** — when it happens, it's a `blocked-on-aviran`-style stop scoped to Gilad: nothing backend-architectural proceeds until he decides. No formal named gate for this yet, on purpose (see Open items) — a 4-person team pays real overhead for every new named gate, so this stays informal until it actually causes friction.
- **Yeari's algorithm calls** — any `[ASSUMPTION]` `data-engineer` surfaces about the algorithm design or a data source's trustworthiness is Yeari's to resolve. Flows through the normal `data-engineer` → `developer` PRD/TRD handoff, no separate named gate — same informal treatment as Gilad's DB call above.

## Single interface: talk to chief, not the team

All four founders default to talking to `chief` (the `chief-of-staff` agent — nicknamed `@chief` since hilos, carried over to buzz once that's wired up, and this doc does the same). It dispatches every other agent, enforces the PRD-then-Linear gate above, runs the rejection loops (code-review ↩ build, qa ↩ build, acceptance ↩ build/design), and reports status back.

Direct dispatch to a specific agent still stands, but only for read-only/verification asks that touch no code and no Linear state — "qa, verify X", "designer, what's the status of Y". **Never for anything that writes code** — that always needs a PRD + Linear task first (above), no exception carved out here. Anything that creates new work, touches code, writes to Linear, or crosses domains goes through `chief`. Favorite-agent affinity (above) is about whose output you personally review — it isn't a way to route real work around chief.

## Open items

- Gilad's backend/DB decision is unscoped — no timeline, no candidate shortlist yet.
- No dedicated Linear gate exists yet for Yeari's or Gilad's domains the way `design-review` does for Serge/Aviran — deliberate, not an oversight (see Human in the loop above). Revisit only if the informal path causes real friction.
- Strategy doc's Technical architecture section still names Supabase as decided, which conflicts with "no DB until Gilad decides." Left unfixed on purpose — editing it ahead of Gilad's actual call would just be guessing. Update it once he decides, not before.
