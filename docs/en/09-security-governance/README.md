---
# provenance: AUTHORED_INDEX
document_metadata:
  domain: "security-governance"
  role: "guide"
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: {scheme: git, value: null}
      approval_scope: {type: Full-document, included_sections: [], included_assets: []}
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "provenance: AUTHORED_INDEX"
        - "directory inventory: 09-security-governance/"
        - "source branch: session-i-security-governance-2026-11-16"
        - "source commit: 8abddf814467b271344a9814613a6b7ca6a446c6"
        - "authoring date: 2026-11-26"
        - "executing operator: user-authorized operator (delegated by account owner)"
        - "no authoritative source; this file is a newly authored index"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "AUTHORED_INDEX; no authoritative source exists; this file is a newly authored navigation index. Owner review pending."
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
    canonical_status: Candidate
    canonical_scope: "Newly authored navigation index for available security governance material; not a recovered root specification"
    canonical_scope_id: "security-governance/directory-index"
    canonical_scope_keywords: ["documentation-index", "source-provenance", "governance"]
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Security, Identity & Governance — Directory Index

> **AUTHORED_INDEX — not a restored specification.** No authoritative source exists; this file is a newly authored index. No source documents were present directly in the root directory at the pre-creation inspection.

## Root-directory inventory

There were no pre-existing root-level documents in `09-security-governance/`. This README is the only root-level document added by this change.

## Available bilingual material

| Document | EN mirror | ZH-CN mirror | Status |
|---|---|---|---|
| Security, Identity & Governance Architecture Guide (DOC-SEC-001) | [English guide](security-governance-guide.md), blob `061c5847b3df879eeaf3c71e5eae0bfa162b276a` | [Chinese guide](../../zh-CN/09-security-governance/security-governance-guide.md), blob `372d27c79dc79d09bcdb0f142c979efdba1c2b6e` | Candidate / Informative; I Owner exact-version acceptance pending; not a production security certification |

These are existing mirrors, listed as navigation targets only. Neither is asserted to be an authoritative root-source blob.

## Governance boundaries

- I owns global identity/authorization policy, delegation and revocation, retention, audit governance, backup/external-copy policy, cross-system Forget governance evaluation policy, evidence-acceptance criteria, and physical-erasure requirements.
- D retains ownership of canonical Forget lifecycle semantics and its domain completion predicate. This index does not redefine that boundary.
- D/E/F/G/H/C retain their respective local enforcement mechanisms and boundary-specific evidence.
- This index does not approve policy, certify production security, establish a canonical source, or grant implementation authority.
- Do not infer authoritative source status from an EN/ZH-CN mirror.

## Missing authoritative sources and blockers

- No authoritative root README or root specification blob was located; this file is newly authored.
- Additional I Owner documents have not been restored here without exact source-body/frontmatter and bilingual review.
- I36-GOV-01..10 remain GOVERNANCE-BLOCKED pending approver, exact policy hash/version, authority, scope and effective-time evidence.
- Exact-version I Owner review and Governance acceptance remain pending.
