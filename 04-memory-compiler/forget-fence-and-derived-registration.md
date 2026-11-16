# Forget Fence and Derived Dependency Registration

**Status:** CANDIDATE — E enforcement protocol proposal; D/I authority contracts and H/I identity policy remain OPEN.  
**Owner:** Session E — Memory Compiler.  
**Integration:** INT-P0-03, D-REV-P1-003, INT-X-02, INT-X-03, INT-X-06.  
**Authority boundary:** D owns canonical ForgetOperation/fence identity and canonical suppression; I owns global completion/retention/erasure policy. E owns enforcement in compiler workers and registration of compiler-produced derivatives.

## 1. Safety objective

After a Forget fence is effective, no compiler worker, lease, retry, DLQ replay, recompile, consolidation proposal, derived-output publication or delayed outbox dispatch may expose, commit or recreate affected content. A completed Forget operation must not be followed by a late derivative whose source lineage includes a forgotten target.

Logical suppression, asynchronous cleanup and physical erasure are separate:
- **Suppression:** protected reads, processing and publication are denied immediately by the effective fence.
- **Cleanup:** queued/in-flight work and derived objects are invalidated/deleted or rendered unavailable and acknowledged.
- **Physical erasure:** storage replicas, backups and external copies follow I's policy and evidence. E cannot claim this from a tombstone or local deletion.

## 2. Authority and shared fence contract

E consumes a D-issued, durable fence reference. Candidate shape, subject to D/I approval:

`ForgetFenceRef{forget_operation_ref, fence_epoch, affected_scope_refs, affected_object_refs_or_tokens, effective_at, fence_status}`

- `forget_operation_ref` is a durable D-owned ForgetOperation identity.
- `fence_epoch` is a monotonic D-owned generation in the relevant declared namespace; it is not an Event cursor, canonical commit cursor, index watermark or ContextVersion.
- Scope/target matching and whether the fence is global, scope-partitioned or target-partitioned are **D/I OPEN**. E must not infer broader/narrower coverage.
- I defines authorization, retention exceptions, required targets and completion policy. D defines the canonical suppression fence and producer barrier protocol.
- Until exact D/I contracts are available, E treats fence data as an interface dependency, not a locally invented authoritative schema.

If the fence service or policy epoch cannot be read, a protected dereference, compilation, canonical write proposal, derivative publication, replay or lease renewal fails closed or pauses. Availability pressure does not permit bypass.

## 3. Mandatory check points

Every compiler execution path checks current authorization and Forget fence:

1. ingress acceptance before protected payload dereference (the receipt may be retained as a minimal ingress fact only where I permits);
2. compile-intent dequeue and before payload fetch;
3. before and after lease acquisition/renewal;
4. before every source read, entity resolution, Evidence/Provenance traversal and model prompt construction;
5. before stage-result commit and next-stage outbox creation;
6. before consolidation comparison-set reads and review-task creation;
7. immediately before submitting a canonical write to D (D independently enforces its own fence);
8. before derived object visibility/publication;
9. before every retry, DLQ enqueue/dequeue, operator replay and recompile;
10. before rebuild/backfill that reads or regenerates derived outputs;
11. before acknowledging producer/barrier completion to D/I.

A cached authorization or fence decision is not sufficient unless D/I explicitly supplies a bounded validity contract and E checks the required epoch at the final commit/publication gate. Worker lease includes the observed fence epoch and permission epoch; any mismatch invalidates the lease.

## 4. Derived lineage and dependency model

Every derived object must carry a durable lineage record before it becomes visible.

Candidate relation:

`DerivedDependency{derived_ref, source_ref_or_opaque_token, source_version_ref?, source_digest_ref?, provenance_ref, derivation_run_ref, scope_refs, observed_fence_epoch, registration_ref, state}`

Required properties:
- Each derived object has one or more source dependencies; if source identity cannot be retained, use an I-approved opaque non-reversible token and a recorded unavailability reason.
- Lineage includes transitive parents, not only the immediate compiler input. A summary derived from another summary must retain the upstream source ancestry.
- Method/model/prompt/schema versions and input digests are provenance metadata, not substitutes for source dependency registration.
- Dependency registration is idempotent on `(derived_ref, source_ref/token, provenance_ref, derivation_run_ref)`.
- Cycles are rejected or quarantined; traversal limits may cap operational work but cannot silently omit dependencies needed for Forget completion.
- Cross-scope lineage cannot be used to infer permission; every source and derived target is independently authorized.

### 4.1 Visibility gate

The required ordering is:

1. Create derived object in a private/staged state, not queryable or publishable.
2. Persist source lineage and provenance.
3. Register every source dependency with the D-owned Forget dependency inventory/barrier (or D/I-approved registration service) and obtain durable registration acknowledgement.
4. Re-read current authorization and fence epoch.
5. Publish/transition the derived object to visible only through a gate that proves the registration is durable and the fence epoch is still admissible.
6. If any step fails or is uncertain, leave the object non-visible and retry/reconcile; do not publish optimistically.

The registration must occur **before** visibility. Merely writing a local provenance edge after publication is insufficient.

