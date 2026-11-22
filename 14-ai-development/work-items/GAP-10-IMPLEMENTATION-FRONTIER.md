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

## 1. Measured state (verified on `main @ caa37a7`)

> **Revision note.** An earlier version of this section measured `main @ 76b6470e`
> and concluded that `PublicationAuthority` had three implementations, all
> `#[cfg(test)]`, and was therefore "THE CHOKEPOINT". That is no longer true.
> `main` advanced through #523, #545, #555 and #570 in a single day. Section 2
> has been rewritten accordingly; the chokepoint is closed.

### 1.1 Production code has zero stubs

```sh
grep -rn "todo!\|unimplemented!" --include=*.rs crates/
```

All 3 hits are in `crates/memory-domain/tests/phase2_acceptance.rs`, inside
`#[ignore]`d test bodies at lines 607, 872, 880.

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

`crates/memory-domain` runs 36 unit tests plus 20 acceptance tests, of which 3
are `#[ignore]`d. Nine of those twenty were closed on `main` by #570 (three
registries/resolver plus the `dm2_03` vectors) and #574 (`RelationTypeRegistry`,
`scope_refs`).

So Phase 2 is now "types and invariants done; three concerns deliberately left
open". The remaining three all need a decision, not code:

| test | reason it stays ignored | what would close it |
|---|---|---|
| `dm2_06` | cross-owner decision `B-P2-XO-01` (§8 PENDING, §9 `PLACEHOLDER ONLY`) | an owner decision |
| `dm2_11` | Provenance DAG is `NOT TYPED` (§9) | a spec decision |
| `dm2_12` | same | a spec decision |

None of the three can be closed by writing code. `dm2_11`/`dm2_12`
need `phase-2-domain-extension.md` §9 to type the DAG and §7 to settle
cycle/compaction policy; `dm2_06` needs `B-P2-XO-01` resolved, and §8 forbids
inferring authorization. The two that were ordinary implementation work
(`dm2_08`, `dm2_09`) were closed by #574.

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
Phase 2 domain types            DONE (3 ignores left, all decision-blocked)
        |
        v
