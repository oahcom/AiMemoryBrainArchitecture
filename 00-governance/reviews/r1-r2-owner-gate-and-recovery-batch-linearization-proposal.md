# R1/R2 Technical Closure Proposal — Recovery Batch and Owner-local Gate Linearization

- Review ID: P-COC-R1-R2-TECH-001
- Date: 2026-11-17
- Prepared by: Session P coordinator
- Status: **COORDINATOR TECHNICAL PROPOSAL — NOT AN OWNER DECISION; NOT NORMATIVE UNTIL OWNER ADOPTION**
- Source under review: Storage Phase 3.6.3 COC protocol blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- Cross-reference: A exact-version review blob `fdf63550696948f77dc37c0a3788276ac4d525f5`, Issue #14 R1/R2
- Scope: define a testable closure model for owner request capture, owner-local admission gates, in-flight admission and repeated recovery batches. Does not decide I/D owner semantics or select a database product.

## 1. Finding against current Storage text

The current Storage protocol §6.2 requires separate I/D request arrays, completeness attestations, owner high-water marks, participant enumeration and owner-controlled gate reopening. This is directionally correct but still leaves four concurrency semantics unspecified:

1. The atomic point at which an I/D request becomes accepted and the affected local gate becomes closed.
2. How an operation that passed admission immediately before gate closure but has not yet reached COC is durably discoverable.
3. How an owner seals a request-set snapshot while new requests may arrive during reconciliation.
4. How the protocol repeats cutoff batches without a request falling between the final batch and gate reopening.

A single immutable batch can only cover a finite sealed prefix. It cannot safely cover requests accepted after its owner high-water mark.

## 2. Required owner-local durable model

Each owner independently maintains a durable gate row per canonical scope key:

- I scope key: `(PolicyDomainRef, Action/ResourceScopeDigest)`.
- D scope key: `(TargetScopeDigest, SourceScopeDigest, AncestorLineageDigest)`.
- `GateGeneration`: monotonically increasing owner-local generation; never reused.
- `GateState`: OPEN | CLOSED_PENDING_COC | CLOSED_RECONCILING | CLOSED_EFFECTIVE | REOPENED.
- `AcceptedRequestHighWater`: monotonically increasing owner-local request sequence.
- `SealedRequestHighWater`: high-water captured for a specific recovery batch.
- `InFlightAdmissionHighWater`: monotonic sequence for owner-admitted operations that have not yet reached terminal owner/COC registration.
- `ScopeVersion`: monotonic scope-expansion version/digest.
- `LastCommittedRecoveryBatchRef/Digest`: exact COC batch acknowledged by this owner.
- `GateTransitionVersion`: compare-and-swap version for serialized transitions.

The request ledger and in-flight admission ledger are append-only, durable, and queryable by stable operation ID and digest. A missing row is never interpreted as an empty set.

## 3. Owner-local linearization transaction (R2)

For each I or D owner, request acceptance MUST be one serializable owner-authoritative transaction (or equivalent single-writer sequencer/CAS protocol) that atomically:

1. Validates the authenticated request identity, canonical scope and immutable request digest.
2. Deduplicates by `(OwnerAuthorityRef, OwnerRequestRef)`; same digest returns the original accepted sequence, changed digest returns CONFLICT.
3. Allocates the next owner-local request sequence and appends the request to the durable request ledger.
4. Advances `AcceptedRequestHighWater`.
5. Changes the affected gate from OPEN to CLOSED_PENDING_COC (or preserves an already closed state), increments GateGeneration when a new closure generation is required, and commits the scope version.
6. Prevents any competing affected admission/receipt operation from committing through the same serialization boundary.

The transaction commit is the exact **owner-local request/gate linearization point**. The owner MUST NOT acknowledge acceptance before this transaction is durably committed.

All operations that can create protected progress MUST acquire an owner admission record/token in the same serialization domain and MUST fail if the matching scope gate is not OPEN. This includes, as applicable:
- I authorization/receipt issuance and receipt consumption / terminal-decision admission;
- D producer/target/source/ancestor admission and Forget barrier membership decisions;
- any owner-local reservation that could later permit an irreversible side effect.

The gate check and admission-token creation must be atomic with respect to the request/gate transaction. A read-then-write check outside this serialization boundary is insufficient.

### In-flight operation rule

An operation admitted before the gate transaction's linearization point must already have a durable `OwnerAdmissionRef` in the in-flight ledger before the owner acknowledges admission to its caller. The record binds operation ID/digest, scope version, gate generation observed, admission sequence, participant intent (if already assigned), and current phase.

At gate closure, the owner freezes new admissions but does not erase earlier admission records. Every admission with sequence at or below the captured in-flight high-water must be:
- proven already represented in the committed COC prefix and participant manifest; or
- included as a pre-batch owner-local unresolved admission requiring explicit reconciliation; or
- proven rejected before any external/provider/visibility side effect.

If the owner cannot enumerate this set completely, its completeness attestation is false and its gate remains closed.

## 4. Request-set sealing and Recovery Cutoff Batch (R1)

A Recovery Cutoff Batch is a snapshot of two independently sealed owner ledgers, not a best-effort query.

For each owner, the sealing procedure is:

1. Under the same owner-local serialization boundary as request acceptance, read `AcceptedRequestHighWater = H` and `InFlightAdmissionHighWater = F`.
2. Persist a `REQUEST_SET_SEALED` owner record binding GateGeneration, ScopeVersion, H, F, request count, canonical request-set digest, canonical in-flight set digest, and explicit empty/non-empty flags.
3. Return an owner-signed completeness attestation over the sealed prefix `[1..H]` and in-flight prefix `[1..F]`, plus the exact ledger query/version and canonicalization profile.
4. Requests accepted after H receive sequence greater than H and are not silently added to this batch. They remain behind the closed gate and force a subsequent batch.
5. An owner may not revoke or mutate a seal. A changed scope, request digest, ledger root or high-water creates a new seal/batch round; it does not overwrite the prior one.

