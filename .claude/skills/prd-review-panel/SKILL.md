---
name: prd-review-panel
description: Multi-agent PRD review (7 perspectives)
---

## Purpose

Get comprehensive feedback on your PRD from 9 role-specific reviewers in parallel: **Backend engineer, iOS developer, QA, Designer, Legal, Engineering manager, Analyst, User (per persona), Executive manager**.

Catches gaps, challenges assumptions, and surfaces conflicts before stakeholder review.

**Role labels are how reviews are presented to the user. Internal agent file names (`engineer-reviewer.md`, `customer-voice.md`, etc.) are implementation details and must NEVER appear in the verdict output, synthesis file, or summary back to the user. Use the role labels above only.**

**No human names in Owner columns or action lists.** When the synthesis or the in-PRD Verdict section assigns owners to blockers, gaps, or action items, **use the role label from the Contacts table, not the person's name**. Examples:
- ❌ "Owner: Itai" / "Lock the power calc with Itai" — wrong (names a specific person).
- ✅ "Owner: Analyst" / "Lock the power calc with Analyst" — right (role label).

Mapping is read off the PRD's own Contacts table: Product Manager → PM; Design Lead → Designer; Engineering Lead → Backend engineer (or iOS developer / Engineering manager depending on context); Data / Analytics → Analyst; Legal → Legal; QA → QA. Cross-PRD owners use the form "<Sibling feature> PM" (e.g., "Social Profile PM"). This rule applies to: the Per-reviewer verdicts table, the Top Blockers table (Owner column), the Action Items list, the Recommended next step sentence, and the Owner field on every Critical Blocker, Important Gap, and Conflict in the synthesis file.

## Usage

- `/prd-review-panel` - Review a PRD with all 7 sub-agents
- `/prd-review-panel [prd-name]` - Review specific PRD
- `/prd-review-panel --perspectives "eng,design,exec"` - Review with subset of agents

---

## Context Routing

**Check these files first:**
1. `content/prds/` - Active PRDs to review
2. `content/prds/` - Reference PRDs and past reviews
3. `.claude/agents/` - The 7 reviewer personas
4. `content/strategy/` - Strategic context for executive review
5. `content/11-competitors/` - User research for UXR validation

**Reviewer roster (9 roles, role labels only — never expose agent file names):**

| # | Role label (use this in output) | Backing agent persona / lens | Notes |
|---|---|---|---|
| 1 | Backend engineer | `engineer-reviewer.md` (backend lens) | Data model, infra, scale, perf |
| 2 | iOS developer | `engineer-reviewer.md` (iOS lens) | Client-side, UI build, platform constraints |
| 3 | QA | Inline-prompted general agent (no persona file yet) | Test plan, regression risk, edge cases, release readiness |
| 4 | Designer | `designer-reviewer.md` | UX, accessibility, design system alignment |
| 5 | Legal | `legal-advisor.md` | Privacy, COPPA, CCPA/GDPR, App Store |
| 6 | Engineering manager | Inline-prompted general agent (or `sprint-planner.md` + `dev-estimator.md` combined lens) | Scope, sequencing, capacity, dependencies, risk to ship date |
| 7 | Analyst | `data-analyst.md` | Holdout design, MDE, power calc, metric validity, anti-metric coverage |
| 8 | User (per persona, with population count) | `customer-voice.md` | At least 3 personas covering the target segment, an adjacent power-user segment, and a retention-at-risk segment. Each persona row in the output shows population count + % share of eligible pool. |
| 9 | Executive manager | `executive-reviewer.md` | Strategic fit, business impact, prioritization, opportunity cost |

**Optional deep-dive agents (invoke separately, not part of the standard panel):**
- `skeptic.md` — invoke when you want adversarial pressure-testing on a specific assumption.
- `uxr-analyst.md` — invoke when you need a dedicated research-validation deep-dive.
- `competitive-intel.md` — invoke when competitive positioning is the central question.

---

## Workflow

### Step 1: PRD Selection

1. **If user specified PRD name:**
   - Look for it in `content/prds/` and `content/prds/`
   - If found: Proceed
   - If not found: List available PRDs, ask user to choose

