# Phase 3.8.24 — H Applied Delivery Evidence 1.0.0 Schema and Validator Candidate

- Status: **IMPLEMENTED AS A TEST/CONFORMANCE CANDIDATE; NOT A PRODUCTION CRYPTOGRAPHIC OR DURABLE REPLAY SERVICE**
- Owner: H — BMCP Protocol / Wire and Interoperability
- G consumer decision: `bd297873bc1e593280484a43cb44b56058d9c4ff` (EN), `82553a47fae2d5e796e0742b46231afe465e75b2` (zh-CN)
- H decision: `be308261c3e000e712a3cdbd3dbf60507156127b` (EN)
- Unified 1.2.15 remains unchanged: `860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- Gateway validator remains unchanged: `9cc426d4c26deb452f39daff34c1008dd535e969`

## 1. Purpose and isolation

This is a separate message family, `APPLIED_DELIVERY_EVIDENCE_RECORDED`, schema revision `1.0.0`. It does not extend or mutate Unified 1.2.15's C Provider Outcome Gateway Attestation P0 allowlist. H Gateway ingress replay identity and H Adapter observation replay identity remain separate.

## 2. Exact identity projections

- `HDeliveryBindingIdentity`: `(adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch)`.
- `HEvidenceIdentity`: `(HDeliveryBindingIdentity, evidence_kind)`.
- `HObservationRecordIdentity`: `(issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence)`.

The first tuple identifies a stable delivery binding; the second selects an evidence slot; the third identifies one immutable signed observation. The three tuples MUST NOT be substituted for one another.

## 3. Schema and P0 rules

The JSON Schema uses Draft 2020-12, `additionalProperties: false`, exact revision/type constants, typed required identity fields, closed `evidence_kind` and coverage/tier enums, digest encodings, and conditional requiredness. The validator derives its P0 allowlist from the schema property set while explicitly excluding only `payload_digest`, `signature` and `integrity_proof_ref`. Unknown members are rejected, never silently omitted from the signed projection.

The test reference canonicalizer is deterministic sorted-key JSON for local tests only. It is NOT the production H canonicalization profile and does not select JCS, hash domains, signature algorithms, key registry or trust roots. Production canonicalization and cryptographic profiles remain I/H authority decisions and require exact vectors.

Tier 1 requires complete managed-region coverage and exact equality of `materialized_context_version` and G `context_version`. C submit outcome refs and record refs are explicit and remain C-owned; H does not mint provider outcome truth.

## 4. Validator behavior

The reference validator performs:
1. strict JSON object and JSON Schema validation;
2. Tier 1 coverage/version predicates;
3. exact P0 projection and payload digest comparison;
4. injected profile registration, key status, signature, protected identity, C final-boundary, G delivery binding and capability-epoch checks;
5. durable observation callback with `NEW`, `SAME_DIGEST_REPLAY` or `CONFLICT` disposition.

Every authority callback is tri-state. False yields INVALID; unavailable/exception/None yields UNKNOWN; no missing verifier is treated as success. Same observation identity + same digest must return the original durable result ref. Same identity with changed digest/immutable tuple is CONFLICT and cannot overwrite the original record.

## 5. Conformance tests

The initial test module covers positive Tier 1, unknown field rejection, each Delivery Binding identity field required, incomplete coverage, context-version mismatch, digest mutation, identity-domain separation, UNKNOWN trust result, invalid signature, exact replay and changed-digest conflict.

Run from repository root:

```bash
python -m pip install -r 08-bmcp-protocol/tests/conformance/provider_outcome/requirements.txt
python -m unittest discover -s 08-bmcp-protocol/tests/conformance/applied_delivery_evidence -p 'test_*.py' -v
```

These tests have not yet been executed in this commit environment. A CI run must be attached before reporting PASS.

## 6. Open gates

- C must exact-review C boundary and C outcome field mapping against its current CSubmitOutcome schema.
- G must exact-review Delivery/Context binding and Full Applied predicate.
- I must approve signer/profile/key registry, trust roots, canonicalization and anti-rollback.
- H must implement durable observation replay storage and deployed validator integration.
- SDK generation, runtime Adapter integration, cross-language vectors and production crypto are not implemented.
- No global Applied freeze, production activation or merge authorization is implied.
