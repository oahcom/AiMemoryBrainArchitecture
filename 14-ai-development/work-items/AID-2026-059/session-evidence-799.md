# Session role / use case

IMPLEMENTER. Implement deliverable A of Issue #799: an unconditional `pull_request`
check that requires AI session evidence in the PR description, in every linked
Issue, and in the Work Item manifest. Deliverable B, the independent trusted
verifier tracked by #859, is out of scope.

# Actual AI input

The instruction set below is the sequence that actually drove the delivered code.
The full prompt files are not committed: each embeds a whole-repository snapshot
(pasted file contents the implementer had to read), and committing them would
duplicate the tree inside the tree. Their names, byte counts and digests are
recorded so a reader can ask for the originals rather than trust this summary.

| # | prompt file | bytes | what it asked for |
|---|---|---:|---|
| 1 | `A_impl.md` | 24576 | first implementation: workflow plus validator plus tests |
| 2 | `A_fix7.md` / `A_fix8.md` | 56217 / 57332 | repair the fixture failures that kept three tests red |
| 3 | `A_unittest2.md` | 39834 | migrate the suite from pytest to unittest; the repository has no pytest |
| 4 | `A_dedupe2.md` | 94515 | delete the dead code that combination mutation exposed |
| 5 | `A_r9.md` | 8519 | close the two false-green tests by scoping the fixture |

Two directives governed the whole session and are reproduced verbatim because
they are what the acceptance criteria are stated against:

> 端口上所有产出必须能被变异检验打穿；全绿不是证据。

> 不要写新逻辑，只做机械删除。

# AI-visible output

The four files in `scope.files_to_create` of this work item's manifest:

```
.github/workflows/session-evidence.yml                     58 lines
scripts/governance/session_evidence/validate.py          2040 lines
tests/session_evidence/support.py                         278 lines
tests/session_evidence/test_validate.py                    913 lines
```

Verification actually run, on this branch:

```
python3 -m unittest discover -s tests/session_evidence -p "test_*.py"
    Ran 57 tests in 0.288s
    OK

mutation sweep, 14 mutants, survivors: none
    compare truncation / 300-file limit / git-tree truncation / provenance enum /
    path-not-in-tree / absolute path / SHA-256 comparison / byte count /
    blob type / git mode / empty size / backslash / percent encoding / URL scheme

python3 scripts/ci/check_test_reachability.py
    60 test files, 60 reachable, 0 unreachable

python3 scripts/ci/check_repository_hygiene.py --base <base> --head <head>
    Work-item index membership directories=47 linked=47
    Repository new-file admission passed

python3 scripts/ci/check_line_endings.py
    1302 files inspected, 0 violations

python3 scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/bilingual-docs.txt
    baseline=77 current=77 regressions=0 fixed=0 | PASS
```

What the delivery does not have, stated here rather than left for a reader to
discover: no frozen prompt snapshot, so `executed_prompt_provenance` is
`NOT_VERIFIED` and the digest below pins this record, not the original inputs.
The false-green finding (F2 in the manifest) is the reason the acceptance
criteria are mutation results and not a test count: the suite was green at 74
tests while two of them never entered the branch they named.
