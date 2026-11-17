# Phase 1.F — A Exact Integration Review of Storage v3.2.7 / H 1.2.14
# Phase 1.F — A 对 Storage v3.2.7 / H 1.2.14 的精确集成审查

- Reviewer perspective: A — Principal Integration Architect
- Review target: Storage v3.2.7 exact bundle manifest
- Exact manifest Blob: `4435fc0340a4fce10751679a95f3b4c821bdae4d`
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H mapping Blob: `1cbe74eba69325510d6b1019d971661f965eabf8`
- H validator Blob: `eab961a08d41e871f38543b18ee60cf024977414`
- H test Blob: `53774aca0224fd9a727dfa625ba142825f1754b0`
- H CI: run `44068247661`, tested commit `0701b12c3f43e1e6d5706c8eb2747e1c583d60b7`, SUCCESS, 25 tests.
- Disposition: **ACCEPT AS A COHERENT ARCHITECTURE CANDIDATE WITH ENUMERATED BLOCKERS — DO NOT FREEZE**
- Provenance: delegated A-role integration simulation in the coordinating session; **not an independent human A Owner acceptance**.

## 1. Integration decision

The v3.2.7 bundle establishes one exact H 1.2.14 / CSubmitOutcome 1.0.1 candidate pair and no longer carries the prior H 1.2.12/1.2.13 mapping as its current binding. The schema, validator, test and mapping Blob identities are explicit. The H CI result is real and is pinned to the exact validator/test Blobs.

The new I terminal, D Forget clearance and Storage resolution callback slots correct an important authority-boundary omission: a generic COC join cannot impersonate these three distinct issuers. Missing callbacks produce UNKNOWN, preserving fail-closed behavior.

A accepts the design composition as a candidate only. This does not establish independent Owner adoption, production authority wiring, complete H↔C object validation, or Storage deployment.

## 2. Blocking conditions

### A1 — Independent Owner adoption

C, I, D and H must each issue fresh exact-Blob decisions against the v3.2.7 bundle. Prior 1.2.13 or earlier decisions do not transfer. The current A and Storage documents are delegated simulations and cannot be counted as independent approvals.

### A2 — H full-path validator conformance

The 25-test CI pass proves callback orchestration, not full end-to-end validation. The new orchestration tests mock schema validation, semantic predicates and digest/preimage computation. Add at least:
- a complete positive H envelope + immutable CSubmitOutcome 1.0.1 fixture through the unmocked validator;
- one negative mutation per duplicated wire field and exact C object identity/digest;
- C sequence namespace/key-status namespace mismatch and rollback/fork cases;
- I terminal non-COMMIT_WON and contradictory same-XID cases;
- D stale FenceGeneration, late lineage and barrier reopen cases;
- Storage wrong DB incarnation, GID, PrepareAttempt, participant ledger and terminal resolution cases;
- UNKNOWN behavior for each unavailable owner authority independently.

### A3 — I authorization semantics

The I callback must verify the exact I terminal proof and must not treat an arbitrary terminal I state as permission. Provider invocation authorization still requires the applicable I COMMIT_WON outcome plus C/D predicates at the transport-owning admission boundary. H verifies evidence; it does not own I policy or revocation authority.

### A4 — D Forget and Storage recovery joins

D clearance must bind exact Forget FenceGeneration, affected lineage/barrier and currentness. Storage proof must bind DB incarnation, GID, prepare attempt, participant ledger and same-GID terminal resolution. These must be separately authenticated and joined; references alone are not proof.

### A5 — R1/R2, Gate A/B/C and deployment evidence

The bundle does not close Recovery Cutoff Batch completeness, owner-local gate linearization/release, COC quorum persistence, exact prefix/readback, deployed Storage recovery or executable distributed fault injection. Existing Gate A remains PARTIAL PASS / OPEN; Gate B BLOCKED; Gate C DEFERRED / NOT RUN.

## 3. Gate and authorization statement

- JF-10 P0: OPEN.
- R1 Recovery Cutoff Batch completeness: OPEN.
- R2 owner-local Gate linearization/release: OPEN.
- Multi-PolicyDomain atomicity: BLOCKED.
- C/I profiles and production trust/key lifecycle: NOT APPROVED / OPEN.
- Production activation and provider egress: NOT AUTHORIZED.
- Full Applied, Global Forget Completion, physical Forget and universal exactly-once: NOT PROVEN.

## 4. Required next sequence

1. Obtain fresh exact H/C/I/D Owner reviews and record each decision without role conflation.
2. Complete unmocked H envelope + C object full-path positive/negative tests.
3. Implement owner-authoritative I/D/Storage adapters and prove their independent currentness and signature/evidence checks.
4. Complete C provider adapter send-vs-close/idempotency/outcome lookup and Storage same-GID/quorum/readback fault evidence.
5. Close R1/R2 and JF-10 P0 through exact, independently reviewed evidence.
6. A must then perform a fresh exact-version re-review before any freeze recommendation.

**Final A disposition: ACCEPT AS A COHERENT ARCHITECTURE CANDIDATE WITH ENUMERATED BLOCKERS — DO NOT FREEZE.**
