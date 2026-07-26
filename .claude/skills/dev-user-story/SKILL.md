---
name: dev-user-story
description: >
  Write structured dev user stories (experience tickets) for the SW board from any input —
  a feature description, PRD excerpt, design ticket, or verbal idea. Outputs a complete story
  with user story, experience requirements, definition of done, QA instructions, and assumptions.
  Use this skill whenever the user asks to write a user story, create a dev ticket, break a
  feature into stories, or mentions "user story", "dev story", "acceptance criteria",
  "definition of done", or "QA instructions". Also trigger when the user says things like
  "write a ticket for engineering", "break this into stories", or "spec this out as a story".
  If the user says "design story", this skill does NOT apply — use the design-story skill.
---

<!-- filename-convention-block -->
## Filename Convention

**Save the output as `[feature-name-kebab]_dev-story.md`** inside the project folder (`content/prds/<feature-slug>/` or `content/13-projects/<feature-slug>/`).

- **Never use generic names** like `dev-story.md`, `ticket.md`, `story.md`, `notes.md`. Always prefix with the feature/initiative name.
- **No date prefix.** Use git/mtime for chronology.
- **Approved doc-types** (extend as needed): `prd`, `prd-draft`, `design-ticket`, `dev-story`, `kickoff-agenda`, `project-notes`, `decision`, `experiment`, `launch-checklist`, `release-notes`.

**Examples:** `rest-timer_dev-story.md`, `external-activities-home_dev-story.md`, `consistency-leaderboard_dev-story.md`.

---

# Dev User Story

A dev story describes the **user-facing experience** the PM owns. Engineering decides how to build it — including any backend work, which the developer opens as their own ticket.

## Core principles

1. **Experience-only scope.** PM tickets cover what the member sees, taps, and gets back. Never specify API contracts, data models, persistence, or backend logic. If a UI behavior depends on backend work, name it once as a Backend Dependency line and stop. The developer opens their own backend ticket.
   - ✓ "When the user taps Start Workout, the rest timer appears at the bottom of the screen and counts down from 90s."
   - ✗ "POST /api/timers returns 201 with `{timer_id, started_at}`."
2. **PRD-first.** If a PRD exists, read it before writing. Don't fill gaps with invention — ask the PM.
3. **Never invent behavior.** Every requirement, state, or scenario must be anchored in the PRD, the design ticket, an existing pattern, or an explicit PM confirmation.
4. **Verifiable, atomic, no filler.** Each requirement is one checkable thing a QA engineer can confirm yes/no without reading minds.
5. **No device-test boilerplate.** Never add "tested on iPhone 14/16 Pro" or similar to the DoD. QA Instructions already capture what to verify.
6. **Current state only — edit in place.** The description is the *current spec*, not a *changelog*. When a requirement changes, edit the line in place and delete what it replaces. Never append a `vN change (date)` section, stack dated blockquotes, or layer `(was X)` / `(v12: …)` parentheticals — they force the reader to replay history to find the truth. History → git + at most one pinned comment. **If the ticket hasn't been started yet** (To Do / Backlog, no one tracking against it), skip even the comment — nobody has read it, so just change the requirements; a dated "changed on …" note on an unstarted ticket is pure noise. **Every spec change updates the QA field (`customfield_10567`) in the same pass** — a QA step that contradicts a requirement is a bug, not a footnote.

## Before you write

**Step 1 — Find and read the PRD.** Check `content/prds/<slug>/` and `content/13-projects/<slug>/`. Read it.

**Step 2 — Check for an existing design ticket.** Dev stories often follow a design spec. If one exists (PD board, or `*_design-ticket.md` in the project folder), pull from it.

**Step 3 — Identify gaps.** List what's missing: persona specificity, states (empty/loading/error/first-time vs returning), entry points, edge behavior, analytics events. Do not invent answers.

**Step 4 — Ask the PM.** One targeted question per gap. Don't re-ask what the PRD or design ticket answers.

**Step 5 — Write the ticket only after gaps are resolved.**

## Output format

Use this exact template. Do not add, rename, or reorder sections.

```markdown
# [Story Title]

## User Story
As a [specific persona], I want [concrete user-facing action] so that [clear benefit].

## Requirements
- [ ] [Experience requirement 1]
- [ ] [Experience requirement 2]
- [ ] [Experience requirement 3]

## Definition of Done
- [ ] [Exit condition 1]
- [ ] [Exit condition 2]
- [ ] [Exit condition 3]

## QA Instructions
1. [Step 1 — start from a specific state]
2. [Step 2 — single action]
3. [Step 3 — expected result]

## Backend Dependency
[One line only — names what backend work the developer needs to open as their own ticket. Omit if none.]

## Assumptions
[Only include if there are genuine unknowns. Otherwise omit entirely.]
```

