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
        - "14-ai-development/work-items/AID-2026-380/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "This file is the task-input snapshot for AID-2026-380. Its exact transmission provenance has not been independently verified."
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
    canonical_scope: "Task input for AID-2026-380 GOV-DOC-002 steward metadata and Context Versioning bilingual mirrors."
    canonical_scope_id: "ai-development/aid-2026-380-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-380"
      - "GOV-DOC-002"
      - "Context Versioning"
      - "bilingual mirrors"
      - "steward metadata"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "Architecture Governance"
---

# Prompt v1 — AID-2026-380

## Task

Complete the GOV-DOC-002 steward metadata and Context Versioning bilingual mirror work tracked by Issue #1507.

The task preserves the existing probe changes, adds complete English and Simplified Chinese mirrors for the Context Versioning source, removes the resolved bilingual-gap baseline entry from both synchronized baseline files, and records the work in a single AID-2026-380 Work Item.

The repository is `oahcom/AiMemoryBrainArchitecture`.

The task-start base is:

`895d5dcbc8d2f00b3403a5173781ee22566fcfe3`

The source document is:

`06-memory-context/context-versioning.md`

The source probe commit is:

`e43e84c365ed4f41f4f62dda864ae4c19fe6a6bb`

The Work Item identifier is `AID-2026-380`.

The tracking Issue is `#1507`.

## Required implementation

Deliver one Work Item, one Issue, and one PR.

Preserve the two existing implementation commits as the first two commits in the PR history, update their commit messages so that their Work Item identifier is AID-2026-380, and add a third dependent commit containing the five Work Item files and the INDEX registration.

The final PR change set consists of fifteen paths:

- Five existing probe-file revisions.
- Two complete language mirrors.
- Two synchronized bilingual-baseline updates.
- Five AID-2026-380 Work Item files.
- One INDEX registration row.

### Commit 1 — Existing probe changes

Preserve the five existing probe files and their intended changes:

1. `06-memory-context/context-versioning.md`
2. `14-ai-development/adr/OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001.md`
3. `14-ai-development/ci-gates-and-ratchets.en.md`
4. `14-ai-development/ci-gates-and-ratchets.zh-CN.md`
5. `14-ai-development/reports/steward-adoption-baseline.json`

The first implementation commit contains the five source/probe and governance-document changes. Identify it by its role and changed paths, not by a Git object ID, because the branch is subject to rebase.

Its recorded change is five files, eighty-one insertions and eight deletions.

### Commit 2 — Complete bilingual mirrors and baseline cleanup

Add both complete mirrors:

1. `docs/en/06-memory-context/context-versioning.md`
2. `docs/zh-CN/06-memory-context/context-versioning.md`

Remove the resolved bilingual-gap entry for the source document from both synchronized baseline files:

3. `scripts/bilingual-baseline.txt`
4. `scripts/ci/baselines/bilingual-docs.txt`

The second implementation commit contains the two bilingual mirrors and the two baseline-entry removals, and depends on the first implementation commit. Identify it by its role and changed paths, not by a Git object ID, because the branch is subject to rebase.

The two baseline files must remain consistent.

The deletion is required because retaining the resolved entry causes the bilingual checker to report:

`Resolved bilingual gap must be removed from scripts/bilingual-baseline.txt`

After the synchronized deletion, the expected baseline result is:

`bilingual baseline: 76 frozen, 0 new gaps`

### Commit 3 — Work Item records and registry

Add the five complete Work Item files:

1. `14-ai-development/work-items/AID-2026-380/manifest.yaml`
2. `14-ai-development/work-items/AID-2026-380/prompt-v1.md`
3. `14-ai-development/work-items/AID-2026-380/evidence.md`
4. `14-ai-development/work-items/AID-2026-380/session-evidence.md`

Append exactly one nine-column registration row to:

`14-ai-development/work-items/INDEX.md`

The INDEX row must use the repository-relative manifest link:

`[AID-2026-380](AID-2026-380/manifest.yaml)`

Append the row at the end of the applicable INDEX table. Do not reorder or rewrite legacy rows.

The manifest documentation list must point only to the five files that exist in this Work Item directory. Each documentation entry must use a permitted relationship value and a repository path that exists in the resulting Git tree.

## Base and branch identity

The Work Item records the task-start base:

`895d5dcbc8d2f00b3403a5173781ee22566fcfe3`

The branch was created from that base. The current main branch later advanced to:

`3894677073191bf6b7ac113e9baf5874c864fffb`

The intervening main commits are:

- `1641ea16b` — Restore Prompt-to-commit traceability for AID-2026-212, PR #1505.
- `389467707` — fix(ci): restore merge_group wiring for GOV-DOC-002 metadata checks, AID-2026-294, PR #1491.

The task-start base remains a valid historical base declaration because it is an ancestor of the later main head. The two intervening commits did not modify any of the nine paths already present in the two implementation commits. Do not rewrite the task-start base field merely to represent the later PR target branch head.

The branch name is:

`docs/aid-2026-380-gov-doc-002-context-versioning-bilingual-mirrors`

The Work Item directory is:

`14-ai-development/work-items/AID-2026-380/`

## Mirror completeness requirements

Both mirrors must correspond to the exact source committed in Commit 1.

The English mirror must be a complete English counterpart of the source document.

