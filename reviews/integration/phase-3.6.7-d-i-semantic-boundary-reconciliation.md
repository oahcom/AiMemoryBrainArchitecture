# Phase 3.6.7 — D × I Forget / Global Inventory Semantic Boundary Reconciliation

- Review date: 2026-11-17
- Review scope: D Phase 3.6.6 Forget Semantic Authority Addendum and I Phase 3.6.6 Global Inventory Authority Addendum
- D source commit/blob: `78d51aa1568d011c4274da188a8a50caecd496ab` / `a384ffb4fff7de9b35ba6b3011d2779ad529573d`
- I source commit/blob: `832701ab8768fd65fff70630bd7ffb87805df915` / `d7e34400738b7269929f48d125711ccf045b410b`
- Status: **JOINT SEMANTIC REVIEW; amendments required before cross-owner contract freeze**
- Authority: This is a delegated D/I boundary synthesis. It is not an independent A integration acceptance, external governance approval, or implementation/conformance result.

## 1. Executive disposition

The two addenda are directionally compatible and correctly separate:
- D's per-Forget canonical coverage, fence, work-item barrier, lineage closure and canonical suppression proof; from
- I's PolicyDomain-scoped global producer/recipient/custody inventory, inventory epoch, target seal, completeness proof and global governance decision.

However, one ownership collision and three protocol gaps must be resolved before treating the interface as closed:

1. **Registry authority collision (BLOCKING):** D §3 says D owns the canonical producer-class registry, while I §2–3 says I owns the authoritative global Producer/Recipient Registry and its epoch. Both cannot be authoritative for producer-class membership.
2. **D↔I snapshot binding gap (BLOCKING):** the I seal binds D's fence/target reference and D closure, but the documents do not define a shared, verifiable handshake tuple proving which exact I registry snapshot and D barrier snapshot were reconciled.
3. **Epoch-change race (BLOCKING):** I registry membership/capability changes may occur between D fence installation, I enumeration, D closure reconciliation and I completeness evaluation. Invalidation is described, but the required revalidation point and fail-closed admission behavior are not normative enough.
4. **Restore trust/reconciliation gap (BLOCKING):** both sides mention restore invalidation, but do not define a joint restore release condition binding current I epoch, D fence/control high-water and the exact reconciliation attempt.

## 2. Authority reconciliation — normative ownership

Adopt the following single-authority model:

| Concern | Sole authority | Other side's permitted role |
|---|---|---|
| Global producer/recipient/backup/export/restore-domain membership, authenticated owner and instance identity, role, Scope/PolicyDomain coverage | **I** | D consumes a signed, scope-filtered registry projection; D cannot create or retire global membership |
| Per-operation concrete WorkItem admission ledger, attempt/lease/retry/replay ancestry, ProducerRegistrationHighWater and barrier membership | **D** | I consumes D's signed operation-specific barrier manifest |
| Canonical target identity, source lineage, canonical descendants and D dependency closure | **D** | I reconciles global enumerations against D's closure; I cannot rewrite D lineage |
| Global target universe, recipient/backup/onward-recipient enumeration and TargetInventorySeal | **I** | D supplies canonical target/lineage manifest and owner evidence |
| Permission/authorization, retention policy, exceptions and Global Forget decision | **I / authorized governance authority** | D enforces authorization references and fence semantics; D cannot approve exceptions |

**Required correction:** D's phrase “D owns the canonical producer-class registry” must be narrowed to “D owns the canonical D work-admission registry/projection and per-operation registration ledger for producer classes authorized and identified by I.” I remains sole authority for global producer-class/instance membership. D may reject an unregistered or unmapped producer at its own admission boundary, but cannot mint global identity or membership.

The mapping must be explicit and versioned:
`I InventoryEntryRef + InventoryEntryGeneration + PolicyDomainRef + ScopeBindingFingerprint ↔ D ProducerClassRef + D registration contract version`.
A mapping mismatch, missing I entry, revoked I entry or scope mismatch blocks protected admission.

## 3. Required shared handshake tuple

Every D/I reconciliation attempt MUST bind one immutable tuple:

- `ForgetOperationRef` and normalized request digest;
- `PolicyDomainRef`, exact `ScopeRef` set and inventory boundary;
- D `ForgetFenceGeneration`, fence-installation CanonicalCommitCursor and target-set digest;
- D producer-registry/projection version, `ProducerRegistrationHighWater`, exact barrier-membership digest;
- D dependency-closure digest and reconciliation cursor/generation;
- I `ProducerDomainInventoryEpoch`, registry snapshot digest and change-set digest;
- I per-entry enumeration-manifest root and retrievable member manifests;
- I `TargetInventorySealRef` and seal digest;
- reconciliation-attempt generation, schema/canonicalization version and signer/key references.

Neither side may infer the other side's values. Each authority signs only its own fields; the joint reconciliation receipt contains both signed proofs and their exact cross-references.

## 4. Epoch-change and late-discovery protocol

