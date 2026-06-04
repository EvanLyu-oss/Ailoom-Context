# Install in 30 seconds

Ailoom Context is a local command-line tool. It does not upload source code, text, bundles, or usage logs.

## macOS

From a cloned or downloaded checkout:

```bash
sh install.sh --setup-shell
ailoom first-run
ailoom handoff
```

If the current terminal cannot find `ailoom` yet, restart the terminal or run the temporary PATH command printed by the installer.

## Windows PowerShell

From a cloned or downloaded checkout:

```powershell
.\install.ps1 -SetupShell
ailoom first-run
ailoom handoff
```

If PowerShell cannot find `ailoom` yet, restart PowerShell or run the temporary PATH command printed by the installer.

## First Useful Commands

| Command | What it proves |
| --- | --- |
| `ailoom first-run` | Checks install readiness, runs a safe demo, shows savings, and prints the next command |
| `ailoom demo` | Runs a safe sample and shows token savings plus restore safety |
| `ailoom handoff` | Creates a restore-safe AI/IDE handoff for the current project |
| `ailoom savings` | Shows the token savings from the most recent handoff |
| `ailoom recent` | Finds the latest bundle, skeleton, manifest, and restore command |
| `ailoom doctor --install` | Checks Python, PATH, and install-readiness status |

## What Success Looks Like

After `ailoom handoff`, look for:

- `Restore safety: OK`
- `Token savings: ...`
- `Give AI this file: .../context_skeleton.mcp`
- `Keep for restore: .../context_manifest.json`

Share the skeleton with AI or your IDE. Keep restore packages local unless you intentionally want to share raw source bytes.
