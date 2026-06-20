# Launch Readiness

This document is the public-trial launch checklist for Ailoom Context.

## Launch Goal

Make the first public user experience feel obvious:

1. Install locally.
2. Run one safe demo.
3. Run one project handoff.
4. See token savings and restore safety.
5. Know exactly what to share with AI and what to keep local.
6. Send useful feedback if anything feels confusing or slow.

## User-Facing Entry Points

| User | Best first path |
| --- | --- |
| CLI user | `sh install.sh --setup-shell` then `ailoom first-run` |
| VS Code user | Install extension, run `Ailoom: Version / Install Check`, then `Ailoom: Handoff Current Workspace` |
| CI user | Use `.github/actions/ailoom-handoff` in a local checkout |
| Evaluator | Run `python3 testing/competitive_benchmark.py --force --check-npm-registry --json` |
| Demo viewer | Run `python3 testing/demo_artifact_pack.py --force --json` |

## Proof To Show

- `python3 testing/release_readiness_check.py`
- `python3 testing/competitive_benchmark.py --force --check-npm-registry --json`
- `python3 testing/demo_artifact_pack.py --force --json`
- `ailoom trial-report --write-report ailoom-trial-report.md`

## Launch Assets

| Asset | Path |
| --- | --- |
| VS Code Marketplace checklist | `docs/VSCODE_MARKETPLACE_RELEASE.md` |
| GitHub Action docs | `docs/GITHUB_ACTION_MVP.md` |
| Competitive benchmark plan | `docs/COMPETITIVE_BENCHMARK_PLAN.md` |
| Two-minute demo script | `docs/DEMO_SCRIPT_2_MIN.md` |
| Social launch copy | `docs/LAUNCH_POSTS.md` |
| Public showcase | `docs/SHOWCASE.md` |
| Feedback template | `FEEDBACK_TEMPLATE.md` |
| GitHub issue form | `.github/ISSUE_TEMPLATE/beta-feedback.yml` |

## Public Trial Success Criteria

- A new user can install and run `ailoom first-run` without reading long docs.
- A real project handoff shows restore safety and token savings.
- The user can tell which files are safe to share with AI.
- The user sees no hidden network, cloud, or telemetry behavior.
- Cleanup and storage visibility are obvious.
- Feedback reports include OS, version, install path, speed, savings, and AI/IDE used.
