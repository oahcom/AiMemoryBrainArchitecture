---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# AID-2026-001 — Joined Forget / Memory Lifecycle Contract Proposal v1
# AID-2026-001 — Forget / Memory 生命周期联合契约提案 v1

- Work Item: AID-2026-001
- Classification: ARCH / R3
- Status: PROPOSED — NOT NORMATIVE UNTIL D/I APPROVAL
- Prepared roles: Owner D (canonical lifecycle semantics), Owner I (security/governance policy), with execution-boundary input from E/F/G/H/C/Storage
- Related authority baseline: `14-ai-development/work-items/AID-2026-001/owner-d-i-forget-authority-matrix.md` (PROPOSED; not Owner approval)
- Baseline: PR #42 Base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`, reviewed Head `3fb10eef38d88b83b48edf5e2818e2ca5ae8ee9e`
- This proposal is a remediation artifact. It does not assert that the named Owners or acceptance authority have approved it.

## 1. Purpose and non-negotiable invariants

This document proposes one joined contract to close D-F01 through D-F04. It separates canonical domain meaning, security/governance authority, execution, and evidence. It is deliberately a proposal pending explicit D and I approval.

1. A Memory lifecycle state is not a Forget operation phase.
2. `Forgotten` is terminal for the canonical content identity and means that a durable suppression decision has linearized; it does not mean physical erasure or global Forget completion.
3. A Forget operation is not complete merely because a tombstone, adapter ACK, queue ACK, cache invalidation, or one storage deletion succeeded.
4. Unknown, unreachable, unsupported, failed, or unregistered-but-required targets never count as successful completion.
5. Once suppression has linearized, retries and failures must never restore ordinary access. There is no rollback to Active/Archived and no cancellation that removes the fence.
6. Security authorization and retention/legal-hold policy are I-owned; canonical Memory lifecycle and Forget operation/fence semantics are D-owned.
7. Every irreversible stage re-checks current authorization and applicable policy immediately before execution.
8. Every completion claim is derived from a sealed, versioned inventory and per-target evidence, under I-owned aggregation policy.

## 2. Authority and responsibility matrix (D-F01)

| Decision / action | Accountable owner | Required participants / evidence |
|---|---|---|
| Memory lifecycle vocabulary and legal transitions | D | Runtime/MCM consumers acknowledge |
| Canonical ForgetOperation identity, phase model, event ordering and transition invariants | D | I approves governance boundary; E/Storage confirm durable execution seams |
| ForgetFence generation, canonical suppression linearization point and tombstone semantics | D | Storage confirms atomic durability; E/F/G/H confirm enforcement points |
| Actor authentication, authorization, delegation, revocation and PermissionEpoch policy | I | H binds authenticated transport principal; each executor re-checks |
| Subject/Scope eligibility, purpose, consent, retention and legal-hold decision | I | D supplies typed target references; domain owners supply ownership/applicability |
| Global target-inventory policy, required target classes and inventory sealing criteria | I | D defines dependency-inventory contract; E/F/G/H/C/Storage register owned targets |
| Per-target action semantics and local capability result | Owning execution domain | E/F/G/H/C/Storage; each emits signed/traceable evidence within its trust boundary |
| D-domain completion predicate | D | I reviews security implications but cannot redefine the predicate; D-owned transition/conformance evidence |
| Cross-system evidence evaluation, governance compliance and policy exceptions | I | D supplies canonical D-domain state/predicate; target owners supply capability-bounded evidence |
| Agent telemetry or model inference | C | May propose/observe; cannot authenticate, authorize, mutate lifecycle or declare Forget complete |
| Queue, lease, retry, replay and publication-gate execution | E | Must consume D fence and I current authorization |
| Retrieval/index/cache/working-set suppression | F | Must enforce current D fence and report per-target result |
| Context/snapshot/delta invalidation and reconciliation | G | Must enforce current D fence and report per-target result |
| Adapter managed-region clearing, quarantine and offline reconnect reconciliation | H | ACK is capability-bounded; cannot claim hidden provider erasure |
| Controlled storage, replicas, backup expiry and restore fencing | Storage/backup operator | Must prove durability, erasure or bounded retention state |
| External recipient action | External recipient; tracked by I | Brain records only verifiable response/contractual evidence |

**Authority rule:** D may define what a canonical Forget transition means, but cannot grant permission, waive legal hold, define an exception to retention policy, or declare global completion unilaterally. I may authorize/deny/defer, define cross-system inventory/evidence acceptance policy, and approve bounded governance exceptions, but cannot redefine D's canonical Memory states, ForgetFence semantics, D-domain completion predicate, or silently mutate D-owned operation transitions. D defines domain completion; I separately assesses cross-system governance compliance. An executor may report only its own target action and evidence.

### 2.1 Required bilateral change control

Any change to (a) the mapping in §3, (b) the global result rules in §5, or (c) the D/I authority split requires both D and I to approve the exact same document version and content SHA. Silence, a PR comment by the implementer, or a single Owner's self-review is not bilateral approval. Until both approvals are recorded, this document remains a proposal and must not supersede DOC-SEC-001 or the lifecycle model.

## 3. Canonical Memory state ↔ Forget operation phase mapping (D-F02)

### 3.1 Distinct state machines

Memory lifecycle:
`Candidate | Consolidated | Active | Superseded | Archived | Forgotten`

**D-owned canonical Forget operation phase:**
`Requested → Authorized → SuppressionCommitted → InventorySealed → CleanupInProgress → DomainCompletionEvaluated → Completed | Failed | Cancelled`

**Separate I-owned cross-system governance assessment:**
`Pending | Compliant | CompliantWithException | NonCompliant | Deferred`

