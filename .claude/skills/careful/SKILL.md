---
name: careful
description: |
  Safety guardrails for destructive commands. Warns before rm -rf, DROP TABLE,
  force-push, git reset --hard, and Aviran-specific patterns (rm in content/,
  edits under amp-backups/). User can override each warning. Use when touching
  prod, debugging live systems, or for any session that might destructively
  modify content/ or git history.
disable-model-invocation: false
user-invocable: true
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/bin/check-careful.sh"
          statusMessage: "Checking for destructive commands..."
---

# /careful — Destructive Command Guardrails

Safety mode is now **active**. Every Bash command will be checked for destructive
patterns before running. If a destructive command is detected, you'll be warned
and can choose to proceed or cancel.

## What's protected

| Pattern | Example | Risk |
|---------|---------|------|
| `rm -rf` / `rm -r` / `rm --recursive` | `rm -rf /var/data` | Recursive delete |
| **`rm` anywhere under `content/`** | `rm content/prds/foo.md` | **Aviran's never-rm-content rule** |
| **`rm` anywhere under `amp-backups/`** | `rm /Users/avirangrisaro/Documents/amp-backups/x.tar.gz` | Loses recoverable state |
| `DROP TABLE` / `DROP DATABASE` | `DROP TABLE users;` | Data loss |
| `TRUNCATE` | `TRUNCATE orders;` | Data loss |
| `git push --force` / `-f` | `git push -f origin main` | History rewrite |
| `git reset --hard` | `git reset --hard HEAD~3` | Uncommitted work loss |
| `git checkout .` / `git restore .` | `git checkout .` | Uncommitted work loss |
| `git branch -D` | `git branch -D feature-x` | Branch deletion |
| `kubectl delete` | `kubectl delete pod` | Production impact |
| `docker rm -f` / `docker system prune` | `docker system prune -a` | Container/image loss |

## Safe exceptions

These patterns are allowed without warning:
- `rm -rf node_modules` / `.next` / `dist` / `__pycache__` / `.cache` / `build` / `.turbo` / `coverage`
- `rm` on temp files (`.write_test`, `test_root.md`, `/tmp/*`)

## How it works

The hook (`bin/check-careful.sh`) reads the command from the PreToolUse JSON,
checks it against the patterns above, and returns `permissionDecision: "ask"`
with a warning message if a match is found. You can always override the warning
and proceed.

To deactivate, end the conversation or start a new one. Hooks are session-scoped.

## Aviran-specific notes

- The `content/` and `amp-backups/` patterns enforce the rules in
  `.claude/CLAUDE.md` "Backup & Destructive Operations Policy" mechanically,
  not just in prose.
- Before any prompted destructive op, the prose policy still applies: confirm a
  fresh backup exists, verify the target isn't a symlink, prefer `mv` to
  `content/archive/YYYY-MM-DD/` over `rm`.

Source: gstack `/careful` (`~/.claude/skills/gstack/careful/SKILL.md`), with
Aviran-specific patterns added for `content/` and `amp-backups/`.
