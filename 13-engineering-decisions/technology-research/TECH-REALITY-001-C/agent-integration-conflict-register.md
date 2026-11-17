# Agent Integration Conflict Register / Agent 集成冲突登记

| ID | Level | Conflict / gap | Authority | Evidence | Closure condition | Gate |
|---|---|---|---|---|---|---|
| C-CON-001 | BLOCKING | Current main does not contain full Owner D/E/F/G/H/I contracts; branches are separate and exact currentness must be reconciled | A + each Owner | Main HEAD `e52594f...`; original C merge base `b3c666...`; refreshed G/H branch pins in baseline | A-approved source pin manifest and each Owner exact-version adoption | C0/C5 |
| C-CON-002 | BLOCKING | Historical H 1.2.15 candidate vs Storage v3.3.2 bundle pinned to H 1.2.14; H successor Applied Delivery Evidence is not implemented | H/Storage/C/I/A | H schema Blob 860fc4... at historical H commit `0d363244...`; current H HEAD `0277a8b...`; Storage manifest 5c6143...; H Phase 3.8.23 | Successor manifest pins exact H schema, Applied Delivery Evidence schema/validator, CI and trust artifacts; all consumers review the same bundle | C3/C5/C6 |
| C-CON-003 | BLOCKING | C crypto profile and I governance signature profile not registered/deployed | I (trust policy), C (data signer), H (verification) | C Phase 3.11.0 Blob 9339b1... | I approval, key custody/rotation/revocation, anti-rollback checkpoints, H validator tests, operational evidence | C3/C5 |
| C-CON-004 | BLOCKING | G Applied freeze remains blocked and execution not verified | G; C/H/I/D supporting | G contract Blob aa3afa... | G-owned exact predicate, C final-request evidence, H wire/ACK, I authorization, D fence currentness and end-to-end tests | C5/C6 |
| C-CON-005 | HIGH | B Fact/Claim semantics ADR blocked; B research PR #55 is Draft and B0/B5 not passed | B + governance | PR #55 metadata; B domain overview Blob 4d1debc... | Formal B/governance ADR and downstream typed consumer mapping | C0/C5 |
| C-CON-006 | HIGH | Historical C branch diverges 167 ahead / 56 behind current main; its contracts cannot be treated as current main | C + A | Compare main...session-c; old C HEAD 71047... | Exact-source reconciliation and independent review; no blind merge | C0/C5 |
| C-CON-007 | HIGH | A research PR #45 is stale-base Draft; independent PR #56 says REVISE and A research remains NOT YET PROVEN | A | PR #45 base b372b... head 6c7c...; PR #56 | A remediates review findings and publishes current-main source pins; C consumes as candidate only | C0/C9 |
| C-CON-008 | HIGH | Provider capability parity not proven across OpenAI, Anthropic, Gemini, local and compatible endpoints | C | Official OpenAI/Anthropic/Gemini/vLLM/llama.cpp/Ollama/Hugging Face docs; exact per-model coverage remains open | Per-provider/versioned conformance matrix for stream/tool/error/cancel/usage/idempotency | C3/C6 |
| C-CON-009 | HIGH | Tool side-effect evidence and safe retry semantics are not standardized across arbitrary tools | I/tool runtime/C | Hermes and PydanticAI runtime docs; project contracts | I-approved capability/authorization model plus per-tool idempotency/effect evidence profile | C5/C6 |
| C-CON-010 | MEDIUM | Telemetry retention, attribute allowlist, data classification and export policy not approved | I/Observability | OTel context guidance; I governance register | I-approved classification/retention/export policy and redaction tests | C4/C6 |
| C-CON-011 | MEDIUM | Runtime/framework versions, licenses and Rust SDK/exporter compatibility not pinned | A/C | Official docs are moving; evidence index | Exact release/tag, license and dependency review | C6 |
| C-CON-012 | MEDIUM | No Brain end-to-end prototype or representative benchmarks executed | C/Testing/Runtime owner | Validation plan only | Reproducible test harness and measured outputs | C6 |
| C-CON-017 | BLOCKING | H Applied Delivery Evidence is a distinct message family from Unified 1.2.15 Provider Outcome Gateway Attestation; successor schema/validator is NOT IMPLEMENTED and wire mapping is NOT FROZEN | H; C final-boundary consumer review; G; I | H Phase 3.8.23 EN/zh-CN Blobs `be308261...` / `641abd9b...`; current H HEAD `0277a8b...` | H publishes exact successor schema/validator/P0 vectors/CI; C accepts exact CSubmitOutcome final-boundary mapping; G and I accept their own predicates/trust | C3/C5/C6 |
| C-CON-018 | HIGH | C research branch is based on old main and diverges from current main | C/A | Merge base `b3c666...`; current main `e52594...`; compare 6 ahead / 2 behind | Rebase or complete equivalent source reconciliation; rerun source-pin and diff checks before merge | C0/C7 |

