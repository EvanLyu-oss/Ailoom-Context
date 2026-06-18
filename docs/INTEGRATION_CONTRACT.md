# Ailoom Integration Contract

This document defines the public integration surface for IDEs, agents, CI jobs, and scripts that want to call Ailoom Context.

The v1 beta integration strategy is intentionally simple:

- Use the local CLI JSON contract.
- Or use the Python SDK, which wraps the same local CLI JSON contract.
- Do not parse human terminal output.
- Do not upload source code to any Ailoom server.

## Stability Levels

| Level | Meaning |
| --- | --- |
| Stable | Intended for plugins, CI, and user scripts. Changes require a compatibility note. |
| Beta | Usable, but may gain fields or minor wording changes before v1 stable. |
| Experimental | Internal or diagnostic. Do not rely on it for integrations. |

## Python SDK

Import path:

```python
from ailoom_core import handoff_project, get_savings, next_action, safety
```

Minimal IDE/agent flow:

```python
from ailoom_core import get_savings, handoff_project, next_action

handoff = handoff_project(".", copy=False, open_bundle=False)
print(handoff.payload["handoff"]["skeleton_file"])
print(handoff.payload["handoff"]["ai_handoff_file"])

savings = get_savings(".")
print(savings.payload["savings_percent"])

next_step = next_action(".")
print(next_step.payload["primary_command_text"])
```

SDK functions return `AiloomResult`:

| Field | Stable | Description |
| --- | --- | --- |
| `payload` | Stable | Parsed JSON object emitted by Ailoom |
| `returncode` | Stable | CLI process exit code |
| `args` | Stable | Executed local command |
| `cwd` | Stable | Working directory used for the command |
| `stdout` | Stable | Raw stdout for debugging |
| `stderr` | Stable | Raw stderr for debugging |

By default, non-zero exit codes raise `AiloomCommandError`. Pass `check=False` if an integration wants to inspect validation or usage errors directly.

## Stable Commands For Integrations

Use these commands with `--json`.

| Command | Stability | Primary use |
| --- | --- | --- |
| `ailoom handoff --json` | Stable | Create or reuse a restore-safe AI/IDE handoff |
| `ailoom savings --json` | Stable | Read token value from the latest handoff |
| `ailoom next --json` | Stable | Show the next best project action |
| `ailoom doctor --install --json` | Stable | Check local install readiness |
| `ailoom doctor --storage --json` | Stable | Inspect generated artifact storage |
| `ailoom safety --json` | Stable | Explain local safety boundaries |
| `ailoom inspect --package-file ... --json` | Stable | Read bundle metadata without restore |
| `ailoom explain --package-file ... --json` | Stable | Convert a bundle into human-oriented guidance |
| `ailoom restore --package-file ... --output-dir ... --json` | Stable | Restore into an explicit output target |

## Handoff Payload Contract

Command:

```bash
ailoom handoff --json
```

Stable fields:

| Field | Description |
| --- | --- |
| `status` | Command status, normally `ok` |
| `entrypoint` | `context-quick` for handoff/quick bundle flow |
| `quick_status` | `ready`, `reused`, or `blocked` |
| `restore_safe` | Boolean restore-safety gate |
| `bundle_root` | Bundle directory path |
| `manifest_file` | `context_manifest.json` path |
| `handoff.skeleton_file` | AI-facing skeleton file |
| `handoff.ai_file` | Same AI-facing file, repeated for simple wrappers |
| `handoff.ai_handoff_file` | Markdown prompt/instructions for AI/IDE |
| `handoff.metadata_file` | `handoff.json` metadata path |
| `handoff.restore_keep_files` | Keep-local restore files |
| `handoff.restore_guidance` | Plain-language restore boundary |
| `handoff.recommended_prompt` | Prompt text to paste into an AI/IDE |
| `daily_handoff.status` | `created` or `reused` |
| `reuse_policy.default_for_handoff` | Whether default handoff reuse is active |
| `value_summary` | Token value classification and recommendation |
| `user_outcome.primary_file` | File the user should give to AI |
| `user_outcome.next_command_text` | Best next command |

Integrations should prefer:

- `handoff.skeleton_file` for the file to show/open/copy.
- `handoff.ai_handoff_file` for the prompt to show the user.
- `handoff.restore_keep_files` for warning users what must stay local.
- `value_summary` for UI badges and token value.
- `daily_handoff.status` for "created vs reused" UI.

## Savings Payload Contract

Command:

```bash
ailoom savings --json
```

Stable fields:

| Field | Description |
| --- | --- |
| `status` | Command status |
| `entrypoint` | `context-savings` |
| `savings_status` | `ready` or `missing` |
| `source_tokens` | Estimated source token count |
| `skeleton_tokens` | Estimated skeleton token count |
| `tokens_saved` | Estimated tokens saved |
| `savings_percent` | Estimated savings percent |
| `freshness_status` | Whether latest handoff is fresh |
| `value_summary.status` | `strong`, `useful`, `watch`, or `tiny_project` |
| `value_summary.headline` | User-facing value headline |
| `value_summary.agent_context_reading` | Estimated agent reading improvement |
| `next_command_text` | Recommended next command |

## Next Payload Contract

Command:

```bash
ailoom next --json
```

Stable fields:

| Field | Description |
| --- | --- |
| `next_status` | `needs_handoff`, `ready`, or `refresh_needed` |
| `current_step` | Machine-readable step name |
| `primary_command_text` | One command the user should run next |
| `commands` | Common next commands |
| `action_plan` | Ordered actions for UI display |
| `tokens_saved` | Latest token savings when available |
| `savings_percent` | Latest savings percent when available |

## Safety Payload Contract

Command:

```bash
ailoom safety --json
```

Stable fields:

| Field | Description |
| --- | --- |
| `safety_status` | Safety output status |
| `guarantees.local_only_processing` | Local-only processing guarantee |
| `guarantees.no_telemetry` | No telemetry guarantee |
| `skeleton_redaction` | AI-facing redaction boundary |
| `restore_package` | Keep-local restore package boundary |
| `patch_replay` | Dry-run-first patch replay guidance |
| `default_noise_protection` | Default skip/noise policy |

## Error Contract

When a JSON command fails, integrations should inspect:

| Field | Description |
| --- | --- |
| `status` | Usually `error` |
| `error.code` | Stable-ish machine-readable error code |
| `error.message` | Human-readable error |
| `error.details.recovery_steps` | Copy/paste recovery guidance when available |
| `error.details.fix_command_text` | Suggested fix command when safe |

Exit codes:

| Code | Meaning |
| --- | --- |
| `0` | Command completed and validation gates passed |
| `1` | General command failure |
| `2` | Invalid usage or invalid input contract |
| `3` | Validation warning or replay gate block |

## Compatibility Rule

Integrations should ignore unknown JSON fields.

Ailoom may add new fields in minor releases. Stable fields listed in this document should not be removed or renamed without a migration note.
