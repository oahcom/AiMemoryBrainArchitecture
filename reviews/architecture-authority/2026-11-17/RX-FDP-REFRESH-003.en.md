# Session 4 — R/X/F/D/P Current-Source Reconciliation and Refresh
# Session 4 — R/X/F/D/P 当前源证据对账与刷新

- Report ID: A-RX-FDP-REFRESH-003
- Review date: 2026-11-17
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Requested baseline: `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
- Final observed main HEAD: `901e38ba7b45ed1822eaefddc2da8d765cf8985c`
- Main tree SHA at both commits: `7096e0bc3fdc9a390fccff388f9261522fa424f2`
- Review branch: `review/session-4-a-rx-fdp-currentness-refresh-2026-11-17`
- Status: **CURRENT-SOURCE RECONCILIATION COMPLETE FOR THE PINNED ARTIFACTS BELOW; SYSTEM-WIDE APPROVAL AND G1 COMPLETION NOT ESTABLISHED**
- Authority: A integration review only. R/X/F/D/P are analytical roles, not independent human Owner signatures.

## 0. Executive disposition

**R/X/F/D/P remain usable as analytical inputs, but their original reports are not current-main baselines and must not be cited as if they were freshly rebased.** R already contains a targeted R-01 correction (its §14) that recognizes Storage Option A at L1; X and F/D/P still identify `b372b62...` as their main baseline. PR #50, #49 and #46 remain open Draft PRs based on that historical SHA.

The refreshed system picture is:

1. Storage Option A is selected by the current Storage ADR as the **L1 logical topology**: one serializable transaction domain and durable serialization anchor per Canonical Memory authority. This is not a joint D/Storage approval and does not prove L3 race behavior or L4 physical engine/deployment conformance.
2. B Fact/Claim remains **ADR-BLOCKED**. D/E/I/Storage Phase 3.7/3.8 artifacts are proposals or candidate contracts, not exact jointly approved and implemented contracts.
3. I36-GOV-01..10 remain governance-blocked; the current governance register explicitly says no policy decision is effective without required external approval.
4. H Unified 1.2.15 exists on H's current branch and C has accepted its schema shape with C-owned semantic conditions. C expressly says validator/CI has not yet been reviewed. The H 60-test evidence pinned in Storage v3.3.2 is for H 1.2.14, not 1.2.15.
5. Storage v3.3.2 remains an exact-version manifest for H 1.2.14 / C 1.0.1 and explicitly requires a fresh A review; it does not bind H 1.2.15. A successor manifest and exact Owner re-reviews are required before a unified bundle can be considered.

**Overall architecture disposition remains DEFERRED / ARCHITECTURE_NOT_READY.** G1 is PARTIAL, not PASS.

## 1. Main baseline and delta

The requested SHA `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f` and final observed main HEAD `901e38ba7b45ed1822eaefddc2da8d765cf8985c` have the identical Git tree SHA `7096e0bc3fdc9a390fccff388f9261522fa424f2`. Two commits intervene in history: `ca69d50...` briefly added a research-only B bilingual parity audit and `901e38b...` reverted it. The transient file was read during the G1 audit but is not in current main. Thus the net file delta from the user's requested baseline to current main is zero.

This does not make Owner branches current or approved. Main tree equality is a source-baseline fact, not a proof of Owner adoption.

## 2. Exact analytical report pins and limitations

| Role | Existing PR | Branch HEAD | Report path | Blob | Main base | Currentness |
|---|---:|---|---|---|---|---|
| R | #50 | `8542d608ccfe6747c5f6171a2a38d325f10a628c` | `reviews/architecture/SYS-RISK-001.en.md` | `4067005a65fe528aa7d5fc43ff5be79eb0adaa53` | `b372b62...` | Contains §14 R-01 correction; not a complete current-main rebase |
| X | #49 | `131f91743bd506517ee354d58c277501ca447929` | `reviews/complexity/architecture-complexity-assessment.en.md` | `c509120644d6f7c7223decf3f9f0ee33b0548bb7` | `b372b62...` | Historical source baseline; targeted refresh required |
| F/D/P | #46 | `8b9ff8efa92a88dacc8f97b5faba5918fe5d2edc` | `reviews/engineering-planning/2026-11-17-session-3-engineering-planning-en.md` | `081610b1734ec08dc7c35c75fae1cae3ca713be4` | `b372b62...` | Historical source baseline; source register explicitly says Owner branches not exhaustively rebound |

Chinese peers were also read: R Blob `5fcc55636619d1df373f4caa0afa7db869e4fb70`; X Blob `981a376ddf283ace1e891795c813b17ac4aa3d8b`; F/D/P Blob `834dc39998342dc2f292fe1dfed411768b3ed156`.

All three PRs remain OPEN / DRAFT / unmerged. Their old base does not invalidate the analytical reasoning automatically, but their statements must be revalidated against exact current sources before adoption. This report does not rewrite or retarget those PRs.

## 3. Exact current Owner source snapshot

The following branch heads were read from GitHub branch metadata during this refresh:

| Owner | Branch | Exact HEAD | Relevant exact source / Blob |
|---|---|---|---|
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | `02-domain-model/ADR-001-fact-claim-semantics.md` — `a1024938ff5baba069cf128c69496a44e143330c` |
| C | `session-c-agent-integration-2026-11-16` | `71047cdb51139ca4080ac67f451e38a48698859d` | Phase 3.8.26 H 1.2.15 schema review — `c5ff68814be49ec5e6e2c081004e7fa058d276fa` |
| D | `session-d-memory-brain-2026-11-16` | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | Phase 3.8 publication participant/terminal contract — `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | Phase 3.7 lifecycle proposal — `4fb9e58511941f59b4d777336f8f85ad88ecccf1` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | Branch HEAD read; no new F Owner approval inferred |
| G | `session-g-memory-context` | `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe` | Applied/Forget contract — `aa3afa73d8a76cc6f025839c52bfbff6a983046a` |
| H | `session-h-bmcp-protocol` | `0d36324457e39bd50ad56ae902d477c4ea765b61` | Unified 1.2.15 schema — `860fc4cec658db7d2703cd6adf72aa31a2723f6d`; mapping — `2dc30f193d9c4f4bdc05ca4c137103687db28924`; local validator — `90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0` |
| I | `session-i-security-governance-2026-11-16` | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | Phase 3.7 enforcement proposal — `e3b1b5d99eb36ac0b395854d8c19287d2b64b752`; governance register — `f5fd2558c657f4ef49396a7a00cdbcd0f226f853` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | Option A ADR — `bb544ba2f346bdc130d524bd5c7310d86f367988`; v3.3.2 manifest — `5c614375e10698e4931d83deb57d20321445e068`; Phase 3.7 realization proposal — `2ab899ee37a18ae6c8f2f64dbb82ad6499842060` |

