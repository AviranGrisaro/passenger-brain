# Modals: full-width, bottom-anchored, one shared shape (T-079 / `PAS-73`)

**Type:** post-ship redesign pass (no PRD/TRD — app-wide chrome-shape correction, same lifecycle as `PAS-60`'s nav-row pass).
**Trigger:** founder-direct, live chief-of-staff chat, 2026-08-07. Verbatim: "Modal design bug — modals should be full-width, anchored to bottom (side-to-side and bottom), NOT floating/centered. All modals across app must share this same size/shape treatment." Full record: `passenger-brain/agent-os/PROGRESS.md`'s 2026-08-07 "L-002 stub" entry.
**Distinct from `PAS-48`** (already `Done`) — that task unified `presentationDetents`/`maxHeight` across surfaces (how *tall* a modal gets). This is a different axis: whether a modal is inset with rounded corners on all sides and floating above the screen edge, or flush to the screen's left/right/bottom edges. `PAS-48` didn't touch shape/anchoring at all — confirmed by reading every modal file below directly, not assumed.
**No render evidence** — source read only, same disclosed limitation as this pass's companion nav-row spec (`nav-row-v2-redesign.md`). A visual change never rendered is not "done" (L-036) — that check is `ios-developer`/`qa`'s, once buildable.

## The actual bug, found by reading every modal file directly

Passenger has **two structurally different modal shapes today**, and the split doesn't match any design intent — it matches which of two construction patterns a given surface happened to use:

**Group A — system `.sheet()`, already full-width/bottom-anchored (no fix needed):**
`EventDetailModal.swift`, `PlaceDetailModal.swift`, `HoodSheet.swift` — all three are presented via `MapScreen.swift`'s single `.sheet(isPresented: detailRouter.isDepth1Presented)` (line 533) / `HoodSheet`'s own nested `.sheet` for depth-2 (`HoodSheet.swift` line 44). A SwiftUI `.sheet()` is, by default, full device width, anchored flush to the bottom and sides, with rounded corners **only on the top two corners**. `presentationDetents([.medium, .large])` + `presentationDragIndicator(.visible)` (all three files, confirmed) doesn't change that shape — it only changes how tall the sheet is. **These three already satisfy Aviran's ask as shipped.**

**Group B — custom `ZStack` overlays, floating/inset (the actual bug):**
`PlacesListOverlay.swift`, `PassportSurface.swift`, `SearchOverlay.swift`, `HeatModalCard.swift`. All four share one `card` construction (confirmed byte-for-byte identical shape across all four files):
```swift
.background(Color("Surface"), in: RoundedRectangle(cornerRadius: 20, style: .continuous))
.padding(.horizontal, 8)   // ← insets both sides, breaking "full-width"
.padding(.bottom, 8)       // or HeatModalCard's own gapAboveNavRow/navRowBandHeight math
```
`RoundedRectangle(cornerRadius: 20)` rounds **all four corners**, and `.padding(.horizontal, 8)` pulls both edges in from the screen's sides. Combined with a bottom gap (`HeatModalCard`'s is the most extreme: `navRowBandHeight + gapAboveNavRow` = 92pt of clearance above the true bottom edge, by design, to clear the nav row beneath it), the result is exactly what Aviran is describing: a card that floats above and inset from the screen edges, not one flush to them. This is a real, confirmed, structural difference from Group A — not a subjective read.

**Why Group B exists at all (context, not an excuse):** each of these 4 files' own header comment says it deliberately avoided `.sheet()` because "a system sheet covers the nav row" (`PlacesListOverlay.swift` line 5, `SearchOverlay.swift` line 5, `PassportSurface.swift` line 5, `HeatModalCard.swift`'s TRD citation) — `ux-flows.md` §2.1's "direct-switch rule" needs the nav row to stay hit-testable underneath these surfaces, which a full-screen `.sheet()` would prevent. **That constraint is real and must be preserved** — the fix below keeps these as `ZStack` overlays, it doesn't move them to `.sheet()`.

## The fix — one shared shape for both groups

**Group A (system sheets): no code change.** Already correct. Named explicitly here so nobody "fixes" what isn't broken — re-styling a `.sheet()` to look like Group B's card would be a regression, not a fix.

