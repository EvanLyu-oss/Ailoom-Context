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
- `check_count`: `25`
- `passed`: `25`
- `failed`: `0`
- `context_scale_benchmark_quick_json_ok`: `true`

## Stress Benchmark

Use this on a test machine when validating large-directory and long-text behavior.

macOS/Linux:

```bash
python3 testing/context_scale_benchmark.py \
  --scale-profile stress \
  --output-json testing/results/stress_benchmark.json \
  --output-md testing/results/stress_benchmark.md
```

Windows PowerShell:

```powershell
python testing/context_scale_benchmark.py `
  --scale-profile stress `
  --output-json testing/results/stress_benchmark.json `
  --output-md testing/results/stress_benchmark.md
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
