from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "testing" / "results"
DEFAULT_RESULTS_JSON = RESULTS_DIR / "quickstart_check.json"


def _python310_plus() -> str:
    candidates = [sys.executable, "python3.12", "python3.11", "python3.10", "python3"]
    for candidate in candidates:
        try:
            proc = subprocess.run(
                [
                    candidate,
                    "-c",
                    "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)",
                ],
                text=True,
                capture_output=True,
            )
        except FileNotFoundError:
            continue
        if proc.returncode == 0:
            return candidate
    raise RuntimeError("Python 3.10+ is required for quickstart checks")


def _run(args: list[str], *, cwd: Path, env: dict[str, str]) -> dict[str, Any]:
    proc = subprocess.run(args, cwd=str(cwd), env=env, text=True, capture_output=True)
    return {
        "args": args,
        "returncode": proc.returncode,
        "passed": proc.returncode == 0,
        "stdout": proc.stdout,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
    }


def _json_from_command(args: list[str], *, cwd: Path, env: dict[str, str]) -> tuple[dict[str, Any], dict[str, Any]]:
    result = _run(args, cwd=cwd, env=env)
    try:
        parsed = json.loads(str(result.get("stdout") or "{}"))
    except json.JSONDecodeError:
        parsed = {}
    result.pop("stdout", None)
    return result, parsed


