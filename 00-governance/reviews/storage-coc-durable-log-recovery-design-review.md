# Storage COC Durable Log & Recovery Protocol — Unified Review

- Review ID: P-COC-DURABLE-LOG-REVIEW-001
- Date: 2026-11-17
- Prepared by: Session P coordinator
- Status: **GATE B DESIGN AUTHORIZED; STORAGE PROPOSAL IS A STRONG CANDIDATE WITH REQUIRED AMENDMENTS; OWNER ACCEPTANCE PENDING**
- Scope: Independent integration review of Storage's detailed COC log/recovery design against A's current COC architecture, I/D/C/H decisions and the Applied 1.1 package. This is not a Storage/A/I/D/C/H Owner decision.

## 1. Source pins

| Artifact | Branch | Blob |
|---|---|---|
| Storage COC durable log and recovery protocol design | `session-storage-consistency-forget-atomicity-2026-11-16` | `cd5566b3d99b5204401ac713a5bb2dcf89a02726` |
| A COC deployment architecture, current file version | `session-a-integration-2026-11-16` | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| A CGH-APPLIED-1.1 package | same | `4961ffefc0f9920efb8425a9b2a7af42d8f64819` |
| A package's pinned companion COC blob | same path, older blob | `fc3bac39ec64fda68b8cba5e1aada4e719e5acea` |
| I JF-10 v2 + COC bridge disposition | `session-i-security-governance-2026-11-16` | `8069ff86988396442c8d9dc3fd58653683abe2f3` |
| H authenticated identity / Applied / JF-10 bridge mapping | `session-h-bmcp-protocol` | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` |
| C submit/causal-order contract | `session-c-agent-integration-2026-11-16` | `45a48249717c8cddb07ab96197730ef93d406c22` |
| D ForgetFence / publication gate | `session-d-memory-brain-2026-11-16` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` |
| Storage exact COC boundary acceptance for old pair | Storage branch | `9b297f0f76c9a054206cee5a6ee18200db3e1798` |
| Storage realization review accepting A COC architecture a3c51 | Storage branch | `107d21bd2c604ee0b04feff2ee5580e1de9c7fce` |

Storage branch HEAD at review: `1752a30d272d940a59735e0d96dc535c2319a3c8`.

## 2. What is sound in the proposal

The design correctly preserves the most important authority boundaries:
- COC is a cross-owner causal-order log and durable participant-accounting/observation service; it is not a second I policy-domain sequencer and does not decide Storage XID COMMIT/ABORT.
- I's policy-domain sequencer alone consumes the single-use CommitAuthorizationReceipt, orders authorization against revocation and durably decides the participant outcome.
- Storage alone resolves the exact prepared XID and atomically publishes VisibilityPointer, PublicationReceipt, owner outcome, receipt-consumption evidence and outbox.
- D alone owns ForgetFence, target/source/ancestor lineage, barrier and effective-fence semantics.
- H transports authenticated, versioned evidence without changing owner authority.
- ParticipantRegistry is a rebuildable projection, not an independent authority.
- COC and I positions remain distinct typed orders; no synthetic total order or numeric comparison.
- Append is idempotent by stable record identity + digest; same identity/different digest is a conflict.
- COC reads require a linearizable quorum-confirmed prefix; stale replicas/caches are not decision sources.
- COC outage closes durable I/D owner-local gates. Recovery first commits a cutoff batch, enumerates pre-batch participants, reconciles I/D outcomes and only then reopens gates.
- Unknown/in-doubt remains private/blocked; no timeout, lease expiry, missing ACK or heuristic resolution.
- Restore begins fenced and requires prefix/checkpoint continuity plus owner reconciliation before serving.
- Single-I-PolicyDomain scope is preserved; multi-policy-domain atomicity remains BLOCKED.

This is a strong architecture candidate and a reasonable next Gate B design artifact. It does not select a consensus product or concrete DB engine, and it does not claim implementation.

## 3. Blocking and required amendments

### COC-REV-001 — I terminal decision during COC outage must be worded precisely (P0)

Storage proposal §7 says, in effect, that “I COMMIT during COC outage” means Storage forward-commits the same XID.

