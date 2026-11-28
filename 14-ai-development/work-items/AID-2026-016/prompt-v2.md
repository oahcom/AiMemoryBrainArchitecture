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
        - "14-ai-development/work-items/AID-2026-016/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "This is the second implementation prompt snapshot; its source body is copied verbatim and its final assembled SHA-256 and byte count are recorded in the work-item manifest."
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
    canonical_scope: "Informative snapshot of the second implementation prompt used for the AID-2026-016 post-review corrections."
    canonical_scope_id: "ai-development/aid-2026-016-prompt-v2"
    canonical_scope_keywords:
      - "implementation-prompt"
      - "post-review-correction"
      - "prompt-provenance"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
<!-- BODY-COPIED-VERBATIM-BY-EXECUTOR -->
# 任务：修掉 #1145 复核的两个阻断项（你出 EDIT 块，执行方机械应用）

上一轮你已产出 #1145 的实现（`content_hash_for` + 双路径校验 + 6 个测试），已在 `731d9d08` 上全绿。独立复核用**变异测试**证明了两个缺口。现在只修缺口，不要重写已通过的部分。

## 硬约束

1. 全部代码由你产出；执行方只按 `===EDIT n===` / `===NEWFILE===` 机械应用。
2. 不要提问、不要选项、不要风险提示。直接给可应用的块。
3. 不要改 `snapshot_hash` 算法，不要动 FNV-1a，不要加依赖，不要改公开签名（除本任务明确要求）。
4. 每个 FIND 必须在文件里唯一；若唯一性无法保证，扩大上下文。
5. 测试必须真的咬住实现：任何一处校验被删掉，都必须有测试变红。

## 复核实测事实（变异测试结果，均为真实运行）

基线 `cargo test -p memory-context --no-fail-fast`：183 passed / 0 failed。

| 变异 | 结果 | 含义 |
|---|---|---|
| M1 删 `ContextEntryVersion::validate` 里的哈希比对（现 1844-1851） | 2 红：`commit_rejects_entry_with_wrong_content_hash`、`validate_rejects_stale_hash_after_content_edit` | 该分支有覆盖 |
| M2 删 `validate_edit_entry` 里的哈希比对（现 835-842） | **0 红，183 passed** | 该分支零覆盖 |
| M3 `content_hash_for` 前缀 `sha256:` → `sha256x:` | 2 红：`pr433_tests::update_entry_recomputes_rendered_bytes_and_content_hash`、`content_hash_is_sha256_prefixed_and_deterministic` | 契约被咬住 |
| M4 删 `ContextEntryVersion::validate` 里的**空摘要**检查（现 1835-1837） | **0 红，183 passed** | 空摘要零覆盖 |

逐测试判定（复核结论）：
- `commit_rejects_entry_with_wrong_content_hash`（`tests/content_hash_integrity.rs:28-36`）：**名不副实**——它只调 `value.validate()`，完全没走 `commit_change_set`/`ContextChangeSet`。名字承诺的 commit 级拒绝无覆盖。
- `content_hash_covers_exact_utf8_bytes`（L61-68）：只做相对比较，若实现改成「先 trim 再哈希」仍然绿。
- 其余 4 个达标。

跨 crate 契约断裂（探针实证）：
- `crates/brain-cli/src/main.rs:729` 用自己的 `sha256_hex`（`main.rs:920-929`）产出**裸 64 hex、无 `sha256:` 前缀**的 `content_hash`；该值经 `build_context`（`memory-context/src/lib.rs:1595` 原样透传）进入 `ContextEntryVersion`，被新校验判为 `ContentHashMismatch`。探针测试已证实 `value.validate()` 返回 `ContentHashMismatch`。
- 结论：`brain-cli` 现在会产出**自己校验不通过**的 Context entry，且没有任何测试守护。

## 要产出的改动

### 1. 让 `commit_rejects_entry_with_wrong_content_hash` 真的走 commit 路径
在 `tests/content_hash_integrity.rs` 里把它重写成：构造 `ContextHead` + `ContextChangeSet`（`status: Prepared`、`base_version` 与 head 一致、`policy_epoch` 与 `authorization_epoch` 一致、`AddEntry` 携带错误摘要的 `ContextEntryVersion`），调 `commit_change_set(...)`，断言返回 `Err(ContextError::ContentHashMismatch { .. })`。
若该测试文件缺少构造 helper，允许新增最小 helper；若 `commit_change_set` 需要 `IdempotencyLog` 与 `VersionMetadata`，一并构造（`snapshot_hash` 可用 `snapshot_hash(&[])`/实际条目计算，勿硬编码假值）。
**注意**：错误必须在 apply 之前返回，因此断言 `commit_change_set` 返回 Err 且 `IdempotencyLog` 未被写入（`idempotency.is_empty()`）。

### 2. 覆盖 `validate_edit_entry` 路径（M2 必须变红）
新增测试（放 `tests/content_hash_integrity.rs`）：构造一个 `ContextChangeSet`，其 `Reconcile`（或 `ReplaceEntry`）携带 `ContextEntry`（注意是 `ContextEntry`，走 `validate_edit_entry`）且 `content_hash` 与 `rendered_content` 不匹配，断言 `change_set.validate()` 返回 `Err(ContentHashMismatch)`。测试名：`change_set_validate_rejects_edit_entry_with_wrong_content_hash`。

### 3. 覆盖空摘要（M4 必须变红）
新增测试：`validate_rejects_empty_content_hash`——`content_hash` 设为空串（或全空白），断言 `Err(ContextError::EmptyField("content_hash"))`。

