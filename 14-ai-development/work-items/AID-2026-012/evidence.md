---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    usage_status: Active
    modification_status: Unchanged
    evidence_verification:
      verification_status: Unverified
  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# AID-2026-012 Evidence — Protection fingerprint

## Session role / use case

This session performed AI-assisted registration and evidence authoring for the existing Protection fingerprint workflow/checker implementation under work item `AID-2026-012`. The use case was to prepare the registration artifacts and proposed PR text while preserving the existing implementation and avoiding unsupported claims about repository actions or acceptance.

## Actual AI input

Conversation ID: `6b0935f1-14d8-83ec-92e4-31725a7c96a7`

The orchestration delivery stdout recorded these five literal inputs for this execution chain:

```text
SEND aid012-r1-brief.md -> 200 respLen=8683183 in 104s
SEND aid012-r2-fix.md -> 200 respLen=11510419 in 73s
SEND aid012-r3-fix.md -> 200 respLen=10754006 in 73s
SEND prompt-v1.md -> 200 respLen=46129 in 5s
SEND aid012-r4-exec.md -> 200 respLen=7972794 in 92s
```

The ten historical rounds and their supplied metadata are recorded in `session-evidence.md`.

## AI-visible output

This execution prepared the work-item manifest, implementation evidence, session evidence, proposed INDEX row, PR title and body, commit message, and the exact governance front matter insertion line. These are proposed artifact contents only: they have not been committed, no PR has been opened, and no merge, Owner acceptance, deployment, or Issue closure is claimed.

## 1. Evidence status and provenance

This document records the implementation and measurements supplied in the dispatch for work item `AID-2026-012`.

The assigned repository and branch facts supplied for this registration are:

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Working tree: `D:\code\wt-protection`
- Branch: `feat/2026-11-27-protection-fingerprint`
- Base branch: `main`
- Base SHA: `cc5d22b9126e00e3f93ffe71282554309908bc89`
- Branch HEAD after rebase: `355b0ccf8`
- Branch commit count: four

The branch reference could not be fetched through the connected GitHub repository interface during this authoring pass; the lookup returned `404 No commit found for the ref`. Accordingly, the branch name, HEAD, changed-file state, and supplied test measurements below are recorded as dispatch-provided facts, not as independently verified observations in this pass. No local checkout or Windows working tree was available to this authoring pass.

## 2. Existing implementation paths

The dispatch identifies the following six existing changed paths. They are recorded here and are not recreated or overwritten by this registration package.

| Path | Role |
|---|---|
| `.github/workflows/protection-fingerprint.yml` | GitHub Actions workflow |
| `14-ai-development/PR-GOVERNANCE-001.md` | Governance declaration |
| `14-ai-development/design/protection-fingerprint-ratchet.md` | Design documentation |
| `scripts/ci/baselines/protection-fingerprint.json` | Fingerprint baseline |
| `scripts/ci/check_protection_fingerprint.py` | Checker implementation |
| `scripts/ci/test_check_protection_fingerprint.py` | Checker tests |

The branch implementation facts supplied by dispatch are:

- The checker reads `GET /repos/{owner}/{repo}/branches/{branch}` (the branch summary endpoint). It does not call the Administration-only `/protection` endpoint.
- The checker supports `--endpoint auto|full|summary`.
- `auto` is the default. It attempts `full` first and falls back to `summary` on HTTP 401, 403, or 404.
- The baseline has `schema_version: 4`.
- The baseline `fingerprint` contains 12 fields.
- The baseline `summary_fingerprint` contains `enabled`, `contexts`, and `enforcement_level`.
- The workflow is named `Protection fingerprint`.
- The workflow triggers are `push` to `main`, daily cron `0 3 * * *`, and `workflow_dispatch`.
- The workflow has no `pull_request` trigger.

## 3. Baseline experiment provenance

The baseline experiment metadata supplied for the registration is:

- Date: `2026-11-25`
- Experiment head: `b5cf4f25…`
- Experiment PR: `#1038`
- Experiment run: `138943464904`

These values identify the baseline experiment. They are not the assigned branch HEAD or the base commit for this work item.

The assigned branch HEAD is reported as `355b0ccf8`; the assigned base SHA is `cc5d22b9126e00e3f93ffe71282554309908bc89`.

## 4. Test and local-run evidence

The dispatch reports the following offline test command and result:

```text
cd scripts/ci; python -m unittest test_check_protection_fingerprint
Ran 60 tests
OK
```

This is dispatch-provided evidence. The command was not independently rerun during this registration-authoring pass.

The dispatch also reports a real local checker run without a token:

