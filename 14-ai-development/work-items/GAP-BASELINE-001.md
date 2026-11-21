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
