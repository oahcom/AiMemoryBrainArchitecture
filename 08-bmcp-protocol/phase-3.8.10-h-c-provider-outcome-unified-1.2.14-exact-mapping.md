# Phase 3.8.10 — H Exact C Provider Outcome Mapping: Unified 1.2.14 × CSubmitOutcome 1.0.1
# Phase 3.8.10 — H 精确 C Provider Outcome 映射：Unified 1.2.14 × CSubmitOutcome 1.0.1

- Owner perspective: H — BMCP Protocol / Schema and Interoperability
- Status: **ACCEPT AS L1/L2 MAPPING CANDIDATE WITH ENUMERATED L3 / TRUST / STORAGE BLOCKERS; NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Exact H Unified schema 1.2.14 / wire 1.3.0: Blob 09fcd1fa29fe24255fbd87cae79dafb406594a59
- H RecoveryJoin schema 1.0.2: Blob 4b664e3bce465499bcdfd93796349a4ba7074002
- H RecoveryCutoff schema 1.0.5: Blob 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7
- Exact CSubmitOutcome schema 1.0.1: Blob a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda
- C Phase 3.11.1 sequence namespace amendment: Blob 6fa67af110ebbc5ef57ed908bb4880d99c5e46fb
- C key-status event schema 1.0.0: Blob 908b293eba337e9fa75864cea3704e28a1a8d82e
- C key-status lifecycle contract: Blob 9339b168165a7a3dd34def5236ad61cfd3163418
- I sequence namespace review: Blob 0d78e5b2bfcf66cae6b757314cead84b9c942601
- C profile identifier decision: Blob 5067dadb9c646a054d78f03c56e635facc36311a
- I C profile naming clarification: Blob 1e86a1349d371a1cdb4a56d69f783e0f316c7203
- H validator core: Blob 910e2a8f0b22adb4a192b3dbb7483e52a881e993
- H validator test source: Blob 9ceab387e114f9a28f9dfc12602e57f3ec5a3f43
- Exact H conformance run: 44067402639, tested commit 2068dd4f89245f9a4913ac069a169a2bed5471be, job 133984532592
- Provenance: delegated H-role review; **not an independent human H Owner signature**.

## 1. Exact version / 精确版本

The current candidate pair is:
- H Unified schema artifact revision 1.2.14, wire schema_version 1.3.0;
- CSubmitOutcome schema/version/artifact revision 1.0.1.

The exact H schema URI is https://schemas.aimemorybrainarchitecture.invalid/bmcp.coc-jf10-unified/1.2.14. The exact C object schema URI is urn:aimba:schema:c-submit-outcome:1.0.1. The H validator checks schema_id, loaded schema URI, artifact revision, wire version, C object schema identity/version/revision and message type. The deployment loader must additionally pin the exact immutable schema Blob/content hash; $id is not a content-integrity proof.

当前候选版本对为 H Unified 1.2.14 / Wire 1.3.0 与 CSubmitOutcome 1.0.1。H/C Schema URI、Artifact Revision、Wire Version、Object Identity/Version/Revision 和 Message Type 均需精确匹配。H Validator 检查 URI/ID；部署 Loader 还必须绑定不可变 Blob/内容哈希，$id 本身不是内容完整性证明。

H 1.2.14 changes the prior 1.2.13 artifact metadata description and adds the required D-only owner high-water field described in §6. The C Provider Outcome branch retains the corrected 1.2.13 semantics. No C object schema change is implied.

## 2. Exact duplicated field mapping / 重复字段精确映射

| H wire field | C immutable object field | Rule |
|---|---|---|
| c_submit_outcome_ref | record_ref | Exact immutable object identity |
| c_submit_outcome_digest | payload_digest | Exact equality and recomputation under C profile |
| provider_outcome | Outcome | Exact enum equality |
| provider_ref | ProviderRef | Exact typed identity |
| provider_adapter_ref | AdapterRef | Exact typed identity |
| provider_idempotency_key_ref | IdempotencyKeyRef | Key only; namespace remains C-object-only |
| final_request_boundary_id | FinalRequestBoundaryRef | Exact boundary |
| request_digest | RequestDigest | Exact digest |
| transaction_ref | CausalOrderTransactionRef | Exact transaction |
| provider_outcome_evidence_ref | OutcomeEvidenceRef | Exact evidence reference |
| provider_request_ref | ProviderRequestRef | Exact when applicable |
| provider_receipt_ref | ProviderReceiptRef | Exact when applicable |
| provider_lookup_proof_ref | ProviderLookupProofRef | Exact when applicable |
| provider_no_handoff_proof_ref | ProviderNoHandoffProofRef | Exact when present/required |
| not_invoked_proof_ref | NotInvokedProofRef | Exact for NOT_INVOKED |
| unknown_reason_ref | UnknownReasonRef | Exact for UNKNOWN / IN_DOUBT |
| owner_signature_ref | OwnerSignatureRef | Exact C signature evidence reference |
| owner_admission_ref/digest | CAdmissionRef/CAdmissionDigest | Exact C admission |
| owner_ledger_ref/version | COwnerLedgerRef/COwnerLedgerVersion | C ledger, not Storage ledger |
| owner_local_sequence/high-water/root | COwnerLocalSequence/COwnerHighWater/COwnerLedgerRoot | Exact C ledger tuple |
| coc_participant_intent_ref | COCParticipantIntentRef | Single authoritative nullable COC intent |
| participant_reservation_ref | COCParticipantReservationRef | Exact reservation |
| coc_absence_reason | COCAbsenceReason | Exact when intent/reservation are absent |

