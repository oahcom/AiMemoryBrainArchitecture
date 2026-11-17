# Rust Ecosystem Assessment / Rust 生态评估

- Task: TECH-REALITY-001-A | Owner A | Research date: 2026-11-17
- Status: **CANDIDATE ECOSYSTEM REVIEW — NOT A LOCKFILE / 候选生态审查，不是依赖锁定清单**

## 1. Assessment rules / 评估规则

A Rust crate existing is not enough. The assessment distinguishes native Rust, official Rust SDK, community Rust SDK, FFI binding, and network API integration. Exact MSRV/platform support must be rechecked against pinned releases and the target OS/CPU/GPU matrix before adoption. Security advisories and full transitive license audits have not yet been run.

仅存在 Rust Crate 并不足以证明可用。本评估区分 Rust 原生实现、官方 Rust SDK、社区 Rust SDK、FFI 绑定和网络 API 接入。正式采用前必须针对固定版本和目标 OS/CPU/GPU 矩阵重新核实 MSRV 与平台支持。本阶段尚未执行安全公告和完整传递依赖许可证审计。

## 2. Candidate assessment / 候选评估

| Technology | Latest observed version / evidence | Integration type | License | Rust/platform notes | Assessment |
|---|---|---|---|---|---|
| Tokio | 1.54.1; repo HEAD tree `02ed9178a471f27ac03a46595e68c7e0a015bfc0` | Native Rust runtime | MIT | Broad Rust async ecosystem; current release MSRV 1.85; Windows/Linux/macOS are normal supported Rust targets, but project-specific feature matrix still required | RECOMMENDED runtime candidate; high maturity |
| SQLx | 0.9.0 (docs.rs); repository currently maintained under transact-rs | Native async Rust SQL toolkit; SQLite uses libsqlite3 C API | MIT/Apache-2.0 | Tokio and async-std runtime support; Postgres/MySQL/SQLite; connection pools and compile-time query checking | Strong SQL adapter candidate; test SQLite concurrency/transactions and offline compile-time metadata |
| rusqlite | 0.43.0 (docs.rs) | Rust wrapper over SQLite C library | MIT/Apache-2.0 | Synchronous API; bundled SQLite feature possible; use dedicated DB thread or spawn_blocking rather than blocking Tokio worker | Strong embedded SQLite option; simplest transaction control but sync boundary must be designed |
| Tantivy | 0.26.1 latest release; HEAD tree `2ad36b4fd0c00ded047b12295423250d8d4d713b`; HEAD Cargo manifest 0.27.0 | Rust-native search engine | MIT | HEAD manifest MSRV 1.91; segment/index writer architecture; separate index lifecycle | Strong lexical alternative; pin released tag, not unreleased main |
| Qdrant | 1.20.2; HEAD tree `23065a0bf6857c3e5da45f6c8939cc746cc0580e` | Rust server + HTTP/gRPC; official Rust client | Apache-2.0 | HEAD manifest MSRV 1.98; service deployment and network failure boundary | Mature dedicated vector service; not first-slice default |
| LanceDB | 0.42.0-beta.18; HEAD tree `57b20fb11d907fd8948827370e7c4032d396c205` | Rust SDK + embedded/distributed engine | Apache-2.0 | Rust crate is beta; columnar Lance format; local/object-store modes | Promising retrieval projection; beta and not canonical SQL replacement |
| Moka | 0.12.16; HEAD tree `a616ec19e8d4ed938caf8b2c88090331d778d5da` | Native Rust cache | Apache-2.0 | MSRV 1.71.1 for sync/future; bounded size/weight, TinyLFU/LRU, TTL/TTI | Suitable in-process cache; must not own auth/Forget truth |
| Rig | 0.46.0; HEAD tree `6428714f6be50fdc8c05eece015c6adebbcb7233` | Native Rust Agent/LLM library | MIT | Provider/tool abstractions, not a durable workflow runtime | Optional Agent-side integration; Brain should not depend on it internally |
| Temporal Rust SDK | 1.2.0; HEAD tree `a5d7742e8c5b925351fff314c2662a316309583b` | First-party Rust SDK + external Temporal Service | MIT | SDK contains replay/workflow state machines; service is separately operated | Candidate for durable long-running workflow; not canonical DB |
| Restate Rust SDK | Latest release observed 0.12.1; inspected HEAD tree `9a08091654f1e6da905f71ffe09bdd4742ecc995`; HEAD manifest 0.13.0, MSRV 1.90 | First-party Rust SDK + Restate server | MIT | SDK release and HEAD manifest differ; pin released SDK and compatible server | Candidate for durable handlers/virtual objects; younger ecosystem and extra stateful service |
| Cedar | Latest CLI release tag cedar-policy-cli-v4.15.0; HEAD tree `6387cb449bbff5e7c7c9617c56e02b36310be733`; docs.rs crate observed 4.14.1 | Native Rust policy engine | Apache-2.0 | Embedded policy evaluation and schema validation | Strong I-owned embedded policy candidate; does not implement identity/revocation workflow |
| OpenTelemetry Rust | 0.33.1; HEAD tree `1e29b1fe1d03bde8e48eb564a3dee8ec9efed6a7` | Native Rust API/SDK/exporters | Apache-2.0 | Official status docs show metrics/logs stable; traces API/SDK beta in inspected status | Use tracing now; add OTel exporters with version/stability pin |
| ort | 2.0.0-rc.15; ONNX Runtime 1.31 binding | Rust FFI binding to ONNX Runtime | MIT/Apache-2.0 (crate) | RC release; native runtime binaries/execution providers/platform packages matter | Candidate only; validate provider/operator/GPU packaging |
| Candle | candle-core 0.11.1 | Rust-native ML framework | Apache-2.0/MIT | CPU/CUDA/Metal-oriented support; model/operator coverage varies | Research candidate; not automatically lower-risk than ONNX Runtime |
| usearch | C++ project with Rust bindings; repo HEAD tree not pinned in this assessment | FFI/native library binding | Apache-2.0 | Rust API sits over C++ implementation | Candidate ANN only; account for FFI, ABI, platform builds and update/delete behavior |
| sqlite-vec | 0.1-era extension family (repo HEAD pushed 2026-05-18) | SQLite C extension, not Rust-native | MIT/Apache-2.0 (verify exact artifact) | Extension loading and platform binary packaging are concerns | Candidate only; do not infer production maturity from SQLite integration |

