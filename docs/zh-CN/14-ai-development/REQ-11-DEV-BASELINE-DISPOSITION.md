# REQ-11（#351）——开发基线范围裁定

**裁定：** CLOSE——Issue #351 的八项验收标准全部属于 `OUT-OF-SCOPE(dev-baseline)`。
**记录类型：** 范围边界与验收处置记录；不是产品设计、实现、采纳或生产就绪批准。
**跟踪 Issue：** [#351](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/351)
**权限依据：** Owner 授权书发布于 [Issue #305 评论 #7042461592](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/305#issuecomment-7042461592)；该授权对各 REQ Issue 的适用性已由 [Issue #351 评论 #7042543179](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/351#issuecomment-7042543179) 确认。

## 范围裁定

REQ-11 是一项战略总括需求，目标是将已验证能力转化为可运行、可采用的产品或服务。其八项验收标准涉及部署配置、干净环境安装、密钥与最小权限、运维生命周期、公共 API 保证、真实集成、可观测性与数据生命周期，以及发布就绪。这些均属于产品化、部署、运营和生态交付结果，而非开发基线实现要求。

#351 没有单独提出仅涉及打包清单、构建元数据或依赖声明的验收标准。若存在此类狭窄的仓库构建缺陷，可以独立评估；但本 Issue 未提出该项，因此本裁定不修改打包/依赖配置，也不凭空新增此类任务。

## 逐条验收处置

| # | Issue #351 验收标准 | 裁定 | 证据与边界 |
|---|---|---|---|
| 1 | 明确目标用户与支持的部署配置 | `OUT-OF-SCOPE(dev-baseline)` | 属于产品定位与支持运行配置定义。独立基线评估仅记录目标/配置部分明确，未建立产品边界（[#351 评论 #7037174694](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/351#issuecomment-7037174694)）。 |
| 2 | 可在干净环境复现安装 | `OUT-OF-SCOPE(dev-baseline)` | 安装器、分发和干净主机安装属于部署交付；评估记录为未满足。 |
| 3 | 配置与密钥处理符合最小权限 | `OUT-OF-SCOPE(dev-baseline)` | 生产级配置、凭据/密钥管理和最小权限部署属于运营安全交付；评估记录为未满足。 |
| 4 | 升级、回滚、备份、卸载均经过测试且无静默数据丢失 | `OUT-OF-SCOPE(dev-baseline)` | 端到端运维生命周期与恢复测试属于产品运营；评估记录为未满足。 |
| 5 | 公共 API 已版本化并有兼容性保证 | `OUT-OF-SCOPE(dev-baseline)` | 公共 API/SDK 生命周期与兼容策略属于产品接口承诺；评估记录为未满足。 |
| 6 | 至少一个真实集成展示端到端使用 | `OUT-OF-SCOPE(dev-baseline)` | 外部生态集成和端到端产品使用属于开发基线之外；评估记录为未满足。 |
| 7 | 可演示监控、诊断、审计和数据导出/删除工作流 | `OUT-OF-SCOPE(dev-baseline)` | 运维可观测性与面向用户的数据生命周期工作流属于部署/产品能力；评估记录为未满足。 |
| 8 | 发布就绪包含安全、可靠性、文档和支持证据 | `OUT-OF-SCOPE(dev-baseline)` | 发布/支持就绪与生产保障明确属于产品/运营范围；评估记录为未满足。 |

此前独立基线评估的总体结论为 **“Productization: not ready”** 和 **“Operational readiness: not established”**；该评估接受的是基线调查，不是产品化就绪。此记录不会把任何未满足的产品标准转换成已满足的实现结果。

## 执行与非声明

- 本裁定不实施产品化、部署、生产集成、公共 API、打包、依赖或运行时变更。
- 不声称 CI PASS，也不声称产品已就绪。
- 因本轮没有交付原生实现，不涉及 Rust/C 工具链执行。
- 本文件仅记录范围裁定；合并此记录不构成产品化工作的授权或暗示。

**最终处置：** 8/8 项均记录为 `OUT-OF-SCOPE(dev-baseline)`；Issue #351 可按范围处置完成关闭。
