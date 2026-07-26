---
name: investigate-metric
description: Systematic root-cause investigation when a product metric drops, spikes, or drifts. Use when WAU, W8 retention, workout volume, conversion, or any KPI moves unexpectedly. Enforces the Iron Law — no recommendations without traced cause — and the 3-strike rule against AI rabbit-holing. Triggers — "why did WAU drop", "investigate the retention dip", "what happened to workouts", "find the cause", "/investigate-metric".
disable-model-invocation: false
user-invocable: true
---

## Iron Law

**NO RECOMMENDATIONS WITHOUT A TRACED CAUSE.**

PMs jump to action: "let's run a survey", "let's A/B test a fix", "let's ship a comms". Each unverified action consumes team time and obscures the real signal. Find the cause first, then act.

The cost of one weekend of confused PMs running unsupported experiments is greater than the cost of a 90-minute investigation. Do the investigation.

---

## When to Use

Trigger this skill when ANY of these happen:
- A primary KPI (WAU, W8 retention, workouts/user, conversion) moves >1 std-dev outside its 28-day band
- A guardrail metric (churn rate, support ticket volume, crash rate) deteriorates without an obvious release cause
- A cohort metric diverges (e.g., new users dropping but returning users stable)
- The PM, exec, or analytics dashboard surfaces an anomaly with no immediate explanation

Do NOT use this for:
- Confirmed expected drops (e.g., post-launch reversion to baseline after a campaign)
- Routine metric reporting (use `/quick-analysis` or `/analytics`)
- Causal experiment readouts (use `/experiment-design` + `/feature-metrics`)

---

## Prior Learnings (load first — before framing)

This is the highest-value skill for compounding because every metric investigation feeds the next one. Always load prior investigations on the same metric or related cohort:

```bash
bash /Users/avirang/Documents/amp/scripts/learnings-search.sh --skill investigate-metric --limit 10
```

If the user named the metric, also search by it:
```bash
bash /Users/avirang/Documents/amp/scripts/learnings-search.sh --query "<metric-name>" --limit 5
```

If a returned learning matches the current anomaly shape (same metric drop, same cohort, same time window pattern), prefix your hypothesis section with **"Prior learning applied: [key] (confidence N/10)"**. A matching prior cause is often the right hypothesis to test first.

---

## Phase 1: Frame the Anomaly

Before forming any hypothesis, get specific about WHAT moved and WHEN.

### 1a. Collect symptoms

Write the anomaly in this exact shape — fill every field. If you can't, stop and ask the PM.

```
ANOMALY FRAME
  Metric:         [exact metric name — WAU, W8 retention, workouts/active user, etc.]
  Direction:      [↑ / ↓ / range-bound but anomalous]
  Magnitude:      [absolute and % change vs prior period]
  Window:         [the window when it changed — be specific to the week or day]
  Baseline:       [pre-change value over a comparable prior window]
  Source:         [chart ID, dashboard, semantic-layer query, Amplitude link]
  First noticed:  [date + by whom]
```

Reject vague framing. "Retention is down" is not a frame. "W8 retention for the 2026-04 cohort dropped to 34% (from a 41% trailing 8-cohort baseline), spotted in Amplitude chart `9yaksqnt` on 2026-05-20" is a frame.

### 1b. Check for known explanations FIRST (cheap filters)

In order — skip if obviously not relevant:

1. **Recent ship:** Run `git log --since='<window>' --oneline` on the Passenger repos (via SDD path config). Did anything ship into the affected surface during the window?
2. **Marketing event:** Check `content/09-meetings/` and Slack for campaign launches, comms, or pricing changes that align with the window.
3. **Seasonality:** Is the window a holiday, school break, end-of-quarter, fiscal year-end? Pull the same window from the prior 1-2 years if available.
4. **Data pipeline:** Was there a `refresh-metrics` failure, dbt run break, Fivetran sync delay, or Amplitude event-spec change in the window? Check `content/07-analytics/metrics.json` last-update timestamp and Fivetran logs.
5. **Composition shift:** Did the user base composition change (new market launch, B2B onboarding, a big influx of trial users)?

If a known explanation FULLY accounts for the magnitude, STOP — write the anomaly off as expected, document why, exit. If it partially explains, note the residual and continue.

### 1c. Search prior investigations

Have we seen this shape before? Grep `content/10-outputs/` and `content/archive/` for prior investigation reports on the same metric:

```bash
grep -ri "METRIC INVESTIGATION REPORT" /Users/avirang/Documents/amp/content/ 2>/dev/null | head -20
```

Recurring drops in the same metric, at the same cadence, or with the same cohort signature are an **architectural signal**, not a coincidence. If a prior investigation matched the shape, lead with that hypothesis.

---

## Phase 2: Pattern Match

Match the anomaly against known shapes before generating new hypotheses.

