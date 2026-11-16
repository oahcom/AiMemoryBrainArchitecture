# Unified A–I Remediation & Evidence Register

- Register ID: P-UNIFIED-MBR-REMEDIATION-001
- Date: 2026-11-17
- Status: **OPEN — coordination register; no Owner decision is inferred**
- Authority: Session P records dependencies and evidence. Module Owners retain their own decisions; I retains security/governance authority; Storage retains physical realization; designated ADR/Governance authority retains project-level decisions.

## 1. Priority actions

| ID | Priority | Work item | Accountable authority | Current state | Closure evidence |
|---|---|---|---|---|---|
| UMR-001 | P0 | Common CGH-APPLIED-1.1 package/schema freeze and executable closure | C, G, H jointly; I/D/B predicate authorities; A records | Exact A package 4961... + COC companion fc3... decisions recorded: C/D/G/H/I ACCEPT WITH EXCEPTIONS; B APPROVE; Storage CONFIRMED WITH CHANGES — interface only. H schema remains candidate/not frozen; COC deployment and runtime tests open | Freeze requires H complete production schema/crypto/compatibility evidence, named/deployed COC, I/D/C/G runtime binding, owner-authoritative tests and conformance; see applied-contract-1.1-exact-version-reconciliation.md |
| UMR-002 | P0 | JF-10 v2 production adapter binding and recovery | Storage engineering + D/E; I for authorization/sequencer | PostgreSQL 18.7 prior probe revision 7/7 PASS on commit 8b8c...; current HEAD 3c8... has six workflows PASS and enhanced PITR run FAILURE; production runtime/adapter NOT IDENTIFIED; Gate A PARTIAL PASS / OPEN | Canonical runtime repo/branch, adapter/schema/build SHA; real I/D/E transaction mapping; production-equivalent fault/failover/PITR; real fencing, operator/runbook and RPO/RTO |
| UMR-003 | P0 | Formal ADR-001 Fact/Claim decision | Designated ADR/Architecture Governance authority; B owns domain recommendation | ADR-BLOCKED | Exact selected option, rationale, approver authority, timestamp, version, migration and affected-consumer acceptance |
| UMR-004 | P0 | I security policy and Global Forget governance | I + named external governance approvers | GOVERNANCE-BLOCKED | I35-DEC/I36-GOV approved exact versions; signed inventory seal; target-state mapping; external recipient/backup/restore evidence; exception decisions |
| UMR-005 | P1 | B/I/H typed identity + permission binding | B, I, H; consumers C/D/E/F/G/Storage | OPEN / PARTIAL DESIGN | Exact typed fields and trust chain, transport authentication binding, permission/epoch mapping, forged identity and stale/revoked negative tests, consumer acceptance |
| UMR-006 | P1 | Owner baseline adoption and current evidence pins | Each A–I Owner; A tracks | All nine module proposals PROPOSED; no module baseline adoption recorded by this review | Owner-specific ADOPT / ADOPT WITH EXCEPTIONS / REVISE / REJECT record, proposal version, current HEAD, artifact blob SHA and affected-consumer acceptance |
| UMR-007 | P1 | Baseline template applicability and structural normalization | Project Governance Authority / P until appointed | P template exists; not in main; governance not ratified | Exact template version adoption or approved replacement; each Owner maps all required sections and records deviations |
| UMR-008 | P1 | Refresh technical-review / integration source HEAD provenance | A/C/F/G/H; B/D/E/I review coverage to be decided | TAB-001 reports static/conditional; A Phase 3.6 closure tracker §13.43 is stale against newer Storage HEAD and Applied 1.1 exact Owner decisions | Refresh each report to current source HEAD/artifact blobs; distinguish exact Owner decision from implementation/test/deployment status; A to refresh closure tracker and gate vector |
| UMR-009 | P1 | TAB-001 Owner technology review coverage for A/B/D/E/I | A/B/D/E/I Owners; A coordinates | Assigned reports absent on current Owner branches; C/F/G/H reports exist as static conditional reviews | Owner-specific review at exact task-pack path, six dimensions R1–R6, current main blueprint blob SHA, current Owner HEAD, findings and no-claim statement |
| UMR-010 | P1 | Inspect PostgreSQL 18.7 capability probe workflow evidence | Storage Owner / CI operator | PR #12 closed; description limits evidence to single-node probe and disclaims production/failover proof; run result not yet verified here | Workflow run URL, commit/build SHA, exact job/test result and logs; preserve non-claims for replication, production restore, hardware durability and operator readiness |
| UMR-011 | P2 | Normalize document structure to 14-section template | Each Owner; governance template authority | A has 13 sections; B/C/G/H/I 14; D/E/F 15; template only on P | Owner-confirmed section map, distinct Evidence & Version History, deviations justified |
| UMR-012 | P2 | Central gate vector and registry synchronization | A; P maintains governance rollout record | Tracking registry stale at review start | Current branch HEADs and artifact SHAs, owner decisions, cross-owner acceptances, governance, implementation and tests tracked independently |


