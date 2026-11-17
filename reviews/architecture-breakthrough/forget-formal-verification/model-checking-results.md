# Model Checking Results

## Method

TLA+/TLC was not available through the connected repository workflow. A Python 3 explicit-state breadth-first enumerator was implemented instead. It explores interleavings of abstract actions and reports shortest counterexamples for deliberately weakened protocol variants.

Run:

    python3 model/forget_model.py

Expected output:

    SAFE MODEL: no counterexample through depth 10 (606 state/depth pairs)
    COUNTEREXAMPLE stale_worker: admit -> install_fence -> publish
    COUNTEREXAMPLE admission_race: install_fence -> admit
    COUNTEREXAMPLE stale_index: admit -> publish -> install_fence -> rebuild_index
    COUNTEREXAMPLE stale_cache: admit -> publish -> install_fence -> repopulate_cache
    COUNTEREXAMPLE stale_restore: install_fence -> restore
    ACK-LOSS RETRY: durable receipt and terminal state remain monotonic
    MODEL CHECK COMPLETE (bounded abstraction only)

## Explored state space

- One canonical object and one source lineage.
- One producer/work item and one publication.
- One Forget generation.
- One index projection and one cache projection.
- One terminalization/receipt and one restore.
- 12 abstract actions: admission, Fence install, publish, retry publish, index rebuild, cache refill, barrier close, terminalize, receipt persistence, ACK loss, Forget retry and restore.
- Safe transition graph: 606 distinct state/depth pairs through depth 10; no modeled invariant violation.
- Five mutant variants produce the shortest traces in counterexample-catalog.md.

## Assumptions for the safe result

1. Fence generation is durable, monotonic and authoritative.
2. Admission and Fence installation are linearizable in one ordering domain.
3. Final publication checks current Fence and lineage in the same atomic visibility boundary.
4. Read paths enforce current Fence even if stale bytes remain in indexes/caches.
5. Barrier membership is durable and unknown work blocks closure.
6. Restore cannot release service before current control high-waters are replayed and revalidated.
7. Receipt identity and request digest are immutable; ACK loss changes caller knowledge, not durable state.

## Not modeled

Multiple objects/scopes/tenants/policy domains; arbitrary dependency DAGs; multiple workers, lease epochs, DLQ and replay; MVCC anomalies, WAL durability, replication lag, split brain or real prepared transactions; real index/cache/Context/Adapter implementations; crypto, authorization and key rotation; crash injection at every persistence instruction; Temporal semantics; actual PITR/pg_rewind.

The safe result is conditional on assumptions. It does not validate existing Owner test suites or prove that proposed runtime realizes these assumptions.
