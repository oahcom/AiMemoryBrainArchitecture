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
        - "14-ai-development/work-items/AID-2026-291/manifest.yaml"
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "PR #1427 merged at 93532c4; all 11 changed file blobs match the merged tree. A post-merge push exposed strict baseline-pin equality, now corrected in the follow-up ratchet change."
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
    canonical_scope: "Execution and audit evidence for the AID-2026-291 prompt-to-implementation trace checker and ratchet."
    canonical_scope_id: "ai-development/aid-2026-291-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-291"
      - "prompt-to-commit trace"
      - "AC6 evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Evidence — AID-2026-291

## Source and implementation

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Assigned issue: #265 (AC6)
- Branch: `feat/aid-290-prompt-commit-trace`
- PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1427
- Current main/base SHA used by the final Actions scan: `5e30d49776a2ce75069227a41470fa7e4ae00b2e`
- Branch synchronization merge commit: `57ff99cf3986d2effea75460a206e8754e3561a2`
- Validated PR head for the final Actions run: `96d2a57f6993bd9ccde507948624d193965c461c`
- Existing AID-2026-290 for Issue #1268 is preserved; this work item and its index row use AID-2026-291 only.

## Actions run and baseline artifact

- Final Existing gates run: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45963335255
- Final metrics artifact: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45963335255/artifacts/15181278161
- The committed `baseline.json` is the byte-for-byte `baseline-seed.json` from Actions run https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45962312050 (artifact 15181835100), generated against the same main SHA.
- Baseline file size: 19,335 bytes.
- Git blob SHA: `c7b982a64a8e75a6ed301161e6fd3e74a2704305`.
- SHA-256: `fdec7294cbe8ddb169d0529d65f21ecf357e8846c8c7652989a825dda46e2188`.
- Baseline JSON `commit` and `source_commit`: `5e30d49776a2ce75069227a41470fa7e4ae00b2e`.
- Baseline entries: 133 (132 manifests in the measured main snapshot plus the initial AID-2026-291 seed). The seed records AID-2026-291 as `NO_TRACE`; it does not assert traceability.
- The checker fails closed if the baseline file is absent or malformed; the follow-up ratchet correction requires the baseline `commit` pin to resolve and be an ancestor of the current comparison base, preserving the immutable snapshot pin as main advances.
- Repository hygiene initially rejected the new JSON path because its allowlist is exact. The allowlist was extended only for `14-ai-development/work-items/AID-2026-291/baseline.json`, with a dedicated admission test. No unrelated gate job or branch-protection setting was changed.

## Five primary states

Actions measured the main snapshot at 132 manifests and the PR snapshot at 133 manifests.

| Primary status | Main snapshot | PR snapshot |
|---|---:|---:|
| `NO_TRACE` | 124 | 125 |
| `DIGEST_UNPINNED` | 5 | 5 |
| `DIGEST_MISMATCH` | 1 | 1 |
| `COMMIT_UNREACHABLE` | 2 | 2 |
| `TRACEABLE` | **0** | **0** |

**TRACEABLE=0** in the measured main snapshot and the PR snapshot.

## 3×4 matrix — main snapshot (Actions artifact)

| Prompt dimension | Commit ABSENT | Commit REACHABLE | Commit UNREACHABLE |
|---|---:|---:|---:|
| `ABSENT` | 66 | 1 | 0 |
| `HEAD_MATCH` | 50 | 3 | 2 |
| `PINNED_OK` | 6 | 0 | 2 |
| `UNPINNED_MISMATCH` | 1 | 0 | 1 |

## 3×4 matrix — PR snapshot (Actions log)

| Prompt dimension | Commit ABSENT | Commit REACHABLE | Commit UNREACHABLE |
|---|---:|---:|---:|
| `ABSENT` | 67 | 1 | 0 |
| `HEAD_MATCH` | 50 | 3 | 2 |
| `PINNED_OK` | 6 | 0 | 2 |
| `UNPINNED_MISMATCH` | 1 | 0 | 1 |

The PR job log's primary and matrix lines (verbatim):

