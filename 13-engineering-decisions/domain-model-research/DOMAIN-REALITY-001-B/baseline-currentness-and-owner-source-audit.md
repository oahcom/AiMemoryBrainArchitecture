# DOMAIN-REALITY-001-B — Baseline Currentness and Owner Source Audit
# DOMAIN-REALITY-001-B — 基线时效性与 Owner 源文件审计

- ID: B-BASELINE-ADD-001
- Status: VERIFIED SNAPSHOT WITH OPEN RECONCILIATION — B0 NOT PASSED
- Audit date: 2026-11-17
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Current main HEAD readback: `901e38ba7b45ed1822eaefddc2da8d765cf8985c`
- Research branch HEAD observed from PR metadata: `5797ff44db7e3fdbc0820a08e91ff78f76c4faac`
- PR: #55, Open / Draft
- PR base SHA in current metadata: `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`
- Original research ancestor: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`

## 1. Currentness correction / 时效性纠正

The original baseline report pins main at `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. That is the historical research ancestor, not the current main HEAD. The live repository metadata and recursive tree readback show current main at `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`.

原基线报告将 main 固定在 `b372b62c640a2b656e54b6db62a4ee67d7d8c001`。该 SHA 是历史研究祖先，不是当前 main HEAD。实时仓库元数据和递归 Tree 读回显示，当前 main 为 `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`。

The commit comparison reports 26 commits ahead from the historical ancestor to current main and no net changed-file entries in the returned comparison result. The latest visible main commits include a sequence of `revert(domain): remove research artifact mistakenly written to main`. This history is relevant to delivery provenance: the research artifacts must remain on the isolated B branch, and main must not be treated as having accepted them.

从历史祖先到当前 main 的 Commit Compare 返回 ahead_by=26，且结果中没有净变更文件条目。当前 main 最近可见提交包含一系列 `revert(domain): remove research artifact mistakenly written to main`。该历史关系到交付溯源：研究文件必须留在隔离 B 分支，不得将 main 视为已接受这些文件。

The existing baseline's domain source Blob pins were re-fetched from current main and remain identical for the six root domain files listed below. This supports continued use of those exact file contents, but does not make the old HEAD value current.

已从当前 main 重新读取原基线中的六个根领域文件，其 Blob Pin 保持一致。这支持继续使用这些精确文件内容，但不代表旧 HEAD 值仍是当前值。

