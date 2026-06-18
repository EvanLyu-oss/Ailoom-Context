const cp = require("child_process");
const fs = require("fs");
const path = require("path");
const vscode = require("vscode");

let output;
let statusBar;
let latestHandoff = null;

function workspaceRoot() {
  const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
  if (!folder) {
    throw new Error("Open a workspace folder before running Ailoom Context.");
  }
  return folder.uri.fsPath;
}

function ailoomCommand() {
  return vscode.workspace.getConfiguration("ailoom").get("commandPath", "ailoom");
}

function runAiloom(args, cwd) {
  return new Promise((resolve, reject) => {
    const command = ailoomCommand();
    const fullArgs = [...args, "--json"];
    output.appendLine(`$ ${command} ${fullArgs.join(" ")}`);
    cp.execFile(command, fullArgs, { cwd }, (error, stdout, stderr) => {
      if (stderr) {
        output.appendLine(stderr.trim());
      }
      let payload;
      try {
        payload = JSON.parse(stdout || "{}");
      } catch (parseError) {
        reject(new Error(`Ailoom did not return JSON. Is '${command}' installed and on PATH?`));
        return;
      }
      if (error) {
        const message = payload && payload.error && payload.error.message
          ? payload.error.message
          : error.message;
        reject(new Error(message));
        return;
      }
      resolve(payload);
    });
  });
}

function updateStatusFromSavings(payload) {
  const savings = payload && typeof payload.savings_percent === "number"
    ? `${payload.savings_percent}%`
    : "ready";
  statusBar.text = `Ailoom ${savings}`;
  statusBar.tooltip = "Ailoom Context local handoff status";
  statusBar.show();
}

function appendHandoffSummary(payload) {
  const handoff = payload.handoff || {};
  const value = payload.value_summary || {};
  const tokenSavings = value.token_savings || {};
  output.appendLine("");
  output.appendLine("Ailoom handoff ready");
  output.appendLine(`Restore safety: ${payload.restore_safe ? "OK" : "CHECK"}`);
  output.appendLine(`Created/reused: ${(payload.daily_handoff || {}).status || payload.quick_status || "unknown"}`);
  output.appendLine(`Skeleton: ${handoff.skeleton_file || ""}`);
  output.appendLine(`AI prompt: ${handoff.ai_handoff_file || ""}`);
  output.appendLine(`Manifest: ${payload.manifest_file || ""}`);
  output.appendLine(`Savings: ${tokenSavings.savings_percent || 0}% (${tokenSavings.tokens_saved || 0} tokens)`);
  output.appendLine(`Next: ${(payload.user_outcome || {}).next_command_text || ""}`);
  output.appendLine("");
  output.appendLine("Keep restore packages local. Share the skeleton and AI_HANDOFF.md prompt, not the restore package.");
}

async function handoffWorkspace() {
  const root = workspaceRoot();
  const payload = await runAiloom(["handoff", "--input-dir", root], root);
  latestHandoff = payload;
  appendHandoffSummary(payload);
  updateStatusFromSavings({ savings_percent: ((payload.value_summary || {}).token_savings || {}).savings_percent });
  output.show(true);
  vscode.window.showInformationMessage("Ailoom handoff ready. Open the skeleton or AI handoff prompt from the command palette.");
}

async function showSavings() {
  const root = workspaceRoot();
  const payload = await runAiloom(["savings", "--input-dir", root], root);
  output.appendLine("");
  output.appendLine("Ailoom savings");
  output.appendLine(`Status: ${payload.savings_status || payload.status}`);
  output.appendLine(`Source tokens: ${payload.source_tokens || 0}`);
  output.appendLine(`Skeleton tokens: ${payload.skeleton_tokens || 0}`);
  output.appendLine(`Tokens saved: ${payload.tokens_saved || 0}`);
  output.appendLine(`Savings percent: ${payload.savings_percent || 0}%`);
  output.appendLine(`Agent reading: ${((payload.value_summary || {}).agent_context_reading || {}).message || ""}`);
  updateStatusFromSavings(payload);
  output.show(true);
}

async function openFileFromLatest(kind) {
  if (!latestHandoff) {
    await handoffWorkspace();
  }
  const handoff = (latestHandoff && latestHandoff.handoff) || {};
  const file = kind === "prompt" ? handoff.ai_handoff_file : handoff.skeleton_file;
  if (!file || !fs.existsSync(file)) {
    throw new Error(`Ailoom ${kind} file is not available yet. Run Ailoom: Handoff Current Workspace first.`);
  }
  const doc = await vscode.workspace.openTextDocument(vscode.Uri.file(file));
  await vscode.window.showTextDocument(doc);
}

async function doctor() {
  const root = workspaceRoot();
  const install = await runAiloom(["doctor", "--install"], root);
  const next = await runAiloom(["next", "--input-dir", root], root);
  output.appendLine("");
  output.appendLine("Ailoom doctor");
  output.appendLine(`Install: ${install.install_doctor_status || install.status}`);
  output.appendLine(`Next status: ${next.next_status || ""}`);
  output.appendLine(`Next command: ${next.primary_command_text || ""}`);
  output.show(true);
}

async function cleanPreview() {
  const root = workspaceRoot();
  const payload = await runAiloom(["clean", "--dry-run", "--all", "--input-dir", root], root);
  output.appendLine("");
  output.appendLine("Ailoom clean preview");
  output.appendLine(`Status: ${payload.clean_status || payload.status}`);
  output.appendLine(`Reclaimable bytes: ${payload.total_bytes || 0}`);
  output.appendLine("Cleanup is dry-run only from the VS Code MVP.");
  output.show(true);
}

function register(context, command, callback) {
  context.subscriptions.push(vscode.commands.registerCommand(command, async () => {
    try {
      await callback();
    } catch (error) {
      output.appendLine(`Error: ${error.message}`);
      output.show(true);
      vscode.window.showErrorMessage(`Ailoom Context: ${error.message}`);
    }
  }));
}

function activate(context) {
  output = vscode.window.createOutputChannel("Ailoom Context");
  statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  statusBar.text = "Ailoom";
  statusBar.command = "ailoom.handoffWorkspace";
  context.subscriptions.push(output, statusBar);
  statusBar.show();

  register(context, "ailoom.handoffWorkspace", handoffWorkspace);
  register(context, "ailoom.showSavings", showSavings);
  register(context, "ailoom.openSkeleton", () => openFileFromLatest("skeleton"));
  register(context, "ailoom.openHandoffPrompt", () => openFileFromLatest("prompt"));
  register(context, "ailoom.doctor", doctor);
  register(context, "ailoom.cleanPreview", cleanPreview);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
