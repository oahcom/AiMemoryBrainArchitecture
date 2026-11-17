# Domain Semantics Conflict Register
# 领域语义冲突登记册

- ID: B-CONFLICT-001
- Status: OPEN REGISTER — no blocking conflict is declared resolved by this document
- Baseline: main @ b372b62c640a2b656e54b6db62a4ee67d7d8c001
- Companion: cross-owner-canonical-semantics-matrix.md

## Severity definitions / 严重级别

- BLOCKING: blocks affected cross-owner contract freeze, schema freeze or architecture gate.
- HIGH: high-impact semantic ambiguity; affected path must fail closed or remain deferred.
- MEDIUM: meaningful modeling ambiguity requiring resolution before dependent implementation.
- LOW: localized terminology/documentation inconsistency.
- INFORMATIONAL: no contradiction found; record for traceability.

## Active conflicts / 未解决冲突

| ID | Severity | Conflicting owners / sources | Exact evidence | Semantic difference and impact | Decision authority | Proposal / blocking gate | Status |
|---|---|---|---|---|---|---|---|
| B-CONFLICT-001 | BLOCKING | B root overview vs B bilingual guide; A | main domain overview Blob 4d1debc0ec19b3917f9e76d04bb66da4df4cd346; guide Blobs a9f53a453aec25c47c58c4aea75adc43c83028d3 / 8a19cebacf5aefb0aded5fdbfeaff406291a5cf1; architecture invariants I-04 Blob 33b037318e459ebb73bea33b3186f31a41d5dcfe; A PR #53 | Root overview describes Fact as qualified Claim and labels DECIDED; architecture invariant I-04 requires Fact to remain a distinct domain concept; bilingual guide keeps the Fact/Claim ADR BLOCKED and forbids schema freeze. The concepts may be distinct while object identity/type representation remains OPEN. Claim identity across Memory Versions is also OPEN. | B decides domain semantics through explicit ADR; A registers exact version; D/E consumers must accept | Preserve ADR-BLOCKED; publish exact B ADR with alternatives, evidence, schema impact and consumer acceptance. Blocks B2/B3 and dependent Schema freeze. | OPEN |
| B-CONFLICT-002 | BLOCKING | C/G/H/I/D/A; Applied evidence | Issue #3; G Applied Blob aa3afa73d8a76cc6f025839c52bfbff6a983046a; C Final Request Blob fd2f47ba6c89bb270e9f2bec956873cb7ae3592b; H capability Blob 74be8374a67da385a5f0f8e34c7aef2b38b72bcf; A candidate package Blob 4961ffefc0f9920efb8425a9b2a7af42d8f64819 | G alone commits Applied; C proves exact actual final submit; H authenticates/transports; I authorization and D fence are independent prerequisites. Historical Applied and current-use eligibility differ. C/D/G/H/I/B exact CGH-APPLIED-1.1 recovery-batch decisions are recorded with enumerated exceptions and Storage confirmed its interface with changes (Issue #3 comments 6920620910 / 6929521979). H local CI reports 60 tests and G full-path fixture reports 38 methods; both use deterministic authority callback/test doubles only. Applied Contract Frozen remains NO; production authority integration, COC/Storage realization and G Applied persistence remain unverified. | G Applied predicate/state; C submission evidence; H wire; I auth; D fence; A registry only | Retain owner-specific exceptions; close only after H schema/crypto governance, C provider-specific idempotency and live provider truth, G Applied persistence, durable COC quorum, Storage same-GID recovery, and L3/L4 end-to-end conformance are proven. Unknown causal order => Unknown/suppress. Blocks B3 and C/G/H production freeze. | OPEN |
| B-CONFLICT-003 | BLOCKING | I / D / E / Storage / C / A | D Forget Blob 1f0391bc49d007c44ec74165bd33d37412cc7990; Storage JF-10 Blob 94679897e84a6f58fd8b9467b5249e1a885cb0b0; C causal Blob 45a48249717c8cddb07ab96197730ef93d406c22; Issue #10 | I COMMIT_WON is authorization ordering, not Storage publication. Storage VisibilityPointer + PublicationReceipt and exact readback are required for Published. DE-S is candidate; JF-10 P0 open and no physical implementation proof. | I owns policy sequencer/authorization; D fence; Storage physical transaction/visibility; C actual provider boundary; A integrates | Exact I acceptance of JF-10 protocol, named DB engine/version, same-XID recovery, COC durable log, fault injection and independent readback. Blocks B3/B4 and system freeze. | OPEN |
| B-CONFLICT-004 | BLOCKING | D / I / Storage / F / G / H / external recipients | D Forget Blob 1f0391bc49d007c44ec74165bd33d37412cc7990; I Global Forget Blob 9100061fa986fb6676656169de3fcf9fc1c72664; I joint trust Blob 0cbf6bb7480db873790c454817593a9b1c5548ba | D CanonicalSuppressionComplete is not global Forget completion; I owns global target inventory/exception policy; Storage/backup operators own physical erasure. InventorySealReceipt and external governance approvals are not evidenced. | D canonical suppression; I global policy/completion; Storage/backup physical erase; external recipients own copies | Preserve distinct state/evidence scopes. No physical purge/global completion claim until closed inventory, approvals, target proofs and backup/restore evidence. Blocks B3/B4 for global Forget claims. | OPEN |
| B-CONFLICT-005 | HIGH | B / I / A / G | B typed identity Blob 0a6b78a842e550b58533b797cdfcd2d954ed6826; B formal type confirmation Blob 3a1e77889cd9a90cd5822d9f0cb3437880868706; I joint closure Blob 0cbf6bb7480db873790c454817593a9b1c5548ba; Issues #5/#6 | PrincipalRef, ActorRef, ScopeRef, EnvironmentRef are distinct and B formally APPROVED its semantic mapping. C/F/G BIH consumer design decisions are ACCEPT WITH ENUMERATED EXCEPTIONS and H ACCEPTED the exact BIH package (Issue #6 CLOSED). However Tenant/Workspace/Project/Agent/Session/Environment scope hierarchy and registry authority remain incomplete; I36 governance approval remains blocked. | B types; I scope isolation/trust/policy; A registry; G scope use | Keep typed refs; prohibit implicit string casts and inheritance. Exact taxonomy/issuer and cross-scope mappings require I/A decision. Consumer approvals apply only to exact pinned versions and do not prove runtime conformance. Blocks affected cross-tenant contracts. | OPEN |
| B-CONFLICT-006 | HIGH | B / D / E / A | B core entities Blob 8cb5a674eec8eac1f3c4d83c400dc08d00166f23; B guide; A PR #53 | Claim has stable claim_id in legacy core schema, while MemoryVersion embeds ClaimSnapshot; identity continuity across versions is unresolved and Fact/Claim ADR is blocked. | B domain ADR; D versioning; E derivation consumer; A registry | Keep Claim identity/schema as OPEN; model ClaimSnapshot separately only as candidate; no downstream forced identity. Blocks B2/B4. | OPEN |
| B-CONFLICT-007 | HIGH | B / D / Storage / E | B temporal Blob 8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7; D commit cursor Blob 4688a0ca487bf4d853c7f0220408abe8d743d159 | Event/Observed/Recorded/Valid times are distinct; canonical commit cursor/Storage Transaction Time is another operational axis. Exact Record Time vs Transaction Time and fuzzy-time schema are not fully bound. | B temporal semantics; D canonical cursor; Storage commit-time authority; E source-time capture | Preserve separate axes; selectively support bitemporal Claims/Relations; do not force all entities into bitemporal schema. Blocks dependent temporal query/schema freeze. | OPEN |
| B-CONFLICT-008 | HIGH | B / C / G / H | B typed identity Blob 0a6b78...; G Phase 3.7 Blob c1de241...; Issue #3 | RuntimeSessionRef, Session ScopeRef, Conversation, Agent identity and Adapter/runtime instance are distinct. Exact Session/Conversation canonical relation and typed mappings are not fully accepted by C/G consumers. | B type semantics; C/G runtime/context semantics; H authenticated session; I Principal binding | Keep nominal types separate; do not alias conversation ID, session ID, runtime session or scope ID. Require exact consumer acceptance. | OPEN |
| B-CONFLICT-009 | MEDIUM | B / E / D / I | B relationships Blob e762f84c59f69de7a44baad2123aed46e1ffea16; E derived registration Blob 00e37ba56596e710513c8d0568acd79141d9101b; D Forget Blob 1f0391bc49d007c44ec74165bd33d37412cc7990 | Provenance graph cycles, derivation-edge identity, lineage compaction and post-Forget retention of metadata remain open. | B provenance semantics; E compiler production; D lineage/fence; I retention; Storage persistence | Start with explicit acyclic derivation constraints; permit exceptions only with a well-defined non-recursive lineage proof and retention rules. | OPEN |
| B-CONFLICT-010 | MEDIUM | B / D / E | B core entities Blob 8cb5...; relationships Blob e762... | Memory Source is modeled as a separately identified source association, but whether Source itself is a canonical entity vs typed origin reference is not justified for all source kinds. | B semantics; E source ingestion; D canonical source authority | Make MemorySource a typed association/value object by default; promote Source to entity only when independent lifecycle/reference/access is demonstrated. | CANDIDATE |
| B-CONFLICT-011 | MEDIUM | B / G / F / E | G Phase 3.7 Blob c1de241...; F Phase 3.7 Blob 29e9504...; E Phase 3.7 Blob 4fb9e585...; Issue #21 | ContextVersion, F Working Set and E frozen compiler input bundle are distinct; exact relation of ContextEntry identity, ChangeSet and Context Snapshot needs G normative pin/consumer mapping. | G Context; F Runtime; E Compiler; B shared vocabulary | Preserve nominal type separation; no scalar version aliases; reconcile G exact schema and consumer acceptance. | OPEN |
| B-CONFLICT-012 | MEDIUM | B / A / C / D / E / F / G / H / I / Storage | Responsibility matrix Blob fbeb6935fe874e6c843c25c3a891d6b3242cbfd3; issue #11; issue #7 | Architecture repository has no runtime implementation; no common executable conformance evidence was located. A requires canonical implementation repository and accountable engineering owner. | Project Governance Authority / appointed engineering authority; A coordinates | Do not mark validation/implementation/production ready; identify runtime repo and testing authority. | OPEN |

