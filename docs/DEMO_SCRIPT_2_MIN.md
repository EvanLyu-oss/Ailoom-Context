# Two-Minute Demo Script

Use this script for a short screen recording or social post demo.

## Goal

Show that Ailoom Context can:

- install locally
- create an AI-facing skeleton
- keep restore files local
- show token savings
- verify restore safety
- clean generated artifacts

## Setup

Use a medium or large local project where token savings are visible.

Do not record private source code, `.env` files, restore package contents, or customer data.

## Script

### 0:00 - 0:15 Opening

Say:

```text
This is Ailoom Context, a local-first context compression tool for AI coding agents.
It turns a large project into a compact AI-facing skeleton while keeping exact restore files local.
```

Show:

```bash
ailoom version
```

### 0:15 - 0:35 Create Handoff

Run:

```bash
ailoom handoff --copy --open
```

Point out:

- `Restore safety: OK`
- `context_skeleton.mcp`
- `AI_HANDOFF.md`
- keep-local restore package guidance

### 0:35 - 0:55 Show Savings

Run:

```bash
ailoom savings
```

Point out:

- source tokens
- skeleton tokens
- tokens saved
- savings percent
- agent context-reading estimate

Suggested line:

```text
This is the part that matters for daily AI coding: the agent reads a smaller skeleton instead of rereading the whole project.
```

### 0:55 - 1:15 Show Next Action

Run:

```bash
ailoom next
```

Point out:

- whether the bundle is fresh
- whether to share, refresh, or report
- next copy/paste command

### 1:15 - 1:35 Show Restore Boundary

Run:

```bash
ailoom safety
```

Point out:

- local-only processing
- no telemetry
- skeleton is AI-facing
- restore files stay local

### 1:35 - 1:50 Show Cleanup

Run:

```bash
ailoom doctor --storage
ailoom clean --dry-run --all
```

Point out:

- generated artifact size is visible
- cleanup previews before deletion
- source tree is protected

### 1:50 - 2:00 Close

Say:

```text
If you use AI coding agents on large projects, Ailoom Context is designed to reduce context pressure without giving up local exact restore.
```

Show:

```text
https://github.com/EvanLyu-oss/Ailoom-Context
Evan <carwyn910@gmail.com>
```

## Screenshot Checklist

- `ailoom handoff` At a glance panel
- `Value summary`
- `ailoom savings`
- `ailoom next`
- `ailoom safety`
- `ailoom clean --dry-run --all`

## Wording Rules

Use:

- "observed"
- "local-first"
- "AI-facing skeleton"
- "keep restore files local"
- "byte-exact restore"

Avoid:

- "guaranteed 10x"
- "always saves 99%"
- "send your whole project to AI"
- "secure by magic"
