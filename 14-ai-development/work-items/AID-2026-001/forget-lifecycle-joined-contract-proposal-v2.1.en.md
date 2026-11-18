# AID-2026-001 — Joined Forget / Memory Lifecycle Contract Proposal v2.1 (EN)

**PROPOSED — NOT NORMATIVE.** Owner D/I have not approved this revision or the same exact content SHA. This is the English counterpart of a reciprocal EN/ZH pair and an additive remediation layer over frozen v2. Read with [ZH counterpart](forget-lifecycle-joined-contract-proposal-v2.1.zh-CN.md) and [immutable v2 baseline](forget-lifecycle-joined-contract-proposal-v2.md). v1 and v2 remain unchanged and traceable.

- Work item: AID-2026-001 / U-023 remediation
- Baseline Head: 411ad16dc6b59acb2821cd0b4b069c078e6ad941
- Source Blobs: v1 96882570d44f6a3c6d60a30b1edb0e405bde5efc; v2 28ce1f735be6781b8de32a310d50e24cb457f01e; U-010 e12bc3beaf7327f7646fa090cb1fe2cda023cacf; U-011 EN c9daf61a538a175718e1bb492797cb2b5a51547a; U-011 ZH d03d26bbdc96ee9df7f532144d331a3a06be3866; execution boundaries 008b625bdb29ee65fe136f21c0e9be6396228e4b; R3 matrix 0dac44f65a47541bf5dca90563c90ade6a5d4331; GOV-DOC-001 b51b054b9f1022133666542680df74dfe19de2fb.
- D approval: NOT CLAIMED; I approval: NOT CLAIMED; same-SHA bilateral approval: NOT GRANTED; Storage approval: NOT CLAIMED.
- Tests: specifications only; NOT RUN.

## 1. Incorporated baseline and invariants

This candidate incorporates v2 §§1–5, including its I decision envelope, commit-bound receipt, PermissionEpoch vector, nine commit-time checks, Legal Hold/exception record, inventory policy/seal, per-target evidence and typed results, with the restorations and Failed guards below. No Owner D/I authority decision is made here.

Unchanged U-010 invariants:
1. Successful durable `SuppressionCommitted` is the sole trigger for the atomic canonical Memory transition to `Forgotten`. I authorization is a mandatory pre-commit condition, not the trigger.
2. Once Forgotten, the same identity never resurrects. Failure, retry, revocation, unknown result, restore or policy change cannot lower/remove its fence or restore ordinary access.
3. I governance completion is not a precondition for Forgotten. D completion, I governance assessment, per-target result, exception decision and physical-erasure evidence remain separate facts.
4. `COMMIT_WON`, `REVOCATION_WON`, `UNKNOWN` retain v2/U-011 meanings. UNKNOWN fails closed before proven commit and requires reconciliation; proven durable commit remains Forgotten.
5. `ExceptionApproved ≠ Succeeded`.
6. `DomainCompletionEvaluated` is canonical; `CompletionEvaluated` is deprecated and MUST NOT be persisted/emitted as API or test identifier.
7. Status remains PROPOSED until Owner D and Owner I approve the same exact content SHA.

## 2. Restored v1 normative requirements

### 2.1 Reauthorization before every protected stage

Before **each** irreversible or otherwise protected stage (not only SuppressionCommitted), the executor MUST revalidate as applicable: authenticated principal/effective actor; delegation; current I decision and authoritative PermissionEpoch vector; exact operation/request hash/target/scope/purpose; current policy ID/version/revision; retention and Legal Hold; current D fence generation; target owner/capability profile/version/action; and evidence validity/freshness. Check at that stage's execution boundary. Cached, queued or earlier-stage authorization is not continuing authority. Any denied, stale, expired, unavailable, unknown or mismatched fact means fail closed and no protected action. Repeat after recovery, lease change, policy/epoch/scope/target change, restore or evidence invalidation. This does not make I governance completion a Forgotten precondition.

