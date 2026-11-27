---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-255/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local command output recorded verbatim; no CI run asserted."
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
    canonical_scope: "Ratchet negative-contract transcript for AID-2026-255"
    canonical_scope_id: "ai-development/aid-2026-255-evidence"
    canonical_scope_keywords:
      - "manifest"
      - "blob-pin"
      - "sibling-key"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
AID-2026-255 ratchet-negative evidence

Scan commit: fda69aa803f9e9505231ccb333b44b151a823de3

Commits after this one touch only evidence files under this directory: this
transcript and `independent-review.md`. The checker reads only
`14-ai-development/work-items/*/manifest.yaml`, and no manifest changes after
the scan commit, so the 91-item set below is the set at the branch head. Verify
with:

  git diff --name-only fda69aa803f9e9505231ccb333b44b151a823de3..HEAD -- '14-ai-development/work-items/*/manifest.yaml'

which must print nothing. The path recorded in this preamble was
`ratchet-negative.log` when Owner A first authorized this file; the new-file
admission policy refuses `.log`, so the file was renamed to
`ratchet-negative.md` under a second owner amendment with the transcript
unchanged.

What this log is: the negative contract of the ratchet that AID-2026-268 landed,
exercised against the landed checker and the landed baseline.

The ratchet is not a green exemption. It fails when a failure appears that the
baseline does not list (regression), and it fails when a baseline item stops
failing (stale baseline). Cases 1 and 4 show the set is unchanged. Cases 2 and 3
show each failure direction actually fires. Case 2 drops one real item from a
copy of the current set, so the ratchet sees a new failure; case 3 adds an item
no run reports, so the ratchet sees a stale baseline.

What this log is not: evidence that CI ran. No workflow run, no merge and no
Owner acceptance is claimed here. The 91 baseline items are known unresolved
mismatches recorded by AID-2026-268; this delta does not fix them and does not
lower the baseline.

Command under test (as wired in .github/workflows/repository-hygiene.yml):

  python3 scripts/ci/check_manifest_blob_pins.py --commit HEAD \
    | sed -n '/^MISMATCH /p; /^PATH_MISSING /p; /^INCOMPLETE /p'

Transcript:

$ python3 scripts/ci/check_manifest_blob_pins.py --commit HEAD | sed -n '/^MISMATCH /p; /^PATH_MISSING /p; /^INCOMPLETE /p'
[checker exit 1; 91 items; scan commit fda69aa803f9e9505231ccb333b44b151a823de3]

--- case 1 control: baseline == current failure set ---
ratchet: C:/Users/ADMINI~1/AppData/Local/Temp/tmpv4jcoxvn/c1.base
ratchet: baseline=91 current=91 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
[exit 0]

--- case 2 regression: baseline omits one reported item ---
ratchet: C:/Users/ADMINI~1/AppData/Local/Temp/tmpv4jcoxvn/c2.base
ratchet: baseline=90 current=91 regressions=1 fixed=0
::error::ratchet regression (new failure not in baseline): MISMATCH session_evidence[0].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-v1.md declared=65474e7f0927d2dfeaad33814fdbd7d576635cc8a0e8d2a3a7441e3a65ab7317 actual=4881d6292e96154d5f7364816ae3e9977365e09b88e8475f4dd9d655e3e34a8c
ratchet: FAIL - 1 new failure(s) above baseline.
[exit 1]

--- case 3 stale: baseline carries an item the run no longer reports ---
ratchet: C:/Users/ADMINI~1/AppData/Local/Temp/tmpv4jcoxvn/c3.base
ratchet: baseline=92 current=91 regressions=0 fixed=1
::error::ratchet baseline is stale (no longer failing): MISMATCH a.b/never-reported path=x declared=0 actual=0
ratchet: FAIL - lower the baseline by 1 fixed item(s).
[exit 1]

--- case 4 landed baseline scripts/ci/baselines/manifest-blob-pins.txt ---
ratchet: D:/code/_wt-blobpins/scripts/ci/baselines/manifest-blob-pins.txt
ratchet: baseline=91 current=91 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
[exit 0]
