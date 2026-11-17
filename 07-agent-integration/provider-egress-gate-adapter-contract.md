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
