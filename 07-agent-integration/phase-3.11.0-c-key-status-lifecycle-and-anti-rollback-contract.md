# Phase 3.11.0 — C Key Status Lifecycle and Anti-Rollback Contract

- Owner: C — Provider Outcome signing authority
- Governance owner: I — trust policy, governance root and key lifecycle approval
- Key-status event schema: `schemas/c-key-status-event-1.0.0.schema.json`, Blob `6159004500bd188438e4bf898bf1a2a77ba6dd59`
- C data profile candidate: `AIMBA-C-CRYPTO-1.0` (NOT REGISTERED)
- Governance signature profile candidate: `AIMBA-I-KEY-GOVERNANCE-1.0` (NOT REGISTERED)
- Status: PROPOSED lifecycle and anti-rollback contract; no production key registry or custody is deployed.
- Provenance: delegated C-role simulation at user's direction; not independent human C Owner approval.

## 1. Authority separation

- C owns creation of its data-plane Ed25519 keypairs, C issuer binding, C key-status event publication and use of a C key for CSubmitOutcome.
- I owns approval of the governance trust root/profile, required custody controls, revocation/compromise policy and profile registration decision.
- H validates governance signatures, C data signatures, key status at signing sequence and current anti-rollback checkpoints.
- A reviews owner boundaries; Storage pins exact key-status snapshots and audit joins.

A C data-plane key MUST NOT sign its own key activation, revocation or compromise event. Key-status events are signed by an independently governed I-approved key-governance authority under the separate candidate `AIMBA-I-KEY-GOVERNANCE-1.0`. The C public key contained in an event is data, never a trust anchor.

## 2. Key identity and scope

A C data key is uniquely identified by:

`(CKeyAuthorityRef, KeyIdRef, KeyVersion, ProfileId, Purpose, Audience)`.

No wildcard purpose or audience is permitted. The key-status event binds the exact Ed25519 public key (32-byte raw key, unpadded Base64url), its SHA-256 fingerprint, C authority, I governance authority, profile, purpose and audience.

The same KeyIdRef/KeyVersion cannot be rebound to a different public-key fingerprint, issuer, profile, purpose or audience. Rebinding requires a new key version and a new event chain.

Private keys and provider idempotency secrets MUST NOT be committed to GitHub or included in event payloads. Only public verification material and opaque references are published.

## 3. Append-only event model

Each status transition is a new immutable `CKeyStatusEvent`:
- `event_sequence` is a canonical decimal string in the C key authority's monotonic sequence namespace;
- `previous_event_ref/digest` links the exact prior event for the same key identity;
- `anti_rollback_anchor_ref/digest` binds the externally retained monotonic checkpoint;
- the governance signature authenticates the event under the I-approved governance trust chain.

No event is overwritten or deleted. A correction is a new event with an explicit reason and a valid predecessor link. Forks, sequence reuse, missing predecessors, digest mismatch or stale checkpoint are INVALID. An unavailable authoritative ledger/checkpoint is UNKNOWN.

For a key used to sign a CSubmitOutcome, `record_sequence` and the key-status event `event_sequence` MUST be comparable within the same C authority sequence namespace. C MUST allocate the outcome's signing sequence and resolve the latest applicable key-status event through the same durable linearizable authority. Wall-clock comparison across services is not a substitute.

## 4. State transition rules

Allowed state transitions:

| Prior state | Allowed next state |
|---|---|
| none | PENDING |
| PENDING | ACTIVE, DESTROYED |
| ACTIVE | RETIRED, REVOKED, COMPROMISED |
| RETIRED | REVOKED, COMPROMISED, DESTROYED |
| REVOKED | COMPROMISED, DESTROYED |
| COMPROMISED | DESTROYED |
| DESTROYED | none |

- PENDING: key is registered but cannot sign.
- ACTIVE: key may sign only for its exact profile/purpose/audience and within the effective sequence range.
- RETIRED: no new signatures; historical verification remains possible subject to compromise/currentness rules.
- REVOKED: no new signatures after the event sequence. Historical signatures may be accepted for audit only if policy and evidence establish they predate revocation and are not compromised.
- COMPROMISED: reject new signatures and reject historical signatures at or after the declared earliest-compromise sequence. If the compromise boundary cannot be established, fail closed for the affected interval.
- DESTROYED: private key destruction is attested; public verification material remains retained as needed for audit. Destruction does not erase prior status or compromise history.

An invalid transition is INVALID. A missing event or unavailable checkpoint is UNKNOWN, not ACTIVE by default.

## 5. Signing-time and current-use predicates

For a CSubmitOutcome with signing sequence (S), the validator must establish:
1. the key's latest applicable event at (S) is ACTIVE;
2. key identity, profile, purpose, audience and fingerprint match exactly;
3. the C outcome sequence and key-status sequence share the same C authority sequence namespace;
4. no RETIRED/REVOKED/COMPROMISED transition is effective at or before (S);
5. the current key-status head and anti-rollback checkpoint are at least as new as the trusted external checkpoint;
6. the governance signature chain for every event is valid.

Historical signature validity and current authorization are separate outputs. A retired key can remain cryptographically verifiable for audit but cannot authorize new work. A compromised key is subject to the declared earliest compromise boundary; no fallback to current wall-clock timestamps is allowed.

## 6. Anti-rollback and restore

C key-status ledger MUST have an external monotonic checkpoint independent of the C application database and backup/restore path. The checkpoint binds:
- C key authority and sequence namespace;
- key-status ledger generation/high-water/root;
- last event sequence and digest;
- governance authority and checkpoint signature;
- restore generation and attestation.

On startup, failover, disaster recovery or restore:
- compare the restored ledger against the latest external checkpoint;
- reject stale roots, lower generations, sequence rollback, event deletion or fork;
- if the checkpoint service is unavailable, return UNKNOWN and prohibit signing/verification-dependent admission;
- never reconstruct ACTIVE state from local cache, environment variables or a prior snapshot without authenticated checkpoint reconciliation.

## 7. Required tests and operational evidence

Before profile registration, require:
- valid PENDING -> ACTIVE transition and rejection of PENDING signing;
- valid ACTIVE -> RETIRED/REVOKED/COMPROMISED transitions and invalid transition rejection;
- key ID/version/fingerprint/profile/purpose/audience substitution;
- same key ID/version rebound to another public key;
- signing sequence immediately before/at/after each status transition;
- compromise earliest-boundary and unknown-boundary behavior;
- duplicate event, missing predecessor, fork, sequence rollback and digest mismatch;
- stale backup restore, stale anti-rollback anchor and checkpoint outage;
- governance signature invalidity, expired/revoked governance key and unavailable trust root;
- rotation overlap, emergency revocation and destruction attestation;
- custody/HSM/KMS evidence, least privilege, access logs, dual control and compromise drill.

Every executed test must pin the schema, source/build, key test fixture, exact command, CI run, expected/actual status and retained logs. Public test keys do not prove production custody.

## 8. Release decision

**PROPOSED — KEY STATUS AND ANTI-ROLLBACK CONTRACT DEFINED; NO PROFILE REGISTRATION OR PRODUCTION KEY AUTHORIZATION.**

This contract does not claim that a C key registry, I governance root, HSM/KMS, append-only ledger, external checkpoint, production verifier or operational drill exists. I must review and approve the exact schema, trust-root ownership, governance signing profile and lifecycle before C can register `AIMBA-C-CRYPTO-1.0`.
