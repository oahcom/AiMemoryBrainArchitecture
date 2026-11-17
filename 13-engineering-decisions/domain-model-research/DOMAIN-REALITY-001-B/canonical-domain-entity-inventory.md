# Canonical Domain Entity Inventory
# 规范领域实体清单

- ID: B-INV-001
- Status: CANDIDATE INVENTORY — B1 IN PROGRESS
- Baseline: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Primary source: `02-domain-model/core-entities.md` Blob `8cb5a674eec8eac1f3c4d83c400dc08d00166f23`; `domain-model-overview.md` Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`.

## 1. Classification rules / 分类规则

- **CANONICAL_ENTITY**: independently addressable domain object with identity and a meaningful reference/lifecycle.
- **VALUE_OBJECT**: meaningful typed value whose identity is supplied by its containing object or relation.
- **DERIVED_VIEW**: runtime/query/presentation result that can be rebuilt and is not canonical truth.
- **PROTOCOL_OBJECT**: transport or adapter envelope; never a domain entity merely because it references one.
- **IMPLEMENTATION_DETAIL**: persistence/runtime mechanism with no independent domain meaning.
- **DEFERRED_CONCEPT**: potentially useful, but no demonstrated independent identity/lifecycle requirement.
- **REJECTED_ABSTRACTION**: duplicates another concept or falsely collapses distinct semantics.

**中文：** CANONICAL_ENTITY 表示需要独立寻址和引用的规范领域对象；VALUE_OBJECT 是由所属对象/关系赋予身份的类型化值；DERIVED_VIEW 是可重建的运行时/查询/呈现结果；PROTOCOL_OBJECT 是传输对象；IMPLEMENTATION_DETAIL 是无独立领域含义的实现机制；DEFERRED_CONCEPT 是尚无独立身份/生命周期依据的概念；REJECTED_ABSTRACTION 是重复或错误合并语义的抽象。

## 2. Core canonical candidates / 核心规范实体候选

| Concept | Classification | Identity / lifecycle rationale | Decision status |
|---|---|---|---|
| Event | CANONICAL_ENTITY | Captured occurrence/report/observation; stable event_id, recorded_at, source and scope; may produce zero/many memories | DECIDED in source |
| Memory | CANONICAL_ENTITY | Retained addressable knowledge asset; memory_id stable across immutable versions; lifecycle owned by D | DECIDED in source |
| Memory Version | CANONICAL_ENTITY | Immutable historical snapshot with version ID and parent relation; independent reference needed for provenance/context | DECIDED in source |
| Claim | CANONICAL_ENTITY (identity policy OPEN) | Proposition with subject/predicate/object, epistemic and temporal qualifications; identity across versions remains OPEN | DECIDED concept; OPEN identity |
| Entity | CANONICAL_ENTITY | Identity-bearing referent distinct from display name/mention; merge/split lineage | DECIDED in source |
| Relation | CANONICAL_ENTITY | Typed, scoped, temporal association with endpoint constraints and lifecycle | DECIDED in source |
| Evidence | CANONICAL_ENTITY | Independently addressable source material/observation with role, locator, access and availability | DECIDED in source |
| Provenance | CANONICAL_ENTITY candidate | Derivation/origin record with inputs, method, time and lineage; identity needed for multi-generation trace | Core concept DECIDED; exact record granularity OPEN |
| Memory Context | CANONICAL_ENTITY | Scoped, versioned task-oriented selection with G-owned lifecycle/version authority | DECIDED concept; G contract authority |
| Context Entry | CANONICAL_ENTITY candidate | Addressable reference/presentation inside Context; whether each entry needs standalone identity must be confirmed by G | DECIDED concept; identity TO_VALIDATE |
| Scope | CANONICAL_ENTITY / typed family | Stable namespace/ownership/applicability reference; exact taxonomy/algebra OPEN with I | Separation DECIDED; taxonomy OPEN |

## 3. Value objects and typed references / 值对象与类型化引用

| Concept | Classification | Reason | Status |
|---|---|---|---|
| Opaque ID | VALUE_OBJECT | Non-semantic identifier value; algorithm not normative (UUIDv7 only candidate) | DECIDED semantics |
| TypedObjectRef | VALUE_OBJECT | Category + canonical identifier; prevents ambiguous cross-module references | CANDIDATE; grammar not pinned |
| ScopeRef | VALUE_OBJECT | Typed reference to a Scope; not Permission | DECIDED separation; shape OPEN |
| ActorRef | VALUE_OBJECT at B boundary | Reference to acting identity; authenticated Principal semantics owned by I/H | OPEN joint mapping |
| ExternalId | VALUE_OBJECT | Namespaced external identifier; uniqueness scoped by issuer/type/tenant as approved | Candidate; policy OPEN |
| TimeValue / TimeInterval | VALUE_OBJECT | Explicit instant/interval with uncertainty and precision; uncertainty encoding OPEN | Core distinction DECIDED |
| ClaimSnapshot | VALUE_OBJECT | Immutable claim representation embedded in Memory Version unless separate versioned Claim identity required | CANDIDATE pending Claim identity ADR |
| AliasRecord | VALUE_OBJECT | Label/alias plus scope/time qualifiers; not an Entity | Source-defined |
| Locator | VALUE_OBJECT | Address/offset/span into source material; may be sensitive and independently authorized | Source-defined |
| ContentRef / Digest | VALUE_OBJECT | Opaque reference/integrity value; not the content itself | Source-defined |
| ConfidenceValue | VALUE_OBJECT | Method-qualified estimate; never substitutes for Evidence or verification | Source-defined |
| Qualifiers / Role / Polarity | VALUE_OBJECT | Typed semantic qualifiers, not free-form identity-bearing objects | Source-defined |

## 4. Associations, provenance and derived views / 关联、溯源与派生视图

| Concept | Classification | Reason | Status |
|---|---|---|---|
| Memory Source | CANONICAL_ENTITY or association record | Typed, version-aware edge from derived asset to input; independent identity only if edge has role/time/scope/evidence/lifecycle | Exact choice OPEN |
| Claim–Evidence Link | Association record / VALUE_OBJECT | Link role can differ per Claim; separate record only when role/strength/time/scope requires it | Candidate |
| Relation Qualifier | VALUE_OBJECT | Qualifies a Relation; not another Relation | Candidate |
| Derivation Run | DEFERRED_CONCEPT pending E | Compiler execution identity belongs to E; B only needs derivation lineage record semantics | Do not duplicate E Run ID |
| Inference | DEFERRED_CONCEPT / process descriptor | Method/result classification, not automatically a persisted domain entity | OPEN |
| Summary | DERIVED_VIEW or Memory kind | No separate entity unless independent lifecycle/identity proven | DEFERRED |
| Retrieval Result / Candidate / Ranking | DERIVED_VIEW | F-owned query result; transient unless explicit audit requirement | DEFERRED as canonical entity |
| Activation | DERIVED_VIEW or domain event | F-owned decision/process; not canonical Memory status | OPEN with F |
| Working Set | DERIVED_VIEW / IMPLEMENTATION_DETAIL | Runtime-local bounded set; not canonical asset | F-owned |
| Runtime State | IMPLEMENTATION_DETAIL / DERIVED_VIEW | Runtime implementation state, not a universal domain entity | F-owned |
| Context Snapshot / ContextVersion | CANONICAL_ENTITY or immutable version record | G owns context version; never interchangeable with Memory Version | G confirmation required |
| ChangeSet | CANONICAL_ENTITY candidate | G-owned change intent with identity and reconciliation lifecycle; do not equate to protocol command | G confirmation required |

## 5. Security, protocol and integration concepts / 安全、协议与集成概念

| Concept | Classification | Boundary |
|---|---|---|
| Principal | CANONICAL_ENTITY in Security domain | I owns authenticated security identity; not the same as domain Entity or User label |
| Subject | DEFERRED / I-owned vocabulary | Must not be used as synonym for Principal until I defines exact meaning |
| Identity / External Identity | CANONICAL_ENTITY or mapping record in I domain | B defines typed references only; issuer/trust/linking policy belongs to I |
| User | DEFERRED as generic universal entity | Could be domain subject/person or security Principal; disambiguate by context |
| Agent | CANONICAL_ENTITY or external actor reference depending on identity scope | C/I decide Agent identity vs executing instance |
| Agent Instance | CANONICAL_ENTITY candidate in integration/security boundary | Distinct runtime instance, not Agent logical identity |
| Tenant / Workspace / Project | DEFERRED taxonomy | Do not assume synonyms; I/A must define namespace and isolation role |
| Session / Conversation | DEFERRED domain status | C/G own integration/runtime semantics; may be distinct but not established by current core domain schema |
| Execution / Operation | CANONICAL_ENTITY in operation domain or C-owned record | Not interchangeable with Event or Protocol Request |
| Protocol Message / Request / Response / Command | PROTOCOL_OBJECT | H-owned wire objects; may reference but do not become domain entities |
| Receipt / Acknowledgement | PROTOCOL_OBJECT or evidence record | Receipt proves a declared boundary outcome only; exact authority H/C/G/Storage |
| Provider Outcome | CANDIDATE canonical integration outcome record | C-owned; do not reinterpret as domain Event without explicit mapping |
| Policy / Permission / Authorization Decision | I-owned governance/security objects | Not Scope; B cannot decide policy engine |
| Forget Request / Forget Operation | D/I split | Request/authorization governance differs from D canonical ForgetOperation and execution lifecycle |
| Audit Record / Governance Decision / Legal Hold | I-owned governance records | Not generic Memory status |

## 6. Similar names that must not be collapsed / 不得合并的相似概念

- Event ≠ Memory ≠ Claim ≠ Evidence.
- Memory ≠ Memory Version; stable asset identity differs from immutable snapshot identity.
- Entity ≠ Claim subject string; Relation ≠ text co-occurrence.
- Source ≠ Evidence ≠ Provenance. Source is origin; Evidence is an evidential object/observation; Provenance is the derivation trace.
- Claim epistemic status ≠ Memory lifecycle state.
- Scope ≠ Permission; Principal ≠ domain Entity; ActorRef ≠ authentication proof.
- Context Version ≠ Memory Version; Context Entry ≠ Memory.
- Applied ≠ Recorded ≠ Committed ≠ Visible ≠ Published.
- Forget Request ≠ Forget decision ≠ Forget execution ≠ deletion/purge evidence.
- Protocol Request ≠ Operation; ACK ≠ Applied proof.

中文对应：Event、Memory、Claim、Evidence 不可互换；Memory 与 Memory Version 分别表示稳定资产和不可变快照；Entity 不等于命题中的文本主体，Relation 不等于文本共现；Source、Evidence、Provenance 分别表示来源、证据对象和派生追溯；Claim 认知状态不等于 Memory 生命周期；Scope 不等于 Permission，Principal 不等于领域 Entity，ActorRef 不构成身份认证证明；Context Version 不等于 Memory Version；Applied、Recorded、Committed、Visible、Published 不得合并；Forget Request、决定、执行和删除/清除证据必须分离；协议 Request 不等于 Operation，ACK 不等于 Applied 证明。

## 7. Inventory questions still open / 清单未决问题

1. Does Claim have stable identity across Memory Versions, or is it a version-local ClaimSnapshot? (B ADR required)
2. Does Provenance require an independent record ID for every derivation edge, or can a typed edge plus immutable artifact version suffice?
3. When does Memory Source need independent identity?
4. Is Context Entry independently addressable and versioned under G?
5. What is the canonical Scope taxonomy and namespace hierarchy (User/Tenant/Workspace/Project/Agent/Instance/Task/Session/Environment/System)?
6. Are Session and Conversation separate domain entities or C/G runtime integration objects?
7. Is Provider Outcome a durable domain record, a C-owned operation outcome, or both via explicit mapping?
8. Which governance records are shared canonical concepts versus I-owned local model?
9. Does a Source require a first-class entity separate from Event/Document/External SourceRef?
10. Which derived views require durable audit retention without becoming canonical domain entities?

## 8. Gate disposition / 门禁结论

B1 is **IN PROGRESS**. This inventory is a classification proposal grounded in the current main domain source and owner guides. It is not a final entity approval. All Owner-owned classifications remain subject to exact normative contract readback and owner confirmation. No schema is frozen by this inventory.

B1 **进行中**。本清单基于当前 main 领域源规范及 Owner 指南形成分类提案，并非最终实体批准。所有 Owner 所属概念仍需精确读取规范契约并由对应 Owner 确认。本清单不冻结任何 Schema。
