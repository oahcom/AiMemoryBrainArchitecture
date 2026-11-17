# Phase 3.6.11 — Storage Bidirectional COC ParticipantManifest ↔ I/D/C Owner Admission Join Proof

- Owner perspective: Storage / COC durable participant accounting
- Status: **PROPOSED STORAGE CONTRACT — H/I/D/C/A exact-version review REQUIRED**
- Scope: Recovery Cutoff Batch, ParticipantManifest, I/D/C owner request/admission snapshots, RecoveryJoin and owner-only Gate Release
- Normative source pair: Storage Design v3.1 + COC protocol 8ac178; H recovery schema 1.0.4 and H semantic validator contract 3.6.10
- Architecture contract only; not implementation or conformance evidence.

## 0. Exact source pins

| Source | Branch | Blob |
|---|---|---|
| Storage Design v3.1 | session-storage-consistency-forget-atomicity-2026-11-16 | d5bdc72f193fcdaa654e4f07f865b77c578673ca |
| COC protocol / prepared participant companion | session-storage-consistency-forget-atomicity-2026-11-16 | 8ac17816476f280ab6fb3afca0688aa03e37de1d |
| H semantic validator contract 3.6.10 | session-h-bmcp-protocol | 7e6f67518e476fe9798f23a87798c7a3eb352f3c |
| H recovery schema 1.0.4 | session-h-bmcp-protocol | d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1 |
| I global inventory amendment 3.6.8 | session-i-security-governance-2026-11-16 | 929b30ba10ac627927d3959e0777b467846b268d |
| D cross-boundary amendment 3.6.8 | session-d-memory-brain-2026-11-16 | 0668667daeb936bf223ab049277ea2a4117c3b09 |
| C owner-local gate amendment 3.6.9 | session-c-agent-integration-2026-11-16 | 9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb |

If any source advances, these pins do not silently advance. Re-review the exact new pair.

## 1. Problem statement and non-equivalence

COC ParticipantManifest and I/D/C owner-local admission ledgers are different authoritative enumerations:

- COC enumerates every ParticipantIntent committed through exact quorum prefix P in the selected CausalOrderDomainRef.
- I enumerates I-local receipt issue/consume and inventory obligations.
- D enumerates D-local producer/work/attempt/barrier admissions and lineage obligations.
- C enumerates C-local reservation/provider-attempt admissions and actual side-effect outcomes.

No one set substitutes for another. COC cannot infer owner admission completeness from its own log. An owner cannot infer COC registration from its local row. A count match, shared operation ID, timestamp, copied digest, or one-way foreign key is not a Join Proof.

The Join Proof is a typed, bidirectional relation between two independently complete sides. It does not merge owner sequence spaces, compare owner high-waters to COC term/index, or grant any owner authority.

## 2. Normative record chain and digest order

Preserve the existing acyclic Storage v3.1 digest chain:

1. ParticipantManifestContentDigest: computed before batch commit over domain-separated canonical manifest content: stable ManifestId, RecoveryEpoch/round, exact prefix P (term,index,root,configuration_epoch), previous-prefix digest, enumeration status, ordered participant entries, count and participant-set root. It excludes future batch ref/digest, quorum proof, final signature envelope and transport metadata.
2. RecoveryBatchDigest: computed over the canonical RecoveryCutoffBatch payload, including stable BatchId, RecoveryEpoch/round, exact P, I/D/C owner snapshot refs and digests, scope binding, reconciliation attempt generation, previous-batch digest, ManifestId and ParticipantManifestContentDigest.
3. ParticipantManifestRecordDigest: computed after the batch is quorum committed. It binds exact RecoveryBatchRef + RecoveryBatchDigest, ParticipantManifestContentDigest, prefix/entries and protected record envelope.
4. RecoveryJoinProofDigest: computed only after the batch and final manifest record are committed and linearly read back. It binds both prior record digests, all three owner snapshot digests, both directional join-edge sets, all owner completeness/high-water/root attestations, and the JF-10 sub-join root where applicable.
5. Owner Gate Release and RECOVERY_EPOCH_COMPLETED bind the exact RecoveryJoinProofRef + RecoveryJoinProofDigest.

