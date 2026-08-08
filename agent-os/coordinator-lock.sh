#!/bin/bash
# coordinator-lock.sh — a real mutex for board-wide coordinator passes.
#
# WHY THIS EXISTS
# The claim protocol (L-039 -> L-049 -> L-052) tried to build a mutex out of a
# markdown file. It cannot work: two sessions both append a PASS line to
# BOARD.md, git accepts both (same working tree, sequential commits, no
# conflict), and the "whose commit landed first" tiebreak only helps if both
# racers remember to re-read. Check-then-act on a text file has no atomic step
# anywhere in it. Three collisions in 20 hours on 2026-08-07/08 proved it.
#
# `mkdir` is atomic on POSIX: given N concurrent callers, exactly one succeeds
# and the rest get EEXIST. That is the primitive the protocol never had.
#
# The BOARD.md PASS line stays — it is the human-readable narrative of what a
# pass is doing, and agents read BOARD.md. This is the lock. They are different
# jobs and both are worth having.
#
# USAGE (run from the workspace root, ~/APE Studio/passenger/)
#   passenger-brain/agent-os/coordinator-lock.sh acquire <role> <ttl-min> "<trigger>"
#   passenger-brain/agent-os/coordinator-lock.sh heartbeat <token> <ttl-min>
#   passenger-brain/agent-os/coordinator-lock.sh release <token>
#   passenger-brain/agent-os/coordinator-lock.sh status
#
# EXIT CODES
#   0  acquired / released / heartbeat ok / status printed
#   1  STAND DOWN — another coordinator holds a live lock
#   2  usage or environment error
#
# Roles that must take this lock: chief, project-manager, retrospective.

set -uo pipefail

LOCK_ROOT="${COORDINATOR_LOCK_ROOT:-$HOME/APE Studio/passenger/.claude/locks}"
LOCK_DIR="$LOCK_ROOT/coordinator"
REAPED_DIR="$LOCK_ROOT/reaped"
META="$LOCK_DIR/meta"

now_epoch() { date +%s; }
human()     { date -r "$1" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || date "+%Y-%m-%d %H:%M:%S"; }

read_meta_field() {
  # $1 = field name; prints value or empty
  [ -f "$META" ] || return 0
  grep -m1 "^$1=" "$META" 2>/dev/null | cut -d= -f2-
}

# Move a dead lock aside rather than deleting it — standing rule is never rm a
# record, and the reaped/ trail is how we find out how often holders leak.
reap_stale() {
  local expires holder
  expires="$(read_meta_field expires_at)"
  holder="$(read_meta_field role)"
  [ -n "$expires" ] || return 1
  [ "$(now_epoch)" -gt "$expires" ] 2>/dev/null || return 1
  mkdir -p "$REAPED_DIR"
  mv "$LOCK_DIR" "$REAPED_DIR/$(date +%Y%m%dT%H%M%S)-${holder:-unknown}" 2>/dev/null || return 1
  echo "REAPED a dead ${holder:-unknown} lock (expired $(human "$expires"))." >&2
  return 0
}

report_holder() {
  echo "STAND DOWN — another coordinator pass is live."
  echo "  role:       $(read_meta_field role)"
  echo "  started:    $(human "$(read_meta_field started_at)")"
  echo "  expires:    $(human "$(read_meta_field expires_at)")"
  echo "  trigger:    $(read_meta_field trigger)"
  echo
  echo "Do NOT run a second board-wide pass. Read that pass's BOARD.md PASS line,"
  echo "report to whoever asked that a pass is already in flight, and stop."
}

cmd_acquire() {
  local role="${1:-}" ttl="${2:-120}" trigger="${3:-unspecified}"
  if [ -z "$role" ]; then echo "usage: acquire <role> <ttl-min> \"<trigger>\"" >&2; exit 2; fi
  case "$role" in
    chief|project-manager|retrospective) ;;
    *) echo "refusing: '$role' is not a coordinator role (chief|project-manager|retrospective)" >&2; exit 2 ;;
  esac

  mkdir -p "$LOCK_ROOT"

  local attempt
  for attempt in 1 2; do
    if mkdir "$LOCK_DIR" 2>/dev/null; then
      local token started expires
      token="$(uuidgen 2>/dev/null || echo "$$-$(now_epoch)-$RANDOM")"
      started="$(now_epoch)"
      expires=$(( started + ttl * 60 ))
      {
        echo "role=$role"
        echo "token=$token"
        echo "started_at=$started"
        echo "expires_at=$expires"
        echo "trigger=$trigger"
      } > "$META"
      echo "ACQUIRED"
      echo "TOKEN=$token"
      echo "Expires $(human "$expires") (${ttl}m). Re-stamp with:"
      echo "  passenger-brain/agent-os/coordinator-lock.sh heartbeat $token <ttl-min>"
      return 0
    fi

    # Lost the race, or a dead holder is squatting. Reap only if genuinely expired.
    if [ "$attempt" -eq 1 ] && reap_stale; then
      continue
    fi

    report_holder
    return 1
  done
}

cmd_heartbeat() {
  local token="${1:-}" ttl="${2:-120}"
  [ -n "$token" ] || { echo "usage: heartbeat <token> <ttl-min>" >&2; exit 2; }
  [ -f "$META" ] || { echo "no lock held — nothing to heartbeat" >&2; exit 2; }
  if [ "$(read_meta_field token)" != "$token" ]; then
    echo "refusing: that token does not own this lock (held by $(read_meta_field role))" >&2
    exit 2
  fi
  local expires
  expires=$(( $(now_epoch) + ttl * 60 ))
  # Rewrite in place, preserving every other field.
  sed -i '' "s/^expires_at=.*/expires_at=$expires/" "$META" 2>/dev/null \
    || sed -i "s/^expires_at=.*/expires_at=$expires/" "$META"
  echo "HEARTBEAT ok — now expires $(human "$expires")"
}

cmd_release() {
  local token="${1:-}"
  [ -n "$token" ] || { echo "usage: release <token>" >&2; exit 2; }
  [ -f "$META" ] || { echo "no lock held — nothing to release"; return 0; }
  if [ "$(read_meta_field token)" != "$token" ]; then
    echo "refusing: that token does not own this lock (held by $(read_meta_field role))" >&2
    exit 2
  fi
  mkdir -p "$REAPED_DIR"
  mv "$LOCK_DIR" "$REAPED_DIR/$(date +%Y%m%dT%H%M%S)-$(read_meta_field role)-released"
  echo "RELEASED"
}

cmd_status() {
  if [ ! -f "$META" ]; then echo "FREE — no coordinator pass in flight."; return 0; fi
  local expires
  expires="$(read_meta_field expires_at)"
  if [ "$(now_epoch)" -gt "$expires" ] 2>/dev/null; then
    echo "STALE — $(read_meta_field role) lock expired $(human "$expires"); next acquire will reap it."
  else
    echo "HELD by $(read_meta_field role), expires $(human "$expires")"
    echo "trigger: $(read_meta_field trigger)"
  fi
}

case "${1:-}" in
  acquire)   shift; cmd_acquire   "$@" ;;
  heartbeat) shift; cmd_heartbeat "$@" ;;
  release)   shift; cmd_release   "$@" ;;
  status)    shift; cmd_status    "$@" ;;
  *) echo "usage: $0 {acquire|heartbeat|release|status} ..." >&2; exit 2 ;;
esac
