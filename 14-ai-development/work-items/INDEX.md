# AI Work Items Index

This index is the entry point for all governed AI development tasks.

| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |
|---|---|---|---|---|---|---|---|---|
| [AID-2026-001](AID-2026-001/manifest.yaml) | Define ChatGPT-native execution model | A | ARCH/R3 | REMEDIATION_IN_PROGRESS | [prompt-v2](AID-2026-001/prompt-v2.md) | PR #42 merged to main (includes PR #72) | Historical FAIL at 1d6ab393; fresh independent review pending | BLOCKED_PENDING_R3_EVIDENCE |
| [PR-GOVERNANCE-001](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/130) | Mandatory session delivery traceability | Integration Owner | DOC/R1 | MERGED_PENDING_GOVERNANCE_ADOPTION | Chat instruction (immutable prompt hash: NOT RECORDED) | [PR #132](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/132) — merged to `main` | Same-author COMMENT; owner-directed one-PR exception recorded; no independent review claimed | MERGED; AI-STD-001 adoption decision remains pending |

## Session-level delivery records / 会话级交付记录

| Session record | Work Item | Owning Issue | Related PR | Branch / exact Head | Prompt identity | Work and evidence | Status / closeout |
|---|---|---|---|---|---|---|---|
| `2026-11-18-GITHUB-CONTINUATION-PR132` | PR-GOVERNANCE-001 | [#130](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/130) | [#132](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/132) | `fix/pr-governance-001-session-traceability` / final PR Head `c5e16e224f7e6fe7c7c1280be2e331c3d91bd7a3` | Prompt ID/version/hash: NOT RECORDED | Five-file documentation change reviewed; exact final PR Head `c5e16e224f7e6fe7c7c1280be2e331c3d91bd7a3`; GOV-DOC-001 structural checks #177/#179 SUCCESS on that exact Head; `git diff --check` NOT RUN; same-author review only, owner-directed exception recorded, no independent approval claimed | COMPLETE — squash-merged to `main`; merge commit `6b7c864e65453f8e8c9f5edc02c6fd937f13813f`; merge commit verified as current main Head and index read-back completed; post-merge workflow checks not yet observed |

## Registration rules

- Create a unique `AID-YYYY-NNN` before substantive work begins.
- Create the work-item directory and manifest before prompt execution.
- Link the exact prompt version and SHA-256 used by each run.
- Update this index when status changes at major gates and at closeout.
- Never delete rejected, blocked or superseded records; mark their final disposition.


## Session traceability maintenance / 会话追溯维护

Every substantive active or completed AI session MUST have a row linking its Work Item, owning Issue, related PRs, exact branch/head SHA, current status and closeout evidence. Update the row at material progress points and final closeout. Missing prompt hashes or historical evidence must be marked NOT RECORDED; never backfill fabricated values. Blocked and no-change work remains visible with its resolver and exit condition.

每个进行中或已完成的实质性 AI 会话 MUST 有一行记录，关联 Work Item、归属 Issue、相关 PR、准确分支/Head SHA、当前状态和结项证据。在重要进展和最终结项时更新。缺少的提示词哈希或历史证据必须标记为 NOT RECORDED，禁止补造。受阻和无变更工作必须保持可见，并注明解决者和退出条件。
