# Provider Egress Gate — Concrete Adapter Contract
# Provider Egress Gate：具体 Adapter 合同

**Owner:** C — Agent Integration Architect  
**Status:** PROPOSED normative Adapter contract; H wire mapping, I policy mapping and implementation tests OPEN.  
**Related:** agent-integration-overview.md.

## 1. Purpose and invariant / 目的与不变量

The Provider Egress Gate is enforced by the concrete Adapter that owns the provider transport. A Brain authorization response, context-delivery acknowledgement, cached OPEN flag or old gate token is not permission to send.

Invariant: no provider request crosses the Adapter's egress linearization point unless the Adapter has validated current gate revision, current authorization/PermissionEpoch, exact request digest and scope, applicable Forget/revocation state, and a one-use admission record. Gate closure and final egress commitment serialize through the same per-gate authority.

Distinguish PREPARED, ADMITTED, EGRESS_COMMITTED, HANDOFF_CONFIRMED and OUTCOME_UNKNOWN. Admission is not proof of sending; transport handoff is not proof of provider execution or model use.

## 2. Adapter obligations / Adapter 义务

A conforming Adapter MUST own the final provider transport call and expose only a gate-controlled send API. It constructs and hashes the exact outbound request envelope; binds provider/account/endpoint/region/model, request ID/attempt, principal/Agent/session, ScopeRefs, purpose, data classification, ContextVersion/AppliedContext when present, source-lineage/Forget reference, I decision/PermissionEpoch/policy revision, Adapter build/capability and transport-policy revision.

No caller may access an ungated SDK/client handle. SDK automatic retries, redirects, streaming payload continuations and failover must be disabled or routed back through a fresh gate decision for each physical outbound attempt. Digest covers exact outbound bytes/semantics; sensitive values may use keyed digests/protected references, but post-approval mutation must be detected.

## 3. Gate and request states / 状态

Gate: CLOSED -> OPEN(revision, policy vector) -> CLOSING(close sequence) -> CLOSED.

Request: PREPARED -> ADMITTED -> EGRESS_COMMITTED -> HANDOFF_CONFIRMED.
Alternative terminal states: REJECTED, CANCELLED_BEFORE_EGRESS, FAILED_BEFORE_EGRESS, OUTCOME_UNKNOWN.

ADMITTED is a durable in-flight reservation only. EGRESS_COMMITTED is the irreversible handoff authorization point. HANDOFF_CONFIRMED records transport acceptance under documented transport semantics, not provider inference completion.

## 4. Linearization and admission / 线性化与准入

One serialization authority per (adapter_id, provider_account_id, egress_gate_id) MUST cover gate changes, permission/revocation and Forget updates, admission, final egress commitment, close barrier/high-water. A durable transactional sequencer or equivalent single-writer journal is acceptable only if it proves multi-process ordering and crash recovery; a process-local mutex alone is insufficient for multiple replicas.

AdmitEgress(request, expected_gate_revision, expected_policy_vector) atomically checks OPEN state/revision, current I authorization and PermissionEpoch, provider/account/model/region and classification policy, exact request digest/scope, ContextVersion/AppliedContext evidence, current Forget fence for included sources, request idempotency and absence of a prior close/revocation. It persists a unique EgressAdmissionReceipt and increments the in-flight ledger atomically. No network call starts here.

Immediately before transport handoff, CommitEgress(admission_id, request_digest) rechecks current gate revision, policy/permission vector, Forget fence and exact digest. It atomically transitions ADMITTED -> EGRESS_COMMITTED. This transition is the egress linearization point only if the Adapter then invokes the bound transport exactly once with the immutable approved bytes.

## 5. Close versus send race / Gate 关闭与发送竞争

CommitEgress and CloseEgressGate MUST serialize through the same authority.

| Winner | Required behavior |
|---|---|
| CommitEgress first | This is pre-close committed egress and MUST appear in close receipt's in-flight set. Close cannot claim it prevented this handoff. |
| CloseEgressGate first | CommitEgress fails GATE_CLOSED/CURRENTNESS_CONFLICT; no transport handoff occurs. |

