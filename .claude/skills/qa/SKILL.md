---
name: qa
description: Browser-driven QA testing for the Product OS dashboard (or any localhost web app). Opens the dev server in a preview, walks through pages, documents bugs with screenshots, classifies by severity, optionally applies fixes with WTF-likelihood self-regulation. Triggers — "qa the dashboard", "find bugs", "test this", "does this work", "check the deploy", "/qa".
disable-model-invocation: false
user-invocable: true
---

## Quick Start

```
/qa                           → QA all touched dashboard surfaces against current branch
/qa <URL>                     → QA a specific URL (localhost or staging)
/qa --tier quick              → Quick pass (~5 pages, surface bugs only)
/qa --tier exhaustive         → Deep pass (every tab, every flow, edge cases)
/qa --report-only             → Find and document; never fix (sibling of `/qa-only`)
/qa --diff                    → Auto-scope to pages affected by the current branch diff
/qa --regression <baseline>   → Diff against a prior QA report
```

**Default behavior:** Open Product OS at `localhost:5173`, walk every dashboard tab the diff touches, document bugs incrementally, optionally fix with WTF-likelihood guardrails, write report to `content/10-outputs/qa-reports/<YYYY-MM-DD>-<slug>.md`.

---

## Core Tooling: preview_* (NOT $B, NOT Claude-in-Chrome)

This skill uses Claude Code's built-in `mcp__Claude_Preview__*` tools — `preview_start`, `preview_click`, `preview_fill`, `preview_screenshot`, `preview_snapshot`, `preview_console_logs`, `preview_network`, `preview_eval`, `preview_inspect`, `preview_resize`. Never use `mcp__Claude_in_Chrome__*` for QA — it controls Aviran's real Chrome with real cookies and is slow.

### The verification workflow (from system prompt)

After any change you're QA'ing, the flow is:
1. `preview_start` (if no server is running)
2. Reload via `preview_eval window.location.reload()` if needed (HMR usually handles it)
3. Check `preview_console_logs` / `preview_logs` / `preview_network` for errors
4. `preview_snapshot` for content and structure
5. `preview_inspect` for CSS values
6. `preview_click` / `preview_fill` to test interactions, then `preview_snapshot` to confirm
7. `preview_resize` for responsive / dark-mode

Share proof via `preview_screenshot` for visual issues, `preview_network` for API issues, `preview_logs` for server-side issues.

---

## Phase 1: Setup

### 1a. Determine scope

Before opening anything, decide what's being tested.

- **Default (`/qa`):** Diff-aware mode. Run `git status` + `git diff --stat origin/main...HEAD`. Map changed files to dashboard surfaces using this table:

| Changed paths | Dashboard surfaces to QA |
|---|---|
| `product-os-server/src/components/codebase/**` | Ask Code tab |
| `product-os-server/src/components/prds/**` | PRDs tab |
| `product-os-server/src/components/projects/**` | Projects tab |
| `product-os-server/src/components/calendar/**` | Calendar tab |
| `product-os-server/src/components/jira/**` | Backlog, Sprints tabs |
| `product-os-server/src/components/notes/**` | Notes tab |
| `product-os-server/src/components/data/**` | Data tab |
| `product-os-server/src/components/figma/**` | Proto tab |
| `product-os-server/src/components/capabilities/**` | Capabilities tab |
| `product-os-server/src/components/uxr/**` | UXR tab |
| `product-os-server/src/components/vision/**` | Vision tab |
| `product-os-server/src/components/release-notes/**` | Releases tab |
| `product-os-server/src/components/daily-summary/**` | Daily Summary tab |
| `product-os-server/src/components/layout/**` | All tabs (shell-level change) |
| `product-os-server/server/**` | Every tab that calls the affected route |

- **With URL:** Skip diff mapping, go directly to the URL.
- **`--tier exhaustive`:** Force every tab regardless of diff.

### 1b. Clean working state check

If the working tree has unstaged changes that aren't part of the QA scope, note them. Fixes from this QA pass should be committed atomically per bug — pre-existing edits muddy the diff.

### 1c. Start the dev server

```
preview_start  →  http://localhost:5173 (Vite)
                  http://localhost:5174 (Express API + WebSocket)
```

If `preview_start` fails because a port is in use, that usually means a real dev server is already running. Use it.

### 1d. Health-score baseline

Before fixing anything, take a baseline. After the QA pass, compare. If final < baseline, something regressed during the fix loop.

