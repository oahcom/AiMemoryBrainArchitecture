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
        - "14-ai-development/work-items/AID-2026-192/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "按收到时的原样记录合同、执行环境以及 evidence.md 中引用的命令输出。没有可用的平台会话标识，因此会话身份记为 NOT_RECORDED，不作推断。"
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

# Session Evidence — AID-2026-192

## Session role / use case

在派发合同内执行的实现 worker。合同由两个任务文件组成：`fix-brief-common.md`（取号、work
item 结构、元数据、PR 正文、合并纪律）与 `unit-gates-b.md`（三个门禁缺陷及其修改要求），
被要求端到端执行、不提问、只在指定 worktree `D:\code\wt-gates-b` 内作业。

实际承担的角色是：读合同 → 复现缺陷（用 `origin/main` 的旧文件实测，而不是从代码推断）→
修改三个助手与三个测试文件 → 以"单独回退某处修复后新用例必须失败"的方式验证用例可推翻 →
补 work item 文档 → 提交、开 PR、等待 16 个 required context、合并、比对 blob。

## Actual AI input

合同以两个文件的形式到达，逐字收录在 `prompt-v1.md` 中，并要求：

- 读 `fix-brief-common.md` 与 `unit-gates-b.md` 并端到端执行，不要提问；
- 只在 worktree `D:\code\wt-gates-b`、分支 `fix/2026-11-27-gates-b` 内作业；
- 修改 `check_index_membership` 的 fail-closed 行为、两处 workflow glob（`*.yml` + `*.yaml`）、
  YAML 解析前剥注释、以及 `check_test_reachability` 的 Rule B 注释问题；
- 补测试：`jobs: # comment` 夹具不得判通过、`.yaml` 文件会被读到、注释里的测试名不计入
  Reachable；
- 跑 `check_repository_hygiene.py` 与 `check_declared_check_contexts.py` 记录前后输出（应为
  16 declared / 16 produced 不变）；
- 禁止项：不新增 required context、不改 job 名、不放宽任何判定。

执行环境为中文本地 Windows 主机、Python 3.12.3、`PYTHONUTF8=1`；仓库为
`oahcom/AiMemoryBrainArchitecture` 的克隆，分支基点 `origin/main` =
`2f4f4118bd2c2d8e43a23975f667deeb06553f3c`（先按合同并入 origin/main 再作业）。

## AI-visible output

对执行会话可见的输出，按出现顺序：

1. 三个门禁的改前输出（在 `origin/main` 的 detached worktree 上）：
   `Work-item index membership version=2026-11-24.8 directories=106 linked=106`、declared 16 /
   produced 16、`65 test files, 65 reachable`、三个测试套件 `97 / 24 / 13` 全绿。
2. 缺陷实测：`produced_contexts` 对 `jobs:  # comment` 夹具返回 0 个 context（改后 3 个）；
   只含 `.yaml` workflow 的树 exit 2（改后 0）；注释中的测试名使 Rule B 报 exit 0（改后
   exit 1）；`check_index_membership` 对无目录树返回 `[]`（改后抛 `RuntimeError`）。
3. 修改后同一批命令的输出：`version=2026-11-27.1 directories=106 linked=106`、declared 16 /
   produced 16、`65 test files, 65 reachable`、套件 `99 / 27 / 16` 全绿。
4. 回退验证：单独回退每处修复，失败的恰好是对应的新用例（详见 `evidence.md` §7）。
5. 首轮全量跑测试时 97 个用例中 65 个失败，全部是同一原因——共享夹具缺少成员关系两侧，
   这正是本次修复要消灭的静默通过；夹具补齐后全绿。

未产生、也未声称：任何 CI context 结果、任何合并 SHA、任何平台会话标识。
