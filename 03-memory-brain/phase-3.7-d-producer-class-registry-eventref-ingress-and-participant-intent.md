# Phase 3.7 — D Producer Registry, EventRef Ingress and Participant Intent

- Owner: D — Canonical Memory / ForgetFence / Lineage
- Status: D semantic boundary proposal; callable schema and implementation OPEN
- Issue: #21
- English and Chinese are normative peers.

## 1. D decisions (EN)
D is the sole authority for canonical Memory admission, ProducerClass registry, producer ledger, dependency/lineage inventory, ForgetFence and producer-barrier disposition. E/F/G local producer declarations never grant admission.

1. Every derivative-capable work item requires an enabled, versioned D ProducerClass and durable D RegistrationReceipt before queueing, leasing, protected source dereference, execution, retry/replay or publication.
2. Producer registration and ForgetFence admission share a linearizable D admission/barrier domain. A fence snapshot accounts for all earlier admitted producers; affected later work is rejected or quarantined.
3. Every immutable derivative registers complete direct and transitive dependencies before visibility.
4. Only D accepts terminal-no-publication evidence and closes its barrier. DLQ, timeout, missing row, lease expiry, worker death and local cancel are insufficient.
5. EventRef-only ingress before canonical Memory exists is quarantined metadata, not D admission. E acceptance is not D registration.
6. C provider submit requires an exact D ParticipantIntentRef admitted into the causal participant barrier and bound to immutable request/digest, G ContextId/ContextVersion, DeliveryId/Attempt, region digest, Adapter/session, Scope/Environment and I authorization evidence. G DeliveryId and H ACK are not substitutes.

## 2. ProducerClass Registry
Each immutable registry version identifies ProducerClassId, owner/workload identity, accepted source-reference classes, output/derivative classes, allowed capabilities (normal, replay, rebuild, cleanup-only), enabled state, effective registry epoch and applicable Scope/PolicyDomain constraints. Registry eligibility is not a work registration. A separate RegistrationReceipt binds stable ProducerWorkItemId, request digest, source refs, Scope, known lineage, admission position and observed fence. Same identity+digest is idempotent; changed digest is conflict; unknown result blocks.

## 3. EventRef-only ingress
Before canonical Memory exists, an EventRef may be stored only as QuarantinedIngressRef. It is not a canonical Memory ref, RegistrationReceipt, dependency registration or barrier participant and grants no protected dereference, queue, execution, publication or replay permission. A future PreCanonicalIngressRegistration requires a separate versioned D contract covering source trust, identity, scope, policy, lineage placeholder, fence participation, deduplication, expiry and terminalization. Until then E stops at quarantined metadata.

## 4. ParticipantIntentRef and terminality
C must present the exact D-admitted ParticipantIntentRef before provider submit. Missing, stale, mismatched, revoked or unknown bindings block submit. G cannot mint/infer it; H only transports it. D accepts terminal-no-publication only when evidence proves no worker, lease, retry, replay, staged artifact, outbox or delayed publisher can later publish. This semantic proposal does not freeze wire schema or prove Storage/C crash safety.

## 5. 中文规范
D 是 Canonical Memory 准入、ProducerClass Registry、Producer Ledger、Dependency/Lineage 清单、ForgetFence 和 Producer Barrier 终态处置的唯一权威。E/F/G 本地 Producer 声明不构成准入授权。

1. 每个 Derivative-capable WorkItem 必须由启用且版本化的 D ProducerClass 覆盖，并在入队、租约、受保护源读取、执行、重试/重放或发布前取得持久化 D RegistrationReceipt。
2. Producer 注册与 ForgetFence 准入必须处于 D 线性一致的 Admission/Barrier 域。Fence 快照覆盖此前所有已准入 Producer；之后受影响工作必须拒绝或隔离。
3. 每个不可变 Derivative 在可见前必须注册完整直接及传递依赖。
4. 只有 D 接受 TerminalNoPublication 证据并关闭 Barrier。DLQ、超时、行缺失、租约过期、Worker 死亡和本地取消均不足。
5. Canonical Memory 形成前的 EventRef-only 入口只能作为隔离元数据，不能视为 D 准入。E Accepted 不等于 D Registered。
6. C Provider Submit 前必须有精确 D ParticipantIntentRef，已进入因果 Participant Barrier，并绑定不可变 Request/Digest、G ContextId/ContextVersion、DeliveryId/Attempt、Region Digest、Adapter/Session、Scope/Environment 和 I 授权证据。G DeliveryId 与 H ACK 不可替代。

ProducerClass 每个不可变版本必须标识 ProducerClassId、Owner/Workload 身份、允许的 SourceRef 类型、输出/Derivative 类型、normal/replay/rebuild/cleanup-only 能力、启用状态、生效 Registry Epoch 和 Scope/PolicyDomain 约束。Registry 资格不等于 Work 注册；单独的 RegistrationReceipt 绑定稳定 WorkItemId、请求摘要、源引用、Scope、已知 Lineage、准入位置和观测 Fence。同身份同摘要幂等；同身份不同摘要冲突；结果未知时阻断。

