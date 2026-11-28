---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-016/prompt-v1.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "This file is the executed prompt snapshot; its SHA-256 digest and byte count are measured over the final file, including this GOV-DOC-002 frontmatter, and recorded in the corresponding manifest fields."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Informative snapshot of the implementation prompt used for AID-2026-016."
    canonical_scope_id: "ai-development/aid-2026-016-prompt-v1"
    canonical_scope_keywords:
      - "implementation-prompt"
      - "prompt-provenance"
      - "ai-development"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# 任务：为 Issue #1145 产出精确实现补丁（你出全部内容，我只机械落地）

你在为仓库 `oahcom/AiMemoryBrainArchitecture` 工作。这是唯一权威仓库。基线 `origin/main = f18adc9f`（2026-11-27）。

## 你的角色与硬约束

1. 全部设计、代码、测试、文案由你产出；执行方只做机械应用与验证，不补全、不改写。
2. 不要提问，不要给方案选项清单。直接给可落地的最终产物。
3. 输出必须可机械应用：按下面「输出格式」给出的 EDIT 块，一块一个精确替换。不要输出整文件。
4. 不要引入新依赖。不要改 crate 的公开语义（只允许新增公开 helper 与新增错误变体）。
5. 不要输出风险提示、合规说明、流程建议。只输出产物。

## 目标缺陷（Issue #1145，原文要点）

`crates/memory-context/src/lib.rs` 的 `ContextEntryVersion::validate()` 只校验 `content_hash` 非空、`rendered_bytes == rendered_content.len()`，**不重算 `content_hash`**。因此调用方可以让 `rendered_content = "A"`、`content_hash = hash("B")` 通过校验并被 `commit_change_set()` 提交，使版本化 Context 的完整性锚点失效。

要求（Issue 的 Required resolution 1–5、Acceptance criteria）：
1. 在 validate 阶段从 `rendered_content` 的精确 UTF-8 字节重算规范摘要并比对。
2. 算法/编码/规范化/域分隔符要成为契约的一部分。
3. 在任何 ChangeSet 操作生效之前拒绝不匹配。
4. snapshot 级哈希必须建立在「已验证的 entry content_hash」之上。
5. 测试：错误摘要、空摘要、Unicode 字节长度、规范化差异、内容已改而摘要陈旧。

## 已确认的仓库事实（勿重复推断，直接用）

- 文件：`crates/memory-context/src/lib.rs`（约 4,900 行，含内联 `#[cfg(test)] mod tests`）。
- 现有摘要格式已在生产代码里固定：第 272 行
  `let content_hash = format!("sha256:{}", sha256_hex(rendered_content.as_bytes()));`