Branch HEADs identify the current candidate source snapshots only. They do not establish Owner approval, branch integration, or runtime implementation. This refresh did not read every file on every Owner branch; it pins the exact artifacts directly relevant to the conclusions below.

## 4. R — System-wide risk refresh

R's existing §14 already corrects the stale statement that no Storage topology has been selected. The correction remains valid against the exact current Storage ADR Blob:

- **L1:** Option A selected in Storage ADR §§8–8.7: one logical serializable transaction domain and durable `CanonicalAuthoritySerializationAnchor` per `BrainAuthorityRef`.
- **Cross-owner D adoption:** not proven. Current D Phase 3.8 artifact is explicitly a D-role proposal; exact Owner approval, callable API and conformance remain OPEN.
- **L3:** race proof not established for both serial orders across ProducerWork/Fence, dependencies, PublicationParticipant and final visibility, including I revocation, retries, lost ACK and recovery.
- **L4:** actual database/build/configuration, authoritative read path, HA/PITR, old-primary fencing, operator and physical crash/failover/restore conformance remain OPEN.

The fundamental risk register therefore remains Critical / OPEN, but the reason must be precise: not “no L1 choice”; rather, **L1 choice exists, while joint adoption, executable logical proof and physical conformance remain absent**.

Other critical risks remain:
- B's Fact/Claim authority and canonical semantics are ADR-BLOCKED.
- Forget/no-resurrection across derivatives, indexes, caches, adapters, replicas, backups and restore remains unproven.
- I governance decisions and closed-world producer/recipient/backup inventory remain unresolved.
- C/G/H Applied must preserve final immutable request identity, actual provider submit evidence, per-request G Applied predicate, late evidence and revocation/fence currentness.
- No runtime repository/accountable engineering owner is designated in Issue #7.

## 5. X — Complexity refresh

X's original rating remains **High complexity; controllability not proven**. Its baseline is stale, but the underlying state-space drivers remain present and are reinforced by the current Owner artifacts.

The highest complexity is concentrated in:
1. D/E/Storage admission, fence, complete dependency registration, private staging and final visibility ordering.
2. Global Forget fan-out and no-resurrection across Canonical, Index, Context, Adapter, replicas, backup and restore.
3. Storage/COC/JF-10 durable participant, quorum, same-GID recovery, failover and anti-rollback.
4. C/G/H final request, provider-side-effect evidence, gateway attestation, Applied idempotency and historical-vs-current validity.
5. I authorization epochs, revocation linearization, issuer trust, cross-scope/environment governance and global completion.
6. B typed domain references and Fact/Claim semantic authority.