These are different aggregates with different identities and authorities. A Memory may be `Forgotten` while its Forget operation is still `InventorySealed` or `CleanupInProgress`. The user-facing label `CompletedWithPolicyException` is a derived combined projection only when D's domain result is `Completed` and I's governance assessment is `CompliantWithException`; it is not a D-owned canonical lifecycle state.

### 3.2 Linearization and transition mapping

| Forget operation event/phase | Canonical Memory effect | Required invariant |
|---|---|---|
| Requested | No lifecycle change | Request is a durable intent only; ordinary access remains governed by current state and permission |
| Authorized | No lifecycle change | I policy decision is current, scoped and auditable; authorization alone does not suppress |
| SuppressionCommitted | Target Memory transitions atomically to `Forgotten`; durable ForgetFence generation and tombstone are committed with operation/outbox record | This durable commit is the canonical linearization point. From it onward, all reads, derivations, activations, deliveries and restore paths must reject or quarantine the forgotten identity |
| InventorySealed | No additional lifecycle change | Versioned target inventory is sealed for a specific inventory revision; late targets create a new revision and invalidate completion evaluation |
| CleanupInProgress | No lifecycle change | Derivatives and physical copies are cleaned according to policy; `Forgotten` remains terminal |
| CompletionEvaluated | No lifecycle change | D evaluates its canonical domain-level completion predicate. I separately evaluates cross-system evidence and policy compliance; I does not rewrite D's result |
| Completed | No lifecycle change | D's canonical domain-level completion predicate is satisfied. Cross-system governance compliance remains a separate I assessment |
| CompletedWithPolicyException | No lifecycle change | Not a D-owned phase. It is a derived public projection only when D result is Completed and I assessment is CompliantWithException under §5.3 |
| Failed | No lifecycle rollback | Failure means the operation cannot currently advance; suppression remains in force. Retry/reconciliation may resume unless I policy explicitly closes further attempts |
| Cancelled | No lifecycle change permitted after suppression | Cancellation is allowed only before SuppressionCommitted. After the linearization point, cancellation is rejected; an operator may stop an attempt but cannot remove the fence or mark the operation Cancelled |

### 3.3 Forgotten invariant

`Forgotten` means: (1) canonical identity is terminal; (2) current content is not retrievable or deliverable; (3) no new derivation/activation may be produced from it; (4) stale replicas, caches, working sets, contexts, adapters and restored backups must be fenced before use; and (5) deletion/de-identification and residual retention are tracked by the operation.

It does **not** mean: all bytes have been physically erased, every backup has expired, every external recipient has complied, or the global operation is Completed.

A later re-submission of similar information must create a new Memory identity with new provenance. It must not resurrect or reuse the forgotten identity.

### 3.4 Cancel and failure boundaries

- Before SuppressionCommitted: I may deny, defer or cancel under policy; D records the operation disposition without changing Memory lifecycle.
- At/after SuppressionCommitted: no cancel/rollback path may remove or lower the fence. A worker may be paused or an attempt abandoned, but the operation remains suppressed and resumable/reconcilable.
- Failed is not proof of safe deletion and is not permission to expose content. It is an incomplete result with an explicit failure reason and retry disposition.

## 4. Per-target evidence record (D-F03)

Each target in the I-governed inventory MUST have one current evidence record for each required action stage. Records are append-only; corrections supersede by reference and never erase prior evidence.

### 4.1 Required fields

| Field | Meaning / constraint |
|---|---|
| operation_id | Stable canonical ForgetOperation identifier |
| inventory_revision | Monotonic inventory revision to which this target belongs |
| target_id | Stable opaque target reference; no content payload |
| target_class | Canonical, derivative, index/cache, working-set, context, adapter-managed, primary-storage, replica, backup, external-recipient, audit-copy, or policy-retained |
| owner_domain | D/E/F/G/H/C/Storage/external-recipient |
| required_action | suppress, invalidate, delete, redact, deidentify, erase, expire, quarantine, restore-fence, notify, or verify |
| capability | supported / unsupported / conditional, plus capability-profile version |
| target_state | pending / in_progress / suppressed / cleaned / erased / expired / quarantined / acknowledged / policy_retained / failed / unknown |
| fence_generation | D-issued generation required to reject stale content |
| authorization_decision_ref | Current I authorization decision used for this stage |
| policy_version_refs | Applicable retention, legal-hold and completion-policy versions |
| evidence_ref | Immutable evidence object or trace reference; no copied forgotten content |
| evidence_kind | transaction receipt, deletion receipt, cryptographic-erasure proof, backup-expiry record, verifier observation, authenticated recipient receipt, or exception approval |
| observed_at | UTC timestamp from trusted clock source |
| verifier | Authenticated verifier identity/service and verification method |
| attempt_id / lease_fence | Current attempt and monotonically increasing lease/fencing token |
| result_code | stable machine-readable success/failure/unknown code |
| exception_ref / expires_at | Required for policy_retained or approved exception; otherwise null |
| provenance | source system, producer identity, signature/checksum or equivalent integrity metadata |

No target may be omitted because it is unsupported, offline, inaccessible, or inconvenient. If a target is discovered after sealing, append a new inventory revision, re-evaluate required actions, and invalidate any prior completion evaluation.

### 4.2 Evidence quality rules

- An ACK proves only the action and region explicitly covered by its capability profile.
- An external-recipient ACK is not physical-erasure proof unless an independently auditable guarantee explicitly covers the relevant copies and scope.
- A queue ACK proves queue acceptance/processing only; it does not prove downstream deletion.
- A cache invalidation receipt proves only the identified cache namespace/generation.
- A backup expiry record proves expiry only for the named backup set and retention schedule.
- Missing evidence, unverifiable provenance, stale fence generation, unsupported capability or unknown state is not success.
- Evidence must not contain the forgotten content itself. Use opaque references, digests where permitted, minimal metadata and integrity protection.

