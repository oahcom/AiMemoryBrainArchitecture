# E2E-CHAIN-001 — 端到端链路可达性测量

**状态：** 测量完成；下附一个可追加的 CLI E2E 测试，尚未在本执行会话中运行验证  
**仓库：** `oahcom/AiMemoryBrainArchitecture`  
**观测基线：** `main`（递归 Git tree：`666d77da77d28926abdd2f6784d1e89e0be654b5`）  
**范围：** 11 个 Rust workspace crate；未修改任何 `src/`

**方法说明：** 文件、manifest 内容和行号来自 GitHub 仓库 tree/file API 静态检查。下列 shell 命令是可复现的核验命令，本轮并未在本地执行；本轮没有实际运行 `grep`、`cargo tree` 或 `cargo test`。

## 核心结论

“没有跨 crate 集成测试”这一前提在当前观测到的 `main` 上不成立：仓库有 14 个 Rust 集成测试文件，其中已经存在五 crate 的正向 Store→SQLite→Context 链路（`memory-context/tests/e2e_store_to_context.rs`），以及经 `brain-cli` 和 `memory-compiler` 执行的七 crate 路径。

但现有 CLI 集成测试只断言输出是 JSON object，没有断言 ContextSnapshot 中确实出现预期的持久化 revision。§1.4 给出一个只增强断言、不改 `src/` 的追加测试。

当前七 crate 链路的真实终点是 compiler publication disposition `Blocked`，不是 `Published` derivative。该链路不包含 EventStore 持久化接收、Agent integration 投递或 BMCP 协议编码。

## 1.1 依赖可达性矩阵

方向定义为“crate A 声明依赖 crate B”。这是 Cargo manifest 依赖图，不等于运行时调用图。矩阵同时纳入 `[dependencies]` 与 `[dev-dependencies]`，并显式区分生产依赖和测试依赖。

标记：

- `D(P)`：直接生产依赖（`[dependencies]`）。
- `D(T)`：直接测试依赖（`[dev-dependencies]`）。
- `I2`、`I3`：最短间接路径分别为 2、3 跳，路径全部由生产依赖构成。
- `I2T`、`I3T`：最短间接路径包含至少一条测试依赖；**不能**据此声称生产可达。
- `×N`：声明的 manifest 依赖图中不存在有向路径。原因是缺少依赖路径，而不是臆测类型不兼容。每个 `×N` 格子均可用矩阵后的 `cargo tree` 命令逐格复核。

| crate A → crate B | agent-integration | bmcp-protocol | brain-cli | memory-compiler | memory-context | memory-domain | memory-event-store-sqlite | memory-event-store | memory-storage-sqlite | memory-storage | memory-store |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `agent-integration` | — | ×N | ×N | ×N | D(P) | D(P) | I2T | I3T | I2T | I2T | I2T |
| `bmcp-protocol` | ×N | — | ×N | ×N | ×N | ×N | ×N | ×N | ×N | ×N | ×N |
| `brain-cli` | ×N | ×N | — | D(P) | D(P) | D(P) | I2T | I2T | D(P) | D(P) | D(P) |
| `memory-compiler` | ×N | ×N | ×N | — | ×N | D(P) | D(T) | D(T) | D(T) | D(P) | ×N |
| `memory-context` | ×N | ×N | ×N | ×N | — | D(P) | D(T) | I2T | D(T) | D(T) | D(T) |
| `memory-domain` | ×N | ×N | ×N | ×N | ×N | — | ×N | ×N | ×N | ×N | ×N |
| `memory-event-store-sqlite` | ×N | ×N | ×N | ×N | ×N | D(P) | — | D(P) | ×N | ×N | ×N |
| `memory-event-store` | ×N | ×N | ×N | ×N | ×N | D(P) | ×N | — | ×N | ×N | ×N |
| `memory-storage-sqlite` | ×N | ×N | ×N | ×N | ×N | D(P) | ×N | ×N | — | D(P) | ×N |
| `memory-storage` | ×N | ×N | ×N | ×N | ×N | D(P) | ×N | ×N | ×N | — | ×N |
| `memory-store` | ×N | ×N | ×N | ×N | ×N | D(P) | ×N | ×N | D(T) | D(P) | — |

