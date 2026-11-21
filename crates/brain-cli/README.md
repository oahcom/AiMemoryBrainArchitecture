# brain-cli

The first executable entry point for the Rust workspace. It orchestrates existing domain,
SQLite storage, store-facade, and context APIs; it does not implement new memory semantics.

## Command

```sh
cargo run -p brain-cli --offline -- compile \
  --input crates/brain-cli/fixtures/event.json \
  --out /tmp/ctx.json
```

The compiler skip notice is printed to stderr on every successful run,
regardless of whether `--verbose` is supplied.

The command preserves its existing exit status: a successful context build
still exits with status `0`.

The input is a JSON envelope containing the domain Event, its referenced raw payload,
the Memory metadata, one Claim, and the context identity. The memory lifecycle is supplied
by the input and is validated by the existing context builder: only Active or Consolidated
memories are eligible for a ContextCandidate.

## Executed path

1. Deserialize and validate the existing domain Event and Claim types.
2. Construct and validate Memory and MemoryVersion.
3. Persist through `SqliteMemoryStorage` in a temporary file-backed SQLite database.
4. Call `MemoryStore::create_memory`, `write_revision`, and `read_current`.
5. Build a ContextSnapshot with `memory_context::build_context` and serialize it to `--out`.
6. Write a compiler-status sidecar recording that the compiler stage was skipped.

The temporary database is removed after the command. The JSON output contains no runtime
timestamps or generated random identifiers, so identical input produces identical output.

The ContextSnapshot JSON serialization contract is unchanged. The compiler status
is recorded in a separate sidecar file alongside the output.

For `/tmp/ctx.json`, the sidecar is:

`/tmp/ctx.json.compiler-status`

Its complete contents are:

```text
compiler stage skipped: PublicationAuthority has no production implementation
```

## Compiler boundary

`memory-compiler` exposes a typed `MemoryCompiler::compile` pipeline, but its publication
gate requires a `PublicationAuthority` implementation that obtains proof from authoritative
D/Storage boundaries. The repository has no production implementation of that authority.
The compiler also requires prior durable producer/dependency admission records. This CLI
does not fabricate either prerequisite and does not call the publication path.

The CLI does not execute the compiler publication path. Every successful invocation
prints the skip notice to stderr and records the same declaration in the
`.compiler-status` sidecar. This behavior is unconditional and does not depend on
`--verbose`.

A successful ContextSnapshot build must not be interpreted as a compiler publication
or as externally authorized memory.

### Exit status

The existing exit-status behavior is preserved:

| Status | Meaning |
|---|---|
| `0` | Existing successful context-build and output path; compiler stage skipped and explicitly recorded |
| `1` | Existing command usage or runtime error |

## Fixture

`fixtures/event.json` is a minimal deterministic input accepted by the command.