### 2.2 Request idempotency

The idempotency key is scoped by authenticated principal, effective Scope, target identity and operation type. Canonical request hash covers action, target set, purpose, policy context and preconditions.
- Same key + same hash: reuse the same stable `operation_id` and current result; no second operation.
- Same key + different hash: reject `IDEMPOTENCY_CONFLICT`; never mutate or broaden the original request.
- Retries and inventory revisions preserve operation_id. A materially changed request is a distinct request/operation under the applicable idempotency scope.
- A retry never weakens Scope or implicitly broadens target identity.

### 2.3 Checkpoint and lease fencing

Checkpoint identity is exactly `operation_id + inventory_revision + target_id + stage + action_version`. Each attempt has a unique `attempt_id`, lease owner and monotonically increasing `lease_fence`. Only the current lease_fence may commit checkpoint, evidence or publication; stale workers MUST be rejected. Concurrent retries for a checkpoint are serialized or use compare-and-swap on checkpoint version. Lease reassignment creates a new attempt, not a new operation.

### 2.4 Retry classification and reconciliation

| Class | Examples | Required behavior |
|---|---|---|
| Retryable | transient network/service outage, rate limit, temporary provider failure, lease expiry | Same operation/checkpoint, new attempt_id, current lease_fence and fresh per-stage checks. |
| Reconcile-before-retry | unknown timeout, possible commit timeout, duplicate ACK, partial batch, lost response, restored backup, inventory revision change, crash after side effect before receipt | Query authoritative state and reconcile side effect, commit, evidence and checkpoint first. Never repeat a non-idempotent physical action while outcome is unknown. |
| Terminal for current operation/policy | invalid target identity, irreconcilable integrity failure, denied authorization, binding Legal Hold/retention prohibition | No blind retry; record reason. New decision or separately identified operation only if permitted. Failure never removes fence. |

Unknown, missing error, worker start, dispatch acceptance, queue ACK or transport ACK is not success.

### 2.5 Complete GovernanceAssessment.Compliant predicate

I MAY record `Compliant` only when ALL hold for the exact inventory revision, policy revision, authorization receipt and evidence set:
1. Authorization and applicable policy decisions are valid/current.
2. Inventory is sealed; no required target is unknown or unaccounted for.
3. Every required target action is in an accepted verified terminal state for its target class.
4. Suppression is effective at every mandatory access/derivation/delivery/restore boundary.
5. Required derivative cleanup is verified.
6. Controlled primary and replica erasure requirements are satisfied.
7. Backups expired or each residual has a separately approved bounded retention exception; an unexpired required backup is not silently erased.
8. External recipients supplied required verifiable evidence or each residual has an explicitly approved bounded exception.
9. Audit evidence is complete, integrity-protected and contains no forbidden Forgotten content.
10. No unresolved legal hold, retention conflict, unsupported mandatory target, failed action or unknown state remains.
Any missing condition blocks Compliant. pending/in_progress/failed/unknown/unsupported required targets block Compliant; record NonCompliant or Deferred with reasons. Re-evaluate after inventory expansion, policy change, revocation, evidence expiry or restore.

### 2.6 CompletedWithPolicyException and public projection

`CompletedWithPolicyException` is a derived public projection iff D independently records `DDomainCompletion=Completed` AND I independently records `GovernanceAssessment=CompliantWithException`. It is not a canonical lifecycle/operation state. If D is not Completed, the combined result is incomplete. ExceptionApproved never changes PerTargetResult to Succeeded.

API/UI MUST expose MemoryLifecycle, ForgetOperationPhase, DDomainCompletion, each PerTargetResult/target_state, GovernanceAssessment, ExceptionDecision and PhysicalErasureEvidence separately. Never collapse SuppressionCommitted, Forgotten, CleanupInProgress, Acknowledged, partial success, D completion or I assessment into “deleted everywhere”/“Forget complete”. Disclose residual pending/failed/unknown/unsupported/policy-retained states without exposing forgotten content.

