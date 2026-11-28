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
        - "14-ai-development/work-items/AID-2026-294/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
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
      - "merge-queue"
      - "required-context"
      - "document-management"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# Session Evidence — AID-2026-294

## Session role / use case

Implementation session for the regression introduced by PR #1453. Scope: restore
the `merge_group` wiring that `document-management.yml` lost, restore the
fail-closed merge-group base/head resolution that went with it, serialize the
workflow by target branch, correct the `gates.yml` required-context count, and
add a repository-hygiene gate so the same loss cannot stay silent.

## Actual AI input

The orchestrating session supplied the investigation result as fixed evidence:
PR #1453 (merge commit `31c1e5d83`, head `8faf593a5`) has `da69e43f` (#1436) as
an ancestor, its base `159095f3c` still carried eight `merge_group` / `MG_BASE`
matches in the workflow, and the merge result carried none; the PR body, its
issue and review comments, and all 52 branch commit messages contain no
rationale for a removal.

The same session required: an independent worktree, no force push, no rebase, no
merge, no merge-queue enablement, no branch-protection change, a gate that goes
red on the current main and green after the repair, and a report with both real
outputs.

A second instruction added two items to the same PR: the target-branch
concurrency form (`cancel-in-progress: false` plus `queue: max`, keyed off
`pull_request.base.ref` / `merge_group.base_ref` / `github.ref`), and the
`gates.yml` count correction from six to seven.

The full prompt is pinned at `14-ai-development/work-items/AID-2026-294/prompt-v1.md`
(25170 bytes, SHA-256 `056b9208fb9425913d3fa57cc8f30414423119b2a98908d706a58f0ed138de55`).

## AI-visible output

The session cut `fix/2026-11-28-docmgmt-merge-group` from `origin/main`
(`a0500d519`) in an isolated worktree and produced:

- `.github/workflows/document-management.yml`: `merge_group:
  types: [checks_requested]` restored; the uniqueness step now branches on
  `github.event_name` — `pull_request` keeps the fetched target branch,
  `merge_group` uses `merge_group.base_sha` / `merge_group.head_sha` and exits 2
  (INCOMPLETE) when either is unusable, `push` keeps `github.event.before`, and
  any other event exits 2 instead of calling the checker without arguments.
- `.github/workflows/document-management.yml`: concurrency keyed by target
  branch for all three events, `cancel-in-progress: false`, `queue: max`.
- `.github/workflows/gates.yml`: `Six required contexts` corrected to `Seven`.
- `scripts/check_required_contexts_merge_group.py`: read-only gate over the
  sixteen declared contexts, the concurrency shape, and per-workflow
  required-context count comments.
- `scripts/test_check_required_contexts_merge_group.py`: seven cases.
- `.github/workflows/repository-hygiene.yml`: the gate and its self-check run
  beside the existing declared-check-contexts steps.

Local execution (Windows, PowerShell, `python`, no WSL):

```text
python scripts\check_required_contexts_merge_group.py      # repaired tree
REQUIRED CONTEXT MERGE_GROUP WIRING: PASS (16 contexts)     exit=0

python scripts\check_required_contexts_merge_group.py      # clean origin/main a0500d519
REQUIRED CONTEXT MERGE_GROUP WIRING: FAIL (5 violation(s))  exit=1

python -m unittest test_check_required_contexts_merge_group
Ran 7 tests ... OK
```

The `scripts/ci/test_work_item_uniqueness.py` failures observed in this
environment reproduce on the clean `origin/main` tree (`9009 != 1`: the suite
spawns `python3`, which does not exist on this Windows host) and are recorded as
pre-existing, environment-related evidence, not as a result of this change.

## Boundary

No force push, no rebase, no merge, no other pull request was modified, the
primary worktree was not touched, the merge queue was not enabled, and branch
protection and rulesets were not changed. No merge is claimed by this document.
