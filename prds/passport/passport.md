# Passport — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Two blockers resolved:** decision #39 ("Profile" is the literal tab name, a naming exception to the no-profiles gate, not a reversal) and #40 (per-Hood Local status replaces the seven-tier ladder outright). Both held this PRD at PAS-10.

## Description

- A private, single-user screen: a per-city sticker album plus per-Hood **Local** progress. Nobody else ever sees it.
- Opened by the **Profile** button, the third of the map's three nav buttons (`design/ux-flows.md` §2, §5).
- One sticker per **Been** place, shaped to match the place type, filed under that city's page (#29).
- Progression is **per-Hood Local status only**; overall "Local" means Local in every designated Hood.
- **Not in scope:** the seven-tier ladder (Tourist → Legend) in any form, including as a derived or display-only status (#40); any social surface — sharing, comparison, follower counts, leaderboards, avatars; accounts or login; "Legend unlocks submitting your own recommendations," which died with the ladder; rewards for answering local-QA (unspecified upstream — see Open questions); per-city flavour names for status; any Phase 2/3 hook.

## Motivation

- Strategy, verbatim: *"a stamp per Been place, contributing toward "Local" status **per Hood** in a set of hoods Passenger designates; overall "Local" status requires reaching Local in every designated Hood."*
- Strategy, verbatim: *""Profile" is the literal, final tab name — it houses only the private, single-user Passport screen."*
- Strategy names the gap it fills: *"V1 still has no habit loop — nothing pulling someone back daily."*
- It reuses the dwell signal Places already needs, adding a consumer rather than a detector (#29).

## Requirements

### Must-have (P0)

1. **Private and single-user, with no social surface anywhere.**
   - [ ] No screen shows another person's Passport, sticker count, status, or name.
   - [ ] No share, invite, compare, follow, follower-count, or leaderboard affordance exists in the tab.
   - [ ] No avatar or profile image renders anywhere in it — avatars are banned by name in the scope gate.
   - [ ] The tab adds no login, sign-up, or account screen (#39: *"no accounts/login being added"*).

2. **One tap from the map, and it never blocks the core loop.**
   - [ ] The Profile button is always visible in map chrome; one tap opens Passport.
   - [ ] Passport is one of the mutually exclusive nav modals — opening search, heat, or Places closes it, and vice versa (`ux-flows.md` §2.1).
   - [ ] A user who never opens Passport loses no map function.
   - [ ] Dismissing returns to the map with camera and selected hour unchanged.

3. **A sticker per Been place, off the existing signal.**
   - [ ] A sticker appears exactly when a place becomes **Been** — the same 20-minute verified dwell that auto-saves it, no second check, no extra permission (#26, #29).
   - [ ] A place logged only as **Visited** earns no sticker.
   - [ ] A manually **Saved** place earns no sticker on the save alone.
   - [ ] One Been place yields exactly one sticker; revisiting adds none.
   - [ ] Sticker shape matches the place's type — a coffee cup for a café (#29). The data field this needs does not exist yet; see Open questions.
   - [ ] Stickers file under the city's page; Tel Aviv is the only page in V1.

4. **Per-Hood Local status is the whole progression.**
   - [ ] The screen shows, per designated Hood, progress toward Local and whether Local is reached.
   - [ ] Overall Local reads as reached only when **every** designated Hood is Local.
   - [ ] No retired tier name — Tourist, Wanderer, Regular, Insider, Native, Legend — appears in app or data (#40).
   - [ ] No global point total, level number, or aggregate rank renders anywhere.
   - [ ] Hoods not designated for progression are absent from the view rather than listed at zero. **[ASSUMPTION]**
   - [ ] The Local threshold is read from configuration, not hardcoded per Hood.

5. **Progress is legible without arithmetic or colour.**
   - [ ] Each Hood row states progress as numerals against the threshold, not a bar or colour alone (`design-principles.md` §3).
   - [ ] A Hood at zero renders as a plain not-started state — never an error, a lock, or a teaser.
   - [ ] An empty Passport shows a plain empty state naming what earns a sticker (`design-principles.md` §4).

6. **Earning something never interrupts the map.**
   - [ ] No modal, full-screen takeover, or blocking celebration fires on a sticker or a Local milestone.
   - [ ] Any in-the-moment surfacing that does ship is non-blocking and auto-dismissing, like the local-QA toast. Whether it exists at all is an open design call (`ux-flows.md` §9 Q13).
   - [ ] A sticker earned while the app was closed is present next time Passport opens, with no catch-up animation required to see it.

7. **Accessibility** (`design-principles.md` §5, §2).
   - [ ] Every sticker carries a VoiceOver label naming the place and its type — never image-only.
   - [ ] Per-Hood status is announced as text, including the count and whether Local is reached.
   - [ ] Every interactive target is ≥44pt.

8. **Degraded permission and offline both open the screen.**
   - [ ] With Location Always denied, Passport opens and shows whatever was earned, with no nagging copy and no re-prompt.
   - [ ] Offline, the screen renders fully from on-device data.

### Nice-to-have (P1)

- A hint of how many more places a Hood needs.
- Passport-book page-turn treatment (designer's, not a requirement).

## Technical design

- **Data model:** stickers are **derived from the Places feature's Been rows** — no second store of truth, so a sticker can never disagree with the list. Passport adds no per-place table.
- **Data model:** `hoods.designated_for_progression` plus one configured Local threshold. Per-Hood progress computes on read as the count of Been places in that Hood, so changing the threshold needs no backfill.
- **APIs / contract:** no new writes. Reads Hood geometry to attribute a Been place to a Hood, and the designated flag with the rest of the static Hood payload.
- **Architecture notes:** V1 adds no identity, so Passport is device-local for the same reason Places is — it inherits that store rather than adding another. `SALVAGE.md` has nothing reusable here; `Services/AuthService.swift` is BURN and nothing here reopens it.
- **Dependencies:** **hard upstream on `places-been-saved`** (the Been signal) and `map-hoods-heat` (Hood polygons for attribution, plus the chrome the Profile button sits in). Nothing depends on Passport.
- **Open technical questions:** where `place_type` comes from (see below — the biggest one); whether progress computes on device or server once a live pipeline exists; how a Been place is re-attributed if a Hood polygon later changes.

## Assumptions

- **[ASSUMPTION]** Stickers derive from Been rows with no separate store, so Passport inherits Places' device-local storage — and its loss on reinstall.
- **[ASSUMPTION]** Undesignated Hoods are absent from the progress view rather than shown at zero (req 4).
- **[ASSUMPTION]** No reward exists for answering local-QA, because none is specified. If one is intended, req 3 is incomplete.

## Open questions & risks

- **Two numbers are missing and this cannot ship without them:** how many Been places make a Hood "Local," and which Hoods are designated. Aviran's or `data-engineer`'s; neither is invented here.
- **`place_type` does not exist in the data model.** #29 requires a sticker shaped to place type — café vs. bar — but `places` carries exactly two category values and nothing finer (#11, #33: *"no third value, no null, no 'other'"*). Either the curated dataset gains a `place_type` field, or V1 ships two sticker shapes and #29 is not met. A dependency on the dataset, not a rendering detail.
- **Nothing rewards answering local-QA.** Strategy's stamp write-up folds in *"rewards for answering local-QA questions, visiting new places, and more"*, but #29 ties stickers to Been places and #40 retired the ladder carrying the rest. So the incentive layer rewards visiting, not answering — while the localness pipeline's cold-start risk is precisely that nobody answers. Aviran's call; same gap flagged in the tourist-trap PRD.
- **Reinstall loses the album**, inherited from Places. Fixing it means anonymous server identity, which strategy parks until Phase 3.
- **Naming drift is the standing risk.** "Profile" is a confirmed *naming* exception (#39), not a licence. Any later ticket reading the tab name as permission for accounts, avatars, or a social surface should be rejected at the scope gate.

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | Decisions #39 and #40 resolved the items held at PAS-10 (PAS-6 items 4, 5) |
| 2026-07-30 | Seven-tier ladder excluded outright, including as a derived status | #40: the per-Hood mechanic "replaces the seven-tier global ladder outright" |
| 2026-07-30 | Stickers derived from Places' Been rows, not stored separately | One signal, three consumers — stops Passport and Places disagreeing |
| 2026-07-30 | Local threshold and designated-Hood set left unset rather than estimated | No source states either; inventing a number is what the scope gate exists to stop |
