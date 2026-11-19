# AI-STD-001 Status Migration Map (EN)

**Work item:** P1-T2 — Process Governance Improvement  
**Source:** AI-STD-001 §4.1, the actual 12 canonical states  
**Target:** Six operational phases; source status remains immutable evidence.

| Exact source state | Target phase | Independent evidence retained |
|---|---|---|
| PROPOSED, ANALYZED, PROMPT_READY | INTAKE | sponsor/Owner; impact analysis; frozen prompt identity, version, hash and base |
| READY | READY | dependencies/contracts and explicit Owner readiness |
| IN_PROGRESS, IMPLEMENTED | ACTIVE | branch/progress; commit, changed-file list and self-check |
| VERIFIED, REVIEWED, INTEGRATION_READY | VALIDATION | exact test evidence; independent review report/dispositions; integration compatibility evidence |
| ACCEPTED | ACCEPTANCE | explicit authorized acceptance decision |
| MERGED, CLOSED | COMPLETE | merge target/SHA and separate closeout/index evidence |

## Non-loss and safety rules

1. Preserve the exact original status string, including suffixes, in source_status. Keep the original status field unchanged during compatibility migration.
2. lifecycle.phase is only a grouping. lifecycle.gates independently records verified, independent_review, integration, owner_acceptance, merge and closeout. A phase never implies a gate passed.
3. VERIFIED, REVIEWED, INTEGRATION_READY, ACCEPTED, MERGED and CLOSED remain distinct checkpoints.
4. BLOCKED and REJECTED are orthogonal markers, not phases. Preserve their reason, responsible party, known timestamp and resolution/disposition evidence. Never infer them.
5. Architecture-decision lifecycle/status remains independent and is out of scope. Owner role definitions, including Owner G's charter, are unchanged.
6. Unknown, missing, ambiguous or unrecognized decorated statuses fail closed and remain unchanged.
7. Migration is additive, idempotent, dry-run by default, backup-first and reversible. Backups are byte-for-byte; rollback restores exact bytes.
8. Never infer missing review, acceptance, integration, merge or closeout evidence. Missing evidence remains NOT RECORDED.

## Six phases

- INTAKE: proposal, analysis and prompt preparation.
- READY: execution prerequisites satisfied.
- ACTIVE: implementation underway or submitted.
- VALIDATION: verification, independent review and integration-readiness checkpoints.
- ACCEPTANCE: authorized acceptance decision.
- COMPLETE: merge and closeout checkpoints.

The migration tool adds lifecycle.phase, lifecycle.source_status, lifecycle.gates and lifecycle.markers without deleting or rewriting historical evidence. The original status remains intact until a separately authorized consumer inventory and cutover.
