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
        - "14-ai-development/work-items/AID-2026-191/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Every number below was produced by running the files in this worktree at base 2f4f4118bd2c2d8e43a23975f667deeb06553f3c: the inventory was enumerated by importing the checker and reading each candidate file, the comparator was run before and after the widening, and both unit-test suites and the ratchet were executed locally. No CI result, merge SHA or post-merge blob is claimed."
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
    canonical_scope: "AID-2026-191 designation of scripts/ci/baselines/bilingual-docs.txt as the single authority for the 77-entry frozen bilingual inventory, the widened copy comparator, and the historical annotation of the 81-entry review snapshot"
    canonical_scope_id: "ai-development/aid-2026-191-frozen-inventory-single-authority"
    canonical_scope_keywords:
      - "bilingual"
      - "baseline"
      - "frozen-inventory"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-191/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-191/evidence.md"
---

# AID-2026-191 — one authority for the 77-entry frozen inventory

## 1. What this record claims

The 77-entry frozen bilingual inventory was carried by seven files. AID-2026-172
compared two of them. One copy had already drifted to 81 entries, and nothing in
the tree was red. This record states four things:

1. the measured enumeration of all seven carriers, with line counts and an
   entry-by-entry verdict against the authority;
2. the designation of `scripts/ci/baselines/bilingual-docs.txt` as the single
   authority;
3. the widened `check_baseline_copies_agree()`, which now covers every copy by
   declared role and fails closed on an undeclared one;
4. the historical annotation of the drifted 81-entry snapshot and the two guide
   passages that quoted `baseline=81`.

It does not claim that the 77 gaps are acceptable, that any gate result was
obtained in CI, or that the branch was merged.

## 2. The seven carriers, measured

Enumerated by reading every tracked file with
`inventory_entries_in()` — bare path lines, numbered table rows, quoted JSON-string
lines and bulleted items — and keeping every file that holds at least half of the
77 authority entries. Exactly seven files reach that threshold.

| # | Path | Lines | Inventory rows | Role | Verdict against the authority |
|---|---|---:|---:|---|---|
| 1 | `scripts/ci/baselines/bilingual-docs.txt` | 77 | 77 | authority | identical to itself; the only gate input |
| 2 | `scripts/bilingual-baseline.txt` | 80 | 77 | live | identical entry set (77/77, 0 either way) |
| 3 | `14-ai-development/governance-register/evidence/main-paths.json` | 805 | 803 | superset register | contains all 77; the other 726 rows are not inventory entries |
| 4 | `00-governance/reports/gov-doc-001-full-scan-2026-11-20.md` | 96 | 83 | dated snapshot | 72 shared, 11 extra, 5 absent — the 83-finding scan at `568b847c` |
| 5 | `reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md` | 737 | 81 in the classification table | historical | 73 shared, 8 extra, 4 absent |
| 6 | `reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md` | 737 | 81 in the classification table | historical | identical drift to #5 |
| 7 | `14-ai-development/work-items/FIX-2026-P1-T3/tier-confirmation-proposal.yaml` | 2452 | 0 | prose only | mentions 62 of the 77 in prose; no list block, so it is not a copy |

Measured before the two annotations below: files 5 and 6 were 735 lines each and
carried no marker; the table rows and entries themselves were not touched.

The premise "多 9 / 缺 5" does not reproduce. Against the authority, the 81-entry
table holds **8** entries the authority does not and omits **4** that it holds:
73 + 8 = 81 = 77 − 4. The arithmetic of the premise is consistent; the two
operands are not, and the measured pair is what this record uses.

## 3. The single authority

`scripts/ci/baselines/bilingual-docs.txt`, 77 lines, 77 entries, is the authority
because it is the file the `bilingual` job in `.github/workflows/gates.yml` feeds
to `scripts/ci/gate_ratchet.py`. A file that no gate reads cannot be the definition
of what a gate permits. `scripts/bilingual-baseline.txt` remains a gate input of
`check_bilingual_docs.py`, so it is a live copy that must equal the authority, not
a second definition.

## 4. The widened comparator

`check_baseline_copies_agree()` now reads a declared registry,
`BASELINE_COPIES`, and applies one rule per role:

| Role | Rule | Failure |
|---|---|---|
| `authority` | is the authority | — |
| `live` | entry set equals the authority | one `::error::` per entry, both directions |
| `superset` | contains every authority entry | one `::error::` per missing entry |
| `snapshot` | declares the 40-hex source revision it was taken at | `::error::` when the declaration is gone |
| `historical` | carries `HISTORICAL — not a gate input` | `::error::` when the marker is gone; measured drift is a `::notice::` |

