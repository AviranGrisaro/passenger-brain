# Test plan — Places: Been & Saved (T-036/PAS-27, PAS-36)

Built from `TRD.md` §9's verification table (8 P0 rows) plus `places-been-saved.md`'s
own requirement checkboxes. Did not exist before this pass — should have been
written at `trd`/`build`, per this agent's own "prepare early" rule; written now,
against already-shipped code (`passenger-code` HEAD `3d8e3b8`, feature landed at
`7688834`+`46d2af2`, contrast/revert fix at `952cf2f`).

This pass's own scope is narrow — verifying `952cf2f`'s two fixes (T-036/PAS-27's
opaque-card contrast fix, PAS-36's revert of the wrong force-dismiss fix) — so rows
1–3, 5–7 are marked from the prior build/code-review evidence already on the board,
not re-derived here. Rows **4d** and **8** are this pass's own direct verification.

| # | Requirement | Check | Verdict | Evidence |
|---|---|---|---|---|
| 1 | One list, three provenance states, precedence Saved>Been>Visited, one row/place | `PlacesListComposition.entries` over 3-state fixture | PASS (prior) | Unit-tested (C3), part of the 253/253 green this session; not re-derived |
| 2 | Manual save <400ms, persists; un-save falls to next word or removes row | `SavedPlacesStoreTests` + composition test | PASS (prior) | Same suite, green this session |
| 3 | Been fires only for known places, 20-min threshold, silent, revisit no-op | Fixture unit tests + diff grep | PASS (prior), threshold/detector explicitly NOT verified in Phase 1 per TRD §9 row 3 — no detector exists yet, carried to Phase 2 | Unchanged this session |
| 4a-c | Closed places save; badge distinct; independent of tourist-flag; never blocks route | Decode + row render + fixture content | PASS (prior) | Unchanged this session |
| **4d** | Badge contrast ≥4.5:1, both interface styles | `PlacesListContrastTests.badgeTokensMeetAA` resolves real `BadgeOnSurface`/`BadgeSurface` from the asset catalog | **PASS** | Ran in this session's full-suite pass (see below); `BadgeSurface`/`BadgeOnSurface` unaffected by `952cf2f` (only `PlacesListOverlay`'s outer card background changed) |
| 5 | Degraded permission degrades, never breaks; no re-ask | Grep + manual denied-location run | PASS (prior), Phase-1 caveat stands (fixture populates regardless of permission — stated in TRD as known, not a gap this pass introduces) | Unchanged |
| 6 | Empty/offline states plain, not errors | Empty fixture + airplane-mode run | PASS (prior) | Unchanged |
| 7 | Map accent binary, close-zoom only, shape+colour, ≥44pt target | `isListed` vs entries, zoom-gated ring, greyscale render | PASS (prior) | Unchanged |
| **8** | Row → place modal directly, skipping Hood; nav-modal exclusivity; dismiss → map unchanged | (a) row tap opens `router.openPlace`, no Hood; (b)/(c) mutual exclusivity vs other nav surfaces; (d) camera/hour untouched | **PASS — this pass's primary target** | Live simulator repro (below) + source read of `DetailRouter.swift`/`MapScreen.swift` |

## This pass's own verification (T-036/PAS-27 contrast + PAS-36 revert)

**Static:**
- `PlacesListOverlay.swift:61` — `.background(Color("Surface"), in: RoundedRectangle(...))`, no `.thickMaterial` anywhere in the file. `Surface.colorset/Contents.json` — alpha `1.000` in both the universal and dark-appearance entries. Genuinely opaque, confirmed by direct asset-catalog read, not inferred from the commit message.
- `PlacesListContrastTests` (`ContrastRatioTests.swift:60-86`) resolve `UIColor(named:)` against the real `.main` bundle asset catalog under real light/dark trait collections — with the card now actually `Color("Surface")` on screen, this test measures the real composited color for the first time (previously it measured a color the `.thickMaterial`-backed UI never displayed).
- `MapScreen.swift:297` — `onSelect: { place in detailRouter.openPlace(place) }`, the restored TRD-correct closure (no `chrome.dismiss()`, no `selectPlaceFromList`). `grep -rn "selectPlaceFromList"` across the repo: zero hits — clean revert, no dangling reference.
- `DetailRouter.swift` — `openPlace` sets `place`, leaves `hood` untouched, clears `event`; `closePlace()` clears only `place`. Dismissing the place-detail sheet (`.sheet(isPresented: isDepth1Presented)`, which routes `false` → `closeHood()` when `hood == nil`, itself a no-op beyond clearing `place`) never touches `chrome.presented`, so the `.places` overlay is untouched by opening/closing the depth-1 sheet on top of it. This is the structural reason row 8(d) holds.
- `MapScreen.swift:481` `handlePresentedSurfaceChange` still calls `router.closePlace()` only when *leaving* `.places` via a different surface switch — the real D8 catch-all, untouched by this revert.

**Live (isolated `git worktree` pinned to `952cf2f`, iPhone 17 Pro simulator `60E0B96F-...`, iOS 26.5):**
1. Built clean (`xcodebuild build`, BUILD SUCCEEDED).
2. Installed + launched. Tapped the Places button → list opened: opaque dark card, four fixture rows (Carmel Market Spice Corner/Been+closed, Dr. Shakshuka/Been, Florentin Street Art Walk/Visited, Nachum Gutman Museum/Visited+closed) — no map bleed-through behind the text, confirming the opaque-card fix visually, not just by asset inspection.
3. Tapped "Dr. Shakshuka" → place-detail sheet opened above the list: title, bookmark save button, close button, "Eat & Drink" category row, "Directions" button, all on a solid opaque card — no translucent/"stacked messily" look. (Blurred bands visible mid-card in the raw screenshot are a redaction artifact of the screenshot tool itself, same class as its Dynamic-Island blackout — confirmed by re-screenshotting twice with identical, non-animating blur, and by the fact `PlaceDetailModal.swift`'s view tree has no content in that region, only a `Spacer()`.)
4. Tapped the sheet's close button → sheet dismissed.
5. **Places list reappeared underneath, unchanged** — all four rows, same order, same content, "Places" header intact. This is the exact TRD §5 flow ("Open a place... Dismiss → back to the list, unchanged") that the wrong `4cd55f8` fix broke and `952cf2f` restores.
6. Full `xcodebuild test` in the same isolated worktree: **253/253 unit tests + 6/6 UI tests, zero failures, zero flakes** this run (including `ColdOpenPerformanceTests`, previously flaky in other sessions' full-suite runs — clean here).

## Verdict

**PAS-27/T-036: PASS.** Opaque `Color("Surface")` confirmed by asset inspection and live render; contrast tests now measure the real on-screen color; no regression in the rest of the suite.

**PAS-36: PASS.** Revert confirmed clean (no dangling code, no test asserting the wrong behavior survives); TRD §4.6/§5/D8-specified list-stays-under-sheet behavior reproduced live end-to-end.

## Left behind
- Rows 3, 5's Phase-1 caveats (no real dwell detector, fixture populates regardless of permission) are pre-existing, TRD-acknowledged gaps, not introduced or affected by `952cf2f` — not re-flagged as new findings.
- Req 4's closed-state refresh (no owner/cadence) is a separate, already-tracked gap (`places-been-saved.md`'s own Open Questions, T-044) — untouched by this commit.
