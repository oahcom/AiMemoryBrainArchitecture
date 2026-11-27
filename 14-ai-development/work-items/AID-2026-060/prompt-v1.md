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
      last_verification_note: "The empty-baseline pass was reproduced at b80e5a40 by running gate_ratchet.py with an empty baseline and a command that exits 9: regressions=0 fixed=0 PASS exit 0. The non-empty case was measured on the same tree and does fail closed (fixed=77 FAIL). The comment claiming 'never as a pass' is quoted from the file, not paraphrased."
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

# AID-2026-060 — The ratchet's fail-closed guarantee does not hold on an empty baseline

**Status:** `PROPOSED` · **Class:** GATE/CODE/TEST · **Risk:** R2
**Measured at:** `main` @ `b80e5a40`
**Raised by:** owner ruling OD-26 on Issue #266, after independent review of AID-2026-056 surfaced it as a floor the work item could not supply.
**Author:** owner delegate under standing instruction.

---

## 1. The defect

`scripts/ci/gate_ratchet.py` carries a comment describing its own safety property:

> a crash yields zero items and is caught below as a stale baseline (fail-closed), never as a pass

The property is not true for an empty baseline. Measured:

```bash
: > /tmp/empty_base.txt
python3 scripts/ci/gate_ratchet.py \
  --baseline /tmp/empty_base.txt \
  --format paths \
  --command "python3 -c 'import sys; sys.exit(9)'"
```

```
baseline=0 current=0 regressions=0 fixed=0
PASS - failure set matches the baseline exactly.
exit 0
```

The command exited **9**. The ratchet reported **PASS**.

The same command against a non-empty baseline does fail closed:

```
--baseline scripts/ci/baselines/bilingual-docs.txt (77 entries)
-> fixed=77, FAIL, exit 1
```

So the guarantee holds for one input class and silently does not hold for another. The comment does not distinguish them.

## 2. Why this is not AID-2026-056's problem

AID-2026-056 regenerates `scripts/ci/baselines/bilingual-docs.txt` from 77 entries down to 11. If the regeneration ever emits an empty file — and *a predicate that resolves everything* is precisely how an empty file gets produced — then the required check `Bilingual docs coverage (ratchet)` stays green forever, including over a crashing command.

AID-2026-056's AC7 now requires the implementer to assert the regenerated baseline is non-empty with exactly 11 lines. That protects **this** generation. It does not protect the next one, from any other work item, on any other baseline.

Owner ruling OD-26 makes the distinction explicit:

> AID-2026-056 AC7：确保这次生成的基线内容符合预期。新守卫工作项：确保以后任何工作项都不能利用空基线把命令失败伪装成通过。

Two guards at two layers. This work item is the second layer.

## 3. The defect is larger than the empty baseline

Writing the test exposed a second gap while measuring: the ratchet compares **path sets** only. A command that fails without emitting paths produces the same empty current-set as a command that succeeds with nothing to report. `--format paths` discards the exit code.

That means the empty-baseline case is a *symptom*. The general condition is: **the ratchet cannot distinguish "the check was never run" from "the check ran and found nothing".** This is the same shape as the defect AID-2026-058 exists to fix in `check_traceability.py`, one level up: a checker that reports a clean result over inputs it never read.

The fix must therefore key on the command's exit code, not only on baseline emptiness.

## 4. Required behaviour

1. **An empty baseline is rejected.** It is not a valid zero-item baseline; it is the absence of a baseline. Exit non-zero with a message naming the path.
2. **A non-zero exit from the command fails the ratchet**, independently of the baseline's content. The current implementation discards it.
3. **`PASS` requires all four**: the command exited 0, the baseline was read and non-empty, the current set was computed, and the diff obeys the ratchet rule.
4. **The comment must match the behaviour.** If the guarantee is narrowed, say to what. A comment that promises more than the code delivers is how the next reader stops looking.

## 5. Acceptance criteria

- **AC1** — With an empty baseline and a command exiting 0: non-zero exit, message names the baseline path, no `PASS` on stdout.
- **AC2** — With an empty baseline and a command exiting 9: non-zero exit, no `PASS`. (This is the case that passes today.)
- **AC3** — With a non-empty baseline and a command exiting 9: non-zero exit, no `PASS`. (Already true; asserted so the fix does not regress it.)
- **AC4** — With a non-empty baseline and a command exiting 0 whose output set matches the baseline exactly: `PASS`, exit 0. The happy path must survive the guard.
- **AC5** — Each of AC1–AC4 is a test in the suite, and **each test fails if the guard is removed**. Mutation-verified rather than counted: state in the manifest which mutation each test catches. A test that passes with and without the guard is not evidence.
- **AC6** — The comment at the top of `gate_ratchet.py` is rewritten to state the guarantee that the tests actually enforce, including what remains outside it.
- **AC7** — Every existing caller still passes: `gate_ratchet.py` is invoked from CI for both `bilingual-docs.txt` and, once AID-2026-058 lands, `traceability.txt`. Both must keep working, and neither baseline may become empty as a side effect of this change.

## 6. Scope

**In scope:** `scripts/ci/gate_ratchet.py`, its test module, and the comment inside it.

**Out of scope, explicitly:**

- Not any baseline file's contents. This work item must not shrink or refresh either baseline.
- Not AID-2026-056's predicate. That work item regenerates a baseline; this one makes regeneration safe.
- Not the CI workflow wiring, unless AC7 cannot be met without it — in which case say so in the manifest rather than changing it silently.

## 7. Ordering with respect to AID-2026-056

OD-26 requires this guard to land **before** AID-2026-056's baseline generation is treated as trustworthy evidence:

> 在守卫修复合入并验证前，不得把它的基线生成结果作为可信的 required-check 验收依据。

AID-2026-056 may continue through independent review. What it may not do is close on a regenerated baseline whose emptiness would be invisible.

## 8. What this work item does not claim

- It does not claim the ratchet is otherwise correct. It claims one specific guarantee is false and states the smallest fix.
- It does not claim an empty baseline is always a mistake. It claims an empty baseline cannot be distinguished from a failed run, and that the ratchet must refuse to guess.
- It does not re-open AID-2026-056. That work item's AC7 stands as written; this one makes a different layer true.
