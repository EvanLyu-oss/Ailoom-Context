#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
INSTALL_DIR="${AILOOM_HOME:-${MCP_SKELETON_HOME:-$HOME/.ailoom}}"
VENV_DIR="$INSTALL_DIR/venv"
BIN_DIR="$HOME/.local/bin"
COMMAND_PATH="$BIN_DIR/ailoom"
LEGACY_COMMAND_PATH="$BIN_DIR/mcp-skeleton"
MARKER_FILE="$INSTALL_DIR/.ailoom-install"
READINESS_FILE="$INSTALL_DIR/install-readiness.json"
MODE="install"
SETUP_SHELL=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --update)
      MODE="update"
      ;;
    --uninstall)
      MODE="uninstall"
      ;;
    --setup-shell)
      SETUP_SHELL=1
      ;;
    -h|--help)
      echo "Ailoom Context macOS installer"
      echo ""
      echo "Usage:"
      echo "  sh install.sh                 install Ailoom Context"
      echo "  sh install.sh --setup-shell   install and add ~/.local/bin to ~/.zshrc for future terminals"
      echo "  sh install.sh --update        refresh the installed command from this checkout"
      echo "  sh install.sh --uninstall     remove the installed command and managed venv"
      exit 0
      ;;
    *)
      echo "error: unknown installer option: $1" >&2
      echo "try: sh install.sh --help" >&2
      exit 2
      ;;
  esac
  shift
done

if [ "$MODE" = "uninstall" ]; then
  echo "Ailoom Context uninstaller"
  echo ""
  echo "Command:     $COMMAND_PATH"
  echo "Install dir: $INSTALL_DIR"
  echo ""
  if [ -L "$COMMAND_PATH" ] || [ -f "$COMMAND_PATH" ]; then
    rm -f "$COMMAND_PATH"
    echo "Removed command: $COMMAND_PATH"
  else
    echo "Command already absent: $COMMAND_PATH"
  fi
  if [ -L "$LEGACY_COMMAND_PATH" ] || [ -f "$LEGACY_COMMAND_PATH" ]; then
    rm -f "$LEGACY_COMMAND_PATH"
    echo "Removed legacy command: $LEGACY_COMMAND_PATH"
  fi
  if [ -f "$MARKER_FILE" ]; then
    rm -rf "$INSTALL_DIR"
    echo "Removed managed install dir: $INSTALL_DIR"
  elif [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/pyvenv.cfg" ]; then
    rm -rf "$VENV_DIR"
    rmdir "$INSTALL_DIR" 2>/dev/null || true
    echo "Removed managed virtual environment: $VENV_DIR"
  else
  echo "Install dir was not removed because it is not marked as Ailoom-managed."
  fi
  echo ""
  echo "Uninstalled successfully."
  exit 0
fi

if [ "${PYTHON:-}" ]; then
  PYTHON_BIN="$PYTHON"
else
  PYTHON_BIN=""
  for candidate in python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      if "$candidate" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 10) else 1)
PY
      then
        PYTHON_BIN="$candidate"
        break
      fi
    fi
  done
fi

if [ "$MODE" = "update" ]; then
  echo "Ailoom Context macOS updater"
else
  echo "Ailoom Context macOS installer"
fi
echo ""
echo "Install dir: $INSTALL_DIR"
echo "Command:     $COMMAND_PATH"
echo ""

if [ -z "$PYTHON_BIN" ] || ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "error: Python 3.10+ was not found. Install Python 3.10+ first, or rerun with PYTHON=/path/to/python3.11 sh install.sh." >&2
  exit 2
fi

"$PYTHON_BIN" - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise SystemExit("error: Ailoom Context requires Python 3.10+")
PY

mkdir -p "$INSTALL_DIR" "$BIN_DIR"

if [ "$MODE" = "update" ] && [ -d "$VENV_DIR" ]; then
  echo "Refreshing virtual environment..."
  rm -rf "$VENV_DIR"
