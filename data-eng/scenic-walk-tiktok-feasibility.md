# Feasibility scoping — Scenic Walk weighted routing + TikTok place extraction

**Owner:** data-engineer
**Linear:** [PAS-7](https://linear.app/passenger-app/issue/PAS-7/scope-scenic-walk-weighted-routing-tiktok-place-extraction-feasibility)
**Date:** 2026-07-30
**Provenance:** 2026-07-29 founders meeting, applied to `strategy/passenger-strategy.md` and `strategy/decisions.md` (decisions #32, #34, #35) 2026-07-30. Same risk class as [PAS-5](https://linear.app/passenger-app/issue/PAS-5/scope-live-events-ingestion-pipeline-new-v1-launch-blocking-dependency) (live-events ingestion).
**Related:** `strategy/passenger-strategy.md` (V1 scope bullets on routing/TikTok import, Key risks), `strategy/decisions.md` #32/#34/#35, `passenger-brain/database/README.md` (schema not yet written — Epic C/places table is a real dependency for part of this).

---

## 1. Scenic Walk — weighted street-segment routing

### What's locked vs. what's being asked here
Decision #19 (2026-07-27) locked a **route-preview-only** version for V1: draw scenic vs. fast as comparison polylines, hand off to native Maps/Waze for the actual walk. The 2026-07-29 founders meeting (decision #32) describes something categorically heavier: every street segment carries an **Attractiveness weight**, and Scenic Walk is a real weighted-routing problem — maximize high-weight streets passed A→B, not just compare two pre-existing routes. This section scopes the heavier version.

### Where would Attractiveness weights come from?

**Option A — derive algorithmically from data we already have (or will have from Epic C).** Passenger's places table carries heat (crowd density) and the tourist-trap flag; a street segment's "attractiveness" could be approximated as a function of nearby tagged places (density of non-touristy/local spots within N meters, category mix, etc.) via a spatial join between the street graph and the places table. **Cost: cheap, incremental** — a derived-scoring view/job on top of data the algorithm already owns. **Real limitation:** this is a proxy for "near good places," not for "pleasant/scenic to walk down" — a street lined with quiet, local, non-touristy shops scores well on this proxy but so does a service road behind them; the proxy doesn't know about greenery, shade, sidewalk width, noise, or aesthetics, which is what "Attractiveness" as a walking-route concept usually means.

**Option B — a new curation/scoring pass.** Genuine street-level "attractiveness" (walkability, greenery, safety, visual appeal) isn't derivable from place-level heat/tag data — streets and places are different graphs. This would mean either hand-scoring streets (a hired/managed pass — the same staffing model decision #22 explicitly moved *away* from for localness, for the same cold-start/scaling reasons) or pulling proxy signals from OSM tags (`leisure=park`, `natural=tree`, sidewalk `surface`/`width` tags — inconsistently mapped for Tel Aviv, not guaranteed complete) or running computer-vision analysis over Street View–style imagery to estimate greenery/aesthetics per segment — the latter is a genuine research project, not a Phase 1 task.

**Realistic read:** Option A is buildable now as a v0 proxy but is honestly a weak stand-in for "attractiveness" as the founders' brief describes it. Option B, done properly, is out of scope for any near-term window.

### Routing algorithm

The "fastest" mode is standard shortest-path (Dijkstra/A*) over a walkable graph — solved problem, not a concern. "Maximize high-weight streets passed" is not literally shortest-path; unconstrained, it's closer to an orienteering/prize-collecting variant. In practice this is solved the standard way routing engines handle preference-biased routing: reweight each edge's cost as a function of distance and attractiveness (e.g. `cost = distance − λ · attractiveness`, tuned so the route stays reasonable rather than wandering arbitrarily), then run ordinary Dijkstra/A* over the reweighted graph. **The algorithm itself is not the hard part — the missing input (a real attractiveness signal, see above) is.**

Street-graph data: OpenStreetMap has usable pedestrian-way coverage for Tel Aviv, pulled via Overpass API or a planet extract. Custom-weighted walking routes need a **self-hosted routing engine** (GraphHopper, Valhalla, or OSRM — all open-source, all support custom cost/weighting profiles as a first-class feature). This is the load-bearing finding: **Apple's and Google's own walking-directions APIs do not expose a way to bias routing by arbitrary custom per-street weights** — you can request A→B walking directions from them, but you cannot hand them an "Attractiveness" layer and ask them to route around it. A genuinely weighted Scenic Walk means running our own routing engine on our own OSM extract, not calling MapKit/Google Directions for it.

### Rough build-cost/timeline (separate from live-events and the synthetic density feed)

- OSM extract + self-hosted routing engine (GraphHopper/Valhalla) setup and Tel Aviv-scoped deployment: real but bounded devops work.
- Attractiveness-proxy pipeline (Option A: spatial join of street segments to places table, scoring job): depends on the places/Hoods schema existing first — this can't meaningfully start before Epic C's places table lands, which is itself not yet built (`database/README.md` — schema is empty, starts at migration `001`).
- Custom-weighted routing integration and tuning against real Tel Aviv streets (does a "scenic" route actually feel different from "fastest," not just algorithmically distinct): needs field-testing, not just correctness testing.
- **Rough total: 3–5 weeks of dedicated data/backend effort** for a working weighted-routing MVP, sequenced after (not parallel to) the places/heat schema — before any iOS integration work on top of it.

### Explicit call

**Not realistically buildable inside the Phase 1 window as a genuinely weighted routing algorithm.** It requires a new self-hosted routing engine, a street-graph ingestion pipeline, and an attractiveness signal that only exists as a weak proxy until the places schema is built — stacked on top of two other unproven Phase 1 dependencies (PAS-5 live events, TikTok import below) already put the launch date at risk. Recommend V1 ship the already-locked lighter version instead: two comparison polylines from Apple/Google's own walking directions, with "scenic" defined by a simple heuristic (e.g. routing through 1–2 via-waypoints picked from nearby tagged/local Hoods) rather than a custom-weighted graph. That's a real, shippable middle ground between "no bias at all" and full custom routing, and it's consistent with how full turn-by-turn Scenic View is already scoped as Phase 2/undecided in `strategy/passenger-strategy.md`. Treat genuinely weighted Attractiveness routing as a fast-follow once the places/heat schema and a real attractiveness signal both exist.

---

## 2. TikTok import — place extraction from saved videos

### Technical approaches

- **Video frame analysis / object detection.** Generic landmark-detection APIs (e.g. Google Vision's Landmark Detection) work for famous global landmarks, not small local venues — identifying "this specific unmarked bar in Florentin" from a video frame requires matching against a maintained image database of local businesses, which doesn't exist. **Least reliable of the three, not viable for generic small-business places.**
- **OCR on-screen text/captions.** Many recommendation-style TikToks overlay the place name as on-screen text, and captions frequently name the place or use a location tag directly. OCR is mature and cheap (Apple's on-device Vision framework does this natively; Google Cloud Vision/AWS Textract as cloud fallbacks). **Highest ROI-per-effort of the three — this and caption text are the primary signal, not a supporting one.**
- **Audio transcription + NLP entity extraction.** Transcribe spoken narration (Whisper API or equivalent ASR), run entity extraction (NER or an LLM prompt) over the transcript plus caption text, geocode candidate names against a places API scoped to the relevant city. Genuinely buildable with commodity tooling — no novel research required.
- **Recommended combination:** caption text + on-screen OCR + audio transcription feeding one LLM-based extraction pass, geocoded and confidence-scored, skipping frame-based visual place recognition entirely (it's the weakest signal for exactly the kind of small local venues this product cares about).

**Access/ToS flag, separate from the technical question:** fetching the full video content of an arbitrary shared TikTok (not the uploader's own account) via unofficial means carries a real ToS risk, not just a technical one — this needs an explicit sign-off before building, not an assumed "we'll scrape it."

### Realistic accuracy/coverage

**[ASSUMPTION] — no benchmark data exists for this; the following is a professional estimate, not a sourced number.** Combined caption+OCR+audio signal probably surfaces an extractable, geocodable place name in a minority-to-roughly-half of "recommendation"-style videos — many videos never name the specific place at all (relying on the viewer already knowing it, or using vague framing like "this hidden gem"), and geocoding accuracy drops further for generic/ambiguous names or chains. This is not a case where V1 can promise reliable extraction — it needs a confirm-before-save UX (asking "did you mean X?"), not silent auto-add.

### Rough build-cost/timeline

Using off-the-shelf APIs (OCR, an ASR service, an LLM call, a geocoding API) rather than building any of these components from scratch, a working v1 pipeline — OCR + transcription + LLM extraction + geocoding + confidence-gated user-confirmation step — is roughly **2–4 weeks**, assuming the ToS/access question above is resolved quickly. Tuning down false positives to a genuinely polished experience is realistic post-launch iteration, not a Phase 1 blocker in itself.

### Explicit call

**Buildable in the Phase 1 window**, as a v1 pipeline with a mandatory user-confirmation step (not fully automatic extraction) — this is the more tractable of the two asks, since it's mostly assembling existing commodity AI APIs rather than inventing a new algorithm. The real risk isn't algorithmic feasibility: it's (a) the TikTok ToS/access question, which needs Aviran's explicit call before a TRD gets written, and (b) accuracy will be genuinely uneven, which is a UX/design constraint (confirm-before-save) more than a build blocker.

---

## 3. Google Maps saved-list import — feasibility read only (decision #35, not authorized to build)

Google doesn't expose a public API for reading a user's personal saved-places lists — the only realistic path today is **Google Takeout**, where a user exports their own saved-places data as a structured file (CSV/JSON/KML) that could then be manually uploaded into Passenger. That's a materially simpler pipeline than TikTok import — no video/OCR/ASR, just parsing a structured export and geocoding/deduping against Passenger's places table — but it still requires the user to do a manual export-and-upload step outside the app, not a one-tap live import. Worth a real look as a fast-follow once there's bandwidth, but it's a different (much smaller) shape of problem than TikTok import, not a comparable build. Per decision #35, this is exploration only — no pipeline is being scoped or authorized here.

---

## Summary

| Ask | Buildable in Phase 1 window? | Recommendation |
|---|---|---|
| Scenic Walk — weighted routing | **No.** Real 3–5 week dependency chain (self-hosted routing engine + street-graph ingestion + an attractiveness signal that only exists as a weak proxy until the places schema ships), stacked on top of two other unproven Phase 1 pipelines. | Ship the already-locked lighter comparison-polyline version for V1; weighted Attractiveness routing is a fast-follow. |
| TikTok place extraction | **Yes**, as a v1 with mandatory confirm-before-save. Mostly commodity APIs (OCR/ASR/LLM/geocoding), ~2–4 weeks. | Build for V1, gated on Aviran resolving the TikTok ToS/access question before a TRD is written. |
| Google Maps saved-list import | Not scoped — exploration only, per decision #35. | Feasible as a future Takeout-upload feature; smaller/simpler than TikTok import. Not a Phase 1 ask. |