For ADMITTED but not EGRESS_COMMITTED requests, close wins by blocking final commitment; Adapter cancels them and records CANCELLED_BEFORE_EGRESS.

CloseEgressGate atomically closes/advances revision, prevents new admission and final commitment, and captures admission high-water plus pre-close in-flight IDs/range. If the product requires “no bytes handed to OS/provider after Close returns,” Close MUST wait for all earlier EGRESS_COMMITTED dispatch calls to reach a transport-return boundary. A network handoff already accepted by the transport cannot be rolled back.

If the Adapter crashes after EGRESS_COMMITTED but before recording transport result, state is OUTCOME_UNKNOWN. Do not blindly resend. Reconcile via provider idempotency/status support or preserve UNKNOWN under I policy.

## 6. In-flight evidence / 在途证据

Each durable ledger entry binds admission ID, request/attempt ID, exact digest, gate/release revision, principal/scope, provider/account/model/region, PermissionEpoch, policy revision, Forget reference, admission/egress sequence, transport attempt and outcome.

Terminal outcomes:
- CANCELLED_BEFORE_EGRESS: no egress commitment;
- FAILED_BEFORE_EGRESS: transport was not invoked;
- HANDOFF_CONFIRMED: transport accepted exact immutable request;
- OUTCOME_UNKNOWN: cannot establish whether handoff occurred;
- RECONCILED_SENT / RECONCILED_NOT_SENT: only with authoritative transport/provider evidence.

Timeout is not proof of not-sent. Provider response proves receipt of a correlated response, not use of any particular memory/context.

## 7. Retries, redirects, streaming and failover / 重试与转发

Every retry is a new attempt and requires fresh currentness/admission. Same idempotency key plus same digest may resolve to same logical request; changed digest conflicts. SDK retries are disabled unless each physical attempt re-enters the gate. Redirect or endpoint/region/account change requires a new descriptor and authorization. New outbound streaming payloads/tool-result forwarding are new egress operations. Provider/model/account failover is a new target and cannot inherit the prior admission. Old receipts cannot be replayed after close, revocation or fence advance.

## 8. Semantic Adapter API / 语义接口

```text
prepare_request(input) -> ImmutableEgressRequest
admit_egress(request, expected_gate_revision, expected_policy_vector)
  -> EgressAdmissionReceipt | REJECTED
commit_egress(receipt, immutable_request_bytes)
  -> EgressCommitReceipt | GATE_CLOSED | CURRENTNESS_CONFLICT
close_egress_gate(reason, expected_gate_revision) -> GateCloseReceipt
record_transport_result(commit_receipt, result) -> EgressTerminalReceipt
reconcile_unknown(admission_id, provider_reference)
  -> ReconciliationReceipt | OUTCOME_UNKNOWN
```

This is a semantic API, not the final wire schema. H owns BMCP encoding/capability negotiation; C owns Adapter boundary semantics.

## 9. Fail-closed and security / 失败关闭与安全

No ungated transport handle. No cached OPEN flag or old release receipt authorizes a new send. Unknown PermissionEpoch, missing I decision, stale Forget fence, scope/digest mismatch, unsupported capability or incomplete provider inventory => deny. Do not log raw sensitive payload merely to prove a digest. Gate close cannot retract bytes already handed to a provider; provider-side retention/deletion is I-owned. Memory is data, never elevated to system/developer instruction authority. If Brain/I currentness is unavailable, default governed egress behavior is fail closed unless an explicit versioned policy says otherwise.

## 10. Required race/fault tests / 必需竞争与故障测试

