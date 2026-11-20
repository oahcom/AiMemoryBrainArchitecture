# Architecture Document Management Policy / 架构文档管理条例

- Policy ID: GOV-DOC-002
- Version: 1.0
- Status: **NORMATIVE — MACHINE-CHECKED**
- Owner: A — Principal Integration / Architecture Governance
- Relation to GOV-DOC-001: **SUPPLEMENTARY — does not weaken, replace or waive GOV-DOC-001**
- Enforced by: `scripts/check_document_management.py`, `.github/workflows/document-management.yml`
- Metadata schema: `00-governance/architecture-document-metadata.schema.yaml`

## 1. Policy statement / 规范声明

GOV-DOC-001 governs **how a document is written** (bilingual parity). This policy governs **what a document is** (its classification and lifecycle) and **how the repository stays consistent** with that classification.

GOV-DOC-001 管辖**文档怎么写**（双语一致性）。本规范管辖**文档是什么**（分类与生命周期），以及**仓库如何与该分类保持一致**。

Where this policy and GOV-DOC-001 differ, GOV-DOC-001 prevails. This policy adds no exemption from any existing requirement.

本规范与 GOV-DOC-001 冲突时，以 GOV-DOC-001 为准。本规范不豁免任何既有要求。

## 2. Scope / 适用范围

Applies to every Markdown file under the normative roots declared in `scripts/check_bilingual_docs.py` (`NORMATIVE_ROOTS`), excluding `PAIR_EXEMPT_PREFIXES` and generated outputs.

适用于 `scripts/check_bilingual_docs.py` 中 `NORMATIVE_ROOTS` 声明的所有 Markdown 文件，排除 `PAIR_EXEMPT_PREFIXES` 与生成产物。

Out of scope: source code, machine-generated schema dumps, raw test logs, images. Their architectural meaning MUST be documented in an in-scope document.

不适用：源代码、机器生成的 Schema 转储、原始测试日志、图片。其架构含义 MUST 在适用范围内的文档中说明。

## 3. The four-dimension model / 四维模型

Classification is **declared in metadata**, never inferred from directory location or filename.

分类**在元数据中声明**，绝不从目录位置或文件名推断。

| Dimension | Question it answers | Allowed values | Maintainer |
|---|---|---|---|
| `domain` | Which technical concern? | See §3.1 | Human |
| `role` | What job does the document do? | `design-specification`, `decision-record`, `normative-standard`, `research`, `review-report`, `work-record`, `guide`, `reference`, `index` | Human |
| `lifecycle` | Is it approved, used, replaced, archived? | See §4 | Human + CI |
| `authority` | Does it bind, and is it unique? | See §5 | Human + CI |

### 3.1 Domain enumeration / Domain 枚举

The 12 technical concerns. This list is closed; adding a value requires a governance decision recorded as a `decision-record` role document.

12 个技术关注领域。该列表封闭；新增取值需形成一条 `decision-record` 职责文档所记录的治理决议。

```
architecture, domain-model, memory-brain, memory-compiler, memory-runtime,
memory-context, agent-integration, protocol, security-governance,
storage-index, consistency-recovery, testing-acceptance, ai-development
```

### 3.2 Independence constraint / 独立性约束

No dimension may be derived from another. CI MUST NOT infer `usage_status` from `decision_status`, or `canonical_status` from `role`.

任何维度不得由另一维度推导。CI 禁止从 `decision_status` 推导 `usage_status`，也禁止从 `role` 推导 `canonical_status`。

All of the following are legal combinations / 以下组合均合法：

| decision_status | usage_status | canonical_status | Meaning |
|---|---|---|---|
| Approved | Active | Canonical | Normal binding authority |
| Approved | Deprecated | Canonical | Still authoritative, no longer recommended |
| Approved | Superseded | Non-Canonical | Replaced by a newer document |
| Revoked | Archived | Non-Canonical | Withdrawn and retired |
| Draft | Active | Candidate | Under consideration, not binding |

## 4. Lifecycle / 生命周期

Lifecycle has four **independent** sub-states. They never collapse into one field.

生命周期含四个**相互独立**的子状态，不得合并为单一字段。

### 4.1 Approval decision / 审批决议

`decision_status` ∈ {`Draft`, `Under-Review`, `Approved`, `Rejected`, `Withdrawn`, `Revoked`}

Approval MUST bind to a version, not to the document in general / 审批 MUST 绑定到版本，而非文档整体：

