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
- Version: 1.17
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

The scope above is declared **and checked**. `00-governance/document-scope-registry.yaml` must account for every top-level directory of the repository, either as a governed root or as an exclusion with a reason; DM-14 fails the gate when a directory is missing, when the registry's governed list differs from `NORMATIVE_ROOTS` in either direction, when a directory is both governed and excluded, or when a named directory does not exist. A new top-level directory is therefore a governance decision that has to be written down, not a silent widening of the ungoverned surface. The registry is the independent basis the gate cannot derive from itself: the accounting identity proves no file was dropped *within* the scan set, and only the registry says whether the scan set is the right one.

上述范围是**声明出来并被检查的**。`00-governance/document-scope-registry.yaml` 必须覆盖仓库每个顶层目录——要么是受治理根目录，要么带理由排除；当某目录缺失、登记表声明的根目录与 `NORMATIVE_ROOTS` 任一方多出或少出、某目录同时受治理又被排除、或登记了不存在的目录时，DM-14 使门禁失败。因此新增顶层目录是一次必须写下来的治理决定，而不是治理空白面的静默扩大。登记表是门禁无法自行推导的独立依据：会计恒等式只能证明扫描集**内部**没有文件被丢弃，扫描集本身是否正确只有登记表能说。

Every directory has exactly one of three states, and only the first is an exemption. **Governed**: scanned, must carry metadata. **Backlog**: scanned, counted, may lack metadata. **Excluded**: not scanned, and only when no architecture claim is made — source code, review transcripts, benchmark logs, prompt text. A directory whose documents *are* architecture documentation goes in `backlog:` with a document count, never in `excluded:` with a reason: backlog is the opposite of an exemption, and treating it as one made "we have not classified these" indistinguishable from "these are not architecture". The count is not decoration — DM-14 compares it to the disk, so "27 documents remain" is a claim that fails the gate when it stops being true.

`docs/` is the one directory that is partly governed and partly backlog. `docs/en` and `docs/zh-CN` are governed mirrors; `docs/governance/documentation-gaps.md` is governed individually because this policy cites it as the record of what remains unclosed, and a governance record that could drift outside governance would defeat its own purpose; the remaining 27 pages under `docs/` are architecture documents — the convergence programme, the minimum-runnable architecture, the canonical transaction, the source-of-truth inventory, the product-first research — and they are backlog. Most of them say `DRAFT / NON-NORMATIVE` in their own header, and that is precisely why they are backlog rather than excluded: `Draft` is a value of `lifecycle.approval.decision_status`, not a reason to be outside the classification system.

每个目录恰有三种状态之一，且只有第一种是豁免。**受治理**：被扫描，必须带元数据。**积压**：被扫描、被计数，可缺元数据。**排除**：不被扫描，且仅当不作出架构主张——源代码、审查记录、基准日志、提示词文本。文档**属于**架构的目录应进入 `backlog:` 并给出文档数，绝不进入 `excluded:` 给一个理由：积压是豁免的反面，把它当作豁免会使"我们还没分类这些"与"这些不是架构"变得无法区分。计数不是装饰——DM-14 会与磁盘核对，因此"还剩 27 份"是一句会在不再为真时使门禁失败的声明。

`docs/` 是唯一部分受治理、部分积压的目录：`docs/en` 与 `docs/zh-CN` 是受治理镜像；`docs/governance/documentation-gaps.md` 按单文件受治理，因为本条例引用它作为"尚未闭合事项"的记录，而一份能漂移到治理之外的治理记录会自毁其目的；`docs/` 下其余 27 份是架构文档——收敛计划、最小可运行架构、规范事务、事实源清单、产品优先研究——它们是积压。它们大多在自身头部写着 `DRAFT / NON-NORMATIVE`，而这正是它们属于积压而非被排除的原因：`Draft` 是 `lifecycle.approval.decision_status` 的取值，不是置身分类体系之外的理由。

Open gap / 未闭合缺口: DM-14 checks that an exclusion *has* a reason and that it is bilingual. It cannot check that the reason is honest — "not documentation" and "not yet migrated" look identical to a gate. Recorded as GAP-03 in `docs/governance/documentation-gaps.md`.

