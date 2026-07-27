# Passenger V1 — Decision Record

**Status:** Locked (grilled with Aviran, 2026-07-22)
**Owner:** Aviran Grisaro
**Source brief:** Passenger Product Brief (V1 / V1.5 / V2, iOS only)
**Linear:** superseded — this record predates the 2026-07-26 reset. The original issues (LOC-79 … LOC-99) live in the archived `locali-app` workspace; current work is in workspace `passenger`, team `PAS`, project **Passenger V1**.

> **Amended 2026-07-26 — the reset.** Decision #1 is **reversed**: Passenger is a greenfield build, not a repositioning. The Locali codebase was frozen (`github.com/AviranGrisaro/locali`) and `passenger-code` started from an empty Xcode project. Reason: ten of the 27 PRDs built against that codebase specified features the strategy forbids, and the drift was structural rather than cosmetic — a god object plus two god views, wired through a social layer that was never supposed to exist.
>
> Knock-on effects on the rows below: **#3** no longer means "flag off" — the social code isn't in the new repo at all, and `FeatureFlags.swift` doesn't exist. **#5** is superseded by the strategy's current line — localness is "algorithm plus local QA, together," crowdsourced from users, not hand-curated by a curator. **#15** is executed as of this date.
>
> Every other row still stands. The rows are kept verbatim as the record of what was decided when; read this note first.

## What this is

Passenger is a **repositioning of the existing `locali-code` app**, not a greenfield build. The brief's V1 (interactive map, now→+12h time slider, density heatmap, tap-a-zone, native-maps hand-off, two categories) is ~70% already built. This project captures the **delta** work to refocus Locali into the tourist "you just landed, immediately know where the locals are" product — and to rebrand it to **Passenger**.

Locali's own strategy was already tourist-first ("where should I walk right now to find the real local vibe?"). What drifted is the *code* — it accreted friends, live-presence, and fog-of-war exploration that appear in neither the strategy nor the brief. Passenger refocuses back to the core.

## Locked decisions

| # | Decision | Notes |
|---|---|---|
| 1 | Reposition existing `locali-code`, not greenfield | — |
| 2 | Map encodes **two orthogonal layers**: heat = crowd density, tag = localness | Packed ≠ good; the tourist trap is the packed-touristy spot. The whole differentiator. |
| 3 | Social layer (friends, live-presence, fog-of-war) → **flag off, not delete** | Off through V2 — no "preserved for V1.5/V2" framing; any return is an undecided future call, beyond V2. Uses FeatureFlags.swift. Superseded by strategy's "No social. No B2B. Full stop." (2026-07-23, direct from Aviran). |
| 4 | Density = external popular-times provider (**TBD spike**); ship a **synthetic feed** for now, **time-bound to the slider hour** | First-party presence deferred (empty at launch). |
| 5 | Localness = **hand-curated for V1**; scraping/algo = **parallel gated spike** | The curator IS the definition of "local" for V1. Algo must beat the hand-curated rank-order before it ships. |
| 6 | Vibe tags (5): **super local · very local · mixed · touristy · tourist trap** | "Tourist trap" is an addition beyond the brief's 4 named. |
| 7 | Launch **Tel Aviv only**; foreign city = fast-follow | Portability proof → existing Multi-City Expansion project. |
| 8 | Cold-open **straight to Tel Aviv map** — no sign-in, no onboarding, no permission gate; lazy location; fading "Tel Aviv, right now" title | — |
| 9 | **Free V1**, monetization deferred (RevenueCat dormant) | Paywall is a later phase with real city coverage. Reconfirmed directly by Aviran, 2026-07-26: no paywall/unlock/trial gate anywhere in Phase 1; subscription (not per-city) introduced starting Phase 2. |
| 10 | "Local read" on tap = **hand-curated neighborhood blurb** | — |
| 11 | **Exactly two categories**: Food & drinks / Things to do | — |
| 12 | Localness granularity = **neighborhood + spot** | Bounded curation: dozens of neighborhoods + key spots, not every hex cell. |
| 13 | Hero screen = **density heat base + localness accent + tap-to-read** | — |
| 14 | **Keep events as a live layer** — reconciled as a time-sensitive overlay on the slider, NOT a third category | Deviation from brief. Watch-item. |
| 15 | **Rebrand Locali → Passenger** | Wordmark, app name, icon, App Store identity. |
| 16 | **Keep Saved + Visited places**; strip only V1.5 target-proximity geofencing | Deviation from brief ("saved lists out of scope"). Visited populates only after lazy location grant. CityGeofenceMonitor stays. |
| 17 | **No gradients anywhere** — heat = stepped bands / flat cells | Supersedes T-024 gradient-heatmap request. |
| 18 | Vibe tags (3): **Local · Mix · Tourist** | 2026-07-27, direct from Aviran. **Supersedes #6.** No dedicated "tourist trap" tag — packed-and-touristy reads off heat + tag together instead of getting its own label. |
| 19 | **Scenic View moves to Phase 2.** V1 tap-a-spot hands off to native Maps/Waze | 2026-07-27, direct from Aviran. No in-app routing in the launch build. Removes routing-engine scope from V1; the cost moves to Phase 2, it doesn't disappear. |
| 20 | **Events overlay moves to Phase 2** | 2026-07-27, direct from Aviran. **Supersedes #14.** V1 map is heat + tag only — two layers, matching the north star exactly. |
| 21 | **Phase 2 additions are subscription-gated** — proximity intelligence, Scenic View, Live Events | 2026-07-27, direct from Aviran. Free core is permanently the V1 scope: heat + tag, both categories, slider, zone/spot detail, Saved/Visited, native hand-off. Consistent with #9 (Phase 1 fully free). |
| 22 | **Localness = algorithm + crowdsourced local QA**, together, as the permanent pipeline | 2026-07-27, confirmed by Aviran. **Supersedes #5** — the curator is not the definition of "local" for V1. Real users are asked in-app whether a spot is actually local; the algorithm proposes, they verify and correct. Trades staffing risk for cold-start and incentive risk (no reward layer until Phase 3's points system). |
| 24 | **Local-QA is asked by a post-visit toast**, fired by a local notification | 2026-07-27, direct from Aviran. Geofence detects the visit; an iOS **local** notification fires while backgrounded; opening it drops a toast from the top of the screen asking whether the place felt local or touristy. Chosen over waiting for the next app open, so the ask lands while the memory is fresh. **Two costs to watch:** it adds a *second* permission prompt to V1 on top of location, which sits awkwardly with #8's "no permission gate" cold open; and it is the first notification of any kind in V1, so the "no push" shorthand in the business-model section no longer reads literally — the habit-loop argument for freemium still stands, a post-visit question is not re-engagement. |
| 25 | **Category chips move into the search sheet** — off the map chrome | 2026-07-27, direct from Aviran. Chips drop from Primary to inside search. One fewer permanent control on the map, consistent with moving spot-level tags off the map surface entirely (see `design/map-rendering-spec.md`). **Cost:** filtering by category while casually browsing now costs an extra tap, since it means opening search first. Supersedes the always-visible-chip assumption in `design/ux-flows.md`. |
| 23 | **Search ships in V1** — place names, keywords, and neighborhoods | 2026-07-27, direct from Aviran. Reached from an icon in the map chrome, opens as a sheet over the map — Secondary tier, not persistent chrome, so the map stays the default answer. Results carry heat + tag and honor the slider hour. Softens, but does not void, the "no query" positioning line: search is for when you already have somewhere in mind. **Watch-item** — if users reach for search before reading the map, that's a signal the map isn't working. |