Dependency order:

ParticipantManifestContentDigest → RecoveryBatchDigest → ParticipantManifestRecordDigest → RecoveryJoinProofDigest → OwnerGateRelease / RecoveryEpochCompleted.

No digest includes a future record that itself includes the earlier digest. No in-place mutation is allowed; any changed membership, scope, prefix, owner high-water, admission state or participant binding requires a new RecoveryEpoch round and new immutable identities.

## 3. Join Proof logical object

RecoveryJoinProof is a Storage-persisted, COC-committed evidence record. H owns its wire schema.

### 3.1 Header and authority bindings

- RecoveryJoinProofRef, RecoveryEpochRef, RecoveryRound, ReconciliationAttemptGeneration;
- exact CausalOrderDomainRef and scope binding / scope generation;
- RecoveryCutoffBatchRef, RecoveryBatchDigest;
- ParticipantManifestRef, ParticipantManifestContentDigest, ParticipantManifestRecordDigest;
- exact COC prefix P: term, index, root, configuration epoch and previous-prefix digest;
- exact I/D/C OwnerSnapshotRefs, OwnerSnapshotDigests and owner authority refs;
- I/D/C request-set count/root/high-water and admission-set count/root/high-water;
- each owner's GateRef, GateGeneration, ScopeGeneration and independent anti-rollback anchor;
- explicit per-side enumeration states COMPLETE_EMPTY or COMPLETE_NON_EMPTY; never infer empty from null, missing, unavailable, partial or zero count alone;
- JoinProof schema/profile, canonicalization profile reference, digest algorithm/profile, issuer, audience, key ID/version and signature reference. Cryptographic policy remains I-owned and H-encoded.

### 3.2 OwnerAdmissionToParticipant edges

One edge for every owner admission entry whose coc_registration_state=REGISTERED:

- owner kind I/D/C;
- exact OwnerAdmissionRef and OwnerAdmissionEntryDigest;
- owner-local sequence namespace/value, GateGeneration and ScopeGeneration;
- stable OperationIdentityRef, OperationDigest and ScopeRef;
- ParticipantIntentRef;
- exact COC (term,index) and ParticipantEntryDigest;
- exact ParticipantManifestRef and ParticipantManifestRecordDigest;
- cardinality rule identifier.

For NOT_REGISTERED, emit a separate OwnerAdmissionNoParticipantDisposition:
- exact owner admission ref/digest and owner-local sequence;
- NOT_REGISTERED state and reason;
- terminal state NO_EFFECT_PROVEN with owner-signed proof, OR PENDING / UNKNOWN which remains a release blocker;
- MUST contain no ParticipantIntentRef, COC position or participant entry digest;
- proof that no protected effect/provider invocation/publication crossed the boundary, or explicit pending obligation that must be registered in a later round before any protected effect.

### 3.3 ParticipantToOwnerEvidence edges

One edge for every ParticipantIntent in the manifest:

- exact ParticipantIntentRef, participant digest, COC position and entry digest;
- exact primary owner binding from the manifest entry's owner_admission_ref;
- exact applicable I receipt issue/consume evidence refs and I terminal-decision refs;
- exact applicable D work/barrier/lineage membership refs and D terminal/clearance refs;
- exact applicable C reservation/provider-attempt refs and immutable CSubmitOutcome refs;
- exact Storage PreparedParticipantRef, GID, DB incarnation and StorageResolutionProofRef for JF-10 participants;
- explicit required-owner set and per-owner evidence disposition PRESENT, NOT_APPLICABLE_WITH_PROOF, PENDING, UNKNOWN.

A participant with a missing required owner edge is not complete. NOT_APPLICABLE requires an authority-signed, scope-bound proof; absence is not non-applicability.

## 4. Bidirectional join rules

### 4.1 Direction A — Owner Admission → COC ParticipantManifest

For every I/D/C admission snapshot entry:

1. Verify the exact owner signature, authority, audience, schema and current key status under I policy.
2. Verify the entry belongs to the exact snapshot, request/admission ledger root, high-water, GateGeneration and ScopeGeneration.
3. If REGISTERED, resolve exactly one ParticipantManifest entry by ParticipantIntentRef; verify exact COC position, ParticipantEntryDigest, OperationIdentityRef, OperationDigest and ScopeRef. No best-effort lookup.
4. A C admission is the primary owner admission anchor represented by participantEntry.owner_admission_ref; it MUST match exactly.
5. I and D may contribute multiple distinct evidence entries to one participant (e.g. I receipt issue and consume, D barrier/work evidence) only through explicit typed edge cardinality. One owner admission entry MUST NOT map to multiple participants.
6. If NOT_REGISTERED, all participant identity/position/digest fields MUST be absent. The entry remains an owner-local obligation. Only owner-signed NO_EFFECT_PROVEN may close it without COC registration; otherwise the owner gate remains closed.
7. A registered admission with no participant in the exact manifest is JOIN_MISSING_PARTICIPANT and blocks release. It cannot be excused by later prefix, timestamp, stale replica or a similarly named participant.

### 4.2 Direction B — COC ParticipantManifest → Owner Admission

For every ParticipantManifest entry:

1. Verify the exact committed COC record exists at its declared position within P and its entry digest matches the committed bytes.
2. Resolve its primary owner_admission_ref to exactly one matching C admission entry in the exact C snapshot.
3. Resolve every required I/D/C owner evidence edge to exact owner-local admission/receipt/barrier/provider evidence in the corresponding snapshot or independently signed evidence registry.
4. Verify operation identity/digest, Scope, owner boundary and participant digest are identical across all joined records.
5. Verify each required participant obligation is reconciled: I terminal/receipt state, D barrier/lineage state, C provider outcome and Storage prepared participant/outcome as applicable.
6. A participant without accountable owner evidence is JOIN_ORPHAN_PARTICIPANT; it blocks gate release even if the COC manifest is internally valid.
7. Duplicate participant identities, duplicate COC positions, owner-ref substitution, same ref with changed digest, cross-epoch or cross-scope joins are JOIN_CONFLICT and quarantine.

### 4.3 Cardinality and identity constraints

- ParticipantIntentRef is unique within the COC prefix/domain and maps to one immutable participant tuple.
- OwnerAdmissionRef is unique within its owner authority and admission ledger; it maps to at most one ParticipantIntentRef.
- Multiple owner evidence refs may map to one participant only where the owner contract explicitly permits it; issue/consume evidence is not collapsed into one event.
- COC owner_kind is the participant's primary owner classification, not a substitute for the I/D/C owner identity. I/D evidence joins are explicit typed edges.
- owner_admission_ref in the current 1.0.4 participant entry is the mandatory primary C admission anchor. It does not encode all I/D evidence edges; the JoinProof must carry those separately.
- No join may be made solely by OperationId, digest equality, sequence number, wall-clock timestamp, array index or matching GID.
- No comparison of I PermissionEpoch, D FenceGeneration, C GateGeneration, owner-local sequences, COC term/index or Storage LSN across namespaces.

## 5. Completeness algorithm

The validator performs these steps in order:

1. Read the quorum-confirmed COC prefix P linearly; verify term/index/root/configuration epoch and digest-chain continuity.
2. Enumerate all ParticipantIntent records in the selected causal domain through P with complete cursor/page continuity. Build authoritative COC set M_P.
3. Read I/D/C owner snapshots linearly from their own authorities; verify independent completeness, explicit empty/non-empty state, signed high-waters, request/admission roots, gate/scope generations and anti-rollback anchors. Build A_I, A_D, A_C separately.
4. Validate the committed batch and manifest digest chain. Require the manifest participant set to equal M_P exactly (not merely equal count).
5. For each owner admission in REGISTERED, resolve one exact participant edge. For each NOT_REGISTERED, verify absence of participant fields and no-effect proof or retain PENDING.
6. For each participant in M_P, resolve its primary C admission and every required I/D/C/Storage evidence edge.
7. Compute both directional difference sets and require them to be empty for all required registered relationships:
   - OwnerRegisteredWithoutParticipant = ∅
   - ParticipantWithoutPrimaryOwnerAdmission = ∅
   - ParticipantWithoutRequiredOwnerEvidence = ∅
   - DuplicateOrConflictingJoinEdges = ∅
   - UnprovedNotRegisteredEffects = ∅
