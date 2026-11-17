# Final Architecture Engineering Assessment — FINAL-A-002

- Authority: A — Principal System Architecture Authority
- Version: 1.0.0
- Date: 2026-11-17
- Exact main baseline: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Review branch: `review/session-4-a-final-architecture-authority-2026-11-17`
- Controlling tracker: Issue #43
- Overall decision outcome: **DEFERRED**
- Architecture state: **ARCHITECTURE_NOT_READY**

## Executive decision

The architecture is **plausible in principle but not yet proven coherent, physically realizable, verifiable and maintainable as a complete system**. The project is not rejected as infeasible. It is deferred from architecture freeze and full implementation entry because non-waivable semantic, authority, atomicity, security and recovery prerequisites remain open.

A grants bounded preparatory work only. This is not a Gate pass, implementation authorization for protected paths, schema/technology freeze, deployment approval or production authorization.

## Five fundamental risks

1. Option A is conditionally accepted as the v1 logical direction only; A-01..A-05 and exact D adoption remain open, as do L2/L3/L4 proofs.
2. B Fact/Claim/identity/temporal semantics remain ADR-BLOCKED.
3. Forget/revocation/restore lacks end-to-end no-resurrection proof and complete inventory.
4. I36 governance, trust and authorization approvals remain open.
5. D/E/I/Storage publication, JF-10 recovery and C/G/H Applied/provider-outcome proof are not end-to-end verified.

## Five complexity bottlenecks

1. Forget fence × producer admission × dependency registration × publication.
2. Global Forget across canonical, derivatives, indexes, cache, context, adapter, replicas and backups.
3. Storage/COC/JF-10 transaction, same-XID recovery, quorum, failover and restore.
4. D/E durable ingress, outbox, lease, retry, replay and cursor composition.
5. C/G/H final request, provider side effect and Applied proof coupled to I/D authority.

## Engineering prerequisites and critical path

P0-01 implementation repo/owner → P0-02 B domain semantics and P0-03 I governance/inventory → P0-04 D/E/I/Storage atomic publication/Forget contract → P0-05 Storage/COC/JF-10 physical proof → P0-06 C/G/H Applied contract → P0-07 bounded durable canonical slice → P0-08 safe retrieval/rebuild → P1 Context/Adapter/Applied → integrated recovery and conformance. This ordering is not fully serial: synthetic benchmarks, harness scaffolding, source refresh, bilingual automation and candidate DB experiments may run in parallel.

## Decision record

**Overall outcome: DEFERRED.** Scope: architecture freeze, full implementation entry, P0 correctness claims and production activation. Permitted next action: bounded preparation listed in READINESS-002 and PRIORITY-002.

Decision outcomes are restricted to:
- APPROVED — evidence complete for the stated scope; all mandatory criteria met.
- APPROVED_WITH_CONDITIONS — only for bounded scope; each accepted residual condition has a complete owner/evidence/deadline/Gate record.
- DEFERRED — evidence/prerequisites insufficient; prohibited scope remains closed.
- REJECTED — proposed design violates a non-waivable invariant or cannot be reconciled.

### Approved condition

COND-NB-01 only: vector/ANN production capability deferred; synthetic benchmark may proceed under F ownership. Full record is in DEFERRED-002. No Critical condition is waived.

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

The following are blocking conditions. They are **not** accepted or waived; their records define ownership and closure evidence only.

### A-01 — Cross-owner transaction executor and write-authority boundary
- Problem: one shared transaction writes D-owned and Storage-owned rows, but executor authority, mutation capabilities and DB-role separation are not yet normative.
- Evidence: PR #54 review Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`; amendment proposal Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525` (NOT ADOPTED); Storage ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`.
- Risk: High; Blocking: Yes for L1/L2 closure.
- Permitted: Owner contract drafting and transaction harnesses. Prohibited: shared generic write permission, cross-owner row mutation or L1 closure.
- Owner: Storage + D. Closure: define per-BrainAuthority transaction executor/UoW, immutable D and Storage mutation commands, DB-role isolation, anchor CAS and same transition-ref/digest idempotency; obtain exact D/Storage acceptance.
- Deadline: before L1/L2 closure. Verification: successor ADR/API Blob, owner decision records, bilingual parity and negative wrong-owner/stale-command tests.
- Risk acceptance rationale/authority: none; A does not accept this unresolved risk on behalf of D/Storage. Escalation: keep L1/L2 closed; stop any implementation assuming implicit shared write authority. Gate: G2/G3, Option A L1/L2.

