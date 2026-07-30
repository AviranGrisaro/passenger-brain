# Map — Hoods & Heat Area — Test Plan

**Task:** T-031 · **Owner:** qa · **Status:** executed 2026-07-30, results filled in below
**Traces to:** [`map-hoods-heat.md`](./map-hoods-heat.md) (PRD, Draft v2) requirements, [`TRD.md`](./TRD.md) contracts
**Written retroactively at the `qa` gate** — no TRD existed early enough in this feature's own pipeline for a pre-build pass; every later feature should get this written at `trd` instead (see `passenger-brain/agent-os/LESSONS.md` candidate note in the QA worklog entry).

Build tested: `passenger-code` commit `6f75a7c`, simulator iPhone 17 Pro / iOS 26.5. No physical device, no applied Supabase migrations, no live backend reachable from this sandbox — noted per case where it limits what could be verified.

## Automated coverage (ran, not just read)

| Case | Trace | Method | Result |
|---|---|---|---|
| Full unit + UI test target, one invocation (not scoped per-class) | L-005 lesson | `xcodebuild test -scheme Passenger -destination iPhone 17 Pro` (both `PassengerTests` + `PassengerUITests` in one run) | **PASS** — 26/26 unit tests, 1/1 UI test, 0 failures |
| Cold-open-to-interactive signpost | TRD §7 | `ColdOpenPerformanceTests`, 5 iterations | **PASS (simulator only)** — avg 0.464s (values 0.467/0.471/0.455/0.458/0.466), well inside the ≤2.0s budget. Third independent simulator reproduction (0.462s ios-code-reviewer, 0.472s ios-developer, 0.464s here) — consistent, but simulator-only each time |
| Hood hit-testing (inside/outside/bbox-miss/concave/near-miss tolerance) | TRD §4.3 | `HoodHitTesterTests`, 6 cases | **PASS** |
| Bundled catalog load (well-formed / missing / malformed) | TRD §4.2 | `HoodCatalogTests`, 3 cases | **PASS** |
| Density boundary validation (unknown band, unparseable timestamp) | TRD §4.5 | `DensitySnapshotTests`, 4 cases | **PASS** |
| DensityStore (cold-launch offset, hour-roll refresh/clamp, live/cache/unavailable) | TRD §4.4, §3.4 | `DensityStoreTests`, 7 cases | **PASS** |
| Heat palette monotonic opacity | PRD req 4 | `HeatPaletteTests`, 2 cases | **PASS** |
| SettingsHint / LinkOnSurface contrast ≥4.5:1, light+dark | TRD §8 D1 | `ContrastRatioTests` + `SettingsHintContrastTests`, resolved against real Asset Catalog | **PASS** |

## Behavioral pass (built + ran the app on simulator, not read-only)

