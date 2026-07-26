# SALVAGE.md — the Locali codebase, inventoried

Passenger replaces **Locali**, a 16.5k-line Swift app frozen on 2026-07-26. Nothing was deleted. This file exists so that building a Passenger feature costs one `git show`, not a full re-read of a dead codebase.

## Where it lives

| | |
|---|---|
| Repo | `github.com/AviranGrisaro/locali` |
| iOS app | branch `main`, commit `93cedacaf86ecb32948487e472136c292c1740c7` |
| Planning workspace | branch `brain`, commit `0a5696c` |
| Local clone | `../locali-code/` and `../locali-brain/` (kept on disk; safe to delete, GitHub has everything) |

Pull one file without cloning anything new:

```bash
git -C ../locali-code show 93cedac:Locali/Services/DirectionsService.swift
```

## Rules

1. **Leaf code only.** Models, service clients, geo/map math, formatting, color logic. These were mostly fine.
2. **Never salvage architecture.** `AppModel.swift` (855 lines), `MapScreen.swift` (940), `HeatmapControlsSheet.swift` (1069) are the rot — one god-object plus two god-views. Read them to understand a behaviour; never copy their structure.
3. **Read every salvaged line.** Old code is Swift 5 with no strict concurrency. It will not compile under Swift 6 unchanged, and the places it fails are exactly the places it was racy.
4. **Check the verdict before the scope gate, not after.** A file marked BURN is usually marked that way because the feature itself is forbidden by the strategy — salvaging it re-imports the drift.

**Verdicts:** `REUSE` — adapt it, it's sound · `REFERENCE` — read for approach, rewrite from scratch · `BURN` — the feature is out of scope; don't open it except out of curiosity.

## App shell & architecture

| File | Lines | Verdict | Note |
|---|---|---|---|
| `AppModel.swift` | 855 | BURN | The god object. Every feature's state in one `@Observable`. Root cause of the rewrite. |
| `LocaliApp.swift` | 48 | BURN | Replaced by `PassengerApp.swift`. |
| `Branding/LocaliWordmark.swift` | 113 | BURN | Dead brand. |
| `Branding/SplashView.swift` | 154 | BURN | Strategy: no ceremony before the map. |

## Map — the part that matters

| File | Lines | Verdict | Note |
|---|---|---|---|
| `Features/Map/MapScreen.swift` | 940 | REFERENCE | Contains the real answers on annotation clustering and camera handling, buried in a 940-line view. Mine the logic, discard the shape. |
| `Features/Map/HeatmapControlsSheet.swift` | 1069 | REFERENCE | The time-slider behaviour (now → +12h, hour snapping) lives here and is genuinely worked out. Extract the model, not the view. |
| `Features/Map/DensityMark.swift` | 83 | REUSE | Heat mark rendering. |
| `Features/Map/DensityPlaceMark.swift` | 50 | REUSE | |
| `Features/Map/LocalnessBadge.swift` | 178 | REUSE | The five vibe tags, rendered. Matches current strategy wording. |
| `Features/Map/AvoidBadge.swift` | 28 | REUSE | The tourist-trap case. |
| `Features/Map/MapLegend.swift` | 139 | REUSE | Two orthogonal layers, legible. |
| `Features/Map/PlacePin.swift` | 18 | REUSE | |
| `Features/Map/EventMarker.swift` | 73 | REUSE | Events overlay is V1 core. |
| `Features/Map/EventDetailCard.swift` | 211 | REUSE | |
| `Features/Map/RouteBanner.swift` | 198 | REUSE | Scenic View surface. |
| `Features/Map/BottomBar.swift` | 129 | REFERENCE | Tied to the old navigation model. |
| `Features/Map/LocationDisabledBanner.swift` | 94 | REUSE | |
| `Features/Map/AlwaysLocationPrimingSheet.swift` | 130 | BURN | Always-location is Phase 2 at the earliest, and only while en route. |
| `Features/Map/FogOverlay.swift` | 169 | BURN | Fog-of-war exploration — not in the strategy. |
| `Features/Map/RevealPulse.swift` | 45 | BURN | Same. |
| `Features/Map/ExploredMapSheet.swift` | 75 | BURN | Same. |
| `Features/Map/ExplorationDegradedBanner.swift` | 73 | BURN | Same. |
| `Features/Map/FriendBubble.swift` | 109 | BURN | Social. |