### 2.7 Target-state vocabulary

`target_state` values: `pending`, `in_progress`, `suppressed`, `cleaned`, `erased`, `expired`, `quarantined`, `acknowledged`, `policy_retained`, `failed`, `unknown`. They are distinct and do not imply global completion. Preserve at least operation_id, inventory_revision, target_id, target_class, owner_domain, required_action, capability/profile version, target_state, D fence generation, authorization/policy references, immutable evidence reference/kind, trusted observed_at, authenticated verifier/method/version, attempt_id, lease_fence, stable result_code, applicable exception reference/expiry and source provenance/integrity. Unknown, unsupported, offline, inaccessible and unregistered-but-required targets MUST remain represented.

## 3. G04-C — Failed recovery and append-only event history

`Failed` is terminal for the **attempt**, not automatically for the stable operation. The v2 §2.2 table is constrained:

| From | To | Mandatory guard |
|---|---|---|
| Failed | CleanupInProgress | Explicit RecoveryStarted event; reconcile prior side effects/checkpoints; current per-stage authorization, policy, capability and fence checks; new attempt_id/current lease_fence. |
| Failed | AuthorizationPending | Explicit ReauthorizationRequired event; close prior attempt; new attempt identity; no protected action before fresh I decision. |
| Failed | Blocked | Explicit BlockerRecorded event with reason/owner; preserve history; no work until resolved. |
| Failed | DomainCompletionEvaluated | Only evaluation-only failure, all required evidence/checkpoints still current and complete, explicit ReconciliationCompleted event, then D re-evaluates its predicate. No shortcut around cleanup/authorization. |
| Failed | Completed / Cancelled / SuppressionCommitted | Direct transition prohibited. |

Every recovery is an immutable event with authenticated actor, reason, causal reference to failed event, prior checkpoint, policy/authorization evidence and trusted timestamp. Post-commit failure preserves Forgotten/fence. Cancelled remains forbidden after SuppressionCommitted.

Stable operation_id spans retries, attempts, lease changes and inventory revisions for the same idempotent request. Each attempt gets a unique never-reused attempt_id. Every transition appends an immutable event containing event_id, operation_id, attempt_id, from/to phase, actor/service and authenticated principal where applicable, reason_code, correlation/causation IDs, inventory_revision, checkpoint identity/version, lease owner/fence, authorization/receipt and policy refs, target/scope ref, trusted observed_at, ordered event sequence/version and integrity provenance. Never rewrite/delete/overwrite prior Failed events, checkpoints, target results or receipts; corrections append a superseding event. Ambiguous post-commit outcome MUST be reconciled against durable SuppressionCommitted evidence before retry. Proven commit remains Forgotten; UNKNOWN fails closed and is reconciled, never destructively replayed.

## 4. Test crosswalk — source IDs preserved one-to-one

All are specifications, NOT execution evidence. Each ID has its own clause, scenario and assertion. DFI source: R3 matrix and Owner Execution Boundary Contracts v1.

### 4.1 DFI-001…DFI-022

