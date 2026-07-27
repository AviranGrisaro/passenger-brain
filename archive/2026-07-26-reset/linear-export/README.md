# Linear export — locali-app workspace

Snapshot taken 2026-07-26, immediately before the Linear connection was re-pointed at the new `passenger` workspace.

| File | What |
|---|---|
| [issues.md](issues.md) | All 110 `LOC-*` issues — index table plus every full description |
| [projects.md](projects.md) | All 22 projects, with why each one is dead, parked, or still live |

## Why this exists

Linear scopes an OAuth grant to one workspace. Reading both `locali-app` and `passenger` live would mean maintaining two connections, and the old workspace is history that will never change again. A flat snapshot is simpler, greppable offline, and can't silently break when a token expires.

The live `locali-app` workspace was **not** deleted — every URL here still resolves, and the workspace remains readable in the Linear UI. This is a convenience copy, not the only one.

## Reading it

```bash
grep -n "LOC-104" issues.md
```

```bash
grep -in "aviran-blocker" issues.md
```

## Do not

- Renumber `LOC-*` to `PAS-*` anywhere. They're different workspaces; a `PAS-104` does not exist and never will.
- Treat an issue here as live work. Nothing in this file is actionable — `PAS` is where work lives now.
- Cite these as current requirements. Ten of the old PRDs specified features the strategy forbids; the issues implementing them are still in this export and still read as legitimate.
