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
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "16/16 exact-head required contexts succeeded; 15/15 post-merge blob SHAs match the merged PR head; cache hit rate remains pending next CI cycle."
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
- Main baseline: `8722a37b0cd72dc550d99c0eaebe9e7556ce2f95`
- Related Issue: #1212
- Attribution: `user-authorized operator (delegated by account owner)`; delegated execution evidence, not a natural-person Owner signature.
- Final base recheck: INDEX maximum AID-2026-114; AID-2026-110 through AID-2026-114 are present on main, AID-2026-116 is occupied by an open PR, and AID-2026-115 remains uniquely reserved by PR #1322. The provisional AID-2026-112 collided and was renumbered to AID-2026-115. Final carrier: PR #1322.

## Observed baseline

Task-supplied measurements: 16 required contexts across eight workflows / 16 jobs, no `needs:`, first-pass wall time 57s; 20 check runs for 16 contexts on the same SHA after four workflows each ran twice, raising wall time to 113s. No workflow-level concurrency or Rust cache existed. Separate Rust builds cost clippy 19s, all-target tests 40s and doctests 21s; doctests took 3s after the same job's target was warmed. Four `fetch-depth: 0` checkouts are load-bearing and remain untouched.

## Workflow concurrency

Eight workflows changed: `bilingual-docs.yml`, `branch-freshness.yml`, `document-management.yml`, `gates.yml`, `repository-hygiene.yml`, `runner-admission-policy.yml`, `rust-phase1.yml`, `session-evidence.yml` (all under `.github/workflows/`).

Seven workflows use this exact policy with `cancel-in-progress: true`:

```yaml
group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
cancel-in-progress: true
```

`session-evidence.yml` uses the same group expression with `cancel-in-progress: false`. Its validator also runs on PR-body `edited` events; multiple body revisions can share one head SHA. Letting an in-flight validation finish preserves the body-digest evidence for each revision instead of cancelling the earlier record. The other seven workflows cancel duplicate in-flight work for the same exact SHA. PR head SHA, not `github.ref`, prevents successive pushes to one branch from cancelling each other solely because they share a ref; non-PR events fall back to `github.sha`.

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

## PR declaration formatting

The PR description's `Work Item ID` field is the standalone value `AID-2026-115`; the provisional status is in a separate section. The per-Issue mapping for historical Issue #1212 is `LEGACY_UNDECLARED` / `N/A`. This matches the Session Evidence validator's field and legacy-issue contract; no validator semantics were changed.

## Post-merge verification

- Implementation PR: [#1322](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1322)
- Merge commit: `ac301e09799bcc094e015db4e12d2e6ff53d5010`
- Merged PR head: `eaf381a9af28ebf86e7ee094f60adaaacc0d97ca`
- Exact-head required checks: **16/16 SUCCESS**, one check-run per required context.
- Post-merge main blob readback: **15/15 paths match** the PR-head blob SHA.
- Issue #1212 comment: `7194114609`; Issue remains OPEN.
- Cache hit rate: **NOT YET MEASURED**; observe the next CI cycle.

### Required contexts

| Required context | Conclusion |
|---|---|
| Rust format (hard gate) | SUCCESS |
| Schema non-empty audit (hard gate) | SUCCESS |
| BMCP protocol index (hard gate) | SUCCESS |
| Rust doctests (hard gate) | SUCCESS |
| Bilingual docs coverage (ratchet) | SUCCESS |
| BMCP conformance suite (hard gate) | SUCCESS |
| Rust clippy (hard gate) | SUCCESS |
| Branch freshness vs base | SUCCESS |
| Session Evidence | SUCCESS |
| rust-workspace-test | SUCCESS |
| Session Evidence self-test (head) | SUCCESS |
| GOV-DOC-002 metadata checks | SUCCESS |
| GOV-DOC-001 structural checks | SUCCESS |
| Repository hygiene (hard gate) | SUCCESS |
| Session Evidence self-test (base) | SUCCESS |
| audit | SUCCESS |

### Post-merge blob readback

| Path | Main blob SHA |
|---|---|
| `.github/workflows/bilingual-docs.yml` | `48c3c88b3899cdf7e10a41d2dac24f8dd820b9e0` |
| `.github/workflows/branch-freshness.yml` | `811370424c7f8d3738a8eaba8f0fd7adfe4f49a8` |
| `.github/workflows/document-management.yml` | `4d49e5d0cd87a395e3f948130be6fe35ce982266` |
| `.github/workflows/gates.yml` | `5844f50c14c63d82864a31503961273cc65a9c77` |
| `.github/workflows/repository-hygiene.yml` | `a11d2a06ac5c23d5f2e51c3a5efb3b0e29c3513b` |
| `.github/workflows/runner-admission-policy.yml` | `82938387a6c1c3acbecd193a70747af50690a731` |
| `.github/workflows/rust-phase1.yml` | `0674e5c40ae4fb0e7fe9df92f6a0504ffbdd3ee0` |
| `.github/workflows/session-evidence.yml` | `8fe7dfa2b02d200f273d8bba6be542cf02d9686c` |
| `14-ai-development/work-items/INDEX.md` | `54134d33919f0c26b7a3ab66f488847a376ede00` |
| `14-ai-development/work-items/AID-2026-115/manifest.yaml` | `6f7cba141f644cad8bbaeb0445430ea976563dd8` |
| `14-ai-development/work-items/AID-2026-115/prompt-v1.md` | `15f98b3702f5b3e69337c98f3ca5dd55c1357ed2` |
| `14-ai-development/work-items/AID-2026-115/session-evidence.md` | `8ecc2a8cf69a82a941ce56737134a34b425697da` |
| `14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md` | `9b4dbadc0a9f61ec0b8be5ff274f42a7549fc781` |
| `docs/en/14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md` | `ad350a1e087ca3e85bee1bcdb63a6f655e35e657` |
| `docs/zh-CN/14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md` | `009ec330f4a4d8fc8fb8f57d4094bdc562bb5dcb` |

## Verification ledger

Implementation head, all 16 exact-head results, merge SHA, post-merge blob SHAs and cache-hit observation remain pending at this pre-merge snapshot. No CI success or merge is claimed.
