# Exact-version review input — Storage Archive × Forget × Inventory × Restore v1

- Review target Blob: `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`
- Target commit: `a65973093bb33c7c06ae503f421e096fadb5796b`
- Target path: `reviews/storage-consistency/archive-producer-classification-forget-inventory-restore-atomicity-v1.md`
- Review provenance: Session P coordinator role simulation, not an independent module Owner decision.
- Status: Technical review input only; no interface freeze or implementation approval.

## G — Context / derivatives / snapshots and delivery

**Simulated disposition: NEEDS REVISION.** G owns Context semantic identity, provenance, compaction, snapshot/delta, delivery and G-local restore invalidation. Storage persistence cannot replace G's semantic lineage or current-use decision.

### Findings

1. **BLOCKER — mixed Context provenance (§§3.2–3.3, 4.1).** Define per-fragment provenance for Context assembled from multiple observations, including ContextObservationReference, source EventRef/MemoryRef, revision and the union of all D-covered ancestors. A single aggregate ContextVersion or summary digest cannot erase ancestry needed to suppress one source.

2. **BLOCKER — checks across all G transitions (§§5.1, 6.2–6.3).** Specify D/I currentness checks at context assembly, compaction input selection, ContextVersion publication, snapshot creation, delta application, reuse and delivery. Stale references must remain suppressed even if restored snapshots or deltas reintroduce them. Delta application must reject stale base generation and stale lineage/permission evidence.

3. **MAJOR — G-local restore receipt (§6.3).** Define receipt bound to RestoreOperationId/generation, ContextVersion/TSS high-water, Context lineage reconciliation digest, compaction epoch, invalidated snapshot/delta set and delivery-intent high-water. Storage SERVING is not proof that G Context is safe to reuse.

4. **MAJOR — transitive ancestry and late derivative (§§5.1, 8).** Add races for late derivative discovery after Forget barrier completion, mixed-source Context, queued delivery before restore, compaction racing fence, stale delta replay and cache/snapshot resurrection. D must be able to invalidate all derived Context versions that contain the forgotten ancestor.

5. **MAJOR — ownership split (§2, 7).** Clarify G owns TSS/ContextVersion/compaction/fidelity and delivery semantics; D owns canonical Forget coverage/fence; I owns permission/inventory; F owns Archive/Recall; H owns wire encoding. Storage receipts prove persistence only.

### Required G-owned closure evidence
- Exact G decision pinned to target Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`.
- Typed provenance graph and ContextVersion/compaction/snapshot/delta state machine.
- G-local restore release receipt and currentness rules.
- Negative vectors for mixed-source suppression, late descendant, stale delta, restore replay, queued delivery and compaction/fence race.

**Freeze impact:** Blocking until provenance and currentness semantics are resolved with D/I; H schema cannot freeze before these fields stabilize.
