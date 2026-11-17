# ARCH-CONVERGENCE-001 — Conflict Register
# ARCH-CONVERGENCE-001 — 架构冲突登记册

- Status: **DRAFT / OPEN REGISTER / NON-NORMATIVE**
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
| CF-006 | Fact/Claim canonical semantics conflict | Main I-04/P-04 distinction vs Domain Overview §5; B ADR-001 says ADR-BLOCKED; D Store also blocks persistence | Identity, revision, evidence, schema and consumer contracts cannot be frozen | B + Architecture Governance; D/E/F/G/H consulted | ADR-BLOCKED — explicit governance decision required |
| CF-007 | D/Storage logical topology vs physical realization | Storage L1 ADR selects Option A; L4 physical engine/deployment OPEN; D record/transaction implementation CANDIDATE | Canonical atomicity cannot be claimed physically | D + Storage | OPEN — exact row ownership, engine/profile, crash/failover/restore evidence |
| CF-008 | Forget local suppression vs global completion | D separates suppression, cleanup and physical erasure; I inventory contract CANDIDATE; D/I/Storage Phase 3.9 PRs #66/#68/#71 remain Draft | A DELETE/ACK cannot prove global Forget terminality | D + I + E/F/G/H/Storage | P0 OPEN — closed-world inventory, barriers, evidence joins and restore proof |
| CF-009 | H branch tree-integrity incident pins do not reconcile | PR #90/#91 cite H `0277a8b...` (7-path incident) and restored `4e65a2...`; fetched live H branch is `6608cde...` (216 blobs) | Cannot infer which H schema/validator/test set is exact current baseline | H + A; C consulted | OPEN — exact commit ancestry, branch ref, tree digest and restoration record |
| CF-010 | C tree-integrity incident vs restored branch | PR #91 cites C `a5dff...` (5-path incident); live C branch `88992da...` is one commit ahead and its recursive tree has 136 blobs | Source tree currentness is reconciled; C Provider Outcome 19/19 remains bounded evidence and exact tested commit must be pinned | C + A | RECONCILED FOR TREE CURRENTNESS — PR #92 remains open; no end-to-end C/Brain proof |
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