| B-CONFLICT-013 | BLOCKING | C / H / I / Storage / A | C review Blob 8fd6052cabf58a78962cc2e776398b2a40604bcd; H P0 correction Blob 4ba7e1699215d02224f805a15484b1da2e40c03f; I trust review Blob b6d1ea45825a1c2090abfba42474814f02f073a3; Storage v3.2.11 manifest Blob 54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57; A blocking review Blob e12cd7b5c79e2234178014243fd51f2e7d51272e | C origin-signer/P0 and immutable C object are separate signed objects; H owns wire extraction/verification; I owns trust profile/issuer/key lifecycle and authorization; Storage owns durable authenticated ingress/replay. H 1.2.14 outer-auth gate remains reference orchestration; C signer profile candidate, I crypto suite/trust registration not approved, H P0 extractor/signature verification and durable replay not implemented. A explicitly says blocking gap / do not freeze. | C owns origin message/P0; H wire; I cryptographic governance/trust; Storage durable ingress; A integration | Require exact C P0/signature profile, I registered trust/key policy, H executable extractor/verification/channel binding/replay, Storage durable acceptance/recovery, independent tests and fresh A review. Gate A/B blocked. | OPEN |
| B-CONFLICT-014 | HIGH | B / Storage / D / I / COC / E / F / A | B nominal-type review Blob e2bc4c8dde9706bfbe443269b702f1b5aa6965f6; Storage topology ADR Blob bb544ba2f346bdc130d524bd5c7310d86f367988; E review Blob 19d708bc29b6115d7bccb7d320781f452ee28b78; F review Blob 122238146830db6188f00a9788e018a82bfb3f90; Storage v3.2.11 manifest Blob 54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57 | Per-authority physical serialization anchor has distinct nominal types and must not merge BrainAuthorityRef, D fence/gate/barrier generations, I PermissionEpoch, C sequence, COC position or XID. B approves type boundary only; E/F accept with conditions; Storage manifest remains not jointly accepted/frozen and requires fresh A review. | B domain type semantics; Storage physical implementation; D/I/C/COC own their semantic counters; A integration | Keep anchor as IMPLEMENTATION_DETAIL; do not introduce global counter or domain entity. Require exact Storage ADR acceptance, same-GID recovery, HA/restore and L4 evidence before physical freeze. | OPEN |

