1. **`prompt_file` + `prompt_sha256`：不纳入 AID-2026-255 范围。** 该不变量归属既有问题 **#1318**（PR #1281 导致的 33 份 manifest digest 失配）及 **#1278**（从未存在的 digest）。不得将其计入本任务的检查结果或基线。

2. **只有路径键、没有同级 digest 键：不是失败。** 路径本身不构成 blob pin 声明；不得因 `scope.changes[].path` 等路径字段缺少 digest 而报错。仅检查下列闭合清单中的完整字段身份，不对其他字段推断配对关系。

3. **AID-2026-255 唯一 in-scope key set（12 项）：**
   - `AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[0].root_blob`
   - `AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[0].en_mirror_blob`
   - `AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[0].zh_cn_mirror_blob`
   - `AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[1].root_blob`
   - `AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[1].en_mirror_blob`
   - `AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[1].zh_cn_mirror_blob`
   - `AID-2026-100/manifest.yaml#related_evidence[0].blob`
   - `AID-2026-100/manifest.yaml#related_evidence[0].en_mirror_blob`
   - `AID-2026-100/manifest.yaml#related_evidence[0].zh_cn_mirror_blob`
   - `AID-2026-150/manifest.yaml#source.files[0].blob`
   - `AID-2026-150/manifest.yaml#source.files[1].blob`
   - `AID-2026-150/manifest.yaml#source.files[2].blob`

   **闭合规则：** 仅以上 12 个字段身份属于本检查器的适用范围；其他路径键、digest 键、prompt 哈希及 pathless digest 一律忽略，不得生成失败项，也不得加入基线。清单内字段仍须按其声明路径验证 Git blob ID。

4. **版本裁定：使用 `prompt-v2`。** `prompt-v1.md` 已执行并提交，保持原样，不得编辑或替换。将本裁定作为 `prompt-v2.md` 提交，并与 v1 并存。

5. **给实现会话的 delta instruction：** 将检查器的适用范围收窄为上述精确 12 个字段身份，删除对 `prompt_file`/`prompt_sha256`、通用 `path`/`blob` 推断配对、其他 manifest 字段及 pathless digest 的失败判定；基线只保留这 12 个身份，不能通过扩大基线来掩盖范围错误。更新测试，覆盖范围外字段被忽略、12 个授权字段逐一验证，以及新增范围外失配不改变结果。对当前 `main` 运行时，直接检查器必须恰好输出 **12 项**并以 **exit 1** 结束；exact-set ratchet 必须接受这 12 项并以 **exit 0** 结束。若计数不是 12，或 ratchet 非 0，任务不得标记通过。
