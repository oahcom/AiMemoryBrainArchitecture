# OWNER-DISPATCH — D4 + production PublicationAuthority adapter

Repository: `oahcom/AiMemoryBrainArchitecture`
Working copy: WSL2 `/home/administrator/brain-wp01` (branch from `origin/main`)
Authoritative decision: `14-ai-development/adr/OWNER-DECISION-PUBLICATION-RECORD-001.md`
(read it first, both EN and zh-CN; it is the spec for this task)
Baseline to beat: `cargo test --workspace --all-targets` → 385 passed / 0 failed /
10 ignored at `b29278a8`

## What you are implementing

Two things, in this order. Do not do anything else.

### Task 1 — D4: expose the durable `PreparedHidden` state

The state already exists on disk. It is not reachable through the port.

Add to `crates/memory-storage/src/lib.rs`:

```rust
/// The persisted publication state of one version, as recorded by
/// `prepare_version` / `publish_prepared`. Returns `None` when no preparation
/// row exists for that publication. Visibility semantics follow `read_current`:
/// absent or forgotten yields `Ok(None)`, non-intersecting scope yields
/// `ScopeMismatch`.
fn publication_state(
    &self,
    publication_id: &str,
    scope: &[ScopeRef],
) -> Result<Option<PublicationState>, StorageError>;
```

Add `pub enum PublicationState { PreparedHidden, Published, Suppressed }` in the
same crate, mirroring the `CHECK` constraint already present at
`crates/memory-storage-sqlite/src/lib.rs:111`.

Implement in `crates/memory-storage-sqlite/src/lib.rs` by reading
`publication_preparations` (table created at line 102), honouring the
`canonical_forget_fences` rules the same way `read_version_row` does. Do not add a
new table. Do not add a new column.

Implement in the test double `FakeStorage` inside `crates/memory-store/src/lib.rs`
(test module starts at line 120) so the trait stays implementable.

### Task 2 — D2/D3: a production `PublicationAuthority` that is an adapter, not a decider

Create the production implementation in `crates/memory-compiler/src/admission.rs`
(or a sibling module — not in `lib.rs`, keep `lib.rs` about the trait).

It must take: an `AdmissionStore` (or `&mut` to it), a `&dyn MemoryStorage`-shaped
access, and nothing else. It must report exactly what those records say:

| `PublicationProof` field | source | value |
|---|---|---|
| `publication_id` | `staged.publication_id` | echo |
| `generation` | `lease.generation` | echo |
| `producer_admitted` | `AdmissionStore::is_producer_registered` | its answer |
| `dependency_closure_complete` | `AdmissionStore::dependencies_complete` | its answer |
| `storage_prepared_hidden` | `MemoryStorage::publication_state` | `== Some(PreparedHidden)` |
| `canonical_commit_confirmed` | **none exists** | hardcode `false`, with a comment naming this ADR |
| `publication_participant_admitted` | **none exists** | hardcode `false`, same comment |
| `protected_visibility_authorized` | **none exists** | hardcode `false`, same comment |

**Hardcoding `false` with a comment is the requirement, not a shortcut.** Do not
infer, default or compute those three. `compiler-stage-contract.md` §8 says
"E MUST NOT implement substitute authorization decisions". The three test-only
authorities in `lib.rs` hardcode them to `true`; that is exactly what must not be
copied into production.

### Task 3 — wire it, so `compile()` is actually called

`crates/brain-cli/src/main.rs` must call the compiler stage through the adapter
instead of printing `COMPILER_SKIP_NOTICE`. Because of Task 2, the realistic result
is `Ok(Blocked)` — that is success for this task.

The notice text must name the blocking flag. Replace:

```
compiler stage skipped: PublicationAuthority has no production implementation
```

with a message that reports the actual disposition and, when it is `Blocked`, which
flag caused it. Keep writing `<output>.compiler-status`. Keep the exit status
unchanged. The existing test `crates/brain-cli/tests/compiler_skip_is_visible.rs`
pins the old text — update it, do not delete it.

## Hard constraints

- **Do not** set any of the three unsourced flags to `true`, anywhere, including in
  tests where it would look harmless. If a test needs a `Published` outcome it must
  construct a fake `PublicationAuthority` in that test, not change the adapter.
- **Do not** mark `forgotten_memory_is_excluded_from_context` as fixed. It reads
  as green today because its body is four comment lines and no assertion. Leave it
  `#[ignore]`d and leave it empty; changing it is a separate item (GAP-11).
- **Do not** add `#[allow(...)]`, remove any existing test, or edit
  `14-ai-development/work-items/GAP-*.md`.
- Bilingual: any new doc gets an EN file and a `.zh-CN.md` neighbour in the same
  change set. Code comments are English only.
- No new dependency in any `Cargo.toml` without naming why in the commit message.

## Acceptance — report the actual command output, not a summary

```
cargo test --workspace --all-targets       # must end 0 failed
cargo clippy --workspace --all-targets     # must be clean
cargo fmt --check                          # must be clean
```

Baseline is 385 passed / 0 failed / 10 ignored. New tests are expected; a *drop* in
the passing count means you removed or broke something. The ignored count must stay
at 10 unless you can name exactly which ignored test you enabled and why.

Then run the binary end to end and paste the output:

```
cargo run -q -p brain-cli -- compile --input <a valid input.json> --out /tmp/o.json
cat /tmp/o.json.compiler-status
```

State explicitly which of the eight flags is `false` on your run and which line of
the ADR authorizes that.

## What NOT to claim

Do not claim GAP-07 is closed. Do not claim `Published` is reachable. Do not claim
the three unsourced flags are "temporarily true". The correct outcome is a
`Blocked` disposition with a named cause, which is strictly better than a skip and
strictly worse than a publication.
