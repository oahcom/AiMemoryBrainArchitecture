# F Owner — Exact JF-10 Prepared Participant Identity / GID Index-Boundary Acceptance

- Storage protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A integration mapping Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- B typed-reference registry Blob: `63ccb4bf687b00dea2b21fc2773f3018648d76e6`
- H BMCP schema 1.1.1 candidate Blob: `c0bbfc7611a8d88a39cee209831db32b62601fde`
- Decision: **ACCEPT WITH F INDEX / CACHE IDENTITY SEPARATION CONDITIONS**
- Mode: delegated F-boundary review under user instruction; not independent human sign-off.

F accepts the prepared participant identity mapping subject to the following:

1. `PreparedParticipantRef` is the stable Storage participant identity; `PreparedTransactionGID` is the Storage/engine-specific prepared handle; `EngineNativeTransactionXIDRef` is post-PREPARE evidence only. None is an F IndexPartitionRef, IndexWatermark, CacheGeneration, WorkingSetRef, SourceArtifactRef or ForgetFenceGeneration.
2. F indexes and caches bind to the immutable source PublicationOperationId/RequestDigest/manifest/VisibilityPointer/PublicationReceipt proof. Storage participant/GID evidence is a supporting source-commit reference, not the index's identity or serving permission.
3. F must not rebuild or serve from a restored/pre-fence snapshot until D ForgetFence/lineage high-water and I current policy/registry proofs are reconciled. A same-GID Storage commit proof does not clear a D tombstone or restore I authorization.
4. Cache invalidation, partition watermarks and rebuild workers remain separate F-owned controls. A native XID, GID, Storage receipt, COC position or I/D epoch cannot be substituted for an F partition watermark or cache generation.
5. Same participant/GID retry must preserve the original source operation tuple; a changed participant, GID, request digest or VisibilityPointer is a conflict and requires source-owner reconciliation.
6. Unknown/unsupported Storage outcome, stale replica, cache fill racing invalidation, incomplete partition watermark or missing D/I proof remains suppressed/Unknown; no timeout or cache eviction proves deletion.

F's 19-test anti-resurrection reference model remains logical evidence only. Actual ANN/index/cache/Working Set runtime, multi-process invalidation, restore and reconnect tests remain NOT RUN. This is design acceptance only; no F runtime conformance or production activation is claimed.