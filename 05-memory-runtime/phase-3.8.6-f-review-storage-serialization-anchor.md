# Phase 3.8.6 — F Review of Per-Authority Storage Serialization Anchor
# Phase 3.8.6 — F 对每 Authority Storage Serialization Anchor 的复审

- Owner: F — Memory Runtime
- Exact Storage ADR Blob: `bb544ba2f346bdc130d524bd5c7310d86f367988`
- Decision: **ACCEPT WITH READ-PATH AND CACHE CONDITIONS**
- Provenance: delegated F-role review, not independent human F Owner approval.

F accepts Option A's anchor as the D/Storage write-order substrate. F does not read or infer anchor revisions as Memory version, Recall freshness, Working Set epoch or visibility truth.

F 接受 Option A Anchor 作为 D/Storage 写入顺序底座。F 不读取或推断 Anchor Revision 为 Memory Version、Recall Freshness、Working Set Epoch 或 Visibility Truth。

1. Public read is authorized only by the exact committed Storage VisibilityPointer and matching artifact/version/digest.
2. PREPARED_HIDDEN and UNKNOWN remain absent from all serving reads, indexes, caches and Working Sets.
3. Stale replicas, cache invalidation lag and read-after-commit uncertainty cannot expose a pre-commit or forgotten artifact.
4. D ForgetFence/restore currentness is checked through D-owned evidence, not `SerializationRevision`.
5. F read-path watermarks remain F-owned and incomparable to the anchor revision.
6. If the DB read path cannot guarantee authoritative visibility-pointer state, fail closed.

**ACCEPT WITH CONDITIONS.** Runtime implementation, cache/index fault tests and deployment are L4 OPEN.
