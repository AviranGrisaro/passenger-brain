---
name: unfreeze
description: |
  Clear the freeze boundary set by /freeze, allowing edits to all directories
  again. Use when you want to widen edit scope without ending the session.
  Trigger with "unfreeze edits", "unlock all directories", "remove freeze",
  "allow all edits".
disable-model-invocation: false
user-invocable: true
---

# /unfreeze — Clear Freeze Boundary

Remove the edit restriction set by `/freeze`, allowing edits to all directories.

## Clear the boundary

```bash
STATE_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/state/passenger-safety}"
if [ -f "$STATE_DIR/freeze-dir.txt" ]; then
  PREV=$(cat "$STATE_DIR/freeze-dir.txt")
  rm -f "$STATE_DIR/freeze-dir.txt"
  echo "Freeze boundary cleared (was: $PREV). Edits are now allowed everywhere."
else
  echo "No freeze boundary was set."
fi
```

Tell the user the result. Note that `/freeze` hooks remain registered for the
session — they will just allow everything since no state file exists. To
re-freeze, run `/freeze` again.

Source: gstack `/unfreeze` (`~/.claude/skills/gstack/unfreeze/SKILL.md`),
simplified to use the local `.claude/state/passenger-safety/` directory.
