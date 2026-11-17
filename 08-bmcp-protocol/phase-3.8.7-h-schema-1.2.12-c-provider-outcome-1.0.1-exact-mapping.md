# Phase 3.8.7 — H Exact Mapping: BMCP 1.2.12 C Provider Outcome to CSubmitOutcome 1.0.1

- Owner: H — BMCP Protocol and Interoperability
- Current BMCP schema: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.12.schema.json`, Blob `a54f66914a819d77f00c6af04e76453ff9f654ee`
- Wire schema version: `1.3.0`; schema artifact revision: `1.2.12`
- C immutable object schema: `schemas/c-submit-outcome-1.0.1.schema.json`, Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C key-status event schema: Blob `908b293eba337e9fa75864cea3704e28a1a8d82e`
- C 1.0.1 sequence namespace amendment: Blob `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb`
- I 1.0.1 sequence namespace review: Blob `0d78e5b2bfcf66cae6b757314cead84b9c942601`
- H validator core: Blob `1a92c0cf7146e2884bd38232005dd9a55d558a85`
- Status: PROPOSED exact mapping; validator integration core exists but is not production-connected.
- Provenance: delegated H-role simulation at user's direction; not independent human H Owner approval.

## 1. Revision currentness

The C Provider Outcome branch's required and optional property names/types are identical between BMCP schema 1.2.11 Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40` and schema 1.2.12 Blob `a54f66914a819d77f00c6af04e76453ff9f654ee`. H nevertheless pins 1.2.12 as current because the common envelope and validator contract are versioned independently. A 1.2.11 envelope is not current for this validator and MUST be rejected when 1.2.12 is required.

## 2. Required inline C branch fields

The 1.2.12 branch requires:
`message_type`, `c_submit_outcome_ref`, `c_submit_outcome_digest`, `provider_outcome`, `provider_ref`, `provider_adapter_ref`, `provider_idempotency_key_ref`, `final_request_boundary_id`, `request_digest`, `transaction_ref`, `provider_outcome_evidence_ref`, `owner_signature_ref`, `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, `owner_admission_ref`, `owner_admission_digest`, `owner_ledger_ref`, `owner_ledger_version`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root`, `coc_participant_intent_ref`.

Optional branch fields include:
`provider_request_ref`, `provider_receipt_ref`, `actual_inference_request_id`, `participant_reservation_ref`, `participant_intent_ref`, `prepared_participant_ref`, `prepare_attempt_ref`, `prepare_attempt_generation`, `participant_ledger_ref`, `participant_ledger_version`, `participant_tuple_digest`, `i_terminal_decision_ref`, `d_clearance_ref`, `storage_resolution_proof_ref`, `provider_lookup_proof_ref`, `provider_no_handoff_proof_ref`, `not_invoked_proof_ref`, `unknown_reason_ref`, `coc_absence_reason`.

The branch is closed by `unevaluatedProperties=false`. H validates the entire envelope against exact schema Blob 1.2.12 before semantic processing.

## 3. C object duplicate mapping

| BMCP 1.2.12 field | CSubmitOutcome 1.0.1 field | Rule |
|---|---|---|
| `c_submit_outcome_ref` | `record_ref` | exact object identity |
| `c_submit_outcome_digest` | `payload_digest` | recompute candidate C-P0 digest and compare |
| `provider_outcome` | `Outcome` | exact enum |
| `provider_ref` | `ProviderRef` | exact |
| `provider_adapter_ref` | `AdapterRef` | exact |
| `provider_idempotency_key_ref` | `IdempotencyKeyRef` | exact opaque ref |
| `provider_request_ref` | `ProviderRequestRef` | exact when present/non-null |
| `provider_receipt_ref` | `ProviderReceiptRef` | exact when present/non-null |
| `provider_lookup_proof_ref` | `ProviderLookupProofRef` | exact when present/non-null |
| `provider_no_handoff_proof_ref` | `ProviderNoHandoffProofRef` | exact when present/non-null |
| `not_invoked_proof_ref` | `NotInvokedProofRef` | exact when present/non-null |
| `unknown_reason_ref` | `UnknownReasonRef` | exact when present/non-null |
| `actual_inference_request_id` | `ActualInferenceRequestId` | exact when present/non-null |
| `final_request_boundary_id` | `FinalRequestBoundaryRef` | exact |
| `request_digest` | `RequestDigest` | exact |
| `transaction_ref` | `CausalOrderTransactionRef` | exact |
| `provider_outcome_evidence_ref` | `OutcomeEvidenceRef` | exact |
| `owner_signature_ref` | `OwnerSignatureRef` | exact |
| `owner_admission_ref/digest` | `CAdmissionRef/Digest` | exact |
| `owner_ledger_ref/version` | `COwnerLedgerRef/Version` | exact |
| `owner_local_sequence` | `COwnerLocalSequence` | exact |
| `owner_high_water` | `COwnerHighWater` | exact |
| `owner_ledger_root` | `COwnerLedgerRoot` | exact |
| `coc_participant_intent_ref` | `COCParticipantIntentRef` | exact |
| `participant_intent_ref` | `COCParticipantIntentRef` | alias; if both aliases present they MUST match |
| `participant_reservation_ref` | `COCParticipantReservationRef` | exact when non-null |
| `coc_absence_reason` | `COCAbsenceReason` | exact when non-null |

