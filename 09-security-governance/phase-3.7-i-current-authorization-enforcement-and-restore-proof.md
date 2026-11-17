# Phase 3.7 — I Current Authorization Enforcement and Restore Proof

- Owner: I — Security, Identity and Governance
- Status: I semantic enforcement proposal; token schema and conformance OPEN
- Issue: #21
- English and Chinese are normative peers.

## 1. Decision (EN)
I owns principal/workload trust, authorization, PolicyDomain and PermissionEpoch currentness, revocation, and global Forget policy/completion. PermissionEpoch is opaque and local to one I-registered PolicyDomain; it is never a global sequence and is never numerically compared with D, COC, Storage, F or G positions.

At each protected boundary, verify authenticated issuer and principal/workload/actor, delegation chain, action, resource, purpose, audience, Scope, Environment, PolicyDomainRef, I-issued PermissionEpoch, current policy/revocation/registry state and exact request/work-item/artifact/region binding. Payload-supplied identity, producer, source, scope, environment or permission_epoch values are untrusted assertions and cannot create authorization.

Revalidate current I authorization before producer admission and source dereference; queue lease and worker execution; materialization and dependency registration; derivative publication; Recall final return/handoff; Context dispatch, Adapter apply and C provider submit; restore replay, rebuild, reconnect and serving enablement. Cached ALLOW or historical receipt is not perpetual authority. Any bounded cache profile requires a separate I-approved maximum age, invalidation propagation, PolicyDomain scope and fail-closed rule. Without it, verify current I state at every protected boundary. Unknown, stale, gapped, revoked, incomparable, unverifiable or indeterminate means DENY/PAUSE and quarantine.

Restore requires an I-signed current proof per PolicyDomain covering policy currentness, revocation continuity, principal/workload registry continuity and relevant audience/scope. I does not mint a composite Storage/COC/D/F/G high-water and cannot grant serving alone. Historical authorization may remain audit evidence; current-use eligibility is recomputed against current I and independent D fence/lineage. I permission never overrides D ForgetFence; D clearance never substitutes for I permission. I alone governs global Forget completion.

## 2. 中文规范
I 管理主体/工作负载信任、授权、PolicyDomain 与 PermissionEpoch 当前性、撤权及 Global Forget 策略/完成。PermissionEpoch 是单个 I-registered PolicyDomain 内的不透明值，不是全局序列，禁止与 D、COC、Storage、F 或 G 的位置做数值比较。

每个受保护边界必须验证经认证的 Issuer 和 Principal/Workload/Actor、Delegation Chain、Action、Resource、Purpose、Audience、Scope、Environment、PolicyDomainRef、I 签发的 PermissionEpoch、当前 Policy/Revocation/Registry，以及精确 Request/WorkItem/Artifact/Region 绑定。Payload 自带身份、Producer、Source、Scope、Environment 或 permission_epoch 都是不可信声明，不能创建授权。

当前 I 授权必须在 Producer 准入/源读取、Queue Lease/Worker 执行、物化/依赖注册、Derivative 发布、Recall 最终返回/交接、Context Dispatch/Adapter Apply/C Provider Submit，以及 Restore Replay/Rebuild/Reconnect/Serving 启用前重新验证。缓存 ALLOW 或历史 Receipt 不是永久授权。任何有界缓存策略必须由 I 另行批准最大时效、失效传播、PolicyDomain 范围和 fail-closed 规则；未批准时，每个受保护边界都必须验证 I 当前状态。未知、陈旧、有缺口、已撤销、不可比较、不可验证或不确定状态一律 DENY/PAUSE 并隔离。

Restore 必须按 PolicyDomain 提供 I 签发的当前证明，覆盖 Policy 当前性、Revocation 连续性、Principal/Workload Registry 连续性及相关 Audience/Scope。I 不签发合并 Storage/COC/D/F/G 的 High-water，也不能单独授予 Serving。历史授权可保留为审计证据；当前使用资格必须根据 I 当前状态和独立 D Fence/Lineage 重新计算。I 授权不能覆盖 D ForgetFence；D Clearance 不能替代 I Permission。只有 I 管理 Global Forget 完成。

## 8. I final-visibility authorization for D/E derivative publication

I confirms derivative publication is a protected irreversible visibility operation. A cached ALLOW or PermissionEpoch snapshot is insufficient. The actual Storage visibility gate must participate in I's PolicyDomain sequencer under the existing CommitAuthorizationReceipt semantics.

