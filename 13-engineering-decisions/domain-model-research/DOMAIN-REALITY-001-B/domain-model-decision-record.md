# Domain Model Decision Record
# 领域模型决策记录

- ID: B-ADR-001
- Status: DECISION REGISTER — candidate recommendations; no unresolved ADR is marked closed
- Baseline: main @ b372b62c640a2b656e54b6db62a4ee67d7d8c001

## B-DEC-001 — Keep Domain Identity Separate from Content
- Context: Memory content, labels, embeddings and source text can change or duplicate.
- Problem: Content-derived IDs cause identity drift and accidental merging.
- Alternatives: content hash as identity; mutable database primary key; opaque stable domain ID plus separate content digest.
- Evidence: core entities Blob 8cb5a674eec8eac1f3c4d83c400dc08d00166f23; Microsoft DDD domain model guidance.
- Decision: recommend opaque stable domain identity, independent of content/version; ID algorithm is not selected.
- Consequences: stable references and immutable version lineage; requires registry/non-reuse discipline.
- Complexity: moderate; avoids content dedup conflating identities.
- Affected owners: B/D/E/Storage/I.
- Reversal conditions: only if a domain-specific entity is proven to be value-only and does not need independent identity.
- Status: DECIDED semantic principle in current source; implementation ID algorithm CANDIDATE.

## B-DEC-002 — Distinguish Typed Reference from Authentication and Permission
- Context: multiple modules pass Principal/Actor/Agent/Scope/Environment identifiers.
- Problem: payload references can be mistaken for verified identity or access rights.
- Alternatives: untyped IDs; universal Actor ID; typed namespaced references resolved through owner registries.
- Evidence: B Phase 3.6 typed identity Blob 0a6b78a842e550b58533b797cdfcd2d954ed6826; I identity trust Blob 0cbf6bb7480db873790c454817593a9b1c5548ba; H protected operation Blob e7ca5ce4ece5d8fd77fe0760e49a85afa0133248.
- Decision: preserve typed distinct references; a Ref is not proof of authentication, registration or permission.
- Consequences: explicit mappings and per-boundary validation; safer tenant/scope isolation.
- Complexity: adds type/namespace validation but prevents high-impact identity confusion.
- Affected owners: B/I/H/C/D/E/F/G.
- Reversal conditions: documented proof that two types have identical identity namespace, lifecycle, trust and authority semantics.
- Status: CANDIDATE B canonical adoption; existing delegated technical baseline is evidence, not new owner acceptance.

## B-DEC-003 — Separate Claim Epistemic Status from Memory Lifecycle
- Context: Memory lifecycle and Claim epistemic standing answer different questions.
- Problem: Active could be misread as Verified; Archived could be misread as false.
- Alternatives: one combined status enum; independent typed state dimensions.
- Evidence: lifecycle Blob 81c48c928cb5f9c76ca29d493fbd9479079e62f7; epistemic/temporal Blob 8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7.
- Decision: keep independent dimensions.
- Consequences: more than one state vocabulary but preserves meaning.
- Complexity: low/moderate; prevents invalid transitions and query filters.
- Affected owners: B/D/E/F/G.
- Reversal conditions: none unless the underlying domain meaning is disproven.
- Status: DECIDED in source.

