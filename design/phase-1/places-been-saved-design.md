# Places — Been & Saved — Design Spec

**Task:** T-036 · **PRD:** [`prds/places-been-saved/places-been-saved.md`](../../prds/places-been-saved/places-been-saved.md) (Draft v1)
**Mockup:** https://claude.ai/code/artifact/2ab0b9c8-5d59-43dd-90e8-8163a7d0b93f — interactive HTML/CSS/JS, click-through, no build step
**Owner:** designer · **Date:** 2026-08-02 · **Status:** ready for `design-approval`
**Research note:** Mobbin MCP requires authorization on this workspace's connector (same standing block T-031/T-033 hit — listed under "MCP servers require authentication" this session). Proceeded from the PRD, `design/ux-flows.md`, `design/map-rendering-spec.md`, and `design/design-principles.md` instead, per the standing "don't block" rule for this research step.
**Figma note:** not attempted. The 2026-07-22 founder ruling makes the HTML artifact the default deliverable, and this task didn't request Figma output.
**Consistency check:** built against the actual shipped code, not just the PRD — `passenger-code/Passenger/Places/{Place,PlaceCatalog,SavedPlacesStore,PlaceCategory}.swift`, `Detail/PlaceDetailModal.swift`, `Map/PlaceLayer.swift`. `Place.swift`'s own doc comment reserves `permanentlyClosed` for "the task that first reads them (T-037/T-038/T-036/T-035)" — this is that task for that field (§8 item 1). `PlaceLayer.swift`'s own doc comment reserves the personal-place ring for "T-036's, §4.4/§6 there" — this spec is that. Palette (`--bg`/`--surface`/`--fg`, category glyphs 🍴/🏛️) carried forward from `design/mockup-prompts.md`'s Block A and T-033's mockup so this reads as the same app, not a new one. The ring/save accent color is grounded in the shipped `AccentColor.colorset` (no override → system blue) and `PlaceDetailModal.swift`'s `saveButton`, not invented (§2, §7). **Cross-spec check against `tourist-trap-flag-design.md` (T-035), also dated 2026-08-02 and also ready for `design-approval`:** that spec already resolves the flag's icon and color token (`camera.fill`, `Color("Flag")` — light `#A15C00`/dark `#F0B429`) for the place modal's own flag line. Caught during this spec's own drafting: an early pass here had invented a second, different amber for this list's tourist-heavy line rather than checking for one already specced. **Fixed before submission** — §2's tourist-heavy line and §4's contrast figures below now cite and reuse T-035's exact token, not a second one for the same signal.
**`ui-design-review` pass:** run explicitly, not cited — see §2.3.

---

## 0. Scope discipline

This spec covers exactly what the PRD hands off:

1. The Places list — one list, three provenance words, precedence at read time.
2. The permanently-closed badge on a Places-list row.
3. The map's personal-place ring accent (binary, close zoom only).
4. Degraded-permission, empty, and offline states for the list.
5. The row → place-detail-modal shortcut and the list's place in the nav-modal exclusivity set.

**Deliberately absent, matching the PRD's own "Not in scope" line:**
- **Passport stickers / per-Hood status** — `passport` (T-037) consumes the Been signal this spec produces; it doesn't render here.
- **The local-QA toast** — `tourist-trap-flag` (T-035) owns it, same dwell/geofence detector, different surface.
- **The place modal's own contents** (name, category, Save, Route) — `hood-place-detail` (T-033), already built and shown here only where the Places list hands off to it. This spec adds nothing to that modal and confirms it stays unchanged (§1, §5).
- **The tourist-heavy flag's icon, animation, and combined "busy and tourist-heavy" phrasing** — `tourist-trap-flag` (T-035) owns all three. This spec places the flag line, on the list row, in a slot marked exactly as T-033 marked its own T-035 slot: placement + the exact locked string ("Tourist-heavy spot") + the on/off condition, nothing else (§2, §2.3).
- **TikTok import as a fourth entry path, share/export** — excluded by the PRD explicitly (PAS-6 item 9; PRD's Not-in-scope line).
- Search, live events, any city but Tel Aviv.

Where the mockup needs to gesture at one of these (map chrome nav icons, the T-035 flag slot), it shows the shallowest possible stub, matching T-033's convention.

---

## 1. Flow

**Entry point:** the persistent Places icon, the 4th icon in map chrome (`ux-flows.md` §2 Primary table, "Saved-places icon"), 0 taps to see, 1 tap to open.

```
Map (depth 0)
  └─ Tap the Places icon → Places list opens (depth "list-1")
        → Tap a row → that place's detail modal opens, stacked over the list (depth "list-2")
              → Swipe down (drag handle) or ✕ → back to the Places list (depth "list-1")
        → Swipe down (drag handle) or ✕ → back to the map (depth 0), camera and selected hour unchanged
```

**The Places list is one of the four mutually-exclusive nav-row modals** — search sheet, heat modal, Places list, Profile tab (`ux-flows.md` §2.1) — opening any one of the other three while the Places list is open closes it first. **If a place modal is stacked over the list at that moment (depth "list-2"), it closes with the list** — there is no orphaned depth-2 sheet left with no depth-1 parent once its parent is gone. This isn't a new rule; it falls directly out of the exclusivity rule already locked in `ux-flows.md` §2.1 applied to the one new case this feature introduces (a modal stacked over a nav-row modal, which none of search/heat/Profile currently have).

**Container mechanism — a custom overlay, not a system `.sheet()`, matching the heat modal's own established fix.** `time-slider-design.md` §2 discovered (REJECT finding 2, 2026-07-30) that a literal `.sheet(isPresented:)` for a nav-row modal covers the nav row itself, breaking the direct nav-button-switch requirement `ux-flows.md` §2.1 states for exactly this modal set. The fix there — a custom `ZStack` overlay layer, above the map content but below the nav row's own layer, sliding in from the bottom — is the exact shape this task's own container needs, since the Places list is explicitly in the same exclusivity set (§2.1's "worked example" note names `time-slider-design.md` §2 for whoever specs this next). **This spec reuses that mechanism rather than re-deriving it:** the Places list is a `ZStack` overlay, not `.sheet(item:)`, so the nav row stays visible and directly tappable the entire time the list is open.

