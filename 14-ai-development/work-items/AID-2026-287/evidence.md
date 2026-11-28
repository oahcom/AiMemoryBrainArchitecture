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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Measurements are reported as supplied by the dispatching operator; this record does not claim an independent second-party re-measurement."
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
    canonical_scope: "Measured facts and evidence boundaries for the capacity alignment ruling AID-2026-287."
    canonical_scope_id: "ai-development/aid-2026-287-evidence"
    canonical_scope_keywords:
      - "AID-2026-287"
      - "capacity alignment"
      - "evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-287 — Evidence

## 1. Measurement baseline

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Branch: `main`
- Measurement baseline: `main` at `6306a858`
- Measurement date: `2026-11-27`
- Commit measurement window: 30 days
- Issue-reference measurement window: 60 days
- The work-item delivery baseline is separately recorded as `origin/main` at `460f437eb3496e10737b9ef20f4b816e34d155c4`. It is not the measurement baseline used for the repository-wide observations below. It is not the measurement baseline used for the repository-wide observations below.

## 2. Measured facts

### 2.1 Commit allocation by top-level path

**Observed values**

The 30-day window contained 3,272 commits, classified by top-level path as follows:

| Category | Commits | Share |
|---|---:|---:|
| `14-ai-development` record-related | 1,382 | 42% |
| Merge or empty commits | 559 | — |
| `.github` and `scripts` | 389 | 12% |
| `docs` | 349 | 11% |
| Architecture chapters | 255 | 8% |
| `crates/` | 201 | 6.1% |
| Other | 137 | — |

**Measurement method**

The commit window was inspected with Git history commands, including `git log --oneline --since="30 days ago"`, and commits were classified according to their changed top-level paths and whether they were merge or empty commits.

**What this does not establish**

These counts do not establish the quality, necessity, or value of any individual record or implementation commit. They do not by themselves prove that record work caused a shortage of implementation capacity, nor do they measure person-hours, review effort, or the complexity of changes.

### 2.2 Open issues and P0 authorization issue references

**Observed values**

The repository had 168 open issues. Eight P0 authorization issues had zero commit-message references during the 60-day window:

- `#1128`
- `#1129`
- `#1132`
- `#1133`
- `#1134`
- `#1136`
- `#1138`
- `#1139`

For each listed issue, the supplied measurement used `git log --grep="#<issue-number>" --since="60 days ago"` and returned no matching commit.

**Measurement method**

The open-issue count and issue classifications were inspected against the repository's issue state. Commit-message references were checked separately for each of the eight issue numbers using the Git `--grep` filter over the 60-day window.

**What this does not establish**

Zero commit-message matches do not prove that no work occurred. They do not inspect issue comments, pull-request descriptions, branch names, external systems, or unreferenced commits. They establish only that the searched commit messages contained no matching issue-number reference.

### 2.3 Normative corpus membership and duplication

**Observed values**

The root chapter directories and `docs/en` do not contain matching member sets. The supplied membership comparisons reported:

| Chapter | Shared members | Root members | `docs/en` members |
|---|---:|---:|---:|
| `01` | 8 | 11 | 8 |
| `03` | 6 | 13 | 6 |
| `04` | — | 43 | 13 |
| `06` | — | 26 | 12 |
| `08` | — | 106 | 5 |

Across 169 English/Chinese document pairs, only 1 pair was byte-identical. The repository contained 11 content-duplicate groups.

**Measurement method**

The root chapter and `docs/en` member sets were compared by chapter. English/Chinese pairs were compared byte-for-byte. Content-duplicate groups were counted using the supplied repository-wide duplicate analysis.

**What this does not establish**

Different membership sets do not establish which files should be deleted, moved, or designated canonical. Byte inequality does not establish semantic disagreement: translations may differ legitimately. The duplicate-group count does not establish that every member of a group is normatively interchangeable.

### 2.4 Gate negative-sample behavior

**Observed values**

Two workflow sections were identified:

- `.github/workflows/repository-hygiene.yml:65-79`: the negative-sample check asserts only `status > 1`.
- `.github/workflows/document-management.yml:36-46`: the workflow uses `github.event.pull_request.base.sha`, rather than the actual merge-candidate target base.

**Measurement method**

The specified workflow line ranges were inspected directly. The first section's negative-sample assertion was evaluated against the reported behavior of a checker that accepts a known-bad commit while still returning a status that satisfies the assertion. The second section's base reference was compared with the merge-candidate context required to validate the candidate being merged.

**What this does not establish**

These observations do not establish that every invocation of either workflow is faulty or that every possible invalid change passes. They identify defects in the stated negative-sample assertion and base-selection mechanism. A passing result from these checks cannot, on the evidence described here, be treated as proof that the relevant failure mode is detected.

### 2.5 Existing executable end-to-end chain

**Observed values**

The repository contains:

- `crates/brain-cli/tests/e2e_full_chain.rs`
- `crates/brain-cli/tests/e2e_full_pipeline.rs`

The supplied inspection describes these tests as connecting all 12 crates and identifies an existing falsification mechanism.

**Measurement method**

The test paths and their stated end-to-end scope were inspected. The existence and described coverage of these files were used as evidence that an executable chain is present in the repository.

**What this does not establish**

The presence of test source files does not establish that the tests were executed for this measurement, that they pass on the measured baseline, that CI ran them, or that their assertions cover every governance claim. It does not establish that governance decisions were actually based on their results.

### 2.6 Product-runtime and Phase 3/Phase 5 positioning

**Observed values**

The README states that the product-level runtime has not yet started. The ROADMAP places prototype/implementation in the final Phase 5. The Phase 3 exit criterion is described as requiring each component to have a bounded purpose, ownership, contract, and open questions.

**Measurement method**

