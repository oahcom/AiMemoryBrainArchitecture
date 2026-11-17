# Exact-version review input — Storage Archive × Forget × Inventory × Restore v1

- Review target Blob: `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`
- Target commit: `a65973093bb33c7c06ae503f421e096fadb5796b`
- Target path: `reviews/storage-consistency/archive-producer-classification-forget-inventory-restore-atomicity-v1.md`
- Review provenance: Session P coordinator role simulation, not an independent module Owner decision.
- Status: Technical review input only; no interface freeze or implementation approval.

## F — Archive / Recall / local serving lifecycle

**Simulated disposition: ACCEPT WITH ENUMERATED CONDITIONS.** F owns Archive/Recall behavior and local read/disclosure suppression. Storage owns bytes and physical restore serving CAS, not F-local Recall or cache release.

### Findings

1. **MAJOR — identity dimensions (§§3.1, 7).** Separate ArchiveObjectRef, immutable ArchiveRevisionRef, ArchiveManifestRef/digest, locator, capture operation, RecallSessionRef, ReadCursorRef and ReadReceiptRef. A locator is mutable routing metadata, never content identity, authorization or stable deduplication key. Specify idempotent capture and revision replacement rules.

2. **BLOCKER — every disclosure boundary must revalidate (§§3.2–3.3, 5.1, 8 FNC-05..06).** Define checks on cache hit, index result materialization, every Recall page, cursor resume, final handoff/export and downstream delivery. A fence/PermissionEpoch/inventory-seal change must invalidate active cursors and sessions, not merely block future fills. No stale cached page may escape between page validation and delivery.

3. **BLOCKER — mixed and late lineage (§§3.2, 5.1).** F must retain per-fragment/source revision lineage for mixed Archive objects. If an Archive-only item later becomes D-covered, quarantine the object and all derived revisions, invalidate recall cursors/cache/index entries, register/reconcile D lineage, then permit only after current D/I checks. Aggregate manifest lineage must not erase fragment ancestry.

4. **MAJOR — F-local restore release (§6.3).** Define an F-owned receipt bound to RestoreOperationId/generation, store and namespace, object/revision manifest root, cache/index/Working Set generations, RecallSession/ReadCursor invalidation set, rebuild completion and F high-water. Storage SERVING does not imply F Recall is safe.

5. **MAJOR — partial transformation and immutable revision retention (§§3.2, 7).** Define partial transform failure, orphan revisions, abandoned staging, duplicate capture and retention/purge semantics. Staged and orphaned bytes remain non-queryable and discoverable by inventory/Forget until an authoritative terminal disposition.

### Required F-owned closure evidence
- Exact F decision pinned to target Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`.
- Archive identity/revision/manifest/capture state machine and F-local gate semantics.
- Read/Recall validation matrix including cursor and cache races.
- Restore invalidation/rebuild receipt and negative vectors.
- Cross-check against D's late-lineage and I's seal-invalidation contracts.

**Freeze impact:** Conditional blocker until D/I contracts are stable; F's local receipt/schema fields must be agreed before H freezes.
