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
