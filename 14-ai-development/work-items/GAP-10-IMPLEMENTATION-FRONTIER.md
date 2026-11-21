# GAP-10 — Implementation frontier: what actually blocks each domain

**Status:** Open — this is a map, not a defect
**Area:** cross-domain
**Purpose:** replace six unmeasured completion percentages with a dependency-ordered frontier

## Why this document exists

A request to "advance the key missing work" listed six domains with
completion estimates: Memory Compiler 85% unimplemented, Memory Context 80%,
Agent Integration 90%, BMCP 60%, Phase 2 domain 100% not started, E2E 100% not
started.

Measured against the repository, three of those six are materially wrong, and
the six are not parallel. They form a chain: most remaining work is blocked by
two upstream authorities (D publication, H transport freeze), so dispatching
"more implementation" to all six at once would produce work that cannot be
merged.

This document replaces the percentages with counts, and orders the work by what
is actually unblocked.

## 1. Measured state (verified on `main @ 76b6470e`)

### 1.1 Production code has zero stubs

```sh
grep -rn "todo!\|unimplemented!" --include=*.rs crates/
```

All 8 hits are in `crates/memory-domain/tests/phase2_acceptance.rs`, inside
`#[ignore]`d test bodies at lines 154, 162, 191, 257, 332, 340, 403, 411.

There is no half-written production code anywhere in the workspace. "Not
implemented" here means **a specified concern with no code at all**, not an
incomplete function. That distinction matters: it means the next increment is
always "write the first version of X", never "finish X".

### 1.2 Phase 2 domain model is largely implemented, not 0%

The claim "Phase 2/3 domain model: 100% not started" is false for Phase 2. The
types exist and are tested:

```sh
grep -n "pub struct Fact\b\|pub struct FactRevision\|pub enum EntityIdentityStatus\|pub struct RelationDefinition\|pub struct EvidenceExtension\|pub struct ClaimRevision" crates/memory-domain/src/lib.rs
```

```
365: pub struct ClaimRevisionRef(OpaqueId);
369: pub struct FactRevisionRef(OpaqueId);
435: pub struct ClaimRevision {
504: pub struct Fact { fact_ref: FactRef, initial_revision: Box<FactRevision> }
522: pub struct FactRevision {
605: pub enum EntityIdentityStatus { Provisional, Resolved, Merged, Split, Retired }
664: pub struct RelationDefinition { pub relation_type: String, ... }
686: pub struct EvidenceExtension {
```

`crates/memory-domain` runs 36 unit tests plus 11 acceptance tests, of which 9
are `#[ignore]`d with a named missing API each (no `ClaimRevisionRegistry`, no
`classify_claim_change`, no `RelationTypeRegistry`, no `ProvenanceGraph`, etc.).

So Phase 2 is roughly "types and invariants done, registries and classifiers
absent". Phase 3 is a different question and is not addressed here.

### 1.3 Memory Context has a measured 77-row coverage map

`06-memory-context/context-implementation-coverage.md` already classifies every
concern. Its most recent round states **25 NOT IMPLEMENTED / 43 PARTIAL /
9 IMPLEMENTED** over 77 rows.

Critically, each row names the responsible party. Counting the attribution
column:

| attribution | rows |
|---|---|
| `D` (publication authority) | 40 |
| `本线程可做` (implementable locally now) | 19 |
| `不在范围` (out of scope) | 10 |
| `I` (authorization authority) | 8 |

"80% unimplemented" is therefore not actionable, but **19 locally-implementable
rows are**, and 40 rows are waiting on D. That is the real shape of the gap.

### 1.4 There is no network transport anywhere

```sh
grep -rn "TcpListener\|hyper\|axum\|transport" --include=*.rs crates/
```

