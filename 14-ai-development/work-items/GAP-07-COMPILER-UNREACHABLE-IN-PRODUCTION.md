# GAP-07 — The compiler stage is unreachable in production

**Status:** Open — blocks every end-to-end claim about compilation
**Area:** GAP-01 / memory-compiler / brain-cli
**Owner track:** Owner E (Compiler Admission) + Owner A (E2E)

## Gap statement

`MemoryCompiler::compile` has no production implementation of its required
`PublicationAuthority` trait, and no non-test caller. The only executable
entrypoint in the repository (`brain-cli`) therefore skips the compiler stage
entirely and says so at runtime:

```
compiler stage skipped: PublicationAuthority has no production implementation
```

Everything downstream of `memory-context` works end to end. Everything inside
`memory-compiler` is exercised only by `#[cfg(test)]` code.

## Evidence (re-verified on `main @ 5643974b`, after #523 and #533)

Every claim below is a repository search, reproducible without reading any
owner handoff.

**1. All three `PublicationAuthority` implementations are inside `#[cfg(test)]`.**

```sh
grep -rn "impl PublicationAuthority" --include=*.rs crates/
```

```
crates/memory-compiler/src/lib.rs:923: impl PublicationAuthority for EvidenceAuthority {
crates/memory-compiler/src/lib.rs:942: impl PublicationAuthority for TestAuthority {
crates/memory-compiler/src/lib.rs:1332: impl PublicationAuthority for RecoveryAuthority {
```

`#[cfg(test)]` appears at lines 757, 764, 875, 1282, 1539. The module gated at
875 covers 923 and 942; the module gated at 1282 covers 1332. All three
implementations are therefore test-only and unreachable from a non-test build.

Note that #533 added `EvidenceAuthority` to model the four publication
dispositions. That is a real improvement to the test model and it does not
change this gap: the new implementation is the third one, and it is also
test-only.

**2. `compile()` is called only from tests.**

```sh
grep -n "\.compile(" crates/memory-compiler/src/lib.rs
```

All hits are at lines 1187–1249, inside the `#[cfg(test)]` module gated at
1282. `grep -rn "MemoryCompiler" crates/` outside
`memory-compiler/src/lib.rs` returns **zero matches**.

**3. `brain-cli` imports the compiler for a version string only.**

```sh
grep -n "memory_compiler" crates/brain-cli/src/main.rs
```

```
1:use memory_compiler::COMPILER_VERSION;
```

The CLI wires `memory-domain` → `memory-storage-sqlite` → `memory-store` →
`memory-context`, then stops. Its own verbose output confirms this ordering.

**4. The publication primitive now exists but is not exposed.**

#523 added exactly the storage operation `PublicationProof.storage_prepared_hidden`
needs. It is on the trait and implemented in SQLite:

```sh
grep -n "prepare_version\|publish_prepared" crates/memory-storage/src/lib.rs
```

```
74: fn prepare_version(&mut self, request: PrepareRequest, scope: &[ScopeRef]) -> Result<PreparedCommitReceipt, StorageError>;
77: fn publish_prepared(&mut self, publication_id: &str, expected_current_version: Option<OpaqueId>, scope: &[ScopeRef]) -> Result<CommitReceipt, StorageError>;
```

`memory-storage-sqlite` implements both. But `MemoryStore` — the façade the CLI
actually uses — exposes none of it:

```sh
awk 'NR<200 && /pub fn /{print NR": "$0}' crates/memory-store/src/lib.rs
```

```
33:     pub fn new(storage: S) -> Self { Self { storage } }
35:     pub fn into_storage(self) -> S { self.storage }
37:     pub fn create_memory(
48:     pub fn read_current(
57:     pub fn read_revision(
67:     pub fn write_revision(
89:     pub fn resolve_idempotency(
```

The only `prepare_version`/`publish_prepared` bodies in `memory-store` are on
`FakeStorage` at lines 212 and 286, inside the `#[cfg(test)]` module gated at
112. So the primitive exists one layer below where anything can call it, and
the one layer that could call it does not surface it.

**5. End-to-end run reproduces the skip.**

A real event JSON through `brain compile --verbose` produces a valid
1103-byte ContextSnapshot with one entry, and prints the skip notice above.
The pipeline is genuinely end-to-end up to and including context assembly;
the compiler is not in it.

## Why this matters more than a test count

`GAP-BASELINE-004` measured 338 passing tests. A large share of those live in
`memory-compiler` (53 at that measurement) and all of them exercise a `compile`
path that no production caller can reach. Test count is therefore **not**
evidence that compilation works in the product. Any statement of the form
"the pipeline compiles an event into a published derivative" is currently
untrue outside `cargo test`.

This is not a defect in Owner E's admission work. The admission ledger,
producer registry, dependency closure and fence are implemented and tested.
The gap is that the authority they feed has no production implementor.

## Candidate directions

### (a) Ship a real `PublicationAuthority`

Implement the trait against the actual publication path: obtain the proof from
whatever durable publication record exists, return typed failure when it cannot
be obtained. This is the only direction that makes the compiler reachable.

#523 materially reduces the work: `prepare_version` returns a
`PreparedCommitReceipt` proving the derivative is staged but not yet readable,
which is what `storage_prepared_hidden` asserts. Two things are still missing
before this can be done honestly: `MemoryStore` must surface prepare/publish,
and the publication record must be durable across process restart rather than
held in the compiler's in-memory admission store.

### (b) Make the skip unmissable, and mark the output

An earlier draft of this item recommended "refuse to produce output". That is
too blunt: it would disable the one working entrypoint and remove the only
executable demonstration that ingestion → storage → context assembly works.
The real defect is not that the CLI runs; it is that a plausible-looking output
can be produced without anyone learning that the most important stage was
skipped.

Minimal honest version:

1. Print the skip notice unconditionally, not only under `--verbose`. It is
   currently inside an `if verbose` block, so the default run says nothing.
2. Record the skip in the produced artifact, so the fact travels with the file
   instead of being lost when stderr is not read. This must not change the
   `ContextSnapshot` serialization contract; a sibling sidecar or an explicit
   top-level marker outside the snapshot is enough.
3. Leave the exit status alone, so existing callers do not break.

This keeps the pipeline runnable while making "this was not compiled"
impossible to mistake for "this was compiled".

### (c) Leave as is and stop calling the path end-to-end

Keep the skip, and stop describing `brain compile` as an end-to-end pipeline in
any document or report. The risk is that the skip notice lives in `--verbose`
stderr and is easy to miss.

## Recommendation

Do **(b) now, (a) when a publication store is specified.** (b) as scoped above
is a few lines and does not remove capability. A CLI that returns a context
snapshot after skipping compilation, while staying silent unless `--verbose` is
passed, is worse than one that refuses, because the output looks correct; but
one that refuses outright also destroys the only working demonstration. Making
the skip unconditional and attaching it to the output gets the honesty without
the loss.

Direction (a) must not be improvised. Implementing a `PublicationAuthority`
against an ad-hoc store would manufacture the same class of unreachable
abstraction this item is about.

## Closure criteria

1. Either a production `PublicationAuthority` exists and `compile()` is called
   from at least one non-test code path, or every successful `brain compile`
   run reports that the compiler stage was skipped, both on stderr without
   requiring `--verbose` and inside or beside the produced artifact.
2. A test proves the chosen behavior through the binary or a non-test entry
   point — not through `#[cfg(test)]` internals.
3. `--verbose` is no longer the only place the skip is reported.
4. No document describes `brain compile` as compiling an event until (1) holds
   for the real authority.
