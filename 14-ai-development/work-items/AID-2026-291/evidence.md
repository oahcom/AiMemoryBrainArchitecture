---
document_metadata:
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
        - "14-ai-development/work-items/AID-2026-291/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Actions runs, generated snapshots and post-merge verification have not yet been independently finalized."
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
    canonical_scope: "Execution and audit evidence for the AID-2026-291 prompt-to-implementation trace checker and ratchet."
    canonical_scope_id: "ai-development/aid-2026-291-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-291"
      - "prompt-to-commit trace"
      - "AC6 evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Evidence — AID-2026-291

## Source and implementation

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Assigned issue: #265 (AC6)
- Branch: `feat/aid-290-prompt-commit-trace`
- PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1427
- Baseline main SHA at synchronization: `7fc4ddabe1ea3b216b4536c0f5cb0a0c84306f19`
- Prior branch head retained as a merge parent: `417c2e4b573eaee51ee9383f9498ccfc25c53c6b`

## Actions evidence

- The earlier run at `417c2e4b573eaee51ee9383f9498ccfc25c53c6b` passed the checker regression tests and snapshot generation, uploaded its snapshot artifact, and failed closed at ratchet enforcement because the baseline file was absent.
- Earlier run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45950219615
- The earlier run is stale-base evidence only; a subsequent run is being validated against the latest main SHA.
- The baseline file is intended to be generated from the Actions main snapshot, reviewed, and committed at `14-ai-development/work-items/AID-2026-291/baseline.json`. Its `commit` field must equal the exact main SHA used for the scan.
- No required-context success, final five-state count, final matrix, merge, or post-merge blob verification is claimed in this preliminary evidence.

## R4 adjudication

AID-2026-047 has no `prompt_file_blob_sha` or `prompt_file_commit_sha` in its current main manifest. Its prompt bytes match HEAD, and its implementation commit is reachable. It is therefore `DIGEST_UNPINNED`, prompt dimension `HEAD_MATCH`, commit dimension `REACHABLE`; findings include `digest_unpinned` and exclude `digest_head_mismatch`. It is not promoted to TRACEABLE and no manifest pin is added. The expected TRACEABLE count on the baseline main snapshot is zero.

## Scope constraints

No change is made to the existing Schema non-empty audit job, token permissions, unrelated jobs, branch protection, or Issue #265 body. The #265 closeout comment is deferred until exact-Head checks, merge, and per-file blob verification are complete.
