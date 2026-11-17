# Canonical Domain Relationships
# 规范领域关系

- ID: B-REL-001
- Status: CANDIDATE RELATIONSHIP MODEL; owner-owned cardinalities require acceptance
- Sources: core entities Blob 8cb5a674eec8eac1f3c4d83c400dc08d00166f23; relationships/provenance Blob e762f84c59f69de7a44baad2123aed46e1ffea16; identity closure Blob 0a6b78a842e550b58533b797cdfcd2d954ed6826; G Context Blob c1de241ec69834377d9b0e24aa4770a809796d4b.

## 1. Relationship kinds / 关系类型

- **Composition:** child is a constituent of parent and its lifecycle is constrained by parent; does not automatically imply shared physical row.
- **Association:** typed semantic link between independent objects; both identities remain independent.
- **Reference:** typed pointer; does not imply ownership, permission, or composition.
- **Derivation:** target produced from source(s) through a declared process; source/target direction is immutable and traceable.
- **Ownership:** authority/custody relationship defining who may govern lifecycle; distinct from applicability and authorization.
- **Causal:** establishes an evidenced before/after or cause/outcome relation; timestamps alone may be insufficient for concurrency order.
- **Temporal:** states when a relation/assertion holds; separate from record lifecycle and transaction time.

## 2. Core relationship matrix / 核心关系矩阵