| ID | Clause | Scenario | Required assertion |
|---|---|---|---|
| DFI-001 | §§1–2 | Concurrent read/derivation vs suppression linearization. | After fence/tombstone commit, no later read/derivation/delivery returns content. |
| DFI-002 | §§1,2,5 | Forgotten while operation CleanupInProgress. | Memory remains terminal; operation is not Completed. |
| DFI-003 | §2 | Cancel after SuppressionCommitted. | Cancel rejected; fence remains effective. |
| DFI-004 | §§2,5,2.5 | Missing/unknown/unsupported required target. | Global completion and Compliant rejected. |
| DFI-005 | §2.7; v2 §4.4 | External ACK covers limited managed region. | ACK proves no hidden-copy erasure beyond authenticated capability/coverage. |
| DFI-006 | §2.6; v2 §§4.2,5 | CompletedWithPolicyException projection. | Requires D Completed AND I CompliantWithException, bounded approved residuals/controls/expiry; exception is not target success. |
| DFI-007 | §2.2 | Same idempotency key with same/different hashes. | Same returns same operation; changed hash rejects IDEMPOTENCY_CONFLICT. |
| DFI-008 | §2.3 | Concurrent retries vs stale lease worker. | Only current lease_fence commits checkpoint/evidence. |
| DFI-009 | §§2.4,3 | Crash after side effect before receipt. | Reconcile before retry; no duplicate destructive action. |
| DFI-010 | §§2.1,2.4 | Revocation or Legal Hold changes mid-operation. | Next protected stage fails closed pending reauthorization/re-evaluation. |
| DFI-011 | v2 §4.3; §§2.5,2.7 | Dependency/required target found after inventory seal. | Append revision, preserve prior revision, invalidate assessment and re-evaluate. |
| DFI-012 | §§1,2.7,3 | Backup restore after Forget. | Latest fence applied before restored data query/delivery. |
| DFI-013 | v2 §4.3; E §3; R3 matrix | Producer admission/dependency registration races with fence. | Registration/publication serializes before fence or fence suppresses staged output; no late derivative/omitted target. |
| DFI-014 | §§2.3,2.4,3; E §3 | Lease/DLQ/recompile with stale lease/replay/duplicate event. | Cannot publish forgotten source; current fence and lease enforced. |
| DFI-015 | §§2.1,2.7; F §4 | In-flight Recall/delayed cache fill races with fence. | Revalidate before response/cache fill; no stale response after fence wins. |
| DFI-016 | §§1,2.7,3; F §4 | Index rebuild uses old snapshot/stale worker. | Rebuild uses canonical state/latest fence watermark; no resurrection. |
| DFI-017 | §§2.1,2.7; G §5 | Offline Snapshot/Delta replay after Forget/revocation. | Reconcile current ContextVersion/PermissionEpoch/Fence; reject stale Delta. |
| DFI-018 | §§1,2.7; G §5 | Context Remove confused with canonical Forget. | Remove changes membership only; Forget invalidates mapped projections/pending deliveries. |
| DFI-019 | §2.7; v2 §4.4; H §6 | ACK class/capability epoch limited or downgraded. | Only current supported scope/action reported; no promotion to erase/Full Applied. |
| DFI-020 | §§1,2.7; C §7 | Telemetry/inference re-emits forgotten source or claims success. | Agent/model claim non-authoritative; lineage/fence checked; stale content rejected. |
| DFI-021 | §§1,3; Storage §8 | Crash/failover around atomic suppression commit. | Tombstone/fence/operation/publication intent recover consistently; no exposure/lost fence. |
| DFI-022 | §§1,2.7,3; Storage §8 | Restore before latest fence applied. | Restored copy quarantined until latest fence/later Forget applied; no resurrection. |

### 4.2 I-U011-T01…T16 — exact original meanings