A necessary correction to the simplification budget: **do not count the Option A L1 topology decision as still missing**. The remaining complexity is in D/Storage adoption, exact row/transition ownership, same-anchor transactional realization, L3 deterministic interleavings and L4 physical proof. Conversely, the existence of H 1.2.15 schema and local validator code adds candidate artifacts but does not reduce the proof burden until validator/CI, I trust registration and C/G/H exact acceptance close.

Complexity containment:
- Preserve distinct Accepted, Compiler Completion, Canonical Commit, Index Applied, Context Applied, Provider Outcome and Forget completion semantics.
- Do not introduce a service, queue, database or version namespace for every conceptual state.
- Keep the first executable slice narrow and local; defer production vector/ANN, reranking, advanced consolidation and distributed scaling.
- Require one traceable proof object per authority boundary, with explicit idempotency and terminality.

## 6. F — Feasibility refresh

F's broad conclusion remains **FEASIBLE_WITH_CONDITIONS / PARTIALLY VERIFIED**, not implementation-ready.

Current positive evidence:
- A Rust modular-monolith / architecture-only path remains plausible in principle.
- H 1.2.15 schema and local validator implementation exist as candidate artifacts.
- H's 1.2.14 reference ingress bundle has a bounded 60-test CI record in Storage v3.3.2.
- Candidate/reference-model tests and synthetic harnesses can support bounded preparation.

Hard feasibility blockers:
- Issue #7 remains OPEN: no canonical runtime repository, accountable engineering lead, reproducible build/CI and deployment/operator map.
- B Fact/Claim ADR remains ADR-BLOCKED.
- D/E/I/Storage atomic producer admission, complete dependency registration, visibility linearization and exact cross-owner adoption remain OPEN.
- Storage L1 Option A is selected, but L4 physical database and deployment proof is OPEN.
- C/G/H final-request Applied contract and I trust registration remain incomplete.
- I36-GOV-01..10 remain GOVERNANCE-BLOCKED.

Permitted preparatory work only: synthetic benchmarks, Rust workspace/toolchain exploration, candidate database capability probes, reference model/fault harness, conformance test scaffolding and bilingual/source-pin automation. Such work must not be described as protected-path implementation, production conformance or Gate passage.

## 7. D — Dependency and critical path refresh

The dependency ordering is confirmed:

`B domain semantics + I governance/identity + D/E producer/fence/lineage`
→ `Storage L1/L3/L4 serialization and visibility proof`
→ `C/G/H final-request and Applied evidence closure`
→ `minimal durable Canonical vertical slice`
→ `authorized Retrieval/Context/Adapter`
→ `recovery, restore, operational and production conformance`.

This is a partial order, not a mandate that every preparatory task be serial. Synthetic benchmarking, tooling exploration, candidate database probes and bilingual automation may proceed in parallel under explicit non-production constraints.

Do not invert dependencies by building vector/re-ranking features ahead of canonical truth, Forget, authorization and durable visibility.

## 8. P — Root-first priority refresh

