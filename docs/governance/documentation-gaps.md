# Documentation gaps / 文档缺口登记

Referenced-but-missing normative documents. Each entry records a link that could not be resolved during the GOV-DOC-002 rollout.

指向但缺失的规范文档。每条记录在 GOV-DOC-002 推行过程中无法解析的链接。

| ID | Missing document | Referenced from | Disposition |
|---|---|---|---|
| GAP-01 | `phase-3.5-forget-suppression-and-cursor-consumption.md` (Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract) | `docs/en/05-memory-runtime/{retrieval-engine, runtime-overview, working-set-and-cache}.md`, `docs/zh-CN/05-memory-runtime/{retrieval-engine, runtime-overview, working-set-and-cache}.md` | OPEN — never committed to this repository. Referencing text preserved; links replaced with an explicit missing-document marker. Content must NOT be reconstructed by an agent. |

## GAP-01 detail / 详情

Six references across the `05-memory-runtime` specifications cite this contract as the authoritative source for the F consumer matrix, retrieval-stage suppression matrix, cache/Working Set invalidation, index rebuild, and ten conformance specifications.

`05-memory-runtime` 各规范中共有六处引用将该契约视为 F Consumer Matrix、Retrieval-stage Suppression Matrix、Cache/Working Set Invalidation、Index Rebuild 及十项 Conformance Specification 的权威来源。

The file does not exist in the working tree or in the git history reachable from `main`. Because the referenced normative content is unavailable, the references are **not** satisfiable by rewriting them to a different file, and the content MUST NOT be invented.

该文件在工作树与 `main` 可达历史中均不存在。由于被引用的规范内容不可得，**不能**通过改指其他文件来满足这些引用，其内容也禁止臆造。

Required resolution / 需要的处置：

1. The owning party for `05-memory-runtime` supplies the actual contract, or
2. the six referencing passages are amended to state that the contract is not yet published.

1. 由 `05-memory-runtime` 责任方提供该契约原文；或
2. 将六处引用改写为「该契约尚未发布」。

Until then, any consumer reading `05-memory-runtime` MUST treat the forget-suppression and typed-cursor semantics as **not specified in a published normative document**.

在此之前，任何阅读 `05-memory-runtime` 的消费者 MUST 将 forget-suppression 与 typed-cursor 语义视为**尚无已发布的规范文档定义**。
