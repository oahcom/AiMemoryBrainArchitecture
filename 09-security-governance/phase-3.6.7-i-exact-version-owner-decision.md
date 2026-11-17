# Phase 3.6.7 — I Exact-Version Owner Decision

- Decision authority represented: I — Security & Governance
- Decision class: exact-blob semantic review of the Phase 3.6.7 I Gate / Admission / Release amendment
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Decision scope: architecture semantics only; no implementation or production approval
- Reviewed I amendment commit: `b0723c61a22d1f1d82bf395d37e0602d2c863d73`
- Reviewed I amendment blob: `0d0b4fb0f5921e63b6ebfd70b62afa31d3d5fdf7`
- Companion Storage Design v3.1 blob: `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- Companion COC protocol blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- Historical Storage Design v2 blob: `4ed4234ce548a814a9496adf7a14c4459ea9f7ce` (not current companion)

## 1. Exact-version disposition

I accepts the reviewed Phase 3.6.7 I amendment as the correct owner-local semantic direction for:
- I-only PolicyDomain permission/revocation Gate authority;
- owner-local monotonic IGateGeneration and atomic request/high-water capture;
- complete I request/receipt issue/consume in-flight inventory, including work not yet represented in COC;
- separation of I terminal JF-10 decision atomicity from I outage-Gate release;
- I-only signed release authority and explicit non-implications for D, Storage, COC and global Forget completion.

This is **not unconditional acceptance**. The exact blob is accepted only with the mandatory amendments below. The reviewed blob remains immutable; amendments MUST be published as a new append-only revision and reviewed by exact blob.

## 2. Mandatory amendments before I semantic freeze

### I-M1 — Bind the global inventory snapshot and D reconciliation tuple

The I request snapshot is not the same thing as I's global Producer/Recipient/Backup inventory snapshot. The amendment MUST bind, in a typed reconciliation receipt, both:
- I request Gate state: GateRef/IGateGeneration, request high-water/root, PermissionEpoch, sequencer position;
- I global inventory state: PolicyDomainRef, normalized scope binding, ProducerDomainInventoryEpoch, registry snapshot digest, relevant entry generations, TargetInventorySealRef/digest and completeness-proof generation/status;
- D state: ForgetOperationRef, D FenceGeneration, D registration/work high-waters, barrier-membership root, dependency-closure digest/cursor;
- COC state: RecoveryEpoch, exact prefix, batch and participant-manifest digests;
- restore identity where applicable: RestoreAttemptRef and restore checkpoint generation.

I must not conflate IRequestHighWater with ProducerDomainInventoryEpoch. Both are required and independently monotonic.

### I-M2 — Define inventory epoch currentness and race closure

Before I issues an inventory completeness or I release proof, it MUST revalidate that the current ProducerDomainInventoryEpoch, registry digest, relevant entry generations, signer/key status and evidence generations still equal the attested values. If not, the proof is stale and must be resealed/re-evaluated.

The protocol must define the atomic/currentness boundary against a concurrent registry mutation. A read-then-sign sequence without a linearizable epoch check is insufficient. If a race cannot be excluded by the authoritative sequencer/CAS, the result is UNKNOWN and I Gate remains closed.

### I-M3 — Tighten receipt consumption against exact participant tuple

The final I sequencer transaction must consume the receipt exactly once against the complete Storage tuple, including COC term/index or equivalent typed position, COC entry digest, DatabaseIncarnationRef, PostgreSQLNativeXID where known, PrepareAttemptGeneration, ParticipantLedgerVersion, ParticipantTupleDigest and owner boundary. Define behavior when native XID is learned after initial intent: immutable append-only enrichment must preserve the same participant/attempt identity and cannot silently replace a field.

### I-M4 — Specify stale admission and cross-boundary enforcement

Define how every protected issuer/consumer validates the current I Gate generation at its authoritative admission/consume point, including stale caches, partitioned workers, retries and leader change. A process observing an old OPEN state must not issue or consume a receipt after Gate close. State the required fencing token / sequencer read and fail-closed behavior.

### I-M5 — Restore and anti-rollback release handshake

I release after restore must bind exact RestoreAttemptRef, restored checkpoint, current non-forked sequencer/registry epochs, anti-rollback anchor and D's current fence/barrier/closure tuple. Both owner snapshots must be revalidated immediately before serving/release. I release alone must never authorize D or Storage serving.

## 3. I-owned atomicity and in-flight admission decisions

I confirms the required linearization point is one durable owner-local transaction/CAS which atomically closes the I Gate, increments IGateGeneration, appends the request and captures the exact I request ledger high-water/root. The operation is not acknowledged as pending before that commit.

The following are mandatory I in-flight classes and cannot be excluded for lacking a COC ParticipantIntent:
- request admitted but not COC registered;
- receipt issuance in progress or ACK lost;
- receipt consumption in progress or outcome uncertain;
- COC intent committed but I terminal decision absent;
- I decision consumed but Storage/COC observation delayed;
- retry/replay/duplicate/lease-expiry/worker restart;
- restored/replayed work and post-high-water discoveries.

## 4. Independent I Release rule

I may issue `IGateReleaseReceipt` only after:
1. exact COC RecoveryEpoch/prefix/batch/manifest verification;
2. exact request-ledger reconciliation through captured high-water;
3. terminal or proven safe non-effect disposition for every receipt issue/consume operation;
4. exact PreparedParticipant tuple join for every I decision affecting Storage;
5. single-use receipt consumption and current PermissionEpoch/sequencer order;
6. current registry epoch/digest/key status and anti-rollback evidence;
7. D/I/COC/restore tuple currentness per I-M1/I-M2/I-M5;
8. zero unresolved UNKNOWN, missing evidence, scope ambiguity or conflicting digest.

UNKNOWN, lost ACK, timeout, expired lease, missing worker, stale epoch or unverified restore is blocking. Only I releases I Gate. This does not clear D Fence, resolve Storage XIDs, or imply Global Forget Completion.

## 5. Non-negotiable authority boundary

- I alone issues I Gate close/release attestations and I terminal authorization decisions.
- D alone issues D Forget Fence/barrier/release evidence.
- Storage alone attests participant durability and its visibility outcome.
- COC orders and persists evidence but cannot mint or substitute any Owner proof.
- A integration acceptance cannot replace I's owner-local proof.

## 6. Final decision

**ACCEPT WITH ENUMERATED AMENDMENTS** for the exact reviewed I amendment blob `0d0b4fb...`, subject to I-M1 through I-M5. No semantic freeze until these are incorporated and exact-version re-reviewed.

Not approved: implementation conformance, cryptographic/key-profile freeze, production activation, global inventory completeness, global Forget completion, physical erasure, or release of any live Gate.

## 7. Authorship and provenance

This is a delegated role-based architectural decision record prepared in this ChatGPT session and committed to I's working branch at the user's direction. It is not a cryptographic signature or proof that a separate human I Owner independently authored or approved it. Treat it as a proposed I decision for governance review, not independent human sign-off.
