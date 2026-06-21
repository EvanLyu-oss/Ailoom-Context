# GitHub Release Template

# Ailoom Context v1.0.0-beta.2

This beta is ready for public local trial use. It focuses on local, lossless AI/IDE handoff for large repositories and long documents, with exact restore packages, visible token savings, storage cleanup guidance, structured beta feedback, VS Code Marketplace preparation, GitHub Action handoff, and public benchmark/demo materials.

This is still a beta, not the final v1.0 stable release. Please report install friction, speed issues, confusing output, Windows/macOS differences, and AI/IDE workflow feedback.

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

For launch/benchmark/demo validation:

```bash
python3 testing/competitive_benchmark.py --force --check-npm-registry --json
python3 testing/demo_artifact_pack.py --force --json
```

## What to look for

- `Restore safety: OK`
- `context_skeleton.mcp` clearly marked as the AI/IDE file
- restore package files clearly marked keep-local
- `Value summary` explaining token value and next command
- second handoff reuse is faster when the project has not changed
- `doctor --storage` shows generated artifact size, risk level, and cleanup safety
- `trial-report` includes value summary, storage risk, readiness, and feedback questions
- VS Code users can run `Ailoom: Version / Install Check`
- demo artifacts include screenshot notes, a recording runbook, and a social caption

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

## Public beta assets

- Launch checklist: `docs/LAUNCH_READINESS.md`
- VS Code Marketplace checklist: `docs/VSCODE_MARKETPLACE_RELEASE.md`
- Benchmark report: `docs/COMPETITIVE_BENCHMARK_REPORT.md`
- Demo script: `docs/DEMO_SCRIPT_2_MIN.md`
- Feedback issue template: `.github/ISSUE_TEMPLATE/beta-feedback.yml`

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
