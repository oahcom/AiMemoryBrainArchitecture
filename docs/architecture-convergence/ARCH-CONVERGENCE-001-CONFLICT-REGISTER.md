---
document_metadata:
  domain: architecture
  role: review-report
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-253/evidence.md"
        - "AID-2026-253 delegated reassessment"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Status ratio and two bounded reconciliations were rechecked against live main and live Owner branch refs by AID-2026-253; remaining closure evidence is listed per row."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# ARCH-CONVERGENCE-001 — Conflict Register
# ARCH-CONVERGENCE-001 — 架构冲突登记册

- Status: **DRAFT / OPEN REGISTER / NON-NORMATIVE — 2/16 RECONCILED (12.5%); 14 REMAIN OPEN / BLOCKED / CANDIDATE**
- Baseline: main@f18adc9fa1d06837433a09498f5297bf13b35756
- Rule: Conflicts remain visible until the authority owning the affected contract resolves them. This register does not decide Owner semantics.
- Reassessment: AID-2026-253 (2026-11-27), proxy ruling, not a natural-person Owner signature. CF-006 is reconciled for semantic/identity decision only; CF-010 remains reconciled for tree currentness only. Four maturity dispositions are recorded in docs/en/13-engineering-decisions/REQ04-MATURE-IMPLEMENTATION-DISPOSITIONS-001.md and its Chinese counterpart.

## 1. Active conflicts / 当前冲突

