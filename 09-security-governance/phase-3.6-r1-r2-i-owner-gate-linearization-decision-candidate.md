# Phase 3.6 — I Owner R1/R2 Gate Linearization Decision Candidate
# Phase 3.6 — I Owner R1/R2 Gate 线性化决议候选

- Owner perspective: I — Security & Governance / Permission and Revocation Authority
- Status: **CANDIDATE / NO INDEPENDENT OWNER APPROVAL**
- Source proposal: P-COC-R1-R2-TECH-001, blob `eac0b079f43da8c52521397e0cd256fda3fd3333`
- A review: blob `fdf63550696948f77dc37c0a3788276ac4d525f5`, Issue #14 R1/R2
- Scope: I-owned revocation/request capture, authorization admission, receipt issuance/consumption and I-only outage-gate release.

## 1. I authority and scope key / I 权限与作用域键

I owns the authoritative serialization boundary for each protected authorization scope. The minimum scope key is:
`(PolicyDomainRef, ActionScopeDigest, ResourceScopeDigest, PrincipalOrCapabilityScopeDigest)`.
A request whose scope expands an existing closure MUST increment a monotonic ScopeVersion and invalidate any prior seal whose scope version is older. I must not compare I sequence values with D/C/COC positions.

I 对每个受保护授权作用域拥有权威串行化边界。作用域扩张必须推进单调递增的 ScopeVersion，并使旧版本封印失效。I 的序列值不得与 D/C/COC 位置比较。

## 2. Exact linearization point / 精确线性化点

The I request acceptance operation MUST execute in one I-authoritative serializable transaction or equivalent single-writer CAS/sequencer. It atomically:
1. authenticates issuer and validates PolicyDomain, action/resource scope and immutable request digest;
2. deduplicates by `(IRequestAuthorityRef, IRevocationRequestRef)`; same digest returns the original durable result; changed digest is CONFLICT;
3. appends the request to the I append-only request ledger and allocates the next I-local sequence;
4. advances AcceptedRequestHighWater and ScopeVersion as applicable;
5. closes the affected authorization/receipt-admission gate and increments GateGeneration for a new closure generation;
6. prevents concurrent authorization admission, receipt issuance, receipt consumption and terminal-decision admission from committing through the same serialization boundary.

The durable transaction commit is the I request/gate linearization point. I MUST NOT acknowledge accepted revocation/fence intent before durable commit. A pre-commit read of OPEN followed by an out-of-transaction write is invalid.

I 请求接收必须在 I 权威可串行化事务或等价单写 CAS/Sequencer 中原子完成：认证请求、稳定身份去重、追加请求账本、分配 I 本地序号、推进 HighWater/ScopeVersion、关闭授权与 Receipt Gate，并阻止并发授权准入、Receipt 签发/消费及终态决策准入越过同一串行化边界。事务持久化提交即线性化点；提交前不得确认接收。

## 3. In-flight admission accounting / 在途准入核算

Every I authorization or receipt operation admitted before closure MUST have a durable IAdmissionRef before the caller receives admission success. The row binds operation/request digest, PolicyDomain and scope version, observed GateGeneration, local admission sequence, receipt identity (if allocated), phase and terminal disposition.

At cutoff, I seals both request prefix `[1..H_I]` and admission prefix `[1..F_I]`, with counts, canonical ordered-set digests, roots, query/projection identity and explicit empty flags. Each pre-closure admission must be either:
- joined to the exact committed COC participant and manifest member;
- retained as an owner-local unresolved admission and reconciled in the batch; or
- proven rejected before any protected authorization/receipt effect.

Missing rows, incomplete pagination, stale replica, unknown key status or unavailable anti-rollback checkpoint means INCOMPLETE/UNKNOWN, never empty.

## 4. Seal and release CAS / 封印与释放 CAS

The I seal is immutable and binds PolicyDomain/scope, GateGeneration, ScopeVersion, request high-water, in-flight admission high-water, counts, roots/digests, anti-rollback anchor and key-status generation. New requests accepted after the seal receive a higher sequence and remain blocked; they require a subsequent Recovery Cutoff Batch.

I may release only its own outage-admission gate, using a durable CAS requiring current GateGeneration, ScopeVersion, AcceptedRequestHighWater and InFlightAdmissionHighWater to equal the sealed values (or later work to be explicitly proven rejected/no-effect and accounted). Every request through H_I and every admission through F_I must have exact owner disposition and Batch/Manifest join. Any changed value fails release and requires a successor seal/batch. COC cannot release I's gate.

I 只能释放自己的 outage-admission gate；CAS 必须核对封印中的 GateGeneration、ScopeVersion、请求及在途准入 HighWater。任一值变化即释放失败并要求后续 Batch。COC 不得代替 I 释放 Gate。

## 5. Terminality and non-equivalence / 终态边界

Outage-gate release is not authorization grant, revocation reversal, PermissionEpoch rollback or proof that every request is effective. Effective revocation remains governed by I's authoritative permission state machine. UNKNOWN/IN_DOUBT, stale key state, incomplete inventory or unresolved receipt consumption keeps the affected scope blocked.

## 6. Required evidence and tests / 必需证据与测试

Required owner-local evidence: durable request ledger; durable admission ledger; serializable request-vs-admission race test; duplicate-same-digest idempotency; duplicate-different-digest conflict; high-water advance during reconciliation; scope expansion invalidating a seal; crash/restart after commit-before-ACK; owner-only release CAS; and negative proof that missing ledger rows cannot produce COMPLETE_EMPTY.

## 7. Decision boundary / 决议边界

This document is a coordinator-authored I-role candidate, not a genuine independent I Owner signature or approval. I must independently adopt/amend/reject it on its own branch and pin the exact source blobs. The sequencer, durable ledgers, signer/key registry, anti-rollback anchor, currentness CAS and executable fault tests are NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED. No Gate B/C or production activation is implied.
