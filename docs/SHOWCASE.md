# Ailoom Context Showcase

This page collects public-facing proof points for Ailoom Context.

## One-Sentence Pitch

Ailoom Context is a local-first context compression tool for AI coding agents: it turns large repositories and long documents into compact AI-readable skeletons while keeping exact restore files local.

## Why Developers Care

AI coding agents get slower and less reliable when they must read too much raw source. Ailoom Context gives the agent a smaller structural skeleton instead of dumping the whole project into context.

The key promise is not just summarization. Ailoom separates:

- AI-facing context: `context_skeleton.mcp`
- Keep-local restore files: `context_manifest.json`, restore package, bundle directory

That means users can reduce token pressure without giving up byte-exact local restore.

## Current Proof Points

These are conservative beta-era signals. They should be phrased as observed results, not universal guarantees.

| Signal | Current result |
| --- | --- |
| Dogfood restore | Ailoom Context compresses and restores its own repository byte-exactly |
| Latest release readiness | `7/7` release checks passing on macOS |
| Python smoke coverage | `62/62` checks passing |
| Quick benchmark restore | `93/93` benchmark cases restore-verified |
| Benchmark status | `ready / ready / ok` |
| Large-directory benchmark | Best observed savings about `94%` vs baseline |
| Long-text benchmark | Best observed savings about `54%` vs baseline |
| Safety model | Local-only, zero telemetry, restore files kept local |
| Early tester signal | Some agent workflows reported up to `10x` faster context-reading experience |

Recommended wording:

```text
In current beta checks, Ailoom Context restores 93/93 benchmark cases and shows up to about 94% large-directory token savings vs baseline. Early testers reported up to 10x faster context-reading workflows in agent use.
```

Avoid wording like:

```text
Always saves 94% tokens and makes all agents 10x faster.
```

## Demo Flow

Use this flow when showing Ailoom Context to a new user:

```bash
ailoom first-run
ailoom handoff --copy --open
ailoom next
ailoom savings
ailoom safety
```

Show these outputs:

- `Restore safety: OK`
- `Give AI this file: .../context_skeleton.mcp`
- `Keep for restore: .../context_manifest.json`
- `Agent reading: ...x fewer input tokens`
- `Reuse policy: active`

## What To Screenshot

For social posts or README images, capture:

- The top of `ailoom handoff`.
- The `Value summary` panel.
- The `Reuse policy` panel after a second handoff.
- The `Ailoom Context Next` output.
- The `Ailoom Context Savings` output.

Do not screenshot restore package contents if they contain private source data.

## Audience Fit

Best first audiences:

- Developers using Cursor, Codex, Claude Code, Cline, Continue, OpenHands, or similar AI coding tools.
- People working in large repositories where agents repeatedly reread context.
- Writers or researchers managing long manuscripts.
- Local-first and privacy-conscious developer-tool users.

Less ideal early audiences:

- Users who expect a hosted SaaS dashboard.
- Users who want cloud sync or telemetry.
- Users who only work on tiny files where token savings may not show yet.

## Links

- Repository: `https://github.com/EvanLyu-oss/Ailoom-Context`
- Good first trial: `GOOD_FIRST_TRIAL.md`
- Beta testing guide: `docs/BETA_TESTING.md`
- User guide: `docs/USER_GUIDE.md`
- Feedback template: `FEEDBACK_TEMPLATE.md`
