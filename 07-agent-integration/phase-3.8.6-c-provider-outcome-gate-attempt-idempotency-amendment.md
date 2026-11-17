# Phase 3.8.6 — C Provider Outcome Gate/Attempt/Idempotency Semantic Amendment

- Owner: C — Agent Integration / Provider transport boundary
- Status: PROPOSED C normative amendment; exact H schema 1.2.11 semantic binding and implementation tests OPEN.
- Supersedes no earlier C contract; extends Provider Egress Gate Adapter contract Blob `a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca`.
- Related H schema artifact 1.2.11 Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`.
- Provenance: delegated C-role simulation at user's direction; not independent human Owner approval.

## 1. Immutable attempt tuple

Every physical provider handoff attempt MUST have one immutable tuple:

`(CSubmitOutcomeRef, CAdmissionRef, CAdmissionDigest, CGateRef, CGateGeneration, ProviderAttemptRef, ProviderAttemptGeneration, ProviderRef, ProviderAccountRef, AdapterRef, EndpointRef, RegionRef, IdempotencyNamespaceRef, IdempotencyKeyRef, FinalRequestBoundaryRef, RequestDigest, COCParticipantIntentRef?, COCParticipantReservationRef?)`.

All opaque refs are authority-issued. A retry that can cause a new physical send MUST allocate a new ProviderAttemptRef/Generation and obtain a fresh current gate CAS; it MUST NOT silently reuse the prior attempt. A same-key reconciliation query is not a new send attempt and must bind the original tuple. A changed request digest, target/provider/account/endpoint/region, idempotency namespace or key is a different operation and MUST be rejected as conflict, never merged into the original outcome.

The exact values MUST be included in the immutable CSubmitOutcome payload and its C owner signature projection. If the BMCP 1.2.11 message does not carry them inline, its typed `c_submit_outcome_ref` MUST dereference to an immutable C-owned object containing every tuple member and the exact schema/profile revision. H semantic validation MUST compare all duplicated inline values with that object; absence, ambiguity or mismatch is INVALID/UNKNOWN as specified below.

## 2. Gate close / egress linearization

The transport-owning Adapter is the only component allowed to invoke the provider SDK/client. `CommitEgress` and `CloseEgressGate` MUST use the same durable, linearizable serialization authority and monotonically increasing CGateGeneration.

- Close CAS wins: generation advances and state is CLOSED; every older uncommitted admission is permanently ineligible. Adapter MUST NOT write any provider bytes for it.
- Egress CAS wins: immutable attempt becomes EGRESS_COMMITTED under the exact prior generation and must be included in close's in-flight set. Close cannot report that this attempt was prevented.
- If an Adapter process dies after EGRESS_COMMITTED and before transport result persistence, outcome is UNKNOWN/IN_DOUBT. Never infer NOT_INVOKED from process death.
- The Adapter must prove the transport invocation is exactly the one bound to the EGRESS_COMMITTED immutable bytes. Hidden SDK retries, redirects, endpoint failover and stream continuations are forbidden unless each physical send re-enters this gate and receives a distinct attempt.
- A process-local mutex or cached OPEN token is insufficient. Multi-replica correctness requires a durable single-writer/consensus/transactional serialization proof and restore anti-rollback.

## 3. Provider idempotency namespace and same-key lookup

For each supported provider adapter, C MUST publish a provider capability record binding:
- provider, tenant/account, endpoint/region and API operation;
- idempotency namespace and key syntax/uniqueness scope;
- provider key retention/expiry and maximum delayed-request horizon;
- whether same-key replay is guaranteed not to create a second side effect;
- authoritative lookup/status API and its consistency/visibility guarantees;
- proof issuer, receipt authentication and key-status/trust source;
- exact distinction between accepted, rejected-before-side-effect, rejected-after-possible-side-effect and not-invoked;
- behavior after provider failover, account migration, retention expiry and provider outage.

A lookup proof MUST bind the original ProviderAttemptRef/Generation, provider/account/endpoint, namespace/key, exact FinalRequestBoundaryRef and RequestDigest, original request ID and authoritative lookup position/result. A provider status endpoint that cannot correlate all these values is not authoritative for this protocol.

No generic exactly-once property is assumed. Same-key provider behavior is provider-specific and must be verified before activation. If the provider lacks authoritative lookup or its key retention is shorter than the maximum ambiguity/recovery horizon, unresolved attempts remain IN_DOUBT and the protected operation/gates remain blocked; no retry-as-new-operation is allowed.

## 4. Outcome semantics and mandatory evidence

### HANDOFF_ACCEPTED
Requires authenticated transport/provider evidence proving the exact immutable request crossed the defined provider handoff boundary, correlated to the exact attempt tuple. It proves neither inference completion, model execution, downstream Memory Brain durability/visibility, user delivery nor G Applied.

### HANDOFF_REJECTED
Requires authenticated provider evidence proving rejection of the exact attempt. If the evidence does not prove no external side effect occurred, this outcome remains nonterminal for retry/forget purposes and MUST be represented as UNKNOWN/IN_DOUBT (or retain REJECTED plus a separate explicit side-effect-unknown terminality flag in a later schema revision). It MUST NOT be interpreted as NOT_INVOKED.

### NOT_INVOKED
Requires an Adapter-origin, durable, signed no-handoff proof from the same serialization authority proving the exact attempt never crossed EGRESS_COMMITTED/transport invocation. Valid examples are close-CAS-won-before-commit or a durable pre-transport abort with invocation counter/ledger proof. Timeout, absent database row, lost ACK, worker death, queue emptiness, provider lookup absence or partial transport write is insufficient unless the provider/transport contract proves authoritative absence.

### UNKNOWN / IN_DOUBT
Nonterminal. Preserve the original tuple, request bytes/digest, key and evidence. No new operation/attempt may be created as a substitute. Reconciliation is by authoritative same-key lookup against the same immutable tuple. Missing/unavailable lookup, retention expiry or contradictory receipts leaves IN_DOUBT.

## 5. Append-only outcome and contradictions

CSubmitOutcome is immutable and append-only. A later observation is a new linked reconciliation/superseding record; it never edits or overwrites the earlier observation. The semantic validator MUST reject:
- ACCEPTED with no provider handoff receipt/evidence;
- NOT_INVOKED with provider receipt or EGRESS_COMMITTED evidence;
- REJECTED represented as safe no-side-effect without an authoritative no-side-effect proof;
- two different terminal outcomes for the same attempt without a valid supersession/reconciliation chain;
- any mismatch in request digest, boundary, attempt, provider/account, key namespace, gate generation, admission digest or C ledger sequence;
- stale gate generation at final egress commitment;
- lookup proof for a different attempt, key, account, endpoint or request digest.

A conflicting immutable record is INVALID and must be preserved as evidence; it must not be overwritten by the later record.

## 6. BMCP 1.2.11 field/dereference binding

For `C_PROVIDER_OUTCOME_RECORDED`, H MUST:
1. Validate the five wire enum values and outcome-specific required refs from schema 1.2.11.
2. Dereference `c_submit_outcome_ref` and compare `c_submit_outcome_digest` against canonical immutable C payload bytes.
3. Validate C gate, gate generation, provider attempt ref/generation, admission ref/digest, final request boundary/digest, provider/account/adapter/endpoint/region and idempotency namespace/key from the immutable C object.
4. Dereference C owner admission/ledger and prove sequence <= high-water and root/version consistency, with no missing admission.
5. Validate COC ParticipantIntent/Reservation pair or explicit null + reason; when non-null, compare exact operation/request digest and reservation position. A null COC intent does not erase C's owner-local admission requirement.
6. Verify provider evidence/lookup/no-handoff proof issuer and trust separately from C owner signature.
7. Return INVALID for cryptographic/digest/identity contradiction; UNKNOWN for unavailable authoritative evidence, stale/unavailable key status or incomplete lookup. Both fail closed for release/Full Applied.

## 7. Required provider adapter conformance

For every production provider/account/endpoint class, add executable tests for close-vs-send linearization, multi-replica race, crash before/after EGRESS_COMMITTED, partial write, lost ACK, same-key lookup, duplicate same-key send, key expiry, provider outage, endpoint failover, SDK retries/redirects/stream continuation, conflicting receipts and restore anti-rollback. Each result must pin adapter build, provider sandbox/API version, test fixture, exact request digest, logs/evidence and CI run.

Status: specified, NOT RUN. No provider is certified by this document. No production activation or universal exactly-once claim.
