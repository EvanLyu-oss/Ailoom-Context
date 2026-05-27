# MCP-Skeleton v1 Beta Trial Guide

This beta is for users who want to try lossless context compression on real projects before the formal v1.0 release.

The recommended beta path is macOS first. Windows has passed regression checks, but the main install experience is still macOS-focused.

## Who should try this beta

- You work with large codebases, long documents, or AI/IDE agents that run out of context.
- You want to give an AI a smaller project skeleton without losing exact restore ability.
- You are comfortable running a few terminal commands from a cloned or downloaded checkout.

## Install

From the repository root:

```bash
sh install.sh --setup-shell
```

Restart the terminal, or run the `export PATH=...` command printed by the installer.

Check the install:

```bash
mcp-skeleton version
mcp-skeleton doctor --install
```

If either command reports a PATH or Python issue, copy the fix command it prints.

## First trial

Run this inside a project you want to hand to an AI or IDE:

```bash
mcp-skeleton handoff
```

This creates a restore-safe bundle under `.workspace_ail/`.

Give this file to your AI/IDE:

```text
context_skeleton.mcp
```

Keep these local unless you intentionally want to share raw source bytes:

```text
context_manifest.json
context_restore_package.*
AI_HANDOFF.md
handoff.json
```

## Copy/open shortcut on macOS

```bash
mcp-skeleton handoff --copy --open
```

This copies the skeleton to the clipboard and opens the bundle folder.

## Day-to-day reuse

Run the same command again:

```bash
mcp-skeleton handoff
```

If the project has not changed, MCP-Skeleton reuses the previous fresh bundle instead of recompressing.

Force a fresh bundle when needed:

```bash
mcp-skeleton handoff --force-refresh
```

## Safety check

```bash
mcp-skeleton safety
```

The short version:

- Share `context_skeleton.mcp` with AI/IDE tools.
- Keep restore packages local by default.
- Start patch replay with dry-run before writing output.

## Performance check

The `handoff` output includes token savings, speed status, and the best next command.

For large projects where the first run feels slow:

```bash
mcp-skeleton quick --fast
```

For unchanged projects:

```bash
mcp-skeleton handoff --reuse-if-fresh
```

## What to report back

Please use [FEEDBACK_TEMPLATE.md](FEEDBACK_TEMPLATE.md).

The most useful feedback includes:

- OS and Python version
- project size or rough file count
- first handoff time
- reuse handoff time
- token savings shown by MCP-Skeleton
- whether the output made it clear which file to give to AI
- any confusing or failed command output

## Current beta readiness

The current beta has passed:

- macOS smoke and release readiness
- Windows smoke and release readiness regression
- dogfood exact restore of this repository
- quick benchmark release checks

This is still beta software. Use restore into a separate output directory when validating important data.
