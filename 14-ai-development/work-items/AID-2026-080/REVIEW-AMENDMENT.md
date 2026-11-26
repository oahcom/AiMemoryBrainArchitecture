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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "The three measurements below were re-run on 2026-11-25 at the branch tip and the numbers are reproduced from those runs. The one thing this record cannot support - that the amended clause was the clause executed - is stated as not supported rather than argued."
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

# Review amendment — AID-2026-080

This file exists because the first attempt to record the amendment put it in the wrong place.

## What went wrong

Round 1 of the governance review returned `ACCEPT WITH AMENDMENTS` and named one blocking
textual defect: the clause did not say which `session_evidence` entry a field could sit in.
The amendment was applied to `PR-GOVERNANCE-001.md`, and a section describing it was **appended
to `prompt-v1.md`**.

`prompt-v1.md` is not a document about the work item. It is the recorded snapshot of the prompt
that was executed, and `session_evidence[0].executed_prompt_sha256` pins its bytes. Appending to
it changed the bytes the pin describes, and the required Session Evidence context failed on the
resulting Head with exactly that diagnostic:

```
MISSING: path '14-ai-development/work-items/AID-2026-080/prompt-v1.md':
executed_prompt_sha256 mismatch in manifest entry #1
```

The first repair attempt made it worse: it re-took the pin to match the amended file. That would
have recorded the amended document as the input that was executed, which it was not. The
reviewing session refused that repair and said why, correctly.

## What is done instead

1. **`prompt-v1.md` is restored byte-for-byte** to the executed snapshot: 9932 bytes, SHA-256
   `08f5e42efdef2c3380056fd8528cf057d6d2a7b25c366566a8599e2aff4df19a`. It is no longer modified
   by this branch at all.
2. **The amendment lives here**, as a separate artifact, so the executed prompt stays the
   executed prompt and the amendment stays identifiable as an amendment.
3. **`prompt_supersession` in the manifest** names the passage the amendment retires, so a session
   reading the pinned snapshot alone is told which part of it no longer states the rule.

## The amendment, verbatim

Applied to `14-ai-development/PR-GOVERNANCE-001.md` §5 item (2), both languages:

- English, before: `The manifest must carry \`sponsor\`, \`accountable_owner\` and \`implementing_ai_session\` as top-level fields at the same time;`
- English, after: `The manifest must carry \`sponsor\`, \`accountable_owner\` and \`implementing_ai_session\` at the same time, each of them either at top level or inside the \`session_evidence\` entries and never in both places;`
- Chinese, before: 「manifest 必须同时在顶层携带 `sponsor`、`accountable_owner` 和 `implementing_ai_session` 三个字段；」
- Chinese, after: 「manifest 必须同时携带 `sponsor`、`accountable_owner` 和 `implementing_ai_session` 三个字段，每个字段或位于顶层、或位于 `session_evidence` 条目内，不得两处并存；」

## Why "either at top level or inside the entries", not "the entry that carries the session"

The reviewer's round-1 suggestion was to identify the entry by its own `implementing_ai_session`
field. Measured against the population, that phrasing does not fit:

1. It is self-referential for `implementing_ai_session`: the field would be defined as living in
   the entry identified by that same field.
2. It says nothing about `sponsor` and `accountable_owner`, which appear inside a
   `session_evidence` entry in no manifest in this repository — they are top-level in 47 and 52
   manifests respectively.
3. It presumes one relevant entry. **AID-2026-055 carries three** `session_evidence` entries and
   three occurrences of `implementing_ai_session`, one per entry. A phrase identifying "the" entry
   is undecidable there.

The reviewer withdrew the suggestion in round 2 and accepted the reasoning: "B1 is closed. The
author was right not to adopt my suggested wording." It also named the distinction the new wording
preserves and the old one obscured: the rule forbids a field occupying **both location classes**;
it does not forbid repeated occurrences **within** the nested class, which the validator requires,
since every entry carries its own `implementing_ai_session`.

## Measurement under the amended wording

55 manifests at the branch tip, with "inside" scoped to the `session_evidence` block and not to any
nested key that happens to share a name:

| result | count | ids |
| --- | --- | --- |
| satisfy the amended clause | 48 | all but the seven below |
| do not satisfy it | 7 | 005, 006, 008, 009, 029 (no `sponsor`, no `implementing_ai_session`); 024, 025 (none of the three) |
| satisfy it and are accepted by `parse_manifest_session_entries` | 21 | the 20 previously conformant manifests plus AID-2026-080 |

The scoping is a correction, not a convenience. An unscoped "appears indented anywhere" test flags
`AID-2026-026`, whose `scope_revision.ownership_unchanged` block restates `sponsor: NOT_ASSIGNED`
while a ruling changes nothing. That is a record about ownership, not a second declaration of the
field, and the clause does not reach it. The unscoped figure would have been 47 and would have been
wrong.

## Limits

- **This file is not the executed prompt.** The executed prompt is `prompt-v1.md`, unmodified, and
  its digest is the one in `session_evidence[0]`. Nothing here is claimed to have been executed.
- **The principal-identity defect in the same paragraph remains open.** No principal registry exists
  in this repository, so nothing can settle whether `accountable_owner` and `implementing_ai_session`
  are different principals. That is a separate defect, deliberately not repaired here.
- **`review.status` is not `APPROVED`.** Round 1 was `ACCEPT WITH AMENDMENTS`, round 2 was
  `NEEDS REVISION` on a different ground — the prompt-snapshot mismatch this file repairs. Whether
  this repair closes round 2 is round 3's decision, at its own Head.