else
  echo "Creating virtual environment..."
fi
echo "Using Python: $PYTHON_BIN"
"$PYTHON_BIN" -m venv "$VENV_DIR"

if [ "$MODE" = "update" ]; then
  echo "Updating Ailoom Context..."
else
  echo "Installing Ailoom Context..."
fi
if "$VENV_DIR/bin/python" -m pip install --upgrade pip >/dev/null 2>&1; then
  echo "Pip: upgraded"
else
  echo "Pip: upgrade skipped (continuing with bundled pip)"
fi

INSTALL_METHOD="package_with_metrics"
if "$VENV_DIR/bin/python" -m pip install --no-build-isolation "$ROOT_DIR[context-metrics]" >/dev/null 2>&1; then
  echo "Package install: full package with tokenizer metrics"
elif "$VENV_DIR/bin/python" -m pip install --no-build-isolation "$ROOT_DIR" >/dev/null 2>&1; then
  INSTALL_METHOD="package_core"
  echo "Package install: core package (tokenizer metrics extra unavailable)"
else
  INSTALL_METHOD="source_runner"
  echo "Package install: source runner fallback"
  cat > "$VENV_DIR/bin/ailoom" <<EOF
#!/usr/bin/env sh
PYTHONPATH="$ROOT_DIR\${PYTHONPATH:+:\$PYTHONPATH}" exec "$VENV_DIR/bin/python" -m cli "\$@"
EOF
  cat > "$VENV_DIR/bin/mcp-skeleton" <<EOF
#!/usr/bin/env sh
PYTHONPATH="$ROOT_DIR\${PYTHONPATH:+:\$PYTHONPATH}" exec "$VENV_DIR/bin/python" -m cli "\$@"
EOF
  chmod +x "$VENV_DIR/bin/ailoom" "$VENV_DIR/bin/mcp-skeleton"
fi

printf '%s\n' "managed-by=ailoom" "source=$ROOT_DIR" > "$MARKER_FILE"
ln -sf "$VENV_DIR/bin/ailoom" "$COMMAND_PATH"
ln -sf "$VENV_DIR/bin/mcp-skeleton" "$LEGACY_COMMAND_PATH"

SHELL_PROFILE="$HOME/.zshrc"
SHELL_PROFILE_STATUS="not requested"
if [ "$SETUP_SHELL" = "1" ]; then
  mkdir -p "$(dirname "$SHELL_PROFILE")"
  touch "$SHELL_PROFILE"
  if grep -q "ailoom PATH" "$SHELL_PROFILE"; then
    SHELL_PROFILE_STATUS="already configured"
  else
    {
      echo ""
      echo "# >>> ailoom PATH >>>"
      echo "export PATH=\"$BIN_DIR:\$PATH\""
      echo "# <<< ailoom PATH <<<"
    } >> "$SHELL_PROFILE"
    SHELL_PROFILE_STATUS="updated"
  fi
  PATH="$BIN_DIR:$PATH"
  export PATH
fi

echo ""
if [ "$MODE" = "update" ]; then
  echo "Updated successfully."
else
  echo "Installed successfully."
fi
echo ""
echo "Ailoom Context Install Ready"
echo ""
if "$COMMAND_PATH" version >/dev/null 2>&1; then
  echo "Command check: OK"
else
  echo "Command check: unable to run $COMMAND_PATH version"
fi
if command -v ailoom >/dev/null 2>&1; then
  echo "PATH status: ready - ailoom is available on PATH"
  PATH_STATUS="ready"
  FIRST_RUN_COMMAND="ailoom first-run"
  HANDOFF_COMMAND="ailoom handoff"
  QUICK_COMMAND="ailoom quick"
  VERSION_COMMAND="ailoom version"
  INSTALL_DOCTOR_COMMAND="ailoom doctor --install"
