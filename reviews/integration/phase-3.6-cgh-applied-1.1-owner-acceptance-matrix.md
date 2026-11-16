# Phase 3.6 — CGH-APPLIED-1.1 / JF-10 COC Exact Owner Acceptance Matrix

- Owner: A — Principal Integration Architect
- Branch: `session-a-integration-2026-11-16`
- Date: 2026-11-17
- Status: **DESIGN-LEVEL OWNER ACCEPTANCE MATRIX COMPLETE WITH ENUMERATED EXCEPTIONS; NOT FROZEN**
- This is an append-only integration record. It does not mutate the exact accepted candidate artifacts.

## 1. Exact artifacts under review

| Artifact | Exact Blob SHA | Role |
|---|---|---|
| A CGH-APPLIED-1.1 package | `4961ffefc0f9920efb8425a9b2a7af42d8f64819` | Shared Applied/causal-order candidate |
| A COC + JF-10 bridge architecture | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` | Durable causal order / participant accounting / prepared-XID bridge |
| Recovery-batch COC companion pinned by the CGH package | `fc3bac39ec64fda68b8cba5e1aada4e719e5acea` | Owner-local cutoff and recovery-batch design |
| D/E/Storage common JF-10 v2 protocol | `94679897e84a6f58fd8b9467b5249e1a885cb0b0` | Same-XID prepared participant and recovery contract |
| H JF-10 bridge schema candidate | `a8a945cc3623c2907003b93625e3c79742150944` | Five additive 1.1.0 message families |

## 2. Exact owner decisions

| Owner | Evidence artifact | Exact disposition | Scope / retained exception |
|---|---|---|---|
| B | `02-domain-model/phase-3.6-cgh-applied-1.1-b-typed-reference-acceptance.md`, Blob `c3ea570e2d467898f4bc449f2b3b98c8df99778f` | ACCEPT | B-owned typed-reference and namespace semantics only; Fact/Claim ADR-001 remains blocked. |
| C | `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`, Blob `45a48249717c8cddb07ab96197730ef93d406c22` | ACCEPT WITH ENUMERATED EXCEPTIONS | Exact package `4961` + recovery COC `fc3`; exact JF-10 bridge COC `a3c`; provider-specific idempotency and provider recovery unverified. |
| D | `03-memory-brain/forget-fence-operation-and-publication-gate.md`, Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`; plus D causal participant contract Blob `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2` | ACCEPT WITH ENUMERATED EXCEPTIONS | Exact bridge `a3c`; exact recovery-batch package `4961` + `fc3`; D fence/lineage remains D-owned; runtime D ledger not verified. |
| E | `04-memory-compiler/phase-3.6.2-e-jf10-coc-bridge-producer-acceptance.md`, Blob `4503628cf6f6ea46696ab14e7decd3e408ced19a` | ACCEPT WITH ENUMERATED CONDITIONS | E producer identity, immutable manifest, retries, D registration and Storage receipt consumption only; E implementation not verified. |
| G | `06-memory-context/phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md`, Blob `25c1da1f6769165881d217bb0bb492a997e0e14c` | ACCEPT WITH ENUMERATED EXCEPTIONS | G Full Applied predicate/current-use boundary only; G validator/persistence implementation not verified. |
| H | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, Blob `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`, §§12.9–12.10; schema Blob `a8a945cc3623c2907003b93625e3c79742150944` | ACCEPT AS SCHEMA CANDIDATE | Exact package `4961` + `fc3` recovery mapping and exact COC bridge `a3c`; generated schema, parser/SDK interoperability, cryptographic validation and production freeze remain open. |
| I | `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md`, Blob `8069ff86988396442c8d9dc3fd58653683abe2f3`; I COC composition boundary Blob `9e1f66ddbe0952f17068b1638feb8ab0094588c3` | ACCEPT SINGLE-POLICY-DOMAIN BRIDGE WITH BINDING CLARIFICATIONS | I sequencer/receipt and PermissionEpoch remain I-owned; multi-policy-domain atomicity blocked; external governance and inventory seal remain open. |
| Storage | `reviews/storage-consistency/forget-atomicity-storage-realization-review.md`, Blob `107d21bd2c604ee0b04feff2ee5580e1de9c7fce`; COC boundary acceptance Blob `774377d04c8ffbce86c5e915783d6b3d3e5cee57` | ACCEPT WITH ENUMERATED EXCEPTIONS | Exact bridge `a3c` and participant bundle accepted at architecture/interface level; PostgreSQL 18.7 is a qualified CI candidate only; production deployment/operator not designated. |