| Current-main source path | Blob SHA | Re-read result |
|---|---|---|
| `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | VERIFIED |
| `02-domain-model/core-entities.md` | `8cb5a674eec8eac1f3c4d83c400dc08d00166f23` | VERIFIED |
| `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | VERIFIED |
| `02-domain-model/lifecycle-model.md` | `81c48c928cb5f9c76ca29d493fbd9479079e62f7` | VERIFIED |
| `02-domain-model/relationships-and-provenance.md` | `e762f84c59f69de7a44baad2123aed46e1ffea16` | VERIFIED |
| `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | VERIFIED |

## 2. Research PR currentness / 研究 PR 时效性

PR #55 is still Open / Draft. Current PR metadata reports head commit `dc05436aaa75a90c70aa3137dcdfadc49cf7e6dd`, while its base SHA is `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`. The PR description itself records current main HEAD `8c0c5b11...` and the earlier base ancestor. These are different facts and must not be collapsed.

PR #55 仍为 Open / Draft。当前 PR 元数据显示 head commit 为 `dc05436aaa75a90c70aa3137dcdfadc49cf7e6dd`，base SHA 为 `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`。PR 描述另行记录了当前 main HEAD `8c0c5b11...` 和更早的基线祖先。这些是不同事实，不得混为一谈。

PR #55 is not a merged or accepted canonical contract. No merge is requested. Before B5 can pass, re-read the live PR metadata, complete diff, latest branch ref, commit list and all final Blob SHAs after the last write; investigate the base/head divergence and mergeability rather than assuming it is harmless.

PR #55 不是已合并或已验收的规范契约。本任务不请求合并。B5 通过前，必须在最后一次写入后重新读取实时 PR 元数据、完整 Diff、最新分支 Ref、Commit 列表和所有最终 Blob SHA；必须调查 base/head 分歧及 Mergeability，不能假定其无影响。

## 3. Owner branch snapshots / Owner 分支快照

The following branch HEADs were read from the repository branch listing and their recursive Git trees were fetched. These are branch snapshots, not proof of Owner approval or independent review.

以下分支 HEAD 来自仓库分支列表，且已读取其递归 Git Tree。这些只是分支快照，不构成 Owner 批准或独立审查证明。

| Owner | Branch | Observed HEAD | Exact source Blob(s) read |
|---|---|---|---|
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | Existing baseline records old Scope/Permission Blob `6a9c47031ca3ecfd47b2f7d7419b2df8d808329b`; current-main counterpart is `b5215ae...` |
| C | `session-c-agent-integration-2026-11-16` | `2e8414f361b0b5d7de959be8a971aadc9e62d6a9` | `phase-3.8.22-c-exact-review-h-authenticated-ingress-1.2.14-60-tests.md` Blob `8fd6052cabf58a78962cc2e776398b2a40604bcd` |
| D | `session-d-memory-brain-2026-11-16` | `76fcc92225666a11893b7241825261319edb621e` | `phase-3.8.13-d-review-h-outer-envelope-authenticated-ingress-gate.md` Blob `152627e00b96355e2ff370acd643a51168c4c78c` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | `phase-3.8.6-e-review-storage-serialization-anchor.md` Blob `19d708bc29b6115d7bccb7d320781f452ee28b78` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | `phase-3.6-runtime-forget-suppression-and-invalidation.md` Blob `ce59252dbbdc5d10d016704797e9ba12d5a941bd` |
| G | `session-g-memory-context` | `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe` | `context-versioning.md` Blob `05c0739d0c22576a1fd5affc7d73c078c89049b1`; Phase 3.7 Blob `c1de241ec69834377d9b0e24aa4770a809796d4b` |
| H | `session-h-bmcp-protocol` | `8e24342048d29ef29195b153b8b9ec53ba7c75d9` | `phase-3.8.20-h-exact-c-envelope-p0-correction-and-json-pointer-mapping.md` Blob `4ba7e1699215d02224f805a15484b1da2e40c03f`; H Unified 1.2.14 schema Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59` |
| I | `session-i-security-governance-2026-11-16` | `2afe0e17f8c0929d9e642ccbe2cad112b5fd43a9` | `phase-3.8.18-i-review-c-outer-envelope-signer-p0-trust-registration.md` Blob `b6d1ea45825a1c2090abfba42474814f02f073a3` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `431138e7c7af8bee716f3d8dcbc20114c046bd36` | `phase-3.6.21-storage-v3.2.11-exact-version-bundle-manifest.md` Blob `54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57`; ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988` |
| A | `session-a-integration-2026-11-16` | `9bdf938b980413f592a4db9fe94f4bf2c299fb01` | Owner-local source inventory not fully fetched in this pass |
| Testing/Quality | NOT VERIFIED | NOT VERIFIED | No accountable branch/source pin established in this pass |

Branch snapshots may lag active work or PR heads. The exact Owner source and decision must be pinned per affected contract; a branch HEAD alone is not enough.

分支快照可能落后于活跃工作或 PR HEAD。每个受影响契约都必须 Pin 精确 Owner 源文件和决策；仅有分支 HEAD 并不足够。

## 4. Relevant PR and Issue register / 相关 PR 与 Issue 登记

Repository PR listing was read for all returned PRs. The following are directly relevant to B's current semantic dependencies:

| Record | Live state | B relevance / boundary |
|---|---|---|
| PR #55 | Open, Draft | This B research package; head/base currentness still requires final reconciliation |
| PR #52 | Open, Draft | A's B→A protocol convergence and Storage topology review; B disposition is candidate, not frozen |
| PR #51 | Open, Draft | A cross-owner protocol alignment; candidate H 1.2.14 / CSubmitOutcome 1.0.1; callbacks remain test doubles |
| PR #53 | Closed, not merged | A final assessment is DEFERRED; Fact/Claim ADR and B semantics remain blockers |
| PR #50 | Open, Draft | System-wide risk assessment affecting semantic readiness |
| PR #49 / #47 | Open, Draft | Complexity assessments; contextual evidence, not B approval |
| PR #46 | Open, Draft | Engineering dependency and implementation feasibility |
| PR #45 | Open, Draft | Technology reality review; no domain authority transfer |
| PR #28 | Open, Draft | Bilingual architecture coverage and parity |

The following issues were fetched directly and remain Open at read time:

以下 Issue 已直接读取，读取时均为 Open：

- **#3 — C/G/H Applied evidence and BMCP wire contract:** requests B's typed ActorRef/ScopeRef/EnvironmentRef mapping, while C/G/H/I/D own their respective proof and authorization semantics.
- **#5 — I36-GOV-01..10:** I governance decisions remain GOVERNANCE-BLOCKED; B cannot infer Principal taxonomy or ActorRef policy approval.
- **#7 — Runtime implementation repository:** this repository README identifies itself as architecture definition and says implementation has not started by design; runtime implementation and accountable engineering owner remain unresolved.
- **#10 — JF-10 P0:** database/COC physical capability and fault recovery are not established by domain documentation.
- **#25 — D/E/I/Storage publication gate:** producer admission, lineage registration, authorization, visibility and Forget ordering remain owner-specific and open.
- **#29 — HRC/RecoveryJoin/topology:** candidate CI evidence is bounded; it does not establish production trust, provider truth, physical JF-10 or deployment topology.
- **#43 — System-wide consolidation:** controlling integration issue remains Open; A's assessment defers architecture freeze.

The full repository listing also contains other open PRs/issues. This register is the relevant subset based on current B dependencies, not a claim that unrelated project records were individually reviewed.

仓库完整列表还包含其他 Open PR/Issue。本表是按 B 当前依赖选出的相关子集，不声称已逐项审查所有无关项目记录。

## 3A. 中文 Owner 分支与来源 Pin 快照

| Owner | 当前观察分支 | HEAD Commit SHA | 最新复审工件 Blob | 中文结论 |
|---|---|---|---|---|
| B | session-b-domain-model-phase3 | 2faf8ec38f14dba49e7263d7a60804dae1a74ee2 | e2bc4c8dde9706bfbe443269b702f1b5aa6965f6 | 批准 Per-authority 名义类型边界；仅 L1/L2，不代表 Storage 物理实现已批准。 |
| C | session-c-agent-integration-2026-11-16 | 2e8414f361b0b5d7de959be8a971aadc9e62d6a9 | 8fd6052cabf58a78962cc2e776398b2a40604bcd | 接受 H Reference Ingress Gate/60 项测试边界；Signer/Attestation 和 Crypto Profile 仍 OPEN。 |
| D | session-d-memory-brain-2026-11-16 | 76fcc92225666a11893b7241825261319edb621e | 152627e00b96355e2ff370acd643a51168c4c78c | H 仅为上游接口；D Forget/RecoveryJoin 权威保持不变。 |
| E | session-e-memory-compiler-2026-11-16 | ee098e14747d9915de5b3efb63b3a8dd77f670ed | 19d708bc29b6115d7bccb7d320781f452ee28b78 | 在 E 生命周期条件下接受 Anchor；L4 实现 OPEN。 |
| F | session-f-memory-runtime | 1908ce4d233b20f7cafd00cb679affd01bd15174 | 122238146830db6188f00a9788e018a82bfb3f90 | 在读路径/Cache 条件下接受 Anchor；L4 实现 OPEN。 |
| G | session-g-memory-context | 3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe | 1894860c76336f8739d354b72beed3992cffd17e | 接受有限 L1/L2 C/H 映射；Applied Contract 未冻结，38 项测试使用 Authority Double。 |
| H | session-h-bmcp-protocol | 8e24342048d29ef29195b153b8b9ec53ba7c75d9 | 4ba7e1699215d02224f805a15484b1da2e40c03f | 修正 C Envelope P0 Proof Locator；可执行认证和 Durable Replay 仍 OPEN。 |
| I | session-i-security-governance-2026-11-16 | 2afe0e17f8c0929d9e642ccbe2cad112b5fd43a9 | b6d1ea45825a1c2090abfba42474814f02f073a3 | 接受 C Origin Signer/P0 分离为候选；Crypto Suite/Trust 注册未批准。 |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | 431138e7c7af8bee716f3d8dcbc20114c046bd36 | 54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57 | v3.2.11 精确候选包已绑定复审，但未联合接受/冻结，需要 A 新审查。 |
| A | session-a-integration-2026-11-16 | 9bdf938b980413f592a4db9fe94f4bf2c299fb01 | e12cd7b5c79e2234178014243fd51f2e7d51272e | 将 Outer Envelope Authentication 明确列为阻塞架构缺口，要求不得冻结。 |

这些值是 2026-11-17 的 Owner 分支观察快照；它们不是永久 HEAD，也不是 Owner 批准。最终验收前必须重新读取实时 Ref。

## 4A. 中文相关 PR 与 Issue 状态摘要

| 记录 | 读取时状态 | 中文相关性 |
|---|---|---|
| PR #55 | Open / Draft | B 研究草稿；不是规范验收。 |
| PR #52 | Open / Draft | B→A 协议收敛和 Storage 拓扑审查；B 决定仍是候选。 |
| PR #51 | Open / Draft | 跨 Owner 协议对齐；H 1.2.14 / CSubmitOutcome 1.0.1 候选，本地 Callback 仍为 Test Double。 |
| PR #53 | Closed / Not Merged | A 最终评估为 DEFERRED；Fact/Claim ADR 和 B 语义仍阻塞。 |
| PR #50 | Open / Draft | 系统风险评估影响语义就绪。 |
| PR #49 / #47 | Open / Draft | 复杂度评估；仅为上下文证据，不代表 B 批准。 |
| PR #46 | Open / Draft | 工程依赖和实现可行性。 |
| PR #45 | Open / Draft | 技术现实研究；不转移领域权威。 |
| PR #28 | Open / Draft | 双语架构覆盖和语义对等。 |
| Issue #3 | Open | C/G/H Applied 证据和 BMCP Wire 契约；要求 B 类型化引用映射，其他证明由各 Owner 拥有。 |
| Issue #5 | Open | I36-GOV-01..10 仍 GOVERNANCE-BLOCKED。 |
| Issue #6 | Closed | C/F/G 对精确 BIH Package 设计验收，带列明例外；G 后继 Blob 需重新确认。 |
| Issue #7 | Open | Runtime 实现仓库和负责 Engineering Owner 未确定。 |
| Issue #10 | Open | JF-10 P0 物理能力/故障恢复未建立。 |
| Issue #25 | Open | D/E/I/Storage Publication Gate 仍按 Owner 边界开放。 |
| Issue #29 | Open | HRC/RecoveryJoin/拓扑的本地 CI 证据有边界，不证明生产信任或物理 JF-10。 |
| Issue #43 | Open | 系统级整合控制 Issue；A 仍推迟架构冻结。 |

Issue #6 的关闭仅表示精确 BIH 设计级消费者验收，不代表 I36 治理批准或 Runtime 认证。C/F 的验收 Pin 与当前源 Blob 一致；G 当前 Blob 已变化，需后继版本确认。

## 5. Source-level semantic observations / 源级语义观察

1. **C:** The exact C review says CSubmitOutcome object authentication does not automatically authenticate the outer BMCP envelope. C's immutable outcome identity, sequence namespace, final-request boundary and provider evidence remain C-owned. The review is a delegated C-role record, not an independent human C Owner signature.
2. **D:** The exact D review accepts the H nullable-COC test only as local L1/L2 evidence. It does not waive ForgetFence clearance, lineage membership, terminal barrier proof, production clearance or release CAS.
3. **E:** Evidence is source material/observation supporting, refuting or qualifying a proposition; Provenance records how a target was derived. E explicitly excludes truth adjudication, final Claim identity, D lifecycle authority and I physical deletion authority. Its graph/DAG finality remains open.
4. **F:** Runtime Forget suppression and invalidation are F-owned; runtime projections/cursors must not be mistaken for canonical Memory lifecycle or D's ForgetFence.
5. **G:** Context and ContextVersion are G-owned and distinct from Memory/MemoryVersion. Applied is a G-owned semantic result with C final-request evidence and H transport; historical Applied does not by itself prove current-use eligibility.
6. **H:** Protocol messages, envelopes, receipts and wire schemas remain protocol objects. A message carrying a domain reference does not become the referenced domain object.
7. **I:** Principal is an authenticated security subject; ActorRef is per-operation attribution; ScopeRef is not Permission. I owns issuer trust, authorization, revocation, PermissionEpoch and global Forget policy. I's crypto profile approval is architecture-profile selection, not production activation.
8. **Storage:** the current Storage ADR contains an Option A / serializable transaction-domain discussion, while A PR #52 reports conditional L1 acceptance and L4 physical engine/deployment as OPEN. The exact ADR decision section and D/Storage approvals must be re-read before claiming Option A is fully selected or accepted. Storage transaction/visibility state is not domain lifecycle state.

1. **C：** 精确 C 复审指出，CSubmitOutcome 对象认证不会自动认证外层 BMCP Envelope。C 的不可变 Outcome 身份、序列命名空间、最终请求边界和 Provider Evidence 仍由 C 负责。该复审是委派角色记录，不是独立人类 C Owner 签名。
2. **D：** 精确 D 复审仅将 H Nullable-COC 测试作为本地 L1/L2 证据接受，不豁免 ForgetFence Clearance、Lineage Membership、Terminal Barrier Proof、生产 Clearance 或 Release CAS。
3. **E：** Evidence 是支持、反驳或限定命题的来源材料/观察；Provenance 记录目标如何派生。E 明确不负责真值裁定、最终 Claim 身份、D 生命周期权威或 I 物理删除权威。最终图/DAG 规则仍开放。
4. **F：** Runtime Forget 抑制与失效由 F 负责；Runtime 投影/Cursor 不得被误认为规范 Memory 生命周期或 D 的 ForgetFence。
5. **G：** Context 与 ContextVersion 由 G 负责，且不同于 Memory/MemoryVersion。Applied 是 G 负责的语义结果，C 提供最终请求证据，H 负责传输；历史 Applied 本身不能证明当前仍可使用。
6. **H：** Protocol Message、Envelope、Receipt 和 Wire Schema 属于协议对象。消息携带领域引用，不会因此变成被引用的领域对象。
7. **I：** Principal 是经过认证的安全主体；ActorRef 是单次操作归因；ScopeRef 不等于 Permission。I 负责 Issuer Trust、Authorization、Revocation、PermissionEpoch 和 Global Forget Policy。I 的密码配置批准是架构配置选择，不代表生产启用。
8. **Storage：** 当前 Storage ADR 包含 Option A / Serializable Transaction Domain 讨论，而 A PR #52 报告的是有条件 L1 接受，L4 物理引擎/部署仍 OPEN。声称 Option A 已完全选定或验收前，必须重新读取 ADR 决策章节及 D/Storage 批准。Storage Transaction/Visibility 状态不是领域生命周期状态。



## 6. Latest Phase 3.8 owner boundary update / 最新 Phase 3.8 Owner 边界更新

The current owner branch tips were refreshed after the earlier source snapshot. Exact current artifacts show:
- B Phase 3.8.6 approves per-authority nominal serialization types only; the anchor is physical implementation detail, not a canonical domain entity or global counter (Blob e2bc4c8dde9706bfbe443269b702f1b5aa6965f6).
  - B Phase 3.8.6 仅批准 Per-authority 名义序列化类型；Anchor 是物理实现细节，不是规范领域实体或全局计数器。
- E accepts the anchor with E lifecycle conditions (Blob 19d708bc29b6115d7bccb7d320781f452ee28b78); F accepts with read-path/cache conditions (Blob 122238146830db6188f00a9788e018a82bfb3f90). Storage v3.2.11 is still not jointly accepted/frozen and needs fresh A review (Blob 54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57).
  - E 在自身生命周期条件下接受 Anchor；F 在读路径/Cache 条件下接受。Storage v3.2.11 尚未联合接受/冻结，需要 A 新一轮复审。
- C Phase 3.8.22 accepts H's reference ingress gate and 60-test boundary only; signer/attestation remains open and crypto is not frozen (Blob 8fd6052cabf58a78962cc2e776398b2a40604bcd).
  - C Phase 3.8.22 仅接受 H 的 Reference Ingress Gate 和 60 项测试边界；Signer/Attestation 仍开放，密码学 Profile 未冻结。
- G Phase 3.8.18 accepts C/H full-path mapping as bounded L1/L2 candidate with G-owned Applied conditions, not frozen; its 38 methods use ten deterministic authority test doubles (Blob 1894860c76336f8739d354b72beed3992cffd17e).
  - G Phase 3.8.18 将 C/H Full-path 映射作为有限 L1/L2 候选接受，并保留 G 自身 Applied 条件；尚未冻结；38 个方法使用 10 个确定性 Authority Test Double。
- H Phase 3.8.20 corrects the C outer-envelope P0 proof-locator omission and documents JSON pointers, but executable authentication, I profile registration and durable replay remain open (Blob 4ba7e1699215d02224f805a15484b1da2e40c03f).
  - H Phase 3.8.20 修正 C Outer Envelope P0 的 Proof Locator 遗漏并记录 JSON Pointer，但可执行认证、I Profile 注册和 Durable Replay 仍开放。
- I accepts C origin-signer/P0 separation as candidate, but does not approve the proposed crypto suite, register the profile/keys, approve custody or authorize deployment (Blob b6d1ea45825a1c2090abfba42474814f02f073a3).
  - I 将 C Origin Signer/P0 分离作为候选接受，但未批准拟议 Crypto Suite、未注册 Profile/Keys、未批准密钥托管，也未授权部署。
- A Phase 3.8.19 marks outer-envelope authentication as a blocking architecture gap and says do not freeze (Blob e12cd7b5c79e2234178014243fd51f2e7d51272e).
  - A Phase 3.8.19 将 Outer Envelope Authentication 标记为阻塞性架构缺口，并明确要求不得冻结。

These findings add a new BLOCKING semantic integration conflict: a typed ActorRef/PrincipalRef or a schema-valid envelope is not authenticated origin proof. C origin signature/P0, H protected transport authentication, I trust/profile/key approval and Storage durable authenticated ingress/replay are separate authority requirements.

上述发现增加一个新的 BLOCKING 语义集成冲突：类型化 ActorRef/PrincipalRef 或 Schema 有效的 Envelope 并不构成已认证的 Origin 证明。C Origin Signature/P0、H Protected Transport Authentication、I Trust/Profile/Key 批准，以及 Storage Durable Authenticated Ingress/Replay 是彼此独立的权威要求。



## 6A. Governance and testing authority / 治理与测试权威

Additional current-main source pins / 当前 main 补充来源 Pin：
- Architecture invariants: 00-governance/architecture-invariants.md, Blob 33b037318e459ebb73bea33b3186f31a41d5dcfe. / 架构不变量文件及精确 Blob。
- Bilingual documentation policy GOV-DOC-001: 00-governance/bilingual-documentation-policy.md, Blob b51b054b9f1022133666542680df74dfe19de2fb. / 双语文档政策 GOV-DOC-001 及精确 Blob。
- AI Development Standard AI-STD-001: 14-ai-development/ai-development-standard.md, Blob f46867f97fc1860015adbe2a1f7b8262640c16fd. / AI 开发标准 AI-STD-001 及精确 Blob。
- AI Development Iteration Lifecycle: 14-ai-development/iteration-lifecycle.md, Blob 8ecc8e4ddde78be01e2038be4ece8dc8ac282c97. / AI 开发迭代生命周期文件及精确 Blob。
- Cross-Module Conformance & Fault-Injection Guide (EN): docs/en/12-testing-and-acceptance/cross-module-conformance-guide.md, Blob 6a32f31f0690b8217ae7c2e7049155814f3f108f. / 跨模块一致性与故障注入指南英文版及精确 Blob。
- Cross-Module Conformance & Fault-Injection Guide (ZH): docs/zh-CN/12-testing-and-acceptance/cross-module-conformance-guide.md, Blob 9a63d38997fd2e7aa8fea5d88470ad7fd83dab6d. / 跨模块一致性与故障注入指南中文版及精确 Blob。
- System Quality Attributes: 01-system-architecture/system-quality-attributes.md, Blob 4350733173d29451a8ea4aa6a544de46526b4fd7. / 系统质量属性文件及精确 Blob。

The conformance guide explicitly assigns TC-01 Domain Identity and References and TC-10 Provenance/Lifecycle/Temporal to B, with D/E/F/G and D/E/F/I collaborators respectively. Testing/QA is a cross-cutting contributor alongside Storage/Consistency and Engineering, coordinated by A; no dedicated Testing/Quality branch or independent accountable Owner was found in the branch search. Therefore B owns domain invariant definitions and domain test semantics; a named Testing/QA specialist must be assigned for independent execution/review rather than treating B self-tests as independent acceptance.

一致性指南明确将 TC-01 Domain Identity and References 与 TC-10 Provenance/Lifecycle/Temporal 分配给 B，分别要求 D/E/F/G 和 D/E/F/I 协作。Testing/QA 与 Storage/Consistency、Engineering 一样属于横切参与方，由 A 协调；分支搜索未找到独立 Testing/Quality 分支或独立负责 Owner。因此 B 负责领域不变量定义和领域测试语义；必须指定 Testing/QA 专家负责独立执行/审查，不能把 B 自测视为独立验收。

Architecture invariant I-04 says Event, Memory, Fact, Entity, Relation and Evidence are distinct domain concepts. The older B overview describes Fact as a qualified interpretation of Claim rather than a separate object type, while the bilingual guide keeps the Fact/Claim ADR BLOCKED and prohibits downstream schema freeze. These statements can only be reconciled provisionally as: Fact is a distinct concept, but whether it has an independent object identity/type or is represented as a qualified Claim remains undecided. Do not erase I-04 or freeze a Fact/Claim schema before the ADR.

架构不变量 I-04 规定 Event、Memory、Fact、Entity、Relation、Evidence 是不同领域概念。较早 B Overview 将 Fact 描述为 Claim 的限定解释而非独立对象类型；双语指南则将 Fact/Claim ADR 保持 BLOCKED，并禁止冻结下游 Schema。当前只能暂时协调为：Fact 是不同概念，但它是否具有独立对象身份/类型，还是作为带限定的 Claim 表示，仍未裁决。不得删除 I-04，也不得在 ADR 完成前冻结 Fact/Claim Schema。

Architecture invariants I-23/I-24 and GOV-DOC-001 require full Chinese/English semantic parity, stable-ID parity, matching decision status and source traceability in the same change set. This research package has bilingual headings and bilingual sections, but several detailed tables and normative passages are not yet fully mirrored. **Bilingual parity is NOT COMPLETE; B5 cannot pass.**

架构不变量 I-23/I-24 与 GOV-DOC-001 要求同一变更集内提供完整中英文语义对等、稳定 ID 对等、决策状态一致和来源可追溯。本研究包已有双语标题和部分双语章节，但若干详细表格和规范段落尚未完整对照翻译。**双语语义对等尚未完成；B5 不能通过。**

## 7. B0 disposition / B0 门禁结论

B0 remains **PARTIAL / NOT PASSED**. The current main HEAD, domain-source Blob pins, owner branch snapshots, selected owner source files, relevant PR metadata and controlling issues have been refreshed. Remaining B0 work: complete A and Testing/Quality source authority inventory; fetch full exact PR diffs/commit/Blob pins for all directly relevant records; pin the latest C/G/H/Storage exact contract bundle; re-read the Storage ADR decision section and latest D review/acceptance; reconcile every Owner-local canonical definition against B's matrix.

B0 仍为 **PARTIAL / NOT PASSED**。当前 main HEAD、领域源 Blob Pin、Owner 分支快照、部分 Owner 源文件、相关 PR 元数据和控制性 Issue 已刷新。B0 剩余工作：补齐 A 与 Testing/Quality 的权威源清单；读取所有直接相关记录的完整精确 PR Diff/Commit/Blob Pin；Pin 最新 C/G/H/Storage 精确契约包；重新读取 Storage ADR 决策章节及 D 最新复审/验收；将每个 Owner 局部规范定义与 B 矩阵逐项协调。

No canonical freeze, schema freeze, implementation authorization, Owner approval, independent review or ACCEPTED status is claimed.

不宣称规范冻结、Schema 冻结、实现授权、Owner 批准、独立审查或 ACCEPTED 状态。


## 7. BIH consumer acceptance currentness correction / BIH 消费方验收时效性纠正

The earlier I BIH addendum Blob `475044ed4c6d468be26459e6201018dd57b3fc80` states that C/F/G remain OPEN. That statement is stale relative to the later Issue #6 closure evidence and must not be repeated as the current Issue #6 state.

较早的 I BIH 补充文件 Blob `475044ed4c6d468be26459e6201018dd57b3fc80` 写明 C/F/G 仍为 OPEN。相对于后续 Issue #6 关闭证据，该表述已过时，不得继续作为 Issue #6 当前状态引用。

Issue #6 was fetched directly and is **CLOSED**. Its comments include:
- Comment `6919556745`: C/F/G each published an Owner-branch design acceptance against exact A BIH package Blob `a45ae90b318a79bf009d14f4d917611881e9e214`.
- Comment `6919649724`: A reports exact Blob readback for C `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`, F `ce59252dbbdc5d10d016704797e9ba12d5a941bd`, G `5406b3f2558daa3f5915f6bb46e808be8d90d3ca`; all were recorded as ACCEPT WITH ENUMERATED EXCEPTIONS.
- The B typed-reference mapping is pinned by the B formal confirmation and the exact A package; H's exact acceptance is separately recorded in Issue #6 comment `6919218061`.

已直接读取 Issue #6，其状态为 **CLOSED**。其评论包括：
- 评论 `6919556745`：C/F/G 均针对精确 A BIH Package Blob `a45ae90b318a79bf009d14f4d917611881e9e214` 发布了 Owner 分支设计验收。
- 评论 `6919649724`：A 报告已精确读回 C `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`、F `ce59252dbbdc5d10d016704797e9ba12d5a941bd`、G `5406b3f2558daa3f5915f6bb46e808be8d90d3ca` Blob；三者均记录为 ACCEPT WITH ENUMERATED EXCEPTIONS。
- B typed-reference mapping 由 B 正式确认文件和精确 A Package Pin；H 的精确验收另见 Issue #6 评论 `6919218061`。

Current source comparison / 当前源版本比较:
- C's current `phase-3.6-final-request-evidence-contract.md` remains Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`, matching the Issue #6 accepted pin.
- F's current `phase-3.6-runtime-forget-suppression-and-invalidation.md` remains Blob `ce59252dbbdc5d10d016704797e9ba12d5a941bd`, matching the Issue #6 accepted pin.
- G's current `phase-3.6-applied-forget-reconciliation-contract.md` is now Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`, whereas the Issue #6 accepted pin was `5406b3f2558daa3f5915f6bb46e808be8d90d3ca`. The current G file contains later amendments; the historical BIH acceptance remains evidence for the exact earlier version only. Re-confirm that the BIH-relevant clauses are unchanged before treating the acceptance as applying to the current G successor.
- I36-GOV-01..10 remain GOVERNANCE-BLOCKED; I36/H36 and consumer runtime conformance remain NOT RUN. Issue #6 closure is design-level BIH consumer acceptance, not governance approval or runtime certification.

