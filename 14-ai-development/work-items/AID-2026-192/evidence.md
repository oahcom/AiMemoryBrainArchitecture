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
        - "14-ai-development/work-items/AID-2026-192/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Counts re-derived from the tree at 4326669c by command, not asserted; the AID-2026-111 row inventory was re-tallied from its own cells; the AID-2026-112 provenance claim was compared line by line against AID-2026-111 §2.3. No historical verdict, blob pin or test result was changed or re-run."
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
    canonical_scope: "Corrected counts and provenance for documentation-gaps GAP-03, the AID-2026-111 combined row and the AID-2026-112 memory-context execution fields"
    canonical_scope_id: "ai-development/aid-2026-192-count-and-provenance-correction"
    canonical_scope_keywords:
      - "documentation-gaps"
      - "work-item-arithmetic"
      - "provenance"
      - "not-recorded"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-192/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-192/evidence.md"
---

# AID-2026-192 — Stale counts and an inherited assumption in the governance record

## Scope and attribution

- Repository: `oahcom/AiMemoryBrainArchitecture`; base `main` at
  `4326669caa6c43193d34219a0451b80762b712ff` (the branch was cut here).
- Branch: `fix/2026-11-27-stale-counts-and-claims`.
- Attribution: user-authorized operator (delegated by account owner). No natural-person Owner
  signature, acceptance or approval is asserted, and nothing here closes an Issue.
- This unit edits four documents and their two mirrors, and adds this registration set plus one
  `INDEX.md` row. It changes no code, no workflow, no checker, no registry and no historical
  verdict.

## 1. What was wrong

Three statements were not reproducible from the tree they describe.

| # | Location | Recorded | Reproducible value |
|---|---|---|---|
| 1 | `docs/governance/documentation-gaps.md` GAP-03 | "26 of its files are architecture documents", "`reviews/` (196 Markdown files …)" | 27 and 198 |
| 2 | `AID-2026-111/evidence.md` §1 combined row | 0 PASS / **36** PARTIAL_EVIDENCE / **52** UNCHANGED | 0 / **34** / **54** |
| 3 | `AID-2026-112/evidence.md` §8, memory-context row | Exit `0`, Test binaries `11`, Passed / Failed `177 / 0` | AID-2026-111 §2.3 records exit code, failed count and test-binary count as `NOT_RECORDED` |

Failure 1 is a stale number in a live governance record: the registry entry it describes has
said `documents: 27` for some time, so the prose and the machine-checked claim disagreed. The
review count is a plain measurement and moved by two files.

Failure 2 is an addition error inside one table. Each set row is internally consistent
(23 + 49 = 72, 6 + 2 = 8, 5 + 3 = 8) and their columns sum to 0 / 34 / 54; the combined row
reports 36 / 52, i.e. two rows were moved from UNCHANGED to PARTIAL_EVIDENCE in the total
while no row in §5–§7 moved.

Failure 3 is not an addition error. It is an upgrade: a field another record of the same run
declares `NOT_RECORDED` reappears three times as a value, and a stdout hash appears that the
earlier record says was never captured. The 552 total that depends on it is still the
arithmetic sum of three passed counts, but "0 failed" and "exit 0" for the third group are
unbacked.

## 2. What was changed

### 2.1 `docs/governance/documentation-gaps.md` (GAP-03, one row)

- 26 → **27** architecture documents under `docs/`, with the inline annotation
  `(verified 2026-11-27 against tree 4326669c…)` and the counting rule spelled out: the
  `backlog: docs: documents: 27` claim in `00-governance/document-scope-registry.yaml`,
  reproduced by counting `docs/**/*.md` minus `docs/en`, `docs/zh-CN` and the individually
  governed gap record.
- 196 → **198** Markdown files under `reviews/`, annotated as the recursive count of
  `reviews/**/*.md` on the same tree.
- No other GAP entry, no front matter and no registry value changed. The registry already said
  27; it was not edited.

### 2.2 `AID-2026-111/evidence.md` — appended `## Correction`

