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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every run id, head SHA, runner name and step conclusion in this register was read from the GitHub Actions REST API in this session. No figure is carried over from another register. The register claims no approval and no independent review."
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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/governance-register/GOV-NC-2026-11-23-EXECUTION-RESTORED-029.md"
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-23-EXECUTION-RESTORED-029.md"
    zh-CN: null
---

# GOV-NC-2026-11-23-EXECUTION-RESTORED-029 — 执行侧已恢复，005 的现在时断言与两条工作流注释随之失效

- 登记编号：GOV-NC-2026-11-23-EXECUTION-RESTORED-029
- 状态：`OPEN` / `MEASUREMENT_ONLY` / 平台能力已恢复，引用该前提的文档尚未更正
- 测量时间：2026-11-23T10:40Z
- 测量基点：`main = 20902c48`（取数期间 main 从 `68fa85a4` 推进至 `20902c48`，下列 run 均已记录 head SHA，不依赖 `main` 的当前位置）
- 前置登记：`GOV-NC-2026-11-20-CI-NOT-EXECUTED-005`（零执行窗口）、`GOV-NC-2026-11-21-GATE-CLOSURE-020`（§5 反向断言）、`GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023`（§5 第 1 项）
- 作者：owner-proxy 会话。**不是**独立审查者，**不是** accountable owner。

---

## 1. 结论先行

登记 005 记录了一个历史窗口：36 小时内门禁逻辑执行 **0 次**。那个窗口的事实不因本登记改变。

但 005 的**状态行是现在时**（「执行侧完全缺失」），而多条现存文档把这一状态当作当前事实引用，并据此做出了**仍然生效的设计决定**。截至 2026-11-22T15:15:13Z，这个前提不再成立：

| | 首次真实执行 | run | head | runner |
|---|---|---|---|---|
| 自托管 | 2026-11-22T10:17:02Z | `45011672799` | `550bb864` | `zesu-x64` |
| GitHub 托管 | 2026-11-22T15:15:13Z | `45037267638` | `38c3c975` | `GitHub Actions 1000005167` |

两条都执行到了 `cargo test --workspace --all-targets` 并返回 `success`。GitHub 托管那条还执行了 `cargo clippy --workspace --all-targets -- -D warnings` 与 `check_fmt.py`。

因此本登记不是「005 有误」，而是「005 的现在时部分已过期，而依赖它的现在时判断没有随之更新」。

---

## 2. 已支付的对价，与它现在覆盖了什么

`ci-gates-and-ratchets.en.md` §2.3 与 `.zh-CN.md` 同名小节，为「`gates.yml` 的 `clippy` Job 为什么只跑 clippy、不跑 fmt 与测试」给出的理由是：

> `cargo clippy --workspace --all-targets -- -D warnings` is kept because it is genuinely uncovered: `rust-phase1.yml` has clippy, but it is `runs-on: ubuntu-latest`, which on this account is allocated no runner at all, so **it has never executed**. Clippy is the independent value of this job.

（`clippy` 保留，因为它是真正无人覆盖的：`rust-phase1.yml` 有 clippy，但它 `runs-on: ubuntu-latest`，本账户下分配不到 runner，因此**从未执行过**。clippy 就是这个 Job 的独立价值。）

这句话的前半段曾经为真，因此「重复执行是亏本交易」的结论曾经成立。现在前提反转：`rust-phase1.yml` 的 clippy 已经执行，而且**在同一个提交上与 `gates.yml` 的 clippy 同时执行**。

实测（同一提交、同一命令、两次成功）：

| 提交 | `gates.yml` clippy | `rust-phase1.yml` clippy |
|---|---|---|
| `d238dd4a` | `success` | `success` |
| `0dc8f5a2` | `success` | `success` |

反例说明这不是「两边一致所以无所谓」：`6b97a659` 上 `gates.yml` 的 clippy Job 在 `actions/checkout` 就失败、clippy 步骤 `skipped`，而同一提交的 `rust-phase1.yml` clippy `success`。同一条命令在两个工作流上给出了不一致的可用性，说明它们不是同一件事的两份拷贝，而是一份可用、一份依赖一条更脆弱的前置。

**本登记不主张立刻删除 `gates.yml` 的 clippy Job。** 删除会把这件事从「两条腿」变成「一条腿依赖计费状态」，而计费状态在 11-22 之前刚刚失败过一次。本登记主张的是：那段注释已经不能作为理由，它现在描述的是**刻意的冗余**，不是「唯一覆盖」。这两种状态需要不同的取舍，而取舍不是注释问题。

---

## 3. 被反证的第二条：前置门禁的可行性条件

`gates.yml` 头部注释写道：

> Pre-merge gating needs one of: GitHub-hosted minutes restored, a second runner, or a relaxed L1/L2 policy — each an Owner decision, not an edit here.

（前置门禁需要三者之一：GitHub 托管分钟恢复、第二台 runner、或放宽 L1/L2 策略——每一条都是 Owner 决定，不是在这里改文件能解决的。）

