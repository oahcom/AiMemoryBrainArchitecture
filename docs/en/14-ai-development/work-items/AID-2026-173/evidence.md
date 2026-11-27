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
        - "14-ai-development/work-items/AID-2026-173/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every row was read from the committed checker sources at base f0d881a88f0f70d45e2c67e22fc372a95198c991; the inventory records thresholds that exist and does not claim any gate was executed or that the list is exhaustive beyond the searched files."
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
    canonical_scope: "AID-2026-173 inventory of hardcoded gate thresholds, their definitions and their verbatim violation text"
    canonical_scope_id: "ai-development/aid-2026-173-hidden-gate-threshold-inventory"
    canonical_scope_keywords:
      - gate-thresholds
      - governance-gates
      - bilingual-baseline
      - session-evidence
      - document-metadata
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-173/evidence.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-173/evidence.md"
---

# AID-2026-173 — Hardcoded gate thresholds: an inventory

**Status: DRAFT — record only.** This work item changes no checker logic, no threshold, no workflow and no registry value. Every row was read from the committed sources at `f0d881a88f0f70d45e2c67e22fc372a95198c991`. The document records what is there; it is not a proposal to change it.

## 1. Why this record exists

Several gates in this repository carry numbers that are invisible until a documentation change trips them. The failure text usually names the path that broke, rarely names the number, and never says which other files must move with the same change. A new last-mile worker therefore loses a check cycle to a constant it had no way to see. This inventory makes the numbers explicit, and it is deliberately separate from any ruling about whether a given number is right.

## 2. Method and scope

Searched at `f0d881a88f0f70d45e2c67e22fc372a95198c991`: `scripts/**/*.py` excluding test modules and `__pycache__`, `.github/workflows/*.yml`, `00-governance/*.yaml`. The sources were first read at `8722a37b0cd72dc550d99c0eaebe9e7556ce2f95`; the ten files under those three paths that changed between `8722a37b0cd72dc550d99c0eaebe9e7556ce2f95` and `f0d881a88f0f70d45e2c67e22fc372a95198c991` were re-read here, and one of them moved a number this record carries (NORMATIVE_ROOTS grew from 12 to 13, row A2). Patterns: `>= \d+`, `<= \d+`, `== \d+`, `!= \d+`, named constants (`MAX`/`MIN`/`LIMIT`/`THRESHOLD`), `len(...)` comparisons, exact-set and exact-count equality, closed enumerations, date constants, and the messages each checker prints. Test modules were read only to bind numbers a test asserts (row B8).

Not searched: `crates/**/*.rs`, `tests/**`, `tools/**`, `experiments/**`, third-party fixtures. A threshold that lives only there is outside this record.

Counts: **56 thresholds — 51 BLOCKING, 2 ADVISORY, 3 SILENT.**

- **BLOCKING** — the required CI context goes red, or the gate exits non-zero, when the threshold is crossed.
- **ADVISORY** — only a notice is printed, or only a log line is shortened.
- **SILENT** — nothing is printed against the number itself: a file stops being read, a pairing silently flips to false, or a job is cancelled before any check speaks.

## 3. Inventory

### A. Document scope registry (GOV-DOC-002, DM-14)

| # | Threshold | Defined at | What change trips it | Violation text (verbatim) | Class |
| --- | --- | --- | --- | --- | --- |
| A1 | `docs` backlog count = 27, exact equality with the tree | check_document_management.py:2077-2087; 00-governance/document-scope-registry.yaml:83 | Adding or removing one .md under `docs/` outside docs/en, docs/zh-CN and the individually governed gap record | DM-14 backlog 'docs' declares 27 documents but N are on disk; update the registry | BLOCKING |
| A2 | registry `governed:` list == NORMATIVE_ROOTS (13 roots), set equality | check_document_management.py:1990-1998; check_bilingual_docs.py:19-24 | Declaring a governed root in one list only | DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [...], enforced-only [...] | BLOCKING |
| A3 | Every top-level directory must be governed, backlog or excluded (4 structural exceptions) | check_document_management.py:2000-2034; STRUCTURAL_EXCEPTIONS at :83 | Any new top-level directory: node_modules, dist, out, build, tmp, .venv | DM-14 top-level directories not accounted for: [...]. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason | BLOCKING |
| A4 | registry_version == "2" and schema_version == "2" | check_document_management.py:76,80,1914-1920,716-721 | Bumping the registry or the metadata schema without bumping the gate constant | DM-14 ... declares registry_version 'X' but this gate implements '2' (schema side: SystemExit) | BLOCKING |
| A5 | Backlog prose may state no document count, in digits or words, English or Chinese | check_document_management.py:1642-1658,1959-1966 | Writing '27 documents' or 'twenty-seven docs' inside `reason`/`reason_zh` | DM-14 backlog 'docs' reason restates a document count [...]; `documents:` is the only place a count may be stated | BLOCKING |
| A6 | governed_files == exactly 1 path, set equality with the gate constant | check_document_management.py:56,2055-2069 | Individually governing a file, or deleting docs/governance/documentation-gaps.md | DM-14 governed_files disagrees with the gate; registry-only [...], gate-only [...] | BLOCKING |
| A7 | docs/en and docs/zh-CN must exist as real directories | check_document_management.py:2041-2053 | Deleting a mirror root, or replacing it with a symlink | DM-14 bilingual mirror directory docs/en is missing (or: is a symbolic link) | BLOCKING |
| A8 | Exclusion kind closed set {not-documentation}; reason and reason_zh both required | check_document_management.py:67,1968-1981 | Adding an excluded directory with kind: not-yet-migrated, or with an English-only reason | DM-14 excluded 'x' must declare kind one of ['not-documentation'], got 'not-yet-migrated' | BLOCKING |

