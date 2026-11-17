# Phase 3.6.4 — COC Recovery Cutoff Batch / Participant Manifest Ordering Amendment

- Owner: Storage / Consistency (COC durable-log authority)
- Status: **PROPOSED NORMATIVE AMENDMENT — EXACT C / H / A REVIEW REQUIRED**
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED
- Base COC protocol: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- Storage Design v3.1 source: `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- H recovery schema 1.0.4 predecessor: `d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1`
- H recovery schema 1.0.5 candidate: see exact binding manifest after branch readback

## 1. Defect being closed

The base COC protocol §6.2 places `RECOVERY_CUTOFF_BATCH` before participant enumeration, while the batch record description requires the participant-set digest. It therefore asks the coordinator to commit a digest before it has completed the authoritative enumeration that produces that digest.

A second ambiguity is that Storage Design v3.1 §5.4 uses a precomputed manifest digest in the batch, then commits a manifest record after the batch, but does not sufficiently distinguish:
- immutable manifest-content digest;
- quorum-committed batch digest; and
- final committed manifest-record digest.

Those digests are not interchangeable. Treating them as one value creates a circular dependency because the batch references the manifest while the final manifest must reference the batch.

This amendment normatively supersedes base COC protocol §3.2's abbreviated `RECOVERY_CUTOFF_BATCH` participant-set binding and §6.2's ten-step recovery ordering wherever they conflict. It does not rewrite the historical base blob.

## 2. Typed digest model

The protocol defines three independent digests:

1. **ParticipantManifestContentDigest** — computed before the batch commit over the domain-separated canonical immutable manifest-content projection. The projection includes ManifestId, RecoveryEpoch, exact prefix P (term/index/root/configuration epoch), previous-prefix digest, enumeration status, canonical ordered participant entries, count and participant-set root. It excludes the future RecoveryBatchRef/RecoveryBatchDigest, quorum commit proof and transport/signature envelope.
2. **RecoveryBatchDigest** — computed over the canonical batch payload. It binds the stable RecoveryBatchRef, RecoveryEpoch/round, exact prefix P, I/D/C owner snapshot refs and digests, scope binding, reconciliation attempt generation, ManifestId and ParticipantManifestContentDigest, and previous-batch digest where applicable.
3. **ParticipantManifestRecordDigest** — the payload digest of the final quorum-committed `COC_PARTICIPANT_MANIFEST` record. It covers the complete manifest record including exact RecoveryBatchRef and RecoveryBatchDigest, ParticipantManifestContentDigest, prefix, entries, quorum proof reference and protected envelope fields according to the selected H profile.

No field named simply `participant_manifest_digest` may ambiguously refer to both content and final record digest in new wire versions. The 1.0.5 wire fields are:
- batch: `participant_manifest_ref` + `participant_manifest_content_digest`;
- manifest: `message_id` + `participant_manifest_content_digest` + `recovery_batch_ref` + `recovery_batch_digest`;
- owner release and RecoveryEpochCompleted: `participant_manifest_content_digest` + `participant_manifest_record_digest`.

The manifest content digest is not the record digest. The final manifest record digest is not included in the batch, so there is no circular hash dependency.

## 3. Normative two-phase commit order

For each immutable RecoveryEpoch/round, the coordinator MUST perform the following order while COC remains RECOVERY_FENCED and all applicable I/D/C owner gates remain closed.

### Phase A — freeze, enumerate and precompute

1. Verify the newest quorum-confirmed COC committed prefix:
   `P = (CoordinatorEpoch, CoordinatorIndex, EntryDigest, VoterConfigurationEpoch)`.
   Verify checkpoint/anti-rollback continuity and all prior committed digest links. If P cannot be proven, enter RESTORE_FENCED.
2. Obtain exact signed I, D and C owner snapshot attestations. Each owner has already atomically closed its own gate and captured request/admission high-waters, roots, scope generation and anti-rollback anchor. Missing owner evidence is UNKNOWN, never empty.
3. Enumerate every ParticipantIntent committed at or before P using a linearizable COC read against P. Pagination/cursor continuity must be complete. Include pre-existing unresolved JF-10 participants. Never use a stale projection or follower-only read.
4. Build the complete immutable participant manifest payload, sorted by H's canonical opaque-reference ordering. Include explicit COMPLETE_EMPTY or COMPLETE_NON_EMPTY, exact count, participant-set root, P, RecoveryEpoch, previous-prefix digest and typed owner evidence references. Every C-owned participant entry must bind exact C owner admission identity, operation/request digest, scope and COC position. Storage entries bind the applicable JF-10 identity tuple.
5. Assign stable ManifestId and compute ParticipantManifestContentDigest using H's domain-separated canonical projection. Persist the prepared payload durably outside the committed COC log (or in an equivalent immutable content-addressed staging store) so it can be recovered by exact ID/digest. This staged payload is not a committed manifest and cannot be used to release gates or start participant reconciliation.
6. Re-read the exact prefix P and manifest payload by stable ID/digest. Confirm the payload is complete and still describes all ParticipantIntentRefs in P. If enumeration or content changes, discard only the uncommitted candidate and restart Phase A under a new reconciliation attempt generation; do not mutate a committed object.

### Phase B — quorum-commit Batch, then Manifest

7. Construct the RecoveryCutoffBatch using a stable BatchId. It MUST bind exact P, RecoveryEpoch/round, I/D/C snapshot refs and digests, their independent high-waters/roots/scope generations, ManifestId, ParticipantManifestContentDigest, participant count, reconciliation attempt generation and previous-batch digest.
8. Quorum-commit `RECOVERY_CUTOFF_BATCH`. The returned commit proof must establish the batch's committed term/index and RecoveryBatchDigest. The batch is the first recovery record appended after P for this round. No post-P protected participant intent may be admitted before this batch commit.
9. Only after step 8, construct and quorum-commit `COC_PARTICIPANT_MANIFEST` using the exact staged payload and adding RecoveryBatchRef + RecoveryBatchDigest. It MUST repeat P, RecoveryEpoch, ManifestId, ParticipantManifestContentDigest, count and participant-set root unchanged. The final record's payload digest is ParticipantManifestRecordDigest.
10. The coordinator MUST linearly read back both records and verify:
    - Batch references the exact ManifestId and ParticipantManifestContentDigest;
    - Manifest references the exact committed BatchId and RecoveryBatchDigest;
    - both bind the same RecoveryEpoch/round and exact P;
    - manifest content digest recomputes from the final manifest's immutable content projection;
    - count, participant-set root, enumeration status and entries match the staged payload;
    - both quorum commit proofs and log predecessor positions are valid and ordered Batch before Manifest.
11. Only after all checks in step 10 may state advance to PARTICIPANTS_RECONCILING. Owner releases and RecoveryEpochCompleted are impossible before this state.

## 4. Crash/restart rules

- **Crash before Batch commit:** no committed batch exists. Resume by stable RecoveryEpoch/round/ManifestId and exact staged digest or rebuild Phase A under a new attempt generation. No protected serving.
- **Crash after Batch commit but before Manifest commit:** next leader remains RECOVERY_FENCED. It performs same-key linearizable lookup of the exact BatchId and recovers the staged manifest payload by exact ManifestId/ParticipantManifestContentDigest. It commits the same manifest identity/content with the batch back-reference. It MUST NOT create a replacement batch, change ManifestId, alter participant membership or recompute a different digest under the same identity.
- **Staged manifest missing or digest mismatch after Batch commit:** RESTORE_FENCED. Do not replace the manifest or release any owner gate. Recovery requires an append-only governed repair record and a new recovery round; no in-place substitution.
- **Crash after Manifest commit but before readback:** remain fenced; linearly read back the same BatchId and ManifestId and validate all cross-bindings.
- **Crash during participant reconciliation:** retain the exact Batch/Manifest pair and append idempotent per-participant observations. Do not rebuild or reorder the pair.
- **Repeated cutoff round:** a new round has a new immutable RecoveryEpoch/round or round identity, new prefix P, new ManifestId/content digest, new BatchId/digest, and a previous-batch link. Earlier rounds are immutable and included in all-rounds root.

## 5. State machine and gate rules

`SERVING → QUORUM_UNAVAILABLE → RECOVERY_FENCED → PREFIX_VERIFIED → OWNER_SNAPSHOTS_FROZEN → MANIFEST_CONTENT_PREPARED → RECOVERY_CUTOFF_BATCH_COMMITTED → COC_PARTICIPANT_MANIFEST_COMMITTED → BATCH_MANIFEST_PAIR_VERIFIED → PARTICIPANTS_RECONCILING → OWNER_RELEASES_RECORDED → RECOVERY_EPOCH_COMPLETED → SERVING`

Any missing/stale/partial/unavailable proof moves to RESTORE_FENCED or remains RECOVERY_FENCED. No timeout or elapsed time advances state.

The owner-local release proof binds both:
- exact RecoveryBatchRef + RecoveryBatchDigest;
- exact ManifestId + ParticipantManifestContentDigest + ParticipantManifestRecordDigest;
- owner's current GateGeneration, snapshot ref/digest, high-waters, roots, scope generation, anti-rollback anchor and final currentness CAS.

I, D and C independently release only their own outage gates. COC records these releases; it never mints them. `RECOVERY_EPOCH_COMPLETED` requires all applicable owner releases and the exact verified Batch/Manifest pair, but is only a COC recovery observation.

## 6. H wire/schema requirements

The H recovery schema 1.0.5 MUST:
- add `recovery_batch_ref` and `recovery_batch_digest` to the committed ParticipantManifest;
- distinguish `participant_manifest_content_digest` from `participant_manifest_record_digest`;
- require the batch to bind ManifestId + content digest, not the not-yet-existing final record digest;
- require owner release and epoch completion to bind both content and final record digests;
- retain strict requiredness, unknown-critical rejection and explicit COMPLETE_EMPTY semantics.

The H semantic validator MUST verify the exact cross-message equality and ordering rules in §§3–5. JSON Schema structural validity alone is insufficient.

## 7. C provider outcome boundary

C's local admission/provider-attempt snapshot remains separate from the COC committed-prefix participant manifest. Each C owner admission is joined by exact stable identity, request digest, scope and (when registered) ParticipantIntentRef/position/digest. Provider outcomes remain C-authoritative:
- COC Batch/Manifest proves only that an intent was in the frozen committed prefix;
- a reservation or DISPATCH_AUTHORIZED state does not prove provider invocation;
- only C's authoritative egress boundary and same-key provider outcome lookup can prove SENT/NOT_SENT/OUTCOME;
- ambiguous send/lost ACK remains UNKNOWN/IN_DOUBT and blocks C release;
- no provider invocation may proceed after C Gate close unless a new post-recovery authorization is performed under current I/D/C gates.

This addendum does not make COC or Storage the provider-outcome authority.

## 8. Required conformance vectors — specified, not run

1. Participant enumeration completes before Batch construction and binds exact prefix P.
2. Batch cannot be committed if manifest content digest/count/root are absent.
3. Batch commit succeeds but manifest commit crashes; next leader recovers the same ManifestId/content digest and commits the same manifest.
4. Manifest cannot commit before its referenced Batch.
5. Manifest content digest stable when only batch backlink/quorum proof changes; final record digest changes and is separately bound.
6. Batch and Manifest with different P, RecoveryEpoch, count, root or content digest fail closed.
7. Participant omitted from a complete prefix enumeration is INVALID; partial pagination is UNKNOWN.
8. Empty participant set requires explicit empty array/count/root and complete authoritative enumeration.
9. Staged payload missing after Batch commit enters RESTORE_FENCED; no replacement ManifestId is minted.
10. Owner release referencing only the batch digest or only a manifest content digest (without final record digest) is rejected.
11. A later round cannot mutate or overwrite an earlier Batch/Manifest pair.
12. C admission NOT_REGISTERED is not fabricated into a COC participant; it remains a C owner-local obligation.
13. Provider send with ambiguous outcome remains UNKNOWN despite Batch/Manifest commitment.

## 9. Status and provenance

This is an assistant-authored Storage/COC role proposal committed at the user's direction. It is not an independent human Storage Owner signature or approval. It supersedes conflicting ordering language in the exact base COC protocol only after the required C/H/A exact-version reviews and binding-manifest publication.

No implementation, quorum durability test, schema interoperability, provider adapter conformance, production activation, physical erasure or Global Forget Completion is claimed.
