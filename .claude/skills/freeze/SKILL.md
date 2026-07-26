---
name: freeze
description: |
  Restrict file edits to a specific directory for the session. Blocks Edit and
  Write outside the allowed path. Use when working on a single PRD, a single
  component, or any focused task where you don't want collateral edits to
  unrelated code. Trigger with "freeze edits", "lock scope to X", "restrict
  changes to this folder".
disable-model-invocation: false
user-invocable: true
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
---

# /freeze — Restrict Edits to a Directory

Lock file edits to a specific directory. Any Edit or Write targeting a file
outside the allowed path will be **blocked** (not just warned).

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
> "Edits are now restricted to `<path>/`. Any Edit or Write outside this
> directory will be blocked. To change the boundary, run `/freeze` again. To
> remove it, run `/unfreeze`."

## How it works

The hook (`bin/check-freeze.sh`) reads `file_path` from the Edit/Write tool
input, then checks whether the path starts with the freeze directory. If not,
it returns `permissionDecision: "deny"` to block the operation.

The freeze boundary persists for the session via the state file at
`$HOME/.claude/state/passenger-safety/freeze-dir.txt`. The hook script reads it on
every Edit/Write invocation.

## Useful invocations for Product OS

- **Focused PRD work:** `/freeze content/prds/<feature-slug>/`
- **Single component:** `/freeze product-os-server/src/components/<tab>/`
- **Server-only change:** `/freeze product-os-server/server/`
- **Skill-only edit:** `/freeze .claude/skills/<skill-name>/`

## Notes

- The trailing `/` on the freeze directory prevents `/src` from matching `/src-old`
- Freeze applies to Edit and Write only — Read, Bash, Glob, Grep are unaffected
- This prevents accidental edits, not a security boundary — Bash commands like
  `sed -i` can still modify files outside the boundary. Combine with `/careful`
  via `/guard` for both rails.
- To deactivate: `/unfreeze` or end the conversation

Source: gstack `/freeze` (`~/.claude/skills/gstack/freeze/SKILL.md`), simplified
to remove the gstack-paths dependency. State file lives in
`$HOME/.claude/state/passenger-safety/`.
