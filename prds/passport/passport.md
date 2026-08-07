# Passport — PRD

**Status:** Accepted v5 — `product` ACCEPT WITH NOTES 2026-08-08 (`passenger-code fe1c8ef`, on `main` at `040ea1e`); at `aviran-review`
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-08-08
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
   - [ ] Sticker shape matches the place's type — a coffee cup for a café (#29). The field is `places.place_type`, now spec'd in [`places-dataset`](../places-dataset/places-dataset.md) req 3: a closed enumeration, internal-only, one sticker shape per value, non-null on every row. It does not exist in any migration yet.
   - [ ] **Pass condition (added at acceptance 2026-08-05, L-009):** with the place name hidden, a person can name what kind of place a sticker is for — a café's reads as a cup, a restaurant's as cutlery, a museum's as a museum. A distinct-but-abstract shape per type (circle for café, triangle for restaurant) **fails** this bullet however consistently it is assigned: "matches the place type" is depiction, not one-to-one mapping. Every gate before this one checked only that each type had *a* shape.
   - [ ] **Pass condition tightened at acceptance 2026-08-08 (L-009):** a blind answer naming a *different real kind of place* fails too — not only a geometry word, "don't know", or another of the six. "Bank" or "courthouse" for the museum sticker is a fail, however plausible the glyph. The prior criterion (TRD §9 row 3(g)) listed a closed set of fail answers, so a wrong-but-off-list answer passed by silence — which is what `qa`'s 2026-08-07 blind read of `building.columns.fill` returned, and no gate could fail it. **Open against this bullet:** that one glyph, escalated to Aviran (see Open questions); the other five pass.
   - [ ] Every `place_type` value has a sticker shape, so no Been place can earn a shapeless sticker (`places-dataset` req 3 fails validation on a value with no shape).
   - [ ] Stickers file under the city's page; Tel Aviv is the only page in V1.

