# Canonical State Semantics
# 规范状态语义

- ID / 编号: B-STATE-001
- Status / 状态: CANDIDATE VOCABULARY BASELINE; Owner-specific state machines remain authoritative. / 候选词汇基线；各 Owner 专属状态机仍具有权威性。
- Source pins / 来源 Pin: Domain lifecycle Blob `81c48c928cb5f9c76ca29d493fbd9479079e62f7`; epistemic/temporal Blob `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7`; D Forget contract Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`; C submit contract Blob `45a48249717c8cddb07ab96197730ef93d406c22`; Storage JF-10 protocol Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`。

## 1. Governing rule / 总原则

There is no universal cross-system `status` field. Status belongs to a typed subject and a named state machine. The same word on different object types does not imply the same transition, authority, evidence or terminality.

全系统不存在通用的 `status` 字段。状态必须属于明确类型的对象和指定状态机。不同对象类型上的同名状态，不代表相同转换、权威、证据或终态属性。

At minimum keep these dimensions separate:
- Claim epistemic standing;
- Memory lifecycle;
- Entity identity resolution;
- Relation lifecycle;
- Evidence availability;
- ForgetOperation phase;
- compiler work/attempt state;
- Context version/entry state;
- protocol delivery/acknowledgement;
- authorization decision and PermissionEpoch;
- storage transaction/visibility outcome;
- audit/governance decision.

至少必须将以下维度分开：
- Claim 认知状态；
- Memory 生命周期；
- Entity 身份解析状态；
- Relation 生命周期；
- Evidence 可用性；
- ForgetOperation 阶段；
- Compiler 工作/尝试状态；
- Context 版本/条目状态；
- 协议交付/确认状态；
- 授权决策与 PermissionEpoch；
- Storage 事务/可见性结果；
- 审计/治理决策。

## 2. Domain-owned state dimensions / 领域状态维度

| Subject / 主体 | Vocabulary evidenced in source / 来源中出现的词汇 | Meaning and owner / 含义与 Owner |
|---|---|---|
| Claim epistemic status / Claim 认知状态 | Observed, Reported, Inferred, Verified, Disputed, Retracted | Basis/standing of proposition; B defines semantics; E supplies derivation evidence; lifecycle manager preserves history. / 命题的依据/认知地位；B 定义语义；E 提供派生证据；生命周期管理方保留历史。 |
| Memory lifecycle / Memory 生命周期 | Candidate, Consolidated, Active, Superseded, Archived, Forgotten | Management stage of canonical asset; B defines valid semantics; D owns canonical lifecycle execution. / 规范资产的管理阶段；B 定义有效语义；D 负责规范生命周期执行。 |
| Entity identity status / Entity 身份状态 | provisional, resolved, merged, split, retired | Identity resolution/redirect state; Entity & Relationship Manager; identity rules need B/I reconciliation. / 身份解析/重定向状态；由 Entity & Relationship Manager 负责；身份规则需 B/I 协调。 |
| Relation lifecycle / Relation 生命周期 | proposed, active, superseded, retracted | State of typed relation; B semantics and entity/relation manager execution. / 类型化关系的状态；B 负责语义，实体/关系管理方负责执行。 |
| Evidence availability / Evidence 可用性 | available, restricted, expired, forgotten, external_unavailable | Whether evidence content/reference is available under policy; Evidence/Provenance owner + I policy. / 根据政策判断证据内容/引用是否可用；由 Evidence/Provenance Owner 与 I 政策共同约束。 |
| Scope status / Scope 状态 | active, suspended, closed, revoked | Namespace availability; I/Governance registry authority; B defines scope reference semantics. / 命名空间可用性；I/Governance 注册表具有权威性；B 定义 Scope 引用语义。 |

### 2.1 Claim epistemic status is not Memory lifecycle / Claim 认知状态不等于 Memory 生命周期

A Memory can be Active while containing Disputed Claims. An Archived Memory can contain a Verified Claim. A Retraction preserves the historical assertion and records authority/reason; it is not a deletion of historical evidence. Confidence alone cannot promote a Claim to Verified.

Memory 可以处于 Active，同时包含 Disputed Claim。Archived Memory 也可以包含 Verified Claim。Retracted 会保留历史断言并记录权威/原因；它不是删除历史证据。置信度本身不能将 Claim 提升为 Verified。