**The place-detail modal, opened from a row, is the opposite case — a real system `.sheet(item:)`, unchanged from T-033.** Once a row is tapped, this spec doesn't invent a second presentation mechanism: it calls the exact same `router.openPlace(id:)` path a direct pin tap already uses (`hood-place-detail-design.md` §1's depth-1 branch), with `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` identical to that branch — not the nested depth-2 case (Hood sheet → place modal), because the Places list isn't a real sheet to nest inside of. The system sheet renders above everything, including the custom Places-list overlay and the nav row, exactly as it already does over a direct pin tap or over an open Hood sheet. Dismissing it reveals the Places list exactly as left; dismissing the list returns to the map, camera and hour untouched — the same "one level up" guarantee every sheet in this app already gives (`hood-place-detail-design.md` §1).

**Bottom-chrome fade, applied not re-derived.** `ux-flows.md` §2.1 names near-me and the Places icon explicitly as the two controls in this footprint that fade out while any nav-row modal is open and fade back in when it closes — including while the Places icon's own modal (this one) is the thing that's open. This spec applies that rule as-is: opening the Places list fades both; closing it restores both. No new chrome-visibility rule is introduced here.

---

## 2. Screens & components

| Component | What it is | SwiftUI-native pattern |
|---|---|---|
| **Places icon (chrome)** | Persistent bottom-region icon, always visible unless another nav-row modal is open (§1's fade rule) | A `Button` in the same floating-icon cluster as near-me, `.opacity`/`.allowsHitTesting()` pair driven by "is any nav-row modal open" — the identical mechanism `time-slider-design.md` §2 built for near-me (`.chrome-hide` class, `setFabsVisible()`), reused for its own second consumer rather than re-implemented. |
| **Places list container** | Custom `ZStack` overlay, slides up from the bottom, below the nav row's own layer (§1) | Not `.sheet()` — see §1's container-mechanism note. Drag handle (swipe down to dismiss) plus an explicit 44×44pt ✕ in the header, same dismiss pattern as the Hood sheet and place modal (`hood-place-detail-design.md` §2). |
| **List header** | "Places" — the exact confirmed name (`ux-flows.md` §9 old Q11, PRD req 1) | `.font(.title2.bold())`, semantic style so Dynamic Type scales it. |
| **Place row** | One list item: category glyph, name, provenance word, closed badge (conditional), tourist-heavy line (conditional) | See §2.2 for the row-density resolution — this is the one real design call this spec makes beyond restating the PRD. `List`/`LazyVStack`, min-height 64pt (comfortably clears the 44pt floor even before Dynamic Type grows it). Tapping anywhere on the row opens that place's modal (§1) — the row itself is the tap target, nothing smaller nested inside it. |
| **Row glyph** | Category icon, 32×32pt, reused from the map pin / Hood-sheet place row (`map-rendering-spec.md` §4, `hood-place-detail-design.md` §2) | Same two-glyph vocabulary everywhere in the app: fork/knife for Eat & Drink, the landmark glyph (never a generic pin) for Things to do. One vocabulary across map, Hood sheet, and this list — never a fourth glyph set invented for this row. |
| **Provenance word** | Plain secondary-tier text, one of **Saved / Been / Visited**, precedence-resolved at read time (PRD req 1) | `Text`, subheadline style, `--muted`-equivalent token (design-principles.md §3, §5 — verified 6.25:1 light / 6.54:1 dark against `--surface` in §4). **Deliberately plain text, not a pill** — see §2.2 for why. |
| **Permanently-closed badge** | The row's one emphasized, pill-styled element — icon + "Permanently closed" | `Capsule()` background, `--badge-bg`/`--badge-fg` tokens (8.59:1 light / 9.67:1 dark against their own pill background, §4), a plain neutral slashed-circle glyph (illustrative in the mockup; exact SF Symbol is `ios-developer`'s call, not a design-time one — same deferral T-033 used for the app-chooser mechanism). **Never red or alarm-toned** — a closed place is a factual state, not a warning (decision #38: "a factual state about the place, not a judgment about its character"), and giving it an alarm color would contradict that framing while also competing with the tourist-heavy line's own color for attention. |
| **Tourist-heavy line — T-035 placeholder slot** | One line, present only when flagged, reading exactly "Tourist-heavy spot" | `HStack { Image(systemName: "camera.fill"); Text("Tourist-heavy spot") }`, smallest/mutedmost tier on the row, rendered below the provenance word and the closed badge. **This spec fixes only placement and the on/off condition** — icon and color are not this spec's call to make, and aren't left generic either: `tourist-trap-flag-design.md` §2 already resolves both (`camera.fill`, `Color("Flag")` — light `#A15C00`/dark `#F0B429`) for the identical signal in the place modal's own copy of this slot, so this row reuses that exact icon and token rather than inventing a second one. Any future combined "busy and tourist-heavy" phrasing stays T-035's call, unaffected by this row. Distinct color family (`Color("Flag")`, 5.19:1 light / 9.16:1 dark against `--surface`, §4, independently reverified against T-035's own figures) from the closed badge's neutral gray, so the two read as different signals even before either label is read. |
| **List empty state** | Icon + one-line description + a real CTA, "Explore the map" | Same shape design-principles.md §4 requires and `hood-place-detail-design.md` §2.3 already fixed once for the Hood sheet's own empty state — applied here from the start rather than needing a second REJECT to add the CTA. Dismisses the list, returning to the map. |
| **Offline banner** | Small, non-blocking strip at the top of the list body, shown only while offline and only if it changes what's on screen | See §3 — in Build Phase 1 this is close to a non-event (bundled seed data has no network dependency at all), so the banner exists for the general product contract, not because Phase 1 can actually go stale. |
| **Personal-place ring accent** | Ring drawn around an existing map pin, close zoom only, wherever that pin's place has any row in the Places list | `map-rendering-spec.md` §6 already specs the *what* (binary, close-zoom-only, reuses the save-icon's accent color) — this spec adds the one thing §6 left silent: the *shape* pairing PRD req 7 bullet 2 requires ("pairs with a shape or icon difference, so it isn't colour-only") and `ux-flows.md` §2.1 flagged as still needed ("the existing ring-accent treatment... needs a shape/icon component alongside it, not just a color/ring difference"). **Resolution, this spec's own addition:** the ring is drawn as a **dashed stroke** (2.5pt weight, 6pt offset from the pin's edge, matching the mockup's own CSS — `.pin.ring::before { border: 2.5px dashed var(--accent); inset: -6px }`), not a solid colored line — the same "weight/dash pattern, not color alone" construction `map-rendering-spec.md` §3 already uses for the tourist-trap zone stroke, applied here to the ring. A dashed ring is legible in grayscale as an added shape (a broken circle around the pin) independent of whether the viewer can perceive its hue, which a solid ring alone would not guarantee. Color: the app's accent color (`AccentColor.colorset`, no override → system blue, `#007AFF`/`#0A84FF`) — the same token `PlaceDetailModal.swift`'s `saveButton` already tints with when saved, grounded in shipped code rather than invented (§7). A short addendum recording this was appended to `map-rendering-spec.md` §6 in this same pass (see that file's dated note, 2026-08-02) — filling the gap, not reopening or reversing the Locked doc's existing calls. |

