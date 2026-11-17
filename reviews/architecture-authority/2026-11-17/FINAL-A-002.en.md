# Final Architecture Engineering Assessment — FINAL-A-002

- Authority: A — Principal System Architecture Authority
- Version: 1.0.0
- Date: 2026-11-17
- Exact main baseline: `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
- Review branch: `review/session-4-a-final-architecture-authority-current-2026-11-17`
- Controlling tracker: Issue #43
- Overall decision outcome: **DEFERRED**
- Architecture state: **ARCHITECTURE_NOT_READY**

## Executive decision

The architecture is **plausible in principle but not yet proven coherent, physically realizable, verifiable and maintainable as a complete system**. The project is not rejected as infeasible. It is deferred from architecture freeze and full implementation entry because non-waivable semantic, authority, atomicity, security and recovery prerequisites remain open.

A grants bounded preparatory work only. Scoped APPROVED_WITH_CONDITIONS applies solely to Option A as the v1 logical direction (A-01..A-05 and exact D adoption remain open) and H 1.2.14/CSubmitOutcome 1.0.1 as an L1/L2 candidate (B-01..B-04 remain open). Neither scope means Gate passage, L1/L2 closure, protected-path implementation authorization, schema/technology freeze, deployment approval or production authorization.

## Five fundamental risks

1. L1 logical serialization profile is selected by Storage Option A; actual L4 physical engine/deployment and visibility proof remain open (Storage/D/I).
2. B Fact/Claim/identity/temporal semantics remain ADR-BLOCKED.
3. Forget/revocation/restore lacks end-to-end no-resurrection proof and complete inventory.
4. I36 governance, trust and authorization approvals remain open.
5. B protocol exact-manifest drift (v3.2.9 stale; v3.3.0 successor required), plus D/E/I/Storage publication, JF-10 recovery and C/G/H Applied/provider-outcome proof remain unresolved.

## Five complexity bottlenecks

1. Forget fence × producer admission × dependency registration × publication.
2. Global Forget across canonical, derivatives, indexes, cache, context, adapter, replicas and backups.
3. Storage/COC/JF-10 transaction, same-XID recovery, quorum, failover and restore.
4. D/E durable ingress, outbox, lease, retry, replay and cursor composition.
5. C/G/H final request, provider side effect and Applied proof coupled to I/D authority.

## Engineering prerequisites and critical path

P0-01 implementation repo/owner → P0-02 B domain semantics and P0-03 I governance/inventory → B-01..B-04 exact H/C/D/I/Storage manifest closure → A-01..A-05 Option A L1/L2 clarification and D exact adoption → P0-04 D/E/I/Storage atomic publication/Forget contract → P0-05 Storage/COC/JF-10 physical proof → P0-06 C/G/H Applied contract → P0-07 bounded durable canonical slice → P0-08 safe retrieval/rebuild → P1 Context/Adapter/Applied → integrated recovery and conformance. This ordering is not fully serial: synthetic benchmarks, harness scaffolding, source refresh, bilingual automation and candidate DB experiments may run in parallel.

## Decision record

**Overall outcome: DEFERRED.** Scope: architecture freeze, full implementation entry, P0 correctness claims and production activation. Permitted next action: bounded preparation listed in READINESS-002 and PRIORITY-002.

Decision outcomes are restricted to:
- APPROVED — evidence complete for the stated scope; all mandatory criteria met.
- APPROVED_WITH_CONDITIONS — only for bounded scope; each accepted residual condition has a complete owner/evidence/deadline/Gate record.
- DEFERRED — evidence/prerequisites insufficient; prohibited scope remains closed.
- REJECTED — proposed design violates a non-waivable invariant or cannot be reconciled.

### Approved condition

- Option A: conditionally accepted only as the v1 logical direction; A-01..A-05 remain blocking and L1 is not closed until the successor ADR and exact D/Storage/I reviews satisfy them.
- B protocol: H Unified 1.2.14 / wire 1.3.0 + CSubmitOutcome 1.0.1 conditionally accepted only as an L1/L2 candidate; B-01..B-04 remain blocking; v3.2.9 is stale and requires v3.3.0/equivalent reviewed by C/H/D/I and A.
- COND-NB-01: vector/ANN production capability deferred; synthetic benchmark may proceed under F ownership. This is the only accepted non-blocking residual issue; full record is in DEFERRED-002. No Critical correctness/security condition is waived.

### Rejected conditions

None of the five independent assessments is rejected as a whole. Any proposal to waive domain truth, canonical authority, atomicity, security/Forget, mandatory Owner contracts or explicit Gate entry criteria is rejected as non-waivable.

### Deferred conditions and owners

| ID | Owner | Closure deadline | Risk acceptance |
|---|---|---|---|
| AR-01 L4 physical realization of selected Option A | Storage + D + I | Before final visibility implementation / JF-10 Gate A completion | Not accepted; blocking |
| AR-02 domain semantics | B | Before dependent schema freeze | Not accepted; blocking |
| AR-03 Forget/inventory | I + D + Storage; all consumers | Before Forget/restore security Gate | Not accepted; blocking |
| AR-04 Applied/provider | C/G/H + I/D | Before Applied implementation/acceptance | Not accepted; blocking |
| AR-05 governance | I + external authorities | Before protected production use | Not accepted; blocking |
| AR-06 JF-10/COC | Storage + A/COC + I/D/C | Gate A→B→C sequential exit | Not accepted; blocking |
| AR-07 source freshness | Each Owner; A tracks | Before G1/G2 and each freeze review | Not accepted; blocking |
| AR-08 cursor/replay | D/E/Storage | Before canonical end-to-end conformance | Not accepted; blocking |
| AR-09 production DR | Storage + I + operations authority | Before production authorization | Not accepted; blocking |
| AR-10 governance economics | A + all Owners + engineering lead | Before scale/operating-model commitment | Residual risk open; not a core semantic waiver |

## Mandatory open condition records — not accepted as residual risk

The following conditions are blocking and NOT accepted or waived. This register supplies accountable ownership, closure criteria and verification requirements; it does not grant Owner approval.

### A-01 — Shared transaction executor and D/Storage write authority
- Problem/evidence: Option A requires D-owned and Storage-owned state changes in one per-BrainAuthority transaction, but executor authority and row-write capabilities are underspecified. Evidence: PR #54 review Blob ff782d7ab32bdbe66f01a2057c516c5a855abdd3; proposed amendment Blob f5ad30c8570d480f60bc9b02ee53c06317b41525 (not adopted); Storage ADR Blob bb544ba2f346bdc130d524bd5c7310d86f367988.
- Risk/blocking: High; blocks L1/L2 closure.
- Permitted/prohibited: contract drafting and synthetic transaction harnesses only; no generic cross-module write permission, cross-owner canonical-row mutation or L1 closure.
- Owner: Storage + D. Closure: define per-BrainAuthority transaction executor/UoW, immutable D and Storage mutation commands, DB-role isolation, narrowly scoped anchor update and same transition-ref/digest idempotency; obtain exact D/Storage acceptance.
- Deadline/evidence: before L1/L2 closure; successor ADR/API Blob, exact Owner decisions, bilingual parity and wrong-owner/stale-command negative tests.
- Risk acceptance rationale/authority: none; A does not accept this unresolved risk for D or Storage. Escalation: keep L1/L2 closed and stop implementation assuming implicit shared write authority. Gate: G2/G3, Option A L1/L2.

### A-02 — D EffectPermit and fence-sensitive lifecycle coverage
- Problem/evidence: anchor transitions may omit attempt/lease, retry/replay, protected source read/execution, late dependency and terminalization races. Evidence: PR #54 review Blob ff782d7ab32bdbe66f01a2057c516c5a855abdd3; D publication contract Blob 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78.
- Risk/blocking: Critical; blocks Forget/publication correctness.
- Permitted/prohibited: state-machine and race-harness design only; no protected source read/execution or final publication with incomplete fence coverage.
- Owner: D (E/Storage are consumers). Closure: map every fence-sensitive transition; define typed single-use/non-replayable EffectPermit bound to BrainAuthority, WorkItem, Attempt, Lease, source/lineage/scope digest, ForgetFenceGeneration and anchor revision; define late-dependency barrier reopen.
- Deadline/evidence: before L1/L2 closure and any protected path; exact D contract, consumer acceptance, both serial orders, stale permit, late dependency, crash/ACK-loss and retry/replay traces.
- Risk acceptance rationale/authority: none; A cannot accept D lifecycle risk. Escalation: keep Forget/publication Gate blocked. Gate: G3/G4.

### A-03 — One BrainAuthority per atomic v1 operation
- Problem/evidence: per-authority anchors do not define whether one Publication/Forget operation can span several BrainAuthorityRefs. Evidence: PR #54 review Blob ff782d7ab32bdbe66f01a2057c516c5a855abdd3 and proposal Blob f5ad30c8570d480f60bc9b02ee53c06317b41525.
- Risk/blocking: High; blocks v1 scope closure.
- Permitted/prohibited: single-authority operation profile and per-authority fan-out design; no cross-BrainAuthority atomicity claim or single transaction across authorities.
- Owner: D + Storage + I; A integrates. Closure: bind every v1 atomic PublicationOperation/ProducerWork admission/fence/visibility outcome to exactly one BrainAuthorityRef and SerializationDomainRef; define Global Forget as per-authority fan-out with complete terminal proof set.
- Deadline/evidence: before L1 closure or any multi-authority feature; normative scope statement, negative cross-authority tests and global inventory/completion proof.
- Risk acceptance rationale/authority: A conditionally accepts the single-authority v1 scope only; no cross-authority atomicity risk is accepted. Escalation: block multi-authority capability. Gate: G2/G3/G4.

### A-04 — I COMMIT_WON receipt crash/revocation/replay semantics
- Problem/evidence: single-use I authorization must define immutable tuple, later revocation, same-receipt replay and crash-before-Storage-commit behavior. Evidence: PR #54 review Blob ff782d7ab32bdbe66f01a2057c516c5a855abdd3; I P0 Blob 44986f5f864bcdc1a79d34978273644d381a68c0.
- Risk/blocking: Critical; blocks L2 authorization correctness.
- Permitted/prohibited: I-owned policy/receipt contract drafting and synthetic replay tests; Storage must not decide COMMIT_WON or mint a new authorization tuple after ambiguous crash.
- Owner: I + Storage (D/H consumers). Closure: exact tuple binding; later revocation cannot retroactively alter a won tuple but blocks later tuples; replay of the same tuple returns the same immutable result; crash remains unresolved until the same Storage operation reaches COMMITTED_VISIBLE or authoritative NO_PUBLICATION.
- Deadline/evidence: before L2 closure/protected visibility; I-signed successor contract, exact D/H/Storage reviews and crash/revocation/replay negative vectors.
- Risk acceptance rationale/authority: none; A cannot accept I policy risk. Escalation: UNKNOWN remains blocking; escalate to I/A. Gate: G2/G3/G4.

### A-05 — Independent anchor checkpoint and restore anti-rollback witness
- Problem/evidence: anchor row and transition log in one DB can roll back together under stale PITR/restore. Evidence: PR #54 review Blob ff782d7ab32bdbe66f01a2057c516c5a855abdd3; Storage ADR Blob bb544ba2f346bdc130d524bd5c7310d86f367988.
- Risk/blocking: Critical; blocks recovery and L2/L3/L4.
- Permitted/prohibited: witness design and disposable restore experiments; no writes reopened after restore without independent continuity proof.
- Owner: Storage + I; D participates. Closure: independent non-rollbackable checkpoint/root outside DB failure domain, exact DatabaseIncarnation and contiguous transition-prefix proof; unavailable/mismatch/fork/missing prefix => RESTORE_FENCED/UNKNOWN.
- Deadline/evidence: before L2/L3 closure and any production restore claim; witness contract, failure matrix, stale PITR/rollback/fork/missing-record tests and Owner approval.
- Risk acceptance rationale/authority: none; A cannot accept Storage/I recovery risk. Escalation: maintain RESTORE_FENCED and stop affected writes. Gate: G3/G4; JF-10 A/B/C.

### B-01 — H mapping must bind current D crosswalk; C must re-review successor
- Problem/evidence: H mapping Blob c196fdc7a9d88e344d37ba2810a9bce1803f8b96 still pins predecessor D crosswalk; current D crosswalk Blob is c4adf827dd62d44c43b8e871dec4835581508adf. Evidence: PR #51 ledger Blob 247b6644a3f1c61078e19befc7428be78d789d5c; C review Blob f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c.
- Risk/blocking: High; blocks protocol bundle closure.
- Permitted/prohibited: H successor mapping and C exact re-review; no protocol freeze or transfer of C approval to a changed H Blob.
- Owner: H + C. Closure: H publishes mapping pinned to current D crosswalk; C accepts that exact successor Blob.
- Deadline/evidence: before B protocol closure; exact H/C Blobs and current branch/commit pins.
- Risk acceptance rationale/authority: none; H/C own their decisions, A only integrates. Escalation: keep B blocked. Gate: G1/G2/G6.

### B-02 — H/I exact P0 and anchor-review pins must converge
- Problem/evidence: current I P0 Blob 44986f5f864bcdc1a79d34978273644d381a68c0 and H schema Blob 09fcd1fa29fe24255fbd87cae79dafb406594a59 are not reflected in one current H review + I anchor-review set. Evidence: PR #52 report Blob b59b2ef745330f901027f59b69c68b99097c604b; PR #51 ledger Blob 247b6644a3f1c61078e19befc7428be78d789d5c.
- Risk/blocking: High; blocks protocol/security closure.
- Permitted/prohibited: H re-review and I pin refresh; no claim that I P0 and H review are jointly current.
- Owner: H + I. Closure: H reviews exact current I P0/H schema; I refreshes anchor review to exact current I P0/H artifacts.
- Deadline/evidence: before B protocol closure; exact review Blobs and consumer matrix.
- Risk acceptance rationale/authority: none; H/I retain domain authority. Escalation: keep G2 blocked. Gate: G1/G2/G6.

### B-03 — H mapping disposition/current CI record is stale
- Problem/evidence: H mapping still says C review required although C acceptance exists; current H CI is run 44069941327, commit ba2c9341fee4eb9ca9e665c74bdd37b4675dd251, job 133993324484. Evidence: H mapping Blob c196fdc7a9d88e344d37ba2810a9bce1803f8b96; C review Blob f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c; PR #51 ledger Blob 247b6644a3f1c61078e19befc7428be78d789d5c.
- Risk/blocking: Medium; blocks exact-bundle currentness.
- Permitted/prohibited: H currentness addendum; do not treat old mapping status or CI as latest proof.
- Owner: H. Closure: publish exact status update binding C review and current H CI run/commit/job.
- Deadline/evidence: before v3.3.0 manifest freeze; H Blob readback and run/job link.
- Risk acceptance rationale/authority: none; H owns status. Escalation: keep G1/G2 partial. Gate: G1/G2.

### B-04 — Storage v3.2.9 manifest is stale
- Problem/evidence: manifest Blob bf323a1682f2bfadc3ff41ea4f86883d678a77e3 pins earlier C/D/I reviews and H CI run 44069777296, not current corrected pins. Evidence: PR #51 ledger Blob 247b6644a3f1c61078e19befc7428be78d789d5c; current H run/commit/job above.
- Risk/blocking: High; blocks protocol bundle closure.
- Permitted/prohibited: Storage publishes v3.3.0 or equivalent; A/C/H/D/I must not hand-edit the Storage manifest or treat v3.2.9 as current.
- Owner: Storage publishes; C/H/D/I review; A integrates. Closure: successor manifest binds current H schema/mapping/CI, C schema/review, D crosswalk/review, I P0/anchor review and exact run/commit/job; C/H/D/I review the same Blob; A independently reads it back.
- Deadline/evidence: before G1/G2 and protocol closure; exact manifest path/branch HEAD/Blob, four Owner decisions, A readback and bilingual parity.
- Risk acceptance rationale/authority: none; Storage publishes, each Owner approves its domain, A accepts integration only. Escalation: protocol bundle remains blocked. Gate: G1/G2/G6.

## Permitted work

- Isolated synthetic-data feasibility spikes and benchmarks.
- Rust workspace/toolchain and contract-neutral ports exploration.
- DB/COC candidate comparison and disposable capability experiments.
- Deterministic reference-model/fault-harness scaffolding.
- Retrieval quality experiments on synthetic fixtures.
- Exact source-pin, bilingual parity and conformance automation.
- Hardware/workload inventory and operations/runbook drafts.

## Prohibited work

- Main/Owner branch modification or merge by this decision.
- Treating any candidate schema/ADR as frozen.
- Canonical production writes or protected production-data retrieval.
- Provider side effects or Applied claims.
- Security policy invention or Global Forget completion claims without I authority.
- Cross-PolicyDomain atomicity.
- Gate release, deployment or production activation.

## Gate restrictions

- Issue #43 G1–G8: G1/G6 partial; G2–G5 blocked; G7 candidate A disposition; G8 NOT READY.
- JF-10 Gate A: PARTIAL PASS / OPEN. Gate B: BLOCKED pending Gate A completion. Gate C: BLOCKED pending Gate B completion. JF-10 P0 remains OPEN.
- Production authorization remains NOT AUTHORIZED.

## Residual risk and reversibility

All Critical risks remain open. Any accepted condition is automatically suspended if its owner, evidence, scope, deadline or Gate boundary is violated, or if a supposedly non-blocking item becomes a P0/P1 correctness dependency. Escalate to A and the relevant Owner; stop affected work; refresh exact source pins; record a new decision. A decision is reversible and does not silently supersede Owner authority.

## Evidence and cross-references

R PR #50; X PR #49; F/D/P PR #46; B protocol PR #51; B→A review PR #52; Option A review PR #54; current main `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`; Issues #3, #5, #7, #10, #25, #29 and #43; source pins in SYS-RISK-002. Companion documents: ARCH-CX-002, DEV-FEAS-002, DEP-DAG-002, PRIORITY-002, READINESS-002, CONFLICT-002, GATE-002, DEFERRED-002. This assessment does not merge PRs, close Issue #43 or authorize production.
