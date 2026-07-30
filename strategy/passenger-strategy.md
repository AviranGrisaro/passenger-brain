# Passenger Strategy

**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
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

**V1 scope, locked at the 2026-07-29 founders meeting (Aviran, Serge, Yeari, Gilad), applied 2026-07-30 — see the reconciliation block right after this list for what's genuinely new, what conflicts with decisions already locked days earlier, and what's still explicitly open:**
- One map. Under the city (Tel Aviv only at launch), the map is organized into **Hoods** — this is now the standing product-facing term for what earlier docs called "zone"/"neighborhood" (decision #12's neighborhood+spot granularity is unchanged; only the name is confirmed). Each Hood carries a **heat area** (crowd density, unchanged from below).
- **Tourist-trap flag, boolean (1/0), no local tags** — replaces the three-way **Local · Mix · Tourist** vibe tag (decision #18) as of 2026-07-30. **[FLAGGED — see reconciliation below, not silently applied as a clean swap.]** A Hood (or place) is flagged a tourist trap or it isn't; there's no graduated "how local is this" read anymore in the verbatim brief. This is a real reversal of a 3-day-old decision and touches the north star's "two orthogonal layers" framing directly — treated here as locked because it came from the founders meeting and is stated as final scope, but flagged hard for Aviran to confirm before `product`/`architect` build anything on it.
- Time slider, now → +12 hours. A place's relevance changes by the hour; the map knows that. Unchanged.
- Two categories, renamed 2026-07-30: **"Things to do"** and **"Eat & Drink"** (was "Food & drinks" / "Things to do", decision #11) — surfaced as **quick filters** alongside search. **[FLAGGED]** Whether "quick filters" means these return to permanent map chrome (reversing decision #25, which moved chips into the search sheet) or stay sheet-internal under a new name is not stated in the brief — not resolved here, see reconciliation below.
- Tap a Hood → hand-curated blurb + tagged spots. Tap a place → detail modal (name, category, save, routing) — matches the existing spot-sheet pattern, terminology aside.
- **Navigation — "Scenic Walk"** (walking only) and a **fastest-route mode**, user's choice. Each street segment carries an **Attractiveness weight**; Scenic Walk routes A→B maximizing high-weight streets passed, not just a comparison polyline. **[FLAGGED — scope increase over what's currently locked, see reconciliation below.]** This is a real routing algorithm over weighted street-segment data, not the lighter "draw two polylines for comparison" version locked 2026-07-29 (§ below) — dispatched to `data-engineer` for feasibility/timeline scoping, same risk class as the live-events pipeline (PAS-5). Hands off to native Maps/Waze for actual turn-by-turn navigation either way. No in-app turn-by-turn, voice, or rerouting in V1. Free in V1, no paywall (monetize later if at all).
- No onboarding. Straight to the map + location permission.
- **Localness is decided by algorithm plus local QA, together.** The algorithm proposes; real users, asked in-app whether a spot is actually local, verify and correct it — crowdsourced from the user base, not a hired/managed team. That combination is the permanent pipeline — not hand-curation alone, waiting for an algorithm to someday replace it solo. **The ask is triggered by a detected visit** — when the geofence logs that someone was actually somewhere, a local notification fires and a toast drops from the top of the screen asking whether the place felt local or touristy (decision #24). Asked while the visit is fresh, from someone who was genuinely there. Two open risks this trades in for the staffing risk it removes: **cold start** (a new city has no users yet to ask, on day one) and **incentive** (no reward system exists in V1 to make anyone bother answering — see Phase 2's stamp collection & status levels, and the risk that creates).
- **Density is a synthetic feed for now**, time-bound to the slider hour, while a live popular-times data source is evaluated separately.
- Tel Aviv only at launch. A second city follows once the approach is proven, not before. Serves residents and tourists the same way — same map, same data, no separate mode.
- **"Been" and "Saved" places, visually/functionally distinct** (decision #26, extended 2026-07-30): "Been" places are auto-saved when you dwell 20+ minutes somewhere already in Passenger's places table (the existing Bump mechanic; your flat and your office are never tagged spots, so they never trigger this) — each gets a sticker in your **Passport** shaped to match the place type (coffee cup for a café, etc.), sticker-album style, per city. "Saved" places are the same list's manual-add path, kept visually/functionally distinct from Been so a deliberate choice never reads as identical to one that saved itself. Geofence-detected plain visits (no 20-min dwell) still log too, per decision #26. **[FLAGGED — open, Aviran's own question, not resolved here]** what happens when someone tries to save a place Apple Maps marks permanently closed: allow it under the tourist-trap classification, or something else? No answer given; don't build against a guess.
- **Passport — pulled forward from Phase 2 into V1, 2026-07-30.** Was a parked Phase 2 candidate (confirmed Phase 2 as recently as 2026-07-28); the founders meeting moves it into V1 outright. Progression system: a stamp per Been place, contributing toward "Local" status **per Hood** in a set of hoods Passenger designates; overall "Local" status requires reaching Local in every designated Hood. **[FLAGGED — reconciliation needed, not resolved here]** this per-Hood mechanic is different from (or possibly sits on top of) the existing seven-tier global ladder (Tourist → Wanderer → Regular → Local → Insider → Native → Legend, confirmed 2026-07-28 below) — whether the ladder still exists as an overall meta-status built from per-Hood Local counts, or is replaced by the per-Hood mechanic entirely, isn't stated in the brief. Surfaces under a **Profile tab** per Aviran's verbatim brief. **[FLAGGED — naming tension, not resolved here]** "Profile" is the literal word the standing scope gate prohibits (`passenger-brain/CLAUDE.md`, `BOARD.md`: "no social features... profiles") and the exact word the 2026-07-28 naming decision deliberately avoided in favor of "Passport" for this reason. Read here as: the tab housing the Passport screen, not a reintroduction of accounts, login, or a social profile — no evidence in the brief that identity/accounts are being added — but this needs Aviran's explicit confirmation before a PRD cites it, since "Profile tab" is exactly the phrase the gate exists to catch. This also resolves §9 Q14 of `design/ux-flows.md` (the undecided 3rd nav button) as option (c): Passport reopens V1 scope for this surface, pending the naming confirmation above.
- **TikTok import — new V1 feature, 2026-07-30.** User saves a TikTok video into Passenger (share-extension or in-app paste); the app extracts places mentioned or shown in the video and adds them to Saved Places. New ingestion pipeline — content/entity extraction from video, not just a URL bookmark. Dispatched to `data-engineer` for feasibility/approach/timeline scoping — same risk class as live events (PAS-5) and Scenic Walk's weighted routing above; not proven buildable in the Phase 1 window yet.
- Live Events overlay ships in V1 as a third map layer alongside heat + tag — but it's launch-blocking: V1 does not ship until data-engineer has a working live-events ingestion pipeline (scoping ticket PAS-5). Real timeline/dependency risk, not yet proven buildable in the Phase 1 window. Added 2026-07-29, founder-direct. Confirmed again in the 2026-07-29 founders meeting: surfaced on the map, algorithmically selected as likely-interesting to the user (not just a raw feed of every event).
- **Search + quick filters**, reached from an icon in the map chrome, opening as a sheet. Covers place names, keywords ("hummus", "rooftop bar"), and Hoods — a name or keyword jumps to the spot, a Hood name pans the map and opens its Hood sheet. Results carry the same heat and tag signals as the map and honor the slider hour; search filters the map, it doesn't bypass it. Added 2026-07-27 (decision #23); category rename and "quick filters" framing added 2026-07-30 (see flagged placement question above).

**Open, not committed — explore only, per Aviran's explicit instruction 2026-07-30:** could users also import a saved Google Maps list, extracted into the map the same way TikTok import works? Not scoped, not authorized to build. A feasibility note only (no build) is reasonable next-step work; a full pipeline is not.

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

~~**Phase 2 — Stamp collection & status levels**~~ — **pulled forward into V1, 2026-07-30, founders meeting.** No longer a Phase 2 candidate; see the "Passport" bullet in V1 scope above. Left here, struck through, as a marker of the move rather than deleted silently (same convention used elsewhere in this doc). Everything below this line describes the mechanic as designed before the pull-forward — still the best available detail on stamps/ladder/naming, just re-scoped to V1 rather than Phase 2 (still subject to the per-Hood reconciliation flagged above, which this text predates):
- *(formerly described below as Phase 3's separate "points system" — unified, see below).* A collectible-per-place record that turns "I came back and it counted" into loot — the retention/return-visit loop V1 itself doesn't have yet (see Key risks: "V1 has no habit loop"). Added 2026-07-28, founder-direct.
- **This is the Phase 3 "points system," not a second mechanic — confirmed by Aviran, 2026-07-28.** The two were previously written up separately (this block, and a "Points system" bullet under the AI local guide below) with an open question about whether they were the same thing. They're the same thing. The points-system framing — rewards for answering local-QA questions, visiting new places, and more — folds into this entry. It's also the incentive layer V1's crowdsourced local QA was missing — now ships in V1 itself rather than waiting for Phase 2, per the pull-forward above.
- **Reuses the existing detected-visit signal, does not reinvent it.** A stamp fires off the same geofence-verified "were you actually there" check decision #24 already built for local-QA — `data-engineer` owns that detection; this only adds a new consumer of it. Anti-gaming for free: a stamp requires the same genuine-presence signal as local-QA, never just opening the app.
- A stamp is a collectible object per place, matching place type (coffee cup for a café, etc. — confirmed 2026-07-30, no longer just "possibly split by category").
- Total stamp count maps to a seven-tier status ladder, generic and global for now (no per-city flavor — see Open questions): **Tourist** (default, 0 stamps) → **Wanderer** (first few) → **Regular** (repeat visitor, knows a few spots) → **Local** (solid count, knows the city) → **Insider** (deep cuts, off-map spots) → **Native** (rare, near-total coverage) → **Legend** (top tier, easter-egg status, profile flex). Exact thresholds TBD (e.g. 0/5/15/30/60/100 illustrative only) — `product` to decide when this is scoped. **[FLAGGED, 2026-07-30]** how this ladder relates to the founders-meeting's per-Hood "Local" status mechanic (V1 scope, above) is not stated — reconcile before this ships.
- **Legend may unlock submitting your own recommendations.** Floated, not decided — that's a new user-write surface into a currently curated+algorithmic pipeline (moderation, quality, abuse questions all open) and needs its own call, not an assumed inclusion.
- **Naming confirmed by Aviran, 2026-07-28 as "Passport," not "profile."** The requested surface was originally "a profile screen" — but V1's own frame says "nothing routes through a feed or a profile," and the standing scope gate (`passenger-brain/CLAUDE.md`) bans profiles as a social feature by name. It ships as a **"Passport"** screen instead (matches the passport-book UI ask): a **private, single-user** stats view — no other user ever sees it, no friend graph, no following, nothing social. **[FLAGGED, 2026-07-30]** the founders-meeting brief calls the housing nav tab "Profile" — read as the tab that houses Passport, not a reversal of this naming decision or a reintroduction of accounts, but needs Aviran's explicit confirmation (see V1 scope bullet above).
- Now free in V1 like the rest of core scope (was "subscription-gated or free: not decided" while still a Phase 2 candidate) — consistent with Phase 1 shipping fully free (Business model, below). Revisit if this ever becomes a premium hook.

**Phase 3 — AI local guide.** A different product bolted onto the same engine: planning, not discovery.
- A named local persona (imagine "a local from Tokyo") is the guide, not a generic assistant — tell her what you're into, she builds the day.
- Loose daily itineraries, assembled from the same time/density logic already powering V1's map.
- Audio-first — listen while walking instead of staring at the phone.
- Personalization that sharpens with use.
- **Shake to decide** — shake your phone, get one random nearby thing to do. No scrolling, no choosing, just go.
- ~~Points system~~ — **unified into the stamp collection & status system, above** (Aviran, 2026-07-28), which itself moved from Phase 2 into V1 on 2026-07-30 (see V1 scope, above). Not a separate Phase 3 item; same mechanic, moved up two phases total.
- Needs identity and preference tracking neither V1 nor Phase 2 requires — that's the real reason this waits for Phase 3, not just sequencing.

**Phase 2 marketing tone** (from the original brief, still the standing direction): fast and uncluttered, conversational not corporate, bold type with real whitespace, colour used on purpose, instant feedback on every tap. References: BeReal (no ceremony), Are.na (typography-forward), TikTok FYP (dense but scannable), Citymapper (legible under heavy data). Avoid gradients, skeuomorphism, corporate polish, anything that reads 2018.

## Positioning

- **Not a guide.** Guides are static; Passenger is live, hour by hour.
- **Not a social feed.** No friends, no posting, no following, no piecing together five apps' worth of saved posts to figure out what's still open. The map answers "what do I do right now" without you having to ask it anything — search is there for when you already have somewhere specific in mind, not for getting an answer out of the product in the first place. If people reach for search before they read the map, the map isn't doing its job.
- **What nobody else does:** real-time heatmaps exist (nightlife-focused, built for residents); static tourist guides exist. Nobody combines both, and nobody treats packed-vs-local as two separate signals on one map. Google Maps' Popular Times is the long-term platform threat — worth watching on a recurring cadence, not a one-time snapshot, since it's the fastest path for a bigger player to close this gap.

## Business model

**Phase 1 ships fully free — decided, not paused.** No paywall, no unlock, no trial gate on anything in the Phase 1 release. Reconfirmed directly by Aviran, 2026-07-26 — consistent with `strategy/decisions.md` decision #9 ("Free V1, monetization deferred," locked 2026-07-22). What's paused is refining the *subscription* shape below, not whether Phase 1 charges — that's settled: it doesn't.

Freemium: core map free forever, subscription unlocks premium features on top.

- Core map stays free, permanently — heat + tourist-trap flag (was "localness," reworded 2026-07-30, see V1 scope), both categories, time slider, tap-Hood detail, Places (Been/Saved), Passport, TikTok import, Scenic Walk/fastest routing, hand-off to native maps. That's the full V1 scope as of the 2026-07-30 founders-meeting lock, and it never goes behind a paywall.
- Subscription unlocks premium features as they ship: **proximity intelligence**, arriving in Phase 2. (Scenic/Fast routing preview and Live Events moved into free V1 scope, 2026-07-29 — see V1 scope above — and are no longer Phase 2 subscription features. Passport moved into free V1 scope 2026-07-30, same treatment.) One recurring price, not gated per-feature.
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
| **1 — Build to launch** | Full V1 per the 2026-07-30 founders-meeting lock: Hoods + heat area + tourist-trap flag (flagged, see V1 scope), time slider, synthetic density, hero flow, hand-curated blurbs, Been/Saved places + Passport (per-Hood progression, flagged reconciliation pending), TikTok import (flagged, data-engineer scoping), Scenic Walk weighted routing + fastest mode (flagged scope increase, data-engineer scoping) + native Maps/Waze hand-off, quick filters + search, live events overlay, QA validation in Tel Aviv. Launch-blocked on working live-events (PAS-5) and TikTok-import ingestion pipelines, and on Scenic Walk's routing-algorithm feasibility. Ships to real strangers, not friends/family. Ends in the App Store release. | Does the core product work end-to-end, and does a real stranger actually come back within a week? |
| **2 — Marketing + first features** | Paid acquisition starts (free core drives installs); subscription launches gating proximity intelligence and live popular-times density | Will people upgrade once acquired, and does the product hold up as real features and real users land at the same time? |
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
- **Mapping:** MapKit/Google Maps SDK, native heatmap layer. **[FLAGGED, 2026-07-30]** the founders meeting describes "Scenic Walk" as a real weighted-routing algorithm over per-street-segment Attractiveness data (maximize high-weight streets passed A→B), a scope increase over the "draw two polylines for comparison" version locked 2026-07-29 — feasibility/timeline scoping dispatched to `data-engineer`. Full in-app turn-by-turn remains Phase 2/undecided (see Open questions).
- **Monetization plumbing:** RevenueCat, wired but dormant — paused along with the rest of Business model, until Phase 1 proves retention.

## Key risks

- **Local QA's future is unclear now that a graduated tag may be gone.** The stamp-collection & status-level system was the planned incentive layer for a crowdsourced **Local/Mix/Tourist** classification — but the 2026-07-30 brief describes a boolean tourist-trap flag with "no local tags," which may mean there's no graduated classification left for local-QA to verify at all. If confirmed, the local-QA toast (decision #24) likely becomes a simple binary "is this a tourist trap?" report rather than a 3-way classification — simpler, but a real mechanic change, not a relabeling. **Not resolved here** — see the V1 scope reconciliation above.
- **Cold start, every new city.** Crowdsourced local QA (in whatever form it ends up taking, see risk above) needs users to already be there to ask. Day one of any new city, before there's a user base, there's nobody to answer — chicken-and-egg, worse than a staffed-QA model would have been.
- **Scenic Walk is real routing-engine scope, and it's now in V1, not Phase 2.** The 2026-07-30 brief describes a weighted street-segment "Attractiveness" routing algorithm, not the lighter polyline-comparison preview locked 2026-07-29. In-app routing is new build surface on top of the map/heatmap shell, cost swings a lot depending on depth, and this version is heavier than what was locked five days earlier. Feasibility/timeline scoping dispatched to `data-engineer` — treat as launch-blocking risk, not a confirmed V1 commitment, until that scoping lands.
- **TikTok import is a new, unscoped ingestion pipeline.** Extracting places mentioned/shown in a saved video is real content/entity-extraction work, not a bookmark feature. Feasibility/timeline scoping dispatched to `data-engineer` — treat as launch-blocking risk alongside live events and Scenic Walk until scoped.
- **Density is synthetic at launch.** The "right now" promise is only as real as the popular-times data source landing later — without it, "right now" stays simulated.
- **Subscription pricing is unvalidated** — moot until Phase 1 proves retention; don't spend more time on it before then.
- **Premium tier keeps getting thinner.** Scenic/Fast routing preview, Live Events, and now Passport (2026-07-30) all moved into free V1 scope — proximity intelligence is the only confirmed subscription feature left (see Business model). One feature has to carry the entire paid-conversion case; if it alone isn't compelling enough, there's nothing else in the subscription to fall back on.
- **V1 just got thicker again, with three real new dependency risks stacked on top of each other.** The 2026-07-30 lock adds Passport, TikTok import, and a heavier Scenic Walk routing algorithm on top of the already-thicker 2026-07-29 build (routing preview + live events, PAS-5). The launch build is now: Hoods/heat/tourist-trap flag + slider + Hood/place detail + Been/Saved/Passport + Scenic Walk routing + quick filters/search + TikTok import + live events — a lot more surface area and now three external feasibility questions (events pipeline, TikTok extraction, routing algorithm), any one of which can slip the launch date. Worth a hard look at whether all three genuinely belong in the Phase 1 launch build or whether some should fall back to a fast-follow once `data-engineer`'s scoping lands.
- **Liability.** Steering someone toward a spot that turns out unsafe or misleading needs a disclaimer/liability posture before any public paywall.
- **Google is the closest real threat, not a distant one.** They already have real popular-times data at global scale and already index local content — "local vs. touristy" is a metadata layer they could ship if they decided to. The competitive gap here is real but closeable, not structural.

## Open questions

- What exactly counts as "a real person came back within a week, unprompted" — install-to-reopen, or does it need to be unprompted by a push/email too (V1 has neither, so probably moot for now, but worth defining before Phase 1 ships)?
- What's the right algorithm/local-QA balance as cities scale — does QA involvement shrink over time, or stay constant per city forever?
- Is the free/premium line now permanent at "V1 scope stays free forever," or could something currently in it (the places list, search) move behind the subscription later? The Phase 2 additions are settled as paid; what's already free is the part still worth pinning down.
- **Stamp collection — per-city flavor names** (e.g. renaming the top tier to local slang per city): explicitly a future cosmetic idea, not level-logic, not in scope now. Needs an answer only once a second city is real.

(Resolved 2026-07-28: "Passport" naming confirmed by Aviran — no longer open, see V1 scope above. Resolved 2026-07-28: stamp collection IS the Phase 3 "points system," unified as one mechanic, not two separate systems — no longer open. Resolved 2026-07-30: the stamp-collection incentive layer did pull forward into V1 — see V1 scope above, no longer a hypothetical.)
- **Scenic View/Scenic Walk depth beyond V1's routing**: V1's answer is unsettled again as of 2026-07-30 — see the flagged Scenic Walk scope-increase item in V1 scope and Key risks above (weighted-routing algorithm vs. the lighter 2026-07-29 polyline-preview). What's still open for Phase 2 regardless of how that resolves: does it ever grow into full in-app turn-by-turn, and is that worth the routing-engine build cost?
- (Resolved 2026-07-29: Events is back in V1 as a third layer alongside heat + tag — the time slider carries both kinds of information again, how packed and what's happening. No longer open.)

**New, from the 2026-07-29 founders meeting, applied 2026-07-30 — none of these are resolved, do not build against a guessed answer:**

1. **Tourist-trap-flag vs. the three-way tag system.** Does "tourist trap flag (boolean 1/0) — no local tags" really mean decision #18's **Local · Mix · Tourist** vibe tag goes away entirely, replaced by a single yes/no flag? Or does the boolean sit alongside a retained graduated tag, and "no local tags" means something narrower (e.g., no separate positive "local" label distinct from the trap flag, but Mix/Tourist framing stays)? This changes what the local-QA algorithm and toast are even for (see Key risks) and reverses a decision that was three days old at the time of the founders meeting — needs Aviran's explicit confirmation before `product`/`data-engineer`/`designer` build anything on it.
2. **What to do when a user tries to save a place Apple Maps marks permanently closed** — allow it under the tourist-trap classification, or something else? Aviran's own open question, verbatim, not answered in the brief.
3. **"Tourist trap" copy needs a softer public-facing label.** Aviran's own flag: current framing risks alienating or angering place owners. No replacement phrase given — this is a copy/positioning task for `product`/`marketing`, not a naming decided here. Note: the Phase 1 marketing plan's own word-of-mouth pitch line currently uses "tourist trap" verbatim externally — that copy needs to be revisited once a softer term exists, not left as-is.
4. **"Profile tab" naming** — does housing Passport under a tab Aviran called "Profile" reopen V1 scope for accounts/identity (the standing no-profiles gate), or is "Profile" just Aviran's shorthand for the tab that houses the private, non-social Passport screen already confirmed under that name? Read here as the latter, pending his confirmation (see V1 scope above).
5. **Passport's per-Hood "Local" status vs. the existing seven-tier global ladder** — does the ladder still exist as a meta-status derived from per-Hood progress, or does the per-Hood mechanic replace it? Not stated in the brief (see V1 scope above).
6. **"Quick filters" placement** — chrome-level (reversing decision #25's move of category chips into the search sheet) or still sheet-internal under a new name? Not stated in the brief (see V1 scope above).
7. **Google Maps saved-list import** — explicitly not committed, exploration only per Aviran's instruction. Not authorized to build; a feasibility note is reasonable next-step work, a full pipeline is not.
