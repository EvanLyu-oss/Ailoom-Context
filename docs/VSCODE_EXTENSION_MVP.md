# VS Code Extension MVP Plan

This plan defines the smallest useful VS Code extension for Ailoom Context.

The extension should stay local-first: it calls the local Ailoom command or Python SDK and does not upload source code, skeletons, restore packages, or usage logs.

## Goal

Make Ailoom usable without terminal hopping.

The first version should answer:

- Can I create a handoff from the current workspace?
- Which skeleton file should I give to my AI/IDE workflow?
- How many tokens did I save?
- Is restore safety OK?
- What should I do next?

## MVP Commands

| Command | Behavior |
| --- | --- |
| `Ailoom: Handoff Current Workspace` | Runs `ailoom handoff --json` for the workspace root |
| `Ailoom: Show Savings` | Runs `ailoom savings --json` and shows a compact value panel |
| `Ailoom: Open Skeleton` | Opens `context_skeleton.mcp` from the latest handoff |
| `Ailoom: Open AI Handoff Prompt` | Opens `AI_HANDOFF.md` from the latest handoff |
| `Ailoom: Doctor` | Runs `ailoom doctor --install --json` and workspace `ailoom next --json` |
| `Ailoom: Clean Preview` | Runs `ailoom clean --dry-run --all --json` |

## UI Surface

Start with simple VS Code primitives:

- command palette commands
- output channel named `Ailoom Context`
- status bar item showing latest savings percent
- quick pick for next actions
- warning message when restore files should stay local

No custom webview is required for MVP.

## Data Source

Preferred integration path:

```python
from ailoom_core import handoff_project, get_savings, next_action
```

Fallback integration path:

```bash
ailoom handoff --json
ailoom savings --json
ailoom next --json
```

The extension should never parse human terminal output.

## First Flow

1. User opens a workspace.
2. User runs `Ailoom: Handoff Current Workspace`.
3. Extension calls local Ailoom.
4. Extension shows:
   - restore safety
   - skeleton path
   - AI handoff prompt path
   - savings percent
   - created vs reused
5. User clicks `Open Skeleton` or `Open AI Handoff Prompt`.

## MVP Success Criteria

- Works on a local workspace without network access.
- Fails clearly if `ailoom` is not installed.
- Points user to `sh install.sh --setup-shell` or `.\install.ps1 -SetupShell`.
- Opens the generated skeleton file.
- Shows token savings from `ailoom savings`.
- Clearly labels restore packages as keep-local.
- Does not copy restore package content into chat.

## Not In MVP

- SSO
- team dashboard
- SaaS sync
- marketplace billing
- JetBrains support
- custom parser for skeleton text
- direct integration with private IDE internals

## Later Extensions

After MVP validation:

- file explorer context menu
- auto-refresh on git changes
- workspace trust integration
- GitHub Action output viewer
- configurable model tokenizer profile
- side panel with recent handoff history
