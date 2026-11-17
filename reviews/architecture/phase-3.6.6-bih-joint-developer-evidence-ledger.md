# Phase 3.6.6 — B/I/H Joint Developer Evidence Ledger and Closure Requests

- Owner boundary: B/I/H delegated joint technical coordination only
- Branch: `session-b-domain-model-phase3`
- Snapshot date: 2026-11-17
- A acceptance authority: `reviews/integration/phase-3.6-final-closure-plan.md`, Blob `0adca0f54ff6ee1e344949cb48334ff475fad247`
- A tracking ledger read: `reviews/integration/phase-3.6-closure-tracking.md`, Blob `e4f45cbee7c8f76de4a0ac1b5939db54a8c7cf7f`
- A final acceptance read: `reviews/integration/phase-3.6-final-architecture-acceptance.md`, Blob `16f86859645447f3f4397c5c89c6013c3cce92b5`
- A current CGH-APPLIED-1.1 owner matrix: Blob `ee35d3b39cb1fddd1feee0e0504b77e73e376893`
- This ledger is a B/I/H-owned coordination record, not an A gate decision and not an approval on behalf of another Owner.

## 1. Current branch-head snapshot

All discoverable repository branches were refreshed from the live branch listing. Owner branches remain independent; `main` is not authoritative for Owner decisions.

| Owner / branch | Current HEAD |
|---|---|
| A — `session-a-integration-2026-11-16` | `0afaeac9e206daf79aca69fb12830b30a1ffc2c7` |
| B — `session-b-domain-model-phase3` | `052eefc3c5724b9f4a8b7cb28927746cb0da7113` |
| C — `session-c-agent-integration-2026-11-16` | `c408d2c138d1975eff1167bd5889ba45a13b126b` |
| D — `session-d-memory-brain-2026-11-16` | `f5cbe59561b73c75708a52f28b0bf12707d75c71` |
| E — `session-e-memory-compiler-2026-11-16` | `fb063e15ee31569e501f5fa0a3198b3cf0b67a9c` |
| F — `session-f-memory-runtime` | `86c013814fbbfff1829729eb18fdc3a5de265969` |
| G — `session-g-memory-context` | `466e2bf5992ea5944ef6ecebd79a39eeb21cdc97` |
| H — `session-h-bmcp-protocol` | `872b6354971386cdcd278b77f3d9eb3af6d61c4a` |
| I — `session-i-security-governance-2026-11-16` | `905cb7753a27ad6fe420b9d5372b9bca15caa713` |
| Storage — `session-storage-consistency-forget-atomicity-2026-11-16` | `f0f9d9fefd31251fc1ee27e543d4351f398627e8` |
| P — `session-p-project-governance-baseline` | `ec2d88f1c9fa742d4b3c270b9defa08d23db0eaf` |
| CI — `ci/jf10-postgres-18.7-capability-run` | `b58d7c5a87c5194384a5d06bed62cb63b746662c` |
| main (non-authoritative) | `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f` |

## 2. A G0–G10 gate ledger

The state column below preserves A's published gate state. Where new evidence satisfies a subrequirement, this ledger records it and requests A's reconciliation; it does not silently change A's authoritative state.

