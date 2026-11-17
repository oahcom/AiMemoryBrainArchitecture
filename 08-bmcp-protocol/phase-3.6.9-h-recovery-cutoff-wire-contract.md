# Phase 3.6.9 — H Recovery Cutoff, Owner Admission & Gate Release Wire Contract

- Owner perspective: H — BMCP Protocol Architect
- Status: **PROPOSED H WIRE CONTRACT — EXACT-VERSION H / I / A REVIEW REQUIRED**
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT INTEROPERABILITY-VERIFIED
- Schema companion: `schemas/bmcp.recovery-cutoff-1.0.1.schema.json`

## 0. Exact normative source bundle

| Source | Exact Blob |
|---|---|
| A Phase 3.6 COC deployment architecture §§11–12 | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| COC durable log / recovery protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| I Phase 3.6.8 amendment | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 amendment | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C Phase 3.6.9 proposal | `104434dc5682ce84ef9f26f3141540a897e4436d` |

The H schema is a candidate mapping of the exact A §§11–12 recovery semantics. It does not select I's signature algorithm, trust-root, key lifecycle or historical-verification policy. It does not claim cross-language canonical-byte interoperability.

## 1. Message families

The current schema candidate is **1.0.1**. It supersedes the first 1.0.0 draft because the first draft combined owner request and admission sets under one root and represented the COC participant manifest as a bare ref list. Version 1.0.1 separates request and admission enumerations and gives every COC participant a typed entry with operation identity, digest and prefix coordinates. The 1.0.0 file is retained as historical drafting evidence, not the current review target.\n\nThe schema defines six strict message families:

1. `OWNER_ADMISSION_SNAPSHOT_ATTESTATION` — I/D/C owner-local request/admission snapshot, including explicit complete-empty state.
2. `COC_PARTICIPANT_MANIFEST` — exact enumeration of ParticipantIntentRefs in a quorum-confirmed COC prefix.
3. `RECOVERY_CUTOFF_BATCH` — immutable batch joining the exact prefix, participant manifest and separately signed I/D/C owner snapshots.
4. `OWNER_ADMISSION_ENTRY` — immutable owner-local member record; explicitly REGISTERED or NOT_REGISTERED with no fabricated COC identity.
5. `OWNER_GATE_RELEASE_ATTESTATION` — owner-only release of that owner's outage gate against exact batch/manifest/snapshot roots.
6. `RECOVERY_EPOCH_COMPLETED` — COC completion observation after required batch rounds, participant reconciliation and independent owner releases.

## 2. Complete-empty versus not-enumerated

The only valid complete enumeration states are:

- `COMPLETE_NON_EMPTY`: a non-empty canonical member array, count greater than zero, and root/digest over the canonical member representation.
- `COMPLETE_EMPTY`: an explicitly present empty array, count exactly zero, and root/digest over the canonical empty representation.

The following are never equivalent to COMPLETE_EMPTY: missing array, null, unavailable ledger, query failure, partial pagination, stale replica, timeout, UNKNOWN, NOT_ENUMERATED or a zero count without a verifiable canonical empty root.

The receiver MUST validate all four together: status, array presence/content, count and root. A schema-valid message is not proof that the source query was complete; the owner attestation and independent authoritative verification remain required.

## 3. Two independent completeness domains

The RecoveryCutoffBatch MUST bind two distinct sets:

- **COC prefix participant set:** exact quorum-committed ParticipantIntentRefs enumerated from the committed prefix and its root.
- **Owner-local admission sets:** all I/D/C accepted requests, receipts, work, reservations and provider attempts, including admissions not yet registered in COC.

The sets may overlap. They MUST NOT be collapsed into one synthetic list or global sequence. Every owner admission entry carries `REGISTERED` plus exact ParticipantIntentRef/position/digest, or `NOT_REGISTERED` plus stable owner-local identity and reason. A NOT_REGISTERED entry is never assigned a fabricated ParticipantIntentRef.

## 4. Batch and repeated-round invariants

A RecoveryCutoffBatch binds:
- RecoveryEpoch and immutable round identity;
- exact quorum-confirmed COC prefix position/root and prior-prefix digest;
- COC ParticipantManifest identity/digest/count;
- separate I, D and C snapshot attestations and their local high-waters/roots;
- exact scope binding and the reconciliation attempt generation;
- quorum commit proof and batch digest.

An owner request that linearizes after its captured high-water remains behind that owner's closed gate. It is included in a subsequent immutable batch round. If any owner high-water, scope generation, admission root or relevant inventory projection advances during reconciliation, the release candidate becomes stale. Earlier rounds are never mutated or overwritten.