### 2.2 Forgotten is not a ForgetOperation phase / Forgotten 不是 ForgetOperation 阶段

D's canonical Memory lifecycle vocabulary includes Forgotten. D's separate ForgetOperation phases include Requested, FenceEstablished, InventoryOpen, BarrierDraining, TargetReconciliation, CanonicalSuppressionComplete, Blocked and Failed. D explicitly states that “Forgetting” is not a Memory state. I separately owns global completion criteria and physical-erasure governance. The lifecycle transition to Forgotten is appended only when I's applicable criterion is met; it is not physical-erasure evidence.

D 的规范 Memory 生命周期词汇包含 Forgotten。D 独立的 ForgetOperation 阶段包括 Requested、FenceEstablished、InventoryOpen、BarrierDraining、TargetReconciliation、CanonicalSuppressionComplete、Blocked 和 Failed。D 明确指出，“Forgetting”不是 Memory 状态。I 独立负责全局完成标准和物理擦除治理。只有满足 I 适用的标准后，才追加到 Forgotten 的生命周期转换；该转换不是物理擦除证据。

## 3. Other owner state domains / 其他 Owner 状态域

| Subject / 主体 | Examples / 示例 | Authority boundary / 权威边界 |
|---|---|---|
| Compiler work / Compiler 工作 | CompileIntent, ProducerWorkItem, DerivationRun, Attempt, Lease, retry/DLQ/replay and terminal outcomes. / CompileIntent、ProducerWorkItem、DerivationRun、Attempt、Lease、重试/DLQ/重放及终态结果。 | E owns compiler-internal work/attempt state; D owns producer registration/barrier semantics. / E 负责 Compiler 内部工作/尝试状态；D 负责 Producer 注册/Barrier 语义。 |
| Context / 上下文 | ContextVersion, ChangeSet, entry states, reconciliation and historical Applied/current-use eligibility. / ContextVersion、ChangeSet、条目状态、协调过程及历史 Applied/当前使用资格。 | G owns Context semantics and Applied state; exact current contract needs readback. / G 负责 Context 语义和 Applied 状态；当前精确契约仍需读回核验。 |
| Protocol delivery / 协议交付 | Accepted/Rejected/Unknown, Delivery ACK, reconnect and capability epochs. / Accepted/Rejected/Unknown、Delivery ACK、重连及 Capability Epoch。 | H owns wire/transport ACK; transport ACK is not final Applied proof. / H 负责 Wire/传输 ACK；传输 ACK 不是最终 Applied 证明。 |
| Provider submit / Provider 提交 | CSubmitOutcome accepted/rejected/unknown/in-doubt. / CSubmitOutcome 的 accepted/rejected/unknown/in-doubt。 | C alone records actual provider boundary outcome; unknown is not success or safe retry. / 只有 C 记录真实 Provider 边界结果；unknown 不代表成功，也不代表可安全重试。 |
| Authorization / 授权 | Allow/Deny/Indeterminate and PermissionEpoch. / Allow/Deny/Indeterminate 与 PermissionEpoch。 | I owns policy, currentness, revocation order. / I 负责政策、时效性及撤销顺序。 |
| Storage transaction / Storage 事务 | Prepared, owner commit/abort, outcome unknown. / Prepared、Owner commit/abort、结果未知。 | Storage owns physical participant outcome; exact XID recovery. / Storage 负责物理 Participant 结果及精确 XID 恢复。 |
| Publication / 发布 | VisibilityPointer, PublicationReceipt, Published. / VisibilityPointer、PublicationReceipt、Published。 | Storage owns durable visibility and publication receipt. / Storage 负责持久可见性及发布 Receipt。 |
| Governance / 治理 | Approved/Denied/Deferred/Exception etc. / Approved/Denied/Deferred/Exception 等。 | I/governance authority; B cannot infer external approval. / 由 I/治理权威负责；B 不得推断外部批准。 |

## 4. Critical execution vocabulary / 关键执行词汇

