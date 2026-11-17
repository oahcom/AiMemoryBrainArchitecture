# Canonical Identity Semantics
# 规范身份语义

- ID: B-ID-001
- Status: CANDIDATE DOMAIN SEMANTICS; cross-owner binding OPEN
- Baseline: main `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Related B technical baseline: `session-b-domain-model-phase3:02-domain-model/phase-3.6-typed-identity-trust-closure.md`, Blob `0a6b78a842e550b58533b797cdfcd2d954ed6826`
- Current B formal type confirmation: `02-domain-model/phase-3.6-b-owner-formal-actor-scope-environment-type-mapping-confirmation.md`, Blob `3a1e77889cd9a90cd5822d9f0cb3437880868706` (supersedes earlier readback Blob 729a706860b1259115816265e847a29683c3c233)
- B exact CGH-APPLIED-1.1 recovery-batch type confirmation: included in current B formal artifact Blob `3a1e77889cd9a90cd5822d9f0cb3437880868706`; exact A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`; companion COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`
- Related I artifact: `session-i-security-governance-2026-11-16:09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md`, Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`
- Related H artifact: `session-h-bmcp-protocol:08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, current readback Blob `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`

## 1. Purpose and authority / 目的与权威边界

Identity semantics must distinguish a domain object's identity, a typed reference, a security Principal, a caller's identity claim, authenticated transport context, and authorization. A serialized identifier is never proof of the presenter, registration, or permission.

身份语义必须区分领域对象身份、类型化引用、安全 Principal、调用方身份声明、认证传输上下文和授权。序列化标识符永远不能证明呈现者身份、注册状态或权限。

B owns domain reference types and identity invariants. I owns issuer trust, Principal registration/resolution, delegation, authorization, revocation and PermissionEpoch. H owns authenticated transport and wire binding. C/D/E/G own operation-specific producer/consumer boundaries. These are non-substitutable authorities.

B 负责领域引用类型和身份不变量。I 负责 Issuer 信任、Principal 注册/解析、委托、授权、撤销和 PermissionEpoch。H 负责认证传输和 Wire 绑定。C/D/E/G 负责各自操作边界。上述权威不可互相替代。

## 2. Canonical distinctions / 规范区分

| Term / 术语 | Canonical meaning / 规范含义 | Must not be confused with / 不得混淆 |
|---|---|---|
| Domain Identity / 领域身份 | Stable identity of a domain object within its declared identity namespace. / 领域对象在声明的身份命名空间内保持稳定的身份。 | Content digest, display label, external identifier. / 内容摘要、显示标签、外部标识符。 |
| Typed Reference / 类型化引用 | Typed, namespaced pointer to a registered identity/object. / 指向已注册身份/对象的类型化、带命名空间引用。 | Authentication credential, grant, permission. / 认证凭证、授权授予或权限。 |
| Identity Claim / 身份声明 | Untrusted caller/payload assertion about an identity. / 调用方或载荷对某个身份提出的未受信声明。 | Authenticated identity. / 已认证身份。 |
| Authentication Credential / 身份认证凭证 | Protected proof material validated by a verifier under I policy. / 在 I 策略下由验证器校验的受保护证明材料。 | Domain Ref or ActorRef. / 领域引用或 ActorRef。 |
| Authenticated Principal / 已认证 Principal | I-resolved security subject after trust/credential/issuer/audience/revocation checks. / 通过信任、凭证、Issuer、Audience 和撤销检查后由 I 解析的安全主体。 | Domain Entity or AgentRef. / 领域 Entity 或 AgentRef。 |
| ActorRef / 行为主体引用 | Immutable per-operation attribution binding to a verified Principal and acting/delegation context. / 每次操作不可变的归因引用，绑定已验证 Principal 及行为/委托上下文。 | PrincipalRef, bearer token, reusable user ID. / PrincipalRef、Bearer Token 或可复用 User ID。 |
| Permission / 权限 | I policy decision for a specific Principal/action/resource/purpose/scope/audience/current epoch. / I 针对特定 Principal、Action、Resource、Purpose、Scope、Audience 和当前 Epoch 作出的策略决定。 | ScopeRef or any identifier. / ScopeRef 或任意标识符。 |
| ScopeRef / 作用域引用 | Typed namespace/ownership/applicability boundary. / 表示命名空间、所有权或适用边界的类型化引用。 | Permission grant. / 权限授予。 |
| EnvironmentRef / 环境引用 | Stable identity of a world/save/simulation/device-fleet/external state domain. / 世界、存档、仿真、设备群或外部状态域的稳定身份。 | Display name, coordinates, environment revision. / 显示名称、坐标或环境修订号。 |
| RuntimeSessionRef / 运行时会话引用 | Bounded runtime/session identity for correlation and binding. / 用于关联和绑定的有界运行时/会话身份。 | Conversation history, long-lived Agent identity. / Conversation 历史或长期 Agent 身份。 |

## 3. Identity stability rules / 身份稳定性规则

### 3.1 Domain object identity

1. Identity is opaque and non-semantic; content edits do not change object identity. / 身份是不透明且无语义的；内容编辑不得改变对象身份。
2. A new immutable version/revision receives its own version identity while the parent aggregate identity remains stable. / 新的不可变 Version/Revision 获得独立版本身份，同时父聚合身份保持稳定。
3. An identity, once assigned, is never silently recycled or reused. / 身份一经分配，不得静默回收或复用。
4. A display label, alias, normalized text, embedding, or content digest is not a canonical identity. / 显示标签、别名、规范化文本、Embedding 或内容摘要都不是规范身份。
5. The same content may legitimately exist as multiple domain objects in different ownership, purpose, time, or source contexts. / 相同内容在不同所有权、用途、时间或来源上下文中可以合法地对应多个领域对象。
6. Merge/split is an explicit identity-governance operation with retained lineage and reference migration; no silent ID reassignment. / 合并/拆分必须是显式身份治理操作，保留谱系并迁移引用；不得静默重新分配 ID。
7. Supersession creates an explicit predecessor/successor relation; it does not make IDs aliases. / Supersession 建立明确的前驱/后继关系，不会使两个 ID 成为别名。
8. Forget does not authorize identity reuse. Reappearance of equivalent content must pass D/I lifecycle, suppression, provenance and admission rules; content equality cannot resurrect a forgotten object. / Forget 不授权复用身份。等价内容重新出现时，必须经过 D/I 生命周期、抑制、Provenance 和准入规则；内容相等不能使已遗忘对象复活。

### 3.2 Version identity

Memory identity remains stable across immutable Memory Versions. MemoryVersionId identifies one immutable snapshot. ContextVersion is a separate G-owned identity and is never cast to MemoryVersionId. Claim identity across Memory Versions remains OPEN until the Fact/Claim and Claim identity ADRs are resolved; current embedded ClaimSnapshot representation must not be assumed to settle it.

Memory 身份在不可变 Memory Version 之间保持稳定；MemoryVersionId 标识一个不可变快照。ContextVersion 是 G 所有的独立身份，不得转换为 MemoryVersionId。Claim 跨 Memory Version 的身份仍为 OPEN，必须等待 Fact/Claim 和 Claim identity ADR；当前嵌入式 ClaimSnapshot 表示不能被当作该问题已解决。

## 4. Typed identity namespace / 类型化身份命名空间

The existing B Phase 3.6 proposal defines the following distinct reference types. This inventory records B's typed semantic proposal, not a claim that all consumer contracts or governance approvals are complete.

现有 B Phase 3.6 提案定义以下不同引用类型。本清单记录 B 的类型语义提案，不表示所有消费者契约或治理批准均已完成。

| Type / 类型 | Namespace / identity boundary / 命名空间与身份边界 | Authority / 权威 |
|---|---|---|
| PrincipalRef / Principal 引用 | Issuer + tenant/security domain + Principal kind + opaque subject ID. / Issuer + Tenant/安全域 + Principal 类型 + 不透明 Subject ID。 | I registry; B type semantics. / I 注册表；B 负责类型语义。 |
| IssuerRef / Issuer 引用 | Trust domain / issuer registry + opaque issuer ID. / 信任域或 Issuer 注册表 + 不透明 Issuer ID。 | I. / I。 |
| ActorRef / 行为主体引用 | Per-operation attribution namespace; immutable ID. / 每次操作独立的归因命名空间；ID 不可变。 | B type; I validates; H binds. / B 定义类型；I 验证；H 绑定。 |
| AgentRef / Agent 引用 | Agent registry + tenant/security domain. / Agent 注册表 + Tenant/安全域。 | Agent/deployment registry; I binding. / Agent/部署注册表；I 负责绑定。 |
| AdapterRef / Adapter 引用 | Adapter application registry + tenant/security domain; instance separate. / Adapter 应用注册表 + Tenant/安全域；实例身份另行区分。 | H registry; I Principal trust. / H 注册表；I 负责 Principal 信任。 |
| ProducerRef / Producer 引用 | Issuer + tenant/security domain + producer namespace. / Issuer + Tenant/安全域 + Producer 命名空间。 | I registration; E/D enforce. / I 注册；E/D 强制执行。 |
| ScopeRef / Scope 引用 | Scope authority + tenant/security domain + scope kind + opaque Scope ID. / Scope 权威 + Tenant/安全域 + Scope 类型 + 不透明 Scope ID。 | B type; I/G registry/policy. / B 定义类型；I/G 负责注册表/策略。 |
| EnvironmentRef / Environment 引用 | Environment authority + tenant/project + environment kind + opaque ID. / Environment 权威 + Tenant/Project + Environment 类型 + 不透明 ID。 | Environment registry; I bridge policy. / Environment 注册表；I 负责跨域桥接策略。 |
| RuntimeSessionRef / 运行时会话引用 | Issuer + runtime/Agent/Adapter instance + session namespace. / Issuer + Runtime/Agent/Adapter 实例 + Session 命名空间。 | H/platform session authority; I trust policy. / H/平台会话权威；I 信任策略。 |

A consumer must preserve type discriminator, issuer/authority namespace and security-domain dimensions. Weakening a typed reference into an untyped string loses essential semantics and is prohibited where it creates ambiguity.

消费者必须保留类型判别符、Issuer/Authority 命名空间和安全域维度。在会造成歧义时，将类型化引用弱化为无类型字符串会丢失必要语义，必须禁止。

## 5. Reference and trust resolution order / 引用与信任解析顺序

The following is the B/I/H semantic dependency order; it is not a wire schema or a replacement for owner-specific executable workflow:

以下是 B/I/H 的语义依赖顺序，不是 Wire Schema，也不替代 Owner 专属的可执行流程：

1. H/platform authenticates protected transport/session/workload context. / H/平台认证受保护的 Transport、Session 和 Workload 上下文。
2. I validates issuer, credential/key, audience, validity and revocation; resolves PrincipalRef. / I 验证 Issuer、Credential/Key、Audience、有效期和撤销状态，并解析 PrincipalRef。
3. Resolve AgentRef, AdapterRef, ProducerRef and RuntimeSessionRef through authoritative registries and bind them to the authenticated Principal. / 通过权威注册表解析 AgentRef、AdapterRef、ProducerRef 和 RuntimeSessionRef，并将其绑定到已认证 Principal。
4. Compare payload identity claims with verifier-produced bindings; mismatch/unknown required binding fails closed. / 将载荷身份声明与验证器生成的绑定进行比较；不匹配或必需绑定未知时必须 Fail Closed。
5. Resolve ActorRef from verifier-produced operation context; validate Principal, Issuer and delegation attribution. / 从验证器生成的操作上下文解析 ActorRef，并验证 Principal、Issuer 和委托归因。
6. Resolve ScopeRef and EnvironmentRef against authoritative registries; validate type, namespace, status, parent and compatibility. / 通过权威注册表解析 ScopeRef 和 EnvironmentRef，并验证类型、命名空间、状态、父级和兼容性。
7. I authorizes the exact Principal + Actor + action + resource + purpose + audience + Scope/Environment + delegation tuple. / I 对精确的 Principal + Actor + Action + Resource + Purpose + Audience + Scope/Environment + Delegation 元组进行授权。
8. Revalidate current PermissionEpoch and the independent D ForgetFence at the owner-defined final commit/disclosure boundary. / 在 Owner 定义的最终提交/披露边界重新验证当前 PermissionEpoch 和独立的 D ForgetFence。

## 6. Non-equivalence invariants / 不等价不变量

- PrincipalRef ≠ AgentRef ≠ AdapterRef ≠ ProducerRef. / PrincipalRef、AgentRef、AdapterRef、ProducerRef 彼此不同。
- ActorRef ≠ PrincipalRef and is not reusable across materially different operations/session/delegation context. / ActorRef 不等于 PrincipalRef；在实质不同的操作、Session 或 Delegation 上下文中不得复用。
- ScopeRef does not grant Permission. / ScopeRef 不授予 Permission。
- EnvironmentRef ≠ Environment ScopeRef ≠ Environment revision. / EnvironmentRef、Environment ScopeRef 和 Environment Revision 彼此不同。
- RuntimeSessionRef ≠ Session ScopeRef ≠ Conversation. / RuntimeSessionRef、Session ScopeRef 和 Conversation 彼此不同。
- Ref resolution ≠ authentication; authentication ≠ authorization. / Ref 解析不等于认证；认证不等于授权。
- PermissionEpoch ≠ D ForgetFenceGeneration; neither may be compared, converted or substituted. / PermissionEpoch 不等于 D ForgetFenceGeneration；二者不得比较、转换或替代。
- Domain Entity identity ≠ Security Principal identity, even when a person/Agent is represented in both domains. / 即使同一 Person/Agent 同时出现在两个领域中，Domain Entity 身份仍不等于 Security Principal 身份。

## 7. Physical serialization identity is not domain identity / 物理序列化身份不等于领域身份

B Phase 3.8.6 exact review approves the per-authority nominal type boundary for Storage Option A (B review Blob e2bc4c8dde9706bfbe443269b702f1b5aa6965f6; exact Storage ADR Blob bb544ba2f346bdc130d524bd5c7310d86f367988). This is a delegated B-role technical review, not an independent human B Owner signature, and is limited to L1/L2 type-system approval.

B Phase 3.8.6 精确复审批准 Storage Option A 的 per-authority 名义类型边界（B 复审 Blob e2bc4c8dde9706bfbe443269b702f1b5aa6965f6；Storage ADR Blob bb544ba2f346bdc130d524bd5c7310d86f367988）。这是委托 B 角色技术复审，不是独立人类 B Owner 签字，范围限于 L1/L2 类型系统批准。

| Type | Meaning | Must not alias |
|---|---|---|
| BrainAuthorityRef | Canonical Memory semantic authority | StorageAuthorityRef, PolicyDomainRef |
| SerializationDomainRef | Physical/logical transaction domain | BrainAuthorityRef, COC domain |
| AuthoritySerializationAnchorRef | One physical anchor row per BrainAuthority | SerializationDomainRef, D Fence, VisibilityPointer |
| SerializationTransitionRef | Stable idempotent physical transition identity | PublicationOperationId, PreparedTransactionGID |
| SerializationRevision | Monotonic physical revision local to one anchor/domain | D FenceGeneration, GateGeneration, BarrierGeneration, I PermissionEpoch, C sequence, COC position, XID |
| PreparedTransactionGID | Stable prepared transaction identity | EngineNativeXIDRef, SerializationTransitionRef |
| D PublicationParticipantRef | D barrier admission identity | StorageVisibilityParticipantRef, COC ParticipantIntentRef |
| I CommitAuthorizationReceiptRef | I single-use sequencer decision | PermissionEpoch, SerializationRevision |
| PublicationOperationId | Logical publication operation | WorkItemId, AttemptId, SerializationTransitionRef |
| ParticipantTupleDigest | Exact cross-owner participant tuple digest | RequestDigest, ArtifactDigest |
| VisibilityPointerRef | Public Storage visibility root | PrivateStageRef, PublicationReceiptRef |

Rules: one AuthoritySerializationAnchorRef per BrainAuthorityRef/SerializationDomainRef; SerializationRevision orders only physical transitions within that anchor and is not comparable across authorities. D ForgetFenceGeneration, owner_gate_generation and barrier_generation remain distinct D types. I PermissionEpoch, C sequence namespace/record sequence, COC quorum position, Storage PreparedTransactionGID and engine-native XID remain separate. Storage physically owns the anchor but cannot create or interpret D/I/C/COC semantic decisions. Same SerializationTransitionRef + same immutable digest is idempotent; same ref with a different digest is an integrity incident.

规则：每个 BrainAuthorityRef/SerializationDomainRef 对应一个 AuthoritySerializationAnchorRef；SerializationRevision 只排序该锚点内的物理转换，不能跨 Authority 比较。D ForgetFenceGeneration、owner_gate_generation、barrier_generation 是不同 D 类型；I PermissionEpoch、C sequence namespace/record sequence、COC quorum position、Storage PreparedTransactionGID 和 Engine-native XID 也必须分离。Storage 物理拥有锚点，但不能创建或解释 D/I/C/COC 语义决策。相同 SerializationTransitionRef + 相同不可变 Digest 才幂等；相同 Ref 配不同 Digest 属于完整性事件。

The anchor is an IMPLEMENTATION_DETAIL / physical serialization primitive, not a new canonical domain entity or universal global counter. E accepts with E lifecycle conditions; F accepts with read-path/cache conditions; Storage v3.2.11 remains candidate, not jointly accepted/frozen, and requires fresh A review. Physical DB, HA/restore, serializable behavior and production implementation remain L4 OPEN.

该 Anchor 属于 IMPLEMENTATION_DETAIL / 物理序列化原语，不是新的规范领域实体，也不是全局计数器。E 在 E 生命周期条件下接受；F 在读路径/缓存条件下接受；Storage v3.2.11 仍为候选，未获联合接受/冻结，且需要 A 新一轮复审。物理数据库、HA/Restore、Serializable 行为和生产实现仍为 L4 OPEN。

## 8. Unresolved namespace questions / 未决命名空间问题

1. Canonical Tenant vs Workspace vs Project vs User Scope taxonomy and parent/child algebra: OPEN; I/A confirmation required. / Tenant、Workspace、Project 与 User Scope 的规范分类及父子代数仍 OPEN，需 I/A 确认。
2. Whether one Principal may be federated across multiple tenant/security domains and under which issuer mapping: I GOVERNANCE-BLOCKED. / 一个 Principal 是否可跨多个 Tenant/安全域联邦，以及采用何种 Issuer 映射，仍被 I GOVERNANCE-BLOCKED。
3. Environment Registry Authority designation and closed-world registry completeness: NOT VERIFIED; cross-environment access remains fail closed. / Environment Registry Authority 的指定及封闭世界注册表完整性尚 NOT VERIFIED；跨 Environment 访问继续 Fail Closed。
4. Exact typed Ref wire names/encoding and authenticated context fields: H-owned; no B unilateral freeze. / 类型化 Ref 的精确 Wire 名称/编码及认证上下文字段由 H 负责；B 不得单方面冻结。
5. Canonical Agent logical identity vs runtime instance/session relationships: C/I/H confirmation required. / 规范 Agent 逻辑身份与 Runtime Instance/Session 关系需 C/I/H 确认。
6. ExternalId uniqueness and issuer-scoped collision behavior: I policy OPEN. / ExternalId 唯一性和 Issuer 作用域内冲突处理仍为 I 策略 OPEN。
7. Claim identity across Memory Versions: B ADR OPEN. / Claim 跨 Memory Version 的身份策略仍为 B ADR OPEN。
8. Whether Session and Conversation are separate domain entities: C/G OPEN; do not conflate with RuntimeSessionRef or Session ScopeRef. / Session 与 Conversation 是否为独立领域实体仍由 C/G OPEN；不得与 RuntimeSessionRef 或 Session ScopeRef 混淆。

## 9. Conflict and decision status / 冲突与决策状态

- B Phase 3.6 typed identity proposal Blob `0a6b78...` labels itself JOINT-DECIDED technical baseline, but explicitly says no separate B-session signature is claimed and implementation tests were not run. / B Phase 3.6 类型化身份提案 Blob `0a6b78...` 将自身标记为 JOINT-DECIDED 技术基线，但明确未声称存在单独 B Session 签字，且实现测试未运行。
- I's current identity-trust closure Blob `0cbf6bb...` says technical baseline JOINT-DECIDED but external governance approvals remain GOVERNANCE-BLOCKED and implementation/conformance NOT VERIFIED. / I 当前身份信任闭合 Blob `0cbf6bb...` 表明技术基线 JOINT-DECIDED，但外部治理批准仍 GOVERNANCE-BLOCKED，实现/一致性仍 NOT VERIFIED。
- H current protected-operation binding Blob `e7ca5c...` says governance and consumer acceptance OPEN; implementation/conformance NOT VERIFIED. / H 当前受保护操作绑定 Blob `e7ca5c...` 表明治理和消费者验收 OPEN；实现/一致性 NOT VERIFIED。
- B formally APPROVED ActorRef/ScopeRef/EnvironmentRef semantic type mapping for the exact BIH package (A Blob `a45ae90b318a79bf009d14f4d917611881e9e214`) and exact CGH-APPLIED-1.1 recovery-batch pair above. C/F/G BIH consumer design decisions were recorded ACCEPT WITH ENUMERATED EXCEPTIONS; H ACCEPTED the BIH package. The separate CGH-APPLIED-1.1 C/D/G/H/I/B decisions are also recorded with enumerated exceptions, while Storage confirmed its architecture interface with changes. / B 已针对精确 BIH Package（A Blob `a45ae90b318a79bf009d14f4d917611881e9e214`）及上述精确 CGH-APPLIED-1.1 Recovery-batch 配对正式 APPROVED ActorRef/ScopeRef/EnvironmentRef 语义类型映射。C/F/G 的 BIH 消费者设计决策记录为 ACCEPT WITH ENUMERATED EXCEPTIONS；H 接受该 BIH Package。独立的 CGH-APPLIED-1.1 C/D/G/H/I/B 决策也均记录了列明例外，Storage 则在变更条件下确认架构接口。
- These are exact-version semantic/design acceptances only. They do not freeze H wire encoding, close I36-GOV-01..10, prove runtime conformance or production readiness. Applied Contract Frozen remains NO; COC/Storage physical implementation and fault tests remain open. / 以上仅为精确版本的语义/设计验收，不冻结 H Wire 编码，不关闭 I36-GOV-01..10，不证明运行时一致性或生产就绪。Applied Contract Frozen 仍为 NO；COC/Storage 物理实现和故障测试仍开放。

## 10. Decision record / 决策记录

**B-ID-DEC-001 — Preserve distinct typed references and separate reference from trust / 保留不同类型化引用，并区分引用与信任**
- Context: payload identity, authenticated principal, domain scope and authorization had been at risk of being conflated. / 背景：载荷身份、已认证 Principal、领域 Scope 和授权曾面临被混为一谈的风险。
- Alternatives: untyped string IDs; one universal Actor/User ID; distinct typed references with verifier/registry binding. / 备选方案：无类型字符串 ID；统一 Actor/User ID；通过验证器/注册表绑定的不同类型化引用。
- Candidate decision: preserve distinct typed references; no implicit casts; reference never proves authentication or permission. / 候选决定：保留不同类型化引用；禁止隐式转换；引用本身永远不能证明认证或权限。
- Consequences: safer cross-module validation, but requires registries, explicit mappings and schema compatibility. / 后果：跨模块验证更安全，但需要注册表、显式映射和 Schema 兼容性。
- Affected owners: B, I, H, C, D, E, G. / 受影响 Owner：B、I、H、C、D、E、G。
- Reversal condition: only a documented domain case proving two concepts are semantically identical without loss of namespace, lifecycle, authority or trust semantics. / 撤销条件：仅当有文档证明两个概念在不损失命名空间、生命周期、权威或信任语义的前提下完全相同时，才可撤销。
- Status: CANDIDATE FOR B CANONICAL MODEL; existing delegated technical decision retained as evidence, no new cross-owner approval inferred. / 状态：B 规范模型候选；保留既有委托技术决策作为证据，不推断存在新的跨 Owner 批准。

## 11. Gate status / 门禁状态

B identity semantics are sufficiently explicit for continued model reconciliation, but B2/B3 remain open. This document does not resolve Fact/Claim, Tenant/Workspace, external governance, cross-owner wire binding or runtime conformance. No schema freeze or authorization for implementation is claimed.

B 身份语义已足以继续领域模型协调，但 B2/B3 仍未通过。本文件不解决 Fact/Claim、Tenant/Workspace、外部治理、跨 Owner Wire 绑定或运行时一致性问题。不宣称 Schema 冻结或实现授权。