else
  echo "PATH status: needs shell setup - $BIN_DIR is not currently on PATH"
  PATH_STATUS="needs_shell_setup"
  FIRST_RUN_COMMAND="$COMMAND_PATH first-run"
  HANDOFF_COMMAND="$COMMAND_PATH handoff"
  QUICK_COMMAND="$COMMAND_PATH quick"
  VERSION_COMMAND="$COMMAND_PATH version"
  INSTALL_DOCTOR_COMMAND="$COMMAND_PATH doctor --install"
fi
echo "Shell profile: $SHELL_PROFILE_STATUS"
echo "Install mode: $INSTALL_METHOD"
if [ "$SETUP_SHELL" = "1" ]; then
  echo "Shell profile file: $SHELL_PROFILE"
  echo "Restart your terminal or run: export PATH=\"$BIN_DIR:\$PATH\""
fi

"$VENV_DIR/bin/python" - "$READINESS_FILE" "$COMMAND_PATH" "$INSTALL_DIR" "$BIN_DIR" "$PATH_STATUS" "$SHELL_PROFILE_STATUS" "$FIRST_RUN_COMMAND" "$HANDOFF_COMMAND" "$QUICK_COMMAND" "$VERSION_COMMAND" "$INSTALL_DOCTOR_COMMAND" "$SHELL_PROFILE" "$INSTALL_METHOD" <<'PY'
import json
import sys
from pathlib import Path

(
    readiness_file,
    command_path,
    install_dir,
    bin_dir,
    path_status,
    shell_profile_status,
    first_run_command,
    handoff_command,
    quick_command,
    version_command,
    install_doctor_command,
    shell_profile,
    install_method,
) = sys.argv[1:14]

payload = {
    "schema": "ailoom.install-readiness.v1",
    "legacy_schema": "mcp-skeleton.install-readiness.v1",
    "status": "ready",
    "command_path": command_path,
    "install_dir": install_dir,
    "bin_dir": bin_dir,
    "command_check": "ok",
    "path_status": path_status,
    "shell_profile_status": shell_profile_status,
    "shell_profile": shell_profile,
    "install_method": install_method,
    "recommended_first_command_text": first_run_command,
    "recommended_project_command_text": handoff_command,
    "quick_command_text": quick_command,
    "doctor_command_text": f"{command_path} doctor",
    "install_doctor_command_text": install_doctor_command,
    "self_check_command_text": version_command,
    "path_setup_command_text": "sh install.sh --setup-shell",
    "path_export_command_text": f"export PATH=\"{bin_dir}:$PATH\"",
}
Path(readiness_file).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PY
echo "Install readiness file: $READINESS_FILE"
echo ""
echo "Copy/paste next:"
echo "  $FIRST_RUN_COMMAND"
echo ""
echo "Then try your project:"
echo "  $HANDOFF_COMMAND"
echo ""
echo "Optional full bundle command:"
echo "  $QUICK_COMMAND"
echo ""
echo "First run self-check:"
echo "  $VERSION_COMMAND"
echo "  $INSTALL_DOCTOR_COMMAND"
echo "  $COMMAND_PATH doctor"
echo ""
echo "Install doctor:"
echo "  $INSTALL_DOCTOR_COMMAND"
echo ""
echo "Self-check command:"
echo "  $VERSION_COMMAND"
echo ""
echo "If command is not found later:"
echo "  Restart your terminal, or run:"
echo "    export PATH=\"$BIN_DIR:\$PATH\""
echo "PATH fix command:"
echo "  sh install.sh --setup-shell"
echo ""
echo "Useful checks:"
echo "  $VERSION_COMMAND"
echo "  $INSTALL_DOCTOR_COMMAND"
echo "  $COMMAND_PATH doctor"
echo ""
if ! printf '%s' "$PATH" | grep -q "$BIN_DIR"; then
  echo "Note: $BIN_DIR is not currently in PATH."
  echo "One-command future shell setup:"
  echo "  sh install.sh --setup-shell"
  echo "Add this to your shell profile:"
  echo "  export PATH=\"$BIN_DIR:\$PATH\""
fi