Canonical Memory 形成前，EventRef 只能保存为 QuarantinedIngressRef。它不是 Canonical Memory Ref、RegistrationReceipt、Dependency Registration 或 Barrier Participant，也不授予受保护解引用、入队、执行、发布或重放权限。未来 PreCanonicalIngressRegistration 必须由 D 另行版本化，明确源信任、身份、Scope、Policy、Lineage 占位、Fence 参与、去重、过期和终态化。此前 E 只能停留在隔离元数据。

C 必须在 Provider Submit 前提交精确 D-admitted ParticipantIntentRef。绑定缺失、陈旧、不匹配、撤销或未知均阻断 Submit。G 不得制造/推断；H 只能传输。只有证据证明 Worker、Lease、Retry、Replay、Staged Artifact、Outbox 或延迟 Publisher 均不可能再发布时，D 才接受 TerminalNoPublication。本提案不冻结 Wire Schema，也不证明 Storage/C 崩溃安全。


## 8. Normative correction — EventRef-only ProducerWork admission

Exact cross-check against D's controlling forget-fence-operation-and-publication-gate.md (Blob 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5), §3.2, shows D already permits ProducerWork registration before a Canonical MemoryRef exists. The earlier blanket statement that EventRef-only ingress is never D admission is withdrawn.

1. D-registered EventRef-only work is permitted. D may issue a durable RegistrationReceipt for a stable ProducerWorkItemId using the immutable EventRef, authenticated producer binding, enabled ProducerClass/version, exact Scope, canonical request digest and D-approved opaque lineage token/digest. It receives a normal D ProducerRegistrationSequence and is included in a later ForgetFence barrier high-water.
2. Registration is not unrestricted source access. The receipt grants only explicitly named capabilities. Protected payload dereference still requires current I authorization and source-access policy at that boundary.
3. Before dependency registration or publication, E must append/link exact Canonical MemoryRef/MemoryVersionRef identities and revisions to the original EventRef lineage. Missing, conflicting or unresolvable lineage remains quarantined and non-publishable.
4. Barrier coverage begins at D registration. A later ForgetFence includes this work when its registration sequence is at/below the captured high-water. EventRef-only cannot bypass the D barrier.
5. Missing/invalid producer authentication, disabled/unknown class, unresolved Scope, absent approved lineage token, digest conflict or unknown D/I state yields REJECTED/QUARANTINED with no queue/lease/execute capability.
6. E AcceptedReceipt remains E-local and never implies D registration. D RegistrationReceipt is mandatory before derivative-capable work is queued, leased or executed.

### 中文规范

经精确核对 D 既有权威合同 forget-fence-operation-and-publication-gate.md（Blob 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5）§3.2，D 已允许 Canonical MemoryRef 形成前注册 ProducerWork。因此撤销此前“EventRef-only 永远不能成为 D Admission”的一刀切表述。

1. 允许 D 注册 EventRef-only Work。D 可基于不可变 EventRef、经认证 Producer Binding、启用的 ProducerClass/Version、精确 Scope、规范请求摘要及 D 批准的不透明 Lineage Token/Digest，为稳定 ProducerWorkItemId 签发持久化 RegistrationReceipt。该工作取得正常 D ProducerRegistrationSequence，并纳入后续 ForgetFence Barrier High-water。
2. 注册不等于无限制读取源数据。Receipt 只授予明确列出的能力；受保护 Payload Dereference 仍须在对应边界验证 I 当前授权和源访问策略。
3. Dependency Registration 或 Publish 前，E 必须把精确 Canonical MemoryRef/MemoryVersionRef 身份和 Revision 追加关联到原 EventRef Lineage。Lineage 缺失、冲突或无法解析时必须隔离且不可发布。
4. Barrier 从 D 注册时开始覆盖。后续 ForgetFence 在 High-water 覆盖该 RegistrationSequence 时必须纳入该 Work。EventRef-only 不得绕过 D Barrier。
5. Producer 身份认证缺失/无效、Class 未知或禁用、Scope 未解析、无批准 Lineage Token、摘要冲突或 D/I 状态未知，都必须 REJECTED/QUARANTINED，不授予 Queue/Lease/Execute 能力。
6. E AcceptedReceipt 只是 E 本地证据，绝不意味着 D 已注册。Derivative-capable Work 入队、租约或执行前，D RegistrationReceipt 仍是硬前置条件。

## 9. D/E/Storage atomic registration-to-visibility boundary

D reaffirms the nine semantic operations in its controlling contract. D owns their meanings and decisions; Storage owns the durable transaction/serialization and authoritative visibility mechanism; E owns compiler work/attempt/lease/private stage/output accounting. The shared serialization domain must cover RegisterProducerWork, InstallForgetFence with immutable registry/work high-water, complete RegisterDerivedDependency, PublishDerivedIfFenceCurrent with visibility flip, and CompleteProducerWork.

Registration and fence have exactly two legal outcomes. Dependency registration is complete-set atomic. Publication becomes visible only at the same authoritative commit that validates the latest D fence, current I authorization, D registration, complete dependencies, current attempt/lease, Scope and exact artifact digest. If the D ledger and visibility authority cannot join one ACID transaction, D must approve a durable prepare/commit or equivalent linearizable protocol. A reusable D token followed by an independent Storage write is prohibited. The final visibility commit must validate/consume the exact D decision against the current fence; ambiguous/prepared state remains hidden across crash, failover and restore.

