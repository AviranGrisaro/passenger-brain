# Nav bar icons — bigger, colored, unique (T-064 / PAS-60)

**Type:** post-ship redesign pass (no PRD/TRD — visual-treatment change to already-shipped chrome, per `BOARD.md`'s retired-design-gate lifecycle, same shape as T-062/T-063).
**Trigger:** founder-direct, live chief-of-staff chat, 2026-08-04. Verbatim request and chief-of-staff's read of it: `passenger-brain/agent-os/PROGRESS.md`, 2026-08-04 "L-002 stub: founder-direct request, nav bar icons" entry.
**Target files:** `passenger-code/Passenger/Map/HeatButton.swift`, `SearchButton.swift`, `ProfileButton.swift`, `NearMeButton.swift`, `PlacesButton.swift` (`MapNavRow.swift` itself is untouched — this is per-button chrome only, not row layout/logic).
**No render evidence.** The disk-space HALT (`BOARD.md` top) blocks `xcodebuild`/simulator work, so nothing below has been seen rendered on device or simulator — this is a spec for `ios-developer` to implement and for QA/Aviran to eyeball once the HALT lifts, not a verified-in-app result (per L-036: a visual change never rendered is not "done").

## What's wrong today

All 5 buttons share identical chrome: `Image(systemName:...)`, `.font(.title3)` (~20pt regular), `44×44` frame, `.thinMaterial` circle, default `.primary` foreground (`.secondary` only on `NearMeButton`'s disabled state). Nothing distinguishes one button from another except the glyph shape itself — no size emphasis, no color, no per-function identity. That's the literal gap Aviran named: not bigger, not colored, not unique.

## The fix

### 1. Bigger — exact sizes
- Frame: **44×44 → 52×52pt** (+18% linear, +39% area). Stays a fixed frame size, not just a bigger glyph in the same box — this is what actually reads as "bigger" from arm's length.
- Glyph: `.font(.title3)` (~20pt regular) → **`.font(.system(size: 24, weight: .semibold))`** (24pt, semibold). The weight jump matters as much as the +4pt — semibold reads noticeably bolder/bigger even before the point-size delta.
- Hit region floor (design-principles.md §2, Fitts's Law): 44×44 is the accessibility minimum, not a target — 52×52 clears it with margin, nothing shrinks below it.
- Row-width check (arithmetic only, not simulator-verified — HALT in effect): `HStack(spacing: 16)` unchanged → row width `5×52 + 4×16 = 324pt`, up from `284pt`. On the narrowest current device (iPhone SE, 375pt width), that leaves ~25pt margin per side with the row horizontally centered and no other padding applied (confirmed by reading `MapScreen.swift`'s `.padding(.bottom, 32)` on the row — no horizontal padding today). Flag for `ios-developer`/QA to confirm on-device once buildable; if it's tighter than expected in practice, the fix is dropping `HStack` spacing to 12, not shrinking the buttons back down.

### 2. Colored — one accent color per icon, using SwiftUI system colors
Per-icon accent, not a shared palette — each button already maps to a distinct function (heat / search / profile / recenter / places), so a distinct hue per button reinforces that distinction rather than being arbitrary decoration (visual hierarchy is "size + weight + color together," design-principles.md §2).

Using SwiftUI's built-in system `Color` cases rather than hand-picked hex: they carry Apple's own light/dark-mode and Increase-Contrast adaptation for free (design-principles.md §3: "Author... each with light+dark variants" / "Use system label/background colors; they already temper"), so nothing needs a new asset-catalog entry.

| Button | Glyph (unchanged) | Color | SwiftUI | Approx. hex (light) |
|---|---|---|---|---|
| `HeatButton` | `flame.fill` | Orange-red | `Color.orange` | `#FF9500` |
| `SearchButton` | `magnifyingglass` | Blue | `Color.blue` | `#007AFF` |
| `ProfileButton` | `person.fill` | Purple | `Color.purple` | `#AF52DE` |
| `NearMeButton` (active) | `location.fill` | Green | `Color.green` | `#34C759` |
| `NearMeButton` (denied) | `location.slash.fill` | Gray | `Color.gray` | `#8E8E93` |
| `PlacesButton` | `list.bullet` | Pink | `Color.pink` | `#FF2D55` |

Five hues, evenly spread around the wheel (orange ~30°, blue ~211°, purple ~280°, green ~142°, pink ~347°) — no two adjacent buttons read as the same color at a glance. `NearMeButton` keeps its existing denied/active swap (glyph + color both change, same pattern as today's `.secondary`/`.primary` swap — color-blind users still get the icon-shape change per design-principles.md §3's "never rely on color alone").

**Contrast — estimated, not measured.** Design-principles.md §5 requires 3:1 for UI components. System `Color` values are Apple-vetted for legibility against system materials in both appearances, and `.thinMaterial` bounds how much arbitrary map content shows through — but I can't render the actual composite (HALT), so this is a reasoned estimate, not a computed ratio. Flag for QA to eyeball once buildable, especially `Color.pink`/`Color.orange` against a bright map background in light mode.

### 3. Unique — SF Symbols kept, restyled (not a custom icon set)
Per the dispatch's own check ("would Aviran recognize this as bigger/colored/unique") — a new custom glyph system is more than this ask needs. The restyle:
- **Colored stroke ring** around the existing `.thinMaterial` circle: `Circle().strokeBorder(<button's color>, lineWidth: 1.5)`, opacity 0.9. This is what makes each button read as a distinct "chip" even in peripheral vision, not just on close inspection of the glyph — the ring is visible before the eye resolves which symbol is inside it.
- Glyph itself rendered in the same accent color at full opacity (see §1 for size/weight).
- `.thinMaterial` circle fill is **unchanged** (requirement #4) — frosted-glass legibility over arbitrary live map content stays; the ring and glyph color sit on top of it, they don't replace it.

Net per-button treatment (example, `HeatButton`):
```swift
Image(systemName: "flame.fill")
    .font(.system(size: 24, weight: .semibold))
    .foregroundStyle(Color.orange)
    .frame(width: 52, height: 52)
    .background(.thinMaterial, in: Circle())
    .overlay(Circle().strokeBorder(Color.orange.opacity(0.9), lineWidth: 1.5))
```
Same shape for all 5, swapping only the `systemName` (unchanged) and the color per the table above. `NearMeButton` additionally keeps its `isDenied` branch driving glyph name + color (green↔gray) exactly as it does today for `.primary`/`.secondary`.

## Non-negotiables — confirmed untouched
- **Glyph→button mapping**: unchanged (`flame.fill`, `magnifyingglass`, `person.fill`, `location.fill`/`location.slash.fill`, `list.bullet`). No swap proposed.
- **`isPresented`/`.isSelected` accessibility pattern**: unchanged — this spec only touches `.font`, `.foregroundStyle`, `.frame`, and adds a `.overlay(Circle().strokeBorder(...))`; none of the `.accessibilityAddTraits(isPresented ? [.isSelected] : [])` lines are touched.
- **`accessibilityLabel` text**: unchanged on all 5 buttons ("Heat", "Search", "Profile", "Near me"/"Near me, location off", "Places").
- **Row z-order/fade behavior** (`MapNavRow.swift`'s header comment — always-visible, always-hit-testable, never faded): `MapNavRow.swift` itself is not edited by this spec at all — only the 5 button files' internal `body` styling.

## Principles conformance
- Fitts's Law, ≥44pt targets (design-principles.md §2): 52×52 frame clears the floor.
- Visual hierarchy, "size + weight + color together" (§2): all three levers used together, not color alone.
- Never rely on color alone (§3): `NearMeButton`'s denied state still swaps the glyph shape (`location.slash.fill`), color is a second channel, not the only one.
- System label/background colors, light+dark variants "for free" (§3): system `Color` cases chosen over hardcoded hex for exactly this reason.
- Accessibility contrast 3:1 for UI components (§5): estimated, not measured — flagged above as needing on-device confirmation once the HALT lifts.

## What ios-developer needs to do
Apply the block above (adjusted per-button color/glyph per the table) to all 5 files. No new files, no new assets, no `MapNavRow.swift` change. Once the disk-space HALT lifts: build, run on simulator, screenshot the row, and confirm (a) all 5 render distinctly, (b) the 324pt row width doesn't clip on iPhone SE, (c) contrast reads acceptably in both light and dark mode over live map content — none of which this pass could verify.