If a C object member is non-null, the corresponding optional wire duplicate cannot be omitted. If a wire duplicate is present, it must equal the immutable C object exactly. Null and absent are not interchangeable.

## 4. C object fields not inline in BMCP

CSubmitOutcome 1.0.1 is the source of truth for:
- `CGateRef/CGateGeneration`;
- `ProviderAttemptRef/ProviderAttemptGeneration`;
- `ProviderAccountRef`;
- `EndpointRef/RegionRef/API operation`;
- `sequence_namespace_ref`;
- C key ID/version/profile/purpose/audience and candidate signature metadata.

These values are not all inline in the BMCP branch. H MUST dereference `c_submit_outcome_ref`, validate the exact C schema 1.0.1, recompute the C-P0 digest and validate the complete immutable tuple. The key-status callback must require equality between C object's `sequence_namespace_ref` and the authenticated CKeyStatusEvent namespace and prove `record_sequence` and `event_sequence` use the same durable C sequencer.

Missing required object member or proven mismatch is INVALID. Unavailable object, sequencer, key-status ledger or checkpoint is UNKNOWN.

## 5. External owner evidence — not C-P0

The following BMCP fields are independently issued and verified; they are not C-authored truth and MUST NOT be copied into C-P0 merely because they are present:
- COC: `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`;
- participant preparation: `prepared_participant_ref`, `prepare_attempt_ref/generation`, participant ledger/version/tuple digest;
- I: `i_terminal_decision_ref`;
- D: `d_clearance_ref`;
- Storage: `storage_resolution_proof_ref`.

H's authenticated COC/owner callbacks receive both the envelope and immutable C object and verify each reference under its own issuer, schema, digest, currentness and join rules. A reference string alone is not proof.

## 6. Crypto and key-status checks

Before any VALID result, H requires:
1. exact BMCP 1.2.12 envelope schema;
2. exact CSubmitOutcome 1.0.1 object schema and digest;
3. registered C profile and authenticated C signature/key status;
4. I-governed key-status event chain and governance signature;
5. ACTIVE state at signing sequence, exact key identity/scope and sequence namespace equality;
6. current anti-rollback checkpoint;
7. provider evidence issuer authentication;
8. C owner ledger inclusion/currentness;
9. COC/participant/Storage/I/D proof joins.

Missing authority callback or unavailable proof is UNKNOWN. Proven contradiction is INVALID. The current H validator core is an integration seam; production callbacks are not wired.

## 7. Decision

**ACCEPT THIS AS THE CURRENT 1.2.12 / C OBJECT 1.0.1 MAPPING PROPOSAL. NOT FROZEN.**

C and H candidate crypto tests exist, but I has not registered either profile or trust root. No production key registry, HSM/KMS custody, provider adapter test, COC/Storage deployment proof or production readiness is claimed.


## 8. Executed H 1.0.1 conformance

- H run `44060704553`, commit `8c377a7218b70621d2348b47341d4cf4755b3733`: SUCCESS, 17 tests.
- H 1.0.1 Python verifier Blob `5559fb7a612c8dd92345ceae3a6aa62f4faae41a`.
- H 1.0.1 Node oracle Blob `07c34b03aff94e1dfbbd1aa056ac849debeb3348`.
- H current validator core Blob `1a92c0cf7146e2884bd38232005dd9a55d558a85`.
- H C 1.0.1 schema and fixture blobs are byte-identical to C: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` and `c447f8c2908469c52cb52a448101495a331277c5`.
- H expected candidate vectors Blob `34e49a49551390f52198b1fa557e15a32a3f6ee2`.

The run verifies the required 1.0.1 sequence namespace, five candidate signatures, all present P0 member mutations and H Python/Node agreement. It does not validate a deployed sequencer, key-status service, governance root, anti-rollback checkpoint or production provider evidence.


## 9. Exact source pin direction and currentness

This H mapping consumes the exact C source amendment Blob `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` and the exact I sequence-namespace review Blob `0d78e5b2bfcf66cae6b757314cead84b9c942601`. C's source amendment intentionally does not pin this H consumer mapping; the Storage successor manifest binds both source and consumer artifacts without a cyclic reference. The previous C/I Blob pins in this file are superseded by the exact pins above.

**中文：** 本 H Mapping 消费精确 C 源修订 Blob `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` 与 I Sequence Namespace Review Blob `0d78e5b2bfcf66cae6b757314cead84b9c942601`。C 源修订不反向绑定 H 消费方 Mapping；Storage 后继清单负责同时绑定源与消费工件，避免循环引用。本文件旧 C/I Blob 引用由本节精确绑定取代。