### 2.1 Precedence and the empty-row edge case

**Precedence is applied at read time, per place, not stored as a single field** (PRD tech design: "one row per (place, provenance)... precedence applied at read time rather than by overwriting"). A place with a Saved row, a Been row, and a Visited row all present still produces exactly one list row, showing "Saved" — the other two rows exist but never render, so un-saving later can reveal them without any new write.

**Un-saving a place with no Been/Visited row removes it from the list entirely** — this follows directly from the precedence model above, not a new invention: if there is no lower provenance to fall back to, there is nothing left to render a row for. The mockup demonstrates this on the one live-interactive row (`florentin-hamakolet`): toggling Save off in the place modal removes that row from the list on return, since this demo place carries no Been/Visited fallback.

**Un-save is reachable only through the place-detail modal's existing bookmark toggle — no swipe-to-unsave on the row itself.** [ASSUMPTION], extending the PRD's own flagged one (req 2 bullet 3, "chosen for consistency with precedence, not specified upstream"): a destructive-feeling swipe gesture implies the row disappears, but a Been/Visited-backed row doesn't — it re-labels instead. Surfacing that outcome inside the modal, where the user can see the place's full context, avoids a swipe action that sometimes deletes a row and sometimes silently relabels it depending on data the swipe gesture itself gives no preview of (Poka-Yoke, design-principles.md §2 — the error this avoids is a user swiping expecting removal and getting a relabel instead, with no way to tell which is coming before committing the gesture).

### 2.2 Row-density resolution (Von Restorff, design-principles.md §2) — PRD's own open risk, resolved here

The PRD names this explicitly as designer's call at `design-review`: *"a row can carry a provenance word, a closed badge, and a tourist-heavy line at once, where design-principles.md §2 allows one special element."* Von Restorff's rule isn't "at most one piece of information per row" — it's that at most one element should visually compete for attention as *special*. This spec resolves the tension by giving **exactly one** row element the emphasized/pill treatment and demoting the other two to plain, differently-toned text:

- **Provenance word** — plain caption text, `--muted` token, no background, no border. Present on every row, so it can't be the "special" element by definition (design-principles.md's own framing: something can't stand out if it's on 100% of rows).
- **Permanently-closed badge** — the row's **one** emphasized element: a filled pill with an icon, its own background token. This is the row's Von Restorff element when present, satisfying the ≥1.5× size / distinct-treatment bar against the plain provenance text above it, without competing with the tourist-heavy line below it (different color family entirely — gray, not amber).
- **Tourist-heavy line** — plain caption text again, smallest tier, its own muted-but-distinct amber token, no pill, no background. Reads as a footnote, not a second badge.

The demo row `neve-nachum-gutman-museum` (Visited + Permanently closed + Tourist-heavy, the worst case) exercises all three at once in the mockup — it reads as one clear hierarchy (name → word → badge → flag line), not three competing signals, because only one of the four elements ever gets pill treatment.

### 2.3 `ui-design-review` pass — applied, not cited

Run against `passenger-brain/design/reference/ui-ux-design-principles-manual.md` and `design/design-principles.md`, directly against this spec and the published mockup's own source, in the skill's own format.

**Passes**
- **Visual hierarchy (manual Ch3; design-principles.md §2, "signalled by size + weight + color together, never size alone"):** the row's four possible elements (name, word, badge, flag) are checked against the mockup's actual CSS, not asserted — name is 16px/600 weight, provenance word 13.5px/400 weight muted color, badge 12px/600 weight on its own pill background, flag line 12.5px/400 weight in its own color family. Four distinct size/weight/color combinations, one clear reading order, matching §2.2's resolution exactly as built.
- **Never-color-alone (manual Ch14; design-principles.md §3):** the closed badge and the tourist-heavy line are distinguished from each other by icon **and** color family **and** pill-vs-plain-text treatment — three independent channels, not one. The ring accent (§2) pairs a dashed stroke shape with its color, the same multi-channel discipline `map-rendering-spec.md` §3 already applies to the zone stroke.
- **Cross-spec token reuse, checked not assumed:** the tourist-heavy line's icon (`camera.fill`) and color (`Color("Flag")`) are read directly from `tourist-trap-flag-design.md` §2's own component table, not re-derived or guessed independently. This matters because an earlier draft of this row had done exactly that — invented a second amber before checking whether one already existed for the same signal (see the issue below).
- **Empty state structure (manual Ch7):** icon + one-line description + a real CTA, present from this spec's first draft — `hood-place-detail-design.md` §2.3 needed a REJECT to add this to the Hood sheet; this spec applies that lesson directly rather than repeating the omission.
- **Touch targets (manual Ch13; design-principles.md §2, Fitts's Law):** checked against actual mockup CSS, not asserted. The list ✕ is 44×44pt with a 32pt visual glyph centered inside (`hood-place-detail-design.md`'s established pattern, `.icon-btn` in the mockup source). Rows are `min-height: 64px` — no row is reachable below the 44pt floor even before any inner content grows it. The row itself is the sole tap target; no smaller element inside it (badge, flag line) is independently tappable, so there's no sub-44pt target hiding inside a larger one.

