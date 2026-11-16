# Phase 3.6 — Hermes Runtime Deployment Binding Assessment

Date: 2026-11-17  
Owner: A (Principal Integration Architect), with Storage deployment evidence review  
Disposition: **DEPLOYMENT BINDING INCOMPLETE — Gate A remains PARTIAL PASS / OPEN**

## 1. Purpose

This assessment corrects the earlier narrow repository inventory. The accessible private oahcom/hermes-scripts repository contains runtime configuration and operational scripts for the Hermes memory services. These artifacts provide concrete service endpoints and local storage references, but they do not yet identify the installed Holographic Memory Server implementation, its authoritative backing database, or the live host topology.

This is an evidence reconciliation, not a claim that the production deployment has been inspected live.

## 2. Repositories and exact refs inspected

| Repository | Branch / HEAD | Relevance |
|---|---|---|
| oahcom/AiMemoryBrainArchitecture | main — 8a6414158c9c056c1638222534e1993d1bbc99d2 | Architecture and governance artifacts; no production DB deployment manifests found in its 47-entry main tree. |
| oahcom/hermes-scripts | quality-gate — 9292ec97d572c4c56d2e4f4938c7d70ce0706afa | Runtime service configuration, memory client scripts, local DB references and service operations. |
| oahcom/DBInstanceManagement | main — 4b8d878e94a7ec3083b5b36ade586d6d886f3408 | Separate database-inventory application; not established as the Canonical Memory Authority. |

## 3. Observed Hermes memory service contract

The hermes-scripts runtime configuration declares two local HTTP memory services:

- DKK memory service: http://localhost:9901, health path /health.
- SSK memory service: http://localhost:9902, health path /health.

The same ports appear in config/ports.yaml. scripts/query_factstore.py calls the HTTP fact-search API, and scripts/precipitate.py posts new facts to both DKK and SSK service endpoints. The default Hermes profile configures the memory-store plugin to use the DKK endpoint.

Exact source pins:
- config/services.yaml — Blob b872263f0d0fdde7e3828bc02ece2fd1e133a9ba
- config/ports.yaml — Blob 7966e963d2347db7d2de8396281048236e7cb023
- config/profiles/default.yaml — Blob 611fc1a4f7a6fbcc43639c36a71118acd82088ee
- scripts/query_factstore.py — Blob 6a2bca957fd2dc3be5a35f3636d8f5d834ef2845
- scripts/precipitate.py — Blob 8058cfff7b5b67671746085c3a6e44aed2003247

The presence of two service endpoints does not prove that they are two I PolicyDomains. That mapping remains an explicit I-owned semantic decision and must not be inferred from process names or ports.

## 4. Observed local storage references — not yet the canonical backing-store proof

Several helper components directly use SQLite:
- scripts/episodic_memory.py defaults to ~/.hermes/data/state/episodic_memory.db — Blob d3a6ea83fe561a654f1b2382b6978d118d674981.
- scripts/memory_md_refresh.py reads ~/.hermes/memory_store.db and ~/.hermes/profiles/sister/memory_sister.db — Blob b8867a313831f23ab72ecf2d6efb2aa22c3acced.
- scripts/memory_cleaner.py reads ~/.hermes/memory_store.db — Blob 74f0e595412d6ddaa6f6bf6dc973ef9b5b1b37da.

These files prove that SQLite is used by auxiliary memory/fact-store tooling. They do not prove that the installed HTTP service at ports 9901/9902 uses those exact files as its authoritative write store.

The service launcher scripts/start_memory_server.sh points to an installed plugin file at ~/.hermes/hermes-agent/plugins/memory/holographic/memory_server.py and defaults to port 8901. The tracked service registry instead declares DKK/SSK on 9901/9902, while scripts/hermes-ops.sh manages memory-server-dkk, memory-server-ssk and sister-mem systemd services. This discrepancy means the launcher path and the active service topology are not fully bound by the tracked artifacts.

Exact source pins:
- scripts/start_memory_server.sh — Blob 1b22c3befe941e0ac6e2852f5e464b4053a91e01
- scripts/hermes-ops.sh — Blob 6d50f176f55133c2f8002e570924d4ff7156e4ee
- scripts/INCIDENT_20260618_DOCKER_MIGRATION.md — Blob 82525df23495c44c593144932c0a9d9ef86a6785

The incident record documents a Docker-to-systemd migration and service recovery work, but it is not a live service-status capture and does not establish the current active process manager or host/zone topology.

