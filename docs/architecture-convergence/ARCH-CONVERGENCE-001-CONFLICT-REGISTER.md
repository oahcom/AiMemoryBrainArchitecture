---
document_metadata:
  steward: "Architecture Governance"
  domain: architecture
  role: reference
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Conflict register is a non-normative integration tracker; each status remains subject to its named Owner's closure evidence."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Non-normative architecture conflict inventory and closure tracking"
    canonical_scope_id: "architecture-convergence/arch-convergence-001-conflict-register"
    canonical_scope_keywords:
      - "architecture-convergence"
      - "conflict-register"
      - "closure-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# ARCH-CONVERGENCE-001 — Conflict Register
# ARCH-CONVERGENCE-001 — 架构冲突登记册

- Status: **DRAFT / OPEN REGISTER / NON-NORMATIVE — 2/16 RECONCILED (12.5%); 14 remain OPEN/BLOCKED/CANDIDATE under their accountable Owners**
- Baseline: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Rule: Conflicts remain visible until the authority owning the affected contract resolves them. This register does not decide Owner semantics.

## 1. Active conflicts / 当前冲突

| ID | Conflict | Evidence | Impact | Required owner(s) | Status / closure condition |
|---|---|---|---|---|---|
| CF-001 | README path map vs actual main tree | Main recursive tree has 126 entries; detailed D/E/F/G/H/I/Storage and testing roots absent | Normative source discoverability and implementation traceability | A + each affected Owner | OPEN — approve canonical paths and publish/link exact sources |
| CF-002 | PR #89 says `02-domain-model/` is missing | Main tree and Blob readback confirm six files under `02-domain-model/` | Source inventory in #89 is factually inaccurate | ARCH-CONVERGENCE integration | OPEN — correct report successor; preserve PR #89 as historical draft |
| CF-003 | H path name `08-protocols/` vs Owner path `08-bmcp-protocol/` | README vs H branch tree | Broken references and duplicate/ambiguous protocol root | H + A | OPEN — H confirms canonical path; update portal map under governance |
| CF-004 | I path name `10-security-and-governance/` vs actual Owner contracts under `09-security-governance/` | README, I branch tree; I tree contains both directory names | Ambiguous source of truth and potential duplicate contract copies | I + A | OPEN — identify canonical directory and disposition of alternate path |
| CF-005 | Storage source root absent; Storage artifacts in review namespace | Storage branch tree has 122 blobs but no `09-storage-and-index/`; L1 ADR is under `reviews/storage-consistency/` | Storage contract and ADR authority are hard to discover | Storage + D | OPEN — publish a canonical Storage source index and exact L1/L4 status |
| CF-006 | Fact/Claim canonical semantics conflict | Approved OWNER-DECISION-FACT-CLAIM-001.md (blob 2225dcb469db37dbebe8d8bab202f3ea4f8b600b; approved version 003fa0063e1e359bc91de8c2950366f757bd1210) selects separate Fact attestation / Claim proposition and I1 stable Claim identity with immutable revisions | Semantic/identity conflict is resolved; schema, DDL, API, wire and runtime implementation remain explicitly unfrozen | B + Architecture Governance; D/E/F/G/H consulted | RECONCILED — SEMANTIC/IDENTITY DECISION ONLY; downstream schema/consumer acceptance remains outside this bounded closure |
| CF-007 | D/Storage logical topology vs physical realization | Storage L1 ADR selects Option A; L4 physical engine/deployment OPEN; D record/transaction implementation CANDIDATE | Canonical atomicity cannot be claimed physically | D + Storage | OPEN — exact row ownership, engine/profile, crash/failover/restore evidence |
| CF-008 | Forget local suppression vs global completion | D separates suppression, cleanup and physical erasure; I inventory contract CANDIDATE; D/I/Storage Phase 3.9 PRs #66/#68/#71 remain Draft | A DELETE/ACK cannot prove global Forget terminality | D + I + E/F/G/H/Storage | P0 OPEN — closed-world inventory, barriers, evidence joins and restore proof |
| CF-009 | H branch tree-integrity incident pins do not reconcile | PR #90/#91 cite H `0277a8b...` (7-path incident) and restored `4e65a2...`; fetched live H branch is `6608cde...` (216 blobs) | Cannot infer which H schema/validator/test set is exact current baseline | H + A; C consulted | OPEN — exact commit ancestry, branch ref, tree digest and restoration record |
| CF-010 | C tree-integrity incident vs restored branch | PR #91 cites C `a5dff...` (5-path incident); live C branch `session-c-agent-integration-2026-11-16` is `3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c`; tree `db46a6d75cad94040cd5d5be236ce0c68e0964b8` has 160 entries / 138 blobs, truncated=false; compare from incident is ahead 11 / behind 0 | Source tree currentness is reconciled; C Provider Outcome 19/19 remains bounded evidence and exact tested commit must be pinned | C + A | RECONCILED FOR TREE CURRENTNESS — PR #92 remains open; no end-to-end C/Brain proof |
| CF-011 | G Applied draft vs C/H exact mapping and cross-owner acceptance | G Phase 3.8.22 says G owns Applied but is a design draft; C review says exact COutcomeRecord/final-boundary mapping NOT ACCEPTED/NOT VERIFIED | Cannot claim exact final request was applied | G + C + H + I + D + Storage | P0 OPEN — exact field mapping, identity, persistence and crash recovery acceptance |
| CF-012 | C Provider Outcome vs H wire vs Storage recovery bundle version | CSubmitOutcome 1.0.1 exists; H 1.2.15 exists on branch; Storage v3.3.2 report pin references H 1.2.14; PR #94 schema trigger execution pending | Version skew and CI false negatives can hide broken conformance | C + H + Storage | OPEN — one exact compatible bundle manifest and successful schema-only CI trigger |
| CF-013 | Cedar PDP candidate vs I authorization authority | PRODUCT-FIRST report recommends only a bounded Cedar candidate; no production approval; evaluation errors must fail closed | Product evaluator may accidentally become policy authority or permit on error | I + Security governance | CANDIDATE — wrapper vectors, revocation tests and Owner approval required |
| CF-014 | SQLite local vs PostgreSQL server profile | PRODUCT-FIRST and Storage research leave L4 open; no representative Brain workload or full restore evidence | Cannot freeze storage engine or deployment topology | Storage + D + Engineering | OPEN — workload, atomicity, HA, backup/restore and operational comparison |
| CF-015 | Bilingual reader guides vs detailed normative contract parity | Translation status says multiple detailed Owner sources NOT STARTED; only reader guides are paired | Normative meaning may diverge or be missing in Chinese | All Owners + A | OPEN — per-contract semantic parity and Owner review |
| CF-016 | Product research recommendation vs architecture approval | PR #74–#79 all Open/Draft/Unmerged; PR #89 is non-normative | No product may be treated as approved or as Brain authority | Product research Owners + Architecture Governance | OPEN — exact Owner ADR and measured conformance evidence |