## B-DEC-004 — Preserve Fact/Claim ADR Block
- Context: main overview uses DECIDED wording, while bilingual guide explicitly marks Fact/Claim ADR-BLOCKED and prohibits schema freeze.
- Problem: downstream consumers could freeze incompatible Claim/Fact schemas.
- Alternatives: adopt overview; adopt guide blocker; silently treat Fact as Claim subtype.
- Evidence: overview Blob 4d1debc0ec19b3917f9e76d04bb66da4df4cd346; guide Blobs a9f53a453aec25c47c58c4aea75adc43c83028d3 and 8a19cebacf5aefb0aded5fdbfeaff406291a5cf1; A PR #53.
- Decision: preserve ADR-BLOCKED; do not use old overview wording to freeze dependent schema. Supplemental decision request B-ADR-FACT-CLAIM-001 (fact-claim-identity-adr.md, Blob 96a2ee7d595fcd4a214201a7c7b6b2a9c3deb961) recommends C2 (Fact as qualified Claim concept) + I1 (stable Claim lineage with immutable version-local snapshots), but explicitly remains CANDIDATE / NOT DECIDED / NOT ACCEPTED / NOT SCHEMA-FROZEN.
- Consequences: Claim/Fact identity and version representation remain open.
- Complexity: delays schema but avoids false certainty.
- Affected owners: B/D/E/A.
- Reversal conditions: explicit B ADR with decision authority, alternatives, evidence, migration impact and consumer acceptance.
- Status: BLOCKING / OPEN.

## B-DEC-005 — Keep Source, Evidence and Provenance Distinct
- Context: system must explain origin, support and derivation.
- Problem: one generic “source” field cannot answer all three.
- Alternatives: one Source object; separate SourceRef, Evidence object and Provenance trace.
- Evidence: core entities Blob 8cb5a674eec8eac1f3c4d83c400dc08d00166f23; relationships/provenance Blob e762f84c59f69de7a44baad2123aed46e1ffea16; W3C PROV-O.
- Decision: keep semantic distinctions; whether every Source/Provenance edge is a first-class entity remains open.
- Consequences: traceability and access control clearer; lineage metadata cost.
- Complexity: moderate; only promote independent identities when needed.
- Affected owners: B/E/D/I/Storage.
- Reversal conditions: only if an entity/link can be proven semantically redundant.
- Status: DECIDED distinctions; identity granularity OPEN.

## B-DEC-006 — Preserve Distinct Temporal Axes and Selective Bitemporal Capability
- Context: events, observations, claims and system records occur at different times.
- Problem: one timestamp loses historical truth and historical knowledge.
- Alternatives: single timestamp; valid time only; record time only; universal bitemporal model; selective bitemporal Claims/Relations/revisions.
- Evidence: epistemic/temporal Blob 8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7; PostgreSQL MVCC/transaction isolation docs; RDF 1.1 atemporal graph note.
- Decision: preserve Event/Observed/Recorded/Valid/Transaction time distinctions; recommend selective bitemporal capability, not universal bitemporal fields.
- Consequences: supports valid-at T and known-by T2 queries; requires temporal indexing/query discipline.
- Complexity: medium/high for selected entities; avoids system-wide temporal schema.
- Affected owners: B/D/E/F/G/Storage/I.
- Reversal conditions: evidence that no supported use case needs historical-as-known semantics.
- Status: CANDIDATE recommendation; exact schema/authority OPEN.

## B-DEC-007 — Do Not Make Event Sourcing Universal
- Context: immutable versions, audit and recovery are required, but external side effects and Forget create replay complexity.
- Problem: full event sourcing everywhere adds unnecessary replay, migration and retention cost.
- Alternatives: universal Event Sourcing; pure mutable state; state + immutable versions + targeted operation ledgers/events.
- Evidence: Martin Fowler Event Sourcing; Temporal Event History; existing D/E/Storage owner contracts.
- Decision: recommend state-based canonical Memory with immutable versions and append-only lifecycle/audit; use durable operation ledgers where ordering/recovery requires.
- Consequences: simpler queries and migration; targeted workflows still need explicit recovery logic.
- Complexity: lower than universal event sourcing; preserves required audit.
- Affected owners: D/E/F/G/I/Storage.
- Reversal conditions: measured requirements for deterministic replay/rebuild that justify full event sourcing in a bounded context.
- Status: RECOMMENDED.

