# MCP-Skeleton Cross-Platform Testing

This document describes the repeatable quick and stress validation flow for test machines.

## Quick Smoke

Use this on every platform after pulling or downloading the latest repository snapshot.

macOS/Linux:

```bash
python3 testing/run_cli_checks.py
```

Windows PowerShell:

```powershell
python testing/run_cli_checks.py
```

Expected result:

- `status`: `ok`
- `check_count`: `32` or higher
- `passed`: same as `check_count`
- `failed`: `0`
- `context_doctor_json_ok`: `true`
- `context_scale_benchmark_quick_json_ok`: `true`

## Release Readiness

Use this before tagging a release candidate. It runs py_compile, Python smoke, dogfood self-check, `context doctor`, quick benchmark with baseline save, and Bash smoke when Bash is available.

macOS/Linux:

```bash
python3 testing/release_readiness_check.py
```

Windows PowerShell:

```powershell
python testing/release_readiness_check.py
```

Expected result:

- `status`: `ok`
- `entrypoint`: `release-readiness-check`
- `failed`: `0`
- `checks.python_smoke.stdout_json.failed`: `0`
- `checks.dogfood_self_check.stdout_json.missing_count`: `0`
- `checks.dogfood_self_check.stdout_json.mismatched_count`: `0`
- `checks.context_doctor.stdout_json.restore_check.status`: `ok`
- `checks.quick_benchmark.stdout_json.executive_summary.overall_status`: `ready` or `watch`

## Stress Benchmark

Use this on a test machine when validating large-directory and long-text behavior.

macOS/Linux:

```bash
python3 testing/context_scale_benchmark.py \
  --scale-profile stress \
  --output-json testing/results/stress_benchmark.json \
  --output-md testing/results/stress_benchmark.md \
  --save-baseline-json testing/results/stress_benchmark_baseline.json
```

Windows PowerShell:

```powershell
python testing/context_scale_benchmark.py `
  --scale-profile stress `
  --output-json testing/results/stress_benchmark.json `
  --output-md testing/results/stress_benchmark.md `
  --save-baseline-json testing/results/stress_benchmark_baseline.json
```

Expected stdout summary:

- `status`: `ok`
- `executive_summary.overall_status`: `ready` or `watch`
- `executive_summary.release_readiness`: `ready` or `watch`
- `executive_summary.scale_health`: `ok` or `warn`
- `executive_summary.restore_verified`: all cases restored, for example `93/93`
- `executive_summary.scale_profile`: `stress`
- `executive_summary.monorepo_package_count`: at least `10`
- `executive_summary.monorepo_files_per_package`: at least `120`
- `executive_summary.best_large_directory_savings_percent`: at least `30`
- `executive_summary.best_long_text_savings_percent`: at least `10`

Treat `blocked`, `fail`, restore mismatches, or non-zero failed smoke checks as blocking issues.

## Report Template

When reporting results back from a test machine, paste this compact summary.

```text
commit:
runner:
os:
python:
quick_smoke: passed/total
failed:
context_scale_benchmark_quick_json_ok:
doctor_readiness_status:
doctor_restore_status:
dogfood_recommended_trial_status:

stress_status:
stress_overall_status:
stress_restore_verified:
stress_scale_profile:
stress_case_count:
stress_monorepo_package_count:
stress_monorepo_files_per_package:
stress_monorepo_max_token_ratio:
stress_realistic_directory_max_token_ratio:
stress_best_large_directory_savings_percent:
stress_best_long_text_savings_percent:
```

## Notes

- Windows machines without Bash should use `testing/run_cli_checks.py`.
- The legacy `--quick` benchmark shortcut is still supported, but `--scale-profile quick` is preferred for new reports.
- Stress results are for release confidence and scale tuning. They do not change restore fidelity because the restore package remains byte-exact.
