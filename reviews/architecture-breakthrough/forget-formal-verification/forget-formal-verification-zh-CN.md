# Forget 协议形式化验证报告（中文）

**结论：NOT READY FOR PRODUCTION IMPLEMENTATION / 生产安全性尚未证明。**

## 执行摘要

本次以当前 Owner 分支 HEAD 和精确 Blob 为准，检查 D/E/F/G/H/I/Storage 的 Forget 契约，并对最小抽象状态机执行有限状态枚举。

- D 已定义单调 Fence、Producer Registration Barrier、Register-before-visible、最终发布前 Fence 检查和未知状态 fail-closed 等核心语义。
- E 的派生登记与发布执行仍为 Candidate；D/E/Storage 原子登记与可见性提交尚未完成跨 Owner 接受。
- I 的 Producer/Recipient Inventory 与 Global Forget Completion 治理仍阻塞，闭世界覆盖无法证明。
- F 已定义最终检索披露边界的 Fence 复核，但实现和执行未验证。
- G 的 Applied 持久化文件是规范设计草案且需要跨 Owner 接受；不能把 ACK 或历史 Applied 当作当前可复用状态。
- H 的 Adapter ACK/重连仍是 Candidate；离线 Adapter 未确认不能视为成功。
- Storage PR #71 是条件性逻辑审查提案，未证明真实数据库、HA、恢复或物理擦除安全。

## 基线

Main HEAD：b3c666e67982cb3d3374e759cfb6552c7765aacb。
D：session-d-memory-brain-2026-11-16 @ 194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f。
E：session-e-memory-compiler-2026-11-16 @ ee098e14747d9915de5b3efb63b3a8dd77f670ed。
F：session-f-memory-runtime @ 1908ce4d233b20f7cafd00cb679affd01bd15174。
G：session-g-memory-context @ 763b3d31e910db8fd29c6e4dbaff9273b7fb66b8。
H：session-h-bmcp-protocol @ 0d36324457e39bd50ad56ae902d477c4ea765b61。
I：session-i-security-governance-2026-11-16 @ 0d071bf1ee7cc71912398c6ae57e4496e08f44ab。
Storage：session-storage-consistency-forget-atomicity-2026-11-16 @ 830a559bd2f4ec72608f5a51e1a0b43779f2b989。

关键 Blob：D Forget Fence 1f0391bc49d007c44ec74165bd33d37412cc7990；D Publication Gate 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5；D Lifecycle 8b972035b449e1eab546aedc9cc5b30581600c65；E Derived Registration 00e37ba56596e710513c8d0568acd79141d9101b；F Runtime Forget ce59252dbbdc5d10d016704797e9ba12d5a941bd；G Applied Persistence bd297873bc1e593280484a43cb44b56058d9c4ff；I Global Inventory 9100061fa986fb6676656169de3fcf9fc1c72664；Storage JF10 model 72fef7be1cd3f111a0151498c686d4556156339f。

PR #66（D）和 PR #68（I）均为非规范提案；PR #71（Storage）仍 open，声明条件性逻辑接受、需要修改、物理实现未验证。Issue #43 明确保留 Producer Inventory、Global Forget、JF-10 和物理拓扑/故障证明阻塞。

## 模型检查

本次连接环境没有可用的 TLC 执行链，因此采用 Python 显式状态 BFS，而非只画状态图。模型包含一个对象、一条 lineage、一个 producer、一个 Fence generation、一个 index、一个 cache、一次 terminalization/receipt 和一次 restore。

安全规则模型在深度 10 内探索 606 个状态/深度组合，没有发现模型内不变量违反。移除关键 guard 的模型变体找到最短反例：

- 旧 Worker：admit → install_fence → publish
- Admission 竞争：install_fence → admit
- Index 重建：admit → publish → install_fence → rebuild_index
- Cache 回填：admit → publish → install_fence → repopulate_cache
- 旧备份恢复：install_fence → restore

这些是模型变体反例，不是生产故障日志。

## F1–F8 判定

- F1 No resurrection：逻辑模型有条件通过；生产未证明。
- F2 No stale publication：逻辑模型有条件通过；D/E/Storage 原子发布未证明。
- F3 Admission safety：逻辑模型有条件通过；跨 Owner 实现未证明。
- F4 Dependency completeness：未证明；I 全局 Producer/Recipient Inventory 与 seal 仍阻塞。
- F5 Visibility safety：逻辑模型有条件通过；F/G/H 端到端披露路径未验证。
- F6 Idempotency：局部语义存在；G Applied 和 D/I terminalization 跨 Owner 接受未闭合。
- F7 Restore fencing：逻辑模型有条件通过；物理 PITR/HA/恢复 campaign 未证明。
- F8 Crash consistency：未证明；JF-10 仍为 P0。

## 实施门槛

生产 Runtime 前至少关闭：D/Storage 同一原子排序域；E 完整依赖登记和最终发布契约；I 全局 Producer/Recipient Inventory 与治理审批；JF-10 I 授权 sequencer 与 Storage 可见性提交的崩溃原子耦合；F/G/H 最终披露、Applied、Adapter 重连门；Restore 高水位隔离和真实故障测试。

**最终判断：架构有可行的安全设计方向，但跨模块 Forget 协议尚未达到可证明、可实现、可生产验收的状态。不得把有限模型通过解释为生产安全认证。**
