---
name: weekly-review
description: Review week's progress, meetings, learnings
---

## Quick Start

1. Run `/weekly-review` on Friday afternoon (best time) or Monday morning
2. I will scan your workspace: weekly plans, daily plans, PRDs, meeting notes, decisions, and launches from the past 7 days
3. I will generate a focused review comparing plan vs. actual, surfacing key wins, blockers, and learnings
4. Output goes to `content/10-outputs/weekly-reports/YYYY-WXX-weekly-review.md`
5. After the review, I will suggest running `/weekly-plan` to plan next week

**Default output is focused (~150 lines max).** Say "full review" if you want the expanded version with stakeholder pulse, task-level execution metrics, and pattern analysis.

## Purpose

End-of-week synthesis reviewing what you accomplished, what you learned, and what needs attention. Feeds into next week's planning and builds institutional memory.

## Usage

- `/weekly-review` - Review current/past week
- `/weekly-review last-week` - Review previous week (if you forgot)

---

## Context Routing

**Check these files first:**
1. `content/10-outputs/weekly-plans/` - This week's plan (what you intended)
2. `content/10-outputs/daily-plans/` - Daily plans from this week (what actually happened)
3. `content/prds/` - PRDs modified this week
4. `content/10-outputs/meeting-notes/` - Meeting notes from past 7 days
5. `content/10-outputs/launches/` - Launches that happened this week
6. `content/10-outputs/decisions/` - Decisions made this week
7. `content/10-outputs/research-synthesis/` - Research conducted
8. `content/strategy/` - Quarter goals (to track progress)

**MCP Queries (if available):**
- **Linear/Jira MCP** - Tasks completed this week
- **Analytics MCP** - Metrics for features launched recently
- **GitHub MCP** - Code activity (if relevant to your role)
- **Slack MCP** - Key conversations and decisions

**Fallback:** File-based analysis of PM OS workspace + manual input for completions.

---

## Workflow

### Step 0: Stale-Anchor Pre-flight (REQUIRED — runs first)

Refuse to generate a weekly review on a quiet week — confidently wrong fiction is worse than no review. Run these checks before Step 1:

```bash
WEEK_START=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d "7 days ago" +%Y-%m-%d)

# 1) Any content/ commits in the past 7 days?
CONTENT_COMMITS=$(cd /Users/avirang/Documents/amp && git log --since="$WEEK_START" --oneline -- content/ 2>/dev/null | wc -l | tr -d ' ')

# 2) Any PRD files modified in past 7 days?
PRD_MTIME_COUNT=$(find /Users/avirang/Documents/amp/content/03-prds -name "*.md" -mtime -7 2>/dev/null | wc -l | tr -d ' ')

# 3) Any new decisions logged this week?
DECISION_COUNT=$(find /Users/avirang/Documents/amp/content/10-outputs/decisions -name "*.md" -mtime -7 2>/dev/null | wc -l | tr -d ' ')

# 4) Any meeting notes from past 7 days?
MEETING_COUNT=$(find /Users/avirang/Documents/amp/content/09-meetings/prep -name "*.md" -mtime -7 2>/dev/null | wc -l | tr -d ' ')

echo "Activity signal: commits=$CONTENT_COMMITS, prd_mods=$PRD_MTIME_COUNT, decisions=$DECISION_COUNT, meetings=$MEETING_COUNT"
```

**Block rule:**

- **If `CONTENT_COMMITS == 0` AND `PRD_MTIME_COUNT == 0` AND `DECISION_COUNT == 0`**, STOP. Use AskUserQuestion:
  > This looks like a quiet week — no PRD movement, no decisions, no commits to `content/`. Are you sure you want a review? Generating one would produce fiction.
  >
  > - **A) Cancel** (recommended — there's nothing to review)
  > - **B) Proceed anyway** — I'll generate based on calendar + meetings only
  > - **C) Confirm period** — I might be checking the wrong dates

- **If `MEETING_COUNT > 0` but everything else is zero**, warn but proceed: "Meetings happened but no decisions / no PRD work — flagging this as a meeting-heavy / output-light week, not a normal review."

- **Otherwise**, proceed to Step 1.

This gate exists because PMs run the skill habitually and the LLM will confidently produce a review even when nothing happened. The first 5 lines of a review will sound plausible regardless. The gate prevents that.

---

### Step 1: Determine Review Period

