---
document_metadata:
  domain: security-governance
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Under-Review
      approver: NOT_RECORDED
      decision_date: NOT_RECORDED
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/architecture-document-management-policy.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "No formal approval record, approver identity or decision date exists in this repository; recorded as NOT_RECORDED rather than inferred."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "Governance: architecture document management"
    canonical_scope_id: "security-governance/document-management-policy"
    canonical_scope_keywords:
      - document-metadata
      - lifecycle
      - canonical-authority
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
---

# Architecture Document Management Policy / 架构文档管理条例

- Policy ID: GOV-DOC-002
- Version: 1.6
- Status: **NORMATIVE — PARTIALLY MACHINE-CHECKED** (see §9.1 for exactly which rules a machine can prove)
- Owner: A — Principal Integration / Architecture Governance
- Relation to GOV-DOC-001: **SUPPLEMENTARY — does not weaken, replace or waive GOV-DOC-001**
- Enforced by: `scripts/check_document_management.py`, `.github/workflows/document-management.yml`
- Metadata schema: `00-governance/architecture-document-metadata.schema.yaml` (machine-readable: every field, its kind, whether it is required, and its full enumeration). The file is parsed by the gate's own parser and compared against the gate's constants in both directions by T19. A field or enum value that exists in one and not the other fails the self-check.
- Fill-in template: `00-governance/templates/document-metadata-template.md`

## 1. Policy statement / 规范声明

GOV-DOC-001 governs **how a document is written** (bilingual parity). This policy governs **what a document is** (its classification and lifecycle) and **how the repository stays consistent** with that classification.

GOV-DOC-001 管辖**文档怎么写**（双语一致性）。本规范管辖**文档是什么**（分类与生命周期），以及**仓库如何与该分类保持一致**。

Where this policy and GOV-DOC-001 differ, GOV-DOC-001 prevails. This policy adds no exemption from any existing requirement.

本规范与 GOV-DOC-001 冲突时，以 GOV-DOC-001 为准。本规范不豁免任何既有要求。

## 2. Scope / 适用范围

Applies to every Markdown file under the normative roots declared in `scripts/check_bilingual_docs.py` (`NORMATIVE_ROOTS`) plus the bilingual mirrors `docs/en` and `docs/zh-CN`. The gate imports the roots from that script rather than restating them, so the two gates cannot disagree about what is governed. It imports the roots **only**: `PAIR_EXEMPT_PREFIXES` is a bilingual-pairing exemption ("this file needs no translated twin"), which is not a governance exemption ("this file need not be classified"). Borrowing that constant silently removed 89 work-item, prompt and ADR files from the governed set. There are no path exemptions. A path that must be out of scope has to be named here with a reason, in this paragraph, and kept in step with the gate.

适用于 `scripts/check_bilingual_docs.py` 中 `NORMATIVE_ROOTS` 声明的所有 Markdown 文件，加上双语镜像 `docs/en` 与 `docs/zh-CN`。门禁直接从该脚本导入根目录清单，不再自行重述，因此两个门禁对"受治理范围"不可能给出不同答案。但**只导入根目录**：`PAIR_EXEMPT_PREFIXES` 是双语配对豁免（"此文件不需要译文"），不等于治理豁免（"此文件不需要分类"）。借用该常量曾静默把 89 个 work-item / prompt / ADR 文件移出受治理集合。本规范不设路径豁免；若某路径确需排除，必须在本段写明理由，并与门禁保持同步。

Generated artifacts are **in scope**: they are scanned so that DM-09 can hold them to "not Normative, not Canonical". Being in scope for scanning is not a requirement that they carry an approval.

生成产物**在治理范围内**：纳入扫描，正是为了让 DM-09 能约束其不得成为 `Normative` / `Canonical`。纳入扫描不等于要求其具备审批。

Out of scope: source code, machine-generated non-Markdown dumps, raw test logs, images. Their architectural meaning MUST be documented in an in-scope document.

不适用：源代码、机器生成的非 Markdown 转储、原始测试日志、图片。其架构含义 MUST 在适用范围内的文档中说明。

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