**Issues found, and fixed in this same pass**
1. **Closed-badge color risked reading as a warning (manual Ch5 "Color meaning"; decision #38's "factual, not a judgment" framing):** an early pass considered amber or red for the closed badge to make it "stand out." Checked against decision #38's explicit language and req 4's "never substitutes for [the tourist-heavy line]" bullet — a warm/alarm color would both misrepresent a factual state as a warning and visually collide with the tourist-heavy line's own amber tone, undermining the "the two are independent" requirement. **Fixed:** closed badge uses a neutral gray pill (`--badge-bg`/`--badge-fg`), reserving the warmer amber family exclusively for the tourist-heavy line, so the two are distinguishable by color family alone before either icon or word is read. §2's badge row and the mockup were both built to this from the start of this pass.
2. **The ring's "shape difference" requirement (PRD req 7 bullet 2) had no resolution anywhere in the existing design system:** `map-rendering-spec.md` §6 specs only a colored ring; `ux-flows.md` §2.1 flags the gap directly but doesn't resolve it. **Fixed:** §2's ring row above specs a dashed stroke (not solid), reusing the exact weight/dash construction `map-rendering-spec.md` §3 already established for the tourist-trap zone stroke — and a short dated addendum was appended to `map-rendering-spec.md` §6 itself in this same pass, so the resolution lives with the rule it completes, not only in this spec.
3. **A duplicate, uncoordinated color token for the tourist-heavy signal — caught by this spec's own cross-spec check, not by a downstream reviewer.** An early draft of the tourist-heavy line (§2) specified its own amber (`#8A5A00` light / `#E3B34D` dark) without first checking whether `tourist-trap-flag` had already named one — it had, in `tourist-trap-flag-design.md` §2, dated the same day. Two design docs specifying two different colors for the identical "tourist-heavy" signal is exactly the kind of drift `design-principles.md` §3's "define a semantic color set" rule exists to prevent. **Fixed:** §2's row and every contrast figure in §4/§7 below now cite and reuse `Color("Flag")` (`#A15C00`/`#F0B429`) directly, independently re-verified at 5.19:1 light / 9.16:1 dark against `--surface` rather than trusted from the other spec's own number.

**Quick wins considered, not applied**
- **A section header per provenance ("Saved," "Been," "Visited") instead of inline words.** Considered as a way to make the precedence rule visually obvious without reading each row. Rejected: the PRD's own P1 list names "filtering or sectioning by provenance" as a nice-to-have, explicitly deferred past P0 — building it into the base row design here would preempt that P1 call rather than leave it open, and a flat list with an inline word already satisfies every P0 bullet in req 1 without it.
- **Showing the closed badge inside the place-detail modal too, for redundancy.** Rejected on the PRD's own explicit line: "the place modal never renders a closed badge; that lives on the Places-list row only" (this PRD's Not-in-scope note, echoed in `hood-place-detail-design.md` §0). Not this spec's call to reopen.

---

## 3. Every state

Per design-principles.md §4 and PRD reqs 1, 2, 5, 6.