The §1 table is untouched: the combined row still reads 0 / 36 / 52 as the recorded value.
The appended section does four things:

1. states the row inventory — **88** verdict-bearing rows (72 Gate A cells, 8 SC, 8 HIR) — and
   records that the "95 rows" figure supplied with the dispatch does not reproduce from the
   body;
2. tabulates the three set rows and their column sums beside the recorded combined row, so the
   discrepancy is visible as arithmetic rather than as a claim;
3. lists **every row's verdict**: the 72 Gate A cells as a 9-checkpoint × 8-flow table with
   per-flow totals (F1 5P/4U, F2 5P/4U, F3 0P/9U, F4 6P/3U, F5 0P/9U, F6 0P/9U, F7 0P/9U,
   F8 7P/2U), then the 8 SC rows (6P/2U) and the 8 HIR rows (5P/3U) individually;
4. concludes **0 PASS / 34 PARTIAL_EVIDENCE / 54 UNCHANGED = 88**, noting that AID-2026-111's
   own `AI-visible output` section already states 34 / 54, so the combined row is the outlier.

### 2.3 `AID-2026-112/evidence.md` — appended `## Provenance correction`

The §8 table, the title and every verdict are untouched. The appended section records:

- AID-2026-111 §2.3, same HEAD `a123ea4e…`, same group: passed 177; failed count and exit code
  `NOT_RECORDED`; command, test-binary count, stdout bytes, raw stdout SHA-256, per-harness
  multiset and test-name inventory `NOT_RECORDED`; normalised digest `NOT_SUPPLIED`;
- no new capture, command log, stdout artifact or hash procedure is cited anywhere for the
  three fields, and the §8 caveat ("operator-supplied, not re-run in this session") describes
  who executed, not where the fields came from;
- `Exit code = 0`, `Failed count = 0`, `Test binaries = 11` are marked
  **`INHERITED_ASSUMPTION`**;
- the row's stdout SHA-256 is unsourced as well, and per AID-2026-111 §2.1 a raw stdout hash
  pins one capture only — without the capture it carries no verification weight;
- what survives: 177 is recorded, 552 = 99 + 276 + 177 remains a valid sum of three passed
  counts, and nothing in the record is claimed to be a misjudgment.

### 2.4 Mirrors

`docs/en/.../AID-2026-111/evidence.md`, `docs/zh-CN/.../AID-2026-111/evidence.md`,
`docs/en/.../AID-2026-112/evidence.md` and `docs/zh-CN/.../AID-2026-112/evidence.md` carry the
same sections, same headings (`## Correction`, `## Provenance correction`) and the same tables,
translated where the mirror is a translation. `docs/governance/documentation-gaps.md` has no
mirror: `docs/governance/` is not a `NORMATIVE_ROOT` and the file is registered individually in
`governed_files`; the GAP-03 row it changes is English-only, so there is no second copy of
those two numbers.

## 3. Reconciliation with main during this PR

While this PR was open, `main` advanced to `0c752ee6` with PR #1340, which appended
**§12 "memory-context capture (2026-11-27)"** to the three AID-2026-111 copies: same HEAD
`a123ea4e…`, same command, exit `0`, 11 test binaries, `177 / 0`, and an explicit statement that
stdout bytes, raw stdout SHA-256, per-harness multiset, normalised digest and the test-name
inventory remain `NOT_RECORDED`.

That changed the truth value of one claim in §2.3 of this record, so the merge was not taken
mechanically:

- §12 corroborates this record's own arithmetic independently — it states 0 PASS, 34
  PARTIAL_EVIDENCE, 54 UNCHANGED — and the appended `## Correction` now says so.
- It does **not** vindicate AID-2026-112's §8 row on its own terms: at the time AID-2026-112 was
  written, no capture existed and none was cited. The three fields were therefore
  `INHERITED_ASSUMPTION` then, and the section now says exactly that, adds §12 as the later,
  separate confirmation, and keeps the row's `43b2b9b6…` stdout hash marked `UNSUPPORTED` —
  because §12 also records that hash as never captured.
