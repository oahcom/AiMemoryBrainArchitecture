# Open Questions and Blockers / 未决问题与阻塞项

- Task: TECH-REALITY-001-A | Owner A | Date: 2026-11-17
- Status: **OPEN / BLOCKED ITEMS PRESERVED**

## 1. Critical architecture blockers / 关键架构阻塞

| ID | Question | Current evidence | Required owner | Blocks |
|---|---|---|---|---|
| OQ-01 | Which physical storage topology can prove canonical commit, cursor and Forget admission/publication semantics? | TAB-001 TEC-003 candidate; Issue #43/PR #44 says D/Storage serialization topology ADR-BLOCKED; Issue #25 open | Storage + D/E; A integrates | DB selection and implementation |
| OQ-02 | How are COC recovery-cutoff and JF-10 prepared-participant protocols bridged? | Issue #43/PR #44 explicitly says separate protocols; automatic composition not approved; JF-10 Gate B/C blocked | Storage/Consistency + A/I | Distributed transaction/recovery claims |
| OQ-03 | What is the exact linearization point for producer admission vs Forget fence installation? | TAB-001 §9 OPEN critical; Issue #25 | D/E/Storage | Forget safety |
| OQ-04 | What is the exact atomic/linearizable dependency-registration and final publication gate? | TAB-001 §9 OPEN critical; Issue #25 | D/E/Storage | Anti-resurrection |
| OQ-05 | What is the full Applied proof chain at final inference request? | Issue #3 says Applied Contract Frozen = NO; PR #44 says chain not frozen | C/G/H (+ I/D) | Context sync and acceptance |
| OQ-06 | Which Fact/Claim representation is normative? | Issue #43/PR #44 preserves B Fact/Claim ADR-BLOCKED | B | Schema, serialization, indexes |
| OQ-07 | What is the sealed Global Forget target inventory and cross-owner evidence vector? | Issues #4/#5; PR #44 says governance approvals remain blocked | I + D/E/F/G/H | Global Forget completion |
| OQ-08 | What identity and trust binding applies to producer/adapter/provider? | I-owned Principal/Actor/Scope and C/H contract dependencies remain open | I/B/C/H | Auth, audit, external egress |
| OQ-09 | What does Storage mean by transaction participant identity and physical participant topology? | Issue #10 JF-10 probe; Issue #43 says topology ADR blocked | Storage/Consistency | COC/JF-10 and recovery |
| OQ-10 | Which OS, hardware, corpus, concurrency and RPO/RTO are actual product requirements? | TAB-001 §11/§12 lists unknowns; no workload data | Product/Owner A/Release | Performance and topology selection |

## 2. Technology-specific open questions / 技术选型未决

1. SQLx or rusqlite for SQLite adapter? Which connection/worker model owns writes and transactions?
2. SQLite or PostgreSQL for the first executable prototype after Storage's physical topology decision?
3. Is a content-addressed filesystem adequate for the first target OS and backup threat model?
4. Does FTS5 meet Chinese/mixed-language recall quality, or is Tantivy required?
5. Is vector retrieval needed in the first vertical slice? If yes, which single candidate wins on filtered recall, updates/deletes and rebuild?
6. Does the compiler require a workflow engine beyond DB-backed leases/outbox? Which task durations and retry patterns prove that?
7. Is Cedar's entity/action/resource model compatible with I's policy semantics? Is an external relationship graph service needed?
8. Which BMCP transport/encoding is required by C's real Agent integration targets?
9. Which inference backend has compatible operators, GPU execution provider and packaging for the target device?
10. Which observability signals are stable and necessary in local deployment, given OTel Rust signal maturity differences?

## 3. Currentness and repository governance / 当前性与仓库治理

### PR #44 / Issue #43

At capture time PR #44 is open and draft. Its body states:
- NOT READY FOR ARCHITECTURE FREEZE.
- D/Storage serialization topology ADR-BLOCKED.
- C/H/D/I exact-version migration incomplete.
- Integrated publication and Forget/restore reference-model evidence incomplete.
- Full Applied chain not frozen.
- B Fact/Claim ADR blocked.
- COC and JF-10 are separate protocols; automatic composition is not approved; JF-10 Gate B/C remain blocked.

This research must remain complementary to PR #44 and must not be used to imply that its architecture freeze gates passed.

### PR #28

PR #28 is open and draft. Its current body explicitly says:
- The bilingual manifest scope is only the files included in that PR; it is not repository-wide completion.
- Detailed Owner source specifications and several C/G/H Applied and Storage/Consistency contract pairs remain incomplete.
- Structural CI is not semantic parity or architecture approval.
- H36 suites remain NOT RUN; Applied freeze remains BLOCKED; Storage topology remains ADR-BLOCKED; JF-10 remains P0 OPEN / NOT IMPLEMENTED / NOT RUN.

The new research files in this task are bilingual in a single paired artifact (Chinese and English sections). They do not translate or alter other Owners' contracts.

### PRs #31–#35

AI-RUN-003 runtime architecture and ADR chain is stacked, open and proposed. PR #35 says its logical data model is storage-neutral and no SQLite/PostgreSQL choice or production migration is claimed. Do not use this Owner Worker runtime as evidence that the product Memory Brain runtime has been implemented.

## 4. Evidence needed to close / 关闭所需证据

- Approved physical storage topology ADR with exact participant and recovery semantics.
- D/E/Storage operation contract and executable race tests in both serial orders.
- C/G/H final-request Applied conformance tests with lost ACK, stale delivery and reconnect.
- I approved identity/revocation/Forget target model and restore semantics.
- B approved Fact/Claim and typed-reference semantics.
- Reproducible storage, workflow, search and inference prototypes on declared hardware.
- Full DB + blob + index backup/restore with current Forget/revocation replay before serving.
- Independent review by the responsible Owners and a separate independent technology reviewer.