1. **Calculate week to review:**
   - Default: Current week (if Friday or later)
   - If Monday-Thursday: Ask "Review last week or current week?"
   - If user specified: Use that week

2. **Check if review already exists:**
   - Look for `content/10-outputs/weekly-reports/YYYY-WXX-weekly-review.md`
   - If exists: Ask "Update existing review or create new version?"

---

### Step 1.5: Prior Learnings (load before data collection)

Surface prior weekly-review learnings — patterns about your own week shape, repeating blockers, stakeholder rhythms:

```bash
bash /Users/avirang/Documents/amp/scripts/learnings-search.sh --skill weekly-review --limit 10
```

If a returned learning matches a pattern observed this week (recurring blocker, meeting that keeps getting cancelled, PRD that always stalls at the same stage), prefix that section with **"Prior learning applied: [key] (confidence N/10)"**.

---

### Step 2: Data Collection

**A. Weekly Plan (What Was Intended):**

Read `content/10-outputs/weekly-plans/YYYY-WXX-weekly-plan.md`:

Extract:
- Top 3 priorities for the week
- Key tasks under each priority
- Success criteria
- Expected meeting load

If no weekly plan exists:
- Note: "Week wasn't planned. Reviewing what happened only."
- Suggest: "Next week, run `/weekly-plan` on Monday for better focus."

---

**B. PRD Progress:**

Scan `content/prds/` and `content/prds/`:

Method 1 - File modification dates:
```bash
# Files modified in the past 7 days
find content/prds/ content/prds/ -name "*.md" -mtime -7
```

For each PRD touched this week:
- Read frontmatter or first section for current stage
- Compare to last week's stage (if weekly review from last week exists)
- Determine: Advanced, Stalled, or New

Method 2 - If Git available:
```bash
# PRDs with commits this week
git log --since="7 days ago" --name-only --pretty=format: | grep -E "prds/.*\.md$" | sort -u
```

**Categorize:**
- **Advanced:** Moved to next stage (Team Kickoff → Planning Review)
- **Active:** Work happened but didn't advance stage
- **Stalled:** No activity this week
- **New:** Started this week

---

**C. Feature Launches:**

Check `content/10-outputs/launches/`:
- Launches completed this week
- Launch checklists finished
- Post-launch monitoring started

For each launch:
If Analytics MCP available:
```
Query metrics since launch date
Compare to success criteria from PRD
```

Categorize:
- ✅ On track (meeting targets)
- ⚠️ Needs attention (below targets)
- ❌ Underperforming (significantly below)
- 🚀 Exceeding (beating targets)

---

**D. Meetings & Decisions:**

Scan `content/10-outputs/meeting-notes/` from past 7 days:

For each meeting:
- Extract date, attendees, topic
- Look for: Decisions made, action items created, blockers identified

Check `content/10-outputs/decisions/`:
- Decision docs created this week
- Link to related meetings

**Build stakeholder pulse:**
- Who did you meet with most? (frequency)
- Who did you miss syncing with? (gaps)
- What topics dominated discussions? (themes)

---

**E. Tasks Completed:**

If Linear/Jira MCP available:
```
Query: Tasks completed in past 7 days
Group by: Priority, PRD/Initiative
Calculate: Planned vs actual completion rate
```

If MCP not available:
- Scan daily plans for checked-off tasks
- Scan meeting notes for completed action items

**Categorize by initiative:**
```
Initiative: [PRD Name]
- ✅ Task 1 (from Priority 1)
- ✅ Task 2 (from Priority 1)
- [ ] Task 3 (carried over - why?)
```

**Calculate metrics:**
- Tasks completed vs planned
- % completion rate
- Carry-over rate

---

**F. User Research & Insights:**

Check `content/11-competitors/`:
- New interview notes this week
- Competitive analysis updates

Check `content/10-outputs/research-synthesis/`:
- Synthesis reports created
- Themes identified

Extract:
- Key findings
- Recurring themes (mentioned in multiple sources)
- Recommendations for roadmap

---

**G. Learnings & Patterns:**

This is where weekly review gets powerful - surfacing patterns.

**From daily plans:**
- What consistently took longer than expected?
- What got deprioritized every day? (maybe not important)
- What meeting prep was valuable vs not?

**From outcomes:**
- What decisions went well? (process to repeat)
- What decisions went poorly? (what to change)
- What blockers kept recurring? (systemic issue)

