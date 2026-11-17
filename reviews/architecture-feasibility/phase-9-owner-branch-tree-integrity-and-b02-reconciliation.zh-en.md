# Phase 9 — Owner Branch Tree Integrity Incident and B-02 Reconciliation
# Phase 9 — Owner 分支文件树完整性事件与 B-02 交叉审查

**Role:** A / Integration Review  
**Date:** 2026-11-18  
**Disposition:** BLOCKED — OWNER BRANCH TREE INTEGRITY MUST BE RESTORED BEFORE FURTHER ACCEPTANCE  
**Scope:** Read-only inspection of current main and H/C/I/D/Storage Owner branch refs. This report does not modify Owner branches, main, Issue #43, or existing PRs.

## 1. Executive decision

The newest H and C Owner branch commits are not safe incremental documentation updates. Each commit has the prior recorded Owner HEAD as its parent, but the resulting Git tree contains only a small subset of the repository paths. Exact GitHub compare results show mass deletion:

| Branch | Prior HEAD | Current HEAD | Added | Removed | Renamed | Paths in current recursive tree |
|---|---|---|---:|---:|---:|---:|
| H | `0d36324457e39bd50ad56ae902d477c4ea765b61` | `0277a8b9ee63be850acc0b8b1b08625524aaa33b` | 2 | 205 | 3 | 7 |
| C | `71047cdb51139ca4080ac67f451e38a48698859d` | `a5dff993e5c2928a28deb777c41023cfe923366f` | 2 | 133 | 1 | 5 |

The current H tree contains only:
- `08-bmcp-protocol/`
- the two Phase 3.8.23 H/G mapping review files
- `workflows/`
- three workflow files

The current C tree contains only:
- `07-agent-integration/`
- the two Phase 3.8.23 C/G identity review files
- `workflows/`
- one workflow file

The compare results classify 205 H paths and 133 C paths as removed. This includes previously present governance, architecture, protocol, schema, tests, and review artifacts. The new commits are one commit ahead of their prior recorded heads, so this is not explained by a stale branch pointer or an unrelated merge-base comparison.

**No Owner branch was modified by this A review.** Do not treat the new H/C branch heads as complete project baselines until the owners restore the expected tree and prove the repair by exact compare/read-back.

## 2. Fresh baseline

| Ref | Current SHA |
|---|---|
| main | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` |
| H | `0277a8b9ee63be850acc0b8b1b08625524aaa33b` |
| C | `a5dff993e5c2928a28deb777c41023cfe923366f` |
| I | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` |
| D | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` |
| Storage | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` |

PR #87 and PR #70 remain open Draft PRs; neither is merged. This report does not update either PR.

## 3. What the new H/C review documents actually decide

### 3.1 H Phase 3.8.23 — Applied Delivery Evidence mapping

Exact files:
- `08-bmcp-protocol/phase-3.8.23-h-exact-review-g-applied-delivery-evidence-mapping.md`
- `08-bmcp-protocol/phase-3.8.23-h-exact-review-g-applied-delivery-evidence-mapping.zh-CN.md`

Blobs:
- EN: `be308261c3e000e712a3cdbd3dbf60507156127b`
- zh-CN: `641abd9b5a4ed271c3c4b561747c99d7cde79463`

H's recorded decision is **ACCEPT WITH ENUMERATED EXCEPTIONS** for identity semantics, while **WIRE MAPPING NOT FROZEN**. It explicitly distinguishes the existing Unified 1.2.15 C Provider Outcome Gateway Attestation from Adapter/Runtime Applied Delivery Evidence. The latter requires a separately versioned message family (candidate `bmcp.applied-delivery-evidence`, revision `1.0.0`) and a new schema, validator, vectors, tests, and CI evidence. The document explicitly says those successor artifacts are not implemented or verified.

Therefore this H decision does not close the missing H Applied Delivery Evidence wire path, does not establish an issuer implementation, and does not authorize global Applied freeze or production activation.

### 3.2 C Phase 3.8.23 — G Applied Persistence identity join

Exact files:
- `07-agent-integration/phase-3.8.23-c-exact-review-g-applied-persistence-identity.md`
- `07-agent-integration/phase-3.8.23-c-exact-review-g-applied-persistence-identity.zh-CN.md`

Blobs:
- EN: `4860c627b4d7e84e23fb39ad83411674f3b88c7b`
- zh-CN: `165d584778950e0cc8c3985d370bce1c6375755d`

C records **ACCEPT WITH ENUMERATED EXCEPTIONS** for the C-owned identity semantics against the exact G Phase 3.8.22 blobs. Its stated scope does not accept H wire mapping, COC/Storage restore semantics, I/D ordering, G persistence implementation, or global Applied freeze. Any change to either G target blob invalidates the decision.

This is useful delegated contract evidence, but it is not a broad acceptance of the complete cross-owner implementation.

## 4. Architecture and governance consequences

1. The H/C current branch trees are not acceptable as integration baselines because the recorded historical artifacts have disappeared from those refs.
2. The new H/C review notes may be inspected as standalone commit payloads, but their branch context is incomplete. Do not use the current H/C tree to infer that prior contracts/tests have been intentionally retired.
3. H's new decision confirms that Applied Delivery Evidence is a separate message family from the C Provider Outcome gateway-attestation family. Do not widen Unified 1.2.15 in place.
4. C's new decision is limited to the exact G identity contract. It does not close H, I, D, or Storage implementation and registration gates.
5. B-02 remains **PARTIAL / OPEN**. No Gate pass, freeze, protected-path implementation authorization, deployment, or production activation is recommended.

## 5. Required Owner remediation — no action taken by A