The following rules close the epoch race without pretending that D and I share one distributed transaction:

1. D installs its fence and captures its own barrier/high-water atomically. D fence remains active regardless of I availability.
2. I issues a signed inventory snapshot attestation for the exact PolicyDomain/Scope boundary and current ProducerDomainInventoryEpoch. I enumerates registry entries and obtains authenticated per-entry manifests against that snapshot.
3. D exposes its signed fence/barrier/closure manifest. I reconciles the global manifests against this exact D evidence.
4. Immediately before I may issue a completeness proof, I revalidates that the inventory epoch, registry snapshot digest, relevant entry generations and evidence validity are still current. If not, the seal/proof is stale and must be rebuilt.
5. D admission for protected work MUST require a currently valid I registry membership mapping for the producer class and MUST check the latest D fence before work execution and before publication. If I membership cannot be authenticated/currently validated, fail closed.
6. A newly registered producer class/instance after the D fence cannot publish against a covered lineage. D rejects or admits only suppression/cleanup work. If discovery shows that the producer or work was already active, D reopens its barrier/closure proof and records the defect.
7. Any I epoch advance invalidates the I completeness proof for the affected inventory boundary. It invalidates D's canonical proof only if the change reveals a D producer/work/lineage omission or contradicts D's closure. The active D fence is never rolled back.
8. A late recipient, onward recipient, backup or external copy invalidates I's completeness proof/seal for current evaluation even if D's canonical barrier remains closed.

The system MUST NOT claim a globally atomic D+I snapshot. It must claim an exact tuple of individually authoritative snapshots plus a currentness/reconciliation check. Any inability to establish currentness is UNKNOWN and blocks completion.

## 5. Restore and release handshake

A restored authoritative serving path remains quarantined until all of the following hold for one reconciliation attempt:

- I proves the current, non-forked ProducerDomainInventoryEpoch and registry snapshot digest using its authoritative sequencer/anti-rollback evidence;
- D proves its current Forget control-ledger checkpoint, fence generation, request cutoff, producer-registration high-water, barrier membership and dependency-closure cursor;
- the restored D and I snapshots are reconciled to the same PolicyDomain/Scope/ForgetOperation tuple;
- all changes after the restored checkpoints are replayed or explicitly accounted for;
- no D barrier reopen, I inventory invalidation, unknown owner/recipient/backup or unresolved target remains;
- the joint receipt is bound to the exact restore attempt and is revalidated immediately before the relevant serving/release transition.

If either authority is unavailable, forked, rolled back or cannot prove freshness, keep the affected serving path fenced. Storage/COC cannot mint D or I proof. I cannot mint D barrier terminal receipts; D cannot mint I inventory seals.

## 6. Required state and proof distinctions

The following states are not interchangeable:
- D `COVERED` ≠ I inventory complete.
- D `CANONICAL_SUPPRESSION_COMPLETE` ≠ I `GlobalInventoryCompletenessProof.COMPLETE`.
- I `TargetInventorySeal.SEALED_COMPLETE` ≠ Global Forget completed.
- Global Forget completion ≠ physical erasure unless the governing policy's physical-erasure evidence is independently satisfied.
- D Barrier Reopen ≠ I inventory epoch advance; either may trigger the other's reconciliation, but each authority controls its own state.
- I registry retirement/revocation ≠ deletion or erasure of the registered target/copy.

## 7. Required amendments before freeze

### D amendment
- Replace global/canonical producer-class registry ownership with an I-authoritative registry projection plus D-owned admission/WorkItem ledger.
- Add I registry entry/generation mapping to D ProducerClassRef and fail-closed admission validation.
- Bind D fence/barrier/closure proof to the exact I inventory snapshot reference observed for reconciliation, without making D responsible for I epoch issuance.
- Define the late producer discovery and restore revalidation consequences exactly as §4–5 above.

### I amendment
- Add a mandatory D/I reconciliation tuple and a signed snapshot-attestation/currentness check.
- Require I to revalidate current epoch and relevant entry generations immediately before completeness proof issuance.
- Define when D proof is invalidated versus when only I proof is invalidated.
- Make restore release depend on both current I inventory proof and D control high-water/closure proof for the same operation/scope.

### Joint acceptance
D and I must each publish an append-only response on their own branch, explicitly accepting or amending these findings and pinning both source addenda by exact commit/blob. A must then perform the cross-owner integration decision. No acceptance is implied by this review.

## 8. Current gate

- D semantic definitions: **PUBLISHED; boundary amendment required**.
- I global inventory definitions: **PUBLISHED; boundary amendment required**.
- D/I authority collision: **OPEN / BLOCKING**.
- D/I shared snapshot tuple and epoch race: **OPEN / BLOCKING**.
- Restore joint freshness/release handshake: **OPEN / BLOCKING**.
- Formal Inventory Governance Approval: **OPEN / NOT APPROVED**.
- Global Forget E2E: **NOT VERIFIED**.
- Production Activation: **NOT AUTHORIZED**.
