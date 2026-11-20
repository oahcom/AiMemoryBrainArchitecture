# REQ-02 Evidence: SQLite FTS5 vs unindexed LIKE scan

- Evidence ID: REQ02-LEXICAL-BENCH-001
- Requirement: REQ-02 / Issue #263
- Status: **CANDIDATE EVIDENCE — NOT A TECHNOLOGY DECISION**
- Baseline: `main@927eadcb1a8ee94cf533491823373b5ce5f4e204`
- Blueprint input: TAB-001 §4.3, Blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- Executable: [`benchmarks/req02/fts5_vs_like.py`](../../../benchmarks/req02/fts5_vs_like.py)
- Captured result: [`benchmarks/req02/results-2026-11-20.json`](../../../benchmarks/req02/results-2026-11-20.json)

## Question

For the first local lexical-retrieval path, what is the measured query-path difference between SQLite FTS5 and a no-index exact-token scan using SQL `LIKE` over the same corpus?

This is a narrow comparison of an embedded full-text index against the simplest no-index baseline. It is not a comparison against Tantivy or another external search product, and it does not decide whether FTS5 is accepted for the product.

## Method

The executable uses only Python's standard library and the linked SQLite FTS5 implementation. It creates a temporary SQLite database, a deterministic synthetic corpus, an FTS5 external-content table using the `unicode61` tokenizer, and a LIKE scan over the same padded token text.

Reproduction command:

```bash
python3 -m py_compile benchmarks/req02/fts5_vs_like.py
python3 benchmarks/req02/fts5_vs_like.py --output benchmarks/req02/results-2026-11-20.json
```

Run parameters: 12,000 documents; 500-token vocabulary; 40 unique tokens per document; seed `20261120`; 100 deterministic queries; 25 warm-up queries per path; 300 measured queries per path. The script checks exact ordered result-set equality for all 100 queries before timing.

## Actual local result

Environment: Python 3.13.5; SQLite 3.46.1; Linux x86_64.

| Metric | SQLite FTS5 | SQL LIKE scan |
|---|---:|---:|
| P50 | 295.74 μs | 10,271.94 μs |
| P95 | 445.75 μs | 12,259.60 μs |
| P99 | 561.48 μs | 13,743.61 μs |
| Mean | 322.01 μs | 10,491.69 μs |
| Throughput | 3,105.54 queries/s | 95.31 queries/s |

- Result-set parity: **100/100 queries identical**.
- Mean-latency ratio (LIKE / FTS5): **32.58×**.
- Query plan: FTS5 reports `SCAN docs_fts VIRTUAL TABLE INDEX 0:M1`; LIKE reports `SCAN docs`.

The captured values are one actual run, not a statistical claim about production workloads. Re-running on another machine or under different cache/load conditions will produce different timings.

## Interpretation and limits

This run is evidence that, for this exact-token synthetic workload, SQLite FTS5 materially outperforms a no-index table scan while returning the same result sets. It supports keeping FTS5 as a leading candidate for the initial colocated lexical channel in TAB-001 §4.3.

It does **not** establish:
- performance of the Rust `memory-storage-sqlite` adapter or a product runtime;
- end-to-end retrieval quality, ranking relevance, scope/permission enforcement, Forget suppression, or authorization safety;
- write/update/delete throughput, concurrent-reader/writer behavior, crash recovery, index rebuild cost, storage growth, or operational maintenance;
- superiority over Tantivy or any other mature search engine;
- an approved technology choice, ADR, or Owner acceptance.

The LIKE baseline is intentionally a no-index comparison, not a separate mature product. A decision between FTS5 and Tantivy requires a comparable executable benchmark with equivalent tokenization, query semantics, result-set correctness, corpus, and workload. The present evidence must remain `CANDIDATE`.

## Provenance and verification

- Prompt provenance: T2 instruction supplied in the current ChatGPT conversation; Prompt ID `REQ02-LEXICAL-BENCH-PROMPT` v1. Session UUID/permalink are not exposed by this interface; SHA-256 of the raw chat instruction is `NOT_VERIFIED`. No synthetic provenance identifier is claimed.
- Script SHA-256: `0e5899406f1fde296e4e23020f317cd6e4d23ddccd14cccefe7ffdf940ec4227`.
- Captured result SHA-256: `d759ffd9c2ddbe8b37aec9723cf55f807ff4cb8181132a7d3f4b0b6f4f91b834`.
- Local verification: `python3 -m py_compile` exit 0; benchmark exit 0; 100/100 result-set parity checks passed.
- Execution classification: `LOCAL_ONLY`; this is Python `sqlite3`, not native Rust execution and not CI.
