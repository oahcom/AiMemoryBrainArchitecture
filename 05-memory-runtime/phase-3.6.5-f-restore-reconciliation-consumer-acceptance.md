# F Owner — Exact Restore Reconciliation / Anti-Resurrection Consumer Acceptance

- Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- I proof acceptance Blob: `85d62b8858fc86addacd3b83f49476e42f49b785`
- D proof acceptance Blob: `211e54acfb4573b1c51d96f07af297671dfc4c4b`
- A restore integration acceptance Blob: `fa5e066a208a64401c96a6b8790d8b53dc7f1585`
- Decision: **ACCEPT WITH F ANTI-RESURRECTION RESTORE GATES**

F accepts that restored indexes, partition snapshots, caches, Working Sets and rebuild workers are derived state and cannot be served merely because Storage restore completed. F must reconcile the restored source with current I PermissionEpoch/registry and D ForgetFence/lineage proofs, replay tombstones/fences through the relevant high-water, invalidate stale watermarks/cache entries, and only then rebuild/re-enable retrieval.

Storage RestoreReconciliationReceipt is not an F IndexWatermark, D clearance, I authorization or Global Forget completion. A stale replica, cache fill racing invalidation, rebuild from a pre-fence snapshot, missing partition watermark or offline Adapter remains suppressed/Unknown. The current F 19-test anti-resurrection model is logical evidence only; real ANN/cache/Working Set restore tests remain NOT RUN.

Limit: no production F index/cache/Working Set restore or multi-process reconnect integration is implemented/verified.