### B. Bilingual documentation and prompt library (GOV-DOC-001)

| # | Threshold | Defined at | What change trips it | Violation text (verbatim) | Class |
| --- | --- | --- | --- | --- | --- |
| B1 | A source counts as embedded-bilingual only at >=100 CJK ideographs | check_bilingual_docs.py:303-309,377-382 | Shortening a 14-ai-development root that pairs with docs/en only (shape 3) | Reported indirectly, as a new bilingual gap (B3); the count itself is never printed | BLOCKING |
| B2 | Exactly 31 required prompt files (4 global + 9 owners x 3), each >=250 chars after strip | check_bilingual_docs.py:852-882 | Adding a tenth Owner, renaming a prompt file, or trimming one below 250 characters | Required prompt library file is empty or incomplete: <rel> (or: Required prompt library file is missing: <rel>) | BLOCKING |
| B3 | Frozen bilingual gap baseline = 77 entries; it may only shrink | scripts/bilingual-baseline.txt; check_bilingual_docs.py:1102-1111 | Adding any .md under a normative root with no docs/en and docs/zh-CN pair | New bilingual gap outside frozen baseline: <path> | BLOCKING |
| B4 | A gap that got fixed must be deleted from the baseline in the same change | check_bilingual_docs.py:1112-1118 | Adding a mirror for a baselined file without editing scripts/bilingual-baseline.txt | Resolved bilingual gap must be removed from scripts/bilingual-baseline.txt: <path> | BLOCKING |
| B5 | PR body must contain the literal token BILINGUAL-MANIFEST: COMPLETE | check_bilingual_docs.py:1141,1146-1176 | Any changed .md under a normative root, or any change under docs/en or docs/zh-CN | Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE' or a fully documented 'BILINGUAL-EXCEPTION: APPROVED': <paths> | BLOCKING |
| B6 | An EMBEDDED_BILINGUAL_SOURCES registration reason must exceed 10 characters | check_bilingual_docs.py:159-169 | Trimming a reason to a placeholder while editing the registry | EMBEDDED_BILINGUAL_SOURCES has missing or placeholder reason: <source> (exit 2) | BLOCKING |
| B7 | Pair-exempt prefixes fixed at 3; 13 normative roots; PARTIAL_SIDE_BY_SIDE_PAIRS fixed at empty | check_bilingual_docs.py:36-46 | Putting a new prose subtree under 14-ai-development without adding a prefix | No dedicated message: pairing applies, and the new file surfaces later as B3 | SILENT |
| B8 | The ratchet comment count 77 must equal the 77 baseline entries, asserted by a test | .github/workflows/gates.yml:163-166; scripts/ci/test_gate_ratchet.py:114-138; scripts/ci/baselines/bilingual-docs.txt | Editing the baseline without editing the comment, or the reverse | gates.yml says N normative paths; <baseline> has M entries | BLOCKING |

### C. Required check contexts and workflow shape

