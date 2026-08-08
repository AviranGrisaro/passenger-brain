# Time Slider — now → +12h — TRD

**Task:** T-032 · **Linear:** `PAS-15` (§9 amendments carried at `PAS-51`; v6 re-scope at `T-077`/`PAS-51`; v7 retirement at `T-090`/`PAS-88`) · **Status:** v7 — §9 amendment (row 5b retired; rows 2b/4/5/6/7d re-targeted, narrowed or re-populated; row 6(a) left **open** and bounced to `product`), C16 retired, C17 added, C13's verify item 5 re-targeted, **D4 and D5 amended**, **§2.3's and §10's co-presentation claim restated on its live mechanism**, no `trd-review` re-run owed. **Written concurrently by two `architect` sessions — see Provenance.**
**Owner:** architect · **Date:** 2026-07-30 · **Revised:** 2026-08-08 (v7)
**PRD:** [`time-slider.md`](./time-slider.md) (Draft v9 — req 5's rendered-legibility bullet added at acceptance 2026-08-03)
**Design reference:** [`design/phase-1/time-slider-design.md`](../../design/phase-1/time-slider-design.md) (v4) + its mockup — **informational input, not a gate.** The pre-code design gate was retired 2026-08-02 (`BOARD.md` lifecycle section). Where this TRD and the design spec disagree, this TRD wins and says so (§8).
**Builds on:** [`prds/map-hoods-heat/TRD.md`](../map-hoods-heat/TRD.md) (T-031, shipped and accepted). Extends that module layout; does not restate it.

**What changed at v7 (2026-08-08) — T-090/`PAS-88`: the in-modal hour path was deleted by founder order, so the rows that measured it are retired, not re-targeted again.** **§9 and §11 move; so do two decisions (D4, D5) and two prose claims that rested on a deleted surface (§2.3's co-presentation bullet, §10's matching risk row).** No *contract* in §4 and no *scope* moves, and nothing here re-opens a design: every edit either records that something already deleted is deleted, or restates a still-true guarantee on the mechanism that actually delivers it today. `trd-review` is not re-run — same posture as v4/v5/v6.

**Provenance — v7 was written by two `architect` sessions at the same time, in the same shared working tree, and that is disclosed rather than smoothed over (`CLAUDE.md` rule 2; v3 had to say a version of this too).** When this session opened the file, part of v7 was already there uncommitted: the "what happened"/"second deletion"/re-audit header blocks, §9's "read the standing rules as history" note, and the rewrites of **rows 2(b), 4 and 5**. Mid-pass, while this session was editing §2.3 and §8, the **other session landed row 5b's retirement, row 6's rewrite, and all of §11** (C16 retired, C17 added, the C4/C5 preamble). Neither half is a re-review of the other; they are complementary, they were checked for contradiction before this session's last edit, and the split of authorship is recorded below so a reviewer can attribute anything they disagree with. **`chief` should treat "two sessions on one T-090 TRD" as the routing defect it is** — no coordination cost was paid here only because the two halves happened not to overlap. **One collision did fire, and it is exactly the one `CLAUDE.md` rule 2 describes:** commit **`passenger-brain 8ed7fbc`** staged this file by explicit path while this session's edits were uncommitted in it, and carried this session's rewritten **`Status:` line** — which announces "D4 and D5 amended" and "§2.3's and §10's co-presentation claim restated" — under a commit message stating "§2–§8 and §10 untouched." Both were true of the *file*, neither of *that commit*; the work they name is in the commit that follows. Nothing else of this session's was swept. Disclosed here rather than quietly reconciled, because a status line that describes work a commit does not contain is the same defect this document keeps finding one level down.

**Everything this session let stand, it re-verified against shipped source at `passenger-code c6398f9` rather than inheriting.** `Passenger/HeatModal/` contains `HourFormat.swift` and nothing else; `EdgeHourZone.swift:89-90` is the sole surviving writer with the signpost bracketed around it; `hourSlider`/`hourReadout`/`hourSegmentCard` return zero hits repo-wide while `searchOverlayCard` (`SearchOverlay.swift:117`) is what C16's identifier became; `EdgeHourZone` carries no accessibility modifier of any kind, so row 6(a)'s gap is real. All of it checks out. One thing did not, and was true of the draft at the moment this session read it: **its header announced rows 5b/6(c) retired, C16 retired and C17 added while the §9 table and §11 were still untouched**, leaving row 2(b) pointing at a **C17 that did not exist** — a claim with nothing behind it, which is this table's own defect class one level up. The other session closed that gap directly; it is recorded because "the header promised it" is not evidence that a row was written.

**What this session wrote.**

- **D5 amended.** Its button-path half ("native `Slider`") is moot — nothing native ships. Its surviving half is now unconditional, and **PRD req 6's inactive-rail 3:1 exemption is retired** in step with `product`'s side (`time-slider.md` req 6, Q5, 2026-08-08): the exemption was conditioned on a platform-drawn control, and there is no longer one anywhere in this feature. §4.12's "explicitly not asserted" carve-out for the native thumb and rail is spent with it.
- **§2.3's co-presentation bullet and §10's matching risk row restated.** Both said req 2's "any open sheet is unchanged by an hour change" holds because the heat modal and a system `.sheet` are never co-presented. With no modal that is vacuously true and argues nothing. **The live reason is `EdgeAvailability.liveEdges` returning `[]` while any detail surface is up** — verified in source, and it turns out to be *stronger* than the claim it replaces.
- **A citation defect, flagged from the PRD side by `product` and confirmed here.** The co-presentation claim was **D4 in TRD `2f955fe`**. Current **D4 is a different decision** ("the shipped modal contains the slider only"), so every "(D4)" attached to co-presentation is pointing at the wrong row. Fixed in this file; `product` fixed the PRD's Technical-design bullet; two other files still carry it and are named below, in other agents' lanes.
- **Row 7(d) re-targeted — a re-audit finding the dispatch did not name.** Sub-checks (d1)/(d2) exercise `HoodSheet` at `.medium` and `.large` and lean on `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` at `MapScreen.swift:186`. **T-079/`PAS-73` moved every detail surface off `.sheet()`**: a repo-wide grep at `c6398f9` finds **zero live `.presentationDetents` and zero live `.presentationBackgroundInteraction`** — every hit is a comment. Two detents that no longer exist cannot be a pass condition.
- **C13's verify item (5) re-targeted in step with row 7(d)**, so the build step and the gate cannot disagree about a state the app can no longer enter. C13 is shipped; the edit records what the check means now, not new work.
- **Row 6(d)'s contrast population re-derived — the second re-audit finding.** The other session had already flagged `SliderFill` as a token nothing draws; **`PillSurface` is the identical case and makes it two of five asserted pairs**, which turns an aside into a pass-condition problem: the requirement is about *rendered* pairs and the check is over *declared* ones. The live population is now enumerated in closed form against what `EdgeHour/` actually draws, with the two dead pairs retained explicitly as re-introduction backstops that discharge nothing.

**How much of this dispatch was found rather than assigned, and why that is the expected result.** T-090 named rows 5b/6(c), C16, D5, §2.3/§10 and the citation defect. The whole-table re-audit `architect.md` requires on **any** amendment (L-047) turned up row 7(d)'s dead detents, C13(5) behind it, and row 6(d)'s second dead token — none of which would have surfaced from the six named items alone, and all of which are the same shape as the ones that were.

**What happened.** Aviran, direct: *"no need 12h slider on the modal if we have this on the sides, remove the 12h sliders from the search modal."* **T-081/`PAS-76`** shipped exactly that (`passenger-code b2dc981`, merged `2a2a4ac`; `product` ACCEPT WITH NOTES, closed `Done`). Deleted outright: `SearchOverlay`'s Search/Hour segmented control and its `hourContent`, **`Passenger/HeatModal/HourSlider.swift`**, **`HourReadout.swift`**, `PassengerUITests/SearchHourSegmentInteractionTests.swift`, `PassengerTests/SearchOverlayHourGuardTests.swift` and `PassengerUITests/HourRepaintPerformanceTests.swift`. `SearchButton`'s label reverted `"Search and hours"` → `"Search"`; C16's `hourSegmentCard` identifier survives renamed to **`searchOverlayCard`** (`SearchOverlay.swift:107-114`). **`EdgeHourZone`/`EdgeHourTrack` are now the sole hour-selection mechanism** — `EdgeHourZone.swift:90` is the only remaining UI writer of `selectedHour`, confirmed by `product` at acceptance by grep and on a rendered app.

**This is the second deletion of this row's surface and the reason it is retired rather than re-pointed a third time.** v6 re-targeted row 5b off `HeatModalCard` onto `SearchOverlay`'s Hour segment after T-078 deleted the first surface. T-081 deleted the second. There is no third surface: the in-modal hour path is gone by product decision, not replaced, so **rows 5b and 6(c) have nothing left to measure and are retired with their reasoning stated in place** (`architect.md`: retire explicitly, never leave a dangling row). C16, whose only purpose was to build that suite, is retired with them.

**Whole-table re-audit (L-047), and it found more than the two rows this pass was dispatched for.** An amendment re-audits the entire §9 table, and this deletion reached four rows the dispatch did not name. All are amended here, with the extension of scope stated plainly rather than done quietly:

- **Row 2(b)** drove the 400ms `HourRepaint` budget through `hourSlider.adjust(toNormalizedSliderPosition:)`, and `HourRepaintPerformanceTests.swift` was deleted with it. `ios-developer` disclosed the gap in T-081's own commit message (*"rewriting it against `EdgeHourZone`'s raw coordinate-drag gesture is a separate, nontrivial task — flagged as a coverage gap, not attempted here"*). The signpost instrumentation survives and is now wired to the edge writer (`EdgeHourZone.swift:89`), so the row is re-targeted and marked **owed and currently unrun**, with **C17** as the step that owes it. A P0 bullet whose only test was deleted is not a passing row.
- **Row 4** named an intra-surface path — Hour segment → Search segment → Hour segment — that no longer exists, and a "read-by-slider" reader that no longer exists.
- **Row 5**'s rendered half compared a "now" mark against an ordinary stop. `HourSlider`'s tick overlay was one of its two subjects; only `EdgeHourTrack`'s tick survives, and that view is `.accessibilityHidden(true)` (§4.11), so the check's *layer* changes.
- **Row 6(a) is the finding this pass would have missed had it stopped at the two named rows, and it is bounced to `product`, not answered here.** `HourSlider` was the app's only VoiceOver-operable hour control. §4.11 hides `EdgeHourTrack`/`EdgeHint` from assistive technology *on the stated grounds* that "req 6's assistive-tech bullet is satisfied entirely by the button path" — **T-081 deleted that path, so §4.11's premise is now false and PRD req 6's VoiceOver bullet has no implementation, not merely no test.** `EdgeHourZone` carries no accessibility modifiers of any kind (checked at `2a2a4ac`), so there is no adjustable element anywhere. Whether that regression is accepted or the bullet is re-homed on the edge path is a **product** call with a design consequence, and `architect.md` says a P0 requirement admitting no statable pass condition is bounced, not invented around. **Row 6(a) is therefore left open and marked, not retired and not passed.**

**Deliberately not touched, per this pass's scope — with two named exceptions.** §2–§5 and D1–D6 still describe `HeatModalCard`/`HeatButton`; that drift was already disclosed at v6 and is unchanged by this pass — read it as history, not as build instruction. **The exceptions are surgical and both were named in the dispatch:** §2.3's second consequence bullet and D4/D5, because those three were not describing a dead surface *in passing* — they were carrying a **live guarantee** (req 2's sheet bullet) and a **live constraint** (the contrast exemption) on a dead premise, which is the difference between stale prose and a wrong instruction. Everything else in §2–§5 stays as written. **§10's three v6 risk rows about row 5b's re-target now describe a retired row**; they are left standing as the record of why the row was written and re-written, not as live risks. §10's **C15 risk row** is likewise left as written, but its stated justification is spent: C15's `UITestOverrides` still ships (`MapScreen.swift:699`) and **no test passes `-uiTestDynamicTypeSize` any more**, because rows 5b and 6(c) were its only consumers. Its doc comment was corrected separately at T-088/`PAS-86` (`passenger-code b90ba83`). Whether a test-only seam with zero consumers stays in shipping code is a call for whoever owns the follow-up, flagged rather than decided here.

**What changed at v6.1 (2026-08-07) — `architect` ratifies the standing rule `product` added at acceptance, and promotes it out of this file.** `product`'s T-077 acceptance REJECT added a rule to §9's preamble — *a sub-check sequenced behind a known-failing sibling is unrun, not passed* — and flagged it as owed ratification by `architect`. **Ratified as written, and generalised:** it is not a property of `SearchHourSegmentInteractionTests`, so it now lives in **`architect.md` §9's bound rules** (rule 4 of five) and binds every TRD in this workspace; the same abort-then-report-one-line shape is produced by `try #require`, `XCTUnwrap` and any early `return` in a shared helper, not only by `continueAfterFailure = false`. Two clauses added on ratification: per-sub-check *execution* is reported, and the row's **layer column** carries the requirement (because `qa` reads rows, not preambles). Applied here to row 5b's and row 6's layer columns, and lifted into the five other TRDs that carry §9 UI-test rows. **Whole-table re-audit against the new rule (L-047):** rows 1–5, 5b, 6 and 7 checked; only **5b(iii)** and its delegate **6(b)** co-locate with an assertion known to fail (the 31pt `hourSlider`, T-081/`PAS-76`), and both are fixed above. Nothing else in §2–§11 moves; no `trd-review` re-run owed.

**What changed at v6 (2026-08-07) — T-077/`PAS-51` re-scope: row 5b/6(c) re-targeted at `SearchOverlay`, because the surface they measured was deleted mid-build.** No decision, contract or scope moves; §9 and §11 do. `trd-review` is not re-run — this changes a gate, not a design, same posture as v4/v5.

**What happened.** `ios-developer` built C15 (`passenger-code 967b7c2` — `UITestOverrides.swift`, surviving on `main` and still wired into `MapScreen.swift`) and fixed `PAS-51` findings 2/3/5 (`8fe34d3`), but before landing row 5b/6(c)'s rendered check a concurrent session shipped **T-078/`PAS-60` + T-079/`PAS-73`** (`44eea9c`, `ddbc7de`): `HeatButton.swift` and `HeatModalCard.swift` are **deleted**, the map-hour surface is now the **"Hour" segment of `SearchOverlay`** (`Passenger/SearchSheet/SearchOverlay.swift`), and `NavSurface.heat` is gone — `chrome.presented == .search` covers both segments. Entry path is two taps, not one: nav-row `SearchButton` (label `"Search and hours"` since `PAS-75`) → the `"Hour"` picker segment. That session's own `SearchHourSegmentInteractionTests.swift` header discloses the rendered check as not carried over — a correct disclosure, and this revision is the answer to it, not a re-review of it.

**The row was not ported forward. Three of v5's pass conditions are now false-by-design and would fail a correct build**, and re-targeting them at the new identifiers would have shipped a gate that fails what T-078/T-079 deliberately built:

1. **The card's height is a fixed screen fraction (`0.45` compact / `0.92` expanded, `SearchOverlay.swift:56-57`), not content-sized.** v5's row 5b reasoned explicitly "the card is *sized to content* (§2.3 z5), so its height is a function of text size" — false on this surface. Two consequences: any pass condition on the **card's own frame** is now *trivially satisfiable* at every text size and cannot fail, and the failure mode it guarded against is replaced by a different one (item 4).
2. **The card is deliberately flush to the true bottom edge** (`.ignoresSafeArea(edges: .bottom)`, T-079/`PAS-73`; `product`'s REJECT measured a 34pt shortfall as the *defect*). v5 row 5b sub-check (iii) asserted the card's `maxY` is **strictly less than** the safe-area bottom. **Inverted by another shipped spec — deleted, not ported.**
3. **`MapNavRow` renders *above* the card by z-order, on purpose** (drawn last at z7, `MapScreen.swift`; stated in `SearchOverlay`'s own header comment). v5 row 5b sub-check (i) required `card.frame.intersects(navRow.frame) == false` plus a ≥8pt separation. **Also inverted — deleted.** The occlusion claim that survives is about the *content*, and always was: F1 was a truncated "next day" pill, never a truncated card.

**The "unsatisfiable by design" class recurs here — checked explicitly, not assumed away, and it recurs in mirror image.** On `HeatModalCard` the defect was a clause that could never *pass* (capture at AX5, on a card clamped to `.accessibility3`). The clamp survived the merge verbatim (`SearchOverlay.maxDynamicTypeSize = .accessibility3`, `SearchOverlay.swift:52`), so that clause stays fixed the same way — capture at the ceiling, plus one check that the ceiling binds. The **new** instance is the opposite: because the card's height no longer varies with text size, a ceiling-binding assertion made on the *card* frame is true whether or not the clamp exists. **A row that cannot fail is the same defect as a row that cannot pass.** Both are fixed by moving every observable off the card frame and onto the content elements plus containment.

**Two further defects in v5's row 5b found by this pass — both were unsatisfiable on the old card too, so they are fixes, not merge fallout:**

4. **`HourReadout` is a *single combined* accessibility element** (`.accessibilityElement(children: .combine)` + an overriding `.accessibilityLabel`, `HourReadout.swift:29-34`). Its numeral, clock label and "next day" pill have **no individually queryable frames**. v5's row 5b asked for "the rendered frames of the three readout elements individually" and for "the pill's `frame.height`" — not obtainable by any test, and obtaining them would mean un-combining the element, trading a P0 VoiceOver behaviour (one spoken unit) for test convenience. The wrap check moves to the **combined row's height**, which is a real observable of the same failure.
5. **v5's positive-control strings were wrong for this codebase.** Because `.accessibilityLabel(HourFormat.voiceOverValue(readout))` overrides the visual text, XCUITest reads `"+12 hours, 03:00, next day"` — never the visual `"+12h"` that v5's row demanded "in full". That control could only ever fail. `ios-developer` hit exactly this at build and corrected it in the test; correcting it in the TRD is this pass's job.

**C15 verdict — applies cleanly to `SearchOverlay`, no adjustment owed.** `.environment(\.dynamicTypeSize, UITestOverrides.dynamicTypeSize ?? systemDynamicTypeSize)` is the **last** modifier in `MapScreen.body`'s chain (`MapScreen.swift:684`), so it covers the whole subtree including `SearchOverlay`; the clamp that receives it survived the merge and is now scoped to `hourContent` rather than a whole card — *narrower and still sufficient*, since every element row 5b measures lives inside `hourContent`. `-uiTestNow` is untouched (`MapScreen.swift:92`, `:185`). The propagation **[ASSUMPTION]** stands unchanged and still unobserved; it must now be observed against `SearchOverlay`, and if it fails that is a **BLOCKED** disclosure on row 5b, never a fall back to the source grep. One stale artifact, comment-only: `UITestOverrides.swift`'s own doc comment still names `HeatModalCard` — fixed in C16.

**Whole-table re-audit (L-047), as every amendment owes.** Beyond 5b/6(c): **row 4** named `MapChromeState.toggle(.heat)`, a case that no longer exists, and its "unchanged" claim had no positive control — both fixed; **row 2(d)** said "no modal", which named the deleted surface — reworded; **rows 5, 6(a)/(b)** are reachable only through the new two-tap entry path — noted in place; **row 6(b)**'s ≥44pt is no longer proved by the unit check alone now that the container stops growing — folded into 5b(iii). Rows 1, 2(a)–(c), 3, 7 were re-read and need nothing: the edge path (`Passenger/EdgeHour/`) is untouched by the merge and gates on the generic `chrome.isPresenting`, not on `.heat`.

**Known drift, disclosed rather than silently fixed:** §2–§5 and D1/D2/D4/D6 still describe the surface as `HeatModalCard` reached from a `HeatButton`. That naming is **superseded by T-078/`PAS-60`** — read every `HeatModalCard` in this document as "`SearchOverlay`'s Hour segment" and every `.heat` chrome state as "`.search` on the Hour segment". §2.3's z5 layering rule itself still binds, in its content form: the readout and slider must not render under the nav row. A full rewrite of §2–§5 is deliberately **not** in this pass's scope — T-032 is `done`, the surface belongs to `nav-row-v2-redesign.md` now, and rewriting a shipped feature's architecture sections to match another spec's build would make this TRD claim ownership it doesn't have.

**What changed at v5 (2026-08-07) — `PAS-51` findings 1 and 4, plus the whole-table re-audit an amendment owes (L-047).** Two rulings were asked of `architect` and both are answered here; neither changes the design, and no contract, decision or scope moves.

- **Finding 1 — the AX5 half of row 5b is *not* amended to accept a source grep, and is *not* BLOCKED.** A render-based check at accessibility text sizes **is** achievable on this machine — just not through either mechanism that was tried. `-UIPreferredContentSizeCategoryName` and `simctl ui <udid> content_size` are both confirmed dead on this toolchain (Xcode 17F113 / iOS 26.5), documented live at T-038/`PAS-29` and again at `PAS-51`. But nothing about this feature requires the *system* content size to move: SwiftUI's `.dynamicTypeSize(_:)` environment value is ours to set, and `HeatModalCard` already reads it. A launch-argument-gated override at the composition root renders the real card at a real accessibility size, in the real `ZStack`, with real frames queryable from XCUITest — a genuine rendered check, not a proxy. That seam is **C15** below. Row 5b is amended to name it, and to fix a second, larger problem the finding exposed: **"capture at AX5" became unsatisfiable the moment `HeatModalCard` gained its `.accessibility3` ceiling** — a clamped card never renders at AX5 by design, so the row as written asked for an observation the design forbids. The row now checks the card at **its own ceiling**, plus one check that the ceiling actually binds (request AX5, assert the geometry equals the AX3 capture). The existing `HeatModalCardLayoutGuardTests` source grep stays as a regression backstop and is stated as such — it cannot discharge this row, and no row is discharged by the thing its own Layer column rules out by name.
- **Finding 4 — the wall-clock dependency is *not* an accepted limitation. It needs the clock injected, and the injection is small.** `HourFormat.readout` and `DensityStore(now:)` are both already clock-injectable; only the composition root hardcodes `Date()` (`MapScreen.swift:177`, and `DensityStore()`'s defaulted initialiser). So the "next day" pill — row 5b's stated positive control, and the exact element F1 truncated — renders only when the suite happens to run after local noon. A control that is absent for half of every day makes the row **unrun for half of every day while reporting a pass**, which is the same failure shape as an empty-set pass condition. Same seam as finding 1: **C15** adds a launch-argument fixed instant that `MapScreen` passes into both call sites. Not an app-wide clock abstraction — the units already take one.
- **Whole-table re-audit.** v4's own scope note admitted rows 1–7 had never been checked against the three standing rules. An amendment re-audits the entire table (`architect.md`, L-047), so this pass did: **rows 2, 3, 5 and 7 gained positive controls or non-zero counts they were missing**, and **row 6(c) had the identical AX5 defect as row 5b** and is fixed the same way. Rows 1 and 4 were checked and needed nothing. The scope note is replaced accordingly.

**What changed at v4 (2026-08-03) — T-055.** One thing: **§9 gains row 5b**, the verification row §2.3's z5 layout rule never had. Nothing else in this document changes — no contract, no decision, no build step, no scope. **§2.3's z5 rule itself is unchanged**; it was correct as written and the build deviated from it. This is a documentation fix to the *gate*, not to the *design*, so **no `trd-review` re-run is owed and nothing here blocks `ios-developer`'s in-flight T-032 rebuild** — the rebuild's correctness is already fully specified by §2.3 z5 and by PRD v9's req 5 bullet, both of which predate this revision. Same shape as T-053's §9 amendment to the `search-quick-filters` TRD.

Why the row was missing, stated plainly because it is the third instance of one failure shape (L-009; T-046, then T-053/`PAS-43`, now this): §2.3 stated the layering rule as *architecture* and §9 never turned it into a *check*. `product`'s acceptance pass found `MapNavRow` drawing on top of `HeatModalCard`'s readout at the **default** text size — the "next day" flag truncated to "…t day", which at +12h/11:00 makes the readout state the wrong hour — after `code-review` and `qa` had both passed the build. Neither gate could have caught it: `XCUIElement.exists` returns `true` for a fully occluded label, and no source read sees an overlap. A rule with no row is a rule no gate can fail.

**What changed at v3 (2026-08-02).** `trd-review` came back split — `ios-developer` APPROVE WITH MINORS, `ios-code-reviewer` REQUEST CHANGES — so this revision resolves exactly those findings and nothing else. No decision, contract, or build step is redesigned; D1–D10 all stand as written at v2.

| # | Finding | Raised by | Fix in v3 |
|---|---|---|---|
| 1 | **Blocking.** §9 row 7 and C13 verified camera-immutability only for an inert horizontal drag (7b) and a pan starting outside the band (7c) — never for a normal, **in-band, vertical** edge slide, the one gesture this task exists to ship. D7/§2.4's central claim ("MapKit's pan recognizer is never in that touch's recognizer chain") therefore shipped on hit-test reasoning alone, with no on-device check — while §4.8 applies "confirm it, do not assume it" to a *less* central claim | `ios-code-reviewer` | §9 row 7 gains sub-check **(e)**; C13's verify-list gains the matching line; §2.4 and D7 restate the claim as a prediction this TRD requires confirmed, not as settled fact |
| 2 | Minor. §9 row 7d / C13's sheet check collapsed to one flat rule, but `MapScreen.swift:186`'s `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` makes "as it does today" two different behaviours — background-interactive at `.medium`, not at `.large` | `ios-code-reviewer` | Row 7d and C13 now exercise **both detents** explicitly, and both touch targets (sheet content, still-exposed map) |
| 3 | Minor. §4.8's `DragGesture(coordinateSpace: .named("map"))` named a coordinate space **no view in this TRD or in the shipped codebase declares** — grep confirms zero `.coordinateSpace` usages anywhere. `EdgeGeometry`'s `band`/`hour(atY:)` are documented in "this view's own coordinates," which is `.local` | `ios-developer` | Corrected to the default `.local`, with the reason stated so it isn't re-invented at build time |
| 4 | Minor. §9 row 6's Step column cited `C9, C12` for the ≥44pt button-path frame assertion, which is actually built in `C4` | `ios-developer` | Step column corrected to `C4, C9, C12` |
| 5 | Found while fixing 1–4, raised by neither review: the TRD named the shipped sheet **`HoodStubSheet`** in three places. **No such type exists** — `Detail/HoodSheet.swift:7` declares `HoodSheet`, and grep finds `HoodStubSheet` nowhere in `passenger-code`. Left standing, C13's and §9 row 7's sheet checks point `ios-developer` and `qa` at a type they cannot find | `architect` (v3 pass) | Renamed to `HoodSheet` at all three sites (§1, §9 row 7, §11 footer). Name only — no behaviour, no scope, no decision changes |

**Two things a re-reviewer should check rather than take on trust.** (1) The header, the four rows above, and the §2.4 / §4.8 / D7 / §9 edits were **already present in the shared working tree, uncommitted, when this `architect` pass opened the file** — several sessions share this tree (`CLAUDE.md` rule 2). They are not this pass's writing. Each was re-read against `27faac4` and `7a1f99c` and against source before being allowed to stand, and the gaps found are what this pass actually wrote: §4.10's detent note, C13's verify-list (which the changelog above promised and the body had not received), §10's new risk row, §2.4's forward pointer, and finding 5. (2) D6's **founder-direct icon-only paragraph** ("remove the name from the icons in the nav bar, show only icons") is `chief-of-staff`'s work, not this pass's — it was uncommitted in the tree while this revision was being written and that session has since committed it separately (`passenger-brain 5220c1f`). It is not part of the v3 review scope and no v3 edit touches it.

**What changed at v2.** v1 (2026-07-30/31) designed one entry path: a heat button opening a modal card around a horizontal `Slider`. The PRD has since added a second, structurally different path — a vertical drag on either live screen edge (req 7) — and Aviran has ratified its three open questions. v2 keeps every v1 decision that survives (D1–D6 stand), adds the edge-gesture architecture (§2.4, §4.8–§4.10, D7–D9), settles the two items the design spec explicitly handed to `architect` (gesture construction, inset geometry), and adds two things v1 could not have: a **Build Phase 1 data seed** without which nothing in this feature is observable (§3.4, D10) and a **§9 verification table with one row per P0 requirement** (`architect.md`, L-018).

---

## 1. Context

Read the PRD first. Nothing here restates it. This document decides what it leaves open and pins the contracts `ios-developer` builds against.

**Surface: iOS-only. Confirmed, not assumed.** Re-checked at v2 against the PRD's Technical design and the shipped code: no new table, no new column, no new endpoint, no change to an existing one. `DensityAPI.fetchDensity(from:)` already fetches the whole `[anchorHour, anchorHour + 12h]` window in one request (`hour_bucket=gte./lte.`), and `hood_density` already keys on an absolute UTC timestamp. Everything this feature needs from the backend is in the shipped contract. **§11 contains no `[Backend]` and no `[Algo/Data]` step.** `trd-review` routes to **`ios-developer` + `ios-code-reviewer` only** (§11).

**What this feature is, architecturally.** Two things, not one:

1. **The app's first chrome above the map** — the persistent nav row, the modal layer hanging off it, and the layering rule deciding what covers what. That layering, not the slider, is what has consequences: T-034/T-036/T-037/T-038 all land in the same bottom band.
2. **The app's first custom gesture surface** — a hit-testable overlay claiming a permanent strip of the map. This is the part that can regress already-shipped behaviour (`HoodSheet`'s drag-to-dismiss, MapKit pan, T-031's tap-to-open-Hood), so it gets the most explicit construction rules in this document.

**Open items resolved here:**

| # | Open item | Source | Call | Where |
|---|---|---|---|---|
| 1 | Heat modal construction — not a `.sheet()` | design §8.1 | `ZStack` overlay in `MapScreen`, below the nav row's layer | §2.3, D2 |
| 2 | `selectedHour` write-path | design §8.2 | Settled by T-031 — plain `var selectedHour: Int` on `@Observable DensityStore`. Confirmed against the shipped file; **not redesigned** | §4.3 |
| 3 | "Now" re-resolving while foregrounded across an hour boundary | PRD Open technical questions (a); design §8.3 | Re-anchor on modal **open** and on **edge touch-down**, on top of T-031's existing `scenePhase → .active` hook. No timer | §4.5, D3 |
| 4 | Day-boundary bucket keying | PRD risks; design §8.4 | **Already resolved by T-031** — `hour_bucket` is an absolute UTC timestamp and `DensityStore` keys on epoch-hour. Closed. The "next day" pill is display-only on top of it | §3.2 |
| 5 | Native `Slider` vs. custom control (button path) | design §8.5 | **Native `Slider(value:in:step:)`.** The tick overlay is decorative and non-interactive | §4.4, D5 |
| 6 | **Edge gesture recognizer construction** | design §8.6; PRD Open technical questions (b) | **SwiftUI `DragGesture` on a dedicated hit-testable overlay above `Map`** — not a `UIGestureRecognizer`, and not a gesture-arbitration problem at all | §4.8, **D7** |
| 7 | **Confirming the 64pt/40pt insets against real device geometry** | design §8.7; PRD Open technical questions (b) | Numbers **confirmed correct** for the reference device and re-derived as `max(designFloor, safeAreaInset + clearance)` so they hold on every device instead of only that one | §4.9, **D8** |
| 8 | Which nav-row buttons exist in this build | found by reading the shipped code | The nav row does not exist yet. T-032 builds the container plus **the heat button only**, glyph `flame.fill` | §2.3, D1/D6 |
| 9 | Landscape and per-idiom edge availability | not raised by any doc — found at v2 | **Edge path is portrait-only on iPhone**; iPad left edge only; right edge never on iPad. One pure function decides | §4.10, **D9** |
| 10 | Nothing in this feature is observable in Build Phase 1 | not raised by any doc — found at v2 by reading `DensityStore` | A **bundled relative density seed** ships in this task, behind the existing `BuildPhase.seedIsAuthoritative` constant | §3.4, **D10** |

---

## 2. Architecture

### 2.1 Module layout — additions to T-031's tree

```
Passenger/
  Map/
    MapScreen.swift            MODIFIED — hosts the chrome ZStack; near-me moves (D1)
    MapChromeState.swift       new — NavSurface + the one-surface-at-a-time rule
    MapNavRow.swift            new — separate side-by-side buttons; heat button only (D1/D6)
  HeatModal/
    HeatModalCard.swift        new — the overlay card: scrim, transitions, dismissals
    HourSlider.swift           new — native Slider + decorative tick overlay + a11y
    HourReadout.swift          new — numeral + "next day" pill
    HourFormat.swift           new — pure offset → (numeral, clock time, isNextDay)
  EdgeHour/
    EdgeHourZone.swift         new — the 24pt capture overlay + DragGesture (§4.8)
    EdgeHourTrack.swift        new — active track + floating readout chip
    EdgeHint.swift             new — the 5pt × 56pt idle capsule (Q8)
    EdgeGeometry.swift         new — pure: insets, usable band, y → hour (§4.9)
    EdgeAvailability.swift     new — pure: which edges are live (§4.10)
  Density/
    DensityStore.swift         MODIFIED — seed path (§3.4) + one guard (§4.5)
    DensitySeed.swift          new — bundled relative seed → rows (§3.4)
  Map/
    HeatComposition.swift      new — pure hoods × hour → [HoodFill] (§4.7)
  Support/
    HeatRepaintSignpost.swift  new — the HourRepaint interval (§4.7)
Resources/
  density-seed-tel-aviv.json   new — Build Phase 1 fake data (§3.4)
Assets.xcassets/
  MutedOnSurface · PillSurface · SliderFill · NowTick · EdgeRail   new colour sets
```

Xcode synchronized file groups are on — dropping files in the folder is enough, no `project.pbxproj` edit.

### 2.2 Boundaries — who is allowed to know what

- **`HeatModal/` knows no map, no geometry, no network.** It reads and writes one `Int` and formats a date. `HourFormat` is pure and takes its calendar and its clock as parameters, so every label string is unit-testable with no simulator and no fixed timezone.
- **`EdgeHour/` knows no map and no density.** It converts a touch position into an `Int` and writes it. `EdgeGeometry` and `EdgeAvailability` are pure functions over `CGSize`/`EdgeInsets`/`UIUserInterfaceIdiom` — the two hardest things in this feature to get right are therefore the two easiest to unit-test, with no simulator and no gesture.
- **`MapChromeState` knows no view.** It holds which nav surface is presented and nothing else. It does not own `selectedHour` — that is the whole point of PRD req 4.
- **`Density/` still knows no geometry.** `HeatComposition` pairs a Hood with a band and lives on the composition seam T-031 already put in `Map/`; it takes a lookup closure, never a `DensityStore`.
- **`Map/` remains the only layer that knows both**, and the only layer that knows the z-order.

### 2.3 The chrome layering rule

`MapScreen`'s body becomes an explicit `ZStack`, top of list = furthest back:

| z | Layer | Behaviour when a nav surface is presented |
|---|---|---|
| 0 | `Map` + `HoodLayer` + `PlaceLayer` + `UserAnnotation`, `ColdOpenTitle`, `CachedDataIndicator` | Unchanged. |
| 1 | **`EdgeHint`** (per live edge) | Hidden — see §4.10's availability rule. Non-hit-testing at all times. |
| 2 | **`EdgeHourZone`** (per live edge, 24pt) | **Not in the hierarchy at all** while a surface or a sheet is presented (D7 rule c). |
| 3 | **Scrim** — `Color.black.opacity(…)`, `.contentShape(Rectangle())`, tap → dismiss | Present only while a nav surface is presented. Makes tap-outside work; stops a map tap opening a Hood sheet under an open modal. |
| 4 | **Bucket-2 chrome** — `NearMeButton`, `HoodButton`, `SettingsHint` | `.opacity(0)` + `.allowsHitTesting(false)` while presented (`ux-flows.md` §2.1 bucket 2). Reduce Motion honoured. |
| 5 | **Modal card** — `HeatModalCard` | Anchored a fixed distance above the nav row, sized to content — never `bottom: 0`. |
| 6 | **`EdgeHourTrack`** | Only during an active edge drag, which can only happen when nothing else is presented. Mutually exclusive with z5 by construction. |
| 7 | **`MapNavRow`** | Always visible, always hit-testable, never covered — this is what makes direct nav-switching work with no dismiss-first step. |

Two consequences worth stating rather than discovering:

- **`.presentationBackgroundInteraction` is not involved and must not be reached for.** That is T-033's mechanism for system sheets. This is a custom overlay in the app's own hierarchy; the scrim at z3 is the equivalent, and the map is deliberately *not* interactive while the modal is open.
- ~~**The heat modal and a system `.sheet` are never co-presented** (D4). A `.sheet` presents above the entire hierarchy including z7; while the modal is up, the scrim blocks the map taps that would open a sheet. Mutually exclusive in both directions.~~ **Rewritten at v7 (T-090/`PAS-88`) — the claim above is now vacuously true and therefore argues nothing.** There is no modal (T-081/`PAS-76`), and there is no system `.sheet` either (T-079/`PAS-73` moved every detail surface to in-hierarchy overlays; grep at `passenger-code c6398f9` finds zero live `.presentationDetents`/`.presentationBackgroundInteraction`). **Two corrections, then the live rule.** *(1) The citation was wrong as well as spent:* co-presentation was **D4 in TRD `2f955fe`**; today's D4 is a different decision entirely, so "(D4)" here pointed at the wrong row — same defect `product` corrected on the PRD's Technical-design bullet the same day. *(2) The guarantee it was carrying is req 2's "any open sheet is unchanged by an hour change," and that guarantee still holds — for a different and stronger reason:*

  > **While any detail surface is presented, `EdgeHourZone` is not in the view hierarchy, so no hour can be set at all.** `EdgeAvailability.liveEdges(…)` returns `[]` when `isAnySheetPresented` is `true` (`EdgeAvailability.swift:16`), and `MapScreen.edgeLayer(for:)` only constructs the zone inside `if liveEdges.contains(edge)` (`MapScreen.swift:1198-1211`). The flag is `detailRouter.isDepth1Presented` (`MapScreen.swift:1187`), which is `hood != nil || place != nil || event != nil` — so it covers all three depth-1 destinations **and** depth-2, since a depth-2 place requires a hood. This is D7 rule c, and it is what §2.4 already called "genuine non-engagement, not deferred no-op."

  **Why this is stronger, not merely different.** The old argument was about two surfaces never being *up at the same time* — a claim that stops holding the moment either surface changes. The live one is about the writer being *absent from the hierarchy* whenever the reader is present, which is a property of one pure function with a full unit-test matrix (§9 row 7a). **The cost is stated, not hidden, and it is now a `product`-owned hole:** with the modal deleted, "the hour cannot change while a sheet is up" also means the hour cannot change *by any means* in that state. `product` has routed exactly that to Aviran as **PRD Q9(b)**; this TRD records the mechanism, not the verdict.

**`MapNavRow` is a layout container, not a visual one** (D6, founder-direct). The icons render as separate, independent buttons side by side, each its own tap target with its own background — no shared capsule, bar, divider, or segmented control. The heat button's glyph is **`Image(systemName: "flame.fill")`**, pinned by `designer` 2026-08-02 (design spec §2, §8 item 8) and adopted here as the build target, closing D6's own flagged gap.

**The near-me cluster moves.** T-031 anchors `NearMeButton`/`HoodButton`/`SettingsHint` at `.bottom` with 32pt padding — the band the nav row now occupies. They move above the nav row. This is a change to accepted, shipped T-031 layout, named here rather than left as an implementation surprise (D1).

### 2.4 The edge surface, and why it is not a gesture-arbitration problem

The design spec (§2, §7, §8 item 6) frames the 24pt capture zone as needing to be "wide enough to reliably win gesture-initiation against MapKit's own pan recognizer," citing T-031's FB19394663 workaround as precedent. **That framing does not apply to this construction, and the difference matters enough to state.**

FB19394663 is about a gesture attached *to the `Map` view itself* — `MapScreen.swift:113-122` uses `.simultaneousGesture(SpatialTapGesture())` precisely because a gesture in `Map`'s own subtree has to coexist with MapKit's internal recognizers. The edge zone is not in that subtree. It is a **sibling view drawn above the map**, and UIKit hit-testing runs front-to-back before any recognizer arbitration happens: a touch inside the zone resolves to the zone's view, so MapKit's pan recognizer is never in that touch's recognizer chain and never competes. On that reasoning there is nothing to win — **and the next paragraph is why this TRD treats that as a prediction to confirm rather than a fact to build on.**

Three things follow, all load-bearing:

- **The 24pt number is not doing the job the design spec assigns it.** Its arbitration justification is void; its *acquisition* justification (§7 there — an edge-anchored target cannot be overshot past the bezel; the ~708pt gesture axis gives large correction margin; req 6 keeps a fully conforming fallback) stands untouched, and that is the argument Aviran ratified at Q7. **The number is unchanged at 24pt and Q7 is not reopened** — only its stated mechanism is corrected.
- **The zone is a genuine dead strip.** 24pt at each live edge cannot be panned, pinched, or tapped through. On a 393pt-wide iPhone that is 48pt, ~12% of the width, permanently unavailable to the map. The design spec priced this ("narrow enough to minimize the permanently-unpannable map band"); §10 names it as the accepted cost it is, and §9 gives `qa` a check for it.
- **Requirement (c) from design §8 item 6 — never claim a touch while a sheet is presented — is satisfied structurally, not by a flag.** The zone is *removed from the view hierarchy* in that state (z2 above), so there is no recognizer to claim anything. This is exactly the "genuine non-engagement, not deferred no-op" the design spec required, and it is the strongest available form of it.

**The paragraph above is a prediction, and this TRD requires it confirmed before C13 is done — it is not a settled fact [added at v3, `ios-code-reviewer`].** Everything in this section rests on one claim: that MapKit's pan recognizer is never in the recognizer chain of a touch that lands in the zone. That claim is derived from documented UIKit hit-test ordering, and it is the strongest reasoning available — but this document cites `FB19394663` two paragraphs up precisely because SwiftUI's `Map` has already been observed not to behave the way plain recognizer-chain reasoning predicts. Reasoning of the same kind therefore cannot be the last word on the most load-bearing claim in the feature, when §4.8 already applies "confirm it, do not assume it" to a narrower one.

**What that means concretely.** If the prediction is wrong — if MapKit's pan recognizer does receive the touch simultaneously under the sibling overlay — the map jumps or drifts under the finger during *every ordinary edge slide*, a visible regression against T-031's shipped camera behaviour on this feature's primary gesture. Nothing in the v2 verification set would have caught it: an inert horizontal drag and a pan starting outside the band are both cases where the camera is *expected* to be untouched or expected to move, so both pass either way. **§9 row 7(e) and C13 now check the in-band vertical case directly, on device or in a UI test.** If that check fails, D7's construction is what changes (the remaining option is a `UIViewRepresentable` recognizer that arbitrates against nothing, since `Map` exposes no recognizer to defer to — meaning the real fallback is a product conversation about the edge path, not a quiet code fix), and it should fail at C13 rather than at `qa` or after ship.

---

## 3. Data model

### 3.1 No new persisted state, on either side

The control owns nothing. `selectedHour` is a plain `Int` on `DensityStore`, in memory, session-scoped, **never written to `UserDefaults`/`AppStorage`/disk**. PRD req 3's cold-launch reset is therefore a property of where the value lives, not of a reset routine someone could forget to call (§4.6). `DensityCache` persists density rows only; it has never held an hour selection and must not gain one. `MapChromeState` is likewise in-memory.

No migration, no schema change, no new query parameter. Nothing here carries a location, a device id, or a user id — the request surface is untouched, so T-031's "location cannot leak through a query that never had a place to put it" holds unchanged. The edge gesture reads a touch's `y` inside a view's own bounds and converts it to an integer; **no touch coordinate is stored, logged, or sent anywhere.**

### 3.2 Time — how an offset becomes a label

`anchorHour` (UTC hour floor, T-031) + `offset × 3600s` = the selected absolute instant. Everything the user reads derives from that instant in the **current** calendar and timezone:

- numeral: `"Now"` for offset 0, `"+\(offset)h"` otherwise — offset is the primary channel, never a bare clock time
- clock time (`"21:00"`, PRD P1): `Date.FormatStyle` in `.current` timezone
- `isNextDay`: `!Calendar.current.isDate(selectedInstant, inSameDayAs: now)`, compared against the real clock, not against `anchorHour`

**[ASSUMPTION]** every supported timezone is a whole-hour offset from UTC, so a UTC hour floor lands on a local hour boundary and "+3h" reads as a clean o'clock. True for Tel Aviv (UTC+2/+3) and for V1's only city; false in e.g. India (+5:30). The failure mode is cosmetic — the P1 clock label would read `20:30` — and it never affects bucket lookup, which stays in epoch-hour arithmetic. Recorded in §10 rather than engineered around for a city V1 does not ship in.

### 3.3 Edge geometry is derived, never stored

`EdgeGeometry` computes from the live `GeometryProxy` on every layout pass. Nothing about the band, the stop spacing, or the last touch position persists between drags. A drag is stateless apart from one `@GestureState` for "is this drag live and vertical-dominant" (§4.8).

### 3.4 Build Phase 1 — the density seed **[new at v2, D10]**

**The finding.** `DensityStore.load()` (read directly, `Density/DensityStore.swift:56-72`) has exactly three outcomes: live fetch → `DensityCache` → `.unavailable`. There is **no seed path**. In Build Phase 1 there is no `SupabaseConfig.plist`, so `DensityAPI.fetchDensity` throws `.unconfigured`, the cache is empty on a fresh install, and `snapshot` is `.empty`. `band(for:hour:)` returns `nil` for every Hood at every hour, and `HoodLayer.fillColor` returns `.clear`. **Shipped as-is, T-032 would be a control that visibly does nothing at every one of its 13 positions**, and three of PRD req 2's four bullets would have no observable to check.

This is not a defect in T-031 — that task's own acceptance carried "heat never observed live" forward as a named gap, correctly, because T-031 could not change the hour. T-032 is the only task that can exercise the repaint, so the data it needs to be exercised against belongs here. `BOARD.md`'s own Build Phase 1 definition names this feature explicitly: *"Fake/hardcoded data baked into the app — just enough to demo interactions (saving places, the 12h time slider, browsing Hoods/places)."* T-034's PRD took the same call for the same reason (a bundled fake event set folded into its own build scope), and T-033 shipped the pattern.

**The shape.** Follow `PlaceCatalog` exactly — the same `BuildPhase.seedIsAuthoritative` constant, the same `Source` enum extension, the same injectable resource name and bundle:

```swift
// Resources/density-seed-tel-aviv.json — relative, not absolute
{ "hoods": [ { "hood_id": "florentin", "bands": [2,2,3,3,4,4,4,3,3,2,1,1,1] } ] }
```

`bands` is 13 entries, index = hour offset 0…12; a `null` entry means **no row for that hour**, which is how the seed exercises req 2's silent-empty bullet on purpose rather than by accident.

**Why relative and not the wire shape.** `DensityAPI.Row.hourBucket` is an absolute ISO timestamp. A bundled file of absolute timestamps is stale the moment it is authored and would make every Phase-1 launch a different demo. `DensitySeed.rows(anchorHour:)` synthesises `DensitySnapshot` input against the live `anchorHour` at load time, so the seed is correct at any launch on any date, and it flows through the same `DensitySnapshot` epoch-hour keying the live path uses — the seed exercises the real code, not a parallel one.

**Authoring rule, so the seed can actually falsify something:** at least three Hoods must change band between at least four adjacent hour pairs, and at least one Hood must have `null` for at least one hour. Without variation, C6's "differs across hours" test and `qa`'s perceptual repaint check both pass vacuously.

**Flagged for `product` at `trd-review`, not decided unilaterally:** this adds a bundled data artifact to a PRD whose Technical design says "nothing to source or author." It is a Build-Phase-1 sequencing consequence, not a scope change to the control — but `product` should confirm it rather than discover it, and confirm that Phase-2 acceptance re-tests the same requirements against the live feed with the constant flipped (§7).

---

## 4. Contracts

All of §4 is `[iOS]`. There is no second build surface to hand a contract to.

### 4.1 Nav-surface state

```swift
enum NavSurface: String, CaseIterable, Sendable, Identifiable {
    case search, heat, places, profile
    var id: String { rawValue }
}

@MainActor @Observable
final class MapChromeState {
    private(set) var presented: NavSurface?
    var isPresenting: Bool { presented != nil }

    /// Exclusivity (`ux-flows.md` §2.1): presenting a surface replaces whatever
    /// was open — it never stacks. Presenting the already-open surface closes it.
    func toggle(_ surface: NavSurface)
    func dismiss()
}
```

Four cases, one view. Deliberate, and the narrowest thing that makes PRD req 4 testable: "switching to a different nav modal and back does not reset the hour" cannot be exercised at this task's own `qa` if the type can only express one surface. The four-member set is not invented here — `ux-flows.md` §2.1 locks it. A case with no view costs nothing, ships nothing, and stops T-036/T-037/T-038 each inventing a private boolean and quietly breaking exclusivity. **This is a state type mirroring a locked spec, not a hook for an unbuilt feature** — `ios-code-reviewer` should read it as such and reject any *view* work for the other three cases in this task's diff.

`toggle` closing the already-open surface is an architect call filling a gap: the design lists three exits and does not say what a second tap on the lit heat button does. Doing nothing there reads as broken.

### 4.2 The modal card

```swift
struct HeatModalCard: View {
    let onDismiss: () -> Void
    // content: section header + HourReadout + HourSlider. Nothing else in V1 (D4).
}
```

- Background: opaque `Color("Surface")` (T-031's token), rounded, sized to content. **Not `.ultraThinMaterial`** — same reasoning as T-031 §8 D1: a contrast ratio against a translucent layer over a live map is not a number anyone can verify, and PRD req 6 demands a verifiable one.
- Dismissals: (a) drag handle + `DragGesture` past a distance/velocity threshold; (b) scrim tap; (c) `MapNavRow` tapping another surface. All three route to `MapChromeState`, none to a private `@State` bool.
- Transition `.move(edge: .bottom).combined(with: .opacity)`; under `\.accessibilityReduceMotion` it cross-fades with no movement.
- **Composes rows, not a bare slider.** T-034's live-events toggle lands as a second row. That is a layout fact, not a hook: no toggle, no placeholder, no "always on" stub row ships in this task (D4).

### 4.3 The one value — Q3, structurally

`selectedHour` stays `var selectedHour: Int` on `@Observable DensityStore`, verified against the shipped file. **There is exactly one storage location for the hour in the entire app.** Q3 ("one shared value across both edges and the heat button") is ratified, and this is what makes it a fact rather than a convention: there is no second property that could desync.

```swift
// In HourSlider — the Double bridge lives in the one file that owns the control:
Slider(
    value: Binding(get: { Double(selectedHour) }, set: { selectedHour = Int($0.rounded()) }),
    in: 0...12, step: 1
)
```

Range clamping and hour snapping are structural on this path — `in: 0...12, step: 1` makes an off-hour or out-of-range value unrepresentable. On the edge path the same invariant is held by `EdgeGeometry.hour(atY:in:)`'s own clamp (§4.9), which is the only other writer.

**`ios-code-reviewer` findings, both blocking:** (1) any second stored hour — an `@State var hour`, a mirror on `MapChromeState`, a per-edge value — anywhere in the diff; (2) a hand-rolled clamp or rounding pass outside those two sites, which means the invariant moved out of the type and into a routine someone can forget.

### 4.4 The slider view (button path)

```swift
struct HourSlider: View {
    @Binding var selectedHour: Int    // 0...12
    let readout: HourFormat.Readout
}
```

- `.frame(minHeight: 44)` on the control itself regardless of how slim the drawn track is (Fitts's Law). The visible thumb may render smaller.
- The tick/hairline overlay is drawn in a `GeometryReader` **with `.allowsHitTesting(false)`** — it must never intercept the drag, or both the native gesture and the VoiceOver adjustable action degrade.
- `.tint(Color("SliderFill"))`, `.accessibilityLabel("Map hour")`, `.accessibilityValue(HourFormat.voiceOverValue(readout))`, `.accessibilityIdentifier("hourSlider")`. The identifier is not cosmetic — §9 drives the control through `XCUIElement.adjust(toNormalizedSliderPosition:)`.
- VoiceOver's discrete stepping comes from `step: 1` on a real `Slider` and is not reimplemented.

```swift
enum HourFormat {
    struct Readout: Equatable, Sendable {
        let offsetLabel: String    // "Now", "+1h" … "+12h"
        let clockLabel: String     // "21:00" — P1 surface, always computed
        let isNextDay: Bool
    }
    static func readout(offset: Int, anchorHour: Date, now: Date, calendar: Calendar) -> Readout
    static func voiceOverValue(_ readout: Readout) -> String   // "+3 hours, 21:00, next day"
}
```

Pure, injectable clock and calendar. Its tests must include a midnight crossing and offsets 0 and 12.

### 4.5 Changes to T-031's store

Three, all named rather than slipped in. `ios-code-reviewer` should confirm T-031's existing `DensityStoreTests` still pass unmodified alongside the new cases.

1. **Seed path in `load()`** (§3.4). Mirrors `PlaceCatalog.load()`: when `BuildPhase.seedIsAuthoritative` is `true`, load `DensitySeed` and attempt no fetch; otherwise the existing live → cache → unavailable precedence, unchanged, with the seed as a final fallback below cache. `Source` gains a `.seed` case. Both branches stay compiled and type-checked, per `BuildPhase.swift`'s own stated reason for being a runtime constant and not `#if`.
2. **New call sites for `refreshIfHourRolled()`** — on heat-modal open *and* on edge touch-down, in addition to T-031's existing `scenePhase → .active` hook (D3). The method already early-returns when the hour has not rolled, so the common case costs one comparison.
3. **A mid-`await` guard in `refreshIfHourRolled()`.** The method reads `selectedHour` before an `await` and writes a remapped value after it (`DensityStore.swift:82-85`). If the user moves the slider or drags an edge during that await, the write clobbers their input. Capture `selectedHour` before the await and apply the remap **only if it is unchanged**; otherwise leave the user's value alone. This becomes reachable the moment call site 2 exists — a modal-open refresh now overlaps a user who is already dragging.

### 4.6 Cold-launch reset (req 3) — by absence, not by routine

**No reset-on-launch code is written, and none should be.** The guarantee is structural, in three parts:

- `DensityStore.selectedHour` is declared `var selectedHour: Int = 0` — a fresh instance is at "now" before anything runs.
- `MapScreen` holds it as `@State private var densityStore = DensityStore()`, constructed once per process. A cold launch is a new process, so it is a new store.
- `anchorHour` is set in `init` from the injected `now()` closure, so "now" re-resolves against the real clock at launch (req 3 bullet 2) with no cached value anywhere to be stale.

The existing cold-open pattern (`ColdOpenSignpost.begin()` in `PassengerApp.init()`, `endIfNeeded()` on `MapScreen`'s `.onAppear`) is a measurement hook and is deliberately *not* extended — hanging a reset off it would replace a structural guarantee with a call someone can delete. **`ios-code-reviewer` treats any `@AppStorage`/`UserDefaults`/file write of the selected hour as a blocking finding**, and §9's C8 asserts a fresh store starts at 0 with an injected clock.

**Warm launch is deliberately different and is not a bug:** resuming from background keeps the session's hour, and `scenePhase → .active` remaps it against the new wall clock (§4.5). Req 3 says *cold* launch. `qa` should test both and expect different answers.

### 4.7 Repaint composition and its measurement

```swift
struct HoodFill: Equatable, Sendable { let hood: Hood; let band: HeatBand? }

enum HeatComposition {
    /// Pure. Takes a lookup closure, not a store — testable with no DensityStore,
    /// no network, no simulator.
    static func fills(hoods: [Hood], hour: Int, band: (String, Int) -> HeatBand?) -> [HoodFill]
}
```

`MapScreen`'s body resolves fills **once per pass** through this function and iterates the result, instead of calling `densityStore.band(...)` inline per Hood as it does today (`MapScreen.swift:79`). Two load-bearing reasons: it gives the repaint a single nameable completion point, and it gives §9 a pure function to measure.

`HoodLayer` is the only hour-bound layer that exists (verified: `PlaceLayer` takes no band and no hour). "Every hour-bound layer" is therefore a set of one today; T-034 joins it by reading the same `selectedHour`.

```swift
enum HeatRepaintSignpost {   // mirrors Support/ColdOpenSignpost.swift exactly
    // interval name "HourRepaint", category "HeatRepaint"
    @MainActor static func begin()        // on a real change, from either writer
    @MainActor static func endIfPending() // immediately after HeatComposition.fills(...) returns
}
```

**Honest scope of the measurement**, stated the way T-031 stated its cold-open one: `HourRepaint` brackets *"`selectedHour` written → every Hood's band resolved for the new hour."* It excludes MapKit's own frame commit, which app code cannot observe. The <400ms budget is held structurally first — T-031's contract that **no code path fetches on an hour change**, now reinforced by the seed being in memory — and measured second. `qa` additionally confirms perceptually that dragging produces no lag, no spinner, and no intermediate state.

### 4.8 Edge gesture construction **[D7]**

```swift
struct EdgeHourZone: View {
    let edge: HorizontalEdge          // .leading / .trailing
    let band: ClosedRange<CGFloat>    // usable y range in this view's coordinates
    @Binding var selectedHour: Int
    @Binding var activeDrag: EdgeDragState?
}

struct EdgeDragState: Equatable {
    let edge: HorizontalEdge
    let y: CGFloat            // clamped to `band`, drives the track + chip position
    let hour: Int
}
```

**Construction: a SwiftUI `DragGesture(minimumDistance: 4)` on a `Color.clear.contentShape(Rectangle())` overlay of fixed 24pt width, aligned to the edge, at z2.** Not a `UIGestureRecognizer` subclass, not a `UIViewRepresentable`, not `.simultaneousGesture`, not `.highPriorityGesture`.

**Coordinate space: the default `.local`, deliberately — corrected at v3 [`ios-developer`].** v2 wrote `coordinateSpace: .named("map")`, which named a space **nothing declares** — no view in §2.1's layout attaches `.coordinateSpace(.named("map"))`, and grep finds no `.coordinateSpace` modifier anywhere in `passenger-code` today. Left as written, `ios-developer` would have had to invent an owner for it at build time, and the obvious candidate is `Map` itself — the one view §2.4 goes out of its way to keep the zone *out of*. The failure mode is silent, not a crash: `value.location.y` measured in one frame, compared against a `band` computed in another, giving a wrong-but-plausible hour. `.local` is correct and needs no declaration: `EdgeGeometry.band(in:safeArea:)` and `hour(atY:in:)` are both documented as operating in **this view's own coordinates** (§3.3, §4.9), which is exactly what `DragGesture`'s default gives, and each zone is sized by its own `GeometryReader` so the two edges never need a shared frame of reference. **If a future step genuinely needs a shared named space, it must name the declaring view in this TRD first** — a named space with no declared owner is not a contract.

Why this and not UIKit — the reasoning, since design §8 item 6 posed it as an open choice:

- **The UIKit option cannot do the thing it would be chosen for.** Its only real advantage would be arbitrating against MapKit's pan via `require(toFail:)` or a delegate. SwiftUI's `Map` exposes no `MKMapView` and no access to its recognizers, so that relationship cannot be established at all. What remains of the UIKit option is a representable wrapper around a recognizer that behaves like the SwiftUI one, with more code and a `@MainActor`/`Sendable` bridging surface Swift 6 strict concurrency will make us justify.
- **Hit-test order already gives us priority** (§2.4). The mechanism the UIKit route would exist to provide is provided for free by being a sibling above the map.
- **It keeps the whole feature in one concurrency domain.** Everything here is `@MainActor` SwiftUI; no bridge, no `nonisolated(unsafe)`, nothing to argue with the compiler about.

Three rules the construction must satisfy, each mapped to its mechanism:

| Rule (design §8 item 6) | Mechanism here |
|---|---|
| (a) Claim the touch before MapKit | Sibling overlay above `Map` in the `ZStack`; UIKit hit-testing resolves to it first. Nothing to arbitrate. **Predicted, not assumed — C13 and §9 row 7(e) confirm it on the in-band vertical drag (§2.4, v3).** |
| (b) Require a vertical-dominant initial displacement | On the first `onChanged` where `hypot(dx,dy) ≥ 4`, latch `isVerticalDominant = abs(dy) > abs(dx)` into `@GestureState` for the whole drag. If `false`, the drag is **inert for its lifetime** — no track, no hour write, no hint change. |
| (c) Never claim a touch while a sheet is presented | The zone is **not in the view hierarchy** in that state (§2.4, §4.10). Strictly stronger than an `isEnabled` flag or a `.gesture` no-op. |

**Honest limit of rule (b), stated rather than glossed:** a horizontal-dominant drag starting inside the band is consumed by the overlay, so the map does not pan under it. (b) guarantees *no false hour change*; it cannot hand the touch back, because SwiftUI has already routed it. Handing it back is not achievable in either construction without a reference to MapKit's recognizer, which does not exist. The residual cost is the dead strip §2.4 names and §10 accepts. `qa` should check that such a drag leaves the hour and the camera both unchanged — that is the checkable promise.

**Rule (a) is checked directly, on the drag that matters [v3, `ios-code-reviewer`].** The inert-horizontal case above and the pan-starting-outside case (§9 row 7c) both leave rule (a) untested: the first expects no camera movement whether or not MapKit saw the touch, the second is a touch the zone never claimed. The case that actually exercises (a) is a **vertical, in-band drag** — the normal gesture — where the hour is expected to change and the camera is expected not to. C13 and §9 row 7(e) require `camera`/`MKCoordinateRegion` to be byte-identical from touch-down through `onEnded`, sampled at least at the drag's start, mid-point and end, using the same comparison §9 row 2c already uses for the button path. Not a "the map looked still" observation — the same recorded-value comparison, on device or in a UI test.

**Also consumed: taps inside the strip.** `minimumDistance: 4` means a tap never becomes a drag, and the overlay swallows it, so a Hood or pin whose only visible part is inside the 24pt strip cannot be tapped there. `qa` verification: a drag in the band must not also fire `MapScreen.handleTap` and open a Hood sheet mid-drag (`SpatialTapGesture` via `.simultaneousGesture` is greedy; it is attached to `Map`'s own subtree, which the overlay is not part of, so this should hold by construction — confirm it, do not assume it).

On `onEnded`: clear `activeDrag`, leave `selectedHour` where it landed, restore the hint. **No commit gesture, per req 7.**

Haptics (P1): `.sensoryFeedback(.selection, trigger: selectedHour)` on the zone — one line, fires on every hour crossing from either path. Ship it if it costs nothing; drop it without a second thought if it complicates anything.

### 4.9 Edge geometry — the 64pt/40pt insets, confirmed **[D8]**

```swift
enum EdgeGeometry {
    static let captureWidth: CGFloat = 24     // Q7, ratified 2026-08-02
    static let topFloor: CGFloat = 64
    static let bottomFloor: CGFloat = 40
    static let hintSize = CGSize(width: 5, height: 56)

    static func band(in size: CGSize, safeArea: EdgeInsets) -> ClosedRange<CGFloat>
    static func hour(atY y: CGFloat, in band: ClosedRange<CGFloat>) -> Int   // clamped 0...12
    static func y(forHour hour: Int, in band: ClosedRange<CGFloat>) -> CGFloat
}
```

**The design's numbers are confirmed, and the construction is changed so they stay correct off the reference device.** Checked against real iOS geometry rather than accepted from the spec, which is what design §8 item 7 asked for:

- Top: the largest top safe-area inset on any current iPhone is **59pt** (Dynamic Island, iPhone 14 Pro family onward); notch devices are 47pt or 44pt. Notification Center and Control Center are pulled from within that same top region. `64 = 59 + 5pt` clearance — the design's number is exactly right for the worst current case, with a small margin.
- Bottom: the home-indicator safe-area inset is **34pt** on every Face ID iPhone. `40 = 34 + 6pt` clearance. Also right.

Because both numbers are the worst-case inset plus a clearance, hardcoding them is correct today and silently wrong on any future device with a larger inset. So `band(in:safeArea:)` computes:

```
top    = max(topFloor,    safeArea.top    + 5)
bottom = max(bottomFloor, safeArea.bottom + 6)
band   = top ... (size.height - bottom)
```

On an 812pt reference device this yields exactly the design's 708pt band and ~59pt per stop, so every arithmetic figure in the design spec and the mockup remains valid. On a device with a smaller inset (iPhone SE, 20pt top) the floors hold the band identical to the design. On a larger one it grows automatically.

`hour(atY:in:)` maps **absolute position, not delta** — this is what makes req 1's widened bullet ("all 13 reachable wherever the finger lands") true by construction rather than by tuning. Up is later: `hour = round((band.upperBound - y) / band.length × 12)`, clamped to `0...12`. One function, called by both edges against their own bounds, so req 7's "identical from both edges" is structural (design §7's own argument, adopted). The value clamp lives here; the track's drawn extent and the readout chip's position are clamped separately to the band so the chip stays pinned at the end rather than floating past it.

**Dynamic Type:** the band and stop spacing are pure geometry and do not reflow with type size, so req 1's "at the largest supported Dynamic Type size" is satisfied structurally on this path. Only the readout chip's text scales; its container is sized to content so it cannot clip. Req 1's Dynamic Type bullet on the *button* path was already verified in the design's own v1 pass.

**Smallest supported band, checked:** the shortest current iPhone in portrait is 667pt (SE). `667 - 64 - 40 = 563pt`, ~47pt per stop — still above the 44pt reference the design used. No device in portrait falls below it.

### 4.10 Which edges are live **[D9]**

```swift
enum EdgeAvailability {
    static func liveEdges(
        idiom: UIUserInterfaceIdiom,
        isPortrait: Bool,
        isAnySurfacePresented: Bool,
        isAnySheetPresented: Bool
    ) -> Set<HorizontalEdge>
}
```

Pure, exhaustively unit-testable, and the single place this policy lives — no view re-derives it.

| Condition | Live edges |
|---|---|
| iPhone, portrait, nothing presented | `[.leading, .trailing]` (Q2) |
| **iPhone, landscape** | `[]` — **new call at v2, D9** |
| iPad, nothing presented | `[.leading]` — right edge is system Slide Over, permanently excluded (Q2) |
| Any sheet presented (`detailRouter.isDepth1Presented`) | `[]` (Q6 — zone leaves the hierarchy, §2.4) |
| Any nav surface presented (`MapChromeState.isPresenting`) | `[]` |

**The sheet row is one flat rule, but the behaviour it falls back to is not one behaviour [added at v3, `ios-code-reviewer`].** Collapsing *any* presented sheet to `[]` is correct and is Q6's call — the zone leaves the hierarchy regardless of detent, and nothing here changes that. What is not single-valued is what the touch then does instead, and PRD req 7's "an edge drag over a presented sheet moves the sheet, as it does today" reads as one behaviour when the shipped code has two. Verified at source, not inferred:

- `MapScreen.swift:186` — `.presentationBackgroundInteraction(.enabled(upThrough: .medium))`. The still-exposed map above the sheet is interactive at `.medium` and **inert at `.large`**.
- `HoodSheet.swift:26` — `.presentationDetents([.medium, .large])`, so both states are reachable.
- `PlaceDetailModal.swift:22` — `.presentationDetents([.medium])` only, so `.large` is reachable through the Hood sheet alone.

So "as it does today" covers four combinations, not one: {`.medium`, `.large`} × {touch on sheet content, touch on the still-exposed map}. §9 row 7(d) and C13 exercise all four explicitly. **No code in this feature changes as a result** — this is verification granularity, not a design change, and `EdgeAvailability` keeps its one flat rule.

**Why landscape is excluded, since no upstream doc considered it.** The app supports all three orientations (`project.pbxproj:367`), and the design reasoned entirely about an 812pt-tall portrait reference device. In landscape:

- The sensor housing sits on a *long* screen edge. On a Dynamic Island iPhone in landscape the horizontal safe-area inset on that side is 59pt — the physical edge where the capture zone would live is under the housing, unreachable and partly invisible. The "an edge-anchored target cannot be overshot past the bezel" argument that Aviran ratified at Q7 does not survive there.
- The usable band drops to roughly 289pt (393 − 64 − 40), about 24pt per stop — below every figure the design and this TRD reason from.
- Nothing is lost: req 6's own bullet already guarantees all 13 hours from the heat button, which works identically in any orientation.

Hiding the hint (rather than drawing the iPad ghost mark) is right here because the *whole gesture* is off in landscape, not one edge of two — a ghost mark on both edges would explain an absence the user has no reason to expect. **Cheap for `designer` or `product` to overturn**: it is one row in one pure function, and `qa` can check it in a rotation.

### 4.11 The idle hint and the active track **[Q8]**

```swift
struct EdgeHint: View { let edge: HorizontalEdge; let band: ClosedRange<CGFloat> }
struct EdgeHourTrack: View { let state: EdgeDragState; let band: ClosedRange<CGFloat>; let readout: HourFormat.Readout }
```

Q8 is ratified: the hint is deliberately persistent chrome, an explicit exception to the PRD's "not permanent chrome" line. Build it as specced and do not treat the tension as unresolved.

- **`EdgeHint`** — 5pt × 56pt capsule, vertically centred in the band, **opacity 1.0**, opaque `Color("Surface")` with a 1pt inner mark in `Color("MutedOnSurface")`. Opaque, never translucent over a live map, for the same reason T-031 §8 D1 gave: a ratio against unknown map pixels is not a number anyone can verify. Rendered once per live edge; hidden while a drag is active (the track replaces it), and absent whenever `liveEdges` excludes that edge. `.allowsHitTesting(false)` — the 24pt zone owns every touch; the 5pt hint is purely visual. Fade honours Reduce Motion.
- **iPad right edge** draws a faint neutral ghost mark instead of a hint, so the absence reads as "OS-reserved" rather than as a missed build (design §3).
- **`EdgeHourTrack`** — custom-drawn vertical control: 13 stops, a "now" tick at the range end that means now, and the floating readout chip beside the finger. It draws its **own opaque `Surface`-backed panel**, so every contrast figure is priced against a background this app actually draws.
- **Both are `.accessibilityHidden(true)`.** The edge path is a supplementary raw-pixel gesture; narrating it would be worse than not exposing it, and req 6's assistive-tech bullet is satisfied entirely by the button path (design §4). This is a deliberate exception to the app's semantic-first default and is stated here so `ios-code-reviewer` does not read it as an omission.

### 4.12 Colour tokens and the contrast rule

PRD req 6 says "**every** text label rendered on the surface housing this control… There is no enumeration exception." A test cannot enumerate labels that do not exist yet, so the invariant moves into the construction:

> **Every text label inside `HeatModal/` and `EdgeHour/` renders with exactly one foreground token, `MutedOnSurface`, on exactly one of two backgrounds: `Surface` or `PillSurface`.** Hierarchy comes from type size and weight, never from a second colour.

That turns an unenumerable claim into four executable assertions ({token} × {2 backgrounds} × {light, dark} ≥ 4.5:1), covering any future label on these surfaces the day it is written. `ios-code-reviewer` treats a second foreground colour in either folder as a blocking finding.

- **`PillSurface` is an opaque colour set**, not the mockup's `color-mix(--heat 14%, transparent)` — the pre-flattened equivalent of the design's own ~5.09:1 light / ~6.01:1 dark figures.
- **Non-text (3:1), asserted:** `NowTick` vs `Surface`, `SliderFill` vs `Surface`, and — new at v2 — **`EdgeRail` vs `Surface`**. The edge track is custom-drawn, so req 6's inactive-rail exemption does not transfer to it (PRD Q5's consequence, design §4). `EdgeRail` exists as its own token precisely so the exempted native rail and the non-exempt custom rail cannot accidentally be the same colour — which is the exact defect the design's own fix pass found (`--surface-3` on both, 1.29:1).
- **Explicitly not asserted:** the native `Slider`'s thumb and inactive rail. The PRD exempts the rail; the thumb is the same category — an unmodified platform-drawn part, where WCAG 1.4.11's author-modification boundary falls. Going custom to control those pixels would cost the discrete VoiceOver adjustable action req 6 depends on (D5). **The test must not be "helpfully" extended to those two pairs** — it would fail against the control the PRD requires.
- `SliderFill` is deliberately **not** `HeatFill`: reusing the heat hue would couple the slider's contrast tuning to the heat palette T-031 req 4 locks.

Test lives beside T-031's, reusing `Support/ContrastRatio.swift` and the same resolve-against-the-real-catalog pattern (`UIColor(named:in:compatibleWith:)` under both `UIUserInterfaceStyle`s) — never hardcoded hex.

---

## 5. Flow

```
Path A — heat button
  tap → MapChromeState.toggle(.heat)
      → refreshIfHourRolled()          re-anchor if the wall clock rolled (§4.5)
      → edge zones + hints leave the hierarchy (§4.10)
      → scrim in; bucket-2 chrome out; nav row stays lit and hit-testable
      → HeatModalCard slides in above the nav row, at this session's hour

Path B — edge slide (portrait iPhone / iPad left; nothing presented)
  touch down inside the 24pt zone
      → refreshIfHourRolled()          same re-anchor (§4.5)
      → first movement ≥4pt latches vertical-dominance; horizontal → inert drag, no write
      → hint hides, EdgeHourTrack + readout chip appear
      → every move: EdgeGeometry.hour(atY:) → selectedHour           ── absolute, clamped
  lift → track and chip disappear; hour holds for the session. No commit gesture.

Both paths converge on the one write:
  selectedHour set
      → HeatRepaintSignpost.begin()
      → @Observable invalidation → MapScreen body
          → HeatComposition.fills(hoods:hour:band:) → HeatRepaintSignpost.endIfPending()
          → HoodLayer re-evaluates foregroundStyle per polygon
      → the readout (numeral + "next day" pill) updates from the same value
  camera, zoom, geometry, polygon identity: untouched. No fetch. No sheet involved
  (v1's D4 — renumbered since; the live reason is §2.3's, EdgeAvailability.liveEdges
   returns [] while any detail surface is presented, so there is no writer to run).

Exit (path A): swipe down · scrim tap · another nav button
      → MapChromeState mutates; selectedHour untouched (PRD req 4)
```

Cold launch: `DensityStore()` initialises `selectedHour = 0` and `anchorHour` from the real clock. Nothing is read from disk, so "now" cannot be stale (req 3, §4.6).

Empty / offline hours are a non-event: `band(for:hour:)` returns `nil`, `HoodLayer` applies no fill, and no banner or modal appears. That is T-031's rendering rule, inherited, not re-implemented.

---

## 6. Third-party / dependencies

**None added.** No package, no account, no cost, nothing Aviran-gated. `Slider`, `DragGesture`, `GeometryReader`, `os_signpost`, `Calendar` and `.sensoryFeedback` are all platform. `passenger-code/README.md`'s "no third-party packages until a TRD justifies one" stays intact.

**Salvage:** `SALVAGE.md` marks `Models/HeatTimeWindow.swift` REUSE and `Features/Map/HeatmapControlsSheet.swift` REFERENCE. The archive is **not reachable from this workspace** (`~/APE Studio/locali` is absent — the same access gap T-031 hit). It is also largely moot: the hour-windowing model REUSE points at is already re-derived and shipped in `DensityStore` (`anchorHour` + `0...12` offset over absolute UTC hours), a stricter design than an hour-of-day window. `ios-developer` should not block on salvage access.

---

## 7. Rollout & migration

- **No feature flag.** The button is reachable only from chrome this same task adds; the off-state of a flag would be a nav row with nothing in it. The edge path's own kill switch already exists and is better than a flag: one row in `EdgeAvailability.liveEdges`.
- **No migration, no backend deploy, no Aviran-gated apply step.** Nothing in §11 touches `database/`.
- **No backward compatibility surface.** No persisted state exists to read forward or backward, by design (§3.1).
- **Build Phase 1 → Phase 2 is one constant.** Flipping `BuildPhase.seedIsAuthoritative` to `false` is the entire wiring change (§3.4), exactly as `BuildPhase.swift`'s own comment describes for `PlaceCatalog`. Both branches stay compiled and reviewable through Phase 1. **Phase 2 must re-run req 2's three data-dependent bullets against the live feed** — Phase-1 acceptance covers them against the seed only, and this TRD does not claim otherwise.
- **Ships independently of the backend.** With no `SupabaseConfig.plist`, the modal opens, both paths move the hour, and the map repaints against the seed. Demoable and testable before migration `001` is ever applied.
- **Dependency direction:** T-034 reads `selectedHour` and adds a row to `HeatModalCard`. T-036/T-037/T-038 add their own `NavSurface` views and their own buttons to `MapNavRow`. None of them need to change anything this task writes.

---

## 8. Decisions and ratified deviations

T-031 set the precedent: a deviation from an approved artifact is recorded and justified here, not silently built. D1–D6 are v1's and stand unchanged; D7–D10 are new at v2.

### D1 — The nav row ships with one button, not three
`ux-flows.md` §2 and the mockup show three or four nav buttons. **None exist in the shipped app**, and neither search (T-038) nor Profile (T-037) nor Places (T-036) has a TRD. This task builds `MapNavRow` as the container plus **the heat button only**. A rendered button that opens nothing fails at the Functional tier before it can be judged on anything else (`design-principles.md` §1), and a dead control in shipped chrome invites exactly the "is the app broken?" read this map cannot afford. The row is laid out so **Search and Profile** slot in without re-layout — **Places is bucket-2 chrome, separate from the nav row, per T-036's D7** (`ux-flows.md` §2/§2.1, confirmed word-for-word by two independent `trd-review` reads); this line previously named "the rest" ambiguously and was corrected 2026-08-02 once T-036's TRD made the distinction concrete. **Consequence:** the near-me cluster moves up out of the nav row's band (§2.3).

### D2 — Custom `ZStack` overlay, not `.sheet()`
Settled shape: a SwiftUI layer inside `MapScreen`'s `ZStack` at z5, below `MapNavRow` at z7, with an explicit scrim at z3. Not `.sheet`, not `.fullScreenCover`, not a `UIViewControllerRepresentable`, and not `.presentationBackgroundInteraction` (there is no presentation). The nav row must stay hit-testable or `ux-flows.md` §2.1's direct nav-switch requirement fails; that is the entire reason for the deviation.

### D3 — "Now" re-resolves on invocation, not on a timer
Re-anchor on modal open **and on edge touch-down**, reusing T-031's `refreshIfHourRolled()`, with no repeating timer. Staleness only becomes visible when the user reaches for the control, and there are now exactly two ways to reach it — a check at each is both sufficient and free. A wall-clock timer would burn a scheduled wake to correct a label nobody is reading and could move the thumb under a live finger. With T-031's `scenePhase → .active` hook, the three triggers cover every path by which a user can observe the value.

### D4 — The shipped modal contains the slider only ~~— MOOT at v7 (2026-08-08)~~
The mockup renders stub toggle rows and a repaint-timing pill; the design spec labels them mockup instrumentation. **None ship.** The heat layer has no on/off toggle in V1, so a row saying so explains an absent feature; the live-events toggle is T-034's; the timing pill becomes the `HourRepaint` signpost (§4.7), which has no UI.

**MOOT at v7 — the modal itself does not ship** (T-081/`PAS-76`). The decision is kept rather than deleted because two of its three clauses outlived their subject and are still live facts: the heat layer still has no on/off toggle in V1, and the timing pill is still the `HourRepaint` signpost with no UI (§4.7, and §9 row 2b's re-target depends on it). Only the container is gone.

**And a numbering hazard this decision carries, recorded here so it stops propagating.** In **TRD `2f955fe`**, D4 was a *different* decision — *"the heat modal and a system `.sheet` are never co-presented"* — which is what PRD req 2's sheet bullet leaned on. That decision was renumbered out of existence in a later revision while three documents kept citing "D4" for it. **Anything citing D4 for co-presentation is citing the old numbering, not this row.** Fixed in this file at v7 (§2.3, §10, §5's flow note); fixed in `time-slider.md`'s Technical-design bullet by `product` the same day. **Still stale at the time of writing, in other agents' lanes, flagged not fixed:** `design/phase-1/time-slider-design.md` §5b (`designer`), and `prds/live-events-overlay/TRD.md:332` + `TEST-PLAN.md:31`, which reason from "T-032's D4 ships the modal with the slider only" and from a `HeatModalCard` that no longer exists (that TRD's own `architect`/`qa` pass, not this task's — amending another feature's TRD from inside this one is exactly the ownership grab v6 refused).

### D5 — ~~Native `Slider` on the button path,~~ custom control on the edge path **[amended at v7 — half moot, surviving half now unconditional]**
~~Native `Slider(step:)` plus a non-interactive overlay for the modal;~~ a fully custom vertical control for the edge (no native vertical `Slider` exists). ~~The consequence is §4.12's: the native thumb and inactive rail are platform-drawn and outside this app's authored contrast surface, while the custom edge rail is inside it and gets its own `EdgeRail` token. Going custom on the button path too would trade a P0 (discrete VoiceOver stepping) for a bar the PRD already exempts the native rail from.~~

**Amended at v7 (T-090/`PAS-88`).** `HourSlider.swift` is deleted (T-081/`PAS-76`); **no native `Slider` ships anywhere in this feature.** What survives is one sentence: *the edge control is fully custom-drawn.* Three consequences, and the third is the one that had to be written down or the two documents would have drifted apart:

1. **`EdgeRail` is inside this app's authored contrast surface unconditionally**, not "unlike the native rail." The token, and `NowTick` and `MutedOnSurface` beside it, are held to the full bar with no carve-out and no comparison class. `EdgeRail` was created precisely so an exempt native rail and a non-exempt custom rail could never be the same colour — **that hazard no longer exists**, and the token is now simply the colour of the only rail there is.
2. **§4.12's "explicitly not asserted" carve-out is spent.** It excluded the native `Slider`'s thumb and inactive rail from the contrast test and warned that extending the test to them "would fail against the control the PRD requires." There is no such control. The warning is now harmless but meaningless; the shipped test never asserted those pairs, so nothing in code changes.
3. **PRD req 6's inactive-rail 3:1 exemption is retired, and this decision is why.** D5 is what created the exemption — it existed only "while the control is a platform-drawn one rendering it low-contrast by default." `product` retired it on the PRD side on 2026-08-08 (`time-slider.md` req 6, and Q5's consequence note); **it is retired here in the same breath, so the two files cannot disagree about whether a future re-draw is allowed a low-contrast rail.** It is not allowed. Note what this does *not* do: it removes a trap for a future author, not an allowance anything shipped was using — the edge track has been held to the full bar since design v4.

**What this decision cost, stated because D5's own rejected alternative is now the shipped reality.** The rejection line read: *"going custom on the button path too would trade a P0 (discrete VoiceOver stepping) for a bar the PRD already exempts the native rail from."* Deleting the button path made that trade anyway, without anyone choosing it — the native `Slider` was the app's only VoiceOver-adjustable hour control, and nothing replaced it. **That is §9 row 6(a), open and bounced to `product`, and PRD Q9(a).** It is recorded here rather than only in §9 because a reader who takes D5 at face value would still believe a conforming path exists.

### D6 — Separate side-by-side icons, glyph `flame.fill`, icon-only (no text caption)
Each nav icon is its own independent button, side by side, no shared container chrome. Provenance: Aviran, verbatim *"yes, separate icons, same switching behavior,"* relayed via `chief-of-staff` (`PROGRESS.md`, 2026-07-31), reconfirming his earlier *"I don't want a nav row. I want separate icons side by side."* Two relays of that answer exist and are deliberately not merged into one quote (L-013); the decision above is the part both support.

**Icon-only, added 2026-08-02, founder-direct:** the heat button renders `Image(systemName: "flame.fill")` alone — **no `Label`, no visible text string beside or beneath the glyph.** Aviran, live hilos `@chief` chat, verbatim *"remove the name from the icons in the nav bar, show only icons"* (`PROGRESS.md`, 2026-08-02 FOUNDER-DIRECT STUB). Carries no behavior change and touches no accessibility surface — `.accessibilityLabel` still names the button for VoiceOver exactly as any icon-only control in this codebase already does (`NearMeButton`'s precedent, cited above). `ios-developer`: build this button as icon-only from the start; this is not a strip-the-caption-later instruction, there was never a caption in the build target to begin with. Search (T-038) and Profile (T-037) inherit the same icon-only rule for their own buttons in this same `MapNavRow` container once they're built — recorded centrally in `design/ux-flows.md`'s 2026-08-02 addendum, not duplicated per-task.

**Visual only; no behaviour is touched** — exclusivity, the z-order table, the never-covered guarantee, and the three dismissal paths all stand.

**Glyph, closed at v2:** `Image(systemName: "flame.fill")`, pinned by `designer` 2026-08-02 (founder-direct *"change the heat icon to flame"*), reasoned against the app's own vocabulary — `NearMeButton` rests at `location.fill`, the same default-to-`.fill` precedent for a circular chrome button, and "modal open" is already carried by the button's background so a glyph swap would be a redundant second channel. This closes the gap v1's D6 flagged. **Still open and still an engineering default: [ASSUMPTION]** background shape, material and spacing follow the existing `NearMeButton` floating-chrome idiom (`.frame(44×44)`, `.background(.thinMaterial, in: Circle())`) — the only bottom-chrome idiom the shipped app has. Cheap to overturn: one button, one file.

### D7 — Edge gesture is a SwiftUI `DragGesture` on a hit-testable overlay **[new, v2]**
Settles design §8 item 6 and PRD open technical question (b). Full reasoning in §2.4 and §4.8. The short version: the UIKit route would exist to arbitrate against MapKit's pan recognizer, SwiftUI's `Map` gives no access to that recognizer, so the arbitration cannot be established — and hit-test order makes it unnecessary anyway. **This corrects the design spec's stated mechanism** (§2, §7, §8 there describe the 24pt zone as needing to win arbitration). The 24pt number is unchanged and Q7 is not reopened: its acquisition argument, which is what Aviran ratified, is untouched. Two costs are accepted rather than hidden: the strip is undraggable and untappable map (§2.4), and a horizontal drag starting in the strip is consumed without panning (§4.8). The gesture uses `DragGesture`'s **default `.local` coordinate space**, not a named one (§4.8, corrected at v3).

**This decision ships with a required confirmation, not on reasoning alone [v3].** "MapKit's pan recognizer is never in that touch's recognizer chain" is a prediction from documented hit-test ordering, and `FB19394663` — cited in this same TRD — is a filed case of SwiftUI `Map` not matching that class of reasoning. **§9 row 7(e) and C13 make it falsifiable on the in-band vertical drag**, the only case that exercises it: `camera`/`MKCoordinateRegion` byte-identical throughout, on device or in a UI test. If it fails, D7's construction is what changes and the fallback is a product conversation about the edge path (there is no third construction that arbitrates, because there is no recognizer to arbitrate against) — which is precisely why it must fail at C13 rather than in the field.

### D8 — 64pt / 40pt confirmed, and re-derived so they hold off the reference device **[new, v2]**
Settles design §8 item 7. Both numbers are correct: 64 = 59pt (largest current top safe-area inset, Dynamic Island) + 5pt; 40 = 34pt (home indicator) + 6pt. They are hardcoded worst-case values, so `EdgeGeometry.band(in:safeArea:)` computes `max(floor, safeAreaInset + clearance)` instead — identical output on every current device, automatically correct on a future one. The design's 708pt / ~59pt-per-stop arithmetic is preserved exactly on an 812pt device, and the shortest current portrait iPhone (667pt) still gives ~47pt per stop.

### D9 — The edge path is portrait-only on iPhone **[new, v2]**
No upstream doc considered orientation; the app ships all three (`project.pbxproj:367`). In landscape the sensor housing occupies a long screen edge (59pt horizontal safe-area inset on Dynamic Island devices), so the capture zone would sit under the housing and Q7's "cannot overshoot past the bezel" argument does not hold; the band also drops to ~24pt per stop. The button path is unaffected and req 6 already guarantees every hour through it, so nothing is lost. One row in one pure function (§4.10) — cheap for `product` or `designer` to overturn, and `qa` can check it with a rotation.

### D10 — A bundled density seed ships in this task **[new, v2]**
Full reasoning in §3.4. Without it, Build Phase 1 renders every Hood empty at every hour and three of PRD req 2's four bullets have nothing to observe. Follows T-033's shipped `BuildPhase.seedIsAuthoritative` pattern exactly rather than inventing a second mechanism, and stores **relative** offsets so the demo is correct at any launch date. **Flagged for `product` at `trd-review`** — it adds a data artifact to a PRD whose Technical design says "nothing to source or author," and that confirmation should be explicit.

---

## 9. Verification — one row per P0 requirement

Per `architect.md` (L-018): every P0 requirement names a falsifiable check with an observable, a pass condition, and the layer it is checked at. `qa` builds `prds/time-slider/TEST-PLAN.md` from this table. **No row's pass condition is "looks right."**

**And no row's pass condition is a value handed to the renderer.** A requirement is verified at the layer the user perceives it. `HeatModalCard`'s padding constant is an *input* to layout; the check belongs on what the two views' frames actually did — which is the whole of row 5b below.

**Six standing rules for this table** — the count was stale from v4 and is corrected here; the list has grown at v5, v6 and at acceptance. The first two are lifted verbatim in substance from the `search-quick-filters` TRD §9 (T-053, 2026-08-03), where they were written after a row passed while its requirement failed; they are restated here rather than cross-referenced because `qa` reads this table on its own. **The general ones now live in `architect.md` §9 and bind every TRD in this workspace** — empty-set, positive-control, rendered-output, and (ratified 2026-08-07 at T-077, below) sequenced-behind-a-known-failure. They stay written out here because `qa` reads this table on its own. The last rule is local to this feature's surface. The first two are about conditions that are *true for the wrong reason*:

- **No pass condition may be satisfiable over an empty set.** "Every X has property P" is worthless without a stated non-zero count of X, because the failure being guarded against is usually "no X was produced at all." A geometric non-intersection check is the sharpest case: two frames that never rendered do not intersect either.
- **Every negative-existence check needs a positive control.** "No overlap", "no truncation", "grep → 0 hits" all pass identically when the thing under test was never produced. Each such check names, alongside it, something that **must** be present; if the positive control is absent, the row is **unrun, not passed**.
- **Rendered-result rows are run on a rendered app.** Rows 5b and 6(c) cannot be discharged by a source read, by `XCUIElement.exists`, or by a "PASS by construction" note — `exists` is `true` for a fully occluded element and `.label` returns the whole string for a truncated one. If the environment blocks the run, the row is **BLOCKED**, and BLOCKED is reported as unrun.
- **A rendered row names a geometric observable, never a verbal one [new at v5].** "No clipping", "no truncation", "no wrap", "reads correctly" are not checks — XCUITest cannot see any of them through `.exists` or `.label`. What it *can* see is frames. So every rendered claim in this table is restated as a frame comparison with recorded numbers (non-zero size, containment, separation, height against a one-line baseline), and the numbers go in the report. **And the environment is set through the app, not through the simulator:** `-UIPreferredContentSizeCategoryName` and `xcrun simctl ui <udid> content_size` are both confirmed non-functional on this toolchain (Xcode 17F113 / iOS 26.5 — established live at T-038/`PAS-29`, re-confirmed at `PAS-51`; also recorded in `passenger-code/CLAUDE.md`'s Simulator facts). Text size and the clock are driven by **C15**'s launch-argument overrides instead. A row is BLOCKED only if C15's seam itself fails to take effect, and that is a finding to report, not a reason to substitute a source grep.

- **A sub-check sequenced behind a known-failing sibling is unrun, not passed [added by `product` at acceptance, T-077, 2026-08-07; **ratified by `architect` the same day and promoted to `architect.md` §9**, where it now binds every TRD in this workspace].** This table's sub-checks are written as independent claims — row 5b's "in captures (a) and (b) **independently**" is the sharpest case — but `SearchHourSegmentInteractionTests` sets `continueAfterFailure = false`, so the *first* failing assertion in a test method aborts every assertion after it, and `xcodebuild` reports exactly one failure line for the whole method. A reader who counts failure lines then concludes "only that one sub-check failed" is reading silence as a pass. **So: no rendered sub-check may share a test method with an assertion that is known to fail and is owned by another ticket.** Where one exists, it moves to its own test method, so it stays visibly red and tracked while its siblings still execute. And a report on this table states, per sub-check, *that it executed* — a sub-check whose execution cannot be demonstrated in the result bundle is **unrun**, exactly as a BLOCKED row is. Evidence this is not hypothetical: at `1021428`, row 5b's capture (b) (AX3 occlusion, containment, ≥44pt) and the F2 wrap check never executed at all, because the known 31pt `hourSlider` failure (owned by T-081/`PAS-76`) aborted the method at the *default* capture — and both `code-review` and `qa` reported them as passing. **Ratification, `architect`, 2026-08-07 (T-077):** accepted as written and generalised. It is not specific to this file — eight of this repo's ten `PassengerUITests` classes set `continueAfterFailure = false`, and the same abort-then-report-one-line shape is produced by `try #require`, `XCTUnwrap`, and any early `return` inside a shared assertion helper, so the rule is stated in `architect.md` in those terms rather than in XCTest's. Two clauses added on ratification: the report must state, per sub-check, *that it executed* (already `product`'s intent, now the wording), and the layer column of any row this applies to must say so, since `qa` reads the row and not this preamble. `XCTExpectFailure` is confirmed as the wrong tool, for `product`'s reason.

- **A rendered row names the surface that exists, not the one it was written against [new at v6].** `HeatModalCard`/`HeatButton` were deleted by T-078/`PAS-60`; every rendered row below is run against **`SearchOverlay`'s Hour segment**, reached nav-row `SearchButton` (label `"Search and hours"`) → `"Hour"` picker segment — **two taps**. Because that card's height is a fixed screen fraction rather than content-sized, **no pass condition in this table may be stated on the card's own frame**: it is identical at every text size, so such a condition passes whether or not the thing it guards works. Card-frame observables are replaced by *content-element* observables plus *containment within* the card. A row that cannot fail is the same defect as a row that cannot pass.

**Read the standing rules above as history where they name rows 5b and 6(c) [v7].** Both rows are **retired** — the surface they measured (`SearchOverlay`'s Hour segment, and `HeatModalCard` before it) was deleted by T-081/`PAS-76`. The rules themselves still bind every other row in this table and every TRD in this workspace; only their worked examples are about rows that no longer run. Rules 3, 5 and 6 are kept verbatim for exactly that reason: each was written after a real failure, and deleting the example would delete the evidence.

**Scope note, replaced at v5.** v4 added row 5b and stated plainly that rows 1–7 had never been audited against the rules above. **This v5 pass audited all of them** (L-047: an amendment re-audits the whole table, not only the row it was dispatched for). Findings, all fixed in this same revision: rows 2(a)/2(d), 3, 5 and 7(b)/(c)/(d) carried negative-existence or "unchanged" pass conditions with no positive control — each now names one; row 6(c) carried the same stale AX5 capture as row 5b and is corrected identically. Rows 1 and 4 hold as written. Whether these rules become workspace-wide (`architect.md`) rather than per-TRD is still `retrospective`'s call, not settled here.

| P0 | Observable | Pass condition | Layer | Step |
|---|---|---|---|---|
| **1** Range now → +12h, hour-snapped, clamped, reachable from any touch-down point | `EdgeGeometry.hour(atY:in:)` over a swept `y`; `Slider` binding's `set` | Exactly 13 distinct outputs across the band; `y` above/below the band returns 12/0, never 13 or −1; every output is an `Int`; sweeping from any start `y` to either band end reaches 0 and 12 | unit | C4, C11 |
| **2** Map repaints for the hour; camera/zoom unchanged; <400ms; silent-empty | (a) `HeatComposition.fills` output for two hours over the seed; (b) `XCTOSSignpostMetric` on `HourRepaint`; (c) `camera` after a full-range drag; (d) a Hood with a `null` seed hour | (a) `[HoodFill]` differs for two hours and is identical for the same hour — **[v5 audit] with the count of non-`.clear` fills recorded and ≥3 in both hours**, since two empty arrays are also "identical for the same hour"; (b) **[re-targeted at v7 — and currently UNRUN, not passed]** p90 < 400ms driving the hour through an **`EdgeHourZone` in-band vertical drag**, the sole surviving writer (`EdgeHourZone.swift:90`). `hourSlider` and its driver `adjust(toNormalizedSliderPosition:)` were deleted with the Hour segment (T-081/`PAS-76`), and `PassengerUITests/HourRepaintPerformanceTests.swift` was deleted with them — so **this sub-check has no test today and must be reported as unrun until C17 lands**, never as passing-by-inheritance from the deleted suite. The `HeatRepaintSignpost` instrumentation itself survives and is already bracketed around the edge writer (`EdgeHourZone.swift:89`, `MapScreen.swift:199`), so only the driver needs rebuilding; (c) `MKCoordinateRegion` byte-identical before/after; (d) `band == nil` → `.clear` fill, no banner, and no surface auto-presents (**[v6] reworded** — v5 said "no modal", naming the deleted `HeatModalCard`) — **[v5 audit] positive control:** in the same pass, a Hood with a non-`null` seed hour renders a non-`.clear` fill, so "no banner" is a claim about a map that actually drew | unit + UI test + manual | C6, C7, C10, **C17** |
| **3** "Now" every cold launch, re-resolved against the real clock | A fresh `DensityStore(now:)` with an injected clock | `selectedHour == 0` and `anchorHour == hourFloor(injectedNow)`; grep of the diff finds no `UserDefaults`/`AppStorage`/file write of the hour — **[v5 audit] positive control:** the same grep is run for a token the diff certainly contains (`selectedHour`) and returns a non-zero, recorded hit count, because a grep over an empty or wrong-path diff returns zero for both | unit + review | C8 |
| **4** Session persistence across every dismissal path | **[rewritten at v6 — `.heat` no longer exists; narrowed at v7 — the Hour segment no longer exists either]** `MapChromeState.toggle(.search)` → `toggle(.places)` → `toggle(.search)`; and set-by-edge → read-back after a full present/dismiss cycle. **Deleted at v7:** the intra-surface path (Hour segment → Search segment → Hour segment without dismissing) and the "read-by-slider" reader — T-081/`PAS-76` removed the segmented control and `HourSlider`, so neither is constructible. **There is now exactly one writer and no second reader UI**, which makes the desync this row guards against unreachable *through the UI* but not through `MapChromeState`, which is what the surviving sub-checks exercise | `selectedHour` unchanged across every switch above; the value set by an edge drag is the value still held after the overlay is presented and dismissed. **[v6 audit] positive control** — this is an *unchanged* claim and passes identically if the hour never moved at all: the value under test is first driven to a **non-default** hour (`selectedHour != 0`, recorded) before the first switch, so "unchanged" is a claim about something that had changed | unit + manual | C2, C11 |
| **5** Hour readable as a number; explicit "now" mark; never colour alone | `HourFormat.readout` strings; the rendered "now" mark | `offsetLabel` is non-empty at all 13 offsets; "Now" at 0; a midnight-crossing case sets `isNextDay`; the "now" mark differs from an ordinary stop in **shape** — **[v5 audit] restated as a geometric observable**, since "differs in shape" is not something a test can see: with the colour catalog forced to greyscale, capture the "now" mark's frame and an ordinary stop's frame, record both, and assert they differ in `width` **or** `height` by ≥2pt. Both frames must be non-zero first, or the row is unrun. **[v7] The subject and the layer both narrow.** `HourSlider`'s decorative tick overlay was one of this check's two subjects and is deleted (T-081/`PAS-76`); the surviving "now" mark is `EdgeHourTrack`'s tick alone (`EdgeHourTrack.swift:50`, `NowTick` on `EdgeRail`). That view is `.accessibilityHidden(true)` by deliberate design (§4.11), so **the comparison is a screenshot pixel scan, not an `XCUIElement.frame` comparison** — and it is observable **only during an active edge drag**, since the track does not render otherwise. **Do not make the track accessible to obtain frames**: that trades a stated design decision for test convenience, the same trade v6 refused for `HourReadout` | unit + **rendered** (screenshot pixel scan during a live edge drag; measurements recorded; blocked → BLOCKED, not passed) | C3, ~~C5~~ **C14** |
| ~~**5b**~~ **RETIRED at v7 (T-090/`PAS-88`)** — the rendered readout row, twice re-targeted, now has no surface | — (the elements this row named are deleted or renamed) | **Nothing left to check. Not "passing", not BLOCKED — retired.** This row made §2.3's z5 layering rule falsifiable on the *modal* hour readout: written at v4 against `HeatModalCard`, re-targeted at v6 onto `SearchOverlay`'s Hour segment after T-078/`PAS-60` deleted the first surface, and retired here because **T-081/`PAS-76` deleted the second** — `hourContent`, `HourSlider.swift` and `HourReadout.swift` are gone, and there is no third in-modal surface, because Aviran removed the path rather than replacing it. Every identifier this row named is deleted (`hourReadout`, `hourSlider`) or renamed (`hourSegmentCard` → `searchOverlayCard`, `SearchOverlay.swift:107-114`), and its suite `PassengerUITests/SearchHourSegmentInteractionTests.swift` is deleted. **What the row cared about, and where each concern went — stated so nobody re-adds it blind:** (a) *occlusion by the nav row* does **not** transfer to the surviving edge path — `MapNavRow` is a centre-anchored 3-button `HStack` (`MapScreen.swift:544-551`, `.padding(.bottom, 32)`) while `EdgeHourTrack`'s readout chip renders at `railX ± (chipInset + 20)`, ~32pt from a live screen edge (`EdgeHourTrack.swift:72-75`), so the two do not share x-extent. **[ASSUMPTION]** — read from source at `passenger-code 2a2a4ac`, not measured on a rendered app. (b) *wrap/clip at large text* does not transfer either: the chip is `.fixedSize()` over a two-label `VStack` (`EdgeHourTrack.swift:60-71`), so it grows rather than wraps — §4.9 already stated this ("its container is sized to content so it cannot clip") and that claim predates this arc. (c) *the AX3/AX5 rendered capture* is unobtainable on the edge path by construction, since `EdgeHourTrack` is `.accessibilityHidden(true)` (§4.11). **Not silently closed:** PRD v9 req 5's rendered-legibility bullet was written about the modal readout (F1's truncated "next day" pill, F2's AX5 wrap) and its subject no longer exists. Whether that bullet retires with the surface or is re-homed on the edge chip is **`product`'s call at T-090's PRD rewrite, not this amendment's to invent** — if it is re-homed, this TRD owes a new row and a new build step, and both are cheaper to write then than to guess at now | ~~UI test on a rendered app~~ — none | ~~**C16**~~ — retired with the row (§11) |
| **6** VoiceOver discrete steps; ≥44pt on the button path; Dynamic Type; contrast — **three of its four sub-checks lost their surface at v7 (T-081/`PAS-76`)** | (a) **OPEN — bounced to `product`, see the pass-condition cell**; (b) ~~the `Slider`'s frame height~~ **retired**; (c) ~~rendered readout at the Hour segment's Dynamic Type ceiling~~ **retired**; (d) `ContrastRatio` over the token pairs — **unchanged and still live** | **(a) is neither retired nor passed — it is an open P0 gap with no implementation, and this row records it rather than closing it.** `HourSlider` was the app's only VoiceOver-operable hour control. §4.11 hides `EdgeHourTrack`/`EdgeHint` from assistive technology *on the explicit stated grounds* that "req 6's assistive-tech bullet is satisfied entirely by the button path" — T-081 deleted that path, so the premise is now false; and `EdgeHourZone` carries no accessibility modifiers of any kind (checked at `passenger-code 2a2a4ac`). **There is consequently no adjustable element and no discrete-step behaviour anywhere in the app.** No pass condition can be written for a requirement with no implementation, so per `architect.md` §9 this is **bounced to `product`**: either accept the regression and amend req 6, or re-home the bullet on the edge path. Either answer is a product/design decision with a build consequence, and this TRD takes a new row plus a new build step once it lands. **Do not record this sub-check as passed, retired, or BLOCKED — it is open.** (b) **retired** — "≥44pt on the button path" had `HourSlider`'s frame as its only subject and there is no button path. The edge path's own acquisition-target argument is the 24pt capture zone, ratified separately at Q7 on edge-anchoring grounds (§2.4), and it is **not** a substitute for a 44pt claim. (c) **retired** — at v6 it delegated wholly to row 5b's captures, and those are retired above. (d) **unchanged:** `MutedOnSurface` on `Surface` and on `PillSurface` ≥4.5:1, and `NowTick`/`SliderFill`/`EdgeRail` on `Surface` ≥3:1, all in both `UIUserInterfaceStyle`s — and the native thumb/rail are **not** asserted (§4.12). **[v7 note, no change owed]** `SliderFill` now has no view referencing it (`HourSlider` deleted); its assertion in `HeatModalContrastTests` still passes and still guards the token, but it guards a token nothing draws — worth knowing before it is read as coverage of a live surface. **[v7, second instance of the same thing, and it makes the note a pass condition rather than an aside]** `PillSurface` is in the identical position — `HourReadout`'s "next day" pill was its only consumer and grep at `passenger-code c6398f9` finds **zero `Color("PillSurface")` anywhere in `Passenger/`** — so **two of this sub-check's five asserted pairs are over colour sets no shipping view draws.** They compute a real ratio and pass forever, which is the empty-set rule in a costume: the population the requirement is about is *rendered* pairs, and the check is over *declared* ones. **Closed form, so an unenumerated pair fails instead of passing:** the live population is exactly what `EdgeHour/` draws today — `MutedOnSurface` on `Surface` (≥4.5:1) and `NowTick`/`EdgeRail` on `Surface` (≥3:1) — enumerated against a fresh grep of `Color("…")` under `Passenger/EdgeHour/` in the same pass, with the hit count recorded and non-zero; any token drawn there and absent from this list fails the row. `SliderFill` and `PillSurface` are **retained as re-introduction backstops and explicitly discharge nothing** — a future author who re-draws a pill inherits a token already held to the bar. **[v7] `HeatModal/` is no longer part of §4.12's construction rule in practice:** the folder contains `HourFormat.swift` alone, which draws nothing, so the rule's live scope is `EdgeHour/` | (d) unit. (b)/(c) retired. **(a) has no layer — it is open and owned by `product`** | **C4** and **C5** are history, not live steps — their artifacts are deleted (§11). (d): C9, C12 |
| **7** Edge slide: both live edges, vertical-only, one shared value, no false fire, **camera untouched by the normal drag**, inert under a sheet | (a) `EdgeAvailability.liveEdges` over the full input matrix; (b) a horizontal-dominant drag inside the band; (c) a pan starting outside the band; **(e) a normal vertical, in-band drag on each live edge, full band travel — `camera` sampled at touch-down, mid-drag and `onEnded`**; **[d1/d2 re-targeted at v7 — the detents they named no longer exist]** ~~(d1) an edge drag with `HoodSheet` at `.medium`… (d2) the same at `.large`~~ → **(d) an edge drag with each depth-1 destination presented — `HoodSheet`, `PlaceDetailModal` reached directly, and `EventDetailModal` — plus one depth-2 case (a place opened under a Hood), on the surface's own content **and** on the still-exposed map; four presented states, two touch targets each; and `EdgeAvailability.liveEdges(…)` sampled in the same states** | (a) matches §4.10's table exactly, every row; (b) `selectedHour` and `camera` both unchanged; (c) the map pans normally, no track appears; **[v5 audit] one positive control covers (b), (c), (d1) and (d2) together:** every one of them is an *unchanged* / *nothing appeared* claim, and all four pass identically if the gesture never reached the app at all — so each is run in a session that also performs sub-check (e)'s ordinary in-band vertical drag and observes `selectedHour` move across all 13 stops and the track appear. If the control drag does not move the hour, the negative sub-checks are **unrun, not passed**; **(e) `selectedHour` moves across all 13 stops and `camera`/`MKCoordinateRegion` is byte-identical at all three samples — same comparison method as row 2c. This is the check for D7/§2.4's central claim; a drift or jump here fails the row, and no other sub-check can substitute for it**; **(d) rewritten at v7, and the rewrite is not cosmetic — the old sub-checks named a construct the app no longer contains.** T-079/`PAS-73` moved every detail surface off `.sheet()` onto in-hierarchy overlays: at `passenger-code c6398f9` a repo-wide grep finds **zero live `.presentationDetents` and zero live `.presentationBackgroundInteraction`** (every hit is a comment), so `.medium`/`.large` are not states this app can be put into and the two-behaviours note is spent. **The requirement behind them is intact and now has a stronger observable.** In each of the four presented states: `EdgeAvailability.liveEdges(…)` returns the **empty set** (recorded, per state), no track appears, and `selectedHour` is unchanged — which is a claim about the writer being *absent from the hierarchy*, not about a gesture politely losing (§2.3, D7 rule c; `EdgeAvailability.swift:16`, `MapScreen.swift:1187`/`1198-1211`). **Closed-form, so an unenumerated state fails rather than passes:** the presented states under test are exactly the four the router can express — `hood`, `place` at depth 1, `event`, and `place` under `hood` — and the enumeration is proved complete against `DetailRouter`'s three fields in the same pass; a fifth destination added later without a row here is a gap this row is written to expose. **Positive control, and this row needs its own rather than borrowing (b)/(c)'s:** every claim in (d) is a *nothing-happened* claim over a state where the zone is deliberately absent, so it also passes if the harness never presented anything — each state therefore records the presented surface's own identifier as visible **before** the drag, and `liveEdges` non-empty in the same session with nothing presented. Without both, (d) is **unrun, not passed** | unit + **UI test or on-device for (e)** + manual | C11, C13 |

**Two carried-forward bullets, called out.** `product`'s T-031 acceptance found req 2's *repaints on hour change* and *<400ms* had zero traced test cases and assigned them to T-032's `qa`/`acceptance`. Row 2 above is that assignment discharged — with the seed (D10) as the precondition that makes either checkable at all. `qa` must show a real case in the trace column for both, not a "PASS by construction" note; that distinction is precisely what `product` caught at T-031.

---

## 10. Risks and alternatives

| Risk | Mitigation / decision |
|---|---|
| The 24pt strip at each edge is undraggable, untappable map — ~12% of an iPhone's width | Accepted, and now stated with its real mechanism (§2.4, D7) rather than as an arbitration cost. `qa` checks that a pan starting outside the band behaves normally. If it proves intolerable in use, the lever is the width constant, and widening or narrowing it re-opens Q7 with Aviran, not in a build. |
| **D7's hit-test prediction is wrong and MapKit pans under every ordinary edge slide** — the map jumps or drifts under the finger on this feature's primary gesture, a visible regression against T-031's shipped camera behaviour **[added at v3, `ios-code-reviewer`]** | The claim is now labelled a prediction, not a settled fact (§2.4, D7), and made falsifiable at the earliest point it can be: **§9 row 7(e) / C13 item 1** check `MKCoordinateRegion` byte-identity through an in-band *vertical* drag, on device or in a UI test. v2's checks could not have caught this — an inert horizontal drag and a pan outside the band both pass whether or not MapKit saw the touch. If it fails, there is no third construction to fall back to (`Map` exposes no recognizer to arbitrate against), so the fallback is a product conversation about the edge path — which is why C13 is defined as not-done until this passes, rather than leaving it to `qa`. |
| A horizontal drag starting in the strip is consumed without panning the map | Named honestly (§4.8). (b)'s vertical-dominance latch guarantees no false hour change, which is the checkable promise; handing the touch back is not achievable in either construction, since SwiftUI's `Map` exposes no recognizer to defer to. |
| `SpatialTapGesture` on `Map` also fires during an edge drag and opens a Hood sheet | Should hold by construction (the gesture is in `Map`'s subtree, the overlay is not) — **confirm, do not assume**; C13 and §9 row 7. |
| The Build-Phase-1 seed makes the feature look verified when only the seed path is | §7 states plainly that Phase-2 acceptance must re-run req 2's data-dependent bullets against the live feed. The seed is named in §3.4, in `Source.seed`, and in the build step — never invisible. |
| The seed is authored without hour-to-hour variation, so C6 and `qa` pass vacuously | §3.4 states the authoring rule as a requirement (≥3 Hoods changing band across ≥4 adjacent hour pairs, ≥1 `null`), and C10 is the step that owns it. |
| SwiftUI re-renders every polygon on an hour change and misses 400ms | Polygons keep stable `Hood.id` identity; only `foregroundStyle` re-evaluates, over dozens of shapes. Measured, not assumed (§9). Fallback is caching resolved `ShapeStyle` per band — local, not architectural. |
| The `HourRepaint` signpost measures resolution, not pixels | Stated plainly in §4.7 rather than claimed as end-to-end, backed by the structural no-fetch guarantee and a perceptual check at `qa`. Same posture T-031 took on `XCTApplicationLaunchMetric`. |
| Custom overlay reimplements sheet behaviours badly | The behaviours are small and enumerated (§4.2); the alternative is unusable, since `.sheet` covers the nav row and breaks the nav-switch rule (D2). |
| Landscape exclusion (D9) is an architect call no upstream doc made | Flagged as such, with its reasoning, and made trivially reversible (one row, §4.10). Named for `product`/`designer` at `trd-review`. |
| The nav row ships with one button and reads as unfinished | D1 — deliberate, reversible, preferable to a dead control. |
| Req 2's "any open sheet is unchanged by an hour change" is unexercisable | ~~The two can never be co-presented (D4, Q6, §2.3), so the bullet is satisfied structurally rather than behaviourally.~~ **Restated at v7 (T-090/`PAS-88`) — the old mitigation is now vacuously true and argues nothing, and its "(D4)" cited a decision that no longer exists under that number** (v1's D4; today's D4 is a different row — see D4's numbering note). There is no modal (T-081/`PAS-76`) and no system `.sheet` either (T-079/`PAS-73`; zero live `.presentationDetents`/`.presentationBackgroundInteraction` at `passenger-code c6398f9`). **The bullet still holds, on a mechanism that is checkable rather than definitional:** `EdgeAvailability.liveEdges(…)` returns `[]` whenever `detailRouter.isDepth1Presented` is true, so `EdgeHourZone` — the sole writer — is **absent from the view hierarchy** while any detail surface is up, at either depth (§2.3, D7 rule c). That is §9 row 7(d)'s check, and unlike "they are never co-presented" it can fail. **Still flagged rather than quietly passed, and the flag has changed shape:** the open question is no longer "did `product` intend them to coexist" but "is *no way at all* to change the hour while a sheet is up acceptable" — routed to Aviran as PRD **Q9(b)**, because the modal that used to cover that state is gone. Not this TRD's call. |
| Non-whole-hour timezones render a `:30` clock label | Cosmetic, P1 surface only, outside V1's single city. §3.2 `[ASSUMPTION]`. |
| Touching accepted T-031 code (`DensityStore`) | Three named changes in §4.5, each with its reason. T-031's existing tests must pass unmodified. |
| **A layering rule stated in §2.3 is not a rule any gate can fail** — the build bottom-anchors the card, the nav row draws over the readout, and `code-review`/`qa` both pass because neither renders the app **[added at v4, T-055, after it happened]** | Row 5b is that rule made falsifiable, on rendered frames, at both text sizes, with a positive control. The residual risk it does *not* cover: **the other four z5-shaped surfaces share the pattern** — `PassportSurface`, `PlacesListOverlay` (`.padding(.bottom, 8)`) and `SearchOverlay` (`.padding(.bottom, 4)`) all sit under the same 96pt nav row, found by source read at `product`'s acceptance and filed as **T-054** (`ios-developer`). Row 5b binds this TRD only; it does not and cannot verify three other PRDs' surfaces, two of them already accepted. |
| **C15 puts test-only branches in shipping code** — the thing this codebase's scope gate exists to keep out **[added at v5]** | Accepted, deliberately, and bounded: two launch-argument reads, defaulted to today's behaviour, at one composition root, guarding no feature and reachable only from a UI-test launch. The alternative was the status quo `PAS-51` found — a P0 rendered row discharged by a source grep its own Layer column rules out by name, and a positive control that fires only after local noon. **[ASSUMPTION], stated because it is load-bearing and unverified by this pass:** that `.environment(\.dynamicTypeSize, …)` applied at `MapScreen`'s root propagates into `HeatModalCard` and is then clamped by its own `.dynamicTypeSize(...maxDynamicTypeSize)` — standard SwiftUI environment behaviour, but not observed live here. If `ios-developer` finds it does not take effect, that is a **BLOCKED** disclosure written into row 5b, not grounds to fall back to the grep. |
| **A verification row outlives the surface it measures** — row 5b was written against `HeatModalCard`, which a concurrent task deleted mid-build, and three of its pass conditions were then *inverted* by the specs that replaced it (bottom-flush card, nav row drawn on top) **[added at v6, T-077, after it happened]** | Re-targeted rather than ported: v6 re-derives every observable from `SearchOverlay`'s actual structure and deletes the three inverted clauses by name, so nobody re-adds them. Residual risk, named: **this TRD's §2–§5 still describe the deleted surface**, and a reader who takes them literally will build against a card that doesn't exist. Disclosed in the v6 header rather than papered over by a rewrite this task has no mandate for. The general lesson — a §9 row is only as durable as the type name it quotes — is `retrospective`'s to generalise, not this TRD's. |
| **The replacement surface makes a pass condition *unfalsifiable* rather than unsatisfiable** — `SearchOverlay`'s card is a fixed screen fraction, so any card-frame assertion is true at every text size **[added at v6]** | Every card-frame observable moved to the content elements plus containment (row 5b (i)–(iii)), and §9's standing rules gain the rule that says so. Stated plainly because the instinct on re-targeting is to keep the same clause and swap the identifier — which here would have produced a row that passes forever. |
| **The fixed-height card clips its own content instead of growing** — at `.accessibility3`, `hourContent`'s top-aligned `VStack` can push `HourSlider` past the card's bottom edge, which is also the screen's bottom edge; a P0 ≥44pt control lands off-screen and nothing in the old row looks for it **[added at v6]** | Row 5b (ii)/(iii) is exactly this check, and it is the substantive new coverage v6 buys. If it fails, the fix is a layout call on `SearchOverlay` (scroll or size the Hour segment's content), owned by `nav-row-v2-redesign.md`, not a change to this row. |
| **`HourReadout`'s combined accessibility element hides the pill from XCUITest**, so F2's original per-element wrap check is unobtainable **[added at v6]** | Accepted deliberately — the combine is a P0 VoiceOver behaviour (one spoken unit, not three stops). The wrap check moves to the combined row's height, which detects the same failure. **Un-combining the element to make the test easier is explicitly out of bounds**; if a future pass thinks it needs per-element frames, that is a design conversation about VoiceOver, not a test refactor. |
| Synthetic density makes every future hour a simulation, not a forecast | Named in the PRD and strategy; unchanged here. Nothing in this TRD should be read as making the control more truthful than the data behind it — least of all the seed. |

**Alternatives considered and rejected:** a `UIGestureRecognizer` subclass for the edge path (D7 — the arbitration it would buy is unreachable); `.sheet(isPresented:)` for the modal (covers the nav row — D2); a fully custom horizontal slider (loses free discrete VoiceOver stepping, a P0 — D5); a repeating timer to re-resolve "now" (D3); persisting `selectedHour` across launches (contradicts req 3); a per-hour network fetch (would make the 400ms budget unachievable); hardcoding 64/40 as literals (D8); enabling the edge path in landscape against a housing-occluded edge (D9); shipping Phase 1 with no density data and calling req 2 satisfied by construction (D10); rendering three nav buttons with two inert (D1); asserting contrast on the platform-drawn thumb and rail (§4.12).

---

## 11. Build breakdown

Ordered. **Every step is `[iOS]`.** No `[Backend]`, no `[Algo/Data]` — see §1. C1–C9 are v1's, unchanged in scope; C10–C14 are new at v2; **C15 is new at v5**, **C16 was new at v6 and is retired at v7**, and **C17 is new at v7**. **C1–C15 were all built and shipped** (`passenger-code` through `967b7c2`).

**Two things a reader of this table needs before acting on it [v7, T-090/`PAS-88`]:**

- **C4 and C5's artifacts no longer exist and must not be rebuilt.** `HeatModalCard.swift` and `HeatButton.swift` were deleted by T-078/`PAS-60`; `HourSlider.swift` and `HourReadout.swift` by T-081/`PAS-76` (`passenger-code b2dc981`, merged `2a2a4ac`, Aviran-ordered and closed `Done`). Both steps are kept below as the record of what was built, not as work to do. `HourFormat.swift` survives and is still consumed — `MapScreen.currentReadout` feeds `EdgeHourTrack` — so C3 is untouched.
- **C16 is retired** (row below), and **C17 is the only outstanding step in this document**, owned by `ios-developer`. One further item is *not* a build step and is not listed as one: §9 row 6(a)'s VoiceOver gap is bounced to `product` and takes a step only once product answers it.

| # | Step | Tag |
|---|---|---|
| C1 | `MapChromeState` + `NavSurface` (§4.1) | **[iOS]** |
| C2 | `MapNavRow` — heat button only (D1), `flame.fill`, separate side-by-side buttons with no shared container chrome (D6); wire into `MapScreen`'s `ZStack` at z7; move the near-me cluster above it; bucket-2 fade driven by `isPresenting` (§2.3). Exclusivity unit test incl. hour-survives-a-switch (§9 row 4) | **[iOS]** |
| C3 | `HourFormat` + tests — numeral, clock label, `isNextDay`, VoiceOver string; injected clock/calendar; midnight-crossing and 0/12 cases (§9 row 5) | **[iOS]** |
| C4 | `HourSlider` — native `Slider(in:step:)`, the `Double` bridge, ≥44pt frame, non-hit-testing tick overlay, a11y label/value/identifier (§4.3, §4.4) | **[iOS]** |
| C5 | `HeatModalCard` + scrim + three dismissal paths + Reduce-Motion-aware transition (§4.2); `HourReadout` (numeral + "next day" pill) | **[iOS]** |
| C6 | `HeatComposition.fills` + switch `MapScreen` to one resolution per pass; the differs-across-hours unit test (§9 row 2a) | **[iOS]** |
| C7 | `HeatRepaintSignpost` + the `XCTOSSignpostMetric` UI test and a `measure` unit test against the 400ms budget (§4.7, §9 row 2b) | **[iOS]** |
| C8 | `DensityStore`: the two new `refreshIfHourRolled()` call sites + the mid-`await` guard (§4.5 items 2–3); cold-launch-reset test (§9 row 3) | **[iOS]** |
| C9 | The five colour sets + the token-level contrast test, light and dark (§4.12, §9 row 6d) | **[iOS]** |
| **C10** | **`DensitySeed` + `density-seed-tel-aviv.json` + the `BuildPhase.seedIsAuthoritative` branch in `DensityStore.load()` and `Source.seed` (§3.4, §4.5 item 1).** Authoring rule enforced by a test: ≥3 Hoods change band across ≥4 adjacent hour pairs, ≥1 `null` hour exists. **Do C10 before C6/C7** — both are unverifiable without it | **[iOS]** |
| **C11** | **`EdgeGeometry` + `EdgeAvailability`, pure, with their full unit-test matrices** (§4.9, §4.10, §9 rows 1 and 7a). No view work in this step — the two hardest things to get right land first, testable with no simulator | **[iOS]** |
| **C12** | **`EdgeHint` + the iPad ghost mark** (§4.11); `.allowsHitTesting(false)`, `.accessibilityHidden(true)`, Reduce-Motion fade | **[iOS]** |
| **C13** | **`EdgeHourZone` — the 24pt overlay, `DragGesture` in the default `.local` coordinate space (§4.8, corrected at v3), the vertical-dominance latch, hierarchy-level removal under a sheet or a presented surface (§4.8, D7).** Verify, and **this step is not done until the first item passes** (§9 row 7): **(1) [v3, blocking] a normal vertical, in-band drag on each live edge, travelling the full band — `selectedHour` moves across all 13 stops while `camera`/`MKCoordinateRegion` stays byte-identical, sampled at touch-down, mid-drag and `onEnded`, compared the same way §9 row 2c compares it, on device or in a UI test rather than by observation.** This is the only check that exercises D7/§2.4's central hit-test claim; if it fails, stop and re-open D7 rather than working around it. (2) a horizontal drag in the band changes neither hour nor camera; (3) a pan starting outside the band pans normally; (4) a drag does not also fire `MapScreen.handleTap`; **(5) [v3; re-targeted at v7 with §9 row 7(d) — C13 is built and shipped, so this line is the record of what the check now means, not new work]** ~~an edge drag with `HoodSheet` up, at `.medium` and again at `.large`… (`.presentationBackgroundInteraction(.enabled(upThrough: .medium))`, `MapScreen.swift:186`)~~ — **those detents no longer exist.** T-079/`PAS-73` moved every detail surface off `.sheet()` to in-hierarchy overlays; at `passenger-code c6398f9` there are **zero live `.presentationDetents` and zero live `.presentationBackgroundInteraction`** in the app. The check is now the four *presented states* §9 row 7(d) enumerates — `hood`, `place` at depth 1, `event`, and `place` under `hood` — on the surface's own content and on the still-exposed map, with `EdgeAvailability.liveEdges(…)` recorded empty in each and a positive control proving something was actually presented | **[iOS]** |
| **C14** | **`EdgeHourTrack` + the floating readout chip** — 13 stops, "now" tick, opaque `Surface` panel, chip position clamped to the drawn extent (§4.11); `.sensoryFeedback(.selection, trigger:)` for the P1 haptic | **[iOS]** |
| **C15** | **`UITestOverrides` — the rendered-verification seam [new at v5, `PAS-51` findings 1 and 4].** One small `enum` read once from `ProcessInfo.processInfo.arguments`, applied at the composition root only: (1) `-uiTestDynamicTypeSize <size>` → `.environment(\.dynamicTypeSize, …)` on `MapScreen`'s root, because the two *simulator* mechanisms for forcing a content size are both dead on this toolchain and this one is ours; (2) `-uiTestNow <ISO-8601 instant>` → the single `Date` that `MapScreen` passes to **both** `HourFormat.readout(now:)` (`MapScreen.swift:177`) and `DensityStore(now:)`, which already take an injected clock and are only hardcoded at the root. **Both default to today's behaviour when the argument is absent** — no branch runs in a normal launch, and neither override is reachable without an explicit launch argument. This is a testability seam, not a feature hook: §9 rows 5b, 6(c) and 5's rendered halves are unrunnable without it, and the alternative on offer was a source grep standing in for a rendered check. Keep it to one file and one call site each; if it grows a third override, that is a design conversation, not a quiet addition | **[iOS]** |
| ~~**C16**~~ | **RETIRED at v7 (T-090/`PAS-88`) — superseded by T-081/`PAS-76`, which deleted the surface this step existed to test.** C16 owned §9 rows 5b and 6(c); both are retired above, so the step has nothing left to build. **Disposition of its three parts, so nobody re-opens it looking for unfinished work:** (1) the `hourSegmentCard` identifier **landed and then outlived its name** — it survives as `searchOverlayCard` on the same card frame (`SearchOverlay.swift:107-114`), renamed at T-081 since the Hour segment it was named for is gone, and it is still queryable; the `.accessibilityElement(children: .contain)`-before-`.accessibilityIdentifier(...)` ordering C16 discovered live is documented in `MapNavRow.swift:40-52` and still correct. (2) the rendered AX3/AX5 suite in `PassengerUITests/SearchHourSegmentInteractionTests.swift` is **moot** — that file was deleted with the segment. (3) the comment-only retarget of `UITestOverrides.swift`'s doc comment **landed separately** as T-088/`PAS-86` (`passenger-code b90ba83`), which also removed C16's now-dead instruction to file BLOCKED against row 5b. **Do not rebuild any part of this step.** Its three prohibitions (no card-vs-nav-row separation assertion, no `maxY`-above-safe-area assertion, no un-combining of `HourReadout`) are retired with it, the first two because the shape they guarded is gone, and the third because `HourReadout` itself is gone | ~~**[iOS]**~~ |
| **C17** | **Rebuild the 400ms `HourRepaint` measurement against the edge writer [new at v7, §9 row 2(b)].** `PassengerUITests/HourRepaintPerformanceTests.swift` was deleted by T-081/`PAS-76` because it drove `hourSlider` through `adjust(toNormalizedSliderPosition:)`, and `ios-developer` disclosed the resulting gap in that commit's own message rather than papering over it. The instrumentation is intact and already brackets the surviving writer (`HeatRepaintSignpost.begin()` at `EdgeHourZone.swift:89`, `endIfPending()` at `MapScreen.swift:199`), so this step rebuilds **only the driver**: an `XCTOSSignpostMetric` UI test that moves the hour by an in-band vertical `EdgeHourZone` drag and asserts p90 < 400ms. **Two things it must do, both learned from the row it discharges:** state a **non-zero count of hour changes** the drag actually produced, so an empty measurement cannot pass as a fast one; and keep the measurement in **its own test method**, not sharing one with any assertion owned by another ticket (§9 standing rule 5). `EdgeHourZoneInteractionTests.swift` already performs exactly this drag for row 7 and is the natural place to borrow the gesture from — it is **not** a place to add this measurement, since that file's existing assertions are row 7's. **Until this lands, §9 row 2(b) is reported UNRUN, never passed.** | **[iOS]** |

**`trd-review` sign-off needed from: `ios-developer` + `ios-code-reviewer` only.** `developer`, `code-reviewer` and `data-engineer` have no step to review — this TRD writes no SQL, no RLS, no pipeline, and no algorithm. Two cross-checks worth one explicit pass at review: **T-033's TRD** against §2.3/§4.10/D4 (chrome layering, and the edge zone's interaction with `HoodSheet`'s drag-to-dismiss), and **`product`** on D10's seed and D9's landscape exclusion, both of which are architect calls that touch scope.
