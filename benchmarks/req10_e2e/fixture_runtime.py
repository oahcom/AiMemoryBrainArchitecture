#!/usr/bin/env python3
"""Deterministic protocol fixture; NOT an integrated product runtime."""
import json
import sys
import time

for line in sys.stdin:
    request = json.loads(line)
    if request.get("phase") == "shutdown":
        break
    # Simulate a small multi-stage path solely to exercise harness accounting.
    start = time.perf_counter()
    records = request["dataset"]["records"]
    memories = request["dataset"]["memories"]
    claims = request["dataset"]["approx_claims"]
    # Bounded deterministic CPU work; never accesses product storage or a model.
    checksum = sum((i * 17) % 101 for i in range(min(records + memories + claims, 20000)))
    total = (time.perf_counter() - start) * 1000.0
    response = {
        "stage_ms": {
            "ingest": total * 0.30,
            "compile": total * 0.25,
            "retrieve": total * 0.25,
            "context_package": total * 0.20,
        },
        "fixture_checksum": checksum,
    }
    print(json.dumps(response), flush=True)
