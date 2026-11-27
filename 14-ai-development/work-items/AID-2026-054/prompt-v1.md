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
      last_verification_note: "Every figure in §1 was measured at main 880e6a78 in this session: all 58 files under 13-engineering-decisions were read in full and scored for dual-language headings; the four gap counts (77 / 77 / 11 / 11) came from patching each variant into a throwaway worktree and calling current_bilingual_gaps(); and all 86 accepted side-by-side pairs were enumerated to calibrate the floor."
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

# AID-2026-054 — make Shape 3 root-agnostic and give both bilingual predicates a floor

**Work item:** `AID-2026-054`
**Dispatched by:** owner-proxy session, 2026-11-23
**Ruling:** `14-ai-development/adr/OWNER-DECISION-EMBEDDED-BILINGUAL-001.md` (Approved, 2026-11-23)
**Registers addressed:** `GOV-NC-2026-11-21-EMBEDDED-ROOT-015` §3.2 and §6, `GOV-NC-2026-11-21-PAIRING-RESIDUAL-013` §3.1, §3.2, §3.3
**Measured at:** `main 880e6a7806bdc93bea3c70d01304fa6c29ee385f`

---

## 1. What you are changing

One file: `scripts/check_bilingual_docs.py`. Three changes, all authorised by the ruling above.

### Change 1 — Shape 3 becomes root-agnostic

Current:

```python
if not paired and source.startswith("14-ai-development/"):
    # Shape 3: the root file IS the Chinese source and docs/en holds
    # the English side. It must be earned by actually carrying Chinese.
    paired = english.is_file() and _carries_chinese(source)
```

The ruling's §1 establishes that the root-name scope is not policy. `00-governance/bilingual-documentation-policy.md` §2 includes "technology evaluations, ADRs, engineering decisions" in its scope and never scopes parity by root.

The `english.is_file()` precondition goes with it. Embedded bilingual is a single-file shape; requiring a mirror file in front of it is the contradiction, not the guard. Measured: with the guard removed but the mirror requirement kept, gaps stay at **77** — the guard is not what fails these files.

**Do not** simply delete `english` from the function. It is still used by the mirror shape above. Read the surrounding code before editing.

### Change 2 — the embedded predicate requires both scripts

Current `_carries_chinese()` counts CJK only. Applied root-agnostically, that accepts a Chinese-only document as "bilingual". Add a predicate requiring both scripts in quantity in the same file:

```python
cjk   >= 100     # unchanged from _carries_chinese
latin >= 1000    # letters A-Z / a-z only, not bytes or punctuation
```

`latin` counts ASCII alphabetic characters only (`ch.isascii() and ch.isalpha()`). Do not count full-width Latin, digits, or punctuation — a Chinese document with a lot of English code identifiers should not pass on that alone.

Keep `_carries_chinese()` — it is still used by the mirror shape at line ~380. Add the new predicate beside it.

### Change 3 — the side-by-side predicate gets a floor

Current:

```python
def _side_by_side_bilingual(source: str) -> bool:
    partner = side_by_side_partner(source)
    if partner is None:
        return False
    return _has_any_chinese(source) or _has_any_chinese(partner)
```

Three defects, all measured by register 013:

- **§3.1** — one CJK character anywhere satisfies it. Two English files each containing `一` pass.
- **§3.2** — a zero-byte partner satisfies it, because the `or` is satisfied by the source alone.
- **§3.3** — `side_by_side_partner()` returns the first existing candidate with no symmetry check; with `.md`, `.en.md` and `.zh-CN.md` all present, `partner(partner(x)) ≠ x`, and all three are reported as paired.

Required result:

1. Both files must exist. `partner is None` stays `False`.
2. Neither file may be empty, and the pair must not be the same file twice.
3. The pair must carry **both scripts in quantity**: `cjk >= 100` and `latin >= 1000` across the pair. Where the split falls between the two files is not your concern — a 50/50 split and a 0/100 split are both legitimate, because one side being the translation is the normal case.
4. `side_by_side_partner()` must be symmetric: if it maps `A → B` then it must map `B → A`, or return `None` from both. With three files present, pick deterministically and document which.

