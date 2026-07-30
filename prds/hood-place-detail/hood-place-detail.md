# Hood & Place Detail — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Scope note, updated 2026-07-30:** both items this PRD left unanswered are now **resolved upstream and owned by other PRDs**, not open questions here. The tourist-trap line in the place modal is decision #37, spec'd in [`../tourist-trap-flag/`](../tourist-trap-flag/tourist-trap-flag.md) req 6. Quick-filters placement is decision #41 — sheet-internal, decision #25 stands — and belongs to the search PRD, not this one. This PRD's own scope is unchanged.

## Description

- Two sheets over the map, both reached in one tap, neither of which leaves the map screen.
- **Hood sheet:** the Hood's name, its hand-curated blurb, and its list of tagged places.
- **Place detail modal:** name, category, save, and the route hand-off.
- Categories are renamed to **"Things to do"** and **"Eat & Drink"** (decision #33) — exactly two, everywhere they appear.
- The route action hands off to native Maps or Waze; Passenger draws no turn-by-turn.
- **Not in scope:** where category filters live — settled sheet-internal (decision #41) and owned by the search PRD; the tourist-trap line's content and rendering (owned by [`tourist-trap-flag`](../tourist-trap-flag/tourist-trap-flag.md), which places one text line in this modal); Scenic Walk vs. fastest-route selection and any route polyline (PAS-7); the Places list surface, Been/Saved provenance, and the permanently-closed badge (owned by [`places-been-saved`](../places-been-saved/places-been-saved.md), decision #38); search; Passport; live events.

## Motivation

- Strategy: "Tap a Hood → hand-curated blurb + tagged spots. Tap a place → detail modal (name, category, save, routing)."
- The map answers "where"; these two sheets are the only V1 surface answering "what is this, and is it worth walking to."
- Decision #10 makes the blurb the "local read" — without it a Hood is a coloured shape with no reason to trust it.

## Requirements

### Must-have (P0)

1. **Hood sheet opens in one tap and does not lose the map.**
   - [ ] Tapping a Hood polygon, or the Hood button when it is showing, opens the same sheet — one destination, more than one door.
   - [ ] The map stays visible and interactive behind the sheet; the sheet is never a full-screen push.
   - [ ] Dismissing returns to the map with camera and selected hour unchanged.

2. **Hood sheet content.**
   - [ ] Shows the Hood name and its hand-curated blurb (decision #10).
   - [ ] Lists every curated place in that Hood, each row carrying name and category.
   - [ ] A Hood with no blurb yet shows the place list alone, with no placeholder copy standing in for the blurb.
   - [ ] A Hood with no curated places shows a plain empty state, not an error (`design/design-principles.md` §4).
   - [ ] Tapping a row opens that place's detail modal.

3. **Place detail modal content.**
   - [ ] Shows name and category.
   - [ ] Offers a save action and a route action, and nothing else that navigates away.
   - [ ] Opens directly on one tap of a pin or a Hood-sheet row — never a two-step preview (`design/map-rendering-spec.md` §4).

4. **One primary action, not three equal ones.**
   - [ ] Exactly one action in the modal reads as primary — unique colour and ≥1.5× the secondary's weight (`design/design-principles.md` §2, Von Restorff).
   - [ ] Save is not the primary action.
   - [ ] Every action in the modal has a ≥44pt touch target (`design/design-principles.md` §2, Fitts's Law).

5. **Route hands off; Passenger never navigates.**
   - [ ] The route action opens native Maps or Waze with the place as destination, walking mode.
   - [ ] No turn-by-turn, no voice, and no rerouting happens inside Passenger — strategy: "No in-app turn-by-turn, voice, or rerouting in V1."
   - [ ] Returning to Passenger from the handed-off app restores the same map state, sheet closed.
   - [ ] With no route app available, the action is disabled with a plain explanation, not a crash.

6. **Exactly two categories, with the new names.**
   - [ ] The only category values that render anywhere are **"Things to do"** and **"Eat & Drink"** (decision #33, superseding decision #11's wording).
   - [ ] Every curated place carries exactly one of the two — no third value, no null, no "other".
   - [ ] Category is distinguishable without colour, by word in the sheets and by glyph on the map (`design/map-rendering-spec.md` §4).
   - [ ] No string reading "Food & drinks" survives anywhere in the shipped app or data.

7. **Save writes to the manual path only.**
   - [ ] The save action adds the place to the manual "Saved" path, never to the dwell-detected "Been" path (decisions #26, #30).
   - [ ] The action's state is visible on reopen — a saved place reads as saved.
   - [ ] Saving a place Apple Maps marks permanently closed **succeeds** — no block, no preventing dialog (decision #38, 2026-07-30). The badge that results is spec'd in [`places-been-saved`](../places-been-saved/places-been-saved.md) req 4, not here.

### Nice-to-have (P1)

- Opening hours and a photo in the place modal, if the curated dataset carries them.
- Hood sheet grouping its place list by category.

## Technical design

- **Data model:** `places` (id, name, category enum of exactly two values, coordinates, hood_id) plus curated blurb text on `hoods`. Public-read. `saved_places` is user-scoped and spec'd by the held Places PRD, not here.
- **Data sourcing (added 2026-07-30, standing rule).** Neither table has rows and neither is authored by this PRD. The `hoods.blurb` column does not exist in migration `001` and every blurb is a person-authored artifact — [`prds/hood-dataset/`](../hood-dataset/hood-dataset.md) req 4. The `places` table does not exist at all; its rows, its two-value category constraint, and its coordinates→`hood_id` containment check are [`prds/places-dataset/`](../places-dataset/places-dataset.md) reqs 1–2. Both are hard upstream of this feature: req 2 and req 6 are unfalsifiable against an empty dataset.
- **APIs / client-server contract:** Hood sheet reads places by `hood_id`; the modal reads one place row. Static curated data — no Realtime, no hour-binding. Save writes locally first so the affordance responds inside the 400ms budget regardless of network.
- **Architecture notes:** native sheet presentation with detents (`design/ux-flows.md` §2.1 — platform primitive, not a custom sheet). `SALVAGE.md` marks `Models/Place.swift`, `Services/DirectionsService.swift`, `Services/SavedPlacesStore.swift` REUSE.
- **Dependencies:** the map PRD lands first, and [`hood-dataset`](../hood-dataset/hood-dataset.md) + [`places-dataset`](../places-dataset/places-dataset.md) supply everything both sheets render. Downstream: routing-mode selector waits on PAS-7, the Places list on PAS-6 item 2.
- **Open technical questions:** whether the two-value category enum is enforced in Postgres or only client-side; whether "Eat & Drink" is stored as display text or a stable key.

## Open questions & risks

- ~~**The localness line is missing from both sheets.**~~ **Resolved 2026-07-30 (decision #37).** `design/map-rendering-spec.md` §4 makes the place modal the flag's only home; that line is now spec'd in [`tourist-trap-flag`](../tourist-trap-flag/tourist-trap-flag.md) req 6. This PRD's modal must leave room for one text line it does not itself own.
- ~~**"Quick filters" placement is unresolved.**~~ **Resolved 2026-07-30 (decision #41):** sheet-internal, decision #25 stands unreversed. Chips never return to map chrome. This PRD still only names the two categories; the sheet itself is the search PRD's.
- ~~**"Tourist trap" copy is being softened** (decision #36, PAS-9). Any label this feature shows should wait for that term.~~ **Resolved 2026-07-30 (decision #42, PAS-9 ACCEPTed):** the public-facing term is **"tourist-heavy spot."** Any label this feature shows uses that wording, not "tourist trap." `design/map-rendering-spec.md` §3 already renders it at Hood level — see the copy-fit follow-up in that spec's own review (a Hood is not a "spot").
- **[ASSUMPTION]** "Tagged spots" means curated places belonging to the Hood, not places carrying a localness tag. Same rows either way; flagged because the wording is ambiguous.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | First PRD pass over the 2026-07-30 V1 lock (PAS-10) |
| 2026-07-30 | Category rename to "Things to do" / "Eat & Drink" spec'd as a hard requirement | Decision #33; rename is confirmed even though the filter placement is not |
| 2026-07-30 | Filter placement, tag line, and routing-mode selection excluded rather than assumed | PAS-6 items 1 and 6, PAS-7 — scope gate forbids specing against unconfirmed lines |
| 2026-07-30 | Localness-label copy resolved to "tourist-heavy spot" | Decision #42, at PAS-9 acceptance. Only the copy — the mechanic and filter placement were reconciled separately, below |
| 2026-07-30 | Data-sourcing bullet added: the blurb column and the whole `places` table are named as other PRDs' deliverables | Standing rule, founder-direct 2026-07-30. The PRD stated the *shape* of both and left "who authors the rows" implicit; reqs 2 and 6 cannot pass against an empty dataset |
| 2026-07-30 | Three stale PAS-6 exclusions rewritten: tag mechanic (#37), filter placement (#41), closed-place save (#38) | All three resolved live by Aviran; the tag line and the closed badge now have owning PRDs. Scope unchanged — only the reasons and the pointers |
