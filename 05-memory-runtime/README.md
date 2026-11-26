---
# provenance: AUTHORED_INDEX
document_metadata:
  domain: memory-runtime
  role: guide
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "provenance: AUTHORED_INDEX"
        - "directory source inventory: 05-memory-runtime/"
        - "source branch: session-f-memory-runtime"
        - "source commit: 1908ce4d233b20f7cafd00cb679affd01bd15174"
        - "authoring date: 2026-11-26"
        - "executing operator: user-authorized operator (delegated by account owner)"
        - "authoritative README source blob: NOT_FOUND; this file is a newly authored index"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Created under delegated documentation-only authority; independent review and domain Owner acceptance remain pending."
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
    canonical_status: Candidate
    canonical_scope: "Newly authored navigation index for existing Memory Runtime candidate documents; not a recovered source specification"
    canonical_scope_id: "memory-runtime/directory-index"
    canonical_scope_keywords:
      - documentation-index
      - source-provenance
      - governance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/05-memory-runtime/README.md"
    zh-CN: "docs/zh-CN/05-memory-runtime/README.md"
---

# Memory Runtime — Directory Index

> **AUTHORED_INDEX — not a restored specification.** 无权威源，本文件为新建索引。 No authoritative source blob for a root `README.md` was located. This file only inventories the documents present in this directory at the 2026-11-26 branch-tree inspection; it does not establish normative authority, resolve conflicts, or grant Owner acceptance.

## Documents present in this directory

All five documents below are **Draft / Candidate / Informative**. Their source blobs are pinned to the F Owner branch; bilingual EN/ZH-CN mirrors are present. Exact-version semantic review, F Owner acceptance, and watermark/scanned-through evidence remain pending.

| Document | Current disposition | Source evidence | Bilingual mirrors |
|---|---|---|---|
| [Runtime Overview](runtime-overview.md) | Candidate; semantic parity and F Owner acceptance pending | `session-f-memory-runtime@1908ce4d233b20f7cafd00cb679affd01bd15174`; source blob `b7a948f014c3ad882a35a18bfc8ce025b26ab85a` | [EN](../docs/en/05-memory-runtime/runtime-overview.md) · [ZH-CN](../docs/zh-CN/05-memory-runtime/runtime-overview.md) |
| [Activation Policy Engine](activation-policy-engine.md) | Candidate; F Owner acceptance and watermark proof pending | source blob `b7f5d85468f5262e472769a1991b812ac4a64f5b` | [EN](../docs/en/05-memory-runtime/activation-policy-engine.md) · [ZH-CN](../docs/zh-CN/05-memory-runtime/activation-policy-engine.md) |
| [Retrieval Engine](retrieval-engine.md) | Candidate; exact-version semantic review and F Owner acceptance pending | source blob `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` | [EN](../docs/en/05-memory-runtime/retrieval-engine.md) · [ZH-CN](../docs/zh-CN/05-memory-runtime/retrieval-engine.md) |
| [Runtime Scheduling](runtime-scheduling.md) | Candidate; exact-version semantic review and F Owner acceptance pending | source blob `ca35d8cddd012c1ff067328ee22177f57c40ae36` | [EN](../docs/en/05-memory-runtime/runtime-scheduling.md) · [ZH-CN](../docs/zh-CN/05-memory-runtime/runtime-scheduling.md) |
| [Working Set and Cache](working-set-and-cache.md) | Candidate; exact-version semantic review and F Owner acceptance pending | source blob `a934491950c876701e8ac592a0e6aaea983b44e3` | [EN](../docs/en/05-memory-runtime/working-set-and-cache.md) · [ZH-CN](../docs/zh-CN/05-memory-runtime/working-set-and-cache.md) |

## Governance and use

- This README is a navigation aid only. It does not amend any source contract or architecture decision.
- `Candidate` and `Informative` are not synonyms for Approved or Normative.
- A source-branch blob pin establishes provenance, not current acceptance or production conformance.
- Bilingual mirror presence does not by itself prove semantic equivalence.
- Do not implement unresolved callable APIs, schemas, budgets, or cross-owner decisions from this index.
- Any promotion requires the relevant F Owner's exact-version review and applicable cross-owner/Governance acceptance.

## Missing source and remaining work

- No authoritative root README source blob was found; this file is newly authored as an index.
- F inventory remains **5/15** source-backed root candidates represented in this batch; the other ten lack an existing bilingual pair in the inspected tree and remain blocked.
- Watermark/scanned-through proof and exact-version Owner acceptance remain open.
