---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    verification_status: Unverified
    last_verified_date: "2026-11-28"
---

# AID-2026-032 — Differential session identity gate

## Decision and measured basis

The selected design is route B: compare the current checkout's violation identities with the work-items tree at the authoritative base commit. The 2026-11-28 coordination measurements supplied for this work were:

- 83 workflow runs sampled: 65 failures and 18 successes, approximately 78% failures.
- The most recent eight results: failure, failure, failure, failure, success, success, failure, failure.
- Current checker on main: 92 violations, 91 baselined, 1 new.
- Inventory: no_evidence_section=39.
- The sole new finding: SESSION_UNPARSEABLE at 14-ai-development/work-items/AID-2026-297/manifest.yaml#1, value MIGRATION-POLICY, introduced by PR #1513.
- Two snapshot deadlocks: --write-baseline refuses expansion; --bootstrap-baseline refuses when the target tree already contains the baseline file.
- Of 18 sampled open PRs, only 2 had ever produced the standalone Session identity ratchet check run.

These are coordinator-supplied measurements, not measurements independently rerun by this implementation session.

## Ruling

The PR admission predicate is:

    new = violations(current_tree) - violations(base_tree)

An empty increment exits 0 and prints a summary containing violations, base and new counts. Each introduced finding prints one line beginning exactly with NEW: and exits 1. An unresolvable ref, non-Git worktree, shallow repository, or missing Git object exits 2 on stderr. The diff mode does not read, write, or require the snapshot baseline. Current-tree SESSION_YAML_INVALID is always a failure; base-tree YAML errors are disclosed as existing debt and excluded from the increment set.

The old snapshot baseline and its command modes are retained for historical/manual use and compatibility, but are no longer invoked by the required CI path. The baseline file is not edited by this work item.

## Required-job integration

The differential self-tests and PR check are steps inside the existing Repository hygiene (hard gate) job. The job ID and name are unchanged, and no required context is added. Session identity ratchet is not a required context; the effective gate is the new step inside Repository hygiene (hard gate). Adding a new required context would strand existing open PRs whose heads never produced that check run.

The new differential step is pull_request-only and uses github.event.pull_request.base.sha. It deliberately does not run on merge_group or push because the R2 contract for this step is PR-event-only. The merge-group candidate therefore relies on the PR check plus the existing required job's other queue checks; this leaves a documented residual gap if the queue candidate differs materially from the already-checked PR head. Direct pushes to main can introduce debt without a PR diff check. Such debt must be exposed by a separate periodic full-tree scan and alert; that full-scan mechanism is not implemented here and remains follow-up work.

## Implementation inventory

- Checker: --diff-base REF; Git verification; base work-items archive; set difference; exact exit/output contract; baseline-independent path.
- Tests: 13 test_diff_* cases, including explicit M1/M2 mutation assertions, plus unchanged legacy snapshot tests.
- Workflow: test step and PR-only check inserted after the existing PyYAML installation in the manifest-parse step; standalone non-required workflow removed.
- Documentation: §12 appended to all three session-identity design counterparts; PR-GOVERNANCE-001 §7 clarified without changing the 16-item declaration.

## Verification status

The GitHub file writes succeeded on the work branch. This environment has not executed the Python unit suite or a GitHub Actions run. Exact-head CI, coordinator placeholder replacement, independent review, and Owner acceptance are pending. No merge is claimed.

## Scope attribution

This PR changes only the session identity checker/tests, the existing Repository hygiene workflow, the standalone session identity workflow, the three session-identity design documents, the required-context explanatory text, and the AID-2026-032 registration/evidence files. It does not repair AID-2026-297, modify any other work-item record, change branch protection, or alter Session Evidence validation.
