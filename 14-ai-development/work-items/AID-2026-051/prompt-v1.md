---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "The 8-test baseline and the 77/21 counts were measured at main 063113f0 in this session: pytest reports 8 passed over the two files named, and check_bilingual_docs.py prints 'bilingual baseline: 77 frozen, 0 new gaps' with 'exemptions: 21'. The absence of T01-T09 was checked by listing every test function name in the three bilingual test files."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# TASK — write the nine gate tests GOV-NC-2026-11-22-ENUM-BOUNDARY-021 requires before it can close

`main` is at `063113f0`.

The gate is already fixed. The tests that would prove it are not written, and the register cannot
close without them. Your job is the tests, not the fix.

---

## 1. Hard constraints

**#0 — Do not change `scripts/check_bilingual_docs.py` behaviour.** It is already correct, and a
test that requires a behaviour change to pass is a finding to report, not a change to make. If you
believe the implementation is wrong, write the test that fails and say so; do not edit the gate.

**#1 — Do not touch the frozen baseline.** `scripts/bilingual-baseline.txt` must stay at exactly
77 entries, and `exemptions` at exactly 21. A test that writes the baseline must restore it
byte-for-byte, and must assert both counts before and after.

**#2 — Every test must leave the worktree clean.** These tests create, stage and delete files in
governed directories. A leaked `_probe*.md` makes the next run fail for the wrong reason. Use
`try/finally` or a fixture with teardown, and make the teardown run even on assertion failure.

**#3 — Tests that need a detached worktree must skip, not fail, when it cannot be created.** CI has
it; a contributor's dirty checkout may not. `pytest.skip` with the reason is correct;
`assert False` is not.

**#4 — No `#[ignore]`, `todo!()`, `unimplemented!()`.** Rust is not involved here, but the
repository-wide rule stands in spirit: no skipped-by-default tests that look like coverage.

**#5 — Report only commands you actually ran, with real output and real exit codes.** `NOT RUN`
is a valid answer. Fabricated green output is the one thing that makes this whole file worthless.

---

## 2. What already exists, so you do not rebuild it

Three test files, 8 tests, all passing at `063113f0`:

| file | tests |
|---|---|
| `tests/test_check_bilingual_docs_full.py` | 5 — root architecture pairs, missing mirror, side-by-side, operational subtrees, markdown-only scope |
| `scripts/test_check_bilingual_docs.py` | 3 — same-head not-applicable, invalid base fails closed, code-only change is not empty |
| `scripts/governance/bilingual/test_bilingual_scripts.py` | 13 — tiering, sync, pairing, drift |

```
$ python -m pytest tests/test_check_bilingual_docs_full.py scripts/test_check_bilingual_docs.py -q
8 passed, 3 warnings in 1.56s
```

None of these cover the enumeration boundary or the baseline write protection. That is the gap.

---

## 3. The nine tests

Specifications are in `14-ai-development/governance-register/GOV-NC-2026-11-22-ENUM-BOUNDARY-021.md`
§6 (T01–T09) and the reproduction script in §7. Read both before writing anything. The summaries
below are navigational, not a substitute.

| id | what it pins | the assertion that matters |
|---|---|---|
| T01 | untracked `.md` in a normative root | absent from `current_bilingual_gaps()`; after `git add`, present |
| T02 | `.pytest_cache/README.md` in two governed paths | neither appears in the gap set |
| T03 | a `.md` matching `.gitignore` | absent from the gap set |
| T04 | tracked `.md` with no mirror | **present**, and the gate exits 2 |
| T05 | `--write-baseline` on a dirty tree | non-zero exit, explicit refusal, baseline bytes **and** SHA-256 unchanged, no temp file left |
| T06 | `--write-baseline` on a clean detached worktree | succeeds; written content equals the tracked gap set |
| T07 | gate run from a cwd outside the repository | `REPO_ROOT` still resolves; git commands succeed |
| T08 | baseline invariance on clean main | `77 frozen`, `exemptions: 21`, `PASS`, `EXIT=0` — exact strings |
| T09 | changed-path semantics | changed-path set unchanged; side-by-side catch-up unchanged; `COMPLETE` manifest unchanged; shallow-history check still runs **before** baseline/path checks |

### 3.1 T04 is the regression lock, and it is the one to get right

T01–T03 all assert *absence*. Three passing absence tests are consistent with a gate that has been
neutered into never reporting anything. T04 is the only test that asserts the gate still **fails**
when it should.

If T04 passes but T01–T03 also pass, the fix is correct. If T01–T03 pass and T04 does not, someone
has bought cleanliness at the price of the gate, and that is worse than the original defect. Write
T04 first and watch it fail for the right reason before you write the others.

### 3.2 T05 must compare bytes, not just exit codes

A write-baseline that returns 2 *after* truncating the file satisfies "returns non-zero" and
destroys governance state. Read the file into memory before, compare `read_bytes()` after, and
compare the SHA-256 too — the register asks for both because the byte comparison alone will not
notice a mode change or a newline rewrite on some platforms.

---

## 4. Acceptance criteria

1. All nine tests exist, named for their T-id so the register can be checked against the suite
   mechanically — `test_t01_...` through `test_t09_...`.
2. `python -m pytest` over the three test files: **all pass**, count stated.
3. Running the full suite twice in a row passes both times. A test that passes once and leaves
   state behind is not a test.
4. `git status --porcelain` is empty after the suite.
5. Baseline still 77 entries, exemptions still 21, verified by the gate's own output.
6. No behavioural change to `scripts/check_bilingual_docs.py`, shown by `git diff` on that file
   being empty.
7. Any test you skip is skipped for an environmental reason and says so in its `pytest.skip` reason.

---

## 5. What this does not close

Writing the tests satisfies closing condition 5 of the register. Conditions 16 asks for
**independent** acceptance evidence, and a session that wrote the tests cannot supply it for its own
work. That condition stays open after you are done, and the register stays `OPEN` until someone
else signs it. Do not mark it closed.

---

## 6. Provenance

Dispatched by the owner-proxy session that re-measured the register at `063113f0`, found both
defects already fixed, and found the required tests absent. The measurement is in the delivery PR,
not in this prompt.
