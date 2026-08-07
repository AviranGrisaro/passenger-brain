# Tourist-Trap Flag & Local QA — PRD

**Status:** Accepted (Build Phase 1) 2026-08-03 — reqs 1–4, 6, 7, 9 verified; req 5 built-but-unobservable and req 8's notification/geofence half not built in this phase, both named in the Decisions log.
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#rollout-sequence)
**Owner:** Aviran Grisaro
**Last updated:** 2026-07-30
**Mechanic confirmed:** decision #37 (boolean replaces the Local · Mix · Tourist tag) and #42 (public copy: "tourist-heavy spot"). Fills the hole `map-hoods-heat` left open.

## Description

- Every Hood and every place carries **one boolean tourist-trap flag** and nothing else on this axis.
- Public copy is always **"tourist-heavy spot"** (decision #42); "tourist trap" is internal vocabulary only.
- Rendering is already specified and **not re-derived here** — `design/map-rendering-spec.md` §§2–3, §4, §7; `design/ux-flows.md` §6.
- A geofence-verified visit fires a local notification, which drops a binary Yes/No toast that corrects the flag (decision #24, made binary by #37).
- **Not in scope:** the algorithm that proposes a flag value (`data-eng/discovery-engine-spec.md`, `data-engineer`'s); heat; the Hood and place sheets; the Places list; Passport; any reward for answering; a "hide tourist-heavy spots" filter (`ux-flows.md` §6 makes that a fresh decision).

## Motivation

- Strategy, verbatim: *"**Tourist-trap flag, boolean (1/0), no local tags** — replaces the three-way **Local · Mix · Tourist** vibe tag (decision #18) entirely."*
- Strategy, verbatim: *"The algorithm proposes; real users, asked in-app whether a spot is actually local, verify and correct it."*
- Without this layer the map is heat alone — *"the half of this product anyone already gets from Google Maps."*
- Positioning rests on it: *"nobody treats packed-vs-local as two separate signals on one map."*

## Requirements

### Must-have (P0)

1. **One boolean per Hood, one per place; no graduated value survives.**
   - [ ] The only rendered states are flagged and not-flagged — no score, no percentage, no third value.
   - [ ] No "Local", "Mix", "Tourist", "super local", "very local", or "touristy" survives as a tag value in app or data (#37 supersedes #18 and #6).
   - [ ] No user-facing string reads "tourist trap" (decision #42).
   - [ ] A Hood's flag is its own value, never aggregated from its places (`map-rendering-spec.md` §3).

2. **The flag never shares a visual channel with heat.**
   - [ ] Heat is always the area fill; the flag is always the Hood's outline stroke (§2).
   - [ ] Flagged state reads without colour — weight and/or dash, not hue alone (`design-principles.md` §3).
   - [ ] Moving the time slider never changes **which** Hoods carry a stroke — the flagged set is time-invariant, and no unflagged Hood ever gains one. An already-flagged Hood's stroke *style* does switch between plain and busy+flagged as its density crosses the threshold for the selected hour (req 5). *(Corrected at acceptance 2026-08-03: the original "changes no stroke" contradicted req 5, which is per-hour by definition. TRD D3 built this reconciled reading; `map-rendering-spec.md` §3 is the locked design it matches.)*

3. **Progressive disclosure by zoom matches `map-rendering-spec.md` §2's table, row for row.**
   - [ ] City-wide shows no stroke and no label on any Hood; neighborhood adds both on flagged Hoods only; close keeps the stroke and drops the label.
   - [ ] No pin carries a flag encoding at any zoom — not a badge, fill, or shape variant (§4).

4. **Not-flagged and not-yet-rated both render blank.**
   - [ ] A not-flagged Hood renders no stroke and no label, at every zoom.
   - [ ] A not-yet-rated Hood renders identically to not-flagged, resolved on tap by the Hood sheet: the sheet always carries one line stating exactly one of three states — "Tourist-heavy spot" / "Not a tourist-heavy spot" / "No local rating yet". *(Pass condition added at acceptance 2026-08-03: "resolved on tap" named no surface and no strings, and the Hood sheet had no flag element at all. TRD D5 built this line; confirmed. L-009.)*
   - [ ] Storage still distinguishes the two, because req 7 depends on it.

5. **Busy + flagged replaces the plain treatment; it never stacks.**
   - [ ] A flagged Hood above the busy threshold for the selected hour renders exactly **one** stroke treatment, distinct from the plain flagged stroke.
   - [ ] Its label reads the combined form ("busy and tourist-heavy"), not two labels.
   - [ ] A busy but not-flagged Hood renders no warning treatment.

6. **A place's flag is one line in its detail modal, and nowhere else.**
   - [ ] A flagged place shows one text line reading "tourist-heavy spot", never a colour chip alone.
   - [ ] A not-flagged place shows no line — silence, matching the map. **[ASSUMPTION]**
   - [ ] It is independent of the "permanently closed" badge (#38): a place may carry both, either, or neither.

7. **VoiceOver states the flag even when nothing renders** — labels per `map-rendering-spec.md` §7.
   - [ ] A Hood's label always states its status in speech, in both states, and a not-yet-rated Hood says so distinctly ("no local rating yet").
   - [ ] Busy+flagged gets its own label, not two announcements to combine (`ux-flows.md` §9 Q5).
   - [ ] Pins never announce the flag, matching the visual rule.

8. **The local-QA ask is binary, post-visit, and asked once.**
   - [ ] A geofence-verified visit fires at most one local notification; tapping it drops a top-anchored, non-blocking toast (#24).
   - [ ] The toast asks one question with exactly two targets, **Yes / No** (#37).
   - [ ] Ignoring it auto-dismisses, with no reminder for that visit.
   - [ ] A place already answered by this install never fires again.
   - [ ] Offline: the toast still renders; the answer queues on device and syncs later.
   - [ ] Notification permission denied: no toast ever fires, and **no fallback ask appears in any sheet** — #24 replaces the embedded ask, never supplements it.
   - [ ] Cadence caps at one local-QA notification per day per install. **[ASSUMPTION]** — `ux-flows.md` §9 Q1 recommends it; unconfirmed.

9. **One answer is a signal, not a write to what everyone sees.**
   - [ ] Answering once never changes the flag any other viewer sees.
   - [ ] The rendered flag changes only through the pipeline that owns it, never directly from a toast answer.
   - [ ] An answer is recorded even when it agrees with the current flag.

### Nice-to-have (P1)

- The Hood sheet's place list marking which places are flagged.
- A foreground arrival dropping the toast directly, skipping the notification (`ux-flows.md` §4).

## Technical design

- **Data model:** `hoods.is_tourist_trap` and `places.is_tourist_trap` as **nullable booleans** — `null` not yet rated, `false` not flagged, `true` flagged. Three storage states, two rendered states, which is what reqs 4 and 7 need. Public-read.
- **Data model:** `local_qa_answers` (place_id, answer, install_id, answered_at). Insert-only, never client-readable; unique on (place_id, install_id) enforces ask-once.
- **Data sourcing — the flag ships with a value, and this PRD does not produce it (added 2026-07-30, standing rule).** Neither column exists yet: `hoods.is_tourist_trap` is [`prds/hood-dataset/`](../hood-dataset/hood-dataset.md) req 5, `places.is_tourist_trap` is [`prds/places-dataset/`](../places-dataset/places-dataset.md) req 6, both nullable so req 4's three storage states hold. The **values** come from the proposing algorithm (`data-eng/discovery-engine-spec.md`), which does not exist. If it does not land, every row ships `null` and this feature renders blank everywhere — legal per req 4, but it means V1 launches with only half its signal. Named as a risk below, not assumed away.
- **APIs / contract:** the flag ships inside the existing Hood and place payloads and caches with them — static reference data, no Realtime, not hour-bound. An answer is one insert, queued offline.
- **Architecture notes:** no accounts in V1 (strategy: *"no accounts/login added"*), so an answer carries an anonymous install id — `SALVAGE.md` marks `Services/AuthService.swift` BURN, *"spec it fresh — anonymous-first."* `Models/DensityContract.swift` REUSE and load-bearing: it encodes the never-one-blended-score rule. **`Features/Map/LocalnessBadge.swift` is marked REUSE but must not be** — it renders the five superseded vibe tags.
- **Dependencies:** `map-hoods-heat` (Hood geometry, stroke channel) and `hood-place-detail` (the modal line) first. The dwell/geofence detector is shared with Places and Passport — one detector, three consumers, `data-engineer`'s.
- **Open technical questions:** how many answers move a flag, and whether that runs on schedule or on write; whether the flag rides the cached Hood payload or its own endpoint; what happens when a place's flag disagrees with its Hood's.

## Assumptions

- **[ASSUMPTION]** A single answer never flips the displayed flag (req 9). If Aviran wants immediate flipping, req 9 is wrong and abuse becomes a live question.
- **[ASSUMPTION]** A not-flagged place shows no line in its modal (req 6). A sheet has room for one, unlike the map, so the opposite call is defensible — designer's.
- **[ASSUMPTION]** One notification per day per install (req 8) — `ux-flows.md` §9 Q1's recommendation, not a decision.

## Open questions & risks

- **Cold start:** a new city has no users to ask, so the flag starts entirely algorithm-proposed with nothing verifying it (strategy, Key risks).
- **Worse than cold start: the proposer may not exist at launch.** Every requirement here is about rendering and correcting a value; nothing in V1 is scheduled to *produce* the first one. A dataset of all-`null` flags passes every bullet in this PRD and ships a product strategy itself calls *"the half anyone already gets from Google Maps."* Aviran's, and it should be answered before this feature reaches `build`.
- **Nothing rewards answering.** Strategy's stamp write-up folds in *"rewards for answering local-QA questions"*, but #29 ties stickers to Been places and #40 retired the ladder carrying the rest. Aviran's call.
- **Notification-denied is a named coverage gap** (§9 Q8): that user is never asked about any visit.
- **Copy-fit at Hood level:** §3 renders "Tourist-heavy spot" at a Hood centroid, but a Hood is a polygon. `designer`'s (PAS-8 residual).
- Background Location Always reliability gates the visit detection this loop needs (§9 Q4).

## Decisions log

| Date | Decision / change | Why |
|---|---|---|
| 2026-07-30 | PRD created | Decision #37 unblocked the item held at PAS-10 (PAS-6 item 1) |
| 2026-07-30 | Written against the boolean model only, no graduated read retained | #37 is a clean supersession of #18 — the graduated tag is gone |
| 2026-07-30 | Rendering referenced, not restated | `map-rendering-spec.md` §§2–3 were already rewritten against #37 by `designer` (PAS-8) |
| 2026-07-30 | Nullable boolean over a separate `is_rated` column | Accessibility (req 7) needs three states stored while the map renders two |
| 2026-07-30 | Data-sourcing bullet added; the "nothing produces the first flag value" gap promoted from implicit to a named risk | Standing rule, founder-direct 2026-07-30. The PRD scoped the proposing algorithm out — correctly — but never said the feature ships blank if it never lands |
| 2026-08-03 | **D3 CONFIRMED** — req 2 bullet 3 was the wrong requirement, not the build | The TRD's reconciled reading (flagged *set* is time-invariant; an already-flagged Hood's stroke *style* varies with the hour) is what `map-rendering-spec.md` §3 locks, and the only reading under which req 5 can exist at all. Req 2 bullet 3 rewritten above |
| 2026-08-03 | **D5 CONFIRMED** — the three-state Hood-sheet line is accepted as new UI, and req 4 bullet 2 now carries its pass condition | "Resolved on tap by the Hood sheet" named no surface and no strings, and `HoodSheet.swift` had no flag element — a requirement no gate could fail. The three-state line is the only construction that distinguishes not-flagged from not-yet-rated, which req 4 bullet 3 and req 7 both depend on |
| 2026-08-03 | **Req 5 (busy+flagged) accepted as built-but-unobservable, not as passed** | `DensityStore` has no seed path in Build Phase 1, so `band` is `nil` for every Hood at every hour and `.busyWarning` can never render. The pure `FlagStroke.treatment(for:band:)`/`HoodSpeech.label` paths are built and unit-covered. Verified against source, not taken from the TRD's claim. Re-verify when T-032's C10 density seed lands |
| 2026-08-03 | **Req 8's notification + geofence half is out of Build Phase 1**, confirming TRD §1's boundary | No dwell detector and no `UserNotifications` link exists anywhere in the app, by design — the PRD assigns the detector to `data-engineer` as "one detector, three consumers." It now has a board row and an owner (`T-046`/`PAS-33`), which it did not when this PRD was written. Bullets 1 and 6 and the "syncs later" half of bullet 5 are re-verified there and at B1 (Build Phase 2), not here. Everything else in req 8 — binary toast, auto-dismiss, ask-once ledger, rolling-24h cap, denied-suppression, device-local queue — is real and verified |
| 2026-08-03 | Fixture completeness gap named, non-blocking | No place in `places-tel-aviv.json` is both permanently closed **and** flagged, so req 6 bullet 3's independence claim is true by construction (separate views, separate fields) but not demonstrable in the demo. One fixture row fixes it — T-051 |

| 2026-08-07 | **Fixture gap CLOSED** (T-051/PAS-39, `passenger-code eecccd5`) — req 6 bullet 3's independence is now demonstrable, not only true by construction | `kerem-carmel-spice-corner` is the sole place carrying both `permanently_closed` and `is_tourist_trap`, and the file keeps a closed-only (`neve-nachum-gutman-museum`) and a flagged-only (`florentin-anna-loulou-bar`) control, so all three combinations render. The two cues live on separate surfaces — closed badge on `PlacesListRow`, "Tourist-heavy spot" in `PlaceDetailModal` — so neither can mask the other. Same row also closes `places-been-saved` req 4 bullet 3. **Standing data need:** any future regeneration of `places-tel-aviv.json` (T-042's `export_places.py`, Build Phase 2) must preserve all three combinations, or both bullets go undemonstrable again |
