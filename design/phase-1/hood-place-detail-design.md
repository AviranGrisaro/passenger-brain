# Hood & Place Detail — Design Spec

**Task:** T-033 · **PRD:** [`prds/hood-place-detail/hood-place-detail.md`](../../prds/hood-place-detail/hood-place-detail.md) (Draft v1 — no v2 exists yet at time of writing)
**Mockup:** https://claude.ai/code/artifact/06f8a49b-7de4-430f-a701-96279db74611 — interactive HTML/CSS/JS, click-through, no build step
**Owner:** designer · **Date:** 2026-07-30 · **Status:** ready for `design-approval` (revised post-REJECT — see PROGRESS.md 2026-07-30 entries for the fix-by-fix record: `product`'s reject, then this fix pass)
**`ui-design-review` pass:** run explicitly against this spec and mockup (Aviran's ask, mid-task — the skill had been cited but not actually invoked). See §2.3 for the applied review (Passes / Issues / Quick Wins) and the two real fixes it produced, both already folded into the spec and mockup below rather than left as follow-ups.
**Research note:** Mobbin MCP is listed as requiring authorization on this workspace's connector (same standing block T-031 hit). Proceeded from the PRD, `design/ux-flows.md`, `design/map-rendering-spec.md`, and `design/design-principles.md` instead, per the standing "don't block" rule for this research step.
**Figma note:** not attempted. The 2026-07-22 founder ruling makes the HTML artifact the default deliverable, and this task didn't request Figma output.
**Consistency check:** fills in the Hood sheet T-031's mockup explicitly stubbed as a T-033 placeholder — same one-tap-open interaction T-031 established (tapping a Hood always opens directly to this sheet, never a two-step preview). Palette (`--bg`/`--surface`/`--fg`, heat accent `#E24E1F`/`#FF7A4D`) carried forward from `design/mockup-prompts.md`'s Block A so this mockup reads as the same app as T-031's, not a new one.

---

## 0. Scope discipline

This spec covers exactly the four components the PRD hands off, no more:

1. Hood sheet — name, hand-curated blurb, place list, empty states
2. Place detail modal — name, category, save action, route action
3. Action hierarchy — exactly one primary action (Route); Save demoted
4. Route hand-off — native Maps/Waze, walking, no in-app navigation

**Deliberately absent, matching the PRD's own "Not in scope" line and this task's brief:**
- **Quick filters / category chips** — decision #41 keeps these sheet-internal to search; owned by `search-quick-filters` (T-038). Never rendered here or on the map.
- **The tourist-heavy flag's full design** — `tourist-trap-flag` (T-035) owns the flag's icon, animation, and combined VoiceOver phrasing (e.g. "busy and tourist-heavy"). Its PRD req 6 already fixes the exact string ("Tourist-heavy spot"), the condition (flagged places only, silence otherwise), and its home (one line in the place modal, nowhere else) — so this spec implements exactly that string and that condition, in a slot clearly marked as T-035's, rather than inventing surrounding visual treatment T-035 hasn't designed yet. Same pattern T-031 used for stubbing this task.
- **Places list, provenance words (Saved/Been/Visited), the permanently-closed badge** — owned by `places-been-saved`. The place modal never renders a closed badge; that lives on the Places-list row only (PRD's own Not-in-scope line).
- **Scenic Walk vs. fastest-route selection, any route polyline** — excluded by this PRD explicitly (PAS-7). `ux-flows.md` §2/§8a's three-button Fast/Scenic/Save proposal does **not** apply here — this modal has exactly two actions, Route and Save, because Scenic/Fast selection isn't in scope for T-033 at all.
- Search, Passport, live events, any city but Tel Aviv.

Where the mockup needs to *gesture* at one of these (map chrome icons, the Places-list ring accent visible on one background pin), it shows the shallowest possible stub and labels it in the mockup's "what this deliberately excludes" card — it does not design the thing it's stubbing.

---

## 1. Flow

**Entry points (both already established by T-031/`ux-flows.md` §5 — this spec doesn't invent new ones):**

```
Map (depth 0)
  ├─ Tap a Hood polygon, or the Hood/neighborhood button → Hood sheet opens directly (depth 1)
  │     → Tap a place row → Place modal opens directly, stacked over the Hood sheet (depth 2)
  │           → Swipe down (drag handle) or ✕ → back to Hood sheet (depth 1)
  │     → Swipe down (drag handle) or ✕ → back to map (depth 0)
  │
  └─ Tap a place pin directly → Place modal opens directly (depth 1) — never via the Hood sheet
        → Swipe down (drag handle) or ✕ → back to map (depth 0)

From either depth, inside the Place modal:
  → Tap Save → toggles the saved state in place, modal stays open, no exit
  → Tap Route → native action sheet (Maps / Waze, when both installed) → hand-off, app exits
        → Returning to Passenger → map state (camera, selected hour) unchanged, all sheets closed
```

**Depth ceiling: 2, matching `ux-flows.md` §5's rule exactly** — Map (0) → Hood sheet (1) → Place modal (2) is the deepest path; a direct pin tap reaches the Place modal at depth 1 instead, a shortcut, not a new level. Dismissing any sheet returns exactly one level up (Place modal → whatever opened it; Hood sheet → map).

**Dismiss gesture, corrected at this fix pass:** a sheet dismisses via its drag handle (swipe down) or the explicit ✕ control — **not** by tapping the exposed map**.** The original submission had "tap outside" dismiss the sheet via a full-surface invisible backdrop, which is what caused finding B1 (`design-approval` REJECT, 2026-07-30): that backdrop sat over the entire screen and intercepted every tap over the still-visible map, so the map was never actually reachable while a sheet was open, contradicting PRD req 1's "stays visible and interactive." §2's Hood sheet container and Place detail modal container rows now name the real mechanism (`.presentationBackgroundInteraction`) and there is no backdrop left to swallow taps — a tap landing on the exposed map interacts with the map, it does not dismiss the sheet.

**Exits:** the only true exit from Passenger is the Route hand-off to native Maps/Waze. Save never exits. Every sheet dismiss (drag handle or ✕) returns exactly one level up, map camera and selected hour untouched (PRD req 1).

---

## 2. Screens & components

| Component | What it is | SwiftUI-native pattern |
|---|---|---|
| **Hood sheet container** | Partial-height sheet over the map, reached from a Hood tap or the Hood button | `.sheet(item:)` with `.presentationDetents([.medium, .large])` **plus `.presentationBackgroundInteraction(.enabled(upThrough: .medium))`, named explicitly here** — `.presentationDetents` alone does not give background interaction in SwiftUI (the default is a dimmed, non-interactive scrim); the separate modifier is required and is the actual mechanism behind PRD req 1's "map stays visible and interactive behind it." Enabled up through `.medium` rather than unconditionally through `.large`, since at `.large` the sheet covers nearly the full screen and there's negligible exposed map to interact with anyway. **Fixed at this pass** — the original submission named no mechanism and the mockup's full-surface backdrop did the opposite (`design-approval` REJECT finding B1, 2026-07-30); see §1's dismiss-gesture note. |
| **Hood sheet header** | Hood name | `.font(.title2.bold())`, semantic text style so Dynamic Type scales it (design-principles.md §3). |
| **Hood blurb** | Hand-curated paragraph, when curated | `Text`, body style. **Renders only when present** — a Hood with no blurb yet shows the place list alone, with zero placeholder copy standing in for it (PRD req 2, hard requirement, not a design call). |
| **Place list** | Every curated place in the Hood, name + category | `List`/`LazyVStack` of place rows, each ≥44pt tall. Tapping a row opens that place's detail modal directly — no intermediate state. |
| **Place row** | One list item: category glyph, name, category word | Reused visual language from the map's own pin glyph (`map-rendering-spec.md` §4: fork/knife vs. a **distinct landmark glyph**) so the same category reads identically on the map and in this list — one glyph vocabulary, not two. **Fixed at this pass:** the mockup's "Things to do" glyph was a generic map pin (📍) rendered inside the pin shape — a pin-inside-a-pin that reads as "location," not "thing to do," and fails map-rendering-spec.md §4's warning that this glyph is "the *only* way to visually tell categories apart during ordinary browsing" post-decision-#25. Replaced with a landmark glyph (🏛️) everywhere the category renders — map pin, place row, category row — so it's visually distinct from both the pin's own shape and Eat & Drink's fork/knife (🍴). |
| **Hood empty state (no curated places)** | Plain empty state, not an error | Icon + one-line text ("No places curated here yet.") + a real CTA ("Explore another Hood," dismisses the sheet) per design-principles.md §4's "illustration + description + a CTA" shape — see §2.3 for why an earlier no-CTA draft was corrected. **44pt hit area fixed at this pass:** the CTA's visible text stays small (13.5pt), but its tappable area now extends to a full 44pt-tall invisible padding box around the text — same "small glyph, full-size hit area" pattern `map-rendering-spec.md` §4 already establishes for map pins, applied here since the CTA has no visible border/background to enlarge. |
| **Place detail modal container** | Sheet presented on top — either directly from the map (depth 1) or stacked over an open Hood sheet (depth 2) | `.sheet(item:)` presented from either the map view or, when stacked, from within the Hood sheet's own view hierarchy — iOS natively supports a sheet presented from a sheet. **Background interaction resolved explicitly at this pass (was left ambiguous, part of REJECT finding B1):** at depth 1 (direct pin tap, presented straight from the map view) the modal carries the same `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` as the Hood sheet, so the map stays live behind it. At depth 2 (stacked over an already-open Hood sheet) the modal does **not** enable background interaction — `.presentationBackgroundInteraction` doesn't cascade through a nested sheet automatically, and nothing in the PRD asks for "tap a Hood-sheet row while the Place modal is open" as an interaction, so the conservative default (dimmed, non-interactive Hood sheet underneath) applies there instead. The mockup demonstrates both: tapping the exposed map at depth 1 reaches it; at depth 2 a toast states the interaction is deliberately paused. **Flagging for architect/TRD:** confirm this same depth-1-vs-depth-2 split is buildable as described — SwiftUI's nested-sheet background-interaction behavior is the one place presentation depth could diverge from what's spec'd here. |
| **Place modal header** | Place name (left) + Save (icon-only, top-right) + dismiss | Save sits in the header, **not** beside Route — this spatial separation is deliberate (see §2.2) so the two actions are never adjacent, reducing accidental taps between "save" and "exit to another app." The ✕ dismiss control (shared with the Hood sheet header) gets the same 44pt hit-area fix described below. |
| **Sheet dismiss (✕), both sheets** | Small circular glyph button, top-right of the header | **44pt hit area fixed at this pass:** the visible circle stays 32×32pt (unchanged appearance — no forced visual resize), but the actual button/tap target is now a 44×44pt box with the 32pt circle centered inside it, matching `map-rendering-spec.md` §4's own established pattern ("the tappable area is never just the drawn glyph's bounding box if that's smaller than 44pt"). Was flat 32×32pt with no expanded target — Fitts's Law violation (design-principles.md §2), REJECT finding B3. |
| **Category row** | Category glyph + word ("Eat & Drink" / "Things to do") | Same glyph as the place row and the map pin — one vocabulary across all three surfaces (PRD req 6, `map-rendering-spec.md` §4). Never color-only. Things to do's glyph is the landmark icon (🏛️), not a generic pin — see the Place row fix above. |
| **Tourist-heavy flag line — T-035 placeholder slot** | One line, present only when the place is flagged, reading exactly "Tourist-heavy spot" | `Text` + small icon, rendered between the category row and the bottom action. **This spec fixes only placement, the exact string, and the on/off condition** — all three already locked by `tourist-trap-flag` req 6. Icon choice, entrance animation, and the combined phrasing for a busy+flagged state are explicitly T-035's design call, not resolved here. The mockup marks this slot inline when "design annotations" is toggled on, so a reviewer can't mistake the placeholder for a finished T-035 design. |
| **Save action** | Icon-only bookmark toggle, header-right | Compact `Button` with an SF Symbol (bookmark / bookmark.fill), `.buttonStyle(.plain)`, tinted with the app's positive accent when saved. **The icon swaps outline→filled variants of the same symbol, never to an unrelated glyph** — a checkmark or similar would read as "confirmed," not "saved" (manual Ch14 "Toggle Buttons with aria-pressed" — keep the icon/label semantically constant, let the fill/tint plus the accessible pressed-state communicate the change). **Never the primary action** (PRD req 4) — no fill, no bottom-anchored placement, styled as the manual's own Secondary button tier (outline, transparent) rather than Primary (solid). Writes to the manual "Saved" path only, instantly and optimistically (PRD req 7, tech design's "responds inside the 400ms budget regardless of network"). **Reads from a per-place saved-state source on every open, fixed at this pass** — the original submission hardcoded `saved = false` on every `openPlace`/`openPlaceFromHood` call, so a previously-saved place always re-opened looking unsaved (REJECT finding B2, PRD req 7's "visible on reopen"). The button's initial render now looks up the current place's persisted saved state (a `[PlaceID: Bool]` store client-side, ahead of whatever real persistence `architect`/`ios-developer` build) before the modal is shown, rather than defaulting to unsaved. See §3's new "already saved, reopened" row. |
| **Route action** | Full-width filled button, bottom-anchored | `Button` with `.buttonStyle(.borderedProminent)`, thumb-zone placement (design-principles.md §3). The modal's **only** primary action (PRD req 4). Tapping it presents a native action sheet choosing Maps or Waze when both are installed on-device; with only one installed, it opens that one directly; with none available (a defensive case — see §3), the button is disabled with inline explanatory text instead of failing silently or crashing (PRD req 5). **The hand-off always requests walking directions** (PRD req 5's own bullet: "opens native Maps or Waze with the place as destination, walking mode") — the deep link's mode parameter is fixed to walking regardless of which app is chosen or which of the two branches below fires; this isn't a user choice or a driving/walking toggle anywhere in this modal. **Threaded through explicitly at this pass** — the original submission named walking mode once in §0's scope list and then dropped it from every other section (REJECT finding, should-fix #6); it's now stated here, carried into §5's traceability row, and folded into §8 item 2 below rather than left implicit. **Flagging for architect/TRD:** whether the app-chooser is a genuine `UIAlertController` action sheet or a direct `UIApplication.open` to the sole available app isn't fully resolved here — a build-time call, not a design one, since either satisfies "hands off to native Maps or Waze" and either must carry the walking-mode parameter. |

### 2.1 Category rename, everywhere

Every string this spec renders uses **"Things to do"** and **"Eat & Drink"** exclusively (decision #33) — Hood sheet place rows, the place modal's category row, and the (excluded) map pin glyph legend referenced above all share the same two values. No third value, no null, no "Food & drinks" residue anywhere in this spec or its mockup (PRD req 6).

### 2.2 Action hierarchy (Von Restorff, design-principles.md §2)

Route and Save are **not** competing for the same visual row — this is the core design decision this spec makes beyond what the PRD states literally:

- **Route** is a filled, full-width, bottom-anchored button — the modal's one and only primary action, sitting alone in the thumb zone.
- **Save** is a small icon-only toggle in the header, spatially separated from Route by the entire height of the modal body. It reads as a lightweight, secondary utility action, not a second thing to decide between.
- This satisfies the ≥1.5× weight ratio by more than just color/size — it removes Save from the same decision context as Route entirely, which is a stronger hierarchy signal than making it smaller in the same row would have been.
- Both remain ≥44pt targets (PRD req 4, Fitts's Law) and neither sits within a mis-tap radius of the other, precisely because they're in different regions of the sheet.

### 2.3 `ui-design-review` pass — applied, not cited

Run against `passenger-brain/design/reference/ui-ux-design-principles-manual.md` (the vendored manual the skill points to) and `design/design-principles.md` (Passenger's own platform-adapted quick-reference), directly against this spec and the published mockup. Output in the skill's own format:

**Passes**
- **Button/Action Hierarchy (manual Ch3 "Button and Action Hierarchy," Ch7 "Buttons"):** Route and Save map cleanly onto the manual's own two-tier definitions, not just a spatial trick. Route is styled **Primary** — solid fill, unique accent color, full-width — one per view, as the rule requires. Save's default (unsaved) state — `border:1.5px solid var(--border)`, transparent-ish background, no fill — is exactly the manual's **Secondary** tier definition ("outline with border, transparent background"). So the demotion isn't just "smaller and to the side": Save is a different, lower button tier by the manual's own vocabulary, and Route is the only element on the sheet styled as Primary.
- **Von Restorff numeric thresholds (manual Ch9, "unique color… 1.5x the size… 4.5:1 contrast"):** checked against actual dimensions, not asserted. Route spans the sheet's full width (~322pt on a 390pt-wide phone, minus phone-frame and sheet-body padding) at 52pt tall; Save is a 44×44pt circle — roughly an 8x width difference, clearing the 1.5x minimum by a wide margin. Route is the only **filled** use of `--primary` in either sheet — a solid 322×52pt block of color — while every other use of that token (Save's saved-state tint/border, the empty-CTA text) is a thin outline, soft background, or plain text, none of which compete with Route's dominant fill for attention. Contrast of the button label against its fill was computed in both themes (§4) and clears 4.5:1 in both.
- **Never-color-alone (manual Ch14 "Don't Rely on Color Alone"; design-principles.md §3):** the tourist-heavy flag line pairs an icon with text, never a bare color chip (also required directly by `tourist-trap-flag` req 6). Category is a glyph + word everywhere, never a color swatch alone. Save's state change pairs a border-presence change with the tint, not tint alone.
- **Empty state structure (manual Ch7 "Empty States"):** the manual's baseline shape — icon + description, centered — is present in both the "no blurb" and "no places" variants.

**Issues found, and fixed in this same pass (not deferred)**

1. **Toggle-button icon swap (manual Ch14 "Toggle Buttons with `aria-pressed`" — "don't change the button's label between states, let `aria-pressed` communicate it"):** the mockup's first draft swapped the Save icon to a checkmark (✓) when saved. A checkmark reads as "confirmed/done," not "saved" — a meaning swap, not just a style change, and exactly the pattern the rule warns against. **Fixed:** the mockup now keeps the 🔖 glyph constant in both states and communicates state only through the tint/border change plus a real `aria-pressed="true"/"false"` attribute that flips on toggle. §2's Save action row and the mockup source were both updated. (The real SwiftUI build should use `bookmark`/`bookmark.fill` — an outline-to-filled variant of the *same* icon, which is the idiomatic native equivalent and doesn't reintroduce the meaning-swap problem, since it's a weight change within one icon family, not a different symbol.)
2. **Empty state with no path forward (manual Ch7 "Empty State Design" — "don't show just the text '[empty]' without a path forward"; design-principles.md §4 — "illustration + one-line description **+ a CTA** — not a blank view"):** the first draft's "no places curated here yet" empty state had no CTA at all, reasoning there was "nothing actionable." That reasoning doesn't hold up against either source, both of which name a CTA as part of the baseline shape, not an optional extra. **Fixed:** added a real, honest CTA — "Explore another Hood" — that dismisses the sheet back to the map. It isn't a manufactured action: some users may not know the drag-handle swipe dismisses a sheet, so an explicit, visible way back is a genuine path forward, not a fake button added to satisfy a checklist. §3's Hood sheet state table and the mockup were both updated. (This CTA is itself the subject of issue 5 below — its own hit area needed a fix once `design-approval` checked it against Fitts's Law.)

**Additional issues found — not by this section's self-review, but by `product`'s `design-approval` gate (2026-07-30 REJECT), fixed in this same resubmission pass rather than deferred:**

3. **Backdrop swallowed every tap over the map (manual Ch13 "Background Interaction"; PRD req 1 "map stays visible and interactive behind it"):** the mockup's full-surface `.sheet-backdrop` intercepted all clicks whenever a sheet was open, and §2 named no real SwiftUI mechanism for background interaction. **Fixed:** §2's Hood sheet and Place detail modal container rows now name `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` explicitly, including the depth-1-vs-depth-2 distinction; the mockup's backdrop no longer intercepts taps, and a tap on the exposed map now visibly reaches it (simulated via a toast) rather than doing nothing or dismissing the sheet. See §1's dismiss-gesture note.
4. **Save state reset on every reopen (manual Ch14 "State Persistence"; PRD req 7 "visible on reopen"):** `state.saved = false` ran unconditionally on every open, so a previously-saved place always looked unsaved again. **Fixed:** the mockup now reads a per-place saved-state store on open instead of hardcoding `false`; §3 gained an "already saved, reopened" row. See the Save action row in §2.
5. **Two controls below the 44pt minimum (manual Ch13 "Touch vs Pointer Targets"; design-principles.md §2, Fitts's Law):** `.sheet-close` (32×32pt) and the empty-state CTA (32pt min-height) were both under-sized, and §4's touch-target bullet only checked Save and Route. **Fixed:** both now have a 44pt tap target while keeping their small visual glyph/text unchanged — the same "small glyph, full hit-area" pattern `map-rendering-spec.md` §4 already uses for map pins. §4 now enumerates every interactive control, not just the two primary ones.

**Quick wins considered, not applied (and why)**
- **Icon-only Save has no visible text label** (manual Ch7 Buttons: "do not use icons without text labels unless universally understood — close/hamburger/search"). Bookmark/save isn't on that short exception list. Considered adding a visible "Save" text label next to the icon, but rejected it: it would sit in the header, competing for space with the place name and dismiss control, and every major map/travel app (Apple Maps, Google Maps) ships this exact icon-only pattern at this exact location. Mitigated instead through what the manual's own accessibility chapter (Ch14) requires regardless: a persistent `aria-label`/VoiceOver label ("Save"/"Saved") so the control is never unlabeled to assistive technology, just visually icon-only to sighted users. Documented here as a deliberate, cited trade-off rather than silently deviating from the manual.

---

## 3. Every state

Per design-principles.md §4 and the PRD's own P0 requirements 1–2, 5, 7:

### Hood sheet

| State | Behavior |
|---|---|
| **Loading** | Hood and place data is static, cached curated content (PRD's tech design: "no Realtime, no hour-binding") — the sheet opens instantly from cache in the overwhelming majority of cases. If a fetch is genuinely still in flight past ~400ms (Doherty, design-principles.md §2), the sheet still opens immediately with header + blurb visible and the place list showing a brief skeleton-row treatment, never a spinner blocking the whole sheet. |
| **Empty (no blurb, places exist)** | Blurb section is omitted entirely — place list starts directly under the header, no gap, no "coming soon" text (PRD req 2, hard requirement). |
| **Empty (no curated places)** | Plain empty state: icon + "No places curated here yet." + a real CTA, "Explore another Hood," that dismisses the sheet back to the map. No error styling (design-principles.md §4, PRD req 2). **The CTA was added at the `ui-design-review` pass (§2.3, issue 2)** — the first draft omitted it, which neither design-principles.md §4 nor the manual's own Empty State rule (Ch7) allows; "nothing actionable" wasn't a real exemption once checked against the source rather than asserted. |
| **Empty (neither blurb nor places)** | The no-places empty state alone; blurb section stays fully absent rather than rendering its own separate empty copy — one empty state per sheet, not two stacked ones. |
| **Error (Hood data unreachable)** | Distinct from Empty: a plain banner ("Couldn't load this Hood's details right now") replaces the blurb region; the place list still renders whatever is cached, if anything. Never presented as a blocking dialog. |
| **Offline** | Same as Error if nothing is cached yet; if a prior fetch succeeded, the sheet renders normally from cache with no visible distinction — this is static reference data, not something that goes stale meaningfully within a session. |
| **Permission-denied** | Not applicable — the Hood sheet has no permission gate of any kind. |

### Place detail modal

| State | Behavior |
|---|---|
| **Loading** | Same reasoning as the Hood sheet — cached static data, effectively instant. No spinner for a sub-400ms wait. |
| **Already saved, reopened** *(added at this pass — REJECT finding B2)* | The Save button renders in its saved visual state (`--primary` tint + border, per §2.2/§2.3) immediately on open, read from a per-place saved-state source at open time — never defaulted to unsaved. Its accessibility label reads "Saved," not "Save," from first render. No entrance animation distinguishes this from a fresh unsaved open; the persisted state itself is the only signal, consistent with §2.3 issue 1's "state via tint/`aria-pressed`, not icon swap" rule (PRD req 7). |
| **Empty (no P1 fields curated)** | Hours/photo (P1, nice-to-have) simply don't render when absent — no gap, no placeholder icon standing in for a photo. Name and category are always present (data contract guarantees exactly one category per place), so there is no "missing core info" case to design for. |
| **Error (place data fails to resolve)** | Plain "Couldn't load this place" message in place of the body content, with dismiss still available — returns to whichever depth opened it. |
| **Offline** | Place info (name, category, flag line) renders from cache normally. Save still responds instantly, writing locally first (PRD tech design). Route remains available — the deep link into Maps/Waze doesn't require Passenger's own connectivity, only the destination app's. |
| **Route unavailable** | Button renders disabled with plain inline text ("No route app is available on this device") rather than crashing or silently failing (PRD req 5). This is a defensive/edge state — Apple Maps ships on every iOS device and can't be uninstalled, so this state is realistically unreachable in production, but the PRD requires it be handled rather than assumed impossible. |
| **Permission-denied** | Not applicable — opening this modal and using Save require no permission; the Route hand-off's own location behavior belongs to Maps/Waze, not Passenger. |

---

## 4. Accessibility notes

- **VoiceOver labels, every row and control:**
  - A Hood sheet place row announces name + category — "Port Said, Eat & Drink" — matching the exact pattern `map-rendering-spec.md` §7 already establishes for map pins, so the same place reads identically whether discovered on the map or in a list.
  - The Save button always has an explicit accessibility label reflecting its current state — "Save" / "Saved" — never relying on the icon alone (design-principles.md §3, "placeholder/icon-as-label is banned" applied to icon-only buttons the same way it applies to text fields).
  - The tourist-heavy flag line, when present, is exposed to VoiceOver as ordinary accessible text in the modal's normal reading order — `map-rendering-spec.md` §7 already establishes that "the flag is available once the spot sheet opens, same as for sighted users," so no special spoken-vs-visual divergence is needed here the way the map surface needs one. This spec doesn't invent combined phrasing (e.g. with a "busy" state) — that VoiceOver detail belongs to T-035, same as the visual detail does.
- **Dynamic Type:** Hood name, blurb, place rows, category row, and the flag line all use semantic text styles (`.title2`, `.body`, `.subheadline`) — never a fixed point size. At the largest accessibility sizes, place rows grow in height and wrap rather than truncate; the category word is never clipped to make room for a fixed-width glyph.
- **Contrast (WCAG AA, design-principles.md §5):** the flag line's accent color and the Save button's "saved" tint were checked against both light and dark surface tokens and clear 4.5:1 — this spec deliberately avoids the mistake carried forward from T-031's `design-approval` (a colored link token that passed light-mode contrast but failed dark-mode at 3.28:1): no colored body text in this mockup uses a token that hasn't been checked in both themes, and the mockup's own dev-annotation overlays (which do reuse a link-styled accent) are explicitly reviewer-only chrome, never shipped UI, so they don't carry the same obligation.
- **Touch targets — every interactive control in both sheets, enumerated (fixed and completed at this pass; REJECT finding B3 was that only two of six controls were checked):**
  - Save (icon-only, 44×44pt) and Route (full-width, 52pt tall) — both ≥44pt, unchanged from the original submission.
  - **Sheet dismiss (✕), both sheets** — was 32×32pt with no expanded hit area (a Fitts's Law violation). Now a 44×44pt tap target with the same 32pt visual circle centered inside it — small glyph, full-size hit area, `map-rendering-spec.md` §4's own pattern.
  - **Hood empty-state CTA ("Explore another Hood")** — was 32pt min-height. Now 44pt min-height via invisible padding; the visible text stays its original 13.5pt size since the control has no background/border to visually enlarge.
  - **Hood/place rows** — already ≥44pt tall per §2's Place list row.
  - Because Save lives in the header and Route anchors the bottom, there is no shared edge where a slightly-off tap could hit the wrong one; the two 44pt dismiss/CTA fixes above don't introduce any new shared edges either.
- **Reduce Motion:** the stacked-sheet presentation (Hood sheet → Place modal) and the action-sheet hand-off both honor Reduce Motion — cross-fade/appear near-instantly rather than skipping the state change outright, consistent with T-031's precedent.

---

## 5. PRD traceability

| PRD requirement | Where this design satisfies it |
|---|---|
| P0-1 Hood sheet opens in one tap, map stays visible, dismiss restores camera/hour | §1 Flow; §2 Hood sheet container row (`.presentationBackgroundInteraction(.enabled(upThrough: .medium))`, named explicitly — fixed at this pass, was previously asserted with no mechanism, REJECT finding B1) |
| P0-2 Hood sheet content (name, blurb, place list, empty states) | §2 Hood sheet header/blurb/place list rows; §3 Hood sheet state table (all four empty/error/offline variants) |
| P0-3 Place detail modal content, opens directly on one tap (pin or Hood-sheet row), never a two-step preview | §1 Flow (both entry paths); §2 Place detail modal container row |
| P0-4 One primary action, Save not primary, ≥44pt targets | §2.2 Action hierarchy; §2 Save action / Route action rows; §4 Touch targets (all six controls enumerated, fixed at this pass — sheet-close and empty-CTA were previously under 44pt, REJECT finding B3) |
| P0-5 Route hands off to native Maps/Waze, walking mode, no in-app navigation, return restores state, unavailable state is disabled not a crash | §1 Flow (Route hand-off branch); §2 Route action row (walking mode now stated explicitly, not just named once in §0 — fixed at this pass); §3 Place modal "Route unavailable" state; §8 item 2 |
| P0-6 Exactly two categories, new names, distinguishable without color | §2.1 Category rename; §2 Category row / Place row (shared glyph vocabulary with `map-rendering-spec.md` §4 — landmark glyph 🏛️ replaces a generic pin, fixed at this pass) |
| P0-7 Save writes to manual "Saved" path only, visible on reopen, succeeds even for permanently-closed places | §2 Save action row (writes locally first, instant; reads from a per-place saved-state source on open — fixed at this pass, was previously hardcoded unsaved, REJECT finding B2); §3 "already saved, reopened" row; **the permanently-closed badge itself is out of scope here** — owned by `places-been-saved` per the PRD's own Not-in-scope line; this spec only confirms Save's success path doesn't block on closed status, since nothing in this modal reads or renders that field |
| P1 Opening hours / photo, if curated | §3 Place modal "Empty (no P1 fields curated)" row |
| P1 Hood sheet grouping by category | **Not built into this pass** — the mockup and this spec show a flat list; grouping is a P1 nice-to-have, not required for `design-approval`, and can be layered on without changing any P0 structure above |
| (Cross-PRD) `tourist-trap-flag` req 6 — one text line, exact string, condition | §0 Scope discipline; §2 Tourist-heavy flag line row — placement/string/condition only, explicitly not the full T-035 design |

---

## 6. Mockup

Interactive HTML/CSS/JS artifact, published as a Claude Artifact: **https://claude.ai/code/artifact/06f8a49b-7de4-430f-a701-96279db74611**

What it demonstrates, live:
- **Two entry paths** — tapping a Hood shape opens the Hood sheet (depth 1); tapping a pin directly opens the place modal directly (depth 1, skipping the Hood sheet); a live breadcrumb above the phone frame tracks depth (0/1/2) so a reviewer can confirm the 2-level ceiling is never exceeded.
- **Hood sheet content states** — full (blurb + place list), no-blurb, no-places (empty, now with a real "Explore another Hood" CTA per §2.3), and error/offline, switchable via the rail without leaving the current Hood.
- **Place modal content states** — default, flagged (tourist-heavy, with the T-035 placeholder marked inline when "design annotations" is on), route-unavailable (disabled button + inline text), and offline (cached-data banner, Save and Route both still functional).
- **The action hierarchy itself** — Route as the sole bottom-anchored filled button (manual's Primary tier); Save as a small header-right icon toggle styled as the manual's Secondary tier, spatially separated rather than color-differentiated alone. Save's icon stays constant across states (`aria-pressed` flips, the glyph doesn't) — see §2.3, issue 1.
- **Route hand-off simulation** — tapping Route opens a native-style action sheet (Maps / Waze), picking either shows a brief "Handing off…" toast, then simulates the return to Passenger with both sheets closed and the map breadcrumb reset to depth 0, per req 5.
- **Category rename** — every place row and the modal's category row read "Eat & Drink" / "Things to do," never the retired "Food & drinks."
- **VoiceOver label preview toggle** — surfaces the spoken string per row/control, same convention as T-031's mockup.
- **Design annotations toggle** — reviewer-only dashed captions marking exactly which pieces are placeholders (the T-035 flag slot) versus fully resolved by this spec.
- Both light and dark themes, palette consistent with `design/mockup-prompts.md`'s Block A and T-031's mockup.

Deliberately **not** in the mockup: quick-filter chips (T-038's), Places-list rows/provenance words/closed badge (`places-been-saved`'s), any Scenic/Fast route selection or polyline (excluded by this PRD, PAS-7), search, Passport, live events. The map background shown behind the sheets is a minimal stub matching T-031's established visual language, not a re-design of the map itself.

---

## 7. Principles conformance

| Call this spec makes | Citation |
|---|---|
| Route is the modal's one filled, full-width (~8x Save's width), bottom-anchored action, styled with the app's accent color as its only solid fill in either sheet (the same token appears elsewhere only as an outline/tint/text color, never another fill — corrected wording, §2.3); Save is a small icon-only header toggle spatially separated from it | design-principles.md §2, Von Restorff; manual Ch9 "Von Restorff Effect" (unique color + ≥1.5x size + 4.5:1 contrast — all three checked numerically in §2.3, not asserted) |
| Route = manual's **Primary** button tier (solid fill); Save's unsaved state = the manual's **Secondary** tier (outline, transparent) — a tier difference, not just a size/position difference | design-principles.md §2 ("3-tier action hierarchy: filled/tinted/plain"); manual Ch3/Ch7 "Button/Action Hierarchy" |
| Save, Route, both sheets' ✕ dismiss, and the Hood empty-state CTA are all ≥44pt hit areas (dismiss/CTA fixed at this pass via invisible padding, no visual size change), and none share an edge a mis-tap could cross | design-principles.md §2, Fitts's Law; manual Ch13 "Touch vs Pointer Targets" (44-48px touch minimum) |
| The map stays visible and interactive behind the Hood sheet and the depth-1 Place modal via `.presentationBackgroundInteraction(.enabled(upThrough: .medium))`, named explicitly; the depth-2 stacked Place modal deliberately does not cascade that interaction to the map, since presentation depth doesn't inherit it automatically | design-principles.md §2 (map-first, PRD req 1); manual Ch13 "Background Interaction" — fixed at this pass, was previously asserted with no mechanism and contradicted by the mockup's own full-surface backdrop (REJECT finding B1) |
| Route's hand-off always requests walking directions, regardless of which app or code branch is used | PRD req 5's own bullet; threaded through §2/§5/§8 at this pass, was previously named once in §0 and dropped everywhere else (REJECT should-fix #6) |
| Sub-400ms opens show no spinner; Save responds optimistically inside the same budget | design-principles.md §2, Doherty Threshold; manual Ch9 "Doherty Threshold" (don't show a spinner under 400ms — causes perceived slowness) |
| Place row / category row / map pin all share one glyph vocabulary, never color-only | design-principles.md §3 (iOS translation: "never rely on color alone"); §5 accessibility; manual Ch14 "Don't Rely on Color Alone" |
| Route button sits bottom-anchored, in the thumb zone | design-principles.md §3, Thumb Zone; manual Ch13 "Thumb Zone" (bottom 1/3) |
| Every state — loading, empty (two variants, both now with a CTA per §2.3), error, offline, permission-denied (n/a, stated explicitly) — specified rather than left to the developer | design-principles.md §4; manual Ch7 "Empty State Design" |
| Contrast: flag line and Save "saved" tint checked at 4.5:1 in both themes; no repeat of T-031's carried-forward dark-mode token defect | design-principles.md §5, WCAG AA; manual Ch14 "Text Contrast Ratios" |
| No confirmation dialog inserted before the Route hand-off | design-principles.md §2, Poka-Yoke / Undo-over-confirmation — hand-off is the expected, common action of a map app, not a destructive one; adding a confirm step would be friction with no error it prevents |
| Icon-only Save carries an explicit accessibility label, and toggles via a real pressed-state rather than swapping to an unrelated icon | design-principles.md §3, placeholder/icon-as-label ban; manual Ch14 "Toggle Buttons with aria-pressed" (§2.3, issue 1's fix) |
| Icon-only Save has no visible text label, which the manual's Button chapter generally discourages outside a short exception list | Deliberate, cited trade-off — §2.3 "Quick wins considered, not applied," not a silent deviation |
| Hick's Law / Miller's Law | Not applicable — this task has exactly two actions and no multi-item decision or list-chunking surface; flagging the omission rather than citing a section that doesn't apply, same convention T-031 used |

No Section 2/3/5 area relevant to this feature was left unaddressed: Hick's/Miller's are the only rows without a live decision to cite against, recorded above rather than silently skipped. §2.3 documents the `ui-design-review` skill actually being run against this spec and mockup — five real issues found and fixed across the two review passes (2 from the original `ui-design-review` self-review, 3 from `product`'s `design-approval` REJECT), one trade-off found and consciously kept, one wording/arithmetic correction, not merely cited in passing.

---

## 8. Open items handed to `architect` / `ios-developer`

Not blocking `design-approval`, flagged for the TRD:

1. **Sheet-over-sheet presentation** (§2, Place detail modal container) — whether presenting the Place modal from within an already-open Hood sheet needs a different SwiftUI presentation approach than presenting it directly from the map view, so both entry paths behave identically (detents, dismiss gesture, backdrop). This spec assumes native support is sufficient; `architect` should confirm before `ios-developer` builds against that assumption.
2. **Route action-sheet vs. direct open, and walking mode on both branches** (§2, Route action row) — whether the app-chooser is a genuine action sheet (when both Maps and Waze are installed) or a direct deep-link when only one is present is a build-time branching detail this spec doesn't fully resolve, since either satisfies PRD req 5 as written. **Threaded through explicitly at this pass** (was named in §2's Route action row and §5's traceability but not carried here, leaving the cross-reference those two rows make to "§8 item 2" pointing at nothing): whichever branch `ios-developer` implements, the deep link's mode parameter must be fixed to walking — this isn't optional or a second decision layered on top of the action-sheet-vs-direct-open call, it applies identically to both branches.
3. **Category enum enforcement** — carried over from the PRD's own open technical question: whether the two-value category enum is enforced in Postgres or client-side only, and whether "Eat & Drink" is stored as display text or a stable key. Not a design-time call.
4. **Hood-sheet-to-place-modal data fetch** — whether tapping a place row needs a fresh fetch or reads from the same cached payload the Hood sheet already loaded; this spec assumes the latter (consistent with "no Realtime, no hour-binding" in the PRD's tech design) but doesn't specify the exact caching mechanism.
