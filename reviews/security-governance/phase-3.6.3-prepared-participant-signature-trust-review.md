# I Review — PreparedParticipantReceipt Signature Trust & Governance

- Reviewer role: I — Security & Governance Architect (role-simulated in the coordinating ChatGPT session; not an independently authenticated I-session signature)
- Decision: **CANDIDATE / NO APPROVAL**
- Review class: architecture/security policy review; no cryptographic profile approval
- Target 1: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v2.md`
  - Commit: `337fe8bffa178e64ad8e4750f1ede1d561424edc`
  - Blob: `4ed4234ce548a814a9496adf7a14c4459ea9f7ce`
  - Relevant: §§2–4, 6–8, 10–11, 13.1
- Target 2: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`
  - Commit: `71f0c745961cff7f75ef0ba2ac7bfd6f8aeccb66`
  - Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
  - Relevant: §14 and §§1, 3.1–3.3, 5, 7–9, 13

## Decision summary

The authority separation is directionally sound: a Storage receipt may attest only to Storage's exact prepared participant; I alone owns authorization, PermissionEpoch, revocation ordering, terminal decision and single-use authorization receipt consumption. COC may store an I proof but cannot mint, reinterpret or upgrade it.

However, neither target defines a complete normative signed-byte contract or historical key-status policy. Target 1 §11 explicitly leaves canonicalization, signature algorithms, issuer/audience semantics, key custody, lifecycle, revocation and historical verification OPEN / NOT FROZEN. That is acceptable as an architecture proposal, but it is a hard blocker to security approval, schema freeze and implementation conformance.

## Blocking security findings

### I-1 — No normative signed envelope or exact signature preimage

Target 2 §14.4 lists signer/key version/audience but does not define the complete signed object. Target 1 §§3.1 and 11 refer to signature and canonicalization profile identifiers without selecting a normative byte construction.

Required contract:
- Define a protected envelope with `payload_type`, `schema_version`, `issuer`, `subject`, `owner_authority`, `audience`, `purpose`, `key_id`, `key_version`, `algorithm_profile`, `canonicalization_profile`, `digest_profile`, `payload_digest`, `issued_at`, `signature` and any required trust-evidence reference.
- Signature input MUST be a domain-separated byte string covering the envelope's protected header and the canonical complete payload, not a mutable URL/reference or a digest whose preimage is unspecified.
- Specify duplicate-key rejection, absent-vs-null behavior, Unicode normalization, numeric representation, field ordering and unknown-critical-field behavior.
- The exact algorithm suite and canonicalization profile remain I/H joint freeze decisions; this review does not select one.

### I-2 — Issuer, subject, audience and purpose are not fully bound

The signer identity alone does not prove that a key is authorized to attest this exact Storage fact in this environment.

Required contract:
- Bind issuer principal, signing service, owner authority, subject participant, target environment, audience/service recipient, message purpose/type and protocol version.
- A Storage receipt must be valid only for the intended COC/I/Storage verification contexts and exact message family; cross-environment or cross-purpose reuse is rejected.
- Trust-root identity and owner authority registry version must be verifiable at the relevant signing time.

### I-3 — Key lifecycle and historical verification policy is absent

Required policy must cover key generation/custody, activation, rotation, suspension, revocation, compromise, retirement, destruction, recovery, dual control and audit.

Historical verification MUST distinguish:
1. cryptographic signature validity;
2. whether the key was authorized for that issuer/purpose at signing time;
3. whether the key was later revoked, and the effective time/reason;
4. whether compromise is believed to predate the claimed signing time;
5. whether the retained public key, trust chain, status evidence and trusted time anchor are available.

A later key revocation must not silently rewrite history, but a compromise with an effective time before signing may invalidate the receipt. The policy and evidence source must be explicit. Missing historical status evidence => UNKNOWN / IN_DOUBT, not accepted by default.

### I-4 — Replay, substitution and GID reuse protection is incomplete

