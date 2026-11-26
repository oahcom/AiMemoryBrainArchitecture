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
      last_verification_note: "This record states the state round 4 actually examined: 767f2eaa plus the author's working-tree rewrite, snapshot md5 fbafaf89da84eb8cf8adbabf1ec558be at 32278 bytes. Round 4 returned REQUEST-CHANGES on two present-tense claims. Both are corrected in the bytes that follow this report, which no reviewer has read."
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

# REVIEW-04-060 — independent review of AID-2026-060 manifest (round 4)

## Provenance

- Reviewer: this session (agent `r6c`), **not** the author of the file.
- File under review: `14-ai-development/work-items/AID-2026-060/manifest.yaml`
  (repo `C:\Users\Administrator\AppData\Local\Temp\opencode\amb2`, branch `req05/round5-followup`).
- Reviewed state: commit `767f2eaa` **plus the author's uncommitted working-tree rewrite**
  (`git status` shows `M 14-ai-development/work-items/AID-2026-060/manifest.yaml`).
- **The file was edited twice while this review ran.** Successive measurements:
  30796 B / 247 L → 31596 B / 259 L (md5 `aaed7865`) → **32278 B / 264 L (md5
  `fbafaf89da84eb8cf8adbabf1ec558be`)**, stable on a 4 s re-check. Everything below is
  measured against the final 264-line state, snapshotted to
  `scratch-untracked/snap-060b.yaml`; line numbers are that snapshot's. Checks 1, 4, 5 and
  the closure table were re-run against it. Check 3's five behavioural runs and check 2's
  mutation runs were executed against `gate_ratchet.py` / `test_gate_ratchet.py`, which are
  untouched by all three revisions (`git status --porcelain` on both is empty), so those
  results stand unchanged.
