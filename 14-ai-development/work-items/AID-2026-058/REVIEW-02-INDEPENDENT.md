---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
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
      last_verification_note: "Describes the state examined at origin/main 2fc4a2ff, before the follow-up fixes in section 5. The INDEX grep discrepancy (023 counted twice because 026's title cites it) and the empty-baseline vacuity were both reproduced by command, not inferred."
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

# AID-2026-058 — Second independent review (OD-26)

**Status:** `COMPLETED` / `REQUEST-CHANGES` / `STATE EXAMINED: origin/main @ 2fc4a2ff`
**Independence basis:** `PR-GOVERNANCE-001` §5 as amended by `2eb4e352` (#935).
**Reviewing session:** newly opened; did not author, did not perform the first review, did not perform the rework.
**Disclosure:** same GitHub identity as the author; session-level independence only. Disclosed, not waived.

---

## 1. Verdict

**`REQUEST-CHANGES`.** Two blocking items stayed open, and one of them is the exact item the first review named and the rework claimed to have fixed.

## 2. Confirmed closed

| Finding | Evidence |
|---|---|
| B3 (evidence attributed to the wrong commit) | F3 marked RETRACTED; independently verified: at `1259f1af` the script prints `ERROR required registry unavailable` + `FAIL TRACEABILITY: 0 requirements / 0 work items / 1 errors / 0 warnings`, exit **1**; at `a23e6cc0` it prints `INCOMPLETE … 0 errors … 1 warnings`, exit **2**. The retraction is correct. |
| B4 (AC5 said "unmodified") | AC5 now names the one assertion that must change and requires it updated rather than deleted. The assertion still exists at line 513. |
| M4 (inputs still untracked) | confirmed: `git cat-file -e origin/main:` returns 128 for both paths |
| M2 (CRLF baseline) | resolved as a side effect of AC4 emptying the file, though not stated as such |

## 3. Blocking findings still open

### B2 — the authorisation field was not changed, only the prose was

AC4 states:

> `baseline_content_change` moves from `NOT_GRANTED` to `GRANTED-FOR-SHRINK-ONLY`

`authorization.baseline_content_change` still read:

```yaml
baseline_content_change: "NOT_GRANTED - AC4 asserts the baseline is byte-unchanged"
```

A machine-readable field saying one thing and an acceptance criterion saying the opposite. **This is the same defect the first review raised, at the same line.** `git log -p -1 da8e429b -- ...058/manifest.yaml | grep baseline_content_change` matches only the AC prose, confirming the field was never touched.

### B1 — AC1's own verification command cannot pass

AC1 required `grep -c 'AID-2026-02[3456]' INDEX.md` to return 1 for each of the four. Measured:

```
AID-2026-023 -> 2
AID-2026-024 -> 1
AID-2026-025 -> 1
AID-2026-026 -> 1
```

The second match is inside AID-2026-026's **title**, which cites AID-2026-023. Satisfying the count would mean deleting a cross-reference from another work item's title — the same class of damage B1 was originally about, one level down. Anchoring to the table's first column (`^\| \[AID-2026-02[3456]\]`) returns exactly 4.

## 4. Material findings

### M1 — emptying the baseline makes AC3 vacuously true

AC4 empties the baseline. AC3 asserted `regressions=0`. With an empty baseline, `regressions=0` holds for a correct checker, a broken checker, and a checker that was never built — measured: empty baseline plus a command exiting 9 gives `regressions=0 fixed=0 PASS`. **AC4 creates exactly the condition that AC7 of the sibling work item documents as a hazard.** AC3 needed a deliberate injection, not a count.

### M1′ — AC2's forbidden pattern missed two shapes

The anchored form `^(PASS|FAIL|INCOMPLETE) TRACEABILITY:` did not match `TRACEABILITY: cannot read registry`, and did not match a verdict line with leading whitespace. Enumerating the three word forms is weaker than forbidding the token.

### M3 — base staleness unrecorded

`base_commit_sha` is 70 commits behind. The sibling work item carries a finding for this; this one carried none, so a reader could conclude its base was current. Two of the intervening commits (`35f2b078`, `f640ba50`) are precisely the ones that falsified the original criteria.

### M4′ — AC5's line numbers were wrong

Named 507-515; the test is defined at 499 and its assertion is at 513.

## 5. Follow-up fixes applied after this review

Not covered by the verdict above; a third pass would be required to confirm them.

| Item | Fix |
|---|---|
| B2 | `authorization.baseline_content_change` changed to `GRANTED-FOR-SHRINK-ONLY` with additions still forbidden and the reason stated |
| B1 | AC1 anchored to the table's first column, with the 023/026 collision explained in the criterion |
| M1 | AC3 now requires an injected failure: one path temporarily removed from INDEX.md must produce `regressions=1` and a non-zero exit |
| M1′ | AC2 forbids the token `TRACEABILITY:` outright, anywhere in a line |
| M3 | finding F5 added recording the 70-commit staleness and the two commits that matter |
| M4′ | AC5 line numbers corrected |

`review.status` stays `CHANGES_APPLIED_AWAITING_RE_REVIEW`.
