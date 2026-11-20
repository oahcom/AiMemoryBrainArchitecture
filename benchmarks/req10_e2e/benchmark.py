#!/usr/bin/env python3
"""JSONL subprocess benchmark harness; stdlib only, Linux/macOS resource attribution."""
from __future__ import annotations

import argparse
import json
import math
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("empty sample")
    rank = (len(ordered) - 1) * p
    lo = math.floor(rank)
    hi = math.ceil(rank)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - rank) + ordered[hi] * (rank - lo)


def storage_bytes(path: Path | None) -> int | None:
    if path is None or not path.exists():
        return None
    if path.is_file():
        return path.stat().st_size
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def child_usage():
    try:
        import resource
        r = resource.getrusage(resource.RUSAGE_CHILDREN)
        return (r.ru_utime + r.ru_stime, r.ru_maxrss)
    except (ImportError, AttributeError, OSError):
        return None


def send(proc: subprocess.Popen, payload: dict) -> dict:
    assert proc.stdin is not None and proc.stdout is not None
    proc.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
    proc.stdin.flush()
    line = proc.stdout.readline()
    if not line:
        stderr = proc.stderr.read() if proc.stderr else ""
        raise RuntimeError(f"adapter exited before response (rc={proc.poll()}): {stderr}")
    result = json.loads(line)
    if not isinstance(result, dict):
        raise RuntimeError("adapter response must be a JSON object")
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--command", required=True, help="adapter command; JSONL request on stdin, one JSON response per line")
    ap.add_argument("--samples", type=int, default=100, help="measured operations (default: 100)")
    ap.add_argument("--warmup", type=int, default=10, help="discarded warm-up operations (default: 10)")
    ap.add_argument("--concurrency", type=int, default=1, help="declared client concurrency; this harness currently requires 1")
    ap.add_argument("--records", type=int, default=1000, help="records in representative dataset")
    ap.add_argument("--memories", type=int, default=100, help="memories in representative dataset")
    ap.add_argument("--claims-per-memory", type=int, default=3)
    ap.add_argument("--storage-path", type=Path, help="runtime storage directory/file to attribute")
    ap.add_argument("--report", type=Path, default=Path("benchmark-report.json"))
    args = ap.parse_args()

    if args.samples < 1 or args.warmup < 0 or args.concurrency != 1:
        ap.error("samples >= 1, warmup >= 0, and concurrency == 1 are required")
    if min(args.records, args.memories, args.claims_per_memory) < 0:
        ap.error("dataset dimensions must be non-negative")

    before_storage = storage_bytes(args.storage_path)
    before_usage = child_usage()
    command = shlex.split(args.command)
    if not command:
        ap.error("--command must not be empty")

    latencies_ms: list[float] = []
    stages: dict[str, list[float]] = {}
    model_calls = input_tokens = output_tokens = 0
    costs: list[float] = []
    model_metrics_complete = True
    wall_start = time.perf_counter()
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, bufsize=1)
    try:
        for i in range(args.warmup + args.samples):
            phase = "warmup" if i < args.warmup else "measure"
            payload = {
                "workload": "representative_memory_ingest_compile_retrieve_context",
                "phase": phase,
                "operation_index": i,
                "dataset": {
                    "records": args.records,
                    "memories": args.memories,
                    "claims_per_memory": args.claims_per_memory,
                    "approx_claims": args.memories * args.claims_per_memory,
                },
                "concurrency": args.concurrency,
            }
            start = time.perf_counter()
            result = send(proc, payload)
            elapsed = (time.perf_counter() - start) * 1000.0
            if phase == "warmup":
                continue
            latencies_ms.append(elapsed)
            stage_map = result.get("stage_ms")
            if isinstance(stage_map, dict):
                for name, value in stage_map.items():
                    if isinstance(value, (int, float)):
                        stages.setdefault(str(name), []).append(float(value))
            metrics = result.get("model_metrics")
            if isinstance(metrics, dict) and all(k in metrics for k in
                    ("calls", "input_tokens", "output_tokens", "cost_usd")):
                model_calls += int(metrics["calls"])
                input_tokens += int(metrics["input_tokens"])
                output_tokens += int(metrics["output_tokens"])
                costs.append(float(metrics["cost_usd"]))
            else:
                model_metrics_complete = False
    finally:
        if proc.stdin:
            proc.stdin.close()
    return_code = proc.wait(timeout=30)
    wall_seconds = time.perf_counter() - wall_start
    stderr = proc.stderr.read() if proc.stderr else ""
    if return_code != 0:
        raise RuntimeError(f"adapter exited rc={return_code}: {stderr}")

    after_usage = child_usage()
    after_storage = storage_bytes(args.storage_path)
    cpu_seconds = None
    peak_rss_raw = None
    if before_usage is not None and after_usage is not None:
        cpu_seconds = max(0.0, after_usage[0] - before_usage[0])
        peak_rss_raw = after_usage[1]
    # ru_maxrss is KiB on Linux, bytes on macOS.
    peak_rss_bytes = (peak_rss_raw * (1024 if sys.platform.startswith("linux") else 1)
                      if peak_rss_raw is not None else None)

    measured_wall = sum(latencies_ms) / 1000.0
    report = {
        "classification": "DEV_BASELINE_HARNESS_FIXTURE_OR_UNVERIFIED_ADAPTER",
        "integrated_runtime": "NOT_MEASURED",
        "workload": "representative_memory_ingest_compile_retrieve_context",
        "dataset": {"records": args.records, "memories": args.memories,
                    "claims_per_memory": args.claims_per_memory,
                    "approx_claims": args.memories * args.claims_per_memory},
        "environment": {"python": sys.version.split()[0], "platform": sys.platform,
                        "system": os.uname().sysname if hasattr(os, "uname") else os.name,
                        "command": command},
        "concurrency": args.concurrency,
        "warmup": args.warmup,
        "samples": len(latencies_ms),
        "latency_ms": {"p50": percentile(latencies_ms, .50),
                       "p95": percentile(latencies_ms, .95),
                       "p99": percentile(latencies_ms, .99)},
        "throughput_ops_per_sec": len(latencies_ms) / measured_wall if measured_wall else None,
        "process_wide": {
            "cpu_seconds": cpu_seconds if cpu_seconds is not None else "NOT_MEASURED",
            "peak_rss_bytes": peak_rss_bytes if peak_rss_bytes is not None else "NOT_MEASURED",
            "storage_bytes_before": before_storage if before_storage is not None else "NOT_MEASURED",
            "storage_bytes_after": after_storage if after_storage is not None else "NOT_MEASURED",
        },
        "per_operation": {
            "cpu_seconds": "NOT_MEASURED",
            "peak_memory_bytes": "NOT_MEASURED",
            "storage_bytes": "NOT_MEASURED",
        },
        "stage_latency_ms": {k: {"p50": percentile(v, .50), "p95": percentile(v, .95),
                                  "p99": percentile(v, .99)} for k, v in stages.items()},
        "model_metrics": ({"calls": model_calls, "input_tokens": input_tokens,
                           "output_tokens": output_tokens, "cost_usd": sum(costs)}
                          if model_metrics_complete and len(costs) == len(latencies_ms)
                          else "NOT_MEASURED"),
        "notes": [
            "Harness execution is not evidence of an integrated product-runtime path.",
            "Process CPU and peak RSS are child-process-wide; no per-operation attribution is inferred.",
            "Stage timings are adapter-reported and only included when returned.",
            "Storage footprint is directory/file bytes before and after; absent path is NOT_MEASURED.",
            "Throughput uses summed measured request wall time; serial concurrency is 1.",
        ],
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("classification=DEV_BASELINE_HARNESS_FIXTURE_OR_UNVERIFIED_ADAPTER")
    print("integrated_runtime=NOT_MEASURED")
    print(f"samples={len(latencies_ms)} warmup={args.warmup} concurrency={args.concurrency} dataset=records:{args.records},memories:{args.memories},claims_per_memory:{args.claims_per_memory}")
    print("latency_ms p50={:.3f} p95={:.3f} p99={:.3f}".format(
        percentile(latencies_ms, .50), percentile(latencies_ms, .95), percentile(latencies_ms, .99)))
    print("throughput_ops_per_sec={:.3f}".format(len(latencies_ms) / measured_wall))
    print("process_cpu_seconds={} peak_rss_bytes={}".format(
        cpu_seconds if cpu_seconds is not None else "NOT_MEASURED",
        peak_rss_bytes if peak_rss_bytes is not None else "NOT_MEASURED"))
    print("storage_bytes_before={} storage_bytes_after={}".format(
        before_storage if before_storage is not None else "NOT_MEASURED",
        after_storage if after_storage is not None else "NOT_MEASURED"))
    print("per_operation_cpu=NOT_MEASURED per_operation_memory=NOT_MEASURED model_tokens_cost={}".format(
        "measured" if model_metrics_complete and len(costs) == len(latencies_ms) else "NOT_MEASURED"))
    print(f"report={args.report}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
