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
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every count in the output section was read from the live protection payload or from the check runs of the named pull request on 2026-11-25, and the two local commands were re-run on this branch before the pull request was opened."
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

IMPLEMENTER. Implement stage B of WO-01 for REQ-01 / Issue #262: correct
`PR-GOVERNANCE-001` section 7 so that the declared required-context set equals the
set the platform enforces, with the delta attributed and dated.

This work item does not touch branch protection, does not run the
deliberately-failing-head experiment, and does not change any other section of
the document.

# Actual AI input

**Committed, byte-exact.** `prompt-v1.md` in this directory is the instruction
this change was executed against. It is the file the manifest pins by digest.

**Recorded, not committed.** The measurements that instruction depends on were
taken through the GitHub REST API in the same session and are quoted inside
`prompt-v1.md`, so a reader does not have to trust a summary:

| observation | value |
|---|---|
| required contexts before this change | 15 |
| required contexts after this change | 16 |
| check runs on merged #1024 (docs-only) | 15, `rust-workspace-test` absent |

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed
file has not changed since it was pinned, not that it is byte-for-byte what the
executing session read.

Two standing directives governed the session and are reproduced verbatim because
the acceptance criteria are stated against them:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可。

> 不能自己动手写代码。

# AI-visible output

One production file changed:

```
14-ai-development/PR-GOVERNANCE-001.md        section 7 only
```

What moved: the enforced-set sentence (twelve to sixteen), the machine-read
declaration block (four names appended), the deliberately-failing-head sentence
carrying the 16-context figure, the dated measurement header, and one new
paragraph in each language attributing the increment.

What did not move: section 7's statement that pull-request reviews are not
enforced, the `required_pull_request_reviews` reasoning, the Issue #134
paragraph, and every other section of the document.

Verification actually run on this branch, at the stated head:

```
python3 scripts/check_declared_check_contexts.py
    ::notice::16 declared check contexts, all produced by a job in .github/workflows
    DECLARED CHECK CONTEXTS: PASS

python3 scripts/check_document_management.py --require-changed <merge-base>
    PASS (incremental): no GOV-DOC-002 violations; 207 classified, 493 unclassified
```

Read back from the platform before and after the change:

```
before 15 -> PUT -> verified contexts : 16
strict True | enforce_admins True | allow_force_pushes False
allow_deletions False | required_pull_request_reviews None
READBACK PASS
```

# Limitations

1. **The measurement is a snapshot.** `2026-11-25` is the date the payload was
   read. A later change to branch protection makes the count stale, and this
   document says so at the point of use rather than promising the number is
   permanent.
2. **Correctness of the count is not enforced by anything.** No machine gate
   compares the declaration against the protection payload.
   `check_declared_check_contexts.py` compares the declaration against the
   workflows and nothing else, so a future divergence between the two sets would
   pass every automated check in this repository.
   **Superseded, `2026-11-25` (Issue #1029, PR #1088, merge commit
   `20adc016`):** that script now reads `GET /branches/main`, takes
   `protection.required_status_checks.contexts` from the payload, and compares
   in both directions: `undeclared` is the set the platform requires but the
   declaration omits, `unprotected` is the set the declaration names but the
   platform does not require. Either being non-empty fails the gate with exit
   1; a payload that cannot be read, or reads empty, exits 2 (INCOMPLETE)
   instead of passing; exit 0 is reserved for the two sets being equal. Its
   docstring names Issue #1029 as the defect class it closes. Measured on
   `main` it reports 16 declared, 16 protected, PASS, exit 0 — so this gap is
   closed and the sentence above describes the state before the change.
3. **The unproven half stays unproven.** A required context that fails is still
   not shown to block a merge, because the deliberately-failing-head experiment
   has not been run. Correcting the count does not correct that.
   **Superseded, `2026-11-25` (Issue #1029, PR #1038):** the experiment has
   been run. PR #1038 added one always-failing `#[test]` at head `b5cf4f25`;
   `PUT /repos/oahcom/AiMemoryBrainArchitecture/pulls/1038/merge` returned
   HTTP 405 with `Required status check "rust-workspace-test" is failing.`
   and the pull request was closed unmerged. `PR-GOVERNANCE-001.md:288`
   records it as passed and dated `2026-11-25`. The boundary that record
   states applies here too: the experiment proves the normal path on that
   date with that payload, not that a bypass route or a renamed job behaves
   the same, and it must be re-run after any material change to the
   protection configuration or to the producing workflows — so this gap is
   closed for that date and the sentence above describes the state before the
   change.