未闭合缺口：DM-14 只能检查排除项**有**理由且理由为双语，无法检查理由是否诚实——"不是文档"与"尚未迁移"对门禁而言完全一样。登记为 `docs/governance/documentation-gaps.md` 中的 GAP-03。

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
| DM-01 | Frontmatter parses under the declared YAML subset; a node of the wrong type is an error, never a crash. Every field's declared `kind` is enforced on the document (`check_kinds()`), and every field the schema marks `required: true` must be present, reported by its full path. There is no second hand-maintained required list: `required_fields()` is derived from the schema, because the two used to disagree (`approval_scope` was required by the schema and omitted by the list). An empty `lifecycle: {approval: {}}` is not a classification. Every path-valued field is a normalised repository-relative path: a non-string, an absolute path, a `..` segment, a backslash, a repeated `./`, or an empty segment is an error, never silently rewritten | Error |
| DM-02 | `domain`, `role` and every status value are in the closed enumerations; unknown keys are errors at every level | Error |
| DM-03 | `Approved` has `approved_version` (scheme + value), `approval_scope.type` and `approval_applicability`; `Selected-sections` has a non-empty `included_sections`; `Selected-assets` has a non-empty `included_assets`. A scope type that requires nothing is a label, not a scope | Error |
| DM-04 | `Revoked` has `revocation.revocation_decision_id`, `revoked_date`, `revocation_reason`; the id is unique repository-wide | Error |
| DM-05 | `Archived` has `archived_date` and `archival_reason` | Error |
| DM-06 | `Canonical` has `canonical_scope`, keywords, and a normalized `canonical_scope_id` whose prefix equals `domain` | Error |
| DM-07 | At most one `Canonical` per `canonical_scope_id` | Error |
| DM-08 | No hand-written reverse relation at the declared path. The forbidden paths come from the schema's `forbidden:` list and are matched **in full** (`walk_paths()`): matching only the last segment reported `authority.superseded_by` as `lifecycle.supersession.superseded_by`, naming a location the author never wrote, and merged declarations that happened to share a leaf. A second hard-coded key in the gate would be a rule declared twice and enforced once | Error |
| DM-09 | A file carrying the generated-artifact marker (an HTML comment containing `GENERATED FILE`, `GENERATED ARTIFACT` or `DO NOT EDIT`, anywhere in the body) MUST NOT be `Normative` or `Canonical` | Error |
| DM-10 | `Approved` + `scheme: git` / `content-hash`: `approved_version.value` is an immutable full commit id; the body is unchanged since then, otherwise `Pending-Reapproval` + `Not-Applicable-To-Current-Version`. "Unchanged" uses only the equivalence §9.1 declares: CRLF/CR → LF, trailing spaces/tabs per line, leading/trailing blank lines. No other character is treated as a line break — `U+2028`, `U+2029`, `U+000B`, `U+000C`, `U+001C`–`U+001E` and `U+0085` are content, so they change the hash | Error |
| DM-11 | A document under `Under-Review` conflict MUST NOT be `Canonical`; `Resolved` requires a complete resolution record whose `selected_document` is the unique `Canonical` document of the scope | Error |
| DM-12 | A mirror group is consistent: every declared counterpart exists, is classified, points into the language directory named by its field, belongs to the same source, and the source lists every mirror that names it. A source that declares no mirrors at all is a failure, not a skipped check. `domain`/`role`/`normative_status` agree, and only one document in the group is `Canonical` | Error |
| DM-13 | `supersedes` targets exist, are not self-references, and form no cycle | Error |
| DM-14 | The declared scope equals the enforced scope. Every top-level directory — hidden ones included, with `.git` as the sole structural exception — must be **governed**, **backlog**, or **excluded**. Excluded requires `kind: not-documentation` plus `reason` and `reason_zh`; backlog requires a document count that DM-14 compares to the disk and a bilingual reason, and is scanned like a governed root. No directory may be in two states, every named directory must exist, the declared roots must equal `NORMATIVE_ROOTS` in both directions, and `governed_files` must equal the gate's list with each entry proven to be a regular file *inside* the repository (a symlink, or a file reached through a symlinked parent, is an error — the registry check and the scanner must agree). A new top-level directory is therefore a governance decision, not a silent widening of the ungoverned surface; `.git` and `target/` are structurally exempt because they are VCS and build state present in some working copies and absent in others, so declaring them would describe a machine rather than the repository | Error |

