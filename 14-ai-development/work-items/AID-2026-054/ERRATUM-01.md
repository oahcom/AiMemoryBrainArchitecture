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
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every figure was produced by a run on 2026-11-24. The pair and file counts were enumerated in-process over `git ls-files` at both 880e6a78 and 5c64e560; the predicate behaviour was measured by patching AID-2026-054 Change 3 into a throwaway worktree and evaluating `_side_by_side_bilingual` on two constructed pairs; the mutation matrix was produced by evaluating the four register/branch configurations in both trees. No figure is carried over from the work order or from register 019."
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

# Erratum 1 for AID-2026-054

- **Raised:** 2026-11-24, by the owner-proxy session that dispatched the work order
- **Applies to:** `14-ai-development/work-items/AID-2026-054/prompt-v1.md` (frozen, SHA-256 `18b12deec0716b5bc20e8400095c89ed125fd514ed333880814001907ee168ae`, 9222 bytes)
- **Does not modify the frozen prompt.** The prompt's hash is the record of what was dispatched. This erratum adds requirements; it does not rewrite them.
- **Measured at:** `880e6a78` (the work order's own `base_commit_sha`) and `5c64e560`

---

## 1. Why this exists

The prompt was frozen before two of its figures and one of its requirements were checked against a number rather than an inference. All three defects were found by measurement on 2026-11-24, after dispatch and before implementation. The work order is `DISPATCHED` and `implementing_ai_session: NOT_ASSIGNED`, so nothing has been built against it yet — which is the only reason an erratum is sufficient and a re-freeze is not needed.

## 2. Defect A — criterion 8 asserts the wrong count

**The prompt says** (§1 Change 3, §3 criterion 8, §4 hard constraint 2, and `notes[0]`):

> All **86 accepted pairs** in the tree have a shorter side of at least 1,364 characters.

**Measured**, by enumerating accepted side-by-side units under `NORMATIVE_ROOTS` at both commits:

| quantity | value at `880e6a78` | value at `5c64e560` |
|---|---|---|
| distinct accepted **pairs** | **43** | **43** |
| accepted **files** (both sides counted) | **86** | **86** |

86 is the file count. There are 43 pairs. Criterion 8 says "Assert the count, not a sample" — an implementer who does exactly that with `86` against a pair count gets `43` and must either fail the criterion or fudge the assertion.

**Amendment.** Criterion 8 reads: *"The 43 existing accepted side-by-side pairs (86 files) still pass. Assert both numbers, and assert them separately: a pair count and a file count that disagree by anything other than a factor of two means the enumeration changed."*

## 3. Defect B — the calibration range is wrong

**The prompt says:**

> the 10 shortest run 1,364–2,214.

**Measured**, shortest side of each accepted pair, sorted ascending:

| rank | shorter side (chars) | pair |
|---|---|---|
| 1 | 1,364 | `14-ai-development/status-migration-map.en.md` |
| 2 | **2,214** | `.../GAP-15-FMT-GATE-ABSENT.zh-CN.md` |
| 3 | 2,302 | `.../GAP-13-PARTICIPANT-ADMISSION-EXTERNAL.zh-CN.md` |
| 4 | 2,648 | `.../GAP-14-PLACEHOLDER-PASSES-VALIDATION.md` |
| 5 | 3,207 | `.../GAP-BASELINE-005.md` |
| 6 | 3,217 | `.../GOV-NC-CONVERGENCE-2026-11-20.en.md` |
| 7 | 3,331 | `.../GAP-BASELINE-003.zh-CN.md` |
| 8 | 3,364 | `.../VERIFICATION-2026-11-22-ROUND11.md` |
| 9 | 3,497 | `.../GAP-12-CANONICAL-COMMIT-UNDEFINED.md` |
| 10 | **4,412** | `14-ai-development/bilingual-tiering-policy.en.md` |

2,214 is the **second** entry. The tenth is 4,412 — twice the stated upper bound.

**This does not weaken the floor.** The minimum is 1,364, which is what the safety argument rests on, and a floor of 100 rejects zero of the 43 pairs. The defect is in the descriptive range only.

**Amendment.** Replace the sentence with: *"The shortest accepted pair has a shorter side of 1,364 characters and the tenth shortest is 4,412; any floor from 1 to 400 rejects zero of the 43 pairs."*

## 4. Defect C — a test that passes for the wrong reason (the load-bearing one)

**The prompt does not mention this at all.** `PARTIAL_SIDE_BY_SIDE_PAIRS` appears zero times in it.

`scripts/governance/evidence/test_gate_normative_roots.py` holds the register's only regression test, at line 659:

```python
def test_partial_side_by_side_pair_rejects_both_sides(self):
    english = "02-domain-model/zz-partial-probe.md"
    chinese = "02-domain-model/zz-partial-probe.zh-CN.md"
    self.write(english, "Complete English specification.\n")
    self.write(chinese, "这是局部中文翻译内容。" * 20 + "\n")
    ...
    gaps = self.inventory_02()
    self.assertIn(english, gaps)
    self.assertIn(chinese, gaps)
```

That English side carries **28 Latin letters**. The floor this work order installs requires **1,000** across the pair. So after Change 3 the pair is rejected by the **predicate**, before `partial_side_by_side` is consulted, and the assertion "both sides are gaps" holds for a reason unrelated to the register.

Measured by evaluating the four `register present/absent × branch present/removed` configurations:

```
today's tree (no floor)          with Change 3 applied (floor)
reg+ branch+  PASS               reg+ branch+  PASS
reg+ branch-  FAIL  <- killed    reg+ branch-  PASS  <- not killed
reg- branch+  FAIL               reg- branch+  PASS
reg- branch-  FAIL               reg- branch-  PASS
```

**2 outcome vectors before, 1 after.** The mutant that deletes the register branch survives the floor.

No existing criterion catches this. Criterion 8 only checks that the accepted pairs still pass. Criterion 9 only forbids the pre-existing 3F/21E count from growing. A test that still passes still counts as a pass.

**Amendment.** Add criterion 11:

> **11.** Deleting the `and not partial_side_by_side` conjunct from `current_bilingual_gaps()` must make at least one test fail. State in the PR body which test fails and paste the failure. If no test fails, the register's only control has become tautological and the change is not acceptable.

And add to §4 hard constraints:

> **8.** Do not weaken the `PARTIAL_SIDE_BY_SIDE_PAIRS` mechanism to make criterion 11 pass. The mechanism stays; the test's fixture must clear the floor so that the register, not the floor, is what rejects the pair.

## 5. A sibling defect this work order is not responsible for

`test_partial_side_by_side_registration_does_not_block_mirrors` (line 676) writes full `docs/en` + `docs/zh-CN` mirrors before asserting that the pair is **not** a gap. `paired = mirrored or (...)` short-circuits on `mirrored`, so the register is never consulted.

Measured: all four configurations give `gap=False`, **in both trees**. That test has never been able to fail. It is out of scope for this work order — recorded so that a reviewer does not read criterion 11 as covering it.

## 6. What this erratum does not change

- The ruling `OWNER-DECISION-EMBEDDED-BILINGUAL-001` is unaffected. Its §6 branch 3 is still true.
- The floor (100 CJK / 1000 Latin) is still correct. Defect B is a wrong description of the margin, not a wrong margin.
- The baseline shrink `77 → 11`, the Shape 3 change, and the symmetry requirement are unchanged.
- Independent review remains `NOT_ASSIGNED`. This erratum was written by the same session that wrote the work order; it corrects the work order's arithmetic, which is the one thing such a session can do without claiming independence.
