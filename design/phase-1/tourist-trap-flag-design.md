# Tourist-Trap Flag & Local QA — Design Spec

**Task:** T-035 · **PRD:** [`prds/tourist-trap-flag/tourist-trap-flag.md`](../../prds/tourist-trap-flag/tourist-trap-flag.md) (Draft v1)
**Mockup:** https://claude.ai/code/artifact/40b9ec94-b831-4d20-a334-fb95bf5f4cbd — interactive HTML/CSS/JS, click-through, no build step
**Owner:** designer · **Date:** 2026-08-02 · **Status:** ready for `design-approval`
**Research note:** Mobbin MCP is listed as requiring authorization on this workspace's connector (same standing block T-031/T-033 hit). Proceeded from the PRD, `design/ux-flows.md` §6/§9, `design/map-rendering-spec.md` §§2–4/§7, and `design/design-principles.md` instead, per the standing "don't block" rule for this research step.
**Figma note:** not attempted. The 2026-07-22 founder ruling makes the HTML artifact the default deliverable, and this task didn't request Figma output.
**Consistency check:** built against the real, already-shipped code this feature slots into — `passenger-code/Passenger/Hoods/Hood.swift` (`isTouristTrap: Bool?` already exists, landed by T-040's Phase-1 carve-out), `Passenger/Map/HoodLayer.swift` (the Hood polygon's stroke is currently one constant value, `.secondary.opacity(0.35)` at 0.5pt, for every Hood regardless of flag — this spec is what makes it vary), and `Passenger/Detail/PlaceDetailModal.swift` (`touristTrapSlot` is a named, currently-empty placeholder this spec fills). Palette (`--bg`/`--surface`/`--fg`, heat accent `#E24E1F`/`#FF7A4D`) carried forward from `design/mockup-prompts.md`'s Block A and T-031/T-033's mockups, so this reads as the same app.

---

## 0. Scope discipline

This spec covers exactly the four surfaces the PRD hands off, no more:

1. Hood outline stroke — flagged / not-flagged / busy+flagged, by zoom tier (PRD req 2, 3, 5)
2. Hood centroid label wording, when the flag renders one (PRD req 3)
3. Place-detail-modal flag line — fills T-033's `touristTrapSlot` (PRD req 6)
4. Local-QA toast — binary Yes/No, top-anchored, non-blocking (PRD req 8)

**Deliberately absent, matching the PRD's own "Not in scope" line:**
- **The algorithm that proposes a flag value** — `data-eng/discovery-engine-spec.md`, `data-engineer`'s. This spec designs for the flag existing as a nullable boolean per Hood/place, seeded with plausible fake values for the Phase-1 demo.
- **Heat rendering itself, the Hood/place sheets' other content, the Places list, Passport** — T-031/T-033/T-036/T-037's, already built or specced.
- **A "hide tourist-heavy spots" filter** — `ux-flows.md` §6 makes that a fresh decision, not this task's.
- **Reward for answering local-QA** — open question, Aviran's (PRD Open questions & risks).
- **The permission sequence itself** (Location Always, Notifications) — `ux-flows.md` §3/§9 Q10 own that; this spec assumes the toast is reachable and designs only what renders once it is.

---

## 1. Flow

This task has no new navigation depth of its own — it adds content to two existing surfaces (the Hood polygon's stroke, T-033's place modal) and one wholly new, push-triggered surface (the toast) that isn't part of the sheet/depth model at all.

