# NVIDIA Context Optimization — Final Owner Acceptance Matrix

- Owner: A — Principal Integration Architect
- Integration branch: `session-a-integration-2026-11-16`
- Status: evidence-backed decision register; not an approval proxy

## 1. Formal decision matrix

| Owner | Formal decision | Accepted contract / boundary | Conditions retained | P0 | P1 | Evidence file |
|---|---|---|---|---|---|---|
| B | ACCEPT WITH CONDITIONS | Typed domain identities; ArchiveLocator vs ContextObservationReference; Observation/Evidence/Derived Summary/Canonical Memory separation; epistemic and temporal provenance | Domain vocabulary, TSS semantics, exact wire mapping; references never grants | No executable authorized/current source path through Context commit and final request | Observation/Evidence vocabulary, source-time mapping, TSS and H/I mapping | `reviews/acceptance/session-a-domain-model-acceptance.md` |
| C | ACCEPT WITH CONDITIONS | F Returned, G Selected, Adapter Materialized, C final request submitted and G Applied are distinct evidence stages | Tier-1 final-request proof, provider idempotency/recovery, exact schema and authority binding | No integrated F→G→H→C→G Applied proof; Issue #3 remains open; stale cache/offline proof absent | Provider hooks, digest profile, telemetry correlation and reconnect tests | `reviews/acceptance/session-a-agent-integration-acceptance.md` |
| D | ACCEPT WITH CONDITIONS | D retains Canonical Memory, ForgetFence, canonical producer/dependency and suppression authority | Complete F producer and G derivative/backup/replica inventory; transitive Forget gates | Forget/restore proof and classification incomplete; negative tests not run | G lineage, tombstone-before-rebuild, stale Snapshot/Delta rejection | `reviews/acceptance/session-a-context-optimization-acceptance.md` |
| E | ACCEPT WITH CONDITIONS | E owns canonical-derived registration and publication gate; F catalog is not E canonical index; G compaction is not auto-published | D/E/Storage atomic registration + final gate; complete dependency set; receipt reconciliation | Atomic gate and production JF-10 recovery not proven | Producer identity, dependency digest, retry/publication schema | `reviews/acceptance/session-a-compiler-acceptance.md` |
| F | ACCEPT WITH CONDITIONS | F owns immutable Archive objects/revisions, locator, RecallSession/cursor/receipt, budgets, completeness, cache and F-local suppression | I retention/authorization; D fence/producer classification; F/G exact Recall contract; restore and cache proof | Forget × Capture/Recall/Cache and Archive Restore/PITR not proven | Recall schema, retention/expiry, catalog/index boundary, cache freshness | `reviews/acceptance/session-a-observation-archive-acceptance.md` |
| G | ACCEPT WITH CONDITIONS | G owns ContextObservationReference, selection, ContextVersion, TSS projection, compaction, fidelity, lineage/loss and delivery intent | B/C/D/F/I/H semantics; transitive Forget; current-use vs historical Applied | Forget × compaction/CAS/delivery and Restore/PITR proof absent | TSS fields, fidelity vetoes, loss retention, telemetry and held-out evaluation | `reviews/acceptance/session-a-context-optimization-acceptance.md` |
| H | ACCEPT WITH CONDITIONS | H owns BMCP Recall/Delivery/ACK/Applied transport families, typed cursor, errors, idempotency and reconnect semantics | Versioned wire schema, capability negotiation, authentication, D/I currentness and replay tests | Wire/reconnect conformance not frozen or run; Issue #3 open | Schema IDs, error registry, retryability, dedupe horizon, unknown-field behavior | `reviews/acceptance/session-a-bmcp-protocol-acceptance.md` |
| I | ACCEPT WITH CONDITIONS | I owns Principal/Actor/Scope authorization, PermissionEpoch, revocation, retention, inventory and global Forget governance | Governance approvals, authoritative registry/seal, target coverage, JF-10 owner-gate integration and restore evidence | Inventory/global completion governance blocked; JF-10 recovery and restore proof open | Producer/recipient lifecycle, exceptions, external recipients, backup/erasure | `reviews/acceptance/session-a-security-governance-acceptance.md` |

No Owner has recorded unconditional ACCEPT for this NVIDIA package. No PENDING or REJECT is hidden: all eight requested Owners have formal reports, and every one is conditional.