**Group B (custom overlays): remove the float.**
```swift
.background(Color("Surface"), in: UnevenRoundedRectangle(
    topLeadingRadius: 20, bottomLeadingRadius: 0,
    bottomTrailingRadius: 0, topTrailingRadius: 20,
    style: .continuous
))
// no .padding(.horizontal, ...) — full device width, flush to both side edges
.ignoresSafeArea(edges: .bottom)  // flush to the true bottom edge, not inset above it
```
- **Corners:** top two only (`UnevenRoundedRectangle`, iOS 16+, already the minimum deployment target implied by the rest of this codebase's SwiftUI usage — `ios-developer` to confirm against the project's actual deployment target before using it; if it's unavailable, the fallback is `RoundedCorner` via a custom `Shape`/`clipShape` masking only the top two corners, same visual result). This matches Group A's own system-sheet corner treatment exactly, so both groups now look like the same family of surface.
- **Width:** drop `.padding(.horizontal, 8)` entirely — full width, edge-to-edge.
- **Bottom anchoring:** drop the floating bottom gap. `PlacesListOverlay`/`PassportSurface`/`SearchOverlay` already anchor via `ZStack(alignment: .bottom)` with no explicit bottom padding beyond `.padding(.bottom, 8)` — remove that 8pt. `HeatModalCard`'s case is different in *kind*, not just degree, and is folded into `SearchOverlay` as a segment by this pass's companion spec (`nav-row-v2-redesign.md` §1) — once merged, its "float above the nav row" problem is solved by removing the standalone surface entirely, not by re-anchoring it. If `ios-developer` lands the modal-shape fix before the nav-row merge, treat `HeatModalCard` as Group B too (same fix) until it's deleted.
- **Nav row hit-testability — the constraint these overlays exist to protect — needs a different mechanism now that the card is flush to the bottom edge**, since `MapNavRow` (52pt-tall buttons, z7, drawn last) would otherwise render *underneath* an edge-to-edge Group-B card sitting at the same z-position. **[ASSUMPTION, this spec's call]**: the fix is **not** "make the card shorter" — it's ordering. `MapNavRow` is already drawn last in `MapScreen.swift`'s overlay chain (line 514, "drawn last among this file's overlays so it renders above all of them") and z5's Group-B overlays are declared *before* it (line 472, comment: "Above the remaining fading chrome... below the system sheet at Site A"). That ordering already makes `MapNavRow` render on top of a full-height Group-B card today — the row survives edge-to-edge cards the same way it survives the current inset ones, because it's a later sibling in the same `ZStack`, not because the card stops short of the row. Removing the bottom-padding gap doesn't change this ordering, so nav-row hit-testability is preserved with no further change. **This should be confirmed on-device once buildable** — it's read correctly from the modifier-order comments, not observed rendered.
- **Drag-to-dismiss and scrim:** both unchanged (`DragGesture`, `Color.black.opacity(0.3)` scrim, dismiss threshold) — this fix is shape/anchoring only, not interaction.

## Correction — added at acceptance, 2026-08-07 (`product`, T-079 REJECT)

Two claims above were derived from source only and are **wrong on the actual runtime** (iOS 26.5, iPhone 17), measured first-hand at acceptance:

1. **Group A does not already satisfy the ask.** "A SwiftUI `.sheet()` is, by default, full device width, anchored flush to the bottom and sides, with rounded corners only on the top two corners" was true through iOS 18. On iOS 26 a `.sheet()` at a non-`.large` detent renders as an **inset, floating card, rounded on all four corners, with map visible on the left, right and bottom** — exactly the shape Aviran reported as the bug. Rendered proof: `EventDetailModal` opened from `eventMarker-seed-0001`, live `simctl io screenshot`. Group A therefore needs its own fix (`presentationBackground`/detent choice, or a non-`.sheet` construction), not a "don't touch."
2. **`.ignoresSafeArea(edges: .bottom)` as applied does not reach the bottom edge.** In all three Group-B files it is applied *inside* the `GeometryReader`, before an outer `.frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .bottom)`, so the card is positioned within the safe area and stops short of the screen edge.

## Pass/fail criteria — measurable, added at acceptance (L-009)

The spec asserted "full-width" and "flush to the bottom edge" with no falsifiable check, so every gate before acceptance had nothing objective to fail. These are the checks; each is a pixel measurement on a screenshot of the surface open, not a source read:

1. **Full width:** the card's surface colour is present at x = 0 and x = width−1 on any row inside the card. *Measured result at `passenger-code ddbc7de`: PASS for all 3 Group-B surfaces.*
2. **Flush bottom:** the card's surface colour is present on the screen's **last** pixel row. *Measured result: **FAIL** — `SearchOverlay` and `PlacesListOverlay` both stop 102px = **34pt** above the bottom edge (exactly the iPhone 17 home-indicator inset), with live map rendering underneath.*
3. **Top-corners-only:** the two bottom corners are square — surface colour reaches x = 0 and x = width−1 on the card's last row. *Measured result: PASS for Group B; **FAIL** for Group A (all four corners rounded, see Correction 1).*
4. **One shape app-wide:** criteria 1–3 give the same answer for a Group-A surface and a Group-B surface, captured in the same session. *Measured result: **FAIL** — the two groups render as visibly different shapes.*
5. **Bounded height — the map stays visible above every modal.** Criteria 1–4 measure the card's *edges* and say nothing about how tall it is, so all four can pass on a card that covers the whole screen. Added at the round-2 acceptance (`product`, 2026-08-07) after exactly that happened. The check: **the card's top edge sits at or below 40% of screen height, and the card contains no contiguous content-free band taller than ~25% of the card.** Measure the top edge by scanning the left-edge pixel column (x = 1) upward from the last row until the surface colour stops — not the centre column, which the nav row and buttons interrupt. *Measured result at `passenger-code 08a09fb`: PASS for `HoodSheet` (card top 45%), `SearchOverlay` (62%), `PlacesListOverlay`/`PassportSurface` (37%); **FAIL** for `EventDetailModal` and `PlaceDetailModal` — both render with the card top at **9% of screen height (80pt from the top of a 874pt screen)**, covering the map entirely, with roughly two-thirds of the card empty white.*

**How to measure the dead-band half of criterion 5 — added 2026-08-07 (`product`, `PAS-77` judgment call, L-009).** The criterion above stated a measurement procedure for the card's *top edge* and none at all for the *content-free band*, which is a large part of why a 60.2%-of-card band cleared code review at round 3 — the gate had a number to hit but no stated way to read it, so each reader read it differently. The procedure:

> For every pixel row inside the card (top edge → last screen row), mark the row **content** if any pixel anywhere across the card's full width differs from the surface colour by more than a small tolerance. The dead band is the **longest contiguous run of non-content rows**, expressed as a percentage of card height. Note this scan is full-width, unlike criterion 5's top-edge scan, which is deliberately left-edge-only (x = 1) — the two halves of this criterion use different scans on purpose, and using one for the other gives a wrong answer in both directions.
>
> Measure on the **sparsest content the shipped data can actually produce**, not on a representative case: for `HoodSheet`, a Hood with zero curated places and no `blurb` (41 of 44 hoods have zero places, 21 of those also have no blurb — see the verdict below); for `PlaceDetailModal`, a place opened with location permission declined, so `RouteControls` renders `EmptyView`; for `EventDetailModal`, the shortest row set `EventDetailRows.rows(for:)` emits. A "typical" case passing is not evidence — the criterion is about the short case by construction.

**Why this criterion has to exist:** under `.sheet()` + `.presentationDetents`, height was bounded by the detent, so no spec needed to state it. Dropping `.sheet()` (the round-2 fix) removed that bound, and each card's own `Spacer` then expanded it to fill the screen. A height rule that was previously enforced by the platform became nobody's, and no criterion caught it. Any future change that removes a platform-supplied constraint owes an explicit replacement for it in this list.

6. **Every modal is dismissable, and the spec says by which paths.** *Added at the round-3 acceptance (`product`, 2026-08-07, L-009) — not a new requirement, a previously unstated one.* The check: **with the surface open, each of these dismisses it — (a) a downward drag starting on the drag-handle strip, (b) the close (X) button, (c) a tap on the scrim outside the card — and each still works after the content has been scrolled.** Verify each path separately and after a scroll, not once on a fresh card; a path that works only before the user touches the content is a fail.

   **Known deviation, accepted for now, `EventDetailModal`/`PlaceDetailModal`/`HoodSheet`:** a downward drag starting *inside* the scrollable content does **not** dismiss — the `ScrollView` consumes the touch and the card-level `DragGesture` never fires (`qa`, measured live at `19861ab`, with control tests ruling out a bad test). This is **not** a criterion-6 failure as written above: all three required paths work, in every scroll state, with no jank and no accidental dismiss. It is recorded here as a deliberate scope line rather than left as tribal knowledge, because it is the kind of thing that gets rediscovered as a "bug" every few rounds. Whether the draggable zone *should* extend into content (e.g. `.simultaneousGesture` priority tuning) is a `designer` question, unfiled — raise it there, don't reopen it here.

   **Why this criterion has to exist** — the same reason as criterion 5, one axis over. Under `.sheet()`, drag-to-dismiss was supplied by the platform and no spec had to state it. Round 2 dropped `.sheet()`, replacing it with a hand-rolled `DragGesture`; round 3 then put a `ScrollView` inside that gesture's own territory. Two rounds of changes to how dismissal works, and no gate had a written bar to check dismissal against — which is why the interaction was only ever spot-checked, at QA, after the code had already cleared review. The Non-negotiables section's "drag-to-dismiss thresholds: unchanged" was doing the work of a requirement without being falsifiable enough to fail anything.

## Add to `design-principles.md` — so future modals default to this, not rediscover it

See `passenger-brain/design/design-principles.md` §8 (added by this pass) — the standard now lives there as the shared reference `ios-code-reviewer`/`designer` check future surfaces against, rather than re-derived per feature.

## Non-negotiables — confirmed

- Group A (`EventDetailModal`, `PlaceDetailModal`, `HoodSheet`): **zero code change** — already correct, don't touch.
- Presentation exclusivity (design-principles.md §6, unchanged by this pass): this fix is shape-only, doesn't change which surfaces can co-present or how `MapChromeState`/`DetailRouter` gate them.
- Drag-to-dismiss thresholds, scrim opacity, accessibility labels, `.accessibilityIdentifier`s on all 4 Group-B files: unchanged.
- `presentationDetents`/height logic already unified by `PAS-48`: untouched by this pass.

## Principles conformance

- Consistency (new §8, design-principles.md, this pass): one modal shape everywhere is the concrete rule this section header exists to state — no threshold to cite beyond "match Group A's own system-default shape," since that's what iOS itself already established as the platform convention.
- Thumb Zone, bottom third (§3): unaffected — these surfaces were already bottom-anchored in spirit; this fix makes the anchoring literal (flush) rather than approximate (gapped).
- Presentation exclusivity (§6): confirmed unaffected, see Non-negotiables above.

## What ios-developer needs to do

1. Confirm the project's deployment target supports `UnevenRoundedRectangle`; use the custom-`Shape` fallback if not.
2. Apply the Group-B fix (drop horizontal padding, drop bottom padding, top-corners-only radius, `.ignoresSafeArea(edges: .bottom)`) to `PlacesListOverlay.swift`, `PassportSurface.swift`, `SearchOverlay.swift`, and (if landed before the nav-row merge) `HeatModalCard.swift`.
3. Do **not** touch `EventDetailModal.swift`, `PlaceDetailModal.swift`, `HoodSheet.swift` — already correct.
4. Once buildable: build, run on simulator, screenshot each of the 4 fixed surfaces open, confirm (a) full device width edge-to-edge, (b) flush to the bottom safe-area edge, (c) top-corners-only radius, (d) `MapNavRow` still renders above and stays tap-able while a Group-B surface is open — none of which this pass could verify (no render evidence, see header).

## Round-3 fix — what's left after the round-2 acceptance REJECT (`product`, 2026-08-07)

Items 1–4 above are done and confirmed. One item remains, scoped exactly:

5. **Bound `EventDetailModal.swift`'s and `PlaceDetailModal.swift`'s card height**, the only two of the seven surfaces with no cap. Apply the same treatment `HoodSheet.swift` already received **in the same commit** (`passenger-code 08a09fb`) — a `ScrollView` around the content plus `.frame(maxHeight: 480)` — and use `HoodSheet`'s own comment as the rationale, verbatim: *"this card is now intrinsically sized, not detent-driven, so an uncapped list would make short Hoods and long Hoods produce very differently sized cards."* That reasoning applies identically to these two files and was simply not carried across to them. Note that each card's `Spacer(minLength: 0)` above the route button is what expands it to full height once the cap is absent — a cap alone fixes it; removing the `Spacer` instead would collapse the route button up against the content, which is not the intent. Re-verify against criterion 5.

**Item 5 — VERIFIED AND ACCEPTED at the round-3 acceptance (`product`, 2026-08-07, `passenger-code 19861ab`).** Re-measured first-hand rather than inherited from the round's own gates: own isolated worktree pinned to `19861ab`, own dedicated simulator (`t079-accept3`, iPhone 17 / iOS 26.5) and `-derivedDataPath`, throwaway XCUITest capturing full-screen screenshots, host-side pixel scan of the x = 1 left-edge column per criterion 5's own stated procedure — all artifacts deleted after. **Card top: 44.8% of screen height (391pt of 874pt) for both `EventDetailModal` and `PlaceDetailModal`**, against criterion 5's "at or below 40%" bar and `HoodSheet`'s 45% reference. The round-2 failure (9% / 80pt, card covering the map entirely) is gone; the map renders above the card on 118 of 118 sampled rows for both surfaces. Three independent measurements of this same commit now exist and agree on the verdict while differing in the second digit — `ios-developer` 45.2%, `qa` ~42.8%, this pass 44.8%. The spread is measurement method and text size, not instability: all three are far above the 40% bar and none is near 9%. **Criterion 5's top-edge half therefore passes; its dead-band half does not, and that is `PAS-77`/`T-082`'s open scope (Round-4 below), deliberately not folded into this item.**

## Round-4 — `PAS-77` judgment call: the fixed 480pt cap is **not** an accepted trade-off (`product`, 2026-08-07)

Round 3 landed the cap and cleared code review, and `ios-developer` correctly flagged what the cap bought: `ScrollView` + `.frame(maxHeight:)` claims the maximum under SwiftUI's sizing rules regardless of content height, so short content leaves a content-free band. Measured live at round 3: `EventDetailModal` **34.7%** of card, `PlaceDetailModal` **60.2%**. Both exceed criterion 5's ~25% bar. The question routed to `product`/`architect` was whether to accept that or fix it.

**Verdict: fix it. A content-measured cap is needed, across all three files** — `EventDetailModal.swift`, `PlaceDetailModal.swift`, `HoodSheet.swift`.

**1. This is not the edge case, it is the default — and the shipped data proves it.** Counted directly from `passenger-code/Passenger/Resources/places-tel-aviv.json` and `hoods-tel-aviv.json`: **9 curated places across 44 hoods.** The per-hood distribution is `{0 places: 41 hoods, 3 places: 3 hoods}` — `florentin`, `kerem-hateimanim`, `neve-tzedek` are the only populated ones. So **41 of 44 Hoods render `HoodSheet`'s `emptyState`** (an icon, one line of copy, and an "Explore another Hood" button, ~150pt with its `.padding(.vertical, 24)`) inside a 480pt box; **21 of those 41 also have no `blurb`**, so the entire card body is header + flag line + empty state. The 3 populated hoods carry 3 place rows each (~44pt apiece). There is **no Hood in shipped V1 whose content fills 480pt.** A defect that fires on 44 of 44 real data rows is not a trade-off, it's the shipped behavior.

**2. `PlaceDetailModal`'s 60.2% case is a first-run-normal state, not an exotic one.** It was measured with location permission declined, which makes `RouteControls` render `EmptyView` via its `.noOrigin` case. Passenger has no onboarding by strategy — the app opens to the map plus the permission prompt — so "permission not yet granted" is the state every single user is in on first open, and the state anyone who declines stays in permanently. The worst measurement of the three is on the most-travelled path.

**3. Shipping as-is would mean silently relaxing criterion 5 rather than editing it.** Criterion 5 was written into this file at the round-2 acceptance the same day, precisely because a height rule the platform used to enforce had become nobody's. Accepting a 60.2% band while leaving "~25%" on the page reintroduces exactly that gap — a written bar that the shipped build doesn't meet and no gate fails it on. If a fixed cap were the right answer, the honest action would be to change the number in criterion 5, and it isn't defensible to: Passenger's one differentiator is the live map, and this spends 290pt of it on empty white for a card carrying ~190pt of content.

**`HoodSheet` — checked, shares the defect, and is the worst of the three by frequency.** Its `card` is the same construction byte-for-byte (`ScrollView { ... }.frame(maxHeight: 480)`, `HoodSheet.swift` lines 85–102); the greedy-`ScrollView` mechanism is already empirically proven on that exact shape by round 3's pixel scan of the other two files; and item 1 above shows its content is short for every Hood in the dataset. **Disclosed limitation:** this is a source-plus-data determination, not a render — I did not build or pixel-measure `HoodSheet` (`EventDetailModal.swift`/`PlaceDetailModal.swift` carry another session's uncommitted WIP in the shared tree, and a screenshot could not have changed a verdict the data already settles). The percentage is `qa`'s to measure against the procedure above; the presence of the defect does not depend on it.

**Mechanism — `architect`'s call, not decided here.** `PAS-77` requirement 1 names `GeometryReader` + `PreferenceKey` reading intrinsic height and clamping to 480. That works, but it writes a layout result into `@State` during layout, which is the usual source of "Modifying state during view update" warnings and size oscillation, and it has to be built so the outer `DragGesture` and `.transition(.move(edge: .bottom))` don't re-trigger measurement every frame. A second candidate worth weighing first because it needs no state and no measurement at all:

```swift
ViewThatFits(in: .vertical) {
    content                 // intrinsic height — used whenever it fits in 480
    ScrollView { content }  // fallback — used only when content exceeds 480
}
.frame(maxHeight: 480)
```

This degrades to exactly today's behavior above 480pt and shrinks to fit below it. **`architect` picks between the two (or a third) and writes the call into the fix's scope** — `product` is not making a SwiftUI layout-mechanism decision, and neither candidate should be implemented on this document's say-so.

### Round-4 mechanism decision (`architect`, 2026-08-07) — neither candidate; use a non-greedy clamp

**Decision: replace `.frame(maxHeight: 480)` with `.frame(maxHeight: 480).fixedSize(horizontal: false, vertical: true)` on the existing `ScrollView`, in all three files. No `GeometryReader`, no `PreferenceKey`, no `@State`, no `ViewThatFits`.** One modifier added per file; the `ScrollView` and the 480 constant stay exactly as they are.

**Both candidates on the table were rejected on measured evidence, not preference.** Measured with a SwiftUI layout harness (`NSHostingController.sizeThatFits`, same layout engine, proposal 393×850 — the bottom-aligned `ZStack` case), sweeping content heights of 150 / 300 / 600 / 900pt:

| construction | 150 | 300 | 600 | 900 |
|---|---|---|---|---|
| `ScrollView{c}.frame(maxHeight: 480)` — today | 480 | 480 | 480 | 480 |
| `ViewThatFits{c; ScrollView{c}}.frame(maxHeight: 480)` — the sketch above | **480** | **480** | **480** | 480 |
| `ViewThatFits{c; ScrollView{c}.frame(maxHeight: 480)}` — clamp moved inside | 150 | 300 | **600** | 480 |
| `ScrollView{c}.frame(maxHeight: 480).fixedSize(horizontal: false, vertical: true)` | **150** | **300** | **480** | **480** |

1. **The `ViewThatFits` sketch as written in this document does not fix anything** — it measures 480pt at every content height, identical to today. The reason is that **`.frame(maxHeight:)` is itself greedy**, which this document's round-3 diagnosis missed by attributing the defect to `ScrollView` alone: a bare 150pt block under `.frame(maxHeight: 480)` measures 480. So the outer clamp re-inflates whatever `ViewThatFits` returns, and the branch choice is irrelevant. Had this been built verbatim, the dead band would have been unchanged and only a render would have caught it.
2. **`ViewThatFits` with the clamp moved inside the fallback branch still leaves a hole in the 481–850pt range** (row 3: 600pt content renders at 600pt). `ViewThatFits` runs its fit test against the *proposed* height — the full screen, ~850pt — not against 480, so content taller than the ceiling but shorter than the screen is judged to "fit" and renders un-scrolled at full height. That is the `PAS-73` defect (card eats the map) reintroduced through the fix for `PAS-77`. No shipped Hood hits this today, but nothing in the mechanism prevents it, and a fuller dataset (`T-075`) is exactly what would.
3. **`GeometryReader` + `PreferenceKey` is rejected as unnecessary, not as unworkable.** Its costs are real (a layout result written into `@State` during layout, re-measurement pressure from the outer `DragGesture` and `.transition`), and there is no reason to pay them for an effect one stateless modifier produces.

**Why the clamp works:** both `ScrollView` and `.frame(maxHeight:)` are greedy *under a concrete proposal* — each takes everything offered. `.fixedSize(horizontal: false, vertical: true)` removes the concrete vertical proposal, so the frame clamps an *ideal* height instead of inflating a proposed one. `horizontal: false` leaves the width proposal intact, so text wrapping and full-width layout are unaffected.

**Verified, and the limit of what was verified.** The table above is a real SwiftUI layout measurement, not reasoning. A view-hierarchy dump at 900pt content confirms the clamped `ScrollView` is structurally identical to today's — `HostingScrollView` 480pt with a real 480pt clip view, *not* a 900pt view clipped by a frame — so `.fixedSize` does not collapse it into a static block. **Disclosed: this is macOS AppKit hosting, and it measures sizing, not gesture behavior.** That the clamped `ScrollView` still *scrolls* on iOS at long content is the one claim not proven here and is a required build-time check (below).

**Interaction with the drag gesture and the transition — better than today, not worse.** Both live outside the card's content (`.offset(y:)` and `.move(edge: .bottom)` translate the card, they don't re-propose its size), so neither re-triggers measurement; there is no measurement to re-trigger. On short content the card is now shorter than the scroll threshold, so the `ScrollView` has nothing to scroll and the outer `DragGesture` gets the touch cleanly — which addresses the drag-vs-scroll spot-check `ios-code-reviewer` left for `qa` at round 3, on the 41-of-44 path.

