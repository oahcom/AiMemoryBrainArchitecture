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
| C Origin Signature | C 来源签名 | C-owned signature over exact C message-family P0; proves origin attribution under an approved profile | Not H transport authentication, I authorization or provider truth by itself | C / I trust registry | Candidate; crypto profile not approved |
| Outer Envelope P0 | 外层 Envelope P0 | Exact canonical projection of serialized H envelope members for digest/signature verification | Not C object P0 or arbitrary JSON serialization | C defines signed semantics; H maps wire; I approves profile | Mapping candidate; executable verification open |
| Protected Transport Context | 受保护传输上下文 | Verifier-produced context binding authenticated transport sender/session/channel/audience | Not payload sender claim or caller-created struct | H transport; I trust | Reference gate only; production open |
| BrainAuthorityRef | Brain 语义权威引用 | Reference to canonical Memory semantic authority | Not StorageAuthorityRef or PolicyDomainRef | B / D | Candidate typed reference |
| SerializationDomainRef | 序列化域引用 | Physical/logical transaction domain for one serialization anchor | Not BrainAuthorityRef or COC domain | Storage / B type boundary | Implementation detail |
| AuthoritySerializationAnchorRef | Authority 序列化锚点引用 | Physical anchor row identity for one BrainAuthority within a SerializationDomain | Not D Fence, VisibilityPointer or global sequence | Storage / B type boundary | Implementation detail |
| SerializationTransitionRef | 序列化转换引用 | Stable idempotent identity of one physical serialization transition | Not PublicationOperationId, WorkItemId or XID | Storage / B type boundary | Implementation detail |
| SerializationRevision | 序列化修订号 | Monotonic physical revision local to one anchor/domain | Not D FenceGeneration, I PermissionEpoch, C sequence, COC position or XID | Storage | Implementation detail |
| Memory Source | 记忆来源关联 | Typed source association attached to Memory with role/locator/scope | Not necessarily first-class Source entity | B/E | OPEN granularity |
| Summary | 摘要 | Derived representation or a Memory kind when explicitly canonicalized | Not automatically an independent entity | E/F/G | DEFERRED |
| Hypothesis | 假设 | Unverified proposed explanation, if the Fact/Claim model adopts it | Not Verified Claim | B/E | DEFERRED pending ADR |

## Chinese definition mirror / 中文定义对照表

