---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Under-Review
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/schemas/work-item-registry.source-rules.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "This is a non-canonical English mirror. Independent governance approval and verification have not been recorded."
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
    canonical_scope: "AI development: work-item registry source rules"
    canonical_scope_id: "ai-development/work-item-registry/source-rules"
    canonical_scope_keywords:
      - work-item-registry
      - source-rules
      - manifest
      - field-state
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "00-governance/schemas/work-item-registry.source-rules.md"
    zh-CN: "docs/zh-CN/00-governance/schemas/work-item-registry.source-rules.md"
---

# Canonical Work Item Registry — Source Rules

## 1. Authority model

The canonical registry is the sole authority for normalized work-item field
values. This file defines how a value may enter or change the registry.

The following are projections or evidence carriers, not independent authorities:

- `14-ai-development/work-items/INDEX.md`
- per-work-item `manifest.yaml`
- PR descriptions and issue descriptions
- comments, reviews, session evidence, and CI output

A projection must never overwrite a canonical value merely because its text
differs from the registry.

Every canonical field value MUST have at least one source reference. A value
without a verifiable source MUST be `UNCONFIRMED`, not inferred.

## 2. Evidence precedence

Apply this precedence to the specific field being resolved. A source that is
authoritative for one field is not automatically authoritative for another.

1. Explicit, attributable Owner decision or authorization, when the field is
   within that person's authority and the decision identifies the work item
   and scope.
2. Exact Git object evidence: file bytes at a pinned commit, tree membership,
   commit metadata, or an exact diff.
3. Explicit structured record in a merged governance artifact, when its
   schema and scope authorize that field.
4. Explicit issue/PR body or comment by the accountable authority, when the
   statement is attributable and unambiguous.
5. Corroborating review, CI, or implementation evidence.
6. INDEX display text or derived prose.

A later source does not automatically outrank an earlier source. It must be
authorized to supersede it and must identify the value being changed.

When equally ranked sources conflict, record `UNCONFIRMED` and preserve both
sources. Do not resolve a conflict by timestamp, majority vote, PR merge order,
or whichever copy is easiest to parse.

## 3. `work_item_id`

Authority:
- The exact directory/manifest identity in the canonical registry namespace.
- The reserved-ID claim record, when the repository's claim registry applies.

Rules:
- Format MUST be `AID-YYYY-NNN`.
- A directory name alone is not proof that its embedded manifest declares
  the same ID.
- A manifest `work_item_id` that disagrees with its directory is a conflict.
- Two distinct canonical record paths declaring the same ID are a hard
  uniqueness violation.
- A renamed directory is not an ID change unless an authorized record
  explicitly changes the ID.
- Never infer a missing ID from a PR number, issue number, title, branch name,
  or nearby directory.

Unknown/mismatch:
- Missing ID: `UNKNOWN`.
- Conflicting directory and manifest IDs: `UNCONFIRMED`.
- Duplicate ID across distinct registry records: reject the registry update.

## 4. `title`

Authority:
- The exact UTF-8 bytes of the explicitly designated title source, preserved
  before parsing or normalization.
- If the title is defined in a manifest, the raw manifest scalar is evidence;
  the YAML parser's value is not authoritative when parsing has changed it.

YAML truncation rule:
- An unquoted ` #` begins a YAML comment in a plain scalar.
- Therefore, when raw bytes contain a title scalar with an unquoted ` #`,
  the parsed YAML value MUST NOT be treated as the complete title.
- The raw scalar MUST be recovered using a YAML-aware source-span parser or
  an exact byte-level extraction that understands quoting, escaping, block
  scalars, and line boundaries.
- A naive split at ` #` is not sufficient because quoted and block scalars
  have different semantics.
- If raw extraction cannot establish the intended complete scalar without
  ambiguity, title MUST be `UNCONFIRMED`.

For the five known truncated titles:
- Do not copy the parsed YAML values into the registry.
- Do not copy INDEX text without corroboration.
- Compare the raw manifest bytes, exact historical Git versions, and any
  explicit title declaration in the originating Issue/PR.
- If those sources establish one identical full title, record it as `KNOWN`.
- If they disagree or the original intended title cannot be established,
  record `UNCONFIRMED` and preserve all candidates in provenance evidence.

A title MUST NOT be reconstructed from a PR title unless the PR explicitly
states that it is the canonical work-item title.

## 5. `owner`

Owner is a structured set of roles. It MUST NOT be flattened into one
account-name string.

Fields:
- `owner.accountable_owner`: who is accountable for the work item.
- `owner.attribution`: who or what is credited with originating or
  contributing to the work.
- `owner.authority`: the authority or delegation basis that permits decisions
  on the work item's scope or acceptance.
- `owner.resolution`: how the available sources relate.

Source handling:
- Top-level `accountable_owner` is evidence for the accountable-owner role.
- `authority.accountable_owner` is evidence for the accountable-owner role
  only when the containing authority object defines that meaning.
