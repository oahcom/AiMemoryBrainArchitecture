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
