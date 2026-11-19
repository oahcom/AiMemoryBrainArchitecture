# AI Work Items Index

This index is the entry point for all governed AI development tasks.

| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |
|---|---|---|---|---|---|---|---|---|
| [AID-2026-001](AID-2026-001/manifest.yaml) | Define ChatGPT-native execution model | A + D + I | ARCH/SEC/R3 | REMEDIATION_IN_PROGRESS — U-010 D-side and U-011 I-side EN/ZH candidates recorded; prior independent bilingual review FAIL; I-U012-001/002 author-side remediation recorded; fresh exact-Head re-review, formal I approval, D/I same-SHA, Storage and R3 evidence pending | [prompt-v2](AID-2026-001/prompt-v2.md) | Historical FAIL at 1d6ab393; fresh exact-Head review pending | BLOCKED_PENDING_R3_EVIDENCE |
| [AID-2026-010](AID-2026-010/manifest.yaml) | Issue #43 — Cross-domain Architecture Integration Review and Evidence Reconciliation | Integration Owner (Accountable: NOT_ASSIGNED) | ARCH/R3 (tentative) | IN_PROGRESS — 9/13 Findings CLOSED (F1/F2, F1/F3, F-43-03, F-43-04, F-43-05, F-43-06B, F-43-08, F-43-09, F-43-10); F-43-02/06A/07/F1/F1 remain BLOCKED/OPEN | [prompt-batch2-dispatch](AID-2026-010/prompt-batch2-dispatch.md) v2 SHA-256 4906dc8ee80e3e1e0f842178c09d3600a8c29cc0d427ee1b1a55c3dca22d0c10 + [continuation](AID-2026-010/prompt-batch2-continuation.md) 245a68b6bd06157e5d3ed5827c55e751be0436f34358deb1fcc46b16c72db30e | 14-ai-development/issue-alignment-2026-11-19/ (evidence archive) | PROGRESS — 9/13 CLOSED; architecture NOT ACCEPTED (G8 NOT READY) | IN_PROGRESS — #43 OPEN |
| [AID-2026-011](AID-2026-011/manifest.yaml) | Storage Owner — F-43-06A JoinProof Dual-Persistence & F-43-07 Stage 2 ParticipantRef Acceptance | Storage Owner | ARCH/R3 | COMPLETED — F-43-06A CLOSED (A R43), F-43-07 Stage 2 ACCEPT WITH LIMITATIONS (A-reviewed) | AI-EXEC-001 v1.1 + AI-EXEC-002 v1.1 | N/A (normative work) | A R43 reviewed | DONE |
| [AID-2026-012](AID-2026-012/manifest.yaml) | H Owner — F-43-07 Stage 3 Consumer Mapping Independent Acceptance | H Owner | ARCH/R3 | COMPLETED — H-OWNER-2026-11-20-001 ACCEPT WITH LIMITATIONS | AI-EXEC-001 v1.1 + AI-EXEC-002 v1.1 | N/A (review work) | DONE | DONE |
| [AID-2026-013](AID-2026-013/manifest.yaml) | COC Owner — F-43-07 Applicability Decision & ParticipantIntent Authority | COC Owner | ARCH/R3 | REGISTERED — dev-baseline auto-registration; COC applicability pending | AI-EXEC-001 v1.1 + AI-EXEC-002 v1.1 | N/A (authority decision) | PENDING | PENDING |

## Registration rules

- Create a unique `AID-YYYY-NNN` before substantive work begins.
- Create the work-item directory and manifest before prompt execution.
- Link the exact prompt version and SHA-256 used by each run.
- Update this index when status changes at major gates and at closeout.
- Never delete rejected, blocked or superseded records; mark their final disposition.
