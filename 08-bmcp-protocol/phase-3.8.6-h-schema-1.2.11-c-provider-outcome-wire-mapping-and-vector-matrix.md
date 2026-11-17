# Phase 3.8.6 — H Exact 1.2.11 C Provider Outcome Wire Mapping and Vector Matrix

- Owner: H — BMCP Protocol and Interoperability
- Exact schema: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.11.schema.json`, Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- Wire family: `schema_version=1.3.0`; exact artifact revision `schema_artifact_revision=1.2.11`
- C semantic amendment: Blob `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4`
- C projection proposal: Phase 3.8.8 Blob `06d9264124d85896ccd44ef7789d9af245d8255b`
- C crypto candidate review: Blob `794d1dc49f034152407e3a42ba5ac937ea3539f8`
- I governance disposition: Phase 3.8.5 Blob `41fc0f508ae75e8c16012966160e9e2a1e368881`
- H validator contract: Phase 3.8.5 Blob `d1ab8c102f097100ed3948c5283dabc4e5e8690e`
- Status: PROPOSED exact-revision mapping and vector specification; NOT IMPLEMENTED / NOT EXECUTED / NOT FROZEN.
- Provenance: delegated H-role simulation at user's direction; not independent human H Owner approval.

## 1. Exact 1.2.11 C outcome branch

The C branch is selected by `message_type = C_PROVIDER_OUTCOME_RECORDED`. Its required branch fields are exactly:

`message_type`, `c_submit_outcome_ref`, `c_submit_outcome_digest`, `provider_outcome`, `provider_ref`, `provider_adapter_ref`, `provider_idempotency_key_ref`, `final_request_boundary_id`, `request_digest`, `transaction_ref`, `provider_outcome_evidence_ref`, `owner_signature_ref`, `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, `owner_admission_ref`, `owner_admission_digest`, `owner_ledger_ref`, `owner_ledger_version`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root`, `coc_participant_intent_ref`.

The exact allowed optional branch fields are:

`provider_request_ref`, `provider_receipt_ref`, `actual_inference_request_id`, `participant_reservation_ref`, `participant_intent_ref`, `prepared_participant_ref`, `prepare_attempt_ref`, `prepare_attempt_generation`, `participant_ledger_ref`, `participant_ledger_version`, `participant_tuple_digest`, `i_terminal_decision_ref`, `d_clearance_ref`, `storage_resolution_proof_ref`, `provider_lookup_proof_ref`, `provider_no_handoff_proof_ref`, `not_invoked_proof_ref`, `unknown_reason_ref`, `coc_absence_reason`.

The schema uses `unevaluatedProperties: false` for this message branch. No additional inline property is permitted unless a new schema artifact revision is published.

## 2. Common envelope mapping

The following common-envelope fields are required by exact 1.2.11:

- schema identity/version: `schema_id`, `schema_artifact_revision`, `schema_version`;
- message identity/replay: `message_type`, `message_id`, `message_nonce`;
- routing/authority: `audience`, `sender_authority_ref`, `sender_subject_ref`, `issuer_ref`, `subject_ref`, `owner_authority`, `owner_record_ref`;
- causal order: `causal_order_profile_ref`, `causal_order_coordinator_ref`, `causal_order_domain_ref`;
- crypto/integrity: `canonicalization_profile_id`, `digest_algorithm`, `payload_digest`, `integrity_proof_ref`, `channel_binding_proof_ref`, `key_id_ref`, `key_version`, `signature`, `created_at`.

Optional common fields include `policy_domain_ref`, `owner_signature_ref`, `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, `coc_previous_entry_digest`, and `signature_profile_id`. For protected owner-signed records, `signature_profile_id` is semantically mandatory even though JSON Schema marks it optional. The profile ID is not inferred from `canonicalization_profile_id`.

The common envelope requires `schema_id=bmcp.coc-jf10-unified`, `schema_version=1.3.0`, `schema_artifact_revision=1.2.11`, and `digest_algorithm=SHA-256`.

