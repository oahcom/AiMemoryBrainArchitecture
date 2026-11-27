# Executed prompt snapshot — AID-2026-268

This is a recorded excerpt of the actual user instruction received in the S6-B implementation session. It is not a byte-for-byte export of the complete chat message; provenance is therefore recorded as NOT_VERIFIED.

> 你是实现会话 **S6-B**。唯一任务：把 Issue **#1350** 落成 **blob-pin 完整性校验**（manifest 声明的每个 blob 身份都必须能在声明的 commit 上解析到真实字节）。

> 仓库 `oahcom/AiMemoryBrainArchitecture`，默认分支 `main`。只能走 GitHub API：读树、读 blob、建分支、写文件、开 PR、合并。没执行过的东西不许说执行过。

> 声明了路径 + 摘要：解析路径、由已提交字节重算摘要、比对；不等即拒绝，并同时给出声明值与实测值。声明了摘要但路径在候选树不存在：拒绝，指明缺失路径。合法 pin：接受，零噪声。跨 commit pin：在声明的那个 commit 上解析；该 commit 取不到 → INCOMPLETE，不是 PASS。`prompt_sha256` / `prompt_bytes` 对已提交字节重算 sha256 与字节数；两者都要对。

> 退出码 `0` PASS / `1` VIOLATION / `2` INCOMPLETE，与仓内既有 gate 一致；读不到条件绝不返回 0。

> 接线位置：`.github/workflows/repository-hygiene.yml` 的 `Repository hygiene (hard gate)` job，紧跟在既有 `Check every work-item manifest parses` step 之后。新增 job 会产出不在保护列表里的 context，等于没有门禁。

> 验收包括字段枚举、候选树路径解析、已提交字节重算、摘要不符和路径缺失拒绝、合法 pin 零误报、改字节和删路径负例、main 全量扫描、`#1220` head `9a2063ae` 负例扫描，以及 traceability、hygiene、bilingual 回归。
