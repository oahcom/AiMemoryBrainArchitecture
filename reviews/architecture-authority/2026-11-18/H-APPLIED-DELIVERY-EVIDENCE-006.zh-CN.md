# A 精确审查 — H Applied Delivery Evidence 1.0.0
# Session 4 / Review A-H-ADE-006

- 审查基线：H `6608cde89d959257db612d8ff8080f631333f3f3`；G `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8`；C `88992da30331121b81cf2773acab11d921daf281`；I `0d071bf1ee7cc71912398c6ae57e4496e08f44ab`；Main `e52594f181d2edb77448adcfed64a0fbdffaf3aa`。
- 状态：**DEFERRED — 候选实现，仍有 P0 条件未关闭**
- 范围：精确审查 H Applied Delivery Evidence 1.0.0 候选实现及其 G/C/I 消费方与安全边界。
- 独立性：由协调会话执行的 A 委派审查；不是独立人工 Owner 批准。

## 1. 执行裁决

H 已新增独立消息族 `APPLIED_DELIVERY_EVIDENCE_RECORDED` 1.0.0，没有扩展 Unified 1.2.15 的 C Provider Outcome Gateway P0。当前 H 树包含 Schema、参考 Validator、11 项测试、Workflow 和双语 Phase 3.8.24 决议。Schema 明确包含 HDeliveryBindingIdentity 的七个字段，并独立定义 HObservationRecordIdentity。

有限 CI 证据真实存在：
- H Applied Delivery Evidence Run `44130722532`：SUCCESS，11 项测试，精确测试 Commit `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`。
- H Recovery Cutoff Run `44130722851`：同一 Commit 上 SUCCESS。
- 当前 H HEAD `6608cde...` 是该测试 Commit 之后的一个纯文档提交；最后提交没有修改 Schema、Validator、Tests 或 Workflow。这属于代码树连续性证据，不是严格绑定当前 HEAD SHA 的 CI。

这些事实只支持**候选实现/符合性进展**，不证明生产密码学、已部署 Trust Registry、Durable Replay、Runtime Adapter 集成、C/G/I 接受、Crash/Restore 安全或 Full Applied 授权。

**A 裁决：DEFERRED。** H-ADE-001..003 保持 OPEN。不得据此冻结 Schema/技术、释放 Gate、合并、部署或生产激活。

## 2. 精确审查工件

