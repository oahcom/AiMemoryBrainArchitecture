# PR 合并依据总结（PR-MERGE-EVIDENCE-SUMMARY-001）

- 基线快照：`main@6b5db2918cffc2281deb22fd9858a37dbaeec726`
- 记录日期：2026-11-18
- 范围：Phase 1 Domain Model / Rust Workspace / SQLite Storage 相关 PR，以及当前待合并治理与 SQLite 验证 PR。
- 原则：本文件是证据索引，不替代 PR review、Owner 决策或平台保护规则。合并状态以 GitHub PR 元数据为准；CI 必须匹配 PR 的 exact Head SHA。未合并 PR 的 merge SHA 记为 N/A，不把关闭/被替代的 PR 计作已合并。
- 本次文档只通过独立分支提交，不直接修改 `main`。

## 1. 结论摘要

| 范围 | 状态 | 可作出的结论 | 不可外推的结论 |
|---|---|---|---|
| Phase 1 canonical Domain Model | DECIDED（限定范围） | 由 #189 建立规范基线；#193/#194 修正并确认 Claim identity 跨 MemoryVersion 仍为 OPEN | 不代表所有领域策略已决 |
| Rust Phase 1 Workspace gate | DECIDED（可执行门禁） | #221、#234、#240 exact-head Workspace CI 成功，Workspace 测试门禁已覆盖 `crates/**` | 不代表生产运行时/部署验收 |
| SQLite idempotency identity binding | DECIDED（已测边界） | #234 exact-head Workspace CI 成功，回放身份绑定到 Memory | 不代表所有跨进程/分布式幂等语义 |
| SQLite scope-filtered pagination | DECIDED（已测边界） | #241 exact-head Workspace CI 成功，分页限制应用于授权可见记录 | 不代表所有复杂权限模型 |
| SQLite WAL/FULL + reopen/process-exit rollback | DECIDED（本地文件库测试边界） | #242 exact-head 测试验证关闭重开持久化和独立进程未提交事务回滚 | 不证明断电、内核崩溃、介质损坏、备份恢复或生产拓扑 |
| SQLite independent-connection CAS/idempotency race | DECIDED（同进程独立连接边界） | #243 exact-head Workspace CI 成功，两个独立连接的竞争写及相同幂等键竞争有测试覆盖 | 不证明跨进程线性化或分布式协调 |
| SQLite rollback/lock/savepoint 扩展 | CANDIDATE / 待验证 | #249 已提交测试实现，Bilingual gate 成功 | Rust Workspace 当前仍在执行；不得提前验收 |
| PR 治理强化 / branch protection | OPEN | #248 文档提案已通过双语结构门禁 | #134 的平台级保护、必需检查强制及负向测试仍未完成 |
| Phase 3.7 D/E/I/Storage publication protocol | OPEN | Issue #25 明确保留 Owner 决策、真实实现及生产证据缺口 | 不得由 Phase 1 SQLite 测试推导出 Forget/Publication 生产闭环已完成 |

## 2. PR 逐项记录

### 2.1 Domain Model 与 Rust Workspace

