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
      last_verified_date: "2026-11-26"
      last_verification_note: "Every figure in this record was produced by running the commands named beside it against branch fix/1223-declared-duplicate-blindness at HEAD 2425dd4. Suite counts, the mutation result and the gate verdicts are transcriptions of that output, not estimates."
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

# Session evidence — AID-2026-059 / Issue #1223

## Session role / use case

IMPLEMENTER. Repair one defect in `scripts/check_declared_check_contexts.py`:
a declared check-context line listed twice was invisible to the comparison, so
the gate printed PASS over a document that had stopped saying what its author
meant.

The session was executed by an AI agent. This record is the agent's report
about its own work, not a third-party attestation.

The defect belongs to a family this work item keeps finding — a check that
reports success over a fact it never read. #1061 (an entry the PR cited but did
not write) and #1076 (a precondition that compared a value to itself) are the
two earlier members. Here the unread fact is the *list*: the document was read,
then immediately collapsed into a set, and the collapse discarded the only
evidence that the document had changed.

## Actual AI input

The operative input is the assignment transcribed in
`14-ai-development/work-items/AID-2026-059/prompt-1223-v1.md`, pinned by digest
at 3961 bytes /
`5de7adc61dcb6659b16a4da5e35826cd635f616ad664654d327c9a1836cade95`. It names
the defect, the measured before-state, six constraints (minimum diff; exit code
1 not 2; keep existing messages; leave `fetch_protected_contexts` and its
endpoint untouched; no new dependency; no behaviour change outside the named
defect) and the acceptance criterion: a named test that goes red when the guard
is deleted.

## AI-visible output

**The commit.** One commit, `2425dd4`, on
`fix/1223-declared-duplicate-blindness` from `main = 9ee89b32`:

```
2425dd4 fix(1223): a duplicated declared-context line must fail, not collapse into a set
    scripts/check_declared_check_contexts.py      +22 -1
    scripts/test_check_declared_check_contexts.py +10
```

### The defect

`main()` read the fenced block into the list `contexts`, printed a notice using
`len(contexts)`, and then compared against the protected side as sets:

```python
undeclared = sorted(set(protection) - set(contexts))
unprotected = sorted(set(contexts) - set(protection))
```

A name listed twice contributes one element to the set, so the comparison could
not see the repetition. With one duplicate line added to the block, the run on
unmodified `main` produced:

```
17 declared check contexts, all produced by a job in .github/workflows and all required on main
DECLARED CHECK CONTEXTS: PASS
main() rc with 17 lines / 16 protected = 0
```

Seventeen declared lines, sixteen protected contexts, exit code 0. Both printed
statements were individually true — the notice counted the list (17), the
comparison used the set (16) — so no single line was wrong and the disagreement
between them was invisible. That is the "reports success over a fact it never
read" shape: the gate never read the list it had already parsed.

### Why it matters

A duplicated line is not a formatting nit. It means the document stopped saying
what its author meant, in one of two ways: a paste that overwrote a context
which is now missing, or a stale leftover from a rename that was applied in one
place and not the other. In the first case a required check has silently left
the declared set; in the second the document claims a check that no longer
exists under that name. Both are exactly what this gate exists to catch, and
the set comparison was structurally unable to catch either — dropping a line or
repeating one can only make a subset test truer.

### The fix

The guard is computed from the list before the collapse, quoted verbatim from
`git show 2425dd4 -- scripts/check_declared_check_contexts.py`:

```python
    # A line listed twice is invisible to the set comparison below: the sets
    # still match, so a copy-paste that overwrote a missing context reads as
    # PASS. The duplication is itself the disagreement, so it fails on the list.
    duplicates = sorted({context for context in contexts if contexts.count(context) > 1})
    if duplicates:
        for context in duplicates:
            print(
                f"::error::{DOC_PATH} declares required check context "
                f"{context!r} more than once; the document no longer says what "
                "its author meant it to say",
                file=sys.stderr,
            )
        print(
            f"DECLARED CHECK CONTEXTS: FAIL (declared {len(contexts)}; "
            f"{len(duplicates)} duplicated)",
            file=sys.stderr,
        )
        return 1
```

The exit code is `1`, not `2`. The document is readable and its content is
wrong — one `::error::` per duplicated name, which is the VIOLATION vocabulary.
`2` remains reserved for `INCOMPLETE`, where the condition could not be read at
all (the credential case, the transport case). Collapsing a content error into
"could not check" would let a wrong document report itself as unevaluated, and
a caller that treats `2` as retryable would retry forever.

