# Public Beta Launch

This is the operator checklist for publishing Ailoom Context v1.0.0-beta.2.

## Release Identity

| Field | Value |
| --- | --- |
| Python package version | `1.0.0b2` |
| Git tag | `v1.0.0-beta.2` |
| Release channel | `v1-beta` |
| Repository | `https://github.com/EvanLyu-oss/Ailoom-Context` |
| Release notes | `docs/V1_BETA_RELEASE_NOTES.md` |
| GitHub release body | `docs/GITHUB_RELEASE_TEMPLATE.md` |

## Pre-Release Checks

Run from the repository root:

```bash
python3 testing/run_cli_checks.py
python3 testing/release_readiness_check.py
python3 testing/competitive_benchmark.py --force --check-npm-registry --json
python3 testing/demo_artifact_pack.py --force --json
```

VS Code extension packaging:

```bash
cd integrations/vscode
npm run prepublish-check
```

Expected result:

- Python smoke passes.
- Release readiness passes.
- Benchmark reports restore fidelity `ok`.
- Demo artifact pack writes `DEMO_SCREENSHOT_NOTES.md`, `RECORDING_RUNBOOK.md`, and `SOCIAL_CAPTION.md`.
- VS Code package creates a `.vsix`; do not commit the `.vsix`.

## GitHub Release

After the commit is pushed:

```bash
git tag v1.0.0-beta.2
git push origin v1.0.0-beta.2
```

Then create a GitHub Release:

- Tag: `v1.0.0-beta.2`
- Title: `Ailoom Context v1.0.0-beta.2`
- Body: copy from `docs/GITHUB_RELEASE_TEMPLATE.md`
- Mark as pre-release.

## VS Code Marketplace

Only publish after the GitHub Release is visible.

```bash
cd integrations/vscode
npx @vscode/vsce login <publisher-id>
npx @vscode/vsce publish
```

Use the copy and safety claims from `docs/VSCODE_MARKETPLACE_RELEASE.md`.

## First Public Posts

Recommended first post order:

1. Personal network or 小红书/朋友圈 with `SOCIAL_CAPTION.md`.
2. GitHub/X post using `docs/COMPETITIVE_BENCHMARK_REPORT.md`.
3. Short demo video using `RECORDING_RUNBOOK.md`.

Keep claims cautious:

- Say "observed" and "in this local fixture".
- Emphasize local-first, no telemetry, no source upload, and restore files kept local.
- Avoid "always saves" or "guaranteed 10x".

## Feedback Window

For the first 7 days, prioritize feedback over new features.

Track:

- install failures
- VS Code command discovery
- Windows path/Python friction
- large project speed
- token savings clarity
- whether users understand skeleton vs restore package
- any accidental cache/storage growth

Ask users to use `.github/ISSUE_TEMPLATE/beta-feedback.yml` or send `ailoom trial-report --write-report ailoom-trial-report.md`.
