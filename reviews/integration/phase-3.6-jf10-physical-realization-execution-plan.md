# JF-10 P0 — Physical Realization Execution Plan

- Owner: Session A — Principal Integration Architect
- Status: **EXECUTION PLAN / NO IMPLEMENTATION OR DEPLOYMENT CLAIM**
- Controlling issue: #10
- Controlling bridge: A COC architecture `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`; I disposition `8069ff86988396442c8d9dc3fd58653683abe2f3`; common D/Storage JF-10 v2 `94679897e84a6f58fd8b9467b5249e1a885cb0b0`; C acceptance `45a48249717c8cddb07ab96197730ef93d406c22`; D `5a56c406578fdf257509315eb3f6f3f75456116c`; Storage `55c01f4512f2e3d8aac767dd004e768ae073178e`; H mapping `1716b23741479740f9e12003cbf2bd1a80c63aab`; H schema candidate `a8a945cc3623c2907003b93625e3c79742150944`.

## 1. Current verified baseline

The architecture/interface decision gate is closed with enumerated exceptions. The physical implementation gate is not closed.

Fresh Owner artifacts state:
- D specifies semantics but does not select/certify a DB, lock manager or distributed transaction product.
- Storage recommends a single transactional database for coordinator/ledgers/publication/visibility/outbox, but explicitly records engine/version, XA/prepared-XID profile, isolation, replication/failover and restore as unselected/unverified.
- Storage requires same-XID recovery and durable lock retention; a DB lacking those capabilities blocks implementation unless I/D approve a different protocol.
- C owns provider outcome and idempotency evidence.
- I remains sole JF-10 terminal decision authority for one I PolicyDomain.
- A's five-message semantic validator is a reference model only. Its 10-test CI PASS applies to the old revision; the expanded 18-test revision has not yet been executed.

No production database, COC consensus deployment, named operator, executable JF-10 service or physical fault-injection harness has been established by the evidence currently read.

## 2. Owner work allocation (no authority transfer)

| Work package | Accountable Owner role | Owner branch | Required artifact | Entry/exit rule |
|---|---|---|---|---|
| A — DB candidate and capability dossier | Storage engineering | `session-storage-consistency-forget-atomicity-2026-11-16` | `reviews/storage-consistency/jf10-database-capability-dossier.md` | Must name real product/version/build/configuration and accountable operator; no generic vendor capability claims |
| A1 — Prepared participant proof | Storage engineering, with I review | Storage branch | executable probe + raw crash/restart/failover traces | Must prove exact XID and lock retention, same-XID forward/rollback recovery; otherwise STOP and raise incompatibility |
| A2 — Canonical visibility transaction | Storage engineering, with D/E review | Storage branch | transaction implementation/schema + concurrency traces | Fence/lineage/final visibility/PublicationReceipt/outbox must share one proven serialization boundary or approved equivalent |
| B — Persistent COC design and implementation | A coordinates; named COC service operator must be designated | A branch for integration contract; operator implementation branch must be named before coding | `reviews/integration/jf10-coc-persistent-coordinator-realization.md` plus executable service | No operator/topology designation means STOP; do not claim A is infrastructure operator |
| C — C provider idempotency/recovery | C | `session-c-agent-integration-2026-11-16` | provider adapter outcome contract + provider-specific idempotency probe | Same idempotency key across UNKNOWN/IN_DOUBT; no retry-as-new; C emits actual terminal CSubmitOutcome |
| D — Fence/lineage race oracle | D | `session-d-memory-brain-2026-11-16` | deterministic cutoff/barrier fixtures and expected traces | D alone defines fence/lineage predicates and accepted ordering |
| I — Sequencer/receipt/revocation proof | I | `session-i-security-governance-2026-11-16` | I sequencer integration proof and terminal receipt/revocation race fixtures | I alone proves receipt consumption and COMMIT/ABORT terminalization |
| H — Schema/parser interoperability | H | `session-h-bmcp-protocol` | generated schema/IDL/parser fixtures and cross-implementation tests | JSON Schema candidate is not production freeze; canonical bytes, duplicate keys, signatures and key lifecycle must be enforced |
| A — Cross-owner fault harness and evidence ledger | A coordinates; each Owner supplies its own oracle | A branch + Owner branches | reproducible runner, run manifest, logs, invariant output, exact build/config hashes | A may aggregate evidence, never synthesize an Owner's authoritative result |

Individual operator/engineer names are not present in the current Owner decisions. The relevant Owner must explicitly name its accountable engineering lead and service operator before any deployment gate is treated as staffed.

## 3. Strict execution sequence