### 依赖声明证据（行号从 1 开始）

- Workspace 成员：`Cargo.toml:1-13`，恰好列出上述 11 个 crate。
- `agent-integration/Cargo.toml:8-11`：生产依赖只有 `memory-context`、`memory-domain`。
- `bmcp-protocol/Cargo.toml:8-11`：只有 serde/serde_json/sha2，没有 workspace crate 依赖。
- `brain-cli/Cargo.toml:12-21`：生产依赖包含 domain、storage、storage-sqlite、store、context、compiler；不依赖 agent-integration、event-store、event-store-sqlite 或 bmcp-protocol。
- `memory-compiler/Cargo.toml:8-23`：domain、storage 是生产依赖；event-store、event-store-sqlite、storage-sqlite 是 dev-dependencies。
- `memory-context/Cargo.toml:8-17`：生产 workspace 依赖只有 domain；event-store-sqlite、store、storage、storage-sqlite 都是测试依赖。
- `memory-store/Cargo.toml:8-13`：domain、storage 是生产依赖；storage-sqlite 是测试依赖。
- `memory-event-store-sqlite/Cargo.toml:8-14`：生产依赖 domain、event-store。
- `memory-storage-sqlite/Cargo.toml:8-14`：生产依赖 domain、storage。
- `memory-storage/Cargo.toml:8-9` 和 `memory-event-store/Cargo.toml:8-9`：生产依赖 domain。

每一个 `×N` 格子都可以把对应行/列 crate 名代入下面命令；无匹配即为预期结果。例如 `agent-integration → bmcp-protocol`：

```sh
cargo tree -p agent-integration -e normal,dev --prefix none | grep -F "bmcp-protocol v"
# 预期：无匹配，退出码 1
```

BMCP 无调用方可用 `grep -RInE 'bmcp_protocol|bmcp-protocol' crates --exclude-dir=bmcp-protocol` 复核（预期无匹配）。EventStore 生产调用缺失可用 `grep -RInE 'EventStore|SqliteEventStore|memory_event_store' crates/brain-cli/src crates/memory-compiler/src` 复核（预期无匹配）。直接依赖清单也可复核：

```sh
grep -nE '^(memory-[a-z-]+|agent-integration|bmcp-protocol)[[:space:]]*=' crates/*/Cargo.toml
```

`×N` 的意思是不存在从 A 到 B 的任何 manifest 依赖路径，不是类型不兼容。`I*T` 是测试依赖路径，不能冒充生产链路。

## 1.2 断边清单（按估算修复成本排序）