## B-DEC-008 — Graph Projection Before Formal Ontology
- Context: typed Relations and entity-centric retrieval may benefit from graph traversal.
- Problem: adopting RDF/OWL or graph DB too early creates ontology governance and dual-store consistency costs.
- Alternatives: relational typed relations; property graph as canonical; RDF/OWL ontology; relational canonical + graph projection.
- Evidence: W3C RDF 1.1, OWL 2, PROV-O; Zep/Graphiti; Mem0 official docs.
- Decision: recommend relational canonical representation with explicit typed Relation and provenance; graph projection only for demonstrated query value; RDF/OWL deferred.
- Consequences: keeps canonical semantics auditable without graph stack commitment.
- Complexity: lower; graph projection adds rebuild/consistency cost if later needed.
- Affected owners: B/E/F/Storage.
- Reversal conditions: concrete interoperability/reasoning requirement and measured query benefit.
- Status: RECOMMENDED; no technology selected.

## B-DEC-009 — Separate Applied, Recorded, Committed, Visible and Published
- Context: multiple owners produce evidence at different boundaries.
- Problem: one generic success state permits unsafe promotion from ACK/authorization to publication/application.
- Alternatives: generic Completed; staged owner-issued evidence states.
- Evidence: G Applied Blob aa3afa73d8a76cc6f025839c52bfbff6a983046a; C Final Request Blob fd2f47ba6c89bb270e9f2bec956873cb7ae3592b; H capability Blob 74be8374a67da385a5f0f8e34c7aef2b38b72bcf; Storage JF-10 Blob 94679897e84a6f58fd8b9467b5249e1a885cb0b0; Issue #3/#10.
- Decision: retain separate typed meanings and issuer authorities; no universal total order.
- Consequences: exact proof vectors and cross-owner causal protocol required.
- Complexity: high, but safety-critical.
- Affected owners: A/C/G/H/I/D/Storage.
- Reversal conditions: none unless proof scopes are formally shown identical (current evidence says otherwise).
- Status: semantic distinctions DECIDED; exact Applied/JF-10 contract BLOCKED.

## B-DEC-010 — Forget, Forgotten, Deleted and Purged Are Distinct
- Context: Memory lifecycle, governance operation, logical suppression and physical storage cleanup are different scopes.
- Problem: false global completion or physical erasure claim.
- Alternatives: one Deleted/Forgotten status; separate D operation, Memory lifecycle, I global policy and Storage physical target evidence.
- Evidence: D Forget Blob 1f0391bc49d007c44ec74165bd33d37412cc7990; I Global Forget Blob 9100061fa986fb6676656169de3fcf9fc1c72664; Storage JF-10 Blob 94679897e84a6f58fd8b9467b5249e1a885cb0b0.
- Decision: keep separate; D CanonicalSuppressionComplete is not I GlobalForgetComplete or physical purge.
- Consequences: multiple target-scoped receipts and inventory completeness required.
- Complexity: high, safety-required.
- Affected owners: D/I/E/F/G/H/Storage/A.
- Reversal conditions: none while ownership and proof scopes remain different.
- Status: DECIDED semantic split; global completion and physical proof OPEN.

## B-DEC-011 — Keep Physical Serialization Anchor Types Separate from Domain Identity
- Context: Storage Option A proposes a per-authority serialization anchor; B reviewed exact Storage ADR Blob bb544ba2f346bdc130d524bd5c7310d86f367988.
- Problem: physical serialization revisions could be mistaken for domain identity, ForgetFence, PermissionEpoch or a global order.
- Alternatives: universal counter; reuse D/I/C/COC epochs; separate per-authority physical anchor and nominal refs.
- Evidence: B review Blob e2bc4c8dde9706bfbe443269b702f1b5aa6965f6; E review Blob 19d708bc29b6115d7bccb7d320781f452ee28b78; F review Blob 122238146830db6188f00a9788e018a82bfb3f90; Storage v3.2.11 manifest Blob 54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57.
- Decision: approve nominal type separation as an L1/L2 semantic boundary; classify anchor as IMPLEMENTATION_DETAIL, not canonical domain entity or global counter.
- Consequences: preserves authority-local order; Storage still must prove physical DB, same-GID recovery, HA/restore and read-path correctness.
- Complexity: additional types but prevents invalid cross-authority comparison and ownership leakage.
- Affected owners: B/C/D/E/F/I/Storage/COC/A.
- Reversal conditions: none unless authority boundaries and causal semantics are formally changed by all affected owners.
- Status: B delegated technical approval with enumerated clarifications; Storage v3.2.11 not jointly accepted/frozen; fresh A review and L4 evidence required.