| ID | Clause | Scenario | Required assertion |
|---|---|---|---|
| I-U011-T01 | v2 §3.1 | Forged/unknown issuer or invalid signature. | Reject authorization; no commit. |
| I-U011-T02 | v2 §§3.1–3.2 | Audience/operation/request hash/purpose/scope mismatch. | Reject receipt; no commit. |
| I-U011-T03 | v2 §§3.1–3.2 | Expired/not-yet-valid receipt or replayed nonce. | Fail closed; no commit. |
| I-U011-T04 | v2 §3.3 | Current PermissionEpoch differs from receipt epoch. | Reject stale receipt. |
| I-U011-T05 | v2 §3.3 | Revocation epoch serializes first. | REVOCATION_WON; no commit. |
| I-U011-T06 | v2 §3.3 | Commit serializes before later revocation. | COMMIT_WON; durable Forgotten terminal; no resurrection. |
| I-U011-T07 | v2 §3.3 | Serialization/current epoch cannot be proven. | UNKNOWN; fail closed/reconcile; proven commit stays Forgotten. |
| I-U011-T08 | v2 §§3.1,3.3 | Delegation revoked/narrowed during race. | Currentness check rejects stale delegation. |
| I-U011-T09 | v2 §§4.1–4.2 | Legal Hold/mandatory retention prohibits action. | Deny/defer; no unauthorized exception. |
| I-U011-T10 | v2 §4.2 | Exception missing approver/authority/scope/jurisdiction/expiry/controls. | Invalid exception; no CompliantWithException. |
| I-U011-T11 | v2 §§2.7,5 | Exception approved but target action not done. | PerTargetResult is not Succeeded. |
| I-U011-T12 | §§2.5,2.7; v2 §§4.3,5 | Required target unknown/unsupported/unregistered. | GovernanceAssessment cannot be Compliant; target remains represented/unresolved. |
| I-U011-T13 | v2 §4.3 | New target/inventory or policy revision after assessment. | Prior assessment invalidated; reassess. |
| I-U011-T14 | v2 §§4.2,5 | Exception expires/revoked or Legal Hold changes. | Reassess; no silent renewal. |
| I-U011-T15 | §§2.5,2.6; v2 §5 | All target evidence present but D completion absent. | I MUST NOT declare D completion; no CompletedWithPolicyException projection. |
| I-U011-T16 | §§1,2.6; v2 §§1,5 | Forgotten committed while cleanup remains pending. | Forgotten terminal; governance remains separately pending/noncompliant as applicable. |

## 5. G04-C disposition

**Specification remediated in this candidate.** §3 guards the previously ambiguous Failed transitions and specifies operation/attempt identity, explicit recovery events, reconciliation and append-only history.

**Implementation/fault-injection gate remains OPEN / NOT EVIDENCED.** Do not call G04-C fully closed until reproducible tests cover all allowed/forbidden recovery transitions, stale lease rejection, stable operation_id/new attempt_id, immutable event history, ambiguous commit reconciliation and no resurrection after commit. No test execution is claimed.

## 6. Semantic decision register

No v1 semantic requirement is intentionally removed; all eight U023-REG-001 groups are restored above. No unilateral D/I semantic change is proposed. If either Owner considers a restored rule incompatible with its authority, register it as **D/I EXPLICIT DECISION REQUIRED**; this executor does not decide, waive or reinterpret it. Until bilateral decision, preserve the v1 source requirement and PROPOSED status.

## 7. Findings, approvals and non-claims

- **U023-GOV-001 — P1 — Issue #41 — FIXED_PENDING_INDEPENDENT_REVIEW.** Separate EN/ZH counterparts, reciprocal links and complete language-specific normative test tables are supplied in the same commit.
- **U023-REG-001 — P1 — Issue #41 — FIXED_PENDING_INDEPENDENT_REVIEW.** All eight v1 requirement groups restored in §2; no semantic deletion claimed.
- **U023-TEST-001 — P1 — Issue #41 — FIXED_PENDING_INDEPENDENT_REVIEW.** I-U011-T01…T16 retain source meanings one-to-one; DFI-001…022 each have an individual crosswalk row.
- **G04-C — P1 — Issue #41 — SPECIFICATION_REMEDIATED; IMPLEMENTATION_EVIDENCE_OPEN.** Recovery guards/history specified; fault-injection evidence outstanding.

Regression self-check: `SuppressionCommitted ⇒ Forgotten` remains sole trigger; atomic entry is non-resurrectable; I authorization is pre-commit precondition, not trigger; I governance completion is not Forgotten precondition; COMMIT_WON/REVOCATION_WON/UNKNOWN preserved; ExceptionApproved ≠ Succeeded; PROPOSED preserved.

No Owner D/I approval, Storage approval/atomicity proof, runtime implementation, production conformance, R3 execution, independent review PASS, D-R3-D-003 closure, acceptance, merge-to-main or production activation is claimed. AID-2026-001 remains BLOCKED_PENDING_R3_EVIDENCE.