| UMR-013 | P0 | SQLite/PostgreSQL transaction-profile decision for JF-10 | D/E/Storage; I for policy/sequencer | TAB-001 recommends SQLite WAL only as a prototype candidate; Storage PostgreSQL 18.7 probe is a single-node capability experiment; no final DB selection | Compare exact producer admission/fence/dependency/publication/recovery semantics, prepared-XID, crash/PITR/failover and operational requirements; keep TEC-003/004 OPEN until evidence |
| UMR-014 | P1 | Integrate G NVIDIA context-optimization research with TAB-001 | G; A coordinates; B/C/D/E/F/H/I/Storage consulted | G impact assessment and candidate register are PROPOSED only; no implementation/interface freeze | Cross-owner mapping for TSS, ObservationRef, compaction, fidelity, immutable evidence archive, cost gate and Forget invalidation; paired controlled benchmark and negative tests |
| UMR-015 | P1 | Reconcile P/main branch divergence before any future integration | P coordinator + A; project governance authority when appointed | P is ahead 30 / behind 4 against main; main contains TAB-001 blueprint, task pack and roadmap update | Reviewed non-destructive reconciliation of four main-side files, fresh compare, no force update and no merge without explicit authorization |


| UMR-016 | P0 | Bind PostgreSQL capability suite to canonical runtime implementation | Storage engineering + D/E/I; A coordinates | Storage dossier confirms no production runtime/Canonical Authority DB adapter/migration package in inspected repo branch; CI fixtures use isolated jf10_* tables | Identify canonical runtime repository/branch and exact adapter/schema/build SHA; map I sequencer, D fence, E publication, pointer/receipt/outbox and real reader path; run production-equivalent suite |


| UMR-017 | P1 | Refresh A Phase 3.6 closure tracking after current exact decisions and Storage regression | A Owner; P records discrepancy only | A closure tracker blob 554d4b85... still records older Storage HEAD df60... and failed deep PITR; live Storage HEAD 3c8ab8... now records corrected deep PITR and 7/7 regression pass; C/G/D/H/I/B exact 1.1 decisions and Storage interface confirmation are present on live branches | A re-fetch exact current C/G/D/H/I/B/Storage branch artifacts and current Storage dossier, update exact blob/HEAD pins and gate vector; preserve Gate A PARTIAL PASS / OPEN due no production runtime/adapter, operator, COC deployment, RPO/RTO and I/D integration |


| UMR-018 | P0 | Fix and rerun enhanced JF-10 PITR exact-WAL negative campaign | Storage Owner | Current probe blob 7fa4bb...; run 43957456225 FAIL. Reader pointer-only/receipt-only, prepared/private, commit/rollback atomicity and missing-WAL checks passed; corrupt-WAL assertion failed to recognize PostgreSQL "invalid magic number"; incomplete-WAL case not reached | Accept exact "invalid magic number" diagnostic while preserving exact segment and no-writable/no-authoritative assertions; rerun all missing/corrupt/incomplete cases and seven-workflow batch on exact current source |

## 2. Non-substitutable acceptance evidence

The following evidence classes are independent:
1. Artifact exists and can be read back.
2. Module Owner adopts a specific proposal version.
3. Affected consumer Owners accept the exact contract version.
4. External/project governance authority approves the exact policy/baseline.
5. Implementation exists at a pinned build/source SHA.
6. Required tests execute and pass with reproducible logs.
7. Deployment/operator readiness and recovery are evidenced.

No row may be marked complete because a different row is complete. Static review, branch commit, PR closure, test specification and CI workflow creation are not test pass evidence.

## 3. Gate snapshot

