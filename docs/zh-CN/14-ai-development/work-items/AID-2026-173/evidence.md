---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-173/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every row was read from the committed checker sources at base f0d881a88f0f70d45e2c67e22fc372a95198c991; the inventory records thresholds that exist and does not claim any gate was executed or that the list is exhaustive beyond the searched files."
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
    canonical_scope: "AID-2026-173 inventory of hardcoded gate thresholds, their definitions and their verbatim violation text"
    canonical_scope_id: "ai-development/aid-2026-173-hidden-gate-threshold-inventory"
    canonical_scope_keywords:
      - gate-thresholds
      - governance-gates
      - bilingual-baseline
      - session-evidence
      - document-metadata
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-173/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-173/evidence.md"
    zh-CN: null
---

# AID-2026-173 —— 写死的门禁阈值清单

**状态：DRAFT —— 只记录。** 本工作项不改任何检查器的判定逻辑、不改任何阈值、不改工作流、不改登记表取值。下表每一行都读自 `f0d881a88f0f70d45e2c67e22fc372a95198c991` 上已提交的源码；本文档记录"现存什么"，不是"应当改成什么"。

## 1. 为什么要这份记录

本仓库有多处门禁把数字写死在代码里，改文档的人在看代码之前看不见它们。报错通常只说哪个路径坏了，很少说那个数字，从不告诉你还有哪些文件必须一起改。于是新接手的 worker 会为一个它根本看不到的常量白掉一轮 check。本清单把这些数字摊开；它与"某个数字是否合理"的判断刻意分开。

## 2. 方法与范围

在 `f0d881a88f0f70d45e2c67e22fc372a95198c991` 上检索：`scripts/**/*.py`（排除测试模块与 `__pycache__`）、`.github/workflows/*.yml`、`00-governance/*.yaml`。首次阅读在 `8722a37b0cd72dc550d99c0eaebe9e7556ce2f95`；这两点之间上述三条路径下共 10 个文件发生变化，均已按 `f0d881a88f0f70d45e2c67e22fc372a95198c991` 重读，其中一处改动了本清单记录的数字（NORMATIVE_ROOTS 由 12 个增至 13 个，见 A2 行）。匹配式：`>= \d+`、`<= \d+`、`== \d+`、`!= \d+`、具名常量（`MAX`/`MIN`/`LIMIT`/`THRESHOLD`）、`len(...)` 比较、集合与计数等值、闭集枚举、日期常量，以及各检查器实际打印的文案。测试模块只用于绑定"某测试断言的数字"（B8 行）。

未检索：`crates/**/*.rs`、`tests/**`、`tools/**`、`experiments/**`、第三方夹具。只存在于这些位置的阈值不在本清单范围内。

计数：**共 56 条 —— BLOCKING 51 条、ADVISORY 2 条、SILENT 3 条。**

- **BLOCKING** —— 越界即该必需 check 变红，或门禁非零退出。
- **ADVISORY** —— 只打印 notice，或只是把日志截短。
- **SILENT** —— 关于这个数字本身什么都不打印：文件不再被读取、配对悄悄翻成 false、job 在有人说话之前就被超时取消。

## 3. 清单

### A. 文档范围登记（GOV-DOC-002，DM-14）

