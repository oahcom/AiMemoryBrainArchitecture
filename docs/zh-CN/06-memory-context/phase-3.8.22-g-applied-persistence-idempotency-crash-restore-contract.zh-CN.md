# G Applied 持久化合同中文源文件的阅读镜像

本文件对应规范中文源文件：
`06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md`。

该合同规定 Full Applied 的持久化决策仅归 G 所有。C `HANDOFF_ACCEPTED` 是必要条件但不充分；G 必须关联 C Provider Outcome、经过认证的 H Evidence、COC Participant/Terminal Proof、I Authorization、D ForgetFence、适用时 Storage Same-GID Resolution，以及 G Context/Delivery Predicate。

合并 PR [#139](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/139) 加入了有明确边界的单节点 SQLite 参考模型。精确 PR Head 运行 [#44187485388](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187485388) 与合并后 main 运行 [#44187595305](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187595305) 均通过；后者绑定 main `af3b0380e35a5834f8b5cdca92dfa0f8fcd8e1bf`，报告 8 项测试通过。

该成果是参考/符合性原型，不是生产 G Runtime，也不是 Owner 验收。它不证明多副本线性化、分布式 Restore-Fencing、Current-Use Revalidation、真实权威解析、密码学认证或生产持久化能力。生产 G Applied 与跨 Owner Full Applied 仍为 **NOT VERIFIED / NOT FROZEN**。
