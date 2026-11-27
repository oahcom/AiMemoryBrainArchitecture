---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Version 1 task input recorded as supplied; this metadata does not assert implementation acceptance, independent review, or merge authorization."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Task input prompt version 1 for AID-2026-212"
    canonical_scope_id: "ai-development/aid-2026-212-prompt-v1"
    canonical_scope_keywords:
      - "task-input"
      - "prompt-v1"
      - "blob-pin-integrity"
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-212 — Executed implementation prompt

## Objective

Implement Issue #1350, blob-pin integrity verification, and repair the
missing gate identified by Issue #1349.

Repository:
oahcom/AiMemoryBrainArchitecture

Baseline:
4fa75e7809a9319db2ab04489cc8f2f9e17fbd79

## Required implementation

1. Add scripts/governance/session_evidence/blob_pins.py.
2. Keep it independent of HTTP and GitHub implementation details.
3. Use only the Python standard library.
4. Enumerate digest-bearing fields dynamically.
5. Bind digest fields to deterministic sibling path keys.
6. Support the explicit d_source_blobs list representation.
7. Reject digest-only and path-only declarations.
8. Resolve all candidate pins against the exact PR Head tree.
9. Recompute Git blob SHA-1 from original bytes.
10. Compare SHA-256 declarations against original bytes.
11. Allow historical references only through an explicitly declared
    and verifiable source commit.
12. Reject unavailable commits, incomplete trees, missing paths,
    malformed digests and corrupted bytes.
13. Cache repeated blob reads.
14. Add check 12 after existing check 11.
15. Do not alter existing check semantics.
16. Add adversarial offline tests and mutation assertions.

## Required security distinctions

A Git tree entry binds a path to a Git object identity. Recomputing
the Git blob identity from the returned bytes independently establishes
that the retrieved content is the same object. Both checks are required.

SHA-256 fields are content digests, not Git object identifiers.
They must be recomputed from the original bytes.

Historical source pins are not blanket exemptions. The only supported
historical form is d_source_blobs with a sibling d_source_commit.
A mutable branch name alone does not authorize bypassing candidate-tree
validation.

## Required acceptance cases

- Valid path plus digest.
- Digest without path.
- Path without digest.
- Digest differing by one character.
- Missing committed path.
- Mutated returned bytes.
- Valid SHA-256 pin.
- Manifest without blob pins.
- Unrelated non-pin fields.
- Historical source with exact source commit.
- Historical source without source commit.
- Duplicate reads use the cache.

## Work Item

AID-2026-212

Owning issue:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1350

Issue #1349 is the defect-origin reference, not a second carrier issue.

## Execution record

This snapshot records the task-specific implementation requirements.
The exact final snapshot bytes are measured after all edits and before
the candidate commit.

SHA-256: __PROMPT_SHA256__
Bytes: __PROMPT_BYTES__