### 4.2 Closing the check-then-publish race

A local E check followed by an unrelated database write has a race: Forget may become effective between the check and publication. Therefore:
- D must provide an atomic or linearizable `register-if-fence-open` / producer-lease operation and a publication/commit gate tied to the same fence epoch, or an equivalent barrier protocol.
- E registers an in-flight producer/run before it can create externally visible derivatives. The registration remains pending until all derived dependencies are registered and the run is terminal.
- Forget completion waits for all pre-fence producer registrations to finish, cancel or acknowledge suppression. A producer that cannot be reached remains pending/unknown under I policy; it is not silently counted complete.
- A post-fence producer cannot acquire a valid registration token for affected sources.
- A publication using a stale fence epoch is rejected even if its local stage output exists.
- If D has not yet specified the atomic barrier/gate, the final visibility guarantee is **OPEN / BLOCKING**. E must fail closed and must not claim that its local check alone closes D-REV-P1-003.

## 5. Worker, lease, retry and DLQ semantics

- Lease identity is separate from Event, receipt and derivation identity. Lease carries worker/run ID, expiry, attempt, permission epoch and fence epoch.
- A worker that loses its lease or observes a changed epoch must stop before protected reads/writes. It cannot publish on a stale lease.
- Retry resumes the same immutable Event and compile intent with a new attempt ID; it does not recreate the Event or receipt.
- DLQ preserves the original Event/intent identity plus failure class and last safe checkpoint. DLQ storage itself must obey retention/Forget policy.
- Replay is a new attempt under current authorization and fence, not a privileged historical execution. A forgotten source is not dereferenced even if its old payload pointer remains in a queue.
- Recompile pins new compiler/model/schema versions and produces new provenance lineage; it is prohibited for a forgotten or retention-ineligible source.
- Operator override cannot bypass D/I fence. Emergency exception requires an explicit I-owned policy decision and audit record; E cannot mint it.

## 6. Derived-output classes and propagation

Apply the same registration/visibility rule to:
- ExtractionIR, CandidateProposition and entity/relation hypotheses;
- Evidence excerpts, normalized values, embeddings and feature artifacts;
- Provenance nodes/edges and consolidation proposals;
- duplicate/conflict/revision proposals and review payloads;
- summaries, compressed representations and compiler caches;
- canonical write request payloads and publication/outbox envelopes;
- downstream index/context artifacts only through their respective owners' contracts.

For every derivative, propagate the transitive set of source dependency tokens. On Forget, E:
1. marks affected jobs and staged outputs suppressed;
2. cancels or fences leases and retries;
3. blocks source dereference and model prompt reconstruction;
4. sends owner-scoped invalidation/dependency notifications to D/F/G/H as applicable;
5. deletes or restricts derivative content under I's policy;
6. records only the minimum non-reconstructive acknowledgement/tombstone;
7. reports per-target status to D/I without declaring global completion.

E cannot claim F index deletion, G Context reconciliation, H Adapter clearing, backup erasure or I global completion.

## 7. Minimal audit tombstone

A Forget-related tombstone must prove suppression/replay rejection without retaining forgotten content. Candidate minimum:
- opaque random tombstone ID;
- D ForgetOperation reference or I-approved non-reversible correlation token;
- non-reversible target/dependency token(s) only if required for suppression;
- state (suppressed / cleanup-pending / cleanup-acknowledged / unknown);
- policy version and fence epoch;
- timestamps and coarse result/error class;
- integrity/authentication metadata.

Do **not** retain source text, excerpt, normalized proposition, prompt, embedding, reversible payload URI, content-bearing filename, raw content hash where it enables dictionary confirmation, or detailed content-derived labels. Keep raw actor/subject identifiers only if I explicitly requires them; prefer opaque tokens. Tombstone access is restricted and retention/expiry is I-owned. A tombstone is not physical-erasure proof.

## 8. Failure and race matrix

| Race / failure | Required outcome |
|---|---|
| Forget becomes effective before dequeue | Job suppressed; no payload dereference |
| Forget during source fetch/extraction | Cancel/stop; discard staged result or retain only policy-approved non-content tombstone |
| Forget after lease but before stage commit | Epoch/lease invalid; no stage publication |
| Forget between local check and derived publish | D atomic publication gate rejects stale fence epoch |
| Forget during consolidation/review | Proposal/review payload suppressed; no D write submission without fresh fence check |
| Forget after D commit but before E records response | Query D by stable operation key; apply canonical Forget state; never recreate from source |
| Forget during DLQ/replay/recompile | Reauthorize and check fence; reject forgotten source |
| Forget during lineage fan-out | Traverse registered dependency inventory; incomplete traversal remains pending/unknown |
| Worker offline/unreachable at Forget completion | D/I barrier remains pending/unknown unless I explicitly approves an exception |
| Index/Context/Adapter cleanup unavailable | E reports its own target state only; D/I global completion remains open |

## 9. Interface impact