## 5. Cross-system governance assessment and exception policy (I authority; separate from D-domain completion)

D alone defines the canonical D-domain completion predicate and the D-owned `Completed` operation result. I MUST NOT set, rewrite or redefine that result. I evaluates whether cross-system evidence and policy obligations are satisfied and records a separate governance assessment.

### 5.1 GovernanceCompliant

I may record `Compliant` only when all of the following hold:

1. Authorization and applicable policy decisions are valid and current.
2. The target inventory is sealed at the evaluated revision; no required target is unknown or unaccounted for.
3. Every required target action is in an accepted verified terminal state for its target class.
4. Suppression is effective at every mandatory access/derivation/delivery/restore boundary.
5. Required derivative cleanup is verified.
6. Controlled primary/replica erasure requirements are satisfied.
7. Backup copies have expired or are covered by a separately approved bounded retention exception; an unexpired required backup cannot silently count as erased.
8. External recipients have supplied the required verifiable evidence or are covered by an explicitly approved, bounded policy exception.
9. Audit evidence is complete, integrity-protected and contains no forbidden content.
10. No legal hold, retention conflict, unsupported mandatory target, failed action or unknown state remains unresolved.

### 5.2 GovernanceNonCompliant / Deferred

Any required target in `pending`, `in_progress`, `failed`, `unknown`, or `unsupported` blocks `Compliant`. A successful subset does not make the cross-system governance result compliant. I records `NonCompliant` or `Deferred` with reasons. Re-evaluation is mandatory after inventory expansion, policy change, authorization revocation, evidence expiry or restore event.

### 5.3 GovernanceCompliantWithException

This assessment is permitted only when I explicitly approves each residual target and records:
- target and data class;
- precise reason and legal/policy basis;
- why full erasure is currently prohibited or infeasible;
- confirmation that access, derivation, delivery and restore remain blocked by the D fence;
- residual exposure and compensating controls;
- accountable policy owner;
- approval reference and approver;
- expiry/review time and required re-evaluation trigger;
- evidence reference and audit-integrity metadata.

It is not equivalent to physical erasure or unconditional completion. A legal hold or mandatory retention may require I to record `Deferred` rather than approve an exception; I must state the governing policy outcome. Exceptions cannot authorize resurrection or ordinary access.

The public projection `CompletedWithPolicyException` is permitted only when D has independently recorded domain result `Completed` and I has recorded `CompliantWithException`. If D is not `Completed`, the combined outcome remains incomplete regardless of I's exception assessment.

### 5.4 Truthful public status

The API/UI must expose D-domain result, I governance assessment and per-stage status distinctly. It must never translate `SuppressionCommitted`, `CleanupInProgress`, `Acknowledged`, or a partial target success into “deleted everywhere” or “Forget complete”.

## 6. Idempotency, retries, concurrency and crash recovery (D-F04)

### 6.1 Request idempotency

The request key is scoped by authenticated principal, effective Scope, target identity and operation type. The canonical request hash covers target set, purpose, policy context, requested action and relevant preconditions.

- Same key + same canonical request hash: return the existing operation identity/result; do not create a second operation.
- Same key + different request hash: reject with `IDEMPOTENCY_CONFLICT`.
- A retry never weakens the original scope or broadens target identity implicitly.
- Operation identity is stable across attempts and inventory revisions.

### 6.2 Stage checkpoint identity

Each stage checkpoint is keyed by:
`operation_id + inventory_revision + target_id + stage + action_version`.

Each attempt has a unique attempt_id, lease owner and monotonically increasing lease_fence. A worker may commit evidence only while holding the current lease fence. Stale workers are rejected. Concurrent retries are serialized per checkpoint or resolved by compare-and-swap against the checkpoint version.

### 6.3 Retry classes

- Retryable: transient network/service unavailability, timeout with unknown outcome, lease expiry, rate limit, temporary provider failure.
- Reconcile-before-retry: timeout after possible commit, duplicate ACK, partial batch, lost response, restored backup, changed inventory revision.
- Terminal for the current operation/policy: invalid target identity, irreconcilable integrity failure, denied authorization, legal hold/retention prohibition. Terminal means no blind retry; it does not remove suppression.
- Unknown outcome must be queried/reconciled before repeating a non-idempotent physical action.

### 6.4 Reauthorization and policy re-check

Before each irreversible or protected stage, the executor MUST re-check:
- authenticated principal/delegation remains valid where relevant;
- current PermissionEpoch and authorization decision;
- target remains within approved Scope;
- retention and legal-hold state;
- policy version and action obligations;
- current fence generation and target ownership/capability.

If authorization or policy cannot be established, fail closed and pause the stage. Previously queued authorization is not permanent authority.

### 6.5 Crash and inventory recovery

- Persist operation transition, checkpoint and evidence using a transaction or durable outbox/inbox protocol.
- On restart, load the last committed checkpoint and reconcile external side effects before retry.
- Never infer success from a worker having started or from a missing error.
- If a new dependency/target is discovered, append inventory revision N+1, preserve revision N, add required checkpoints, and return the operation to cleanup/reconciliation before any new completion evaluation.
- Before a backup/replica is made queryable after restore, enforce the latest D fence/high-water mark and reconcile all applicable Forget operations.
- A lost lease cannot authorize a stale worker to publish success.

## 7. Execution boundary contracts (E/F/G/H/C/Storage)

