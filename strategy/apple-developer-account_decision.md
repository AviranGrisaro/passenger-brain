# Decision: Apple Developer account — personal vs. Organization

**Date:** 2026-07-30
**Owner:** Aviran Grisaro
**Status:** Locked for now — revisit when incorporating
**Type:** Two-way door (fully reversible via App Transfer, see below)

## Decision

Register Passenger under Aviran's **personal Apple ID** (Individual Developer Program) now. Defer creating an Organization Apple Developer account until the company is incorporated. Transfer the app to the Org account later via App Store Connect's app transfer feature.

## Why

- Individual enrollment is instant — no legal entity, no D-U-N-S number, no waiting.
- Organization enrollment requires a D-U-N-S number (free, but up to ~7 business days) and a qualifying legal entity, which doesn't exist yet.
- Waiting on incorporation to start shipping would block the whole timeline for a business-structure question, not a product one.
- The transfer path is well-defined and reversible — no lock-in from starting personal.

## What "Organization" requires, when the company exists

Apple's own wording: *"your business must be recognized as a legal entity (such as a corporation, limited partnership, or limited liability company)"* — sole proprietors are explicitly told to enroll as Individual, not Organization. [Source](https://developer.apple.com/help/account/membership/D-U-N-S)

Entity types checked for Israel:

| Entity | Separate legal entity? | Qualifies for Apple Org? | Notes |
|---|---|---|---|
| עוסק פטור (exempt dealer) | No — legally still the person | No | Apple says use Individual |
| עוסק מורשה (licensed dealer) | No — legally still the person | No | Apple says use Individual |
| שותפות (general partnership) | Yes | Not explicitly listed by Apple | Apple's examples name "limited partnership," not general partnership — untested, some risk |
| שותפות מוגבלת (limited partnership) | Yes | Yes, per Apple's wording | Needs a general partner with unlimited personal liability — poor fit for 4 co-founders splitting equity |
| חברה בע"מ (Ltd) | Yes | Yes | Standard choice for Israeli tech startups; limited liability for all founders |

**No cheaper Israeli entity gives the same limited-liability + Apple-eligible result as חברה בע"מ.** The only genuine alternative to Ltd, if avoiding it, is registering a US LLC instead (e.g. via Stripe Atlas) — also Apple-eligible, but adds Israeli foreign-entity tax reporting complexity.

## Cost, if/when incorporating in Israel (Ltd)

- Companies Registrar registration fee: ~2,200 ILS one-time ([Rasham HaChavarot](https://www.gov.il/he/departments/units/registrar_of_companies))
- Annual report fee: ~1,250 ILS/year
- D-U-N-S number: free ([Apple D-U-N-S guide](https://developer.apple.com/support/D-U-N-S/))
- Apple Developer Program: $99/year (same for Individual and Organization)
- Lawyer/accountant for incorporation docs: optional, commonly ~1,500–3,000 ILS if used

No US registration is required for any of this — Apple accepts a legal entity from any country.

## How the later transfer works

Apple's App Transfer moves the app between developer accounts (e.g. personal → Org) while it stays live on the App Store — ratings, reviews, and update delivery to existing users are preserved.

Eligibility requirements ([Apple's transfer criteria](https://developer.apple.com/help/app-store-connect/transfer-an-app/app-transfer-criteria)):
- App must have **at least one version already released** to the App Store — can't transfer a never-submitted app.
- App can't be mid-review (Waiting for Review / In Review / Accepted / Pending Release states) at time of transfer.
- Both accounts' Apple agreements must be current, neither account in a pending/changing state.
- In-App Purchase product IDs on the app can't collide with IDs already in the receiving account (moot for a first transfer into a fresh Org account).

**[ASSUMPTION]** TestFlight external tester lists and Game Center configuration are not explicitly documented as transferring — plan to rebuild these after the transfer rather than assume continuity.

## Trigger to revisit

Revisit this decision when:
- The company is legally incorporated (Ltd or otherwise), and
- Passenger has at least one version released to the App Store (transfer prerequisite).

At that point: get the Org's D-U-N-S number → enroll Organization on Apple Developer Program → initiate App Transfer from the personal account.

## Sources

- [Apple: D-U-N-S Number requirements](https://developer.apple.com/support/D-U-N-S/)
- [Apple: Program enrollment](https://developer.apple.com/help/account/membership/program-enrollment/)
- [Apple: Compare memberships](https://developer.apple.com/support/compare-memberships/)
- [Apple: App transfer criteria](https://developer.apple.com/help/app-store-connect/transfer-an-app/app-transfer-criteria)
- [Apple: Overview of app transfer](https://developer.apple.com/help/app-store-connect/transfer-an-app/overview-of-app-transfer)
- [Israel Registrar of Companies (Rasham HaChavarot)](https://www.gov.il/he/departments/units/registrar_of_companies)
- [כל-זכות: עוסק פטור](https://www.kolzchut.org.il/he/%D7%A2%D7%95%D7%A1%D7%A7_%D7%A4%D7%98%D7%95%D7%A8)
- [כל-זכות: עוסק מורשה](https://www.kolzchut.org.il/he/%D7%A2%D7%95%D7%A1%D7%A7_%D7%9E%D7%95%D7%A8%D7%A9%D7%94)
