---
name: release-notes
description: Generate user-facing release notes from Jira tickets, PRDs, and recent shipped work.
disable-model-invocation: false
user-invocable: true
---

<!-- filename-convention-block -->
## Filename Convention

**Save the output as `[feature-name-kebab]_[doc-type].md`** inside the project folder (`Projects/<feature-slug>/` or `content/<numbered>/<feature-slug>/`).

- **Never use generic names** like `prd.md`, `design-ticket.md`, `README.md`, `direction.md`, `dev-story.md`, `notes.md`. Always prefix with the feature/initiative name so the filename is self-describing out of context.
- **No date prefix.** Use git/mtime for chronology.
- **Approved doc-types** (extend as needed): `prd`, `prd-draft`, `prd-team-kickoff`, `prd-planning-review`, `prd-xfn-kickoff`, `prd-solution-review`, `prd-launch-readiness`, `design-ticket`, `dev-story`, `kickoff-agenda`, `project-notes`, `decision`, `experiment`, `launch-checklist`, `meeting-notes`, `release-notes`, `competitor-analysis`, `retention-analysis`, `status-update`, `roadmap`, `uxr-synthesis`, `impact-sizing`, `strategy-direction`, `risks-and-decisions`, `eng-validation`, `readme`.

**Examples:** `visible-consistency_prd-draft.md`, `device-lock_kickoff-agenda.md`, `consistency-leaderboard_design-brief.md`, `external-activities-home_design-ticket.md`.

---


# Release Notes

## Quick Start

```
/release-notes
```

Then provide:
1. **Version or sprint** (e.g., "v2.5.0", "Sprint 15")
2. **Audience** (optional — defaults to "users", can be "internal" or "app store")

I'll pull shipped tickets from Jira, cross-reference with PRDs, and generate polished release notes.

**Output:** Saved to `content/10-outputs/release-notes/[version]-[date].md`
**Time:** ~5-10 min

**When to use:** Before an app release, for sprint demos, or for stakeholder updates on shipped work.

## Process

### Step 1: Gather Shipped Work
- Query Jira MCP for tickets in "Done" status from the target sprint/version
- Read PRDs for shipped features to get user-facing descriptions
- Check `content/06-execution/tasks/TASKS.md` for completed items

### Step 2: Categorize Changes
Group by type:
- **New Features**: Major new capabilities
- **Improvements**: Enhancements to existing features
- **Bug Fixes**: Issues resolved
- **Performance**: Speed, stability, reliability improvements
- **Behind the Scenes**: Infrastructure changes users won't see directly

### Step 3: Write User-Facing Copy
For each item:
- Translate technical ticket into user benefit
- Use active voice and plain language
- Focus on what the user can now DO, not what was changed technically
- Include relevant context (if fixing a reported issue, acknowledge it)

### Step 4: Format for Audience

## Output Formats

### User-Facing (App Store / In-App)
```markdown
# What's New in [Version]

## [Feature Name]
[1-2 sentence description of what's new and why it matters to users]

## Improvements
- [Improvement in user terms]
- [Improvement in user terms]

## Bug Fixes
- Fixed an issue where [user-visible problem]
- Resolved [user-visible problem]
```

### Internal (Team / Stakeholders)
```markdown
# Release Notes: [Version/Sprint]
_Released [date] | [X] tickets shipped_

## Highlights
1. **[Feature]** ([ticket keys]) — [description + early metrics if available]

## All Changes
| Ticket | Type | Summary | Impact |
|--------|------|---------|--------|

## Known Issues
- [Issue] — [Workaround] — [ETA for fix]

## Metrics to Watch
- [Metric affected by this release]
```

### App Store Description
```
Version [X.Y.Z]

- [Feature]: [One-line benefit]
- [Improvement]: [One-line benefit]
- Bug fixes and performance improvements
```

## Sell Test (Quality Gate — MANDATORY before saving)

Every entry must pass the sell test for its target audience BEFORE you save the file. Entries that fall below the threshold get flagged for rewrite, not auto-shipped.

### Audience-specific tests

**App Store entries** (2-point scale — both points required):

| Point | Question | What it means |
|---|---|---|
| 1 | **Is "what" concrete?** | Names the feature with a noun a user would recognize. NOT "Improvements to performance" — DO "Faster home screen load (now 1.4s vs 2.8s)" |
| 2 | **Does "why care" land in <5 words?** | A user scanning the app store sees the benefit instantly. NOT "We refactored the data pipeline" — DO "Workouts now sync 3× faster" |

Entry score: 0-2. **Threshold: 2/2.** Score <2 → flag for rewrite. Don't ship vague app-store copy — it's the first thing the user reads.

---

**Internal entries** (2-point scale — both points required):

| Point | Question | What it means |
|---|---|---|
| 1 | **What shipped?** | Specific tickets, file paths, or surfaces. NOT "Improved auth flow" — DO "Removed `/api/auth/legacy` endpoint (SW-1234, SW-1235); login now goes through new OAuth path" |
| 2 | **Why now / why this release?** | The reason this work was prioritized this cycle. NOT "Cleanup" — DO "Unblocks the upcoming social-profile launch which depends on the new OAuth scopes" |

Entry score: 0-2. **Threshold: 2/2.** Score <2 → flag for rewrite. Internal audiences want to know what's actually different in the codebase AND why it mattered.

---

**User-facing entries** (3-point scale — all three required):

| Point | Question | What it means |
|---|---|---|
| 1 | **What changed?** | Names the feature/fix as a user would describe it |
| 2 | **Why should the user care?** | The pain removed or value added, in the user's vocabulary |
| 3 | **How do they use it?** | The command, the gesture, the menu path, or a link to docs. NOT "Available in settings" — DO "Tap Settings → Workouts → Auto-pause to enable" |

Entry score: 0-3. **Threshold: 2/3 minimum, 3/3 preferred.** Entries scoring <2 are rejected outright. Entries at 2/3 ship with a flag for the next iteration.

---

### How to run the gate

For every entry in the draft release notes, score it against the matching audience test BEFORE saving:

```
SELL TEST RESULTS — [audience]
─────────────────────────────────────────────
✅ "Added auto-pause for workouts" — 3/3
✅ "Faster home screen" — 2/2 (App Store)
⚠️ "Performance improvements" — 0/2 ❌ REWRITE
✅ "OAuth scope refactor" — 2/2 (Internal)
─────────────────────────────────────────────
Total entries: 12
Passing: 10
Below threshold (needs rewrite): 2
```

For every flagged entry, propose a rewrite inline and ask the user to confirm before saving. **Do NOT save release notes with entries below the threshold** — fix them first.

### Common rewrites

| Slop (low score) | Fixed (passing) |
|---|---|
| "Performance improvements and bug fixes" | "Home screen loads 50% faster (1.4s → 0.7s); fixed a crash when starting a workout offline" |
| "Improved auth flow" (internal) | "Removed legacy `/api/auth/v1`; login now goes through OAuth 2.1 (SW-1234) — unblocks social-profile rollout" |
| "Now you can see your progress" | "Your weekly volume now appears on the home screen — tap any workout in the history list to see the rep-by-rep breakdown" |
| "We listened to your feedback" | (Cut entirely — not a feature, not a benefit, padding) |

Source: gstack `/document-release` sell test (`document-release/SKILL.md:987-995`), adapted from single-audience to three audience tiers for Aviran's release-notes workflow (app store / internal / user-facing).

---

## Tone
User-facing: Friendly, benefit-focused, no jargon. Internal: Direct, comprehensive, metric-aware.
