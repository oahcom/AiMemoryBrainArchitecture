---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: work-record
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
        - "14-ai-development/work-items/AID-2026-250/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Exact PR-head checker and tests passed on d2fe8598bb4d140f62f23060c644845f72ebec36; post-merge blob verification pending."
    usage_status: Active
    modification_status: Active-Modified
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

# Evidence — AID-2026-250

## Scope and baseline
- Base: `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028`
- Branch: `w7/aid-250`
- Related Issue: #262
- Four reports: SYS-RISK-001 EN/ZH-CN and architecture-complexity-assessment EN/ZH-CN.

## Historical provenance boundary
All four reports identify historical baseline `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. The metadata preserves that source baseline. SYS-RISK-001 does not record the original assessor session identity; that limitation is disclosed. The attachment does not retroactively prove a contemporaneous signature.

## Checker evidence
- Checker and tests: `scripts/ci/check_req_assessment_signatures.py`, `scripts/ci/test_check_req_assessment_signatures.py`.
- Exact PR Head: `d2fe8598bb4d140f62f23060c644845f72ebec36`.
- Workflow: Existing gates, run 1969 / run ID `45942503331`; job `Schema non-empty audit (hard gate)`, job ID `140319749141`.
- Checkout log explicitly records `ref: d2fe8598bb4d140f62f23060c644845f72ebec36`, not the synthetic PR merge ref.
- Checker output:
```text
PASS reviews/architecture/SYS-RISK-001.en.md: assessor, assessed_version, evidence_baseline
PASS reviews/architecture/SYS-RISK-001.zh-CN.md: assessor, assessed_version, evidence_baseline
PASS reviews/complexity/architecture-complexity-assessment.en.md: assessor, assessed_version, evidence_baseline
PASS reviews/complexity/architecture-complexity-assessment.zh-CN.md: assessor, assessed_version, evidence_baseline
SUMMARY records=4 failures=0
```
- Regression tests: `Ran 5 tests in 0.008s`; `OK`.
- Schema audit in the same job: `OK: 32 schemas; 5599 registered constraints; no unregistered or stale entries.`
- Job URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45942503331/job/140319749141
- This is a CI observation on the exact PR Head above; the subsequent evidence-only commit will be rechecked on its own exact PR Head. Post-merge blob verification remains pending.

## Integration
Reuse the existing `Schema non-empty audit (hard gate)` job. No new job/context, branch-protection mutation, Issue body change, or Issue closure.

## Base synchronization
- A merge commit incorporated latest observed main `a588cd9914949c2c9db7b2c5704d906fd3f05b70` into the work branch before exact-Head verification: `8a6fe56b0a2a10018a6dbda1c546d7002eb3a64a`.
- This is a normal two-parent merge commit; no rebase, squash or force update was used.

## Base synchronization and PR traceability
- Latest observed main incorporated by merge commit: `242cf101c8b79007ad2fb8d9c89681224577188d`.
- Merge commit on the work branch: `83500c919e19f1ad02df617d7cf07a5aa08f6453` (two parents; no rebase, squash or force update).
- PR: #1388. The PR description now includes the required per-Issue mapping table for #262.
