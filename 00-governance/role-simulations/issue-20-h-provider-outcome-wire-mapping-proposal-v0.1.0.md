# H-role proposal — BMCP 1.2.12 to CSubmitOutcome 1.0.1 exact mapping
# H 角色提案 — BMCP 1.2.12 到 CSubmitOutcome 1.0.1 精确映射

- Status / 状态: **PROPOSED / COORDINATOR ROLE SIMULATION / NOT H OWNER ACCEPTANCE**
- Exact H schema candidate: Unified 1.2.12 Blob `9aa366d857d0229687df7e44e8e70d2097a99237`; RecoveryJoin 1.0.2 Blob `4b664e3bce465499bcdfd93796349a4ba7074002`.
- Exact C object: CSubmitOutcome 1.0.1 Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`; C sequence namespace amendment Blob `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb`.
- Existing H validator core: Blob `1a92c0cf7146e2884bd38232005dd9a55d558a85`.
- Provenance: Session P simulated H role; no independent H Owner signature.

## 1. Version tuple / 版本元组

| Dimension | Required value | Meaning |
|---|---|---|
| BMCP schema artifact revision | `1.2.12` | Selects exact Unified schema artifact |
| BMCP wire-family version | `1.3.0` | Protocol family version |
| C object schema version | `1.0.1` | Immutable CSubmitOutcome object revision |
| RecoveryJoin artifact | `1.0.2` | Membership proof carrier artifact |

H must authenticate/select the artifact revision independently from the wire-family version. RecoveryJoin's `$id`/artifact label is 1.0.2 while `schema_version` is const 1.0.0; H must explicitly document whether the latter is the stable message-family version and where the artifact revision is authenticated. Do not silently change the const.

H 必须区分 Schema Artifact Revision 与 Wire Family Version。RecoveryJoin 的 `$id`/Artifact 标识为 1.0.2，而 `schema_version` 常量为 1.0.0；H 必须明确后者是否是稳定消息族版本，以及 Artifact Revision 在何处被认证。禁止未经兼容性审查直接修改常量。

## 2. Immutable C object dereference / C 不可变对象解引用

H must dereference `c_submit_outcome_ref`, validate the exact CSubmitOutcome 1.0.1 schema, recompute the canonical digest, and verify the C owner signature and current key status. C's `sequence_namespace_ref` must equal the authenticated C key-status event namespace and the authoritative C signing sequencer namespace. An unavailable sequencer/key-status ledger/checkpoint is UNKNOWN, not VALID.

H 必须解引用 `c_submit_outcome_ref`，验证精确 CSubmitOutcome 1.0.1 Schema、重算 Canonical Digest，并验证 C Owner Signature 与当前 Key Status。C 的 `sequence_namespace_ref` 必须与认证后的 C Key Status Event Namespace 及 C 权威签名 Sequencer Namespace 相等。Sequencer/Key Status Ledger/Checkpoint 不可用时返回 UNKNOWN，不得返回 VALID。

## 3. Duplicate wire-field equality / 重复 Wire 字段一致性

For every C field duplicated in BMCP, compare exact typed value and nullability:
- outcome, provider, adapter, idempotency key, request digest and final request boundary;
- C outcome ref/digest and owner signature ref;
- C admission ref/digest and C owner ledger ref/version/local sequence/high-water/root;
- provider request/receipt/lookup/no-handoff/not-invoked/unknown evidence refs when applicable;
- COC participant intent/reservation pair or explicit absence reason.

The C object remains authoritative. BMCP envelope fields are projections, not alternate provider truth. Independent COC/I/D/Storage references must be validated by their own owner callbacks.

## 4. Tri-state semantics / 三态语义

- **VALID:** exact schema/digest/signature/key status and all required C/COC/I/D/Storage owner callbacks return valid current evidence.
- **INVALID:** proven malformed structure, digest/signature mismatch, tuple substitution, stale generation or contradictory terminal evidence.
- **UNKNOWN:** missing/unavailable authority callback, owner ledger, key-status chain, anti-rollback checkpoint, C object or provider evidence.

Missing callback is never success. H schema validity alone never proves provider handoff truth, C ledger completeness or Storage visibility.

## 5. Currentness and required H action / 当前性与 H 行动

The current H mapping document Blob `fad28f1b62f6a686669e209ebe30d69df6330d75` maps C object 1.0.1 but still pins the old H Unified schema Blob `a54f669...`. H must publish a new immutable mapping revision pinning current H schema Blob `9aa366d...`, current C object Blob `a631bc7...`, C sequence amendment Blob `6fa67af...` and RecoveryJoin 1.0.2 Blob `4b664e3...`. The validator core's constants and schema registry must be read back against the same set.

## 6. Evidence boundary / 证据边界

H Provider Outcome validator run `44060704553` passed 17 tests on exact validator/test blobs `1a92c0c...` / `a90b5c4...`, which remain unchanged at the observed H head. H Recovery Cutoff run `44062391968` passed 266, skipped 22 and failed 0; H schema run `44062392943` passed 47. These are candidate reference/structural suites. Production owner callbacks, production key registry, COC quorum and live C provider adapter are not connected.

H Provider Outcome 验证器 17 项测试、H Recovery Cutoff 266 项通过/22 项跳过，以及 H Schema 47 项测试均属于候选参考/结构测试。生产 Owner Callback、生产 Key Registry、COC Quorum 与真实 C Provider Adapter 尚未接通。

## 7. Non-claims / 非声明

No independent H approval, production signature verification, I profile registration, provider truth, production readiness or wire freeze is claimed.
