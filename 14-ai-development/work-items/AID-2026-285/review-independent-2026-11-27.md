---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Independent review of the exact head aac82d45, executed by a reviewer session that did not implement the change. Verdict and findings were produced by a separate review conversation; the reviewer ran every command recorded here on this machine."
    usage_status: Active
    modification_status: Unchanged
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
  steward: "independent reviewer session (no implementation role)"
---

# Independent Review — AID-2026-285

## Review identity

| Field | Value |
|---|---|
| Work item | AID-2026-285 |
| Issue / PR | #1341 / #1447 |
| Reviewed candidate HEAD | `aac82d45193bbd3964184220f4bf11713a142ec8` |
| Merge commit | `08167492c786658bbb2f0ebdfd24236157ebd169` |
| Candidate / merge tree | `f43bc26c6bf0ad6b9034dd57e0a075ed85964333` |
| Changed files | 8 |
| Review date | 2026-11-27 |

The tree object IDs were verified as follows:

```text
git rev-parse aac82d45^{tree} = f43bc26c6bf0ad6b9034dd57e0a075ed85964333
git rev-parse 08167492^{tree} = f43bc26c6bf0ad6b9034dd57e0a075ed85964333
```

## Execution provenance and environment

All local commands and test runs documented in this review were executed by the independent reviewer on the reviewer's own machine.

- Host: Windows
- Shell: PowerShell 7
- Python: 3.12.3
- Python executable: `C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe`

Three detached worktrees were used:

| Worktree | Revision / purpose |
|---|---|
| `D:\code\_scratch\rev285\head` | Reviewed candidate `aac82d45193bbd3964184220f4bf11713a142ec8` |
| `D:\code\_scratch\rev285\base` | Base comparison worktree at `7ecf2a8e7d1e40a13f6af6d4335a6766a222194f` |
| `D:\code\_scratch\rev285\race` | Race-reproduction worktree, created from `7ecf2a8e…`; a local competing-claim probe commit `a1c9552057f450631c8cf82987b1dcc021f54f03` was created here |

The race worktree commit added only a `claim.txt` probe file to reproduce a competing declaration in real repository history. No implementation code was modified by the reviewer. All `EXIT=` / `RC=` values below are exit codes captured by the reviewer.

## Acceptance criteria

The criterion names below retain the original Issue #1341 wording.

| # | Criterion | Verdict | Evidence and rationale |
|---|---|---|---|
| 1 | Contract | **PASS** | The uniqueness contract distinguishes a newly introduced directory claim from a directory already occupied on the evaluated base. A directory absent at the base and introduced by the candidate can be claimed; an existing directory on the evaluated base is occupied. Adding files under an existing directory does not create a new directory claim. |
| 2 | Serialization | **PASS** | The workflow concurrency group is keyed by workflow and target branch (`pull_request.base.ref || github.ref_name`), with `cancel-in-progress: false`. PRs targeting the same branch share a group. A running check is not cancelled by a later queued run. A newer run can replace an older pending run in the same group; see finding F-03. |
| 3 | Positive test | **PASS** | `test_new_unoccupied_directory_passes` passes. The real-history positive case also reports `introduced=1 occupied=0` when evaluated against the older base. |
| 4 | Negative test | **PASS** | `test_occupied_directory_is_rejected` passes. The C6/C7 real-history replay shows the candidate passes against the older base but is rejected with `VIOLATION AID-2026-285 already exists` against the base containing the competing declaration. |
| 5 | Additive test | **PASS** | The additive-file test passes. An additional file under an already existing directory is not treated as a newly introduced directory claim. |
| 6 | Race test | **GAP** | The workflow configuration establishes target-branch serialization, and local history replay verifies rejection against a fresh base. The evidence does not include an end-to-end experiment in which multiple real GitHub Actions runs overlap, are scheduled by GitHub's concurrency service, and are then evaluated against the protected branch's required-check behavior. |
| 7 | Exact-Head test | **PASS** | The workflow passes `CANDIDATE_SHA: ${{ github.sha }}` to the checker as `--head "$CANDIDATE_SHA"`. The captured run records candidate merge SHA `124fd67ddd0412fc360251773b39683dd8ad0d81`; checkout fetches that SHA into `refs/remotes/pull/1447/merge`. The candidate merge commit has parents `168f66a6…` and `aac82d45…` and the same tree as the final merge commit. The check-run `head_sha` identifying the PR source head is not the checker input and must not be confused with it. |
| 8 | Regression evidence | **PASS** | The independent reviewer ran the uniqueness test suite, document-management regression suite, repository-hygiene suite, exact-head repository-hygiene check, governance operation traceability check, and owner namespace reference check. The reviewed candidate also has 25 successful check-runs and 16 required contexts. The command outputs are recorded below. |