8. Revalidate current owner high-waters, scope generations, GateGenerations, I inventory epoch/currentness, D projection/lineage generation and C provider-attempt generation immediately before JoinProof commit and again before each owner release CAS.
9. Persist immutable JoinProof, quorum commit it, linearly read it back, then allow I/D/C to independently evaluate their own release predicates.

A complete empty join is valid only if COC prefix enumeration is complete and explicitly empty; I/D/C request and admission sets are each explicitly complete-empty or have fully accounted no-effect dispositions; each empty root is recomputed from the H-approved canonical profile; all owner signatures and anti-rollback anchors verify; and no owner gate/high-water/scope generation advanced during final currentness check. count=0 alone is never empty proof.

## 6. Gate release and completion coupling

- Storage/COC may persist and report JoinProof; it MUST NOT sign or issue I/D/C OwnerGateRelease.
- I release requires I's own current request/admission roots, receipt issue/consume high-waters, ProducerDomainInventoryEpoch, GateGeneration and I anti-rollback anchor to match the JoinProof.
- D release requires D's own producer/work/attempt/barrier high-waters, per-Fence affected-lineage membership and terminalization proof to match.
- C release requires C's own reservation/provider-attempt high-waters, provider side-effect ledger and same-key outcome reconciliation to match.
- Every release binds exact RecoveryBatchDigest, ParticipantManifestRecordDigest and RecoveryJoinProofDigest.
- A release only reopens that owner's outage-admission gate. It does not make Forget effective, grant I authorization, establish Storage visibility, prove provider success or complete Global Forget.
- RECOVERY_EPOCH_COMPLETED is appended only after all three valid owner releases and all participant reconciliations. It is a COC observation, not an owner release.

## 7. Failure semantics

| Condition | Join result | Required action |
|---|---|---|
| Missing owner snapshot or owner authority unavailable | UNKNOWN | Keep all affected gates closed |
| Owner says COMPLETE_EMPTY but ledger/pagination unavailable | INVALID or UNKNOWN | Never treat as empty |
| Registered owner admission absent from manifest | INVALID | JOIN_MISSING_PARTICIPANT; new round/reconcile |
| Manifest participant has no primary C admission | UNKNOWN / INVALID | JOIN_ORPHAN_PARTICIPANT; quarantine |
| I/D evidence edge missing | UNKNOWN | Retain owner gate and participant |
| NOT_REGISTERED carries participant ref/position/digest | INVALID | JOIN_FORGED_PARTICIPANT |
| NOT_REGISTERED with unresolved possible side effect | UNKNOWN | Keep gate closed |
| Same owner admission ref maps to two participants | CONFLICT | Quarantine and integrity incident |
| Same participant ref has different digest/tuple | CONFLICT | Quarantine and integrity incident |
| Batch/manifest/join digest mismatch | INVALID | RESTORE_FENCED |
| Owner high-water/scope/gate generation advances | STALE | New immutable round; no stale release |
| COC quorum/prefix unavailable | UNKNOWN | No new JoinProof or release |
| JF-10 I/Storage terminal mismatch | INVALID | Keep same participant quarantined |
| I COMMIT_WON + same Storage participant COMMITTED | VALID for I/Storage pair only | C provider and D predicates still independently required |
| I REVOCATION_WON / INDETERMINATE_ABORTED + same Storage participant ROLLED_BACK | VALID for pair only | No provider side effect |
| Any I/Storage UNKNOWN or IN_DOUBT | UNKNOWN | Preserve same participant/GID/locks |

## 8. Join Proof test vectors

