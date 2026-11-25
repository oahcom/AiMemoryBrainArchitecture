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
      last_verified_date: "2026-11-25"
      last_verification_note: "All five sections were produced by scripts run against main 68591920 on 2026-11-25 and are reproduced verbatim. The one thing this record cannot support - that an earlier draft's repairs were needed - is stated as not supported rather than argued."
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

# Session evidence — AID-2026-078

## Session role / use case

MEASURER. This session measured the manifest-parse coverage of this repository and
registered the gate that is missing, as `AID-2026-078`. It did not implement the gate:
`implementation.status` is `NOT_STARTED` and no file under `scripts/ci/` was written.

## Actual AI input

The instruction that produced this record, verbatim:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。以最高效率去执行，动用所有能动用的资源，使用最多的子线程子代理

and, when the session paused for a boundary decision:

> 请继续执行任务

The constraint `不能自己动手写代码` is why this work item registers a gate rather than
writing one, and why `implementation.status` is `NOT_STARTED` rather than
`IMPLEMENTED_IN_BRANCH`.

## AI-visible output

The output visible to the user consists of: the measurements in sections 1-5 below, the
three files in this directory (`manifest.yaml`, `prompt-v1.md`, this record), one row added
to `14-ai-development/work-items/INDEX.md`, one corrected `AID-2026-057` INDEX row, and
pull request #1137. No checker was written.

Two subagent sessions were spawned to run the register sweep in parallel and both
terminated with `upstream connection lost`; the sweep was then performed directly by this
session, and the results below are this session's own measurements rather than theirs.


**Role:** MEASURER. **Session:** req05 convergence, identity NOT_RECORDED.
**Measured at:** `68591920` (origin/main at the time of measurement), 2026-11-25.

## 1. Coverage of the only strict-parse job

Enumerated the trigger paths and the job body of
`.github/workflows/aid-2026-001-manifest-validation.yml`:

```
on:
  pull_request:
    paths:
      - "14-ai-development/work-items/AID-2026-001/manifest.yaml"
      - ".github/workflows/aid-2026-001-manifest-validation.yml"
  push:
    branches: [main]
    paths:
      - "14-ai-development/work-items/AID-2026-001/manifest.yaml"
      - ".github/workflows/aid-2026-001-manifest-validation.yml"
```

and, inside the job:

```python
path = Path("14-ai-development/work-items/AID-2026-001/manifest.yaml")
```

One path, named twice. The loader below it is a correct duplicate-key-rejecting
`UniqueKeyLoader`, and it carries two regression guards (top-level and nested duplicate
keys). The machinery is right; the coverage is one file.

## 2. Corpus state at 68591920

Enumerated `14-ai-development/work-items/AID-*/manifest.yaml` and parsed each with a
`SafeLoader` subclass whose `construct_mapping` raises on a repeated key:

```
manifests on disk: 50
strict parse ok:   50
strict parse fail: 0 []
```

So the ordering constraint `b34c8e37` described — a gate cannot be made required while
existing files fail it — is satisfied at this commit. That is the precondition for this
work item, not a result of it.

## 3. The hygiene checker does not parse YAML

Read `scripts/ci/check_repository_hygiene.py`:

```
check_repository_hygiene.py imports yaml: False
check_repository_hygiene.py has safe_load: False
CHECK_VERSION = "2026-11-24.8"
```

It reads manifest content as text and extracts top-level scalars with
`_top_level_manifest_scalar`, a pattern applied to unindented lines. Its output line
`manifests=50 violations=0` therefore reports on that scan. It cannot fail on a document
that no parser can load, because it never builds one.

## 4. The silent-loss case

`b34c8e37` records that `AID-2026-029` declared `related_prs` twice — `[356]` at line 8
from `d8fdf54`, `[]` at line 9 from an earlier `84b1255` — and that PyYAML took the last
while the project's line parser took the first. Reproduced the substance of that on the
pre-repair blob at `30c7277e`:

```
AID-2026-029  duplicate key: 'related_prs'
              line 9, column 1
```

and under plain `yaml.safe_load` the same blob loads without error and returns
`related_prs = []`, with PR 356 absent. This is why AC2 asserts both halves — that the
default loader succeeds and that the check does not — rather than only the second.

## 5. Collision with an earlier draft of this same work

Recorded because it changes what this work item may claim.

An earlier draft, prepared in this session before `origin/main` was re-fetched, registered
the same gap under the id `AID-2026-074` and independently repaired the same four manifests
(`023`, `029`, `040`, `055`) that `b34c8e37` had already repaired. On fetching, `origin/main`
had advanced `30c7277e..68591920` and already contained:

- a merged `AID-2026-074` for an unrelated subject (the declared-versus-protected context
  set, Issue #1029), with its own prompt and `session-evidence-1029.md`;
- `b34c8e37`, which made the identical four repairs, with byte-identical parsed values.

Consequences, all applied:

- the id `AID-2026-074` was abandoned rather than re-used; this work item is `075`;
- the four repairs were dropped from this branch, because re-applying them would have
  written a second, conflicting version of files main already has;
- the earlier draft's claim to have "found" the defect is withdrawn. `b34c8e37` found it.
  What remains to this work item is the gate, which that commit explicitly deferred.

The earlier draft's review report and session evidence are not carried into this work item.
They measure a state of the tree that no longer exists, and a review of a withdrawn
registration is not evidence about this one.

## 6. What this record does not claim

- It does not claim the four manifests were ever unparseable *for this work item's benefit*.
  Two sessions reached the same repair independently; the record attributes it to
  `b34c8e37` because that is the one that landed.
- It does not claim the new check will be a required status context. AC4 requires it to run
  on pull requests; promotion into branch protection is out of scope and is not authorised.
- It does not claim any semantic validation of manifest contents. AC5 exists precisely to
  keep a green run from being read that way.
- `executed_prompt_provenance` is `NOT_VERIFIED`: the prompt was written before the
  measurements above and has not been re-read against them line by line.

## 7. Implementation evidence (branch `feat/078-manifest-gate`, PR #1198)

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