**`Spacer(minLength: 0)`** (`EventDetailModal.swift:82`, `PlaceDetailModal.swift:93`) is **inert** under this mechanism — measured: a card with and without it both report 190pt at 150pt content, because a nil proposal reduces a `Spacer` to its `minLength`. Removing it is optional cleanup, not part of the fix. It is worth removing anyway, as it is the one thing that would silently re-inflate these cards if anyone later drops the `.fixedSize`.

#### Build scope for `ios-developer` [iOS]

All three files get the **same one-line change**, and nothing else. `HoodSheet` does **not** need different treatment — its "existing fix" is the same greedy `.frame(maxHeight: 480)` as the other two (`HoodSheet.swift:102`), so it has a cap but no shrink, exactly like them. Three identical edits, one commit.

1. `Detail/EventDetailModal.swift:92` — `.frame(maxHeight: 480)` → `.frame(maxHeight: 480)` + `.fixedSize(horizontal: false, vertical: true)`
2. `Detail/PlaceDetailModal.swift:104` — same
3. `Detail/HoodSheet.swift:102` — same

Extract the constant if you prefer (`private static let maxCardHeight: CGFloat = 480`), but do not change its value — the 480 ceiling is settled in `PAS-73`. Update each site's existing comment to say the cap is now a ceiling rather than a fixed height. Optional, same commit: delete the two dead `Spacer(minLength: 0)` lines. Nothing else in these files changes — not the `ScrollView`, not the `ZStack`/scrim, not the `DragGesture`, not the `.transition`, not the background shape.

