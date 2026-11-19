# Repository Policy Inheritance Declaration

- Declaration ID: GOV-DOC-001-REPOSITORY-INHERITANCE
- Policy ID: GOV-DOC-001
- Version: 1.2
- Status: DRAFT — TEMPLATE ONLY

## 1. Repository identity

- Repository Name:
- Repository URL:
- Repository Type: DEVELOPMENT / SUBREPOSITORY / SUPPORTING
- Parent Repository:
- Accountable Owner:
- Formal Governance Inclusion Reference:
- Inclusion Decision Date:

## 2. Policy inheritance state

This declaration does not itself establish approval or inheritance.

本声明本身不构成批准或继承关系的成立。

The inheritance state MUST be exactly one of:

- PENDING: Evidence is incomplete. The four evidence fields below MUST explicitly contain NOT_RECORDED.
- INHERITED: The repository has an approved, traceable policy reference. The source commit and policy blob SHA MUST be supplied and independently reproducible.
- NOT_APPLICABLE: A documented governance decision establishes that inheritance does not apply. This state does not waive other applicable governance requirements.

继承状态必须且只能为以下三种之一：

- PENDING：证据不完整。以下四个证据字段必须明确填写 NOT_RECORDED。
- INHERITED：仓库具有经批准且可追溯的规范引用；源提交和规范 Blob SHA 必须提供并可独立复算。
- NOT_APPLICABLE：有记录的治理决定确认不适用。此状态不豁免其他适用治理要求。

### Machine-readable declaration

The following block is the sole canonical format. Preserve field names and one-field-per-line syntax.

以下代码块是唯一规范格式。必须保留字段名及每行一个字段的格式。

POLICY-INHERITANCE-DECLARATION
- Policy ID: GOV-DOC-001
- Inherited Version: NOT_RECORDED
- Authoritative Repository: NOT_RECORDED
- Approved Source Commit: NOT_RECORDED
- Policy Blob SHA: NOT_RECORDED
- Inheritance State: PENDING
===END

Do not change PENDING to INHERITED merely by completing this template. INHERITED requires a formally approved adoption reference and a reproducible policy blob SHA. The SHA must identify the actual policy file blob at the approved source commit, not the commit object itself.

不得仅凭填写模板把状态改为 INHERITED。INHERITED 必须伴随正式批准的纳管引用及可复算的规范 Blob SHA。该 SHA 必须指向批准源提交中的实际规范文件 Blob，而非 Commit 对象本身。

## 3. Bilingual enforcement scope

EN:

This repository MUST enforce bilingual requirements for:

1. Architecture documents.
2. Umbrella Requirements.
3. Newly created Issues.
4. Newly created Commit Messages.
5. Pull Request titles and bodies.
6. Local governance and migration records.

中文：

本仓库 MUST 对以下内容执行双语要求：

1. 架构文档。
2. Umbrella Requirement。
3. 新建 Issue。
4. 新建 Commit Message。
5. Pull Request 标题和正文。
6. 本地治理和迁移记录。

## 4. Required repository templates

- Issue template path:
- Umbrella Requirement template path:
- Commit Message guidance path:
- PR template path:
- Architecture documentation entry:
- Migration register path:

All templates MUST link to the authoritative GOV-DOC-001 source.

所有模板 MUST 链接至权威 GOV-DOC-001 来源。

## 5. Historical migration

EN:

The repository MUST inventory historical single-language records and track migration debt. Historical commits MUST NOT be rewritten.

中文：

本仓库 MUST 清点历史单语记录并跟踪迁移技术债。历史 Commit MUST NOT 被重写。

- Historical Issue inventory:
- Historical Commit inventory:
- Historical PR inventory:
- Migration Work Item:
- Migration Register:

## 6. Exceptions and authority

No local team or AI agent may unilaterally weaken or waive GOV-DOC-001.

任何本地团队或 AI Agent 均不得单方面削弱或豁免 GOV-DOC-001。

- Authorized exception reference:
- Decision authority:
- Expiry:
- Evidence:

If none exists, use NOT_RECORDED.

如不存在，使用 NOT_RECORDED。

## 7. Approval record

- Repository governance authority:
- Approval status:
- Approval date:
- Exact approval reference:
- Effective date:

The existence of this declaration does not itself establish approval.

本声明存在本身不构成正式批准。

## 8. Governance acknowledgement

EN:

GOV-DOC-001 is inherited governance, not an optional style guide. Changes to the inherited policy remain subject to the central governance authority.

中文：

GOV-DOC-001 属于继承的治理规范，而非可选写作指南。对继承规范的修改仍须遵循中央治理机构的权限和审批流程。
