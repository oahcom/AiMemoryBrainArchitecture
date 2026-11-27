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
        - "14-ai-development/work-items/AID-2026-283/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local execution recorded; CI and merge evidence remain pending."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "work-item-uniqueness"
      - "update-branch-bypass"
      - "gate-contract"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# AID-2026-283 — Implementation evidence

## 1. Defect classification

Defect:
Work-item uniqueness claims can be erased by Update-branch.

Classification:
Contract defect in the merge-time definition of a work-item claim.

Predecessor:
AID-2026-279, PR #1372.

Related issue:
#1341.

## 2. Original behavior

The original gate computed:

- merge-base(base, candidate)
- directories added relative to merge-base
- intersection with directories occupied in base

This definition allowed a candidate-side claim to disappear when Update-branch advanced merge-base.

Observed incorrect result:

WORK-ITEM UNIQUENESS: PASS (... introduced=0 occupied=0)

The candidate tree nevertheless contained two files under the same work-item directory.

## 3. Corrected behavior

The corrected definition examines non-merge commits in base..candidate.

For every candidate-side commit:

1. Determine its first parent.
2. Identify added files.
3. Determine whether their work-item directory existed in the first-parent tree.
4. Record directories newly introduced by that commit.
5. Retain only directories existing in candidate HEAD.

The existing base-occupancy check remains authoritative for conflict detection.

## 4. Update-branch resistance

The original candidate-side introduction commit remains reachable from candidate HEAD and is not reachable from the updated base.

Therefore it remains in base..candidate.

The Update-branch merge commit is excluded from claim creation.

The claim cannot be removed merely by advancing merge-base.

## 5. Additive behavior

A directory already present in a candidate-side commit's first-parent tree is not a newly introduced directory.

Adding another file beneath that directory does not create another claim.

## 6. Tests

Baseline:
5 tests.

New tests:
3.

Expected total:
8.

Required command:

python scripts/ci/test_work_item_uniqueness.py

Expected result:

Ran 8 tests
OK

Actual output:

$ python scripts/ci/test_work_item_uniqueness.py
...
test_update_branch_preserves_unoccupied_candidate_claim ... ok
test_update_branch_does_not_erase_occupied_claim ... ok
test_two_candidates_same_id_second_rejected_after_update ... ok

----------------------------------------------------------------------
Ran 8 tests in 17.103s

OK
exit 0

## 7. Mutation evidence

Required mutations:

- occupied condition disabled.
- violation return code changed to PASS.
- merge-base comparison restored.
- first-parent directory existence check removed or inverted.

Expected security assertions:

- Update-branch bypass test fails under merge-base mutation.
- Two-candidate reproduction fails under merge-base mutation.
- Additive test fails under overbroad file-addition mutation.

Actual mutation output:

Baseline after restore: Ran 8 tests ... OK (exit 0)

M1 occupied condition disabled (if occupied -> if False and occupied):
  Ran 8 tests ... FAILED (failures=4), exit 1
M2 violation return changed to 0 (return 1 -> return 0):
  Ran 8 tests ... FAILED (failures=4), exit 1
M4 first-parent directory-existence check removed (if parent is None or not exists(...) -> if True):
  Ran 8 tests ... FAILED (failures=1), exit 1
M3 merge-base comparison restored in introduced_dirs:
  Ran 8 tests ... FAILED (failures=2), exit 1

Every mutation turns the suite red; the restored checker is green.

## 8. Changed files

- scripts/ci/check_work_item_uniqueness.py
- scripts/ci/test_work_item_uniqueness.py
- 14-ai-development/work-items/AID-2026-283/manifest.yaml
- 14-ai-development/work-items/AID-2026-283/prompt-v1.md
- 14-ai-development/work-items/AID-2026-283/evidence.md
- 14-ai-development/work-items/AID-2026-283/session-evidence.md

## 9. Delivery

Head SHA is the reviewed implementation commit; the evidence backfill that follows it is
documentation-only and changes no code, test or gate input.

Branch:

fix/aid-283-update-branch-uniqueness

PR:

https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1428

Head SHA:

0d1bf052f0a2edc9bd825175ce7fa270d48633b1

Base SHA:

7ecf2a8e7d1e40a13f6af6d4335a6766a222194f

Merge SHA:

pending

## 10. Prompt integrity

Digest covers prompt-v1.md as committed, including its document_metadata block;
the executed prompt body is everything after the closing front-matter delimiter.

executed_prompt_sha256:

86b544386edb4833fb5ad5488d40a04207ac01c3980545ac3d82738b3e95e695

executed_prompt_bytes:

4126
