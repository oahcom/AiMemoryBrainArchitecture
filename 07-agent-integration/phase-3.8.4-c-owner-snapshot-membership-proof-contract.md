# Phase 3.8.4 — C Owner Snapshot Membership Proof Contract
# Phase 3.8.4 — C Owner Snapshot Membership Proof 合同

- Owner: C — Agent Integration / Provider Outcome Authority
- Status: **PROPOSED / CANDIDATE ONLY — NOT APPROVED OR FROZEN**
- Applies to C admissions, reservations, provider attempts and outcomes in H Unified Manifest 1.2.11 / wire 1.3.0.

## 1. Authority boundary

C alone attests C request/admission/reservation/provider-attempt/provider-outcome ledger rows and provider-boundary observations. A COC ParticipantIntent, Storage receipt, I authorization, D fence proof or H transport ACK cannot synthesize C Provider Outcome.

## 2. Proof required for each C row

Every C row represented in a COC participant binding or as an unregistered owner-local admission MUST carry one immutable `CAdmissionSnapshotMembershipProof` binding:

- `proof_ref`, `owner_kind=C`, C Adapter/ProviderAccount authority ref;
- exact C ledger ref/version, row/entry ref and entry digest;
- exact C admission/reservation/provider-attempt/outcome refs and row kind;
- C-local sequence namespace/value and captured request, admission, reservation, provider-attempt and provider-outcome high-waters as applicable;
- immutable C snapshot ref/digest, snapshot-attestation ref/digest and complete C ledger root;
- C Gate ref/generation, adapter/provider-account/egress-gate identity and scope binding digest;
- operation identity/digest, immutable final request digest, provider idempotency namespace/key ref;
- COC ParticipantIntentRef/reservation ref or explicit null plus absence reason;
- provider receipt/lookup evidence ref/digest when the row is an outcome;
- independent C anti-rollback anchor, key-status generation and C signature-profile/key/version/signature refs.

All C counters remain within their C-owned namespace. No comparison to I/D counters or COC indexes is permitted.

## 3. Membership and completeness

The proof attests that the exact row is included in the frozen signed C snapshot and at/below its applicable C-local high-water. Completeness additionally requires the exact provider/account/adapter query projection, pagination completion, counts, ordered set root, request/admission/reservation/provider-attempt/provider-outcome high-waters and anti-rollback checkpoint.

A membership proof does not prove provider success. Provider truth remains a separate immutable CSubmitOutcome derived from actual provider receipt or authoritative same-key lookup. UNKNOWN/IN_DOUBT stays blocking. A missing COC ParticipantIntent is represented as explicit null plus reason; it is not repaired by fabricating a participant. Empty C sets require a separate signed COMPLETE_EMPTY proof.

## 4. C signature projection and verification

C owns the proof P0, canonical digest preimage and signature profile. It binds every field in §2 plus issuer/subject/audience/purpose, adapter/provider-account/egress-gate identity, gate generation, immutable request boundary, idempotency namespace/key and snapshot roots. Only signature bytes/ref and explicitly derived digest fields are excluded.

The verifier checks C key status, signature, exact adapter/provider-account scope, snapshot membership, high-water inclusion and anti-rollback anchor. H cannot infer provider outcome from the membership proof.

## 5. Gate/recovery semantics

C Gate Release validates all C membership proofs and reconciles every reservation, attempt and outcome in the frozen C snapshot. The final provider send-vs-close linearization remains owned by the transport-owning C Adapter. Recovery must keep provider invocation/retry closed until Batch and Manifest S4 readback and semantic join complete. Ambiguous handoff is reconciled only using the same immutable request/attempt and provider idempotency key; if the provider lacks authoritative same-key lookup, IN_DOUBT may persist indefinitely.

A membership proof is not an egress permit, provider outcome, successful delivery or exactly-once guarantee.

## 6. Decision boundary

This is a C-role proposal in the coordinating session, not independent human C Owner approval. Provider-specific key custody, same-key lookup authority, receipt authenticity, durable C ledger/adapter serialization and real provider fault-injection remain unimplemented/unverified. No production provider acceptance or production activation is claimed.
