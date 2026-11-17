# Phase 3.8.4 — C Exact Review: H Owner Snapshot Membership Proof Contract
# Phase 3.8.4 — C 精确审查：H Owner Snapshot Membership Proof 合同

- Owner perspective: C — Agent Integration / Provider Outcome Authority
- Review mode: delegated C-role review in the coordinating session; not an independent human Owner signature
- Decision: **ACCEPT WITH ENUMERATED C-OWNED CONDITIONS**
- Exact H Unified Schema: 1.2.11 / wire 1.3.0, Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- Exact H RecoveryJoin: 1.0.2, Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- C proof contract candidate: Blob `5e37185610869951c3b392c9ad143a72b4c702ac`
- H semantic module candidate: Blob `6710bd7876be5f2c60640f21090729b8859a7a3e`

## 1. Accepted semantics

C accepts the required proof ref/digest on each C owner-admission binding and unregistered owner-local admission, and accepts RecoveryJoin 1.0.2 as the structural envelope for C-owned membership evidence.

The C proof binds exact C Adapter/ProviderAccount authority, ledger/version/entry identity and digest, C admission/reservation/provider-attempt/outcome refs, C-local sequence namespace/value and relevant request/admission/reservation/attempt/outcome high-waters, immutable C snapshot/attestation refs and digests, C ledger root, C Gate generation, adapter/provider-account/egress-gate identity, scope and operation/request digest, provider idempotency namespace/key, applicable COC reservation or explicit null plus reason, provider receipt/lookup evidence where applicable, anti-rollback anchor, key status and C signature profile/key/version.

## 2. C authority and provider truth

C alone signs/verifies C membership proofs and authors CSubmitOutcome. Membership proves exact C ledger-row inclusion in a frozen C snapshot; it does not prove provider success, no-handoff, durable Memory Brain visibility, model execution, user delivery or exactly-once behavior.

C Provider Outcome remains one of HANDOFF_ACCEPTED, HANDOFF_REJECTED, NOT_INVOKED, UNKNOWN or IN_DOUBT under the exact immutable provider attempt/request/idempotency identity. UNKNOWN/IN_DOUBT blocks. A COC membership row, Storage receipt, I decision or D proof cannot synthesize provider truth.

## 3. Conditions

1. C must bind proof to the exact adapter/provider-account, immutable request boundary and provider idempotency namespace/key.
2. Provider outcomes require actual receipt or authoritative same-key lookup; a membership proof cannot substitute.
3. C Gate close and final transport handoff remain serialized by the transport-owning adapter; the test verifier callback does not prove the send-vs-close race.
4. Recovery keeps provider invocation/retry closed until exact Batch/Manifest S4 readback and semantic join.
5. C's snapshot proof signer, durable ledger, same-key lookup, anti-rollback and multi-replica adapter behavior remain unimplemented/unverified.
6. H verifier callback is a test seam until connected to C's owner proof authority.

## 4. C disposition

**ACCEPT WITH ENUMERATED C-OWNED CONDITIONS** for the exact candidate wire shape. No production provider conformance, universal exactly-once, C egress activation, JF-10 P0 closure or production activation is claimed.


## 5. H semantic payload validator follow-up

H now validates the actual proof payload against the exact C row and frozen snapshot and requires a C-authoritative signature verifier callback. Exact module Blob: `e26379d38825ee13d15f652d3bd019c4091da37d`; RecoveryJoin tests Blob: `3c61cc8c9d973a27f890e1452305e3fb0ad09f1a`. H CI Run `44051676055` passed 288 tests (266 passed, 22 skipped, 0 failed). The callback remains TEST-ONLY; C's real signer, provider-account ledger and same-key lookup remain unimplemented. C's ACCEPT WITH ENUMERATED CONDITIONS is unchanged.
