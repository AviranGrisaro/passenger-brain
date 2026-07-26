# Passenger V1 — Decision Record

**Status:** Locked (grilled with Aviran, 2026-07-22)
**Owner:** Aviran Grisaro
**Source brief:** Passenger Product Brief (V1 / V1.5 / V2, iOS only)
**Linear:** superseded — this record predates the 2026-07-26 reset. The original issues (LOC-79 … LOC-99) live in the archived `locali-app` workspace; current work is in workspace `passenger`, team `PAS`, project **Passenger V1**.

> **Amended 2026-07-26 — the reset.** Decision #1 is **reversed**: Passenger is a greenfield build, not a repositioning. The Locali codebase was frozen (`github.com/AviranGrisaro/locali`) and `passenger-code` started from an empty Xcode project. Reason: ten of the 27 PRDs built against that codebase specified features the strategy forbids, and the drift was structural rather than cosmetic — a god object plus two god views, wired through a social layer that was never supposed to exist.
>
> Knock-on effects on the rows below: **#3** no longer means "flag off" — the social code isn't in the new repo at all, and `FeatureFlags.swift` doesn't exist. **#5** is superseded by the strategy's current line — localness is "algorithm plus local QA, together," crowdsourced from users, not hand-curated by a curator. **#15** is executed as of this date.
>
> Every other row still stands. The rows are kept verbatim as the record of what was decided when; read this note first.

## What this is

Passenger is a **repositioning of the existing `locali-code` app**, not a greenfield build. The brief's V1 (interactive map, now→+12h time slider, density heatmap, tap-a-zone, native-maps hand-off, two categories) is ~70% already built. This project captures the **delta** work to refocus Locali into the tourist "you just landed, immediately know where the locals are" product — and to rebrand it to **Passenger**.

Locali's own strategy was already tourist-first ("where should I walk right now to find the real local vibe?"). What drifted is the *code* — it accreted friends, live-presence, and fog-of-war exploration that appear in neither the strategy nor the brief. Passenger refocuses back to the core.

## Locked decisions

| # | Decision | Notes |
|---|---|---|
| 1 | Reposition existing `locali-code`, not greenfield | — |
| 2 | Map encodes **two orthogonal layers**: heat = crowd density, tag = localness | Packed ≠ good; the tourist trap is the packed-touristy spot. The whole differentiator. |
| 3 | Social layer (friends, live-presence, fog-of-war) → **flag off, not delete** | Off through V2 — no "preserved for V1.5/V2" framing; any return is an undecided future call, beyond V2. Uses FeatureFlags.swift. Superseded by strategy's "No social. No B2B. Full stop." (2026-07-23, direct from Aviran). |
| 4 | Density = external popular-times provider (**TBD spike**); ship a **synthetic feed** for now, **time-bound to the slider hour** | First-party presence deferred (empty at launch). |
| 5 | Localness = **hand-curated for V1**; scraping/algo = **parallel gated spike** | The curator IS the definition of "local" for V1. Algo must beat the hand-curated rank-order before it ships. |
| 6 | Vibe tags (5): **super local · very local · mixed · touristy · tourist trap** | "Tourist trap" is an addition beyond the brief's 4 named. |
| 7 | Launch **Tel Aviv only**; foreign city = fast-follow | Portability proof → existing Multi-City Expansion project. |
| 8 | Cold-open **straight to Tel Aviv map** — no sign-in, no onboarding, no permission gate; lazy location; fading "Tel Aviv, right now" title | — |
| 9 | **Free V1**, monetization deferred (RevenueCat dormant) | Paywall is a later phase with real city coverage. Reconfirmed directly by Aviran, 2026-07-26: no paywall/unlock/trial gate anywhere in Phase 1; subscription (not per-city) introduced starting Phase 2. |
| 10 | "Local read" on tap = **hand-curated neighborhood blurb** | — |
| 11 | **Exactly two categories**: Food & drinks / Things to do | — |
| 12 | Localness granularity = **neighborhood + spot** | Bounded curation: dozens of neighborhoods + key spots, not every hex cell. |
| 13 | Hero screen = **density heat base + localness accent + tap-to-read** | — |
| 14 | **Keep events as a live layer** — reconciled as a time-sensitive overlay on the slider, NOT a third category | Deviation from brief. Watch-item. |
| 15 | **Rebrand Locali → Passenger** | Wordmark, app name, icon, App Store identity. |
| 16 | **Keep Saved + Visited places**; strip only V1.5 target-proximity geofencing | Deviation from brief ("saved lists out of scope"). Visited populates only after lazy location grant. CityGeofenceMonitor stays. |
| 17 | **No gradients anywhere** — heat = stepped bands / flat cells | Supersedes T-024 gradient-heatmap request. |

## Knowing deviations from the brief

- **Events kept** (brief: two categories only, that's the whole taxonomy).
- **Saved + Visited kept** (brief: saved lists out of scope for V1).
- **"Tourist trap"** tag added (brief names 4 + "etc.").
- **V1 does not live-scrape** — the "from TikTok / local-language" north star is delivered via hand-curation in V1; the real pipeline is the C4 spike.

## Critical path

C4 (localness algo) is the risk and a gate — but a research track, not a V1 blocker. C1 (synthetic density) + B1 (design) start day 1 in parallel. Epic A (shell) can start immediately (our own code). B3–B5 join on C1 + C3. Design unblocks build flow-by-flow.

## Ticket map (LOC team)

- **Epic A — Shell** (LOC-79): A1 cold-open (LOC-83) · A2 flag-off social + V1.5 proximity (LOC-84) · A3 two categories (LOC-85) · A4 rebrand (LOC-86) · A5 supersede T-024 (LOC-87)
- **Epic B — Two-layer map** (LOC-80): B1 tag+non-gradient design (LOC-88) · B2 hero flow (LOC-89) · B3 accent + tap-zoom (LOC-90) · B4 blurb + tagged spots (LOC-91) · B5 spot tag + hand-off (LOC-92)
- **Epic C — Data** (LOC-81): C1 synthetic density + contract (LOC-93) · C2 provider spike (LOC-94) · C3 hand-curated localness (LOC-95) · C4 define-local spike+gate (LOC-96) · C5 events overlay (LOC-97)
- **Epic D — Validate** (LOC-82): D1 QA acceptance (LOC-98) · D2 success metric (LOC-99)

## Related existing Linear projects

- **Flag off / de-scope for V1:** Follow Friends & Locations, Onboarding Flow, Auth & Login, Live Heatmap (cross-user aggregation).
- **Reuse:** Map Screen, Heatmap & Live Events.
- **Defer, keep dormant:** Paywall & Monetization.
- **Foreign fast-follow:** Multi-City Expansion.
