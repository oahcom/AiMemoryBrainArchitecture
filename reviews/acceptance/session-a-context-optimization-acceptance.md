# D — Formal Cross-Owner Acceptance of A Context Optimization & Observation Archive

- Owner: D — Memory Brain Architect
- Decision: ACCEPT WITH CONDITIONS
- Date: 2026-11-17
- Branch: session-d-memory-brain-2026-11-16
- Last HEAD explicitly recorded by A: 9dd48eddb3c8f91d15dfa6981a7f53cc70bd4bf8. Branch name verified; current tip SHA is not exposed by the branch-search operation, so this is the last evidenced snapshot, not a fresh HEAD assertion.
- D baseline: 03-memory-brain/forget-fence-and-completion-contract.md Blob 1f0391bc49d007c44ec74165bd33d37412cc7990; 03-memory-brain/forget-fence-operation-and-publication-gate.md Blob 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5.
- A exact reviewed files: A branch session-a-integration-2026-11-16; commit 6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f. Files and Blob SHAs: system integration review b53db1ecb7830a7f1057d09c8ef73aceab942cea; contract candidates 55257bdf85a56a78df96b797b063bc49d91f5a6d; conformance plan 1c941c3e55be1e539a76ef89f297c168296c7db2; decision register 36581cf286ddf2516f571eb823fddc9cf8707d80.

## Scope and formal decision
D accepts the conceptual ownership split and canonical-domain invariants in the exact A package. This is not acceptance of F/G wire schemas, Storage atomicity, I governance policy, interface freeze, implementation or conformance.

D exclusively owns Canonical Memory identity/lifecycle, ForgetOperation, ForgetFence generation/cursor, canonical dependency inventory, producer registration/barrier and canonical suppression proof. F owns Archive bytes/manifests/revisions/locators, recall sessions/cursors/receipts/budgets/completeness/cache. G owns Context membership/selection, ContextObservationReference, TSS projection, ContextVersion, compaction, fidelity/lineage/loss, reconciliation and delivery intent. I owns Principal/Scope/PermissionEpoch, retention, revocation, target inventory and global completion. E owns canonical-derived publication; Storage owns physical durability/recovery.

Archive-only transient observations are not automatically Canonical Memory or D producer targets. However, every F/G producer class that processes D-covered canonical lineage or emits a D-covered derivative must register work/dependencies before execution or visibility and recheck the latest applicable fence at the final publication/disclosure boundary. A new Memory ID, summary, cache, index, snapshot or delta cannot evade ancestor lineage.

Forget Fence is authoritative only in D's namespace. F/G must fail closed if current fence or lineage cannot be established. Local tombstone, stale fence token, ReadReceipt, IndexWatermark or ContextVersion cannot replace it. D's CanonicalSuppressionComplete is not I global Forget completion or physical erasure.

## Cross-owner review
| Pair | Binding decision / unresolved point |
|---|---|
|D↔F|D owns canonical Forget/fence/barrier; F owns runtime Archive. F work over D-covered lineage registers and checks final fence. Archive-only observations are not automatically canonical.|
|D↔G|G owns Context/TSS/version; D owns canonical truth/Forget. D-covered G derivatives require registration and transitive fence.|
|D↔I|D owns canonical suppression facts; I owns authorization, PermissionEpoch, retention, inventory seal and global completion. Neither substitutes for the other.|
|F↔G|F owns locator/session/cursor/receipt/completeness; G owns Context ref/selection/version. Receipt is not acceptance or Applied; cursor cannot cross ContextVersion.|
|F↔I|I authorizes; F enforces at lookup/page/cache/fill/final handoff. F cannot set retention or global Forget.|
|G↔I|G owns Context/compaction/delivery; I owns policy. Revalidate at commit/delivery; unknown epoch blocks.|

No executable atomic cross-owner visibility gate joining D fence, I authorization, F archive and G Context is evidenced.

Unresolved classification conflict: the complete F producer and G derivative inventory must distinguish runtime-only observations, D-covered derivatives and external/backup copies. Neither blanket D ownership of all Archive bytes nor blanket exclusion of all Archive-derived objects from D lineage is accepted.

