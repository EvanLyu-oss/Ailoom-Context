from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence, Union


PathLike = Union[str, os.PathLike[str]]


@dataclass(frozen=True)
class AiloomResult:
    """Structured result returned by the Ailoom Python SDK."""

    payload: dict[str, Any]
    returncode: int
    args: tuple[str, ...]
    cwd: str
    stdout: str
    stderr: str


class AiloomCommandError(RuntimeError):
    """Raised when a local Ailoom CLI JSON command fails."""

    def __init__(self, result: AiloomResult) -> None:
        self.result = result
        code = result.payload.get("error", {}).get("code") if isinstance(result.payload.get("error"), dict) else ""
        message = result.payload.get("error", {}).get("message") if isinstance(result.payload.get("error"), dict) else ""
        detail = f" ({code}: {message})" if code or message else ""
        super().__init__(f"ailoom command failed with exit {result.returncode}{detail}")


def _stringify_path(value: PathLike | None) -> str | None:
    if value is None:
        return None
    return str(Path(value))


def _append_path_option(args: list[str], option: str, value: PathLike | None) -> None:
    normalized = _stringify_path(value)
    if normalized:
        args.extend([option, normalized])


def _append_bool_option(args: list[str], option: str, enabled: bool) -> None:
    if enabled:
        args.append(option)


def _ensure_json(args: Sequence[str]) -> list[str]:
    normalized = list(args)
    if "--json" not in normalized:
        normalized.append("--json")
    return normalized


def run_cli_json(
    args: Sequence[str],
    *,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    check: bool = True,
    python_executable: PathLike | None = None,
    env: Mapping[str, str] | None = None,
) -> AiloomResult:
    """Run a local Ailoom CLI command and parse its JSON output.

    This is the stable integration primitive for v1 beta. It intentionally
    executes the same local CLI path that users see in the terminal, which keeps
    IDE plugins and CI wrappers aligned with smoke/release-readiness coverage.
    """

    command_args = _ensure_json(args)
    executable = str(python_executable or sys.executable)
    completed_args = (executable, "-m", "cli", *command_args)
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    run_cwd = str(Path(cwd).resolve() if cwd is not None else Path.cwd().resolve())
    proc = subprocess.run(
        completed_args,
        cwd=run_cwd,
        env=merged_env,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    payload: dict[str, Any]
    try:
        loaded = json.loads(proc.stdout)
        payload = loaded if isinstance(loaded, dict) else {"status": "error", "value": loaded}
    except json.JSONDecodeError:
        payload = {
            "status": "error",
            "error": {
                "code": "invalid_json_output",
                "message": "ailoom command did not emit valid JSON",
            },
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    result = AiloomResult(
        payload=payload,
        returncode=proc.returncode,
        args=tuple(completed_args),
        cwd=run_cwd,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )
    if check and proc.returncode != 0:
        raise AiloomCommandError(result)
    return result


def handoff_project(
    input_dir: PathLike | None = None,
    *,
    output_dir: PathLike | None = None,
    copy: bool = False,
    open_bundle: bool = False,
    force_refresh: bool = False,
    reuse_if_fresh: bool = False,
    fast: bool = False,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    check: bool = True,
) -> AiloomResult:
    """Create or reuse a restore-safe AI/IDE handoff for one project."""

    args = ["handoff"]
    _append_path_option(args, "--input-dir", input_dir)
    _append_path_option(args, "--output-dir", output_dir)
    _append_bool_option(args, "--copy", copy)
    _append_bool_option(args, "--open", open_bundle)
    _append_bool_option(args, "--force-refresh", force_refresh)
    _append_bool_option(args, "--reuse-if-fresh", reuse_if_fresh)
    _append_bool_option(args, "--fast", fast)
    return run_cli_json(args, cwd=cwd, timeout=timeout, check=check)


def quick_bundle(
    input_dir: PathLike | None = None,
    *,
    output_dir: PathLike | None = None,
    copy: bool = False,
    open_bundle: bool = False,
    preview: bool = False,
    force_refresh: bool = False,
    reuse_if_fresh: bool = False,
    fast: bool = False,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    check: bool = True,
) -> AiloomResult:
    """Run the explicit quick bundle workflow for a project."""

    args = ["quick"]
    _append_path_option(args, "--input-dir", input_dir)
    _append_path_option(args, "--output-dir", output_dir)
    _append_bool_option(args, "--copy", copy)
    _append_bool_option(args, "--open", open_bundle)
    _append_bool_option(args, "--preview", preview)
    _append_bool_option(args, "--force-refresh", force_refresh)
    _append_bool_option(args, "--reuse-if-fresh", reuse_if_fresh)
    _append_bool_option(args, "--fast", fast)
    return run_cli_json(args, cwd=cwd, timeout=timeout, check=check)


def get_savings(
    input_dir: PathLike | None = None,
    *,
    write_report: PathLike | None = None,
    force: bool = False,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    check: bool = True,
) -> AiloomResult:
    """Read token savings from the most recent handoff."""

    args = ["savings"]
    _append_path_option(args, "--input-dir", input_dir)
    _append_path_option(args, "--write-report", write_report)
    _append_bool_option(args, "--force", force)
    return run_cli_json(args, cwd=cwd, timeout=timeout, check=check)


def next_action(
    input_dir: PathLike | None = None,
    *,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    check: bool = True,
) -> AiloomResult:
    """Return the next best Ailoom command for the current project state."""

    args = ["next"]
    _append_path_option(args, "--input-dir", input_dir)
    return run_cli_json(args, cwd=cwd, timeout=timeout, check=check)


def doctor_project(
    input_dir: PathLike | None = None,
    *,
    install: bool = False,
    storage: bool = False,
    write_report: PathLike | None = None,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    check: bool = True,
) -> AiloomResult:
    """Run readiness, install, or storage diagnostics."""

    args = ["doctor"]
    _append_path_option(args, "--input-dir", input_dir)
    _append_bool_option(args, "--install", install)
    _append_bool_option(args, "--storage", storage)
    _append_path_option(args, "--write-report", write_report)
    return run_cli_json(args, cwd=cwd, timeout=timeout, check=check)


def safety(
    *,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    check: bool = True,
) -> AiloomResult:
    """Explain local-only safety and share-vs-keep-local boundaries."""

    return run_cli_json(["safety"], cwd=cwd, timeout=timeout, check=check)


def inspect_bundle(
    package_file: PathLike,
    *,
    emit_summary: bool = False,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    check: bool = True,
) -> AiloomResult:
    """Inspect one bundle manifest without restoring the original content."""

    args = ["inspect", "--package-file", str(package_file)]
    _append_bool_option(args, "--emit-summary", emit_summary)
    return run_cli_json(args, cwd=cwd, timeout=timeout, check=check)


def explain_bundle(
    package_file: PathLike,
    *,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    check: bool = True,
) -> AiloomResult:
    """Explain one bundle in human-oriented terms for IDEs or agents."""

    return run_cli_json(["explain", "--package-file", str(package_file)], cwd=cwd, timeout=timeout, check=check)


def restore_bundle(
    package_file: PathLike,
    *,
    output_dir: PathLike | None = None,
    output_file: PathLike | None = None,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    check: bool = True,
) -> AiloomResult:
    """Restore one bundle into an explicit output directory or output file."""

    args = ["restore", "--package-file", str(package_file)]
    _append_path_option(args, "--output-dir", output_dir)
    _append_path_option(args, "--output-file", output_file)
    return run_cli_json(args, cwd=cwd, timeout=timeout, check=check)
