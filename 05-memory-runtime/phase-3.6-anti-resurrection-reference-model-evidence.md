# F Phase 3.6 — Anti-Resurrection Logical Reference Model Evidence

- Branch: `session-f-memory-runtime`
- Branch HEAD: `f1ba5c478e395da6b126423e32e20d0990e61920`
- Model: `tests/anti_resurrection/f_runtime_model.py`, Blob `33fa2ca2dc29771aca241e194f13e078a4f8d774`
- Tests: `tests/anti_resurrection/test_f_runtime_model.py`, Blob `c2575327a75577923440ef770d42122218a1e091`
- Workflow: `.github/workflows/f-anti-resurrection-reference-model.yml`, Blob `c0fac9eff93ca46e466cda5fe04613bd4565e9b3`
- CI run: `43961714501`
- Job: `133630540252`
- Run commit: `f1ba5c478e395da6b126423e32e20d0990e61920`
- Result: **19/19 TESTS PASS**

## 1. Covered logical invariants

1. Current D fence suppresses stale index candidates.
2. A targeted Forget does not expose the affected item and does not unnecessarily suppress an unrelated authorized index entry.
3. A cache shard that missed an invalidation notification cannot serve a stale hit; stale generation is evicted.
4. An in-flight cache fill started before Forget cannot publish after the fence changes.
5. Rebuilding from a pre-Forget snapshot cannot resurrect a fenced item.
6. Incomplete watermark/coverage or non-contiguous replay blocks retrieval.
7. Missing I/D authoritative state blocks retrieval and cache access; stale is not downgraded to miss.
8. Scope and Environment filtering occurs before ranking/count exposure.
9. Stale PermissionEpoch blocks old entries.
10. Reconnect clears the old Working Set before restore and requires fresh I/D authority plus reconciled invalidation checkpoint.
11. Same invalidation identity/digest is idempotent; changed digest conflicts.
12. Cache key binds principal, issuer, policy domain, Scope, Environment, PermissionEpoch, ForgetFence generation, MemoryVersion, partition, query and config.
13. F target evidence is local only and cannot claim I global completion.

## 2. Exact CI result

The workflow compiled the model and test suite and ran `python -m unittest discover -v`. The raw log reports 19 tests in 0.002 seconds and `OK`. Workflow run `43961714501` concluded SUCCESS.

## 3. Limits

This is an in-memory deterministic logical reference model, not a production index/cache/Working Set implementation. It does not execute concurrent threads/processes, real index partitions, ANN pre-filter, storage transactions, adapter reconnect, network partitions, I/D service APIs, external targets, backup restore or cryptographic authentication. F-RT-01..13 remain SPECIFIED / NOT RUN for the actual runtime. The model closes a logical regression-evidence gap only; it does not certify Anti-Resurrection or Global Forget completion.