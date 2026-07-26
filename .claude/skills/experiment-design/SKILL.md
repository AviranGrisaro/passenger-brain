---
name: experiment-design
description: Design A/B tests with hypotheses, metrics, sample size calculations, and analysis plans.
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


# Experiment Design

## Quick Start

```
/experiment-design
```

Then provide:
1. **What you want to test** (e.g., "new onboarding flow", "shorter workout recommendations")
2. **Current baseline** (if known — e.g., "current activation rate is 45%")
3. **Minimum detectable effect** (optional — e.g., "we need at least a 5% lift to justify the effort")

I'll design a rigorous experiment with hypothesis, metrics, sample size, duration, and analysis plan.

**Output:** Saved to `content/10-outputs/experiments/[name]-[date].md`
**Time:** ~10 min

**When to use:** Before running any A/B test, feature flag experiment, or staged rollout.

## Experiment Design Framework

### Step 1: Hypothesis Formation
- **Null hypothesis (H0)**: [No difference between control and treatment]
- **Alternative hypothesis (H1)**: [Treatment produces measurable improvement]
- **Rationale**: Why we believe the treatment will work (cite research, data, intuition)

### Step 2: Metric Selection (STEDII Framework)
For each metric:
- **S**pecific: Precisely defined, no ambiguity
- **T**rustworthy: Accurately measured, no gaming
- **E**xplainable: Team understands what moves it
- **D**irectional: Clear which direction is good
- **I**mpactful: Connected to business outcomes
- **I**nspectable: Can drill into components

Define:
- **Primary metric**: The one metric that determines success/failure
- **Secondary metrics**: Supporting metrics that add context
- **Guardrail metrics**: Metrics that must NOT degrade (e.g., crash rate, revenue)

### Step 3: Sample Size & Duration
Calculate based on:
- Baseline conversion rate
- Minimum detectable effect (MDE)
- Statistical significance level (default: 95%)
- Statistical power (default: 80%)
- Expected traffic/users per day
- Estimated experiment duration

### Step 4: Segmentation & Targeting
- Who is eligible for the experiment?
- Any exclusion criteria?
- Should we segment by user type, device, geography?
- Is there a ramp-up plan? (1% → 10% → 50% → 100%)

### Step 5: Analysis Plan
- When will we check results? (No peeking!)
- What statistical test will we use?
- How will we handle multiple comparisons?
- What's the decision framework? (Ship / Iterate / Kill)

## Output Format

```markdown
# Experiment: [Name]
_Designed [date] | Status: Draft_

## Hypothesis
**If** we [change], **then** [metric] will [improve/increase/decrease] by [amount],
**because** [rationale].

## Metrics
| Type | Metric | Current Baseline | Target |
|------|--------|-----------------|--------|
| Primary | ... | ... | ... |
| Secondary | ... | ... | ... |
| Guardrail | ... | ... | Must not degrade |

## Design
- **Type**: A/B test / Multi-variant / Staged rollout
- **Variants**: Control (current) vs. Treatment (new)
- **Allocation**: 50/50
- **Targeting**: [Who is eligible]
- **Exclusions**: [Who is excluded]

## Sample Size
- **MDE**: [X]%
- **Significance**: 95%
- **Power**: 80%
- **Required sample**: [N] per variant
- **Estimated duration**: [X] days at current traffic

## Ramp Plan
1. Day 1-3: 5% (validate no crashes)
2. Day 4-7: 25% (early signal)
3. Day 8+: 50% (full experiment)

## Analysis Plan
- **Check date**: [Date — no peeking before this]
- **Statistical test**: [t-test / chi-squared / etc.]
- **Decision framework**:
  - Ship if: Primary metric improves ≥ MDE AND guardrails hold
  - Iterate if: Directionally positive but below MDE
  - Kill if: Negative or guardrail violations

## Risks
- [Risk and mitigation]
```
