# A Owner — Storage Gate A Architecture Design Conditional Acceptance

- Storage readiness document current Blob: `ae33b4124329dd904d0f1ba871c96f9ce6744ba4`
- Storage restore control-high-water contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- COC §14 exact-owner matrix Blob: `4059a228613cf2c72a7797f2a1427f843ef066a0`
- Restore I/D/B/H/A/Storage exact acceptance artifacts are pinned in Storage readiness §29.
- Decision: **CONDITIONAL PASS — STORAGE ARCHITECTURE DESIGN CONTRACT COMPLETE**

A accepts Storage Gate A's architecture design baseline with these decisions:

1. One logical Canonical Authority transaction domain per authority boundary; PostgreSQL SERIALIZABLE target for safety-critical admission/fence/dependency/visibility/terminal transactions with explicit row locks and whole-transaction idempotent retry.
2. Storage visibility is one authoritative transaction over VisibilityPointer, PublicationReceipt, owner outcome/receipt-consumption evidence and outbox; outbox is notification only; stale replicas/caches/object listings cannot authorize reads.
3. PreparedParticipantRef, PreparedTransactionGID and EngineNativeTransactionXIDRef are separate; Storage preallocates/binds the stable participant/GID tuple before COC prepare intent; PREPARE only after exact COC intent commit; same GID resolves terminal state.
4. PostgreSQL 18.7 is a qualified capability candidate with seven successful CI workflows, not a production engine/deployment freeze.
5. COC durable log and amended §14 are exact-owner-accepted at design level.
6. Restore starts quarantined and requires COC committed-prefix proof, per-domain I control-high-water proof, per-operation D Forget/lineage high-water proof and Storage participant-ledger proof. Storage's receipt is RECONCILED_BUT_FENCED, not authorization or permission to serve.
7. RPO 0 is bounded to the specified synchronous durability and one-voter crash-fault models; correlated majority/primary+sync-standby/site loss is outside the guarantee. Numeric RTO remains TBD pending measured restore.

### Conditions / exclusions

- Real proof APIs, signature verification, COC/I/D/Storage service integration and Gate C distributed fault injection are deferred to engineering.
- Representative corpus/workload benchmarks, SERIALIZABLE contention, storage/manifest/WAL growth, restore time and resource budgets remain engineering measurements.
- Production failure-domain placement, physical fencing/STONITH, KMS, archive/checkpoint custody, named operator/approver and runbooks remain deployment decisions.
- I36-GOV-01..10 remain GOVERNANCE-BLOCKED; Fact/Claim ADR-001 remains ADR-BLOCKED; Global Forget target inventory/physical erasure remains open; multi-PolicyDomain atomicity remains blocked.

**Final Gate A vector:** Storage architecture design CONDITIONAL PASS; implementation/deployment NOT PASSED and deferred; Gate B design accepted with conditions; Gate C deferred; JF-10 runtime P0 open; TAB-001 candidate/not frozen; production activation not authorized.