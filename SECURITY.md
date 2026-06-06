# Ailoom Context Security Model

Ailoom Context is designed as a local-first context compression tool. Its core safety boundary is simple: share the AI-facing skeleton when you want compact context, and keep restore packages local when you need byte-exact recovery.

## Local-Only Promise

- Ailoom Context does not upload source code, text files, restore packages, skeletons, patch bundles, logs, or usage records to any Ailoom Context server.
- Ailoom Context does not include telemetry, analytics beacons, background log collection, or silent network reporting.
- Compression, restore, patch, replay, benchmark, dogfood, and doctor checks run on the user's local machine by default.
- Optional third-party dependencies such as tokenizers may be installed by the user, but Ailoom Context itself does not require cloud processing for the core workflows.

## What Is Safe To Share

- `context_skeleton.mcp` and JSON `skeleton_text` are the intended AI-facing surfaces.
- AI-facing skeleton output is redacted for common secret shapes such as API keys, tokens, passwords, client secrets, database URLs, access keys, and private key blocks.
- `context_manifest.json`, `context_restore.json`, restore packages, patch source packages, and local bundle metadata can preserve raw source bytes for exact restore. Keep those files local unless you intentionally want to share the original content.

## Lossless Restore Boundary

Redaction only applies to the skeleton surface. It does not modify original files, and it does not modify restore packages. This is intentional: local restore must remain byte-exact, while the file users paste into AI should avoid exposing obvious secrets.

## Local Artifact Cleanup

Generated bundle and handoff artifacts normally live under `.workspace_ail/`. To preview or remove local generated artifacts:

```bash
ailoom doctor --storage
ailoom clean --dry-run --all
ailoom clean --all
ailoom clean --dry-run --include-test-results
ailoom clean --dry-run --include-build-artifacts
```

`doctor --storage` reports generated artifact size, risk level, largest target, and cleanup safety before anything is deleted. It also separates project-generated artifact roots from global install visibility so users can tell the difference between files created inside a repository and the local command installation. The clean command targets known Ailoom Context generated directories such as `.workspace_ail/` and, with `--all`, `mcp-skeleton-restore/`. It does not delete source files, config files, global install files, or files outside known generated artifact roots. Test result cleanup requires the explicit `--include-test-results` flag so ordinary project test outputs are not removed accidentally. Build/package cleanup requires `--include-build-artifacts` for `build/`, `dist/`, and `*.egg-info`. Use `ailoom clean --dry-run --all --older-than 7d` when you want to preview cleanup for older generated artifacts while keeping fresh handoff bundles.

## Import And Replay Safety

- Restore writes to an explicit output file or output directory instead of overwriting the source tree by default.
- Patch replay should start with `--dry-run --write-dry-run-report`.
- Policy-aware patch replay supports `open`, `safe`, and `strict` modes.
- Imported manifests are checksum-verified before restore.

## Original Skeleton Language And Project Identity

`AILOOM-SKL.v1`, the Ailoom Context bundle schema, and the associated lossless context compression workflow are original project artifacts of Ailoom Context.

Please do not misrepresent derived tools, forks, rebranded packages, or commercial products as the official Ailoom Context project. If you build on this work, keep clear attribution to the original project and author, and keep project identity separation visible to users.

Commercial use cases such as SaaS hosting, enterprise integration, paid redistribution, rebranded resale, or building a competing commercial product based on Ailoom Context should contact the author for written permission: carwyn910@gmail.com.

The current repository license remains the source of legal permissions and restrictions. If Ailoom Context later needs stronger restrictions against competing commercial clones or rebranded resale, that should be handled through an explicit license change and legal review rather than a documentation-only claim.

## Reporting Security Issues

For now, please report security concerns through the repository issue tracker with a minimal reproduction, affected command, expected safety boundary, and whether any generated bundle or restore package exposed data unexpectedly.
