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

## 3. Current model vs contract / 当前模型与合同差异

PR #172 currently binds:
- authorization ID
- publication ID
- Storage participant ID
- canonical request/artifact/dependency digest
- Owner Boundary
- Final Visibility Gate Identity
- D admission proof
- I COMMIT_WON proof
- one COMMIT_WON winner per PublicationParticipantRef

The model does **not** yet model the full I authorization tuple as authoritative state.

当前模型尚未把完整 I 授权元组建模为权威状态。

### Missing authority/currentness fields / 缺失字段

At minimum the gap includes:
- issuer and issuer-key status
- principal / actor / workload identity
- delegation chain
- action/resource
- purpose/audience/scope/environment
- PolicyDomainRef
- PermissionEpoch
- current policy/revocation/registry state

当前 revoked set is not equivalent to I's PolicyDomain-local PermissionEpoch/currentness model.

## 4. Proposed next reference-model increment / 下一版参考模型

Introduce an immutable authorization-context record containing, at minimum:

`issuer_ref, principal_ref, workload_ref, actor_ref, delegation_digest, action, resource_ref, purpose, audience, scope_ref, environment_ref, policy_domain_ref, permission_epoch, request_digest, artifact_digest, dependency_digest`

Exact optionality/cardinality must be confirmed against the I normative source before implementation. No semantics are invented here.

建议引入不可变 Authorization Context；具体字段可选性和基数必须再次依据 I 规范确认，不得自行发明语义。

## 5. Required negative tests / 必须新增负向测试

Reject mutation/replay of:
- issuer
- principal
- workload
- actor
- delegation
- action
- resource/artifact
- purpose
- audience
- scope
- environment
- PolicyDomainRef
- PermissionEpoch
- stale/revoked PermissionEpoch
- cross-PolicyDomain PermissionEpoch reuse
- any authorization-context mutation on operation replay

## 6. Required race tests / 必须新增竞态测试

At minimum:
- revocation before I consumption
- revocation after COMMIT_WON but before Storage terminal outcome
- PermissionEpoch advance before consumption
- PermissionEpoch advance after COMMIT_WON
- issuer-key invalidation before consumption
- PolicyDomain currentness becoming UNKNOWN
- replay after authorization-context mutation

UNKNOWN/unverifiable states must remain fail-closed and must not create visibility or disclose protected results.

## 7. Non-invention rule / 禁止自行发明

Do not invent:
- numeric comparison between PermissionEpoch and other Owner high-waters
- global PermissionEpoch ordering
- cross-PolicyDomain comparability
- reset semantics
- cryptographic token serialization
- issuer-key rotation protocol

These remain I/H/Storage decision gates.

## 8. Acceptance boundary / 验收边界

Reference-model closure requires:
- exact I source re-read
- every implemented field mapped to an exact source definition
- all mutation tests pass
- currentness/race tests pass
- bilingual parity
- independent I Owner decision
- D/Storage acceptance of cross-boundary tuple portions

## 9. Current disposition / 当前状态

**CANDIDATE — NOT FROZEN — NOT PRODUCTION AUTHORIZATION**

Issue #25 remains OPEN.

The current 44-test result proves only a bounded deterministic reference model. It does not prove production authorization, cryptographic authenticity, durable DB serialization, multi-process fencing, crash/failover/restore, live D/I/Storage adapters, independent Owner acceptance, or production activation.

## 10. Decision request / 决策请求

I Owner must explicitly confirm whether the 13 protected-boundary authorization fields above are complete for Phase 3.8 derivative publication, or enumerate missing/optional fields.

Until that decision exists, the current reference-model binding must not be promoted into a production authorization contract.