## B-DEC-012 — Keep Origin Signature, Transport Authentication and Authorization Separate
- Context: H 1.2.14 adds a reference authenticated-ingress gate; C defines provider outcome and outer envelope P0; I owns trust/profile/key governance.
- Problem: a payload sender claim, transport authentication, C origin signature and authorization could be conflated.
- Alternatives: reuse C object P0 for envelope; treat H transport sender as C origin signer; separate C origin signature/P0, H protected transport context, I trust registry and Storage durable ingress.
- Evidence: C review Blob 8fd6052cabf58a78962cc2e776398b2a40604bcd; H correction Blob 4ba7e1699215d02224f805a15484b1da2e40c03f; I review Blob b6d1ea45825a1c2090abfba42474814f02f073a3; Storage manifest Blob 54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57; A blocking review Blob e12cd7b5c79e2234178014243fd51f2e7d51272e.
- Decision: B preserves typed identity distinctions; C owns origin-signed message semantics/P0; H owns wire parsing and verification orchestration; I owns trust profile/issuer/key policy; Storage owns durable authenticated ingress/replay. No layer substitutes for another.
- Consequences: secure separation, but production ingress cannot be frozen until C/H/I/Storage contracts and tests close.
- Complexity: high, security-critical; requires exact P0, trust profile, protected context, channel binding, replay persistence and independent tests.
- Affected owners: B/C/H/I/Storage/A.
- Reversal conditions: only an explicit jointly approved profile proving equivalent signer, trust, transport and authorization semantics.
- Status: semantic boundary CANDIDATE/RECOMMENDED; production crypto/trust/ingress BLOCKED; A says do not freeze.

## 2A. Chinese decision record mirror / 中文决策记录对照

