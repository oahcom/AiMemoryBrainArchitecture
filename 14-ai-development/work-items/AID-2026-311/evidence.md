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
        - "14-ai-development/work-items/AID-2026-311/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Implementation and CI verification are pending independent review."
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
      - "merge-queue"
      - "claim-identity"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# AID-2026-311 — Evidence

**Attribution:** user-authorized operator (delegated by account owner)  
**Date:** 2026-11-27  
**Issue:** #1341  
**Implementation base observed:** 460f437eb3496e10737b9ef20f4b816e34d155c4

## Scope note

This work item originally also carried the `merge_group: checks_requested`
wiring for eight workflows and a `PR_BASE` / `MERGE_GROUP_BASE` / `PUSH_BEFORE`
resolver for `document-management.yml`. That wiring landed on main through
#1436. It is therefore absent from this PR by design; the PR now carries only
the claim-identity increment of the uniqueness checker and its tests.

## Defect and reproduction model

The former checker computed newly introduced directories from
`merge-base(base, head)`. If candidate B merges an advanced target branch after
candidate A has added the same work-item ID, the merge-base moves to the target
commit containing A's directory. B's distinct file is then additive relative to
that merge-base and the former checker reports `introduced=0 occupied=0`.

The regression test constructs exactly this graph in a temporary Git
repository:
1. Create A and B from one old base.
2. A adds `AID-2026-311/a.txt`.
3. B adds `AID-2026-311/b.txt`.
4. Advance simulated main to A.
5. Merge simulated main into B, representing GitHub Update branch.
6. Assert merge-base(B, latest main) equals latest main, both files exist in B,
   the legacy calculation returns 0/0, and the fixed checker returns VIOLATION.

## Claim identity

The checker enumerates non-merge commits in `base..candidate`. For each
candidate-only commit it inspects added AID paths against that commit's
first-parent tree. A commit that adds the first file under a directory absent
from its own first parent is the claim commit. Update branch creates a merge
commit, which is excluded; the original B claim commit remains candidate-only
and stays visible. Files added under a directory already present in the claim
commit's first-parent tree are additive and do not create a second claim.

This intentionally covers merge-based Update branch, merge-queue
reconstruction/reordering, retries, and base advancement. A rebase that
rewrites the original claim commit is outside this identity guarantee; a
candidate-only directory with no detectable claim returns INCOMPLETE.

## Merge-group reconstruction regression

A second test builds the merge-queue shape: A and B fork from one old base; A
adds `a.txt`; B adds `b.txt`; A advances simulated main; the queue candidate is
a merge of that advanced base with B's original head. The merge-base is the
advanced base, both files are in the candidate tree, the legacy algorithm is
asserted to return `introduced=0 occupied=0`, and the fixed checker returns
VIOLATION.

## Verdict contract

The CLI, exit codes (0 PASS, 1 VIOLATION, 2 INCOMPLETE), `Incomplete` failure
semantics and the `base=` / `candidate=` / `introduced=` / `occupied=` verdict
line are unchanged, so the existing `document-management.yml` invocation and
the pre-existing tests keep working. Violation lines now also name the
candidate claim commits, and duplicated claims are reported as
`duplicate_claims=`.

## Fail-closed inputs

Missing base or head, unreadable commit or parent objects, failed Git commands,
and a candidate-only new directory with no identifiable claim return exit 2. An
occupied base plus a candidate-only claim returns exit 1. An established
directory with no candidate-only claim remains eligible for additive files.

## Verification status

Local verification on the scoped branch:

```
python -m unittest discover -s scripts/ci -p "test_work_item_uniqueness.py"
Ran 13 tests ... OK
```

The negative proof (A lands first, B Update-branches, both claim
`AID-2026-311`) is recorded below with the constructed repository and the
checker's exit code. No merge-queue race and no merge are claimed by this
document.

