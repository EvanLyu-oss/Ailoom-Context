# Competitive Benchmark Plan

This plan defines a fair, reproducible comparison between Ailoom Context and other context packaging approaches.

The goal is not to attack competitors. The goal is to show where Ailoom's lossless restore boundary and token efficiency are objectively useful.

MVP runner:

```bash
python3 testing/competitive_benchmark.py --force --check-npm-registry --json
```

The first runner compares Ailoom Context with a raw concatenation baseline, detects local `repomix` / `repopack` binaries, and can record npm registry versions without installing or running competitors by default.

Important package note: `repopack` is the older package name and is deprecated in favor of `repomix`. Public reports should avoid presenting it as a separate modern competitor unless a user specifically asks for the old package lineage.

## Tools To Compare

Initial candidates:

- Ailoom Context
- Repomix
- Repopack
- raw concatenation baseline

Only include tools that can be installed and run locally in a repeatable way.

## Metrics

| Metric | Why it matters |
| --- | --- |
| Output tokens | Direct context cost and agent-reading pressure |
| Output bytes | File size and transfer weight |
| Runtime | User experience |
| Restore fidelity | Whether exact local reconstruction is available |
| Secret redaction behavior | Whether AI-facing output hides common secrets |
| Default skip/noise behavior | Whether dependencies, caches, and build outputs are skipped |
| Local-only behavior | Whether the tool requires network/cloud processing |

## Fixtures

Use repeatable fixtures:

- small code project
- medium realistic repo
- synthetic monorepo
- long markdown manuscript
- repo with generated dependency/cache directories
- repo with `.env`-style secret shapes

Do not benchmark private user code in public reports.

## Ailoom Commands

```bash
ailoom handoff --input-dir fixture --output-dir results/ailoom --json
ailoom savings --input-dir fixture --json
ailoom restore --package-file results/ailoom/context_manifest.json --output-dir results/ailoom-restore --json
```

## Baseline Commands

Raw concatenation should be implemented by a short script that:

- walks included files
- applies the same broad skip list where appropriate
- concatenates file paths and contents
- reports token count and bytes

Competitor tools should use their documented recommended commands. Record exact versions.

For version discovery without global installation:

```bash
npm view repomix version --silent
npm view repopack version --silent
```

For a local external-tool readiness check:

```bash
python3 testing/competitive_benchmark.py --force --check-npm-registry --run-external-tools --json
```

The MVP records external availability/version. Full output-level competitor runs should only be published after each tool-specific command is implemented and reviewed for fairness.

## Report Shape

Each benchmark report should include:

- OS
- Python/Node versions
- tool versions
- fixture name
- file count
- source bytes
- output bytes
- estimated output tokens
- runtime
- restore fidelity result
- notes on redaction/default skips
- npm registry versions when `--check-npm-registry` is used
- exact next command required to reproduce the run

## Fairness Rules

- Do not compare Ailoom's best tuned mode against another tool's worst mode.
- Show command lines.
- Show fixture generation.
- Separate "token efficiency" from "restore fidelity".
- State when a tool does not provide restore.
- Use "observed" and "in this benchmark", not universal claims.

## First Public Claim Target

The first public comparison should aim for a cautious claim:

```text
In reproducible local fixtures, Ailoom Context provides compact AI-facing skeletons with byte-exact local restore packages. Token savings and runtime vary by project size and focus mode.
```

Avoid:

```text
Ailoom is always faster and always smaller than every competitor.
```
