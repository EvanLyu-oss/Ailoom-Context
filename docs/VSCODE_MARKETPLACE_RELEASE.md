# VS Code Marketplace Release Checklist

This checklist prepares the Ailoom Context VS Code extension for a public Marketplace upload.

## Current Extension

| Field | Value |
| --- | --- |
| Folder | `integrations/vscode/` |
| Package | `ailoom-context-vscode` |
| Display name | `Ailoom Context` |
| Version | `0.0.1` |
| Publisher placeholder | `ailoom` |
| Icon | `integrations/vscode/assets/ailoom-icon.png` |
| License file | `integrations/vscode/LICENSE` |
| Local boundary | Local CLI only, no telemetry, no upload |

## Preflight

```bash
cd integrations/vscode
npm run lint
npm run package
```

Expected:

- `node --check extension.js` exits with code `0`.
- `npx @vscode/vsce package --no-dependencies` creates one `.vsix`.
- No source bundles, restore packages, `.workspace_ail/`, or test artifacts are included.

## Publish Steps

1. Create or confirm a VS Code Marketplace publisher id.
2. If the publisher id is not `ailoom`, update `publisher` in `integrations/vscode/package.json`.
3. Create a Personal Access Token for Azure DevOps Marketplace publishing.
4. Run:

```bash
cd integrations/vscode
npx @vscode/vsce login <publisher-id>
npx @vscode/vsce publish
```

## Listing Copy

Short description:

```text
Local-first AI/IDE handoff for compact Ailoom skeletons, token savings, and restore safety checks.
```

Marketplace summary:

```text
Ailoom Context helps AI coding users hand off large workspaces without dumping the whole source tree into context. It creates a compact AI-facing skeleton, keeps exact restore files local, shows token savings, and provides install/safety diagnostics from VS Code.
```

## Safety Claims To Keep

- Local-first processing.
- No telemetry.
- No source upload.
- Restore package stays local.
- The extension calls the local Ailoom CLI and reads JSON output.

## Avoid

- Do not claim universal token savings.
- Do not imply hosted cloud sync.
- Do not publish restore package contents in screenshots.
- Do not publish under a publisher id that users may confuse with an unrelated owner.
