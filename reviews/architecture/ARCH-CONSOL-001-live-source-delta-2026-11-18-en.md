# ARCH-CONSOL-001 — A Integration Live-Source Delta Review
# 2026-11-18 — Draft / Partial, Not Final Acceptance

**Repository:** `oahcom/AiMemoryBrainArchitecture`  
**Review role:** A — System Integration / Architecture Convergence  
**Review branch:** `review/arch-consol-001-live-delta-2026-11-18`  
**Base main SHA:** `282a82e58d8d9d1aa876621481df3184fbe5d284`  
**Base parent:** `ee76e054ccf71bfc3b5d50af6113c699c455852a`  
**Status:** PARTIAL LIVE-SOURCE DELTA — NOT A COMPLETE G1–G8 ACCEPTANCE REPORT  
**Independence:** This is the coordinating A review session, not an independent D, I, Storage, or Integration Reviewer sign-off.

## 1. Scope and hard boundaries

This report refreshes exact live source pins for the current A–I, P and Storage Owner branches and records the material Phase 3.8/3.9 cross-owner deltas visible at those pins. It does not claim that every source file has been reviewed line-by-line, that all G1–G8 evidence has been completed, or that any Owner has approved a normative successor contract.

This workstream is isolated from `main` and all Owner branches. It makes no production changes, no permission/ruleset changes, no workflow dispatch, no merge, and no production activation. The PR carrying this report is intentionally Draft. Commit messages use `[skip ci]` to honor Issue #43's no-workflow-execution constraint.

## 2. Exact live Owner branch pins

| Role | Branch | Exact HEAD |
|---|---|---|
| A | `session-a-integration-2026-11-16` | `8d2d59fff5ebc6077adc470e91d5d8b9684b3b0e` |
| B | `session-b-domain-model-phase3` | `e8a708faa50f7e0ab3f53b11d2f4f2003feced33` |
| C | `session-c-agent-integration-2026-11-16` | `3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c` |
| D | `session-d-memory-brain-2026-11-16` | `b525e1f8fee2471a131e4a38efda99804045e424` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` |
| G | `session-g-memory-context` | `0f77ffbe956c5f93df295c436fcb0a750629d595` |
| H | `session-h-bmcp-protocol` | `654d4449fd491cdda37d9761fe63a3efca55dc9d` |
| I | `session-i-security-governance-2026-11-16` | `029ae8f8f48992532d5c0a9397816e4d8a9220a2` |
| P | `session-p-project-governance-baseline` | `0559a03ccd4f9640ddb7d4af8e37a059930b55af` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `268af57b099209b33835b663596e87d21bb9c22b` |

These are freshness pins only. They do not imply branch integration, semantic completeness, independent review, or Owner acceptance.

## 3. Critical source/Blob ledger

All paths and Blob SHAs below were read from the recursive tree at the corresponding exact Owner branch HEAD in §2.

| Role | Critical artifact | Exact Blob SHA |
|---|---|---|
| A | `reviews/integration/phase-3.8.1-a-contract-surface-and-exact-pin-refresh.md` | `ad5450ea35f6dabc7de1ffa1ea63661f2e500064` |
| A | `reviews/integration/phase-3.8.2-a-race-crash-failover-conformance-matrix.md` | `29125b89ddf47af4c358c0cddbd5c3d6077e1f53` |
| B | `02-domain-model/ADR-001-fact-claim-semantics.md` | `a1024938ff5baba069cf128c69496a44e143330c` |
| B | `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` |
| B | `02-domain-model/lifecycle-model.md` | `81c48c928cb5f9c76ca29d493fbd9479079e62f7` |
| C | `07-agent-integration/phase-3.8.4-c-normative-provider-submit-outcome-contract.md` | `819705037da89834e10b6dd2ec6e66c1b8c70886` |
| C | `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` |
| C | `07-agent-integration/phase-3.8.28-c-exact-review-h-applied-delivery-evidence-csubmitoutcome-join.md` | `7ae8f2609a8786c4a5a715a270faa706156ed462` |
| D | `03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md` | `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` |
| D | `03-memory-brain/phase-3.9-d-forget-terminal-semantics-and-linearization-closure-proposal.md` | `9c02b5680317f0092788ad0da66d621338b1c54c` |
| E | `04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md` | `475fee41e5eea527af4edefbfe88c58c86967d0a` |
| E | `04-memory-compiler/phase-3.8.6-e-review-storage-serialization-anchor.md` | `19d708bc29b6115d7bccb7d320781f452ee28b78` |
| F | `05-memory-runtime/phase-3.8.5-f-storage-logical-serialization-topology-impact-review.md` | `9dae404993d3006e59d2dae88a0a97a3c0998d58` |
| F | `05-memory-runtime/phase-3.8.6-f-review-storage-serialization-anchor.md` | `122238146830db6188f00a9788e018a82bfb3f90` |
| G | `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | `a8efd1aa9696783035e157131fa9751666a4182d` |
| G | `06-memory-context/phase-3.8.26-g-restore-fenced-write-admission-hardening.md` | `d6cd4e8ce18c88ade747eb7d19c6c83840b54792` |
| H | `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` | `1b8f44675f30919764481d33755c566ef5cf1ea8` |
| H | `08-bmcp-protocol/phase-3.8.34-h-owner-gate-release-semantic-reference.md` | `b27dbfe57a7b3a3312d3d8576a74b81e72ac86f7` |
| H | `08-bmcp-protocol/phase-3.8.32-h-unified-1.2.16-owner-snapshot-completeness.md` | `cc40b50d99e329eafa6851049ad0e2cdbba5e955b` |
| I | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | `54bab0484bd232a5a258e65e34cc7425288b39a6` |
| I | `09-security-governance/phase-3.9-i-d-forget-lifecycle-terminalization-authorization-proposal.md` | `362307f6fff84cbe81fb71f37d6319e691db4f89` |
| P | `00-governance/project-decision-authority.md` | `ca3777acae5ceb38a2a421cbf9e738053e4a4057` |
| P | `00-governance/architecture-invariants.md` | `66266667bdbb1cf15a2644fa98db5ecaaf3bb23b` |
| Storage | `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md` | `175ee7b1349cfdb79a19898b311a88391ed88010` |
| Storage | `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` | `bb544ba2f346bdc130d524bd5c7310d86f367988` |
| Storage | `reviews/storage-consistency/phase-3.9-storage-review-d-i-forget-terminalization-and-read-suppression.md` | `1cd9f35f1e28fb5f71cd74599d1560fa36043ed8` |

