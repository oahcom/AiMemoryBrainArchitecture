以人类 Owner 身份授权：为本次实施正式登记仓库标准 Work Item，解除 Session Evidence Gate 的阻塞。

要求：
1) 按仓库编号规则取下一个可用 AID（先查重，不得复用或伪造已有编号），为 `SOURCE-RESTORE-02` 与 `DECISION-ACCEPTANCE-03` 建立 Stage 0 注册与 manifest，并更新 INDEX；
2) 把外部工作流编号（`AID-2026-11-26-…`）保留为证据引用，不作为仓库标准 ID；
3) 提交到 PR #1220 同一分支，重新触发 Session Evidence Gate；
4) 回报：分配到的标准 Work Item ID、改动路径、CI 最新结果、剩余阻塞。
不合并、不部署、不关闭 Issue、不修改 validator 逻辑。