# QA Report: {APP_NAME}

| Field | Value |
|-------|-------|
| **Date** | {DATE} |
| **URL** | {URL} |
| **Branch** | {BRANCH} |
| **Commit** | {COMMIT_SHA} ({COMMIT_DATE}) |
| **PR** | {PR_NUMBER} ({PR_URL}) or "—" |
| **Tier** | Quick / Standard / Exhaustive |
| **Scope** | {SCOPE or "Full dashboard"} |
| **Duration** | {DURATION} |
| **Tabs visited** | {COUNT} |
| **Screenshots** | {COUNT} |
| **Index** | [All QA runs](./INDEX.md) |

## Health Score: {SCORE}/100

| Category | Score |
|----------|-------|
| Console | {0-100} |
| Functional | {0-100} |
| Visual | {0-100} |
| UX | {0-100} |
| Performance | {0-100} |
| Accessibility | {0-100} |

## Top 3 Things to Fix

1. **{ISSUE-NNN}: {title}** — {one-line description}
2. **{ISSUE-NNN}: {title}** — {one-line description}
3. **{ISSUE-NNN}: {title}** — {one-line description}

## Console Health

| Error | Count | First seen |
|-------|-------|------------|
| {error message} | {N} | {URL or tab} |

## Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| **Total** | **0** |

---

## Issues

### ISSUE-001: {Short title}

| Field | Value |
|-------|-------|
| **Severity** | critical / high / medium / low |
| **Category** | visual / functional / ux / content / performance / console / accessibility |
| **Surface** | {tab or page} |
| **URL** | {page URL} |

**Description:** {What is wrong, expected vs actual.}

**Repro Steps:**

1. Navigate to {tab/URL}
   ![Step 1](screenshots/issue-001-step-1.png)
2. {Action}
   ![Step 2](screenshots/issue-001-step-2.png)
3. **Observe:** {what goes wrong}
   ![Result](screenshots/issue-001-result.png)

**Notes:** {anything unusual — flake potential, only-on-mobile, console error correlated, etc.}

---

## Fixes Applied (if applicable)

| Issue | Fix Status | Commit | Files Changed |
|-------|-----------|--------|---------------|
| ISSUE-NNN | verified / best-effort / reverted / deferred | {SHA} | {files} |

### Before/After Evidence

#### ISSUE-NNN: {title}

**Before:** ![Before](screenshots/issue-NNN-before.png)
**After:** ![After](screenshots/issue-NNN-after.png)

---

## Regression Tests

| Issue | Test File | Status | Description |
|-------|-----------|--------|-------------|
| ISSUE-NNN | path/to/test | committed / deferred / skipped | description |

### Deferred Tests

#### ISSUE-NNN: {title}

**Precondition:** {state that triggers the bug}
**Action:** {what the user does}
**Expected:** {correct behavior}
**Why deferred:** {reason — usually "couldn't write a stable test in <2min"}

---

## Ship Readiness

| Metric | Value |
|--------|-------|
| Health score | {before} → {after} ({delta}) |
| Issues found | N |
| Fixes applied | N (verified: X, best-effort: Y, reverted: Z) |
| Deferred | N |
| WTF-likelihood at end | X% |

**PR Summary line:** "QA found N issues, fixed M (verified: X), health {before} → {after}."

---

## Regression (if --regression baseline provided)

| Metric | Baseline | Current | Delta |
|--------|----------|---------|-------|
| Health score | {N} | {N} | {+/-N} |
| Issues | {N} | {N} | {+/-N} |

**Fixed since baseline:** {list of ISSUE-NNN that are gone}
**New since baseline:** {list of ISSUE-NNN that appeared}

---

## Notes

{Anything that affected the run — server restarts, flaky tests, environmental issues, mid-run scope changes.}
