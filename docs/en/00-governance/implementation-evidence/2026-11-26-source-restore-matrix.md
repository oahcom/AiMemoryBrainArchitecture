---
document_metadata:
  domain: security-governance
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-11-26-SOURCE-RESTORE-02"
        - "Bilingual evidence companion"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Draft evidence companion; CI and Owner review pending."
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
    source: "00-governance/implementation-evidence/2026-11-26-source-restore-matrix.md"
    en: null
    zh-CN: "docs/zh-CN/00-governance/implementation-evidence/2026-11-26-source-restore-matrix.md"
---

- Source revision: a09ede9b70457b1dd0a42272b6e421557996ee8e
- Source: [canonical evidence record](../../../../00-governance/implementation-evidence/2026-11-26-source-restore-matrix.md) (source Blob `a09ede9b70457b1dd0a42272b6e421557996ee8e`).

# AID-2026-11-26-SOURCE-RESTORE-02 — Source Restore Evidence Matrix

**Baseline main:** `6314a65bd8be48c1a4bb0768e9960c4c808110ab`  
**D source commit:** `b525e1f8fee2471a131e4a38efda99804045e424`

## D per-file evidence

| File | Original source Blob | Candidate final Blob | Eligibility |
|---|---|---|---|
| `03-memory-brain/memory-brain-overview.md` | `b4ed712ac0626ab127cccfd205c50a9013df01fb` | `9ca153df403d09264a50add8ad78bb5a6111c7c0` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/canonical-memory-store.md` | `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `d47366d1ca04da37ff77f6edd31fe42efc93e0f9` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/memory-lifecycle-manager.md` | `8b972035b449e1eab546aedc9cc5b30581600c65` | `453d42592942d0508b00a4b8c5ed9320b9ced3f7` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | `c6f343011a8be0fa0d4bae2659ecffc33d9557ac` | BLOCKED_OWNER_REVIEW |

## Governance

The PR adds `03-memory-brain` to the bilingual gate's normative roots and the GOV-DOC-002 governed-root registry, adds a D source index, and records exact source and mirror Blob pins. Source documents remain Candidate / Draft / Informative. No Owner acceptance, Governance approval or effective normative promotion is asserted.

## Other Owners

F remains blocked pending F Owner resolution, exact-version acceptance and continuous watermark coverage proof. I remains governance-blocked. H remains blocked pending exact core inventory, H Owner acceptance and cross-owner dependency reviews. No F/I/H source files are restored.

## Validation

No local shell/worktree was available. Local git and Python gate commands are NOT RUN; PR CI and independent semantic mirror review remain pending. The PR is Draft and is not merged.
