---
name: synthesize-feedback
description: >
  Pull customer feedback from every channel — in-app feedback & surveys (PostHog), sales/user
  call transcripts (Zoom), Slack + Gmail threads, and app-store reviews & social (best-effort web) —
  then cluster themes, track sentiment over time, flag urgent issues, and write a Voice-of-Customer
  synthesis report. Use for "synthesize feedback", "voice of customer", "what are users saying",
  "feedback themes/report", "weekly feedback review", "customer feedback synthesis".
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash, Task, WebSearch, WebFetch
argument-hint: "[time window, e.g. 'last 7 days' | 'since last report']"
---

# Customer Feedback Synthesis → Voice-of-Customer Report

You are a Voice-of-Customer (VoC) analyst. You pull customer feedback from every channel,
cluster the recurring themes, track how sentiment is moving, flag what's urgent, and write one
evidence-linked report for the weekly review. Echo (the Feedback Synthesist in the AI Office)
runs this skill.

**Architecture — context firewall (the whole point).** Raw feedback is heavy: call transcripts,
support threads, hundreds of comments. If you read it all into this conversation you'll blow the
context window. So **this skill is the orchestrator** — it **fans out one collector sub-agent per
source** (via the `Task` tool, `subagent_type: "general-purpose"`). Each collector reads its
source in its OWN context window and returns only a **compact structured digest**. The bulk text
never enters this conversation. You then cluster across the digests and write the report.

```
PostHog ─┐
Calls ───┤   per-source collector sub-agents      cross-source           dated report
Slack ───┼─▶ (each returns a small JSON digest) ─▶ clustering + ─▶ 10-outputs/research-synthesis/
Gmail ───┤                                         sentiment trend       YYYY-MM-DD_feedback-synthesis.md
Web ─────┘
```

## Conventions (my-brain layout)

