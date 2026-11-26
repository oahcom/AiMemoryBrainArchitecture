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
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-198/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Every number below was produced on 2026-11-27 in this worktree at base 4326669caa6c43193d34219a0451b80762b712ff by importing scripts/check_bilingual_docs.py and calling current_bilingual_gaps(), by running the two test suites named in section 7, and by running a two-fixture probe against a throwaway git repository. No CI result, gate verdict or merge outcome is claimed that was not produced locally; the CJK/latin counts are character counts, not translation quality."
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
    canonical_status: Canonical
    canonical_scope: "AID-2026-198 measurement and repair of the side-by-side bilingual predicate, whose 'either file carries one CJK character' test let an English source certify an untranslated partner"
    canonical_scope_id: "ai-development/aid-2026-198-side-by-side-cjk-designated-side"
    canonical_scope_keywords:
      - "bilingual"
      - "side-by-side"
      - "cjk-predicate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-198/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-198/evidence.md"
---

# AID-2026-198 — One CJK character on the English side certified a pair that was never translated

**Status: DRAFT — measured, then repaired.** The dispatch was "measure first, decide second": change
the predicate, count the damage, and implement only if the new gaps are three or fewer. The
measurement below found that the literal reading of the instruction ("the partner must contain
Chinese") produces twelve new gaps, and that all twelve are false positives caused by the
predicate being direction-blind. The rule that was implemented instead — only the
Chinese-designated file of a pair may certify the pair — produces **zero** new gaps.

## 1. The defect

`_side_by_side_bilingual()` in `scripts/check_bilingual_docs.py` accepted a pair when either file
carried one CJK character:

```python
return _has_any_chinese(source) or _has_any_chinese(partner)
```

`source` is whichever file the scan reached first, which for a `.zh-CN.md` file is the Chinese
file and for a `.md` file is the English one. So an English source with two CJK characters in
passing, plus a `.zh-CN.md` member that is a verbatim English copy, was a "bilingual pair". The
English side was allowed to vouch for the pair; the file that was supposed to hold the
translation was never read.

`test_issue_469_short_translation_is_accepted` (formerly at
`scripts/governance/evidence/test_gate_normative_roots.py:649`) pinned the *shape* of that test —
short is enough — but not the leak: its `.zh-CN.md` fixture does contain Chinese, so it passes
under either reading. The leak was untested, not locked.

## 2. Measurement 1 — the literal rule: the partner must contain Chinese

The rule was implemented as written and `current_bilingual_gaps()` was run over the committed
tree:

| | |
|---|---|
| Gaps before | **77** |
| Gaps after | **89** |
| New gaps | **12** |
| Resolved | **0** |

Twelve is more than three, so this reading would be `DEFERRED_TO_OWNER` by the dispatch's own
threshold. The twelve new gaps, each with its designated Chinese file and the partner the literal
rule demands Chinese from:

| # | New gap (flagged side) | cjk | latin | ratio | Its partner | cjk | latin | ratio |
|---:|---|---:|---:|---:|---|---:|---:|---:|
| 1 | `02-domain-model/phase-2-domain-extension.zh-CN.md` | 5135 | 9172 | 0.5599 | `02-domain-model/phase-2-domain-extension.md` | 0 | 26074 | 0.0 |
| 2 | `07-agent-integration/adapter-capability-tiers.zh-CN.md` | 3168 | 2916 | 1.0864 | `07-agent-integration/adapter-capability-tiers.md` | 0 | 11640 | 0.0 |
| 3 | `08-bmcp-protocol/protocol-index.zh-CN.md` | 2052 | 9606 | 0.2136 | `08-bmcp-protocol/protocol-index.md` | 0 | 16524 | 0.0 |
| 4 | `08-bmcp-protocol/schema-nonempty-audit.zh-CN.md` | 260510 | 485305 | 0.5368 | `08-bmcp-protocol/schema-nonempty-audit.md` | 0 | 1317582 | 0.0 |
| 5 | `14-ai-development/PR-MERGE-EVIDENCE-SUMMARY-001.zh-CN.md` | 1536 | 4767 | 0.3222 | `14-ai-development/PR-MERGE-EVIDENCE-SUMMARY-001.en.md` | 0 | 10205 | 0.0 |
| 6 | `14-ai-development/bilingual-tiering-policy.md` | 2298 | 890 | 2.5820 | `14-ai-development/bilingual-tiering-policy.en.md` | 0 | 9078 | 0.0 |
| 7 | `14-ai-development/ci-gates-and-ratchets.zh-CN.md` | 5461 | 7037 | 0.7760 | `14-ai-development/ci-gates-and-ratchets.en.md` | 0 | 22268 | 0.0 |
| 8 | `14-ai-development/evidence-tiering-policy.md` | 2206 | 3822 | 0.5772 | `14-ai-development/evidence-tiering-policy.en.md` | 0 | 11331 | 0.0 |
| 9 | `14-ai-development/governance-register/GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004.md` | 3139 | 4982 | 0.6301 | `…/GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004.en.md` | 0 | 13368 | 0.0 |
| 10 | `14-ai-development/governance-register/GOV-NC-CONVERGENCE-2026-11-20.md` | 1196 | 717 | 1.6681 | `…/GOV-NC-CONVERGENCE-2026-11-20.en.md` | 0 | 4735 | 0.0 |
| 11 | `14-ai-development/governance-register/README.md` | 1228 | 2739 | 0.4483 | `14-ai-development/governance-register/README.en.md` | 0 | 6937 | 0.0 |
| 12 | `14-ai-development/status-migration-map.zh-CN.md` | 490 | 519 | 0.9441 | `14-ai-development/status-migration-map.en.md` | 0 | 2126 | 0.0 |

Every one of the twelve is a pair in which the Chinese document is the real one and the partner is
the English rendering: the Chinese side carries 490 to 260,510 CJK characters, the partner carries
zero. The literal rule calls all twelve unpaired because `side_by_side_partner()` is symmetric —
`side_by_side_partner("X.md")` returns `X.zh-CN.md`, and `side_by_side_partner("X.zh-CN.md")`
returns `X.md`. A rule phrased as "the partner must contain Chinese" therefore demands Chinese
from the *English* file whenever the scan reaches the Chinese file first. The twelve gaps are
artefacts of the phrasing, not untranslated pairs, and adopting them would also be refused by the
baseline itself: `--write-baseline` only shrinks and would report twelve entries to add.

## 3. Measurement 2 — the designated-side rule

Rule implemented: of a pair, the file that is designated to hold the Chinese text must carry at
least one CJK character. Designation is unambiguous because it is a naming convention:
`.zh-CN.md` wherever it appears; otherwise the plain root `.md` (Shape 3, where the root document
is the Chinese original and the `.en.md` sibling is the English rendering). The English side never
counts.

| | |
|---|---|
| Gaps before | **77** |
| Gaps after | **77** |
| New gaps | **0** |
| Resolved | **0** |

Both frozen baselines are therefore unchanged, and the shrink-only write is not needed: no entry is
added and no entry is removed. `scripts/bilingual-baseline.txt` and
`scripts/ci/baselines/bilingual-docs.txt` are untouched by this change.

## 4. Why the leak was latent

Over the committed tree, `side_by_side_partner()` resolves **103** pairs. Of those:

- **26** carry Chinese on both sides;
- **76** carry Chinese only on the designated Chinese side (English source, Chinese partner — the
  normal shape);
- **1** carries Chinese on neither side, and is paired through its `docs/en` + `docs/zh-CN`
  mirror rather than through this predicate;
- **0** are accepted only through the English side.

Zero is the reason the repair costs nothing: no pair in the tree today is being certified by the
branch that was removed, so tightening the predicate cannot move an entry into the gap set.
Register 013 §3.1 already measured that the leak was reachable; this measurement adds that it is
unoccupied.

## 5. Two-fixture proof, before and after

A throwaway git repository holding `02-domain-model/` with one CJK-bearing English source and
one English `.zh-CN.md` copy, plus one genuine short translation, was scanned with
`current_bilingual_gaps()` at both revisions:

| Fixture | Before the change | After the change |
|---|---|---|
| `zz-stray.md` = `English source naming 方案 and 编排 in passing.`, `zz-stray.zh-CN.md` = `English source naming the plan and the orchestration in passing.` | pair accepted; neither side in the gap set | pair rejected; **both** sides in the gap set |
| `zz-short.md` = `English source.`, `zz-short.zh-CN.md` = `中文翻译。` | pair accepted | pair accepted (unchanged) |

The second row is the #469 obligation: brevity is still not punished, because the floor remains one
CJK character on the designated side.

## 6. What changed, and what deliberately did not

Changed:

- `scripts/check_bilingual_docs.py` — one new helper `_chinese_side(source, partner)` names the
  designated file; `_side_by_side_bilingual()` reads that file and nothing else. The
  `_has_any_chinese()` helper, its one-character threshold, `_carries_chinese()` and its
  100-character threshold, `PARTIAL_SIDE_BY_SIDE_PAIRS` and the mirror branch are all unchanged.
- `scripts/governance/evidence/test_gate_normative_roots.py` — `test_issue_469_short_translation_is_accepted`
  is renamed to the rule it actually tests, `test_short_translation_on_the_chinese_side_is_accepted`,
  and two regression tests are added: `test_stray_cjk_in_english_source_does_not_vouch_for_the_pair`
  and `test_english_copy_without_cjk_under_zh_cn_name_is_rejected`. Test count 52 → 54.

Not done, on purpose:

- No mirror deleted, no translation written: the twelve files of section 2 and the 77 baseline
  entries are untouched.
- The 100-character threshold of `_carries_chinese()` was not moved, and the side-by-side floor
  stays at one CJK character.
- No baseline entry added, removed or reordered; no required check context, workflow or branch
  protection touched.
- No Issue closed.

## 7. Test evidence

Both suites were run at this head in this worktree with `PYTHONUTF8=1`:

| Command | Result |
|---|---|
| `python -m unittest scripts.governance.evidence.test_gate_normative_roots` | `Ran 54 tests … OK`, exit 0 |
| `python -m unittest discover -s scripts -p "test_check_bilingual*"` | `Ran 15 tests … OK`, exit 0 |

The CI job `GOV-DOC-001 structural checks` runs both of these before the gate itself, so the two
commands are the same ones the required context executes.

## 8. `DEFERRED_TO_OWNER`

- **D1 — the one-character floor itself.** Register 013 §3.2 and
  `OWNER-DECISION-EMBEDDED-BILINGUAL-001.md` §4 ask for a 100-character floor on the shorter side of
  a pair. Measured cost of applying the existing `_carries_chinese()` 100-CJK threshold to the
  designated side instead of one character: gaps 77 → 77, new 0, resolved 0 — the same zero as
  section 3. It was **not** adopted here because this unit was explicitly told not to change that
  threshold, and the floor is `AID-2026-054`'s scope. The overlap is real: whoever lands 054 will
  rewrite the same function, and the two changes are independent but adjacent.
- **D2 — the mirror branch is still structural only.** `mirrored` counts `docs/en/X` +
  `docs/zh-CN/X` as paired without reading either file, so a `docs/zh-CN` path can hold English and
  still pass. One live example, measured and not repaired:
  `docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md`
  carries 0 CJK and 1,073 latin characters; it passes because its `docs/zh-CN` siblings exist, not
  because anything is translated. Closing that branch is a different predicate with a different
  cost than the 77-entry baseline, and it was not in this unit's scope.

Merging this change proves repository integration only. No Owner acceptance, independent review or
translation adequacy is asserted here.
