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
        - "14-ai-development/work-items/AID-2026-345/manifest.yaml"
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Coordinator-local path-line verification, checker execution, unit tests, mutation tests and related repository gates were performed and recorded separately; they are not CI results. This evidence record retains its stated scope and limitations. Independent review and Owner acceptance are not established."
    usage_status: Active
    modification_status: Active-Modified
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
    canonical_scope: "AID-2026-345 evidence record for the documentation and validation carriers addressing Issue #262 AC3, AC4, AC6 and AC8."
    canonical_scope_id: "ai-development/aid-2026-345-evidence-record"
    canonical_scope_keywords:
      - "AID-2026-345"
      - "Issue #262"
      - "evidence record"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# AID-2026-345 Evidence Record

## Baseline

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Commit: `31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`
- Issue: #262
- Scope: AC3, AC4, AC6, AC8 only

## Exact source blobs inspected

| Source | Blob SHA |
|---|---|
| `reviews/architecture/SYS-RISK-001.en.md` | `36aafa19bd944da07e1164f83545375410c27c90` |
| `reviews/architecture/SYS-RISK-001.zh-CN.md` | `b570ea243fff41af1fa4ac61b0ee8ae6da4491be` |
| `reviews/complexity/architecture-complexity-assessment.en.md` | `fe08e712b253a4282dbe5d0877be794f2c6b8b29` |
| `reviews/complexity/architecture-complexity-assessment.zh-CN.md` | `90d77646519459434a5703e49a1098ae7f4b3000` |

## AC3 evidence status

The §4 register contains ten risk rows. All ten now have primary `PATH_LINE` evidence. Five additional evidence pointers are also recorded, for a total of fifteen verified path:line pointers.

- Primary risk-row pointers: 10.
- Additional evidence pointers: 5.
- Total verified pointers: 15.
- Verification result: `total=15`, `ok=15`, `mismatch=0`.
- Risk rows without a supporting line: 0.

### R-09 correction record

R-09 was previously classified as `NO_EVIDENCE_FOUND`. That classification was incorrect and has been corrected to `PATH_LINE`.

The original search record is retained:

- Command: `git grep -n -i -E "RPO|RTO|disaster recovery|restore drill" 31c1e5d83e7dad326dbd4b69d4a8e19534718ff1 -- 01-system-architecture 03-memory-brain 04-memory-compiler 05-memory-runtime 06-memory-context 09-security-governance reviews docs`
- Recorded execution: exit 0, 392 hits, declared 392.

The 392 results are keyword matches, not 392 supporting citations. Subsequent source inspection identified three relevant supporting lines in `01-system-architecture/system-quality-attributes.md`:

- Primary evidence: line 239 — `| QA-03 | OPEN | High | Define RTO/RPO and audit availability requirements for intended deployment modes. |`
- Additional evidence: line 153 — `Availability SLOs and recovery objectives (RTO/RPO) require workload and deployment assumptions; do not invent values at architecture stage.`
- Additional evidence: line 253 — `- **OPEN:** Workload corpus, SLO/RTO/RPO, evaluation labels, and backup erasure semantics.`

R-09 now uses line 239 as its primary `PATH_LINE` and lines 153 and 253 as its two `additional_evidence` pointers. The earlier search command, scope and hit count remain part of the record so that the correction does not erase the original search result or the earlier mistaken classification.

## AC4 evidence status

- Four named dimensions are defined: `change_surface`, `coupling`, `irreversibility` and `concurrency_state`.
- Ten module rows are represented.
- Forty score cells are populated with integers 1–5.
- Ten module-level `path_line`/quote pointers are present.
- Twenty `evidence[*]` pointers are present.
- Total module-level pointers: 30.
- Pointer verification: 30/30 valid; 20 unique path:line locations; no missing paths, out-of-range lines or quote mismatches.
- All ten modules retain exactly the same four-dimensional scores as the previous carrier-data.
- Module A's `evidence_gap` explicitly names `irreversibility`.
- Module B's `evidence_gap` explicitly names `concurrency_state`.
- The four-dimensional judgments remain provisional. Verified source pointers do not by themselves establish Owner acceptance or close the stated evidence gaps.
- Historical eight-number scores are retained and explicitly labelled historical.

## AC6 evidence status

The carrier checker implements twelve rules, R1–R12. The local carrier check passed against the unmutated carrier data, and fifteen unit tests passed.

- Checker: `scripts/ci/aid_2026_345_carrier_validation.py`
- Test file: `tests/session_evidence/test_aid_2026_345_carriers.py`
- Test result: `Ran 15 tests in 0.166s; OK`.
- Checker result: `AID-2026-345 CARRIER CHECK PASS`; `R1-R12: 12/12 structural and source-evidence rules satisfied`.

R11 requires a B-variant `NO_EVIDENCE_FOUND` search to complete successfully and return zero matching lines. A search with matches cannot support that evidence state. The negative test restored the former R-09 `NO_EVIDENCE_FOUND` state while retaining its 392-hit search and correctly failed with `R11_B_VARIANT_REQUIRES_ZERO_HITS`.

R12 requires every module to name each of the four dimensions in either `evidence[*].supports` or `evidence_gap`. The negative test retained module A's otherwise valid `path_line` but omitted `irreversibility` from both locations; it correctly failed with `R12_MODULE_DIMENSION_COVERAGE`.

Four existing mutation cases also failed closed as expected:

- Nonexistent quote: `R10_QUOTE_MATCHES_LINE`, exit 1.
- Out-of-range line number: `R9_LINE_IN_RANGE` and `R10_QUOTE_MATCHES_LINE`, exit 1.
- Nonexistent source path: `R8_PATH_EXISTS`, `R9_LINE_IN_RANGE` and `R10_QUOTE_MATCHES_LINE`, exit 1.
- Truncated quote: `R10_QUOTE_MATCHES_LINE`, exit 1.

These checker, unit-test and mutation results were executed in the coordinator's local worktree. They are not CI results.

## AC8 evidence status

The bilingual review templates pin the four baseline blob SHAs. Reviewer identity, review date, findings and conclusion remain unfilled by design.

- Review templates are present.
- Independent reviewer identity: pending.
- Review conclusion: `TO_BE_FILLED_BY_INDEPENDENT_REVIEWER`.
- Independent review and Owner acceptance are not established.
