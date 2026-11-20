# F-43-02 阻塞前提证伪与证据独立复现（L0 测量记录）

**记录日期：** 2026-11-20
**记录角色：** L0 协调层（机械测量，不作架构裁定、不作 Owner 决定）
**仓库：** `oahcom/AiMemoryBrainArchitecture`（记录） / `oahcom/AiMemoryBrain`（被测对象）
**被测 HEAD：** `341bb04b3c531a941d792ec0f50c14a7e793a1bf`

---

## 一、被证伪的既有裁定前提

`A-OWNER-INTEGRATION-R42-2026-11-19` 对 F-43-02 作出 `BLOCKED（实现目标未授权）` 裁定，其核心事实依据原文为：

> `oahcom/AiMemoryBrain` 当前仍为空仓且无分支

**该前提在本次测量时点已不成立。**

| 测量项 | 实测值 |
|---|---|
| 仓库可见性 | 可读，`private=false` |
| 默认分支 | `main` |
| 分支数 | 2（`main`、`ai/REQ-REUSE-2026-11-19-001/tech-lead-governance-gaps`） |
| `main` 提交数 | 8 |
| `main` HEAD | `341bb04b3c531a941d792ec0f50c14a7e793a1bf` |
| 最后推送 | 2026-11-20T09:26:15Z |
| open PR | 0 |
| open Issue | 0 |

`main` 提交序列（最新在前）：

```text
341bb04b 2026-11-20T09:26:15Z feat(governance): land N-01 reuse-first and N-06 risk-tiered decision depth (#1)
ff1b72a1 2026-11-20T09:21:46Z feat(governance): land N-01 reuse-first and N-06 risk-tiered depth
bb1420b3 2026-11-20T06:23:39Z feat(aid-2026-022): batch2 item5 — bind normalizer to Cargo.lock digest and resolved version
d1771520 2026-11-20T05:58:08Z feat(aid-2026-022): batch2 item4 — full Unicode 15.1.0 conformity evidence
c994abcd 2026-11-20T05:49:27Z feat(aid-2026-022): batch2 item3 — fail-closed build.rs UCD lock verification
1f85b286 2026-11-20T05:46:20Z feat(aid-2026-022): batch2 item2 — deterministic UCD 15.1.0 lock generator
db94086c 2026-11-20T05:10:37Z feat(aid-2026-022): batch2 normalization.rs — NFC/NFD normative relation
d11722e3 2026-11-20T04:51:58Z feat(aid-2026-022): Step-2 batch 1 — lockfile/version/ucd core modules
```

仓库内容（`main` 树）：

```text
AiMemoryBrain/
  Cargo.toml, Cargo.lock, build.rs, LICENSE, THIRD-PARTY-NOTICES
  src/  authority.rs, d_predicates.rs, lib.rs, lockfile.rs,
        normalization.rs, receipt.rs, ucd.rs, version.rs
  src/bin/  d-ucd-lockgen.rs, d-ucd-validate.rs
  tests/  f1_scenarios.rs, normalization_conformance.rs,
          d_normalization_vectors.rs,
          scenarios/f1-dual-high-water-scenarios.yaml,
          vectors/d-normalization-vectors.json
  ucd/15.1.0/  UnicodeData.txt (1914200B), NormalizationTest.txt (2625136B),
               DerivedNormalizationProps.txt (1355530B),
               CompositionExclusions.txt (8888B),
               ucd-lock.json, derived/normalization-index.json
  governance/  decisions/DEC-RD-2026-11-20-001.md,
               N01-reuse-first-principle.md, N06-risk-tiered-decision-depth.md
```

因此 R42 所列解阻条件中的「指定现有工程仓库、分支、validator/build 路径」在事实上已存在可核验载体。本记录只陈述该事实，**不**裁定授权是否成立——授权归属 Product/Platform Architecture responsibility holder 与 A，不属 L0。

## 二、AID-2026-027 所引证据的独立复现

`AID-2026-027` 据以将 F-43-02 判为 CLOSED 的证据，本次在远端 43 服务器以全新 `CARGO_TARGET_DIR` 独立复跑。

**环境：** `cargo 1.100.0 (3acc79c0c 2026-11-05)`，`CARGO_TARGET_DIR=/home/ubuntu/cargo-tgt/aid022`。

**正向（`cargo test -j 2`，HEAD `341bb04b`）：** 退出码 0。

| 测试目标 | 结果 |
|---|---|
| lib 单元测试 | 24 passed / 0 failed |
| `tests/d_normalization_vectors.rs` | 3 passed / 0 failed |
| `tests/normalization_conformance.rs` | 1 passed / 0 failed |
| `tests/f1_scenarios.rs` | 0 passed / 3 ignored（`Step 2 implementation pending`） |
| doc-tests | 0 |
| **合计** | **28 passed / 0 failed / 4 ignored** |

