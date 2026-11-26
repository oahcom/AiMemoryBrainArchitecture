---
document_metadata:
  domain: memory-brain
  role: index
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
        - "Issue #1177"
        - "D candidate source index"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Index identifies candidate source versions only; final Owner acceptance is pending."
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
    canonical_scope: "Navigation index for D-owned Memory Brain source specifications"
    canonical_scope_id: "memory-brain/source-index"
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/03-memory-brain/README.md"
    zh-CN: "docs/zh-CN/03-memory-brain/README.md"
---

# Memory Brain — Canonical Source Index

This index identifies the four D-owned source artifacts restored from the exact Owner-branch snapshot below. Their presence in this Draft PR is a candidate-source restoration for review; it does not constitute D Owner acceptance, cross-Owner acceptance, Governance approval, or effective normative promotion.

- Source branch: `session-d-memory-brain-2026-11-16`
- Source commit: `b525e1f8fee2471a131e4a38efda99804045e424`
- Tracking issue: #1177
- Review state: Candidate restoration; Owner acceptance pending
- Authority state: `canonical_status: Candidate`, `normative_status: Informative`

| Source document | Original source Blob SHA | Candidate final Blob SHA | Status boundary |
|---|---|---|---|
| [memory-brain-overview.md](./memory-brain-overview.md) | `b4ed712ac0626ab127cccfd205c50a9013df01fb` | `9ca153df403d09264a50add8ad78bb5a6111c7c0` | authority boundaries DECIDED; detailed contracts CANDIDATE/OPEN |
| [canonical-memory-store.md](./canonical-memory-store.md) | `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `d47366d1ca04da37ff77f6edd31fe42efc93e0f9` | INT-P0-01 ADR-blocked; detailed model CANDIDATE |
| [memory-lifecycle-manager.md](./memory-lifecycle-manager.md) | `8b972035b449e1eab546aedc9cc5b30581600c65` | `453d42592942d0508b00a4b8c5ed9320b9ced3f7` | state separation DECIDED; thresholds/transitions OPEN |
| [forget-fence-operation-and-publication-gate.md](./forget-fence-operation-and-publication-gate.md) | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | `c6f343011a8be0fa0d4bae2659ecffc33d9557ac` | D semantics DECIDED; E/Storage/I enforcement OPEN |

The source files preserve their original source bodies. GOV-DOC-002 metadata is prepended as a governance wrapper; the original Owner-branch Blob SHAs remain pinned in each document's `evidence_reference`.

The EN and ZH-CN reading companions remain non-canonical mirrors. Their prose is preserved; only governance metadata and source-revision pointers are updated. The Forget Fence source retains its existing four-part bilingual reading set. Semantic parity remains a manual review item and is not claimed as mechanically proven.

## Acceptance boundary

No document in this set is declared `Approved` or `Normative` by this PR. D Owner must review each exact final Blob. Relevant dependency Owners and Governance must separately accept their assigned boundaries. A later approval must bind to the exact final Blob, not merely to this branch name.