**Required verification (the sizing claim is proven; these two are not).** Both are renders on the *sparsest* case each surface can produce, per `product`'s round-4 note — a "typical" case passing is not evidence:
- **Shrink:** card height at short content is measurably less than 480pt, and the dead band is under criterion 5's ~25% bar, measured by the procedure above. Sparsest cases: a Hood with no places and no blurb (41 of 44 qualify; 21 have no blurb); a place with location permission declined; the shortest `EventDetailRows` set.
- **Scroll, at long content — this is the one that can actually fail.** Force content past 480pt and confirm the card caps at 480pt **and still scrolls to its last row**. Pass condition: the final row/button is reachable by scrolling and not merely clipped. A build that shrinks correctly but clips instead of scrolling is a regression worse than the defect being fixed, and no existing test covers it.

**Out of scope, explicitly:** the 480pt ceiling itself and the round-2 decision to drop the `.medium` detent both stay as settled in `PAS-73`. This changes only whether the card is *allowed to be shorter* than the ceiling.

**Not filed as a defect but noted for `T-075`'s thread:** the 9-places-across-44-hoods count above is itself a content-coverage gap, and it is the same scarcity `T-075`/`PAS-71` already has open with Aviran (curated places per Hood). No new task filed — flagging that the modal-shape symptom and the curation-coverage question share a root cause, and that a fuller dataset would shrink but not remove this defect (`HoodSheet` would still be short for any Hood under ~7 places).
