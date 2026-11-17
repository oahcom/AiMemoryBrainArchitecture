# Phase 3.8.23 — C Exact Consumer Decision: G Applied Persistence Identity Join

- Role: delegated C Owner review; not an independent human Owner signature.
- Decision: **ACCEPT WITH ENUMERATED EXCEPTIONS** for the C-owned identity semantics below.
- G target EN Blob: `bd297873bc1e593280484a43cb44b56058d9c4ff`
- G target zh-CN Blob: `82553a47fae2d5e796e0742b46231afe465e75b2`
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C normative Provider Submit Outcome Blob: `819705037da89834e10b6dd2ec6e66c1b8c70886`
- C Final Request Evidence Blob: `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`
- C causal-order addendum Blob: `45a48249717c8cddb07ab96197730ef93d406c22`

## 1. Decision scope

This decision reviews only the C/G identity join in the exact G Phase 3.8.22 blobs above. It does not accept H wire mapping, COC/Storage restore semantics, I/D ordering, G persistence implementation, or global Applied freeze. Any change to either G blob invalidates this decision.

## 2. Field-level decisions

### 2.1 CProviderAttemptIdentity — ACCEPT

G tuple:
`(issuer_authority_ref, sequence_namespace_ref, ProviderAttemptRef, ProviderAttemptGeneration, ProviderRef, ProviderAccountRef, IdempotencyNamespaceRef, IdempotencyKeyRef, RequestDigest)`

C confirms the semantic components are supported by CSubmitOutcome 1.0.1:
- `issuer_authority_ref` + `sequence_namespace_ref`: issuer and owner-ledger sequence namespace. Sequence namespace is part of the issuer's authoritative record scope, not a global sequence.
- `ProviderAttemptRef` + `ProviderAttemptGeneration`: stable logical attempt and explicit generation.
- `ProviderRef` + `ProviderAccountRef`: provider and authenticated account/tenant scope.
- `IdempotencyNamespaceRef` + `IdempotencyKeyRef`: stable provider key namespace and key reference.
- `RequestDigest`: exact immutable final request digest. A changed request digest means a different provider-attempt scope and MUST NOT be retried under the old idempotency identity.

C requires the consumer to retain the exact C-issued references and compare the complete tuple; no display-name normalization, account inference, or key reconstruction is allowed.

### 2.2 COutcomeRecordIdentity — ACCEPT

G tuple:
`(issuer_authority_ref, sequence_namespace_ref, record_ref, record_sequence)`

C confirms this is the immutable ledger observation identity. It is distinct from ProviderAttempt identity. `payload_digest` and `OutcomeEvidenceDigest` are content-integrity values, not identity fields.

Same record identity + same payload digest + same immutable tuple = exact replay. Same record identity with changed payload digest or changed immutable tuple = integrity conflict; quarantine and no promotion. C record sequence is scoped to its issuer/sequence namespace; consumers must not compare it numerically with COC, I, D or Storage positions.

### 2.3 RequestDigest and digest separation — ACCEPT

`RequestDigest` is included in ProviderAttempt identity because C's provider idempotency key is scoped by provider/account/endpoint/model semantics and immutable request digest. This does not authorize putting `payload_digest`, `OutcomeEvidenceDigest`, H P0 digest, H receipt digest, COC participant digest or G EvidenceSetDigest into GAppliedIdentity.

C P0/object digest and H envelope P0 digest are separate cryptographic domains. A digest value never substitutes for issuer authentication, ledger inclusion, semantic outcome validation or exact source-record identity.

### 2.4 Late receipt / successor observation — ACCEPT WITH CONDITION

C accepts append-only successor observations under the same ProviderAttempt identity only if:
1. each successor has a new immutable COutcomeRecordIdentity and C owner-ledger position;
2. `PriorObservationRef`, `SupersedesObservationRef` and/or `ReconciliationParentRef` establish the exact lineage (as applicable);
3. provider/account/key/request digest and attempt generation remain unchanged;
4. C semantics identify it as lookup/reconciliation/late receipt, not a second physical send.

A successor may enrich the G evidence revision for the same logical G Applied identity. It MUST NOT rewrite the original record or create a new ProviderAttempt merely to escape UNKNOWN/IN_DOUBT.

### 2.5 UNKNOWN / IN_DOUBT / retry — ACCEPT

C confirms UNKNOWN and IN_DOUBT are nonterminal. Recovery MUST query/reconcile the same provider idempotency key and exact request digest. No retry-as-new, key rotation, account/region/model failover, SDK automatic retry, redirect or transport reconnect may bypass C's egress gate. If provider-authoritative idempotency/lookup is unavailable, ambiguity remains IN_DOUBT and automatic retry is disabled.

Only a determinate C `HANDOFF_ACCEPTED` with required provider and participant evidence is eligible for G Full Applied evaluation. C outcome alone is never G Applied.

## 3. Exceptions / open dependencies

1. H must accept and implement a distinct H Delivery Evidence mapping; C's acceptance does not approve H's schema or validator.
2. C must re-review any future H schema/validator mapping that duplicates C-owned fields, ensuring exact equality to the immutable C object and no transfer of provider truth to H.
3. COC/Storage must separately accept G's participant/GID/restore joins.
4. This delegated review is not independent human C Owner approval, provider integration evidence, or runtime conformance.

## 4. Disposition

**C identity semantics: ACCEPTED for the exact G Phase 3.8.22 blobs, with the conditions and exceptions above. C/H wire interoperability: NOT ACCEPTED / NOT VERIFIED. G persistence implementation: NOT VERIFIED. Global Applied freeze: NO. Production activation: NOT AUTHORIZED.**