## 3. Integration determination

All required owner-boundary design decisions for the single-I-PolicyDomain CGH-APPLIED-1.1 / JF-10 COC bridge are now recorded against exact immutable artifacts. The prior candidate package and companion COC pins remain unchanged. The newer A COC bridge artifact `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` is accepted by C, D, E, G, H, I, Storage and B within each owner's stated authority.

**A integration status: DESIGN-LEVEL ACCEPTANCE MATRIX COMPLETE WITH EXCEPTIONS.** This is not an unconditional system acceptance, package freeze, production approval or conformance PASS.

## 4. Non-waived blockers

1. **JF-10 P0 remains OPEN.** The protocol is specified and owner-accepted at the architecture boundary, but I sequencer durability/receipt consumption, COC quorum implementation, D barrier implementation, E producer ledger and Storage/I/D end-to-end recovery are not integrated or proven by a production-equivalent implementation.
2. **COC deployment is not designated or deployed.** The three-voter/two-quorum profile remains a target design; actual failure domains, service owner/operator, KMS, retention, RPO/RTO and operational runbook require engineering/deployment decisions.
3. **Storage Gate A remains partial.** PostgreSQL 18.7 CI probes establish pinned engine capabilities and isolated fixture behavior only. They do not establish production Canonical Authority, real I/D service integration or production fencing.
4. **Gate B is design-authorized, not passed.** Persistent COC log, quorum configuration epoch, participant registry, recovery-cutoff batch, snapshot/restore fencing, read APIs, compaction/retention and crash matrix must be completed as one normative protocol package.
5. **Gate C remains deferred to engineering.** Full multi-process, quorum, network partition, failover, restore and cross-owner fault injection requires executable integrated services.
6. **Multi-I-PolicyDomain atomicity remains BLOCKED / NOT ACCEPTED.** No partial per-domain aggregation or synthetic global success.
7. **H schema remains a candidate.** The JSON Schema artifact parses and has five distinct variants, but is not generated from an executable IDL/source of truth; semantic, canonicalization, duplicate-key, signature/channel-binding and interoperability validation remain outstanding.
8. **External I governance remains blocked.** I36-GOV decisions, ProducerDomainInventoryEpoch/InventorySeal authority, complete producer/recipient/backup/export inventory and Global Forget Completion remain open. No physical-erasure claim.
9. **Fact/Claim ADR-001 remains ADR-BLOCKED.** No canonical domain schema or dependent wire representation is frozen.

## 5. Phase and freeze boundary

- CGH-APPLIED-1.1: candidate remains NOT FROZEN.
- CausalOrderProfile/1.0: architecture accepted with enumerated exceptions; not deployed.
- H bmcp.applied-ack/1.1.0: schema candidate only; NOT production-frozen.
- JF-10: architecture interface accepted for one I PolicyDomain; P0 implementation/conformance remains OPEN.
- Global Forget: governance and target inventory remain CANDIDATE/OPEN; completion NOT CLAIMED.
- Production activation: NOT AUTHORIZED.

## 6. Required next sequence

1. Complete Gate B COC durable protocol design and exact owner readback against one final immutable protocol artifact.
2. Close the remaining Storage Gate A architecture specification, keeping implementation binding explicitly deferred to the engineering phase.
3. Run H schema structural/semantic validation and publish exact conformance fixtures; keep schema candidate status until owner review and interoperability evidence.
4. Reconcile I's global inventory/governance decisions without converting technical JF-10 acceptance into external policy approval.
5. Carry the exact owner-accepted architecture bundle into the engineering phase with a complete implementation/fault-injection acceptance matrix.

**Final:** exact owner-boundary design acceptance is recorded; JF-10, Gate B, production deployment, global Forget and all implementation conformance gates remain open as stated.