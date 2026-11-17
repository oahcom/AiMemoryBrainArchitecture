# System-wide Architecture Risk Register — SYS-RISK-002

- Authority: A — Principal System Architecture Authority
- Version: 1.0.0 (candidate integration baseline)
- Date: 2026-11-17
- Main baseline: `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
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
| AR-01 | L1 logical serialization profile selected; L4 physical engine/deployment proof incomplete | Critical | Yes | Storage + D + I; A integrates | Storage §8 Option A per-Canonical-Authority serializable transaction domain; prove actual DB adapter/product/config, anchor/transition persistence, HA/old-primary fencing, authoritative reads, PITR/restore and physical race/failover | G3/G4; JF-10 A/B/C |
| AR-02 | Fact/Claim/Evidence/temporal semantics not normatively closed | Critical | Yes | B | B-authorized ADR, typed definitions, correction/conflict cases, downstream exact-version adoption | G2/G3 |
| AR-03 | Forget/revocation/restore lacks end-to-end no-resurrection proof | Critical | Yes | I + D + Storage; E/F/G/C/H consumers | Closed-world inventory and owner proofs; both race orders; replay/index/cache/backup/restore tests | G4; Forget gate |
| AR-04 | Publication, provider outcome and Applied proofs do not yet form a complete chain | High | Yes for Applied workflow | C/G/H with I/D/Storage dependencies | Exact owner contracts, final-request boundary, same-key UNKNOWN recovery, conformance | G2/G4 |
| AR-05 | Identity, Scope, delegation and authorization governance incomplete | Critical for protected production use | Yes | I + external governance authorities; B/C/H consumers | I36-GOV-01..10 signed decisions, currentness/revocation evidence, consumer acceptance | G2/G4 |
| AR-06 | JF-10/COC persistent recovery and physical topology incomplete | Critical | Yes | Storage + A/COC + I/D/C | Gate A/B/C evidence, same-XID recovery, quorum/restore/fault traces | JF-10 A/B/C |
| AR-07 | Exact-version drift and candidate schema mismatch | High | Yes for freeze | Each source Owner; A tracks | Current branch HEAD + path + Blob, exact consumer binding, parity and freshness check | G1/G2/G6 |
| AR-08 | Canonical cursor, replay and lineage recovery incomplete | High | Yes for canonical end-to-end claim | D/E/Storage | Durable cursor/outbox atomicity; replay/gap/duplicate/crash tests | G3/G4 |
| AR-09 | Production DR, key custody, operator and RPO/RTO unspecified | High | Yes for production | Storage + I + project operations authority | Deployment ADR, named operator, key lifecycle, backup/PITR/restore drill, RPO/RTO | production acceptance |
| AR-10 | Governance/contract burden may exceed maintainable budget | High | No for bounded preparation; yes for scale commitment | A + all Owners + engineering lead | Measured review cost, automated conformance yield, duplicate state-machine reduction without invariant loss | G5/G7 follow-up |

## Five root risks

1. L1 logical serialization is selected (Storage Option A); actual L4 engine/deployment, authoritative adapter, HA/fencing and restore conformance remain unproven.
2. Canonical domain truth (especially Fact/Claim and temporal/evidence semantics) is not closed by B.
3. Forget and revocation do not yet dominate every derivative, cache, replay, backup and restore path with proof.
4. Identity/security governance and global inventory lack required external approvals.
5. Cross-owner publication, JF-10 recovery and Applied/provider outcome lack complete physical and end-to-end conformance evidence.

## Risk handling

No Critical risk is accepted or waived. High risks AR-04, AR-07, AR-08 and AR-10 remain blocking where they touch mandatory correctness or freeze criteria. Only capability deferrals explicitly listed in the Deferred Capabilities Register may proceed as bounded non-blocking work.

A may accept system-wide scope and sequencing risks; A cannot accept B, D, I, C, G, H or Storage domain risks on their behalf. Each risk remains open until its authority supplies the evidence above and the relevant Gate Owner separately records disposition.

## Cross-references

See ARCH-CX-002, DEV-FEAS-002, DEP-DAG-002, PRIORITY-002, READINESS-002, CONFLICT-002, GATE-002, DEFERRED-002 and FINAL-A-002. All are bound to the same main baseline SHA.
