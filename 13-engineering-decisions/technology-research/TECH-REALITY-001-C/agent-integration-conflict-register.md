# Agent Integration Conflict Register / Agent 集成冲突登记

| ID | Level | Conflict / gap | Authority | Evidence | Closure condition | Gate |
|---|---|---|---|---|---|---|
| C-CON-001 | BLOCKING | Current main does not contain full Owner D/E/F/G/H/I contracts; branches are separate and exact currentness must be reconciled | A + each Owner | Main HEAD b3c666...; Owner branch pins in baseline | A-approved source pin manifest and each Owner exact-version adoption | C0/C5 |
| C-CON-002 | BLOCKING | H 1.2.15 candidate vs Storage v3.3.2 bundle pinned to H 1.2.14 | H/Storage/C/I/A | H schema Blob 860fc4...; Storage manifest 5c6143... | Successor manifest pins 1.2.15 exact schema, validator, CI and trust artifacts; all consumers review same bundle | C3/C5 |
| C-CON-003 | BLOCKING | C crypto profile and I governance signature profile not registered/deployed | I (trust policy), C (data signer), H (verification) | C Phase 3.11.0 Blob 9339b1... | I approval, key custody/rotation/revocation, anti-rollback checkpoints, H validator tests, operational evidence | C3/C5 |
| C-CON-004 | BLOCKING | G Applied freeze remains blocked and execution not verified | G; C/H/I/D supporting | G contract Blob aa3afa... | G-owned exact predicate, C final-request evidence, H wire/ACK, I authorization, D fence currentness and end-to-end tests | C5/C6 |
| C-CON-005 | HIGH | B Fact/Claim semantics ADR blocked; B research PR #55 is Draft and B0/B5 not passed | B + governance | PR #55 metadata; B domain overview Blob 4d1debc... | Formal B/governance ADR and downstream typed consumer mapping | C0/C5 |
| C-CON-006 | HIGH | Historical C branch diverges 167 ahead / 56 behind current main; its contracts cannot be treated as current main | C + A | Compare main...session-c; old C HEAD 71047... | Exact-source reconciliation and independent review; no blind merge | C0/C5 |
| C-CON-007 | HIGH | A research PR #45 is stale-base Draft; independent PR #56 says REVISE and A research remains NOT YET PROVEN | A | PR #45 base b372b... head 6c7c...; PR #56 | A remediates review findings and publishes current-main source pins; C consumes as candidate only | C0/C9 |
| C-CON-008 | HIGH | Provider capability parity not proven across OpenAI, Anthropic, Gemini, local and compatible endpoints | C | Official source evidence index; several provider docs not inspected | Per-provider versioned conformance matrix for stream/tool/error/cancel/usage/idempotency | C3/C6 |
| C-CON-009 | HIGH | Tool side-effect evidence and safe retry semantics are not standardized across arbitrary tools | I/tool runtime/C | Hermes and PydanticAI runtime docs; project contracts | I-approved capability/authorization model plus per-tool idempotency/effect evidence profile | C5/C6 |
| C-CON-010 | MEDIUM | Telemetry retention, attribute allowlist, data classification and export policy not approved | I/Observability | OTel context guidance; I governance register | I-approved classification/retention/export policy and redaction tests | C4/C6 |
| C-CON-011 | MEDIUM | Runtime/framework versions, licenses and Rust SDK/exporter compatibility not pinned | A/C | Official docs are moving; evidence index | Exact release/tag, license and dependency review | C6 |
| C-CON-012 | MEDIUM | No Brain end-to-end prototype or representative benchmarks executed | C/Testing/Runtime owner | Validation plan only | Reproducible test harness and measured outputs | C6 |

## Conflict handling / 冲突处理
BLOCKING items fail closed. C cannot resolve B/D/E/F/G/H/I/Storage authority conflicts by renaming fields, adding a parallel enum, or treating an author-side acceptance as Owner approval. Any change to exact Blob SHA invalidates reviews that pin the predecessor.


## 完整中文版本

| ID | 等级 | 冲突/缺口 | 权威 Owner | 关闭条件 |
|---|---|---|---|---|
| C-CON-001 | BLOCKING | main 未包含完整 D/E/F/G/H/I 合同，Owner 分支尚未联合对账 | A 与各 Owner | A 批准精确源 Pin Manifest，各 Owner 对同版本采纳 |
| C-CON-002 | BLOCKING | H 1.2.15 候选与 Storage v3.3.2 的 H 1.2.14 Pin 不一致 | H/Storage/C/I | 后继 Manifest 精确绑定 1.2.15 Schema、Validator、CI、Trust，并由消费者复审 |
| C-CON-003 | BLOCKING | C/I 密钥信任配置尚未注册或部署 | I/C/H | I 批准、密钥托管/轮换/撤销、Anti-Rollback、H 验证器和运维证据 |
| C-CON-004 | BLOCKING | G Applied 冻结阻塞，端到端执行未验证 | G/C/H/I/D | G Predicate、C 最终请求证据、H Wire/ACK、I 授权、D Fence 和端到端测试 |
| C-CON-005 | HIGH | B Fact/Claim ADR 阻塞，B PR #55 Draft | B/治理 | 正式 ADR 和下游类型映射 |
| C-CON-006 | HIGH | 历史 C 分支与 main 分叉 167 ahead/56 behind | C/A | 精确源对账和独立审查，禁止盲目合并 |
| C-CON-007 | HIGH | A PR #45 旧基线 Draft，PR #56 判定 REVISE | A | 修复发现、刷新当前源 Pin 并独立复审 |
| C-CON-008 | HIGH | Provider 能力等价性未跨 OpenAI/Anthropic/Gemini/本地服务证明 | C | 每 Provider/Model 的版本化 Stream/Tool/Error/Cancel/Usage/Idempotency 符合性矩阵 |
| C-CON-009 | HIGH | 任意 Tool 的副作用证据和安全重试语义未标准化 | I/Tool Runtime/C | I 批准能力授权模型及每类 Tool 的幂等/副作用证据 |
| C-CON-010 | MEDIUM | Telemetry 保留期限、属性白名单、数据分类未批准 | I/Observability | I 批准分类/保留/导出策略和脱敏测试 |
| C-CON-011 | MEDIUM | Runtime/Framework 版本、许可证和 Rust Exporter 未固定 | A/C | 精确 Release、许可证和依赖审查 |
| C-CON-012 | MEDIUM | Brain 端到端原型和基准未执行 | C/Testing/Runtime | 可复现 Harness 和测量结果 |

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