## 2. Priority order / 优先级

1. **P0 source and identity blockers:** CF-001, CF-006, CF-007.
2. **P0 safety blockers:** CF-008, CF-009, CF-011, CF-012.
3. **P1 implementation readiness:** CF-005, CF-010, CF-014, CF-015.
4. **P1 product governance:** CF-013, CF-016.

Priority is an integration planning classification, not a formal Owner severity change.

## 3. Resolution protocol / 冲突解决规则

For every conflict:
1. Identify the exact authority and version that owns the decision.
2. Read the live branch ref and exact Blob; never rely on an old PR body alone.
3. Record the affected downstream consumers and incompatible assumptions.
4. Ask the Owner to accept, reject or amend the proposed resolution on its own branch.
5. Require bilingual semantic parity for normative changes.
6. Require executable acceptance tests for state, concurrency, crash, retry, authorization, Forget and restore claims.
7. Preserve unresolved alternatives; do not resolve by silently copying a candidate into main.
8. Update this register only with evidence and exact commit/PR pins.

## 4. Explicit non-resolutions / 明确不作出的决定

- No Fact/Claim model is selected.
- No physical database engine or deployment profile is selected.
- No new global Forget state machine is approved.
- No Cedar/OPA/OpenFGA production selection is made.
- No H/C/G Applied wire mapping is frozen.
- No external memory product is granted Canonical Truth, Evidence, Authorization, Forget, Lifecycle or Applied authority.
- No implementation or production activation is authorized.

All conflicts remain OPEN unless the closure evidence above is supplied by the accountable Owner and governance process.


## 5. W10 closure review — 2026-11-27 (AID-2026-253)

This review applies each row's existing closure condition literally. It does not substitute evidence of discussion, product maturity, or a candidate recommendation for the accountable Owner's required decision and acceptance evidence. The register remains DRAFT and NON-NORMATIVE.