**From stakeholder interactions:**
- What communication worked well?
- What caused confusion or misalignment?
- Who needs more/less frequent updates?

---

### Step 3: Analysis & Synthesis

**PRD Pipeline Analysis:**

For each PRD:
- Last week's stage → This week's stage
- Movement: ✅ Advanced / → Active / ⚠️ Stalled

**Why analysis:**
- Advanced: What unblocked it? (repeat this)
- Stalled: What's blocking? (action needed)

---

**Strategic Alignment:**

Read `content/strategy/` for quarter goals.

For each goal:
- Which priorities/tasks contributed to it this week?
- Progress estimate: X% → Y% (did we move the needle?)
- Velocity: Are we on track for quarter target?

**Pillar balance:**
If strategy has defined pillars:
- Pillar 1: X% of time this week
- Pillar 2: Y% of time
- Pillar 3: Z% of time

Compare to target allocation: Are we balanced?

---

**Pattern Detection:**

Look for:
- **Recurring blockers:** Same dependency/person blocked multiple things
- **Underestimated tasks:** Consistently took 2x longer than planned
- **Overcommitted weeks:** Planned 30 hours with 25 hours of meetings
- **Meeting value:** Which meetings led to outcomes vs were FYI only?
- **Best working times:** When did deep work happen? (protect these blocks)

---

### Step 4: Generate Weekly Review

Create file: `content/10-outputs/weekly-reports/YYYY-WXX-weekly-review.md`

**Output Length Guidance:**

**Default (focused review, ~150 lines max).** Include only:
1. TL;DR (5-6 bullet summary)
2. Priority Completion (plan vs actual for top 3 priorities)
3. Key Decisions Made (list with one-line rationale each)
4. Metrics Movement (table of metrics that changed)
5. Top 3 Learnings (what worked, what did not, what to change)
6. Next Week Preview (draft priorities + items to unblock)

**Full review (when user asks for it).** Expand to also include:
- Stakeholder pulse (engagement gaps, new relationships)
- Task-level execution metrics (completion rate, carry-over rate, scope creep indicator)
- PRD pipeline table with stage movement
- Meeting value assessment (high/medium/low for each meeting)
- Pattern analysis (recurring blockers, underestimated task types, best working times)
- User research and competitive intelligence updates

**Template:**

