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
        - "14-ai-development/work-items/AID-2026-204/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "记录两道门在 GBK 控制台上的改前/改后实测判定、新增测试，以及本次运行显示必须改编码的文件；不声称 CI 结果，不声称独立评审。"
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
    canonical_scope: "AID-2026-204 locale-independent Git output decoding in the documentation and bilingual gates"
    canonical_scope_id: "ai-development/aid-2026-204-git-output-decode-locale"
    canonical_scope_keywords:
      - git-output-decoding
      - locale
      - gbk
      - dm-10
      - fail-closed
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-204/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-204/evidence.md"
    zh-CN: null
---
# AID-2026-204 — 读 Git 输出的门禁把"解码失败"当成"内容断言失败"

- Work item: AID-2026-204；id_status: PROVISIONAL。
- Attribution: user-authorized operator (delegated by account owner)；date: 2026-11-27。
- base_commit_sha: `4326669caa6c43193d34219a0451b80762b712ff`（建分支时的 `origin/main`）。
- 结论先行：`subprocess(text=True)` 用控制台 locale 解码 Git 输出；GBK 控制台上解码失败，`stdout` 变成 `None`，调用方把"没读懂"当成"不存在"。改后 GBK 控制台与 UTF-8 环境给出同一个判定。
- 本记录不声称任何 CI 结果，也不声称独立评审或 Owner 接受。

## 1. 观察到的事实

### 1.1 根因

`check_document_management.py` 的 `git()` 与 `check_bilingual_docs.py` 的 `_git_log_output()` 都用
`subprocess.run(..., text=True)` 读 Git 输出。`text=True` 的解码器是 **locale codec**：CI 上是 UTF-8，
默认 Windows 控制台（代码页 936）上是 GBK。GBK 解不动 UTF-8 文档时，`subprocess` 的读线程抛
`UnicodeDecodeError`，主线程拿到的 `stdout` 是 `None`。调用方随后把 `None` 解释为"这条 git 子命令没有输出"，
再翻译成"该文件在该 commit 不存在"——一个从未被读取过的历史，被断言成了确定性结论。

同一缺陷在 `check_bilingual_docs.py` 上是崩溃而不是误判：AID-173 worker 的 `git show` 在 GBK 下抛
`UnicodeDecodeError`，`_embedded_sources_in_revision()` 直接 `ast.parse(None)`。

### 1.2 实测（同一棵树，同一台机器）

`git cat-file -e <pin>:<path>` 对 9 条 DM-10 报错涉及的 9 个文件全部返回存在。与缺陷描述一致。

| 树 | 控制台 | 退出码 | `DM-10 … did not exist` | `UnicodeDecodeError: 'gbk'` | 末尾判定 |
|---|---|---|---|---|---|
| `main` @ `4326669c` | 代码页 936（不设 `PYTHONUTF8`） | **1** | **9** | **9** | `FAIL: 9 error(s)` |
| `main` @ `4326669c` | `PYTHONUTF8=1` | 2 | 0 | 0 | `INCOMPLETE`（496 已分类 / 446 未分类） |
| 本分支（改后） | 代码页 936（不设 `PYTHONUTF8`） | 2 | 0 | 0 | `INCOMPLETE`（496 / 446） |

第三行与第二行逐行比对：判定行、计数行、`DM-10 out-of-scope stale bindings: 0` 全部相同；
唯一差异是 advisory 段落里回显正文 `- Status:` 取值时的控制台转码（`main` 的 GBK 与 UTF-8 两次运行之间本来就有同类差异）。
也就是说：改前 GBK 控制台比 CI 多出 9 条错误并崩 9 次，改后两者一致。

## 2. 变更内容

### 2.1 `scripts/check_bilingual_docs.py`（解码原语与主入口）

1. 新增 `GIT_TEXT_ENCODING = "utf-8"`、`GitOutputDecodeError(RuntimeError)`、`decode_git_output(raw, what)`：
   显式按 UTF-8 严格解码，失败时抛出消息含 `decode` 的异常，且不含任何"不存在/内容"措辞。
2. `_git_log_output()` 改为 `capture_output=True` 取字节，再交给 `decode_git_output()`，**不再**用 `text=True`。
3. 其余 6 处读 Git 输出的调用（`rev-parse --is-shallow-repository`、`git status --porcelain`、
   `git diff --name-status`×2、`rev-parse --verify <rev>:<path>`）统一 `encoding="utf-8", errors="replace"`。
