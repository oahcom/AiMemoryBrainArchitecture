# System-wide Architecture Risk Register — SYS-RISK-002

- Authority: A — Principal System Architecture Authority
- Version: 1.0.0 (candidate integration baseline)
- Date: 2026-11-17
- Main baseline: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- A review branch: `review/session-4-a-final-architecture-authority-2026-11-17`
- Source assessments: R PR #50; X PR #49; F/D/P PR #46
- Decision status: DEFERRED for architecture freeze; bounded preparation only.

## Evidence pins

| Source | Branch | Commit | Report Blob |
|---|---|---|---|
| R EN | review/session-1-system-wide-risk-2026-11-17 | 8542d608ccfe6747c5f6171a2a38d325f10a628c | 4067005a65fe528aa7d5fc43ff5be79eb0adaa53 |
| R ZH | same | same | 5fcc55636619d1df373f4caa0afa7db869e4fb70 |
| X EN | assessment/x-architecture-complexity-2026-11-17 | 131f91743bd506517ee354d58c277501ca447929 | c509120644d6f7c7223decf3f9f0ee33b0548bb7 |
| X ZH | same | same | 981a376ddf283ace1e891795c813b17ac4aa3d8b |
| F/D/P EN | review/session-3-engineering-planning-2026-11-17 | 8b9ff8efa92a88dacc8f97b5faba5918fe5d2edc | 081610b1734ec08dc7c35c75fae1cae3ca713be4 |
| F/D/P ZH | same | same | 834dc39998342dc2f292fe1dfed411768b3ed156 |

## Risk register

