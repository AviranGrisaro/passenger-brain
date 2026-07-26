---
name: review-pr
description: Review a GitHub PR for regressions, conflicts, and code quality. Uses the pr-reviewer agent to analyze diffs and decide whether to approve or request changes. Essential for multi-contributor safety.
---

## Purpose

Automated PR review gate for the Product OS repo. When multiple people (Aviran, Serge, etc.) push changes, this skill catches regressions, merge conflicts, and bugs before they hit main.

## Usage

- `/review-pr` — Review all open PRs
- `/review-pr 42` — Review PR #42 specifically
- `/review-pr --author serge` — Review PRs from a specific author
- `/review-pr --act` — Review AND post the verdict as a GitHub review (approve/request changes)

---

## Context Routing

**Check these first:**
1. GitHub API — Fetch open PRs, diffs, and existing reviews
2. `.claude/agents/pr-reviewer.md` — The reviewer persona and framework
3. Recent commits on `main` — Understand current state
4. Other open PRs — Check for conflicts between PRs

---

## Workflow

### Step 1: Identify PRs to Review

1. **If PR number specified:** Fetch that specific PR
2. **If author specified:** Filter open PRs by author
3. **If no arguments:** List all open PRs and let user choose, or review all

**For each PR, gather:**
- PR metadata (title, author, branch, description)
- File diff (changed files + patch content)
- List of other open PRs (for conflict detection)
- Recent commits on main (for regression context)

Use the GitHub API via the configured token:
```
GET /repos/{owner}/{repo}/pulls/{number}
GET /repos/{owner}/{repo}/pulls/{number}/files
GET /repos/{owner}/{repo}/pulls?state=open
```

### Step 2: Analyze Each PR

For each PR being reviewed, use the `gh` CLI or GitHub API to:

1. **Fetch the diff:**
   ```bash
   gh pr diff {number} --repo {owner}/{repo}
   ```

2. **Fetch other open PRs for conflict detection:**
   ```bash
   gh pr list --repo {owner}/{repo} --state open --json number,title,headRefName,files
   ```

3. **Check recent main commits for context:**
   ```bash
   git log main --oneline -20
   ```

4. **Read the pr-reviewer agent instructions:**
   - Load `.claude/agents/pr-reviewer.md`
   - Apply all 6 review dimensions

### Step 3: Generate Review Verdict

For each PR, produce a structured review following the pr-reviewer agent's output format:

- **APPROVE** — Safe to merge, no concerns
- **REQUEST CHANGES** — Has issues that must be fixed before merging
- **NEEDS DISCUSSION** — Ambiguous, needs human judgment

### Step 4: Act on Verdict (if --act flag)

If the user passed `--act`:

1. **APPROVE:** Post an approving review via GitHub API
   ```bash
   gh pr review {number} --approve --body "..."
   ```

2. **REQUEST CHANGES:** Post a review requesting changes
   ```bash
   gh pr review {number} --request-changes --body "..."
   ```

3. **NEEDS DISCUSSION:** Post a comment (not a formal review)
   ```bash
   gh pr comment {number} --body "..."
   ```

If no `--act` flag, just display the review to the user for their decision.

### Step 5: Cross-PR Conflict Report

After reviewing individual PRs, generate a conflict matrix:

```markdown
## Cross-PR Conflict Report

| PR | Files | Overlaps With | Risk |
|----|-------|---------------|------|
| #42 (Serge) | server/routes/tasks.ts | #45 (Aviran) | HIGH — both modify task parsing |
| #43 (Serge) | src/stores/project.ts | None | LOW |
| #45 (Aviran) | server/routes/tasks.ts, src/components/Tasks.tsx | #42 (Serge) | HIGH |

### Recommended Merge Order
1. Merge #43 first (no conflicts)
2. Merge #42 next (contains the task parser changes)
3. Rebase #45 after #42 merges (needs to pick up new parser)
```

---

## Output Format

```
PR Review Complete!

Reviewed: [X] PRs
✅ Approved: [list]
❌ Changes Requested: [list]
💬 Needs Discussion: [list]
⚠️ Cross-PR Conflicts: [count]

[Detailed review for each PR]
[Cross-PR conflict report]
```

---

## Integration with Other Skills

**Triggers well after:**
- Someone pushes a PR (manual trigger or scheduled)
- `/daily-plan` — Include PR review in morning routine
- GitHub webhook (future: auto-trigger on new PR)

**Pairs with:**
- `/create-tickets` — If review finds issues, create follow-up tickets
- `/status-update` — Include PR review status in stakeholder updates

---

## Output Quality Self-Check

Before presenting to user, verify:
- [ ] Every concern references a specific file and line/section
- [ ] Every "request changes" item has a concrete fix suggestion
- [ ] Cross-PR conflict check was performed
- [ ] Verification steps are actionable (not generic "test it")
- [ ] Review tone is constructive, not nitpicky
