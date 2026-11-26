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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "All figures come from the GitHub REST API and from local reads on 2026-11-21; the 2026-11-25 annotation in section 7 records no new measurement and changes no number."
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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004 — Issue Closed With Unmet Acceptance Criteria

**Status**: `OPEN` / `NOT_REMEDIATED`
**Defect class**: Governance Conformance — Acceptance Closure Integrity
**Severity**: High
**Failure mode**: Closure asserted against acceptance criteria that were never executed
**Discovered**: 2026-11-21 re-check
**Related registers**: `DIRECT-MAIN-001`, `SELF-AUTH-002`, `MERGE-AFTER-RULING-003`

---

## 1. Why this is registered separately

The first three registers record **how code entered `main`** (direct push, gate bypass, merge without review).

This register records **how an Issue was closed**: the closure comment asserts the fix is complete, while most of the acceptance criteria the Issue itself defined were never executed — and were measured as unmet.

This is not the same thing as "the implementation has a bug". A bug is an engineering problem. Claiming unexecuted criteria are satisfied is a record-integrity problem, and it degrades every downstream judgement that relies on the Issue's closed state.

---

## 2. Facts

| Item | Value |
|---|---|
| Issue | #384 `[GOV-DOC] Bilingual documentation gate whitelist does not match the repository tree` |
| Closed by | `oahcom` |
| Closed at | 2026-11-20T18:25:06Z |
| Related PR | #394, `merged_at` 18:25:04Z |
| **Close minus merge** | **2 seconds** |
| PR #394 change | 1 file, `scripts/check_bilingual_docs.py`, `+15/−5` |
| PR #394 reviews | 0 |
| PR #394 check run | `GOV-DOC-001 structural checks` → `failure` |
| PR #394 open-to-merge | 14 seconds |

Issue #384 was authored and filed by this side (same GitHub account `oahcom`), and defined AC-1 through AC-10. The closure comment does not map to them one by one; it supplies three pieces of evidence: a before/after whitelist comparison, the `NORMATIVE_ROOTS` diff, and a fail-closed self-check demonstration.

**A 2-second gap between merge and close** leaves no time to run AC-5, AC-6, AC-7 or AC-9, which require constructing a change set.

---

## 3. Criterion-by-criterion measurement

All results below were produced by execution on a shallow clone of `main @ e2644784c010`, not by reading the code.

Method: set `BASE_SHA` / `HEAD_SHA` / `PR_BODY`, run the in-repo `scripts/check_bilingual_docs.py`, record the exit code.

### AC-1 — derive from the tree, not a hand-maintained list

> The gate derives its normative root set from the repository tree at run time. No hand-maintained list of directory names decides whether a path is normative.

**Measured**: create unpaired `09-storage-and-index/spec.md`, commit, run:

```
$ BASE_SHA=<B> HEAD_SHA=<H> PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
  python3 scripts/check_bilingual_docs.py
Bilingual documentation and prompt-library gate: PASS (1 changed paths inspected).
STDERR: NOTE: 1 changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked
EXIT=0
```

**Verdict: `NOT_SATISFIED`.** `NORMATIVE_ROOTS` is still a module-level literal set (lines 16–20, 9 names). A newly added numbered directory is not recognised as normative; it produces one stderr note and exit code 0. AC-1 requires the opposite behaviour.

### AC-2 — fail when the list names a nonexistent directory

**Measured**: inject `"99-nonexistent"`:

```
STDERR: NORMATIVE_ROOTS references non-existent directories: 99-nonexistent
EXIT=2
```

**Verdict: `SATISFIED`.** This is the one mechanism the fix genuinely implemented.

### AC-3 — every numbered directory covered or explicitly exempted with a reason

**Measured**: `08-bmcp-protocol` is now in the set and covered. But `09-storage-and-index` — created in the AC-1 test — is neither covered nor exempted, and produces no failure.

**Verdict: `PARTIALLY_SATISFIED`.** True for directories that exist **today**; false for directories added **later**, because nothing forces a new directory to be covered or exempted. That is exactly what AC-1 and AC-9 exist to prevent.

### AC-4 — print the normative count and the skipped count; error when both are zero

**Measured** (genuine paired change set, 3 files):

```
STDOUT: Bilingual documentation and prompt-library gate: PASS (3 changed paths inspected).
STDERR: NOTE: 2 changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked
EXIT=0
```

**Verdict: `NOT_SATISFIED`.** Only the skipped count is printed; there is no "paths classified normative" count. The "error when both are zero" branch does not exist in the code at all.

### AC-5 — negative test: direct-push bypass

> given a change set where a normative Chinese document already exists on `main` without a counterpart, and a PR adds only the English counterpart, the gate must **not** report complete bilingual compliance.

