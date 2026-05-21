# MCP-Skeleton v0.1 Release Checklist

Use this checklist before tagging or publishing the `0.1.x` line.

## Scope

Release goal:

- publish `MCP-Skeleton` as a focused, standalone project for lossless context compression, exact restore, patch, replay, incremental bundles, and benchmark reporting

Included in `0.1.x`:

- `context compress`, `inspect`, `restore`, `apply-check`, `bundle`, `patch`, and `patch-apply`
- text, file, directory, and incremental directory restore paths
- dry-run replay reports
- policy-aware and merge-aware replay gates
- incremental compress, bundle, apply-check, patch, and patch-apply flows
- focus modes: `full`, `tree`, `imports`, `symbols`, `writing-outline`
- skeleton density modes: `adaptive`, `standard`, `compact`
- realistic benchmark cases for this repository and repository-derived documentation

Out of scope for `0.1.x`:

- ecommerce, website, homepage, personal-site, or writing-generation product surfaces
- promises that `skeleton_text` wording or ordering is stable across minor releases
- billing-grade token accounting
- semantic code transformation beyond patch export and controlled replay

## Pre-Tag Checks

Run from the repository root:

```bash
pwd
git status --short --branch
git log --oneline --decorate -n 10
python3 -m py_compile cli/ail_cli.py cli/context_compression.py testing/context_scale_benchmark.py testing/run_cli_checks.py testing/dogfood_self_check.py
python3 testing/run_cli_checks.py
python3 testing/dogfood_self_check.py
bash testing/run_cli_checks.sh
python3 testing/context_scale_benchmark.py --quick --output-json testing/results/release_quick_benchmark.json --output-md testing/results/release_quick_benchmark.md
```

On Windows or other environments without Bash, run:

```powershell
python -m py_compile cli/ail_cli.py cli/context_compression.py testing/context_scale_benchmark.py testing/run_cli_checks.py testing/dogfood_self_check.py
python testing/run_cli_checks.py
python testing/dogfood_self_check.py
python testing/context_scale_benchmark.py --quick --output-json testing/results/windows_release_quick_benchmark.json --output-md testing/results/windows_release_quick_benchmark.md
```

Optional fuller benchmark:

```bash
python3 testing/context_scale_benchmark.py \
  --directory ./cli \
  --real-directory . \
  --real-text-files README.md CONTEXT_COMPRESSION_PRINCIPLES_20260507.md CONTEXT_COMPRESSION_SPEC_20260428.md CHANGELOG.md \
  --iterations 2
```

Expected minimum result:

- `testing/run_cli_checks.py` reports `status: ok`
- Python smoke coverage reports `28/28` passing or better
- `testing/dogfood_self_check.py` reports `status: ok`, `missing_count: 0`, and `mismatched_count: 0`
- `run_cli_checks.sh` reports `status: ok` on Unix-like environments
- Bash smoke coverage reports `36/36` passing or better on Unix-like environments
- realistic directory and realistic text benchmark cases are present
- restore verification is true for directory, text, incremental, and realistic benchmark cases

## Documentation Review

Confirm these files match the release boundary:

- `README.md`: quick start, `v0.1 stability contract`, benchmark instructions, scope statement
- `CHANGELOG.md`: `0.1.0` feature list and release notes
- `CONTEXT_COMPRESSION_PRINCIPLES_20260507.md`: project principles still align with the public positioning
- `CONTEXT_COMPRESSION_SPEC_20260428.md`: compression and restore contract remains accurate
- `RELEASE_CHECKLIST_0_1.md`: this checklist is current
- `CONTEXT_CROSS_PLATFORM_VALIDATION_REPORT_20260520.md`: latest macOS and Windows validation snapshots are recorded

## Artifact Review

Before tagging, inspect at least one generated bundle and one generated patch:

- `context_manifest.json` includes `skeleton_density`, `focus_mode`, `source_summary`, and `restore_package`
- `context_skeleton.mcp` starts with `MCP-SKL.v1`
- `context_restore.json` can restore the original input exactly
- `patch_manifest.json` includes `apply_check_passed`, changed paths, added paths, and removed paths
- dry-run reports include surface size and risk band

## Git Steps

Review changes:

```bash
git diff --stat
git diff -- README.md CHANGELOG.md RELEASE_CHECKLIST_0_1.md CONTEXT_CROSS_PLATFORM_VALIDATION_REPORT_20260520.md
```

Suggested commit shape:

```bash
git add README.md CHANGELOG.md RELEASE_CHECKLIST_0_1.md CONTEXT_CROSS_PLATFORM_VALIDATION_REPORT_20260520.md cli/ail_cli.py cli/context_compression.py testing/run_cli_checks.py testing/dogfood_self_check.py testing/context_scale_benchmark.py
git commit -m "prepare v0.1.x release candidate"
```

Suggested tag pattern:

```bash
git tag -a v0.1.x -m "MCP-Skeleton v0.1.x"
```

Only tag after the working tree contains exactly the intended release changes and both macOS and Windows validation results have been recorded.

## Release Notes Summary

Short summary:

MCP-Skeleton `v0.1.0` provides a standalone lossless context compression workflow with exact restore, structural drift checks, patch export, controlled replay, incremental bundles, focus/density skeleton modes, and repeatable benchmark reporting.

Known experimental areas:

- adaptive skeleton budgeting heuristics
- apply-check scoring thresholds
- exact skeleton text layout
- cross-machine benchmark timing