- `attribution` is attribution evidence, not an automatic substitute for
  accountable ownership.
- INDEX composite text is a display projection. It MUST be decomposed only
  when each component can be traced to a source.
- A GitHub login, commit author, PR author, implementing session, or proxy
  publisher MUST NOT be inferred to be the natural-person accountable owner.

Precedence:
1. Explicit, attributable Owner appointment or decision for the work item.
2. Explicit structured `authority.accountable_owner`, if the authority record
   is valid and scoped to this work item.
3. Explicit structured top-level `accountable_owner`.
4. Other structured owner fields, only for their declared roles.
5. INDEX composite text, as corroboration only.

Conflict rules:
- If `accountable_owner` and `authority.accountable_owner` agree, record the
  normalized accountable owner and preserve both source references.
- If they disagree and no authorized later decision resolves the conflict,
  `accountable_owner.state` MUST be `UNCONFIRMED`.
- `attribution` MUST remain a separate field even when its value equals the
  accountable owner.
- If an INDEX cell combines multiple roles, split it only when the source
  text explicitly identifies those roles. Otherwise the affected role is
  `UNCONFIRMED`.
- A proxy action MUST be recorded as proxy attribution/authority evidence;
  it MUST NOT be represented as a natural-person Owner signature.

Known source-shape cases:
- Six records whose INDEX owner equals `attribution` remain attribution
  evidence unless a separate source establishes accountability.
- Six manifests with no owner field MUST NOT inherit Owner from INDEX.
- Twelve `authority.accountable_owner` records are candidates for
  accountable-owner evidence, subject to scope and authority validation.
- Eighteen composite INDEX owner cells MUST NOT be treated as one canonical
  owner value.

## 6. `class`

Authority:
- An explicit structured classification in an authorized work-item record
  or an authorized classification decision.
- Legacy manifest or INDEX labels are migration evidence only.

Rules:
- Map a legacy value only when the mapping to the canonical enum is
  unambiguous and documented.
- Do not infer class from title keywords, file paths, PR labels, or
  implementation language.
- If two canonical classes are plausible, use `UNCONFIRMED`.
- If the field is known to be intentionally empty, use `KNOWN_EMPTY`.
- If no classification has been made, use `UNDECIDED`, not `UNKNOWN`.

## 7. `risk`

Authority:
- An explicit risk classification by an authorized reviewer or risk owner,
  with scope and evidence.
- Existing `risk`, `risk_level`, or INDEX risk labels are evidence only until
  their meaning is mapped to the canonical enum.

Rules:
- Do not infer risk from severity words in a title or issue description.
- Do not equate an implementation priority with risk.
- Do not equate "no risk recorded" with `LOW`.
- `UNKNOWN` means no reliable risk evidence exists.
- `UNDECIDED` means assessment is required but no decision has been made.
- `NOT_APPLICABLE` requires an explicit reason that risk classification does
  not apply.
- A conflict between risk sources is `UNCONFIRMED`.

## 8. `status`

Authority:
- The actual work-item lifecycle record, supported by exact merged PR,
  repository, and acceptance evidence.
- A status token in INDEX is a projection, not the lifecycle authority.
- Free-form status prose is not a machine lifecycle token.

Canonical status tokens:
- `PROPOSED`
- `DISPATCHED`
- `IN_PROGRESS`
- `BLOCKED`
- `IN_REVIEW`
- `MERGED`
- `VERIFIED`
- `ACCEPTED`
- `REJECTED`
- `CANCELLED`
- `SUPERSEDED`

INDEX parsing:
- Parse only a recognized, whole-cell-leading token from the explicit
  allowlist maintained by the registry importer.
- The token must be separated from following prose by a recognized delimiter.
- The delimiter and remaining prose MUST be retained separately as
  `status_note` evidence; prose MUST NOT be appended to the token.
- `—` followed by prose, `-` followed by prose, and other separators are
  formatting patterns, not status values.
- A cell with multiple mutually exclusive lifecycle tokens is
  `UNCONFIRMED`.
- A cell with no recognized token is not assigned a lifecycle status from
  prose. It is `UNCONFIRMED` if it contains an ambiguous status assertion,
  otherwise `UNKNOWN`.
- The importer MUST NOT infer `MERGED` merely because a PR is closed.
- `MERGED` requires a merged PR or equivalent exact merge evidence.
- `VERIFIED` requires verification evidence against the exact relevant
  artifact/head.
- `ACCEPTED` requires an explicit acceptance decision by the authorized
  acceptance authority.
- `SUPERSEDED` requires a valid successor relationship.

Known INDEX distribution:
- 66 `—` + prose cells, 8 `-` + prose cells, and 8 other-separator cells
  MUST be treated as token-plus-note candidates, not copied as combined
  status strings.
- 26 mutually exclusive token cells MUST be `UNCONFIRMED` until their
  lifecycle meaning is resolved.
- These counts are migration diagnostics, not permanent schema constants.

## 9. `prompt`

