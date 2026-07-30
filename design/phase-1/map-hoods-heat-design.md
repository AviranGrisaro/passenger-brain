# Map — Hoods & Heat Area — Design Spec

**Task:** T-031 · **PRD:** [`prds/map-hoods-heat/map-hoods-heat.md`](../../prds/map-hoods-heat/map-hoods-heat.md) (Draft v1)
**Mockup:** https://claude.ai/code/artifact/967ade63-ea5b-46c9-89a8-d606ed11a819 — interactive HTML/CSS/JS, click-through, no build step
**Owner:** designer · **Date:** 2026-07-30 · **Status:** ready for `design-approval`
**Consistency check:** built against the locked 2026-07-30 revisions of `design/ux-flows.md` and `design/map-rendering-spec.md` — Hoods terminology (§0 of both), the boolean tourist-trap model, the heat-modal/nav-button reorganization. Nothing here contradicts either; see §7 below for the specific cross-references.
**Research note:** Mobbin MCP was queried for comparable map/heatmap/permission-priming flows before building the mockup and returned `Mobbin MCP requires a paid plan` — not authorized on this workspace's connector. Proceeded from the PRD, `ux-flows.md`, `map-rendering-spec.md`, and `design-principles.md` instead, per the standing "don't block" rule for this research step. Figma was not attempted — the founder ruling (2026-07-22) makes the HTML artifact the default deliverable, and this task didn't request Figma output.

---

## 0. Scope discipline

This spec covers exactly the five components product handed off, no more:

1. Map shell — MapKit base layer, cold open, Tel Aviv city-wide camera
2. Hood layer — named polygons, tap target, one-tap open
3. Heat area layer — stepped-band density fill, no gradients
4. Location permission flow — lazy When-In-Use prompt, granted/denied states
5. Density feed client — 13 hour buckets, synthetic source

**Deliberately absent, matching the PRD's own "Not in scope" line:** the tourist-trap/localness layer (PAS-6 item 1, unresolved), the time slider and heat modal (T-032), Hood/place detail sheet content (T-033), search, live events (T-034), Places/Passport/routing, any city but Tel Aviv. Where the mockup needs to *gesture* at one of these (e.g., tapping a Hood has to go somewhere), it shows the shallowest possible stub and says so on-screen — it does not design the thing it's stubbing.

---

## 1. Flow

**Entry point:** the app icon. There is no other entry point — no onboarding, no splash (`BOARD.md` scope gate).

```
App icon tap
  → Map renders (Tel Aviv, city-wide camera, heat + Hoods already visible, 0 taps)
      → "Tel Aviv, right now" title fades in, holds, fades out (~2s) — no persistent chrome after
      → [~1.2–2s later] Location — When In Use system prompt appears, non-blocking to the map underneath
          → Allow  → map recenters, "you are here" marker, near-me button becomes active
          → Deny   → map stays city-wide, near-me greys out, never re-prompted this install
      → User pans / zooms / taps freely (all live before and after the permission answer)
          → Tap inside a Hood → Hood sheet opens directly (no preview step)
              → Swipe down / tap outside → returns to the map, exactly one level up
          → Pan outside Tel Aviv → plain base map, Hoods and heat both disappear silently
              → Pan back inside → Hoods and heat return, nothing to recover from
```

**Exits:** there is no exit *from* this screen in T-031's scope — no "Go" hand-off lives here (that's the spot sheet, T-033). The only dismissal path is the Hood sheet's swipe-down/tap-outside, which returns to the map. The permission system sheet resolves itself (Allow/Don't Allow) and is never re-shown.

