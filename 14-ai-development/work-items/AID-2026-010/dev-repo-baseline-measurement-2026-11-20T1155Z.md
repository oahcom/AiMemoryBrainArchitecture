# 开发仓库实测：可构建、可测试，F1 操作级证明在代码中被显式标为未实现

测量时点 `2026-11-20T11:55Z`，执行环境 remote-43（`ubuntu@43.138.133.238`），`cargo 1.100.0`。

本文件由 L0 协调层测量填写，只提交测量事实与复现步骤。是否据以改变 F-43-01/F1、G8 或开发准入状态，由 A 与相应 Owner 裁定。

## 一、开发仓库基线

| 项 | 值 |
|---|---|
| 仓库 | `oahcom/AiMemoryBrain` |
| 默认分支 | `main` |
| `main` HEAD | `341bb04b3c531a941d792ec0f50c14a7e793a1bf` |
| 分支数 | 2（`main`、`ai/REQ-REUSE-2026-11-19-001/tech-lead-governance-gaps`） |
| 提交数（main） | 8 |
| 最近推送 | `2026-11-20T09:26:15Z` |
| 工程根 | `AiMemoryBrain/`（Rust workspace） |

## 二、工程结构

```
AiMemoryBrain/
  Cargo.toml          clap 4.5.53 / serde 1.0.228 / serde_json 1.0.145
                      sha2 0.10.9 / unicode-normalization 0.1.24 / toml 0.9.8
  Cargo.lock
  build.rs            fail-closed UCD 15.1.0 锁校验
  src/
    authority.rs      D 权威接口
    d_predicates.rs
    lib.rs
    lockfile.rs
    normalization.rs  NFC/NFD 规范化
    receipt.rs        Receipt 结构
    ucd.rs            UCD 15.1.0 数据
    version.rs
    bin/d-ucd-lockgen.rs
    bin/d-ucd-validate.rs
  tests/
    d_normalization_vectors.rs
    f1_scenarios.rs
    normalization_conformance.rs
    scenarios/
    vectors/
  governance/
    N01-reuse-first-principle.md
    N06-risk-tiered-decision-depth.md
    decisions/DEC-RD-2026-11-20-001.md
```

## 三、构建与测试实测

命令：`cargo test --workspace --all-targets -j 2`（`CARGO_TARGET_DIR=/home/ubuntu/cargo-tgt/aid2026`）

**退出码 `0`。**

| 测试目标 | 结果 |
|---|---|
| `src/bin/d-ucd-validate.rs`（unittests） | 0 passed, 0 failed |
| `tests/d_normalization_vectors.rs` | **0 passed, 0 failed, 1 ignored** |
| `tests/f1_scenarios.rs` | **0 passed, 0 failed, 3 ignored** |
| `tests/normalization_conformance.rs` | **1 passed, 0 failed**（0.54s） |

有效通过测试：**1 个**（`validates_complete_locked_unicode_15_1_0_normalization_corpus`）。

## 四、关键事实：F1 操作级证明在代码中被显式标注未实现

`tests/f1_scenarios.rs` 的三个测试全部带 `#[ignore]`，理由字符串为：

```
Step 2 implementation pending
```

| 测试名 | 标注 |
|---|---|
| `all_ten_scenarios_are_defined_and_clause_mapped` | `ignored, Step 2 implementation pending` |
| `real_authority_and_receipt_are_required_for_operational_proof` | `ignored, Step 2 implementation pending` |
| `test_double_cannot_satisfy_operational_proof` | `ignored, Step 2 implementation pending` |

`tests/d_normalization_vectors.rs` 同样被 ignore（`Step 2 implementation pending`）。

这三个被 ignore 的测试名恰好覆盖 F-43-01/F1 关闭条件所需的语义：场景定义与条款映射、真实 authority/receipt 要求、test double 不得满足操作级证明。**它们存在但未启用**，与 ledger 中 F1 `OPEN (implementation evidence)`、`Five operational D authority operations: NOT IMPLEMENTED`、`seven canonical D-002 scenarios S1–S7: NOT RUN` 的记录一致。

## 五、与开发准入的关系

`development-readiness-register.md` §4 记载：

> F1 remains OPEN because no real D-authoritative callback exists. **Building the integration boundary can proceed**; claiming operational proof cannot.

实测支持这一区分：

- **可继续**：工程可构建（exit 0）、依赖已锁定、UCD 15.1.0 一致性语料通过、fail-closed `build.rs` 生效。基线工程质量成立。
- **不可声称**：`cargo test` 的 exit 0 **不构成** F1 操作级证明。有效通过仅 1 个测试，F1 三个场景测试处于 ignore 状态。把 exit 0 读作「F1 已验证」是错误解读。

## 六、复现步骤

```
ssh ubuntu@43.138.133.238
export PATH=/home/ubuntu/.cargo/bin:$PATH
export CARGO_TARGET_DIR=/home/ubuntu/cargo-tgt/aid2026
cd /home/ubuntu/ai-projects/AiMemoryBrain/AiMemoryBrain
git rev-parse HEAD                 # 341bb04b3c53...
cargo test --workspace --all-targets -j 2
```

判据：`exit 0` 且 `tests/f1_scenarios.rs` 报告 `3 ignored`。

## 七、记录边界

本记录只提交测量事实与复现步骤。据以关闭 F-43-01/F1、变更 G8、或宣布开发阶段进入下一里程碑，均超出 L0 职责。
