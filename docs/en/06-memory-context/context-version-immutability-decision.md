# ContextVersion Immutability Decision

- Authority: user-authorized operator (delegated by account owner)
- Decision date: 2026-11-26
- Decision status: direction recorded; G and A exact-version acceptance pending
- Canonical source: [context-versioning.md](../../../06-memory-context/context-versioning.md)
- Related Issues: #1144, #1151

## Decision

A committed ContextVersion is an immutable historical aggregate. Its identity, sequence, parent, snapshot reference/hash/profile, exact committed ContextEntryVersion set, source/provenance references, Scope and commit metadata cannot be rewritten. A committed ContextEntryVersion and its content are immutable under that entry revision. The mutable current-head pointer may advance only as part of the same atomic commit that accepts a new ChangeSet and records its immutable receipt/idempotency result.

A ContextChangeSet is an immutable mutation request. Changing its payload requires a new ChangeSet identity. The only ordinary mutation path is: construct a ChangeSet against an exact base version; validate Scope, authorization and current head; compute/verify the resulting snapshot commitment inside the trusted commit boundary; atomically persist the successor ContextVersion, entry revisions, commit receipt/idempotency result and head advancement. A stale base is rejected; rebasing creates a new ChangeSet. A retry with the same idempotency identity and digest returns the prior result; the same identity with a different digest is a conflict.

Correction, reorder, replacement, membership removal, invalidation, supersession, rollback and Forget create a successor ContextVersion. They never edit a committed version in place. Forget/revocation makes affected historical versions non-serving for current use; it does not make them mutable. Physical payload erasure is a separate I-governed retention action: it may remove payload under explicit authorization and evidence, while preserving a non-reconstructive tombstone/audit proof. Immutability is not a requirement to retain forbidden plaintext forever.

## Violation definition

A violation exists if any of the following is observed: (a) the same ContextVersion ID/sequence resolves to different committed bytes or metadata; (b) an entry's content changes under the same ContextEntryVersion revision; (c) the head advances without one accepted ChangeSet and corresponding commit/idempotency receipt; (d) a stale base is accepted; (e) a committed record is updated/deleted in place outside an I-authorized erasure with tombstone evidence; or (f) a mismatched snapshot commitment is accepted.

## #1144 / #1151 evidence disposition

#1144 remains OPEN because durable ContextVersion history, head, ChangeSet and idempotency state are not proven to survive restart. This decision defines immutability but does not implement or prove persistence.

#1151's stated missing-recomputation defect is not reproduced on the measured main source: commit_change_set computes snapshot_hash(&staged) and rejects a mismatch; snapshot_hash sorts by entry ID and serializes the complete entries. The current reference digest is FNV-1a 64-bit and is not cryptographically collision-resistant. That is a distinct digest-strength question, not evidence that recomputation is absent. #1151 remains OPEN for accountable Owner disposition; this document does not close it.

## Reviewer-verifiable criteria

- CV-I1 PASS iff committed version identity and all committed fields/entries cannot change in place; otherwise FAIL.
- CV-I2 PASS iff every semantic change creates a new successor version via an accepted ChangeSet; otherwise FAIL.
- CV-I3 PASS iff head advancement is atomic with successor version and durable commit/idempotency receipt; otherwise FAIL.
- CV-I4 PASS iff stale bases and changed payload under reused identity are rejected; otherwise FAIL.
- CV-I5 PASS iff I-authorized erasure is a separately evidenced purge/tombstone, not silent version mutation; otherwise FAIL.
- CV-I6 PASS iff #1151's missing-recomputation claim is recorded as not reproduced and the FNV-1a strength limitation is kept separate; otherwise FAIL.

Open: durable storage/recovery acceptance under #1144; exact canonical serialization and digest-strength decision; G Owner and A governance acceptance; runtime conformance.