## Conflict handling / 冲突处理
BLOCKING items fail closed. C cannot resolve B/D/E/F/G/H/I/Storage authority conflicts by renaming fields, adding a parallel enum, or treating an author-side acceptance as Owner approval. Any change to exact Blob SHA invalidates reviews that pin the predecessor.


## 完整中文版本

| ID | 等级 | 冲突/缺口 | 权威 Owner | 关闭条件 |
|---|---|---|---|---|
| C-CON-001 | BLOCKING | main 未包含完整 D/E/F/G/H/I 合同，Owner 分支尚未联合对账 | A 与各 Owner | A 批准精确源 Pin Manifest，各 Owner 对同版本采纳 |
| C-CON-002 | BLOCKING | Historical H 1.2.15 candidate vs Storage v3.3.2 bundle pinned to H 1.2.14; H successor Applied Delivery Evidence is not implemented | H/Storage/C/I/A | H schema Blob 860fc4... at historical H commit `0d363244...`; current H HEAD `0277a8b...`; Storage manifest 5c6143...; H Phase 3.8.23 | Successor manifest pins exact H schema, Applied Delivery Evidence schema/validator, CI and trust artifacts; all consumers review the same bundle | C3/C5/C6 |
| C-CON-003 | BLOCKING | C/I 密钥信任配置尚未注册或部署 | I/C/H | I 批准、密钥托管/轮换/撤销、Anti-Rollback、H 验证器和运维证据 |
| C-CON-004 | BLOCKING | G Applied 冻结阻塞，端到端执行未验证 | G/C/H/I/D | G Predicate、C 最终请求证据、H Wire/ACK、I 授权、D Fence 和端到端测试 |
| C-CON-005 | HIGH | B Fact/Claim ADR 阻塞，B PR #55 Draft | B/治理 | 正式 ADR 和下游类型映射 |
| C-CON-006 | HIGH | 历史 C 分支与 main 分叉 167 ahead/56 behind | C/A | 精确源对账和独立审查，禁止盲目合并 |
| C-CON-007 | HIGH | A PR #45 旧基线 Draft，PR #56 判定 REVISE | A | 修复发现、刷新当前源 Pin 并独立复审 |
| C-CON-008 | HIGH | Provider capability parity not proven across OpenAI, Anthropic, Gemini, local and compatible endpoints | C | Official OpenAI/Anthropic/Gemini/vLLM/llama.cpp/Ollama/Hugging Face docs; exact per-model coverage remains open | Per-provider/versioned conformance matrix for stream/tool/error/cancel/usage/idempotency | C3/C6 |
| C-CON-009 | HIGH | 任意 Tool 的副作用证据和安全重试语义未标准化 | I/Tool Runtime/C | I 批准能力授权模型及每类 Tool 的幂等/副作用证据 |
| C-CON-010 | MEDIUM | Telemetry 保留期限、属性白名单、数据分类未批准 | I/Observability | I 批准分类/保留/导出策略和脱敏测试 |
| C-CON-011 | MEDIUM | Runtime/Framework 版本、许可证和 Rust Exporter 未固定 | A/C | 精确 Release、许可证和依赖审查 |
| C-CON-012 | MEDIUM | Brain 端到端原型和基准未执行 | C/Testing/Runtime | 可复现 Harness 和测量结果 |
| C-CON-017 | BLOCKING | H Applied Delivery Evidence 与 Unified 1.2.15 Provider Outcome Gateway Attestation 是不同消息族；后继 Schema/Validator 尚未实现，Wire Mapping 未冻结 | H；C 最终请求边界消费方审查；G；I | H Phase 3.8.23 EN/zh-CN Blob `be308261...` / `641abd9b...`；当前 H HEAD `0277a8b...` | H 发布精确后继 Schema/Validator/P0 Vector/CI；C 接受 CSubmitOutcome Final-Boundary 精确映射；G/I 分别批准自身谓词和 Trust | C3/C5/C6 |
| C-CON-018 | HIGH | C 研究分支基于旧 main，与当前 main 分叉 | C/A | Merge Base `b3c666...`；当前 main `e52594...`；Compare 领先 6 / 落后 2 | 在合并前 Rebase 或完成等价对账，并重新运行源 Pin 与 Diff 检查 | C0/C7 |

