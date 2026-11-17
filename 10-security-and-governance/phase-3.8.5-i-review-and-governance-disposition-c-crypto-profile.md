# Phase 3.8.5 — I Governance Review and Disposition for C Crypto Profile

- Owner perspective: I — Security, Identity and Governance
- Reviewed candidate: `AIMBA-C-CRYPTO-1.0`
- I proposal: Phase 3.8.4 Blob `1bcddbaaa4a9ca730d492a6554941becac305668`
- C candidate acceptance: Phase 3.8.7 Blob `794d1dc49f034152407e3a42ba5ac937ea3539f8`
- C exact projection proposal: Phase 3.8.8 Blob `39ff523c41f10e3a82442d4746dd7ca7763d271c`
- H schema: artifact 1.2.11 Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- Disposition: **CONDITIONAL CRYPTOGRAPHIC SUITE ACCEPTANCE; PROFILE REGISTRATION AND DEPLOYMENT NOT APPROVED**
- Provenance: delegated I-role simulation at user's direction; not independent human I Owner approval.

## 1. Governance decision

I accepts the *algorithm-suite proposal in principle* for a separately scoped C profile, subject to the conditions in this decision:

- canonicalization: RFC 8785 JSON Canonicalization Scheme, with strict RFC 7493 I-JSON input constraints;
- digest: SHA-256;
- signature: Ed25519;
- signature representation: unpadded Base64url;
- C-specific profile ID and domain separation;
- independent C issuer, key namespace, trust root and key-status authority.

This is not registration of `AIMBA-C-CRYPTO-1.0`, not approval of any deployed key, and not approval of C's semantic truth claims. C retains sole authority for the C-owned projection and Provider Outcome semantics. H retains wire-schema and validator ownership.

## 2. Mandatory cryptographic profile invariants

Before registration, the profile specification MUST normatively fix:

1. Exact byte-level JCS behavior, including number constraints, string handling, duplicate-key rejection and absent/null/empty distinction.
2. SHA-256 digest preimage, domain tag, separator bytes, output encoding and digest field placement.
3. Ed25519 variant, key encoding, signature length, malformed-key rejection and verification behavior.
4. Exact C profile identifier, version, message-family scope, purpose and audience restrictions.
5. Exact C-P0 and BMCP-C-WIRE-P0 projections, with no wildcard exclusions and no implicit serializer defaults.
6. Key ID/version binding and authenticated trust-chain resolution; payload-supplied public keys are never trust anchors.
7. Strict no-fallback behavior. No algorithm negotiation, downgrade, alternate encoding or "best effort" verification.
8. Historical verification semantics that distinguish signature validity at signing time from current authorization to admit new work.

Any change to the projection, algorithm, domain tag, key encoding or trust semantics requires a new immutable profile version.

## 3. C key lifecycle and trust requirements

C must publish an append-only, authority-authenticated key-status ledger with at least:

- states: PENDING, ACTIVE, RETIRED, REVOKED, COMPROMISED, DESTROYED;
- effective sequence/time boundary and monotonic status version;
- issuer, owner authority, key ID/version, profile, purpose and audience binding;
- key generation/activation evidence and custody/HSM/KMS attestation where applicable;
- rotation overlap rules and maximum accepted historical signature age;
- revocation reason, compromise discovery time and effective compromise boundary;
- incident response, containment, re-signing/reconciliation and evidence preservation rules;
- external anti-rollback checkpoint and restore/failover behavior.

A key marked COMPROMISED must not authorize new work after the effective boundary. Historical signatures cannot automatically be trusted merely because their cryptographic bytes verify; the validator must apply the recorded compromise window and policy.

If current key status, trust chain or anti-rollback anchor is unavailable, the result is UNKNOWN and all dependent release gates fail closed.

## 4. Custody and operational controls

Before profile registration, C/I must provide evidence for:

- private-key generation in an approved controlled environment;
- non-exportability or explicitly approved custody exception;
- least-privilege signing service identity and workload binding;
- access logging, dual control for high-risk operations and emergency revocation;
- backup/recovery controls that do not permit rollback to an older active-key state;
- rotation, disaster recovery and compromise drills;
- separation between C signing authority and provider credentials;
- key destruction evidence and retention of public verification material.

No private key, provider credential or secret idempotency key may be committed to the repository.

## 5. Required independent test evidence

The profile cannot be registered until at least two independently implemented verifiers agree on exact vectors for:

- canonical bytes and SHA-256 digest;
- valid/invalid Ed25519 signatures;
- every signed-field mutation in C Phase 3.8.8;
- duplicate keys, invalid UTF-8, numeric edge cases and malformed Base64url;
- absent/null/empty distinction;
- wrong profile, wrong purpose/audience, wrong key ID/version;
- revoked/compromised key at before/after effective boundary;
- replay, nonce reuse and cross-owner/cross-message substitution;
- restore to stale key-status checkpoint and unavailable trust service.

The evidence must pin source commit, build artifact, runtime/library versions, vector blob, exact command, CI run and retained logs. Checked-in vectors without execution are not evidence.

## 6. Explicit exclusions and non-claims

This decision does not certify provider receipts, C gate linearization, provider idempotency, C owner ledger correctness, COC quorum, Storage persistence or downstream application. Cryptographic authenticity is not semantic truth. It does not establish exactly-once delivery or production readiness.

## 7. Conditions for a later registration decision

I requires all of the following exact inputs:

- C final projection artifact and C approval of its field inventory;
- H exact schema 1.2.11 JSON Pointer mapping and validator contract, including dereference rules;
- finalized profile byte-level specification and key-status schema;
- C key authority/trust-root registration and custody evidence;
- independent cross-language vector execution;
- Storage exact-version manifest pinning the complete bundle;
- A integration review confirming owner boundaries and no unresolved downgrade/rollback path.

Only after those inputs exist may I issue a new exact-version registration decision. This document is not that registration.

## 8. Decision

**CONDITIONAL ACCEPTANCE OF THE CRYPTOGRAPHIC SUITE IN PRINCIPLE.** Profile registration, trust-root activation, key custody approval, implementation conformance and production use remain NOT APPROVED.

No cryptographic implementation, HSM/KMS deployment, independent test run or production readiness is claimed.
