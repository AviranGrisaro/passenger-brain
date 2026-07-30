# Discovery engine: turning social travel content into time-aware recommendations

**Status:** Draft for review (working spec v0.1)
**Owner:** Aviran
**For:** Yeari
**Date:** 2026-07-27
**Provenance:** Written by Aviran directly as a Claude Artifact, never previously saved into this repo — recovered 2026-07-30 and pulled into `data-eng/` so `data-engineer` can actually reference it. Predates the 2026-07-29 founders meeting and the 2026-07-30 lock; read alongside `strategy/decisions.md` (especially #22, #28/#37, #34/#45) and `data-eng/tourist-trap-algorithm-rescope.md` — this spec is the detailed algorithm-design thinking behind that lighter rescope note, not a replacement for it.

We are not building a place directory. We are answering "where should I be, and when" — a neighborhood in the morning, a beach at sunset. This doc is a starting point for discussion, not a decided design.

---

## What we're building

A per-city index of **experiences** — an area, a time of day, and an activity — mined from social content, blogs and forums, then ranked by how credible and how current the recommendation is.

The output is not an address. "Trastevere, early morning, wander and coffee" is a record. "Via del Moro 12" is not. This matters technically as much as it does for the product: matching a caption to a neighborhood polygon is a far easier and far more durable problem than matching it to a specific business. Neighborhoods don't close down, don't get renamed, and aren't covered by anyone's map-data licensing terms.

### Explicit non-goals

- *Storing or maintaining* booking, menus and prices. Permanently commoditised, and a maintenance treadmill where users blame us for errors that originate in someone else's feed. Opening hours are the exception — we read them from Apple Maps at request time, as a filter, and never persist them. See R8.
- A complete POI database. We *do* recommend specific venues — see Venues below — but always as options hanging off an experience, never as a standalone directory.
- Coverage breadth. Better to have five cities that feel alive than fifty stale directories.

---

## The record

Every record is a triple. This is the whole data model and everything else hangs off it.

```
Experience
  where      geo shape — neighborhood, coastline, market street, viewpoint
  when       time-of-day bucket + day-of-week + season
  what       activity / mood

  conviction     0–1, from independent corroborating sources
  local_score    0–1, weight of local-classed authors
  tourist_score  0–1, weight of visitor-classed authors
  momentum       trailing mention rate vs. city baseline
  sources[]      each with publish_date, capture_date, author_class
  venues[]       optional — specific places inside this experience

Venue — a leaf on an Experience, never a top-level record
  quality_conf   0–1, slow decay — is it any good
  exists_conf    resolved at read time, never stored — is it still open
  opened_est     estimated opening date, triggers the new-place rule
  sources[]      same shape, plus per-author reliability weight
```

Note that "North Beach / sunset / swim" and "North Beach / midday / crowded, skip it" are two separate records over the same geography, and one of them is a negative recommendation. That falls out of the schema for free and it wouldn't from a place list.

**Polygons.** Overture and OpenStreetMap give us named neighborhoods, but coverage is patchy and informal areas — "the quiet end", "behind the station" — aren't in there. Our team draws those by hand during seeding. That hand-drawn polygon set is proprietary data nobody else has, which is a better asset than another restaurant list.

---

## Sources and how we get them

Half of the obvious source list is not legally reachable. Worth agreeing on this before anyone builds a crawler.

| Source | Verdict | Notes |
|---|---|---|
| Reddit | **Core** | Real paid API. Best signal-to-noise on the list, and timestamped history we can backfill. |
| Overture / OSM | **Core** | Open license, storable. Our base geography layer. |
| Blogs | **Filtered** | Crawlable, but a large share of recent travel blogging is AI listicle filler. Needs an aggressive quality gate or it poisons the index. |
| TikTok | **Share-in only** | Research API is academic-gated; Display API is own-content only. No crawl path exists. |
| Instagram | **Share-in only** | Graph API is limited to owned accounts. Hashtag discovery effectively dead. |
| Google Places | **Read-time only** | Usable to validate, e.g. is this venue still open. Terms prohibit using it to build a competing dataset, so it can never be our index. |
| Apple Maps | **Read-time only** | Same posture as Google. |
| Snap | **Drop** | No API. No extraction path. |
| Other travel apps | **Drop** | Scraping competitors is brittle and legally hostile. |

### The way around the TikTok problem

We don't crawl it — users bring it to us. They see a video, hit share, our app resolves it. That is user-supplied content rather than scraped content, which is a completely different legal position, and it needs almost no crawling infrastructure. It also gives us a growth loop, since the user's saved list becomes their reason to come back.

**Note, 2026-07-30:** this is exactly the mechanism behind decision #34/#45's "TikTok import" V1 feature — save a video into the app, extract places, add to Saved Places. This spec is the original design rationale for why share-in (not crawling) is the only legally viable path; read the two together.

---

## Pipeline

Per item, in order.

1. **Ingest** — Share-sheet hand-off, Reddit API pull, or blog crawl. Store the raw item plus its platform metadata.
2. **Extract** — Transcript, on-screen text via OCR, caption, and top comments. Comments matter — the "what's this place called" reply is often where the answer actually lives.
3. **Date** — Resolve publish date and estimate capture date. These are different fields and are used for different things (see below).
4. **Read the frames** — A vision pass on sampled frames classifies time of day, season, weather and crowd level. This is our primary source for the *when* field, because people film at sunset without ever writing the word.
5. **Resolve geography** — Match to a polygon in our geo layer. Candidate generation by bounding box and fuzzy name, then a rerank using context from the extraction.
6. **Classify the author** — Local, long-stay, or visitor. Details below.
7. **Merge** — Attach as a source to an existing Experience record, or create a new one. Recompute that record's scores.

### How the "when" field actually gets filled

Almost nobody writes "go in the morning". They just film in the morning. So the frames are the primary source and the caption is corroboration, not the other way round — that inversion is the whole trick and it's what lets us build a time-aware index out of content that was never tagged with times.

The three parts of *when* are not equally easy, though, and we shouldn't pretend otherwise:

- **Time of day** — reliable from vision. Light angle, colour temperature, shadow length, artificial lighting, how many shutters are open. Bucket it (dawn, morning, midday, afternoon, golden hour, night) rather than predicting a clock time.
- **Season** — reliable from vision. Foliage, clothing, snow, daylight length, decorations, crowd density.
- **Weekday vs. weekend** — *not* reliable from vision, and this is the one to be careful about. A Tuesday market and a Sunday market look identical in a frame. Get it from explicit text where it exists ("Sunday flea market"), from venue opening hours where we have them, and otherwise from the aggregate: if mentions of a place cluster on particular days across many posts, that's a weekend pattern. Treat a single video as near-zero evidence for this field.

Every inferred value carries a confidence score, and low-confidence values do not get used as a hard filter — see R1. If we don't know when a place is good, it competes on the general shelf rather than being wrongly excluded from the morning one.

---

## Two dates, not one

They diverge constantly — reposts, compilations, nostalgia posts — and confusing them is how the trending shelf fills up with ghosts.

- **Publish date** drives momentum. A video posted last week counts as a signal last week.
- **Capture date** drives seasonality and validity. A video shot in 2021 tells us nothing about what's rising now, and a snow-covered street tells us nothing about August.

Platforms strip most capture metadata, so we infer it from what's in the frames — foliage, crowd density, clothing, decorations — and carry a confidence value. Where confidence is low, treat publish date as an upper bound only.

---

## Who is talking: local, long-stay, visitor

The strongest signal by a wide margin is **how a poster's history is spread over time**. A visitor produces a four-day burst from one city and never posts from there again. A local posts from that city across months and seasons. That one feature does most of the work and needs no clever modeling.

Supporting signals, in rough order of usefulness: posting language, presence of mundane non-touristy content, bio self-declaration, and how much their mentions overlap with the tourist canon. If someone's entire location history is landmark-tier, they are a visitor whatever the bio says.

### The class we should weight highest is not "local"

Locals know daily life but have stopped seeing their own city, so they're weak at knowing what an outsider would find remarkable. Visitors are useful for logistics — queue length, is it worth the trip — and weak at discovery. The **long-stay resident or repeat visitor** has both: local knowledge plus a working memory of what's striking. That's precisely our use case, and almost nobody targets that band on purpose.

### Keep the two scores apart

Store `local_score` and `tourist_score` separately and never blend them, because the gap between them is the signal. High local with near-zero tourist is a genuine find. High tourist with zero local is a tourist trap. Collapse them into one number and we lose the only interesting thing we know.

**Note, 2026-07-30:** decision #37 confirms the *product surface* collapses this into a boolean tourist-trap flag (no graduated Local/Mix/Tourist read shown to the user) — but this spec's underlying `local_score`/`tourist_score` separation is about the *algorithm's internal model*, not the UI. The two scores likely still need to stay separate internally even if the flag exposed to users is binary; `tourist-trap-algorithm-rescope.md` covers the UI-facing implication, this section covers the modeling rationale underneath it. Worth reconciling explicitly when the algorithm actually gets built — don't assume the boolean flag means the internal scoring collapses too.

---

## Three layers, three clocks

Same record type underneath, three separate scoring passes on different refresh cycles.

| Layer | Clock | Score | Fails when |
|---|---|---|---|
| Baseline | Quarterly | Conviction across independent sources, slow recency decay, local weighting. | It churns for no reason. If a canon entry moves week to week, the decay is too fast. |
| Rising | Weekly | Mention rate over a trailing window vs. that record's own history and the city baseline. | Small-count noise. Going from one mention to three is a 200% rise and means nothing. |
| Live | Daily | Dated events plus time-bound conditions — festival, season, tide, today's sunset time. | Anything expired shows. A concert that already happened is worse than an empty shelf. |

### Rising has the longest cold start, not the shortest

Velocity needs history — we can't call something rising until we know what normal looks like. The team can hand-seed the baseline in a couple of weeks; nobody can hand-seed a baseline distribution. The way out is Reddit specifically: its API returns timestamped historical posts, so we can pull two years of the city subreddits and reconstruct a mention timeline *backwards* on day one. TikTok and Instagram can't do that for us, which is another reason Reddit is the spine of the momentum layer.

On the math: use a test that accounts for how noisy low counts are — Poisson or beta-binomial rather than a raw ratio. Rising is the shelf where a bad call is most visible, so an honest four entries beats a padded twenty.

### Live events are a feed problem, not a mining problem

Events have structured fields — start, end, venue, price, ticket link — and ticketing platforms, venue calendars and tourism boards already publish them cleanly. Mining them out of social posts is hard work for a worse result. Ingest events from feeds, and use our social signal only to *rank* which ones a given user should care about. That ranking is the part nobody does well.

**Note, 2026-07-30:** directly relevant to the V1 Live Events overlay (PAS-5, launch-blocking) — this section's "feed problem, not mining problem" framing plus the ranking-not-raw-feed direction matches strategy.md's V1 scope line ("algorithmically selected as likely-interesting to the user, not just a raw feed of every event"). Worth handing to whoever scopes PAS-5.

---

## Venues, and why "newly opened" is the sharpest case

We do want to recommend specific restaurants, bars and shops. Two reasons. Food is consumed three times a day where an experience is consumed once, so it's the difference between an app opened twice a trip and the habit for the whole trip. And a very large share of the social content we ingest *is* food — refusing to resolve it means discarding most of what we collect.

### The gap in the incumbents

Google and TripAdvisor are structurally unable to surface a restaurant that opened six weeks ago, because their ranking runs on accumulated review volume. A new place has eleven reviews and sits on page four regardless of quality, and it stays there for a year. That's a permanent architectural gap, not an execution gap we'd have to out-run them on.

A newly opened venue is also the cleanest momentum signal that exists — no baseline, no history, then a sudden cluster of mentions. This isn't a departure from the three-layer design. It's the best demonstration of why the rising layer is there.

### Venue as payload, not as a parallel list

"Trastevere, dinner, evening" is the record. Three specific restaurants hang off it as options. The area and the time are the durable spine; the venues are the perishable leaves.

That structure buys **graceful degradation**, which is the real reason to do it this way. Restaurants close constantly — it's the highest-churn category in the product. Send a user to a shuttered restaurant and they never trust the app again. Send them to a neighborhood where one of three options has closed and they barely notice. The experience layer is what makes venue staleness survivable.

### The scoring problem this creates

Our conviction score rewards corroboration across independent sources. A restaurant open for one month has no corroboration by definition, so it scores near zero — meaning the rising layer would suppress exactly the thing it exists to find.

So new venues score on a different rule: **source credibility replaces source count**. One trusted local food account with a track record of being right outweighs five anonymous mentions. That requires per-author reliability tracking, which is the single most expensive thing in this document and is called out as an open question below.

---

## Rules we shouldn't break

| # | Rule |
|---|---|
| R1 | **Time fit is a hard filter, not a weight.** A sunset spot never surfaces at 9am, however high it scores. Breaking this once undermines the entire premise of the product. Applies to confident time values only — an unknown *when* is never grounds for exclusion. |
| R2 | **Never rank by raw mention volume.** That rebuilds TripAdvisor and surfaces tourist traps. Volume is popularity, not quality. |
| R3 | **Momentum uses publish date. Seasonality uses capture date.** Never mix them. |
| R4 | **Local and tourist scores stay separate.** The divergence is the product. |
| R5 | **Nothing derived from Google or Apple map data enters the stored index.** Read-time validation only. |
| R6 | **Every manual resolution gets logged as a labeled pair** — including rejects and near-misses. This is our eval set for the automated resolver later, and most teams throw it away. |
| R7 | **A venue is always a leaf on an Experience, never a top-level record.** This is what guarantees graceful degradation when a venue closes. |
| R8 | **Existence and opening hours are read from Apple Maps at request time and never persisted.** Consistent with R5 — it's validation, not indexing. "Closed right now" hard-excludes the *venue*; it never excludes the parent experience, because a neighborhood has no opening hours and a viewpoint at sunrise has no door. |
| R9 | **New venues are scored on author credibility, not source count.** Applying the normal conviction rule to a place that opened last month suppresses precisely what the rising layer exists to find. |

One caveat on R8 worth stating explicitly: hours data across every provider is unreliable around holidays, seasonal changes and temporary closures. Treat "closed" as a strong exclusion, but never present "open" to the user as a promise.

**Note, 2026-07-30:** R8's closed-venue exclusion is a different mechanism from decision #38's "permanently closed" Saved-place badge — R8 is about the discovery/ranking algorithm never surfacing a closed venue as a *recommendation*; decision #38 is about what happens when a user *manually saves* a place Apple Maps already marks permanently closed. Not a conflict, just two different surfaces touching the same "closed" concept — worth keeping straight when either gets built.

---

## Cold start

The team seeds by hand. Because an experience covers an area and a time slot rather than a single venue, roughly 50–80 records makes a city feel complete — a week or two of work per city, not months.

Two things to get right while seeding. First, the hand-drawn polygons for informal areas, which become permanent proprietary geography. Second, the labeled pairs from rule R6, which are the only way we'll ever know whether the automated resolver is any good.

---

## Assume the rising shelf gets gamed

The moment a venue learns that twenty TikToks puts them on "trending in Barcelona", twenty TikToks becomes a cheap marketing spend. Build in independent-author diversity requirements, account-age checks, and cross-source corroboration now — retrofitting anti-gaming after the first incident is much harder than designing for it.

---

## Open questions

- **How many cities do we intend to keep hot?** Baseline is a one-time cost per city. Rising and live are permanent ongoing ingest per city, forever. That's the real constraint on the business model.
- **Three layers in the app — three tabs, or one ranked answer?** All three answer the same question: what should I do, here, now. Three tabs pushes the job of knowing which tab to check onto the user. Argument for keeping three pipelines underneath but merging the surface, with a badge showing why something appeared.
- **How do we handle negative records in the UI?** "Skip the south side at midday" is genuinely valuable and nobody publishes it, but it's also the fastest way to get complaints from a business.
- **What's the minimum viable author classifier?** Posting-history spread needs profile history access, which varies by source. Do we ship with a weaker heuristic for share-ins and improve later?
- **Per-author reliability tracking — is it in v1 or not?** R9 depends on it, and R9 is what makes new venues work at all. But it's the most expensive item in this document: it needs an author identity store, an outcome signal to learn from, and enough time for a track record to accumulate. There may be a cheap proxy for v1 — follower count and topical consistency rather than measured accuracy — but that's a guess about credibility, not a measurement of it.
- **What does read-time Apple Maps lookup cost us at scale?** R8 puts a third-party call on the render path for every venue we show. MapKit quotas are tied to the developer account and we'd be hitting it on every session, not every save. Needs a rough volume estimate before we commit to it architecturally, plus a decision on what the UI does when the lookup fails or times out.

---

Draft for discussion — nothing here is decided.
