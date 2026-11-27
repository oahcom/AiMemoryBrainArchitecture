---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-241/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "All numeric measurements in this record are observations from the current working tree; no CI result, merge, or post-merge state is claimed."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-241 — Evidence and declared exceptions

## 1. 基线与测量边界

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base commit: `788fbc011877a14976fc0a974ffe2e013dd9991b`
- Branch HEAD reported for this work tree: `ce3d7cb8`.
- `check_source_revision_pointers.py`:
  - POINTERS=50
  - ACCURATE=16
  - STALE=8
  - DEREFERENCED=26
  - BAD_DEREFERENCE=0
  - NON_BLOB_REFERENCE=6
  - BAD=14
  - exit=1
- The pointer checker remains unwired. Its 14 BAD results remain registered debt.
- These figures describe the supplied working-tree measurements only. They do not assert CI success, merge, or post-merge verification.

## 2. RC-1 — M-02 文案对齐

修改 `scripts/check_document_management.py` 中 M-02 的两段描述，使其只声明实际执行的检查：

- `decision_status` 枚举值；
- `decision_status` 为 `Approved` 时的 `approved_version` 与 `approval_scope` 绑定；
- DM-10 正文哈希绑定。

文案明确说明：校验不要求 `approver` 或 `decision_date` 存在，也不验证任何批准是否实际发生。

未修改 `MANUAL_CONTROLS` 元组结构、判定逻辑或 policy 第 9.2 节生成机制。

## 3. RC-2 — Security Governance README

英文与中文 README 的状态描述统一为五份文档各自 frontmatter 声明的 `canonical_status: Canonical`。

每份文档自己的 frontmatter 是其 `canonical_status` 的唯一权威来源；README 仅为导读，不是规范来源。

免责声明保留：这些文档的存在不代表 Phase 3.x 决策获批，不代表生产策略获批，也不构成实现或符合性证据；中文说明同时明确不代表 Owner 已批准或生产实现已符合。

中文 README 中原有的英文 Candidate / Informative 段落已以语义一致的中文表述替换。

## 4. Source revision pointer debt

### 4.1 STALE — 8 条

涉及以下四组 EN/ZH 镜像：

- `docs/en/00-governance/design-principles.md:56`
- `docs/zh-CN/00-governance/design-principles.md:56`
- `docs/en/01-system-architecture/responsibility-matrix.md:37`
- `docs/zh-CN/01-system-architecture/responsibility-matrix.md:37`
- `docs/en/01-system-architecture/system-architecture-specification.md:6`
- `docs/zh-CN/01-system-architecture/system-architecture-specification.md:6`
- `docs/en/01-system-architecture/system-boundaries.md:37`
- `docs/zh-CN/01-system-architecture/system-boundaries.md:37`

裁决：不将 declared revision 直接替换为当前根文件 blob。

STALE 在本情形下表示镜像内容未随根文件更新。直接将指针改为当前根文件 blob，会制造镜像已对应当前根版本的虚假 provenance 声明。

不将镜像自动降级为 stub；现有证据不足以证明这种降级符合其实际内容和用途。

处置：保持指针脚本原有失败语义，保持 workflow 不接线，登记为 8 条未解决债务。禁止为获得绿色结果而将 declared revision 改为 actual revision。

### 4.2 NON_BLOB_REFERENCE — 6 条

涉及以下文件：

- `docs/en/01-system-architecture/forget-fence-and-completion-contract.md:52`
- `docs/zh-CN/01-system-architecture/forget-fence-and-completion-contract.md:52`
- `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md:53`
- `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md:53`
- `docs/en/03-memory-brain/memory-brain-guide.md:6`
- `docs/zh-CN/03-memory-brain/memory-brain-guide.md:6`

这六条使用描述性散文，而不是可解析的 blob revision。

特别说明：`4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` 是源正文 blob，不是规范根文件 blob。二者不得混同。

裁决：本工作项不猜测、不构造根文件 blob，不将源正文 blob 冒充根文件 blob。六条作为未解决债务登记。只有取得对应根文件的真实 blob 身份并确认指针语义后，才允许修改这些值。

### 4.3 门禁接线裁决

本工作项不修改 `scripts/check_source_revision_pointers.py`，不增加基线豁免，不修改任何 workflow，也不新增 required context。

14 条 BAD 不得通过以下方式消除：

- 放宽脚本判定；
- 将未经验证的译文声明为与当前根同步；
- 将源正文 blob 冒充规范根文件 blob；
- 将散文转换成猜测的 SHA；
- 将未解决的债务标记为准确。

脚本仍保持严格失败语义，workflow 仍保持不接线状态。14 条作为明确登记的未解决债务保留。

## 5. AID-2026-113 — Verified 覆盖范围收窄

保留 `verification_status: Verified`，不修改 Correction 段首句。

将 `last_verification_note` 的 Verified 覆盖范围限定为既有源文件与镜像身份列、Owner 替换裁决及有界语言对应关系观察。

两张表中的 new-blob identity columns 明确排除在 Verified 覆盖范围之外。`NEW_BLOB_IDENTITIES_NOT_VERIFIABLE` 结论继续有效，不得将其解释为新 Blob 身份已经验证。

该处理保留原作者关于 Correction 未修改原有声明的陈述，同时明确区分已验证内容和不可验证的新 Blob 身份列。

## 6. 本轮变更范围

本轮已报告的工作树变更包括：

- `scripts/check_document_management.py`：M-02 两条字符串。
- `docs/en/09-security-governance/README.md`：状态及权威来源说明。
- `docs/zh-CN/09-security-governance/README.md`：状态及权威来源说明。
- `05-memory-runtime/README.md`：增加导读内容。
- `docs/en/05-memory-runtime/README.md`：增加对应英文导读。
- `docs/zh-CN/05-memory-runtime/README.md`：增加对应中文导读。
- `14-ai-development/work-items/AID-2026-113/restore-evidence.md`：收窄验证说明。
- `docs/en/14-ai-development/work-items/AID-2026-113/restore-evidence.md`：收窄验证说明。
- `docs/zh-CN/14-ai-development/work-items/AID-2026-113/restore-evidence.md`：收窄验证说明。

上述文件清单和数字来自所提供的工作树测量，不构成对 CI、PR 合并或主分支状态的声明。
