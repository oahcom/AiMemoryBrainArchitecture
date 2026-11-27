---
document_metadata:
  domain: ai-development
  role: reference
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
        - "14-ai-development/work-items/AID-2026-281/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Composite structured capture of three dispatched prompts. It is not a byte-for-byte platform transcript or a replacement for the original prompt files."
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
      - "prompt-snapshot"
      - "memory-read-authorization-boundary"
      - "complete-scope-read"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-281 Prompt Snapshot

Source: three user-dispatched task prompt files in the AID-2026-281 implementation conversation.  
Capture status: structured composite task capture; not a raw platform transcript.  
Date: 2026-11-27.  
Repository: `oahcom/AiMemoryBrainArchitecture`.  
Branch: `triage-20261127-p0-authz-read-boundary`.  
Base: `main` at `a588cd99`.

## Original dispatched prompt provenance

The following values identify the original dispatched files. They do not identify this composite snapshot.

| Original file | Bytes | SHA-256 |
|---|---:|---|
| `prompt1.md` | 57732 | `fd0a7c79cafcfe214e5f5c54244db03a998b00204bcbe16e9e544e2c205f2186` |
| `prompt2.md` | 6960 | `1592572de7306fad44591f7fc5b9ba50399a24a555ca72e64f4c158583141041` |
| `prompt3.md` | 4626 | `9732c0e14f0d564aa410da5c1575cd268cfc5032ca4e58b3d8a2eebc3d7b522c` |

No SHA-256 or byte count is asserted here for this composite snapshot.

## Task objective

Resolve the SQLite Memory read-boundary defects tracked by:

- #1128 — Filter aggregate MemoryVersion references for partial-Scope readers.
- #1129 — Prevent partial-Scope Memory reads from disclosing hidden Scope membership.
- #1139 — Do not return Scope-filtered content under canonical MemoryVersion identity.

The related but broader authorization issues are:

- #1136 — Require I authorization rather than caller-supplied Scope for Memory reads.
- #1138 — Require I authorization for Event status and payload reads.

The implementation must distinguish a storage disclosure boundary from authentication and I authorization. It must not claim that caller-supplied Scope values prove the caller's identity or authorization.

## Required implementation decision

A canonical `Memory` or `MemoryVersion` is an indivisible stored object. Do not return a filtered or partially reconstructed value under its canonical identity.

For SQLite canonical Memory reads:

1. Validate the requested Scope set.
2. Decode and validate the complete stored Scope set.
3. Require the requested set to cover every stored Scope.
4. Return `StorageError::ScopeMismatch` if the caller's Scope set is incomplete.
5. Return the complete canonical object unchanged if authorization succeeds.

Apply this complete-Scope rule consistently to the SQLite MemoryVersion read path, Memory metadata reads, current-version reads and change-feed records.

Do not solve the defect by returning a partially filtered canonical object. Do not invent a new projection type or projection identity in this task.

## Required regression evidence

Cover at least:

- Partial-Scope denial for canonical `read_current`.
- Partial-Scope denial for canonical `read_version`.
- Partial-Scope denial for `read_memory`, including hidden Scope membership.
- Partial-Scope denial when a MemoryVersion contains Claims in separate Scopes and aggregate entity/relation/source/provenance references and a full-version digest.
- Complete-Scope reads returning the unchanged canonical Memory and MemoryVersion.
- Canonical version identity and digest remaining bound to the same complete content.
- Rejection of a commit whose Claim Scope is outside the commit caller's Scope set.
- Confirmation that a rejected commit did not persist a version, idempotency record or change-feed record.

Rewrite tests whose old expected behavior required partial canonical objects. Do not weaken the complete-Scope disclosure rule to preserve those old assertions.

## Explicit non-goals

Do not implement #1136 in this task:

- No Principal/workload-bound I authorization receipt.
- No new capability proof, permission epoch or policy revalidation.
- No public MemoryStore/MemoryStorage read API signature change.
- No claim that Scope matching authenticates a caller.

Do not implement #1138 in this task:

- No EventStore status or payload read changes.
- No Event read authorization capability.
- No pending-intent, replay, backup or restore authorization changes.

Do not decide the global Principal–Scope–Memory ownership model. Do not transfer I authorization authority or D canonical storage/Forget authority. Do not claim EventStore tests passed if they were not run.

## Execution and reporting requirements

The implementation diff is authored by ChatGPT. The implementing session applies the diff and runs formatting and tests on the user's machine. Record those roles separately.

Record the actual operating system, Rust toolchain, target, build-job setting and compiler environment detail. Distinguish local test output from GitHub Actions results.

Record the exact test commands and observed output. Do not claim CI, independent review, Owner acceptance, merge or post-merge verification unless separately observed.

## Work-item and PR records

Create the AID-2026-281 manifest, evidence record, session-evidence record and this prompt snapshot. Add one INDEX row. The manifest must enumerate the exact changed paths.

Issue disposition must distinguish the three SQLite read-boundary issues addressed by this work from #1136 and #1138, which remain deferred.

Bilingual status must follow the repository's actual governing policy and approved tier classification. Do not infer a Tier 3 classification merely from the absence of a Chinese mirror in a prior work item. Do not claim bilingual completion or an approved exception without evidence.