```markdown
---
week: YYYY-WXX
week_start: YYYY-MM-DD
week_end: YYYY-MM-DD
quarter: Q[X] YYYY
---

# Weekly Review - Week of [Month] [DD], [YYYY]

## TL;DR

- **PRDs:** [X active], [Y advanced], [Z stalled]
- **Launches:** [N features shipped]
- **Meetings:** [M total], [P key decisions]
- **Completion rate:** [X%] of planned tasks done
- **Key win:** [Biggest accomplishment]
- **Key challenge:** [Biggest blocker/lesson]

---

## Strategic Progress

**Quarter Goal:** [Primary goal for Q]
**Progress This Week:** [What moved forward]

| Goal | Start of Week | End of Week | This Week | Status |
|------|---------------|-------------|-----------|--------|
| [Goal 1] | X% | Y% | +Z% | ✅ On track |
| [Goal 2] | A% | B% | +C% | ⚠️ Behind |

**Velocity check:**
- [X] weeks left in quarter
- [Y%] progress needed per week to hit goal
- [Z%] actual progress this week
- **Assessment:** [On track / Need to accelerate / Ahead]

---

## Top 3 Priorities Review

[Compare planned vs actual]

### Priority 1: [Title]

**Planned:** [What we intended to achieve]
**Actual:** [What we achieved]

**Tasks:**
- ✅ [Task 1] - Done
- ✅ [Task 2] - Done
- [ ] [Task 3] - Carried over because [reason]

**Status:** ✅ Complete / 🟡 Partial / ❌ Not started

**Key outcome:**
- [What this unlocked or enabled]

**Learning:**
- [What went well or what to change]

---

### Priority 2: [Title]

[Same structure]

---

### Priority 3: [Title]

[Same structure]

---

## PRD Pipeline

| PRD | Stage (Start of Week) | Stage (End of Week) | Movement | Next Action |
|-----|----------------------|---------------------|----------|-------------|
| [Name] | Team Kickoff | Planning Review | ✅ Advanced | Get eng estimates |
| [Name] | Solution Review | Solution Review | ⚠️ Stalled | Need legal review |
| [Name] | - | Team Kickoff | 🆕 New | Scope and plan |

**Analysis:**
- **Advanced:** [PRD X] moved forward because [stakeholder signed off / design done / etc.]
- **Stalled:** [PRD Y] blocked on [dependency / decision / resource]
- **Recommendation:** [What to prioritize next week to unblock]

---

## Launches & Impact

### Shipped This Week

[If anything launched]

**[Feature Name]** (Launched [Day])

**Success Criteria (from PRD):**
- [Metric 1]: Target [X], Actual [Y] ([+/-Z%])
- [Metric 2]: Target [A], Actual [B] ([+/-C%])

**Early assessment:** ✅ On track / ⚠️ Needs attention / ❌ Below target / 🚀 Exceeding

**Insights:**
- [User feedback received]
- [Unexpected behavior observed]
- [Next iteration needed]

---

### Post-Launch Monitoring

[Features launched in past 4 weeks still being monitored]

| Feature | Launch Date | Key Metric | Target | Actual | Trend | Status |
|---------|-------------|------------|--------|--------|-------|--------|
| [Name] | [Date] | [Metric] | [X] | [Y] | [↗↘→] | [✅⚠️❌] |

---

## Key Decisions Made

1. **[Decision]** ([Date] - [Meeting])
   - **Context:** [Why this came up]
   - **Decision:** [What was decided]
   - **Rationale:** [Why we chose this]
   - **Owner:** [Who's executing]
   - **Impact:** [What this affects]
   - **Doc:** [Link if exists]

2. **[Decision 2]**
   [Same structure]

---

## Meetings & Stakeholder Pulse

### Meetings This Week: [Total]

| Day | Meeting | Attendees | Outcome | Value |
|-----|---------|-----------|---------|-------|
| Mon | [Topic] | [Names] | [Decision/Alignment] | 🟢 High |
| Tue | [Topic] | [Names] | [Info sharing] | 🟡 Medium |
| Wed | [Topic] | [Names] | [Cancelled] | ⚫ None |

**Meeting load:** [X] hours / 40 = [Y%]
**Deep work time:** [Z] hours (vs [A] hours planned)

**Value assessment:**
- 🟢 High value: Led to decision or unblocked work
- 🟡 Medium value: Useful context but no immediate action
- 🔴 Low value: Could have been async or skipped

**Recommendation:** [Which meetings to keep/change/cancel]

---

### Stakeholder Pulse

**High engagement this week:**
- **[Name]** - [Why: Multiple syncs, key decision, strong collaboration]
  - Impact: [What this enabled]
  - Continue: [Keep this cadence / Increase collaboration]

**Needs attention:**
- **[Name]** - [Why: Haven't synced in 2+ weeks, blocking issue, misalignment suspected]
  - Impact: [What's at risk]
  - Action: [Specific next step - schedule 1:1, send update, etc.]

**New relationships:**
- **[Name]** - [Met for first time, context]
  - Follow-up: [Add to stakeholder profiles, schedule regular sync]

---

## User Research & Insights

[Only include if research happened]

**New Research This Week:**
- **[Interview/Study]** - [Date]
  - Key finding: [Insight]
  - Validates: [Which hypothesis or PRD]
  - Challenges: [What assumption or approach]

**Recurring Themes:**
- **[Theme 1]** - Mentioned in [X] sources
  - Evidence: [Quote or data point]
  - Implication: [What this means for roadmap]

- **[Theme 2]** - Validates hypothesis from [PRD]
  - Evidence: [Quote or data point]
  - Recommendation: [Accelerate this PRD / Pivot approach]

**Competitive Intelligence:**
[If competitive analysis updated]
- [Competitor] launched [Feature]
- Implication: [How this affects our strategy]

---

## Tasks & Execution

**Completion Metrics:**
- **Completed:** [X] tasks
- **Carried over:** [Y] tasks ([Z%] carry-over rate)
- **Added mid-week:** [A] tasks (scope creep indicator)

**By initiative:**

### [Initiative/PRD Name]

- ✅ [Task completed]
- ✅ [Task completed]
- [ ] [Task carried over] - **Why:** [Blocked by X / Deprioritized for Y / Under-estimated]

### [Initiative 2]

[Same structure]

**Patterns:**
- Tasks that took longer than expected: [Type/category]
- Blockers that repeated: [Dependency on X person/team]
- Tasks that got bumped repeatedly: [Maybe not actually important?]

---

## Learnings & Patterns

**What Worked Well:**
- **[Approach/Decision]** - [Why it was effective]
  - Example: [Specific instance]
  - Repeat: [How to apply this pattern again]

**What Didn't Work:**
- **[Mistake/Inefficiency]** - [What happened]
  - Impact: [Consequence]
  - Root cause: [Why this happened]
  - Fix: [Specific change for next time]

**Process Improvements:**
- [ ] [Specific improvement to implement]
  - Why: [Problem it solves]
  - How: [Concrete action]
  - Owner: You
  - By when: [Next week / Next sprint]

**Personal Development:**
[If applicable]
- Skill practiced: [What you worked on]
- Feedback received: [From whom, about what]
- Growth area identified: [What to develop]

---

## Next Week Preview

### Top 3 Priorities (Draft)

[Based on this week's outcomes, suggest next week's priorities]

1. **[Priority 1]** - [Why: Carries over from this week / New urgent item / Strategic next step]
2. **[Priority 2]** - [Why]
3. **[Priority 3]** - [Why]

> Note: Run `/weekly-plan` to formalize these and add detail

---

### Key Meetings Next Week

[From calendar if available]
- **[Day]:** [Meeting] - [Goal/Outcome needed]
- **[Day]:** [Meeting] - [Prep needed]

---

### Items to Unblock

| Item | Blocked Since | Blocked By | Action Needed |
|------|---------------|------------|---------------|
| [PRD/Task] | [Date/Week] | [Person/Dependency/Decision] | [Specific ask] |

**Priority unblocks:**
1. [Most critical blocker to address Monday]
2. [Second priority]

---

## Metrics to Monitor Next Week

[Features to keep watching]

- **[Feature 1]** - [Why: Early launch / Trending down / Critical metric]
  - Watch: [Specific metric]
  - Check: [Daily / Every other day]
  - Flag if: [Threshold or condition]

---

*Generated: [Timestamp]*
*Data sources: [Weekly plan, Daily plans, PRDs, Meeting notes, Linear/Jira, Analytics]*
*Next: Run `/weekly-plan` to plan next week*
```