No matches outside doc comments that explicitly disclaim transport
(`agent-integration/src/lib.rs:3` "does not perform ... network transport",
`memory-context/src/lib.rs:3` "deliberately stops before persistence and
transport").

The only binary in the workspace is `crates/brain-cli/src/main.rs`.

So "BMCP complete protocol stack 60% unimplemented" is the wrong frame. The
protocol **artifacts** are substantial: 32 JSON schemas, 5 Python validators,
a conformance suite of 545 passing tests, plus `bmcp-protocol` in Rust
(1372 lines: `evidence`, `strict_json`, `validate`, `digest`,
`parse_and_validate`). What does not exist is the **transport and server** — and
that is one thing, not 60% of a stack.

### 1.5 Agent Integration is blocked, not neglected

`07-agent-integration/agent-integration-architecture-completion.md` §8.3 lists a
7-step integration sequence and states plainly that steps 3–6 are not available
as a callable path. §9 lists RT-01..RT-09 acceptance scenarios, all marked
NOT RUN or BLOCKED / DEPENDENCY_NOT_FROZEN.

The blocker is explicit: D publication/dependency/final gate, I authorization,
and H BMCP transport/ACK. Agent Integration cannot be implemented ahead of
those without inventing contracts.

## 2. The dependency chain

```
Phase 2 domain types            DONE (registries/classifiers missing)
        |
        v
memory-storage / memory-store   DONE incl. hidden prepare / explicit publish (#523)
        |
        v
memory-context                 77-row map: 9 done, 43 partial, 25 absent
        |                      19 rows implementable locally
        v
PublicationAuthority  <-- THE CHOKEPOINT. 3 impls exist, all #[cfg(test)]
        |
        +--> memory-compiler::compile reachable
        +--> 40 of the 25+43 context rows unblocked
        +--> Agent Integration steps 3-6 unblocked
        |
        v
BMCP transport + server   <-- does not exist; also gates Agent Integration
        |
        v
End-to-end (brain-cli beyond context assembly)
```

**The chokepoint is `PublicationAuthority` (GAP-07).** It is a single trait
with a single missing production implementation. Everything above it in the
chain is either done or locally implementable; everything below it is blocked.

This is why "advance all six domains" cannot work as stated. Five of the six
converge on one missing trait implementation plus one missing transport.

## 3. What is actually unblocked right now

In dependency order. Each item is dispatchable today with no external decision.

### Tier 1 — unblocks the most downstream work

**T1.1 — A production `PublicationAuthority` (GAP-07, direction (a))**

`prepare_version` / `publish_prepared` already exist on the Storage trait and in
`memory-storage-sqlite` (#523). What is missing:

- `MemoryStore` does not surface them (it exposes 5 methods, none of them
  prepare/publish; the only bodies are on `FakeStorage` inside `cfg(test)`).
- No durable publication record outside the compiler's in-memory admission
  store.

Implementing this makes `MemoryCompiler::compile` reachable, which is the
prerequisite for any claim that the system compiles.

**T1.2 — 19 locally-implementable Memory Context rows**

Enumerated in the coverage map with `本线程可做`. Notable ones:
candidate-set marginal-coverage optimizer, budget/sufficiency observability,
delivery attempt ledger, Compact operation with lineage-safe output.

These need no external authority and are independently testable.

### Tier 2 — unblocked but narrower

**T2.1 — Phase 2 registries and classifiers**

The 9 `#[ignore]`d acceptance tests each name the missing API. Implementing
`ClaimRevisionRegistry`, `classify_claim_change` (CI-01..CI-13),
`RelationTypeRegistry`, `ProvenanceGraph` and `EvidenceIndependence::validate`
would convert 9 ignored tests into real ones and complete DM2-01..DM2-14.

**T2.2 — CI wiring for the existing gates**

GAP-08 and GAP-09 both reached `main` red because only `rust-phase1.yml` runs on
PRs. Wiring the schema audit, the protocol index check and the conformance suite
into CI is small and prevents recurrence. It does not add capability but it
stops the measurement from being the only detector.

### Tier 3 — blocked, must not be dispatched as implementation

| work | blocked by | what would unblock it |
|---|---|---|
| BMCP transport/server | H has not frozen the transport contract | H decision |
| Agent Integration RT-01..RT-09 | same, plus D and I gates | H + D + I |
| 40 context rows attributed `D` | publication authority | T1.1 |
| 8 context rows attributed `I` | authorization authority | I decision |

Dispatching implementation for these produces unmergeable work. They need
decisions, not code.

## 4. Recommendation

**Do T1.1 first, then T1.2, then T2.1/T2.2.** Do not dispatch Tier 3 as
implementation.

The reason to start with T1.1 rather than the larger T1.2 is that T1.1 is one
trait implementation that unblocks 40 attributed-`D` rows plus the compiler plus
Agent Integration steps 3–6. T1.2's 19 rows are each small and independent; they
can run in parallel with T1.1 and should.

If T1.1 is genuinely blocked on a decision nobody has made — namely *what is the
durable publication record* — then that decision is the highest-value thing to
settle, because it is the single gate in front of the largest block of work.

## 5. Correction to the stated estimates

| domain | stated | measured |
|---|---|---|
| Memory Compiler | 85% unimplemented | ~100% of `compile` unreachable; admission/registry/fence implemented and tested (58 tests). Missing: production authority, Store-level prepare/publish exposure |
| Memory Context | 80% unimplemented | 77-row map: 9 implemented / 43 partial / 25 absent. 19 rows locally doable, 40 waiting on D |
| Agent Integration | 90% unimplemented | Accurate for runtime; but blocked by H/D/I, not by absence of effort. RT-01..RT-09 all NOT RUN |
| BMCP | 60% unimplemented | Artifacts substantial (32 schemas, 545 conformance tests). Transport/server entirely absent — a binary, not a percentage |
| Phase 2 domain | 100% not started | **False.** Types + invariants implemented, 36 unit + 11 acceptance tests; 9 ignored for named missing registries |
| E2E | 100% not started | Partially false. `brain-cli` runs ingestion → storage → context end to end. It stops at the compiler skip (GAP-07) |

## 6. Re-measurement at `b29278a8` (2026-11-22 02:05 +08:00)

This section is additive. It does not edit §1-§5 above; it records what changed
after those sections were written, and one figure that does not reconcile.

### 6.1 Test totals changed

```
$ cargo test --workspace --all-targets
TOTAL passed=385 failed=0 ignored=10
```

Per crate, measured separately:

| crate | passing |
|---|---|
| agent-integration | 33 |
| bmcp-protocol | 46 |
| brain-cli | 5 |
| memory-compiler | 59 |
| memory-context | 77 |
| memory-domain | 47 |
| memory-event-store | 2 |
| memory-event-store-sqlite | 31 |
| memory-storage | 3 |
| memory-storage-sqlite | 59 |
| memory-store | 23 |

### 6.2 One figure does not reconcile, and is recorded unresolved

Another document in this directory records **371 passed at `1ebbab84`**. I measure
**385 at `b29278a8`**. #541's own diff adds 19 `#[test]` attributes, and
371 + 19 = 390 ≠ 385. So the two figures count different target sets, or one of
them is wrong. This is not explained away here; it is flagged so the next person
re-derives rather than inherits.

### 6.3 The dependency graph gained one consumer link, and lost none

Measured from `crates/*/Cargo.toml`:

```
agent-integration          -> memory-context, memory-domain
bmcp-protocol              -> NONE
brain-cli                  -> memory-domain, memory-storage-sqlite, memory-store,
                              memory-context, memory-compiler
memory-compiler            -> memory-domain, memory-event-store, memory-event-store-sqlite
memory-context             -> memory-domain, memory-event-store-sqlite, memory-store,
                              memory-storage, memory-storage-sqlite
memory-domain              -> NONE
memory-event-store         -> memory-domain
memory-event-store-sqlite  -> memory-domain, memory-event-store
memory-storage             -> memory-domain
memory-storage-sqlite      -> memory-domain, memory-storage
memory-store               -> memory-domain, memory-storage, memory-storage-sqlite

used by NOBODY:  agent-integration, bmcp-protocol
only binary:     brain-cli
```

§1.5 and §2 above remain correct: `brain-cli` still imports neither
`agent-integration` nor `bmcp-protocol`.

### 6.4 Tier 1 item 2 changed shape

GAP-06 was not closed by #541. #541 added a *target*-keyed fence
(`canonical_forget_fences`, keyed by Memory/Version) alongside the pre-existing
*namespace*-keyed fence (`forget_fence`, keyed by `namespace_key`), in a different
crate, with no reconciliation. `forget_api_absence_is_detectable` still passes —
which is the defect it was written to detect. See
`GAP-11-FORGET-FENCE-SPLIT-AUTHORITY.md` for the measurements and the closure
criteria. Tier 1 item 2 is therefore not "wire the fence in"; it is "decide which
fence is canonical, then delete the other".

### 6.5 The gates are unchanged, and one of them is now measurable

- `08-bmcp-protocol/scripts/check_protocol_index.py` → `missing=0 extra=0
  duplicate_types=0 invalid_rows=0 PASS`.
- `08-bmcp-protocol/schemas/test_nonempty_audit.py` → **exit 1**, 5506 lines of
  unregistered constraints (GAP-09, unchanged).
- `python3 -m unittest discover -s tests/conformance` → **Ran 493 tests**,
  6 errors, 27 skipped. The 6 errors are all
  `ModuleNotFoundError: No module named 'rfc8785'`, i.e. an uninstalled declared
  dependency (`requirements.txt` pins `rfc8785==0.1.4`), not a code defect.
  Before #540 this command found 0 tests and died on ImportError.
- #546 declared the Node dependency that GAP-08 reported; worth re-checking
  whether the three `.mjs` references now resolve on a clean checkout.

### 6.6 CI still evaluates nothing

All four check runs on both the #541 head commit and on `main` carry the same
annotation, verbatim:

> The job was not started because recent account payments have failed or your
> spending limit needs to be increased.

`GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` →

```
403 — Upgrade to GitHub Pro or make this repository public to enable this feature.
```

Every green in this document is a local measurement. Nothing here was checked by
a workflow.