| 编号 | 阈值 | 定义位置（文件:行） | 改什么会触发 | 违反时原文案 | 类别 |
| --- | --- | --- | --- | --- | --- |
| A1 | `docs` backlog 计数 = 27，与磁盘精确等值 | check_document_management.py:2077-2087; 00-governance/document-scope-registry.yaml:83 | 在 `docs/` 下（docs/en、docs/zh-CN 与单独受治理的缺口记录之外）增删任意一个 .md | DM-14 backlog 'docs' declares 27 documents but N are on disk; update the registry | BLOCKING |
| A2 | registry `governed:` 列表 == NORMATIVE_ROOTS（13 个根），集合等值 | check_document_management.py:1990-1998; check_bilingual_docs.py:19-24 | 只在一个清单里声明某个受治理根 | DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [...], enforced-only [...] | BLOCKING |
| A3 | 每个顶层目录必须是 governed、backlog 或 excluded（4 个结构性例外） | check_document_management.py:2000-2034; STRUCTURAL_EXCEPTIONS at :83 | 任何新增顶层目录：node_modules、dist、out、build、tmp、.venv | DM-14 top-level directories not accounted for: [...]. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason | BLOCKING |
| A4 | registry_version == "2"，schema_version == "2" | check_document_management.py:76,80,1914-1920,716-721 | 改了登记表或元数据 schema 的版本而没同步改门禁常量 | DM-14 ... declares registry_version 'X' but this gate implements '2' (schema side: SystemExit) | BLOCKING |
| A5 | backlog 的理由文字不得复述文档数量（数字或数词、英文或中文都不行） | check_document_management.py:1642-1658,1959-1966 | 在 `reason`/`reason_zh` 里写 '27 documents' 或 'twenty-seven docs' | DM-14 backlog 'docs' reason restates a document count [...]; `documents:` is the only place a count may be stated | BLOCKING |
| A6 | governed_files == 恰好 1 条路径，与门禁常量集合等值 | check_document_management.py:56,2055-2069 | 单独把一个文件纳入受治理，或删除 docs/governance/documentation-gaps.md | DM-14 governed_files disagrees with the gate; registry-only [...], gate-only [...] | BLOCKING |
| A7 | docs/en 与 docs/zh-CN 必须是真实目录 | check_document_management.py:2041-2053 | 删除镜像根目录，或用符号链接替代 | DM-14 bilingual mirror directory docs/en is missing (or: is a symbolic link) | BLOCKING |
| A8 | 排除类型闭集 {not-documentation}；reason 与 reason_zh 都必填 | check_document_management.py:67,1968-1981 | 新增 excluded 目录时写 kind: not-yet-migrated，或只写英文理由 | DM-14 excluded 'x' must declare kind one of ['not-documentation'], got 'not-yet-migrated' | BLOCKING |

### B. 双语文档与 prompt 库（GOV-DOC-001）

| 编号 | 阈值 | 定义位置（文件:行） | 改什么会触发 | 违反时原文案 | 类别 |
| --- | --- | --- | --- | --- | --- |
| B1 | 源文件只有含 >=100 个 CJK 统一表意文字才算内嵌双语 | check_bilingual_docs.py:303-309,377-382 | 把只靠 docs/en 配对的 14-ai-development 根文件改短 | Reported indirectly, as a new bilingual gap (B3); the count itself is never printed | BLOCKING |
| B2 | 恰好 31 个必需 prompt 文件（4 个全局 + 9 个 Owner 各 3 个），每个 strip 后 >=250 字符 | check_bilingual_docs.py:852-882 | 加第十个 Owner、改 prompt 文件名，或把某个文件删到 250 字符以下 | Required prompt library file is empty or incomplete: <rel> (or: Required prompt library file is missing: <rel>) | BLOCKING |
| B3 | 冻结的双语缺口基线 = 77 条；只许减少 | scripts/bilingual-baseline.txt; check_bilingual_docs.py:1102-1111 | 在受治理根下新增任何没有 docs/en + docs/zh-CN 配对的 .md | New bilingual gap outside frozen baseline: <path> | BLOCKING |
| B4 | 已修复的缺口必须在同一次改动里从基线删除 | check_bilingual_docs.py:1112-1118 | 给基线里的文件补了镜像，却没改 scripts/bilingual-baseline.txt | Resolved bilingual gap must be removed from scripts/bilingual-baseline.txt: <path> | BLOCKING |
| B5 | PR 正文必须含字面量 BILINGUAL-MANIFEST: COMPLETE | check_bilingual_docs.py:1141,1146-1176 | 改动受治理根下任何 .md，或改动 docs/en、docs/zh-CN 下任何文件 | Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE' or a fully documented 'BILINGUAL-EXCEPTION: APPROVED': <paths> | BLOCKING |
| B6 | EMBEDDED_BILINGUAL_SOURCES 的登记理由必须超过 10 个字符 | check_bilingual_docs.py:159-169 | 编辑登记表时把理由缩成占位符 | EMBEDDED_BILINGUAL_SOURCES has missing or placeholder reason: <source> (exit 2) | BLOCKING |
| B7 | pair 豁免前缀固定为 3 个；13 个受治理根；PARTIAL_SIDE_BY_SIDE_PAIRS 固定为空集 | check_bilingual_docs.py:36-46 | 在 14-ai-development 下新开一个散文子树而没加前缀 | No dedicated message: pairing applies, and the new file surfaces later as B3 | SILENT |
| B8 | 棘轮注释写的 77 必须等于基线里的 77 条，且有测试断言 | .github/workflows/gates.yml:163-166; scripts/ci/test_gate_ratchet.py:114-138; scripts/ci/baselines/bilingual-docs.txt | 改了基线没改注释，或反过来 | gates.yml says N normative paths; <baseline> has M entries | BLOCKING |