| Pattern | Signature | Where to look |
|---|---|---|
| **Funnel break** | Sharp drop at one step of a flow; downstream metrics follow | Amplitude funnel chart; recent UX/copy/code change at that step |
| **Cohort dilution** | New cohort underperforms; old cohorts stable | Acquisition channel mix; marketing campaign quality |
| **Cohort decay** | A specific past cohort regressed; new cohorts unaffected | App version distribution; firmware/app version (Passenger) |
| **Tracking break** | Drop is exactly at integer % (e.g., "exactly 30% of events disappeared") | Event-spec change; Amplitude rate limit; Fivetran sync gap |
| **Composition shift** | Headline metric moves but per-cohort metrics stable | New market launched, B2B push, trial conversion change |
| **Substitution** | Metric A drops but Metric B rises in proportion | Feature replacing another (e.g., Reflect vs activity feed) |
| **Seasonal/external** | Drop aligns with calendar event or platform-wide shift | Holidays, app-store policy change, iOS update, competitor launch |
| **Engagement decay** | Top-of-funnel stable but downstream activity drops | Content quality, recommendation algo, push notification gap |
| **B2B segment** | Aggregate moves but consumer-only or B2B-only is stable | Specific account churn or expansion |

For each pattern that plausibly fits, name ONE specific testable claim. Move into Phase 3 with the top 1-3.

---

## Phase 3: Hypothesis Testing (3-strike rule active)

Test hypotheses one at a time. Use `/analytics` (dbt semantic layer) or `/quick-analysis` (Amplitude) to query.

### For each hypothesis:

1. **State it precisely.** Not "users are churning more" — "users acquired via paid social in 2026-04 have 50% worse W4 retention than 2026-03 paid social cohort."
2. **State the evidence that would CONFIRM it.** Be specific about the number.
3. **State the evidence that would REJECT it.** Equally specific.
4. **Query.** Run via `/analytics` if the question fits the semantic layer (cross-domain joins, fiscal calendar, entity-graph), otherwise via `/quick-analysis` (Amplitude charts).
5. **Compare to (2) and (3).** Confirm, reject, or inconclusive.

### The 3-strike rule

**If 3 hypotheses fail, STOP.** Use AskUserQuestion:

```
3 hypotheses tested, none match the anomaly shape.
This may be a structural / systemic issue rather than a single cause.

A) Continue investigating — I have a new hypothesis: [describe specifically]
B) Escalate for human review — pull in Mike (tech lead) / Shahar (CPO) / data team
C) Add instrumentation and wait — the cause may only be visible with more data
D) Reframe — the anomaly itself may be defined wrong; re-run Phase 1
```

The 3-strike rule prevents AI rabbit-holing. After 3 misses, the problem is usually NOT "we need to think harder" — it's "the framing or data is wrong."

### Red flags — slow down if you see these

- **"Probably it was the marketing campaign"** without checking campaign attribution data
- **Proposing a fix before naming the cause** — that's a guess
- **Each hypothesis revealing a new metric to investigate** — you're flailing, reframe
- **"Let's just run a survey"** — surveys are slow and biased; exhaust quantitative paths first
- **A hypothesis that requires 4+ co-occurring conditions** to be true — Occam's razor

### Sanitize before WebSearching

If you hit a public-pattern question ("did iOS 19 affect health-app session length"), search for it — but **strip internal data first**: no user IDs, no specific revenue numbers, no PII, no internal codenames. Search the generic pattern, not your data.

---

## Phase 4: Action

Once you have a traced cause:

1. **State the cause precisely.** With evidence — a chart link, a query result, a code change reference.
2. **Classify the cause:**
   - **Known acceptable** (campaign ended, seasonality, intentional ship) → document, no action
   - **Bug** (tracking, code, pipeline) → file ticket; do NOT propose UX experiments
   - **Real product signal** (cohort actually behaves differently) → THIS is where PRDs and experiments come from
   - **External** (competitor, market, platform) → strategic input, not tactical fix
3. **Recommend ONE next action.** Not a list of options — your best call, with the reasoning. The PM can override.
4. **State the kill criteria for the recommendation.** If the action doesn't move the metric by X in Y weeks, what's the next step?

### Anti-pattern — DO NOT do this

- Suggest 5 experiments without picking one
- Recommend "more user research" as the action (research is investigation, not action)
- Propose a redesign that doesn't address the named cause
- Skip step 4 — every recommendation needs a kill criterion

---

## Phase 5: Report

Output a structured report. Save it to `content/10-outputs/metric-investigations/<YYYY-MM-DD>-<metric-slug>.md`.

