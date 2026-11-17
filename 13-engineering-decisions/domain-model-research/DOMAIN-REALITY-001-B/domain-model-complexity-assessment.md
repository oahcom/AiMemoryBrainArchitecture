# Domain Model Complexity Assessment
# 领域模型复杂度评估

- ID: B-COMP-001
- Status: FIRST-PASS ASSESSMENT — CANDIDATE CLASSIFICATION
- Baseline: main @ b372b62c640a2b656e54b6db62a4ee67d7d8c001
- Method: assess necessity, independent identity, lifecycle, reference value, semantic distinction, implementation cost and future optionality; do not reduce to a numeric score.

## 1. Overall finding / 总体判断

The current model is conceptually rich and covers real requirements (identity, evidence, temporal claims, version history, scope, provenance, Context and Forget). It is not yet sufficiently minimized or semantically closed: some concepts are repeated across Owner-local models, some are only candidates, and a few status labels overstate approval. The main risk is not simply “too many entities”; it is premature identity/lifecycle assignment and duplicated authority across modules.

当前模型概念丰富，覆盖了真实需求（身份、证据、时间化 Claim、版本历史、Scope、Provenance、Context 和 Forget），但尚未完成最小化和语义闭合：部分概念在 Owner 局部模型中重复，有些仍是候选，少数状态标签夸大了批准程度。主要风险不只是“实体太多”，而是过早赋予独立身份/生命周期，以及模块间重复维护同一权威。

## 2. Assessment dimensions / 评估维度

Each concept is assessed qualitatively:
- Domain Necessity: essential to answer a real domain question? / **领域必要性：** 是否为回答真实领域问题所必需？
- Independent Identity: must it be referenced independently over time? / **独立身份：** 是否需要在时间维度上被独立引用？
- Lifecycle Necessity: does it have distinct allowed/forbidden transitions? / **生命周期必要性：** 是否具有独立的允许/禁止状态转换？
- Referential Value: do other objects need to refer to it? / **引用价值：** 其他对象是否需要引用它？
- Semantic Distinction: would merging lose meaning/invariants? / **语义差异：** 合并是否会丢失含义或不变量？
- Implementation Cost: identity registry, persistence, indexes, migration, authorization and tests. / **实现成本：** 身份注册表、持久化、索引、迁移、授权和测试成本。
- Future Optionality: is it justified only by a speculative future use? / **未来可选性：** 是否仅由推测性的未来用途支撑？

## 3. Keep as canonical entities / 保留为规范实体

| Concept | Necessity | Identity / lifecycle | Cost | Decision |
|---|---|---|---|---|
| Event | High | Stable captured occurrence/source record; immutable accepted evidence | Medium | CANONICAL_ENTITY |
| Memory | Essential | Stable ID; lifecycle owned by D | High but foundational | CANONICAL_ENTITY |
| MemoryVersion | Essential | Immutable version identity; monotonic history | Medium-high | CANONICAL_ENTITY |
| Claim | Essential concept | Proposition and epistemic state; identity policy OPEN | High due ADR/schema | CANONICAL_ENTITY concept; identity CANDIDATE/OPEN |
| Entity | High | Stable referent identity; merge/split lineage | Medium-high | CANONICAL_ENTITY |
| Relation | High | Typed endpoints, direction, scope, validity, evidence | Medium-high | CANONICAL_ENTITY |
| Evidence | Essential | Independently addressable and separately authorized/retained | Medium-high | CANONICAL_ENTITY |
| Context | High | G-owned desired state, scoped and task-bound | High; not canonical Memory | CANONICAL_ENTITY in G context |
| ContextVersion | High | Immutable G version identity | Medium-high | CANONICAL_ENTITY in G context |
| ForgetOperation | Essential | Durable operation identity, phases, fence and barrier | High but mandatory safety concept | D-owned operation entity, not Memory child |

## 3A. 中文规范实体保留评估