The authoritative A/I bridge is more precise:
- If COC becomes unavailable after I has already durably decided COMMIT, Storage must still forward-commit that exact XID; COC later records the already-durable I decision and Storage proof idempotently.
- If COC is unavailable before the I owner-final-gate decision, I must not admit a new owner-final-gate decision until the required COC prefix and prepared-participant evidence are linearly readable. The I owner-local pending gate remains closed.
- No new receipt issuance/consumption or new I terminal decision is permitted merely because Storage has a prepared XID.

Required change: replace the ambiguous phrase with “a pre-existing I COMMIT_WON durably recorded before COC outage, whose Storage resolution/recovery occurs while COC is unavailable.” Explicitly state that a new I decision cannot be created during the COC outage. Align Storage §7 with A COC architecture §12.4 and I disposition §§10.4–10.6.

### COC-REV-002 — Record-family table omits RECOVERY_EPOCH_COMPLETED (P1)

The state machine and recovery algorithm require a durable, quorum-confirmed recovery-complete record before the system transitions back to SERVING. The minimum record-family table lists RECOVERY_CUTOFF_BATCH_COMMITTED and RECOVERY_RECONCILIATION_RECORDED but not RECOVERY_EPOCH_COMPLETED.

Required change: add a versioned record with:
- recovery epoch ID and prior/current COC prefix;
- final cutoff-batch IDs/digests;
- complete participant manifest count + digest/locator;
- I and D request-set digests and owner high-water positions;
- every required owner acknowledgement/reference;
- unresolved participant count = 0 (or explicit blocked state);
- exact service/member configuration epoch and durable quorum commit proof.

The transition to SERVING must require this record, not merely a local state flag.

### COC-REV-003 — Normative record names need exact H schema mapping (P1)

A/H's JF-10 bridge names include:
- `I_JF10_TERMINAL_DECISION_OBSERVED`
- `JF10_BRIDGE_RECONCILIATION_RECORDED`

Storage proposal uses `I_AUTHORIZATION_TERMINAL_RECORDED` and `RECOVERY_RECONCILIATION_RECORDED`. These may represent the same concepts, but no exact version mapping is stated.

Required change: publish one normative mapping table with source owner, COC record type, H message family/schema name, required fields, canonicalization, signer, idempotency key, and whether it is an owner decision or a COC observation. Do not create two competing names for the same event without a versioned alias rule.

### COC-REV-004 — Recovery participant manifest must be durably committed (P1)

The recovery algorithm says to persist the participant count and sorted ParticipantIntentRef set (or deterministic Merkle/set digest plus retrievable manifest) with an enumeration high-water. The record-family schema only clearly names a high-water field.

Required change: make the exact participant set reproducible and immutable: count, deterministic ordering rule, digest/Merkle root, manifest locator/content-address, enumeration prefix/high-water, and the rule for verifying no omission. Bind the manifest digest into RECOVERY_CUTOFF_BATCH_COMMITTED or a dedicated manifest-committed record.

### COC-REV-005 — Multiple cutoff batches within one recovery epoch (P1)

The proposal correctly says requests arriving after the recovery snapshot remain behind closed owner-local gates and require a subsequent batch. The state machine, however, reads as one cutoff batch → reconciliation → epoch complete → SERVING.

Required change: specify whether the service loops through repeated cutoff batches until I/D high-water marks are stable, or creates sequential recovery sub-epochs. Owner-local gates may reopen only after every request through the final committed owner high-water is represented and reconciled. New requests arriving during reconciliation must force another batch, not be silently carried into SERVING.

### COC-REV-006 — Domain registry authority and membership/configuration proof (P1)

The proposal correctly says CausalOrderDomainRef is resolved by a registry and never caller-selected, but does not clearly assign that registry's authority. It also needs a stable membership/configuration epoch in append/commit evidence, not only a coordinator term.

Required change:
- bind each CausalOrderDomainRef to exactly one I-owned PolicyDomainRef and registry version/digest;
- define who may create/change/revoke the mapping and how a stale mapping fails closed;
- bind every quorum commit to CoordinatorEpoch + MembershipConfigEpoch + log index + entry digest + quorum/durability proof;
- define key status/rotation/revocation handling for historical signed records.

### COC-REV-007 — COC source pin must be reconciled with Applied package companion (P0/P1)