- The merge keeps both texts: §12 stands as written by PR #1340, the `## Correction` follows it,
  and neither rewrites the other.

## 4. Verification performed

All commands were run in `D:\code\wt-counts` at the base commit with `PYTHONUTF8=1`.

| Check | Command shape | Result |
|---|---|---|
| Architecture documents under `docs/` | recursive `.md` count, minus `docs/en`, `docs/zh-CN`, the gap record | **27**, equal to the registry claim |
| Review transcripts | recursive `.md` count under `reviews/` | **198** (196 before) |
| AID-2026-111 row inventory | parse rows matching the three section prefixes, tally the bolded verdict | **88** rows → 23/49, 6/2, 5/3 → **0/34/54** |
| Metadata parse | `read_metadata` from `check_document_management` on all seven edited files | `True` for every file |
| Line endings | `python scripts/ci/check_line_endings.py` | 1635 files inspected, **0 violations** |
| Document management | `python scripts/check_document_management.py` | `INCOMPLETE: no rule violations in 501 classified documents, but 446 governed documents are still unclassified` (exit 2) — the documented pre-existing backlog state, see GAP-02; **zero rule violations** |

The DM gate's exit code 2 is the backlog state this repository records in GAP-02 ("that scan now
returns INCOMPLETE (exit 2) while backlog remains"), not a finding against this change.

## 5. What was deliberately not done

- No verdict was changed: all 23/49 + 6/2 + 5/3 cells, all 72 flow cells, and the Gate A
  PARTIAL / OPEN and Gate B PARTIAL / OPEN (NOT VERIFIED) dispositions stand as recorded.
- The AID-2026-111 §1 combined row and the AID-2026-112 §8 table were not rewritten; the record
  of what was written is preserved and the correction is additive.
- No blob pin was altered, and no test, harness or workflow was run to fill the
  `NOT_RECORDED` fields — doing so would create the very evidence whose absence is the point.
- The misplaced §4 table inside the zh-CN mirror of AID-2026-111 is a pre-existing layout
  defect; it was left alone rather than folded into a count-and-provenance change.
- No Issue was closed, no branch protection or check context was touched, and nothing under
  `scripts/`, `tests/` or `.github/` changed.

## 6. Non-claims

- This record does not claim that AID-2026-111 or AID-2026-112 misjudged any predicate; it
  corrects one total and one provenance grade.
- It does not claim that the memory-context run did not pass 177 tests — 177 is recorded — only
  that its exit code, failed count and harness count are not.
- It does not claim that the gate is green: the whole-tree DM scan remains INCOMPLETE by
  design while the backlog exists.
- It does not claim Owner acceptance, independent review, or Issue closure.

## Session role / use case

Documentation repair session for the governance record and two evidence work items. The session
read the two brief files, re-derived the disputed counts from the tree, appended the two
correction sections without editing any verdict, synchronized the mirrors, and registered the
result as AID-2026-192. No runtime, schema, test, workflow or deployment change was made.

## Actual AI input

NOT_RECORDED

The dispatching message was not preserved verbatim. `prompt-v1.md` in this directory is a
structured snapshot of the dispatched task, assembled after the fact, and the manifest records
`prompt_status: NOT_RECORDED` accordingly.

## AI-visible output

Appended `## Correction` to the canonical, EN and ZH-CN copies of AID-2026-111 — 88 rows
enumerated, 0/34/54 established, the recorded 0/36/52 left in place. Appended
`## Provenance correction` to the three copies of AID-2026-112 — Exit code, Failed count and
Test binaries marked `INHERITED_ASSUMPTION`, the unsourced stdout hash noted, 552 retained as a
sum of three passed counts. Corrected GAP-03 from 26/196 to 27/198 with the verification
annotation and tree SHA. Added this registration set and one INDEX row. Reported the local gate
results above, including the pre-existing INCOMPLETE backlog state.
