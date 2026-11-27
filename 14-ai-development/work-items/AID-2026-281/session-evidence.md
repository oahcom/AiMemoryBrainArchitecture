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
        - "14-ai-development/work-items/AID-2026-281/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Session provenance and locally observed test results are recorded from the implementing session report. No platform transcript hash is asserted for this composite capture."
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
      - "session-evidence"
      - "memory-read-authorization-boundary"
      - "implementation-provenance"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Session Evidence — AID-2026-281

## Session role / use case

Implementation work for the SQLite Memory read-boundary defects tracked by #1128, #1129 and #1139, with #1136 and #1138 explicitly retained as deferred work.

ChatGPT authored the implementation diff and the follow-up test corrections. The implementing session on the user's Windows machine applied the diff, ran formatting and tests, and supplied the observed outputs recorded in `evidence.md`.

ChatGPT conversation ID:

`6b090b5d-f3d0-83e8-96c7-d293f2a475bd`

The conversation was used for design, patch authoring, follow-up correction and this work-item record authoring.

## Actual AI input

Three task prompt files were dispatched. Their byte counts and SHA-256 values are recorded exactly as supplied:

| Dispatched file | Bytes | SHA-256 |
|---|---:|---|
| `prompt1.md` | 57732 | `fd0a7c79cafcfe214e5f5c54244db03a998b00204bcbe16e9e544e2c205f2186` |
| `prompt2.md` | 6960 | `1592572de7306fad44591f7fc5b9ba50399a24a555ca72e64f4c158583141041` |
| `prompt3.md` | 4626 | `9732c0e14f0d564aa410da5c1575cd268cfc5032ca4e58b3d8a2eebc3d7b522c` |

`prompt-v1.md` is a structured composite capture of the task and prompt provenance. It is not represented as a byte-for-byte copy of any of the three dispatched prompt files. The three hashes above refer only to the original dispatched files, not to `prompt-v1.md`.

The task covered the five issues #1128, #1129, #1136, #1138 and #1139. It required an explicit read-boundary decision, preservation of canonical stored bytes, regression coverage, no unauthorized broadening into EventStore or I authorization implementation, and work-item evidence.

## AI-visible output

ChatGPT authored a diff confined to:

`crates/memory-storage-sqlite/src/lib.rs`

The diff adds `scope_allowed_complete()`, validates both requested and stored Scope sets, requires complete Scope coverage, removes in-place Claim filtering from canonical MemoryVersion reads, and applies complete-Scope authorization to the relevant SQLite Memory read and change-feed paths.

ChatGPT also authored the corrected test changes. The implementing session applied the diff and corrected the ownership issue in the test by borrowing `first_scope` for `list_changes` using `std::slice::from_ref(&first_scope)`.

The resulting source diff reported by the implementing session is +249 / -38 in the one changed Rust file.

## Implementing environment and toolchain

The implementing machine was Windows, using:

- `rustc 1.100.0`
- target `x86_64-pc-windows-gnu`
- `CARGO_BUILD_JOBS=2`

`CC` was set to the WinLibs mingw64 GCC because the default `gcc.exe` wrapper did not have a working `cc1` component. No exact filesystem path is asserted in this record because none was supplied in the session evidence.

The implementing session ran:

- `cargo fmt --all`
- `cargo test -p memory-storage-sqlite`
- `cargo test -p memory-store`
- `cargo test -p memory-context`
- `cargo test -p brain-cli`
- six focused SQLite regression-test commands recorded in `evidence.md`

All observed results are recorded in `evidence.md`. `cargo test -p memory-event-store-sqlite` was not run after the change.

## Execution and authority boundaries

The local commands were run by the implementing session on the user's machine. They are not GitHub Actions results.

No CI check result, independent review, Owner acceptance, issue closure, merge, or post-merge verification is claimed by this session record.

The session did not implement #1136 or #1138. It did not add Principal-bound I authorization receipts, alter public Memory read API signatures, change EventStore behavior, or decide the global Principal–Scope ownership model.