| 工件 | 精确 Blob |
|---|---|
| H Schema `08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json` | `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608` |
| H Validator `08-bmcp-protocol/validators/applied_delivery_evidence_validator.py` | `2f6de24eea737cf75a16ead7495bea4627bb1bb4` |
| H Tests `08-bmcp-protocol/tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py` | `bb2bb6c94cc73293f736c6dcd450ab32bffc6ee5` |
| H Workflow `.github/workflows/h-applied-delivery-evidence-conformance.yml` | `7bd9bf3a4141d1e239d0f165e2e98fdd25961254` |
| H Phase 3.8.24 EN | `f193113f142506b0d0848c7131f780db93a83aef` |
| H Phase 3.8.24 ZH | `2c612ff11f9e3da784eeb5a9033aceb5bf01b55f` |
| G Phase 3.8.22 Applied 合同 | `bd297873bc1e593280484a43cb44b56058d9c4ff` |
| CSubmitOutcome 1.0.1 Schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` |
| C Phase 3.8.27 Gateway 顺序审查 | `3ca06dbfd7d59483e9604b7a68df924c719f60aa` |
| I Phase 3.8.23 Replay 顺序审查 | `85cdbad04ae4b688338cdf2b667c21d2f02d8b96` |

## 3. 已接受边界与证据上限

1. `HDeliveryBindingIdentity` = (adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch)。
2. `HEvidenceIdentity` = (HDeliveryBindingIdentity, evidence_kind)。
3. `HObservationRecordIdentity` = (issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence)。
4. 三者是不同身份域。H Gateway Ingress Replay Ledger、H Adapter Observation Ledger、G Applied Idempotency Ledger 必须保持分离。
5. H 独立 1.0.0 消息族正确避免原地修改 Unified 1.2.15 的 C Provider Outcome P0 Allowlist。
6. H Phase 3.8.23 对 G 身份语义作带例外接受，并明确 Wire Mapping 未冻结。C Phase 3.8.23 审查的是 C/G 身份连接，不是新 H 1.0.0 消息族的精确接受。C Phase 3.8.27 与 I Phase 3.8.23 接受的是独立 Gateway Attestation 路径的 C-before-H-signing 顺序，不能替代对新 Adapter Evidence 消息族的精确批准。
7. I 的 `AIMBA-I-CRYPTO-1.0` 只适用于 I-authored evidence，H 不得继承。H Profile 注册与 H Trust/Key Authority 仍未关闭。

## 4. 阻塞 Condition Records

### H-ADE-001 — Strict JSON Parser 未拒绝重复对象键

- **问题：** H Validator 直接调用 `json.loads(raw_envelope.decode("utf-8"))`。标准 Decoder 会在 Schema 校验与 P0 构造前静默折叠重复 JSON 对象键。
- **证据：** Validator Blob `2f6de24...`；当前 11 项测试没有重复键负向向量。
- **风险：** HIGH — 签名消息歧义与 Parser Differential。
- **阻塞：** 是，阻塞任何认证生产使用。
- **开放期间允许：** 有界候选测试与 Shadow-only 评估。
- **开放期间禁止：** 生产接受该消息族；声称已实现严格签名字节解析。
- **Owner：** H。
- **关闭标准：** 在对象物化前拒绝重复键；增加顶层与嵌套重复成员测试，覆盖身份、Digest、Signature、Authority 字段；在精确当前 HEAD 重跑 CI；发布 Parser/Test Blob Pin 与结果。
- **截止/Gate：** H Wire-Conformance Gate 通过前；同时阻塞生产 Trust/Activation。
- **验证证据：** 精确 Parser 源码、负向向量、精确 HEAD Workflow Run、独立读回。

### H-ADE-002 — CSubmitOutcome 语义 Join 未在 Validator 合同中明确

- **问题：** H Schema 携带 C Outcome 引用、Record Sequence 和 Payload Digest，但没有显式 Outcome 值。参考 Validator 仅暴露 `verify_c_final_boundary`，未定义独立 CSubmitOutcome Resolver/Verifier 合同。C Schema 1.0.1 拥有权威字段 `Outcome`、`SideEffectStatus`、`FinalRequestBoundaryRef`、`RequestDigest`、`ActualInferenceRequestId` 和不可变 Record Identity。G 要求 Full Applied 前必须有确定的成功 Provider Handoff 证据。
- **证据：** H Schema Blob `2ce8776...`；H Validator Blob `2f6de24...`；C Schema Blob `a631bc7...`；G 合同 Blob `bd29787...`。
- **风险：** HIGH — H Evidence 可能在未证明被引用的不可变 C Record 是同一最终请求的精确 `HANDOFF_ACCEPTED` / `PROVEN_OCCURRED` Outcome 时，被误当作 Applied-ready。
- **阻塞：** 是，阻塞 Full Applied 与跨 Owner Wire Freeze。
- **开放期间允许：** H 可将不透明 C Ref/Digest 作为候选证据；C 继续独占 Provider Truth。
- **开放期间禁止：** H 签发或声称 C Provider Truth；G 仅凭 H Evidence 作 Full Applied。
- **Owner：** H（Wire/Validator）、C（语义权威）、G（消费方谓词）。
- **关闭标准：** 发布精确 CSubmitOutcome 1.0.1 字段到 H 映射；定义三态 Resolver/Verifier，验证 Issuer、不可变 Record Identity/Sequence、Digest、Outcome、SideEffectStatus、Final Boundary/Request Digest/Inference Request 相等性与 Successor Lineage；取得 C/G 精确审查；增加正负 Mutation Vector。
- **截止/Gate：** C/H/G Applied 合同 Gate 或 Full Applied 启用前。
- **验证证据：** 版本固定映射、Callback 合同、测试与 C/G 精确决议。

### H-ADE-003 — Replay 结果披露前的当前授权复核未明确

- **问题：** I Phase 3.8.23 要求 SAME_DIGEST_REPLAY 在重新读取原始 Durable Result 后，重新检查当前 I Authorization/PermissionEpoch、Key Status、Audience/Scope 与适用 D Forget Fence。H Validator 在返回 `original_result_ref` 前没有显式 Current-Authorization/PermissionEpoch Callback；注入式 `commit_observation` Seam 的合同也没有明确该要求。
- **证据：** I Phase 3.8.23 Blob `85cdbad...`；H Validator Blob `2f6de24...`。
- **风险：** HIGH — 已撤销或权限过期的调用方可能获知旧 Durable Result Ref。
- **阻塞：** 是，阻塞 Replay Acceptance 与 Production Trust。
- **开放期间允许：** 不披露生产 Result Ref 的本地 Replay Callback 测试。
- **开放期间禁止：** 未经当前授权复核返回 Durable Prior-Result Ref。
- **Owner：** H 与 I；适用的 Consumer/Fence 顺序由 G/D 参与。
- **关闭标准：** 定义并实现返回任何 Replay Result Ref 前的 Current Authorization/Audience/Scope/PermissionEpoch 复核；定义正确 G Decision Boundary 上的 D Fence 复核；测试已撤销 Key/Permission、旧 Epoch、Audience/Scope 变化及 I/D 状态不可用；取得 I/H/G 精确审查。
- **截止/Gate：** I Trust/Replay Gate 与 G Applied Gate 通过前。
- **验证证据：** Callback/API 合同、Durable Replay 实现测试、负向向量、精确源码 Pin 和 Owner 决议。

## 5. 非阻塞但必须关闭的生产 Seam

- Phase 3.8.24 测试 Canonicalizer 使用排序键 JSON，并明确不是生产 H Canonicalization Profile。
- H 生产 Signature Profile、Key Registry、Issuer/Signer 注册、Trust Root、Key Custody、Revocation Precedence 与 Anti-rollback 必须由 H/I 批准；不得继承 I Profile。
- Durable Observation Replay Storage、Crash-safe Reservation/Commit、同 Digest 原始结果读取、变更 Digest 冲突处理与 Retention 尚未由参考 Validator 实现。
- Runtime Adapter 集成、Capability Epoch 签发、真实 Transport Identity、跨语言向量、SDK 生成、Crash/Restore 与多副本线性化尚未证明。
- G Applied Persistence 与 D Forget Fence 仍由各自 Owner 掌权；H Evidence 本身不能提交 G Applied。

## 6. 必需后续顺序

1. H 通过 Strict Parsing 与精确 HEAD CI 关闭 H-ADE-001。
2. H/C/G 联合关闭 H-ADE-002：精确 C Outcome 语义与 Request-Boundary Mapping。
3. H/I/G/D 联合关闭 H-ADE-003：Replay Authorization/Fence 复核顺序与测试。
4. H/I 发布 H 自有生产 Profile/Registry 决议与独立向量；不得继承 I Profile。
5. H/G/Storage 提供 Durable Replay 与 Crash/Restore 证据；G 仍独占 Applied 权威。
6. A 在 Owner 当前 HEAD 重新读取所有精确工件并作出新裁决。在此之前总体架构仍为 DEFERRED / ARCHITECTURE_NOT_READY。

## 7. A 最终裁决

**DEFERRED — 候选实现已有有限 CI 成功；H-ADE-001、H-ADE-002、H-ADE-003 仍 OPEN，并分别阻塞其对应受保护路径。** 本审查不授予架构冻结、Schema Freeze、Full Applied Activation、Gate Release、合并或生产授权。