| Source → Target | Kind | Cardinality / optionality | Owner | Lifecycle / referential integrity | Forget / deletion semantics | Cross-Tenant / version rules |
|---|---|---|---|---|---|---|
| Memory → MemoryVersion | Composition / version ownership | 1 Memory : 1..N immutable Versions; current pointer exactly 1 after first commit | D; Storage persists | Version immutable; parent Memory stable; version sequence monotonic, no reuse | Forget gates content access across identity/version family and registered descendants; physical erasure separate | Version ref must bind Memory ID + version ID; no cross-tenant alias |
| MemoryVersion → ClaimSnapshot | Composition (candidate) | 1 version : 0..N snapshots; empty only for declared non-propositional kind | B semantics; D canonical; E producer | Immutable snapshot; Claim identity across versions OPEN | Source evidence/claim lineage subject to D/I Forget; no plaintext retention beyond policy | Claim ref and snapshot identity must not be conflated |
| Claim → Evidence | Association | N:M; one Claim needs ≥1 epistemic basis for Verified; Evidence may support/refute multiple Claims | B semantics; E evidence production; I access policy | Link role/strength/time/scope is Claim-relative; link versioned/immutable if assessed | Forget may suppress Evidence and dependent claims; preserve only permitted non-reconstructive metadata | Both ends independently scope-authorized; no implicit cross-tenant support |
| Evidence → Source | Reference / origin association | Each Evidence 1 source_ref; a Source may have 0..N Evidence | E source capture; B type semantics | Typed source identity/version; source may be external/unavailable | Source retention policy controls content; Evidence availability updated without erasing historical existence | Source refs namespaced by issuer/authority; external IDs never canonical IDs |
| Memory → MemorySource | Association (default) | 0..N source links per Memory; each link one source ref + role/locator/scope | B semantics; E produces; D persists | Promote MemorySource to entity only if link itself has independent lifecycle/identity | Link removed/suppressed per Forget; source data handled separately | Typed source version and Scope; no string-only identity |
| Derived Memory → Source Memory / Event | Derivation | Derived target 1..N direct source refs; sources 0..N targets | E production; D lineage/fence | Immutable lineage manifest; preserve transitive ancestry and exact versions | D registers dependencies before visible; source Forget suppresses descendants according to fence | Every source edge independently scoped/authorized; no cross-tenant derivation without I-approved explicit grant |
| Derived Artifact → Provenance | Composition/reference | 1 target : 1..N provenance refs or explicit unavailable reason | B semantics; E producer | Provenance captures method/version/time/input digests; graph cycle policy OPEN | Forget may restrict provenance payload; non-reconstructive audit metadata only | Preserve source namespace and issuer; no unverified model attribution |
| Entity → Relation | Association | Entity 0..N Relations; Relation has exactly two typed endpoints in current binary model | B semantics; Entity/Relation Manager | Endpoint types validated; Relation has own ID, type, direction, qualifiers, Valid Time and evidence | Forget/scope policy applies to endpoints and relation; do not leave dangling disclosure path | Both endpoints independently authorized; explicit cross-scope relation does not grant access |
| Relation → Evidence | Association | N:M | B semantics; E evidence | Evidence support is relation-relative | Same as Claim–Evidence; retain only permitted metadata | Each Evidence dereference separately authorized |
| Principal → ActorRef | Attribution/reference | 1 Principal : 0..N ActorRefs; each ActorRef resolves to 1 Principal and one operation context | B ActorRef type; I Principal validation; H verifier binding | ActorRef immutable per operation; distinct session/delegation context requires distinct ref | Revocation does not rewrite historical ActorRef; current authorization rechecked | Issuer/security-domain namespace required; no cross-tenant implicit identity |
| Principal → Agent/Adapter/Producer | Registered binding association | N:M only through explicit registry mapping | I trust/Principal; C/H/E registry owners | Workload identity distinct from security Principal; instances/epochs separate | Revocation disables new operations; historical attribution retained | No string equality or implicit inheritance; I policy controls scope |
| Scope → Domain Asset | Ownership/applicability association | Asset 1..N role-tagged ScopeRefs; Scope 0..N assets | B type; I/G policy | Ownership Scope and Applicability Scope are distinct roles | Scope closure/revocation restricts access; does not silently delete asset | Fail closed for ambiguous tenant/security-domain mismatch |
| Environment → Scope / Claim / Relation | Reference + temporal qualification | 0..N associations; environment-bound Claim/Relation requires exact EnvironmentRef | B type; I bridge policy; environment registry owner | EnvironmentRef distinct from Environment Scope and revision | Environment retirement does not erase history; bridge access policy-controlled | Cross-environment denied by default absent explicit mapping/authorization |
| Context → ContextVersion | Composition/version ownership | 1 Context : 1..N immutable ContextVersions; current pointer one | G | ContextVersion is desired-state snapshot, immutable; CAS/ChangeSet semantics G-owned | Forget invalidates current-use membership and delivery; historical snapshot audit-only if policy allows | Context scope-bound; never cast to MemoryVersion |
| ContextVersion → ContextEntry | Composition | 1 version : 0..N entries | G | Entry references exact Memory ID + MemoryVersion; membership changes create new ContextVersion | Remove is membership change, not canonical Forget; Forget invalidates affected entries | Source Memory scope checked independently; no scope inheritance |
| ContextVersion → ChangeSet | Association / causal | 0..N ChangeSets; each ChangeSet binds exact base/target digest and outcome | G | Stale base rejected; applied/committed reconciliation run separate from version state | Superseded ChangeSet cannot be replayed as current delivery | Exact ContextVersion references; no cross-scope mutation |
| F Retrieval → G Context | Reference/selection handoff | One retrieval request yields 0..N candidate refs; G selects 0..N | F supplies candidate/rank; G owns membership | Candidate list may be incomplete/truncated; G revalidates canonical refs | Forgotten/suppressed refs cannot be selected or delivered | Scope authorization per ref; F Working Set is not Context |
| Delivery → ContextVersion | Reference | Each Delivery targets exactly one ContextVersion + attempt; version may have 0..N attempts | G; H transports | Attempt immutable; late ACK historical only; no head rollback | Forget/revocation cancels/supersedes and blocks late Applied | Exact Adapter/session/capability binding |
| CSubmitOutcome → Delivery/ContextVersion | Causal/reference | Each outcome binds one exact final request, delivery attempt and ContextVersion; retries preserve operation identity when outcome unknown | C | Immutable provider-boundary evidence; Unknown/InDoubt non-terminal | Must not promote to Applied without G validation; current-use can be invalidated later | Exact request digest, Scope, Environment, Actor/Principal binding |
| G Applied Record → C/H/I/D evidence | Evidence association | Each Applied record references one exact request boundary and required evidence vector | G commits; C/H/I/D issue evidence | Historical Applied immutable; current-use eligibility separate | Forget/revocation invalidates current use, not historical truth | All issuer, scope and authority-specific epochs validated |
| Operation → Protocol Message | Reference/correlation | 1 operation : 0..N protocol messages; each message references one operation/attempt/correlation | Operation owner + H wire | Message is not operation state; ACK bounded to message/action | Deletion/Forget operation state not represented by arbitrary protocol status | Wire reference preserves typed operation identity |
| ForgetOperation → ForgetFence / Targets | Causal/ownership | One operation establishes 0..N target fences; target set immutable per operation version | D; I policy | Fence generation monotonic; target/source/ancestor lineage; barriers tracked | D CanonicalSuppressionComplete distinct from I global completion and physical purge | Scope and target inventory exact; no cross-tenant omission |
| Storage PublicationReceipt → VisibilityPointer | Composition/transaction evidence | Published artifact has one matching authoritative pointer and receipt | Storage | Pointer + receipt + owner outcome atomically committed per proposed JF-10; exact readback required | Private staged bytes never visible; physical purge separate | Receipt binds exact operation/digest/XID/owner boundary; no stale replica inference |

