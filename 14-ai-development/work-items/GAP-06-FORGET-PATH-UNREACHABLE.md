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

## Candidate implementation directions

### (a) Add `MemoryStore::forget(namespace_key, reason)` and delegate to `ForgetFence`

This gives callers an obvious Store-level operation, but the Store must coordinate the event-store fence and Memory storage. Correctness requires a shared connection or a transaction/commit protocol spanning the crates; otherwise a fence could commit while the Memory read gate remains unaware of it. This is a cross-crate change with nontrivial atomicity and failure-ordering requirements.

### (b) Enforce the fence in the MemoryStorage read path

Make the storage read boundary consult the authoritative namespace fence before returning a current revision (and define the same rule for every other read path). This puts enforcement at the boundary that actually returns data, rather than relying on callers to remember a Store-level precondition. It adds a fence lookup to reads and requires a well-defined shared database/schema or equivalent atomic visibility contract between the memory store and fence writer.

### (c) Keep the path unreachable pending an engineering-phase decision

Do not add a partial API or pretend that event-store restore is a Memory forget operation. Keep the desired E2E ignored and record this item as requiring an engineering-phase ruling. The consequence is that the ignored E2E remains indefinitely and no Memory-level forget guarantee exists until that ruling is implemented.

## Recommendation

**Recommend (b): enforce the fence at the MemoryStorage read boundary.** The security/correctness property is “a fenced namespace cannot yield a Memory revision,” so the check belongs at the last common boundary before data is returned. A Store-only method can be bypassed by direct Storage consumers or future read entry points; a read-boundary invariant is harder to bypass and gives one place to fail closed. The implementation must first settle how the memory database observes the fence atomically (shared SQLite database/connection or an explicitly specified equivalent); this work item does not authorize an ad hoc second database query with a race window.

## Closure criteria

Close this item only when all of the following are true:

1. A public, documented contract connects the durable namespace fence to MemoryStorage reads, including failure behavior if fence state is missing, corrupt, or unavailable.
2. Every public read path that can return a Memory revision enforces that contract; a fenced namespace returns no readable revision (or a typed refusal), never the pre-fence revision.
3. The implementation has an atomicity/visibility story for fence recording versus concurrent reads and is covered by tests across the relevant storage adapter boundary.
4. The reverse test `forget_fence_is_not_yet_enforced_by_memory_store_reads` is changed to assert the enforced behavior or removed with an explicit replacement regression test, and the ignored desired E2E `forgotten_memory_is_excluded_from_context` is enabled and passes.
5. The relevant crate tests and workspace validation pass on the merged implementation.

Until these conditions are met, keep this work item open and retain both tests as executable documentation of the current and desired contracts.
