# Ailoom Context Beta Feedback Template

Thank you for trying Ailoom Context.

Please copy this template, fill in what you can, and attach any command output that looks relevant.

## Environment

- OS:
- CPU/RAM if known:
- Python version:
- Ailoom Context commit or version:
- Install method:

## Project tested

- Project type:
- Approximate file count:
- Approximate repository size:
- Large generated/dependency folders present:
- Long text/manuscript tested:

## Commands run

```bash
ailoom version
ailoom doctor --install
ailoom handoff
ailoom handoff
ailoom savings
ailoom savings --write-report ailoom-savings-report.md
ailoom safety
```

Add any other commands you tried:

```bash

```

## Results

- Did install complete successfully:
- Did `doctor --install` make sense:
- Did first `handoff` complete:
- First handoff time shown:
- Reuse handoff time shown:
- Restore safety shown as OK:
- Source tokens shown:
- Skeleton tokens shown:
- Estimated tokens saved:
- Estimated savings percent:
- Was the token savings report useful:
- Attach or paste the savings report:
- Did `handoff` clearly identify the file to give to AI:
- Did `handoff` clearly identify files to keep local:

## AI/IDE trial

- AI/IDE used:
- Did you attach or paste `context_skeleton.mcp`:
- Did the AI understand the project better:
- Did you also use the recommended prompt from `AI_HANDOFF.md`:
- Any confusing AI behavior:

## Problems

Paste errors or confusing output here:

```text

```

If a command failed, include:

- command:
- exit code:
- what you expected:
- what happened:

## Overall experience

- Was installation easy:
- Was the first successful command obvious:
- Was the safety boundary clear:
- Was the speed acceptable:
- Did the second `handoff --reuse-if-fresh` feel faster:
- Would you keep using this during development:
- What is the one thing that should improve before v1.0:
