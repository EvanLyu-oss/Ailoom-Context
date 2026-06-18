# Ailoom Context Release Checklist

Use this checklist before publishing a beta or v1.0 release.

## 1. Local Readiness

```bash
python3 -m py_compile cli/ail_cli.py cli/context_compression.py testing/context_scale_benchmark.py testing/run_cli_checks.py testing/quickstart_check.py testing/dogfood_self_check.py testing/release_readiness_check.py
python3 -m py_compile ailoom_core/__init__.py ailoom_core/sdk.py
python3 testing/run_cli_checks.py
python3 testing/release_readiness_check.py
```

Required result:

- Python smoke passes
- quickstart passes
- dogfood restore status is `ok`
- benchmark status is `ready`
- scale health is `ok`
- restore verification is complete
- `executive_summary.v1_beta_readiness.status` is `ready`
- `executive_summary.v1_user_experience_readiness.status` is `ready`

## 2. Storage Safety

```bash
ailoom doctor --storage --json
ailoom clean --dry-run --all --older-than 7d --json
```

Required result:

- cleanup preview only lists known generated artifacts
- no source files are listed
- large generated directories are visible before deletion

## 3. User Trial Path

```bash
ailoom demo
ailoom first-run
ailoom handoff
ailoom savings --write-report ailoom-savings-report.md
ailoom trial-report --write-report ailoom-trial-report.md
ailoom safety
```

Required result:

- first-run output is understandable
- savings report includes source tokens, skeleton tokens, tokens saved, and savings percent
- trial report includes value summary, storage risk, trial readiness, and feedback questions
- safety output clearly says skeletons can be shared and restore packages stay local

## 4. Documentation

Check:

- [INSTALL.md](../INSTALL.md)
- [docs/USER_GUIDE.md](USER_GUIDE.md)
- [docs/BETA_TESTING.md](BETA_TESTING.md)
- [docs/V1_STABLE_READINESS.md](V1_STABLE_READINESS.md)
- [FEEDBACK_TEMPLATE.md](../FEEDBACK_TEMPLATE.md)
- [SECURITY.md](../SECURITY.md)

Required documentation result:

- README first screen shows the 3-command install / first-run / handoff path.
- INSTALL shows the no-learning path for macOS and Windows.
- USER_GUIDE starts with the five-minute loop.
- V1 stable readiness states install, first project, value, safety, performance, and release gates.
- Integration docs cover Python SDK, JSON contract, AILOOM-SKL.v1, VS Code MVP, competitive benchmark plan, and two-minute demo script.

## 5. Release Notes

Use [docs/GITHUB_RELEASE_TEMPLATE.md](GITHUB_RELEASE_TEMPLATE.md).

For v1 beta trial distribution, also publish [docs/V1_BETA_RELEASE_NOTES.md](V1_BETA_RELEASE_NOTES.md) and tag the release as `v1.0.0-beta.1`.