1. CommitEgress races Close: exactly one winner and transport behavior matches.
2. Admit races Close: receipt is in close high-water or admission is rejected.
3. Permission revocation races final commitment: no commitment after revocation.
4. Forget fence advances after admission but before commitment: reject.
5. Payload mutates after admission: digest mismatch, no send.
6. Crash after admission before commitment: recover blocked/cancelled, no send.
7. Crash after commitment before transport result: UNKNOWN, no blind resend.
8. Partial transport write/error is not mislabeled not-sent.
9. SDK retry/redirect cannot bypass gate.
10. Provider failover changes target and requires new admission.
11. Two Adapter replicas share serialization; no split-brain sends.
12. Close with ADMITTED but uncommitted requests prevents handoff.
13. Close with committed requests accounts for them and honors wait/return semantics.
14. Duplicate idempotent request and conflicting digest are distinguished.
15. Delayed provider response after close does not reopen gate.
16. No alternate ungated provider client path exists.

## 11. Ownership and status / Owner 与状态

C owns Provider Egress Gate semantics, Adapter API and race outcomes. I owns authorization, PermissionEpoch, revocation, classification, provider/recipient inventory, retention and provider-side deletion policy. H owns BMCP wire and capability/ack encoding. G supplies exact ContextVersion/AppliedContext evidence; delivery is not egress. D/E/F supply canonical identity/lineage/Forget references; their internal gates never authorize network sends. Agent/provider runtime owns inference beyond transport handoff.

Acceptance requires executable conformance against the actual Adapter/transport, including SDK retries, redirects, streaming and multi-replica behavior. **PROPOSED:** no implementation, test pass, interface freeze or implementation sign-off is claimed.


## 12. Cross-authority revocation and availability / 跨权威撤销与可用性

The Adapter's local send CAS cannot magically make an independently stored I PermissionEpoch atomic. The implementation MUST NOT claim immediate revocation based only on a previously fetched signed decision.

Strict revocation requires either a shared linearizable sequencer for I epoch changes and Adapter final egress commitment, a proven distributed transaction/consensus equivalent, or an I-owned revocation barrier. Under the barrier profile, I marks revocation PENDING, sends the newer fencing epoch to every Adapter/provider-account gate in the closed-world inventory, and waits for durable acknowledgements that each gate rejects old epochs. I may declare revocation EFFECTIVE only after the required acknowledgements or an explicit policy-approved residual exception. Each Adapter validates the highest installed epoch at CommitEgress.

A time-bounded authorization lease is a weaker profile with an explicit maximum stale-send window and clock/partition assumptions; it must not be represented as immediate revocation. If the Adapter cannot establish current policy/fencing epoch, governed egress fails closed. Offline Adapter means revocation remains pending for that target unless I approves and records a residual exception.


## 13. Controlling composition with C Phase 3.6 and Phase 3.8.2

**This section controls over any reading of §§3–5 that would make a local Adapter token sufficient for provider invocation or omit the common causal participant protocol.** The C Provider Egress Gate is the final C-owned side-effect boundary; it composes with, and does not replace, C's existing causal-order contract phase-3.6-c-submit-cross-authority-causal-order-contract.md, C's local admission/recovery amendment phase-3.6.9-c-owner-local-admission-gate-recovery-release-amendment.md, and the exact review phase-3.8.2-c-recovery-join-provider-side-effect-exact-review.md.

### 13.1 Distinct authorities and identities

C owns CGateGeneration, CAdmissionRef/ledger, provider reservation/attempt, actual egress dispatch and immutable CSubmitOutcome. COC owns the durable causal participant order and recovery prefix. I owns IGateGeneration, PermissionEpoch, policy decision and single-use authorization terminality. D owns ForgetFence/lineage and the exact D participant/clearance required for this operation. H transports typed evidence and ACKs but does not mint any of these decisions. Storage PreparedParticipant/GID/XID is not a provider idempotency key or C attempt identity.

CGateGeneration, ForgetFenceGeneration, PermissionEpoch, COC RecoveryEpoch/position and H CapabilityEpoch are separate opaque namespaces. They are bound by exact typed refs/digests in the operation tuple; they are never numerically compared or collapsed into a synthetic global counter.

### 13.2 Mandatory provider-submit causal chain

