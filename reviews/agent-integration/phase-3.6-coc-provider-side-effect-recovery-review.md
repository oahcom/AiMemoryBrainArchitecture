# C Owner Review — COC Provider Side-effect & Recovery Contract

- Reviewer: C — Agent Integration Architect
- Review target: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design.md`
- Exact target: commit 9a975f665ee60f4551effe0104ea8f867716d9dd; blob cd5566b3d99b5204401ac713a5bb2dcf89a02726
- Decision: **ACCEPT_WITH_CONDITIONS**
- Scope: C provider/runtime submission boundary, provider idempotency and C-owned outcome evidence only.

## 1. Accepted C-side invariants

The proposal correctly says COC records C-signed actual provider outcome evidence and must not infer provider success from timeout, retry, reservation, coordinator state or an ACK. The durable participant registry and pre-cutoff participant enumeration are useful for ensuring a provider side effect cannot disappear from recovery. UNKNOWN/IN_DOUBT must remain durable and block relevant I/D barriers.

C's authoritative contract remains: exact final request identity/digest and provider idempotency key are frozen before side effect; C alone records the actual provider/runtime outcome, including actual provider receipt and InferenceRequestId where supplied. Provider ACCEPTED requires determinate handoff evidence; definitive REJECTED requires proof of no handoff. Timeout, process death, lost response or contradictory provider evidence remains UNKNOWN/IN_DOUBT. Retry must use the same transaction/reservation/provider key and must never mint a new operation identity.

## 2. Binding gaps

### C-COC-01 — C outage admission behavior is not specified at the owner-local gate layer (BLOCKING)

§5.2 describes only I and D durable local pending gates, while §5.1 states C/I/D gates close. Add an explicit C fail-closed rule: when COC quorum, prefix or relevant cutoff state cannot be authoritatively confirmed, C does not create/accept a new protected intent/reservation and does not invoke the provider for any protected operation whose common causal-order status is unknown. C must not infer that no I revocation or D fence exists because COC is unavailable.

### C-COC-02 — Recovery inventory must account for all C side-effect states (BLOCKING)

For every participant at/before P, the recovery manifest must include C-side state: not invoked, invocation in progress, definitive accepted, definitive rejected/no handoff, or unknown/ambiguous. It must bind provider idempotency key namespace, exact request digest/boundary, provider receipt/lookup ref and C evidence digest. A missing provider outcome remains unresolved; it cannot be treated as safe abort.

### C-COC-03 — Same-key recovery contract is provider-specific (BLOCKING FOR PRODUCTION)

The protocol's generic idempotency rule is necessary but not sufficient. Provider idempotency-key scope, retention window, lookup consistency, duplicate-submit behavior, and whether an ambiguous request can be queried without reissuing the side effect must be defined per provider adapter. If the provider cannot prove same-key recovery, the operation remains IN_DOUBT and C cannot claim exactly-once behavior.

### C-COC-04 — C evidence is distinct from Storage resolution (BLOCKING)

A resolved Storage XID/PublicationReceipt does not prove provider handoff. Conversely, provider acceptance does not prove Storage visibility or G Applied. The participant reconciliation record must keep CSubmitOutcomeRef, Storage outcome, I decision and D barrier as separate typed evidence; no aggregate status may synthesize one from another.

## 3. Recovery Cutoff Batch assessment

C accepts the batch as the common cutoff barrier only if:
- every pre-P participant is enumerated from the verified quorum prefix;
- the manifest is complete, deterministic and bound to the batch digest;
- every participant's C side-effect state is authoritatively resolved or explicitly IN_DOUBT;
- requests after owner high-water remain gated and are included in a later batch;
- COC does not return to SERVING until the manifest and all required owner reconciliations are durably recorded.

The current algorithm appends the batch before participant enumeration, despite defining enumeration high-water as part of the batch. This must be corrected by precomputing the manifest or introducing a separate immutable batch-bound manifest record.

## 4. Owner-local Gate assessment

C's runtime gate is not an I/D authority gate. It is a fail-closed side-effect admission rule: no new protected submit while the common coordinator state or applicable I/D cutoff prefix cannot be confirmed. Existing in-flight provider requests must not be cancelled or replayed blindly; they must be looked up using the same provider key and reconciled to exact C evidence. C cannot reopen I or D gates.

## 5. JF-10 same-XID bridge assessment

C accepts that COC records the JF-10 participant lifecycle but does not decide I terminality or Storage resolution. C requires exact operation ID/digest, ParticipantIntentRef, owner boundary, PolicyDomainRef, DB identity, preallocated XID and provider idempotency key to remain bound. If I has a durable decision while COC is unavailable, Storage follows the same-XID I decision; C later records only its own actual provider outcome. No new XID or provider key is minted to escape UNKNOWN.

The JF-10 bridge must remain a separately accepted I/Storage/D contract. C's review does not accept COC as a second transaction coordinator or approve I's owner-final-gate implementation.

## 6. Required C tests

- C-COC-01: COC unavailable before reservation; no provider call.
- C-COC-02: COC lost after reservation but before provider invocation; no call unless exact reservation/prefix is authoritatively recoverable.
- C-COC-03: provider request crosses boundary then C crashes before outcome append; same provider key authoritative lookup, no retry-as-new.
- C-COC-04: provider response lost; same-key lookup yields accepted/rejected/unknown without duplicate side effect.
- C-COC-05: recovery batch manifest includes provider-invoked but outcome-unknown participant; C/I/D barriers remain held.
- C-COC-06: provider definitive rejection versus timeout; only definitive no-handoff may be terminal rejection.
- C-COC-07: Storage resolved but C provider outcome unknown; do not synthesize C terminality.
- C-COC-08: C evidence replay with same ID/digest idempotent; changed digest conflict.
- C-COC-09: provider idempotency key namespace/retention mismatch; fail closed.
- C-COC-10: coordinator restore with pre-P C side-effect participant omitted; remain RESTORE_FENCED.

**Conclusion:** C accepts the design direction with binding C-side conditions. The exact proposal is not production-ready and should be revised before joint freeze. No provider integration, C conformance, implementation or deployment pass is claimed.