| Gate | A plan state | Exact evidence / current finding | Blocker and responsible authority | Next required action |
|---|---|---|---|---|
| G0 Baseline Integrity | PASS | All live Owner branches refreshed in §1; relevant A/B/I/H/Storage source Blobs re-read in this run. A ledger Blob `e4f45...` still carries older branch-head/package pins. | A owns the final baseline registry. | A refresh its own full artifact inventory and replace stale snapshots before final closure. |
| G1 DE-S Design Closure | PASS | A plan Blob `0adca0...`; BIH36-JD-01..17 preserved. Fact/Claim ADR-001 remains independently ADR-BLOCKED. | B owns ADR-001; I/Environment Registry authority owns identity/inventory policy. | Resolve ADR-001 only with actual authority/evidence; do not infer from this type update. |
| G2 DE-S External Dependency Approval | BLOCKED | I register Blob `2fdd5a03678fe5bb000715cf8e58ac35d3126ac8` still separates technical I decisions from I36-GOV-01..10. Storage readiness Blob `a66499765bb2032fc769d1e2028e2a29c3625c75` says production Canonical Authority deployment/operator is not designated. | I + named external governance approvers + Storage deployment authority. | Produce effective I36-GOV approvals, Environment Registry Authority, InventorySeal/ProducerDomainInventoryEpoch authority, AuthorizationCommitPermit/revocation serialization, and an accountable Storage deployment decision. |
| G3 DE-S Implementation Verification | BLOCKED | Storage Gate A is PARTIAL PASS for pinned PostgreSQL 18.7 CI capabilities; Gate B prior protocol revision `4ac63...` was design-accepted, but current amended protocol Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` requires focused exact-owner re-review; Gate C is deferred to engineering. D36/E36/C01–C20 application suites are NOT RUN. | Storage, D, E, C, I and the designated engineering owner. | Storage reconcile §14 with v3; then engineering-phase implementation, durable receipts, authoritative reader, D/E integration and reproducible D36/E36/C01–C20 execution. |
| G4 BIH Technical Agreement | CONDITIONAL PASS | B registry Blob `e7a1ced41421230bd41a3f68a1074bd95721adc0`; B review Blob `00d36dc348d2e0ff8f2a281cd71bb9b7ceb3391b`; I review Blob `e73b94a46a762ba524292d419fc963203502ffc7`; H review Blob `7d46ffcc5380a3abc102c0a13096583cb23126cd`. BIH36-JD-01..17 unchanged. | B/I/H technical boundaries accepted with amendments; Storage v3 and companion §14 still diverge; I security profile not frozen. | Storage publish one normative tuple; I/H reconcile signature profile and exact proof binding; A record the exact current owner artifacts. |
| G5 BIH Governance Approval | BLOCKED | I register Blob `2fdd...` retains I36-GOV-01..10 as GOVERNANCE-BLOCKED. I's v3 review is technical only; no external approver or signature is supplied. | I + independent Identity/Security/Privacy/Legal/Environment authorities. | Obtain effective approvals, exact policy hashes, jurisdiction/scope, approver authority and effective versions; do not convert technical acceptance into governance approval. |
| G6 BIH Consumer Acceptance | BLOCKED in A plan; evidence subrequirement now COMPLETE | I register §11 Blob `2fdd...` records current branch readbacks: C `fd2f47...`, D `184423...`, E `6f410...`, F `ce592...`, G `aa3afa...`, Storage `ec8e49...`; H's own acceptance `ccbac2...`. C/D/E/F/G/Storage accept BIH design with exceptions. | A must reconcile its G0–G10 plan/ledger. | A verify the listed current branch Blobs and update G6; no runtime PASS is implied. |
| G7 BIH Test Verification | NOT RUN | H's separate structural schema suite passed 47/47 (run `44000078669`, job `133761649293`, commit `d26a40e2483e32a6afb1e8f9ccd456e8ae3c815c`). I36/H36, D36/E36 and integrated JF-10 remain NOT RUN. | I/H and consuming runtime Owners. | Execute I36/H36 and owner-specific suites on identified builds with fixtures, raw logs, expected/actual results and reviewer sign-off. |
| G8 CFG Applied Contract Freeze | BLOCKED | A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`; owner matrix Blob `ee35...` says design-level acceptance complete with exceptions; COC bridge Blob `a3c51...`; recovery companion Blob `fc3bac...`. H Applied ACK schema Blob `a8a945...` has five variants while A package §4 enumerates eight evidence families. New Storage proof schema Blob `6327d9...` is a separate two-message family and does not close that gap. | A/C/G/H and D/I/B predicate Owners. | H publish exact one-to-one mapping or additional versioned families for Reservation, D fence terminal, C submit outcome, CausalOrderTerminalProof and COC ACK; link Storage proof family; A freeze only after exact same-version readback. |
| G9 CFG Runtime/Security Verification | NOT RUN | CFG-01..20 and PI-01..08 have no verified execution evidence. H 47/47 structural tests do not count as CFG/H36/I36 execution. | C/G/H/I/D/B plus engineering/test owners. | Run the full race, replay, key/authorization, fence, provider, restore and current-use suites with reproducible build/fixture/log evidence. |
| G10 Overall Implementation Readiness | BLOCKED | G2/G3/G5/G7/G8/G9 remain blocked/not run; JF-10 P0 remains OPEN; ADR-001 remains ADR-BLOCKED. | A final integration authority plus all named Owners/governance authorities. | No final acceptance until every required gate is closed with exact evidence. |

