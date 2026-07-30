# Hood & Place Detail — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Scope note:** two flagged items are deliberately left unanswered here — "quick filters" placement (decision #33, PAS-6 item 6) and the localness / tourist-trap line in either sheet (decision #28, PAS-6 item 1).

## Description

- Two sheets over the map, both reached in one tap, neither of which leaves the map screen.
- **Hood sheet:** the Hood's name, its hand-curated blurb, and its list of tagged places.
- **Place detail modal:** name, category, save, and the route hand-off.
- Categories are renamed to **"Things to do"** and **"Eat & Drink"** (decision #33) — exactly two, everywhere they appear.
- The route action hands off to native Maps or Waze; Passenger draws no turn-by-turn.
- **Not in scope:** where category filters live — chrome vs. sheet-internal is unconfirmed (PAS-6 item 6); any localness / tourist-trap line in either sheet (PAS-6 item 1); Scenic Walk vs. fastest-route selection and any route polyline (PAS-7); the Places list surface, Been/Saved provenance, and the permanently-closed-place case (PAS-6 item 2); search; Passport; live events.

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
   - [ ] Behaviour when Apple Maps marks the place permanently closed is **not** specified here — PAS-6 item 2, Aviran's own open question. Do not build a guess.

### Nice-to-have (P1)

- Opening hours and a photo in the place modal, if the curated dataset carries them.
- Hood sheet grouping its place list by category.

## Technical design

- **Data model:** `places` (id, name, category enum of exactly two values, coordinates, hood_id) plus curated blurb text on `hoods`. Public-read. `saved_places` is user-scoped and spec'd by the held Places PRD, not here.
- **APIs / client-server contract:** Hood sheet reads places by `hood_id`; the modal reads one place row. Static curated data — no Realtime, no hour-binding. Save writes locally first so the affordance responds inside the 400ms budget regardless of network.
- **Architecture notes:** native sheet presentation with detents (`design/ux-flows.md` §2.1 — platform primitive, not a custom sheet). `SALVAGE.md` marks `Models/Place.swift`, `Services/DirectionsService.swift`, `Services/SavedPlacesStore.swift` REUSE.
- **Dependencies:** the map PRD lands first. Downstream: routing-mode selector waits on PAS-7, the Places list on PAS-6 item 2.
- **Open technical questions:** whether the two-value category enum is enforced in Postgres or only client-side; whether "Eat & Drink" is stored as display text or a stable key.

## Open questions & risks

- **The localness line is missing from both sheets.** `design/map-rendering-spec.md` §4 makes the place sheet the tag's only home, and PAS-6 item 1 has not settled what the tag is. Both sheets are buildable without it; neither is complete until it lands.
- **"Quick filters" placement is unresolved** (PAS-6 item 6). Decision #25 moved category chips into the search sheet; decision #33 reintroduces "quick filters" without saying where. This PRD names the categories and stops there deliberately.
- **"Tourist trap" copy is being softened** (decision #36, PAS-9). Any label this feature shows should wait for that term.
- **[ASSUMPTION]** "Tagged spots" means curated places belonging to the Hood, not places carrying a localness tag. Same rows either way; flagged because the wording is ambiguous.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | First PRD pass over the 2026-07-30 V1 lock (PAS-10) |
| 2026-07-30 | Category rename to "Things to do" / "Eat & Drink" spec'd as a hard requirement | Decision #33; rename is confirmed even though the filter placement is not |
| 2026-07-30 | Filter placement, tag line, and routing-mode selection excluded rather than assumed | PAS-6 items 1 and 6, PAS-7 — scope gate forbids specing against unconfirmed lines |
