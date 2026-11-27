---
# provenance: AUTHORED_INDEX
document_metadata:
  domain: "memory-runtime"
  role: "guide"
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
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "provenance: AUTHORED_INDEX"
        - "directory inventory: 05-memory-runtime/"
        - "source branch: session-f-memory-runtime"
        - "source commit: 1908ce4d233b20f7cafd00cb679affd01bd15174"
        - "authoring date: 2026-11-26"
        - "executing operator: user-authorized operator (delegated by account owner)"
        - "no authoritative source; this file is a newly authored index"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "AUTHORED_INDEX; no authoritative source exists; this file is a newly authored navigation index. Owner review pending."
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
      - "documentation-index"
      - "source-provenance"
      - "governance"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "05-memory-runtime/README.md"
    en: null
    zh-CN: "docs/zh-CN/05-memory-runtime/README.md"
---

# Memory Runtime — Directory Index

> **AUTHORED_INDEX — not a restored specification.** No authoritative source exists; this file is a newly authored index. It inventories the documents present in the root directory at the 2026-11-26 inspection and does not establish normative authority or Owner acceptance.

## Documents in this directory

All five source documents are Draft / Candidate / Informative. Their source blobs are pinned to the F Owner branch; bilingual mirrors exist. Exact-version semantic review and F Owner acceptance remain pending.

| Document | Status and pending review | Source blob |
|---|---|---|
| [Runtime Overview](runtime-overview.md) | Candidate; semantic parity and F Owner acceptance pending | `b7a948f014c3ad882a35a18bfc8ce025b26ab85a` |
| [Activation Policy Engine](activation-policy-engine.md) | Candidate; F Owner acceptance and watermark proof pending | `b7f5d85468f5262e472769a1991b812ac4a64f5b` |
| [Retrieval Engine](retrieval-engine.md) | Candidate; exact-version semantic review and F Owner acceptance pending | `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` |
| [Runtime Scheduling](runtime-scheduling.md) | Candidate; exact-version semantic review and F Owner acceptance pending | `ca35d8cddd012c1ff067328ee22177f57c40ae36` |
| [Working Set and Cache](working-set-and-cache.md) | Candidate; exact-version semantic review and F Owner acceptance pending | `a934491950c876701e8ac592a0e6aaea983b44e3` |

## Governance

- This index is a navigation aid only; it does not amend architecture decisions or runtime contracts.
- Candidate / Informative does not mean Approved or Normative.
- A source-branch blob pin proves provenance, not acceptance or production conformance.
- Bilingual mirror presence does not prove semantic equivalence.
- Do not implement unresolved APIs, schemas, budgets or cross-owner decisions from this index.
- Promotion requires F Owner exact-version review and applicable cross-owner/Governance acceptance.

## Missing sources and remaining work

- No authoritative root README source blob was found; this index is newly authored.
- Ten of fifteen F inventory entries lack an existing EN/ZH-CN pair and remain blocked.
- F watermark/scanned-through evidence and exact-version Owner acceptance remain open.