## Local execution evidence

All commands in this section were executed by the independent reviewer.

### Work-item uniqueness tests on the reviewed HEAD

Working directory:

```powershell
cd D:\code\_scratch\rev285\head
```

HEAD: `aac82d45193bbd3964184220f4bf11713a142ec8`

Command:

```powershell
python -X utf8 scripts/ci/test_work_item_uniqueness.py
```

Output:

```text
Ran 8 tests in 12.226s
OK
EXIT=0
```

The test suite exercises `scripts/ci/check_work_item_uniqueness.py` through `sys.executable`.

### Work-item uniqueness tests on the base worktree

Working directory:

```powershell
cd D:\code\_scratch\rev285\base
```

HEAD: `7ecf2a8e7d1e40a13f6af6d4335a6766a222194f`

Command:

```powershell
python -X utf8 scripts/ci/test_work_item_uniqueness.py
```

Output:

```text
Ran 5 tests in 7.520s
FAILED (failures=5)
EXIT=1
```

All five failures were `AssertionError: 9009 != <expected>`. The subprocess attempted to invoke `python3`, which resolved to the WindowsApps stub; subprocess stdout was empty. This is a test-environment invocation failure, not evidence of a uniqueness-checker logic defect.

### Positive and negative uniqueness-checker cases

Working directory:

```powershell
cd D:\code\_scratch\rev285\head
```

Positive case against the event base:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --base 168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab --head aac82d45193bbd3964184220f4bf11713a142ec8
```

Result:

```text
WORK-ITEM UNIQUENESS: PASS (base=168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab candidate=aac82d45193bbd3964184220f4bf11713a142ec8 introduced=1 occupied=0)
EXIT=0
```

Base-ref resolution case:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --base refs/remotes/origin/main --head aac82d45193bbd3964184220f4bf11713a142ec8
```

Result:

```text
WORK-ITEM UNIQUENESS: PASS (base=5e30d49776a2ce75069227a41470fa7e4ae00b2e candidate=aac82d45193bbd3964184220f4bf11713a142ec8 introduced=0 occupied=0)
EXIT=0
```

Older-base case:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --base 7ecf2a8e7d1e40a13f6af6d4335a6766a222194f --head ece472aa8d4139fa0d3d441b199a1251549f7eb1
```

Result:

```text
WORK-ITEM UNIQUENESS: PASS (base=7ecf2a8e7d1e40a13f6af6d4335a6766a222194f candidate=ece472aa8d4139fa0d3d441b199a1251549f7eb1 introduced=0 occupied=0)
EXIT=0
```

Missing-base fail-closed case:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --head aac82d45
```

Result:

```text
INCOMPLETE (missing required ref(s): --base)
EXIT=2
```

Unresolvable-base fail-closed case:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --base refs/heads/nope-zzz --head aac82d45
```

Result:

```text
WORK-ITEM UNIQUENESS: INCOMPLETE (git ('rev-parse', '--verify', 'refs/heads/nope-zzz^{commit}') exited 128: fatal: Needed a single revision)
EXIT=2
```

Local competing-claim positive replay:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --base 7ecf2a8e7d1e40a13f6af6d4335a6766a222194f --head a1c9552057f450631c8cf82987b1dcc021f54f03
```

Result:

```text
WORK-ITEM UNIQUENESS: PASS (base=7ecf2a8e7d1e40a13f6af6d4335a6766a222194f candidate=a1c9552057f450631c8cf82987b1dcc021f54f03 introduced=1 occupied=0)
EXIT=0
```

