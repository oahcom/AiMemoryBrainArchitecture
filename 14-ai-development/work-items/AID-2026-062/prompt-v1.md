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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "The two platform measurements quoted in the text were read through the REST API in the session that produced this instruction; the byte size and digest were measured from the committed blob after the manifest pinned them."
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

# WO-01 stage B — executed instruction

Scope: correct `PR-GOVERNANCE-001` section 7 to the required-check set the
platform actually enforces, as a dated measurement, and change nothing else.

Acceptance asked for:

1. The declared count equals the live payload count at the moment of the reading.
2. Every declared context is produced by a job id or a job `name` in
   `.github/workflows`, because that is what `check_declared_check_contexts.py`
   can verify and the only thing it verifies.
3. The English and Chinese blocks state the same count.
4. The increment is attributed rather than folded into one number: which contexts
   were already required before the document noticed them, and which one was
   added by a change — and why that change had to come first.
5. The deliberately-failing-head sentence stays, with its count corrected. It is
   not softened by this edit.

Excluded, and stated as excluded: the branch-protection change (already applied),
the deliberately-failing-head experiment (still not run), and every other section
of the document.

Context that produced the numbers in the acceptance text:

- `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` on
  2026-11-25 returned fifteen contexts before this change and sixteen after.
- Merged pull request #1024 changed six markdown files, none under `crates/`, and
  produced exactly fifteen check runs. `rust-workspace-test` was absent from its
  Head, which is what makes "require it first" a deadlock rather than a choice.
