# Phase 3.8.4 — I Cryptographic Profile Addendum for C Provider Outcome (Candidate)

- Owner: I — Security, Identity and Governance
- Base I profile: `AIMBA-I-CRYPTO-1.0`, Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`
- Related H schema: artifact 1.2.11 Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- Status: PROPOSED candidate only; not an I approval of C's authority or Provider Outcome truth.
- Provenance: delegated I-role simulation at user's direction; not independent human I Owner approval.

## 1. Boundary

I owns cryptographic suite governance, key trust/status, anti-rollback, algorithm lifecycle and approval of any profile bundle. C owns the semantic content and exact field projection of CSubmitOutcome. H owns wire encoding and validator implementation. I does not create, certify or reinterpret provider-side-effect evidence.

The existing `AIMBA-I-CRYPTO-1.0` profile is explicitly I-only. It MUST NOT be applied to C merely because C and I share BMCP common-envelope fields.

## 2. Candidate C profile proposal

For cross-owner review only, I proposes that C consider the same cryptographic primitive suite as the I candidate, but under a distinct owner-scoped profile ID and independent key namespace:

- Profile bundle: `AIMBA-C-CRYPTO-1.0` (proposed; not registered/approved)
- Canonicalization: `RFC8785-JCS-1.0` (proposed)
- Signature: `AIMBA-ED25519-SHA256-1.0` (proposed)
- Digest: `SHA-256`
- Signature encoding: Base64url without padding
- JSON constraints: RFC 8785 JCS + RFC 7493 I-JSON, strict duplicate-key rejection, UTF-8 only, no implicit Unicode normalization.

This is not inheritance of I's key material, trust root, authority or projection. C must register its own issuer/authority, key IDs/versions, audience/purpose restrictions, key-status ledger and independent revocation/currentness evidence. I's key status cannot authorize a C signature.

If the deployment has regulatory/FIPS constraints or a different threat model, I must review a separately versioned suite; no silent algorithm fallback or negotiation.

## 3. C projection ownership and required signed fields

C MUST publish the exact message-family projection. At minimum the immutable CSubmitOutcome projection must bind:
- schema ID, wire family version and exact schema artifact revision;
- message type, message ID, nonce, audience, sender/issuer/subject and owner authority;
- owner record ref and immutable CSubmitOutcome ref;
- C admission ref/digest and C ledger/version/local sequence/high-water/root;
- C gate ref and CGateGeneration;
- ProviderAttemptRef and ProviderAttemptGeneration;
- provider, account, adapter, endpoint, region and API operation;
- idempotency namespace and key reference;
- final request boundary ref and exact request digest;
- outcome enum and outcome evidence/no-handoff/not-invoked/lookup proof refs/digests;
- ParticipantIntent/Reservation refs or explicit null + reason;
- creation/validity metadata and key ID/version/profile identifiers.

C may add fields, but no semantic owner-authored field may be omitted from the projection. Coordinator-added quorum/COC position proofs and transport channel-binding evidence are separately verified and excluded only under an exact H-published projection rule.

## 4. Candidate two-stage construction

Subject to C/H/I approval of the exact C projection:
- `P0Bytes = JCS(P0)`
- `payload_digest = SHA-256(ASCII("AIMBA-C-PAYLOAD-v1") || 0x00 || P0Bytes)`, lowercase hex
- `P = P0 + { payload_digest }`
- `PBytes = JCS(P)`
- `signature_preimage = ASCII("AIMBA-C-SIGNATURE-v1") || 0x00 || ASCII("AIMBA-C-CRYPTO-1.0") || 0x00 || ASCII(message_type) || 0x00 || PBytes`
- `signature = Ed25519.Sign(C_private_key, signature_preimage)`, Base64url without padding.

Distinct C domain tags and key namespace prevent an I signature from being replayed as C authority. The proposed profile does not authorize reuse of I keys, I receipts or I's P0 allowlist.

## 5. Key trust and lifecycle

C key identity must be bound to `(C IssuerRef, C OwnerAuthority, KeyIdRef, KeyVersion, ProfileId, Purpose, Audience)`. C key-status records must be append-only and anchored to C's durable authority, with I-approved governance controls where required. H verifies using authenticated C trust/key-status evidence, not payload-supplied public keys.

The profile must define PENDING/ACTIVE/RETIRED/REVOKED/COMPROMISED/DESTROYED states, effective sequencer boundary, historical verification, compromise disposition, rotation, nonce replay and restore anti-rollback. If C key status or external anti-rollback anchor is unavailable, verification is UNKNOWN and dependent gates remain closed.

## 6. I disposition

I proposes the candidate suite and domain-separated construction for C review. I does **not** approve C profile registration, C trust roots, C key custody, C key lifecycle implementation, H 1.2.11 wire mapping or production use. C must accept the semantic projection; H must publish exact schema/validator mapping; I must then review the resulting exact profile and trust lifecycle before any freeze.

No cryptographic implementation, key registry, HSM/KMS, test execution or production deployment is claimed.