| 概念 | 必要性 | 身份/生命周期 | 成本 | 分类 |
|---|---|---|---|---|
| Event | 高 | 稳定捕获发生/来源记录；已接受证据不可变 | 中 | CANONICAL_ENTITY |
| Memory | 必需 | 稳定 ID；生命周期由 D 拥有 | 高，但属于基础能力 | CANONICAL_ENTITY |
| MemoryVersion | 必需 | 不可变版本身份；历史单调递增 | 中高 | CANONICAL_ENTITY |
| Claim | 必需概念 | 命题及认知状态；身份策略 OPEN | 因 ADR/Schema 成本高 | CANONICAL_ENTITY 概念；身份 CANDIDATE/OPEN |
| Entity | 高 | 稳定指称身份；合并/拆分需保留谱系 | 中高 | CANONICAL_ENTITY |
| Relation | 高 | 类型化端点、方向、Scope、有效时间和 Evidence | 中高 | CANONICAL_ENTITY |
| Evidence | 必需 | 可独立寻址，并单独授权/保留 | 中高 | CANONICAL_ENTITY |
| Context | 高 | G 拥有的期望状态，受 Scope 和任务约束 | 高；不是规范 Memory | G Context 中的 CANONICAL_ENTITY |
| ContextVersion | 高 | G 拥有的不可变版本身份 | 中高 | G Context 中的 CANONICAL_ENTITY |
| ForgetOperation | 必需 | 持久操作身份、阶段、Fence 和 Barrier | 高，但属于必要安全概念 | D 拥有的操作实体，不是 Memory 子对象 |

## 4. Use value objects / 值对象化

| Concept | Why not separate entity by default | Promote only if |
|---|---|---|
| OpaqueId | Identifier value only; no lifecycle | Never; the identified object is the entity |
| TypedObjectRef / ActorRef / ScopeRef / EnvironmentRef | Typed reference and namespace semantics | Reference itself gains independent lifecycle/authority (not currently shown) |
| TimeInterval / TimeValue | Describes a time assertion | Independent revision/audit identity is required |
| ConfidenceValue | Method-qualified estimate | Separate assessment record must be independently audited |
| Locator / Digest / ContentRef | Address/integrity values | External artifact itself has independent identity |
| Claim–Evidence role link | Relationship qualifier | Link strength/time/authority needs independent version and audit |
| AliasRecord | Label plus time/scope qualifiers | Alias registry requires independent lifecycle/authority |
| ScopeBindingSet | Operation-bound set of role-labelled scope refs | It becomes a separately governed policy object |

## 4A. 中文值对象分类

| 概念 | 默认不作为独立实体的原因 | 仅在何种条件下提升 |
|---|---|---|
| OpaqueId | 只是标识符值，本身没有生命周期。 | 不提升；真正实体是被标识的对象。 |
| TypedObjectRef / ActorRef / ScopeRef / EnvironmentRef | 表达类型化引用和命名空间语义。 | 引用自身获得独立生命周期/权威（当前没有证据）。 |
| TimeInterval / TimeValue | 描述时间断言。 | 需要独立修订/审计身份。 |
| ConfidenceValue | 带方法限定的估计值。 | 评估记录必须独立审计。 |
| Locator / Digest / ContentRef | 表达地址/完整性值。 | 外部产物本身具有独立身份。 |
| Claim–Evidence role link | 关系限定符。 | 链接强度/时间/权威需要独立版本和审计。 |
| AliasRecord | 带时间/Scope 限定的标签。 | Alias Registry 需要独立生命周期/权威。 |
| ScopeBindingSet | 操作绑定的一组带角色 Scope 引用。 | 成为独立治理的策略对象。 |

## 5. Keep as derived views or owner-local execution objects / 派生视图与 Owner 局部执行对象

| Concept | Classification | Reason |
|---|---|---|
| Retrieval Result / Candidate / Ranking | DERIVED_VIEW | Query-specific, recomputable; F-owned |
| Working Set | DERIVED_VIEW | Runtime-local selected refs, not canonical Memory or G ContextVersion |
| Activation | DERIVED_VIEW or F-owned event | Runtime selection/process; not a universal Memory state |
| Index / Embedding / Graph Projection | IMPLEMENTATION_DETAIL / DERIVED_VIEW | Rebuildable representation of canonical assets |
| Summary | DERIVED_VIEW or Memory kind | Do not create standalone entity without independent identity/lifecycle |
| Runtime State | IMPLEMENTATION_DETAIL | F/C/H runtime execution state |
| Reconciliation Run | Owner-local operation record | Run outcome scoped to declared watermark; not Context state |
| DerivationRun / Attempt / Lease | E-owned operation entities | Needed for retry/recovery but not B universal domain entity |
| DeliveryAttempt | G/H protocol/context operation record | Attempt identity belongs to delivery workflow, not Context/Memory |
| Applied record | G-owned immutable evidence record | Per exact request/region/session; distinct from Memory lifecycle |
| ProviderOutcome / CSubmitOutcome | C-owned operation evidence | Actual external side-effect boundary; do not duplicate as generic Event |
| PublicationReceipt | Storage-owned evidence record | Proves exact visibility commit; not a domain Memory entity |

## 5A. 中文派生视图与 Owner 局部执行对象分类

