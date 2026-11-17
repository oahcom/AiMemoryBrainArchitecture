# Phase 3.6.8 — D Exact-Blob Owner Re-Review Decision

- Decision authority represented: D — Memory Brain / Forget Authority
- Review date: 2026-11-17
- Decision: **ACCEPT WITH ENUMERATED MANDATORY AMENDMENTS**
- Reviewed D source Blob: 0668667daeb936bf223ab049277ea2a4117c3b09
- Companion I source Blob: 929b30ba10ac627927d3959e0777b467846b268d
- Storage Design v3.1 Blob: d5bdc72f193fcdaa654e4f07f865b77c578673ca
- COC protocol Blob: 8ac17816476f280ab6fb3afca0688aa03e37de1d
- Prior D Phase 3.6.7 decision Blob: 3603aff5881dd8a375f22aad67b90ade312bbfad
- Scope: D ForgetFence, work admission, lineage/barrier membership, publication terminalization, D outage-Gate release and Forget completion. Architecture semantics only.

## 1. Decision summary

D accepts the Phase 3.6.8 amendment as a substantial and materially correct response to Phase 3.6.7 D-M1..D-M6.

It correctly makes D FenceGeneration enforceable at affected admission and final publication boundaries; fails closed on uncertainty/partition; keeps I as sole authority for global Producer/Recipient/Backup/Export/Restore membership and ProducerDomainInventoryEpoch; binds D work/barrier state to I, COC, Storage and Restore typed references; requires evidence-backed terminalization; separates D outage-Gate release from effective ForgetFence and Global Forget Completion; and invalidates/reopens closure after late pre-fence discovery or post-fence publication violations.

## 2. Mandatory amendments before D semantic freeze

### D36.8-R1 — Align DReconciliationTuple with IReconciliationTuple (BLOCKING)

D-M3 binds I ProducerDomainInventoryEpoch, registry digest, relevant entry generations, IGateGeneration and IRequestHighWater. To match I Phase 3.6.8 and prove the same inventory-currentness boundary, it MUST additionally bind:
- PermissionEpoch and I sequencer position where relevant;
- TargetInventorySealRef/digest and GlobalInventoryCompletenessProof generation/status;
- signer/key-status generation and relevant scope/policy mapping fingerprint;
- stable ReconciliationAttemptRef, attempt generation, tuple schema/version and canonical digest;
- exact I-signed subrecord digest/ref and exact D-signed subrecord digest/ref.

The shared attempt identity is a join envelope over independently signed owner subrecords, not a fictional atomic cross-owner snapshot. Any changed I epoch, target seal, entry generation, D FenceGeneration, barrier root or subrecord digest invalidates the affected attempt and requires a new reconciliation attempt/batch as applicable.

### D36.8-R2 — Make publication-before-fence proof mechanically decidable (BLOCKING)

For every PUBLISHED_BEFORE_FENCE member, bind:
- exact D FenceGeneration and D fence-installation cursor/linearization reference;
- exact generation validated by the final publication/visibility transaction (ValidatedFenceGeneration);
- authoritative publication transaction/commit reference and visibility receipt/pointer digest;
- exact WorkItemRef/AttemptRef/LeaseGeneration, scope and lineage digest;
- proof that the final publication transaction's current-generation comparison and publication mutation shared one atomic/linearizable boundary.

If the publication system cannot prove this ordering, disposition is UNKNOWN and output remains private/quarantined. Wall-clock timestamps or a worker's earlier fence read are insufficient. A post-fence publication remains a safety violation and cannot be converted to success by later high-water advancement.

### D36.8-R3 — Include C provider-side-effect outcome in applicable barrier members (BLOCKING)

For a D barrier member that crossed C's provider/runtime side-effect boundary, terminalization/reconciliation MUST include C's authoritative CSubmitOutcomeRef and digest, provider idempotency-key namespace, exact request digest and provider receipt/lookup evidence where available.

C outcome remains C-owned. Storage COMMITTED/ROLLED_BACK, I terminality, COC participant state or transport ACK cannot synthesize C provider success/rejection. UNKNOWN provider outcome remains a blocking D barrier member. If no provider invocation was permitted, bind authoritative proof of non-invocation rather than infer it from a missing COC row.

### D36.8-R4 — Revalidate I global inventory currentness at every D release/completion boundary (BLOCKING)

D-M2 requires current I evidence before barrier closure or D outage-Gate release. Strengthen the release/completion predicate to bind the exact current TargetInventorySeal and GlobalInventoryCompletenessProof generation/status where applicable, and repeat I currentness validation immediately before D outage release and D Forget terminalization.

If ProducerDomainInventoryEpoch, registry digest, relevant InventoryEntryGeneration, TargetInventorySeal or scope mapping advances/changes, D must determine whether omitted producer/work/lineage exists; absent positive proof, reopen the affected barrier and remain closed. D cannot treat stale I proof as current merely because D-local FenceGeneration is unchanged.

## 3. Clause-by-clause disposition

| Clause | D disposition |
|---|---|
| §1 authority and typed values | ACCEPT |
| §2 D-M1 enforceable fencing | ACCEPT WITH R2 |
| §3 D-M2 I registry projection/currentness | ACCEPT WITH R1/R4 |
| §4 D-M3 typed reconciliation tuple | ACCEPT WITH R1 |
| §5 D-M4 terminalization | ACCEPT WITH R2/R3 |
| §6 D-M5 outage release vs Forget completion | ACCEPT |
| §7 D-M6 late discovery/post-fence safety | ACCEPT |
| §8 D release algorithm | ACCEPT WITH R1/R3/R4 |
| §9 conformance cases | ACCEPT AS SPECIFIED; NOT EXECUTED |

## 4. D invariants reaffirmed

1. Only D owns ForgetOperation semantics, FenceGeneration, affected WorkItem admission, lineage/barrier membership, D terminalization and D outage-Gate release.
2. I alone owns global membership and inventory epoch; D consumes and validates I-signed current projections.
3. A D fence close is a durable D-local linearization point, but every external boundary must enforce the current generation at its final effect transaction.
4. Every barrier member has source-backed terminal proof; missing ACK, empty queue, absent worker, expired lease or missing COC record is not proof.
5. D outage-Gate release is OUTAGE_ADMISSION_RELEASE_ONLY; it never clears an effective Forget Fence.
6. Forget completion and Global Forget Completion are separate transitions with separate evidence.
7. UNKNOWN, late discovery, stale restore, post-fence publication or unresolved provider side effect keeps the relevant barrier closed.

## 5. Final D decision

**ACCEPT WITH ENUMERATED MANDATORY AMENDMENTS D36.8-R1..R4.**

The exact D Phase 3.6.8 Blob is accepted as the correct owner-local semantic direction, but is **not semantically frozen** until a new immutable D amendment addresses R1–R4 and is re-reviewed by exact Blob. This decision does not approve the joint I/D/Storage/COC bundle, does not claim implementation/conformance, physical erasure, Global Forget Completion, deployment or production activation.

## 6. Provenance

This is a delegated role-based architectural review and decision record prepared in this ChatGPT session at the user's direction. It is not a cryptographic signature and does not prove independent human D Owner authorship or approval.
