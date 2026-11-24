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
      last_verification_note: "This record describes the state the second review actually examined, which is the state on origin/main at 2fc4a2ff, not the state after the follow-up fixes. Those fixes came later and are listed separately in section 5 with their own verification. Keeping the two apart matters: a review verdict belongs to the artifact it read."
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

# AID-2026-056 — Second independent review (OD-26)

**Status:** `COMPLETED` / `REQUEST-CHANGES` / `STATE EXAMINED: origin/main @ 2fc4a2ff`
**Independence basis:** `PR-GOVERNANCE-001` §5 as amended by `2eb4e352` (#935).
**Reviewing session:** newly opened, did not participate in authoring, the first review, or the rework.
**Disclosure:** same GitHub identity as the author (`collaborators = 1`); independence is session-level only, weaker than human review and weaker than a cross-model-family review. Disclosed, not waived.

---

## 1. Verdict

**`REQUEST-CHANGES`.** `review.status` may not move to `APPROVED`.

The numeric rework held up — AC1's 11, AC2's 66, AC5's four assertions and AC8's module path were each confirmed by re-measurement. What failed was a different layer: **the machine-readable fields still contradicted the prose.**

## 2. What the review confirmed closed

| Finding | Evidence |
|---|---|
| B2 (AC1 said 9, AC2's 72 did not add up) | re-measured independently: 77 violations = 66 embedded + 11 real; the 11 match the erratum's list exactly; baseline set difference both ways empty |
| B3 (AC5 had one side) | four assertions present, two per side, including `cjk=100/latin=1000` must resolve |
| B4 (AC8 named a module that does not exist) | `python3 -m unittest tests.test_check_bilingual_docs_full` → `Ran 7 tests ... OK` |
| M4 (empty-baseline pass) | reproduced independently: empty baseline + command exiting 9 → `regressions=0 fixed=0 PASS exit 0`; recorded in AC7 as a floor |

## 3. What the review found still open

### B5 — no machine-readable authorisation

`authorization:` and `scope:` blocks were absent. The write boundary existed only as prose inside `security_scope`, which describes attack surface. Finding F5's own resolution text referred to "this work item's file scope" — a field that did not exist.

### B1 (second half) — the prompt still commands the withdrawn criterion

`prompt-v1.md:127` still reads:

> **AC6** — `NORMATIVE_ROOTS` is byte-identical to its pre-change value, verified by `git diff` on that hunk, and the seven non-existent roots are still listed.

The manifest had withdrawn AC6, and AID-2026-058 declares that its manifest governs over its prompt. **AID-2026-056 declared nothing.** A frozen prompt is the instruction set an implementer actually reads. Withdrawing a criterion in one file while another file still commands it is not a withdrawal — it is a choice the implementer has to make, without being told the rule.

### M2 — the erratum claimed more than it delivered

`errata[0].status` said all six items (A)–(F) were "now reflected … in risk_rationale and owner_decisions[OD-18]". Both were still unconverted:

- `risk_rationale` said "from 81 to 9" and "The predicted 9".
- `OD-18.constraints[3]` said "The remaining 9 are the real backlog".

An implementer following OD-18 would under-report two real debts, in a block the manifest itself describes as "not options for the implementer to re-litigate".

### M1 — a byte count that is not reproducible

AC4 named 50488 bytes. Measured: the git blob at `8e489ec1` is **49758** bytes. 50488 is that blob checked out with CRLF — 49758 + 730 line terminators. The first review substituted 50488 for the prompt's 49666 and the number was adopted without re-measuring. A count that changes with a checkout setting is not an anchor.

### M3 — `security_scope` answering a question it was not asked

`security_scope: None` is correct (no attack surface) and irrelevant to whether review is needed. The risk here is check silence, which the manifest's own `risk_rationale` states. The two axes were being read as one.

## 4. What this review did not do

- It did not modify any file.
- It did not accept CI green as review evidence. Every negative conclusion came from a command it ran itself.
- It noted, correctly, that the state described in its own commission (`DISPATCHED`, `CHANGES_APPLIED_AWAITING_RE_REVIEW`) did not exist on `origin/main` at the time — that state lived on an unmerged branch. A review verdict belongs to the artifact it read; this one is therefore attached to `2fc4a2ff`, where the file still read `BLOCKED` / `CHANGES_REQUESTED`.

## 5. Follow-up fixes applied after this review

Listed separately because they are **not** covered by the verdict above. A third pass would be required to confirm them.

| Item | Fix |
|---|---|
| B5 | `authorization:` and `scope:` blocks added, with `root_membership_change: NOT_GRANTED`, `baseline_content_change: GRANTED-FOR-SHRINK-ONLY`, and an explicit `files_not_to_touch` list |
| B1 (prompt half) | `prompt_supersession:` block added naming the five superseded prompt criteria, the reason (prompt is FROZEN), and the block that governs |
| M2 | `risk_rationale` corrected to 77→11; `OD-18.constraints[3]` annotated with the re-measured count; erratum status narrowed to the items actually converted; item (D) recorded as F8 |
| M1 | AC4 restated on the blob size (49758, LF) with the CRLF discrepancy explained |
| M3 | a comment separating `security_scope` from the review axis |

`review.status` stays `CHANGES_APPLIED_AWAITING_RE_REVIEW`. It does not become `APPROVED` on the strength of a list of edits — that is exactly what this review rejected.
