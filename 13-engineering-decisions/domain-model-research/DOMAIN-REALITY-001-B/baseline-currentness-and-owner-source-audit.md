# DOMAIN-REALITY-001-B — Baseline Currentness and Owner Source Audit
# DOMAIN-REALITY-001-B — 基线时效性与 Owner 源文件审计

- ID: B-BASELINE-ADD-001
- Status: VERIFIED SNAPSHOT WITH OPEN RECONCILIATION — B0 NOT PASSED
- Audit date: 2026-11-17
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Current main HEAD readback: `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
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
- E accepts the anchor with E lifecycle conditions (Blob 19d708bc29b6115d7bccb7d320781f452ee28b78); F accepts with read-path/cache conditions (Blob 122238146830db6188f00a9788e018a82bfb3f90). Storage v3.2.11 is still not jointly accepted/frozen and needs fresh A review (Blob 54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57).
- C Phase 3.8.22 accepts H's reference ingress gate and 60-test boundary only; signer/attestation remains open and crypto is not frozen (Blob 8fd6052cabf58a78962cc2e776398b2a40604bcd).
- G Phase 3.8.18 accepts C/H full-path mapping as bounded L1/L2 candidate with G-owned Applied conditions, not frozen; its 38 methods use ten deterministic authority test doubles (Blob 1894860c76336f8739d354b72beed3992cffd17e).
- H Phase 3.8.20 corrects the C outer-envelope P0 proof-locator omission and documents JSON pointers, but executable authentication, I profile registration and durable replay remain open (Blob 4ba7e1699215d02224f805a15484b1da2e40c03f).
- I accepts C origin-signer/P0 separation as candidate, but does not approve the proposed crypto suite, register the profile/keys, approve custody or authorize deployment (Blob b6d1ea45825a1c2090abfba42474814f02f073a3).
- A Phase 3.8.19 marks outer-envelope authentication as a blocking architecture gap and says do not freeze (Blob e12cd7b5c79e2234178014243fd51f2e7d51272e).

These findings add a new BLOCKING semantic integration conflict: a typed ActorRef/PrincipalRef or a schema-valid envelope is not authenticated origin proof. C origin signature/P0, H protected transport authentication, I trust/profile/key approval and Storage durable authenticated ingress/replay are separate authority requirements.

上述发现增加一个新的 BLOCKING 语义集成冲突：类型化 ActorRef/PrincipalRef 或 Schema 有效的 Envelope 并不构成已认证的 Origin 证明。C Origin Signature/P0、H Protected Transport Authentication、I Trust/Profile/Key 批准，以及 Storage Durable Authenticated Ingress/Replay 是彼此独立的权威要求。



## 6A. Governance and testing authority / 治理与测试权威

Additional current-main source pins:
- Architecture invariants: 00-governance/architecture-invariants.md, Blob 33b037318e459ebb73bea33b3186f31a41d5dcfe.
- Bilingual documentation policy GOV-DOC-001: 00-governance/bilingual-documentation-policy.md, Blob b51b054b9f1022133666542680df74dfe19de2fb.
- AI Development Standard AI-STD-001: 14-ai-development/ai-development-standard.md, Blob f46867f97fc1860015adbe2a1f7b8262640c16fd.
- AI Development Iteration Lifecycle: 14-ai-development/iteration-lifecycle.md, Blob 8ecc8e4ddde78be01e2038be4ece8dc8ac282c97.
- Cross-Module Conformance & Fault-Injection Guide (EN): docs/en/12-testing-and-acceptance/cross-module-conformance-guide.md, Blob 6a32f31f0690b8217ae7c2e7049155814f3f108f.
- Cross-Module Conformance & Fault-Injection Guide (ZH): docs/zh-CN/12-testing-and-acceptance/cross-module-conformance-guide.md, Blob 9a63d38997fd2e7aa8fea5d88470ad7fd83dab6d.
- System Quality Attributes: 01-system-architecture/system-quality-attributes.md, Blob 4350733173d29451a8ea4aa6a544de46526b4fd7.

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
