---
document_metadata:
  domain: ai-development
  role: decision-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Owner acting as owner proxy"
      decision_date: "2026-11-23"
      approved_version:
        scheme: content-hash
        value: "31c2240efa3db8d89a9c46d208548c64b3594d16640ca4191f53307b3bb654d8"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "Owner ruling, round 15, 2026-11-23 — placement, metadata and merge decisions for this document"
        - "Owner ruling, round 12, recovered verbatim from chatgpt-session-ops account acct6 reply reply-6b02c810-234212.md, line 44"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "The normative text is the round-12 owner ruling recovered byte-for-byte from the session archive; no wording was retranslated or normalised. The provenance rule exists because GOV-NC-2026-11-20-MERGE-AFTER-RULING-003 s13.1 and s13.4 recorded a comment creation time as a review submission time, and because a merge time on PR #825 was reported as 13:31:23Z when that value is the comment time and the merge time is 13:24:15Z."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Canonical
    canonical_scope: "Event timestamp provenance across governance, audit, incident and merge-history records"
    canonical_scope_id: ai-development/event-timestamp-provenance
    canonical_scope_keywords:
      - timestamp-provenance
      - event-type
      - merge-time
      - comment-time
      - review-submission-time
    canonical_conflict_status: None
    normative_status: Normative
---

# OWNER-DECISION-EVENT-TIMESTAMP-PROVENANCE-001 — Event Timestamp Provenance

**DECIDED — 2026-11-23, Owner acting as owner proxy.**

### Event Timestamp Provenance / 事件时间戳溯源

**English**

Every material event timestamp recorded in a governance, audit, incident, or merge-history document MUST be traceable to an authoritative source for that specific event. The record MUST identify:

1. the event being asserted, distinguishing, where applicable, merge time, commit time, review-submission time, comment-creation time, and other distinct event types;
2. the authoritative source system and resource identifier, such as the repository and pull-request number, review ID, comment ID, or commit SHA;
3. the exact API endpoint or authoritative record location and the field from which the timestamp was read;
4. the timestamp value as returned by the source, including its timezone or UTC designation.

A timestamp for one event MUST NOT be used as evidence of a different event. In particular, a comment creation time MUST NOT be represented as a pull-request merge time, and a review submission time MUST NOT be represented as the time at which a merge occurred.

When a timestamp is corrected, the document MUST preserve the distinction between the previously recorded value and the verified value, identify the source supporting the correction, and avoid implying that the earlier value was independently verified.

If the authoritative source or event type cannot be established, the timestamp MUST be marked unverified or omitted; it MUST NOT be inferred from nearby comments, commit ordering, display order, or approximate chronology.

**中文**

治理、审计、事件或合并历史文档中记录的每个重大事件时间戳 MUST 能够追溯到该事件本身的权威来源。记录 MUST 标明：

1. 所声明的事件类型；适用时，必须区分合并时间、提交时间、审查提交时间、评论创建时间及其他不同事件；
2. 权威来源系统及资源标识，例如仓库与 PR 编号、Review ID、评论 ID 或 commit SHA；
3. 读取时间戳所依据的精确 API 端点或权威记录位置，以及对应字段；
4. 来源返回的原始时间戳值，包括其时区或 UTC 标识。

某一事件的时间戳 MUST NOT 被用作另一事件的证据。尤其是，评论创建时间 MUST NOT 被表述为 PR 合并时间，审查提交时间 MUST NOT 被表述为实际发生合并的时间。

修正时间戳时，文档 MUST 保留此前记录值与核实后值之间的区别，标明支持修正的来源，并且不得暗示此前记录值已经过独立核实。

若无法确定权威来源或事件类型，则该时间戳 MUST 标记为未经核实或予以省略；MUST NOT 根据相邻评论、提交顺序、页面显示顺序或大致时间线推断。

### 对这次事件的具体适用

| 事实 | 应取字段 | 不能替代它的字段 |
|---|---|---|
| PR 合并时间 | `GET /repos/{owner}/{repo}/pulls/{number}` → `merged_at` | 评论 `created_at` |
| Issue/PR 评论创建时间 | 对应评论记录 → `created_at` | PR `merged_at` |
| 正式 Review 提交时间 | Review 记录 → `submitted_at` | 普通评论 `created_at` |
| Commit 时间 | Commit 记录 → `commit.committer.date` 或 `commit.author.date`，并注明使用哪一个 | PR 合并时间 |

这条规范不要求把每个时间戳写成冗长的 API 调用日志；可以在同一事实表的来源列或集中证据表中登记，但必须能从每个时间戳反查到具体来源字段。

**最终边界：** 时间戳溯源规则应作为独立规范变更提出，不要混进新文件准入 gate 的代码 PR。