构建脚本输出：`warning: d_unicode_validator@0.1.0: UCD 15.1.0 lock verified: 4 files, payload SHA-256 b62c0cd588e8`。

与 `AID-2026-027` 记载的「28 passed / 4 ignored」**完全一致**。

**锁绑定实测：**

| 项 | 实测值 |
|---|---|
| `Cargo.lock` SHA-256 | `a697d9051dc486f9707b1f1dd20f135ca922628805dcecf46a9e41078f751f24` |
| `ucd-lock.json` → `payload.normalizer.cargo_lock_sha256` | `a697d9051dc486f9707b1f1dd20f135ca922628805dcecf46a9e41078f751f24` |
| `payload.normalizer.crate_name` | `unicode-normalization` |
| `payload.normalizer.crate_version` | `0.1.24` |
| `Cargo.lock` 实际解析版本 | `unicode-normalization 0.1.24` |
| `payload.unicode_version` | `15.1.0` |
| `payload_sha256` | `b62c0cd588e863cf1294e06cbfbd943f3a89594be0aa3f72e79c1a9848948824` |

两项 digest 逐字符相同，锁定版本与解析版本一致。

**负向（伪造 `cargo_lock_sha256` 并重算 payload digest，使只有绑定检查可能触发）：** 构建退出码 **101**，`build.rs:185` panic：

```text
payload.normalizer.cargo_lock_sha256: expected 0000000000000000000000000000000000000000000000000000000000000000,
actual a697d9051dc486f9707b1f1dd20f135ca922628805dcecf46a9e41078f751f24
```

期望值即伪造值，实际值即真实 `Cargo.lock` digest，证明校验读取的是真实 lock 字节而非自证字段。负向测试后文件已还原，`git status` 干净，HEAD 未变。

**排除项复核：** 此前「对 `Cargo.lock` 追加注释」的负向测试因 Cargo 规范化 lock 文件而不成立，`AID-2026-027` 已明确排除。本次改用伪造 payload 字段并重算 digest 的方式，绕开该缺陷，结论成立。

## 三、由此产生的待裁定事项（不属 L0）

以下事项需由相应权威裁定，L0 不作判断：

1. **R42 前提失效的处置：** R42 的 `BLOCKED` 建立在「空仓」事实上。该事实已不成立。是由 A 重开 F-43-02 状态、还是以新裁定取代 R42，属 A 与 D Owner 职权。
2. **实现载体授权：** 仓库存在不等于授权存在。`AiMemoryBrain` 是否即为 R42 解阻条件所指的「获授权 D Unicode validator/build 载体」，以及 D Owner 是否具备该仓写权限，须由 Product/Platform Architecture responsibility holder 指定、A 核验。
3. **F-43-02 与 AID-2026-027 的一致性：** `finding-ledger.md` 当前对 F-43-02 存在三处并存表述——表格状态 `CLOSED`、R41「不得 CLOSED」、R42 `BLOCKED`。三者互斥，须由 A 作单一权威表述收敛。
4. **main 基线同步：** `AID-2026-027` 将 F-43-02 限定为 CLOSED，但 `AiMemoryBrain` 的实现在其自身 `main`，与 `AiMemoryBrainArchitecture` 的 `main` 是否已同步、以何者为准，须裁定。

## 四、本记录不改变的事项

- G8：仍为 **NOT READY**。
- 架构整体：仍为 **NOT ACCEPTED**。
- PR 配额冻结（open PR ≤10）未解除；当前 open PR = 9，高于解冻阈值 6。
- 本记录不构成 F-43-02 关闭、不构成架构验收、不构成生产授权、不构成任何角色任命。
- 本记录不修改 `finding-ledger.md` 任何状态字段。

## 五、复现命令

```bash
# 正向
export PATH=$HOME/.cargo/bin:$PATH
cd ~/ai-projects/AiMemoryBrain/AiMemoryBrain
CARGO_TARGET_DIR=~/cargo-tgt/aid022 cargo test -j 2
# 期望：28 passed / 0 failed / 4 ignored，exit 0

# 负向（伪造并重算，验证后必须还原）
python3 -c "import json,hashlib; p='ucd/15.1.0/ucd-lock.json'; d=json.load(open(p)); d['payload']['normalizer']['cargo_lock_sha256']='0'*64; d['payload_sha256']=hashlib.sha256(json.dumps(d['payload'],separators=(',',':'),ensure_ascii=False).encode()).hexdigest(); json.dump(d,open(p,'w'),separators=(',',':'))"
CARGO_TARGET_DIR=~/cargo-tgt/aid022-neg cargo build -j 2
# 期望：exit 101，build.rs:185 panic，expected 全 0 / actual a697d905…
```

---

**记录边界：** 本记录只提交测量事实与复现步骤。是否据以改变 F-43-02、R42 或任何验收状态，由 A 与相应 Owner 裁定，L0 不代行。