### Gate 0 — Freeze exact inputs and name accountable operators
1. Refresh exact Blob SHAs for A/C/D/I/H/Storage and common JF-10 v2.
2. D and Storage separately append exact-bundle confirmation covering every pinned Blob (tracked in Issue #9).
3. Storage names the Canonical Authority DB engineering owner and service operator.
4. A/COC names the COC service operator and infrastructure owner.
5. Record environment boundary, security/KMS owner, failure domains, RPO/RTO, SLO, retention and escalation.

**STOP** if a named owner/operator or actual environment cannot be identified. Architecture acceptance is not a substitute.

### Gate A — Select and probe the real database
1. Record product, exact version/build, extensions, topology and configuration digest.
2. Specify transaction isolation, replication mode, durability/ack semantics and authoritative-read path.
3. Probe durable prepared-XID (or an explicitly approved equivalent), lock retention across DB/process restart and failover, same-XID commit/rollback recovery, and heuristic recovery policy.
4. Prove atomicity of fence/lineage validation, VisibilityPointer, PublicationReceipt, terminal disposition and outbox at the final serialization boundary.
5. Test stale replica exclusion, lost ACK, duplicate request, failover during commit, backup restore and snapshot rollback fencing.
6. Obtain Storage, D and I decisions on the exact implementation protocol.

**STOP** on any inability to preserve exact XID/locks or to atomically enforce the current fence at publication. No check-then-write substitute.

### Gate B — Implement persistent COC
1. Select consensus/log product and version; name operator and voter/failure domains.
2. Implement quorum-confirmed append, monotonic term/index, digest-chained committed prefix and durable participant registry.
3. Implement preallocated-XID intent binding, prepared receipt registration and atomic recovery-cutoff batch.
4. Implement unresolved participant enumeration and idempotent reconciliation APIs.
5. Implement restore fencing on prefix/high-water mismatch; no TTL/heuristic release for IN_DOUBT.
6. Prove quorum loss, leader restart, lost append/read ACK, duplicate append, stale replica, snapshot rollback, partial restore and missing-prefix behavior.

**STOP** if a participant can disappear from authoritative enumeration or if restore can reopen admission before prefix/high-water reconciliation.

### Gate C — Integrate owner authorities and provider
1. I sequencer atomically consumes the exact authorization receipt and records terminal decision for the same prepared XID.
2. Storage resolves only that same XID in the I-directed forward/rollback direction.
3. D barrier remains open until I terminal, Storage resolution, C provider outcome and lineage obligations are authoritative.
4. C preserves provider idempotency key across timeout, process death and UNKNOWN/IN_DOUBT; provider outcome is never inferred from COC/Storage state.
5. H generated parser rejects duplicate keys, non-canonical bytes, invalid signatures, stale key epoch, unknown critical fields and tuple mismatch.
6. One I PolicyDomain only. Multi-PolicyDomain remains blocked.

### Gate D — Deterministic fault-injection campaign
Execute Issue #10 cases 1–14, plus the 18 reference-validator tests. Add owner-specific tests for every production transition. Every run records:
- test ID, deterministic seed and exact source/build SHA;
- database/coordinator/provider product/version/configuration digest;
- operation/request/participant/XID/idempotency IDs and all authority positions/digests;
- crash point, restart/failover/restore action and observed durable state;
- DB lock/transaction trace, COC quorum/prefix proof, I/D/Storage authoritative lookups, provider evidence;
- invariant checker output, raw logs, and independent Owner sign-off.

A green reference-model test is not a substitute for any physical campaign test.

## 4. Required evidence artifacts

- Storage: DB capability dossier, schema/migrations, transaction implementation, prepared-XID probe, lock trace, same-XID crash/recovery traces, failover/restore report.
- COC operator: topology/config manifest, persistent log/registry implementation, quorum/prefix proof, restore-fence report and operator runbook.
- C: provider-specific idempotency evidence and CSubmitOutcome traces.
- I: receipt-consumption and terminal decision persistence proof, revocation cutoff race traces.
- D: fence/lineage serialization traces and barrier completion evidence.
- H: generated schema/IDL/parser artifacts, canonicalization/signature test vectors, interoperability report.
- A: cross-owner run matrix, exact evidence ledger, unresolved-risk register and final gate recommendation.

## 5. Current gate ledger

| Gate | Status | Reason |
|---|---|---|
| Architecture/interface bridge | CLOSED WITH ENUMERATED EXCEPTIONS | Exact C/D/Storage/I/H owner decisions recorded; single I PolicyDomain only |
| D + Storage full multi-artifact bundle confirmation | OPEN | Issue #9 has no Owner response yet |
| Named Storage DB/operator | NOT DESIGNATED | No actual DB product/version or accountable operator in Storage artifact |
| Named COC operator/infrastructure | NOT DESIGNATED | No deployed consensus/log service or accountable operator |
| DB prepared-XID/lock/visibility capability | NOT PROVEN | No executable capability probe or environment trace |
| Persistent COC | NOT IMPLEMENTED / NOT VERIFIED | Architecture proposal only |
| Provider idempotency | NOT VERIFIED | No provider-specific implementation/probe evidence |
| 18-test reference validator revision | COMMITTED / READBACK VERIFIED / CI PENDING | New commit should trigger push workflow; no run result read back yet |
| Physical fault campaign | NOT RUN | No selected environment/harness evidence |
| JF-10 P0 | OPEN | Physical gates above remain open |
| Production activation / merge | NOT AUTHORIZED | No production approval or merge authorization |

## 6. Change control

Any change to I terminal authority, exact-XID semantics, D fence ordering, Storage visibility atomicity, C provider idempotency, COC committed-prefix semantics or H wire meaning requires the owning authority's append-only decision and a new exact bundle SHA. A coordinates the reconciliation and does not override Owner authority.
