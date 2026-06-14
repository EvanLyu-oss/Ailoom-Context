# Ailoom Context User Guide

This guide focuses on real workflows: AI coding handoff, large repository review, long manuscript context, and Patch replay.

## Five-Minute Loop

If you are using Ailoom Context with an AI coding agent for the first time, use this loop before reading the rest of the guide:

```bash
ailoom first-run
ailoom handoff --copy --open
ailoom next
ailoom savings
ailoom safety
```

The loop should answer five questions:

- Is the local install healthy?
- Which file should I give to AI?
- Which restore files should stay local?
- Did this project save meaningful tokens?
- What should I do next?

## AI Coding Handoff

Use this when you want an AI assistant or IDE agent to understand a project without pasting the whole source tree.

If you just installed Ailoom Context, run the guided first screen once:

```bash
ailoom first-run
```

Then follow its `First real project loop`: `handoff`, `next`, `savings`, `trial-report`, and `doctor --storage`.

```bash
ailoom handoff --copy --open
ailoom next
```

What to share:

- `context_skeleton.mcp`
- the recommended prompt in `AI_HANDOFF.md`

What to keep local:

- `context_manifest.json`
- `context_restore.json`
- the bundle directory

Check the latest savings:

```bash
ailoom savings
```

Read the `Value summary` first. It tells you whether the current project shows strong token value, useful token value, a watch-level result, or a tiny-project result where the skeleton may not look smaller yet. It also shows estimated AI/agent context-reading speedup, calculated from source tokens versus skeleton tokens.

If you lose track, run:

```bash
ailoom next
```

It reads the current project's recent handoff state and tells you whether to create the first handoff, share/review the fresh skeleton, refresh a stale bundle, check savings, or write a trial report.

## Large repository

Large repositories usually benefit most from `imports` or `tree` focus with adaptive density.

```bash
ailoom handoff
ailoom next
ailoom savings
ailoom recent
```

If the project has not changed, repeated handoffs reuse the latest fresh bundle automatically:

```bash
ailoom handoff
```

If the project changed and you want a new bundle:

```bash
ailoom handoff --force-refresh
```

## Long manuscript

Use writing mode when the source is prose, chapters, notes, or long-form drafts.

```bash
ailoom compress --text-file manuscript.md --preset writing --focus-mode writing-outline --skeleton-density adaptive --json
```

The skeleton keeps headings, chapter folds, section flow, and topic vocabulary visible while the restore package keeps the original text exact.

## Patch Replay

Use patch replay when you want controlled updates instead of direct source overwrites.

```bash
ailoom patch --package-file bundle/context_manifest.json --input-dir edited --output-dir patch-bundle --json
ailoom patch-apply --patch-file patch-bundle/context_manifest.json --dry-run --write-dry-run-report dry-run.json --json
```

Review the dry-run report first. Then apply into a safe output directory, not directly over the original source.

## Safety Boundary

Ailoom Context is designed around a simple boundary:

- Share skeletons with AI.
- Keep restore packages local.
- Run dry-run before patch replay.
- Use `ailoom clean --dry-run` before deleting generated artifacts.

For long development sessions or beta testing, check generated storage first:

```bash
ailoom doctor --storage
```

Read the `Cleanup safety` section before running the suggested clean command. The clean path only targets known generated Ailoom Context artifact roots.

For a machine-readable check, run:

```bash
ailoom safety --json
```