Prompt identity is a multi-field record. A prompt ID alone is not a content
pin. A digest alone is not a locator.

Fields:
- `prompt_id`: identity of the prompt.
- `prompt_sha256`: digest of the exact prompt bytes under the declared
  canonical byte convention.
- `prompt_path`: repository path or other exact locator.
- `prompt_version`: explicit version identifier.
- `prompt_commit_sha`: Git commit containing the prompt bytes.
- `provenance_note`: historical explanation or legacy evidence.

Evidence sufficient for `PINNED`:
- A verified prompt locator.
- Exact bytes at that locator.
- A SHA-256 digest calculated from those exact bytes.
- A consistent prompt identity/version relationship.
- A source reference that identifies the commit or immutable artifact.

`IDENTIFIED_UNPINNED`:
- A prompt ID and/or exact path is established, but no verified digest exists.

`LEGACY_PROVENANCE_ONLY`:
- The only available prompt identity evidence is a historical free-text
  provenance note.
- This status MUST NOT be treated as a complete prompt pin.

`NOT_PRESENT`:
- An authoritative source explicitly states that no prompt applies or was
  used, as appropriate to the work item's declared process.
- Mere absence of `prompt_id` is not proof of `NOT_PRESENT`.

Known source-shape cases:
- The 56 records with no `prompt_id` MUST NOT receive a fabricated ID.
- The 6 records with `prompt_id` but no `prompt_sha256` MUST NOT be labeled
  `PINNED`; they are at most `IDENTIFIED_UNPINNED`.
- For AID-2026-064, a `prompt_provenance_note` is historical evidence only.
  It does not become a prompt ID or digest by extraction or guesswork.
- A digest with no verified byte locator is not a pin.
- An ID plus an empty digest is not a complete prompt record.
- A guessed prompt path, branch name, or latest prompt file is not evidence.

## 10. `provenance`

Authority:
- Evidence attached to each field, not a single general claim that the
  manifest is trustworthy.

Grades:
- `PRIMARY`: a direct authoritative source for the field, with exact scope.
- `CORROBORATED`: two or more independent sources agree, but no single
  source alone is the direct authority.
- `DERIVED`: computed deterministically from identified primary evidence.
- `CONFLICTED`: primary or equally ranked sources disagree.
- `UNCONFIRMED`: evidence is insufficient to establish the field.

Rules:
- A provenance grade MUST NOT be stronger than the weakest material source
  required to establish that field.
- Derived values MUST record the derivation and all input source references.
- CI success proves only the checks actually executed; it does not prove
  authorship, Owner identity, or acceptance unless the check explicitly
  validates that proposition.
- A merged PR proves merge state and merge commit, not acceptance.
- A commit author field proves Git metadata, not natural-person identity.
- A proxy publication proves the proxy action and its declared authority,
  not personal publication by the delegating Owner.

## 11. `supersedes` and `superseded_by`

Authority:
- An explicit work-item replacement decision or an unambiguous, authorized
  successor declaration.

Rules:
- Both directions MUST agree.
- A supersession edge MUST NOT be inferred merely because two PRs have
  similar titles or touch the same files.
- A duplicate carrier is not automatically a successor work item.
- A carrier PR replacement under the same work-item ID does not create a
  supersession edge between work items.
- A cycle is invalid.
- A missing target record is a validation failure unless the edge is
  explicitly marked `UNCONFIRMED` during migration.

## 12. `source_refs`

Authority:
- Exact Git paths and commits, GitHub Issue/PR/comment/review identifiers,
  CI run identifiers, or immutable external document locators.

Rules:
- Each locator MUST resolve to the intended object.
- Git references used as evidence MUST include an immutable commit SHA.
- A branch name or `main` without a commit SHA is not immutable evidence.
- A source reference MUST declare its role: `PRIMARY`, `CORROBORATING`,
  `HISTORICAL`, or `CONTRADICTING`.
- Do not cite a PR head SHA as merge evidence. Use the actual merge commit.
- Do not cite a merged PR as proof that every statement in its body was
  accepted.
- Preserve contradictory sources; do not delete them after choosing a
  canonical value.

## 13. Migration and write rules

- Preserve original manifest bytes before parsing or rewriting.
- Never round-trip a manifest through a parser and serializer as a
  "normalization" step until all lossy scalar cases have been resolved.
- Never generate INDEX values from an unconfirmed registry field.
- A registry update MUST modify only the work-item record being changed,
  except for explicit cross-record relationship updates.
- A registry validator MUST reject duplicate work-item IDs, invalid
  supersession graphs, invalid source references, and illegal status
  transitions.
- A registry writer MUST use compare-and-swap semantics against the expected
  current blob SHA. A stale writer MUST fail rather than overwrite.
- A merge conflict MUST be resolved by comparing source evidence, not by
  choosing the first, last, or shortest row.
- Unknown legacy data MUST remain visibly unknown. Migration completeness
  MUST NOT be achieved by inventing values.