# AI Work Items Index

This index is the entry point for all governed AI development tasks.

| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |
|---|---|---|---|---|---|---|---|---|
| [AID-2026-001](AID-2026-001/manifest.yaml) | Define ChatGPT-native execution model | A + D + I | ARCH/SEC/R3 | REMEDIATION_IN_PROGRESS — U-010 D-side and U-011 I-side EN/ZH candidates recorded; prior independent bilingual review FAIL; I-U012-001/002 author-side remediation recorded; fresh exact-Head re-review, formal I approval, D/I same-SHA, Storage and R3 evidence pending | [prompt-v2](AID-2026-001/prompt-v2.md) | Historical FAIL at 1d6ab393; fresh exact-Head review pending | BLOCKED_PENDING_R3_EVIDENCE |
| [AID-2026-010](AID-2026-010/manifest.yaml) | Issue #43 — Cross-domain Architecture Integration Review and Evidence Reconciliation | Integration Owner (Accountable: NOT_ASSIGNED) | ARCH/R3 (tentative) | PROPOSED — registration REGISTERED (A-OWNER-ALIGNMENT-001-R17 status reconciliation); supplement received, integration review authorized | L2-05 batch2 supplement + A R16 ruling (SHA-256 NOT_VERIFIED) | 14-ai-development/issue-alignment-2026-11-19/ (evidence archive) | PENDING — integration review continues in L2-05 session 6afeef2f | PROPOSED — #43 remains OPEN; no Finding closed |

## Registration rules

- Create a unique `AID-YYYY-NNN` before substantive work begins.
- Create the work-item directory and manifest before prompt execution.
- Link the exact prompt version and SHA-256 used by each run.
- Update this index when status changes at major gates and at closeout.
- Never delete rejected, blocked or superseded records; mark their final disposition.
