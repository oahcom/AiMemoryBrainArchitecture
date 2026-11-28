---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-25"
      last_verification_note: "This file records the assignment text one agent received in a multi-agent session. It is transcribed, not captured as a platform payload: the session transport was not recorded, so the digest below proves the committed file has not changed since it was pinned, not that this is the byte-exact string any model received."
    usage_status: Active
    modification_status: Unchanged
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

# AID-2026-059 session prompt — Issue #1026

The assignment as received by the implementing session: fix Issue #1026 in
`scripts/governance/session_evidence/validate.py`, add four assertions, verify
them by mutation, and pass the gate on its own pull request.

## Task

Repo: `/d/code/AiMemoryBrainArchitecture`. Create a worktree at `/d/wt/a1026`
from a freshly fetched `origin/main`. Do not touch any other worktree under
`/d/wt/`. Do not edit the main checkout in place.

Issue #1026: the validator enforces the PR-body declaration before its own
historical-exemption guard can run, so every PR whose linked Issues all predate
the policy effective time is required to fill a form the policy says does not
yet apply to it.

Facts to re-verify rather than trust:

- `_run_checks(ctx)` calls `check_01_pr_fields_and_issue_references(ctx)` as its
  first statement. `check_01` begins with
  `_parse_status(_extract_field(ctx.body, "AI-assisted work"), "PR")`, and
  `_parse_status(None, ...)` raises
  `ValidationError: PR: missing AI-assisted work declaration`.
- The historical guard `_historical_not_applicable(ctx)` is only reached near the
  end of `_run_checks`, after `check_01`, `check_02`, the mapping-set equality
  check and `check_03`.
- Therefore a PR that links only pre-effective Issues still fails at `check_01`.

Constraint: `_historical_not_applicable` returning `False` on an empty
`ctx.issues` is the #1003 fail-open. A naive move of the guard to the top of
`_run_checks` must not be able to see an empty Issue set.

Ruling on the shape of the fix:

1. Parse first, without enforcing: call `parse_related_issues(ctx.body, ctx.repo)`
   at the top of `_run_checks`. Change nothing about how it behaves.
2. Exempt only the undeclared case: if `_historical_not_applicable(ctx)` is true
   and the body declares neither `AI-assisted work` nor
   `Session evidence reference(s)`, return the existing historical verdict and
   exit 0.
3. Otherwise keep today's order byte-for-byte, including `check_01`, `check_02`,
   the mapping-set equality, `check_03`, and the historical/`check_04` branch. A
   PR that volunteers `AI-assisted work: YES` with a reference that does not
   exist must still fail; the issue's weaker "skip the body checks" version is
   rejected.

Tests, four assertions:

1. A pre-effective PR body containing only `Related issue(s): #481` exits 0 with
   `AI-SESSION-EVIDENCE: NOT_APPLICABLE`.
2. The same body plus one post-effective linked Issue still exits non-zero with
   the missing-declaration message.
3. A pre-effective PR declaring `YES` with a nonexistent reference still exits
   non-zero.
4. A pre-effective PR declaring `YES` with an existing non-empty reference exits
   0 with `NOT_APPLICABLE`.

Reverse-verification: mutate `_historical_not_applicable` to return `False`
unconditionally and confirm assertion 1 fails with an `AssertionError`; make the
new early exit unconditional and confirm assertion 3 fails with an
`AssertionError`; restore after each and re-run the full suite.

Deliverable: commit, push a branch, open a ready pull request against `main`,
and report the PR number, head SHA, the exact `validate.py` diff, the four test
names and the full suite count, each mutation with the test it killed, and every
gate read with its conclusion.