| State | Behavior |
|---|---|
| **Loading** | Place metadata (name, category, coordinates) comes from the same session-scoped `PlaceCatalog` load the map already performs — in Build Phase 1 this is seed-authoritative and effectively instant (`PlaceCatalog.swift`'s own doc comment: "no code path fetches when a sheet opens"). The list opens immediately; there is no realistic loading state to design for in Phase 1. |
| **Empty (nothing saved, been, or visited yet)** | Icon + "Nothing saved yet. Save a place from its detail card, or wait for Passenger to notice where you've been." + "Explore the map" CTA (§2, §2.3). Not an error — this is the expected first-run state for every new install (PRD req 6). |
| **Populated** | Rows in whatever order the underlying store returns them (P1: sectioning by provenance is deferred, §2.3). No sort order is specified as a P0 requirement here — flagged for `architect`/`ios-developer` at §8 item 4. |
| **Degraded permission — Location Always denied** | Manual Saved rows render and behave fully. No Been or Visited rows ever appear, and the list renders **no copy explaining why** (PRD req 5, hard requirement — this is not an empty-with-explanation state, it's identical in appearance to a world where nobody has dwelled anywhere yet). Re-requesting the denied permission from this screen never happens. |
| **Degraded permission — Location denied entirely** | Same as above; the list still opens and still shows every Saved row (PRD req 5 bullet 2). |
| **Offline** | Every already-known row (Saved, Been, or Visited) renders from the device, unchanged (PRD req 6 bullet 2). A manual Save made while offline appears in the list immediately — it was always a local-only write in Build Phase 1 (no server round trip exists to wait on at all, `SavedPlacesStore.swift`'s `toggle()` is synchronous-to-memory with fire-and-forget disk persistence). **Clarifying the PRD's "syncs later" language for a device-local, no-backend feature:** in V1's actual technical design ("writes nothing server-side"), there is no server copy for an offline save to sync *to* — the offline banner communicates "this device's own data," not a pending-upload state, since no upload exists in this feature at all. Flagged at §8 item 5 rather than silently reinterpreting the PRD's own wording. |
| **A row's place has no current-hour density** | The row still opens the place modal normally; whatever "no data this hour" treatment the heat readout uses inside that modal (owned by `map-hoods-heat`/`hood-place-detail`, not this spec) is unchanged by arriving via this list instead of the map (PRD req 6 bullet 3, Journey 3). This spec adds no new blocking condition on top of what those specs already handle. |
| **Error (place data fails to resolve for a row already in the list)** | Extremely unlikely in Build Phase 1 given the seed-authoritative catalog, but specified rather than assumed impossible (design-principles.md §4): the row still renders its provenance word and any badge/flag from local storage, and tapping it shows the place modal's own "Couldn't load this place" state (`hood-place-detail-design.md` §3), not a second error surface invented here. |

---

## 4. Accessibility notes

- **VoiceOver labels, every row:** one combined announcement per row — name, category, provenance word, and (when present) "permanently closed" / "Tourist-heavy spot" appended in that order, e.g. *"Nachum Gutman Museum, Things to do, Visited, permanently closed, Tourist-heavy spot."* This mirrors `map-rendering-spec.md` §7's existing pattern of appending clauses rather than requiring a second gesture to discover state (the same construction that section already uses for a personal-place pin's "in your Places" clause). The mockup's VoiceOver-preview toggle renders this exact string per row.
- **The ring accent's VoiceOver label** is `map-rendering-spec.md` §7's own established clause ("...in your Places") — unchanged by this spec; this spec only adds the visual dashed-stroke detail (§2), not a new spoken string.
- **Dynamic Type:** name, provenance word, badge text, and the flag line all use semantic text styles, never a fixed point size. At the largest accessibility sizes, the row's elements stack vertically rather than wrap awkwardly inline — this spec deliberately never places the badge or flag line inline beside the provenance word (§2.2's own layout), so there is no horizontal wrap to manage at any type size; the row simply grows taller.
- **Contrast (WCAG AA, design-principles.md §5) — computed against the mockup's own source tokens, not asserted:**
  - Provenance word (`--muted` on `--surface`): **6.25:1 light / 6.54:1 dark** — clears the 4.5:1 normal-text bar with margin in both themes.
  - Closed-badge text on its own pill background: **8.59:1 light / 9.67:1 dark**.
  - Tourist-heavy line text (`Color("Flag")`, reused from `tourist-trap-flag-design.md` §2) on `--surface`: **5.19:1 light / 9.16:1 dark** — independently recomputed here, matches that spec's own §2.3 figures for the same token.
  - Ring stroke against the map background: **4.02:1 light / 3.65:1 dark** — checked against the 3:1 UI-component bar (WCAG AA's lower threshold for graphical objects, not the 4.5:1 text bar), since the ring is a stroke, not text; both pass. The mockup's live "Contrast, computed" panel recomputes all four pairs from the same hex values the CSS actually uses, in both themes, rather than a value copied once and left to drift.
- **Touch targets:** the list ✕ (44×44pt hit / 32pt visual glyph) and every row (≥64pt tall) are the only interactive elements this spec adds; both checked in §2.3.
- **Reduce Motion:** the list's slide-up entrance/exit and the stacked place-modal's own transition both honor Reduce Motion — the mockup's toggle sets both transitions to 0ms rather than skipping the state change, matching `hood-place-detail-design.md` §4's precedent.

---

## 5. PRD traceability

| PRD requirement | Where this design satisfies it |
|---|---|
| P0-1 One list, three provenance states, one word/row, precedence Saved>Been>Visited, distinguishable by word not color | §2 Provenance word row; §2.1 Precedence; §2.2 Row-density resolution |
| P0-2 Manual save <400ms, persists, reopening shows saved | Already built and unchanged (`SavedPlacesStore.swift` — synchronous in-memory toggle, fire-and-forget persistence); §2.1 confirms how the list reads it |
| P0-2 bullet 3 Un-save drops Saved, falls to next provenance or removes the row | §2.1 Precedence and the empty-row edge case — [ASSUMPTION], extending the PRD's own flagged one |
| P0-3 Been/Visited detection, silent, no confirmation, revisit adds nothing | Out of this spec's surface (detector is `data-engineer`'s, shared across T-035/T-036/T-037 per the PRD's own tech design) — §3's Populated/Loading rows confirm the list has no confirmation UI for either to design against |
| P0-4 Closed places save; badge distinct, never substitutes, never blocks, updates on next render | §2 Permanently-closed badge row; §2.2/§2.3 issue 1 (color resolved to avoid reading as a warning); §8 item 6 for the still-ownerless refresh job the last bullet depends on |
| P0-5 Degraded permission never breaks the feature, no re-ask, no error copy | §3 Degraded-permission rows |
| P0-6 Empty/offline states plain, not errors; row still opens with no current-hour density | §2 List empty state; §3 Empty/Offline/no-density rows |
| P0-7 Map ring accent, binary, close-zoom only, pairs with shape not color, ≥44pt target unaffected | §2 Personal-place ring accent row (this spec's own shape addition, §2.3 issue 2); `map-rendering-spec.md` §6 (cited, addendum appended) |
| P0-8 Row opens place modal directly, skipping the Hood sheet; nav-modal exclusivity; dismiss returns to unchanged map | §1 Flow (full container-mechanism and dismiss-chain resolution) |
| P1 Filtering/sectioning by provenance | §2.3 Quick wins considered, not applied — explicitly deferred, not built into the base row |
| P1 Opening hours on the row | **Not built into this pass** — P1, no curated-hours field reaches this list's data source in Build Phase 1; layering it on later doesn't change any P0 structure above |

---

## 6. Mockup

Interactive HTML/CSS/JS artifact, published as a Claude Artifact: **https://claude.ai/code/artifact/2ab0b9c8-5d59-43dd-90e8-8163a7d0b93f**

**Reviewer instrumentation lives entirely outside the phone frame** — a deliberate, stricter separation than `hood-place-detail-design.md`'s inline dashed captions, which predate the 2026-07-30 artifact-conformance standing rule this spec follows. Every control (state buttons, theme/VoiceOver/Reduce-Motion toggles, the live contrast table, the "now showing" caption) sits in a bordered panel beside the phone frame, set in a monospace face specifically so it reads as instrumentation, not app chrome; nothing inside the frame is demo-only or unlabeled by a spec row (§0, §2's own component table maps every element the mockup draws).

What it demonstrates, live:
- **The full flow** — tapping the Places icon opens the list (fading near-me and the icon itself, per §1); tapping a row stacks the place modal over the still-visible list; dismissing either returns exactly one level up, matching §1's flow diagram exactly.
- **All six row-density combinations** — plain (Saved, Been, Visited alone), provenance + closed badge, provenance + tourist-heavy line, and the worst case (all three at once) — the same six demo places named in §2.2 and §8 item 3.
- **Precedence live, not just described:** toggling Save off on `florentin-hamakolet`'s row (via the stacked place modal's own bookmark button) removes that row from the list on return, since this demo place has no Been/Visited fallback (§2.1).
- **Empty and offline states**, switchable via the panel without leaving the current theme/toggle state.
- **The ring accent on the map**, at close zoom, on two of three demo pins — dashed stroke, not a solid colored ring, next to a third plain pin for contrast.
- **VoiceOver label preview**, per row and aggregated in a log panel, same convention as T-031/T-033's mockups.
- **A live, recomputed contrast table** for every color pair this spec cites a ratio for (§4), reading the mockup's own CSS custom properties rather than a static number typed once.
- Both light and dark themes via the theme toggle, palette consistent with `design/mockup-prompts.md`'s Block A and both prior Phase-1 mockups.

Deliberately **not** in the mockup: the place modal's own full content beyond what's needed to demonstrate the hand-off (Route hand-off simulation, Scenic/Fast selection — none of that is this task's), Passport stickers, the local-QA toast, search, live events, any city but Tel Aviv. The map background is the same minimal abstract-blob stub `mockup-prompts.md` specifies, not a re-design of the map itself.

---

## 7. Principles conformance

| Call this spec makes | Citation |
|---|---|
| The Places list is a custom overlay layer, not `.sheet()`, so the nav row stays reachable while it's open | design-principles.md §3 (Sovereign posture — dense, learnable, used constantly); `ux-flows.md` §2.1 (nav-row-must-stay-reachable rule, and its own pointer to `time-slider-design.md` §2 as the worked example this spec reuses) |
| Places list itself is Sovereign, not Transient — no first-run over-explanation | `ux-flows.md` §2.1, explicit: "the 3(4)-button nav row and its modals (heat modal, search sheet, Places list) should be classified Sovereign" |
| Provenance word is plain text; closed badge is the row's one pill-styled/emphasized element; tourist-heavy line is plain text in a third tone | design-principles.md §2, Von Restorff ("only one 'special' element per view"); manual Ch9 — checked against the row's actual four-tier size/weight/color set in §2.3, not asserted |
| Closed badge and tourist-heavy line never rely on color alone — icon + color family + pill-vs-plain treatment, three channels | design-principles.md §3 ("never rely on color alone"); manual Ch14; `map-rendering-spec.md` §3's same multi-channel construction, reused |
| Ring accent is a dashed stroke, not a solid colored line — the shape-pairing PRD req 7 bullet 2 requires, filling the gap `map-rendering-spec.md` §6 and `ux-flows.md` §2.1 both left open | PRD req 7 bullet 2 (direct requirement); `map-rendering-spec.md` §3's weight/dash construction, applied to a second surface (§2.3 issue 2) |
| List ✕ and every row clear the 44pt floor; row min-height 64px measured in the mockup source, not asserted | design-principles.md §2, Fitts's Law; manual Ch13 |
| Sub-400ms open, no spinner, for a load this feature performs against an already-cached catalog | design-principles.md §2, Doherty Threshold; manual Ch9 |
| Un-save reachable only via the modal's own toggle, not a swipe gesture on the row | design-principles.md §2, Poka-Yoke — a swipe that sometimes deletes and sometimes relabels, with no preview, is the exact error-prone pattern the principle warns against |
| Every state — loading (n/a in Phase 1, stated why), empty (icon + description + CTA), degraded-permission (×2), offline, error — specified rather than left to the developer | design-principles.md §4; manual Ch7 |
| Contrast: provenance word, closed badge, and tourist-heavy line all checked at their real WCAG bar (4.5:1 text) in both themes; ring stroke checked at the correct lower UI-component bar (3:1), not held to the text bar by mistake | design-principles.md §5, WCAG AA; manual Ch14 — the mockup's live-recomputed table is the artifact-conformance check for this row, not a value typed once and left unverified |
| VoiceOver label appends clauses in a fixed order (name, category, provenance, closed, flagged) rather than expecting multiple separate announcements to be inferred together | design-principles.md §3, §5; `map-rendering-spec.md` §7's identical construction for the ring's own "in your Places" clause, extended here to a full row |
| Hick's Law / Miller's Law | Not applicable — this screen has no multi-option decision or chunking surface; a flat list of provenance rows isn't a decision the user is making, it's a record. Flagging the omission rather than citing a section that doesn't apply, same convention T-031/T-033 used |

No Section 2/3/5 area relevant to this feature was left unaddressed. §2.3 documents the `ui-design-review` skill run for real against this spec and mockup — two issues found and fixed in this same pass (closed-badge color risk, the ring's missing shape pairing), one deferred call recorded with its reasoning (provenance sectioning, correctly left to the PRD's own P1), one PRD ambiguity (closed-badge-vs-modal redundancy) checked and correctly left alone rather than "fixed" into a PRD violation.

---

## 8. Open items handed to `architect` / `ios-developer`

Not blocking `design-approval`, flagged for the TRD:

1. **`Place.permanentlyClosed` needs adding to the model and decoded from the seed JSON's existing `permanently_closed` key** (`Place.swift`'s own comment names T-036 as the task that reads it; `places-tel-aviv.json` already authors the field on every row, currently all `false` — `PlaceCatalog`'s `SeedFile.Entry` currently ignores it as an undeclared key). Recommend flipping `kerem-carmel-spice-corner` and `neve-nachum-gutman-museum` to `true` in the bundled seed for the two demo rows this spec's mockup uses to exercise the badge (§2.2, §6) — a data change, not a design one, but named here so the demo the PRD's dispatch brief asked for ("a permanently-closed one to exercise the badge") has a concrete seed to point at.
2. **A Been/Visited provenance store needs building — there is no live dwell/geofence detector in Build Phase 1.** The PRD's own tech design already says this detector is shared across three consumers (this list, `tourist-trap-flag`'s local-QA ask, `passport`'s stickers) and named `data-engineer` as its owner, "must not be built three times." For Build Phase 1's fake/seeded data specifically: recommend a small bundled fixture (parallel to `places-tel-aviv.json`, same `PlacesFetching`/`PlacesCaching`-style protocol seam `PlaceCatalog` and `SavedPlacesStore` already establish) rather than wiring a real background-location detector this early — consistent with the board's Build Phase 1 scope ("fake/hardcoded data baked into the app"). Suggested demo rows: `kerem-dr-shakshuka` and `kerem-carmel-spice-corner` as Been, `florentin-street-art-walk` and `neve-nachum-gutman-museum` as Visited — the exact six rows this spec's mockup already uses (§6), so the design and the eventual build exercise the same fixture rather than two different ad hoc sets.
3. **Read-time precedence merge (§2.1) needs a real implementation home** — some function or store that, given a place ID, returns the highest-precedence provenance across Saved/Been/Visited sources without mutating any of them. This spec specifies the *behavior* (PRD tech design already requires it); the *class/actor boundary* is `architect`'s call, following the same `@Observable`/protocol-seam pattern `SavedPlacesStore`/`PlaceCatalog` already use.
4. **Row sort order** — this spec doesn't specify one (§3 Populated row). Recency of the underlying provenance event, alphabetical, or Hood-grouped are all live options; none is a P0 requirement.
5. **The PRD's "an offline save appears immediately and syncs later" (req 6 bullet 2) doesn't describe an operation this feature's technical design actually performs** — there is no server-side write in V1 for this data to sync *to* (PRD tech design: "writes nothing server-side in V1"). §3's Offline row reads this as inherited boilerplate rather than silently building a sync path that doesn't otherwise exist; flagging for `product`/`architect` to confirm the PRD's wording should be read that way, or correct it, at the next PRD revision — not resolved unilaterally here.
6. **Closed-state refresh remains ownerless**, exactly as the PRD's own Open questions & risks section already states — req 4's last bullet ("closes after being saved shows the badge next time the list renders") is unbuildable-with-integrity until that refresh job has an owner and cadence. This spec's badge design is correct regardless of when the underlying field last changed; it doesn't attempt to resolve the staleness question itself, per the dispatch brief's explicit instruction not to resolve PRD-level open risks here.
