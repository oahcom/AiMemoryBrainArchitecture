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
      last_verification_note: "Every command and count in the output section was run on this branch after the gate merged to main at ebadbe84. The input section distinguishes what is committed (prompt-v1.md, byte-exact) from what is only recorded (the five source prompts, which are not in the repository)."
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

IMPLEMENTER. Implement deliverable A of Issue #799: an unconditional `pull_request`
check that requires AI session evidence in the PR description, in every linked
Issue, and in the Work Item manifest. Deliverable B, the independent trusted
verifier tracked by #859, is out of scope.

# Actual AI input

Two classes of input exist for this session, and they are not interchangeable.

**Committed, byte-exact.** `prompt-v1.md` in this directory is the consolidated
instruction set for the delivered code: the standing directives, the task, the
ten frozen constraints, and the repository constraints that were discovered
while implementing. It is the file the manifest pins by digest:

| file | bytes | sha256 |
|---|---:|---|
| `14-ai-development/work-items/AID-2026-059/prompt-v1.md` | 3866 | `65474e7f0927d2dfeaad33814fdbd7d576635cc8a0e8d2a3a7441e3a65ab7317` |

**Recorded, not committed.** The session that produced the code was driven by
five source prompt files. They are not committed because each embeds a
whole-repository snapshot — pasted file contents the implementer had to read —
and committing them would duplicate the tree inside the tree. Their sizes are
recorded so a reader can ask for the originals rather than trust a summary:

| # | prompt file | bytes | what it asked for |
|---|---|---:|---|
| 1 | `A_impl.md` | 24576 | first implementation: workflow plus validator plus tests |
| 2 | `A_fix7.md` / `A_fix8.md` | 56217 / 57332 | repair the fixture failures that kept three tests red |
| 3 | `A_unittest2.md` | 39834 | migrate the suite from pytest to unittest; the repository has no pytest |
| 4 | `A_dedupe2.md` | 94515 | delete the dead code that combination mutation exposed |
| 5 | `A_r9.md` | 8519 | close the two false-green tests by scoping the fixture |

`prompt-v1.md` was assembled after the session from those files. That is why the
manifest records `executed_prompt_provenance: NOT_VERIFIED`: the digest proves
the committed file has not changed since it was pinned, not that it is
byte-for-byte what any model received.

Two directives governed the whole session and are reproduced verbatim because
the acceptance criteria are stated against them:

> 端口上所有产出必须能被变异检验打穿；全绿不是证据。

> 不要写新逻辑，只做机械删除。

# AI-visible output

Four files, all merged to `main` as `ebadbe84`:

```
.github/workflows/session-evidence.yml                     58 lines
scripts/governance/session_evidence/validate.py          2038 lines
tests/session_evidence/support.py                         278 lines
tests/session_evidence/test_validate.py                   971 lines
```

Verification actually run on this branch:

```
python3 -m unittest discover -s tests/session_evidence -p "test_*.py"
    Ran 60 tests in 0.29s
    OK

mutation sweep, 16 mutants, survivors: none
    compare truncation / 300-file limit / git-tree truncation / provenance enum /
    path-not-in-tree / absolute path / SHA-256 comparison / byte count / blob type /
    git mode / empty size / backslash / percent encoding / URL scheme /
    absent AI-assisted work value / non-YES/NO AI-assisted work value

python3 scripts/ci/check_test_reachability.py
    60 test files, 60 reachable, 0 unreachable
```

Three facts about this delivery are stated here rather than left for a reader to
discover:

1. **The pull request that installs the gate cannot be validated by it.** The job
   checks out the base revision, and the validator does not exist at that revision
   until the pull request merges. `#965` merged with `Session Evidence` red for
   that reason, documented in the ruling on that pull request rather than repaired
   by making the check report success over a validator it never ran.
2. **The first real run found a defect the suite could not see.** With the gate
   merged, this pull request's run reached `Validate session evidence` and failed
   with `MISSING: Cannot decode blob bytes: .../manifest.yaml`. The REST API wraps
   its base64 payload at 60 characters; `gh_blob_bytes` passed the wrapped string
   to `base64.b64decode(..., validate=True)`, which rejects newlines. Every real
   file larger than one line therefore failed to decode, while the fixtures —
   which encoded short blobs with no wrapping — passed. Fixed by stripping the
   whitespace before decoding, with one test that hands the validator the payload
   shape the API actually sends; reverting the fix fails that test and no other.
   This is why Issue #799 requires calibration on a real pull request instead of
   accepting a green suite as evidence.
3. **This pull request is the first one the gate reads end to end.** Its base
   contains the validator, so the self-test runs for real here, and the verdict it
   prints is produced by the delivered code rather than asserted by the author.
4. **The gate only proves structure and presence.** It does not prove that this
   record was not edited afterwards, that the content is complete, or that the
   model identity is real. Those are reviewer judgements, and this file is written
   to be usable as material for that judgement: what was asked, what came back,
   and what could not be obtained.
