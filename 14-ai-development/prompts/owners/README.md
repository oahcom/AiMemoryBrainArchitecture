# Owner Prompt Directory / Owner 提示词目录

Each Owner has a separate ChatGPT conversation prompt. The prompt defines only that Owner's authority; all prompts inherit the [global ChatGPT session contract](../global/chatgpt-session-contract-v1.md).

每个 Owner 都有独立的 ChatGPT 对话提示词。Owner 提示词只定义该 Owner 的权限范围；所有提示词均继承[全局 ChatGPT 会话契约](../global/chatgpt-session-contract-v1.md)。

| Owner | Prompt |
|---|---|
| A — Principal Integration Architect | [owner-session-v1.md](A/owner-session-v1.md) |
| B — Domain Model Architect | [owner-session-v2.md](B/owner-session-v2.md) — domain identity is distinct from security identity |
| C — Agent Integration Architect | [owner-session-v1.md](C/owner-session-v1.md) |
| D — Memory Brain Architect | [owner-session-v2.md](D/owner-session-v2.md) — bilateral D/I Forget contract agreement required |
| E — Memory Compiler Architect | [owner-session-v1.md](E/owner-session-v1.md) |
| F — Memory Runtime Architect | [owner-session-v1.md](F/owner-session-v1.md) |
| G — Memory Context Architect | [owner-session-v1.md](G/owner-session-v1.md) |
| H — BMCP Protocol Architect | [owner-session-v1.md](H/owner-session-v1.md) |
| I — Security & Governance Architect | [owner-session-v2.md](I/owner-session-v2.md) — security/Forget governance boundary clarified |

Prompts are PROPOSED until reviewed and accepted. Executed versions must never be overwritten; create v2 for material changes.

提示词在审查和批准前均为 PROPOSED。已经执行的版本不得覆盖；重大变更必须创建 v2。


## Historical prompt versions / 历史提示词版本

- **Owner B v1 — SUPERSEDED / HISTORICAL.** Retained unchanged for audit and historical replay only. It is not a current execution entry point. All new Owner B work MUST use [owner-session-v2.md](B/owner-session-v2.md).
- **Owner B v1 — 已被取代 / 历史版本。** 原文件保持不变，仅用于审计和历史回放，不得作为当前执行入口。所有新的 Owner B 工作必须使用 [owner-session-v2.md](B/owner-session-v2.md)。