For each publication, I's single-use receipt and terminal proof must bind: PolicyDomainRef/current PermissionEpoch/current issuer-key status; authenticated producer Principal/Actor/workload and delegation; action=derivative publication; exact DerivedArtifactRef/version; purpose/audience/Scope/Environment; PublicationOperationId and canonical request/artifact/dependency digest; D PublicationParticipantRef and fence/lineage binding; exact StorageVisibilityParticipantRef, owner boundary and final visibility gate identity.

I consumes the receipt once in its authoritative PolicyDomain sequencer and returns COMMIT_WON, REVOCATION_WON or UNKNOWN/IN_DOUBT. The terminal proof is bound to the exact publication and cannot be replayed for another artifact, digest, scope, attempt or Storage participant.

Ordering:
1. Revocation sequenced before receipt consumption => REVOCATION_WON; Storage must not expose the artifact.
2. Receipt consumption terminalized COMMIT_WON first => I records the publication participant unresolved and holds a later effective revocation epoch advance until Storage reports COMMITTED_VISIBLE or authoritative NO_PUBLICATION.
3. Storage COMMITTED_VISIBLE => I closes that exact participant; later revocation may advance and invalidate current-use according to policy without rewriting historical publication.
4. Storage NO_PUBLICATION => I closes the participant as safely aborted; pending revocation may advance.
5. UNKNOWN/IN_DOUBT => participant and affected revocation remain unresolved. Timeout, missing row, lease expiry or process death never releases the I gate.

I does not decide D ForgetFence. D independently holds its PublicationParticipantRef against later Fence effectiveness. Storage visibility requires both current D clearance and I terminal authorization, each verified in its own authority namespace. COMMIT_WON is ordering evidence, not a standalone permission to write visibility after participant binding changes.

This extends the I owner contract to derivative publication; cryptographic algorithms, token serialization and Storage technology remain open I/H/Storage freeze gates.

### 中文规范

I 确认 Derivative Publication 属于受保护的不可逆可见性操作。缓存 ALLOW 或 PermissionEpoch 快照不足以授权。实际 Storage Visibility Gate 必须按既有 CommitAuthorizationReceipt 语义参与 I PolicyDomain Sequencer。

每次发布的单次 Receipt 和 Terminal Proof 必须绑定 PolicyDomainRef/当前 PermissionEpoch/Issuer-Key Status、经认证 Producer Principal/Actor/Workload 与 Delegation、Derivative Publication Action、精确 DerivedArtifactRef/Version、Purpose/Audience/Scope/Environment、PublicationOperationId 与规范 Request/Artifact/Dependency Digest、D PublicationParticipantRef/Fence/Lineage，以及精确 StorageVisibilityParticipantRef、Owner Boundary 和最终 Visibility Gate 身份。

I 在自己的权威 PolicyDomain Sequencer 中单次消费 Receipt，并返回 COMMIT_WON、REVOCATION_WON 或 UNKNOWN/IN_DOUBT。证明绑定精确 Publication，不得跨 Artifact、Digest、Scope、Attempt 或 Storage Participant 重放。

顺序规则：
1. Revocation 先于 Receipt Consumption 提交，则 REVOCATION_WON，Storage 不得暴露 Artifact。
2. Receipt Consumption 先终态为 COMMIT_WON，则 I 将 Publication Participant 记为未解决，并让后续有效 Revocation Epoch Advance 等待 Storage 报告 COMMITTED_VISIBLE 或权威 NO_PUBLICATION。
3. Storage COMMITTED_VISIBLE 后，I 关闭该 Participant；后续 Revocation 可以推进并按策略使当前使用资格失效，但不改写历史发布事实。
4. Storage NO_PUBLICATION 后，I 以安全中止关闭 Participant；等待中的 Revocation 可以推进。
5. UNKNOWN/IN_DOUBT 时，Participant 和受影响 Revocation 均保持未解决。超时、行缺失、租约过期或进程死亡绝不释放 I Gate。

I 不决定 D ForgetFence。D 独立保持 PublicationParticipantRef，阻止后续 Fence 越过未解决发布。Storage Visibility 必须同时验证 D 当前 Clearance 和 I Terminal Authorization，且分别在各自权威命名空间内验证。COMMIT_WON 是顺序证据，不是 Participant 绑定改变后独立写入 Visibility 的许可。

本修订将 I 既有合同扩展至 Derivative Publication；密码算法、Token 序列化和 Storage 技术仍属于 I/H/Storage 冻结门槛。
