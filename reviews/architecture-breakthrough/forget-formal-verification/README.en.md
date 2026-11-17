# Forget Protocol Formal Verification Workstream

**Status:** Baseline pinned; research not yet completed.  
**Baseline:** `main@b3c666e67982cb3d3374e759cfb6552c7765aacb` (2026-11-18)  
**Tracking:** [Issue #43](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43)

## Objective

Determine whether Forget, Producer Admission, Derived Registration, Canonical Publication, Retrieval/Delivery, Index/Cache, and Restore/Recovery preserve anti-resurrection safety under concurrency, crashes, retries, stale workers, and restoration. The work is counterexample- and executable-model-first; adding prose specifications is not a substitute for proof.

## Initial evidence boundary

- Issue #43 records unresolved composition of D ForgetFence with Storage visibility linearization, cross-owner publication, Global Forget inventory, and Restore anti-resurrection.
- PR #71 is a role-simulated Storage review proposal for D/I Phase 3.9, not an independent Storage Owner signature or physical validation.
- These are discovery leads only. Re-read exact current sources and pin branch HEAD, path, and Blob SHA. Issue text and PR summaries are not current normative specifications.

## Model scope

Actors: Forget coordinator, Producer, Admission authority, Worker, Queue, Derived registrar, Canonical store, Index, Cache, Retrieval/Delivery, Backup/Restore.

Specify at minimum:
1. authoritative Forget state and linearization point;
2. ordering between Admission and Forget;
3. atomicity boundary for dependency registration and publication;
4. creation, propagation, and validation of fencing epoch/generation;
5. lost ACK, duplicate request, retry, and unknown outcomes;
6. index/cache rebuild, backup restore, and stale task replay;
7. visibility checks and final delivery boundary.

## Candidate invariants (must be refined against normative sources)

- F1 No resurrection: after authoritative revocation, stale work, replay, projection rebuild, or Restore cannot make the target visible again.
- F2 Stale publisher rejection: workers with obsolete epoch/generation cannot publish.
- F3 Admission ordering: Forget and new Producer Admission have an unambiguous serialization order.
- F4 Dependency completeness: every executor capable of producing a derivative is covered by verifiable dependency/revocation constraints before publication.
- F5 Read/delivery suppression: retrieval, cache, context, and adapter delivery cannot bypass revocation.
- F6 Idempotent retry: duplicate Forget, lost ACK, and retry cannot roll back safety state.
- F7 Restore fencing: restored old data is reconciled against the current revocation generation.
- F8 Crash safety: every supported crash point preserves the safety properties above.

## Execution plan

1. Re-read current relevant D/E/I/Storage/F/G/H specifications, models, tests, and PR changes.
2. Build a source ledger: branch, HEAD, path, Blob SHA, evidence class, and read timestamp.
3. Model in TLA+/TLC first; if unavailable, use executable finite-state enumeration and disclose limitations.
4. Check both serial orders for each race; inject crash before/after durable boundaries, lost ACK, duplicate/replay, stale worker, and restore rollback.
5. Preserve shortest counterexamples, model configuration, reproduction commands, and output summaries.
6. Propose minimal remediations assigned to the correct authority; do not modify its contract.

## Evidence levels

Normative specification, static model, model checking, CI tests, physical database fault injection, and deployment/operational validation must be distinguished. No counterexample within a bounded state space is not a production safety proof.

## Restrictions

Read existing Owner-authoritative artifacts only; add models, fixtures, and reports only on this research branch. Do not rewrite D/E/I/Storage authority contracts, merge, deploy, or begin production Runtime implementation. Classify conclusions as DECIDED / CANDIDATE / TO_VALIDATE / UNRESOLVED / REJECTED.

## Acceptance

Deliver a state machine, invariants, executable model, reproducible commands, counterexample catalog, source ledger, remediation proposals, and bilingual conclusions. Explicitly retain every uncovered area as UNRESOLVED.
