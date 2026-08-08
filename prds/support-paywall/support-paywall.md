# Support-the-project prompt (voluntary $5 Apple IAP) — PRD

**Status:** Draft v1
**Phase:** [Phase 1 — Build to launch](../../strategy/passenger-strategy.md#strategic-phasing)
**Build phase:** 1 — client-side only (StoreKit 2 IAP is a client + App Store Connect config change; no backend table needed for a single non-consumable/consumable product).
**Owner:** Aviran Grisaro
**Linear:** [PAS-94](https://linear.app/passenger-app/issue/PAS-94/support-the-project-paywall-dollar5-one-time-apple-iap-on-app-start-no) · **Board:** T-092
**Note:** a near-simultaneous duplicate ticket, `PAS-95`, was filed by a concurrent session ~1 minute after this one and is now marked Duplicate of `PAS-94`. `PAS-94` is canonical.
**Last updated:** 2026-08-08
**Scope ruling:** this PRD exists on a direct, live founder instruction (see Decisions log) that runs against locked decision #9 below — flagged, not silently reconciled.

## Description

- A screen shown once at app start (cold open, before or alongside the location-permission prompt — exact ordering is Q1) asking the user to voluntarily support the project with a one-time $5 payment via Apple (StoreKit 2 in-app purchase).
- Framed entirely as **support, not purchase** — no feature, content, or capability is on the other side of it. No ads exist to remove, no premium tier exists to unlock.
- **Fully skippable.** Dismissing it costs the user nothing — same app, same functionality, whether they pay or not.
- One-time, one price ($5), not a subscription.

**Not in scope:** any feature gate, ad removal, premium tier, or content unlock of any kind; recurring/subscription billing; any price other than the single $5 tier; a paywall that blocks or delays reaching the map; backend receipt-validation infrastructure (P1 default is client-side StoreKit 2 transaction verification only — see Technical design); analytics beyond a single conversion event (full instrumentation is a P1-nice-to-have, not required for ship).

## Motivation

- Direct founder instruction, verbatim, live chief-of-staff chat, 2026-08-08 (full quote in `agent-os/PROGRESS.md`'s matching L-002 stub, `passenger-brain 8309e5e`): *"do we have paywall? for now i want paywall for support our project, it will pop on start with 5$ payment, there are not ads or premium feature (for p1). so the paywall is a request of supporting this project. create ticket for paywall (pay with apple)."*
- **This directly conflicts with locked decision #9** (`strategy/decisions.md`): *"Free V1, monetization deferred (RevenueCat dormant) — Paywall is a later phase with real city coverage. Reconfirmed directly by Aviran, 2026-07-26: no paywall/unlock/trial gate anywhere in Phase 1."* This PRD does not resolve that conflict — it ships the ticket per this run's brief and surfaces the conflict for Aviran to reconcile (either amend #9 himself, or confirm the two coexist because this isn't a *gate* — it unlocks nothing, so "paywall" in #9's sense may not apply to it. That reading is **not** assumed here; it's Q2 below, his call.)
- No paywall/IAP/StoreKit code exists anywhere in the client today (verified live: grepped all `*.swift` under `passenger-code` for `storekit`, `"in-app purchase"`, `paywall`, `Product.purchase` — zero hits) and no prior ticket covers this (Linear search, `PAS`, "paywall"/"support"/"IAP" — zero existing issues).

## Requirements

### Must-have (P0)

1. **Shown once per install, at app start.**
   - [ ] First cold open after install shows the prompt. Exact ordering relative to the location-permission prompt is Q1 (open).
   - [ ] Does not reappear on subsequent launches once dismissed or purchased (persisted locally — `UserDefaults`/similar, no backend needed).

2. **Fully skippable, no gate.**
   - [ ] A visible, always-enabled "Not now" / "Skip" (or equivalent) control dismisses the prompt with zero effect on app functionality.
   - [ ] The map, search, and every other P1 feature work identically whether the user pays, skips, or never sees the prompt again.

3. **One product, one price, one-time.**
   - [ ] A single StoreKit 2 product, $5 USD tier (or Apple's nearest equivalent in the user's storefront currency), purchased through Apple's standard payment sheet.
   - [ ] Not a subscription — no recurring billing, no trial, no auto-renew.

4. **Framing is honest — "support," never "unlock."**
   - [ ] Copy states plainly that this is a voluntary contribution to the project, not a purchase of anything the user doesn't already have.
   - [ ] No claim of ad removal, feature unlock, or premium status anywhere in the copy (there is nothing to claim — no ads or premium tier exist in P1).

5. **Purchase completes or fails cleanly.**
   - [ ] A successful purchase shows a short thanks/confirmation state, then proceeds into the app exactly as skip would.
   - [ ] A failed or cancelled purchase (network error, user cancels Apple's sheet, etc.) returns the user to the prompt or proceeds to skip — never stalls or crashes.
   - [ ] Handles StoreKit 2's transaction verification (`VerificationResult`) — an unverified transaction is treated as failed, not silently accepted.

### P1 / nice-to-have

- Restore-purchases affordance (mostly moot for a non-gating one-time IAP, but Apple reviewers sometimes expect it if any IAP exists — Q3).
- A single analytics event on prompt-shown / accepted / skipped.
- A supporter acknowledgment the user can find later (e.g. a line in Settings/About) rather than only a one-time thanks screen — depends on Q4/framing (a) below.

## Technical design

- **StoreKit 2** (`StoreKit` framework, `Product`, `Transaction`, async/await purchase flow) — no third-party SDK, no RevenueCat (strategy already flags RevenueCat as "dormant," reserved for the real Phase 2 subscription per decision #9/#21).
- Product configured in App Store Connect as a single **non-consumable** IAP (a one-time "supported the project" purchase reads more naturally as non-consumable than consumable — Aviran/App Store Connect setup, not a code decision).
- Client-side transaction verification only for P1 (`Transaction.currentEntitlements` / `VerificationResult.verified`); no backend receipt validation, no server-side entitlement store — nothing is gated, so there is no security surface a client-only check would leave open. If this changes to unlock anything in a later phase, backend validation becomes required at that point, not now.
- Local persistence for "already shown/decided" state — a `UserDefaults` flag or similar, no schema/migration needed.
- **App Store Connect setup itself (creating the IAP product, price tier, submission metadata) is Aviran's/an external-account action** — same class of action this fleet cannot perform (blocked-on-aviran, per standing rule on App Store/credentials).

## Open questions & risks (Aviran)

- **Q1 — placement.** Aviran said "pop on start." Before the location-permission prompt, after it, or on its own separate screen? **[ASSUMPTION]** default to *after* location permission (don't stack two system-level interruptions before the map ever renders) — flag for override.
- **Q2 — does this actually conflict with decision #9, or does #9's "paywall" mean specifically a feature gate?** This PRD ships regardless per this run's brief; the strategy doc itself is not edited here (Aviran-gated, and the standing rule on gated-file edits — an agent doesn't self-resolve this). Needs his explicit call: amend #9, or confirm a non-gating support ask isn't what #9 was locking down.
- **Q3 — App Store rejection risk, real and the reason this ticket is `aviran-blocker`.** Apple's App Review Guidelines (3.1.1 and related) have a documented history of rejecting in-app purchases that unlock nothing tangible, treating a "just give us money" IAP as functionally indistinguishable from a disguised donation button — and Apple requires **donations** to go through Apple Pay or an approved nonprofit/charitable-giving flow, not the IAP mechanism, unless the payer receives something of value in return. Three framings, all buildable, ships regardless of which Aviran picks — **but which one ships is his call, not this PRD's:**
  - **(a) StoreKit 2 IAP with a token unlock** — e.g. a supporter badge somewhere in the app, or a dedicated "thanks" screen/acknowledgment the payer can revisit. Closest to what Aviran described ("pay with apple," IAP mechanism) while giving Review something to point to as the purchased good. Small scope add (a badge or an about-page line) beyond what's specced above.
  - **(b) Apple Pay donation flow instead of IAP** — genuinely a donation, sidesteps 3.1.1 entirely, but is not "in-app purchase" in Apple's technical sense (different framework, `PassKit`/Apple Pay, not `StoreKit`) — a different build than what's specced above.
  - **(c) Keep it purely skippable with no purchase mechanism in P1** — ship the prompt as pure messaging/awareness ("if you'd like to support us, [link out]" or nothing at all), defer any real money-collection to when Aviran picks (a) or (b). Lowest risk, least useful for actually collecting $5s.
  - This PRD specs (a)'s shape by default since it's closest to the literal ask ("pay with apple," StoreKit) and the P0 requirements above are written to (a). If Aviran picks (b) or (c), requirements 3/5 and the Technical design section need a follow-up revision — noted here so that revision isn't a surprise.
- **Q4 — copy/creative.** Exact prompt wording, whether a supporter badge/acknowledgment ships (ties to Q3a), and visual treatment are all undecided — no PRD requirement locks specific copy; `ios-developer` proposes reasonable default text if Aviran doesn't supply it, flagged `[ASSUMPTION]` in the build.

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-08-08 | PRD opened, ships despite unresolved conflict with decision #9 | Direct founder instruction to create the ticket now; the strategy-level conflict (Q2) and the App Store framing risk (Q3) are both routed to Aviran rather than resolved by this PRD or a code decision. |
