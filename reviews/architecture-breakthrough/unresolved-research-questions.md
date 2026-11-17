# Unresolved Research Questions

- Status: OPEN unless explicitly classified
- Baseline: `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`

## A. Forget / Model Checking

1. What is the exact physical linearization authority for RegisterProducerWork vs InstallForgetFence?
2. Can dependency registration, canonical target commit, outbox and final visibility be committed in one PostgreSQL/SQLite transaction, or is a recoverable prepare/commit protocol unavoidable?
3. What does “terminal” mean for a worker whose lease expired but whose process may still publish?
4. Is the producer inventory closed-world at a stable inventory epoch, and how are unknown/offline external recipients represented?
5. Which ACKs are authoritative evidence, which are transport observations, and how are lost ACKs reconciled by stable operation identity?
6. What is the restore order across COC, database, D/I control high-waters, indexes, Context and Adapters?
7. Which liveness assumptions are legitimate (eventual worker availability, quorum availability, retry fairness), and which should not be assumed?
8. Can the current protocol be refined into one transaction plus outbox for v1 without losing required multi-failure-domain guarantees?

## B. Memory Operating System

1. Which F/G budget structures are independently enforced today, and which are merely descriptive?
2. Are candidate/evidence/token/byte/VRAM budgets double-counted or do they protect different resources?
3. What is the target workload: concurrent sessions, context size, corpus size, request mix and 12–16 GB VRAM usage?
4. Which work classes need reserved capacity and fairness guarantees?
5. Is Working Set actually improving latency/token cost over request-local retrieval cache?
6. What is the measured benefit of LRU vs LFU vs TTL vs segmented admission under memory-specific workloads?
7. How should a resource manager report pressure without allowing low-priority tasks to starve indefinitely?
8. Can Resource Manager remain a small in-process module with no new durable state beyond reservations and telemetry?

## C. Memory IR / Compiler

1. What are the minimum canonical candidate types that B/D have approved? Fact/Claim remains ADR-blocked.
2. Should IR be a versioned Rust type hierarchy, JSON schema, protobuf, or internal Serde envelope for v1?
3. Which transformations are deterministic and which are model Activities with recorded outputs?
4. How should source span locators remain valid across source format/parser evolution?
5. What is the stable identity/fingerprint of a derivation when prompts, models, normalizers and schemas change independently?
6. How are conflicts represented without prematurely choosing one truth?
7. What lineage graph restrictions apply (DAG vs selected cycle semantics)?
8. What is the minimum incremental invalidation closure needed for source updates and Forget?
9. Which fields are retained when source content is forgotten but audit metadata must remain?
10. How can IR schema evolution preserve old run replay without pinning obsolete models forever?

## D. Product adoption / topology

1. Does v1 require multiple concurrent writers or only a local single-host deployment?
2. Is PostgreSQL 18.7 an approved production candidate or only a CI capability qualification?
3. What exact data must be transactionally co-located for the Forget/publication linearization point?
4. What workload justifies Qdrant versus embedded vector index or database extension?
5. Is Tantivy sufficient for multilingual lexical search, tokenizer customization, phrase matching and incremental deletion?
6. What measured condition triggers Temporal or Kafka adoption?
7. Which deployment/backup/operator responsibilities are in scope for v1?
8. Which external product costs (RAM, disk, backup, upgrade, restore, observability, security) are acceptable?

## E. Governance and evidence

1. Who approves cross-owner architectural changes and candidate ADRs?
2. What exact evidence is required before an experiment result can upgrade CANDIDATE to DECIDED?
3. Which Owner must approve each proposed shared contract?
4. How will bilingual parity be checked for generated/experimental artifacts?
5. How can duplicated report/PR coordination be measured and reduced without weakening Owner review independence?
6. What is the canonical place for experiment fixtures, model configs, traces and benchmark outputs?