### 9.1 Verified versus unverified / 已验证与未验证

| Rule | Machine-verified | Left to reviewers |
|---|---|---|
| DM-01..DM-09, DM-11..DM-14 | Full | — |
| DM-10 `Full-document` | Full (body hash, commit id pinned) | — |
| DM-10 `Selected-sections` | Scope declared | Whether the selected sections are the right ones |
| Body hash normalisation | CRLF/CR normalised to LF (checkout setting must not invalidate every approval); trailing spaces/tabs per line ignored; leading/trailing blank lines ignored; everything else, including leading spaces on a non-blank line, is compared byte-for-byte. Only these three equivalences apply: any other character, including Unicode line/paragraph separators, changes the hash | Whether that equivalence is too coarse for a given document |
| Governed set | One entry point (`collect_governed()`) builds the set from three sources — normative roots, backlog roots, individually governed files — keyed on the resolved path, so no file is collected twice and no problem found during the walk is dropped; an unresolvable path is a problem, never a fallback key. `governed_files()` remains for diagnostics and T67 walks the AST of every Python source file inside the declared repository scan boundary to prove no verdict is built from it — a comment saying so is not evidence. DM-14 additionally proves the scan set equals the declared set: every top-level directory — hidden included — must be governed, backlog, or excluded; a symlink satisfies neither; a backlog count is declared once in `documents:`, is checked against the disk, and the prose reasons are forbidden from restating a document count (a second copy of a fact is a copy that can disagree); and `registry_version` must be one this gate implements | Whether an *exclusion* reason is honest (the gate checks that a reason exists and is bilingual, not that it is true) |
| Manual controls | `MANUAL_CONTROLS` is the single authority: a tuple of (id, control, why-a-machine-cannot-do-it, accountable). Section 9.2 is **rendered** from it between generated-block markers. The run prints each entry's id and control only -- not the whole tuple, and the gate does not claim otherwise. T69 re-renders the table and compares byte for byte, scoped to section 9.2, so a hand edit inside the block fails instead of drifting. It also checks the block's structure, not just its rows: exactly one BEGIN and one END marker, BEGIN before END, header and separator present, each control exactly once, no second hand-kept control table elsewhere in the section, and the marker itself must not match DM-09's generated-artifact pattern (a marker worded to please a human would make this Normative policy a generated artifact). Two representations from one authority — not two authorities with a synchronisation test. Two representations from one authority — not two authorities with a synchronisation test | Whether each control is *actually* left to a human: the list says what the gate does not check, and a reviewer must decide whether that residue is acceptable |
| Verdict semantics | Three distinct outcomes: incremental pass, whole-tree pass, whole-tree INCOMPLETE (exit 2). A run cannot report PASS while backlog exists | Whether a given directory's backlog is acceptable to ship with |
| Schema/gate agreement | Both directions: fields shown but rejected, required leaves absent, enum values missing or extra. The schema is parsed by the gate's own parser, so it cannot be written in syntax the gate refuses. Every declared `kind` is *enforced* on real documents, not merely published (`check_kinds()`) | Whether the schema's prose describes the rule correctly |
| Schema semantics | A hand-written golden corpus (`GOLDEN`, 13 cases, plus 3 body-level DM-09 cases) states expected verdicts without deriving them from any gate constant, so a fault shared by schema and constants still fails | Whether the corpus covers the case you care about |
| Schema self-defence | The schema is loaded from `--root`, not from the gate's own directory, so the contract travels with the repository. `fields: {}`, a missing dimension, fewer than 5 required leaves, an unread constraint key, or a `schema_version` this gate does not implement all stop the run instead of leaving `check_kinds()` with nothing to check | — |
| Constraint-key vocabulary | Only keys the gate actually reads are accepted: `kind`, `required`, `enum`, `items`, `fields` — and each is **typed**, not merely named. Rejecting unknown names is not enforcement: `required: "false"` is a string, `is True` is False for it, and the field silently became optional; `enum: architecture` iterates as characters; `items` on a non-sequence describes nothing. Meaningless combinations are refused too (`items` only on a sequence, `enum` never on a boolean, every leaf needs a `kind` or `fields`, and a node with children can only be a mapping — `kind: string` beside `fields:` states two contradictory things and the gate would honour whichever it read first). `pattern` and `when` were removed outright: nothing evaluated them | — |
| Symbolic links | One walk serves both the scan and the count (`scan_root()`), and `collect_governed()` is the single entry point that turns its results into the governed set — the problems travel with the files, so a walk that found fewer files cannot do so silently. Every symlink met — a root, a subdirectory, a `.md` — is **reported by path** and not traversed. Directory enumeration for the registry uses `is_dir() and not is_symlink()`, because `is_dir()` follows links: a top-level link otherwise satisfied both "on disk" and "declared", making a registry entry true that pointed outside the repository | Whether a symlink was intended as content rather than a mistake — the gate only reports it |
| Increment scope | Added, modified, renamed, type-changed and copied paths (`AMRTC`), plus untracked | Whether a path that changes meaning without changing name can hide elsewhere |
| Accounting | Classified + unclassified equals the governed count, asserted every run | — |
| Cross-document rules (DM-07, DM-11, DM-12, DM-13) | Only over a whole-tree scan; the gate offers no partial mode, because one file can hide another's duplicate scope | — |
| Canonical scope overlap | Unique ids, unique `Canonical` | Whether two scopes genuinely overlap |
| Approval / evidence truth | Field presence and shape | Whether the decision or evidence is real |
| Bilingual parity | Existence, language-directory match, group closure, metadata agreement | Semantic parity (GOV-DOC-001) |
| `_unclassified` citation ban | Not verifiable in-repo | Enforced by readers and AI agents |