### H Owner
- Restore the expected H branch file tree from the correct pre-incident baseline without losing the Phase 3.8.23 EN/zh-CN decision.
- Submit a new incremental commit whose compare against the immediately preceding valid H HEAD contains only intended additions/changes.
- Provide recursive tree count, exact compare summary, and read-back of the preserved H protocol/schema/validator/tests/workflows.
- Continue the separately versioned Applied Delivery Evidence schema/validator/vectors/CI work; do not claim it complete until exact artifacts and CI are available.
- Separately provide issuer-side pre-sign execution evidence; the Phase 3.8.23 mapping decision is not issuer implementation evidence.

### C Owner
- Restore the expected C branch file tree from the correct pre-incident baseline without losing the Phase 3.8.23 EN/zh-CN decision.
- Submit a new incremental commit whose compare against the immediately preceding valid C HEAD contains only intended additions/changes.
- Provide recursive tree count, exact compare summary, and read-back of the preserved C schema, normative contract, crypto/status material, conformance tests, and prior reviews.
- Keep the Phase 3.8.23 decision scoped to the exact G target blobs; do not represent it as H wire or global Applied acceptance.

### A / Integration
- Re-run exact branch/tree comparisons after H and C report restoration.
- Revalidate PR #87 issuer-state-machine findings against the restored H tree.
- Obtain exact C review of the actual H Applied Delivery Evidence successor implementation when it exists.
- Keep I production profile/trust-root/key-custody/revocation/anti-rollback registration, D exact currentness/Forget seam review, and Storage successor manifest as separate gates.

## 6. Evidence and reproducibility

GitHub refs and compare inputs used:
- H branch: `session-h-bmcp-protocol`; prior `0d36324457e39bd50ad56ae902d477c4ea765b61`; current `0277a8b9ee63be850acc0b8b1b08625524aaa33b`.
- C branch: `session-c-agent-integration-2026-11-16`; prior `71047cdb51139ca4080ac67f451e38a48698859d`; current `a5dff993e5c2928a28deb777c41023cfe923366f`.
- H current tree SHA: `bdfa89d7d34714c8290929b21809509c91b055b7`.
- C current tree SHA: `c416650b01dd942d25b26f8fe15a0c7ff6bce849`.
- Main current SHA: `e52594f181d2edb77448adcfed64a0fbdffaf3aa`.

The compare counts above are GitHub compare API results; tree path counts are recursive Git tree API results. This report is an A-side integration finding, not a substitute for H/C Owner incident acknowledgment or repair.

---

## 中文结论

### 1. 总体裁决

H、C 两个 Owner 分支的最新提交不是安全的增量文档提交。它们的父提交分别是此前记录的 Owner HEAD，但新提交生成的 Git Tree 只剩少量路径：

| 分支 | 旧 HEAD | 当前 HEAD | 新增 | 删除 | 重命名 | 当前递归 Tree 路径数 |
|---|---|---|---:|---:|---:|---:|
| H | `0d36324457e39bd50ad56ae902d477c4ea765b61` | `0277a8b9ee63be850acc0b8b1b08625524aaa33b` | 2 | 205 | 3 | 7 |
| C | `71047cdb51139ca4080ac67f451e38a48698859d` | `a5dff993e5c2928a28deb777c41023cfe923366f` | 2 | 133 | 1 | 5 |

H 当前 Tree 仅保留两个 Phase 3.8.23 审查文件及三个 workflow 文件；C 当前 Tree 仅保留两个 Phase 3.8.23 审查文件及一个 workflow 文件。原有治理、架构、协议、Schema、测试和审查材料大量从当前分支 Tree 消失。

两个提交均是相对旧 HEAD 的单个后继提交，因此不能用“分支指针陈旧”或无关 Merge Base 差异解释。

**A 审查没有修改任何 Owner 分支。** 在 Owner 恢复预期文件树并通过精确 Compare/Read-back 前，不得把当前 H/C HEAD 当作完整项目基线。

### 2. 新增审查决议的真实范围

- H Phase 3.8.23：身份语义为 **ACCEPT WITH ENUMERATED EXCEPTIONS**，但 **WIRE MAPPING NOT FROZEN**。Unified 1.2.15 C Provider Outcome Gateway Attestation 与 Adapter/Runtime Applied Delivery Evidence 是不同消息族。后者必须使用独立版本化 Schema/Validator/向量/测试/CI；文档明确这些实现尚未完成。
- C Phase 3.8.23：仅针对精确 G Phase 3.8.22 Blob，对 C 所有的身份语义作 **ACCEPT WITH ENUMERATED EXCEPTIONS**。它不接受 H Wire Mapping、Storage Restore、I/D 顺序、G 持久化实现或全局 Applied Freeze。

这些审查文件有价值，但不能扩大解释为完整跨 Owner 实现已通过。

### 3. 必须先完成的恢复工作

**H Owner：** 从正确的事故前基线恢复原有文件树，保留 Phase 3.8.23 双语决议；重新提交纯增量提交；提供 Tree 数量、Compare 统计和原有 Schema/Validator/测试/workflow 读回证据；继续独立 Applied Delivery Evidence Schema/Validator/CI 与 Issuer pre-sign 执行证据。

**C Owner：** 从正确的事故前基线恢复原有文件树，保留 Phase 3.8.23 双语决议；重新提交纯增量提交；读回 C Schema、规范合同、Crypto/Status 材料、Conformance Tests 和历史审查；严格维持对 G 精确 Blob 的审查范围。

**A 总审查：** 等待恢复后重新进行 Tree/Compare 核验，再复审 PR #87 的 Issuer 结论；取得 C 对真实 H Successor 实现的精确审查；I、D、Storage 各自 Gate 继续独立开放。

**最终状态：B-02 仍为 PARTIAL / OPEN。不得宣称 Gate 通过、全局冻结、受保护路径实现授权、部署或生产启用。**