| B-CONFLICT-015 | HIGH | A architecture invariant I-10 vs G Applied contract / C final-request evidence / H ACK boundary | Architecture invariants Blob 33b037318e459ebb73bea33b3186f31a41d5dcfe; G Applied Blob aa3afa73d8a76cc6f025839c52bfbff6a983046a; G full-path review Blob 1894860c76336f8739d354b72beed3992cffd17e; C review Blob 8fd6052cabf58a78962cc2e776398b2a40604bcd | I-10 says Context delivery is Applied only after explicit Adapter acknowledgement. G requires complete per-request predicate and exact final-request/provider evidence; H ACK alone is not Applied and does not prove execution/understanding. These can be reconciled if I-10 is a necessary but insufficient condition, but current wording may be misread as sufficient. | A owns global invariant wording; G Applied semantics; C final request proof; H protocol ACK | Clarify I-10 as necessary condition only; define Applied solely by G-owned complete predicate and evidence, never by ACK alone. A should update invariant wording in a separate approved change. | OPEN — clarification required |
| B-CONFLICT-016 | HIGH | A GOV-DOC-001 / I-23/I-24 vs current B research package | Bilingual policy Blob b51b054b9f1022133666542680df74dfe19de2fb; architecture invariants Blob 33b037318e459ebb73bea33b3186f31a41d5dcfe; current research files in this PR | The research package contains bilingual headings and some translated prose, but several detailed tables/normative sections are not full semantic peers. This violates the current same-change-set parity requirement for an architecture change. | A owns bilingual policy; B owns this research deliverable | Complete full Chinese/English semantic parity for every file and stable IDs before B5. No silent waiver. | OPEN — B5 BLOCKED |

## 1A. 中文冲突严重级别

- **BLOCKING（阻塞）：** 阻止受影响的跨 Owner 契约冻结、Schema 冻结或架构 Gate。
- **HIGH（高）：** 高影响语义歧义；受影响路径必须 Fail Closed 或延后。
- **MEDIUM（中）：** 在依赖实现开始前必须解决的建模歧义/复杂度。
- **LOW（低）：** 不立即破坏不变量的局部术语/文档不一致。
- **INFORMATIONAL（信息）：** 未发现矛盾，仅为追溯记录兼容差异或边界。

## 1B. Chinese active-conflict mirror / 中文未解决冲突对照

