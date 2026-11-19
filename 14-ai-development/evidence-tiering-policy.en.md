# Evidence Chain Tiering Policy

- **Document ID:** AI-DOC-EVIDENCE-TIERING
- **Version:** 1.0
- **Status:** PROPOSED (pending formal adoption by the project governance authority)
- **Owner:** G (process architecture)
- **Chinese counterpart:** [evidence-tiering-policy.md](evidence-tiering-policy.md)
- **Governing references:** AI-STD-001 §4.2 (independent gate evidence), AI-EXEC-001 v1.1 (ADOPTED), GOV-DOC-001
- **Authorization basis:** DEC-FIX-2026-P1-T4-GO-001
- **Explicitly not a basis:** AI-EXEC-002 v1.2 (its status field remains PENDING ADOPTION; this policy does not rely on it)

## 1. Purpose and Position

This policy sets evidence-chain depth by change risk so that low-risk changes stop paying full evidence cost, without relaxing any gate. An evidence level is an **evidence depth selector**, not a status axis, review level, or lifecycle phase.

Three dimensions MUST remain independent:

| Dimension | Values | Determines | Must not be substituted |
|---|---|---|---|
| Change risk | Level 1 / 2 / 3 | Evidence depth (required field set) | MUST NOT be inferred from review level or change size |
| Review level | R0 / R1 / R2 / R3 | Independent and specialist review requirements | MUST NOT be lowered or replaced by a Level |
| Lifecycle | 12 states / 6 phases | Gate milestones and phase grouping | Unaffected by any Level |

No Level may change the independent gate meaning of VERIFIED, REVIEWED or INTEGRATION_READY. Missing evidence remains fail-closed.

## 2. Three Levels

| Level | Applies to | Required evidence |
|---|---|---|
| **Level 1 (strict)** | ARCHITECTURE, SECURITY, PERFORMANCE_CRITICAL, PUBLIC_API, DATA_MIGRATION, DOC_NORMATIVE; and every R3 change | subject_head (40-hex commit SHA), change_summary, design_doc, impact_analysis, test_log, review_record, rollback_plan, binding.protocol=v3, binding.subject_tree_contains_evidence, binding.sidecar_anchor, source_authenticity (when NOT_VERIFIED, authenticity.acknowledged=true is required) |
| **Level 2 (standard)** | FEATURE, BUGFIX (bounded, no contract change) | subject_head, change_summary, test_log, review_record, binding.protocol=v3, binding.subject_tree_contains_evidence, source_authenticity |
| **Level 3 (lightweight)** | DOC_EDITORIAL (editorial documentation with no normative change), OPS (non-release-critical) | subject_head, change_summary, evidence.review_note |

Every level MUST retain a full 40-hex subject_head and a change summary, without exception.

## 3. Non-Downgrade Rules

1. **Level 1 floor:** anything involving R3, security boundaries, authorization, data integrity, deletion/Forget, migration, public API, architecture semantics or normative-document semantics MUST be Level 1. Any assessment downgrading it to Level 2/3 is invalid.
2. **R2 MUST NOT be auto-downgraded:** an R2 change MUST NOT drop to Level 3 merely because it touches few files, looks small, or "reads like wording". Where genuinely warranted, `downgrade_justification` MUST be supplied and confirmed by the reviewer; without that field the result is BLOCKED.
3. **Documentation is not automatically low risk:** a documentation change that alters normative meaning, obligation strength, interfaces/protocols, data models, state machines or security boundaries MUST be escalated to DOC_NORMATIVE → Level 1.
4. **UNKNOWN is always BLOCKED:** if the class cannot be determined, no Level may be assigned; the result is BLOCKED / NEEDS_CLASSIFICATION until an authorized Owner or governance authority confirms the class and the declaration is re-assessed.
5. **No automatic pass:** a Level only sets evidence depth and is never evidence that any gate passed.

## 4. Assessment and Audit Trail

Every evidence declaration MUST record the following audit fields for independent review:

| Field | Meaning |
|---|---|
| `change_class` | Risk class (enumeration per §2) |
| `review_level` | Review level R0–R3 |
| `evidence_level` | 1/2/3 |
| `assessed_by` | Who assessed (Owner/session identifier) |
| `assessed_at` | Assessment timestamp (with timezone) |
| `rationale` | Why this Level is sufficient |
| `base_head` | Baseline commit the assessment relies on |
| `downgrade_justification` | Required only for R2 → Level 3 |
| `escalation_target` | Escalation target when classification is uncertain or needs an Owner decision |

An assessment missing `assessed_by`, `assessed_at` or `rationale` MUST NOT be used as a Level basis.

## 5. Relationship to Existing Evidence Infrastructure

1. The existing applied-delivery-evidence validator and its CI workflow are **neither replaced nor weakened** (this policy does not modify `.github/workflows`).
2. **Evidence binding protocol v3 is preserved:** subject_head must be a commit object, evidence files must be inside the subject tree, working-tree bytes must match the subject blob, and sidecar SHA anchoring remains in force.
3. **The source_authenticity boundary is unchanged:** content integrity is not source authenticity. A VERIFIED claim requires `authenticity.verification_record`; otherwise BLOCKED.
4. Level 1's `sidecar_anchor` follows the v3 anchoring protocol (the commit message of the commit that most recently touched the sidecar carries the SHA-256 of the sidecar bytes).

## 6. Checker

Checker: `scripts/governance/evidence/check-evidence-tiering.py` (stdlib only, no third-party dependencies).

BLOCKED scenarios that MUST each be judged individually:

| # | Scenario | Reason code |
|---|---|---|
| 1 | Missing evidence level declaration | `CE_NO_LEVEL` |
| 2 | Level conflicts with risk class | `CE_LEVEL_CLASS_CONFLICT` / `CE_R3_DOWNGRADE` |
| 3 | Any Level 1 required field missing | `CE_L1_MISSING_FIELD` |
| 4 | UNKNOWN assigned a level | `CE_UNKNOWN_CLASS` |
| 5 | v3 binding fields missing | `CE_NO_BINDING_PROTOCOL` / `CE_NO_BINDING_TREE` / `CE_NO_SIDECAR_ANCHOR` |
| 6 | SHA format or length invalid | `CE_BAD_SHA` / `CE_BAD_SUBJECT` |
| 7 | NOT_VERIFIED passed silently / VERIFIED unsupported | `CE_AUTH_NOT_ACK` / `CE_UNFOUNDED_VERIFIED` |
| 8 | Unparseable input or internal error | `CE_UNPARSABLE` / `CE_INTERNAL_ERROR` |

The checker emits `VERDICT`, `LEVEL`, `REASON` and `SUMMARY` records. **An exit code alone is not acceptance evidence:** the acceptor MUST verify the actual per-scenario records above.

Exit codes: 0 = PASS; 1 = BLOCKED (declaration defect); 2 = BLOCKED (input/usage error, still fail-closed).

## 7. Bilingual Obligation

This policy is a Tier 1 document (architecture/governance policy). Chinese and English must be updated in the same change set with equivalent meaning, equivalent obligation strength and reciprocal links. A missing counterpart means NOT DONE.

## 8. Change and Effectiveness

1. Any change to Level definitions, required field sets or non-downgrade rules requires a formal change record (rationale, affected files, proposer, approver, effective version).
2. This policy is PROPOSED until formally adopted by the governance authority; passing independent review and merging an implementation does not constitute adoption.
3. The adoption record MUST state the approver, effective date, and the checker version and commit SHA in force.