| 断点 | 位置（文件:行） | 断的性质 | 修复需要什么 | 是否已有载体 |
|---|---|---|---|---|
| BMCP 没有 workspace 集成边，也没有调用方 | `crates/bmcp-protocol/Cargo.toml:8-11`；crate 外没有代码引用 | **零依赖** | 先确定协议边界归属；由归属方声明依赖并建立真实序列化/调用路径，再补跨 crate 契约测试。当前没有可延伸的调用方。 | 未发现既有集成载体；`crates/bmcp-protocol/tests/p0_conformance.rs` 只测协议 crate 自身。 |
| EventStore 持久化接收没有接入 CLI/compiler 生产链 | `crates/brain-cli/Cargo.toml:12-21`；`crates/memory-compiler/Cargo.toml:20-23`；`crates/brain-cli/src/main.rs:246-254` | **生产依赖为零**（compiler 只有测试依赖） | 增加生产 adapter seam，从 EventStore 读取真实 `AcceptedReceipt`/payload 并交给 compiler；保留 receipt、payload digest、scope、idempotency 语义。 | 有测试载体：`crates/memory-compiler/tests/event_store_digest_compat.rs` 只证明 digest 兼容，不是生产接线。 |
| EventStore 与 compiler 的 identity 类型不兼容 | `crates/memory-domain/src/lib.rs:8-24`；`crates/memory-event-store/src/lib.rs:35-43`；`crates/memory-compiler/src/lib.rs:39-48` | **类型不兼容** | 增加显式且带校验的 `OpaqueId` ↔ `Identity(String)` 转换/adapter；不能假定隐式转换。测试空 ID 和 identity 保真。 | 有测试载体 `crates/memory-compiler/tests/event_store_digest_compat.rs`；无生产 adapter。 |
| Agent integration 未接入 CLI 可执行投递链 | `crates/agent-integration/Cargo.toml:8-11`；`crates/brain-cli/Cargo.toml:12-21`；`crates/agent-integration/tests/context_snapshot_delivery.rs:38-60,63-108` | CLI 与 agent-integration 之间是**零依赖**；现有 Agent 测试使用 fixture，不是 Store 产出的 snapshot | 建立明确应用边界，把生成的 `ContextSnapshot` 交给 Agent adapter，并断言实际投递 payload/version。不要把推理 provider 行为混入此边界。 | 有测试载体 `crates/agent-integration/tests/context_snapshot_delivery.rs`，但它自行构造 `ContextCandidate`，没有连到 storage/CLI。 |
| Context crate 声明了未使用的 EventStore-SQLite 测试依赖 | `crates/memory-context/Cargo.toml:13-17`；`grep -RIn 'memory_event_store_sqlite' crates/memory-context/tests` | **有依赖但无调用点**（Context 集成测试中没有使用它） | 要么移除未使用 dev-dependency，要么增加真正通过它接收/读取 Event 的测试并写明边界。成本较低，但不能把它误报为生产依赖。 | 既有载体 `crates/memory-context/tests/e2e_store_to_context.rs` 覆盖 Store/SQLite/Context，不覆盖 EventStore。 |

### 类型边界证据

`OpaqueId` 是私有字段 newtype，提供 `new`/`as_str`（`memory-domain/src/lib.rs:8-24`）。Compiler 的 `Identity` 是独立的 `String` tuple newtype（`memory-compiler/src/lib.rs:39-48`）。EventStore 的 `AcceptedReceipt` 用 `OpaqueId` 表示 `event_id` 和 `receipt_id`（`memory-event-store/src/lib.rs:35-43`）。这些类型不能直接赋值；接线时必须显式转换。复核转换实现：

```sh
grep -RInE 'impl[[:space:]]+From<.*(OpaqueId|Identity)|impl[[:space:]]+From<(OpaqueId|Identity)' crates/memory-domain crates/memory-compiler
```

### 对既有 GAP 结论的重要更正

在当前观测到的 `main` 上，`brain-cli` **确实调用** `MemoryCompiler::compile`：`crates/brain-cli/src/main.rs:246-254,280-290`。它创建 `AdmissionPublicationAuthority` 并执行 `compile`，因此旧 GAP-07 work item 中“compiler 被跳过/没有生产调用方”的结论已过时。

当前 production authority 将 `canonical_commit_confirmed`、`publication_participant_admitted`、`protected_visibility_authorized` 三个字段明确置为 `false`（`crates/memory-compiler/src/publication_authority.rs:99-101`）。所以 CLI 真实路径会进入 publication gate，但最终为 `Blocked`，不会发布。不要继续引用“compiler 没有被调用”的旧结论。

## 1.3 现有集成测试覆盖了什么、不能证明什么：全部 14 个 Rust 文件

计数证据：

```sh
ls crates/*/tests/*.rs
ls crates/*/tests/*.rs | wc -l
# 14
```

下表的 crate 数量按实际被调用的 workspace crate/API 计算，不把 serde、rusqlite 等第三方依赖计入。

| # | 集成测试文件 | 跨越 crate 数 | 实际验证的边 | 不能证明什么 |
|---:|---|---:|---|---|
| 1 | `agent-integration/tests/context_snapshot_delivery.rs` | 3（agent-integration、memory-context、memory-domain） | fixture candidate → `build_context` → `DeliveryPayload::from_snapshot` → 内存 adapter | 不会从 SQLite 创建/读取 Memory；不测 EventStore、CLI、BMCP 或真实 Agent runtime。 |
| 2 | `agent-integration/tests/delivery_lifecycle.rs` | 1 | Agent integration 内部的 delivery 状态转换和 attestation 不变量 | 不构造 ContextSnapshot，也不跨 storage/protocol 边界。 |
| 3 | `bmcp-protocol/tests/p0_conformance.rs` | 1 | BMCP digest 与严格 conformance vectors | 不与 Agent integration 交换报文，也不消费真实 ContextSnapshot。 |
| 4 | `brain-cli/tests/compiler_skip_is_visible.rs` | 7（CLI + domain、storage、storage-sqlite、store、context、compiler） | 执行 `brain compile`；断言退出码、Blocked notice/sidecar 和 JSON object 输出 | 文件名沿用旧称；没有断言 snapshot 中具体 entry、memory ID/version，也不证明 EventStore 接收、Agent 投递、BMCP 编码或 Published 结果。 |
| 5 | `memory-compiler/tests/event_store_digest_compat.rs` | 4（memory-compiler、memory-domain、memory-event-store、memory-event-store-sqlite） | SQLite EventStore receipt digest 可被 compiler ingestion 接受 | 没有把 EventStore 变成 compiler/CLI 的生产依赖；digest 兼容不等于 accepted-event 全链路。 |
| 6 | `memory-context/tests/e2e_negative_paths.rs` | 5（memory-context、memory-domain、memory-storage、memory-storage-sqlite、memory-store） | Store/SQLite/Context 的 scope、lifecycle、forget、stale-write、budget、restart 负路径 | 不经过 EventStore、compiler、Agent integration 或 BMCP。 |
| 7 | `memory-context/tests/e2e_store_to_context.rs` | 5（memory-context、memory-domain、memory-storage-sqlite、memory-store、storage trait） | 真实 SQLite Store create/write/read → 从持久化 Claim 构建 ContextSnapshot | 不包含原始 EventStore 接收、compiler、Agent 投递或 BMCP。它已经是一条真实的五 crate 正向 E2E。 |
| 8 | `memory-domain/tests/phase2_acceptance.rs` | 1 | Domain claim/fact/relation/provenance acceptance 规则 | 不跨 crate，也不持久化数据。 |
| 9 | `memory-event-store-sqlite/tests/forget_fence.rs` | 1 | 使用手工 schema 的 ForgetFence restore/fail-closed/并发行为 | 不执行 MemoryStore read gate，也不构建 Context。 |
| 10 | `memory-event-store-sqlite/tests/forget_fence_real_schema.rs` | 3（memory-event-store-sqlite、memory-event-store、memory-domain） | 在真实 EventStore schema 建立的数据库上执行 fence restore | 不进入 MemoryStorage/MemoryStore 或 Context；Event 行不是 canonical Memory revision。 |
| 11 | `memory-event-store-sqlite/tests/resilience.rs` | 3（memory-event-store-sqlite、memory-event-store、memory-domain） | payload custody、digest 篡改检测、replay、并发、rollback、WAL recovery | 不把 Event 接收连接到 compiler ingestion 或 Context 组装。 |
| 12 | `memory-store/tests/cross_crate_contract.rs` | 4（memory-store、memory-storage、memory-storage-sqlite、memory-domain） | Store facade + trait + SQLite round-trip、scope、CAS、idempotency、重复创建 | 不构建 Context，也不涉及 EventStore/compiler/Agent/BMCP。 |
| 13 | `memory-store/tests/forget_e2e.rs` | 4（memory-store、memory-storage、memory-storage-sqlite、memory-domain） | MemoryStore forget facade 与 version/sibling 可见性语义 | 不使用独立的 EventStore ForgetFence，也不涉及 Context/compiler/protocol。 |
| 14 | `memory-store/tests/sqlite_integration.rs` | 4（memory-store、memory-storage、memory-storage-sqlite、memory-domain） | 最小 SQLite MemoryStore 路径与 facade identity 校验 | 不构建 Context，也不验证 Event 接收/compiler/Agent/BMCP。 |

