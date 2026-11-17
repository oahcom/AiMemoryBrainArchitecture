# H Applied Delivery Evidence 1.0.0 — Exact C/G/I Consumer Mapping Review

- Review ID: ABR-INTEGRATION-004
- H branch: `session-h-bmcp-protocol@6608cde89d959257db612d8ff8080f631333f3f3`
- H Schema Blob: `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`
- H Validator Blob: `2f6de24eea737cf75a16ead7495bea4627bb1bb4`
- H Phase 3.8.24 candidate report Blob: `f193113f142506b0d0848c7131f780db93a83aef`
- G Phase 3.8.22 contract Blob: `bd297873bc1e593280484a43cb44b56058d9c4ff`
- C Phase 3.8.23 identity review Blob: `4860c627b4d7e84e23fb39ad83411674f3b88c7b`
- CSubmitOutcome 1.0.1 Schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- Status: **Integration consumer review only; not C/G/I Owner acceptance**

## 1. Disposition

H Applied Delivery Evidence 1.0.0 correctly separates Adapter Delivery Evidence into a distinct message family from Unified 1.2.15 Gateway Attestation. Its HDeliveryBindingIdentity and HObservationRecordIdentity field shapes broadly match G Phase 3.8.22, and the Schema/Validator/11-test candidate suite has passed CI.

However, the candidate does not establish that C/G/I have accepted the complete wire contract. Three exact Owner decisions remain necessary:

1. The H Schema carries opaque C Submit Outcome / Outcome Record references, a record sequence and payload digest; it does not expand the complete CProviderAttemptIdentity / COutcomeRecordIdentity required by G into first-class fields. The H Validator exposes only `verify_c_final_boundary`, not an explicit C Owner Ledger Record / C Outcome Identity binding callback. This may be valid if opaque refs resolve uniquely to authenticated immutable C Owner records, but that requires an exact C acceptance and callback contract.
2. `integrity_proof_ref` is required by the Schema but excluded from the H P0 signed/digest projection; the current Validator has no separate integrity-proof-reference verifier. It must be decided whether this is intentionally untrusted/advisory metadata or whether it must be bound by signature/separate proof.
3. H `adapter_capability_epoch` is not I `PermissionEpoch`. The current H 1.0.0 Schema contains neither I PermissionEpoch nor CommitAuthorizationReceipt. G/I must decide whether authorization evidence is joined through an independent I record at the final request boundary or whether the H message must carry an authenticated I epoch/reference. Capability epoch must never be treated as permission epoch.

Disposition: **H 1.0.0 is a runnable conformance candidate, but exact C/G/I consumer mapping remains OPEN; Global Applied remains NOT FROZEN / NOT PROVEN.**

## 2. H identity fields already aligned

### 2.1 HDeliveryBindingIdentity

H Phase 3.8.24 defines:
`(adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch)`

All seven fields are required and present in H Schema properties:
- `adapter_instance_ref`
- `runtime_session_ref`
- `delivery_id`
- `delivery_attempt_id`
- `inference_request_id`
- `final_request_boundary_id`
- `adapter_capability_epoch`

This matches G Phase 3.8.22's HDeliveryBindingIdentity field set. G must still accept the issuer, scope, session binding, final boundary and capability-epoch currentness semantics exactly; Schema requiredness proves field presence, not trusted provenance.

### 2.2 HEvidenceIdentity

`(HDeliveryBindingIdentity, evidence_kind)`

H Schema's `evidence_kind` is a required closed enum, which is directionally correct. A new evidence kind should be a new evidence slot/revision under the same delivery binding; it must not create a new DeliveryAttempt or G Applied identity.

### 2.3 HObservationRecordIdentity

H Phase 3.8.24 defines:
`(issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence)`

All seven fields are required and present in H Schema. The Validator uses this as observation identity and delegates NEW / SAME_DIGEST_REPLAY / CONFLICT to `commit_observation`; the production durable uniqueness ledger is not implemented.

## 3. C identity mapping remains open

G Phase 3.8.22's C identity contracts are:

- `CProviderAttemptIdentity = (issuer_authority_ref, sequence_namespace_ref, ProviderAttemptRef, ProviderAttemptGeneration, ProviderRef, ProviderAccountRef, IdempotencyNamespaceRef, IdempotencyKeyRef, RequestDigest)`
- `COutcomeRecordIdentity = (issuer_authority_ref, sequence_namespace_ref, record_ref, record_sequence)`

CSubmitOutcome 1.0.1 Schema contains these as C-owned properties with independent field/type constraints.

H Applied 1.0.0 currently carries only:
- `c_submit_outcome_ref`
- `c_outcome_record_ref`
- `c_outcome_record_sequence`
- `c_outcome_payload_digest`

H Schema does not explicitly contain C issuer authority, sequence namespace, ProviderAttemptRef/generation, ProviderRef/account, IdempotencyNamespace/Key or RequestDigest. Do not treat `c_outcome_payload_digest` as `RequestDigest` or `OutcomeEvidenceDigest`; these belong to different identity/evidence domains.

### Two acceptable implementation paths (C/G must explicitly choose)

**Option A — Full typed tuple:** an H 1.0.1 successor explicitly carries the fields required for full CProviderAttemptIdentity and COutcomeRecordIdentity, and signs them in H P0.

**Option B — Opaque authenticated reference:** retain H's current reference shape, but C must define the uniqueness, issuer/namespace scope, version, record sequence, payload digest, Owner signature/ledger inclusion and immutable-resolution semantics of `c_submit_outcome_ref` / `c_outcome_record_ref`. H's C verifier callback must validate these and return VALID/INVALID/UNKNOWN. Merely checking that a string is non-empty is insufficient.