### 中文规范

D 重申既有权威合同定义的九项语义操作。D 管理其语义和决策；Storage 管理持久化事务/序列化及权威可见性机制；E 管理 Compiler Work/Attempt/Lease/Private Stage/Output Accounting。共享序列化域必须覆盖 RegisterProducerWork、带不可变 Registry/Work High-water 的 InstallForgetFence、完整 RegisterDerivedDependency、与 Visibility Flip 绑定的 PublishDerivedIfFenceCurrent，以及 CompleteProducerWork。

注册与 Fence 只有两种合法结果；Dependency Registration 必须完整集合原子提交。只有在同一权威提交中验证最新 D Fence、I 当前授权、D Registration、完整依赖、当前 Attempt/Lease、Scope 和精确 Artifact Digest 后，Derivative 才可见。若 D Ledger 与 Visibility Authority 无法加入同一 ACID 事务，必须由 D 批准持久化 Prepare/Commit 或等效线性一致协议。禁止可重复使用的 D Token 后接独立 Storage 写入。最终 Visibility Commit 必须针对当前 Fence 验证/消费精确 D 决策；崩溃、Failover 和 Restore 后，歧义/Prepared 状态仍须保持隐藏。

## 10. D publication participant — order the ForgetFence race before physical visibility

D adds a durable, D-owned PublicationParticipantRef as a pre-visibility barrier participant for each protected derivative publication. It is not a PublicationReceipt and does not make an artifact visible.

The D admission binds PublicationOperationId + canonical request digest, ProducerWorkItemId/RegistrationReceipt, DerivedArtifactRef/version, complete dependency/lineage digest, Scope, active AttemptId/LeaseId, ProducerClass/version and exact target/source ancestry. D admits it only after complete dependency registration and a current D fence check in the same serialization domain used by InstallForgetFence.

- If D ForgetFence wins before this participant is admitted, D rejects/quarantines the publication; no Storage visibility commit is permitted.
- If the publication participant is admitted first, D records it as unresolved in the D barrier. A later fence request may be recorded, but cannot become effective past this participant until Storage proves COMMITTED_VISIBLE or authoritative NO_PUBLICATION. This is an in-flight ordering hold, not publication permission.
- Storage final visibility commit must validate the exact active PublicationParticipantRef and current D barrier state.
- Storage COMMITTED_VISIBLE proof lets D terminalize the participant and account the derivative in fence inventory. Authoritative NO_PUBLICATION closes it without a derivative. UNKNOWN/IN_DOUBT keeps the D barrier open and artifact private.
- D signs terminal/clearance evidence only after authoritative Storage outcome readback. Queue/worker/transport ACK is not terminal evidence.

The I gate is independent and conjunctive: I's single-use authorization receipt/terminal decision must bind the same PublicationOperationId/digest and exact Storage visibility participant. D PublicationParticipantRef grants no I authorization; I COMMIT_WON does not bypass D Fence.

### 中文规范

D 为每次受保护 Derivative 发布增加持久化、由 D 管理的 PublicationParticipantRef，作为可见前 Barrier Participant。它不是 PublicationReceipt，也不会让 Artifact 可见。

D 准入时绑定 PublicationOperationId/规范请求摘要、ProducerWorkItemId/RegistrationReceipt、DerivedArtifactRef/Version、完整 Dependency/Lineage Digest、Scope、活动 AttemptId/LeaseId、ProducerClass/Version 及精确 Target/Source Ancestors。只有完整依赖登记完成，并在与 InstallForgetFence 相同的序列化域内验证当前 D Fence 后，D 才准入。

- 若 D ForgetFence 先于该 Participant 准入，D 必须拒绝/隔离发布，不允许 Storage Visibility Commit。
- 若 Publication Participant 先准入，D 将其记录为未解决 Barrier Participant。之后的 Fence 请求可以记录，但在 Storage 证明 COMMITTED_VISIBLE 或权威 NO_PUBLICATION 前，不得越过该 Participant 生效。这只是进行中操作的顺序保持，不是发布许可。
- Storage 最终 Visibility Commit 必须验证精确且仍活动的 PublicationParticipantRef 与当前 D Barrier 状态。
- Storage COMMITTED_VISIBLE 证明使 D 终态化该 Participant 并将 Derivative 纳入 Fence Inventory；权威 NO_PUBLICATION 使 D 在无 Derivative 情况下关闭 Participant；UNKNOWN/IN_DOUBT 保持 D Barrier 开放且 Artifact Private。
- D 只有在权威 Storage Outcome 回读后才签发终态/清除证明。Queue/Worker/Transport ACK 均不是终态证据。

I Gate 独立且必须合取满足：I 的单次授权 Receipt/Terminal Decision 必须绑定相同 PublicationOperationId/Digest 和精确 Storage Visibility Participant。D PublicationParticipantRef 不授予 I Authorization；I COMMIT_WON 也不能绕过 D Fence。