| Owner/domain | Minimum obligation | Minimum evidence |
|---|---|---|
| E — orchestration | Persist durable operation dispatch, leases, checkpoint/retry state, DLQ/replay suppression; reauthorize before protected stages | operation/checkpoint IDs, lease fence, attempt trace, dispatch and replay result |
| F — retrieval | Enforce fence before candidate enumeration/ranking/return; invalidate index/cache/working-set entries; prevent rebuild resurrection | index generation, query-denial test, invalidation/rebuild receipt |
| G — context | Remove or quarantine Context entries, snapshots and deltas; block delivery and reconcile offline clients | context revision, delivery denial, reconciliation receipt |
| H — adapters | Enforce managed-region capability, clear/quarantine where supported, reconcile offline reconnect; accurately classify unsupported regions | capability profile, ACK scope, quarantine/clear result, reconnect reconciliation |
| C — principal agent/inference/telemetry | Treat memory/telemetry as untrusted; cannot authorize Forget, alter lifecycle or infer completion; prevent stale forgotten content from being emitted as a new candidate | source/fence lineage and rejection trace; no authority-bearing telemetry |
| Storage / backup | Atomically persist canonical tombstone/fence with operation record; erase controlled copies; enforce fence before restore | transaction/WAL receipt, generation, erasure proof, backup-set expiry, restore-fence test |
| External recipients | Execute only authorized scoped action and return verifiable response | authenticated receipt, declared coverage, timestamp, provenance; no implied hidden-copy proof |

Every owner must publish its own capability and evidence contract. This proposal does not claim that any of these execution obligations are implemented or tested.

The owner-specific normative questions, local preconditions, visibility gates, evidence envelopes, failure behavior and cross-owner handshakes are expanded in [Forget Execution Boundary Contracts v1](owner-execution-boundary-contracts-v1.md). The R3 matrix adds DFI-013…DFI-022 for E/F/G/H/C/Storage race, replay, stale-cache, offline-reconciliation, ACK-capability and restore cases. Both documents remain proposals pending each accountable Owner's acknowledgement of the exact blob SHA.

## 8. Minimum conformance tests to add to R3 matrix

| Test ID | Scenario | Required assertion |
|---|---|---|
| DFI-001 | Suppression linearization race with concurrent read/derivation | Once canonical fence/tombstone commit succeeds, no later read/derivation/delivery returns content |
| DFI-002 | Memory Forgotten while operation CleanupInProgress | Memory state remains terminal; operation is not reported Completed |
| DFI-003 | Cancel requested after SuppressionCommitted | Cancel rejected; fence remains effective |
| DFI-004 | Missing/unknown/unsupported required target | Global Completed rejected |
| DFI-005 | External ACK with limited managed-region coverage | ACK does not prove hidden-copy erasure |
| DFI-006 | CompletedWithPolicyException | Requires I approval, bounded residual, expiry/review, and enforced fence |
| DFI-007 | Same idempotency key, same/different request hash | Same returns same operation; different rejects |
| DFI-008 | Concurrent retries and stale lease worker | Only current lease fence may commit checkpoint/evidence |
| DFI-009 | Crash after side effect before receipt | Reconcile actual side effect before retry; no duplicate destructive action |
| DFI-010 | Permission revocation or legal hold change mid-operation | Next irreversible stage fails closed pending re-evaluation |
| DFI-011 | Dependency discovered after inventory sealing | New inventory revision invalidates previous completion evaluation |
| DFI-012 | Backup restore after Forget | Latest fence is enforced before restored data is queryable/deliverable |

These are test specifications only. They are NOT RUN until a reproducible harness, fixtures, commands, outputs and exact commit SHA are recorded.

## 9. Required approvals and closure evidence

| Gate | Required evidence | Status |
|---|---|---|
| D approval | Explicit approval of exact version/SHA and D-owned semantics | PENDING |
| I approval | Explicit approval of exact version/SHA and I-owned governance policy | PENDING |
| E/F/G/H/C/Storage acknowledgements | Each owner confirms its execution/evidence boundary or records a bounded disagreement | PENDING |
| B/H identity and transport implications | Confirm authenticated actor and typed target/scope binding compatibility | PENDING |
| Bilingual semantic parity | Independent line-by-line parity review of both language versions | PENDING |
| R3 conformance | Executed DFI and R3-002…R3-009 tests with reproducible evidence | NOT RUN |
| Integration review | Distinct non-implementing reviewer checks exact merged baseline | PENDING |
| Acceptance authority | Separate explicit decision after all mandatory gates | PENDING |

## 10. Proposed disposition of D-F01…D-F04

- D-F01: PROPOSED RESOLUTION — responsibility/decision matrix in §2; closure still requires D/I approval and execution-owner acknowledgements.
- D-F02: PROPOSED RESOLUTION — distinct state machines and linearization mapping in §3; closure still requires D/I approval and conformance tests.
- D-F03: PROPOSED RESOLUTION — per-target evidence record and I-owned aggregation in §§4–5; closure still requires schema implementation, owner evidence and executed tests.
- D-F04: PROPOSED RESOLUTION — request/stage idempotency, leases, reauthorization and recovery in §6; closure still requires implementation and fault-injection tests.

**Current result: D-F01…D-F04 are addressed by a concrete proposal, NOT CLOSED.** No architecture acceptance, security certification, test pass, merge authorization or production readiness is claimed.

---

# 中文版本

## 1. 目的与不可妥协的不变量

本文提出统一联合契约，以关闭 D-F01 至 D-F04。它区分规范领域含义、安全/治理权限、执行职责和证据职责。本文件在 D 与 I 明确批准前始终是提案。

