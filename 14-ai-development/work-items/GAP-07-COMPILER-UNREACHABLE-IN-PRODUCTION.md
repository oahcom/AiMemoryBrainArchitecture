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

## Evidence (verified on `main @ b961ba31`)

Every claim below is a repository search, reproducible without reading any
owner handoff.

**1. Both `PublicationAuthority` implementations are inside `#[cfg(test)]`.**

```sh
grep -rn "impl PublicationAuthority" --include=*.rs crates/
```

```
crates/memory-compiler/src/lib.rs:899: impl PublicationAuthority for TestAuthority {
crates/memory-compiler/src/lib.rs:1227: impl PublicationAuthority for RecoveryAuthority {
```

`#[cfg(test)]` appears at lines 738, 745, 856, 1177, 1434. Both implementations
fall after 856 and before 1434, i.e. inside test-only modules. Neither is
reachable from a non-test build.

**2. `compile()` is called only from tests.**

```sh
grep -n "\.compile(" crates/memory-compiler/src/lib.rs
```

All five hits are at lines 1095–1157, inside the `#[cfg(test)]` module starting
at 1177's predecessor block. `grep -rn "MemoryCompiler" crates/` outside
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

**4. End-to-end run reproduces the skip.**

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
be obtained. This is the only direction that makes the compiler reachable. It
requires first naming the production publication store, which does not exist
yet.

### (b) Wire `brain-cli` to fail closed instead of skipping

Change the CLI from "skip the compiler stage" to "refuse to produce output
unless a publication authority is configured". This does not add capability but
removes the false impression that `brain compile` compiles. It is small and
honest, and it makes the gap visible to anyone running the binary rather than
only to anyone reading the source.

### (c) Leave as is and stop calling the path end-to-end

Keep the skip, and stop describing `brain compile` as an end-to-end pipeline in
any document or report. The risk is that the skip notice lives in `--verbose`
stderr and is easy to miss.

## Recommendation

Do **(b) now, (a) when a publication store is specified.** The skip notice is
currently the only signal that the most important stage did not run, and it is
suppressed without `--verbose`. A CLI that silently returns a context snapshot
after skipping compilation is worse than a CLI that refuses, because the output
looks correct.

Direction (a) must not be improvised. Implementing a `PublicationAuthority`
against an ad-hoc store would manufacture the same class of unreachable
abstraction this item is about.

## Closure criteria

1. Either a production `PublicationAuthority` exists and `compile()` is called
   from at least one non-test code path, or `brain-cli` refuses to emit output
   when the compiler stage cannot run.
2. A test proves the chosen behavior through the binary or a non-test entry
   point — not through `#[cfg(test)]` internals.
3. `--verbose` is no longer the only place the skip is reported.
4. No document describes `brain compile` as compiling an event until (1) holds
   for the real authority.