| # | Case | PRD trace | Method | Result |
|---|---|---|---|---|
| 1 | Cold open: first frame is the map, no splash/carousel/sign-in | Req 1 | Fresh install, launch, immediate screenshot | **PASS** — caught "Tel Aviv, right now" title over an already-rendered, already-interactive map, zero prior chrome |
| 2 | "Tel Aviv, right now" title fades in/out within ~2s, leaves no persistent chrome | Req 1 | Screenshot at launch; absent in all later screenshots | **PASS** |
| 3 | Map pannable/zoomable/tappable before permission answered | Req 1 | Pinch-zoom and Hood tap performed while a system dialog had not yet resolved / immediately after cold open | **PASS** |
| 4 | Cold launch interactive <3s (device) | Req 1 | Simulator signpost only, see automated table | **PASS (simulator), unverified on physical A13 — see Unverifiable** |
| 5 | Tel Aviv only — city-wide default camera | Req 2 | Screenshot at cold open | **PASS** |
| 6 | Panning outside Tel Aviv shows plain base map, no crash, no error takeover | Req 2 | Panned/zoomed to Herzliya, Ramat Gan, Rishon LeZion | **PASS** — no Hoods, no heat, no error, fully interactive |
| 7 | No city picker in UI | Req 2 | Visual sweep of chrome (title, near-me, settings hint, cached-data pill) | **PASS** — no such control exists |
| 8 | Hood polygons named, dozens not thousands (placeholder scope) | Req 3 | Visual — 4 placeholder Hoods (Florentin, Neve Tzedek, Kerem HaTeimanim, Lev HaIr) render with name labels at Hood zoom | **PASS for the fixture in place; real geometry (B3) not yet landed — see carried-forward item 4** |
| 9 | One tap inside a Hood opens its sheet, no two-step preview | Req 3 | Tapped Florentin at Hood zoom | **PASS** — opened `HoodStubSheet` directly, one tap, `.medium` detent |
| 10 | Heat renders as stepped bands, never a gradient; no blur/feather at any zoom | Req 4 | Code read (`HeatPalette.opacity(for:)`, single-argument switch, no blur/material) + visual (no fill anywhere in this build, consistent with no backend) | **PASS by construction; cannot visually confirm actual stepped-band appearance without a live density feed — see Unverifiable** |
| 11 | Heat visible at 0 taps on cold open (no control gates it) | Req 4 | No control found anywhere in chrome that toggles heat | **PASS by construction (same caveat as #10 — no data to actually paint in this sandbox)** |
| 12 | Same band = same appearance at every zoom | Req 4 | Code read — `HeatPalette` takes one argument, no zoom term; `ios-code-reviewer` already verified no added parameter | **PASS (static); not independently re-visualized live — no density data available** |
| 13 | Lazy permission — system prompt only after map on screen | Req 6 | Screenshot before/around prompt appearance across 3 fresh-install runs | **PASS** — prompt never precedes an interactive map |
| 14 | Denied: map stays city-wide, fully usable, never re-prompted | Req 6 | Denied via "Don't Allow", relaunched app 2x, panned/tapped/zoomed | **PASS** — no re-prompt observed across relaunches within the same install; map fully interactive |
| 15 | Denied: near-me button shows disabled affordance | Req 6 | Screenshot — icon renders `location.slash.fill`, secondary tint | **PASS** |
| 16 | Granted: "you are here" marker appears | Req 6 | Granted via system prompt with a simulated location; `UserAnnotation()` rendered | **PASS** |
| 17 | **Granted: the map recenters on the user** | Req 6 | Granted via the app's own auto-scheduled system prompt (not a NearMeButton tap) with a simulated location far from the default camera (Jerusalem, 31.7683/35.2137); observed for >60s real time | **FAIL — see Finding A below** |
| 18 | Degraded data: Hood with no value renders with no fill, no error copy | Req 7 | This entire sandbox has no backend configured (`AppConfig.supabase == nil`) — every Hood is permanently in this state | **PASS** — no fill, no on-map text anywhere, at any zoom, across every screenshot taken |
| 19 | No on-map text of any kind announces a data gap | Req 7 | Same as #18 | **PASS** |
| 20 | Feed unreachable: base map + Hoods still render, stay interactive | Req 7 | Same as #18 — feed has been "unreachable" for the entire test pass | **PASS** |
| 21 | Hood name label at neighborhood zoom, name only, no density word | P1 | Zoomed to Hood level, read labels | **PASS** — labels show only Hood names ("Florentin", "Neve Tzedek", etc.), no density word anywhere near a centroid |
| 22 | VoiceOver states density (or "no data right now") per Hood, at every zoom | TRD §4.1/C10 | Code read — `HoodLayer.voiceOverLabel`, always-present accessibility element even when `showsName == false` | **PASS (static) — not run with VoiceOver actually enabled, see Unverifiable** |
| 23 | Offline-with-cache indicator | TRD §3.4/§5.3 | Requires a prior successful live fetch to produce a cache file; no backend ever reachable in this feature's whole pipeline | **Untestable from this sandbox — see Unverifiable** |
| 24 | 3 privileged RPC functions deny anon/authenticated (401/403) | Security fix, `code-review` HIGH finding | Migrations not applied to any Supabase project; no credentials, no `SupabaseConfig.plist`, no project URL anywhere in the repo (`grep` swept for `supabase.co`/`anon_key`/`apikey`, only the TRD's own prose matched) | **Untestable from this sandbox — see Unverifiable** |

## Finding A (new, found in this pass — not one of the 4 carried-forward items)

**Req 6's "Granted: the map recenters on the user" is not satisfied on the app's own default flow.**

- `passenger-code/Passenger/Map/MapScreen.swift:150-163` (`handleNearMeTap`) is the *only* place `camera` is ever set to `.userLocation(fallback:)` (lines 159, 161). There is no `onChange(of: locationStore.authorizationStatus)` or equivalent that reacts to a grant happening via the app's own auto-scheduled system prompt (`PermissionPrompt`, fired ~3.4s after cold open, independent of any near-me tap).
- Design spec (`design/phase-1/map-hoods-heat-design.md` line 58) states the intended contract in state terms, not tap terms: *"Granted state drives `MapCameraPosition.userLocation()` for the recenter and shows the system-provided user-location dot."* The TRD's D2 mechanism (§8) only wires this inside the near-me tap handler, narrower than the design spec's own framing.
- Reproduced live: fresh install, simulated location set far from the default Tel Aviv camera (Jerusalem — clearly distinguishable from Tel Aviv on screen), granted "Allow While Using App" via the auto-scheduled system prompt (never tapped near-me first). The "you are here" marker rendered correctly at the simulated location, but the camera stayed on the city-wide Tel Aviv region — observed for over a minute of real elapsed time, no recenter ever occurred.
- **Not a crash, not data-unsafe, and there is a one-tap workaround**: tapping near-me afterward (now in the `.authorizedWhenInUse` branch) does trigger `camera = .userLocation(...)`. But the PRD's own bullet and the design spec's own contract both describe recentering as a consequence of the *granted state*, not of a *subsequent explicit tap* — and the app's own designed flow (lazy, auto-scheduled prompt) is precisely the path that misses it. A first-time user who grants permission when asked gets a marker but not the promised recenter.
- **Severity: Major, not Blocker.** No crash, no data exposure, one extra tap recovers the intended experience, and the marker itself (the other half of req 6) does work. But it is a confirmed, reproducible gap against a P0 requirement bullet on the app's primary onboarding-equivalent path, not an edge case.
- **Recommended fix:** add a reaction to `locationStore.authorizationStatus` transitioning into `.authorizedWhenInUse`/`.authorizedAlways` (e.g. `.onChange` in `MapScreen`) that sets `camera = .userLocation(fallback: .region(telAvivCityWide))` the same way `handleNearMeTap` does, so the recenter happens regardless of which path granted the permission.

## Carried-forward items — triage

1. **Security RPC 401/403 check** — untestable from this sandbox (see case 24 above). Same conclusion as `code-reviewer`/`security-auditor`: fix is present in the SQL file, re-confirmed twice by static review, but the live behavior has never been exercised because migration `002` is not applied to any Supabase project and no credentials exist in this environment. **Confirmed still needing verification once Aviran applies the migrations** — not skipped silently.
2. **4 `ios-code-reviewer` should-fix findings** — all 4 independently re-confirmed present in the current build by direct source read (not re-derived from the reviewer's description):
   - Edge-tap 22pt tolerance fallback to 0 (`MapScreen.swift:132` area, `mapPointTolerance(...) ?? 0`) — confirmed real, still present. Non-blocking, matches original triage.
   - `SettingsHint` lacking an explicit `frame(minHeight: 44)` (`Map/SettingsHint.swift`) — confirmed real, still present (only footnote-text padding, no explicit frame). Non-blocking.
   - Cold-open camera framing renders the 4 placeholder Hoods small/off-center in portrait — confirmed by direct observation: at the default `telAvivCityWide` region (span 0.14) on a portrait iPhone 17 Pro, the visible viewport spans roughly Herzliya to Rishon LeZion, and none of the 4 fixture Hoods (all central-Tel-Aviv) are visible without zooming in. This is a placeholder-geometry artifact per the original note, not a code defect — flagging again for whoever lands real B3 geometry to re-check Hood prominence at default zoom.
   - `ContrastRatio.swift`'s `getRed(...)` discarded boolean return (`Support/ContrastRatio.swift:16`) — confirmed real, still present.
   - All 4: **downgraded status unchanged (should-fix, non-blocking)** — none affect core functionality or safety: agree with `ios-code-reviewer`'s original triage.
3. **C11 physical-device measurement** — still outstanding. `xcrun xctrace list devices` from this sandbox shows one physical device, "Aviran Grisaro (27.0)," listed under **Devices Offline** — unreachable, and its OS/model aren't confirmed to be the TRD's assumed A13 class oldest-supported device either way. Third independent simulator-only reproduction in this pass (0.464s). **Confirmed still unverified on real hardware — flagging as the one remaining P0 unverifiable from any sandbox so far.**
4. **Placeholder data (iOS fixture + backend seed)** — confirmed both are toy geometry, not real Tel Aviv boundaries (4 rectangles client-side, 5 rough placeholders in migration 001's seed). Test plan accounted for this: no case above fails a "Hoods look right" geometric check against the placeholder shapes. What *is* newly flagged (see carried-forward item 2's cold-open framing note above) is that the toy fixture's small size relative to the default cold-open camera makes "are Hoods prominent at default zoom" genuinely untestable until real geometry lands — noting this rather than passing or failing it against fake data.

## Unverifiable from this sandbox (explicit list)

- **Live 401/403 behavior on the 3 RPC endpoints** — migrations not applied, no Supabase project/credentials reachable.
- **Physical A13/iPhone-11-class cold-open measurement** — no reachable physical device (one listed, offline, model/OS not confirmed as the right class anyway).
- **Actual stepped-band heat rendering at real densities** — no live or seeded density data anywhere reachable; every observation in this pass is the permanent "no data" state, which is a real and correctly-handled state but not the same as seeing bands 1/2/3 painted and confirming visual step-distinctness.
- **VoiceOver spoken output** — code read confirms the label logic, but this pass did not turn on VoiceOver and listen.
- **Offline-with-cache indicator** — requires a prior successful live fetch to produce a cache file; no backend has ever been reachable at any point in this feature's pipeline to produce one.
- **Hood-boundary hit-testing against real neighborhood shapes** — both the iOS fixture and backend seed are hand-authored placeholders, not real Tel Aviv Hood polygons; hit-testing logic itself is unit-tested against synthetic shapes (concave notch, near-miss tolerance, etc.) but not against what real geometry will actually look like.

## Verdict

**FAIL — one Major finding (Finding A, req 6 recenter-on-grant), one route back to `build` for `ios-developer`.** Everything else in this pass is PASS, matches or exceeds what `code-review` already established, and the 4 carried-forward should-fix items remain correctly triaged as non-blocking. Security and physical-device verification remain explicitly tracked as unverified-from-any-sandbox, not silently dropped.
