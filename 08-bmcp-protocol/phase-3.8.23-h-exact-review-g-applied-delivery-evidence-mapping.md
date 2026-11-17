# Phase 3.8.23 — H Exact Consumer Decision and Delivery Evidence Mapping for G Applied Persistence

- Role: delegated H Owner review; not an independent human Owner signature or I security registration.
- Decision: **ACCEPT WITH ENUMERATED EXCEPTIONS** for identity semantics; **WIRE MAPPING NOT FROZEN**.
- G target EN Blob: `bd297873bc1e593280484a43cb44b56058d9c4ff`
- G target zh-CN Blob: `82553a47fae2d5e796e0742b46231afe465e75b2`
- H Unified 1.2.15 schema Blob: `860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- H Gateway validator Blob: `9cc426d4c26deb452f39daff34c1008dd535e969`
- H Gateway validator tests Blob: `9a5051b001a6e59d7b71e6dd175e84bb7d01d252`
- H Adapter/Applied attestation contract Blob: `74be8374a67da385a5f0f8e34c7aef2b38b72bcf`
- H Phase 3.8.21 exact mapping note Blob: `2dc30f193d9c4f4bdc05ca4c137103687db28924`

## 1. Critical boundary finding

Unified 1.2.15 + `gateway_attestation_validator.py` authenticate the H Gateway's attestation of a `C_PROVIDER_OUTCOME_RECORDED` envelope, including origin transport receipt, H signing sequence and duplicated C outcome fields. This is not the same message/evidence family as Adapter/Runtime Applied Delivery Evidence.

The gateway validator P0 allowlist is explicit and rejects unlisted fields. It is therefore incorrect to append Adapter delivery fields to that existing P0 projection without a versioned profile/schema successor and new vectors. It is also incorrect to treat the H Gateway's `message_id/message_nonce/signing_record_sequence` as the immutable identity of an Adapter evidence observation.

H §11.1 candidate mapping already names delivery fields, but that candidate table is not itself the Unified 1.2.15 schema or an executable validator mapping. The prior G observation that the full delivery tuple is absent from the 1.2.15 C Provider Outcome branch is therefore upheld, with this refinement: the fields are described in H's candidate document but are not wired into the exact 1.2.15 message schema/validator path.

## 2. Field-level decisions

### 2.1 HDeliveryBindingIdentity — ACCEPT AS H-OWNED SEMANTIC TUPLE

`(adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch)`

H confirms:
- `adapter_instance_ref`: exact H-registered Adapter instance, not merely Adapter product/build.
- `runtime_session_ref`: authenticated Runtime Session binding; never inferred from transport connection alone.
- `delivery_id` + `delivery_attempt_id`: G-issued Delivery and exact non-superseded attempt; H preserves both and does not create G identity.
- `inference_request_id`: actual Runtime/Provider-assigned request ID; never synthesized from DeliveryId.
- `final_request_boundary_id`: exact C-observed successful submit boundary; H cannot mint or substitute it.
- `adapter_capability_epoch`: H-issued capability epoch bound to the exact Adapter instance/session and negotiated profile.

Required companions for a Full Tier-1 observation include `runtime_instance_ref`, `adapter_ref`, `context_id`, `context_version`, `materialized_context_version`, `final_request_boundary_type`, exact request/managed-region digest profile, coverage and integrity references. They are evidence predicates, not additional components of the stable delivery key unless G explicitly versions that key.

### 2.2 HEvidenceIdentity — ACCEPT

`(HDeliveryBindingIdentity, evidence_kind)`

`evidence_kind` is a closed, versioned enum controlled by H's evidence profile. A new evidence kind is a new evidence slot/revision under the same delivery binding; it does not create a new DeliveryAttempt or G Applied identity. Unknown critical kinds fail closed.

### 2.3 HObservationRecordIdentity — ACCEPT WITH MAPPING CONDITION

`(issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence)`

This identifies one immutable authenticated H observation, not the logical delivery. The issuer/sender fields are exact verifier-resolved identities. Message ID + nonce provide envelope replay identity; signing sequence is scoped to its namespace and anti-rollback checkpoint. Timestamp is descriptive only.

Same observation identity + same canonical H P0 digest + same immutable receipt/result ref = exact replay. Same observation identity with changed digest or changed immutable tuple = conflict/quarantine. A legitimate successor requires a new observation identity and an authenticated H owner-ledger link to the same HDeliveryBindingIdentity.

### 2.4 Digest and replay separation — ACCEPT

H P0 digest is content integrity for one signed H envelope. It is not part of HDeliveryBindingIdentity, HEvidenceIdentity or GAppliedIdentity. The gateway message replay ledger, Adapter evidence observation ledger and G Applied uniqueness ledger are separate idempotency domains. No layer may substitute its replay key for another layer's logical identity.

## 3. Exact schema/validator mapping decision

H will not mutate the immutable Unified 1.2.15 artifact or widen the existing C Provider Outcome P0 allowlist in place.

The correct successor is a separately versioned H Applied Delivery Evidence message family (candidate schema ID `bmcp.applied-delivery-evidence`, artifact revision `1.0.0`) with:
- required typed properties for every HDeliveryBindingIdentity component;
- required `evidence_kind` and immutable observation identity fields;
- authenticated issuer/sender, signature profile, signing sequence namespace/sequence, message ID/nonce, audience and H P0 digest/signature;
- explicit exact mapping of H document §11.1–11.6 candidate fields;
- strict unknown-critical-field rejection and explicit absent/null semantics;
- P0 allowlist covering every present field except the exact derived digest/signature/integrity-reference exclusions;
- validator checks for schema revision, protected identity binding, capability epoch, C final-boundary equality, G delivery/attempt equality, digest integrity, replay conflict and successor lineage.

This is a normative mapping decision, not a claim that the successor schema, validator, SDK or tests have already been implemented. The exact successor artifact paths, Blob SHAs, P0 vectors and CI run must be added in a follow-up H implementation commit before H can mark wire mapping complete.

## 4. Enumerated exceptions / gates

1. H Unified 1.2.15 Gateway Validator remains valid only for its current C Provider Outcome gateway-attestation purpose; no Adapter Delivery Evidence acceptance is inferred.
2. The separate H Applied Delivery Evidence schema/validator is specified but **NOT YET IMPLEMENTED / NOT VERIFIED**.
3. C must review exact field duplication and final-boundary equality against CSubmitOutcome 1.0.1; G must review exact Delivery/Context binding; I must approve signer/profile/key registry and trust roots.
4. H Gateway message replay, H Adapter observation replay and G Applied idempotency remain three distinct durable ledgers.
5. This delegated H-role review is not independent human H Owner approval, I cryptographic registration, production trust or deployed durable replay evidence.

## 5. Disposition

**H identity semantics: ACCEPTED WITH ENUMERATED EXCEPTIONS for the exact G Phase 3.8.22 blobs. H Delivery Evidence wire mapping: NOT FROZEN; successor schema/validator implementation outstanding. H 1.2.15 Gateway Attestation remains separately scoped. Global Applied freeze: NO. Production activation: NOT AUTHORIZED.**
