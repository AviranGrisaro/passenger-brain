# Localness algorithm rescope — boolean tourist-trap flag

**Owner:** data-engineer
**Date:** 2026-07-30
**Provenance:** `strategy/decisions.md` #37 — Aviran confirmed live, 2026-07-30, that the boolean tourist-trap flag (1/0) fully replaces the three-way **Local · Mix · Tourist** vibe tag (decision #18). This doc scopes what that reversal actually changes in decision #22's "algorithm proposes, local QA verifies" pipeline — the strategy/UX lock resolved *what the tag is*; this is the follow-on read on *what the algorithm now has to predict*.
**Related:** `strategy/passenger-strategy.md` (V1 scope, Key risks), `strategy/decisions.md` #22/#24/#37, `design/ux-flows.md` §4 Journey 4 (local-QA toast, now binary), `design/map-rendering-spec.md` §3 (rendering, already rewritten to the boolean model), `data-eng/discovery-engine-spec.md` (the underlying algorithm design this rescope is scoped against — see its note on keeping `local_score`/`tourist_score` separate internally even though the user-facing flag is now binary).

---

## What actually changes for the algorithm

**The target variable shrinks from a 3-class problem to a binary one.** Decision #22's pipeline — an algorithm proposes a classification, crowdsourced local-QA verifies/corrects it — was scoped against **Local / Mix / Tourist**, a 3-way ordinal-ish label. It now only needs to predict **tourist-trap: yes/no**. This is a real scope reduction, not a relabeling:

- **Fewer classes to calibrate.** A 3-way classifier needs to place a boundary on both sides of "Mix"; a binary classifier needs one decision boundary. Simpler to reason about, simpler to validate, likely fewer labeled examples needed to get a usable v0.
- **Local-QA's ask is now a single yes/no toast** (`ux-flows.md` §4 Journey 4, rewritten 2026-07-30) instead of a 3-way tap. Lower cognitive cost per answer, which should help response rate — a real, if unmeasured, upside for the cold-start problem (strategy.md Key risks).
- **What signal actually predicts "tourist trap" is not settled here.** Candidate proxy features (review-language patterns, price-vs-neighborhood-baseline, foreign-language review share, opening-hours patterns typical of trap-y spots) are the same kind of features a 3-way model would have used for the "Tourist" end of its scale — this rescope doesn't invent a new feature-engineering problem, it removes the "Mix" middle class the model no longer needs to separate from either end.

## What doesn't change

- **Cold start is unaffected.** A new city still has zero local-QA answers on day one regardless of whether the target is 2-class or 3-class — this rescope doesn't touch that risk.
- **The crowdsourced-verification mechanic itself is unaffected** (decision #22, #24) — geofence-verified dwell still triggers the ask, the algorithm still proposes and users still correct. Only the label space changed.
- **Heat/density computation (the other half of the map) is untouched** — this rescope is scoped entirely to the tourist-trap side of the pipeline.

## Explicit call

**No new feasibility risk introduced — if anything, this simplifies what was already the riskiest unproven piece of V1** (strategy.md Key risks: "local QA's future" / cold start). Recommend building the v0 classifier against the binary target directly rather than building a 3-way model and collapsing it post-hoc — training against the actual target is simpler and avoids inventing a "Mix" boundary that no longer has a UI to attach to. Nothing here blocks or delays anything already scoped in `scenic-walk-tiktok-feasibility.md` (PAS-7) or PAS-5 (live events) — this is a separate, smaller piece of the same agent's ownership area.