Local competing-claim negative replay against the base containing the merged claim:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --base 08167492c786658bbb2f0ebdfd24236157ebd169 --head a1c9552057f450631c8cf82987b1dcc021f54f03
```

Result:

```text
VIOLATION: 14-ai-development/work-items/AID-2026-285 already exists on target base 08167492c786658bbb2f0ebdfd24236157ebd169
WORK-ITEM UNIQUENESS: VIOLATION (base=08167492c786658bbb2f0ebdfd24236157ebd169 candidate=a1c9552057f450631c8cf82987b1dcc021f54f03 introduced=1 occupied=1)
EXIT=1
```

These cases establish the distinction between a valid new claim against the older base and a duplicate claim against a base that already contains AID-2026-285.

### Document-management regression suite

Working directory:

```powershell
cd D:\code\_scratch\rev285\head
```

Command:

```powershell
python -X utf8 scripts/test_check_document_management.py
```

Result:

```text
371/371 passed
1 skipped, 1 registered of 5 allowed: T68c a real 0o000 directory is reported by path (integration)
EXIT=0
```

### Repository-hygiene regression suite

Working directory:

```powershell
cd D:\code\_scratch\rev285\head
```

Command:

```powershell
python -X utf8 scripts/test_check_repository_hygiene.py
```

Output:

```text
Ran 105 tests in 151.586s
OK (skipped=1)
RC1=0
```

### Exact-head repository-hygiene check

Working directory:

```powershell
cd D:\code\_scratch\rev285\head
```

Command:

```powershell
python -X utf8 scripts/ci/check_repository_hygiene.py --base 168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab --head aac82d45193bbd3964184220f4bf11713a142ec8
```

Output:

```text
Work-item index membership version=2026-11-27.2 directories=142 linked=142
Work-item manifest consistency version=2026-11-27.2 manifests=131 in_scope=116 excluded_by_record_type=5 unrecognized=10 violations=0
Repository new-file admission version=2026-11-27.2 base=168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab head=aac82d45193bbd3964184220f4bf11713a142ec8 merge_base=168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab
Repository new-file admission passed: 4 new path(s) checked.
RC2=0
```

This is repository-hygiene admission evidence. It is not used as evidence for the work-item uniqueness check's positive test; that evidence is the uniqueness test and the real-history `introduced=1 occupied=0` replay above.

### Governance operation traceability

Working directory:

```powershell
cd D:\code\_scratch\rev285\head
```

Command:

```powershell
python -X utf8 scripts/check_governance_operation_traceability.py --check
```

Output:

```text
GOVERNANCE OPERATION TRACEABILITY: PASS (7 operations x 3 mirrors)
RC=0
```

### Owner namespace references

Working directory:

```powershell
cd D:\code\_scratch\rev285\head
```

Command:

```powershell
python -X utf8 scripts/check_owner_namespace_references.py --check
```

Output:

```text
OWNER NAMESPACE: PASS (15 registered documents scanned)
RC=0
```

## GOV-DOC-002 workflow execution evidence

The following is the captured run record for the GOV-DOC-002 execution:

```text
PR_BASE: 168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab
BASE_REF: main
PUSH_BEFORE: 23d8b42b746179b3e0153149d433e1139acc3794
CANDIDATE_SHA: 124fd67ddd0412fc360251773b39683dd8ad0d81

