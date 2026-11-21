# GAP-06 — Forget fence is not connected to MemoryStore reads

**Status:** Open — requires engineering-phase architecture decision  
**Area:** GAP-06 / Memory lifecycle / forget semantics  
**Owner track:** Owner A (E2E Test Architecture)

## Gap statement

There is no public forget API that connects `ForgetFence`'s namespace-fence semantics to the `MemoryStore` read gate, so recording a fence does not currently prevent a memory in that namespace from being read.

## Evidence of unreachability

The repository-level API search is:

```sh
grep -rn "pub fn.*forget" crates/memory-store/src/lib.rs crates/memory-storage/src/lib.rs
```

**Result: zero matches.** The Owner's Round 7 handoff supplied this exact command and zero-match result as an independent repository check; this work item records that evidence without claiming a new local shell execution.

The event-store fence is a separate mechanism: `ForgetFence::record_forget(namespace_key, reason_digest)` persists a namespace fence using its own database connection. Its restore operation applies the fence while restoring the event-store tables; it does not mutate Memory records and is not consulted by `MemoryStorage::read_current` or `MemoryStore::read_current`.

The current negative-path suite therefore keeps the desired end-to-end forget test ignored, while a separate reverse test fixes the present observable behavior: a recorded fence does not stop a MemoryStore read.

## 2. Current readers of the fence

The repository search commands run for this round were:

```sh
grep -RIn 'load_fences' crates/memory-event-store-sqlite crates/memory-store crates/memory-storage crates/memory-storage-sqlite
grep -RInE 'FROM[[:space:]]+forget_fence|INTO[[:space:]]+forget_fence|UPDATE[[:space:]]+forget_fence' crates/memory-event-store-sqlite crates/memory-store crates/memory-storage crates/memory-storage-sqlite
grep -RIn 'restore_backup' crates
```

The Rust production matches are confined to `crates/memory-event-store-sqlite/src/forget_fence.rs`:

- `record_forget` writes the row.
- `open_existing` calls `load_fences` to validate the existing fence database; this reads and validates the rows but does not enforce them against live Memory reads.
- `restore_backup` calls `load_fences`; `load_fences` executes `SELECT namespace_key,fence_seq,reason_digest FROM forget_fence`. The resulting namespace set is used while scanning the backup's `accepted_events.scope_json`, and matching event rows are purged from `accepted_events`, `event_payloads`, and `compile_outbox` before activation.

**Conclusion: the fence has a real enforcement reader, but only in the event-store backup-restore path.** No normal `MemoryStore` or `MemoryStorage` read path reads the fence table. The gap is therefore larger than a missing call from one Store method: the fence is not part of the Memory read boundary at all. The five `tests/forget_fence.rs` integration tests exercise restore behavior, validation/fail-closed behavior, malformed scopes, retry after fence commit, and concurrent recording; they do not establish Memory read enforcement.

The Round 8 behavior probe is named `forget_api_absence_is_detectable`. It deliberately asserts that a Memory revision remains readable after recording a fence. It is green under today's split architecture and must become red when Memory read enforcement is added; at that point remove the characterization test and enable `forgotten_memory_is_excluded_from_context`.


## Candidate implementation directions

### (a) Add `MemoryStore::forget(namespace_key, reason)` and delegate to `ForgetFence`

This gives callers an obvious Store-level operation, but the Store must coordinate the event-store fence and Memory storage. Correctness requires a shared connection or a transaction/commit protocol spanning the crates; otherwise a fence could commit while the Memory read gate remains unaware of it. This is a cross-crate change with nontrivial atomicity and failure-ordering requirements.

### (b) Enforce the fence in the MemoryStorage read path

Make the storage read boundary consult the authoritative namespace fence before returning a current revision (and define the same rule for every other read path). This puts enforcement at the boundary that actually returns data, rather than relying on callers to remember a Store-level precondition. It adds a fence lookup to reads and requires a well-defined shared database/schema or equivalent atomic visibility contract between the memory store and fence writer.

### (c) Keep the path unreachable pending an engineering-phase decision

Do not add a partial API or pretend that event-store restore is a Memory forget operation. Keep the desired E2E ignored and record this item as requiring an engineering-phase ruling. The consequence is that the ignored E2E remains indefinitely and no Memory-level forget guarantee exists until that ruling is implemented.

## Recommendation

**Recommend (b): enforce the fence at the MemoryStorage read boundary.** The security/correctness property is “a fenced namespace cannot yield a Memory revision,” so the check belongs at the last common boundary before data is returned. A Store-only method can be bypassed by direct Storage consumers or future read entry points; a read-boundary invariant is harder to bypass and gives one place to fail closed. The implementation must first settle how the memory database observes the fence atomically (shared SQLite database/connection or an explicitly specified equivalent); this work item does not authorize an ad hoc second database query with a race window.

## Proposed implementation surface (not authorized by this work item)

If implementation is authorized, take direction (b), with the read invariant enforced by the storage adapter rather than by a caller-side precheck:

1. Add `MemoryStore::forget_namespace(namespace_key, reason_digest)` in `crates/memory-store/src/lib.rs`. It validates non-empty inputs and delegates to the storage port; it must not implement a check-then-read sequence itself.
2. Extend the `MemoryStorage` trait in `crates/memory-storage/src/lib.rs` with a durable namespace-fence recording operation. Specify that `read_current` and `read_version` must both refuse a fenced namespace. `MemoryStore::read_current` and `read_revision` already route through those two trait methods.
3. Implement recording and enforcement in `crates/memory-storage-sqlite/src/lib.rs`: the SQLite adapter must make the fence decision at the same storage boundary as the revision read, including a defined transaction/locking strategy. Do not perform a separate preflight query followed by an unprotected read.
4. Refactor `crates/memory-event-store-sqlite/src/forget_fence.rs` to expose transaction/connection-scoped primitives for recording and querying a namespace fence (for example, `record_forget_in` and `is_fenced_in`), while retaining the existing path-based API for restore callers. The adapter must use a shared authoritative fence state and an atomic visibility strategy; simply adding a public `is_fenced` that opens another connection is insufficient to close the race.

Expected primary files: `crates/memory-store/src/lib.rs`, `crates/memory-storage/src/lib.rs`, `crates/memory-storage-sqlite/src/lib.rs`, and `crates/memory-event-store-sqlite/src/forget_fence.rs`, plus adapter and cross-crate tests. This is an implementation map only; it grants no implementation authorization.

## Closure criteria

Close this item only when all of the following are true:

1. A public, documented contract connects the durable namespace fence to MemoryStorage reads, including failure behavior if fence state is missing, corrupt, or unavailable.
2. Every public read path that can return a Memory revision enforces that contract; a fenced namespace returns no readable revision (or a typed refusal), never the pre-fence revision.
3. The implementation has an atomicity/visibility story for fence recording versus concurrent reads and is covered by tests across the relevant storage adapter boundary.
4. The reverse test `forget_api_absence_is_detectable` is changed to assert the enforced behavior or removed with an explicit replacement regression test, and the ignored desired E2E `forgotten_memory_is_excluded_from_context` is enabled and passes.
5. The relevant crate tests and workspace validation pass on the merged implementation.

Until these conditions are met, keep this work item open and retain both tests as executable documentation of the current and desired contracts.