## 5. Separate DBInstanceManagement repository disposition

oahcom/DBInstanceManagement is a separate Django/Celery database-inventory service. Its README describes inventory of database instances, clusters, departments, credential rotation and daily statistics. Its tracked config/settings.py defaults Django to a local SQLite database. No evidence connects it to Hermes Holographic Memory or the JF-10 Canonical Memory Authority.

Therefore it is not selected as the JF-10 production database target and must not be used to claim that a production PostgreSQL deployment exists.

Source pins:
- README.md — Blob d72fc4f4dac0ac46d612de8ed5703416e158f77c
- config/settings.py — Blob ff079e36f05d0d1c0ad13680721bb6918f782a78
- inventory/models.py — Blob 1bc2136f759cf2d90e529d79640e62e69788778d

## 6. PostgreSQL 18.7 decision boundary

PostgreSQL 18.7 remains the pinned capability-qualification candidate only. The five CI evidence classes now pass on that profile:
1. single-node prepared-XID, lock retention, hard restart and same-XID commit/rollback;
2. synchronous two-node WAL replay, primary loss, standby promotion and same-XID commit/rollback;
3. physical backup/restore with prepared-XID survival and stale-control fail-closed fixture;
4. coordinator process crash after participant success but before ACK/checkpoint persistence;
5. actual TCP CommandComplete response loss after PREPARE, COMMIT PREPARED and ROLLBACK PREPARED, followed by same-XID reconciliation.

These tests prove properties of the PostgreSQL 18.7 CI profile. They do not prove that the currently deployed Hermes memory services use PostgreSQL, or that the production system is ready to migrate to it.

If the authoritative JF-10 participant is currently SQLite-backed, SQLite does not provide PostgreSQL-style prepared transactions / recoverable XA participants; it cannot be accepted as the JF-10 participant merely because its local transactions are atomic. The actual authoritative service implementation and storage binding must be inspected before selecting migration or adapter work.

## 7. Live inspection limitation

The authorized Desktop Commander device was listed but was OFFLINE at the time of this assessment. Therefore no live command was executed against the host. In particular, the following remain unverified:
- active systemd unit names and states for DKK/SSK memory servers;
- exact executable path and source version for memory_server.py;
- actual database engine, database file/cluster path and schema used by the HTTP service;
- whether memory_store.db / memory_sister.db are authoritative stores or helper/replica stores;
- actual persistent volume, filesystem, host and zone;
- backup/PITR policy and tested restore point;
- current I/D control-ledger source and service-to-PolicyDomain mapping;
- production failover fencing, routing, human on-call, runbook and RPO/RTO.

## 8. Required binding sequence — still Gate A, no Gate B

1. Bind the live DKK and SSK service processes to exact executable paths, code versions and unit definitions.
2. Read the installed memory_server.py implementation and identify its actual authoritative database adapter and path.
3. Map each service endpoint to the authoritative memory owner and I PolicyDomain; resolve whether the two endpoints share one PolicyDomain or are separate domains. Do not infer this from DKK/SSK labels.
4. Inspect the actual backing store and durability profile, including filesystem/volume, WAL/journal settings, backup and restore.
5. If the canonical participant is not PostgreSQL 18.7, create a migration/adapter plan and run the same JF-10 prepared-XID, failover, restore and TCP ACK-loss tests against the actual participant.
6. Bind production host/zone, fencing/quorum/routing, named human operator, runbook, RPO/RTO and the real I/D control-ledger source.
7. A independently re-reads the exact deployment binding and test evidence before accepting Gate A.

## 9. Current gate disposition

| Gate | Status |
|---|---|
| Gate 0 — D + Storage exact complete-bundle decisions | CLOSED |
| Gate A — PostgreSQL 18.7 candidate qualification | PARTIAL PASS; five CI evidence classes PASS |
| Gate A — actual Hermes canonical memory service and production binding | OPEN / NOT VERIFIED |
| Gate B — persistent COC/quorum log | BLOCKED until Gate A closes |
| Gate C — deterministic end-to-end fault campaign | BLOCKED until Gate B closes |
| JF-10 P0 / production activation | OPEN / NOT AUTHORIZED |

This assessment supersedes the earlier blanket statement that no relevant runtime repository was identified. It does not supersede the requirement for live production binding. The newly found Hermes runtime repository provides service-level evidence, but the installed memory-server implementation and actual canonical backing database remain outside the tracked repository and unavailable while the authorized device is offline.
