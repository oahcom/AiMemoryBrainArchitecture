# Storage-role draft — v3.2.5 successor exact-version bundle manifest
# Storage 角色草案 — v3.2.5 后继精确版本绑定清单

- Status / 状态: **DRAFT / COORDINATOR ROLE SIMULATION / NOT STORAGE OWNER ISSUED**
- Supersedes / 拟替代: Storage v3.2.4 manifest Blob `6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7` for successor review only; does not rewrite Storage v3.2.3 normative body.
- Storage normative base remains: Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- Provenance: Session P simulated Storage role; no independent Storage Owner signature.

## 1. Purpose / 目的

This draft refreshes exact source/consumer pins after CSubmitOutcome 1.0.1 and the current H Unified 1.2.12 Blob. It is a review-routing manifest only. It does not select a database topology, approve implementation, or authorize deployment.

本草案在 CSubmitOutcome 1.0.1 与 H Unified 1.2.12 当前 Blob 更新后刷新精确源/消费方绑定。它仅用于审查路由，不选择数据库拓扑、不批准实现，也不授权部署。

## 2. Proposed exact bundle / 拟议精确绑定

| Owner | Artifact | Exact Blob | Binding role |
|---|---|---|---|
| Storage | Normative COC durable log / recovery protocol v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative Storage body; S0a–S4 and Storage visibility boundary |
| Storage | v3.2.4 predecessor manifest | `6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7` | Historical predecessor; not current successor decision |
| Storage | C Provider Outcome boundary review | `a99d9df1e14f990f0d4ccd47d48d008b9d9c01fe` | Storage/C authority join only; ACCEPT WITH ENUMERATED AMENDMENTS |
| C | Normative Provider Outcome semantic contract | `819705037da89834e10b6dd2ec6e66c1b8c70886` | C source authority for provider handoff outcome |
| C | CSubmitOutcome 1.0.1 sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | Immutable 1.0.1 source amendment |
| C | CSubmitOutcome 1.0.1 JSON Schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Exact C object schema |
| C | C Provider Outcome 1.0.1 test/vector source | `0357c7fc22c714ce50ed4ce4771510431f2b1637` / `c447f8c2908469c52cb52a448101495a331277c5` | Candidate structural/semantic/crypto fixtures only |
| H | Unified COC/JF-10/Provider schema 1.2.12 | `9aa366d857d0229687df7e44e8e70d2097a99237` | Current exact wire envelope schema; artifact 1.2.12 / wire 1.3.0 |
| H | RecoveryJoin schema 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Owner snapshot membership proof structure |
| H | C 1.0.1 exact mapping | `fad28f1b62f6a686669e209ebe30d69df6330d75` | Current mapping draft; requires refreshed H schema pin |
| H | Provider Outcome validator core | `1a92c0cf7146e2884bd38232005dd9a55d558a85` | Candidate fail-closed integration seam; callbacks not production-wired |
| H | Unified manifest union contract | `e0f561df814c1539ee3b1e72ce7cfc2fd15dd175` | Recovery union and digest semantics |
| D | D Owner snapshot membership proof | `d80dabe7210e681bc4e2290355a38f8b67be9ddd` | D owner-owned membership proof candidate |
| I | I Owner snapshot membership proof | `88209bbea0ab600880c5c630cfe83af31ee16dd7` | I owner-owned membership proof candidate |
| I | I Commit Authorization / revocation sequencer contract | `54bab0484bd232a5a258e65e34cc7425288b39a6` | Pre-commit authorization and revocation ordering |
| A | A Phase 3.8.4 integration review | `81d8956eedceb0b8842034c4ea1989e765dd6e4e` | Historical candidate review; fresh A review still required |

## 3. Authority separation / 权限分离

- C alone attests provider handoff outcome. Storage cannot create or upgrade C outcome.
- Storage alone attests StorageVisibilityOutcome and visibility pointer/receipt/outbox durability.
- H validates wire structure, dereference and exact joins; it cannot attest C/I/D/Storage ledger truth.
- I owns PermissionEpoch, key status/trust registration and authorization; D owns ForgetFence, producer/work lineage and publication participant semantics.
- C `HANDOFF_ACCEPTED` does not imply Storage `COMMITTED_VISIBLE`; Storage `COMMITTED_VISIBLE` does not prove provider acceptance.
- UNKNOWN/IN_DOUBT on either side retains the applicable participant/barrier and cannot be converted into success by COC commit.

## 4. Required owner decisions / 必须的 Owner 决议

1. C publishes a new immutable amendment that replaces C 1.0.0 references in Phase 3.8.10 for new records and explicitly binds C 1.0.1.
2. H publishes a new mapping revision pinning exact H Unified Blob `9aa366d...`, C schema Blob `a631bc7...` and RecoveryJoin Blob `4b664e3...`.
3. I confirms the C sequence namespace is included in the protected signing/key-status projection and states whether the profile remains unregistered.
4. D confirms C egress and publication remain bound to exact D participant/current FenceGeneration without transferring D authority to C/H/Storage.
5. Storage issues the actual successor manifest on its own branch and confirms the exact C/H source/consumer relationship.
6. A independently reviews this same manifest and exact Owner decisions before any interface freeze consideration.

## 5. Evidence and gate state / 证据与 Gate 状态

C 1.0.1 CI: run `44059935858`, 19 tests PASS. H Provider Outcome validator: run `44060704553`, 17 tests PASS. H Recovery Cutoff: run `44062391968`, 266 passed / 22 skipped / 0 failed. H schema validation: run `44062392943`, 47 tests PASS.

These are candidate tests only. Provider-specific Adapter behavior, real same-key provider lookup, durable C sequencer/ledger, I profile registration/key custody, H production owner callbacks, COC quorum, Storage deployment topology and end-to-end fault/race conformance remain NOT VERIFIED.

## 6. Non-claims / 非声明

This draft is not an independent Storage Owner decision, not a new normative Storage protocol, not a topology selection, not a C/H/I/D acceptance, not an A integration approval and not authorization for implementation, deployment, merge or production activation.
