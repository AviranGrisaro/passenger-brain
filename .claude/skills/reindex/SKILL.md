---
name: reindex
description: Refresh passenger-brain INDEX.md files against the actual filesystem. Use when indexes are stale, after adding several PRDs/projects/outputs, when the user says "reindex", "update the index", "refresh indexes", or monthly as hygiene. Also run after any bulk archive or folder move.
---

# Reindex — keep INDEX.md files honest

Indexes are the brain's retrieval layer. A stale index means future sessions grep blind. This skill diffs each INDEX.md against the filesystem and patches it.

## Indexes to check

| Index | Covers |
|---|---|
| `INDEX.md` (root) | Domain folders 01–17, 99 + counts of skills/agents |
| `prds/INDEX.md` | One row per PRD folder, nested under `<phase-slug>/` |
| `09-meetings/INDEX.md` | calendar/, prep/, summaries/ |
| `10-outputs/INDEX.md` | Subfolders + root-level generated docs |
| `13-projects/INDEX.md` | One row per project folder |
| `15-templates/INDEX.md` | Template files |
| `archive/INDEX.md` | One row per dated archive folder |

## Steps

1. For each index: `ls` the directory, parse existing entries, compute (a) on disk but not indexed, (b) indexed but gone from disk.
2. **Add** missing entries in the file's existing format. For a new PRD/project folder, peek at its primary .md to write a one-line purpose. Never guess content.
3. **Fix or flag** dead entries. If the target was archived, point the row at its `archive/` location; if truly gone, remove the row and note it in the run summary.
4. Do NOT rewrite healthy entries or change the file's structure/columns.
5. Update the header date line to `Updated YYYY-MM-DD`.
6. Root `INDEX.md` extras: verify skill count (`ls .claude/skills | wc -l`) and agent count, fix the "Skills / Sub-agents" rows, and confirm the CLAUDE.md link points at `../CLAUDE.md` (repo root).
7. Report: per index — added N, fixed M, removed K.
