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
      last_verification_note: "This record states the state round 5 actually examined: origin/main ce6b65b7, clean working tree, manifest 34354 bytes / 281 lines, md5 b9801feda32dbb7175fe13d87a541faa, unchanged across a 3 s re-check. Round 4 returned REQUEST-CHANGES on two blocking items; both are verified fixed below, and the fixes introduced no new false claim."
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

# REVIEW-05-060 — independent review of AID-2026-060 manifest (round 5)

## Provenance

- Reviewer: this session (agent `r7c`), **not** the author of the file.
- File under review: `14-ai-development/work-items/AID-2026-060/manifest.yaml`
  (repo `C:\Users\Administrator\AppData\Local\Temp\opencode\amb2`).
- Reviewed state: `origin/main` = `ce6b65b7`, **committed**, working tree clean
  (`git status --porcelain` empty). Unlike round 4, the bytes did not move under
  review: 34354 bytes / 281 lines, md5 `b9801feda32dbb7175fe13d87a541faa`,
  identical on a 3 s re-check. Round 4's N4 (freeze the bytes) is satisfied.
- Independence: **session-level only**. Same GitHub identity as the author, so this
  is not structurally independent review. Disclosed under `PR-GOVERNANCE-001` §5 as
  amended by `2eb4e352` (#935).
- Scope: whether round 4's two blocking items (B1, B2) and its one non-blocking
  citation note (N1) are actually fixed in the current bytes, and whether the fixes
  broke anything. Nothing else is re-litigated; rounds 1–4 are taken as read.
- The reviewer wrote nothing to the repository except this report.

---

## Check 1 — B1: AC1's coverage claim

**What round 4 blocked.** AC1 said "Tested with both an empty and a non-empty
baseline", which the suite does not do.

**What the file says now** (`manifest.yaml:121`, AC1, final clause):

> "Coverage caveat, measured: the suite's only status-outside-{0,1} case is
> test_exit_status_outside_zero_one_is_not_comparable, which uses the non-empty
> baseline 'a.md'; the two empty-baseline tests use exit 1 and exit 0. The guard is
> not baseline-dependent, so the case is pinned, but the pair 'empty baseline plus
> status 2' is not itself exercised by any test, and this criterion does not claim
> otherwise."

The present-tense "Tested with both an empty and a non-empty baseline" is gone.
`grep -n "Tested with both"` over the file → one hit, and it is inside the
round-4 changelog comment at L178 quoting the retired sentence, not an assertion.

**Is the caveat true?** Yes, on every clause:

```
$ grep -n "sys.exit(2)\|sys.exit(9)\|no entries\|def test_" scripts/ci/test_gate_ratchet.py
50:    def test_empty_baseline_with_nonzero_exit_and_no_output_fails(self):
51:        proc = run_gate("# no entries\n", python("import sys", "sys.exit(1)"))
56:    def test_empty_baseline_with_clean_exit_and_no_output_passes(self):
57:        proc = run_gate("# no entries\n", python("import sys", "sys.exit(0)"))
61:    def test_reported_failure_outside_the_baseline_is_a_regression(self):
69:    def test_exact_match_with_nonzero_exit_still_passes(self):
77:    def test_baseline_item_that_no_longer_fails_is_stale(self):
82:    def test_exit_status_outside_zero_one_is_not_comparable(self):
85:            python("print('a.md')", "import sys", "sys.exit(2)"),
```

- only status-outside-{0,1} case is #6, baseline `"a.md\n"` → **TRUE**
- two empty-baseline tests use exit 1 and exit 0 → **TRUE** (L51, L57)
- no test exercises "empty baseline + status 2" → **TRUE** (one `sys.exit(2)` hit, L85)
- "the guard is not baseline-dependent" → **TRUE**: `gate_ratchet.py:117` returns
  before any baseline/current comparison is consumed; it reads `proc.returncode`
  alone.

**AC1's measurement claim also re-checked.** AC1 says an empty baseline plus a
command exiting 9 gives `regressions=0 fixed=0` then FAIL exit 1. Measured with the
real script:

```
$ py scripts/ci/gate_ratchet.py --baseline <tmp "# none"> --format paths \
    --command "python3 -c \"import sys; sys.exit(9)\""
ratchet: baseline=0 current=0 regressions=0 fixed=0
ratchet: FAIL - the wrapped command exited 9; only 0 (clean) and 1 (red) carry a comparable failure set.
EXIT: 1
```

**MATCHES.** B1 is **CLOSED**: the false claim is replaced by a true, measured
caveat, and no test was quietly added to make the old sentence true.

## Check 2 — B2: the "~20 shrink-only baselines" figure

**What round 4 blocked.** `risk_rationale` said the ratchet "keeps ~20 shrink-only
baselines honest". One baseline exists; two have ever existed.

**What the file says now** (`manifest.yaml:6`):

> "… the risk is not damage but false assurance: **the ratchet is the mechanism
> that keeps a shrink-only baseline honest**, and at b80e5a40 it reported PASS over
> an empty baseline even when the command it ran exited non-zero. Measured at
> 767f2eaa, exactly one baseline exists in the tree
> (scripts/ci/baselines/bilingual-docs.txt) and exactly two have ever existed (the
> other, document-management.txt, was retired); gates.yml:41-42 says so in prose."

The figure is gone. `grep -n "~20"` over the file → one hit, L182, inside the
round-4 changelog comment quoting the retired sentence. No live claim.

**Is the replacement true?** Yes, on every count:

```
$ ls -1 scripts/ci/baselines/
bilingual-docs.txt

$ git log --all --diff-filter=A --name-only --pretty=format: -- "scripts/ci/baselines/*" | sort -u
scripts/ci/baselines/bilingual-docs.txt
scripts/ci/baselines/document-management.txt
```

- exactly one baseline in the tree → **TRUE**
- exactly two have ever existed, across all refs → **TRUE**
- `document-management.txt` was retired → **TRUE** (added, not present now)

**The cited prose supports it** (`.github/workflows/gates.yml:39-43`):

```
39 | # Baselines live in `scripts/ci/baselines/`. Each file is the exact set of
40 | # currently-failing items, one per line; `#` starts a comment. After the
41 | # `schema-nonempty` ratchet was retired there is exactly one baseline left,
42 | # `bilingual-docs.txt`. A baseline directory with a file per green gate would be
43 | # a directory of exemptions.
```

`gates.yml:41-42` does say "there is exactly one baseline left". The citation
resolves and the paraphrase is faithful. **MATCHES.**

One thing checked and not a defect: the replacement sentence is now longer and
carries a measurement, which is the correct repair direction — it makes the R2
argument rest on a fact a reader can re-run (`ls`, `git log`) rather than on a
recollection. **B2 is CLOSED.**

## Check 3 — N1: F5's citation at `measured_at: ba293506`

**What round 4 noted.** F5 was attributed to `ba293506` but cited
`gates.yml:165-168`, a range that is correct at `767f2eaa` and wrong at
`ba293506`.

**What the file says now** (`manifest.yaml:262`, F5):

> "… the only caller in the repository is **the step named 'Ratchet the GOV-DOC-001
> full scan'** in gates.yml (lines 161-164 at ba293506, the commit this finding is
> measured at; 165-168 at 767f2eaa) …"

Both halves of the round-4 ask are met: the step is **named**, and each line range
is pinned to its own commit.

**Are both ranges correct for the commit they are attached to?**

At `ba293506` (`git show ba293506:.github/workflows/gates.yml`):
```
157 |       - name: Ratchet the GOV-DOC-001 full scan
158 |         shell: bash
159 |         run: |
160 |           set -euo pipefail
161 |           python3 scripts/ci/gate_ratchet.py \
162 |             --baseline scripts/ci/baselines/bilingual-docs.txt \
163 |             --format paths \
164 |             --command "python3 scripts/check_bilingual_docs_full.py"
```
→ `161-164` is the invocation. **CORRECT.**

At `767f2eaa` (and at the reviewed `ce6b65b7`, identical in this region):
```
161 |       - name: Ratchet the GOV-DOC-001 full scan
162 |         shell: bash
163 |         run: |
164 |           set -euo pipefail
165 |           python3 scripts/ci/gate_ratchet.py \
166 |             --baseline scripts/ci/baselines/bilingual-docs.txt \
167 |             --format paths \
168 |             --command "python3 scripts/check_bilingual_docs_full.py"
```
→ `165-168` is the invocation. **CORRECT.** The four-line shift is the
`Self-check the ratchet wrapper` step (157-158 at 767f2eaa) that #1031 added.

`grep -n "gates.yml:[0-9]"` over the whole file now returns only `41-42` (L6, L184,
the baseline count) and the round-4 changelog line L186 — **no live
`gates.yml:165-168` remains**. **N1 is CLOSED.**

*Non-blocking nuance, recorded not raised:* both ranges point at the four-line
invocation body, while the step's `- name:` line is 157 at ba293506 and 161 at
767f2eaa. A reader following the range lands inside the correct step, and the step
is named in the same sentence, so nothing is ambiguous. If the range is ever
re-cut, `157-164` / `161-168` would bound the step including its name.

## Check 4 — Regression: did the fixes break anything?

### 4a. AC3 still unimplemented, and still true

The file still says so twice — `manifest.yaml:125` ("This is the one criterion of
AC1-AC5 that #1031 did NOT implement, and it is the whole of the remaining work")
and `manifest.yaml:206-208` ("AC3 … is unimplemented, has no test, and is the whole
of the remaining work"). Measured with the real script:

```
$ printf 'a.md\nb.md\nc.md\n' > /tmp/three.txt
$ py scripts/ci/gate_ratchet.py --baseline /tmp/three.txt --format paths \
    --command "python3 -c \"print('a.md'); print('b.md'); print('c.md')\""
ratchet: baseline=3 current=3 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
EXIT: 0
```

**CONFIRMED** — a zero status over a non-empty set still PASSes. AC3 is genuinely
open, and the manifest's description of the defect ("a checker that always exits 0
and always prints the same items ratchets itself into permanence") reproduces
exactly.

### 4b. AC4 still holds — empty baseline, clean exit

```
$ printf '# none\n' > /tmp/empty.txt
$ py scripts/ci/gate_ratchet.py --baseline /tmp/empty.txt --format paths \
    --command "python3 -c \"import sys; sys.exit(0)\""
ratchet: baseline=0 current=0 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
EXIT: 0
```

**PASS exit 0**, as AC4 requires. (First attempt at this case printed `a.md` while
exiting 0, which correctly FAILed as a regression — that is AC3's defect firing, not
a contradiction of AC4; re-run with no output, above.)

### 4c. YAML still parses to the same shape

```
$ py -c "import yaml,io; d=yaml.safe_load(io.open('.../manifest.yaml',encoding='utf-8')); print(len(d), d['status'], [a['id'] for a in d['acceptance_criteria']])"
38 DISPATCHED ['AC1', 'AC2', 'AC3', 'AC4', 'AC5', 'AC6', 'AC7', 'AC8']
```

38 top-level keys, `status: DISPATCHED`, AC1–AC8 intact. Nothing was dropped while
the two sentences were rewritten.

### 4d. Other checks touched by the edits

- `scripts/ci/baselines/bilingual-docs.txt` still 77 entries (`wc -l` → 77;
  `grep -vc '^\s*#\|^\s*$'` → 77), matching AC5/AC8/F5.
- `gate_ratchet.py:117-120` and `:122-125` unchanged: the two guards are where
  every citation says they are.
- `scripts/ci/` and `.github/` have no working-tree modifications — the fixes are
  manifest-only, consistent with `authorization.implementation_write: NOT_GRANTED`.
- AC7's docstring claim still true: `gate_ratchet.py:19-20` reads "a wrapped command
  that exited non-zero without reporting an item" and says nothing about a status
  outside {0,1}, so that deliverable is still correctly recorded as open.

---

## Closure table

| # | Round-4 item | Verdict | Evidence |
|---|---|---|---|
| B1 | AC1 claimed "Tested with both an empty and a non-empty baseline" | **CLOSED** | L121 now states the coverage caveat; `sys.exit(2)` appears once (L85, baseline `a.md`); the two empty-baseline tests use exit 1/0 (L51, L57); no "Tested with both" survives outside the L178 changelog quote |
| B2 | `risk_rationale` claimed "~20 shrink-only baselines" | **CLOSED** | L6 now says "a shrink-only baseline" and adds the measured counts; `ls scripts/ci/baselines/` → 1 file; all-refs history → 2 files; `gates.yml:41-42` supports it; no live "~20" |
| N1 | F5 `measured_at: ba293506` but cited `gates.yml:165-168` | **CLOSED** | L262 names the step and pins `161-164` to ba293506 (verified: invocation is 161-164 there) and `165-168` to 767f2eaa (verified); no live `gates.yml:165-168` remains |
| R1 | AC3 unimplemented — still true? | **TRUE, unchanged** | L125, L206-208; real script: 3-entry baseline + 3 items + exit 0 → PASS exit 0 |
| R2 | AC4 empty baseline + clean exit → PASS | **TRUE** | real script: PASS exit 0 |
| R3 | YAML shape preserved | **TRUE** | 38 keys, DISPATCHED, AC1–AC8 |
| R4 | Fixes touched only the manifest | **TRUE** | `git status --porcelain` clean; `scripts/ci/`, `.github/` unmodified; `bilingual-docs.txt` still 77 entries |

## Blocking items

**None.**

Both round-4 blocking items are repaired in the bytes now on `origin/main`, the
repair replaced a false claim with a measured one in each case rather than adding
code to make the old sentence true, and no new false claim was introduced by either
edit. Round 4's citation note is also closed, and the two `gates.yml` ranges it now
carries each resolve at the commit they are attached to.

## Non-blocking notes

- **N1 (new, cosmetic)** F5's `161-164` / `165-168` bound the invocation body, not
  the step. The step's `- name:` line is 157 at ba293506 and 161 at 767f2eaa, so
  `157-164` / `161-168` would bound the step including its name. The step is named
  in the same sentence, so nothing is ambiguous today; worth re-cutting only if the
  range is next touched for another reason.
- **N2 (carried, still open by design)** 5 deliverables / 8 criteria; AC8 is named
  by no deliverable. No one-to-one coverage is claimed, and AC8 is a no-change
  constraint pinned by test #4, so nothing is misstated. Recorded, not raised.
- **N3 (process, satisfied)** Round 4's N4 asked for frozen bytes. Satisfied: the
  file is committed at `ce6b65b7`, the tree is clean, and the md5 was stable across
  the whole review. This round read one state, not three.
- **N4 (carried)** `review.status: CHANGES_APPLIED_AWAITING_RE_REVIEW` with
  `rounds_completed: 4` is still accurate as written: it describes the bytes before
  this report, and no reviewer had read them when it was set. Applying this
  report's verdict is what would move it, and that is the author's edit, not mine.

---

`VERDICT: APPROVE`

Both blocking items from round 4 are closed with measurements that reproduce, the
non-blocking citation note is closed and both of its replacement ranges are correct
at their own commits, and the two edits changed nothing else: AC3 is still
unimplemented and still described as the whole of the remaining work, AC4 still
passes over an empty baseline, and the document still parses to 38 keys with
AC1–AC8 and `status: DISPATCHED`.

This verdict is on the record only. No implementation exists: `implementation.status`
is `NOT_STARTED`, `remaining_scope` is "AC3 only", and nothing in this review
suggests the manifest's claim that four of five behavioural criteria already hold is
wrong — it is exactly what the script does today.