1. Memory 生命周期状态不等于 Forget Operation 阶段。
2. `Forgotten` 对规范内容身份而言是终态，表示持久化抑制决策已经线性化；它不表示物理擦除或全局 Forget 完成。
3. 不能仅凭 Tombstone、Adapter ACK、Queue ACK、Cache Invalidation 或单个存储删除就认定 Forget 完成。
4. 未知、不可达、不支持、失败或未登记但必需的目标，绝不能计为成功。
5. 抑制线性化后，任何重试或失败都不得恢复普通访问。不得回滚到 Active/Archived，也不得通过取消操作移除 Fence。
6. 安全授权及 Retention/Legal Hold 策略归 I；规范 Memory 生命周期及 Forget Operation/Fence 语义归 D。
7. 每个不可逆阶段执行前，必须重新检查当前授权和适用策略。
8. 每项完成声明必须基于已封存的版本化目标清单、逐目标证据和 I 管理的聚合策略。

## 2. 权限与责任矩阵（D-F01）

| 决策 / 行为 | 负责 Owner | 必须参与者 / 证据 |
|---|---|---|
| Memory 生命周期词汇及合法转换 | D | Runtime/MCM 消费方确认 |
| 规范 ForgetOperation 身份、阶段模型、事件顺序和转换不变量 | D | I 批准治理边界；E/Storage 确认持久化执行接口 |
| ForgetFence generation、规范抑制线性化点和 Tombstone 语义 | D | Storage 确认原子持久化；E/F/G/H 确认执行边界 |
| Actor 认证、授权、Delegation、Revocation 和 PermissionEpoch 策略 | I | H 绑定已认证传输主体；各执行方重新检查 |
| Subject/Scope 资格、Purpose、Consent、Retention 和 Legal Hold 决策 | I | D 提供类型化目标引用；领域 Owner 提供归属/适用性 |
| 全局目标清单策略、必需目标类别及清单封存标准 | I | D 定义依赖清单契约；E/F/G/H/C/Storage 登记各自目标 |
| 逐目标动作语义及本地能力结果 | 对应执行域 Owner | E/F/G/H/C/Storage；各自在信任边界内输出可追踪证据 |
| D 领域完成判定条件 | D | I 审查安全影响，但不得重定义判定条件；提供 D 所有的转换/一致性证据 |
| 跨系统证据评估、治理合规和策略例外 | I | D 提供规范 D 领域状态/判定条件；目标 Owner 提供能力范围内的证据 |
| Agent Telemetry 或模型推理 | C | 可以提出/观察；不能认证、授权、修改生命周期或声明 Forget 完成 |
| Queue、Lease、Retry、Replay 和 Publication Gate 执行 | E | 必须消费 D Fence 并检查 I 当前授权 |
| Retrieval/Index/Cache/Working Set 抑制 | F | 必须执行当前 D Fence 并报告逐目标结果 |
| Context/Snapshot/Delta 失效和对账 | G | 必须执行当前 D Fence 并报告逐目标结果 |
| Adapter 管理区域清理、隔离及离线重连对账 | H | ACK 受能力范围约束；不得声称隐藏 Provider 副本已擦除 |
| 受控存储、Replica、Backup 到期及 Restore Fence | Storage/Backup Operator | 必须证明持久化、擦除或有边界的保留状态 |
| 外部接收方动作 | 外部接收方；由 I 跟踪 | Brain 只记录可验证响应 |

**权限规则：** D 可以定义规范 Forget 转换的含义，但不能授予权限、豁免 Legal Hold、定义 Retention 策略例外，也不能单方面声明全局完成。I 可以授权/拒绝/延期，定义跨系统清单/证据接受策略并批准有边界的治理例外，但不能重新定义 D 的规范 Memory 状态、ForgetFence 语义、D 领域完成判定条件，也不能静默修改 D 所有的 Operation 转换。D 定义领域完成；I 单独评估跨系统治理合规性。执行方只能报告自己的目标动作和证据。

### 2.1 必须的双边变更控制

对以下内容的任何变更：(a) §3 状态映射；(b) §5 全局结果规则；(c) D/I 权责划分，均须 D 与 I 对同一文档版本及内容 SHA 明确批准。沉默、实施者 PR 评论或单个 Owner 自检都不构成双边批准。在双方批准前，本文件仍是提案，不得取代 DOC-SEC-001 或生命周期模型。

## 3. 规范 Memory 状态与 Forget Operation 阶段映射（D-F02）

### 3.1 两套独立状态机

Memory 生命周期：
`Candidate | Consolidated | Active | Superseded | Archived | Forgotten`

**D 所有的规范 Forget Operation 阶段：**
`Requested → Authorized → SuppressionCommitted → InventorySealed → CleanupInProgress → DomainCompletionEvaluated → Completed | Failed | Cancelled`

**独立的 I 所有跨系统治理评估：**
`Pending | Compliant | CompliantWithException | NonCompliant | Deferred`

两者是不同身份、不同权限的聚合对象。Memory 可以已经处于 `Forgotten`，而 Forget Operation 仍处于 `InventorySealed` 或 `CleanupInProgress`。面向用户的 `CompletedWithPolicyException` 仅是派生展示结果：只有 D 的领域结果为 `Completed` 且 I 的治理评估为 `CompliantWithException` 时才允许出现；它不是 D 所有的规范生命周期状态。

### 3.2 线性化点与状态映射

