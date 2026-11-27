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
      last_verified_date: "2026-11-25"
      last_verification_note: "The verdict reproduced below is the reviewing session's own text, extracted byte-for-byte from its reply and not summarised. The disposition in section 3 states what was changed in response and what was not."
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

# Independent governance review — AID-2026-080, round 1

## 1. What was reviewed, by whom, at which Head

| item | value |
| --- | --- |
| Pull request | #1215, branch `gov/aid-079-s5-location` |
| Base | `bc1d09aa222c6f805ab5d9145a58887ca3ed7cfe` |
| Exact Head reviewed | `a538dbf289cb21fc04a03fb412c90482619187bc` |
| Reviewer | a separate ChatGPT conversation, `6b07448b-ac9c-83ec-9115-f056a313f972` |
| Independence basis | `PR-GOVERNANCE-001.md` §5, session-level: the reviewing session did not write or implement the change, and read the artifacts from the repository at that Head through its own GitHub connector rather than from this session's account of them |
| Same GitHub identity | yes, `oahcom`; §5 states identity is the carrier and independence is decided by the session |

The reviewing session read, by its own calls at `a538dbf2`: `14-ai-development/PR-GOVERNANCE-001.md`,
`AID-2026-071/manifest.yaml`, `AID-2026-075/manifest.yaml`, `INDEX.md`, `AID-2026-080/manifest.yaml`,
`AID-2026-080/prompt-v1.md`, `AID-2026-080/session-evidence-1201.md`,
`scripts/governance/session_evidence/validate.py`, `GET /repos/.../pulls/1215`, and
`pull/1215.diff`. The verdict below is therefore of the artifacts, not of the request.

This review is required, not optional: §9 requires an exact-Head governance review for changes
to this standard, and the paragraph's own closing sentence makes it exemptible only by an
exception record that names the paragraph. None exists, so this review cannot be an exemption.

## 2. Verdict, verbatim

The following is the reviewing session's reply, unedited. Nothing is summarised, reordered or
trimmed; the disposition in section 3 follows it.

```text
VERDICT: ACCEPT WITH AMENDMENTS

HEAD REVIEWED: a538dbf2 (`a538dbf289cb21fc04a03fb412c90482619187bc`)

## 1. Satisfiable and non-vacuous

**FINDING: PASS, with an important distinction between parser acceptance and complete gate execution.**

The new wording admits a concrete conforming shape:

```yaml
sponsor: USER-PRINCIPAL-DELEGATED
accountable_owner: USER-PRINCIPAL-DELEGATED

session_evidence:
  - role: IMPLEMENTER
    implementing_ai_session: session-r45-coordinator
    # remaining required evidence fields
