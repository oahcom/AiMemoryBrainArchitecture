---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "New AID registration prompt; no implementation or independent review has occurred."
    usage_status: Active
    modification_status: Unchanged
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

# AID-2026-082 — Automated architecture-governance traceability checks

## Purpose

Implement two read-only documentation checks in a separate Draft PR. This work item does not modify PR #1221, Runtime/product code, domain semantics, schemas, API/DDL, or the semantics of any existing validator.

## Check A — Owner namespace anti-confusion (#1196)

Scan the canonical root, `docs/en`, and `docs/zh-CN` versions of Component Map and Responsibility Matrix, plus the architecture diagrams and references registered as in-scope.

Requirements:
- Formal accountability references use `Owner A` through `Owner I`.
- Logical subsystem references use `SYS-*` identifiers.
- Capability/component labels and P/S markers are not Owner identifiers.
- Reject bare A–I references when used as accountability claims, subsystem IDs, or capability-to-Owner assignments without explicit qualification.
- Do not reject unrelated prose, ordinary alphabetic labels, or explicitly qualified examples.
- Preserve the existing Owner A–I authority assignments and the joint nature of aggregate subsystem groups.
- Include positive and negative fixtures for qualified Owner references, SYS-* references, capability labels, bare-letter collisions, and bilingual parity.

## Check B — Governance operation authority traceability (#1208)

Read the governance-operation traceability register in root and EN/ZH-CN System Boundaries.

For every registered operation, independently require:
1. policy / authorization authority;
2. canonical-state authority;
3. physical executor;
4. minimum completion evidence and explicit non-inference boundary.

Requirements:
- Reject missing or collapsed authority columns.
- Reject inference of physical deletion, backup expiry, external-recipient compliance, or Global Forget Completion from a canonical Forgotten state or D fence alone.
- Reject unilateral Global Forget Completion claims.
- Cover authorization/revocation, retention/legal hold, logical Forget/fence, physical erasure, backup expiry, external-recipient deletion, and Global Forget Completion.
- An unassigned role must be explicit `NOT_ASSIGNED` and remain an open finding, not silently pass as assigned.
- Include positive and negative fixtures, including missing columns, same-role collapse, and false completion claims.

## Delivery constraints

- Add two distinct read-only checker scripts, separate test modules/fixtures, and a workflow that runs both checks with distinct result names.
- The workflow is initially advisory; do not add required branch-protection contexts or change repository rulesets.
- Do not modify `scripts/check_document_management.py`, existing validator semantics, GOV-DOC-001/002 semantics, Runtime/product code, `crates/`, schemas, APIs, DDL, deployment, or production configuration.
- Do not alter Owner A–I assignments or decide the unassigned backup catalog Owner.
- Keep #1196 and #1208 OPEN until the corresponding checker is merged and exact-Head CI evidence exists, and any separately identified Owner decision is resolved.

## Acceptance criteria

- **C1:** Owner namespace checker scans the declared canonical and bilingual paths and distinguishes Owner IDs, SYS-* IDs, capability labels, and P/S markers.
- **C2:** Owner namespace checker rejects unqualified ambiguous references and passes explicitly qualified references; fixtures demonstrate both directions.
- **C3:** Governance traceability checker independently validates policy authority, canonical-state authority, physical executor, and completion evidence for every registered operation.
- **C4:** Governance traceability checker rejects missing/collapsed roles, inferred physical completion, and unilateral global completion.
- **C5:** Both checkers cover root, EN, and ZH-CN sources and detect mirror drift in their respective registries.
- **C6:** CI runs the two checks under distinct names; workflow is advisory until separate Owner authorization changes branch protection.
- **C7:** Existing validator behavior and Runtime/product behavior are unchanged; no schema/API/DDL changes occur.
- **C8:** Tests include positive, negative, boundary, and regression fixtures; test output is reproducible from the PR Head.
- **C9:** Independent exact-Head review records all acceptance results and the PR remains Draft until then.

## Current state

Registration and design scope only. Implementation is NOT_STARTED. The #1221 documentation updates are the source contract, not evidence that either automated check already exists. No Owner acceptance is asserted by this prompt.