## Knowing deviations from the brief

- ~~**Events kept**~~ — reversed by #20. Events is Phase 2; V1 is back to the brief's two-layer map.
- **Saved + Visited kept** (brief: saved lists out of scope for V1).
- ~~**"Tourist trap"** tag added~~ — reversed by #18. Down to three tags, fewer than the brief's four.
- **V1 does not live-scrape** — the "from TikTok / local-language" north star is delivered in V1 by the algorithm-plus-crowdsourced-QA pipeline (#22), not by live scraping; the scraping pipeline is the C4 spike.

## Critical path

C4 (localness algo) is the risk and a gate — but a research track, not a V1 blocker. C1 (synthetic density) + B1 (design) start day 1 in parallel. Epic A (shell) can start immediately (our own code). B3–B5 join on C1 + C3. Design unblocks build flow-by-flow.

## Ticket map (LOC team)

- **Epic A — Shell** (LOC-79): A1 cold-open (LOC-83) · A2 flag-off social + V1.5 proximity (LOC-84) · A3 two categories (LOC-85) · A4 rebrand (LOC-86) · A5 supersede T-024 (LOC-87)
- **Epic B — Two-layer map** (LOC-80): B1 tag+non-gradient design (LOC-88) · B2 hero flow (LOC-89) · B3 accent + tap-zoom (LOC-90) · B4 blurb + tagged spots (LOC-91) · B5 spot tag + hand-off (LOC-92)
- **Epic C — Data** (LOC-81): C1 synthetic density + contract (LOC-93) · C2 provider spike (LOC-94) · C3 hand-curated localness (LOC-95) · C4 define-local spike+gate (LOC-96) · C5 events overlay (LOC-97)
- **Epic D — Validate** (LOC-82): D1 QA acceptance (LOC-98) · D2 success metric (LOC-99)

## Related existing Linear projects

- **Flag off / de-scope for V1:** Follow Friends & Locations, Onboarding Flow, Auth & Login, Live Heatmap (cross-user aggregation).
- **Reuse:** Map Screen, Heatmap & Live Events.
- **Defer, keep dormant:** Paywall & Monetization.
- **Foreign fast-follow:** Multi-City Expansion.
