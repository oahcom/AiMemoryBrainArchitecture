# Issue #20 — D Role Simulation: ProducerWork Admission and Forget Fence Linearization

**Status:** COORDINATOR-AUTHORED ROLE SIMULATION / PROPOSED / NOT D OWNER DECISION  
**Exact Storage review target:** commit `a65973093bb33c7c06ae503f421e096fadb5796b`, Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`  
**Authority boundary:** This draft proposes D-owned semantics for D Owner review. It is not a D signature, acceptance, implementation, or permission for Storage to define D semantics.

## 1. Classification rule

Every ingress, transform, copy, archive item, restore object and derivative MUST resolve to exactly one of:
- `D_COVERED`: it may create, update, summarize, index, compile, cache or otherwise influence canonical Memory or a D-governed derivative;
- `ARCHIVE_ONLY`: it is provably isolated from canonical Memory and all D-covered derivatives;
- `MIXED_OR_UNKNOWN`: lineage is mixed, incomplete, untrusted or not yet resolved.

Default is `MIXED_OR_UNKNOWN`. Absence of MemoryRef is not proof of Archive-only. An ArchiveOnly assertion requires a signed classification receipt bound to producer identity, work identity, input set, output set, policy version and lineage digest. Any later D-covered ancestor discovery invalidates that assertion and quarantines the object and every derivative until D reconciliation completes.

## 2. Stable work identity

Define a D ProducerWork identity as the immutable tuple:
`(PolicyDomainId, ProducerId, ProducerInstanceId, ProducerWorkId, WorkGeneration, InputSetDigest, OperationKind)`.

Attempt, lease, worker process, retry count and transport request IDs are attributes, not replacement logical work identities. Retries and DLQ replay retain ProducerWorkId and WorkGeneration; a semantic change to the input set or operation creates a new generation linked to the prior work, never an overwrite.

Every D-covered work item must obtain a durable `DProducerAdmissionReceipt` before execution or before any externally observable side effect. Receipt binds the identity tuple, D registry generation, admission sequence, declared ancestors, expected output classes, idempotency key, expiry/lease policy and signer.

## 3. Admission/Fence single linearization rule

D's authoritative admission ledger and Fence state are serialized by one D-owned transactional authority or equivalent linearizable single-writer CAS. For a given PolicyDomain and Forget scope, admission and fence installation MUST contend on the same durable serialization key.

Admission transaction:
1. authenticate producer and resolve classification;
2. check active Fence generation/scope and D authorization;
3. allocate monotonically increasing D admission sequence;
4. append immutable admission + ancestor declaration;
5. commit receipt and sequence atomically.

Fence-install transaction:
1. acquire the same serialization point;
2. close admission for the target scope and increment FenceGeneration;
3. capture the committed admission high-water and unresolved in-flight set digest/count;
4. persist barrier request and closure event atomically;
5. return only after durable commit.

The transaction commit is the linearization point. An admission ordered before Fence closure is in the captured prefix and must be reconciled; one ordered after closure is rejected/quarantined and cannot execute. No “checked open, then later admitted” gap is allowed. If the store cannot atomically serialize both transitions, it cannot claim this contract.

## 4. Dependency closure and publication

Before any output becomes visible, D must durably register:
- all direct input references;
- all transitive D-covered ancestors known at publication;
- output-to-input edges and derivative class;
- producer/work identity and generation;
- canonical content digest and publication intent.

Publication is a two-step private-stage/visible-commit protocol. Staged data is not retrievable. Visibility commit is conditional on unchanged FenceGeneration, current authorization and complete dependency registration. A concurrent Fence causes the visibility CAS to fail and output remains quarantined.

## 5. Late lineage discovery

If a descendant is discovered after a barrier's apparent completion:
- immediately suppress/quarantine the object and all known descendants;
- append a late-lineage event bound to the original Forget operation and new FenceGeneration;
- invalidate the previous completion receipt;
- reopen/reconcile the barrier over the newly discovered closure;
- publish a replacement completion receipt only after all affected work is terminal and independently checked.

No silent amendment to an already sealed set; no release based on the earlier receipt.

## 6. D-local terminal/release predicates

D may release its own Fence only if:
- request set and admission prefix are sealed and complete;
- all pre-Fence admissions are committed, rejected without side effect, or included in the unresolved set and reconciled;
- all direct/transitive descendants are registered and terminal;
- no late lineage remains unresolved;
- D-owned canonical suppression and derivative invalidation are durable;
- the D release CAS confirms unchanged FenceGeneration, scope version and admission high-water.

D release is D-local. It does not release I authorization, F Recall, E compiler, G Context or Storage serving gates.

## 7. Required tests

Admission-vs-Fence race in both serial orders; crash before/after admission commit; crash after Fence closure; retry with same work ID; lease takeover; DLQ replay; late descendant after terminal; mixed Archive/D lineage; publication racing Fence; stale receipt replay; restore of pre-Fence snapshot; missing ancestor; empty work set proof. Every negative case must assert no visibility/no side effect where applicable.

## 8. Open Owner decisions

D must decide exact identity fields, scope key, serialization mechanism, high-water semantics, late-discovery reopening authority, and whether EventRef registration precedes MemoryRef creation. Storage may propose persistence mapping but cannot decide these D-owned semantics.
