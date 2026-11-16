# Unified A–I Remediation & Evidence Register

- Register ID: P-UNIFIED-MBR-REMEDIATION-001
- Date: 2026-11-17
- Status: **OPEN — coordination register; no Owner decision is inferred**
- Authority: Session P records dependencies and evidence. Module Owners retain their own decisions; I retains security/governance authority; Storage retains physical realization; designated ADR/Governance authority retains project-level decisions.

## 1. Priority actions

| ID | Priority | Work item | Accountable authority | Current state | Closure evidence |
|---|---|---|---|---|---|
| UMR-001 | P0 | Common C/G/H Applied contract version/digest | C, G, H jointly; I/D/B predicate authorities | OPEN / NOT FROZEN | One canonical schema artifact, exact version + SHA-256, field ownership map, C/G/H exact-version acceptance, I/D/B predicate confirmation, verifier and negative tests |
| UMR-002 | P0 | JF-10 v2 physical atomicity and recovery | Storage engineering + D/E; I for authorization/sequencer | D architecture ACCEPT WITH ENUMERATED EXCEPTIONS; engineering OPEN | Named DB/platform and accountable operator; prepared-XID/lock retention; same-XID restart/failover; atomic visibility pointer + receipt; PITR/restore and crash/fault evidence |
| UMR-003 | P0 | Formal ADR-001 Fact/Claim decision | Designated ADR/Architecture Governance authority; B owns domain recommendation | ADR-BLOCKED | Exact selected option, rationale, approver authority, timestamp, version, migration and affected-consumer acceptance |
| UMR-004 | P0 | I security policy and Global Forget governance | I + named external governance approvers | GOVERNANCE-BLOCKED | I35-DEC/I36-GOV approved exact versions; signed inventory seal; target-state mapping; external recipient/backup/restore evidence; exception decisions |
| UMR-005 | P1 | B/I/H typed identity + permission binding | B, I, H; consumers C/D/E/F/G/Storage | OPEN / PARTIAL DESIGN | Exact typed fields and trust chain, transport authentication binding, permission/epoch mapping, forged identity and stale/revoked negative tests, consumer acceptance |
| UMR-006 | P1 | Owner baseline adoption and current evidence pins | Each A–I Owner; A tracks | All nine module proposals PROPOSED; no module baseline adoption recorded by this review | Owner-specific ADOPT / ADOPT WITH EXCEPTIONS / REVISE / REJECT record, proposal version, current HEAD, artifact blob SHA and affected-consumer acceptance |
| UMR-007 | P1 | Baseline template applicability and structural normalization | Project Governance Authority / P until appointed | P template exists; not in main; governance not ratified | Exact template version adoption or approved replacement; each Owner maps all required sections and records deviations |
| UMR-008 | P1 | Refresh technical-review source HEAD provenance | C/F/G/H; A records; B/D/E/I review coverage to be decided | Existing reports are static conditional; source HEADs are pre-publication snapshots | Reviewed source HEAD, report publication commit, artifact blob SHA, and explicit statement whether newer changes alter findings |
| UMR-009 | P1 | Technology review coverage for B/D/E/I | B/D/E/I Owners; A coordinates scope | No separate TAR-AI-001 report located in inspected current artifacts | Owner-specific review or explicit scope rationale; six dimensions, dependency/failure/recovery, resource limits, interface compatibility and evidence-based verdict |
| UMR-010 | P1 | Inspect PostgreSQL 18.7 capability probe workflow evidence | Storage Owner / CI operator | PR #12 closed; description limits evidence to single-node probe and disclaims production/failover proof; run result not yet verified here | Workflow run URL, commit/build SHA, exact job/test result and logs; preserve non-claims for replication, production restore, hardware durability and operator readiness |
| UMR-011 | P2 | Normalize document structure to 14-section template | Each Owner; governance template authority | A has 13 sections; B/C/G/H/I 14; D/E/F 15; template only on P | Owner-confirmed section map, distinct Evidence & Version History, deviations justified |
| UMR-012 | P2 | Central gate vector and registry synchronization | A; P maintains governance rollout record | Tracking registry stale at review start | Current branch HEADs and artifact SHAs, owner decisions, cross-owner acceptances, governance, implementation and tests tracked independently |

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
| Common Applied freeze | BLOCKED | No common C/G/H version/digest + exact acceptance |
| ADR-001 | ADR-BLOCKED | No formal decision record |
| JF-10 P0 | OPEN | Storage engineering/recovery and I authority evidence incomplete |
| Global Forget | GOVERNANCE-BLOCKED | I approvals, sealed inventory and target-state evidence incomplete |
| Project G0 / architecture freeze | GOVERNANCE-OPEN / NOT AUTHORIZED | No PGA appointment or exact G0 approval evidenced |
| Production implementation/test sign-off | NOT VERIFIED / NOT RUN where applicable | No general end-to-end implementation and conformance evidence |

## 4. Operating sequence

1. Close UMR-001, UMR-003 and UMR-005 at the exact contract/ADR level without conflating their authority.
2. Close UMR-002 and UMR-004 with real Storage and I evidence.
3. Obtain each Owner's exact-version baseline disposition under UMR-006.
4. Normalize the documents and review coverage under UMR-007/008/009/011.
5. A publishes an updated integration gate vector; P updates project tracking.
6. Only a formally appointed Project Governance Authority may ratify G0 or authorize a project-wide architecture freeze.

## 5. Change log

- 2026-11-17: Initial unified register prepared from live A–I branch reads, current baseline artifact blobs, A Phase 3.6 closure tracking, D JF-10 bounded acceptance and Storage PR #12 metadata.
