# AILOOM-SKL.v1 Format Spec

`AILOOM-SKL.v1` is the AI-facing skeleton format produced by Ailoom Context.

It is designed for one job: give AI tools enough project or document structure to reason efficiently, while keeping exact restore data local.

## Scope

This spec describes the public skeleton and bundle boundary. It does not require third-party tools to implement Ailoom's internal compression heuristics.

## Core Boundary

Ailoom separates a compressed context into two surfaces:

| Surface | Intended location | Purpose |
| --- | --- | --- |
| `context_skeleton.mcp` / `skeleton_text` | AI/IDE-facing | Compact, redacted, structural context |
| `context_manifest.json` | Local | Restore metadata and bundle entrypoint |
| `context_restore.json` / restore package | Local | Byte-exact source recovery |
| `handoff.json` | Local or IDE wrapper | Stable handoff metadata |

The skeleton is not the source of truth for restore. The restore package is.

## Header

An AILOOM-SKL.v1 skeleton should identify itself near the top of the text with the schema marker:

```text
AILOOM-SKL.v1
```

Readers should treat the marker as a format identity, not as a guarantee that every optional section is present.

## Common Sections

A skeleton may include sections such as:

- source summary
- project tree
- directory groups
- file entries
- imports
- symbols
- writing outline
- omitted entries
- compression warnings
- restore boundary notes

Section wording can evolve. Integrations should not parse the skeleton text as the primary machine-readable API. Use `context_manifest.json`, `handoff.json`, or CLI/SDK JSON for automation.

## Restore Fidelity

`AILOOM-SKL.v1` is allowed to be smaller, redacted, folded, or structurally summarized.

Exact restore depends on the local restore package, not on the skeleton text.

Required behavior:

- Original source files are not modified during compression.
- Restore packages preserve the bytes needed for local recovery.
- Restore writes to explicit output targets.
- Directory restore reconstructs included files, symlinks, and empty directories according to the restore package.

## Redaction Boundary

AI-facing skeleton output may redact common secret shapes, including:

- API keys
- access tokens
- passwords
- client secrets
- database URLs
- private key blocks

Redaction applies to skeleton output. It must not modify original files. It must not modify restore packages, because local restore must remain byte-exact.

## Focus Modes

Current focus modes:

| Mode | Intent |
| --- | --- |
| `full` | Broad skeleton surface |
| `tree` | Directory and structural overview |
| `imports` | Codebase dependency and import flow |
| `symbols` | Code symbols and definitions |
| `writing-outline` | Long-form prose outline and chapter flow |

## Density Modes

Current density modes:

| Mode | Intent |
| --- | --- |
| `adaptive` | Default balance for real projects |
| `standard` | More complete skeleton surface |
| `compact` | Smaller skeleton for large inputs |

Density changes the AI-facing skeleton, not restore fidelity.

## Bundle Manifest

`context_manifest.json` is the stable entrypoint for inspect and restore.

Integrations should call:

```bash
ailoom inspect --package-file context_manifest.json --json
ailoom restore --package-file context_manifest.json --output-dir restore-root --json
```

Do not assume restore package internals unless a later spec explicitly covers them.

## Handoff Metadata

`handoff.json` is the recommended metadata file for IDEs and agent wrappers.

Stable fields are documented in [INTEGRATION_CONTRACT.md](INTEGRATION_CONTRACT.md).

## Compatibility

Readers should:

- treat unknown skeleton sections as informational
- ignore unknown JSON fields
- prefer JSON metadata over parsing skeleton text
- keep restore packages local by default

Writers should:

- include the `AILOOM-SKL.v1` marker
- preserve local restore-package compatibility
- make AI-facing redaction explicit when secrets are detected
- avoid embedding raw restore bytes in AI-facing skeleton text

## Non-Goals

This spec does not define:

- a cloud protocol
- telemetry
- hosted sync
- enterprise policy semantics
- a universal tokenizer standard

Those may be documented separately if they become necessary.
