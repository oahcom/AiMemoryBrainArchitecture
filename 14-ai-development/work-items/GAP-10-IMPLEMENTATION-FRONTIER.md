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

`crates/memory-domain` has implemented the Claim identity classifier in
`claim_identity::classify` (PR #545). The remaining ignored acceptance tests
name other missing capabilities such as `ClaimRevisionRegistry`,
`RelationTypeRegistry` and `ProvenanceGraph`; `classify_claim_change` is
not the API name and must not be counted as a missing symbol.

So Phase 2 is "types, invariants and Claim identity classification implemented;
some registries and graph capabilities remain absent". Phase 3 is a different
question and is not addressed here.

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

**T2.1 — Phase 2 registries and remaining graph capabilities**

The Claim identity classifier is already implemented by PR #545 as
`claim_identity::classify`; the public function is named `classify`, not
`classify_claim_change`. This work item makes `dm2_03` a real acceptance
test using `ClaimRevision::initial` / `successor` and covers the 10 reachable
vectors: CI-01..CI-04, CI-07..CI-11 and CI-13. CI-05, CI-06 and CI-12 are
unreachable because `ClaimRevision` has no quantifier, modality or confidence
field; they are explicitly not counted as covered.

The remaining ignored acceptance tests concern other missing APIs, including
`ClaimRevisionRegistry`, `RelationTypeRegistry`, `ProvenanceGraph` and
`EvidenceIndependence::validate`. Implementing those capabilities is separate
from the already-present Claim identity classifier.

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
| Phase 2 domain | 100% not started | **False.** Types, invariants and `claim_identity::classify` are implemented; `dm2_03` now exercises 10 reachable CI vectors. CI-05/06/12 are unreachable from the current `ClaimRevision` shape; other registry/graph gaps remain |
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