| 概念 | 分类 | 原因 |
|---|---|---|
| Retrieval Result / Candidate / Ranking | DERIVED_VIEW | 查询特定、可重算，由 F 拥有。 |
| Working Set | DERIVED_VIEW | Runtime 局部选定引用；不是规范 Memory 或 G ContextVersion。 |
| Activation | DERIVED_VIEW 或 F-owned event | Runtime 选择/过程，不是通用 Memory 状态。 |
| Index / Embedding / Graph Projection | IMPLEMENTATION_DETAIL / DERIVED_VIEW | 规范资产的可重建表示。 |
| Summary | DERIVED_VIEW 或 Memory kind | 无独立身份/生命周期证明时，不创建独立实体。 |
| Runtime State | IMPLEMENTATION_DETAIL | F/C/H Runtime 执行状态。 |
| Reconciliation Run | Owner 局部操作记录 | 结果受声明的 Watermark 限定；不是 Context 状态。 |
| DerivationRun / Attempt / Lease | E-owned operation entities | 支持重试/恢复，但不是 B 的通用领域实体。 |
| DeliveryAttempt | G/H Protocol/Context 操作记录 | Attempt 身份属于 Delivery Workflow，不属于 Context/Memory。 |
| Applied record | G-owned immutable evidence record | 绑定精确请求/区域/会话；与 Memory 生命周期不同。 |
| ProviderOutcome / CSubmitOutcome | C-owned operation evidence | 真实外部副作用边界证据；不得重复建模为通用 Event。 |
| PublicationReceipt | Storage-owned evidence record | 证明精确可见性提交；不是 Memory 领域实体。 |

## 6. Merge, defer or reject / 合并、延后或拒绝

| Concepts | Recommendation | Semantic consequence |
|---|---|---|
| Memory Record / Memory Item / Memory Fragment | Merge as non-canonical synonyms or representation kinds under Memory/ContentRef; DEFER standalone entities | Avoids three parallel identity/lifecycle schemes |
| Fact / Claim | Do NOT merge yet; preserve ADR-BLOCKED | Must decide whether Fact is a claim subtype/qualified epistemic result or distinct entity before schema |
| Observation / Event / Evidence | Do NOT collapse: Event is captured occurrence/report, Observation is observation content/time, Evidence is supporting material | A single captured observation may produce an Event and Evidence link; exact model depends on source |
| Source / Evidence / Provenance | Keep distinct; Source may remain a typed origin ref/association | Prevents source identity, support material and derivation history from collapsing |
| Memory Revision / Memory Version | Prefer one canonical MemoryVersion concept; use Revision only if it means a different operation/change record | Avoid synonym inflation; validate with D |
| Snapshot / Version | Keep owner-scoped: MemoryVersion, ContextVersion, Storage snapshot and runtime checkpoint are different | Prevents cross-domain version alias |
| User / Principal / Subject / Actor | Keep typed distinctions; User is ambiguous universal noun | I owns security subject; B typed refs; C/G runtime actors |
| Tenant / Workspace / Project / Scope | Do not synonymize; defer taxonomy | I/A must establish isolation and namespace rules |
| Session / Conversation / RuntimeSessionRef | Keep distinct until C/G/H confirm relation | Avoids ID and lifecycle ambiguity |
| Protocol Request / Operation / Event Envelope / Receipt | Protocol objects remain distinct from domain operation and evidence | H wire contract cannot define domain truth |
| Delete / Forget / Purge | Never merge | Logical deletion, governed suppression and physical erasure have different owners/proofs |

## 6A. 中文合并、延后或拒绝评估

