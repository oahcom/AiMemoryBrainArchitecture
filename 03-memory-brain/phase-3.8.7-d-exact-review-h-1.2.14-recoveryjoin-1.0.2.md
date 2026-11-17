# Phase 3.8.7 — D Exact Review of H Unified 1.2.14 and RecoveryJoin 1.0.2 D Fence High-Water
# Phase 3.8.7 — D 对 H Unified 1.2.14 / RecoveryJoin 1.0.2 D Fence High-Water 的精确审查

- Owner: D — Memory Brain / ForgetFence Authority
- Branch: `session-d-memory-brain-2026-11-16`
- Exact H Unified schema 1.2.14: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- Exact H RecoveryJoin schema 1.0.2: Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- D membership proof contract: Blob `d80dabe7210e681bc4e2290355a38f8b67be9ddd`
- D RecoveryJoin P0 crosswalk (refreshed exact pin): Blob `c4adf827dd62d44c43b8e871dec4835581508adf`
- D ForgetFence contract: Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`
- D Gate Release currentness contract: Blob `7f2861d9441b9be6c8e69f41fd0276636be483a8`
- Decision: **ACCEPT AS D-OWNED L1/L2 SCHEMA/CROSSWALK CANDIDATE; L3 AND OWNER AUTHORITY GATES OPEN**
- Provenance: delegated D-role review; not an independent human D Owner signature.
- English and Chinese are normative peers.

## 1. Exact schema decision / 精确 Schema 决议

D accepts the corrected H Unified 1.2.14 schema Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59` and RecoveryJoin 1.0.2 Blob `4b664e3bce465499bcdfd93796349a4ba7074002` as the current candidate carriers for D owner-specific high-waters and generic owner membership proofs.

The schema description correction from the prior 1.2.14 Blob is metadata-only. The required `schema_artifact_revision=1.2.14`, wire version 1.3.0 and D high-water semantics are unchanged.

D 接受修正后的 H Unified 1.2.14 与 RecoveryJoin 1.0.2 作为 D Owner-Specific High-Water 和通用 Owner Membership Proof 的当前候选载体。此前 1.2.14 Schema Description 的修正仅是元数据；必需的 `schema_artifact_revision=1.2.14`、Wire 1.3.0 和 D High-Water 语义未改变。

## 2. Exact D high-water vector / 精确 D High-Water 向量

H Unified 1.2.14 `ownerSpecificHighWatersD` MUST contain exactly:
- `producer_registration_high_water`;
- `work_item_high_water`;
- `attempt_high_water`;
- `barrier_generation`;
- `barrier_root`;
- `forget_fence_generation_high_water`.

The last field is mandatory and is a distinct D-local monotonic namespace. It is not:
- `owner_gate_generation`;
- `barrier_generation`;
- ProducerRegistrationSequence;
- WorkItem/Attempt high-water;
- I PermissionEpoch;
- C record/event sequence;
- COC term/index;
- Storage transaction sequence.

最后一个字段是强制 D-local 单调命名空间，不能替代或被 Gate Generation、Barrier Generation、ProducerRegistrationSequence、WorkItem/Attempt High-Water、I PermissionEpoch、C Sequence、COC Term/Index 或 Storage Transaction Sequence 替代。

## 3. Exact no-loss join / 精确无损 Join

D confirms the Phase 3.8.6 crosswalk Blob `c4adf827dd62d44c43b8e871dec4835581508adf` preserves the closed generic RecoveryJoin 1.0.2 proof envelope:
- D proof P0 contains the exact generic owner fields and typed D authority/ledger/entry/admission/snapshot/attestation/gate/scope/operation/request/key/profile references;
- D-only ForgetFenceGeneration, lineage and barrier semantics remain committed by the exact D canonical row/ForgetOperation digest and the signed D owner snapshot/attestation;
- the H Unified 1.2.14 D high-water summary is derived from the same signed D snapshot and bound by the owner-specific high-water digest;
- RecoveryJoin 1.0.2 membership proof binds the exact owner snapshot ref/digest and attestation ref/digest;
- no D-only property is appended to the closed generic RecoveryJoin membership-proof object.

The D high-water summary is not inferred from the RecoveryJoin request/admission counts. The signed snapshot/attestation and exact owner proof are the authority. H checks the exact summary digest and typed joins; D alone checks ledger completeness and fence semantics.

D 确认 Phase 3.8.6 Crosswalk 保留 RecoveryJoin 1.0.2 封闭通用 Proof Envelope。D 专属 ForgetFenceGeneration、Lineage 和 Barrier 语义由精确 D Canonical Row/ForgetOperation Digest 与签名 D Owner Snapshot/Attestation 承诺；H 1.2.14 D High-Water Summary 来自同一签名 D Snapshot，并由 Owner-Specific High-Water Digest 绑定；RecoveryJoin Membership Proof 绑定精确 Snapshot/Attestation Ref/Digest；不得向封闭通用 Proof 对象追加 D-only 字段。

D High-Water Summary 不能从 RecoveryJoin Request/Admission Count 推断。权威来自签名 Snapshot/Attestation 和精确 Owner Proof。H 校验 Summary Digest 与 Typed Join；D 独自校验 Ledger Completeness 和 Fence 语义。

## 4. Required D invariants / 必需 D 不变量

1. Every included D fence row has `ForgetFenceGeneration <= forget_fence_generation_high_water` within the same D sequence namespace.
2. Any late-discovered pre-fence producer/work/attempt/derivative row invalidates the old snapshot and reopens the affected barrier.
3. A stale/lower high-water, changed barrier root, missing pagination, missing anti-rollback checkpoint or mismatched attestation yields UNKNOWN/INVALID and cannot release D Gate.
4. `owner_gate_generation`, `barrier_generation` and `forget_fence_generation_high_water` are three distinct typed values.
5. The owner snapshot attestation and owner-specific high-water digest bind the exact same captured D snapshot; no independently sampled high-water vector is accepted.
6. D proof membership and D snapshot completeness are separate: every represented row needs membership; the snapshot also needs complete authoritative enumeration, pagination, count, ordered root and anti-rollback.

## 5. L3 reference obligations / L3 参考义务

- mutate only `forget_fence_generation_high_water` while keeping the owner snapshot digest → reject;
- fence row generation greater than captured high-water → reject;
- replace fence high-water with gate/barrier generation → reject;
- high-water namespace mismatch with D owner sequence → reject;
- late producer discovered after snapshot → old snapshot invalid, new round required;
- pagination incomplete or anti-rollback unavailable → UNKNOWN;
- RecoveryJoin proof ref points to another snapshot/attestation → reject;
- missing D owner row in canonical union → reject.

## 6. Final D disposition / D 最终结论

**ACCEPT AS D-OWNED L1/L2 SCHEMA/CROSSWALK CANDIDATE; L3 AND OWNER AUTHORITY GATES OPEN.**

D accepts the exact H 1.2.14 + RecoveryJoin 1.0.2 carrier/crosswalk for the ForgetFenceGeneration high-water. This does not prove real D ledger completeness, producer inventory, runtime Gate Release, key registry, physical Storage integration or production Forget completion.

**接受为 D 自有 L1/L2 Schema/Crosswalk 候选；L3 与 Owner Authority Gate 仍 OPEN。** 不证明真实 D Ledger 完整性、Producer Inventory、Runtime Gate Release、Key Registry、物理 Storage 集成或生产 Forget 完成。
