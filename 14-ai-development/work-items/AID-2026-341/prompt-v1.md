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
        - "14-ai-development/work-items/AID-2026-341/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Local test suite passes; independent review is pending."
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
    canonical_scope_keywords:
      - "work-item-uniqueness"
      - "shared-id"
      - "duplicate-declaration"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# Prompt Snapshot — AID-2026-341

## Task

Replace the shared-ID verdict of the work-item uniqueness gate with the rule
recorded as section 4 of the `#1413` ruling. A duplicate declaration is one
work-item id declared by two different registry record paths inside the same
candidate tree. A modified or deleted path under an id the target branch
already owns is not a duplicate declaration.

## Required design

- `build_id_map(tree)` reads `work_item_id` from each registry record's content,
  not from the directory name; an unreadable record is INCOMPLETE.
- `check_candidate_tree` rejects only an id declared by two or more record
  paths in the candidate tree.
- `introduced_ids = head - base`; `occupied_ids = set(base_map)`; a shared id
  asserts exactly one declaration in the candidate tree.
- `introduced_ids` is additionally checked against the claim ledger for another
  pull request's valid `CLAIMED` or `MERGED` entry.
- `base_tip` decides occupancy; `merge_base` must not.

## Regression requirement

Take the eight most recent first-parent commits of main, record each head SHA
and its first parent, run the old rule and the new rule on every pair, and
record `commit / verdict_old / verdict_new / triggering_paths`. Every commit
the old rule rejected must pass now, and no real duplicate may be released.
Add three positive cases: one id declared under `registry/` and `archive/`; two
different work-item directories declaring one id; and an id already occupied on
the base tip.

## Execution constraints

Local worktree only; no force-push, no rebase, no merge, no change to other
pull requests. The report must state measured PR states rather than repeating
earlier claims.
