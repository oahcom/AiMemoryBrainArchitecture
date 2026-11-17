# Exact-version review input — Storage Archive × Forget × Inventory × Restore v1

- Review target Blob: `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`
- Target commit: `a65973093bb33c7c06ae503f421e096fadb5796b`
- Target path: `reviews/storage-consistency/archive-producer-classification-forget-inventory-restore-atomicity-v1.md`
- Review provenance: Session P coordinator role simulation, not an independent module Owner decision.
- Status: Technical review input only; no interface freeze or implementation approval.

## E — Compiler / producer lifecycle / publication

**Simulated disposition: ACCEPT WITH ENUMERATED CONDITIONS.** E owns queue/worker/compiler lifecycle, work identity, staged outputs and its publication facts. D owns Forget registration/barrier semantics; I owns permission/inventory; Storage owns physical commit/visibility mechanics.

### Findings

1. **BLOCKER — admission-to-scheduling atomic handoff (§5.1).** Define the exact durable ordering between D ProducerWork registration receipt, E queue/outbox insertion and worker lease acquisition. A worker must never execute protected work before D admission is authoritative. If D registration succeeds but queue insertion ACK is lost, E must recover the same WorkItem and same request digest, not create a replacement work ID.

2. **BLOCKER — stable work and attempt identity (§§5.1–5.2, 8).** Specify ProducerWorkItemId, CompilerJobRef, AttemptRef, LeaseGeneration, RetryRef, DLQEntryRef and ReplayRef as distinct identities. Worker replacement/lease expiry increments attempt generation but preserves logical work identity and dependency set. Retries cannot bypass a fence or become invisible to D.

3. **MAJOR — deterministic output provenance (§§5.1, 7).** Bind each staged output to input revision set, full dependency digest, compiler binary/version, config/model/ruleset version, request digest and output content digest. Partial outputs remain private; output identity must not be inferred from object path or queue message ID.

4. **BLOCKER — ambiguous publication/ACK (§§5.2–5.3).** Define same-ID authoritative lookup for crashes after prepare, visibility commit, outbox publish and ACK loss. Retry queries the same PublicationOperationId/ProducerWorkItemId and terminal record. No fresh ID, alternate output or replay may bypass UNKNOWN/IN_DOUBT. A transactional outbox is required where queue delivery and durable state are separate.

5. **MAJOR — terminal work and barrier release (§§5.1, 6.2).** D cannot terminalize while E has queued, leased, executing, retryable, DLQ or replayable work that can create descendants. Define E's authoritative terminal evidence and how D consumes it. Restore must reconcile all queue/lease/DLQ/replay states against the restored cutoff and current D fence before E-local release.

### Required E-owned closure evidence
- Exact E decision pinned to target Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`.
- Queue/lease/retry/DLQ/replay/outbox state machine with crash points.
- Stable ID and digest contract; D registration handoff and publication ordering.
- Same-ID lost-ACK recovery proof and restore reconciliation matrix.
- Negative vectors for D receipt loss, lease expiry during fence, duplicate queue delivery, partial output, crash after visibility commit, DLQ replay after terminalization.

**Freeze impact:** Conditional blocker until D's admission/barrier contract is stable and Storage's publication boundary is exact.
