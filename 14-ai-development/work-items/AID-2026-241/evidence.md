# AID-2026-241 — Evidence and declared exceptions

## 1. 基线

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base commit: `788fbc011877a14976fc0a974ffe2e013dd9991b`
- `check_source_revision_pointers.py` baseline:
  - POINTERS=50
  - ACCURATE=16
  - STALE=8
  - DEREFERENCED=26
  - BAD_DEREFERENCE=0
  - NON_BLOB_REFERENCE=6
  - BAD=14
  - exit=1
- The pointer checker is not connected to any workflow.
- No checker relaxation or workflow integration is authorized by this work item.

## 2. RC-1 — M-02 文案修正

修正文案，使其仅声明实际校验的内容：

- `decision_status` 枚举；
- `Approved` 状态下的 `approved_version` 和 `approval_scope` 绑定；
- DM-10 正文哈希绑定。

明确声明不要求 `approver` 或 `decision_date` 存在，也不验证任何批准是否真实存在。

未修改判定逻辑及 policy 第 9.2 节生成机制。

## 3. RC-2 — Security Governance README

README 改为与五份文档的 `canonical_status: Canonical` frontmatter 一致。

各文档自身 frontmatter 是其状态的唯一权威来源。README 仅作导读，不构成规范来源。

保留不批准 Phase 3.x 决策、不批准生产策略、不构成实现或符合性证据的免责声明。

## 4. Source revision pointer debt

### 4.1 STALE — 8 条

以下四组 EN/ZH 镜像指针仍有 8 条 STALE：

- `docs/en/00-governance/design-principles.md:56`
- `docs/zh-CN/00-governance/design-principles.md:56`
- `docs/en/01-system-architecture/responsibility-matrix.md:37`
- `docs/zh-CN/01-system-architecture/responsibility-matrix.md:37`
- `docs/en/01-system-architecture/system-architecture-specification.md:6`
- `docs/zh-CN/01-system-architecture/system-architecture-specification.md:6`
- `docs/en/01-system-architecture/system-boundaries.md:37`
- `docs/zh-CN/01-system-architecture/system-boundaries.md:37`

裁决：不将 declared revision 直接替换为当前根文件 blob。

原因：镜像正文未随根文件更新。直接更新指针会将尚未验证的镜像错误声明为对应当前根版本，制造虚假的同步证据。

不将镜像自动降级为 stub，因为这不能证明其正文已被正确处理。

处置：保持指针门禁不接入 workflow，将这 8 条登记为待解决债务。不得放宽脚本判定。

### 4.2 NON_BLOB_REFERENCE — 6 条

以下 6 条使用散文而非可解析的 blob revision：

- `docs/en/01-system-architecture/forget-fence-and-completion-contract.md:52`
- `docs/zh-CN/01-system-architecture/forget-fence-and-completion-contract.md:52`
- `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md:53`
- `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md:53`
- `docs/en/03-memory-brain/memory-brain-guide.md:6`
- `docs/zh-CN/03-memory-brain/memory-brain-guide.md:6`

裁决：本次不猜测、不构造根文件 blob，不将源正文 blob 冒充根文件 blob。

特别说明：`4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` 是源正文 blob，不等于规范根文件 blob。

处置：保持指针门禁不接入 workflow，将 6 条登记为待解决债务。后续只有取得对应文件的真实 blob 身份并确认指针语义后，才能替换为可解析值。

### 4.3 门禁接线裁决

当前 14 条 BAD 不得通过以下方式消除：

- 放宽 `check_source_revision_pointers.py`；
- 将未经验证的译文声明为与当前根同步；
- 将源正文 blob 冒充根文件 blob；
- 将散文转换成猜测的 commit SHA；
- 将尚未解决的债务标记为准确。

保持脚本原有失败语义，保持 workflow 不接线，并将 14 条作为明确登记的债务。

## 5. AID-2026-113

待执行方核对 `restore-evidence.md`、英文镜像和中文镜像的完整 frontmatter 与 Correction 原文。

裁决原则：

- 不得保留与现有证据相矛盾的 `verification_status: Verified`。
- 若降级为 `Unverified`，必须同步修正 Correction 中声称该字段保持原样的文字。
- 不得仅将 Correction 提升为 frontmatter 注释来掩盖验证状态冲突。
- 三份文件必须保持语义一致。
- `NEW_BLOB_IDENTITIES_NOT_VERIFIABLE` 必须如实保留，不能改写为验证通过。

本项具体字节替换待取得三份文件完整原文后执行。
