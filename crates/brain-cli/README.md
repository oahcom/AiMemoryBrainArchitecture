# brain-cli

The first executable entry point for the Rust workspace. It orchestrates existing domain,
SQLite storage, store-facade, and context APIs; it does not implement new memory semantics.

## Command

```sh
cargo run -p brain-cli --offline -- compile \
  --input crates/brain-cli/fixtures/event.json \
  --out /tmp/ctx.json
```

Add `--verbose` to print each completed stage.

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

The temporary database is removed after the command. The JSON output contains no runtime
timestamps or generated random identifiers, so identical input produces identical output.

## Compiler boundary

`memory-compiler` exposes a typed `MemoryCompiler::compile` pipeline, but its publication
gate requires a `PublicationAuthority` implementation that obtains proof from authoritative
D/Storage boundaries. The repository has no production implementation of that authority.
The compiler also requires prior durable producer/dependency admission records. This CLI
does not fabricate either prerequisite and does not call the publication path.

**compiler stage skipped: PublicationAuthority has no production implementation**

The CLI reports this exact reason with `--verbose`. A successful context build is not
represented as a compiler publication or as externally authorized memory.

## Fixture

`fixtures/event.json` is a minimal deterministic input accepted by the command.