| Forget Operation 事件/阶段 | 规范 Memory 影响 | 必须满足的不变量 |
|---|---|---|
| Requested | 不改变生命周期 | 仅为持久化意图；普通访问仍受当前状态和权限控制 |
| Authorized | 不改变生命周期 | I 的策略决策当前有效、Scope 明确且可审计；授权本身不产生抑制 |
| SuppressionCommitted | 目标 Memory 原子转换为 `Forgotten`；持久化 ForgetFence generation 与 Tombstone，并与 Operation/Outbox 记录一起提交 | 此持久化提交是规范线性化点。从此之后，所有读取、派生、激活、交付和 Restore 路径必须拒绝或隔离该 Forgotten 身份 |
| InventorySealed | 不再改变生命周期 | 目标清单针对特定 revision 封存；迟到目标产生新 revision，并使此前完成评估失效 |
| CleanupInProgress | 不改变生命周期 | 按策略清理派生项和物理副本；`Forgotten` 始终保持终态 |
| CompletionEvaluated | 不改变生命周期 | D 评估其规范领域完成判定条件；I 独立评估跨系统证据和策略合规性，不得改写 D 的结果 |
| Completed | 不改变生命周期 | D 的规范领域完成判定条件已满足。跨系统治理合规性仍由 I 单独评估 |
| CompletedWithPolicyException | 不改变生命周期 | 不是 D 所有阶段；仅当 D 结果为 Completed 且 I 评估为 CompliantWithException 时，才可作为 §5.3 的派生公开展示结果 |
| Failed | 不回滚生命周期 | 表示 Operation 当前无法继续；抑制持续有效。除非 I 策略明确关闭后续尝试，否则可重试/对账 |
| Cancelled | SuppressionCommitted 后不允许生命周期变化 | 仅在 SuppressionCommitted 之前允许取消。线性化之后必须拒绝取消；操作员可以停止一次尝试，但不能移除 Fence 或将 Operation 标记为 Cancelled |

### 3.3 Forgotten 不变量

`Forgotten` 表示：(1) 规范身份已终结；(2) 当前内容不可检索或交付；(3) 不得基于该身份产生新派生或激活；(4) 旧 Replica、Cache、Working Set、Context、Adapter 和 Restore Backup 在使用前必须受到 Fence 约束；(5) 删除/去标识化及残余保留由 Operation 跟踪。

它**不表示**：所有字节均已物理擦除、所有 Backup 均已到期、所有外部接收方均已履约，或全局 Operation 已 Completed。

之后重新提交相似信息，必须使用新 Memory 身份和新 Provenance；不得复活或复用已 Forgotten 身份。

### 3.4 Cancel 与 Failure 边界

- SuppressionCommitted 之前：I 可依策略拒绝、延期或取消；D 记录 Operation 处置，不改变 Memory 生命周期。
- SuppressionCommitted 时及之后：任何 Cancel/Rollback 路径都不得移除或降低 Fence。Worker 可以暂停或放弃一次尝试，但 Operation 仍保持抑制，并可恢复/对账。
- Failed 不是安全删除证明，也不是暴露内容的许可。它表示结果未完成，必须带有明确失败原因和重试处置。

## 4. 逐目标证据记录（D-F03）

I 管理的目标清单中，每个目标对每个必需动作阶段都必须有一条当前证据记录。记录只追加；修正通过引用 supersede，不得删除历史证据。

### 4.1 必需字段

| 字段 | 含义 / 约束 |
|---|---|
| operation_id | 稳定的规范 ForgetOperation 标识 |
| inventory_revision | 此目标所属的单调递增清单版本 |
| target_id | 稳定不透明目标引用；不得包含内容载荷 |
| target_class | canonical、derivative、index/cache、working-set、context、adapter-managed、primary-storage、replica、backup、external-recipient、audit-copy 或 policy-retained |
| owner_domain | D/E/F/G/H/C/Storage/external-recipient |
| required_action | suppress、invalidate、delete、redact、deidentify、erase、expire、quarantine、restore-fence、notify 或 verify |
| capability | supported / unsupported / conditional，以及 capability-profile 版本 |
| target_state | pending / in_progress / suppressed / cleaned / erased / expired / quarantined / acknowledged / policy_retained / failed / unknown |
| fence_generation | D 签发、用于拒绝陈旧内容的 generation |
| authorization_decision_ref | 此阶段使用的当前 I 授权决策 |
| policy_version_refs | 适用的 Retention、Legal Hold 和完成策略版本 |
| evidence_ref | 不可变证据对象或 Trace 引用；不得复制已 Forgotten 内容 |
| evidence_kind | transaction receipt、deletion receipt、cryptographic-erasure proof、backup-expiry record、verifier observation、authenticated recipient receipt 或 exception approval |
| observed_at | 来自可信时钟源的 UTC 时间戳 |
| verifier | 已认证的验证者身份/服务及验证方法 |
| attempt_id / lease_fence | 当前 attempt 和单调递增的 Lease/Fencing Token |
| result_code | 稳定的机器可读成功/失败/未知代码 |
| exception_ref / expires_at | policy_retained 或批准例外时必填，否则为空 |
| provenance | 来源系统、Producer Identity、签名/校验和或等效完整性元数据 |

不得因为目标不支持、离线、不可访问或不方便就从清单中省略。封存后发现新目标，必须追加新 inventory revision，重新评估必需动作，并使之前的完成评估失效。

### 4.2 证据质量规则

- ACK 仅证明其 capability profile 明确覆盖的动作和区域。
- 外部接收方 ACK 不等于物理擦除证明，除非有独立可审计保证明确覆盖相关副本和 Scope。
- Queue ACK 仅证明 Queue 接收/处理，不证明下游删除。
- Cache Invalidation Receipt 仅证明指定 Cache Namespace/Generation。
- Backup Expiry Record 仅证明指定 Backup Set 和保留计划已到期。
- 缺失证据、不可验证 Provenance、陈旧 Fence Generation、不支持的能力或未知状态都不算成功。
- 证据不得包含已 Forgotten 内容本身。应使用不透明引用、在允许时使用 Digest、最少元数据和完整性保护。

## 5. 跨系统治理评估与例外策略（I 权限；独立于 D 领域完成）

只有 D 可以定义规范 D 领域完成判定条件及 D 所有的 `Completed` Operation 结果。I 不得设置、改写或重定义该结果。I 评估跨系统证据及策略义务是否满足，并记录独立的治理评估。

### 5.1 GovernanceCompliant

仅当以下条件全部满足，I 才可记录 `Compliant`：