4. `main()` 捕获注册历史校验抛出的 `GitOutputDecodeError`，打印 `::error::` 并返回 **2**（INCOMPLETE），
   不再让崩溃冒出去，也不把它降级成内容判定（1）。

### 2.2 `scripts/check_document_management.py`（DM-10 读取路径）

1. `git()` 改为 `capture_output=True` 取字节 + `decode_git_output()`。spawn 失败仍返回 `None`
   （T92a 钉住的既有契约不变），但**解码失败不再返回 `None`**，而是抛出 `GitOutputDecodeError`。
2. DM-10 的两次读取（`rev-parse --verify <pin>^{commit}` 与 `git show <commit>:<rel>`）各自捕获该异常，
   写入既有的 `unanswerable` 通道 → 主流程打印 `INCOMPLETE` 并返回 **2**。
3. `None` / 空输出不再直接等于"不存在"：先问 `git cat-file -s <commit>:<rel>`——
   - 对象不存在 → 保留原判定 `did not exist at approved_version`（退出码 1，断言仍然可用）；
   - 对象存在但读不出（`None`，或空串而字节数不为 0）→ 记为 unanswerable（退出码 2），
     消息写明是解码/读取失败，不冒充"不存在"；
   - 对象存在且大小确为 0 → 空文件是真实可读版本，按空文本参与哈希（与改前一致）。
4. `changed_paths()` 与 `is_git` 探测的解码失败同样走 `::error::` + 退出码 2，不再落进
   "does not resolve to a commit"（退出码 1）的错误分支。

### 2.3 其余读取 Git 输出的门禁

`check_bilingual_docs_full.py`（`git ls-files -z` 解码失败 → 打印 `git output decode failed` 并 exit 2）、
`check_fmt.py`、`check_policy_inheritance.py`、`check_source_revision_pointers.py`、`check_traceability.py`、
`ci/check_branch_freshness.py`、`governance/evidence/check-evidence-tiering.py`（有 `errors="replace"`
但缺 `encoding`，仍是 locale 解码）、`governance/bilingual/check-bilingual-tiering.sh` 内嵌 Python：
统一 `encoding="utf-8", errors="replace"`。

`scripts/governance/status_migration/check_status_gates.py` 是 sidecar 锚定的受保护文件
（`PR272-evidence-hardening.sha256`）。它的 `git log --format=%B` 在本仓库会读到中文提交信息，
GBK 下同样失败：改前跑 `test_status_migration.py` 得到 28 个 `UnicodeDecodeError` 错误。
按该文件自己文档化的流程重新生成 sidecar，并在提交信息里写入新 sidecar 的 SHA-256
（`06ea8d36581b0eeea60c93dbd4a3b8dec216bde2839fe6ba8f6cb7a123389c17`）——这就是它要求的可审计路径，
不是绕过。

### 2.4 测试

1. `scripts/test_check_document_management.py` 新增 `run_git_decode_locale()`：
   - **T95a**：把 approved 版本做成非 UTF-8 blob → 断言退出码 2，输出含 `decode`，且**不含** `did not exist`；
   - **T95b**：反例——pin 指向的提交里确实没有该文件 → 断言退出码 1，消息仍是
     `DM-10 … did not exist at approved_version`。没有这一条，"解码失败不再说成不存在"就可能退化成两种情形都不再说话。
2. `scripts/test_check_bilingual_docs.py` 新增两个用例：非 UTF-8 blob 经 `_git_log_output()` 抛
   `GitOutputDecodeError`（消息含 `decode`、不含 `not exist`）；`main()` 把它报成退出码 2 而不是 1 或 traceback。
3. 受影响的夹具 Git 助手（`test_check_line_endings`、`test_check_repository_hygiene`、`test_check_traceability`、
   `test_check_fmt`、`ci/test_check_branch_freshness`、`governance/bilingual/test_bilingual_scripts`、
   `governance/evidence/test_gate_normative_roots`、`governance/status_migration/test_status_migration`）
   统一 UTF-8 解码，使这些自检在 GBK 控制台上也不再依赖 `PYTHONUTF8`。

## 3. 为什么这不改变任何门禁的通过条件

- **同一判定**：把 locale 解码换成显式 UTF-8，等于把 CI（UTF-8）上既有行为搬到本机。实测第 1 节表格第二、三行逐行相同。
- **失败方向更严，不是更松**：解码失败从"退出码 1 的确定性错误"或"崩溃"变成"退出码 2 的 INCOMPLETE"。
  CI 的 workflow 对 2 与 1 都判红（`document-management.yml` 只特判退出码 3），所以合并门槛没有变低。