| Term / 术语 | Canonical semantic meaning / 规范语义 | What it does NOT prove / 不证明什么 | Authority / 权威 |
|---|---|---|---|
| Recorded | A fact/evidence/decision has been durably recorded by its owning system, with an authoritative record reference. / 某事实/证据/决策已由所属系统持久记录，并具有权威记录引用。 | It does not prove an external side effect, context application, transaction commit, or reader visibility. / 不证明外部副作用、Context 应用、事务提交或读者可见性。 | Record-owning module. / 记录所属模块。 |
| Applied | The declared target operation crossed its exact application boundary and has the owner-required evidence; for Context, exact Adapter/final-request proof is required by approved contract. / 声明的目标操作已跨越精确应用边界，并具备 Owner 要求的证据；对于 Context，已批准契约要求精确 Adapter/最终请求证明。 | Transport ACK, buffer digest, reservation, or delivery receipt alone does not prove final request Applied; does not prove model comprehension. / 单独的传输 ACK、Buffer Digest、Reservation 或 Delivery Receipt 不能证明最终请求 Applied；也不证明模型理解了内容。 | G validates/commits Context Applied; C proves final provider submit; H transports proof. / G 验证/提交 Context Applied；C 证明最终 Provider 提交；H 传输证明。 |
| Committed | The owning transaction/authority durably committed the defined state change and can resolve it after recovery. / 所属事务/权威已持久提交定义的状态变更，并能在恢复后解析其结果。 | It does not universally imply indexing, Context application, or reader visibility in unrelated projections. / 不普遍意味着其他投影已完成索引、Context 应用或读者可见。 | Transaction/authority owner. / 事务/权威 Owner。 |
| Visible | The object is eligible for reader disclosure through the authoritative visibility mechanism after policy/scope checks. / 对象通过政策/Scope 检查后，符合权威可见性机制的读者披露条件。 | Staged bytes, queue/outbox state, object-store path, I COMMIT_WON alone, or local compiler state do not make it visible. / Staged Bytes、Queue/Outbox 状态、Object Store 路径、单独的 I COMMIT_WON 或 Compiler 局部状态都不会使其可见。 | Storage visibility authority; reader enforcement also applies. / Storage 可见性权威；读者侧仍须执行访问控制。 |
| Published | The Storage-owned visibility transaction committed and the exact PublicationReceipt/VisibilityPointer can be authoritatively read back; E may then terminalize its work as Published. / Storage 所属的可见性事务已提交，且可权威回读精确 PublicationReceipt/VisibilityPointer；此后 E 才可将其工作终结为 Published。 | I COMMIT_WON alone, E local state, ACK or staged bytes do not prove Published. / 单独的 I COMMIT_WON、E 局部状态、ACK 或 Staged Bytes 都不能证明 Published。 | Storage owns publication; E consumes receipt. / Storage 负责发布；E 消费 Receipt。 |
| Acknowledged | A recipient/adapter reports the specific protocol action covered by its ACK class. / 接收方/Adapter 报告其 ACK 类别所覆盖的特定协议动作。 | Does not prove any stronger operation than that ACK's declared coverage; may be necessary but is not sufficient for Applied. / 不证明超出 ACK 声明范围的更强操作；它可能是 Applied 的必要条件，但不是充分条件。 | H/recipient. / H/接收方。 |
| Authenticated | A verifier establishes the exact sender/issuer/credential/transport context under an approved trust profile. / 验证器依据获批信任 Profile 确立精确发送方/Issuer/凭据/传输上下文。 | Does not prove authorization, C provider truth, Applied, or Storage publication. / 不证明已授权、C Provider 结果真实、Applied 或 Storage 已发布。 | H transport; I trust/profile; C origin signature. / H 负责传输；I 负责信任/Profile；C 负责来源签名。 |
| Superseded | A successor replaces an object for current use while historical identity/version remains retained subject to policy. / 后继对象替代当前使用对象，而历史身份/版本仍按政策保留。 | Does not imply deletion or invalidity of every historical assertion. / 不意味着删除历史断言，也不意味着所有历史断言均无效。 | Domain object's lifecycle owner. / 领域对象生命周期 Owner。 |
| Invalidated | A specified result/claim/proof/lease is no longer eligible under a named invalidation rule. / 指定结果/Claim/Proof/Lease 根据命名失效规则不再具备资格。 | Does not erase history or necessarily alter parent object's lifecycle. / 不会抹除历史，也不一定改变父对象生命周期。 | Owner of invalidated artifact/state. / 被失效工件/状态的 Owner。 |
| Deleted | A defined logical record/content reference has been removed under a stated deletion operation. / 根据指定删除操作，定义的逻辑记录/内容引用已被移除。 | Does not prove all replicas, backups, exports or derivatives are physically erased. / 不证明所有副本、备份、导出件或派生物均已物理擦除。 | Deleting subsystem / Storage. / 执行删除的子系统/Storage。 |
| Forgotten | D canonical Memory lifecycle state after governed Forget criterion; ordinary content access is denied and cleanup tracked. / 满足治理 Forget 标准后的 D 规范 Memory 生命周期状态；普通内容访问被拒绝，清理过程受到跟踪。 | Does not itself prove global completion or physical erasure. / 本身不证明全局完成或物理擦除。 | D, gated by I policy. / D，受 I 政策门控。 |
| Purged | A specified physical retention target has passed its approved erasure criterion with target-scoped evidence. / 指定物理保留目标已通过批准的擦除标准，并具有按目标限定的证据。 | Cannot be claimed from tombstone, suppression, or missing row. / 不能仅凭 Tombstone、抑制或行缺失宣称已 Purged。 | Storage/backup operator under I policy. / I 政策下的 Storage/备份操作方。 |

