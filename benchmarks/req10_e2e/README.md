# REQ-10 integrated workload benchmark harness

**Status: development baseline only. Integrated product-runtime measurements: NOT_MEASURED.**

The repository README states that the product-level runtime has not started. This directory therefore delivers the reusable harness contract and a deterministic protocol fixture; it does not claim an end-to-end product-runtime benchmark. The fixture is not a substitute for the runtime.

## Representative workload contract

Selected critical path: one representative memory-ingest request that traverses **ingest → compile/normalize → retrieve → context-package assembly**. An integrated adapter must execute the real product path for each request. It must not route to the PR #355 SQLite mirror.

Default dataset shape (override with CLI flags): 1,000 input records, 100 canonical memories, 3 claims per memory (approximately 300 claims). Concurrency: one serial client. Default run: 10 warm-up requests discarded, then 100 measured requests. The adapter remains alive across all requests so startup is outside each request's latency.

The dataset values are workload descriptors sent in each JSONL request. The integrated adapter is responsible for provisioning the corresponding deterministic dataset and storage state before the run; this harness does not invent or seed product records.

## Adapter protocol

`benchmark.py --command '<adapter command>'` starts one long-lived child process. Each request is one JSON line on stdin; the adapter must return exactly one JSON object line on stdout. The request includes `workload`, `phase`, `operation_index`, `dataset`, and `concurrency`.

Optional response fields:
- `stage_ms`: object mapping stage names to numeric milliseconds. These are adapter-reported stage durations, not independently instrumented by the harness.
- `model_metrics`: object with all four numeric fields `calls`, `input_tokens`, `output_tokens`, and `cost_usd`. If any measured response omits this object or a field, model/token/cost totals are `NOT_MEASURED`.

The adapter must send diagnostics to stderr, not stdout. Exit non-zero to fail the run. No shell is used; `--command` is tokenized with `shlex`.

## Reproducible invocation

From the repository root, Python 3.10+:

```sh
python3 benchmarks/req10_e2e/benchmark.py \
  --command "python3 -u benchmarks/req10_e2e/fixture_runtime.py" \
  --samples 100 --warmup 10 --concurrency 1 \
  --records 1000 --memories 100 --claims-per-memory 3 \
  --report /tmp/req10-e2e-dev-baseline.json
```

For a real integrated runtime, replace only the fixture command with the product adapter implementing the JSONL protocol, provision the dataset described above, and pass `--storage-path` pointing at the runtime's storage directory. The harness deliberately does not supply a product adapter because no integrated runtime is present.

## Attribution semantics

- Latency P50/P95/P99 is measured at the request boundary, in milliseconds. Throughput is measured requests divided by summed measured request wall time; the harness is serial (`concurrency=1`).
- Stage percentiles are emitted only for stage durations returned by the adapter.
- Process CPU seconds and peak RSS are child-process-wide (POSIX `RUSAGE_CHILDREN`); they are not per-operation. Unsupported platforms return `NOT_MEASURED`.
- Storage footprint is the byte sum of the supplied file/directory before and after the run. Without `--storage-path`, it is `NOT_MEASURED`.
- Per-operation CPU, memory, and storage attribution are `NOT_MEASURED`; no division of process-wide values is presented as an operation measurement.
- Model calls, tokens, and cost are summed only when every measured response returns the complete `model_metrics` object. Otherwise all are `NOT_MEASURED`.

## Local verification record

A 100-sample/10-warm-up fixture execution was run with Python 3.13.5 on Linux. The captured output is committed as [dev-fixture-report.json](dev-fixture-report.json). It records fixture-only latency, throughput, process CPU, and peak RSS; storage, per-operation attribution, and model/token/cost are `NOT_MEASURED`. **None of these values are integrated-runtime measurements or product performance evidence.** The report's `integrated_runtime` field remains `NOT_MEASURED` by design.

PR #355 remains a separate SQLite commit carrier. Its Python SQL-path mirror results are not imported, combined, or represented here.

## Deferred

No production SLO, capacity commitment, infrastructure expansion, optimization decision, backpressure/degradation design, or regression threshold is introduced. These require representative integrated-runtime measurements and variance evidence first.
