# Issue #20 — A Integration Readiness Assessment (Coordinator Simulation)

- Review target: Storage proposal Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`, commit `a65973093bb33c7c06ae503f421e096fadb5796b`.
- Status: **FREEZE NOT APPROVED — COORDINATOR INTEGRATION INPUT ONLY**.
- Provenance: Session P role-separated analysis; this is not an A Owner artifact or A's formal integration decision.
- Six role review-input artifacts are coordinator-authored and do not satisfy Issue #20's independent Owner review exit criterion.

## 1. Exact review-input artifacts

| Perspective | Artifact | P commit | Simulated disposition |
|---|---|---|---|
| D — Forget Fence/lineage | `00-governance/reviews/issue-20-d-forget-fence-lineage-review-input.md` | `8dd912d785a0e1ce0724b6615eaf7a9d6c8cabda` | NEEDS REVISION |
| I — inventory/governance | `00-governance/reviews/issue-20-i-inventory-governance-review-input.md` | `f822d241d2ef2b21768a69054fb5b0e8518f6874` | NEEDS REVISION |
| F — Archive/Recall | `00-governance/reviews/issue-20-f-archive-recall-review-input.md` | `f694149f5b2bcd4a411427efed841c2418394534` | ACCEPT WITH ENUMERATED CONDITIONS |
| E — compiler lifecycle | `00-governance/reviews/issue-20-e-compiler-producer-lifecycle-review-input.md` | `32d625f5074e4208358bc64a2d347da8fe4dbd05` | ACCEPT WITH ENUMERATED CONDITIONS |
| G — Context/derivatives | `00-governance/reviews/issue-20-g-context-derivative-review-input.md` | `aa8fb7c7f7b1f331afaa0b8e2192006bd009dda6` | NEEDS REVISION |
| H — BMCP/wire | `00-governance/reviews/issue-20-h-bmcp-wire-contract-review-input.md` | `623938a98d3f5dcb35bb3f12daa51ca7b4c933a0` | NEEDS REVISION |

These are review inputs only. No Owner branch has been modified and no independent decision is claimed.

## 2. Integrated architecture assessment

The proposal's high-level authority split is sound and should be preserved:
- D: canonical Forget coverage, work admission, fence/high-water, dependency closure and barrier terminal/reopen semantics.
- I: authenticated producer/recipient registry, global inventory epoch/seal, PermissionEpoch/revocation, retention exceptions and Global Forget evaluation.
- F: Archive object/revision/manifest, Recall/cursor/cache/index and F-local restore release.
- E: compiler queue/lease/retry/DLQ/replay, staged output and publication lifecycle.
- G: Context/TSS/ContextVersion/compaction/snapshot/delta lineage and G-local restore release.
- H: strict versioned wire schemas, canonicalization and interoperability; I separately owns cryptographic/security policy.
- Storage: physical durability, hidden prepare, WAL/snapshot verification, restore quarantine and final serving CAS.
- A: cross-owner integration only; cannot override any of the above authorities.

The current proposal correctly keeps I's global inventory epoch/seal separate from D's per-Forget work high-water and separates each owner-local release from Storage's final serving gate. Preserve these separations.

## 3. Blocking conflicts and missing contracts

### A1 — D late-lineage and barrier semantics
Archive-only is a provisional classification, not an escape from D. A later EventRef/MemoryRef link must trigger quarantine of the object and all derivatives, retroactive D registration and barrier reconciliation before any disclosure. D must specify what happens if the original barrier has terminalized; a terminal barrier cannot be silently reopened without an append-only D-authorized event/new reconciliation generation.

### A2 — D admission/fence linearization
The phrase “one serialization boundary” needs an exact D owner-local primitive and high-water semantics. Registration and fence installation must have a single total order. D must account for attempt/lease/retry/DLQ/replay paths, not just logical ProducerWorkItemId.

### A3 — I inventory completeness is independently verifiable
A TargetInventorySeal must prove a bounded snapshot of a universe sourced from independent control planes, not merely hash the I registry's own rows. It needs authenticated enrollment, external discovery/reconciliation, positive empty/NotApplicable proofs, pagination completeness, recipient/backup/restore graph and change invalidation.

### A4 — Owner-specific local release
D/I/F/E/G/H/C releases must be independently scoped and typed. Storage's RestoreReadinessManifest and SERVING CAS are final data-plane controls only. Storage cannot infer an owner release from data presence, a stale receipt or another owner's cursor.

### A5 — shared receipt and authority-position registry
Before H freezes, semantic owners must define each receipt's issuer, subject, scope, generation, high-water, digest and terminal meaning. I's epoch, D's fence/work high-water, F cursor/revision, E lease/attempt, G ContextVersion/TSS, H schema version and Storage restore generation/WAL position must remain nominally distinct. No cross-authority numeric ordering.

### A6 — restore readiness manifest and CAS binding
RestoreReadinessManifest must include exact snapshot/WAL prefix digest, restore generation, independent D/I control readbacks, inventory seal, all owner-local release receipts, participant reconciliation root and explicit serving scope. Storage CAS must compare the exact manifest digest and generation; any new inventory epoch, fence, participant or missing receipt fails closed. Lost ACK must query the same RestoreOperationId/generation.

### A7 — evidence boundary
Storage's PostgreSQL capability tests and individual reference models do not establish end-to-end Archive × Forget × Inventory × Restore conformance. Keep implementation, race/fault tests, restore/PITR proof, deployment and production activation as later gates. Issue #4 governance and JF-10 P0 remain separately open.

## 4. Required dependency order

1. **D + I semantics first, independently:** D defines coverage, admission, fence/high-water, lineage closure and terminal/reopen. I defines authenticated registry, independent inventory completeness, seal, invalidation and exception policy. D/I then define a typed join proof without merging authority positions.
2. **F/E/G lifecycle contracts second:** each binds its lifecycle and local release to stable D/I contracts. F/E/G must not invent or weaken D/I predicates.
3. **H wire schema third:** H encodes settled semantic contracts; I approves the security/signature profile. H must provide canonical positive/negative vectors.
4. **Storage realization fourth:** Storage pins exact transaction/restore CAS, WAL continuity, hidden-prepare, participant recovery and no-visible-before-release against the accepted contracts.
5. **A integration last:** A pins all real Owner artifacts, resolves contradictions and issues a formal freeze decision. No coordinator-simulated report can substitute.

## 5. Provisional A-style disposition

**FREEZE NOT APPROVED.** The architecture is directionally coherent, but D/I semantics are blockers, G lineage is a blocker, H wire contracts are absent, and F/E have material conditions. The six independent Owner decisions have not been received. This report cannot be counted as A acceptance.

## 6. Exit evidence required

- D and I append exact decisions on their own branches, with normative replacements and race/negative vectors.
- F/E/G append exact decisions on their own branches and bind their local lifecycle/release contracts to D/I.
- H publishes actual schemas and vectors; H and I agree on the same envelope version.
- Storage publishes a revised exact-version proposal that pins all accepted owner contracts and clarifies the serving CAS/restore evidence chain.
- A publishes a separate integration artifact pinning the six independent Owner artifacts and decides FREEZE APPROVED or FREEZE NOT APPROVED.
- Issue #4 governance approvals and JF-10 P0 remain separate gates.

## 7. Non-claims

No independent Owner approval, formal A integration decision, common interface freeze, implementation PASS, end-to-end test PASS, production database selection, deployment or production activation is claimed. No merge to main or Owner branch was performed.
