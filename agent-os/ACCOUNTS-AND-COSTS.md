# Accounts, seats & costs — four founders

Every external account the team touches: who's on it, who pays, what it costs, what's still open. Companion to `ONBOARDING.md` (which covers *how* to get set up); this doc covers *what has to exist and be paid for*. Aviran owns every money decision here.

**Last updated:** 2026-07-26.

## The table

| Account | Needed for | Seats needed | Cost | Status |
|---|---|---|---|---|
| **GitHub** | Both repos (`main` = app, `brain` = planning) | 4 collaborators, write | $0 — free tier covers a private repo with collaborators | Aviran has it. **Add the other three.** |
| **Claude Code** | Every founder's session — this is how anyone talks to the agents | 4 personal accounts, no shared login (Aviran's standing decision) | Each founder's own plan. Agent loops are usage-heavy; a plan that sustains long multi-agent runs matters more than the sticker price. Not centrally billed. | Aviran has it. Others self-serve. |
| **Linear** | Task state + the claim lock the whole pipeline depends on | 4 | Reported June 2026: **Basic ~$10/user/mo, Business ~$16/user/mo, billed yearly** — from third-party pricing trackers, not read off Linear's own page. Verify before committing. At 4 seats that's roughly **$480–$770/yr**. | Aviran has it. **Add three seats.** |
| **Supabase** | The entire backend — Postgres, Auth, Realtime | 4 org/project members (Admin if they'll run migrations) | Free tier today. Paid tier becomes a question at real user volume, not before. | Project exists. **Add the other three.** |
| **hilos** | The founders' channel — run summaries and gate pings | 4 | **$0.** Free plan has no seat limits and covers team chat plus self-run agents; hosted agents (which we deliberately don't use) are what burn credits. 200 one-time starter credits sit unused. | Workspace exists. **Everyone joins + generates their own token.** |
| **Figma** | `designer` works in one shared file; the design-review gate is people looking at a mockup | Serge: edit. Other three: at least view. | Not researched — check current plan pricing before assuming the free tier covers four people on one file. | Shared file exists (`figma.com/design/45siCO8UGQivJEBhAqAH08/locali`). **Seats unconfirmed.** |
| **Apple Developer Program** | Sign in with Apple, TestFlight, App Store — all of Phase 2 | Organization account, so multiple founders can hold App Store Connect roles | **$99/yr** + a D-U-N-S number lookup for the org | **Doesn't exist. Blocks Phase 2.** Aviran-gated. |
| **Mobbin** | `designer`'s design-research step (MCP already wired) | 1 would do | Requires a paid plan; price not researched | Wired but dormant. Optional — the designer proceeds without it and notes the gap. |

## Open decisions (Aviran's)

1. **Apple Developer, Organization not Individual.** An Individual account is tied to one Apple ID and can't give four people App Store Connect roles — you'd be funnelling every build, cert, and TestFlight invite through one person forever. Needs the D-U-N-S lookup started early; it's the slow part, not the $99.
2. **Linear tier and whether four seats are worth it now.** The claim lock is what stops two founders' loops colliding, so this isn't optional infrastructure — but Basic vs Business is a real choice.
3. **Figma seats.** Serge can't do his half of the design-review gate without edit access, and the other three can't do their half without at least view.

## Not a cost

No web server, no container host, no CI runner. The app is native iOS against Supabase's managed services, and GitHub Actions builds it on free macOS runners. Resist provisioning anything else.

## Offboarding / rotation checklist

Nothing here is urgent today. It becomes urgent the day someone leaves or a laptop is lost, which is exactly when nobody wants to be reconstructing the list.

- [ ] Revoke the hilos token (hilos → same panel it was generated in) — tokens post as that person
- [ ] Remove GitHub collaborator access
- [ ] Remove the Linear seat (reassign any `owner:` labels first — orphaned claims block the pipeline)
- [ ] Remove Supabase project membership
- [ ] Remove Figma access
- [ ] Remove App Store Connect role, once that account exists
- [ ] Rotate the Supabase anon key if their machine held a `SupabaseConfig.plist` and can't be wiped

Same list, applied to yourself, is the answer to "my laptop was stolen."

## Sources

- hilos pricing read directly from `hilos.sh/pricing`, 2026-07-26.
- Linear pricing from third-party trackers (vendr, costbench), June 2026 — **not** verified against Linear's own pricing page. Treat as an estimate.
- Apple Developer Program $99/yr and the Organization-vs-Individual distinction: long-standing Apple terms, already recorded in `ONBOARDING.md`.
- Figma and Mobbin: **not researched.** Don't quote a number for these until someone checks.
