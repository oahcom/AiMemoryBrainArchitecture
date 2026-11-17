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
- Domain Necessity: essential to answer a real domain question?
- Independent Identity: must it be referenced independently over time?
- Lifecycle Necessity: does it have distinct allowed/forbidden transitions?
- Referential Value: do other objects need to refer to it?
- Semantic Distinction: would merging lose meaning/invariants?
- Implementation Cost: identity registry, persistence, indexes, migration, authorization and tests.
- Future Optionality: is it justified only by a speculative future use?

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

## 7. DDD and aggregate complexity / DDD 与聚合复杂度

Do not assign an aggregate root based on a table or folder. An aggregate is justified only when a set of invariants must be committed atomically under one owner boundary. Current candidates:
- D: Memory + version/current pointer; ForgetOperation + fence/barrier ledger.
- G: Context + ContextVersion/ChangeSet, and separate Delivery/Applied records.
- E: CompileIntent/WorkItem/DerivationRun/Attempt as E-owned workflow state.
- I: Principal/trust/authorization policy records.
- Storage: publication participant and receipt transaction boundary.

These are candidates for owner-side transaction analysis, not a B mandate. Cross-owner atomicity must be handled by explicit causal/receipt protocols, not a giant aggregate spanning modules.

不要根据数据库表或目录来分配聚合根。只有当一组不变量必须在单一 Owner 边界内原子提交时，聚合才成立。上列均为 Owner 侧事务分析候选，不是 B 的强制决定。跨 Owner 原子性必须通过明确因果/Receipt 协议处理，而不是建立横跨模块的巨型聚合。

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

## 9. Minimum and recommended models / 最小模型与推荐模型

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

## 10. Gate status / 门禁状态

B1 is IN PROGRESS. The assessment identifies a minimum and recommended candidate model but does not finalize Fact/Claim, Claim identity, aggregate boundaries or Owner-local schemas. No implementation cost estimates or performance measurements were run; complexity comparisons are qualitative.

B1 进行中。本评估识别了最小和推荐候选模型，但未最终决定 Fact/Claim、Claim 身份、聚合边界或 Owner 局部 Schema。未执行实现成本估算或性能测量；复杂度比较为定性判断。
