# Agentic Flow Development — Refinements

**Date:** 2026-07-30
**Status:** Approved, pending write-back to `agent-os/FOUNDER-WORKFLOW.md` + the founder-workflow artifact.
**Input:** Brainstorm stress-test of `agent-os/FOUNDER-WORKFLOW.md` (written same day). Five real gaps surfaced; four resolved with a decision, one deliberately left open.

## 1. Founders/owns split — Yeari vs Gilad sharpened

Previous doc had both under vague "algorithm" / "backend" labels. Sharpened:

- **Yeari — algorithm design.** Video/location extraction, scraping, street-weight generation, routing-algorithm spec. Drives `data-engineer`.
- **Gilad — execution.** Backend process, database, scaling — actually builds it. Drives `developer`/`ios-developer`.

Every algo feature (TikTok import, Scenic Walk weights, presence algorithm) is now explicitly two hops: Yeari designs the spec, Gilad builds against it. Same shape as `design-review` (Serge designs, Gilad builds against Serge's spec) but without a formal named gate (see §3).

## 2. Phase 0 vibe-coded MVP — not exempt from the PRD/Linear gate

Decided: the gate applies from day one, not just to post-MVP features.

- One umbrella PRD + Linear epic covers the Phase 0 build — loose, fast to write, doesn't slow down the "ship fast" goal.
- Serge's later per-component refinement passes are ordinary sub-tasks under the same gate, not a special case bolted on afterward.
- Rationale: avoids a "the first version doesn't count" exception that would need remembering and re-litigating later.

## 3. Domain gates — stay informal

`design-review` is a formal, named, two-person Linear gate (Serge + Aviran). Yeari's algorithm-design calls and Gilad's DB/backend calls get no equivalent formal gate right now.

- Algorithm specs flow through the existing `data-engineer` → `developer` PRD/TRD pipeline. `[ASSUMPTION]`-tagged calls `data-engineer` surfaces are resolved by conversation with Yeari, not a Linear gate.
- Gilad's DB/backend architecture call is the same: informal, resolved when he actually makes it, not pre-built as a named gate.
- Rationale: 4-person team, every new named gate is process overhead with a real cost. Add one only if the informal path actually causes friction.

## 4. Chief-only interface — shortcut carve-out, not a hard rule

Original framing ("talk only to chief") conflicted with `agent-os/README.md`'s documented "direct dispatch still works" pattern (e.g. "use the qa agent to verify X").

Resolved: keep both, scoped by stakes —

- **Direct dispatch stays allowed** for quick, low-stakes, single-agent asks that don't create new work.
- **Anything that creates new work, writes to Linear, or crosses domains must go through `chief`** (prose shorthand for the `chief-of-staff` agent — the underlying agent id is unchanged; this is a naming convention for how the doc refers to it, matching how hilos already nicknames it `@chief`).
- README/ONBOARDING's existing direct-dispatch line is not removed, just implicitly scoped by this rule.

## 5. Left open, deliberately: Supabase-vs-no-DB contradiction

`strategy/passenger-strategy.md`'s Technical architecture section still names Supabase as the decided backend, which conflicts with "no DB until Gilad decides." Explicitly **not fixed now** — Gilad hasn't made the call yet, and editing that section ahead of his decision would just be guessing. Stays flagged as an open item in `FOUNDER-WORKFLOW.md` until he does.

## Write-back scope (for implementation)

Files to update, no others:

- `passenger-brain/agent-os/FOUNDER-WORKFLOW.md` — founders table (§1), Phase 0 language (§2), domain-gates language (§3), single-interface section (§4), "chief" terminology throughout.
- Founder-workflow HTML artifact (`claude.ai/code/artifact/7ba1429d-e90b-42dc-9e1e-b2e2146ec47d`) — same content changes, redeployed to the same URL.
- No changes to: `strategy/passenger-strategy.md` (already points here, §5 stays untouched), `agent-os/README.md`, `agent-os/ONBOARDING.md`, any agent definition files.
