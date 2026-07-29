# Passenger Strategy

**Owner:** Aviran Grisaro
**Last updated:** 2026-07-29
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

V1 is a single map, and the whole product lives on it. Nothing routes through a feed or a profile. Search exists, but as a sheet over the map rather than a destination — you never leave the map screen to reach it.

**V1 scope:**
- One map. Two orthogonal layers: **heat** (crowd density) and **tag** (localness) — never one blended score.
- Time slider, now → +12 hours. A place's relevance changes by the hour; the map knows that.
- Three vibe tags, plain language, no scores: **Local** (trust it) · **Mix** · **Tourist**. There's no separate "tourist trap" tag — packed-and-touristy is what to avoid, and it reads off the two layers together rather than needing a label of its own.
- Two categories: Food & drinks, Things to do — selected inside the search sheet, not from permanent chrome on the map (decision #25).
- Tap a zone → hand-curated neighborhood blurb + tagged spots. Tap a spot → preview a fast or scenic route as a polyline on the map for comparison, then hand off to native Maps/Waze for actual turn-by-turn navigation. No in-app turn-by-turn, voice, or rerouting in V1 — routing preview only. Free in V1, no paywall (monetize later if at all). Added 2026-07-29, founder-direct.
- No onboarding. Straight to the map + location permission.
- **Localness is decided by algorithm plus local QA, together.** The algorithm proposes; real users, asked in-app whether a spot is actually local, verify and correct it — crowdsourced from the user base, not a hired/managed team. That combination is the permanent pipeline — not hand-curation alone, waiting for an algorithm to someday replace it solo. **The ask is triggered by a detected visit** — when the geofence logs that someone was actually somewhere, a local notification fires and a toast drops from the top of the screen asking whether the place felt local or touristy (decision #24). Asked while the visit is fresh, from someone who was genuinely there. Two open risks this trades in for the staffing risk it removes: **cold start** (a new city has no users yet to ask, on day one) and **incentive** (no reward system exists in V1 to make anyone bother answering — see Phase 2's stamp collection & status levels, and the risk that creates).
- **Density is a synthetic feed for now**, time-bound to the slider hour, while a live popular-times data source is evaluated separately.
- Tel Aviv only at launch. A second city follows once the approach is proven, not before. Serves residents and tourists the same way — same map, same data, no separate mode.
- **One list of places, fed three ways** (decision #26): you save somewhere manually, you dwell somewhere 20+ minutes and it saves itself, or the geofence detects you were there. Saved and Visited are no longer separate lists. The list also renders on the map, so your own places are visible in place rather than only in a list. Auto-save only ever fires on places already in Passenger's own places table — your flat and your office are not tagged spots, so they never get saved.
- Live Events overlay ships in V1 as a third map layer alongside heat + tag — but it's launch-blocking: V1 does not ship until data-engineer has a working live-events ingestion pipeline (scoping ticket PAS-5). Real timeline/dependency risk, not yet proven buildable in the Phase 1 window. Added 2026-07-29, founder-direct.
- **Search**, reached from an icon in the map chrome, opening as a sheet. Covers place names, keywords ("hummus", "rooftop bar"), and neighborhoods — a name or keyword jumps to the spot, a neighborhood pans the map and opens its zone sheet. Results carry the same heat and tag signals as the map and honor the slider hour; search filters the map, it doesn't bypass it. Added 2026-07-27 (decision #23).

**Out of scope:** itineraries, bookings, Android, social features of any kind (no friends, no posting, no following, no presence), any business-facing monetization.

**Phase 2/3 feature candidates (parked until Phase 1 proves retention, not committed until each phase actually starts):**

**Phase 2 — proximity intelligence.** Discovery gets you interested; proximity makes you competent once you're there.
- Geofence detection — the app notices when you're near a spot you were already heading to.
- One-screen arrival card — "you're here, order this, say it like this, tickets here." Generated, minimal, nothing to scroll.
- Location access only turns on while you're actually en route to a suggestion — never standing, never background.
- Real cost is on the build side (permissions + geofencing logic + generated UI), not design — scope it properly before committing, don't assume it's cheap because the UI is thin.

**Phase 2 — Scenic View, full in-app navigation.** V1 now ships a route preview only — polyline comparison of scenic vs. fast, then hand-off to native Maps/Waze for the actual walk (see V1 scope, added 2026-07-29). What's still a Phase 2 candidate is whether that preview ever grows into full in-app turn-by-turn navigation.
- Real routing-engine build scope if it happens — full turn-by-turn is a different cost tier than the V1 preview, not an incremental step from it.
- Gating undecided. Proximity intelligence is the only confirmed subscription feature now (see Business model, updated 2026-07-29); whether full turn-by-turn is ever paid is an open call, not an assumed default.

**Phase 2 — Live Events, business layer.** The live events map overlay itself is V1 scope now, launch-blocking on data-engineer's ingestion pipeline (see V1 scope, added 2026-07-29). What remains a Phase 2 candidate is only a further monetization layer on top of that overlay, not the overlay itself.
- If Events ever grows a business side (ticketing commission, promoter placement), that's B2B-shaped monetization and conflicts with the standing "no business-facing monetization" line. Needs an explicit call if it comes up, not an assumed exception.

**Phase 2 — Stamp collection & status levels** *(formerly described below as Phase 3's separate "points system" — unified, see below).* A collectible-per-place record that turns "I came back and it counted" into loot — the retention/return-visit loop V1 itself doesn't have yet (see Key risks: "V1 has no habit loop"). Added 2026-07-28, founder-direct. **Phase placement confirmed by Aviran, 2026-07-28** — this is a committed Phase 2 item, not a parked candidate awaiting a placement call (still subject to the standing rule that Phase 2 doesn't start until Phase 1 proves retention, same as every other Phase 2 item).
- **This is the Phase 3 "points system," not a second mechanic — confirmed by Aviran, 2026-07-28.** The two were previously written up separately (this block, and a "Points system" bullet under the AI local guide below) with an open question about whether they were the same thing. They're the same thing. The points-system framing — rewards for answering local-QA questions, visiting new places, and more — folds into this entry, and the whole mechanic moves to Phase 2. It's also the incentive layer V1's crowdsourced local QA is missing (see Key risks): it ships in Phase 2, not V1; until then V1 runs on early-user goodwill alone.
- **Reuses the existing detected-visit signal, does not reinvent it.** A stamp fires off the same geofence-verified "were you actually there" check decision #24 already built for local-QA — `data-engineer` owns that detection; this only adds a new consumer of it. Anti-gaming for free: a stamp requires the same genuine-presence signal as local-QA, never just opening the app.
- A stamp is a collectible object per place, possibly split by place-category (a coffee stamp, a nightlife stamp) — exact shape is a product/design call, not decided here.
- Total stamp count maps to a seven-tier status ladder, generic and global for now (no per-city flavor — see Open questions): **Tourist** (default, 0 stamps) → **Wanderer** (first few) → **Regular** (repeat visitor, knows a few spots) → **Local** (solid count, knows the city) → **Insider** (deep cuts, off-map spots) → **Native** (rare, near-total coverage) → **Legend** (top tier, easter-egg status, profile flex). Exact thresholds TBD (e.g. 0/5/15/30/60/100 illustrative only) — `product` to decide when this is scoped.
- **Legend may unlock submitting your own recommendations.** Floated, not decided — that's a new user-write surface into a currently curated+algorithmic pipeline (moderation, quality, abuse questions all open) and needs its own call, not an assumed inclusion.
- **Naming confirmed by Aviran, 2026-07-28.** The requested surface was originally "a profile screen" — but V1's own frame says "nothing routes through a feed or a profile," and the standing scope gate (`passenger-brain/CLAUDE.md`) bans profiles as a social feature by name. It ships as a **"Passport"** screen instead (matches the passport-book UI ask): a **private, single-user** stats view — no other user ever sees it, no friend graph, no following, nothing social — so it was never the social-profile pattern the gate exists to catch, just the same banned word. This line now authorizes a PRD to cite it under the "Passport" name — no longer an open assumption.
- Subscription-gated or free: not decided — see Business model when this gets scoped.

**Phase 3 — AI local guide.** A different product bolted onto the same engine: planning, not discovery.
- A named local persona (imagine "a local from Tokyo") is the guide, not a generic assistant — tell her what you're into, she builds the day.
- Loose daily itineraries, assembled from the same time/density logic already powering V1's map.
- Audio-first — listen while walking instead of staring at the phone.
- Personalization that sharpens with use.
- **Shake to decide** — shake your phone, get one random nearby thing to do. No scrolling, no choosing, just go.
- ~~Points system~~ — **unified into Phase 2's stamp collection & status levels, above** (Aviran, 2026-07-28). Not a separate Phase 3 item; same mechanic, moved up a phase.
- Needs identity and preference tracking neither V1 nor Phase 2 requires — that's the real reason this waits for Phase 3, not just sequencing.

**Phase 2 marketing tone** (from the original brief, still the standing direction): fast and uncluttered, conversational not corporate, bold type with real whitespace, colour used on purpose, instant feedback on every tap. References: BeReal (no ceremony), Are.na (typography-forward), TikTok FYP (dense but scannable), Citymapper (legible under heavy data). Avoid gradients, skeuomorphism, corporate polish, anything that reads 2018.

## Positioning

- **Not a guide.** Guides are static; Passenger is live, hour by hour.
- **Not a social feed.** No friends, no posting, no following, no piecing together five apps' worth of saved posts to figure out what's still open. The map answers "what do I do right now" without you having to ask it anything — search is there for when you already have somewhere specific in mind, not for getting an answer out of the product in the first place. If people reach for search before they read the map, the map isn't doing its job.
- **What nobody else does:** real-time heatmaps exist (nightlife-focused, built for residents); static tourist guides exist. Nobody combines both, and nobody treats packed-vs-local as two separate signals on one map. Google Maps' Popular Times is the long-term platform threat — worth watching on a recurring cadence, not a one-time snapshot, since it's the fastest path for a bigger player to close this gap.

## Business model

**Phase 1 ships fully free — decided, not paused.** No paywall, no unlock, no trial gate on anything in the Phase 1 release. Reconfirmed directly by Aviran, 2026-07-26 — consistent with `strategy/decisions.md` decision #9 ("Free V1, monetization deferred," locked 2026-07-22). What's paused is refining the *subscription* shape below, not whether Phase 1 charges — that's settled: it doesn't.

Freemium: core map free forever, subscription unlocks premium features on top.

- Core map stays free, permanently — heat + localness, both categories, time slider, tap-zone detail, the places list, hand-off to native maps. That's the full V1 scope, and it never goes behind a paywall.
- Subscription unlocks premium features as they ship: **proximity intelligence**, arriving in Phase 2. (Scenic/Fast routing preview and Live Events moved into free V1 scope, 2026-07-29 — see V1 scope above — and are no longer Phase 2 subscription features.) One recurring price, not gated per-feature.
- **AI local guide** (Phase 3) is a further purchase on top of the subscription — its own upsell, not included even for subscribers.
- Free core reaches every tourist who'd never subscribe for a 3-day trip — it's the growth engine. Subscription is the monetization layer on top of people who already show up, not a gate in front of them.
- Price point is TBD — test once there's a premium feature worth charging for and real paid traffic to test against.

Subscription launches in Phase 2, alongside proximity intelligence and marketing spend. The free core doesn't change.

**Why freemium over a hard paywall:** V1 still has no habit loop — nothing pulling someone back daily. The one notification it sends (decision #24) fires after a visit the user already made, asking a question that helps the map; it isn't a re-engagement mechanic and shouldn't be counted as one. Betting Phase 2 revenue on "residents will open this weekly" stakes the whole plan on an unproven assumption. Freemium defers that bet — free core proves reach immediately, subscription only has to work on people who already show up.

**[ASSUMPTION]** Whether the premium layer is actually worth paying for is unproven — a thin premium tier risks nobody upgrading and the free tier absorbing everyone.

## Rollout sequence

**Phases 2 and 3 don't start until Phase 1 proves retention** — see "Right now" above. This table is the plan for after that signal exists, not a fixed calendar.

| Phase | What ships | Question it answers |
|---|---|---|
| **1 — Build to launch** | Full V1: three-layer map (heat + algo/local-QA localness + live events), time slider, synthetic density, hero flow, hand-curated blurbs, routing preview (scenic/fast polyline) + native Maps/Waze hand-off, QA validation in Tel Aviv. Launch-blocked on a working live-events ingestion pipeline (data-engineer, PAS-5). Ships to real strangers, not friends/family. Ends in the App Store release. | Does the core product work end-to-end, and does a real stranger actually come back within a week? |
| **2 — Marketing + first features** | Paid acquisition starts (free core drives installs); subscription launches gating proximity intelligence and live popular-times density (Scenic/Fast routing preview and Live Events moved to V1, 2026-07-29 — see above); stamp collection & status levels ("Passport" screen) also ships this phase, gating TBD; core map stays free | Will people upgrade once acquired, and does the product hold up as real features and real users land at the same time? |
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
- **Mapping:** MapKit/Google Maps SDK, native heatmap layer. A route-preview polyline (scenic + fast, comparison only, no turn-by-turn) is V1 scope as of 2026-07-29. Full in-app turn-by-turn remains Phase 2/undecided (see Open questions).
- **Monetization plumbing:** RevenueCat, wired but dormant — paused along with the rest of Business model, until Phase 1 proves retention.

## Key risks

- **Local QA is crowdsourced with no incentive layer in V1.** The stamp-collection & status-level system (formerly described separately as a "points system") that's supposed to make users bother answering local-QA questions doesn't ship until Phase 2 — V1 has to get real signal on goodwill alone. If that doesn't produce enough answers, the algorithm has nothing real to check itself against.
- **Cold start, every new city.** Crowdsourced local QA needs users to already be there to ask. Day one of any new city, before there's a user base, there's nobody to answer — chicken-and-egg, worse than a staffed-QA model would have been.
- **Scenic View is real routing-engine scope, whenever it ships.** In-app routing is new build surface on top of the map/heatmap shell, and cost swings a lot depending on depth. Out of the launch build now, but the cost doesn't go away — it moves to Phase 2, where it lands alongside proximity intelligence and paid acquisition all at once.
- **Density is synthetic at launch.** The "right now" promise is only as real as the popular-times data source landing later — without it, "right now" stays simulated.
- **Subscription pricing is unvalidated** — moot until Phase 1 proves retention; don't spend more time on it before then.
- **Premium tier just got thinner, not thicker.** Scenic/Fast routing preview and Live Events moved into free V1 scope 2026-07-29 — proximity intelligence is now the only confirmed subscription feature (see Business model). One feature has to carry the entire paid-conversion case; if it alone isn't compelling enough, there's nothing else in the subscription to fall back on.
- **V1 is now a thicker bet, with real new dependency risk.** Adding routing preview and a live events layer (launch-blocking on data-engineer's ingestion pipeline, PAS-5) makes the launch build heat + tag + events + slider + zone/spot detail + routing preview + search + the places list — more surface area and a real external dependency, versus the leaner two-layer build this replaces. That's more to validate the core "comes back within a week" bet against, and more that can slip the launch date if the events pipeline isn't ready in time.
- **Liability.** Steering someone toward a spot that turns out unsafe or misleading needs a disclaimer/liability posture before any public paywall.
- **Google is the closest real threat, not a distant one.** They already have real popular-times data at global scale and already index local content — "local vs. touristy" is a metadata layer they could ship if they decided to. The competitive gap here is real but closeable, not structural.

## Open questions

- What exactly counts as "a real person came back within a week, unprompted" — install-to-reopen, or does it need to be unprompted by a push/email too (V1 has neither, so probably moot for now, but worth defining before Phase 1 ships)?
- What's the right algorithm/local-QA balance as cities scale — does QA involvement shrink over time, or stay constant per city forever?
- Does the stamp-collection incentive layer need to pull forward into V1 since local QA depends on it, or is early-user goodwill actually enough for a small first cohort in one city?
- Is the free/premium line now permanent at "V1 scope stays free forever," or could something currently in it (the places list, search) move behind the subscription later? The Phase 2 additions are settled as paid; what's already free is the part still worth pinning down.
- **Stamp collection — per-city flavor names** (e.g. renaming the top tier to local slang per city): explicitly a future cosmetic idea, not level-logic, not in scope now. Needs an answer only once a second city is real.

(Resolved 2026-07-28: "Passport" naming confirmed by Aviran — no longer open, see Phase 2 candidate above. Resolved 2026-07-28: stamp collection IS the Phase 3 "points system," unified as one Phase 2 mechanic, not two separate systems — no longer open, see Phase 2 candidate above and the now-struck-through "Points system" bullet under Phase 3.)
- **Scenic View depth beyond V1's preview**: V1's answer is settled — route preview only, hands off to native maps for the actual walking (added 2026-07-29). What's still open for Phase 2: does it ever grow into full in-app turn-by-turn, and is that worth the routing-engine build cost? Not a launch blocker either way now.
- (Resolved 2026-07-29: Events is back in V1 as a third layer alongside heat + tag — the time slider carries both kinds of information again, how packed and what's happening. No longer open.)