The 13 technical concerns. This list is closed; adding a value requires a governance decision recorded as a `decision-record` role document.

13 个技术关注领域。该列表封闭；新增取值需形成一条 `decision-record` 职责文档所记录的治理决议。

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

L1 enforcement boundary / L1 执行边界: for `approval_scope.type: Full-document` the gate compares the body hash (frontmatter excluded) at `approved_version` with the body hash now, and fails when a stale approval still presents itself as applicable. `approved_version.value` under `scheme: git` MUST be a full 40-hex commit id: a branch or tag name can move, which would silently re-point the approval at different content. The body hash normalisation is defined in §9.1: CRLF and CR become LF (otherwise a checkout setting would invalidate every approval at once), trailing spaces and tabs per line are ignored, leading and trailing blank lines are ignored, and everything else is compared byte-for-byte — including leading spaces on a non-blank line. For `Selected-sections` and `Selected-assets` the gate only checks that the declared scope is non-empty; section-level staleness remains a manual control, because no stable section identity exists yet.

L1 执行边界：当 `approval_scope.type: Full-document` 时，门禁比较 `approved_version` 时点与当前正文（不含 frontmatter）的哈希，若失效审批仍声称适用则报错。`scheme: git` 下的 `approved_version.value` MUST 为完整 40 位 commit id：分支名或标签可移动，会静默把审批指向不同内容。正文哈希规范化口径见 §9.1：CRLF 与 CR 规范化为 LF（否则 checkout 设置会把所有审批一次性判失效）、忽略每行行尾空格与制表符、忽略首尾空行；其余逐字节比较，非空行行首空格也算差异。当为 `Selected-sections` / `Selected-assets` 时，门禁只校验声明的范围非空；章节级失效仍属人工控制，因为目前尚无稳定的章节标识。

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

**Rule A1 — scope conflict / 范围冲突**: at most ONE `Canonical` document per `canonical_scope_id`, at all times. Conflict state MUST NOT double as authority: while `canonical_conflict_status` is `Under-Review`, every conflicting document MUST declare `canonical_status: Candidate`. Two documents claiming `Canonical` in one scope is a gate error, not a state a document may sit in.

**规则 A1 — 范围冲突**：任何时刻，每个 `canonical_scope_id` 最多允许一份 `Canonical` 文档。冲突状态禁止与权威叠加：当 `canonical_conflict_status` 为 `Under-Review` 时，每份冲突文档 MUST 声明 `canonical_status: Candidate`。同一范围内两份文档同时声称 `Canonical` 属门禁错误，而不是文档可以长期停留的状态。

**Rule A2 — conflict consumption / 冲突期消费规则**: consumers MUST resolve authority through `resolve_canonical(documents, scope_id)`, the single sanctioned resolver. It returns `NO_AUTHORITATIVE_SOURCE` whenever the scope is empty, has more than one `Canonical`, or carries any conflict status other than `None`. There is NO fallback heuristic: an earlier approval date is not evidence of authority, and guessing hides the conflict.

**规则 A2 — 冲突期消费规则**：消费者 MUST 通过唯一受认可的解析接口 `resolve_canonical(documents, scope_id)` 解析权威。当范围为空、存在多份 `Canonical`，或存在 `None` 以外的冲突状态时，该接口返回 `NO_AUTHORITATIVE_SOURCE`。禁止任何回退启发式：更早的审批日期不是权威证据，猜测只会掩盖冲突。

Interface contract / 接口契约: `resolve_canonical` accepts a document set that has already passed DM-01..DM-13 across the whole governed tree. It resolves authority; it does not certify that the set is complete or valid. A caller that feeds it a partial or unvalidated set gets a wrong answer, and the gate's own run is the only place that guarantee is established.

接口契约：`resolve_canonical` 接受的是已通过全树 DM-01..DM-13 的文档集合。它只解析权威，不认证集合的完整性与合法性。传入不完整或未校验的集合会得到错误答案；该保证只在门禁自身运行时成立。

