# Forget State Machine

## Model boundary

Forget is a product of distinct authority-owned state machines, not one Boolean deleted flag.

- D: ForgetOperation, ForgetFence generation, canonical target/lineage inventory, producer registry and barrier.
- E: ProducerWork, attempts/leases, private staging, dependency registration and publication orchestration.
- Storage: durable participant/visibility transaction and recovery outcome.
- I: authorization/revocation, producer-domain inventory/seal, global completion and exceptions.
- F: retrieval, index, cache and Working Set suppression.
- G: Context, delivery and Applied evidence/reconciliation.
- H: Adapter managed-region state, local suppression/clear and reconnect ACK.

## Abstract transitions

1. Request: persist stable ForgetOperation identity, normalized request digest and exact target selector.
2. Coverage: establish target/lineage and producer-domain coverage. Unknown coverage blocks closure.
3. Admission: register ProducerWork durably before queueing, lease, source dereference or execution.
4. Fence: atomically advance D's monotonic generation and capture producer-registration high-water for the affected authority/lineage.
5. Drain: resolve every pre-fence participant, retry, DLQ/replay and child output to a durable terminal disposition.
6. Derive: register the complete direct/transitive dependency set before any derivative becomes visible.
7. Publish: validate current D Fence, I authorization and immutable publication tuple at the final durable visibility boundary.
8. Suppress: all canonical reads and downstream disclosure boundaries evaluate the latest applicable Fence; unknown Fence state fails closed.
9. Reconcile: F/G/H and other owners report scoped suppression/cleanup outcomes. Unknown is not success.
10. Terminalize: D lifecycle Forgotten requires current D suppression proof plus exact I-authorized terminalization outcome. This is proposed in PRs #66/#68, not yet accepted as a cross-owner authority contract.
11. Restore: restore remains fenced until current COC, I, D and Storage high-waters and participant outcomes are reconciled; old snapshots cannot lower a Forget epoch.

## Linearization points

| Operation | Required linearization point | Current evidence |
|---|---|---|
| Forget request identity | Durable idempotency/operation record commit | D semantics specified; implementation absent |
| Fence installation | Canonical D transaction advances generation and captures registration high-water | D semantic requirement; physical transaction not demonstrated |
| Producer Admission | Durable ProducerWork registration ordered with Fence in same authority serialization domain | D requirement; E/Storage realization open |
| Derived Registration | Atomic dependency/manifest registration before visibility | D requirement; E contract Candidate |
| Canonical Publication | One durable transaction/atomic protocol commits visibility pointer and receipt after final Fence check | Design requirement; concrete DB/runtime absent |
| Applied receipt | G-owned immutable decision-ledger commit after complete evidence predicate | G normative design draft; implementation/cross-owner freeze open |
| Restore release | Final high-water stability check and owner-specific release gate | Candidate reference model; physical restore/failover proof absent |

## Race ordering

For admission/fence and publication/fence, exactly two legal serial orders exist:
- admission/publication wins first: the item is included in the fence barrier and its output is accounted for;
- fence wins first: new admission/publication is rejected or quarantined.

There must be no third state in which a worker is admitted but absent from the barrier, or an output is visible without its dependency edge and final gate.

Asynchronous projections need not be physically erased synchronously, but every disclosure path must consult current authority state or remain fail-closed until reconciliation.

## Multiple Forget operations

Fence generations are monotonic within the D authority. For overlapping target sets, effective suppression is the greatest applicable generation. A later Forget cannot erase, lower or supersede an earlier Fence. Operations may reconcile independently, but shared target/lineage state must retain all applicable operation references and strongest current suppression. Idempotency keys are scoped to a normalized request digest; same key/different digest is conflict.