- Independence: **session-level only**. Same GitHub identity as the author, so this is not
  structurally independent review. Disclosed under `PR-GOVERNANCE-001` §5 as amended by
  `2eb4e352` (#935).
- Scope: the increment applied **after** round 3's REQUEST-CHANGES
  (`REVIEW-03-INDEPENDENT.md`, same directory). Round 3 is not re-done here; only
  "is the rewrite now factually true, and did it leave anything false" is asked.
- The reviewer wrote nothing to the repository. Only this report file was written.

---

## Check 1 — Parse with a duplicate-key-detecting loader

Loader: `yaml.SafeLoader` subclass overriding `construct_mapping` to raise
`ConstructorError` on a repeated key at the same node. Sanity-checked first against a
deliberate duplicate (`a: 1` / `a: 2` → `found duplicate key 'a'`, exit 1), so the clean
result below is not a silently-ignoring loader. Script `scratch-untracked/p060b.py`, raw
output `scratch-untracked/out060b.txt`.

```
bytes: 32278
top_level_keys: 38
keys: [work_item_id, title, class, risk, risk_rationale, security_scope, authorization,
scope, prompt_supersession, status, sponsor, accountable_owner, implementing_ai_session,
repository, base_branch, base_commit_sha, tracking_issue, created_at, updated_at,
prompt_id, prompt_version, prompt_file, prompt_status, prompt_sha256, prompt_bytes,
prompt_provenance_tier, prompt_provenance_note, owner_decisions, deliverables,
acceptance_criteria, withdrawn_acceptance_criteria, independent_reviewer,
integration_reviewer, review, acceptance, implementation, errata, findings]
acceptance_criteria: 8 ['AC1','AC2','AC3','AC4','AC5','AC6','AC7','AC8']
withdrawn: 1 ['AC1-ORIGINAL']
findings: 8 ['F1','F2','F3','F4','F5','F6','F7','F8']
owner_decisions: 1 ['OD-26']
overlap_ac_wac: []
deliverables_count: 5
```

No duplicate key at any node. No id appears in both the live and withdrawn lists.
**PASS.**

## Check 2 — Every line-number and commit claim

`git rev-parse 767f2eaa` → `767f2eaac0443bc4c092fd81c114d924946102e6`;
`b80e5a40` → `b80e5a4059e7503136697d89935ce8dddc6c87f9`;
`git merge-base --is-ancestor c6602739 767f2eaa` → exit 0, so `c6602739` is an ancestor of
the reviewed commit. `git log -1 c6602739` →
`fix(governance): remove two unreachable duplicate guards and close gate_ratchet's
empty-baseline fail-open (#799) (#1031)`.

### 2a. `gate_ratchet.py:117` rejects a status outside {0,1}; `:122` rejects non-zero with no items

Real file, `scripts/ci/gate_ratchet.py` at 767f2eaa:

```
117|    if proc.returncode not in (0, 1):
118|        print(f"ratchet: FAIL - the wrapped command exited {proc.returncode}; "
119|              "only 0 (clean) and 1 (red) carry a comparable failure set.")
120|        return 1

122|    if proc.returncode != 0 and not current:
123|        print(f"ratchet: FAIL - the wrapped command exited {proc.returncode} "
124|              "without printing any item; a crash is not a clean run.")
125|        return 1
```

Manifest sentences checked against this:

- L113 (`deliverables[0]`): "At 767f2eaa the first two shapes are implemented
  (gate_ratchet.py:117 and :122, added by c6602739 / #1031); the third is not, and is the
  whole of the remaining work." → **TRUE**.
- L121 (AC1): "Satisfied at 767f2eaa by c6602739 (#1031), which added the guard at
  gate_ratchet.py:117" → **TRUE**.
- L123 (AC2): "added the guard at gate_ratchet.py:122 … a command exiting 9 with no output
  is caught earlier by gate_ratchet.py:117 as a status outside {0, 1}" → **TRUE** (case 3a
  shows the `:117` message; `:122` is never reached for status 9).
- L125 (AC3): "gate_ratchet.py:117 rejects a status outside {0,1} and :122 rejects a non-zero
  status with no items, but nothing compares a zero status against a non-empty set" →
  **TRUE** (nothing in 81-140 reads `returncode` outside those two conditions).

The `117-120` / `122-125` block boundaries used by the mutation instructions in AC1 and AC6
are exactly right.

### 2b. `scripts/ci/test_gate_ratchet.py` — exists, six cases

`ls -la` → present, 3220 bytes. `grep -c "def test_"` → **6**. Names, in file order:

1. `test_empty_baseline_with_nonzero_exit_and_no_output_fails` (L50)
2. `test_empty_baseline_with_clean_exit_and_no_output_passes` (L56)
3. `test_reported_failure_outside_the_baseline_is_a_regression` (L61)
4. `test_exact_match_with_nonzero_exit_still_passes` (L69)
5. `test_baseline_item_that_no_longer_fails_is_stale` (L77)
6. `test_exit_status_outside_zero_one_is_not_comparable` (L82)

`git log --follow` → the file was added by `c6602739`, matching "added by c6602739 (#1031)
with six cases".

Test-by-test against AC1–AC5 and against the mutation results the manifest asserts (harness
`scratch-untracked/mut060.py`, raw output `scratch-untracked/mut060.txt`):

| Manifest claim (L131, AC6) | Test that pins it | Measured |
|---|---|---|
| removing `:117-120` fails `test_exit_status_outside_zero_one_is_not_comparable` | #6 | **TRUE** — M1: exit 1, that one test FAILED |
| removing `:122-125` fails `test_empty_baseline_with_nonzero_exit_and_no_output_fails` | #1 | **TRUE** — M2: exit 1, that one test FAILED |
| rejecting empty baselines outright fails `test_empty_baseline_with_clean_exit_and_no_output_passes` and the preceding test | #2 and #1 | **TRUE** — M3: both FAILED |
| turning `:117` into "any non-zero status fails" fails `test_exact_match_with_nonzero_exit_still_passes` among others | #4 (+#1,#3) | **TRUE** — M4: 3 FAILED, incl. `test_exact_match_with_nonzero_exit_still_passes` |
| "AC1, AC2, AC4 and AC5 are pinned by named tests; AC3 has no test" | — | AC2←#1, AC4←#2, AC5←#4, AC3←none: **TRUE** for AC2/AC3/AC4/AC5 |
| AC1 pinned by a named test | #6 | pinned, but not as described — see 2b-note |

The mutation harness copies `gate_ratchet.py` and `test_gate_ratchet.py` into a temp `ci/`
directory, applies one textual mutation, and runs the real suite with the same interpreter.
Nothing in the repository was edited.

**2b-note — one clause of AC1 is false.** AC1 (L121) says the guard is
"Tested with both an empty and a non-empty baseline." There is no test that runs a status
outside {0,1} against an empty baseline. The only test of that guard is #6, whose baseline
is `"a.md\n"` — one entry:

```
82|    def test_exit_status_outside_zero_one_is_not_comparable(self):
83|        proc = run_gate(
84|            "a.md\n",
85|            python("print('a.md')", "import sys", "sys.exit(2)"),
86|        )
```

`grep -n "sys.exit(2)\|sys.exit(9)"` over the test file returns exactly one hit (L85);
`grep -n 'no entries'` returns L51 and L57, which use exit 1 and exit 0. The empty-baseline
half of that sentence is untested. The *measurement* in the same sentence ("empty baseline
plus a command exiting 9 gives … FAIL exit 1") is true — reproduced in 3a — but a manual
measurement is not a test, and the sentence says "Tested".

### 2c. `gates.yml:165-168` is the ratchet invocation of `check_bilingual_docs_full.py`

```
161|      - name: Ratchet the GOV-DOC-001 full scan
162|        shell: bash
163|        run: |
164|          set -euo pipefail
165|          python3 scripts/ci/gate_ratchet.py \
166|            --baseline scripts/ci/baselines/bilingual-docs.txt \
167|            --format paths \
168|            --command "python3 scripts/check_bilingual_docs_full.py"
```

**TRUE** at 767f2eaa. The job name is `Bilingual docs coverage (ratchet)` (L150), so AC5's
"the required check Bilingual docs coverage (ratchet)" resolves.

The rewrite moved this citation from `161-164` to `165-168` in all three places (L47, L129,
L241); the `161-164` form was correct at `ba293506`, where the same block sits four lines
higher because the `Self-check the ratchet wrapper` step that #1031 added occupies 157-158.
`grep -c "161-164"` over the snapshot → 0, so the correction is complete.

**Residual, non-blocking:** F5 (L241) is `measured_at: "ba293506"` yet cites
`gates.yml:165-168`. At `ba293506` the block is at 161-164
(`git show ba293506:.github/workflows/gates.yml | grep -n` → 161 `gate_ratchet.py`, 164
`--command`). The line number does not resolve at the commit the measurement is attributed
to; the block it names is the right block. Historical citation drift, not a false
conclusion — the conclusion (77 violations, exit 1, ratchet PASS) reproduces.

## Check 3 — The four behavioural claims, with the real script

Flags from argparse: `--baseline` (required, Path), `--command` (required, str), `--format`
(`schema|paths`, default `schema`). Harness `scratch-untracked/cases060.py`, raw output
`scratch-untracked/cases060.txt`. Each case uses a fresh temp baseline and the real
`scripts/ci/gate_ratchet.py`.

**(a) empty baseline, command exits 9, no output** — L123/L121 claim FAIL exit 1 naming the
status:
```
ratchet: baseline=0 current=0 regressions=0 fixed=0
ratchet: FAIL - the wrapped command exited 9; only 0 (clean) and 1 (red) carry a comparable failure set.
EXIT: 1
```
**MATCHES.**

**(b) empty baseline, command exits 9 after printing one item** — L123 claims caught at
`:117`, not `:122`:
```
ratchet: baseline=0 current=1 regressions=1 fixed=0
ratchet: FAIL - the wrapped command exited 9; only 0 (clean) and 1 (red) carry a comparable failure set.
EXIT: 1
```
**MATCHES** — the `:117` message, i.e. `:122` is never reached for status 9.

**(c) empty baseline, exit 0, no output** — AC4 (L127) claims PASS exit 0:
```
ratchet: baseline=0 current=0 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
EXIT: 0
```
**MATCHES.**

**(d) baseline of three items, command prints the same three, exits 0** — AC3 (L125) claims
this **passes** and that this is the remaining defect:
```
ratchet: baseline=3 current=3 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
EXIT: 0
```
**MATCHES** — the defect is real and exactly as described.

**(e) `bilingual-docs.txt` (77 entries), command prints those entries, exits 1** — AC5
(L129) and AC8 (L135) claim PASS exit 0:
```
baseline entries: 77
ratchet: baseline=77 current=77 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
EXIT: 0
```
**MATCHES.** Independently, the real checker agrees with "77 violations, exits 1":
`python3 scripts/check_bilingual_docs_full.py` → 77 numbered items + `GOV-DOC-001 full
scan: FAIL`, `EXIT=1`.

No behavioural case contradicts the manifest. **PASS** on check 3.

## Check 4 — Sentences still false at 767f2eaa

`grep -n "never read\|does not exist\|no test\|today\|currently\|is not implemented\|fails today"`
on the final snapshot — nine hits, each judged on its tense marker:

| L | Sentence fragment | True at 767f2eaa? |
|---|---|---|
| 6 | "it reported PASS over an empty baseline … at b80e5a40" | anchored to b80e5a40 — fine |
| 6 | "Two of the three shapes are now closed by c6602739 (#1031); the third … is open at 767f2eaa" | **TRUE** |
| 6 | **"the ratchet is the mechanism that keeps ~20 shrink-only baselines honest"** | **FALSE** — see 4a |
| 58 | "It **was** not already true at b80e5a40 … proc.returncode **was** never read … c6602739 (#1031) has since added that guard, so at 767f2eaa the case fails correctly" | past tense throughout, present corrected — **fine** (this revision fixed the earlier "is never read") |
| 117 | "The file exists at 767f2eaa with six cases added by c6602739; AC3 has no test, because the guard it would test does not exist yet" | **TRUE** |
| 131 | same, restated | **TRUE** except the AC1 coverage clause — see 2b-note |
| 190 | comment: "has no test, and is the whole of the remaining work" (AC3) | **TRUE** |
| 214 | "At b80e5a40, proc.returncode was never read, in any format; c6602739 (#1031) has since added the two guards" | **TRUE** — `grep -n returncode` over the b80e5a40 revision returns no hits; running it over an empty baseline + exit 9 gives `PASS … EXIT: 0` |
| 221 | "As measured at b80e5a40, proc.returncode was never read … Corrected at REVIEW-03 … so the present-tense form of the first sentence is false at 767f2eaa" | **TRUE**, and explicitly re-anchored |
| 258 | "this sentence used to attribute the status-9 pin to AC5" | past tense — fine |

The rewrite is consistent: every surviving "never read" is either anchored to `b80e5a40` or
explicitly labelled historical, and the last revision converted the two remaining present-tense
ones (L58) to past. **One present-tense quantity claim survives and is false.**

### 4a. Blocking falsehood — "~20 shrink-only baselines"

`manifest.yaml:6` (untouched by any of the three revisions: `git diff HEAD` contains no
`shrink-only baselines` hunk) reads:

> "… the ratchet is the mechanism that keeps **~20 shrink-only baselines** honest …"

At 767f2eaa there is exactly one:

```
$ find . -path ./.git -prune -o -name "*.txt" -path "*baseline*" -print
./scripts/bilingual-baseline.txt          # not a ratchet baseline
./scripts/ci/baselines/bilingual-docs.txt
$ git log --all --diff-filter=A --name-only --pretty=format: -- "scripts/ci/baselines/*" | sort -u | wc -l
2
```

and the workflow says so in prose:

```
gates.yml:41|# `schema-nonempty` ratchet was retired there is exactly one baseline left,
gates.yml:42|# `bilingual-docs.txt`.
```

Never 20: two baseline files have ever existed in this repository's history
(`bilingual-docs.txt`, `document-management.txt`), and `document-management.txt` is gone.
The figure is not "roughly twenty" — it is off by a factor of twenty — and it is the sentence
carrying the R2 risk argument. Current tense, contradicted by `gates.yml:41-42` in the same
tree.

## Check 5 — Cross-references, paths, and status honesty

Reference resolution (`grep -o` counts, re-run on the final snapshot):

```
findings[F1] ×5   findings[F4] ×2   findings[F5] ×2      → F1,F4,F5 all defined
AC1 ×31  AC1-ORIGINAL ×3  AC2 ×10  AC3 ×26  AC4 ×19  AC5 ×17  AC6 ×4  AC7 ×9  AC8 ×2
OD-26 ×9                                                 → defined
bare "(F7)" / "F7)"                                      → 0 hits (round-4 note stayed fixed)
```

Every referenced id resolves; no dangling reference.

Paths named: `scripts/ci/gate_ratchet.py` ✓, `scripts/ci/test_gate_ratchet.py` ✓ (present at
767f2eaa — `git cat-file -e` succeeds), `scripts/ci/baselines/bilingual-docs.txt` ✓ (77
entries), `.github/workflows/gates.yml` ✓, `scripts/check_bilingual_docs_full.py` ✓,
`REVIEW-0{1,2,3}-INDEPENDENT.md` ✓ all present.
`scripts/ci/baselines/traceability.txt` does **not** exist at 767f2eaa — it is
AID-2026-058's deliverable, and AC8 (L135) anchors it with "once AID-2026-058 lands", so the
reference is forward-looking by construction, not broken.

`prompt-v1.md`: declared `prompt_sha256:
f9a01079c017cfbd1487ea09f3efe148c564d646b24ca55d5226967bb51ec5e9`, `prompt_bytes: 7797`.
Measured: `sha256sum` gives the same digest, `wc -c` gives 7797. The FROZEN claim holds.

**Scope block, re-checked after the last edit.** `files_to_create: []` with a comment
explaining that `scripts/ci/test_gate_ratchet.py` moved to `files_to_modify` because #1031
created it, and F8 (L261) now says the same. That is coherent with 2b: the file exists, so
asking an implementer to create it would invite an overwrite. **Consistent, and an
improvement.**

**Status honesty.** `review.status: CHANGES_APPLIED_AWAITING_RE_REVIEW`,
`prior_status: CHANGES_REQUESTED`, `rounds_completed: 3`, and:

> "APPROVED is not claimed for the current bytes: no reviewer has read them."

That is exactly right for the state this round found: round 3 returned REQUEST-CHANGES, the
author's corrections were unreviewed, and the file says so without overclaiming. It does not
deny an approval it has (round 2's APPROVE is named and scoped to earlier bytes) and does not
assert one it lacks. `implementation.status: NOT_STARTED` with `remaining_scope: "AC3 only …"`
is consistent with 3d. `acceptance.status: NOT_ASSIGNED` asserts no acceptance decision.
**Honest.**

Non-blocking observation on coverage counting: 5 deliverables against 8 criteria, and AC8 is
not named by any deliverable. AC8 is a no-change constraint pinned by test #4, so nothing is
unowned in practice; the file does not claim one-to-one coverage.

---

## Closure table

| # | Item | Verdict | Evidence |
|---|---|---|---|
| R3-1 | Round 3 blocking item: manifest asserted "`proc.returncode` is never read" as current | **CLOSED** | L6, L58, L113, L121, L123, L214, L221 all anchored to b80e5a40 or explicitly historical; `grep returncode` over the b80e5a40 revision → 0 hits; guards present at 767f2eaa `:117`/`:122` |
| A1 | `:117` rejects status outside {0,1} | **TRUE** | `:117-120` quoted; cases (a),(b) |
| A2 | `:122` rejects non-zero with no items; status 9 caught earlier at `:117` | **TRUE** | `:122-125` quoted; case (a) |
| A3 | test file exists with exactly six cases, added by c6602739 | **TRUE** | 6 `def test_`; `git log --follow` |
| A4 | removing `:117-120` fails `test_exit_status_outside_zero_one_is_not_comparable` | **TRUE** | M1 |
| A5 | removing `:122-125` fails `test_empty_baseline_with_nonzero_exit_and_no_output_fails` | **TRUE** | M2 |
| A6 | rejecting empty baselines fails the clean-exit test + the preceding test | **TRUE** | M3 |
| A7 | `:117` → "any non-zero fails" fails `test_exact_match_with_nonzero_exit_still_passes` | **TRUE** | M4 |
| A8 | AC3 has no test; zero-status-over-non-empty passes today | **TRUE** | case (d) |
| A9 | AC4: empty baseline + exit 0 → PASS 0 | **TRUE** | case (c) |
| A10 | AC5: 77-entry baseline, echo, exit 1 → PASS 0 | **TRUE** | case (e); real checker 77 items / exit 1 |
| A11 | `gates.yml:165-168` is the bilingual ratchet invocation | **TRUE** | quoted block |
| A12 | `161-164` → `165-168` correction complete | **TRUE** | `grep -c "161-164"` → 0 |
| A13 | AC1 "Tested with both an empty and a non-empty baseline" | **FALSE** | only test of that guard (L82-88) uses a 1-entry baseline; `sys.exit(2)` appears once; `no entries` baselines use exit 1/0 |
| A14 | "~20 shrink-only baselines" (L6) | **FALSE** | one baseline; `gates.yml:41-42`; 2 baseline files ever, across all refs |
| A15 | F5 cites `gates.yml:165-168` at `measured_at: ba293506` | **UNVERIFIED at that commit / non-blocking** | at ba293506 the block is 161-164 |
| A16 | AC7: docstring omits the status-outside-{0,1} condition | **TRUE** | docstring L19-20 names only "exited non-zero without reporting an item" |
| A17 | prompt sha256 / bytes | **TRUE** | measured digest and 7797 bytes match |
| A18 | review block claims no approval it lacks | **TRUE** | L176 |
| A19 | scope: `files_to_create: []`, test file moved to `files_to_modify` | **TRUE / coherent** | file exists at 767f2eaa; F8 L261 says the same |

## Blocking items

**B1 — `manifest.yaml:121` (AC1 text), false coverage claim.**
Sentence: "Tested with both an empty and a non-empty baseline."
Contradicted by:
```
$ grep -n "sys.exit(2)\|sys.exit(9)" scripts/ci/test_gate_ratchet.py
85:            python("print('a.md')", "import sys", "sys.exit(2)"),
$ grep -n 'no entries' scripts/ci/test_gate_ratchet.py
51:        proc = run_gate("# no entries\n", python("import sys", "sys.exit(1)"))
57:        proc = run_gate("# no entries\n", python("import sys", "sys.exit(0)"))
```
The empty-baseline cases use exit 1 and exit 0; the only status-outside-{0,1} case uses a
non-empty baseline. Fix the sentence, or add the missing test — but the latter is
implementation, not the record.

**B2 — `manifest.yaml:6` (`risk_rationale`), false quantity, present tense.**
Sentence: "the ratchet is the mechanism that keeps ~20 shrink-only baselines honest".
Contradicted by:
```
$ find . -path ./.git -prune -o -name "*.txt" -path "*baseline*" -print
./scripts/bilingual-baseline.txt
./scripts/ci/baselines/bilingual-docs.txt
$ git log --all --diff-filter=A --name-only --pretty=format: -- "scripts/ci/baselines/*" | sort -u | wc -l
2
gates.yml:41|# `schema-nonempty` ratchet was retired there is exactly one baseline left,
gates.yml:42|# `bilingual-docs.txt`.
```
One baseline exists; two have ever existed. Replace the figure or drop it. This is the
sentence the R2 rating rests on.

## Non-blocking notes

- **N1** F5 (L241) is `measured_at: ba293506` but cites `gates.yml:165-168`; at that commit
  the block is 161-164. The conclusion reproduces; only the citation drifts.
- **N2** (fixed in the final revision) AC7 no longer says the docstring phrase "describes the
  pre-#1031 behaviour"; it now says #1031 added the phrase and that it covers AC2's shape
  only. That is accurate.
- **N3** 5 deliverables / 8 criteria; AC8 is named by no deliverable. No one-to-one coverage
  is claimed, so nothing is misstated.
- **N4** The file changed twice under review (30796 → 31596 → 32278 bytes). Three revisions
  in one round is how a false sentence survives a review; freeze the bytes before the next
  round.

---

`VERDICT: REQUEST-CHANGES`

Two present-tense factual claims are contradicted by files in the same tree:
`manifest.yaml:121` claims test coverage the suite does not have, and `manifest.yaml:6` claims
a baseline count off by a factor of twenty. Everything else the rewrite asserts — the two
guards and their line numbers, the six test cases and what each pins, the `gates.yml`
invocation, the scope move, and all five behavioural cases — reproduces exactly, and round 3's
blocking item is closed.

The lifecycle record is otherwise sound: `implementation.status: NOT_STARTED` is correct, AC3
is correctly identified as the whole of the remaining work, and the `review` block claims no
approval it does not have. This verdict is on the record, not on any implementation; no
implementation exists.