For a protected provider submit, the Adapter MUST establish and preserve this order:
1. **C local admission:** persist exact CAdmissionRef/request digest and bind authenticated principal, Agent/runtime/session, Scope/Environment, ContextId/ContextVersion, DeliveryId/attempt, ManagedRegion identity/revision/digest and final-request boundary. C Gate must be OPEN at this C-local admission linearization point.
2. **COC intent:** obtain the durable common ParticipantIntentRef from the coordinator, bound to the same CAdmissionRef, exact immutable post-transformation request digest, boundary, identity/session and context/delivery tuple. Intent is not provider permission.
3. **Owner evidence:** bind the exact D ParticipantIntent/lineage clearance and current D ForgetFence; obtain I's exact single-use authorization terminal receipt. REVOCATION_WON or unknown I terminality means zero provider invocation. COMMIT_WON is valid only for this exact operation/digest and holds later I revocation behind the in-flight participant.
4. **COC reservation:** coordinator finalizes the exact ParticipantReservationRef after verifying the COC intent and I/D owner evidence. Reservation is not proof of sending and is not permission to bypass C's local gate.
5. **C final egress CAS:** immediately before any request bytes are released to the provider transport, the concrete transport-owning Adapter atomically validates current CGateGeneration, exact CAdmissionRef, reservation, I COMMIT_WON receipt, D clearance/current fence, exact request digest and one-use ProviderAttemptRef; it durably transitions the attempt to EGRESS_COMMITTED in the same C serialization domain used by CloseEgressGate.
6. **Transport invocation:** only the winner of the C final egress CAS may invoke the bound transport, exactly once for that attempt. The immutable approved bytes must be the bytes sent. No caller-visible SDK handle, retry middleware, redirect, stream continuation or failover may bypass a fresh C gate/causal authorization check.
7. **C outcome and closeout:** C records immutable CSubmitOutcome from actual provider/runtime observation, including actual provider receipt and InferenceRequestId when available. COC terminal proof and I/D closeout follow; a transport ACK alone is not C provider truth.

The coordinator intent/reservation and C egress commit are separate durable facts. A coordinator reservation cannot linearize against C Gate closure by itself. The final C CAS is the C egress ordering point; COC/I/D proofs are mandatory conjunctive preconditions, not replacements for that CAS.

### 13.3 Close/send race and crash windows

CommitEgress and CloseEgressGate MUST serialize on the same durable C authority and CGateGeneration:
- CommitEgress first: the exact provider attempt is pre-close in-flight, included in C close high-water/member root and must be reconciled using the same provider idempotency key.
- Close first: CommitEgress rejects; no provider request bytes are released.
- C admission first but COC intent/reservation or egress commit not reached: the request is captured in C's local ledger, but it is NOT a provider invocation. Close blocks it; after recovery it may proceed only under a fresh release/currentness check and the same stable operation identity.
- Crash after EGRESS_COMMITTED but before transport result: UNKNOWN/IN_DOUBT; never infer no-send and never retry as a new operation. Use provider-authoritative same-key lookup. If no authoritative lookup exists, retain IN_DOUBT and hold C/I/D barriers.
- Close must not report drained while any committed or ambiguous attempt lacks terminal evidence. If the API promises no bytes handed to transport after Close returns, Close waits for all earlier committed dispatch calls to cross a recorded transport-return boundary; bytes already accepted by transport cannot be recalled.

A process-local mutex is insufficient across Adapter replicas. All replicas for one provider-account/gate must share the same durable C serialization authority or an approved linearizable single-writer/consensus mechanism with split-brain fencing and crash recovery. If the authority is unreachable, no new provider bytes are sent.

### 13.4 Exact provider outcome states

The canonical C evidence must distinguish at least:
- NOT_DISPATCHED: no final egress commitment exists and authoritative C ledger proves transport was not invoked;
- EGRESS_COMMITTED: C committed the one-use send boundary; this alone does not prove provider acceptance;
- HANDOFF_CONFIRMED: transport/provider accepted the exact request under documented semantics;
- OUTCOME_UNKNOWN: send may or may not have crossed transport; blocks drain/release;
- OUTCOME_RECONCILED_SENT / OUTCOME_RECONCILED_NOT_SENT: only from authoritative same-key provider/transport evidence.

