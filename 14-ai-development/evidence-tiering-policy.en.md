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

The **Level 1/2/3** scale here is evidence depth. It is a different scale from **Tier 1/2/3** in the neighbouring policy `AI-DOC-BILINGUAL-TIERING`, which governs whether a document needs a Chinese/English counterpart (section 7 relies on it). The two axes are independent: a decision on one MUST NOT be read as a decision on the other.

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
| **Level 1 (strict)** | ARCHITECTURE, SECURITY, PERFORMANCE_CRITICAL, PUBLIC_API, DATA_MIGRATION, DOC_NORMATIVE; and every R3 change | subject_head (40-hex commit SHA), change_summary, design_doc, impact_analysis, test_log, review_record, rollback_plan, the full v3 binding (protocol + subject-tree containment + blob equality + **sidecar_path and sidecar_anchor**), source_authenticity (when NOT_VERIFIED, authenticity.acknowledged=true is required) |
| **Level 2 (standard)** | FEATURE, BUGFIX (bounded, no contract change) | subject_head, change_summary, test_log, review_record, v3 binding (protocol + subject-tree containment + blob equality), source_authenticity |
| **Level 3 (lightweight)** | DOC_EDITORIAL (editorial documentation with no normative change), OPS (non-release-critical) | subject_head, change_summary, evidence.review_note, v3 binding (protocol + subject-tree containment + blob equality) |

Every level MUST retain a full 40-hex subject_head and a change summary, without exception. The exact v3 scope is defined in §5: protocol, subject-tree containment and blob equality apply to every level; the sidecar anchor is mandatory only for Level 1. `evidence.review_note` is a **path to an acknowledgement record**, not free text — free text cannot be Git-bound.

## 3. Non-Downgrade Rules

1. **Level 1 floor:** anything involving R3, security boundaries, authorization, data integrity, deletion/Forget, migration, public API, architecture semantics or normative-document semantics MUST be Level 1. Any assessment downgrading it to Level 2/3 is invalid.
2. **R2 MUST NOT be auto-downgraded:** an R2 change MUST NOT drop to Level 3 merely because it touches few files, looks small, or "reads like wording". Where genuinely warranted, all three of the following MUST be supplied: `downgrade_justification`, `downgrade_confirmed_by` (which MUST differ from `assessed_by`) and `downgrade_confirmation_record` (verified in the subject tree, the working tree and the subject blob per §5 item 6). Any missing item, or self-confirmation, is BLOCKED.
3. **Documentation is not automatically low risk:** a documentation change that alters normative meaning, obligation strength, interfaces/protocols, data models, state machines or security boundaries MUST be escalated to DOC_NORMATIVE → Level 1.
4. **UNKNOWN is always BLOCKED:** if the class cannot be determined, no Level may be assigned; the result is BLOCKED / NEEDS_CLASSIFICATION until an authorized Owner or governance authority confirms the class and the declaration is re-assessed.
5. **Classification trust boundary:** forced Level 1 classes (ARCHITECTURE, SECURITY, PERFORMANCE_CRITICAL, PUBLIC_API, DATA_MIGRATION, DOC_NORMATIVE) MUST NOT be lowered by relabelling them as FEATURE/BUGFIX/DOC_EDITORIAL/OPS. Any declaration using a downgrade-capable class (FEATURE, BUGFIX, DOC_EDITORIAL, OPS) MUST supply `classification_basis`, `classification_confirmed_by` (an independent confirmer, not `assessed_by`) and `classification_record` (verified in the subject tree, the working tree and the subject blob per §5 item 6). Missing or unverifiable classification is BLOCKED; the declarant is never trusted by default. `classification_basis` MUST correspond to the actual change impact (the files, interfaces, boundaries or data models this change touches), and the confirmer MUST record in `classification_record` what was actually examined and what was concluded; an attestation that only restates the declared label is not independent confirmation and is BLOCKED. The record MUST cover three parts: **what was examined** (the files, interfaces, boundaries or data models), **the conclusion**, and **who confirmed**; a record missing any part, or saying only "confirmed", is BLOCKED. The reviewer MUST record the result of each of the three parts in its review record (for Level 3, in the acknowledgement record that `evidence.review_note` points at); a missing part is BLOCKED, and "reviewed" alone is not a record.
6. **No automatic pass:** a Level only sets evidence depth and is never evidence that any gate passed.

## 4. Assessment and Audit Trail

Every evidence declaration MUST record the following audit fields for independent review:

| Field | Meaning | Machine-enforced |
|---|---|---|
| `change_class` | Risk class (enumeration per §2) | Yes |
| `repository` | Repository the declaration belongs to (owner/name); MUST match the clone's origin remote | Yes (mismatch/unverifiable → BLOCKED) |
| `review_level` | Review level R0–R3 | Yes |
| `evidence_level` | 1/2/3 | Yes |
| `assessed_by` | Who assessed (Owner/session identifier) | Yes (missing → BLOCKED) |
| `assessed_at` | Assessment timestamp (with timezone) | Yes (missing → BLOCKED) |
| `rationale` | Why this Level is sufficient | Yes (missing → BLOCKED) |
| `base_head` | Baseline commit the assessment relies on (must be an ancestor of subject_head) | Yes (format and ancestry both checked) |
| `classification_basis` | Why this change_class applies | Yes (missing → BLOCKED) |
| `classification_confirmed_by` | Independent confirmer for downgrade-capable classes (≠ assessed_by) | Mandatory for downgrade-capable classes |
| `classification_record` | Classification confirmation record (must exist in the subject tree, with worktree/blob equality verified) | Mandatory for downgrade-capable classes |
| `downgrade_justification` | Required only for R2 → Level 3 | Mandatory in that case |
| `downgrade_confirmed_by` | Downgrade confirmer (≠ assessed_by) | Mandatory in that case |
| `downgrade_confirmation_record` | Downgrade confirmation record (must exist in the subject tree, with worktree/blob equality verified) | Mandatory in that case |
| `escalation_target` | Escalation target when classification is uncertain or needs an Owner decision | No (record only) |

An assessment missing any of `assessed_by`, `assessed_at`, `rationale`, `base_head` or `classification_basis` MUST NOT be used as a Level basis; the checker returns BLOCKED.

## 5. Relationship to Existing Evidence Infrastructure

1. The existing applied-delivery-evidence validator and its CI workflow are **neither replaced nor weakened** (this policy does not modify `.github/workflows`).
2. **Evidence binding protocol v3 is preserved:** subject_head must be a commit object; evidence files must be inside the subject tree; working-tree bytes must equal the subject blob.
3. **The v3 verification scope is stated per level** (removing ambiguity). This table tunes evidence depth only and **does not change binding integrity**: the first three rows are mandatory at every level, the sidecar row is a Level 1 depth requirement, and its absence MUST NOT be read as allowing evidence to detach from the reviewed object:

| v3 check | Scope | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| `subject_head` is a commit object | ALL LEVELS | Mandatory | Mandatory | Mandatory |
| Evidence path exists in the subject tree | ALL LEVELS | Mandatory | Mandatory | Mandatory |
| Working-tree bytes == subject blob | ALL LEVELS | Mandatory | Mandatory | Mandatory |
| `sidecar_path` + `sidecar_anchor` (sha256 plus commit-message anchoring) | LEVEL 1 ONLY | Mandatory | Not applicable | Not applicable |

The **Scope** column is the single normative source for scope; the three level cells express only what each level requires, and MUST NOT be used on their own to infer scope. The two MUST NOT evolve independently.

4. **The source_authenticity boundary is unchanged:** content integrity is not source authenticity. A VERIFIED claim requires `authenticity.verification_record`; otherwise BLOCKED.
5. Level 1's `sidecar_anchor` follows the v3 anchoring protocol: the anchor is `sha256:<64 hex>`, equal to the SHA-256 of the sidecar bytes in the subject tree, and the commit message of the commit that most recently touched that sidecar MUST carry that digest.
6. **Governance confirmation records are verified the same way:** `classification_record` and `downgrade_confirmation_record` MUST exist in the subject tree with working-tree bytes equal to the subject blob. A non-existent path is BLOCKED (`CE_CLASS_RECORD_NOT_IN_SUBJECT` / `CE_DOWNGRADE_RECORD_NOT_IN_SUBJECT`); a record is never an arbitrary string.
7. **Repository identity:** the declaration MUST carry `repository` (owner/name) matching the clone's `origin` remote. A missing remote, or one outside the allowlisted forms (`CE_REPO_IDENTITY_UNVERIFIED`), or a declaration that disagrees with the remote (`CE_REPO_IDENTITY_MISMATCH`) is BLOCKED. Only three origin forms are accepted (username must be `git`, host exactly `github.com`, path exactly `owner/repo` with an optional `.git` suffix; no port, query or fragment):

   | Form | Example |
   |---|---|
   | HTTPS | `https://github.com/owner/repo[.git]` |
   | SSH URL | `ssh://git@github.com/owner/repo[.git]` |
   | SCP | `git@github.com:owner/repo[.git]` |

   `http://`, `git://`, non-`git` usernames and URLs carrying a port are rejected. This defines the trust boundary for *where* evidence is verified; it does not establish source authenticity.

8. **Path resolution base:** every evidence path (including `evidence.review_note` and `declaration_path`) is resolved against the **repository root** of the subject commit, **not** against the directory holding the declaration. `evidence.review_note` MUST point at an acknowledgement record that really exists in the subject tree; free text or a bundle-relative name yields `CE_EVIDENCE_NOT_IN_SUBJECT`. This item **adds no new verification layer**; it only fixes the path resolution semantics shared by items 3 and 6, which keep defining scope and applicability.

