---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "The counts quoted below were measured in this session at main eb94cab1, not copied from the issue text."
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
    source: null
    en: null
    zh-CN: null
---

You are an author session for a governed repository. Fix issue #904: `approval_scope`
admits exactly one value and still requires three keys.

REPO: oahcom/AiMemoryBrainArchitecture
BASE: origin/main eb94cab11f8d46b1f42d6123656b448b0b710e1e (measured 2026-11-26)

## The defect

Ruling 76 (in #833, comment 7120131295) ordered the two dead keys removed from
`SCOPE_KEYS` AND from the corpus in the same change. #888 removed the values and
left the keys; #833 was then closed. The result is a schema that admits one scope
value and still demands three keys, two of which no rule reads.

Measured at eb94cab1, re-measured rather than taken from the issue text (the issue
says 99 documents; the tree has moved):

| fact | value |
| --- | --- |
| `SCOPE_TYPES` (scripts/check_document_management.py) | {"Full-document"} |
| `SCOPE_KEYS` | {"type", "included_sections", "included_assets"} |
| documents whose frontmatter carries `approval_scope` | 269 |
| of those, carrying `included_sections` | 269 |
| of those, with a non-empty `included_sections` | 0 |
| distinct `type` values | `Full-document` only |
| line forms present | `included_sections: []` and `included_assets: []`, 269 each |

Per root: 00-governance 8, 01-system-architecture 1, 06-memory-context 1,
07-agent-integration 6, 08-bmcp-protocol 1, 10-storage-consistency 1,
14-ai-development 168, docs 83 (docs/en 42, docs/zh-CN 40, docs/governance 1).

## Why the corpus edit is approval-neutral

`body_hash()` hashes `body_text()`, and `body_text()` strips frontmatter before
hashing — its own comment says "An approval binds to document content, not to the
governance metadata." Deleting two frontmatter keys therefore cannot invalidate an
`approved_version` pin.

This was verified, not assumed, on a live `content-hash` document:
14-ai-development/adr/OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001.md, pinned at
3375f59e78a2960c700b9800593c857f263bc3c94438358561d45ceafce2ddc0. Before the edit
the recomputed body hash equals the pin; after removing the two lines it is still
3375f59e78a2960c700b9800593c857f263bc3c94438358561d45ceafce2ddc0. File size fell
16883 -> 16825 bytes, so the deletion really happened.

## What to implement

1. `SCOPE_KEYS = {"type"}`. Any document still carrying a removed key then becomes a
   DM-02 unknown-key error — that is the point: the gate must refuse the shape the
   corpus no longer uses.
2. Delete the two keys from every frontmatter that carries them, in both language
   halves and in every root, with a script that is run and then deleted.
3. Remove what becomes dead: the schema's two field declarations, the DM-03
   "refused when non-empty" loop, the two template placeholders, and the DM-03 policy
   row's sentence about them. Do not rewrite policy prose beyond that.
4. Do not touch anything else.

Order: the gate is red between the two edits locally; the committed tree must be
green, so both land in one commit.

## Verification required

- `check_document_management.py` whole-tree: exits 2 by design (unclassified
  backlog); read the verdict line, report it and the exit code.
- `check_document_management.py --require-changed <base>`.
- `scripts/test_check_document_management.py`, pass count before and after.
- `grep -rc 'included_sections' --include=*.md .` must be 0 outside historical
  records that must keep their original text; list any left alone and say why.
- Mutation: add a test that fails if `SCOPE_KEYS` regains the keys, put them back,
  record the verbatim `AssertionError`, restore, confirm green.

## Work item

AID-2026-104, class GATE/SCHEMA, risk R3, status DISPATCHED, tracking_issue #904,
sponsor/accountable_owner USER-PRINCIPAL-DELEGATED, acceptance_authority NOT_ASSIGNED.