- JPF-01: every REGISTERED C admission maps to one exact manifest participant; reverse C primary-owner link resolves.
- JPF-02: registered I receipt issue and consume entries both join the same participant through distinct typed edges.
- JPF-03: registered D work/attempt/barrier entries join exact participant and exact fence/lineage scope.
- JPF-04: C admission maps to no participant but is marked REGISTERED — reject.
- JPF-05: participant exists in manifest but primary C admission is absent — UNKNOWN / quarantine.
- JPF-06: NOT_REGISTERED carries ParticipantIntentRef, position or entry digest — reject.
- JPF-07: NOT_REGISTERED has unresolved possible provider/publication effect — UNKNOWN / keep gate closed.
- JPF-08: same OwnerAdmissionRef maps to two ParticipantIntentRefs — CONFLICT.
- JPF-09: same ParticipantIntentRef joins with changed participant digest/operation/scope — CONFLICT.
- JPF-10: owner high-water/scope/gate generation advances between JoinProof creation and release CAS — STALE.
- JPF-11: COC manifest is complete but one I/D required evidence edge is missing — UNKNOWN.
- JPF-12: I COMMIT_WON + same participant/GID/DB incarnation Storage COMMITTED; negative controls include different GID/DB incarnation, ROLLED_BACK or UNKNOWN — only exact COMMITTED pair validates.

## 9. JF-10 sub-join

For every Storage prepared participant in the COC manifest, JoinProof carries a typed JF-10 edge binding:
- ParticipantIntentRef and CausalOrderTransactionRef;
- PublicationOperationId / RequestDigest / ParticipantTupleDigest;
- PreparedParticipantRef / PreparedTransactionGID;
- CanonicalAuthorityDBRef / DatabaseIncarnationRef / PostgreSQL cluster system identifier / database OID;
- PostgreSQL native XID as observed evidence only (never the preallocated identity);
- PrepareAttemptRef / PrepareAttemptGeneration;
- ParticipantLedgerRef / ParticipantLedgerVersion;
- COC prepare-intent position/digest;
- exact I CommitAuthorizationReceiptRef and single-use consumption/terminal evidence;
- exact Storage PreparedParticipantReceipt and StorageResolutionProof.

I COMMIT_WON must resolve the same PreparedParticipantRef + GID + DatabaseIncarnationRef to Storage COMMITTED. I REVOCATION_WON or accepted INDETERMINATE_ABORTED must resolve that same tuple to ROLLED_BACK. I/Storage UNKNOWN keeps the exact same participant unresolved. No alternate GID/XID, timeout, COC observation or absence from pg_prepared_xacts can terminalize it.

## 10. Open decisions and ownership

- H: exact wire field mapping for JoinProof, edge cardinality, schema version, canonical bytes, duplicate-key and unknown-critical behavior.
- I: signature/trust policy, historical key status, currentness CAS, inventory epoch and I release predicates.
- D: D lineage/barrier edge schema and D release predicates.
- C: C provider/reservation edge schema and authoritative same-key outcome.
- Storage: durable JoinProof record, quorum append/readback, immutable digest chain and exact participant evidence.
- A: cross-owner reconciliation and final acceptance.
- Engineering: executable storage/COC adapters, deterministic fault injection, failover/restore and read-path evidence.

The HRC suite is not a substitute for cryptographic verification, physical DB/COC tests, provider adapter tests or owner-local transaction proofs. This artifact does not freeze H schema 1.0.4 or the JoinProof wire format.

## 11. 中文规范

### 11.1 双向 Join 的含义
COC ParticipantManifest 枚举指定 CausalOrderDomain 中、精确 Quorum Prefix P 之前所有 ParticipantIntent；I/D/C Owner Admission Ledger 分别枚举各自本地准入、Receipt、Barrier、Reservation 和 Provider Attempt。两者是独立权威集合。COC 不能推断 Owner Ledger 完整，Owner 也不能推断 COC 已登记。计数相等、OperationId 相同、时间戳相近或单向 Foreign Key 都不是 Join Proof。

### 11.2 无环摘要顺序
必须保留 Storage v3.1 的无环顺序：先算 ParticipantManifestContentDigest；RecoveryBatchDigest 绑定 ManifestId/ContentDigest；Batch 提交后再算 ParticipantManifestRecordDigest 并绑定 BatchRef/BatchDigest；Batch 和 Manifest 均线性回读后再计算 RecoveryJoinProofDigest；Owner Release 和 RecoveryEpochCompleted 最后绑定 JoinProofDigest。禁止循环摘要或原地改写。

