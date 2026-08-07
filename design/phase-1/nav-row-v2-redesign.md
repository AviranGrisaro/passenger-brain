# Nav row v2 — merge search/heat, relocate locate-me, bookmark icon, cohesive palette (T-078 / `PAS-60` reopened)

**Type:** post-ship redesign pass (no PRD/TRD — this is a second pass over already-shipped chrome, same lifecycle as `PAS-60`'s first pass: `passenger-brain/design/phase-1/nav-bar-icons-redesign.md`).
**Trigger:** founder-direct, live chief-of-staff chat, 2026-08-07. Verbatim request + chief-of-staff's read: `passenger-brain/agent-os/PROGRESS.md`'s 2026-08-07 "L-002 stub" entry. This is Aviran's live review of `PAS-60`'s shipped result — reject-with-findings, routed back to `design`, not a fresh unrelated ask.
**No render evidence.** This pass is a source read + spec, not a simulator run — same disclosed limitation `PAS-60`'s own spec carried (that one cited a disk-space HALT; this run simply has no build/simulator tool access delegated to it). Per `passenger-code/CLAUDE.md`'s L-036 rule, a visual change never rendered is not "done" — that responsibility sits with whoever next builds and confirms this on-device (`ios-developer`/`qa`), not with this spec.
**Target files:** `passenger-code/Passenger/Map/{MapNavRow,SearchButton,ProfileButton,NearMeButton,PlacesButton,HeatButton,MapScreen,MapChromeState}.swift`, `passenger-code/Passenger/SearchSheet/SearchOverlay.swift`, `passenger-code/Passenger/HeatModal/HeatModalCard.swift`. Exact file names for chrome state (`MapChromeState`/`NavSurface`) inferred from `MapNavRow.swift`'s and `MapScreen.swift`'s doc comments (`chrome.presented`, `NavSurface?`) — `ios-developer` should confirm the literal type/file location before editing, it wasn't opened directly this pass.

## What's wrong today (read directly from shipped code)

Read `passenger-code/Passenger/Map/MapNavRow.swift`, its 5 button files, and `MapScreen.swift`'s nav-row wiring (lines ~514-531). Confirmed against source, not against the `PAS-60` spec's intent:

1. **5 buttons, 5 unrelated hues** — `HeatButton` orange, `SearchButton` blue, `ProfileButton` purple, `NearMeButton` green/gray, `PlacesButton` pink. Evenly spread around the color wheel was the explicit goal last pass (`nav-bar-icons-redesign.md` §2) — which is exactly what reads as "clashing" once seen live: five saturated, unrelated hues sitting permanently on screen is decoration competing for attention, not hierarchy (design-principles.md §2, Von Restorff: "only one special element per view" — this row has five).
2. **Heat and Search are two separate entry points** for what a user experiences as one "what's on the map / when" decision — `HeatButton` opens `HeatModalCard` (hour slider), `SearchButton` opens `SearchOverlay` (text + category search). Two buttons for two related but overlapping mental tasks.
3. **`NearMeButton` sits in the bottom nav row**, not top-right — `flame.fill`... `location.fill`/`location.slash.fill` at 52×52 alongside Search/Profile/Places, all in `MapNavRow`'s single `HStack`.
4. **`PlacesButton` uses `list.bullet`** — a generic list glyph, not a save/bookmark glyph, despite the button's own function being "your saved places." `PlaceDetailModal.swift`'s own `saveButton` (line 62-75) already uses `bookmark`/`bookmark.fill` for the per-place save action — the nav-row entry point to that same saved list uses an unrelated icon, so the "save" concept has two different glyphs in the same app today.

## 1. Merge Heat into Search — one button, `SearchOverlay` gains a segment

**The call:** `SearchButton` stays the nav-row entry point (accessibility label unchanged: `"Search"`). `HeatButton` is deleted from `MapNavRow` entirely — 3 buttons remain in the row: Search, Profile, Places. Tapping Search opens `SearchOverlay` as it does today; `SearchOverlay` gains a top segmented control, **`Picker("", selection: $segment) { Text("Search").tag(.search); Text("Hour").tag(.hour) }.pickerStyle(.segmented)`**, placed between `dragHandle` and `header`, defaulting to `.search`. Selecting `.hour` swaps `CategoryChipRow` + `resultsArea` for `HeatModalCard`'s existing content (`HourReadout` + `HourSlider`, read `HeatModalCard.swift` lines 155-162) — reused as a private subview, not duplicated. `HeatModalCard.swift` and `HeatButton.swift` are deleted once the content moves; `MapChromeState`'s `NavSurface` (or equivalent enum — see file-map note above) loses its `.heat` case, since there is no longer an independent heat-presented state — `chrome.presented == .search` now covers both segments.

**[ASSUMPTION]** the mechanism (single button, in-surface segmented control) is this spec's call, not Aviran's literal words — he said "fold that function into search," not how. Rejected alternatives, with reasoning:
- *Long-press for heat, tap for search* — fails Poka-Yoke/discoverability (design-principles.md §2 "error prevention... constrain at the control," §1 Functional-before-Pleasurable): a hidden gesture is not a control a first-time user can find.
- *Heat opens automatically as part of every search* — conflates two genuinely different tasks (find a place vs. change the time window) into one screen with no way to reach one without the other's UI in view.
- **Chosen: visible segmented control, default to Search** (search is the higher-frequency action — finding a place — per the existing UI's own primacy; Hour is a secondary, still one tap away, never hidden). This keeps Hick's Law's option count sane (2 segments, well under the 3–5 guideline) and satisfies "fold into search" literally: one entry point, one surface, function still reachable in full.

**Edge-drag hour gesture is untouched.** `MapScreen.swift`'s `EdgeHourZone`/`EdgeHourTrack` (z2/z6, lines ~431-441) is a separate swipe-the-map-edge mechanism for nudging the hour and is not part of this button merge — it stays as the fast/ambient path, the Search→Hour segment becomes the deliberate/precise path (same "fast nudge vs. precise picker" pairing the app already has elsewhere, not a new pattern).

**Accessibility, stated explicitly (non-negotiable per dispatch brief):** `SearchButton`'s `accessibilityLabel("Search")` and `.isSelected` trait pattern (unchanged, driven by `chrome.presented == .search`) carry over unmodified. `HeatButton`'s own `"Heat"` label and its re-tap-to-dismiss test (`HeatButtonInteractionTests.testTappingHeatButtonAgainDismissesTheModal`, cited in `MapNavRow.swift`'s header comment) **do not survive** — this is a deliberate, disclosed removal (the button itself is gone), not silent breakage. `ios-developer` needs to either delete or retarget that test at the new segmented control's own dismiss behavior (re-tapping Search while `.search` is presented, in either segment, should still dismiss — same as every other nav-row button's existing pattern).

## 2. NearMe → top-right, Apple/Google-Maps-style floating button

**Placement:** `MapScreen.swift` already has an `.overlay(alignment: .topTrailing)` (line 386-391) rendering `CachedDataIndicator()` conditionally, with `.padding()` (system default, 16pt). `NearMeButton` moves into this same overlay, stacked above/beside `CachedDataIndicator` — both are top-trailing chrome and need to coexist: `VStack(alignment: .trailing, spacing: 8) { NearMeButton(...); if densityStore.source == .cache { CachedDataIndicator() } }`, keeping the existing `.padding()`. `NearMeButton` is removed from `MapNavRow`'s `HStack` (3 buttons remain: Search, Profile, Places) and from `MapNavRow`'s parameter list (`nearMeAuthorizationStatus`, `onNearMeTap` move to `MapScreen`'s new top-trailing overlay call site instead).

**Style — reference-app convention, adapted:** Apple Maps and Google Maps both use a circular floating "locate me" control, ~34-44pt, opaque or lightly-materialed white/gray circle, target-outline or filled-arrow glyph, gray/black by default and switching to the app's accent blue only while actively tracking the user's location. Passenger's version:
- Frame: **44×44** (not 52×52 — this is a secondary, single-purpose utility control, not one of the 3 primary nav-row actions; Fitts's Law floor is met, no reason to inflate it to nav-row prominence, which would fight for attention with the actual 3-button row per Von Restorff).
- `.thinMaterial` circle background (unchanged from today — matches the rest of the app's floating-chrome idiom, `CachedDataIndicator`'s neighbor).
- Glyph: `location.fill` (active/authorized) / `location.slash.fill` (denied) — **unchanged**, already matches the reference-app convention of an arrow/target glyph swapping to a "slash"/disabled state.
- Color: `.secondary` (gray) by default and when denied, **`Color.blue`** only while `authorizationStatus == .authorizedWhenInUse || .authorizedAlways`(active/tracking) — this replaces the old green/gray pair. Blue is chosen deliberately to match this spec's new cohesive nav-row family (§4 below), so NearMe reads as part of the same app rather than a 4th unrelated hue, while still being visually distinct from the nav row by virtue of position (top-right vs. bottom) and size (44 vs. 52).
- No colored stroke ring (§4 below explains why the ring treatment is dropped for the nav row too) — a plain `.thinMaterial` circle, consistent with `CachedDataIndicator`'s own existing chrome-below-it.

**Accessibility label unchanged**: `"Near me"` / `"Near me, location off"`.

**[ASSUMPTION]** exact vertical offset from `ColdOpenTitle`'s top overlay (line 381-385, `.padding(.top, 56)`) — not measured on-device. `ios-developer` should confirm the top-trailing `VStack` doesn't visually collide with `ColdOpenTitle`'s fade-in text at cold open; if it does, drop `NearMeButton`'s appearance in from `.opacity(0)` until `ColdOpenTitle`'s own fade completes (mirroring the pattern `ColdOpenTitle(onFadeComplete:)` already exposes), rather than hard-coding a magic offset.

## 3. PlacesButton → bookmark glyph

`list.bullet` → **`bookmark.fill`**, matching `PlaceDetailModal.swift`'s own per-place save button exactly (line 70: `isSaved ? "bookmark.fill" : "bookmark"`). The nav-row button itself has no "saved" binary state of its own (it's a static entry point into the list, not a toggle), so it uses the filled variant permanently — `bookmark.fill`, not a state-driven swap — reading as "your bookmarks," the standard convention (Safari Reading List, Apple News, Apple Maps' own "Saved Places" tab all use `bookmark`/`bookmark.fill` for a saved-items list entry point). Accessibility label unchanged (`"Places"`).

## 4. Cohesive palette for the 3 remaining nav-row buttons + NearMe

**Why the old palette clashed, structurally, not just by hue choice:** 5 unrelated system colors spread evenly around the wheel is decoration, not signal — nothing in the app *needs* Heat to be orange and Profile to be purple; the color carried no information the icon shape didn't already carry (§3's own "never rely on color alone" principle, restated the other way: color that carries no extra information is just noise). **Mobbin was queried for shipped-app reference and returned "requires a paid plan" (Starter-plan limit, same shape as this repo's now-familiar Figma-connector limit) — this palette is reasoned from Apple's own Human Interface Guidelines color system and directly-observed reference-app convention (Apple Maps' own locate-me blue), not from a Mobbin pattern break-down. Flagged per designer.md's standing instruction: proceed rather than block, note unavailability.**

**New palette — one analogous family, not five arbitrary hues:**

| Button | Glyph | Color | SwiftUI | Approx. hex (light) |
|---|---|---|---|---|
| `SearchButton` (Search + Hour) | `magnifyingglass` | Blue | `Color.blue` | `#007AFF` |
| `ProfileButton` | `person.fill` | Indigo | `Color.indigo` | `#5856D6` |
| `PlacesButton` | `bookmark.fill` | Teal | `Color.teal` | `#30B0C7` |
| `NearMeButton` (top-right, active) | `location.fill` | Blue (matches Search) | `Color.blue` | `#007AFF` |
| `NearMeButton` (top-right, default/denied) | `location.fill`/`location.slash.fill` | Gray | `Color.secondary` | system-adaptive |

Blue → indigo → teal is one **analogous family** (hues ~211°, ~243°, ~193° — all within ~50° of each other on the wheel), read together as "one app's color system," not "five random accents." `NearMeButton` reusing the same blue when active ties it back into the same family rather than adding a 4th unrelated hue, while its top-right position and smaller 44pt frame already differentiate it from the 3-button row (position + size carry that distinction, not a unique hue — consistent with "size + weight + color **together**," design-principles.md §2, not color alone).

**Ring treatment dropped.** `PAS-60`'s spec added a `Circle().strokeBorder(<color>, lineWidth: 1.5)` per button. With 3 buttons in a tighter, less saturated family, the ring becomes redundant (the glyph + background color pairing already reads as a distinct chip) and starts to look like a fourth visual layer competing with the segmented-control redesign inside Search. Dropped for all 4 buttons (nav row + NearMe) — plain `.thinMaterial` circle, glyph in its accent color, no stroke overlay. This is a real simplification, not an oversight: fewer visual layers per button now that there are 3 buttons instead of 5.

**Contrast — estimated, not measured** (same disclosed limitation as `PAS-60`'s own spec): `Color.blue`/`.indigo`/`.teal` are Apple-vetted system colors with light/dark variants; `.thinMaterial` bounds how much map content shows through. Flag for `qa`/`ios-code-reviewer` to confirm ≥3:1 (design-principles.md §5) once buildable, particularly `Color.teal` against a bright sky-blue map region in light mode — the one pairing in this palette with the least hue separation from typical map content.

## Non-negotiables — confirmed

- **Touch targets:** 52×52 for the 3 nav-row buttons (unchanged from `PAS-60`, clears the 44pt Fitts's Law floor with margin), 44×44 for `NearMeButton` (still exactly at the floor, not below it).
- **`isPresented`/`.isSelected` pattern:** unchanged for Search/Profile; Places never had it (static entry point, unchanged). Search's `.isSelected` now covers both its segments (still driven by `chrome.presented == .search`).
- **`accessibilityLabel`s:** `"Search"`, `"Profile"`, `"Places"`, `"Near me"`/`"Near me, location off"` all unchanged. `"Heat"` is deliberately removed (§1) — the control it labeled no longer exists as an independent button.
- **`MapNavRow`'s z-order/fade rule** (header comment: always visible, always hit-testable, never faded): untouched — the row still renders last among `MapScreen`'s overlays, just with 3 children instead of 5. `NearMeButton`'s new top-trailing home does **not** need to obey that same always-visible rule by default (it wasn't specified either way) — **[ASSUMPTION]**: keep it always-visible too, matching its own current behavior (it was never gated on any `NavSurface` state before this move), just relocated.

## Principles conformance

- Von Restorff / one thing stands out (design-principles.md §2): 5 unrelated hues → 3 nav-row hues in one analogous family + NearMe reusing one of them, positioned and sized to differentiate itself without a 4th color.
- Hick's Law, 3–5 options (§2): SearchOverlay's new segmented control is 2 segments, well inside the range; the nav row itself drops from 5 choices to 3.
- Never rely on color alone (§3): every button still carries a distinct glyph shape; NearMe's active/inactive state still swaps glyph (`location.fill`/`location.slash.fill`) in addition to color.
- System label/background colors, light+dark "for free" (§3): all colors are system `Color` cases, no hardcoded hex.
- Fitts's Law ≥44pt (§2): 52×52 nav-row / 44×44 NearMe, both clear the floor.
- Accessibility contrast 3:1 (§5): estimated, not measured — flagged above for `qa`/`ios-code-reviewer` confirmation once buildable.

## What ios-developer needs to do

1. Delete `HeatButton.swift`; fold `HeatModalCard.swift`'s `HourReadout`/`HourSlider` content into a new `.hour` segment inside `SearchOverlay.swift`; remove the `.heat` case from `MapChromeState`'s `NavSurface` (or equivalent — confirm exact type first) and its wiring in `MapScreen.swift`.
2. Update `SearchButton.swift`, `ProfileButton.swift`, `PlacesButton.swift` per §3/§4 above (glyph swap on Places only; color + drop the stroke ring on all three).
3. Move `NearMeButton` out of `MapNavRow.swift` into `MapScreen.swift`'s existing `.overlay(alignment: .topTrailing)` (line 386), stacked with `CachedDataIndicator`; restyle per §2 (44×44, gray/blue swap, no ring).
4. Update `MapNavRow.swift`'s `HStack` to 3 children and its `init` parameters to match (drop `nearMeAuthorizationStatus`/`onNearMeTap`).
5. Once buildable: build, run on simulator, screenshot both the nav row and the top-right corner, confirm (a) no visual collision with `ColdOpenTitle`/`CachedDataIndicator`, (b) the Search/Hour segmented control is reachable and both segments render their full content without clipping, (c) contrast reads acceptably in both light and dark mode over live map content — none of which this pass could verify (no render evidence, see header).
