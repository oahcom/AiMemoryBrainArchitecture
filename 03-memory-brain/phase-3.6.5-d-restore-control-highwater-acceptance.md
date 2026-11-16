# D Owner — Exact Restore DForgetControlHighWaterProof Boundary Acceptance

- Exact Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- D ForgetFence/lineage contract Blob: `1f0391bc49d007c44ec74165bd33d37412cc7990`
- D participant barrier contract Blob: `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2`
- Decision: **ACCEPT WITH D-OWNED FENCE / LINEAGE HIGH-WATER CONDITIONS**
- Mode: delegated D-boundary review under user instruction; not independent human sign-off.

D accepts the DForgetControlHighWaterProof semantic boundary:

1. The proof is scoped to the restored Canonical Authority dataset and enumerates the complete set/digest of relevant active or recently terminal ForgetOperationRefs.
2. For each operation it binds DControlLedgerCheckpoint/HighWater, ForgetFenceGeneration, immutable request cutoff/effective position, ProducerRegistrationHighWater/WorkItemBarrier, target/source/ancestor lineage inventory snapshot/digest and barrier terminal state.
3. The proof is D-signed and audience-bound. D alone attests its fence generation, request cutoff, lineage coverage, producer barrier and canonical suppression state. COC, I or Storage cannot mint or infer D proof.
4. An open/unknown barrier, unresolved participant/lease, missing pre-batch intent, incomplete/late lineage, post-fence derivative or changed producer high-water makes the proof incomplete and keeps restore fenced.
5. Any D control-ledger change during restore invalidates the captured proof; Storage must re-read/reconcile before RestoreReconciliationReceipt.
6. D proof is not I authorization, COC prefix proof, Storage visibility proof, Global Forget completion or physical-erasure evidence.
7. If target-level isolation is not proven, any relevant unresolved D operation keeps the entire restored authoritative serving path fenced; no partial release is inferred.

Exceptions: D durable control-ledger checkpoint/proof API, complete lineage inventory and restore integration remain NOT IMPLEMENTED / NOT RUN. D's existing D-CO crash/failover/restore conformance remains open. This is architecture acceptance only.