## 2A. Chinese relationship matrix mirror / 中文关系矩阵对照

| Source → Target / 来源→目标 | Kind / 类型 | Cardinality / 基数 | Owner / 权威 | Lifecycle & reference / 生命周期与引用 | Forget, deletion & scope / Forget、删除与 Scope |
|---|---|---|---|---|---|
| Memory → MemoryVersion | Composition / 组合与版本归属 | 一个 Memory 对应 1..N 个不可变 Version；首次提交后当前指针恰为一个 | D；Storage 持久化 | Version 不可变；Memory 身份稳定；版本序列单调且不可复用 | Forget 覆盖身份/版本族及登记的派生后代；物理擦除另行证明。引用必须绑定 Memory ID + Version ID，不得跨 Tenant 别名化。 |
| MemoryVersion → ClaimSnapshot | Composition（候选）/ 组合 | 一个 Version 对应 0..N 个 Snapshot；仅声明为非命题类型时允许为空 | B 语义；D 规范存储；E 生产 | Snapshot 不可变；Claim 跨版本身份仍 OPEN | Source Evidence/Claim 谱系受 D/I Forget 约束；不得超出策略保留明文。Claim Ref 与 Snapshot 身份不得混同。 |
| Claim → Evidence | Association / 关联 | N:M；Verified Claim 至少需要一项认知依据；Evidence 可支持/反驳多个 Claim | B 语义；E 生产 Evidence；I 访问策略 | 关联角色/强度/时间/Scope 相对于 Claim；评估结果需要独立版本时应不可变 | Forget 可抑制 Evidence 和依赖 Claim；只保留策略允许且不可重建内容的元数据。两端分别授权，不隐式跨 Tenant 支持。 |
| Evidence → Source | Reference / 来源引用 | 每个 Evidence 有一个 source_ref；一个 Source 可关联 0..N 个 Evidence | E 来源捕获；B 类型语义 | Source 身份/版本类型化；外部 Source 可不可用 | Source 保留策略控制内容；Evidence 可用性更新不得抹去历史存在。Source Ref 按 Issuer/Authority 命名空间，外部 ID 不是 Canonical ID。 |
| Memory → MemorySource | Association（默认）/ 关联 | 每个 Memory 有 0..N 个来源链接；每个链接含一个 Source Ref、角色、Locator 和 Scope | B 语义；E 生成；D 持久化 | 仅当链接自身具备独立生命周期/身份时才升级为实体 | Forget 按规则移除/抑制链接；来源数据单独处理。必须使用类型化 Source Version 和 Scope，不得仅用字符串。 |
| Derived Memory → Source Memory / Event | Derivation / 派生 | 每个派生目标至少引用一个直接源；源可派生到多个目标 | E 生产；D 谱系/Fence | 不可变 Lineage Manifest；保留传递祖先和精确版本 | 发布前由 D 登记依赖；源 Forget 按 Fence 抑制后代。每条 Source Edge 独立授权，跨 Tenant 派生须 I 明确授权。 |
| Derived Artifact → Provenance | Composition / Reference | 每个目标有 1..N 个 Provenance Ref，或明确记录不可用原因 | B 语义；E 生产 | Provenance 记录方法/版本/时间/输入摘要；图循环策略 OPEN | Forget 可限制 Provenance 载荷；仅保留不可重建审计元数据。保留来源命名空间和 Issuer，不得伪造模型归因。 |
| Entity → Relation | Association / 关联 | Entity 可有 0..N 个 Relation；当前二元模型中 Relation 恰有两个类型化端点 | B 语义；Entity/Relation Manager | 验证端点类型；Relation 自有 ID、类型、方向、限定符、Valid Time 和 Evidence | Forget/Scope 策略作用于端点及关系；不得留下可披露的悬空路径。端点分别授权，跨 Scope 关系不授予访问权。 |
| Relation → Evidence | Association / 关联 | N:M | B 语义；E Evidence | Evidence 支持关系的含义相对于具体 Relation | 与 Claim–Evidence 相同；仅保留允许的元数据。每次 Evidence 解引用均需独立授权。 |
| Principal → ActorRef | Attribution / Reference / 归因引用 | 一个 Principal 对应 0..N 个 ActorRef；每个 ActorRef 解析到一个 Principal 和一个操作上下文 | B 定义 ActorRef 类型；I 验证 Principal；H 绑定 | ActorRef 按操作不可变；不同 Session/Delegation 上下文需要不同 Ref | 撤销不得改写历史 ActorRef；当前授权重新验证。要求 Issuer/安全域命名空间，不得跨 Tenant 隐式继承。 |
| Principal → Agent/Adapter/Producer | Registered Binding / 注册绑定 | 仅通过显式注册表映射形成 N:M | I 信任/Principal；C/H/E 注册表 Owner | Workload Identity 与 Security Principal 不同；实例和 Epoch 分开 | 撤销阻止新操作，保留历史归因。禁止字符串相等或隐式继承；Scope 由 I 策略控制。 |
| Scope → Domain Asset | Ownership / Applicability / 所有权与适用性关联 | 每个 Asset 有 1..N 个带角色的 ScopeRef；Scope 可关联 0..N 个 Asset | B 类型；I/G 策略 | Ownership Scope 与 Applicability Scope 是不同角色 | Scope 关闭/撤销限制访问，不静默删除 Asset。Tenant/安全域不明确时 Fail Closed。 |
| Environment → Scope / Claim / Relation | Reference + Temporal Qualification / 引用与时间限定 | 0..N 个关联；绑定 Environment 的 Claim/Relation 必须有精确 EnvironmentRef | B 类型；I Bridge 策略；Environment Registry Owner | EnvironmentRef 与 Environment Scope、Revision 分离 | Environment 退役不删除历史；Bridge 访问受策略控制。无显式映射/授权时默认拒绝跨 Environment。 |
| Context → ContextVersion | Composition / Version Ownership / 组合与版本归属 | 一个 Context 对应 1..N 个不可变 ContextVersion；当前指针一个 | G | ContextVersion 是不可变期望状态 Snapshot；CAS/ChangeSet 语义由 G 拥有 | Forget 使当前使用成员资格和 Delivery 失效；历史 Snapshot 仅在策略允许时用于审计。Context 绑定 Scope，不能转换为 MemoryVersion。 |
| ContextVersion → ContextEntry | Composition / 组合 | 一个 Version 对应 0..N 个 Entry | G | Entry 引用精确 Memory ID + MemoryVersion；成员变更产生新 ContextVersion | Remove 是成员关系变更，不是 Canonical Forget；Forget 使相关 Entry 失效。Source Memory Scope 独立检查，不继承 Context Scope。 |
| ContextVersion → ChangeSet | Association / Causal / 关联与因果 | 0..N 个 ChangeSet；每个绑定精确 Base/Target Digest 和结果 | G | 拒绝过期 Base；Applied/Committed Reconciliation 与 Version 状态分离 | Superseded ChangeSet 不得作为当前 Delivery 重放。必须引用精确 ContextVersion，不得跨 Scope 修改。 |
| F Retrieval → G Context | Reference / Selection Handoff / 引用与选择交接 | 一次 Retrieval 返回 0..N 个候选 Ref；G 选择 0..N 个成员 | F 提供候选/排序；G 拥有成员资格 | 候选列表可不完整/被截断；G 必须重新验证规范引用 | Forgotten/Suppressed Ref 不得被选择或交付。每个 Ref 独立检查 Scope 授权；F Working Set 不等于 Context。 |
| Delivery → ContextVersion | Reference / 引用 | 每个 Delivery 精确指向一个 ContextVersion 和一次 Attempt；一个 Version 可有 0..N 次 Attempt | G；H 传输 | Attempt 不可变；迟到 ACK 仅是历史证据，不回滚 Head | Forget/撤销取消或 Supersede 并阻止迟到 Applied。绑定精确 Adapter/Session/Capability。 |
| CSubmitOutcome → Delivery/ContextVersion | Causal / Reference / 因果与引用 | 每个 Outcome 绑定精确 Final Request、Delivery Attempt 和 ContextVersion；未知结果重试保持操作身份 | C | Provider 边界证据不可变；Unknown/InDoubt 非终态 | 未经 G 验证不得提升为 Applied；当前使用资格可后续失效。绑定精确 Request Digest、Scope、Environment、Actor/Principal。 |
| G Applied Record → C/H/I/D evidence | Evidence Association / 证据关联 | 每个 Applied Record 引用一个精确请求边界和所需证据向量 | G 提交；C/H/I/D 签发证据 | 历史 Applied 不可变；当前使用资格独立判断 | Forget/撤销使当前使用失效，不改变历史事实。验证所有 Issuer、Scope 和 Authority-specific Epoch。 |
| Operation → Protocol Message | Reference / Correlation / 引用与关联 | 一个 Operation 对应 0..N 条 Protocol Message；每条消息引用一个 Operation/Attempt/Correlation | Operation Owner + H Wire | Message 不是 Operation 状态；ACK 仅覆盖其声明的消息/动作 | 不得用任意 Protocol Status 表示 Delete/Forget Operation。Wire Ref 保留类型化操作身份。 |
| ForgetOperation → ForgetFence / Targets | Causal / Ownership / 因果与所有权 | 一个操作建立 0..N 个目标 Fence；目标集对操作版本不可变 | D；I 策略 | Fence Generation 单调；跟踪 Target/Source/Ancestor 谱系和 Barrier | D CanonicalSuppressionComplete 不等于 I Global Completion 或物理 Purge。Scope 与目标清单必须精确，不得跨 Tenant 遗漏。 |
| Storage PublicationReceipt → VisibilityPointer | Composition / Transaction Evidence / 组合与事务证据 | 已 Published 的 Artifact 恰有匹配的权威 Pointer 和 Receipt | Storage | 按提议的 JF-10 原子提交 Pointer + Receipt + Owner Outcome；必须精确读回 | Private Staged Bytes 永不可见；物理 Purge 另行证明。Receipt 绑定精确 Operation/Digest/XID/Owner 边界，不得从 Stale Replica 推断。 |

