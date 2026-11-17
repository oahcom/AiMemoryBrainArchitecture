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
