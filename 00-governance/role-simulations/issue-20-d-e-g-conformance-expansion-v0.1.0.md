# Issue #20 — D/E/G Owner-Obligation Conformance Expansion (Coordinator Reference)
# Issue #20 — D/E/G Owner 义务符合性测试扩展（协调者参考模型）

- Status / 状态: **PROPOSED / COORDINATOR REFERENCE ONLY**
- Authority / 权限: Session P role simulation; not D, E, or G Owner acceptance.
- Scope / 范围: executable semantic tests for D producer-work/fence behavior, E attempt/lease/replay lifecycle, and G fragment lineage/reconnect/delivery replay.
- Non-claims / 不代表: production implementation, Owner-local conformance, independent Owner signature, database serialization, distributed race safety, adapter interoperability, or architecture freeze.

## D — ProducerWork and ForgetFence

The reference model now exercises late-discovered derivative admission as a barrier-reopening event. A derivative must join an exact admitted parent, receive a new registration sequence, remain unresolved, and invalidate a prior release attempt through the changed high-water. Fence release requires all admitted work terminal and a refreshed generation/high-water CAS.

D 参考模型覆盖迟发现派生工作重新打开屏障：派生工作必须绑定已登记父项，获得新的登记序号并保持未决；旧 high-water 的释放 CAS 必须失败。只有全部工作终态化且使用最新 generation/high-water 才能释放 Fence。

## E — WorkItem, Attempt, Lease, DLQ and replay

D Producer Registration is a prerequisite to every E enqueue/lease/attempt and remains bound to the stable WorkItem across retries. The later publication-participant admission is a distinct join after hidden Storage prepare. Lease expiry is bound to the exact current lease/attempt. An expired attempt may enter DLQ and replay under the same stable WorkItem/request identity with a new attempt number. DLQ and lease expiry are not terminal no-publication evidence. Once private staging, Storage prepare, D admission, or UNKNOWN is reached, a new attempt is blocked until the exact publication is reconciled.

D Producer Registration 必须先于 E 入队、Lease 和 Attempt，并在重试中绑定稳定 WorkItem；发布阶段的 D PublicationParticipant Admission 则是 Storage 隐藏 Prepare 后的另一项独立 Join。Lease 过期绑定精确当前 lease/attempt。过期尝试可进入 DLQ，并以相同 WorkItem/request 身份重放、递增 attempt。DLQ/过期不构成 NO_PUBLICATION 终态证明。进入私有暂存、Storage Prepare、D Admission 或 UNKNOWN 后，必须先对原发布操作进行精确对账，不得创建新尝试。

## G — fragment lineage, ContextVersion and reconnect

Every fragment retains source references and D generation. Reconnect requires the exact current ContextVersion and current D authorization for every source reference. A stale snapshot, changed D generation, forgotten source, or old delivery/ACK cannot authorize replay.

每个 Fragment 保留来源引用及 D generation。重连必须验证精确当前 ContextVersion，并逐项确认所有来源引用仍获 D 授权。过期 Snapshot、D generation 变化、已遗忘来源或旧 Delivery/ACK 均不能授权重放。

## Test boundary / 测试边界

The tests are deterministic single-process reference-model tests. Passing proves only that this candidate model enforces the stated transitions. D/E/G Owners must independently adopt or amend the semantics and add equivalent tests against their own implementation/owner-local contracts before any Owner conformance claim.

测试为确定性单进程参考模型测试。通过仅证明候选模型执行了上述状态约束。D/E/G Owner 必须独立采纳或修订语义，并在各自实现/Owner 本地合同上补充等价测试，之后才能声称 Owner 符合性。