All duplicated values are exact equality assertions. A mismatch is INVALID; an unavailable object, ledger, verifier or currentness source is UNKNOWN. H 1.2.14 does not contain the legacy participant_intent_ref alias. It must not be accepted or normalized.

## 3. Mandatory C-object dereference / 强制 C 对象解引用

The following are mandatory C object fields even when not inlined in H:
- CGateRef/CGateGeneration/CGateCommitRef/CGateCommitDigest;
- ProviderAttemptRef/ProviderAttemptGeneration;
- ProviderAccountRef/AdapterBuildRef/EndpointRef/RegionRef/ApiOperation;
- IdempotencyNamespaceRef/ProviderCapabilityRecordRef/ProviderCapabilityDigest;
- FinalRequestBoundaryType/RequestContentType/RequestMethod;
- SideEffectStatus/OutcomeObservedAt/OutcomeEvidenceDigest/ProviderEvidenceIssuerRef/ProviderEvidenceType;
- sequence_namespace_ref;
- prior/supersession/reconciliation observation links.

CSubmitOutcome 1.0.1 sequence_namespace_ref must equal the authenticated CKeyStatusEvent sequence namespace and the namespace of the authoritative C signing sequencer. H's key-status callback must prove record_sequence and event_sequence are allocated in that same durable monotonic namespace. A proven mismatch is INVALID; unavailable sequencer/key-status/anti-rollback evidence is UNKNOWN.

C ProviderAttempt is not Storage prepare_attempt; C OwnerLedger is not Storage participant_ledger. COC, I, D and Storage proof references remain independent typed authorities.

## 4. Outcome semantic predicates / Outcome 语义谓词

| C Outcome | C SideEffectStatus | Required evidence | H semantic result |
|---|---|---|---|
| HANDOFF_ACCEPTED | PROVEN_OCCURRED | provider request + receipt + outcome evidence + COC reservation/intent | VALID only after C/provider evidence and all owner joins verify |
| HANDOFF_REJECTED | PROVEN_NONE | provider request + outcome evidence + ProviderNoHandoffProofRef | No-side-effect only after authoritative proof verifies |
| HANDOFF_REJECTED | POSSIBLE_OR_UNKNOWN | provider request + outcome evidence; no fabricated no-handoff proof | Nonterminal/blocking; never safe retry-as-new |
| HANDOFF_REJECTED | PROVEN_OCCURRED | provider request + outcome evidence | Preserve occurred side effect and reconcile |
| NOT_INVOKED | PROVEN_NONE | ProviderNoHandoffProofRef + NotInvokedProofRef; no provider receipt | Requires same durable gate serialization authority proof |
| UNKNOWN / IN_DOUBT | POSSIBLE_OR_UNKNOWN | unknown reason | Preserve original attempt/key/request tuple; no retry-as-new |

A provider rejection label does not prove no handoff. HANDOFF_REJECTED + PROVEN_NONE requires ProviderNoHandoffProofRef only; it does not require NotInvokedProofRef. NOT_INVOKED requires both proofs. H must read C SideEffectStatus from the immutable C object and never infer it from the H enum.

Provider 拒绝标签不证明没有交接。HANDOFF_REJECTED + PROVEN_NONE 只要求 ProviderNoHandoffProofRef，不要求 NotInvokedProofRef；NOT_INVOKED 才要求两种 Proof。H 必须读取不可变 C 对象中的 SideEffectStatus，不得从 H 枚举推断。

## 5. Digest and profile separation / 摘要与 Profile 隔离

- C c_submit_outcome_digest equals C object payload_digest.
- BMCP envelope payload_digest is a separate digest domain.
- C OutcomeEvidenceDigest is a third separate digest domain.
- C object signature and BMCP envelope signature are separately verified.
- C profile candidate is AIMBA-C-CRYPTO-1.0; I profile is AIMBA-I-CRYPTO-1.0.
- C has not adopted AIMBA-C-OUTCOME-CRYPTO-1.0; it is a non-normative example only.
- I may govern trust registration/status within I's authority but cannot rename C's profile.
- Both profiles remain non-production until their trust/key lifecycle and anti-rollback requirements are approved and deployed.

## 6. H 1.2.14 D high-water delta / H 1.2.14 D 高水位变化

H 1.2.14 adds required ownerSpecificHighWatersD.forget_fence_generation_high_water. It is distinct from owner_gate_generation and barrier_generation. It captures D's authoritative ForgetFenceGeneration high-water and is bound by the D owner snapshot attestation and owner_specific_high_waters_digest. It is not a C field, not part of C's P0 and not comparable with C GateGeneration, I PermissionEpoch, COC term/index or Storage LSN.

