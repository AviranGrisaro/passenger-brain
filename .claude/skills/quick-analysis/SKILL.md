---
name: quick-analysis
description: Ad-hoc data question to Amplitude query to answer. Fast, focused analysis for specific product questions.
disable-model-invocation: false
user-invocable: true
---

# Quick Analysis

## Quick Start

```
/quick-analysis
```

Then ask your question:
- "What's the conversion rate from session to workout this week?"
- "How many users completed onboarding in the last 7 days?"
- "What's the retention curve for users who signed up in February?"
- "Compare workout frequency between iOS 17 and iOS 18 users"

I'll query Amplitude (via MCP), interpret the results, and give you a concise answer with context.

**Output:** Direct answer in conversation (optionally saved to `content/10-outputs/analyses/`)
**Time:** ~2-5 min

**When to use:** When you have a specific data question and don't need a full analysis. Perfect for Slack threads, meeting prep, or quick decision-making.

## Process

### Step 1: Parse the Question
Identify:
- **Metric**: What's being measured (conversion, retention, count, rate)
- **Segment**: Who (all users, new users, specific cohort, device type)
- **Time range**: When (today, this week, last 30 days, specific dates)
- **Comparison**: Against what (previous period, different segment, benchmark)

### Step 2: Query Amplitude
Use available Amplitude MCP tools:
- `query_chart` / `query_charts` for existing saved charts
- `query_dataset` for custom queries
- `get_event_properties` to understand available data

Key chart IDs:
- WAU: `urzosb7i`
- W8 Retention: `9yaksqnt`
- Workouts: `2ephtco3`

### Step 3: Interpret & Contextualize
- What's the number?
- Is it good or bad? (Compare to baseline, trend, benchmark)
- What's driving it? (If obvious from the data)
- What should you do about it? (If actionable)

### Step 4: Respond

## Output Format

```markdown
## [Your Question — Rephrased]

**Answer:** [The number/metric, clearly stated]

**Context:**
- Trend: [Up/Down/Flat] vs. last week/month
- Benchmark: [How this compares to expectations or industry]

**What this means:** [1-2 sentences of interpretation]

**Suggested follow-up:** [Optional — deeper analysis or action to take]
```

## Example

**Q:** "What's our session-to-workout conversion this week?"

**A:**
- **This week**: 34.2% of sessions include a workout
- **Last week**: 32.8% (+1.4pp improvement)
- **30-day avg**: 33.1%
- **Context**: Slight uptick, likely driven by the new workout recommendation algorithm shipped in Sprint 14. Worth monitoring if the trend holds next week.

## Tone
Be concise and direct. Lead with the number. Add context only if it changes the interpretation. If you can't get the exact data, say what you can approximate and what would be needed for precision.