## Section-by-section guidance

### Story Title
Short, descriptive, action-oriented. Should make sense on a sprint board at a glance.

**Good:** "Show rest timer between sets on workout screen"
**Bad:** "Timer feature" or "REST-234: Implement timer functionality for workout module"

### User Story
Strict "As a / I want / so that" format. Persona must be specific — "member mid-workout", "new user on day 1", "returning member checking progress" — not generic "user." The benefit explains *why* this matters.

**Good:** "As a member mid-workout, I want a rest timer to count down between sets so that I know when to start my next set without watching the clock."
**Bad:** "As a user, I want a timer so that I can use it."

### Requirements
Experience requirements only. Each should be:

- **User-facing**: Describes what the member sees, taps, hears, or receives. Not API contracts, data shapes, or business logic — those are engineering's call.
- **Verifiable**: A QA engineer can look at the app and confirm yes/no.
- **Atomic**: One requirement = one checkable thing. Split anything with "and" in it.
- **State-aware**: Name distinct states the experience must address — default, selected, disabled, empty, active, error, loading, first-time vs returning.
- **Anchored**: Traces to the PRD, design ticket, existing pattern, or an explicit PM call.
- **No filler**: Skip "app should not crash", "should be performant", "should be intuitive."

Think about: happy path, error states, edge cases, empty states, loading states, boundary conditions, permissions, platform-specific behavior.

### Definition of Done
Exit criteria that must ALL be true for the story to ship. Cover:

- Experience works as specified (reference key requirements; don't restate them)
- States handled (empty/loading/error/etc.)
- Analytics events firing (name the events, don't spec them)
- No regressions in adjacent screens

**Do not add device-test lines.** QA Instructions handle that.

### QA Instructions
A step-by-step test script a QA engineer can follow literally:

- Start from a specific state ("Open the app, navigate to workout screen, start a chest workout")
- Each step is a single action ("Tap Start Rest")
- Include expected results after key steps ("Timer counts down from 90s")
- Happy path first, then error/edge cases

### Backend Dependency
One line. Example: "Requires backend endpoint to return per-exercise rest duration — dev to open SW ticket." Stop there. Do not specify the contract.

If there's no backend work, omit the section entirely.

### Assumptions
Only when there are genuine unknowns that could change requirements. Skip if everything is well-defined.

## Jira defaults

When pushing a dev story to Jira (via `/create-tickets`):

- **Project**: SW
- **Issue type**: Story
- **Team**: `ec87fbf0` (Reflect team)
- **Parent**: set via `parent` field (not `customfield_10014`)
- **QA Instructions**: must be written into `customfield_10567` in ADF format
- **Assignee**: leave unassigned unless the PM explicitly names one
- **Document links → Google Drive**: when the ticket references the PRD or any doc, link its Google Drive copy (upload it to the feature's Drive folder first if it isn't there yet) — not a `prds/…` repo path. Engineers can't open a repo path; a Drive link opens in one click. Full procedure (Shared Drive id, raw-markdown upload) is in `/create-tickets` → "Link documents via Google Drive".

## What NOT to do

- **Don't write backend tickets.** UI-facing only. The developer opens backend tickets themselves.
- **Don't invent behavior.** Anchor every requirement in the PRD, design ticket, existing pattern, or an explicit PM call.
- **Don't add implementation notes, technical architecture, or "suggested approach" sections.** That's engineering's domain.
- **Don't duplicate** between Requirements and DoD. The DoD says "experience works as specified", not a verbatim repeat.
- **Don't add device-test boilerplate** ("tested on iPhone 14/16 Pro"). Banned.
- **Don't include design specs** (colors, spacing, font sizes) unless the PRD constrains them. Reference the Figma instead.
- **Don't write vague requirements** like "should handle errors gracefully." Specify: "If the workout fails to start, show an error banner with a Retry button."
- **Don't auto-assign.** Leave assignee blank unless the PM names one.
- **Don't write a novel.** A good dev story is tight — usually 15–40 lines total.

## After the story is written

The story is half the job. The next step is to push it to Jira using `/create-tickets`, which handles the SW board fields (team, parent, QA in ADF).