---

### Step 4.5: Save JSON Snapshot (REQUIRED — enables trend tracking)

After saving the markdown review, write a structured JSON snapshot to `content/10-outputs/weekly-reports/YYYY-WXX.json`. This is what enables next week's review to show ↑↓ deltas.

**Schema:**

```json
{
  "week": "2026-W21",
  "week_start": "2026-05-19",
  "week_end": "2026-05-23",
  "ts": "2026-05-23T16:30:00Z",
  "calendar_notes": "normal | holiday | conference | vacation",
  "prds": {
    "advanced": [
      {"slug": "activity-feed", "from_stage": "Planning Review", "to_stage": "XFN Kickoff"}
    ],
    "stalled": [
      {"slug": "device-lock", "stuck_at_stage": "Solution Review", "weeks_at_stage": 3}
    ],
    "new": ["consistency-leaderboard"],
    "completed_to_launch": []
  },
  "decisions_made": [
    {"key": "rep-counting-paid-only", "file": "content/10-outputs/decisions/rep-counting-paid-only_decision.md"}
  ],
  "experiments": {
    "running": 2,
    "concluded": 1,
    "concluded_keys": ["streak-mechanic-test"]
  },
  "meetings": {
    "total": 14,
    "xfn_meetings": 4,
    "low_value_count": 3
  },
  "tasks": {
    "completed": 18,
    "carried_over": 5,
    "added_mid_week": 7,
    "completion_rate": 0.72
  },
  "launches": [],
  "metrics_referenced": {
    "wau_pp_change": null,
    "w8_retention_pp_change": null
  },
  "biggest_win": "Activity-feed PRD advanced past Planning Review with all 9 reviewers approving.",
  "biggest_challenge": "Device-Lock stalled for 3rd consecutive week at Solution Review."
}
```

**Definitions (be strict):**