```yaml
approval:
  decision_status: Approved
  approver: Architecture Board
  decision_date: "2026-03-15"
  approved_version:
    scheme: git        # git | content-hash
    value: "abc123def" # 审批时的 commit 或内容哈希
  approval_scope:
    type: Full-document  # Full-document | Selected-sections | Selected-assets
    included_sections: []
    included_assets: []
  evidence_reference: []
  revocation: null
```

**Rule L1 — stale approval / 失效审批**: if content within `approval_scope` changes after `approved_version`, `modification_status` MUST become `Pending-Reapproval`, and `approval_applicability` MUST become `Not-Applicable-To-Current-Version`. The historical `Approved` record is preserved and MUST NOT be rewritten.

**规则 L1 — 失效审批**：若 `approval_scope` 范围内内容在 `approved_version` 之后发生变化，`modification_status` MUST 变为 `Pending-Reapproval`，`approval_applicability` MUST 变为 `Not-Applicable-To-Current-Version`。历史 `Approved` 记录必须保留，禁止改写。

**Rule L2 — revocation evidence / 撤销证据**: `decision_status: Revoked` REQUIRES a non-null `revocation` block containing a unique `revocation_decision_id`.

**规则 L2 — 撤销证据**：`decision_status: Revoked` 必须提供非空 `revocation` 块，且含唯一 `revocation_decision_id`。

```yaml
revocation:
  revocation_decision_id: "GOV-REV-2026-004"   # unique, never reused
  revoked_date: "2026-10-01"
  revoker: Security Team
  revocation_reason: "Security vulnerability discovered"
  revocation_evidence: []
  superseding_document: null
```

### 4.2 Evidence verification / 证据核验

Separate from approval. A document can be approved and its evidence unreachable.

与审批分离。文档可以已批准，而其证据不可达。

`verification_status` ∈ {`Unverified`, `Verified`, `Invalidated`}

`Invalidated` (evidence proven wrong) MUST NOT be conflated with `Unreachable` (temporarily inaccessible); the latter is recorded in `last_verification_note` while `verification_status` stays `Unverified`.

`Invalidated`（证据被证伪）禁止与 `Unreachable`（暂时不可访问）混用；后者记录在 `last_verification_note` 中，`verification_status` 保持 `Unverified`。

`evidence_verification` is maintained by CI; humans supply the references. CI MUST NOT change `decision_status`.

`evidence_verification` 由 CI 维护，人类提供引用。CI 禁止修改 `decision_status`。

### 4.3 Usage / 使用状态

`usage_status` ∈ {`Active`, `Deprecated`, `Archived`, `Superseded`}

`Archived` REQUIREs `archival.archived_date` and `archival.archival_reason` / `Archived` 必须提供 `archival.archived_date` 与 `archival.archival_reason`。

### 4.4 Supersession / 替代关系

**Single-direction declaration.** The new document declares `supersedes`. `superseded_by` is **CI-derived**, never hand-edited. `superseded_by` MUST NOT be written back into the source Markdown; it lives only in the generated index.

**单向声明**。新文档声明 `supersedes`。`superseded_by` 由 **CI 衍生**，禁止人工编辑，且禁止回写到源 Markdown，仅存于生成索引。

```yaml
supersession:
  supersedes: ["docs/en/02-domain-model/entity-model-v1.md"]
  supersession_reason: "Superseded by revised entity model"
  effective_date: "2026-06-01"
```

## 5. Authority / 权威性

Two **independent** attributes. Neither implies the other.

两个**相互独立**的属性，互不蕴含。

### 5.1 Canonical status / 唯一权威

`canonical_status` ∈ {`Canonical`, `Non-Canonical`, `Candidate`}

`Canonical` REQUIRES a non-empty `canonical_scope` and `canonical_scope_keywords`, and a normalized `canonical_scope_id`.

`Canonical` 必须提供非空 `canonical_scope`、`canonical_scope_keywords`，以及规范化的 `canonical_scope_id`。

**Rule A1 — scope conflict / 范围冲突**: at most ONE `Canonical` document per `canonical_scope_id`. On conflict, all conflicting documents MUST set `canonical_conflict_status: Under-Review`.

**规则 A1 — 范围冲突**：每个 `canonical_scope_id` 最多允许一份 `Canonical` 文档。发生冲突时，所有冲突文档 MUST 设置 `canonical_conflict_status: Under-Review`。

**Rule A2 — conflict consumption / 冲突期消费规则**: while `canonical_conflict_status` is `Under-Review`, consumers MUST NOT treat either document as authoritative; they MUST use the last `Resolved` decision in `canonical_conflict_resolution`, or, absent one, fall back to the document with the earliest `approval.decision_date` and raise a finding.

