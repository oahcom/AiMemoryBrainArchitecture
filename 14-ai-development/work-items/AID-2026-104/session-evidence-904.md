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
      last_verification_note: "Every count, hash and exit code below was produced by a command run against this branch, based on origin/main eb94cab1, on 2026-11-26."
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

# Session evidence — AID-2026-104 (issue #904)

## Session role / use case

IMPLEMENTER. This session removed `approval_scope`'s two permanently-empty keys from
`SCOPE_KEYS`, from the schema, from the template, from the DM-03 policy row, and from
every governed frontmatter that carried them. It did not change `SCOPE_TYPES`, the
DM-10 body-hash equivalence, or any other rule.

## Actual AI input

The assignment, abridged only where it repeated repository context:

> `approval_scope` admits exactly one value and still requires three keys. Ruling 76 (in
> #833, comment `7120131295`) ordered the two dead keys removed from `SCOPE_KEYS` **and**
> from the corpus in the same change. #888 removed the values and left the keys.
>
> Frontmatter edits are approval-neutral by construction: `body_hash()` hashes
> `body_text()`, and `body_text()` strips frontmatter before hashing. **Verify this on a
> live document** rather than asserting it: take one document with a `content-hash`
> scheme, record its pin, delete the keys, recompute, show the pin still matches.
>
> **Order matters**: the committed tree must be green — commit both together.

## AI-visible output

The diff to `scripts/check_document_management.py`,
`scripts/test_check_document_management.py`,
`00-governance/architecture-document-metadata.schema.yaml`,
`00-governance/templates/document-metadata-template.md`,
`00-governance/architecture-document-management-policy.md`, 269 documents' frontmatter,
the three files in this directory, one row appended to
`14-ai-development/work-items/INDEX.md`, and the pull request that carries them.

## 1. Re-measured counts at `eb94cab1`

The issue text says 99 documents. The tree has moved, so the count was taken again
before it was relied on:

```
documents with approval_scope               269
of those, carrying included_sections        269
of those, with a non-empty included_sections  0
distinct approval_scope.type values         Full-document only
line forms present                          included_sections: []   x269
                                            included_assets: []     x269
```

Per root: `00-governance` 8, `01-system-architecture` 1, `06-memory-context` 1,
`07-agent-integration` 6, `08-bmcp-protocol` 1, `10-storage-consistency` 1,
`14-ai-development` 168, `docs` 83 (`docs/en` 42, `docs/zh-CN` 40, `docs/governance` 1).

After the deletion, the same scan reports `docs with included_* in frontmatter: 0`.

## 2. Approval neutrality, measured on a live document

Document: `14-ai-development/adr/OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001.md`,
`scheme: content-hash`, pin
`3375f59e78a2960c700b9800593c857f263bc3c94438358561d45ceafce2ddc0`.

Measured on the two blobs rather than on a simulation: the file as it stands at
`71548b7b`, and the file as it stands in this commit.

```
before(eb94cab1): scheme=content-hash pin=3375f59e78a2960c700b9800593c857f263bc3c94438358561d45ceafce2ddc0
before(eb94cab1): body_hash=3375f59e78a2960c700b9800593c857f263bc3c94438358561d45ceafce2ddc0 matches=True bytes=16883
after (HEAD)    : scheme=content-hash pin=3375f59e78a2960c700b9800593c857f263bc3c94438358561d45ceafce2ddc0
after (HEAD)    : body_hash=3375f59e78a2960c700b9800593c857f263bc3c94438358561d45ceafce2ddc0 matches=True bytes=16825
pin unchanged across the edit: True
body_hash unchanged across the edit: True
both match the recorded pin: True
byte delta: -58
```

The hash is unchanged and the byte count fell by 58, so the deletion really happened and
the pin did not move. This is what makes the corpus edit approval-neutral: it is a
property of `body_text()`, which returns the document with its frontmatter removed, and
of `body_hash()`, which hashes that.

## 3. What was removed

- `scripts/check_document_management.py`: `SCOPE_KEYS` is `{"type"}`; the DM-03 loop
  that refused a non-empty `included_sections` / `included_assets` is deleted. With the
  keys no longer in `SCOPE_KEYS`, that loop's condition is unreachable — the
  unknown-key check fires first on any document that carries them — so it cannot be
  tested except by reintroducing the keys, which `T94 SCOPE_KEYS admits only 'type'`
  refuses. That is why no separate test guards the deleted loop.
- `00-governance/architecture-document-metadata.schema.yaml`: the two field
  declarations under `approval_scope`.
- `00-governance/templates/document-metadata-template.md`: the two placeholder lines.
- `00-governance/architecture-document-management-policy.md`: the DM-03 row's sentence
  about the two keys, replaced by one that states they were removed and why. Change-log
  rows 1.11 and 1.21 are **not** edited: they record what was true at their own date.

## 4. The mutation

`T94` cases were added to `scripts/test_check_document_management.py`. With
`SCOPE_KEYS` edited back to `{"type", "included_sections", "included_assets"}`, the suite
exits 1 and prints:

```
approval scope keys (#904)
  [FAIL] T94 a document carrying included_sections is refused  AssertionError: a document carrying included_sections was accepted by the gate
  [FAIL] T94 a document carrying included_assets is refused  AssertionError: a document carrying included_assets was accepted by the gate
  [FAIL] T94 a non-empty included_sections is refused, not reinterpreted  AssertionError: a document carrying included_sections was accepted by the gate
  [FAIL] T94 SCOPE_KEYS admits only 'type'  AssertionError: SCOPE_KEYS readmits ['included_assets', 'included_sections']; #904 removed those keys from the corpus in the same change
  [ok  ] T94 the corpus shape (type only) is still accepted
321/326 passed
EXIT=1
```

Each failure is an `AssertionError` with a message, not a traceback. The mutation also
turns `T19 every gate-accepted field is declared in the schema` red
(`undeclared: lifecycle.approval.approval_scope.included_assets,
lifecycle.approval.approval_scope.included_sections`), which is the schema half of the
same coupling. Restored, the suite is `326/326 passed`.

## 5. Test counts

```
before   324/324 passed, 1 skipped (T68c, registered)
after    326/326 passed, 1 skipped (T68c, registered)
```

Two net new cases. Three `T87` cases asserted the old non-empty behaviour and its empty
placeholder; they were deleted with the rule they tested. Five `T94` cases replaced them:
three refusals, the `SCOPE_KEYS == {"type"}` guard, and a control proving the corpus shape
is still accepted. 324 - 3 + 5 = 326.

## 6. Gate verdicts

```
whole-tree, before   INCOMPLETE: no rule violations in 362 classified documents, but 466
                     governed documents are still unclassified            exit 2
whole-tree, after    INCOMPLETE: no rule violations in 364 classified documents, but 466
                     governed documents are still unclassified            exit 2
incremental          --require-changed eb94cab1                            exit 0
bilingual            check_bilingual_docs.py with PR_BODY                 exit 0
                     278 changed paths, 21 exemptions, 0 new gaps
traceability         check_traceability.py --index-only                   exit 2
                     INCOMPLETE: 0 errors / 85 warnings — the same exit 2 and
                     the same 0-error class as the base, which reports
                     0 errors / 84 warnings. The one added warning is T-05 on
                     this work item's own `tracking_issue: "#904"`, identical
                     in kind to the 15 others in the file.
```

Exit 2 is the designed verdict for the unclassified backlog, not a regression. The
classified count rises by two because this work item adds two classified documents
(`prompt-v1.md`, `session-evidence-904.md`); the unclassified backlog is unchanged at
466, so no document moved out of the backlog as a side effect of the edit.

The incremental run over the change is `exit 0`. Before `prompt-v1.md` carried a
frontmatter block the same run was `exit 1` with
`DM-01 missing document_metadata block: .../prompt-v1.md` — recorded here because it is
the one moment the gate refused something this change introduced.

## 7. What this record does not claim

- It does not claim the 254-document count will stay true. It is a measurement at
  `eb94cab1`, and the count has already moved repeatedly
  (99 -> 202 -> 231 -> 246 -> 252 -> 254 -> 266 -> 269).
- It does not claim the change-log rows 1.11 and 1.21 are wrong. They are dated records
  and were left unedited on purpose.
- It does not claim review. No independent review is recorded; this manifest and this
  record were written by the session that made the change.
- `executed_prompt_provenance` is `NOT_VERIFIED`: the prompt was assembled from the
  assignment and the same measurements, but was not re-read line by line against the
  final diff.
