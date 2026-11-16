# I — Formal Cross-Owner Security & Governance Acceptance

- Owner: I — Security & Governance Architect
- Decision: ACCEPT WITH CONDITIONS
- Date: 2026-11-17
- Branch: session-i-security-governance-2026-11-16
- Current I HEAD surfaced by Issue #4: 8d1ddadb6af70a7c387105d20ca8f2f6de80c5fb, newer than A discovery snapshot 1fc3b3293ebf2077edfd6ad253647d382173d9fa.
- I technical baseline Blob: 0cbf6bb7480db873790c454817593a9b1c5548ba.
- I global inventory contract Blob: 9100061fa986fb6676656169de3fcf9fc1c72664.
- I governance register Blob: 3718ae8b24940ff655a2652e908996635709c1ad.
- A exact reviewed files: A branch session-a-integration-2026-11-16; commit 6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f. Files and Blob SHAs: system integration review b53db1ecb7830a7f1057d09c8ef73aceab942cea; contract candidates 55257bdf85a56a78df96b797b063bc49d91f5a6d; conformance plan 1c941c3e55be1e539a76ef89f297c168296c7db2; decision register 36581cf286ddf2516f571eb823fddc9cf8707d80.

## Scope and formal decision
I accepts A's security architecture constraints conditionally. This is an I Owner architecture decision only. It is not external governance approval, production security certification, implementation or interface freeze.

I is the logical authority for issuer trust, Principal/Actor/Producer registration, delegation, authorization, PermissionEpoch, revocation, retention, target inventory seal, exceptions and global Forget evaluation. D owns ForgetFence and canonical suppression. PermissionEpoch and ForgetFence are independent typed authorities. Locator, cursor, receipt, ContextVersion, index watermark, cached ALLOW or caller-supplied scope/identity are not authorization.

Protected operations include Archive capture/read, cache hit/fill, Context commit, compaction publication, delivery, reconnect and final request submission. Each owner enforces its own boundary using current I policy and applicable D fence.

## Security and Restore/PITR gate
Restore is quarantine-only. Before any restored Archive/Context/index/cache is queryable:
1. Verify data integrity and WAL/archive continuity; missing/corrupt/incomplete prefix means RESTORE_FENCED.
2. Read authoritative D ForgetFence and lineage high-water from a control source not rolled back with data.
3. Read authoritative I PermissionEpoch/revocation and current ProducerDomainInventoryEpoch/TargetInventorySeal independently.
4. Reconcile newly discovered producers, recipients, replicas and restore destinations; invalidate stale inventory seals.
5. Invalidate/rebuild F caches/indexes/sessions/cursors and G Context refs/snapshots/deltas.
6. Release quarantine only after required owner receipts and complete coverage.
No local permission check alone closes end-to-end Forget. No offline lease, stale-epoch grace or cached ALLOW without currentness proof is accepted under the inspected Phase 3.6 baseline.

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

I rejects any interpretation that F suppression or G tombstone alone equals global Forget completion. D CanonicalSuppressionComplete is a D-domain result. I global completion requires sealed inventory, D barrier, E/F/G/H evidence, backup/restore and external recipient obligations, and required physical-erasure evidence or valid policy exception.

## P0 / P1
P0: no executable Forget × Restore/PITR × permission recovery proof; no proof control state is independent of restored snapshot and checked before Recall/Cache Fill; global inventory contract remains CANDIDATE with governance approval missing; JF-10 remains P0 OPEN.
P1: Archive classification/retention/data residency/external recipients need effective policy; revocation currentness and consumer receipt mapping need exact F/G/H acceptance; seal completeness and late-discovery tests NOT RUN; reconnect must block stale local snapshots/queues.

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

All 15 cases are NOT RUN. I's Phase 3.6 technical baseline is JOINT-DECIDED but GOVERNANCE-BLOCKED; global inventory contract is CANDIDATE; governance register has no effective named approvals. This decision does not change those statuses.

## Dependencies and gate
D: authoritative fence/lineage/barrier. F/G: local enforcement and target evidence. H/C: authenticated transport, Adapter ACK and final request boundary. Storage: restore quarantine and WAL/control-ledger readback. E: producer/derived registration and replay controls.

Interface freeze: NOT AUTHORIZED. Implementation: NOT AUTHORIZED. Security approval: NOT GRANTED.

**Final I decision: ACCEPT WITH CONDITIONS** for I-owned authorization, PermissionEpoch, inventory, revocation, retention and restore-gating boundaries.