**规则 A2 — 冲突期消费规则**：当 `canonical_conflict_status` 为 `Under-Review` 时，消费者禁止将任一文档视为权威；必须采用 `canonical_conflict_resolution` 中最近一次 `Resolved` 的决议；若无，则回退到 `approval.decision_date` 最早者并提交 Finding。

`canonical_scope_id` normalization / 规范化：lowercase, `domain` prefix, kebab-case, ASCII only. Example: `architecture/data-model-design`.

`canonical_scope_id` 规范化：小写、`domain` 前缀、kebab-case、仅 ASCII。示例：`architecture/data-model-design`。

### 5.2 Normative status / 规范效力

`normative_status` ∈ {`Normative`, `Informative`}

`Normative` means the content binds implementation. `Informative` means it explains or records. An `Informative` document MUST NOT be cited as a requirement source.

`Normative` 表示内容约束实现。`Informative` 表示解释或记录。`Informative` 文档禁止被引用为需求来源。

## 6. Directory is not classification / 目录不等于分类

Directory expresses physical grouping only. Moving a file MUST NOT change `domain`, `role`, `decision_status` or `canonical_status`. A move MAY trigger a consistency check; it cannot substitute for a governance decision.

目录仅表达物理分组。移动文件禁止改变 `domain`、`role`、`decision_status` 或 `canonical_status`。移动可以触发一致性检查，但不能替代治理决议。

Canonical primary directory: `docs/{en,zh-CN}/<domain>/`. Auxiliary navigation paths (`docs/governance/`, `reviews/`, `archive/`) are indexes and records, not classification.

权威主目录为 `docs/{en,zh-CN}/<domain>/`。辅助导航路径（`docs/governance/`、`reviews/`、`archive/`）是索引与记录，不是分类。

## 7. Data authority / 数据权威来源

**Markdown frontmatter is the single source of truth.** Any CSV/YAML inventory is a CI-generated read-only view.

**Markdown frontmatter 是唯一权威来源。** 任何 CSV/YAML 盘点清单均为 CI 生成的只读视图。

CI MUST NOT write back into governed Markdown. Derived relations (`superseded_by`, reverse links, index rows) live only in generated artifacts.

CI 禁止回写受治理 Markdown。衍生关系（`superseded_by`、反向链接、索引行）仅存在于生成产物中。

## 8. Progressive adoption / 渐进采纳

A document without metadata is `_unclassified`, not "compliant by default". `_unclassified` MUST NOT be cited as a normative source.

无元数据的文档属于 `_unclassified`，不得视为默认合规。`_unclassified` 禁止被引用为规范来源。

Governance of a directory is complete only when `scripts/check_document_management.py` reports zero errors for it.

某目录只有在 `scripts/check_document_management.py` 报告零错误时，才算完成纳管。

## 9. Enforcement / 强制实施

`scripts/check_document_management.py` MUST run on every pull request and MUST fail the build on error.

`scripts/check_document_management.py` MUST 在每个 Pull Request 上运行，出错必须使构建失败。

Machine-checkable rules / 机器可检查规则：

| ID | Rule | Severity |
|---|---|---|
| DM-01 | Frontmatter parses and contains all four dimensions | Error |
| DM-02 | `domain` and `role` values are in the closed enumeration | Error |
| DM-03 | `Approved` has `approved_version` and `approval_scope` | Error |
| DM-04 | `Revoked` has `revocation.revocation_decision_id` | Error |
| DM-05 | `Archived` has `archived_date` and `archival_reason` | Error |
| DM-06 | `Canonical` has `canonical_scope_id` and keywords | Error |
| DM-07 | At most one `Canonical` per `canonical_scope_id` | Error |
| DM-08 | No hand-written `superseded_by` in frontmatter | Error |
| DM-09 | No generated inventory committed as authoritative | Warning |

Rules that cannot be mechanized — semantic parity, whether a scope is genuinely non-overlapping, whether evidence truly supports a decision — remain reviewer responsibility under GOV-DOC-001 §2.1.

无法机械化的规则（语义一致性、范围是否真正不重叠、证据是否真正支撑决议）仍属审查者职责，见 GOV-DOC-001 §2.1。

## 10. Amendment / 修订

Amendments require a `decision-record` role document, bilingual, approved by the governance authority, and MUST NOT reduce any existing guarantee.

修订须形成一份 `decision-record` 职责的双语文档，经治理机构批准，且禁止削减任何既有保证。

## 11. Change log / 变更记录

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-21 | Initial policy. Consolidates the four-dimension model, lifecycle and authority rules from the v3.1 design into an enforceable repository policy. |
