# Passenger Agent OS — Progress

Append-only worklog. Every agent adds an entry when it finishes a task — what shipped, what it learned, what it left behind. Newest at the bottom. `BOARD.md` holds current state; this holds history.

Entry format:

```
### YYYY-MM-DD — <agent> — <task id> <short title>
- **Did:** what actually changed (files, migrations, issue IDs)
- **Evidence:** build/test output, screenshots, review verdicts
- **Left behind:** follow-ups, known gaps, anything the next agent needs
```

---

### 2026-07-27 — designer — UX flows doc: search (decision #23) added

- **Did:** Updated `design/ux-flows.md` and its HTML reading view (`design/ux-flows.html`) for decision #23 — search ships in V1. Landed search sheet as a third **Secondary**-tier item alongside zone sheet and spot sheet (Aviran's explicit call, not Primary chrome — preserved the reasoning inline: a permanent search bar undercuts "you don't need to ask"). Confirmed the depth rule holds at 2 levels for both result types, but by two different mechanics (place/keyword result matches the Saved/Visited shortcut; neighborhood result is not a shortcut, it's the same zone sheet one level deeper because the query itself occupies level 1). Added Journey 5 — "I already know what I'm looking for" — as a new sixth journey (renumbered the old degraded-run journey to 6), since search is the one path that doesn't start by reading the map; attached its unhappy paths (no results, no data at the hour, offline, neighborhood with no blurb) inline. Made an explicit `[design call]` in §6 on search's visual effect on the map (dims non-matching pins while the sheet is open, clears on selection — kept temporary and non-persistent so it doesn't become a second filter alongside the category chips). Updated both mermaid diagrams, fixed §1's frame paragraph (dropped the now-wrong "no search bar" line, kept "no profile"), and added two new open questions (recent-searches persistence; whether search respects the active category filter).
- **Evidence:** Both files updated and grepped clean for stale "Journey 5"/"five journeys"/decision-count references. Rendered the HTML twin in the browser preview to confirm the new journey card, hierarchy row, and diagram nodes display correctly.
- **Left behind:** Seven open questions now stand in §9/HTML footer for Aviran, two new to this revision. Section 8's parked-feature list (Scenic View, Live Events, Phase 3 items) is unaffected by this change and wasn't touched.

---

### 2026-07-27 — designer — UX flows doc revised: conflict resolved, restructured around journeys

- **Did:** Rewrote `design/ux-flows.md` per Aviran's resolution of the prior entry's flagged conflict, relayed by the coordinator. Settled as fact: three vibe tags (Local · Mix · Tourist, no dedicated "tourist trap" tag), Scenic View moved to Phase 2 (V1's "Go" hands off to native Maps/Waze and exits the app), Live Events moved to Phase 2 (V1 map is heat + tag only). Deleted the conflict-banner section and all "committed vs. briefed" hedging entirely — the doc now reads as settled. Restructured §4 from 8 disconnected micro-flows into 5 end-to-end journeys (just landed → hand-off; resident planning with the slider; returning to a saved place; giving back a local-QA answer; the full degraded run under denied-location/offline) with unhappy paths embedded at the step where they bite. Updated: Secondary tier (Scenic View removed, now just zone sheet + spot sheet), depth rule (2 levels inside the app, not 3 — "Go" is an exit, not a level), §6's packed+touristy legibility treatment (now load-bearing since no tag names the worst case — added a display-time-only warning badge for busy+Tourist as a `[design call]`), both mermaid diagrams, and §8 (Scenic View and Events now written up as Phase 2 parked candidates, with what each would displace). Dropped the conflict question from §9; added two new ones (Visited-detection reliability during a Maps/Waze hand-off; VoiceOver labeling for the new computed warning badge).
- **Evidence:** File at `design/ux-flows.md`, fully rewritten. Grepped for residual "conflict"/"committed strategy"/"tourist trap"/"five vibe" references post-edit — none found outside one intentional "very local but temporarily busy" scenario description.
- **Left behind:** Section 8 notes the Scenic View depth question (full turn-by-turn vs. route-preview-then-handoff) is still open but is now a Phase 2 scoping question, not a V1 blocker — flagged there instead of in §9. Five open questions remain in §9 for Aviran, two of them new to this revision.

---

### 2026-07-27 — designer — UX flows doc for Passenger V1

- **Did:** Wrote `design/ux-flows.md` at Aviran's direct request — flow, feature hierarchy (primary/secondary/tertiary with reasoning + tap-cost from cold open), primary flow (first launch vs. subsequent), 8 numbered secondary flows with unhappy paths, navigation model + depth rule, map state/density behavior (including the packed+touristy legibility problem), 2 mermaid diagrams, Phase 2/3 placement, and 5 open questions for Aviran. Not a per-feature spec — no PRD-traceability table or mockup link, since `prds/INDEX.md` is still empty.
- **Evidence:** File at `design/ux-flows.md`. No PRD exists yet to verify against; this doc is meant to shape the six PRDs `product` hasn't written yet.
- **Left behind:** Flagged a real conflict at the top of the doc — the task brief's strategy summary (3 vibe tags, spot-tap hands off to native maps, Scenic View + Events as Phase 2) doesn't match the committed `strategy/passenger-strategy.md` + `decisions.md` (5 tags, in-app Scenic View routing in V1, Events as V1 core). Built the doc against the committed files and flagged the discrepancy as Open Question 1 rather than silently picking one — needs Aviran's call before `product` writes PRDs off either version. Also flagged: two tier placements I made unilaterally against the task brief's own examples (time slider + category chips as Primary, not Secondary — reasoning in the doc), and that Visited is automatic/read-only per decision #16, not a manual "mark visited" action as the brief assumed.

---

### 2026-07-26 — chief-of-staff — reset: Locali → Passenger

- **Did:** Hard reset. Locali (16.5k Swift lines, 27 PRDs, 26 migrations, 13 Linear projects) frozen and replaced with a fresh Passenger workspace.
  - Old repos committed and pushed, then frozen at `github.com/AviranGrisaro/locali` — nothing deleted, `main` = iOS app, `brain` = planning workspace.
  - `passenger-code/` — new Xcode project. Swift 6 strict concurrency, iOS 26, SwiftUI + MapKit, zero third-party packages. Builds clean, one passing test.
  - `passenger-brain/` — carried forward only: the strategy doc, the north-star HTML, `decisions.md`, `LESSONS.md` (13 entries), and the agent fleet. Everything else archived.
  - New Linear workspace `passenger`, team `PAS`, single project **Passenger V1**.
- **Evidence:** `xcodebuild build` exit 0, no warnings. `xcodebuild test -only-testing:PassengerTests` — 1 test, passed.
- **Why:** Ten of the 27 old PRDs built features the strategy explicitly forbids — social graph, friend following, profile avatars, onboarding carousels. All ten passed every lifecycle gate. The process didn't fail at build quality; it failed because no gate checked work against the strategy.
- **Left behind:**
  - `SALVAGE.md` inventories the old codebase with a per-file reuse/reference/burn verdict — check it before building anything.
  - New scope gate in `BOARD.md`: no PRD leaves `spec` without quoting the strategy line that authorizes it. `product` enforces it.
  - `prds/` is empty. First `product` pass over the strategy doc generates roughly six PRDs, not twenty-seven.
  - Supabase schema starts at `001` — the old 26 migrations stay in the archive repo.
