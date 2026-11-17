# Issue #20 — D/I Cross-Review and Boundary Reconciliation (Role Simulation)

**Status:** COORDINATOR-AUTHORED CROSS-REVIEW / PROPOSED / NOT D OR I OWNER ACCEPTANCE  
**Storage target:** `a65973093bb33c7c06ae503f421e096fadb5796b` / Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`

## 1. Drafts reviewed

- D simulation: `00-governance/role-simulations/issue-20-d-producerwork-forget-fence-proposal.md`
- I simulation: `00-governance/role-simulations/issue-20-i-global-inventory-seal-proposal.md`

These are coordinator-authored design drafts on Session P, not Owner-branch artifacts or Owner decisions.

## 2. Cross-review findings

### CR-01 — Identity tuple must have one shared typed join key

D's ProducerWork identity includes PolicyDomainId, ProducerId, ProducerInstanceId and work identity. I's inventory identity includes PolicyDomainId, ProducerDomainId, ProducerId, ProducerInstanceId and IdentityGeneration.

**Resolution proposal:** define a shared `ProducerInstanceRef` as the exact typed join key:
`(PolicyDomainId, ProducerDomainId, ProducerId, ProducerInstanceId, IdentityGeneration)`.
D ProducerWork then embeds ProducerInstanceRef plus D-owned ProducerWorkId, WorkGeneration, InputSetDigest and OperationKind. I owns the authority and lifecycle of ProducerInstanceRef; D owns its use in D work registration. IdentityGeneration rollover never rewrites historical D work.

### CR-02 — Classification cannot be decided by I inventory presence alone

I inventory inclusion proves a producer/route is known to governance, not that a specific work item is D-covered or Archive-only. Conversely, D registration does not prove the global universe is complete.

**Resolution proposal:** D signs per-work classification and lineage disposition. I signs universe completeness and producer/recipient enrollment. The join proves identity correspondence only; it must not conflate the two claims.

### CR-03 — Fence and Inventory Seal have independent invalidation domains

D FenceGeneration/admission high-water and I InventoryEpoch/SealGeneration are independent. A D event must not numerically advance I epoch, and an I topology change must not fabricate a D admission.

**Resolution proposal:** every combined operation stores both typed generation references and a join digest. Any change invalidates the combined completion proof and forces re-evaluation by the affected authority.

### CR-04 — Admission must reject stale I identity/authorization

D admission cannot rely on a cached producer identity whose I generation has been revoked or superseded.

**Resolution proposal:** D admission consumes an I-signed authorization/enrollment assertion bound to ProducerInstanceRef, PermissionEpoch, audience, purpose and expiry. D validates freshness/revocation according to an I-defined online or bounded-staleness rule. I must define that rule; D cannot invent it.

### CR-05 — Inventory seal must account for D work not yet represented as MemoryRef

D may have accepted work whose outputs have not yet created MemoryRef. I inventory alone cannot discover all logical work; D's admission ledger must provide the work prefix.

**Resolution proposal:** the Forget completion evidence includes two independent sets: I target universe (producers/routes/recipients/backups) and D work closure (admitted work and dependencies). A typed join maps producer instances, not individual high-water values. D must seal its own work set; I must seal its own inventory set.

### CR-06 — Race between topology change and Forget completion

An I inventory topology change may occur after TargetInventorySeal but before Global Forget completion. Similarly, D admission/late-lineage may occur after D's closure attempt.

**Resolution proposal:** both authorities maintain independent generation-bound completion CAS. Global completion is permitted only when both D and I attest unchanged generations at their respective terminal CAS and the integrator verifies both receipts. If either CAS fails, the operation remains incomplete and re-seals the affected domain.

## 3. Proposed composite evidence object

A non-authoritative integration envelope may bind:
- ForgetOperationId, PolicyDomainId, scope digest;
- I TargetInventorySealRef + InventoryEpoch + SealGeneration + PermissionEpoch;
- D FenceReceiptRef + FenceGeneration + DAdmissionHighWater + DependencyClosureDigest;
- D/I ProducerInstanceRef join digest + unmatched-set digests;
- F/E/G module-local release receipt refs;
- Storage restore/visibility generation and durable commit receipt;
- H schema version/digest and canonical encoding version.

This envelope is not a new authority. It is a typed collection of independently signed Owner receipts. No field may be minted by Storage or A on behalf of D or I.

## 4. Remaining disagreements requiring real Owner decisions

1. D must decide whether classification is per ingress, per work generation, per output, or all three (recommended: all three, with monotonic lineage union).
2. I must decide authoritative inventory sources, freshness limits, online revocation semantics and exception authority.
3. D/I must jointly decide identity generation rollover and treatment of work spanning producer replacement.
4. D must decide exact Fence linearization key and transaction semantics; I must decide seal invalidation CAS semantics.
5. H must not publish final schemas until D/I pin these fields.

## 5. Cross-review verdict

**DESIGN COHERENCE: CONDITIONALLY COHERENT. OWNER ACCEPTANCE: NOT RECEIVED.**

The drafts can be made interoperable if ProducerInstanceRef is shared as a typed identity while D and I retain independent authority, high-water/generation domains and release decisions. The unresolved policy choices above block final schema and Storage implementation mapping.

No issue closure, interface freeze, implementation, CI, runtime conformance, external governance approval or production readiness is claimed.
