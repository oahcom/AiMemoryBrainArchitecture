# GAP-15 — 合并前没有任何环节执行 `cargo fmt --check`，因此它每小时坏两次

**状态：** 开放 — 实测，非推测
**领域：** CI / 工程门禁
**严重度：** 单次低，按频次高
**实测于：** `main @ caa37a7e`，2026-11-22 03:30 UTC

## 1. 观测事实

十五分钟内，两个不同提交、两个不同 crate，各把一处 fmt 回归送进 `main`：

| 提交 | 文件 | 谁发现 | 谁修 |
|---|---|---|---|
| `c1e0dcdb` | `crates/memory-event-store-sqlite/src/lib.rs`（277、479 行） | 我，为另一个无关 PR 跑 `--check` 时 | #572（`78985c6c`） |
| `#566` | `crates/brain-cli/tests/e2e_full_chain.rs`（12、43 行） | 我，又一次，同样无关 | #577 |

两处都不是合并前发现的。两处都只是因为有人在验证别的东西时顺手跑了 `cargo fmt --all -- --check`。

## 2. 为什么现有 workflow 拦不住

`.github/workflows/rust-phase1.yml` 是唯一在 `crates/**` 的 `pull_request` 上运行的 workflow，它只跑一条命令：

```yaml
- run: cargo test --workspace --all-targets
```

`cargo test` 不检查格式。编译通过、测试全绿而格式是红的，workflow 照样通过。

## 3. 而且它根本不会运行

相关 head 上的四次 check run 带着同一条注解，逐字如下：

> The job was not started because recent account payments have failed or your spending limit needs to be increased.

所以连唯一有可能拦住回归的 workflow 也不在执行。`GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` 返回 `403 — Upgrade to GitHub Pro or make this repository public`，因此也无法配置 required status check。

**门禁缺了两层**：命令不在 workflow 里，workflow 也不在跑。

## 4. 真正能修的是什么

两层，互相独立，先做便宜的。

**第一层 — 现有 workflow 里加一行。**

```yaml
- run: cargo fmt --all -- --check
```

放在 `cargo test` 之前，遇到格式差异约 5 秒内失败。零成本，不新增文件。Actions 计费恢复的那一刻起生效。

**第二层 — 一条不依赖 Actions 的合并前检查。**

仓库已有这个先例：`scripts/precheck_delivery.py` 是 stdlib-only 的检查器，手动对 Rust 源文件运行。加一个同类的 `scripts/check_fmt.py`，内部调 `cargo fmt --all -- --check` 并以非零退出，合并者就能在 `PUT /pulls/{n}/merge` 之前跑一条命令。

在现状下这一层比第一层更重要，因为第一层执行不了。

## 5. 我不做什么

本 work item 不实现上述任何一层。两者都是 CI/治理变更，而仓库自己的规则是：会话不得凭自身权限新建强制门禁（见 `#305` 先例：会话级裁决不能凌驾已采纳的治理工具，工具也不得扩张出声明范围）。带实测地登记缺陷在范围内；决定「此后每次合并都需要一项新检查」不在。

不需要任何权限就能断言的是：**截至 `caa37a7e`，`main` 的 fmt 是红的，而我是手工修了两次，不是靠门禁。**

## 6. 复现

```sh
curl -sL https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/tarball/caa37a7e | tar xz
cd oahcom-AiMemoryBrainArchitecture-*/
cargo fmt --all -- --check     # 退出 1，crates/brain-cli/tests/e2e_full_chain.rs 两处 diff
```

## 7. 关闭标准

1. `rust-phase1.yml` 在 `cargo test` 之前包含 `cargo fmt --all -- --check` 步骤。
2. 存在一条非 Actions 路径，合并者能用一条命令运行，且合并流程里点名它。
3. 连续一周没有 fmt-red 的提交进入 `main`。
