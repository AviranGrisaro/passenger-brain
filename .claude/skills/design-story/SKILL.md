---
name: design-story
description: >
  Write structured design tickets (specs) for the design team from any input — a feature idea, PRD excerpt,
  verbal description, or Figma reference. Outputs a design-ready ticket with user story, design requirements,
  use cases, and edge cases. Use this skill whenever the user asks to write a design ticket, create a design
  spec, write a design story, or mentions "design ticket", "design story", "design spec", or "spec for design".
  Also trigger when the user says things like "write a ticket for Serg", "spec this for design", "write a design
  task", or asks to push something to the PD board. If the user says "dev story" or "user story" without
  mentioning design, this skill does NOT apply — use the dev-user-story skill instead.
---

<!-- filename-convention-block -->
## Filename Convention

**Save the output as `[feature-name-kebab]_[doc-type].md`** inside the project folder (`Projects/<feature-slug>/` or `content/<numbered>/<feature-slug>/`).

- **Never use generic names** like `prd.md`, `design-ticket.md`, `README.md`, `direction.md`, `dev-story.md`, `notes.md`. Always prefix with the feature/initiative name so the filename is self-describing out of context.
- **No date prefix.** Use git/mtime for chronology.
- **Approved doc-types** (extend as needed): `prd`, `prd-draft`, `prd-team-kickoff`, `prd-planning-review`, `prd-xfn-kickoff`, `prd-solution-review`, `prd-launch-readiness`, `design-ticket`, `dev-story`, `kickoff-agenda`, `project-notes`, `decision`, `experiment`, `launch-checklist`, `meeting-notes`, `release-notes`, `competitor-analysis`, `retention-analysis`, `status-update`, `roadmap`, `uxr-synthesis`, `impact-sizing`, `strategy-direction`, `risks-and-decisions`, `eng-validation`, `readme`.

**Examples:** `visible-consistency_prd-draft.md`, `device-lock_kickoff-agenda.md`, `consistency-leaderboard_design-brief.md`, `external-activities-home_design-ticket.md`.

---


# Design Story

A design ticket frames the **problem** for a designer. It does not draw the solution.

## Core principles

1. **Problem-first, not solution-prescriptive.** Describe the user need or gap, not the UI you imagine. The designer owns the *how*.
   - ✓ "Member needs lightweight feedback that the BLE dial connected before starting the workout."
   - ✗ "Add a BLE tray to the home screen with a green/red dot."
2. **PRD-first.** If a PRD exists, read it before writing. Don't fill gaps with invention — ask the PM.
3. **Never invent behavior.** Every requirement, state, or scenario must be anchored in the PRD, an existing pattern, or an explicit PM confirmation. If it isn't, ask.
4. **Accurate, sharp, short.** No padding, no platitudes, no boilerplate. Every line earns its place.
5. **Story format always**, unless the PM explicitly says otherwise.

## Before you write

**Step 1 — Find and read the PRD.** Check `content/prds/<slug>/` and `content/13-projects/<slug>/`. Read it.

**Step 2 — Identify gaps.** List what's missing for design: persona specificity, states (empty/loading/error/first-time vs returning), entry points, related screens, edge behavior, copy ownership. Do not invent answers.

**Step 3 — Ask the PM.** One targeted question per gap. Don't re-ask what the PRD answers. Don't guess.

**Step 4 — Write the ticket only after gaps are resolved.**

If no PRD exists, ask first: what problem this solves, who the user is, what comes before and after.

## Output format

Use this exact template. Do not add, rename, or reorder sections.

```markdown
# [Ticket Title]

## User Story
As a [specific persona], I want [concrete action/experience] so that [clear benefit].

## Design Requirements
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

## Use Cases
- [Primary use case — the canonical happy-path scenario this design serves]
- [Secondary use case — additional valid scenarios the design must handle]

## Edge Cases
- [Edge case 1 — what happens at boundaries, empty states, failures, conflicts with other features]
- [Edge case 2 — interactions with adjacent systems, race conditions, permission/visibility flips]
```

That's it. No Definition of Done. No QA instructions. Those belong on dev stories, not design specs. If the PM explicitly asks for DOD or QA, add them — otherwise omit.

## Section-by-section guidance

### Ticket Title
Short, specific, and scannable on a board. Name the thing being designed, not the outcome.

**Good:** "Muscle Picker — Tile States and Selection Logic"
**Bad:** "Design the muscle selector" or "PD-1407: Implement muscle picker interaction flow"

### User Story
Use "As a / I want / so that" strictly. The persona should be specific to this product — "member mid-workout", "new user on day 1", "returning member checking progress" — not generic "user." The benefit should explain why this matters to that person.

