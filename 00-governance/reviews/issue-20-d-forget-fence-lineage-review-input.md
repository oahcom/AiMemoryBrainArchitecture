# Exact-version review input — Storage Archive × Forget × Inventory × Restore v1

- Review target Blob: `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`
- Target commit: `a65973093bb33c7c06ae503f421e096fadb5796b`
- Target path: `reviews/storage-consistency/archive-producer-classification-forget-inventory-restore-atomicity-v1.md`
- Review provenance: Session P coordinator role simulation, not an independent module Owner decision.
- Status: Technical review input only; no interface freeze or implementation approval.

## D — Forget Fence / canonical lineage

**Simulated disposition: NEEDS REVISION.** D owns canonical ForgetFence semantics, work admission, dependency closure, barrier completion and reopen; Storage may provide persistence/atomicity but cannot define these semantics.

### Findings

1. **BLOCKER — late lineage discovery after Archive-only classification (§§3.2–3.3, 5.1).** The proposal says an Archive-only observation may later be linked to EventRef/MemoryRef and must then be quarantined/reclassified. It does not define a normative transition protocol when the related Forget barrier has already terminalized. Require a D-owned retroactive lineage event binding object/revision and every derivative, original EventRef/source ancestry, current ForgetFenceGeneration, and barrier reopen/invalidation. All read/export/cache/index/delivery paths must be suppressed before reclassification is acknowledged. A terminal historical barrier cannot be silently rewritten; a new reconciliation epoch/barrier or equivalent D-authorized reopen record is required.

2. **BLOCKER — D registration/fence linearization (§§4.2, 5.2–5.3).** “Exactly one serialization order” is not an implementation-neutral contract. D must define the owner-local serialization primitive, inclusive/exclusive high-water semantics, generation increment, request idempotency/digest conflict, and the exact point where registration becomes admitted. Every registration racing fence installation must be included at or below the captured cutoff, or rejected/quarantined above it. No third state or unaccounted gap.

3. **BLOCKER — retries, leases, DLQ and late attempts (§§5.1, 8 FNC-03..06).** A ProducerWorkItemId alone does not close execution attempts. D must model attempt/lease identity, lease generation, worker handoff, retry/DLQ/replay authorization, terminal attempt proof and late attempt suppression. Barrier completion requires no executable lease/replay path capable of producing a derivative. Any post-terminal descendant discovery must invalidate/reopen the barrier and propagate to all descendants.

4. **MAJOR — dependency closure evidence (§§5.1, 7).** DProducerWorkRegistrationReceipt and DependencyRegistrationReceipt need D-owned normative semantics: source/ancestor snapshot version, canonical dependency set/order/digest, D registry version, captured high-water, observed fence generation, completeness/unknown-lineage treatment and terminal outcome. Storage durability receipts are not substitutes for D lineage proofs.

5. **MAJOR — visibility predicate (§§5.1–5.3).** Define D's exact final predicate for each publication/disclosure boundary and how one-time D authorization is consumed atomically with the visibility transition. A staged object must remain non-addressable through every alternate read path until D's final decision is consumed.

### Required D-owned closure evidence
- Exact D contract revision and append-only decision pinned to target Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`.
- Formal state machine for ProducerWorkItem / Attempt / Dependency / Barrier / LateLineage.
- Boundary semantics for registration-vs-fence and terminalization-vs-late-derivative races.
- Positive and negative vectors: pre-fence admitted; fence-first rejected; lost admission ACK; retry after lease expiry; DLQ replay; late descendant after terminal barrier; mixed lineage; incomplete dependency root; duplicate and conflicting request digest.

**Freeze impact:** Blocking. D's semantics must precede F/E/G implementation contracts and H schema finalization.
