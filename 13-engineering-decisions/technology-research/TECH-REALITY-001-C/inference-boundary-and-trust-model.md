# Inference Boundary and Trust Model / 推理边界与信任模型

## 1. Core rule / 核心规则
Generated content is a model output, not a verified fact. Provider acceptance is not inference completion; inference completion is not output validity; tool execution is not canonical commit. B defines epistemic distinctions; C defines integration evidence; D/E decide canonical lifecycle and derived-memory production.

生成内容是模型输出，不是已验证事实。Provider 接受请求不等于推理完成；推理完成不等于输出有效；工具执行不等于规范提交。B 定义认识论区别；C 定义集成证据；D/E 决定规范生命周期与派生记忆生产。

## 2. Distinct stages / 不可合并阶段
1. Input captured / received.
2. InferenceRequest frozen with immutable identity and request digest.
3. Provider handoff attempted and outcome recorded.
4. Provider execution start/completion observed, if supported.
5. Output received; stream may be partial.
6. Output parsed against declared format/schema.
7. Output validated against domain and safety constraints.
8. ToolCallProposal emitted by model.
9. Tool authorization evaluated by I; tool executes under its own execution identity.
10. Tool result observed and evidence/provenance attached.
11. Candidate Memory submitted to Brain.
12. D accepts/rejects/commits under canonical lifecycle; E handles derived assets.
13. G Applied is a separate context-inclusion predicate, not a consequence of model response.

## 3. Trust dimensions / 信任维度
Trust is not truth, epistemic status, confidence, evidence strength, or authorization. Track separate attributes:
- origin/authentication: who/what emitted the data and how verified;
- integrity: whether bytes/semantic projection match a digest/signature;
- provenance: source and derivation lineage;
- validation: which independent rules/checkers ran and their result;
- epistemic status: B's Observed/Reported/Inferred/Verified/Disputed/Retracted;
- authorization: I's decision for actor/action/resource/scope/policy epoch.

Trust does not automatically transfer from a Provider to model output or from a Tool to the factual interpretation of its result. Model self-critique or self-rating is not independent validation. Provider signatures can attest origin/integrity of a Provider statement only within the registered trust profile; they do not attest real-world truth.

## 4. Trust elevation / 信任提升
- No automatic monotonic trust ladder.
- A verifier may add a new validation event with method, verifier identity, source references, time and scope; it does not erase prior provenance.
- Only an I-approved trust authority may establish issuer/key trust. C's key lifecycle proposal says C data keys do not self-authorize and the I governance profile is NOT REGISTERED.
- Independent corroboration requires independent source lineage; duplicated copies of one model response are not independent evidence.
- Revocation, source correction or key compromise creates a new status/reconciliation event; consumers re-check current validity before use.
- Canonical Domain Evidence exists only when accepted under B/D/E rules; C cannot declare it.

## 5. Candidate-to-memory boundary / 候选记忆边界
Possible direct candidates: explicit user statements with source identity and scope; authenticated external records; observed tool results with verifiable execution identity; validated structured extraction linked to source evidence. In all cases, candidate submission is not Canonical Memory Applied.
Require independent validation for high-impact, disputed, external-world, financial, safety, identity, or destructive-action claims. Inferred summaries must retain source lineage and be marked Inferred unless a declared verification procedure succeeds. Untrusted model output may be transient context only; it must not become instruction authority.

可能直接成为候选的信息包括带来源和 Scope 的用户明确陈述、认证外部记录、可验证执行身份的工具观察结果、关联源证据的结构化提取。但候选提交不等于规范记忆已应用。高影响、争议、外部世界、财务、安全、身份或破坏性操作主张必须独立验证。推断摘要必须保留来源链，并保持 Inferred，除非声明的验证程序成功。未受信模型输出只能作为临时 Context，不能成为指令权威。

## 6. Conflict handling / 冲突处理
Conflicting model outputs create competing Claims/Evidence, not majority-vote truth. Preserve model/provider/version, prompt/request digest where retention permits, independent sources, event_time and recorded_at. B owns Claim semantics and conflict interpretation; E owns derived-memory pipeline; D owns lifecycle. C only preserves invocation and output provenance.

相互冲突的模型输出形成相互竞争的 Claim/Evidence，而不是多数投票事实。保留模型/Provider/版本、允许保留时的 Prompt/Request Digest、独立来源、event_time 和 recorded_at。B 负责 Claim 语义和冲突解释；E 负责派生记忆流水线；D 负责生命周期。C 只保存调用与输出来源证据。


## 完整中文版本

模型生成内容不是已验证事实。Provider 接受请求不等于推理完成；推理完成不等于输出有效；Tool 执行不等于 Canonical Commit。B 拥有认识论语义，C 负责集成证据，D/E 负责规范生命周期和派生记忆生产。

输入接收、InferenceRequest 冻结、Provider Handoff、Provider 执行开始/完成、响应接收、流完整性、解析、结构验证、领域验证、Tool Call Proposal、Tool 授权、Tool Execution、结果观察、候选 Memory 提交、D 接受/提交，以及 G Applied 必须分别记录。不得压缩为一个 success 状态。

信任不是事实、认识论状态、置信度、证据强度或授权。必须分别记录来源认证、完整性、Provenance、验证结果、B 的 Epistemic Status 和 I 的授权决定。Provider 签名只能在已注册的信任配置范围内证明来源/完整性，不能证明现实世界真伪。模型自我评价不是独立验证。

信任提升必须产生新的验证事件，记录方法、验证者、来源、时间和 Scope，不得抹除历史。I 批准的信任权威才能建立 Issuer/Key 信任。多个相同模型输出的副本不构成独立佐证。密钥撤销、来源更正或证据失效必须触发新的状态/对账事件。

带来源的用户明确陈述、认证外部记录、可验证工具观察结果、关联源证据的结构化提取，可以成为候选输入，但不等于 Canonical Memory Applied。高影响、争议、外部世界、财务、安全、身份和破坏性操作主张必须独立验证。模型推断摘要应保留来源链并保持 Inferred，除非经过声明的验证程序。

模型输出冲突应保留为竞争 Claim/Evidence，不采用简单多数投票决定事实。记录模型/Provider/版本、请求摘要、独立来源、Event Time 和 Recorded At。B 解释 Claim 冲突，E 管理派生流程，D 管理生命周期；C 不得越权裁决事实。
