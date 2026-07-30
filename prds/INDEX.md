# PRDs

One folder per feature, flat — `prds/<feature-slug>/<feature-slug>.md`. Phase goes on the PRD's `**Phase:**` header line, never in the path. Add a row here whenever you add a PRD.

**Before writing one:** it must quote the line in `../strategy/passenger-strategy.md` that authorizes the feature. A PRD that can't cite one doesn't leave `spec`. See the scope gate in `../CLAUDE.md`.

| Feature | Phase | Status | PRD |
|---|---|---|---|
| Map — Hoods & heat area | 1 | Draft v1 | [`map-hoods-heat/`](map-hoods-heat/map-hoods-heat.md) — base map, Hoods, heat, cold open, Tel Aviv only. Localness/trap layer deliberately excluded (PAS-6 item 1). |
| Time slider — now → +12h | 1 | Draft v1 | [`time-slider/`](time-slider/time-slider.md) — 13 hour-snapped positions, lives in the heat modal, resets to "now" each launch. |
| Hood & place detail | 1 | Draft v1 | [`hood-place-detail/`](hood-place-detail/hood-place-detail.md) — Hood blurb + place list, place modal, native Maps/Waze hand-off, category rename to "Things to do" / "Eat & Drink". Filter placement left open (PAS-6 item 6). |
| Live events overlay | 1 | Draft v1 | [`live-events-overlay/`](live-events-overlay/live-events-overlay.md) — third map layer, hour-bound, ranked subset. **Launch-blocking on PAS-5**; client ships usable with an empty layer. |
| Tourist-trap flag & local QA | 1 | Draft v1 | [`tourist-trap-flag/`](tourist-trap-flag/tourist-trap-flag.md) — the boolean flag (decision #37), its Hood-stroke channel, the place-modal line, and the binary post-visit local-QA toast. Fills the layer `map-hoods-heat` leaves out. |
| Places — Been & Saved | 1 | Draft v1 | [`places-been-saved/`](places-been-saved/places-been-saved.md) — one list, three provenance states, permanently-closed badge (decision #38), binary map ring. Device-local: does not survive reinstall. |
| Passport | 1 | Draft v1 | [`passport/`](passport/passport.md) — private sticker album + per-Hood Local status (decision #40, ladder retired), under the Profile tab (decision #39). Depends on Places. |

## Expected V1 shape

**Updated 2026-07-30** for the founders-meeting V1 scope lock (`strategy/passenger-strategy.md`, decisions #27–36) — the count grew past the original six once routing, events, Passport, and TikTok import all pulled into V1. Roughly nine to ten PRDs now, not twenty-seven, and **several of the items below can't leave `spec` yet** — the scope gate requires a PRD to quote its authorizing line, and a few of these lines are themselves flagged as unconfirmed (see strategy.md's Open questions). `product`: write PRDs for the unambiguous parts first; don't resolve a flagged item yourself.

**`product` pass, 2026-07-30 (PAS-10):** four written — map, time slider, Hood/place detail, live events. Five held: three on PAS-6, two on PAS-7.

**Second `product` pass, 2026-07-30 (after PAS-6's resolution):** the three PAS-6-held items are written — tourist-trap flag, Places, Passport — against decisions #37–#40, confirmed live by Aviran. **Seven of nine written.** Still genuinely held: Scenic Walk (PAS-6 item 8, Aviran's ship-vs-slip call) and TikTok import (item 9, ToS sign-off). **Newly unblocked and not yet written: search + quick filters** — decision #41 settled placement as sheet-internal, so nothing blocks it any more; it is the next PRD.

- The map itself: cold open, Hoods (decision #27), heat area, Tel Aviv only — **written**
- **Tourist-trap flag** (boolean, decision #37) plus the binary local-QA loop that corrects it — **written**
- Time slider: now → +12h, hour snapping (unchanged) — **written**
- Hood and place detail: hand-curated blurb, tagged spots/places, two categories (renamed "Things to do" / "Eat & Drink", decision #33), hand-off to native Maps/Waze — **written**
- Quick filters + search: icon in map chrome opening a sheet; place names, keywords, and Hoods, results carrying heat + flag and honoring the slider hour (decision #23) — **unblocked, not yet written.** Placement is settled sheet-internal (decision #41); decision #25 stands unreversed
- Places: Been (dwell auto-save) + Saved (manual), visually/functionally distinct (decisions #26, #29, #30), permanently-closed badge (decision #38) — **written**
- Passport: per-Hood Local status (decision #40 retires the seven-tier ladder), stickers (#29), Profile tab (#39) — **written**
- Scenic Walk + fastest-route mode: weighted street-segment routing (decision #32) — **launch-blocking on `data-engineer`'s feasibility scoping**, don't spec ahead of that
- TikTok import: video → extracted places → Saved Places (decision #34) — **launch-blocking on `data-engineer`'s feasibility scoping**, don't spec ahead of that
- Places + localness/tourist-trap pipeline: sourcing, the algorithm, and the in-app local-QA loop that corrects it — shape depends on how decision #28's flagged ambiguity resolves

**Not V1, do not write a PRD:** Google Maps saved-list import (decision #35) — exploration only, not authorized to build. A feasibility note is fine; a pipeline PRD is not.

**No longer excluded — reversed by the 2026-07-30 lock:** Scenic View (now "Scenic Walk," V1, decision #32) and the Live Events overlay (V1 since 2026-07-29, decisions #19/#20 superseded) both moved back into V1. The prior version of this section excluded them; that exclusion no longer holds. The Locali client had an events overlay shipping unflagged before — worth double-checking any salvage-driven PRD here actually matches the current locked scope (algorithmically-selected likely-interesting events, not a raw feed) rather than the old unflagged version.

Cross-feature UX reference for all of the above: `../design/ux-flows.md` (reading view: `../design/ux-flows.html`).