WORK-ITEM UNIQUENESS: PASS (base=168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab candidate=124fd67ddd0412fc360251773b39683dd8ad0d81 introduced=1 occupied=0)
```

The checkout fetched the candidate merge SHA with this refspec:

```text
+124fd67ddd0412fc360251773b39683dd8ad0d81:refs/remotes/pull/1447/merge
```

This records the exact candidate SHA evaluated by the workflow and the positive uniqueness-check result for that candidate.

## Required CI checks

At the reviewed candidate HEAD `aac82d45193bbd3964184220f4bf11713a142ec8`, all 25 check-runs were `success`. The set included:

- `Repository hygiene (hard gate)`
- `GOV-DOC-001 structural checks`
- `Bilingual docs coverage (ratchet)`
- `Session Evidence`
- `Schema non-empty audit (hard gate)`
- `rust-workspace-test`

The protected branch configuration had 16 required contexts, including `GOV-DOC-002 metadata checks`. The branch-protection setting was `strict: true`.

## Base-refresh and race-replay evidence

The reviewer reproduced the relevant history distinction: the candidate passes against the older base, while the same candidate is rejected as a violation against the base containing the competing declaration. The missing-base and unresolvable-base paths return `INCOMPLETE` with exit code 2, i.e. fail closed.

The workflow source and static tests establish that the base fetch occurs before the checker invocation. The GOV-DOC-002 run record above identifies the PR base and the candidate merge SHA used for the uniqueness check. The local `refs/remotes/origin/main` invocation separately resolved to `5e30d49776a2ce75069227a41470fa7e4ae00b2e` and returned `introduced=0 occupied=0`; that local ref-resolution result is not evidence that the workflow run used that later SHA.

## Findings

### F-01 — No end-to-end GitHub Actions concurrency race test

- **Severity:** Medium
- **Acceptance criterion:** Race test
- **Merge-blocking:** No — the PR has already merged.
- **Evidence:** The workflow configuration uses a target-branch concurrency group and `cancel-in-progress: false`. Local sequential replay verifies that a competing claim is rejected against a base containing the prior claim. No captured experiment demonstrates overlapping real GitHub Actions runs, GitHub's actual scheduling behavior, and the resulting required-check enforcement as one end-to-end scenario.
- **Impact:** The implementation has credible source-level and local behavioral evidence, but the strongest operational race guarantee has not been demonstrated under the actual CI scheduler and branch-protection mechanism.
- **Follow-up:** Add an integration test or controlled CI exercise that creates overlapping PR runs against the same protected target branch, observes their running/pending/cancelled states, and verifies that no candidate can merge using a stale successful required check after the target branch advances.

### F-02 — Runtime evidence does not independently demonstrate a refreshed base

- **Severity:** Low
- **Acceptance criterion:** Race test / runtime evidence
- **Merge-blocking:** No — the PR has already merged.
- **Evidence:** Source inspection and static tests show that the base fetch precedes checker execution. The captured GOV-DOC-002 run records the PR base SHA and candidate SHA, but does not show a fetched target-branch SHA that differs from the event base. The local `refs/remotes/origin/main` invocation resolved to `5e30d49776a2ce75069227a41470fa7e4ae00b2e`; it is a separate local invocation and does not establish which base the workflow fetched at runtime.
- **Impact:** The runtime trace does not independently prove that the workflow evaluated a base that advanced after the event was created. The separate local fresh-base replay does demonstrate the checker's behavior when given a base containing the competing claim.
- **Follow-up:** Emit the resolved target-branch base SHA immediately after fetch and immediately before checker execution. Add a controlled run in which the target branch advances after the event is created, and assert that the checker receives the advanced base SHA.

### F-03 — Newer runs can replace pending runs in a shared concurrency group

- **Severity:** Low
- **Acceptance criterion:** Serialization operational liveness
- **Merge-blocking:** No — this is fail-closed behavior, not a false-success path.
- **Evidence:** The `push: branches: [main]` workflow run and PR-to-main runs use the same concurrency group name, `Architecture document management gate-main`. GitHub concurrency permits one running and one pending run per group. When another run enters the same group, the oldest pending run is cancelled/replaced; `cancel-in-progress: false` prevents cancellation of the running run but does not preserve every pending run.
- **Impact:** During a burst of merges or PR updates, a queued PR validation can be cancelled before it starts. The cancelled run does not produce a successful check, so this does not create a false PASS or bypass the gate. It can nevertheless create avoidable check noise and require a PR validation rerun.
- **Follow-up:** Consider separating push-to-main and PR-to-main concurrency groups if their mutual serialization is not required, or document the expected cancellation/re-run behavior. Preserve target-branch serialization for PR checks and retain `cancel-in-progress: false`.

### F-04 — Merged work-item records incorrectly say GitHub Actions was not run

- **Severity:** Low
- **Acceptance criterion:** Regression evidence / work-item record accuracy
- **Merge-blocking:** No — this is a documentation accuracy defect, not a runtime gate defect.
- **Evidence:** On the reviewed, merged candidate, the AID-2026-285 `manifest.yaml` test list ends with `GitHub Actions workflow execution — NOT RUN.` The `evidence.md` statements in sections 7 and 8 also say `GitHub Actions workflow execution: NOT RUN`, and `INDEX.md` says `GitHub Actions NOT RUN`. However, the candidate's `GOV-DOC-002 metadata checks` run completed successfully at `2026-11-27T07:32:59Z`, and the candidate has 25 successful check-runs.
- **Impact:** The merged work-item record makes a factually incorrect statement about whether GitHub Actions ran. This weakens the accuracy and auditability of the work-item evidence even though the CI gate itself passed.
- **Follow-up:** Correct the manifest, evidence record, and index entry to distinguish local execution from GitHub Actions execution and record the actual successful workflow/check-run evidence. Add a closeout check that detects stale `NOT RUN` claims when corresponding successful check-runs exist.

## Overall verdict

**ACCEPT WITH AMENDMENTS**

The implementation satisfies the core uniqueness contract, exact-candidate evaluation, positive and negative checker behavior, additive-file behavior, and target-branch serialization configuration. The expanded independent regression evidence closes the earlier AC8 evidence gap: the reviewer executed the uniqueness test suite, document-management suite, repository-hygiene suite and exact-head hygiene check, governance operation traceability check, and owner namespace reference check locally. The reviewed candidate also has all 25 check-runs successful.

The Race test remains a gap because the evidence does not include an end-to-end concurrency race exercise using actual GitHub Actions scheduling and required-check enforcement. The shared concurrency group also has a low-severity pending-run replacement/liveness consequence. Separately, the merged work-item records contain stale `NOT RUN` statements despite successful GitHub Actions execution; these should be corrected as a documentation follow-up.

None of the findings establishes a false-PASS path or requires reverting the already merged implementation. The follow-ups above should be tracked to close the remaining operational-evidence and documentation-accuracy gaps.

**The independent reviewer executed the documented local commands and did not modify any implementation code.**