## P0 / P1
P0:
- No executable Forget × Capture/Recall/Cache/Compaction/Delivery proof.
- No Archive Restore/PITR proof that D fence survives data rollback and is read before queryability.
- No proven D registration/fence/visibility linearization with Storage and I final authorization.
- Unknown producer, missing lineage, WAL gap, stale fence or indeterminate terminal state must quarantine.

P1:
- F producer-class and G derivative inventory not fully accepted.
- F/G/B/H exact receipt/cursor/reference schemas not frozen.
- D/E/F/G/I recovery receipt and final-gate mapping remains design-level.

## Required negative verification
| # | Scenario / required outcome | Evidence | Status / owner |
|---|---|---|---|
|1|Forget then Archive Restore: quarantine until independent current D fence and I policy state verified|restore ID, snapshot/WAL coverage, fence/epoch readback, release receipt|NOT RUN; Storage+D/I/F|
|2|Forget then PITR: no rollback of fence/permission; missing control prefix stays RESTORE_FENCED|PITR cutoff, WAL continuity, independent high-water|NOT RUN; Storage+D/I|
|3|WAL missing/corrupt/incomplete: no partial state queryable|segment manifest, gap finding, quarantine evidence|NOT RUN; Storage|
|4|Fence recovery fails then Recall: fail closed, no bytes/page/receipt disclosed|authority failure and denied recall trace|NOT RUN; D/F/I|
|5|Old cache refilled after Forget: reject fill and hit|lineage, fill gate, hit denial, fence generation|NOT RUN; F+D|
|6|Offline reconnect replays old data: fresh auth/fence, suppress before restore; otherwise block|session, epochs, fence, replay rejection, ACK|NOT RUN; H+I/D/G|
|7|Old ReadCursor across ContextVersion: reject; new authorized session|versions, session/cursor binding, rejection|NOT RUN; F+G|
|8|Source Revision changes: old Reference becomes STALE, no silent float|old/new revision/hash, stale result, new G version|NOT RUN; F+G|
|9|Compaction loses critical evidence: veto/abort, prior version preserved|fidelity report, loss ledger, source anchors, unchanged head|NOT RUN; G+B/D/F|
|10|Unauthorized Principal reads Archive: deny without existence leakage|authenticated principal, scope/action/resource, I decision|NOT RUN; I+F|
|11|Revoked Principal uses old authorization: stale epoch denied at page/cache/handoff|old/new epoch and denial trace|NOT RUN; I+F/G/H|
|12|Derived Summary re-enters after Forget: ancestor fence blocks registration/publication|lineage, work ID, fence and quarantine receipt|NOT RUN; D+G/F/E|
|13|Restore permission/Forget mismatch: remain quarantined|D fence, I epoch/seal, restore mismatch|NOT RUN; Storage+D/I|
|14|Capture races Forget: one serialization order; pre-fence work in barrier, fence-first denied|registration sequence, fence cutoff, visibility decision|NOT RUN; F+D+Storage|
|15|Recall races Forget: fence-first blocks pages/final serialization; historical first disclosure does not authorize later reads|per-page checks, causal order, cancel/discard evidence|NOT RUN; F+D/I+Storage|

All 15 cases are NOT RUN. A conformance plan is not execution evidence. D owns fence/barrier predicates; F owns Archive races; G owns Context/compaction; I owns policy/inventory; Storage owns WAL/PITR and physical recovery. E/H/C provide publication, reconnect and final-boundary evidence.

## Dependencies and gate
F: stable work IDs, lineage, cache/index and final read/capture gate.
G: transitive TSS/compaction lineage, tombstone-before-rebuild, stale Snapshot/Delta rejection.
I: PermissionEpoch, ProducerDomainInventoryEpoch, TargetInventorySeal, retention and exceptions.
E: derived registration/publication and replay exclusion.
H/C: reconnect, final request boundary and distinct Applied/Forget evidence.
Storage: linearizable registration/fence/publication and restore quarantine.

Interface freeze: NOT AUTHORIZED. Implementation: NOT AUTHORIZED. P0 remains open.

**Final D decision: ACCEPT WITH CONDITIONS**, limited to the ownership split, canonical-vs-runtime boundary, transitive Forget requirements and typed-object separation.