IRequestHighWater, IGateGeneration, PermissionEpoch, ProducerDomainInventoryEpoch, D FenceGeneration, C high-waters, Storage ledger versions and COC positions are nominally distinct. The wire contract does not authorize arithmetic comparison across them.

## 5. Gate release authority

An `OWNER_GATE_RELEASE_ATTESTATION` is signed/issued by exactly one owner authority (I, D or C) for its own gate generation and exact sealed snapshot. COC can record and verify the release evidence but MUST NOT mint, infer or issue it.

- I release does not imply D or C release, Storage visibility, revocation completion or Global Forget Completion.
- D outage-gate release does not clear the effective Forget Fence or prove lineage completion.
- C outage-gate release does not prove provider success or authorize replay of an unresolved provider attempt.
- No owner release is valid if its high-water/root/scope generation differs from the final current authoritative snapshot.

`RECOVERY_EPOCH_COMPLETED` is a COC observation that all required rounds and owner receipts have been recorded. It is not itself an owner gate release or a terminal I/D/C decision.

## 6. Required cross-message semantic validators

The JSON Schema enforces structural requiredness, enums, strict additional-property rejection and basic conditional field presence. A validator MUST additionally enforce:

1. Owner authority matches owner kind and the exact gate namespace.
2. Owner signature envelope issuer/subject/audience/purpose and trust status validate under I policy.
3. Snapshot and each member list are immutable, ordered canonically and rooted under the declared profile.
4. COMPLETE_EMPTY has present empty array, zero count and the canonical empty-set digest; all other statuses reject it.
5. ParticipantManifest prefix/root exactly matches the quorum-committed COC prefix; no stale follower or partial page is accepted.
6. RecoveryCutoffBatch binds the exact snapshot attestation digests and ParticipantManifest digest; no missing owner is treated as empty.
7. Every REGISTERED owner admission maps to one exact participant identity and digest; NOT_REGISTERED never carries a ParticipantIntentRef.
8. Post-high-water requests force a subsequent batch round before that owner's release.
9. Release receipt matches current gate generation, snapshot generation, high-water, root, scope and anti-rollback anchor at the owner's release CAS.
10. RecoveryEpochCompleted requires all required rounds and all required owner-only release attestations; it cannot substitute for them.
11. Duplicate message identity + same digest is idempotent; same identity + changed digest is immutable CONFLICT.
12. Unknown critical fields, unsupported versions, downgrade, absent/null substitution and noncanonical encodings fail closed.

## 7. Ownership split and non-claims

- I owns its request ledger, receipt issue/consume, global inventory and I release.
- D owns its Forget Fence, work/lineage barrier and D release.
- C owns its admission/provider attempt ledger and C release.
- Storage owns its prepared participant ledger and same-XID resolution.
- COC owns quorum prefix, participant manifest, batch append and recovery epoch observation.
- H owns schema, field encoding, requiredness, canonicalization and interoperability fixtures.
- I owns signature trust policy and cryptographic profile approval; H implements but does not unilaterally select it.

**Status:** H wire proposal only. Exact H Owner acceptance, I trust-policy approval, A integration acceptance, canonical-byte interoperability and executable validator tests remain OPEN. No schema freeze, runtime conformance, deployment or production activation is claimed.


## 8. 1.0.1 schema refinement and current review target

The 1.0.0 candidate was found insufficient during coordinator self-review: it used one owner member array/root despite distinct request and admission high-waters, and its COC participant manifest contained only opaque participant refs. Those shapes could not independently prove request-set completeness, admission-set completeness and per-participant operation binding.

The 1.0.1 candidate corrects this by:
- separate `request_members` and `admission_members`, each with independent enumeration status, count and root;
- explicit scope generation in the owner snapshot;
- richer owner admission entries binding operation identity/digest, scope, effect boundary, source/lineage/attempt/reservation/provider/idempotency evidence where applicable;
- a typed `participant_entries` manifest with owner kind, operation identity, participant digest, COC term/index and entry digest;
- required I, D and C snapshot references and digests in the recovery batch;
- release attestations that bind both request and admission roots and scope generation;
- at least three owner release references before a COC recovery epoch can be recorded completed.

The JSON Schema remains structural. Count-to-array equality, canonical ordering, root calculation, cryptographic signature verification, prefix completeness, cross-owner joins and final owner-local CAS currentness require executable semantic validators and positive/negative interoperability fixtures.

**Current H review target:** `schemas/bmcp.recovery-cutoff-1.0.1.schema.json`. Schema 1.0.0 is superseded for new review.