### 11.3 双向关联
方向 A：每条 REGISTERED Owner Admission 必须解析到唯一 ParticipantIntentRef，并核对 COC Position、ParticipantEntryDigest、Operation Identity/Digest 和 Scope。C Admission 是当前 1.0.4 owner_admission_ref 的 Primary Anchor；I/D 的 Receipt、Work、Attempt、Barrier 证据通过独立 Typed Edge 加入。同一 OwnerAdmissionRef 不得映射多个 Participant。NOT_REGISTERED 不得带 ParticipantRef/Position/Digest，必须有 Owner 签署的 NO_EFFECT_PROVEN，或保持 PENDING 并阻断 Gate Release。

方向 B：每条 COC Participant 必须反向解析到 Primary C Admission，并解析所有适用 I Receipt/Terminal、D Work/Barrier/Lineage、C Reservation/Provider Outcome 和 Storage Prepared Participant/Resolution 证据。缺少 Owner Evidence 不能视为不适用；不适用必须有 Owner 签署的 Scope-bound Proof。

### 11.4 完整性
分别核验 COC Prefix Enumeration 与 I/D/C Owner Snapshot 的完整性，计算双向差集：OwnerRegisteredWithoutParticipant、ParticipantWithoutPrimaryOwnerAdmission、ParticipantWithoutRequiredOwnerEvidence、DuplicateOrConflictingJoinEdges、UnprovedNotRegisteredEffects。所有差集必须为空。不得比较跨域 High-water、Epoch、FenceGeneration、COC Position 或 LSN。

### 11.5 Gate Release
Storage/COC 只能存储/报告 JoinProof，不能签发 I/D/C Gate Release。I、D、C 必须分别在自己的权威事务域中重新检查当前 High-water、Scope、GateGeneration、Inventory/Lineage/Provider Attempt 和 Anti-rollback Anchor，并绑定相同 Batch/Manifest/JoinProof Digest。RecoveryEpochCompleted 只是 COC 观察记录，不是 Owner Release。

### 11.6 状态边界
缺项、未知、分页不完整、陈旧副本、签名不可验证、Owner 不可用均为 UNKNOWN 或 INVALID，绝不能折算为空集合。任何身份/摘要冲突都隔离。JF-10 只接受同一 Participant/GID/DB Incarnation 的 I/Storage 终态配对。未知时保留同一 Participant、GID、锁和 Gate。


## 12. H implementation artifact linkage and exact current pins

H has now committed the following candidate artifacts to its owner branch:

- H semantic validator contract 3.6.10 latest: Blob `142425b6280f7e0fe517489bc87bc81db892225a`
- H recovery-cutoff structural schema 1.0.4: Blob `d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1`
- H RecoveryJoin structural schema candidate 1.0.0: Blob `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`
- H executable HRC semantic suite: Blob `60a2f4db4bd12f2131ecd147db9bbe328da6db50`
- H wire interoperability candidate suite: Blob `18e50957848178f3f35593b3e618dfa9b90cdb31`

The semantic suite contains HRC-01..25 plus JPF-01..12. The wire suite contains WIRE-01..10. These are committed test candidates, not CI execution evidence. The test-only digest helper is not a production canonicalization profile.

### 12.1 Storage/H boundary clarification

Storage owns the logical bidirectional join invariants, durable JoinProof persistence, exact digest chain and quorum readback. H owns the wire schema, nominal type encoding, strict parser, canonical serialization and interoperability. I owns signature trust/key status; D/I/C own their admission ledgers and final currentness/release CAS. A owns integration reconciliation.

The H RecoveryJoin schema is a candidate. It does not make Storage the issuer of I/D/C gate releases and does not make a valid structural document proof of owner-ledger completeness. Storage may commit a JoinProof record only after both authoritative sides have been completely read and joined; each owner still independently evaluates its release predicate in its own serialization domain.

