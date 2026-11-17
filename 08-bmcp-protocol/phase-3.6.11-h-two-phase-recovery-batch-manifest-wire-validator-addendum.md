# Phase 3.6.11 — H Two-Phase Recovery Batch / Manifest Wire and Semantic Validation Addendum

- Owner perspective: H — BMCP Protocol Architect
- Status: **PROPOSED WIRE/VALIDATOR AMENDMENT — EXACT-VERSION H / C / A REVIEW REQUIRED**
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT INTEROPERABILITY-VERIFIED

## 0. Exact source bundle

| Source | Exact Blob |
|---|---|
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| COC base protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| Storage/COC Batch-Manifest ordering amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` |
| I Phase 3.6.8 | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C Phase 3.6.9 | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| H Recovery Cutoff schema 1.0.4 predecessor | `d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1` |
| H Recovery Cutoff schema 1.0.5 candidate | `3d451778b9867c3b54779c5cd478522993719025` |
| H semantic validator predecessor | `7e6f67518e476fe9798f23a87798c7a3eb352f3c` |
| H wire contract predecessor | `b4cae9c0c9121c27ea2933c029b83b3f4367672b` |

Schema 1.0.5 is a structural candidate. It does not freeze canonical bytes, digest/signature algorithms or trust policy.

## 1. Digest names and non-interchangeability

H defines three independent digest semantics. A field named `participant_manifest_digest` is deprecated for new 1.0.5 messages because it is ambiguous.

### 1.1 ParticipantManifestContentDigest

This is computed before the RecoveryCutoffBatch commit over the domain-separated canonical manifest-content projection:
- stable ManifestId/message_id;
- RecoveryEpoch and exact prefix P (term, index, root);
- previous-prefix digest;
- enumeration status;
- canonical ordered participant entries;
- participant count and participant-set root.

It excludes:
- RecoveryBatchRef and RecoveryBatchDigest (not yet available);
- quorum commit proof;
- signature/envelope fields and transport metadata.

The canonicalization and digest profile identifiers are carried by the protected envelope/profile contract. The exact digest preimage must be identical across implementations. H does not select I's signature algorithm or key policy.

### 1.2 RecoveryBatchDigest

This covers the canonical RecoveryCutoffBatch payload, including stable BatchId, RecoveryEpoch/round, exact prefix P, I/D/C snapshot refs and digests, scope binding, reconciliation attempt generation, previous-batch digest, ManifestId and ParticipantManifestContentDigest.

### 1.3 ParticipantManifestRecordDigest

This is the digest of the final committed `COC_PARTICIPANT_MANIFEST` record payload, including RecoveryBatchRef + RecoveryBatchDigest and ParticipantManifestContentDigest. It is represented by the committed manifest record's protected payload digest. It is computed only after the batch has committed and the manifest back-reference is present.

No circular dependency exists:
`ManifestContentDigest → RecoveryBatchDigest → ManifestRecordDigest`.
The batch never contains the future ManifestRecordDigest.

## 2. Schema 1.0.5 normative field mapping

The exact structural schema is `schemas/bmcp.recovery-cutoff-1.0.5.schema.json`, Blob `3d451778b9867c3b54779c5cd478522993719025`.

### 2.1 RECOVERY_CUTOFF_BATCH

Required manifest binding:
- `participant_manifest_ref`: stable ManifestId;
- `participant_manifest_content_digest`: precomputed immutable content digest.

It MUST NOT carry a final manifest-record digest because that record is committed after the batch.

### 2.2 COC_PARTICIPANT_MANIFEST

Required reverse binding:
- `message_id`: same stable ManifestId referenced by the batch;
- `participant_manifest_content_digest`: same precomputed content digest;
- `recovery_batch_ref`: exact committed BatchId;
- `recovery_batch_digest`: exact committed RecoveryBatchDigest;
- `quorum_commit_proof_ref`: proof of this manifest record's own later quorum commit.

The final manifest's envelope payload digest is the ParticipantManifestRecordDigest. It is distinct from ParticipantManifestContentDigest.

### 2.3 OWNER_GATE_RELEASE_ATTESTATION

Each owner release binds:
- RecoveryBatchRef + RecoveryBatchDigest;
- ParticipantManifestContentDigest;
- ParticipantManifestRecordDigest;
- exact owner snapshot/gate generation/high-waters/roots/scope generation/anti-rollback anchor/final currentness CAS.

A release that omits either manifest digest is invalid. An owner cannot release based on the staged manifest payload alone.

### 2.4 RECOVERY_EPOCH_COMPLETED

COC completion binds final batch ref/digest, ParticipantManifestContentDigest, ParticipantManifestRecordDigest, all-rounds root and required owner release references. It is a COC observation only.

## 3. Semantic validator order and joins

The validators MUST enforce this order:

1. Validate quorum-certified prefix P and complete prefix enumeration.
2. Validate staged immutable manifest content, stable ManifestId, content digest, count, root, explicit empty/non-empty status and exact P.
3. Validate the RecoveryCutoffBatch references the staged ManifestId/content digest and exact owner snapshot refs/digests; verify its quorum commit.
4. Validate the committed ParticipantManifest is ordered after that Batch in the same committed COC log, references the exact BatchId/BatchDigest, and repeats the exact ManifestId/content digest/P/count/root/entries.
5. Recompute ParticipantManifestRecordDigest from the committed manifest record and verify the envelope payload digest.
6. Verify both records by linearizable readback and verify their predecessor/term/index continuity.
7. Only then accept the pair as `BATCH_MANIFEST_PAIR_VERIFIED` and begin participant reconciliation.

Cross-message assertions:
- Batch.participant_manifest_ref == Manifest.message_id.
- Batch.participant_manifest_content_digest == Manifest.participant_manifest_content_digest.
- Manifest.recovery_batch_ref == Batch.message_id.
- Manifest.recovery_batch_digest == Batch.batch_digest.
- Batch and Manifest RecoveryEpoch/round and prefix term/index/root are identical.
- Manifest content digest recomputes from the defined projection.
- Manifest record digest equals its protected envelope payload digest and is later referenced by each release/completion record.
- Batch log position < Manifest log position.
- No participant intent may be inserted into the closed prefix between P and the Batch; no protected new intent is admitted until Batch commitment and recovery rules permit it.
- ParticipantManifest entries enumerate every participant intent in P exactly once; owner-local C admissions not yet registered remain in C's separate admission snapshot and are never fabricated into COC entries.

Any mismatch is INVALID or UNKNOWN according to evidence availability; neither may be coerced to empty or success.

## 4. Crash and replay semantic validators

- Crash before batch commit: no authoritative Batch exists.
- Crash after batch but before manifest: remain fenced; recover exact same ManifestId/content digest and commit its record with the exact batch back-reference.
- Staged payload missing or changed after batch commit: RESTORE_FENCED; do not mint a replacement manifest under the same batch.
- Crash after manifest commit but before pair readback: same-key linearizable lookup and pair verification; no replacement records.
- Repeated round: new immutable round/batch/manifest identities and previous-batch link; old pairs remain unchanged.

Same message identity + same digest is idempotent replay. Same identity + changed digest is CONFLICT.

## 5. C Provider Outcome cross-boundary rules

H validates that the C owner snapshot and every C-owned participant entry bind the exact CAdmissionRef/owner_entry_ref, operation identity, request digest, scope, provider reservation/attempt identity and COC prefix position where registered.

H MUST NOT infer provider outcome from:
- COC ParticipantIntent or RecoveryCutoffBatch commitment;
- ParticipantManifest membership;
- provider reservation;
- DISPATCH_AUTHORIZED without authoritative egress evidence;
- transport ACK, timeout, lost ACK or client response.

Only C's signed CSubmitOutcome, backed by the actual provider egress boundary and provider-specific same-key lookup/receipt, is provider-outcome evidence. SENT_OR_AMBIGUOUS remains UNKNOWN until authoritative same-key resolution. If the provider has no authoritative same-key lookup, the attempt remains IN_DOUBT and C release is blocked.

## 6. Required positive/negative vectors — specified, not run

- Batch references a ManifestRecordDigest instead of the precomputed ContentDigest: INVALID.
- Manifest committed before Batch: INVALID.
- Batch commits, manifest does not: pair incomplete; remain fenced.
- Manifest back-reference points to wrong BatchId or BatchDigest: INVALID.
- ContentDigest stable across addition of batch back-reference; RecordDigest changes accordingly.
- Release references ContentDigest but omits RecordDigest: INVALID.
- EpochCompleted references only one of the two manifest digests: INVALID.
- Batch/Manifest mismatch on prefix, RecoveryEpoch, count, root or entries: INVALID.
- Prefix enumeration incomplete or stale: UNKNOWN.
- COMPLETE_EMPTY without authoritative complete enumeration and canonical empty root: INVALID/UNKNOWN.
- C provider outcome inferred from COC commit/manifest: INVALID.
- C SENT_OR_AMBIGUOUS with no authoritative same-key lookup: UNKNOWN; C release blocked.
- Same stable identity/digest replay: VALID idempotent; changed digest: CONFLICT.

## 7. Status and provenance

This is an assistant-authored H role proposal committed at the user's direction. It is not an independent human H Owner signature. Schema 1.0.5 and this addendum require exact H/C/A review, executable semantic validators and cross-implementation canonical-byte fixtures.

No schema freeze, signature-policy approval, interoperability PASS, runtime conformance, deployment, production activation or JF-10 P0 closure is claimed.


## 8. Exact-version rebinding for revised Phase 3.6.8 I/D and COC ordering bundle

This section supersedes the historical source pins in §0 for the next exact-version review. The earlier pins remain provenance for the original drafting pass; they are not the current review target.

| Artifact | Exact Blob | H treatment |
|---|---|---|
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` | Normative Storage manifest-first/two-record semantic source |
| COC protocol with §15–16 supersession | `a07a8d352f31d5406786e1cd8ecddd4065ec384a` | Current COC candidate; §15 fixes order, §16 fixes digest projections |
| Storage ordering amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Detailed two-phase content/batch/record digest contract |
| I Phase 3.6.8 revised source | `cf4b76f151204fa47b156b5d807e7378c28fd268` | Current I owner-local source |
| D Phase 3.6.8 revised source | `2d95099a2e19a8cbec325925b70da576f73d9899` | Current D owner-local source |
| C Provider Outcome contract | `f538d921d06c92dfaba13fbe326a80d6550fe1b7` | C-owned provider outcome semantics |
| C exact-version re-review of revised bundle | `c0f113f2fda52450f1f2aa3bff187cb1279022d0` | C accepts with provider-specific exceptions |
| H Recovery Cutoff schema 1.0.5 | `3d451778b9867c3b54779c5cd478522993719025` | Structural candidate only |

