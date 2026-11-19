# Bilingual Commit Message Standard / 双语 Commit Message 规范

- Policy Reference: GOV-DOC-001
- Template Version: 1.0
- Status: DRAFT

## 1. Subject format / Subject 格式

Required recommended format:

<type>(<scope>): <English summary> / <中文摘要>

Examples of types:

- feat
- fix
- docs
- test
- refactor
- perf
- build
- ci
- chore

Scope MUST be a concise stable technical scope.

scope MUST NOT be translated if it is a canonical technical identifier.

## 2. Body format / Body 格式

EN:
- Context:
- Changes:
- Rationale:
- Verification:
- Limitations:

中文：
- 背景：
- 修改：
- 原因：
- 验证：
- 限制：

Substantive Body content MUST be provided in both languages.

实质性 Body 内容 MUST 同时提供中英文。

## 3. Footer format / Footer 格式

Preserve canonical machine-readable metadata.

Examples:

Refs: #262
Work-Item: GOV-DOC-001-V1.2-REMEDIATION
Policy: GOV-DOC-001
BREAKING CHANGE: <English explanation> / <中文说明>

Do not translate stable identifiers or machine-consumed tokens.

不得翻译稳定标识或机器消费的 Token。

## 4. Complete example / 完整范例

docs(governance): expand bilingual governance baseline / 扩展双语治理基线

EN:
- Extend GOV-DOC-001 to cover Issues, Umbrella Requirements, Commit Messages, and Pull Requests.
- Define inheritance requirements for future governed repositories.
- Establish historical migration tracking without rewriting historical commits.
- Preserve the existing normative status of v1.1 until v1.2 is formally approved.

中文：
- 扩展 GOV-DOC-001，使其覆盖 Issue、Umbrella Requirement、Commit Message 和 Pull Request。
- 定义未来治理仓库的规范继承要求。
- 建立历史迁移跟踪机制，不重写历史 Commit。
- 在 v1.2 正式批准前保留 v1.1 的现有规范效力。

Refs: #262 #263 #264 #265 #266
Work-Item: GOV-DOC-001-V1.2-REMEDIATION
Policy: GOV-DOC-001

## 5. Historical commits / 历史 Commit

Historical Commit Messages MUST NOT be rewritten solely to comply with this policy.

历史 Commit Message MUST NOT 仅为了满足本规范而重写。

Historical single-language commits are registered as MIGRATION_DEBT unless a formally authorized EXEMPTION exists.

历史单语 Commit 应登记为 MIGRATION_DEBT，除非存在正式授权的 EXEMPTION。
