# Passenger V1 — mockup & flow prompts

Paste-ready prompts for generating visual mockups from `design/ux-flows.md` (artifact: *Passenger — V1 UX Flows*).

**How to use**
- **Claude (artifact / design):** paste **Block A** (context), then one **Screen prompt**. Ask for an HTML artifact rendering iPhone-sized frames. For a full set in one go, paste Block A + "Generate S1–S11 as one scrollable board, 3 frames per row."
- **Figma:** paste Block A + a screen prompt, and say "build this in Figma" — the `figma-generate-design` skill + `use_figma` handle the write.
- **Flow diagrams:** use **Block C** with `generate_diagram` (FigJam/Mermaid).

---

## Block A — context (always paste first)

```
You are designing mockups for Passenger, an iOS app. Ground truth below — do not invent
features, do not add a tab bar, do not add a feed, profile, or onboarding carousel.

PRODUCT IN ONE LINE
One map of Tel Aviv, right now: how packed everywhere is (heat) and whether each place
feels local or touristy (tag). Nothing to scroll. Every screen is either the map, or
something the map handed you.

THE TWO LAYERS (the entire V1 map)
- HEAT — crowd density. Stepped bands, NO gradients. Time-variant: driven by the slider.
  Renders as FILL.
- TAG — localness. Three plain-language values: Local / Mix / Tourist. NOT time-variant.
  Renders as the ZONE OUTLINE STROKE, never as a badge, never blended with heat.
  Mix renders NOTHING — no stroke, no label, at any zoom. A blank zone reads as Mix.
  A zone with no data yet also renders blank, identically.
  BUSY + TOURIST = one distinct warning stroke that REPLACES the plain Tourist stroke.
  Never two decorations stacked. Busy + Local never gets a warning.

ZOOM LEVELS
- City-wide: heat as neighborhood-scale blobs. Stroke on LOCAL zones only. No labels, no pins.
- Neighborhood: zone boundaries visible, heat as zone-level stepped fill. Stroke on Local
  OR Tourist. Word label at zone centroid — the only zoom where the word appears. No pins.
- Close: spot pins appear. Zone stroke persists, no label. PINS CARRY NO TAG SIGNAL AT ALL —
  they mark location + category only, plus a ring accent if the place is in the user's
  Places list (binary: yours or not).

PERSISTENT MAP CHROME (never dismissed)
map · heat · tag · fading "Tel Aviv, right now" title (cold open only, ~2s in and out) ·
time slider (now → +12h, thumb in the bottom third, always visible) · near-me button ·
search icon · Places icon. Plus, conditionally: a "See all of [Neighborhood]" button,
visible ONLY at neighborhood zoom.
NO category chips on the map — they live inside the search sheet only.

SURFACES — three types and one exit
- Sheets (partial height, swipe down or tap outside, always return exactly one level up):
  zone sheet, spot sheet, search sheet, Places list.
- Toast: local-QA ask. Top-anchored, non-blocking, not modal, arrives on its own,
  auto-dismisses. Never invoked by the user.
- "Go" is not a surface: it hands off to native Maps/Waze and exits the app.
Depth ceiling is 2: map(0) → zone sheet(1) → spot sheet(2). Nothing goes deeper.

VISUAL DIRECTION
Quiet, editorial, map-first. Content-forward, minimal chrome, generous whitespace,
system font (SF). Light and dark both. Suggested accents:
  heat  #E24E1F (dark: #FF7A4D)   local #1C7A5E (dark: #3FD9A6)
  bg    #FAF9F6 / #121315   surface #FFFFFF / #1A1C1F   fg #14171A / #ECEDEE
Heat bands = stepped opacities of the heat accent. Never gradient-blend heat into tag.

FORMAT
Render each screen as a 390×844 iPhone frame with a caption above it. Self-contained HTML,
inline CSS, no external assets. Use CSS shapes/SVG for the map — abstract polygons and
blobs are fine, this is a mockup, not a real map.
```

---

## Screen prompts

**S1 — Cold open, city-wide.** Heat blobs across an abstract Tel Aviv, outline stroke on two or three Local zones only, "Tel Aviv, right now" title mid-fade, slider at *now*, near-me / search / Places icons in chrome. No neighborhood button at this zoom. Show light + dark side by side.

**S2 — Neighborhood zoom.** Zone boundaries drawn, stepped-band fill per zone, strokes on Local and Tourist zones (leave at least two zones blank = Mix), word label at each stroked zone's centroid, "See all of Florentin" button visible. One zone busy + Tourist showing the warning stroke — label reflects it.

