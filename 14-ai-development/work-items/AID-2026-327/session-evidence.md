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
        - "14-ai-development/work-items/AID-2026-327/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Local suite passes; independent review is pending."
    usage_status: Active
    modification_status: New
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
      - "merge-group"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# Session Evidence — AID-2026-327

## Session role / use case

Implementation session for Issue #1341. The session replaced the shared-ID
modification/deletion rejection in the work-item uniqueness gate with a
tree-level duplicate-declaration rule, added the missing `merge_group` trigger
and merge-group SHA handling to `document-management.yml`, and pinned a
first-parent regression window comparing the old rule with the new one.

## Actual AI input

The executed prompt is recorded verbatim in `prompt-v1.md`. It fixed the
authority for the decision (section 4 of the `#1413` ruling), required the
`base_tip` / `merge_base` separation, and demanded a regression fixture over
the eight most recent first-parent commits of main with recorded base and head
SHAs, old-rule and new-rule verdicts, and triggering paths, plus three positive
cases.

Two follow-up rulings refined the implementation: canonical manifest paths with
legacy identity shapes read from content, deletion of the unreachable
`occupied` branch, a pinned oracle instead of a weak subset assertion, hard
failure when the pinned window is absent, a target-tree-only claim ledger,
`--pull-request` requiring `--repository`, identity conflicts reported as
violations rather than incomplete input, and a merge-group-aware workflow with
the missing trigger added.

A third ruling covered a change on main during implementation: PR #1432 and PR
#1477 merged, and #1477 replaced the checker with a tree-only directory-diff
verdict that rejects added files under an existing work-item directory and
treats a deleted directory as a failure. The ruling required replacing that
verdict with the manifest-identity rule, keeping this branch's version of the
two checker files when merging `origin/main`, and leaving #1432's lifecycle
untouched because it is already merged.

## AI-visible output

Measured results.

```text
origin/main at start of work                        31c1e5d83e7dad326dbd4b69d4a8e19534718ff1
origin/main merged into this branch                 473f06d76f7a06ff91615a2dae0ddd75295391c0
old rule location (M/D branch)                      #1413 head 54c44fbac,
                                                    competing_claims(), status in M/D/T/R/C
tree-only rule replaced                             #1477, commit a0500d519
old rule on the pinned window                       VIOLATION on 2 of 8 commits
                                                    (31c1e5d83: 45 ids; 6482901cb: AID-2026-291)
new rule on the pinned window                       PASS on 8 of 8, duplicate_declarations=0
test suite                                          Ran 28 tests, OK
```

Deleted and additive outcomes: a same-path deletion and an auxiliary file added
inside an existing work-item directory both PASS. #1477 reported the first as
`DELETION` with exit 1 and the second as `VIOLATION new_paths=...`; the ruling
replaced that verdict rather than layering on top of it.

Duplicate and identity cases executed by the suite: two work-item directories
declaring one id (VIOLATION), base record plus a second candidate path in the
merge tree (VIOLATION), a record with no supported identity field
(VIOLATION), a record whose id disagrees with its directory (VIOLATION), a
blocking `CLAIMED` ledger entry owned by another pull request (VIOLATION), a
candidate-supplied ledger with no target-tree ledger (INCOMPLETE), and
`--pull-request` without `--repository` (INCOMPLETE).

Legal shared-id operations executed by the suite: same-path modification,
deletion, and additive files under an existing record all PASS.

No merge, force push, branch-protection change, or real merge-queue run is
claimed. Independent review is not claimed.