### 4. 锁死「不 trim、不归一化」
在 `content_hash_covers_exact_utf8_bytes` 里追加断言：`content_hash_for("a ") != content_hash_for("a")` 且 `content_hash_for(" a") != content_hash_for("a")`（若该测试已存在则改为追加，不要新建重复测试）。

### 5. 修 `crates/brain-cli/src/main.rs` 的裸 hex
把 `main.rs:729` 附近的 `content_hash` 构造改为调用 `memory_context::content_hash_for(...)`（若 `brain-cli` 尚未依赖该 crate，请改为在 `brain-cli` 内部产出 `sha256:` 前缀并说明为什么这样等价；**优先**用已依赖的 `memory_context`）。
同时检查 `main.rs:920-929` 的本地 `sha256_hex` 是否还有其它调用点：若仅此一处，删除该本地实现；若还有其它用途，保留但注明「非 content_hash 用途」。
若因此需要在 `Cargo.toml` 加依赖，说明并给出精确改动（只允许 workspace 内 crate 依赖，不允许新第三方依赖）。

### 6. 不做的事
- 不加 `#[non_exhaustive]`（会改公开语义）。
- 不改 `snapshot_hash` 的 FNV-1a。
- 不重命名已通过的测试。
- 不改 `ContextCandidate::validate_for`（它只查非空，属候选阶段，Issue 未要求）。

## 输出格式

```
===EDIT 1===
FILE: crates/memory-context/tests/content_hash_integrity.rs
FIND:
<<<
（逐字节原文）
>>>
REPLACE:
<<<
（替换后）
>>>
```

- `FILE:` 行必须有。`===NEWFILE===` 块格式：`FILE:` 行 + 空行 + 完整文件内容。
- 若某个测试需要整体替换，FIND 用该测试函数从头到尾的完整原文。
- 最后给 `ACCEPTANCE:` 三行以内（跑什么命令、期望什么结果），以及 `MUTATION:` 两行说明「删掉哪一处校验后哪个测试必须变红」。
不要输出其他内容。


---

## 附：需要你改动的源码原文

以下全部为当前 worktree（路径 `D:\code\wt-1145`，HEAD `731d9d08`，分支 `fix/2026-11-27-aid-252-content-hash-v2`）里的**真实文件内容**，逐字节照抄；标注的行号就是文件真实行号，`FIND` 块请直接从这里取。

### 现状补充事实（复核过，直接采信）

1. `crates/memory-context/Cargo.toml` **没有** `sha2` 依赖，`content_hash_for` 用的是 crate 内部自写的 `sha256_hex`（段 D）。
2. `crates/brain-cli/Cargo.toml` **已经**依赖 `memory-context`（L20），也直接依赖 `sha2`（L24）。
3. `crates/brain-cli/src/main.rs` 的本地 `sha256_hex` 还有两个**非 content_hash** 用途：L559（`payload_digest`）与 L609（`content_digest`），两处都需要裸 hex，不能带 `sha256:` 前缀。
4. `build_context` 在 L1595 把 `candidate.content_hash` 原样搬进 `ContextEntryVersion.content_hash`（段 P）。
5. **上一轮提示词里「`ContextChangeSet` 的 `Reconcile`」不成立**：`Reconcile` 只存在于旧 `ChangeSet`/`ChangeSetOperation`（段 L），而 `validate_edit_entry` 的调用点是 `ChangeSet::validate` 的 `Update`/`Replace`（L770）与 `Reconcile`（L808）。`ContextChangeSet.operations` 里装的是 `ContextEntryVersion`（走 `ContextEntryVersion::validate`）。写 M2 的测试请按段 K/L 的真实类型来。
6. `crates/memory-context/tests/` 现有 10 个文件：budget_vector、content_hash_integrity、delivery_attempt_ledger、delivery_lifecycle、e2e_negative_paths、e2e_store_to_context、forget_excludes_from_context、marginal_coverage_selection、observability、sufficiency_report。
7. `ContextError` 相关变体原文名：`EmptyField(&'static str)`、`ContentHashMismatch { entry_id, declared, actual }`、`EntryByteCountMismatch { actual, recorded }`（段 B/C 可见用法）。

### A. `crates/memory-context/tests/content_hash_integrity.rs` L1-89

全文（M2/M3/M4 的落点；当前 6 个测试）