当前源版本比较：
- C 当前 `phase-3.6-final-request-evidence-contract.md` 仍为 Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`，与 Issue #6 已验收 Pin 一致。
- F 当前 `phase-3.6-runtime-forget-suppression-and-invalidation.md` 仍为 Blob `ce59252dbbdc5d10d016704797e9ba12d5a941bd`，与 Issue #6 已验收 Pin 一致。
- G 当前 `phase-3.6-applied-forget-reconciliation-contract.md` 已更新为 Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`，而 Issue #6 验收 Pin 为 `5406b3f2558daa3f5915f6bb46e808be8d90d3ca`。当前 G 文件包含后续修订；历史 BIH 验收仅证明其精确旧版本。将该验收应用于当前 G 后继版本前，必须确认 BIH 相关条款未发生变化。
- I36-GOV-01..10 仍 GOVERNANCE-BLOCKED；I36/H36 和消费者运行时符合性仍 NOT RUN。Issue #6 关闭仅代表设计级 BIH 消费方验收，不代表治理批准或运行时认证。

Disposition / 处置：
- Mark C/F BIH design acceptance as exact-version VERIFIED.
- Mark G BIH acceptance as VERIFIED FOR HISTORICAL PIN; SUCCESSOR RECONFIRMATION REQUIRED.
- Do not reopen Issue #6 on the basis of later governance/runtime gates; track those separately.
- Keep B3 NOT PASSED until successor pins, remaining cross-owner conflicts and all required Owner acceptances are reconciled.