Beyond the declared set, a discovery step walks `git ls-files` and flags any other
tracked file that carries at least half of the authority's entries: unmarked, it is
a `::error::`; marked, it is a notice. A declared copy that is absent from the tree
is skipped — a file that does not exist cannot disagree with anything, which is
also what keeps the check usable on fixture trees that hold only the two baselines.

Measured, with the files at this head:

```
before widening: check_baseline_copies_agree() -> 0 errors, 0 notices   (2 copies compared)
after  widening: check_baseline_copies_agree() -> 0 errors, 2 notices   (6 copies compared + discovery)
```

The two notices are the historical snapshots, and they report what the annotation
states: the review snapshot lists 27 inventory-shaped entries file-wide that the
authority does not have, and 4 authority entries appear nowhere in it. They are
notices because a marked snapshot is not a gate input; the moment either marker is
removed the same function returns `::error::`.

## 5. The drifted snapshot and the 81 references

Content was not changed. `BMCP-ARCH-001.en.md` and `.zh-CN.md` each received a
heading prefix and a one-line blockquote:

```
### HISTORICAL — not a gate input: path-by-path classification of the 81 frozen GOV-DOC-001 findings
```

The table beneath it is byte-for-byte what it was; both files went from 735 to 737
lines. `00-governance/reports/gov-doc-001-full-scan-2026-11-20.md` was **not**
edited: it already declares `Source revision / 扫描源 Commit` with the 40-hex
revision, which is what the `snapshot` rule requires, and editing it would have
forced a bilingual exception it does not need.

`14-ai-development/ci-gates-and-ratchets.en.md` and `.zh-CN.md` were updated in
three places each: the baselines table now names the single authority and says that
`81` is the historical review-snapshot count, and the two measured rows
(`baseline=81 current=81`, `81 uncovered paths`) now carry the date those numbers
belong to. The numbers themselves are left as measured; they are a 2026-11-22
transcript and rewriting them would falsify the record.

## 6. Tests

`scripts/test_check_bilingual_docs.py` gained `BaselineCopyRegistryTests` (10 cases):

| Case | What it pins |
|---|---|
| `test_registry_declares_every_role` | exactly one `authority`, and it is the ratchet baseline |
| `test_all_declared_copies_agreeing_passes` | all roles consistent → `[]`, no `::error::` |
| `test_historical_snapshot_without_marker_fails` | the drifted file is red until it is marked |
| `test_historical_snapshot_drift_is_a_notice_not_an_error` | marked + drifted → `[]` and a notice |
| `test_register_missing_a_frozen_entry_fails` | the register must contain every entry |
| `test_snapshot_without_revision_declaration_fails` | a scan record without its revision is red |
| `test_undeclared_copy_of_the_inventory_fails` | a new copy nobody declared is red even when it mostly agrees |
| `test_marked_undeclared_snapshot_is_a_notice` | marked → notice, not error |
| `test_this_repository_has_no_undeclared_inventory_copy` | the declared set is the whole set at this head |
| `test_entry_shapes_are_read_from_every_copy_format` | all four entry shapes are read |

```
python -m unittest discover -s scripts -p "test_check_bilingual*"   -> Ran 25 tests, OK   (was 15)
python -m unittest discover -s tests   -p "test_check_bilingual*"   -> Ran 7 tests, OK
```

## 7. Local gate runs

```
python scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/bilingual-docs.txt \
  --format paths --command "python scripts/check_bilingual_docs_full.py"
  -> ratchet: baseline=77 current=77 regressions=0 fixed=0
  -> ratchet: PASS - failure set matches the baseline exactly.          exit 0

python scripts/check_bilingual_docs_full.py
  -> 77 violations                                                        exit 1

python scripts/check_bilingual_docs.py   (BASE_SHA=origin/main HEAD_SHA=PR head)
  -> bilingual baseline: 77 frozen, 0 new gaps
  -> PASS                                                               exit 0
```

## 8. What was not done

- No entry of any copy was added, removed or reordered. The authority and the live
  copy are byte-identical to their state at `4326669c`; the two review snapshots
  changed only in the two lines named in §5.
- Neither baseline was regenerated, and `current_bilingual_gaps()` is unchanged.
- `00-governance/reports/gov-doc-001-full-scan-2026-11-20.md` and
  `main-paths.json` were not edited.
- No workflow, branch-protection setting, required context or Issue was touched.
- No CI result, merge SHA or post-merge blob digest is claimed here.
