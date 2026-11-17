# Exact-version review input — Storage Archive × Forget × Inventory × Restore v1

- Review target Blob: `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`
- Target commit: `a65973093bb33c7c06ae503f421e096fadb5796b`
- Target path: `reviews/storage-consistency/archive-producer-classification-forget-inventory-restore-atomicity-v1.md`
- Review provenance: Session P coordinator role simulation, not an independent module Owner decision.
- Status: Technical review input only; no interface freeze or implementation approval.

## H — BMCP / strict wire contracts

**Simulated disposition: NEEDS REVISION.** H owns exact wire representation, schema evolution, canonicalization and interoperability. I owns signature policy/key governance; each semantic owner defines the meaning of its receipt.

### Findings

1. **BLOCKER — evidence names are not schemas (§7).** Publish strict versioned schemas for ProducerClassificationReceipt, ArchiveManifestReceipt, DProducerWorkRegistrationReceipt, DependencyRegistrationReceipt, TargetInventorySeal, RestoreReadinessManifest, D/I/F/E/G/H/C owner-local release receipts and Storage RestoreReleaseReceipt. Define requiredness, optionality, nullability, field constraints and nominal types.

2. **BLOCKER — authority positions must remain nominally distinct (§§3.1, 4.1, 4.2, 6.2–6.3).** Use distinct opaque types for I PermissionEpoch/ProducerDomainInventoryEpoch/TargetInventorySealRef; D ProducerRegistryVersion/ProducerRegistrationHighWater/ForgetFenceGeneration/WorkItemBarrierRef; G ContextVersion/TSS high-water; E work/attempt/lease positions; F archive revision/Recall cursor; Storage RestoreGeneration/DB incarnation/WAL position; H protocol/schema version. No generic cursor, integer coercion, ordering or equality across authorities.

3. **BLOCKER — signature envelope and digest preimage (§§4.1, 7).** Define canonical serialization, duplicate-key rejection, digest preimage, signer/issuer/subject/audience/purpose, key ID/version, algorithm/profile, scope, owner position, restore generation, manifest digest, expiry/revocation and historical verification. H owns wire syntax; I approves security profile. A signature alone does not establish current authority.

4. **BLOCKER — restore receipt chain (§6.3, 7).** Define separate owner-local receipt schemas and Storage RestoreReleaseReceipt. Each owner receipt binds exact RestoreOperationId/generation, its own typed high-water/epoch, source snapshot/WAL digest, reconciliation manifest and scope. Storage receipt must be emitted only after its serving CAS commits; lost ACK resolves by same RestoreOperationId and manifest digest.

5. **MAJOR — downgrade/unknown-critical/replay (§§7–8).** Specify reject rules for unknown critical fields, duplicate fields, missing required fields, null-vs-empty ambiguity, stale generation, old seal, cross-owner receipt substitution, wrong audience/purpose, revoked signer, digest mismatch, replay and schema downgrade. Include deterministic positive/negative vectors and generated SDK/parser interoperability.

### Required H-owned closure evidence
- Exact H decision pinned to target Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`.
- Versioned schemas and conformance vectors for all named receipts.
- Canonical encoding and typed authority-field registry.
- I-approved signature profile reference; negative vectors for downgrade/replay/substitution.
- Explicit binding to owner semantic decisions and exact A integration bundle.

**Freeze impact:** Blocking. H must not freeze a schema while D/I/F/E/G semantic field meanings remain unresolved.