**Every subsequent launch:** identical, minus the permission prompt if iOS already recorded an answer. Granted opens already recentered, no animate-in beat; denied opens at the same city-wide default. The fading title still plays every cold open (it's tied to app-launch, not first-ever-launch, per PRD req. 1).

---

## 2. Screens & components

| Component | What it is | SwiftUI-native pattern |
|---|---|---|
| **Map shell** | Tel Aviv, city-wide default camera on cold open | `Map(position:)` (MapKit's SwiftUI API, iOS 17+) with a `MapCameraPosition` seeded to a fixed Tel Aviv `MKCoordinateRegion`. Pinch-zoom and pan use MapKit's native gesture handling — never suppressed (design-principles.md §3). |
| **Hood layer** | Named, non-overlapping polygons | `MapPolygon` per Hood inside the `Map`'s `MapContentBuilder`, geometry from the `hoods` table (PRD's Technical design). MapKit's SwiftUI `MapPolygon` has no built-in tap gesture — hit-testing needs a `MapReader` to convert a tap's screen point to a coordinate, then a point-in-polygon test against each Hood's stored geometry to resolve which one (if any) was hit. **Flagging for the architect/TRD:** this hit-testing approach, and whether it needs to fall back to `MKPolygonRenderer` inside a `UIViewRepresentable` if `MapReader` proves too imprecise at small Hood sizes, is an implementation call this spec doesn't resolve — it's the one place "SwiftUI-native" and "reliable tap target" could be in tension, and `architect` should settle it before `ios-developer` builds against an assumption. |
| **Heat area layer** | Stepped-band density fill per Hood, keyed to the current hour | Same `MapPolygon` shapes, `.foregroundStyle(bandColor(for:))` where `bandColor` maps a discrete `enum HeatBand { case none, quiet, moderate, busy }` to a fixed opacity step of one accent hue — never a computed gradient. `HeatBand` is exactly the `DensityContract.swift` idea `SALVAGE.md` flags REUSE: one enum, no blended score. |
| **Location permission flow** | Lazy When-In-Use ask, granted/denied handling | `CLLocationManager` wrapped in an `@Observable` `LocationStore`. Call `requestWhenInUseAuthorization()` only once, only when `authorizationStatus == .notDetermined`, triggered a couple of seconds after the map's first `onAppear` — not at launch, not gated behind a tap (per `ux-flows.md` §9 Q2's recommendation, which this spec treats as the working default; it is still an open item for Aviran to confirm per that doc). Granted state drives `MapCameraPosition.userLocation()` for the recenter and shows the system-provided user-location dot; denied state is read once from `CLLocationManager.authorizationStatus` and never re-requested. |
| **Density feed client** | 13 hourly buckets (now → +12h), synthetic source, fetched once | A `DensityStore` service fetching `hood_density` rows for the current session, keyed `hood_id` + `hour_bucket`, cached client-side so **T-032's slider never round-trips per drag** (PRD's API contract). T-031 only ever reads the "now" bucket — the store's shape must already support a `selectedHour` binding so T-032 can attach the slider to it later without a re-fetch model change. This is a **handoff seam to flag explicitly**, not a T-031 build item: T-031 should expose `DensityStore.band(for hoodID:, hour:)` even though nothing in this task's own UI calls it with anything but "now." |
| Fading title (P0) | "Tel Aviv, right now," ~2s fade in/out, cold-open only | `Text` with `.transition(.opacity)` driven by a `Task.sleep`-based timer; respects Reduce Motion by cross-fading over a shorter/near-instant duration rather than skipping the state change entirely. |
| Near-me button (P1) | Recenter control | Standard circular icon button, bottom-third placement (Thumb Zone, design-principles.md §3). Disabled visual state when permission is denied; tapping it while denied shows inline copy pointing to Settings, never re-triggers the system dialog. |
| Hood name label (P1) | Visible at Hood zoom and closer only | `Text` anchored near each Hood's rendered centroid, hidden at city-wide zoom — mirrors `map-rendering-spec.md` §2's zoom-gated disclosure pattern, applied here to the name label since heat itself (unlike the excluded tourist-trap stroke) is visible at every zoom per PRD req. 4. |

---

## 3. Every state

Per design-principles.md §4 (loading / empty / error / permission-denied / offline) and the PRD's own P0 requirements 2, 6, 7:

| State | Behavior |
|---|---|
| **Loading (cold open, before density arrives)** | The map, Hood geometry, and base chrome render immediately and are interactive — heat fill simply doesn't paint until the density fetch resolves, no spinner, no blocking. If the fetch is still in flight past ~400ms (Doherty, design-principles.md §2), the Hood layer stays in its unfilled/no-data visual (see Empty below) rather than showing a loading affordance — this is a case where "no state" *is* the correct state, since a spinner over an already-interactive map would contradict req. 1. |
| **Empty (a Hood has no density value for the selected hour)** | No fill, no error copy, no placeholder icon — the Hood polygon renders in its neutral base tone, indistinguishable on the map from "not yet curated." (PRD req. 7; same silent-gap convention `map-rendering-spec.md` §3 already uses for the excluded tourist-trap layer, applied here to heat.) The gap resolves on tap: the Hood sheet (T-033) is where "no data" gets an actual sentence, not the map surface. |
| **Error (density feed unreachable)** | Base map and Hood geometry still render and stay fully interactive — pan, zoom, and tap all keep working. No error banner, no retry button on the map itself. This degrades identically to the Empty state visually (no fill anywhere) since from the map's point of view "the feed is down" and "this Hood has no data" should look the same to the user — the difference isn't worth surfacing at this layer. |
| **Permission-denied** | Map stays at the default Tel Aviv city-wide camera, fully pannable/zoomable/tappable. Near-me button greys out and shows inline "turn on location in Settings" copy on tap instead of re-prompting (iOS won't re-trigger the system dialog once denied, and the app shouldn't pretend otherwise). No degradation to Hood or heat rendering — those never depended on location. |
| **Offline** | Base map, Hood polygons, and the last-cached density bands keep rendering and stay interactive. A small, non-blocking indicator (not a takeover) communicates "showing cached data" — kept out of the map's primary visual field (top corner, not competing with the fading title or the heat read itself) so it never contests Von Restorff's one-special-element rule with the actual content. |
| **Panned outside Tel Aviv** | Plain base map, zero Hoods, zero heat, zero chrome about it (PRD req. 2 explicitly rules out an error or empty-state takeover here). This is the one state where *less* is correct — no "you've left the mapped area" copy anywhere on the map surface. |

