# G Claim/Fact Context 可见性补充

> 规范关系：
> 本双语补充文件中的规范要求已经合并进入
> 根级规范文件
> `06-memory-context/context-versioning.md` §13.3。
>
> 本文件是中文同步配对文件，不构成独立竞争协议。
>
> 如果出现文本漂移，以根级 §13.3 为准，
> 并必须重新同步本文件。
>
> 谱系：Phase 3.8.27 G Claim/Fact Context
> Visibility Addendum；
> AID-2026-014 R5 FLIP_TO_B。

## 1. 精确 Revision 引用

引用 ClaimRevision、FactRevision 或派生资产的 ContextVersion MUST 绑定精确不可变 Revision 引用和适用 ForgetFenceCursor。

G MUST NOT 使用当前 Claim Head 替代固定的 ClaimRevisionRef。

## 2. 受保护提交

G MUST：

1. 重新验证当前 I 授权。
2. 重新验证适用 D Forget Fence。
3. 验证所有被引用的 Claim/Fact Revision。
4. 验证完整 Dependency Registration Receipt。
5. 适用时验证精确 Storage Visibility Outcome。
6. 通过受保护可见性协议提交不可变 ContextVersion。
7. 只有权威提交结果得到确认后才允许发布。

G 不得仅凭本地预检查，随后独立执行不受保护的 Head 更新来暴露新 ContextVersion。

## 3. 历史可见性

后续 Forget 不会因为 ContextVersion 曾经提交就赋予永久访问权。

历史 Context 读取和 Replay MUST 重新执行当前授权和 Forget 抑制检查。

不得通过既有 FactRevision 或历史 ContextVersion 披露已遗忘 ClaimRevision。

## 4. UNKNOWN 与恢复

UNKNOWN 提交或 Lost ACK MUST 保持非最终状态。

恢复 MUST 解析同一个操作及准确 ContextVersion 身份。

任何 Retry 都不得创建重复可见的 ContextVersion 状态。

B 版顺序以及 T17/T18 不变量，
对所有源自受保护规范 Claim/Fact 内容的
G ContextVersion 均具有强制效力。

G MUST NOT 绕过已准入参与者的 Forget Barrier。

根级 §13.3 的物理实现门禁继续有效。

## 5. Storage 边界

既有 Storage L1 决策保持不变。

Storage L4 继续保持 OPEN / NOT APPROVED。
