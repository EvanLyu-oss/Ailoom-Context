# Launch Posts

Copy, adapt, and post these when sharing Ailoom Context.

Repository:

```text
https://github.com/EvanLyu-oss/Ailoom-Context
```

Author:

```text
Evan <carwyn910@gmail.com>
```

## Short English Post

```text
I am building Ailoom Context, a local-first context compression tool for AI coding agents.

It turns a large repo or long document into a compact AI-readable skeleton, while keeping exact restore files local.

Current beta checks:
- 62/62 Python smoke checks passing
- 93/93 benchmark cases restore-verified
- local-only, zero telemetry
- best observed large-directory savings around 94% vs baseline

If you use Cursor, Codex, Claude Code, Cline, Continue, or other AI coding agents on larger projects, I would love feedback.

GitHub:
https://github.com/EvanLyu-oss/Ailoom-Context
```

## Short Chinese Post

```text
我正在做一个开源工具 Ailoom Context。

它是给 AI 编程 Agent 用的本地上下文压缩工具：把大项目、长文档转成更小的 AI 可读 skeleton，同时把精确还原文件留在本地。

目前 beta 检查：
- Python smoke 62/62 通过
- benchmark 93/93 可还原
- 本地运行，零遥测
- 大目录场景最高观察到约 94% token 节省

如果你在用 Cursor、Codex、Claude Code、Cline、Continue 这类工具处理大项目，欢迎试用和反馈。

GitHub:
https://github.com/EvanLyu-oss/Ailoom-Context
```

## Friend Circle / WeChat Style

```text
我最近开源了一个自己边开发边用的工具：Ailoom Context。

它解决的问题很具体：AI agent 读大项目太慢、太吃 token、上下文容易爆。

Ailoom 会把项目压缩成一个 AI 可读的 context_skeleton.mcp，同时把完整还原文件留在本地，不上传云端、不做遥测。

目前已经能稳定 dogfood 自己，benchmark 里 93/93 restore verified。朋友测试里也反馈，在 agent 工作流里上下文读取速度明显提升。

如果你平时用 Cursor / Codex / Claude Code / Cline / Continue 处理大项目，欢迎帮我试一下。

项目地址：
https://github.com/EvanLyu-oss/Ailoom-Context
```

## Hacker News / Show HN Draft

Title:

```text
Show HN: Ailoom Context – local-first context compression for AI coding agents
```

Body:

```text
Hi HN,

I am building Ailoom Context, a local-first CLI tool that compresses large repositories or long documents into compact AI-readable skeletons.

The goal is to reduce token pressure for AI coding agents without giving up exact local restore. Ailoom writes two coordinated artifacts:

- context_skeleton.mcp: the AI-facing structural context
- context_manifest.json + restore package: keep-local files for byte-exact restore

It is not a hosted service and does not upload source code or usage logs.

Current beta checks include:

- 62/62 Python smoke checks passing
- 93/93 benchmark cases restore-verified
- dogfood restore of this repo
- local-only / zero telemetry safety model
- best observed large-directory savings around 94% vs baseline

I am especially looking for feedback from people using Cursor, Codex, Claude Code, Cline, Continue, OpenHands, or similar tools on large repos.

Repo:
https://github.com/EvanLyu-oss/Ailoom-Context
```

## Reddit / Dev Community Draft

```text
I am looking for feedback on Ailoom Context, an open-source local-first context compression tool for AI coding agents.

Problem:
Large repos make AI agents slow and expensive because they repeatedly read too much raw context.

Approach:
Ailoom creates a compact AI-facing skeleton and keeps exact restore files local. You share context_skeleton.mcp with the agent, while keeping context_manifest.json and restore packages on your machine.

Why it may be useful:
- local-only, zero telemetry
- exact restore path
- shows token savings and speed guidance
- daily handoff reuses fresh bundles when the project has not changed
- designed for Cursor/Codex/Claude Code/Cline/Continue-style workflows

I would love feedback from people working on larger projects.

GitHub:
https://github.com/EvanLyu-oss/Ailoom-Context
```

## Product Hunt Draft

Tagline:

```text
Local-first context compression for AI coding agents.
```

Description:

```text
Ailoom Context turns large repositories and long documents into compact AI-readable skeletons while keeping exact restore files local. It helps AI coding agents read less context, reduce token pressure, and preserve a byte-exact restore path without cloud upload or telemetry.
```

First comment:

```text
I built Ailoom Context because AI coding agents become slower and less reliable when they repeatedly read large codebases as raw context.

The beta is local-first: it creates an AI-facing skeleton, keeps restore packages local, and reports token savings plus restore safety.

I am looking for developers who use AI coding tools on large repositories and can share honest feedback.
```

## GitHub Repository Description

```text
Local-first context compression for AI coding agents: compact AI-readable skeletons, exact local restore, patch/replay, and benchmark-ready token savings.
```

## GitHub Topics

```text
ai-agents
ai-coding
coding-agents
context-compression
context-engineering
developer-tools
llm
local-first
privacy
token-optimization
cursor
codex
claude-code
cli
python
```

## Social Image Prompt

Use this in an image generator:

```text
Create a clean, premium open-source developer-tool promo graphic for "Ailoom Context".

Theme: local-first AI context compression for coding agents.

Visual concept:
- A large messy codebase on the left, shown as dense file trees and code fragments.
- A woven loom or folding structure in the center compressing the project.
- A compact glowing "context_skeleton.mcp" artifact on the right flowing into an AI coding agent terminal.
- A separate locked local restore package below, labeled "exact restore stays local".

Text on image:
Ailoom Context
Local-first context compression for AI coding agents
Compact skeletons. Exact local restore. Zero telemetry.
GitHub: github.com/EvanLyu-oss/Ailoom-Context
Author: Evan <carwyn910@gmail.com>

Style:
Modern developer tooling, sharp typography, dark graphite background with warm amber and teal accents, trustworthy and technical, not cartoonish, no purple default SaaS look, high contrast, suitable for sharing on social media.

Aspect ratio: 16:9.
```

## Reply Playbook

If someone asks "Is this just summarization?":

```text
Not exactly. The skeleton is compact and AI-facing, but the restore package stays local so exact reconstruction remains possible. The project separates "what the AI needs to read" from "what your machine keeps for restore".
```

If someone asks "Does it upload my code?":

```text
No. The beta is local-first and has no telemetry. Source processing, restore packages, and generated bundles stay on your machine unless you choose to share a skeleton.
```

If someone says "My small project got larger":

```text
That can happen on tiny inputs because the skeleton includes structure and restore metadata. The value is clearer on larger repositories or long documents; use ailoom savings to check the real token impact.
```

If someone asks "What should I run first?":

```text
From the repo root:
sh install.sh --setup-shell
ailoom first-run
Then inside your project:
ailoom handoff --copy --open
ailoom next
```