## 3. Ecosystem conclusions / 生态结论

### 3.1 Runtime and database access

Tokio is the lowest-risk Rust async runtime candidate. SQLx 0.9.0 is attractive if the Brain needs async SQL pools and both SQLite/PostgreSQL paths; rusqlite is attractive if SQLite transaction semantics and synchronous database operations are preferred. These are alternatives at the adapter layer, not a requirement to use both. A single writer/transaction owner must be explicit even if the crate offers many pooled connections.

Tokio 是当前最低风险的 Rust 异步运行时候选。若 Brain 需要异步 SQL 连接池并保留 SQLite/PostgreSQL 双路径，SQLx 0.9.0 有吸引力；若优先采用 SQLite 事务语义和同步数据库操作，rusqlite 更直接。两者是 Storage Adapter 层的替代方案，不要求同时采用。即使连接池支持多个连接，也必须明确单一写入/事务所有者。

### 3.2 Search

Tantivy is the most direct Rust-native lexical engine candidate. FTS5 has the smallest deployment footprint and can be used through SQLite without a separate service. Qdrant is a complete vector service; LanceDB is a Rust-capable retrieval database but its inspected release is beta. Use a lexical baseline first; choose one vector path only after recall evaluation.

Tantivy 是最直接的 Rust 原生全文检索候选。FTS5 部署负担最低，可通过 SQLite 使用而无需独立服务。Qdrant 是完整向量服务；LanceDB 支持 Rust 检索但本次检查版本仍为 Beta。应先建立词法检索基线，再依据 Recall 评估选择一种向量路径。

