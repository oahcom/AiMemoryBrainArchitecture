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
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count in this file was produced by the commands quoted, in the session that wrote it, on the commits named. The concurrency table is two runs of six processes on one commit with only the fixture lines changed; the binding table is five mutations, each restored and its sha256 checked."
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

# AID-2026-102 prompt snapshot

**Provenance: assembled after the session, not captured live.** This file was written when the pull
request was being prepared, from the three issue rulings the session actually worked to. It is not a
transcript and it is not the text the session was handed at the start. `prompt_status` is
`RECORDED_NOT_FROZEN` and `executed_prompt_provenance` is `NOT_VERIFIED` for that reason: the
sha256 below matches this file, and nothing claims it matches the original instruction.

## What the session was asked

Continue work on the repository's open issues, taking each to a ruling and, where the ruling calls
for code, to a change that can be merged.

## The three subjects, as the session found them

**#989** — six fixtures in `scripts/test_check_document_management.py` build their "outside the
repository" target at a fixed name under `Path(tmp).parent`, which is the shared system temp root.
Two processes running the file at once therefore race, and the loser reports a DM-14 assertion
against a gate that did nothing wrong. The issue's own measurement isolates the cause: three serial
runs green, six concurrent runs with a shared `TMPDIR` red two or three times, six concurrent runs
with a per-process `TMPDIR` green.

**#988** — two claims. That the bilingual-mirror symlink branch has no case observing it, and that
the enum-on-a-non-None-kind rule has none either because `T63`'s fixture trips the YAML parser's
duplicate-key detector first.

**#827** — an audit of the gate's error emissions. Its latest ruling narrowed the open work to five
specific emitters, each to be bound by a case that asserts its message prefix, and moved the
ratchet harness (`scripts/mutation_report.py`) out of scope because the file does not exist.

## What was required of the work

1. Measure before asserting. A claim that a branch is unbound is established by deleting it and
   watching the suite stay green; a claim that it is bound is established by deleting it and
   requiring a named case to go red.
2. Correct the issue where the measurement contradicts it, rather than implementing the claim.
3. Do not touch `scripts/check_document_management.py`. Every branch in scope already exists and is
   correct; the defect is that nothing observed them.
4. Keep the change to one test file plus its work item.

## What the session was told not to do

- Not to fix `#989` by renaming the six paths with a pid or a uuid: that lowers the collision
  probability and leaves the fixture writing into a directory it does not own.
- Not to turn `ignore_errors=True` into `False`: on Windows a failed delete is normal, so that
  converts a concurrency defect into a platform-dependent crash.
- Not to add a shared-fixture helper across the suite: per-fixture ownership is what the tests
  already do everywhere except these six sites.
- Not to build `scripts/mutation_report.py` inside this change.
