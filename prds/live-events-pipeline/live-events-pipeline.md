# Live Events Ingestion Pipeline — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Launch-blocking.** Strategy makes the pipeline, not the overlay, the thing V1 waits on. `live-events-overlay` specs the client and explicitly fences the pipeline out; `PAS-5` delivered a **feasibility read** (`data-eng/live-events-feasibility.md`), not a spec. This PRD is the spec that was missing between them.
**Source set is deliberately open** — which feed(s) ship is `PAS-6` item 10, Aviran's call. Every requirement below is written to hold regardless of which source lands.

## Description

- The backend job that gets real Tel Aviv events into the `events` table the overlay reads, and decides which ones surface.
- Two halves with different risk profiles (`data-eng/live-events-feasibility.md`): **ingestion** (get structured events in at all) and **ranking** (decide which are "likely-interesting").
- Ingest from structured feeds; do not mine social content. That is Aviran's own framing in `data-eng/discovery-engine-spec.md` and matches the strategy line word for word.
- The `rank` column is the contract boundary: this pipeline writes it, the client only sorts and truncates by it.
- **Not in scope:** the client surface, markers, detail sheet, and toggle (`live-events-overlay`); ticketing, booking, or promoter placement (strategy fences B2B outright); user-submitted events; personalization of any kind; choosing the source set (`PAS-6` item 10).

## Motivation

- Strategy, verbatim: *"it's launch-blocking: V1 does not ship until data-engineer has a working live-events ingestion pipeline (scoping ticket PAS-5)."*
- Strategy, verbatim: *"surfaced on the map, algorithmically selected as likely-interesting to the user (not just a raw feed of every event)."*
- `data-eng/discovery-engine-spec.md` names the failure mode this spec exists to prevent: an expired listing is *"worse than an empty shelf."*

## Requirements

### Must-have (P0)

1. **The source set is a recorded decision, not an inference.**
   - [ ] Which feed(s) V1 ingests is written down, with the coverage each one does and does not give (`data-eng/live-events-feasibility.md` §1).
   - [ ] If the shipped set is ticketed-only (Eventbrite/Ticketmaster class), that skew is stated in the ticket and to Aviran before build, not discovered at launch — it is the exact reason `PAS-6` item 10 is open.
   - [ ] Every source's terms permit the use. No source is integrated on an unverified access assumption.

2. **An event enters the table only if it carries every field the client contract requires.**
   - [ ] Required: name, start time, end time, coordinates, source, source event id.
   - [ ] A record missing any required field is dropped at ingest and counted, never written with a placeholder — `live-events-overlay` req 4 omits absent optional fields but cannot render an event with no time or no location.
   - [ ] Times are stored as absolute timestamps, not local hour-of-day — the slider's now → +12h window crosses midnight (`time-slider` Open questions).

3. **Every event is attributed to exactly one Hood.**
   - [ ] `hood_id` is resolved from the event's coordinates against `hoods` (`prds/hood-dataset/`), at ingest.
   - [ ] An event whose coordinates fall in no Tel Aviv Hood is not ingested — the map has nowhere to draw it.
   - [ ] Attribution is re-resolvable: a Hood boundary correction re-attributes existing events rather than leaving them on a stale Hood.

4. **The same real event appears once, however many sources carry it.**
   - [ ] Records matching on venue, start time, and name across sources collapse to one row.
   - [ ] `(source, source_event_id)` is unique, so re-ingesting a source never duplicates.
   - [ ] Pass condition: ingesting two overlapping sources produces no two rows a person would call the same event.

5. **Expired events never render, and this is checked, not assumed.**
   - [ ] An event whose end time has passed is excluded from what the client can fetch — `live-events-overlay` req 5 states the rule; this pipeline is what makes it true.
   - [ ] An event whose end time passes while the client holds a cached payload is filtered client-side too, so a stale cache cannot resurrect it.
   - [ ] Nothing is hard-deleted on expiry; expired rows are excluded from the served set. **[ASSUMPTION]** — retention period unstated.

6. **The pipeline writes `rank`, and rank uses no per-user signal.**
   - [ ] Every served event carries a `rank` the client sorts and truncates by, re-deriving nothing (`live-events-overlay` req 3).
   - [ ] Ranking inputs are generic — quality, popularity, recency, proximity, category. **No per-user profile, preference store, or interest history**: V1 has no identity, and strategy puts personalization in Phase 3 (`live-events-overlay` Open questions).
   - [ ] Two devices requesting the same hour receive the same order.
   - [ ] Pass condition: the ranked top set for a busy Friday hour is reviewed by a person and is not simply "everything ingested, in time order" — the strategy line requires selection, and a ranker that selects nothing fails it.

