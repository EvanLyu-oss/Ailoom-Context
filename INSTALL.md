# Install in 30 seconds

Ailoom Context is a local command-line tool. It does not upload source code, text, bundles, or usage logs.

## Confirm You Have The Current Beta

Before reporting install or Windows compatibility issues, confirm the checkout or ZIP is the current beta:

```bash
ailoom version --json
```

Expected beta identity:

- `version`: `1.0.0b1`
- `release_channel`: `v1-beta`
- `expected_beta_tag`: `v1.0.0-beta.1`
- `repo_url`: `https://github.com/EvanLyu-oss/Ailoom-Context`
- `version_check`: `ok`

If `version` still shows `0.1.0` or `version_check` is `watch`, refresh the checkout or download the current beta ZIP from the `latest_beta_zip_url` printed by `ailoom version --json`, then reinstall.

## macOS

From a cloned or downloaded checkout:

```bash
sh install.sh --setup-shell
ailoom
ailoom first-run
ailoom handoff --copy --open
```

If the current terminal cannot find `ailoom` yet, restart the terminal or run the temporary PATH command printed by the installer.
If you are unsure what to run next, type `ailoom` with no arguments. It prints a welcome panel with the first safe demo, daily handoff, install check, storage cleanup, and local-only safety commands.

## Windows PowerShell

From a cloned or downloaded checkout:

```powershell
.\install.ps1 -SetupShell
ailoom
ailoom first-run
ailoom handoff --copy --open
```

If PowerShell cannot find `ailoom` yet, restart PowerShell or run the temporary PATH command printed by the installer.

## First Useful Commands

| Command | What it proves |
| --- | --- |
| `ailoom` | Shows the zero-learning welcome panel and the next command to copy |
| `ailoom first-run` | Checks install readiness, runs a safe demo, shows savings, and prints the next command |
| `ailoom demo` | Runs a safe sample and shows token savings plus restore safety |
| `ailoom handoff --copy --open` | Creates a restore-safe AI/IDE handoff for the current project, opens the bundle, and copies the skeleton when possible |
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