Conflict resolution is an auditable record, not a status flip / 冲突决议是可审计的记录，而非状态翻转：

```yaml
canonical_conflict_status: Resolved
canonical_conflict_resolution:
  resolution_decision_id: "GOV-CONF-2026-002"   # unique, never reused
  resolved_date: "2026-05-10"
  selected_document: "docs/en/02-domain-model/entity-model.md"
  resolution_evidence: []
```

The gate checks that a `Resolved` status carries a complete record, that `selected_document` really declares the scope, and that it is the document holding `Canonical`. It cannot check that the decision was a good one; that remains reviewer responsibility.

门禁检查 `Resolved` 状态是否带有完整记录、`selected_document` 是否确实声明该范围、以及它是否就是持有 `Canonical` 的文档。门禁无法检查该决议是否合理，那仍属审查者职责。

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

Generated artifacts MUST identify themselves with an HTML comment containing `GENERATED FILE`, `GENERATED ARTIFACT` or `DO NOT EDIT`, anywhere in the body. The marker is the protocol: a file without it is treated as hand-written, and a file with it MUST NOT claim `Normative` or `Canonical` (DM-09). Prose that merely mentions generated files does not count.

生成产物 MUST 在正文任意位置用包含 `GENERATED FILE`、`GENERATED ARTIFACT` 或 `DO NOT EDIT` 的 HTML 注释自证身份。该标记即为协议：无标记视为手写文件，有标记则禁止声明 `Normative` 或 `Canonical`（DM-09）。仅在正文中提及"生成文件"不算标记。

## 8. Progressive adoption / 渐进采纳

A document without metadata is `_unclassified`, not "compliant by default". `_unclassified` MUST NOT be cited as a normative source.

无元数据的文档属于 `_unclassified`，不得视为默认合规。`_unclassified` 禁止被引用为规范来源。

Governance of a directory is complete only when `scripts/check_document_management.py` reports **zero errors AND zero unclassified documents** for it. Zero errors alone is not completion: an unclassified document is not a compliant document, it is an unreviewed one.

某目录只有在 `scripts/check_document_management.py` 对该目录报告**零错误且零未分类**时，才算完成纳管。仅零错误不构成完成：未分类文档不是合规文档，而是未受审查的文档。

Because the backlog is large, the gate also offers a hard edge that does not require full adoption: `--require-changed <ref>` makes metadata mandatory for every governed file added or modified since `<ref>`, untracked included. The backlog may stay unclassified; it may not grow.

由于存量积压较大，门禁另提供不依赖全量采纳的硬边界：`--require-changed <ref>` 要求自 `<ref>` 以来新增或修改（含未跟踪）的所有受治理文件必须带元数据。积压可以继续未分类，但禁止增长。

The gate therefore has three distinct verdicts, and they MUST NOT be reported as one another:

1. **Incremental** (`--require-changed REF`): exit 0, message `PASS (incremental)`. Says the changed files are classified and no cross-document rule is violated. Says nothing about the rest of the tree.
2. **Whole tree, complete** (`--strict`, zero unclassified): exit 0, message `PASS (whole tree)`.
3. **Whole tree, backlog present** (no flag, unclassified > 0): exit **2**, message `INCOMPLETE`. Rules passed, adoption did not. This is deliberately not exit 0 and deliberately not the word PASS: a first push with no base commit lands here, and it must not read as "the repository is classified".

`--require-changed` and `--strict` are mutually exclusive; combining them is a usage error.

门禁因此有三种互不相同的判定，禁止互相冒充：

1. **增量**（`--require-changed REF`）：退出 0，输出 `PASS (incremental)`。表示变更文件已分类且无跨文档规则违规，对树内其余部分不作任何声明。
2. **全树且完成**（`--strict`，零未分类）：退出 0，输出 `PASS (whole tree)`。
3. **全树但存在积压**（无参数，未分类 > 0）：退出 **2**，输出 `INCOMPLETE`。规则通过，采纳未完成。这里刻意不用退出 0、刻意不用 PASS 字样：首次推送无基线时会落到这一态，它不得被读成"仓库已完成分类"。

