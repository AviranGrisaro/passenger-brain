# Phase 1 Marketing & Acquisition — Ship to Real Strangers in Tel Aviv

**Status:** Draft
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)

## The one thing this plan serves

Per `strategy/passenger-strategy.md` ("Right now"): nothing matters this phase except whether **a real stranger in Tel Aviv reopens the app within a week, unprompted.** Not installs, not reach, not App Store ranking. Every tactic below is judged against whether it can plausibly produce *that* kind of user — not against how many people it reaches.

Per the strategy doc's Rollout sequence table (`strategy/passenger-strategy.md`, lines ~113–116), which defines only three phases: **paid acquisition starts at Phase 2, and Phase 1 is zero-spend by definition, not just by Aviran's budget call.** (The marketing agent's own role file previously said "real marketing spend starts at Phase 4" — stale, no Phase 4 exists in the current strategy doc; corrected in `.claude/agents/marketing.md` and its mirrors, commit `8b19a5e`.)

## Audience for this phase

Not "travelers" broadly — specifically, people physically reachable in Tel Aviv for free, right now:
- International tourists on the backpacker/hostel circuit (short stay, actively looking for "what's actually good, right now" — the exact problem statement in the north star).
- Young Tel Aviv residents/expats who go to the kind of local spots the app needs to learn from — this cohort also matters because local-QA needs real answers from people who were actually there (decision #22), and Tel Aviv is the very first city, so there is no existing user base to ask yet (strategy doc, Key risks: "cold start, every new city").
- Explicitly **not** friends/family/internal QA — the strategy gate and `passenger-brain/CLAUDE.md`'s phase framing both exclude that cohort from counting toward the Phase 1 signal. Founders may still dogfood the app for bug-catching, but those sessions must be excluded from the retention metric (see Metrics).

## Positioning

Applies the master strategy's positioning as-is (`strategy/passenger-strategy.md`, "Positioning") — not re-derived here: not a guide, not a social feed, the one thing nobody else does is treating packed-vs-local as two separate live signals. For Phase 1 in Tel Aviv specifically, the pitch simplifies to one sentence for word-of-mouth use: **"One map that shows what's actually packed right now, and whether it's a real local spot or a tourist-heavy spot — no scrolling five apps to find out."**

**Copy note (2026-07-30, decision #36):** "tourist trap" replaced with **"tourist-heavy spot"** everywhere this plan speaks to a real person — Aviran flagged at the 2026-07-29 founders meeting that the old phrasing risks alienating/angering place owners. **Update, same day:** the underlying mechanic question is now resolved too — decision #37 confirms the map's tourist-trap flag is a literal boolean (1/0), fully replacing decision #18's three-way Local/Mix/Tourist tag. The public phrase and the internal data model were separate questions when this note was first written; both are settled now, and both point the same direction — "tourist-heavy spot" is the copy for a binary flag, not a hedge on a still-undecided mechanic. Runner-up options considered: "touristy spot" (softer/more casual, but weaker on signaling "maybe skip it"), "mainstream pick" (drops the geographic/traveler framing that makes the pitch land), "crowd-magnet for visitors" (too colorful/informal for a first pass). Recommending "tourist-heavy spot": it's descriptive of foot traffic, not a verdict on the business, and it pairs cleanly with "real local spot" in the existing sentence.

## Channels & tactics

All zero/near-zero budget, per Aviran's explicit Phase 1 budget call. Every tactic assumes no paid boosting, no influencer fees, no ad spend.

- **Hostel front-desk seeding.** Tel Aviv has a dense backpacker circuit (e.g. Abraham Hostel Tel Aviv and similar). Ask front-desk staff to mention the app or display a printed card/QR code at check-in — this is the standard grassroots channel travel apps use to reach exactly the "just landed, don't know where to go" moment the app is built for. Cost: founder time to visit and ask; a small print run for cards (flag — see Escalations, this is a real dollar cost even if trivial).
- **Free walking-tour partnerships.** Tel Aviv has active free/paid walking tour operators; guides already talk to groups of tourists at the start of their trip. Asking a guide to mention the app costs nothing but a conversation, and reaches the same "just arrived" moment. Cost: founder time only, if the guide agrees to mention it unprompted rather than the tour operator's brand co-promoting (co-promotion = external partnership, escalate).
- **Local Facebook/expat groups** (e.g. Tel Aviv tourist/expat/backpacker groups). Organic, disclosed post from a founder — "we built this, would love feedback from people actually using Tel Aviv right now" — not a covert plant. Precedent: city-specific apps have long used local Facebook/subreddit communities as a pre-paid-spend seeding channel; Foursquare's own early growth famously started as word-of-mouth among a small in-person crowd (SXSW 2009) before any paid acquisition existed — the same "seed a real, present crowd first" logic applies here at city-launch scale. Cost: founder time; posting under a personal account costs nothing, posting as a "Passenger" brand page is a new public account (escalate).
- **Local Reddit (r/telaviv, r/Israel travel threads).** Same disclosed-founder-post approach; check each subreddit's self-promotion rules before posting to avoid removal. Cost: time only.
- **Café/bar table-tents at genuinely local spots.** A handful of spots the app would *not* flag as tourist-heavy — ask the owner to let you leave a small card/QR code. This double-purposes as acquisition *and* as a seed source for local-QA answers, since people scanning it are standing in a real local spot right now. Cost: founder time to approach owners + small print cost (escalate, see below) — and approaching businesses for a standing display is itself a public-facing partnership, escalate before committing to any specific venue.
- **App Store Optimization (ASO) basics.** Keyword-optimized title/subtitle/description drafted now so the listing is ready — e.g. "Tel Aviv," "local," "heatmap," "right now." Free to draft; **publishing the live listing is an App Store Connect action and needs Aviran's go-ahead**, same as any other external public presence.
- **Not doing:** paid social ads, paid influencer posts, boosted posts, referral-reward mechanics, or a public waitlist/landing page with a domain — all either cost money or create new public presence, both gated to Aviran this phase. A native iOS share-sheet "tell a friend" button is cheap to build and worth flagging to `product`/`ios-developer` as a P1 nice-to-have, but it is not committed in this plan since it's a build dependency, not a marketing action.

## Acquisition funnel

Awareness → Install → Activation → **Unprompted 7-day reopen (the only metric that matters)**.

- **Awareness:** hostel/tour/café/community-post touches above. No paid reach, so awareness volume will be small and slow — that's expected, not a failure mode, given the budget constraint.
- **Install:** App Store link only (TestFlight would work too, but a public TestFlight beta is itself an App Store Connect artifact — escalate before setting one up).
- **Activation:** first session where the map renders and the person taps at least one zone or spot. **[ASSUMPTION]** no activation event exists yet in the app to measure this precisely — see Metrics below; this is a proxy definition, not a confirmed instrumented one.
- **Retention (the gate):** person opens the app again 2–8 days after first open, without any push, email, or direct human nudge from the team. Phase 1 ships with no push/email infrastructure (per strategy doc, Business model section), so "unprompted" mainly means: no founder personally messaged them to come back.
- **Drop-off expectations:** not stated — **[ASSUMPTION]** no baseline exists for any of these steps since the app hasn't shipped yet; this plan doesn't invent a conversion-rate estimate.

## Budget / resourcing

**Zero cash budget, confirmed by Aviran.** This is a founder-time-only plan: visiting hostels/cafes, posting in communities, drafting ASO copy. The only real dollar costs anywhere in this plan are small print runs for QR cards — flagged for Aviran below rather than assumed approved. If Aviran wants to spend anything (printing, a paid boosted post, an influencer micro-partnership), that's a Phase 1 exception to the "zero spend" default and needs explicit sign-off, not an assumption baked into this plan.

## Metrics

**Success metric definition (this phase's exit gate):**

A **tracked, non-founder-network install** counts as a "real stranger" if its device/session ID isn't on the team's manual test-device list (see Tracking, below — there's no account system to filter by identity instead).

**Pass/fail bar: [ASSUMPTION] ≥20% of tracked real-stranger installs reopen the app 2–8 days after first open, with zero direct human follow-up from the team to that person in between.** This number is not sourced from any benchmark — none exists for a pre-launch app with this exact shape — it's a working bar to test against, flagged here so Aviran/product can replace it with an official number rather than this plan silently picking one. **[ASSUMPTION] minimum sample: 30 real-stranger installs** before treating the resulting percentage as signal rather than noise; below that, report the raw count instead of a rate.

**Tracking — what actually exists vs. what's needed:** `passenger-code`'s git history shows the app was emptied to start Phase 1 build from scratch (`chore: empty the app so the first feature starts from scratch`), and no analytics/event tooling (Amplitude, PostHog, Firebase, etc.) appears anywhere in the codebase or agent files. **There is no tracking infrastructure to point to today.** This plan cannot instrument anything itself — that's a build dependency, not a marketing deliverable — but the specific ask this plan is surfacing to `product`/`architect` is:
- A minimal `app_opens`-style event (anonymous device ID, timestamp) is the smallest thing that answers the Phase 1 question. It doesn't need to be a full analytics SDK — a single Supabase table the app writes to on launch would do.
- A manual, human-maintained list of team/QA device IDs to exclude from the "real stranger" count, since there's no user-identity system to filter by otherwise.
- A simple log of any direct outreach (e.g., a founder following up with an early user for feedback) so those individuals can be excluded from the "unprompted" count.

None of this is decided or built yet — flagging it here so the retention gate has something to measure against once `architect`/`developer` scope it, rather than this plan assuming instrumentation that doesn't exist.

## Open questions and risks

- **No tracking infrastructure exists yet.** The entire metric this plan serves is unmeasurable until a minimal event log ships — this is the single biggest open risk to the phase, bigger than any channel choice above.
- **Cold-start local-QA risk compounds the acquisition problem.** The strategy doc already flags that a new city has no users to ask "is this local" on day one (Key risks). The café/table-tent tactic above is deliberately chosen to help with both problems at once, but it's still an unproven approach, not a solved one.
- **"Unprompted" is genuinely hard to guarantee** with zero push/email infra and a small, manually-run grassroots funnel — the team will know many of these early users personally by name from having approached them in person, which sits in tension with "real stranger." Recommend the team keep outreach to a single first touch (hand someone a card, don't follow up) to keep the signal clean.
- **[ASSUMPTION]** The 20%/7-day bar and the 30-install sample floor are both working numbers proposed here, not sourced or Aviran-approved — flagged explicitly per this agent's "no invented numbers" rule.
- ~~**"Tourist trap" → "tourist-heavy spot" (2026-07-30, decision #36) — copy-only, not a mechanic decision.**~~ **Resolved 2026-07-30:** the mechanic question is settled too — decision #37 confirms the boolean flag. See the Positioning section note; no longer a hedge.
- **Stale-reference scan (this session, not fixed):** the Acquisition funnel's activation definition ("taps at least one **zone** or spot") predates decision #27 confirming **"Hoods"** as the product-facing term — decisions.md itself flags internal docs as not yet swept, so this is a should-fix, not new. **This plan still has no Passport/stamp-collection retention-hook copy** — the blocker that held this back (whether "Profile" reopens the no-profiles gate, and how per-Hood status relates to the old ladder) is resolved as of decisions #39/#40 (Profile confirmed as a naming exception; per-Hood status replaces the ladder outright), so this is now unblocked and worth a dedicated copy pass — not written here since it's new copy work, not a reference fix.
- **Escalations to Aviran (not decided here):** any spend (QR card printing, any paid post/tactic); creating any external public presence (a "Passenger" Facebook/Instagram account, a domain, the live App Store Connect listing, a public TestFlight link); approaching specific named businesses (hostels, cafés, tour operators) for a standing partnership/display; committing to any public launch date.
