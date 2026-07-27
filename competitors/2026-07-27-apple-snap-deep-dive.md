# Deep dive — Apple Maps and Snap Map

**Date:** 2026-07-27 · **Companion to:** [2026-07-27-competitive-landscape.md](2026-07-27-competitive-landscape.md)

Why these two and not Google: Google is the known threat and the strategy doc already names it. Apple and Snap are the two that were underweighted. Apple because Passenger is iOS-only and Apple ships to that surface for free. Snap because it already runs a live map with a heat layer at scale, and — this is the finding — it holds the data needed to build Passenger's core differentiator.

Desk research only. No hands-on testing of either product. Israel-specific numbers are thin and flagged where they are.

---

## Part 1 — Apple Maps

### What it is now

| Shipped | When | What |
|---|---|---|
| **Visited Places** | iOS 26 | Opt-in, automatic visit log. No check-ins, no manual tagging. Searchable, shareable. |
| **Suggested Places** | iOS 26.5 | Two recommendations inside the search box, from "what's trending nearby, recent searches, and more". |
| **Guides** | Existing | Publisher-curated place collections that auto-update as places are added. |
| **Look Around** | Existing | Street-level imagery — available broadly in Israel by address. |

| Coming in iOS 27 | What |
|---|---|
| **Local Lists** (US first) | Curated collections of nearby places from what's trending locally — dining, kid-friendly. Explicitly **not tied to individual users** — privacy-preserving aggregate trending. |
| **Trending Restaurants** | A section in the search screen showing top restaurants in the current area. |
| **Suggested Places expansion** | Swipe through more than two suggestions. |
| **Natural-language search for routing** | Query specifics in plain language. |
| **Visited Places + Guides go international** | More countries. |
| **AI Flyover, Parked Car widget, offline improvements, Liquid Glass icon** | Not competitively relevant. |

### The ads decision — and why it matters more than the features

Apple Maps ads launch **summer 2026, US and Canada, iPhone and iPad**. Search results and **Suggested Places** both carry them. Keyword-bidding auction, same shape as App Store Search Ads. Ads are labeled, **no opt-out**, and Apple caps it at a **single ad per search result set**. Privacy framing holds: location data isn't given to advertisers, ad interactions aren't linked to an Apple Account. Prohibited categories at launch include home services, bail bonds, crypto ATMs.

Competitive read: **Apple has now joined Google and Snap in monetizing the discovery surface.** That is the load-bearing fact. As of summer 2026, all three map platforms have a paid relationship with the venues on their maps. None of them can ship a first-class **tourist trap** label without flagging a bidder. The moat argument in the landscape brief was speculative when written; the Apple ads announcement makes it sourced.

Secondary read: ads landing specifically in Suggested Places means Apple's zero-query surface — the one closest to Passenger's — is now partly a paid ranking. Its recommendation quality has a ceiling Passenger does not have.

### Where Apple collides with Passenger V1

| Passenger V1 item | Apple's version | Verdict |
|---|---|---|
| Saved / Visited places | **Visited Places, iOS 26** — automatic, OS-level, opt-in, zero install | Apple wins outright. Passenger's version only earns its place if it is tied to the heat/local layers, not as a standalone list. |
| Tap-zone curated neighborhood blurbs | **Guides** + **Local Lists** (iOS 27) | Apple wins on breadth and freshness-at-scale. Passenger wins only on the localness angle Apple's trending data cannot express. |
| No onboarding, straight to the answer | **Suggested Places** | Converging. Apple gets there with ads in the results; Passenger gets there clean. |
| Scenic View routing | Apple routing + natural-language routing (iOS 27) | Apple wins on turn-by-turn quality. "Interesting streets over fastest path" is the only defensible part. |
| Events overlay | Nothing comparable | Passenger holds this. |
| **Heat / crowd density** | **Nothing. Apple ships no busyness data at all.** | Uncontested. |
| **Local vs. touristy** | **Nothing.** | Uncontested. |
| **Time slider, now → +12h** | **Nothing.** | Uncontested. |

The pattern is clean: **Apple is eating Passenger's supporting features, not its differentiators.** Every uncontested row is one of the three things the landscape brief said to differentiate on. Every contested row is something the brief said not to chase.

The practical consequence is scope, not survival: any V1 feature that Apple ships free at OS level stops being a reason to install Passenger. It can stay in the product as table stakes, but it should stop consuming build time or marketing lines.

### Apple's weaknesses in this fight

