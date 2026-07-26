---
name: guard
description: |
  Full safety mode — destructive command warnings + directory-scoped edits.
  Combines /careful (warns before rm -rf, DROP TABLE, force-push, rm in content/,
  etc.) with /freeze (blocks edits outside a specified directory). Use when
  touching production-adjacent code, debugging tricky state, or any session
  where collateral damage is high cost.
disable-model-invocation: false
user-invocable: true
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/../careful/bin/check-careful.sh"
          statusMessage: "Checking for destructive commands..."
    - matcher: "Edit"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/../freeze/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/../freeze/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
---

# /guard — Full Safety Mode

Activates both destructive command warnings (`/careful`) and directory-scoped
edit restrictions (`/freeze`).

**Dependency note:** This skill references hook scripts from the sibling
`/careful` and `/freeze` skill directories. All three must be installed (they
were installed together as the safety quartet).

## Setup

Ask the user which directory to restrict edits to. Use AskUserQuestion with a
text input — the user types a path (relative or absolute).

Once you have the path:

1. Resolve to absolute path:
   ```bash
   FREEZE_DIR=$(cd "<user-provided-path>" 2>/dev/null && pwd)
   echo "$FREEZE_DIR"
   ```

2. Ensure trailing slash and save to the freeze state file:
   ```bash
   FREEZE_DIR="${FREEZE_DIR%/}/"
   STATE_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/state/passenger-safety}"
   mkdir -p "$STATE_DIR"
   echo "$FREEZE_DIR" > "$STATE_DIR/freeze-dir.txt"
   echo "Freeze boundary set: $FREEZE_DIR"
   ```

Tell the user:
- **"Guard mode active.** Two protections are now running:"
- **1. Destructive command warnings** — rm -rf, rm in `content/`, DROP TABLE,
  force-push, git reset --hard, kubectl delete, etc. will warn before executing
  (you can override).
- **2. Edit boundary** — file edits restricted to `<path>/`. Edits outside this
  directory are blocked (not warned, denied).
- To remove the edit boundary: `/unfreeze`. To deactivate everything: end the
  session.

## What's protected

See `/careful` for the full list of destructive command patterns and safe
exceptions, including Aviran-specific rules (`rm content/`, `rm amp-backups/`).

See `/freeze` for how the edit-boundary enforcement works.

Source: gstack `/guard` (`~/.claude/skills/gstack/guard/SKILL.md`), simplified
to use the local `careful` + `freeze` hook scripts.
