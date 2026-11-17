# Phase 3.10.0 — A Review: C Crypto Candidate and Independent H Verification

- Owner perspective: A — Principal Integration Architect
- Scope: CSubmitOutcome 1.0.0 schema, candidate JCS/SHA-256/Ed25519 construction, C and H Python/Node vector execution, I governance disposition, Storage binding.
- Disposition: **ACCEPT CANDIDATE CRYPTO CONSTRUCTION + INDEPENDENT TEST AGREEMENT; DO NOT REGISTER OR FREEZE**
- Provenance: delegated A-role simulation at user's direction; not independent human A Owner approval.

## 1. Exact artifacts reviewed

| Owner | Artifact | Exact Blob / Run |
|---|---|---|
| C | CSubmitOutcome 1.0.0 schema | `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c` |
| C | Ten structural/semantic outcome vectors | `b4c32dc8cd7072a04843c2db74c7f96c6de001a4` |
| C | Candidate vector manifest, test-only seed | `88a16f0d9aaa8a5e46af857c2cd34c2bcedd07ae` |
| C | Static expected crypto fingerprints/signatures | `a4bfe0b431d5e710ac99d604e7b1bce49c044d23` |
| C | Python crypto test | `2e1f572facc644c378ee1880a553c27a72ed2cc4` |
| C | Node JCS/Ed25519 oracle | `31c8ac889766f9574725357ae6134a901bfb5f33` |
| C | Phase 3.8.9 schema/conformance contract | `2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac` |
| C | Candidate crypto CI | Run `44057463855`, commit `08ae2649c3be812ef425fb7a958d41a62f933850`, SUCCESS, 7 tests |
| I | Phase 3.8.6 crypto review | `b2e37b0ba9137f2ef1b9fd65bf815bc136ca28c8` |
| H | Fail-closed validator core | `e8f737326bc4791e8d7acf917b4725dbb7171fad` |
| H | H Python independent crypto verifier | `a49d588ea6f840927fe21ad8c41cd8089dceac29` |
| H | H Node independent crypto oracle | `c35ddea3ecaf5e452b14fb57fb20327ad80703cc` |
| H | H exact wire mapping | `f929e3be358b7f73fbfc1fb11179dd4578bdef19` |
| H | H validator contract | `e67ed63b6dcbd0530c0343bde9245b8cf96c3c4d` |
| H | Independent H CI | Run `44057944517`, commit `b8a22cecdf6238c81f08338d30776be250fd69a4`, SUCCESS, 10 tests |
| Storage | Exact version manifest current | `0a33ed93cb2a4b5cf4e60b201c1f892bec2a0a7a` |

## 2. Cryptographic construction reconciliation — ACCEPT AS CANDIDATE

The candidate profile uses:
- RFC 8785 JCS over strict UTF-8/I-JSON;
- SHA-256 over `AIMBA-C-PAYLOAD-v1\0 || JCS(C-P0)`;
- Ed25519 over `AIMBA-C-SIGNATURE-v1\0 || AIMBA-C-CRYPTO-1.0\0 || ASCII(message_type) || 0x00 || JCS(C-P0 + payload_digest)`;
- 64-byte Ed25519 signatures encoded as unpadded Base64url.

C's schema requires the exact message type and profile ID. C-P0 is closed by the exact schema's `additionalProperties=false` rule and consists of all present allowed object fields except derived `payload_digest` and `signature`. H independently uses the same P0 construction and message_type domain component.

A accepts the candidate construction as internally consistent with the I proposal and the H implementation interface. Any schema field addition requires explicit signed-projection review and a new immutable revision; silent omission is forbidden.

## 3. Executed C evidence — ACCEPT

C CI run `44057463855` passed 7 tests. It:
- validated the C JSON Schema and ten structural/semantic vectors;
- generated/verified five test-only signatures for ACCEPTED, REJECTED-with-ambiguous-side-effect, NOT_INVOKED, UNKNOWN and IN_DOUBT;
- mutated every present C-P0 member and confirmed the original signature fails;
- compared Python RFC 8785/Ed25519 and Node JCS/Ed25519 output;
- matched static expected fingerprints, preimage hashes, public key and signatures.

The deterministic private seed is publicly disclosed test material and MUST NEVER be used in production.

## 4. Independent H evidence — ACCEPT

H ran its own Python and Node implementations against byte-identical C schema, fixtures, manifest and expected vector blobs. Run `44057944517` passed 10 tests, including five signature verifications, every-field mutation checks and comparison to C's static expected vectors.

A accepts this as independent owner-side candidate construction verification. It is not production key trust verification and does not replace I registration.

## 5. I governance disposition — RESPECTED

I accepts candidate construction and cross-owner test agreement but explicitly does not register `AIMBA-C-CRYPTO-1.0`, activate a C trust root, approve key custody or authorize production use.

A will not override this I boundary. The following remain mandatory:
- C trust root and issuer registration;
- append-only authenticated key-status ledger and anti-rollback checkpoint;
- key generation/custody/HSM/KMS controls, rotation, revocation and compromise lifecycle;
- historical signature and compromise-boundary semantics;
- production trust/key-status callback integration and drills.

## 6. Remaining blockers

| Gate | Status |
|---|---|
| Candidate JCS/SHA-256/Ed25519 construction | <badge>Verified by C and H candidate CI</badge> |
| I profile registration | OPEN / NOT APPROVED |
| C production trust root and key lifecycle | OPEN |
| H production signature/key-status callbacks | NOT CONNECTED |
| C owner ledger append-only inclusion/currentness | OPEN |
| Provider evidence issuer authentication | OPEN |
| C provider adapter race/fault/idempotency tests | NOT RUN |
| COC quorum and Storage deployment-grade joins | OPEN |
| Production activation / final freeze | NOT APPROVED |

## 7. Final decision

**ACCEPT THE CANDIDATE CRYPTO CONSTRUCTION AND INDEPENDENT C/H TEST AGREEMENT. DO NOT REGISTER OR FREEZE.**

The project now has real candidate-only cryptographic execution evidence rather than merely a primitive proposal. It does not yet have a registered profile or production trust lifecycle. H's validator remains an integration core with injected, not production-connected, authority callbacks. Provider adapter, C ledger, COC and Storage deployment proofs remain open.

No production provider egress, Full Applied, Global Forget Completion or universal exactly-once behavior is authorized. All Owner conclusions are delegated role simulations, not independent human Owner signatures.
