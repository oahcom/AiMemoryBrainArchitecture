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
        - "14-ai-development/work-items/AID-2026-115/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Exact-Head CI, merge and post-merge blob readback remain pending."
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
    source: "14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md"
---

# AID-2026-115 — Gate Dispatch Deduplication and Rust CI Cache Evidence

## Purpose and authority

This record documents workflow-level deduplication and job-isolated Rust build caching. It does not change required-check membership, gate commands, checker semantics, job boundaries, or runtime behavior.

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Main baseline: `17bfc43c2b9f2f9c91cb0eb074580141e701c0b3`
- Related Issue: #1212
- Attribution: `user-authorized operator (delegated by account owner)`; delegated execution evidence, not a natural-person Owner signature.
- Allocation: INDEX maximum 109; AID-2026-110 is present on main and AID-2026-111 is reserved by an open PR; AID-2026-115 is the next collision-free ID and remains provisional pending merge-time recheck.

## Observed baseline

Task-supplied measurements: 16 required contexts across eight workflows / 16 jobs, no `needs:`, first-pass wall time 57s; 20 check runs for 16 contexts on the same SHA after four workflows each ran twice, raising wall time to 113s. No workflow-level concurrency or Rust cache existed. Separate Rust builds cost clippy 19s, all-target tests 40s and doctests 21s; doctests took 3s after the same job's target was warmed. Four `fetch-depth: 0` checkouts are load-bearing and remain untouched.

## Workflow concurrency

Eight workflows changed: `bilingual-docs.yml`, `branch-freshness.yml`, `document-management.yml`, `gates.yml`, `repository-hygiene.yml`, `runner-admission-policy.yml`, `rust-phase1.yml`, `session-evidence.yml` (all under `.github/workflows/`).

Each uses this exact policy:

```yaml
group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
cancel-in-progress: true
```

PR head SHA, not `github.ref`, prevents successive pushes to one branch from cancelling each other solely because they share a ref. Non-PR events fall back to `github.sha`. All eight are commit-scoped; no workflow was identified as needing an in-flight run for a superseded SHA preserved, since merge eligibility is evaluated for the current exact PR head.

## Rust cache

Four jobs receive `Swatinem/rust-cache@v2`:

| Job | Existing toolchain | Shared key |
|---|---|---|
| gates / clippy | stable + clippy | gates-clippy |
| gates / fmt | stable + rustfmt | gates-fmt |
| gates / doctest | stable | gates-doctest |
| rust-phase1 / rust-workspace-test | stable + rustfmt | rust-phase1-workspace-test |

After toolchain setup each job records the resolved `rustc --version`. Cache key suffix:

```yaml
key: ${{ hashFiles('Cargo.lock') }}-${{ steps.rust-toolchain-version.outputs.version }}
```

Distinct shared keys isolate each job's target directory; Cargo.lock hash and resolved compiler version invalidate incompatible caches. Existing `stable` selectors are retained, with the actual resolved version captured rather than assumed.

## Explicit job names and protected contexts

- `runner-admission-policy.yml`: id `audit`, explicit `name: audit`.
- `rust-phase1.yml`: id `rust-workspace-test`, explicit `name: rust-workspace-test`.

Each explicit display name matches the existing protected context exactly. ID and display-name fields are independently declared, so a future internal ID rename cannot silently rename the platform context. The 16 protected contexts are unchanged; no branch-protection edit is needed. This removes reliance on GitHub's implicit ID fallback for the emitted check-run name. `check_declared_check_contexts.py` is unchanged.

## Preserved exclusions

No jobs merged; no `fetch-depth` changed; no gate/checker semantics changed; no required context added/removed/renamed; #1212 remains open; no runtime/schema/API/database/deployment changes.

## Performance expectation

Baseline was 113s with duplicate dispatch and 57s for the first-pass 16-context run. Requested planning estimate after duplicate dispatch is eliminated and caches are populated: approximately **38s**. This is an estimate, not a measurement or SLA. Cache hit rate is **NOT YET MEASURED** and must be observed on subsequent exact-head CI.

## Verification ledger

Implementation head, all 16 exact-head results, merge SHA, post-merge blob SHAs and cache-hit observation remain pending at this pre-merge snapshot. No CI success or merge is claimed.
