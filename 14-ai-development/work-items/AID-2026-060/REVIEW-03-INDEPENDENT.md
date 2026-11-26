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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "This record states the state round 3 actually examined, main at 767f2eaa. Round 3 returned REQUEST-CHANGES: the work item's premise was true at its base b80e5a40 but false at 767f2eaa after c6602739 (#1031)."
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

# REVIEW-03-060 — Independent review of AID-2026-060 manifest.yaml (round 3, increment)

- Reviewer: this session (r5c). Not the author of the manifest.
- Reviewed commit: 767f2eaa (detached worktree wt5-c, "current main")
- File under review: 14-ai-development/work-items/AID-2026-060/manifest.yaml
- Independence: session-level only, under PR-GOVERNANCE-001 §5 as amended by 2eb4e352 (#935). Same GitHub identity as the author — disclosed, not claimed as organizational independence.
- Scope: this round reviews the INCREMENT applied after the round-2 APPROVE (REVIEW-02-INDEPENDENT.md), namely edits (a) findings[F7].resolution and (b) acceptance_criteria[AC7]. It does not repeat round 2.
- Nothing inside the worktree was modified.

## Findings

### 1. Parse + id partition — PASS

Duplicate-key-detecting loader (`SafeLoader` subclass, `construct_mapping` raising on a repeated key at the same node), script `rv03_060.py`, output `rv03_060.out`:

```
bytes: 24278
top-level keys: 38
AC ids (8): ['AC1','AC2','AC3','AC4','AC5','AC6','AC7','AC8']
withdrawn ids (1): ['AC1-ORIGINAL']
finding ids (8): ['F1'..'F8']
overlap: []
```

No duplicate key, no id in both lists. Matches the file size on disk (24278).

### 2. Is edit (a) true? — YES, it is now correct

`acceptance_criteria[AC5]` (manifest.yaml:114-115), verbatim:

> "A non-empty baseline with status 1 and a parsed set equal to the baseline exits 0 and prints PASS. This is the live caller: gates.yml:161-164 wraps scripts/check_bilingual_docs_full.py, which exits 1 with 77 violations as its normal result. A rule reading 'any non-zero status fails' turns the required check Bilingual docs coverage (ratchet) permanently red, so this criterion exists to make that outcome a test failure rather than a CI discovery."

`acceptance_criteria[AC1]` (manifest.yaml:106-107), verbatim:

> "A command exit status outside {0, 1} fails the ratchet, whatever the parsed set and whatever the baseline contains: non-zero exit, no PASS, and the observed status named in the message. Tested with both an empty and a non-empty baseline. Measured at b80e5a40: empty baseline plus a command exiting 9 gives regressions=0 fixed=0 PASS exit 0, so this criterion fails today."

From the text: AC1 carries the non-empty-baseline case ("Tested with both an empty and a non-empty baseline") and pins **status outside {0,1} → fail** (the status-9 shape). AC5 carries the non-empty baseline and pins **status 1 → PASS**. `findings[F7].resolution` (manifest.yaml:216) now reads "Pinned by AC1's non-empty-baseline case, which requires a status of 9 with a full baseline to fail; AC5 pins the opposite direction (status 1 must pass)." That matches the two criteria. The round-2 misattribution (status-9 pin assigned to AC5) is gone. Verified against the code: `gate_ratchet.py:117` rejects status outside {0,1}; the live caller at `gates.yml:165-168` exits 1 and the ratchet passes (measured below).

Minor, non-blocking: the citation `gates.yml:161-164` (AC5:115, also findings[F5]:203) points at the job's name/shell lines; the actual `gate_ratchet.py` invocation is `gates.yml:165-168`. The construct exists, four lines off.

### 4. Is the premise true? — NO. BLOCKING.

`grep -n "returncode\|check_returncode\|subprocess" scripts/ci/gate_ratchet.py` at `767f2eaa`:

```
31:import subprocess
95:    proc = subprocess.run(
117:    if proc.returncode not in (0, 1):
118:        print(f"ratchet: FAIL - the wrapped command exited {proc.returncode}; "
122:    if proc.returncode != 0 and not current:
123:        print(f"ratchet: FAIL - the wrapped command exited {proc.returncode} "
```

Four lines read the exit status, and two of them are guards that return 1. The premise is false at the reviewed commit.

Provenance of the change: `c6602739` "fix(governance): remove two unreachable duplicate guards and close gate_ratchet's empty-baseline fail-open (#799) (#1031)", 2026-11-25 10:33:09 +0800, is an ancestor of `767f2eaa` (14:35:20 +0800) — `git merge-base --is-ancestor c6602739 HEAD` → YES. Its diff adds exactly the two guards:

```
+    if proc.returncode not in (0, 1):
+        print(f"ratchet: FAIL - the wrapped command exited {proc.returncode}; "
+              "only 0 (clean) and 1 (red) carry a comparable failure set.")
+        return 1
+
+    if proc.returncode != 0 and not current:
+        print(f"ratchet: FAIL - the wrapped command exited {proc.returncode} "
+              "without printing any item; a crash is not a clean run.")
+        return 1
```

The premise WAS true at `b80e5a40` (the manifest's own `base_commit_sha`, manifest.yaml:67): `git show b80e5a40:scripts/ci/gate_ratchet.py | grep -n returncode` returns nothing, and line 105 there is `current = normalize(proc.stdout.splitlines(), args.format)`, exactly as findings[F1]:178 says. So the `measured_at: b80e5a40` fields are honest; what is false is their use in the present tense.

Live measurements at `767f2eaa` (HEAD):

- `py scripts/check_bilingual_docs_full.py` → exit 1, parsed set 77.
- `py scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/bilingual-docs.txt --format paths --command "py scripts/check_bilingual_docs_full.py"` → exit 0, `baseline=77 current=77 regressions=0 fixed=0`, `PASS`. AC5 holds.
- Empty baseline + command printing one item and exiting 9 → exit 1, `FAIL - the wrapped command exited 9; only 0 (clean) and 1 (red) carry a comparable failure set.` AC1 holds at HEAD.
- Empty baseline + exit 9 with no output → exit 1, `FAIL ... without printing any item; a crash is not a clean run.` AC2 holds at HEAD.

False sentences:

- manifest.yaml:178 (findings[F1].statement): "proc.returncode is never read, in any format: the only reference to the completed process is current = normalize(proc.stdout.splitlines(), args.format) at line 105." Contradicted by the grep above and by `sed -n '105p'` at HEAD, which is a comment line.
- manifest.yaml:107 (AC1): "...so this criterion fails today." It passes at HEAD (third measurement above).
- manifest.yaml:99 (deliverables[1]): describes as future work what `gate_ratchet.py:117-124` already does.

Also stale: `scripts/ci/test_gate_ratchet.py` — named in AC6:117 and in `scope.files_to_create` — already exists at `767f2eaa` with `test_exit_status_outside_zero_one_is_not_comparable`, `test_empty_baseline_with_nonzero_exit_and_no_output_fails`, `test_exact_match_with_nonzero_exit_still_passes`. AC6 and findings[F8]:223 are written as if the file were absent.

The manifest nowhere records #1031 / c6602739 / #799-as-landed; `grep -n "1031\|c6602739\|already landed"` hits only manifest.yaml:190, an unrelated note about AID-2026-059's id colliding with #799.

Consequence, not style: a work item in status DISPATCHED (manifest.yaml:59) whose acceptance criteria all pass before implementation will be "satisfied" by doing nothing, which is the same fail-open shape findings[F1] exists to name. Either the work item is now a regression guard (and must say so, with the commit that closed the hole cited and the criteria re-based on `767f2eaa`), or it is done and should be closed. The file as written claims the former while asserting the latter's premise.

