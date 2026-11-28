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
        - "14-ai-development/work-items/AID-2026-345/manifest.yaml"
        - "#1507"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Repository measurements, commit identities, mirror measurements and bilingual-gate output in this record are supplied as completed local measurements. The authoring session has not independently rerun the local checks or verified the eventual PR and CI state."
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
    canonical_scope: "Evidence boundary and acceptance measurements for AID-2026-345 GOV-DOC-002 Context Versioning bilingual mirrors."
    canonical_scope_id: "ai-development/aid-2026-345-context-versioning-evidence"
    canonical_scope_keywords:
      - "AID-2026-345"
      - "GOV-DOC-002"
      - "Context Versioning"
      - "bilingual mirrors"
      - "evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "Architecture Governance"
---

# Evidence — AID-2026-345

## 1. Evidence boundary

This document records the supplied repository facts, completed local measurements, existing commit identities, and remaining acceptance boundaries for AID-2026-345.

The repository is:

`oahcom/AiMemoryBrainArchitecture`

The Work Item is tracked by Issue:

`#1507`

The task-start base is:

`895d5dcbc8d2f00b3403a5173781ee22566fcfe3`

The branch is:

`docs/aid-2026-345-gov-doc-002-context-versioning-bilingual-mirrors`

The worktree is:

`D:\code\wt-aid-332-pr`

The task-start base remains the declared `base_commit_sha`. The later `origin/main` head is:

`3894677073191bf6b7ac113e9baf5874c864fffb`

The two intervening main commits are:

- `1641ea16b` — Restore Prompt-to-commit traceability for AID-2026-212, PR #1505.
- `389467707` — fix(ci): restore merge_group wiring for GOV-DOC-002 metadata checks, AID-2026-294, PR #1491.

The supplied comparison establishes that the task-start base is an ancestor of the later main head and that neither intervening commit modified any of the nine paths already present in Commit 1 and Commit 2.

Accordingly, the task-start base is retained as historical work provenance. It is not a claim that the PR target branch remains at that commit.

The repository measurements and checker results below are supplied local measurements. They are not represented as fresh executions by this authoring session.

## 2. Work item identity

| Field | Value |
|---|---|
| Work Item | AID-2026-345 |
| Title | Complete GOV-DOC-002 steward metadata and Context Versioning bilingual mirrors |
| Tracking Issue | #1507 |
| Class | DOC/GOVERNANCE |
| Risk | R1 |
| Status | DISPATCHED |
| ID status | PROVISIONAL |
| Acceptance authority | NOT_ASSIGNED |
| Repository | oahcom/AiMemoryBrainArchitecture |
| Base branch | main |
| Task-start base | 895d5dcbc8d2f00b3403a5173781ee22566fcfe3 |
| Current main at latest supplied measurement | 3894677073191bf6b7ac113e9baf5874c864fffb |
| Branch | docs/aid-2026-345-gov-doc-002-context-versioning-bilingual-mirrors |
| Issue | #1507 |

The identifier AID-2026-332 was not available for this work. The existing directory on `origin/main` belongs to PR #1504 and the different work item titled "Split GOV-DOC-001 owner-namespace and governance-operation checker steps". AID-2026-345 was selected as the first identifier in the supplied verified-free range 341 through 350.

## 3. Source and baseline evidence

The source document is:

`06-memory-context/context-versioning.md`

The source probe commit is:

`e43e84c365ed4f41f4f62dda864ae4c19fe6a6bb`

The source export supplied for the initial probe measured 564 physical lines and 38,792 bytes.

The two complete mirrors were measured after completion:

| File | Physical lines | Bytes |
|---|---:|---:|
| `docs/en/06-memory-context/context-versioning.md` | 562 | 38,775 |
| `docs/zh-CN/06-memory-context/context-versioning.md` | 537 | 36,917 |

The measured structural correspondence is:

| Measurement | Source | English | Simplified Chinese |
|---|---:|---:|---:|
| Heading hierarchy | 37 | 37 | 37 |
| CV identifiers | 48 | 48 | 48 |
| Table rows | 77 | 77 | 77 |
| MUST occurrences | 57 | 57 | 57 |

The Chinese mirror has 21 fewer physical lines than the English mirror because hard-wrapped paragraphs are combined in Chinese. This line-count difference is not omitted content.

The bilingual baseline initially contained the source as a frozen gap. Once both complete mirrors existed, the resolved gap had to be removed from both baseline files.

The original locations were:

- `scripts/bilingual-baseline.txt`, line 10.
- `scripts/ci/baselines/bilingual-docs.txt`, line 7.

After deleting the matching entry from both files, the supplied baseline result was:

```text
bilingual baseline: 76 frozen, 0 new gaps
```

The two baseline files must remain synchronized.

## 4. Required bilingual mirror evidence

The required English mirror is:

`docs/en/06-memory-context/context-versioning.md`

The required Simplified Chinese mirror is:

`docs/zh-CN/06-memory-context/context-versioning.md`

Both mirrors are reported as completed and measured against the source version committed in Commit 1.

The English mirror is a complete English counterpart of the source.

The Simplified Chinese mirror is a complete translation of the entire source document. It is not limited to the newly changed section.

The supplied measurements establish:

- 37 matching heading levels and hierarchy positions.
- 48 CV identifiers in each language mirror.
- 77 table rows in each language mirror.
- 57 MUST occurrences in each language mirror.
- 562 English physical lines and 537 Chinese physical lines.
- 38,775 English bytes and 36,917 Chinese bytes.

The 21-line physical difference is attributed to hard-wrapped paragraphs being combined in Chinese. It is not an omission of source sections or requirements.

The completed mirrors preserve the source's section hierarchy, normative meaning, references, tables, code examples and literal paths according to the supplied comparison.

## 5. Document-management evidence

The Work Item uses the following metadata decisions:

- `class: DOC/GOVERNANCE`
- `risk: R1`
- `status: DISPATCHED`
- `id_status: PROVISIONAL`
- `acceptance_authority: NOT_ASSIGNED`

The evidence, prompt and session-evidence Markdown files use:

- `domain: ai-development`
- `role: work-record`
- `decision_status: Draft`
- `approval_scope: {type: Full-document}`
- `approval_applicability: Not-Applicable-To-Current-Version`
- `verification_status: Unverified`
- `usage_status: Active`
- `modification_status: Modified`
- `canonical_status: Non-Canonical`
- `canonical_conflict_status: None`
- `normative_status: Informative`

Each document has a distinct `canonical_scope_id` under the `ai-development/` domain prefix and a non-empty steward.

The manifest has no Markdown frontmatter. It uses the Work Item manifest schema and records the five documentation files in the resulting Work Item directory.

The manifest's `implementation.status` is `IMPLEMENTED` because the two implementation commits already exist. This does not imply that the PR is open, CI has run, independent review has completed, or acceptance has been granted.

The required document-management commands for the completed three-commit PR are:

```bash
python scripts/check_document_management.py --require-changed
python scripts/check_document_management.py --strict
```

The `--require-changed` result must be recorded from the completed PR checkout.

The probe baseline reported 369 pre-existing strict errors. No claim is made here that those strict errors have been fixed.

## 6. Bilingual gate evidence

The supplied local measurement identified the following failure when the mirrors existed but the baseline still retained the resolved gap:

```text
Resolved bilingual gap must be removed from scripts/bilingual-baseline.txt
```

The checker exited 2 in that state.

The required correction was to remove the matching source entry from both:

- `scripts/bilingual-baseline.txt`
- `scripts/ci/baselines/bilingual-docs.txt`

After the two synchronized deletions, the supplied baseline output was:

```text
bilingual baseline: 76 frozen, 0 new gaps
```

The actual PR body must contain:

```text
BILINGUAL-MANIFEST: COMPLETE
```

The checker receives the PR body through the `PR_BODY` environment variable.

The supplied successful run used a PR body containing the declaration and produced:

```text
Bilingual documentation and prompt gate: PASS (9 changed paths inspected)
```

The supplied exit code was 0.

The nine inspected paths are the five probe paths, two mirror paths and two baseline paths. The five Work Item records and INDEX registration are separate additions to the final PR change set.

The successful local bilingual-gate result is not a claim that the eventual GitHub Actions run has completed.

## 7. Commit evidence

The branch contains two implementation commits at the time of this evidence snapshot.

### Commit 1

The source/probe changes are recorded in the first implementation commit, which updates the five previously identified probe and governance-document paths. Its Git object ID is not pinned here because the branch is subject to rebase.

Original subject:

`docs(aid-2026-332): amend ratchet, authz, context-versioning and steward metadata`

Files:

1. `06-memory-context/context-versioning.md`
2. `14-ai-development/adr/OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001.md`
3. `14-ai-development/ci-gates-and-ratchets.en.md`
4. `14-ai-development/ci-gates-and-ratchets.zh-CN.md`
5. `14-ai-development/reports/steward-adoption-baseline.json`

