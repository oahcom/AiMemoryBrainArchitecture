---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Under-Review
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-284/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Delegated proxy scope statement awaiting Owner confirmation. Offline-recomputable: AID-2026-260 blob e6425787, AID-2026-280 blob 3cde57f7, ADR metadata enums. Not offline-recomputable: Issue #265 body text, Issue #305 comment 7042461592. Not a natural-person Owner signature."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes:
        - "14-ai-development/work-items/AID-2026-260/scope-confirmation.md"
      supersession_reason: "AC8 exclusion in AID-2026-260:69 ruled ineffective by AID-2026-280:75; AC8 restated as in-scope and ABSENT"
      effective_date: "2026-11-27"
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  steward: "user-authorized operator (delegated by account owner)"
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Proxy scope determination for REQ-04 Issue #265"
    canonical_scope_id: "ai-development/req-04-scope-confirmation"
    canonical_scope_keywords:
      - "req-04"
      - "scope-confirmation"
      - "ac8-absent"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# REQ-04 Scope Confirmation — AID-2026-284

- Issue: [#265 — REQ-04](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/265)
- Attribution: user-authorized operator (delegated by account owner)
- Decision date: 2026-11-27
- Decision character: **代理裁决，非自然人 Owner 签署**
- Supersedes: 14-ai-development/work-items/AID-2026-260/scope-confirmation.md
- Base observed: cbdaf78313404fc24a6c250dc06faa72d4d0b97c

## Confirmed domains

1. **Architecture deadlock capture and review — AC2.** In scope. Acceptance means material architecture conflicts can be recorded with evidence, impact, accountable owner(s), and explicit closure conditions, and can be reviewed. Existing carrier: `docs/architecture-convergence/ARCH-CONVERGENCE-001-CONFLICT-REGISTER.md`, CF-001 through CF-016. Existing SATISFIED status is preserved.
2. **Evidence-based alternative evaluation and convergence — AC3.** In scope. Acceptance requires alternatives to be compared against explicit evidence and a recorded disposition; a candidate or open-register entry alone is not closure. Current PARTIAL status remains. Follow-up disposition: supplement evidence and reconcile the open alternatives; if an alternative cannot be resolved within REQ-04, retain it as an explicitly identified residual/record-only gap for later Owner review. Do not check AC3.
3. **Mature implementation leverage — AC4.** In scope. Acceptance means mature implementations relevant to the architecture are identified, their fit and trade-offs are evidenced, and their adoption/defer/reject status is explicit. Existing SQLite/PostgreSQL, Cedar and Tantivy records remain in scope. Current PARTIAL status remains. Follow-up disposition: complete comparative evidence where required; otherwise preserve a clearly labelled record-only gap for explicit Owner review. This scope confirmation does not select or freeze a technology. Do not check AC4.
4. **Minimal runnable architecture closure — AC5.** In scope. Acceptance means a reproducible end-to-end minimal path is runnable and demonstrates the required process and persisted/read-back result. Existing `crates/brain-cli/tests/e2e_full_chain.rs` carrier is retained. Existing SATISFIED status is preserved.
5. **Prompt-to-commit traceability — AC6.** In scope. Acceptance means an implementation can be traced through its actual prompt/session evidence, work item, branch/commit and changed artifacts, with missing pins visible rather than inferred. Current PARTIAL coverage remains. Follow-up disposition: improve coverage for implemented work or explicitly retain uncovered historical/pending items as record-only gaps; do not infer universal coverage from the 11/12 implemented subset. Do not check AC6.
6. **Small-defect capture and follow-up — AC7.** In scope. Acceptance means defects have stable capture records and an identifiable follow-up route/status; filenames alone are not treated as proof of completed follow-up. Existing 48 GAP records remain in scope. Existing SATISFIED status is preserved only at the stated capture/path level, not expanded into a claim that every GAP has closed.

## AC8 — in scope, ABSENT, gap named

AC8 (human engineering attention cost and context-switching cost) is **in REQ-04's scope**. It is **not excluded**, and it is **not satisfied**.

The "EXCLUDED" determination recorded at `AID-2026-260/scope-confirmation.md:69` is **withdrawn and ineffective**. `AID-2026-280/decision.md:75` rules it so: "F3 satisfies condition 1. In this case conditions 2 and 3 are not satisfied: AID-260 is only an unverified proxy record and the Issue body was not changed. Therefore EXIT-2 is not an effective exclusion." A superseded carrier cannot be the basis for deleting an acceptance criterion.

`AID-2026-254` is retained as an **optional, out-of-scope proxy observation**, not as an AC8 acceptance carrier. Its declared root/domain fan-out measures manifest path dispersion; it does not measure elapsed attention time, human context transitions, reorientation cost, cognitive load, or Agent context-window/token cost (`AID-2026-254/evidence.md:98`, `:107`; `scripts/measure_attention_context_cost.py:1-6`).

**Status: ABSENT. Direct-measurement carrier: NO_CARRIER_FOUND.**

Closure requires the units named in `AID-2026-280/decision.md:105-112`: (1) a declared measurement population and unit; (2) recorded human transition events with pseudonymous role/session identifiers, ordered timestamps and reorientation duration; (3) recorded review burden (distinct PRs, version families, review rounds, active minutes); (4) Agent context-window/token cost recorded separately, or NOT_MEASURED; (5) a reproducible read-only command publishing cohort definition and missing-data counts; (6) thresholds derived from a declared baseline with sample size and limitations; (7) at least one reproducible cohort independently recomputed, plus the authority required to accept AC8.

No exclusion is claimed here, and this record does not mark AC8 as passed.

## AC9 sequencing and decision boundary

AC9 remains **NOT YET JUDGEABLE**. The required order is: **first merge this carrier → then disposition the AC3/AC4/AC6 residuals → finally the Owner records AC9**. This record does not claim PASS.
