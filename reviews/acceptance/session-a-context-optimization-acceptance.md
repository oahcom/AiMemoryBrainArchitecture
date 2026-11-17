# G — Formal Cross-Owner Acceptance of Context Optimization

- Owner: G — Memory Context Architect
- Decision: ACCEPT WITH CONDITIONS
- Date: 2026-11-17
- Branch: session-g-memory-context
- Last HEAD explicitly recorded by A: 72a8066b4401f9586fe10775d545384b82736f07. Branch name verified; current tip SHA is not exposed by branch search, so this is the last evidenced snapshot.
- G research Blob: 3fb9f011e24c93a748442018d48c5954584e4f43.
- G candidate register Blob: eadefd4e0fe541ef8479a030a2a99a0d57dbcf8b.
- A exact reviewed files: A branch session-a-integration-2026-11-16; commit 6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f. Files and Blob SHAs: system integration review b53db1ecb7830a7f1057d09c8ef73aceab942cea; contract candidates 55257bdf85a56a78df96b797b063bc49d91f5a6d; conformance plan 1c941c3e55be1e539a76ef89f297c168296c7db2; decision register 36581cf286ddf2516f571eb823fddc9cf8707d80.

## Scope and formal decision
G accepts the G-owned Context boundary and proposed direction of selective recall, task-state projection, boundary-triggered compaction and evidence lineage, conditionally. G's candidate register remains PROPOSED/OPEN; no baseline change, interface freeze, implementation or benchmark result is implied.

G owns Context membership/selection, ContextObservationReference, TSS as Context projection, ContextVersion, ChangeSet/Snapshot/Delta reconciliation, compaction, fidelity validation, lineage/loss accounting and delivery intent. F owns raw Archive lifecycle, locator, recall sessions/cursors/receipts/budgets/completeness/cache. D owns Canonical Memory and ForgetFence. I owns identity, permission, retention and global inventory. H/C own transport and final request/application evidence.

ContextObservationReference is a G-owned edge binding an F locator to exact object revision/hash/range, source lineage, Scope and optional receipt. It is not the Archive object or an authorization token. G cannot mutate F Archive lifecycle; F cannot select or commit Context.

TSS is a typed/versioned task projection: goal, completion criteria, progress, verified outcomes, unresolved work, constraints, decisions, uncertainty, next action and source refs. It is not Canonical Memory, Agent private state or CoT. Reported remains Reported; Inferred remains Inferred; Verified requires B/D/E evidence rules.

## Research transfer, applicability and cost
- You don't need long context motivates separating retained history from active context and selective reading. Its benchmarks do not prove our private archive, multi-scope authorization, Forget or retrieval completeness.
- SoL-Pi ObservationPack is a useful immutable-source/handle/paged-recall pattern. Its local filesystem, session-derived paths and host-process trust model do not meet our policy/restore requirements as-is.
- Evidence-Preserving Reducer quote/hash checks are necessary for excerpts, not semantic completeness, representativeness, freshness, counterexample retention, authorization or epistemic correctness. Preserve original fallback where policy permits.
- Online Context Compact makes boundaries reevaluation opportunities, not unconditional compaction. Economics require project measurements of request/cache read-write, remaining horizon, compaction/retry/validation, Archive recall/recovery, latency and omission risk. Do not adopt SoL-Pi thresholds or cache ratio.
- SAC is an independent stress condition for suitable task classes, not default. Action Fusion is outside G.

Every compaction preserves prior committed ContextVersion until candidate passes hard fidelity vetoes and CAS; records source membership/revision/hash, transitive lineage, immutable decision/fidelity/loss ledger; preserves rare negative constraints, temporal order, epistemic status, conflicts, provenance and Scope/Permission/Forget; and revalidates D/I immediately before publication/delivery. Do not retain forgotten plaintext for audit. No numeric threshold or savings claim is accepted without paired held-out evidence.

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

F completeness and G semantic sufficiency are distinct. F COMPLETE means bounded read coverage was executed; it does not prove task-relevant evidence sufficiency. G cannot reinterpret PARTIAL/STALE/SUPPRESSED as complete.

## P0 / P1
P0: no executable Forget × compaction/Context CAS/delivery proof; Restore/PITR may resurrect stale Context refs unless D/I state is independently recovered first; no proof forgotten ancestors cannot re-enter TSS/summary/Loss Ledger/Snapshot/Delta.
P1: TSS and Context ref fields need B/C/D/F/I/H; fidelity hard vetoes and loss retention need agreement; cost model lacks telemetry and held-out evaluation; delivery intent is not Applied.

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

All 15 cases are NOT RUN. G candidates remain PROPOSED/OPEN/NEEDS_CROSS_OWNER_APPROVAL.

## Dependencies and gate
F: exact revision-pinned recall and completeness. D/E/Storage: derivative registration, Forget barrier and atomic gate. I: policy, epoch, retention, inventory and restore controls. B: typed refs and epistemic/temporal semantics. C/H: boundary telemetry and Applied evidence.

Interface freeze: NOT AUTHORIZED. Implementation: NOT AUTHORIZED.

**Final G decision: ACCEPT WITH CONDITIONS** for Context ownership, non-canonical TSS, distinct ContextObservationReference, versioned compaction and evidence lineage.

## Decision provenance clarification — 2026-11-18

This acceptance record is a delegated G-role decision prepared centrally under the user's instruction. It is not an independent human Owner signature. The recorded source pin `72a8066b4401f9586fe10775d545384b82736f07` is the last explicitly evidenced G branch HEAD in the source record, not a verified current branch tip. This acceptance is limited to the G-owned Context optimization boundary, remains conditional, and does not authorize interface freeze, implementation, benchmark claims, global Forget completion or cross-owner production acceptance.