| Priority | Work item | Gate condition |
|---|---|---|
| P0-01 | Name canonical runtime repository and accountable engineering owner (Issue #7) | Repository, owner, maintainers, build/CI and deployment boundary recorded |
| P0-02 | Close B Fact/Claim semantic authority | Formal ADR decision with exact approved hash and typed consumer mapping |
| P0-03 | Close I36 governance and closed-world inventory | I36-GOV-01..10 approvals plus signed inventory/exception evidence |
| P0-04 | Close D/E/I/Storage atomic admission, fence, dependency and visibility contracts | Exact same-version Owner decisions, row/API ownership and race/fault conformance |
| P0-05 | Prove Storage/COC/JF-10 physical capability | Actual engine/configuration, durable prepared-XID/equivalent, same-XID recovery, HA/failover, authoritative read and restore evidence |
| P0-06 | Close C/G/H final-request Applied evidence | Exact C/G/H schemas, validator/CI, signer/profile trust, idempotency, late evidence and revocation behavior |
| P0-07 | Build minimal durable Canonical vertical slice | Only after P0-02 through P0-05; bounded authorization and Forget semantics preserved |
| P0-08 | Secure Retrieval/Rebuild | Current I authorization + D fence/lineage + index/Context freshness proof |

P1: event/ingress, compiler, canonical memory, retrieval, context, adapter and Applied integration after their P0 dependencies.

P2: hybrid/vector retrieval, reranking, entity resolution, consolidation and conflict resolution.

P3: high concurrency, distributed expansion, performance optimization and scaled operations.

## 9. C/G/H and Storage exact-version reconciliation

### 9.1 H 1.2.15 candidate

Current H schema Blob `860fc4...` and mapping Blob `2dc30f...` are present on H HEAD `0d363244...`. H's local validator Blob `90a2d4...` explicitly says it does not authenticate outer BMCP envelope, transport principal, channel binding or replay; it is an integration seam with injected authority callbacks, and missing callbacks return UNKNOWN.

C's exact review Blob `c5ff688...` accepts the 1.2.15 **schema shape** with C-owned semantic conditions, but expressly states **VALIDATOR/CI NOT YET REVIEWED**. This is a delegated C-role review, not an independent human C Owner signature.

### 9.2 Storage v3.3.2 mismatch

Current Storage v3.3.2 manifest Blob `5c6143...` explicitly binds:
- H Unified schema **1.2.14** Blob `09fcd1...`;
- CSubmitOutcome 1.0.1;
- the 60-test H reference ingress bundle and associated C/I review pins;
- Option A ADR Blob `bb544b...`.

It does **not** bind H 1.2.15. The 60-test CI result in this manifest is evidence for the 1.2.14 pinned bundle, not for H 1.2.15. The manifest itself says A exact review of v3.3.2 is required and that it is not jointly accepted / not frozen.

Required next step: H publishes exact 1.2.15 validator, test and workflow evidence; C/I complete exact semantic/trust re-review; Storage issues a successor exact-version manifest binding those precise blobs; D and other affected Owners review only the exact successor bundle; A then reviews that same bundle. No predecessor review transfers automatically.

## 10. Issue and Gate evidence

Directly refreshed issue metadata:
- #43 system-wide consolidation — OPEN.
- #7 runtime repository/accountable engineering owner — OPEN.
- #25 D/E/I/Storage atomic producer admission and derivative visibility — OPEN.
- #29 HRC/RecoveryJoin and physical topology proof — OPEN.
- #3 C/G/H Applied contract owner decisions — OPEN.
- #4 I external governance/inventory decisions — OPEN.
- #5 I36-GOV-01..10 formal governance approvals — OPEN.
- #10 JF-10 physical prepared-XID/COC/recovery proof — OPEN.

The controlling state remains:
- G1 PARTIAL, not PASS.
- Gate A PARTIAL PASS / OPEN.
- Gate B BLOCKED.
- Gate C BLOCKED.
- Production authorization NOT AUTHORIZED.

## 11. Updated findings and closure requirements

| ID | Finding | Severity | Blocking | Owner(s) | Closure evidence |
|---|---|---|---|---|---|
| RXFDP-01 | R/X/FDP old main baseline not fully refreshed; reports cannot be treated as current-main approval | High | Yes for G1 completion | A/R/X/F/D/P | Exact source ledger, bilingual parity and current-main re-review |
| RXFDP-02 | Option A selected only at Storage L1; D adoption/L3/L4 remain open | Critical | Yes | D/Storage/I | Joint exact contract, race/fault suite and physical proof |
| RXFDP-03 | B Fact/Claim ADR remains blocked | Critical | Yes | B / Architecture Governance | Formal authority decision with exact hash |
| RXFDP-04 | I36 governance/inventory unresolved | Critical | Yes | I / external governance authorities | Signed I36-01..10 and closed-world inventory evidence |
| RXFDP-05 | H 1.2.15 schema shape accepted conditionally, but validator/CI/trust not closed | High | Yes for Applied closure | H/C/I | Exact validator tests, trusted signer profile and C/I acceptance |
| RXFDP-06 | Storage v3.3.2 binds H 1.2.14, not 1.2.15 | High | Yes for exact bundle | Storage/H/C/I/D/A | Successor manifest with exact blob pins and Owner re-reviews |
| RXFDP-07 | Runtime repository and accountable engineering owner absent | Critical | Yes for implementation entry | Project authority | Issue #7 formal response and implementation traceability map |

No condition is accepted as non-blocking if it touches domain truth, canonical authority, authorization, Forget, atomicity, durable visibility or mandatory Gate proof.

## 12. Explicit boundaries

This report:
- does not approve any Owner proposal;
- does not convert delegated role simulations into independent Owner approval;
- does not freeze architecture, schema, technology or protocol;
- does not authorize protected-path implementation, deployment or production;
- does not merge PRs, close Issues or release Gates.

**Final A integration disposition: DEFERRED / ARCHITECTURE_NOT_READY. G1 remains PARTIAL.**