## 3. Inline / dereference / independent-proof matrix

| Semantic value | 1.2.11 wire representation | Validation rule |
|---|---|---|
| Immutable C outcome identity | inline `c_submit_outcome_ref` | dereference exact C-owned immutable object |
| C outcome object digest | inline `c_submit_outcome_digest` | recompute using C-defined object digest rule; mismatch INVALID |
| Outcome enum | inline `provider_outcome` | exact five-value enum; compare to immutable C object |
| Provider / adapter | inline `provider_ref`, `provider_adapter_ref` | compare to C object; adapter/provider capability record is separate evidence |
| Idempotency key | inline opaque `provider_idempotency_key_ref` | never expose raw secret; compare namespace/key binding in C object and provider proof |
| Final request boundary / digest | inline `final_request_boundary_id`, `request_digest` | compare to C object and exact immutable request commitment |
| C owner admission | inline `owner_admission_ref`, `owner_admission_digest` | dereference C owner admission and verify exact ledger inclusion |
| C ledger position | inline `owner_ledger_ref`, `owner_ledger_version`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root` | verify sequence <= high-water, root/version and membership proof |
| COC participant intent | inline nullable `coc_participant_intent_ref`; optional `coc_absence_reason` | null requires reason; non-null requires exact COC record/member join |
| Participant reservation | optional `participant_reservation_ref` | dereference and compare intent, transaction and request digest |
| Provider outcome evidence | required `provider_outcome_evidence_ref` | dereference under provider/transport issuer trust, not C key trust |
| Same-key lookup | optional `provider_lookup_proof_ref` | if used, bind original attempt, key namespace, target and request digest |
| No-handoff / not-invoked | optional `provider_no_handoff_proof_ref`, `not_invoked_proof_ref` | outcome-specific authoritative proof; absence of receipt is insufficient |
| C gate ref/generation | NOT INLINE IN 1.2.11 C branch | MUST exist in immutable C object; H dereferences and validates generation/currentness |
| Provider attempt ref/generation | NOT INLINE IN 1.2.11 C branch | MUST exist in immutable C object; H dereferences and validates attempt identity |
| Provider account/endpoint/region/API operation | NOT INLINE IN 1.2.11 C branch | MUST exist in immutable C object and provider capability proof; not inferred from provider_ref |
| COC / quorum position | inline COC refs/position/digest plus external proof | verify quorum/record chain independently; not part of C provider truth |

**Critical gap:** Schema 1.2.11 does not inline C GateRef/CGateGeneration, ProviderAttemptRef/Generation, provider account, endpoint, region or API operation. This is not silently treated as schema coverage. The required source is the immutable C object at `c_submit_outcome_ref`, whose digest is bound by `c_submit_outcome_digest`. If the object lacks any required tuple member, the record is INVALID. If dereference or currentness cannot be obtained, the result is UNKNOWN.

## 4. Equality and absence rules

- Every duplicated inline value MUST equal the immutable C object value exactly after only the field-specific normalization explicitly defined by the exact profile. No generic trimming, case folding or Unicode normalization.
- A reference string is an opaque identifier, not proof of the referenced object's contents or authority.
- `coc_participant_intent_ref=null` requires `coc_absence_reason`. A non-null intent requires exact COC member and reservation joins where applicable. C owner-local admission remains mandatory either way.
- Optional provider receipt, lookup and no-handoff refs are conditionally required by the outcome predicate. Their absence does not make an outcome valid by default.
- An optional field not present is distinct from a present null. Only fields whose schema type explicitly includes null may carry null.
- Schema acceptance is structural only. All semantic and issuer-authentication checks remain mandatory.

## 5. Vector matrix — expected result

This matrix is a specification, not execution evidence. Each vector must be materialized as canonical bytes plus exact references and expected layer/result.

| ID | Mutation / condition | Expected result |
|---|---|---|
| V01 | valid HANDOFF_ACCEPTED with exact provider evidence and all joins | VALID |
| V02 | ACCEPTED but provider evidence missing/unavailable | UNKNOWN if locator unavailable; INVALID if authoritative evidence proves no handoff |
| V03 | HANDOFF_REJECTED with authenticated rejection and side-effect state unresolved | UNKNOWN for release/terminality; never safe NOT_INVOKED |
| V04 | NOT_INVOKED with valid Adapter no-handoff proof and close-wins evidence | VALID |
| V05 | NOT_INVOKED based only on timeout, worker death or absent receipt | INVALID as asserted no-handoff; preserve as UNKNOWN observation |
| V06 | UNKNOWN / IN_DOUBT with original tuple preserved and lookup unavailable | UNKNOWN |
| V07 | same idempotency key, same request digest, authoritative lookup bound to original attempt | VALID reconciliation if all other proofs pass |
| V08 | same idempotency key but different request digest | INVALID |
| V09 | C GateGeneration stale at egress commitment | INVALID |
| V10 | C GateRef/generation missing from dereferenced C object | INVALID |
| V11 | C Gate/attempt object cannot be dereferenced | UNKNOWN |
| V12 | ProviderAttemptRef or generation mismatch with provider evidence | INVALID |
| V13 | provider account/endpoint/region differs from immutable C tuple | INVALID |
| V14 | C owner sequence exceeds high-water or ledger root mismatches | INVALID |
| V15 | owner ledger or anti-rollback currentness unavailable | UNKNOWN |
| V16 | COC intent null with explicit reason and valid C owner admission | continue semantic validation; may be VALID |
| V17 | COC intent null without reason | INVALID |
| V18 | non-null intent but missing/contradictory reservation or request digest | INVALID |
| V19 | duplicated inline request digest differs from immutable C object | INVALID |
| V20 | duplicate JSON key, malformed UTF-8 or schema additional property | INVALID |
| V21 | schema artifact revision != 1.2.11 or wire version != 1.3.0 | INVALID |
| V22 | protected C owner record lacks signature_profile_id | INVALID |
| V23 | C signature verifies but key status is unavailable | UNKNOWN |
| V24 | signature mutation in any signed field | INVALID |
| V25 | contradictory terminal outcomes for same attempt without valid append-only reconciliation chain | INVALID |
| V26 | Batch/Manifest order reversed or any of the three distinct digests mismatches | INVALID |
| V27 | required external provider/COC/ledger proof is unavailable without contradiction | UNKNOWN |
| V28 | authenticated provider proof explicitly contradicts the claimed outcome | INVALID |

## 6. Cross-language vector encoding requirements

For each vector publish:

- exact raw UTF-8 JSON bytes and SHA-256 of the fixture file;
- exact schema blob, C object blob/version, validator source commit and profile version;
- JSON Pointer mutation path (for wire fields) or immutable object member path (for dereferenced fields);
- canonical byte output, payload digest and signature test key identifier (test-only key; never private production key);
- expected layer: parse, schema, canonicalization, signature, dereference, semantic, COC/Storage join or currentness;
- expected VALID / INVALID / UNKNOWN;
- independent Python and JavaScript implementations and exact runtime/library versions;
- command, CI run ID, pass/fail count and retained output.

Test private keys must be generated solely for test vectors and must not be reused in production. Test fixtures must contain synthetic references and no real provider secrets.

## 7. Freeze decision

H accepts the exact structural field inventory above as the 1.2.11 mapping baseline. H does **not** accept the schema as complete inline representation of the C attempt tuple. The immutable C object dereference is mandatory for missing tuple fields.

I Phase 3.8.5 conditionally accepts the cryptographic suite in principle but explicitly does not register the profile. Therefore C Provider Outcome protected records remain blocked from VALID until the exact profile is registered, H's projection implementation exists, C object contract is immutable and dereferenceable, and independent vectors are executed.

No executable validator, test fixtures, cross-language execution, provider adapter test, production readiness or exactly-once property is claimed.


## 8. C immutable object schema 1.0.0 binding

C has now published the proposed immutable object schema:
- C schema `urn:aimba:schema:c-submit-outcome:1.0.0`, Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`.
- C schema/conformance contract Phase 3.8.9, Blob `3a3f4e6be9537faa919dd54650c81cb8a08345c0`.
- C structural/semantic fixture pack, Blob `e14eab2bed41f30af10a073b8e6523512128e78e`.
- C Python harness, Blob `92e8e9e607566eafa6ad89110202dbeed0fc43cb`; dependency pin Blob `89099e36f214d8d0e0c7d4aacc19e2b4450f0744`.