## 3A. Chinese referential-integrity invariants / 中文引用完整性不变量

1. 每个引用必须携带类型判别符和命名空间；不同实体类型之间禁止隐式转换。
2. 每个 Relation 端点必须满足已注册的 Relation Type 端点约束。
3. 每个派生对象必须具有完整的直接/传递谱系，或明确记录不可用原因；谱系不完整不得发布。
4. 派生边必须明确方向，不得含糊地从目标指向来源。
5. 跨 Tenant/Scope/Environment 引用不授予访问权；每个端点和 Evidence 解引用都必须单独授权。
6. 即使对象退役或 Superseded，历史引用仍保持类型化且可解析为历史身份；当前使用资格另行判断。
7. Context Entry 必须引用精确 MemoryVersion；ContextVersion 不得替代规范 Memory 版本。
8. Protocol Message 和 Receipt 可以引用 Operation，但不得因名称相似而成为规范领域实体。
9. Delete/Forget 传播由 Owner 生命周期和已登记依赖控制，不得依赖通用数据库级联删除。
10. 引用缺失、权威不可用或命名空间歧义必须返回 UNKNOWN/BLOCKED，不得视为成功。

## 4A. Chinese cardinality and modeling questions / 中文基数与建模问题

- 如果 Claim–Evidence 的链接强度、角色、时间和 Provenance 必须独立修订，则可能需要独立 Assessment Entity；否则类型化关联值对象即可。
- 当派生记录需要独立寻址时，Provenance 可以成为实体；否则类型化谱系边和不可变目标版本可能足够。状态 OPEN。
- MemorySource 默认应是类型化关联/值对象；只有证明其具有独立身份和生命周期时，才考虑独立 Source Entity。
- ContextEntry 当前由 G Schema 单独标识；B 将其最终实体/值对象分类交由 G 决定。
- ForgetOperation 和 Storage PublicationReceipt 是 Owner 拥有的操作/证据对象，不是通用 Memory 子对象。

