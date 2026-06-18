from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS_DIR = ROOT / "testing" / "results" / "competitive-benchmark"
DEFAULT_SKIP_DIRS = {
    ".git",
    ".workspace_ail",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".venv",
    "venv",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "mcp-skeleton-restore",
    "test-results",
    "testing/results",
}
TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".css",
    ".html",
    ".sh",
}


def _estimate_tokens(text: str) -> int:
    return max(1, int(round(len(text) / 4))) if text else 0


def _elapsed_ms(started_at: float) -> float:
    return round((time.perf_counter() - started_at) * 1000.0, 2)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _run_json_cli(args: list[str], *, cwd: Path) -> tuple[dict[str, Any], int, float, str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    env["MCP_SKELETON_IGNORE_CWD_CONFIG"] = "1"
    started_at = time.perf_counter()
    proc = subprocess.run(
        [sys.executable, "-m", "cli", *args, "--json"],
        cwd=str(cwd),
        env=env,
        text=True,
        capture_output=True,
    )
    elapsed_ms = _elapsed_ms(started_at)
    try:
        payload = json.loads(proc.stdout)
        if not isinstance(payload, dict):
            payload = {"status": "error", "value": payload}
    except json.JSONDecodeError:
        payload = {
            "status": "error",
            "error": {
                "code": "invalid_json_output",
                "message": "command did not emit valid JSON",
            },
        }
    return payload, proc.returncode, elapsed_ms, proc.stdout, proc.stderr


def _create_fixture(root: Path) -> Path:
    fixture = root / "fixture"
    if fixture.exists():
        shutil.rmtree(fixture)
    (fixture / "src").mkdir(parents=True)
    (fixture / "docs").mkdir()
    (fixture / "node_modules" / "ignored").mkdir(parents=True)
    (fixture / "src" / "app.py").write_text(
        "import json\n\n"
        "def summarize(items: list[str]) -> dict[str, int]:\n"
        "    return {item: len(item) for item in items}\n\n"
        "def run() -> str:\n"
        "    return json.dumps(summarize(['ailoom', 'context', 'benchmark']))\n",
        encoding="utf-8",
    )
    (fixture / "src" / "worker.py").write_text(
        "class Worker:\n"
        "    def __init__(self, name: str) -> None:\n"
        "        self.name = name\n\n"
        "    def execute(self) -> str:\n"
        "        return f'worker:{self.name}'\n",
        encoding="utf-8",
    )
    (fixture / "README.md").write_text(
        "# Competitive Benchmark Fixture\n\n"
        + "Ailoom Context should produce a compact AI-facing skeleton while keeping restore files local.\n\n" * 120,
        encoding="utf-8",
    )
    (fixture / "docs" / "guide.md").write_text(
        "# Guide\n\n" + "This guide simulates a medium documentation surface for an AI coding agent.\n\n" * 100,
        encoding="utf-8",
    )
    (fixture / ".env.example").write_text(
        "API_KEY=sk-demo-secret-should-be-redacted\nDATABASE_URL=postgres://user:pass@example.local/db\n",
        encoding="utf-8",
    )
    (fixture / "node_modules" / "ignored" / "large.js").write_text(
        "console.log('ignored dependency');\n" * 500,
        encoding="utf-8",
    )
    return fixture


def _iter_source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, dirs, filenames in os.walk(root):
        current_path = Path(current)
        rel_dir = current_path.relative_to(root).as_posix()
        dirs[:] = [
            item
            for item in dirs
            if item not in DEFAULT_SKIP_DIRS and f"{rel_dir}/{item}".strip("/") not in DEFAULT_SKIP_DIRS
        ]
        for filename in filenames:
            path = current_path / filename
            if path.suffix.lower() in TEXT_EXTENSIONS or filename.startswith(".env"):
                files.append(path)
    return sorted(files)


def _raw_concat_benchmark(input_dir: Path, output_dir: Path) -> dict[str, Any]:
    started_at = time.perf_counter()
    files = _iter_source_files(input_dir)
    chunks: list[str] = []
    source_bytes = 0
    for path in files:
        data = path.read_bytes()
        source_bytes += len(data)
        text = data.decode("utf-8", errors="replace")
        rel = path.relative_to(input_dir).as_posix()
        chunks.append(f"\n--- file: {rel} ---\n{text}")
    output_text = "\n".join(chunks)
    raw_output = output_dir / "raw_concat.txt"
    raw_output.parent.mkdir(parents=True, exist_ok=True)
    raw_output.write_text(output_text, encoding="utf-8")
    return {
        "tool": "raw_concat",
        "status": "ok",
        "command": "internal raw concat baseline",
        "output_file": str(raw_output),
        "file_count": len(files),
        "source_bytes": source_bytes,
        "output_bytes": raw_output.stat().st_size,
        "output_tokens": _estimate_tokens(output_text),
        "runtime_ms": _elapsed_ms(started_at),
        "restore_fidelity": "not-supported",
        "local_only": True,
        "notes": "raw concatenation baseline; no exact restore package",
    }


def _ailoom_benchmark(input_dir: Path, output_dir: Path) -> dict[str, Any]:
    bundle_dir = output_dir / "ailoom_bundle"
    restore_dir = output_dir / "ailoom_restore"
    payload, returncode, runtime_ms, stdout, stderr = _run_json_cli(
        ["handoff", "--input-dir", str(input_dir), "--output-dir", str(bundle_dir)],
        cwd=input_dir,
    )
    skeleton_file = Path(((payload.get("handoff") or {}).get("skeleton_file") or bundle_dir / "context_skeleton.mcp"))
    manifest_file = Path(str(payload.get("manifest_file") or bundle_dir / "context_manifest.json"))
    restore_payload: dict[str, Any] = {}
    restore_returncode = -1
    if returncode == 0 and manifest_file.exists():
        restore_payload, restore_returncode, _, _, _ = _run_json_cli(
            ["restore", "--package-file", str(manifest_file), "--output-dir", str(restore_dir)],
            cwd=input_dir,
        )
    skeleton_text = skeleton_file.read_text(encoding="utf-8", errors="replace") if skeleton_file.exists() else ""
    value_summary = payload.get("value_summary") or {}
    token_savings = value_summary.get("token_savings") or {}
    return {
        "tool": "ailoom",
        "status": "ok" if returncode == 0 else "error",
        "command": f"ailoom handoff --input-dir {input_dir} --output-dir {bundle_dir} --json",
        "returncode": returncode,
        "runtime_ms": runtime_ms,
        "bundle_dir": str(bundle_dir),
        "skeleton_file": str(skeleton_file),
        "manifest_file": str(manifest_file),
        "output_bytes": skeleton_file.stat().st_size if skeleton_file.exists() else 0,
        "output_tokens": int(token_savings.get("skeleton_tokens") or _estimate_tokens(skeleton_text)),
        "source_tokens": int(token_savings.get("source_tokens") or 0),
        "tokens_saved": int(token_savings.get("tokens_saved") or 0),
        "savings_percent": float(token_savings.get("savings_percent") or 0.0),
        "restore_fidelity": "ok" if restore_returncode == 0 and restore_payload.get("status") == "ok" else "unknown",
        "restore_returncode": restore_returncode,
        "restore_status": restore_payload.get("status", ""),
        "local_only": True,
        "redaction_boundary": "AI-facing skeleton redacts common secret shapes; restore package stays local",
        "stderr_tail": stderr[-1200:] if stderr else "",
        "stdout_tail": stdout[-1200:] if stdout else "",
    }


def _external_tool_status(name: str, *, run_external_tools: bool) -> dict[str, Any]:
    path = shutil.which(name)
    if not path:
        return {
            "tool": name,
            "status": "skipped",
            "reason": f"{name} was not found on PATH",
            "detected": False,
        }
    if not run_external_tools:
        return {
            "tool": name,
            "status": "detected-not-run",
            "path": path,
            "detected": True,
            "reason": "external tools are not executed unless --run-external-tools is set",
        }
    started_at = time.perf_counter()
    proc = subprocess.run([path, "--version"], text=True, capture_output=True)
    return {
        "tool": name,
        "status": "version-checked" if proc.returncode == 0 else "error",
        "path": path,
        "detected": True,
        "returncode": proc.returncode,
        "runtime_ms": _elapsed_ms(started_at),
        "stdout_tail": proc.stdout[-1200:],
        "stderr_tail": proc.stderr[-1200:],
        "note": "first MVP only records external tool availability/version; full tool-specific runs come later",
    }


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Competitive Benchmark Report",
        "",
        f"- Status: `{payload['status']}`",
        f"- Fixture: `{payload['fixture_dir']}`",
        f"- Platform: `{payload['environment']['platform']}`",
        f"- Python: `{payload['environment']['python']}`",
        "",
        "## Results",
        "",
        "| Tool | Status | Output tokens | Output bytes | Runtime ms | Restore | Notes |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for result in payload["results"]:
        lines.append(
            "| {tool} | {status} | {tokens} | {bytes} | {runtime} | {restore} | {notes} |".format(
                tool=result.get("tool", ""),
                status=result.get("status", ""),
                tokens=result.get("output_tokens", ""),
                bytes=result.get("output_bytes", ""),
                runtime=result.get("runtime_ms", ""),
                restore=result.get("restore_fidelity", ""),
                notes=str(result.get("notes") or result.get("reason") or result.get("redaction_boundary") or "").replace("|", "/"),
            )
        )
    summary = payload.get("summary") or {}
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Ailoom vs raw token ratio: `{summary.get('ailoom_vs_raw_token_ratio', '')}`",
            f"- Ailoom restore fidelity: `{summary.get('ailoom_restore_fidelity', '')}`",
            f"- External tools checked: `{', '.join(summary.get('external_tools', []))}`",
            "",
            "This benchmark is local-only and reproducible. It should be treated as observed data, not a universal claim.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_benchmark_payload(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = Path(args.output_dir or DEFAULT_RESULTS_DIR).resolve()
    if output_dir.exists() and args.force:
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.input_dir:
        fixture_dir = Path(args.input_dir).resolve()
    else:
        fixture_dir = _create_fixture(output_dir)
    raw = _raw_concat_benchmark(fixture_dir, output_dir)
    ailoom = _ailoom_benchmark(fixture_dir, output_dir)
    external = [
        _external_tool_status("repomix", run_external_tools=args.run_external_tools),
        _external_tool_status("repopack", run_external_tools=args.run_external_tools),
    ]
    raw_tokens = int(raw.get("output_tokens") or 0)
    ailoom_tokens = int(ailoom.get("output_tokens") or 0)
    ratio = round(ailoom_tokens / raw_tokens, 4) if raw_tokens else 0.0
    payload = {
        "status": "ok" if ailoom.get("status") == "ok" and raw.get("status") == "ok" else "error",
        "entrypoint": "competitive-benchmark",
        "fixture_dir": str(fixture_dir),
        "output_dir": str(output_dir),
        "environment": {
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            "local_only": True,
        },
        "results": [ailoom, raw, *external],
        "summary": {
            "ailoom_vs_raw_token_ratio": ratio,
            "ailoom_restore_fidelity": ailoom.get("restore_fidelity"),
            "raw_restore_fidelity": raw.get("restore_fidelity"),
            "external_tools": [item["tool"] for item in external],
            "claim_guidance": "use observed/local/reproducible wording; avoid universal competitor claims",
        },
    }
    output_json = Path(args.output_json or output_dir / "competitive_benchmark.json")
    output_md = Path(args.output_md or output_dir / "competitive_benchmark.md")
    _write_json(output_json, payload)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(_render_markdown(payload), encoding="utf-8")
    payload["artifacts"] = {
        "output_json": str(output_json),
        "output_md": str(output_md),
    }
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a local competitive benchmark for Ailoom Context.")
    parser.add_argument("--input-dir", help="Existing fixture/project directory. Defaults to a generated fixture.")
    parser.add_argument("--output-dir", help="Directory for benchmark artifacts.")
    parser.add_argument("--output-json", help="JSON report path.")
    parser.add_argument("--output-md", help="Markdown report path.")
    parser.add_argument("--run-external-tools", action="store_true", help="Run detected external tool version checks.")
    parser.add_argument("--force", action="store_true", help="Replace --output-dir if it exists.")
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout.")
    args = parser.parse_args(argv)
    payload = build_benchmark_payload(args)
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(_render_markdown(payload))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
