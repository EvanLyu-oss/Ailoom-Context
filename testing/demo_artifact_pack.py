from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "testing" / "results" / "demo-artifact-pack"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _run_json(args: list[str], *, cwd: Path) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    env["MCP_SKELETON_IGNORE_CWD_CONFIG"] = "1"
    proc = subprocess.run(
        [sys.executable, "-m", "cli", *args, "--json"],
        cwd=str(cwd),
        env=env,
        text=True,
        capture_output=True,
    )
    try:
        payload = json.loads(proc.stdout)
        if not isinstance(payload, dict):
            payload = {"status": "error", "value": payload}
    except json.JSONDecodeError:
        payload = {
            "status": "error",
            "error": {
                "code": "invalid_json_output",
                "message": "command did not emit JSON",
            },
            "stdout_tail": proc.stdout[-1200:],
        }
    payload["_command"] = " ".join([sys.executable, "-m", "cli", *args, "--json"])
    payload["_returncode"] = proc.returncode
    payload["_stderr_tail"] = proc.stderr[-1200:] if proc.stderr else ""
    return payload


def _create_demo_source(output_dir: Path) -> Path:
    source = output_dir / "source"
    if source.exists():
        shutil.rmtree(source)
    (source / "src").mkdir(parents=True)
    (source / "notes").mkdir()
    (source / "src" / "agent_workflow.py").write_text(
        "from pathlib import Path\n\n"
        "def collect_context(root: Path) -> list[str]:\n"
        "    return [path.name for path in root.rglob('*.py')]\n\n"
        "def summarize_context(root: Path) -> str:\n"
        "    return ', '.join(collect_context(root))\n",
        encoding="utf-8",
    )
    (source / "README.md").write_text(
        "# Demo Project\n\n"
        + "This project simulates an AI coding workflow where context reading gets expensive as the project grows.\n\n" * 140,
        encoding="utf-8",
    )
    (source / "notes" / "architecture.md").write_text(
        "# Architecture Notes\n\n"
        + "Ailoom creates an AI-facing skeleton while keeping exact restore files local.\n\n" * 110,
        encoding="utf-8",
    )
    return source


def _snippet_from_payloads(payloads: dict[str, dict[str, Any]]) -> str:
    handoff = payloads["handoff"]
    savings = payloads["savings"]
    safety = payloads["safety"]
    clean = payloads["clean_preview"]
    handoff_info = handoff.get("handoff") or {}
    value = handoff.get("value_summary") or {}
    token_savings = value.get("token_savings") or {}
    lines = [
        "# Ailoom Demo Screenshot Notes",
        "",
        "## Handoff",
        "",
        f"- Restore safety: {'OK' if handoff.get('restore_safe') else 'CHECK'}",
        f"- Skeleton: `{handoff_info.get('skeleton_file', '')}`",
        f"- AI handoff prompt: `{handoff_info.get('ai_handoff_file', '')}`",
        f"- Keep local manifest: `{handoff.get('manifest_file', '')}`",
        "",
        "## Savings",
        "",
        f"- Source tokens: `{savings.get('source_tokens', token_savings.get('source_tokens', 0))}`",
        f"- Skeleton tokens: `{savings.get('skeleton_tokens', token_savings.get('skeleton_tokens', 0))}`",
        f"- Tokens saved: `{savings.get('tokens_saved', token_savings.get('tokens_saved', 0))}`",
        f"- Savings percent: `{savings.get('savings_percent', token_savings.get('savings_percent', 0))}%`",
        "",
        "## Safety",
        "",
        f"- Local-only processing: `{(safety.get('guarantees') or {}).get('local_only_processing', False)}`",
        f"- No telemetry: `{(safety.get('guarantees') or {}).get('no_telemetry', False)}`",
        "",
        "## Cleanup",
        "",
        f"- Clean status: `{clean.get('clean_status', clean.get('status', ''))}`",
        f"- Reclaimable bytes: `{clean.get('total_bytes', 0)}`",
        "",
        "## Copyable Caption",
        "",
        "Ailoom Context turns a large project into a compact AI-facing skeleton, while exact restore files stay local.",
    ]
    return "\n".join(lines) + "\n"


def _social_caption(payloads: dict[str, dict[str, Any]]) -> str:
    handoff = payloads["handoff"]
    savings = payloads["savings"]
    handoff_info = handoff.get("handoff") or {}
    lines = [
        "Ailoom Context beta demo",
        "",
        "I am building a local-first context compression tool for AI coding agents.",
        "",
        "What it does:",
        "- turns a project into a compact AI-facing skeleton",
        "- keeps exact restore files local",
        "- shows token savings and restore safety",
        "- no telemetry and no source upload",
        "",
        "Demo result:",
        f"- Restore safety: {'OK' if handoff.get('restore_safe') else 'CHECK'}",
        f"- Source tokens: {savings.get('source_tokens', 0)}",
        f"- Skeleton tokens: {savings.get('skeleton_tokens', 0)}",
        f"- Tokens saved: {savings.get('tokens_saved', 0)}",
        f"- Savings: {savings.get('savings_percent', 0)}%",
        "",
        "Files:",
        f"- Give AI: {handoff_info.get('skeleton_file', 'context_skeleton.mcp')}",
        f"- Keep local: {handoff.get('manifest_file', 'context_manifest.json')}",
        "",
        "GitHub:",
        "https://github.com/EvanLyu-oss/Ailoom-Context",
        "",
        "Author:",
        "Evan <carwyn910@gmail.com>",
    ]
    return "\n".join(lines) + "\n"


