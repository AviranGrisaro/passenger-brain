#!/usr/bin/env bash
# check-careful.sh — PreToolUse hook for /careful skill (Aviran's adaptation)
# Reads JSON from stdin, checks Bash command for destructive patterns.
# Returns {"permissionDecision":"ask","message":"..."} to warn, or {} to allow.
set -euo pipefail

# Read stdin (JSON with tool_input)
INPUT=$(cat)

# Extract the "command" field value from tool_input
CMD=$(printf '%s' "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*:[[:space:]]*"//;s/"$//' || true)

# Python fallback if grep returned empty (escaped quotes in command)
if [ -z "$CMD" ]; then
  CMD=$(printf '%s' "$INPUT" | python3 -c 'import sys,json; print(json.loads(sys.stdin.read()).get("tool_input",{}).get("command",""))' 2>/dev/null || true)
fi

# If we still couldn't extract a command, allow
if [ -z "$CMD" ]; then
  echo '{}'
  exit 0
fi

# Normalize: lowercase for case-insensitive SQL matching
CMD_LOWER=$(printf '%s' "$CMD" | tr '[:upper:]' '[:lower:]')

# --- Safe exceptions for `rm -rf` of build artifacts ---
if printf '%s' "$CMD" | grep -qE 'rm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+|--recursive\s+)' 2>/dev/null; then
  SAFE_ONLY=true
  RM_ARGS=$(printf '%s' "$CMD" | sed -E 's/.*rm[[:space:]]+(-[a-zA-Z]+[[:space:]]+)*//;s/--recursive[[:space:]]*//')
  for target in $RM_ARGS; do
    case "$target" in
      */node_modules|node_modules|*/\.next|\.next|*/dist|dist|*/__pycache__|__pycache__|*/\.cache|\.cache|*/build|build|*/\.turbo|\.turbo|*/coverage|coverage)
        ;; # safe target
      /tmp/*|/var/folders/*)
        ;; # temp file
      -*)
        ;; # flag, skip
      *)
        SAFE_ONLY=false
        break
        ;;
    esac
  done
  if [ "$SAFE_ONLY" = true ]; then
    echo '{}'
    exit 0
  fi
fi

# --- Destructive pattern checks ---
WARN=""

# Aviran-specific: rm anywhere under content/
if printf '%s' "$CMD" | grep -qE '\brm\s+([^&|;]*\s)?([^&|;]*/)?content/' 2>/dev/null; then
  WARN="[careful] DANGEROUS: rm targeting content/. This is gitignored personal work (PRDs, research, strategy). Per CLAUDE.md: never rm in content/ — use mv to content/99-archive/YYYY-MM-DD/ instead."
fi

# Aviran-specific: rm anywhere under amp-backups/
if [ -z "$WARN" ] && printf '%s' "$CMD" | grep -qE '\brm\s+([^&|;]*\s)?([^&|;]*/)?amp-backups/' 2>/dev/null; then
  WARN="[careful] DANGEROUS: rm targeting amp-backups/. This is the recovery layer for content/. Removing backups defeats the per-turn backup rule."
fi

# rm -rf / rm -r / rm --recursive
if [ -z "$WARN" ] && printf '%s' "$CMD" | grep -qE 'rm\s+(-[a-zA-Z]*r|--recursive)' 2>/dev/null; then
  WARN="[careful] Destructive: recursive delete (rm -r). This permanently removes files."
fi

# DROP TABLE / DROP DATABASE
if [ -z "$WARN" ] && printf '%s' "$CMD_LOWER" | grep -qE 'drop\s+(table|database)' 2>/dev/null; then
  WARN="[careful] Destructive: SQL DROP detected. This permanently deletes database objects."
fi

# TRUNCATE
if [ -z "$WARN" ] && printf '%s' "$CMD_LOWER" | grep -qE '\btruncate\b' 2>/dev/null; then
  WARN="[careful] Destructive: SQL TRUNCATE detected. This deletes all rows from a table."
fi

# git push --force / git push -f / git push --force-with-lease
if [ -z "$WARN" ] && printf '%s' "$CMD" | grep -qE 'git\s+push\s+.*(-f\b|--force(-with-lease)?)' 2>/dev/null; then
  WARN="[careful] Destructive: git force-push rewrites remote history. Product OS has external contributors — this can destroy their work."
fi

# git reset --hard
if [ -z "$WARN" ] && printf '%s' "$CMD" | grep -qE 'git\s+reset\s+--hard' 2>/dev/null; then
  WARN="[careful] Destructive: git reset --hard discards all uncommitted changes."
fi

# git checkout . / git restore .
if [ -z "$WARN" ] && printf '%s' "$CMD" | grep -qE 'git\s+(checkout|restore)\s+\.' 2>/dev/null; then
  WARN="[careful] Destructive: discards all uncommitted changes in the working tree."
fi

# git branch -D
if [ -z "$WARN" ] && printf '%s' "$CMD" | grep -qE 'git\s+branch\s+-D' 2>/dev/null; then
  WARN="[careful] Destructive: git branch -D force-deletes a branch even if unmerged. Use -d for safe delete."
fi

# kubectl delete
if [ -z "$WARN" ] && printf '%s' "$CMD" | grep -qE 'kubectl\s+delete' 2>/dev/null; then
  WARN="[careful] Destructive: kubectl delete removes Kubernetes resources. May impact production."
fi

# docker rm -f / docker system prune
if [ -z "$WARN" ] && printf '%s' "$CMD" | grep -qE 'docker\s+(rm\s+-f|system\s+prune)' 2>/dev/null; then
  WARN="[careful] Destructive: Docker force-remove or prune. May delete running containers or cached images."
fi

# --- Output ---
if [ -n "$WARN" ]; then
  WARN_ESCAPED=$(printf '%s' "$WARN" | sed 's/\\/\\\\/g;s/"/\\"/g')
  printf '{"permissionDecision":"ask","message":"%s"}\n' "$WARN_ESCAPED"
else
  echo '{}'
fi
