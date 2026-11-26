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
| Status | CLOSED-BY-RULING (`OWNER-DECISION-RELEASE-BOUNDARY-001`); residue in §7 |
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

---

## 7. Ruling (2026-11-23)

Decision record: `OWNER-DECISION-RELEASE-BOUNDARY-001`. All three questions in §5 are answered, so the §1 closure condition holds.

| Question | Answer | Basis |
|---|---|---|
| 1. Authorized within the current release boundary? | The question has no subject yet — there is no release boundary, so no authorization was required | 11 of 12 crates are `publish = false`, all are `0.1.0`, there are 0 tags, no CHANGELOG, and every intra-workspace dependency is versionless |
| 2. Compatibility layer or deprecation period? | **No** | Zero external callers; a shim would reintroduce the second-lineage-source defect described in §3 |
| 3. What migration notice? | External: none. Internal: already discharged twice, by the function docs and by `65fa040f`'s commit message | As above |

**Category and severity require correction.** §1 records this as `PUBLIC_API_BREAKING_CHANGE` / `DOWNSTREAM COMPILE BREAK`. Both labels presuppose a published surface that has never existed. The correct classification is **in-repo signature change**. The original values are preserved here rather than rewritten in place.

**Two citations in §2 do not survive measurement. They are recorded here, not applied to the original text:**

- "After (PR #707, commit `bbd214f`)": `bbd214f` is PR #707's head and touches eight markdown files with zero `.rs` changes. The signature change is `65fa040f` (2026-11-22 13:36:00 +0800), an ancestor of `bbd214f` within the same PR.
- "Before (base 6418e9c)": the signature at `6418e9c` is indeed the two-parameter form, so the sample is valid — but its date, 2026-11-22 18:35, is **later** than `65fa040f`'s 13:36, because it arrived on the other lineage, which had not yet seen PR #707. The accurate statement is that the two-parameter form holds at `65fa040f^`.

**Residue, not a compatibility question, and not to be closed with this registration:** `crates/bmcp-server/Cargo.toml` declares neither `publish` nor `license`, unlike the other eleven crates. An absent `publish` means publishable; it is blocked today only incidentally, because its only sibling dependency is versionless. D4 requires it to be corrected.

**No new registration.** PR #707 carried a bmcp route, an Evidence field-set change, the deletion of the MC-03 registry and this breaking signature change in 3671 added lines with **0 reviews**, under a title naming only the first. That evidence belongs to `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` and `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008`; per `GAP-27-THE-BACKLOG-IS-NOT-ONE-BACKLOG`, one mechanism does not get a second number.
