# Phase 3.8.7 — I Review of C Key Status Event Schema and Governance Signature

- Owner: I — Security, Identity and Governance
- C key-status event schema: Blob `908b293eba337e9fa75864cea3704e28a1a8d82e`
- C lifecycle/anti-rollback contract: Phase 3.11.0 Blob `de581ea59e724faf5972217e17b983de641ad3f7`
- C crypto candidate review baseline: Phase 3.8.6 Blob `b2e37b0ba9137f2ef1b9fd65bf815bc136ca28c8`
- Disposition: **STRUCTURAL LIFECYCLE MODEL ACCEPTED; GOVERNANCE SIGNATURE PROFILE ACCEPTED AS CANDIDATE; NO TRUST ROOT OR PROFILE REGISTRATION**
- Provenance: delegated I-role simulation at user's direction; not independent human I Owner approval.

## 1. Authority decision

I accepts the authority separation:
- C owns C data-plane key generation, use and append-only key-status event production.
- I owns the governance trust root, governance-signature profile approval, key lifecycle policy, custody standards, revocation/compromise rules and registration.
- H validates governance signatures, C data signatures, status-at-signing-sequence and current anti-rollback.
- A reviews integration; Storage binds exact immutable ledger/checkpoint evidence.

A C data-plane key MUST NOT activate, revoke or attest its own status. C key-status events are signed by a separate I-governed key authority. The public C key carried by an event is never a trust anchor.

## 2. Candidate governance-signature profile

I accepts the following construction as the candidate `AIMBA-I-KEY-GOVERNANCE-1.0` for C key-status events only:

- Canonicalization: RFC 8785 JCS over strict UTF-8/I-JSON input; duplicate keys rejected.
- Digest: SHA-256.
- Signature: Ed25519, 64-byte signature, unpadded Base64url.
- Governance key namespace and trust root: independent I governance namespace; never the C data-plane key namespace.
- Purpose: `C_KEY_STATUS_EVENT_GOVERNANCE`.
- Audience: exact C key registry / H key-status validator audience; no wildcard.

Exact construction:
1. `P0 = all present schema-allowed CKeyStatusEvent members except event_digest and governance_signature`.
2. `P0Bytes = JCS(P0)`.
3. `event_digest = SHA-256(ASCII("AIMBA-I-KEYSTATUS-PAYLOAD-v1") || 0x00 || P0Bytes)`, lowercase hex.
4. `P = P0 + {event_digest}`; `PBytes = JCS(P)`.
5. `signature_preimage = ASCII("AIMBA-I-KEYSTATUS-SIGNATURE-v1") || 0x00 || ASCII("AIMBA-I-KEY-GOVERNANCE-1.0") || 0x00 || ASCII(message_type) || 0x00 || PBytes`.
6. Ed25519 signature by the I-governed key-status authority, encoded Base64url without padding.

The profile is a candidate construction only. It is not registered, no I governance public key is activated, and no trust root is distributed.

## 3. Key status semantics — ACCEPT WITH REQUIRED STATE MACHINE

I accepts the proposed states and transition model, subject to:
- PENDING cannot sign.
- ACTIVE can sign only for the exact key ID/version/profile/purpose/audience and sequence interval.
- RETIRED forbids new signatures but can preserve historical audit verification.
- REVOKED forbids new signatures at/after the event sequence; historical acceptance is policy-limited.
- COMPROMISED applies the earliest defensible compromise sequence; if that boundary is unknown, fail closed for the affected history.
- DESTROYED proves private-key destruction but does not erase historical public verification/compromise evidence.

Allowed transitions must be enforced by the semantic validator, not JSON Schema alone. Event forks, duplicate sequence, invalid predecessor, key fingerprint rebinding, invalid transition or anti-rollback mismatch are INVALID. Unavailable ledger/checkpoint is UNKNOWN.

## 4. Sequence and anti-rollback decision

I accepts the requirement that C outcome `record_sequence` and key-status `event_sequence` be comparable within the same C authority sequence namespace. This must be proven by the same durable linearizable C sequencer; wall-clock timestamps or independent process-local counters are not accepted.

Every status event must be append-only and linked to its predecessor. The external anti-rollback anchor must bind C authority, sequence namespace, key-status generation/high-water/root, latest event sequence/digest and governance signature. Restore/failover with stale checkpoint, lower generation, missing event or fork must fail closed.

If current key status, governance trust chain or anti-rollback checkpoint is unavailable, the result is UNKNOWN and all dependent C provider egress/admission gates remain closed.

## 5. Required I governance and custody evidence before registration

Before registering either `AIMBA-C-CRYPTO-1.0` or `AIMBA-I-KEY-GOVERNANCE-1.0`, require:
1. I governance root identity, custody and trust-chain registration.
2. Governance key generation, non-exportability/custody, dual control and access audit.
3. C data-key generation and custody/HSM/KMS evidence.
4. Key-status ledger append-only durability and independent monotonic checkpoint.
5. Rotation overlap, emergency revocation, compromise boundary, recovery and destruction drills.
6. Historical signature verification and current-use eligibility policy.
7. Stale restore, checkpoint outage, fork and key-status downgrade tests.
8. H validator implementation wired to authenticated governance and C key-status services.
9. Independent Python/Node vectors for key-status event digest/signature and invalid transitions.

Public deterministic test seeds and checked-in signatures are not operational key custody evidence.

## 6. Disposition

**ACCEPT THE STRUCTURAL LIFECYCLE MODEL AND GOVERNANCE SIGNATURE CONSTRUCTION AS CANDIDATES. DO NOT REGISTER OR DEPLOY.**

I has not approved or activated a governance trust root, C key registry, key custody, HSM/KMS, anti-rollback service or production profile. This review is a delegated role simulation, not an independent human I Owner signature.