| Conflict ID / 冲突 ID | 严重级别 | 冲突含义与系统影响 | 决策权威 | 解除条件与当前状态 |
|---|---|---|---|---|
| B-CONFLICT-001 | BLOCKING | B Overview 将 Fact 描述为限定 Claim 并标记 DECIDED；架构不变量 I-04 要求 Fact 是独立领域概念；双语 Guide 将 Fact/Claim ADR 保持 BLOCKED。可以确认概念区分，但是否为独立对象/类型或限定 Claim 表示仍 OPEN；Claim 跨 MemoryVersion 身份也未决。 | B 通过明确 ADR 决定领域语义；A 登记精确版本；D/E 必须验收消费者影响。 | 保留 I-04 的概念区分和 ADR-BLOCKED；ADR 必须比较备选方案、证据、Schema 影响及 Owner 验收。阻塞 B2/B3 和下游 Schema 冻结。 |
| B-CONFLICT-002 | BLOCKING | G 单独提交 Applied；C 证明真实 Final Submit；H 负责 Wire；I 授权和 D Fence 是独立前提。历史 Applied 与当前使用资格不同。CGH-APPLIED-1.1 设计决策已记录例外，但 Frozen=NO；H 60 项 CI 与 G 38 项 Full-path Fixture 使用确定性 Authority Double，不能证明生产集成。 | G 决定 Applied 谓词/状态；C 提供 Submit 证据；H 负责 Wire；I 负责认证/授权；D 负责 Fence；A 仅登记集成契约。 | 必须完成 H Schema/Crypto Governance、C Provider Idempotency/真实 Provider Truth、G Applied 持久化、COC Quorum、Storage same-GID Recovery 和 L3/L4 端到端验证。因果顺序未知必须 Unknown/Suppress。 |
| B-CONFLICT-003 | BLOCKING | I COMMIT_WON 是授权顺序，不是 Storage Published。Published 必须有 Storage VisibilityPointer、PublicationReceipt 和精确读回。DE-S 仍是候选；JF-10 P0 和物理实现证明未完成。 | I 拥有 Policy Sequencer/Authorization；D Fence；Storage 物理事务/可见性；C Provider 边界；A 集成。 | I 精确接受 JF-10；指定数据库引擎/版本；完成 same-XID Recovery、COC Durable Log、故障注入和独立读回。阻塞 B3/B4/系统冻结。 |
| B-CONFLICT-004 | BLOCKING | D CanonicalSuppressionComplete 不等于 I Global Forget Complete；Storage/备份操作方拥有物理擦除。InventorySealReceipt 和外部治理批准尚无证据。 | D 规范抑制；I 全局策略/完成；Storage/备份物理擦除；外部接收方拥有其副本。 | 保持状态/证据范围分离；完成封闭目标清单、治理批准、目标证明和备份/恢复证据前，不得宣称物理 Purge 或 Global Completion。 |
| B-CONFLICT-005 | HIGH | PrincipalRef、ActorRef、ScopeRef、EnvironmentRef 不同；B 已正式批准类型映射；C/F/G 对 BIH 设计有例外地接受，H 接受精确包。但 Tenant/Workspace/Project/Agent/Session/Environment 层级和 Registry 权威仍不完整，I36 治理阻塞。 | B 定义类型；I 管 Scope 隔离/Trust/Policy；A 管 Registry；G 使用 Scope。 | 保留类型化引用，禁止隐式字符串转换/继承；I/A 决定精确分类、Issuer 和跨 Scope 映射。消费者接受仅对精确 Pin 有效，不证明运行时一致性。 |
| B-CONFLICT-006 | HIGH | 旧 Core Schema 有稳定 claim_id，而 MemoryVersion 嵌入 ClaimSnapshot；跨版本身份连续性未决定，Fact/Claim ADR 阻塞。 | B Domain ADR；D 版本；E 派生消费者；A Registry。 | Claim 身份/Schema 保持 OPEN；ClaimSnapshot 仅作为候选，不得强制下游身份。 |
| B-CONFLICT-007 | HIGH | Event/Observed/Recorded/Valid Time 不同；规范 Commit Cursor/Storage Transaction Time 又是操作时间轴。Record Time 与 Transaction Time 字段权威及模糊时间 Schema 未完全绑定。 | B 时间语义；D 规范 Cursor；Storage Commit Time；E 来源时间捕获。 | 保留独立时间轴；仅对 Claim/Relation 选择性支持双时态；不得强制所有实体使用双时态。 |
| B-CONFLICT-008 | HIGH | RuntimeSessionRef、Session ScopeRef、Conversation、Agent 身份和 Adapter/Runtime Instance 不同；Session/Conversation 规范关系和类型映射仍需 C/G/H 确认。 | B 类型语义；C/G Runtime/Context；H 认证 Session；I Principal 绑定。 | 保持名义类型分离；不得混用 Conversation ID、Session ID、Runtime Session 或 Scope ID；需要精确消费者验收。 |
| B-CONFLICT-009 | MEDIUM | Provenance 图循环、Derivation Edge 身份、谱系压缩和 Forget 后元数据保留仍 OPEN。 | B Provenance 语义；E Compiler；D 谱系/Fence；I 保留；Storage 持久化。 | 默认采用明确无环约束；只有具备非递归谱系证明和保留规则时才允许例外。 |
| B-CONFLICT-010 | MEDIUM | Memory Source 当前为独立来源关联，但 Source 本身是否应成为规范实体，尚未证明适用于所有来源类型。 | B 语义；E 来源摄取；D 规范来源权威。 | 默认将 MemorySource 作为类型化关联/值对象；只有证明独立生命周期/引用/访问需求时才提升为实体。 |
| B-CONFLICT-011 | MEDIUM | ContextVersion、F Working Set、E Frozen Compiler Input Bundle 不同；ContextEntry 身份、ChangeSet 和 Context Snapshot 的精确关系需 G 规范 Pin/消费者映射。 | G Context；F Runtime；E Compiler；B 共享词汇。 | 保留名义类型分离；禁止标量版本别名；协调 G 精确 Schema 和消费者验收。 |
| B-CONFLICT-012 | MEDIUM | 架构仓库尚无 Runtime 实现；未找到覆盖全部契约的共同可执行一致性证据。A 要求指定规范实现仓库和负责 Engineering Owner。 | 项目治理权威/指定 Engineering Authority；A 协调。 | 不得标记 Validation/Implementation/Production Ready；必须确定 Runtime Repo 和测试权威。 |
| B-CONFLICT-013 | BLOCKING | C Origin Signer/P0、H Wire 提取/验证、I Trust Profile/Issuer/Key 生命周期和 Storage Durable Authenticated Ingress/Replay 是独立边界。当前 H 1.2.14 只是 Reference Orchestration；C Signer Profile 候选；I Crypto Suite/Trust 注册未批准；H P0 验证和 Durable Replay 未实现。A 明确要求不得冻结。 | C 拥有 Origin Message/P0；H Wire；I Crypto Trust/Governance；Storage Durable Ingress；A 集成。 | 需要精确 C P0/签名 Profile、I 注册 Trust/Key Policy、H 可执行 Extractor/Verification/Channel Binding/Replay、Storage 持久接收/恢复、独立测试和 A 新审查。Gate A/B 阻塞。 |
| B-CONFLICT-014 | HIGH | Per-authority 物理 Serialization Anchor 必须与 BrainAuthorityRef、D Fence/Gate/Barrier、I PermissionEpoch、C Sequence、COC Position 和 XID 区分。B 仅批准类型边界；E/F 有条件接受；Storage Manifest 未联合接受/冻结。 | B 领域类型语义；Storage 物理实现；D/I/C/COC 拥有各自计数器；A 集成。 | Anchor 保持 IMPLEMENTATION_DETAIL；不得引入全局计数器或领域实体。物理冻结前需 Storage ADR 验收、same-GID Recovery、HA/Restore 和 L4 证据。 |
| B-CONFLICT-015 | HIGH | 架构不变量 I-10 表述 Context Delivery 在 Adapter ACK 后 Applied；G 要求完整逐请求谓词和精确 Final Request/Provider 证据。若把 I-10 误读为 ACK 充分条件，就会与 G 契约冲突。 | A 管全局不变量；G 管 Applied；C 管 Final Request 证明；H 管 Protocol ACK。 | A 应澄清 I-10：Adapter ACK 是必要但不充分条件；Applied 只能由 G 完整谓词和证据确定。当前 OPEN。 |
| B-CONFLICT-016 | HIGH | GOV-DOC-001/I-23/I-24 要求同一变更集完整双语语义对等；当前研究包仍有部分英文单语表格/规范段落。 | A 管双语政策；B 负责本研究交付。 | 所有文件完成双语对等、稳定 ID 对齐后才可通过 B5；不得静默豁免。当前 B5 BLOCKED。 |