---

## 4. Accessibility notes

Adapts `map-rendering-spec.md` §7's resolution pattern to heat alone, since this task excludes the tourist-trap layer that §7 was jointly written for:

- **Every Hood polygon needs a VoiceOver label that states its density explicitly in speech**, regardless of whether anything renders visually — e.g. *"Florentin, busy"* or *"Kerem HaTeimanim, no data right now."* This matters for the same reason it mattered in `map-rendering-spec.md` §7: a sighted user reads "no fill" as "quiet or no data," but VoiceOver can't read an absence — the spoken label has to say it, not rely on silence meaning the same thing it does visually. (The mockup's "Show VoiceOver labels" toggle demonstrates this literally, rendering the spoken string as an on-map caption per Hood.)
- **Heat bands never rely on color alone** (design-principles.md §3, and `ux-flows.md` §2's own citation for the heat-layer row). The stepped bands in this spec differ by **opacity/lightness step over a single hue**, not by hue alone — so the band sequence stays ordinally legible in grayscale and for colorblind users without needing a second channel invented. The VoiceOver label above is the non-visual backstop for the same requirement.
- **Contrast:** the fading title and any inline copy (Settings deep-link, near-me disabled state) meet 4.5:1 against the map background at the moment they're legible (design-principles.md §5, WCAG AA normal text). The Hood layer's own stroke against its neighbors only needs the 3:1 large-graphics bar, since it's a boundary line, not text.
- **Touch targets:** a Hood's tappable region is never smaller than 44pt regardless of how thin the polygon renders on screen (Fitts's Law, design-principles.md §2) — where a Hood's screen-space shape is narrower than that at a given zoom, the hit-test area extends beyond the drawn boundary rather than shrinking the target to match the visual. Near-me is a standard ≥44pt circular target.
- **Dynamic Type:** the fading title and any inline permission/error copy use semantic text styles, not fixed point sizes — tested at largest accessibility sizes per design-principles.md §3's iOS translation row.
- **Reduce Motion:** the title's fade and the "you are here" marker's pulse both honor Reduce Motion — cross-fade/appear near-instantly instead of animating, rather than skipping the state change outright.

---

## 5. PRD traceability

| PRD requirement | Where this design satisfies it |
|---|---|
| P0-1 Cold open goes straight to the map | §1 Flow; §2 Map shell / fading title rows |
| P0-2 Tel Aviv only | §1 Flow ("pan outside" branch); §2 Map shell row; §3 "Panned outside Tel Aviv" state |
| P0-3 Hoods (non-overlapping, one-tap open) | §2 Hood layer row (incl. the flagged hit-testing open question); §1 Flow's Hood-tap branch |
| P0-4 Heat area rendering (stepped bands, no gradients, 0-tap visible, consistent band meaning, never a blended score) | §2 Heat area layer row; §4's color-alone note |
| P0-5 Heat bound to one hour | §2 Density feed client row (the `selectedHour` handoff seam for T-032) |
| P0-6 Lazy location permission | §2 Location permission flow row; §1 Flow; §3 Permission-denied state |
| P0-7 Degraded data is silent | §3 Empty and Error states |
| P1 Near-me recenter | §2 Near-me button row |
| P1 Hood name label at neighborhood zoom | §2 Hood name label row |

---

## 6. Mockup

Interactive HTML/CSS/JS artifact, published as a Claude Artifact: **https://claude.ai/code/artifact/967ade63-ea5b-46c9-89a8-d606ed11a819**

