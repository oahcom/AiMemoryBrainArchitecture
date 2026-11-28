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
# Session Evidence — AID-2026-311

## Session role / use case

Implementation session for Issue #1341. Scope after #1436: repair the
work-item uniqueness checker's claim identity and its unit suite. Workflow
wiring is out of scope because `merge_group: checks_requested` and the
`PR_BASE` / `MERGE_GROUP_BASE` / `PUSH_BEFORE` resolver already exist on main.

## Actual AI input

The user supplied the independent acceptance findings:
- merge-base-based introduction detection loses the original claim after Update branch;
- a candidate that declares an AID the base already owns must still be rejected after the merge-base moves.

A later user message reduced the scope: #1436 has already merged the
merge_group wiring and the three-way base resolver, so #1432 must carry only
the claim-identity logic and its tests; every `.github/workflows/*.yml` file is
to be taken from main unchanged. The same message required a fresh branch cut
from current main rather than a further merge on the original branch, local
Python verification, the negative Update-branch proof, and the unchanged
`AID-2026-311` carrier.

## AI-visible output

The session fetched origin, cut `fix/1341-claim-identity-aid-311` (rebuilt) from
current main, and replaced the merge-base introduction scan with per-commit
first-parent claim resolution. The CLI, exit codes, `Incomplete` semantics and
verdict line are unchanged. All pre-existing tests are retained; five mutations
are added: Update branch with a colliding claim, merge-queue reconstruction,
Update branch with a free claim, two candidate-only claims for one ID, and
repeat determinism. The two collision tests assert that the legacy merge-base
calculation returns `introduced=0 occupied=0` on the same graph.

Local execution (PowerShell, `python`, no WSL):

```
python -m unittest discover -s scripts/ci -p "test_work_item_uniqueness.py" -v
Ran 13 tests ... OK
```

The negative proof builds A-first / B-Update-branch in a scratch repository,
shows `merge-base(base, B)` equals the advanced base, and records the checker
exit code 1 with the claim-commit SHA of B.

## Boundary

No workflow file, branch protection, ruleset, merge queue setting or other PR
was modified. No merge is claimed by this document.

