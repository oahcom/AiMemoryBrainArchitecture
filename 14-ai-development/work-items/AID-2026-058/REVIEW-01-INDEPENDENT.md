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
      last_verified_date: "2026-11-24"
      last_verification_note: "Every figure below was re-measured by the author of the manifest after the review was returned, at main 8e489ec1. The reviewer's reproduction of #926's degraded output was independently confirmed: the script at 1259f1af prints FAIL with 1 error and exits 1, not INCOMPLETE with 0 errors and exit 2. The two error-classification rows and the four baseline paths were checked by running the checker and grepping INDEX.md, not by reading the prompt."
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

# AID-2026-058 — Independent review, session-level (OD-25)

**Status:** `COMPLETED` / `REQUEST-CHANGES` / `PRE-DISPATCH`
**Independence basis:** `PR-GOVERNANCE-001` §5 as amended by `2eb4e352` (#935).
**Reviewing session:** newly opened, no share of the authoring context, conclusions reached from the repository and from commands it ran itself.
**Disclosure:** same GitHub identity as the author (`collaborators = 1`). Independence is session-level only — weaker than human review, weaker than a different model family. Disclosed, not waived.

---

## 1. Verdict

**`REQUEST-CHANGES`.** Not dispatchable.

The work item's central claim — the four errors that justify the whole exercise — is **already false at `8e489ec1`**, and its central piece of evidence (what `#926` prints) is **attributed to the wrong commit**.

---

## 2. Blocking findings

### B1 — AC1 requires four errors that no longer exist

| | |
|---|---|
| Location | `prompt-v1.md:82` (AC1) |
| Claim | "On a clean checkout of the merged result, `python scripts/check_traceability.py` exits 1 with `4 errors` and the four errors are exactly `AID-2026-023`…`026` not appearing in `INDEX.md`." |
| Measured | `PASS TRACEABILITY: 4 requirements / 35 work items / 0 errors / 45 warnings`, **exit 0**. All four AIDs are in `INDEX.md` (lines 82–85). |
| Difference | The four defects were fixed by a later commit. AC1 does not describe a state the implementer should reach; it describes a state that must **not** exist. Satisfying it would require removing four INDEX rows — i.e. re-breaking four work items so a checker can report them. |

This is the same shape as AID-2026-056's AC6: a criterion bound to a snapshot of a defect. It is the second time in this batch, which makes it a pattern rather than an accident.

### B2 — AC3 and AC4 cannot both hold

| | |
|---|---|
| Location | `prompt-v1.md:84` (AC3), `:85` (AC4), `manifest` `baseline_content_change: NOT_GRANTED` |
| Claim | AC3: ratchet `regressions=0 fixed=0`, exit 0. AC4: baseline byte-unchanged, `fixed=0`. |
| Measured | `baseline=4 current=0 regressions=0 fixed=4`, exit 1, `FAIL - lower the baseline by 4 fixed item(s).` |
| Difference | The four baseline entries stopped failing. A shrink-only ratchet reports that as **stale** and fails by design — `fixed > 0` is itself a failure signal. To get `fixed=0` the implementer must either empty the baseline (forbidden by AC4 and by `baseline_content_change: NOT_GRANTED`) or make the four paths fail again (forbidden by B1's own logic). **Three criteria, two of them mutually exclusive and the third requiring a defect.** |

### B3 — the evidence for (B) is attributed to the wrong commit

| | |
|---|---|
| Location | `prompt-v1.md` §1, `manifest` `findings[F3]` |
| Claim | "Measured at `1259f1af` … `INCOMPLETE TRACEABILITY: 0 requirements / 0 work items / 0 errors / 1 warnings`, `$? = 2`", and that `#926`'s commit message describes intent rather than behaviour. |
| Measured | At `1259f1af`: stdout `ERROR required registry unavailable: …`, stderr `FAIL TRACEABILITY: 0 requirements / 0 work items / 1 errors / 0 warnings`, **exit 1**. The `INCOMPLETE`/`0 errors`/`exit 2` output belongs to `a23e6cc0` (#899), the **parent**. |
| Difference | `#926`'s commit message is accurate. The finding that accused it of inaccuracy is based on an unreproducible measurement of the wrong revision. |

The work item's premise survives — the verdict-shaped line is still printed — but the numeric evidence for it does not. An implementer told to hunt an `INCOMPLETE` line will not find one.

### B4 — AC5 contradicts AC2

| | |
|---|---|
| Location | `prompt-v1.md:86` (AC5) vs `:83` (AC2) |
| Claim | AC5: "the existing suite passes **unmodified** except where AC2 requires a new case." |
| Measured | `scripts/test_check_traceability.py:507-515`, test `test_missing_registry_is_fail_not_zero_error_incomplete`, asserts the output **must contain** `"FAIL TRACEABILITY: 0 requirements / 0 work items / 1 errors"`. AC2 forbids `FAIL`, `0 requirements` and `0 work items`. |
| Difference | Satisfying AC2 requires **modifying** that existing assertion, not adding a case beside it. AC5's "unmodified" is false the moment AC2 is met. |

---

## 3. Material findings

### M1 — AC2's forbidden-string list is too wide and too narrow at once

It greps for `PASS`, `FAIL`, `INCOMPLETE`, `0 requirements`, `0 work items`, `0 errors` as substrings. `FAIL` matches `FAILED TO READ`, `PASS` matches `PASSED THE DIAGNOSTIC` — legitimate diagnostic text would be judged a violation. Conversely the list does **not** include `TRACEABILITY:`, so a line shaped `INCOMPLETE TRACEABILITY: …` is caught only by the `INCOMPLETE` token, and a line shaped `TRACEABILITY: cannot read registry` would pass the grep while still being a verdict-shaped summary.

### M2 — the baseline file uses CRLF in an LF repository

`scripts/ci/baselines/traceability.txt` ends every line with `^M$`. AC4 demands "byte-identical", which would freeze that difference in place. Every other baseline in `scripts/ci/baselines/` is LF.

### M3 — `base_commit_sha` is 70 commits behind, and the two commits that matter are exactly the ones that falsify AC1

`b3a65e54..8e489ec1` = 70. `35f2b078` added the four INDEX rows that B1 is about; `f640ba50` changed the checker's error classification that B3 is about. Both landed after the work item's base. The work item is not merely stale — it is stale in precisely the two places its criteria depend on.

### M4 — the two files this work item exists to commit are still untracked

`git cat-file -e origin/main:00-governance/requirements-registry.yaml` → 128 (absent). Same for `scripts/ci/baselines/traceability.txt`. Both exist only as untracked files in one working tree. **This part of the premise is intact** and remains the work item's real reason to exist.

---

## 4. Passed

- **Authorisation is explicit and correct.** `implementation_write: NOT_GRANTED`, `baseline_content_change: NOT_GRANTED`, `gate_behaviour_change: DECIDED by OD-23, PARTIALLY IMPLEMENTED by #926`. The work item does not treat a ruling as a commit.
- **The ordering argument holds.** (B) before (A) is right: committing the inputs without changing the failure path leaves the misleading line in place, and it returns the moment the registry is unreadable again.
- **AC6 is enforceable.** Exit code in `{1,2}`, never 0 — measured exit 1 under the AC2 condition, so this one is already true and is a regression guard.
- **Identity, uniqueness and hashes are correct.** One INDEX row; `prompt_sha256 62fb366b…` and 8328 bytes match the file.

---

## 5. What this review does not do

- It does not modify any file.
- It does not approve. `review.status` is `CHANGES_REQUESTED`.
- It does not resolve B2 by picking a side. Whether AC3 or AC4 gives way is the author's call, and the call has to be visible in the manifest rather than left to the implementer.