**Pin status:** Every Blob SHA in this table is the full 40-character Git object ID read from the recursive tree at the exact branch HEAD listed in §2. The branch HEAD and Blob must both be re-fetched immediately before any normative decision because Owner branches remain mutable.

## 4. Cross-owner architecture findings

### 4.1 B Fact/Claim semantics remain a system-level blocker

B's `ADR-001-fact-claim-semantics.md` is still a proposal/decision gap. The Domain Model Overview and lifecycle material use Fact/Claim language that is not yet reconciled with the controlling I-04/P-04 distinction. The system cannot safely freeze canonical memory semantics while the meaning, authority, versioning and conflict behavior of Fact versus Claim remain unsettled.

**A disposition:** BLOCKED. B must publish one exact normative decision, align all dependent schemas and lifecycle references, and identify downstream consumers that require migration.

### 4.2 Lifecycle Manager authority must not overlap I policy authority

The lifecycle model describes Lifecycle Manager responsibilities in terms that can be read as policy, execution, authorization and audit authority. This conflicts with I's ownership of authentication, authorization, retention and legal-hold decisions.

The D/I Phase 3.9 proposals converge on a candidate split:
- D owns canonical lifecycle semantics, state transitions, ForgetFence and the D-side suppression proof.
- I owns authenticated authorization, revocation/PermissionEpoch decisions and the I-side receipt.
- Lifecycle Manager is orchestration/enforcement only, not an independent policy authority.
- Storage owns durable atomic persistence and resolution of commit/UNKNOWN outcomes.

This is a candidate convergence, not an approved normative decision. D and I must approve the same exact successor contract Blob.

### 4.3 Forget terminalization requires four non-interchangeable facts

The D/I/Storage Phase 3.9 documents support keeping these outcomes distinct:
1. D Fence linearization and immediate read suppression.
2. Closure of all pre-Fence participant barriers.
3. D canonical `LifecycleEvent(Forgotten)` and I governance completion/receipt.
4. Physical erasure confirmation.

A durable D Fence must suppress reads at its own linearization point; it must not wait for every old participant barrier to close before read suppression becomes effective. Barrier closeout is a separate completion fact. `CanonicalSuppressionComplete`, `LifecycleEvent(Forgotten)`, `GlobalForgetCompleted` and `PhysicalErasureConfirmed` must not be treated as synonyms.

Storage's Phase 3.9 review is explicitly conditional and same-session role simulation, not an independent Storage Owner signature. D/I/Storage approval is still missing.

### 4.4 Publication Protocol model evidence is materially improved, but remains abstract

Main now includes PR #179, #181, #183 and #186:
- exact Operation identity across D/I/Storage participant and UNKNOWN binding;
- 25 modeled authorization-context positions;
- fail-closed in-memory PermissionEpoch currentness;
- dependency-digest equality checks at I COMMIT_WON, final Storage commit and UNKNOWN reconciliation;
- 61/61 tests on PR #186 exact Head.