7. **Freshness is bounded and stated.**
   - [ ] Ingest runs on a fixed schedule, and the served set is never older than one full cycle.
   - [ ] An event published by a source at least one full cycle before its start time is present when the map reaches that hour.
   - [ ] **[ASSUMPTION]** Cadence unstated upstream. Events are known in advance (`live-events-overlay`'s own assumption), so a periodic job suffices and Realtime is not required.

8. **An empty result is a valid output, not a failure.**
   - [ ] A source outage, an empty window, or a rejected-everything ranking pass all yield an empty set the client renders as absence (`live-events-overlay` req 5), never an error state.
   - [ ] Failures are visible to the team — a source that has returned nothing for a full day is logged, not silently absorbed.

### Nice-to-have (P1)

- A per-source ingest health readout — rows in, rows dropped, drop reason.
- Event category normalized across sources, so `live-events-overlay`'s P1 glyphs become possible.

## Technical design

- **Data model:** new `public.events` — `id`, `source`, `source_event_id`, `name`, `start_at`, `end_at`, `lat`, `lng`, `venue_name`, `hood_id` (FK → `hoods.id`), `category`, `rank`, `ingested_at`. Unique on `(source, source_event_id)`. Public-read, no user-scoped rows. This extends the sketch in `live-events-overlay`'s technical design with the ingest-side fields that sketch omitted (source identity, dedup key, ingest time).
- **APIs / contract:** the client fetches the whole now → +12h window alongside the density load and re-filters locally per hour (`live-events-overlay`). The served set is already deduped, expired-filtered, Hood-attributed and ranked — the client applies no business logic.
- **Architecture notes:** ingest runs server-side on a schedule (`pg_cron` is already the pattern migration `002` established for synthetic density). Source credentials are env/config only, never committed (`CLAUDE.md`).
- **Dependencies:** **`hood-dataset` first** — req 3's attribution is impossible without real polygons, and `data-eng/live-events-feasibility.md` §2 already sequences this work after the Hoods schema. `places-dataset` is needed only if venue matching against known places is wanted (it is not required by any P0 here). Blocks `live-events-overlay`'s real-data path; the client ships without it, empty.
- **Open technical questions:** whether `rank` is absolute or per-hour (`live-events-overlay`'s question, unresolved); the on-screen marker cap, unknowable until real Tel Aviv event volume is measured; whether the ranker runs at ingest or at read.

## Assumptions

- **[ASSUMPTION]** Events are known in advance, so periodic ingest is sufficient and Realtime is not needed. Inherited from `live-events-overlay`. If the useful events turn out to be same-hour and unpredictable, req 7's cadence and the whole contract change.
- **[ASSUMPTION]** "Likely-interesting" means generically interesting, ranked identically for every viewer. `live-events-overlay` flagged this for Aviran and it is still unconfirmed. A per-user reading is a Phase 3 identity dependency, not a ranking tweak.

## Open questions & risks

- **`PAS-6` item 10 is open and this PRD does not close it.** `data-engineer`'s call was **conditional**: the thin ticketed-only version is buildable in Phase 1; the version that makes "something's happening near you right now" feel true is a **data-access gap, not an engineering-hours gap**. Whether the thin version meets the bar that made this launch-blocking is Aviran's, and the launch date genuinely depends on it.
- **The informal-events layer has no reachable source.** Facebook Events is very likely dead as a feed; local Israeli platforms' API access is unverified; an aggregator is a procurement conversation with unverified Israel coverage; manual or crowd curation repeats the staffing and cold-start tradeoffs decisions #22 and #24 already moved away from. All four paths are outside `data-engineer`'s unilateral reach.
- **Cost:** roughly 3–5 weeks for a thin single-feed v1 with basic ranking, sequenced after the Hoods schema, before any iOS work (`data-eng/live-events-feasibility.md` §2). Each additional source is another 1–2 weeks.
- Three launch-blocking feasibility questions stack — events, Scenic Walk, TikTok import. Any one can slip the date (strategy, Key risks).

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | Standing rule, founder-direct 2026-07-30. The pipeline is launch-blocking, had a feasibility read (`PAS-5`, closed) and a client PRD that explicitly fences it out — no spec existed in between |
| 2026-07-30 | Written source-agnostic, with the source set as req 1 rather than a choice made here | `PAS-6` item 10 is Aviran's open call; specifying one feed would pre-decide it. Schema, dedup, expiry, attribution and rank contract hold whichever source lands |
| 2026-07-30 | Ingest-side fields added to the `events` sketch in `live-events-overlay` (source, source event id, ingested_at) | Reqs 4 and 7 are unfalsifiable without a dedup key and an ingest timestamp |