| 概念 | 建议 | 语义后果 |
|---|---|---|
| Memory Record / Memory Item / Memory Fragment | 作为非规范同义词或 Memory/ContentRef 下的表示类型合并；独立实体 DEFER。 | 避免三套并行身份/生命周期方案。 |
| Fact / Claim | 目前不得合并；保留 ADR-BLOCKED。 | Schema 前必须决定 Fact 是 Claim 子类型/限定认知结果，还是不同实体。 |
| Observation / Event / Evidence | 不得折叠：Event 是捕获的发生/报告；Observation 是观察内容/时间；Evidence 是支持材料。 | 一次 Observation 可产生 Event 和 Evidence 链接；精确模型依来源而定。 |
| Source / Evidence / Provenance | 保持区分；Source 可保留为类型化来源引用/关联。 | 防止来源身份、支持材料和派生历史混为一谈。 |
| Memory Revision / Memory Version | 优先统一为 MemoryVersion；只有 Revision 表示不同操作/变更记录时才保留。 | 避免同义概念膨胀；需 D 验证。 |
| Snapshot / Version | 按 Owner 区分 MemoryVersion、ContextVersion、Storage Snapshot 和 Runtime Checkpoint。 | 防止跨域版本别名。 |
| User / Principal / Subject / Actor | 保持类型区分；User 是含义模糊的通用词。 | I 拥有安全主体；B 定义类型化引用；C/G 定义 Runtime Actor。 |
| Tenant / Workspace / Project / Scope | 不得视为同义词；分类延后。 | I/A 必须建立隔离和命名空间规则。 |
| Session / Conversation / RuntimeSessionRef | 在 C/G/H 确认关系前保持区分。 | 避免身份和生命周期歧义。 |
| Protocol Request / Operation / Event Envelope / Receipt | Protocol 对象与领域 Operation/Evidence 保持区分。 | H Wire 契约不能定义领域真值。 |
| Delete / Forget / Purge | 永不合并。 | 逻辑删除、治理抑制和物理擦除具有不同 Owner/证明。 |

## 7. DDD and aggregate complexity / DDD 与聚合复杂度

Do not assign an aggregate root based on a table or folder. An aggregate is justified only when a set of invariants must be committed atomically under one owner boundary. Current candidates:
- D: Memory + version/current pointer; ForgetOperation + fence/barrier ledger.
- G: Context + ContextVersion/ChangeSet, and separate Delivery/Applied records.
- E: CompileIntent/WorkItem/DerivationRun/Attempt as E-owned workflow state.
- I: Principal/trust/authorization policy records.
- Storage: publication participant and receipt transaction boundary.

These are candidates for owner-side transaction analysis, not a B mandate. Cross-owner atomicity must be handled by explicit causal/receipt protocols, not a giant aggregate spanning modules.

不要根据数据库表或目录来分配聚合根。只有当一组不变量必须在单一 Owner 边界内原子提交时，聚合才成立。上列均为 Owner 侧事务分析候选，不是 B 的强制决定。跨 Owner 原子性必须通过明确因果/Receipt 协议处理，而不是建立横跨模块的巨型聚合。

### 中文 DDD 聚合复杂度说明

不得根据数据库表或文件夹分配 Aggregate Root。只有当一组不变量必须在单一 Owner 边界内原子提交时，聚合才成立。当前候选包括：
- D：Memory + Version/Current Pointer；ForgetOperation + Fence/Barrier Ledger。
- G：Context + ContextVersion/ChangeSet；以及独立 Delivery/Applied 记录。
- E：CompileIntent/WorkItem/DerivationRun/Attempt 等 E-owned Workflow State。
- I：Principal/Trust/Authorization Policy 记录。
- Storage：Publication Participant 和 Receipt 事务边界。

这些仅是 Owner 侧事务分析候选，不是 B 的强制命令。跨 Owner 原子性必须通过显式 Causal/Receipt 协议处理，不得建立横跨模块的巨型 Aggregate。

## 8. Complexity risks and mitigations / 复杂度风险与缓解

| Risk | Impact | Mitigation |
|---|---|---|
| Too many first-class IDs | Registry, joins, authorization, migration, test burden | Require independent identity/lifecycle proof before promotion |
| One universal status enum | Semantic corruption and unsafe transitions | Typed state machines by subject/owner |
| Universal Event Sourcing | Replay, migration, external side effects, retention/Forget cost | State + immutable versions + targeted ledgers |
| Universal bitemporal fields | Storage/index/query explosion | Selective bitemporal Claims/Relations |
| Full ontology / RDF/OWL too early | Formal reasoning, mapping and governance cost | Typed relations first; ontology deferred |
| Graph DB as canonical truth | Dual write, consistency and Forget complexity | Canonical relational model + derived graph projection |
| Duplicate Owner models | Conflicting definitions and approval ambiguity | Shared vocabulary + Owner-local bounded models + exact-version registry |
| Cross-tenant implicit inheritance | Security leakage | Explicit namespace and per-reference authorization |
| Unverifiable provenance metadata | False audit guarantees | Mark unavailable; only require obtainable/verified evidence |