## 6. Checker

Checker: `scripts/governance/evidence/check-evidence-tiering.py` (stdlib only, no third-party dependencies).

BLOCKED scenarios that MUST each be judged individually:

| # | Scenario | Reason code |
|---|---|---|
| 1 | Missing evidence level declaration | `CE_NO_LEVEL` / `CE_BAD_LEVEL` |
| 2 | Level conflicts with risk class | `CE_LEVEL_CLASS_CONFLICT` / `CE_R3_DOWNGRADE` / `CE_R2_AUTO_DOWNGRADE` |
| 3 | Any Level 1 required field missing | `CE_L1_MISSING_FIELD` (Level 2/3 map to `CE_L2_MISSING_FIELD` / `CE_L3_MISSING_FIELD`) |
| 4 | UNKNOWN assigned a level | `CE_UNKNOWN_CLASS` |
| 5 | v3 binding verification failure | `CE_NO_BINDING_PROTOCOL` / `CE_BAD_BINDING_PROTOCOL` / `CE_EVIDENCE_NOT_IN_SUBJECT` / `CE_EVIDENCE_MISSING_WORKTREE` / `CE_BLOB_MISMATCH` / `CE_NO_SIDECAR_PATH` / `CE_NO_SIDECAR_ANCHOR` / `CE_BAD_SIDECAR_ANCHOR` / `CE_SIDECAR_MISSING` / `CE_SIDECAR_MISMATCH` / `CE_SIDECAR_UNANCHORED` |
| 6 | SHA format or length invalid | `CE_BAD_SHA` / `CE_BAD_SUBJECT` / `CE_BAD_BASE_HEAD` / `CE_BASE_NOT_ANCESTOR` |
| 7 | NOT_VERIFIED passed silently / VERIFIED unsupported | `CE_AUTH_NOT_ACK` / `CE_UNFOUNDED_VERIFIED` / `CE_NO_AUTHENTICITY` |
| 8 | Unparseable input, no repository, or internal error | `CE_UNPARSABLE` / `CE_NO_REPO` / `CE_INTERNAL_ERROR` / `CE_INPUT_MISSING` |
| Add. | Classification and downgrade trust boundary | `CE_NO_CLASSIFICATION_BASIS` / `CE_CLASS_UNCONFIRMED` / `CE_CLASS_SELF_CONFIRMED` / `CE_NO_CLASSIFICATION_RECORD` / `CE_CLASS_RECORD_NOT_IN_SUBJECT` / `CE_CLASS_RECORD_MISSING_WORKTREE` / `CE_CLASS_RECORD_BLOB_MISMATCH` / `CE_R2_DOWNGRADE_UNCONFIRMED` / `CE_R2_DOWNGRADE_SELF_CONFIRMED` / `CE_R2_DOWNGRADE_NO_RECORD` / `CE_DOWNGRADE_RECORD_NOT_IN_SUBJECT` / `CE_DOWNGRADE_RECORD_MISSING_WORKTREE` / `CE_DOWNGRADE_RECORD_BLOB_MISMATCH` |
| Add. | Repository identity | `CE_NO_REPOSITORY` / `CE_REPO_IDENTITY_UNVERIFIED` / `CE_REPO_IDENTITY_MISMATCH` |
| Add. | Missing audit fields | `CE_NO_AUDIT_FIELD` / `CE_NO_REVIEW_LEVEL` / `CE_BAD_REVIEW_LEVEL` |

The checker MUST run with a usable Git repository (discovered upward from the declaration's directory, or given via `--repo`); without a repository the result is `CE_NO_REPO` → BLOCKED. "Unable to verify" is never a reason to pass.

The checker emits `VERDICT`, `LEVEL`, `REASON` and `SUMMARY` records. **An exit code alone is not acceptance evidence:** the acceptor MUST verify the actual per-scenario records above.

Exit codes: 0 = PASS; 1 = BLOCKED (declaration defect); 2 = BLOCKED (input/usage error, still fail-closed).

## 7. Bilingual Obligation

This policy is a Tier 1 document (architecture/governance policy). Chinese and English must be updated in the same change set with equivalent meaning, equivalent obligation strength and reciprocal links. A missing counterpart means NOT DONE.

## 8. Change and Effectiveness

1. Any change to Level definitions, required field sets or non-downgrade rules requires a formal change record (rationale, affected files, proposer, approver, effective version).
2. This policy is PROPOSED until formally adopted by the governance authority; passing independent review and merging an implementation does not constitute adoption.
3. The adoption record MUST state the approver, effective date, and the checker version and commit SHA in force.
4. The blank form for the adoption record is `14-ai-development/work-items/ADOPTION-EVIDENCE-2026-P1/adoption-record-template.md`; the assembly of ready and missing evidence is `adoption-evidence-dossier.md` in the same directory. Both are preparation material: neither constitutes adoption, and neither may be cited as adoption or as proof that an approver exists.
