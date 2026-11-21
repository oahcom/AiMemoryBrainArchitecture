# GAP-BASELINE-001 — Key Missing Workload Baseline

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Frozen at: **2026-11-21 15:00 +08:00**
- Measured at commit: `a8fd2b7` (main, after `git pull --ff-only` from a stale `67ab237`)
- This file committed as: `1ad6c2c` (the commit that introduces this document; tree content
  of all measured paths is identical to `a8fd2b7` because this commit adds only this file)

**Baseline authority rule:** when this document and a dispatch prompt name different SHAs,
the dispatch prompt's SHA is authoritative for *which tree to read*. `1ad6c2c` and
`a8fd2b7` differ by exactly one file — this one. All measurements below were taken at
`a8fd2b7` and remain valid at `1ad6c2c`.
- Status: **FROZEN BASELINE — not an acceptance decision**
- Authority: Owner-level dispatch baseline; each Owner retains normative authority in its own scope.

## Why this document exists

Six work areas were named as key missing workload, with percentages (85% / 80% / 90% /
60% / 100% / 100% unimplemented). Those figures were produced against an older tree.
The repository has since advanced 536 commits. This document re-measures each area at
the current base commit so dispatch rests on the tree, not on remembered numbers.

**All prior percentages are superseded by the measurements below.** Where a measurement
contradicts the prior claim, the measurement governs and the contradiction is stated.

## Measured state at commit `a8fd2b7` (= tree of `1ad6c2c`)

### GAP-01 — Memory Compiler core logic

| Item | Measured |
|---|---|
| Owning Owner | **E** (Memory Compiler Architect) |
| Docs | `04-memory-compiler/` exists with 2 files: `phase-1-event-store-contract.md` + `.zh-CN.md` |
| Rust code | **0** — no crate references `compiler`/`Compiler` anywhere under `crates/` |
| Reference model | 0 |
| Prior claim | 85% unimplemented |

**Correction:** the area is not 85% unimplemented — it is **0% implemented as code** and
~10% specified. The two existing files are an event-store contract, not a compiler stage
contract. There is no `crates/memory-compiler`.

Acceptance condition: a compiler stage contract exists naming stages, inputs, outputs,
provenance fields and failure semantics; plus `crates/memory-compiler` (or an equivalent
reference model) whose tests run under the pinned toolchain and report exact pass counts.

### GAP-02 — Memory Context engine

| Item | Measured |
|---|---|
| Owning Owner | **G** (Memory Context Architect) |
| Design docs | 19 `.md` files |
| Rust implementation | `crates/memory-context/src/lib.rs` — **472 lines, 7 `#[test]`** |
| Python reference model | `06-memory-context/reference-model/g_applied_ledger.py` + test |
| Prior claim | 80% unimplemented |

**Correction: the prior claim is wrong.** A real, compiling implementation exists with
deterministic snapshot planning (`ContextBudget`, `ContextIdentity`, delivery intents
that are non-sendable by construction). The area is partially implemented, not 80% absent.

Residual gap: the crate stops before persistence and transport by design. Delivery
intents are non-sendable, so no end-to-end path exists yet.

Acceptance condition: every documented concern (budget/sufficiency, edit operations,
reconciliation, versioning, manager) maps to either an executable model with tests or an
explicit `NOT IMPLEMENTED` row with a stated blocking reason.

### GAP-03 — Agent Integration core

| Item | Measured |
|---|---|
| Owning Owner | **C** (Agent Integration Architect) |
| Design docs | 4 `.md` files |
| Rust code | **0** — no crate references adapter/agent-integration types |
| Tests | **0** |
| Prior claim | 90% unimplemented |

**Correction:** confirmed — nothing executable exists. The `adapter` matches found under
`crates/memory-*` are SQLite adapter naming, unrelated to agent adapters.

Acceptance condition: an adapter capability tier table bound to concrete operations,
plus an executable reference model demonstrating tier enforcement and inference-boundary
rejection, with tests.

### GAP-04 — BMCP full protocol stack

| Item | Measured |
|---|---|
| Owning Owner | **H** (BMCP Protocol Architect) |
| Contracts | 4 `.md` files |
| Schemas | 1 (`bmcp.applied-delivery-evidence-1.0.0.schema.json`) |
| Validators | 1 (`applied_delivery_evidence_validator.py`) |
| Conformance suites | `applied_delivery_evidence` has a test file; `provider_outcome` has **fixtures + requirements.txt only, no test** |
| Rust code | **0** — no crate or tool references BMCP |
| Prior claim | 60% unimplemented |

**Correction:** the area is ~85% unimplemented as code. Only one of two conformance
suites executes; the protocol itself has no runtime implementation.

Acceptance condition: every schema has a validator and an executing conformance suite;
`provider_outcome` fixtures gain a test file; a protocol index enumerates all message
types with implemented/unimplemented status.

### GAP-05 — Phase 2/3 domain model extension

| Item | Measured |
|---|---|
| Owning Owner | **B** (Domain Model Architect) |
| Docs under `02-domain-model/` | 10 `.md` files, all Phase-1 scoped (`phase-1-*` ×4) |
| Rust code | `crates/memory-domain/src/lib.rs` — 679 lines, 13 `#[test]` |
| Phase 2 artefacts | **0** |
| Phase 3 artefacts | **0** |
| Prior claim | 100% not started |

**Correction:** "100% not started" is accurate for Phase 2/3 specifically, but must be
read narrowly — Phase 1 domain model **is** implemented in Rust. The gap is the Phase 2/3
extension, not the domain model as a whole.

Acceptance condition: a Phase 2 domain extension specification with entity, invariant and
migration statements, accepted by Owner B or explicitly blocked with a named dependency.

### GAP-06 — End-to-end tests

| Item | Measured |
|---|---|
| Owning Owner | **A** (Principal Integration Architect) |
| `tests/` at repo root | 2 files: `test_check_bilingual_docs_full.py`, `test_policy_inheritance.py` — both governance, neither cross-module |
| Integration tests | `crates/memory-event-store-sqlite/tests/{forget_fence,resilience}.rs`, `crates/memory-store/tests/sqlite_integration.rs` — each exercises one crate |
| E2E harness | `benchmarks/req10_e2e/` exists with `benchmark.py` + `fixture_runtime.py` |
| E2E actual run | **NOT_MEASURED** — the harness README states "development baseline only. Integrated product-runtime measurements: NOT_MEASURED" and "The fixture is not a substitute for the runtime" |
| Prior claim | 100% not started |

**Correction:** "100% not started" understates the work — a harness contract and protocol
exist. But the harness has **no adapter executing the real product path**, so no
end-to-end test actually runs. The area is ~20% done (harness) / 0% done (real path).

Acceptance condition: at least one test executes a path spanning two or more of
{compiler, context, agent-integration, bmcp} against the real product path and asserts an
observable contract outcome, runnable by a single documented command.

## Corrected summary table

| Gap | Owner | Prior claim | Measured reality | Verdict on prior claim |
|---|---|---|---|---|
| 01 Compiler | E | 85% missing | 0% code, ~10% specified | **Understated** — worse than claimed |
| 02 Context | G | 80% missing | Partial: 472 lines Rust + 7 tests | **Overstated** — real code exists |
| 03 Agent Integration | C | 90% missing | 0% code | Confirmed |
| 04 BMCP | H | 60% missing | ~85% missing as code; 1 of 2 suites executes | **Understated** |
| 05 Phase 2/3 | B | 100% not started | 100% not started (Phase 1 is done) | Confirmed, with scope caveat |
| 06 E2E | A | 100% not started | Harness exists, no real adapter → nothing runs | **Understated** — work has begun |

