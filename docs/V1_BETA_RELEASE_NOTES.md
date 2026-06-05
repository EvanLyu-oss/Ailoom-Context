# Ailoom Context v1.0.0-beta.1 Release Notes

Release date: 2026-06-05

This beta is the first Ailoom Context release candidate intended for real local macOS beta use. It focuses on zero-friction installation, restore-safe AI/IDE handoff, visible token savings, local-only safety, generated-artifact cleanup, and structured beta feedback.

## Who should try this beta

- Developers using AI coding tools on medium or large repositories.
- Writers or researchers working with long markdown/text manuscripts.
- Users who want local-only context compression with exact restore packages.
- Testers willing to send `ailoom trial-report --write-report ailoom-trial-report.md` output.

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

Windows compatibility is covered by the Python smoke runner, but this beta is primarily recommended for local macOS trial use first.

## First real project loop

Run these commands inside a project:

```bash
ailoom handoff --copy --open
ailoom savings
ailoom trial-report --write-report ailoom-trial-report.md
ailoom doctor --storage
```

Expected result:

- `context_skeleton.mcp` is the AI-facing file.
- Restore package files are clearly marked keep-local.
- `Value summary` explains whether token savings are strong, useful, watch-level, or tiny-project.
- `doctor --storage` reports generated artifact size, risk level, and cleanup safety.
- `trial-report` creates one Markdown report for beta feedback.

## Safety model

- Local-only processing by default.
- No telemetry, analytics beacons, background log collection, or source upload.
- AI-facing skeletons are redacted for common secret shapes.
- Restore packages preserve original bytes and should stay local.
- Restore writes to explicit output targets instead of overwriting source by default.
- Cleanup commands only target known generated Ailoom Context artifact roots.

## Release readiness status

The release gate for this beta is:

```bash
python3 testing/release_readiness_check.py
```

Required summary:

- `executive_summary.v1_beta_readiness.status`: `ready`
- `executive_summary.v1_user_experience_readiness.status`: `ready`
- benchmark overall/release/scale: `ready / ready / ok`
- restore verified: complete

## Feedback

Please send:

- OS and Python version.
- Install method.
- Whether `ailoom first-run` made the next step obvious.
- Whether `Value summary` made token savings clear.
- Whether handoff speed felt acceptable.
- Whether storage cleanup guidance felt safe.
- The generated `ailoom-trial-report.md`.

Contact: carwyn910@gmail.com