What it demonstrates, live:
- Cold-open sequence — fading title, then the lazy system permission prompt appearing after the map is already interactive ("Replay cold open" replays this).
- Zoom-level control (City-wide / Hood / Close) — heat rendering as blurred blobs at city-wide vs. crisp stepped bands + name labels at Hood zoom+, matching `map-rendering-spec.md` §2's zoom-gated disclosure pattern applied to heat.
- Permission control (Not asked / Granted / Denied) — recenter + "you are here" marker on Granted; greyed near-me + inline Settings copy on Denied.
- One-tap Hood open — tapping any Hood polygon opens a sheet stub that names itself as a placeholder for T-033, proving the interaction without designing the destination.
- Network toggle (Online/Offline) — a small non-blocking "showing cached Hoods" indicator, map stays interactive.
- Density-gap toggle — one Hood (Kerem HaTeimanim) can be flipped to "no data," rendering with no fill and no error copy.
- Map-bounds toggle (Tel Aviv / Panned outside) — the outside state clears Hoods and heat with zero on-screen commentary.
- VoiceOver-label preview toggle — surfaces the spoken label text per Hood, per §4 above.
- Both light and dark themes, following the palette already established in `design/mockup-prompts.md` (kept consistent with prior Passenger mockups rather than inventing a new one).

Deliberately **not** in the mockup: the search/heat/profile nav buttons and the Places icon. Those open surfaces owned by other PRDs (T-032's heat modal, and Passport/Places aren't part of this task at all) — including them here would be designing outside this spec's scope. Their absence is a scope decision, not an oversight; noted so a reviewer doesn't read the sparse chrome as incomplete.

---

## 7. Principles conformance

| Call this spec makes | Citation |
|---|---|
| Base map + Hood geometry render and stay interactive before heat, permission, or the density feed resolve — functioning beats polished | design-principles.md §1, Maslow precedence (Functional > Reliable > Usable > Pleasurable) |
| Heat repaint / initial paint targeted under 400ms; no spinner for a sub-400ms wait | design-principles.md §2, Doherty Threshold |
| Hood tap targets never below 44pt even when the drawn shape is thinner | design-principles.md §2, Fitts's Law |
| Heat bands step by opacity/lightness, never hue alone; paired with an explicit VoiceOver label | design-principles.md §3 (iOS translation row: "never rely on color alone... critical for Passenger's map"); §5 accessibility | 
| Near-me button sits in the bottom third | design-principles.md §3, Thumb Zone |
| Pinch-to-zoom and pan are never suppressed, at any state (denied permission, offline, outside Tel Aviv) | design-principles.md §3 |
| Every state — loading, empty, error, permission-denied, offline — specified rather than left to the developer | design-principles.md §4 |
| Contrast: title/inline copy 4.5:1, Hood boundary stroke 3:1 | design-principles.md §5, WCAG AA |
| One "special" element at a time — the offline indicator is kept subordinate to the map/heat read, not competing for attention | design-principles.md §2, Von Restorff |
| Hick's Law / Miller's Law | Not applicable — this task has no multi-option decision surface or list to chunk; flagging the omission rather than citing a section that doesn't apply. |

No Section 2/3/5 area relevant to this feature was left unaddressed: Hick's/Miller's are the only two rows in §2 without a live decision to cite against, and that's recorded above rather than silently skipped.

---

## 8. Open items handed to `architect` / `ios-developer`

Not blocking `design-approval`, but real enough to flag rather than silently assume:

1. **Hood tap hit-testing** (§2) — whether `MapReader` + point-in-polygon is precise enough at small Hood sizes, or whether it needs an `MKPolygonRenderer`-backed fallback. This is the one place this spec couldn't fully resolve "SwiftUI-native" without more information than a design pass has.
2. **`selectedHour` seam for T-032** (§2, Density feed client) — T-031 should build `DensityStore` so a later hour parameter is a binding change, not a re-architecture. Flagging so the TRD accounts for it now rather than retrofitting.
3. **Exact band count and thresholds** — the PRD itself leaves this as a `data-engineer` open call (Technical design, Open technical questions). This spec's mockup uses three non-empty bands (Quiet / Moderate / Busy) as an illustrative default; the real thresholds aren't decided here.
4. **Permission-prompt exact timing** — this spec follows `ux-flows.md` §9 Q2's recommendation (auto-prompt a couple of seconds after first render) as the working default, but that recommendation is still open for Aviran to confirm, not yet a locked decision.