```rust
use memory_context::{
    content_hash_for, snapshot_hash, ContextEntryVersion, ContextError, ContextTier, EntryState,
};
use memory_domain::OpaqueId;

fn entry(content: &str) -> ContextEntryVersion {
    ContextEntryVersion {
        entry_id: OpaqueId::new("entry-test").unwrap(),
        memory_id: OpaqueId::new("memory-test").unwrap(),
        memory_version_id: OpaqueId::new("version-test").unwrap(),
        revision: 1,
        state: EntryState::Active,
        tier: ContextTier::P1,
        priority: 10,
        activation_reason: "test".into(),
        rendered_content: content.into(),
        source_refs: vec![OpaqueId::new("source-test").unwrap()],
        evidence_refs: vec![],
        epistemic_qualifiers: vec![],
        content_hash: content_hash_for(content),
        rendered_bytes: content.len(),
        valid_time: None,
        temporal_ref: None,
    }
}

#[test]
fn commit_rejects_entry_with_wrong_content_hash() {
    let mut value = entry("A");
    value.content_hash = content_hash_for("B");

    assert!(matches!(
        value.validate(),
        Err(ContextError::ContentHashMismatch { .. })
    ));
}

#[test]
fn validate_rejects_stale_hash_after_content_edit() {
    let mut value = entry("original");
    value.rendered_content = "modified".into();
    value.rendered_bytes = value.rendered_content.len();

    assert!(matches!(
        value.validate(),
        Err(ContextError::ContentHashMismatch { .. })
    ));
}

#[test]
fn content_hash_is_sha256_prefixed_and_deterministic() {
    let first = content_hash_for("deterministic content");
    let second = content_hash_for("deterministic content");

    assert_eq!(first, second);
    assert!(first.starts_with("sha256:"));
    assert_eq!(first.len(), 71);
}

#[test]
fn content_hash_covers_exact_utf8_bytes() {
    let content = "中文内容 🧠🌏";
    let value = entry(content);

    assert_eq!(value.rendered_bytes, content.len());
    assert_eq!(value.content_hash, content_hash_for(content));
    assert_ne!(value.content_hash, content_hash_for("中文内容"));
}

#[test]
fn content_hash_does_not_normalize_unicode() {
    let nfc = "é";
    let nfd = "e\u{0301}";

    assert_ne!(nfc, nfd);
    assert_ne!(content_hash_for(nfc), content_hash_for(nfd));
}

#[test]
fn snapshot_hash_changes_when_entry_content_hash_changes() {
    let original = entry("snapshot content");
    let mut modified = original.clone();
    modified.content_hash = content_hash_for("different content");

    assert_ne!(
        snapshot_hash(&[original]).unwrap(),
        snapshot_hash(&[modified]).unwrap()
    );
}
```

### B. `crates/memory-context/src/lib.rs` L1807-1876

ContextEntryVersion 结构 + impl validate（M1 哈希比对 1844-1851、M4 空摘要检查 1835-1837 都在此）

```rust
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextEntryVersion {
    pub entry_id: OpaqueId,
    pub memory_id: OpaqueId,
    pub memory_version_id: OpaqueId,
    pub revision: u64,
    pub state: EntryState,
    pub tier: ContextTier,
    pub priority: i32,
    pub activation_reason: String,
    pub rendered_content: String,
    pub source_refs: Vec<OpaqueId>,
    pub evidence_refs: Vec<OpaqueId>,
    pub epistemic_qualifiers: Vec<String>,
    pub content_hash: String,
    pub rendered_bytes: usize,
    pub valid_time: Option<TimeValue>,
    pub temporal_ref: Option<TemporalRef>,
}

impl ContextEntryVersion {
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
        let actual = content_hash_for(&self.rendered_content);
        if self.content_hash != actual {
            return Err(ContextError::ContentHashMismatch {
                entry_id: self.entry_id.clone(),
                declared: self.content_hash.clone(),
                actual,
            });
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum ContextOperation {
    AddEntry {
        operation_id: String,
        entry: ContextEntryVersion,
    },
    ReplaceEntry {
        operation_id: String,
        entry: ContextEntryVersion,
        expected_revision: u64,
    },
    RemoveEntry {
        operation_id: String,
        entry_id: OpaqueId,
        expected_revision: u64,
    },
    ReorderEntries {
        operation_id: String,
        entry_ids: Vec<OpaqueId>,
    },
}
```

### C. `crates/memory-context/src/lib.rs` L819-844

validate_edit_entry（M2 哈希比对 835-842 在此；上一轮零覆盖）

```rust
fn validate_edit_entry(entry: &ContextEntry) -> Result<(), ContextError> {
    if entry.rendered_content.trim().is_empty() {
        return Err(ContextError::EmptyField("rendered_content"));
    }
    if entry.content_hash.trim().is_empty() {
        return Err(ContextError::EmptyField("content_hash"));
    }
    if entry.source_refs.is_empty() {
        return Err(ContextError::MissingLineage);
    }
    if entry.rendered_bytes != entry.rendered_content.len() {
        return Err(ContextError::EntryByteCountMismatch {
            actual: entry.rendered_content.len(),
            recorded: entry.rendered_bytes,
        });
    }
    let actual = content_hash_for(&entry.rendered_content);
    if entry.content_hash != actual {
        return Err(ContextError::ContentHashMismatch {
            entry_id: entry.entry_id.clone(),
            declared: entry.content_hash.clone(),
            actual,
        });
    }
    Ok(())
}
```

### D. `crates/memory-context/src/lib.rs` L405-496

内部 sha256_hex + content_hash_for（M3 前缀在 495）

