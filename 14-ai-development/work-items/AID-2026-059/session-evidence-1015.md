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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every exit code and message in the output section was produced by running scripts/check_session_evidence_workflow_shape.py against this branch on 2026-11-25, before and after each of the three mutations. The unmutated baseline was re-run after restoring the file, and `git status --porcelain` confirmed the workflow file itself was unmodified."
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

# Session role / use case

IMPLEMENTER. Issue #1015: `.github/workflows/session-evidence.yml` was split into three
independent jobs by PR #1014 to end a defect that had produced 18 consecutive failing runs.
Nothing prevented it being collapsed back, and the collapse was silent — the gate keeps
reporting PASS while it has stopped being independent.

The session's job was to add a guard that fails when the workflow loses that shape, and to
prove the guard fires by mutating the artifact it guards rather than by reporting a green
test run.

# Actual AI input

The operative input was one dispatch brief, recorded byte-exact at
`14-ai-development/work-items/AID-2026-059/prompt-1015.md`:

| file | bytes | sha256 |
|---|---:|---|
| `14-ai-development/work-items/AID-2026-059/prompt-1015.md` | 8159 | `260ee8a814f480ac880569073f471c18ae88c528653fd747690b87f9fff6368b` |

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest pins the committed bytes, not
that they are byte-for-byte what any model received. The file is a transcription of the
brief, and a transcription can be faithful without being provably identical.

Three directives in that brief decided the shape of the delivery:

> It must NOT go in `tests/session_evidence/`. That directory is checked out from the
> **base** commit in CI by design, so a guard living there would itself be read from the
> base tree and would never see a change to the workflow in the PR under test.

> A guard tested only against the unmodified file proves nothing.

> Never claim a check is green without reading its conclusion.

The first is the reasoning that placed the script under `scripts/`, which is read from the
PR head like every other gate script. The second is why the output section below is a table
of mutations rather than a test count. The third is why the PR body states which contexts
were read to green and which were not.

# AI-visible output

Three files, plus one appended manifest entry and one added workflow step:

```
scripts/check_session_evidence_workflow_shape.py            216 lines   new
scripts/test_check_session_evidence_workflow_shape.py        141 lines   new
14-ai-development/work-items/AID-2026-059/session-evidence-1015.md      new
14-ai-development/work-items/AID-2026-059/prompt-1015.md                new
14-ai-development/work-items/AID-2026-059/manifest.yaml                 modified (+1 entry)
.github/workflows/repository-hygiene.yml                                modified (+2 steps)
```

**The guard.** Regex over the raw text of the workflow, the same approach as
`scripts/check_declared_check_contexts.py`, because the repository has no YAML parser
(PyYAML and node `yaml` both failed to install for a previous author) and adding a
dependency for one file would be the wrong trade. Exit codes follow the repository
vocabulary: `0` PASS, `1` VIOLATION, `2` INCOMPLETE. The INCOMPLETE branch is deliberate —
"workflow file not found" must never fall through to "no violations".

**Where it runs.** Two steps appended to the existing `Repository hygiene (hard gate)` job
in `.github/workflows/repository-hygiene.yml`, which triggers on
`pull_request: [opened, synchronize, reopened, ready_for_review]`. No job was added and no
`name:` was altered, so no required check context changed. The pair is the checker plus its
self-check, the same pairing the declared-check-contexts gate uses one block above.

**The measurement.** Each mutation was applied to `.github/workflows/session-evidence.yml`,
the checker was run, and the file was restored from a copy. The unmutated baseline was
re-run afterwards.

| # | mutation | exit | message |
|---|---|---:|---|
| 0 | none (baseline) | 0 | `SESSION EVIDENCE WORKFLOW SHAPE: PASS` |
| 1 | delete the `self-test-pr-head:` job block (lines 35–53) | 1 | `::error::job id 'self-test-pr-head' is missing from .github/workflows/session-evidence.yml; ... (job: self-test-pr-head)` |
| 2 | add `ref: ${{ github.event.pull_request.base.sha }}` to the head job's checkout | 1 | `::error::the 'self-test-pr-head' job's checkout step declares a `ref:` key (uses: actions/checkout@v4); ... (job: self-test-pr-head)` |
| 3 | add `needs: self-test-pr-head` to `validate` | 1 | `::error::the 'validate' job declares `needs:`; the verdict must not depend on another job, ... (job: validate)` |
| 0′ | restored | 0 | `SESSION EVIDENCE WORKFLOW SHAPE: PASS` |

`git status --porcelain` after restoration shows the workflow file unmodified, so the guard
is not passing by accident of a stale edit.

**Mutation 1 also had to prove it was not over-firing.** Deleting a job removes a block
that contains a `ref:` (the head job never had one, but the base job does), so a checker
that scanned the whole file would have reported assertion 2 as well and the operator could
not tell which property broke. It reports exactly one violation, naming the missing job id.

**Gates read, and their conclusions**, all run on this branch before the PR was opened:

| command | conclusion |
|---|---|
| `python3 scripts/check_session_evidence_workflow_shape.py` | PASS, exit 0 |
| `cd scripts && python3 -m unittest test_check_session_evidence_workflow_shape` | 9 tests, OK |
| `python3 scripts/ci/check_test_reachability.py` | 61 test files, 61 reachable, 0 unreachable |
| `python3 scripts/check_declared_check_contexts.py` | PASS, 12 contexts all produced |

The reachability figure moved from 60 to 61 because the new self-check is referenced by the
new `Self-check the session-evidence workflow shape gate` step; that gate's rule is that a
`test_*.py` no workflow executes is an unreachable test, and the step is what keeps this one
out of that set.

## What this record does not contain

- **No green `Session Evidence` verdict on its own PR.** The `Session Evidence` step
  currently has an ordering defect (issue #1026) that blocks any PR whose linked Issues all
  predate 2026-12-01, and #1015 was created on 2026-11-25. The entry below therefore
  attributes its evidence at PR scope with empty `issue_refs`, following the pattern
  `AID-2026-059` already uses for #799 rather than forcing a declaration to `NO`. Whether
  the context went green for #1026 or for this content is stated in the PR, not here, and
  is not claimed here.
- **No claim that the collapse is impossible.** The guard detects three named regressions.
  A fourth way to break the independence — for example a `validate` step that reads the head
  tree by some path other than `actions/checkout` — is not checked. The `ponytail:` note in
  the script names that ceiling: it is an indentation-based block scanner, not a YAML
  parser, so a `ref:` inside a `run:` block scalar would read as a key.
- **No session transcript.** Only this summarising document and the prompt snapshot are
  committed. The raw session was not.
- **No assertion that the workflow file's current content is correct.** The guard holds
  three properties. If the three-job shape were wrong in some fourth way, all three
  properties could hold and the guard would still pass, which is what a property check is
  and is not a substitute for reading the workflow.