| Gate | State | Reason |
|---|---|---|
| Nine module proposal documents | PASS — submitted as PROPOSED | All nine artifacts fetched from their Owner branches |
| Nine module baseline Owner adoptions | OPEN | Explicit exact-version adoption not established by this review |
| ABC boundary review | PASS WITH OPEN BLOCKERS | A/B/C authority boundaries align; ADR-001 and identity binding remain open |
| DEF boundary review | PASS WITH OPEN BLOCKERS | D bounded JF-10 decision exists; physical recovery/deployment and tests remain open |
| GHI boundary review | PASS WITH OPEN BLOCKERS | G/H semantics align directionally; Applied exact-version freeze and I governance remain open |
| Common Applied freeze | DESIGN DECISIONS RECORDED WITH EXCEPTIONS; FREEZE BLOCKED | C/D/G/H/I accept exact A package+COC pair; B approves types; Storage confirms interface only. H schema/deployment/implementation/tests remain open |
| ADR-001 | ADR-BLOCKED | No formal decision record |
| JF-10 P0 | OPEN — Gate A PARTIAL PASS | Earlier seven-workflow batch passed on 8b8c; current HEAD 3c8 has six workflow passes and enhanced PITR failure 43957456225; production adapter/runtime binding, I/D/E integration, real fencing and operations remain unverified |
| Global Forget | GOVERNANCE-BLOCKED | I approvals, sealed inventory and target-state evidence incomplete |
| JF-10 PostgreSQL 18.7 CI evidence | PARTIAL PASS — earlier 7/7 on 8b8c; current HEAD 6/7 PASS, enhanced PITR FAIL | Current probe has meaningful new checks but corrupt-WAL diagnostic assertion failed; incomplete-WAL case not reached; no production adapter or end-to-end conformance |
| TAB-001 Owner technology review | 4/9 reports present; 5/9 missing | A/B/D/E/I reports absent at assigned paths; C/F/G/H reports are conditional/static |
| Project G0 / architecture freeze | GOVERNANCE-OPEN / NOT AUTHORIZED | No PGA appointment or exact G0 approval evidenced |
| Production implementation/test sign-off | NOT VERIFIED / NOT RUN where applicable | No general end-to-end implementation and conformance evidence |

## 4. Operating sequence

1. Close UMR-001, UMR-003 and UMR-005 at the exact contract/ADR level without conflating their authority.
2. Close UMR-018 and bind the corrected PostgreSQL capability suite to the actual runtime under UMR-016; decide the SQLite alternative under UMR-013 only after exact JF-10 invariants are mapped. Reconcile G research under UMR-014; do not merge P/main while UMR-015 remains open.
3. Have A refresh its stale Phase 3.6 closure tracker under UMR-017; P cannot rewrite A's Owner record.
3. Close UMR-002 and UMR-004 with real Storage and I evidence.
4. Obtain each Owner's exact-version baseline disposition under UMR-006.
5. Normalize the documents and review coverage under UMR-007/008/009/011.
6. A publishes an updated integration gate vector; P updates project tracking.
7. Only a formally appointed Project Governance Authority may ratify G0 or authorize a project-wide architecture freeze.

## 5. Change log

- 2026-11-17: Initial unified register prepared from live A–I branch reads, current baseline artifact blobs, A Phase 3.6 closure tracking, D JF-10 bounded acceptance and Storage PR #12 metadata.

- 2026-11-17 addendum: reconciled current TAB-001 v0.1 and A–I technology-review task pack. Main HEAD `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f`; TAB-001 blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`; task pack blob `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`. G research blobs `3fb9f011e24c93a748442018d48c5954584e4f43` and `eadefd4e0fe541ef8479a030a2a99a0d57dbcf8b`. P/main divergence: ahead 30 / behind 4.

- 2026-11-17 JF-10 evidence reconciliation: Storage branch `a1fbbd15d3a7993bbb61821ad44957e4f69d3ed1`, dossier blob `2f76ca8b8c19b84c37e7604cd254990dd93eb8b1`. Seven PostgreSQL 18.7 CI workflows succeeded on commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`; see `00-governance/reviews/jf10-storage-evidence-assessment.md`. Gate A is PARTIAL PASS / OPEN, not closed.

- 2026-11-17 Applied correction: live C/D/G/H/I exact-version decision artifacts and B type approval all pin A package `4961ffefc0f9920efb8425a9b2a7af42d8f64819` plus COC companion `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`; Storage confirms interface only. Applied freeze remains blocked by H candidate schema/deployment, COC operator, runtime implementation and conformance. See `applied-contract-1.1-exact-version-reconciliation.md`.
- 2026-11-17 A source freshness: A closure tracker blob `554d4b85a94f433856506dce4c020b9c00183e69` ends at §13.43 and records old Storage head `df60b547...` / failed PITR; current Storage head is `3c8ab8ee4579a550300aa48aecab928149cf9370` with corrected seven-workflow regression pass. Gate A remains PARTIAL PASS / OPEN because production runtime/adapter, I/D integration, COC deployment/operator and operations remain unverified.

- 2026-11-17 current Storage regression: Storage HEAD `3c8ab8ee4579a550300aa48aecab928149cf9370`, enhanced PITR probe blob `7fa4bb3fb07eacc3f708f5682ea4c9e2019f267d`. Current branch batch: six workflows PASS, PITR run `43957456225` FAILURE because corrupt-WAL assertion did not accept the observed `invalid magic number`; incomplete-WAL case not reached. Earlier 7/7 on `8b8c749...` remains scoped to the older probe blob. See `00-governance/reviews/jf10-storage-evidence-assessment.md` §10 and UMR-018.
