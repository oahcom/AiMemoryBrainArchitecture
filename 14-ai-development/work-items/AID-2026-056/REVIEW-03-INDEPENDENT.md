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
      last_verification_note: "This record states the state the third review actually examined, origin/main at ebadbe84, and not the state after the fixes it produced. The four follow-up fixes (D1-D3 and the erratum byte claim) are later, are the author's, and are not covered by this verdict. origin/main has since advanced to 431525c5; the six files this verdict covers are byte-identical across that range."
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

# REVIEW-03 — AID-2026-056 (round 3, independent)

Reviewer: rev3-056b (independent; did not author any file under review)
Repo: /tmp/opencode/amb2
Reviewed commit: `origin/main` = **ebadbe84** (as instructed)
NOTE: `origin/main` has since advanced to `ba293506`. Diff `ebadbe84..ba293506` touches only `14-ai-development/work-items/INDEX.md`, and only the **AID-2026-055** row. AID-2026-056's five files are byte-identical in both. Review therefore holds for current main too.

Method: files read via `git show <sha>:<path>`; nothing checked out, nothing modified.

---

## 1. Manifest parse + duplicate-key detection

Command:
```
py parse_manifest_056.py manifest.yaml     # yaml.SafeLoader subclass whose construct_mapping
                                           # records any key already seen at the same node
```

Real output:
```
PARSE: OK
DUPLICATE KEYS: none
TOP-LEVEL KEYS: ['work_item_id', 'title', 'class', 'risk', 'risk_rationale', 'security_scope',
 'authorization', 'scope', 'prompt_supersession', 'status', 'sponsor', 'accountable_owner',
 'implementing_ai_session', 'repository', 'base_branch', 'base_commit_sha', 'tracking_issue',
 'created_at', 'updated_at', 'prompt_id', 'prompt_version', 'prompt_file', 'prompt_status',
 'prompt_sha256', 'prompt_bytes', 'prompt_provenance_tier', 'prompt_provenance_note',
 'dependency_refs', 'owner_decisions', 'deliverables', 'acceptance_criteria',
 'withdrawn_acceptance_criteria', 'independent_reviewer', 'integration_reviewer', 'review',
 'acceptance', 'implementation', 'errata', 'findings']
```

Shape: `acceptance_criteria` = 10 items (AC1, AC2, AC3, AC4, AC5, AC6a, AC6b, AC7, AC8, AC9);
`withdrawn_acceptance_criteria` = 1 (AC6); `prompt_supersession.superseded` = 5; `findings` = 8 (F1–F8).

Result: **PASS** — parses clean, no duplicate mapping keys.

---

## 2. `prompt_supersession` — do the quotes exist, do the targets exist

`grep -nF <quote> prompt-v1.md` for each `prompt_item`, and each `replaced_by` id looked up in
`acceptance_criteria`.

| # | `prompt_item` claim | quote found in prompt-v1.md? | `replaced_by` id exists? |
|---|---|---|---|
| 1 | AC1 "(exactly 9 violations)" | **Not verbatim.** `grep -F 'exactly 9 violations'` → no match. Line 122: ``reports **9** violations, and the nine are exactly the C list in §2. Not "about 9": the set equality is the criterion.`` Semantically an accurate paraphrase — the prompt does demand set equality. | AC1 ✓ |
| 2 | AC2 "(72 removals = 6 side-by-side + 66 embedded)" | Line 123: ``The baseline diff is **72 removals, 0 additions**, and the 72 are exactly the A and B classes.`` The `= 6 + 66` split is not stated in AC2, but §2's table gives A=6, B=66. Accurate derivation. | AC2 ✓ |
| 3 | AC5 "(two negative assertions)" | Line 126: exactly two negative cases (`cjk = 99`/`latin = 5000`; `cjk = 100`/`latin = 999`). Verbatim in substance. | AC5 ✓ |
| 4 | AC6 + §5 bullet citing "81 to 9 prediction" | Line 127 (`the seven non-existent roots are still listed`); line 113 (`It lists 15 roots, 7 of which do not exist on disk`; `81 → 9 prediction`). Both present. | AC6a ✓ and AC6b ✓ |
| 5 | AC8 "`python3 -m unittest scripts.test_check_bilingual_docs_full`" | Line 129: **verbatim, exact.** | AC8 ✓ |

