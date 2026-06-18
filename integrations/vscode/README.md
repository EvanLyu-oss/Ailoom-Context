# Ailoom Context VS Code MVP

This is a local-first VS Code extension skeleton for Ailoom Context.

It is intentionally minimal and not yet published to the Marketplace. The MVP validates the user flow before adding custom UI or billing surfaces.

## Commands

- `Ailoom: Handoff Current Workspace`
- `Ailoom: Show Savings`
- `Ailoom: Open Skeleton`
- `Ailoom: Open AI Handoff Prompt`
- `Ailoom: Doctor`
- `Ailoom: Clean Preview`

## Local-Only Boundary

The extension calls the local `ailoom` command with `--json`. It does not upload source code, skeletons, restore packages, logs, or usage records.

## Development

1. Install Ailoom Context locally.
2. Open this folder in VS Code.
3. Press `F5` to launch an Extension Development Host.
4. Open a project folder in the development host.
5. Run `Ailoom: Handoff Current Workspace`.

## Configuration

Set `ailoom.commandPath` if `ailoom` is not on PATH:

```json
{
  "ailoom.commandPath": "/absolute/path/to/ailoom"
}
```

## MVP Success Criteria

- Create or reuse a handoff for the current workspace.
- Show restore safety.
- Show skeleton and `AI_HANDOFF.md` paths.
- Show token savings.
- Open the skeleton and prompt files.
- Preview cleanup without deleting anything.