The current H Validator's `verify_c_final_boundary(envelope)` callback could be implemented to perform additional checks, but its interface/report does not explicitly require validation of C OutcomeRecordIdentity, CProviderAttemptIdentity, C Owner Ledger inclusion and C outcome payload digest. Do not infer those checks from the callback name alone.

## 4. Exact C Final Request Boundary crosswalk

H fields:
- `inference_request_id`
- `final_request_boundary_id`
- `final_request_boundary_type`
- `c_submit_outcome_ref`
- `c_outcome_record_ref`
- `c_outcome_record_sequence`
- `c_outcome_payload_digest`

CSubmitOutcome 1.0.1 fields:
- `ActualInferenceRequestId`
- `FinalRequestBoundaryRef`
- `FinalRequestBoundaryType`
- `RequestDigest`
- `Outcome`
- `payload_digest`
- `OutcomeEvidenceDigest`
- C owner/attempt/record identity fields

C Owner must confirm these mappings field by field:
1. Whether H `inference_request_id` must equal C `ActualInferenceRequestId`, and how missing/not-applicable values are handled.
2. How H `final_request_boundary_id` binds to C `FinalRequestBoundaryRef`, including reference type/authority namespace normalization.
3. Whether H `final_request_boundary_type` maps one-to-one to C values and how unknown values fail closed.
4. Whether H `c_outcome_payload_digest` refers exactly to C `payload_digest` or another digest; it must not be confused with `RequestDigest` or `OutcomeEvidenceDigest`.
5. Only a determinate C `HANDOFF_ACCEPTED` with complete provider/participant evidence may become an input to G Full Applied evaluation; UNKNOWN/IN_DOUBT/NOT_INVOKED/REJECTED cannot promote Full Applied.

C Phase 3.8.23 accepts only C-owned identity semantics in G Phase 3.8.22 and explicitly says C/H wire interoperability is NOT ACCEPTED / NOT VERIFIED. It cannot be broadened into acceptance of H 1.0.0.

## 5. Integrity proof reference in H P0 projection

The H Validator:
- excludes `payload_digest`, `signature` and `integrity_proof_ref` from P0;
- passes `envelope` and P0 bytes to `verify_signature`;
- has no `verify_integrity_proof_ref` callback;
- while the Schema requires `integrity_proof_ref` as a string.

This creates a normative question: if the reference affects evidence interpretation, integrity validation or later audit, but is not in signed P0, an intermediary can replace the reference without changing the P0 digest. If it is only a non-authoritative hint, the contract must state that consumers cannot trust it. If it is an authoritative evidence locator, it must be signature-bound or bound by a separately signed/immutable ledger proof.

The current 11-test suite does not separately prove that mutation of `integrity_proof_ref` is rejected or semantically harmless. H should add a mutation test and an exact decision.

## 6. I PermissionEpoch versus H CapabilityEpoch

- H `adapter_capability_epoch`: H/Adapter capability-state namespace.
- I `PermissionEpoch`: I policy-domain authorization-currentness namespace.
- They cannot be compared, converted or substituted.

I Phase 3.6 requires PermissionEpoch to be revalidated at protected irreversible commit/disclosure boundaries; the I Phase 3.8 receipt proposal further binds a single-use CommitAuthorizationReceipt to D PublicationParticipantRef and StorageVisibilityParticipantRef.

H Applied 1.0.0 has no explicit PermissionEpoch / CommitAuthorizationReceipt field. G/I must decide:
- whether H evidence is linked to a separate authoritative I record through an authenticated final-boundary reference;
- if so, how H/G prove the join is exact, current and for the same Scope/Actor/Audience/operation;
- if H must carry PermissionEpoch unchanged, it needs a distinct typed field/reference and cannot reuse `adapter_capability_epoch`.

## 7. Required exact consumer decisions

| Authority | Required confirmation | Current status |
|---|---|---|
| H | Semantics of C opaque refs, complete C callback checks, integrity_proof_ref authentication, production canonicalization/profile | OPEN |
| C | Exact H 1.0.0 to CSubmitOutcome 1.0.1 identity/final-boundary/digest mapping | OPEN; 3.8.23 reviewed only G's C-owned tuple |
| G | Exact mapping of HDeliveryBindingIdentity/HEvidenceIdentity/HObservationRecordIdentity to GAppliedIdentity, Full Applied predicate and durable evidence join | OPEN; 3.8.22 is a design draft |
| I | Association of PermissionEpoch/CommitAuthorizationReceipt with H delivery/final boundary and trust profile | OPEN; I 3.8 technical contract remains proposal |
| Storage/COC | Binding H/C evidence references to the same GID/participant/terminal outcome | OPEN |

## 8. Disposition

- H schema shape: **CANDIDATE IMPLEMENTED**.
- H local validator/test suite: **BOUNDED CI PASS**.
- HDeliveryBindingIdentity / HEvidenceIdentity / HObservationRecordIdentity field shape: **STRUCTURALLY ALIGNED WITH G**.
- Authenticated binding of CProviderAttemptIdentity / COutcomeRecordIdentity through opaque references: **UNRESOLVED**.
- `integrity_proof_ref` P0 exclusion semantics: **UNRESOLVED / SECURITY REVIEW REQUIRED**.
- I PermissionEpoch join: **UNRESOLVED**.
- Exact C/G/I consumer acceptance: **NOT FOUND**.
- Global Applied / Production activation: **NOT FROZEN / NOT AUTHORIZED**.

This is an integration technical finding, not a C/G/I Owner decision. It does not modify H/C/G/I Owner branches or authorize schema freeze, merge or production activation.