The receipt needs explicit bindings for:
- `PreparedParticipantRef`;
- `PreparedTransactionGID`;
- PostgreSQL native XID as a distinct engine-evidence type;
- `CanonicalAuthorityDBRef` and non-reusable `DatabaseIncarnationRef`;
- cluster system identifier and database identity;
- `PublicationOperationId`, `RequestDigest`, participant tuple digest and owner boundary;
- `CausalOrderDomainRef`, `PolicyDomainRef`;
- COC prepare-intent position/digest;
- `PrepareAttemptRef` / generation and durable participant-ledger ref/version;
- receipt type, schema/profile, audience and purpose.

Same identity with changed tuple, incarnation, attempt, digest, authority or audience MUST be CONFLICT. A prior receipt cannot authorize a later attempt.

### I-5 — Restore and anti-rollback trust evidence is underspecified

Target 1 §8 requires independent monotonic anchors, but does not define the authority, retention, verification and recovery procedure for the anchor or for owner key-status evidence.

Required:
- Anchor COC checkpoint, I PermissionEpoch/receipt-consumption ledger and owner key-status snapshots independently.
- Restoring an older snapshot or key-status view MUST NOT make a consumed receipt reusable or resurrect a revoked key.
- Missing, rolled-back or contradictory anchor evidence leaves I gate closed and the operation UNKNOWN.
- Privileged archive/key recovery requires separation of duties and immutable audit.

### I-6 — Atomic I terminal proof and exact Storage final-gate participant must be specified

Target 1 §7.2 requires exact I proof binding and atomic consumption, but I's own transaction contract is not represented as a normative schema.

Required I-authoritative transaction must atomically:
- validate the one-time CommitAuthorizationReceipt and its current PermissionEpoch/key status;
- consume that exact receipt once;
- bind the exact Storage final-gate participant, PreparedParticipantRef, GID, DB incarnation, operation/request/participant digest and owner boundary;
- record the I terminal outcome and sequencer position;
- persist the proof/receipt-consumption record.

A detached COMMIT token or COC observation cannot substitute. If any binding is missing, Storage cannot commit.

## Required negative security vectors

- Signature valid but wrong audience, purpose, environment or owner authority => reject.
- Same signature envelope with changed participant/GID/database incarnation/operation digest => reject.
- Old key revoked before signing time or compromise effective before signing time => reject/UNKNOWN per policy.
- Key-status evidence unavailable or rolled back => UNKNOWN; gate remains closed.
- Duplicate JSON/map keys, noncanonical number, alternate Unicode form or absent/null ambiguity => reject.
- Replayed receipt under a new COC epoch, recovery epoch, prepare attempt or participant => reject.
- Receipt from a cloned/restored database incarnation => reject.
- COC-signed statement presented as I authorization => reject.
- Storage-signed PREPARED receipt presented as I COMMIT_WON => reject.
- I terminal proof referencing another Storage participant or GID => reject.
- Restore of a consumed receipt snapshot cannot permit second consumption.

## Owner boundaries

- I owns authorization receipt issuance/consumption, PermissionEpoch, revocation ordering, I terminal decision, I key policy and I gate release.
- Storage owns its prepared participant, GID/native XID mapping, database identity and visibility resolution.
- H owns wire schema/canonical serialization implementation under I-approved policy.
- COC stores references/proofs and orders events only; it cannot create I authority.
- D, C and G retain their independent authorities.

## Disposition

**CANDIDATE / NO APPROVAL.** The architecture may proceed as a proposal, but I does not approve the signature trust boundary, historical verification policy, JF-10 terminal proof contract, schema freeze or implementation conformance until I-1 through I-6 are normatively specified and reviewed. No cryptographic suite is selected here.

## Review provenance

This is an I-role technical assessment authored by the coordinating session at the user's direction. It is not evidence that the separate I owner session independently reviewed or signed these targets.
