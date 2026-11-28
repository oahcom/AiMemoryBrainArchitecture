---
title: "Nested gate_a_reconstruction declarations are not inspected by the blob-pin checker"
status: "OPEN"
classification: "checker-contract-gap"
discovered_at_commit: "daa935f7a7ecc808f1775be8cf153cf715961b08"
evidence:
  - "14-ai-development/work-items/AID-2026-100/manifest.yaml @ daa935f7a (nested baseline_and_source_evidence.gate_a_reconstruction[0])"
  - "scripts/ci/check_manifest_blob_pins.py @ daa935f7a (line 207 reads top-level only; lines 220-221 show the nested fallback used for authored_indexes)"
  - "scripts/ci/check_manifest_blob_pins.py --commit daa935f7a output (4 findings, none for gate_a_reconstruction)"
  - "git cat-file -e daa935f7a:04-memory-compiler/compiler-stage-contract.md (absent)"
related_baseline_ids:
  - "#33"
scope: "diagnostic"
---

# DEFECT-2 — Nested `gate_a_reconstruction` declarations are not inspected by the blob-pin checker

> 本记录只陈述调查结果。**尚未裁定修复方案，不构成 checker 变更授权，也不构成 manifest 修改授权。**

## 1. 三个事实必须分开看

### 事实 A — 底层路径缺失
`04-memory-compiler/compiler-stage-contract.md` 在目标 commit `daa935f7a` 中**不存在**；
`docs/en/04-memory-compiler/compiler-stage-contract.md` 存在。

### 事实 B — manifest 声明仍存在
AID-2026-100 仍声明（字段已迁入 `baseline_and_source_evidence`）：

```yaml
baseline_and_source_evidence:
  gate_a_reconstruction:
    - root: 04-memory-compiler/compiler-stage-contract.md
      reconstructed_root_blob: 1f79eeb40fb234423290f97fcce934e11bdca9bf
      disposition: REMOVED_FROM_PR_SCOPE_BY_OWNER_RULING_ON_OA_MERGE_2026_11_26_01
      note: The reconstruction was produced at commit cae1b31e and is retained there; ...
```

### 事实 C — checker 因读取位置不兼容而漏读
tip checker 第 207 行读取 `doc.get("gate_a_reconstruction")`（**仅顶层**）；
同一函数在 `authored_indexes` 上做了嵌套兼容（第 220–221 行）：

```python
source_evidence = as_mapping(doc.get("baseline_and_source_evidence"))
authored_indexes = source_evidence.get("authored_indexes", doc.get("authored_indexes", []))
```

`gate_a_reconstruction` 没有对应的嵌套回退。

**不得把事实 C 描述为「已修复」。**

## 2. 结果

- `daa935f7a` 上 main checker 输出 4 条 finding，**不含** #33
- 因此 #33 的消失不是「路径已恢复」，也不是「声明已撤回」，而是读取位置不兼容
- 同一 commit 上 `#1426` checker 因整套 `blob_pins[]` 模型报 384 条 UNCLASSIFIED，也未对该嵌套字段给出分类结论

## 3. 未决问题（本记录不裁定）

1. 修 checker 增加嵌套兼容，还是要求 manifest 把 `gate_a_reconstruction` 放回顶层？
2. `disposition: REMOVED_FROM_PR_SCOPE_BY_OWNER_RULING_…` 是否构成「不再校验该 pin」的正当豁免依据？（当前 checker 不读 `disposition`）
3. 未声明 `source_commit` / `commit`，`note` 中 `commit cae1b31e` 为短 SHA —— 是否满足 pin 的 scope 要求？

## 4. 复现

```
git cat-file -e daa935f7a:04-memory-compiler/compiler-stage-contract.md            # 不存在
git cat-file -e daa935f7a:docs/en/04-memory-compiler/compiler-stage-contract.md    # 存在
python scripts/ci/check_manifest_blob_pins.py --commit daa935f7a7ecc808f1775be8cf153cf715961b08
# 输出 4 条 finding，其中没有 gate_a_reconstruction
```
