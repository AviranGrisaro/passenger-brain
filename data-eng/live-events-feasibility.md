# Feasibility scoping — Live Events ingestion pipeline

**Owner:** data-engineer
**Linear:** [PAS-5](https://linear.app/passenger-app/issue/PAS-5/scope-live-events-ingestion-pipeline-new-v1-launch-blocking-dependency)
**Date:** 2026-07-30
**Provenance:** Founder-direct, 2026-07-29 live founders meeting — Live Events moved from a parked Phase 2 candidate into V1 scope, but explicitly **launch-blocking**: V1 does not ship until this pipeline works. Applied to `strategy/passenger-strategy.md` (lines 46, 65, 108, 125, 145, 148–149, verified directly in the file). Design side already updated in `design/ux-flows.md` §8a (third Primary-tier map toggle — out of scope for this doc). Same risk class and same ticket-shape precedent as [PAS-7](https://linear.app/passenger-app/issue/PAS-7/scope-scenic-walk-weighted-routing-tiktok-place-extraction-feasibility) (`data-eng/scenic-walk-tiktok-feasibility.md`), followed here for output shape/location.
**Related:** `data-eng/discovery-engine-spec.md` §"Live events are a feed problem, not a mining problem" (Aviran's own algorithm-design framework, written 2026-07-27 — this scoping pass builds directly on it rather than re-deriving from scratch) and its Sources table (§"Sources and how we get them"); `strategy/decisions.md` #22 (staffing-model rejection for localness), #24 (local-QA cold-start risk).

**Explicitly not this ticket's scope:** the events-overlay UI/UX (already designed, `design/ux-flows.md` §8a) and the routing-preview scope question (separate, resolved by PAS-7).

**Explicitly two other systems, not to be conflated with this one:** the synthetic density feed (a placeholder heat data source, decision #4 — unrelated, not being touched here) and the localness/local-QA pipeline (decision #24's geofence-triggered "was this touristy?" crowd toast — a different signal, different trigger, different data entirely). This doc scopes a third, new system: ingesting real-world dated events and deciding which ones are worth showing.

---

## The one framing decision everything else hangs off

`discovery-engine-spec.md`'s existing algorithm design already answers the shape of this problem, written before PAS-5 existed as a ticket: **"Events have structured fields — start, end, venue, price, ticket link — and ticketing platforms, venue calendars and tourism boards already publish them cleanly. Mining them out of social posts is hard work for a worse result. Ingest events from feeds, and use our social signal only to rank which ones a given user should care about."** That single sentence rules out the mining/scraping-social-content approach this codebase already rejected for a different reason (the Sources table marks Instagram "Share-in only," TikTok "Share-in only," Snap "Drop" — no crawl path exists for any of them, for the same legal/ToS reasons that would apply here). It also matches the strategy line word for word: "algorithmically selected as likely-interesting to the user (not just a raw feed of every event)" is exactly "ingest from feeds, rank with our own signal," not "mine social media for happenings."

So this pipeline has two genuinely separate halves, and they have very different feasibility profiles:

1. **Ingestion** — get structured event data (what/where/when) into the system at all.
2. **Ranking/selection** — decide which ingested events are "likely-interesting," so the layer isn't a raw firehose. This is new build work on top of whichever feed(s) get chosen, not a byproduct of ingestion.

---

## 1. Sourcing options for Tel Aviv

| Option | Type | Freshness | Coverage | Verdict |
|---|---|---|---|---|
| **Eventbrite API** | Real public API | Good — organizers publish ahead of time, near-real-time once posted | Skews to ticketed workshops, meetups, community events. Real global platform with an actual Tel Aviv presence, but only events whose organizers specifically chose Eventbrite | **Core candidate** — cheapest real feed to integrate |
| **Ticketmaster (Discovery API)** | Real public API | Good | Skews to larger commercial venues/concerts (arenas, established clubs) | **Core candidate**, but narrow — this is the "big show" layer, not the "something's happening tonight nearby" layer |
| **Songkick / Bandsintown** | Real public APIs | Good | Concert/music-specific only | Supplementary at best — one category, not general events |
| **PredictHQ**-style event-intelligence aggregators | Paid B2B API, aggregates many underlying ticketing/venue/public-event sources into one feed | Depends on the freshness of whatever it aggregates | **[ASSUMPTION]** — broadest coverage of any single integration in principle, but Tel Aviv-specific depth is unverified without a direct vendor conversation; pricing isn't public, so no real cost figure exists without a sales engagement | Worth a scoping conversation, not something to build against on spec |
| **Facebook Events** | Historically the best source for informal/local "happening tonight" events | N/A | N/A | **[ASSUMPTION, based on Meta's public, well-documented lockdown of the Events Graph API for third-party developers]** — very likely not viable as a general-purpose feed anymore. Consistent with `discovery-engine-spec.md`'s own verdict on the adjacent Instagram/Snap channels ("Share-in only" / "Drop," no crawl path) |
| **Local Israeli ticketing/event platforms** (e.g. the kind of nightlife/party/comedy/tech-meetup listing sites that actually carry Tel Aviv's informal event layer) | Unknown — API availability not confirmed | Unknown | This is very plausibly where the "genuinely alive, not just concerts" layer of events actually lives, but **whether any of them expose a public API at all is unverified this session** — most likely requires either a scraper (fragile, per-source maintenance) or a direct partnership/data-sharing agreement | **Named risk, not resolved** — the single biggest open question in this doc |
| **Municipal / cultural-institution calendars** (Tel Aviv-Yafo municipality culture calendar, museums, Cinematheque, port-area listings) | Public web listings, no confirmed API | High trust, but narrow scope (official/curated only) | Requires scraping/parsing, not a clean feed; each source is its own small maintenance burden | Supplementary — good for the small number of large public happenings, not general coverage |
| **Manual curation** (a human-maintained events calendar) | Not automated ingestion at all | As fresh as the labor put into it | As broad as the labor put into it | Reliable near-term stopgap for the informal layer no API reaches, but this repeats the exact staffing-model tradeoff decision #22 already moved *away* from for localness (cold-start/scaling reasons) — same problem, different pipeline |
| **Crowd-submitted events** (users report events they know about) | Automated collection, manual content | Depends on user participation | Depends on user participation | Inherits the same cold-start risk already flagged for local-QA (decision #24's Key risks: day one of a new city has no users yet to ask) — worth naming as a parallel, not a novel risk |

**The honest coverage gap:** the two real, cheaply-integrable public APIs (Eventbrite, Ticketmaster) together give reliable freshness but skew hard toward *commercial, ticketed* events — concerts, workshops, big shows. The category that would make a "Tel Aviv right now" live-events layer feel genuinely alive rather than "a concert calendar" — informal pop-ups, parties, spontaneous street happenings — is exactly the category Facebook Events used to solve and can no longer be reached through, and the local platforms that might fill that gap have unconfirmed API access. This is not a solvable-by-more-engineering-hours problem; it's a data-access problem, the same shape PAS-7 found for Scenic Walk's attractiveness signal (the algorithm is fine, the input doesn't fully exist yet).

---

## 2. Rough build-cost/timeline

Scoped separately from the synthetic density feed (untouched, not part of this pipeline) and the localness/local-QA pipeline (a different signal, different trigger, not part of this pipeline either).

- **First structured feed integration** (Eventbrite or Ticketmaster, pick one): API integration, mapping each event's venue coordinates to a Hood (depends on Epic C's places/Hoods schema existing first — same sequencing dependency PAS-7 flagged for Scenic Walk; `database/README.md` confirms the schema is still empty, starts at migration `001`), basic dedup, and expiry handling so an event that already ended never shows (`discovery-engine-spec.md`'s Live-layer table names this exact failure mode: "anything expired shows... worse than an empty shelf"). **Roughly 1–2 weeks** of engineering once the Hoods schema exists.
- **Second feed source, to broaden past "just concerts"** (a second ticketed API, and/or a municipal-calendar scraper): each additional source is its own integration, with scraped sources carrying ongoing maintenance burden beyond the initial build. **Roughly 1–2 weeks per additional source**, and this is where the total climbs if V1 needs more than one category of event to feel adequate.
- **The ranking/selection layer** — the part `discovery-engine-spec.md` calls out as "the part nobody does well" and the strategy line explicitly requires ("algorithmically selected... not just a raw feed"). At minimum this needs: event→Hood mapping (shared with ingestion above), a recency/proximity/category scorer, and a review pass to confirm the output doesn't just degrade into "show everything." This is new build, not a byproduct of ingestion — **roughly 1–2 weeks** for a first, simple version (e.g. proximity + recency + category-match scoring, no social-momentum signal yet); a version that actually uses Passenger's own local/tourist signal to weight events (closer to what "algorithmically selected as likely-interesting" implies) is more open-ended and not something to put a firm number on without first knowing which feed(s) are in play.
- **The local-platform / informal-events gap** (the biggest open item in Section 1) is not estimable as engineering hours at all right now — it's either a partnership negotiation (timeline owned by whoever runs that conversation, not data-engineer), a paid vendor evaluation (PredictHQ-style, procurement timeline unknown), or an accepted coverage gap for V1. Any of these could add real time or could add none, depending on which path gets chosen.

**Rough total for a working v1 pipeline** (one ticketed-events feed, mapped to Hoods, with a basic ranking pass): **roughly 3–5 weeks of dedicated data/backend effort**, sequenced after the places/Hoods schema, before any iOS integration on top of it — comparable in shape to PAS-7's Scenic Walk estimate. That figure covers only the commercial/ticketed layer; it does **not** include however long the informal-events gap takes to close, because that path isn't chosen yet.

---

## 3. Explicit call: buildable in Phase 1?

**Conditional — yes for a thin version, no for the fuller version the strategy line implies.**

A single ticketed-events-API integration (Eventbrite and/or Ticketmaster), mapped to Hoods, with a first-pass "likely-interesting" ranking (recency + proximity + category, not yet using Passenger's own local/tourist signal), is realistically buildable inside the Phase 1 window — roughly 3–5 weeks, sequenced after the places/Hoods schema lands, matching the PAS-7 precedent's shape.

What is **not** realistically buildable inside Phase 1 with any confidence right now is the version that actually makes the "something's happening near you right now" promise feel true rather than "here's a concert calendar": that needs either (a) a confirmed API/partnership with a local Israeli events platform (access unverified this session), (b) a paid vendor relationship with an aggregator like PredictHQ (Israel coverage and pricing both unverified, and it's a procurement timeline outside engineering's control), or (c) a manual or crowd-curated layer that repeats a staffing/cold-start tradeoff this team already moved away from for a different pipeline (decision #22) and already has open as an unresolved risk for a related one (decision #24).

This is the same shape of finding PAS-7 landed on for Scenic Walk: the mechanism (ingest-and-rank, not mine-and-infer) is sound and matches Aviran's own pre-existing algorithm design — the risk is a genuine data-access gap, not an engineering-effort gap. **Recommend:** ship the thin ticketed-events version for V1 launch (real, bounded, matches the timeline), explicitly flag to Aviran that it will skew toward commercial/ticketed events rather than informal happenings, and treat closing the informal-events gap (partnership, paid feed, or crowd layer) as a fast-follow decision rather than a Phase 1 blocker — unless Aviran judges the thin version doesn't meet the bar that made this launch-blocking in the first place, in which case the launch-blocking risk is real and the date is genuinely at stake, not a formality.

---

## Summary

| Question | Answer |
|---|---|
| Sourcing options | Eventbrite/Ticketmaster (real APIs, ticketed-events only) · PredictHQ-style aggregator (unverified Israel coverage/cost) · Facebook Events (very likely dead as a feed) · local Israeli platforms (API access unconfirmed — the real gap) · municipal calendars (scraping, narrow) · manual/crowd curation (repeats known staffing/cold-start tradeoffs) |
| Cost/timeline | ~3–5 weeks for a thin, single-feed, ticketed-events v1 with basic ranking, sequenced after the places/Hoods schema. The fuller informal-events version has no reliable estimate yet — depends on a path (partnership/vendor/crowd) not yet chosen. |
| Buildable in Phase 1? | **Conditional.** Yes for the thin ticketed-events version. No, not with confidence, for the fuller "feels genuinely alive" version — that's a data-access gap, not a build-hours gap, and needs an explicit Aviran call on which version actually satisfies why this was made launch-blocking. |