- **唯一新增的失败面**：Git 输出确实不是 UTF-8 的情形。改前它在 GBK 上是误判/崩溃、在 UTF-8 上是崩溃；
  改后它在任何环境都是"报告解码失败并停止"。这不是新增规则，是把已有的不确定性说清楚。
- **不触碰**：DM-10 的陈旧审批语义、两份 bilingual 基线的内容、`current_bilingual_gaps()`、任何阈值或 workflow。

## 4. 本地验证（Windows，代码页 936，未设 `PYTHONUTF8`）

| 命令 | 结果 |
|---|---|
| `python scripts/check_document_management.py`（`main` @ `4326669c`） | exit 1，`FAIL: 9 error(s)`，9 条 `did not exist`，9 次 GBK 解码异常 |
| `python scripts/check_document_management.py`（本分支） | exit 2，0 条 `did not exist`，0 次解码异常，`INCOMPLETE`（496 / 446） |
| `python scripts/test_check_document_management.py` | `329/329 passed`，1 个已登记 skip（`T68c`） |
| `python scripts/test_check_bilingual_docs.py` | 17 tests OK（原有 15 + 新增 2） |
| `python scripts/check_bilingual_docs.py`（`BASE_SHA=origin/main`，`HEAD_SHA=本分支`） | 见下表 |
| `python scripts/test_check_line_endings.py` | 17 tests OK |
| `python scripts/test_check_repository_hygiene.py` | 97 tests OK（1 skip） |
| `python scripts/test_check_traceability.py` | 41 tests OK |
| `python scripts/ci/test_check_branch_freshness.py` | 9/9 passed |
| `python -m scripts.governance.evidence.test_gate_normative_roots` | 52 tests OK |
| `python -m scripts.governance.evidence.test_evidence_tiering` | 67 tests OK |
| `python scripts/governance/status_migration/test_status_migration.py` | 26/27 OK。另 1 例 `test_sidecar_anchor_detects_silent_tampering` 在本机**预置失败**：该用例用工作树字节算 sidecar 的 sha256，而 Windows 检出让工作树是 CRLF、提交 blob 是 LF；用 `main` 树的同一用例复跑同样失败。真实 sidecar 锚经 `_verify_sidecar_anchor(repo)` 实测返回 `True`（blob sha256 = 提交信息里的 `06ea8d36…`） |
| `python -m pytest tests/test_check_bilingual_docs_full.py` | 7 passed |
| `python scripts/test_check_fmt.py` | 3 个失败，**与本次改动无关**：夹具用 shell 脚本假冒 `cargo`，Windows 上 `WinError 193`。用 `HEAD` 版本的 `check_fmt.py` 复跑同样 3 个失败 |

`check_bilingual_docs.py` 的实测（GBK 控制台，`PR_BODY` 含 `BILINGUAL-MANIFEST: COMPLETE`）：见第 6 节。

## 5. 未做事项

- 未改任何门禁的通过条件、阈值、基线内容或 workflow；未新增 required context。
- 未改 DM-10 的陈旧审批语义，也未改 `current_bilingual_gaps()`。
- 未处理与本缺陷无关的 `text=True` 调用（例如跑 `python`/`cargo` 子进程并读其 stdout 的位置），
  它们的输出不是 Git 输出，不在本 Work Item 的范围。
- 未做独立评审（`review.status = NOT_ASSIGNED`），未关闭或修改任何 Issue。

## 6. `check_bilingual_docs.py` 实测（区间 `4326669c...f85257df`）

GBK 控制台，未设 `PYTHONUTF8`，`BASE_SHA=4326669c…`、`HEAD_SHA=f85257df…`、`PR_BODY` 含 `BILINGUAL-MANIFEST: COMPLETE`：

| 脚本版本 | 退出码 | 结果 |
|---|---|---|
| 改前（`4326669c` a.k.a. `main` 的 `check_bilingual_docs.py`） | 1 | `AttributeError: 'NoneType' object has no attribute 'strip'`，栈顶 `_embedded_sources_in_revision()` ← `_git_log_output()`：`git show` 解码失败使 `stdout` 为 `None`，随后 `.strip()` 崩溃。这正是 AID-173 worker 撞到的那处 |
| 改后 | 0 | `bilingual baseline: 77 frozen, 0 new gaps`；`exemptions: 21`；`PASS (29 changed paths inspected)`；附 `NOTE: 2 changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked` |

同一区间在 UTF-8 环境下的输入字节不变，因此 CI 上的判定不变；改前之所以在 GBK 上崩溃，只取决于本地解码器。

