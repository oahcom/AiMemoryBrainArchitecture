# D Owner Review — COC Recovery Cutoff & ForgetFence Owner-local Gate

- Reviewer: D — Memory Brain Architect
- Review target: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design.md`
- Exact target: commit 9a975f665ee60f4551effe0104ea8f867716d9dd; blob cd5566b3d99b5204401ac713a5bb2dcf89a02726
- Decision: **ACCEPT_WITH_CONDITIONS**
- Scope: D ForgetFence, lineage, producer-work barrier, D-local cursor and D-owned gate only.

## 1. D authority preserved

The proposal correctly states that D alone owns ForgetFence, ForgetFenceGeneration, lineage coverage, producer-work barrier and D cursor. COC may record D-signed cutoff/clearance evidence but cannot decide fence effectiveness, lineage completeness or barrier completion. D positions are typed and cannot be compared with COC or I positions. Owner-local timestamps are audit metadata only.

The outage rule is directionally correct: D must durably persist `PENDING_COC_CUTOFF` and close admission for the affected target/source/ancestor lineage before acknowledging the request as pending. COC recovery-batch membership does not make Forget effective and does not itself release the producer-work barrier.

## 2. Blocking conditions for D acceptance to become unconditional

### D-COC-01 — Participant enumeration must be bound to the batch (BLOCKING)

The algorithm commits `RECOVERY_CUTOFF_BATCH_COMMITTED` before it enumerates all pre-P participants, although the record definition says the batch carries participant enumeration high-water. D cannot attest barrier completeness against an unbound or later-changing participant manifest.

Required amendment: enumerate against the frozen prefix P and capture deterministic participant manifest/set digest before batch commit, or append a distinct immutable manifest record bound to the exact batch digest. D clearance must bind both batch and manifest digest.

### D-COC-02 — D lineage scope and participant membership need a completeness attestation (BLOCKING)

For every D request, the batch must preserve the exact ForgetOperationRef, target/source/ancestor selector digest, D request cutoff, D cursor/high-water and the complete affected participant set. A global pre-P participant list alone is not a substitute for D's per-fence affected-lineage membership proof. D must authoritatively classify each participant as affected/not affected with evidence; unknown lineage remains blocking.

### D-COC-03 — Delayed/concurrent D requests must not reopen a gate early (BLOCKING)

A request arriving after the captured D high-water remains behind the closed D gate and must enter a later batch. The protocol must define an atomic owner-local snapshot/high-water operation and a release check proving no unrepresented request exists before D emits `REOPENED`. If D cannot prove the cursor is monotonic after restart/restore, remain closed.

## 3. D gate close/reopen preconditions

D accepts these as mandatory:

1. Before pending acknowledgement, durably persist the local pending cutoff and close admission for all affected target/source/ancestor scopes.
2. Preserve the local request ID, canonical digest, ForgetOperationRef, owner cursor/high-water and local gate generation across restart/failover.
3. Bind the request into the quorum-committed recovery batch without comparing D time/cursor to I or COC.
4. Reconcile every pre-cutoff affected participant and verify complete lineage/producer-work inventory.
5. Ensure each earlier participant has an authoritative C outcome or safe abort, plus the required I terminal decision and Storage same-XID resolution where JF-10 applies.
6. Emit D-signed gate release only for the outage gate, bound to RecoveryEpoch, batch digest, participant-manifest digest and D high-water. This does not declare ForgetFence effective.
7. Separately commit the effective ForgetFenceGeneration only after all D lineage and producer-work barrier obligations are satisfied.

## 4. Recovery Cutoff Batch assessment

- One exact pre-recovery prefix P: **ACCEPT**.
- I and D inventories remain independently ordered: **ACCEPT**.
- Owner high-water and delayed requests: **ACCEPT WITH CONDITIONS**; atomic snapshot/release check needed.
- Participant enumeration: **ACCEPT WITH CONDITIONS**; must be immutable and batch-bound.
- Missing lineage or participant proof: **FAIL CLOSED**.
- Recovery complete versus D gate release versus effective Forget: **must remain three distinct events**.

## 5. JF-10 same-XID bridge impact on D

D accepts the bridge only as participant accounting and evidence observation. COC cannot decide I COMMIT/ABORT, cannot resolve Storage XID, and cannot make D barrier complete. If a D fence cutoff precedes `JF10_PREPARE_INTENT_REGISTERED`, the prepare is rejected. If prepare intent precedes the fence cutoff, D must include the prospective/prepared participant in its exact target/source/ancestor barrier. D cannot make the fence effective until I's exact owner-final-gate decision, Storage's same-XID resolution, C's actual provider outcome where applicable, and all D lineage obligations are proven.

UNKNOWN/IN_DOUBT remains a barrier participant. A COC `RECOVERY_EPOCH_COMPLETED` or owner-local gate release is not a Forget completion event.

## 6. Required D test additions

- D-COC-01: fence request races owner-local high-water snapshot; exactly one request set is bound and later request remains gated.
- D-COC-02: concurrent D requests across target/source/ancestor scopes; no omitted lineage participant.
- D-COC-03: restart/restore of stale D snapshot cannot reopen a gate or reduce D cursor.
- D-COC-04: participant manifest mismatch or delayed participant record leaves barrier open.
- D-COC-05: COC batch committed but D owner reconciliation ACK lost; same request/batch lookup, no duplicate gate release.
- D-COC-06: gate release succeeds but ForgetFence effective transition has not committed; no false completion.
- D-COC-07: IN_DOUBT same-XID participant retains D barrier through all owner restarts.

**Conclusion:** D accepts the intended owner-local cutoff and authority separation with the binding conditions above. The exact proposal is not an unconditional D acceptance until D-COC-01..03 are addressed in a new exact version. No Forget completion, implementation, test pass or production activation is claimed.