处置：
- C/F BIH 设计验收标记为精确版本 VERIFIED。
- G BIH 验收标记为历史 Pin 已验证；后继版本需要重新确认。
- 不因后续治理/运行时门禁而重开 Issue #6；这些事项应单独跟踪。
- 在后继 Pin、剩余跨 Owner 冲突及所有必要 Owner 验收协调完成前，B3 保持 NOT PASSED。


## 8. Live repository and Owner-ref refresh / 实时仓库与 Owner Ref 刷新 — 2026-11-18

This section supersedes conflicting branch/PR/main snapshots above wherever the same field is concerned. Snapshot time: 2026-11-17/18 review session; refs and PR metadata were fetched directly from GitHub immediately before this update.

本节在相同字段存在冲突时，优先于上文旧分支/PR/main 快照。快照时间：2026-11-17/18 审查会话；本节 Ref 和 PR 元数据均在更新前直接从 GitHub 读取。

### 8.1 Repository and PR pointers / 仓库与 PR 指针

| Item / 项目 | Live value / 实时值 | Meaning / 含义 |
|---|---|---|
| `main` HEAD | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | Current main ref at refresh time; supersedes historical `901e38b...` snapshot. |
| Research branch HEAD | `138be006ae6874ef44be47f2c8a1aebe96af4314` | Exact current ref; matches PR #55 head. |
| PR #55 | Open / Draft; base branch `main`; base SHA `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`; head SHA `138be006ae6874ef44be47f2c8a1aebe96af4314` | Not merged and not accepted. GitHub reports `mergeable=false`; cause not investigated/verified in this refresh. |
| Current compare | `main` → research branch: DIVERGED; 145 commits ahead, 32 behind; merge base `b372b62c640a2b656e54b6db62a4ee67d7d8c001` | The compare endpoint returned 22 research-package files, 4,328 additions and 0 deletions. This is metadata/diff inventory, not semantic acceptance. |

The PR base SHA is not the current main HEAD. Do not collapse the PR's recorded base SHA and live main ref into one value. No rebase, retarget, merge or Ready transition is authorized by this audit.

PR 的 Base SHA 并非当前 main HEAD。不得将 PR 记录的 Base SHA 与实时 main Ref 混为一谈。本审计不授权 Rebase、改目标分支、合并或转为 Ready。

### 8.2 Owner branch HEAD refresh / Owner 分支 HEAD 刷新