The COC `RECOVERY_CUTOFF_BATCH` must bind:
- recovery epoch and batch-round identity;
- exact pre-batch quorum prefix position and root digest;
- I and D owner refs, GateGeneration and ScopeVersion;
- I request high-water H_I, in-flight high-water F_I, count, empty flag, request-set digest and owner-signed seal;
- D request high-water H_D, in-flight high-water F_D, count, empty flag, request-set digest and owner-signed seal;
- canonical union digest over both owner sets without imposing a false cross-owner time order;
- complete pre-batch COC participant manifest count, deterministic ordering rule, content-addressed locator and digest/root;
- explicit owner-local admission manifest count/digest for pre-COC unresolved admissions;
- COC quorum commit receipt and exact idempotency key.

An empty set must be represented by count=0 plus an explicit signed empty-set attestation. Missing set/attestation is not empty.

## 5. Repeated cutoff rounds and safe reopening

A recovery epoch may contain multiple sequential cutoff-batch rounds:

`RECOVERY_EPOCH_OPEN → BATCH_n_COMMITTED → RECONCILING_n → OWNER_SEAL_CHECK_n → (BATCH_(n+1) if changed) → RECOVERY_EPOCH_COMPLETED`

The owner gate remains CLOSED_PENDING_COC / CLOSED_RECONCILING for the entire sequence.

After COC participant reconciliation for batch n, I and D independently attempt owner-local gate release using compare-and-swap against the exact sealed state:
- current GateGeneration equals sealed GateGeneration;
- current ScopeVersion equals sealed ScopeVersion;
- current AcceptedRequestHighWater equals sealed H;
- current InFlightAdmissionHighWater equals sealed F, or every later admission is proven rejected/no-side-effect and accounted;
- every request through H has a COC batch reference and owner disposition;
- every applicable pre-batch participant and owner-local unresolved admission is reconciled;
- no UNKNOWN/IN_DOUBT participant or missing proof remains within the owner's release scope.

If any high-water or scope version advanced after the seal, the CAS fails. The owner remains closed and emits a new seal for a subsequent batch. This is the mechanism that prevents the final request from slipping between the batch snapshot and reopening.

I and D release independently, by their own signed durable gate-transition records. A COC record can attest reconciliation but cannot reopen either gate. Temporary outage-gate reopening is distinct from I's effective authorization/revocation state and D's effective ForgetFence/barrier completion.

## 6. Required new record families / evidence

At minimum, H and Storage should jointly map these logical records to one versioned canonical wire contract:

- `OWNER_REQUEST_SET_SEALED` — owner-signed scope/generation/high-water/count/digest/empty-set proof.
- `OWNER_INFLIGHT_SET_SEALED` — owner-signed in-flight high-water/count/digest proof.
- `RECOVERY_CUTOFF_BATCH_COMMITTED` — COC quorum record binding both owner seals, pre-batch prefix and participant manifest.
- `OWNER_GATE_RELEASED` — owner-signed release decision; COC only observes it.
- `RECOVERY_EPOCH_COMPLETED` — COC quorum record only after all required owners released and all required participants are terminal; unresolved count must be zero for SERVING.

If an existing record family is reused, the normative mapping must explicitly define exact semantics and schema version; do not rely on similar names.

## 7. Safety invariants

1. **No admission gap:** every operation is either durably admitted before gate closure and enumerable, or rejected after closure.
2. **No request gap:** every accepted request is in one sealed batch prefix or a later batch prefix.
3. **No empty-set ambiguity:** empty means an owner-signed count-zero seal; absence means unknown/incomplete.
4. **No cross-owner ordering fiction:** I and D sequence spaces remain independent; COC batch position orders the batch, not request arrival times across owners.
5. **No unilateral release:** only I releases I gate; only D releases D gate.
6. **No serving with unresolved work:** any missing request, in-flight admission, participant, lineage, proof, or changed high-water keeps the affected gate closed.
7. **No silent scope narrowing:** scope expansion increments ScopeVersion and invalidates the previous seal for release purposes.
8. **Idempotent retries:** same stable request/batch identity and digest returns original proof; changed digest is CONFLICT.
9. **Crash persistence:** owner gate, request ledger, in-flight ledger and seal survive process restart/failover under the owner's declared durable authority.
10. **Recovery is iterative:** a new accepted request after a seal requires a later batch; it cannot be hidden in an earlier batch.

## 8. Required owner decisions

- **I:** define and accept the I-local sequencer/transaction linearization point, receipt issuance/consumption serialization, request and in-flight ledgers, scope key and I-only release.
- **D:** define and accept the D-local ForgetFence/lineage admission linearization point, producer/target/source/ancestor in-flight enumeration, scope expansion and D-only release.
- **C:** define which C operations require a valid owner admission token and how provider invocation is rejected after gate closure; provider call must remain gated by I COMMIT_WON and D clearance.
- **H:** define canonical schema requiredness, signed empty-set proof, count/digest/locator, replay/conflict and exact owner-vs-COC record mapping.
- **Storage:** define COC record atomicity/idempotency, immutable participant-manifest storage and multi-round recovery epoch state machine.
- **A:** integrate only after the above owner decisions and publish a new exact-version bundle.

## 9. Non-claims

This proposal does not claim any Owner has accepted the algorithm, does not change Issue #14 acceptance, does not implement a database transaction or COC service, and does not authorize Gate B acceptance, Gate C execution, merge or production activation. It is a technical proposal for precise Owner review only.
