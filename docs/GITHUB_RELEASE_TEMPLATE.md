# GitHub Release Template

## Ailoom Context beta release

This beta focuses on local, lossless AI/IDE handoff for large repositories and long documents.

## Install

macOS:

```bash
sh install.sh --setup-shell
ailoom demo
ailoom handoff
```

Windows PowerShell:

```powershell
.\install.ps1 -SetupShell
ailoom doctor --install
ailoom demo
ailoom handoff
```

## Recommended beta test

```bash
ailoom demo
ailoom handoff --copy --open
ailoom savings --write-report ailoom-savings-report.md
ailoom doctor --storage
ailoom clean --dry-run --all --older-than 7d
```

## What to look for

- `Restore safety: OK`
- clear skeleton file path for AI/IDE handoff
- source tokens, skeleton tokens, tokens saved, and savings percent
- second handoff reuse is faster when the project has not changed
- restore package files are clearly marked keep-local

## Safety model

- local-only processing
- no telemetry
- share `context_skeleton.mcp`
- keep restore packages local
- cleanup previews only target known generated artifacts

## Feedback

Please include:

- OS and Python version
- install method
- `ailoom savings --write-report` report
- speed notes from first and second handoff
- any confusing output or safety concerns