## 3. Referential integrity invariants / 引用完整性不变量

1. Every reference carries a type discriminator and namespace; no implicit casts between entity types.
2. Every Relation endpoint satisfies the registered relation-type endpoint constraints.
3. Every derived object has complete direct/transitive lineage or an explicit unavailable reason; incomplete lineage cannot be published.
4. A derived edge must not point from target to source ambiguously; derivation direction is explicit.
5. Cross-Tenant/Scope/Environment references do not grant access; every endpoint and Evidence dereference is separately authorized.
6. Historical references remain typed and resolvable as historical identity even after retirement/supersession; current-use eligibility is separate.
7. A Context Entry references an exact MemoryVersion; ContextVersion does not replace canonical Memory version.
8. Protocol messages and receipts reference operations but do not become canonical domain entities by name similarity.
9. Deletion/Forget propagation is governed by owner lifecycle and registered dependencies, not generic cascading foreign-key deletion.
10. A missing reference, unavailable authority or ambiguous namespace is UNKNOWN/BLOCKED, not success.

## 4. Cardinality and modeling questions / 基数与建模问题

- Claim↔Evidence may require a first-class assessment entity if link-specific strength, role, time and provenance must be independently revised. Otherwise a typed association value is sufficient.
- Provenance may be a first-class entity when an independently addressable derivation record is required; otherwise typed lineage edges plus immutable target version may suffice. OPEN.
- MemorySource should default to a typed association/value object; standalone Source entity is deferred unless it has independent identity/lifecycle.
- ContextEntry is currently separately identified by G schema; B defers its final entity/value classification to G.
- ForgetOperation and Storage PublicationReceipt are owner-owned operation/evidence objects, not generic Memory children.

## 5. Gate status / 门禁状态

B2 remains IN PROGRESS; B3 remains NOT PASSED. This matrix records candidate semantic relationships. It does not prescribe database foreign keys, cascading deletion, aggregate transaction boundaries, or storage schema.

B2 仍在进行；B3 未通过。本矩阵记录候选语义关系，不规定数据库外键、级联删除、聚合事务边界或存储 Schema。
