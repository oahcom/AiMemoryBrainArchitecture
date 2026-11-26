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
        - "14-ai-development/work-items/AID-2026-191/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Every number below was produced by running the commands shown at the head named in the manifest; the base-revision behaviour was produced by running the origin/main blob of the same script, not by reading it."
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
    canonical_scope: "Evidence for AID-2026-191: the repository-hygiene gate no longer reports a pass for new-file admission it did not run"
    canonical_scope_id: "ai-development/aid-2026-191-hygiene-silent-skip-evidence"
    canonical_scope_keywords:
      - "gate"
      - "hygiene"
      - "silent-skip"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-191 — the hygiene gate stops printing a pass for admission it did not run

## Scope and attribution

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base branch: `main`; base commit `4326669caa6c43193d34219a0451b80762b712ff`, read at branch
  creation and again before merge.
- Attribution: user-authorized operator (delegated by account owner). No natural-person Owner
  signature, acceptance or approval is asserted.
- Predecessor in the same batch: AID-2026-189 (PR #1339), the CI unit merged immediately before
  this one at the same commit.
- Files changed: `scripts/ci/check_repository_hygiene.py`,
  `scripts/test_check_repository_hygiene.py`, `.github/workflows/repository-hygiene.yml`, this
  registration set, and one appended `INDEX.md` row.

## The defect

`check_repository_hygiene.py` does two things under one name: a head-tree half (prohibited paths,
INDEX membership, work-item manifest consistency) and new-file admission, which needs a range. The
range was optional. When it was absent the script skipped admission and still printed
`Repository hygiene check passed`, the same sentence a full run prints. `.github/workflows/
repository-hygiene.yml` ran that script twice in the same job — once with no arguments and once
with `--base`/`--head` — so the job carried a step that was green by construction and a second
step doing the work the first step's name implied.

## Measurements

All four runs below are on the same working tree; the base-revision runs use the `origin/main` blob
of the script written to a temporary file, so the comparison is between code revisions and not
between remembered text.

| # | revision | invocation | exit | deciding line |
|---|---|---|---|---|
| 1 | base `4326669c` (`2026-11-24.8`) | none | **0** | `Repository hygiene check passed (version=2026-11-24.8).` |
| 2 | head (`2026-11-27.1`) | none | **2** | `Repository new-file admission SKIPPED (new-file admission requires --base and --head).` |
| 3 | head (`2026-11-27.1`) | `--base <origin/main> --head <HEAD>` | 0 | `Repository new-file admission passed: 0 new path(s) checked.` |
| 4 | head (`2026-11-27.1`) | `--head-tree-only` | 0 | `Repository hygiene head-tree checks complete (version=2026-11-27.1). New-file admission SKIPPED (new-file admission requires --base and --head).` |

Run 2 also emits `::error::repository hygiene cannot be determined: new-file admission requires
--base and --head` on stderr — the same annotation shape the script already used for its other
INCOMPLETE exits, so a CI reader finds it in the same place as every other undeterminable
condition.

Run 1 is the defect, measured: exit 0 and a pass sentence, with new-file admission never executed.
The base revision's own log shows it — the last three lines are the INDEX-membership line, the
manifest-consistency line, and the pass; there is no `Repository new-file admission` line at all.

## The decision the brief asked for, with its reason

Chosen: refuse in the script (option 1), not supply the range in CI alone (option 2).

Supplying the range at the one existing CI caller repairs that caller and leaves the script able
to print a pass for admission it did not run for everyone else. The callers were counted before
the choice: one unqualified invocation in `.github/` and 27 in the test module. The tests are the
same-program callers a future step would be copied from, so the output contract is where the lie
is, and that is where it was fixed.

Cost accepted, stated rather than hidden: the head-tree half now has to be asked for by name
(`--head-tree-only`). Deleting it was the alternative and it is a real check, so the flag keeps it
and four tests cover it. The 27 existing call sites were updated to name the mode rather than left
relying on a default that no longer exists.

The CI half was implemented as well, because the refusal makes an unqualified step red: the
duplicated pair collapses to one step that supplies the range.

## Measurements — the gate that has to stay green

- `python scripts/test_check_repository_hygiene.py` → `Ran 101 tests`, `OK (skipped=1)`, exit 0.
  Base revision: 97 tests. The one skip is pre-existing and platform-conditional
  (`test_newline_in_allowed_filename_is_handled_as_one_path`, "requires newline-capable
  filenames"), not one of the four added here.
- The four added tests: `test_unqualified_run_is_refused_not_reported_as_passed` (exit 2,
  `SKIPPED` line, and the old pass sentence must be absent), `test_head_tree_only_reports_the_skipped_half`
  (exit 0, `New-file admission SKIPPED`), `test_head_tree_only_still_rejects_a_prohibited_path`
  (exit 1, denylist message), `test_head_tree_only_cannot_be_combined_with_a_range` (exit 2).
- `.github/workflows/repository-hygiene.yml`, parsed as YAML on both revisions: `jobs` is
  `['repository-hygiene']` on both; the display name `Repository hygiene (hard gate)` is unchanged;
  steps 18 → 17. No job was added, renamed, merged or removed, so the sixteen declared required
  contexts are produced by the same jobs as before.
- `CHECK_VERSION` 2026-11-24.8 → 2026-11-27.1. This is a contract change, not an allowlist change,
  and the comment above the constant says so: without a distinct version string a reader cannot
  tell a 2026-11-24.8 PASS that skipped admission from one that performed it.

## Prohibitions honoured

- The decision logic taken when `--base` and `--head` are both present is untouched:
  `check_new_paths`, `is_allowed_new_path`, `is_root_scratch_path`, `check_prohibited_head_paths`,
  `check_index_membership` and `check_work_item_manifest_consistency` are byte-identical to the
  base revision. The diff to the checker is the CLI, `main()`'s new guard, the summary line and the
  version constant.
- No required context was added, removed or renamed.
- Branch protection was not read or written.
- No Issue was closed or reopened.
- No other checker, registry, baseline or workflow was touched.

## What this record does not claim

- It does not claim the gate was previously *passing* work it should have failed. New-file
  admission did run in CI, in the second step of the same job. The defect is that the first step
  claimed a check it had not performed, so deleting or breaking the second step would have left the
  job green with admission gone — the difference between a gate and a sentence.
- It does not claim the sixteen contexts were observed green from here; that is the PR's check-run
  record, and it is read from the API, not asserted in this file.
- It does not claim independent review.