## 8A. 中文复杂度风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| 一等身份 ID 过多 | Registry、Join、授权、迁移和测试负担上升。 | 只有证明独立身份/生命周期必要后才提升为实体。 |
| 通用 Status Enum | 语义损坏和不安全转换。 | 按对象和 Owner 使用类型化状态机。 |
| 全系统 Event Sourcing | Replay、迁移、外部副作用、保留/Forget 成本增加。 | 使用状态 + 不可变版本 + 有针对性的操作账本。 |
| 所有对象都使用双时态字段 | Storage/Index/Query 复杂度膨胀。 | 对 Claim/Relation 选择性使用双时态。 |
| 过早引入完整 Ontology/RDF/OWL | 形式化推理、映射和治理成本高。 | 先采用类型化 Relation；Ontology 延后。 |
| Graph DB 作为规范真值 | 双写、一致性和 Forget 复杂度增加。 | 关系型规范模型 + 派生图投影。 |
| Owner 模型重复 | 定义冲突和批准权威不清。 | 共享词汇 + Owner 局部有界模型 + 精确版本 Registry。 |
| 隐式跨 Tenant 继承 | 安全泄漏。 | 显式命名空间和逐引用授权。 |
| 无法验证的 Provenance Metadata | 产生虚假的审计保证。 | 标记不可用；只要求可获得/可验证的信息。 |

## 9. Physical serialization anchor classification / 物理序列化锚点分类

The per-authority Storage serialization anchor and its nominal references are IMPLEMENTATION_DETAIL, not CANONICAL_ENTITY. B's Phase 3.8.6 review approves the type boundary only; it does not make SerializationRevision a domain clock or introduce a global counter. The anchor adds physical consistency complexity and must remain under Storage authority. E/F accept with conditions; Storage v3.2.11 remains not jointly accepted/frozen and needs fresh A review plus L4 DB/HA/recovery proof.

每 Authority Storage Serialization Anchor 及其名义引用属于 IMPLEMENTATION_DETAIL，而非 CANONICAL_ENTITY。B Phase 3.8.6 复审仅批准类型边界；不将 SerializationRevision 变成领域时钟，也不引入全局计数器。Anchor 增加物理一致性复杂度，必须归 Storage 权威。E/F 有条件接受；Storage v3.2.11 仍未联合接受/冻结，需要 A 新复审和 L4 DB/HA/恢复证据。

## 10. Minimum and recommended models / 最小模型与推荐模型

### Minimum canonical model
- Event
- Memory + immutable MemoryVersion
- Claim proposition with explicit epistemic status (identity ADR unresolved)
- Entity + typed Relation
- Evidence + SourceRef + Provenance lineage
- Typed Scope/Actor/Environment references
- Context + ContextVersion + ContextEntry as G-owned boundary
- Owner-specific ForgetOperation/ForgetFence and operation/evidence records
- Explicit temporal values and Valid/Record time where applicable

### Recommended canonical model
Minimum model plus:
- Claim–Evidence link assessment with role and method-qualified strength;
- selective bitemporal support for time-qualified Claims/Relations;
- explicit Source/Derived lineage graph with provenance method/input version;
- typed per-request Applied and current-use projection (G-owned);
- typed Operation/ProtocolMessage/Receipt separation;
- explicit identity registry references and issuer/namespace dimensions.

### Deferred concepts
- formal RDF/OWL ontology and reasoning;
- universal event store;
- universal aggregate framework;
- full graph database as canonical store;
- standalone Summary, Inference, Hypothesis, Source or DerivationRun domain entities without independent lifecycle proof;
- universal Session/Conversation model until C/G/H agreement.

### Rejected abstractions
- universal BaseEntity/BaseMemoryRecord hierarchy without behavior/invariant;
- universal Status enum;
- untyped universal Actor/User/ID;
- one Timestamp field for all temporal concepts;
- single Fact/Claim entity declaration while ADR remains blocked;
- MemoryVersion = ContextVersion = checkpoint;
- Applied = Delivered/ACK/Recorded;
- Forgotten = Deleted = Purged.

## 10A. 中文最小、推荐、延后与拒绝模型

### 最小规范模型
- Event；
- Memory + 不可变 MemoryVersion；
- 带明确认知状态的 Claim 命题（身份 ADR 未决）；
- Entity + 类型化 Relation；
- Evidence + SourceRef + Provenance 谱系；
- 类型化 Scope/Actor/Environment 引用；
- 作为 G 所有权边界的 Context + ContextVersion + ContextEntry；
- Owner 专属 ForgetOperation/ForgetFence 及操作/证据记录；
- 在适用处明确的时间值及 Valid/Record Time。

### 推荐规范模型
在最小模型上增加：
- 带角色和方法限定强度的 Claim–Evidence Link Assessment；
- 对时间限定 Claim/Relation 及 Revision 选择性支持双时态；
- 显式 Source/Derived 谱系图，记录 Provenance 方法和输入版本；
- G 拥有的、按请求类型化 Applied 历史记录及独立当前使用投影；
- 类型化 Operation/ProtocolMessage/Receipt 区分；
- 显式 Identity Registry 引用及 Issuer/Namespace 维度。

