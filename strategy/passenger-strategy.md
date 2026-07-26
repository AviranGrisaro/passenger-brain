# Passenger Strategy

**Owner:** Aviran Grisaro
**Last updated:** 2026-07-23
**Related:** [V1 decision record](decisions.md) · [North star](passenger-north-star.html)

## North star

**Land like a tourist. Move like a local.**

Where to go right now — not what a guidebook says.

**Right now, finding out what's good means scrolling TikTok, blogs, Instagram — then saving it to Google Maps, showing up, and finding half of it closed.**

That's not a discovery problem. It's a freshness problem — everything's frozen the second it's posted.

Passenger's bet: one live map instead of five stale sources. Heat shows what's packed right now. Tag shows what's actually local. Packed doesn't mean good — packed and touristy is the trap. Packed and local? Exactly where you want to be.

Works the same whether you just landed or you're home, tired of the same five places.

## Right now

Ship Phase 1, fast, to real strangers in Tel Aviv — not friends and family, not internal QA. Nothing else matters until we know if a real person reopens the app within a week, unprompted. That's the one number that validates the bet.

Everything downstream — monetization, second city, Events as a bigger vertical — is parked until that signal exists. Not deprioritized forever. Parked.

## The product

V1 is a single map, and the whole product lives on it. Nothing routes through a feed, a profile, or a search bar.