第一项已经满足。而且不需要新工作流：`rust-phase1.yml` 本身就以 `pull_request` 为触发条件，路径过滤为 `Cargo.toml` / `Cargo.lock` / `crates/**` / `scripts/check_fmt.py` / 自身，运行在 GitHub 托管 runner 上。

实测：run `45155022673`，`2026-11-23T10:19:21Z`，head `72cc25fe`，event `pull_request`，runner `GitHub Actions 1000005710`，步骤 `check_fmt` / `clippy` / `cargo test --workspace --all-targets` 三步全 `success`。

**结论：本仓库现在有可用的 Rust 前置门禁**，覆盖 `crates/**` 的 PR。这不是我新增的能力，是既有工作流在计费恢复后自然开始工作。`gates.yml` 的「无法前置设卡」仍然为真——它是自托管 + L1/L2 限制的结果，与本条无关；被反证的是「前置门禁在本账户下不可达」这个更大的判断。

这条有直接后果：AID-2026-052 / AID-2026-053 的工作令都写着「工作区测试属于 CI，本地多 GB 的 `target/` 不是贡献」。在该判断仍为假时，这句话是**空头承诺**——CI 不会跑。现在它成立了，而且是通过一条会读到 `crates/**` 改动的前置路径成立的。

---

## 4. 第三条：`gates.yml` 在 `main` 上的裁决覆盖

推送触发的 `gates.yml` run，最近 73 个的结论分布：

| 结论 | 数量 |
|---|---|
| `failure` | 31 |
| `cancelled` | 23 |
| `success` | 18 |
| `queued` | 1 |

`cancelled` 不是失败，也不是通过——它**没有裁决**。成因是 `gates.yml` 的并发组：单 runner 意味着串行，GitHub 每个组只保留一个运行中 + 一个待运行 run，突发推送时较旧的待运行 run 被取消。

因此 `main` 上约 31%（23/73）的推送没有得到 `gates.yml` 的任何结论。这与 005 记录的是**同一类缺陷的不同成因**：005 是「run 存在但步骤未执行」，这里是「run 被取消，连步骤都不会有」。两者的治理含义相同——那段提交没有任何自动化结论——但只有一个被登记过。

---

## 5. 需要更正的地方（本登记不代为更正）

| 文件 | 位置 | 断言 | 现状 |
|---|---|---|---|
| `14-ai-development/ci-gates-and-ratchets.en.md` | §2.3 | `rust-phase1` "has never executed" | 已假 |
| `14-ai-development/ci-gates-and-ratchets.zh-CN.md` | §2.3 | 「因此从未执行过」 | 已假 |
| `.github/workflows/gates.yml` | 头部注释、clippy Job 注释 | `ubuntu-latest` 分配不到 runner | 已假 |
| `.github/workflows/rust-self-hosted.yml` | 头部注释 | 托管分钟因计费失败被封 | 已假 |
| `GOV-NC-2026-11-20-CI-NOT-EXECUTED-005` | 状态行 | 「执行侧完全缺失」 | 窗口内为真，现在时为假 |
| `GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023` | §5 第 1 项 | "CI has never executed a test" | 已假 |
| `GOV-NC-2026-11-21-GATE-CLOSURE-020` | §5 | 「不主张 CI 执行过」 | 该轮测量的限定语，历史为真；不得再作为现状引用 |

前两条与工作流注释是**现在时**断言，读的人会当作当前事实，应当更正。005 与 023 是**带测量点的历史登记**，其正文不应改写；应当补一条带日期的附注指向本登记，而不是把「从未」改成「曾经」。

`gates.yml` 与 `rust-self-hosted.yml` 是工作流文件。本登记不修改它们——注释更正与 Job 去留是两件事，而后者需要一次关于计费依赖的取舍。

---

## 6. 本登记不主张什么

- **不主张 005 的统计有误。** 那 36 小时里门禁逻辑确实执行 0 次，本登记不改变该窗口的任何计数。
- **不主张门禁现在可信。** 执行了不等于通过，通过了不等于覆盖充分。§4 的 23 个 `cancelled` 就是「执行侧可用」与「裁决侧可靠」之间的差距。
- **不主张应当删除重复的 clippy。** 见 §2 末段。
- **不主张恢复是永久的。** 计费状态在 11-22 之前刚失败过一次；本登记记录的是一个时间点的事实，并明确它可能再次反转。任何依赖「CI 会跑」的授权都应当写明这一点。
- **不主张本次测量经过独立复核。** 全部数字来自 GitHub Actions API 的只读查询，任何人都可复现，但复现者不是独立审查者。

---

## 7. 复现

对任一 run，读取 `/repos/{repo}/actions/runs/{id}/jobs` 的每个 job 的 `runner_name` 与 `steps[].conclusion`：

```text
runner_name == ""            -> 未分配 runner（005 的第 3 层）
steps == []                  -> 未执行任何步骤（005 的第 4 层为 0）
steps[*].conclusion == skip  -> 该步骤未执行，其所属 job 的 failure 不是实质门禁失败
run.conclusion == cancelled   -> 无裁决（本登记 §4）
```

本登记引用的 run id 全部列在 §1、§2、§3、§4 的表格中，可直接重查。