### A-02 — D fence-sensitive lifecycle and EffectPermit coverage
- Problem: current anchor transition set may omit attempt/lease, retry/replay, protected source-read/execution, late dependency and terminalization races.
- Evidence: PR #54 review Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`; proposal Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525`; D publication proposal Blob `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78`.
- Risk: Critical; Blocking: Yes for Forget/publication correctness.
- Permitted: state-machine and race-harness design. Prohibited: protected source read/execution or final publication based on incomplete fence coverage.
- Owner: D, with E/Storage consumers. Closure: map every fence-sensitive transition; issue typed single-use/non-replayable EffectPermit bound to BrainAuthority, WorkItem, Attempt, Lease, source/lineage/scope digest, ForgetFenceGeneration and anchor revision; define late-dependency barrier reopen semantics.
- Deadline: before L1/L2 closure and any protected path. Verification: exact D contract, consumer acceptance, both serial orders, stale permit, late dependency, crash/ACK-loss and retry/replay traces.
- Risk acceptance rationale/authority: none; A cannot accept D's lifecycle correctness risk. Escalation: keep Forget/publication Gate blocked. Gate: G3/G4.

### A-03 — One BrainAuthority per atomic v1 operation
- Problem: per-authority anchor does not itself state whether one Publication/Forget operation may span several BrainAuthorityRefs.
- Evidence: PR #54 review Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`; proposal Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525`.
- Risk: High; Blocking: Yes for v1 scope closure.
- Permitted: single-authority operation profile and fan-out design. Prohibited: cross-BrainAuthority atomicity claims or a single transaction across authorities.
- Owner: D + Storage + I; A integrates. Closure: explicitly bind each v1 atomic PublicationOperation/ProducerWork admission/fence/visibility outcome to exactly one BrainAuthorityRef and SerializationDomainRef; define global Forget as per-authority fan-out with complete terminal proof set.
- Deadline: before L1 closure and any multi-authority feature. Verification: normative scope statement, negative cross-authority tests, global inventory/completion proof.
- Risk acceptance rationale/authority: A conditionally accepts the single-authority v1 scope only; no cross-authority risk accepted. Escalation: block multi-authority feature. Gate: G2/G3/G4.

### A-04 — I COMMIT_WON receipt crash/revocation/replay semantics
- Problem: single-use I authorization consumption must define immutable tuple, later revocation, same-receipt replay and crash-before-Storage-commit behavior.
- Evidence: PR #54 review Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`; proposal Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525`; I P0 Blob `44986f5f864bcdc1a79d34978273644d381a68c0`.
- Risk: Critical; Blocking: Yes for L2/authorization correctness.
- Permitted: I-owned policy/receipt contract drafting and synthetic replay tests. Prohibited: Storage interpreting COMMIT_WON independently or reauthorizing with a new tuple after ambiguous crash.
- Owner: I + Storage, with D/H consumers. Closure: exact tuple binding; later revocation cannot retroactively change a won tuple but blocks later tuples; same tuple replay returns same immutable result; crash remains unresolved until same Storage operation reaches COMMITTED_VISIBLE or authoritative NO_PUBLICATION.
- Deadline: before L2 closure and protected visibility. Verification: I-signed successor contract, D/H/Storage exact reviews, crash/revocation/replay negative vectors.
- Risk acceptance rationale/authority: none; A cannot accept I policy risk. Escalation: UNKNOWN remains blocking; escalate to I/A. Gate: G2/G3/G4.

### A-05 — Independent anchor checkpoint and restore anti-rollback witness
- Problem: anchor row and transition log in one DB can roll back together under stale PITR/restore and appear internally consistent.
- Evidence: PR #54 review Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`; proposal Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525`; Storage ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`.
- Risk: Critical; Blocking: Yes for recovery/L2/L3/L4.
- Permitted: witness design and disposable restore experiments. Prohibited: reopening writes after restore without independent continuity proof.
- Owner: Storage + I; D participates. Closure: independent non-rollbackable checkpoint/root outside DB failure domain, exact DatabaseIncarnation and contiguous transition prefix proof; unavailable/mismatch/fork/missing prefix => RESTORE_FENCED/UNKNOWN.
- Deadline: before L2/L3 closure and any production restore claim. Verification: witness contract, failure-mode matrix, stale PITR/rollback/fork/missing-record tests and Owner approval.
- Risk acceptance rationale/authority: none; A cannot accept Storage/I recovery risk. Escalation: maintain RESTORE_FENCED and stop affected writes. Gate: G3/G4; JF-10 A/B/C.