The README's runtime-status statement and the ROADMAP's phase ordering and Phase 3 exit criterion were inspected as repository documentation.

**What this does not establish**

These documentation statements do not independently verify deployed runtime state, production infrastructure, or operational usage. The Phase 3 criterion's wording does not prove that Phase 3 has or has not been completed. The observation is that the stated criterion can be satisfied as a documentation exercise without necessarily demonstrating executable product behavior.

## 3. Instruments and their limits

### 3.1 `repository-hygiene.yml:65-79`

The negative-sample assertion checks whether the command's status is greater than 1. It does not assert that the known-bad sample is rejected with the specific failure behavior required by the check.

Consequently, a checker that accepts the known-bad sample can still produce a status satisfying the assertion. The test can therefore report success without demonstrating that the intended defect is detected. In this defined sense, the gate cannot prove that it can fail for the targeted negative case.

### 3.2 `document-management.yml:36-46`

The workflow obtains its base SHA from `github.event.pull_request.base.sha`. That value describes the pull request event's base reference; it is not, by itself, the actual target base of a merge-queue candidate.

A check evaluated against the wrong base can validate a different comparison from the one required for the merge candidate. Thus, a green result does not demonstrate that the candidate was checked against its actual target base. In this defined sense, the gate cannot reliably fail on defects that exist only relative to the merge candidate's true base.

### 3.3 Commit-message issue-reference search

`git log --grep="#<issue-number>" --since="60 days ago"` searches commit messages. An empty result proves only that no commit message in the searched history matched the specified pattern and time window.

It does not search issue comments, pull-request discussion, review comments, branch metadata, external trackers, or unreferenced implementation work. The eight zero-reference observations must therefore be read as commit-message-level evidence, not as proof that no activity or discussion occurred.

### 3.4 Repository documentation as an instrument

README and ROADMAP statements are evidence of what the repository documentation declares. They are not runtime telemetry or deployment attestations. They can support a diagnosis of the documented development posture, but cannot substitute for an independent runtime or deployment inspection.

## 4. What was not measured

The following items were not measured or independently verified for this record:

1. No independent second-party re-measurement of the repository-wide counts or classifications was performed.
2. The end-to-end tests were not run as part of producing this evidence record.
3. No CI result for the measured baseline or a changed branch was retrieved or verified.
4. Issue comments, pull-request comments, and review discussions were not counted in the P0 issue-reference measurement.
5. No independent runtime deployment or production-operation check was performed.
6. No independent bilingual semantic-equivalence review of the Chinese ruling and English counterpart was performed.
7. No person-hour, staffing-capacity, review-latency, or implementation-throughput measurement was performed.
8. No exhaustive audit was performed to determine whether every duplicate group is a normative conflict or whether every differing bilingual pair is semantically inconsistent.

## 5. Reproducibility

The following commands and inspection steps identify the principal evidence surfaces. They are reproducibility guidance; this record does not claim that every command below was rerun by an independent operator.

### 5.1 Commit window and path classification

```bash
git log --oneline --since="30 days ago"
```

Classify the returned commits by changed top-level path and identify merge or empty commits. For path-level verification, inspect each commit's changed paths rather than relying solely on its subject line.

### 5.2 P0 issue commit-message references

Run the following command separately for each listed issue:

```bash
git log --grep="#1128" --since="60 days ago"
git log --grep="#1129" --since="60 days ago"
git log --grep="#1132" --since="60 days ago"
git log --grep="#1133" --since="60 days ago"
git log --grep="#1134" --since="60 days ago"
git log --grep="#1136" --since="60 days ago"
git log --grep="#1138" --since="60 days ago"
git log --grep="#1139" --since="60 days ago"
```

An empty result is a zero-match result for commit messages only.

### 5.3 Normative corpus membership and content comparison

Compare the member sets of the root chapter directories and their corresponding `docs/en` directories. Preserve the path lists used for each comparison so that shared and non-shared members can be independently recounted.

For bilingual byte comparisons, pair the corresponding English and Chinese documents and compare their file bytes. For duplicate-group verification, use the same content identity rule across the repository and retain the member paths of each reported group.

### 5.4 Workflow line inspection

```bash
sed -n '65,79p' .github/workflows/repository-hygiene.yml
sed -n '36,46p' .github/workflows/document-management.yml
```

Inspect the negative-sample assertion and the source of the base SHA in their surrounding workflow context.

### 5.5 End-to-end test inventory

```bash
ls crates/brain-cli/tests/
```

Inspect the contents of `e2e_full_chain.rs` and `e2e_full_pipeline.rs` to verify the test scope. File presence alone is not a test execution result.

### 5.6 README and ROADMAP positioning

Locate and inspect the README statement about product-level runtime status and the ROADMAP sections describing Phase 3 exit criteria and Phase 5 prototype/implementation placement. Treat these as documentation claims, not runtime verification.

## 6. Evidence integrity statement

This record distinguishes three kinds of statements:

1. **Direct measurements:** repository counts, path membership comparisons, byte comparisons, duplicate-group counts, issue commit-message search results, and inspected workflow or test-file locations. These are reported as supplied by the dispatching operator and are not represented as independently re-measured here.
2. **Causal diagnosis:** explanations of how the observed negative-sample assertion and base-SHA selection can fail to validate their intended conditions. These are reasoned interpretations of the inspected mechanisms, not additional measured counts.
3. **Normative rulings:** the A1–A4 decisions in the associated capacity alignment ruling. They are proposed governance decisions, not empirical observations and not evidence of adoption.

This record does not claim that the ruling has been adopted, approved, merged, independently reviewed, or accepted. It does not claim that CI ran or passed, that the end-to-end tests were executed, or that a production runtime was independently inspected. The evidence status remains Unverified.