```
Baseline computed at end of Phase 6.
```

---

## Phase 2: Authenticate (if needed)

Product OS uses per-user OAuth flows for Google, Jira, Slack, Atlassian, Amplitude. For QA against `localhost:5173`, you're already authenticated as `avirang@ampfit.com` — no cookie import needed. If hitting a staging URL with auth, document this and ask the user to log in via `preview_click` / `preview_fill` before continuing.

**Credential safety:** Never write real credentials into the QA report. Use `[REDACTED]` in repro steps.

---

## Phase 3: Orient

Run one initial pass to understand the surface:

1. `preview_screenshot` of the landing screen (Tasks tab is default)
2. `preview_snapshot` to capture the accessibility tree
3. `preview_console_logs` to check the baseline error state
4. List every visible tab (read from `SidebarNav.tsx` or via snapshot)

Record: which tabs exist, which are visible, what the initial state looks like. This is the orientation — bugs are noted but not yet investigated.

---

## Phase 4: Explore (Per-Page Checklist)

For each in-scope tab, walk this checklist. Document bugs incrementally — append each finding to the report as you see it. Don't batch.

### Per-page checklist

1. **Visual scan** — `preview_screenshot`. Look for layout issues, broken images, alignment, overflow.
2. **Interactive elements** — Click every button, link, and primary control. Does each do what its label says?
3. **Forms** — Fill and submit. Test empty submit, invalid input, edge cases (long text, special characters, paste).
4. **Navigation** — Tab switching, sidebar collapse, deep links via URL bar.
5. **States** — Empty state, loading state, error state, full/overflow state. Force them where possible (e.g., disconnect from network for error states, clear data for empty states).
6. **Console** — `preview_console_logs` after every interaction. Any new JS errors or failed network calls?
7. **Network** — `preview_network` to confirm API calls succeed. 4xx and 5xx on background polling counts as a bug.
8. **WebSocket** — Product OS uses ws://localhost:5174/ws. Verify it reconnects after a brief disconnect (check by killing/restarting the server).
9. **Responsiveness** — `preview_resize 375 812` (iPhone), `preview_resize 768 1024` (iPad), back to default. The dashboard is desktop-first but mobile shouldn't crash.

### Cross-cutting flows worth checking

When the diff touches a shared concern, walk one end-to-end:

- **PRD lifecycle:** Open PRDs tab → click a PRD → does the renderer work? Are stage badges correct? Are filter chips clickable?
- **Refresh:** Sidebar refresh button → does it pool calendar/jira/tasks? Does notetaker dedup work? (Per memory `feedback_refresh_behavior.md`.)
- **Telegram integration:** Settings → Telegram bot status → does auto-detection work?
- **Codebase Q&A:** Ask Code tab → submit a question → does it complete? Console errors?

---

## Phase 5: Document Each Bug Immediately

For every issue, write an ISSUE-NNN block to the report as you find it. Append-only. Don't wait to batch.

### What to record

- **Severity:** critical / high / medium / low (see `references/issue-taxonomy.md`)
- **Category:** visual / functional / ux / content / performance / console / accessibility
- **URL:** the page where it appears
- **Description:** what's wrong, expected vs actual — one paragraph
- **Repro steps:** numbered, with `preview_screenshot` evidence per step

### Two-tier evidence

- **Interactive bugs** (click does wrong thing, form misbehaves): 4-step screenshot sequence — before, action, after, then `preview_snapshot` diff
- **Static bugs** (layout, copy, accessibility): single annotated screenshot

### Important rules

1. **Repro is everything.** Every issue needs at least one screenshot. No exceptions.
2. **Verify before documenting.** Retry once to confirm it's reproducible, not a fluke.
3. **Never include credentials.** `[REDACTED]` for passwords.
4. **Write incrementally.** Append each issue. Don't batch.
5. **Check console after every interaction.** JS errors that don't surface visually are still bugs.
6. **Show screenshots to Aviran.** After every `preview_screenshot`, the file is captured; reference it in the report so it renders inline when opened.
7. **Never refuse to use the browser.** When the user invokes `/qa`, they're asking for browser-based testing. Don't suggest evals or unit tests as substitutes. Even a backend-only diff can affect dashboard behavior — open the browser and test.
8. **Depth over breadth.** 5-10 well-documented issues with evidence > 20 vague descriptions.

---

## Phase 6: Triage Tier