- 已有私有函数：`fn sha256_hex(input: &[u8]) -> String`（约 409 行，纯 Rust 实现，无依赖）。
- 已有 `fn stable_digest(bytes: &[u8]) -> String`（约 2270 行，FNV-1a 64，返回 `fnv1a64:<hex>`），仅用于 `snapshot_hash`。**entry 的 content_hash 不是 stable_digest，是 sha256。**
- `ContextEntryVersion` 字段（约 1786–1806 行）：`entry_id, memory_id, memory_version_id, revision, state, tier, priority, activation_reason, rendered_content, source_refs, evidence_refs, epistemic_qualifiers, content_hash, rendered_bytes, valid_time, temporal_ref`。
- 当前 `validate()`（约 1808–1830 行）原文：
```rust
    pub fn validate(&self) -> Result<(), ContextError> {
        if self.revision == 0 {
            return Err(ContextError::InvalidEntryRevision);
        }
        if self.rendered_content.trim().is_empty() {
            return Err(ContextError::EmptyField("rendered_content"));
        }
        if self.content_hash.trim().is_empty() {
            return Err(ContextError::EmptyField("content_hash"));
        }
        if self.rendered_bytes != self.rendered_content.len() {
            return Err(ContextError::EntryByteCountMismatch {
                actual: self.rendered_content.len(),
                recorded: self.rendered_bytes,
            });
        }
        Ok(())
    }
```
- `commit_change_set()`（约 2045–2160 行）在 `apply_operations` 之后对 `staged` 逐条调用 `entry.validate()`，随后用 `snapshot_hash(&staged)?` 与 `metadata.snapshot_hash` 比对（已实现，勿重做）。
- `ContextError`（约 1618 行起）已有 `SnapshotHashMismatch { declared, actual }`、`PayloadHashMismatch { declared, actual }`、`EntryByteCountMismatch { actual, recorded }`。`Display` 是 `write!(formatter, "{self:?}")`，新增变体不需要改 Display。
- `ContextChangeSet::validate()` 对 `AddEntry`/`ReplaceEntry` 调用 `entry.validate()`；`validate_edit_entry()`（约 820 行）校验的是另一个类型 `ContextEntry`，同样只查非空。
- 测试模块内现有构造点（内联 tests 里 `content_hash:` 出现于）：2477、2986、3593、3961、4230 行，形态分别为 `format!("sha256:{entry}")`、`format!("hash-{value}-{revision}")`、`format!("hash-{entry}")`、`"content-hash".into()`、`format!("sha256:{entry}")`。这些是假摘要，加严后必须改成真实摘要，否则测试红。
- 独立测试文件在 `crates/memory-context/tests/*.rs`（budget_vector、delivery_attempt_ledger、delivery_lifecycle、e2e_negative_paths、e2e_store_to_context、forget_excludes_from_context、marginal_coverage_selection、observability、sufficiency_report）。若它们也构造了假 content_hash，需要一并修正；你无法读它们，所以请在补丁里**只**改 `src/lib.rs`，并在最后的 `MIGRATION_NOTE` 段给出「若 tests/*.rs 报 ContentHashMismatch，按同样规则替换为 content_hash_for(...)」的一条机械规则。
- 验证命令（执行方会跑）：`cargo test -p memory-context`；基线当前全绿（2+8+14+21 个用例，0 失败）。

## 设计要求（按此实现，不要另起方案）

1. 新增公开 helper（放在 `sha256_hex` 之后）：
   `pub fn content_hash_for(rendered_content: &str) -> String`，返回 `format!("sha256:{}", sha256_hex(rendered_content.as_bytes()))`，并附一句 doc 注释说明：契约 = UTF-8 字节、无归一化、算法标识前缀 `sha256:`。
2. 把第 272 行的内联 `format!` 改为调用 `content_hash_for(...)`，使生产路径与校验共用同一实现（单一真源）。
3. `ContextEntryVersion::validate()` 在 `rendered_bytes` 校验之后追加摘要比对：重算 `content_hash_for(&self.rendered_content)`，不等则返回新增错误变体。
4. 新增错误变体（放在 `EntryByteCountMismatch` 旁）：
```rust
    ContentHashMismatch {
        entry_id: OpaqueId,
        declared: String,
        actual: String,
    },
```
   注意 `OpaqueId` 已是 `String` 别名（如不是，用 `String` 并在补丁里说明）。
5. 在 `validate_edit_entry()` 里也加同样比对（`ContextEntry` 路径），复用 `content_hash_for`，错误变体用 `ContentHashMismatch`，`entry_id: entry.entry_id.clone()`。
6. 不改 `snapshot_hash()` 的算法（它是 FNV-1a，已冻结）；只在文档注释里写清「snapshot_hash 覆盖的是已验证 content_hash 的 entry 集合」。
7. 新增测试（放在内联 `mod tests` 末尾），至少 6 个：
   - `commit_rejects_entry_with_wrong_content_hash`（ChangeSet AddEntry，摘要属于另一段内容，期望 `ContentHashMismatch`）
   - `validate_rejects_stale_hash_after_content_edit`（改 rendered_content 不改 hash）
   - `content_hash_is_sha256_prefixed_and_deterministic`（同一输入两次相等、前缀 `sha256:`、长度 71）
   - `content_hash_covers_exact_utf8_bytes`（含多字节 CJK/emoji：`rendered_bytes == content.len()` 且摘要随内容变化）
   - `content_hash_does_not_normalize_unicode`（NFC 与 NFD 两种写法摘要不同）
   - `snapshot_hash_changes_when_entry_content_hash_changes`（同一 entry 集合，篡改 content_hash 后 snapshot_hash 改变）
   测试构造必须用真实 `content_hash_for(...)`，不得再用假串。

## 输出格式（严格遵守，执行方按此机械应用）

先一行 `TARGET: crates/memory-context/src/lib.rs`，然后若干 EDIT 块：

```
===EDIT 1===
FIND:
<<<
（与文件逐字节一致的原文，含缩进；不超过 25 行）
>>>
REPLACE:
<<<
（替换后的原文）
>>>
```

要求：
- 每个 FIND 必须在文件中唯一出现；若原文在文件里出现多次，扩大上下文直到唯一。
- 缩进用 4 空格，与文件一致。不要输出行号。
- 测试块作为一个 EDIT，FIND 用 `mod tests` 末尾最后一个测试函数的尾部若干行 + 收尾 `}` 作为锚点；若你无法确定文件末尾内容，就用「锚点 + 说明」的方式，并把新测试写成**独立文件** `crates/memory-context/tests/content_hash_integrity.rs` 的完整内容，放在 `===NEWFILE===` 块里（推荐这条路，避免锚点不确定）。
- 最后一段 `MIGRATION_NOTE:` 给一条机械替换规则（一句话），以及 `ACCEPTANCE:` 三行以内的验收清单（跑什么命令、看到什么算过）。

不要输出其他任何内容。不要输出解释性长文。