| Owner | Branch | Live HEAD at refresh / 本轮实时 HEAD |
|---|---|---|
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` |
| C | `session-c-agent-integration-2026-11-16` | `71047cdb51139ca4080ac67f451e38a48698859d` |
| D | `session-d-memory-brain-2026-11-16` | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` |
| G | `session-g-memory-context` | `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe` |
| H | `session-h-bmcp-protocol` | `0d36324457e39bd50ad56ae902d477c4ea765b61` |
| I | `session-i-security-governance-2026-11-16` | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` |
| A | `session-a-integration-2026-11-16` | `6e05831d264040e0e3b3359245b1e01ea613b46c` |

These are branch refs, not Owner approval. No dedicated Testing/Quality branch or accountable independent QA owner was established in this ref refresh.

以上是分支 Ref，不是 Owner 批准。本轮 Ref 刷新仍未建立专门的 Testing/Quality 分支或独立负责的 QA Owner。

### 8.3 Exact selected source pins and successor evidence / 精确选定来源 Pin 与后继证据

The following selected artifacts were fetched by exact path from the refreshed Owner branches. The Blob values confirm the selected artifacts still exist at those exact contents; they do **not** prove that each is the latest or controlling successor.

以下选定工件均从刷新后的 Owner 分支按精确路径读取。Blob 值证明这些选定工件仍存在且内容精确；但**不**证明每份都是最新或控制性后继版本。

| Owner | Exact path | Blob SHA | Currentness qualification |
|---|---|---|---|
| C | `07-agent-integration/phase-3.8.22-c-exact-review-h-authenticated-ingress-1.2.14-60-tests.md` | `8fd6052cabf58a78962cc2e776398b2a40604bcd` | Selected C review re-read; later branch tip exists, so inspect successor C decisions before treating it as current approval. |
| D | `03-memory-brain/phase-3.8.13-d-review-h-outer-envelope-authenticated-ingress-gate.md` | `152627e00b96355e2ff370acd643a51168c4c78c` | Selected D gate review re-read at current branch tip. |
| G | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | Current G Applied contract still differs from Issue #6 historical accepted Blob `5406b3f...`; successor BIH clause re-confirmation remains required. |
| H | `08-bmcp-protocol/phase-3.8.21-h-exact-schema-mapping-unified-1.2.15-gateway-attestation.md` | `2dc30f193d9c4f4bdc05ca4c137103687db28924` | Current selected H mapping is Unified 1.2.15; earlier H 1.2.14/Phase 3.8.20 evidence is not the newest selected mapping. |
| I | `09-security-governance/phase-3.8.22-i-exact-review-h-unified-1.2.15-gateway-attestation-schema.md` | `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf` | Newer I review is pinned; inspect its decision clauses before interpreting as crypto/profile approval. |
| Storage | `reviews/storage-consistency/phase-3.6.21-storage-v3.3.1-authenticated-ingress-exact-version-bundle-manifest.md` | `f6e61691ecdcfcbf1fb423cc45242868676ca925` | Successor v3.3.1 bundle exists; older v3.2.11 pin is historical and must not be described as latest. |
| A | `01-architecture/phase-3.12.1-a-exact-review-storage-v3.3.1-h-authenticated-ingress.md` | `d3d4e6f4b6d7e82f90e3eee3427c8ace3b4160c8` | Newer A integration review exists and references Storage v3.3.1. Earlier Phase 3.8.19 evidence is historical. |

### 8.4 Issue #7 current state / Issue #7 当前状态

Issue #7 was fetched directly on 2026-11-18 and remains **OPEN**. It requests the canonical runtime implementation repository, accountable engineering owner, reproducible build/CI/test entry points, deployment topology and contract-to-code traceability. It explicitly says this architecture repository is not itself runtime implementation evidence and prohibits claiming production readiness without reproducible build/run evidence.

Issue #7 已于 2026-11-18 直接读取，仍为 **OPEN**。它要求确定规范运行时实现仓库、负责工程 Owner、可复现 Build/CI/Test 入口、部署拓扑及契约到代码的追溯机制。Issue 明确说明本架构仓库本身不是运行时实现证据，并禁止在没有可复现 Build/Run 证据时宣称生产就绪。

### 8.5 B0 disposition after refresh / 刷新后的 B0 结论

B0 remains **PARTIAL / NOT PASSED**. The main/PR/Owner refs and selected C/D/G/H/I/Storage/A artifacts have been refreshed. Remaining work includes: inspect the exact successor decision clauses for C/G/H/I/Storage/A; read the full relevant PR diffs and commits rather than relying on PR metadata; refresh the current-main domain source pins; complete A's and Testing/QA's accountable source/authority inventory; and reconcile the full Owner-local contract set. The current compare is DIVERGED (145 ahead / 32 behind), and mergeability is false with cause unverified.

B0 仍为 **PARTIAL / NOT PASSED**。main/PR/Owner Ref 及选定的 C/D/G/H/I/Storage/A 工件已刷新。剩余工作包括：检查 C/G/H/I/Storage/A 的精确后继决策条款；读取相关 PR 的完整 Diff 和 Commit，不能只依赖 PR 元数据；刷新 current-main 领域来源 Pin；补齐 A 与 Testing/QA 的负责来源/权威清单；协调全部 Owner 局部契约。当前 Compare 为 DIVERGED（领先 145 / 落后 32），Mergeability 为 false，原因尚未核实。

No canonical freeze, schema freeze, implementation authorization, Owner approval, independent review or ACCEPTED status is claimed. No main-branch write, rebase, PR retarget, merge or Ready transition was performed.

不宣称规范冻结、Schema 冻结、实现授权、Owner 批准、独立审查或 ACCEPTED 状态。本轮未写入 main、未 Rebase、未修改 PR Base、未合并、未转为 Ready。


## 9. A Phase 3.12.1 / Storage v3.3.1 successor reconciliation / A Phase 3.12.1 与 Storage v3.3.1 后继协调

### 9.1 Exact source pins / 精确来源 Pin

- Storage/D Option A topology ADR: Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`; fetched directly by Blob. Its status line states **L1 LOGICAL TOPOLOGY SELECTED — OPTION A; L4 PHYSICAL ENGINE/DEPLOYMENT OPEN**. Section 8 selects Option A as the normative v1 logical architecture; §8.7 describes one durable `CanonicalAuthoritySerializationAnchor` per `BrainAuthorityRef` and an append-only transition record / SERIALIZABLE-CAS protocol.
- Storage v3.3.1 exact manifest: `reviews/storage-consistency/phase-3.6.21-storage-v3.3.1-authenticated-ingress-exact-version-bundle-manifest.md`, Blob `f6e61691ecdcfcbf1fb423cc45242868676ca925`.
- A Phase 3.12.1 exact integration review: `01-architecture/phase-3.12.1-a-exact-review-storage-v3.3.1-h-authenticated-ingress.md`, Blob `d3d4e6f4b6d7e82f90e3eee3427c8ace3b4160c8`.
- H Unified 1.2.15 exact schema mapping: `08-bmcp-protocol/phase-3.8.21-h-exact-schema-mapping-unified-1.2.15-gateway-attestation.md`, Blob `2dc30f193d9c4f4bdc05ca4c137103687db28924`; H schema candidate Blob `860fc4cec658db7d2703cd6adf72aa31a2723f6d`; H P0 candidate Blob `a08bff1145dfeccac3e583e065055ca7dfdcb189`.
- I Phase 3.8.22 exact review of H Unified 1.2.15: `09-security-governance/phase-3.8.22-i-exact-review-h-unified-1.2.15-gateway-attestation-schema.md`, Blob `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf`; I exact P0 review Blob `6a8717930f8822033c047bd6384df2aacf630a4b`.
- G current Applied contract: Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`; G explicitly records C/G/H Applied freeze blocked and implementation/execution not verified.

### 9.2 Confirmed contradiction / 已确认矛盾

A's exact Phase 3.12.1 review accepts the bounded H 1.2.14 / CSubmitOutcome 1.0.1 reference-ingress candidate and 60-test evidence only with enumerated amendments, but **rejects Storage v3.3.1 as a final consistent bundle manifest** until its Option A wording is corrected. The exact ADR selects Option A as the normative v1 logical architecture and leaves only L4 physical engine/deployment open. The v3.3.1 manifest instead calls Option A a “conditional L1 candidate” and refers to “A-01–A-05 clarifications” that are not present in the pinned ADR. A requires a successor manifest to correct both statements and retain the L4 gates.

A 的精确 Phase 3.12.1 复审仅在列明修订条件下接受 H 1.2.14 / CSubmitOutcome 1.0.1 Reference-Ingress 候选及 60 项测试证据，但在 Option A 措辞修正前，**拒绝将 Storage v3.3.1 作为最终一致的 Bundle Manifest**。精确 ADR 已选择 Option A 作为 v1 规范逻辑架构，只有 L4 物理引擎/部署仍开放。v3.3.1 Manifest 却将 Option A 称为“conditional L1 candidate”，并引用精确 ADR 中不存在的“A-01–A-05 clarifications”。A 要求通过后继 Manifest 修正两项表述，并保留 L4 门禁。

This is a real semantic/status contradiction, not a wording-only difference: the manifest's decision state and unresolved-work register do not match its pinned authority artifact. Storage owns the manifest and must publish the correction; B must not edit or reinterpret the Storage decision.

这是实际的语义/状态矛盾，不只是措辞差异：Manifest 的决策状态和未决事项登记与其绑定的权威 ADR 不一致。Manifest 由 Storage 负责，必须由 Storage 发布修正；B 不得编辑或重新解释 Storage 决策。

### 9.3 Successor version gap / 后继版本缺口

The current Storage v3.3.1 manifest binds H 1.2.14 and its 60-test reference-gate evidence. H has since published a Unified 1.2.15 structural schema candidate, and I has reviewed its schema shape as a trust-carrier candidate only. I explicitly leaves profile registration, gateway issuer/key approval, key status, custody, anti-rollback and production verification OPEN. The current A Phase 3.12.1 review is explicitly scoped to the exact v3.3.1 / H 1.2.14 bundle and does not approve H 1.2.15. Therefore a future Storage successor must bind the exact H 1.2.15/C/I artifacts and obtain fresh A review; do not infer cross-version acceptance.

当前 Storage v3.3.1 Manifest 绑定 H 1.2.14 及其 60 项 Reference-Gate 测试证据。此后 H 已发布 Unified 1.2.15 结构 Schema 候选，I 也仅将其 Schema 形态作为 Trust-Carrier 候选复审。I 明确保留 Profile 注册、Gateway Issuer/Key 批准、Key Status、Custody、Anti-Rollback 和生产验证为 OPEN。当前 A Phase 3.12.1 复审明确仅针对精确 v3.3.1 / H 1.2.14 Bundle，不批准 H 1.2.15。因此 Storage 后继版本必须绑定精确 H 1.2.15/C/I 工件并取得 A 新复审；不得推断跨版本验收。

### 9.4 Required closure / 解除条件

1. Storage publishes a successor manifest correcting Option A to “normative v1 logical architecture selected; L4 physical engine/deployment OPEN”, removing unsupported A-01–A-05 references unless a separate exact register is pinned, and preserving all L4 constraints.
2. Storage binds the exact H 1.2.15 schema/P0, C review and I review Blob set (or explicitly records a justified predecessor version), with tested-commit/current-head distinctions.
3. H closes exact P0 canonicalization, signature verification, protected transport provenance, durable replay and schema/profile binding order; I separately decides profile/issuer/key trust registration.
4. C retains independent C-object P0 and Provider Outcome semantics; no implicit reuse of C-object signature for the outer envelope.
5. A performs a fresh exact-version integration review of the successor manifest and changed source pins.
6. D/G/Storage still separately close ForgetFence/lineage, Applied predicate/persistence, durable recovery and L4 physical gates; this manifest correction does not close them.

1. Storage 发布后继 Manifest，将 Option A 修正为“已选择 v1 规范逻辑架构；L4 物理引擎/部署 OPEN”；除非绑定独立精确登记表，否则删除无依据的 A-01–A-05 引用，并保留全部 L4 约束。
2. Storage 绑定精确 H 1.2.15 Schema/P0、C 复审和 I 复审 Blob 集（或明确记录有理由的前序版本），并区分 Tested Commit 与 Current HEAD。
3. H 关闭精确 P0 Canonicalization、Signature Verification、Protected Transport 来源证明、Durable Replay 和 Schema/Profile Binding 顺序；I 独立决定 Profile/Issuer/Key Trust 注册。
4. C 保持独立 C Object P0 与 Provider Outcome 语义；不得将 C Object Signature 隐式复用于 Outer Envelope。
5. A 对后继 Manifest 和变更后的来源 Pin 执行精确版本集成复审。
6. D/G/Storage 仍须分别关闭 ForgetFence/Lineage、Applied Predicate/Persistence、Durable Recovery 和 L4 物理门禁；Manifest 修正不会自动关闭这些事项。

Disposition: registered as **B-CONFLICT-017 — BLOCKING / OPEN** in B's conflict register and cross-owner matrix. B3 remains NOT PASSED. This is a delegated A-role review and exact source reconciliation, not an independent human A Owner approval or a Storage Owner decision.

处置：已在 B 冲突登记和跨 Owner 矩阵中登记为 **B-CONFLICT-017 — BLOCKING / OPEN**。B3 仍 NOT PASSED。本结论基于委派 A 角色复审和精确来源协调，不是独立人类 A Owner 批准，也不是 Storage Owner 决议。


## 10. Storage v3.3.2 and A Phase 3.12.2 exact re-review / Storage v3.3.2 与 A Phase 3.12.2 精确复审

This section supersedes §9's temporary status that B-CONFLICT-017 remained open. A Storage successor and exact A re-review were found on the live Owner branches.

本节取代 §9 中 B-CONFLICT-017 仍开放的临时状态。已在实时 Owner 分支发现 Storage 后继版本及 A 精确复审。

- Storage current branch HEAD: `830a559bd2f4ec72608f5a51e1a0b43779f2b989`.
- Storage v3.3.2 manifest path: `reviews/storage-consistency/phase-3.6.22-storage-v3.3.2-option-a-status-corrected-exact-version-manifest.md`.
- Storage v3.3.2 exact Blob: `5c614375e10698e4931d83deb57d20321445e068`.
- A Phase 3.12.2 exact review path: `01-architecture/phase-3.12.2-a-exact-rereview-storage-v3.3.2-option-a-status-correction.md`.
- A Phase 3.12.2 exact review Blob: `eb3c946065aff4fbc6d76f384402fb9f75fa32dc`.
- A review status: **ACCEPT AS A CONSISTENT EXACT-VERSION CANDIDATE MANIFEST WITH ENUMERATED RELEASE BLOCKERS; NOT FROZEN / NOT PRODUCTION-APPROVED**.
- A explicitly marks the prior Option A status inconsistency **CLOSED AT MANIFEST CONSISTENCY LEVEL**: v3.3.2 now says Option A is selected as normative v1 logical architecture, retains L4 physical engine/deployment OPEN, removes unsupported A-01–A-05 references and preserves the exact ADR §8.7 per-BrainAuthority anchor obligation.

- Storage 当前分支 HEAD：`830a559bd2f4ec72608f5a51e1a0b43779f2b989`。
- Storage v3.3.2 Manifest 路径：`reviews/storage-consistency/phase-3.6.22-storage-v3.3.2-option-a-status-corrected-exact-version-manifest.md`。
- Storage v3.3.2 精确 Blob：`5c614375e10698e4931d83deb57d20321445e068`。
- A Phase 3.12.2 精确复审路径：`01-architecture/phase-3.12.2-a-exact-rereview-storage-v3.3.2-option-a-status-correction.md`。
- A Phase 3.12.2 精确复审 Blob：`eb3c946065aff4fbc6d76f384402fb9f75fa32dc`。
- A 复审状态：**接受为带列明 Release Blocker 的一致精确版本候选 Manifest；不冻结 / 不批准生产**。
- A 明确将此前 Option A 状态不一致判为 **Manifest 一致性层面 CLOSED**：v3.3.2 现已表述 Option A 已选为 v1 规范逻辑架构，保留 L4 物理引擎/部署 OPEN，删除无依据的 A-01–A-05 引用，并保留精确 ADR §8.7 的 Per-BrainAuthority Anchor 义务。

### 10.1 Exact scope and remaining gaps / 精确范围与剩余缺口

A Phase 3.12.2 review is scoped to the exact Storage v3.3.2 Blob and its pinned H 1.2.14 / C 1.0.1 / C Phase 3.8.22 / I Phase 3.8.18 evidence. It does not approve or bind H Unified 1.2.15, I Phase 3.8.22's 1.2.15 structural review, or a future Storage bundle containing those successor pins. The v3.3.2 manifest itself says a fresh A review is required for its exact version and remains NOT JOINTLY ACCEPTED / NOT FROZEN.

A Phase 3.12.2 复审仅针对精确 Storage v3.3.2 Blob 及其绑定的 H 1.2.14 / C 1.0.1 / C Phase 3.8.22 / I Phase 3.8.18 证据。它不批准或绑定 H Unified 1.2.15、I Phase 3.8.22 对 1.2.15 的结构复审，或包含这些后继 Pin 的未来 Storage Bundle。v3.3.2 Manifest 自身也要求对其精确版本取得 A 新复审，并保持 NOT JOINTLY ACCEPTED / NOT FROZEN。

Remaining blockers explicitly retained by A include outer-envelope P0/canonical bytes/signature profile; signer-role decision; I trust root/issuer/key registration and lifecycle; non-forgeable protected transport context; durable replay/ingress atomicity and replay authorization; C provider truth; D lineage/fence/barrier/release; I terminality/currentness; Storage/COC quorum, RecoveryJoin and same-GID; and Option A L4 deployment evidence.

A 明确保留的阻塞项包括 Outer-Envelope P0/Canonical Bytes/Signature Profile、Signer Role 决议、I Trust Root/Issuer/Key 注册及生命周期、不可伪造的 Protected Transport Context、Durable Replay/Ingress 原子性及重放授权、C Provider Truth、D Lineage/Fence/Barrier/Release、I Terminality/Currentness、Storage/COC Quorum/RecoveryJoin/Same-GID，以及 Option A L4 部署证据。

### 10.2 Updated disposition / 更新后的处置

B-CONFLICT-017 is now **CLOSED — MANIFEST CONSISTENCY REMEDIATED**, based on Storage v3.3.2 exact Blob `5c614375e10698e4931d83deb57d20321445e068` and A Phase 3.12.2 exact re-review Blob `eb3c946065aff4fbc6d76f384402fb9f75fa32dc`. Qualification: both the Storage manifest and A review identify delegated-role provenance, not independent human Owner signatures. The closure is limited to the Option A status inconsistency and unsupported A-01–A-05 reference. It does not close B3, Storage L4, authenticated ingress, production trust, Applied, Forget or runtime conformance.

B-CONFLICT-017 现更新为 **CLOSED — MANIFEST CONSISTENCY REMEDIATED**，依据 Storage v3.3.2 精确 Blob `5c614375e10698e4931d83deb57d20321445e068` 与 A Phase 3.12.2 精确复审 Blob `eb3c946065aff4fbc6d76f384402fb9f75fa32dc`。限定条件：Storage Manifest 与 A 复审均注明委派角色来源，不是独立人类 Owner 签名。关闭范围仅限 Option A 状态不一致及无依据的 A-01–A-05 引用，不关闭 B3、Storage L4、Authenticated Ingress、Production Trust、Applied、Forget 或 Runtime Conformance。

B3 remains **NOT PASSED**. H 1.2.15 successor integration and a fresh exact Storage/A bundle review remain open. This author-side currentness refresh does not claim independent review or global Owner acceptance.

B3 仍为 **NOT PASSED**。H 1.2.15 后继集成以及 Storage/A 对精确后继 Bundle 的新复审仍开放。本次作者侧时效性刷新不代表独立审查或全局 Owner 验收。


## 11. Current B Owner Fact/Claim ADR and governance baseline / 当前 B Owner Fact/Claim ADR 与治理基线 — 2026-11-18

### 11.1 Live refs and exact B artifacts / 实时 Ref 与 B 精确工件

- Current `main` ref observed: `e52594f181d2edb77448adcfed64a0fbdffaf3aa`; recursive tree SHA equals that commit; tree is not truncated. No paths exist under `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/`.
- Current B Owner branch observed: `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2`.
- B summary ADR `02-domain-model/ADR-001-fact-claim-semantics.md`: Blob `a1024938ff5baba069cf128c69496a44e143330c`.
- B detailed canonical ADR `02-domain-model/adr/ADR-001-fact-claim-canonical-model.md`: Blob `df77e4a93cb8fef689ae7c828888d960cbf381d6`.
- B consumer mapping `02-domain-model/fact-claim-consumer-mapping.md`: Blob `dd45a37199c9b69ab6b68f65e051a484a04691d4`.
- B typed-reference approval `02-domain-model/phase-3.6-b-owner-formal-actor-scope-environment-type-mapping-confirmation.md`: Blob `3a1e77889cd9a90cd5822d9f0cb3437880868706`; this is a separate approved scope and does not decide Fact/Claim.

### 11.2 Corrected B recommendation / B 建议纠偏

The current B Owner artifacts recommend **Option A — a separate Fact attestation object and Claim proposition thread** as the preferred candidate. This supersedes the older C2/Option B recommendation in the B research package's earlier `fact-claim-identity-adr.md`. Neither option is approved: both B ADRs explicitly remain ADR-BLOCKED; the named formal Architecture Governance authority, approver, decision timestamp and approval record are absent. Option B would require an explicit Governance amendment/reinterpretation of I-04/P-04 and terminology before it could become normative.

当前 B Owner 工件优先推荐 **Option A——Fact Attestation 独立对象与 Claim 命题线程分离**。这取代 B 研究包旧版 `fact-claim-identity-adr.md` 中此前倾向 C2/Option B 的建议。两个方案均未获批准：B 的两份 ADR 都明确保持 ADR-BLOCKED；具名正式 Architecture Governance 权威、批准人、决策时间和批准记录均缺失。Option B 若要成为规范方案，必须先由 Governance 明确修订/重新解释 I-04/P-04 和术语基线。

The B Owner consumer map remains CANDIDATE / ADR-BLOCKED. It keeps E's CandidateProposition/ExtractionIR neutral; proposes stable ClaimRef + immutable ClaimRevisionRef and ConflictSet over exact ClaimRevisionRefs; assigns canonical ID allocation, persistence, revision commit and ConflictSet lifecycle/commit shape to D after approval; and keeps F/G exact-version-bound and H wire fields unfrozen. These are proposals, not downstream Owner acceptance.

B Owner 消费者映射仍为 CANDIDATE / ADR-BLOCKED。它要求 E 的 CandidateProposition/ExtractionIR 保持中立；提出稳定 ClaimRef + 不可变 ClaimRevisionRef 及按精确 ClaimRevisionRef 构建 ConflictSet；批准后由 D 负责规范 ID 分配、持久化、Revision Commit 和 ConflictSet 生命周期/Commit 形态；F/G 保持精确版本绑定，H Wire 字段不冻结。这些均为提案，不是下游 Owner 验收。

### 11.3 Exact current main contradiction / 当前 main 精确矛盾

| Source / 来源 | Exact Blob / 精确 Blob | Current statement / 当前表述 |
|---|---|---|
| `00-governance/architecture-invariants.md` I-04 | `33b037318e459ebb73bea33b3186f31a41d5dcfe` | Fact is distinct from Claim as a domain concept |
| `00-governance/design-principles.md` P-04 | `192e6ba6e9287792a02b679dda0d391844270228` | Fact and Claim are different objects |
| `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | Fact is a qualified interpretation of Claim, not a separate object type; labels this DECIDED |
| `00-governance/terminology.md` | `9b287ebe027ae01128baf164952ce15aad050638` | Defines “Fact / Claim” together |
| EN domain guide | `8a19cebacf5aefb0aded5fdbfeaff406291a5cf1` | Explicitly ADR-BLOCKED; prohibits downstream schema freeze |
| ZH domain guide | `a9f53a453aec25c47c58c4aea75adc43c83028d3` | Same ADR-BLOCKED status and freeze prohibition |