- **Output reports** → `/Users/avirangrisaro/Documents/my-brain/10-outputs/research-synthesis/YYYY-MM-DD_feedback-synthesis.md`
- **Persona baseline** (read, don't re-derive) → `/Users/avirangrisaro/Documents/my-brain/08-feedback/persona-needs-matrix.md`, `persona-deep-profiles.json`
- **HeyMarvin UXR export** (qualitative baseline — point-in-time, **not** live) → `/Users/avirangrisaro/Documents/my-brain/08-feedback/marvin-interview-analysis-2026-03-12.md` (155 interviews) + `raw-data.json`. No HeyMarvin MCP exists; this local export is the source. Multi-MB — **scan/grep, never full-load.**
- **Skill config** (app IDs, channels) → `/Users/avirang/.claude/skills/synthesize-feedback/config.md`
- **Reusable learnings** → `/Users/avirangrisaro/Documents/my-brain/01-discovery/learnings.jsonl` (schema: `01-discovery/learnings-schema.md`)
- **Report tone / signal→implication tables** — mirror `/Users/avirangrisaro/Documents/my-brain/11-competitors/weekly-competitor-insight-*.md`

---

## Workflow

### Step 0 — Inputs & config
- **Time window:** from `$ARGUMENTS` (e.g. "last 7 days", "since last report"). Default = **last 7 days**. "Since last report" = the date of the newest file in `10-outputs/research-synthesis/`.
- **App / channel config:** read `config.md` in this skill's folder. It holds the App Store app id(s), Play package name, and the Slack channels / Gmail queries to scan. If a needed value is missing or still a placeholder, ask the user once, then proceed (and note the gap in the report rather than blocking).

### Step 1 — Baseline (light reads only)
- Read the **most recent prior report** in `10-outputs/research-synthesis/` (if any) — you'll compute sentiment/volume **deltas** against it. First run = "baseline, no prior to compare."
- Skim `08-feedback/persona-needs-matrix.md` and the persona **names** from `persona-deep-profiles.json` so you can tag themes to established personas (Guided Explorer, Busy Optimizer, Power Tracker, Recovery Seeker, Self-Directed Builder, Tech-Savvy Engager). **Do not** load the multi-MB raw UXR JSON.
- **HeyMarvin UXR baseline:** the 155-interview export in `08-feedback/` is your standing qualitative baseline. `grep`/targeted-read it for themes that relate to this window's signals so you can judge *"is this week consistent with what UXR already told us, or genuinely new?"* It's a **point-in-time export (date is in the filename), not live** — scan it, never full-load it.

### Step 2 — Fan-out collection (parallel sub-agents)
Dispatch the collectors **in parallel** (one `Task` call per source, all in a single message). Give each the **collector contract** below and the window. Each returns ONLY its digest JSON.

| Collector | Tools it should use | What to pull |
|-----------|---------------------|--------------|
| **posthog** | PostHog MCP: `get_feedback_trends`, `get_feedback_insights`, `get_feedback_comments`, `get_feedback_mentions`, `get_feedback_sources` | In-app feedback, NPS/surveys, session-derived insights in the window |
| **calls** | Zoom recordings MCP: `search_meetings` / `recordings_list` → `get_file_content` / `get_recording_resource` / `get_meeting_assets` | Sales & user-call transcripts in the window; extract customer-feedback moments (quotes, objections, requests) |
| **slack-gmail** | Slack MCP: `slack_search_public_and_private`, `slack_read_channel`, `slack_read_thread`; Gmail MCP: `gmail_search_emails`, `gmail_read_email` | Support/community threads in the configured channels + support/NPS/feedback emails |
| **web-reviews-social** *(best-effort)* | `WebFetch`, `WebSearch` | App Store reviews RSS for the configured app id (`https://itunes.apple.com/us/rss/customerreviews/page=1/id=<APP_ID>/sortby=mostrecent/json`); `WebSearch` Reddit / X / Google Play for "Amp Fit" mentions in-window. **Mark `best_effort: true`.** |

> **HeyMarvin is NOT a windowed collector** — there's no HeyMarvin MCP, so live recent-interview pulls aren't possible. It's handled as the **qualitative baseline in Step 1** (local export). To add live interview pulls, build a HeyMarvin MCP (see *Live HeyMarvin* below) and add a `uxr-heymarvin` collector row here.

**Collector contract (paste into each Task prompt):**
> You are a single-source feedback collector. Window: `<WINDOW>`. Pull customer feedback from
> **`<SOURCE>`** using the tools listed for you. Read everything in YOUR context — do not return
> raw transcripts/threads. Return ONLY this JSON (no prose):
> ```json
> {
>   "source": "<source>",
>   "window": "<window>",
>   "items_reviewed": 0,
>   "best_effort": false,
>   "themes": [
>     {
>       "theme": "short label",
>       "summary": "1–2 sentences",
>       "volume": 0,
>       "sentiment": "positive|mixed|negative",
>       "urgent": false,
>       "quotes": [
>         {"text": "verbatim quote", "source_ref": "url / message id / channel+date", "who": "segment or persona if known"}
>       ]
>     }
>   ],
>   "coverage_notes": "what you searched, what errored, what's missing"
> }
> ```
> Rules: quotes must be **verbatim** with a real `source_ref` (never invent). Flag `urgent: true`
> for outage/data-loss/billing/churn/legal/safety language or sharp negative spikes. If a tool
> errors or returns nothing, say so in `coverage_notes` — don't fail silently.

### Step 3 — Synthesize & cluster
- Merge the digests. **Cluster** similar themes across sources into unified themes; dedupe.
- **Rank** by `volume × severity × sentiment` (negative + high-volume + urgent floats to top).
- **Sentiment trend:** compare overall and per-theme sentiment/volume to the prior report (Δ). First run = baseline.
- **Urgent set:** anything any collector flagged `urgent`, plus negative-sentiment spikes and P1 bug / churn / billing clusters.
- Tag each theme with affected **persona(s)** from the baseline where evident.

### Step 4 — Write the report
Write to `10-outputs/research-synthesis/YYYY-MM-DD_feedback-synthesis.md` (today's date). Use the **Output Format** below.

### Step 5 — Urgent alert (optional, ask first)
If there are urgent items, **offer** to post a short summary to a Slack channel (e.g. `#product` or a configured channel) via `slack_send_message`. Posting is outward-facing — **confirm with the user before sending**, never auto-post.

### Step 6 — Log learnings (optional)
If the synthesis surfaced a reusable, high-confidence (≥7) strategic insight or pitfall, append one line to `01-discovery/learnings.jsonl` following `learnings-schema.md` (only if it'd save 5+ minutes next time).

### Step 7 — Backup (workspace policy)
```bash
tar -czf "/Users/avirangrisaro/Documents/amp-backups/my-brain-$(date +%Y%m%d-%H%M%S).tgz" -C "/Users/avirangrisaro/Documents" my-brain
```

### Step 8 — Report to the user
Reply with: the report path, the **TL;DR**, the **urgent flags**, sources covered (+ any gaps), and a suggested next step (e.g. "want this every Monday? I can schedule it").

---

## Output Format

The report file:

```markdown
---
type: feedback-synthesis
date: YYYY-MM-DD
window: <window>
sources_covered: [posthog, calls, slack-gmail, web-reviews-social]
items_reviewed: <total int>
prior_report: <filename or "none (baseline)">
---

# Voice of Customer — <window>

## TL;DR
- 3–5 bullets: the few things that should change a decision this week.

## 🚨 Urgent — needs attention now
| Issue | Signal | Source(s) | Suggested owner |
|-------|--------|-----------|-----------------|
| ... | spike / verbatim / volume | ... | ... |
*(omit table if nothing urgent — say "Nothing urgent this window.")*

## Top themes
### 1. <Theme> — <sentiment> · vol <n> · Δ <vs last week>
<1–2 sentence summary.> **Personas:** <…>. **Implication for Amp:** <…>.
> "verbatim quote" — <source_ref>
> "verbatim quote" — <source_ref>
*(repeat per theme, ranked)*

## Sentiment trend
Overall: <this window> vs <prior> (<Δ>). Per-theme movers: <up/down>.

## Coverage & gaps
- **PostHog:** <n items> — <notes>
- **Calls (Zoom):** <n> — <notes>
- **Slack + Gmail:** <n> — <notes>
- **App reviews & social:** <n> — ⚠️ *best-effort web scrape (no integration). `TODO: wire a proper App Store / Play / social integration`.*
- **HeyMarvin UXR:** baseline only (export dated <date>) — ⚠️ *point-in-time local export, not live. `TODO: build a HeyMarvin MCP for live interview pulls`.*

## Recommended actions
1. … (owner) — tied to a theme above.
```

## Tool Reference

| Step | Tool | Purpose |
|------|------|---------|
| 0 | Read | Load skill `config.md` (app ids, channels) |
| 1 | Glob / Read | Prior report (deltas) + persona baseline |
| 2 | Task ×4 (general-purpose) | Parallel per-source collectors → digests |
| 2 | PostHog / Zoom / Slack / Gmail MCP, WebFetch, WebSearch | (inside collectors) pull the actual feedback |
| 3 | — | Cluster, rank, trend, persona-tag |
| 4 | Write | Write the dated report |
| 5 | Slack MCP `slack_send_message` | Optional urgent alert (confirm first) |
| 6 | Read / Bash | Append learning to `learnings.jsonl` |
| 7 | Bash | Backup tarball |

## Live HeyMarvin (optional, future)
There is **no HeyMarvin MCP** in this environment and none in the connector registry — so HeyMarvin is used as a **local export baseline** (Step 1), not a live source. HeyMarvin has a REST API, so a live connection is buildable: run `/mcp-builder` to wrap it as an MCP, add the server name to Echo's `mcps`, then add a windowed `uxr-heymarvin` collector to Step 2. Until then, periodically refresh the export in `08-feedback/` to keep the baseline current.

## Automate it (weekly review)
On-demand by default. To run it every week automatically, register a routine with `/schedule`
(e.g. "every Monday 8am, run /synthesize-feedback since last report") or `/loop`. Set this up only
when the user asks.

## Notes
- **Verbatim or nothing.** Every quote needs a real `source_ref`. Never fabricate quotes, counts, or sources.
- **Be honest about coverage.** App reviews & social are best-effort web until a real integration exists — always labeled, never overstated. A source that errors goes in "Coverage & gaps," not silently dropped.
- **Don't re-cluster personas from scratch** — reuse `08-feedback/persona-needs-matrix.md`.
- **One report per run**, dated; trend tracking works by reading the previous report.