```rust
    Ok(())
}

/// Dependency-free SHA-256 used to refresh the digest of edited rendered content.
fn sha256_hex(input: &[u8]) -> String {
    const K: [u32; 64] = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4,
        0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe,
        0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f,
        0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc,
        0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
        0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116,
        0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7,
        0xc67178f2,
    ];
    let mut msg = input.to_vec();
    let bit_len = (input.len() as u64).wrapping_mul(8);
    msg.push(0x80);
    while msg.len() % 64 != 56 {
        msg.push(0);
    }
    msg.extend_from_slice(&bit_len.to_be_bytes());
    let mut h = [
        0x6a09e667u32,
        0xbb67ae85,
        0x3c6ef372,
        0xa54ff53a,
        0x510e527f,
        0x9b05688c,
        0x1f83d9ab,
        0x5be0cd19,
    ];
    for chunk in msg.as_chunks::<64>().0 {
        let mut w = [0u32; 64];
        for (i, word) in w.iter_mut().take(16).enumerate() {
            let j = i * 4;
            *word = u32::from_be_bytes([chunk[j], chunk[j + 1], chunk[j + 2], chunk[j + 3]]);
        }
        for i in 16..64 {
            let x = w[i - 15];
            let y = w[i - 2];
            let s0 = x.rotate_right(7) ^ x.rotate_right(18) ^ (x >> 3);
            let s1 = y.rotate_right(17) ^ y.rotate_right(19) ^ (y >> 10);
            w[i] = w[i - 16]
                .wrapping_add(s0)
                .wrapping_add(w[i - 7])
                .wrapping_add(s1);
        }
        let [mut a, mut b, mut c, mut d, mut e, mut f, mut g, mut hh] = h;
        for i in 0..64 {
            let s1 = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
            let ch = (e & f) ^ (!e & g);
            let t1 = hh
                .wrapping_add(s1)
                .wrapping_add(ch)
                .wrapping_add(K[i])
                .wrapping_add(w[i]);
            let s0 = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
            let maj = (a & b) ^ (a & c) ^ (b & c);
            let t2 = s0.wrapping_add(maj);
            hh = g;
            g = f;
            f = e;
            e = d.wrapping_add(t1);
            d = c;
            c = b;
            b = a;
            a = t1.wrapping_add(t2);
        }
        h[0] = h[0].wrapping_add(a);
        h[1] = h[1].wrapping_add(b);
        h[2] = h[2].wrapping_add(c);
        h[3] = h[3].wrapping_add(d);
        h[4] = h[4].wrapping_add(e);
        h[5] = h[5].wrapping_add(f);
        h[6] = h[6].wrapping_add(g);
        h[7] = h[7].wrapping_add(hh);
    }
    let mut out = String::with_capacity(64);
    for word in h {
        out.push_str(&format!("{word:08x}"));
    }
    out
}

/// Returns the canonical content digest: exact UTF-8 bytes, without normalization,
/// using SHA-256 and the `sha256:` algorithm identifier prefix.
pub fn content_hash_for(rendered_content: &str) -> String {
    format!("sha256:{}", sha256_hex(rendered_content.as_bytes()))
}
```

### E. `crates/brain-cli/src/main.rs` L689-757

compile 路径：ContextCandidate 构造，L729 用本地 sha256_hex 产出裸 64 hex（阻断项 1 的现场）

```rust
    let snapshot = {
        let sqlite = SqliteMemoryStorage::open(storage_database_path)
            .map_err(|error| format!("cannot open SQLite storage: {error:?}"))?;
        let mut store = MemoryStore::new(sqlite);

        store
            .create_memory(memory.clone(), &input.event.scope_refs)
            .map_err(|error| format!("create_memory failed: {error:?}"))?;
        store
            .write_revision(
                RevisionWrite {
                    memory_id: memory.memory_id.clone(),
                    expected_current_version: None,
                    revision,
                    idempotency_key,
                    request_digest: content_digest,
                },
                &input.event.scope_refs,
            )
            .map_err(|error| format!("write_revision failed: {error:?}"))?;

        let current = store
            .read_current(&memory.memory_id, &input.event.scope_refs)
            .map_err(|error| format!("read_current failed: {error:?}"))?
            .ok_or_else(|| "read_current returned no revision".to_owned())?;
        let claim = current
            .claims
            .first()
            .ok_or_else(|| "stored revision contains no Claim".to_owned())?;
        let rendered_content = serde_json::to_string(claim)
            .map_err(|error| format!("cannot serialize Claim: {error}"))?;
        let candidate = ContextCandidate {
            entry_id: claim.claim_id.clone(),
            memory_id: current.memory_id.clone(),
            memory_version_id: current.memory_version_id.clone(),
            memory_lifecycle: memory.lifecycle_state.clone(),
            scope_refs: claim.scope_refs.clone(),
            tier: ContextTier::P0,
            priority: 0,
            activation_reason: format!("source event {}", input.event.event_id.as_str()),
            content_hash: sha256_hex(rendered_content.as_bytes()),
            rendered_content,
            source_refs: current.source_refs.clone(),
            evidence_refs: claim.evidence_refs.clone(),
            epistemic_qualifiers: claim.qualifiers.clone(),
        };
        let identity = ContextIdentity {
            context_id: input.context.context_id,
            scope_refs: input.event.scope_refs.clone(),
            agent_id: input.context.agent_id,
            agent_instance_id: input.context.agent_instance_id,
            session_id: input.context.session_id,
            task_id: input.context.task_id,
            environment_id: input.context.environment_id,
            purpose: input.context.purpose,
            schema_version: input.context.schema_version,
        };

        build_context(
            identity,
            1,
            ContextBudget {
                max_entries: 64,
                max_rendered_bytes: 1_048_576,
            },
            vec![candidate],
        )
        .map_err(|error| format!("build_context failed: {error:?}"))?
    };
```

### F. `crates/brain-cli/src/main.rs` L895-954

本地 sha256_hex 定义（920-929）、usage()、以及 main.rs 内仅有的 #[cfg(test)] 模块（943-954）