The table is the contract. A rule listed in the right column MUST NOT be described elsewhere as governed by CI.

该表即契约。列在右列的规则，禁止在其他地方被描述为由 CI 保障。

### 9.2 Manual controls / 人工控制

These are the controls a machine cannot perform. They are listed by identifier so a review can name the one it is relying on, and so that no future text can claim CI covers them. Each is a judgement about truth or intent, not about shape: the gate can prove a field is present, non-empty and bilingual; it cannot prove the sentence is honest.

以下是机器无法执行的控制项。逐条编号，使审查可以指名它所依赖的那一条，也使今后任何文本都无法声称 CI 覆盖了它们。每一条都是关于真伪或意图的判断，而不是关于形状：门禁能证明字段存在、非空、双语齐备，不能证明那句话是真的。

<!-- BEGIN MANUAL-CONTROLS (rendered from MANUAL_CONTROLS in scripts/check_document_management.py) -->
| ID | Manual control | Why a machine cannot do it | Accountable |
|---|---|---|---|
| M-01 | Whether two `Canonical` scopes genuinely overlap | Overlap is a claim about meaning. The gate proves the ids are unique and only one document per group is `Canonical`; whether two *different* ids cover the same subject is not derivable from metadata | Reviewer |
| M-02 | Whether an `Approved` decision is real | The gate proves a decision record exists, names an approver and binds to a commit. It cannot prove a person with that authority actually decided | Approver, then reviewer |
| M-03 | Whether `evidence_verification` evidence supports the decision | The gate proves a verification status and a reference exist. Whether the reference supports the claim is an argument, not a field | Reviewer |
| M-04 | Whether the `Selected-sections` chosen are substantively sufficient | The gate proves the declared sections exist, that the identifiers resolve and that the scope is non-empty. Whether that selection is *adequate* for the document is a judgement | Approver |
| M-05 | Semantic parity of a bilingual mirror | GOV-DOC-001 requires that the two versions say the same thing. The gate proves both exist, point at each other, and agree on metadata — not that the prose agrees | Reviewer |
| M-06 | Whether an exclusion reason is honest | DM-14 proves a reason exists and is bilingual. `kind: not-documentation` is an assertion by the author; no file content can refute it | Reviewer |
| M-07 | Whether a declared backlog is acceptable to ship | The count is checked against the disk, which proves the number is true, not that the remainder is tolerable | Governance authority |
| M-08 | Whether external consumers obey `resolve_canonical()` | The gate can see this repository. Readers outside it (agents, tools, downstream systems) are not observable here, so their discipline is a contract, not a check | Consumer owners |
| M-09 | Whether the normalisation equivalence is appropriate for a document's semantics | §9.1 fixes three equivalences (CRLF/CR → LF, trailing whitespace, blank-line edges) and the gate applies them exactly. Whether that equivalence is right for one document's meaning is not a property of the bytes | Reviewer |
| M-10 | Whether the `_unclassified` citation ban is respected | The ban is on how a document is *used*. Nothing in the repository records who cited what | Reader / agent operators |
<!-- END MANUAL-CONTROLS -->

