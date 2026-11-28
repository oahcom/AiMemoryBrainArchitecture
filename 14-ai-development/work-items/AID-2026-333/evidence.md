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
        - "14-ai-development/work-items/AID-2026-333/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Implementation and live race qualification remain pending."
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
      - "strict-branch-protection"
      - "duplicate-merge"
      - "acceptance-row-6"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-333 — Evidence

**Attribution:** user-authorized operator (delegated by account owner)

**Date:** 2026-11-27

**Issue:** #1341

**Related review:** #1497

**Related implementation:** #1477

**Observed base:** `cc3e9ed9dbe0eb860a583bc51d6b086248624766`

## 1. Decision

The original merge-queue ruling is withdrawn.

The ruleset creation request was rejected with HTTP 422 and:

```text
Invalid rule 'merge_queue':
```

The repository is public and owned by a GitHub user account. GitHub's documented merge-queue eligibility requires a public repository owned by an organization, or an eligible private organization repository.

The selected prevention mechanism is strict required-status-check branch protection.

The independent push detector is supplementary. It detects certain two-parent duplicate merges but cannot prevent them.

## 2. Round 1 — measured duplicate-claim experiment

The original scratch repository contained the real checker copied from origin/main.

B0 was the common baseline.

A added:

`AID-2026-999/manifest.yaml`

B independently added:

`AID-2026-999/evidence.md`

| Experiment | Exit code | Finding |
|---|---:|---|
| A PR gate against B0 | 0 | PASS |
| B PR gate against B0 | 0 | PASS |
| A push check, B0 → M1 | 0 | PASS |
| B revalidated against M1 | 1 | VIOLATION |
| Merge candidate containing A and B, M1 → M2 | 1 | VIOLATION |
| Post-merge push check, M1 → M2 | 1 | VIOLATION |

The second PR's explicit revalidation failed, but that revalidation was not mandatory under the measured branch-protection configuration.

### Variant 2 — same path, different content

Both independent PR checks:

`0 / 0`

Git merge before resolution:

`1`

After manual resolution retaining both INDEX rows:

- Merge candidate checker: `0`
- Post-merge checker: `0`

The tree-only checker compares path sets, not blob contents. A textual conflict was the only measured obstacle in that experiment.

## 3. Platform measurements

| Measurement | Result |
|---|---|
| REST repository visibility | `public` |
| Repository owner type | `User` |
| Ruleset POST with merge_queue | HTTP 422 |
| Ruleset GET | `[]` |
| `required_status_checks.strict` | `false` |
| GraphQL `requiresStrictStatusChecks` | `false` |
| Rulesets | `[]` |
| Merge queue configured | No |
| Required context `GOV-DOC-002 metadata checks` | Present |

The Administration-only protection endpoint exposes the strict setting. The endpoint available to the workflow's read-only token does not expose it.

Consequently, the workflow cannot independently attest that strict protection remains enabled.

## 4. Selected implementation

The original checker remains tree-only.

A separate push detector:

1. Enumerates commits in the push range.
2. Selects two-parent merge commits.
3. Finds each merge's two-parent merge base.
4. Compares the two parent trees against that base tree.
5. Reports AIDs newly present in both parents.
6. Reports both parent SHAs and subjects.

This detector is not a prevention mechanism. It is an independent post-merge alarm.

The actual prevention mechanism is strict branch protection, which forces an out-of-date PR to become current and obtain fresh required checks before merging.

## 5. Red-before / green-after regression evidence

The workflow-wiring regression was measured against the supplied `origin/main` workflow. The complete suite was then measured with all patch files applied.

| Test | Red-before result | After-patch result |
|---|---:|---:|
| Workflow wiring and strict limitation assertion | 1 test failed, exit 1 | Passed |
| Two-parent duplicate-claim detector | Not present in red-before run | Passed |
| Existing tests | Not part of the isolated red-before run | 10 tests: 9 passed, 1 pre-existing Windows interpreter-resolution failure |
| Complete suite | Not run as a complete suite | 11 of 12 passed; 1 failure |

Red-before command:

```bash
python -X utf8 scripts/ci/test_work_item_uniqueness.py \
  WorkItemUniquenessTreeTests.test_push_detector_is_wired_and_strict_limitation_is_recorded
```

Measured red-before result:

```text
Ran 1 test
FAILED (failures=1)
```

Assertion:

```text
AssertionError: 'Strict protection is an owner-side' not found in ... :
workflow must record strict protection as an external prerequisite
```

After-patch command:

```bash
python -X utf8 scripts/ci/test_work_item_uniqueness.py
```

Measured after-patch result:

```text
Ran 12 tests in 16.055s
FAILED (failures=1)
```

The sole failure was `test_checker_executes_only_rev_parse_and_ls_tree`: the test invokes the literal interpreter `python3`, which resolves to the Microsoft Store stub on this Windows host and exits 9009. The identical failure was reproduced using the unmodified `origin/main` test file and checker in a clean directory. It is therefore pre-existing and not introduced by this patch.

The new two-parent duplicate-claim detector test passed, and the workflow-wiring test passed. The required CI gate runs on `ubuntu-latest`, where `python3` is available; the CI result remains authoritative.

These are measured Windows results. They do not establish that the required Ubuntu CI run has passed.

## 6. Acceptance boundary

Row 6 is not yet accepted.

The owner must enable strict required-status checks on main.

After that setting is independently verified, the live experiment must establish:

- A and B independently pass against B0.
- A advances main.
- B becomes out of date.
- GitHub prevents B from merging using the stale required check.
- B's fresh required check runs against the advanced target.
- B's uniqueness check rejects the duplicate ID.
- A merges and B remains unmerged.

The supplementary detector must also be tested against a real two-parent duplicate merge in a scratch repository.

A successful local detector test is not a live GitHub prevention experiment.

No merge, owner acceptance, or closure of #1341 is asserted by this record.
