# Feature inspiration log

Running list of features Aviran sees in other apps and wants to consider for Passenger. Raw capture, not vetted — a feed into roadmap/PRD triage, not a commitment to build.

Add a new entry any time Aviran drops an out-of-context feature mention (no need for him to say "add this to the list" — just capture it). Newest first.

## Format

```
## YYYY-MM-DD — <short name>
- **Seen in:** <app>
- **What it does:** <1-3 lines>
- **Why it caught his eye:** <if stated>
- **Status:** inbox
```

## Entries

## 2026-07-15 — Continuous gradient heat map (Google Maps / Apple Maps style)
- **Seen in:** Google Maps and Apple Maps — their density heat-map rendering (smooth blended yellow/orange/red gradient across an area, not discrete markers).
- **What it does:** A continuous, blurred color field over the map that reads as one smooth "hot zone," rather than individual dots/circles per location.
- **Why it caught his eye:** Wants Passenger's heat map to look like this instead of circles — but fed by Passenger's own real local data, not just a headcount/crowd-density proxy.
- **Status:** inbox — routed same day to T-024 (see BOARD.md) since it directly redirects the already-approved, already-built rendering approach in the Tel Aviv Heatmap feature (T-013 / TRD §6.2). Not a fresh PRD — an amendment to in-flight work. See T-024 for the live thread.

## 2026-07-14 — Activity-aware friend icon (avatar + auto activity badge)
- **Seen in:** N/A — Aviran's own idea, dropped directly in chat (not sourced from another app)
- **What it does:** On the map/friends list, each friend's icon is part user-chosen (their profile avatar) and part auto-filled from their current real-world activity — e.g. Apple HealthKit shows them running → running icon; location/venue detection suggests a coffee shop → coffee icon. The activity part updates automatically as their real-world state changes.
- **Why it caught his eye:** Not stated beyond the idea itself.
- **Status:** inbox — sent to product 2026-07-14 for exploratory options thinking (signals, icon composition, privacy/permissions, MVP-vs-fuller scope). Not a PRD yet.

### Exploration / NOT YET A PRD (product, 2026-07-14)

Grounding facts found in the codebase (not assumptions):
- `FriendBubble` (`passenger-code/Passenger/Features/Map/FriendBubble.swift`) **already renders a primitive auto-activity badge** — a `figure.walk.motion` glyph in the bottom-trailing corner of the avatar, driven by `Friend.isMoving` (`speedKmh > 2`). The badge slot exists.
- `Friend.Presence` (`Models/Friend.swift`) **already has an unused `statusText: String?` field** — a slot for a user-set status the UI doesn't surface yet.
- So this idea = extend two things that already exist, not build from zero.

**1. Signal feasibility (reliability, honest):**
- **Manual status (user taps "☕ at a cafe"):** most reliable, most private, cheapest — writes to the existing `statusText` slot. Beats inference for accuracy.
- **Core Motion (`CMMotionActivity`):** the realistic engine for walking/running/cycling/driving/still — live-ish, low-power, no Apple Watch needed. This, not HealthKit, is the feasible auto-movement signal. Can't tell "at a gym" or "at a cafe."
- **Location/POI ("at a cafe"):** stationary + nearest-POI reverse geocode, reusing Visited Places' `PlaceCategory` mapping. Inherently **low-confidence** (proximity ≠ presence). Can't geofence every venue (20-region cap, per Visited Places precedent). Needs fresher location than the presence model uses.
- **HealthKit workouts (running/cycling/gym):** weakest of the auto options. Live `HKWorkoutSession` is watchOS-only; on iPhone, workout samples usually land **after** the activity ends. Best-effort, after-the-fact, needs an Apple Watch for most cases. Heaviest App-Review + privacy cost. **Aviran's framing named HealthKit, but Core Motion is the better fit for the movement part.**
- **Calendar (EventKit):** skip — high privacy cost, marginal value for a local/travel app.

**2. Icon composition (grounded in current `FriendBubble`):** recommend **reuse the existing bottom-trailing badge slot** for the activity SF Symbol (running/coffee/cycling), base avatar (the T-015 chosen face) stays put. Zero layout change, same idiom as Visited Places' icon-above-name. Alternatives: activity-colored ring (subtle), or temporarily replace the avatar (rejected — loses the person's identity).

**3. Privacy — the crux, real product risk:**
- HealthKit authorization is **per-type opt-in, framed for the DATA OWNER reading their own data** — Apple provides no "broadcast my health to friends" primitive. Passenger reading HealthKit then transmitting to friends is a novel exposure App Review scrutinizes hard.
- The follow-friends design (T-008) is **deliberately privacy-protective** — ghost mode is an anti-stalker feature, presence states are coarsened, ghosted-vs-offline must be byte-identical. Broadcasting "she's running / at a bar right now" is a **finer, more sensitive real-time signal that cuts against that whole philosophy.** This is a strategy-fit question, not an engineering checkbox.
- Must be **strictly opt-in**, never default ON, and activity must auto-suppress under ghost mode.

**4. Scope menu (recommend Level 0, optionally +1):**
- **L0 — manual status only:** taps set the badge via existing `statusText`. No new permission, no inference risk, honors ghost mode, ships fast. Tradeoff: not automatic (but auto real-time is largely infeasible anyway).
- **L1 — coarse auto-motion (Core Motion):** adds walking/running/cycling/driving/still. Live-ish, low power, no Watch. Tradeoff: motion class only; "running for a bus" reads as running.
- **L2 — auto venue guess (POI):** adds low-confidence "likely at a cafe/bar/beach." Tradeoff: false positives, must be styled as a guess, more battery/location.
- **L3 — HealthKit workouts:** adds gym/run/ride from Health. Tradeoff: after-the-fact, needs Apple Watch, heaviest privacy/App-Review cost — least bang for buck.

**Not PRD-ready.** Blocked on Aviran decisions (see product worklog in PROGRESS.md 2026-07-14). If he picks L0 (manual status), *that slice* is small and PRD-ready and composes cleanly with T-015 + the existing `statusText` field. The auto/HealthKit versions are not ready and the privacy-fit question is escalate-worthy.