- **No busyness data, and no visible path to it.** Apple's discovery signals are trending and search-derived, not occupancy-derived. Nothing in the iOS 27 list points at crowd density. This is the structural gap.
- **Israel is a weak market for Apple Maps specifically.** Reported gaps: no transit data in Israeli cities, thin place data, weaker routing. Community sentiment in Israel treats Google Maps and Waze as the only serious options. Passenger's launch city is one of Apple Maps' weaker cities. **[ASSUMPTION]** that these reports still hold in mid-2026 — they come from forum sentiment and comparison articles, not an audit. Worth ten minutes of hands-on checking before relying on it.
- **Regional constraint that cuts both ways:** Apple, Google and Waze all disabled live traffic data in Israel and Gaza at IDF request. That is traffic, not venue busyness, and it does not obviously extend to popular-times data — but it establishes that live location-derived layers in this region are subject to a security veto. Worth understanding before building the launch density pipeline on any live feed. Not a blocker, a diligence item.
- **US-first rollout.** Local Lists is US-only initially, ads are US/Canada. Israel gets these later, which buys time.
- **Apple does not do opinionated.** Guides are publisher-safe, Local Lists are trending-derived and deliberately not personalized. A negative label like "tourist trap" is off-brand and now off-limits commercially.

### Threat verdict: **high certainty, low lethality**

Apple will keep shipping into this territory every OS cycle, and Passenger cannot outbuild the default app on the platform it lives on. But nothing on the roadmap touches density, localness, or time-scrubbing. Apple's effect on Passenger is to **compress the sellable surface down to the three differentiators** — which is what the strategy already says the product is.

**Watch triggers — any of these changes the assessment:**
1. Apple Maps ships any busyness or crowd signal. This is the one that matters.
2. Local Lists or Suggested Places gains a locals-vs-visitors or neighbourhood-character dimension.
3. Apple Maps ads expand to Israel.
4. Apple Maps place-data quality in Tel Aviv materially improves (a proxy for Apple investing in the market).

---

## Part 2 — Snap Map

### Scale, and the direction it's moving

| Metric | Value | Source date |
|---|---|---|
| Snap Map monthly users | 400M+ | May 2025 |
| Snapchat DAU, global | 483M, **+9M** QoQ | Q1 2026 |
| Snapchat DAU, North America | 92M, **−2M** QoQ | Q1 2026 |
| Snapchat DAU, EU | **−1M** QoQ | Q1 2026 |
| Revenue | $1,529M, +12% YoY | Q1 2026 |
| Net loss | $89M (improved from $140M) | Q1 2026 |
| Snapchat ad reach, **Israel** | ~16% of population 18+ | 2024 |

Read: Snap is growing in aggregate but **shrinking in its two richest markets**, and monetizing harder to compensate. Promoted Places is part of that compensation. A company under that pressure ships more monetization into the map, not less.

The Israel number is the important one for Phase 1. **~16% adult reach in 2024** makes Snap Map a marginal presence in Tel Aviv compared to its position in the US or the Gulf. **[ASSUMPTION]** that this hasn't shifted much by 2026 — it's a two-year-old figure and Israel-specific 2026 data was behind a paywall.

### What Snap Map actually does

| Feature | Mechanics |
|---|---|
| **Heat map / Explore layer** | Colour-coded intensity zones at city scale, warmest = most concentrated activity. **The signal is Snapchat posting activity, not venue occupancy.** |
| **My Places / Visited** | Tag, check in, save; a Visited tab. |
| **Footsteps** | Location-history travel tracker. Reports "you've explored 30.4% of your city", country counts. Seeds from Memories on first use, then location-only. Private, deletable, requires Ghost Mode off. |
| **Place Loyalty** (Apr 2026) | Gold = top 1% of a venue's visitors over the past year, silver = top 10%, bronze = top 25%. Aggregated across locations for chains. Requires sharing location. **Private by default**, shareable by choice. |
| **Promoted Places** (May 2026) | Sponsored pins with optional 3D animations. Tap opens a Place Profile labeled "Sponsored" with a Snap Ad, Business Profile carousel, custom Map Effect, save-for-later. Place Partnerships lets brands without retail piggyback on partners with 200+ locations. Metrics: impressions, place opens, aggregated actions. |
| **Context Cards** | Historically powered by Foursquare place data. No evidence Foursquare powers the heat layer. |

### The finding: Snap can compute localness today

Passenger's differentiator is a per-place answer to "are the people here locals or visitors?"

