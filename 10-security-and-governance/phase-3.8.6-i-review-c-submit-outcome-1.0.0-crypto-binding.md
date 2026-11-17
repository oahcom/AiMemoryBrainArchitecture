# Phase 3.8.6 — I Review of CSubmitOutcome 1.0.0 Crypto Binding

- Owner: I — Security, Identity and Governance
- C schema: `urn:aimba:schema:c-submit-outcome:1.0.0`, Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`
- C projection proposal: Phase 3.8.8 current Blob `06d9264124d85896ccd44ef7789d9af245d8255b`
- C schema/conformance contract: Phase 3.8.9 Blob `7939c84e950b50f3ec44e4e2fbe5e7f93e544c2e`
- Prior I governance disposition: Phase 3.8.5 Blob `41fc0f508ae75e8c16012966160e9e2a1e368881`
- Status: **STRUCTURAL CRYPTO BINDING ACCEPTED WITH CONDITIONS; PROFILE REGISTRATION NOT APPROVED**
- Provenance: delegated I-role simulation at user's direction; not independent human I Owner approval.

## 1. Review decision

I accepts the C schema's structural separation of immutable C outcome content, payload digest, key ID/version and signature fields as a reasonable candidate design. I accepts the distinct C profile namespace and the proposed domain separation in principle.

I does NOT register `AIMBA-C-CRYPTO-1.0`, activate a C trust root, approve C key custody, or authorize production signing/verification. This review does not supersede the conditional-only Phase 3.8.5 decision.

## 2. Exact candidate construction reviewed

The candidate construction is:
- `C-P0`: all present schema-allowed members except `payload_digest` and `signature`;
- JCS RFC 8785 canonicalization over strict UTF-8/I-JSON input with duplicate-key rejection;
- payload digest: SHA-256 over `AIMBA-C-PAYLOAD-v1\0 || JCS(C-P0)`;
- signed projection: C-P0 plus `payload_digest`;
- signature preimage: `AIMBA-C-SIGNATURE-v1\0 || AIMBA-C-CRYPTO-1.0\0 || ASCII(message_type) || 0x00 || JCS(signed projection)`;
- Ed25519, 64-byte signature, unpadded Base64url.

The C schema's required `message_type=C_PROVIDER_OUTCOME_RECORDED` is necessary to make the message-family domain component explicit. H must compare the object message_type with the BMCP envelope message_type. It MUST NOT substitute message_id.

## 3. Mandatory crypto and parser checks

Before registration, implementation and vectors must prove:
1. Strict UTF-8 decoding; malformed sequences rejected.
2. Duplicate JSON object members rejected before schema validation.
3. Non-finite numeric constants rejected; JCS/I-JSON numeric constraints enforced.
4. No implicit Unicode normalization; strings differing by normalization form remain distinct.
5. Base64url decoder rejects padding, invalid alphabet, incorrect length and non-canonical encodings; decoded signature is exactly 64 bytes.
6. Ed25519 public key encoding and trust-chain resolution are exact; payload-supplied key material is never a trust anchor.
7. Digest is recomputed from the exact C-P0 allowlist and compared to both object `payload_digest` and BMCP `c_submit_outcome_digest`.
8. Signature preimage includes the exact profile ID and message_type with exact zero-byte separators.
9. Cross-profile, cross-owner, cross-message and cross-audience replay fail.
10. Profile/key downgrade and stale key-status restore fail closed.

The JSON Schema pattern for 86 Base64url characters is only a structural prefilter. It does not prove decoding correctness, canonical encoding or signature validity.

## 4. Projection and schema governance

The current C schema uses `additionalProperties=false`, which is appropriate for a closed projection. Any new signed semantic field requires a new immutable C schema revision and corresponding projection/profile revision or explicitly governed compatibility rule. The validator must not silently ignore unknown properties or apply serializer defaults.

The exact C-P0 allowlist must remain mechanically derivable from the schema. A future schema change that adds a property but fails to include it in the signed projection is a security defect. H must test every schema property for signed coverage, except the derived digest and signature fields.

The C object digest and BMCP wire digest must have one unambiguous definition. Current candidate rule is that `c_submit_outcome_digest` equals the recomputed C `payload_digest`; this must be explicitly registered in the final profile, not inferred from field names.

## 5. Key trust lifecycle remains a registration blocker

Before registration, C/I must publish and review:
- independent C trust root and issuer chain;
- append-only C key-status schema/ledger with PENDING/ACTIVE/RETIRED/REVOKED/COMPROMISED/DESTROYED states;
- key ID/version/profile/purpose/audience binding;
- effective sequencer boundary and historical signature verification rules;
- key generation/custody/HSM/KMS evidence and access controls;
- rotation overlap, revocation, compromise discovery/effective boundary and incident handling;
- external anti-rollback checkpoint and stale restore tests;
- private key destruction and public verification key retention evidence.

Unavailable current key status or anti-rollback proof yields UNKNOWN. Compromised keys cannot authorize new work after the effective compromise boundary.

## 6. Test evidence required

The current C fixture signatures are placeholders and are explicitly not cryptographically valid. The current Python harness is structural/semantic only and has not been executed. Neither is crypto registration evidence.

Required next vectors:
- at least one known-good C test-only Ed25519 keypair and exact RFC 8785 bytes;
- expected C-P0 bytes, digest, signed projection bytes, preimage bytes and signature;
- each field mutation, absent/null/empty mutation, duplicate key, malformed UTF-8 and invalid number;
- invalid Base64url and wrong signature length;
- wrong key/profile/message type/audience/purpose;
- revoked/compromised key boundaries and anti-rollback restore;
- independent Python and JavaScript implementation agreement with pinned runtime/library versions and retained CI logs.

## 7. Disposition

**ACCEPT STRUCTURAL CRYPTO BINDING AS A CANDIDATE; DO NOT REGISTER OR DEPLOY.**

I has not approved the C profile, C trust root, key custody or production use. No signature verification, cross-language execution, key lifecycle drill or production readiness is claimed.


### 4.1 Additional schema fields

The reviewed schema revision also requires `OwnerSignatureRef`, binding the owner-signature evidence reference separately from the inline `key_id_ref`, `key_version` and `signature`. It permits `ActualInferenceRequestId` where the provider/runtime assigns a real request identifier. H must compare both fields when the corresponding wire member is present and must not infer an actual request ID from a local attempt identifier.


## 8. Review of executed structural CI

C's schema/semantic CI run `44055965702` at commit `a0c197fa94e71c52758fadaa335a686815485dd7` passed 3 tests. I accepts this as evidence that the Draft 2020-12 schema is internally valid and that the ten synthetic structural/semantic vectors match their expected local outcomes under the checked harness.

This does not alter the crypto decision: all fixture signatures are placeholders, the C profile remains unregistered, and there is no executed Ed25519 signature vector, C key-status/trust verification, provider proof authentication or cross-language C-profile conformance. No registration or deployment approval is granted.
