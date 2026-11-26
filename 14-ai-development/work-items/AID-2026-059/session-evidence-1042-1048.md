---
document_metadata:
  domain: ai-development
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
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every figure in 'AI-visible output' was produced in this session by running the commands named there against this branch. The suite counts, the three mutation results, the gate verdicts and the digest are transcriptions of that output, not estimates."
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

# Session evidence — AID-2026-059 / Issues #1042, #1045, #1047, #1048

## Session role / use case

IMPLEMENTER. Close the four residuals left open after Issue #799's session
evidence gate landed. Each residual is a place where a check reported success
over a fact it never read: the manifest was picked by a body-wide regex
(#1042), the workflow-shape violation quoted the one correct line in the step
(#1045), a duplicate digest was unvalidated and the check numbers were
unmapped (#1047), and the new-file gate had no root-level shape rule (#1048).

The session was executed by an AI agent. This record is the agent's report
about its own work, not a third-party attestation.

## Actual AI input

The operative input is the assignment transcribed in
`14-ai-development/work-items/AID-2026-059/prompt-1042-1048-v1.md`, pinned by
digest at 6507 bytes /
`ceae6530d70c60803b58ba91a3f5ed28671a525bcc640c32aa8f020d3defaffd`. It
names the four defects, the required behaviour per Issue, and the three
session constraints, and it forbids scope beyond them.

Per Issue, as instructed:

- **#1042** — `_manifest_path_from_pr` must read the `Work Item ID` field via
  `_extract_field` instead of grepping the body for the first
  `AID-\d{4}-\d{3}`; accept the literal `NONE` only with
  `AI-assisted work: NO`; reject anything that is neither `AID-YYYY-NNN` nor
  `NONE`; return `str | None`; when `None`, print
  `AI-SESSION-EVIDENCE: PRESENT (no Work Item declared; manifest and session-evidence entry checks not applicable)`.
  No `work item` alias in `FIELD_ALIASES` — a `## Work Item` heading carries a
  task title, so the two fixtures that used it are corrected to
  `## Work Item ID`.
- **#1045** — `_checkout_refs` must append the offending `ref:` line,
  defaulting to the `uses:` line so the expression stays total, and the new
  test must assert the full
  `ref: ${{ github.event.pull_request.base.sha }}` value rather than the token
  `ref:`.
- **#1047** — annotate the top-level `prompt_id` / `prompt_sha256` as
  non-normative (keep them: historical manifests must not be rewritten) and
  add a check-number table to `validate.py` for `01/02/03/04/06/09/11`, with
  no renumbering.
- **#1048** — refuse a new path whose parent is the repository root and whose
  name begins with `_` or `.`; keep the rule root-scoped; keep `/_dm.txt` in
  `PROHIBITED_PATHS`; keep the two rejection reasons distinguishable; bump
  `CHECK_VERSION` to `2026-11-24.8`.

Three constraints governed the work and the acceptance criteria are stated
against them: no unrequested abstraction (the smallest edit that changes the
reported behaviour); each fix carries a mutation check (revert the fix, the
new test must fail); no behaviour change outside the four defects.

## AI-visible output

**What changed, by commit.** Five commits on `fix/session-evidence-residuals`,
based on `main` at `adb31099470fe688f96e50dc0c733652477f6cbb`:

```
40aa5ac7933253c0b25dad3cce11830d7f058637  test(session-evidence): declare the Work Item ID field the resolver reads
66df557fb319db8365d64dfd7b2d477db5c99be5  fix(session-evidence): read the Work Item ID field instead of grepping the body
242287a01d671268c0cdc2ab79ffebb933bdcf92  fix(ci): refuse root-level underscore and dot files as new paths (#1048)
a82ad0ade4a5756c7d8f43d19ef6bcc3ea56082e  docs(session-evidence): mark the top-level prompt hash non-normative and map the check numbers (#1047)
8cff88ad9923dd9b33b25b8cabc87cc71a30885b  fix(ci): name the offending ref: line in the workflow-shape violation (#1045)
```

- `scripts/governance/session_evidence/validate.py`: `_manifest_path_from_pr`
  reads the field, validates `NONE` against a `NO` declaration, returns
  `str | None`, and the `None` branch prints the qualified PRESENT verdict;
  the module docstring gains the check-number table. (#1042, #1047)
- `tests/session_evidence/test_validate.py`: four tests for #1042, and the two
  pre-effective fixtures changed from `## Work Item` to `- Work Item ID:`
  (#1042, 40aa5ac7).
- `scripts/check_session_evidence_workflow_shape.py` and its test: the
  offending `ref:` line is appended; the new test pins the full expression.
  (#1045)
- `scripts/ci/check_repository_hygiene.py` and its test: `is_root_scratch_path`
  plus the root-scoped rejection branch, two distinguishable reasons, version
  `2026-11-24.8`. (#1048)
- `14-ai-development/prompt-and-evidence-template.md`: the non-normative note
  in the YAML block and in section 3.2, in both languages. (#1047)
- `14-ai-development/work-items/AID-2026-059/`: this document, the prompt
  snapshot, and the fourth `session_evidence` entry.

**Verification actually run on this branch.**

```
python -m unittest discover -s tests/session_evidence -p "test_*.py"
    Ran 89 tests in 0.522s
    OK
```

```
cd scripts && python -m unittest test_check_session_evidence_workflow_shape
    Ran 10 tests in 0.016s
    OK
```

```
python -m unittest scripts.test_check_repository_hygiene
    Ran 93 tests in 53.288s
    OK (skipped=1)
```

```
python scripts/check_session_evidence_workflow_shape.py
    ::notice::.github/workflows/session-evidence.yml has the three independent jobs self-test-trusted-base, self-test-pr-head, validate; the head job carries no `ref:`, the verdict job carries no `needs:`
    SESSION EVIDENCE WORKFLOW SHAPE: PASS
```

```
python scripts/ci/check_repository_hygiene.py \
    --base adb31099470fe688f96e50dc0c733652477f6cbb \
    --head <HEAD>
    Work-item index membership version=2026-11-24.8 directories=55 linked=55
    Work-item manifest consistency version=2026-11-24.8 manifests=44 in_scope=42 excluded_by_record_type=2 unrecognized=0 violations=0
    Repository new-file admission version=2026-11-24.8 base=adb31099470fe688f96e50dc0c733652477f6cbb head=<HEAD> merge_base=adb31099470fe688f96e50dc0c733652477f6cbb
    Repository new-file admission passed: 2 new path(s) checked.
```

```
python scripts/ci/check_line_endings.py
    Line-ending check: 1350 files inspected, 0 binary skipped, 0 violations.
```

**Mutations run, one per code fix.**

```
#1042  reverted validate.py to 66df557f^ (the body-wide regex resolver)
    python -m unittest tests.session_evidence.test_validate.SessionEvidenceValidatorTests.test_declared_work_item_id_binds_over_a_prose_mention
        Ran 1 test in 0.006s
        FAILED (failures=1)
        AssertionError: '14-ai-development/work-items/AID-2026-003/manifest.yaml'
                     != '14-ai-development/work-items/AID-2026-055/manifest.yaml'
```

```
#1045  reverted scripts/check_session_evidence_workflow_shape.py to 8cff88ad^
    cd scripts && python -m unittest test_check_session_evidence_workflow_shape
        Ran 10 tests in 0.019s
        FAILED (failures=1)
        test_head_job_checkout_with_ref_names_the_ref_line:
        AssertionError: 'ref: ${{ github.event.pull_request.base.sha }}' not
        found in "... declares a `ref:` key (uses: actions/checkout@v4); ..."
```

```
#1048  reverted scripts/ci/check_repository_hygiene.py to 242287a0^
    python -m unittest scripts.test_check_repository_hygiene -k new_root_underscore
        Ran 1 test in 0.632s
        FAILED (failures=1)
        AssertionError: 0 != 1 : stdout:
        Version 2026-11-24.7 ...
        Repository new-file admission passed: 1 new path(s) checked.
```

Each mutant was restored with `git checkout --` immediately after it was
measured, and `git status` was clean before the bundle was written.

No mutation was run for **#1047**: the change is a docstring table and
template prose, and it alters no control flow, so there is no behaviour to
revert. The "no mutation for #1047" statement is deliberate, not an omission.

**What could not be verified.**

- The workflow reads the validator from the **base** revision, so the first CI
  run of this pull request exercises the base copy, not the code changed here.
  That is the gate's security property, recorded rather than worked around.
- Three of the four Issues (#1042, #1045, #1048) are attested by an offline
  mutation each, not by an independent reviewer. `independent_reviewer` stays
  `NOT_ASSIGNED` in the work item.
- The new tests exercise the validators through fixtures; they do not exercise
  the GitHub API, the workflow file as executed by Actions, or branch
  protection.