**Live Storage source correction (2026-11-17):** `session-storage-consistency-forget-atomicity-2026-11-16`, `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`, Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`. Section 8 selects Option A for L1 logical architecture; L4 physical engine/deployment remains OPEN. The branch commit SHA was not exposed by the file-read operation and remains a G1 evidence item.

| ID | Risk | Level | Blocking | Accountable authority | Minimum closure evidence | Gate |
|---|---|---:|---|---|---|---|
| AR-01 | Option A conditionally accepted as L1 direction; L1 clarifications and L2/L3/L4 remain open | Critical | Yes | Storage + D + I + A; COC/COC owner as applicable | Close A-01..A-05: transaction executor/write authority; D effect-permit/lifecycle coverage; one BrainAuthority per atomic operation; I COMMIT_WON crash/revocation/replay; independent anchor/DB-incarnation anti-rollback witness; then prove L2/L3/L4 | G1–G5; JF-10 A/B/C |
| AR-02 | Fact/Claim/Evidence/temporal semantics not normatively closed | Critical | Yes | B | B-authorized ADR, typed definitions, correction/conflict cases, downstream exact-version adoption | G2/G3 |
| AR-03 | Forget/revocation/restore lacks end-to-end no-resurrection proof | Critical | Yes | I + D + Storage; E/F/G/C/H consumers | Closed-world inventory and owner proofs; both race orders; replay/index/cache/backup/restore tests | G4; Forget gate |
| AR-04 | Publication, provider outcome and Applied proofs do not yet form a complete chain | High | Yes for Applied workflow | C/G/H with I/D/Storage dependencies | Exact owner contracts, final-request boundary, same-key UNKNOWN recovery, conformance | G2/G4 |
| AR-05 | Identity, Scope, delegation and authorization governance incomplete | Critical for protected production use | Yes | I + external governance authorities; B/C/H consumers | I36-GOV-01..10 signed decisions, currentness/revocation evidence, consumer acceptance | G2/G4 |
| AR-06 | JF-10/COC persistent recovery and physical topology incomplete | Critical | Yes | Storage + A/COC + I/D/C | Gate A/B/C evidence, same-XID recovery, quorum/restore/fault traces | JF-10 A/B/C |
| AR-07 | Exact-version drift and candidate schema mismatch | High | Yes for freeze | Each source Owner; A tracks | Current branch HEAD + path + Blob, exact consumer binding, parity and freshness check | G1/G2/G6 |
| AR-08 | Canonical cursor, replay and lineage recovery incomplete | High | Yes for canonical end-to-end claim | D/E/Storage | Durable cursor/outbox atomicity; replay/gap/duplicate/crash tests | G3/G4 |
| AR-09 | Production DR, key custody, operator and RPO/RTO unspecified | High | Yes for production | Storage + I + project operations authority | Deployment ADR, named operator, key lifecycle, backup/PITR/restore drill, RPO/RTO | production acceptance |
| AR-10 | Governance/contract burden may exceed maintainable budget | High | No for bounded preparation; yes for scale commitment | A + all Owners + engineering lead | Measured review cost, automated conformance yield, duplicate state-machine reduction without invariant loss | G5/G7 follow-up |

| AR-11 | B/H/C/D/I/Storage exact protocol bundle is stale/incompletely joined | High | Yes for protocol freeze | H + C + D + I + Storage; A integrates | H current D-crosswalk mapping and C re-review; H current I P0 review and I anchor refresh; H mapping disposition/CI currentness; Storage v3.3.0 or successor manifest reviewed by C/H/D/I and A | G1/G2/G6 |

## Five root risks

1. Option A is conditionally accepted only as the v1 logical direction; L1 A-01..A-05 clarifications, L2 contract composition, L3 concurrency proof and L4 physical deployment remain open.
2. Canonical domain truth (especially Fact/Claim and temporal/evidence semantics) is not closed by B.
3. Forget and revocation do not yet dominate every derivative, cache, replay, backup and restore path with proof.
4. Identity/security governance and global inventory lack required external approvals.
5. Cross-owner publication, JF-10 recovery and Applied/provider outcome lack complete physical and end-to-end conformance evidence.

## Risk handling

No Critical risk is accepted or waived. High risks AR-04, AR-07, AR-08 and AR-10 remain blocking where they touch mandatory correctness or freeze criteria. Only capability deferrals explicitly listed in the Deferred Capabilities Register may proceed as bounded non-blocking work.

A may accept system-wide scope and sequencing risks; A cannot accept B, D, I, C, G, H or Storage domain risks on their behalf. Each risk remains open until its authority supplies the evidence above and the relevant Gate Owner separately records disposition.

## Current source refresh against main@6470f25 (2026-11-17)

- Main adds `canonical-identity-semantics.md` Blob `403105e130353884a6369b3d091e2284ee9f1c2c` (CANDIDATE; cross-owner binding OPEN) and `canonical-domain-entity-inventory.md` Blob `2e0d45dfef9db2ddee19493cd274194312ad6332` (CANDIDATE INVENTORY; B1 IN PROGRESS). B Fact/Claim ADR Blob `a1024938ff5baba069cf128c69496a44e143330c` remains ADR-BLOCKED.
- B→A review PR #52: branch HEAD `2727bd8544f812d796186769f86cf92aba244dee`, report Blob `b59b2ef745330f901027f59b69c68b99097c604b`.
- Option A review PR #54: branch HEAD `208c5e84f64ec68338045b963407bcb6d2463faf`, report Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`; proposed amendment Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525` is NOT ADOPTED.
- B protocol alignment PR #51: branch HEAD `042f60217903215b75251bc36a650d7a4c994704`, evidence ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`. Candidate H 1.2.14 / wire 1.3.0 + CSubmitOutcome 1.0.1; v3.2.9 manifest Blob `bf323a1682f2bfadc3ff41ea4f86883d678a77e3` is stale against later C/D/I review and H CI pins.
- Exact candidate source Blobs: H schema `09fcd1fa29fe24255fbd87cae79dafb406594a59`; C schema `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`; H mapping `c196fdc7a9d88e344d37ba2810a9bce1803f8b96`; C re-review `f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c`; D review `55ae7bc33b37f0e729949fdd2a694eb6211bbc55`; I P0 `44986f5f864bcdc1a79d34978273644d381a68c0`; I anchor review current Blob `f22d31dec3a95f094c2942ab816c830f007e830e`; Storage topology ADR `bb544ba2f346bdc130d524bd5c7310d86f367988`.
- H CI currentness correction: run `44069941327`, commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251`, job `133993324484`; H branch HEAD cited by PR #51 ledger: `362cc113cfb5b595a4002a6f6e980d19ae2d2d15`. Storage branch HEAD cited by the same ledger: `39a1e0429f6b4b08c6c437c8e3f5ace582a7315f`.
- PR #51 says v3.2.9 is stale; Storage must publish v3.3.0 or equivalent, then C/H/D/I review the identical manifest and A re-reviews. Exact manifest branch path/commit must be pinned by Storage; do not hand-edit Owner branch.

## Cross-references

See ARCH-CX-002, DEV-FEAS-002, DEP-DAG-002, PRIORITY-002, READINESS-002, CONFLICT-002, GATE-002, DEFERRED-002 and FINAL-A-002. All are bound to the same main baseline SHA.


## Source freshness / assessed baseline

This assessment's source-evidence baseline is pinned to main commit `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. At publication, the observed main HEAD is `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f` (a later revert commit); this later HEAD is not silently substituted for the assessed baseline. Before any Gate closure or freeze decision, refresh every cited Owner artifact and repeat the delta review against that HEAD. The Storage L1 topology source is separately pinned to Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`, branch `session-storage-consistency-forget-atomicity-2026-11-16`; §8 selects Option A for L1, while L4 physical conformance remains OPEN.
