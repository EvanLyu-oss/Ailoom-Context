# Good First Trial

Use this when you want to try Ailoom Context on a real project without reading the full docs.

## What You Are Testing

Ailoom Context turns a large repository or long document into a compact AI-facing skeleton while keeping exact restore files local.

You should finish this trial knowing:

- Which file to give to an AI or IDE agent.
- Which restore files must stay local.
- Whether the project shows meaningful token savings.
- Whether repeated handoff feels faster when the project has not changed.

## 1. Install

From a cloned or downloaded checkout:

```bash
sh install.sh --setup-shell
```

Restart the terminal if needed, then run:

```bash
ailoom doctor --install
```

Expected result:

- The command explains Python and PATH readiness.
- If PATH is not ready, it prints a copy/paste fix.

## 2. Run The Safe Demo

```bash
ailoom demo
```

Expected result:

- `Restore safety: OK`
- Source tokens and skeleton tokens are visible.
- Inspect and restore commands are printed.

## 3. Try A Real Project

Run this inside a project you already use with AI coding tools:

```bash
ailoom handoff --copy --open
```

Expected result:

- `context_skeleton.mcp` is the file to share with AI or your IDE agent.
- `AI_HANDOFF.md` contains the recommended prompt.
- `context_manifest.json` and restore packages are clearly marked as keep-local.

## 4. Ask What To Do Next

```bash
ailoom next
```

Expected result:

- If no handoff exists, it tells you to create one.
- If the handoff is fresh, it tells you to share or review the skeleton.
- If the project changed, it tells you to refresh before sharing.

## 5. Check The Value

```bash
ailoom savings
```

Look for:

- Source tokens.
- Skeleton tokens.
- Estimated tokens saved.
- Estimated savings percent.
- Estimated AI/agent context-reading speedup.

## 6. Verify Restore Safety

Use the restore command printed by `handoff` or `quick`, and restore into a temporary output directory.

Expected result:

- Restore status is `ok`.
- No missing files.
- No mismatched files.
- The original source directory is not overwritten.

## 7. Send Feedback

If you are helping test the beta:

```bash
ailoom trial-report --write-report ailoom-trial-report.md
```

Send the report plus anything confusing to:

```text
carwyn910@gmail.com
```

Please include:

- OS and Python version.
- Project type and rough size.
- First handoff time.
- Reuse handoff time.
- Token savings shown by Ailoom Context.
- Whether the AI/IDE understood the skeleton well enough to help.