### 延后概念
- 正式 RDF/OWL Ontology 和推理；
- 全局 Event Store；
- 通用 Aggregate Framework；
- 作为规范存储的完整 Graph Database；
- 未证明独立身份/生命周期的独立 Summary、Inference、Hypothesis、Source 或 DerivationRun 领域实体；
- 在 C/G/H 达成一致前的通用 Session/Conversation 模型。

### 拒绝的抽象
- 没有行为/不变量支撑的通用 BaseEntity/BaseMemoryRecord 层级；
- 通用 Status Enum；
- 无类型的通用 Actor/User/ID；
- 所有时间概念共用一个 Timestamp；
- ADR 仍阻塞时将 Fact/Claim 宣布为单一实体；
- MemoryVersion = ContextVersion = Checkpoint；
- Applied = Delivered/ACK/Recorded；
- Forgotten = Deleted = Purged。

## 11. Gate status / 门禁状态

B1 is IN PROGRESS. The assessment identifies a minimum and recommended candidate model but does not finalize Fact/Claim, Claim identity, aggregate boundaries or Owner-local schemas. No implementation cost estimates or performance measurements were run; complexity comparisons are qualitative.

B1 进行中。本评估识别了最小和推荐候选模型，但未最终决定 Fact/Claim、Claim 身份、聚合边界或 Owner 局部 Schema。未执行实现成本估算或性能测量；复杂度比较为定性判断。


## 12. Full Chinese semantic mirror / 完整中文语义对照

### 12.1 评估维度补充

每个概念均采用定性方式评估，不压缩为单一数值分数：
- **Domain Necessity（领域必要性）**：是否为回答真实领域问题所必需。
- **Independent Identity（独立身份）**：是否必须在时间维度上被独立引用。
- **Lifecycle Necessity（生命周期必要性）**：是否具有独立的允许/禁止状态转换。
- **Referential Value（引用价值）**：其他对象是否需要引用该概念。
- **Semantic Distinction（语义差异）**：合并是否会丢失含义或不变量。
- **Implementation Cost（实现成本）**：身份注册表、持久化、索引、迁移、授权和测试的成本。
- **Future Optionality（未来可选性）**：该概念是否仅由推测性的未来用途支撑。

### 12.2 保留为规范实体

| 概念 | 必要性 | 身份/生命周期 | 成本 | 决策 |
|---|---|---|---|---|
| Event | 高 | 稳定的捕获发生/来源记录；已接受证据不可变 | 中 | CANONICAL_ENTITY |
| Memory | 必需 | 稳定 ID；生命周期由 D 负责 | 高，但属于基础能力 | CANONICAL_ENTITY |
| MemoryVersion | 必需 | 不可变版本身份；历史单调递增 | 中高 | CANONICAL_ENTITY |
| Claim | 必需概念 | 命题及认知状态；身份策略 OPEN | 因 ADR/Schema 而高 | CANONICAL_ENTITY 概念；身份 CANDIDATE/OPEN |
| Entity | 高 | 稳定指称身份；合并/拆分谱系 | 中高 | CANONICAL_ENTITY |
| Relation | 高 | 类型化端点、方向、Scope、有效性和 Evidence | 中高 | CANONICAL_ENTITY |
| Evidence | 必需 | 可独立寻址并单独授权/保留 | 中高 | CANONICAL_ENTITY |
| Context | 高 | G 负责的期望状态，受 Scope 和任务约束 | 高；不是规范 Memory | G Context 中的 CANONICAL_ENTITY |
| ContextVersion | 高 | G 负责的不可变版本身份 | 中高 | G Context 中的 CANONICAL_ENTITY |
| ForgetOperation | 必需 | 持久操作身份、阶段、Fence 和 Barrier | 高，但属于强制安全概念 | D 负责的操作实体，不是 Memory 子对象 |

### 12.3 值对象化

| 概念 | 默认不作为独立实体的原因 | 仅在何种条件下提升 |
|---|---|---|
| OpaqueId | 仅为标识符值，本身没有生命周期。 | 不提升；被标识的对象才是实体。 |
| TypedObjectRef / ActorRef / ScopeRef / EnvironmentRef | 表达类型化引用和命名空间语义。 | 引用本身获得独立生命周期/权威（当前没有证据）。 |
| TimeInterval / TimeValue | 描述时间断言。 | 需要独立修订/审计身份。 |
| ConfidenceValue | 带方法限定的估计值。 | 独立评估记录必须接受审计。 |
| Locator / Digest / ContentRef | 地址/完整性值。 | 外部产物本身具有独立身份。 |
| Claim–Evidence role link | 关系限定符。 | 链接强度/时间/权威需要独立版本和审计。 |
| AliasRecord | 带时间/Scope 限定的标签。 | Alias Registry 需要独立生命周期/权威。 |
| ScopeBindingSet | 操作绑定的一组带角色 Scope 引用。 | 其成为独立治理的策略对象。 |

