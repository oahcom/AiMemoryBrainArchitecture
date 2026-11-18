# Phase 3.8 Integration Addendum — I Full Authorization Tuple Gap
# Phase 3.8 集成补充 — I 完整授权元组缺口

**Status / 状态:** CANDIDATE / 候选  
**Owner:** Integration Owner  
**Issue:** #25

## 1. Evidence baseline / 证据基线

Exact I source reviewed:
- Branch: `session-i-security-governance-2026-11-16`
- Path: `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md`
- Blob: `e3b1b5d99eb36ac0b395854d8c19287d2b64b752`

Latest reference-model correction:
- PR #172 Head: `6f231976ef665e5c961f467e0cc0e931ae708349`
- Publication Protocol run #44196418535: 44/44 SUCCESS
- GOV-DOC-001 run #44196418676: SUCCESS

PR #172 is a provisional fail-closed reference-model invariant, not independent Owner approval or production conformance.

## 2. Exact I authorization tuple / I 精确授权元组

The I contract requires protected-boundary verification of:

1. authenticated issuer
2. Principal / Workload / Actor
3. Delegation chain
4. Action
5. Resource
6. Purpose
7. Audience
8. Scope
9. Environment
10. PolicyDomainRef
11. I-issued PermissionEpoch
12. current policy/revocation/registry state
13. exact Request / WorkItem / Artifact / Region binding

I 合同要求受保护边界验证以上 13 项。

## 3. Corrected coverage assessment / 修正后的覆盖评估

A source-level re-read shows that the current reference model already represents many of these fields inside its immutable test-seam authorization context:

- Principal: `principal_ref`
- Workload: `workload_binding_ref`
- Actor: `actor_ref`
- Delegation: `delegation_chain_ref`
- Action: `action`
- Resource: `resource_ref`
- Purpose: `purpose`
- Audience: `audience`
- Scope: `scope_binding_digest`, `ownership_scope_ref`, `applicability_scope_set_digest`
- Environment: `environment_ref`
- PolicyDomain: `policy_domain_id`
- PermissionEpoch: `permission_epoch`
- Request-level binding: `operation_payload_digest` plus the publication request digest
- Producer/adapter/session bindings: represented by explicit test-seam fields

因此，不能再把“这些字段完全不存在”作为当前结论。

The remaining gap is more precise: these fields are currently **test-seam values/defaults**, not a demonstrated authoritative I state with authenticated issuer/key status, current policy/revocation/registry continuity, and exact Artifact/Region semantics. The reference model also does not yet prove that every protected boundary revalidates the same authoritative tuple.

当前真正的缺口不是字段名称不存在，而是这些字段目前只是**测试接缝值/默认值**，尚未证明它们来自 I 权威状态，也未证明 Issuer/Key Status、当前 Policy/Revocation/Registry 连续性、精确 Artifact/Region 语义以及所有受保护边界的重新验证。

### Remaining authority/currentness gaps / 剩余权威与当前性缺口

1. Authenticated issuer identity and issuer-key status are not modeled as authoritative state.
2. Current policy state and registry currentness are not modeled as authoritative state.
3. Revocation is represented by a simple local revoked set, not the full I PolicyDomain currentness contract.
4. ArtifactRef/version and Region binding are not independently modeled as I-authoritative tuple members.
5. The model does not yet prove that the same authoritative authorization context is revalidated at every protected boundary.
6. Restore proof, registry continuity and key-currentness are not executable in this reference model.

1. 经认证 Issuer 身份及 Issuer-Key Status 尚未建模为 I 权威状态。
2. 当前 Policy 状态及 Registry Currentness 尚未建模为 I 权威状态。
3. 当前 Revocation 只是简单 revoked set，不等价于完整 I PolicyDomain 当前性合同。
4. ArtifactRef/Version 与 Region 尚未作为 I 权威元组成员独立建模。
5. 尚未证明所有受保护边界都重新验证同一份 I 权威授权上下文。
6. Restore Proof、Registry Continuity 与 Key Currentness 尚未进入可执行参考模型。

## 4. Proposed next reference-model increment / 下一版参考模型

Do **not** blindly add another large field list.

First add an explicit authoritative I state seam containing, at minimum:

`issuer_ref, issuer_key_status, policy_domain_ref, current_policy_ref, current_permission_epoch, revocation_registry_state, principal_registry_state`

Then bind the existing authorization context to the exact operation/artifact/region tuple once the I Owner confirms the canonical representations.

不要继续盲目增加字段。

下一步首先应引入显式 I 权威状态接缝，至少包含：

`issuer_ref, issuer_key_status, policy_domain_ref, current_policy_ref, current_permission_epoch, revocation_registry_state, principal_registry_state`

然后，在 I Owner 确认规范表示后，把现有 Authorization Context 绑定到精确 Operation/Artifact/Region 元组。

Exact optionality/cardinality and cryptographic semantics must be confirmed against the I normative source before implementation. No semantics are invented here.

## 5. Required negative tests / 必须新增负向测试

Reject mutation/replay of:

- issuer
- issuer-key status
- principal
- workload
- actor
- delegation
- action
- resource
- artifact/version
- purpose
- audience
- scope
- environment
- PolicyDomainRef
- PermissionEpoch
- current policy reference
- revocation/registry currentness
- region binding
- any authorization-context mutation on operation replay

## 6. Required race tests / 必须新增竞态测试

At minimum:

- revocation before I consumption
- revocation after COMMIT_WON but before Storage terminal outcome
- PermissionEpoch advance before consumption
- PermissionEpoch advance after COMMIT_WON
- issuer-key invalidation before consumption
- policy revision change before consumption
- principal/workload registry invalidation before consumption
- PolicyDomain currentness becoming UNKNOWN
- artifact/version substitution
- region substitution
- replay after authorization-context mutation

UNKNOWN/unverifiable states must remain fail-closed and must not create visibility or disclose protected results.

## 7. Protected-boundary revalidation / 受保护边界重新验证

The I source requires current authorization revalidation before producer admission, queue/worker execution, materialization/dependency registration, derivative publication, Recall final handoff, Context dispatch/Adapter apply/C provider submit, and restore/rebuild/reconnect/serving enablement.

The reference model currently proves final publication sequencing, but does not yet prove this full boundary matrix.

I 源规范要求在 Producer Admission、Queue/Worker、Materialization/Dependency Registration、Derivative Publication、Recall Final Handoff、Context Dispatch/Adapter Apply/C Provider Submit 以及 Restore/Rebuild/Reconnect/Serving Enablement 前重新验证当前授权。

当前参考模型已经证明最终 Publication Sequencing，但尚未证明完整边界矩阵。

## 8. Non-invention rule / 禁止自行发明

Do not invent:

- numeric comparison between PermissionEpoch and other Owner high-waters
- global PermissionEpoch ordering
- cross-PolicyDomain comparability
- reset semantics
- cryptographic token serialization
- issuer-key rotation protocol
- canonical Region semantics
- ArtifactRef/version semantics not present in the I contract

These remain I/H/Storage decision gates.

## 9. Acceptance boundary / 验收边界

Reference-model closure requires:

- exact I source re-read
- every modeled field mapped to an exact source definition
- authoritative currentness state represented separately from test defaults
- all mutation tests pass
- currentness/race tests pass
- protected-boundary revalidation matrix is executable
- bilingual parity
- independent I Owner decision
- D/Storage acceptance of cross-boundary tuple portions

## 10. Current disposition / 当前状态

**CANDIDATE — NOT FROZEN — NOT PRODUCTION AUTHORIZATION**

Issue #25 remains OPEN.

The current 44-test result proves a bounded deterministic publication reference model. It does not prove production authorization, cryptographic authenticity, durable DB serialization, multi-process fencing, crash/failover/restore, live D/I/Storage adapters, independent Owner acceptance, or production activation.

## 11. Decision request / 决策请求

I Owner must explicitly confirm:

1. canonical representation of issuer/key status;
2. canonical current policy and revocation/registry state;
3. ArtifactRef/version and Region binding semantics;
4. whether the listed protected-boundary revalidation points are complete;
5. which fields are required vs optional;
6. which values must be cryptographically authenticated.

Until those decisions exist, the reference model must not promote test-seam authorization context into a production authorization contract.
