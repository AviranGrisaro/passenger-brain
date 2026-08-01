# Passenger V1 — interactive wireframe prompt (paste into Claude Design)

Copy everything below into a fresh Claude Design conversation.

---

```
Build an interactive, clickable wireframe of Passenger, an iOS app — greyscale only,
no colour, structure and flow over visuals. Goal: let me tap through every button and
see what screen it leads to, so I can validate the navigation model before any visual
design happens.

GROUND TRUTH — do not invent screens, do not add a tab bar, feed, or profile.

PRODUCT
One map of Tel Aviv, right now: heat (crowd density, fill) and tag (localness —
Local / Mix / Tourist, zone outline stroke). No feed, no scroll. Every screen is either
the map, or something the map handed you.

SURFACES (build every one as a real, tappable frame)
1. MAP — city-wide zoom: heat blobs, stroke on Local zones only, fading "Tel Aviv,
   right now" title, near-me button, search icon, Places icon, time slider (Now→+12h).
2. MAP — neighbourhood zoom: zone boundaries + stepped heat fill, stroke on Local or
   Tourist zones (Mix = no stroke, ever), word label at each stroked zone's centroid,
   "See all of [Neighbourhood]" button (only visible at this zoom).
3. MAP — close zoom: spot pins, NO tag signal on pins ever, ring accent on pins already
   in the user's Places list.
4. LOCATION PERMISSION — iOS system sheet stub (Allow / Don't allow), non-blocking.
5. ZONE SHEET — bottom sheet: neighbourhood blurb + list of spots, each row shows a
   tag word (Local/Mix/Tourist). Reachable 3 ways: tap zone shape, tap neighbourhood
   button, tap a neighbourhood search result — all three must lead to this same screen.
6. SPOT SHEET — name, category, tag word, save icon (toggles filled/"Saved" on tap),
   "Go" button. One level under a zone sheet OR reached directly from a close-zoom pin
   OR from Places OR from a search place result.
7. "GO" HANDOFF — a stub screen: "Exits to Maps/Waze" — not a real Passenger screen,
   dead-ends here, back returns to the spot sheet.
8. SEARCH SHEET — opened by tapping the search icon. One text field + two category
   chips (Food & drinks / Things to do). Typing shows a few fake matching rows (place
   name, keyword, neighbourhood) — tapping a place-name row goes to Spot sheet, tapping
   a neighbourhood row goes to Zone sheet, tapping a chip shows a filtered result state.
9. PLACES LIST — opened by tapping the Places icon. Rows each labeled with a provenance
   word: Saved / Auto-saved / Visited. Tapping a row skips straight to that Spot sheet
   (no zone sheet in between).
10. LOCAL-QA TOAST — a top-anchored banner over the map: "Does this feel like a local
    spot, or more of a tourist one?" with Local/Mix/Tourist buttons. Tapping one
    collapses it to "Thanks — that's shared with other travelers." This is reachable
    from a "Simulate visit notification" debug button somewhere on the map screen,
    since in the real product it arrives on its own, not from user navigation.
11. DEGRADED STATES — toggle switches (not real screens) for "Location denied" and
    "Offline" that a viewer can flip to see the map/zone-sheet/Places variants change:
    near-me greyed out, "last updated Xm ago, offline" label on sheets, Places list
    showing only manually-saved rows.

NAVIGATION RULES TO ENFORCE
- Every sheet (zone/spot/search/Places) must have a visible dismiss (swipe-down handle
  or an X) that returns exactly one level up — never more than one.
- Depth ceiling is 2: Map(0) → Zone sheet(1) → Spot sheet(2). Nothing goes deeper.
  Places and Search-to-spot skip the zone step (they land straight at level 2).
- Zone shape tap, neighbourhood button tap, and a neighbourhood search result must all
  route to the identical Zone sheet screen (same content) — prove this by having them
  literally link to the same screen ID.
- Dragging the time slider only ever redraws heat (implement as a simple state change
  between 3 preset hours: Now / +3h / +8h) — it must NEVER move or change any tag
  stroke, and must not navigate anywhere.

STYLE
Wireframe / low-fidelity only: black outlines, greyscale fills only (use hatching or
grey tints to distinguish heat intensity — no colour), monospace or plain system font
for labels, visible tap affordances (buttons/rows look clickly), a small on-screen
breadcrumb or state label showing which screen is currently active. Frame each screen
at iPhone proportions (~390x844) inside a browser-window shell so multiple screens can
be inspected at once, but only one is "live"/navigable at a time — clicking anything
navigates within that single live frame like a real prototype.

INTERACTION
Make it a real click-through prototype: every button, icon, row, chip, and pin is
clickable and transitions to its target screen with no page reload. Add a lightweight
"back" affordance everywhere (matching the one-level-up rule above) plus a top-level
"reset to map" control for restarting the walkthrough at any point.

Do not add anything not listed above — no settings, no account, no onboarding carousel,
no tab bar.
```

---

**Notes for reuse:** ground-truth block mirrors `design/ux-flows.md` (decisions #8, #12, #17, #23–26) and the static board at `design/mockup-prompts.md` / the wireframe artifact already built. If those decisions change, update this prompt's SURFACES / NAVIGATION RULES sections to match before regenerating.
