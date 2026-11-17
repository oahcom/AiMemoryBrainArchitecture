# Phase 3.6.12 — Storage Exact Recovery Batch / Manifest Ordering and Bundle Amendment

- Owner perspective: Storage / Consistency
- Status: **PROPOSED STORAGE AMENDMENT — EXACT C / H / A REVIEW REQUIRED**
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED

## 0. Exact immutable source set

| Artifact | Exact Blob | Role |
|---|---|---|
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` | Base Storage durability/participant contract |
| COC base protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` | Historical immutable base; §6.2 is superseded by the ordering addendum below |
| Storage/COC Batch-Manifest ordering amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Normative two-phase order |
| H Recovery Cutoff schema 1.0.5 | `3d451778b9867c3b54779c5cd478522993719025` | Structural message contract |
| H two-phase wire/validator addendum | `5a3def4f7e84ed489993681455b6840b93ecc282` | Content/record digest and bidirectional batch-manifest validation |
| C owner-local provider gate amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` | C admission and actual provider egress authority |
| I Phase 3.6.8 | `929b30ba10ac627927d3959e0777b467846b268d` | I global inventory, receipt and restore currentness |
| D Phase 3.6.8 | `0668667daeb936bf223ab049277ea2a4117c3b09` | D fencing, barrier and terminalization |

Storage v2 `4ed4234ce548a814a9496adf7a14c4459ea9f7ce` remains historical only. Storage v3.1 and the COC base are not overwritten; this addendum creates a new exact review target.

## 1. Storage ruling on the ordering defect

Storage confirms that COC base protocol §6.2 is insufficient: it commits RECOVERY_CUTOFF_BATCH before participant enumeration even though the batch is required to bind the participant-set digest. Storage v3.1 §5.4 already identified a precomputed-manifest / batch / committed-manifest sequence, but the digest names and reverse link were underspecified.

The normative sequence is now the exact order in the Storage/COC amendment Blob `9704d110a06d0c2ee98be960054e0396d0b68546`:
1. Verify immutable quorum prefix P and freeze I/D/C owner snapshots.
2. Enumerate all participants in P and precompute a stable immutable manifest payload and ParticipantManifestContentDigest.
3. Commit RecoveryCutoffBatch binding ManifestId + ParticipantManifestContentDigest and exact owner snapshots.
4. Commit COC_PARTICIPANT_MANIFEST after the batch, adding RecoveryBatchRef + RecoveryBatchDigest and retaining the same ManifestId/content digest/P/entries.
5. Read back both committed records and verify their cross-bindings and log order.
6. Only then begin participant reconciliation; owner releases and RecoveryEpochCompleted remain later independent steps.

The Batch does not bind the future final manifest-record digest. The final manifest record digest is computed only after its batch back-reference exists. This prevents a circular digest dependency.

## 2. Three digest contract

- `ParticipantManifestContentDigest`: precomputed digest over the stable manifest content projection; excludes batch backlink, quorum proof and envelope.
- `RecoveryBatchDigest`: digest over the batch payload, including ManifestId and ParticipantManifestContentDigest.
- `ParticipantManifestRecordDigest`: final committed manifest payload digest, including RecoveryBatchRef and RecoveryBatchDigest.

The values are distinct and MUST NOT be copied into a generic digest field. The H 1.0.5 schema expresses:
- Batch → ManifestId + ContentDigest;
- Manifest → BatchRef + BatchDigest + same ContentDigest;
- Owner Release / RecoveryEpochCompleted → ContentDigest + final RecordDigest.

H's exact canonicalization profile and I's cryptographic/trust policy remain open until jointly approved. No signature algorithm or canonical-byte profile is frozen here.

## 3. C, H and owner boundary conditions

### 3.1 C — provider outcome

C owns provider admission, reservation/attempt identity, actual egress boundary and CSubmitOutcome. COC Batch/Manifest commitment proves prefix membership only. It does not prove provider invocation or success. A reserved or queued NOT_DISPATCHED attempt cannot cross egress after C Gate close. A SENT_OR_AMBIGUOUS attempt is reconciled using the same provider idempotency key; lost ACK cannot authorize retry-as-new. No authoritative same-key lookup means IN_DOUBT and blocks C release.

### 3.2 H — wire/schema

H owns strict message schema, field encoding, canonicalization rules, schema evolution and cross-message semantic validators. Schema 1.0.5 and H addendum Blob `5a3def4f7e84ed489993681455b6840b93ecc282` are the candidate wire contract. H must verify bidirectional Batch/Manifest binding, distinct digest semantics, quorum order, complete prefix enumeration and C owner-admission joins. JSON Schema validity alone is not semantic acceptance.

### 3.3 I/D/Storage authority

I, D and C independently sign/release only their own outage gates. Storage attests only its prepared participant and same-XID visibility resolution. COC records ordering/evidence; it does not mint owner decisions. The exact I/D/Storage/Restore tuple remains independently authoritative and currentness-checked.

## 4. Storage acceptance gate for a recovery round

A round is eligible for participant reconciliation only if:
- prefix P and checkpoint/anti-rollback proof are current;
- I/D/C owner snapshots are exact, signed, complete and separately rooted;
- staged ManifestId/content digest has complete prefix enumeration;
- Batch is quorum committed after P and references exact ManifestId/content digest;
- Manifest record is quorum committed after Batch and back-references exact BatchId/BatchDigest;
- both records bind same RecoveryEpoch/round/P/count/root/entries;
- linearizable readback proves Batch position < Manifest position;
- all digests recompute under the exact declared H profile;
- no UNKNOWN, missing owner, partial enumeration, duplicate participant, stale high-water or cross-owner mismatch exists.

A crash between Batch and Manifest commit is a fenced incomplete pair, not a successful batch and not a reason to mint a new batch identity. Recovery must resume by exact stable IDs/digests or enter RESTORE_FENCED.

## 5. Exact review requirements and status

Required exact-version review:
- C: verify provider outcome remains exclusively C-authoritative and C owner admissions join the manifest exactly.
- H: verify schema 1.0.5, digest separation, Batch-before-Manifest ordering, reverse binding, release/completion digest requirements and semantic vectors.
- A: integrate this exact bundle with A §§11–12, I/D Phase 3.6.8, Storage participant identity and restore/anti-rollback semantics.
- I/D: re-review only if final integrated bundle changes their authority-owned fields or currentness requirements.

**Status:** proposed Storage ordering correction. It is not independent human Storage Owner approval, not a C/H/A acceptance, not a quorum/restore conformance result, not implementation PASS, not production activation and not Global Forget Completion.

## 6. Provenance

This document is an assistant-authored Storage role proposal committed at the user's direction. It is not a cryptographic signature or proof of independent human Owner authorship.
