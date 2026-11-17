# Governance Decision — NR-001
# 治理决议 — NR-001

- Decision ID: AID-2026-001-GOV-NR-001
- Work Item: AID-2026-001
- Related PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42
- Decision date: 2026-11-17
- Decision authority: Project governance authority (explicit decision supplied by the project sponsor/governance authority in the ChatGPT conversation and recorded in PR discussion)
- Decision: **OPTION A — ACCEPTED**
- Scope: Interpretation of AI-STD-001 §3.2 for this repository's ChatGPT-native execution model.

## English — Binding decision

A genuinely separate, newly started ChatGPT conversation satisfies the requirement for a “separate AI session/agent” under AI-STD-001 §3.2, provided all controls below are met:

1. The reviewer starts a new ChatGPT conversation with a clean, separate conversation context.
2. The reviewer did not author, edit, implement, or otherwise participate in the implementation under review.
3. The reviewer independently retrieves and examines the exact PR Head SHA, base SHA, full diff, frozen prompt, authoritative source contracts, Work Item manifest, and available verification evidence from GitHub.
4. The review report identifies the exact Head SHA, inspected artifacts, checks actually performed, checks not run, findings, residual risks, and disposition.
5. The reviewer explicitly discloses that the separation is **conversation/context isolation only**. It does not establish model independence, provider independence, runtime/environment independence, or statistical independence, and must not be represented as multi-model consensus.
6. All existing R3 controls remain mandatory. In particular, R3 work still requires independent security/domain specialist review and reproducible test evidence before acceptance. This decision does not waive, downgrade, combine away, or replace specialist review.
7. Integration review, acceptance authority, risk acceptance, and merge authorization remain separate gates. The implementer and integration coordinator cannot self-approve or infer acceptance from this decision.

This decision resolves NR-001 only. It does not approve AI-ARCH-002, approve the current PR, establish that the current Head has passed independent review, mark CI/YAML/schema/manifest checks as passed, or authorize merge/deployment.

## 中文 — 具有约束力的决议

真正独立、全新启动的 ChatGPT 对话，在满足以下全部控制条件时，满足 AI-STD-001 §3.2 对“独立 AI 会话/Agent”的要求：

1. Reviewer 必须新建 ChatGPT 对话，并使用干净、独立的对话上下文。
2. Reviewer 不得编写、修改、实现或以其他方式参与被审查的实现工作。
3. Reviewer 必须从 GitHub 独立读取并检查准确的 PR Head SHA、Base SHA、完整 Diff、冻结提示词、权威源契约、Work Item Manifest 和现有验证证据。
4. 审查报告必须标明准确 Head SHA、检查过的工件、实际执行的检查、未执行的检查、发现项、残余风险和审查结论。
5. Reviewer 必须明确披露：这种隔离**仅代表对话/上下文隔离**，不构成模型独立、服务商独立、运行环境独立或统计意义上的独立，也不得描述为多模型共识。
6. 所有既有 R3 控制要求继续强制有效。尤其是 R3 工作在验收前仍须接受独立安全/领域专业审查，并提供可复现的测试证据。本决议不豁免、不降低、不合并取消或替代专业审查。
7. 集成审查、验收授权、风险接受和合并授权仍是彼此独立的门禁。实现者和集成协调者不得自行批准，也不得从本决议推断项目已验收。

本决议仅解决 NR-001。不代表批准 AI-ARCH-002、不代表批准当前 PR、不代表当前 Head 已通过独立审查、不代表 CI/YAML/Schema/Manifest 检查通过，也不授权合并或部署。

## Audit trail / 审计记录

- Decision request: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42#issuecomment-6945859120
- Decision supplied: “NR-001: OPTION A” with explicit scope and limitations.
- Effective status: NR-001 = RESOLVED_BY_GOVERNANCE_DECISION; implementation/review/acceptance gates remain independently pending as applicable.
