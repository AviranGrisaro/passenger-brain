# data-eng

Feasibility scoping and algorithm-design writeups owned by the `data-engineer` agent — the layer above `passenger-brain/database/` (which holds only the SQL migrations/RLS that `developer` owns; `data-engineer` is a guest there per its own role file).

**[ASSUMPTION] — proposed convention, not yet ratified by a TRD.** Per `.claude/agents/data-engineer.md`'s standing note that "no convention exists yet for exactly where algorithm/pipeline code lives," this folder is proposed as the home for pre-TRD feasibility/scoping documents specifically (not code, not SQL, not PRDs — those still live in `prds/<slug>/`). One flat file per scoping ticket, named `<topic-slug>-feasibility.md`. Revisit and replace this with whatever the first real TRD in this area settles on.

## Status

- `discovery-engine-spec.md` — the working spec (v0.1) for the discovery/localness algorithm itself: experience/venue data model, source viability, ingestion pipeline, author classification, the three-layer (baseline/rising/live) scoring model, R1–R9 rules. Written by Aviran for Yeari, 2026-07-27, as a Claude Artifact — never saved into this repo until recovered 2026-07-30. Read this first for the *why* behind the algorithm; the other two docs below are narrower scoping notes against it.
- `scenic-walk-tiktok-feasibility.md` — PAS-7 scoping (Scenic Walk weighted routing + TikTok place extraction + Google Maps import read).
- `tourist-trap-algorithm-rescope.md` — impact read on decision #22's localness-algorithm pipeline now that decision #37 (2026-07-30) confirms a boolean tourist-trap flag replaces the old 3-way tag.
- `live-events-feasibility.md` — PAS-5 scoping (live-events ingestion pipeline: sourcing options, cost/timeline, explicit Phase-1-buildability call). Conditional call: thin ticketed-events version buildable in Phase 1 (~3–5 weeks), fuller "informal happenings" version is a genuine data-access gap, not yet estimable.
