# AI Work Items Index

This index is the entry point for all governed AI development tasks.

| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |
|---|---|---|---|---|---|---|---|---|
| [AID-2026-001](AID-2026-001/manifest.yaml) | Define ChatGPT-native execution model | A | ARCH/R3 | REMEDIATION_IN_PROGRESS | [prompt-v2](AID-2026-001/prompt-v2.md) | PR #42 merged (includes #72); [PR #141](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/141) adds 24/24 reference-model tests | Historical FAIL at 1d6ab393; fresh independent review pending | BLOCKED_PENDING_R3_EVIDENCE |
| [PR-GOVERNANCE-001](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/130) | Mandatory session delivery traceability and PR integration governance | Integration Owner | DOC/R1 | ADOPTED | Chat instruction (immutable prompt hash: NOT RECORDED) | [PR #132](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/132) traceability implementation; [PR #144](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/144) governance standard + synchronized templates — both merged to `main` | Same-author COMMENT; owner-directed adoption recorded in Issue #130 comment #6962523529; no independent review claimed | ADOPTED as repository process policy; platform enforcement remains blocked by Issue #134 |

## Session-level delivery records / 会话级交付记录

| Session record | Work Item | Owning Issue | Related PR | Branch / exact Head | Prompt identity | Work and evidence | Status / closeout |
|---|---|---|---|---|---|---|---|
| `2026-11-18-GITHUB-CONTINUATION-PR132` | PR-GOVERNANCE-001 | [#130](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/130) | [#132](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/132) | `fix/pr-governance-001-session-traceability` / final PR Head `c5e16e224f7e6fe7c7c1280be2e331c3d91bd7a3` | Prompt ID/version/hash: NOT RECORDED | Five-file documentation change reviewed; exact final PR Head `c5e16e224f7e6fe7c7c1280be2e331c3d91bd7a3`; GOV-DOC-001 structural checks #177/#179 SUCCESS on that exact Head; `git diff --check` NOT RUN; same-author review only, owner-directed exception recorded, no independent approval claimed | COMPLETE — squash-merged to `main`; merge commit `6b7c864e65453f8e8c9f5edc02c6fd937f13813f`; merge commit verified as current main Head and index read-back completed; post-merge workflow checks not yet observed |
| `2026-11-18-PR-INTEGRATION-CONTINUATION` | AID-2026-001 | [#135](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/135) | [#132](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/132), [#133](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/133), [#136](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/136) | `docs/aid-2026-001-current-status-reconciliation` / final PR Head `1ca57512cdc093a11c5aa7294c873edebbec9c4b` | Prompt ID/version/hash: NOT RECORDED | Reviewed current-state reconciliation; GOV-DOC-001 run #190 SUCCESS on exact Head; changed YAML fragments parsed with PyYAML; full manifest/schema and R3 tests NOT RUN; #132/#133/#136 verified merged | COMPLETE — squash-merged to `main` at `fb9269661225a26416d11528e9a94d845345b2af`; three changed files read back from main |

## Registration rules

- Create a unique `AID-YYYY-NNN` before substantive work begins.
- Create the work-item directory and manifest before prompt execution.
- Link the exact prompt version and SHA-256 used by each run.
- Update this index when status changes at major gates and at closeout.
- Never delete rejected, blocked or superseded records; mark their final disposition.


## Session traceability maintenance / 会话追溯维护
| `2026-11-18-AID-2026-001-CONTINUATION-ALL` | AID-2026-001 | [#41](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/41) | [#141](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/141) | `test/aid-2026-001-reference-model-coverage-22` / final Head `d5702426147456f0bf00e0aec9ad5916200cebef` | ChatGPT continuation instruction; immutable prompt hash NOT RECORDED | Expanded non-production Forget reference model to 24 tests; exact-Head CI #44188134319 SUCCESS; bilingual docs #44188134357/#44188136170 SUCCESS; found and fixed empty-inventory vacuous completion and ambiguous delimiter hashing; D/I non-independent preliminary review filed in Issue #41; runtime-repository blocker updated in Issue #7 | PR #141 merged; merge commit `9edc746c001f1f82950edad7ce130342db53ff67`; production R3, independent D/I review, integration review and acceptance remain blocked/pending |

Every substantive active or completed AI session MUST have a row linking its Work Item, owning Issue, related PRs, exact branch/head SHA, current status and closeout evidence. Update the row at material progress points and final closeout. Missing prompt hashes or historical evidence must be marked NOT RECORDED; never backfill fabricated values. Blocked and no-change work remains visible with its resolver and exit condition.

每个进行中或已完成的实质性 AI 会话 MUST 有一行记录，关联 Work Item、归属 Issue、相关 PR、准确分支/Head SHA、当前状态和结项证据。在重要进展和最终结项时更新。缺少的提示词哈希或历史证据必须标记为 NOT RECORDED，禁止补造。受阻和无变更工作必须保持可见，并注明解决者和退出条件。