```text
PRIMARY NO_TRACE=125
PRIMARY DIGEST_UNPINNED=5
PRIMARY DIGEST_MISMATCH=1
PRIMARY COMMIT_UNREACHABLE=2
PRIMARY TRACEABLE=0
MATRIX PINNED_OK x REACHABLE=0
MATRIX PINNED_OK x UNREACHABLE=2
MATRIX PINNED_OK x ABSENT=6
MATRIX HEAD_MATCH x REACHABLE=3
MATRIX HEAD_MATCH x UNREACHABLE=2
MATRIX HEAD_MATCH x ABSENT=50
MATRIX UNPINNED_MISMATCH x REACHABLE=0
MATRIX UNPINNED_MISMATCH x UNREACHABLE=1
MATRIX UNPINNED_MISMATCH x ABSENT=1
MATRIX ABSENT x REACHABLE=1
MATRIX ABSENT x UNREACHABLE=0
MATRIX ABSENT x ABSENT=67
BASE_SHA: 5e30d49776a2ce75069227a41470fa7e4ae00b2e
```

## Eleven named manifest assertions

All rows below are from the PR snapshot in artifact 15181278161.

| Manifest | Prompt dimension | Commit dimension | Primary status | Findings |
|---|---|---|---|---|
| AID-2026-011 | `PINNED_OK` | `ABSENT` | `NO_TRACE` | `commit_absent` |
| AID-2026-040 | `PINNED_OK` | `ABSENT` | `NO_TRACE` | `commit_absent` |
| AID-2026-041 | `UNPINNED_MISMATCH` | `UNREACHABLE` | `DIGEST_MISMATCH` | `digest_pinned_mismatch`, `commit_unreachable` |
| AID-2026-042 | `PINNED_OK` | `UNREACHABLE` | `COMMIT_UNREACHABLE` | `commit_unreachable` |
| AID-2026-043 | `PINNED_OK` | `UNREACHABLE` | `COMMIT_UNREACHABLE` | `commit_unreachable` |
| AID-2026-044 | `PINNED_OK` | `ABSENT` | `NO_TRACE` | `commit_pending` |
| AID-2026-045 | `PINNED_OK` | `ABSENT` | `NO_TRACE` | `commit_pending` |
| AID-2026-046 | `PINNED_OK` | `ABSENT` | `NO_TRACE` | `commit_pending` |
| AID-2026-047 | `HEAD_MATCH` | `REACHABLE` | `DIGEST_UNPINNED` | `digest_unpinned` |
| AID-2026-048 | `HEAD_MATCH` | `UNREACHABLE` | `DIGEST_UNPINNED` | `digest_unpinned`, `commit_unreachable` |
| AID-2026-049 | `HEAD_MATCH` | `UNREACHABLE` | `DIGEST_UNPINNED` | `digest_unpinned`, `commit_unreachable` |

AID-2026-047 remains `DIGEST_UNPINNED` / `HEAD_MATCH` + `REACHABLE`. It has no immutable prompt pin, receives no exception or fabricated pin, and is not TRACEABLE.

## Required contexts and check-run evidence

The final validated head `96d2a57f6993bd9ccde507948624d193965c461c` had 18 check-runs. The 16 required contexts, derived by matching the recent merged-PR required-name set, were all SUCCESS (16/16):

1. `Session Evidence self-test (head)` — SUCCESS
2. `Session Evidence` — SUCCESS
3. `Rust format (hard gate)` — SUCCESS
4. `Rust doctests (hard gate)` — SUCCESS
5. `Session Evidence self-test (base)` — SUCCESS
6. `BMCP protocol index (hard gate)` — SUCCESS
7. `Rust clippy (hard gate)` — SUCCESS
8. `Schema non-empty audit (hard gate)` — SUCCESS
9. `BMCP conformance suite (hard gate)` — SUCCESS
10. `GOV-DOC-002 metadata checks` — SUCCESS
11. `GOV-DOC-001 structural checks` — SUCCESS
12. `audit` — SUCCESS
13. `Bilingual docs coverage (ratchet)` — SUCCESS
14. `Repository hygiene (hard gate)` — SUCCESS
15. `Branch freshness vs base` — SUCCESS
16. `rust-workspace-test` — SUCCESS

The two additional check-runs were `Prompt-to-commit trace (ratchet)` — SUCCESS and `Work Item manifest schema (read-only baseline)` — SUCCESS. Neither is a required branch-protection context. In particular, Prompt-to-commit trace can make a PR check suite red if it fails, but it does not technically block merge under the current branch-protection configuration. Adding it to the required context set is an Owner/operator follow-up; this work did not change branch protection. The existing Schema non-empty audit job was not modified and passed.

## R4 adjudication

AID-2026-047 has no `prompt_file_blob_sha` or `prompt_file_commit_sha` in its current main manifest. Its prompt bytes match HEAD, and its implementation commit is reachable. It is therefore `DIGEST_UNPINNED`, prompt dimension `HEAD_MATCH`, commit dimension `REACHABLE`; findings include `digest_unpinned` and exclude `digest_head_mismatch`. No manifest pin is added.

