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
        - "14-ai-development/work-items/AID-2026-322/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Session provenance is recorded from the current interaction. The operator, not the implementation author, performed the repository measurements and will execute the patches and gates."
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
    canonical_scope: "Session role, actual input and AI-visible implementation output for AID-2026-322."
    canonical_scope_id: "ai-development/aid-2026-322-session-record"
    canonical_scope_keywords:
      - "AID-2026-322"
      - "implementation session"
      - "prompt input"
      - "AI-visible output"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-322 session evidence

## Session role

The implementation content in this work item was authored by a ChatGPT session.

The implementing session is recorded as:

`9router-hermes-aid-322-2026-11-27`

The session authored:

- The implementation ruling and scope disposition.
- The exact manifest repin patches.
- The AID-2026-322 manifest.
- The measurement and historical-value evidence document.
- This session-evidence record.
- The proposed INDEX row.
- The explanatory wording intended for the pull request.

The operator is a mechanical executor. The operator applies the authored blocks verbatim, runs the repository commands and gates, and reports actual results. The operator does not author or silently revise implementation content.

## Actual AI input

The actual AI input is the user-supplied implementation task for AID-2026-322, including:

- The hard constraints and four-file work-item requirement.
- The measured baseline and the operator's raw-byte audit output.
- The 40-entry repin table.
- The three exceptional entries and their provenance facts.
- The historical Issue #1318 description.
- The explicit requirement to preserve prior digest values.
- The required manifest frontmatter and session-evidence shapes.
- The required INDEX row and pull-request evidence format.
- The single-invariant scope restriction.

The operator placed that exact task text in `14-ai-development/work-items/AID-2026-322/prompt-v1.md` and prepended the governance frontmatter. The committed snapshot is therefore the executed message plus that frontmatter, not the raw message. The manifest pins the committed file bytes; provenance remains NOT_VERIFIED. The `__PROMPT_SHA256__` and `__PROMPT_BYTES__` placeholders were replaced by the operator's measurement.

## AI-visible output

The session produced the following implementation artifacts:

1. Forty exact `executed_prompt_sha256` and `executed_prompt_bytes` repin pairs across 36 manifests.
2. A decision to leave AID-2026-186[0], AID-2026-241[0] and AID-2026-261[0] unchanged, with their reasons recorded as findings.
3. A new AID-2026-322 manifest with the required session evidence fields.
4. An evidence document retaining every superseded digest and byte count.
5. A session record describing the author/operator division of responsibility.
6. One new INDEX row.
7. A short explanation distinguishing a committed-byte data repair from restoration of removed approval-scope keys.

The AI-visible output does not constitute proof that the patches have been applied, that any gate has passed, or that the pull request has merged.

## Measurement and execution responsibility

The digest and byte-count values used in the patches were measured by the operator's script against the repository tree at the stated baseline commit.

They were not calculated, independently reproduced, or asserted as raw-byte measurements by the ChatGPT implementation author.

The operator is responsible for mechanically applying the authored patches, running the commands and gates, and reporting their actual output.

The operator must measure the committed bytes of the newly placed `prompt-v1.md` and replace the two placeholders in `manifest.yaml`. This session does not invent those values.

No independent verification, Owner acceptance, CI success, pull-request merge, or post-merge state is claimed by this session.
```

### 4. Required count correction

The 40 repaired entries belong to **34 distinct manifests**. The 36-manifest figure in the original audit includes the two exceptional CRLF manifests, which are deliberately untouched.

Apply these corrections to the newly authored files:

=== PATCH: 14-ai-development/work-items/AID-2026-322/manifest.yaml
```text
--- OLD ---
  Documentation-only data repair. Forty executed-prompt SHA-256 and byte-count
  pairs in 36 existing manifests are corrected against their committed prompt
--- NEW ---
  Documentation-only data repair. Forty executed-prompt SHA-256 and byte-count
  pairs in 34 existing manifests are corrected against their committed prompt
```

=== PATCH: 14-ai-development/work-items/AID-2026-322/manifest.yaml
```text
--- OLD ---
    Forty measured executed-prompt pin pairs across 36 manifests are
    repinned to their committed snapshot bytes.
--- NEW ---
    Forty measured executed-prompt pin pairs across 34 manifests are
    repinned to their committed snapshot bytes.
```

=== PATCH: 14-ai-development/work-items/AID-2026-322/evidence.md
```text
--- OLD ---
The 40 rows above represent 40 entry-level changes in 36 distinct manifests. AID-2026-078 contributes two entries with the same digest and byte count but different issue references and session-evidence references.
--- NEW ---
The 40 rows above represent 40 entry-level changes in 34 distinct manifests. AID-2026-078 contributes two entries with the same digest and byte count but different issue references and session-evidence references.
```

## (d) INDEX.md insertion

The insertion anchor is the existing final table row, AID-2026-280, followed by its blank line. The new row preserves the neighbouring ten-column structure and does not claim a PR number, merge, or acceptance.

=== PATCH: 14-ai-development/work-items/INDEX.md
```text
--- OLD ---
| [AID-2026-280](AID-2026-280/manifest.yaml) | Adjudicate REQ-04 AC8 EXIT-1 / EXIT-2 carrier conflict | USER-PRINCIPAL-DELEGATED | DOC/GOVERNANCE / R1 | DISPATCHED — proxy adjudication B; AC8 remains in scope; no binding Owner scope act or Issue body edit claimed | Reconstructed task snapshot: prompt-v1.md, 3708 bytes, SHA-256 582f797c73360b0b200208af761f3ec511461017f68c288c8c4ecb837c70cd11; NOT_VERBATIM | Decision/evidence/session provenance only; no existing carrier, Issue body, code, workflow, or branch protection changed | NOT_ASSIGNED — independent review not recorded | PENDING — no natural-person Owner acceptance; Issue #265 remains OPEN |

--- NEW ---
| [AID-2026-280](AID-2026-280/manifest.yaml) | Adjudicate REQ-04 AC8 EXIT-1 / EXIT-2 carrier conflict | USER-PRINCIPAL-DELEGATED | DOC/GOVERNANCE / R1 | DISPATCHED — proxy adjudication B; AC8 remains in scope; no binding Owner scope act or Issue body edit claimed | Reconstructed task snapshot: prompt-v1.md, 3708 bytes, SHA-256 582f797c73360b0b200208af761f3ec511461017f68c288c8c4ecb837c70cd11; NOT_VERBATIM | Decision/evidence/session provenance only; no existing carrier, Issue body, code, workflow, or branch protection changed | NOT_ASSIGNED — independent review not recorded | PENDING — no natural-person Owner acceptance; Issue #265 remains OPEN |
| [AID-2026-322](AID-2026-322/manifest.yaml) | Repair 40 executed-prompt digest and byte-count declarations that do not describe their committed snapshots | USER-PRINCIPAL-DELEGATED | DOC/GOVERNANCE / R1 | PR_OPEN — Issue #1318; 40 nested execution pins corrected across 34 manifests; three exceptional entries retained as findings; no merge or acceptance claimed | AID-2026-322-PROMPT v1 — prompt-v1.md; provenance NOT_VERIFIED; committed-byte digest and size to be measured by operator | DOCUMENTATION-ONLY DATA REPAIR — 40 manifest field pairs and one INDEX row; no prompt snapshot, checker, workflow, schema, policy or approval-scope change | NOT_ASSIGNED — independent exact-Head review not recorded | PENDING — no Owner acceptance asserted; #1318 remains OPEN |

