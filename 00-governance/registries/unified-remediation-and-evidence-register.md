# Unified A–I Remediation & Evidence Register

- Register ID: P-UNIFIED-MBR-REMEDIATION-001
- Date: 2026-11-17
- Status: **OPEN — coordination register; no Owner decision is inferred**
- Authority: Session P records dependencies and evidence. Module Owners retain their own decisions; I retains security/governance authority; Storage retains physical realization; designated ADR/Governance authority retains project-level decisions.

## 1. Priority actions

| ID | Priority | Work item | Accountable authority | Current state | Closure evidence |
|---|---|---|---|---|---|
| UMR-001 | P0 | Common CGH-APPLIED-1.1 package/schema freeze and executable closure | C, G, H jointly; I/D/B predicate authorities; A records | Exact A package 4961... + COC companion fc3... decisions recorded: C/D/G/H/I ACCEPT WITH EXCEPTIONS; B APPROVE; Storage CONFIRMED WITH CHANGES — interface only. H schema remains candidate/not frozen; COC deployment and runtime tests open | Freeze requires H complete production schema/crypto/compatibility evidence, named/deployed COC, I/D/C/G runtime binding, owner-authoritative tests and conformance; see applied-contract-1.1-exact-version-reconciliation.md |
| UMR-002 | P0 | JF-10 v2 production adapter binding and recovery | Storage engineering + D/E; I for authorization/sequencer | PostgreSQL 18.7 enhanced PITR probe and all six supporting workflows now PASS 7/7 on tested commit 2d476...; current branch e6e... retains identical tested probe blob; production runtime/adapter NOT IDENTIFIED; Gate A PARTIAL PASS / OPEN | Canonical runtime repo/branch, adapter/schema/build SHA; real I/D/E transaction mapping; production-equivalent fault/failover/PITR; real fencing, operator/runbook and RPO/RTO |
| UMR-003 | P0 | Formal ADR-001 Fact/Claim decision | Designated ADR/Architecture Governance authority; B owns domain recommendation | ADR-BLOCKED | Exact selected option, rationale, approver authority, timestamp, version, migration and affected-consumer acceptance |
| UMR-004 | P0 | I security policy and Global Forget governance | I + named external governance approvers | GOVERNANCE-BLOCKED | I35-DEC/I36-GOV approved exact versions; signed inventory seal; target-state mapping; external recipient/backup/restore evidence; exception decisions |
| UMR-005 | P1 | B/I/H typed identity + permission binding | B, I, H; consumers C/D/E/F/G/Storage | OPEN / PARTIAL DESIGN | Exact typed fields and trust chain, transport authentication binding, permission/epoch mapping, forged identity and stale/revoked negative tests, consumer acceptance |
| UMR-006 | P1 | Owner baseline adoption and current evidence pins | Each A–I Owner; A tracks | All nine module proposals PROPOSED; no module baseline adoption recorded by this review | Owner-specific ADOPT / ADOPT WITH EXCEPTIONS / REVISE / REJECT record, proposal version, current HEAD, artifact blob SHA and affected-consumer acceptance |
| UMR-007 | P1 | Baseline template applicability and structural normalization | Project Governance Authority / P until appointed | P template exists; not in main; governance not ratified | Exact template version adoption or approved replacement; each Owner maps all required sections and records deviations |
| UMR-008 | P1 | Refresh technical-review / integration source HEAD provenance | A/C/F/G/H; B/D/E/I review coverage to be decided | TAB-001 reports B/C/F/G/H/I present; A/D/E missing. A Phase 3.6 closure tracker §13.43 and A context integration source pins are stale against current Owner HEADs | Refresh each report to current source HEAD/artifact blobs; distinguish exact Owner decision from implementation/test/deployment status; A to refresh closure tracker and gate vector |
| UMR-009 | P1 | TAB-001 Owner technology review coverage for A/D/E | A/D/E Owners; A coordinates | Six reports present: B, C, F, G, H, I. A, D, E assigned reports remain missing. B/I reports state centralized delegated review, not independent human Owner attestation. | A/D/E publish owner-specific reviews at exact task-pack paths; refresh all report source HEADs/blueprint SHA and preserve the delegated-review caveat for B/I |
| UMR-010 | P1 | Inspect PostgreSQL 18.7 capability probe workflow evidence | Storage Owner / CI operator | PR #12 closed; description limits evidence to single-node probe and disclaims production/failover proof; run result not yet verified here | CLOSED for pinned PostgreSQL 18.7 CI capability profile; retain production non-claims and link exact run/job/log pins in jf10-storage-evidence-assessment.md |
| UMR-011 | P2 | Normalize document structure to 14-section template | Each Owner; governance template authority | A has 13 sections; B/C/G/H/I 14; D/E/F 15; template only on P | Owner-confirmed section map, distinct Evidence & Version History, deviations justified |
| UMR-012 | P2 | Central gate vector and registry synchronization | A; P maintains governance rollout record | Tracking registry stale at review start | Current branch HEADs and artifact SHAs, owner decisions, cross-owner acceptances, governance, implementation and tests tracked independently |