A's current Applied package Blob `4961...` still pins companion COC Blob `fc3...`. The current A branch file at the same path `phase-3.6-causal-order-coordinator-deployment-architecture.md` is now Blob `a3c51...`, which contains the later I/JF-10 bridge §§12.1–12.8. C, D, H, I and Storage have separate exact-version acceptance evidence for `a3c51...`; G's exact Applied decision still pins `4961...` + `fc3...`.

Required change: A must publish one canonical version manifest that states whether `a3c51...` is a superseding companion or a separate additive architecture artifact. If it supersedes `fc3...`, issue a refreshed Applied package/companion pair and obtain exact re-acceptance from every affected Owner (at minimum G; others may reaffirm their already-pinned a3c51 decision). Do not treat the two blob pairs as interchangeable.

### COC-REV-008 — Checkpoint anti-rollback and recovery retention remain open (P1)

The proposal requires comparison to an independently retained checkpoint/high-water anchor but does not designate its authority, physical failure domain, immutable retention, rollback detection and restore policy.

Required change: define the external anchor owner, storage/failure domain, update quorum, retention, anti-rollback proof, key rotation, restore procedure and behavior if the anchor is missing/stale/unverifiable. Missing anchor must remain RESTORE_FENCED.

## 4. Additional design questions to settle before Gate B acceptance

1. **Record authority matrix:** for every RecordType, which owner/service may emit it, whose signature is required, and whether COC validates or only records it.
2. **Idempotency namespace:** stable operation ID, participant ID, recovery epoch, record type and digest conflict behavior across leader change and restore.
3. **Quorum semantics:** what constitutes durable quorum ACK, how leader term changes fence old leaders, and how membership changes avoid split brain.
4. **Retention/compaction:** no record or checkpoint needed for unresolved participant, revocation, Forget, inventory seal or audit may be compacted away; specify retention floor.
5. **Restore fencing:** require both COC prefix continuity and I/D authoritative high-water reconciliation before COC can return SERVING.
6. **Owner-local pending gate lifecycle:** exact durable state transitions, acknowledgement semantics, duplicate requests, cancellation and operator escalation.
7. **Multi-domain:** keep explicitly blocked; do not imply that CausalOrderDomainRef-per-domain yields global all-or-none atomicity.

## 5. Gate sequencing and project phase

Storage's current readiness record clarifies:
- The project is in architecture-design phase; no production runtime/adapter is expected yet.
- Set `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`; do not use absent production code as a Gate A architecture blocker.
- Gate A remains PARTIAL PASS / OPEN for remaining storage architecture specifications and cross-owner decisions.
- Gate B persistent COC/quorum log/participant registry/recovery-cutoff design is authorized to proceed now in parallel with Gate A closure.
- Gate B design acceptance remains pending until exact Owner decisions close the amendments above.
- Gate C implementation fault-injection is deferred until an implementation exists.
- JF-10 P0 remains OPEN; production activation NOT AUTHORIZED.

The readiness document still contains stale later lines saying Gate B/C remain BLOCKED after it authorizes Gate B design. Those lines must be reconciled to distinguish “Gate B design activity authorized” from “Gate B acceptance/implementation passed.”

## 6. Required next actions

1. Storage Owner: revise the COC design for COC-REV-001..008, publish exact new blob SHA and change log.
2. A Owner: reconcile the Applied package companion pin (fc3 vs a3c51), refresh source pins and gate vector.
3. I Owner: confirm the I outage/terminal semantics, domain registry authority, record signer matrix and external anti-rollback anchor.
4. D Owner: confirm repeated cutoff batch / complete lineage barrier and owner high-water requirements.
5. H Owner: publish exact record-to-message/schema mapping and requiredness/signature fields.
6. C Owner: confirm participant intent / provider outcome and idempotency/replay mapping.
7. G Owner: confirm the recovery batch and I/D terminal evidence requirements for Full Applied/current-use suppression.
8. A records exact Owner acceptance of the revised Storage design; no silence-as-acceptance.

## 7. Final verdict

**ACCEPT AS A STRONG GATE B DESIGN CANDIDATE WITH ENUMERATED BLOCKING AMENDMENTS.**

Gate B design activity is authorized; the Storage proposal is not yet accepted/frozen. No consensus product, DB product/version, quorum topology, operator or deployment is selected. No COC implementation or conformance pass is claimed. JF-10 P0 remains OPEN; multi-policy-domain atomicity BLOCKED; production activation NOT AUTHORIZED.