| ID | Prior status | W10 status | Missing closure evidence / accountable completion |
|---|---|---|---|
| CF-001 | OPEN | OPEN | A and each affected Owner must approve canonical paths and publish/link exact source documents. Missing: approved path map and per-owner source pins. |
| CF-002 | OPEN | OPEN | ARCH-CONVERGENCE integration must publish a correction successor to the inaccurate PR #89 report while retaining #89 as historical draft. Missing: correction artifact and exact main-tree/blob readback. |
| CF-003 | OPEN | OPEN | H must confirm the canonical path and A must update the governance portal map. Missing: H confirmation and committed portal-map correction. |
| CF-004 | OPEN | OPEN | I must identify the canonical directory and disposition alternate copies. Missing: explicit I decision and disposition/readback for the alternate directory. |
| CF-005 | OPEN | OPEN | Storage must publish a canonical source index and exact L1/L4 status. Missing: accepted index and exact source/version/status pins. |
| CF-006 | ADR-BLOCKED | RECONCILED — SEMANTIC/IDENTITY DECISION ONLY | Approved OWNER-DECISION-FACT-CLAIM-001.md on main, blob 2225dcb469db37dbebe8d8bab202f3ea4f8b600b, approved version 003fa0063e1e359bc91de8c2950366f757bd1210; Owner delegation instrument is Issue #305 comment 7042461592. Schema, DDL, API, wire and runtime implementation remain expressly unfrozen. |
| CF-007 | OPEN | OPEN | D and Storage must settle row ownership, physical engine/profile and supply crash/failover/restore evidence. Missing: accepted topology and executable recovery evidence. |
| CF-008 | P0 OPEN | P0 OPEN | D/I/Storage must supply closed-world inventory, barriers, evidence joins and restore proof. Missing: accepted inventory and end-to-end Forget/restore evidence. |
| CF-009 | OPEN | OPEN | H and A must pin exact ancestry, live branch ref, tree digest and restoration record. Missing: complete reproducible incident-to-restoration chain. |
| CF-010 | RECONCILED FOR TREE CURRENTNESS | RECONCILED FOR TREE CURRENTNESS | Re-verified live C branch `session-c-agent-integration-2026-11-16` at `3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c`; tree `db46a6d75cad94040cd5d5be236ce0c68e0964b8` returned 160 entries / 138 blobs / truncated=false; compare from incident returned ahead=11, behind=0, merge-base=incident. This is tree-currentness only; Provider Outcome 19/19, exact tested-commit pinning and end-to-end C/Brain proof remain outside this reconciliation. |
| CF-011 | P0 OPEN | P0 OPEN | G/C/H/I/D/Storage must accept exact field mapping, identity, persistence and crash recovery. Missing: complete mapping and acceptance tests. |
| CF-012 | OPEN | OPEN | C/H/Storage must publish one exact compatible bundle manifest and trigger successful schema-only CI on that bundle. Missing: pinned manifest and successful exact-bundle run. |
| CF-013 | CANDIDATE | CANDIDATE | I must accept the Cedar wrapper, fail-closed vectors and revocation tests. Missing: version-pinned wrapper vectors, revocation evidence and explicit I approval. |
| CF-014 | OPEN | OPEN | Storage/D/Engineering must provide representative workload, atomicity, HA, backup/restore and operational comparison. Missing: reproducible workload results and accepted physical-profile comparison. |
| CF-015 | OPEN | OPEN | All Owners must complete per-contract bilingual semantic parity and review. Missing: complete contract-by-contract parity evidence and Owner review. |
| CF-016 | OPEN | OPEN | Product research Owners and Architecture Governance must issue exact Owner ADRs and measured conformance evidence. Missing: approved ADRs and reproducible conformance results. |

### W10 reconciliation accounting

- RECONCILED: 2/16 (12.5%): CF-006 semantic/identity decision only; CF-010 tree currentness only.
- Unresolved: 14/16. The accountable Owners and missing evidence are listed above.
- CF-006 meets its own bounded closure condition because an approved Owner-delegated semantic/identity decision is present on main. Its downstream schema/consumer implementation remains explicitly unfrozen and is not included in this reconciliation.
- The pre-existing CF-010 evidence is retained as recorded in §1. This review does not claim a fresh shell command/output for it; no unexecuted command is represented as measured output.


### CF-006 reproducible evidence anchor

- GitHub API: GET /repos/oahcom/AiMemoryBrainArchitecture/contents/14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md?ref=main
- Observed blob SHA: 2225dcb469db37dbebe8d8bab202f3ea4f8b600b
- Metadata: decision_status=Approved; approved_version=003fa0063e1e359bc91de8c2950366f757bd1210
- Authority evidence: GET /repos/oahcom/AiMemoryBrainArchitecture/issues/comments/7042461592; comment authored by repository Owner (OWNER association), establishing the delegation instrument.
- Bounded result: Fact/Claim semantic and identity decision reconciled. Schema, DDL, public API, BMCP wire and runtime implementation remain outside this closure.


### CF-010 reproducible evidence anchor

- GET /repos/oahcom/AiMemoryBrainArchitecture/branches/session-c-agent-integration-2026-11-16
  - commit.sha = 3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c
  - commit.commit.tree.sha = db46a6d75cad94040cd5d5be236ce0c68e0964b8
- GET /repos/oahcom/AiMemoryBrainArchitecture/git/trees/db46a6d75cad94040cd5d5be236ce0c68e0964b8?recursive=1
  - truncated=false; tree.length=160; blob count=138
- Compare incident a5dff993e5c2928a28deb777c41023cfe923366f to live C branch head 3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c
  - ahead_by=11; behind_by=0; merge_base=incident commit
