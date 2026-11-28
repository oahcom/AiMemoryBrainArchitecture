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
        - "14-ai-development/work-items/AID-2026-328/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Implementation and exact-head verification remain pending."
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
    canonical_scope: "Implementation-session identity and evidence for AID-2026-328."
    canonical_scope_id: "ai-development/aid-2026-328-session-evidence"
    canonical_scope_keywords:
      - "AID-2026-328"
      - "Issue #1462"
      - "gate ratchet"
      - "baseline anchoring"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Session Evidence — AID-2026-328

## Session role / use case

Implementation session for Issue #1462.

The task is to correct the ratchet exemption mechanism. The prior implementation
read the candidate working-tree baseline. The replacement contract anchors
the comparison to the pull-request base commit and prohibits candidate
baseline growth.

This record distinguishes authored implementation artifacts from commands
actually executed against a repository checkout. No local Git execution,
modified repository tree, successful Actions run, pull request, or merge is
claimed by this record.

## Actual AI input

The user supplied the following implementation requirements:

- Repository: `oahcom/AiMemoryBrainArchitecture`.
- Issue: `#1462`.
- Base-commit baseline authority.
- Candidate baseline may only shrink.
- Every unauthorized addition must be named.
- Missing base commit or missing base path must return exit 2.
- No new workflow or required context.
- Migrate the two existing ratchet invocations.
- Do not change `check_manifest_blob_pins.py` decision logic.
- Preserve existing tests and add T-a through T-f.
- Provide complete source files, workflow replacement fragments,
  work-item manifest, INDEX registration, and reproducible commands.

The supplied defect evidence identifies the old working-tree read,
the unrestricted `--baseline` path, and the two existing workflow call sites.

## Implementation decisions

### Baseline authority

The authoritative baseline is read from the resolved base commit:

    git show <resolved-base-commit>:<registered-baseline-path>

The candidate baseline is read separately and is treated only as a proposed
debt reduction. It is never permitted to introduce a new entry.

### Registered invocation identity

The two registered baseline identities are:

    manifest-blob-pins
      scripts/ci/baselines/manifest-blob-pins.txt

    bilingual-docs
      scripts/ci/baselines/bilingual-docs.txt

The supplied path must match the path registered for the invocation identity.
A path substitution is INCOMPLETE, exit 2.

### Comparison semantics

Blank lines and full-line comments are ignored.
Remaining entries use set semantics.
Candidate additions fail with exit 1 and are individually printed.
Candidate removals are allowed only when the corresponding failure is absent
from the current checker output.

The checker output is normalized without discarding the details after ` -> `.
A nonzero checker exit without reported failure items remains a failure.

### Failure semantics

    0 = comparison complete and ratchet holds
    1 = unauthorized baseline growth or failure-set violation
    2 = comparison incomplete or invocation invalid

No unanchored execution mode is introduced.

## AI-visible output

The session produced:

- A proposed complete replacement for `scripts/ci/gate_ratchet.py`.
- A proposed complete replacement for `scripts/ci/test_gate_ratchet.py`.
- Replacement fragments for the two existing workflow steps.
- Proposed explanatory-only changes to the two baseline headers.
- A work-item manifest and INDEX registration proposal.
- A self-verification command sequence.

These are authored artifacts, not evidence that the repository files have
already been committed or that the tests have executed successfully.

## Test plan

The required named tests are:

- `test_t_a_identical_base_and_candidate_baseline_passes`
- `test_t_b_removing_a_fixed_entry_is_legal_debt_repayment`
- `test_t_c_adding_an_entry_fails_and_names_the_original_line`
- `test_t_d_added_failure_and_added_baseline_still_fails`
- `test_t_e_missing_base_ref_is_incomplete_exit_two`
- `test_t_e_missing_path_in_base_is_incomplete_exit_two`
- `test_t_f_candidate_cannot_switch_the_registered_baseline_path`

Additional cases cover:

- Empty baseline and empty successful checker output.
- Nonzero checker exit with no failure items.
- Distinct failures on the same path.
- Failure details after ` -> `.
- Verdict-prefixed failure items.
- Symlink rejection.
- Comment and blank-line normalization.
- Existing bilingual baseline count consistency.

## Required negative control

The decisive negative control is T-d.

The test must create a real temporary Git repository with a committed base
baseline. It then adds a new failing manifest pin to the candidate baseline
and causes the underlying checker command to emit that same failure and
return exit 1.

The expected ratchet result is exit 1. The diagnostic must name the exact
newly added baseline line.

The checker must actually execute in this negative control. A baseline-growth
rejection without execution of the underlying checker is not sufficient
evidence for T-d.

## Validation status

Repository-side execution has not been recorded in this session.

Pending:

- Corrected final source files applied to the working branch.
- Full unittest execution.
- T-d manual reproduction.
- Both existing workflow jobs executing against their PR base commits.
- Existing required-context success readback.
- Independent exact-head review.
- Owner acceptance.

No merge, CI success, or Issue closure is claimed.

## Scope exclusions

This change does not:

- Modify `scripts/ci/check_manifest_blob_pins.py`.
- Increase either baseline's permitted failure set.
- Change the failure predicates of either underlying checker.
- Migrate `check_test_reachability.py` to `gate_ratchet.py`.
- Add a workflow, job, or required context.
- Introduce an unanchored or default-allow mode.