## PR merge and post-merge blob verification

- PR #1427 merged: `93532c4899cc130ae4cc6a6c26b39f1499c26f6d`.
- Merged at: `2026-11-27T08:14:31Z`.
- Merge base: `5e30d49776a2ce75069227a41470fa7e4ae00b2e`.
- The 11 changed file blobs in the PR head were compared with the merge commit tree; all 11 match exactly.

| File | Expected PR-head blob | Merge-tree blob | Result |
|---|---|---|---|
| `.github/workflows/gates.yml` | `50a04591963109b5112d97c388319d61d6268fb0` | `50a04591963109b5112d97c388319d61d6268fb0` | MATCH |
| `14-ai-development/work-items/AID-2026-291/baseline.json` | `c7b982a64a8e75a6ed301161e6fd3e74a2704305` | `c7b982a64a8e75a6ed301161e6fd3e74a2704305` | MATCH |
| `14-ai-development/work-items/AID-2026-291/evidence.md` | `be06c039c3a98c2e4b0d352968b3d05a34caf4b0` | `be06c039c3a98c2e4b0d352968b3d05a34caf4b0` | MATCH |
| `14-ai-development/work-items/AID-2026-291/manifest.yaml` | `35ebd80cd519842f28a9c8040ee39e6b8024a007` | `35ebd80cd519842f28a9c8040ee39e6b8024a007` | MATCH |
| `14-ai-development/work-items/AID-2026-291/prompt-v1.md` | `1cba3071755b1e93a8b70bd4ef3efcf3eab94fed` | `1cba3071755b1e93a8b70bd4ef3efcf3eab94fed` | MATCH |
| `14-ai-development/work-items/AID-2026-291/session-evidence.md` | `4046ba511ee7192ccb5153d7a71d716b706e60be` | `4046ba511ee7192ccb5153d7a71d716b706e60be` | MATCH |
| `14-ai-development/work-items/INDEX.md` | `4eb0f62283f61e1d84689266d2abeed3411458c7` | `4eb0f62283f61e1d84689266d2abeed3411458c7` | MATCH |
| `scripts/ci/check_prompt_commit_trace.py` | `af38cc48525f01d5238f73f4979af0bf0ae56660` | `af38cc48525f01d5238f73f4979af0bf0ae56660` | MATCH |
| `scripts/ci/check_repository_hygiene.py` | `f2a7b93d9f6b3847fbaa0a6f7e9ab8e459009400` | `f2a7b93d9f6b3847fbaa0a6f7e9ab8e459009400` | MATCH |
| `scripts/ci/test_check_prompt_commit_trace.py` | `556a7cbf88d01f840f43ecd337e7cf9447441008` | `556a7cbf88d01f840f43ecd337e7cf9447441008` | MATCH |
| `scripts/test_check_repository_hygiene.py` | `7963f2efc6746d994ce0904c21a344b30a0a0c74` | `7963f2efc6746d994ce0904c21a344b30a0a0c74` | MATCH |

The unrelated Issue #1268 work item was preserved: `AID-2026-290/manifest.yaml` blob `6cec1ee583a29cff889161bf147686f2d2c3e59a` is identical before and after the merge.

## Post-merge ratchet correction

The push-triggered Existing gates run on merge commit `93532c4899cc130ae4cc6a6c26b39f1499c26f6d` was run at https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45964155877. All ordinary hard-gate jobs passed, but the non-required `Prompt-to-commit trace (ratchet)` job failed closed because it required the historical baseline pin `5e30d49776a2ce75069227a41470fa7e4ae00b2e` to equal the new main SHA `93532c4899cc130ae4cc6a6c26b39f1499c26f6d`. This exposed a baseline-age bug, not a trace classification regression. The follow-up change now accepts the immutable baseline pin only when it resolves and is an ancestor of the current comparison base; it retains the exact pin, continues to fail closed for missing/non-ancestor pins, and uses the pre-push main SHA for push events. The follow-up PR's exact-head checks are the final gate before the #265 comment.

## Required-context interpretation

The 18 check-runs on PR head `96d2a57f6993bd9ccde507948624d193965c461c` included the 16 required contexts listed above, all SUCCESS, plus two non-required contexts. `Prompt-to-commit trace (ratchet)` and `Work Item manifest schema (read-only baseline)` are not required branch-protection contexts. If the trace job fails, it can make the PR check suite red but does not technically block merge under current protection. Adding it to the required set remains an Owner/operator follow-up; no branch protection was modified.

**TRACEABLE=0** remains the measured conclusion for the main snapshot and the PR snapshot.
