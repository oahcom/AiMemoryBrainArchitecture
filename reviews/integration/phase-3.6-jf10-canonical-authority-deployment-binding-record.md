# JF-10 Canonical Authority Deployment Binding Record

**Owner:** A / Principal Integration (coordination only; does not select another Owner's database or operate production infrastructure)  
**Date:** 2026-11-17  
**Status:** NOT DESIGNATED — Gate A remains PARTIAL PASS / OPEN  
**Authority:** Issue #10, Gate A; Storage PostgreSQL 18.7 capability dossier

## 1. Purpose and scope

This record defines the project-owned evidence required to bind the JF-10 Storage participant contract to an actual Canonical Memory Authority deployment. It does not select a production database, invent a deployment target, or authorize production activation.

Only deployment evidence explicitly designated for AiMemoryBrainArchitecture may satisfy this record. Unrelated repositories, helper tools, local service names, or exploratory runtime observations are not dependencies or acceptance evidence unless the project formally adopts them through the relevant Owner decisions.

## 2. Current evidence boundary

Storage has selected PostgreSQL 18.7 as a candidate for physical capability qualification. The pinned CI image is:

`postgres:18.7@sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc`

The following CI evidence groups have passed for that pinned test profile:

1. Single-node prepared-XID, lock retention, hard restart, same-XID commit/rollback.
2. Two-node synchronous replication, primary hard loss, standby promotion, same-XID commit/rollback.
3. Physical backup/restore with prepared-XID survival and stale-control fail-closed behavior.
4. Coordinator process crash after participant success but before ACK/checkpoint persistence.
5. PostgreSQL protocol TCP CommandComplete response loss after PREPARE, COMMIT PREPARED and ROLLBACK PREPARED, followed by same-XID reconciliation.

These are bounded CI capability results. They do not identify the project's production Canonical Authority deployment or prove production fencing, operational ownership, external I/D ledger integration, or persistent COC consensus.

## 3. Deployment binding — all fields currently unassigned

| Required field | Current value | Required evidence |
|---|---|---|
| Canonical Authority service / deployment name | NOT DESIGNATED | Project architecture/operations decision |
| Environment and deployment boundary | NOT DESIGNATED | Environment identifier and deployment inventory |
| Accountable service owner | NOT DESIGNATED | Named accountable owner or formally assigned role |
| Production operator / on-call | NOT DESIGNATED | Named rotation or accepted operational ownership |
| Database product and exact build | NOT DESIGNATED | Live server version/build readback |
| Database image/package digest | NOT DESIGNATED | Immutable deployed artifact digest |
| Database configuration | NOT DESIGNATED | Redacted, versioned configuration and SHA |
| Primary / standby topology | NOT DESIGNATED | Live topology and replication-state evidence |
| Host / zone / storage failure domains | NOT DESIGNATED | Infrastructure inventory and provider evidence |
| Prepared-XID participant adapter | NOT DESIGNATED | Source path, commit, build and runtime binding |
| D fence / lineage serialization integration | NOT DESIGNATED | D-owned contract and executable integration evidence |
| I sequencer / terminal decision ledger | NOT DESIGNATED | I-owned service, persistence and recovery evidence |
| COC durable log / quorum | NOT DESIGNATED | A/COC implementation, topology, quorum and operator evidence |
| Authoritative read path / stale replica exclusion | NOT DESIGNATED | Runtime routing and consistency proof |
| Failover fencing / split-brain prevention | NOT DESIGNATED | Fencing mechanism, failure tests and rejoin policy |
| Backup / restore / PITR procedure | NOT DESIGNATED | Approved runbook and tested recovery trace |
| Forget-control replay before restored reads | NOT DESIGNATED | I/D authoritative high-water integration test |
| RPO / RTO | NOT DESIGNATED | Approved service objectives and measured recovery |
| Runbook and incident escalation | NOT DESIGNATED | Versioned, approved operations documentation |

## 4. Acceptance sequence

Gate A cannot be accepted until all of the following are complete on the designated project deployment:

1. Storage identifies the actual database product, exact build, immutable artifact digest, configuration, isolation level and participant adapter.
2. The deployment owner identifies the primary/standby and storage failure domains, synchronous replication policy, failover manager, fencing/STONITH, split-brain prevention and reconnect/routing behavior.
3. D and I identify the authoritative fence/lineage and authorization/terminal-decision persistence sources and demonstrate their integration with the participant recovery path.
4. The service owner and human production on-call/operator are formally designated; runbook, RPO and RTO are approved.
5. Storage reruns the applicable prepared-XID, restart, failover, rollback, backup/restore, stale-control and TCP ACK-loss probes against the exact deployed profile.
6. A verifies immutable artifact/configuration pins, raw traces, authoritative readbacks and each Owner's explicit acceptance. A does not synthesize another Owner's evidence or decision.

Any missing or ambiguous authoritative state must remain UNKNOWN / IN_DOUBT / RecoveryQuarantined as required by the contracts. No TTL, heuristic outcome, new-XID retry, or read-service reopening is permitted to bypass unresolved state.

## 5. Gate disposition

- Gate 0 (D + Storage exact full-bundle decisions): CLOSED.
- Gate A (PostgreSQL 18.7 CI capability qualification): substantial physical subtests PASS.
- Gate A (actual project deployment binding and production operations): OPEN / NOT DESIGNATED.
- Gate B (persistent COC implementation and quorum proof): BLOCKED until Gate A is accepted.
- Gate C (end-to-end deterministic fault-injection campaign): BLOCKED until Gate B is accepted.
- JF-10 P0: OPEN.
- Production activation: NOT AUTHORIZED.
- Multi-PolicyDomain atomicity: BLOCKED; the existing single-I-PolicyDomain constraint remains.

## 6. Explicit exclusions