## 5. Ordering semantics / 顺序语义

Do not define one universal total order among Recorded, Applied, Committed, Visible and Published. Their relationship depends on the operation and authority.

不得为 Recorded、Applied、Committed、Visible、Published 规定全系统通用的全序关系。它们之间的关系取决于具体操作和权威。

Verified constraints from current source / 当前来源中已核验的约束：
1. A source/evidence record may be Recorded before any downstream Claim/Memory is committed. / 来源/证据记录可以先于任何下游 Claim/Memory 提交而 Recorded。
2. A Context delivery ACK is weaker than Applied; Applied requires the G/C/H/I/D owner-defined evidence chain and must bind the actual final request boundary where Full Applied is claimed. Architecture invariant I-10 currently says explicit Adapter acknowledgement is required; B proposes clarifying it as a necessary but insufficient condition, with G's complete predicate remaining authoritative. / Context Delivery ACK 弱于 Applied；Applied 要求 G/C/H/I/D 定义的证据链，并且在声称 Full Applied 时必须绑定真实最终请求边界。架构不变量 I-10 当前规定必须有明确 Adapter ACK；B 建议澄清该 ACK 是必要但不充分条件，G 的完整判定谓词仍具有权威性。
3. In the Storage JF-10 candidate, I's COMMIT_WON is an authorization-order decision, not publication. Storage must resolve the same XID and atomically commit VisibilityPointer + PublicationReceipt + outcome + outbox; only after authoritative receipt readback may Storage return PUBLISHED. / 在 Storage JF-10 候选方案中，I 的 COMMIT_WON 是授权顺序决策，不是发布。Storage 必须解析同一 XID，并原子提交 VisibilityPointer + PublicationReceipt + outcome + outbox；只有权威回读 Receipt 后，Storage 才能返回 PUBLISHED。
4. The visibility pointer is the Storage publication authority. Outbox delivery is notification/reconciliation only. / Visibility Pointer 是 Storage 发布权威。Outbox Delivery 仅用于通知/协调。
5. If the result is unknown or in doubt, keep bytes private; do not infer commit/abort from timeout, row absence, stale replica, missing ACK or process death. / 如果结果未知或存疑，必须保持数据私有；不得根据超时、行缺失、过期副本、ACK 缺失或进程死亡推断 Commit/Abort。

Items 2–5 are owner-specific contracts/candidates and must not be promoted to a universal domain transition machine.

第 2–5 项是 Owner 专属契约/候选方案，不得提升为通用领域转换状态机。

## 6. State machine requirements / 状态机要求

Only entities with genuine independent lifecycle require a state machine. A state machine must name:

只有确实具有独立生命周期的实体才需要状态机。状态机必须明确：

- subject type and state dimension; / 主体类型及状态维度；
- initial/terminal states; / 初始状态/终态；
- allowed and forbidden transitions; / 允许和禁止的转换；
- preconditions and authority; / 前置条件和权威；
- required transition evidence; / 转换所需证据；
- idempotency key and same-key/different-payload behavior; / 幂等 Key，以及相同 Key/不同载荷的处理规则；
- failure/unknown semantics; / 失败/未知语义；
- recovery and replay behavior; / 恢复和重放行为；
- supersession/retention behavior. / 替代/保留行为。