## 3. Current B/I/H work products and verification

### B — Domain Model

- Branch HEAD: `052eefc3c5724b9f4a8b7cb28927746cb0da7113`.
- Typed reference registry: Blob `e7a1ced41421230bd41a3f68a1074bd95721adc0`.
- Exact Storage v3 type review: Blob `00d36dc348d2e0ff8f2a281cd71bb9b7ceb3391b`.
- Added DatabaseIncarnationRef, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version, ParticipantTupleDigest and PostgreSQL-specific nominal mappings.
- Explicitly distinguishes PreparedTransactionGID from PostgreSQLNativeXID and from engine-neutral EngineNativeTransactionXIDRef.
- Requires complete lookup key (CanonicalAuthorityDBRef, DatabaseIncarnationRef, PreparedParticipantRef, PreparedTransactionGID).
- Fact/Claim ADR-001 remains ADR-BLOCKED.
- B runtime type validator: NOT RUN; no B executable domain-model harness identified.

### I — Security & Governance

- Branch HEAD: `905cb7753a27ad6fe420b9d5372b9bca15caa713`.
- Storage v3 security review: Blob `e73b94a46a762ba524292d419fc963203502ffc7`.
- Governance/consumer register: Blob `2fdd5a03678fe5bb000715cf8e58ac35d3126ac8`.
- I review accepts the I-owned v3 semantics with amendments: serializable owner-local gate close, exact request high-water/generation, in-flight receipt classification, exact attempt/ledger binding, independent anti-rollback anchor, and historical key-status verification.
- ABORT_WON is not an I terminal outcome; accepted I vocabulary is COMMIT_WON, REVOCATION_WON, INDETERMINATE_ABORTED, with UNKNOWN/IN_DOUBT nonterminal.
- Candidate signature domain separation is proposed only; algorithm suite, key custody and governance remain unapproved.
- I36-GOV-01..10 remain GOVERNANCE-BLOCKED; I36 execution NOT RUN.

### H — BMCP Protocol

- Branch HEAD: `872b6354971386cdcd278b77f3d9eb3af6d61c4a`.
- Storage proof schema candidate: Blob `6327d9d387bdc0d6610aba08ff3e51ca9da17f5d`.
- Structural test file: Blob `f8de63379d4d411ff9c9831f25294e4c8b09f158`.
- Workflow: Blob `f9a8a403b4fd523a065c0aee6c51f3575c4270a2`.
- H exact v3 wire review: Blob `7d46ffcc5380a3abc102c0a13096583cb23126cd`.
- CI: run `44000078669`, job `133761649293`, exact schema/test commit `d26a40e2483e32a6afb1e8f9ccd456e8ae3c815c`; Python 3.12, jsonschema 4.23.0, compile succeeded, `python -m unittest discover -s tests/schema -v`: 47 tests, all PASS.
- Scope: structural JSON Schema/parser reference only. No signature verification, canonical-byte interoperability, production transport, owner-authority lookup or H36 PASS.
- H Applied ACK 1.1.0 remains a five-variant candidate; full CGH family mapping is incomplete.

## 4. Cross-owner technical contradictions requiring Storage/H/I action

