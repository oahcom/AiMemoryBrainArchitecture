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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every figure here is re-measured at main ac0f0dfd in the working checkout, not carried over from the prompt. #910 (150fb45e) is the commit that changed the ground the prompt stands on; the numbers before and after are both stated with the commit they belong to. The 77-path split was produced by reading check_bilingual_docs_full.py's own violation list and counting CJK and latin characters per file; the mirror count by calling counterpart() over all 64 .zh-CN.md paths outside 14-ai-development; the pairing comparison by calling side_by_side_partner() and counterpart() over all 932 tracked Markdown files; the absence of the floor by grepping both scripts for the literal 1000."
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

# AID-2026-056 — ERRATUM-01

**Raised:** 2026-11-24, after this work item was already merged as `5d83b3cd` (#908).
**Measured at:** `ac0f0dfd`.
**Effect on the prompt:** the SHA-256, the base commit and the frozen text are unchanged. Several premises the frozen text asserts are no longer true of the tree, and one acceptance criterion is now impossible to satisfy.

This erratum exists because the work item was written at `d40d4e09` and merged at `5d83b3cd`, and in between `150fb45e` (#910) fixed the very divergence the work item was created to fix. An implementer who reads `prompt-v1.md` without this file will implement work that is already done, and will fail AC6 while believing they caused it.

---

## 1. What changed underneath this work item

`150fb45e fix(858): one authority for GOV-DOC-001 scope, not two divergent copies (#910)` made `check_bilingual_docs_full.py` import `NORMATIVE_ROOTS`, `EMBEDDED_BILINGUAL_SOURCES` and `PAIR_EXEMPT_PREFIXES` from `check_bilingual_docs.py` instead of keeping copies, and added a derived-root guard that exits 2 when the literal and the tree disagree.

Measured at `ac0f0dfd`:

| property | prompt v1 asserts | measured now |
|---|---|---|
| `NORMATIVE_ROOTS` in the full scan | 15, of which 7 do not exist, `08-bmcp-protocol` absent | 9, of which 0 do not exist, `08-bmcp-protocol` present |
| embedded list | 18 entries vs the authority's 21 | imported from the authority, no copy |
| side-by-side pairing outside `14-ai-development` | not recognised | recognised |
| gate B violations | 81 | 77 |
| gate A vs gate B baselines | two divergent sets, 12 apart | byte-identical, 77 = 77 |
| `.zh-CN.md` mirrors asked for a mirror of themselves | 3 of 4 | 0 of 64 |

---

## 2. Corrections to specific statements in `prompt-v1.md`

**(A) §2's split table is wrong by two rows and one total.** The prompt's `A=6, B=66, C=9` summed to 81. The tree now reports 77, and the six A-class paths are no longer violations at all, because #910 taught `counterpart()` to recognise a side-by-side pair under any normative root. Measured split of the current 77:

```
embedded, dropped by the ruling's predicate : 66
real, must stay as debt                   : 11
```

**(B) §2's nine-path C list is incomplete.** Two paths entered it that the old root set could not see, because `08-protocols` does not exist and `08-bmcp-protocol` was never scanned:

```
08-bmcp-protocol/phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md              cjk=72  latin=3341
08-bmcp-protocol/phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md   cjk=4   latin=2603
```

Both are real backlog. Neither is a false positive. The prompt's sentence "the nine are the whole of the real backlog" is now false, and AC1's set equality would reject a correct implementation.

**(C) §3 is resolved and its three paths are no longer violations.** `counterpart()` no longer reaches the `NORMATIVE_ROOTS` branch for a path that is itself a mirror: all 64 `.zh-CN.md` files outside `14-ai-development` now resolve to a sibling, measured `unpaired: 0 of 64`. §4 change 1 is therefore done, and AC3 is satisfied by the tree rather than by any implementer.

**(D) §4 change 3 was not followed, and the risk it names was re-introduced.** The prompt says:

> Reuse `side_by_side_partner()` rather than writing a second pairing implementation — two implementations of "is this paired" is how gate A and gate B came to disagree in the first place.

#910 wrote the pairing inline inside `counterpart()` instead. Measured consequence at `ac0f0dfd`: over 932 tracked Markdown files, "gate A says paired and gate B says violation" occurs **0 times**. So the current behaviour agrees — but by having two implementations that happen to agree today, not by having one. The prompt's stated reason for the constraint was exactly this shape. Recording it as a known deviation with a measured zero, not as a resolved concern.

**(E) §5's first hard constraint is now false and AC6 is unsatisfiable.** The prompt says:

> **`NORMATIVE_ROOTS` stays exactly as it is.** It lists 15 roots, 7 of which do not exist on disk, and it omits `08-bmcp-protocol`, which does. That is `GAP-26` and it is a different work item.

AC6 then requires "`NORMATIVE_ROOTS` is byte-identical to its pre-change value … and the seven non-existent roots are still listed." The pre-change value no longer exists in the tree; the seven roots were removed by #910 and `08-bmcp-protocol` was added. **An implementer obeying AC6 literally would have to reintroduce a defect in order to pass.** AC6 is withdrawn, not deferred.

**(F) §2's control case is still valid.** `13-engineering-decisions/technology-architecture-blueprint.md` is still `cjk=0`, still a violation, still the file a too-permissive predicate would wrongly resolve. AC4 stands unchanged.

---

## 3. What remains actually undone

Measured at `ac0f0dfd`, against the current tree:

1. **The embedded predicate does not exist.** `grep -rn "1000" scripts/check_bilingual_docs.py scripts/check_bilingual_docs_full.py` returns nothing. The full scan still consults `EMBEDDED_BILINGUAL_SOURCES` — a 21-entry allowlist — while the ruling describes a property (`cjk >= 100` and `latin >= 1000` in one file) that 66 of the 77 violating files satisfy and that no code computes. This is the one substantive change left, and it is the reason the work item exists.

2. **The `gates.yml` comment is still wrong.** `.github/workflows/gates.yml:155` still reads `# GOV-DOC-001 full scan: 81 normative paths lack an en/zh-CN counterpart.` The current number is 77 and will be 11 after change 1. §4 change 5 stands.

Everything else in §4 is either already done by #910 (changes 1 and 3) or already true (change 2's side-by-side recognition).

---

## 4. Corrected acceptance criteria

These replace §6. Each is checkable without trusting this file.

- **AC1′** — `python3 scripts/check_bilingual_docs_full.py` reports **11** violations, and the eleven are exactly: the prompt's nine C paths minus nothing, plus the two `08-bmcp-protocol` paths in §2(B). Set equality, not a count.
- **AC2′** — The baseline diff is **66 removals, 0 additions**, and the 66 are exactly the paths for which `cjk >= 100 and latin >= 1000` holds in the current 77.
- **AC3′** — Withdrawn: satisfied by #910. A regression test may assert it, but no implementer action is required.
- **AC4** — unchanged; `technology-architecture-blueprint.md` is still a violation.
- **AC5** — unchanged; both floor boundaries asserted from both sides.
- **AC6′** — Withdrawn. Replaced by two separate assertions:
  - **AC6a** — this work item does not modify `NORMATIVE_ROOTS`. The derived-root guard from #910 still exits 0.
  - **AC6b** — withdrawing AC6 grants **no** authority to change `NORMATIVE_ROOTS`. The pre-#910 value is not restored, and nothing here widens this work item's file scope. Owner ruling OD-22(a): *"撤回错误绑定历史字节值的 AC6，不等于授予修改根目录的权限"*. If the roots need changing, that is a different work item with its own authorisation.

  The distinction matters because both ways of satisfying the old AC6 fail: keeping the pre-change value requires reintroducing seven non-existent roots, and writing the current value into the criterion would freeze another implementation detail as if it were a requirement.
- **AC7** — unchanged in form, new numbers: after change 1 and the baseline regeneration, `gate_ratchet.py` exits 0 with `baseline=11 current=11 regressions=0 fixed=0`.
- **AC8** — enlarged: the suite must also cover the two `08-bmcp-protocol` paths, since they are the only two paths in the set that the pre-#910 code structurally could not observe.
- **AC9** — unchanged; gate A still reports `77 frozen, 0 new gaps`.

---

## 5. Does not change

The prompt's SHA-256, `prompt_status: FROZEN`, the base commit `d40d4e09`, the ruling in `OWNER-DECISION-EMBEDDED-BILINGUAL-001`, the floor values `100`/`1000`, the `technology-architecture-blueprint.md` control, and the instruction not to touch `scripts/check_bilingual_docs.py` or `scripts/bilingual-baseline.txt`.

---

## 6. Why this was not caught before merge

The prompt was written at `d40d4e09`, the branch was opened against it, and #910 landed on `main` while the registration PR was open. The registration PR's own checks were green because it changed no code. This is the same shape as the `aaf6da96` (#892) correction earlier in this session: a measurement is only current relative to a commit, and a frozen prompt is by construction stale the moment anything relevant lands.

The durable fix is not "measure more carefully". It is that a work item whose prompt asserts facts about the tree should carry the commit it asserted them at, and a merged work item should be re-checked against `main` before anyone implements it. This work item carries `base_commit_sha: d40d4e09` — it did name its commit. What was missing is a step that compares that SHA to current `main` at dispatch time. That gap is `GAP-29`, proposed below.

---

## 7. Proposed follow-on

`GAP-29-DISPATCH-TIME-STALENESS-CHECK.md` — a work item in `DISPATCHED` state whose `base_commit_sha` is not an ancestor of current `main`, or is more than N commits behind, should be flagged before an implementer starts. Measured trigger for this instance: `d40d4e09` is 13 commits behind `ac0f0dfd`, of which two touch the files this work item names (`150fb45e` on the scan and its baseline, `70fc01f2` on `gates.yml`).

Registered as a proposal only. Creating the work item is an Owner decision, not this erratum's.
