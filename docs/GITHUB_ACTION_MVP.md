# GitHub Action MVP

This document defines the first CI/CD integration path for Ailoom Context.

The action is local-first: it runs inside the GitHub Actions runner, installs Ailoom locally, writes a skeleton handoff, and emits JSON reports. It does not upload source code to any Ailoom server.

MVP action location:

```text
.github/actions/ailoom-handoff/action.yml
```

## Usage

From this repository or a checkout that contains the local action:

```yaml
name: Ailoom Handoff

on:
  pull_request:
  workflow_dispatch:

jobs:
  ailoom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/ailoom-handoff
        with:
          input-dir: "."
          output-dir: ".workspace_ail/github-action-handoff"
          result-dir: ".workspace_ail/github-action-results"
```

## Outputs

| Output | Description |
| --- | --- |
| `handoff-json` | Path to the generated handoff JSON |
| `savings-json` | Path to the generated savings JSON |
| `skeleton-file` | Path to `context_skeleton.mcp` |

## What It Proves

- Ailoom can be installed in CI.
- A restore-safe handoff can be generated from a pull request workspace.
- Token savings can be reported as JSON.
- CI wrappers do not need to parse terminal text.
- GitHub Action outputs are emitted through `$GITHUB_OUTPUT`.

## Not In MVP

- GitHub Marketplace publication.
- PR comments.
- artifact upload.
- policy gates.
- private enterprise audit reporting.

Those should come after local action validation and real user feedback.