Result: all five quotes correspond to real prompt text; one (#1) is a paraphrase rather than a
literal quote, which is honest for a "prompt_item" label but is not a string that can be grepped —
a reader cannot reproduce it as a citation. All five `replaced_by` targets resolve to ids that
exist in `acceptance_criteria` (AC6a/AC6b, not the withdrawn AC6).

### `not_superseded` — is anything claimed to "stand as written" that the manifest actually changes?

The clause claims standing for: the ruling in `owner_decisions`, the floor 100/1000,
the blueprint control, **AC3, AC4, AC9**, and AC7 (explicitly "strengthened rather than replaced").

- **AC7** — disclosed as strengthened. Fine.
- **AC3** — prompt: "a fourth `.zh-CN.md` mirror added in a test fixture"; manifest: "a `.zh-CN.md`
  mirror created in a test fixture", plus a parenthetical saying it **is already true at 8e489ec1**
  and "is a regression guard, not a task". The requirement is unchanged; the *force* is downgraded
  from task to guard. Disclosed in the same text. Not a contradiction.
- **AC9** — identical wording both sides (`77 frozen, 0 new gaps`). But note the collision flagged in
  §3 below: **77** is also the full-scan violation count at 8e489ec1. Two different sevens-sevens.
- **AC4** — **not fully "as written".** Prompt AC4 is one sentence ("is still a violation after the
  change"). Manifest AC4 adds `0 CJK`, `49758 bytes as a git blob at 8e489ec1`, `LF line endings`,
  and a paragraph correcting the byte figure. The same `not_superseded` string then says the 49666
  figure "is corrected in AC4 of this file" — i.e. it simultaneously asserts AC4 stands and records
  that AC4 was amended. The amendment strengthens the check and is disclosed, so this is a wording
  defect, not a lost requirement.

Result: **no criterion is silently reversed.** One wording inconsistency (AC4 claimed to "stand as
written" while being rewritten in the same document). Not blocking on its own — the reader is told.

---

## 3. The four numbers, run rather than recalled

### 3a. Blueprint blob size (claimed 49758)
```
$ git cat-file -s 8e489ec1:13-engineering-decisions/technology-architecture-blueprint.md
49758
```
**CONFIRMED.** Also 49758 at d40d4e09, ac0f0dfd, ebadbe84, ba293506 — the file has exactly one
commit in history (`git rev-list --all -- <path>` returns 1), so grepping every historical blob for
size 49666 finds nothing. AC4's statement that "49666 from the prompt matches no version in git
history" is **TRUE**, and the prompt's 49666 (§2 line 85) is unreproducible.

### 3b. Line count (claimed 730; 49758+730=50488)
```
$ git show 8e489ec1:13-engineering-decisions/technology-architecture-blueprint.md | wc -l
730
$ git show 8e489ec1:13-...-blueprint.md | tail -c 20 | xxd | tail -1
00000010: 6f6e 2e0a                                on..
```
**CONFIRMED.** 730 newline terminators, last byte `0x0a`, so every line is LF-terminated and a CRLF
checkout adds exactly 730 bytes: 49758 + 730 = **50488**. AC4's explanation of why 50488 appeared
(REVIEW-01 header line 23 records "blueprint 50488 bytes") is correct, and anchoring on the blob
size plus the line-ending convention is the right call.

### 3c. `python3 scripts/check_bilingual_docs_full.py | tail -1` (claimed 77 / 659 in-scope / 208 exempt)

The command as written does **not** produce a count:
```
$ python3 scripts/check_bilingual_docs_full.py | tail -1
GOV-DOC-001 full scan: FAIL
```
The summary is the **first** line.
```
$ python3 scripts/check_bilingual_docs_full.py | head -1
GOV-DOC-001 full scan: 664 in-scope Markdown files; 211 exempt; 77 violations.
$ python3 scripts/check_bilingual_docs_full.py | grep -cE '^[0-9]{3}\. '
77
```

Measured at each commit (each via `git archive <sha> | tar -x` into a scratch dir, `git init`,
`git add -Af`, commit, then run the script — force-add so `.gitignore` cannot shrink the tracked set
inside a fresh repo):

| commit | in-scope | exempt | violations |
|---|---:|---:|---:|
| `ac0f0dfd` (erratum's measurement point) | 647 | 202 | 77 |
| `8e489ec1` (AC1/AC4's measurement point) | 657 | 206 | 77 |
| `ebadbe84` (reviewed commit) | 662 | 211 | 77 |
| `ba293506` (current main) | 664 | 211 | 77 |

- **77 violations: CONFIRMED at all four commits.**
- **659 in-scope / 208 exempt: NOT REPRODUCIBLE.** No file under review states those numbers —
  `grep -nE '659|208'` over manifest.yaml, ERRATUM-01.md, REVIEW-01.md, REVIEW-02.md, prompt-v1.md
  returns nothing. REVIEW-01 line 127 tabulates "**656 / 205** / 77", which is also off by exactly 1
  in each column against the 657 / 206 measured at the commit it names (consistent with one file
  landing after the measurement). The in-scope/exempt counters are the only figures here that do not
  reproduce — and they are decorative: no acceptance criterion cites them.

### 3d. Decompose 77 = 66 embedded + 11 real — own script over the repo's own scan logic

`decompose_056.py` imports `check_bilingual_docs_full` and `check_bilingual_docs` and calls
`m.tracked_paths`, `m.in_scope`, `m.counterpart`, `m.EMBEDDED_BILINGUAL_SOURCES`. It does not
re-implement pairing; it only counts characters.

```
$ py decompose_056.py <repo>
in_scope=664 exempt=211 violations=77

embedded (cjk>=100 AND latin>=1000): 66
real (not both):                    11
one-sided (exactly one met):        11
sum = 77
```
Same run at `8e489ec1`: `in_scope=657 exempt=206 violations=77` → **66 + 11 = 77**.

The 11, with my own counts:
```
00-governance/reports/gov-doc-001-full-scan-2026-11-20.md   cjk=35  latin=18497
06-memory-context/context-architecture.md                   cjk=0   latin=13906
06-memory-context/context-budget-and-sufficiency.md         cjk=0   latin=7667
06-memory-context/context-edit-operations.md                cjk=0   latin=11214
06-memory-context/context-manager.md                        cjk=0   latin=11019
06-memory-context/context-reconciliation.md                 cjk=0   latin=25184
06-memory-context/context-versioning.md                     cjk=0   latin=28669
06-memory-context/phase-3.8.6-g-review-storage-serialization-anchor.md  cjk=21 latin=1135
08-bmcp-protocol/phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md  cjk=72 latin=3341
08-bmcp-protocol/phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md cjk=4 latin=2603
13-engineering-decisions/technology-architecture-blueprint.md cjk=0 latin=39156
```
**66 + 11 CONFIRMED, independently.** The two `08-bmcp-protocol` rows carry exactly the counts
ERRATUM-01 §2(B) records (72/3341, 4/2603), every one of the 11 fails `cjk>=100`, and the blueprint
is the only `cjk=0` file in the set that is also huge. AC1's 11 and AC2's 66 are mutually consistent
and both match the tree.

Ancillary check made while there — ERRATUM-01 line 68 claims the two baselines are "byte-identical, 77 = 77":
```
$ git ls-files -s scripts/ci/baselines/bilingual-docs.txt scripts/bilingual-baseline.txt
100644 b7f3dc33... 0	scripts/bilingual-baseline.txt
100644 6166b186... 0	scripts/ci/baselines/bilingual-docs.txt
$ diff <(git show HEAD:scripts/bilingual-baseline.txt) <(git show HEAD:scripts/ci/baselines/bilingual-docs.txt)
1,3d0
< # Frozen inventory of pre-existing bilingual documentation gaps.
< # This baseline may only shrink; entries must never be added.
< # Regenerate only when explicitly adopting a new baseline.
80c77
< ...SESSION-4-ADOPTION-ISOLATION-REPORT.md
\ No newline at end of file
```
**"Byte-identical" is FALSE.** Gate A's file carries three comment lines and no trailing newline;
gate B's has neither. The **entry sets are identical (77 = 77)** — that part is true. Wording defect:
no criterion depends on it, and the files must stay separate anyway (`files_not_to_touch` names
gate A's).

Other numbers checked in passing:
- `prompt_sha256` 325f567c…d2e4 and `prompt_bytes` 10114 → `sha256sum`, `wc -c` both **match**.
- `EMBEDDED_BILINGUAL_SOURCES` "21-entry allowlist" (ERRATUM §3.1) → `len() == 21` **matches**.
- blueprint `cjk=0` **matches**; `latin=39156` **matches** the prompt's §2 figure.


---

## 4. Internal consistency

### 4a. Does any criterion require something `authorization:` forbids?

| criterion | action required | authorisation field | verdict |
|---|---|---|---|
| AC1 (11 violations, set equality) | predicate change in `check_bilingual_docs_full.py` | `gate_behaviour_change: GRANTED by OD-18` | consistent |
| AC2 (66 removals, 0 additions) | edit `scripts/ci/baselines/bilingual-docs.txt` | `baseline_content_change: GRANTED-FOR-SHRINK-ONLY` | consistent |
| AC6a (do not modify `NORMATIVE_ROOTS`) | restraint | `root_membership_change: NOT_GRANTED` | consistent, and AC6a *is* the prohibition |
| AC8 (tests in `tests/test_check_bilingual_docs_full.py`) | write tests | `scope.files_to_modify` names that file | consistent |
| deliverable 5 / AC for `gates.yml` prose | edit one comment | `workflow_comment_change: GRANTED` | consistent |
| AC9 (gate A still `77 frozen`) | read-only re-run; gate A's file in `files_not_to_touch` | consistent | consistent |

**No criterion demands an action that `authorization:` forbids.** Two near-misses worth recording:

1. `scope.files_to_create: []` while AC3 requires "a `.zh-CN.md` mirror **created in a test fixture**".
   If that fixture is a tracked file, no authorisation covers creating it. It is satisfiable only if
   the fixture is built in a tempdir at run time. Under-specified rather than contradictory.
2. AC2 and AC9 would be **mutually unsatisfiable** if gate A's baseline and gate B's baseline were
   the same file. They are not (`git ls-files -s` gives two blobs, 6934 and 7119 bytes, and
   `files_not_to_touch` names gate A's). ERRATUM-01 line 68's "byte-identical" claim would, if
   believed, make the work item impossible; the measured state saves it. This is the one place where
   an erratum error is load-bearing in the reader's mind even though the tree is fine.

### 4b. `status` / `review.status`
```
status: DISPATCHED                                    → holds
review.status: CHANGES_APPLIED_AWAITING_RE_REVIEW     → holds
review.status == APPROVED?                            → NO (it is not APPROVED)
review.prior_status: CHANGES_REQUESTED
review.rounds_completed: 2
acceptance.status: NOT_ASSIGNED      implementation.status: NOT_STARTED
```
All consistent with "dispatched, not approved, not implemented".

### 4c. INDEX row 46 vs the manifest

| INDEX row 46 says | manifest says | agrees? |
|---|---|---|
| `DISPATCHED` | `status: DISPATCHED` | ✓ |
| "AC1 restated to 11 violations with set equality" | AC1: exactly 11, set equality | ✓ |
| "AC2 to 66 removals" | AC2: 66 removals, 0 additions | ✓ |
| "AC6 withdrawn to AC6a/AC6b" | `withdrawn_acceptance_criteria[AC6]`, AC6a/AC6b present | ✓ |
| "AC5 now four assertions on both sides" | AC5: four assertions, two per side | ✓ |
| "AC8 module path corrected" | AC8: `tests.test_check_bilingual_docs_full` | ✓ |
| "baseline regenerated **77 → 11** as 66 removals" | risk_rationale 77→11; AC2 66 removals (77−66=11) | ✓ (and INDEX is *more* correct than `deliverables`) |
| "eight registered (F1-F4 closed, F5-F8 recorded)" | `findings` = F1…F8, 8 entries | ✓ |
| "`REVIEW-02-INDEPENDENT.md` is the live report, `REVIEW-01…` the one it answers" | `review.report_ref` / `prior_report_ref` | ✓ |
| SHA-256 `325f567c…d2e4`, 10114 bytes | `prompt_sha256`, `prompt_bytes`; both re-measured | ✓ |
| `CHANGES_APPLIED_AWAITING_RE_REVIEW` | `review.status` | ✓ |

**INDEX row 46 agrees with the manifest on every field it states.** No disagreement on status,
no disagreement on 11 / 66 / 77, correct report reference.

### 4d. Internal contradictions *inside* the manifest — two of them, both real

Both are in `deliverables:`, which is the list an implementer works from. Both are grep-able.

**(D1) `deliverables[3]` still says the baseline is regenerated "from 81".**
```
$ git show ebadbe84:.../manifest.yaml | grep -n 'from 81'
63:      why: "... only its rationale moved, from 81 to 9 to 77 to 11."
136:  - "The baseline regenerated from 81 to the number the new predicate actually produces, as removals only and 0 additions, in the same commit."
225:      - "risk_rationale: 'shrinks its frozen baseline from 81 to 9' — the baseline is already 77 and will shrink to 11, not from 81 to 9."
$ git show HEAD:scripts/ci/baselines/bilingual-docs.txt | wc -l
77
```
The baseline has **77** entries, not 81. 81 − 66 = 15 ≠ 11, so a literal reading of this
deliverable cannot reach AC1. `risk_rationale` was corrected to "77 to 11", `OD-18.constraints[3]`
was annotated to 11, and INDEX row 46 says "77 → 11" — this one line was missed. It is the exact
defect REVIEW-01 B2 found, surviving in the field that tells the implementer what to build.

**(D2) `deliverables[5]` still says the test asserts "the 9 still reported".**
```
$ git show ebadbe84:.../manifest.yaml | grep -n 'still reported'
138:  - "At least one test per clause: ... side-by-side recognised, and the 9 still reported."
148:    text: "AC4 ... is still reported as a violation. (Byte count corrected twice ...)"
```
AC1 requires **11**, by set equality. `deliverables[5]` requires a test asserting **9**. An
implementer who writes the deliverable's test fails AC1 and vice versa. The correction in
ERRATUM-01 §2(B) ("the nine are the whole of the real backlog is now false") was applied to AC1 and
to `OD-18.constraints[3]` and to `risk_rationale` — and not to this line.

Neither of these changes a number that a *check* reads, and `prompt_supersession.governing_block`
declares `acceptance_criteria` as what governs. So the machine-readable core is right and the two
lines are prose. But they are the instructions the implementer reads first, they contradict the
governing block by name, and they are the same defect class round 2 rejected the file for — a
manifest whose prose still says what its criteria were corrected away from.

Two smaller ones, recorded and not counted as blocking:
- `not_superseded` claims AC4 "stands as written in the prompt" while AC4 is rewritten in the same
  document (49758 / LF / 0 CJK added). `deliverables[0]` is likewise a no-op — ERRATUM (C) says the
  work is already done by #910, so deliverable 1 of 6 cannot be distinguished from "never needed
  doing", which AC3 itself admits in its own parenthetical.
- `errata[0].summary` (F) says "AC4 ... stand unchanged" while `errata[0].status` says (F) is
  reflected in "AC4", which was changed. Same wording collision as above.


---

## 5. Closure table — REVIEW-01 (B1–B5) and REVIEW-02

| Finding | Status | Evidence that decides it |
|---|---|---|
| **R1-B1** AC6 requires reintroducing the #910 defect | **CLOSED** | `AC6` appears only under `withdrawn_acceptance_criteria` (`status: WITHDRAWN`, `superseded_by: [AC6a, AC6b]`); `acceptance_criteria` carries AC6a ("does not modify NORMATIVE_ROOTS… guard still exits 0") and AC6b ("Withdrawing AC6 grants no authority to change"). Parse output lists exactly those ids. |
| **R1-B1 (second half)** — prompt still commands AC6, and nothing says which file wins | **CLOSED** | `prompt_supersession.governing_block: "acceptance_criteria in this file"`, plus five `superseded` entries with a stated `reason` (prompt FROZEN). The prompt's AC6 line (line 127) is still there — it cannot be edited — but it is now named as superseded in the same directory. |
| **R1-B2** AC1 says 9; AC2's 72 cannot reach it | **CLOSED** | Manifest AC1 = 11 with set equality; AC2 = 66 removals, 0 additions. My independent decomposition: `66 + 11 = 77`, and 77 − 66 = 11, so AC1 and AC2 are arithmetically mutually reachable for the first time. |
| **R1-B3** AC5 asserted the floor on one side only | **CLOSED** | AC5 text now: negatives `cjk=99/latin=5000`, `cjk=100/latin=999`; positives `cjk=100/latin=1000`, `cjk=101/latin=1001`. Four assertions, two per side. A predicate resolving nothing now fails. |
| **R1-B4** AC8 names `scripts.test_check_bilingual_docs_full` | **CLOSED** | AC8 now names `tests.test_check_bilingual_docs_full`; `python3 -m unittest tests.test_check_bilingual_docs_full` → `Ran 7 tests … OK`. |
| **R1-B5** no machine-readable file authorisation | **CLOSED** | `authorization:` present with 6 keys (`implementation_write`, `gate_behaviour_change`, `baseline_content_change`, `allowlist_change`, `root_membership_change`, `workflow_comment_change`); `scope:` with `files_to_create` / `files_to_modify` (4) / `files_not_to_touch` (2). |
| **R1-M1** every premise figure stale | **PARTIALLY-CLOSED** | 77 / 66 / 11 / 49758 / 730 all confirmed by measurement in §3. But `deliverables[3]` still says "from 81" and `deliverables[5]` still says "the 9 still reported" — the same defect class, in the field the implementer reads as the build list. |
| **R1-M2** erratum claimed 6-for-6 sync, was unconverted | **CLOSED** | `errata[0].status` now narrowed to "(A), (B), (C), (E), (F) … Item (D) is reflected as a recorded deviation"; `risk_rationale` says 77→11; `OD-18.constraints[3]` annotated with 11. |
| **R1-M4** empty baseline passes the ratchet | **CLOSED AS RECORDED, NOT FIXED** | Not a criterion defect: recorded in AC7's NOTE with the measured behaviour and turned into a requirement ("baseline non-empty and exactly 11 lines"). The script itself is AID-2026-060's scope. Acceptable here. |
| **R1-M5 / F6** `OD-22(a)` cannot be verified | **OPEN, disclosed** | Manifest F6: "Unresolved, and recorded as unresolved." Nothing was fixed; the reader is told. Judgement call, not a defect of fact. |
| **R2-B2/B3/B4/M4** (re-confirmed closed) | **CLOSED** | Independently re-measured here: 11 = 11, four assertions present, `Ran 7 tests … OK`, and my own §3d decomposition reproduces 66 + 11 without trusting the report. |
| **R2-B5** no authorisation block | **CLOSED** | See R1-B5 above; block exists and is internally consistent (§4a). |
| **R2-B1 (prompt half)** | **CLOSED** | See R1-B1 second half; `governing_block` + five enumerated supersessions. |
| **R2-M1** non-reproducible byte count | **CLOSED** | AC4 now names 49758 as the git blob at `8e489ec1` with LF; `git cat-file -s` = 49758 at every commit; `wc -l` = 730; 49758 + 730 = 50488 explains the old figure exactly. |
| **R2-M2** erratum claimed more than delivered | **CLOSED** | Status line narrowed, and it names the review that caught it. |
| **R2-M3** `security_scope` answering the wrong question | **CLOSED** | manifest lines 10–17: "security_scope answers 'what can be attacked'. It does not answer 'does this need independent review' … security_scope: None is therefore correct and is not a reason to skip independent review". |
| **NEW-D1** `deliverables[3]` says baseline regenerates "from 81" | **OPEN — blocking** | `grep -n 'from 81'` → line 136, in `deliverables`. Baseline is 77 entries (`wc -l`). 81−66=15≠11. Contradicts AC1/AC2/`risk_rationale`/INDEX. |
| **NEW-D2** `deliverables[5]` requires a test asserting "the 9 still reported" | **OPEN — blocking** | `grep -n 'still reported'` → line 138, in `deliverables`. AC1 requires 11 by set equality. The build list and the criteria demand different tests. |
| **NEW-D3** AC1's set-equality anchor does not exist where it says | **OPEN — blocking** | AC1: "the eleven paths enumerated in `ERRATUM-01.md` section 2". Measured: ERRATUM §2 lists **two** paths (§2(B)); §4's AC1′ says "the prompt's nine C paths … plus the two", i.e. it points back at prompt §2 rather than enumerating eleven. `grep -cE '\.md'` over ERRATUM §2 → 5 matches, none of them the nine. The eleven are derivable only by stitching two documents, which is the defect AC1 says it exists to remove. |
| **NEW-D4** ERRATUM claims the two baselines are "byte-identical" | **OPEN — minor** | Two different blobs (b7f3dc33 vs 6166b186, 6934 vs 7119 bytes); diff shows 3 comment lines and a missing trailing newline. Entry *sets* are identical; bytes are not. Harmless as long as no reader believes AC2 and AC9 act on one file. |
| **NEW-D5** in-scope/exempt counters | **OPEN — minor** | `659 / 208` (as commissioned) and `656 / 205` (REVIEW-01 line 127) both fail re-measurement: 657/206 at `8e489ec1`, 662/211 at `ebadbe84`, 664/211 at `ba293506`. No criterion cites them. |

---

## Verdict

**`REQUEST-CHANGES`**

What holds, and holds under adversarial measurement:

- the manifest parses, with no duplicate mapping keys;
- all five `prompt_supersession` entries point at real prompt text and at acceptance-criteria ids that
  exist, and one declared governing block now resolves the "two files, no rule" defect of round 1;
- **77 = 66 embedded + 11 real**, reproduced by importing the repository's own scan functions rather
  than trusting the report, at both commits the documents name; 77 − 66 = 11, so AC1 and AC2 are
  finally consistent with each other and with the tree;
- **49758** bytes, **730** lines, **50488** = 49758 + 730, and 49666 matching no blob in git history;
- prompt SHA-256 and byte count; INDEX row 46 agreeing with the manifest on status, 11, 66, 77→11 and
  the report reference; `status: DISPATCHED`, `review.status: CHANGES_APPLIED_AWAITING_RE_REVIEW`,
  not APPROVED;
- every REVIEW-01 blocking finding B1–B5 and every REVIEW-02 open item closed by something I could
  re-run.

What blocks it is one layer, and it is the layer round 2 rejected the file for: **the prose that tells
the implementer what to build still contradicts the acceptance criteria that govern.**

1. `deliverables[3]` (line 136) regenerates the baseline "from 81". It has 77 entries; the arithmetic
   in that sentence cannot reach AC1's 11.
2. `deliverables[5]` (line 138) requires a test that asserts "the 9 still reported", while AC1
   requires 11 by set equality and calls 9 the value #910 invalidated.
3. AC1 anchors its set equality on "the eleven paths enumerated in `ERRATUM-01.md` section 2", and
   that section enumerates two paths, not eleven. The authoritative eleven exist only as a
   cross-document sum.

Each is a one-line fix in an editable file. None is a measurement I am disputing — the numbers in the
criteria are right; three sentences elsewhere in the same file still describe the state those numbers
replaced, and an implementer reading `deliverables` before `acceptance_criteria` will build to the old
state. That is exactly what "CHANGES_APPLIED" was supposed to have ended.

Fix the three lines, re-run nothing (no number changes), and this is an APPROVE.

