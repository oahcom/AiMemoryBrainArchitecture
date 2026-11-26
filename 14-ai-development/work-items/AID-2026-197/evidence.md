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
        - "14-ai-development/work-items/AID-2026-197/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Every number below was produced by running the committed files in this work tree at base 4326669c (merge base 0c752ee6): the two gates before and after the fix, the two self-checks against both the fixed and the pre-fix script, and the ratchet against the shipped 77-entry baseline. No CI result, check-run status or merge outcome is claimed."
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
    canonical_status: Canonical
    canonical_scope: "The two gate defects DEF-gates-08 (check_source_revision_pointers.py) and DEF-gates-07 (gate_ratchet.py), what changed in each, and the measured before/after behaviour of both scripts"
    canonical_scope_id: "ai-development/aid-2026-197-source-revision-and-ratchet-item-fidelity"
    canonical_scope_keywords:
      - "gate"
      - "ratchet"
      - "source-revision-pointer"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-197/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-197/evidence.md"
---

# AID-2026-197 — Two gates that looked like they checked stopped doing what they claimed

**Status: DRAFT — dispatched, implemented, locally verified.** This record covers two
defects from the `gates` lane. Both were silent: each produced a report, and each report
was missing the thing the gate existed to report.

## 1. DEF-gates-08 — `scripts/check_source_revision_pointers.py`

The module docstring says "Exit 0 only when every live pointer resolves and matches its
source blob". Two mechanisms contradicted that.

**(a) A movable reference passed.** A `Source revision:` value that is not a 40-character
blob (`main`, `HEAD`, a tag, a prose sentence) was printed as `NON_BLOB_REFERENCE`, counted,
and then left out of `BAD`, which is the only thing the exit code reads. A pointer that
resolves to nothing was therefore a passing pointer.

**(b) Every pointer was compared with `links[0]`.** In a document with two
`Source revision:` / `Source:` pairs, both records were verified against the *first*
`Source:` link. The second pointer was compared with the wrong file: a correct pointer
could be reported `STALE`, and a wrong one could be confirmed by a blob it never named.
The synthetic reproduction in the defect file shows the second pointer's declared blob
being reported against `00-governance/a.md`.

### What changed

- A non-blob value keeps its own counter and now also enters `BAD`.
- Live revision records and live `Source:` lines are paired by document order: the n-th
  record with the n-th line. A record with no line of its own is `UNRESOLVED`
  (`NO_SOURCE_LINK`) instead of inheriting the previous record's file.
- `scan(root)` plus an optional `--root` make the behaviour testable against a fixture
  repository. The default root is unchanged; the CLI with no arguments behaves as before.

### Measured on this tree (base 4326669c)

| run | exit | POINTERS | ACCURATE | STALE | NON_BLOB | BAD |
|---|---|---|---|---|---|---|
| before the fix | 1 | 50 | 16 | 8 | 6 | 8 |
| after the fix | 1 | 50 | 16 | 8 | 6 | 14 |

The exit code does not move, because the eight STALE pointers already fail the scan (that
is why the script is baselined as unwired in `scripts/ci/baselines/gate-wiring.txt`).
What moves is the verdict: six movable references that were reported and then ignored now
count. Six of them, all prose or branch names rather than blobs:

```
docs/en/01-system-architecture/forget-fence-and-completion-contract.md:52
docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md:53
docs/en/03-memory-brain/memory-brain-guide.md:6
docs/zh-CN/01-system-architecture/forget-fence-and-completion-contract.md:52
docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md:53
docs/zh-CN/03-memory-brain/memory-brain-guide.md:6
```

They are reported, not repaired: repairing them means editing documents, which is not this
work item.

### Fixture proof (same bytes, both scripts)

| fixture | before the fix | after the fix |
|---|---|---|
| one pointer, `Source revision: main`, one source line | exit 0, `BAD=0`, `NON_BLOB_REFERENCE=1` | exit 1, `BAD=1` |
| two pointers, both correct, each with its own source line | exit 1, `ACCURATE=1` `STALE=1`, the second pointer blamed on `00-governance/a.md` | exit 0, `ACCURATE=2` `STALE=0` |

The second row is the false red and the false green in one table: the old script both
invented a failure for a correct pointer and, had the wrong blob matched, would have
confirmed a bad one for the wrong reason.

## 2. DEF-gates-07 — `scripts/ci/gate_ratchet.py`

The ratchet's whole value is "the failing set is exactly the baseline". Two normalisation
steps removed information before the comparison happened.

