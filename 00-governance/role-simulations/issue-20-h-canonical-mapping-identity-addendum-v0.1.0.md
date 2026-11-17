# H-role simulation — canonical mapping identity and supersession addendum
# H 角色模拟 — Canonical Mapping 身份与替代关系补充

- Status: **P COORDINATOR SIMULATION / NOT H OWNER BRANCH PUBLICATION**
- Canonical current mapping candidate: `phase-3.8.10-h-c-provider-outcome-unified-1.2.14-exact-mapping.md`, Blob `579dd2a91edf47b86e744e897ba6668b839944bd`.
- Duplicate predecessor mapping: `phase-3.8.10-h-unified-1.2.14-c-submit-outcome-1.0.1-authority-join-mapping.md`, Blob `1cbe74eba69325510d6b1019d971661f965eabf8`.

## Decision / 决议

Treat Blob `579dd...` as the sole canonical H 1.2.14 / CSubmitOutcome 1.0.1 Authority-Join Mapping for successor bundle reviews. Preserve Blob `1cbe...` as immutable historical evidence, but mark its path as superseded and prohibit new manifest/review pins to it.

The two documents have the same core mapping/authority semantics and exact H validator core, but different test and CI pins:
- canonical: test `70a379...`, run `44068869146`, 27/27;
- predecessor: test `53774...`, run `44068247661`, 25/25.

No file is deleted or rewritten by this P simulation. H Owner must publish the supersession notice or merge the canonical mapping into one unambiguous path. Storage, I, D and A must bind the canonical Blob and its exact CI/test set.

This identity addendum does not establish a complete unmocked H envelope/C object validation path, production I/D/Storage callbacks, production trust or physical Storage deployment.