```
METRIC INVESTIGATION REPORT
═══════════════════════════════════════════════════════════════

Anomaly:        [metric, direction, magnitude, window]
First noticed:  [date + source]
Investigator:   Aviran (with /investigate-metric)
Status:         CAUSE FOUND / INCONCLUSIVE / ESCALATED

───────────────────────────────────────────────────────────────
ROOT CAUSE

  Traced cause:   [specific, with chart/query evidence inline]
  Classification: KNOWN-ACCEPTABLE / BUG / REAL-SIGNAL / EXTERNAL
  Confidence:     [1-10] — see calibration below

───────────────────────────────────────────────────────────────
EVIDENCE TRAIL

  1. [Symptom check]:    [what we saw + source]
  2. [Pattern match]:    [which pattern + why]
  3. [Hypothesis 1]:     [result]
  4. [Hypothesis 2]:     [result]
  5. [Hypothesis 3]:     [result, if applicable]
  6. [Confirming query]: [the query that landed the cause]

───────────────────────────────────────────────────────────────
RECOMMENDATION

  Next action:      [ONE thing, with reasoning]
  Owner:            [name]
  Timeline:         [when to revisit]
  Kill criteria:    [if action doesn't move metric by X in Y, do Z]

───────────────────────────────────────────────────────────────
RELATED

  Prior investigations: [links to similar past reports]
  Affected surfaces:    [components / flows / cohorts]
  TODOS / Jira tickets: [if any filed from this]

═══════════════════════════════════════════════════════════════
```

### Confidence calibration

Be honest about confidence. The number gets quoted to Shahar / Mike / the data team — overclaiming is worse than admitting uncertainty.

- **9-10**: Cause directly proven by a query result that matches both confirm-evidence AND rejects all 3 alternates.
- **7-8**: Strong evidence, one or two unverifiable assumptions remaining.
- **5-6**: Plausible cause, but could be explained by 2+ other hypotheses. State this honestly.
- **3-4**: Hunch. Don't recommend an action — recommend more investigation.
- **1-2**: Don't ship this report. Continue investigating or escalate.

---

## Capture Learnings (run at skill end — after report is saved)

**This is the highest-leverage capture in the entire stack.** Every metric investigation should produce at least one learning. The compounding here is the difference between PM intuition that improves and PM intuition that stalls.

```bash
bash /Users/avirang/Documents/amp/scripts/learnings-log.sh \
  --skill investigate-metric \
  --type <pattern|pitfall|strategic|tool> \
  --key <metric-or-cause-slug> \
  --insight "The cause pattern, sanitization issue, or root mechanic this investigation revealed." \
  --confidence <1-10 — see calibration> \
  --source <observed|cross-model> \
  --project-or-feature <passenger-feature-slug if cause is feature-tied> \
  --files content/10-outputs/metric-investigations/<this-report>.md
```

**Multiple learnings often emerge from one investigation:**
1. The cause itself ("WAU drop on 2026-04-22 was paid-social cohort dilution, not retention regression")
2. The diagnostic pattern that surfaced it ("cohort dilution always shows as: aggregate moves, per-cohort stable")
3. The data tool quirk ("Fivetran sync delays >12h on Tuesdays — check timestamp before trusting the chart")
4. The disproven hypothesis (`pitfall` type — "stop assuming feature X moves W4")

**Confidence calibration here matters most.** If the cause is directly proven by a query result: 9-10. If you traced it via reasoning but couldn't isolate cleanly: 6-7. If it's a hypothesis the user accepted but you didn't formally verify: 4-5 and revisit.

**Calibration loop:** when the same metric anomaly recurs, your prior learning's confidence either gets upgraded (you found the right cause-pattern) or downgraded (the pattern doesn't generalize). Log the recalibration explicitly.

---

## Important Rules

1. **Iron Law:** No recommendation without a traced cause. Reject "let's just try X".
2. **Frame before hypothesize:** Phase 1 is non-skippable. A bad frame leads to confidently wrong investigations.
3. **3-strike rule:** STOP after 3 failed hypotheses. The problem is usually framing, not effort.
4. **Cheap filters first:** Ship + marketing + seasonality + data pipeline checks BEFORE generating new hypotheses. The cause is usually mundane.
5. **One recommendation, not a menu.** If you can't pick one, you haven't traced the cause confidently enough.
6. **Kill criteria are mandatory.** Every recommendation needs "if X by Y, then Z".
7. **Save the report.** Investigations compound — `grep` your prior reports first on the next anomaly.
8. **Sanitize before public search.** Strip internal data before any WebSearch on the pattern.

---

## Outputs

- **Primary**: `content/10-outputs/metric-investigations/<YYYY-MM-DD>-<metric-slug>.md`
- **Index**: append a one-line entry to `content/10-outputs/metric-investigations/INDEX.md` (create if missing) — `2026-05-24 — W8 retention drop 2026-04 cohort — CAUSE: paid-social acquisition mix shift — confidence 8`

## Cross-skill Integration

- **Feeds into:** `/prd-draft` (real signals become PRDs), `/decision-doc` (architectural causes become decisions), `/status-update` (anomalies + causes get reported)
- **Pulls from:** `/analytics` (dbt semantic layer queries), `/quick-analysis` (Amplitude one-off queries), `/competitor-analysis` (external-cause hypotheses), `content/07-analytics/metrics.json` (live state)

---

Source: gstack `/investigate` skill (`investigate/SKILL.md`) — Iron Law, 3-strike rule, structured report shape — adapted from code-bug investigation to product-metric investigation for Aviran's Passenger PM workflow.
