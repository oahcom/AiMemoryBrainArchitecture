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


## 10. Cross-authority revocation linearization / 跨权威撤销线性化

A local CAS cannot atomically compare an I-owned PermissionEpoch if the gate/admission authority and I governance authority are independent stores. The design MUST NOT describe such a read-then-write as an atomic cross-service CAS.

For strict immediate revocation, one of these realizations is required:
1. a shared linearizable authorization/gate sequencer that orders PermissionEpoch changes, release, admission and final side-effect commitment; or
2. a distributed transaction/consensus protocol with an equivalent proof; or
3. a revocation-barrier protocol in which I marks revocation PENDING, sends a higher fencing epoch to every enforcement gate, receives durable close/fence acknowledgements from the complete recipient/producer inventory, and only then declares revocation EFFECTIVE. Every gate must reject older epochs at its own side-effect linearization point.

A time-bounded authorization lease is a weaker, explicitly bounded-revocation profile; it MUST NOT be described as immediate revocation. Its maximum stale-authorization window, clock assumptions, renewal and partition behavior must be declared in policy.

If an enforcement point is offline/unreachable, strict revocation remains PENDING and global completion remains blocked unless I records a policy-approved residual exception. A cached signed decision alone does not prove currentness.


## 11. Controlling clarification — I-local CAS and cross-owner release barrier

**This section controls over any earlier wording in §§2–3 or §10 that could be read as requiring one atomic CAS across independent owner authorities.** I, D, C, H and Storage do not share one implied transaction domain. A digest containing several owner epochs is a reconciliation tuple, not a globally atomic snapshot. Owner-local counters are opaque and must never be numerically compared.

### 11.1 I-local serialization domain

I's PolicyDomain Sequencer is authoritative only for I-owned state: IGateGeneration, PermissionEpoch, authorization-policy revision, I inventory epochs/digests, revocation request sequence, and I-issued authorization/commit receipts. CommitIGateRelease MUST atomically compare and persist those I-owned values, proposal nonce/expiry, evidence-manifest digest, target-set digest and I gate revision. It MUST NOT claim that a D FenceGeneration, C CGateGeneration, H CapabilityEpoch, Storage transaction position or COC RecoveryEpoch was atomically compared in the I transaction.

Foreign owner evidence is represented by exact typed refs, immutable digests, issuer/key identity, owner-local generation, scope, target mapping, validity and status. I verifies signatures and queries currentness where required. A foreign proof is never converted into an I epoch or treated as a globally ordered position.

### 11.2 Cross-owner release is a barrier protocol

A global release/reopen that depends on several owner gates MUST use a staged protocol:
1. I creates a GLOBAL_RELEASE_PROPOSAL bound to exact I state and the complete mandatory owner/recipient inventory.
2. Each affected owner prepares its own gate release against its own current local state and returns a signed OWNER_RELEASE_PREPARED receipt. Prepare does not open that owner gate.
3. I commits its I-local release decision by CAS. If I currentness changed, abort the proposal; all owner gates remain closed.
4. I issues a one-use GLOBAL_RELEASE_COMMIT bound to the exact proposal and prepared-receipt set. Each owner performs its own local CAS and returns a durable OWNER_RELEASE_COMMITTED receipt.
5. I marks global release EFFECTIVE only after all mandatory owner acknowledgements are verified against the closed-world inventory. Missing/offline/unknown owner remains PENDING; an exception must be explicit, scoped, time-bounded where applicable, and policy-approved.

If an owner changes local gate generation between prepare and commit, its local CAS rejects. I must not infer release from a sent message or transport ACK. This protocol is not a distributed ACID transaction; it is a recoverable barrier with explicit partial states. No owner may accept a stale or replayed global release token.

### 11.3 Per-operation authorization and C causal order

I authorization for a protected side effect is not granted by global Gate Release. For C provider submission, I's PolicyDomain Sequencer orders the exact operation's single-use authorization receipt consumption against revocation:
- REVOCATION_WON before consumption: C MUST NOT invoke the provider.
- COMMIT_WON consumption first: the exact operation is held as an I in-flight participant; later revocation cannot become effective past it until C supplies authoritative terminal outcome or an approved recovery disposition.
- UNKNOWN/IN_DOUBT: no provider invocation if authorization terminality is unknown; keep the relevant barrier held.

The I receipt binds exact Publication/ParticipantIntent identity as applicable, request digest, C admission/request identity, D lineage/fence evidence, Storage participant where applicable, PolicyDomain, principal, scope, purpose, target, issuer/key and one-use consumption. COC/RecoveryJoin transports and reconciles evidence; it does not mint I authorization. The exact C causal-order contract controls provider submit sequencing.

### 11.4 Currentness and admission proof semantics

I Gate Release proves only the I-owned transition. I AdmissionReceipt proves only I authorization/admission for its exact operation and digest. It does not prove D admission, C egress, Storage visibility, provider execution, Adapter application or Forget completion. Owner-local close receipts and in-flight snapshots remain owner-issued. I global drain/completion is a verified join of those receipts plus the complete I inventory, not a synthesized global counter.

### 11.5 Required tests / 强制测试

1. I PermissionEpoch changes between I Prepare and I Commit: I CAS rejects.
2. D/C/H owner gate generation changes after OWNER_RELEASE_PREPARED: that owner's local commit rejects.
3. I commits global release but one owner is offline: global state remains PENDING, never EFFECTIVE.
4. Duplicate GLOBAL_RELEASE_COMMIT with same digest is idempotent; changed owner set/digest conflicts.
5. Revocation wins before I single-use authorization consumption: C records no provider invocation.
6. I COMMIT_WON wins before revocation: revocation remains held until exact C terminal outcome.
7. C provider outcome UNKNOWN: I target/participant remains unresolved.
8. Inventory epoch changes after release prepare: I CAS rejects or requires a fresh proposal.
9. Foreign owner counters are intentionally non-comparable: validator accepts exact refs/digests only, never numeric ordering.
10. Missing, invalidated, offline or key-revoked owner evidence blocks global effectiveness unless an explicit I exception is recorded.

**Disposition:** This is the controlling I semantic refinement. I-local CAS and the recoverable cross-owner barrier are specified; implementation, exact H wire schema, inventory completeness, cryptographic profile and race execution remain OPEN. No global release or Forget completion is claimed.

### 中文规范摘要

本节明确：I 的 CAS 只原子比较 I 自己的 PolicyDomain 状态；D Fence、C Gate、H Capability、Storage 事务位置和 COC RecoveryEpoch 均是独立权威值。跨 Owner Release 采用可恢复的分阶段 Barrier：Owner 先本地 Prepare，I 本地 CAS 后发出一次性 Commit，各 Owner 再执行本地 CAS；所有强制 Owner 的持久化确认齐备后，I 才能标记 Global Release EFFECTIVE。部分成功、离线或未知状态只能是 PENDING。

对 C Provider Submit，I 单次授权消费与撤销由 I PolicyDomain Sequencer 排序：REVOCATION_WON 禁止发送；COMMIT_WON 将精确操作纳入在途参与者，后续撤销等待 C 的权威终态；UNKNOWN 不得推断授权或发送。I Receipt 不替代 D Admission、C Egress、Storage Visibility 或 Provider Outcome。
