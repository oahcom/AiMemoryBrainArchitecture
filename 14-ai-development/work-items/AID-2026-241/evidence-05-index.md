# AID-2026-241 — 05-memory-runtime 入口角色调和证据

## 文件角色对照

| 文件 | H1 | 章节数 | designated_root | canonical_status |
|---|---|---|---|---|
| `05-memory-runtime/README.md` | Memory Runtime — Directory Index | TODO_SECTION_COUNT_ROOT | 否 | AUTHORED_INDEX |
| `05-memory-runtime/runtime-overview.md` | Runtime Overview | TODO_SECTION_COUNT_OVERVIEW | 是（唯一规范根） | Canonical |

## 裁决依据

本次采用“索引 + 唯一规范根”结构。

`05-memory-runtime/README.md` 的职责是提供目录导航、文档入口及相关链接，属于 `AUTHORED_INDEX`，不承担 Runtime 设计规范根的角色。

`05-memory-runtime/runtime-overview.md` 承载 Runtime 的实际设计说明，并依据 AID-2026-113 保留 `designated_root`。该文件继续作为唯一规范根。

README 顶部新增明确的索引声明，指出规范根的位置及 AID-2026-113 的裁决依据，避免读者将导航入口误认为规范根。

本次仅增加索引导读，不改变任何文件的规范角色，不撤销 AID-2026-113，不删除任何一方的正文，也不修改 `03-memory-brain` 的任何文件。

## 正文完整性

- `05-memory-runtime/README.md`：原有正文全部保留。
- `05-memory-runtime/runtime-overview.md`：未修改，正文全部保留。
- `docs/en/05-memory-runtime/README.md`：原有正文全部保留。
- `docs/zh-CN/05-memory-runtime/README.md`：原有正文全部保留。

章节数须由执行方在目标提交树上实测后填写，不得以估算值替代。