Snap already holds every input:
- **Home region** — implicit in a user's normal location pattern.
- **Travel state** — Footsteps explicitly models "you are away from your city", down to percentage-of-city-explored.
- **Per-venue visitor ranking** — Place Loyalty already ranks each user against every other visitor to a venue over a rolling year.

Place Loyalty is, functionally, a locals-vs-visitors computation that Snap ships to the individual as a badge instead of to the map as a layer. Turning it into "this venue is 80% locals / 80% visitors" is a **product decision, not a data-acquisition problem**. That is a shorter path to Passenger's core differentiator than Google's — Google would derive it from Timeline home locations, which is one more inference step away.

This is the sharpest single competitive fact in either brief.

### Why Snap probably won't

- **Promoted Places is the direct conflict.** Snap now sells sponsored pins on the map. A "mostly tourists" or "tourist trap" label devalues the exact inventory it is selling. This is the same structural block that applies to Apple and Google, and Snap shipped its version most recently and most aggressively.
- **The heat layer measures the wrong thing and Snap is fine with that.** Snap activity ≠ occupancy. Snap has no incentive to fix that, because the signal it measures is engagement with Snap, which is what it monetizes.
- **Audience mismatch.** Snapchat skews 18–24. Passenger's user is anyone who just landed, of any age.
- **Privacy posture.** Place Loyalty rankings are private by default. Publishing an aggregate visitor-origin layer per venue is a materially different privacy decision from a private personal badge, and Snap frames all of these features as personal-and-private.

### Where Snap collides with Passenger

| Passenger item | Snap's version | Verdict |
|---|---|---|
| Heat layer | Explore layer heat map, at scale, since 2021 | Snap has the rendering and the scale. Different underlying signal — arguably a worse proxy for "is this place packed", but it looks the same to a user. |
| Saved / Visited | My Places, Visited tab, Footsteps | Snap wins, and Footsteps is a better-designed version of "places I've been" than anything in V1. |
| **Points system (Passenger Phase 3)** | **Place Loyalty, shipped April 2026** | Snap already shipped the mechanic Passenger deferred by two phases. |
| Localness | Nothing shipped — but see above | Uncontested **today**, and Snap is one product decision from contesting it. |
| Time slider | Nothing | Uncontested. |
| Tourist trap label | Nothing, and structurally blocked | Uncontested. |
| Curated blurbs, events, routing | Weak / absent | Passenger holds these. |

### What to take from Snap, not fear about it

1. **Place Loyalty is a working answer to V1's incentive gap.** V1 has crowdsourced local QA with no reward layer until Phase 3, and the strategy names this as a top risk. Snap's badge tiers cost nothing to compute, need no currency, no store, no points economy — just a ranking users can see and choose to share. A "you're a top-x% local here, is this place actually local?" prompt is a plausible V1-scale incentive that doesn't require pulling the whole Phase 3 points system forward. **This is worth a product exploration, not a decision here** — it needs a check against the no-social-features rule, since a shareable badge edges toward social.
2. **Footsteps proves people opt into passive location history for a self-directed reward** — percentage-of-city-explored, no social element required. Directly relevant to V1's Visited Places and to whether crowdsourced QA prompts will get answered at all.
3. **Heat-at-city-scale is a solved rendering problem.** Snap has run colour-coded intensity zones since 2021. Consistent with the continuous-gradient direction already logged in `feature-inspiration.md`.

### Threat verdict: **low in Tel Aviv, high if Passenger expands**

For Phase 1: **not a threat.** ~16% adult reach in Israel, wrong age skew, no localness layer shipped. Snap Map is not what a tourist landing in Tel Aviv opens.

For Phase 3 (second city, especially US or Gulf): **the most dangerous player on the board**, because it has the data, the map, the scale, and a demonstrated willingness to ship map features every quarter. Only its ad model stands in the way, and ad models change.

**Watch triggers:**
1. Any aggregate visitor-origin or locals-vs-visitors signal surfacing on Snap Map. Highest-priority signal in this brief.
2. Place Loyalty going from private badge to public venue-level statistic.
3. The heat layer shifting from Snap-activity to a real occupancy signal.
4. Promoted Places expanding to Israel (indicates Snap is investing in the market).
5. Any Snap Map feature aimed at travellers rather than friends.

---

## Head-to-head

