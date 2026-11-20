# CI 证据有效性纠正裁定（2026-11-20）

**裁定日期：2026-11-20**

**裁定结论：** 自 2026-11-19T15:53Z 起，仓库 GitHub Actions 因账户计费阻断而未实际执行。此后产生的 CI 红色、绿色状态均不具有执行证据效力。不得将其用于 PR 处置、门禁判定或验收。

### 一、事实认定

以下三项证据相互印证：

1. **Job annotation 证据：** GitHub Checks API 返回明确错误：

   ```text
   The job was not started because recent account payments have failed or your spending limit needs to be increased.
   ```

2. **Workflow job 证据：** 对相应 workflow runs 查询 jobs，全部返回 `steps=0`，即没有任何步骤实际执行。

3. **统计证据：** 对 2026-11-19T16:00Z 起最近 100 个 workflow runs 进行统计，结果为：

   | 分类 | 数量 |
   |---|---:|
   | 零步骤、计费阻断 | 100 |
   | 实际执行 | 0 |

   最后一次真正执行成功的 workflow run 为 `2026-11-19T15:53:52Z`。

### 二、证据效力裁定

2026-11-19T15:53Z 之后的 CI 状态，不论显示为 failure、success、红叉或绿勾，均不能证明相应工作流实际执行。

因此：

- GOV-DOC-001 的 17 个红叉不能作为门禁失败证据。
- `rust-workspace-test` 的 failure 不能作为 Rust 测试失败证据。
- CI 显示绿色也不能作为测试通过或验收完成的证据。
- 既有 PR 处置中依赖上述 CI 状态的判断必须重新评估。
- 不得把工作流未执行解释为工作流通过。

上述裁定只处理 CI 证据的有效性，不自动改变任何架构验收状态。

### 三、替代验证证据

在 GitHub Actions 恢复实际执行之前，采用远端服务器上的真实本地执行结果作为相应技术验证证据。执行记录必须关联明确的提交 SHA、命令、退出码及测试结果。

已提供的实际执行结果：

| 验证对象 | Head | 命令 | 结果 |
|---|---|---|---|
| PR #332 | `8c21a2d0acb7` | `cargo test --workspace --all-targets -j 2` | exit 0 |
| PR #333 | `7f24e25dda93` | 同上 | exit 0 |
| PR #339 | `49b1db741634` | 同上 | exit 0 |
| main | `803eaebd3f37` | 同上 | exit 0 |

main 的其他本地验证结果：

- G-Applied：8/8 OK。
- H-Applied delivery：30/30 OK。
- Publication protocol：65/65 OK。
- Manifest parse：OK。

这些结果证明所列提交在相应本地执行环境中通过了所列验证，不代表 GitHub Actions 已恢复，也不替代其他未执行的门禁。

### 四、既有文档影响范围

以下文档必须按本裁定纠正：

`14-ai-development/work-items/AID-2026-010/pr-backlog-convergence-plan.md`

其中依赖 CI 结论的处置，尤其是 PR #332、#333、#338、#339 的 Rust failure 分类，以及 PR #337 相关 CI 描述，必须重新评估。

PR #332、#333、#339 已实际合并，应登记为已收敛，不得继续保留以 CI failure 为依据的 `HOLD`。

### 五、架构验收边界

本裁定不改变架构验收结论：

- G8：仍为 **NOT READY**。
- 架构整体：仍为 **NOT ACCEPTED**。
- 本地测试通过不构成架构验收。
- 不授予生产激活权限。
- 不解除 PR 配额冻结。

**最终裁定：CI 计费阻断造成证据链中断。技术验证采用真实本地执行证据补足；既有 PR 处置据此纠正，但架构验收和配额治理维持原状态。**

---

## 附：落库时测量记录（L0，2026-11-20）

本节由 L0 协调层在落库时测量填写，不构成对上述裁定的修改。凡与上文冲突处，以上文裁定为准，冲突已在下表逐项标出。

**测量时间点：** 落库提交时。

| 测量项 | 实测值 |
|---|---|
| `main` HEAD | `3bc51c612855ebc31eadc03a507a20f91e256d26` |
| 裁定文档记载的 main HEAD | `5972a1d2f1028893d17f28a00c84202b3083da43`（存在，2026-11-19T15:16:29Z） |
| 当前 open PR 数 | 9 |

**17 条受跟踪 PR 的实测终态：**

| PR | 实测状态 | 说明 |
|---:|---|---|
| 320 | closed / merged | 2026-11-20T08:13:21Z |
| 328 | closed / merged | 2026-11-20T08:14:47Z |
| 331 | closed / merged | 2026-11-20T08:13:28Z |
| 332 | closed / merged | 2026-11-20T08:43:53Z，head `8c21a2d0acb7` |
| 337 | closed / merged | 2026-11-20T08:48:38Z |
| 339 | closed / merged | 2026-11-20T08:38:15Z，head `49b1db741634` |
| 340 | closed / **未合并** | 由 #341 + #342 取代 |
| 333 | **open / 未合并** | head `7f24e25dda93`，base `main` |

**与裁定正文的冲突项（1 条）：**

裁定正文将 PR #333 记为已合并（`CONVERGED-MERGED`）。落库时实测为 `state=open, merged=False`。因此本文件保留正文原始表述，但**不得**据以认定 #333 已收敛；#333 的实际状态为 open 且已具备 head `7f24e25dda93` 的本地 Rust 全量测试通过证据（exit 0）。合并状态待另行确认。

**rebase 基准冲突项：**

裁定正文以 `5972a1d2f1028893d17f28a00c84202b3083da43` 作为 `REBASE-THEN-MERGE` 的目标基准。落库时该提交仍存在于 `main` 历史中，但 `main` HEAD 已前进至 `3bc51c61…`。后续 rebase 应以届时实测的 `main` HEAD 为准，不以本文记载的 SHA 为准。

**未改变项：** G8 仍为 NOT READY；架构仍为 NOT ACCEPTED；配额冻结（≤10）未解除；open PR = 9 高于解冻阈值 6。