### 8.1 Normative ordering and digest consistency

H confirms the following pair construction and validator order:

1. Freeze owner snapshots and verify exact committed prefix P.
2. Enumerate all participant intents through P and stage immutable manifest content; compute ParticipantManifestContentDigest before Batch commit.
3. Commit RecoveryCutoffBatch binding ManifestId + ParticipantManifestContentDigest and exact owner snapshots.
4. Commit COC_PARTICIPANT_MANIFEST after the Batch, binding exact RecoveryBatchRef + RecoveryBatchDigest and the same content digest.
5. Compute/verify ParticipantManifestRecordDigest over the final committed manifest record.
6. Linearly read back both records and verify their cross-bindings and log order before entering PARTICIPANTS_RECONCILING.

The three digests are non-interchangeable:
- ParticipantManifestContentDigest is precomputed before Batch and excludes the future Batch back-reference.
- RecoveryBatchDigest covers the committed Batch payload and its reference to ManifestId/content digest.
- ParticipantManifestRecordDigest covers the final committed manifest record including the Batch back-reference.

The required dependency is ContentDigest → BatchDigest → ManifestRecordDigest. A Manifest *record* committed before Batch is invalid; precomputing/staging its immutable content before Batch is required. The batch MUST NOT include the future ManifestRecordDigest.

### 8.2 C provider boundary

C's provider gate remains closed after Batch commit but before Manifest Record commit, and after Manifest Record commit but before exact linearizable pair readback. Only after S4 pair readback and independent current C/I/D/Storage predicates may C begin provider-specific lookup/reconciliation. H validates C-owned CSubmitOutcome references and MUST NOT infer provider success from Batch, Manifest membership, Storage resolution, I terminality, D clearance or transport ACK.

### 8.3 Exact-version review result and limits

The current schema 1.0.5 fields and this addendum's digest/order semantics are consistent with revised COC §15–16 and the C Provider Outcome contract. This is a semantic exact-version consistency finding only; it does not claim:
- H independent human Owner approval or cryptographic signature;
- executable validator implementation or passing tests;
- canonical-byte interoperability across independent implementations;
- approval of I's cryptographic/key lifecycle profile;
- production provider same-key lookup or exactly-once behavior;
- joint protocol freeze or production activation.

The existing §6 vectors remain **SPECIFIED / NOT RUN**. H exact-owner decision and A final integration review are still required.
