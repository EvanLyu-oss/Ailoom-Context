# Ailoom Context User Guide

This guide focuses on real workflows: AI coding handoff, large repository review, long manuscript context, and Patch replay.

## AI Coding Handoff

Use this when you want an AI assistant or IDE agent to understand a project without pasting the whole source tree.

If you just installed Ailoom Context, run the guided first screen once:

```bash
ailoom first-run
```

Then follow its `First real project loop`: `handoff`, `savings`, `trial-report`, and `doctor --storage`.

```bash
ailoom handoff --copy --open
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

Read the `Value summary` first. It tells you whether the current project shows strong token value, useful token value, a watch-level result, or a tiny-project result where the skeleton may not look smaller yet.

## Large repository

Large repositories usually benefit most from `imports` or `tree` focus with adaptive density.

```bash
ailoom handoff
ailoom savings
ailoom recent
```

If the project has not changed, repeated handoffs can reuse the latest fresh bundle:

```bash
ailoom handoff --reuse-if-fresh
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

For a machine-readable check, run:

```bash
ailoom safety --json
```