| Producer → consumer | Contract | Owner |
|---|---|---|
| D → E | ForgetOperationRef, fence epoch, affected target/scope semantics, producer registration/barrier, atomic publish gate, completion evidence | D; I policy |
| I → E | principal/actor, permission epoch, retention class, exceptions, audit/tombstone requirements | I |
| E → D | producer run registration, dependency registration before visibility, cancellation/terminal acknowledgement, canonical write with fresh fence epoch | E implements; D validates |
| E → F | derivative/canonical change refs plus dependency/invalidation metadata; no E claim about index cleanup | F owns index behavior |
| E → G | canonical change/forget impact event refs only; no ContextVersion writes | G owns reconciliation |
| H → E | authenticated producer identity and request correlation; no payload-asserted authority | H/I |

## 10. Conformance tests

- Derived object cannot become visible before every source dependency registration is durable.
- Forget racing with producer registration is serialized: producer is either included in barrier or rejected.
- Forget between local precheck and publication is rejected by authoritative atomic gate.
- Stale lease/fence/permission epoch cannot publish, commit or renew.
- DLQ replay and operator recompile cannot resurrect forgotten source or any transitive derivative.
- A derivative of a derivative is suppressed when any required ancestor is forgotten.
- Duplicate dependency registration is idempotent; partial registration remains non-visible.
- Fan-out traversal reports completeness and unresolved targets; it cannot report complete on truncation.
- Tombstone inspection cannot reconstruct source content or confirm guessed low-entropy content.
- Unknown/offline producers remain pending/unknown under global completion policy.

## 11. Open dependencies

- **OPEN — D:** exact ForgetOperationRef/fence schema, epoch namespace, target matching, producer registration and barrier/atomic publish gate; read D branch's authoritative candidate contract before implementation freeze.
- **OPEN — I:** global completion policy, required target set, residual exceptions, retention/tombstone horizon, backup/external-copy and physical erasure.
- **OPEN — H:** authenticated producer/actor binding and wire representation; no H contract assumed.
- **OPEN — F/G:** downstream invalidation acknowledgement semantics; E only publishes notifications.
- **OPEN — Storage/Engineering:** transaction boundary between staged derived object, dependency registration and visibility gate.


## 12. Alignment with D candidate Forget contract (read on D branch)

D's `memory-lifecycle-manager.md` proposes a durable ForgetOperation containing operation/request identity, typed targets, actor/scope, authorization and policy versions, suppression time, dependency snapshot ID/watermark, per-target results, residual exceptions and completion proof reference. It explicitly requires a durable suppression fence before cleanup; a ForgetOperation cannot complete while required targets remain pending/failed. D's `canonical-memory-store.md` also requires Forget suppression to be consulted by canonical reads and projection consumers.

D's current candidate consistency text describes dependency discovery using a snapshot/watermark and recording late-arriving derivatives for follow-up suppression/cleanup. **That is not yet a closed producer-registration barrier or an atomic register-if-open / publish-if-fence-current gate.** The late-derivative race identified as D-REV-P1-003 therefore remains OPEN. E's pre-visibility registration and atomic publication gate above is a required proposal for D/I/Storage to reconcile; E does not claim D has already specified or implemented it.

D's `memory-versioning.md` leaves canonical sequence scope (per aggregate vs global) OPEN. LifecycleEvent per-aggregate sequence and Forget dependency snapshot/watermark are not substitutes for the canonical commit cursor or E source cursor.


## 13. I/H governance alignment

I's Forget policy requires a closed inventory of registered producer/consumer/copy domains, including E queued/leased/retry/DLQ/replay/model jobs and staged outputs. Every producer domain registers stable target class, owner, Scope coverage, supported operations, last processed watermark, online/offline state, retention horizon and evidence capability. A new dependency cannot be silently registered against a sealed target; it must be included in a reopened/reconciled inventory and barrier.

I's no-resurrection proof requires:
1. inventory sealed at a recorded producer-registration epoch;
2. every derivative-capable producer crossed the barrier or is disabled/revoked;
3. all in-flight work at/below the barrier is terminal and cannot publish after the fence;
4. each consumer/partition advanced beyond the required ForgetFence;
5. external recipients/backups are Confirmed or covered by an explicitly approved PolicyException;
6. restore/replay reapplies the fence before content becomes queryable/deliverable.

If an E producer is offline, its target remains Pending/Unknown; E cannot translate unknown into confirmation. An unregistered copy discovered later reopens the inventory and can invalidate a prior completion claim. The exact atomic registration and publish gate remains a D/E/Storage implementation dependency.

I's audit policy requires non-reconstructive tombstones: random opaque IDs, coarse target class, non-reversible restricted partition token, typed suppression fence and coarse state/time. It explicitly disallows raw content, low-entropy or correlatable content digests, embeddings, summaries, provenance edges and plaintext object identifiers/URLs/paths that reveal the forgotten subject. Tombstones are bounded by approved retention and are not eternal IDs by default.

H's `forget-revocation-and-reconnect.md` defines Adapter-local clear/quarantine ACK only. H cannot declare global Forget complete or claim provider-side physical erasure. E's completion evidence is likewise limited to E producer/job/dependency statuses and watermarks. I owns global completion and physical-erasure policy.