**S3 — Close zoom.** Spot pins visible, no tag signal on any pin, two pins carrying the Places ring accent, zone stroke still drawn at the boundary in view, no centroid label.

**S4 — Zone sheet.** Partial-height bottom sheet over a still-visible map. Hand-curated neighborhood blurb + scrollable list of tagged spots, each row a name, category, and its Local / Mix / Tourist word. Include the empty variant: "Nobody's mapped this corner of Tel Aviv yet."

**S5 — Spot sheet.** Name, category, vibe tag word, save icon, "Go" button. Three variants: default, saved (icon filled + inline "Saved"), and data-gap ("no live data right now" where heat would read).

**S6 — Time slider states.** Same map at *now*, *+3h*, *+8h* — heat redraws, tag strokes identical in all three. Caption the invariant: tag never moves with the slider.

**S7 — Search sheet.** Sheet over the map: single text field, two category chips (Food & drinks / Things to do), no default suggestions. Three states: empty, typing with live matches (place name, keyword, neighborhood), and no-results ("Nothing matching 'Port Said' right now", field still open). While results show, the map underneath dims everything except matching pins/zones.

**S8 — Places list.** One merged list. Each row carries a short provenance word — **Saved** / **Auto-saved** / **Visited** — no separate list per mechanism. Include the location-denied variant: only manual saves present, plus "Turn on location to build this automatically" and a Settings link.

**S9 — Local-QA toast.** Top-anchored banner over the map: *"Does this feel like a local spot, or more of a tourist one?"* with Local / Mix / Tourist. Non-blocking, map fully visible and legible behind it. Second frame: collapsed confirmation, "Thanks — that's shared with other travelers."

**S10 — Permission priming.** The single in-app priming line before the two system prompts: *"Let Passenger notice your visits, even when it's closed?"* Plain, one line, not a full-screen takeover. Then the two OS sheets it precedes (Location — Always, then Notifications) sketched as stubs.

**S11 — Degraded.** Location denied: map at default city-wide center, no "you are here", near-me button greyed with inline copy pointing to Settings. Offline: sheet with cached content and a "last updated 12m ago, offline" label. Same board, both conditions.

---

## Block C — flow diagrams

```
Draw these as flow diagrams (FigJam / Mermaid). Boxes are screens, dotted boxes are
system-owned, and mark clearly where the user leaves the app.

1. LAUNCH
Tap icon → Map renders (city-wide, heat + tag, now)
  → Location permission (lazy, non-blocking)
      granted → recenter + Places detection starts → steady state
      denied  → stay city-wide, near-me greyed → steady state

2. FROM STEADY STATE — six reachable things, none leaving the map
tap zone shape → zone sheet | neighborhood button (neighborhood zoom only) → zone sheet |
tap spot pin → spot sheet | drag slider (heat redraws, no navigation) |
Places → spot sheet | Search → spot sheet OR zone sheet OR category browse
Note on the diagram: zone shape, neighborhood button, and a search neighborhood result
are THREE DOORS INTO THE SAME ZONE SHEET.

3. DEEPEST PATH
Zone sheet (1) → Spot sheet (2) → [EXIT] native Maps/Waze

4. ASYNC LOOP (not part of the flow above)
Geofence + dwell timer → dwell ≥ 20 min at a spot already in Passenger's places table?
  yes → auto-save to Places + local notification → tap → toast → answer or ignore
  no (short stop) → plain "Visited" entry, no notification
Guard to render on the diagram: auto-save NEVER fires on an arbitrary coordinate —
only on spots already in Passenger's places table.

5. SIX JOURNEYS as swimlanes, with tap cost per lane
J1 tourist cold discovery (3 taps) · J2 resident planning + save · J3 return via Places
(3 taps) · J4 post-visit feedback (0 in-app taps to trigger) · J5 search-first (2 taps) ·
J6 degraded run
```

---

## Guardrails to repeat if a generation drifts

- No tab bar, no nav bar, no feed, no profile, no settings screen — V1 has none.
- No permanent search bar. Search is an icon that opens a sheet.
- No category chips on the map surface.
- No tag on spot pins, in any form — not a badge, not a tag-colored pin shape.
- No gradient heat. Stepped bands only.
- No in-app route or map-within-a-map — "Go" exits to native Maps/Waze.
- No stacked decorations on a busy + Tourist zone — one warning stroke, replacing.
- Never more than 2 levels deep.
