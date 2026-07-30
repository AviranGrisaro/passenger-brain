# Search & Quick Filters — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Placement settled:** decision #41 — quick filters stay sheet-internal, #25 unreversed. **Layout is not settled** (`ux-flows.md` §9 Q15, Aviran's); every requirement below holds either way.

## Description

- One sheet over the map, opened by the search icon — one of three nav buttons in map chrome.
- A single text field matching three things: place names, keywords, Hood names.
- Two chips — **"Eat & Drink"** and **"Things to do"** (#33) — the "quick filters", and the only place either lives.
- A place or keyword result opens the place modal; a Hood result pans the map and opens the Hood sheet.
- **Not in scope:** the sheet's layout (`ux-flows.md` §9 Q15, open); the destination sheets' contents (`hood-place-detail`); heat and flag rendering (`map-hoods-heat`, `tourist-trap-flag`); search history across launches (§9 Q6, open); any third filter axis — no tourist-trap filter, no open-now, no distance; voice search; TikTok or Google Maps import as a result source.

## Motivation

- Strategy, verbatim: *"**Search + quick filters**, reached from an icon in the map chrome, opening as a sheet. Covers place names, keywords ("hummus", "rooftop bar"), and Hoods… Results carry the same heat and tag signals as the map and honor the slider hour; search filters the map, it doesn't bypass it."*
- Strategy, verbatim, on the chips: *"surfaced as **quick filters** inside the search sheet, unchanged from decision #25."*
- Strategy caps its ambition: *"you never leave the map screen to reach it."* Positioning adds the watch-item — if people reach for search first, the map isn't working.

## Requirements

### Must-have (P0)

1. **One door, one sheet, never a destination.**
   - [ ] The search icon opens the sheet over the map; the map stays visible behind it throughout.
   - [ ] No path through search pushes a full-screen view or leaves the map screen.
   - [ ] Dismissing returns to the map with camera and selected hour unchanged.
   - [ ] Opening search closes whichever of {heat modal, Places list, Profile} is open (`ux-flows.md` §2.1).

2. **One field matches three kinds of things.**
   - [ ] It matches place names ("Port Said"), keywords ("hummus", "rooftop bar"), and Hood names ("Florentin").
   - [ ] Every row states which of the three it is, in a word — a Hood is never mistakable for a place.
   - [ ] Matches update as the user types, rendering under 400ms of a keystroke pause (`design-principles.md` §2).
   - [ ] The field carries a visible label; a placeholder never stands in as the only label (§3).

3. **Two chips, quick filters and nothing more.**
   - [ ] Exactly two chips exist, and neither renders anywhere outside this sheet (#25, #41).
   - [ ] A chip with an empty field produces a category-scoped result set — the same mechanic a typed query produces (`ux-flows.md` §6).
   - [ ] A chip narrows a typed query rather than replacing it.
   - [ ] Both categories are active on every fresh open.
   - [ ] Selected state reads without colour alone (`design-principles.md` §3).
   - [ ] No third chip and no other filter axis ships — a "hide tourist-heavy spots" filter is a fresh decision (`ux-flows.md` §6).

4. **Search filters the map at the selected hour; it never builds a second view of the data.**
   - [ ] While results show, the map dims everything except matching pins and Hoods, and keeps heat and the flag on what remains (§6).
   - [ ] Dimming clears the instant a result is selected or the sheet is dismissed.
   - [ ] Search reads the same cached place and Hood data the map reads — no search-only dataset, no search-only ranking.
   - [ ] Opening a result shows heat and the flag exactly as tapping that pin or Hood would, at the current hour.
   - [ ] Search re-reads against the current hour on every open, never an hour cached from a past session.
   - [ ] A result with no density for that hour gets the standard no-live-data treatment, not an error (`ux-flows.md` Journey 5).
   - [ ] A row carries name, category and Hood — **not** a tourist-trap line: the flag has one home, the place modal (`tourist-trap-flag` req 6). **[ASSUMPTION]**

5. **A result goes where the map would have gone.**
   - [ ] A place or keyword result opens that place's detail modal — the sheet a pin tap opens (`hood-place-detail` req 3).
   - [ ] A Hood result pans there and opens the Hood sheet — the sheet a polygon tap opens (`ux-flows.md` §5).
   - [ ] Depth never exceeds map (0) → search (1) → destination sheet (2).
   - [ ] Search creates no exit of its own; routing still hands off from the place modal (`hood-place-detail` req 5).

6. **Every state is specified, none is a dead end.**
   - [ ] Empty field: two chips, no result list, no default suggestions.
   - [ ] No match: one line naming the query, field stays open and editable — never a blank view or a modal error.
   - [ ] Offline: matching runs on cached data only, and anything opened carries the standard staleness label.
   - [ ] Hood result with no blurb: the Hood sheet's own empty state, unchanged (`hood-place-detail` req 2).
   - [ ] Location denied changes nothing — search is not location-scoped (`ux-flows.md` Journey 6).

7. **In-progress state survives an interruption, not a completion.**
   - [ ] Tapping another nav button preserves the typed query and chip selection; reopening restores both (§2.1).
   - [ ] Tapping a result, or manually dismissing, clears query and chip selection.
   - [ ] Nothing persists across launches — no search history, matching the slider's reset convention. **[ASSUMPTION]**

8. **Reach and accessibility.**
   - [ ] Search icon, every chip, and every row has a ≥44pt touch target (`design-principles.md` §2).
   - [ ] Every row announces type and name in VoiceOver — "Florentin, Hood" / "Port Said, place, Eat & Drink".
   - [ ] The sheet stays usable at the largest Dynamic Type size; rows grow rather than truncate.
   - [ ] Search-result pins differ from Places-list pins by shape or icon, never colour alone (§2.1).

### Nice-to-have (P1)

- Session-only recent searches, cleared on relaunch (`ux-flows.md` §9 Q6's middle ground).
- Result list sectioned by type — places, then Hoods.

## Technical design

- **Data model:** no new tables. Reads `places` (name, category, hood_id) and `hoods` (name), both public-read and already cached by the map PRD. **Keyword matching needs a searchable text field on `places` that no PRD specifies** — see Open questions.
- **APIs / contract:** matching runs client-side against the cached place and Hood payloads. No per-keystroke round trip — that is what makes both the 400ms budget and the offline requirement achievable.
- **Architecture notes:** the sheet reads the single `selectedHour` source of truth the slider owns (`time-slider`), never its own copy. Native sheet presentation (`ux-flows.md` §2.1), subject to the open layout call. `SALVAGE.md` marks `Services/PlaceSearchService.swift` REUSE — start there.
- **Dependencies:** `map-hoods-heat` (place/Hood data, dim behaviour), `hood-place-detail` (both destinations), `time-slider` (selected hour). `tourist-trap-flag` supplies the modal's flag line but does not block this.
- **Open technical questions:** what field keyword matching runs against and who curates it; prefix vs. substring vs. fuzzy matching; whether Hoods and places share one ranked list.

## Assumptions

- **[ASSUMPTION]** A row carries no tourist-trap line (req 4). Strategy says results carry "the same heat and tag signals as the map" — and a pin carries no flag at any zoom (`map-rendering-spec.md` §4), so the destination sheet is the honest reading. If Aviran means a per-row line, req 4 changes and `tourist-trap-flag` req 6 reopens.
- **[ASSUMPTION]** No search history across launches (req 7). `ux-flows.md` §9 Q6 recommends it; unconfirmed.
- **[ASSUMPTION]** Matching runs client-side on cached data. Nothing states it; the offline requirement implies it.

## Open questions & risks

- **The sheet's layout is unresolved and it is Aviran's call.** His ask was a literal 50/50 top/bottom map-over-list split; design review recommended native `.medium`/`.large` detents (`ux-flows.md` §2, §9 Q15). Nothing here resolves it; `ios-developer` must not build against either reading first.
- **Keyword search has no data behind it.** "hummus", "rooftop bar" need a per-place keyword field; `places` has name, one of two categories, coordinates, hood_id. Without it, keyword search degrades to name-matching and the strategy line goes unmet. Escalation, not a build detail.
- **Decision #23 makes search a watch-item** — reaching for search before reading the map means the map failed — and nothing in V1 measures that. No analytics pipeline exists.
- **Req 7's interrupted-vs-completed rule is `designer`'s reconciliation** of two decisions made in different sessions, flagged at `ux-flows.md` §9 Q17 as needing Aviran's confirmation.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | Decision #41 settled sheet-internal placement — the last thing holding it (`prds/INDEX.md`) |
| 2026-07-30 | Sheet layout left open rather than assumed | §9 Q15 — Aviran's literal-split ask vs. design's detent recommendation is unresolved |
| 2026-07-30 | Rows carry no tourist-trap line, labelled **[ASSUMPTION]** | `tourist-trap-flag` req 6 gives the flag one home; a per-row line would reopen that PRD |
