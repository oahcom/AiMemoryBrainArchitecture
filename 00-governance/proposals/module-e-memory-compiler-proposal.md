# Module E — Memory Compiler Baseline & Redlines

- Proposal: E-MBR-0.1.0
- Status: **PROPOSED — prepared by Session P for E Owner review/adoption; NOT an E Owner decision**
- Intended Owner: E — Memory Compiler
- Source branch / HEAD: `session-e-memory-compiler-2026-11-16` @ `530645a08b55716257cf4cde20b0900b628abb52`
- Evidence: `04-memory-compiler/compiler-state-and-producer-admission.md` blob `e59f517fff161ab882aa0ddc4a5bda513964ae1a`; `04-memory-compiler/forget-fence-and-derived-registration.md` blob `00e37ba56596e710513c8d0568acd79141d9101b`; `04-memory-compiler/phase-3.6-joint-producer-publication-decision.md` blob `aaa15de9d6e3a6ce74b11fda376369d6a49659ab`
- Project PB/PR: P proposal v0.1.0 only, not approved/active.

## 1. Module Mission
Transform accepted source Events and evidence into governed, provenance-preserving derived artifacts while ensuring no derivative becomes visible before all canonical, authorization and Forget gates succeed.

## 2. Ownership Baseline
E owns compiler work/attempt/lease/retry/DLQ/replay state, extraction/normalization/consolidation, derivation lineage and private staging lifecycle. D owns canonical producer registration/barrier and ForgetFence; Storage owns durable visibility pointer/receipt; I owns authorization and global policy.

## 3. Capability Baseline
Durable ingress receipts; stable WorkItemId and per-attempt identity; fenced leases; idempotent retries; lineage manifests; private staging; dependency registration reconciliation; final publication gate; deterministic recovery and non-visible failure states.

## 4. Domain Ownership
E owns compiler lifecycle and derivative lineage, not canonical Memory identity/commit (D), security permission/epoch (I), typed domain meaning (B), transport identity (H), index watermark/cache (F) or Context (G).

## 5. Interface Baseline
Lifecycle candidate: Accepted → Registered → Queued → Leased → Running → StagedPrivate → DependenciesRegistered → PublishGatePending → Published. WorkItemId stable across retries; AttemptId and LeaseId change; DerivationRunId changes per recompile; child work remains linked to root barrier. StagedPrivate is never queryable. Published requires D registration/fence, current I authorization and Storage visibility transaction.

## 6. Security Baseline
Authenticated producer binding is supplied by H/I/B; payload-supplied IDs are not trusted. Re-check PermissionEpoch and ForgetFence at execution and publication. Fail closed when any authority or recovery result is ambiguous.

## 7. Module Redlines
- E-PR-01 No staged/private derivative, provenance edge, embedding, excerpt, outbox or cache payload may be exposed before final authoritative publication. CRITICAL.
- E-PR-02 No retry/recompile/DLQ/replay may create an unlinked root that evades D barrier. CRITICAL.
- E-PR-03 No local E state/receipt may be represented as D canonical commit or Storage publication. CRITICAL.
- E-PR-04 No stale lease epoch may stage, publish or terminalize work. HIGH.
- E-PR-05 No compiler success may imply global Forget completion or physical erasure. CRITICAL.

## 8. Forbidden Cross-module Actions
E cannot create canonical Memory commits outside D; mint permissions/epochs (I); define wire/authentication (H); mutate indexes/cache (F); update Context (G).

## 9. Dependency Contracts
D producer registration/barrier/fence; I PermissionEpoch and commit authorization; H authenticated producer binding; Storage atomic visibility pointer/publication receipt. JF-10 and D/E/Storage atomic registration/final publication gate remain OPEN until implementation and crash/race conformance.

## 10. Conformance Requirements
Retry/replay idempotency; lease fencing; child/root barrier accounting; staged artifact invisibility; registration race with Forget; authorization revocation race; publication crash windows; recovery after lost ACK; provenance completeness and no bypass tests.

## 11. Acceptance Criteria
E Owner accepts exact version; D/I/H/Storage interface versions accepted; executable linearization and recovery tests pass; no visible derivative without gate proof; consumer readback confirms exact version.

## 12. Change Authority
E Owner decides compiler lifecycle. D, I and Storage decide their own gates and state. Publication protocol changes require joint authority acceptance.

## 13. Open Decisions
Concrete Storage atomic profile; D/E registration and publication API realization; I JF-10 acceptance; final recovery behavior and fault-test evidence; producer identity binding.

## 14. Explicit Non-Claims
No production implementation, crash-safety proof, physical deletion, or JF-10 closure claim.
