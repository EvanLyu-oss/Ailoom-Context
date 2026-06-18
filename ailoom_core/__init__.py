"""Public Python integration helpers for Ailoom Context.

The SDK is intentionally thin in v1 beta: it calls the local Ailoom CLI JSON
contract and returns structured payloads for IDEs, agents, CI jobs, and scripts.
"""

from .sdk import (
    AiloomCommandError,
    AiloomResult,
    doctor_project,
    explain_bundle,
    get_savings,
    handoff_project,
    inspect_bundle,
    next_action,
    quick_bundle,
    restore_bundle,
    run_cli_json,
    safety,
)

__all__ = [
    "AiloomCommandError",
    "AiloomResult",
    "doctor_project",
    "explain_bundle",
    "get_savings",
    "handoff_project",
    "inspect_bundle",
    "next_action",
    "quick_bundle",
    "restore_bundle",
    "run_cli_json",
    "safety",
]