2. **If no PRD specified:**
   - Scan `content/prds/` for recent PRDs (modified in last 30 days)
   - List them with:
     - File name
     - Title (from content)
     - Last modified date
     - Current stage (if indicated)
   - Prompt: "Which PRD do you want to review?"

3. **Read the full PRD:**
   - Load complete content
   - Note the current stage (Team Kickoff / Planning Review / XFN Kickoff / Solution Review / Launch Readiness)
   - Identify sections present (some PRDs may be incomplete)

---

### Step 1.5: Mode Selection (REQUIRED before reviewers run)

Every PRD lifecycle stage has a distinct review posture. Pick a mode BEFORE dispatching reviewers and commit to it for the full run. Reviewers must apply the chosen posture consistently — don't let them silently drift.

**The four modes mapped to PRD lifecycle stages:**

| Mode | Stage | Posture | What reviewers do |
|------|-------|---------|--------------------|
| **EXPAND** | Team Kickoff | "What's the 10-star version of this?" | Push ambition. Surface whether the wedge is too narrow. Challenge the framing itself, not the details. |
| **SELECTIVE** | Planning Review | "Which parts deserve quarter commitment?" | Trim the ambitious vision into a shippable v1. Surface dependencies arguing for/against scope. |
| **HOLD** | XFN Kickoff + Solution Review | "Scope is locked. Refine within it." | Stress-test the chosen approach. Surface implementation risks, edge cases, alignment gaps. **Don't reopen the scope debate.** |
| **REDUCE** | Launch Readiness | "Cut anything not v1-essential." | Identify what can be deferred without breaking launch. Apply pre-launch rigor — rollback, kill criteria, comms. |

**Impact Review uses different logic.** It's a retro comparing predicted vs actual, not a forward-looking review. Don't apply these modes — instead pull the original PRD predictions, compare to current data, and log learnings. (See `/investigate-metric` and the boomerang pattern from `/devex-review`.)

### Mode selection prompt

Read the PRD's `Stage:` field. Compute the recommended mode from the mapping. Then use AskUserQuestion:

> The PRD is currently in **[detected stage]**. Recommended review mode is **[mapped mode]**. Pick a mode for this review:
>
> - **A) Use [mapped mode]** (recommended for [detected stage])
> - **B) Use EXPAND** (push ambition / 10-star reframe)
> - **C) Use SELECTIVE** (trim scope to shippable v1)
> - **D) Use HOLD** (lock scope, stress-test approach)
> - **E) Use REDUCE** (pre-launch cut; only what's essential)

Wait for the user's choice. Record it as `REVIEW_MODE`. **Do not proceed to Step 2 without a chosen mode.**

### Commitment Lock

Once `REVIEW_MODE` is chosen:

1. Prepend the mode header to **every** reviewer agent prompt in Step 3:
   ```
   REVIEW MODE: [REVIEW_MODE]
   Posture: [one-line description from the table above]
   Apply this posture consistently throughout your review. Do not drift to a different mode mid-review.
   ```

2. **Reviewers must not silently change posture.** If a reviewer's natural lens conflicts with the mode (e.g., the skeptic agent in HOLD mode wanting to reopen scope, or the executive in EXPAND wanting to cut), they must explicitly flag the conflict at the start of their review with: *"Mode conflict — this review's natural posture conflicts with [REVIEW_MODE]. Flagging as observation, not as scope change."* Then continue within the chosen mode.

3. The Verdict synthesis (Step 5+) must include the mode at the top:
   > **Review mode:** [REVIEW_MODE] — applied to PRD at [detected stage] stage.

This prevents the most common failure mode of multi-agent PRD review: reviewers tearing at the scope from different directions while the PM is trying to lock something down.

---

### Step 2: Review Preparation

**Extract key elements from PRD:**
- **Problem statement** - What user pain are we solving?
- **Hypothesis** - If we build X, then Y will happen because Z
- **Strategic fit** - Why this vs other things?
- **Non-goals** - What's explicitly out of scope?
- **Success metrics** - How we measure success
- **Rollout plan** - A/B test or full launch?
- **Technical approach** - How we'll build it (if specified)
- **UX design** - Mockups, flows, behavior examples
- **Stakeholders** - Who needs to approve/support
- **Risks** - Known concerns or open questions

**Determine review focus based on stage:**

- **Team Kickoff stage:** Focus on problem definition, strategic fit
- **Planning Review stage:** Focus on scope, estimates, prioritization
- **XFN Kickoff stage:** Focus on cross-functional alignment, dependencies
- **Solution Review stage:** Focus on technical approach, UX design, edge cases
- **Launch Readiness stage:** Focus on rollout plan, metrics, compliance

---

### Step 3: Spawn 7 Sub-Agents in Parallel

**CRITICAL: Use single message with multiple Task tool calls for parallel execution. Spawn 9 agents (or however many roles are in the roster) in one message.**

**Every reviewer prompt MUST start with the mode header from Step 1.5:**

```
REVIEW MODE: [REVIEW_MODE]
Posture: [one-line from Step 1.5 table — EXPAND / SELECTIVE / HOLD / REDUCE]
Apply this posture consistently throughout your review. If your natural lens conflicts with this mode, flag the conflict explicitly at the start of your review and continue within the chosen mode anyway.
```

For each role, create a Task. Use the role label in your internal tracking but **never expose internal agent file names** in the prompt text shown to the user or in the synthesis output. The prompt content can read the relevant `.claude/agents/<file>.md` for the lens, but the role label is what appears everywhere user-facing.

Per-role prompt template:

**Agent 1: Engineering Reviewer**
```
Prompt:
You are an engineering reviewer. Review this PRD for technical feasibility.

PRD Content:
[Full PRD text]

Review framework:
1. Technical Feasibility
   - Is the proposed solution technically sound?
   - Are there better technical approaches?
   - What's the complexity (S/M/L/XL)?

2. Dependencies & Integration
   - What systems/services does this touch?
   - What dependencies are missing from the PRD?
   - What could break?

3. Scalability & Performance
   - Will this scale to expected load?
   - What performance concerns exist?
   - What monitoring is needed?

4. Edge Cases & Error Handling
   - What edge cases aren't addressed?
   - How should errors be handled?
   - What failure modes exist?

5. Timeline & Estimates
   - Are engineering estimates realistic?
   - What's missing from the estimate?
   - What unknowns could cause delays?

Provide:
- ✅ What looks good technically
- ⚠️ Concerns or gaps
- ❌ Blockers or red flags
- 💡 Suggestions for improvement

Be specific. Reference line numbers or sections of the PRD.
```

**Agent 2: Design Reviewer**
```
Prompt:
You are a design reviewer. Review this PRD for user experience.

PRD Content:
[Full PRD text]

Review framework:
1. User Experience
   - Is the proposed UX intuitive?
   - Are there better interaction patterns?
   - What friction points exist?

2. Visual Design
   - Do mockups align with design system?
   - Are UI patterns consistent?
   - Is information hierarchy clear?

3. Accessibility
   - Are accessibility requirements specified?
   - Can all users complete the flow?
   - What a11y concerns exist?

4. Edge Cases in UX
   - Error states defined?
   - Loading states clear?
   - Empty states addressed?

5. User Research Validation
   - Is this validated with users?
   - What assumptions need testing?
   - Are there usability risks?

Provide:
- ✅ Strong UX decisions
- ⚠️ Usability concerns
- ❌ UX blockers
- 💡 Design improvements

Be specific about which flows or screens have issues.
```

**Agent 3: Executive Reviewer**
```
Prompt:
You are an executive reviewer. Review this PRD for strategic alignment and business impact.

PRD Content:
[Full PRD text]

Strategic Context:
[Include content from content/strategy/ if available]

Review framework:
1. Strategic Alignment
   - How does this support company strategy?
   - Does it advance key metrics (North Star, OKRs)?
   - Why this vs other opportunities?

2. Business Impact
   - What's the expected ROI?
   - How does this affect revenue/growth/retention?
   - What's the opportunity cost?

3. Prioritization
   - Is this the right thing to build now?
   - What else could the team be working on?
   - What's the urgency/importance trade-off?

4. Market & Competitive
   - How does this position us vs competitors?
   - What market need does this address?
   - What's the differentiation?

5. Resource Allocation
   - Is the team/time investment justified?
   - What other initiatives does this affect?
   - Should we staff this differently?

Provide:
- ✅ Strategic strengths
- ⚠️ Strategic concerns
- ❌ Misalignment with strategy
- 💡 Strategic recommendations

Think like a VP or C-level executive reviewing this for approval.
```

**Agent 4: Legal Advisor**
```
Prompt:
You are a legal/compliance reviewer. Review this PRD for risk and regulatory concerns.

PRD Content:
[Full PRD text]

Review framework:
1. Privacy & Data
   - What user data is collected/stored/processed?
   - Are privacy requirements specified (GDPR, CCPA)?
   - Is data retention addressed?

2. Compliance & Regulations
   - What regulations apply (industry-specific)?
   - Are compliance requirements called out?
   - What legal reviews are needed?

3. Security
   - What security considerations exist?
   - Are security requirements specified?
   - What attack vectors should be considered?

4. Contracts & Terms
   - Does this affect user agreements/ToS?
   - Are B2B contract implications considered?
   - What legal language is needed?

5. Risk Assessment
   - What legal risks exist?
   - What liability concerns apply?
   - What could go wrong legally?

Provide:
- ✅ Legal considerations addressed
- ⚠️ Legal/compliance gaps
- ❌ Legal blockers or high-risk items
- 💡 Risk mitigation recommendations

Flag anything that needs legal team review before proceeding.
```

**Agent 5: UX Research Analyst**
```
Prompt:
You are a UX research analyst. Review this PRD for research validation and user insights.

PRD Content:
[Full PRD text]

User Research Context:
[Include recent research from content/11-competitors/ if relevant]

Review framework:
1. Research Validation
   - What user research supports this?
   - Are assumptions validated or just assumed?
   - What evidence backs the problem statement?

2. User Needs
   - Does this solve a real user pain?
   - How acute is the pain (nice-to-have vs must-have)?
   - What user quotes or data support this?

3. Jobs to Be Done
   - What job is the user trying to accomplish?
   - Does the proposed solution help them do the job?
   - Are there better ways to solve the job?

4. Behavioral Insights
   - What user behaviors are expected?
   - Are those behaviors realistic?
   - What might users actually do (vs intended)?

5. Research Gaps
   - What should be researched before building?
   - What assumptions need validation?
   - What user testing is needed?

Provide:
- ✅ Well-researched decisions
- ⚠️ Unvalidated assumptions
- ❌ Contradicts user research
- 💡 Research recommendations

Reference specific research findings or recommend studies needed.
```

**Agent 6: Skeptic**
```
Prompt:
You are the devil's advocate. Challenge this PRD's assumptions and poke holes.

PRD Content:
[Full PRD text]

Review framework:
1. Challenge the Problem
   - Is this really a problem worth solving?
   - How do we know users care?
   - What if we're wrong about the problem?

2. Challenge the Solution
   - Why is this the right solution?
   - What simpler alternatives exist?
   - What if we just don't build this?

3. Challenge the Metrics
   - Will these metrics actually move?
   - What if success metrics are hit but users hate it?
   - Are we measuring the right things?

4. Challenge the Assumptions
   - What assumptions are we making?
   - Which assumptions are risky?
   - What happens if key assumptions are wrong?

5. What Could Go Wrong
   - Best case / worst case scenarios
   - What are we not thinking about?
   - What second-order effects might occur?

Provide:
- 🤔 Questions that need answers
- ⚠️ Risky assumptions
- ❌ Flawed logic or reasoning
- 💡 Alternative approaches to consider

Be direct. The goal is to strengthen the PRD by challenging it.
```

**Agent 7: Customer Voice**
```
Prompt:
You are simulating the customer perspective. Review this PRD as if you're the target user.

PRD Content:
[Full PRD text]

Review framework:
1. As a User, I Want...
   - Does this actually solve my problem?
   - Is this how I'd want it to work?
   - What am I missing or confused about?

2. First Impression
   - If I see this feature, what's my reaction?
   - Is it immediately valuable or confusing?
   - Would I use this?

3. Daily Use
   - How does this fit my workflow?
   - Does it create more work for me?
   - What friction does it introduce?

4. Comparison to Alternatives
   - How does this compare to competitors?
   - Why would I choose this over alternatives?
   - What would make me switch?

5. Delight vs Frustration
   - What would delight me?
   - What would frustrate me?
   - What's the emotional experience?

Provide:
- ✅ User value delivered
- ⚠️ User confusion or friction
- ❌ User would reject or avoid
- 💡 Ways to increase user love

Write from first person ("I") as the user. Be honest about whether you'd use this.
```

---

### Step 4: Collect & Synthesize Reviews

Once all 7 agents complete (wait for all Task outputs):

**Read each review and extract:**
1. ✅ Strengths (what's working well)
2. ⚠️ Concerns or gaps (important but not blocking)
3. ❌ Blockers (must fix before proceeding)
4. 💡 Suggestions (improvements to consider)

**Identify patterns:**
- **Convergent feedback:** Multiple agents flagging same issue (high priority)
- **Conflicting perspectives:** Agents disagree (requires PM judgment)
- **Blind spots:** Issue only one agent caught (could be critical)

**Categorize all feedback:**

**Critical Blockers** (Must fix before next stage):
- [Issue from Agent X]
- [Issue from Agent Y]
- **Why critical:** [Impact if not addressed]

**Important Gaps** (Address before launch):
- [Gap from Agent X]
- [Gap from Agent Y]
- **Why important:** [Risk or limitation]

**Enhancements** (Consider for v1 or v2):
- [Suggestion from Agent X]
- [Suggestion from Agent Y]
- **Value if added:** [Benefit]

**Conflicting Perspectives** (Requires decision):
- **Agent X says:** [Position]
- **Agent Y says:** [Opposite position]
- **PM decision needed:** [What to prioritize]

---

### Step 5: Generate Review Synthesis

Create file: `content/prds/[prd-name]-review-synthesis.md`

**Template:**

```markdown
---
prd: [PRD filename]
review_date: YYYY-MM-DD
stage: [Current PRD stage]
agents: [engineer, designer, executive, legal, uxr, skeptic, customer]
---

# PRD Review Synthesis: [PRD Title]

**Reviewed:** [Date]
**Current Stage:** [Stage]
**Reviewers:** Engineering, Design, Executive, Legal, UXR, Skeptic, Customer Voice

---

## TL;DR

**Overall Assessment:** [Ready to proceed / Needs minor fixes / Requires significant work / Not ready]

**Critical Blockers:** [X]
**Important Gaps:** [Y]
**Conflicting Perspectives:** [Z]

**Recommended Next Step:** [Specific action]

---

## Critical Blockers

[Must be addressed before moving to next stage]

### 1. [Blocker Title]

**Flagged by:** [Role label(s) — never agent file names]
**Issue:** [Description of the problem]
**Impact if not fixed:** [Consequence]
**Recommendation:** [Specific fix]
**Owner:** [Role label from Contacts table — never a person's name]

---

### 2. [Blocker Title]

[Same structure]

---

## Important Gaps

[Should be addressed before launch, may not block next stage]

### [Gap Category - e.g., "Missing Technical Specs"]

**Flagged by:** [Agent(s)]
**Gap:** [What's missing]
**Risk:** [What could go wrong]
**Recommendation:** [How to fill the gap]

---

## Enhancements to Consider

[Nice-to-haves that would strengthen the PRD or feature]

**From Engineering:**
- [Suggestion]
- [Suggestion]

**From Design:**
- [Suggestion]

**From Executive:**
- [Suggestion]

**From Legal:**
- [Suggestion]

**From UXR:**
- [Suggestion]

**From Skeptic:**
- [Challenging question or alternative]

**From Customer:**
- [User perspective suggestion]

---

## Conflicting Perspectives

[Where agents disagreed - requires PM judgment]

### Conflict 1: [Topic]

**Perspective A** ([Agent]):
- [Position]
- [Rationale]

**Perspective B** ([Agent]):
- [Opposite position]
- [Rationale]

**Decision needed:**
- [What the PM needs to decide]
- [Trade-offs to consider]
- [Recommendation if any]

---

## Detailed Feedback by Perspective

### Engineering Review

**✅ Strengths:**
- [What looks good technically]

**⚠️ Concerns:**
- [Technical concerns or gaps]

**❌ Blockers:**
- [Technical blockers]

**💡 Suggestions:**
- [Engineering improvements]

**Estimated Complexity:** [S/M/L/XL based on feedback]

---

### Design Review

**✅ Strengths:**
- [UX decisions that work well]

**⚠️ Concerns:**
- [Usability issues]

**❌ Blockers:**
- [UX blockers]

**💡 Suggestions:**
- [Design improvements]

**Usability Risk:** [Low/Medium/High]

---

### Executive Review

**✅ Strengths:**
- [Strategic alignment]

**⚠️ Concerns:**
- [Strategic questions]

**❌ Blockers:**
- [Strategic misalignment]

**💡 Suggestions:**
- [Strategic recommendations]

**Business Impact:** [High/Medium/Low]
**Strategic Fit:** [Strong/Moderate/Weak]

---

### Legal Review

**✅ Strengths:**
- [Legal considerations addressed]

**⚠️ Concerns:**
- [Legal/compliance gaps]

**❌ Blockers:**
- [Legal red flags]

**💡 Suggestions:**
- [Risk mitigation]

**Legal Risk:** [Low/Medium/High]
**Requires Legal Team Review:** [Yes/No]

---

### UX Research Review

**✅ Strengths:**
- [Research-backed decisions]

**⚠️ Concerns:**
- [Unvalidated assumptions]

**❌ Blockers:**
- [Contradicts research]

**💡 Suggestions:**
- [Research needed]

**Research Validation:** [Strong/Moderate/Weak]

---

### Skeptic Review

**🤔 Questions to Answer:**
- [Challenging questions]

**⚠️ Risky Assumptions:**
- [Assumptions that need validation]

**❌ Flawed Logic:**
- [Issues with reasoning]

**💡 Alternatives:**
- [Different approaches to consider]

---

### Customer Voice Review

**✅ User Value:**
- [What users will love]

**⚠️ User Friction:**
- [What might confuse or frustrate]

**❌ User Rejection:**
- [What users might hate]

**💡 Delight Opportunities:**
- [Ways to exceed expectations]

**User Sentiment:** [Would love it / Would use it / Might use it / Would avoid it]

---

## Action Items

**Before Next Review:**
- [ ] [Critical blocker 1] - Owner: [Role label]
- [ ] [Critical blocker 2] - Owner: [Role label]

**Before Launch:**
- [ ] [Important gap 1] - Owner: [Role label]
- [ ] [Important gap 2] - Owner: [Role label]

**Decisions Needed:**
- [ ] [Decision on conflict 1] - Owner: PM
- [ ] [Decision on conflict 2] - Owner: PM

---

## Next Steps

1. **Immediate:** [What to do right now]
2. **This week:** [What to tackle soon]
3. **Before next stage:** [What must be done]

**Recommended:**
- Run `/decision-doc` for conflicting perspectives
- Update PRD to address blockers
- Schedule follow-up review after fixes (if needed)

---

*Generated: [Timestamp]*
*Agents used: 7 (Engineering, Design, Executive, Legal, UXR, Skeptic, Customer)*
*Next: Update PRD → Re-review or proceed to next stage*
```

---

### Step 5.5: Write the verdict into `review-synthesis.md` — do NOT stamp it into the PRD body

**Changed 2026-07-25 (PRD restructure).** The PRD's new 6-section shape (Description / Motivation / Requirements / Technical design / Assumptions / Open questions & risks / Decisions log — see `.claude/skills/feature-prd/SKILL.md`) has no `Review Panel Verdict`, `Per-reviewer verdicts`, `Severity totals`, `Top reframes`, `Top blockers`, or `Prior reviews` section, and never gets one — that content lives ONLY in the sibling `review-synthesis.md`, never duplicated into the PRD. Old PRDs that still had a `Review Panel Verdict` section stamped in the body had that content moved out and merged into `review-synthesis.md` as part of the 2026-07-25 restructure; do not reintroduce it.

**What to write, and where:**

1. Write/update the sibling `review-synthesis.md` in the same folder as the PRD with the full verdict content (template below, unchanged).
2. In the PRD itself, add at most a one-line pointer inside `## Open questions & risks` — e.g. `- Review panel verdict pending/recorded: see [review-synthesis.md](./review-synthesis.md).` Do not add a table, a per-reviewer breakdown, or anything more than that pointer line to the PRD body.
3. Bump the PRD's `Last updated` field to today's date. There is no PRD version number field in the new shape (no `vX.Y` in Status) — don't invent one.
4. Log the review event as a row in the PRD's bottom `Decisions log` table (`Date | Decision / change | Why`), e.g. `| YYYY-MM-DD | Review panel run, verdict: <one phrase> | <why, if recoverable> |`.

**Section template (write into `review-synthesis.md`, not the PRD):**

```markdown
## Review Panel Verdict

**Latest review:** YYYY-MM-DD (PRD vX.Y) — **<overall verdict — one phrase>**
**Review mode:** <EXPAND | SELECTIVE | HOLD | REDUCE> (applied to <detected stage>)

### Per-reviewer verdicts

| Reviewer | Status | One-line verdict |
|----------|--------|------------------|
| Backend engineer | Approve / Conditional / Concerns / Block / (pending) | <Top concern, one line.> |
| iOS developer | … | … |
| QA | … | … |
| Designer | … | … |
| Legal | … | … |
| Engineering manager | … | … |
| Analyst | … | … |
| User — <Persona name> (~<count>, ~<% of eligible pool>) | Would love it / Would use it / Might use it / Would avoid it | <Top reaction, one line.> |
| User — <Persona name> (~<count>, ~<% of eligible pool>) | … | … |
| User — <Persona name> (~<count>, ~<% of eligible pool>) | … | … |
| Executive manager | … | … |

**Status values:** Approve / Conditional / Concerns / Block / (pending run).
**User persona statuses:** Would love it / Would use it / Might use it / Would avoid it.

### Severity totals

| Severity | Count |
|----------|-------|
| Critical blockers | N |
| Important gaps | N |
| Conflicts requiring PM decision | N |

### Top blockers (must fix before next stage)

1. <Blocker> — <Owner>
2. <Blocker> — <Owner>
...

**Recommended next step:** <One sentence, action-oriented.>

**Full synthesis:** [review-synthesis.md](./review-synthesis.md)

---

### Prior reviews

<If first review: write "*No prior reviews — this is the first.*">
<If subsequent: collapse the previous latest-review block here, oldest at bottom, as a compact 1–3 line summary per prior review:>

- **YYYY-MM-DD (vX.Y)** — <verdict>. N blockers, N gaps. [Synthesis](./review-synthesis-YYYY-MM-DD.md)
```

**User persona sizing (mandatory for User rows):**

Each User row must include the persona's population count and share of the leaderboard-eligible (or feature-relevant) pool. Pull counts from Omni / Amplitude / Snowflake against the relevant filter combo. Show both absolute count and % of pool: `User — <Persona> (~<N>, ~<X%>)`. If population is approximate, prefix with `~`. If the persona crosses multiple buckets, sum the buckets.

**Update logic when `review-synthesis.md` already exists:**

1. **Read `review-synthesis.md`** (not the PRD — the verdict content lives there only, see Step 5.5 above).
2. **If it exists:**
   - Extract the current top block (the "Latest review" content above the `### Prior reviews` subheading).
   - Reformat that extracted block as a 1–3 line summary and prepend it to the `### Prior reviews` list (newest prior at the top).
   - Replace the top block with the new latest-review content.
3. **If it does not exist:** create it with the template above, and initialize `### Prior reviews` with `*No prior reviews — this is the first.*`
4. **Save `review-synthesis.md`.** In the PRD, update (or add, if missing) the one-line pointer in `Open questions & risks` and add a `Decisions log` row — see Step 5.5. Bump the PRD's `Last updated` field.
5. **If the PRD has an `.html` twin**, re-render it (`python3 scripts/md-to-html.py <path>`) so it picks up the `Last updated` bump and pointer line — the verdict detail itself only needs to render inside `review-synthesis.md`'s own HTML twin, if one exists.

**Synthesis filename convention (for the link):**
- Default: `./review-synthesis.md` (overwritten on each review).
- If you want to keep history of synthesis files (recommended for high-stakes PRDs), use `./review-synthesis-YYYY-MM-DD.md` and link the dated file in the "Prior reviews" list.

**One-liner verdicts (use these or paraphrase):**
- "Approve" — no blockers, ready for next stage.
- "Conditional approve" — minor gaps only, can proceed in parallel with fixes.
- "Needs minor fixes" — 1–2 blockers, fast cycle.
- "Needs significant work" — 3+ blockers or conflicts. Not ready for next stage.
- "Not ready / send back" — fundamental issues with mechanic, hypothesis, or strategy.

---

### Step 6: Output & Next Actions

1. **Save review synthesis file**

2. **Display summary:**
   ```
   7-agent review complete for [PRD]!

   ✅ Strong areas: [X]
   ⚠️ Critical blockers: [Y]
   💡 Key recommendations: [Z]

   Overall: [Ready to proceed / Needs work]

   Verdict stamped into PRD §"Review Panel Verdict" (PRD bumped to vX.Y).
   Full synthesis: [path]
   ```

3. **Offer next steps:**
   - If blockers exist: "Want me to help update the PRD to address blockers?"
   - If conflicts exist: "Run `/decision-doc` to document the [Conflict] decision?"
   - If ready: "PRD looks solid! Ready for stakeholder review."
   - Always: "Review synthesis saved to [file path]"

---

## Integration with Other Skills

**Before `/prd-review-panel`:**
- `/prd-draft` - Create the initial PRD
- `/user-interview` - Gather research to validate PRD
- `/impact-sizing` - Quantify expected value

**After `/prd-review-panel`:**
- `/decision-doc` - Document decisions on conflicting perspectives
- `/prd-draft` - Update PRD based on feedback
- `/prototype` - Build prototype for validation
- `/launch-checklist` - Plan the launch

**Iterative use:**
- Run review at each PRD stage (Team Kickoff, Planning, Solution, Launch)
- Each review focuses on stage-appropriate concerns

---

## Tips for Best Results

**When to run:**
- After completing first draft (Team Kickoff stage)
- Before stakeholder review (catch gaps privately first)
- After major changes (validate new approach)
- Before committing to build (final gate)

**How to use the output:**
- Address blockers immediately (don't proceed without fixing)
- Discuss conflicts in next stakeholder meeting
- Park enhancements for v2 (don't let perfect kill good)
- Use as peer review before formal review

**Common patterns:**
- Engineering often conflicts with Design (speed vs polish)
- Executive often conflicts with Customer (business vs user needs)
- Legal often blocks what users want (compliance vs freedom)
- **Your job as PM:** Make the call, document the trade-off

---

## Related Skills

**Before this:**
- `/prd-draft` - Create the PRD
- `/user-research-synthesis` - Validate with research
- `/impact-sizing` - Quantify value

**After this:**
- `/decision-doc` - Document key decisions
- `/prototype` - Build based on feedback
- `/launch-checklist` - Prepare for launch

**Complements:**
- `/competitor-analysis` - Inform strategic review
- `/stakeholder-update` - Share review results

---

## Output Quality Self-Check

Before presenting output to the PM, verify:

- [ ] **All requested reviewer perspectives included:** The synthesis contains feedback from all 7 sub-agents (or all specifically requested agents), each with their own dedicated section
- [ ] **Each reviewer has specific, actionable feedback:** Every reviewer section contains at least one concrete, actionable item (not generic praise like "looks good" or vague concerns like "needs more detail")
- [ ] **Conflicting perspectives between reviewers explicitly flagged:** Any disagreements between agents (e.g., Engineering wants simplicity while Design wants richness) are called out in the "Conflicting Perspectives" section with both positions stated
- [ ] **Synthesis section prioritizes feedback items:** The TL;DR and summary sections rank issues by severity (Critical Blockers > Important Gaps > Enhancements) with a clear recommended next step
- [ ] **Feedback references specific PRD sections:** Each piece of feedback points to the exact section, requirement, or design element it applies to (e.g., "the rollout plan in Section 5" not "the rollout approach")
- [ ] **Verdict written to `review-synthesis.md`, NOT stamped into the PRD body** (changed 2026-07-25 — see Step 5.5): the sibling `review-synthesis.md` has the latest review summary, severity counts, top blockers with owners; the PRD itself gets only a one-line pointer in `Open questions & risks` plus a `Decisions log` row. `Last updated` bumped accordingly.
- [ ] **Prior reviews preserved:** If this is not the first review, the previous verdict block is moved to `### Prior reviews` as a 1–3 line summary (not deleted).
- [ ] **Role labels everywhere, no human names:** Verify the Per-reviewer verdicts table, Top Blockers Owner column, Action Items, Recommended next step, and every Owner field in the synthesis use role labels (Analyst, Backend engineer, Designer, Legal, PM, QA, Social Profile PM, etc.) — never a person's first or last name.
