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
        - "14-ai-development/work-items/AID-2026-360/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Every number below was produced in this working tree by the quoted command; no CI result or merge SHA is claimed."
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
    canonical_scope: "Execution and audit evidence for the AID-2026-360 merge-group candidate validation."
    canonical_scope_id: "ai-development/aid-2026-295-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-360"
      - "merge-group candidate"
      - "GAP-03"
      - "GAP-04"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-360 evidence

## Objective

A merge-group candidate is one tree. Validating only the tail pull request of a
queue would accept a candidate in which an earlier member's head is absent, in
which the trusted base is not an ancestor, or in which a member head is already
contained in the base. This change decides all three relations on the candidate
tree and then validates every member pull request body against that same tree.

## What changed

| Path | Role |
| --- | --- |
| `scripts/governance/merge_group/candidate.py` | Shared resolver: complete queue paging, prefix resolution, `B ≼ C`, `∀i H_i ≼ C`, `∀i H_i ⋠ B`, failure-semantics table |
| `scripts/governance/session_evidence/validate.py` | Merge-group branch, incomplete-versus-violation split, per-member verdict, candidate-tree evidence resolution |
| `.github/workflows/session-evidence.yml` | Candidate resolution step, merge-group validation step, self-test wiring |
| `.github/workflows/bilingual-docs.yml` | Candidate-tree checkout for the bilingual gate on merge groups |
| `tests/merge_group/` | Offline fixtures, parser and relation tests, multi-pull-request integration tests |

Not changed: `document-management.yml`, `gates.yml`, branch protection, the merge
queue configuration, and every other pull request.

## Verification

Commands run in the worktree, with the results they printed:

```text
python -m unittest discover -s tests/merge_group -p "test_*.py" -v
Ran 30 tests ... OK

python -m unittest discover -s tests/session_evidence -p "test_*.py"
Ran 100 tests ... OK

python scripts/check_session_evidence_workflow_shape.py
SESSION EVIDENCE WORKFLOW SHAPE: PASS

python scripts/ci/check_test_reachability.py
Test reachability: 74 test files, 74 reachable, 0 unreachable

python scripts/ci/check_line_endings.py
Line-ending check: 1925 files inspected, 0 binary skipped, 0 violations.
```

The integration tests are offline: `gh_api`, `gh_tree`, `gh_blob_bytes` and
`gh_blob_text` are replaced by fixtures, and the compare endpoint is answered by
the same fake API. No test reaches the network.

## Failure semantics

| Condition | Verdict | Exit |
| --- | --- | --- |
| All three relations hold, every member body valid | `AI-SESSION-EVIDENCE: PRESENT` | 0 |
| `H_i ≼ B` (member head already in the base) | `PR_HEAD_ALREADY_IN_BASE` | 1 |
| `H_i ⋠ C` (member head not in the candidate) | `PR_HEAD_NOT_IN_CANDIDATE` | 1 |
| `B ⋠ C` (base not in the candidate) | `BASE_NOT_IN_CANDIDATE` | 1 |
| Queue membership cannot be read completely | `QUEUE_MEMBERSHIP_INCOMPLETE` | 2 |
| Git graph cannot be read completely | `GIT_GRAPH_INCOMPLETE` | 2 |

An incomplete member prevents a `PRESENT` total even when another member already
produced a confirmed violation.