Recorded change:

Five files, 81 insertions and 8 deletions.

### Commit 2

The bilingual-mirror changes are recorded in the second implementation commit, which adds the English and Simplified Chinese mirrors and removes the resolved bilingual-gap entries from both baseline files. This commit depends on the source/probe commit. Neither Git object ID is pinned here because the branch is subject to rebase.

Original subject:

`docs(aid-2026-332): add Context Versioning bilingual mirrors`

Files:

1. `docs/en/06-memory-context/context-versioning.md`
2. `docs/zh-CN/06-memory-context/context-versioning.md`
3. `scripts/bilingual-baseline.txt`
4. `scripts/ci/baselines/bilingual-docs.txt`

The two baseline files each remove the resolved bilingual-gap entry.

Commit 2 depends on Commit 1 because its mirrors correspond to the source version changed in Commit 1.

The two original commit subjects still contain the old identifier AID-2026-332. They must be rewritten to AID-2026-345 in the same history rewrite that creates the final third commit. No commit message in the final branch history may identify this work as AID-2026-332.

### Commit 3

Commit 3 is reserved for the five AID-2026-345 Work Item files and the INDEX registration row:

1. `14-ai-development/work-items/AID-2026-345/manifest.yaml`
2. `14-ai-development/work-items/AID-2026-345/prompt-v1.md`
3. `14-ai-development/work-items/AID-2026-345/prompt-v1-executed.md`
4. `14-ai-development/work-items/AID-2026-345/evidence.md`
5. `14-ai-development/work-items/AID-2026-345/session-evidence.md`
6. `14-ai-development/work-items/INDEX.md`

Commit 3 depends on Commit 1 and Commit 2. It records the final Work Item directory and the INDEX row that points to its manifest.

The final PR change set therefore contains fifteen paths: five probe revisions, two mirrors, two baseline updates, five Work Item files and one INDEX update.

## 8. Session and prompt evidence

The byte-exact task-input snapshot used for the recorded execution is:

`14-ai-development/work-items/AID-2026-345/prompt-v1-executed.md`

The editable task-input text is maintained separately in `14-ai-development/work-items/AID-2026-345/prompt-v1.md`.

The session record is:

`14-ai-development/work-items/AID-2026-345/session-evidence.md`

The manifest and session record use the same Issue reference:

`"#1507"`

The session-evidence validator requires nine Session identity fields:

1. `role`
2. `issue_refs`
3. `implementing_ai_session`
4. `executed_prompt_snapshot_file`
5. `executed_prompt_sha256`
6. `executed_prompt_bytes`
7. `executed_prompt_provenance`
8. `session_reference_status`
9. `session_evidence_ref`

The SHA-256 digest and byte count recorded for the executed prompt snapshot identify the exact bytes of `14-ai-development/work-items/AID-2026-345/prompt-v1-executed.md`.

The session identifier must identify the actual implementing session. It must not be invented.

The prompt provenance remains `NOT_VERIFIED` unless the exact prompt transmission is independently established.

The session reference status is recorded as `RECORDED` because the session evidence artifact is the declared reference. This does not assert that the session identifier or prompt transmission has been independently verified.

## 9. Validation evidence

The supplied successful bilingual gate and baseline measurements are recorded above.

The following commands remain required on the completed three-commit PR checkout:

```bash
python scripts/check_document_management.py --require-changed
python scripts/check_document_management.py --strict
python scripts/check_bilingual_docs.py
python scripts/check_line_endings.py
python scripts/check_repository_hygiene.py
python scripts/check_traceability.py
git diff --check
```

The bilingual gate must be run with the actual PR body supplied through `PR_BODY`, including the exact declaration `BILINGUAL-MANIFEST: COMPLETE`.

The completed PR checkout must also verify:

- All fifteen intended paths are present.
- Both mirrors correspond to the Commit 1 source.
- Both baseline files are synchronized.
- The baseline reports 76 frozen entries and zero new gaps.
- The manifest parses as YAML and satisfies the Work Item manifest schema.
- Every manifest documentation path exists in the resulting Git tree.
- The INDEX row is a single physical nine-column row with the repository-relative manifest link.
- The session-evidence record contains all nine required Session identity fields.
- The prompt digest and byte count match the final prompt file bytes.

The PR has not yet been opened at the time of this evidence snapshot. CI has not yet run. No merge, independent review or Owner acceptance is claimed.