These are current live `main` Blob pins at the refresh. The conflict is not resolved by the B recommendation: B recommends Option A but cannot amend governance invariants. Issue #43 remains OPEN and preserves the blocker. Issue #5 remains OPEN for I36 governance approvals, a separate authority track; it is not the missing Architecture Governance decision record for this ADR.

以上均为本次刷新时实时 `main` 的 Blob Pin。B 的建议不能解除该冲突：B 推荐 Option A，但无权修改治理不变量。Issue #43 仍 OPEN 并保留阻塞。Issue #5 仍 OPEN，负责 I36 治理批准，是独立权威轨道；它不是本 ADR 缺失的 Architecture Governance 决议记录。

## 12. B3 ingress and research-maturity refresh / B3 入口与研究成熟度刷新 — 2026-11-18

- A Phase 8 B-02 issuer state-machine reconciliation: `reviews/architecture-feasibility/phase-8-b02-issuer-state-machine-and-cross-owner-reconciliation.md`, Blob `8a0a428ebf9cd8c8fe00562d2267ff490d5c3205`. It corrects the earlier A summary: I schema/P0/order review and C order review exist as **ACCEPT WITH CONDITIONS** reference-contract reviews; neither is production trust registration or H executable issuer approval. D's exact 1.2.15 review remains OPEN. H issuer pre-sign chain and integrated authority-join successor remain OPEN / NOT FOUND. B-02 here means the H gateway-ingress workstream; it is not B's B2 gate.
- A H 1.2.15 Validator/CI/Trust exact review: Blob `582ed576f73d9096dcc77b3a559df8c3b997b895`; H tested commit `0d36324457e39bd50ad56ae902d477c4ea765b61`. It reports 91 Provider Outcome tests and 288 Recovery Cutoff tests (22 skipped), both successful. Evidence is bounded local/reference CI with deterministic callback seams; production cryptographic trust, issuer signing, I registration and durable replay remain OPEN. A disposition: DEFERRED.
- Storage v3.3.2 remains pinned to H 1.2.14 / C 1.0.1; it is not the H 1.2.15 successor bundle. New exact H/C/I/D pins, Storage successor manifest and fresh A review are required.
- PRODUCT-FIRST-001 integration review Blob `3e7f0fc604761533ddd521924ff69d2039a63282` is NON-NORMATIVE / DRAFT and confirms Fact/Claim ADR remains blocked; no ADR, technology freeze or implementation authorization is issued.
- Memory Operating System research Blob `00e09d91ad3e7f08a9b7f7a26e30ebc98160d9c5` and Memory IR research Blob `084fc03bc5f09393bdd1ea6e8af3d8a6b703d3fc` both say baseline pinned, but design/prototype work not completed. They are not evidence for changing B canonical semantics.
- Issues #5, #7 and #43 are all OPEN. #5 tracks I36 external governance approvals; #7 tracks authoritative runtime repository/accountable engineering owner; #43 tracks system-wide consolidation and explicitly preserves Fact/Claim ADR-BLOCKED.