```rust
            let sequence = store
                .forget_version(&memory_id, &version_id, &reason_digest, &scope)
                .map_err(|error| format!("forget_version failed: {error:?}"))?;
            (
                "Version",
                format!(
                    "memory={} version={}",
                    memory_id.as_str(),
                    version_id.as_str()
                ),
                sequence,
            )
        }
        None => {
            let sequence = store
                .forget_memory(&memory_id, &reason_digest, &scope)
                .map_err(|error| format!("forget_memory failed: {error:?}"))?;
            ("Memory", format!("memory={}", memory_id.as_str()), sequence)
        }
    };

    println!("forget applied: target={target} {detail} fence_sequence={fence_sequence}");
    Ok(())
}

fn sha256_hex(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let digest = Sha256::digest(bytes);
    let mut output = String::with_capacity(64);
    for byte in digest {
        output.push(HEX[(byte >> 4) as usize] as char);
        output.push(HEX[(byte & 0x0f) as usize] as char);
    }
    output
}

fn usage() -> String {
    concat!(
        "usage: brain compile --input <event.json> --out <context.json> [--verbose]\n",
        "       [--store <memory.sqlite>] [--event-store <events.sqlite>]\n",
        "         --store       write the memory database to this path and keep it.\n",
        "                       Without it the database is temporary and removed on exit.\n",
        "usage: brain forget --store <memory.sqlite> --scope <scope.json> ",
        "--forget <memory_id> --forget-reason <digest> [--forget-version <version_id>]"
    )
    .to_owned()
}

#[cfg(test)]
mod tests {
    use super::sha256_hex;

    #[test]
    fn sha256_output_is_stable() {
        assert_eq!(
            sha256_hex(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
    }
}
```

### G. `crates/brain-cli/Cargo.toml` L1-24

全文（已依赖 memory-context，L20；sha2 见 L24）

```toml
[package]
name = "brain-cli"
version = "0.1.0"
edition = "2021"
license = "UNLICENSED"
publish = false

[[bin]]
name = "brain"
path = "src/main.rs"

[dependencies]
agent-integration = { path = "../agent-integration" }
memory-domain = { path = "../memory-domain" }
memory-storage = { path = "../memory-storage" }
memory-storage-sqlite = { path = "../memory-storage-sqlite" }
memory-store = { path = "../memory-store" }
memory-event-store = { path = "../memory-event-store" }
memory-event-store-sqlite = { path = "../memory-event-store-sqlite" }
memory-context = { path = "../memory-context" }
memory-compiler = { path = "../memory-compiler" }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
sha2 = "0.10"
```

### H. `crates/memory-context/src/lib.rs` L1769-1784

ContextHead 结构与 validate（commit 测试的入参）

```rust
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextHead {
    pub context_id: OpaqueId,
    pub version: Option<ContextVersionId>,
    pub sequence: u64,
}

impl ContextHead {
    pub fn validate(&self) -> Result<(), ContextError> {
        match (&self.version, self.sequence) {
            (None, 0) => Ok(()),
            (Some(version), sequence) if !version.as_str().is_empty() && sequence > 0 => Ok(()),
            _ => Err(ContextError::InvalidVersion),
        }
    }
}
```

### I. `crates/memory-context/src/lib.rs` L1889-1974

ChangeSetStatus、ContextChangeSet 结构（status/policy_epoch/payload_hash/idempotency_key 字段）、compute_payload_hash、validate

```rust
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum ChangeSetStatus {
    Prepared,
    Committed,
    Rejected,
    Superseded,
    Abandoned,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextChangeSet {
    pub change_set_id: ChangeSetId,
    pub context_id: OpaqueId,
    pub base_version: Option<ContextVersionId>,
    pub target_version: Option<ContextVersionId>,
    pub operations: Vec<ContextOperation>,
    pub reason: String,
    pub actor_ref: ActorRef,
    pub created_at: String,
    pub idempotency_key: String,
    pub payload_hash: String,
    pub policy_epoch: u64,
    pub status: ChangeSetStatus,
    pub correlation_id: Option<String>,
    pub causation_id: Option<String>,
    pub result_ref: Option<String>,
}

impl ContextChangeSet {
    pub fn compute_payload_hash(&self) -> Result<String, ContextError> {
        let payload = (
            &self.change_set_id,
            &self.context_id,
            &self.base_version,
            &self.target_version,
            &self.operations,
            &self.policy_epoch,
        );
        let bytes = serde_json::to_vec(&payload)
            .map_err(|error| ContextError::Serialization(error.to_string()))?;
        Ok(stable_digest(&bytes))
    }

    pub fn validate(&self) -> Result<(), ContextError> {
        if self.reason.trim().is_empty() {
            return Err(ContextError::EmptyField("reason"));
        }
        if self.created_at.trim().is_empty() {
            return Err(ContextError::EmptyField("created_at"));
        }
        if self.idempotency_key.trim().is_empty() {
            return Err(ContextError::EmptyField("idempotency_key"));
        }
        if self.payload_hash.trim().is_empty() {
            return Err(ContextError::EmptyField("payload_hash"));
        }
        if self.operations.is_empty() {
            return Err(ContextError::InvalidOperation);
        }
        if self.target_version.is_some() && self.status == ChangeSetStatus::Prepared {
            return Err(ContextError::TargetVersionAlreadySet);
        }
        let mut operation_ids = HashSet::new();
        for operation in &self.operations {
            if operation.operation_id().trim().is_empty() {
                return Err(ContextError::EmptyField("operation_id"));
            }
            if !operation_ids.insert(operation.operation_id()) {
                return Err(ContextError::DuplicateOperationId);
            }
            match operation {
                ContextOperation::AddEntry { entry, .. } => entry.validate()?,
                ContextOperation::ReplaceEntry { entry, .. } => entry.validate()?,
                ContextOperation::RemoveEntry {
                    expected_revision, ..
                } if *expected_revision == 0 => return Err(ContextError::InvalidEntryRevision),
                _ => {}
            }
        }
        let actual = self.compute_payload_hash()?;
        if actual != self.payload_hash {
            return Err(ContextError::PayloadHashMismatch {
                declared: self.payload_hash.clone(),
                actual,
            });
        }
```