### 3.3 Durable execution

Temporal's Rust SDK has a substantial first-party implementation and a mature external service model. Restate's Rust SDK exposes durable handlers and Virtual Objects but is at an earlier version surface; the HEAD manifest is ahead of the latest tagged release. Neither engine replaces SQL transactions or the Brain's Forget fence. The first implementation should prove SQL outbox/lease recovery before adopting either.

Temporal Rust SDK 具有较完整的一方实现和成熟的外部服务模式。Restate Rust SDK 提供 Durable Handler 和 Virtual Object，但版本生态相对较新，HEAD Manifest 领先于最新 Tag。两者都不能替代 SQL 事务或 Brain Forget Fence。首次实现应先证明 SQL Outbox/Lease 恢复能力，再决定是否引入。

### 3.4 Authorization

Cedar is the most direct Rust-native embedded authorization candidate among the reviewed projects. OpenFGA/SpiceDB provide relationship-graph authorization as services; OPA provides a general policy distribution/evaluation system. The I Owner must decide whether the project needs embedded policy evaluation, relationship tuple graph, or centralized policy distribution. The Brain still owns authentication binding, permission epoch, revocation semantics and audit.

在本次审查的项目中，Cedar 是最直接的 Rust 原生嵌入式授权候选。OpenFGA/SpiceDB 提供服务化关系图授权；OPA 提供通用策略分发和评估系统。I Owner 必须决定项目需要嵌入式策略评估、关系 Tuple 图，还是集中策略分发。Brain 仍需负责认证绑定、PermissionEpoch、撤销语义和审计。

### 3.5 Inference

`ort` is an FFI wrapper and currently a release candidate; actual operator/execution-provider compatibility is model-specific. Candle is Rust-native but model/operator/platform coverage must be tested. llama.cpp via an isolated process/HTTP adapter may be operationally simpler for local generative inference, while the core Brain remains independent. No inference backend is selected.

`ort` 是 FFI 封装且当前为 Release Candidate；算子和 Execution Provider 兼容性取决于具体模型。Candle 是 Rust 原生实现，但模型、算子和平台覆盖必须测试。对于本地生成式推理，通过隔离进程/HTTP Adapter 接入 llama.cpp 可能更易运维，同时保持 Brain Core 独立。当前不选择任何推理后端。

## 4. Platform and maintenance caveats / 平台与维护注意事项

- Rust target availability does not prove each native dependency or GPU provider works on Windows, Linux and macOS. Validate all three with CI and packaging tests if all are product targets.
- SQLite WAL depends on same-host shared memory and must not be placed on network filesystems.
- FFI components require ABI, native library, dynamic loading, packaging, crash and security review.
- Qdrant's MSRV and Tantivy's MSRV can constrain the workspace toolchain; set one project MSRV only after resolving the complete dependency graph.
- Restate SDK's latest release tag and HEAD manifest differ; do not consume unreleased main without explicit approval.
- License identifiers above are repository/crate-level observations, not legal review of all transitive dependencies.
- No dependency vulnerability audit, SBOM, cargo-deny/cargo-audit run, cross-platform build matrix or production benchmark was run.

## 5. Recommended next validation / 下一步验证

1. Pin Rust toolchain and build a minimal workspace on Windows/Linux/macOS.
2. Run SQLite concurrency/crash tests with the chosen SQLx or rusqlite adapter.
3. Compare FTS5 and Tantivy on Chinese, English, mixed-language and identifier-heavy corpora.
4. Compare vector candidates only after a labeled recall dataset exists.
5. Run one inference model on the actual target GPU and capture VRAM, context, startup and tail latency.
6. Test Cedar policy evaluation against I-owned test vectors before selecting a policy language.
7. Evaluate Temporal and Restate with one end-to-end compiler workflow including cancellation, retry, crash, replay and Forget fence checks.
