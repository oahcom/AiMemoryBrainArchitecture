# Exact-version review input — Storage Archive × Forget × Inventory × Restore v1

- Review target Blob: `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`
- Target commit: `a65973093bb33c7c06ae503f421e096fadb5796b`
- Target path: `reviews/storage-consistency/archive-producer-classification-forget-inventory-restore-atomicity-v1.md`
- Review provenance: Session P coordinator role simulation, not an independent module Owner decision.
- Status: Technical review input only; no interface freeze or implementation approval.

## I — Security / producer & recipient inventory / governance

**Simulated disposition: NEEDS REVISION.** I owns authenticated identity, global inventory completeness, PermissionEpoch/revocation, TargetInventorySeal, retention exceptions and Global Forget evaluation. This review cannot approve Issue #4 governance requirements.

### Findings

1. **BLOCKER — closed-world inventory is asserted, not proven (§§3.1, 4.1).** A registry cannot prove its own completeness by enumerating itself. Define authoritative enrollment sources, authenticated producer/instance attestation, deployment/account/tenant discovery, control-plane reconciliation, independent inventory source(s), inventory freshness and drift detection. Unregistered or unreachable producers, recipients, restore targets and backup routes must remain UNKNOWN and block closure.

2. **BLOCKER — TargetInventorySeal lacks a complete normative encoding (§§4.1, 4.3, 7).** Specify canonical target-set ordering and digest preimage; partition/shard and pagination completeness; snapshot boundary; inclusion/exclusion reasons; positive empty-category evidence; signer, verifier and authority; validity interval; revocation/invalidation sequence; and reproducible independent verification. “Empty” and “NotApplicable” require positive evidence, not omitted rows.

3. **BLOCKER — I-to-D coverage join (§§3.2–3.3, 4.3).** Define a signed/immutable mapping for each ProducerClassRef + ProducerIdentityRef + instance + scope to D registry version/work coverage or a positive D-approved non-applicability proof. Class, capability, owner, scope, issuer, recipient, backup or restore route change must invalidate the affected seal and any Global Forget evaluation using it. Do not merge I epoch with D high-water/generation.

4. **BLOCKER — recipient and copy graph (§§4.1, 6.2).** Inventory direct recipients, onward recipients, provider-managed copies, caches, replicas, snapshots, WAL, offline buffers, backup media, exports, restore clones and operator-access paths. Unknown onward route or unverified external recipient must block closure. ACK receipt is not evidence of downstream deletion.

5. **MAJOR — retention/legal hold/crypto-erasure conflict (§§3.1, 4.1, 6.2).** Define exception authority, scope, reason, data minimization, retention duration, review/expiry and evidence separation. A retained audit proof must not retain payload or be counted as deletion. Define key destruction evidence separately from physical erasure and backup expiry.

6. **BLOCKER — Issue #4 governance remains independent (§9).** This proposal and this review do not grant privacy/legal/security approval, waive policy-domain restrictions or claim Global Forget completion. Explicitly carry the governance dependency and evidence owner.

### Required I-owned closure evidence
- Exact I decision pinned to target Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`.
- Registry source-of-truth and independent completeness/reconciliation model.
- TargetInventorySeal schema semantics and verifiable positive absence/NotApplicable evidence.
- Change invalidation matrix and I/D join proof.
- Recipient/backup/restore inventory, retention exception and Global Forget evidence vector.
- Negative vectors for unknown issuer, unregistered instance, stale seal, newly added recipient, missing backup shard, incomplete page, owner/scope drift, revocation during restore.

**Freeze impact:** Blocking. I's closed-world and seal semantics must be settled before H wire freeze or Storage serving release.
