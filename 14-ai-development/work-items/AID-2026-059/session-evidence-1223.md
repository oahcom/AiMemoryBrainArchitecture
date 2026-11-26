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
      last_verification_note: "Every figure under 'Gate results' and 'Mutation' was produced in this session by running the commands named there against this branch. The mutation was run twice: once by the delegated implementation agent and once, independently, by the orchestrating session on a fresh copy of the tree."
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

IMPLEMENTER. Repair one defect: a duplicated line in the declared-context block
of a normative document reported `PASS`.

The shape is the one already recorded for #1061, #1063, #1076 and #1074 — a
check that reported success over a fact it never read. Here the unread fact is
**multiplicity**: `set()` collapses the declared lines before they are compared,
so a name listed twice leaves no trace in either difference set.

The session was executed by an AI agent. This record is the agent's report about
its own work, not a third-party attestation.

## The defect

`scripts/check_declared_check_contexts.py` reads the fenced block under a marker
in `14-ai-development/PR-GOVERNANCE-001.md` as a **list** (`declared_contexts()`),
then compares it to the platform's required contexts as a **set**:

```python
undeclared  = sorted(set(protection) - set(contexts))
unprotected = sorted(set(contexts) - set(protection))
```

Seventeen declared lines, sixteen unique names, sixteen protected names:

```
declared lines 17, unique 16, dupes ['GOV-DOC-001 structural checks']
::notice::17 declared check contexts, all produced by a job in .github/workflows
         and all required on main
DECLARED CHECK CONTEXTS: PASS
rc = 0
```

The notice reports `len(contexts)` — the **list**, 17. The comparison used the
**set**, 16. Both statements are individually true and the file is wrong. Nothing
in the output can tell a reader that the document lists one name twice.

## Why it matters here

The block is hand-maintained prose in a normative document. The change that added
this comparison (#1088) was itself a hand edit to that block, so a duplicated
line is the edit shape this file actually receives.

Two readings are possible when a duplicate appears, and both are defects: a
copy-paste that overwrote a still-missing context (the author meant to add a
seventeenth name and pasted an existing one), or a stale leftover that makes the
document stop saying what its author believed it said. The gate is the only thing
in the tree that could catch either, and it was the one thing that could not see
them.

This is strictly weaker than #1069's starting position, which the ruling on this
Issue records: there, the duplicate was invisible to *the only detector that
existed*, and #1090 closed it by adding a second detector. Here there is exactly
one comparison and it is set-based, so there is no other reader at all.

## The fix

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

Placement: after the "produced by a job" check and **before** the
`if protection is None:` platform read. That ordering is deliberate and is the
requirement recorded in the ruling on this Issue — a duplicated declaration is a
defect in the document, so it must fail whether or not the protected side is
reachable. Placing it after the fetch would let the same document pass on a
machine with no network, which is the false-PASS shape this file's own docstring
refuses.

Exit code `1`, not `2`. `2` is `INCOMPLETE`: a condition that could not be
evaluated at all. This condition was evaluated and the document is wrong, which
is `VIOLATION`. Classifying a known-wrong normative document as "could not
evaluate" would put it in the bucket reserved for infrastructure failure and let
it be retried instead of fixed.

## Mutation

Run twice, independently.

Deleting the guard block turns exactly one test red, and it is the named one:

```
MUT delete duplicate guard   ran=13 rc=1 fails=1
    FAIL test_violation_when_a_context_is_declared_twice
```

Restored:

```
RESTORED  ran=13 rc=0 fails=0
```

The failure is an `AssertionError`, not a traceback, so the test binds the guard
rather than the code path around it.

## Two directions, because one alone is satisfiable by a constant

The ruling on this Issue requires both, and both were measured:

```
(3) unmodified block, unmodified 16 names   -> declared 16, unique 16, rc = 0
(2) one line duplicated                     -> declared 17, unique 16,
                                               rc = 1
    ::error::... declares required check context
      'GOV-DOC-001 structural checks' more than once; the document no longer
      says what its author meant it to say
    DECLARED CHECK CONTEXTS: FAIL (declared 17; 1 duplicated)
```

A guard that returned `1` for everything would satisfy the second alone. The
first is what makes it a detector rather than a wall.

## What was deliberately not done

- `fetch_protected_contexts()` and the `GET /branches/{branch}` endpoint are
  untouched. #1224 records why the endpoint must stay: it needs only
  `contents: read`, and the `/protection` variant needs Administration (read) and
  is forbidden by this file's own docstring.
- The two existing set-difference directions and their message wording are
  unchanged, so no existing diagnostic was reworded.
- No new dependency. The guard uses a comprehension over a list of sixteen; the
  Issue's sketch used `Counter`, which is equivalent at this size and would have
  added an import for nothing.
- `declared_contexts()`'s return type and its `None` semantics are unchanged —
  `None` still means "block absent", which stays `INCOMPLETE`.

## Gate results

Run on this branch at HEAD `2425dd4`:

```
python -m unittest discover -s tests/session_evidence -p "test_*.py"
    Ran 98 tests ... OK                     (unrelated suite; no regression)

cd scripts && python test_check_declared_check_contexts.py
    Ran 13 tests ... OK                     (was 12; the guard's test is the 13th)

python scripts/check_declared_check_contexts.py
    ::notice::16 declared check contexts, all produced by a job in
              .github/workflows and all required on main
    DECLARED CHECK CONTEXTS: PASS
    rc = 0

python scripts/ci/check_line_endings.py
    1396 files inspected, 0 binary skipped, 0 violations

python scripts/ci/check_repository_hygiene.py
    Work-item manifest consistency version=2026-11-24.8 manifests=55
    in_scope=53 excluded_by_record_type=2 unrecognized=0 violations=0
    Repository hygiene check passed
```

The live `PASS` in the third block is **not** evidence that the fix does nothing.
The committed block has sixteen lines and sixteen unique names, so the guard is
correctly silent on it. The guard's behaviour is shown by the two-direction
measurement above, which injects the duplicate into a scratch copy and restores
the file afterwards (`git status --short` empty).

## AI-visible output

The commands above are the transcript. No figure in this document is an estimate:
the test counts are `unittest`'s own summary lines, the mutation rows are
`FAIL`/`OK` lines with the failing test named, and the duplicate detection line is
the program's own `::error::` output.