- A Phase 8 B-02 Issuer 状态机协调：`reviews/architecture-feasibility/phase-8-b02-issuer-state-machine-and-cross-owner-reconciliation.md`，Blob `8a0a428ebf9cd8c8fe00562d2267ff490d5c3205`。它修正此前 A 摘要：I 的 Schema/P0/顺序复审和 C 的顺序复审已作为 Reference 契约获得 **ACCEPT WITH CONDITIONS**；但都不是生产 Trust 注册，也不是 H 可执行 Issuer 批准。D 对 1.2.15 的精确复审仍 OPEN。H Issuer Pre-sign 链和 Integrated Authority-Join 后继版本仍 OPEN / NOT FOUND。此处 B-02 指 H Gateway Ingress 工作流，不是 B 的 B2 Gate。
- A H 1.2.15 Validator/CI/Trust 精确复审：Blob `582ed576f73d9096dcc77b3a559df8c3b997b895`；H 测试 Commit `0d36324457e39bd50ad56ae902d477c4ea765b61`。报告 91 项 Provider Outcome 测试和 288 项 Recovery Cutoff 测试（22 项跳过），均成功。证据仅限使用确定性 Callback Seam 的本地/Reference CI；生产密码学 Trust、Issuer 签名、I 注册和 Durable Replay 仍 OPEN。A 处置为 DEFERRED。
- Storage v3.3.2 仍绑定 H 1.2.14 / C 1.0.1，不是 H 1.2.15 后继 Bundle。需要新的精确 H/C/I/D Pin、Storage 后继 Manifest 和 A 新复审。
- PRODUCT-FIRST-001 集成审查 Blob `3e7f0fc604761533ddd521924ff69d2039a63282` 为 NON-NORMATIVE / DRAFT，并确认 Fact/Claim ADR 仍阻塞；未签发 ADR、技术冻结或实现授权。
- Memory Operating System 研究 Blob `00e09d91ad3e7f08a9b7f7a26e30ebc98160d9c5` 与 Memory IR 研究 Blob `084fc03bc5f09393bdd1ea6e8af3d8a6b703d3fc` 均表示基线已 Pin，但设计/原型尚未完成。它们不是改变 B 规范语义的证据。
- Issue #5、#7 和 #43 均为 OPEN。#5 跟踪 I36 外部治理批准；#7 跟踪规范 Runtime 仓库/负责工程 Owner；#43 跟踪全系统整合，并明确保留 Fact/Claim ADR-BLOCKED。

### 12.1 Main/PR currentness snapshot / Main/PR 当前性快照

At this refresh: main HEAD `e52594f181d2edb77448adcfed64a0fbdffaf3aa`; B Owner branch HEAD `2faf8ec38f14dba49e7263d7a60804dae1a74ee2`; research branch HEAD before this refresh's author-side writes `8ba14b99f1c303d9a368eb65178b0d79d507f2ff`. PR #55 remains Open / Draft, base `main`, recorded base SHA `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`; compare is DIVERGED, 166 ahead / 34 behind, merge base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`; 22 files, 4,864 additions, 0 deletions. GitHub reports `mergeable=true` at the read. These are metadata only; no rebase, retarget, merge or Ready transition is authorized. The main tree contains zero B research package paths.

本次刷新时：main HEAD `e52594f181d2edb77448adcfed64a0fbdffaf3aa`；B Owner 分支 HEAD `2faf8ec38f14dba49e7263d7a60804dae1a74ee2`；本轮作者侧写入前研究分支 HEAD `8ba14b99f1c303d9a368eb65178b0d79d507f2ff`。PR #55 仍 Open / Draft，Base 为 `main`，记录的 Base SHA 为 `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`；Compare 为 DIVERGED，领先 166 / 落后 34，Merge Base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`；22 个文件，新增 4,864 行，删除 0 行。GitHub 本次返回 `mergeable=true`。以上仅为元数据；不授权 Rebase、改 Base、合并或转 Ready。Main Tree 中 B 研究包路径为零。


## 13. Final live PR snapshot after B2/B3 source reconciliation / B2/B3 来源协调后的最终实时 PR 快照 — 2026-11-18

At the live read immediately before this §13 update:
- Main HEAD: `e52594f181d2edb77448adcfed64a0fbdffaf3aa`.
- B Owner branch HEAD: `2faf8ec38f14dba49e7263d7a60804dae1a74ee2`.
- Research branch / PR head: `df4dcbe58eb711364fe0d7b1f49ec78b151810e6`.
- PR #55: Open / Draft, base `main`, recorded base SHA `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`; 22 changed files, 5,128 additions, 0 deletions.
- Compare: DIVERGED; 177 commits ahead / 34 behind; merge base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`; GitHub reports `mergeable=true` (metadata only).
- The current main recursive tree is not truncated and contains zero paths under the B research package directory.
- No rebase, retarget, merge, Ready transition or main write occurred.

本节更新前的实时读取：
- Main HEAD：`e52594f181d2edb77448adcfed64a0fbdffaf3aa`。
- B Owner 分支 HEAD：`2faf8ec38f14dba49e7263d7a60804dae1a74ee2`。
- 研究分支 / PR Head：`df4dcbe58eb711364fe0d7b1f49ec78b151810e6`。
- PR #55：Open / Draft，Base 为 `main`，记录的 Base SHA 为 `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`；22 个变更文件，新增 5,128 行，删除 0 行。
- Compare：DIVERGED；领先 177 个 Commit / 落后 34 个 Commit；Merge Base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`；GitHub 返回 `mergeable=true`（仅为元数据）。
- 当前 main 递归 Tree 未截断，B 研究包目录下路径数量为零。
- 未发生 Rebase、改 Base、合并、转 Ready 或 main 写入。