## Dispatch rules

1. Each gap is dispatched to exactly one Owner conversation. No Owner edits another
   Owner's normative contract.
2. Cross-owner questions are recorded verbatim in the Owner's reply and the Owner stops
   at that boundary. Recording a boundary question is a valid terminal state.
3. No self-approval. Every delivery requires a separate review conversation with frozen
   inputs.
4. Percentages here are measurements at `a8fd2b7` and must be recomputed, not quoted, by
   any later status report.

## Explicit non-claims

- This baseline does not authorize merge, production activation, or closure of any
  finding in the R3 defect register.
- The corrected verdicts above are measurements of *presence in the tree*, not quality
  judgements of the code that exists.

## Post-baseline measurements

Everything above is a measurement at `a8fd2b7` and is left unedited, per dispatch
rule 4. This section records what changed afterwards, so a reader can tell a frozen
baseline from a moving target.

### GAP-01 — the compiler now has an executing admission layer

`GAP-01` above says "0% code". That is no longer true, and the change came from two
commits that were not part of the original dispatch:

| Commit | Content |
|---|---|
| `a730880e` | `crates/memory-compiler` — five typed stages, structured provenance, two distinct admissions, `PREPARED_HIDDEN`, pure Rust, zero dependencies |
| `8c58d4c6` (PR #427) | `src/admission.rs` +1217 lines — producer admission, fence/gate contention, protocol-sequence receipts; crate gains `rusqlite`, `sha2`, `serde` |

Measured on `main` at `8c58d4c6`, tree read back from the API and built in a clean
directory:

```
$ cargo test --offline -p memory-compiler
running 19 tests
test admission::tests::alternative_exit_transitions_are_accepted_and_persisted ... ok
test admission::tests::fence_and_gate_compete_on_one_protocol_sequence_exactly_one_wins ... ok
test admission::tests::final_gate_receipt_binds_observed_fence_and_permission_epoch ... ok
test admission::tests::gate_reports_stale_protocol_when_fence_generation_matches ... ok
test admission::tests::illegal_transition_accept_to_published_is_rejected ... ok
test admission::tests::partial_dependencies_remain_hidden_until_all_edges_are_registered ... ok
test admission::tests::producer_receipt_lookup_and_not_found_are_distinct ... ok
test admission::tests::producer_registration_is_idempotent_and_conflicting_digest_does_not_add_rows ... ok
test tests::extraction_is_deterministic_and_lineaged ... ok
test tests::ingestion_preserves_original_receipt ... ok
test tests::ingestion_requires_durable_receipt_and_intent ... ok
test tests::late_worker_cannot_publish ... ok
test tests::normalization_preserves_upstream_identity ... ok
test tests::publication_requires_second_admission ... ok
test tests::publication_requires_visibility_authorization ... ok
test tests::staged_derivative_is_hidden ... ok
test tests::staging_requires_complete_dependency_closure ... ok
test tests::staging_requires_producer_admission ... ok
test tests::successful_publication_requires_both_admissions ... ok

test result: ok. 19 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.29s
```

Nineteen tests, not eleven. The eight new ones are all admission-layer behaviour.

**Environment note, because it changes how this must be reproduced:** the crate now
depends on `rusqlite`, which needs a C compiler. On the Windows host `gcc` cannot
execute `cc1`, so `libsqlite3-sys` cannot build there at all — this is a host
environment defect, not a crate defect. The run above was executed in WSL2 Ubuntu
with `cargo 1.95.0` / `gcc 13.3.0` and `CARGO_BUILD_JOBS=1` (parallel codegen on the
`/mnt/c` mount exhausts memory). Any future claim about this crate must state which
toolchain produced it.

### GAP-01 — one architecture, not two: Owner E ruling recorded

A second GAP-01 delivery existed as PR #425 (root `04-memory-compiler/`, six stages,
Python reference model, 10 tests). Owner E was asked to adjudicate and returned
`FINAL: DECIDED`:

| Question | Ruling |
|---|---|
| Path convention | `docs/en/` + `docs/zh-CN/` mirrors. Root `.zh-CN.md` suffix is **not** the pattern for new normative documents. |
| Stage inventory | **Five** stages. `Provenance` is a cross-cutting field on every stage output, **not** a sixth stage. |
| Reference implementation | `crates/memory-compiler` (Rust) only. The Python model does not survive as a second executable authority. |

The ruling is `DECIDED FOR CONVERGENCE`, explicitly not `ACCEPTED`, and it does not
grant Owner E any authority over D, I or Storage admission — `PublicationAuthority`
stays an injection boundary, and the seven `PublicationProof` booleans are evidence
inputs E may verify but may not issue.

This ruling was not accepted on assertion. Reproducing `current_bilingual_gaps()` from
`scripts/check_bilingual_docs.py` against both trees showed PR #425 would add **three**
new bilingual gaps (its two contract files plus `reference-model/README.md`, none with
`docs/en` or `docs/zh-CN` counterparts), and `main()` returns 2 on any new gap. `main`
itself has **zero** gaps in that directory. One of the two placements could not
survive the gate; the ruling chose the one that can.

### GAP-06 — first cross-module test exists and executes

PR #444 adds `crates/memory-context/tests/e2e_store_to_context.rs`, spanning
`memory-storage-sqlite` → `memory-store` → `memory-context`. Measured:

```
$ cargo test -p memory-context --test e2e_store_to_context
running 1 test
test sqlite_store_read_current_builds_context_from_persisted_revision ... ok
test result: ok. 1 passed; 0 failed; 0 ignored
```