### B-01 — H mapping must bind current D crosswalk; C must re-review successor
- Problem: H mapping Blob `c196fdc7a9d88e344d37ba2810a9bce1803f8b96` still pins predecessor D crosswalk; current D crosswalk is `c4adf827dd62d44c43b8e871dec4835581508adf`.
- Evidence: PR #51 ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`; C acceptance Blob `f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c`.
- Risk: High; Blocking: Yes for protocol bundle closure.
- Permitted: H successor mapping and C re-review. Prohibited: protocol freeze or silently transferring C approval to a changed H Blob.
- Owner: H + C. Closure: H publishes mapping bound to current D crosswalk; C accepts that exact successor Blob.
- Deadline: before B protocol closure. Verification: exact H/C Blobs and current branch/commit pins. Risk acceptance: none. Authority: H/C; A only integrates. Escalation: keep B blocked. Gate: G1/G2/G6.

### B-02 — H/I exact P0 and anchor review pins must converge
- Problem: current I P0 Blob `44986f5f864bcdc1a79d34978273644d381a68c0` and H 1.2.14 schema `09fcd1fa29fe24255fbd87cae79dafb406594a59` are not yet reflected in one current H review + I anchor review set.
- Evidence: PR #52 report Blob `b59b2ef745330f901027f59b69c68b99097c604b`; PR #51 ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`.
- Risk: High; Blocking: Yes for protocol/security closure.
- Permitted: H re-review and I pin refresh. Prohibited: claim that I P0 and H review are jointly current.
- Owner: H + I. Closure: H reviews exact current I P0/H schema; I refreshes anchor review to exact current I P0/H artifacts.
- Deadline: before B protocol closure. Verification: exact review Blobs and consumer matrix. Risk acceptance: none. Authority: H/I. Escalation: keep G2 blocked. Gate: G1/G2/G6.

### B-03 — H mapping disposition/current CI record is stale
- Problem: H mapping still says C review required although C acceptance exists; current H CI binding is run 44069941327 / commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251` / job `133993324484`.
- Evidence: H mapping Blob `c196fdc7a9d88e344d37ba2810a9bce1803f8b96`; C review Blob `f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c`; PR #51 ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`.
- Risk: Medium; Blocking: Yes for exact bundle currentness.
- Permitted: H currentness addendum. Prohibited: treating old status or CI as latest proof.
- Owner: H. Closure: publish exact status update binding C review and current H CI run/commit/job. Deadline: before v3.3.0 manifest freeze. Verification: H Blob readback and run/job link. Risk acceptance: none. Authority: H. Escalation: keep G1/G2 partial. Gate: G1/G2.

### B-04 — Storage v3.2.9 manifest is stale
- Problem: manifest Blob `bf323a1682f2bfadc3ff41ea4f86883d678a77e3` pins earlier C/D/I reviews and H CI run 44069777296, not current corrected pins.
- Evidence: PR #51 ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`; current H run 44069941327 / commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251` / job `133993324484`.
- Risk: High; Blocking: Yes for protocol bundle closure.
- Permitted: Storage publishes v3.3.0 or equivalent. Prohibited: A/C/H/D/I hand-editing Storage manifest or treating v3.2.9 as current.
- Owner: Storage; C/H/D/I review; A integrates. Closure: successor manifest binds current H schema/mapping/CI, C schema/review, D crosswalk/review, I P0/anchor review and exact run/commit/job; C/H/D/I all review the same Blob; A independently re-reads it.
- Deadline: before G1/G2 and protocol closure. Verification: exact manifest path/branch HEAD/Blob, four Owner decisions, A readback and bilingual parity. Risk acceptance: none. Authority: Storage publishes; each Owner approves its domain; A accepts integration only. Escalation: protocol bundle remains blocked. Gate: G1/G2/G6.

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

R PR #50; X PR #49; F/D/P PR #46; Issues #3, #5, #7, #10, #25, #29 and #43; source pins in SYS-RISK-002. Companion documents: ARCH-CX-002, DEV-FEAS-002, DEP-DAG-002, PRIORITY-002, READINESS-002, CONFLICT-002, GATE-002, DEFERRED-002. This assessment does not merge PRs, close Issue #43 or authorize production.