1. **Storage v3 vs companion §14:** v3 Blob `4a60420d457f359780c568dce42b8bef000026ca` requires DatabaseIncarnationRef, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version and ParticipantTupleDigest. Companion §14 Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` omits them. Storage must amend §14 or explicitly supersede it.
2. **I proof tuple incomplete:** v3 §15.7 does not explicitly enumerate attempt/generation and participant-ledger ref/version. I requires the atomic receipt-consumption proof to bind the exact PreparedParticipantReceipt digest, participant tuple digest, attempt/generation, ledger version and owner-final-gate participant.
3. **Outcome vocabulary conflict:** v3 §7.3 uses ABORT_WON; I/H current enum does not. Storage must remove it or I must issue a separately approved new outcome. Until then ABORT_WON is rejected.
4. **I owner-local gate linearization:** v3 §6.1 does not state the exact serializable PolicyDomain sequencer transaction that closes issue/consume gates, increments generation and captures request high-water. I's review supplies the required transaction semantics, but no I service implementation is verified.
5. **CGH Applied message-family gap:** A package §4 enumerates eight evidence families; H Applied ACK 1.1.0 schema has five JF-10 variants. Reservation, D fence terminal, C submit outcome, CausalOrderTerminalProof and a distinct COC ACK lack explicit schema variants/mapping. H must add versioned families or identify exact alternate schemas.
6. **Storage proof family is separate:** H's new two-message Storage proof schema does not automatically extend Applied ACK 1.1.0. The exact inline-vs-reference/digest mapping must be pinned to the same CausalOrderTransactionRef, ParticipantIntentRef, participant tuple, request digest and owner boundary.
7. **A package/ledger stale pins:** current A package file is Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` and current owner matrix is Blob `ee35d3b39cb1fddd1feee0e0504b77e73e376893`. A final acceptance and tracking ledger still refer to package Blob `9808b31f840606b329f1a794935dfc9c5084d63b` and older pending-decision state. A must reconcile its own artifacts; B/I/H do not rewrite them.

## 5. Cross-workstream request/evidence checklist

| Responsible Owner | Exact action required | Evidence required to advance |
|---|---|---|
| A | Re-read all current branch heads and source Blobs; reconcile G6 and CGH package pins in A's own plan/tracking/final acceptance. | Updated A-owned G0–G10 ledger with package `4961ff...`, matrix `ee35...`, I register `2fdd...`, current B/I/H heads and explicit gate decisions. |
| Storage | Amend §14 to match v3 or supersede it; add I terminal proof attempt/ledger fields; remove unsupported ABORT_WON; issue one exact normative revision. | New Storage Blob SHA, exact field mapping, updated tests/fixtures, owner review request. |
| I | Approve actual signature/key policy and independent anchor; obtain I36-GOV-01..10, Environment Registry Authority, InventorySeal and AuthorizationCommitPermit decisions. | Effective policy hashes, named authorized approvers, trust-root/key-status history, monotonic anchor evidence, I36 execution logs. |
| H | Map all eight CGH families, or explicitly map missing families to other exact schemas; link Storage proof schema; complete canonical bytes/signature profile after I approval. | Versioned IDL/schema, generated fixtures/SDK, semantic validator, signature/replay/canonicalization tests, exact C/G/H readbacks. |
| C/D/E/F/G/Storage | Implement consumer boundaries and run owner-specific suites in the engineering phase. | Immutable build/source SHA, environment/fixtures, command, raw output, expected/actual results, durable readback and owner sign-off. |
| A/C/G/H/D/I/B | Keep one exact CGH-APPLIED-1.1 package and same-version owner/predicate decisions; do not infer freeze from design acceptance matrix. | Exact package/schema digests, explicit same-version decisions, no missing message families, A freeze record. |

## 6. Change log and limits

- This is the first scheduled evidence-ledger run; there is no prior automation ledger to compare against.
- B added the v3 nominal type mapping and the §14 mismatch finding.
- I added exact v3 owner-gate/terminal-proof/security requirements and reconciled current C/D/E/F/G/Storage BIH consumer acceptance evidence. The design-acceptance subrequirement is recorded complete in I's register; A's G6 state remains unchanged pending A readback.
- H added a separate Storage proof schema, wired structural tests into CI, corrected an initial schema composition defect, and obtained 47/47 structural test PASS. H also recorded the unresolved CGH message-family gap.
- No Owner branches were merged. No main-branch change was made. No external governance approval, production deployment, runtime implementation, I36/H36 execution, CFG execution, Runtime Forget E2E closure, Global Forget completion or physical erasure is claimed.
