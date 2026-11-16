# E — Memory Compiler Technology Architecture Review

- Document: TAR-E-001
- Owner perspective: E — Memory Compiler Architect
- Execution mode: centralized delegated review by the project integration assistant; not an independent human-owner attestation.
- Branch: `session-e-memory-compiler-2026-11-16`
- Reviewed branch HEAD: `4402549c39824b89a0dc49973226187c62e056c5`
- TAB-001 blob: `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- E compiler state/admission contract blob: `e59f517fff161ab882aa0ddc4a5bda513964ae1a`
- E Forget/derived registration contract blob: `00e37ba56596e710513c8d0568acd79141d9101b`
- D Forget fence contract blob: `1f0391bc49d007c44ec74165bd33d37412cc7990`
- D publication gate blob: `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`
- Date: 2026-11-17
- Verdict: **CONDITIONAL PASS — local durable compiler pipeline is viable; publication and recovery remain blocked on Storage realization.**

## 1. Executive verdict

TAB-001's modular Rust host, durable ingress, database-backed outbox/worker model and optional isolated inference worker fit a local-first first release. Kafka-class infrastructure is not justified without measured throughput or multi-host requirements. The compiler must preserve distinct accepted, registered, staged, dependency-registered, published, canonical-committed and terminal evidence.

E's current contracts describe a detailed state machine and private staging rule. D has defined the semantic producer/fence/publication ordering. Neither document proves callable integration or a physical atomic visibility boundary. The most serious remaining issue is the final publish operation and its recovery semantics.

## 2. R1–R6 assessment

| Dimension | Verdict | Evidence and gap | Impact |
|---|---|---|---|
| R1 Requirements/workload | CONDITIONAL | E state contract separates accepted receipt, compile intent, stable WorkItem, run, attempt, lease and immutable artifact. Exact queue throughput, payload and model workload unknown. | Work model is sound but sizing open. |
| R2 Boundaries/dependencies | CONDITIONAL | E owns compiler lifecycle; D owns registration/fence/gate; I auth; Storage visibility; B types; H transport. | Must not let E local state substitute D receipts. |
| R3 Technology selection | CONDITIONAL | DB-backed outbox and workers suit local-first; Tokio/Serde/provider abstractions are candidates. External broker not justified. | Keep technology choices reversible. |
| R4 Resources | NOT MEASURED | CPU/GPU, model batch size, queue age, blob staging, retry amplification and 12–16 GB VRAM contention unmeasured. | Cannot claim throughput or VRAM fit. |
| R5 Recovery | BLOCKED | State machine covers retries/DLQ/lease expiry, but fault matrix is design-only and storage publication gate unverified. | Late derivative/resurrection risk remains. |
| R6 Compatibility | CONDITIONAL | Stable IDs and typed cursors/epochs specified; callable D API, H authenticated envelope, I current auth and B source-reference mappings remain open. | No end-to-end conformance yet. |

## 3. Findings

### TAR-E-P0-001 — Compiler cannot expose derivatives without a proven authoritative publication transaction

- Evidence: E gate blob `00e37ba56596e710513c8d0568acd79141d9101b`; D gate blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`.
- Consequence: local staging or a successful pre-check can be followed by a concurrent Forget fence before visibility; index/context consumers may see an artifact that should remain suppressed.
- Recommendation: all candidate/proposal/embedding/excerpt/provenance edges remain private until D/Storage commits a final PublicationReceipt and visible marker in the same serialization decision that validates current fence, I authorization, WorkItem/Attempt/Lease, full dependency receipts and artifact digest.
- Owners: D/E/Storage/I; F/G/H/C consumers must reject non-visible references.
- Closure: implement same transaction/coordinator and run deterministic publish-vs-fence, dependency-vs-fence and crash/ACK-loss fixtures.

### TAR-E-P0-002 — Durable acceptance and producer admission must be distinct, recoverable steps

AcceptedReceipt proves durable ingress only; it does not prove D registration. Enqueue, lease, source dereference or execution must not occur until D RegistrationReceipt resolves. If ACK is lost, query the same stable WorkItemId and digest; never assume success or create a new barrier identity.

### TAR-E-P1-001 — Idempotency identity hierarchy needs end-to-end enforcement

Preserve EventRef, AcceptedReceiptId, CompileIntentId, ProducerWorkItemId, DerivationRunId, AttemptId, LeaseId, DerivedArtifactRef/version, DependencyRegistrationId and PublicationOperationId. Retry preserves WorkItemId; attempt/lease changes are explicit; recompile creates a new DerivationRunId and cannot escape root barrier. Conflicting digest for same operation identity is an immutable conflict, not an overwrite.

### TAR-E-P1-002 — Outbox, worker lease and DLQ semantics need executable recovery

Use transactional outbox for durable accepted intent. Queue can be database-backed initially; worker lease must have monotonic fencing epoch and expiry. DLQ/queue deletion/worker loss is not terminal while replay remains possible. Define retention and replay authority. External broker deferred unless measured need appears.

### TAR-E-P1-003 — Blob staging and content-addressed identity need integrity/visibility rules

Verify digest, byte length, media type and source provenance before metadata registration. Keep staged objects private; no public object URI, generic listing, cache warm or downstream event before final visibility commit. Reconcile orphan blobs without deleting referenced content.

### TAR-E-P1-004 — Inference is optional and must not block durable acceptance

Model extraction, resolution, embedding and summarization are asynchronous proposal-producing stages. Record model/provider/version/tokenizer/config metadata and deterministic input digest. Model unavailable/OOM/rate-limited produces retryable/degraded state; accepted source remains durable. No model output is canonical truth.

