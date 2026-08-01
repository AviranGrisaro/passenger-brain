# Analytics — Event Taxonomy & Supabase Tables

**Owner:** `analytics-engineer`
**Status:** Draft v1 — first pass across all written V1 PRDs, 2026-08-01. No table exists yet; no migration has been written. This is the spec `developer` builds from once requested.
**Why this exists:** no analytics pipeline exists in Passenger today. `prds/search-quick-filters/search-quick-filters.md` names the gap directly — decision #23 makes search a watch-item ("reaching for search before reading the map means the map failed") and nothing in V1 measures it. Every other PRD is equally silent. This doc is the first cut at closing that gap for all of V1, not just search.

## North star

Strategy, verbatim: *"Nothing else matters until we know if a real person reopens the app within a week, unprompted."* Every table and event below exists in service of measuring that one number (7-day unprompted return) and the funnel that leads to or away from it. If an event doesn't trace to this or a named PRD risk/KPI below, it doesn't belong here.

## Identity constraint (load-bearing)

**V1 has no accounts.** Every table keys on an anonymous **`install_id`** — the same identifier `local_qa_answers` already uses (`prds/tourist-trap-flag/tourist-trap-flag.md`). No user id, no email, no cross-install identity. This is not a simplification to revisit later; it's the same "no accounts/login" constraint the whole product is built under (`CLAUDE.md` standing prohibitions).

## Tables

### `app_installs`
One row per device install. Written once, on first launch.

| Column | Type | Notes |
|---|---|---|
| `install_id` | uuid, PK | Client-generated, persisted in SwiftData. Lost on reinstall — same loss Places/Passport already accept. |
| `first_seen_at` | timestamptz | First cold launch. |
| `platform` | text | `ios` only in V1. |
| `app_version` | text | For version-correlated funnel breaks. |