def _recording_runbook(payloads: dict[str, dict[str, Any]]) -> str:
    handoff = payloads["handoff"]
    savings = payloads["savings"]
    clean = payloads["clean_preview"]
    handoff_info = handoff.get("handoff") or {}
    lines = [
        "# Ailoom Two-Minute Recording Runbook",
        "",
        "Use this as a tight recording checklist. Do not show private source files, restore package contents, `.env` files, or customer data.",
        "",
        "## Shot 1: Positioning",
        "",
        "Say: Ailoom Context is a local-first context compression tool for AI coding agents.",
        "",
        "Show:",
        "",
        "```bash",
        "ailoom version",
        "```",
        "",
        "## Shot 2: Handoff",
        "",
        "Show the `Restore safety`, `Give AI`, and `Keep local` lines.",
        "",
        "```bash",
        "ailoom handoff --copy --open",
        "```",
        "",
        "Expected demo file paths:",
        "",
        f"- Skeleton: `{handoff_info.get('skeleton_file', '')}`",
        f"- AI prompt: `{handoff_info.get('ai_handoff_file', '')}`",
        f"- Manifest kept local: `{handoff.get('manifest_file', '')}`",
        "",
        "## Shot 3: Token Value",
        "",
        "```bash",
        "ailoom savings",
        "```",
        "",
        f"- Source tokens: `{savings.get('source_tokens', 0)}`",
        f"- Skeleton tokens: `{savings.get('skeleton_tokens', 0)}`",
        f"- Tokens saved: `{savings.get('tokens_saved', 0)}`",
        f"- Savings percent: `{savings.get('savings_percent', 0)}%`",
        "",
        "## Shot 4: Safety Boundary",
        "",
        "```bash",
        "ailoom safety",
        "```",
        "",
        "Point out: local-only, no telemetry, AI-facing skeleton, restore files kept local.",
        "",
        "## Shot 5: Cleanup",
        "",
        "```bash",
        "ailoom doctor --storage",
        "ailoom clean --dry-run --all",
        "```",
        "",
        f"- Clean preview status: `{clean.get('clean_status', clean.get('status', ''))}`",
        f"- Reclaimable bytes in demo: `{clean.get('total_bytes', 0)}`",
        "",
        "## Closing Line",
        "",
        "Ailoom reduces context pressure for large AI coding workflows without giving up local exact restore.",
        "",
        "Repository: https://github.com/EvanLyu-oss/Ailoom-Context",
        "Author: Evan <carwyn910@gmail.com>",
    ]
    return "\n".join(lines) + "\n"


def build_demo_pack(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = Path(args.output_dir or DEFAULT_OUTPUT_DIR).resolve()
    if output_dir.exists() and args.force:
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    source = Path(args.input_dir).resolve() if args.input_dir else _create_demo_source(output_dir)
    bundle_dir = output_dir / "handoff_bundle"
    payloads = {
        "version": _run_json(["version"], cwd=source),
        "handoff": _run_json(["handoff", "--input-dir", str(source), "--output-dir", str(bundle_dir)], cwd=source),
        "savings": _run_json(["savings", "--input-dir", str(source)], cwd=source),
        "next": _run_json(["next", "--input-dir", str(source)], cwd=source),
        "safety": _run_json(["safety"], cwd=source),
        "clean_preview": _run_json(["clean", "--dry-run", "--all", "--input-dir", str(source)], cwd=source),
    }
    artifacts_dir = output_dir / "artifacts"
    for name, payload in payloads.items():
        _write_json(artifacts_dir / f"{name}.json", payload)
    screenshot_notes = output_dir / "DEMO_SCREENSHOT_NOTES.md"
    screenshot_notes.write_text(_snippet_from_payloads(payloads), encoding="utf-8")
    social_caption = output_dir / "SOCIAL_CAPTION.md"
    social_caption.write_text(_social_caption(payloads), encoding="utf-8")
    recording_runbook = output_dir / "RECORDING_RUNBOOK.md"
    recording_runbook.write_text(_recording_runbook(payloads), encoding="utf-8")
    status = "ok" if all(payload.get("_returncode") == 0 for payload in payloads.values()) else "error"
    summary = {
        "status": status,
        "entrypoint": "demo-artifact-pack",
        "source_dir": str(source),
        "output_dir": str(output_dir),
        "bundle_dir": str(bundle_dir),
        "screenshot_notes": str(screenshot_notes),
        "social_caption": str(social_caption),
        "recording_runbook": str(recording_runbook),
        "artifacts": {name: str(artifacts_dir / f"{name}.json") for name in payloads},
        "handoff_restore_safe": bool(payloads["handoff"].get("restore_safe")),
        "savings_percent": payloads["savings"].get("savings_percent", 0),
        "local_only": bool((payloads["safety"].get("guarantees") or {}).get("local_only_processing")),
        "no_telemetry": bool((payloads["safety"].get("guarantees") or {}).get("no_telemetry")),
        "recommended_post_line": "Ailoom Context turns large projects into compact AI-facing skeletons while keeping exact restore files local.",
    }
    _write_json(output_dir / "demo_artifact_pack.json", summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate local demo artifacts for Ailoom Context screenshots/videos.")
    parser.add_argument("--input-dir", help="Existing project directory. Defaults to a generated demo project.")
    parser.add_argument("--output-dir", help="Output directory for demo artifacts.")
    parser.add_argument("--force", action="store_true", help="Replace --output-dir if it already exists.")
    parser.add_argument("--json", action="store_true", help="Emit summary JSON to stdout.")
    args = parser.parse_args(argv)
    payload = build_demo_pack(args)
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(Path(payload["screenshot_notes"]).read_text(encoding="utf-8"))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