These states must map to C's existing CSubmitOutcome and CausalOrderTerminalProof schema under H's wire authority. Do not introduce a competing terminal enum without H schema review. Final Request Submitted and Full Applied evidence require C's existing final immutable request + actual successful submit boundary; reservation, intent, COMMIT_WON or EGRESS_COMMITTED alone is insufficient.

### 13.5 Required C conformance vectors

1. C Gate close wins against C admission: reject; no COC intent, reservation or provider call.
2. C admission wins but close precedes C egress CAS: admission is in close snapshot; zero provider bytes.
3. COC intent exists but I REVOCATION_WON: zero provider bytes.
4. COC intent exists but D fence/lineage clearance stale: zero provider bytes.
5. I COMMIT_WON + D clearance + reservation, then C close wins: zero provider bytes.
6. C egress CAS wins then close: attempt is included in close snapshot and same-key reconciled.
7. Payload changes after C admission/COC intent: digest conflict; zero provider bytes.
8. Crash after C egress CAS before transport invocation/result: UNKNOWN; no new attempt/key.
9. Lost provider response: same provider idempotency key lookup only.
10. Adapter SDK retry/redirect/failover attempts to send outside C gate: conformance failure.
11. Two Adapter replicas race Close/CommitEgress: one durable order, no split-brain send.
12. COC outage: no new protected intent/reservation/provider invocation; pre-existing ambiguous sends remain in-flight.
13. H wire ACK delayed or replayed after close: historical evidence only; cannot reopen C gate.
14. Provider outcome known but CSubmitOutcome persistence ACK lost: same C attempt lookup resolves immutable result.
15. Close returns while an earlier EGRESS_COMMITTED dispatch is still pending: reject if API promised transport-return drain; otherwise close receipt explicitly reports outstanding committed dispatch.

**Disposition:** C semantic composition is now explicit and aligned to Phase 3.6/3.6.9/3.8.2. Actual provider Adapter implementation, multi-replica serialization, H schema mapping, I/D exact receipt validation and all race/fault execution remain OPEN. No provider conformance, Full Applied, implementation sign-off or interface freeze is claimed.

### 中文规范摘要

C Provider Egress Gate 必须嵌入既有因果链：C 本地 Admission → COC ParticipantIntent → I 单次 COMMIT_WON 与 D 精确 Fence/Lineage Clearance → COC ParticipantReservation → C 本地最终 Egress CAS → Provider Transport → CSubmitOutcome → COC Terminal Proof。COC Reservation 不能代替 C Gate 的最终发送 CAS。C Gate Close 与 CommitEgress 在同一 C 持久化序列化域竞争：关闭先赢则零字节发送；发送提交先赢则进入 Close Snapshot 并以同一 Provider Idempotency Key 恢复。发送结果不明必须 UNKNOWN/IN_DOUBT，禁止新 Key 重发。多 Adapter 实例必须共享可证明的持久化线性化权威，不能依赖进程锁。


### 13.6 Currentness after I/D participant ordering

The final egress check MUST validate the authoritative outcome of the exact I authorization consumption, not perform a numeric comparison between PermissionEpoch and any C/D/COC generation. If I's sequencer records REVOCATION_WON before consumption, the send is rejected. If it records COMMIT_WON first, the exact participant remains in-flight and later revocation is ordered behind it until C terminal outcome. A later PermissionEpoch value alone does not rewrite that historical operation ordering; the Adapter must verify the exact receipt, digest, participant binding, issuer/key validity and that the I sequencer has not invalidated the receipt under its own policy.

The same rule applies to D: final egress validates the exact D participant/clearance and D fence relation. Fence-first blocks; participant-first holds the fence behind the unresolved participant. The Adapter MUST NOT infer ordering from timestamps or compare D and I counters.

This rule is not a reusable permission lease. The COMMIT_WON receipt is one-use, operation-bound, digest-bound and terminalized only through the C outcome/recovery path. It authorizes no other request, retry identity, redirect, stream continuation, provider account or model.
