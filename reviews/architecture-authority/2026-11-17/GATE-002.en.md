# Gate Entry and Exit Criteria — GATE-002

- Version: 1.0.0; baseline `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`.
- This document preserves two separate layers: Issue #43 integration gates G1–G8 and JF-10 physical gates A/B/C. They are not interchangeable.

## Issue #43 integration gates

| Gate | Entry/exit evidence | Current A disposition |
|---|---|---|
| G1 Exact source pins/freshness | Each critical source has current branch HEAD, commit, path, Blob SHA, supersession and readback | PARTIAL; reports pin sources, but exhaustive Owner refresh and A readback remain |
| G2 Authority/consumer acceptance | Complete A–I + Storage authority/consumer matrix; exact-version Owner decisions; no inferred approval | BLOCKED |
| G3 End-to-end state/causal consistency | One contradiction-free model or every unresolved conflict assigned and blocking; typed local positions not compared | BLOCKED |
| G4 P0/P1 race/crash/recovery/identity/trust | Direct proofs or explicit blocking status for every critical case | BLOCKED |
| G5 Technology/topology feasibility | Accountable topology/technology decisions and reproducible evidence; no unsupported deployment assumption | BLOCKED |
| G6 Bilingual semantic parity | Paired files and independently checked semantic/status parity | PARTIAL; paired reports exist; full cross-document parity still needs review |
| G7 A integration disposition | A decision record and Owner-specific outstanding actions | This PR supplies candidate A disposition; final independent review remains |
| G8 Freeze recommendation | Explicit READY / READY WITH ENUMERATED BLOCKERS / NOT READY backed by G1–G7 | NOT READY |

No G1–G8 gate passes by document existence, role simulation, schema-only tests or candidate reference-model runs.

**Option A sub-gates:** L1 direction conditionally accepted only; L1 closure waits A-01/A-02/A-03 and exact D acceptance. L2 OPEN pending shared transaction/UoW and I COMMIT_WON/COC/JF-10 composition (A-04/A-05). L3 OPEN pending executed concurrency/reference-model/fault evidence. L4 OPEN pending real DB/adapter/deployment/operator/HA/PITR/read-path and physical drills.

**B protocol sub-gate:** H 1.2.14/C 1.0.1 is a candidate, not a current joint bundle. Storage v3.2.9 is stale; successor manifest and exact C/H/D/I adoption are required before G1/G2 closure.

## JF-10 physical gates (preserved exactly as separate gates)

**Gate A — Real database capability.** Must identify the selected product/version/build/configuration and actual Canonical Authority DB adapter/path; prove transaction isolation, prepared-XID (or explicitly approved equivalent), lock retention, same-XID commit/rollback after restart, atomic VisibilityPointer + PublicationReceipt + owner outcome + receipt-consumption evidence + outbox, authoritative read consistency, failover fencing, WAL-archive PITR/restore, stale-snapshot quarantine and deployment durability. Storage §8 selects L1 Option A (one serializable transaction domain per Canonical Memory authority). Latest Issue #10 status: **PARTIAL PASS / OPEN** for Gate A. Bounded PostgreSQL 18.7 capability probes do not close actual-runtime DB adapter/product/config, synchronous standby/promotion, old-primary fencing, PITR, control-ledger and operator/runbook requirements.

**Gate B — Persistent COC coordinator.** Requires selected durable log/consensus implementation, quorum-confirmed digest-chained prefix, monotonic term/index, durable participant-intent registry and preallocated XID binding, outage recovery-cutoff batch, unresolved participant enumeration/reconciliation, rollback-protected snapshot/restore and fail-closed missing-prefix behavior. Current: **BLOCKED until Gate A fully passes**.

**Gate C — Deterministic fault-injection suite.** Requires reproducible tests for every listed crash, ACK loss, race, provider UNKNOWN, COC quorum outage, stale replica, lost prefix, restore rollback, IN_DOUBT retention, invalid receipt/signature and inventory/lineage mismatch; evidence must bind exact binaries/schema/DB/config and include independent Owner review. Current: **BLOCKED until Gate B passes**.

Gate A partial pass does not imply B or C pass. Gate B/C do not authorize production activation. JF-10 P0 remains OPEN; multi-PolicyDomain atomicity remains BLOCKED.

## Production authorization

Requires all applicable Owner approvals, selected and deployed topology, security/identity governance, physical conformance, tested backup/restore and DR, named accountable operator/on-call, approved runbooks, monitoring, RPO/RTO, explicit production authorization. No current evidence satisfies this.

See SYS-RISK-002, READINESS-002 and FINAL-A-002.