**Measured (corrected — see §11.1)**: AC-5 names one shape only — "a PR adds **only** the English counterpart". Reproduced literally:

```
BASE:   08-bmcp-protocol/bypass9.md            (normative source on main, no counterpart)
HEAD:   docs/en/08-bmcp-protocol/bypass9.md    (English side only)

$ BASE_SHA=<B> HEAD_SHA=<H> PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
    python3 scripts/check_bilingual_docs.py
::error::docs/en/08-bmcp-protocol/bypass9.md changed without paired change docs/zh-CN/...
::error::Chinese counterpart does not exist: docs/zh-CN/08-bmcp-protocol/bypass9.md
Bilingual documentation gate: FAIL
EXIT=1
```

**Verdict: `SATISFIED`.**

> **Correction.** This section previously read `NOT_SATISFIED`, on a probe whose HEAD added **both** `docs/en/` and `docs/zh-CN/` (the old record is quoted above). That probe does not have the shape AC-5 describes, and its `PASS` was correct: the source was unpaired on BASE, the PR added both mirrors, so the source became paired.
>
> The previous version also attributed "the gate judges a diff, not a tree" to AC-5. The property is real, but its subject is the 83 pre-existing unpaired paths (§11.3), not AC-5.
>
> Basis: reproduced on `main @ eca6f5706e` and `@ 8dc92c3debde` (`EXIT=1`), and on #351's **real** commit pair `568b847ce39f → af1e93d49d` (`EXIT=1`).

### AC-6 — unpaired normative md fails

**Measured**: lone `02-domain-model/unpaired-*.md`:

```
::error::02-domain-model/unpaired-...md requires both counterparts changed in this PR
::error::Both counterpart files must exist for 02-domain-model/unpaired-...md
Bilingual documentation gate: FAIL
EXIT=1
```

**Verdict: `SATISFIED`.**

### AC-7 — exception without an approval record fails

**Measured**: `PR_BODY="BILINGUAL-EXCEPTION: APPROVED"` with no approval fields:

```
::error::Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE' or a fully documented 'BILINGUAL-EXCEPTION: APPROVED'.
Bilingual documentation gate: FAIL
EXIT=1
```

**Verdict: `SATISFIED`.**

### AC-8 — positive control: a genuine pair passes

**Measured**: source + `docs/en/` + `docs/zh-CN/` in one change set:

```
Bilingual documentation and prompt-library gate: PASS (3 changed paths inspected).
EXIT=0
```

**Verdict: `SATISFIED`.**

### AC-9 — a test asserting the on-disk directory set equals the gate's set

**Measured**: full search for `NORMATIVE_ROOTS` under `scripts/` and `tests/`:

- `scripts/governance/evidence/test_gate_normative_roots.py` has 4 references, all of the form `assertIn("14-ai-development", ...)` or `src.split("/")[0] in ...`.
- No assertion walks the on-disk `^\d\d-` directories and compares them to `NORMATIVE_ROOTS` for set equality.
- PR #394 added or modified no test file (`files = 1`, `check_bilingual_docs.py` only).

**Verdict: `NOT_SATISFIED`.** The test does not exist.

### AC-10 — exercised in the repository test suite, offline-runnable, command and exit code recorded

**Measured**:

```
$ python3 -m pytest scripts/governance/evidence/test_gate_normative_roots.py -q
.................                                                        [100%]
17 passed in 0.36s
```

**Verdict: `PARTIALLY_SATISFIED`.** The suite runs offline and passes, but it is the F-07 test covering the `14-ai-development` pairing conventions; it covers **none** of AC-1, AC-4, AC-5 or AC-9. The closure comment records no test command and no exit code.

---

## 4. Summary

| AC | Requirement | Verdict |
|---|---|---|
| AC-1 | derive from the tree at run time | `NOT_SATISFIED` |
| AC-2 | fail when the list names a nonexistent directory | `SATISFIED` |
| AC-3 | every numbered directory covered or exempted with a reason | `PARTIALLY_SATISFIED` |
| AC-4 | print both counts; error when both zero | `NOT_SATISFIED` |
| AC-5 | direct-push bypass negative test must fail | `SATISFIED` (corrected) |
| AC-6 | unpaired fails | `SATISFIED` |
| AC-7 | unapproved exception fails | `SATISFIED` |
| AC-8 | genuine pair passes | `SATISFIED` |
| AC-9 | directory-set equality test | `NOT_SATISFIED` |
| AC-10 | covered by the suite and recorded | `PARTIALLY_SATISFIED` |

**5 satisfied, 2 partially satisfied, 3 not satisfied.**

> Previously "4 / 2 / 4" with AC-5 as `NOT_SATISFIED`. Corrected per §11.1.