**Good:** "As a returning member reviewing my progress, I want to tap any muscle group — even one showing 0% — so that I can see the muscle detail view and understand what exercises target it."
**Bad:** "As a user, I want to see muscles so that I can interact with them."

### Design Requirements

Requirements describe the **problem space** — user needs, gaps, constraints, and states the design must address. They are *not* a list of UI components to build.

- **Problem-first**: Name the user need or gap, not the UI fix. The designer chooses the form.
  - ✓ "Member needs lightweight confirmation that BLE connected before starting."
  - ✗ "Add a BLE status tray to the home screen with green/red dot."
- **Anchored**: Every requirement traces to the PRD, an existing pattern, or an explicit PM call. No invention.
- **State-aware**: List the distinct states the design must address (default, selected, disabled, empty, active, error, loading, first-time vs returning) — as scenarios, not as screens to draw.
- **Interaction-specific**: Name what user actions matter and what should happen, without dictating the exact gesture or transition unless the PRD specifies.
- **Boundary-conscious**: Max selections, character limits, truncation, extremes.
- **System-aware**: Name related screens and existing patterns. Say what's net-new vs re-applying existing visual language.
- **Honest about unknowns**: If the PRD doesn't answer something, flag it as an open question — don't invent.

Skip in requirements:
- Implementation details (APIs, data models, state management)
- Pixel specs (colors, spacing, font sizes) unless the PRD constrains them
- Obvious platform conventions
- Vague quality statements ("should feel intuitive")

### Use Cases

Use cases are the canonical scenarios this design serves. They answer: *when does a real user actually encounter this, and what are they trying to do?* Each use case should be a one-line user scenario, written from the user's POV, anchored in a specific persona and trigger.

**Good:** "Returning member opens the Activity tab and types the first three letters of a teammate's name to find their profile and check whether they trained this week."
**Bad:** "User searches for another user."

Aim for 2–5 use cases. Cover the primary happy path plus the most common variants (different personas, different entry points, different goals). Skip exotic scenarios — those belong in edge cases.

Use cases differ from the user story: the story names *the* core motivation; use cases enumerate the *scenarios* in which that motivation shows up.

### Edge Cases

Edge cases are the boundary conditions, failure modes, and adjacent-system interactions the design must survive. They answer: *what happens when reality breaks the happy path?* Each edge case should describe a specific situation and what the design needs to do about it.

Cover at minimum:
- **Empty / zero state** — what shows when there's no content yet?
- **Permission / visibility flips** — what happens if the underlying user/object becomes private, blocked, deleted, or hidden mid-flow?
- **Failure modes** — network failure, timeout, server error, no permissions granted.
- **Race conditions** — user A acts while user B is mid-render; state changes during interaction.
- **Cross-feature interactions** — how this interacts with adjacent features (Block, Hide, Not Visible, age gate, etc.).
- **Extreme content** — very long names, very short streaks, zero followers, max selections.
- **Re-entry / persistence** — what state does the user return to after backgrounding the app, switching tabs, or completing the flow?

The designer doesn't have to design every edge case as a pixel-perfect screen, but every edge case must have a defined behavior. If the answer is "follow [existing pattern]," say which pattern.

### When to present design options

If the problem has multiple valid approaches and you want the designer's input, structure requirements with explicit options:

```markdown
- [ ] **Option A — [Name]**: [Description of approach, tradeoffs]
- [ ] **Option B — [Name]**: [Description of approach, tradeoffs]
- [ ] **Recommendation**: Option [X] because [rationale]. Designer to validate or propose alternative.
```

This is especially useful for entry points, layout variations, or information hierarchy decisions.

## Jira defaults

When pushing a design ticket to Jira:
- **Project**: PD (Product & Design board)
- **Issue type**: Spec
- **Assignee**: **leave unassigned.** Do not auto-assign. Only set an assignee if the PM explicitly names one.

## What NOT to do

- **Don't invent behavior, states, or screens.** Anchor everything in the PRD, an existing pattern, or an explicit PM confirmation. If it isn't anchored, ask.
- **Don't write the solution.** Write the problem. "Add a tray with a green dot" is solution. "User needs lightweight feedback that BLE connected" is problem.
- **Don't auto-assign.** Leave assignee blank.
- **Don't skip the PRD.** If one exists, read it first. If gaps remain, ask the PM.
- **Don't add Definition of Done or QA Instructions** — those are dev-story sections. Only add if the PM asks.
- **Don't pad** with the obviously-true ("should not crash on tap").
- **Don't dictate pixel specs** unless the PRD constrains them.
- **Don't restate the user story** in requirements or use cases.
- **Don't list edge cases as platitudes.** Name the failure and the behavior.