The dereference target of `c_submit_outcome_ref` MUST validate against this exact schema revision and object digest. The object contains the complete C gate/attempt/provider/account/endpoint/region/API/idempotency/request tuple absent from the BMCP 1.2.11 inline branch. H must compare all duplicated wire fields to the dereferenced object.

The C fixture pack contains ten synthetic structural/semantic cases. Its signatures are explicit placeholders; the profile is unregistered and these tests are NOT EXECUTED. The C harness is not a cryptographic verifier, provider proof verifier, owner-ledger membership verifier or COC quorum verifier. H must not elevate its existence to cross-language or production evidence.

### 8.1 H decision

H accepts the C schema as a proposed dereference contract for validator implementation planning. H does not yet accept it as a frozen interoperable object because:
- I has not registered `AIMBA-C-CRYPTO-1.0`;
- no valid C signed vectors or C key-status evidence exist;
- no H dereference/duplicate-field validator implementation exists;
- the C harness has not been executed;
- provider adapter and Storage deployment evidence remain open.

C schema structural validity and BMCP envelope structural validity are separate gates; both must pass before semantic joins.


## 9. I exact C object crypto review

I Phase 3.8.6 review Blob `cdfaa1c112210d65f9fd24fc1f5eb3caf8514fec` accepts the C object structure and candidate digest/signature construction only. It explicitly does not register/deploy the profile or approve trust roots/custody. The H implementation must enforce strict UTF-8, duplicate-key rejection, JCS, exact C-P0 field coverage, 86-character Base64url structural screening plus strict decoding to 64 bytes, and the exact message_type domain component. The C test signatures remain placeholders and no cryptographic vector execution is claimed.