**V1 scope:**
- One map. Two orthogonal layers: **heat** (crowd density) and **tag** (localness) — never one blended score.
- Time slider, now → +12 hours. A place's relevance changes by the hour; the map knows that.
- Five vibe tags, plain language, no scores: super local · very local · mixed · touristy · **tourist trap**. Packed + touristy is its own tag, because that combination is exactly what to avoid.
- Two categories: Food & drinks, Things to do.
- Tap a zone → hand-curated neighborhood blurb + tagged spots. Tap a spot → **Scenic View** routes you there in-app, favoring interesting/local streets over the fastest path — not a flat hand-off to native Maps/Waze.
- No onboarding. Straight to the map + location permission.
- **Localness is decided by algorithm plus local QA, together.** The algorithm proposes; real users, asked in-app whether a spot is actually local, verify and correct it — crowdsourced from the user base, not a hired/managed team. That combination is the permanent pipeline — not hand-curation alone, waiting for an algorithm to someday replace it solo. Two open risks this trades in for the staffing risk it removes: **cold start** (a new city has no users yet to ask, on day one) and **incentive** (no reward system exists in V1 to make anyone bother answering — see Phase 3's points system, and the risk that creates).
- **Density is a synthetic feed for now**, time-bound to the slider hour, while a live popular-times data source is evaluated separately.
- Tel Aviv only at launch. A second city follows once the approach is proven, not before. Serves residents and tourists the same way — same map, same data, no separate mode.
- Saved places, Visited places, and a live Events overlay on the time slider — all kept, all core.

**Out of scope:** itineraries, bookings, Android, social features of any kind (no friends, no posting, no following, no presence), any business-facing monetization.

**Phase 2/3 feature candidates (parked until Phase 1 proves retention, not committed until each phase actually starts):**

**Phase 2 — proximity intelligence.** Discovery gets you interested; proximity makes you competent once you're there.
- Geofence detection — the app notices when you're near a spot you were already heading to.
- One-screen arrival card — "you're here, order this, say it like this, tickets here." Generated, minimal, nothing to scroll.
- Location access only turns on while you're actually en route to a suggestion — never standing, never background.
- Real cost is on the build side (permissions + geofencing logic + generated UI), not design — scope it properly before committing, don't assume it's cheap because the UI is thin.

**Phase 3 — AI local guide.** A different product bolted onto the same engine: planning, not discovery.
- A named local persona (imagine "a local from Tokyo") is the guide, not a generic assistant — tell her what you're into, she builds the day.
- Loose daily itineraries, assembled from the same time/density logic already powering V1's map.
- Audio-first — listen while walking instead of staring at the phone.
- Personalization that sharpens with use.
- **Shake to decide** — shake your phone, get one random nearby thing to do. No scrolling, no choosing, just go.
- **Auto-saved places** — stay somewhere 20+ minutes, it auto-saves. No manual save needed. Same mechanic as Bump.
- **Points system** — rewards for answering local-QA questions, visiting new places, and more. This is also the incentive layer V1's crowdsourced local QA is missing — but it ships here, in Phase 3, not V1. Until then, V1 runs on early-user goodwill alone.
- Needs identity and preference tracking neither V1 nor Phase 2 requires — that's the real reason this waits for Phase 3, not just sequencing.

**Phase 2 marketing tone** (from the original brief, still the standing direction): fast and uncluttered, conversational not corporate, bold type with real whitespace, colour used on purpose, instant feedback on every tap. References: BeReal (no ceremony), Are.na (typography-forward), TikTok FYP (dense but scannable), Citymapper (legible under heavy data). Avoid gradients, skeuomorphism, corporate polish, anything that reads 2018.

## Positioning

- **Not a guide.** Guides are static; Passenger is live, hour by hour.
- **Not a social feed.** No friends, no posting, no following, no piecing together five apps' worth of saved posts to figure out what's still open. The map answers "what do I do right now" with no query.
- **What nobody else does:** real-time heatmaps exist (nightlife-focused, built for residents); static tourist guides exist. Nobody combines both, and nobody treats packed-vs-local as two separate signals on one map. Google Maps' Popular Times is the long-term platform threat — worth watching on a recurring cadence, not a one-time snapshot, since it's the fastest path for a bigger player to close this gap.

## Business model

**Phase 1 ships fully free — decided, not paused.** No paywall, no unlock, no trial gate on anything in the Phase 1 release. Reconfirmed directly by Aviran, 2026-07-26 — consistent with `strategy/decisions.md` decision #9 ("Free V1, monetization deferred," locked 2026-07-22). What's paused is refining the *subscription* shape below, not whether Phase 1 charges — that's settled: it doesn't.

Freemium: core map free forever, subscription unlocks premium features on top.

- Core map stays free, permanently — heat + localness, both categories, time slider, tap-zone detail, Scenic View, Saved/Visited, Events. No paywall on the thing that makes Passenger Passenger.
- Subscription unlocks premium features as they ship, starting with Phase 2's proximity intelligence. One recurring price, not gated per-feature.
- **AI local guide** (Phase 3) is a further purchase on top of the subscription — its own upsell, not included even for subscribers.
- Free core reaches every tourist who'd never subscribe for a 3-day trip — it's the growth engine. Subscription is the monetization layer on top of people who already show up, not a gate in front of them.
- Price point is TBD — test once there's a premium feature worth charging for and real paid traffic to test against.

Subscription launches in Phase 2, alongside proximity intelligence and marketing spend. The free core doesn't change.

**Why freemium over a hard paywall:** V1 has no retention mechanics yet — no push, no habit loop, nothing pulling someone back daily. Betting Phase 2 revenue on "residents will open this weekly" stakes the whole plan on an unproven assumption. Freemium defers that bet — free core proves reach immediately, subscription only has to work on people who already show up.

**[ASSUMPTION]** Whether the premium layer is actually worth paying for is unproven — a thin premium tier risks nobody upgrading and the free tier absorbing everyone.

## Rollout sequence

**Phases 2 and 3 don't start until Phase 1 proves retention** — see "Right now" above. This table is the plan for after that signal exists, not a fixed calendar.

| Phase | What ships | Question it answers |
|---|---|---|
| **1 — Build to launch** | Full V1: two-layer map (heat + algo/local-QA localness), time slider, synthetic density, hero flow, hand-curated blurbs, Scenic View routing, events overlay, QA validation in Tel Aviv. Ships to real strangers, not friends/family. Ends in the App Store release. | Does the core product work end-to-end, and does a real stranger actually come back within a week? |
| **2 — Marketing + first features** | Paid acquisition starts (free core drives installs); subscription launches gating proximity intelligence and live popular-times density; core map stays free | Will people upgrade once acquired, and does the product hold up as real features and real users land at the same time? |
| **3 — More features** | Second city (proves the approach isn't Tel Aviv-specific), localness algorithm + local QA scaling to new cities, AI local guide (paid add-on on top of the subscription) | Does this generalize past one city, and is there a genuine next tier to the product? |

## How it gets built

A role-based agent team runs day-to-day execution, dispatched by a **chief-of-staff** agent:

```
backlog → spec (product) → design (designer) → build (developer/ios-developer)
        → code-review (code-reviewer/ios-code-reviewer) → qa (qa) → acceptance (product) → done

rejection loops: code-review ↩ build · qa ↩ build · acceptance ↩ build/design
stops only at: blocked-on-aviran (scope/strategy calls, money, App Store, credentials)
```

**Roles:** `product` (reads this strategy, generates its own tasks, writes PRDs, accepts finished work) · `architect` (turns PRDs into technical designs) · `designer` (UX specs + mockups, gated jointly by Serge + Aviran) · `developer` (Supabase backend/schema/RLS) · `ios-developer` (Swift/SwiftUI client) · `data-engineer` (Yeari's domain — the localness/density algorithm and ingestion pipeline) · `code-reviewer` / `ios-code-reviewer` (gate every diff, security pass mandatory) · `qa` (tests against the PRD) · `marketing` (per-phase GTM) · `competitor-research` · `project-manager` (hygiene) · `retrospective` (process learning).

Everything resolves on its own except scope/strategy calls, money, App Store actions, and credentials — those stop for Aviran.

## Technical architecture

- **Frontend:** native iOS, Swift/SwiftUI. No cross-platform framework, no Android.
- **Backend:** Supabase (Postgres) — Realtime subscriptions, RLS for per-viewer access control.
- **Mapping:** MapKit/Google Maps SDK, native heatmap layer, in-app routing for Scenic View.
- **Monetization plumbing:** RevenueCat, wired but dormant — paused along with the rest of Business model, until Phase 1 proves retention.

## Key risks

- **Local QA is crowdsourced with no incentive layer in V1.** The points system that's supposed to make users bother answering local-QA questions doesn't ship until Phase 3 — V1 has to get real signal on goodwill alone. If that doesn't produce enough answers, the algorithm has nothing real to check itself against.
- **Cold start, every new city.** Crowdsourced local QA needs users to already be there to ask. Day one of any new city, before there's a user base, there's nobody to answer — chicken-and-egg, worse than a staffed-QA model would have been.
- **Scenic View adds real routing-engine scope to V1.** In-app routing is new build surface on top of the map/heatmap shell — cost swings a lot depending on depth (see open questions), and it's now back in the launch build, not deferred.
- **Density is synthetic at launch.** The "right now" promise is only as real as the popular-times data source landing later — without it, "right now" stays simulated.
- **Subscription pricing is unvalidated** — moot until Phase 1 proves retention; don't spend more time on it before then.
- **Premium-conversion assumption is unproven.** Free core guarantees reach, but subscription only works if people actually upgrade for proximity intelligence (and later, the AI guide) rather than just staying on the free map forever.
- **Liability.** Steering someone toward a spot that turns out unsafe or misleading needs a disclaimer/liability posture before any public paywall.
- **Google is the closest real threat, not a distant one.** They already have real popular-times data at global scale and already index local content — "local vs. touristy" is a metadata layer they could ship if they decided to. The competitive gap here is real but closeable, not structural.

## Open questions

- What exactly counts as "a real person came back within a week, unprompted" — install-to-reopen, or does it need to be unprompted by a push/email too (V1 has neither, so probably moot for now, but worth defining before Phase 1 ships)?
- What's the right algorithm/local-QA balance as cities scale — does QA involvement shrink over time, or stay constant per city forever?
- Does the points system need to pull forward into V1 since local QA depends on it, or is early-user goodwill actually enough for a small first cohort in one city?
- Where's the free/premium line permanently — is it fixed at "V1 scope stays free forever," or could something currently free (Saved/Visited, events) move behind the subscription later?
- **Scenic View depth:** full in-app turn-by-turn navigation, or a route preview/suggestion that still hands off to native maps for actual turn-by-turn? Real build-cost difference between the two, needs an answer before build, not after.
- **Events and the no-B2B line:** if Events ever grows a business side (ticketing commission, promoter placement), that's B2B-shaped monetization — conflicts with the standing "no business-facing monetization" scope line. Needs an explicit call if/when it comes up, not an assumed exception.
