# Competitive Benchmark Report

Generated from a local reproducible fixture on 2026-06-20.

This report is an observed local result, not a universal claim. It compares Ailoom Context with a raw concatenation baseline and records external package availability/version data for Repomix/Repopack.

## Command

```bash
python3 testing/competitive_benchmark.py --force --check-npm-registry --json
```

## Environment

| Field | Value |
| --- | --- |
| Platform | `macOS-26.5.1-arm64-arm-64bit` |
| Python | `3.9.6` |
| Processing | Local-only |
| Fixture | Generated benchmark fixture |

## Results

| Tool | Status | Output tokens | Output bytes | Runtime ms | Restore fidelity | Notes |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Ailoom Context | `ok` | `515` | `1,735` | `193.38` | `ok` | AI-facing skeleton, restore package stays local |
| Raw concat | `ok` | `4,931` | `19,725` | `0.47` | `not-supported` | Concatenates files, no exact restore package |
| Repomix | `skipped` | | | | | Not installed on PATH; npm registry version `1.15.0` |
| Repopack | `skipped` | | | | | Not installed on PATH; npm registry version `0.1.45`; old package name now deprecated in favor of Repomix |

## Observed Summary

- Ailoom vs raw token ratio: `0.1044x`
- Ailoom token savings vs raw output in this fixture: about `89.56%`
- Ailoom restore fidelity: `ok`
- Raw concat restore fidelity: `not-supported`
- Ailoom source tokens reported by CLI: `3,564`
- Ailoom skeleton tokens reported by CLI: `515`
- Ailoom estimated tokens saved from source: `3,049`
- Ailoom estimated savings from source: `85.55%`

Safe public claim:

```text
In this local fixture, Ailoom used 0.1044x the raw-concat token output while preserving restore fidelity: ok.
```

Avoid:

```text
Ailoom is always smaller or faster than every competitor.
```

## Next Fairness Step

Install competitor tools locally, record exact versions, and only publish output-level competitor comparisons after their recommended commands are implemented and reviewed.

```bash
npm view repomix version --silent
npm view repopack version --silent
python3 testing/competitive_benchmark.py --force --check-npm-registry --run-external-tools --json
```
