# Canonical Domain Entity Inventory
# 规范领域实体清单

- ID: B-INV-001
- Status: CANDIDATE INVENTORY — B1 IN PROGRESS
- Baseline: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Primary source: `02-domain-model/core-entities.md` Blob `8cb5a674eec8eac1f3c4d83c400dc08d00166f23`; `domain-model-overview.md` Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`.

## 1. Classification rules / 分类规则

- **CANONICAL_ENTITY**: independently addressable domain object with identity and a meaningful reference/lifecycle.
  **CANONICAL_ENTITY（规范实体）**：具有独立身份、可独立寻址，并具有有意义的引用/生命周期的领域对象。
- **VALUE_OBJECT**: meaningful typed value whose identity is supplied by its containing object or relation.
  **VALUE_OBJECT（值对象）**：具有明确类型和值语义，但其身份由所属对象或关系提供的值。
- **DERIVED_VIEW**: runtime/query/presentation result that can be rebuilt and is not canonical truth.
  **DERIVED_VIEW（派生视图）**：可重建的运行时/查询/呈现结果，不属于规范事实。
- **PROTOCOL_OBJECT**: transport or adapter envelope; never a domain entity merely because it references one.
  **PROTOCOL_OBJECT（协议对象）**：传输层或适配器封套；不能仅因其引用某个领域对象就被视为领域实体。
- **IMPLEMENTATION_DETAIL**: persistence/runtime mechanism with no independent domain meaning.
  **IMPLEMENTATION_DETAIL（实现细节）**：不具有独立领域含义的持久化/运行时机制。
- **DEFERRED_CONCEPT**: potentially useful, but no demonstrated independent identity/lifecycle requirement.
  **DEFERRED_CONCEPT（延后概念）**：可能有用，但尚未证明其需要独立身份或生命周期。
- **REJECTED_ABSTRACTION**: duplicates another concept or falsely collapses distinct semantics.
  **REJECTED_ABSTRACTION（已拒绝抽象）**：重复其他概念，或错误合并本应区分的语义。

**中文：** CANONICAL_ENTITY 表示需要独立寻址和引用的规范领域对象；VALUE_OBJECT 是由所属对象/关系赋予身份的类型化值；DERIVED_VIEW 是可重建的运行时/查询/呈现结果；PROTOCOL_OBJECT 是传输对象；IMPLEMENTATION_DETAIL 是无独立领域含义的实现机制；DEFERRED_CONCEPT 是尚无独立身份/生命周期依据的概念；REJECTED_ABSTRACTION 是重复或错误合并语义的抽象。

## 2. Core canonical candidates / 核心规范实体候选

| Concept / 概念 | Classification / 分类 | Identity / lifecycle rationale / 身份与生命周期依据 | Decision status / 决策状态 |
|---|---|---|---|
| Event / 事件 | CANONICAL_ENTITY | Captured occurrence/report/observation; stable event_id, recorded_at, source and scope; may produce zero/many memories. / 被捕获的发生事项、报告或观察；具有稳定 event_id、recorded_at、source 和 scope；可产生零个或多个 Memory。 | DECIDED in source / 源规范已决定 |
| Memory / 记忆 | CANONICAL_ENTITY | Retained addressable knowledge asset; memory_id stable across immutable versions; lifecycle owned by D. / 被保留且可寻址的知识资产；memory_id 在不可变版本之间保持稳定；生命周期由 D 负责。 | DECIDED in source / 源规范已决定 |
| Memory Version / 记忆版本 | CANONICAL_ENTITY | Immutable historical snapshot with version ID and parent relation; independent reference needed for provenance/context. / 具有版本 ID 和父级关系的不可变历史快照；溯源/上下文需要独立引用。 | DECIDED in source / 源规范已决定 |
| Claim / 主张 | CANONICAL_ENTITY (identity policy OPEN / 身份策略开放) | Proposition with subject/predicate/object, epistemic and temporal qualifications; identity across versions remains OPEN. / 具有 subject/predicate/object 及认知、时间限定的命题；跨版本身份仍为 OPEN。 | DECIDED concept; OPEN identity / 概念已决定；身份开放 |
| Entity / 实体 | CANONICAL_ENTITY | Identity-bearing referent distinct from display name/mention; merge/split lineage. / 具有身份的指称对象，不等同于显示名称/文本提及；需保留合并/拆分谱系。 | DECIDED in source / 源规范已决定 |
| Relation / 关系 | CANONICAL_ENTITY | Typed, scoped, temporal association with endpoint constraints and lifecycle. / 具有类型、Scope、时间语义、端点约束和生命周期的关联。 | DECIDED in source / 源规范已决定 |
| Evidence / 证据 | CANONICAL_ENTITY | Independently addressable source material/observation with role, locator, access and availability. / 可独立寻址的来源材料/观察，具有角色、定位符、访问控制和可用性。 | DECIDED in source / 源规范已决定 |
| Provenance / 溯源 | CANONICAL_ENTITY candidate / 规范实体候选 | Derivation/origin record with inputs, method, time and lineage; identity needed for multi-generation trace. / 记录输入、方法、时间和谱系的派生/来源记录；多代追踪可能需要独立身份。 | Core concept DECIDED; exact record granularity OPEN / 核心概念已决定；记录粒度开放 |
| Memory Context / 记忆上下文 | CANONICAL_ENTITY | Scoped, versioned task-oriented selection with G-owned lifecycle/version authority. / 按 Scope 限定、带版本的任务导向选择集合；生命周期/版本权威由 G 负责。 | DECIDED concept; G contract authority / 概念已决定；G 拥有契约权威 |
| Context Entry / 上下文条目 | CANONICAL_ENTITY candidate / 规范实体候选 | Addressable reference/presentation inside Context; whether each entry needs standalone identity must be confirmed by G. / Context 内可寻址的引用/呈现项；每个条目是否需要独立身份须由 G 确认。 | DECIDED concept; identity TO_VALIDATE / 概念已决定；身份待验证 |
| Scope / 范围 | CANONICAL_ENTITY / typed family / 规范实体或类型化族 | Stable namespace/ownership/applicability reference; exact taxonomy/algebra OPEN with I. / 稳定的命名空间/所有权/适用性引用；精确分类/代数结构需与 I 协调，仍为 OPEN。 | Separation DECIDED; taxonomy OPEN / 区分已决定；分类开放 |

## 3. Value objects and typed references / 值对象与类型化引用

| Concept / 概念 | Classification / 分类 | Reason / 理由 | Status / 状态 |
|---|---|---|---|
| Opaque ID / 不透明 ID | VALUE_OBJECT | Non-semantic identifier value; algorithm not normative (UUIDv7 only candidate). / 不携带领域语义的标识值；算法不是规范要求（UUIDv7 仅为候选）。 | DECIDED semantics / 语义已决定 |
| TypedObjectRef / 类型化对象引用 | VALUE_OBJECT | Category + canonical identifier; prevents ambiguous cross-module references. / 类别加规范标识符；防止跨模块引用产生歧义。 | CANDIDATE; grammar not pinned / 候选；语法未固定 |
| ScopeRef / 范围引用 | VALUE_OBJECT | Typed reference to a Scope; not Permission. / 指向 Scope 的类型化引用；不等于 Permission。 | DECIDED separation; shape OPEN / 区分已决定；结构开放 |
| ActorRef / 行为者引用 | VALUE_OBJECT at B boundary / B 边界上的值对象 | Reference to acting identity; authenticated Principal semantics owned by I/H. / 指向执行行为的身份；经过认证的 Principal 语义由 I/H 负责。 | OPEN joint mapping / 联合映射开放 |
| ExternalId / 外部 ID | VALUE_OBJECT | Namespaced external identifier; uniqueness scoped by issuer/type/tenant as approved. / 带命名空间的外部标识符；其唯一性按获批的 issuer/type/tenant 范围确定。 | Candidate; policy OPEN / 候选；策略开放 |
| TimeValue / TimeInterval / 时间值与时间区间 | VALUE_OBJECT | Explicit instant/interval with uncertainty and precision; uncertainty encoding OPEN. / 明确表示时点/区间及其不确定性和精度；不确定性编码开放。 | Core distinction DECIDED / 核心区分已决定 |
| ClaimSnapshot / 主张快照 | VALUE_OBJECT | Immutable claim representation embedded in Memory Version unless separate versioned Claim identity required. / 嵌入 Memory Version 的不可变 Claim 表示；除非需要独立的版本化 Claim 身份。 | CANDIDATE pending Claim identity ADR / 候选，等待 Claim 身份 ADR |
| AliasRecord / 别名记录 | VALUE_OBJECT | Label/alias plus scope/time qualifiers; not an Entity. / 标签/别名及其 Scope/时间限定；不是 Entity。 | Source-defined / 源规范定义 |
| Locator / 定位符 | VALUE_OBJECT | Address/offset/span into source material; may be sensitive and independently authorized. / 指向来源材料的地址/偏移量/片段；可能敏感，且需独立授权。 | Source-defined / 源规范定义 |
| ContentRef / Digest / 内容引用与摘要 | VALUE_OBJECT | Opaque reference/integrity value; not the content itself. / 不透明引用/完整性值；不是内容本身。 | Source-defined / 源规范定义 |
| ConfidenceValue / 置信度值 | VALUE_OBJECT | Method-qualified estimate; never substitutes for Evidence or verification. / 由方法限定的估计值；绝不能替代 Evidence 或验证。 | Source-defined / 源规范定义 |
| Qualifiers / Role / Polarity / 限定符、角色与极性 | VALUE_OBJECT | Typed semantic qualifiers, not free-form identity-bearing objects. / 类型化语义限定符，不是自由形式且具有独立身份的对象。 | Source-defined / 源规范定义 |

## 4. Associations, provenance and derived views / 关联、溯源与派生视图

| Concept / 概念 | Classification / 分类 | Reason / 理由 | Status / 状态 |
|---|---|---|---|
| Memory Source / 记忆来源 | CANONICAL_ENTITY or association record / 规范实体或关联记录 | Typed, version-aware edge from derived asset to input; independent identity only if edge has role/time/scope/evidence/lifecycle. / 从派生产物指向输入的类型化、版本感知边；仅当该边具有角色/时间/Scope/证据/生命周期时才需要独立身份。 | Exact choice OPEN / 精确选择开放 |
| Claim–Evidence Link / Claim–Evidence 关联 | Association record / VALUE_OBJECT / 关联记录或值对象 | Link role can differ per Claim; separate record only when role/strength/time/scope requires it. / 关联角色可能因 Claim 而异；仅当角色/强度/时间/Scope 要求时才单独建记录。 | Candidate / 候选 |
| Relation Qualifier / 关系限定符 | VALUE_OBJECT | Qualifies a Relation; not another Relation. / 用于限定 Relation；不是另一条 Relation。 | Candidate / 候选 |
| Derivation Run / 派生运行 | DEFERRED_CONCEPT pending E / 延后概念，等待 E | Compiler execution identity belongs to E; B only needs derivation lineage record semantics. / Compiler 执行身份归 E 所有；B 只需要定义派生谱系记录语义。 | Do not duplicate E Run ID / 不得重复定义 E 的 Run ID |
| Inference / 推断 | DEFERRED_CONCEPT / process descriptor / 延后概念或过程描述 | Method/result classification, not automatically a persisted domain entity. / 方法/结果分类，不自动成为持久化领域实体。 | OPEN / 开放 |
| Summary / 摘要 | DERIVED_VIEW or Memory kind / 派生视图或 Memory 类型 | No separate entity unless independent lifecycle/identity proven. / 除非证明其具有独立生命周期/身份，否则不单独建实体。 | DEFERRED / 延后 |
| Retrieval Result / Candidate / Ranking / 检索结果、候选项与排序 | DERIVED_VIEW | F-owned query result; transient unless explicit audit requirement. / 由 F 负责的查询结果；除非存在明确审计要求，否则为临时结果。 | DEFERRED as canonical entity / 作为规范实体予以延后 |
| Activation / 激活 | DERIVED_VIEW or domain event / 派生视图或领域事件 | F-owned decision/process; not canonical Memory status. / 由 F 负责的决策/过程；不是规范 Memory 状态。 | OPEN with F / 与 F 协调中 |
| Working Set / 工作集 | DERIVED_VIEW / IMPLEMENTATION_DETAIL | Runtime-local bounded set; not canonical asset. / 运行时局部的有界集合；不是规范资产。 | F-owned / F 负责 |
| Runtime State / 运行时状态 | IMPLEMENTATION_DETAIL / DERIVED_VIEW | Runtime implementation state, not a universal domain entity. / 运行时实现状态，不是通用领域实体。 | F-owned / F 负责 |
| Context Snapshot / ContextVersion / 上下文快照与版本 | CANONICAL_ENTITY or immutable version record / 规范实体或不可变版本记录 | G owns context version; never interchangeable with Memory Version. / G 负责 Context 版本；绝不能与 Memory Version 互换。 | G confirmation required / 需要 G 确认 |
| ChangeSet / 变更集 | CANONICAL_ENTITY candidate / 规范实体候选 | G-owned change intent with identity and reconciliation lifecycle; do not equate to protocol command. / 由 G 负责、具有身份和协调生命周期的变更意图；不得等同于协议命令。 | G confirmation required / 需要 G 确认 |

## 5. Security, protocol and integration concepts / 安全、协议与集成概念

| Concept / 概念 | Classification / 分类 | Boundary / 权威边界 |
|---|---|---|
| Principal / 安全主体 | CANONICAL_ENTITY in Security domain / 安全域规范实体 | I owns authenticated security identity; not the same as domain Entity or User label. / I 负责经过认证的安全身份；不同于领域 Entity 或 User 标签。 |
| Subject / 主体 | DEFERRED / I-owned vocabulary / 延后或 I 所有的词汇 | Must not be used as synonym for Principal until I defines exact meaning. / 在 I 明确定义前，不得将其作为 Principal 的同义词。 |
| Identity / External Identity / 身份与外部身份 | CANONICAL_ENTITY or mapping record in I domain / I 域规范实体或映射记录 | B defines typed references only; issuer/trust/linking policy belongs to I. / B 仅定义类型化引用；issuer/trust/linking 策略归 I。 |
| User / 用户 | DEFERRED as generic universal entity / 通用实体概念延后 | Could be domain subject/person or security Principal; disambiguate by context. / 可能指领域主体/人物，也可能指安全 Principal；必须结合上下文消歧。 |
| Agent / 智能体 | CANONICAL_ENTITY or external actor reference depending on identity scope / 依身份范围确定为规范实体或外部行为者引用 | C/I decide Agent identity vs executing instance. / Agent 身份与执行实例的区分由 C/I 决定。 |
| Agent Instance / Agent 实例 | CANONICAL_ENTITY candidate in integration/security boundary / 集成/安全边界上的规范实体候选 | Distinct runtime instance, not Agent logical identity. / 独立的运行时实例，不是 Agent 的逻辑身份。 |
| Tenant / Workspace / Project / 租户、工作区与项目 | DEFERRED taxonomy / 分类体系延后 | Do not assume synonyms; I/A must define namespace and isolation role. / 不得假定它们是同义词；I/A 必须定义命名空间和隔离角色。 |
| Session / Conversation / 会话与对话 | DEFERRED domain status / 领域状态延后 | C/G own integration/runtime semantics; may be distinct but not established by current core domain schema. / C/G 负责集成/运行时语义；二者可能不同，但当前核心领域 Schema 尚未确立。 |
| Execution / Operation / 执行与操作 | CANONICAL_ENTITY in operation domain or C-owned record / 操作域规范实体或 C 所有记录 | Not interchangeable with Event or Protocol Request. / 不得与 Event 或 Protocol Request 互换。 |
| Protocol Message / Request / Response / Command / 协议消息、请求、响应与命令 | PROTOCOL_OBJECT | H-owned wire objects; may reference but do not become domain entities. / 由 H 负责的 Wire 对象；可以引用领域对象，但自身不因此成为领域实体。 |
| Receipt / Acknowledgement / 回执与确认 | PROTOCOL_OBJECT or evidence record / 协议对象或证据记录 | Receipt proves a declared boundary outcome only; exact authority H/C/G/Storage. / Receipt 仅证明声明的边界结果；具体权威为 H/C/G/Storage。 |
| Provider Outcome / 提供方结果 | CANDIDATE canonical integration outcome record / 规范集成结果记录候选 | C-owned; do not reinterpret as domain Event without explicit mapping. / 由 C 负责；没有明确映射时，不得重新解释为领域 Event。 |
| Policy / Permission / Authorization Decision / 策略、权限与授权决策 | I-owned governance/security objects / I 所有的治理/安全对象 | Not Scope; B cannot decide policy engine. / 不等于 Scope；B 无权决定策略引擎。 |
| Forget Request / Forget Operation / 遗忘请求与遗忘操作 | D/I split / D/I 分工 | Request/authorization governance differs from D canonical ForgetOperation and execution lifecycle. / 请求/授权治理不同于 D 负责的规范 ForgetOperation 及其执行生命周期。 |
| Audit Record / Governance Decision / Legal Hold / 审计记录、治理决策与法律保留 | I-owned governance records / I 所有的治理记录 | Not generic Memory status. / 不是通用 Memory 状态。 |

## 6. Similar names that must not be collapsed / 不得合并的相似概念

- Event ≠ Memory ≠ Claim ≠ Evidence.
  Event、Memory、Claim、Evidence 彼此不同，不得互换。
- Memory ≠ Memory Version; stable asset identity differs from immutable snapshot identity.
  Memory 不等于 Memory Version；稳定资产身份不同于不可变快照身份。
- Entity ≠ Claim subject string; Relation ≠ text co-occurrence.
  Entity 不等于 Claim 的 subject 字符串；Relation 不等于文本共现。
- Source ≠ Evidence ≠ Provenance. Source is origin; Evidence is an evidential object/observation; Provenance is the derivation trace.
  Source、Evidence、Provenance 彼此不同：Source 是来源；Evidence 是证据对象/观察；Provenance 是派生追踪记录。
- Claim epistemic status ≠ Memory lifecycle state.
  Claim 的认知状态不等于 Memory 生命周期状态。
- Scope ≠ Permission; Principal ≠ domain Entity; ActorRef ≠ authentication proof.
  Scope 不等于 Permission；Principal 不等于领域 Entity；ActorRef 不等于身份认证证明。
- Context Version ≠ Memory Version; Context Entry ≠ Memory.
  Context Version 不等于 Memory Version；Context Entry 不等于 Memory。
- Applied ≠ Recorded ≠ Committed ≠ Visible ≠ Published.
  Applied、Recorded、Committed、Visible、Published 是不同状态/结果，不得合并。
- Forget Request ≠ Forget decision ≠ Forget execution ≠ deletion/purge evidence.
  Forget Request、Forget 决策、Forget 执行以及删除/清除证据彼此不同。
- Protocol Request ≠ Operation; ACK ≠ Applied proof.
  Protocol Request 不等于 Operation；ACK 不等于 Applied 证明。

中文对应：Event、Memory、Claim、Evidence 不可互换；Memory 与 Memory Version 分别表示稳定资产和不可变快照；Entity 不等于命题中的文本主体，Relation 不等于文本共现；Source、Evidence、Provenance 分别表示来源、证据对象和派生追溯；Claim 认知状态不等于 Memory 生命周期；Scope 不等于 Permission，Principal 不等于领域 Entity，ActorRef 不构成身份认证证明；Context Version 不等于 Memory Version；Applied、Recorded、Committed、Visible、Published 不得合并；Forget Request、决定、执行和删除/清除证据必须分离；协议 Request 不等于 Operation，ACK 不等于 Applied 证明。

## 7. Inventory questions still open / 清单未决问题

1. Does Claim have stable identity across Memory Versions, or is it a version-local ClaimSnapshot? (B ADR required)
   Claim 是否在不同 Memory Version 之间具有稳定身份，还是仅为版本局部的 ClaimSnapshot？（需要 B ADR）
2. Does Provenance require an independent record ID for every derivation edge, or can a typed edge plus immutable artifact version suffice?
   每条派生边的 Provenance 是否都需要独立记录 ID，还是类型化边加不可变产物版本即可？
3. When does Memory Source need independent identity?
   Memory Source 在什么条件下需要独立身份？
4. Is Context Entry independently addressable and versioned under G?
   Context Entry 是否由 G 负责独立寻址和版本化？
5. What is the canonical Scope taxonomy and namespace hierarchy (User/Tenant/Workspace/Project/Agent/Instance/Task/Session/Environment/System)?
   规范 Scope 分类及命名空间层级是什么（User/Tenant/Workspace/Project/Agent/Instance/Task/Session/Environment/System）？
6. Are Session and Conversation separate domain entities or C/G runtime integration objects?
   Session 与 Conversation 是独立领域实体，还是 C/G 的运行时集成对象？
7. Is Provider Outcome a durable domain record, a C-owned operation outcome, or both via explicit mapping?
   Provider Outcome 是持久领域记录、C 所有的操作结果，还是通过明确映射同时具备两者？
8. Which governance records are shared canonical concepts versus I-owned local model?
   哪些治理记录属于共享规范概念，哪些属于 I 所有的局部模型？
9. Does a Source require a first-class entity separate from Event/Document/External SourceRef?
   Source 是否需要成为独立的一等实体，并与 Event/Document/External SourceRef 区分？
10. Which derived views require durable audit retention without becoming canonical domain entities?
    哪些派生视图需要持久审计保留，但不因此成为规范领域实体？

## 8A. Chinese candidate inventory mirror / 中文候选领域对象清单

| Candidate term / 候选概念 | Classification / 分类 | 中文存在性判断 / 中文理由 |
|---|---|---|
| User | DEFERRED_CONCEPT | 人类用户可能由 I Principal 和 C/G Conversation Actor 表示；在 Owner 分类前不得作为通用身份根。 |
| Agent | CANONICAL_ENTITY or IMPLEMENTATION_DETAIL by context | 逻辑 Agent 可具有稳定身份；Runtime Agent Instance 属于执行细节；必须区分 AgentRef 和 PrincipalRef。 |
| Principal | CANONICAL_ENTITY (I-owned security context) | I 解析的安全主体；不是 Memory 领域实体或 Agent 的同义词。 |
| Subject | VALUE_OBJECT / SECURITY TERM | 必须由 I/具体上下文定义；不得用作 Principal/User/Entity 的通用别名。 |
| Tenant | CANONICAL_SCOPE_CONCEPT, exact type OPEN | 安全隔离边界，必须由 I/A 明确其命名空间和层级。 |
| Workspace | DEFERRED_CONCEPT | 可能是协作空间，但不能假定等于 Tenant 或 Project。 |
| Session | DEFERRED_CONCEPT | 由 C/G/H 明确生命周期和作用域；不得与 Conversation/RuntimeSessionRef 混同。 |
| Conversation | CANONICAL_ENTITY candidate | 交互历史/对话对象，可能具有独立引用和生命周期；需 C/G 确认。 |
| Identity / External Identity | VALUE_OBJECT + mapping association | 外部身份映射必须有 Issuer/Namespace；External ID 不能直接作为 Canonical ID。 |
| ActorRef | VALUE_OBJECT / typed attribution reference | 每次操作不可变的归因引用；不具备认证或授权能力。 |
| Execution | OWNER-LOCAL OPERATION | C/Runtime 执行记录；不是通用 Memory 领域实体。 |
| Memory | CANONICAL_ENTITY | 具有稳定身份、生命周期和可引用内容；由 D 拥有。 |
| Memory Record / Memory Item / Memory Fragment | REJECTED_ABSTRACTION as separate canonical entities | 默认是 Memory/ContentRef 的旧称或表示形式；不创建三套身份/生命周期。 |
| MemoryVersion | CANONICAL_ENTITY | Memory 的不可变版本身份；与 ContextVersion/Checkpoint 分离。 |
| Memory Revision | DEFERRED / VALUE OBJECT | 若仅表示版本则统一为 MemoryVersion；若表示变更操作才考虑独立记录。 |
| Memory Snapshot | DERIVED_VIEW / VERSIONED REPRESENTATION | 需按 Owner 区分 MemoryVersion、ContextVersion、Storage Snapshot 和 Runtime Checkpoint。 |
| Memory Collection / Namespace | DEFERRED_CONCEPT / VALUE_OBJECT | 仅在需要独立访问、生命周期或治理时提升为实体；不能仅因数据库分区而创建。 |
| Claim | CANONICAL_DOMAIN CONCEPT; identity OPEN | 命题对象，认知状态与 Memory Lifecycle 分离；Claim 跨版本身份由 ADR 决定。 |
| Fact | DISTINCT DOMAIN CONCEPT; representation ADR-BLOCKED | I-04 要求概念区分；是否独立对象/类型或限定 Claim 仍未决。 |
| Observation | CANONICAL_DOMAIN CONCEPT / VALUE OBJECT | 带观察者、Observed At 和来源的观察内容；不自动成为已验证 Claim。 |
| Event | CANONICAL_ENTITY | 已捕获的发生/观察/报告/状态变化；不得与 Protocol Event Envelope 混同。 |
| Evidence | CANONICAL_ENTITY | 可独立寻址、支持/反驳/限定 Claim/Relation 的材料；拥有自身可用性和保留语义。 |
| Source / Memory Source | VALUE OBJECT or ASSOCIATION by context | 表示信息来源；MemorySource 默认是类型化关联，不默认是独立 Source Entity。 |
| Provenance | VALUE OBJECT / DERIVATION GRAPH | 记录精确输入、方法、版本和派生关系；是否单独实体取决于生命周期/审计需求。 |
| Derived Memory | CANONICAL_ENTITY candidate | 具有稳定身份的派生知识资产；必须保留来源谱系并受 Forget 传播规则约束。 |
| Derivation | ASSOCIATION / OWNER-LOCAL OPERATION | Source→Target 的有向派生关系；DerivationRun/Attempt 属于 E 工作流，不是通用 B 实体。 |
| Inference / Synthesis / Summary | DERIVED_VIEW unless promoted | 默认是算法/表示结果；只有显式纳入 Memory 并获得生命周期时才成为 Memory 类型。 |
| Entity | CANONICAL_ENTITY | 具有稳定指称身份，不等于任意名词或标签。 |
| Relationship / Relation | CANONICAL_ENTITY | 类型化端点、方向、限定条件、Scope、时间和 Evidence；不是简单共现边。 |
| Assertion / Hypothesis | DEFERRED_CONCEPT / CLAIM SUBTYPE candidate | 若需要区分命题类型，可作为 Claim 的受控分类；不得先建通用实体。 |
| Confidence | VALUE_OBJECT | 带量规/方法/校准条件的估计，不等于 Truth 或 Evidence。 |
| Evidence Link | ASSOCIATION / VALUE OBJECT | Claim–Evidence 关系；若需独立版本/审计再提升为实体。 |
| Context | G-OWNED CANONICAL_ENTITY | 任务范围的期望状态/成员视图，不是第二套规范 Memory。 |
| ContextVersion | G-OWNED CANONICAL_ENTITY | Context 的不可变版本身份；不得与 MemoryVersion 混用。 |
| Context Snapshot | DERIVED_VIEW / G-owned version representation | ContextVersion 的快照语义由 G 拥有；不是 Memory Snapshot。 |
| Context Item / Context Entry | G-OWNED ENTITY or VALUE OBJECT, G decides | ContextVersion 的成员/引用；身份分类由 G Schema 决定。 |
| ChangeSet | G-OWNED OPERATION / CANONICAL CONTEXT OBJECT | 绑定精确 Base/Target Version 和 Digest；不是 BMCP Command。 |
| Working Set | DERIVED_VIEW | F Runtime 局部集合；不是规范 Memory 或 G ContextVersion。 |
| Activation | DERIVED_VIEW / F-OWNED EVENT | 运行时选择/过程，不是 Memory 生命周期状态。 |
| Retrieval Result / Candidate / Ranking | DERIVED_VIEW | 查询相关、可重算，由 F 拥有；不得改变规范身份/状态。 |
| Runtime State | IMPLEMENTATION_DETAIL | F/C/H Runtime 执行状态，不是跨模块规范领域实体。 |
| Protocol Message / Request / Response / Command | PROTOCOL_OBJECT | H Wire 对象；不得因为引用领域对象而成为领域实体。 |
| Event Envelope | PROTOCOL_OBJECT | 传输封装，不等于领域 Event。 |
| Provider Outcome | C-OWNED OPERATION EVIDENCE | 真实 Provider/Runtime Submit 边界证据；不是通用 Event 或 ACK。 |
| Operation | OWNER-OWNED CANONICAL OPERATION | 具有身份/幂等/恢复语义的操作；Owner 定义状态，不使用通用 Status。 |
| Correlation / Idempotency | VALUE OBJECT / PROTOCOL METADATA | 关联/幂等键；不是领域实体，必须绑定命名空间和操作身份。 |
| Receipt / Acknowledgement | OWNER-ISSUED EVIDENCE / PROTOCOL OBJECT | 证明声明的特定后置条件；不得自动证明更下游状态。 |
| Principal Policy / Permission | I-OWNED GOVERNANCE OBJECT or VALUE | 策略/权限属于 I；不能合并到 Domain Entity 的 status。 |
| Authorization Decision | I-OWNED DECISION RECORD | 对精确主体/动作/资源/Scope/Audience 的授权结果。 |
| Consent | I-OWNED GOVERNANCE RECORD | 同意状态独立于授权和 Forget。 |
| Forget Request | GOVERNANCE REQUEST OBJECT | 请求对象，不等于 Forget 决定/操作/结果。 |
| ForgetOperation | D-OWNED OPERATION ENTITY | 持久操作身份、阶段、Fence、Barrier；不等于 Memory 状态。 |
| Audit Record | OWNER-OWNED EVIDENCE | 记录某个可验证行为/决定；不等于业务实体。 |
| Legal Hold / Retention Policy | I-OWNED GOVERNANCE OBJECT | 法律保留和保留策略独立于 Delete/Forget/Purge 状态。 |
| Serialization Anchor / SerializationRevision | IMPLEMENTATION_DETAIL | Storage 物理序列化原语；不是领域实体、Memory Version 或全局时钟。 |

## 9. Gate disposition / 门禁结论

B1 is **IN PROGRESS**. This inventory is a classification proposal grounded in the current main domain source and owner guides. It is not a final entity approval. All Owner-owned classifications remain subject to exact normative contract readback and owner confirmation. No schema is frozen by this inventory.

B1 **进行中**。本清单基于当前 main 领域源规范及 Owner 指南形成分类提案，并非最终实体批准。所有 Owner 所属概念仍需精确读取规范契约并由对应 Owner 确认。本清单不冻结任何 Schema。
