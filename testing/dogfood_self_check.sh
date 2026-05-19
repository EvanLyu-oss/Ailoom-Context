#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
ROOT="${AIL_REPO_ROOT:-$(cd -- "${SCRIPT_DIR}/.." && pwd)}"
export AIL_REPO_ROOT="$ROOT"
export PYTHONPATH="$ROOT"

RESULTS_DIR="$ROOT/testing/results"
DOGFOOD_ROOT="$RESULTS_DIR/dogfood-self-check"
BUNDLE_DIR="$DOGFOOD_ROOT/context-bundle"
RESTORE_PARENT="$DOGFOOD_ROOT/restore"
RESTORED_ROOT="$RESTORE_PARENT/$(basename "$ROOT")"
SUMMARY_JSON="$DOGFOOD_ROOT/dogfood_self_check.json"

mkdir -p "$RESULTS_DIR"
rm -rf "$DOGFOOD_ROOT"
mkdir -p "$DOGFOOD_ROOT"

python3 -m cli context bundle \
  --preset codebase \
  --input-dir "$ROOT" \
  --exclude testing/results/ \
  --output-dir "$BUNDLE_DIR" \
  --json > "$DOGFOOD_ROOT/bundle.json"

python3 -m cli context inspect \
  --package-file "$BUNDLE_DIR/context_manifest.json" \
  --json > "$DOGFOOD_ROOT/inspect.json"

python3 -m cli context restore \
  --package-file "$BUNDLE_DIR/context_manifest.json" \
  --output-dir "$RESTORE_PARENT" \
  --json > "$DOGFOOD_ROOT/restore.json"

python3 - "$ROOT" "$RESTORED_ROOT" "$DOGFOOD_ROOT/bundle.json" "$DOGFOOD_ROOT/inspect.json" "$DOGFOOD_ROOT/restore.json" "$SUMMARY_JSON" <<'PY'
import hashlib
import json
import os
import sys
from pathlib import Path

source_root = Path(sys.argv[1]).resolve()
restored_root = Path(sys.argv[2]).resolve()
bundle_json = Path(sys.argv[3])
inspect_json = Path(sys.argv[4])
restore_json = Path(sys.argv[5])
summary_json = Path(sys.argv[6])

skip_dir_names = {".git", "__pycache__", ".pytest_cache"}
excluded_prefixes = {"testing/results"}

bundle = json.loads(bundle_json.read_text(encoding="utf-8"))
inspect = json.loads(inspect_json.read_text(encoding="utf-8"))
restore = json.loads(restore_json.read_text(encoding="utf-8"))

expected_files = []
for current_root, dirnames, filenames in os.walk(source_root):
    current_path = Path(current_root)
    dirnames[:] = [name for name in dirnames if name not in skip_dir_names]
    for filename in sorted(filenames):
        source_path = current_path / filename
        rel_path = source_path.relative_to(source_root).as_posix()
        if any(rel_path == prefix or rel_path.startswith(f"{prefix}/") for prefix in excluded_prefixes):
            continue
        if source_path.is_symlink():
            continue
        expected_files.append(rel_path)

missing = []
mismatched = []
for rel_path in expected_files:
    source_path = source_root / rel_path
    restored_path = restored_root / rel_path
    if not restored_path.exists():
        missing.append(rel_path)
        continue
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    restored_hash = hashlib.sha256(restored_path.read_bytes()).hexdigest()
    if source_hash != restored_hash:
        mismatched.append(rel_path)

source_summary = (bundle.get("compression") or {}).get("source_summary") or {}
payload = {
    "status": "ok" if not missing and not mismatched else "error",
    "entrypoint": "dogfood-self-check",
    "source_root": str(source_root),
    "restored_root": str(restored_root),
    "bundle_status": bundle.get("status"),
    "inspect_status": inspect.get("status"),
    "restore_status": restore.get("status"),
    "included_file_count": int(source_summary.get("total_files", 0) or 0),
    "expected_file_count": len(expected_files),
    "skeleton_char_count": int((bundle.get("compression") or {}).get("skeleton_char_count", 0) or 0),
    "compression_ratio": (bundle.get("compression") or {}).get("compression_ratio", 0),
    "missing_count": len(missing),
    "mismatched_count": len(mismatched),
    "missing_paths": missing[:40],
    "mismatched_paths": mismatched[:40],
    "artifacts": {
        "bundle_json": str(bundle_json),
        "inspect_json": str(inspect_json),
        "restore_json": str(restore_json),
        "summary_json": str(summary_json),
    },
}
summary_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2, ensure_ascii=False))
raise SystemExit(0 if payload["status"] == "ok" else 1)
PY