1. 授权及适用策略决策仍有效且为当前版本。
2. 目标清单已针对被评估 revision 封存；没有未知或未解释的必需目标。
3. 每个必需目标动作都处于该目标类别认可的、已验证终态。
4. 所有强制访问/派生/交付/Restore 边界均已有效执行 Suppression。
5. 必需派生项清理已验证。
6. 受控 Primary/Replica 擦除要求已满足。
7. Backup 副本已到期，或受独立批准且有边界的保留例外覆盖；未到期的必需 Backup 不得静默计作已擦除。
8. 外部接收方已提供要求的可验证证据，或被明确批准且有边界的策略例外覆盖。
9. 审计证据完整、完整性受保护，且不含禁止保留的内容。
10. 不存在未解决的 Legal Hold、Retention 冲突、不支持的必需目标、失败动作或未知状态。

### 5.2 GovernanceNonCompliant / Deferred

任何必需目标处于 `pending`、`in_progress`、`failed`、`unknown` 或 `unsupported`，都阻止 `Compliant`。部分目标成功不代表跨系统治理结果合规。I 应记录带有原因的 `NonCompliant` 或 `Deferred`。发生清单扩展、策略变更、授权撤销、证据过期或 Restore 事件后，必须重新评估。

### 5.3 GovernanceCompliantWithException

仅当 I 对每个残留目标明确批准并记录以下信息时，才允许此评估：
- 目标及数据类别；
- 精确原因和法律/策略依据；
- 当前禁止或无法完全擦除的原因；
- 确认访问、派生、交付和 Restore 仍被 D Fence 阻止；
- 残余暴露和补偿控制；
- 负责的策略 Owner；
- 批准引用和批准人；
- 到期/复核时间及必须重新评估的触发条件；
- 证据引用和审计完整性元数据。

它不等于物理擦除，也不等于无条件完成。法律保留或强制 Retention 也可能要求 I 记录 `Deferred` 而不是批准例外；I 必须说明适用策略结果。例外不能授权复活或普通访问。

公开展示的 `CompletedWithPolicyException` 仅在 D 已独立记录领域结果 `Completed` 且 I 已记录 `CompliantWithException` 时允许。如果 D 尚未 `Completed`，无论 I 的例外评估如何，联合结果都仍为未完成。

### 5.4 真实状态对外呈现

API/UI 必须分别呈现 D 领域结果、I 治理评估和各阶段状态。不得把 `SuppressionCommitted`、`CleanupInProgress`、`Acknowledged` 或部分目标成功翻译成“已全域删除”或“Forget 已完成”。

## 6. 幂等、重试、并发与崩溃恢复（D-F04）

### 6.1 请求幂等

请求 Key 以已认证 Principal、有效 Scope、目标身份和 Operation Type 为范围。规范请求 Hash 覆盖目标集合、Purpose、Policy Context、请求动作和相关前置条件。

- 相同 Key + 相同规范请求 Hash：返回现有 Operation 身份/结果，不创建第二个 Operation。
- 相同 Key + 不同请求 Hash：以 `IDEMPOTENCY_CONFLICT` 拒绝。
- 重试不得削弱原 Scope，也不得隐式扩大目标身份。
- Operation 身份在所有 attempt 和 inventory revision 中保持稳定。

### 6.2 阶段检查点身份

每个阶段检查点以如下组合为 Key：
`operation_id + inventory_revision + target_id + stage + action_version`。

每次 attempt 都有唯一 attempt_id、Lease Owner 和单调递增 lease_fence。Worker 只有持有当前 Lease Fence 才能提交证据。陈旧 Worker 必须被拒绝。并发重试按 checkpoint 串行，或通过 checkpoint version 的 Compare-and-Swap 解决。

### 6.3 重试分类

- 可重试：临时网络/服务不可用、超时且结果未知、Lease 过期、Rate Limit、临时 Provider 故障。
- 重试前必须对账：可能已提交后的超时、重复 ACK、部分批次、响应丢失、Backup Restore、清单版本变化。
- 当前 Operation/Policy 下的终止错误：目标身份无效、无法调和的完整性失败、授权被拒绝、Legal Hold/Retention 禁止。终止意味着不得盲目重试；不意味着移除抑制。
- 结果未知时，必须先查询/对账，再重复非幂等物理动作。

### 6.4 重新授权与策略复查

每个不可逆或受保护阶段之前，执行方必须重新检查：
- 相关已认证 Principal/Delegation 仍有效；
- 当前 PermissionEpoch 和授权决策；
- 目标仍属于批准的 Scope；
- Retention 和 Legal Hold 状态；
- Policy Version 和动作义务；
- 当前 Fence Generation 和目标归属/能力。

如果无法确认授权或策略，必须失败关闭并暂停阶段。此前排队的授权不是永久权限。

### 6.5 崩溃与清单恢复

- 使用事务或 Durable Outbox/Inbox 协议持久化 Operation 转换、Checkpoint 和证据。
- 重启时加载最后已提交 Checkpoint，并在重试前对账外部副作用。
- 不得从 Worker 已启动或缺少错误推断成功。
- 发现新依赖/目标时，追加 inventory revision N+1，保留 revision N，增加必需 Checkpoint，并在任何新完成评估前将 Operation 返回清理/对账阶段。
- Backup/Replica Restore 后、变为可查询前，必须执行最新 D Fence/High-water Mark，并对账所有适用 Forget Operation。
- Lease 丢失不得授权陈旧 Worker 发布成功。

## 7. 执行边界契约（E/F/G/H/C/Storage）

