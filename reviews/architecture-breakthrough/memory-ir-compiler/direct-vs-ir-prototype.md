# Direct Pipeline vs Memory IR Prototype

- Experiment: MB-IR-001-PROTOTYPE
- Status: SYNTHETIC / REPRODUCIBLE RESEARCH FIXTURE
- Runtime requirement: Python 3.10+, standard library only
- Run: `python3 reviews/architecture-breakthrough/memory-ir-compiler/prototype/memory_ir_prototype.py`

## 1. Experimental design

Both paths consume the same five synthetic experience rows. Four rows are well-formed; one intentionally lacks a source identifier. Two valid rows assert incompatible values for the same subject/predicate/scope over overlapping valid time. Other rows represent a preference and a plan-like intention. The fixture does not call an LLM and does not use production data.

A. Direct: validate a row and immediately map it to a target-like record in one pass.

B. IR: parse into typed candidate nodes; perform structural/type checks; perform semantic validation; lower to a target-like representation; analyze conflicts. IR node IDs derive from stable input digests.

The direct baseline is intentionally compact, not a production-grade competing implementation. The IR path has additional pass boundaries and therefore more bookkeeping. This is a design probe, not a statistically valid benchmark.

## 2. Expected observable results

With the committed fixture and rules:
- 5 input rows; 4 accepted by each path; the malformed row is rejected.
- Both paths propose one overlapping-value conflict and preserve both candidates.
- IR diagnostics localize the missing source to the parse stage and report a stable code.
- Reprocessing the same fixture yields byte-stable IR lowering and diagnostics.
- Editing one row leaves unaffected source nodes' stable IDs unchanged; the changed source and its descendants are invalidated.
- Direct output carries evidence references; IR output carries evidence plus derivation metadata. The prototype does not claim a measured production provenance-completeness gain.
- The IR path uses more passes (three logical phases vs one direct mapping pass) and no model calls. Wall-clock performance is intentionally not reported because this tiny fixture would be misleading.

## 3. Metric interpretation

| Metric | Direct | IR | Interpretation |
|---|---|---|---|
| Provenance completeness | Evidence ref inline; no standardized pass lineage | Evidence + derivation node metadata | IR makes lineage contract explicit; source retention still governed |
| Type validation | Inline required-field checks | Typed node kind + epistemic enum + semantic checks | More localized and extensible diagnostics |
| Conflict detection | Same conservative rule | Same conservative rule on lowered IR | IR itself does not improve conflict semantics |
| Reprocessing determinism | Deterministic fixture mapping | Deterministic IDs and pass output | Model calls require recorded-output replay |
| Incremental processing | No dependency graph in direct fixture | Source digest IDs demonstrate unchanged-node reuse | Persistent cache/invalidation is not implemented |
| Schema evolution | No version marker | IR version marker | Migration/compatibility not implemented |
| Error localization | Row-level missing-field list | Stage/code/row/node diagnostics | Clearer stage attribution |
| Processing cost | Fewer passes | More passes and metadata | Overhead is real; no wall-time conclusion |
| Data loss | Invalid row rejected | Invalid row rejected with diagnostic; raw input remains fixture | IR does not make invalid content valid |

## 4. Results boundary

The script prints exact counts and output records. Expected counts above are derived from the fixed dataset and algorithm; they are not production-quality proof, quality estimates, or evidence of model extraction performance. The prototype does not test entity resolution, real incremental persistence, concurrency, crash recovery, canonical commit, Forget, authorization, external source availability, or high-volume cost.

## 5. Reproduction and extension

Run the command above from the repository root. The output JSON is deterministic for a fixed Python implementation and fixture. To extend the experiment, add property-based tests for interval overlap, schema upgrades, node invalidation, provenance graph closure, malformed inputs, and cross-scope rejection before comparing performance on an approved anonymized corpus.