AC-1 and AC-9 are the **core mechanism** criteria: "stop relying on a hand-maintained list" and "a regression test guards it". Both are unmet. AC-4 is the observability criterion and is unmet.

---

## 5. What the fix actually changed

Recording fairly: PR #394 was not a no-op.

| Change | Effect |
|---|---|
| Removed 7 nonexistent directory names | the list no longer contradicts the tree |
| `08-protocols` → `08-bmcp-protocol` | **4 normative md files regained pairing coverage** — a substantive improvement |
| Added module-level `_missing_roots` check | closes one direction of list drift (pointing at nothing) |
| Added skipped-count stderr note | silent skipping became announced skipping |

But it fixed **the current disagreement between list and tree**, not **the mechanism by which they will disagree again**. The latter is what Issue #384 §"Required fix" demanded in its second paragraph:

> If a hand-maintained list is kept for exclusion purposes, add a self-check that fails when a whitelisted directory does not exist, **and fails when a numbered directory exists but is neither whitelisted nor explicitly exempted with a reason**.

The second half is not implemented. Measured: `09-storage-and-index` exists, is not listed, is not exempted, and does not fail.

---

## 6. A structural fact worth stating

The 4 md files under `08-bmcp-protocol` were unchecked before the fix and are checked after it. So **after** the fix, any unpaired change to those files fails.

The corrected AC-5 measurement shows the bypass shape **is** closed: source on BASE, PR adds only EN → `EXIT=1`. That part of PR #394 works.

A **different** shape still passes: a PR that adds the English mirror *and* the Chinese mirror in the same change set reports `PASS`, while an unpaired source on the BASE side is never inspected. That `PASS` is correct behaviour — the source ends up paired — and what it exposes is a scope question: the gate's judgement domain is the diff, not the tree.

That question is outside #384's AC set. It belongs to the existing backlog: see §11.3 and **#407**.

---

## 7. Coupling with the first three registers

| Register | Coupling point |
|---|---|
| `DIRECT-MAIN-001` | the bypass presupposes direct pushes; direct pushes are still happening (`ae5a886f`, `25c61283`, and others) |
| `SELF-AUTH-002` | closer, implementer and reviewer are the same `oahcom`; the closure ruling has no third party |
| `MERGE-AFTER-RULING-003` | PR #394 merged in 14 seconds at `reviews=0` with check `failure`, then the Issue closed 2 seconds later |

All four point at one root cause: **this repository currently has no role separation at all**. Implementation, review, ruling and closure are performed by the same account at second-scale intervals.