def build_quickstart_check_payload() -> dict[str, Any]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if shutil.which("sh") is None:
        payload = {
            "status": "ok",
            "entrypoint": "quickstart-check",
            "runner": "python",
            "platform": sys.platform,
            "check_count": 0,
            "passed": 0,
            "failed": 0,
            "skipped": True,
            "skip_reason": "sh is not available; macOS installer quickstart is skipped on this platform",
            "checks": {},
            "artifacts": {"results_json": str(DEFAULT_RESULTS_JSON)},
        }
        DEFAULT_RESULTS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return payload
    with tempfile.TemporaryDirectory(prefix="mcp_skeleton_quickstart.") as tmp:
        workspace = Path(tmp)
        home = workspace / "home"
        project = workspace / "project"
        home.mkdir()
        (project / "src").mkdir(parents=True)
        (project / "src" / "app.py").write_text(
            "def run() -> str:\n"
            "    return 'quickstart-ready'\n",
            encoding="utf-8",
        )
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["AILOOM_HOME"] = str(home / ".ailoom")
        env["PYTHON"] = _python310_plus()
        env["PYTHONPATH"] = str(ROOT)
        env["MCP_SKELETON_IGNORE_CWD_CONFIG"] = "1"
        env["PATH"] = f"{home / '.local' / 'bin'}{os.pathsep}{env.get('PATH', '')}"

        command_path = home / ".local" / "bin" / "ailoom"
        install = _run(["sh", str(ROOT / "install.sh"), "--setup-shell"], cwd=ROOT, env=env)
        install.pop("stdout", None)
        first_run, first_run_json = _json_from_command(
            [str(command_path), "first-run", "--output-dir", str(workspace / "first-run"), "--json"],
            cwd=project,
            env=env,
        )
        demo, demo_json = _json_from_command(
            [str(command_path), "demo", "--output-dir", str(workspace / "demo"), "--json"],
            cwd=project,
            env=env,
        )
        handoff, handoff_json = _json_from_command(
            [str(command_path), "handoff", "--output-dir", str(workspace / "handoff_bundle"), "--json"],
            cwd=project,
            env=env,
        )
        quick, quick_json = _json_from_command(
            [str(command_path), "quick", "--output-dir", str(workspace / "bundle"), "--json"],
            cwd=project,
            env=env,
        )
        reuse, reuse_json = _json_from_command(
            [
                str(command_path),
                "handoff",
                "--json",
            ],
            cwd=project,
            env=env,
        )

        install_passed = bool(install["passed"] and command_path.exists() and "Ailoom Context Install Ready" in install["stdout_tail"])
        readiness_file = home / ".ailoom" / "install-readiness.json"
        readiness_json = json.loads(readiness_file.read_text(encoding="utf-8")) if readiness_file.exists() else {}
        readiness_passed = bool(
            readiness_json.get("schema") == "ailoom.install-readiness.v1"
            and readiness_json.get("status") == "ready"
            and readiness_json.get("command_path") == str(command_path)
            and str(readiness_json.get("recommended_first_command_text") or "").endswith("first-run")
            and str(readiness_json.get("recommended_project_command_text") or "").endswith("handoff")
        )
        first_run_passed = bool(
            first_run["passed"]
            and first_run_json.get("first_run_status") in {"ready", "watch"}
            and first_run_json.get("demo_status") == "ready"
            and first_run_json.get("restore_safe")
            and (first_run_json.get("token_savings") or {}).get("estimated_savings_percent", 0) > 0
            and Path(str(first_run_json.get("skeleton_file") or "")).exists()
        )
        demo_passed = bool(demo["passed"] and demo_json.get("demo_status") == "ready" and (demo_json.get("quick") or {}).get("restore_safe"))
        handoff_passed = bool(
            handoff["passed"]
            and handoff_json.get("quick_status") == "ready"
            and handoff_json.get("restore_safe")
            and Path(str((handoff_json.get("handoff") or {}).get("ai_file") or "")).exists()
            and Path(str((handoff_json.get("handoff") or {}).get("ai_handoff_file") or "")).exists()
        )
        quick_passed = bool(
            quick["passed"]
            and quick_json.get("quick_status") == "ready"
            and quick_json.get("restore_safe")
            and Path(str(quick_json.get("manifest_file") or "")).exists()
        )
        reuse_passed = bool(
            reuse["passed"]
            and reuse_json.get("reuse_status") == "reused"
            and reuse_json.get("freshness_status") == "fresh"
        )
        checks = {
            "install_sh": {
                **install,
                "passed": install_passed and readiness_passed,
                "command_exists": command_path.exists(),
                "has_ready_panel": "Ailoom Context Install Ready" in install["stdout_tail"],
                "shell_profile_updated": "Shell profile:" in install["stdout_tail"],
                "readiness_file_exists": readiness_file.exists(),
                "readiness_status": readiness_json.get("status", ""),
                "readiness_recommended_first_command": readiness_json.get("recommended_first_command_text", ""),
            },
            "ailoom_first_run": {
                **first_run,
                "passed": first_run_passed,
                "first_run_status": first_run_json.get("first_run_status", ""),
                "demo_status": first_run_json.get("demo_status", ""),
                "restore_safe": bool(first_run_json.get("restore_safe")),
                "skeleton_file_exists": Path(str(first_run_json.get("skeleton_file") or "")).exists(),
            },
            "ailoom_demo": {
                **demo,
                "passed": demo_passed,
                "demo_status": demo_json.get("demo_status", ""),
                "restore_safe": bool((demo_json.get("quick") or {}).get("restore_safe")),
            },
            "ailoom_handoff": {
                **handoff,
                "passed": handoff_passed,
                "quick_status": handoff_json.get("quick_status", ""),
                "restore_safe": bool(handoff_json.get("restore_safe")),
                "ai_file_exists": Path(str((handoff_json.get("handoff") or {}).get("ai_file") or "")).exists(),
                "ai_handoff_file_exists": Path(str((handoff_json.get("handoff") or {}).get("ai_handoff_file") or "")).exists(),
            },
            "ailoom_quick": {
                **quick,
                "passed": quick_passed,
                "quick_status": quick_json.get("quick_status", ""),
                "restore_safe": bool(quick_json.get("restore_safe")),
                "manifest_exists": Path(str(quick_json.get("manifest_file") or "")).exists(),
            },
            "ailoom_handoff_auto_reuse": {
                **reuse,
                "passed": reuse_passed,
                "quick_status": reuse_json.get("quick_status", ""),
                "reuse_status": reuse_json.get("reuse_status", ""),
                "freshness_status": reuse_json.get("freshness_status", ""),
            },
        }

    passed = all(bool(item.get("passed")) for item in checks.values())
    payload = {
        "status": "ok" if passed else "error",
        "entrypoint": "quickstart-check",
        "runner": "python",
        "platform": sys.platform,
        "check_count": len(checks),
        "passed": sum(1 for item in checks.values() if item.get("passed")),
        "failed": sum(1 for item in checks.values() if not item.get("passed")),
        "checks": checks,
        "artifacts": {"results_json": str(DEFAULT_RESULTS_JSON)},
    }
    DEFAULT_RESULTS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    payload = build_quickstart_check_payload()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
