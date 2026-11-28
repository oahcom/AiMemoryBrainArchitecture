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
        - "14-ai-development/work-items/AID-2026-332/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Workflow execution and exact-head CI evidence are pending."
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
    canonical_scope: "Implementation and verification record for AID-2026-332."
    canonical_scope_id: "ai-development/aid-2026-332-gov-doc-001-step-split-evidence"
    canonical_scope_keywords:
      - "AID-2026-332"
      - "GOV-DOC-001"
      - "owner-namespace references"
      - "governance-operation traceability"
      - "workflow step split"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-332 — Evidence

## Purpose

This work item implements the workflow-level portion of #1237 AC3:
CI must report distinct named results for the two GOV-DOC-001 checks.

The change is limited to `.github/workflows/bilingual-docs.yml`. It separates
the previously combined workflow step into one step for #1196 owner-namespace
references and another for #1208 governance-operation traceability.

## Baseline

The supplied baseline is `origin/main` at:

`4a6cdd0e7c5dc0db53be37a2f945e02c59d5abf9`

The branch is:

`fix/2026-11-28-govdoc001-split-checkers`

It is based on `origin/main`. If `origin/main` advances before the branch is
pushed, the planned integration method is merge rather than rebase, so the
recorded base and implementation commit identities are not rewritten by a
rebase.

## Original combined workflow step

The original step in `.github/workflows/bilingual-docs.yml` was:

```yaml
      - name: Run required Owner namespace and governance traceability gates
        run: |
          python3 scripts/check_owner_namespace_references.py --check
          python3 scripts/check_governance_operation_traceability.py --check
          (cd tests && python3 -m unittest -v test_check_owner_namespace_references.py)
          (cd tests && python3 -m unittest -v test_check_governance_operation_traceability.py)
```

This combined four commands under one workflow step. A failure was associated
with the combined step rather than producing two independently named
workflow-step results.

## Intended split

The replacement consists of two independently named steps.

The #1196 owner-namespace step runs:

```bash
(cd tests && python3 -m unittest -v test_check_owner_namespace_references.py)
python3 scripts/check_owner_namespace_references.py --check
```

The #1208 governance-operation step runs:

```bash
(cd tests && python3 -m unittest -v test_check_governance_operation_traceability.py)
python3 scripts/check_governance_operation_traceability.py --check
```

Within each step, the corresponding unit test runs before its checker.
Both commands are attempted, and the step exits unsuccessfully if either
command fails. The `(cd tests && ...)` form is retained because the test
modules are run from the `tests` directory, while the checker scripts are
invoked from the repository root.

## CI observability change

Before the split, the four commands shared one workflow step and therefore
one named step result. The workflow did not expose separate named outcomes
for the #1196 and #1208 checks.

After the split, the workflow is intended to expose two named outcomes:

- `Test and check #1196 owner-namespace references`
- `Test and check #1208 governance-operation traceability`

This separates the CI reporting and failure boundary for the two checks.
It does not by itself prove that either checker passes, that all canonical
root and EN/ZH-CN mirror cases are covered, or that the positive and negative
fixtures demonstrate the required boundaries.

## Accompanying repair: AID-2026-016 manifest schema regression

This PR also carries a narrowly scoped repair for the pre-existing
manifest-schema regression on `origin/main`. The required
`Work Item manifest schema (read-only baseline)` context was failing because
`14-ai-development/work-items/AID-2026-016/manifest.yaml` lacked the required
top-level `documentation` and `implementation` keys. This baseline failure
blocked PRs independently of the GOV-DOC-001 workflow change.

The AID-2026-016 manifest was updated with a `documentation` section listing
its five existing work-item records and an `implementation` section recording
the implementation status, factual summary, three changed source files, and
three recorded test results. No implementation or test source files for
AID-2026-016 were changed by this accompanying repair.

The schema checker was run locally on the updated tree using
`check_work_item_manifest_schema.py --tree HEAD --baseline 14-ai-development/reports/work-item-manifest-ac4-baseline.json`.
It reported `Legacy ratchet new regressions: 0` and exited `0`.

This result establishes that the updated tree introduces no new regressions
under the local manifest-schema ratchet invocation. It does not establish
that `origin/main` has been repaired, that the required context has passed
on this PR's exact head in GitHub Actions, or that the GOV-DOC-001 workflow
change has passed CI. The AID-2026-016 manifest repair is included here as a
supporting repository-hygiene correction; it does not change the scope or
acceptance criteria of #1237 AC3.

## Local execution boundary

The operator environment is Windows PowerShell with Python 3.12. WSL is
prohibited. The GitHub Actions workflow cannot be run locally in this
environment, so the workflow steps have not been locally executed as a
workflow.

No local workflow pass is claimed. No exact-head GitHub Actions result is
claimed in this evidence record.

## Verification still required

The following evidence remains necessary:

- The workflow change is committed and pushed.
- The relevant GitHub Actions workflow runs on the exact PR head.
- CI reports separate results for the #1196 and #1208 named steps.
- Both checks are shown to run against the canonical root and EN/ZH-CN
  mirrors and to fail closed.
- Positive and negative fixtures demonstrate each check's intended boundary.
- Any update to #1196 or #1208 is made only after the corresponding check is
  merged and exact-head CI evidence is available.

## Status boundary

This record documents the intended workflow change and the verification
boundary. It does not claim that CI has passed, that the full #1237 AC3 is
satisfied, or that #1196 or #1208 can be closed.
