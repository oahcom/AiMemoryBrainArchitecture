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
        - "14-ai-development/work-items/AID-2026-013/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "任务输入与产出已记录；会话身份、精确提示词字节与独立执行来源未验证。"
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
    canonical_scope: "AID-2026-013 implementation evidence and measured defect record"
    canonical_scope_id: "ai-development/aid-2026-013-evidence"
    canonical_scope_keywords:
      - "AID-2026-013"
      - "GOV-DOC-002"
      - "concurrency"
      - "required context"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "AI-assisted implementation; human-directed"
---

# AID-2026-013 — GOV-DOC-002 concurrency defect evidence

## 1. Baseline

Repository: `oahcom/AiMemoryBrainArchitecture`

Base branch: `main`

Base commit: `3d9b32bef6775974117ea0ab925179acf43c6ecb`

Evidence date: `2026-11-28`

This document records the defect facts supplied with the implementation task and the intended bounded change. The measurements below are task-provided evidence; this document does not claim that this session independently reran the measurements.

## 2. Measured defect

Before the change, the repository-wide measurement found:

| Measurement | Result |
|---|---:|
| Cancelled workflow runs across the repository | 281 |
| Cancelled runs in `document-management.yml` | 9 |
| Open pull requests examined | 19 |
| Remote branches examined | 1155 |

PR #1443, at head `938e160f`, had no check run at all for the required context:

`GOV-DOC-002 metadata checks`

The relevant workflow run was `45963399555`. It was cancelled. In the same second, PR #1448's run in the same concurrency group succeeded.

Consequently, PR #1443 did not receive a failure result for this required context. The context was absent, leaving the PR blocked without a corresponding failing check to explain the missing result.

The examination of 19 open PRs and 1155 remote branches found no existing changes to the three affected workflow lines.

## 3. Original workflow concurrency block

The original nine lines were:

```yaml
# Work-item uniqueness is a shared target-branch invariant, not a
# per-candidate invariant. PRs targeting the same branch must not run this
# gate in independent concurrency groups. Do not cancel a running decision
# when another candidate arrives.
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.base.ref || github.ref_name }}
  cancel-in-progress: false
```

All PRs targeting `main` shared the same group string.

`cancel-in-progress: false` prevented cancellation of an already-running decision. It did not provide unlimited pending-run capacity. The concurrency group had one pending slot. A later run could replace an earlier pending run.

The observed cancellation and missing required context demonstrate the practical consequence: a workflow run could disappear before producing its required check result.

## 4. Replacement workflow concurrency block

The replacement is:

```yaml
# This job is read-only and re-fetches the current target base before evaluating
# uniqueness, so concurrent pull requests do not need a global serial decision.
# Branch freshness vs base requires an out-of-date PR to catch up and rerun
# this workflow, including its required contexts, after synchronization.
# We abandon global serialization, which never actually held: the single pending
# slot replaced queued runs. Keep running decisions safe within each pull request.
concurrency:
  group: ${{ github.workflow }}-${{ github.event_name }}-${{ github.event.pull_request.number || github.ref_name }}
  cancel-in-progress: false
```

The new expression distinguishes:

- Different event types through `github.event_name`.
- Different pull requests through `github.event.pull_request.number`.
- Non-pull-request events through the fallback `github.ref_name`.

Different pull requests therefore have independent concurrency groups.

The `cancel-in-progress: false` setting remains unchanged.

## 5. Why per-pull-request concurrency is acceptable

The reason for abandoning cross-PR global serialization is based on the actual decision implementation and its freshness protection.

### 5.1 Read-only decision

The document-management job has:

```yaml
permissions: contents: read
```

It is read-only. It performs no write operations and does not modify shared mutable state.

There is therefore no shared mutable resource between independent executions that requires mutual exclusion.

### 5.2 Evaluation uses the current target base

The unchanged step:

`Enforce work-item uniqueness against the current target base`

fetches the current target branch using:

```bash
git fetch origin "+refs/heads/${BASE_REF}:..."
```

It evaluates the generated merge candidate against the fetched target base.

The uniqueness decision does not depend on a stale base SHA embedded in the pull-request event.

### 5.3 Freshness is independently enforced

The required context:

`Branch freshness vs base`

rejects a pull-request head that does not contain the target base.

An outdated pull request must catch up with the target base. That synchronization produces a `synchronize` event, which reruns this workflow together with its required contexts.

Consequently, per-PR concurrency does not rely on a stale successful decision being sufficient for acceptance.

### 5.4 What is abandoned

The change abandons the proposed global serialization of uniqueness decisions across all pull requests targeting the same branch.

That serialization never actually held: the concurrency group had only one pending slot, and later arrivals could replace pending runs.

Its observed cost included 281 cancelled runs repository-wide, nine cancelled runs in this workflow, and the permanently absent `GOV-DOC-002 metadata checks` result on PR #1443.

### 5.5 What is retained

The change retains:

- No cancellation of an already-running decision when a new run for the same PR arrives.
- Independent concurrency groups for different pull requests.
- Execution-time fetching of the current target base.
- The existing branch-freshness required context.
- All existing workflow triggers, jobs, steps, names, and required-context producers.

## 6. Branch protection qualification

The branch protection `strict` setting was measured as `false` by API on 2026-11-28.

This implementation does not claim that branch protection has `strict: true`.

The freshness argument relies on the existing required context `Branch freshness vs base` and its explicit catch-up and synchronization behavior, not on a strict branch-protection setting.

## 7. Required-context preservation

The job name remains exactly:

`GOV-DOC-002 metadata checks`

It is not renamed, removed, or replaced.

The 16 required contexts are:

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

This change modifies only the concurrency group and its explanatory comments. The job name and all steps remain unchanged. No workflow trigger is added or modified.

The concurrency change does not alter the definition or production mechanism of any of these 16 required contexts.

## 8. Local acceptance commands

The six commands designated for this work item are:

1. YAML parsing and inspection of the job name and concurrency configuration:

```bash
python -c "import yaml;d=yaml.safe_load(open('.github/workflows/document-management.yml',encoding='utf-8'));print(d['jobs']['document-management']['name']);print(d['concurrency'])"
```

2. Manifest parsing:

```bash
python scripts/ci/check_manifest_parse.py
```

3. Work-item index traceability:

```bash
python scripts/check_traceability.py --index-only
```

4. Document-management validation:

```bash
python scripts/check_document_management.py --require-changed origin/main
```

5. Work-item uniqueness validation:

```bash
python scripts/ci/check_work_item_uniqueness.py --base origin/main --head HEAD
```

6. Declared required-context validation:

```bash
python scripts/check_declared_check_contexts.py
```

These commands are the designated validation set. Their successful execution is not asserted by this document.

## 9. Verification boundary

The following are not claimed:

- Successful execution of the six local gates.
- Successful GitHub Actions execution.
- Independent review.
- Owner acceptance.
- PR merge.
- Production deployment.

The recorded cancellation counts, run identifiers, pull-request observations, and branch-protection setting are supplied as measured task evidence. Their inclusion does not represent independent remeasurement by this implementation session.