- **PRD advanced** — a PRD that moved to a later lifecycle stage during this week. Staying at the same stage doesn't count, even if active work happened.
- **PRD stalled** — a PRD that hasn't moved stage in 2+ consecutive weeks AND has been touched (so it's not dead, it's stuck).
- **PRD new** — a PRD file that didn't exist last week (or that was archived and revived).
- **PRD completed_to_launch** — a PRD that hit Impact Review or Launch Readiness → Launched this week.
- **Decisions** — entries in `content/10-outputs/decisions/` modified or created this week.
- **Experiments** — A/B tests or controlled rollouts running. Pull from `content/prds/` flag-gated PRDs or from any `experiment_*.md`.
- **completion_rate** — `tasks.completed / (tasks.completed + tasks.carried_over)`. If denominator = 0, set to null (don't divide by zero).
- **calendar_notes** — flag the week type. A holiday week's deltas shouldn't be interpreted as regression.

**Write the file:**

```bash
WEEK_LABEL="$(date +%Y)-W$(date +%V)"
SNAPSHOT_PATH="/Users/avirang/Documents/amp/content/10-outputs/weekly-reports/${WEEK_LABEL}.json"
# Compose JSON from the data already collected in Steps 2-3, save:
cat > "$SNAPSHOT_PATH" <<'EOF'
{ "week": "...", ... }
EOF
echo "Snapshot saved: $SNAPSHOT_PATH"
```

### Step 4.6: Read Prior Snapshot + Show Deltas

Read last week's JSON snapshot and compute ↑↓ deltas. Append to the markdown review as a "Week-over-week deltas" section.

```bash
PRIOR_WEEK_LABEL="$(date -v-7d +%Y)-W$(date -v-7d +%V 2>/dev/null || date -d '7 days ago' +%V)"
PRIOR_PATH="/Users/avirang/Documents/amp/content/10-outputs/weekly-reports/${PRIOR_WEEK_LABEL}.json"

if [ -f "$PRIOR_PATH" ]; then
  # Compute deltas via jq
  CURRENT_PATH="$SNAPSHOT_PATH"
  jq -s '{
    advanced_delta:        (.[0].prds.advanced | length) - (.[1].prds.advanced | length),
    stalled_delta:         (.[0].prds.stalled  | length) - (.[1].prds.stalled  | length),
    decisions_delta:       (.[0].decisions_made | length) - (.[1].decisions_made | length),
    meetings_delta:        (.[0].meetings.total) - (.[1].meetings.total),
    completion_rate_delta: ((.[0].tasks.completion_rate // 0) - (.[1].tasks.completion_rate // 0))
  }' "$CURRENT_PATH" "$PRIOR_PATH"
fi
```

Add this section to the bottom of the markdown review:

```markdown
## Week-over-week Deltas (vs [PRIOR_WEEK_LABEL])

| Metric | This week | Last week | Δ |
|---|---|---|---|
| PRDs advanced | N | M | ↑/↓ X |
| PRDs stalled | N | M | ↑/↓ X |
| Decisions logged | N | M | ↑/↓ X |
| Meetings | N | M | ↑/↓ X |
| Task completion rate | X% | Y% | ↑/↓ Zpp |

**Trend signals:**
- [Note any composite signal — e.g., "stalled-to-advancing ratio is 2:1, up from 1:2 — pipeline jam forming"]
- [Holiday/conference week → annotate so deltas aren't misread]
```

If no prior snapshot exists (first run), skip the deltas section gracefully: "First weekly snapshot — deltas will appear from next week."

---

### Step 5: Follow-Up Prompts

After generating review, prompt user with contextual suggestions:

**Always offer:**
> "Week synthesized and saved! Next steps:
>
> 1. **Plan next week?** Run `/weekly-plan` (5-10 min) - I've drafted initial priorities above
> 2. **Share with team?** I can format this as a stakeholder update
>
> What would help?"

**If significant wins:**
> "🎉 Nice work on [Achievement]! Worth documenting this:
>
> - Add to portfolio/resume
> - Share in team update
> - Capture as case study for future reference
>
> Want me to help with any of these?"

**If patterns emerged:**
> "📊 I noticed some patterns:
>
> - [Recurring blocker X] appeared [Y] times
> - [Task type Z] consistently took 2x longer than estimated
>
> Want to dig into these and create process improvements?"

**If learnings captured:**
> "💡 This week's learnings worth remembering:
>
> - [Learning 1]
> - [Learning 2]
>
> I'll surface these in future planning. Want me to add to `content/personal-context/lessons-learned.md`?"

**If metrics concerning:**
> "⚠️ [Feature] metrics need attention:
>
> - [Metric] is [X%] below target
> - Trending [down/flat] since launch
>
> Run `/feature-results` for deeper analysis? Or schedule stakeholder review?"

---

## Capture Learnings (run at skill end)

After producing the review, log any week-shape learning that would save 5+ minutes next time. Schema: `content/01-discovery/learnings-schema.md`.

```bash
bash /Users/avirang/Documents/amp/scripts/learnings-log.sh \
  --skill weekly-review \
  --type <pattern|pitfall|operational> \
  --key <short-slug> \
  --insight "1-2 sentence pattern about your own working rhythm or pipeline behavior." \
  --confidence <1-10> \
  --source observed \
  --files content/10-outputs/weekly-reports/<this-week>.md
```

Good things to log: a meeting type that consistently produces decisions vs. one that's always low-value; a category of task that always carries over (re-plan or kill); a stakeholder rhythm that's been working; a PRD-stage transition that always takes longer than expected. **Skip:** "I had a lot of meetings this week" — that's a number, not a learning.

---

## Integration with Other Skills

**Before `/weekly-review`:**
- `/daily-plan` - Ran throughout the week (provides daily context)
- `/meeting-notes` - Captured meeting outcomes
- `/prd-draft` - Created/updated PRDs this week

**After `/weekly-review`:**
- `/weekly-plan` - Plan next week based on this review
- `/decision-doc` - Document key decisions made
- `/status-update` - Share with stakeholders
- `/feature-results` - Deep dive on launched features

**Parallel use:**
- `/impact-sizing` - Validate completed work had expected impact
- `/competitor-analysis` - If competitive intel emerged this week

---

## Tips for Best Results

**When to run:**
- **Best time:** Friday afternoon (4-5pm)
  - Week is fresh in memory
  - Can plan next week immediately after
  - Creates clean mental closure for weekend
- **Alternative:** Monday morning (reflect before planning)
- **Avoid:** Mid-week (incomplete picture)

**What makes a good review:**
- ✅ Honest about what didn't go well (not just wins)
- ✅ Specific about patterns (not vague "work harder")
- ✅ Actionable improvements (concrete next steps)
- ✅ Connects to strategy (not just task completion)
- ❌ Just a task list (misses the "why" and learnings)
- ❌ All problems, no wins (demotivating)

**How to build the habit:**
- Week 1-2: I'll prompt you Friday afternoon
- Week 3-4: You'll start expecting it (ritual forming)
- Week 5+: Feels incomplete without it

**Use the output:**
- Reference in 1:1s with manager (shows progress)
- Share with stakeholders (transparency)
- Compare month-over-month (velocity trends)
- Review quarterly (pattern detection across multiple weeks)

---

## Related Skills

**Before this:**
- `/daily-plan` - Daily execution throughout week
- `/weekly-plan` - Set priorities at start of week
- `/meeting-notes` - Captured throughout week

**After this:**
- `/weekly-plan` - Plan next week immediately after review
- `/status-update` - Share summary with stakeholders
- `/decision-doc` - Formalize key decisions made

**Periodic use:**
- `/feature-results` - Monthly deep dive on launched features
- `/quarter-review` - (If exists) Quarterly synthesis of weekly reviews

---

## Output Quality Self-Check

Before delivering the weekly review, verify:

- [ ] **Plan vs. actual compared:** If a weekly plan existed, every planned priority is addressed with a status (complete, partial, not started) and a reason for any gap.
- [ ] **Learnings are specific and actionable:** Each learning includes what happened, why, and a concrete change for next time. "Work harder" is not a learning.
- [ ] **Next week priorities are drafted:** At least 3 draft priorities for next week are suggested, grounded in this week's outcomes and strategic goals.
- [ ] **Blockers have owners:** Every unresolved blocker has a specific action and person to contact on Monday.
- [ ] **Metrics referenced where available:** If launches happened or metrics data exists, actual numbers are cited (not just "things went well").
- [ ] **Appropriate length:** Default review is ~150 lines. Full review is longer but still organized with clear section headers. Do not generate a full review unless the user asked for one.
- [ ] **Honest about what did not go well:** The review includes at least one thing that did not go as planned, with root cause analysis. A review with only wins is incomplete.