```

This is the shape actually used by AID-2026-071.

It satisfies the three-field presence and single-location requirements. The `parse_manifest_session_entries` implementation accepts this structure.

The alternative is also permitted by the wording: all three fields at top level, provided no conflicting nested occurrence exists. However, that legacy shape must additionally satisfy the validator's seven-field legacy requirements.

Non-vacuity is preserved. A manifest missing `sponsor`, `accountable_owner`, or `implementing_ai_session` violates the clause.

Concrete examples from the measured population:

- AID-2026-071: satisfies the corrected clause.
- AID-2026-075: satisfies the corrected clause.
- AID-2026-024 and AID-2026-025: do not satisfy it because the required names are absent.

**Evidence limitation:** The supplied measurements establish acceptance by `parse_manifest_session_entries`, not independently a successful end-to-end execution of the entire required status context against these examples. Those are different evidentiary claims.

This limitation does not negate the demonstrated structural satisfiability.

## 2. Obligation preserved

**FINDING: PASS.**

All five obligations survive the modification.

| Obligation | Finding |
|---|---|
| Presence of all three names | Preserved |
| `sponsor` and `accountable_owner` may identify the same principal | Preserved |
| `accountable_owner` and `implementing_ai_session` must identify different principals | Preserved |
| Textual difference does not establish independence | Preserved |
| Principal identity determines independence | Preserved |

The English and Chinese modifications change placement constraints, not identity constraints.

In particular, the replacement does not introduce a weaker rule under which different strings automatically establish different principals.

The old top-level-only requirement is removed, but the three-field presence requirement is not.

## 3. Ambiguity introduced

**FINDING: PASS WITH A CLARIFICATION RECOMMENDED.**

The three requested cases:

**(a) `sponsor` at top level with a `session_evidence` block present**

Permitted.

The rule says each field must occur in exactly one place. It does not require every field to be nested merely because the block exists.

A top-level `sponsor` therefore satisfies the location rule, provided there is no second occurrence inside the block.

**(b) `implementing_ai_session` inside the second of two `session_evidence` entries**

Permitted if that second entry is the entry carrying the relevant implementing session.

The wording does not require the first entry to carry it.

However, there is a minor drafting weakness: the standard does not explicitly define how to identify the relevant entry when a manifest contains multiple session entries.

A more mechanically precise expression would identify the entry by its `implementing_ai_session` field.

**(c) The same name at top level and inside the block**

Prohibited.

Both languages expressly require exactly one occurrence and expressly prohibit coexistence.

The wording is sufficiently understandable for ordinary cases. Nevertheless, the phrase identifying the session-bearing entry should be tightened to remove uncertainty in multi-entry manifests.

Suggested clarification:

> the `session_evidence` entry containing the corresponding `implementing_ai_session` field

The clarification should be applied consistently in both languages.

This is a drafting improvement, not evidence that the central correction fails.

## 4. Bilingual parity

**FINDING: PASS.**

The three negative constraints have equivalent force.

| English | Chinese | Finding |
|---|---|---|
| and not both | 不得两处并存 | Equivalent prohibition |
| each of them in exactly one place | 每个字段只能出现于一处 | Equivalent cardinality |
| top level, or the `session_evidence` entry | 顶层，或承载该会话的 `session_evidence` 条目内 | Equivalent alternatives |

Neither language permits duplication.

Neither language requires all three fields to occupy the same location.

Neither language silently removes the requirement that all three names exist.

The Chinese version is not weaker than the English version.

The recommended clarification in section 3 should nevertheless be mirrored.

## 5. Scope discipline

**FINDING: PASS.**

Neither omission constitutes a defect of this change.

**Executable files**

The standard is being corrected to agree with the existing validator.

The validator's exclusion rule explicitly prevents two independently mutable sources of truth.

Changing that validator to accommodate the previous normative wording would reverse the proper direction of correction.

The PR's decision not to modify `scripts/`, `.github/`, `tests/`, or `crates/` is appropriate.

**Principal-identity defect**

This is a separate unresolved requirement.

The existing paragraph requires principal identity to determine independence, rather than string inequality.

The absence of a principal registry prevents mechanical resolution of that requirement.

Removing or weakening that requirement would be a separate normative decision.

Keeping it intact while registering the implementation problem separately is appropriate scope discipline.

The remaining defect must not be interpreted as resolved by this PR.

## 6. Honesty of the retired-statement annotations

**FINDING: PASS.**

The annotations are adequate.

**AID-2026-071**

The historical deviation statement remains, but the subsequent dated annotation explicitly says that the earlier belief was wrong and identifies the corrected requirement.

It does not leave the old statement standing as current compliance guidance.

**AID-2026-075**

The historical deviation and C2 are explicitly superseded.

Importantly, C2 now states the corrected criterion and explicitly withdraws the previous top-level-only interpretation.

The pinned `prompt-v1.md` is not silently rewritten. Its superseded passage is identified through `prompt_supersession`.

That preserves historical bytes without treating the obsolete instruction as authoritative.

**INDEX.md**

The current cell explicitly identifies the superseded requirement and states that the manifest satisfies the corrected clause.

It does not continue presenting the old deviation as current.

The distinction between preserving historical evidence and preserving an operative instruction is sufficiently clear.

## 7. Anything else that blocks merge

**FINDING: No additional substantive defect established.**

Two governance conditions deserve explicit attention.

1. The standard's approval metadata remains `Pending-Reapproval`. The change does not silently refresh the previous approval. That is correct, but subsequent adoption must respect the applicable reapproval procedure.
2. The new work item's `review.status` is `NOT_ASSIGNED`. That is not evidence of an independent review. This review supplies the requested exact-Head assessment, but its actual recording and acceptance remain separate governance actions.

The PR's stated local `check_declared_check_contexts.py` result is INCOMPLETE because of HTTP 403. It must not be represented as PASS.

The PR metadata confirms the exact Head is `a538dbf289cb21fc04a03fb412c90482619187bc`, targeting `main`, with one commit.

---

## BLOCKING

1. **Recommended textual clarification:** Identify the `session_evidence` entry by its corresponding `implementing_ai_session` field, rather than relying on the less precise phrase "the entry that carries the session". Mirror the clarification in both languages.
2. Record the independent exact-Head governance review and its disposition in the appropriate repository carrier.
3. Do not claim the incomplete declared-check-context verification as PASS. Resolve or explicitly disposition that outstanding verification before asserting that every applicable merge gate has passed.

## NON-BLOCKING

1. The unresolved principal-identity registry requirement. It remains a separate governance defect.
2. Historical superseded annotations in AID-2026-071 and AID-2026-075. Their historical status is sufficiently explicit.
3. The unchanged, hash-pinned AID-2026-075 prompt. Its supersession is explicitly recorded.
4. The absence of executable changes. This is appropriate to the authorized scope.
5. The distinction between parser acceptance and complete end-to-end gate execution. The former is demonstrated; the latter should not be overstated.

**Final disposition:** The normative correction is substantively acceptable. I would not reject it or demand a redesign. The multi-entry wording clarification and the outstanding exact-Head review/verification record should be addressed before treating the PR as fully merge-ready.
```