| UMR-013 | P0 | SQLite/PostgreSQL transaction-profile decision for JF-10 | D/E/Storage; I for policy/sequencer | PostgreSQL 18.7 native prepared-XID and enhanced CI profile now pass 7/7; stronger direct evidence than SQLite WAL for prepared participant semantics; no final DB selection | Bind engine capability to production runtime/adapter and operational profile; if SQLite retained, specify/prove an alternate durable participant protocol; keep TEC-003/004 OPEN pending Owner/ADR decision |
| UMR-014 | P1 | Integrate G/F NVIDIA context-optimization and observation-archive research with TAB-001 | A coordinates; F/G own proposals; B/C/D/E/H/I/Storage consulted | A system integration review now defines F-owned Observation Archive + G-owned Context projection, no new service; F/G candidates remain PROPOSED and all cross-owner acceptances pending | Exact F/G Recall contract and owner approvals; classify archive producer/retention; map TSS/ObservationRef/compaction/fidelity/lineage/Forget to B-I/Storage; then run paired benchmarks and negative tests |
| UMR-015 | P1 | Reconcile P/main branch divergence before any future integration | P coordinator + A; project governance authority when appointed | P is ahead 30 / behind 4 against main; main contains TAB-001 blueprint, task pack and roadmap update | Reviewed non-destructive reconciliation of four main-side files, fresh compare, no force update and no merge without explicit authorization |


| UMR-016 | P0 | Bind PostgreSQL capability suite to canonical runtime implementation | Storage engineering + D/E/I; A coordinates | Storage dossier confirms no production runtime/Canonical Authority DB adapter/migration package in inspected repo branch; CI fixtures use isolated jf10_* tables | Identify canonical runtime repository/branch and exact adapter/schema/build SHA; map I sequencer, D fence, E publication, pointer/receipt/outbox and real reader path; run production-equivalent suite |


| UMR-017 | P1 | Refresh A Phase 3.6 closure tracking after current exact decisions and Storage regression | A Owner; P records discrepancy only | A closure tracker blob 554d4b85... still records older Storage HEAD df60... and failed deep PITR; live Storage HEAD 3c8ab8... now records corrected deep PITR and 7/7 regression pass; C/G/D/H/I/B exact 1.1 decisions and Storage interface confirmation are present on live branches | A re-fetch exact current C/G/D/H/I/B/Storage branch artifacts and current Storage dossier, update exact blob/HEAD pins and gate vector; preserve Gate A PARTIAL PASS / OPEN due no production runtime/adapter, operator, COC deployment, RPO/RTO and I/D integration |


| UMR-018 | P0 | Fix and rerun enhanced JF-10 PITR exact-WAL negative campaign | Storage Owner | CLOSED for tested code: probe blob 9d2a85... and seven-workflow batch 7/7 PASS on commit 2d476...; current branch e6e... retains identical probe blob | Preserve passing assertions; any probe change requires rerun; Gate A still open for production runtime/adapter, I/D integration, COC deployment and operations |