`--require-changed` 与 `--strict` 互斥，同时使用属用法错误。

Open gap / 未闭合缺口: if a branch's first push has no base commit to diff against (`github.event.before` all zeros), the workflow falls back to the whole-tree scan. That run now returns INCOMPLETE (exit 2) whenever the backlog is non-empty, so it fails loudly instead of passing quietly, but it still cannot prove that the *newly added* files are classified — it only proves the backlog exists. Recorded as GAP-02 in `docs/governance/documentation-gaps.md`.

未闭合缺口：若某分支的首次推送没有可比对的基线提交（`github.event.before` 全零），工作流退回全仓扫描。该次运行在积压非空时现在返回 INCOMPLETE（退出 2），因此会显式失败而非静默通过；但它仍无法证明**本次新增**文件已分类，只能证明积压存在。登记为 `docs/governance/documentation-gaps.md` 中的 GAP-02。

## 9. Enforcement / 强制实施

`scripts/check_document_management.py` MUST run on every pull request and every push to `main`, with `--require-changed <base>` where a base commit exists, and MUST fail the build on error.

`scripts/check_document_management.py` MUST 在每次 Pull Request 与每次推送 `main` 时运行；存在基线提交时必须带 `--require-changed <base>`；出错必须使构建失败。

Machine-checkable rules / 机器可检查规则：

| ID | Rule | Severity |
|---|---|---|
| DM-01 | Frontmatter parses under the declared YAML subset; a node of the wrong type is an error, never a crash; every required field is present leaf by leaf (`domain`, `role`, `lifecycle.approval.decision_status`, `lifecycle.usage_status`, `lifecycle.modification_status`, `lifecycle.evidence_verification.verification_status`, `authority.canonical_status`, `authority.normative_status`, `authority.canonical_conflict_status`). An empty `lifecycle: {approval: {}}` is not a classification. Every path-valued field is a normalised repository-relative path: a non-string, an absolute path, a `..` segment, a backslash, a repeated `./`, or an empty segment is an error, never silently rewritten | Error |
| DM-02 | `domain`, `role` and every status value are in the closed enumerations; unknown keys are errors at every level | Error |
| DM-03 | `Approved` has `approved_version` (scheme + value), `approval_scope.type` and `approval_applicability`; `Selected-sections` has a non-empty `included_sections` | Error |
| DM-04 | `Revoked` has `revocation.revocation_decision_id`, `revoked_date`, `revocation_reason`; the id is unique repository-wide | Error |
| DM-05 | `Archived` has `archived_date` and `archival_reason` | Error |
| DM-06 | `Canonical` has `canonical_scope`, keywords, and a normalized `canonical_scope_id` whose prefix equals `domain` | Error |
| DM-07 | At most one `Canonical` per `canonical_scope_id` | Error |
| DM-08 | No hand-written `superseded_by` anywhere in the frontmatter | Error |
| DM-09 | A file carrying the generated-artifact marker (an HTML comment containing `GENERATED FILE`, `GENERATED ARTIFACT` or `DO NOT EDIT`, anywhere in the body) MUST NOT be `Normative` or `Canonical` | Error |
| DM-10 | `Approved` + `scheme: git` / `content-hash`: `approved_version.value` is an immutable full commit id; the body is unchanged since then, otherwise `Pending-Reapproval` + `Not-Applicable-To-Current-Version`. "Unchanged" uses only the equivalence §9.1 declares: CRLF/CR → LF, trailing spaces/tabs per line, leading/trailing blank lines. No other character is treated as a line break — `U+2028`, `U+2029`, `U+000B`, `U+000C`, `U+001C`–`U+001E` and `U+0085` are content, so they change the hash | Error |
| DM-11 | A document under `Under-Review` conflict MUST NOT be `Canonical`; `Resolved` requires a complete resolution record whose `selected_document` is the unique `Canonical` document of the scope | Error |
| DM-12 | A mirror group is consistent: every declared counterpart exists, is classified, points into the language directory named by its field, belongs to the same source, and the source lists every mirror that names it. A source that declares no mirrors at all is a failure, not a skipped check. `domain`/`role`/`normative_status` agree, and only one document in the group is `Canonical` | Error |
| DM-13 | `supersedes` targets exist, are not self-references, and form no cycle | Error |

