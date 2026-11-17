# Canonical Domain Glossary
# 规范领域术语表

- ID: B-GLOSSARY-001
- Status: CANDIDATE GLOSSARY; Fact/Claim and several cross-owner terms remain OPEN
- Rule: English canonical term is stable; Chinese is the semantic equivalent, not a forced one-word translation.

| Canonical English | Canonical Chinese | Definition | Non-definition / forbidden synonym | Owner | Status |
|---|---|---|---|---|---|
| Memory | 记忆资产 / 规范记忆 | Stable, addressable canonical knowledge asset with lifecycle and immutable versions | Not a transcript, single row, Context or embedding | D (semantics B) | DECIDED concept |
| Memory Version | 记忆版本 | Immutable snapshot/revision of one Memory identity | Not ContextVersion, Runtime checkpoint or updated Memory identity | D | DECIDED |
| Claim | 命题 / 主张 | Proposition about an Entity, Event or state, with epistemic and temporal qualification | Not automatically Fact or verified truth | B/E/D | ADR-BLOCKED identity/schema |
| Fact | 事实（待裁决） | Term reserved for explicit Fact/Claim ADR; must not be assumed equivalent to Verified Claim | Forbidden as a silent synonym for Claim | B | ADR-BLOCKED |
| Observation | 观察 / 观测 | An observed phenomenon/report with observer and observation time | Not automatically verified Claim or Evidence | B/E | CANDIDATE |
| Event | 事件记录 | Captured occurrence, observation, report or state transition with stable identity and Recorded At | Not protocol Event Envelope or every state update | B/C/D | DECIDED concept |
| Entity | 实体 / 指称对象 | Identity-bearing referent distinct from its label, mention or description | Not any noun phrase or RDF class automatically | B | DECIDED |
| Relation | 关系 | Typed association between domain endpoints with direction, qualifiers, time, scope and evidence | Not text co-occurrence or arbitrary graph edge | B | DECIDED |
| Evidence | 证据材料 | Independently addressable source material/observation used to support, refute or qualify a Claim/Relation | Not Source, Confidence or Provenance | B/E | DECIDED concept |
| Source | 来源 | Origin from which information is obtained | Not necessarily an independent canonical entity; not Evidence itself | B/E | OPEN classification |
| Provenance | 来源追溯 / 派生溯源 | Trace of how an asset/assertion was captured or derived from exact inputs and methods | Not source trust or correctness proof | B/E | DECIDED concept; granularity OPEN |
| Derivation | 派生 | Explicit source-to-target transformation/lineage relation | Not inference correctness or generic update | B/E | DECIDED concept |
| Confidence | 置信度 | Method-, scale- and calibration-qualified estimate about support | Not truth, verification or Evidence Strength | B/E/F | DECIDED distinction |
| Evidence Strength | 证据支持强度 | Claim-relative assessment of how materially/directly Evidence supports/refutes a Claim | Not global Evidence quality or confidence | B/E | TO_VALIDATE rubric |
| Identity | 身份 | Stable referent of an object within an explicit namespace | Not content hash, label, credential or permission | B/I | DECIDED distinction |
| Typed Reference (Ref) | 类型化引用 | Typed, namespaced pointer to a registered domain/security identity or object | Not authentication, trust or authorization | B | DECIDED technical baseline |
| Principal | 安全主体 | I-resolved security subject after trust/credential/issuer validation | Not User label, Domain Entity or ActorRef | I | I technical baseline; governance blocked |
| ActorRef | 行为主体引用 / 操作归因引用 | Immutable per-operation attribution binding a verified Principal and acting/delegation context | Not PrincipalRef, credential, bearer token or grant | B/I/H | JOINT technical baseline; consumer acceptance open |
| Subject | 主体（需限定上下文） | Security/domain term whose exact meaning must be defined by owning context | Not universal synonym for Principal/User/Entity | I/B | OPEN |
| Tenant | 租户 / 安全隔离域（待定义） | Namespace/isolation concept; exact taxonomy is I/A-owned | Not automatically Workspace, Project or User | I/A | OPEN |
| Workspace | 工作空间 | Project/application collaboration boundary if defined by project governance | Not automatically Tenant or Scope | A/I | OPEN |
| Scope | 作用域 / 适用边界 | Typed boundary for ownership, applicability or access resolution | Not Permission or a generic string tag | B/I/G | DECIDED distinction; taxonomy OPEN |
| ScopeRef | 作用域引用 | Typed reference to an authoritative Scope | Not access grant | B/I | JOINT technical baseline |
| Environment | 环境域 | Authoritative world/save/simulation/device-fleet/external state domain | Not display label, coordinate or deployment environment unless typed | B/C/I | DECIDED distinction; registry authority OPEN |
| EnvironmentRef | 环境引用 | Typed identity reference to an Environment | Not Environment Scope or Environment revision | B/I/H | JOINT technical baseline |
| Session | 会话（需限定） | Bounded execution/interaction context as defined by C/G/H | Not automatically Conversation or RuntimeSessionRef | C/G/H | OPEN mapping |
| Conversation | 对话 | Interaction/history object as defined by C/G | Not necessarily runtime session or authorization scope | C/G | OPEN |
| RuntimeSessionRef | 运行时会话引用 | Authenticated bounded runtime/session identity for operation binding | Not Conversation ID or Session ScopeRef | B/H/I | JOINT technical baseline |
| Context | 上下文目标 | G-owned scoped desired set/materialization of canonical references for a task/Agent/Environment | Not a second canonical Memory store or F Working Set | G | G-local semantics |
| ContextVersion | 上下文版本 | Immutable G-owned version of desired Context state | Not MemoryVersion, index watermark or checkpoint | G | G-local semantics |
| Context Entry | 上下文条目 | G-owned membership/reference record in a ContextVersion | Not canonical Memory or Evidence | G | G-local; identity to validate |
| ChangeSet | 变更集 | G-owned proposed/reconciled changes bound to Context base/target versions | Not BMCP Command or Memory revision | G | G-local |
| Retrieval | 检索 | F-owned process that returns candidate canonical references | Not Context membership or Activation | F | Owner-local |
| Activation | 激活 | F/runtime selection/use-readiness process for a candidate | Not canonical Memory lifecycle state | F | OPEN |
| Working Set | 工作集 | F-owned runtime-local set of refs/snippets for active task | Not G ContextVersion or canonical Memory | F | Owner-local |
| Recorded | 已记录 | Owning system durably records an event/evidence/decision | Not Applied, Committed, Visible or Published | Record owner | DECIDED distinction |
| Applied | 已应用 | G-committed historical proof that exact ContextVersion was included in exact submitted request under full predicate | Not Delivered, ACK, model attention, understanding or execution success | G (C/H/I/D evidence) | Freeze BLOCKED |
| Committed | 已提交 | Owning transaction/authority durably commits defined state change | Not universal reader visibility or Applied | Transaction owner | DECIDED distinction |
| Visible | 可见 | Eligible for reader disclosure through authoritative visibility and access checks | Not staged bytes, outbox or local state | Storage + reader enforcement | Storage proposal |
| Published | 已发布 | Storage visibility commit and exact PublicationReceipt/VisibilityPointer readback | Not I COMMIT_WON or E local terminal flag | Storage | JF-10 open |
| Deleted | 已删除 | A specified logical deletion action completed for a defined target scope | Not Forget or physical Purge by implication | Deleting owner | DECIDED distinction |
| Forgotten | 已遗忘 | D canonical Memory lifecycle state after governed Forget criterion; content access denied and cleanup tracked | Not ForgetOperation phase, global completion or physical erasure | D/I | DECIDED split |
| Purged | 已物理清除 | Named physical target met approved erasure criterion with target-scoped proof | Not tombstone, suppression or missing row | Storage/backup under I | OPEN implementation |
| Forget Request | 遗忘请求 | Request to initiate governed Forget; distinct from authorization and execution | Not ForgetOperation outcome | D/I | DECIDED distinction |
| ForgetOperation | 遗忘操作 | D-owned durable operation identity/phases/fence/barrier | Not Memory lifecycle state | D | DECIDED semantics |
| ForgetFence | 遗忘栅栏 | Monotonic D-owned suppression/order boundary over target lineage | Not I PermissionEpoch | D | DECIDED semantics |
| PermissionEpoch | 权限策略纪元 | Opaque monotonic I policy-domain epoch used for current authorization | Not D fence generation or global sequence | I | JOINT technical baseline; governance blocked |
| Source Event | 来源事件 | Captured source occurrence/report that can feed compiler | Not BMCP Event Envelope | B/C/E | DECIDED concept |
| Protocol Message | 协议消息 | H-owned wire envelope/message | Not domain object or operation state | H | DECIDED distinction |
| Command | 命令 | Protocol or workflow request to perform an operation | Not evidence that operation occurred | H / workflow owner | DECIDED distinction |
| Receipt | 回执 | Issuer-bound evidence of one declared operation boundary/outcome | Not generic success or stronger downstream proof | Issuing owner | DECIDED distinction |
| Provider Outcome | Provider 执行结果 | C-owned observed outcome at actual provider/runtime submit boundary | Not request intent, transport ACK or G Applied | C | C-owned |
| Memory Source | 记忆来源关联 | Typed source association attached to Memory with role/locator/scope | Not necessarily first-class Source entity | B/E | OPEN granularity |
| Summary | 摘要 | Derived representation or a Memory kind when explicitly canonicalized | Not automatically an independent entity | E/F/G | DEFERRED |
| Hypothesis | 假设 | Unverified proposed explanation, if the Fact/Claim model adopts it | Not Verified Claim | B/E | DEFERRED pending ADR |

## Forbidden synonym rules / 禁止同义替换

1. Memory Record / Item / Fragment are not separate canonical entities unless independent identity/lifecycle is justified.
2. Fact must not silently replace Claim while ADR-BLOCKED.
3. Source, Evidence and Provenance are not synonyms.
4. Principal, ActorRef, AgentRef, AdapterRef and ProducerRef are not interchangeable.
5. Tenant, Workspace, Project and Scope are not interchangeable.
6. Session, Conversation and RuntimeSessionRef are not interchangeable.
7. ContextVersion, MemoryVersion, checkpoint and index generation are not interchangeable.
8. Recorded, Applied, Committed, Visible and Published are not interchangeable.
9. Deleted, Forgotten and Purged are not interchangeable.
10. Delivered ACK is not Final Request Submitted or Applied.

## Gate status / 门禁状态

Glossary is a candidate shared vocabulary. Terms with OPEN/ADR-BLOCKED/TO_VALIDATE status must not be used to freeze schemas or infer cross-owner approval.

本术语表是共享词汇候选版本。标记 OPEN/ADR-BLOCKED/TO_VALIDATE 的术语不得用于冻结 Schema 或推断跨 Owner 批准。