```text
DEGRADED MODE — 3 field(s) verifiable, 11 unverifiable
exit code 0
```

This is also a dispatch-provided measurement, not an independently rerun result from this pass.

## 5. Endpoint access and degraded-mode rationale

The checker distinguishes between the branch summary endpoint and the full branch-protection endpoint.

The workflow token does not have the Administration permission needed to read `/protection`. A workflow using the standard `GITHUB_TOKEN` therefore cannot assume it can retrieve the full branch-protection representation. Treating an authorization failure as proof that branch protection is absent would conflate lack of permission with an observed configuration state.

The summary endpoint exposes only a limited subset of the full fingerprint. In the reported no-token run, three fields were verifiable and 11 full-protection fields were unverifiable. The checker reports degraded mode rather than presenting those 11 fields as verified or silently treating inaccessible data as a real protection value.

Consequently, this workflow does not establish that all 12 full-protection fingerprint fields are observable with its workflow token. The three-field summary is a partial observation, not a substitute for full verification. The design document explains this policy in `Why degrade instead of fail` (§9).

## 6. Required-context distinction

The dispatch reports 16 platform-required contexts measured through `GET /branches/main/protection`:

1. `GOV-DOC-001 structural checks`
2. `Branch freshness vs base`
3. `audit`
4. `GOV-DOC-002 metadata checks`
5. `BMCP protocol index (hard gate)`
6. `BMCP conformance suite (hard gate)`
7. `Schema non-empty audit (hard gate)`
8. `Bilingual docs coverage (ratchet)`
9. `Rust clippy (hard gate)`
10. `Repository hygiene (hard gate)`
11. `Rust format (hard gate)`
12. `Rust doctests (hard gate)`
13. `Session Evidence`
14. `Session Evidence self-test (base)`
15. `Session Evidence self-test (head)`
16. `rust-workspace-test`

The dispatch separately reports that `PR-GOVERNANCE-001.md` declares 17 entries. The 17 declared entries and 16 platform-required contexts are distinct counts and must not be represented as an exact match.

`Protection fingerprint` is not among the 16 platform-required contexts. This PR does not make `Protection fingerprint` a required check and does not add it to the platform-required context list.

## 7. Governance metadata repair

The dispatch reports that `scripts/check_document_management.py --require-changed origin/main` currently fails with:

```text
FAIL: 1 error(s)
  14-ai-development/PR-GOVERNANCE-001.md: DM-15 new governed document must declare a non-empty steward
```

The reported cause is that the existing governance declaration changes modify `14-ai-development/PR-GOVERNANCE-001.md`, whose `document_metadata` lacks a non-empty `steward`.

The required repair is to retain the governance declaration content changes and add the following line as a child of the existing `document_metadata:` mapping, at the same indentation as its other child fields:

```yaml
  steward: "Architecture Governance"
```

The dispatch reports that `approval.approval_applicability` is `Not-Applicable-To-Current-Version` and that the metadata-only repair is not expected to trigger a DM-10 content-hash mismatch. This expectation must still be checked by running the document-management checker.

## 8. Issue and session-evidence mapping

The dispatch identifies `#134` as the only relevant open Issue for this registration. It is a historical Issue whose record did not declare AI-assisted work.

The PR description and session evidence therefore map the Issue as:

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
|---|---|---|
| #134 | LEGACY_UNDECLARED | N/A |

Do not substitute unrelated Issue `#1145`.

The executing AI session identifier is `6b0935f1-14d8-83ec-92e4-31725a7c96a7`. The detailed session record is in `14-ai-development/work-items/AID-2026-012/session-evidence.md`.

## 9. Outstanding verification

The following checks and facts remain to be verified in the assigned checkout or at PR time:

- Confirm the repository, branch, exact branch HEAD, base SHA, and four-commit count in the working tree.
- Confirm all six existing implementation paths and their actual contents at the target HEAD.
- Confirm every manifest documentation path exists in the target HEAD git tree.
- Run `scripts/ci/check_work_item_manifest_schema.py` against the completed manifest.
- Run `scripts/ci/check_manifest_blob_pins.py` against the prompt snapshot pin values now recorded in the manifest.
- Run `scripts/check_document_management.py --require-changed origin/main` after the steward insertion.
- Run `scripts/ci/check_repository_hygiene.py`.
- Run `scripts/governance/session_evidence/validate.py` against the proposed PR body and the final session evidence.
- Confirm the generated evidence artifacts are present in the target tree and satisfy the repository-specific document checks.

No claim is made here that these checks passed in this authoring pass. No merge, acceptance, deployment, or Issue closure is claimed.