## 2. Conflict resolution protocol / 冲突解决流程

1. Pin the exact conflicting artifact branch/path/Blob and, where available, commit SHA. / 精确 Pin 冲突工件的 Branch/Path/Blob，并在可获得时记录 Commit SHA。
2. Quote the exact semantic clauses and state why they are incompatible (not merely differently worded). / 引用精确语义条款，说明其为何不兼容，而非仅指出措辞不同。
3. Identify the sole authority for each clause; do not assign a cross-owner authority by convenience. / 为每条语义识别唯一权威，不得为方便而赋予跨 Owner 权限。
4. Mark affected contract/schema/gate and safe interim behavior (normally fail closed / defer). / 标记受影响的契约/Schema/Gate 及安全临时行为（通常为 Fail Closed/Deferred）。
5. Obtain explicit Owner-authored decision with exact version and exceptions. / 获取 Owner 明确编写的决定，并记录精确版本和例外。
6. Update only B-owned synthesis; never edit another Owner's normative file. / 只更新 B 拥有的综合文件；不得编辑其他 Owner 的规范文件。
7. Re-run bilingual parity and invariant validation; retain superseded evidence and record explicit supersession. / 重新执行双语对等和不变量验证；保留已被替代的证据并明确记录 Supersession。

## 3. Gate status / 门禁状态

No BLOCKING conflict is closed. B3 is NOT PASSED. The latest Phase 3.8 branch reviews add B-CONFLICT-013 (outer-envelope authenticated ingress) and B-CONFLICT-014 (physical serialization anchor acceptance/implementation boundary). This register is an evidence-backed issue ledger, not a claim of independent review, owner acceptance or project governance approval.