H 1.2.14 新增必需字段 ownerSpecificHighWatersD.forget_fence_generation_high_water，与 owner_gate_generation、barrier_generation 严格区分。该字段由 D Snapshot Attestation 与 owner_specific_high_waters_digest 绑定，不属于 C 字段或 C P0，不得与 C GateGeneration、I PermissionEpoch、COC term/index 或 Storage LSN 比较。

## 7. RecoveryJoin and owner membership / RecoveryJoin 与 Owner Membership

H RecoveryJoin 1.0.2 uses a closed generic ownerSnapshotMembershipProof object with additionalProperties=false. C/D/I-specific facts are committed by each owner's exact owner entry, operation, scope and snapshot digests; no ad hoc untyped properties are added. The C, D and I owner-specific crosswalks are:
- C Phase 3.8.13 RecoveryJoin P0 crosswalk: Blob df12af95e6859a389ba71eb1b7dba512b9feb8f6.
- D Phase 3.8.6 RecoveryJoin P0 crosswalk: Blob bf35b7f047a374268920b99199c06fc2a78dabb7.
- I Phase 3.8.10 P0 allowlists: Blob 35e6843da8becbf3b152512a561b05cf5486819b.
- H Phase 3.8.11 C/D/I cross-review: Blob 36c9e53dbec3b1e71eea22ddcb52a5d1d9f459c8.

C, D and I retain their own authority. H verifies exact typed references/digests and owner-specific high-water summaries; it does not synthesize owner facts or issue owner releases. L3 per-owner P0 vectors, full pagination/currentness proofs and independent human Owner approvals remain open.

## 8. Exact CI evidence / 精确 CI 证据

- Workflow: H Provider Outcome Conformance.
- Run: 44067402639.
- Tested commit: 2068dd4f89245f9a4913ac069a169a2bed5471be.
- Job: provider-outcome / 133984532592.
- Result: **SUCCESS — 22 tests passed, 0 failed**.
- Exact schema at tested commit: H Unified 1.2.14 Blob 09fcd1fa29fe24255fbd87cae79dafb406594a59.
- Validator core: Blob 910e2a8f0b22adb4a192b3dbb7483e52a881e993.
- Test source: Blob 9ceab387e114f9a28f9dfc12602e57f3ec5a3f43.

The run covers H 1.2.14 artifact revision, D ForgetFenceGeneration high-water distinctness, C 1.0.1 sequence namespace, conditional HANDOFF_REJECTED semantics, legacy intent alias removal, Python/Node candidate signature agreement and field-mutation rejection.

该 Run 精确覆盖 H 1.2.14 当前 Schema Blob、C 1.0.1 Sequence Namespace、D Fence High-Water 区分、HANDOFF_REJECTED 条件语义、旧 Intent Alias 移除、Python/Node 候选验签一致性与字段篡改拒绝，22/22 PASS。

**Evidence ceiling:** candidate structural/semantic/crypto-vector conformance only. It does not register C/I profiles, deploy production trust roots/key custody/anti-rollback, prove provider truth, execute live C egress races, prove D fence currentness, close COC/Storage bidirectional RecoveryJoin or authorize production activation.

## 9. Remaining blockers / 剩余阻断项

1. C exact review of H Unified 1.2.14 C Provider Outcome mapping is required; earlier C review pins H 1.2.13.
2. H full-envelope positive/negative fixtures and every duplicated-field mutation matrix remain incomplete.
3. Exact schema Blob/content hash must be enforced by the trusted deployment loader/release manifest.
4. I per-family P0 L3 vectors, profile registration, trust roots, key lifecycle, historical verification and anti-rollback deployment remain OPEN.
5. C profile registration, C key-status production service, C sequencer and provider-specific same-key lookup/idempotency remain OPEN.
6. Provider adapter lost-ACK, timeout, partial-write, SDK retry, failover and close-vs-send race evidence remains OPEN.
7. Storage must bind C/H/I/D proof tuples into a bidirectional RecoveryJoin and prove same-GID resolution, quorum persistence and linearizable readback.
8. D lineage completeness, late-discovery tests and final release CAS remain OPEN.
9. A must perform a fresh exact-version integration review after C/D/I/H and Storage pin the same current bundle.

## 10. H disposition / H 侧结论

**Delegated H-role decision: ACCEPT H Unified 1.2.14 × CSubmitOutcome 1.0.1 AS THE CURRENT L1/L2 MAPPING CANDIDATE WITH ENUMERATED L3/TRUST/STORAGE BLOCKERS. NOT FROZEN.**

JF-10 P0 remains OPEN. No provider exactly-once, production egress, Gate B/C, Multi-PolicyDomain, Global Forget completion, physical Forget or production activation is claimed.

**角色模拟 H 侧结论：接受 H Unified 1.2.14 × CSubmitOutcome 1.0.1 作为当前 L1/L2 Mapping 候选，L3/Trust/Storage 阻断项仍 OPEN，不冻结。** JF-10 P0 仍 OPEN。