| Canonical English Term | 中文定义 | 中文非定义 / 禁止混淆 |
|---|---|---|
| Memory | 具有稳定身份、可被独立寻址并受生命周期管理的规范知识资产。 | 不是 Transcript、单条数据库记录、Context 或 Embedding。 |
| Memory Version | 同一 Memory 身份下不可变的内容/语义版本。 | 不等于 ContextVersion、Runtime Checkpoint 或新的 Memory 身份。 |
| Claim | 关于 Entity、Event 或状态的命题，带有认知状态和时间限定。 | 不自动等于 Fact，也不自动代表已验证真相。 |
| Fact | 与 Claim 不同的领域概念；其对象身份和表示方式仍由 ADR 裁决。 | 不得在 ADR 完成前静默作为 Claim 的同义词或独立 Schema。 |
| Observation | 带观察者和观察时间的观察现象、记录或报告。 | 不自动成为已验证 Claim 或 Evidence。 |
| Event | 具有稳定身份及 Recorded At 的已捕获发生、观察、报告或状态变化。 | 不等于 BMCP Event Envelope，也不是每次状态更新。 |
| Entity | 与标签、提及或描述相区分的、具有身份的指称对象。 | 不等于任意名词短语，也不自动等于 RDF Class。 |
| Relation | 端点、方向、限定条件、时间、Scope 和 Evidence 明确的类型化关联。 | 不等于文本共现或任意图边。 |
| Evidence | 可独立寻址、用于支持/反驳/限定 Claim 或 Relation 的材料。 | 不等于 Source、Confidence 或 Provenance。 |
| Source | 信息取得的来源或起点。 | 不必然是独立规范实体；也不等于 Evidence 本身。 |
| Provenance | 对资产/命题如何从精确输入和处理方法中捕获或派生的追溯记录。 | 不等于来源可信度，也不单独证明结论正确。 |
| Derivation | 明确从源对象到目标对象的转换/谱系关系。 | 不等于推理正确性或一般更新。 |
| Confidence | 关于支持程度的、带方法/量表/校准条件的估计。 | 不等于 Truth、Verification 或 Evidence Strength。 |
| Evidence Strength | 针对特定 Claim 评估 Evidence 支持/反驳的实质性和直接程度。 | 不等于 Evidence 的全局质量或 Confidence。 |
| Identity | 对象在明确命名空间内稳定的指称身份。 | 不等于内容 Hash、标签、凭证或权限。 |
| Typed Reference (Ref) | 指向已注册领域/安全身份或对象的类型化、带命名空间引用。 | 不等于 Authentication、Trust 或 Authorization。 |
| Principal | 经 I 验证信任链、凭证和 Issuer 后解析的安全主体。 | 不等于 User 标签、Domain Entity 或 ActorRef。 |
| ActorRef | 每次操作不可变的归因引用，绑定已验证 Principal 和行为/委托上下文。 | 不等于 PrincipalRef、Credential、Bearer Token 或 Grant。 |
| Subject | 必须由所属上下文限定含义的安全/领域主体术语。 | 不得作为 Principal、User 或 Entity 的通用同义词。 |
| Tenant | 隔离/命名空间概念，精确分类由 I/A 决定。 | 不自动等于 Workspace、Project 或 User。 |
| Workspace | 若项目治理定义，则表示协作/项目工作边界。 | 不自动等于 Tenant 或 Scope。 |
| Scope | 用于解析所有权、适用性或访问边界的类型化边界。 | 不等于 Permission，也不是任意字符串标签。 |
| ScopeRef | 指向权威 Scope 的类型化引用。 | 不等于访问授权。 |
| Environment | 世界、存档、仿真、设备群或外部状态域。 | 不等于显示标签、坐标或未加类型的部署环境。 |
| EnvironmentRef | 指向 Environment 的稳定类型化身份引用。 | 不等于 Environment Scope 或 Environment Revision。 |
| Session | 由 C/G/H 定义的有界执行/交互上下文。 | 不自动等于 Conversation 或 RuntimeSessionRef。 |
| Conversation | 由 C/G 定义的交互历史/对话对象。 | 不必然等于 Runtime Session 或授权 Scope。 |
| RuntimeSessionRef | 用于操作绑定的、经过认证的有界运行时/会话身份。 | 不等于 Conversation ID 或 Session ScopeRef。 |
| Context | G 拥有的、任务范围内期望的引用集合/物化视图。 | 不等于第二套规范 Memory 存储，也不等于 F Working Set。 |
| ContextVersion | G 拥有的 Context 期望状态的不可变版本。 | 不等于 MemoryVersion、Index Watermark 或 Checkpoint。 |
| Context Entry | ContextVersion 中由 G 管理的成员/引用记录。 | 不等于规范 Memory 或 Evidence。 |
| ChangeSet | G 拥有的、绑定 Context 基础/目标版本的提议或协调变更集合。 | 不等于 BMCP Command 或 Memory Revision。 |
| Retrieval | F 拥有的返回规范对象候选引用的检索过程。 | 不等于 Context 成员资格或 Activation。 |
| Activation | F/Runtime 对候选对象进行选择或判定可供当前任务使用的过程。 | 不等于规范 Memory 生命周期状态。 |
| Working Set | F 拥有的当前任务运行时局部引用/片段集合。 | 不等于 G ContextVersion 或规范 Memory。 |
| Recorded | 权威系统已持久记录事件、证据或决定。 | 不等于 Applied、Committed、Visible 或 Published。 |
| Applied | G 对精确 ContextVersion 已进入精确提交请求的历史事实证明，且满足完整谓词。 | 不等于 Delivered、ACK、模型注意、理解或执行成功。 |
| Committed | 所属事务/权威已持久提交所定义的状态变化。 | 不等于所有读取方已可见，也不等于 Applied。 |
| Visible | 通过权威可见性和访问检查后可向读取方披露。 | 不等于 Staged Bytes、Outbox 或局部状态。 |
| Published | Storage 完成可见性提交，并精确读回 PublicationReceipt/VisibilityPointer。 | 不等于 I COMMIT_WON 或 E 局部终态标志。 |
| Deleted | 在明确目标范围内完成指定逻辑删除动作。 | 不自动等于 Forget 或物理 Purge。 |
| Forgotten | D 规范 Memory 生命周期状态，满足受治理 Forget 标准后拒绝内容访问并跟踪清理。 | 不等于 ForgetOperation 阶段、全局完成或物理擦除。 |
| Purged | 指定物理目标满足批准的擦除标准并具有目标级证明。 | 不等于 Tombstone、Suppression 或记录缺失。 |
| Forget Request | 请求启动受治理 Forget 流程的请求对象。 | 不等于授权决定或 ForgetOperation 结果。 |
| ForgetOperation | D 拥有的持久操作身份、阶段、Fence 和 Barrier。 | 不等于 Memory 生命周期状态。 |
| ForgetFence | D 拥有的、覆盖目标谱系的单调抑制/排序边界。 | 不等于 I PermissionEpoch。 |
| PermissionEpoch | I 策略域中用于当前授权判断的不透明单调 Epoch。 | 不等于 D Fence Generation 或全局序列。 |
| Source Event | 可供 Compiler 使用的已捕获来源发生/报告。 | 不等于 BMCP Event Envelope。 |
| Protocol Message | H 拥有的 Wire Envelope/消息。 | 不等于领域对象或操作状态。 |
| Command | 请求执行某个操作的协议/工作流命令。 | 不证明操作实际发生。 |
| Receipt | 由签发者绑定、证明某个明确操作边界/结果的证据。 | 不等于通用成功，也不自动证明更下游结果。 |
| Provider Outcome | C 在真实 Provider/Runtime Submit 边界观察到的执行结果。 | 不等于请求意图、传输 ACK 或 G Applied。 |
| Memory Source | 附属于 Memory、带角色/Locator/Scope 的类型化来源关联。 | 不必然是独立 Source 实体。 |
| Summary | 派生表示；只有显式规范化时才可作为 Memory 类型。 | 不自动具有独立身份和生命周期。 |
| Hypothesis | 若 Fact/Claim 模型采用，则表示尚未验证的解释假设。 | 不等于 Verified Claim。 |
| C Origin Signature | C 对精确 C Message-family P0 的签名，在批准 Profile 下证明来源归属。 | 不等于 H Transport Authentication、I Authorization 或 Provider Truth。 |
| Outer Envelope P0 | 用于摘要/签名验证的 H Envelope 序列化成员规范投影。 | 不等于 C Object P0 或任意 JSON 序列化。 |
| Protected Transport Context | 由验证器生成，绑定认证传输发送方、Session、Channel 和 Audience 的上下文。 | 不等于载荷发送方声明或调用者自建 Struct。 |
| BrainAuthorityRef | 对规范 Memory 语义权威的引用。 | 不等于 StorageAuthorityRef 或 PolicyDomainRef。 |
| SerializationDomainRef | 物理/逻辑事务域的引用。 | 不等于 BrainAuthorityRef 或 COC Domain。 |
| AuthoritySerializationAnchorRef | 一个 BrainAuthority 在 SerializationDomain 中对应的物理 Anchor 行身份。 | 不等于 D Fence、VisibilityPointer 或全局序列。 |
| SerializationTransitionRef | 一个物理序列化转换的稳定幂等身份。 | 不等于 PublicationOperationId、WorkItemId 或 XID。 |
| SerializationRevision | 单个 Anchor/Domain 内单调递增的物理修订号。 | 不等于 D FenceGeneration、I PermissionEpoch、C Sequence、COC Position 或 XID。 |

Owner 和 Status 继续使用英文规范标识；其实际责任与状态以英文主表为准。/ Owner 与 Status 保留英文规范标识；具体责任和状态以英文主表为准。

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