| UMR-019 | P1 | Freeze F/G Observation Archive ↔ Context Recall contract | F/G jointly; B/C/D/E/H/I/Storage accept their own dependencies; A records | A system review selects F-owned Runtime Archive + G-owned Context projection and rejects a new service now; F/G research candidates are PROPOSED; F/G module baseline proposals do not yet mention Archive/TSS/fidelity/lineage; A decision register says same-version cross-owner acceptances pending | Joint exact-version RecallIntent/ObservationRecallResult, ArchiveLocator vs ContextObservationReference, cursor/receipt/completeness, source revision, TSS/ContextVersion and retention/Forget semantics; exact Owner decisions on each branch |
| UMR-020 | P1 | Execute Context Optimization conformance plan after contract and implementation readiness | A test governance; F/G primary; C/D/E/H/I/Storage supporting | Plan blob 1c941c... is PROPOSED / NOT RUN; tests specified for archive capture/recall, cursor/EOF, Forget races, restore, cache, compaction fidelity, permissions, benchmarks | Pinned implementation/build; test ownership, seed/config/hardware/model; nominal/negative/concurrency/recovery suite; zero leakage/false completeness/epistemic upgrade; paired held-out performance evidence |


| UMR-021 | P1 | Align F/G module baseline proposals with new Archive/TSS research candidates | F/G Owners; A coordinates; B/C/D/E/H/I/Storage review affected interfaces | F baseline proposal blob d4756c... and G baseline proposal blob fb2eb8... predate the new work and contain none of Observation Archive/ArchiveLocator/RecallSession or TSS/ContextObservationReference/compaction/fidelity terms | F/G publish revised PROPOSED baseline addenda on their own branches with exact owner-scoped boundaries, cross-owner dependencies and explicit OPEN/TO_VALIDATE statuses; then request exact consumer acceptance |

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
| JF-10 P0 | OPEN — Gate A PARTIAL PASS | Current enhanced PITR + six supporting workflows pass 7/7 on pinned PostgreSQL CI profile; production adapter/runtime binding, I/D/E integration, COC deployment, real fencing and operations remain unverified |
| Global Forget | GOVERNANCE-BLOCKED | I approvals, sealed inventory and target-state evidence incomplete |
| JF-10 PostgreSQL 18.7 CI evidence | PASS — current enhanced probe batch 7/7 | Probe blob 9d2a85... tested on commit 2d476...; current Storage HEAD e6e... retains identical probe blob. Engine fixtures only; no production runtime/adapter or end-to-end JF-10 conformance |
| TAB-001 Owner technology review | 6/9 reports present; 3/9 missing | B/C/F/G/H/I reports present; A/D/E missing. B/I reviews are delegated assistant reviews, not independent human-Owner attestations |
| Project G0 / architecture freeze | GOVERNANCE-OPEN / NOT AUTHORIZED | No PGA appointment or exact G0 approval evidenced |
| Production implementation/test sign-off | NOT VERIFIED / NOT RUN where applicable | No general end-to-end implementation and conformance evidence |

## 4. Operating sequence

1. Close UMR-001, UMR-003 and UMR-005 at the exact contract/ADR level without conflating their authority.
2. Preserve UMR-018 PASS; bind the PostgreSQL capability suite to the actual runtime under UMR-016; decide the SQLite alternative under UMR-013 only after exact JF-10 invariants are mapped.
3. Advance UMR-019/021 exact F/G Archive–Context contract and baseline alignment; run UMR-020 only after Owner acceptances and an implementation build exist.
4. Have A refresh stale Phase 3.6 and context-integration source pins under UMR-017; P cannot rewrite A's Owner record.
5. Close UMR-002 and UMR-004 with real Storage and I implementation/governance evidence.
6. Obtain each Owner's exact-version baseline disposition under UMR-006 and normalize documents/review coverage under UMR-007/008/009/011.
7. A publishes an updated integration gate vector; P updates project tracking.
8. Only a formally appointed Project Governance Authority may ratify G0 or authorize a project-wide architecture freeze.

## 5. Change log

- 2026-11-17: Initial unified register prepared from live A–I branch reads, current baseline artifact blobs, A Phase 3.6 closure tracking, D JF-10 bounded acceptance and Storage PR #12 metadata.