| | Apple Maps | Snap Map |
|---|---|---|
| Threat timing | **Now, every OS cycle** | Phase 3 and beyond |
| Threat to the *core bet* | Low — no density, no localness, no time axis | **High — holds the inputs for localness today** |
| Threat to *V1 scope* | **High** — makes Saved/Visited, blurbs, routing non-differentiating | Low |
| Relevance in Tel Aviv | Moderate — default app, but weak local data | Low — ~16% adult reach |
| Blocked from the tourist-trap position by | Maps ads, summer 2026 | Promoted Places, May 2026 |
| What Passenger should do | Cut or de-emphasize what Apple gives free | Study the incentive design; watch the locals signal |

## Recommendations

1. **Treat Apple as a scope forcing-function, not a threat.** Anything iOS ships free stops being a reason to install Passenger. Concretely: Saved/Visited should not get differentiating build effort or a marketing line, and Scenic View's case weakens further — Apple is adding natural-language routing in the same cycle.
2. **Raise "any busyness signal from Apple" to the top of the watch list.** It is the single event that would put Apple in the core lane, and there is currently no sign of it. Cheap to monitor: one check per OS beta.
3. **Take the moat argument as sourced, and use it.** All three platforms now monetize their maps. The tourist-trap label is a position they are commercially blocked from taking. This belongs in the positioning line and in any investor conversation.
4. **Explore a Place-Loyalty-shaped incentive for V1's local QA** — a visible, private, computed standing rather than a points economy. Must be checked against the no-social-features rule before it becomes a PRD.
5. **Verify the Israel assumptions before they carry weight.** Two load-bearing claims here are soft: Apple Maps' place-data weakness in Tel Aviv (forum sentiment) and Snapchat's ~16% Israeli reach (2024 figure). Both are checkable — the first by opening Apple Maps in Tel Aviv for ten minutes, the second by a current DataReportal or Statista pull.

---

## Sources

**Apple:** [iOS 27 Maps features, MacRumors](https://www.macrumors.com/2026/06/11/apple-maps-to-get-these-10-new-features-in-ios-27/) · [iOS 27 Maps guide, MacRumors](https://www.macrumors.com/guide/ios-27-maps/) · [Local Lists, Android Headlines](https://www.androidheadlines.com/2026/06/apple-maps-ios-27-ai-flyover-local-lists.html) · [Suggested Places, 9to5Mac](https://9to5mac.com/2026/03/30/ios-26-5-adds-new-apple-maps-feature-for-trending-places/) · [Visited Places, Gadget Hacks](https://apple.gadgethacks.com/news/apple-maps-visited-places-in-ios-26-what-it-does-and-how-it-works/) · [Maps ads, MacRumors](https://www.macrumors.com/2026/04/24/apple-maps-ads-what-to-expect/) · [Ad category bans, TechCrunch](https://techcrunch.com/2026/07/15/apple-quietly-reveals-how-its-maps-ads-will-differ-from-googles/) · [Apple vs Google Maps share](https://scrap.io/google-maps-vs-apple-maps-vs-waze-navigation-app-comparison) · [Israel traffic-data disabling, GovTech](https://www.govtech.com/question-of-the-day/why-have-apple-and-google-disabled-map-features-in-israel-and-gaza)

**Snap:** [Q1 2026 results, Snap IR](https://investor.snap.com/news/news-details/2026/Snap-Inc--Announces-First-Quarter-2026-Financial-Results/default.aspx) · [Q1 usage decline, Social Media Today](https://www.socialmediatoday.com/news/snapchat-usage-declined-in-the-us-and-eu-in-q1/819535/) · [Snap Map 400M MAU, TechCrunch](https://techcrunch.com/2025/05/07/snap-map-reaches-new-milestone-of-400m-monthly-active-users) · [Place Loyalty, TechCrunch](https://techcrunch.com/2026/04/22/snap-maps-new-place-loyalty-badges-will-show-the-spots-you-visit-most-often/) · [Promoted Places, Campaign Middle East](https://campaignme.com/snap-launches-promoted-places-transforming-the-snap-map-into-real-world-discovery/) · [Footsteps, TechCrunch](https://techcrunch.com/2024/09/30/snapchats-new-footsteps-feature-tracks-your-location-history) · [Map layers, Snapchat Support](https://help.snapchat.com/hc/en-us/articles/7012293543572-How-to-Toggle-Between-Different-Map-Layers-on-Snap-Map) · [Israel ad reach 2024, Statista](https://www.statista.com/statistics/1318634/snapchat-s-potential-advertising-reach-in-israel/)
