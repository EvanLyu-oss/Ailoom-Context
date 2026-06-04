# Ailoom Context Beta Testing

Beta users: start here.

This checklist is designed for real users testing Ailoom Context on macOS or Windows. It focuses on installation, first-run confidence, token savings, restore safety, and whether the handoff feels fast enough for daily development.

## 1. Install

macOS:

```bash
sh install.sh --setup-shell
ailoom doctor --install
```

Windows PowerShell:

```powershell
.\install.ps1 -SetupShell
ailoom doctor --install
```

Expected result:

- install completes without manual Python debugging
- `doctor --install` explains whether PATH and Python are ready
- the next command is obvious

## 2. Safe Demo

```bash
ailoom demo
```

Expected result:

- `Restore safety: OK`
- source tokens and skeleton tokens are visible
- estimated token savings are visible
- restore and inspect commands are printed

## 3. Real Project Handoff

Run this from a real project directory:

```bash
ailoom handoff --copy --open
ailoom savings --write-report ailoom-savings-report.md
```

Expected result:

- `context_skeleton.mcp` is the file to share with AI or an IDE
- restore package files are clearly marked as keep-local
- the savings report contains source tokens, skeleton tokens, tokens saved, and savings percent

## 4. Restore verification

Use the restore command printed by `handoff` or `quick`, and restore into a safe temporary directory.

Expected result:

- restore status is `ok`
- no missing files
- no mismatched files
- original source is not overwritten

## 5. Reuse and Speed

Run handoff again without changing the project:

```bash
ailoom handoff --reuse-if-fresh
ailoom savings
```

Expected result:

- the previous fresh bundle is reused
- the second run feels much faster
- output explains why reuse happened

## 6. Feedback Package

Please send:

- OS and Python version
- install method
- first `ailoom doctor --install` result
- first `ailoom handoff` result
- `ailoom savings --write-report ailoom-savings-report.md` output
- whether speed felt acceptable
- whether the safety boundary was clear

Use [FEEDBACK_TEMPLATE.md](../FEEDBACK_TEMPLATE.md).