- 2026-11-17 addendum: reconciled current TAB-001 v0.1 and A–I technology-review task pack. Main HEAD `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f`; TAB-001 blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`; task pack blob `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`. G research blobs `3fb9f011e24c93a748442018d48c5954584e4f43` and `eadefd4e0fe541ef8479a030a2a99a0d57dbcf8b`. P/main divergence: ahead 30 / behind 4.

- 2026-11-17 JF-10 evidence reconciliation: Storage branch `a1fbbd15d3a7993bbb61821ad44957e4f69d3ed1`, dossier blob `2f76ca8b8c19b84c37e7604cd254990dd93eb8b1`. Seven PostgreSQL 18.7 CI workflows succeeded on commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`; see `00-governance/reviews/jf10-storage-evidence-assessment.md`. Gate A is PARTIAL PASS / OPEN, not closed.

- 2026-11-17 Applied correction: live C/D/G/H/I exact-version decision artifacts and B type approval all pin A package `4961ffefc0f9920efb8425a9b2a7af42d8f64819` plus COC companion `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`; Storage confirms interface only. Applied freeze remains blocked by H candidate schema/deployment, COC operator, runtime implementation and conformance. See `applied-contract-1.1-exact-version-reconciliation.md`.
- 2026-11-17 A source freshness: A closure tracker blob `554d4b85a94f433856506dce4c020b9c00183e69` ends at §13.43 and records old Storage head `df60b547...` / failed PITR; current Storage head is `3c8ab8ee4579a550300aa48aecab928149cf9370` with corrected seven-workflow regression pass. Gate A remains PARTIAL PASS / OPEN because production runtime/adapter, I/D integration, COC deployment/operator and operations remain unverified.

- 2026-11-17 current Storage regression: Storage HEAD `3c8ab8ee4579a550300aa48aecab928149cf9370`, enhanced PITR probe blob `7fa4bb3fb07eacc3f708f5682ea4c9e2019f267d`. Current branch batch: six workflows PASS, PITR run `43957456225` FAILURE because corrupt-WAL assertion did not accept the observed `invalid magic number`; incomplete-WAL case not reached. Earlier 7/7 on `8b8c749...` remains scoped to the older probe blob. See `00-governance/reviews/jf10-storage-evidence-assessment.md` §10 and UMR-018.

- 2026-11-17 Storage correction: current branch HEAD `e6e578766b081b6d450d6af7fc4d6d673f8afd53`; current probe blob `9d2a85f9a5d53f91df247a310c38377e563d259d`; run `43957910909` SUCCESS; seven-workflow batch on `2d476dd32ac020d329e8290ee2aaaa1f0c057c92` 7/7 PASS. Current branch is three commits ahead with docs only; same probe blob. UMR-018 closed for this tested revision; Gate A still PARTIAL PASS / OPEN.
- 2026-11-17 TAB-001 report coverage: B/C/F/G/H/I present (six); A/D/E missing. B and I reports explicitly say centralized delegated review, not independent human-owner attestation.
- 2026-11-17 Context Optimization integration: A review blob `b53db1ecb7830a7f1057d09c8ef73aceab942cea` chooses F-owned Observation Archive + G-owned Context projection, no independent service; F/G candidates remain PROPOSED and cross-owner approvals pending. A conformance plan blob `1c941c3e55be1e539a76ef89f297c168296c7db2` is NOT RUN.

- 2026-11-17 Owner proposal inventory refreshed: all nine A–I branches contain baseline/redlines proposals, all PROPOSED / not APPROVED. Exact paths and blob SHAs are recorded in the central tracking file. A 13 sections; B/C/G/H/I 14; D/E/F 15. The canonical P template is not on main; proposals record that template gap and are not treated as template-compliant approvals.
- 2026-11-17 TAB-001 review coverage: B/C/F/G/H/I reports present (6/9); A/D/E missing. B and I reports are centralized delegated reviews, not independent human Owner attestations.
- 2026-11-17 F/G baseline alignment gap: F and G proposal files contain no Archive/Recall/TSS/fidelity/lineage concepts despite new research and A integration candidate. UMR-021 requires Owner-authored proposal addenda.
