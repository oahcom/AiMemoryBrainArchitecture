# Module D — Canonical Memory Brain Baseline & Redlines

- Proposal: D-MBR-0.1.0
- Status: **PROPOSED — prepared by Session P for D Owner review/adoption; NOT a D Owner decision**
- Intended Owner: D — Memory Brain
- Source branch / HEAD: `session-d-memory-brain-2026-11-16` @ `edf35b8a80bb9d096748dab129cea5867561b5d3`
- Evidence: `03-memory-brain/forget-fence-and-completion-contract.md` blob `1f0391bc49d007c44ec74165bd33d37412cc7990`; `03-memory-brain/commit-cursor-semantics.md` blob `4688a0ca487bf4d853c7f0220408abe8d743d159`; `03-memory-brain/phase-3.6.2-jf10-cross-authority-recovery-protocol.md` blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`
- Project PB/PR: P proposal v0.1.0 only, not approved/active.

## 1. Module Mission
Maintain authoritative canonical Memory identities, revisions, lifecycle and ForgetFence state, providing stable, ordered canonical truth to downstream projections and consumers.

## 2. Ownership Baseline
D owns canonical Memory domain state, canonical commit ordering, ForgetOperation identity/state, ForgetFence generation/cursor, canonical dependency inventory, producer registration/barrier semantics and canonical-domain suppression proof. I owns global completion/retention/authorization policy; Storage owns durable physical transaction/visibility realization; E owns compiler work lifecycle; F/G/H own their consumer/runtime boundaries.

## 3. Capability Baseline
Support canonical writes/revisions/lifecycle, immutable history, typed cursors, target capture, monotonic fence, producer admission/registration barrier, canonical visibility checks and recoverable operation status. Ambiguous authority or barrier state must fail closed.

## 4. Domain Ownership
D owns canonical memory and Forget semantic objects; not compiler queue/lease state (E), index/cache state (F), ContextVersion (G), Adapter state/ACK (H), Principal/Permission/retention/global completion (I), or storage engine implementation.

## 5. Interface Baseline
One globally ordered CanonicalCommitCursor per Brain authority; independent aggregate revisions and lifecycle cursors. ForgetFenceCursor identifies exact operation/generation/target set and is not interchangeable with commit cursor or F IndexWatermark. D producer barrier and final publication gate must preserve ordering with I authorization and Storage visibility pointer.

## 6. Security Baseline
D operations require authenticated I policy decision and typed B references; payload IDs are not authority. D may declare canonical-domain suppression only; cannot claim external recipient, backup, Adapter, global or physical erasure.

## 7. Module Redlines
- D-PR-01 No canonical mutation outside D-authorized write path. CRITICAL.
- D-PR-02 No reuse/conflation of CanonicalCommitCursor, LifecycleEventCursor, IndexWatermark and ForgetFenceCursor. CRITICAL.
- D-PR-03 No late producer/derivative publication after fence/barrier closure. CRITICAL.
- D-PR-04 No Forgotten/global completion claim without I-owned criterion and required evidence. CRITICAL.
- D-PR-05 No timeout/absence inference as commit or non-commit; recovery must consult authoritative sequencer and durable visibility. CRITICAL.

## 8. Forbidden Cross-module Actions
D must not implement E queue lifecycle, F index/cache invalidation, G Context mutation, H Adapter protocol, I permission/revocation/global completion policy or Storage internals by undocumented assumption.

## 9. Dependency Contracts
D/E/Storage JF-10 cross-authority recovery remains candidate/open until I accepts sequencer interface and crash/recovery tests pass. Consumers E/F/G require typed cursor and fence mapping. I defines global completion and external/backup residual policy.

## 10. Conformance Requirements
Monotonic fence; late producer rejection; producer registration vs barrier race; publication vs revocation ordering; commit-won/storage-not-visible and storage-visible/ACK-lost recovery; cursor monotonicity; replay/idempotency; restart and crash injection; no false Forgotten/global claims.

## 11. Acceptance Criteria
D Owner accepts exact proposal; canonical semantics and interfaces versioned; I and Storage accept JF-10 authority handoff; E/F/G consumers accept cursor/fence mapping; executable recovery and race tests pass before implementation sign-off.

## 12. Change Authority
D Owner decides canonical domain semantics. I decides security/global policy; Storage decides its durable visibility realization; cross-authority protocol requires all affected authorities.

## 13. Open Decisions
I acceptance of JF-10 commit authorization sequencer; concrete Storage transaction profile and recovery proof; producer registration atomicity; cross-module cursor conformance; global Forget criterion and target completeness.

## 14. Explicit Non-Claims
No physical erasure, global Forget completion, implementation correctness, fault-injection pass or deployment readiness claim.