### 9.1 Verified versus unverified / 已验证与未验证

| Rule | Machine-verified | Left to reviewers |
|---|---|---|
| DM-01..DM-09, DM-11..DM-13 | Full | — |
| DM-10 `Full-document` | Full (body hash, commit id pinned) | — |
| DM-10 `Selected-sections` | Scope declared | Whether the selected sections are the right ones |
| Body hash normalisation | CRLF/CR normalised to LF (checkout setting must not invalidate every approval); trailing spaces/tabs per line ignored; leading/trailing blank lines ignored; everything else, including leading spaces on a non-blank line, is compared byte-for-byte. Only these three equivalences apply: any other character, including Unicode line/paragraph separators, changes the hash | Whether that equivalence is too coarse for a given document |
| Governed set | The roots come from `check_bilingual_docs.py`; no path exemption exists. A file either carries metadata or counts as backlog | Whether the root list covers every directory that should be governed (no repository-wide ground truth exists) |
| Verdict semantics | Three distinct outcomes: incremental pass, whole-tree pass, whole-tree INCOMPLETE (exit 2). A run cannot report PASS while backlog exists | Whether a given directory's backlog is acceptable to ship with |
| Schema/gate agreement | Both directions: fields shown but rejected, required leaves absent, enum values missing or extra. The schema is parsed by the gate's own parser, so it cannot be written in syntax the gate refuses | Whether the schema's prose describes the rule correctly |
| Increment scope | Added, modified, renamed, type-changed and copied paths (`AMRTC`), plus untracked | Whether a path that changes meaning without changing name can hide elsewhere |
| Accounting | Classified + unclassified equals the governed count, asserted every run | — |
| Cross-document rules (DM-07, DM-11, DM-12, DM-13) | Only over a whole-tree scan; the gate offers no partial mode, because one file can hide another's duplicate scope | — |
| Canonical scope overlap | Unique ids, unique `Canonical` | Whether two scopes genuinely overlap |
| Approval / evidence truth | Field presence and shape | Whether the decision or evidence is real |
| Bilingual parity | Existence, language-directory match, group closure, metadata agreement | Semantic parity (GOV-DOC-001) |
| `_unclassified` citation ban | Not verifiable in-repo | Enforced by readers and AI agents |

The table is the contract. A rule listed in the right column MUST NOT be described elsewhere as governed by CI.

该表即契约。列在右列的规则，禁止在其他地方被描述为由 CI 保障。

Rules that cannot be mechanized — semantic parity, whether a scope is genuinely non-overlapping, whether evidence truly supports a decision — remain reviewer responsibility under GOV-DOC-001 §2.1.

无法机械化的规则（语义一致性、范围是否真正不重叠、证据是否真正支撑决议）仍属审查者职责，见 GOV-DOC-001 §2.1。

## 10. Amendment / 修订

Amendments require a `decision-record` role document, bilingual, approved by the governance authority, and MUST NOT reduce any existing guarantee.

修订须形成一份 `decision-record` 职责的双语文档，经治理机构批准，且禁止削减任何既有保证。