**Surface 1 — Hood stroke (ambient, 0 taps, part of the always-on map):**
```
Map, any zoom
  City-wide         → no stroke, no label, on any Hood (flagged or not)
  Neighborhood zoom → flagged Hoods: stroke + centroid word label ("Tourist-heavy spot" / "Busy and tourist-heavy")
                     → not-flagged / not-yet-rated: unchanged thin neutral boundary, no label
  Close zoom        → flagged Hoods: stroke persists, label drops · pins appear, carry no flag signal (unchanged, map-rendering-spec.md §4)
```
Tapping a Hood still opens its sheet directly (T-031/T-033's flow, unchanged) — the stroke is read-only, ambient information, never itself a tap target beyond the Hood polygon's existing hit area.

**Surface 2 — Place-detail-modal flag line:**
```
Place modal opens (T-033's flow, either entry path, unchanged)
  → flagged: one line renders between the category row and the route button — icon + "Tourist-heavy spot"
  → not flagged: nothing renders there — the slot stays visually silent, same footprint as before this task
```

**Surface 3 — Local-QA toast, entirely push-triggered, no user-invoked entry point:**
```
Geofence-verified dwell at a tagged place (data-engineer's detector, shared with Places/Passport)
  → at most one local notification fires (Notifications granted, first time for this place)
  → user taps the notification → app foregrounds to whatever it was last showing
  → toast drops from the top, over whatever's on screen (map, an open sheet, another modal) — not a sheet, not part of the {search / heat / Places / Profile} exclusivity set
  → Yes / No → collapses into a one-line thanks (or an offline-queued variant) → disappears
  → ignored → auto-dismisses on its own after ~5s, no reminder for this visit
  → Notifications denied, or this place already answered by this install → no toast, ever; no fallback anywhere else in the app
```
There is no dismiss gesture to design beyond "ignore it" — the toast never blocks, so there's nothing to swipe away that the user couldn't just tap through.

---

## 2. Screens & components

| Component | What it is | SwiftUI-native pattern |
|---|---|---|
| **Hood flag stroke** | The Hood polygon's own stroke, made to vary by `isTouristTrap` and the current hour's `HeatBand`, instead of the constant value `HoodLayer.swift` renders today | `HoodLayer`'s `MapPolygon(...).stroke(...)` call becomes a function of three inputs already available to it or one hop away: `hood.isTouristTrap` (already on the `Hood` model), the Hood's current `HeatBand` (already passed in as `band`), and the existing `showsNames` zoom gate. Not-flagged/not-yet-rated (`isTouristTrap != true`) keeps exactly today's `.stroke(.secondary.opacity(0.35), lineWidth: 0.5)` unchanged — this constant is identical on every Hood regardless of flag, so it carries zero information and doesn't violate PRD req 4's "not-flagged renders no stroke" as a signal. Flagged (`isTouristTrap == true`, `band != .busy`): `.stroke(Color("Flag"), lineWidth: 2.5)`, solid. Flagged + busy (`isTouristTrap == true`, `band == .busy`): `.stroke(Color("Flag"), style: StrokeStyle(lineWidth: 3, dash: [6, 4]))` — **replaces the plain flagged stroke outright, never both** (PRD req 5, one `if/else`, not two conditions that could both fire). |
| **Flag accent color** | New semantic color, not reused from `HeatPalette` or any existing token | New entry in the asset catalog, `Color("Flag")` — light `#A15C00`, dark `#F0B429` (light/dark variants, per design-principles.md §3's semantic-color-set rule). Distinct hue from the heat accent (`#E24E1F`/`#FF7A4D`) so the two channels never read as one signal even where they're adjacent on screen — heat is always the fill, flag is always the stroke (PRD req 2), and this color choice makes that true perceptually too, not just structurally. Checked, not asserted — see §2.3. |
| **Zoom tier for the flag label — a new threshold, not the existing one** | `showsNames` (`MapScreen.swift`, `nameLabelSpanThreshold`) today gates the Hood name label **and** spot pins together at one span value — the map-rendering-spec.md §2 table needs a **third**, coarser tier: stroke+label at Neighborhood, stroke-only (label drops) at Close, where pins appear. This spec cannot reuse `showsNames` for the label without either showing the flag label at the same moment pins appear (wrong, contradicts req 3's "close... drops the label") or hiding it entirely (also wrong). | **Flagging for architect/ios-developer (§8):** a second span threshold, coarser than `nameLabelSpanThreshold`, gates the flag's centroid label specifically. The flag *stroke* itself uses the existing `showsNames` threshold (city-wide vs. everything closer) — only the *word label* needs the new, third tier. Exact span value is an implementation call, not a design one, same carve-out T-031 made for heat-band thresholds. |
| **Hood centroid label, combined** | The flag's word doesn't get a second annotation stacked at the same centroid `HoodLayer.swift` already anchors the Hood name to — that would be two text elements competing for one point (Von Restorff, one special element per view; also the exact channel-collision T-031's own design doc flagged as reserved for this task). | `HoodLayer`'s existing name capsule (`Text(hood.name)` in a `.thinMaterial` capsule) gains a second, smaller line **only when flagged and the new label-tier threshold is crossed**: `Text(hood.name).font(.caption.weight(.medium))` unchanged, plus `Text(flagLabelText).font(.caption2.weight(.semibold)).foregroundStyle(Color("Flag"))` beneath it. `flagLabelText` is `"Tourist-heavy spot"` (flagged, not busy) or `"Busy and tourist-heavy"` (flagged + busy) — never both lines' text competing in size or weight with the Hood name above it (name stays visually primary). Not-flagged/not-yet-rated Hoods render the capsule exactly as `HoodLayer.swift` does today — one line, no change. |
| **Place-modal flag line** | Fills `PlaceDetailModal.swift`'s `touristTrapSlot`, currently a bare `EmptyView()` reserved for this task | `HStack(spacing: 6) { Image(systemName: "camera.fill"); Text("Tourist-heavy spot") }.font(.subheadline).foregroundStyle(Color("Flag"))`, rendered between `categoryRow` and `routeButton`, exactly where the placeholder already sits. Conditioned on `place.isTouristTrap == true` — `false` or `nil` render nothing, same footprint the `EmptyView()` already occupies today (PRD req 6, [ASSUMPTION] carried from the PRD, not resolved here — see §9). Icon is new to the app: `camera.fill`, distinct from the fork/knife and landmark glyphs `hood-place-detail-design.md` already established for category, so the flag line never reads as a third category. |
| **Local-QA toast container** | New surface, no existing analog in the codebase — not a `.sheet`, not part of `DetailRouter`'s depth model | A `ZStack` overlay anchored at the app's root view (not scoped to `MapScreen` or any one sheet), so it can render over the map, an open Hood/place sheet, or the heat/search/Profile modals alike — it is not a member of `ux-flows.md` §2.1's modal-exclusivity set `{search, heat, Places, Profile}` and doesn't close or get closed by any of them. Positioned top-anchored, safe-area-respecting, `.transition(.move(edge: .top).combined(with: .opacity))`, honoring Reduce Motion (cross-fade near-instantly instead). Non-blocking: no scrim, no dimming behind it — everything else on screen stays exactly as interactive as it was the instant before the toast appeared. |
| **Toast content** | Question + two buttons | `Text("Does this feel like a tourist-heavy spot?")` (`.subheadline.weight(.semibold)`), then an `HStack` of two `Button`s, **Yes** filled (`.borderedProminent`) and **No** outline (`.bordered`) — equal width, ≥44pt tall each (Fitts's Law). Neither reads as more "correct" than the other by weight/color beyond the ordinary filled/outline pairing already used elsewhere (Route/Save in T-033) — this is a factual either/or, not a recommended-vs-alternative choice, so Von Restorff's "one thing stands out" doesn't apply the way it does to Route. |
| **Toast — answered state** | Collapses in place, doesn't replace itself with a new toast | Both buttons and the question text cross-fade out; a single `Text` reading **"Thanks — shared with other travelers"** (online) or **"Saved on device — will sync once you're back online"** (offline, PRD req 8 bullet 5) fades in for ~1.6s, then the whole toast dismisses via the same transition it entered with. |
| **Toast — ignored** | No visible countdown affordance in the shipped app; the mockup's progress bar is a reviewer aid, not shipped UI | Auto-dismisses on a fixed timer (~5s is this spec's working default — not a PRD-specified number, flagged as an open call for `ios-developer`/`architect` alongside req 8's [ASSUMPTION] cadence question). No reminder, no second toast for the same visit (PRD req 8 bullet 3). |
| **Toast — never renders** | Notifications denied, or this place already answered by this install | Nothing to build beyond correctly *not* triggering the notification/toast pipeline (PRD req 8 bullets 4 and 6) — there is no visual "denied" or "already answered" state inside the app itself; these are absence states, not rendered ones. The mockup's explanatory cards for these two scenarios are reviewer-only annotations, not shipped screens — marked as such in the mockup and not claimed as a real app state in §3 below. |

### 2.1 Copy discipline

Every string this spec renders reads **"Tourist-heavy spot"** or **"Busy and tourist-heavy"** — never "tourist trap," anywhere, in any state, including VoiceOver output (decision #42, PRD req 1 bullet 3). See §2.3 for a real divergence this citation caught in a sibling doc's own example text, fixed here rather than repeated.

### 2.2 Why the stroke and the label are separate design calls

The stroke (PRD req 2) and the word label (PRD req 3) look like one feature but resolve two different problems, and conflating them was the exact mistake `map-rendering-spec.md` §1 documents correcting twice already (badge → stroke → boolean). The **stroke** is what makes the flag legible at a glance without reading anything — it has to survive Florentin at 8pm, dozens of Hoods on screen, without adding a word anyone has to parse. The **label** is a concession to clarity at one specific zoom (Neighborhood) where there's room for it and a genuine reason to spell it out rather than leave a first-time user guessing what an amber line means. Keeping them on two different zoom-gates (stroke: existing `showsNames` tier; label: a new, coarser tier) is what lets the Close-zoom stroke persist for continuity while the label correctly drops — same discipline `map-rendering-spec.md` §2's table already specifies, this spec just names the SwiftUI-level consequence of it.

### 2.3 `ui-design-review` pass — applied, not cited

Run against `passenger-brain/design/reference/ui-ux-design-principles-manual.md` (the vendored manual) and `design/design-principles.md` (Passenger's platform-adapted quick-reference), directly against this spec and the published mockup's actual source (`--flag` tokens, stroke CSS, and rendered copy — grepped, not eyeballed).

**Passes**
- **Never rely on color alone (manual Ch5/Ch14 "Don't Rely on Color Alone"; design-principles.md §3):** flagged-vs-not is a weight+dash change (0.5pt neutral → 2.5pt solid `--flag`), not a hue swap on the same weight — a colorblind or grayscale reading still distinguishes "no stroke" from "stroke present." Flagged-vs-busy+flagged is a dash-pattern change (solid → dashed) at the *same* hue, satisfying PRD req 2 bullet 2 ("weight and/or dash, not hue alone") literally, not just in spirit. The place-modal line pairs an icon (`camera.fill`) with text, never a bare color chip (PRD req 6 bullet 1).
- **Von Restorff (manual Ch9 "Von Restorff Effect" — unique color, ≥1.5× size, 4.5:1 contrast; design-principles.md §2):** the flag stroke (2.5–3pt) against the Hood's own unflagged-baseline stroke (0.5pt) is a 5–6× weight ratio, well past the 1.5× minimum, and `--flag` is used nowhere else in the app's existing palette (checked against `HeatPalette`'s hue and the `--primary` accent used for Save/Route in T-033's spec — no collision). One busy+flagged Hood never shows both the plain and warning stroke at once — checked against the actual CSS (§2's table; `.hood[data-flag="true"][data-busy="true"] .stroke` is the *only* rule that fires for that combination, not an additive second rule stacked on the plain-flagged one).
- **UI Component Contrast (manual Ch14 "UI Component Contrast" — 3:1 minimum for non-text graphical elements) and Text Contrast Ratios (manual Ch14, 4.5:1 normal text; design-principles.md §5):** the flag stroke only needs 3:1 as a boundary line, but the centroid label is real text and needs 4.5:1. Computed, not asserted, against both theme backgrounds the label could sit over: `--flag` light `#A15C00` on bg `#FAF9F6` is **4.93:1**, on surface `#FFFFFF` is **5.19:1**; `--flag` dark `#F0B429` on bg `#121315` is **9.97:1**, on surface `#1A1C1F` is **9.16:1**. All four clear 4.5:1, with margin — the label capsule's `.thinMaterial` background sits between bg and surface in practice, so both bounds being clean means the real rendered case is too.
- **Alert Structure (manual Ch7 "Alert Structure" — icon + text, never color-only, for a status message):** the toast pairs a question with two labeled buttons, never a color-only affordance; the "Thanks —" / "Saved on device —" confirmation is plain text, not a colored badge standing alone.
- **Touch targets (manual Ch12/Ch13, 44–48px min; design-principles.md §2 Fitts's Law):** both toast buttons are ≥44pt tall (checked in the mockup's own CSS: `min-height:44px`), matching the place modal's existing Save/Route/dismiss precedent from T-033.

**Issues found, and fixed in this same pass**
1. **`map-rendering-spec.md` §7's own quoted VoiceOver example violates decision #42.** That doc's accessibility section (written before req 1 bullet 3 and decision #42 were both locked) gives *"Florentin, busy, not a tourist trap"* as its example not-flagged label. That string contains the literal banned phrase — VoiceOver output is spoken to the user, so it's user-facing copy, not internal vocabulary exempt from the ban. **Fixed here:** §4 below defines the actual not-flagged label as **"Florentin, busy, not a tourist-heavy spot"** — same information, compliant copy, consistent with the flagged label's own approved phrasing ("tourist-heavy spot," negated). `map-rendering-spec.md` itself is a locked, shared doc this task doesn't own — flagging the stale example there rather than silently diverging from it (§8) is the honest way to leave this, since a future reader citing that doc verbatim would reproduce the violation.
2. **First pass gave the flag stroke and the flag label the same zoom threshold as pins/Hood name (`showsNames`), which fails PRD req 3 literally.** Req 3's own bullet says Close "keeps the stroke and drops the label" — a single shared threshold can't produce that, since crossing it would turn stroke and label on or off together. **Fixed:** §2's "Zoom tier for the flag label" row names the actual fix (a second, coarser threshold for the label only) rather than leaving the spec internally inconsistent with its own cited requirement — caught by checking the requirement's literal text against the component table, not by re-deriving the rule from scratch.

**Quick wins considered, not applied**
- **A visible countdown affordance on the toast** (so a user glancing at it knows how long before it auto-dismisses) was considered — the mockup includes one as a reviewer aid. Rejected for the shipped app: a countdown bar adds a second thing competing for attention on a surface whose whole design goal is "quiet, ignorable, no obligation" (PRD req 8's ask-once ethics, design-principles.md §2 Poka-Yoke). A user who wants to answer has ~5 seconds either way; a visible timer would read as urgency this ask deliberately doesn't carry. Documented as a deliberate omission, not an oversight — the mockup's own note (§6) says so explicitly rather than presenting it as shipped UI.
- **A stronger, hue-shifted warning color for busy+flagged** (distinct from plain-flagged's amber) was considered, since a warning state often gets its own hue in other systems (manual's Alert Structure table uses a distinct warning hue per severity). Rejected: PRD req 2 bullet 2 requires the flagged-vs-not distinction to survive without hue, and keeping busy+flagged on the *same* hue as plain-flagged (differing only by dash/weight) is what makes "still fundamentally the same flag, just a stronger form of it" legible — introducing a second hue here would imply a third semantic category (a *different* kind of warning) that doesn't exist in the PRD's two-state model.

### 2.4 Artifact conformance check (spec vs. published mockup, both directions)

Checked against the mockup's actual published source, not against what this spec intended to build:
- **No claim without a source line.** The 4.93:1/5.19:1/9.97:1/9.16:1 contrast figures above were recomputed with a WCAG relative-luminance script against the exact `--flag`/`--bg`/`--surface` hex values the mockup ships (`grep`-verified: `--flag:#A15C00` light, `--flag:#F0B429` dark, at the two CSS lines quoted in §2's Flag accent color row) — not asserted from the palette plan alone. The "zero literal 'tourist trap' anywhere" claim in §2.1 was verified with a case-insensitive grep across the published source: zero matches outside this spec document itself.
- **No rendered element without a spec row.** Every DOM element the mockup draws inside the phone frame has a component row above: the Hood stroke/label pair, the pin glyphs (existing, T-031/T-033's, unchanged here), the place-modal flag slot, the toast and its two static-card variants (marked reviewer-only, not shipped states, in the table above). The mockup's zoom-tier buttons, scenario buttons, and theme/VoiceOver/annotation toggles are outside the phone frame — reviewer instrumentation, not app chrome, and not claimed as shipped UI anywhere in this spec.
- No divergence found in either direction this pass — the one thing worth flagging is that the mockup's toast countdown bar is instrumentation-only (§2.3 quick win), and it's labelled as such in the mockup itself, not left ambiguous.

---

## 3. Every state

Per design-principles.md §4 and PRD reqs 4, 8, 9.

### Hood stroke (map surface)

| State | Behavior |
|---|---|
| **Flagged** | Solid 2.5pt `Color("Flag")` stroke at Neighborhood zoom and closer; centroid label ("Tourist-heavy spot") at Neighborhood only. City-wide: no stroke, no label, matching every other Hood (PRD req 3). |
| **Flagged + busy** | Dashed 3pt `Color("Flag")` stroke, **replacing** the plain flagged stroke — never both at once. Label at Neighborhood reads "Busy and tourist-heavy" (PRD req 5). |
| **Not flagged** | Unchanged 0.5pt neutral boundary, at every zoom. No warning treatment even when busy (PRD req 5 bullet 3). |
| **Not yet rated** (`isTouristTrap == nil`) | Renders identically to Not flagged — same stroke, no label, at every zoom. Resolves on tap via the Hood sheet, same convention as every other "no data yet" gap in this product (PRD req 4). |
| **Loading / offline** | Hood geometry and the base 0.5pt boundary are bundled, static data (T-031) — never a loading state of their own. If `isTouristTrap` is momentarily unresolved for any reason, it renders as Not-yet-rated (nil), never a distinct "loading flag" visual. |

### Place-detail-modal flag line

| State | Behavior |
|---|---|
| **Flagged** | Icon + "Tourist-heavy spot," between category row and route button. |
| **Not flagged / not-yet-rated** | Nothing renders — the slot occupies zero visible height, same as `PlaceDetailModal.swift`'s current `EmptyView()` (PRD req 6 bullet 2, [ASSUMPTION] — see §9). |
| **Offline** | Unaffected — the flag is bundled/cached place data, not a live fetch (PRD tech design: "no Realtime, no hour-binding"). |

### Local-QA toast

| State | Behavior |
|---|---|
| **Fires (notification tapped)** | Toast drops from the top, over whatever's currently on screen. Non-blocking — nothing dims, nothing else stops responding to taps. |
| **Answered (Yes or No)** | Collapses to a one-line thanks, disappears after ~1.6s. Recorded as a signal either way, even if it agrees with the current flag (PRD req 9 bullet 3) — not a rendering concern, but worth restating here since it's the reason "No" isn't styled as a correction or an error. |
| **Ignored** | Auto-dismisses after a fixed interval (this spec's working default ~5s — not a PRD-specified number, see §8). No reminder, no second toast for this visit. |
| **Offline** | Renders identically — three fixed words plus a place name already on-device need no network. Answering shows "Saved on device — will sync once you're back online" instead of "shared" (PRD req 8 bullet 5). |
| **Notifications denied** | Never renders. No fallback ask anywhere else in the app — decision #24 replaces the embedded ask, it doesn't supplement it (PRD req 8 bullet 6). Absence state, not a visual one. |
| **Already answered for this place** | Never renders again for it, this install (PRD req 8 bullet 4). Absence state. |
| **Foreground arrival (P1)** | If Passenger is already foregrounded when the geofence fires, the same toast component can drop directly, skipping the system notification — no new component, just a different trigger path (`ux-flows.md` §4 Journey 4 step 2's `[design call]`). Not required for `design-approval`. |

---

## 4. Accessibility notes

- **Hood VoiceOver labels — every state says its status explicitly in speech**, per `map-rendering-spec.md` §7's resolution (VoiceOver can't perceive an absent stroke, so silence isn't a valid "not flagged" signal). Exact strings, all using approved copy only (see §2.3 issue 1's fix — none of these say "tourist trap"):
  - Flagged, not busy: *"Florentin, quiet, tourist-heavy spot."*
  - Flagged + busy: *"Kerem HaTeimanim, busy and tourist-heavy — worth a second look"* (own combined label, not two announcements left for VoiceOver to merge — PRD req 7 bullet 2, `ux-flows.md` §9 Q5).
  - Not flagged: *"Neve Tzedek, busy, not a tourist-heavy spot."*
  - Not yet rated: *"Bavli, quiet, no local rating yet."*
  - These labels extend `HoodLayer.swift`'s existing `voiceOverLabel` computed property (currently `"\(hood.name), \(band.spokenWord)"`) with one more clause — not a parallel, separate label system.
- **Pins never announce the flag** — unchanged from `map-rendering-spec.md` §7; a pin's label stays "name, category" only.
- **Place-modal flag line** is exposed as ordinary accessible text in the modal's normal reading order when present — no special spoken-vs-visual divergence needed, matching `hood-place-detail-design.md` §4's existing treatment of this exact slot. Silent when absent, same as visually.
- **Toast announcement.** The toast is the one surface in this spec with no directly-matching manual citation — it's a passively-appearing, non-modal element triggered by a system event, not a dynamically-loaded content region (manual Ch14's "Focus Management After Dynamic Content Load" is the closest rule and doesn't quite fit: that rule is about moving keyboard focus after a user-initiated load, not about announcing an unsolicited arrival). Named as a genuine gap rather than forcing a citation: **`ios-developer` should post an accessibility notification** (`UIAccessibility.post(notification: .announcement, argument: "Does this feel like a tourist-heavy spot?")`, or the SwiftUI `AccessibilityNotification.Announcement` equivalent) the moment the toast appears, since a VoiceOver user has no other way to discover it arrived — flagged in §8, not resolved as a citation this spec doesn't have.
- **Toast buttons** carry explicit labels — "Yes" / "No" — read together with the question text preceding them in VoiceOver's reading order, so neither button is ambiguous in isolation.
- **Dynamic Type:** the flag's centroid label and the place-modal line both use semantic text styles (`.caption2`, `.subheadline`) per design-principles.md §3 — never a fixed point size. At largest accessibility sizes, the centroid label's two lines wrap rather than truncate, same as the Hood name capsule already does.
- **Reduce Motion:** the toast's slide-in/out and the stroke/label's zoom-triggered appearance both honor Reduce Motion — cross-fade near-instantly rather than skipping the state change outright, consistent with T-031/T-033's precedent.

---

## 5. PRD traceability

| PRD requirement | Where this design satisfies it |
|---|---|
| P0-1 One boolean per Hood/place, no graduated value, no banned tag strings, Hood flag never aggregated | §2 Hood flag stroke row (reads `hood.isTouristTrap` directly, already a plain `Bool?`); §2.1 copy discipline; §2.3 issue 1 (banned-phrase fix) |
| P0-2 Flag never shares a visual channel with heat; weight/dash not hue alone; slider repaints heat, never the stroke | §2 Flag accent color row (new hue, stroke-only, never a fill); §2.3 Passes (weight/dash checked, not hue); §3 Hood stroke states (no time/hour-binding on any state) |
| P0-3 Zoom disclosure matches map-rendering-spec.md §2's table, row for row; no pin ever carries the flag | §1 Flow (Surface 1); §2 Zoom tier row + Hood centroid label row (new threshold flagged for req 3's exact behavior); §3 Hood stroke states |
| P0-4 Not-flagged and not-yet-rated both render blank; storage still distinguishes them | §3 Hood stroke states ("Not flagged" / "Not yet rated" rows, visually identical, resolved by the existing Hood-sheet-on-tap flow) |
| P0-5 Busy+flagged replaces, never stacks; its own distinct label; busy-not-flagged gets no warning | §2 Hood flag stroke row (one `if/else`, not two conditions); §2.3 Passes (checked against the mockup's actual CSS rule); §4 combined VoiceOver label |
| P0-6 One text line in the place modal, nowhere else; independent of the closed badge | §2 Place-modal flag-line row; §3 Place-detail-modal-flag-line states; §0 scope discipline (closed badge explicitly T-036's) |
| P0-7 VoiceOver states the flag even when nothing renders, in both states; not-yet-rated says so distinctly; busy+flagged gets its own label; pins never announce it | §4 Accessibility notes (all four Hood label strings, extending `HoodLayer.swift`'s existing property) |
| P0-8 Local-QA ask: binary, post-visit, once; ignored auto-dismisses with no reminder; answered-once install never fires again; offline still renders and queues; notification-denied has no fallback anywhere | §1 Flow (Surface 3); §2 Toast rows; §3 Local-QA toast states (all six rows) |
| P0-9 One answer is a signal, not a direct write to the rendered flag; recorded even if it agrees | §3 "Answered" state row (styling doesn't distinguish agree/disagree, matching req 9's "not a correction" framing) |
| P1 Hood sheet place list marks flagged places | **Not built into this pass** — P1, not required for `design-approval`, and no component in T-033's existing Hood sheet reserves a slot for it the way `touristTrapSlot` does for the modal. |
| P1 Foreground arrival drops the toast directly | §3 "Foreground arrival (P1)" row — same component, different trigger, not blocking. |

---

## 6. Mockup

Interactive HTML/CSS/JS artifact, published as a Claude Artifact: **https://claude.ai/code/artifact/40b9ec94-b831-4d20-a334-fb95bf5f4cbd**

What it demonstrates, live:
- **Three tabs** — Map (Hood stroke), Place detail modal, Local-QA toast — switchable without losing state, each with its own control rail below the phone frame.
- **Map tab:** a zoom-tier control (City-wide / Neighborhood / Close) driving the exact PRD req 3 table — no stroke/label at City-wide on any Hood; stroke + label on flagged Hoods only at Neighborhood; stroke persists and label drops at Close, where pins appear (unchanged category glyphs, no flag encoding). Four Hoods demonstrate all four flag states at once: flagged-quiet (Florentin), flagged-busy (Kerem HaTeimanim, dashed warning stroke), not-flagged-busy (Neve Tzedek, no warning), not-yet-rated (Bavli, visually identical to not-flagged).
- **Place modal tab:** a toggle between flagged and not-flagged, showing the flag line appear/disappear in `PlaceDetailModal`'s existing layout, marked inline as filling T-033's placeholder slot.
- **Toast tab:** six scenario buttons — show, ignore-and-watch-it-auto-dismiss, offline, notifications-denied, already-answered, reset — each driving the real component state, not a static screenshot per state.
- **VoiceOver label preview toggle** — surfaces the exact spoken strings from §4 as on-map captions, same convention as T-031/T-033's mockups.
- **Design annotations toggle** — dashed captions marking exactly what's new in this task (the stroke/label logic, the place-modal slot fill, the entire toast) versus what's reused unchanged from T-031/T-033 (pins, the map/sheet chrome around the flag line).
- Both light and dark themes; palette consistent with `design/mockup-prompts.md` and T-031/T-033's mockups.

Deliberately **not** in the mockup: the notification permission system prompts themselves, the proposing algorithm, the Hood/place sheet's other content, Places/Passport, search, live events. The map and sheet chrome shown around this task's own components are minimal stubs matching the established visual language, not a re-design.

---

## 7. Principles conformance

| Call this spec makes | Citation |
|---|---|
| Flagged-vs-not is a weight+dash change on the Hood stroke, never a hue-only change; busy+flagged is a dash-pattern change at the same hue | design-principles.md §3 (never rely on color alone); manual Ch5/Ch14 "Don't Rely on Color Alone"; PRD req 2 bullet 2 verbatim |
| `Color("Flag")` is used nowhere else in the app's palette and is ≥5× the stroke weight of the unflagged baseline | design-principles.md §2, Von Restorff; manual Ch9 "Von Restorff Effect" (unique color + size ratio, both checked against the mockup's actual CSS, §2.3) |
| Flag stroke (3:1) and centroid label text (4.5:1) checked separately, both themes, both cleared with margin | design-principles.md §5, WCAG AA; manual Ch14 "Text Contrast Ratios" / "UI Component Contrast" — real numbers in §2.3, not asserted |
| Toast buttons ≥44pt, equal weight (a factual either/or, not a recommended choice) | design-principles.md §2, Fitts's Law; manual Ch12/Ch13 touch-target minimums |
| Toast is non-blocking — no scrim, nothing else stops responding | design-principles.md §2, Poka-Yoke / low-friction ask; PRD req 8 bullet 1 |
| No countdown/urgency affordance on the toast — deliberately kept quiet | design-principles.md §2 (B=MAT, raise ability not motivation); §2.3 Quick wins (trade-off recorded, not silently omitted) |
| Every state — Hood stroke (5 rows), place-modal line (3 rows), toast (7 rows) — specified rather than left to the developer | design-principles.md §4 |
| VoiceOver states the flag in speech in every state, including the two that render nothing visually | design-principles.md §5; `map-rendering-spec.md` §7's own resolution, extended and copy-corrected (§2.3 issue 1) |
| Hick's Law / Miller's Law | Not applicable — the toast is a single binary decision (2 options, well under Hick's 3–5), and no list/chunking surface exists in this task's scope. Flagging the omission rather than citing a section that doesn't apply, same convention T-031/T-033 used. |

No Section 2/3/5 area relevant to this feature was left unaddressed. §2.3 documents the `ui-design-review` skill actually being run against this spec and the published mockup's real source — two genuine issues found and fixed (one a banned-phrase leak in a sibling doc's own example text, one an internal inconsistency between this spec's first-pass zoom-gating and the PRD requirement it cites), two trade-offs weighed and knowingly not applied, not merely cited in passing. §2.4 re-checked every number and every rendered element against the mockup's actual published source rather than this document's intentions.

---

## 8. Open items handed to `architect` / `ios-developer`

Not blocking `design-approval`, flagged for the TRD:

1. **New zoom threshold for the flag's centroid label** (§2, "Zoom tier for the flag label" row) — the existing `showsNames`/`nameLabelSpanThreshold` gates Hood names and pins together at one span value; the flag *label* (not the stroke) needs a second, coarser threshold so it shows at Neighborhood zoom and drops at Close, per PRD req 3's literal wording. Exact span value is `ios-developer`'s call, same carve-out T-031 made for heat-band thresholds.
2. **`Place.isTouristTrap` doesn't exist yet.** `Hood.isTouristTrap: Bool?` already landed (T-040's Phase-1 carve-out). `Place.swift`'s own header names `isTouristTrap` as a field that "lands in the task that first reads them" — this is that task. Needs the same nullable-boolean treatment added to the `Place` struct and its bundled fixture, mirroring how `Hood` already did it.
3. **Every bundled Hood currently ships `isTouristTrap: null`.** Checked directly against `Passenger/Resources/hoods-tel-aviv.json`: all 24 Hoods are `null` today — the real cold-start state the PRD's own Open questions & risks section names, not a bug. For the Phase-1 demo to actually show flagged/busy+flagged/not-flagged states (not just the identical-looking null case), the fixture needs at least 2–3 Hoods and a handful of places seeded with real `true`/`false` values — plausible fake data, same spirit as `florentin`'s existing `[PROVISIONAL]` blurb. Not this spec's call to pick which Hoods; flagging the concrete gap so `ios-developer` doesn't have to discover it mid-build.
4. **Toast auto-dismiss interval (~5s)** — this spec's working default, not a PRD-specified number. The PRD leaves cadence itself as an [ASSUMPTION] (one notification/day); this is a narrower, purely-visual timing question the PRD doesn't address at all. Confirm or adjust against real usability testing once built.
5. **Toast accessibility announcement mechanism** (§4) — needs `UIAccessibility.post`/`AccessibilityNotification.Announcement` (or equivalent) fired the instant the toast appears, since nothing else alerts a VoiceOver user that a non-modal, unsolicited surface has arrived. No existing pattern in the codebase to follow (T-031/T-033 have no comparable passively-arriving surface) — this is new ground, named as such rather than forced into an ill-fitting citation.
6. **`map-rendering-spec.md` §7's stale example text** ("Florentin, busy, not a tourist trap") should be corrected in that doc directly by whoever next has write reason to touch it — flagged here (§2.3 issue 1) rather than edited in place, since that's a separate, already-locked shared doc this task doesn't own outright.

---

## 9. Assumptions carried from the PRD, not resolved here

Per the PRD's own Assumptions section — restated so this spec's traceability doesn't silently imply any of these were settled by design work:

- **[ASSUMPTION, PRD]** A not-flagged place shows no line in its modal (req 6). This spec builds to that reading (§2 Place-modal flag-line row) — if Aviran wants the opposite (an explicit "not flagged" line, since a sheet has room unlike the map), that's a PRD-level reversal, not a mockup tweak.
- **[ASSUMPTION, PRD]** A single answer never flips the displayed flag (req 9) — this spec's toast styling (§2.3 Passes: "No" isn't styled as a correction) depends on that reading holding.
- **[ASSUMPTION, PRD]** One local-QA notification per day per install (req 8) — doesn't affect this spec's per-instance toast design, only how often it fires; not re-litigated here.

Not resolved by this pass, and not this task's to resolve: the cold-start risk (no proposer at launch), the notification-denied coverage gap, whether anything rewards answering, and the exact Hood-vs-place flag-disagreement rule (PRD Open questions & risks). All carried forward exactly as the PRD states them.
