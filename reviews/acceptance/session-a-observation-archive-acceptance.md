# F — Formal Cross-Owner Acceptance of Observation Archive & Recall

- Owner: F — Memory Runtime Architect
- Decision: ACCEPT WITH CONDITIONS
- Date: 2026-11-17
- Branch: session-f-memory-runtime
- Last HEAD explicitly recorded by A: 714fe628fdcfe62b5e6ea901810b779c58ddddb3. Branch name verified; current tip SHA is not exposed by branch search, so this is the last evidenced snapshot.
- F research Blob: cea136cbfba6629c8b04bce4855febb1c988161c.
- F candidate contract Blob: 0b5c5b02c5b318c79606328ef1c22d686b8fc8b3.
- A exact reviewed files: A branch session-a-integration-2026-11-16; commit 6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f. Files and Blob SHAs: system integration review b53db1ecb7830a7f1057d09c8ef73aceab942cea; contract candidates 55257bdf85a56a78df96b797b063bc49d91f5a6d; conformance plan 1c941c3e55be1e539a76ef89f297c168296c7db2; decision register 36581cf286ddf2516f571eb823fddc9cf8707d80.

## Scope and formal decision
F accepts the F-owned Archive capability boundary and separation from G Context, conditionally. No wire/API schema, topology, retention policy, I authorization, production readiness or implementation is approved.

F owns immutable observation bytes/revisions, hash/source-revision binding, ArchiveObjectManifest, ArchiveLocator, metadata catalog, exact bounded reads, RecallSession, ReadCursor, ReadReceipt, ReadBudget, completeness/freshness, cache/Working Set, integrity and F-local suppression. F does not own Principal/Permission, PermissionEpoch, retention policy, Forget authority, canonical publication, Context selection/versioning, TSS, compaction or Applied proof.

## Recall contract conditions
1. ArchiveLocator and G ContextObservationReference are different typed objects. Context ref pins exact locator, object revision/hash/range, lineage and optional receipt; it is not a bearer capability.
2. ReadReceipt proves only the exact range/bytes returned by F under a particular permission and Forget checkpoint. It does not prove semantic truth, G acceptance, Context commit, delivery, Adapter application or future read permission.
3. ReadCursor binds one RecallSession, object/revision/hash, selector and coordinate system. Reject reuse across session, principal/scope, revision, permission/fence change and ContextVersion. A new ContextVersion requires a new authorized RecallSession.
4. ReadBudget is not a grant. COMPLETE requires a fully executed bounded selector, integrity-verified bytes and no known omission. Timeout, budget exhaustion, index lag, partial page or missing channel is PARTIAL/DEGRADED/UNKNOWN, never COMPLETE.
5. Revision drift becomes STALE; hash mismatch/truncation/corrupt page map quarantines. No silent locator float.
6. F summaries/previews are non-canonical, lineage-bound derivatives and cannot upgrade epistemic status. Locator-only output is not injected evidence.
7. Recheck I authorization and D fence at lookup, each page/cursor continuation, cache hit, cache-fill publication and final F→G handoff.
8. Capture requires stable work identity, immutable publication, orphan handling, manifest/receipt idempotency and a final fence gate.

## Restore/PITR boundary
After Restore/PITR, F remains RESTORE_FENCED/QUARANTINED until Storage verifies data/WAL continuity, D authoritative fence/lineage high-water is read independently of the restored snapshot, I current PermissionEpoch/revocation and inventory seal are validated, and stale indexes/caches/sessions/cursors are invalidated or rebuilt. If any authority, WAL prefix, inventory or lineage is missing/unknown/corrupt, Recall, Cache Fill, index publication and locator dereference remain closed. The data snapshot cannot roll back the independent control ledger.

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

F returns factual recall result and completeness; G decides selection and Context commit. F cannot mark Context accepted or Applied.

## P0 / P1
P0: Restore/PITR quarantine and independent D/I replay unproven; Forget × Capture/Recall/Cache lacks executable proof; final disclosure gate is not shown atomically ordered with D fence and I revocation; corrupt/incomplete WAL has no executed negative evidence.
P1: RecallIntent/session/cursor/receipt/budget/completeness schemas not frozen; F catalog vs E index needs D/E/I acceptance; cache freshness/offline semantics need I/H; retention/expiry/deletion remain I-owned.

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

All 15 cases are NOT RUN. A's conformance plan is PROPOSED / NOT RUN and F's candidate interface is NOT_IMPLEMENTED.

## Dependencies and gate
D: fence/lineage, producer registration and final gate. I: authenticated identity/scope, current epoch, retention/revocation. G: Context ref/version invalidation. B/H: typed refs, authenticated Recall envelope and reconnect. Storage: immutable durability, WAL/PITR and quarantine. E: metadata/index namespace separation.

Interface freeze: NOT AUTHORIZED. Implementation: NOT AUTHORIZED.

**Final F decision: ACCEPT WITH CONDITIONS** for Archive lifecycle, bounded Recall, integrity/completeness, cursor/receipt semantics and F/G separation.