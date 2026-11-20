# Adoption Record Template

**Purpose.** Both `AI-DOC-EVIDENCE-TIERING` and `AI-DOC-BILINGUAL-TIERING` are `PROPOSED` and each mandates an adoption record as the act that makes it effective. Neither policy ever said where that record lives or what shape it takes. This file is that shape. It is a **blank form**: nothing here is adopted, approved, or effective.

**Status of this file:** TEMPLATE. Nothing in it is a record of anything.

---

## Part A — fields common to both policies

These four fields are required by both policies' section 8. Until all four carry real values, the policy in question is `PROPOSED` and its gates are not in force.

| Field | Value | Who may fill it |
|---|---|---|
| `approver` | **PENDING** | The project governance authority only. NOT any ChatGPT session, NOT the coordinator, NOT the implementing Owner. |
| `effective_date` | **PENDING** | Set by the approver at the moment of adoption. Never back-dated. |
| `policy_id` | `AI-DOC-EVIDENCE-TIERING` or `AI-DOC-BILINGUAL-TIERING` | Fixed by the policy text. |
| `policy_blob_at_adoption` | **PENDING** | The blob SHA of the policy file exactly as it stands when the approver signs. It MUST be re-measured at signing time, not copied from an earlier dossier. |

## Part B — policy-specific required fields

### For `AI-DOC-EVIDENCE-TIERING` (section 8 item 3)

| Field | Value |
|---|---|
| `checker_path` | `scripts/governance/evidence/check-evidence-tiering.py` |
| `checker_version` | **PENDING** — a version identifier the approver accepts (the script carries no version constant; a tag or the blob SHA serves) |
| `checker_commit_sha` | **PENDING** — the commit SHA in force at adoption |

### For `AI-DOC-BILINGUAL-TIERING` (section 8)

| Field | Value |
|---|---|
| `inventory_kind` | per-file classification inventory |
| `inventory_path` | **PENDING** — the approved per-file list. Neither `tier-mapping-proposal.yaml` nor `tier-confirmation-proposal.yaml` is that list; both are proposals and say so in their own headers. |
| `inventory_sha` | **PENDING** — SHA of the approved list |

## Part C — attestation block (unsigned)

```
I, <approver>, adopt <policy_id> effective <effective_date>.
Policy blob at adoption: <policy_blob_at_adoption>.
<Policy-specific fields from Part B, filled.>
I confirm that the per-file / per-level obligations in the adopted text are
the ones I intend to make binding, and that every item the policy marks
UNKNOWN or PENDING remains unconfirmed at adoption unless separately listed.
```

An adoption record without a completed Part C is not an adoption record.

## What this template does not do

- It does not adopt anything. Filling a field in a copy of this template does not adopt a policy.
- It does not supply an approver. No approver is assignable by the coordinator or by any ChatGPT session.
- It does not close the UNKNOWN / PENDING counts. Those are separate confirmations, and the bilingual policy is explicit that they cannot be auto-promoted.
