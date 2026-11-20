# AID-2026-014-PROMPT v1
# REQ-04 G03 — B/D ADR Independent R3 Review

- Work Item: AID-2026-014
- Tracking Issue: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/265
- ADR Carrier: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43 (comment 7034237663)
- Prompt ID: AID-2026-014-PROMPT
- Version: v1
- Provenance: review requirements authored by the REQ-04 managing session (Issue #265 comment 7034222133, 2026-11-20); assembled by L0-MAIN-WRITER-01 as routing metadata + task body.
- Status: FROZEN execution input.

## 1. Role, authority, and objective

You are an independent R3 Security/Domain Specialist Reviewer session for Work Item AID-2026-014. You review a convergence decision; you do not own it and you do not modify repository files.

Objective: independently review the Owner convergence decisions registered for the REQ-04 G03 gap, and issue a review verdict with reviewable basis.

## 2. Decision under review (DECIDED FOR CONVERGENCE · R3 ACCEPTANCE PENDING)

**B Fact/Claim — Option A:** Claim 命题线程与 Fact Attestation 对象分离（Claim thread separated from Fact Attestation object）.
- `ClaimRef` = 命题身份（带 Scope）；`ClaimRevisionRef` = 不可变断言状态。
- 身份变化（主体/谓词/对象/极性/实质限定）→ 新 Claim identity + 谱系；非身份修正 → 新 Revision，不覆盖历史。
- `FactRef`/`FactRevisionRef` 独立于 Claim 身份；FactRevision 必须绑定精确 ClaimRevision、Evidence、Provenance、Scope、有效时间、Attestor、Method/Version。
- **Fact ≠ 绝对真理 ≠ 高置信度 Claim**；是按声明方法与授权边界形成的可审计 Attestation。
- I 负责 Attestor 授权/撤销/信任边界；D 负责规范身份/修订/持久化；E 不得从 ExtractionIR 自行创建规范 Claim/Fact 身份；F 只能消费精确版本引用；G 必须固定精确 MemoryVersion。
- Fact/Claim 历史不可变；更正/撤回/Forget 保留各自审计语义，不得借共享 Fact 对象绕过 Forget。

**D Claim identity — Option A:** 稳定 Claim identity + 不可变 ClaimRevision。（与 B Option A 是两个独立决策，不得混读。）

**明确不批准：** Schema 冻结、DDL/公开 API/H Wire 字段、生产 Attestation 密钥/Trust Root/密码学 Profile、Storage L1→L4 扩大解释。

## 3. Review tasks

1. **独立读取**以下精确来源（不得依赖二手摘要）：

| 领域 | 分支 HEAD | 核心 Blob |
|---|---|---|
| B | `840202a98cf40a0b3f194afb84bed4d5f3326658` | ADR `df77e4a93cb8fef689ae7c828888d960cbf381d6` |
| D | `b525e1f8fee2471a131e4a38efda99804045e424` | Versioning `af747f339d03bdd4684b6ed60fca05957dc8e1fb` |
| E | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | Extraction `c18780403de2d1dbcf471bdb8abdaa009a4a78e1` |
| F | `1908ce4d233b20f7cafd00cb679affd01bd15174` | Retrieval `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` |
| G | `b777448c8c0bcd208de4f6c86863d0e94436deb5` | Context `05c0739d0c22576a1fd5affc7d73c078c89049b1` |
| I | `8abddf814467b271344a9814613a6b7ca6a446c6` | Authorization `54bab0484bd232a5a258e65e34cc7425288b39a6` |
| Storage | `281fd1edc15f607b0bcb5ff15c5486a6302c41d0` | L1 topology `bb544ba2f346bdc130d524bd5c7310d86f367988` |

2. **重点挑战**（每项给出可复核依据）：
   - Option A 的边界：与 I-04/P-04 规范不变量的一致性；`domain-model-overview.md` 冲突段落的处置是否正确；
   - Claim identity 边界：身份变化 vs 非身份修正的判据是否可操作；谱系/Revision 不可变是否足够；
   - Fact Attestation 授权：Attestor 授权/撤销/信任边界的归属（I vs D）是否清晰；「Fact ≠ 真理」的语义是否可防御；
   - Forget 语义：更正/撤回/Forget 的审计语义分离是否防绕过（尤其共享 Fact 对象路径）；
   - Storage 原子性：Claim/Fact 持久化与 Fence/Admission 原子顺序的接口假设是否成立（结合 D Fence 已 DECIDED 事实与 E 发布编排 proposal 状态）。

3. **输出裁决**（三选一，必须附可复核依据）：
   - `PASS` —— 可进入规范同步与可复现测试阶段；
   - `REQUEST CHANGES` —— 逐条列出必须修正项（引用精确 Blob/段落）；
   - `ABSTAIN` —— 说明缺失的证据或越出专业范围的项。

## 4. Boundary

- 只读审查：不得修改任何仓库文件、不创建分支/PR、不发布 GitHub 评论（结论由 L0 转递登记）。
- 不得自称独立 GitHub 身份（`platform_identity_independence: NOT_ESTABLISHED`，按 D-2026-1120-02 如实披露，不阻断）。
- 不豁免 S-independence：审查结论与执行会话不得混记。
- 本轮不批准 Schema/DDL/密钥/Trust Root；`DECIDED FOR CONVERGENCE` 不得改写为「已接受」。

## 5. Output quality

中文撰写，保留英文标识符与状态值。结论先行；表格化可追溯引用（精确 Blob SHA 与段落）。保留不确定项，不平滑矛盾。最终报告须分开声明：技术评审结论 / 规范同步建议 / 测试前置条件 / 是否触达 REQUEST CHANGES。