| # | Threshold | Defined at | What change trips it | Violation text (verbatim) | Class |
| --- | --- | --- | --- | --- | --- |
| C1 | Declared required contexts = 16 names, set equality with the platform payload | check_declared_check_contexts.py:239-269; 14-ai-development/PR-GOVERNANCE-001.md | Renaming a required job, or adding or removing a required context on main | main requires 'X', but 14-ai-development/PR-GOVERNANCE-001.md does not declare it (and the reverse) | BLOCKING |
| C2 | Every declared context must be produced by some job id or job name | check_declared_check_contexts.py:178-206 | Deleting or renaming a job whose name is in the declared block | 14-ai-development/PR-GOVERNANCE-001.md declares required check context 'X', but no job in .github/workflows produces it | BLOCKING |
| C3 | A declared context may appear only once | check_declared_check_contexts.py:208-225 | A copy-paste edit that duplicates a line instead of adding the missing one | 14-ai-development/PR-GOVERNANCE-001.md declares required check context 'X' more than once | BLOCKING |
| C4 | session-evidence.yml must keep exactly the three job ids self-test-trusted-base, self-test-pr-head, validate | check_session_evidence_workflow_shape.py:56,271-281 | Merging those jobs back into one, or renaming one | job id 'X' is missing from .github/workflows/session-evidence.yml; the workflow must keep the three jobs PR #1014 split it into | BLOCKING |
| C5 | Shape keys: head job carries no ref:, verdict job carries no needs:, trigger types must list edited | check_session_evidence_workflow_shape.py:283-303,240-267 | Adding needs: to the verdict job, adding ref: to a head checkout, or dropping edited from types | the 'validate' job declares `needs:` ...; the verdict must not depend on another job | BLOCKING |
| C6 | Per-job timeout-minutes: 5, 10, 30, 35, 45 depending on the workflow | .github/workflows/*.yml (16 occurrences) | Making a job slower than its timeout, e.g. a full-tree scan in a 5-minute job | No checker message: the run is cancelled and the required context never becomes success | SILENT |

### D. Session evidence gate

| # | Threshold | Defined at | What change trips it | Violation text (verbatim) | Class |
| --- | --- | --- | --- | --- | --- |
| D1 | AI session evidence effective at 2026-12-01T00:00:00Z; issues created earlier are historical | .github/workflows/session-evidence.yml:21; validate.py:1991-2006,2053-2062 | Any issue created after that instant must carry its own declaration | Issue #N: policy-effective Issue has no declaration | BLOCKING |
| D2 | PR body fields are required unconditionally: Related issue(s), AI-assisted work, review identity, and a per-Issue table with 3 columns | validate.py:381-409,828-904,912-970,2187-2201 | Opening a PR with a short or template-pruned body | PR description: missing Related issue(s) / missing per-Issue mapping table | BLOCKING |
| D3 | GitHub compare returns at most 300 files; >=300 fails closed | validate.py:238-242 | A PR touching 300 or more paths | unable to determine changed paths: compare result reached the 300-file limit and may be truncated | BLOCKING |
| D4 | A truncated Git tree is refused rather than partially validated | validate.py:262-280 | A repository large enough for the recursive tree call to truncate | Git tree for <sha> is truncated; refusing partial validation | BLOCKING |
| D5 | Every referenced session-evidence blob must be larger than 0 bytes | validate.py:770-780 | Citing an empty placeholder file as evidence | raise ValidationError on a zero-size or missing tree entry | BLOCKING |
| D6 | Every SHA in the body must be 40 to 64 hex characters | validate.py:204-216,2021-2027 | Writing an abbreviated SHA, or a branch name, where a SHA is read | unable to determine changed paths: PR Base SHA is missing or invalid | BLOCKING |
| D7 | Each mapping-table row must resolve to 3 cells | validate.py:945-975 | A cell containing a pipe, or a row missing a column | raise ValidationError on a malformed row | BLOCKING |
| D8 | PR number must parse as a positive integer | validate.py:2001-2004 | A dispatch without PR_NUMBER | PR_NUMBER is missing or invalid | BLOCKING |

### E. Repository hygiene and new-file admission

| # | Threshold | Defined at | What change trips it | Violation text (verbatim) | Class |
| --- | --- | --- | --- | --- | --- |
| E1 | New-file admission allowlist: .md/.rst/.adoc, 20 source suffixes, 12 exact config names, named YAML and JSON paths | check_repository_hygiene.py:19-161,244-325,382-396 | Adding a .txt, .csv, .json or .yaml file outside the named paths | new-file admission violation: no allowlist rule for '<path>' | BLOCKING |
| E2 | New root-level files may not start with _ or . | check_repository_hygiene.py:328-342,375-381 | Adding _pr_body.md or .scratch at the repository root | '<path>' is a root-level underscore/dot file; scratch files do not belong at the repository root | BLOCKING |
| E3 | INDEX.md must carry exactly one table row per work-item directory, both directions | check_repository_hygiene.py:419-538 | Adding a work-item directory without a table row, or a row with no directory | index membership violation: directory present, no index entry: 14-ai-development/work-items/AID-... | BLOCKING |
| E4 | Every manifest-schema-registry exclusion must still exist in the commit | check_repository_hygiene.py:803-811 | Deleting or renaming a manifest listed as excluded | '14-ai-development/work-items/manifest-schema-registry.yaml' excludes N path(s) absent from this commit | BLOCKING |
| E5 | R20-01: status PR_OPEN requires implementation.pull_request to be a positive unquoted integer | check_repository_hygiene.py:853-869 | Writing pull_request: PENDING or pull_request: "123" | manifest consistency violation: '<path>': PR_OPEN requires pull_request to be a positive integer | BLOCKING |
| E6 | R20-02: merge_commit_sha NOT_MERGED cannot coexist with MERGED or VERIFIED | check_repository_hygiene.py:871-882 | Updating one lifecycle field and not the other | manifest consistency violation: '<path>': merge_commit_sha is NOT_MERGED while the lifecycle status asserts merged implementation | BLOCKING |
| E7 | Manifest path shape is AID-\d{4}-\d{3}/manifest.yaml, four digits then three | check_repository_hygiene.py:72-81,798-801 | Naming a directory AID-2026-73 or AID-173 | No message here: the file is simply never read, so nothing is checked | SILENT |

### F. Requirements traceability (T-01..T-08)

| # | Threshold | Defined at | What change trips it | Violation text (verbatim) | Class |
| --- | --- | --- | --- | --- | --- |
| F1 | T-04: an AID id may appear only once in INDEX.md | check_traceability.py:735-745 | A union merge of two appends that touched the same row | T-04 duplicate INDEX entry <id> | BLOCKING |
| F2 | T-04: a committed manifest must be indexed | check_traceability.py:786-792 | Committing a work-item directory without its INDEX row | T-04 manifest <path> exists on disk but is not indexed | BLOCKING |
| F3 | T-04: the INDEX id must name the same directory as the manifest | check_traceability.py:762-776 | Copying a row and editing only some cells | T-04 INDEX id <x> does not match manifest directory <y> | BLOCKING |
| F4 | Full 40-hex SHAs in manifests and registry, including base_commit_sha | check_traceability.py:39,818-826 | Writing a 7-character SHA, or omitting base_commit_sha | T-06 <id> has no base_commit_sha; historical baseline is ... | BLOCKING |

### G. Document metadata (GOV-DOC-002, DM-01..DM-13)

| # | Threshold | Defined at | What change trips it | Violation text (verbatim) | Class |
| --- | --- | --- | --- | --- | --- |
| G1 | schema_version must equal "2" exactly | check_document_management.py:76,713-721 | Editing the metadata schema and bumping only one side | SystemExit: 00-governance/architecture-document-metadata.schema.yaml declares schema_version 'X' but this gate implements '2' | BLOCKING |
| G2 | The schema must mark at least 5 leaves required | check_document_management.py:734-738 | Removing a required: marker while tidying the schema | SystemExit: <schema> marks fewer than 5 leaves required; a classification needs at least the four dimensions' states | BLOCKING |
| G3 | All four dimensions domain, role, lifecycle, authority must stay declared | check_document_management.py:216,722-730 | Renaming or merging a dimension | SystemExit: <schema> no longer declares ['authority']; a schema without the four dimensions cannot describe a classification | BLOCKING |
| G4 | DM-10: approved_version must be a 40-hex ancestor, and the body must be byte-identical after normalisation | check_document_management.py:1242-1315 | Editing any document whose decision_status is Approved with a pinned version | DM-10 content changed after approved_version: approval_applicability ... | BLOCKING |
| G5 | Closed enumerations: 13 domains, 9 roles, 6 decision statuses, 4 usage statuses, 3 canonical statuses, and the rest | check_document_management.py:142-171,973-1005 | Inventing a domain or a role value in a new document | DM-02 <where>.<key>: unknown value ... | BLOCKING |
| G6 | On a shallow clone the metadata gate returns INCOMPLETE, never PASS | check_document_management.py:1209,1280-1290; .github/workflows/document-management.yml:24-26 | Dropping fetch-depth: 0 from the document-management checkout | DM-10 <rel>: cannot verify ... on a shallow clone | BLOCKING |

### H. Remaining numeric gates in scripts and workflows

| # | Threshold | Defined at | What change trips it | Violation text (verbatim) | Class |
| --- | --- | --- | --- | --- | --- |
| H1 | An AI worker issue body may not exceed 20,000 characters | scripts/ai_worker/prepare_task.py:42 | A task body carrying long excerpts | issue body exceeds 20,000 characters | BLOCKING |
| H2 | Format gate: 300 s cargo timeout, 15 s git timeouts, --expect requires exactly 40 hex | check_fmt.py:61,95-99,153,267 | A slow runner, or passing an abbreviated SHA to --expect | --expect requires exactly 40 hexadecimal characters (timeout side exits 4) | BLOCKING |
| H3 | An evidence file must exceed 32 bytes and carry meaningful content | check_status_gates.py:135-168 | Citing a one-line placeholder as evidence | <field> evidence content is too short to be meaningful | BLOCKING |
| H4 | Evidence tiering: indentation exactly 0 or 2, class-to-level map, sha256 anchors 64 hex | check-evidence-tiering.py:61-78,99-110,425-432 | Declaring DOC_NORMATIVE at level 2, or indenting with 4 spaces | unsupported indentation 4 / binding.sidecar_anchor=... is not sha256:<64 hex> | BLOCKING |
| H5 | Governance operation register: exactly 7 rows x 5 columns in each of 3 files, localized headers exact | check_governance_operation_traceability.py:19-33,24,102-110 | Adding an eighth operation, or rewording a header cell | <file>: expected 7 operations, found 8 (or: row N has X columns, expected 5) | BLOCKING |
| H6 | No CRLF in any committed text blob; a NUL in the first 8,000 bytes marks a blob binary and skips it | check_line_endings.py:32,1050-1117 | Saving a document with Windows line endings | CRLF line endings in committed file '<path>': N CRLF sequences, M total lines | BLOCKING |
| H7 | Branch freshness: stale branch touching a guarded root fails; path lists print at most 20 entries | check_branch_freshness.py:42-44,111-141 | Merging main forward but leaving a governed document stale | branch is N commit(s) behind <base> and touches N guarded path(s); rebase before review so the diff equals the increment | BLOCKING |
| H8 | Delivery precheck scans only the last 3 non-empty lines, and a char literal may not exceed 12 characters | precheck_delivery.py:20-39,53-63 | Pasting tool output at the end of a .rs file | Reported as a finding line, not as a gate failure | ADVISORY |
| H9 | Display caps: 10 prose values, 5 unclassified names, 20 branch paths per list | check_document_management.py:97,2383; check_branch_freshness.py:119-123 | Nothing: the cap only shortens the log | Truncation suffix '... (+N)' with no error | ADVISORY |

## 4. Gates that fire only because a document changed

These are the ones a writer meets without touching code, in the order they usually appear:

1. **A1** — one new `.md` under `docs/` moves the count off 27, and the message asks you to edit a governance registry you did not open.
2. **B3 / B4** — a new `.md` under any normative root has no mirror, so it is a new gap; and adding the mirror to an already-baselined file requires deleting its baseline line in the same commit.
3. **B5** — any change under `docs/en` or `docs/zh-CN`, or any `.md` under a normative root, requires the literal token `BILINGUAL-MANIFEST: COMPLETE` in the PR body. The body is re-read on every `edited` event, so a body edit after a green run re-runs the gate.
4. **A3 / A4 / A5** — a new top-level directory, a registry version, or a count written in prose each fail DM-14 without any document being wrong.
5. **E3 / F1..F3** — a work-item directory and its INDEX row are one fact in two places: the row is required, it must be unique, and its id must name the same directory.
6. **H6** — a Windows editor writes CRLF and the gate rejects the committed blob, not the working file.
7. **H7** — a stale branch that touches a governed document fails even when the diff is correct.

## 5. What this record does not claim

- It does not assert any threshold is correct, too strict or too loose. The task was to record, not to judge.
- It does not claim completeness outside the searched paths in section 2.
- It does not re-run any gate as evidence. Each violation text is quoted from the checker source at `f0d881a88f0f70d45e2c67e22fc372a95198c991`; a run's output would be a different artifact with a different date.
- 77 and 27 are quoted because they are the values at `f0d881a88f0f70d45e2c67e22fc372a95198c991`. Both are designed to change; the record of the number is not a claim that the number stays.

## 6. Reproduction

```
cd <repo>; git checkout f0d881a88f0f70d45e2c67e22fc372a95198c991
grep -rnE '(>=|<=|==|!=) *[0-9]+' scripts --include=*.py
grep -rn 'MAX_\|LIMIT\|THRESHOLD' scripts .github/workflows 00-governance
grep -rn 'len(' scripts/check_bilingual_docs.py scripts/check_document_management.py \
  scripts/ci/check_repository_hygiene.py scripts/governance/session_evidence/validate.py
grep -c '' scripts/bilingual-baseline.txt
```