No new state machine is introduced for every metadata field. State names without a subject type and owner are invalid as normative contracts.

不得为每个元数据字段都新增状态机。没有主体类型和 Owner 的状态名称，不得作为规范契约。

## 7. Cross-owner decision evidence / 跨 Owner 决策证据

The exact CGH-APPLIED-1.1 recovery-batch package and companion COC architecture have owner decisions recorded: C, D, G, H, I and B accepted their respective semantic portions with enumerated exceptions; Storage confirmed its architecture interface with changes. H/C local L1/L2 validation passed 38 methods, but all ten authority callbacks were deterministic test doubles. This is bounded design/local validation evidence only. Applied Contract Frozen remains NO; production trust, provider-specific idempotency/live provider truth, COC quorum durability, Storage same-GID recovery, G Applied persistence and L3/L4 end-to-end conformance remain NOT VERIFIED / NOT RUN. Issue #3 remains OPEN.

精确版本的 CGH-APPLIED-1.1 Recovery-Batch 套件及配套 COC 架构已有 Owner 决策记录：C、D、G、H、I、B 分别接受其语义部分，并列出例外；Storage 对其架构接口作出带修改的确认。H/C 本地 L1/L2 验证通过 38 个方法，但全部 10 个权威回调均为确定性测试替身。这仅构成有边界的设计/本地验证证据。Applied Contract Frozen 仍为 NO；生产信任、Provider 专属幂等性/实时 Provider 真实性、COC Quorum 持久性、Storage 同 GID 恢复、G Applied 持久化及 L3/L4 端到端一致性仍 NOT VERIFIED / NOT RUN。Issue #3 仍 OPEN。

## 8. Blocking issues / 阻塞问题

- **B-STATE-001:** Fact/Claim ADR remains BLOCKED; epistemic status cannot settle object identity. / Fact/Claim ADR 仍 BLOCKED；认知状态不能决定对象身份。
- **B-STATE-002:** Memory lifecycle and D ForgetOperation phase are distinct; all owner docs and schemas must preserve that split. / Memory 生命周期与 D ForgetOperation 阶段不同；所有 Owner 文档和 Schema 必须保留该区分。
- **B-STATE-003:** Applied predicate remains cross-owner OPEN; B cannot define final request proof or G Applied commit. / Applied 判定谓词仍为跨 Owner OPEN；B 无权定义最终请求证明或 G Applied 提交。
- **B-STATE-004:** I COMMIT_WON vs Storage Published distinction is critical to JF-10; implementation and conformance NOT VERIFIED. / I COMMIT_WON 与 Storage Published 的区分对 JF-10 至关重要；实现和一致性尚 NOT VERIFIED。
- **B-STATE-005:** Forgotten vs Deleted vs Purged/global completion remains D/I/Storage split; do not claim physical erasure from logical state. / Forgotten、Deleted、Purged/全局完成仍由 D/I/Storage 分工；不得从逻辑状态宣称物理擦除。
- **B-STATE-006:** Context/ChangeSet/ContextVersion state transitions need G's exact current Owner contract pin; not yet reconciled here. / Context/ChangeSet/ContextVersion 状态转换需要 G 当前精确 Owner 契约 Pin；本文件尚未完成协调。
- **B-STATE-007:** Architecture invariant I-10 Applied wording may be misread as Adapter ACK sufficient. G requires a complete per-request predicate and exact final-request evidence; A must clarify the global invariant. Until then, ACK alone MUST NOT be promoted to Applied. / 架构不变量 I-10 的 Applied 表述可能被误读为 Adapter ACK 已足够。G 要求完整的逐请求判定谓词和精确最终请求证据；A 必须澄清全局不变量。在此之前，绝不能仅凭 ACK 将状态提升为 Applied。

## 9. Gate status / 门禁状态

B2 is **IN PROGRESS**. This document establishes a typed vocabulary proposal and records exact Owner boundaries; it does not close Owner-specific state machines or approve the cross-owner Applied/Forget/Storage contract. No universal status enum or production schema is authorized.

B2 **进行中**。本文件建立类型化状态词汇提案并记录精确 Owner 权威边界，但不关闭 Owner 专属状态机，也不批准跨 Owner Applied/Forget/Storage 契约。不授权通用状态枚举或生产 Schema。