The docstring's exit-code table gained one line so the vocabulary states the
new case: `1  VIOLATION   a declared context is produced by no job, is listed
twice, or the sets differ`.

### Mutation result

Before the fix, and after it, on the same input (one duplicate line added to the
real 16-name block; protection side = the real 16 names):

| | declared lines | unique | verdict | rc |
|---|---|---|---|---|
| baseline, pre-fix | 16 | 16 | PASS | 0 |
| mutated, pre-fix | 17 | 16 | PASS | 0 |
| baseline, post-fix | 16 | 16 | PASS | 0 |
| mutated, post-fix | 17 | 16 | `FAIL (declared 17; 1 duplicated)` | 1 |

The post-fix mutant emits one error line naming the duplicated context:

```
::error::14-ai-development/PR-GOVERNANCE-001.md declares required check context 'GOV-DOC-001 structural checks' more than once; the document no longer says what its author meant it to say
DECLARED CHECK CONTEXTS: FAIL (declared 17; 1 duplicated)
```

Independent mutation check — the guard block deleted from the working tree, the
test suite run, the file restored and verified byte-identical afterwards
(`sha256` of the file before and after the mutant matched):

```
MUTANT rc= 1
FAIL: test_violation_when_a_context_is_declared_twice (__main__.DeclaredCheckContextsTest.test_violation_when_a_context_is_declared_twice)
Ran 13 tests in 0.055s
FAILED (failures=1)
AssertionError: 0 != 1
restored_identical= True 7cda3054233f
```

Restoring the guard returns `Ran 13 tests in 0.048s` / `OK`. Exactly one test
goes red, and it is the one that names the defect; no other test moves.

### What was deliberately not done

- **`fetch_protected_contexts` and the `/branches/{branch}` payload are
  untouched.** #1224 requirement 1 owns whether the protected side is read
  through a different endpoint or a credential. This change compares the list
  it already had.
- **No new dependency.** Standard library only; the file still imports
  `json`, `os`, `re`, `sys`, `urllib.request` and `pathlib`.
- **The two set-difference directions and their wording are unchanged.** Both
  existing failure branches print exactly what they printed before, so no
  existing message-based assertion moves.
- **The duplicate check runs after the produced-context check, not before.** An
  unproduced context is the more specific complaint; a document with both
  problems should report the missing one first, and the ordering keeps the
  existing first-failure behaviour stable.

### Gate results

```
python -m unittest discover -s tests/session_evidence -p "test_*.py"
    Ran 98 tests in 0.506s
    OK

cd scripts && python test_check_declared_check_contexts.py
    Ran 13 tests in 0.048s
    OK

python scripts/ci/check_line_endings.py
    Line-ending check: 1404 files inspected, 0 binary skipped, 0 violations.

python scripts/ci/check_repository_hygiene.py
    Work-item index membership version=2026-11-24.8 directories=67 linked=67
    Work-item manifest consistency version=2026-11-24.8 manifests=56 in_scope=54 excluded_by_record_type=2 unrecognized=0 violations=0
    Repository hygiene check passed (version=2026-11-24.8).

python scripts/check_declared_check_contexts.py        # live, no token in this environment
    ::error::INCOMPLETE: the branch-protection payload could not be read, so the declared set cannot be compared to it: HTTPError: HTTP Error 403: rate limit exceeded
    rc=2
```

The live run returns `2`, not `0`: the environment has no `GITHUB_TOKEN`, the
anonymous GitHub API rate limit was already spent, and `2` is the correct
verdict for "the condition could not be evaluated". The PASS path is not
untested — it was verified against the real document by supplying the
document's own 16 names as the protection side, which is the same comparison
with the network removed:

```
16 declared check contexts, all produced by a job in .github/workflows and all required on main
DECLARED CHECK CONTEXTS: PASS
rc=0
```

So `PASS` on the real block means "this 16-name document has no duplicate", not
"the fix did nothing". The fix changed what happens to a 17-line block, and that
case returns `1`.

`python scripts/check_document_management.py` and
`python scripts/check_bilingual_docs.py` were run and are reported separately in
the pull request; both stop on this host because the clone is shallow
(`git rev-parse --is-shallow-repository` → `true`), which they state in their own
words rather than as a violation of these two documents.
