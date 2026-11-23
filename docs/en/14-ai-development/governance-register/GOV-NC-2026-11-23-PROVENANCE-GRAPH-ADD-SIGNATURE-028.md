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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "This work record documents a public API signature change and the owner decision it requires; no approval or independent verification is claimed."
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028.md"
---

# GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028 — ProvenanceGraph::add Public API Signature Change

## 1. Registration

| Field | Value |
|---|---|
| Registration ID | GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028 |
| Registration date | 2026-11-23 |
| Category | PUBLIC_API_BREAKING_CHANGE |
| Status | OPEN |
| Severity | DOWNSTREAM COMPILE BREAK |
| Affected component | `memory-domain` (`ProvenanceGraph::add`) |
| Related registration | GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027 |
| Implementation authorization | OWNER DECISION REQUIRED |
| Closure condition | Owner rules on the compatibility policy, and the migration notice and release boundary are fixed |

**Numbering note.** The number `028` is derived as highest-used (027) + 1. It is not issued by the registration process.
Basis: `-027` is the highest number in this directory, and `028` is unoccupied repo-wide and on every remote branch.
If the registration process requires a formally assigned number, replace this one with the process conclusion; the rest of this document is unaffected.

## 2. Change

The public signature of `ProvenanceGraph::add` changes from two arguments to one.

```rust
// Before (base 6418e9c)
pub fn add(
    &mut self,
    provenance: Provenance,
    parents: &[ProvenanceRef],
) -> Result<(), DomainError>

// After (PR #707, commit bbd214f)
pub fn add(&mut self, provenance: Provenance) -> Result<(), DomainError>
```

## 3. Behavioral change

Lineage now comes exclusively from `Provenance.parent_provenance_refs` rather than a caller-supplied `parents` argument.
The entry point now calls `provenance.validate()?`.

Rationale, as recorded in the `provenance_graph.rs` function documentation: with two arguments a caller could declare one lineage on the record and a different one on the graph, and the two sources cannot both be true. The single-argument form removes that conflict.

## 4. Compatibility impact

Downstream callers using the former public signature will no longer compile.

Repository-local compilation and tests establish only that **in-repository** call sites have migrated; they do not establish downstream compatibility.

## 5. Owner decisions required

1. Whether this breaking API change is authorized for the current release boundary.
2. Whether a compatibility layer or deprecation transition is required.
3. What migration notice must accompany the change.

Until the Owner rules explicitly, "in-repository call sites have migrated" must not be written as "public API compatibility has been verified."

## 6. Scope boundary

This registration does not replace or expand
GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027.

027 covers per-element revalidation of the four Provenance reference fields; this registration covers a public signature change and its compatibility authorization.
They are independent and neither absorbs the other.

The change recorded here **is already present in the code of PR #707** (commit `bbd214f`).
This registration does not claim the change is authorized; it records the state "change has occurred, authorization pending."