**(a) `--format paths` truncated at the arrow.** `\s+->\s+.*$` was stripped from every
item, so `a.md -> missing docs/en/a.md` and `a.md -> missing docs/zh-CN/a.md` became the
same item `a.md`. Two different failures on one path were one item, and the second could
never be a regression.

**(b) Lines wearing a verdict prefix were dropped whole.** Any line starting with `PASS`,
`FAIL`, `OK`, `Ran `, `FAILED` or `NO TESTS` was skipped as a summary — including
`OK 00-governance/a.md has no counterpart`, which is a real offending item.

### What changed

- An item keeps everything the wrapped gate printed for it, minus the `NNN. ` prefix.
- A line is a summary only if it starts like a verdict *and* names no repository object.
  `OK <path> …` is an item; `OK`, `PASS`, `FAILED (failures=2)`, `Ran 12 tests in 0.031s`
  and `GOV-DOC-001 full scan: … violations.` are still summaries.
- The prefix test now has a word boundary, so `OK_STATUS` is an item rather than a
  summary.
- Because baseline entries are bare paths by design (`gates.yml` and
  `14-ai-development/ci-gates-and-ratchets.en.md` both document the
  `sed -E 's/ -> .*$//'` regeneration), a bare entry covers **one** item beginning with
  `"<path> -> "` — not every item on that path. Two details on one path now need two
  entries; the second is a regression. A path whose items all disappear is still `fixed`.

### Measured on this tree

The shipped baseline still matches exactly, so the required `bilingual` context keeps its
colour:

```
ratchet: baseline=77 current=77 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.    (exit 0)
```

The same command against the pre-fix script also exits 0 with the same four numbers: the
defect is invisible on today's output, which is why it needed a fixture to pin.

### Fixture proof (`scripts/ci/test_gate_ratchet.py`)

| fixture | before the fix | after the fix |
|---|---|---|
| baseline `a.md`; gate prints `a.md -> m1` and `a.md -> m2` | `current=1`, PASS (two failures merged into one item) | `current=2`, exit 1, exactly one regression naming `a.md -> m2` |
| baseline `a.md -> x`; gate prints `a.md -> y` | `current=1` bare `a.md`, one regression and two stale entries | one regression naming the new detail |
| empty baseline; gate prints `OK 00-governance/a.md has no counterpart` | `current=0` → "exited 1 without printing any item" | `current=1` → regression naming the line |
| gate prints only `PASS`, `OK`, `FAILED (failures=2)`, `Ran 12 tests …`, the full-scan count line | no items → crash guard | no items → crash guard (unchanged) |

## 3. Tests

`scripts/ci/test_gate_ratchet.py`: 7 tests before, 14 after. All pass on the fixed script
and the seven new ones are falsifiable: six of them fail against the pre-fix
`gate_ratchet.py` (the seventh pins behaviour that must survive, so it fails only on the
item-fidelity assertion, not on its premise).

`scripts/test_check_source_revision_pointers.py` (new): 5 tests. All pass on the fixed
script; all five fail against the pre-fix script. Because the pre-fix script has neither
`--root` nor `scan()`, the falsification was also run end to end: the pre-fix script, moved
into a fixture repository as `<root>/scripts/check_source_revision_pointers.py`, prints the
two rows in the fixture table above on the same bytes the fixed script then passes.

The new test file is reachable: it is added to the existing
"Run unreachable self-checks from the repository root" list in
`.github/workflows/repository-hygiene.yml`, and
`scripts/ci/check_test_reachability.py` reports `66 test files, 66 reachable`.

## 4. What this record does not claim

- No required context changed colour. `bilingual` is still the same ratchet over the same
  77 entries.
- `scripts/check_source_revision_pointers.py` was not wired into a workflow, and its
  baseline entry in `gate-wiring.txt` was not removed.
- Neither bilingual baseline was edited, lowered or regenerated.
- The eight STALE pointers and the six movable references the script reports were left as
  they are. Making the gate red is the repair; making the repository clean is a different
  work item.
- The `--format schema` branch of `gate_ratchet.py` is still uncalled. Its own ponytail note
  asks for it to be deleted when the file is next touched; that deletion changes the
  command line `gates.yml` passes and reads better as its own change.
- The comment in `scripts/ci/baselines/gate-wiring.txt` still says the script fails on main
  because of "8 STALE pointers". It now fails with 14 failing records. The baseline was not
  edited, so the comment understates the run; this paragraph is the correction of record.
