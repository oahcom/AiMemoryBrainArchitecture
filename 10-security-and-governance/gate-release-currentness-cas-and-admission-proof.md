# Gate Release Currentness CAS and Admission Proof
# Gate Release 当前性 CAS 与在途 Admission 证明

**Owner:** I — Security & Governance Architect  
**Status:** PROPOSED normative governance contract; implementation and conformance OPEN.

## 1. Purpose / 目的

A Gate Release is a conditional authorization against one exact governance state, not a reusable bearer permission. Release must prove (a) all security-relevant inputs are current at the release linearization point and (b) every operation admitted before closure/revocation is durably represented as in-flight. Release, admission, provider egress, cleanup and global Forget completion are distinct facts.

Gate Release 是针对精确治理状态的条件授权，不是可重复使用的通行令牌。必须证明发布时治理输入仍然当前，并证明关闭前已准入的操作均被持久记录为在途工作。

## 2. Typed currentness vector / 强类型当前性向量

The release proposal MUST bind a complete GovernanceCurrentnessVector:
- gate_id, gate_revision and gate_state;
- authenticated principal/actor reference and authentication-context revision;
- PermissionEpoch and authorization-policy revision;
- exact ScopeRefs and target-set digest;
- producer registry version/epoch and producer-class inventory digest;
- recipient/replica/export/backup inventory epoch and digest, where applicable;
- retention-policy and exception-policy revisions, including applicable holds;
- ForgetOperationId, ForgetFenceGeneration, target-set digest and required target-state vector, where applicable;
- evidence-manifest digest, schema version and validation profile;
- proposal nonce, issued_at and expires_at.

PermissionEpoch, ForgetFenceGeneration, ProducerInventoryEpoch, RecipientInventoryEpoch and GateRevision are distinct typed namespaces. They MUST NOT be compared, substituted or collapsed into one counter. Unknown or unenumerated security-relevant producer/recipient classes block release.

## 3. Prepare and final Currentness CAS / 提案与最终 CAS

Prepare authenticates the actor, resolves exact scope/targets, reads authoritative epochs and inventories, validates required evidence, and creates an immutable GateReleaseProposal. Prepare is advisory: it does not open the gate or authorize admission.

CommitGateRelease(proposal_id, expected_gate_revision, expected_vector_digest) MUST be a single linearizable conditional transition serialized with admission, gate closure and revocation. At its linearization point it MUST compare:
1. gate state/revision;
2. every component of the complete currentness vector;
3. proposal expiry, nonce and one-use status;
4. scope/target digest and evidence-manifest validity;
5. absence of newer revocation, policy change, Forget fence, inventory change or unresolved mandatory target.

Success atomically opens the gate and persists a GateReleaseReceipt binding proposal, resulting gate revision, full vector digest, evidence digest, actor, policy decision reference, timestamp and expiry. Any mismatch returns CURRENTNESS_CONFLICT, leaves the gate closed and requires a fresh Prepare. Never silently rebase a proposal. CAS on gate_revision alone or PermissionEpoch alone is insufficient.

## 4. Admission and in-flight proof / Admission 与在途证明

Every protected operation MUST call Admit before side effects. Admission atomically checks OPEN state and expected revision, full currentness vector, authenticated principal, exact operation/scope/target digest, release expiry/revocation and idempotency identity. It persists an AdmissionReceipt containing operation/request digest, scope/target digest, gate/release IDs and revisions, PermissionEpoch, policy revision, applicable inventory/fence epochs, producer/recipient class, principal, monotonic admission sequence and timestamp. The in-flight ledger increment and receipt are one atomic operation.

A queue message, lease, local boolean or old release receipt is not an admission receipt. No work may begin before durable admission.

## 5. Close/revoke ordering / 关闭与撤销顺序

CloseGate/revocation MUST serialize with Admit:
- Admission first: it is included in the immutable close high-water/barrier and remains in-flight until an owner records a durable terminal disposition.
- Close/revocation first: admission fails and no protected side effect begins.
- Lease timeout, queue deletion, worker loss, network timeout or restart is not terminal evidence.
- Pre-close work must be completed, cancelled, suppressed or explicitly excepted according to a versioned gate policy. Unknown work blocks a drained claim.
- Close immediately prevents new admission. Reopening requires a new release against a fresh currentness vector; old receipts cannot reopen the gate.

GateCloseReceipt binds close sequence/high-water, gate revision, currentness-vector digest, exact admitted set or verifiable contiguous range and unresolved count.

## 6. Invalidation / 当前性失效

Identity/authentication change, PermissionEpoch or policy change, scope/target change, Forget fence advance, inventory epoch change, new producer/recipient class, retention/hold change, evidence revocation/supersession/expiry or gate revision change invalidates a prepared proposal and triggers policy-defined revocation for an open gate. If currentness cannot be established, fail closed.

## 7. Evidence semantics / 证据语义

| Evidence | Proves | Does not prove |
|---|---|---|
| GateReleaseProposal | Prepared vector/evidence digest | Gate is open |
| GateReleaseReceipt | Exact conditional transition committed | Future currentness or any admission |
| AdmissionReceipt | One operation admitted under a release/vector | Side effect completed |
| InFlightLedgerEntry | Work remains accounted for | Work succeeded or was cancelled |
| TerminalDispositionReceipt | Owner-reported terminal outcome | Erasure outside owner control |
| GateCloseReceipt | No later admission; captures prior high-water | Drain completion by itself |
| DrainProof | All pre-close admissions have terminal evidence | Global Forget/physical deletion unless its evidence scope expressly covers them |

Evidence is immutable, integrity-protected, typed and replay-safe. Conflicting receipts are rejected and audited.

## 8. Required race tests / 强制竞争测试

1. Permission/policy epoch advances between Prepare and Commit: CAS fails.
2. Forget fence advances between Prepare and Commit: CAS fails.
3. Producer or recipient inventory changes between Prepare and Commit: CAS fails.
4. Two release proposals target one gate revision: at most one commits.
5. Admit races CloseGate: operation is either in the captured barrier or rejected.
6. Admit races revocation: no admission linearizes after revocation.
7. Duplicate admission with same digest is idempotent; changed digest conflicts.
8. Crash after admission before work start: recovery finds in-flight record.
9. Crash after side effect before terminal receipt: outcome UNKNOWN, not drained.
10. Lease expiry/queue deletion does not terminalize work.
11. Old release replay after close/revocation is rejected.
12. Unknown producer/recipient class or inventory gap blocks release/drain proof.
13. Evidence superseded after Prepare prevents commit or invokes policy-defined revocation.
14. Multiple in-flight operations at close are all covered by close high-water.

## 9. Ownership and status / Owner 与状态

I owns governance vector, authorization/revocation semantics, inventory completeness policy, release/close evidence and global completion criteria. D supplies canonical Forget/fence and producer-barrier evidence. E/F/G/H supply owner-local producer/recipient admission and terminal evidence. C owns Provider Egress Gate and Adapter send semantics. Storage/Consistency must prove linearizable ordering and crash recovery; this contract chooses no database.

**PROPOSED.** This closes the semantic gap only after exact gate profiles, vector schema, evidence mapping and owner confirmations are recorded. No implementation, race test, inventory completeness or global Forget completion is claimed.