| ID | Conflict | Evidence | Impact | Required owner(s) | Status / closure condition |
|---|---|---|---|---|---|
| CF-001 | README path map vs actual main tree | Live main tree now contains subsystem roots, but exact canonical path approvals and governed portal links are not evidenced | Normative source discoverability and implementation traceability | A + each affected Owner | OPEN — approve canonical paths and publish/link exact sources |
| CF-002 | PR #89 says 02-domain-model/ is missing | Currentness addendum corrects the false absence claim; live PR #89 is now merged, not Open/Draft | Source inventory in #89 is factually inaccurate | ARCH-CONVERGENCE integration | OPEN — corrected successor exists, but “preserve PR #89 as historical draft” is not literally met because PR #89 is merged; record explicit governance disposition without rewriting PR history |
| CF-003 | H path name 08-protocols/ vs Owner path 08-bmcp-protocol/ | Main contains 08-bmcp-protocol/; docs/README.md does not link this root; no current H canonical-path approval is pinned | Broken references and duplicate/ambiguous protocol root | H + A | OPEN — H confirms canonical path; update portal map under governance |
| CF-004 | I path name 10-security-and-governance/ vs actual Owner contracts under 09-security-governance/ | Main contains 09-security-governance/; its index remains Draft and does not disposition the alternate path/copies | Ambiguous source of truth and potential duplicate contract copies | I + A | OPEN — identify canonical directory and disposition of alternate path |
| CF-005 | Storage source root absent; Storage artifacts in review namespace | Main contains 10-storage-consistency/, but no root README/index was found; L4 remains unselected | Storage contract and ADR authority are hard to discover | Storage + D | OPEN — publish a canonical Storage source index and exact L1/L4 status |
| CF-006 | Fact/Claim canonical semantics conflict | Approved OWNER-DECISION-FACT-CLAIM-001.md selects separate Fact/Claim semantics and I1 stable Claim identity / immutable revisions; explicitly excludes schema, DDL, API, wire and runtime freeze | Identity/revision semantic ambiguity is resolved; downstream schema/consumer contracts remain bounded and unfrozen | B + Architecture Governance; D/E/F/G/H consulted | RECONCILED — SEMANTIC/IDENTITY DECISION ONLY; schema/wire/persistence/consumer acceptance remains outside this closure |
| CF-007 | D/Storage logical topology vs physical realization | SQLite reference crates/tests exist; ADR-RUN-001 remains PROPOSED and disclaims deployment/recovery validation | Canonical atomicity cannot be claimed physically | D + Storage | OPEN — exact row ownership, engine/profile, crash/failover/restore evidence |
| CF-008 | Forget local suppression vs global completion | I source README says restored contracts remain Draft/Informative; G package says global Applied/Forget and crash/restore are not frozen/verified | A DELETE/ACK cannot prove global Forget terminality | D + I + E/F/G/H/Storage | P0 OPEN — closed-world inventory, barriers, evidence joins and restore proof |
| CF-009 | H branch tree-integrity incident pins do not reconcile | Live H branch session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74; tree a03964fc62dea1b7eb50dafdec6adc5d0795fa0e (282 entries / 249 blobs); incident 0277a8b9ee63be850acc0b8b1b08625524aaa33 is an ancestor of current head | Cannot infer restoration integrity from tree size alone while ancestry narrative conflicts | H + A; C consulted | OPEN — exact commit ancestry, branch ref, tree digest and consistent restoration record |
| CF-010 | C tree-integrity incident vs restored branch | Live C branch session-c-agent-integration-2026-11-16 @ 3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c; tree db46a6d75cad94040cd5d5be236ce0c68e0964b8 (160 entries / 138 blobs); incident-to-head compare is ahead 11 / behind 0 | Source tree currentness is reconciled; bounded Provider Outcome evidence is not C/Brain end-to-end proof | C + A | RECONCILED FOR TREE CURRENTNESS — no end-to-end C/Brain proof |
| CF-011 | G Applied draft vs C/H exact mapping and cross-owner acceptance | Main G README says Phase 3.8.22 is design draft, implementation NOT VERIFIED, crash/restart/restore tests NOT RUN, C/G/H Applied freeze NO | Cannot claim exact final request was applied | G + C + H + I + D + Storage | P0 OPEN — exact field mapping, identity, persistence and crash recovery acceptance |
| CF-012 | C Provider Outcome vs H wire vs Storage recovery bundle version | PR #94 merged; schema-only trigger and schema restore workflow runs are recorded SUCCESS, but no one exact compatible C/H/Storage bundle manifest is evidenced | Version skew can still hide broken conformance | C + H + Storage | OPEN — one exact compatible bundle manifest and successful schema-only CI trigger |
| CF-013 | Cedar PDP candidate vs I authorization authority | AID-2026-253 decision record DEFERs production Cedar; wrapper/revocation evidence and I/Security approval absent | Product evaluator may accidentally become policy authority or permit on error | I + Security governance | CANDIDATE — wrapper vectors, revocation tests and Owner approval required |
| CF-014 | SQLite local vs PostgreSQL server profile | AID-2026-253 DEFERs both final L4 profiles; no representative Brain workload or complete comparative HA/restore evidence | Cannot freeze storage engine or deployment topology | Storage + D + Engineering | OPEN — workload, atomicity, HA, backup/restore and operational comparison |
| CF-015 | Bilingual reader guides vs detailed normative contract parity | Multiple roots have bilingual companions, but E README records detailed Owner sources whose full bilingual companions remain pending | Normative meaning may diverge or be missing in Chinese | All Owners + A | OPEN — per-contract semantic parity and Owner review |
| CF-016 | Product research recommendation vs architecture approval | PRs #74–#79 and #89 are merged research publications; main README says product-level runtime has not started and production validation is not established | No product may be treated as approved or as Brain authority | Product research Owners + Architecture Governance | OPEN — exact Owner ADR and measured conformance evidence |

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

- No Fact/Claim schema, DDL, public API or wire contract is frozen by the semantic decision.
- No physical database engine or deployment profile is selected.
- No new global Forget state machine is approved.
- No Cedar/OPA/OpenFGA production selection is made.
- No H/C/G Applied wire mapping is frozen.
- No external memory product is granted Canonical Truth, Evidence, Authorization, Forget, Lifecycle or Applied authority.
- No implementation or production activation is authorized.
