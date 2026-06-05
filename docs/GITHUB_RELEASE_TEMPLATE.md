# GitHub Release Template

# Ailoom Context v1.0.0-beta.1

This beta is ready for local macOS trial use. It focuses on local, lossless AI/IDE handoff for large repositories and long documents, with exact restore packages, visible token savings, storage cleanup guidance, and structured beta feedback.

## Install

macOS:

```bash
sh install.sh --setup-shell
ailoom first-run
```

Windows PowerShell beta path:

```powershell
.\install.ps1 -SetupShell
ailoom doctor --install
```

## Recommended beta test

Run this inside a real project:

```bash
ailoom handoff --copy --open
ailoom savings
ailoom savings --write-report ailoom-savings.md
ailoom trial-report --write-report ailoom-trial-report.md
ailoom doctor --storage
ailoom clean --dry-run --all --older-than 7d
```

## What to look for

- `Restore safety: OK`
- `context_skeleton.mcp` clearly marked as the AI/IDE file
- restore package files clearly marked keep-local
- `Value summary` explaining token value and next command
- second handoff reuse is faster when the project has not changed
- `doctor --storage` shows generated artifact size, risk level, and cleanup safety
- `trial-report` includes value summary, storage risk, readiness, and feedback questions

## User experience gate

This beta should feel usable without reading the full documentation:

- install with one script
- run `ailoom first-run`
- run `ailoom handoff --copy --open` in a real project
- see token savings and speed guidance immediately
- know which file is safe to share with AI
- know which restore files must stay local
- clean generated artifacts with a dry-run-first command

## Safety model

- local-only processing
- no telemetry or background log collection
- share `context_skeleton.mcp`
- keep restore packages local
- cleanup previews only target known generated artifacts

## Release gate

This release should show:

- `testing/run_cli_checks.py`: all checks passing
- `testing/release_readiness_check.py`: all checks passing
- `executive_summary.v1_beta_readiness.status`: `ready`
- `executive_summary.v1_user_experience_readiness.status`: `ready`
- benchmark: `ready / ready / ok`
- restore verified: complete

## Feedback

Please include:

- OS and Python version
- install method
- whether `ailoom first-run` made the next step obvious
- whether `Value summary` made token savings clear
- whether speed felt acceptable
- whether storage cleanup guidance felt safe
- generated `ailoom-trial-report.md`

Contact: carwyn910@gmail.com
