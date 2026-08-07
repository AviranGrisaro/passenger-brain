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
