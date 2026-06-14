# Ailoom Context v1.0 Stable Readiness

This document defines the v1.0 stable target for Ailoom Context.

The goal is not to add more commands. The goal is to make the existing commands feel obvious, safe, and fast for a first-time AI coding user.

## Product Promise

Ailoom Context should let a developer install the tool, create a restore-safe AI/IDE handoff, and see token savings without learning the internal bundle format.

The stable v1.0 promise:

- Install in one local command from a cloned or downloaded checkout.
- Run one safe first command: `ailoom first-run`.
- Use one daily project command: `ailoom handoff`.
- Ask one state-aware guide: `ailoom next`.
- See value with one report: `ailoom savings`.
- Keep source and restore packages local by default.
- Clean generated artifacts with dry-run-first commands.

## Zero-Learning Command Loop

These are the commands a new user should remember:

```bash
ailoom first-run
ailoom handoff --copy --open
ailoom next
ailoom savings
```

If the user only runs `ailoom`, the welcome screen should still point them back to this loop.

## Install Experience Gate

Stable v1.0 should pass this user story:

> I downloaded or cloned the repository, ran the installer, and the terminal told me exactly what to run next.

Required behavior:

- macOS installer prints the command path, PATH status, first-run command, handoff command, and install doctor command.
- Windows installer prints the same guidance in PowerShell terms.
- `ailoom version --json` exposes version, release channel, repository URL, install-readiness file, and command availability.
- `ailoom doctor --install` explains whether Python, PATH, version identity, and install readiness are OK.
- If PATH is not ready, the output includes a copy/paste temporary PATH command and a persistent setup command.

## First Project Gate

Stable v1.0 should pass this user story:

> I ran one command inside my project and knew which file to give AI, which files to keep local, and whether the result was worth using.

Required behavior:

- `ailoom handoff` defaults to the current directory.
- `context_skeleton.mcp` is clearly marked as the AI-facing file.
- `context_manifest.json`, restore packages, and bundle metadata are clearly marked keep-local.
- `AI_HANDOFF.md` gives a copy/paste AI prompt.
- `handoff.json` provides machine-readable fields for IDEs and wrappers.
- The output includes restore safety, token savings, speed guidance, reuse status, and the next command.

## Value Gate

Stable v1.0 should pass this user story:

> I can quickly tell whether Ailoom helped this project.

Required behavior:

- `ailoom savings` shows source tokens, skeleton tokens, tokens saved, savings percent, and estimated agent context-reading speedup.
- Tiny projects are explained honestly instead of being treated as failures.
- Reused handoffs explain that the previous fresh bundle was reused because the project fingerprint did not change.
- Benchmark and dogfood outputs keep reporting restore verification counts.

## Safety Gate

Stable v1.0 should pass this user story:

> I trust that the tool is local-first and that cleanup will not delete my source.

Required behavior:

- README first screen states local-only and zero telemetry.
- `ailoom safety` explains share-vs-keep-local boundaries.
- `ailoom doctor --storage` shows generated artifact size before cleanup.
- `ailoom clean --dry-run --all` is the recommended cleanup preview.
- Cleanup only targets known generated Ailoom Context artifact roots.
- Restore writes to explicit output targets instead of overwriting source by default.

## Performance Gate

Stable v1.0 should pass this user story:

> The tool should not make daily AI development feel slower.

Required behavior:

- `ailoom handoff` automatically reuses a fresh unchanged bundle.
- `ailoom handoff --force-refresh` is the explicit escape hatch.
- Large or slower runs recommend faster next commands when useful.
- Release readiness includes quick benchmark coverage and dogfood timing.
- Public claims use observed data, not guarantees.

## Release Gate

Before calling a release v1.0 stable, run:

```bash
python3 -m py_compile cli/ail_cli.py cli/context_compression.py testing/context_scale_benchmark.py testing/run_cli_checks.py testing/quickstart_check.py testing/dogfood_self_check.py testing/release_readiness_check.py
python3 testing/run_cli_checks.py
python3 testing/release_readiness_check.py
python3 testing/dogfood_self_check.py
```

Required result:

- Python smoke passes.
- Release readiness passes.
- Dogfood restore status is `ok`.
- Benchmark overall/release/scale is `ready / ready / ok`.
- Restore verification is complete.
- `v1_beta_readiness.status` is `ready` until the release channel is renamed for stable.
- `v1_user_experience_readiness.status` is `ready`.

## What Is Not Required For v1.0

These are valuable after stable, but should not block v1.0:

- Full IDE plugin.
- Hosted service or dashboard.
- Team sharing workflow.
- Enterprise policy engine.
- Cloud sync.
- A web UI.

The v1.0 focus is the local CLI experience.