### 12.4 派生视图与 Owner 局部执行对象

| 概念 | 分类 | 原因 |
|---|---|---|
| Retrieval Result / Candidate / Ranking | DERIVED_VIEW | 查询特定、可重算，由 F 负责。 |
| Working Set | DERIVED_VIEW | Runtime 局部选定引用；不是规范 Memory 或 G ContextVersion。 |
| Activation | DERIVED_VIEW 或 F-owned event | Runtime 选择/过程；不是通用 Memory 状态。 |
| Index / Embedding / Graph Projection | IMPLEMENTATION_DETAIL / DERIVED_VIEW | 规范资产的可重建表示。 |
| Summary | DERIVED_VIEW 或 Memory kind | 无独立身份/生命周期证明时，不创建独立实体。 |
| Runtime State | IMPLEMENTATION_DETAIL | F/C/H Runtime 执行状态。 |
| Reconciliation Run | Owner 局部操作记录 | Run 结果受声明的 Watermark 限定；不是 Context 状态。 |
| DerivationRun / Attempt / Lease | E-owned operation entities | 支持重试/恢复，但不是 B 的通用领域实体。 |
| DeliveryAttempt | G/H Protocol/Context 操作记录 | Attempt 身份属于 Delivery Workflow，不属于 Context/Memory。 |
| Applied record | G-owned immutable evidence record | 绑定精确请求/区域/会话；与 Memory 生命周期不同。 |
| ProviderOutcome / CSubmitOutcome | C-owned operation evidence | 真实外部副作用边界证据；不得重复建模为通用 Event。 |
| PublicationReceipt | Storage-owned evidence record | 证明精确可见性提交；不是 Memory 领域实体。 |

### 12.5 合并、延后或拒绝

| 概念 | 建议 | 语义后果 |
|---|---|---|
| Memory Record / Memory Item / Memory Fragment | 作为非规范同义词或 Memory/ContentRef 下的表示类型合并；独立实体 DEFER。 | 避免三套并行身份/生命周期方案。 |
| Fact / Claim | 目前不得合并；保留 ADR-BLOCKED。 | Schema 前必须决定 Fact 是 Claim 子类型/限定认知结果，还是不同实体。 |
| Observation / Event / Evidence | 不得折叠：Event 是捕获的发生/报告；Observation 是观察内容/时间；Evidence 是支持材料。 | 一次捕获的 Observation 可产生 Event 和 Evidence 链接；精确模型依来源而定。 |
| Source / Evidence / Provenance | 保持区分；Source 可保留为类型化来源引用/关联。 | 防止来源身份、支持材料和派生历史混为一谈。 |
| Memory Revision / Memory Version | 优先统一为 MemoryVersion；仅当 Revision 表示不同操作/变更记录时才保留。 | 避免同义概念膨胀；需 D 验证。 |
| Snapshot / Version | 按 Owner 区分 MemoryVersion、ContextVersion、Storage Snapshot 和 Runtime Checkpoint。 | 防止跨域版本别名。 |
| User / Principal / Subject / Actor | 保持类型区分；User 是含义模糊的通用词。 | I 负责安全 Subject；B 定义类型化引用；C/G 负责 Runtime Actor。 |
| Tenant / Workspace / Project / Scope | 不得视为同义词；分类延后。 | I/A 必须建立隔离和命名空间规则。 |
| Session / Conversation / RuntimeSessionRef | 在 C/G/H 确认关系前保持区分。 | 避免 ID 和生命周期歧义。 |
| Protocol Request / Operation / Event Envelope / Receipt | Protocol 对象与领域 Operation/Evidence 保持区分。 | H Wire 契约不能定义领域真值。 |
| Delete / Forget / Purge | 永不合并。 | 逻辑删除、治理抑制和物理擦除具有不同 Owner/证明。 |

### 12.6 DDD 与 Aggregate 复杂度

