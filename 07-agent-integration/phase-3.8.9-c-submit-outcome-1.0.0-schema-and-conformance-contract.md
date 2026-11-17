# Phase 3.8.9 — CSubmitOutcome 1.0.0 Schema and Conformance Contract

- Owner: C — Provider Outcome / immutable submit evidence
- Status: PROPOSED structural schema and local conformance harness; NOT EXECUTED.
- Schema: `schemas/c-submit-outcome-1.0.0.schema.json`, Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`
- Semantic amendment: Phase 3.8.6 Blob `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4`
- Signature projection: Phase 3.8.8 Blob `39ff523c41f10e3a82442d4746dd7ca7763d271c`
- H wire schema: 1.2.11 Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- H mapping/vector matrix: Phase 3.8.6 Blob `de3db907b4077e0e4d37df19d289cf1bf51afbad`
- Provenance: delegated C-role simulation at user's direction; not independent human C Owner approval.

## 1. Purpose and authority

This schema defines the immutable C-owned object dereferenced by BMCP `c_submit_outcome_ref`. It is not the BMCP envelope schema. The immutable object is the authoritative source for gate generation, provider attempt generation, account/endpoint/region/API operation, idempotency namespace/key, exact request boundary/digest, outcome, and evidence references.

C owns the semantic truth and issuance of this object. H validates its structure, digest, signature and wire joins. I governs cryptographic profile registration, trust roots and key lifecycle. Storage validates owner-ledger/COC persistence joins. No owner may infer another owner's truth from a valid signature alone.

## 2. Exact schema identity and profile status

- Schema ID: `urn:aimba:schema:c-submit-outcome:1.0.0`
- Schema version/artifact revision: `1.0.0`
- Candidate signature profile ID: `AIMBA-C-CRYPTO-1.0`
- Profile status: **PROPOSED / NOT REGISTERED**. The schema's profile identifier is a candidate binding, not proof of I registration or activation.
- JSON Schema dialect: Draft 2020-12.
- Unknown properties: rejected (`additionalProperties=false`).
- Sequence/generation values are decimal strings to avoid cross-language integer precision loss.
- SHA-256 digest fields are lowercase 64-character hexadecimal strings.
- Signature is unpadded Base64url with 86 characters for a 64-byte Ed25519 signature. The checked-in fixtures use placeholders and are NOT cryptographically valid.

## 3. Required semantic tuple

The schema requires the exact C tuple from Phase 3.8.6:

`CSubmitOutcomeRef`, `CAdmissionRef`, `CAdmissionDigest`, `CGateRef`, `CGateGeneration`, `ProviderAttemptRef`, `ProviderAttemptGeneration`, `ProviderRef`, `ProviderAccountRef`, `AdapterRef`, `EndpointRef`, `RegionRef`, `IdempotencyNamespaceRef`, `IdempotencyKeyRef`, `FinalRequestBoundaryRef`, `RequestDigest`, and the paired optional COC ParticipantIntent/Reservation refs.

The JSON object maps the object identity to `record_ref` and its exact tuple members to the PascalCase fields in the schema. It additionally binds:
- C owner ledger/version/local sequence/high-water/root;
- durable Gate commit ref/digest;
- Adapter build and provider capability record/digest;
- request method/content type and API operation;
- CausalOrderTransactionRef;
- outcome enum, side-effect status, provider evidence ref/digest/issuer/type;
- append-only prior/supersession/reconciliation links;
- schema/profile, message identity, audience/purpose and signature metadata.

The object must be immutable after issuance. A correction or new observation is a new record linked through the append-only linkage fields. No in-place mutation is permitted.

## 4. Outcome conditional invariants

| Outcome | Structural requirements | Semantic rule |
|---|---|---|
| HANDOFF_ACCEPTED | ProviderRequestRef + ProviderReceiptRef; SideEffectStatus=PROVEN_OCCURRED | Authenticated receipt proves exact handoff for exact immutable attempt and request digest |
| HANDOFF_REJECTED | ProviderRequestRef; side-effect status explicit | Rejection alone does not prove no side effect; PROVEN_NONE additionally requires authoritative no-handoff proof |
| NOT_INVOKED | ProviderNoHandoffProofRef + NotInvokedProofRef; SideEffectStatus=PROVEN_NONE | Same durable gate serialization authority proves no EGRESS_COMMITTED/transport invocation |
| UNKNOWN | UnknownReasonRef; SideEffectStatus=POSSIBLE_OR_UNKNOWN | Nonterminal; preserve original tuple and prohibit retry-as-new-operation |
| IN_DOUBT | UnknownReasonRef; SideEffectStatus=POSSIBLE_OR_UNKNOWN | Nonterminal; same-key lookup only against original attempt and digest |

COC linkage is either a complete non-null intent/reservation pair with null absence reason, or both refs null with an explicit absence reason. A half-pair is invalid. C owner-local admission remains required even when COC intent is absent.

## 5. Conformance source files

- Schema: `schemas/c-submit-outcome-1.0.0.schema.json`, Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`
- Fixture pack: `tests/conformance/provider_outcome/c_submit_outcome_1_0_0_vectors.json`, Blob `e14eab2bed41f30af10a073b8e6523512128e78e`
- Python harness: `tests/conformance/provider_outcome/test_c_submit_outcome_1_0_0.py`, Blob `92e8e9e607566eafa6ad89110202dbeed0fc43cb`
- Dependency pin: `tests/conformance/provider_outcome/requirements.txt`, Blob `89099e36f214d8d0e0c7d4aacc19e2b4450f0744`

