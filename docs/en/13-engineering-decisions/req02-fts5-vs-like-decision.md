# ADR-REQ02-LEXICAL-001 — Select SQLite FTS5 for the Initial Local Lexical Channel

- Decision ID: ADR-REQ02-LEXICAL-001
- Requirement: REQ-02 / Issue #263
- Status: **ACCEPTED — BOUNDED INITIAL-RELEASE DECISION**
- Decision date: 2026-11-20
- Decision authority: USER-PRINCIPAL-DELEGATED, exercised under the delegation instrument recorded in Issue #305, comment 7042461592; this record does not claim a separate human signature.
- Supersedes: none
- Complements: TAB-001 v0.1 §4.3; DOC-TEC-001 v1.0 §4; benchmark REQ02-LEXICAL-BENCH-001.
- Scope: the first colocated lexical full-text retrieval channel in the local-first initial release only. This is not a system-wide search, vector retrieval, database, or production deployment freeze.

## 1. Context

TAB-001 §4.3 identifies SQLite FTS5 as the recommended first comparison for a colocated lexical channel and Tantivy as a candidate when indexing throughput, ranking control, tokenization, or corpus scale justify a separate Rust index. The merged executable evidence compares FTS5 with an unindexed SQL `LIKE` scan on the same deterministic synthetic corpus.

The benchmark is intentionally narrow. It establishes a measurable baseline for the simplest no-index alternative; it does not compare FTS5 with Tantivy or establish product-level retrieval correctness.

## 2. Decision

**Select SQLite FTS5 as the initial local lexical full-text index**, colocated with the SQLite storage authority, behind the retrieval/index interface.

This selection is bounded by the following mandatory conditions:

1. Canonical Memory remains authoritative. FTS5 is derived, rebuildable data and must never become the source of truth.
2. Scope and Permission filtering must be enforced before unauthorized candidates can influence ranking, summaries, or context.
3. Query visibility must apply authoritative Forget/suppression checks; stale or behind-fence index state must fail closed.
4. Index updates must follow committed canonical changes and expose an explicit index watermark distinct from CanonicalCommitCursor and ForgetFenceGeneration.
5. Rebuild must consume canonical history plus current Forget state and must not resurrect suppressed content.
6. The production Rust adapter must pass migration, update/delete, restart/rebuild, authorization, and Forget-race tests before this channel is treated as production-ready.

## 3. Alternatives and disposition

| Alternative | Disposition | Reason and evidence boundary |
|---|---|---|
| SQLite FTS5 | **SELECTED** for the bounded initial lexical channel | The executable comparison returned identical ordered result sets for 100/100 deterministic queries and measured mean latency 322.01 μs versus 10,491.69 μs for no-index LIKE (32.58× ratio) on the recorded synthetic warm-cache workload. It is colocated with the selected local SQLite direction and avoids a separate index service/process. |
| SQL `LIKE` full-table scan without a full-text index | **REJECTED** as the normal production lexical path; retained as a tiny-data fallback and regression baseline only | Same 100/100 results in the benchmark, but mean latency was 32.58× higher and the query plan scanned `docs` rather than using a full-text index. The evidence supports rejecting this no-index path for the measured workload, not rejecting all SQL filtering or indexed LIKE use. |
| Tantivy | **DEFERRED — NOT REJECTED** | TAB-001 already lists it as a candidate for higher indexing throughput, ranking control, tokenization, or corpus scale. No comparable FTS5-vs-Tantivy benchmark, adapter integration evidence, or operational comparison is present. Claiming it inferior would exceed the evidence. Reopen this decision if measured requirements trigger a comparable evaluation. |
| PostgreSQL full-text search or an external search service | **NOT SELECTED / OUT OF THIS DECISION** | Adds a separate service or operational boundary not justified by the current local-first requirement. No same-workload comparative evidence exists here; this is a scope/complexity decision, not a measured performance rejection. |

## 4. Evidence