> **〔Added 2026-11-25〕** This sentence turns "all four roles carry the login `oahcom`" — an **account-layer** fact — into the conclusion that no role separation exists. §5 was amended on 2026-11-24 by `2eb4e352` (PR #935) to a session-level test (see `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`): a separate session under the same GitHub identity suffices for independence. `/pulls/{n}/reviews` returns only `user.login`, never a session, so "same identity ⇒ same session" cannot be verified from that payload. Read it as "account layer not independent; session layer not verified".
> **What survives:** every checkable field in the four rows above is independent of how identity is defined — `SELF-AUTH-002`'s closer is the sole account, PR #394 carried `reviews=0` with a `failure` check, the 14-second interval, and the second-scale timing itself. Those support "no third party took part in these four acts". They do not support "role separation is structurally absent". The difference is *did not happen* versus *cannot happen*, and the original sentence states the second.

---

## 8. Corrective measures (pending approval, not executed)

| # | Measure | Nature | Status |
|---|---|---|---|
| N-1 | Reopen #384, or file `#384-FOLLOWUP`, scoped only to AC-1, AC-4, AC-5, AC-9 | Scope correction | **Executed 2026-11-20** — #384 reopened, verdict comment `7048799466`, body scope clause added |
| N-2 | Add a post-closure annotation to #384 stating "of 10 ACs, 4 satisfied, 4 not satisfied", linking this register | Retrospective annotation | **Executed** — folded into the same verdict comment |
| N-3 | Implement AC-5's bypass detection | Implementation | **Withdrawn** — AC-5 measured as satisfied, see §11.1 |
| N-4 | Implement AC-9's directory-set equality test | Implementation | Not executed |
| N-6 | Independent inventory of the 83 existing unpaired paths | Backlog | **Filed as #407**, see §11.3 |
| N-5 | State in `PR-GOVERNANCE-001` that an Issue closure comment must list a verdict per acceptance criterion, and that a closure without such a list may not be treated as acceptance | Normative | Not executed (requires Owner) |

N-5 is the only measure that stops this class of defect recurring. N-1 through N-4 only repair the instance.

---

## 9. Verification evidence

| Evidence | Value |
|---|---|
| Re-check baseline | `main @ e2644784c010da488b4794f3e6b10d17c32e9b4b` |
| Gate script blob | `check_bilingual_docs.py` @ main, 20451 bytes |
| AC-1 measured | new `09-storage-and-index/spec.md` → `PASS`, `EXIT=0` |
| AC-2 measured | inject `99-nonexistent` → `EXIT=2` |
| AC-4 measured | 3-file paired change set → only stderr skipped count, no normative count, `EXIT=0` |
| AC-5 measured | #351 shape reproduced → `PASS`, `EXIT=0` |
| AC-6 measured | unpaired md → `EXIT=1` |
| AC-7 measured | unapproved exception → `EXIT=1` |
| AC-8 measured | three-file pair → `EXIT=0` |
| AC-9 measured | 4 `NORMATIVE_ROOTS` references repo-wide, all membership assertions, no set-equality assertion |
| AC-10 measured | `pytest ... test_gate_normative_roots.py` → `17 passed in 0.36s` |
| close-minus-merge gap | merge 18:25:04Z → close 18:25:06Z, 2 seconds |
| PR #394 | `files=1`, `reviews=0`, check `failure`, open-to-merge 14 seconds |

The re-check ran on a shallow clone of `main`; test change sets were local temporary commits, **never pushed, never modifying the remote**.

---

## 10. Explicitly not done

- #384 was not reopened by this register's first draft; the reopening was a separate Owner ruling and is recorded in §8 N-1.
- No finding that the fixer's technical judgement was wrong. All four changes in PR #394 are correct; the problem is scope.
- No argument that #394 should be reverted. Restoring coverage for `08-bmcp-protocol` is a net improvement; reverting makes things worse.
- No finding that the closer knew the ACs were unmet. A 2-second gap proves verification did not run; it does not prove intent.
- No modification of the gate script. N-3 and N-4 are implementation work assigned elsewhere; this session does not write the code.

---

**Register conclusion**: Issue #384 was closed with **3 of its own 10 acceptance criteria unmet, 2 partially met, 5 satisfied**, the first closure 2 seconds after the fix merged. The core mechanism criteria (AC-1 tree derivation, AC-9 regression test) are unimplemented and AC-4 observability is unimplemented; AC-5 bypass detection **is** implemented. Recommendation: annotate #384's closure as `AC_PARTIALLY_UNMET` rather than `FIXED`.

---

## 11. Fifth verification round: corrections to this document (after 2026-11-21 03:30Z)

### 11.1 AC-5 verdict corrected: `NOT_SATISFIED` → `SATISFIED`

**What was wrong.** The §3 AC-5 probe added **both** mirrors. AC-5's text says "adds **only** the English counterpart". A probe with a different change set cannot decide the criterion.

**Why the old `PASS` was not a defect.** The source was unpaired on BASE; the PR added both mirrors; the source became paired. Reporting compliance is correct.

**Re-measured** on `eca6f5706e`, on `8dc92c3debde`, and on #351's real pair `568b847ce39f → af1e93d49d`: all `EXIT=1`.

### 11.2 The right home for "the gate judges a diff, not a tree"

Real property, wrong criterion. At `main @ 8dc92c3debde` a full-tree scan reports **409 in-scope, 107 exempt, 83 violations, `EXIT=1`** — the same 83 as at `ae5462f6ef`. N-3 is withdrawn; the 83 go to #407.

### 11.3 New carrier: #407, disposition of the existing 83

Gate fix (#401) and backlog disposition (#407) have different acceptance objects. #401 answers "can the gate see a base-side unpaired source?" with purpose-built negative tests. #407 answers "have the existing 83 been individually disposed of?" with per-path classification and reasons. Merging them lets either one cover for the other.

### 11.4 New facts tied to this register

| Fact | Value | Effect |
|---|---|---|
| PR #403 merged | 03:26:28Z, `merged_by=oahcom` | the "counterexample" lasted 7 hours; the 10-minute prediction failed, the merge still happened |
| One review preceded it | 03:26:13Z, `COMMENTED`; author = reviewer = merger = `oahcom` | "has a review" ≠ "has an independent review"; gap 15 seconds |
| Check at merge | `GOV-DOC-002 metadata checks` = `failure` | merged with a failing check |
| #384 closed again | 20:06:51Z, 2 s after #402 merged | the 19:34Z reopen was overridden 32 minutes later; third closure |
| Direct pushes | **53 → 62** (9 new, incl. 2 by `governance@localhost`) | `DIRECT-MAIN-001` §14 |
| Gate implementation rewritten by direct push | `1733c3bf4a` +721/−166, `0f5b5a00e7` +141/−63 | the checker changes with no PR and no review |
