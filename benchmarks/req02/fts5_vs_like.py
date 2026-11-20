#!/usr/bin/env python3
"""Reproducible SQLite FTS5 vs unindexed LIKE scan benchmark.

This is a retrieval-path microbenchmark, not a product/runtime benchmark.
It compares identical exact-token result sets over one deterministic corpus:
  * FTS5: SQLite's built-in unicode61 full-text index.
  * LIKE: a full table scan using a space-delimited exact-token predicate.

Only Python's standard library is required. FTS5 must be enabled in the linked
SQLite build. Run: python3 fts5_vs_like.py --output results.json
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import random
import sqlite3
import statistics
import tempfile
import time
from pathlib import Path


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    rank = (len(ordered) - 1) * p
    lo = int(rank)
    hi = min(lo + 1, len(ordered) - 1)
    frac = rank - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def make_corpus(documents: int, vocab_size: int, tokens_per_doc: int, seed: int):
    rng = random.Random(seed)
    vocab = [f"term{n:05d}" for n in range(vocab_size)]
    rows = []
    for doc_id in range(1, documents + 1):
        terms = rng.sample(vocab, tokens_per_doc)
        rows.append((doc_id, " " + " ".join(terms) + " "))
    query_rng = random.Random(seed ^ 0x5A17)
    queries = [vocab[query_rng.randrange(vocab_size)] for _ in range(100)]
    return rows, queries


def run(args: argparse.Namespace) -> dict:
    if args.tokens_per_doc > args.vocab_size:
        raise ValueError("tokens-per-doc must not exceed vocab-size")
    rows, queries = make_corpus(args.documents, args.vocab_size, args.tokens_per_doc, args.seed)
    tmp = tempfile.NamedTemporaryFile(prefix="req02-fts5-", suffix=".sqlite", delete=False)
    db_path = tmp.name
    tmp.close()
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode=OFF")
        conn.execute("PRAGMA synchronous=OFF")
        conn.execute("CREATE TABLE docs (doc_id INTEGER PRIMARY KEY, body TEXT NOT NULL)")
        conn.executemany("INSERT INTO docs(doc_id, body) VALUES (?, ?)", rows)
        conn.execute("CREATE VIRTUAL TABLE docs_fts USING fts5(body, content='docs', content_rowid='doc_id', tokenize='unicode61')")
        conn.execute("INSERT INTO docs_fts(docs_fts) VALUES ('rebuild')")
        conn.commit()

        fts5_plan = conn.execute(
            "EXPLAIN QUERY PLAN SELECT rowid FROM docs_fts WHERE docs_fts MATCH ?",
            (queries[0],),
        ).fetchall()
        like_plan = conn.execute(
            "EXPLAIN QUERY PLAN SELECT doc_id FROM docs WHERE body LIKE ?",
            (f"% {queries[0]} %",),
        ).fetchall()

        def fts(q: str) -> list[int]:
            return [r[0] for r in conn.execute(
                "SELECT rowid FROM docs_fts WHERE docs_fts MATCH ? ORDER BY rowid", (q,)
            )]

        def like(q: str) -> list[int]:
            return [r[0] for r in conn.execute(
                "SELECT doc_id FROM docs WHERE body LIKE ? ORDER BY doc_id", (f"% {q} %",)
            )]

        parity_checked = 0
        result_counts = []
        for q in queries:
            a, b = fts(q), like(q)
            if a != b:
                raise AssertionError(f"result mismatch for {q}: FTS5={len(a)} LIKE={len(b)}")
            parity_checked += 1
            result_counts.append(len(a))

        for i in range(args.warmup):
            q = queries[i % len(queries)]
            fts(q)
            like(q)

        fts_times: list[float] = []
        like_times: list[float] = []
        for i in range(args.iterations):
            q = queries[i % len(queries)]
            start = time.perf_counter_ns()
            fts(q)
            fts_times.append((time.perf_counter_ns() - start) / 1_000.0)
            start = time.perf_counter_ns()
            like(q)
            like_times.append((time.perf_counter_ns() - start) / 1_000.0)

        def summary(samples: list[float]) -> dict:
            total_s = sum(samples) / 1_000_000.0
            return {
                "p50_us": round(percentile(samples, 0.50), 2),
                "p95_us": round(percentile(samples, 0.95), 2),
                "p99_us": round(percentile(samples, 0.99), 2),
                "mean_us": round(statistics.fmean(samples), 2),
                "throughput_queries_per_s": round(len(samples) / total_s, 2) if total_s else None,
            }

        conn.close()
        return {
            "benchmark": "REQ-02 SQLite FTS5 vs unindexed LIKE exact-token scan",
            "classification": "LOCAL_ONLY_MICROBENCHMARK_NOT_PRODUCT_RUNTIME",
            "environment": {
                "python": platform.python_version(),
                "sqlite": sqlite3.sqlite_version,
                "platform": platform.platform(),
                "machine": platform.machine(),
            },
            "parameters": {
                "documents": args.documents,
                "vocab_size": args.vocab_size,
                "tokens_per_document": args.tokens_per_doc,
                "warmup_queries_per_path": args.warmup,
                "measured_queries_per_path": args.iterations,
                "seed": args.seed,
                "query_count": len(queries),
            },
            "correctness": {
                "queries_compared": parity_checked,
                "result_sets_identical": True,
                "mean_results_per_query": round(statistics.fmean(result_counts), 2),
            },
            "latency": {
                "fts5": summary(fts_times),
                "like_scan": summary(like_times),
                "fts5_speedup_by_mean": round(
                    statistics.fmean(like_times) / statistics.fmean(fts_times), 2
                ),
            },
            "query_plans": {
                "fts5": [str(r) for r in fts5_plan],
                "like_scan": [str(r) for r in like_plan],
            },
            "limitations": [
                "Synthetic deterministic corpus; not representative of production memory distributions.",
                "Single-process, warm-cache, read-only microbenchmark; no concurrent writers or update/delete churn.",
                "LIKE is a no-index exact-token baseline, not a separate search product.",
                "Measures Python sqlite3 call path; does not measure the Rust adapter or end-to-end retrieval quality.",
                "No relevance ranking, scope filtering, authorization, Forget suppression, or index rebuild cost is measured.",
            ],
        }
    finally:
        try:
            os.unlink(db_path)
        except FileNotFoundError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--documents", type=int, default=12000)
    parser.add_argument("--vocab-size", type=int, default=500)
    parser.add_argument("--tokens-per-doc", type=int, default=40)
    parser.add_argument("--warmup", type=int, default=25)
    parser.add_argument("--iterations", type=int, default=300)
    parser.add_argument("--seed", type=int, default=20261120)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if min(args.documents, args.vocab_size, args.tokens_per_doc, args.iterations) <= 0 or args.warmup < 0:
        parser.error("documents, vocab-size, tokens-per-doc and iterations must be positive; warmup must be non-negative")
    result = run(args)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