## 2. Exact report evidence manifest

The report-introducing commit SHA is the commit that added the formal report. The observed branch HEAD is the live Owner branch ref queried during this integration. Blob SHA identifies the exact report contents.

| Owner | Branch | Report path | Blob SHA | Report commit SHA | Observed branch HEAD |
|---|---|---|---|---|---|
| B | `session-b-domain-model-phase3` | `reviews/acceptance/session-a-domain-model-acceptance.md` | `253f37247e0b7c2a07844c80cea287cc62465a23` | `a69ffe15b8c5f2a0de3d7c847c235cde1cdbf837` | `a5bf20b57ebb3db849f91c555b658f9a2ee09851` |
| C | `session-c-agent-integration-2026-11-16` | `reviews/acceptance/session-a-agent-integration-acceptance.md` | `f3bcfe38f8a35d54de8789c82f6f4e13e2ae827c` | `3774ace4b7d3e55a5a188e9a30e60631e1a9317e` | `d13aa06ba42820a27bba18ecb6eae13dc9071599` |
| D | `session-d-memory-brain-2026-11-16` | `reviews/acceptance/session-a-context-optimization-acceptance.md` | `91ebbc0b9cfb96fd92837ff67909d09282df7e33` | `75629584e4b692c83121bebd09e9cb0ea7607226` | `06bce7f13bfe003d6d70b8d57c9522f5e46e2ed9` |
| E | `session-e-memory-compiler-2026-11-16` | `reviews/acceptance/session-a-compiler-acceptance.md` | `c6597bcb03ad24fa8128e8d335e8101671688822` | `bf572b7a057dc3179e66308f7a7d11fed3da1147` | `0d77d0ad6e564873127c53d7dd02edca09e822e1` |
| F | `session-f-memory-runtime` | `reviews/acceptance/session-a-observation-archive-acceptance.md` | `9fc183cc1b6b9989cb9c52c806c91e888afc474d` | `5a9816ce5732a3f437e24bbd9a82630a5f4f2c6f` | `5a9816ce5732a3f437e24bbd9a82630a5f4f2c6f` |
| G | `session-g-memory-context` | `reviews/acceptance/session-a-context-optimization-acceptance.md` | `3ab43d091764d953c52ae28d2570708359c5571c` | `4851b46b9de78ecae73186dc104b8be33bb4b519` | `e8547303bc464dbfd42d8d402b538e2b32033934` |
| H | `session-h-bmcp-protocol` | `reviews/acceptance/session-a-bmcp-protocol-acceptance.md` | `101ff9ffc0755667183ab80b64cd5c6dee1799da` | `a998c4e63f7404f8e5bf80f548a8339c41d0d05a` | `9c33237ecc4801a63d62d1c56184f3d48c53f65f` |
| I | `session-i-security-governance-2026-11-16` | `reviews/acceptance/session-a-security-governance-acceptance.md` | `89e964a12373350cb831881b262a3a69aaa1cb91` | `001204ba7ed73242ac18c59f5de83c3470d2dfe6` | `4b1ef1c607089db1c886ae9af82e8cab5d9c6af3` |

## 3. Exact review pin

All eight reports identify A package commit `6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f` and list the same four A source Blob SHAs. Those source files were independently re-read on the live A branch and remain byte-identical. This does not approve a later revision automatically.

## 4. Separate design-level acceptance matrices

The following exact matrices exist and must not be conflated with the eight NVIDIA package decisions:

- `reviews/integration/phase-3.6-cgh-applied-1.1-owner-acceptance-matrix.md`, Blob `ee35d3b39cb1fddd1feee0e0504b77e73e376893`: CGH-APPLIED-1.1 / JF-10 bridge design-level owner acceptance complete with enumerated exceptions; not frozen.
- `reviews/integration/phase-3.6.3-coc-durable-protocol-acceptance-matrix.md`, Blob `9a39e48a394fedbab16d15589056d59ef33f390f`: Gate B COC durable protocol design-level owner review complete with enumerated exceptions; not implemented.

These matrices improve design-level reviewability but do not close runtime, global governance, restore or implementation gates.

## 5. Scope limitations

A did not edit any B–I or Storage branch and did not alter any Owner formal acceptance report. Report existence proves a decision was recorded, not that a test passed.
