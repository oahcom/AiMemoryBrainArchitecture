---
document_metadata:
  steward: "Architecture Governance"
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
        - "14-ai-development/work-items/AID-2026-250/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Exact PR-head checker and tests passed on d2fe8598bb4d140f62f23060c644845f72ebec36; post-merge blob verification pending."
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
# Evidence — AID-2026-250

## Scope and baseline
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Initial base: `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028`
- Branch: `w7/aid-250`
- PR: #1388
- Related Issue: #262

## Four in-scope assessment comments

| Comment | Assessment record | assessor | assessed_version | evidence_baseline |
|---|---|---|---|---|
| [#7011312621](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/262#issuecomment-7011312621) | Initial architecture internal technical risk assessment | REQ-01 Risk Assessment Owner — session `6afdd273-f2e8-83e8-b554-e52408b6086e` | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `main@d61f813cac6780b6bcc5c09536a8e9bee96cc362` |
| [#7014315135](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/262#issuecomment-7014315135) | Supplemental clarification to initial technical risk assessment | REQ-01 Risk Assessment Owner — session `6afdd273-f2e8-83e8-b554-e52408b6086e` | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `main@d61f813cac6780b6bcc5c09536a8e9bee96cc362` |
| [#7143927480](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/262#issuecomment-7143927480) | Round 26 consolidated assessment | REQ-01 Risk Assessment Owner — session `6b05b478-39e0-83ec-8bf-03ff7eb53ce5` | `aeebcbeefae874aabdf85c44f74dffd6d8fc0a1e` | `main@aeebcbeefae874aabdf85c44f74dffd6d8fc0a1e` |
| [#7149369280](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/262#issuecomment-7149369280) | Round 29 final investigation assessment | REQ-01 Risk Assessment Owner — session `6b0633de-b128-83ec-b601-d6931b084344` | `a33b482e5da5f78c4144e85dd9aef0f3f2e54fbf` | `main@a33b482e5da5f78c4144e85dd9aef0f3f2e54fbf` |

The four comment bodies were updated by appending a dedicated metadata block. Existing assessment text, findings, severity, disposition, and historical author declarations were retained. The two later comments (R26/R29) were selected as the final assessment reports; AC8 independent review comment #7153382475 and Owner adjudication #7153880925 are review/adjudication records, not assessment outputs.

## Branch synchronization
- Latest main synchronized: `756e1e25d735f526254fc3241b47880fef527b24`.
- Work-branch merge commit: `b6680b461c0f096d342b7b9855f84b3c0283146f` (two parents; no rebase, squash, or force update).

## Historical provenance boundary
The metadata is a retrospective attachment derived from the author/session and baseline already recorded in each original comment. It does not claim that the three fields were present at publication time, does not create a contemporaneous signature, and does not constitute risk acceptance or approval.

## Checker evidence
- Checker: `scripts/ci/check_req_assessment_signatures.py`
- Tests: `scripts/ci/test_check_req_assessment_signatures.py`
- Exact PR Head: `d0b137e0c28a91d5f0a1568e2a6ca64346baf4ad`.
- Workflow run: `45943429973` (Existing gates); required job: `Schema non-empty audit (hard gate)`, job ID `140323094623`.
- Checkout log explicitly records `ref: d0b137e0c28a91d5f0a1568e2a6ca64346baf4ad`; the checker did not run against the synthetic PR merge ref.
- Checker stdout:
```text
PASS comment 7011312621: assessor, assessed_version, evidence_baseline
PASS comment 7014315135: assessor, assessed_version, evidence_baseline
PASS comment 7143927480: assessor, assessed_version, evidence_baseline
PASS comment 7149369280: assessor, assessed_version, evidence_baseline
SUMMARY comments=4 failures=0
```
- Regression tests: `Ran 8 tests in 0.002s`; `OK`.
- Job URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45943429973/job/140323094623
- The run also passed the schema non-empty audit: `OK: 32 schemas; 5599 registered constraints; no unregistered or stale entries.`
- This is an exact-head CI observation. Post-merge blob verification remains pending.

## Integration
The checker and tests run in the existing required `Schema non-empty audit (hard gate)` job. The workflow adds only `issues: read` permission for the four GET requests. No new job, required context, branch-protection mutation, Issue #262 body change, or Issue closure is in scope.


## Rework — signature moved into the four assessment documents

### Defect and original carrier timestamps

The prior checker validated four Issue #262 comments rather than the four assessment-document bodies named by AC2 §5(3). The four document bodies had zero hits for the required lowercase `assessor`, `assessed_version`, and `evidence_baseline` fields (the complexity EN document had one pre-existing `- Assessor: X — ...` role line, which is not the required field). The comment metadata was appended retrospectively: #7011312621 created 2026-11-19T14:01:37Z / updated 2026-11-27T04:54:03Z; #7014315135 created 2026-11-19T15:54:06Z / updated 2026-11-27T04:54:07Z; #7143927480 created 2026-11-24T20:41:32Z / updated 2026-11-27T05:03:43Z; #7149369280 created 2026-11-25T01:15:47Z / updated 2026-11-27T04:54:14Z. The earlier checker therefore tested a different carrier and did not establish the three fields in the four document bodies.

### Four document field locations

The supplied anchors were present exactly on live main and were used. Four lines were inserted after each anchor, preserving the prior text. English/Chinese pairs use identical line positions:
- `reviews/architecture/SYS-RISK-001.en.md:12-15` — assessor, assessed_version, evidence_baseline, signature_attached.
- `reviews/architecture/SYS-RISK-001.zh-CN.md:12-15` — same four fields.
- `reviews/complexity/architecture-complexity-assessment.en.md:10-13` — same four fields.
- `reviews/complexity/architecture-complexity-assessment.zh-CN.md:10-13` — same four fields.

The assessed version is the full declared baseline `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. Each evidence_baseline is `main@b372b62c640a2b656e54b6db62a4ee67d7d8c001:` followed by that exact document path. The assessor values reuse the existing R/X role declaration.

### Checker and gate semantics

`scripts/ci/check_req_assessment_signatures.py` now reads the four document paths from the current checkout tree, not Issue comments. It has no `GITHUB_TOKEN`, HTTP client, or network access. `--root` selects an alternate checkout root for mutation tests; the default resolves the repository root from the script's own path. Missing/empty files and absent, duplicate, malformed, or mismatched fields fail closed. Output order is the fixed four-file order and is deterministic.

The checker and its tests remain in the existing `Schema non-empty audit (hard gate)` job. The workflow removes `GITHUB_TOKEN` and `issues: read`; no other workflow use of that permission was present.

### Mutation verification

The workflow mutation step checks the baseline tree, then independently deletes each of the three fields from each of the four files (12 mutations), requiring baseline exit 0 and every mutation exit 1. It recreates both document directories before each mutation so unrelated missing files cannot create false-positive failures. The exact PR-head run URL and verbatim stdout are recorded in the CI addendum below after the workflow run completes.

### Historical comments and scope

The four historical Issue #262 comment bodies and their appended metadata were not modified by this rework. This rework adds no comment metadata and does not rewrite any comment.

### Baseline-diff boundary and honest limitations

Commit `fdc36af7db20b00c2f15df9d9dd74dd999491531` changes the I P0 allowlist row in both SYS-RISK-001 language versions from the phase-3.8.9 / 1.2.13 artifact and Blob to the phase-3.8.10 / 1.2.14 successor artifact and Blob, retaining the superseded Blob and reconciliation provenance. Commit `c1de9baa9af1e245f9ebe39e955a835dbb557910` adds three explicit “not restored on main; see AID-2026-107 §10” status annotations to I-path references in each language version. These are reference/pin/status annotations, not changes to the assessment conclusions. The assessed_version remains the documents' own declared baseline; it is not a claim that the later annotation bytes existed at that baseline.

- The three fields are a **2026-11-27 retrospective attachment**, not a contemporaneous signature; the `signature_attached` line says so.
- Therefore the contemporaneity test in §5(3), which prohibits retrospective signing against the baseline, remains **not satisfied** and is an Owner adjudication item. This rework does one limited thing: it puts the three fields in the literal AC2 document-body carriers and points the checker at those carriers. It does not claim contemporaneous-signature acceptance.
- It is not verified that R/X correspond to any particular natural person's identity.
- The `reviews` scope is recorded as `not-documentation` in `document-scope-registry.yaml`; these assessment files therefore do not require GOV-DOC frontmatter. No frontmatter was added.
- Live `main` fetched for this rework was `46dac1b1e198c8d88daff5a34faf759ecb075869`; the prompt's local observation `a7cf5256` did not match this API-fetched head. The branch was created from the fetched head, not the local observation.

### Exact-head CI mutation output

Workflow run: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45947446221/job/140335286252
Head tested: `afca74bcc20ffd17609d2c6e716079ece8f84860`
Required job: `Schema non-empty audit (hard gate)` — SUCCESS.

The first mutation attempt exposed a shell issue: GitHub's default `bash -e` exited on the expected checker exit 1 before the script could record it. The workflow step was corrected with `set +e`; this successful run is the corrected implementation. Verbatim relevant output:

```text
PASS reviews/architecture/SYS-RISK-001.en.md: assessor, assessed_version, evidence_baseline
PASS reviews/architecture/SYS-RISK-001.zh-CN.md: assessor, assessed_version, evidence_baseline
PASS reviews/complexity/architecture-complexity-assessment.en.md: assessor, assessed_version, evidence_baseline
PASS reviews/complexity/architecture-complexity-assessment.zh-CN.md: assessor, assessed_version, evidence_baseline
SUMMARY files=4 failures=0
........
----------------------------------------------------------------------
Ran 8 tests in 0.013s

OK
baseline_exit=0
mutation file=reviews/architecture/SYS-RISK-001.en.md field=assessor exit=1
mutation file=reviews/architecture/SYS-RISK-001.en.md field=assessed_version exit=1
mutation file=reviews/architecture/SYS-RISK-001.en.md field=evidence_baseline exit=1
mutation file=reviews/architecture/SYS-RISK-001.zh-CN.md field=assessor exit=1
mutation file=reviews/architecture/SYS-RISK-001.zh-CN.md field=assessed_version exit=1
mutation file=reviews/architecture/SYS-RISK-001.zh-CN.md field=evidence_baseline exit=1
mutation file=reviews/complexity/architecture-complexity-assessment.en.md field=assessor exit=1
mutation file=reviews/complexity/architecture-complexity-assessment.en.md field=assessed_version exit=1
mutation file=reviews/complexity/architecture-complexity-assessment.en.md field=evidence_baseline exit=1
mutation file=reviews/complexity/architecture-complexity-assessment.zh-CN.md field=assessor exit=1
mutation file=reviews/complexity/architecture-complexity-assessment.zh-CN.md field=assessed_version exit=1
mutation file=reviews/complexity/architecture-complexity-assessment.zh-CN.md field=evidence_baseline exit=1
MUTATION OK: 12 of 12 deletions rejected
```
