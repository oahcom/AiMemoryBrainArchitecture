# Module F — Memory Runtime & Retrieval Baseline & Redlines

- Proposal: F-MBR-0.1.0
- Status: **PROPOSED — prepared by Session P for F Owner review/adoption; NOT an F Owner decision**
- Intended Owner: F — Memory Runtime
- Source branch / HEAD: `session-f-memory-runtime` @ `6cdc23f0835ea9576867f7cd1ac145e57f598c4b`
- Evidence: `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md` blob `99f950f9fabe97969b5ad580c9c80e52930a1423`; `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` blob `ce59252dbbdc5d10d016704797e9ba12d5a941bd`; `05-memory-runtime/retrieval-engine.md` blob `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af`
- Project PB/PR: P proposal v0.1.0 only, not approved/active.

## 1. Module Mission
Return authorized, current, evidence-bearing Memory candidates while maintaining suppression, freshness and isolation across indexes, caches, Working Sets and in-flight retrieval.

## 2. Ownership Baseline
F owns retrieval planning/execution, candidate generation/fusion/ranking, freshness/completeness reporting, index projections, IndexWatermark, caches and Working Sets, cancellation and runtime-local suppression evidence. D owns canonical truth/fence; E owns compiler publication; I owns authorization; G owns Context.

## 3. Capability Baseline
Scope-before-candidate filtering; canonical revalidation; hybrid retrieval and provenance-aware ranking; per-index/partition watermark tracking; final disclosure-boundary reauthorization; forget suppression and invalidation; rebuild/replay safety; fail-closed stale/unknown handling.

## 4. Domain Ownership
F's index/cache/working-set state is a projection, never canonical truth. F cannot mutate D canonical memory, E compiler lifecycle, G ContextVersion/Applied, H wire/Adapter ACK or I permission/global completion.

## 5. Interface Baseline
Consume D CanonicalCommitCursor, LifecycleEventCursor and ForgetFence; F emits IndexWatermark per index/partition with contiguous accounted-through cursor plus coverage/schema versions. These tokens are not interchangeable. F returns completeness, omissions, freshness, policy/fence snapshot and local evidence.

## 6. Security Baseline
Authorization and Scope filtering occur before candidate emission, fusion, reranking, counts, traces or cache access that could leak protected existence. Revalidate I permission and D fence immediately before final return/handoff. Unknown/stale/gapped authority state fails closed.

## 7. Module Redlines
- F-PR-01 No index/cache/Working Set may override D canonical state. CRITICAL.
- F-PR-02 No protected candidate may be emitted before Scope/permission filtering. CRITICAL.
- F-PR-03 No stale/gapped watermark may be treated as complete coverage or Forget proof. HIGH.
- F-PR-04 No rebuild/backfill/replay/cache warming may resurrect forgotten sources/derivatives. CRITICAL.
- F-PR-05 No F-local suppression may be represented as G Applied, H Adapter purge or I global completion. CRITICAL.

## 8. Forbidden Cross-module Actions
No canonical writes; no compiler publication; no Context mutation; no wire ACK manufacture; no authorization policy or global Forget completion decision.

## 9. Dependency Contracts
D canonical cursors/fence; E committed/registered projections; I authorization/PermissionEpoch/revocation; G Context membership boundaries; H Adapter protocol only where required. Cursor mapping and API/backend cancellation conformance remain OPEN/TO_VALIDATE.

## 10. Conformance Requirements
Scope leakage through counts/traces; stale cache; in-flight cancellation; fence race at final return; watermark gaps; rebuild/replay resurrection; partition loss; authorization revocation; incomplete retrieval disclosure; latency/benchmark evidence.

## 11. Acceptance Criteria
F Owner accepts exact proposal; D/E/I cursor and fence interfaces accepted; final suppression tested at every disclosure boundary; race/fault and performance tests reproducible; F evidence stays local and correctly scoped.

## 12. Change Authority
F Owner decides retrieval/runtime internals; D/E/I/G decide upstream semantics; cross-module token/interface changes require affected Owners.

## 13. Open Decisions
Concrete API binding for cursor/fence; backend cancellation and in-flight finalization; watermark coverage semantics and persistence; consumer conformance tests; performance budgets.

## 14. Explicit Non-Claims
No runtime implementation, backend race/cancellation proof, benchmark pass, G Applied or global Forget completion claim.
