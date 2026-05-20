from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "testing" / "results"
DEFAULT_RESULTS_JSON = RESULTS_DIR / "cli_smoke_python_results.json"


class SmokeFailure(AssertionError):
    pass


def _run(args: list[str], *, cwd: Path = ROOT, expect: int = 0) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    proc = subprocess.run(
        args,
        cwd=str(cwd),
        env=env,
        text=True,
        capture_output=True,
    )
    if proc.returncode != expect:
        raise SmokeFailure(
            f"command failed: {' '.join(args)}\n"
            f"expected exit {expect}, got {proc.returncode}\n"
            f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc


def _run_cli_json(args: list[str], *, cwd: Path = ROOT, expect: int = 0) -> dict[str, Any]:
    proc = _run([sys.executable, "-m", "cli", *args], cwd=cwd, expect=expect)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise SmokeFailure(f"command did not emit JSON: {' '.join(args)}\nSTDOUT:\n{proc.stdout}") from exc


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_py_compile(workspace: Path) -> None:
    del workspace
    _run(
        [
            sys.executable,
            "-m",
            "py_compile",
            str(ROOT / "cli" / "ail_cli.py"),
            str(ROOT / "cli" / "context_compression.py"),
            str(ROOT / "testing" / "context_scale_benchmark.py"),
        ]
    )


def _check_preset_json(workspace: Path) -> None:
    del workspace
    payload = _run_cli_json(["context", "preset", "--json"])
    assert payload["status"] == "ok"
    assert payload["selected_preset"]["preset_id"] == "generic"
    assert payload["preset_count"] >= 5


def _check_text_restore(workspace: Path) -> None:
    text_file = workspace / "long_text.md"
    text_file.write_text(
        "# MCP Skeleton\n\n"
        "This is a cross-platform smoke paragraph about exact restore and context compression.\n",
        encoding="utf-8",
    )
    bundle_dir = workspace / "text_bundle"
    payload = _run_cli_json(
        [
            "context",
            "compress",
            "--text-file",
            str(text_file),
            "--output-dir",
            str(bundle_dir),
            "--json",
        ]
    )
    assert payload["status"] == "ok"
    assert payload["compression_mode"] == "text"

    restore_file = workspace / "restored_text.md"
    restore = _run_cli_json(
        [
            "context",
            "restore",
            "--package-file",
            str(bundle_dir / "context_manifest.json"),
            "--output-file",
            str(restore_file),
            "--json",
        ]
    )
    assert restore["status"] == "ok"
    assert _sha256(text_file) == _sha256(restore_file)


def _check_non_utf8_text_restore(workspace: Path) -> None:
    source = workspace / "gbk_notes.md"
    source.write_bytes("# 标题\n\n这是 GBK 编码文本，用于测试无损恢复。\n".encode("gb18030"))
    bundle_dir = workspace / "gbk_bundle"
    payload = _run_cli_json(
        [
            "context",
            "compress",
            "--text-file",
            str(source),
            "--output-dir",
            str(bundle_dir),
            "--json",
        ]
    )
    assert payload["status"] == "ok"
    assert payload["source_summary"]["source_encoding"] in {"gb2312", "gb18030"}
    restored = workspace / "gbk_restored.md"
    _run_cli_json(
        [
            "context",
            "restore",
            "--package-file",
            str(bundle_dir / "context_manifest.json"),
            "--output-file",
            str(restored),
            "--json",
        ]
    )
    assert _sha256(source) == _sha256(restored)


def _check_directory_restore(workspace: Path) -> None:
    project = workspace / "project"
    (project / "src").mkdir(parents=True)
    (project / "docs").mkdir()
    (project / "empty" / "leaf").mkdir(parents=True)
    (project / "src" / "app.py").write_text("def run() -> str:\n    return 'alpha'\n", encoding="utf-8")
    (project / "docs" / "notes.md").write_text("# Notes\n\nDirectory restore smoke.\n", encoding="utf-8")
    (project / "assets.bin").write_bytes(bytes(range(32)))

    bundle_dir = workspace / "dir_bundle"
    payload = _run_cli_json(
        [
            "context",
            "compress",
            "--input-dir",
            str(project),
            "--output-dir",
            str(bundle_dir),
            "--json",
        ]
    )
    assert payload["status"] == "ok"
    assert payload["compression_mode"] == "directory"
    assert payload["source_summary"]["total_files"] == 3

    restore_root = workspace / "dir_restore"
    restore = _run_cli_json(
        [
            "context",
            "restore",
            "--package-file",
            str(bundle_dir / "context_manifest.json"),
            "--output-dir",
            str(restore_root),
            "--json",
        ]
    )
    assert restore["status"] == "ok"
    restored_project = restore_root / "project"
    for rel in ["src/app.py", "docs/notes.md", "assets.bin"]:
        assert _sha256(project / rel) == _sha256(restored_project / rel)
    assert (restored_project / "empty" / "leaf").is_dir()


def _check_apply_patch_roundtrip(workspace: Path) -> None:
    source = workspace / "source.md"
    candidate = workspace / "candidate.md"
    source.write_text("# Plan\n\nOriginal context.\n", encoding="utf-8")
    candidate.write_text("# Plan\n\nOriginal context with a safe update.\n", encoding="utf-8")
    bundle_dir = workspace / "patch_source_bundle"
    _run_cli_json(
        [
            "context",
            "compress",
            "--text-file",
            str(source),
            "--output-dir",
            str(bundle_dir),
            "--json",
        ]
    )
    apply_check = _run_cli_json(
        [
            "context",
            "apply-check",
            "--package-file",
            str(bundle_dir / "context_manifest.json"),
            "--text-file",
            str(candidate),
            "--json",
        ]
    )
    assert apply_check["status"] == "ok"
    assert apply_check["apply_check_passed"] is True

    patch_dir = workspace / "patch_bundle"
    patch = _run_cli_json(
        [
            "context",
            "patch",
            "--package-file",
            str(bundle_dir / "context_manifest.json"),
            "--text-file",
            str(candidate),
            "--output-dir",
            str(patch_dir),
            "--json",
        ]
    )
    assert patch["status"] == "ok"

    output_file = workspace / "patched.md"
    replay = _run_cli_json(
        [
            "context",
            "patch-apply",
            "--patch-file",
            str(patch_dir / "patch_manifest.json"),
            "--output-file",
            str(output_file),
            "--json",
        ]
    )
    assert replay["status"] == "ok"
    assert _sha256(candidate) == _sha256(output_file)


def _check_invalid_input_dir(workspace: Path) -> None:
    missing = workspace / "missing"
    payload = _run_cli_json(
        ["context", "compress", "--input-dir", str(missing), "--json"],
        expect=2,
    )
    assert payload["status"] == "error"
    assert payload["error"]["code"] == "invalid_usage"


def _check_scale_benchmark_quick(workspace: Path) -> None:
    output_json = workspace / "benchmark.json"
    output_md = workspace / "benchmark.md"
    proc = _run(
        [
            sys.executable,
            str(ROOT / "testing" / "context_scale_benchmark.py"),
            "--quick",
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
        ],
        cwd=ROOT,
    )
    stdout_payload = json.loads(proc.stdout)
    report = json.loads(output_json.read_text(encoding="utf-8"))
    assert output_md.exists()
    assert stdout_payload["status"] == "ok"
    assert stdout_payload["executive_summary"]["overall_status"] in {"ready", "watch"}
    assert report["status"] == "ok"
    assert report["release_readiness"]["restore_verified_count"] == report["release_readiness"]["case_count"]
    assert report["scale_health"]["status"] in {"ok", "warn"}
    assert report["executive_summary"]["large_directory_recommendations"]
    assert report["executive_summary"]["long_text_recommendations"]


CHECKS: list[tuple[str, Callable[[Path], None]]] = [
    ("py_compile_ok", _check_py_compile),
    ("context_preset_json_ok", _check_preset_json),
    ("context_restore_text_json_ok", _check_text_restore),
    ("context_non_utf8_text_restore_json_ok", _check_non_utf8_text_restore),
    ("context_restore_directory_json_ok", _check_directory_restore),
    ("context_apply_patch_roundtrip_json_ok", _check_apply_patch_roundtrip),
    ("context_invalid_input_dir_json_ok", _check_invalid_input_dir),
    ("context_scale_benchmark_quick_json_ok", _check_scale_benchmark_quick),
]


def run_checks(*, results_json: Path) -> dict[str, Any]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    checks: dict[str, bool] = {}
    failures: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="mcp_skeleton_py_smoke.") as tmp:
        workspace = Path(tmp)
        for name, func in CHECKS:
            try:
                func(workspace)
            except Exception as exc:  # noqa: BLE001 - report all smoke failures as structured JSON
                checks[name] = False
                failures[name] = f"{type(exc).__name__}: {exc}"
            else:
                checks[name] = True
    status = "ok" if all(checks.values()) else "error"
    payload = {
        "status": status,
        "exit_code": 0 if status == "ok" else 1,
        "runner": "python",
        "platform": sys.platform,
        "check_count": len(checks),
        "passed": sum(1 for value in checks.values() if value),
        "failed": sum(1 for value in checks.values() if not value),
        "checks": checks,
        "failures": failures,
    }
    results_json.parent.mkdir(parents=True, exist_ok=True)
    results_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run cross-platform MCP-Skeleton CLI smoke checks.")
    parser.add_argument("--results-json", default=str(DEFAULT_RESULTS_JSON), help="Where to write the smoke result JSON.")
    args = parser.parse_args()
    payload = run_checks(results_json=Path(args.results_json).expanduser())
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return int(payload["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