### J. `crates/memory-context/src/lib.rs` L2018-2200

VersionMetadata、CommitOutcome、IdempotencyLog、commit_change_set 全文、validate_unique_entries

```rust
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct VersionMetadata {
    pub context_version_id: ContextVersionId,
    pub schema_version: String,
    pub scope_fingerprint: String,
    pub canonical_watermarks: Vec<CanonicalWatermark>,
    pub policy_epoch: u64,
    pub snapshot_ref: String,
    pub snapshot_hash: String,
    pub budget_summary: ContextBudgetSummary,
    pub committed_at: String,
    pub actor_ref: ActorRef,
    pub reason: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum CommitOutcome {
    Committed {
        version: ContextVersion,
        entries: Vec<ContextEntryVersion>,
    },
    Replayed {
        version: ContextVersion,
        entries: Vec<ContextEntryVersion>,
    },
}

#[derive(Clone, Debug, Default)]
pub struct IdempotencyLog {
    records: HashMap<(String, String), IdempotencyRecord>,
}

#[derive(Clone, Debug)]
struct IdempotencyRecord {
    payload_hash: String,
    version: ContextVersion,
    entries: Vec<ContextEntryVersion>,
}

impl IdempotencyLog {
    pub fn len(&self) -> usize {
        self.records.len()
    }

    pub fn is_empty(&self) -> bool {
        self.records.is_empty()
    }
}

pub fn commit_change_set(
    head: &ContextHead,
    change_set: ContextChangeSet,
    current_entries: &[ContextEntryVersion],
    idempotency: &mut IdempotencyLog,
    authorization_epoch: u64,
    metadata: VersionMetadata,
) -> Result<CommitOutcome, ContextError> {
    head.validate()?;
    change_set.validate()?;
    if change_set.status != ChangeSetStatus::Prepared {
        return Err(ContextError::ChangeSetNotPrepared);
    }
    if change_set.context_id != head.context_id {
        return Err(ContextError::ContextMismatch);
    }
    if change_set.base_version != head.version {
        return Err(ContextError::BaseVersionMismatch);
    }
    if metadata.policy_epoch != authorization_epoch
        || change_set.policy_epoch != authorization_epoch
    {
        return Err(ContextError::PolicyEpochStale {
            expected: authorization_epoch,
            actual: metadata.policy_epoch,
        });
    }

    let principal_scope = change_set.actor_ref.actor_id.as_str().to_owned();
    let idempotency_key = (principal_scope, change_set.idempotency_key.clone());
    if let Some(record) = idempotency.records.get(&idempotency_key) {
        if record.payload_hash != change_set.payload_hash {
            return Err(ContextError::IdempotencyConflict);
        }
        return Ok(CommitOutcome::Replayed {
            version: record.version.clone(),
            entries: record.entries.clone(),
        });
    }

    let sequence = head
        .sequence
        .checked_add(1)
        .ok_or(ContextError::SequenceOverflow)?;
    let mut staged = current_entries.to_vec();
    validate_unique_entries(&staged)?;
    apply_operations(&mut staged, &change_set.operations)?;
    validate_unique_entries(&staged)?;
    for entry in &staged {
        entry.validate()?;
    }

    let actual_snapshot_hash = snapshot_hash(&staged)?;
    if metadata.snapshot_hash != actual_snapshot_hash {
        return Err(ContextError::SnapshotHashMismatch {
            declared: metadata.snapshot_hash,
            actual: actual_snapshot_hash,
        });
    }

    let rendered_bytes = staged
        .iter()
        .try_fold(0usize, |sum, entry| sum.checked_add(entry.rendered_bytes))
        .ok_or(ContextError::BudgetSummaryMismatch)?;
    let actual_summary = ContextBudgetSummary {
        entry_count: staged.len(),
        rendered_bytes,
    };
    if metadata.budget_summary != actual_summary {
        return Err(ContextError::BudgetSummaryMismatch);
    }

    for (field, value) in [
        ("schema_version", metadata.schema_version.as_str()),
        ("scope_fingerprint", metadata.scope_fingerprint.as_str()),
        ("snapshot_ref", metadata.snapshot_ref.as_str()),
        ("committed_at", metadata.committed_at.as_str()),
        ("reason", metadata.reason.as_str()),
    ] {
        if value.trim().is_empty() {
            return Err(ContextError::EmptyField(field));
        }
    }
    validate_watermarks(&metadata.canonical_watermarks)?;

    let version = ContextVersion {
        context_version_id: metadata.context_version_id,
        context_id: head.context_id.clone(),
        sequence,
        parent_version_id: head.version.clone(),
        snapshot_ref: metadata.snapshot_ref,
        snapshot_hash: metadata.snapshot_hash,
        schema_version: metadata.schema_version,
        scope_fingerprint: metadata.scope_fingerprint,
        canonical_watermarks: metadata.canonical_watermarks,
        policy_epoch: metadata.policy_epoch,
        committed_change_set_id: change_set.change_set_id,
        committed_at: metadata.committed_at,
        actor_ref: metadata.actor_ref,
        reason: metadata.reason,
        entry_count: staged.len(),
        budget_summary: actual_summary,
    };
    version.validate()?;

    idempotency.records.insert(
        idempotency_key,
        IdempotencyRecord {
            payload_hash: change_set.payload_hash,
            version: version.clone(),
            entries: staged.clone(),
        },
    );

    Ok(CommitOutcome::Committed {
        version,
        entries: staged,
    })
}

fn validate_unique_entries(entries: &[ContextEntryVersion]) -> Result<(), ContextError> {
    let mut ids = HashSet::new();
    for entry in entries {
        if !ids.insert(entry.entry_id.clone()) {
            return Err(ContextError::DuplicateEntryId);
        }
    }
    Ok(())
}
```