memory-storage / memory-store   DONE incl. hidden prepare / explicit publish (#523)
        |
        v
memory-context                 77-row map: 9 done, 43 partial, 25 absent
        |                      19 rows implementable locally
        v
PublicationAuthority            DONE. AdmissionPublicationAuthority is production
        |                       code, reads the durable ledger, and brain-cli uses it.
        +--> memory-compiler::compile reachable  <-- brain-cli calls it
        +--> 40 of the 25+43 context rows unblocked
        +--> Agent Integration steps 3-6 unblocked
        |
        v
BMCP transport + server   <-- does not exist; now the only remaining chokepoint
        |
        v
End-to-end (brain-cli beyond context assembly)
```

**`PublicationAuthority` is no longer the chokepoint.** As of `main @ caa37a7`
there are two production implementations:

| impl | location | backing |
|---|---|---|
| `AdmissionPublicationAuthority` | `publication_authority.rs:50` | durable admission ledger + storage prepare row |
| `EvidenceAuthority`, `TestAuthority`, `RecoveryAuthority` | `lib.rs:921/940/1355` | `#[cfg(test)] mod tests` |

`AdmissionPublicationAuthority` is not a test double. It takes an
`AdmissionStore` and a `&dyn MemoryStorage`, reads committed rows only, and
derives producer identity and scope from the durable admission request rather
than from a caller-supplied boolean. `crates/brain-cli/src/main.rs:280`
constructs a `MemoryCompiler` with it and calls `compile`, then reports
`published` / `blocked` / `suppressed` on stderr unconditionally. GAP-07 (b) —
"skip is invisible" — was closed with a sidecar file plus a binary-level test at
`crates/brain-cli/tests/compiler_skip_is_visible.rs`.

**The only remaining chokepoint is BMCP transport + server.** It gates Agent
Integration and the end-to-end path, and nothing above it does.

This is why "advance all six domains" cannot work as stated: five of the six
converge on one missing transport. The earlier reading — that they converge on a
missing trait implementation *plus* a missing transport — was true at
`76b6470e` and is now half resolved.

## 3. What is actually unblocked right now

In dependency order. Each item is dispatchable today with no external decision.

> **Partly superseded.** T1.1 below was completed by `AdmissionPublicationAuthority`
> and the `brain-cli` wiring. See §2 and §7.3. T1.2 and T2.2 are still open;
> T2.1 is down to `dm2_08`/`dm2_09` (PR #574) plus three items that need
> decisions, not code.

### Tier 1 — unblocks the most downstream work

**T1.1 — A production `PublicationAuthority` (GAP-07, direction (a)) — DONE**

Closed by `AdmissionPublicationAuthority`. It takes an `AdmissionStore` plus a
`&dyn MemoryStorage`, reads committed rows only, and derives producer identity
and scope from the durable admission request rather than from a caller-supplied
boolean. `crates/brain-cli/src/main.rs:280` constructs `MemoryCompiler` with it
and calls `compile`, reporting `published` / `blocked` / `suppressed` to stderr
unconditionally, with a sidecar file and a binary-level test
(`compiler_skip_is_visible.rs`) so the skip cannot go unseen.

`MemoryStore` still does not surface `prepare_version` / `publish_prepared`.
That is no longer a blocker for `compile` — the authority reads storage
directly — but it remains a hole in the Store abstraction, and the honest
description is "the chokepoint was routed around", not "the abstraction was
completed".

**T1.2 — 19 locally-implementable Memory Context rows**

Enumerated in the coverage map with `本线程可做`. Notable ones:
candidate-set marginal-coverage optimizer, budget/sufficiency observability,
delivery attempt ledger, Compact operation with lineage-safe output.

These need no external authority and are independently testable.

### Tier 2 — unblocked but narrower

**T2.1 — Phase 2 registries and remaining graph capabilities**

The Claim identity classifier is already implemented by PR #545 as
`claim_identity::classify`; the public function is named `classify`, not
`classify_claim_change`. This work item makes `dm2_03` a real acceptance
test using `ClaimRevision::initial` / `successor` and covers the 10 reachable
vectors: CI-01..CI-04, CI-07..CI-11 and CI-13. CI-05, CI-06 and CI-12 are
unreachable because `ClaimRevision` has no quantifier, modality or confidence
field; they are explicitly not counted as covered.

The remaining ignored acceptance tests are all decision-blocked, none of them
implementation work:

| test | closure requires |
|---|---|
| `dm2_06` | owner decision `B-P2-XO-01`; §8 forbids inferring authorization |
| `dm2_11`, `dm2_12` | spec decision — §9 marks Provenance DAG `NOT TYPED`, §7 leaves cycle policy open |

`ClaimRevisionRegistry`, `AcceptedRevisionState` and `ClaimRevisionResolver`
landed in #570; `RelationTypeRegistry` and `scope_refs` landed in #574.
`EvidenceIndependence::validate` is not a named blocker in any current ignore
reason.

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
| 40 context rows attributed `D` | ~~publication authority~~ publication **record** shape | `AdmissionPublicationAuthority` unblocked `compile`; the 40 rows still need a durable publication record surfaced through `MemoryStore` |
| 8 context rows attributed `I` | authorization authority | I decision |
| `dm2_06` | cross-owner decision `B-P2-XO-01` | owner decision |
| `dm2_11`, `dm2_12` | Provenance DAG `NOT TYPED` (§9) | spec decision |

Dispatching implementation for these produces unmergeable work. They need
decisions, not code.

## 4. Recommendation

**T1.1 is done. Do T1.2 next, then T2.2, then the decision items.**

T1.2's 19 rows are each small and independent, need no external authority, and
are the only remaining block of work that is both substantial and dispatchable
today. T2.2 (CI wiring) adds no capability but stops the measurement from being
the only detector — worth doing early precisely because it is cheap.

The four items in Tier 3 that need decisions should be escalated as decisions.
Dispatching them as implementation is what produced #573: a PR that
re-implemented work #570 had already landed, because nobody had re-measured
`main` before writing code.

## 5. Correction to the stated estimates

| domain | stated | measured |
|---|---|---|
| Memory Compiler | 85% unimplemented | `compile` is now reachable via `AdmissionPublicationAuthority` and `brain-cli`. Admission/registry/fence implemented and tested. Remaining: `MemoryStore` does not surface prepare/publish |
| Memory Context | 80% unimplemented | 77-row map: 9 implemented / 43 partial / 25 absent. 19 rows locally doable, 40 waiting on a durable publication record |
| Agent Integration | 90% unimplemented | Accurate for runtime; but blocked by H/D/I, not by absence of effort. RT-01..RT-09 all NOT RUN |
| BMCP | 60% unimplemented | Artifacts substantial (32 schemas, 545 conformance tests). Transport/server entirely absent — a binary, not a percentage |
| Phase 2 domain | 100% not started | **False.** Types, invariants, `claim_identity::classify`, `ClaimRevisionRegistry`, `AcceptedRevisionState` and `ClaimRevisionResolver` are all implemented. 3 ignores left, all decision-blocked (§1.2) |
| E2E | 100% not started | **False.** `brain-cli` runs ingestion → storage → context → compiler end to end, including the publication gate and its visible skip |

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

## 7. Re-measurement at `dba34a35` (2026-11-22 03:05 +08:00)

Additive again. §1-§6 are untouched. Six things changed on main since `b29278a8`,
and one of them invalidates a `#[ignore]` reason rather than closing a gap.

### 7.1 Test totals moved, and the ignored count moved for the wrong reason

```
$ CC=zigcc AR=zigar cargo test --workspace --all-targets
binaries: 26
TOTAL passed=438 failed=0 ignored=9
```

§6.1 recorded 385 / 0 / 10 at `b29278a8`. The +53 passing is real work. The
10 → 9 ignored is **not** a converted test: see §7.2.

Per crate, from the same run:

| crate | unit | integration |
|---|---|---|
| agent-integration | 36 | 2 + 19 |
| bmcp-protocol | 42 | 4 |
| brain-cli | 1 | 4 |
| memory-compiler | 62 | 1 |
| memory-context | 68 | 8 + 1 |
| memory-domain | 55 | 11 (+9 ignored) |
| memory-event-store | 2 | — |
| memory-event-store-sqlite | 18 | 5 + 2 + 6 |
| memory-storage | 3 | — |
| memory-storage-sqlite | 60 | — |
| memory-store | 15 | 6 + 3 + 2 |

The `371 vs 385` discrepancy flagged in §6.2 is not resolved here either. What is
now certain is that the §6.1 table counted a different target set than this one:
`--all-targets` includes integration binaries, and the §6.1 numbers match the
`--lib`-only runs.

### 7.2 dm2_03 now exercises the implemented classifier

PR #545 (merge `444deef1`) added `crates/memory-domain/src/claim_identity.rs`
and publicly re-exported `claim_identity::classify`. That implementation is
not a missing API and is not changed by this work item.

The current `dm2_03_ci_classification_vectors` acceptance test is active, but
its earlier form used JSON mutation helpers and did not exercise the full
reachable CI set with the canonical constructors. This work item replaces those
vectors with real `ClaimRevision::initial` / `ClaimRevision::successor`
values and asserts CI-01, CI-02, CI-03, CI-04, CI-07, CI-08, CI-09, CI-10,
CI-11 and CI-13 (10/10 reachable dimensions).

CI-05, CI-06 and CI-12 are not fabricated as passing tests. The
`ClaimRevision` struct has no quantifier, modality or confidence field. The
source-shape check is:

```sh
sed -n '/^pub struct ClaimRevision {/,/^}/p' crates/memory-domain/src/lib.rs | grep -En '\\b(quantifier|modality|confidence)\\b'
```

Expected result: no output; `grep` exits 1 because none of those fields occurs
inside the struct. These three vectors are unreachable, not covered.

The classifier treats every qualifier change as
`QualifierSubstantivenessUnprovable`; this remains an explicit governed
decision, never a guessed `NewClaim` or `NewRevision`. The test also checks
that a normalized label-only subject change is `NewRevision/LabelOnly`.

### 7.3 GAP-07's gap statement is now false; its closure criteria are half met

> **Status correction (2026-11-22):** The quoted GAP-07 gap statement has been
> superseded by PR #552 and subsequent production integration.
> `AdmissionPublicationAuthority` now provides a production implementation, and
> `brain-cli` invokes `MemoryCompiler::compile()` through a non-test path. GAP-07
> is therefore **closed for production reachability** — all four of its closure
> criteria were verified at `main @ 87d503ba`. Publication success and durable
> publication authority remain unresolved and are tracked separately under
> `GAP-14-PUBLICATION-AUTHORITY-AND-STORE-LIFECYCLE.md` (A: facade does not
> surface prepare/publish; B: three flags have no issuer under D3; C: durability
> unverified). The text below is retained as the measurement that produced this
> correction.

§1.2 of GAP-07 says, verbatim, that `compile` has "no production implementation
of its required `PublicationAuthority` trait, and no non-test caller". Both
halves are now wrong:

```
$ grep -rn "impl.*PublicationAuthority for" --include=*.rs crates/
crates/memory-compiler/src/lib.rs:921:  impl PublicationAuthority for EvidenceAuthority      (cfg(test))
crates/memory-compiler/src/lib.rs:940:  impl PublicationAuthority for TestAuthority          (cfg(test))
crates/memory-compiler/src/lib.rs:1355: impl PublicationAuthority for RecoveryAuthority      (cfg(test))
crates/memory-compiler/src/publication_authority.rs:50:
        impl PublicationAuthority for AdmissionPublicationAuthority<'_>   (production)
```

`brain-cli/src/main.rs:4` imports `memory_compiler::publication_authority::AdmissionPublicationAuthority`,
constructs it at line 245, and `run_compiler_stage` calls `compiler.compile(...)`
at line 285. A real run:

```
$ brain compile --input fixtures/event.json --out ctx.json --verbose
compiler stage blocked: publication not authorized; blocking flag: canonical_commit_confirmed;
  false flags: [canonical_commit_confirmed, publication_participant_admitted,
                protected_visibility_authorized]
EXIT=0
```

Against GAP-07's own closure criteria:

1. **MET** — a production authority exists and a non-test path calls `compile`.
2. **MET** — `crates/brain-cli/tests/compiler_skip_is_visible.rs`, 4 tests, spawns
   the built binary and asserts the notice appears exactly once on stderr and in
   the sidecar, with exit code 0.
3. **MET** — the notice is unconditional, outside `--verbose`.
4. **Not met, and now the only thing standing** — GAP-07 still describes itself
   as open in the present tense while its subject no longer exists.

The three `false` flags are not a bug. `OWNER-DECISION-PUBLICATION-RECORD-001` D3
states the adapter "never computes, infers, defaults or substitutes a flag", and
`compiler-stage-contract.md` §8 states "E MUST NOT implement substitute
authorization decisions". Reporting `false` is the required behaviour when no
authoritative issuer exists. The run is therefore **correctly refusing to
publish**, which is a different outcome from "the stage did not run".

This is a documentation defect of the exact kind GAP-10 §5 was written to catch:
a stale statement about the present, inherited rather than re-derived.

### 7.4 The E2E claim moves from "false" to "true up to the publication gate"

§5 row for E2E says "`brain-cli` runs ingestion → storage → context end to end.
It stops at the compiler skip". The path now runs ingestion → extraction →
normalization → staging → `compile` → proof acquisition → refusal. That is one
more stage than §5 recorded, and the refusal is a real decision from a real
authority rather than a skip.

What is still absent is a **successful** publication. Nothing in the repository
can produce a `Published` disposition, because the three proof fields have no
issuer. No test asserts `PublicationDisposition::Published` from a non-test path.

### 7.5 The bilingual gate is contaminated by untracked build output

```
$ BASE_SHA=HEAD~1 HEAD_SHA=HEAD python scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 08-bmcp-protocol/.pytest_cache/README.md
::error::New bilingual gap outside frozen baseline: 08-bmcp-protocol/tests/conformance/.pytest_cache/README.md
EXIT=2
```

Both paths are untracked (`.gitignore` line 6 has `.pytest_cache/`), and
`current_bilingual_gaps()` walks `root.rglob("*.md")` on the filesystem rather
than `git ls-files`. So any local pytest run turns the gate red on files that
cannot exist in CI. Removing them:

```
bilingual baseline: 77 frozen, 0 new gaps
EXIT=1   (only the PR-body manifest error remains)
```

This is not a new gap. It is a **reproducibility defect**: the gate's answer
depends on untracked local state, so "the gate passes" is not a statement about
the commit.

### 7.6 The 77-gap baseline did not move, and its shape is now fully attributed

`current_bilingual_gaps()` returns 79 locally, 77 on a clean tree. The clean-tree
distribution:

| root | gaps | note |
|---|---:|---|
| `13-engineering-decisions` | 58 | 58 `.md` files, 0 `.en.md`, 0 `docs/en` mirror |
| `06-memory-context` | 10 | |
| `08-bmcp-protocol` | 6 | |
| `14-ai-development` | 4 | all `research/phase-0/SESSION-*.md` |
| `00-governance` | 1 | `reports/gov-doc-001-full-scan-2026-11-20.md` |

`13-engineering-decisions` is **100% of its own subtree** and 75% of the whole
baseline. `PAIR_EXEMPT_PREFIXES` covers `work-items/`, `prompts/`, `adr/` under
14 but nothing under 13, and `EMBEDDED_BILINGUAL_SOURCES` has 21 entries of which
**zero** are under 13. So the entire root is in the baseline because no shape the
gate accepts was ever created for it — the same mechanism GAP-10 §1 and register
015 established for the 77, now localised to one root.

`14-ai-development/governance-register/` is **not** in the baseline despite 31
`.md` files: 19 have `docs/en` + `docs/zh-CN` mirrors, and the 12 that do not are
side-by-side pairs (`README.md` + `README.en.md`, and the five `GOV-NC-2026-11-20-*`
pairs). `side_by_side_partner()` resolves all of them. This is the mechanism
working as designed, and it is the counter-example to §7.5: the register is
clean because its files are tracked and its pairs are real.

## 8. The whole workspace builds and tests green (2026-11-22 12:00 +08:00)

This section exists because §7 and the PR bodies that preceded it asserted
something that is not true on this host: that six crates cannot be built because
`libsqlite3-sys` (bundled) needs a C compiler and none exists here.

That was a **measurement error, not an environment limit.** A working C compiler
was already on the machine.

### 8.1 What was actually wrong

`gcc` at `~/.local/bin/gcc.exe` is a real MinGW-w64 GCC 14.2.0, but its `libexec`
tree is missing, so `cc1` cannot be spawned:

```
$ gcc t.c -o t.exe
gcc.exe: fatal error: cannot execute 'cc1': CreateProcess: No such file or directory
```

`gcc -print-search-dirs` still points at `~/.local/libexec/gcc/x86_64-w64-mingw32/14.2.0/`,
which does not exist. So `cc` is on `PATH`, reports a version, and fails on the
first translation unit — the worst possible failure shape, because a version
check says it works.

MSVC is genuinely absent (`link.exe` missing), which is why
`+stable-x86_64-pc-windows-msvc` fails too.

### 8.2 What was already installed

A complete Zig toolchain at
`%LOCALAPPDATA%/Temp/zigpkg/ziglang/zig.exe` (190 MB), plus a `zigcc.exe`
wrapper left over from an earlier probe at
`2026-11-18-13-49-20/_l0probe/zigcc.exe`. The wrapper spawns
`zig cc -fno-sanitize=all` and forwards arguments.

§7's own command line already used it:

```
$ CC=zigcc AR=zigar cargo test --workspace --all-targets
TOTAL passed=438 failed=0 ignored=9
```

So §7 recorded the working invocation and §7's own prose then claimed the
workspace could not be built. The two statements were never reconciled.

`zigar` did not exist; it was built from the same wrapper pattern:

```c
nv[n++] = "C:/Users/Administrator/AppData/Local/Temp/zigpkg/ziglang/zig.exe";
nv[n++] = "ar";
```

### 8.3 Measured result

```
$ CC=<zigcc> AR=<zigar> cargo test --workspace --all-targets --offline
TOTAL passed=476 failed=0 ignored=3
```

| crate | passed | ignored |
|---|---:|---:|
| agent-integration | 57 | 0 |
| bmcp-protocol | 48 | 0 |
| brain-cli | 6 | 0 |
| memory-compiler | 66 | 0 |
| memory-context | 91 | 0 |
| memory-domain | 77 | 3 |
| memory-event-store | 2 | 0 |
| memory-event-store-sqlite | 38 | 0 |
| memory-storage | 3 | 0 |
| memory-storage-sqlite | 62 | 0 |
| memory-store | 26 | 0 |
| **total** | **476** | **3** |

The 3 ignored are `dm2_06`, `dm2_11`, `dm2_12` — the decision-blocked ones from
§1.2. Every other test in the workspace runs.

Also green:

```
cargo clippy --workspace --all-targets -- -D warnings   # clean
cargo fmt --all -- --check                              # clean
```

### 8.4 Why this matters beyond a number

Three PRs (#573, #574, #581) were scoped down to `memory-domain` and their bodies
told the reviewer that six crates could not be built here. That disclaimer was
false, and it made the PRs look smaller and less verifiable than they were. The
correct framing was always available: the whole workspace builds, and every
claim about `memory-compiler` or `brain-cli` can be checked locally.

The lesson is specific and worth recording: **a compiler that reports a version
but cannot compile is worse than no compiler**, because every "is it installed?"
check passes. The check that would have caught it is one translation unit, not
`--version`.

### 8.5 What this does not change

Nothing above §8 is invalidated. The chokepoint analysis in §2, the attribution
counts in §1.3, and the decision-blocked items in §1.2 all stand. What changes is
the claim that the workspace is unbuildable here — that claim was wrong, and it
is the reason several PRs were under-verified.

The environment fix is not in the repository: `CC`/`AR` are passed per
invocation, and no toolchain is vendored. A future contributor still hits the
broken `gcc` unless they know to override it. Recording the working invocation
in this section is the only durable artifact.


## 9. Re-measurement at `d89fd5fa8` (2026-11-22 12:30 +08:00)

Additive again. §1-§8 untouched. This section exists because the six percentages
in the original request were re-stated a fourth time, and because §8's own
numbers were already stale when they landed.

Observed at `2026-11-22T04:29:28Z`, tree `d89fd5fa8`.

### 9.1 The whole workspace is green, and the ignored count is down to one

```
$ CC=<zigcc> AR=<zigar> cargo test --workspace --all-targets --offline
TOTAL passed=503 failed=0 ignored=1
$ cargo clippy --workspace --all-targets -- -D warnings   # clean
$ cargo fmt --all -- --check                              # clean
```

§8.3 recorded `476 / 0 / 3` at `0ae644f32`. Between that commit and this one,
`fe9e25a5c` landed `ProvenanceGraph` and evidence independence, which closed
`dm2_11` and `dm2_12`.

The single remaining ignore is `dm2_06_missing_authorization_ref_blocks_fact_publication`.
Its reason is not a missing API: `FactRevision::initial` *requires* an
`AuthorizationDecisionRef`, and the only public constructor is
`AuthorizationDecisionRef::pending_i()`. Proving that a missing authorization is
rejected needs a type state that distinguishes absent from I-issued, and §8 of
`phase-2-domain-extension.md` forbids inferring authorization. So this one is
decision-blocked, not code-blocked — the same category §1.2 put it in, now the
only member of that category.

### 9.2 Four of the six stated percentages are now measurably wrong

| domain | stated | measured at `d89fd5fa8` |
|---|---|---|
| Memory Compiler | 85% unimplemented | `compile` is reachable from `brain-cli` through a production `AdmissionPublicationAuthority`. 66 tests. Five stages all have entry points. `Published` remains unreachable for three named reasons (GAP-12/13/14), none of which is "the compiler is 85% unwritten". |
| Memory Context | 80% unimplemented | 77-row map unchanged in counts (9 implemented / 42 partial / 26 absent) but the crate now runs **82 unit + 17 integration = 99 tests**, up from 68+9. The coverage map has not been re-attributed since the code moved; treat the row counts as stale, not the tests. |
| Agent Integration | 90% unimplemented | **False.** The crate now depends on `memory-context` *and* `memory-domain` at runtime, `brain-cli` consumes it (`crates/brain-cli/Cargo.toml:13`), and it runs 36 unit + 21 integration tests including `context_snapshot_delivery.rs`, which crosses the crate boundary with a real `ContextSnapshot`. #525's premise is dead. |
| BMCP | 60% unimplemented | Protocol artifacts substantial; `bmcp-protocol` is 44 unit + 4 conformance tests. Transport/server still absent — a binary, not a percentage. Unchanged from §1.4. |
| Phase 2 domain | 100% not started | **False.** 70 unit + 20 acceptance tests, 1 ignore (`dm2_06`), decision-blocked. `ClaimRevisionRegistry`, `ClaimRevisionResolver`, `AcceptedRevisionState`, `RelationTypeRegistry`, `ProvenanceGraph`, `EvidenceIndependence` and `claim_identity::classify` are all implemented. |
| E2E | 100% not started | **False.** `brain-cli` runs ingestion → extraction → normalization → staging → `compile` → proof → context assembly → adapter delivery. `crates/brain-cli/tests/e2e_full_chain.rs` asserts the whole chain including the persisted snapshot and the refusal notice. One test, 3.6 s, passes. |

The pattern worth naming: **each of these six numbers was true at some earlier
commit.** They are not lies, they are fossils. Re-stating them without
re-measuring is what makes them wrong.

### 9.3 What is genuinely absent, and it is three things

Everything above is code that exists. The set of specified work with no
implementation at all is now:

1. **A successful `Published` disposition.** Blocked by three issuer-less proof
   fields, each tracked: GAP-12 (canonical commit), GAP-13 (participant
   admission, external and tripartite), GAP-14 (store lifecycle plus the other
   two).
2. **BMCP transport and server.** No `TcpListener`, no `hyper`, no `axum`
   anywhere in `crates/`. Frozen by H, so dispatching it produces unmergeable
   work.
3. **`dm2_06`'s authorization type state.** Blocked by `B-P2-XO-01` and by §8's
   prohibition on inferring authorization.

That is the honest frontier: one decision-gated disposition, one
transport-frozen binary, one owner-gated type state. Not six percentages.

### 9.4 The `13-engineering-decisions` bilingual gap is still 75% of the baseline

§7.6 measured 58 of 77 gaps in that one root, and nothing has changed:

```
$ BASE_SHA=HEAD~1 HEAD_SHA=HEAD python scripts/check_bilingual_docs.py
bilingual baseline: 77 frozen, 0 new gaps
```

`PAIR_EXEMPT_PREFIXES` and `EMBEDDED_BILINGUAL_SOURCES` still cover nothing
under `13-engineering-decisions`. This is not a code defect and not a doc defect;
it is a policy shape that root has never satisfied. Recorded here so the next
reader does not re-derive it.

### 9.5 Two governance records are red on main, and one of them is a ruling that did not land

`GOV-DOC-002` fails on `main` with exactly two errors, both `NO_AUTHORITATIVE_SOURCE`:

| scope | declaring file | status |
|---|---|---|
| `memory-compiler/reading-guide` | `04-memory-compiler/README.md:15` | `Non-Canonical` |
| `protocol/bmcp-message-type-index` | `08-bmcp-protocol/protocol-index.md:14` | `Candidate` |

The first is the one Architecture Owner already ruled on. PR #496 merged the
root README with `canonical_status: Non-Canonical`, but the ruling was
`Canonical / Informative`. The merge did not carry the ruling. Fixing it is a
one-line metadata edit plus the same edit in the two mirrors — and it is a
content-authority assertion, not a code change, which is why it needs an owner
rather than a patch.

The second has had no ruling at all. `protocol-index.md` is a generated
inventory audited at a pinned base; whether it is *authoritative* for the
message-type namespace, or merely a report about it, has not been decided.

Both are recorded in #564. Neither is fixed by this document.

## 10. Errata for §9, measured at `61b9d743` (2026-11-22 13:30 +08:00)

§9 is not edited above. Two of its statements were wrong when written, and one
became wrong when `main` moved. They are corrected here rather than in place,
because a frontier document whose measurements are silently rewritten cannot be
audited — the next reader cannot tell a correction from an original claim.

### 10.1 `bmcp-server` exists, and §9 said it did not

§9 §2 said:

> No `TcpListener`, no `hyper`, no `axum` anywhere in `crates/`.

False at `61b9d743`. `crates/bmcp-server` is a workspace member — 723-line
`lib.rs`, 67-line `main.rs`, 166-line `rt_scenarios.rs` — and its fourth line is:

```rust
use std::net::{SocketAddr, TcpListener, TcpStream};
```

The error is worth naming because it is the same class §9 exists to diagnose: an
absence reported without checking for the artifact. I measured `crates/` from a
tree that predated the crate.

### 10.2 The corrected BMCP finding is narrower and more useful

What is actually true is not "transport absent" and not "transport present":

- 22 unique `message_type` values are declared across 32 schemas, and the index
  checker passes (`unique_message_types=22`, `missing=0`, `extra=0`).
- Exactly **one** has a Rust parser: `parse_and_validate` returns
  `AppliedDeliveryEvidence` by name, and the `message_type` check is a constant
  comparison (`lib.rs:892-903`), so any other type yields `WrongConst`.
- `bmcp-server` implements one JSON-RPC method (`initialize`) and returns
  `-32601 Method not found` for everything else.
- `bmcp-server` never reaches the parser. Its only `bmcp_protocol` reference in
  the whole crate is:

```rust
// lib.rs:718-723
// This local formatter is available for a future evidence-validation call site.
#[allow(dead_code)]
fn describe(error: &bmcp_protocol::validate::EvidenceError) -> String {
```

`#[allow(dead_code)]`, "for a future call site", zero call sites.

So: **a listener exists, and zero of the 22 message types reach a parser.** That
is a routing gap plus 21 missing parsers, not a missing binary. The 21 parsers
are transcription against existing JSON Schema and are not frozen by anything.
Framing, session and handshake remain frozen by H — `TECH-REALITY-001-C/README.md:70`
still reads *"H wire mapping remains NOT FROZEN"* — so building on the existing
JSON-RPC/TCP choice would build on an undocumented premise.

Full measurement: GAP-16.

### 10.3 §9 filed `dm2_06` under the wrong owner

§9 §3 said `dm2_06` was "blocked by `B-P2-XO-01` and by §8's prohibition on
inferring authorization". The second half is right; the first is a conflation.

`B-P2-XO-01` asks *is this authorization genuine?* — I's question, still open.
`dm2_06` asks *is one present at all?* — a type-state question.
`FactRevision::initial` takes `AuthorizationDecisionRef` as a **required,
non-`Option`** parameter (`memory-domain/src/lib.rs:831`) and the type is a unit
struct whose only constructor is `pending_i() -> Self(())`, so no value of it can
mean "absent". That is why the negative case could not be written, and it needs
nothing from I.

Decided in `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`: three states
(`Absent` / `Placeholder` / `Issued`), only `Absent` blocks, and the type must
not be nameable as proof.

### 10.4 What survives §9 unchanged

The four falsified percentages, the `503 / 0 / 1` measurement, the
`13-engineering-decisions` 58-of-77 attribution, and the ruling that the two
`NO_AUTHORITATIVE_SOURCE` scopes are retirements rather than promotions. §9's
central claim — that the six percentages are the wrong frame — is strengthened
by these corrections, not weakened: three different errors of the same class
(reporting a state without re-measuring it) appeared inside the document that
argues against that class.

**Authority correction for the reading-guide scope:** §9.5's statement that the
reading guide had been ruled `Canonical / Informative` is superseded by Issue
#564 comment `7074302216`. The current Owner decision is not to promote it:
`04-memory-compiler/README.md` remains `canonical_status: Non-Canonical` and
`normative_status: Informative`. The later execution records in #564 comments
`7074470193` and `7074777892` clarify clauses 2/3; they do not reverse clause 1.
The protocol index remains `Candidate` with canonical current version
`NOT DECLARED`.
