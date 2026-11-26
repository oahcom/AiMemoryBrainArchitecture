# AID-2026-082 - ContextVersion immutability and legal successor path
Authority: user-authorized operator (delegated by account owner)
Date: 2026-11-26
Base: main 364ef4ad6deeedbd5d383b5855973061503387f8
Issues: #1144 and #1151

Define a committed ContextVersion as an immutable historical aggregate. Freeze its identity, sequence, parent, snapshot reference/hash/profile, exact ordered ContextEntryVersion set, source/provenance refs, Scope and commit metadata. A committed entry revision and its content are immutable. The current-head pointer may move only through an atomic accepted ChangeSet commit.

Legal change path: immutable ChangeSet with exact base version; validate authorization/scope/current head; compute and verify snapshot commitment at the trusted commit boundary; atomically persist successor ContextVersion, entries, commit receipt/idempotency result and head advancement. Stale base is rejected; rebase creates a new ChangeSet. Corrections, reorder, replacement, removal, invalidation, rollback or Forget use a new successor version, never an in-place edit. I-governed retention/erasure may purge payload under explicit policy but must leave a non-reconstructive tombstone/audit proof and must not rewrite a retained version as another version.

Violation: same version ID/sequence with different bytes; mutate entry content under same entry revision; head advances without accepted ChangeSet/receipt; stale base accepted; in-place UPDATE/DELETE except I-authorized erasure with tombstone; wrong snapshot hash accepted.

Current-main finding for #1151: commit_change_set computes snapshot_hash over staged entries and rejects mismatch; snapshot_hash sorts by entry_id and serializes full entries. The implementation's stable_digest is FNV-1a 64-bit, non-cryptographic. The filed missing-recomputation claim is therefore not reproduced; digest-strength concerns are separate and must not be silently conflated.

#1144 durable persistence remains a separate OPEN gap: immutability semantics do not prove the ContextVersion ledger survives restart. Keep both issues OPEN.

PASS/FAIL:
- CV-I1 PASS iff committed version identity and all committed fields/entries cannot change in place; otherwise FAIL.
- CV-I2 PASS iff every semantic change creates a new successor version via an accepted ChangeSet; otherwise FAIL.
- CV-I3 PASS iff the head advances atomically with the new immutable version and durable idempotency/commit receipt; otherwise FAIL.
- CV-I4 PASS iff stale bases and changed payload under reused identity are rejected; otherwise FAIL.
- CV-I5 PASS iff I-authorized erasure is a separately evidenced purge/tombstone, not silent version mutation; otherwise FAIL.
- CV-I6 PASS iff the #1151 recomputation claim is recorded as not reproduced on measured main and the FNV-1a strength limitation is kept separate; otherwise FAIL.

Modify only the canonical Context versioning document, its EN/ZH-CN decision addenda, this Work Item directory and INDEX.md. No runtime/product code, tests, schema, validator, deployment or production changes. Create independent branch and Draft PR; no merge; Issues stay OPEN. G and A retain exact-version acceptance authority.