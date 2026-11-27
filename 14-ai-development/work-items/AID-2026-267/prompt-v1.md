# AID-2026-267 — Prompt snapshot

Prompt status: RECORDED_NOT_FROZEN
Provenance: USER_AUTHORIZED_DELEGATED_REQUEST
Capture type: structured scope snapshot, not a byte-for-byte chat export.

## Requested outcome

Implement Issue #134's remaining P0 closure condition in
oahcom/AiMemoryBrainArchitecture: enforce required ⊆ declared ⊆ produced in
scripts/check_declared_check_contexts.py.

## Mandatory behavior

- Read the live branch payload through GET /repos/{owner}/{repo}/branches/{branch},
  using protection.required_status_checks.contexts; do not use /protection.
- Reuse declared_contexts().
- Exit 0 only when every required context is declared and every declared context
  is produced; print declared, required and produced counts and both empty diffs.
- Exit 1 and name a context required by the branch but absent from the document.
- Preserve exit 1 for a declared context not produced by any workflow.
- Exit 2 and name the unavailable input and reason when the payload cannot be
  read, is None, or lacks the required field.
- Test injected payloads, including a required-only context and unavailable
  payload; do not depend on live branch state for probes.
- Keep the existing workflow invocation hard-failing; no warn-only or 