不得根据数据库表或目录分配 Aggregate Root。只有当一组不变量必须在单一 Owner 边界内原子提交时，Aggregate 才有成立依据。当前候选：
- D：Memory + Version/Current Pointer；ForgetOperation + Fence/Barrier Ledger。
- G：Context + ContextVersion/ChangeSet；以及独立 Delivery/Applied 记录。
- E：CompileIntent/WorkItem/DerivationRun/Attempt 等 E-owned Workflow State。
- I：Principal/Trust/Authorization Policy 记录。
- Storage：Publication Participant 和 Receipt 事务边界。

这些是 Owner 侧事务分析候选，不是 B 的强制命令。跨 Owner 原子性必须通过显式 Causal/Receipt 协议处理，不得建立横跨模块的巨型 Aggregate。

### 12.7 复杂度风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| 一等身份 ID 过多 | Registry、Join、授权、迁移和测试负担上升。 | 只有证明独立身份/生命周期必要后才提升为实体。 |
| 通用 Status Enum | 语义损坏和不安全转换。 | 按对象和 Owner 使用类型化状态机。 |
| 全系统 Event Sourcing | Replay、迁移、外部副作用、保留/Forget 成本增加。 | 使用状态 + 不可变版本 + 有针对性的操作账本。 |
| 所有对象都使用双时态字段 | Storage/Index/Query 复杂度膨胀。 | 对 Claim/Relation 选择性使用双时态。 |
| 过早引入完整 Ontology/RDF/OWL | 形式化推理、映射和治理成本高。 | 先采用类型化 Relation；Ontology 延后。 |
| Graph DB 作为规范真值 | 双写、一致性和 Forget 复杂度增加。 | 关系型规范模型 + 派生图投影。 |
| Owner 模型重复 | 定义冲突和批准权威不清。 | 共享词汇 + Owner 局部有界模型 + 精确版本 Registry。 |
| 隐式跨 Tenant 继承 | 安全泄漏。 | 显式命名空间和逐引用授权。 |
| 无法验证的 Provenance Metadata | 产生虚假的审计保证。 | 标记不可用；只要求可获得/可验证的信息。 |

### 12.8 物理序列化锚点分类

每 Authority Storage Serialization Anchor 及其名义引用属于 IMPLEMENTATION_DETAIL，而非 CANONICAL_ENTITY。B 的 Phase 3.8.6 复审仅批准类型边界；不将 SerializationRevision 变成领域时钟，也不引入全局计数器。该 Anchor 增加物理一致性复杂度，必须归 Storage 权威。E/F 有条件接受；Storage v3.2.11 仍未联合接受/冻结，需要 A 新复审以及 L4 DB/HA/恢复证据。

### 12.9 最小、推荐、延后与拒绝模型

**最小规范模型：**
- Event；
- Memory + 不可变 MemoryVersion；
- 带明确认知状态的 Claim 命题（身份 ADR 未决）；
- Entity + 类型化 Relation；
- Evidence + SourceRef + Provenance 谱系；
- 类型化 Scope/Actor/Environment 引用；
- 作为 G 所有权边界的 Context + ContextVersion + ContextEntry；
- Owner 专属 ForgetOperation/ForgetFence 及操作/证据记录；
- 在适用处明确的时间值及 Valid/Record Time。

**推荐规范模型：** 在最小模型上增加 Claim–Evidence Link Assessment（带角色和方法限定强度）；对时间限定 Claim/Relation 选择性支持双时态；显式 Source/Derived 谱系图及 Provenance 方法/输入版本；G 拥有的按请求类型化 Applied 历史记录及独立当前使用投影；类型化 Operation/ProtocolMessage/Receipt 区分；显式 Identity Registry 引用及 Issuer/Namespace 维度。

**延后概念：** 正式 RDF/OWL Ontology 和推理；全局 Event Store；通用 Aggregate Framework；作为规范存储的完整 Graph Database；未证明独立生命周期的独立 Summary、Inference、Hypothesis、Source 或 DerivationRun 领域实体；在 C/G/H 达成一致前的通用 Session/Conversation 模型。

**拒绝的抽象：** 没有行为/不变量支撑的通用 BaseEntity/BaseMemoryRecord 层级；通用 Status Enum；无类型的通用 Actor/User/ID；所有时间概念共用一个 Timestamp；ADR 仍阻塞时将 Fact/Claim 宣布为单一实体；MemoryVersion = ContextVersion = Checkpoint；Applied = Delivered/ACK/Recorded；Forgotten = Deleted = Purged。

### 12.10 门禁结论

B1 仍为 IN PROGRESS。本评估识别了最小和推荐候选模型，但未最终决定 Fact/Claim、Claim 身份、Aggregate 边界或 Owner 局部 Schema。未执行实现成本估算或性能测量；复杂度比较均为定性判断。
