# B-02 多角色修复协调与精确证据复核（中文）

- 审查角色：A / Integration Coordinator（协调性角色模拟，不构成独立 Owner 批准）
- 范围：H Unified 1.2.15 Gateway Attestation、CSubmitOutcome 1.0.1、C/H integrated authority-join、Storage exact-version bundle
- 基线：main `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- H 分支：`session-h-bmcp-protocol` @ `0d36324457e39bd50ad56ae902d477c4ea765b61`
- C 分支：`session-c-agent-integration-2026-11-16` @ `71047cdb51139ca4080ac67f451e38a48698859d`
- Storage 分支：`session-storage-consistency-forget-atomicity-2026-11-16` @ `830a559bd2f4ec72608f5a51e1a0b43779f2b989`
- 本报告是只读审查与跨角色修复任务分派；不得替代 H/C/I/D/Storage Owner 的权威决策。

## 1. 当前结论

**B-02 = PARTIAL / OPEN。** 本轮确认 H 已修复一个此前报告的 CI 触发缺口，但其余关键集成缺口仍未关闭。

### 已解决 / 已验证的部分

1. H 在 commit `0d36324457e39bd50ad56ae902d477c4ea765b61` 更新 `.github/workflows/h-provider-outcome-conformance.yml`，新增对：
   - H Unified 1.2.15 schema；
   - `provider_outcome_validator_1_2_15.py`；
   - `gateway_attestation_validator.py`；
   - `envelope_auth_validator.py`；
   - provider outcome conformance tests
   的路径触发。
2. 同一精确 H HEAD 上，GitHub Actions Run `44079842914`（H Provider Outcome Conformance，run 65）完成且结论为 SUCCESS；Job `134027249681` 的 setup、依赖安装、Python/Node JCS oracle 安装和 conformance test step 均成功。
3. 因此，旧审查中“1.2.15 路径未进入 H Provider Outcome workflow”的发现已关闭。该结论仅覆盖该 commit 上该工作流的执行结果，不等于生产级认证、密码学信任或端到端部署验收。
4. H 当前 1.2.15 schema Blob：`860fc4cec658db7d2703cd6adf72aa31a2723f6d`；P0 合同 Blob：`93b83ac35114d20d64579d919c0699886940f0fa`；schema mapping Blob：`2dc30f193d9c4f4bdc05ca4c137103687db28924`；gateway receiver validator Blob：`9cc426d4c26deb452f39daff34c1008dd535e969`；workflow Blob：`2ad679952ce5499a16c8fffa0a1543e26460e6eb`。

## 2. 仍然开放的 P0/P1 问题

### B02-R1 — H Issuer 侧 pre-sign 执行链缺失（P0 / H）

H 的 1.2.15 P0 合同规定 H 在签发前必须验证 CSubmitOutcome 对象、C-P0 digest/signature、序列命名空间、provider evidence 与 C 语义；接收方还必须独立重验 H Attestation 与 C 对象，之后才允许 durable ingress。

但本轮在 H 当前分支树中找到的是 receiver-side `gateway_attestation_validator.py` 和相应测试，没有找到独立的 Gateway Issuer / signing pipeline 入口或能够证明“C 校验先于 H 签名”的执行实现。接收端 validator 不能证明签发端顺序。

**H 修复要求：**
- 发布独立、不可变的 1.2.15 Issuer contract/implementation entrypoint；
- 显式顺序：严格解析 C 对象 → 精确 schema 校验 → C digest/P0/signature 验证 → C 语义与 provider evidence 验证 → I-approved H signer/profile/key-status/delegation 检查 → durable H signing sequence reservation → H P0 canonicalization/digest/signature → immutable attestation record；
- C INVALID 或 UNKNOWN 时不得签 H Attestation，不得推进 H signing sequence，不得 durable ingress；
- 将 H signing sequence reservation、签名和失败恢复的 crash/retry/duplicate 语义写清；
- 为每个阶段增加正反例测试，证明无 C-valid proof 时 signer 不会被调用；
- 明确区分 issuer 与 receiver validator，不得把 receiver revalidation 作为 issuer pre-sign proof。

### B02-R2 — 1.2.15 Integrated Authority-Join successor 缺失（P0 / H，C/I/D/Storage 交叉复审）

H 分支当前仍有 1.2.14 integrated authority-join mapping Blob `1cbe74eba69325510d6b1019d971661f965eabf8`，未发现独立 1.2.15 successor mapping。1.2.15 schema mapping `2dc30f...` 不是 integrated authority-join successor。

**H 修复要求：** 发布新 immutable mapping，至少绑定：
- H Unified 1.2.15 schema 与 CSubmitOutcome 1.0.1；
- C-P0 与 H-P0 独立签名/摘要域；
- origin transport receipt、raw-byte digest 与 C AdapterRef 身份关系；
- I terminal/authorization/key-status/revocation/anti-rollback；
- D Forget clearance、lineage/fence/currentness；
- Storage resolution、COC reservation/commit/absence 语义；
- COC evidence、replay/durable ingress、late evidence；
- issuer 与 receiver 两条独立执行路径；
- 所有 validator/test/workflow exact Blob 与 callback contract；
- INVALID / UNKNOWN / NOT_INVOKED / PROVEN_NONE 的不同语义；
- 对 1.2.14 mapping 的 supersession/coexistence 规则。

不得把 H attestation 解释为 provider truth、I authorization、D clearance 或 Storage/COC commitment。

### B02-R3 — C 对 1.2.15 integrated mapping 与 Issuer 的 exact review 缺失（P0 / C）

C Phase 3.8.17 对 H 1.2.14 integrated mapping 的审查真实存在，不能再声称 C 从未审过 integrated mapping。C Phase 3.8.26/3.8.27 分别覆盖 1.2.15 schema shape 和 corrected ordering。

但当前 C HEAD `71047cdb51139ca4080ac67f451e38a48698859d` 尚未提供对 1.2.15 integrated successor mapping、Issuer pre-sign executable chain、receiver validator 与本轮 H CI evidence 的 exact-Blob review。

**C 修复要求：** 在 H 发布 R1/R2 后，C 必须逐 Blob 审查：
- C object 仍由 C 持有语义权威；
- C P0 signature 独立且不可被 H attestation 替代；
- H 不能在 C INVALID/UNKNOWN 时签发；
- origin adapter identity、C AdapterRef 与 transport receipt 关系；
- C Provider Outcome duplicated fields 的逐字段一致性；
- INVALID/UNKNOWN 与 NOT_INVOKED/PROVEN_NONE 的边界；
- replay/late evidence 不重写 C terminal truth。
C 的接受范围必须明确标记 candidate / conditional / rejected，不得由 A 代签。

### B02-R4 — Storage exact-version manifest 尚未绑定 H 1.2.15（P1 / Storage）

Storage 当前分支的 Phase 3.6.22 manifest Blob `5c614375e10698e4931d83deb57d20321445e068` 是 v3.3.2，明确绑定 H 1.2.14 + C 1.0.1 authenticated-ingress reference bundle。该 manifest 不包含 H 1.2.15 schema、gateway validator、Issuer、1.2.15 CI run 或 C 对 1.2.15 integrated successor 的复审。

**Storage 修复要求：**
- 等待 H 1.2.15 integrated mapping、Issuer、C/I/D review 与精确测试证据稳定；
- 发布新的 immutable successor manifest（不得改写 v3.3.2）；
- 精确绑定 schema、mapping、issuer/receiver validator、测试、workflow、CI run/commit/job、C review、I/D review、COC/Storage proof；
- 对每个证据声明标记 source maturity（normative / candidate / deterministic double / CI-tested / physical / operational）；
- 明确 v3.3.2 仍是历史 1.2.14 bundle，不把它升级解释为 1.2.15 接受。

### B02-R5 — 测试与生产信任边界（P0 / H + I + C）

H receiver validator 文件头声明其为 reference integration implementation，trust、signer、origin transport、key-status、integrity evidence 和 durable replay 都是 deployment callbacks。测试中 deterministic callback doubles 不能证明真实 HSM/KMS、I registry、签名密钥保管、撤销和 anti-rollback。

**修复要求：**
- H 明确将 callback contract、生产 adapter contract、部署验收证据分开；
- I 负责签署 H profile、trust root、issuer/delegation、key lifecycle、revocation 与 anti-rollback 的权威语义；
- C 负责 C P0 profile、C key-status/trust 和 provider adapter authority；
- 不得用模拟 callback 或 schema/fixture CI 把 L3/L4/production gate 标为 PASS。

## 3. 多角色职责与完成顺序

| 角色 | 必须交付 | 不得越权 |
|---|---|---|
| H | 1.2.15 issuer path、integrated mapping successor、receiver/issuer tests、CI exact pins | 不得定义 C truth、I trust policy、D clearance 或 Storage commitment |
| C | exact review H 1.2.15 mapping/issuer/validator/CI；确认 C-P0 与 C semantic authority | 不得替 H 签 H envelope |
| I | H signer/profile/trust/delegation/key status/revocation/anti-rollback review | 不得替 H 实现 gateway，不得替 C 定义 provider truth |
| D | Forget fence、lineage、currentness、late evidence 与 clearance seam review | 不得替 I 授权或替 Storage 声明持久提交 |
| Storage | successor manifest、COC/Storage persistence/replay/recovery exact bundle | 不得合成 C/I/D Owner decision |
| A | 逐 Blob 交叉核验、记录冲突、更新集成 disposition | 不得代签 Owner 批准或把角色模拟视为独立审查 |

依赖顺序：H R1/R2 → C/I/D exact review → Storage successor manifest → A same-bundle readback。H 的 CI trigger 与本轮成功运行可以并行保留，但后续任何 validator/schema/workflow Blob 变化都必须重新 pin 并核验对应 commit 的 CI。

## 4. A 集成处置与 Gate

- H 1.2.15 workflow path + exact-head CI run：**PASS（bounded workflow execution only）**
- H 1.2.15 schema structural artifact：**CANDIDATE**
- H receiver validator：**CANDIDATE reference implementation**
- H issuer pre-sign executable proof：**OPEN / NOT PROVEN**
- H 1.2.15 integrated authority-join successor：**OPEN / NOT FOUND**
- C exact review of 1.2.15 integrated successor/issuer：**OPEN**
- I signer/trust registration：**OPEN**
- D currentness/Forget/lineage integration：**OPEN**
- Storage 1.2.15 same-bundle manifest：**OPEN**
- B-02：**PARTIAL / OPEN**
- G1–G8：本报告不宣告 PASS；不建议架构冻结。

## 5. 治理声明

本报告只作为 A 集成审查工作产物。没有修改 main、任何 Owner branch、现有 PR 或 Issue #43。所有角色模拟均不是独立人类 Owner 签署。没有合并、Gate 放行、schema/crypto freeze、实现授权、部署或生产激活。

## 6. 精确证据索引

| 项目 | Exact evidence |
|---|---|
| main | `b3c666e67982cb3d3374e759cfb6552c7765aacb` |
| H HEAD | `0d36324457e39bd50ad56ae902d477c4ea765b61` |
| C HEAD | `71047cdb51139ca4080ac67f451e38a48698859d` |
| Storage HEAD | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` |
| H 1.2.15 schema | `860fc4cec658db7d2703cd6adf72aa31a2723f6d` |
| H P0 contract | `93b83ac35114d20d64579d919c0699886940f0fa` |
| H 1.2.15 mapping | `2dc30f193d9c4f4bdc05ca4c137103687db28924` |
| H receiver validator | `9cc426d4c26deb452f39daff34c1008dd535e969` |
| H workflow | `2ad679952ce5499a16c8fffa0a1543e26460e6eb` |
| H CI run / job | `44079842914` / `134027249681` (SUCCESS) |
| H 1.2.14 integrated mapping | `1cbe74eba69325510d6b1019d971661f965eabf8` |
| C Phase 3.8.17 integrated mapping review | `36e5b97c55ebc5c01cf1b071957777225f448e64` |
| Storage v3.3.2 manifest | `5c614375e10698e4931d83deb57d20321445e068` |
| Existing A PR #64 | base `901e38ba7b45ed1822eaefddc2da8d765cf8985c`, now 4 commits behind current main; not modified |

---
End of Chinese report.