| Decision ID / 决策 ID | Context and problem / 背景与问题 | Alternatives / 备选方案 | Decision and consequences / 决定与后果 | Status / 状态 |
|---|---|---|---|---|
| B-DEC-001 | Memory 内容、标签、Embedding 和来源文本可能变化/重复；内容 Hash 会造成身份漂移或误合并。 | 内容 Hash 身份；可变数据库主键；不透明稳定领域 ID + 独立内容摘要。 | 推荐领域身份独立于内容/版本；ID 算法尚未选择。稳定引用和版本谱系需要 Registry 及禁止复用规则。 | 语义原则 DECIDED；实现 ID 算法 CANDIDATE。 |
| B-DEC-002 | 多模块传递 Principal/Actor/Agent/Scope/Environment ID，载荷引用可能被误认为认证身份或访问权。 | 无类型 ID；统一 Actor ID；由 Owner Registry 解析的类型化命名空间引用。 | 保留不同类型引用；Ref 不证明认证、注册或权限。需要显式映射和逐边界验证，提升 Tenant/Scope 隔离。 | B 规范采纳 CANDIDATE；既有委托技术基线仅作证据，不推断新的 Owner 批准。 |
| B-DEC-003 | Memory 生命周期与 Claim 认知地位回答不同问题。 | 一个合并状态 Enum；独立类型化状态维度。 | 保持两套独立维度，避免 Active 被误读为 Verified、Archived 被误读为 False。 | 源规范 DECIDED。 |
| B-DEC-004 | Overview 的 DECIDED 与双语 Guide 的 ADR-BLOCKED 不一致；下游可能冻结不兼容的 Fact/Claim Schema。 | 采用 Overview；采用 Guide 阻塞；静默把 Fact 当作 Claim 子类型。 | 保留 ADR-BLOCKED。补充 ADR 请求 B-ADR-FACT-CLAIM-001 提议 C2+I1，但仅为候选，不是决定/接受/Schema 冻结。 | BLOCKING / OPEN。 |
| B-DEC-005 | 系统必须解释信息来源、证据支持和派生过程；单一 Source 字段无法回答三者。 | 单一 Source 对象；分离 SourceRef、Evidence 对象和 Provenance Trace。 | 保持语义区分；Source/Provenance Edge 是否每条都独立成实体仍 OPEN。 | 区分 DECIDED；身份粒度 OPEN。 |
| B-DEC-006 | Event、Observation、Claim 和系统记录发生于不同时间；单一 Timestamp 会丢失历史真值和历史知识。 | 单一时间；仅 Valid Time；仅 Record Time；全局双时态；选择性双时态。 | 保留 Event/Observed/Recorded/Valid/Transaction 时间差异；推荐仅对时间敏感 Claim/Relation/Revision 使用双时态。 | 推荐 CANDIDATE；Schema/权威 OPEN。 |
| B-DEC-007 | 不可变版本、审计和恢复是必要的，但外部副作用与 Forget 会增加 Replay 复杂度。 | 全系统 Event Sourcing；纯可变状态；状态 + 不可变版本 + 目标操作账本。 | 推荐规范 Memory 使用状态 + 不可变版本 + 追加式生命周期/审计记录；只在需要顺序/恢复时使用持久操作账本。 | RECOMMENDED。 |
| B-DEC-008 | 类型化 Relation 和实体检索可能受益于图遍历；过早采用 RDF/OWL 或 Graph DB 会增加治理和双存储一致性成本。 | 关系型类型化 Relation；Property Graph 作为规范存储；RDF/OWL；关系型规范模型 + 图投影。 | 推荐关系型规范表示 + 显式类型化 Relation/Provenance；只有查询价值得到证明才使用图投影；RDF/OWL 延后。 | RECOMMENDED；未选技术。 |
| B-DEC-009 | 多 Owner 在不同边界产生证据；通用 Completed 会导致 ACK/授权被错误提升为 Published/Applied。 | 通用 Completed；按 Owner 签发的分阶段证据状态。 | 保留 Recorded/Applied/Committed/Visible/Published 各自语义和签发权威；不建立通用全序。 | 语义区分 DECIDED；精确 Applied/JF-10 契约 BLOCKED。 |
| B-DEC-010 | Memory 生命周期、治理操作、逻辑抑制和物理清理范围不同。 | 单一 Deleted/Forgotten 状态；D 操作、Memory 生命周期、I 全局策略、Storage 物理目标证明分离。 | D CanonicalSuppressionComplete 不等于 I GlobalForgetComplete 或物理 Purge；需要目标级 Receipt 和清单完整性。 | 语义分离 DECIDED；全局完成/物理证明 OPEN。 |
| B-DEC-011 | Storage Option A 的 Per-authority Anchor 可能被误认为领域身份、ForgetFence、PermissionEpoch 或全局顺序。 | 通用计数器；复用 D/I/C/COC Epoch；独立物理 Anchor 和名义引用。 | B 仅批准 L1/L2 名义类型边界；Anchor 属于 IMPLEMENTATION_DETAIL，不是规范领域实体/全局计数器。Storage 仍须证明物理 DB、same-GID、HA/Restore 和读路径。 | B 委托技术批准带例外；Storage v3.2.11 未联合接受/冻结；需 A 新审查和 L4 证据。 |
| B-DEC-012 | 载荷 Sender Claim、传输认证、C Origin Signature 和 Authorization 可能被混为一谈。 | 复用 C Object P0；把 H Transport Sender 当作 C Signer；分离 C Origin P0、H Protected Context、I Trust Registry 和 Storage Durable Ingress。 | B 保留类型化身份区分；C 拥有 Origin-signed Message/P0；H 负责 Wire 解析/验证编排；I 负责 Trust/Profile/Issuer/Key Policy；Storage 负责认证后持久 Ingress/Replay。各层不可互相替代。 | 语义边界 CANDIDATE/RECOMMENDED；生产 Crypto/Trust/Ingress BLOCKED；A 要求不得冻结。 |

