---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# Owner D / Owner I Forget Authority Matrix
# Owner D / Owner I Forget 权责矩阵

- Work Item: AID-2026-001
- Status: PROPOSED clarification; not an approval of implementation or runtime behavior
- Applies to: normative contracts joining Canonical Forget lifecycle semantics and security/governance controls

## 1. Governing distinction / 核心区分

**D owns domain semantics and lifecycle truth. I owns security/governance policy and the criteria by which cross-system evidence may be accepted.**

D determines what a Canonical Forget operation means, its canonical state machine, domain-level completeness, and the meaning of each domain result. I determines who may request/authorize it, applicable privacy/retention/legal-hold policy, mandatory security controls, required evidence classes, and the governance conditions under which a cross-system result may be represented as policy-compliant.

I's governance completion criteria MUST NOT redefine D's canonical lifecycle states or claim that a domain operation is complete when D's canonical conditions are unmet. D MUST NOT declare a cross-system governance outcome compliant, waive retention/legal-hold rules, or weaken I's evidence requirements.

**D 负责领域语义与生命周期事实；I 负责安全/治理策略，以及跨系统证据可被接受的条件。**

D 决定 Canonical Forget Operation 的含义、规范状态机、领域层完整性以及各领域结果的含义。I 决定谁可以请求/授权、适用的隐私/保留/Legal Hold 策略、强制安全控制、必需证据类别，以及跨系统结果可被认定为符合治理策略的条件。

I 的治理完成条件不得重定义 D 的规范生命周期状态，也不得在 D 的规范条件尚未满足时声称领域操作已完成。D 不得自行声明跨系统治理结果合规、豁免 Retention/Legal Hold 规则或削弱 I 的证据要求。

## 2. Responsibility matrix / 职责矩阵

| Concern | Owner D — accountable | Owner I — accountable | Required joint evidence |
|---|---|---|---|
| Canonical ForgetOperation schema and identity | Define canonical domain contract | Define security constraints on authenticated requester/authorizer | Approved field/authority mapping |
| Canonical lifecycle states and transitions | Define and own | Review security implications; no unilateral state changes | State-transition contract |
| Domain-level completion meaning | Define what D's operation completion means | Must not redefine it | D-owned completion predicate and tests |
| Forget fence / generation semantics | Define canonical semantics and domain enforcement contract | Define security requirements for trustworthy observation and revocation | Fence contract and race/replay tests |
| Requester authentication | Consume authenticated principal contract | Own trust policy and authentication requirements | Principal binding and negative tests |
| Authorization to request/approve | Enforce agreed decision contract at D boundary | Own policy, delegation, approval and revocation semantics | Authorization matrix and deny tests |
| Scope / tenant isolation | Enforce domain boundary | Define security policy and required dimensions | Cross-scope isolation tests |
| Privacy, retention, legal hold | Implement applicable constraints at D boundary | Own policy and exception authority | Policy decision and auditable exception evidence |
| Target inventory | Define D-owned target/dependency inventory interface and completeness of D's inventory | Define cross-system inventory policy and required coverage | Per-target inventory with owner and capability |
| Cleanup / erasure semantics | Define D-owned domain effects and truthful state | Define security/governance obligations and evidence requirements | Per-target results and provenance |
| Cross-system completion evaluation | Supply canonical D state and domain evidence; cannot claim other owners' completion | Own governance evaluation against policy and evidence criteria; cannot rewrite D state | Evidence vector, unresolved/unknown targets, explicit exceptions |
| Legal/policy exception | Cannot grant or waive | Own approval under applicable governance authority | Signed/attributed decision and scope |
| Audit evidence requirements | Emit D-owned event/evidence fields | Define integrity, provenance, retention and access requirements | Verifiable audit record |
| Recovery / retry / idempotency | Own canonical lifecycle behavior and idempotency semantics | Define authorization re-check and audit constraints | Fault-injection and replay tests |

## 3. Completion vocabulary / 完成状态术语

- **D-domain completion**: the Canonical ForgetOperation has satisfied D's normative lifecycle predicate. Only D defines this predicate.
- **Cross-system evidence evaluation**: I evaluates whether all required target classes have sufficient evidence under the approved governance policy. This does not mutate D's canonical state.
- **Governance-compliant outcome**: a policy-level conclusion based on the evidence vector, unresolved targets, retention/legal-hold decisions and authorized exceptions.
- **Physical erasure**: a target-specific claim requiring evidence from the system/operator that controls the relevant storage or copy. Neither D nor I may infer it from a logical tombstone or an unqualified ACK.

- **D 领域完成**：Canonical ForgetOperation 满足 D 的规范生命周期判定条件。该判定条件只能由 D 定义。
- **跨系统证据评估**：I 根据已批准的治理策略，评估所有必需目标类别是否具备充分证据。该评估不得修改 D 的规范状态。
- **治理合规结果**：基于证据向量、未解决目标、保留/Legal Hold 决策和经授权例外作出的策略层结论。
- **物理擦除**：必须由控制相关存储或副本的系统/运营方提供目标级证据。D 或 I 均不得仅凭逻辑 Tombstone 或不具备充分证明力的 ACK 推断物理擦除完成。

## 4. Non-negotiable boundary rules / 不可违反的边界规则

1. Neither D nor I may unilaterally publish a joined D/I contract as normative without explicit agreement from both.
2. I may reject a governance outcome for insufficient evidence or policy violation, but may not rewrite D's canonical lifecycle state.
3. D may report its domain operation state, but may not represent unverified external targets as completed.
4. UNKNOWN, FAILED, UNSUPPORTED and NOT_EVIDENCED remain distinct and cannot be silently coerced to success.
5. An exception requires an identified authority, scope, rationale, expiry/review condition and audit evidence.
6. Any unresolved authority conflict blocks READY/ACCEPTED status for the joined contract.

1. 未经 D/I 双方明确同意，任何一方均不得单方面将 D/I 联合契约发布为规范性内容。
2. I 可以因证据不足或违反策略而拒绝治理合规结论，但不得改写 D 的规范生命周期状态。
3. D 可以报告自身领域操作状态，但不得将未经验证的外部目标表示为已完成。
4. UNKNOWN、FAILED、UNSUPPORTED 和 NOT_EVIDENCED 必须保持区分，不得静默转换为成功。
5. 任何例外都必须记录授权主体、适用范围、理由、到期/复核条件和审计证据。
6. 任何未解决的权责冲突都会阻止联合契约进入 READY/ACCEPTED 状态。

## 5. Required validation / 必需验证

- D lifecycle transition, completion-predicate and idempotency tests.
- Authorization-before-mutation and authorization-revocation tests.
- Cross-tenant / cross-scope denial tests.
- Retention and legal-hold conflict/exception tests.
- Per-target inventory completeness and unknown-target handling tests.
- Partial failure, retry, replay and recovery tests.
- Evidence provenance and physical-erasure claim-boundary tests.

- D 生命周期迁移、完成判定条件和幂等性测试。
- 修改前授权以及授权撤销测试。
- 跨 Tenant / 跨 Scope 拒绝测试。
- Retention 与 Legal Hold 冲突/例外测试。
- 逐目标清单完整性及未知目标处理测试。
- 部分失败、重试、重放和恢复测试。
- 证据来源完整性及物理擦除声明边界测试。

## 6. Approval status / 批准状态

This matrix is a proposed clarification for review. It is NOT evidence that Owners D and I have approved it, that implementation conforms, that tests have run, or that R3 has passed.

本矩阵是待审查的澄清提案。它不代表 D/I 已批准、不代表实现符合要求、不代表测试已执行，也不代表 R3 已通过。