| PR | 目标 / 改动范围 | Exact Head / 门禁 | 合并提交 SHA | 决策关联与处置 |
|---|---|---|---|---|
| [#189](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/189) | Phase 1 Domain Model 规范冻结；canonical object、identity、time、scope 等领域契约 | Head `42368891ed21f5c7e47867475ee620054b774637`；Bilingual runs `44247363131`、`44253844020`、`44254167924` 均 FAILURE | `f9f4e7975de58c60b724d5fcb9a72ae76f81e52b` | 已合并，但其后必须结合 #193/#194 的修正理解当前规范；不能把 #189 单独的失败门禁说成通过 |
| [#190](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/190) | 重复的 Domain Model freeze；错误地把 Claim identity across Memory Versions 标为 DECIDED | Head `ddad9d5333fbb4c2ba21318ea075582171cd62ee`；Bilingual `44254039968` SUCCESS（另有失败 run `44252052239`） | N/A（closed, unmerged） | 被 #189 及后续 #193/#194 替代；保留为历史证据。其 Claim identity 结论不得采用 |
| [#193](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/193) | 修正 Domain Model，保留 Claim identity 跨版本决策为 OPEN | Head `b6dcb5c432398b1f413adbec777ee6dd4ea954cd`；Bilingual `44254205801` SUCCESS | `a9f6d9431ef1f4918b025a23a69463008e92b3c2` | 支撑当前规范状态：Claim identity across Memory Versions = OPEN |
| [#194](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/194) | 再次明确 Claim identity 为 OPEN，校正规范来源 | Head `2ca3de62a6b31a60304385982ecdca28bec5c33e`；Bilingual `44254223209` SUCCESS | `87a2199a0b6f89c14858f475e10e86cb7d6a452f` | 支撑 Claim identity 保持 OPEN；CI 是文档门禁，不是 Rust 测试 |
| [#191](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/191) | Rust Workspace 骨架、纯领域 crate、DM-01..DM-10 单元测试 | Head `a6c44b35ca8f326ddd52825cd5283b8b00380ab0`；Bilingual `44254025064` SUCCESS；合并时尚无适用 Rust CI | `2bedbcf8c0cdf4a4ff434049c973389c526a75ad` | 实现 Phase 1 纯领域层；不冻结 Claim identity，不含 Storage/SQLite |
| [#217](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/217) | 启用 Workspace Rust CI、补 SQLite serde 依赖 | Head `7db2d3c4d27f043c02cda8f46b0beea42912e0fd`；Rust `44255133793` FAILURE；Bilingual `44255133773` SUCCESS | `5447db7d0316e1725e0288cfad081cd7db74fe6c` | 门禁接入提交；该 PR 自身 Rust 失败不能作为测试通过证据，后由 #221 修复 |
| [#219](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/219) | 与 #217 重复的 Workspace CI / SQLite serde 改动 | 无独立可采信的 exact-head 验收记录 | N/A（closed, superseded） | 被已合并 #217 替代，不作为独立实现或决策证据 |
| [#221](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/221) | 修复 Event Store ScopeRef fixture，并确保 Rust CI 覆盖 Workspace crates | Head `7f546bf2c9414788a168089d248438f5e0e057b0`；Rust `44255671837` SUCCESS；Bilingual `44255671757` SUCCESS | `7b8eef64390ed31cb92bdf7b29c98623d79a31fe` | 形成可执行 Workspace gate；当时记录 21 tests passed / 0 failed |
| [#222](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/222) | Event Store fixture、SQLite serde dependency、Workspace workflow trigger 修复尝试 | Head `d3ade61f1d015e5c63ad1985d8a19753edf82acf`；未找到该 exact Head 的 CI run | N/A（closed, superseded） | 被 #221 的整合修复替代；不声称本 PR 自身通过 |
| [#224](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/224) | ScopeRef fixture 与 Rust workflow 修复尝试 | Head `092e708a1b9f8db501eabd41cdf062e11e3ae675`；未找到该 exact Head 的 CI run | N/A（closed, superseded） | 被 #221 替代；其重复 workflow 未保留 |
| [#225](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/225) | serde derive、SQLite/Event Store ScopeRef fixture 对齐 | PR 最终 Head `17c6ca786a08b31103b4f0b7fcd07a38902fd573`；记录过中间 Head `604e843432c5aa0dffef142af67cc948d8027db5` 的 Rust run `44255722412` FAILURE；不能将该失败归到最终 Head 或说最终 Head 通过 | N/A（closed, superseded） | 被 #221 及后续集成修复替代；保留失败证据，不合并过期分支 |
| [#234](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/234) | 修复 SQLite 幂等回放未绑定 Memory identity 的缺陷 | Head `c4c02d0dcb44dc1089e8ebed61a211520992c9ea`；Rust `44256767166` SUCCESS；Bilingual `44256767193` SUCCESS | `e68a5d66f11383c5252a00bc9547073ff9f911d7` | 支撑“幂等回放绑定 Memory identity”的已测实现边界 |
| [#240](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/240) | 恢复 canonical domain/storage records 的 serde serialization derives，最小两文件修复 | Head `d5c7c41298118182a295d39fee3223beebfb5f77`；Rust Workspace `44258489811` SUCCESS；Bilingual `44258489883` SUCCESS | `715878ef3f5ce1331bc9caf771dd20481da1145e` | 支撑 Workspace + SQLite 序列化编译/测试集成；不证明生产持久性或崩溃恢复 |

### 2.2 SQLite Storage 验证

| PR | 目标 / 改动范围 | Exact Head / 门禁 | 合并提交 SHA | 决策关联与处置 |
|---|---|---|---|---|
| [#241](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/241) | 修复 scope filter 后 change-record pagination：按授权可见记录计数并推进 cursor | Head `fa8de8442ae9ff4311f2c0f42cfa4983df1737c1`；Rust `44258500677` SUCCESS；Bilingual `44258500686` SUCCESS | `6691bfba44cbebce6c4d3556e1c1cf9bbb3b16c8` | 支撑“scope-filtered visible pagination”这一局部实现结论 |
| [#242](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/242) | 文件 SQLite WAL、synchronous=FULL、foreign_keys、busy timeout；close/reopen 持久化与独立子进程未提交事务回滚测试 | Head `92d4910057a6f5b48e627a393b7bc7005bb73b20`；Rust `44258883510` SUCCESS；Bilingual `44258883432` SUCCESS | `aa711289785395d2efa202e34def64c393ee0ac7` | 支撑本地文件库重开持久化、进程终止时未提交事务回滚；明确不证明断电/内核崩溃/介质损坏/恢复演练 |
| [#244](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/244) | 两个独立 SQLite connections 竞争首次 commit 的 CAS 测试 | Head `09ab26963293ee460237c6f27c5b95ed3b401730`；Rust `44259233587` SUCCESS；Bilingual `44259233358` SUCCESS | N/A（closed, superseded） | 虽有自身 exact-head 通过证据，但被 #243 合并的增强覆盖替代；不作为 main 已合并代码依据 |
| [#243](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/243) | 合并独立连接 CAS 竞争与并发相同幂等键 replay 测试 | Head `179059a5be1973e2e188fd648ee57d1db7b004fe`；Rust Workspace `44259219033` SUCCESS；Bilingual `44259218907` SUCCESS | `4a3e06fd263e9dbd1056179dceb3cb21b17e330f` | 支撑同一进程内独立连接竞争写的 bounded CAS 结论；不证明跨进程线性化/分布式协调 |

### 2.3 当前待合并 PR

| PR | 目标 / 改动范围 | Exact Head / 门禁快照 | 合并提交 SHA | 当前状态 / 决策 |
|---|---|---|---|---|
| [#248](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/248) | PR-GOVERNANCE-001 双语执行附录：exact-head CI、独立审批、prompt/evidence 追踪、Issue #130/#134 runbook | Head `b887e9518977dca985776bf8715de9cd7597beb2`；Bilingual `44264271033` SUCCESS；Rust 不适用 | N/A（OPEN） | 文档提案；CANDIDATE。Issue #134 的 GitHub 平台级保护设置和负向阻断测试仍 OPEN |
| [#249](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/249) | SQLite SAVEPOINT rollback、busy timeout/retry、injected commit failure、panic/unwind rollback 测试 | Head `be1eb17334864b1d74aa70612a09033f09b40d36`；Bilingual `44264275487` SUCCESS；Rust Workspace `44264277063` 在本次抓取时 IN_PROGRESS | N/A（OPEN） | CANDIDATE / TO_VALIDATE；待 exact-head Rust 结果完成，不提前验收 |

## 3. 状态分类与证据边界

### DECIDED（仅限有证据的具体命题）

1. Phase 1 canonical Domain Model 的已冻结范围按 #189 落地，并由 #193/#194 修正文档冲突；Claim identity across Memory Versions 明确仍为 OPEN。证据：merge #189 `f9f4e7975de58c60b724d5fcb9a72ae76f81e52b`；修正 merge #193 `a9f6d9431ef1f4918b025a23a69463008e92b3c2` / run `44254205801`；#194 `87a2199a0b6f89c14858f475e10e86cb7d6a452f` / run `44254223209`。
2. Rust Workspace CI 对 crates 的测试门禁可执行且通过。证据：#221 merge `7b8eef64390ed31cb92bdf7b29c98623d79a31fe` / run `44255671837`；#240 merge `715878ef3f5ce1331bc9caf771dd20481da1145e` / run `44258489811`。
3. SQLite idempotency identity binding、scope-filtered pagination、WAL/FULL reopen/process-exit rollback、同进程独立连接 CAS race，分别只在各 PR 的测试边界内视为 DECIDED。证据分别为 #234 run `44256767166`、#241 run `44258500677`、#242 run `44258883510`、#243 run `44259219033`，且各自 exact Head 和 merge SHA 已在上表列出。

### CANDIDATE

- PR #248 的治理执行附录：双语 gate 通过，但 PR 未合并，且不能替代 GitHub 平台配置。
- PR #249 新增的 SQLite rollback/lock/savepoint 测试：实现已提交，Rust exact-head 结果尚待完成。
- SQLite WAL/FULL 配置可作为当前 adapter 的实现配置，但不能提升为生产环境的最终 durability policy。

### OPEN

- Claim identity across Memory Versions。
- Issue #25 的 D/E/I/Storage exact-owner decision、真实 publication participant/sequencer、production authorization、crash/failover/restore 及生产证据。
- Issue #134 的 main branch protection / required checks 强制、独立审批与失败门禁负向测试。
- Issue #130 的完整 prompt/session traceability audit。

### TO_VALIDATE

- 跨进程线性化、跨主机/分布式并发与协调。
- 断电、内核崩溃、写缓存、介质损坏、备份恢复及真实生产部署拓扑。
- SQLite connection pool 生命周期与池化连接异常回收；#249 明确没有 connection-pool abstraction。
- 更完整 Scope/Permission algebra 与生产授权服务集成。

## 4. 合并纪律

- 只以 exact Head SHA 对应的 CI 作为该 PR 的门禁证据；旧 Head、同名 workflow 或 merge 后其他提交的成功结果不得替代。
- PR 关闭但未合并（例如 #190、#222、#224、#225、#244）必须保留 N/A merge SHA，并注明 superseded/failed/closed，不得记作 main 已集成。
- CANDIDATE → DECIDED 必须同时记录实现 Commit SHA 与 exact-head CI Run ID，并限定结论边界。
- 双语门禁只证明文档结构/清单门禁；不能代替语义审查、Rust 测试或生产证据。
- 本文基线是抓取时的 `main@6b5db2918cffc2281deb22fd9858a37dbaeec726`。后续 main 前进时，应以新快照增量更新本记录，不覆盖历史证据。
