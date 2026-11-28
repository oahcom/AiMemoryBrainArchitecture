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
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Local suite passes; independent review is pending."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "work-item-uniqueness"
      - "shared-id"
      - "duplicate-declaration"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Evidence — AID-2026-345

All figures below were measured in this session against `origin/main`
`daa935f7a7ecc808f1775be8cf153cf715961b08` and re-measured after merging
`origin/main` at `bf7fd91cbb3ccad4d2dba5662b14b849e446d706`.

## 1. The two recorded collisions

| id | merge that took the id | the branch that lost |
|---|---|---|
| `AID-2026-327` | PR #1495, `79b38c944480926195edd64e3d751a1ce5010fb7`, 2026-11-28T03:11:54Z | PR #1506 (`ccbc4909c`), four add/add conflicts on `evidence.md`, `manifest.yaml`, `prompt-v1.md`, `session-evidence.md`, renumbered to `AID-2026-341` |
| `AID-2026-292` | PR #1483, `cc3e9ed9dbe0eb860a583bc51d6b086248624766` | PR #1467 (`df393073e`), closed unmerged, still naming `AID-2026-292`; Issue #264 and Issue #1332 also cite it |

`79b38c944` touches exactly the four record files plus `INDEX.md`. Nothing in
the required-check set rejected the second claim: the collision surfaced as a
Git conflict during the merge, which is what the adjudication forbids recording
as a gate success.

## 2. Why the existing gate never fired

`scripts/ci/check_work_item_uniqueness.py` already carried the claim rule:

- `DEFAULT_REGISTRY = "14-ai-development/work-items/registry/work-item-claims.yaml"` (L48)
- `BLOCKING_STATUSES = {CLAIMED, MERGED}` (L54)
- `load_claims()` (L251–299) reads only the target tree and is fail-closed when
  the candidate supplies the ledger
- the blocking loop (L373–394) exempts a claim owned by the same pull request

`git ls-tree origin/main -- 14-ai-development/work-items/registry` returned
nothing, so `load_claims` returned `[], "absent (no ledger in either tree)"` and
the blocking loop had no data. The only ledger-shaped file in the repository was
`aid-ledger.yaml` on the unmerged `origin/aid-ledger` branch, which no workflow
reads.

The workflow also called the checker with `--base` and `--head` only, so the
own-claim exemption was unreachable: had the ledger held data, every claiming
pull request would have failed on its own claim.

## 3. Platform facts (live API, this session)

| fact | value |
|---|---|
| `strict` | `false` |
| required contexts | 17 |
| `enforce_admins` | `true` |
| `allow_force_pushes` | `false` |
| required reviews | none |
| merge queue | GraphQL `repository.mergeQueue(branch: "main")` returned `null` |
| `concurrency` | all 12 workflows group by head SHA or pull request number; none groups by work-item id |

## 4. What changed

| file | change |
|---|---|
| `scripts/ci/check_work_item_uniqueness.py` | `--registry-ref` reads the ledger from the authoritative ref; `EXPIRED` added to the known states; ownership exemption narrowed to a matching `CLAIMED`; introduced ids must carry a claim; `WORK_ITEM_ID_UNREGISTERED` and `WORK_ITEM_ID_RELEASED` are distinct verdicts; duplicate current claims are a violation |
| `scripts/ci/claim_work_item.py` | the writer: read the ref, refuse a held id, commit one file, push without force; a rejected push is `LOST_THE_RACE` and is never retried |
| `scripts/ci/migrate_work_item_claims.py` | deterministic ledger construction from the main tree, Git history and the GitHub API |
| `scripts/ci/test_work_item_claims.py` | 13 tests for the authoritative ledger, the writer and the race |
| `.github/workflows/document-management.yml` | fetches the ledger ref, passes the pull request identity, resolves the merge-group pull request and fails closed when it cannot, keeps the push run on the tree rule |

## 5. Migration result

```
main_work_item_directories: 164
legacy_ledger_entries: 64
verified_merged: 165
verified_claimed: 3
verified_abandoned: 2
unresolved: 0
unverified_claims: 3
  - AID-2026-262: legacy OCCUPIED_BY_OTHER without a resolvable carrier
  - AID-2026-263: legacy RESERVED without a resolvable carrier
  - AID-2026-313: legacy RESERVED without a resolvable carrier
missing_manifest: 0
no_pull_request: 7
duplicate_ids: 0
ownership_conflicts: 0
migration_status: READY
```

The seven ids with no pull request are recorded with their first adding commit
as the evidence reference; no number was guessed. The three unverified legacy
holds are recorded as `CLAIMED` with a null pull request and a note, so they
keep holding the number until their owner re-points them.

## 6. Tests

```
python scripts/ci/test_work_item_uniqueness.py    Ran 28 tests ... OK
python scripts/ci/test_work_item_claims.py        Ran 13 tests ... OK
```

## 7. The concurrent claim experiment

Sandbox remote seeded with `origin/main` and the bootstrapped ledger commit
`0a3fc6e476f89e66ff3bcdaf3b6a10a2d6903ece`; two clones, two branches, one id,
launched at the same moment.

```
--- branch A (pull request 9001) exit=0
CLAIMED AID-2026-903 for PR 9001 at fac022e8ce160c63d7339c45fcd33cff4502c20f
--- branch B (pull request 9002) exit=3
CLAIM LOST_THE_RACE: the authoritative ref moved while this claim was being
built; re-read the ledger, re-scan the id, and try again. Do not rebase this
claim onto the new ref and re-push it.
remote: error: cannot lock ref 'refs/heads/work-item-claims': is at
fac022e8ce160c63d7339c45fcd33cff4502c20f but expected ...
```

The losing branch then added its own `AID-2026-903/manifest.yaml` and ran the
gate:

```
--- gate on the losing branch (PR 9002, id AID-2026-903) exit=1
VIOLATION: AID-2026-903 is already CLAIMED in the claim ledger by pull request
9001 (oahcom/AiMemoryBrainArchitecture)
WORK-ITEM UNIQUENESS: VIOLATION (... introduced=1 duplicate_declarations=0
registry=refs/heads/work-item-claims (60d0c0bea4631f85c5da4ca48db4d094c16d5361))
```

A different-id race at the same moment proves the guard is not a global
one-winner lock:

```
--- different-id race: branch A exit=0
CLAIMED AID-2026-904 for PR 9001 at 60d0c0bea4631f85c5da4ca48db4d094c16d5361
--- different-id race: branch B exit=3
CLAIM LOST_THE_RACE: ...
--- branch B retry after re-reading the ref: exit=0
CLAIMED AID-2026-905 for PR 9002 at fc0b6f46485687af0e4c4564927c2c7a4d73354c
```

## 8. Residual gaps, stated plainly

- A direct push to `main` is not evaluated against the ledger: the push run
  keeps the pre-existing tree rule because the event carries no pull request
  identity. The governed path is the pull request.
- `merge_group` resolution depends on the GitHub API; when it cannot resolve
  exactly one open pull request the run is `INCOMPLETE`, not a pass. The merge
  queue is not enabled today.
- Write access to `work-item-claims` is not separated by a dedicated GitHub
  App. Anyone who can push to the repository can move the ref; that is a
  permission property of the repository, not of this mechanism.