**Status:** JoinProof contract and H wire candidate are published. Independent Owner review, actual schema/semantic adapter, CI execution, DB/COC physical realization and failover/restore evidence remain OPEN.

## 13. Exact owner request and admission row mapping (H 1.0.4 → RecoveryJoin 1.0.0)

The join must not collapse three different owner-side concepts:

- OwnerAdmissionRef: stable admission identity carried by the signed OWNER_ADMISSION_ENTRY message and referenced by the COC participant's owner_admission_ref.
- OwnerEntryRef: exact ledger-row identity carried by an owner snapshot member's owner_entry_ref.
- OwnerAdmissionEntryDigest: digest of the exact owner snapshot admission member row.

The JoinProof edge carries OwnerAdmissionRef + OwnerEntryRef + OwnerAdmissionEntryDigest + owner-local sequence namespace/value. It must resolve both the signed admission identity and the exact row in the captured owner snapshot. A matching string in one namespace does not replace the other binding.

The RecoveryJoinProof also carries owner_request_dispositions for every request member in each I/D/C snapshot. This is necessary because a request can be pending, out-of-scope with proof, or later admitted; it is not equivalent to an admission and need not yet have a COC ParticipantIntent. Every request row is bound by OwnerRequestRef, OwnerEntryRef, OwnerRequestDigest, owner-local sequence namespace/value, Scope and owner signature. OUT_OF_SCOPE_WITH_PROOF requires an explicit proof reference. A missing request disposition blocks the JoinProof even if all admission and participant edges match.

The H schema keeps the COC ParticipantManifest's owner_admission_ref as the primary C admission anchor. I and D evidence are separate typed edges; the COC participant owner_kind is not overloaded to represent all three owner authorities.

Latest H pins:
- RecoveryJoin schema candidate: f531c1d4b89a48457188c4988f140952759223a6
- H semantic validator contract: 6f66a72a2d0aa43af338ff9e22d650d47aa2bd80
- HRC semantic suite: 794ac0c34aaad921e5d4a5bcc42b6601f7caf817
- Wire interop suite: 1a4e754ba9bfa57eb973c6d39731e9f89443b323
- Schema integrity suite: 67aba74c120f2916d768e7b01c45408ee2624f3a

The test inventory is 66 unittest methods: 25 HRC, 19 JPF, 10 wire and 12 schema-integrity. The 66-method Python candidate suite passed GitHub Actions run 44039990464. This is not production conformance or physical Storage/COC proof.


## 14. Typed owner-evidence refinements

The latest H RecoveryJoin schema makes the owner evidence edges typed rather than relying only on opaque references:
- D LINEAGE/BARRIER evidence binds ForgetOperationRef, FenceGeneration, LineageManifestRef/Digest and BarrierMemberRef.
- I receipt/terminal evidence binds PolicyDomainRef, PermissionEpoch, ProducerDomainInventoryEpoch, issuer key and authorization receipt.
- C provider evidence binds reservation, provider attempt and idempotency key.
- Storage prepared/resolution evidence binds PreparedParticipantRef, GID and DatabaseIncarnationRef.
- NOT_REGISTERED admission dispositions bind operation identity/digest, Scope, GateGeneration and ScopeGeneration, and NO_EFFECT_PROVEN requires its proof.
- Request dispositions bind both logical OwnerRequestDigest and exact OwnerEntryDigest.

These structural conditions reduce ambiguous joins but do not prove that referenced owner records are genuine/current. Runtime adapters must resolve and verify each signed evidence record in its owner authority. Latest H schema Blob: dd3234aa1c74caf6d0e335875cd96e0b2b64082f.


## 15. Owner admission identity separation tests

HRC/JPF now explicitly tests both sides of the OwnerAdmissionRef vs OwnerEntryRef distinction. OwnerAdmissionRef is the stable admission identity referenced by the COC participant's primary owner_admission_ref. OwnerEntryRef is the exact member row in the signed owner snapshot. The JoinProof binds both plus the snapshot row digest and owner-local sequence. JPF-18/JPF-19 reject substituting one for the other. Latest HRC/JPF suite Blob: 60a2f4db4bd12f2131ecd147db9bbe328da6db50.


