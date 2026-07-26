---
name: ship
description: Check Product OS changes, generate a conventional commit, and push to git. Surveys diffs, proposes a commit message, and pushes after user confirmation.
---

## Purpose

One-command git workflow: review changes, commit with a proper conventional message, and push. Prevents forgotten commits and ensures clean git history.

## Usage

- `/ship` — Review all changes, commit, and push
- `/ship --dry` — Show what would be committed without actually committing

---

## Workflow

### Step 1: Survey the workspace

Run these commands to understand the current state:

```bash
git status
git diff --stat
git log --oneline -5
git branch --show-current
git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "0 unpushed commits"
```

Report to the user:
- **Current branch** and tracking status
- **Unpushed commits** (already committed but not pushed)
- **Staged changes** (ready to commit)
- **Unstaged changes** (modified tracked files)
- **Untracked files** (new files not yet in git)

### Step 2: Classify changes

Group files into categories:

| Category | Examples | Default action |
|----------|---------|----------------|
| **Product OS code** | `product-os-server/src/**`, `product-os-server/server/**` | Stage |
| **Skills & agents** | `.claude/skills/**`, `.claude/agents/**` | Stage |
| **Config & build** | `package.json`, `tsconfig.json`, `vite.config.*` | Stage |
| **Templates** | `Templates/**` | Stage |
| **Adhoc scripts** | `scripts/adhoc_*`, `scripts/*_check*.py` | Flag — ask user |
| **Sensitive / gitignored** | `content/**`, `.env*`, `*.json` with keys | Never stage |

**Important**: Never stage files matching `.gitignore` patterns. Never stage files that might contain secrets (API keys, tokens, credentials).

### Step 3: Read diffs and draft commit message

1. Run `git diff` (unstaged) and `git diff --cached` (staged) to read actual changes
2. Analyze the nature of changes:
   - New feature → `feat: <description>`
   - Bug fix → `fix: <description>`
   - Refactor → `refactor: <description>`
   - Config/build change → `chore: <description>`
   - Documentation → `docs: <description>`
   - Multiple types → use the dominant one, mention others in body
3. Draft a commit message following repo conventions:
   - Subject line: `<type>: <concise description>` (under 72 chars)
   - Body (if needed): explain **why**, not what
   - Trailer: `Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>`

### Step 4: Present summary and ask for confirmation

Show the user:

```
## Ship Summary

**Branch**: <branch> → origin/<branch>
**Unpushed commits**: <N>

### Changes to commit:
- <file1> (modified) — <brief description>
- <file2> (new) — <brief description>

### Flagged (not included):
- scripts/adhoc_foo.py — adhoc script, include? [y/N]

### Proposed commit message:
feat: <description>

<body if applicable>

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

Use **AskUserQuestion** to confirm:
- "Ship these changes with this commit message?"
- Options: "Ship it", "Edit message first", "Add/remove files", "Cancel"

### Step 5: Commit

On confirmation:

1. Stage the approved files: `git add <file1> <file2> ...` (specific files, never `git add -A`)
2. Commit with the approved message using HEREDOC format

### Step 5.5: Verification Gate (before pushing)

**IRON LAW: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

Before pushing, if any product code changed in this turn (not just docs / .md / config), verify it still works:

1. **Type check:** If `product-os-server/` or any `.ts`/`.tsx` was touched, run `cd product-os-server && npx tsc --noEmit` and paste fresh output. Stale output from earlier in the turn is NOT acceptable.
2. **Build verification:** If `vite.config.*`, `package.json`, or build-relevant files changed, run `cd product-os-server && npm run build` and paste output.
3. **Smoke check:** If a dashboard tab, route, or component was modified and the dev server is running, hit the affected route via `preview_*` and confirm it renders without console errors.

**Rationalization prevention:**
- "Should work now" → RUN IT.
- "I'm confident" → Confidence is not evidence.
- "I already tested earlier in the turn" → Code changed since then. Test again.
- "It's a trivial change" → Trivial changes break production.
- "It's only a .md file" → Skip verification only if EVERY changed file is `.md` / `.gitignore` / pure docs.

**If verification fails here:** STOP. Do not push. Fix the issue, re-stage, re-verify, then continue.

Claiming work is complete without verification is dishonesty, not efficiency.

### Step 6: Push

3. Push: `git push` (if tracking branch exists) or `git push -u origin <branch>` (if not)
4. Report: commit SHA, push result, link to branch on GitHub

### Step 6: Handle edge cases

- **Nothing to commit, nothing to push**: Report "All clean, nothing to ship."
- **Nothing to commit, unpushed commits**: Ask "Push N existing commits?" then push
- **Merge conflicts**: Report the conflict, do not attempt to resolve
- **No upstream branch**: Offer to create one with `git push -u origin <branch>`
- **`--dry` flag**: Stop after Step 4, do not commit or push

---

## Safety Rules

1. **Never force-push** (`--force` or `--force-with-lease`)
2. **Never commit secrets** — scan for API keys, tokens, passwords in diffs
3. **Never stage `content/`** — it's gitignored for a reason
4. **Always show diff before committing** — no silent commits
5. **Always get user confirmation** before `git commit` and `git push`
6. **Stage specific files** — never use `git add -A` or `git add .`