### TAR-E-P1-005 — 12–16 GB VRAM envelope requires admission control

Do not co-schedule embedding, reranking and large LLM workloads by default. Define per-model peak VRAM, KV cache/context, batch size, concurrency and CPU fallback. Use bounded queues/backpressure; GPU worker isolation prevents inference stalls from blocking ingress/recovery.

## 4. Technology disposition

| Technology/approach | Disposition | Conditions |
|---|---|---|
| Rust/Tokio compiler host | ACCEPT AS CANDIDATE | Supervised tasks, cancellation, bounded queues and graceful shutdown. |
| DB-backed transactional outbox | RECOMMEND | Accepted receipt + intent durable atomically or equivalent recoverable protocol. |
| DB-backed worker queue | ACCEPT AS FIRST PROTOTYPE | Lease fencing, retries, fairness and queue-age measurement required. |
| Kafka-class broker | DEFER | Only justified by measured throughput, multi-host or independent scaling requirements. |
| Serde/provider traits | ACCEPT AS CANDIDATE | Explicit versioning and untrusted output validation. |
| Isolated model worker | RECOMMEND | Process boundary, resource admission, no authority over durable ingress. |
| Content-addressed blob store | ACCEPT AS CANDIDATE | Private staging, integrity checks and DB/blob backup consistency. |
| SQLite WAL | NEEDS D/Storage VALIDATION | Compiler must not infer atomic gate semantics from WAL mode. |
| ONNX/llama.cpp/Candle | CANDIDATE | Benchmark actual model/operator, platform, quantization and VRAM profile. |

## 5. Failure/recovery matrix

| Failure | Required behavior | Test |
|---|---|---|
| Duplicate Accepted request, same digest | Return original receipt and IDs | E-FAULT-15 |
| Same idempotency key, different digest | Immutable conflict; no side effect | E-IDEM-01 |
| Crash after acceptance before D registration | Recover pending registration with same WorkItemId | E-REC-01 |
| Registration ACK lost | Resolve same receipt by same ID/digest | E-FAULT-16 |
| Worker crash/lease expiry | Old attempt cannot publish; root item stays open | E-FAULT-11 |
| Outbox duplicate/out-of-order replay | Deduplicate stable IDs; do not skip cursor gaps | E-FAULT-12 |
| DLQ replay after Forget | Fresh authorization/fence check; reject/quarantine | E-FAULT-13 |
| Recompile after Forget | Preserve lineage/root barrier; no reset of fence cutoff | E-FAULT-14 |
| Partial dependency edge set | No complete receipt; artifact private | E-FAULT-18 |
| Publish ACK lost | UNKNOWN remains private until same operation resolves | E-FAULT-16 |
| Permission revoked at final gate | Deny/quarantine | E-FAULT-19 |
| Restore stale snapshot | Quarantine and replay current control ledger before serve | E-FAULT-17 |

The referenced E fault matrix is explicitly **DESIGN ONLY / NOT RUN**; the test IDs above are required future evidence, not test results.

## 6. Resource assessment

Measure events/sec, bytes/event, acceptance latency, outbox lag, queue depth/age, worker concurrency, retry amplification, stage duration, blob write throughput, orphan ratio, model latency, peak VRAM and CPU fallback throughput. Bound queues by count and bytes; derive capacity from arrival rate × service time and test overload/backpressure. No benchmark values are asserted.

## 7. Required sequence

1. Bind E's semantic operations to callable D request/receipt schemas and authenticated H transport.
2. Finalize I's current PermissionEpoch/authorization freshness input.
3. Implement Storage transaction/visibility boundary with D.
4. Implement private staging and durable dependency receipt handling.
5. Run duplicate, crash, lease, replay, permission-revocation and fence-race tests.
6. Benchmark DB queue/outbox and model workers; only then consider external broker or additional inference runtime.

## 8. Final recommendation and non-claims

Conditionally accept TAB-001's compiler topology. Do not freeze queue implementation, database, model runtime or publication coordinator. No executable race/fault suite, model benchmark, VRAM measurement, production queue, database-backed outbox, or end-to-end compiler publication was run by this review.
## 9. Reassessment — Storage candidate and JF-10 producer boundary (2026-11-17)

The original report's Storage realization blocker is refined for the current architecture phase:
- PostgreSQL 18.7 is now a qualified prepared-XID candidate for the pinned CI profile, with seven capability workflows 7/7 SUCCESS (PITR `43958775001`; prepared-XID `43959079736`; synchronous promotion `43959079669`; backup/restore `43959079703`; WAL PITR `43959079745`; sync-unavailable `43959079760`; pg_rewind/rejoin `43959079930`). These are engine capability fixtures, not production E/Storage integration.
- E has accepted the exact JF-10 producer lifecycle contract in `04-memory-compiler/phase-3.6.2-e-jf10-coc-bridge-producer-acceptance.md`, Blob `4503628cf6f6ea46696ab14e7decd3e408ced19a`.
- E has accepted the exact COC durable protocol Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25` in `04-memory-compiler/phase-3.6.3-e-coc-durable-protocol-acceptance.md`, Blob `b9dd9af8c770a40b44849d02caac306e0a701100`.
- Gate B COC protocol design is accepted by exact owner review; Gate C integrated runtime/fault injection remains deferred to engineering.

Updated E disposition: **CONDITIONAL PASS — compiler architecture and producer-boundary contract accepted; runtime integration remains NOT IMPLEMENTED / NOT VERIFIED.** No E ledger, durable queue, D client, artifact store or Storage adapter is claimed. JF-10 P0 remains OPEN until executable end-to-end conformance.