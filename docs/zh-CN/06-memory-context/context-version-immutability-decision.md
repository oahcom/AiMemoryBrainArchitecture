---
document_metadata:
  domain: memory-context
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Owner-delegated direction decision, 2026-11-26"
        - "Work Item AID-2026-087"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Direction decision recorded; exact-version Owner acceptance and normative approval pending."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "memory-context decision contract"
    canonical_scope_id: "memory-context/decision-084"
    canonical_scope_keywords:
      - architecture-decision
      - memory-context
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "06-memory-context/context-version-immutability-decision.md
---
# ContextVersion 不可变性决议
决议 ID：CV-IMM-01
授权人：user-authorized operator (delegated by account owner)
日期：2026-11-26
Owner：G；依赖边界为 B、D、I、C/H 与 Storage/Consistency
关联 Issue：#1144、#1151
状态：方向已裁定；精确版本 Owner 验收及规范批准仍待完成。

## 决议与不可变边界
已提交的 ContextVersion 是一个不可变、内容寻址的快照，表示完整的期望托管 Context 状态。提交后，不得原地修改任何用于标识、描述或改变该快照语义的字段。

不可变字段包括：Context ID、Context Session ID、不可变 Version ID、单调递增序号、parent/base Version 引用、完整有序的 ContextEntryVersion 集合、每个 Entry 的身份/Revision/内容摘要/限定条件/状态/交付相关元数据、规范序列化配置及版本、snapshot reference 和 digest、提交身份/时间、来源 Revision 引用及适用的 ForgetFence cursor 引用。

可变状态必须位于版本对象之外：current-head 指针；delivery attempt、receipt、retry、Applied 证据及运行健康状态；可重建索引、缓存和投影。它们均不得重写或重新解释已提交版本。

## 合法变更路径
1. 任何内容或成员关系变化都必须创建新的 ChangeSet 和后继 ContextVersion。
2. ChangeSet 必须指定精确 expected base。提交时原子检查该 base 仍为当前版本，持久化新的不可变快照并推进 head；过期 base 必须冲突。
3. 更正、替换、移除、策略变化或 Forget 失效必须创建带明确来源/原因的后继版本，不得编辑前驱。
4. 相同幂等 key 和相同请求 digest 重放原始 receipt/version；相同 key 但 digest 不同必须冲突。
5. Delivery、Applied、过期、拒绝、Superseded 和重试属于追加式外部证据记录。
6. 可信提交边界必须基于精确规范有序的已提交 Entry 计算 snapshot digest。调用方提供的 digest 仅供参考，必须重新计算并比较。读取/重放时验证 snapshot reference 与 digest 指向同一份不可变字节。

## 违规行为
原地修改已提交字段/Entry 顺序/内容/来源引用；将同一 Version ID/序号复用于不同内容；未提交后继版本或未验证 expected-base 就推进 head；接受不匹配的调用方 digest；在 Version 内记录 delivery/Applied/Forget 状态；以不同字节重放相同 Version 身份。

## Reviewer PASS/FAIL
- CVI-01 PASS：已提交 ContextVersion 及 Entry 快照不可变；否则 FAIL。
- CVI-02 PASS：Context/session/version/序号/parent/有序 Entry/交付相关元数据均在不可变边界内；否则 FAIL。
- CVI-03 PASS：head 只能通过追加式后继 ChangeSet 和精确 expected-base/CAS 推进；否则 FAIL。
- CVI-04 PASS：更正/移除/Forget 创建后继版本，不编辑前驱；否则 FAIL。
- CVI-05 PASS：delivery attempt/receipt/Applied/投影均位于 ContextVersion 之外；否则 FAIL。
- CVI-06 PASS：digest 绑定精确有序 Entry，并在读取/重放时验证；否则 FAIL。
- CVI-07 PASS：同 key 同 digest 重放；同 key 不同 digest 冲突；否则 FAIL。
- CVI-08 PASS：EN 与 ZH-CN 的边界和合法路径语义一致；否则 FAIL。

## 权威边界
G 拥有 ContextVersion 语义和精确版本验收。B 拥有被引用领域对象的身份/Revision；D/I 拥有 Forget 权威/策略；C/H 拥有交付和推理边界证据；Storage 拥有物理原子性/持久性/恢复。此决议不选择存储拓扑、摘要算法、Wire 编码或超出语义不变量的实现细节。#1144 和 #1151 在各自证据及 Owner 验收完成前保持 OPEN。不修改产品/Runtime 代码、测试、Schema、Validator、Workflow、部署或生产状态。