4. **Per-Hood Local status is the whole progression.**
   - [ ] The screen shows, per designated Hood, progress toward Local and whether Local is reached.
   - [ ] Overall Local reads as reached only when **every** designated Hood is Local.
   - [ ] No retired tier name — Tourist, Wanderer, Regular, Insider, Native, Legend — appears in app or data (#40).
   - [ ] No global point total, level number, or aggregate rank renders anywhere.
   - [ ] Hoods not designated for progression are absent from the view rather than listed at zero. **[ASSUMPTION]**
   - [ ] The Local threshold is read from configuration, not hardcoded per Hood. **Value: 2** (decision #45).
   - [ ] **Pass condition (added at acceptance 2026-08-07, L-009):** every designated Hood's row must be able to reach the Local state by visiting places open today — count its `permanently_closed: false` places and compare to the threshold, not its row count ([`hood-dataset`](../hood-dataset/hood-dataset.md) req 5). A Hood whose row is pinned below Local wherever the user goes is a dataset defect, not a UI state. Today `kerem-hateimanim` and `neve-tzedek` sit at exactly 2 of 2 visitable — passing with zero margin, one closure from failing.

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
   - [ ] **Pass condition (added at acceptance 2026-08-05, L-009):** the label's second clause names the kind of place. *"Dr. Shakshuka, cutlery sticker"* passes; *"Dr. Shakshuka, triangle sticker"* fails — a geometry word is not a type. Speaking the raw `place_type` string stays forbidden (`places-dataset` req 3), and naming what the sticker depicts is not the same thing: once the sticker depicts the type, one word satisfies both rules.
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
- **Data sourcing (added 2026-07-30, standing rule).** Passport stores nothing of its own; it reads three things none of which exist yet. `hoods.designated_for_progression` is [`hood-dataset`](../hood-dataset/hood-dataset.md) req 5. `places.place_type` is [`places-dataset`](../places-dataset/places-dataset.md) req 3. **The Local threshold is 2** (decision #45, 2026-08-04 — was "a configured number nobody has stated"). It has a dataset consequence, not just a config one: `places-dataset` req 7 requires every designated Hood to contain at least that many curated places, or Local is unreachable there by construction and req 4 can never pass. Now that the number exists, that check is concrete — **every designated Hood must hold ≥2 curated places that are open** (`permanently_closed: false`; corrected 2026-08-07 at T-048 acceptance — the raw row count it previously named stays green even if every place in a Hood closes), which unblocks the `validate_dataset.py` rule that was skipped while the threshold was unknown (`PAS-6` item 12), and constrains [`hood-dataset`](../hood-dataset/hood-dataset.md)'s designated set (T-047): a Hood with fewer than 2 curated places may not be designated.
- **APIs / contract:** no new writes. Reads Hood geometry to attribute a Been place to a Hood, and the designated flag with the rest of the static Hood payload.
- **Architecture notes:** V1 adds no identity, so Passport is device-local for the same reason Places is — it inherits that store rather than adding another. `SALVAGE.md` has nothing reusable here; `Services/AuthService.swift` is BURN and nothing here reopens it.
- **Dependencies:** **hard upstream on `places-been-saved`** (the Been signal) and `map-hoods-heat` (Hood polygons for attribution, plus the chrome the Profile button sits in). Nothing depends on Passport.
- **Open technical questions:** where `place_type` comes from (see below — the biggest one); whether progress computes on device or server once a live pipeline exists; how a Been place is re-attributed if a Hood polygon later changes.

## Assumptions

- **[ASSUMPTION]** Stickers derive from Been rows with no separate store, so Passport inherits Places' device-local storage — and its loss on reinstall.
- **[ASSUMPTION]** Undesignated Hoods are absent from the progress view rather than shown at zero (req 4).
- **[ASSUMPTION]** No reward exists for answering local-QA, because none is specified. If one is intended, req 3 is incomplete.

## Open questions & risks

- ~~**Two numbers are missing and this cannot ship without them:**~~ **One is now decided; one is still open.** The **threshold is 2** (decision #45, 2026-08-04, `product`) — Local per Hood means *you came back*, not *you completed the Hood*: one 20-minute dwell is a tourist having lunch, two distinct curated places each earned by a separate dwell is someone who returned on purpose. The value was bounded to [2, 3] before judgement entered (floor: at 1 the status is true on first contact; ceiling: the smallest curated place count across designated Hoods, 3 nominal) and 3 was rejected because it makes Local identical to completing a Hood's catalogue with zero margin. **Confirmed at acceptance 2026-08-07 (T-048), with the ceiling corrected: counting only open places, two of the three designated Hoods hold 2, not 3, so the admissible range is [2, 2] and 2 is forced rather than chosen.** The zero-margin property 3 was rejected for is therefore already true of 2 in those two Hoods — which the threshold cannot fix, because no smaller value is admissible. **The dataset is what has to move:** a third open curated place in `kerem-hateimanim` and `neve-tzedek` restores the margin. **[ASSUMPTION]** 2 is correct for roughly 3–6 curated places per designated Hood; re-derive if a designated Hood leaves that band. **Still open and not invented here:** which Hoods are designated (T-047) — three are provisionally seeded (`florentin`, `kerem-hateimanim`, `neve-tzedek`), derived from being the only three with curated places.
- **The museum sticker's glyph is Aviran's call, and it is the only thing left open on this feature.** `building.columns.fill` depicts a columned building front — but it is also Apple's conventional *bank* glyph in Wallet/Finance contexts, and `qa`'s blind read (2026-08-07) came back "bank or courthouse," not museum. It breaks no automated rule; it fails the human half of req 3's tightened pass condition on one of six types. `qa` disclosed its own method — read from SF Symbol knowledge, not a rendered screenshot with labels hidden — so a founder's ten-second look at the shipped screen is the authoritative test, not another agent round. Alternatives if he wants a swap: `theatermasks.fill`, `photo.artframe`, `paintpalette.fill`. A swap is a one-line registry + fixture change, not a rebuild.
- **Nothing in V1 produces a real Been place yet.** Every Been row today comes from a bundled fixture; the dwell/geofence detector that would produce one is T-046 / `PAS-33`, which has no PRD. Passport's own progression is therefore unobservable on a real device until that lands — and it is **launch-blocking**, not Phase 2/3 work (decision #46, 2026-08-04). Passport itself needs no change when it lands; that is what T-036's `VisitSourcing` seam is for.
- ~~**`place_type` does not exist in the data model.**~~ **Field spec'd 2026-07-30** in [`places-dataset`](../places-dataset/places-dataset.md) req 3 — a closed internal enumeration alongside, not inside, the two-value `category` (#11, #33: *"no third value, no null, no 'other'"* still holds for `category`). **Still open, and it is Aviran's:** whether an internal-only place type is the reading he intended, or whether place type is meant to be user-facing — the latter reopens `hood-place-detail` req 6 and `search-quick-filters` req 3. Until confirmed, `places-dataset` carries it as an **[ASSUMPTION]**. The dataset still has to be authored either way; without it V1 ships two sticker shapes and #29 is not met.
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
| 2026-07-30 | `place_type` and `designated_for_progression` given owning PRDs; the Local threshold's *dataset-sizing* consequence surfaced | Standing rule, founder-direct 2026-07-30. Both fields were flagged as missing and left as open questions with no deliverable behind them; the threshold's effect on how many places a designated Hood needs was not noticed at all |
| 2026-08-04 | **Local threshold fixed at 2, no longer provisional** (decision #45, T-048/`PAS-35`, `product`). PRD → Draft v2 | TRD D6 picked 2 from fixture observability and explicitly disclaimed being a product judgement, which is not a basis a number can ship on. Re-argued from what "Local" should mean to a user — *came back*, not *completed the Hood* — inside a [2, 3] range that the data fixes independently of taste. Not escalated to Aviran: decision #40 locked the mechanic, the strategy states no number, and *"a set of hoods Passenger designates"* puts the parameterisation with the company |
| 2026-08-04 | The detector this PRD depends on is recorded as **launch-blocking**, not Phase 2/3 | Decision #46 (`product` scope gate, T-046/`PAS-33`). The prior "not launch-blocking" framing was true only of *build sequencing* — the consumers compile against stand-ins. Without the detector this feature ships permanently empty on a real device |
| 2026-08-05 | **REJECT at acceptance (T-037).** Req 3's shape bullet and req 7's label bullet each gained a falsifiable pass/fail criterion, added at acceptance per L-009. PRD → Draft v3 | The build ships six abstract geometric stickers assigned one per `place_type` (café→circle, restaurant→triangle, bar→diamond) and speaks the geometry (*"Dr. Shakshuka, triangle sticker"*). Neither bullet was falsifiable: TRD §9 row 3's pass condition checked totality and symbol resolution only, so no gate downstream had anything to fail it on — L-009 exactly |
| 2026-08-07 | **ACCEPT at acceptance (T-048/`PAS-35`): threshold stays 2.** Req 4 gained a reachability pass/fail bullet (L-009); the data-sourcing line's "≥2 curated places" corrected to ≥2 *open* places. PRD → Draft v4 | Re-derived from source: `LocalStatus.swift:27` is the sole declaration site, every other reference reads it. The value is forced, not merely chosen — counting only open places the ceiling is 2, not 3, so [2, 3] collapses to [2, 2]. What no gate could fail was the dataset guard behind it: both the PRD line and `PassportBundleInvariantTests` count rows, not visitable places, so they stay green if every place in a designated Hood closes (already filed as T-068/`PAS-64`) |
| 2026-08-08 | **ACCEPT WITH NOTES at acceptance (T-037).** F1/F2 both resolved by `passenger-code fe1c8ef`; req 3's blind-read pass condition tightened (L-009); museum glyph escalated to Aviran. PRD → Accepted v5 | The rejected circle/square/triangle bijection is gone — six real depicting SF Symbols, a build-time gate that fails on any geometry word, and a VoiceOver label that speaks the depiction. What still had no objective check was a blind answer that names a *plausible but wrong* kind of place: the fail list was closed, so "bank" for the museum glyph passed by silence. Criterion tightened; the one glyph it now catches is a taste call, escalated rather than agent-debated |
| 2026-08-05 | **TRD D12's premise rejected**: req 7 bullet 1 and `places-dataset` §4.4 were never in conflict | §4.4 forbids rendering the raw `place_type` string; it does not forbid naming what a place is in the app's own words. The contradiction D12 resolved existed only because the shape vocabulary was abstract. A depictive sticker's spoken noun satisfies both documents, so the deviation is rejected along with its cause rather than confirmed |