## 3A. 中文被拒绝方案

- **通用 Status Enum：** 丢失对象/Owner 专属权威和状态转换语义。
- **全系统 Event Sourcing：** 所有 Bounded Context 都没有被证明需要；增加 Replay、Forget 和外部副作用成本。
- **Content Hash 作为身份：** 相同内容可能代表不同对象，身份还必须在内容变化后保持稳定。
- **通用 Actor/User ID：** 混淆安全身份、操作归因和逻辑 Agent 身份。
- **默认完整 RDF/OWL Ontology：** 当前没有正式推理/互操作需求证据。
- **Graph DB 作为规范真值：** 在用例未证明前增加双写、一致性和 Forget 复杂度。
- **所有对象使用双时态字段：** 对非时间身份和 Runtime 状态过度建模。
- **在 Fact/Claim 和跨 Owner 验收前冻结 Schema：** 与未决 ADR 和 Owner 权威冲突。

## 4A. 中文未决决策

- Fact/Claim 及 Claim 跨版本身份。
- Tenant/Workspace/Project/Scope/Environment 分类和 Registry 权威。
- 精确 ContextVersion/ChangeSet/Entry Schema 和跨 Owner 验收。
- Applied 谓词及 CGH-APPLIED-1.1 精确版本验收。
- JF-10 same-XID/COC/Storage 物理能力和故障注入。
- Provenance 图循环策略和 Source/Provenance 记录身份。
- 模糊时间编码及 Record Time 与 Transaction Time 映射。
- Runtime 实现仓库和负责 Engineering Owner（Issue #7）。

## 3. Rejected alternatives / 被拒绝方案

- Universal status enum — loses subject-specific authority and state transitions.
- Universal Event Sourcing — no demonstrated benefit across all bounded contexts; replay/Forget/external side-effect cost.
- Content hash as identity — same content can represent different objects and identity must survive content change.
- Universal Actor/User ID — collapses security identity, operation attribution and logical Agent identity.
- Full RDF/OWL ontology by default — no demonstrated requirement for formal reasoning/interoperability yet.
- Graph database as canonical source of truth — adds dual-write, consistency and Forget complexity before use-case proof.
- Bitemporal fields on every object — over-models non-temporal identities and runtime state.
- Schema freeze before Fact/Claim and cross-owner acceptance — explicitly conflicts with open ADRs and owner authority.

## 4. Open decisions / 未决决策

- Fact/Claim and Claim identity across versions.
- Tenant/Workspace/Project/Scope/Environment taxonomy and registry authority.
- Exact ContextVersion/ChangeSet/Entry schema and cross-owner acceptance.
- Applied predicate and CGH-APPLIED-1.1 exact-version approvals.
- JF-10 same-XID/COC/Storage physical capability and fault injection.
- Provenance graph cycle policy and Source/Provenance record identity.
- Fuzzy-time encoding and Record vs Transaction Time mapping.
- Runtime implementation repository and accountable engineering owner (Issue #7).

## 5. Gate status / 门禁状态

This register does not close any blocking ADR, owner acceptance or implementation gate. All recommendations remain subject to exact-version owner review and independent review.

本登记册不关闭任何阻塞 ADR、Owner 验收或实现门禁。所有建议仍需精确版本 Owner 审查和独立审查。