A run prints this list under `manual controls (not machine-verified)` so the boundary travels with every verdict rather than living only in this table.

每次运行都会在 `manual controls (not machine-verified)` 下打印该清单，使边界随每个裁决一起出现，而不是只活在这张表里。

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
| 1.8 | 2026-11-21 | Eighth review, five blockers. P0-01: `required: true` was published and never executed — `approval_scope` was required by the schema, omitted from the hard-coded `REQUIRED_FIELDS`, and absent from every fixture, so the schema and the gate disagreed while the tests endorsed the schema-violating input. `check_kinds()` now enforces `required` too, `required_fields()` is derived from the schema, and the second list is deleted (T19 fails if one reappears). The same review found `approval_scope` should not be unconditionally required — DM-03 covers it for `Approved` — so the schema says `when: decision_status == Approved` rather than a flat `required: true`. P1-04: `fields: {}` parsed, was a dict, and left `check_kinds()` with nothing to check; `schema()` now refuses a schema that has lost a dimension or marks fewer than 5 leaves required, and loads from `--root` so the contract travels with the repository. P1-01: `docs/governance/documentation-gaps.md` was cited by this policy three times as the gap record while sitting outside governance — a governance record that can drift outside governance defeats its purpose; it is now governed individually via `GOVERNED_FILES`, and §2 distinguishes "not documentation" from "not yet migrated" so an exclusion cannot be used to hide backlog. P1-02: `Path.is_dir()` follows symlinks, so a symlinked top-level directory looked like a root to declare; symlinked roots and files are now skipped and a root-level symlink is an error. P1-03: the corpus claimed 11 cases and had 10, and no case covered DM-09; it now has 13 metadata cases plus 3 body-level generated-artifact cases. |
| 1.9 | 2026-11-21 | Pre-review self-audit. The schema declared `when: decision_status == Approved` and the gate never read it: the same class of defect as `required: true` used to be, one level quieter. Two keys were affected. `pattern` is removed from the vocabulary entirely -- the gate has no evaluator for it, so allowing it would let the schema publish a constraint nothing enforces; T19 now rejects any constraint key the gate does not read. `when` is kept but must name the rule that owns the requirement (`when: DM-03 ...`), and T19 fails if that id is not a row in this policy's rule table, so a `when` can no longer point at a rule that does not exist. |
| 1.10 | 2026-11-21 | Ninth review, three blockers plus one gap of my own. R1-01: the registry check used `is_file()` (which follows symlinks) while the scanner skipped symlinks, so a symlinked `governed_files` entry passed the registry and was never scanned -- in the reproduction the gate reported **zero governed documents** and exit 0. Containment is now proven on the resolved path, which also catches a file reached through a symlinked *parent*, a case `is_symlink()` cannot see. R1-02: `on_disk` skipped dot-directories, so `.new-architecture/` was neither governed, excluded, reported nor scanned; hidden directories now count, with `.git` as the one structural exception. R1-03: the `docs/` exclusion was not honest -- 26 files there include the minimum-runnable architecture, the canonical transaction and the source-of-truth inventory, and their own `DRAFT / NON-NORMATIVE` header is a value of `lifecycle.approval.decision_status`, not a reason to be outside classification. `not-yet-migrated` is no longer an exclusion kind: such directories go in a new `backlog:` section, are scanned, and carry a document count DM-14 compares to the disk. S1-02: the schema cache is keyed on content instead of path, so rewriting a root's schema no longer leaves the process validating the previous contract. S1-03 was reported as missing material; the increment already failed such a commit, and T48 now proves it: deleting metadata from a classified file fails `--require-changed`. |
| 1.11 | 2026-11-21 | Self-audit while assembling the tenth review packet. `Selected-assets` was in the scope enumeration and required nothing: declaring it and listing no asset passed DM-03, so the type named a scope the gate never checked. It now requires a non-empty `included_assets`, symmetric with `Selected-sections`. Disclosed in the packet rather than fixed silently, because the reviewer has twice asked what else is declared and unenforced The backlog count did its job on the same day it was written: rebasing onto main brought a new `docs/governance/` disposition record, and the gate failed with "declares 26 documents but 27 are on disk" -- a count that went stale in hours is exactly the kind of claim that would otherwise have rotted silently. |
| 1.12 | 2026-11-21 | Tenth review, and the reviewer's sharpest finding was structural rather than a single rule: `governed_files` had `inside_repo()`, backlog did not. There were **two** directory walks with **two** skip rules, and they disagreed. A symlinked `docs/` was skipped by the counter, so the declared count was never compared to anything, and skipped by the scanner, so the run reported `0 governed documents` and exit 0 — a count that is never checked and a scan that never happens look identical to a clean result. `scan_root()` is now the single walk, serving both, and every symlink it meets is reported by path instead of dropped. Two more published-but-unread keys fell out of asking the reviewer's question again: `schema_version` was never compared to the gate's implemented version, and `forbidden` was a list DM-08 did not read (it checked a hard-coded key instead). `when` is removed outright: T19 could only verify the rule id, so `== Draft` passed as readily as `== Approved`, which made it prose wearing a constraint's clothes. `schema()` now refuses to load a contract with an unread key, so the class of defect cannot recur silently. `target/` joined `.git` as a structural exception: build output exists in some working copies and not others, and a registry entry would assert it exists on every clone. |
| 1.13 | 2026-11-21 | Eleventh review, five blockers, and two of them were introduced by v1.12 itself. R11-01: "one walk" had not become "one set" — three sources were still concatenated at the call site and nothing enforced uniqueness, so a file reachable two ways was counted twice. R11-02: `is_dir()` follows links, so a top-level symlink satisfied both "on disk" and "declared" and made a registry entry true that pointed outside the repository. R11-03: rejecting unknown key *names* is not enforcement — `required: "false"` is a string and `is True` is False for it, so the field silently became optional; every key is typed now and meaningless combinations are refused. R11-04: DM-08 read a full path from the schema and matched only its last segment, naming locations the author never wrote. R11-05: `governed_files()` discarded the problems from normative-root walks, so a symlinked subdirectory inside `00-governance/` produced no diagnostic at all. Each fix was verified by reverting it and watching the matching case fail; the R11-05 revert reproduces the silent pass (exit 0, `2 governed documents`). |
| 1.14 | 2026-11-21 | Twelfth review, four blockers, and one of them was a defect in v1.13's own fix. R12-01: a node could declare `kind: string` and `fields: {...}` simultaneously — two contradictory statements, with the gate honouring whichever it read first. My first attempt at the fix rejected the real schema, whose structural nodes legitimately say `kind: mapping` beside `fields:` (the same statement twice); the rule is now that children require a mapping kind, not that the combination is forbidden. R12-02: `registry_version` was published and never compared. R12-03: `documents: 27` sat beside "26 architecture documents" in the English reason — a number stated three ways and agreeing twice is the same defect as a rule declared twice and enforced once, and T66 now compares all three. R12-04: `governed_files()` still discarded diagnostics and a comment claiming it was not a verdict entry point is not evidence, so T67 walks the AST of every production script and fails on any call site. Also: an unresolvable path is now a problem rather than a fallback key, and a bilingual mirror that is a symlink is an error instead of looking present. |
| 1.15 | 2026-11-21 | Thirteenth review: **91/100, ACCEPT WITH MANUAL CONTROLS** — "GOV-DOC-002 v1.14 can stand as the final version", with the caveat that final means acceptable to freeze, not exempt from future revision. This version closes its three non-blocking notes and, more importantly, stops claiming more than the gate proves. N13-01: T66 used to check that the machine count and the two prose reasons *agreed*, which left two numbers to keep in step and only noticed after they diverged. `documents:` is now the only place a count may be stated; a reason that restates one is an error. Fewer statements is a stronger guarantee than agreeing statements. N13-02: T67 scanned `scripts/*.py`, which is a rule about a directory rather than about the gate — moving the entry point would have retired it silently. It now walks every production `.py` in the repository (excluding tests and build output) and asserts that scope, so the limit is checked instead of commented. N13-03: `os.walk` swallows errors by default, so an unreadable directory shortened the scanned set with no diagnostic — the tenth review's `0 governed documents, exit 0` arriving by a different route. `scan_root()` now passes `onerror` and T68 proves the callback is wired by injecting the error. Section 9.2 is new: M-01..M-10 are the controls a machine cannot perform, listed by identifier, printed on every run from a single constant (`MANUAL_CONTROLS`), and checked by T69 in both directions against the table — so the run cannot understate what it did not verify, and no future text can quietly claim CI covers these. |
| 1.16 | 2026-11-21 | Fourteenth review: **87/100, REQUEST CHANGES**, one blocker — and the blocker was mine, not the code's. R14-01: section 9.1 still said a backlog count "and its two prose reasons must agree with the disk and with each other", which is precisely the rule v1.15 removed. The implementation, the new table, the change log and the docstring had all moved; the one sentence that described the mechanism had not. A policy that describes the previous mechanism is worse than a vague one, because it is specific and wrong. R14-02 is the more interesting finding: T69 compared two hand-maintained lists, which is the *same shape* as the duplicate count N13-01 had just removed — two authorities plus a synchronisation test. The reviewer's correction is now the design principle: multiple representations are fine when derived from one authority; multiple independently maintained authorities are not. `MANUAL_CONTROLS` is the authority, section 9.2 is rendered from it between markers, and T69 re-renders and compares bytes rather than comparing two lists. R14-03: T68's third case did not fail when `onerror` was removed — I had disclosed that, and the reviewer's ruling is that disclosure is not enough: a test must be named for what it proves. It is now T68c, explicitly an integration case, and a skipped case is reported as skipped instead of recorded as a pass (a `True` for a test that never ran inflates coverage with nothing). T68b2 was added so the diagnostic must name the failing subdirectory, not the root it started from. R14-05: `COUNT_CLAIM_RE` now covers `docs`, `files`, `篇`, `文档`, `文件`, and its coverage gap — spelled-out numbers, omitted nouns — is named in the comment and pinned by T70 as cases, so the comment cannot quietly become false in either direction. R14-06: T67's docstring no longer says it "greps the production scripts"; it states the scan boundary and what the boundary does not prove. |
| 1.17 | 2026-11-21 | Fifteenth review: **78/100, REQUEST CHANGES**. The reviewer read the actual commit rather than my summary, and found that the module docstring still said `MANUAL_CONTROLS` "is the single list; T69 compares it to the policy table in both directions" — the third instance of one defect in this series: implementation moved, the sentence describing the mechanism did not. R15-01 fixed. R15-03 was a real escape hatch: `skip()` was bounded in name only, so `return 0 if passed == total` still returned success when everything was skipped, and `0/0 passed` is arithmetically a pass and evidentially nothing. Skips are now registered in `ALLOWED_SKIPS` with the reason they may skip; an unregistered skip fails the run, and a run with no executed cases fails too. Both are pinned by mutation: an invented skip exits 1, and clearing the results exits 1. R15-04 was the reviewer disagreeing with me and being right. I had listed `twenty-seven documents` as a case that MUST be missed, which does not document a boundary — it licenses a defect. A spelled-out count is still a second statement of the count. Numerals written as words are now caught in English and Chinese (CJK characters are not word characters to `re`, so the Chinese branch carries no ``), and the test's remaining gap is `27 artefacts` / `27 records` — checked as *not detected*, with a case that fails if the vocabulary ever widens without the comment being updated. R15-02/R15-06: T69 now checks the generated block's structure, not only its rows — one BEGIN, one END, order, header and separator, each control once, no second hand-kept table in the section, and the marker itself must not match DM-09's generated-artifact pattern (my first marker said `do not edit by hand` and DM-09 rejected the policy). R15-05: §9.1 said the run prints "the same tuple"; it prints id and control only, and now says so. |