### C. 必需 check context 与工作流形状

| 编号 | 阈值 | 定义位置（文件:行） | 改什么会触发 | 违反时原文案 | 类别 |
| --- | --- | --- | --- | --- | --- |
| C1 | 声明的必需 check context = 16 个名字，与平台 payload 集合等值 | check_declared_check_contexts.py:239-269; 14-ai-development/PR-GOVERNANCE-001.md | 重命名必需 job，或在 main 上增删必需 context | main requires 'X', but 14-ai-development/PR-GOVERNANCE-001.md does not declare it (and the reverse) | BLOCKING |
| C2 | 每个声明的 context 必须由某个 job id 或 job name 产出 | check_declared_check_contexts.py:178-206 | 删除或重命名声明块里列出的 job | 14-ai-development/PR-GOVERNANCE-001.md declares required check context 'X', but no job in .github/workflows produces it | BLOCKING |
| C3 | 同一个声明的 context 只能出现一次 | check_declared_check_contexts.py:208-225 | 复制粘贴时把某行写了两遍，而不是补上缺的那行 | 14-ai-development/PR-GOVERNANCE-001.md declares required check context 'X' more than once | BLOCKING |
| C4 | session-evidence.yml 必须保留三个 job id：self-test-trusted-base、self-test-pr-head、validate | check_session_evidence_workflow_shape.py:56,271-281 | 把这三个 job 合回一个，或重命名其中一个 | job id 'X' is missing from .github/workflows/session-evidence.yml; the workflow must keep the three jobs PR #1014 split it into | BLOCKING |
| C5 | 形状键：head job 不得带 ref:，verdict job 不得带 needs:，trigger types 必须含 edited | check_session_evidence_workflow_shape.py:283-303,240-267 | 给 verdict job 加 needs:、给 head checkout 加 ref:，或从 types 删掉 edited | the 'validate' job declares `needs:` ...; the verdict must not depend on another job | BLOCKING |
| C6 | 每个 job 的 timeout-minutes：按工作流为 5、10、30、35、45 | .github/workflows/*.yml (16 occurrences) | 让 job 超过它的超时，例如在 5 分钟的 job 里跑全树扫描 | No checker message: the run is cancelled and the required context never becomes success | SILENT |

### D. 会话证据门禁

| 编号 | 阈值 | 定义位置（文件:行） | 改什么会触发 | 违反时原文案 | 类别 |
| --- | --- | --- | --- | --- | --- |
| D1 | AI 会话证据生效时间 2026-12-01T00:00:00Z；更早创建的 Issue 视为历史 | .github/workflows/session-evidence.yml:21; validate.py:1991-2006,2053-2062 | 生效时刻之后创建的任何 Issue 都必须自带声明 | Issue #N: policy-effective Issue has no declaration | BLOCKING |
| D2 | PR 正文字段无条件必填：Related issue(s)、AI-assisted work、审查身份，以及 3 列的逐 Issue 表 | validate.py:381-409,828-904,912-970,2187-2201 | 用精简过的、删掉字段的 PR 正文开 PR | PR description: missing Related issue(s) / missing per-Issue mapping table | BLOCKING |
| D3 | GitHub compare 最多返回 300 个文件；>=300 一律 fail closed | validate.py:238-242 | PR 触及 300 个及以上路径 | unable to determine changed paths: compare result reached the 300-file limit and may be truncated | BLOCKING |
| D4 | Git tree 被截断时拒绝验证，而不是部分验证 | validate.py:262-280 | 仓库大到递归 tree 调用被截断 | Git tree for <sha> is truncated; refusing partial validation | BLOCKING |
| D5 | 被引用的会话证据 blob 必须大于 0 字节 | validate.py:770-780 | 把一个空的占位文件当证据引用 | raise ValidationError on a zero-size or missing tree entry | BLOCKING |
| D6 | 正文里的每个 SHA 必须是 40 到 64 位十六进制 | validate.py:204-216,2021-2027 | 该填 SHA 的地方填了缩写 SHA 或分支名 | unable to determine changed paths: PR Base SHA is missing or invalid | BLOCKING |
| D7 | 映射表每一行必须解析出 3 个单元格 | validate.py:945-975 | 单元格里含竖线，或整行少一列 | raise ValidationError on a malformed row | BLOCKING |
| D8 | PR 编号必须是正整数 | validate.py:2001-2004 | 触发时没有 PR_NUMBER | PR_NUMBER is missing or invalid | BLOCKING |

### E. 仓库卫生与新文件准入

| 编号 | 阈值 | 定义位置（文件:行） | 改什么会触发 | 违反时原文案 | 类别 |
| --- | --- | --- | --- | --- | --- |
| E1 | 新文件准入白名单：.md/.rst/.adoc、20 个源码后缀、12 个精确配置名、若干具名 YAML 与 JSON 路径 | check_repository_hygiene.py:19-161,244-325,382-396 | 在具名路径之外新增 .txt、.csv、.json 或 .yaml 文件 | new-file admission violation: no allowlist rule for '<path>' | BLOCKING |
| E2 | 仓库根目录的新文件不得以 _ 或 . 开头 | check_repository_hygiene.py:328-342,375-381 | 在仓库根目录加 _pr_body.md 或 .scratch | '<path>' is a root-level underscore/dot file; scratch files do not belong at the repository root | BLOCKING |
| E3 | INDEX.md 每个 work-item 目录恰好一行表格，且双向成立 | check_repository_hygiene.py:419-538 | 加了 work-item 目录却没加表格行，或加了行却没有对应目录 | index membership violation: directory present, no index entry: 14-ai-development/work-items/AID-... | BLOCKING |
| E4 | manifest-schema-registry 里每条排除都必须在提交中仍存在 | check_repository_hygiene.py:803-811 | 删除或重命名一个被列为排除的 manifest | '14-ai-development/work-items/manifest-schema-registry.yaml' excludes N path(s) absent from this commit | BLOCKING |
| E5 | R20-01：status 为 PR_OPEN 时 implementation.pull_request 必须是未加引号的正整数 | check_repository_hygiene.py:853-869 | 写成 pull_request: PENDING 或 pull_request: "123" | manifest consistency violation: '<path>': PR_OPEN requires pull_request to be a positive integer | BLOCKING |
| E6 | R20-02：merge_commit_sha 为 NOT_MERGED 时不得同时出现 MERGED 或 VERIFIED | check_repository_hygiene.py:871-882 | 只改了一个生命周期字段，没改另一个 | manifest consistency violation: '<path>': merge_commit_sha is NOT_MERGED while the lifecycle status asserts merged implementation | BLOCKING |
| E7 | manifest 路径形状是 AID-\d{4}-\d{3}/manifest.yaml，四位年份加三位序号 | check_repository_hygiene.py:72-81,798-801 | 把目录命名为 AID-2026-73 或 AID-173 | No message here: the file is simply never read, so nothing is checked | SILENT |

### F. 需求可追溯（T-01..T-08）

| 编号 | 阈值 | 定义位置（文件:行） | 改什么会触发 | 违反时原文案 | 类别 |
| --- | --- | --- | --- | --- | --- |
| F1 | T-04：同一个 AID 在 INDEX.md 只能出现一次 | check_traceability.py:735-745 | 两次追加动到同一行后 union 合并 | T-04 duplicate INDEX entry <id> | BLOCKING |
| F2 | T-04：已提交的 manifest 必须被索引 | check_traceability.py:786-792 | 提交 work-item 目录却没提交 INDEX 行 | T-04 manifest <path> exists on disk but is not indexed | BLOCKING |
| F3 | T-04：INDEX 里的 id 必须与 manifest 所在目录一致 | check_traceability.py:762-776 | 复制一行只改了部分单元格 | T-04 INDEX id <x> does not match manifest directory <y> | BLOCKING |
| F4 | manifest 与登记表里的 SHA 必须是完整 40 位，包括 base_commit_sha | check_traceability.py:39,818-826 | 写 7 位缩写的 SHA，或漏掉 base_commit_sha | T-06 <id> has no base_commit_sha; historical baseline is ... | BLOCKING |

### G. 文档元数据（GOV-DOC-002，DM-01..DM-13）

| 编号 | 阈值 | 定义位置（文件:行） | 改什么会触发 | 违反时原文案 | 类别 |
| --- | --- | --- | --- | --- | --- |
| G1 | schema_version 必须精确等于 "2" | check_document_management.py:76,713-721 | 改了元数据 schema 却只更新一侧 | SystemExit: 00-governance/architecture-document-metadata.schema.yaml declares schema_version 'X' but this gate implements '2' | BLOCKING |
| G2 | schema 至少要标记 5 个必填叶子 | check_document_management.py:734-738 | 整理 schema 时删掉一个 required 标记 | SystemExit: <schema> marks fewer than 5 leaves required; a classification needs at least the four dimensions' states | BLOCKING |
| G3 | domain、role、lifecycle、authority 四个维度必须都保留声明 | check_document_management.py:216,722-730 | 重命名或合并某个维度 | SystemExit: <schema> no longer declares ['authority']; a schema without the four dimensions cannot describe a classification | BLOCKING |
| G4 | DM-10：approved_version 必须是 40 位祖先提交，正文规范化后必须逐字节不变 | check_document_management.py:1242-1315 | 编辑任何 decision_status 为 Approved 且已钉版本号的文档 | DM-10 content changed after approved_version: approval_applicability ... | BLOCKING |
| G5 | 闭集枚举：13 个 domain、9 个 role、6 个 decision status、4 个 usage status、3 个 canonical status 等 | check_document_management.py:142-171,973-1005 | 在新文档里自造 domain 或 role 取值 | DM-02 <where>.<key>: unknown value ... | BLOCKING |
| G6 | 浅克隆下元数据门禁返回 INCOMPLETE，绝不返回 PASS | check_document_management.py:1209,1280-1290; .github/workflows/document-management.yml:24-26 | 把 document-management 的 checkout 去掉 fetch-depth: 0 | DM-10 <rel>: cannot verify ... on a shallow clone | BLOCKING |

### H. scripts 与 workflows 中其余数值门禁

| 编号 | 阈值 | 定义位置（文件:行） | 改什么会触发 | 违反时原文案 | 类别 |
| --- | --- | --- | --- | --- | --- |
| H1 | AI worker 的 Issue 正文不得超过 20,000 字符 | scripts/ai_worker/prepare_task.py:42 | 任务正文里塞了很长的摘录 | issue body exceeds 20,000 characters | BLOCKING |
| H2 | 格式门禁：cargo 超时 300 秒、git 超时 15 秒、--expect 必须恰好 40 位十六进制 | check_fmt.py:61,95-99,153,267 | runner 变慢，或给 --expect 传缩写 SHA | --expect requires exactly 40 hexadecimal characters (timeout side exits 4) | BLOCKING |
| H3 | 证据文件必须超过 32 字节且内容有意义 | check_status_gates.py:135-168 | 用一行占位文字当证据 | <field> evidence content is too short to be meaningful | BLOCKING |
| H4 | 证据分级：缩进只能是 0 或 2、类到级别的映射、sha256 锚为 64 位 | check-evidence-tiering.py:61-78,99-110,425-432 | 把 DOC_NORMATIVE 声明成 level 2，或用 4 空格缩进 | unsupported indentation 4 / binding.sidecar_anchor=... is not sha256:<64 hex> | BLOCKING |
| H5 | 治理操作登记表：3 个文件各恰好 7 行 x 5 列，本地化表头必须精确匹配 | check_governance_operation_traceability.py:19-33,24,102-110 | 加第八个操作，或改动表头某个单元格的措辞 | <file>: expected 7 operations, found 8 (or: row N has X columns, expected 5) | BLOCKING |
| H6 | 已提交的文本 blob 不得含 CRLF；前 8,000 字节内的 NUL 会把 blob 判为二进制并跳过 | check_line_endings.py:32,1050-1117 | 用 Windows 换行保存文档 | CRLF line endings in committed file '<path>': N CRLF sequences, M total lines | BLOCKING |
| H7 | 分支新鲜度：落后分支只要触及受保护根就失败；路径清单最多打印 20 条 | check_branch_freshness.py:42-44,111-141 | 向前合并了 main，却让某个受治理文档停在旧版本 | branch is N commit(s) behind <base> and touches N guarded path(s); rebase before review so the diff equals the increment | BLOCKING |
| H8 | 交付预检只扫最后 3 个非空行，字符字面量不得超过 12 个字符 | precheck_delivery.py:20-39,53-63 | 在 .rs 文件末尾粘贴工具输出 | Reported as a finding line, not as a gate failure | ADVISORY |
| H9 | 显示上限：10 个散文取值、5 个未分类名、每份清单 20 条分支路径 | check_document_management.py:97,2383; check_branch_freshness.py:119-123 | 无：该上限只缩短日志 | Truncation suffix '... (+N)' with no error | ADVISORY |

## 4. 只在"改了文档"时才触发的门槛

按通常踩到的顺序：

1. **A1** —— 在 `docs/` 下新增一个 `.md`，27 这个计数就偏了，而报错让你去改一张你没打开过的治理登记表。
2. **B3 / B4** —— 受治理根下新增 `.md` 没有镜像，就是新缺口；给已在基线里的文件补镜像，必须在同一次提交里删掉它的基线行。
3. **B5** —— 只要动了 `docs/en`、`docs/zh-CN` 下任何文件，或受治理根下任何 `.md`，PR 正文就必须含字面量 `BILINGUAL-MANIFEST: COMPLETE`。正文在每次 `edited` 事件被重读，所以绿了之后再改正文会重跑门禁。
4. **A3 / A4 / A5** —— 新增顶层目录、登记表版本号、或在散文里写数量，都会让 DM-14 失败，哪怕没有任何一份文档写错。
5. **E3 / F1..F3** —— work-item 目录与它的 INDEX 行是同一个事实的两处表述：行必须有、必须唯一、id 必须指向同一目录。
6. **H6** —— Windows 编辑器写出的 CRLF，门禁拒绝的是已提交的 blob，不是你工作区的文件。
7. **H7** —— 落后的分支只要触及受治理文档就失败，哪怕 diff 本身是对的。

## 5. 本记录不声称什么

- 不判断任何阈值是否正确、过严或过松。任务是记录，不是评判。
- 不声称第 2 节所列路径之外也完整。
- 不把任何一次门禁运行当作证据。所有违反文案都引自 `f0d881a88f0f70d45e2c67e22fc372a95198c991` 的检查器源码；一次运行的输出是另一件带日期的产物。
- 77 与 27 是 `f0d881a88f0f70d45e2c67e22fc372a95198c991` 上的取值，两者都设计成会变；记录这个数字不等于声称它保持不变。

## 6. 复现

```
cd <repo>; git checkout f0d881a88f0f70d45e2c67e22fc372a95198c991
grep -rnE '(>=|<=|==|!=) *[0-9]+' scripts --include=*.py
grep -rn 'MAX_\|LIMIT\|THRESHOLD' scripts .github/workflows 00-governance
grep -rn 'len(' scripts/check_bilingual_docs.py scripts/check_document_management.py \
  scripts/ci/check_repository_hygiene.py scripts/governance/session_evidence/validate.py
grep -c '' scripts/bilingual-baseline.txt
```