## 3. Disposition of the three blocking items

### B1 — "Identify the `session_evidence` entry by its corresponding `implementing_ai_session` field … mirror in both languages"

**Applied, but not in the suggested wording.** The suggestion was checked against the population
before adopting it, and it does not fit:

1. It is self-referential for `implementing_ai_session` itself — the field would be defined as
   living in the entry identified by that same field.
2. It says nothing about `sponsor` and `accountable_owner`, which are never inside a
   `session_evidence` entry in any manifest that exists.
3. It presumes there is one relevant entry. **AID-2026-055 carries three** `session_evidence`
   entries, and three occurrences of `implementing_ai_session`, one per entry. A phrase that
   identifies "the" entry is undecidable there, which is the ambiguity the item set out to
   remove.

The applied wording removes the reference to a particular entry instead of sharpening it,
because the constraint the gate enforces is about *locations*, not about *which entry*:

- English: `each of them either at top level or inside the `session_evidence` entries and never in both places`
- Chinese: 「每个字段或位于顶层、或位于 `session_evidence` 条目内，不得两处并存」

Measured against the branch tip (55 manifests), with "inside" scoped to the `session_evidence`
block and not to any nested key that happens to share a name:

| result | count | ids |
| --- | --- | --- |
| satisfy the amended clause | 48 | every manifest except the seven below |
| do not satisfy it | 7 | 005, 006, 008, 009, 029 (no `sponsor`, no `implementing_ai_session`); 024, 025 (none of the three) |
| satisfy it **and** accepted by `parse_manifest_session_entries` | 21 | the 20 previously conformant manifests plus AID-2026-080 itself |

The scoping matters and is the reason this measurement differs from the one in the request: an
unscoped "appears indented anywhere" test flags AID-2026-026, whose `scope_revision.ownership_unchanged`
block restates `sponsor: NOT_ASSIGNED` while a ruling undoes nothing. That is a record about
ownership, not a second declaration of the field, and the amended clause does not reach it. The
number published from the unscoped test would have been 47 and would have been wrong.

### B2 — "Record the independent exact-Head governance review and its disposition in the appropriate repository carrier"

**This file is that carrier.** It is committed in the work item directory, it names the Head the
review read, and `AID-2026-080/manifest.yaml` cites it under `review`.

### B3 — "Do not claim the incomplete declared-check-context verification as PASS"

**Resolved by re-running it with a token.** The earlier `INCOMPLETE` was `HTTP 403: rate limit
exceeded` on an unauthenticated call, not a verdict:

```
::notice::16 declared check contexts, all produced by a job in .github/workflows and all required on main
DECLARED CHECK CONTEXTS: PASS
```

The pull request body is corrected to report this result rather than the rate-limited one.

## 4. What this record does not claim

- **It does not claim a human review.** The reviewer is a separate AI session. §5 as amended makes
  independence a property of the session, and this satisfies that; it does not make the review
  human, and no statement here says otherwise.
- **It does not claim the verdict applies to a Head it did not read.** Round 1 read `a538dbf2`.
  The amendment in B1 and this file change the Head; the disposition round is recorded separately
  and names its own Head.
- **It does not claim the principal-identity defect is resolved.** The reviewer's non-blocking item
  1 and this work item's `files_out_of_scope` both say it remains open.
- **It does not upgrade `review.status` to APPROVED on the strength of round 1.** Round 1 returned
  `ACCEPT WITH AMENDMENTS`; whether the amendments close it is round 2's decision, not this file's.