**The floor is calibrated, not chosen.** All 86 accepted pairs in the tree have a shorter side of at least 1,364 characters; the 10 shortest run 1,364–2,214. Any floor from 1 to 400 rejects zero of them. 100 is used because `_carries_chinese()` already uses 100 for the same purpose. If your implementation rejects any of the 86, the implementation is wrong, not the floor.

## 2. What must also change, or the gate fails

**The baseline must be regenerated.** After Changes 1–3, `current_bilingual_gaps()` returns **11** entries, not 77. The ratchet treats every one of the 66 missing entries as `resolved` and exits 2 on all of them:

> `Resolved bilingual gap must be removed from scripts/bilingual-baseline.txt`

Regenerate it in the same commit:

```
python scripts/check_bilingual_docs.py --write-baseline
```

Expected: `baseline written: 11 entries`. It refuses to run on a dirty tree — commit or stash first, then regenerate, then commit the result.

The baseline is a shrink-only ratchet. 77 → 11 is a shrink. A regenerated baseline larger than 77 is a failure of this work order, and so is one where `13-engineering-decisions/technology-architecture-blueprint.md` is absent.

## 3. Acceptance

1. `python scripts/check_bilingual_docs.py` exits 0 on a clean tree, and the only baseline diff is 66 removals and 0 additions.
2. `13-engineering-decisions/technology-architecture-blueprint.md` **remains a gap**. It has 0 CJK characters in 49,666 bytes. If it disappears from the baseline, the predicate is wrong.
3. A file containing 100 CJK characters and no Latin letters is **not** accepted as embedded bilingual. A test asserts this.
4. A file containing 1,000 Latin letters and no CJK is **not** accepted. A test asserts this.
5. A pair `X.md` + `X.zh-CN.md` where `X.zh-CN.md` is 0 bytes is **not** accepted. A test asserts this.
6. A pair where both files are English and each contains exactly one `一` is **not** accepted. A test asserts this.
7. `side_by_side_partner()` is symmetric: for every accepted pair `A → B`, `partner(B) == A`. A test asserts this, including the three-file case.
8. The existing 86 accepted pairs still pass. Assert the count, not a sample.
9. `python -m unittest scripts.test_check_bilingual_docs` passes. Note: `scripts/governance/evidence/test_gate_normative_roots.py` already fails 3 tests and errors on 21 at `main` (Windows temp-path assertions); that set must not grow. Do not fix them — they are out of scope.
10. The ruled change is measured, not asserted: state in the commit message the before and after (`77` → `11`) as produced by a run, not by arithmetic.

## 4. Hard constraints

1. **`scripts/check_bilingual_docs.py` and `scripts/bilingual-baseline.txt` only.** No other file. Not the workflow YAML, not the registers, not the ADRs.
2. **Do not raise the floor above 400.** It would start rejecting real pairs. §1 states where the real boundary is.
3. **Do not remove `EMBEDDED_BILINGUAL_SOURCES`.** The ruling keeps all 21 entries. This work order changes the predicate; it does not retire the allowlist.
4. **Do not add `13-engineering-decisions/technology-architecture-blueprint.md` to any allowlist.** Acceptance criterion 2 forbids it, and the ruling's §6 defers that decision to the document owner.
5. **Do not touch the 3 failures and 21 errors in `test_gate_normative_roots.py`.** They are pre-existing and unrelated. If your change alters that count in either direction, stop and report.
6. **Do not modify any register or ADR to make it agree with your implementation.** If implementation contradicts the ruling, say so in the PR body; do not edit the ruling.
7. **Do not run `cargo`.** This work order touches no Rust. Local verification is Python only.

## 5. Why this is not a policy change

The ruling's §1 establishes that no recorded policy decision excludes `13-engineering-decisions` from embedded-bilingual recognition. This work order makes the gate match the policy that exists. If you find a recorded decision that says otherwise, stop: the ruling is wrong and the register needs correcting, not the gate.

## 6. Reporting

In the PR body, state:

- the measured gap count before and after, from a run;
- the baseline diff as `+N / −M`, with both numbers;
- that `technology-architecture-blueprint.md` is still a gap and why;
- whether any of the 86 accepted pairs changed status, and if so which.

Do not claim independent review. A session that writes the predicate cannot supply independence for its own predicate; §9 of register 015 stays `NOT_ASSIGNED`.
