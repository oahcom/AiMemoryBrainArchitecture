# Executed prompt — VALIDATOR-IMPL (AID-2026-293)

Verbatim prompt delivered to the implementation sub-session. It is snapshotted
because the manifest pins the bytes this session actually received, not a
reconstruction of them.

---

你是实施子 Agent VALIDATOR-IMPL。环境：Windows，**Windows PowerShell 5.1**，命令用 `;` 分隔，不用 `&&`/`||`。**严禁 WSL**（不调 `wsl`/`wsl.exe`/`bash -lc`，不用 `/mnt/*` `/tmp` `/home/*`）。

仓库 `D:\code\AiMemoryBrainArchitecture`。主工作树被别人占用，**必须用独立 worktree**（`D:\code\_aimb\wt-validator`）。

## 规格来源（唯一权威，逐字使用，不得改写或"优化"）
- `D:\code\chatgpt-session-ops\scripts\replies\reply-6b07c97e-080615.md` 第 **3–335** 行 = registry 强制校验器规格（§1 全部：职责边界、全量扫描与唯一性、解析与重复分类、schema 一致性、prompt pin 与已提交字节、既有 `check_manifest_blob_pins.py` 处置、INDEX 防静默丢行、人工散文列数据结构、输出格式与退出码）
- `D:\code\chatgpt-session-ops\scripts\replies\reply-6b07c97e-182004.md` 第 **24–747** 行 = `work-item-registry.schema.json` 的完整 JSON 正文（```json 围栏内逐字取）

## 并行前提（重要）
另一个工作包 `SCHEMA-IMPL` 正在同一路径创建 `00-governance/schemas/work-item-registry.schema.json`。**你也要创建这个文件，字节必须与第 24–747 行完全一致**。两边内容相同时，add/add 合并不冲突，所以不要等待、不要依赖它的分支。

## 任务
1. `git fetch origin --prune --quiet`；记录 `origin/main` 完整 SHA。
2. `git worktree add -f D:\code\_aimb\wt-validator -B gov/2026-11-28-registry-validator origin/main`
3. 按 p71 第 24–747 行创建 `00-governance/schemas/work-item-registry.schema.json`（逐字）。
4. 按 p72 §1 实现校验器。落地位置遵循仓库既有约定（参考 `scripts/ci/` 与 `scripts/governance/` 的现有组织方式自行判断，并在报告里说明理由）。
5. **必须实现并测试**这些行为（每条都要有对应用例）：
   - 全量扫描 registry 目录，**从文件内容**读 `work_item_id`（不得用目录名代替）
   - 同一 ID 多路径 → `VIOLATION`
   - 解析失败 → fail-closed（按 §1.2「解析与重复的分类」的具体分类实现，不要自己发明）
   - schema 校验失败：枚举越界、`additionalProperties` 越界、缺失状态带 `value`、`KNOWN` 无 `value`、`work_item_id` 格式非法 —— 各一条用例
   - `prompt_sha256` / `prompt_bytes` 与**已提交字节**的比对（按 §1.4）
   - §1.5 的 INDEX 防静默丢行机制（按规格实现，不要只说"用生成器"）
   - §1.7 的 JSON 输出格式与退出码语义
6. 跑全部测试，贴**真实输出**；必须 `ALL PASS`。不得声明未跑过的结果。
7. 按 §1.4 对既有 `check_manifest_blob_pins.py` 的处置裁决执行（取代 / 保留 / 删除），并在报告里逐字引用该裁决。
8. push（不 force）并开 PR：
   - 标题：`feat(gov): add canonical work-item registry validator (AID-2026-293)`
   - body 含 `AI-assisted work: YES`、`Work Item ID: AID-2026-293`、`Related issues:`（如需补三列映射表 `| #<n> | LEGACY_UNDECLARED | N/A |`）、`Session evidence reference(s)` 指向 head 树真实文件
   - **开 PR 前扫描 `14-ai-development/work-items/` 与 `INDEX.md` 确认号未占用**；已占用则取扫描后第一个空闲号并如实记录
9. 轮询 check-runs（60s × 30），逐个记录 16 个 declared context；红则修。
10. 交付 `D:\code\_aimb\round\VALIDATOR-IMPL.md`：`origin/main` SHA、规格行号范围、落地文件清单、每条用例的输入与期望/实际、测试输出原文、对 `check_manifest_blob_pins.py` 的处置、PR 号与 head、16 项 check 结论、未达标项。

**本轮不迁移任何 registry 数据文件**（那是阶段 C）。不改现有 135 个 manifest，不动 `INDEX.md` 内容。

硬约束：不 force、不 rebase、不合并、不改其他 PR、不动主工作树。
