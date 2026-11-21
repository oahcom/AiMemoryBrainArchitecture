# GAP-BASELINE-005 · 第七次独立测量

**测量者**：Verifier（不写业务代码，只派工、独立核验、合并）
**基线**：`main @ 6e7026c0`
**测量时间**：2026-11-21 23:40 (+08:00)
**环境**：WSL2 Ubuntu 24.04，`cargo`，16 核；Node 22.22.2；Python 3.13
**方法**：`git archive HEAD | tar -x` 干净导出 → 原生 ext4 副本 → `cargo test --workspace --all-targets`

---

## 1. Rust 实测数字

```
agent-integration    lib                 12 passed
agent-integration    delivery_lifecycle  19 passed
bmcp-protocol        lib                 42 passed
bmcp-protocol        p0_conformance       4 passed
brain-cli            main                 1 passed
memory-compiler      lib                 58 passed
memory-compiler      event_store_digest_compat 1 passed
memory-context       lib                 68 passed
memory-domain        lib                 36 passed
memory-domain        phase2_acceptance   11 passed / 9 ignored
memory-store         lib                  2 passed
memory-storage       lib                  3 passed
memory-storage-sqlite lib                47 passed
memory-event-store   lib                  2 passed
memory-event-store-sqlite lib             6 passed
memory-event-store-sqlite forget_fence    6 passed
其它集成测试                              若干
```

合计 **360 passed / 0 failed / 10 ignored**（上轮 338）。

增量来源：`memory-compiler` 53→58（#533 四种发布处置），
`memory-storage-sqlite` 35→47（#523 hidden prepare / explicit publish）。

## 2. Python 一致性套件

```
545 passed, 27 skipped, 3 failed, 1 error, 272 subtests
```

那 3 个失败与 1 个 error **不是代码缺陷**，已在 GAP-08 中完全归因：

- 3 个失败：三个 `.mjs` 参考实现 `import` 了 npm 包 `canonicalize`，
  而仓库无 `package.json` 也无任何锁文件。装上该包后同一批测试
  **13 passed**。
- 1 个 error：`test_hrc_semantics.py` 里一个名为 `test_digest` 的普通辅助
  函数被 pytest 收集。其模块文档指定用 `python -m unittest`，按该运行器
  **44/44 OK**。

## 3. 本轮新增/更新的工作项

| 项 | 状态 | 要点 |
|---|---|---|
| GAP-07 | 未关闭（新） | 编译阶段在生产路径不可达 |
| GAP-08 | 未关闭（新） | BMCP 套件存在未声明的 Node 依赖 |
| GAP-06 | 未关闭（更新） | #529 固定了"fence 不阻止读取"的现状 |
| GAP-07 | 更新 | #523 提供了原语，但 Store 门面未暴露 |

## 4. 本轮发现

**4.1 编译阶段不可达（GAP-07，最重要）**

`brain compile` 的真实运行输出：

```
memory-domain: Event, Memory, Claim and MemoryVersion validated
memory-storage-sqlite: persisted revision to a temporary SQLite database
memory-store: create_memory -> write_revision -> read_current succeeded
memory-context: build_context produced 1 entr(y/ies)
compiler stage skipped: PublicationAuthority has no production implementation
```

产出是合法的 1103 字节 ContextSnapshot。管道到上下文组装为止是真的端到端，
编译器不在其中。

三个 `PublicationAuthority` 实现（`EvidenceAuthority`:923、`TestAuthority`:942、
`RecoveryAuthority`:1332）全部位于 `#[cfg(test)]` 内（875、1282 行开启）。
`compile()` 的五处调用全部在 1282 行开启的测试模块内。`MemoryCompiler`
在 `memory-compiler/src/lib.rs` 之外零引用。

**后果**：`memory-compiler` 的 58 个测试演练的是一条没有生产调用方的路径。
测试数量不构成"编译可用"的证据。

**4.2 #523 提供了原语但未贯通**

`prepare_version` / `publish_prepared` 已在 `memory-storage` trait（74、77 行）
与 `memory-storage-sqlite` 实现。但 `MemoryStore` 门面只暴露 5 个方法
（37–89 行），新的两个不在其中；`memory-store` 里仅有的函数体在
`FakeStorage`（212、286 行，位于 112 行开启的 `#[cfg(test)]` 内）。

这是好消息：方向 (a) 从"无原语"降级为"缺一层暴露 + 缺跨重启持久化"。
`PreparedCommitReceipt` 正好是 `storage_prepared_hidden` 所断言的语义。

**4.3 GAP-06 的现状被诚实地固定下来**

#529 新增 `forget_api_absence_is_detectable`，断言记录 fence **之后**读取
仍然成功。它描述当前真实行为，是诚实的表征测试。文档同时澄清：fence 唯一
的执行读者是 event-store 的 backup/restore 路径，Memory 读边界完全不读
fence。"fence 校验"与"fence 执行"被明确区分开。

## 5. 我本轮自己的错误

**5.1 我一开始怀疑 GAP-06 的建议 (b) 是错的，是我错了。**

我认为"在读边界执行 fence"是误分类，理由是 `restore_backup` 只在恢复时清
事件行。查 `01-system-architecture/data-flows.md` §5.2 后确认规范原文是
"先持久记录 fence，**然后阻止新的读取/激活**，再变更规范状态"。建议 (b)
与规范一致。我此前的怀疑不成立，不应基于"看起来像过度设计"就否定一条有
规范依据的建议。

**5.2 两个 Owner 派发静默失败，我差点误判为进程被杀。**

`send_a8`/`send_h9` 的日志是 0 字节，进程也不在了。直接原因不是进程管理，
而是 `chatgpt.com:443` 不可达（`curl` 21 秒超时，两个任务均 `rc=124`）。
我应该在派发前先探测目标可达性，而不是在失败后从进程状态倒推。

**5.3 把 pytest 的 error 当成了被测代码的缺陷。**

`test_hrc_semantics.py` 报 `fixture 'value' not found` 时，我第一反应是文件
有问题。实际上该文件的文档字符串已写明运行器是 `python -m unittest`。
读到失败先查该文件的既定运行契约，比改代码更快。

## 6. 未验证事项

- 网络不稳，`git push` 多次失败重试；`6e7026c0` 已确认落地。
- Owner A（GAP-06）与 Owner H（GAP-04）本轮**未派发成功**，无新增交付。
- `canonicalize` 的版本未锁定，我仅在临时目录安装了最新版验证通过。
