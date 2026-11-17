# Issue #20 — Executable State Machines, Race Matrix and Conformance Vectors

**Status:** Session P multi-role simulation / engineering proposal / NON-NORMATIVE  
**Exact Storage source under review:** commit `a65973093bb33c7c06ae503f421e096fadb5796b`; Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`.  
**Depends on:** D/I semantic drafts and cross-review; F/E/G/H/Storage/A integrated role simulations.  
**Authority warning:** This file is authored by Session P while simulating the roles. It is not an Owner signature, production implementation, CI result, or interface-freeze decision.

## 1. Normative vocabulary for this proposal

- **MUST / MUST NOT** are requirements proposed for Owner adoption, not currently binding project policy.
- **Linearization point** is the single durable commit/CAS at which a concurrent operation takes effect.
- **UNKNOWN** means the system cannot prove either terminal outcome; UNKNOWN is never treated as success.
- **Quarantine** means data may be retained for reconciliation but is not eligible for governed serving, export, or downstream execution.
- **Owner receipt** is signed evidence issued by the authority that owns the semantic decision. Storage persists and verifies it; Storage does not mint it.

## 2. D state machine — ProducerWork admission and Forget Fence

### 2.1 ProducerWork lifecycle

`DECLARED -> CLASSIFIED -> ADMISSION_PENDING -> ADMITTED -> EXECUTING -> STAGED -> DEPENDENCIES_CLOSED -> VISIBLE`

Terminal or blocked branches:
- `REJECTED`: no execution and no externally visible side effect.
- `QUARANTINED`: unresolved classification, stale I authorization, active Fence, incomplete lineage, or uncertain publication.
- `ABORTED`: durable proof that execution/publication was cancelled without visibility.
- `UNKNOWN`: commit/ack ambiguity; resolve by same ProducerWorkId + WorkGeneration + operation id, never by creating replacement identity.

Transitions:
1. `DECLARED -> CLASSIFIED`: D resolves per-work and per-output lineage as D_COVERED, ARCHIVE_ONLY, or MIXED_OR_UNKNOWN. Default is MIXED_OR_UNKNOWN.
2. `CLASSIFIED -> ADMISSION_PENDING`: authenticate ProducerInstanceRef and obtain current I authorization reference.
3. `ADMISSION_PENDING -> ADMITTED`: D admission transaction commits immutable receipt and increments D AdmissionSequence under the same serialization key used by Fence closure.
4. `ADMITTED -> EXECUTING`: execution can start only after durable admission receipt is queryable by stable operation ID.
5. `EXECUTING -> STAGED`: output is private and non-serving.
6. `STAGED -> DEPENDENCIES_CLOSED`: D verifies complete direct/transitive lineage and current FenceGeneration.
7. `DEPENDENCIES_CLOSED -> VISIBLE`: visibility CAS checks no scope Fence, same generation, current I authorization and dependency digest.
8. Any uncertain durable outcome enters UNKNOWN and is reconciled against the same operation identity.

### 2.2 Fence lifecycle

`OPEN -> CLOSING -> SEALED -> RECONCILING -> RELEASE_READY -> RELEASED`

- `OPEN -> CLOSING`: one D-owned transaction serializes with admission on the same scope key, increments FenceGeneration and captures the AdmissionSequence high-water.
- `CLOSING -> SEALED`: durable request set, admitted prefix, in-flight set count/digest and dependency inventory are sealed.
- `SEALED -> RECONCILING`: all pre-close admitted work is committed, rejected-with-no-side-effect, or explicitly unresolved and reconciled.
- `RECONCILING -> RELEASE_READY`: no unresolved descendant, publication, replay, late lineage or derivative remains.
- `RELEASE_READY -> RELEASED`: D-local CAS checks unchanged FenceGeneration, scope version, AdmissionSequence high-water and dependency-closure digest.
- Any late lineage or generation mismatch returns the operation to `CLOSING/RECONCILING` under a new generation; old completion receipt is invalidated.

### 2.3 D linearization rule

Admission and Fence closure MUST contend on the same durable serialization key `(PolicyDomainId, ForgetScopeId)`. The transaction commit is the linearization point. An admission committed before closure belongs to the captured prefix. A request ordered after closure is rejected/quarantined before execution. The design MUST NOT allow a producer to check OPEN, pause, and then commit admission after closure.

## 3. I state machine — Inventory and authorization seal

`SOURCES_DISCOVERED -> SOURCES_SNAPSHOTTED -> RECONCILED -> SEALED -> ACTIVE`

Invalidation:
`ACTIVE -> INVALIDATED -> RECONCILING -> SEALED`

1. `SOURCES_DISCOVERED`: enumerate authoritative control-plane, deployment, egress, backup, restore and external processor sources.
2. `SOURCES_SNAPSHOTTED`: record source identity, authority, snapshot boundary, watermark, extraction digest, freshness and known blind spots.
3. `RECONCILED`: reconcile identities, routes, recipients, backups and onward-copy edges; all pages/shards accounted for.
4. `SEALED`: sign canonical TargetInventorySeal including category counts, empty-category proofs, unknown/discrepancy sets, source digests and validity.
5. `ACTIVE`: seal is usable only while InventoryEpoch, SealGeneration and PermissionEpoch remain current.
6. Enrollment, de-enrollment, identity rollover, route/capability change, backup/restore topology change, revocation, source correction or policy change invalidates affected seal.
7. Seal re-creation requires a new source snapshot and reconciliation; old seal is not patched in place.

## 4. D/I join contract

The join key is nominally typed `ProducerInstanceRef`:
`(PolicyDomainId, ProducerDomainId, ProducerId, ProducerInstanceId, IdentityGeneration)`.

Join rules:
- Every I-inventoried producer capable of D-covered output maps to one D registration or an explicit D-approved exemption.
- Every D-registered producer maps to an I identity or an explicit I-governed exception.
- A generation mismatch is an orphan, not a fuzzy match.
- Join evidence binds I source digest + InventoryEpoch + SealGeneration and D registry digest + registry generation.
- Numeric comparison between I epoch and D AdmissionSequence/FenceGeneration is forbidden.
- A join does not transfer ownership: I owns inventory identity; D owns work closure.

## 5. F/E/G local state machines

### 5.1 F Archive/Recall
Capture: `REQUESTED -> CLASSIFIED -> CAPTURING_PRIVATE -> MANIFEST_SEALED -> AVAILABLE`; uncertainty/corruption -> `QUARANTINED`.
Recall: `SESSION_OPEN -> PAGE_AUTHORIZED -> PAGE_DELIVERED -> CURSOR_ISSUED`; each page/resume/export rechecks D FenceGeneration, I PermissionEpoch/SealGeneration and F index generation. Cursor is bound to principal, scope, object-set digest, policy, expiry and authority generations. Any mismatch invalidates it.
F release requires catalog/revision/index/cache/session/cursor reconciliation and an F-signed release receipt.

### 5.2 E Compiler
`QUEUED -> LEASED -> EXECUTING -> OUTPUT_STAGED -> PUBLICATION_PENDING -> PUBLISHED`; any ambiguity -> `UNKNOWN`, stale authority/fence -> `QUARANTINED`.
WorkItemId/WorkGeneration survive lease changes and retries; AttemptId changes per attempt; OutputId/PublicationId are stable for the logical output. Publication is private until D dependency closure and I authorization checks pass. Lost ACK queries the same PublicationId and OutputId.

### 5.3 G Context
`ASSEMBLING -> LINEAGE_CLOSED -> COMPACTING -> SNAPSHOT_STAGED -> SNAPSHOT_VALIDATED -> SERVABLE`.
Each fragment carries provenance. Effective lineage is the union of all D-covered ancestors. Missing ancestor means MIXED_OR_UNKNOWN and non-servable. Snapshot/Delta application requires exact base version, lineage digest and current D/I generations. Restore invalidates stale snapshots/deltas and requires G-local release.

## 6. Storage restore state machine

`RESTORE_REQUESTED -> DATA_RESTORED_PRIVATE -> CONTROL_REPLAYED -> D_RECONCILED -> I_RECONCILED -> FEG_RECONCILED -> JOIN_VERIFIED -> SERVING_CAS_COMMITTED -> SERVING`

Hard requirements:
- Restore older data snapshot without rolling back D Fence, I InventoryEpoch/PermissionEpoch/SealGeneration or owner release generations.
- Data restored from PITR is private/non-serving until all control logs and Owner receipts are replayed and checked.
- D/I/F/E/G release receipts are independent, signed and bound to RestoreGeneration.
- Final Serving CAS binds data snapshot ID/digest, control log positions, all Owner receipt digests, schema-set digest and RestoreGeneration.
- Any receipt stale, missing, revoked, malformed or mismatched -> CAS abort and remain non-serving.
- Lost ACK queries same RestoreOperationId and transaction identity. If outcome cannot be proven, remain UNKNOWN/non-serving.

## 7. H schema constraints

Candidate schemas are not finalized until semantic Owners decide exact fields. All wire objects MUST:
- carry explicit schema ID/version and canonicalization version;
- use nominal types for D AdmissionSequence, D FenceGeneration, I InventoryEpoch, I SealGeneration, I PermissionEpoch, F CursorId/IndexGeneration, E WorkItemId/PublicationId, G ContextVersion and Storage RestoreGeneration;
- define required/optional/null separately;
- bind issuer, audience, purpose, key ID, signature algorithm, issued-at, expiry and revocation context;
- reject duplicate keys, invalid canonical encoding, unknown critical fields, downgrade and cross-domain reference substitution;
- distinguish absent, empty and NotApplicable with explicit proof objects.

## 8. Conformance and race matrix

Each test must run against the selected persistence profile and actual adapter implementation before claiming conformance. Expected result below is a proposal.

| ID | Interleaving / fault | Required result |
|---|---|---|
| D-01 | Admission commits immediately before Fence closure | Included in sealed prefix; must reconcile |
| D-02 | Fence closure commits immediately before Admission | Admission rejected/quarantined; no execution |
| D-03 | Admission ACK lost after commit | Same admission ID query returns committed receipt; no duplicate sequence |
| D-04 | Crash before admission commit | No receipt and no execution; retry same identity |
| D-05 | Fence ACK lost after closure commit | Same ForgetOperationId returns same generation/seal |
| D-06 | Late descendant found after D release-ready | Old completion invalidated; quarantine and reopen under new generation |
| D-07 | DLQ replay after Fence closure | Same ProducerWork identity; no new admission bypass |
| D-08 | Visibility CAS races Fence generation advance | CAS fails; output remains private |
| I-01 | One inventory page omitted | Seal rejected |
| I-02 | Empty category without signed positive source proof | Seal rejected |
| I-03 | Unknown onward-copy recipient | Inventory incomplete; completion blocked |
| I-04 | Source stale/unreachable at seal boundary | Seal rejected or explicit authorized exception; never silently empty |
| I-05 | PermissionEpoch changes after seal | Seal invalidated; downstream authorization fails |
| I-06 | IdentityGeneration rollover | Old identity does not fuzzy-match new generation |
| DI-01 | I target has no D registration | Join fails unless explicit D-approved exemption |
| DI-02 | D registration has no I identity | Join fails unless explicit I-governed exception |
| F-01 | Recall cursor resumed after Fence generation changes | Cursor rejected; no page disclosure |
| F-02 | Cache hit after PermissionEpoch revocation | Cache result suppressed; reauthorization required |
| E-01 | Worker crashes after publication commit before ACK | Query same PublicationId; no second logical publication |
| E-02 | DLQ replay after Forget | Quarantine/reject; no fresh work identity |
| G-01 | Snapshot has one missing ancestor | Snapshot non-servable |
| G-02 | Old Delta replayed after restore | Reject due base/version/generation mismatch |
| S-01 | Restore old data snapshot with newer D/I control log | Replay controls; data remains private until reconciliation |
| S-02 | Serving CAS races I revocation | CAS fails or revocation is ordered after serving under explicit linearization; never stale silent release |
| S-03 | Lost Serving CAS ACK | Query same RestoreOperationId; UNKNOWN remains non-serving |
| H-01 | Duplicate JSON keys / unknown critical field | Strict parser rejects |
| H-02 | D sequence substituted into I epoch field | Type/schema validation rejects |

## 9. Evidence required before any status upgrade

1. Owner exact-version decisions on D/I/F/E/G/H branches, with commit and Blob SHA.
2. D/I reciprocal join vectors and signed sample receipts.
3. H schema source, generated artifacts, canonicalization/signature vectors and compatibility tests.
4. Storage selected DB/version/config and exact transaction/lock/recovery semantics.
5. Crash/failover/restore tests on real persistence and adapters, including same-operation lost-ACK recovery.
6. A exact-version manifest and formal integration decision.

## 10. Simulated disposition

- D/I: semantically coherent proposal; Owner decisions required.
- F/E: lifecycle direction acceptable with conditions; implementation and tests absent.
- G: lineage and stale snapshot/delta conditions must be adopted before acceptance.
- H: blocked on semantic Owner fields.
- Storage: blocked on persistence profile and conformance evidence.
- A: FREEZE NOT APPROVED.

Issue #20 remains OPEN. This file does not assert Owner adoption, test execution, CI pass, runtime conformance, physical deletion, Global Forget completion, restore safety, production readiness or merge.