BLOCKING 项必须 Fail Closed。C 不得通过重命名字段、添加竞争枚举或将作者自检接受视为 Owner 批准来消除冲突。任何 Blob SHA 变化都会使绑定旧 Blob 的审查失效。



## Direct open-issue cross-reference / 开放 Issue 交叉引用
The following project issues were directly fetched on 2026-11-18 and remain OPEN: #3 C/G/H Applied freeze, #4 I identity/authorization/Global Forget external decisions, #5 I36 governance approvals, #7 runtime repository/accountable engineering owner, #10 JF-10 physical recovery proof, #25 D/E/I/Storage producer admission and visibility, #29 HRC/RecoveryJoin and physical topology, #43 system-wide consolidation. These are external dependencies, not C-local issues that this PR can close.

**中文：** 本次直接读取的 Issue #3/#4/#5/#7/#10/#25/#29/#43 均为 OPEN，分别涉及 C/G/H Applied 冻结、I 身份/授权/Global Forget 治理、I36 正式批准、Runtime 仓库与工程 Owner、JF-10 物理恢复、D/E/I/Storage Producer Admission、HRC/RecoveryJoin 和全系统收敛。这些是跨 Owner/项目级依赖，不是 C 可通过本 PR 自行关闭的事项。



## Current-source delta conflicts / 当前性增量冲突

| ID | Level | New evidence | Remaining blocker / closure |
|---|---|---|---|
| C-CON-013 | HIGH | H 1.2.15 now has local validators and exact-head CI (91 tests + 288 tests/22 skipped) | Bounded callback tests do not prove production issuer, live gateway order, durable replay or trust registration; PR #67 DEFERRED |
| C-CON-014 | BLOCKING | Storage v3.3.2 manifest still pins H 1.2.14 while H current candidate is 1.2.15 | Successor exact-version manifest and all C/H/I/Storage owner approvals |
| C-CON-015 | HIGH | D/I/Storage PR #66/#68/#71 propose Phase 3.9 Forget terminalization/read-suppression changes | Proposals are non-normative; exact D/I/Storage decisions and executable/physical conformance required |
| C-CON-016 | HIGH | A PR #73 refreshes A against current D/E/I/Storage proposals | PR remains Draft and verdict REVISE/NOT YET PROVEN; no Owner approval is inferred |

These additions do not close C-CON-002/003/004. H CI success is evidence of local conformance only; it cannot close the H/Storage version mismatch, production trust registration or G Applied freeze.


## C-REVIEW-001 disposition / C 独立审查增量处置

C-CON-017 is a cross-owner blocker, not a C-owned schema fix. C may correct its consumer contract and evidence pins only after H publishes the successor artifact. The current H branch HEAD `0277a8b...` has removed the prior 1.2.15 schema/validator/test files from its tree; the old `0d363244...` artifacts and CI remain historical immutable evidence. Do not describe them as current H branch contents. C-CON-018 is a C-owned baseline/reconciliation task and must be closed before PR #69 can be considered merge-ready.

C-CON-017 属于跨 Owner 阻塞，不是 C 可自行修复的 Schema 问题。C 只能在 H 发布后继工件后更新消费方合同和证据 Pin。当前 H 分支 HEAD `0277a8b...` 已从分支树中删除旧 1.2.15 Schema/Validator/Test；旧 `0d363244...` 工件和 CI 仅是历史不可变证据，不得描述为当前 H 分支内容。C-CON-018 属于 C 自有基线对账任务，PR #69 在其关闭前不能视为可合并。
