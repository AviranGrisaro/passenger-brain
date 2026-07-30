# data-eng

Feasibility scoping and algorithm-design writeups owned by the `data-engineer` agent — the layer above `passenger-brain/database/` (which holds only the SQL migrations/RLS that `developer` owns; `data-engineer` is a guest there per its own role file).

**[ASSUMPTION] — proposed convention, not yet ratified by a TRD.** Per `.claude/agents/data-engineer.md`'s standing note that "no convention exists yet for exactly where algorithm/pipeline code lives," this folder is proposed as the home for pre-TRD feasibility/scoping documents specifically (not code, not SQL, not PRDs — those still live in `prds/<slug>/`). One flat file per scoping ticket, named `<topic-slug>-feasibility.md`. Revisit and replace this with whatever the first real TRD in this area settles on.

## Status

- `scenic-walk-tiktok-feasibility.md` — PAS-7 scoping (Scenic Walk weighted routing + TikTok place extraction + Google Maps import read).
- PAS-5 (live-events ingestion pipeline scoping) expected to land here too, same convention, whenever that session completes.