## 11. Change log / 变更记录

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-21 | Initial policy. Consolidates the four-dimension model, lifecycle and authority rules from the v3.1 design into an enforceable repository policy. |
| 1.1 | 2026-11-21 | Independent review response. Fail-closed parser (DM-01), version-bound approval made mechanical for full documents (DM-10), A1/A2 conflict state no longer doubles as authority and the date fallback is removed (DM-11), mirror consistency and supersession graph added (DM-12/13), domain count corrected to 13, completion redefined as zero unclassified, and the machine-checked claim replaced by the §9.1 split. |
| 1.2 | 2026-11-21 | Second independent review (5.2/10). Parser: unescaped single quotes, missing space after `:`, and unknown keys under `supersession` now rejected; wrong node types produce a DM-01 error instead of a traceback. DM-09 scans the whole body and defines the marker as an HTML comment. DM-11 requires `selected_document` to be the unique Canonical document even when none holds Canonical. DM-12 requires the counterpart to be classified and to declare this document back. DM-10 requires a full 40-hex commit id, so a moving branch name cannot carry an approval. `--require-changed` reads NUL-separated paths, so a filename with spaces cannot dodge it, and now also runs on direct pushes. |
| 1.3 | 2026-11-21 | Third independent review (56/100). `_enum()` now type-guards before the membership test, so a non-scalar (`domain: []`) yields a DM-01 error instead of a `TypeError` (P0-01). Required fields are checked leaf by leaf, so `lifecycle: {approval: {}}` plus `authority: {}` no longer passes as an empty shell (P1-01). §4.1 and §9.1 now state the same body-hash normalisation, and the ceiling of that equivalence is named as a residual risk (P1-02). `--only` is removed: cross-document rules are only sound over a whole tree (P1-03). DM-12 is restated as three-way group closure — source, `docs/en` mirror, `docs/zh-CN` mirror — so a missing third member is an error rather than an untested assumption (P1-04). The governed roots are imported from `check_bilingual_docs.py` instead of duplicated. |
| 1.4 | 2026-11-21 | Fourth independent review (43/100). **Scope had been silently shrunk**: the gate imported `PAIR_EXEMPT_PREFIXES` and used it as a path exemption, so 89 work-item, prompt and ADR files were never governed. A pairing exemption is not a governance exemption; the import is now roots-only and §2 says so (P0-01). `lstrip("./")` is a character set, not a prefix — `"../../00-governance/a.md"` collapsed to `"00-governance/a.md"` — so every path-valued field goes through `rel_path()`, which rejects absolute paths, `..`, backslashes, repeated `./` and empty segments (P1-01). DM-12's reverse closure used `.get()`, so a source that declared nothing made the check silently pass; it now uses a `defaultdict(set)` and reports a mirror naming an undeclared or unclassified source (P1-02). DM-10's "unchanged" test used `str.splitlines()`, which also breaks on `U+2028`, `U+2029`, `U+000B`, `U+000C`, `U+001C`–`U+001E` and `U+0085` — two different bodies could hash alike; only CRLF/CR are normalised now, and `git show` is read raw instead of stripped (P1-03). Three verdicts replace the old single PASS: incremental, whole-tree complete, and whole-tree INCOMPLETE (exit 2) when backlog remains, so a first push with no base can no longer read as a full pass (P1-04). The schema file is now cross-checked against the gate in both directions — every key it shows, every required leaf, and every enum value — which immediately caught that it had never listed the 13 domain values. |
| 1.5 | 2026-11-21 | Fifth independent review (72/100). `--diff-filter=AMR` missed `T` (type change), so turning a governed path into a symlink — or a symlink into a file — escaped the increment without changing the path; the filter is now `AMRTC` (P1-05). The schema file was a filled-in template, not a contract: it is now machine-readable (per-field `kind`, `required`, full `enum`), parsed by the gate's own parser and compared both ways by T19, which immediately rejected the file's own use of flow sequences the gate refuses, and then proved it catches a missing enum value. The copy-paste example moved to `00-governance/templates/document-metadata-template.md`, which now carries its own metadata and is checked against the gate (P1-06). `rel_path()` rejects non-string values instead of stringifying them, and the mutually exclusive flag check runs before any git call, so a bad REF can no longer mask a usage error (P1-01/P1-04 follow-ups). |
| 1.6 | 2026-11-21 | Sixth review. T19 checked that `kind` was present but never that it was a legal value, so `kind: completely-unknown-kind` passed; the kind vocabulary is now closed and `items`, `required` and `enum`-on-string are checked too (P1-06-R). The increment filter adds `C` for copies, since `diff.renames=copies` can present a new path as a copy rather than an addition (P2-02). The gate now asserts the accounting identity classified + unclassified = governed, so a file dropped by the classification loop cannot hide as a smaller total (P1-08). |