尚无 BLOCKING 冲突关闭。B3 未通过。本登记册是有证据支持的问题台账，不代表独立审查、Owner 验收或项目治理批准。


## 1C. Resolved at manifest-consistency level — Storage v3.3.1 → v3.3.2 / Manifest 一致性层面已解决 — Storage v3.3.1 → v3.3.2

| Field | Record |
|---|---|
| Conflict ID | **B-CONFLICT-017** |
| Original severity | **BLOCKING** |
| Original source A | Storage/D Option A topology ADR, Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`: Option A selected as normative v1 logical architecture; L4 physical engine/deployment OPEN. |
| Original source B | Storage v3.3.1 manifest, Blob `f6e61691ecdcfcbf1fb423cc45242868676ca925`: incorrectly called Option A a “conditional L1 candidate” and cited unpinned A-01–A-05 clarifications. |
| Corrected successor | Storage v3.3.2 manifest, Blob `5c614375e10698e4931d83deb57d20321445e068`: corrects Option A to selected normative v1 logical architecture, preserves L4 OPEN, removes unsupported A-01–A-05 reference and retains ADR §8.7 anchor obligation. |
| Exact A re-review | A Phase 3.12.2, Blob `eb3c946065aff4fbc6d76f384402fb9f75fa32dc`: **ACCEPT AS A CONSISTENT EXACT-VERSION CANDIDATE MANIFEST WITH ENUMERATED RELEASE BLOCKERS**; marks the prior inconsistency CLOSED at manifest-consistency level. |
| Authority | Storage owns its manifest; A owns integration review; B records cross-owner consistency only. Both successor artifacts identify delegated-role provenance, not independent human Owner signatures. |
| Closure scope | **CLOSED — MANIFEST CONSISTENCY REMEDIATED.** This closes only the Option A status wording and unsupported A-01–A-05 reference. |
| Remaining limitations | Storage v3.3.2 is NOT JOINTLY ACCEPTED / NOT FROZEN; A review is delegated and exact-version scoped; H 1.2.15 is not included (v3.3.2 binds H 1.2.14); L4 and all production gates remain open. |

**English finding.** The original conflict was substantive, not stylistic. Storage v3.3.2 corrects the mismatch, and A Phase 3.12.2 explicitly closes it at manifest-consistency level. The closure is accepted as exact-version source evidence, but not upgraded to independent human Owner approval, global acceptance or production authorization.

**中文发现。** 原冲突属于实质性状态矛盾，而非文风差异。Storage v3.3.2 已修正不一致，A Phase 3.12.2 明确在 Manifest 一致性层面将其关闭。该关闭作为精确版本来源证据记录，但不升级为独立人类 Owner 批准、全局验收或生产授权。

B-CONFLICT-013 remains separately OPEN for authenticated ingress, H 1.2.15 successor binding, I trust/profile/key registration, durable replay and production verification. B-CONFLICT-014 remains separately open for physical serialization-anchor acceptance/implementation boundaries and L4 evidence. B3 remains NOT PASSED.

B-CONFLICT-013 仍单独 OPEN，涵盖 Authenticated Ingress、H 1.2.15 后继绑定、I Trust/Profile/Key 注册、Durable Replay 和生产验证。B-CONFLICT-014 仍单独开放，涵盖物理 Serialization Anchor 验收/实现边界及 L4 证据。B3 仍 NOT PASSED。

## 3A. Updated gate / 更新后的门禁

B-CONFLICT-017 is **CLOSED at manifest-consistency level**. No claim is made that all blocking conflicts are closed. B3 remains NOT PASSED. This is a source-backed author-side status reconciliation based on Storage v3.3.2 and delegated A Phase 3.12.2 review, not independent human Owner acceptance or governance approval.

B-CONFLICT-017 已在 **Manifest 一致性层面 CLOSED**。不声称所有阻塞冲突均已关闭。B3 仍 NOT PASSED。本次是基于 Storage v3.3.2 和委派 A Phase 3.12.2 复审的有来源作者侧状态协调，不代表独立人类 Owner 验收或治理批准。


## 4. Current B Owner ADR and H ingress source correction / 当前 B Owner ADR 与 H 入口来源纠偏 — 2026-11-18

This section supersedes earlier recommendation wording where it conflicts with the live B Owner branch. It does not close any ADR or cross-owner blocker.

本节在与实时 B Owner 分支不一致时，取代此前的建议表述；不关闭任何 ADR 或跨 Owner 阻塞项。

### 4.1 B-CONFLICT-001 — Fact / Claim / B-CONFLICT-001 — Fact / Claim

- **Current B recommendation:** Option A — distinct Claim proposition thread and independently addressable Fact attestation object — is the preferred **CANDIDATE** in B's current Owner branch.
- **Exact B evidence:** summary ADR Blob `a1024938ff5baba069cf128c69496a44e143330c`; detailed canonical ADR Blob `df77e4a93cb8fef689ae7c828888d960cbf381d6`; consumer map Blob `dd45a37199c9b69ab6b68f65e051a484a04691d4`; branch `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2`.
- This supersedes the earlier C2/Option B recommendation in the B research ADR. Neither Option A nor B is approved. Both current B ADRs remain ADR-BLOCKED because no formal Architecture Governance authority/approver/timestamp/approval record is recorded.
- I-04/P-04 require distinction; main Domain Overview and terminology still conflict with that baseline; bilingual guides retain ADR-BLOCKED. Option B would require an explicit Governance amendment to I-04/P-04/terminology before it could become normative.
- **Status remains BLOCKING / OPEN.** B2 NOT PASSED; no schema freeze.

- **当前 B 建议：** Option A——独立 Claim 命题线程与可独立寻址 Fact Attestation 对象——是 B 当前 Owner 分支优先推荐的 **CANDIDATE**。
- **B 精确证据：** 摘要 ADR Blob `a1024938ff5baba069cf128c69496a44e143330c`；详细规范 ADR Blob `df77e4a93cb8fef689ae7c828888d960cbf381d6`；消费者映射 Blob `dd45a37199c9b69ab6b68f65e051a484a04691d4`；分支 `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2`。
- 这取代 B 研究 ADR 此前倾向 C2/Option B 的建议。Option A 或 B 均未获批准。当前两份 B ADR 仍 ADR-BLOCKED，因为没有记录正式 Architecture Governance 权威/批准人/时间戳/批准记录。
- I-04/P-04 要求概念区分；Main Domain Overview 和术语仍与该基线冲突；中英文指南保留 ADR-BLOCKED。Option B 若要成为规范方案，必须先由 Governance 明确修订 I-04/P-04/术语。
- **状态仍为 BLOCKING / OPEN。** B2 未通过；不得冻结 Schema。

### 4.2 B-CONFLICT-006 — Claim identity / B-CONFLICT-006 — Claim 身份

B's current detailed ADR proposes stable ClaimRef + immutable ClaimRevisionRef and exact-revision-targeted Evidence/Provenance; ConflictSet groups incompatible exact ClaimRevisionRefs. These remain CANDIDATE. D owns canonical ID allocation, persistence, revision commit and ConflictSet lifecycle/commit shape after approval. E's CandidateProposition/ExtractionIR remains neutral. No ClaimRef, ClaimRevisionRef, FactRevision or ConflictSet schema is frozen.

B 当前详细 ADR 提出稳定 ClaimRef + 不可变 ClaimRevisionRef、针对精确 Revision 的 Evidence/Provenance，以及按不兼容精确 ClaimRevisionRef 分组的 ConflictSet。这些仍为 CANDIDATE。批准后 D 负责规范 ID 分配、持久化、Revision Commit 和 ConflictSet 生命周期/Commit 形态。E 的 CandidateProposition/ExtractionIR 保持中立。ClaimRef、ClaimRevisionRef、FactRevision 或 ConflictSet Schema 均未冻结。

### 4.3 B-CONFLICT-013 — H 1.2.15 authenticated ingress / B-CONFLICT-013 — H 1.2.15 认证入口

A Phase 8 B-02 reconciliation Blob `8a0a428ebf9cd8c8fe00562d2267ff490d5c3205` and A H 1.2.15 exact review Blob `582ed576f73d9096dcc77b3a559df8c3b997b895` refine the earlier status:
- C and I have accepted corrected 1.2.15 schema/P0/order reference contracts **WITH CONDITIONS**; this is not production trust registration or exact current-validator/issuer acceptance.
- H has a local receiver validator and tests; A found no separate executable issuer pre-sign pipeline.
- H exact-head CI reported 91 Provider Outcome tests and 288 Recovery Cutoff tests (22 skipped), but deterministic callbacks do not prove production crypto, I registration, durable replay or end-to-end integration.
- D's exact 1.2.15 currentness/Forget/lineage review, I production trust registration, H issuer execution, Storage successor bundle and fresh A review remain OPEN.
- Storage v3.3.2 remains H 1.2.14 / C 1.0.1 historical bundle.

A Phase 8 B-02 协调 Blob `8a0a428ebf9cd8c8fe00562d2267ff490d5c3205` 和 A H 1.2.15 精确复审 Blob `582ed576f73d9096dcc77b3a559df8c3b997b895` 细化了此前状态：
- C 和 I 已对修正后的 1.2.15 Schema/P0/顺序 Reference 契约作出 **WITH CONDITIONS** 验收；这不是生产 Trust 注册，也不是对当前 Validator/Issuer 的精确验收。
- H 已有本地 Receiver Validator 和测试；A 未发现独立可执行 Issuer Pre-sign Pipeline。
- H 精确 Head CI 报告 91 项 Provider Outcome 测试和 288 项 Recovery Cutoff 测试（22 项跳过），但确定性 Callback 不能证明生产 Crypto、I 注册、Durable Replay 或端到端集成。
- D 对 1.2.15 的 Currentness/Forget/Lineage 精确复审、I 生产 Trust 注册、H Issuer 执行、Storage 后继 Bundle 和 A 新复审仍 OPEN。
- Storage v3.3.2 仍是 H 1.2.14 / C 1.0.1 历史 Bundle。

B-CONFLICT-013 remains **BLOCKING / OPEN**. Do not confuse A's workstream label “B-02” (H gateway ingress) with B's B2 semantic gate.

B-CONFLICT-013 仍 **BLOCKING / OPEN**。不得将 A 工作流标签 “B-02”（H Gateway Ingress）与 B 的 B2 语义 Gate 混淆。

### 4.4 Overall gate / 总体门禁

B-CONFLICT-017 remains closed only at manifest-consistency level. B2 remains IN PROGRESS / NOT PASSED; B3 remains NOT PASSED; B4 NOT READY; B5 BLOCKED / NOT PASSED; B6 INDEPENDENT_REVIEW_PENDING. No independent Owner acceptance, governance approval, production ingress, Applied freeze, Forget completion or L4 implementation is claimed.

B-CONFLICT-017 仍仅在 Manifest 一致性层面关闭。B2 仍 IN PROGRESS / NOT PASSED；B3 仍 NOT PASSED；B4 NOT READY；B5 BLOCKED / NOT PASSED；B6 INDEPENDENT_REVIEW_PENDING。不宣称独立 Owner 验收、治理批准、生产 Ingress、Applied 冻结、Forget 完成或 L4 实现。


### 4.5 B-CONFLICT-006 — D/E/F/G exact consumer status / B-CONFLICT-006 — D/E/F/G 精确消费者状态

The live Owner sources confirm alignment with the blocked boundary, not downstream acceptance:
- D Canonical Store Blob `6b37c91033fda21f072e2a3bde6f274663b1e76e` explicitly keeps Fact/Claim persistence ADR-BLOCKED and allows only neutral PropositionRef until INT-P0-01 approval. D Memory Versioning Blob `af747f339d03bdd4684b6ed60fca05957dc8e1fb` calls stable Claim ID + immutable ClaimRevision **D Option A**, a candidate under INT-P1-02.
- E Extraction Blob `c18780403de2d1dbcf471bdb8abdaa009a4a78e1` says CandidateProposition/ExtractionIR is pre-canonical and E excludes canonical Fact/Claim identity. E Evidence/Provenance Blob `38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963` keeps final Evidence/Provenance contracts dependent on D/B/I.
- F Retrieval Blob `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` assigns Claim identity/status to D, prohibits F from resolving disputed claims and leaves Claim revision identity OPEN.
- G Context Versioning Blob `05c0739d0c22576a1fd5affc7d73c078c89049b1` pins exact MemoryVersion in ContextEntry; ContextVersion/ChangeSet are G-owned and do not mint Claim/Fact identity.

实时 Owner 来源确认的是与阻塞边界一致，而不是下游验收：
- D Canonical Store Blob `6b37c91033fda21f072e2a3bde6f274663b1e76e` 明确保留 Fact/Claim 持久化 ADR-BLOCKED，INT-P0-01 批准前只允许中立 PropositionRef。D Memory Versioning Blob `af747f339d03bdd4684b6ed60fca05957dc8e1fb` 将稳定 Claim ID + 不可变 ClaimRevision 称为 **D Option A**，属于 INT-P1-02 下的候选。
- E Extraction Blob `c18780403de2d1dbcf471bdb8abdaa009a4a78e1` 明确 CandidateProposition/ExtractionIR 属于规范化前表示，E 不负责规范 Fact/Claim 身份。E Evidence/Provenance Blob `38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963` 将最终 Evidence/Provenance 契约保留为依赖 D/B/I 的事项。
- F Retrieval Blob `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` 将 Claim 身份/状态权威分配给 D，禁止 F 裁决争议 Claim，并将 Claim Revision 身份保留为 OPEN。
- G Context Versioning Blob `05c0739d0c22576a1fd5affc7d73c078c89049b1` 在 ContextEntry 中固定精确 MemoryVersion；ContextVersion/ChangeSet 由 G 拥有，不创建 Claim/Fact 身份。

**Option-label warning / 方案编号警告:** D's “Option A” (stable Claim ID + immutable ClaimRevision) is a different decision from B's “Option A” (separate Fact attestation object + Claim proposition thread). Do not treat D's candidate as approval of B's Fact/Claim recommendation. Both remain CANDIDATE and schema freeze remains blocked.

**方案编号警告：** D 的 “Option A”（稳定 Claim ID + 不可变 ClaimRevision）与 B 的 “Option A”（独立 Fact Attestation 对象 + Claim 命题线程）是两个不同决策。不得将 D 的候选视为对 B Fact/Claim 建议的批准。两者均仍为 CANDIDATE，Schema 冻结仍受阻。

B-CONFLICT-006 remains **HIGH / OPEN**. D's candidate is not an accepted revision identity contract; B's Fact/Claim ADR is still blocked; E/F/G provide no substitute approval. No ClaimRef, ClaimRevisionRef, FactRevisionRef or ConflictSet schema may be frozen.

B-CONFLICT-006 仍为 **HIGH / OPEN**。D 的候选不是已验收的 Revision 身份契约；B 的 Fact/Claim ADR 仍阻塞；E/F/G 不提供替代批准。不得冻结 ClaimRef、ClaimRevisionRef、FactRevisionRef 或 ConflictSet Schema。