## Models

| File | Lines | Verdict | Note |
|---|---|---|---|
| `Models/DensityContract.swift` | 209 | REUSE | The heat/localness split as a type. The single best file in the old codebase — it encodes the "never one blended score" rule the strategy insists on. |
| `Models/HeatPlace.swift` | 165 | REUSE | |
| `Models/HeatState.swift` | 183 | REUSE | |
| `Models/HeatTimeWindow.swift` | 125 | REUSE | Time-slider windowing. |
| `Models/Place.swift` | 79 | REUSE | |
| `Models/VisitedPlace.swift` | 75 | REUSE | |
| `Models/LiveEvent.swift` | 88 | REUSE | |
| `Models/LiveHeatEntry.swift` | 37 | REFERENCE | Live presence is parked — density is synthetic in V1. |
| `Models/PendingConfirmation.swift` | 47 | REFERENCE | Local-QA confirmation loop; re-spec before reusing. |
| `Models/DiscardedVisit.swift` | 17 | REFERENCE | |
| `Models/Friend.swift` | 55 | BURN | Social. |
| `Models/UserProfile.swift` | 20 | BURN | Social. |
| `Models/LocationShare.swift` | 271 | BURN | Social. |

## Services

| File | Lines | Verdict | Note |
|---|---|---|---|
| `Services/DirectionsService.swift` | 263 | REUSE | Walking directions + Scenic View routing. Debugged, and its last commit fixed the deprecated `MKMapItem` init — start from the fixed version. |
| `Services/LocationService.swift` | 252 | REUSE | Permission handling and authorization states, worked out properly. |
| `Services/PlaceSearchService.swift` | 188 | REUSE | |
| `Services/TelAvivPlacesService.swift` | 27 | REUSE | |
| `Services/EventsService.swift` | 140 | REUSE | |
| `Services/SavedPlacesStore.swift` | 55 | REUSE | |
| `Services/VisitedPlacesStore.swift` | 447 | REFERENCE | Large, and entangled with auto-detection that's Phase 3. V1 visited-places is manual. |
| `Services/SupabaseService.swift` | 79 | REUSE | Thin client. Good shape. |
| `Services/CityGeofenceMonitor.swift` | 209 | REFERENCE | Geofencing is Phase 2. Keep the pointer. |
| `Services/VisitDetectionService.swift` | 353 | REFERENCE | Auto-save on 20-min dwell is explicitly Phase 3. |
| `Services/VisitCandidateRanker.swift` | 168 | REFERENCE | Same. |
| `Services/VisitConfirmationCoordinator.swift` | 276 | REFERENCE | Same. |
| `Services/LiveHeatService.swift` | 25 | REFERENCE | Density is synthetic in V1. |
| `Services/LivePresenceReporter.swift` | 154 | REFERENCE | Same. |
| `Services/LocationEmitter.swift` | 137 | REFERENCE | Same. |
| `Services/ExplorationService.swift` | 127 | BURN | Fog-of-war. |
| `Services/ExploredCellsStore.swift` | 235 | BURN | Fog-of-war. |
| `Services/AuthService.swift` | 387 | BURN | Built for social sign-in. If V1 needs identity for saved places, spec it fresh — anonymous-first. |
| `Services/GoogleSignInConfig.swift` | 50 | BURN | |
| `Services/UsernameService.swift` | 62 | BURN | Social. |
| `Services/FriendsService.swift` | 298 | BURN | Social. |
| `Services/SupabaseFriendsService.swift` | 297 | BURN | Social. |
| `Services/AudienceService.swift` | 164 | BURN | Social. |
| `Services/SupabaseAudienceService.swift` | 354 | BURN | Social. |
| `Services/IncomingSharesService.swift` | 55 | BURN | Social. |
| `Services/SupabaseIncomingSharesService.swift` | 176 | BURN | Social. |
| `Services/ShareNotificationService.swift` | 92 | BURN | Social. |

## Support

