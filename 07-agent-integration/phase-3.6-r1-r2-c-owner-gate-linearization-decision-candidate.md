# Phase 3.6 — C Owner R1/R2 Provider Gate Linearization Decision Candidate
# Phase 3.6 — C Owner R1/R2 Provider Gate 线性化决议候选

- Owner perspective: C — Agent Integration / Provider Adapter and Outcome Authority
- Status: **CANDIDATE / NO INDEPENDENT OWNER APPROVAL**
- Source proposal: P-COC-R1-R2-TECH-001, blob `eac0b079f43da8c52521397e0cd256fda3fd3333`
- A review: blob `fdf63550696948f77dc37c0a3788276ac4d525f5`, Issue #14 R1/R2
- Scope: C adapter/provider-account admission, reservation, provider attempt and C-only outage-gate release.

## 1. C authority and scope key / C 权限与作用域键

C owns the final serialization boundary at the transport-owning adapter that can cause provider handoff. The scope key binds provider/account, adapter instance or partition, egress gate, operation/request digest and idempotency namespace. I/D/COC state is an admission prerequisite, not C's provider outcome authority.

C 拥有可能触发 Provider Handoff 的传输 Adapter 最终串行化边界。作用域键绑定 Provider/Account、Adapter、Egress Gate、Operation/Request Digest 与 Idempotency Namespace。I/D/COC 状态是准入前置条件，不替代 C 的 Provider Outcome 权威。

## 2. Exact send-vs-close linearization / 发送与关闭的精确线性化点

The final provider send and C gate-close request MUST serialize through the same adapter-owned durable sequencer/transaction or equivalent atomic gate primitive. Immediately before any irreversible handoff:
1. validate exact immutable final request digest, provider/account/adapter identity and stable idempotency key;
2. require authoritative I decision `COMMIT_WON` and all required D predicates; any other I terminal outcome forbids provider invocation;
3. atomically check the C egress gate OPEN and append a durable provider-attempt/admission record with a unique C-local sequence;
4. commit the admission record before handing bytes to the transport.

A gate-close request uses the same serialization boundary to append the close request and close the gate. If close linearizes first, send is rejected with authoritative NOT_INVOKED proof. If send admission linearizes first, its durable attempt remains in the frozen in-flight set and must be reconciled by the exact provider idempotency key. No read-OPEN-then-send sequence outside the shared boundary is allowed.

The durable admission commit is the C send-admission linearization point; it does not itself prove provider handoff. The immutable CSubmitOutcome is written only from authoritative transport/provider evidence or same-key lookup. UNKNOWN/IN_DOUBT blocks retries as a new operation.

发送准入与 Gate 关闭必须通过同一 Adapter 权威串行化边界。关闭先线性化则拒绝发送并给出 NOT_INVOKED 证明；发送准入先线性化则将 attempt 纳入冻结在途集合，并按同一 Provider Idempotency Key 对账。准入提交不等于 Provider 已接收；Outcome 只能由真实传输证据或同 Key 权威查询生成。

## 3. C in-flight set and recovery rounds / C 在途集合与恢复轮次

Before returning send-admission success, C persists CAdmissionRef/ProviderAttemptRef, exact final request digest, provider/account/adapter, idempotency namespace/key reference, participant/reservation binding, gate generation, C-local sequence and transport phase. C seals request/admission/reservation/attempt/outcome high-waters and complete query projection, pagination, count and ordered-set roots.

Any new attempt/request or scope change after the seal remains blocked and requires a successor Recovery Cutoff Batch. Every admitted attempt must be joined to the exact COC manifest or remain an explicit owner-local admission; missing or ambiguous provider handoff remains UNKNOWN/IN_DOUBT and prevents release.

在封印后出现新请求或 Attempt 时必须保持阻断并进入后续 Recovery Cutoff Batch。所有已准入 Attempt 必须进入精确 COC Manifest 或作为 Owner-local Admission 明确列出；不明确的 Provider Handoff 保持 UNKNOWN/IN_DOUBT。

## 4. C-only release and evidence / C 独立释放与证据

C releases only its own outage egress-admission gate after exact Batch-before-Manifest S4 readback, full C ledger/manifest reconciliation, stable same-key provider lookup for ambiguous attempts and unchanged gate/scope/high-water CAS. C cannot release I or D gates. A released outage gate does not bypass the per-operation I COMMIT_WON, D clearance, C idempotency or provider policy checks.

Required tests include send-vs-close in both serialization orders; crash after admission commit before transport write; crash after transport write before outcome ACK; same-key lookup after lost ACK; duplicate same-key/different-digest conflict; high-water advance during reconciliation; and negative proof that timeout/worker death is not NOT_INVOKED.

## 5. Decision boundary / 决议边界

This is a coordinator-authored C-role candidate, not independent C Owner approval. C must independently adopt/amend/reject and pin exact source versions. The real adapter sequencer, provider-specific idempotency/lookup, durable attempt/outcome ledger, transport fault injection and production provider verification remain NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED. No exactly-once or production activation is claimed.
