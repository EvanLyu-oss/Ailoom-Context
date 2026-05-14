# Changelog

## 0.1.0

- split `context` compression, restore, patch, replay, and benchmark workflows into the dedicated `MCP-Skeleton` repository
- switched the standalone repository license to MIT
- preserved the context-specific commit history from the original private parent repository
- included full and incremental compression flows, dry-run replay previews, policy-aware replay gates, merge-aware replay checks, and scale benchmark tooling
- promoted incremental `context apply-check` into the public surface, including top-level incremental metadata, summary fields, and dedicated smoke coverage
- enabled incremental `context patch-apply`, including incremental replay manifest updates and standalone smoke coverage
- enriched incremental patch dry-run reports with scope, per-lane counts, and first-path summary fields
- added a formal full-vs-incremental benchmark report for the standalone `MCP-Skeleton` repository
- added `context` skeleton focus modes for full, tree, imports, symbols, and writing-outline views
- extended the benchmark harness to compare focus-mode skeleton variants against the full baseline
- added a formal focus-mode benchmark report for directory and long-text skeleton views
- added adaptive and compact skeleton-density modes so large repos and long-form text can ship smaller AI-facing skeletons without changing restore fidelity
- extended the benchmark harness to compare skeleton-density variants against the standard full skeleton baseline
- added grouped directory and extension overviews so large directory skeletons can omit more per-file detail without losing top-level continuity
- added hot-subtree expansion and cold-subtree folding so large directory skeletons spend entry budget where structural signal is densest
- added chapter-fold outlines so long-form text can preserve chapter continuity while spending fewer skeleton tokens
- extended the benchmark harness with realistic repo-directory and repo-document corpora so synthetic results can be checked against repeatable real samples
- tightened directory apply-check drift detection for large added surfaces and added edge-case smoke coverage for missing files, kind changes, and bulk additions
- documented the `0.1.x` stability contract, experimental boundaries, exit-code semantics, and repeatable benchmark signals in the README
- added a `v0.1` release checklist covering scope, required validation commands, documentation review, artifact review, commit shape, and tag steps

## Selected history carried into this repo

- incremental context patches
- context compression principles documentation
- incremental context benchmarks
- incremental context bundles
- incremental context compression
- benchmark restore verification stabilization
- repo-scale benchmark harness
- dry-run report enrichment and risk bands
- merge-aware and policy-aware patch replay
- tokenizer-backed metrics and cross-platform benchmark reporting
