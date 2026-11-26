---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every line number and every count in the acceptance text was re-read on 2026-11-25 from the immutable snapshot of main at a1533c67, with git show and grep against that ref; the byte size and digest of this file were measured from the committed blob after the manifest pinned them."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# WO-02 / F8 — executed instruction (not yet executed)

Scope: make the storage contract able to say *why* a write was refused, so that a
duplicate creation and a genuinely invalid reference stop arriving at the caller
as the same value. Four production files and one existing test file. No schema
migration. No change to what the CLI does with the answer — that is WO-03.

## What is actually there, measured at `a1533c67`

| fact | measurement |
|---|---|
| contract variants | `crates/memory-storage/src/lib.rs:7-21` declares `StorageError` with 13 variants; the string `AlreadyExists` occurs 0 times anywhere under `crates/` |
| fold site 1 | `crates/memory-storage-sqlite/src/lib.rs:317` — `.map_err(\|_\| StorageError::InvalidReference)?` on the `INSERT INTO memories(...)` at `:308-309` |
| fold site 2 | same file `:555`, on the `INSERT INTO versions(...)` |
| fold site 3 | same file `:793`, on an `INSERT INTO publication_preparations(...)` |
| why it collides | `crates/memory-storage-sqlite/src/lib.rs:85-89` declares `CREATE TABLE IF NOT EXISTS memories ( memory_id TEXT PRIMARY KEY, ...)`, so a second insert of the same `memory_id` is a constraint violation and nothing else |
| genuine invalid-reference producers | `crates/memory-store/src/lib.rs:419` and `:488` return `InvalidReference` when `request.memory_id != request.new_version.memory_id`. That is the condition the folded SQLite path is indistinguishable from |
| facade pass-through | `crates/memory-store/src/lib.rs:46-55` forwards `create_memory` to the port with no classification of its own |
| caller | `crates/brain-cli/src/main.rs:694-696` formats whatever variant arrives into `create_memory failed: {error:?}` |
| the one-direction contract test | `crates/memory-store/tests/cross_crate_contract.rs` is 271 lines. Its only assertion naming a storage variant for this case is `:269`, `Err(MemoryStoreError::Storage(StorageError::InvalidReference))`, inside `c6_duplicate_memory_creation_preserves_the_storage_error_variant`. Nothing in that file asserts the other direction: that a genuine `memory_id` mismatch still yields `InvalidReference` |

The last row is what "asserted in one direction only" means concretely. `c6`
pins today's conflation as expected behaviour, so it will have to change; it must
change into two assertions, not into one assertion plus a deletion.

## Acceptance asked for

1. The contract gains a variant that means "this identity already exists", and
   `InvalidReference` keeps meaning "the reference does not resolve". Both are
   named in the enum, not inferred from a message string.
2. The three fold sites stop discarding the SQLite error. A constraint violation
   on a primary key is classified as the new variant; anything else keeps a
   classified mapping. An `.map_err(|_| ...)` that discards the cause is gone
   from all three sites.
3. Both storage implementations agree: the SQLite adapter and the in-memory
   store return the same variant for the same duplicate-creation input.
4. The two directions are both asserted in `cross_crate_contract.rs`: duplicate
   creation yields the new variant, and a `memory_id` mismatch yields
   `InvalidReference`. Set equality over the variants the file asserts, not a
   count of tests.
5. No caller turns a real reference error into a success. The CLI still exits
   non-zero on a `memory_id` mismatch and names `InvalidReference`; it must not
   name the new variant for that input.
6. No DDL change, no migration, no new table.

## Excluded, and stated as excluded

- What the CLI does when it receives the new variant. WO-03 owns that decision
  (read back, reuse, or refuse with a clear message), and WO-02 is the
  precondition that makes the decision expressible at all.
- Any change to `write_revision`, `commit`, `prepare_version` or the publication
  path. The other 83 `map_err(|_| ...)` occurrences in
  `memory-storage-sqlite/src/lib.rs` are out of scope unless one of them is the
  cause of a failing criterion above.
- Any schema migration, any new table, any change to
  `crates/memory-storage-sqlite/src/lib.rs:82-136`.

## Ordering constraint that made this WO-02

`crates/memory-storage/src/lib.rs:7-21` has no variant that can express "already
exists", and `crates/memory-storage-sqlite/src/lib.rs:317` reports the primary-key
conflict as `InvalidReference`. A caller that wanted to distinguish "the same
memory is already stored" from "this reference is wrong" had no value to branch
on. That is why the work order sequence in the R29 closeout puts F8 before E2 and
why E2 cannot be accepted on its own.