Source: PR #361, merged at `1cf71dffb2a64494439c2d2562a0a1fb5dffd3e1`; exact pre-merge head `6b7ea2202b26548464b2605d0dad4805096deb1e`.

Main Blob SHAs:

- Benchmark executable `benchmarks/req02/fts5_vs_like.py`: `28b27557bbaf3e63995db356b81ebbf484a5ae14`
- Captured result `benchmarks/req02/results-2026-11-20.json`: `c688f7ef5f43ba0ec76efbbdf2e6dc5d168bd0f2`
- English benchmark report: `12ed3d68113d8204b43179ba2b4efbacdffc992f`
- Chinese benchmark report: `6a6d5952840588ac821ab7687d416682a56a3032`

Recorded run (Python 3.13.5, SQLite 3.46.1, Linux x86_64):

| Metric | FTS5 | LIKE scan |
|---|---:|---:|
| P50 | 295.74 μs | 10,271.94 μs |
| P95 | 445.75 μs | 12,259.60 μs |
| P99 | 561.48 μs | 13,743.61 μs |
| Mean | 322.01 μs | 10,491.69 μs |
| Throughput | 3,105.54 q/s | 95.31 q/s |

100/100 ordered result sets matched. Mean latency ratio: 32.58×. FTS5 query plan used `docs_fts` virtual-table index; LIKE plan scanned `docs`.

## 5. Known limitations and explicit non-claims

The benchmark is LOCAL_ONLY Python `sqlite3`, not native Rust adapter execution, not CI, and not end-to-end product evidence. It uses a synthetic exact-token workload and does not establish:

- CJK segmentation quality, tokenizer suitability for production multilingual corpora, ranking relevance, or user-visible search quality;
- write/update/delete churn, concurrent readers/writers, crash recovery, index rebuild cost, storage growth, or maintenance cost;
- Scope/Permission enforcement, Forget suppression, anti-resurrection, or authorization safety;
- superiority over Tantivy or any other mature search product.

The CI attempt associated with PR #361 is not represented as PASS: Run `44749692316`, job `136334035195`, returned `steps=[]`; log retrieval returned HTTP 404 `BlobNotFound` (RequestId `226d976d-001e-00b7-45f8-78b640000000`). This is platform infrastructure evidence; the local benchmark remains LOCAL_ONLY.

## 6. Reconsideration triggers

Reopen this ADR when any of the following is demonstrated with a reproducible workload:

- the Rust adapter cannot meet correctness, migration, or operational requirements with FTS5;
- representative multilingual relevance/tokenization requirements cannot be met;
- indexing throughput, corpus size, concurrent update pressure, or rebuild time exceeds an agreed measured envelope;
- a comparable FTS5-vs-Tantivy evaluation demonstrates a material advantage after equalizing tokenizer, query semantics, corpus, result correctness, and workload;
- the system changes from the bounded local-first deployment assumption.

Any reconsideration must preserve canonical authority, Scope/Permission-first filtering, Forget anti-resurrection, and rebuildability.

## 7. Consequences

**Positive:** a single-node initial lexical channel is selected with a traceable, reproducible baseline; no separate search service is required.

**Negative / accepted costs:** FTS5 tokenizer and ranking behavior become a bounded dependency; index maintenance, migrations, rebuilds, and correctness gates remain implementation responsibilities.

**Not decided here:** vector retrieval, database authority, Tantivy adoption, ranking policy, production readiness, and system-wide technology freeze.

## 8. Provenance

- Prompt/source: current ChatGPT user instruction requesting the REQ-02 formal selection decision and rejected-alternative reasons; conversation session UUID/permalink and raw instruction bytes are not exposed by this interface. SHA-256: `NOT_VERIFIED`. No synthetic source identifier or hash is claimed.
- Governance loaded from main: AI-EXEC-001 v1.1 ADOPTED, Blob `58af59af266b81109269156ea667df1a15edfb7b`; AI-EXEC-002 v1.2 PENDING ADOPTION, Blob `7f5928a5d16eb12da7621cfb8bd99ca463afd859` (v1.1 remains adopted).