关键区别：测试文件名含 `e2e_*`、workspace 全绿、或存在跨 crate import，都不能证明完整产品链。上表逐项写明了每个测试没有跨过的边界。

## 1.4 唯一的最小可信 E2E 提案

**选定链路（7 个 workspace crate）：**

`原始 Event JSON fixture → brain-cli → memory-domain 校验 → memory-storage-sqlite → memory-storage / memory-store → memory-context ContextSnapshot → memory-compiler publication gate → snapshot 输出 + compiler-status sidecar`

选择理由：这是当前已经接线、最长且有可执行 binary 和仓库内 fixture 的链路。无需改 `src/`，也无需增加生产依赖。`brain-cli/src/main.rs:304-479` 解析/校验输入，创建并持久化 Memory/revision，读取持久化 revision，从 Claim 派生 ContextCandidate 并构建 snapshot。`main.rs:246-290` 通过 `AdmissionPublicationAuthority` 执行 compiler；`main.rs:502-520` 序列化 snapshot 并输出 compiler disposition。现有测试已经会调用该 binary（`compiler_skip_is_visible.rs:59-75,129-159`）。

**起点：** 仓库中的 `crates/brain-cli/fixtures/event.json`，包含原始 Event、payload、Memory、Claim 和 Context 请求。

**终点/断言：** 有效序列化的 `ContextSnapshot`，其中 `identity.context_id` 为 `context-demo-001`，首个 entry 引用 `memory-demo-001` 和 `memory-version-demo-001`；旁边的 `.compiler-status` sidecar 明确以 `compiler stage blocked:` 开头。按当前 production authority 状态，Blocked 是预期结果：三个 proof flag 尚无权威 issuer，保持 false。

**能证明：** 可执行 CLI 路径完成 domain 校验；通过 MemoryStore 在 SQLite 中创建并持久化 Memory/revision；读回持久化 revision；从真实存储 Claim 派生 candidate；构建并序列化 ContextSnapshot；调用 compiler 并把有类型的 Blocked 结果保存在 sidecar。

**不能证明：** EventStore 持久化接收/receipt 或 payload custody；EventStore 到 compiler 的转换；compiler 发布（当前结果刻意为 Blocked）；Agent adapter 投递；BMCP 序列化/签名/conformance；模型推理或 provider 侧应用。它是当前已接线的 CLI→Context→Compiler-gate E2E，不是覆盖全部 11 个 crate 的 E2E。

### 段二——追加测试

现有 `compiler_skip_is_visible.rs` 只检查 snapshot JSON root 是 object。下面这个新增测试强化断言，不改 `src/`。放在 CLI 测试目录，因为 CLI 是当前唯一把这七个 crate 接起来的生产入口。

文件：`crates/brain-cli/tests/e2e_full_chain.rs`

```rust
use serde_json::Value;
use std::fs;
use std::process::Command;
use std::sync::atomic::{AtomicU64, Ordering};

static NEXT_ID: AtomicU64 = AtomicU64::new(1);

#[test]
fn raw_event_to_persisted_memory_context_and_compiler_gate_is_observable() {
    let nonce = NEXT_ID.fetch_add(1, Ordering::Relaxed);
    let output_path = std::env::temp_dir().join(format!(
        "brain-e2e-full-chain-{}-{nonce}.json",
        std::process::id()
    ));
    let sidecar_path = std::path::PathBuf::from(format!(
        "{}.compiler-status",
        output_path.display()
    ));
    let fixture = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("fixtures")
        .join("event.json");

    let output = Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("compile")
        .arg("--input")
        .arg(&fixture)
        .arg("--out")
        .arg(&output_path)
        .arg("--verbose")
        .output()
        .expect("execute brain compile");

    assert_eq!(
        output.status.code(),
        Some(0),
        "CLI failed: {}",
        String::from_utf8_lossy(&output.stderr)
    );

    let bytes = fs::read(&output_path).expect("read ContextSnapshot output");
    let snapshot: Value =
        serde_json::from_slice(&bytes).expect("output must be a serialized ContextSnapshot");

    assert_eq!(snapshot["identity"]["context_id"], "context-demo-001");
    assert_eq!(snapshot["context_version"], 1);
    assert_eq!(snapshot["entries"].as_array().expect("entries must be an array").len(), 1);
    assert_eq!(snapshot["entries"][0]["memory_id"], "memory-demo-001");
    assert_eq!(
        snapshot["entries"][0]["memory_version_id"],
        "memory-version-demo-001"
    );
    let rendered = snapshot["entries"][0]["rendered_content"]
        .as_str()
        .expect("entry content must be serialized as text");
    assert!(rendered.contains("uses"));
    assert!(rendered.contains("a governed memory context"));

    let sidecar =
        fs::read_to_string(&sidecar_path).expect("compiler status sidecar must be written");
    assert!(
        sidecar.starts_with("compiler stage blocked:"),
        "the production compiler gate must expose its typed Blocked disposition: {sidecar}"
    );

    let _ = fs::remove_file(&output_path);
    let _ = fs::remove_file(&sidecar_path);
}
```

**执行状态：** 本轮没有运行。已连接的本地终端因当月用量上限而不可用；GitHub 文件检查确认 binary、fixture、`serde_json` 依赖和 CLI 进程测试模式均已存在，但本轮不能诚实声称 `cargo test --workspace --offline` 已通过。接收新增测试前必须执行：

```sh
cargo test --workspace --offline
ls crates/*/tests/*.rs | wc -l
# 预期：全部测试通过；数量 15
```

没有修改 `src/`，没有增加生产依赖。如果新增测试失败，只能修正测试 fixture/assertion；本 work item 不授权通过修改实现代码来凑通。

## 登记用 finding

- **证据：** `cargo tree -p brain-cli -e normal,dev` 与 `crates/brain-cli/src/main.rs:418-479,502-520` 可复现七 crate Store→Context 路径；`crates/brain-cli/tests/compiler_skip_is_visible.rs:59-75,129-159` 表明既有进程级测试只断言 JSON object 输出；`crates/agent-integration/Cargo.toml:8-11` 与 `crates/bmcp-protocol/Cargo.toml:8-11` 展示其独立依赖边界。
- **判定：** CLI→MemoryStore→ContextSnapshot→Compiler gate 已接通，但测试 oracle 太弱，不能证明持久化 identity；EventStore 接收、Agent 投递和 BMCP 仍未接入该可执行链。Compiler 已进入 gate，但有意返回 Blocked。
- **下一步：** Owner A 增加并执行 `crates/brain-cli/tests/e2e_full_chain.rs`，用 `cargo test --workspace --offline` 验证 snapshot identity 和 Blocked sidecar；Owner E/Owner D 分别提供三个 false publication flag 的权威 issuer；协议/Agent owner 再定义并测试各自明确的 adapter 边界。

## 最终建议

如果只能修一条断边，优先把持久化 EventStore acceptance 接到 CLI/compiler ingestion 边界：它消除原始 Event 到当前可执行 Memory/Context/Compiler 路径之间最早的语义缺口，并为后续 Agent/BMCP 提供真实 accepted-event identity 和 payload。
