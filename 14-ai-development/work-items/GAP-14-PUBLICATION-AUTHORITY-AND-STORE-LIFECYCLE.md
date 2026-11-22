# GAP-14 — Production publication authority and MemoryStore publication lifecycle

**Status:** Open — A open, B blocked on D3, C unverified
**Area:** memory-store / memory-compiler / memory-storage-sqlite
**Owner track:** Owner D (Publication) + Owner I (Authorization)
**Split from:** GAP-07, closed 2026-11-22 for production reachability only
**Measured at:** `main @ 87d503ba`

## Why this exists as three items, not one

GAP-07 asked a single question — *can the compiler be called from production?* — and the answer is now yes. That closure deliberately did not absorb three other questions that had been sitting inside it, because collapsing them made all of them unanswerable at once:

- Can the publication lifecycle be reached through the facade the CLI actually uses? (**A**)
- Can any of the three authorization flags ever become true? (**B**)
- Does the publication record survive a process restart? (**C**)

They have different owners, different blockers and different evidence requirements. A single "publication is incomplete" row would hide that B is a decision nobody has made while A is a few forwarders.

## GAP-14-A — `MemoryStore` does not surface the publication lifecycle

**Status:** OPEN — no external decision required

`crates/memory-store/src/lib.rs` (1175 lines) exposes ten `pub fn`:

```
new, into_storage, create_memory, read_current, read_memory,
read_revision, write_revision, resolve_idempotency,
forget_memory, forget_version
```

`prepare_version`, `publish_prepared` and `publication_state` appear in that file only on `FakeStorage`, inside the `#[cfg(test)]` module:

```
:317  fn publication_state       (FakeStorage)
:426  fn prepare_version         (FakeStorage)
:524  fn publish_prepared        (FakeStorage)
```

The real implementations are one layer below, in `crates/memory-storage-sqlite/src/lib.rs`:

```
:388  fn publication_state
:606  fn prepare_version
:822  fn publish_prepared
```

So the primitive exists where nothing can reach it, and the layer that could reach it does not expose it. This is the same shape as the original GAP-07 defect, one level down.

**Why it is not simply three forwarders.** Each of the three carries a contract, not just a signature:

1. `PrepareRequest` / `PreparedCommitReceipt` — what "staged but not readable" means, and which fields must be preserved.
2. `publish_prepared(publication_id, expected_current_version, scope)` — the `expected_current_version` argument is a concurrency fence, not a hint; passing it wrong converts a stale-version conflict into a silent overwrite.
3. `publication_state` — whether its answer is authoritative for a caller outside the storage layer, or only a local observation.

**Closure criteria**

1. The three methods exist on `MemoryStore<S: MemoryStorage>` with the same semantics as the trait, including `validate_scope` on every call.
2. At least one test drives `prepare_version` → `publication_state == PreparedHidden` → `publish_prepared` through `MemoryStore` against real SQLite, not `FakeStorage`.
3. A test proves a stale `expected_current_version` is rejected rather than silently accepted through the facade.
4. No new abstraction is introduced: no second trait, no builder, no policy object. Three methods and their tests.

**Do not implement ahead of GAP-14-B.** Exposing `publish_prepared` on the facade while no authority can legitimately authorize a publication produces an API that is callable but has no complete authorization contract — exactly the unreachable-abstraction class GAP-07 warned about. The 2026-11-22 ruling ordered B before A for this reason.

## GAP-14-B — Three publication flags have no authoritative issuer

**Status:** BLOCKED — requires the D3 decision

`PublicationProof` carries eight flags. `brain-cli` reports the false ones in gate order:

```
canonical_commit_confirmed
publication_participant_admitted
protected_visibility_authorized
```

Measured on `main @ 87d503ba`, all three are false on every real run, so the disposition is always `Blocked`:

```
$ brain compile --input crates/brain-cli/fixtures/event.json --out /tmp/o.json
compiler stage blocked: publication not authorized; blocking flag: canonical_commit_confirmed;
false flags: [canonical_commit_confirmed, publication_participant_admitted, protected_visibility_authorized]
```

`OWNER-DECISION-PUBLICATION-RECORD-001` D3 records that these three have no authoritative issuer. The code is honest about it — `crates/brain-cli/src/main.rs:111` states in a doc comment that `Blocked` is the expected outcome of a real run — but the consequence is that the `Published` disposition is currently unreachable in production.

**What is required to close this**

Not code. Three answers:

1. Who signs `canonical_commit_confirmed`, and against what durable record?
2. Who admits a publication participant, and by what criterion?
3. Who authorizes protected visibility, and can that authority be delegated?

**Explicitly rejected:** adding `authorized: bool` to any request, deriving a flag from local state, or letting a test authority satisfy the gate in a production build. Each of those converts an unanswered governance question into a false claim of authorization.

## GAP-14-C — Publication-record durability is unverified

**Status:** UNVERIFIED — must not be marked resolved without evidence

`crates/brain-cli/src/main.rs:244` opens the admission ledger by path:

```rust
let authority_admission = AdmissionStore::open(request.admission_path)
```

That line proves a file path is opened. It does **not** prove:

- that the publication record is persisted in a form that survives process exit;
- that reopening the same path recovers the same record;
- that a recovered record is authoritative in the sense D3 requires;
- that a recovered record can confirm a canonical commit.

None of these has been tested. An earlier draft of this assessment was prepared to call durability "probably resolved" on the strength of the file-path argument alone; that inference is not supported and is recorded here as the reason the item stays open.

**Closure criteria**

1. A test writes a publication record, exits the process, reopens the same path in a new process, and reads the same record back.
2. A test proves a record that was prepared but never published is still distinguishable from a published one after restart.
3. The test runs against the real on-disk store, not an in-memory handle.

## Ordering

```
GAP-14-B  (decision — who signs the three flags)
    |
    v
GAP-14-A  (facade — three methods designed against the settled contract)
    |
    v
GAP-14-C  (durability — recovery verified against the real store)
    |
    v
re-evaluate whether Published is reachable in production
```

Doing A first would produce a callable publication API with no authority behind it. Doing C first would verify recovery of a record whose authority is undefined. B is first because it is the only one that is a decision rather than work.

## What this item is not

- Not a defect report against #552. That PR did what it claimed: it made the compiler reachable and honest about refusal.
- Not a claim that publication is broken. It is not broken; it is unauthorized by design, pending D3.
- Not a re-litigation of D3. This item records the consequence of D3, not an argument against it.
