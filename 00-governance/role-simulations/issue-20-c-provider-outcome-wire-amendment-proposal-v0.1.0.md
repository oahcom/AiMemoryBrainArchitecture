# C-role proposal — Provider Outcome wire amendment for CSubmitOutcome 1.0.1
# C 角色提案 — CSubmitOutcome 1.0.1 Provider Outcome Wire 修订

- Status / 状态: **PROPOSED / COORDINATOR ROLE SIMULATION / NOT C OWNER ACCEPTANCE**
- Supersedes / 拟替代: C Phase 3.8.10's 1.0.0 object mapping for new records only; historical 1.0.0 remains immutable.
- Exact C source: C semantic contract Blob `819705037da89834e10b6dd2ec6e66c1b8c70886`; C 1.0.1 amendment Blob `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb`; schema Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`.
- Exact H candidate consumer: Unified 1.2.12 Blob `9aa366d857d0229687df7e44e8e70d2097a99237`; RecoveryJoin 1.0.2 Blob `4b664e3bce465499bcdfd93796349a4ba7074002`.
- Provenance: Session P simulated C role; no independent C Owner signature.

## 1. Proposed decision / 拟议决议

Adopt CSubmitOutcome **1.0.1** as the immutable C object for new `C_PROVIDER_OUTCOME_RECORDED` events when carried in BMCP Unified 1.2.12. C 1.0.0 remains historical and must never be silently interpreted as 1.0.1.

新 `C_PROVIDER_OUTCOME_RECORDED` 事件使用不可变 CSubmitOutcome **1.0.1** 对象，并由 BMCP Unified 1.2.12 承载。C 1.0.0 保留为历史版本，禁止静默按 1.0.1 解释。

## 2. Exact binding set / 精确绑定集合

| Item | Exact Blob |
|---|---|
| C normative Provider Outcome semantics | `819705037da89834e10b6dd2ec6e66c1b8c70886` |
| C 1.0.1 sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` |
| C 1.0.1 JSON Schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` |
| C 1.0.1 fixture pack | `c447f8c2908469c52cb52a448101495a331277c5` |
| H Unified 1.2.12 schema | `9aa366d857d0229687df7e44e8e70d2097a99237` |
| H RecoveryJoin 1.0.2 schema | `4b664e3bce465499bcdfd93796349a4ba7074002` |

## 3. Required object and wire rules / 对象与 Wire 规则

1. CSubmitOutcome 1.0.1 is the immutable C source of truth. It requires `sequence_namespace_ref` and binds `record_sequence` to the same durable C sequencer namespace used by CKeyStatusEvent.
2. H envelope `c_submit_outcome_ref` dereferences the exact C object. H recomputes the canonical payload digest, validates exact schema ID/version/artifact revision, and checks the C signature/key-status state.
3. Every duplicated BMCP field must equal the C object exactly. Missing, null and absent are not interchangeable. An object member that is non-null cannot be omitted from the corresponding wire projection.
4. External COC, I, D and Storage proofs remain independently issued; they are not copied into C's signed P0 object or synthesized by H.
5. Provider outcomes remain `HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT`. UNKNOWN/IN_DOUBT preserve the same immutable attempt, request digest and provider idempotency key; they do not authorize retry-as-new-operation.
6. The C transport-owning Adapter must serialize gate admission/close and the physical handoff through one durable C authority. A process-local lock, SDK retry or missing ACK is not a proof of no invocation.
7. RecoveryJoin 1.0.2 carries C owner-snapshot membership proof structure; it does not transfer C completeness, signing or provider-outcome authority to H.

## 4. Required C/H amendment / 必须的 C/H 修订

- C must publish a new immutable wire amendment replacing the 1.0.0 references in Phase 3.8.10 for new records and explicitly binding C 1.0.1 + H Unified 1.2.12 Blob `9aa366d...` + RecoveryJoin 1.0.2 Blob `4b664e3...`.
- H must publish a matching immutable mapping revision pinning the same exact source set.
- The Storage successor manifest must bind both C source and H consumer artifacts independently to avoid a cyclic source/consumer reference.
- I must confirm that the sequence namespace is covered by the registered signing profile before any VALID result. The profile remains NOT REGISTERED.

## 5. Non-claims / 非声明

This proposal does not certify a provider adapter, provider idempotency/lookup semantics, production C sequencer, C owner ledger, COC quorum, I trust root, H production verifier, Storage transaction topology, exactly-once side effects, production readiness or architecture freeze.

本提案不认证 Provider Adapter、Provider 幂等/查询语义、生产 C Sequencer/Ledger、COC Quorum、I Trust Root、H 生产验证器、Storage 事务拓扑、Exactly-once 副作用、生产就绪或架构冻结。