### K. `crates/memory-context/src/lib.rs` L118-132

ContextEntry 结构（edit 路径的载体）

```rust
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextEntry {
    pub entry_id: OpaqueId,
    pub memory_id: OpaqueId,
    pub memory_version_id: OpaqueId,
    pub tier: ContextTier,
    pub priority: i32,
    pub activation_reason: String,
    pub rendered_content: String,
    pub source_refs: Vec<OpaqueId>,
    pub evidence_refs: Vec<OpaqueId>,
    pub epistemic_qualifiers: Vec<String>,
    pub content_hash: String,
    pub rendered_bytes: usize,
}
```

### L. `crates/memory-context/src/lib.rs` L690-817

旧 ChangeSet / ChangeSetOperation / ChangeSet::validate —— validate_edit_entry 的真实调用点

```rust
/// A pure in-memory edit envelope. The source snapshot is never mutated.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ChangeSet {
    pub base_version: u64,
    pub operations: Vec<ChangeSetOperation>,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum ChangeSetOperation {
    Update {
        operation_id: String,
        entry_id: OpaqueId,
        updated: ContextEntry,
        reason: String,
    },
    Remove {
        operation_id: String,
        entry_id: OpaqueId,
        reason: String,
    },
    Replace {
        operation_id: String,
        old_entry_id: Option<OpaqueId>,
        replacement: ContextEntry,
        reason: String,
    },
    Reorder {
        operation_id: String,
        entry_ids: Vec<OpaqueId>,
        reason: String,
    },
    Expire {
        operation_id: String,
        entry_id: OpaqueId,
        expires_at_context_version: u64,
        reason: String,
    },
    Reconcile {
        operation_id: String,
        desired_entries: Vec<ContextEntry>,
        reason: String,
    },
}

impl ChangeSetOperation {
    fn operation_id(&self) -> &str {
        match self {
            Self::Update { operation_id, .. }
            | Self::Remove { operation_id, .. }
            | Self::Replace { operation_id, .. }
            | Self::Reorder { operation_id, .. }
            | Self::Expire { operation_id, .. }
            | Self::Reconcile { operation_id, .. } => operation_id,
        }
    }
}

impl ChangeSet {
    pub fn validate(&self) -> Result<(), ContextError> {
        if self.base_version == 0 || self.operations.is_empty() {
            return Err(ContextError::InvalidOperation);
        }
        let mut ids = HashSet::new();
        for operation in &self.operations {
            let id = operation.operation_id();
            if id.trim().is_empty() {
                return Err(ContextError::InvalidOperationId);
            }
            if !ids.insert(id) {
                return Err(ContextError::DuplicateOperationId);
            }
            match operation {
                ChangeSetOperation::Update {
                    updated, reason, ..
                }
                | ChangeSetOperation::Replace {
                    replacement: updated,
                    reason,
                    ..
                } => {
                    validate_edit_entry(updated)?;
                    if reason.trim().is_empty() {
                        return Err(ContextError::EmptyField("reason"));
                    }
                }
                ChangeSetOperation::Remove { reason, .. }
                | ChangeSetOperation::Expire { reason, .. }
                | ChangeSetOperation::Reconcile { reason, .. } => {
                    if reason.trim().is_empty() {
                        return Err(ContextError::EmptyField("reason"));
                    }
                }
                ChangeSetOperation::Reorder {
                    entry_ids, reason, ..
                } => {
                    if reason.trim().is_empty() {
                        return Err(ContextError::EmptyField("reason"));
                    }
                    if entry_ids.is_empty() {
                        return Err(ContextError::InvalidReorder);
                    }
                }
            }
            if let ChangeSetOperation::Expire {
                expires_at_context_version,
                ..
            } = operation
            {
                if *expires_at_context_version == 0 {
                    return Err(ContextError::InvalidVersion);
                }
            }
            if let ChangeSetOperation::Reconcile {
                desired_entries, ..
            } = operation
            {
                let mut desired_ids = HashSet::new();
                for entry in desired_entries {
                    validate_edit_entry(entry)?;
                    if !desired_ids.insert(entry.entry_id.clone()) {
                        return Err(ContextError::DuplicateEntry);
                    }
                }
            }
        }
        Ok(())
    }
}
```

### M. `crates/memory-context/src/lib.rs` L2983-3096

#[cfg(test)] mod tests 里的构造 helper：oid/actor/version_id/changeset_id/entry/head/rollback/metadata/prepared_change_set

