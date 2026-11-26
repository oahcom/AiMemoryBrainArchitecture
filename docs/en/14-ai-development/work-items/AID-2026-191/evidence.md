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
        - "14-ai-development/work-items/AID-2026-191/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Every number below was re-measured in this work tree at the stated head: before and after blob ids and byte sizes read with git rev-parse and git cat-file, insert/delete counts from git diff --numstat, gate output read from the gate's own stdout. What is NOT verified: semantic parity between the English and Chinese mirrors is not claimed, and no approval or acceptance decision is asserted."
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
    canonical_scope: "Evidence for AID-2026-191: GOV-DOC-002 metadata for the 07-agent-integration inference-boundary and telemetry mirror groups, and the measured limit on the remaining 07/08/13 mirrors"
    canonical_scope_id: "ai-development/aid-2026-191-mirror-frontmatter-b-evidence"
    canonical_scope_keywords:
      - "gov-doc-002"
      - "frontmatter"
      - "bilingual-mirror"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-191/evidence.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-191/evidence.md"
---

# AID-2026-191 — GOV-DOC-002 metadata for the 07/08/13 mirrors

## Scope and attribution

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base branch: `main`; branch `fix/2026-11-27-mirror-frontmatter-b`, work tree `D:\code\wt-corpus-b`
- Base commit at branch creation: `4326669c` (full SHA in `manifest.yaml`); `origin/main` was merged in
  again as `0c752ee6` before the pull request
- Attribution: user-authorized operator (delegated by account owner). No natural-person Owner
  signature, acceptance or approval is asserted.
- Unit brief: `unit-corpus-b.md` — "give 07/08/13 mirrors a frontmatter block". Prohibitions carried
  from it: no body edits, no baseline edits, no `03/04/05/09` changes, no new canonical, no new
  mirror.

## Defect

`docs/en/**` and `docs/zh-CN/**` contain mirror Markdown files whose first line is not `---`, so
GOV-DOC-002 cannot classify them (`check_document_management.py` reports them as unclassified).
In the three directories this unit owns, the unclassified mirrors are 22 files (11 mirror pairs):

| directory | en | zh-CN | pairs |
|---|---|---|---|
| `07-agent-integration` | 5 | 5 | 5 |
| `08-bmcp-protocol` | 3 | 3 | 3 |
| `13-engineering-decisions` | 3 | 3 | 3 |

## What this change does

Six files, in two complete mirror groups. Each group gains one metadata block on the root source and
one on each mirror; the body of every file is byte-identical to its previous content.

| path | before blob | after blob | bytes | added | `--numstat` |
|---|---|---|---|---|---|
| `07-agent-integration/inference-boundary-model.md` | `e2d5cb6abd9ec40da6e3680531de5944fc8b14df` | `9afd414bb5f3224f28f605fd854ff06d9fd4ceb2` | 13533 → 15004 | +1471 | 46 / 0 |
| `docs/en/07-agent-integration/inference-boundary-model.md` | `e2d5cb6abd9ec40da6e3680531de5944fc8b14df` | `a1b7f7555cc0231860b325d1c4ca4890ce6d50a4` | 13533 → 14927 | +1394 | 45 / 0 |
| `docs/zh-CN/07-agent-integration/inference-boundary-model.md` | `ba3a737b7b4fcf1a4a88e4f99667ef2f2ee4bbea` | `8b208da3f013cfb572f3c7d390a1592bb8bca180` | 14022 → 15386 | +1364 | 45 / 0 |
| `07-agent-integration/telemetry-model.md` | `9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0` | `7afef508b3d83c4381eb9cfc91c5dd9d03317856` | 15077 → 16497 | +1420 | 46 / 0 |
| `docs/en/07-agent-integration/telemetry-model.md` | `9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0` | `5a23480422d1a74467bd20fb5cce542d1d25ef9c` | 15077 → 16429 | +1352 | 45 / 0 |
| `docs/zh-CN/07-agent-integration/telemetry-model.md` | `a8141952eed383a3827f3d4eb26aa9345740ca24` | `205338cc8fa2d7d337467d138919f94602b8aec9` | 15589 → 16911 | +1322 | 45 / 0 |

`git diff --numstat` reports zero deleted lines in all six files: the insertion is exactly the
metadata block (46 lines on a root source, 45 on a mirror, which carries `source:` instead of the
`en:`/`zh-CN:` pair). The two `docs/en` files had the same pre-change blob as their root source —
they were byte-identical copies — which is why the before blob ids repeat.

Structure follows the already-classified group `07-agent-integration/agent-integration-guide.md`:

- root source: `canonical_status: Non-Canonical`, `normative_status: Informative`, and a
  `bilingual_counterpart` block listing both mirrors;
- each mirror: `bilingual_counterpart.source` naming the root source, plus the sibling mirror;
- `domain`, `role` and `normative_status` agree across the group (DM-12 requirement);
- `decision_status: Draft`, `approver: null`: no approval exists for these documents and none is
  claimed here.

## What this change does not do, and why (measured, not assumed)

### 16 of the 22 mirrors in 07/08/13 are orphans — `ORPHAN_SKIPPED`

For 9 of the 11 pairs the root source does not exist in the tree, so the mirror names nothing:

- `07-agent-integration`: `phase-3.6-c-submit-cross-authority-causal-order-contract.md`,
  `phase-3.6-final-request-evidence-contract.md`,
  `phase-3.8.19-c-exact-review-h-fullpath-38-test-current-head.md`
- `08-bmcp-protocol`: `adapter-capability-and-applied-attestation.md`, `bmcp-guide.md`,
  `phase-3.6-identity-binding-consumer-conformance-status.md`
- `13-engineering-decisions`: `req02-fts5-vs-like-benchmark.md`, `req02-fts5-vs-like-decision.md`,
  `technology-architecture-overview.md`

DM-12 admits no shape for an orphan mirror. Measured on `docs/{en,zh-CN}/08-bmcp-protocol/bmcp-guide.md`
(probe reverted immediately, not part of this change):

```
FAIL: 4 error(s)
  DM-12 docs/en/08-bmcp-protocol/bmcp-guide.md: bilingual_counterpart.source does not exist: 08-bmcp-protocol/bmcp-guide.md
  DM-12 docs/zh-CN/08-bmcp-protocol/bmcp-guide.md: bilingual_counterpart.source does not exist: 08-bmcp-protocol/bmcp-guide.md
  DM-12 docs/en/08-bmcp-protocol/bmcp-guide.md: names 08-bmcp-protocol/bmcp-guide.md as its source, but that file is not a classified governed document
  DM-12 docs/zh-CN/08-bmcp-protocol/bmcp-guide.md: names 08-bmcp-protocol/bmcp-guide.md as its source, but that file is not a classified governed document
```

Omitting `source` does not help either: a file under a language mirror root without it is refused
for belonging to no group. Creating the missing canonical would be a new canonical, which this
unit's brief forbids, so these 16 files are left untouched and listed here instead of guessed at.

### The 58 frozen `13-engineering-decisions` gaps stay frozen

`scripts/bilingual-baseline.txt` holds 77 entries, distributed as
`13-engineering-decisions: 58`, `06-memory-context: 10`, `08-bmcp-protocol: 4`,
`14-ai-development: 4`, `00-governance: 1`. The 58 are root sources under
`13-engineering-decisions/domain-model-research/` and `13-engineering-decisions/technology-research/`
(plus `technology-architecture-blueprint.md`) that carry no `docs/en` and no `docs/zh-CN` mirror.

They are already unclassified (the gate prints `13-engineering-decisions: 0/58 classified`). Adding a
metadata block to one of them was measured, not assumed — probe on
`13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md`, reverted immediately:

```
::error::13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md requires all counterparts changed in this PR: 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md, docs/en/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md, docs/zh-CN/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md
Bilingual documentation gate: FAIL
```

The two required mirrors do not exist. Creating them would resolve frozen gaps, and a resolved gap
must then be removed from `scripts/bilingual-baseline.txt` in the same change — a baseline edit that
only an Owner decision may make. This task therefore does not change the 77-entry baseline, adds no
gap and closes none: `13-engineering-decisions` remains `0/58` classified, deliberately.

## Gate measurements

Before = `4326669c` (branch point, 6 files unmodified); after = `c27a23df` plus the `origin/main`
merge. All figures are the gate's own stdout.

| gate | before | after |
|---|---|---|
| `check_document_management.py` (whole tree) | 942 governed, 496 classified, 446 unclassified, 0 rule violations, INCOMPLETE (backlog) | 942 governed, 502 classified, 440 unclassified, 0 rule violations, INCOMPLETE (backlog) |
| `check_document_management.py --require-changed origin/main` | n/a (no change) | PASS (incremental): no GOV-DOC-002 violations; 502 classified, 440 unclassified |
| `07-agent-integration` bucket | 6/8 classified | 8/8 classified |
| `docs` bucket | 173/343 classified | 177/343 classified |
| `13-engineering-decisions` bucket | 0/58 classified | 0/58 classified |
| `check_bilingual_docs.py` (incremental) | NOT_APPLICABLE — zero changed paths, nothing judged | PASS: `bilingual baseline: 77 frozen, 0 new gaps` (6 changed paths inspected) |
| `check_bilingual_docs_full.py` + ratchet | 77 entries, FAIL-as-baseline | `baseline=77 current=77 regressions=0 fixed=0`, PASS — failure set matches the baseline exactly |
| `test_check_document_management.py` | 326/326 passed | 326/326 passed (unchanged by this work item) |
| `test_check_bilingual_docs.py` | 15 tests OK | 15 tests OK |
| `test_gate_normative_roots` | 52 tests OK | 52 tests OK |
| `scripts/ci/check_line_endings.py` | 0 violations | 1629 files, 0 violations |
| `scripts/ci/check_repository_hygiene.py --base --head` | n/a | new-file admission 0 paths checked, manifest consistency violations=0 |

The frozen baseline is unchanged by this work item: `baseline=77 current=77 regressions=0 fixed=0`
before and after.

## Limits of this record

- No semantic-equivalence claim is made between the English and the Chinese mirror text. This change
  only inserts metadata; the gate checks structure, not translation quality.
- No claim that the 22-file defect in these three directories is closed. 6 of 22 are classified here;
  the other 16 are recorded as `ORPHAN_SKIPPED` with the gate error that refuses them.
- No claim about `00/01/02/06` (unit corpus-a) or `03/04/05/09` (out of scope for every unit in this
  batch).
- No checker, workflow, schema, registry or baseline file is modified by this work item.
