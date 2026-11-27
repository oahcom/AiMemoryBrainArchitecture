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
      last_verification_note: "Operator-provided observations are transcribed; this record and the proposed changes have not been independently verified by repository gates."
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
    canonical_scope: "Operator-supplied baseline measurements and provenance distinctions for AID-2026-321."
    canonical_scope_id: "ai-development/aid-2026-321-measurement-evidence"
    canonical_scope_keywords:
      - "AID-2026-321"
      - "operator measurements"
      - "platform totals"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-321 — Evidence

## 1. Purpose and evidence boundary

This record preserves the operator-supplied observations that motivate the correction to AID-2026-079 AC1 and AC5.

The baseline was measured on 2026-11-27 against commit:

`229c0a6b51f4c761ed969337f6ddf7d0bbbb7d0c`

The operator reports that the test and gate blobs were the same on both platforms. These observations are not executions performed by this authoring session.

## 2. Windows baseline — operator measured

Platform: Windows 11, Python 3.12.

Command:

```text
python scripts/test_check_document_management.py
```

Exit code: `0`.

Verbatim final output:

```text
371/371 passed
1 skipped, 1 registered of 5 allowed: T68c a real 0o000 directory is reported by path (integration)
```

Verbatim in-run skip line:

```text
[skip] T68c a real 0o000 directory is reported by path (integration)  (running as root: mode bits cannot deny access)
```

The output wording `running as root` is inaccurate on Windows because `os.geteuid` is absent. This task deliberately does not modify that message or its implementation.

## 3. Ubuntu baseline — operator measured

Platform: `ubuntu-latest`, required context `GOV-DOC-002 metadata checks`, job `140346856045`, commit `229c0a6b`.

Command:

```text
python3 scripts/test_check_document_management.py
```

Verbatim relevant job output:

```text
2026-11-27T06:19:25.7067578Z   [ok  ] T68c a real 0o000 directory is reported by path (integration)
2026-11-27T06:19:25.7140302Z 372/372 passed
```

The operator searched the complete 276291-byte job log and reports that `registered of` does not occur anywhere in it.

The two `[skip] T68c` lines inside T72 meta-tests are deliberately constructed skip entries that are deleted by those probes. They are not the suite's tally. The suite-level `SKIPPED` collection ends empty on Ubuntu, so no suite skip summary is printed.

## 4. Windows counterfactual — operator measured

The operator temporarily changed the exception handler in `scripts/check_document_management.py` from `except OSError:` to `except ZeroDivisionError:`, thereby neutralising the refusal under test. The original file was restored immediately afterwards and the operator reports the tree clean.

Command:

```text
python scripts/test_check_document_management.py
```

Exit code: `1`.

Verbatim failure and final output:

```text
[FAIL] T92a git() spawn failure is refused by the caller, not raised  exit 2, matching lines [], output "::error::Unable to determine Git history completeness: [Errno 2] No such file or directory: 'git'\n"
370/371 passed
1 skipped, 1 registered of 5 allowed: T68c a real 0o000 directory is reported by path (integration)
```

This is a measured Windows counterfactual. It is not evidence of an Ubuntu counterfactual run.

## 5. Ubuntu counterfactual — arithmetic only

No Ubuntu counterfactual was executed or supplied.

The value 371/372 is arithmetic only: subtracting the one successful T92a case from the observed 372/372 baseline while keeping the denominator fixed at 372. It must not be described as a measured result, a CI run, or a reproduced failure.

## 6. Explanation of the platform total difference

The operator supplied the current T68c conditional:

```python
if hasattr(os, "geteuid") and os.geteuid() != 0:
    ... record("T68c a real 0o000 directory is reported by path (integration)", ...)
else:
    skip("T68c a real 0o000 directory is reported by path (integration)",
         "running as root: mode bits cannot deny access")
```

On Windows, `hasattr(os, "geteuid")` is false, so the case is skipped and does not enter the result count. On Ubuntu, `geteuid` exists and the runner is non-root, so the case records a passing result. The one-case difference is therefore an existing platform-dependent branch, not a missing test.

The implementation of this conditional and the skip text are outside the scope of this documentation correction.

## 7. Measurement interpretation

| Platform | Command | Baseline | T68c accounting |
|---|---|---:|---|
| Windows 11 / Python 3.12 | `python scripts/test_check_document_management.py` | 371/371 | One registered skip |
| Ubuntu latest / GOV-DOC-002 | `python3 scripts/test_check_document_management.py` | 372/372 | Passing result; no suite-level skip summary |

Both totals are observations tied to the same measured commit and date. They are not platform-independent constants. A later tree can change either total, so future measurements must preserve the commit and command alongside the count.

## 8. Scope of the documentation correction

The proposed AID-2026-079 manifest change:
- replaces only AC1 and AC5 measurement text;
- preserves both platform totals;
- gives the reproduction command for each platform;
- records the measured commit and date;
- distinguishes the measured Windows counterfactual from the arithmetic-only Ubuntu projection;
- retains AC5's T93a-T93h same-invocation statement.

No source code or test behavior is changed by this proposal.

## 9. Verification status and non-claims

The supplied baseline and Windows counterfactual outputs are operator-provided evidence. They do not establish that the proposed changed branch has passed CI.

At authoring time:
- no CI run of the changed branch is claimed;
- no GOV-DOC-002 result for the changed branch is claimed;
- no Session Evidence validator result for the new documents is claimed;
- no independent review is recorded;
- no Owner acceptance is recorded;
- no PR merge is claimed;
- issue #1269 remains open.

The operator must calculate the prompt snapshot's final SHA-256 and byte count and substitute the placeholders in the manifest and session-evidence record before running the applicable gates.
