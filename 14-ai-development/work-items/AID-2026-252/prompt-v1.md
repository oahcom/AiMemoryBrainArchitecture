---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Task prompt scope snapshot; source provenance is not a byte-for-byte transcript."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "User-assigned W9 task prompt snapshot for AID-2026-252"
    canonical_scope_id: "ai-development/aid-2026-252-prompt"
    canonical_scope_keywords:
      - "document-stewardship"
      - "issue-266"
      - "metadata-gate"
    canonical_conflict_status: None
    normative_status: Informative
---

# Prompt Snapshot — AID-2026-252

This is a structured scope snapshot of the user-provided W9 task, not a byte-for-byte export of the original chat message. Its provenance is therefore marked NOT_VERIFIED.

## Objective

Implement W9 / Issue #266 AC3 in oahcom/AiMemoryBrainArchitecture by adding a machine-enforceable document-maintenance responsibility field, continuing the required work item AID-2026-252.

## Required constraints

1. Use only the assigned identifier AID-2026-252; do not allocate from INDEX max+1 and do not use numbers reserved for parallel work.
2. Add the ownership field to 00-governance/architecture-document-metadata.schema.yaml. Do not name it owner because M-08 already uses “Consumer owners” for external consumers; use steward or maintainer and explain the distinction.
3. Implement enforcement in scripts/check_document_management.py; schema-only declaration is insufficient.
4. Choose either immediate required enforcement with a legacy missing list, or optional legacy compatibility with enforcement only for new documents. State a deterministic closure condition.
5. Include the required PR declarations: Related issue(s): #266; AI-assisted work: YES; Session evidence reference(s) to this Work Item's session-evidence.md. The PR body must contain an Issue mapping row and use a real Issue number.
6. If actions/runs?head_sha returns total_count 0 within three minutes after PR opening, rebuild the branch with a non-fast-forward merge commit from origin/main, comment and close the first PR, then open a replacement PR.
7. Merge only after all 16 required contexts succeed, branch protection strict and enforce_admins are both true, behind count is zero, and the merge is performed with the merge method. Do not squash, rebase, force-push, change protection, close the Issue, or fabricate evidence.
8. Before merging, merge the current origin/main into the branch and push. If a 405 occurs, restart the merge attempt. After merging, verify each changed path's main blob against the PR head blob.
9. After merge, comment on Issue #266 with the field name and rationale, schema diff, checker output including the missing count, and proposed replacement AC3 wording. Do not modify or close Issue #266.
10. Attribute work to “user-authorized operator (delegated by account owner)” and date 2026-11-27. Preserve the fact that any proxy ruling is not a natural-person Owner signature.
11. Preserve concurrent changes and modify only this work item's scope.

## Expected deliverables

AID-2026-252 manifest, evidence and session evidence; schema and checker changes; regression tests; template and policy updates; PR and merge evidence; post-merge blob verification; and an Issue #266 comment with a proposed AC3 text.