## Verified H candidate CI result

GitHub Actions run 44039990464, job 133891944149, checked out H commit da94bcc1796cb350eed12845e49cbc3663faab9c and completed 66/66 candidate tests successfully (Ubuntu 26.04 / CPython 3.12.16). This is a PASS for the committed Python HRC/JPF/WIRE/SCHEMA candidate suite only. It does not prove production signatures, cross-language canonical bytes, live owner/COC adapters, physical JF-10 behavior or deployed Storage topology/HA/restore.


## 16. H exact executable suite refresh / H 精确可执行测试刷新

The current H branch exact bundle is:
- RecoveryJoin schema 1.0.0: `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`.
- H semantic validator contract: `6f66a72a2d0aa43af338ff9e22d650d47aa2bd80`.
- HRC/JPF semantic suite: `60a2f4db4bd12f2131ecd147db9bbe328da6db50` (25 HRC + 19 JPF).
- Wire suite: `1a4e754ba9bfa57eb973c6d39731e9f89443b323` (10).
- Schema integrity suite: `67aba74c120f2916d768e7b01c45408ee2624f3a` (12).
- Workflow: `.github/workflows/h-recovery-cutoff-conformance.yml`, Blob `ea7a3d9c365b84352d3bac69da94fe0d510e46a4`.

GitHub Actions run [44040502709](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44040502709), commit `1c6ddd301d538652ceea22ea665d50c5fad8178e`, completed **66/66 PASS**. The job executed HRC-01..25, JPF-01..19, WIRE-01..10 and SCHEMA-01..12. The test command and raw result are recorded in the H branch contract/evidence.

This is a repeatable candidate-suite CI pass only. It does not prove real COC prefix enumeration, live I/D/C owner-ledger snapshots, owner signature/key-status verification, Storage durable JoinProof commit, owner-local release CAS, production JF-10 same-GID resolution, cross-language canonical bytes or deployed topology. HRC-TEST-v1 remains test-only.

The H test fixture correction for JPF-08 isolates the duplicate primary C admission invariant; it does not weaken the semantic validator. H's latest 66-test run supersedes earlier 61/56-test inventory counts.

### 16.1 Storage interpretation

Storage recognizes H's current 66/66 result as evidence that the reference semantic vectors and schema-shape checks execute successfully. Storage does not promote this result to integrated Storage conformance. The ST-JOIN-01..20 physical/authority tests and topology T1–T8 remain required; mocks cannot substitute for live quorum, owner ledger or DB evidence.

### 16.2 中文结论

当前 H 分支包含 RecoveryJoin 1.0.0 Schema、HRC-01..25、JPF-01..19、WIRE-01..10 和 SCHEMA-01..12，共 66 个测试方法。GitHub Actions Run 44040502709 在 Commit 1c6ddd3 上完成 66/66 PASS。

该结果只证明 Python 参考语义/Schema/Wire 候选套件在 CI 上通过，不证明真实 COC Prefix、I/D/C Owner Ledger、签名与 Key Status、Storage JoinProof 持久化、Owner Currentness CAS、JF-10 物理同 GID 恢复或跨语言互操作。Storage 集成测试和物理拓扑仍 OPEN。


## 17. Latest H branch workflow rerun

After the H contract and freeze-evidence documentation updates, the H branch workflow ran again on its latest branch commit `b4d7ed2798fcd6514892ac91d8f3ae6c06f0a338`. GitHub Actions run [44041395001](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44041395001), job `133896572160`, completed successfully; raw log reports **66 tests ran, OK**.

The exact test sources remained unchanged: HRC/JPF `60a2f4db4bd12f2131ecd147db9bbe328da6db50`, Wire `1a4e754ba9bfa57eb973c6d39731e9f89443b323`, Schema Integrity `67aba74c120f2916d768e7b01c45408ee2624f3a`, RecoveryJoin schema `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`. This is a repeat CI pass of the same 66 candidate methods, not additional coverage and not production conformance.