```rust
    fn oid(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn actor() -> ActorRef {
        ActorRef {
            actor_id: oid("actor-1"),
        }
    }

    fn version_id(value: &str) -> ContextVersionId {
        ContextVersionId::new(value).unwrap()
    }

    fn changeset_id(value: &str) -> ChangeSetId {
        ChangeSetId::new(value).unwrap()
    }

    fn entry(value: &str, content: &str, revision: u64) -> ContextEntryVersion {
        ContextEntryVersion {
            entry_id: oid(value),
            memory_id: oid(&format!("memory-{value}")),
            memory_version_id: oid(&format!("memory-version-{value}")),
            revision,
            state: EntryState::Active,
            tier: ContextTier::P1,
            priority: 10,
            activation_reason: "test".into(),
            rendered_content: content.into(),
            source_refs: vec![oid("source")],
            evidence_refs: vec![],
            epistemic_qualifiers: vec![],
            content_hash: content_hash_for(content),
            rendered_bytes: content.len(),
            valid_time: Some(TimeValue::Unknown),
            temporal_ref: None,
        }
    }

    fn head() -> ContextHead {
        ContextHead {
            context_id: oid("ctx"),
            version: Some(version_id("v1")),
            sequence: 1,
        }
    }

    fn rollback(
        target_entries: &[ContextEntryVersion],
        current_entries: &[ContextEntryVersion],
    ) -> Result<ContextChangeSet, ContextError> {
        rollback_with_reason(target_entries, current_entries, "restore")
    }

    fn rollback_with_reason(
        target_entries: &[ContextEntryVersion],
        current_entries: &[ContextEntryVersion],
        reason: &str,
    ) -> Result<ContextChangeSet, ContextError> {
        plan_rollback(
            &head(),
            RollbackPlanRequest {
                target: version_id("v0"),
                target_entries: target_entries.to_vec(),
                current_entries: current_entries.to_vec(),
                reason: reason.to_owned(),
                actor: actor(),
                change_set_id: changeset_id("rollback-1"),
                created_at: "2026-01-01T00:00:00Z".into(),
                policy_epoch: 7,
            },
        )
    }

    fn metadata(entries: &[ContextEntryVersion]) -> VersionMetadata {
        VersionMetadata {
            context_version_id: version_id("v2"),
            schema_version: "1".into(),
            scope_fingerprint: "scope-fp".into(),
            canonical_watermarks: vec![],
            policy_epoch: 7,
            snapshot_ref: "snapshot://v2".into(),
            snapshot_hash: snapshot_hash(entries).unwrap(),
            budget_summary: ContextBudgetSummary {
                entry_count: entries.len(),
                rendered_bytes: entries.iter().map(|item| item.rendered_bytes).sum(),
            },
            committed_at: "2026-01-01T00:00:01Z".into(),
            actor_ref: actor(),
            reason: "commit".into(),
        }
    }

    fn prepared_change_set(operations: Vec<ContextOperation>) -> ContextChangeSet {
        let mut value = ContextChangeSet {
            change_set_id: changeset_id("cs-1"),
            context_id: oid("ctx"),
            base_version: Some(version_id("v1")),
            target_version: None,
            operations,
            reason: "test".into(),
            actor_ref: actor(),
            created_at: "2026-01-01T00:00:00Z".into(),
            idempotency_key: "key-1".into(),
            payload_hash: String::new(),
            policy_epoch: 7,
            status: ChangeSetStatus::Prepared,
            correlation_id: None,
            causation_id: None,
            result_ref: None,
        };
        value.payload_hash = value.compute_payload_hash().unwrap();
        value
    }
```

### N. `crates/memory-context/src/lib.rs` L3342-3382

现有 commit_change_set 调用样例（commit_rejects_stale_policy_epoch / commit_rejects_wrong_base_version）

```rust
    #[test]
    fn commit_rejects_stale_policy_epoch() {
        let change_set = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: entry("a", "a", 1),
        }]);
        let mut metadata = metadata(&[entry("a", "a", 1)]);
        metadata.policy_epoch = 6;
        assert!(matches!(
            commit_change_set(
                &head(),
                change_set,
                &[],
                &mut IdempotencyLog::default(),
                7,
                metadata
            ),
            Err(ContextError::PolicyEpochStale { .. })
        ));
    }

    #[test]
    fn commit_rejects_wrong_base_version() {
        let mut change_set = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: entry("a", "a", 1),
        }]);
        change_set.base_version = Some(version_id("stale"));
        change_set.payload_hash = change_set.compute_payload_hash().unwrap();
        assert_eq!(
            commit_change_set(
                &head(),
                change_set,
                &[],
                &mut IdempotencyLog::default(),
                7,
                metadata(&[entry("a", "a", 1)])
            ),
            Err(ContextError::BaseVersionMismatch)
        );
    }
```

### O. `crates/memory-context/Cargo.toml` L1-17

全文（无 sha2 依赖；dev-dependencies 见 13-17）

```toml
[package]
name = "memory-context"
version = "0.1.0"
edition = "2021"
license = "UNLICENSED"
publish = false

[dependencies]
memory-domain = { path = "../memory-domain" }
serde = { version = "1", features = ["derive"] }
serde_json = "1"

[dev-dependencies]
memory-event-store-sqlite = { path = "../memory-event-store-sqlite" }
memory-store = { path = "../memory-store" }
memory-storage = { path = "../memory-storage" }
memory-storage-sqlite = { path = "../memory-storage-sqlite" }
```

### P. `crates/memory-context/src/lib.rs` L1585-1600

build_context 对 content_hash 的原样透传（阻断项 1 的传导链）

```rust
            entry_id: candidate.entry_id,
            memory_id: candidate.memory_id,
            memory_version_id: candidate.memory_version_id,
            tier: candidate.tier,
            priority: candidate.priority,
            activation_reason: candidate.activation_reason,
            rendered_content: candidate.rendered_content,
            source_refs: candidate.source_refs,
            evidence_refs: candidate.evidence_refs,
            epistemic_qualifiers: candidate.epistemic_qualifiers,
            content_hash: candidate.content_hash,
            rendered_bytes: bytes,
        });
    }

    debug_assert_eq!(
```