| File | Lines | Verdict | Note |
|---|---|---|---|
| `Support/HeatField.swift` | 47 | REUSE | Heat interpolation math. |
| `Support/HeatRamp.swift` | 29 | REUSE | Heat colour ramp. |
| `Support/Color+Theme.swift` | 87 | REUSE | |
| `Support/ContrastRatio.swift` | 70 | REUSE | Accessibility check for heat-over-map legibility — worth keeping, easy to forget to rebuild. |
| `Support/Format.swift` | 147 | REUSE | |
| `Support/AppClock.swift` | 44 | REUSE | Injectable clock — the time slider needs it and it makes the tests deterministic. |
| `Support/FailableDecodable.swift` | 60 | REUSE | Boundary-validation helper. |
| `Support/SupabaseDecoding.swift` | 42 | REUSE | |
| `Support/ExternalMaps.swift` | 22 | REFERENCE | Strategy: Scenic View routes in-app, not a hand-off. Keep only as a fallback. |
| `Support/MunicipalBoundary.swift` | 187 | REUSE | Tel Aviv boundary polygon. |
| `Support/HexGrid.swift` | 516 | REFERENCE | Built for fog-of-war, but it's generic hex math. Useful if heat ever aggregates into cells. |
| `Support/DevToggles.swift` | 163 | REFERENCE | |
| `Support/FeatureFlags.swift` | 143 | REFERENCE | Was mostly used to hide the social layer. Rebuild only if something actually needs flagging. |
| `Support/FriendInviteLink.swift` | 19 | BURN | Social. |

## Everything else in the old app

`Features/Auth/`, `Features/Friends/`, `Features/Profile/`, `Features/Share/` (≈2,300 lines total) — all BURN. Social sign-in, friend graph, profile avatars, and location sharing. Every one of them is forbidden by the current strategy, and building them is what triggered this reset.

`Features/Onboarding/LocationPrimingView.swift` (67) and `LocationDeniedView.swift` (74) — REFERENCE. The strategy allows the location permission prompt; it forbids everything around it.

`Features/Places/` — mixed: `PlaceDetailCard` (85) and `SavedPlacesSheet` (84) REUSE; `DiscoverSheet` (126), `VisitedPlaceRow` (128), `VisitedSegment` (189) REFERENCE; the confirmation/visit-candidate views REFERENCE pending a fresh local-QA spec.

## Supabase migrations

Old schema: 26 migrations, `locali-brain/06-database/`, branch `brain`. Passenger starts at `001` from scratch. Verdicts by group:

| Migration group | Verdict | Note |
|---|---|---|
| `001_init_users_and_tel_aviv`, `002_seed_tel_aviv_places` | REUSE | The places table and Tel Aviv seed — the most expensive data to recreate. Start here. |
| `022_create_neighborhoods`, `023_add_localness_and_neighborhood`, `024a_seed_neighborhoods_placeholder` | REUSE | Zone blurbs + localness are V1 core. |
| `005_add_avoid_to_tel_aviv`, `016_add_activity_score` | REUSE | Tourist-trap flag, activity score. |
| `017_create_place_candidates`, `018_add_provenance`, `019_place_promotion_functions`, `020–021 places ingest` | REUSE | The place-sourcing pipeline. Non-trivial and still in scope. |
| `006_create_events`, `007_schedule_events_ingest` | REUSE | Events overlay is V1 core. |
| `009_create_visited_places`, `026_add_user_confirmed` | REFERENCE | V1 visited-places is manual; re-spec. |
| `010_create_presence_pings`, `011_create_live_heat`, `012_schedule_live_heat_aggregate` | REFERENCE | Density is synthetic in V1. Revisit when a live source is chosen. |
| `008_create_explored_cells` | BURN | Fog-of-war. |
| `013_create_friends_graph`, `014_create_location_shares`, `015_schedule_location_share_sweeps` | BURN | Social. |
| `003_skeleton_ping`, `004_drop_skeleton_ping` | BURN | Scaffolding, already reverted. |

Also worth pulling before writing `001`: `06-database/gen_heat.py` and `tel-aviv-places-heat.json` — the synthetic density generator and its output.
