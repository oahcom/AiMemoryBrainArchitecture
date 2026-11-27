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
        - "14-ai-development/work-items/AID-2026-197/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the dispatched task and what the implementing session did with it; the session identifier and the verbatim model input stream were not captured."
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
      - "gate"
      - "ratchet"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session Evidence — AID-2026-197

## Session role / use case

Gate-repair worker. The session was dispatched as a single unit inside a batch of parallel
workers, each taking one defect from the same defect inventory. This unit's remit was
narrow: two checkers whose output looked complete and was not.

The session's own judgement was limited to mechanism. It did not decide whether the six
movable references, the eight stale pointers or the 77 bilingual gaps should be repaired;
each of those is a document edit, and this unit was forbidden to make one.

## Actual AI input

The dispatching session supplied, in order:

- an assignment of the work tree `D:\code\wt-gates-a` on branch `fix/2026-11-27-gates-a`,
  based on `main` at `4326669c`, with the instruction to work only there and to merge
  `origin/main` before pushing;
- a common contract: how to take a provisional AID number without colliding, the required
  work-item file set, the block-style metadata requirement, the PR-body shape, the
  sixteen-context merge discipline, and a prohibition list (no branch-protection change, no
  Issue close, no required-context deletion, no unrelated file, no fabricated SHA, test
  output or gate result, no baseline edit);
- a unit brief naming two defects with their file, line ranges and measured symptoms:
  DEF-gates-08 in `scripts/check_source_revision_pointers.py` (a movable reference is
  reported and then ignored; every pointer is compared with `links[0]`) and DEF-gates-07 in
  `scripts/ci/gate_ratchet.py` (`-> ` truncation merges two failures on one path; items
  beginning with `OK`/`PASS`/`FAILED`/`Ran ` are dropped as summaries);
- the four things to produce: the two fixes, a falsifiable test for each, and a before/after
  measurement of both scripts on `main`;
- one instruction about redness: if the fix makes a script red, record the newly red items
  and the reason instead of widening the condition.

The serving model was `opencode-go/deepseek-v4.1-flash` because the primary pool returned
429 for both models. That is recorded because it changes which model produced the edits, not
what was asked for.

## AI-visible output

What the session produced, and what a reviewer can check without re-running anything:

1. **`scripts/check_source_revision_pointers.py`** — non-blob values enter `BAD`; the n-th
   live revision record is paired with the n-th live `Source:` line; a record without its
   own line is `UNRESOLVED`; plus `scan(root)` and an optional `--root`. Measured on this
   tree: exit 1 both before and after, `POINTERS=50 ACCURATE=16 STALE=8 NON_BLOB=6` both
   before and after, `BAD` 8 → 14.
2. **`scripts/ci/gate_ratchet.py`** — the arrow detail is kept; a summary line must name no
   repository object; the prefix test has a word boundary; a bare-path baseline entry
   covers exactly one `<path> -> …` item. Measured on this tree: `baseline=77 current=77
   regressions=0 fixed=0`, exit 0, before and after.
3. **`scripts/ci/test_gate_ratchet.py`** — 7 tests → 14, all passing on the fixed script.
   Against the pre-fix script, six of the seven new tests fail; the seventh pins the summary
   filter that must survive, so its premise is not a defect and only its item-fidelity
   assertion differs.
4. **`scripts/test_check_source_revision_pointers.py`** (new) — 5 tests, all passing on the
   fixed script and all failing against the pre-fix script. The falsification was also run
   end to end for the two pointer defects, because the pre-fix script has no `--root` and a
   test-time import would fail for the wrong reason:
   - `Source revision: main` only — before: exit 0, `BAD=0`, `NON_BLOB_REFERENCE=1`; after:
     exit 1, `BAD=1`.
   - two correct pointers, each with its own source line — before: exit 1, `ACCURATE=1`,
     `STALE=1`, the second pointer blamed on `00-governance/a.md`; after: exit 0,
     `ACCURATE=2`, `STALE=0`.
5. **`.github/workflows/repository-hygiene.yml`** — one line added to the existing
   unreachable-self-checks list, so `scripts/ci/check_test_reachability.py` keeps reporting
   every test file as reachable (`66 test files, 66 reachable`).
6. **Work record** — this directory's four files plus the EN and ZH-CN mirrors of
   `evidence.md`, and one INDEX row.

What the session did **not** do, and said so in the record: it did not wire
`check_source_revision_pointers.py` into a workflow, did not touch either bilingual
baseline or `scripts/ci/baselines/gate-wiring.txt`, did not repair the eight stale pointers
or the six movable references, did not delete the uncalled `--format schema` branch of
`gate_ratchet.py`, and did not close the tracking Issue. One consequence is recorded rather
than fixed: the comment in `gate-wiring.txt` still describes the script's failure as
"8 STALE pointers", which after this change understates it by six records.