Decide how deep to go based on what you've found.

- **Quick (≤3 critical/high in 10 minutes):** stop exploring after the in-scope tabs. Move to fix loop.
- **Standard (5-10 issues across multiple tabs):** finish all in-scope tabs, then fix. Default.
- **Exhaustive (15+ issues OR severe regression suspected):** walk every tab regardless of diff, then triage before fixing.

Record baseline health score now. Health score components:
- Console: 100 - 5 per JS error - 2 per warning (min 0)
- Functional: 100 - 25 per critical - 10 per high - 5 per medium - 1 per low (min 0)
- Visual: 100 - 10 per visual high - 5 per visual medium (min 0)
- UX: 100 - 10 per UX high - 5 per UX medium (min 0)
- Performance: subjective 0-100 based on load + interaction feel
- Accessibility: 100 - 10 per high - 5 per medium (min 0)

Composite health = weighted mean. Save it. After fixes, recompute. If final < baseline, WARN — something regressed.

---

## Phase 7: Fix Loop (skip if --report-only)

For each issue, in severity order:

### Per-issue fix workflow

1. **Locate.** Use Grep / Read to find the relevant code. For React components, the path mapping from Phase 1a points to the file.
2. **Minimal fix.** Smallest change that addresses the issue. Resist refactoring adjacent code.
3. **Atomic commit.**
   ```bash
   git add <files>
   git commit -m "fix(qa): <one-line description of issue> [ISSUE-NNN]"
   ```
4. **Re-test.** Reload via `preview_eval window.location.reload()`. Re-run the repro from the issue block.
5. **Classify the fix:**
   - **verified** — repro no longer reproduces, no regressions in adjacent surfaces
   - **best-effort** — appears fixed but couldn't fully verify (e.g., requires production data)
   - **reverted** — fix caused worse problem; backed out
   - **deferred** — recorded but not attempted this pass

6. **Before/after screenshots.** Embed both in the report.
7. **Regression test (optional).** If the bug has a clear codepath and you can write a Vitest / Playwright assertion in <2 minutes, do so. If not, defer with a description so a future test pass can capture it.

### WTF-likelihood self-regulation

Every 5 fixes (or after any revert), compute:

```
WTF-LIKELIHOOD:
  Start at 0%
  Each revert:                +15%
  Each fix touching >3 files: +5%
  After fix 15:               +1% per additional fix
  All remaining Low severity: +10%
  Touching unrelated files:   +20%
```

**If WTF > 20%: STOP immediately.** Show Aviran what you've done so far. Ask whether to continue. Hard cap: 50 fixes per QA pass.

The point is the same as `/investigate-metric`'s 3-strike rule: after a certain amount of unfocused work, the problem is usually framing, not effort.

---

## Phase 8: Final QA

After all fixes are applied:

1. Reload the dev server, re-run a quick pass on all affected tabs.
2. Compute final health score.
3. **If final < baseline, WARN PROMINENTLY in the report.** Investigate the regression before claiming done.
4. Reset `preview_resize` to default desktop size.

---

## Phase 9: Report

Save to `content/10-outputs/qa-reports/<YYYY-MM-DD>-<slug>.md` using the template in `templates/qa-report-template.md`.

Also append a one-line entry to `content/10-outputs/qa-reports/INDEX.md` (create if missing):
```
2026-05-24 — Codebase tab — H 78 → 91 — 7 fixes / 2 deferred
```

### PR Summary line (for `/ship`)

If this QA pass ran in preparation for a ship, output a one-line summary that `/ship` can paste into the PR body:
```
QA found N issues, fixed M (verified: X, best-effort: Y), health 78 → 91.
```

---

## When NOT to use this skill

- **For PRD review** — use `/prd-review-panel`
- **For pure code review** — use `/review-pr` or `/code-review`
- **For metric anomalies** — use `/investigate-metric`
- **For competitive dogfooding** — use `/qa --report-only` against the competitor URL

---

## Related Files

- `templates/qa-report-template.md` — the report skeleton
- `references/issue-taxonomy.md` — severity definitions + 7-category schema

---

Source: gstack `/qa` skill (`/Users/avirang/.claude/skills/gstack/qa/`) — report template, severity taxonomy, WTF-likelihood self-regulation, two-tier evidence model. Adapted from `$B` (gstack browse daemon) to `mcp__Claude_Preview__*` (Claude Code built-in preview tools) for Aviran's Product OS dashboard.