## 10. Complete optional proof-reference disposition

The H validator mapping now compares all C-owned duplicated proof refs when present:
- `provider_request_ref` ↔ `ProviderRequestRef`;
- `provider_receipt_ref` ↔ `ProviderReceiptRef`;
- `provider_lookup_proof_ref` ↔ `ProviderLookupProofRef`;
- `provider_no_handoff_proof_ref` ↔ `ProviderNoHandoffProofRef`;
- `not_invoked_proof_ref` ↔ `NotInvokedProofRef`;
- `unknown_reason_ref` ↔ `UnknownReasonRef`;
- `owner_signature_ref` ↔ `OwnerSignatureRef`;
- `actual_inference_request_id` ↔ `ActualInferenceRequestId`;
- `participant_intent_ref` and `coc_participant_intent_ref` ↔ `COCParticipantIntentRef`;
- `participant_reservation_ref` ↔ `COCParticipantReservationRef`.

If a mapped C object member is non-null, the wire duplicate cannot be omitted. If a wire duplicate is present, it must equal the immutable object exactly. Both participant-intent aliases, if present, must agree.

The following envelope values are not C-authored fields and MUST be verified independently by H's COC/owner-ledger authority callbacks: `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, `prepared_participant_ref`, `prepare_attempt_ref/generation`, participant ledger/version/tuple digest, `i_terminal_decision_ref`, `d_clearance_ref`, and `storage_resolution_proof_ref`. They must not be silently ignored or promoted into C-P0; they are external owner evidence with independent issuer and join semantics.

Current H validator core: Blob `e8f737326bc4791e8d7acf917b4725dbb7171fad`. H unit/fixture test file current Blob `1f17bdcef6004eca165644ce96bcf35d3b10c3f8`. Exact vendored C schema and fixture Blobs are `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c` and `e14eab2bed41f30af10a073b8e6523512128e78e`.