One test is not an E2E suite, and `benchmarks/req10_e2e/README.md` still says
`NOT_MEASURED` — correctly, because this exercises modules, not the product runtime.
The GAP-06 acceptance condition ("a path spanning two or more modules, single
documented command") is met for the first time.

### GAP-02, GAP-04 — suites now execute

| Gap | Suite | Measured |
|---|---|---|
| 02 | `06-memory-context/reference-model/test_g_context_model.py` (PR #433) | `Ran 15 tests ... OK` |
| 04 | `08-bmcp-protocol/tests/conformance/provider_outcome/test_provider_outcome.py` (PR #436) | `Ran 10 tests ... OK (skipped=5)` |

The five skips in GAP-04 name their own blocker (`requires Owner C authoritative
validator`). Recording a skip with a named dependency is the correct outcome; making
them pass against a local reimplementation would have been a false green.

### What has not changed

- GAP-03 remains 0% code. PR #430 is a candidate specification, `DRAFT`, `approver:
  null`, `normative_status: Informative`.
- GAP-05 remains unimplemented. PR #435 is a specification; the Phase 2 entities,
  revisions and invariants it defines exist in no Rust type.
- No gap is closed. Every number above is a measurement of presence, not a quality
  judgement, and none of it is acceptance.

## Independent reviews and the CI outage

This section records two things the earlier sections could not: the first independent
reviews required by dispatch rule 3, and the fact that no CI job in this repository has
executed since billing broke. Both change what "measured" can mean here.

### The CI outage invalidates every check status in this repository

Every check run I sampled — on `main` HEAD and on five PR heads — reports
`completed / failure` with exactly one annotation:

> The job was not started because recent account payments have failed or your spending
> limit needs to be increased.

No job executed. There is no log, because there is no run.

| ref | check runs | all failures are billing |
|---|---|---|
| `main` HEAD `477a55e6` | 2 | yes |
| PR #451 `1f139cea` | 3 | yes |
| PR #444 `d84ea5c5` | 5 | yes |
| PR #433 `2d291569` | 6 | yes |
| PR #436 `1ffed9ed` | 5 | yes |
| PR #425 `8142b1ca` | 5 | yes |

Consequence, stated plainly because it was being misused: **"CI is red" is not evidence
against a PR in this repository right now.** A correct PR and a broken one carry the same
red X. `mergeable` is still computed by git and is still reliable; check runs are not.

This is a repo-level blocker. Nothing in any GAP delivery can fix it. Every measurement
in this document therefore comes from local execution, and is labelled as such.

### A gate defect found while measuring: `ROOT` is `Path.cwd()`

`scripts/check_bilingual_docs.py` sets `ROOT = Path.cwd()` at import time. Pairing
resolution (`side_by_side_partner`, `mirror_partner`) reads files through `ROOT`, while
the baseline is read through `REPO_ROOT`. Running the script from any directory other
than the repository root silently produces a different answer.

I hit this: measuring from the parent directory reported **32 new gaps on `main`**, which
would mean `main` itself was broken. Running from the repository root reported
**86 frozen, 0 new gaps**. The 32 were an artefact of my own invocation, not a repo state.

Anyone reproducing these numbers must `cd` to the tree root first. I record this because
I nearly filed the artefact as a finding.

### Two independent reviews, both FAIL, both finding something I missed

Dispatch rule 3 says test execution is not approval. Two review sessions were dispatched
with frozen inputs (branch head, my raw outputs, and an explicit prohibition on reusing my
conclusions). Both re-derived the measurements rather than trusting them.

| PR | GAP | reviewer verdict | found independently |
|---|---|---|---|
| #433 | 02 | `FAIL` / `FINAL: BLOCKED` | coverage doc miscounts its own tests: says 14, actual 15 |
| #436 | 04 | `FAIL` / `FINAL: BLOCKED` | index declares baseline `1ad6c2cf` but lists a file created by the PR |

Both findings are real and both are mine to record as misses:

**#433.** `context-implementation-coverage.md:131` and `:143` say the reference model has
14 tests. `grep -c "    def test_"` gives 15. Verified by me after the reviewer reported it:

```
$ python3 -m unittest test_g_context_model.py -v   ->  Ran 15 tests ... OK
$ python3 -m unittest test_g_applied_ledger.py -v  ->  Ran 8 tests ... OK
$ python3 -m unittest discover -s . -p 'test_*.py' ->  Ran 23 tests ... OK
```

The document's stated total of 29 is wrong under either basis: 30 if counting only
`test_g_context_model.py` against the pre-existing 15, 23 if counting the whole directory.
**The document never says which basis it uses**, which is the deeper defect.

**#436.** `protocol-index.md` states `Baseline: 1ad6c2cf...` and its evidence-boundary
section says it records presence "at the indexed repository baseline". It then lists
`tests/conformance/provider_outcome/test_provider_outcome.py`, which this PR creates.
I confirmed the contradiction:

```
GET /contents/08-bmcp-protocol/tests/conformance/provider_outcome/test_provider_outcome.py?ref=1ad6c2cf...
-> 404
```

The same class of defect as #433: a document whose declared basis does not match its
contents.

### What the reviews confirmed rather than refuted

Not everything failed. These hold up under independent re-derivation:

- **#436's pin is genuine.** Blob `a631bc7a...` resolves to `$id:
  urn:aimba:schema:c-submit-outcome:1.0.1`, `title: CSubmitOutcome`, `schema_version:
  1.0.1`, with `$defs` and `allOf` present. The index's claim about an external C-owned
  schema is accurate, and it correctly declines to reclassify it as BMCP-local.
- **#436's assertions are real schema assertions.** `Draft202012Validator` and
  `validator.validate(record)`, not attribute checks.
- **#433's 19-row mapping is correct** against source SHA `1ad6c2cf`: 0 missing, 0
  nonexistent, 0 blob-SHA mismatches.
- **#433's bilingual pair is a translation**, per 8 line-by-line spot checks.

### GAP-04's merged-tree result

Re-measured on a real merge of `main` (`00e3d2ea`) with the branch, in a real git clone:

```
$ python3 -m unittest discover -p 'test_*.py' -v
Ran 10 tests ... OK (skipped=5)
```

5 pass, 5 skip, 0 fail. The five skips name their own blocker (`requires Owner C
authoritative validator`). That matches what this document already recorded above and is
unchanged.

### GAP-06 re-verified after 58 commits of main drift

The earlier entry measured PR #444 on its own head. That was the weaker claim. Re-measured
on the merged tree (`main` + branch, no conflicts), in WSL2 because the Windows host cannot
compile `libsqlite3-sys`:

```
$ cargo test -p memory-context                    ->  20 passed; 0 failed
$ ./target/debug/deps/e2e_store_to_context-...    ->  1 passed; 0 failed
```

The bilingual gate on that same merged tree: `rc=0`, `86 frozen, 0 new gaps`, `PASS`.
That last line matters because two other GAP PRs fail the identical command.

### Corrected gate results, using `main`'s gate against each PR tree

Measured on real merges, `PR_BODY` empty:

| PR | GAP | merged gate `rc` | new bilingual gaps |
|---|---|---|---|
| #444 | 06 | 0 | 0 |
| #433 | 02 | 2 | 2 |
| #436 | 04 | 2 | 2 |
| #425 | 01 | 2 | 3 (closed before this re-measurement) |

Root cause is one rule, not four mistakes: `.zh-CN.md` side-by-side pairing is only
understood inside `14-ai-development`. For every other normative root the requirement is
`docs/en/<path>` **and** `docs/zh-CN/<path>`, both present. Four PRs placed translated
pairs at the root of a non-`14` directory and assumed they paired. They do not.

### Two PRs closed during this period, not by me

- **#425** closed without merge at `2026-11-21T09:03:37Z`. Reason recorded by the Project
  Owner: superseded by the five-stage Rust direction in `a730880e`, not a rejection of its
  10/10 Python tests.
- **#451** closed without merge at `2026-11-21T09:13:52Z`. Its intent landed via #455,
  which fixed a one-sided-mirror hole that #450 had introduced.

I record both because #425 was the subject of the Owner E adjudication in the section
above, and that adjudication now has an executed disposition rather than a pending one.

### What still has not changed

- GAP-03 remains 0% code. GAP-05 remains unimplemented.
- No gap is closed by this document. Every number here measures presence and execution,
  not quality, and none of it is acceptance.
- Four PRs still have zero approvals. Two now have zero-approval reviews that returned
  `FAIL`. A review is not an approval either.

## Correction: PR #461 invalidated the gate results above

The section "Corrected gate results" and two rows of "Two independent reviews" were
accurate when written and are no longer true. PR #461 merged while I was writing them.

### What #461 changed

`7de3111d` and `0d0c1c62` widened `side_by_side_partner()` from `14-ai-development` only
to **every** normative root:

```python
def side_by_side_partner(source: str) -> str | None:
    """Conventional side-by-side counterpart, accepted in every normative root."""
    ...
    elif source.endswith(".zh-CN.md"):
        stem = source[: -len(".zh-CN.md")]
        for cand in (stem + ".en.md", stem + ".md"):
            if cand != source and (ROOT / cand).is_file():
                return cand
```

Before #461, `06-memory-context/context-implementation-coverage.md` +
`.zh-CN.md` did not pair and both were gaps. After #461 they pair.

### What this does to the numbers

| claim above | status after #461 |
|---|---|
| #433 merged gate `rc=2`, 2 new gaps | **no longer true** — the pair resolves |
| #436 merged gate `rc=2`, 2 new gaps | **no longer true** — the pair resolves |
| "Root cause is one rule, not four mistakes" | still the right diagnosis of the *old* gate; the rule was changed rather than the files |

I re-measured on the current `main` (`c3713452`, tree `_gm4`):

```
gaps=85  baseline=85  new=0  resolved=0   ->  PASS
```

Both #433 and #436 have since been merged (`2026-11-21T09:33:25Z` and later), and `main`
carries no new gap. So the gate failure I reported was real at the time, was fixed by
changing the gate, and the deliveries landed.

### The honest reading

I reported a gate failure. It was a genuine measurement of the gate as it stood. Then the
gate changed, which is a legitimate way to resolve it and also the way that makes my
measurement stale within the hour.

I am not withdrawing the finding — the files genuinely did not pair under the rule that was
in force, and three PRs were blocked by it. I am withdrawing the implication that the
deliveries were defective. They were not; the rule was too narrow for where they put their
translations.

### The open question this creates

Widening `side_by_side_partner()` to every root accepts `X.md` + `X.zh-CN.md` as a pair
**without checking that the second file contains Chinese**. An English file named
`X.zh-CN.md` now satisfies the gate. `_carries_chinese()` exists in the script but applies
only to the `mirrored` branch, not to the side-by-side branch.

That is a testable weakening and I have flagged it for measurement rather than asserting it
here. If it holds, the correct fix is to apply `_carries_chinese()` to the side-by-side
branch too — a two-line change — not to revert #461.

### Also corrected: "GAP-03 remains 0% code"

No longer accurate. PR #465 (`GAP-03: implement in-memory ContextDeliveryAdapter
lifecycle`) exists as a draft. "0% code" was true at the baseline and at the time of
writing; it is now a statement about a moving target, which is exactly what this section
exists to prevent.

### Still true

- No CI job in this repository has started since billing broke.
- No gap is closed by this document, and none of this is acceptance.
- The two review findings (#433's test miscount, #436's baseline/file mismatch) are
  independent of the gate question and remain unaddressed by #461.

## Round three: four new PRs, one merged-file defect, and a gate that cannot see any of it

This section covers work done after the correction above: PRs #463, #464, #465, #466, the
merged state of #433, and an audit of #461's gate change.

### Merged state of #433: a row cites a guard and a test that do not exist

#433 merged at `09:33:25Z`. Its coverage map is now in `main`, and one row overclaims:

```
| Historical Applied versus current-use after Forget/revocation | ...
  PARTIAL — current-use guard `current_use_allowed`;
  test `test_current_use_requires_every_currentness_gate`; ... | D |
```

Measured on `main` at `0ccdf0a1`:

```
$ grep -rn "current_use_allowed\|current_use_requires" 06-memory-context/reference-model/
(no output)
```

`06-memory-context/reference-model/` contains exactly two files, and
`test_g_applied_ledger.py` defines 8 tests — none of them the ninth name the document cites.

Of the 9 backticked test identifiers in the document, **8 are present and 1 is not.** That is
a different class of defect from the miscount I reported earlier. A miscount is arithmetic;
this is a row asserting that a capability exists in a `PARTIAL` state when the capability is
absent entirely. A reader planning the remaining work would conclude the current-use guard
needs persistence, when the guard itself does not exist.

The other 18 rows hold: 19 rows, each pinned to a spec section, each with an explicit
status and a named blocker owner, and the assessment pinned to a stated `main` SHA inside
the document rather than in a PR comment. One row overclaims; the rest is the most
disciplined artifact in the GAP series.

### #465 is blocked by a tool artifact committed as content

`9ff2f018` appends an execution-environment marker to **three** tracked files:

```
07-agent-integration/adapter-capability-tiers.md         line 232 of 232
07-agent-integration/adapter-capability-tiers.zh-CN.md   line 52 of 52
crates/agent-integration/src/lib.rs                      line 372 of 372
```

```
[executed on device: VM-0-9-ubuntu (d03d92fd-4b5d-4bc1-a701-985eb5de69cc)]
```

The string appears in 0 files on `main`, #463, #464 and #466. It is introduced here.

In Rust it is a hard failure — `expected item, found '['`, and `(d03d92fd-...)` is parsed as
a float exponent. In the two `.md` files it is a quiet failure: the gate reads them, they
parse as Markdown, and the marker renders as a bracketed paragraph. **So the bilingual pair
satisfies the gate in its broken state.** If the Rust line alone were fixed, the PR would
merge with the contamination intact and no check would notice.

On a cleaned copy the work is real:

```
running 8 tests
test result: ok. 8 passed; 0 failed
```

Covering apply/reconnect/clear, tier gating, frozen-region rejection, stale/skipped version
handling with no mutation. One commit ago (`4f0b4dbd`, the blob the body cites) the tests
passed. The body was not updated after the head moved, so every verification claim in it
describes a superseded commit.

### #466: gate PASS, 25/158 green, but the revision type lacks the fields it documents

`cargo test -p memory-domain` → `25 passed`. `cargo test --workspace` → `158 passed`
(base `0d0c1c6`: 146, so +12, matching the 12 added tests). The body says **156**; actual is
**158**. Second PR in a row with a wrong test count.

The substantive question is a design one. `ClaimRevision`'s doc comment says CI-09–CI-13 —
including epistemic status and confidence — classify as `NEW_REVISION` under the same
`ClaimRef`. But:

```rust
pub struct ClaimRevision { revision_ref, claim_ref, subject_ref, predicate,
    object_value, polarity, asserted_at, scope_refs, qualifiers, evidence_refs }
```

No `epistemic_status`, no `confidence`. The legacy flat `Claim` has both. So migrating a
consumer, which the `ponytail: superseded by ...` comment invites, would **lose** them. The
revision cannot express the change class it was created to express.

Two assertions are vacuous — `assert_ne!(fact_ref.as_str(), "claim-independent")` compares
against a literal that never participates in construction.

What holds: the four opaque newtypes are genuinely non-interchangeable at the type level;
`ClaimRevision` separates stable proposition identity from revision identity and tests it;
`FactRevision` binds `claim_revision_ref` and `authorization_decision_ref` exactly.

### #464: the four corrections are right, the authority they cite is absent

All four field changes verify against the GitHub API: branch, PR number, merge commit
`776f04fb...`, and the `FROZEN` carrier blob `6eb1a1fd...` unchanged at `main`, base and
head. Governance tests `Ran 25 tests ... OK`. The YAML parse failure reproduces on `main`,
so it is pre-existing, exactly as claimed.

But the `revision_history` entry cites `gap-owner-w1w3-decision.md` and
`gap-owner-v1v4-decision.md` as its authority. Neither exists in the tree at `61a45da7` —
1082 entries walked, 0 matches, and the only occurrence of those strings in the repository
is the manifest citing itself.

That is now three consecutive PRs whose stated authority cannot be read: #433's baseline
row, #436's baseline row, and this. A pattern, not three coincidences.

Two smaller things: the body labels `2fe294f5` as the `prompt-v1.md` blob when it is the
`manifest.yaml` blob (the conclusion is true, the evidence line points at the wrong object);
and `updated_at: 09:55:00Z` predates the commit that carries it (`61a45da7`, `09:59:33Z`).

### #463 is the clean one

```
$ cargo test -p memory-store --test cross_crate_contract --offline
running 6 tests ... test result: ok. 6 passed; 0 failed
```

Gate PASS. C2 and C3 assert that a *rejection* leaves no row behind — the failure mode that
corrupts storage silently. C4 and C5 assert stale and replayed writes do not mutate the
current revision. C6 asserts a duplicate creation preserves the typed error variant. That is
contract coverage, which is what the title claims.

### #461 weakened the gate, and the minimal exploit is a zero-byte file

The gate change widened `side_by_side_partner()` from `14-ai-development` only to all nine
normative roots, and deleted the root guard in `current_bilingual_gaps()`. The function tests
existence only:

```python
elif source.endswith(".md"):
    stem = source[: -len(".md")]
    for cand in (stem + ".en.md", stem + ".zh-CN.md"):
        if cand != source and (ROOT / cand).is_file():
            return cand
```

`.is_file()` is true for zero bytes. Measured on `main` `0ccdf0a1`:

```
02-domain-model/zz-empty-probe.md        -> in_gaps: False  (309 bytes, English only)
02-domain-model/zz-empty-probe.zh-CN.md  -> in_gaps: False  (0 bytes)
```

A zero-byte file satisfies the bilingual requirement, in eight additional roots. Pre-#461 the
same tree reported both as gaps and exited 2.

Inventory delta from the change, same tree, old vs new script: 93 gaps → 85, with 8 newly
accepted and **0 newly rejected**. All four of the real `.zh-CN.md` files in that set are
genuine translations (CJK counts 4020 / 2291 / 505 / 536), so the current inventory is not
falsified — only the mechanism is now content-blind in more places.

A second independent widening: `_carries_chinese()` now governs all nine roots instead of
one, so a document with 20 English lines plus a 143-character Chinese glossary passes as
bilingual where it previously did not.

**My own proposed fix was wrong and I withdrew it.** Adding `_carries_chinese()` to the
side-by-side branch produced **17 false positives**, because the helper requires >= 100 CJK
characters and several legitimate bilingual policy stubs are shorter. I measured the patch
before recommending it, which is the only reason it did not go out as advice. The narrow fix
that needs no threshold decision is `and (ROOT / cand).stat().st_size > 0` — it cannot
produce a false positive on any real document and raises the cheapest evasion from "create
an empty file" to "put something in it".

### What this round changes about the GAP series

| PR | GAP | gate | tests | state |
|---|---|---|---|---|
| #463 | 06 | PASS | 6 passed | clean |
| #464 | — | PASS | 25 passed (governance) | authority absent |
| #465 | 03 | FAIL (no manifest) | build broken at head | blocked |
| #466 | 05 | PASS | 25 / 158 passed | design question open |

GAP-03 and GAP-05 are no longer 0% code — they are now two PRs with real implementations and
real defects. That is progress of a specific kind: the gap between "nothing exists" and
"something exists and does not compile" is smaller than it looks from a distance, and larger
than it looks from a PR description.

Still true: no gap is closed by this document, no PR has an approval, and no CI job has run.

## Correction to round three: the merged-overclaim finding was mine, not the repository's

The round-three section above states that #433 merged and that one of its rows cites a guard
and a test absent from `main`. **Both parts are wrong.** I am appending the correction rather
than editing the section, because the wrong version is the one that was published.

### Wrong claim 1: #433 has not merged

```
GET /pulls/433 -> state=open  merged=False  merged_at=None
```

`09:33:25Z` is when **#436 and #444** merged. I read a batch of PR states and attached the
wrong timestamp to the wrong PR number.

### Wrong claim 2: the artifacts are in the PR, not missing from it

I checked `main` for `current_use_allowed` and
`test_current_use_requires_every_currentness_gate`, found them absent, and attributed the
absence to #433. I never checked #433's own tree. On head `2d291569`:

```
06-memory-context/reference-model/g_context_model.py         contains `current_use_allowed` -> True
06-memory-context/reference-model/test_g_context_model.py   defines the test             -> True
                                                            15 test functions
```

Both artifacts are present. The PR supplies them.

### What is actually true — the reverse of what I wrote

`main` already carries the coverage document, by direct commit rather than by PR:

```
5cc54a54  08:54:37Z  docs(memory-context): add implementation coverage map
b68b96bb  08:55:09Z  docs(memory-context): qualify design source filenames
9c92fefd  08:55:45Z  docs(memory-context): correct assessment scope and status legend
3fef2d7f  09:06:39Z  docs(memory-context): record applied ledger test result
351f4a4c  09:22:41Z  docs(GAP-02): refresh Memory Context coverage map to current main
```

And `main` at `b9ddd241` contains only:

```
06-memory-context/reference-model/g_applied_ledger.py
06-memory-context/reference-model/test_g_applied_ledger.py   (8 tests)
```

No `g_context_model.py`, no `test_g_context_model.py`. Yet `main`'s copy of the document cites
both `current_use_allowed` and `test_current_use_requires_every_currentness_gate`:

```
main doc cites current_use_allowed:                              True
main doc cites test_current_use_requires_every_currentness_gate: True
main doc cites g_context_model:                                  False
g_context_model files in main:                                   NONE
```

So the document reached `main` describing a reference model that is not on `main`. **#433 is
the delivery that closes that gap, not the defect that opened it.** Merging it moves `main`
from "document describes absent code" to "document describes present code".

### What survives from round three

The two independent review findings on #433 and #436 are unaffected, because they were about
different things: a test count (14 stated, 15 measured — re-verified by `grep -c` and by
`unittest`), and a baseline row in `protocol-index.md` listing a file the baseline does not
contain (verified 404). Neither depended on merge state or on where I looked for an artifact.

Everything else in round three stands: #465's three stray marker lines, #466's missing
`epistemic_status`/`confidence` and its 156-vs-158 count, #464's absent authority files,
#463's clean six tests, and the #461 zero-byte exploit.

### The failure mode, named

Both errors are the same error: I checked a convenient thing instead of the thing I was
claiming about. A batch read for merge state; `main` for a branch artifact. The first is
careless, the second is worse — `main` is exactly where an artifact would be missing if a PR
had not landed, so checking `main` guaranteed the answer I then misattributed.

Recorded because a wrong finding published on a PR is worse than no finding: someone acts on
it. The corrected comment is on #433 at `7061701355`.

## Round four: what actually landed, verified against `main` at `b9ddd241`

The merge timestamps, checked one PR at a time rather than in a batch:

| PR | state | merged_at |
|---|---|---|
| #433 | **open** | — |
| #436 | merged | 09:33:25Z |
| #444 | merged | 09:33:26Z |
| #463 | merged | 10:09:56Z |
| #464 | merged | 10:52:58Z |
| #465 | **open** (draft) | — |
| #466 | merged | 10:53:05Z |

Five merged, two open. What that means for each finding, checked against the tree rather
than assumed from the merge:

### #436's review finding survived the merge

```
main b9ddd241, 08-bmcp-protocol/protocol-index.md
  cites baseline 1ad6c2cf:                  True
  cites test_provider_outcome.py:           True
```

The independent review returned `FAIL` on exactly this: the document declares a baseline and
then lists a file created by the PR, which the baseline does not contain. Both statements are
still in the file on `main`. The finding had no effect on the merge decision, and the defect
is now in `main`.

This is worth stating plainly because the PR merged at `09:33:25Z` with **zero approvals and
an open `FAIL` review**, and no CI job has run since billing broke. The merge had neither
human sign-off nor automated verification.

### #433 has not merged, and it is the delivery, not the defect

`main` carries the coverage document by direct commit:

```
5cc54a54  08:54:37Z  docs(memory-context): add implementation coverage map
b68b96bb  08:55:09Z  docs(memory-context): qualify design source filenames
9c92fefd  08:55:45Z  docs(memory-context): correct assessment scope and status legend
3fef2d7f  09:06:39Z  docs(memory-context): record applied ledger test result
351f4a4c  09:22:41Z  docs(GAP-02): refresh Memory Context coverage map to current main
```

But `main`'s `06-memory-context/reference-model/` contains only `g_applied_ledger.py` and
`test_g_applied_ledger.py`. No `g_context_model.py`, no `test_g_context_model.py`.

And `main`'s copy of the document cites both `current_use_allowed` and
`test_current_use_requires_every_currentness_gate`:

```
main doc cites current_use_allowed:                              True
main doc cites test_current_use_requires_every_currentness_gate: True
main doc cites g_context_model:                                  False
```

On #433's head `2d291569` both artifacts exist (`g_context_model.py` contains
`current_use_allowed`; `test_g_context_model.py` defines that test, 15 test functions).

**So `main` currently documents a reference model it does not contain, and #433 is the PR that
supplies it.** The document is ahead of the code on `main`, and merging #433 closes the gap.

### #466 merged with the two missing fields

```
main b9ddd241, crates/memory-domain/src/lib.rs
  pub struct ClaimRevision present:   True
  #[test] count:                      25
  epistemic_status inside struct:     False
  confidence inside struct:           False
```

The type is on `main` and the design question I raised is unresolved on `main`: the doc
comment says CI-09–CI-13 classify as `NEW_REVISION` under a stable `ClaimRef`, and the struct
that implements `NEW_REVISION` has neither field. Migrating a consumer from the legacy `Claim`
would lose `epistemic_status` and `confidence`.

### #463 merged cleanly

```
main b9ddd241, crates/memory-store/tests/cross_crate_contract.rs   6 #[test]
```

Six contract tests, asserting that rejections leave no row behind and that stale/replayed
writes do not mutate the current revision. This is the one GAP PR of the round that landed
without an open defect.

### #464 merged with its unverifiable authority

```
main b9ddd241, 14-ai-development/work-items/AID-2026-040/manifest.yaml
  branch docs/aid-2026-040-e1-e8-measurement:  True
  pull_request 437:                            True
  merge_commit_sha 776f04fb:                   True
  cites gap-owner-w1w3:                        True
```

The four corrections are accurate and now on `main`. The authority they cite
(`gap-owner-w1w3-decision.md`, `gap-owner-v1v4-decision.md`) still does not exist in the tree.
Third consecutive PR whose stated authority cannot be read.

### #465 has not merged and its content is not in `main`

```
main b9ddd241, crates/agent-integration/src/lib.rs
  DeliveryPayload:            False
  ContextDeliveryAdapter:     False
  #[test]:                    4
  executed-on-device marker:  False
```

So the three stray marker lines are contained to the branch. `main` is clean: scanning every
tracked file for `executed on device` gives **0 hits** outside my own document, which
contains the string only because it quotes it.

### The pattern across five merges

Four of the five merged PRs carried a defect that was known before the merge and is still
present after it:

| PR | known defect before merge | present on `main` now |
|---|---|---|
| #436 | baseline row lists a file the baseline lacks | yes |
| #466 | revision type lacks the fields its comment says it carries | yes |
| #464 | cited authority files do not exist | yes |
| #444 | (clean — 20 unit + 1 integration passing) | — |
| #463 | (clean — 6 contract tests) | — |

That is not a claim that the merges were wrong. #466 and #464 are net improvements, and #433
not merging is worse for `main` than #433 merging. It is a claim about the review mechanism:
an independent `FAIL` review, a wrong test count, and a missing authority file all had zero
effect on whether a PR merged, because nothing in this repository currently gates on any of
them.

### Correction to my own round-three text

Two statements in the round-three section above are wrong and are superseded here:

1. "**#433 merged at `09:33:25Z`**" — it did not merge. That timestamp is #436.
2. "**a row cites a guard and a test that do not exist in `main`**" — the row is accurate and
   the artifacts exist, in #433. The absence is on `main`, because the document landed there
   by direct commit before the code did.

Both errors are the same error: I checked a convenient source (`main`) for a claim about a
branch. The corrected comment is on #433 at `7061701355`.

## Round five: the three PRs that were open at round four, measured

#471, #482, #483. All three pass the bilingual gate. Two of the three carry a structural
problem that the gate cannot see.

### Gate results, all measured against each tree's own baseline

| PR | GAP | gate | tests |
|---|---|---|---|
| #471 | compiler admission | PASS (85/85) | 30 passed default; SQLite test `#[ignore]`d |
| #482 | Phase 2 domain | PASS (80/80) | 21 passed + 3 compile-fail doctests |
| #483 | context ChangeSet | PASS (77/77) | not run (documentation + 1032-line lib.rs) |

### #471: the SQLite integration test never executes

The feature change is correct and does what the title says:

```toml
[features]
default = []
sqlite = ["dep:rusqlite"]
```

```
$ cargo test -p memory-compiler --offline
test result: ok. 30 passed; 0 failed; 0 ignored
```

No C toolchain, no SQLite. But the new 143-line `tests/sqlite_admission.rs` is gated twice:

```
$ cargo test -p memory-compiler --test sqlite_admission
error: target `sqlite_admission` requires the features: `sqlite`

$ cargo test -p memory-compiler --features sqlite --test sqlite_admission
test sqlite_fence_and_publication_gate_compete_on_one_protocol_sequence ... ignored
test result: ok. 0 passed; 0 failed; 1 ignored
```

`#[ignore]` survives `--all-features`, so this test does not run in a full-suite CI either.
It is well-written and dead by default. Making `rusqlite` optional is the right call — the
Windows host here cannot build it at all — but the "and here is where it actually runs" line
is missing, so a future green CI will not report that the real SQLite path is untested.

### #482 collides with `main`, and its version is the better one

`main` (`b9ddd241`, includes merged #466):

```rust
pub struct ClaimRevision { revision_ref, claim_ref, subject_ref, predicate,
    object_value, polarity, asserted_at, scope_refs, qualifiers, evidence_refs }
```

#482 (`4984042a`):

```rust
pub struct ClaimRevision { revision_ref, claim_ref, parent_revision_ref, subject,
    predicate, object, polarity, qualifiers, epistemic_status, valid_time,
    evidence_refs, provenance_refs, asserted_at, revision_reason }
```

Different field names, private visibility, different ref types, plus `epistemic_status`,
`valid_time` and `parent_revision_ref` that `main` lacks. Test sets confirm the fork point:
of `main`'s 25 tests, **12 are absent** — exactly the 12 #466 added.

So this branch forked before #466 merged and re-implemented the same types from a different
reading. Merging it replaces #466's types rather than extending them, and resolving the
conflict in this branch's favour silently reverts 12 tests that are now on `main`.

**And this branch's version fixes the exact defect I reported against #466.** I said
`ClaimRevision` cannot express a `NEW_REVISION` because it lacks `epistemic_status` while its
doc comment says CI-09–CI-13 classify as one. This version has `epistemic_status`, plus
`valid_time` and `parent_revision_ref`.

That is the shape of the problem in one PR: #466 merged a structurally incomplete type, and
the version that completes it arrives incompatible with what just landed. Three defensible
resolutions (rebase and reconcile; merge as explicit replacement; split the type change into
its own PR) and no way to pick one from measurement. Recorded, not decided.

### #483 rewrites the document that carries the defect, and keeps the defect

This PR modifies `06-memory-context/context-implementation-coverage.md` (`+20 -19`, 25354 →
29505 bytes), updates the base SHA to `b9ddd241`, and adds a ChangeSet round.

Line 104 is untouched:

```
| Historical Applied versus current-use after Forget/revocation | ...
  PARTIAL — current-use guard `current_use_allowed`;
  test `test_current_use_requires_every_currentness_gate`; ... | D |
```

Neither artifact exists in this tree. The reference model has 8 test functions; the document
cites 9 test identifiers, and the ninth is this one.

So the row has now propagated: written once, committed to `main` by direct commit
(`5cc54a54..351f4a4c`), carried through #433 where the code **does** exist, and carried again
here where it does not. The fix is either one row edit or merging #433 first.

### What round five adds to the pattern

Round four showed that a `FAIL` review, a wrong test count and an absent authority file do
not affect whether a PR merges. Round five shows the next layer: a document can be rewritten
by a later PR without the known-wrong row being fixed, because nothing checks a document
against the tree it describes.

The gate checks whether `X.md` has a partner. It does not check whether the claims inside
`X.md` are true. Every defect in this document — the miscount, the absent guard, the absent
test, the baseline row in `protocol-index.md` — is invisible to it, and all four survived at
least one merge or rewrite.

That is not an argument for a semantic gate; that is out of reach. It is an argument that
"the bilingual gate passed" is currently being read as "the document is sound", and those are
different claims.

### Standing caveat

No CI job in this repository has started since billing broke. Every number above is local
execution in WSL2 (`cargo 1.95.0`, `CARGO_BUILD_JOBS=1`, `--offline`) or local inspection.
Builds must be run from a native filesystem — compiling on the `/mnt/c` mount fails with
`Cannot allocate memory (os error 12)`.

## Correction to round three: the zero-byte gate exploit is closed on current `main`

Round three above states, with a reproduction, that a zero-byte `X.zh-CN.md` satisfies the
bilingual gate in eight additional roots. **That is no longer true, and it was fixed by a
better mechanism than the one I proposed.**

### Re-measured on `main` `f687346c`

Two scratch trees copied from `main`, one pair each, both under `02-domain-model/`:

```
=== zero-byte .zh-CN.md ===
  zz-empty-probe.md          exists=True  size=805  in_gaps=True
  zz-empty-probe.zh-CN.md    exists=True  size=0    in_gaps=True

=== all-English .zh-CN.md (byte-identical copy of the .md) ===
  zz-eng-probe.md            exists=True  size=805  in_gaps=True
  zz-eng-probe.zh-CN.md      exists=True  size=805  in_gaps=True
```

Both files of both pairs are reported as gaps. The exploit does not reproduce.

### The mechanism, which is the part worth recording

`main` now contains:

```python
def _side_by_side_bilingual(source: str) -> bool:
    partner = side_by_side_partner(source)
    if partner is None:
        return False
    return _has_any_chinese(source) or _has_any_chinese(partner)

paired = mirrored or _side_by_side_bilingual(source)
```

with `_has_any_chinese()` requiring **one** CJK character, while the >= 100 threshold in
`_carries_chinese()` stays for the embedded-bilingual shape only.

This is exactly the split I failed to produce. My proposed patch routed the side-by-side
branch through `_carries_chinese()` and generated **17 false positives** on short but genuine
bilingual policy stubs; I withdrew it. The fix that landed instead added a second predicate
calibrated for a different shape.

**The lesson is specific, not general:** the 100-character threshold was calibrated for one
pairing shape, and reusing it for another shape was the error. Two shapes, two rules. I
looked for one rule that would cover both and concluded the threshold was the problem.

### What this changes in the round-three text

| round-three claim | status |
|---|---|
| a zero-byte `X.zh-CN.md` satisfies the gate | **withdrawn** — re-measured, both files are gaps |
| an all-English `X.zh-CN.md` satisfies the gate | **withdrawn** — same |
| my two-line patch closes it | **withdrawn earlier** — 17 false positives |
| #461 widened content-blind pairing to eight more roots | **stands as history** — true when measured, since fixed |
| `_carries_chinese`'s 100-char threshold is too blunt for short docs | **stands** — which is why a separate predicate was needed |

### And #485 adds a further layer

PR #485 (head `9d77fd96`, `+11 -1`) introduces `PARTIAL_SIDE_BY_SIDE_PAIRS`:

```python
partial_side_by_side = (
    side_by_side is not None
    and frozenset((source, side_by_side)) in PARTIAL_SIDE_BY_SIDE_PAIRS
)
paired = mirrored or (_side_by_side_bilingual(source) and not partial_side_by_side)
```

A pair registered as partially translated does not count as paired even though it carries
CJK. That closes the "10% translated, passes `_has_any_chinese`, counted as done" case, which
is the next hole after the one that was just closed.

I have not verified the register's entries, or that the accompanying test change
(`test_gate_normative_roots.py`, `+49 -1`) covers the register rather than only the happy
path.

### Why this correction matters more than the average one

I published a reproduction and a patch on a public PR. Both were wrong, in opposite
directions: the reproduction stopped being true, and the patch would have made things worse.
Leaving either standing means the next reader tests a finding that does not reproduce.

The gate is materially stronger than when I last examined it. Recorded here because most of
this document is about what the gate cannot see, and that balance should be accurate.

## Correction to the correction: the gate hole is half closed, not closed

The section above says the zero-byte exploit "does not reproduce" and "is closed on current
`main`". **That is half true, and stated as if it were wholly true.** The direction I tested
is closed; the other direction is open.

### What I tested, and what I failed to vary

My probe held the source English and varied only the partner:

```
zz-empty-probe.md        = 20 lines of English   (805 bytes)
zz-empty-probe.zh-CN.md  = ""                    (0 bytes)
-> both in_gaps=True    correctly rejected
```

Correct. But `_side_by_side_bilingual()` is:

```python
return _has_any_chinese(source) or _has_any_chinese(partner)
```

An `or`. I varied the right operand and left the left one English, so the short-circuit
never fired. The case that matters is the mirror image, and I did not test it.

### Both directions, measured on `main` `f687346c`

```
=== one CJK character, both files otherwise English ===
02-domain-model/zz-c1_one_char.md        = "# Title\n\nThis is English.\n\n一\n"
02-domain-model/zz-c1_one_char.zh-CN.md  = "# Title\n\nThis is English.\n\n一\n"
.md_in_gaps=False  .zh_in_gaps=False  =>  ACCEPTED as pair

=== Chinese source, zero-byte partner ===
02-domain-model/zz-c3_zero_partner.md        = 29 lines of Chinese
02-domain-model/zz-c3_zero_partner.zh-CN.md  = "" (0 bytes)
.md_in_gaps=False  .zh_in_gaps=False  =>  ACCEPTED as pair
```

Both pass. So:

| case | before #487 | after #487 (`main` now) |
|---|---|---|
| all-English `.zh-CN.md` | accepted | **rejected** — fixed |
| zero-byte `.zh-CN.md` with English source | accepted | **rejected** — fixed |
| zero-byte `.zh-CN.md` with Chinese source | accepted | **accepted** — still open |
| one `一` character in both files | accepted | **accepted** — still open |

`_has_any_chinese()` raised the floor from "no content check" to "one CJK character somewhere
in the pair". That closes the all-English case and leaves the asymmetric one open.

### The accurate statement of the current state

Not "the hole is closed" and not "the hole is open", but:

> The side-by-side branch now requires one CJK character in at least one of the two files.
> It does not require the *partner* to contain anything, and it does not require the two
> files to differ. A Chinese source with a zero-byte `.zh-CN.md` passes, and so does a pair
> of English files that each contain `一`.

The remaining fix is small and has no threshold problem: require `_has_any_chinese(partner)`
specifically — the partner must carry Chinese — rather than the disjunction. That is one
predicate, not a threshold decision, and it cannot produce a false positive on a real pair
because a real `.zh-CN.md` contains Chinese by definition.

### Where this came from, and why it is worth recording

Register 013 in PR #494 documents both cases with reproductions. I read it, re-ran them
myself, and they reproduce. I did not find them; I confirmed them, and in doing so found that
my own earlier "closed" conclusion was scoped to the one direction I happened to test.

That is the same failure as the #433 error recorded above, in a different form: I measured a
convenient instance of a claim instead of the claim. There I checked `main` for a branch
artifact; here I checked one operand of an `or`.

### Register 013 itself

The document is the most useful artifact in this repository on this subject, and specifically
because it withdraws its own claims:

```
C-1  "PR #470 wrote a GitHub API JSON body into scripts/bilingual-baseline.txt"  WITHDRAWN
C-2  "7 three-file (ambiguous) side-by-side groups exist"                       WITHDRAWN (this round)
C-3  "AI-EXEC-001.md edit returns rc=0, so the 14 root passes"                  CORRECTED
```

> C-2 and C-3 matter because both, taken at face value, would have inflated the defect count.
> A register that overstates its findings is as unusable as one that understates them.

One observation about the PR's own files: `docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-PAIRING-RESIDUAL-013.md`
contains **3 CJK characters in 10171 bytes**, and all three are the literal `一` being quoted
as the exploit. The register documenting that one character suffices is written entirely in
English in the `zh-CN` slot. It passes the gate — which is the point the register is making —
and it is the strongest available example of its own §3.1, which the document does not say.

The other three files in the PR are genuinely Chinese (764, 1565, 5896 CJK), and all four
root copies are byte-identical to their `docs/zh-CN/` counterparts, which is correct for this
repository's convention.

## Round five: the gate stopped being the bottleneck, and two crates turned out to be islands

This section records a measurement round taken against `main` at `665c8869`, after the
bilingual gate was repaired three times in one hour (`5f109308`, `d647e7d5`, and the
`_side_by_side_bilingual` / `_has_any_chinese` pair). The gate is no longer the thing that
rejects work. Something else is, and it is worth naming.

### Every open PR passes the gate. All nine of them.

Measured by overlaying each PR's *actual changed paths* (from the files API) onto a clean
`main` tree at `665c8869`, then running `current_bilingual_gaps()` from the tree root:

| PR | state | files | gate |
|---|---|---|---|
| #517 | READY | 1 | PASS |
| #513 | READY | 2 | PASS |
| #512 | READY | 2 | PASS |
| #507 | DRAFT | 4 | PASS |
| #500 | READY | 77 | PASS |
| #496 | DRAFT | 9 | PASS |
| #494 | READY | 30 | PASS |
| #471 | DRAFT | 8 | PASS |
| #433 | READY | 3 | PASS |

All nine: `gaps=77 base=77 new=0 resolved=0`.

**This contradicts what I reported twice before, and the contradiction was my method.**
My earlier runs measured each PR's *branch snapshot*, where files added to `main` after the
branch point appear as gaps the PR did not introduce. Two examples of that artefact, both
of which I published before checking:

- I reported #471 and #433 as introducing 6 new gaps each. Those six were
  `06-memory-context/README.md`, four `phase-3.6.x` contracts and
  `07-agent-integration/agent-integration-overview.md` — all added to `main` by later
  commits, none touched by either PR. Overlaid correctly, both are clean.
- My first overlay attempt was also wrong, in the opposite direction: it copied *every*
  file in the PR tree that differed from `main`, which re-introduced the same drift and
  reported `resolved=8, FAIL`. Copying only the paths the files API names is the correct
  method.

The lesson is narrow and worth keeping: **a PR's gate result is only meaningful on
`main + this PR's changed paths`.** Branch snapshots answer a different question.

### Two crates in this workspace are used by nobody

This is the finding that explains the completion percentages better than any line count.

```
agent-integration    used by: NOBODY     production deps: NONE
bmcp-protocol        used by: NOBODY     production deps: NONE
memory-compiler      used by: brain-cli
```

`crates/brain-cli/src/main.rs` is the only executable entry point in the workspace. It
imports `memory_domain`, `memory_storage_sqlite`, `memory_store`, `memory_context` and
`memory_compiler`. It does **not** import `agent-integration`. It does **not** import
`bmcp-protocol`.

So the chain that actually executes today is:

```
event -> memory-compiler -> memory-domain -> memory-storage-sqlite -> memory-store -> memory-context -> (stdout)
```

and it stops at `memory-context`. The two crates that represent "delivery to an agent" and
"the wire protocol" are both terminal leaves with no consumer and no production dependency.
They compile, they have 27 and 46 tests respectively, and nothing calls them.

That is not a gap that more tests close. It is a missing edge in the dependency graph, and
it is the highest-value thing in the backlog.

### Measured code size and test count per crate at `665c8869`

| crate | src lines | `#[test]` | consumed by |
|---|---|---|---|
| memory-context | 3468 | 78 | brain-cli |
| memory-compiler | 3032 | 48 | brain-cli |
| memory-storage-sqlite | 1782 | 35 | memory-store |
| memory-event-store-sqlite | 1475 | 29 | memory-context |
| memory-domain | 1059 | 43 | everything |
| bmcp-protocol | 1373 | 46 | **nobody** |
| agent-integration | 514 | 27 | **nobody** |
| memory-store | 670 | 12 | brain-cli |
| brain-cli | 273 | 1 | — (binary) |
| memory-event-store | 123 | 2 | memory-event-store-sqlite |
| memory-storage | 88 | 3 | memory-store |

### Memory Context is further along than its own coverage document implies

`06-memory-context/context-implementation-coverage.md` at this commit records
**9 IMPLEMENTED / 43 PARTIAL / 25 NOT IMPLEMENTED**. The crate has 42 public items
including `ChangeSet`, `apply_change_set`, `commit_change_set`, `plan_rollback`,
`supersede_version`, `assess_sufficiency`, `prepare_delivery_intent` and
`build_context`. The 25 "NOT IMPLEMENTED" rows are mostly about *delivery and
reconciliation* — adapters, attempt ledgers, reconnect, durable cursors — not about the
context engine itself. Reading the percentage as "the engine is 80% missing" would be
wrong; the engine is largely there and the delivery half is not.

### Two open PRs map directly onto the two islands

Neither is merged, and both are the kind of change that closes a structural gap rather
than adding surface:

- **#513** adds `memory-context` as a **dev**-dependency of `agent-integration` and a
  `tests/context_snapshot_delivery.rs` that carries a real `ContextSnapshot` across the
  crate boundary. Measured on `main + #513`: 8 unit + 2 cross-boundary + 19 lifecycle
  tests, all pass. This is the first test in the repository that crosses into
  `agent-integration` from outside it.
- **#512** replaces `request_frozen: bool` with `AssemblyState::{Open, Frozen}` and
  consumes `self` on `freeze`, so freezing can no longer be bypassed by passing `false`.
  Measured on `main + #512`: 32 unit + 19 integration tests, all pass.

The `bool` → typestate change in #512 is the single clearest correctness improvement in the
open queue: a security-relevant check gated by a caller-supplied boolean is not a check.

### What has not changed

- No PR in this repository has an approval. All nine open PRs show `reviews=0`.
- No CI job has started since billing broke. Every check run still carries the
  spending-limit annotation, so every number above is local execution.
- GAP-03 and GAP-05 still have no merged code. #507 is the GAP-05 draft at round 4.
