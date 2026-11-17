# Phase 3.8.7 — C Review of I Candidate C-Scoped Cryptographic Profile

- Owner perspective: C — Provider Outcome authority
- I proposal: `AIMBA-C-CRYPTO-1.0`, addendum Blob `1bcddbaaa4a9ca730d492a6554941becac305668`
- C semantic amendment: Phase 3.8.6 Blob `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4`
- H schema: 1.2.11 Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- Disposition: **ACCEPT AS CANDIDATE CONSTRUCTION; PROFILE REGISTRATION / TRUST / WIRE FREEZE OPEN**
- Provenance: delegated C-role simulation at user's direction; not independent human C Owner approval.

## 1. C authority decision

C accepts the proposed *shape* of an owner-scoped, domain-separated C profile:
- distinct profile bundle ID `AIMBA-C-CRYPTO-1.0`;
- RFC 8785 JCS / RFC 7493 I-JSON candidate canonicalization;
- SHA-256 payload digest;
- Ed25519 signature and canonical unpadded Base64url encoding;
- C-specific `AIMBA-C-PAYLOAD-v1` and `AIMBA-C-SIGNATURE-v1` domain separation;
- independent C key namespace, C issuer/authority and C key-status lifecycle.

This does not reuse I's key material, I trust root, I owner projection, I receipt or I authorization. C remains sole authority for provider outcome truth and exact CSubmitOutcome semantic fields. H remains responsible for exact message-family wire projection and validator behavior. I remains responsible for cryptographic governance and trust-profile approval.

## 2. C-owned projection requirements

The exact C P0 MUST include every immutable C-authored field in the exact schema and referenced CSubmitOutcome object, including:
- schema ID, wire family and artifact revision;
- message identity, nonce, audience, sender/issuer/subject and C owner authority;
- immutable CSubmitOutcome ref and record identity;
- C admission ref/digest, ledger/version/sequence/high-water/root;
- C gate ref/generation and provider attempt ref/generation;
- provider/account/adapter/endpoint/region/API operation;
- idempotency namespace/key reference;
- final request boundary and exact request digest;
- outcome enum and outcome-specific evidence refs/digests;
- ParticipantIntent/Reservation or explicit null + reason;
- C-authored creation/validity metadata and key/profile identifiers.

C accepts I's proposed construction only on condition that H publishes an exhaustive exact P0 field allowlist for `C_PROVIDER_OUTCOME_RECORDED` and the dereferenced immutable CSubmitOutcome object, with no wildcard exclusions. COC quorum/position fields and transport channel-binding evidence remain separately verified under their own authority.

## 3. Conditions before acceptance/freeze

1. I must formally approve the C-scoped profile bundle, trust/key-status authority, custody controls, revocation/compromise boundary, historical verification and anti-rollback policy. I's current document is a proposal only.
2. C must publish its exact final projection allowlist and stable record semantics; no profile may sign an incomplete projection.
3. H must bind schema artifact 1.2.11 / wire family 1.3.0 to the exact C profile and validator; profile ID and artifact revision are mandatory for protected C outcomes.
4. C/H/I must produce canonical-byte, digest and signature vectors, including mutation of each signed field, duplicate keys, null/absent distinction, profile downgrade, wrong audience, wrong key version and cross-message replay.
5. Independent implementations must execute and publish reproducible results against exact pinned blobs. A checked-in vector is not execution evidence.
6. Key status, C ledger and external anti-rollback checkpoints must survive crash/restore/failover; unavailable currentness yields UNKNOWN and closed gates.

## 4. Decision

**ACCEPT AS CANDIDATE CONSTRUCTION ONLY.** No C signature profile is registered or frozen by this review. C does not accept I's authority over C provider truth or C's owner projection. No cryptographic implementation, HSM/KMS, conformance execution or production readiness is claimed.
