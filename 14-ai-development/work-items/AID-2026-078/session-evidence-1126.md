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
    last_verification_note: "The implementation evidence in section 1 was produced by commands run in pull request #1198 on branch feat/078-manifest-gate on 2026-11-26 and is reproduced verbatim from that run. It records what was executed and what was not claimed; it asserts no review, no acceptance and no merge."
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

# Session evidence — AID-2026-078, implementation session

This file is the evidence record of the session that implemented the gate, kept separate from
`session-evidence-266.md`, which is the evidence record of the session that measured the gap and
registered the work item. Two sessions, two records: the manifest carries one entry per session,
and attributing implementation work to the measuring session's Issue would assert a link that
does not exist.

---

## 1. Implementation evidence (branch `feat/078-manifest-gate`, PR #1198)

The gate this work item registered was written in pull request #1198 on branch
`feat/078-manifest-gate`, and the commands below were run there on 2026-11-26 against the
branch working tree, with output reproduced as recorded in the job log and in the PR body.
`python3 scripts/ci/check_manifest_parse.py` printed `Manifest parse: 55 manifests found, 55
parsed, 0 failed.` and exited 0, with `ls 14-ai-development/work-items/*/manifest.yaml | wc -l`
also reporting 55 and `ls -d 14-ai-development/work-items/AID-*/ | wc -l` reporting 54 — the
one-file difference being `FIX-2026-P1-T1/manifest.yaml`, which is why AC1's measurement now
counts manifest files rather than `AID-*` directories.
`cd scripts/ci && python3 -m unittest test_check_manifest_parse` ran 13 tests and reported
`OK`; `python3 scripts/ci/check_repository_hygiene.py` reported `violations=0` with
`manifests=54 in_scope=52 excluded_by_record_type=2 unrecognized=0`; and
`py -c "import yaml,io,glob;[yaml.safe_load(io.open(p,encoding='utf-8')) for p in glob.glob('14-ai-development/work-items/*/manifest.yaml')]"`
exited 0. A negative test run in the same session, over a temporary tree whose single
manifest declared `related_prs` twice, exited 1 and named that manifest's path in the
`::error::` line. Two limits are stated rather than implied: the test that runs over the
real tree asserts that the printed count equals the number of manifest files actually
present, and does not pin that number, because a pinned count already disagreed with the
tree; and the workflow step runs in the existing `repository-hygiene` job, which is not a
required status context, so this evidence supports "runs on every pull request" and not
"blocks a merge".