| Owner/领域 | 最低义务 | 最低证据 |
|---|---|---|
| E — Orchestration | 持久化 Operation Dispatch、Lease、Checkpoint/Retry 状态、DLQ/Replay 抑制；受保护阶段前重新授权 | operation/checkpoint ID、lease fence、attempt trace、dispatch 和 replay 结果 |
| F — Retrieval | 在 Candidate 枚举/排序/返回前执行 Fence；失效 Index/Cache/Working Set；防止 Rebuild 复活 | index generation、query-denial test、invalidation/rebuild receipt |
| G — Context | 删除或隔离 Context Entry、Snapshot 和 Delta；阻止交付并对账离线 Client | context revision、delivery denial、reconciliation receipt |
| H — Adapter | 执行 Managed Region 能力；在支持时清理/隔离；对账离线重连；准确分类不支持区域 | capability profile、ACK Scope、quarantine/clear result、reconnect reconciliation |
| C — Principal Agent/Inference/Telemetry | 将 Memory/Telemetry 视为不可信；不得授权 Forget、改变生命周期或推断完成；阻止陈旧 Forgotten 内容作为新 Candidate 输出 | source/fence lineage 和 rejection trace；无权威性的 Telemetry |
| Storage / Backup | 将规范 Tombstone/Fence 与 Operation Record 原子持久化；擦除受控副本；Restore 前执行 Fence | transaction/WAL receipt、generation、erasure proof、backup-set expiry、restore-fence test |
| External Recipients | 仅执行已授权、限定 Scope 的动作并返回可验证响应 | authenticated receipt、覆盖范围、时间戳、Provenance；不暗示隐藏副本已擦除 |

每个 Owner 必须发布自己的能力和证据契约。本提案不声称上述任何执行义务已实现或测试。

各 Owner 的规范问题、本地前置条件、可见性 Gate、证据封装、故障行为和跨 Owner 握手已在[Forget 执行边界契约 v1](owner-execution-boundary-contracts-v1.md)中展开。R3 矩阵新增 DFI-013…DFI-022，覆盖 E/F/G/H/C/Storage 的竞态、Replay、陈旧 Cache、离线对账、ACK 能力和 Restore 场景。两份文件仍为提案，须由每个责任 Owner 针对准确 Blob SHA 确认。

## 8. 应加入 R3 矩阵的最低一致性测试

| 测试 ID | 场景 | 必须断言 |
|---|---|---|
| DFI-001 | 并发 Read/Derivation 与 Suppression Linearization Race | 规范 Fence/Tombstone 提交成功后，任何后续读取/派生/交付均不得返回内容 |
| DFI-002 | Memory 已 Forgotten、Operation 仍 CleanupInProgress | Memory 状态保持终态；Operation 不得报告 Completed |
| DFI-003 | SuppressionCommitted 后请求 Cancel | Cancel 被拒绝；Fence 继续有效 |
| DFI-004 | 缺失/未知/不支持的必需目标 | 拒绝全局 Completed |
| DFI-005 | 外部 ACK 只覆盖有限 Managed Region | ACK 不证明隐藏副本已擦除 |
| DFI-006 | CompletedWithPolicyException | 必须有 I 批准、有边界的残余、到期/复核和有效 Fence |
| DFI-007 | 相同幂等 Key 配合相同/不同请求 Hash | 相同返回同一 Operation；不同则拒绝 |
| DFI-008 | 并发重试与陈旧 Lease Worker | 只有当前 Lease Fence 可以提交 Checkpoint/证据 |
| DFI-009 | 副作用发生后、Receipt 返回前崩溃 | 重试前对账真实副作用；不得重复破坏性动作 |
| DFI-010 | Operation 中途 Permission Revocation 或 Legal Hold 变化 | 下一不可逆阶段失败关闭，等待重新评估 |
| DFI-011 | Inventory Sealing 后发现依赖 | 新 Inventory Revision 使此前完成评估失效 |
| DFI-012 | Forget 后发生 Backup Restore | 恢复数据变为可查询/交付前必须执行最新 Fence |

这些仅是测试规范。只有在记录可复现 Harness、Fixture、命令、输出和准确 Commit SHA 后才可执行；当前均为 NOT RUN。

## 9. 必需批准与关闭证据

| Gate | 必需证据 | 状态 |
|---|---|---|
| D 批准 | 对准确版本/SHA 及 D 所有语义的明确批准 | PENDING |
| I 批准 | 对准确版本/SHA 及 I 所有治理策略的明确批准 | PENDING |
| E/F/G/H/C/Storage 确认 | 各 Owner 确认自己的执行/证据边界，或记录有边界的分歧 | PENDING |
| B/H 身份与传输影响 | 确认认证 Actor 和类型化 Target/Scope 绑定兼容 | PENDING |
| 双语语义一致性 | 对两个语言版本逐段进行独立一致性审查 | PENDING |
| R3 一致性验证 | 执行 DFI 及 R3-002…R3-009 测试并提供可复现证据 | NOT RUN |
| 集成审查 | 非实施者审查准确合并基线 | PENDING |
| 验收权限 | 所有强制 Gate 完成后的独立明确决定 | PENDING |

## 10. D-F01…D-F04 拟议处置

- D-F01：拟议解决方案 — §2 权责/决策矩阵；仍需 D/I 批准及执行 Owner 确认才能关闭。
- D-F02：拟议解决方案 — §3 独立状态机和线性化映射；仍需 D/I 批准及一致性测试。
- D-F03：拟议解决方案 — §§4–5 逐目标证据记录及 I 所有的聚合规则；仍需 Schema 实现、Owner 证据和实际测试。
- D-F04：拟议解决方案 — §6 请求/阶段幂等、Lease、重新授权和恢复；仍需实现及故障注入测试。

**当前结论：D-F01…D-F04 已由具体提案回应，但尚未关闭。** 不声称架构验收、安全认证、测试通过、合并授权或生产就绪。
