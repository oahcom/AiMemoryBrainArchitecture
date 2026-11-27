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
        - "14-ai-development/work-items/AID-2026-321/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Normalised task snapshot authored in this session; prompt provenance is NOT_VERIFIED and no approval or execution result is implied."
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
    canonical_scope: "Normalised task prompt snapshot for AID-2026-321 platform-scoped acceptance measurement correction."
    canonical_scope_id: "ai-development/aid-2026-321-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-321"
      - "prompt snapshot"
      - "platform-scoped measurements"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-321 — Prompt Snapshot

## 1. Task

Close GitHub issue #1269 by correcting the AC1 and AC5 measurement text in:

`14-ai-development/work-items/AID-2026-079/manifest.yaml`

The change is documentation-only. Replace the existing platform-ambiguous measurements with measurements that explicitly state both Windows and Ubuntu CI totals and give the exact command that reproduces each total.

Do not change either acceptance criterion, any other manifest key, or any file outside the declared scope.

## 2. Authoritative operator measurements

The operator supplied the following observations for the current tree, measured on 2026-11-27 against commit:

`229c0a6b51f4c761ed969337f6ddf7d0bbbb7d0c`

The two platforms used the same test and gate blobs.

### Windows 11, Python 3.12

Command:

```text
python scripts/test_check_document_management.py
```

Observed exit code: `0`.

Observed final output:

```text
371/371 passed
1 skipped, 1 registered of 5 allowed: T68c a real 0o000 directory is reported by path (integration)
```

The suite-level skip line identifies T68c. The in-run skip text says:

```text
[skip] T68c a real 0o000 directory is reported by path (integration)  (running as root: mode bits cannot deny access)
```

The wording is inaccurate on Windows because `os.geteuid` is absent. Correcting that message is explicitly outside this task.

### Ubuntu latest, required context GOV-DOC-002 metadata checks

Command:

```text
python3 scripts/test_check_document_management.py
```

Observed job: `140346856045`, commit `229c0a6b`.

Observed output:

```text
[ok  ] T68c a real 0o000 directory is reported by path (integration)
372/372 passed
```

A search over the complete job log found no occurrence of `registered of`. The suite emits no suite-level skip summary on Ubuntu because T68c executes and the final `SKIPPED` collection is empty. The two T68c skip lines inside T72 meta-tests are deliberately constructed and deleted; they are not the suite tally.

### Windows counterfactual

The operator neutralised the `git()` refusal in `scripts/check_document_management.py` by changing `except OSError:` to `except ZeroDivisionError:`, ran the same test command, and restored the file immediately afterwards.

Observed exit code: `1`.

Observed failure:

```text
[FAIL] T92a git() spawn failure is refused by the caller, not raised  exit 2, matching lines [], output "::error::Unable to determine Git history completeness: [Errno 2] No such file or directory: 'git'\n"
370/371 passed
1 skipped, 1 registered of 5 allowed: T68c a real 0o000 directory is reported by path (integration)
```

This Windows counterfactual is measured.

### Ubuntu counterfactual

The Ubuntu counterfactual is **arithmetic only**, not measured. Removing one successful T92a case from the observed Ubuntu baseline gives 371/372 if the denominator remains unchanged. No Ubuntu counterfactual execution is claimed.

## 3. Platform-dependent cause

The existing T68c conditional is:

```python
if hasattr(os, "geteuid") and os.geteuid() != 0:
    ... record("T68c a real 0o000 directory is reported by path (integration)", ...)
else:
    skip("T68c a real 0o000 directory is reported by path (integration)",
         "running as root: mode bits cannot deny access")
```

On Windows, `os.geteuid` is absent, so T68c is skipped and does not add a result. On Ubuntu, the runner has `geteuid` and is non-root, so T68c records a passing result. This accounts for the one-case difference between the platform totals.

The task does not change this code or the skip message.

## 4. Required manifest correction

Replace only the `measurement` scalar for AC1 and AC5 in AID-2026-079.

Both measurements must:
- state Windows 371/371 and Ubuntu 372/372;
- identify the exact command used on each platform;
- identify the measured commit `229c0a6b51f4c761ed969337f6ddf7d0bbbb7d0c`;
- identify measurement date `2026-11-27`;
- describe the Windows T68c skip and Ubuntu T68c pass accurately;
- preserve the T93a-T93h same-invocation statement in AC5;
- state that the totals are tree- and platform-scoped observations.

AC1 must additionally:
- retain the measured Windows counterfactual 370/371 and the exact T92a failure;
- label Ubuntu 371/372 as arithmetic only, not a measurement.

Do not remove the platform totals in favour of invariants alone.

## 5. Scope and exclusions

Permitted paths:
- `14-ai-development/work-items/AID-2026-079/manifest.yaml`, AC1 and AC5 measurement values only;
- the new `14-ai-development/work-items/AID-2026-321/` directory;
- one new row in `14-ai-development/work-items/INDEX.md`.

Forbidden changes:
- `scripts/test_check_document_management.py`;
- `scripts/check_document_management.py`;
- any workflow, required status context, branch-protection setting or production code;
- any other AID-2026-079 manifest field or acceptance criterion;
- any change to T68c behavior or its wording;
- any unrelated work item or index row.

If a code change is considered necessary, it must be argued explicitly and separately; the default is documentation-only.

## 6. Provenance and claims

The measurements above were supplied by the operator. They are not executions performed by this authoring session.

The Windows counterfactual was measured by the operator. The Ubuntu counterfactual is arithmetic only.

Record the base commit as `229c0a6b51f4c761ed969337f6ddf7d0bbbb7d0c`.

Do not claim:
- CI ran on the changed branch;
- the changed branch passed GOV-DOC-002;
- the Session Evidence validator passed;
- independent review occurred;
- Owner acceptance occurred;
- a PR was merged;
- issue #1269 was closed.

The prompt digest and byte count in the manifest and session-evidence entry are placeholders. The operator must calculate them from the final bytes of this `prompt-v1.md` and replace both placeholders. This prompt snapshot must not contain its own digest.

## 7. Required deliverables

Provide:
1. A patch replacing only AC1 and AC5 measurement text in AID-2026-079.
2. Complete AID-2026-321 `manifest.yaml`, `prompt-v1.md`, `evidence.md`, and `session-evidence.md`.
3. One INDEX row immediately after the table header, with nine cells.
4. A concise statement of whether code changes are required and a list of files touched.

The work item remains pending verification, independent review and Owner acceptance until those events are separately evidenced.