The Simplified Chinese mirror must be a complete Chinese translation of the entire source document, not merely a translation of the newly changed section.

Preserve:

- The complete section hierarchy.
- Normative meaning and modality.
- All CV identifiers.
- All tables and their row content.
- Links and references.
- Code examples and literal paths.
- The meaning of MUST, SHOULD and MAY requirements.

The measured mirror facts are:

- English mirror: 562 physical lines and 38,775 bytes.
- Simplified Chinese mirror: 537 physical lines and 36,917 bytes.
- Heading hierarchy: 37 in the source, 37 in English and 37 in Chinese.
- CV identifiers: 48 in each.
- Table rows: 77 in each.
- MUST occurrences: 57 in each.

The 21-line difference between the English and Chinese mirrors is caused by hard-wrapped paragraphs being combined in Chinese. It is not omitted content.

## Baseline correction requirements

The resolved bilingual-gap entry must be removed from both files:

- `scripts/bilingual-baseline.txt`
- `scripts/ci/baselines/bilingual-docs.txt`

The original locations were line 10 and line 7 respectively.

Both files must remain synchronized.

The measured result after deletion is:

`bilingual baseline: 76 frozen, 0 new gaps`

Do not retain the resolved gap as a frozen exception.

## Acceptance evidence checklist

Run the checks from the completed PR checkout after all three commits are present.

### 1. Document-management checks

Run:

```bash
python scripts/check_document_management.py --require-changed
python scripts/check_document_management.py --strict
```

Record each exit status and complete relevant output.

The `--require-changed` check must exit 0.

The strict check must be reported separately. The probe baseline reported 369 pre-existing strict errors. Do not claim those errors are fixed by this work unless the new run demonstrates that result.

Do not manipulate the steward adoption baseline pin to bypass stale-count comparison.

### 2. Bilingual documentation gate

The workflow supplies the PR body through the `PR_BODY` environment variable.

The actual PR body must contain this exact declaration:

```text
BILINGUAL-MANIFEST: COMPLETE
```

Run:

```bash
export PR_BODY="$(cat /path/to/actual-pr-body.md)"
python scripts/check_bilingual_docs.py
```

The expected result is:

`Bilingual documentation and prompt gate: PASS (9 changed paths inspected)`

The command must exit 0.

The checker must recognize both complete mirror paths for the Context Versioning source.

Do not put the manifest declaration only in a repository Markdown file. The workflow passes the actual PR body through `PR_BODY`.

### 3. Repository hygiene and diff checks

Run:

```bash
python scripts/check_line_endings.py
python scripts/check_repository_hygiene.py
python scripts/check_traceability.py
git diff --check
```

All commands must exit 0.

If the applicable CI workflow invokes a different canonical command, use the exact workflow command and record the actual command and result.

### 4. Mirror and baseline verification

Verify that:

- Both mirror files exist at their exact required paths.
- Both mirrors correspond to the source committed in Commit 1.
- The English mirror is complete.
- The Simplified Chinese mirror is a complete translation.
- The structural measurements agree with the recorded values.
- Both bilingual baseline files have the resolved entry removed.
- The two baseline files remain synchronized.
- The baseline reports 76 frozen entries and zero new gaps.

### 5. Work Item and session evidence

Verify that:

- All five Work Item files exist in the Git tree.
- The manifest parses as YAML and satisfies the Work Item manifest schema.
- The manifest documentation paths resolve in the resulting Git tree.
- The INDEX row is a single physical nine-column table row.
- The first cell links to the manifest using the repository-relative AID directory path.
- The session-evidence file contains all nine required Session identity fields.
- The prompt digest and byte count are computed from the final prompt file bytes.
- Session identity and prompt provenance are not represented as independently verified unless evidence establishes that status.

## Work Item metadata

Use these values:

- `work_item_id`: `AID-2026-380`
- `class`: `DOC/GOVERNANCE`
- `risk`: `R1`
- `status`: `DISPATCHED`
- `id_status`: `PROVISIONAL`
- `acceptance_authority`: `NOT_ASSIGNED`
- `tracking_issue`: `#1507`
- `base_branch`: `main`
- `base_commit_sha`: `895d5dcbc8d2f00b3403a5173781ee22566fcfe3`

The implementation commits exist. The PR has not yet been opened and CI has not yet run. Do not claim a PR number, CI result, merge, independent review or acceptance decision that does not exist.

## Non-goals

- Do not change `scripts/check_bilingual_docs.py`.
- Do not change `scripts/check_document_management.py`.
- Do not change checker implementation or validation rules.
- Do not change CI workflow behavior.
- Do not change branch protection.
- Do not change required status checks or required contexts.
- Do not change gate semantics.
- Do not create a bilingual catch-up exception for this source document.
- Do not treat a baseline entry as a substitute for either required mirror.
- Do not split the work into multiple Work Items, Issues or PRs.
- Do not merge Commit 2 independently of Commit 1.
- Do not merge Commit 3 independently of Commits 1 and 2.
- Do not claim pre-existing strict-check failures are resolved unless the evidence proves they are resolved.
- Do not fabricate session identifiers, prompt hashes, byte counts, test results or evidence references.
- Do not claim that commands, tests, repository writes or API probes were executed unless actual execution evidence is available.