The 10 fixture cases cover accepted, rejected-with-ambiguous-side-effect, not-invoked, unknown, in-doubt, missing accepted receipt, not-invoked without proof, broken COC pair, high-water violation and request-digest mismatch.

Run command (not yet executed):
```sh
python -m pip install -r 07-agent-integration/tests/conformance/provider_outcome/requirements.txt
python -m unittest discover -s 07-agent-integration/tests/conformance/provider_outcome -p 'test_*.py' -v
```

The harness checks Draft 2020-12 schema validity and selected semantic invariants. It deliberately does not validate cryptographic signatures, provider issuer trust, actual provider outcome truth, gate linearizability, append-only ledger inclusion, COC quorum, Storage durability or cross-language canonicalization. Its fixture signatures are placeholders. A passing local run would be structural/semantic unit evidence only, not production certification.

## 6. Remaining blockers

1. I must register the profile and approve C trust root/key-status/custody/rotation/revocation/compromise/anti-rollback controls.
2. C must provide the append-only owner ledger implementation and proof of immutable record inclusion/currentness.
3. H must implement the 1.2.11 envelope-to-object dereference, digest/signature verification and exact duplicate-field comparison.
4. H/C must generate real test-only Ed25519 keys and canonical-byte/digest/signature vectors after profile registration.
5. Independent Python and JavaScript verifiers must agree on exact bytes and signature results.
6. Provider-specific Adapter race/fault tests must execute against each supported provider/account/endpoint class.
7. Storage must validate C ledger and COC Batch/Manifest joins against durable readback.
8. A must review exact implementation/test/registration blobs before any freeze decision.

## 7. Decision

**C ACCEPTS THIS AS THE PROPOSED IMMUTABLE OBJECT SCHEMA AND STRUCTURAL/SEMANTIC TEST CONTRACT. NOT FROZEN.**

No tests have been executed by this artifact. No profile is registered. No provider adapter is certified. No production activation, universal exactly-once behavior, Full Applied or Global Forget Completion is claimed.


### 3.1 Additional exact wire bindings

The schema requires `OwnerSignatureRef` in addition to inline `key_id_ref`, `key_version` and `signature`. It also permits `ActualInferenceRequestId` when the runtime/provider assigns one. The H wire validator must compare `owner_signature_ref` and `actual_inference_request_id` when present.

C's conditional provider proof members are `ProviderRequestRef`, `ProviderReceiptRef`, `ProviderLookupProofRef`, `ProviderNoHandoffProofRef`, `NotInvokedProofRef` and `UnknownReasonRef`. Each matching BMCP optional field, when present, must equal the immutable C object; if the immutable C object contains a non-null value, its wire duplicate cannot be silently omitted.

The BMCP `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, `prepared_participant_ref`, `prepare_attempt_ref/generation`, participant ledger fields, I terminal decision, D clearance and Storage resolution proof are independent owner/COC evidence, not C-authored truth. H verifies them through the appropriate authenticated COC/owner-ledger callback; they are not copied into C-P0 merely because they appear in the envelope.