### 13.1 Exact B package readback before this refresh / 本次刷新前 B 研究包精确读回

| File / 文件 | Blob SHA / Blob SHA | Lines / 行数 |
|---|---|---:|
| README.md | `480efa28b281e21a2358c1bddc5b4788a37bd160` | 337 |
| fact-claim-identity-adr.md | `958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593` | 223 |
| domain-model-decision-record.md | `b83d99d3c66b30c5834f08ce61c5acfd27004e6a` | 271 |
| baseline-currentness-and-owner-source-audit.md | `646d3e3308ba0a8c2a40ede6655b37b4e4391303` (pre-update self Blob) | 484 |
| cross-owner-canonical-semantics-matrix.md | `d9ec7f9cb6f72e2756d12da73c48a784ea9c7a83` | 291 |
| domain-semantics-conflict-register.md | `980f8563ec772939826b338a9b048efebd5bf2f6` | 166 |
| bilingual-parity-audit.md | `231760102377a8866cf9c8b221bd6e0ff3aeb72c` (pre-update self Blob) | 407 |

### 13.2 Gate disposition / 门禁处置

The current B Owner recommendation is Option A, but the Fact/Claim ADR remains ADR-BLOCKED because formal Architecture Governance approval is absent. Stable ClaimRef/ClaimRevisionRef and ConflictSet remain candidates. A Phase 8 B-02 refers to H ingress and is not B's B2 gate. H 1.2.15 contract reviews are conditional; issuer implementation, production I trust registration, D exact 1.2.15 review, Storage successor bundle and fresh A review remain open. Memory OS/IR research remains incomplete. B2 remains IN PROGRESS / NOT PASSED; B3 NOT PASSED; B4 NOT READY; B5 BLOCKED / NOT PASSED; B6 INDEPENDENT_REVIEW_PENDING.

当前 B Owner 推荐 Option A，但 Fact/Claim ADR 仍 ADR-BLOCKED，因为缺少正式 Architecture Governance 批准。稳定 ClaimRef/ClaimRevisionRef 和 ConflictSet 仍为候选。A Phase 8 B-02 指 H 入口，不是 B 的 B2 Gate。H 1.2.15 契约复审为有条件接受；Issuer 实现、I 生产 Trust 注册、D 对 1.2.15 的精确复审、Storage 后继 Bundle 和 A 新复审仍开放。Memory OS/IR 研究仍未完成。B2 仍 IN PROGRESS / NOT PASSED；B3 NOT PASSED；B4 NOT READY；B5 BLOCKED / NOT PASSED；B6 INDEPENDENT_REVIEW_PENDING。


## 14. D/E/F/G consumer-source reconciliation for Fact/Claim and Claim revision / D/E/F/G Fact/Claim 与 Claim Revision 消费者来源协调 — 2026-11-18

All refs below were re-fetched from their named live Owner branches. These sources confirm that the current B recommendation is not yet a cross-owner accepted or frozen canonical model.

以下来源均从指定实时 Owner 分支重新读取。它们确认当前 B 建议尚未成为跨 Owner 验收或冻结的规范模型。

| Owner | Live branch HEAD / 实时分支 HEAD | Exact artifact / 精确工件 | Blob SHA / Blob SHA | Source-backed status / 来源支持的状态 |
|---|---|---|---|---|
| B | `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | Summary ADR; detailed canonical ADR; consumer map | `a1024938ff5baba069cf128c69496a44e143330c`; `df77e4a93cb8fef689ae7c828888d960cbf381d6`; `dd45a37199c9b69ab6b68f65e051a484a04691d4` | Option A separate Fact attestation + Claim proposition is preferred candidate; ADR blocked; mapping candidate |
| D | `session-d-memory-brain-2026-11-16` @ `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | Canonical Store; Memory Versioning; Lifecycle Model | `6b37c91033fda21f072e2a3bde6f274663b1e76e`; `af747f339d03bdd4684b6ed60fca05957dc8e1fb`; `81c48c928cb5f9c76ca29d493fbd9479079e62f7` | Fact/Claim persistence ADR-BLOCKED; neutral PropositionRef only; stable Claim ID + immutable ClaimRevision is a candidate; D does not freeze schema/DDL/API/wire |
| E | `session-e-memory-compiler-2026-11-16` @ `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | Extraction & Normalization; Evidence & Provenance | `c18780403de2d1dbcf471bdb8abdaa009a4a78e1`; `38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963` | ExtractionIR/CandidateProposition is intentionally pre-canonical and neutral; E does not assign Fact/Claim identity or adjudicate truth; Evidence/Provenance final schema remains D/B/I-dependent |
| F | `session-f-memory-runtime` @ `1908ce4d233b20f7cafd00cb679affd01bd15174` | Memory Retrieval Engine | `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` | D owns Memory/Version/Claim/Entity/Relation/Evidence identity; F does not resolve disputed claims; Claim revision identity remains OPEN; F deduplicates exact MemoryVersion refs and preserves conflict alternatives |
| G | `session-g-memory-context` @ `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | Context Versioning and Change Sets | `05c0739d0c22576a1fd5affc7d73c078c89049b1` | G Entry pins exact MemoryVersion; ContextVersion/ChangeSet are G-owned and distinct; canonical revision watermark schema remains CANDIDATE/OPEN; no unapproved Claim/Fact identity is minted |

### 14.1 Important option-label disambiguation / 重要方案编号消歧

There are two unrelated “Option A” labels in the source set:
1. **B Fact/Claim Option A:** separate Claim proposition thread and independently addressable Fact attestation object. This is B's preferred CANDIDATE under INT-P0-01 and remains ADR-BLOCKED.
2. **D Claim identity Option A:** stable Claim ID + immutable ClaimRevision for corrections, contrasted with Option B (new Claim ID for every correction/successor). D marks this as a CANDIDATE under INT-P1-02, pending the Fact/Claim ADR.

The two labels must never be conflated. The current B Fact/Claim Option A does not itself approve D's Claim identity Option A; both remain candidate decisions, with the first requiring Architecture Governance + B approval and the second requiring B ADR approval plus D's canonical mechanics.

来源中存在两个互不相关的 “Option A”：
1. **B Fact/Claim Option A：** Claim 命题线程与可独立寻址的 Fact Attestation 对象分离。这是 B 在 INT-P0-01 下优先推荐的 CANDIDATE，仍 ADR-BLOCKED。
2. **D Claim Identity Option A：** 稳定 Claim ID + 不可变 ClaimRevision，用于更正；其对照方案 Option B 是每次更正/后继都创建新 Claim ID。D 将其标为 INT-P1-02 下的 CANDIDATE，等待 Fact/Claim ADR。

两个编号不得混淆。当前 B Fact/Claim Option A 并不会自动批准 D 的 Claim Identity Option A；两者仍是候选决策。前者需要 Architecture Governance + B 批准，后者需要 B ADR 批准及 D 的规范持久化机制确认。

### 14.2 Consumer boundary / 消费者边界

- **D:** Canonical Store accepts only neutral PropositionRef/opaque proposal envelope while INT-P0-01 is blocked. Stable Claim ID + immutable ClaimRevision is an option sketch; Claim/Fact identity, ClaimRevision schema and ConflictSet schema remain ADR-BLOCKED. D owns canonical identity allocation, persistence and commit mechanics only after the semantic ADR is approved.
- **E:** ExtractionIR and CandidateProposition are compiler IR, not public Claim/Fact schemas. E may emit candidate proposals, source spans, Evidence and Provenance, but cannot assign canonical ClaimRef/FactRef or convert confidence/model output into Verified/Fact.
- **F:** D remains canonical identity/status authority. F consumes authorized exact version refs and cannot adjudicate disputed claims or upgrade epistemic status. Claim revision identity is explicitly OPEN.
- **G:** ContextEntry pins exact MemoryVersion; ContextVersion/ChangeSet are G-owned. Context references do not create canonical Claim identity, and a MemoryVersion pin does not imply an approved ClaimRef/ClaimRevisionRef model.

- **D：** INT-P0-01 阻塞期间，Canonical Store 只接受中立 PropositionRef/不透明提案 Envelope。稳定 Claim ID + 不可变 ClaimRevision 只是方案草图；Claim/Fact 身份、ClaimRevision Schema 和 ConflictSet Schema 仍 ADR-BLOCKED。语义 ADR 批准后，D 才负责规范身份分配、持久化和 Commit 机制。
- **E：** ExtractionIR 和 CandidateProposition 是 Compiler IR，不是公开 Claim/Fact Schema。E 可提交候选提案、Source Span、Evidence 和 Provenance，但不得分配规范 ClaimRef/FactRef，也不得把 Confidence/模型输出转为 Verified/Fact。
- **F：** D 仍是规范身份/状态权威。F 消费已授权的精确版本引用，不得裁决争议 Claim 或提升认知状态。Claim Revision 身份明确保持 OPEN。
- **G：** ContextEntry 固定精确 MemoryVersion；ContextVersion/ChangeSet 由 G 拥有。Context 引用不会创建规范 Claim 身份，MemoryVersion Pin 也不意味着 ClaimRef/ClaimRevisionRef 模型已获批准。

B2 remains **IN PROGRESS / NOT PASSED**. The consumer-source review identifies no downstream acceptance that can substitute for the missing formal Fact/Claim decision. B4 schema freeze remains NOT READY.

B2 仍为 **IN PROGRESS / NOT PASSED**。消费者来源审查未发现任何可替代正式 Fact/Claim 决议缺失的下游验收。B4 Schema 冻结仍 NOT READY。