RLS: insert-only (client can create its own row, never read another's), no update, no delete.

### `app_sessions`
One row per app session. Powers DAU/WAU and the north-star retention calc.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid, PK | |
| `install_id` | uuid, FK → `app_installs` | |
| `started_at` | timestamptz | App entered foreground. |
| `ended_at` | timestamptz, nullable | App backgrounded; null while session is open. |
| `launch_source` | text | `icon` \| `notification` (local-QA) \| `deep_link` (none in V1 — future-proofing only if a real source exists; don't add a column nobody writes). |

RLS: insert/update own row only (client updates `ended_at` on background), no select.

### `app_events`
The generic event log. Every discrete user or system action below is one row here — no per-feature tables. Keeps the taxonomy centralized instead of one table per PRD.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid, PK | |
| `install_id` | uuid, FK → `app_installs` | |
| `session_id` | uuid, FK → `app_sessions`, nullable | Null only for events that can legitimately fire outside a foreground session (a local-QA answer queued offline and synced later). |
| `event_name` | text | `snake_case`, from the catalog below. Constrained by a check or enum once the catalog stabilizes — don't let free-text event names drift. |
| `properties` | jsonb | Event-specific payload, see catalog. No raw location, no raw search text, no PII — see Privacy rules in the agent file. |
| `occurred_at` | timestamptz | Client-stamped, not `now()` at insert, so offline-queued events keep their real time. |

RLS: insert-only, no client select — client never reads its own history back; founders/aggregate views use a service-role or SQL-editor path, not the anon key.

### `kpi_daily_active_installs` (view, not a table)
`select date_trunc('day', started_at) as day, count(distinct install_id) from app_sessions group by 1`. DAU. WAU is the same windowed to 7 days.

### `kpi_weekly_retention` (view, not a table)
For each `install_id`, `first_seen_at` from `app_installs` vs. the next `app_sessions.started_at` at least 1 day and at most 7 days later. The percentage with at least one such session **is the north-star number**. This is the one dashboard query that matters more than any other in this document.

## Event catalog

Every event below is a row in `app_events`. Grouped by the PRD that specs the interaction. `[system]` marks events fired by app logic, not a tap — still worth logging, since they're what proves a background mechanic (dwell detection, flag correction) is actually working.

### App lifecycle
| Event | Properties | Fires when | Serves |
|---|---|---|---|
| `app_opened` | `launch_source` | Cold launch, first frame interactive | Session start; north-star retention |
| `app_backgrounded` | `session_duration_s` | App leaves foreground | Session length distribution |
| `location_permission_prompted` | — | System prompt shown (map PRD req 6) | Permission funnel |
| `location_permission_resolved` | `result: granted\|denied` | User answers the system prompt | Permission funnel; segments every downstream metric by granted/denied |

### Map & heat (`map-hoods-heat`)
| Event | Properties | Fires when | Serves |
|---|---|---|---|
| `hood_tapped` | `hood_id` | Tap opens a Hood sheet, any door | Which Hoods get explored |
| `map_recentered` | — | Near-me button (P1) | Engagement with live-location surface |

### Time slider (`time-slider`)
| Event | Properties | Fires when | Serves |
|---|---|---|---|
| `slider_opened` | `entry: heat_button\|edge_left\|edge_right` | Control becomes visible | Which of the two entry paths people actually use — directly informs Q1/Q8's open discoverability question |
| `slider_hour_changed` | `to_offset_h` (0-12) | Hour selection changes | Whether "planning ahead" gets used vs. "now" only |
| `slider_dismissed` | `final_offset_h` | Control closes | Pairs with `_changed` to see if people explore then revert to now |

### Hood & place detail (`hood-place-detail`)
| Event | Properties | Fires when | Serves |
|---|---|---|---|
| `place_modal_opened` | `place_id, entry: pin_tap\|hood_list_row\|search_result\|places_list` | Modal opens | Core "did the map deliver a place worth looking at" funnel step |
| `place_saved` | `place_id, source: modal` | Save tapped | Activation signal; feeds `places_been_saved` |
| `place_unsaved` | `place_id` | Un-save tapped | Save-quality signal (immediate un-saves = bad recommendation) |
| `place_route_requested` | `place_id, target_app: maps\|waze, result: opened\|no_app_available` | Route action tapped | **Intent-to-visit conversion** — the strongest "this worked" signal V1 has, since there's no purchase/booking event to fall back on |

### Tourist-trap flag & local QA (`tourist-trap-flag`)
| Event | Properties | Fires when | Serves |
|---|---|---|---|
| `local_qa_notification_fired` `[system]` | `place_id` | Geofence-verified visit triggers the ask | Cold-start tracking — PRD names this as an unmitigated risk |
| `local_qa_toast_answered` | `place_id, answer: yes\|no` | User taps Yes/No | **Local-QA participation rate** — directly measures the cold-start/incentive risk both `tourist-trap-flag` and `passport` PRDs flag as open and unresolved |
| `local_qa_toast_ignored` | `place_id` | Toast auto-dismisses unanswered | Same participation metric, the denominator's other half |

### Places — Been & Saved (`places-been-saved`)
| Event | Properties | Fires when | Serves |
|---|---|---|---|
| `place_been_recorded` `[system]` | `place_id, hood_id` | 20-min dwell verified | Real-world usage signal independent of any tap — the closest V1 gets to "did they actually go" |
| `place_visited_recorded` `[system]` | `place_id, hood_id` | Geofence visit under the Been threshold | Weaker signal, same funnel |
| `places_list_opened` | — | Places icon tapped | Feature engagement |
| `places_list_row_tapped` | `place_id, provenance: saved\|been\|visited` | Row opens a place modal | Return-visit behavior — does yesterday's save get revisited |

### Passport (`passport`)
| Event | Properties | Fires when | Serves |
|---|---|---|---|
| `passport_opened` | — | Profile tab tapped | Habit-loop engagement — the PRD itself flags "V1 has no habit loop" as a named risk; this is how you'd see if Passport is fixing that |
| `sticker_earned` `[system]` | `place_id, place_type` | Been row created (mirrors `place_been_recorded`) | Progression signal |
| `hood_local_status_reached` `[system]` | `hood_id` | Per-Hood threshold crossed | Milestone completion rate |
| `passport_all_local_reached` `[system]` | — | Every designated Hood reaches Local | Top-of-funnel "finished the game" rate — expect this near zero at launch, useful once thresholds are tuned |

### Search & quick filters (`search-quick-filters`)
| Event | Properties | Fires when | Serves |
|---|---|---|---|
| `search_opened` | `seconds_since_launch` | Search icon tapped | **Directly answers decision #23's named gap** — "reaching for search means the map failed." A high rate of `search_opened` early in a session is the map underperforming. |
| `search_query_submitted` | `query_length_bucket, result_count` | Debounced match completes | Zero-result rate, query volume — never the raw string (privacy) |
| `search_chip_toggled` | `chip: eat_drink\|things_to_do, state: on\|off` | Chip tapped | Category demand signal |
| `search_result_selected` | `result_type: place\|hood, result_id` | Row tapped | Search's own conversion rate |

### Live events overlay (`live-events-overlay`, client ships Build Phase 1 with fake/empty data)
| Event | Properties | Fires when | Serves |
|---|---|---|---|
| `events_layer_toggled` | `state: on\|off` | Toggle in heat modal | Feature adoption once the pipeline (`live-events-pipeline`) is live |
| `event_marker_tapped` | `event_id` | Marker tapped | Engagement with the layer |
| `event_route_requested` | `event_id, target_app` | Route action in event detail | Same intent-to-visit signal as `place_route_requested` |

## KPI rollups (what to actually look at)

- **North star — W1 unprompted return:** `kpi_weekly_retention` view. The only number Phase 1 exists to produce (strategy, "Right now").
- **Activation:** share of installs with `location_permission_resolved` (granted) → `place_modal_opened` in the same session. Proxy for "map delivered something worth looking at" on day one.
- **Map-failure signal:** share of sessions with `search_opened` inside the first ~30s. Decision #23's own watch-item, made measurable.
- **Local-QA health:** `local_qa_toast_answered` / (`local_qa_toast_answered` + `local_qa_toast_ignored`). Both `tourist-trap-flag` and `passport` name cold-start/no-incentive as unresolved risks; this is the number that tells you if the risk is materializing.
- **Intent-to-visit conversion:** `place_route_requested` / `place_modal_opened`. Best available "this recommendation worked" proxy without booking/purchase data.
- **Habit-loop signal:** `passport_opened` repeat rate per install per week. Passport's own PRD names "no habit loop" as what it's supposed to fix — this checks whether it does.
- **Save quality:** `place_unsaved` within N minutes of `place_saved`, as a share of all saves.

## What's deliberately not tracked

- Raw search query text, raw GPS coordinates in event properties, anything that would require accounts — all excluded per the Privacy section in the `analytics-engineer` agent file (`.claude/agents/analytics-engineer.md`).
- Scenic Walk and TikTok import events — both features are still held (Aviran's ship-vs-slip / ToS calls), not written PRDs yet. Add their events once a PRD exists, not before.
- `live-events-pipeline`'s ingest-side metrics (source freshness, dedup rate) — that's `data-engineer`'s operational monitoring, not user-facing product analytics, and belongs in that PRD's own TRD, not here.

## Next steps

1. `analytics-engineer` opens a `type:analytics-request` Linear issue for `developer`: the four tables above (`app_installs`, `app_sessions`, `app_events`, plus the two views), RLS as specified.
2. Per-feature `ANALYTICS.md` files (mirroring `qa`'s `TEST-PLAN.md` convention) get written into each PRD's own folder as each feature reaches `design-review`, elaborating the relevant rows above into exact trigger conditions — this doc is the taxonomy, not the last word per feature.
3. `ios-developer` instruments the client calls once schema lands; `qa` verifies each event fires with correct properties as part of normal acceptance.