These tests establish only deterministic in-memory reference-model transitions and substitution guards. They do not establish authenticated issuer/key status, a live I sequencer or registry, canonical dependency-set digest derivation, authenticated receipts, database durability, transaction isolation, distributed races, crash/failover/restore, or production adapters.

### 4.5 C/H applied-delivery and owner-gate release still require schema-level reconciliation

H's unified 1.2.17 schema and owner-gate release semantic reference improve the COC/JF-10 handoff. C's SubmitOutcome 1.0.1 contract and schema remain separate normative inputs. The cross-owner join still needs exact field-by-field acceptance:
- H's `final_request_boundary_generation` requirement must be reconciled with C's SubmitOutcome contract, where the matching field is not yet evidenced.
- D's dependency cursor/root semantics require D-owned exact semantics.
- I's signed P0 projection and owner-snapshot authorization require I-owned exact fields and evidence.
- H's validator results are not equivalent to production authenticated owner signatures, live quorum or production COC release.

**A disposition:** CONDITIONAL / NOT ACCEPTED. C, D, I and H must agree on the exact field mapping and versioned schema tuple.

### 4.6 Storage topology is only logically selected, not physically proven

The Storage ADR records L1 logical serialization topology Option A as the current selection. L4 engine/deployment topology remains open. A logical owner/transaction boundary does not establish a real database engine, XA/prepared-XID support, durable transaction, isolation level, crash recovery, HA failover or restore behavior.

**A disposition:** CONDITIONAL. Do not claim production atomicity or crash safety until L4 is selected and tested in the actual runtime repository.

### 4.7 G persistence/restore remains reference evidence

G's idempotency, crash/restore and fenced-write admission documents describe important safety rules. They do not by themselves prove a production persistence engine, atomic restore manifest, delayed-fill rejection, replica rebuild, or cross-process fence. The architecture phase may specify these requirements, but production conformance remains NOT RUN.

### 4.8 Runtime implementation binding is deferred, not an architecture-phase blocker

The Project Owner decision in Issue #7 remains `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`. The absence of a canonical runtime repository is not a current architecture-phase blocker. It does mean production implementation and conformance cannot be claimed now.

## 5. G1–G8 status snapshot

| Gate | Current A disposition | Reason |
|---|---|---|
| G1 Exact source inventory | PARTIAL | Current branch heads and selected critical Blob pins refreshed; full 40-character Blob ledger still required for abbreviated entries. |
| G2 Authority/consumer contract | BLOCKED | B Fact/Claim semantics and D/I/Storage/C/H exact field approvals remain unresolved. |
| G3 Cross-owner contradiction closure | BLOCKED | Lifecycle Manager authority, C/H field join, Forget terminalization and publication tuple decisions remain proposals. |
| G4 Race/crash/failover/restore evidence | NOT PROVEN | Matrices and reference models exist; production adversarial execution is not evidenced. |
| G5 Technology/topology decision | PARTIAL | Storage L1 logical Option A selected; L4 physical engine/deployment unresolved. |
| G6 Bilingual/document parity | PARTIAL | Key paired documents exist; this delta is bilingual; full line-by-line parity audit remains outstanding. |
| G7 Independent Owner approval | NOT EVIDENCED | No exact-SHA D/I/Storage approval set or independent Integration Reviewer report evidenced here. |
| G8 Architecture freeze/release | NOT READY | Upstream gates remain open; production activation is not authorized. |

## 6. Governance and integration status

- Current `main`: `282a82e58d8d9d1aa876621481df3184fbe5d284`.
- Open PR inventory at this refresh: 0.
- Main branch protection: `protected=false`; required checks are not platform-enforced. Issue #134 remains OPEN/P0.
- Issue #7 runtime binding decision remains deferred to Engineering Phase.
- AID-2026-001 Owner D approval, Owner I approval and independent Integration Review remain pending; production DFI-001…DFI-022 remain NOT RUN/NOT EVIDENCED; overall Acceptance remains BLOCKED.

## 7. A recommendation

**DO NOT FREEZE / DO NOT AUTHORIZE PRODUCTION ACTIVATION.**

Next required work:
1. Complete the full 40-character exact-source ledger and line-by-line source review for every critical A–I/Storage consumer.
2. Resolve B Fact/Claim semantics and lifecycle authority conflicts.
3. Obtain D/I/Storage exact-SHA decisions for the Phase 3.9 Forget terminalization contract.
4. Obtain C/D/H/I exact field/schema acceptance for COC/JF-10 owner-gate release.
5. Select and prove L4 physical Storage topology.
6. Execute production-boundary race/crash/failover/restore and DFI/R3 conformance in the canonical engineering repository after the Project Owner's deferred binding is satisfied.
7. Obtain three separate D, I and Integration review reports against one frozen normative SHA.

This draft is a bounded live-source delta, not the final system-wide acceptance report. No Owner approval, architecture freeze, implementation authorization or production activation is inferred.
