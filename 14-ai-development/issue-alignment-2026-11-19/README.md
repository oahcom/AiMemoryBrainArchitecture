# Issue Responsibility Alignment — Evidence Index (2026-11-19)

Issue 责任人对齐证据索引（2026-11-19）

## Scope / 范围

Owner A (`A-OWNER-ALIGNMENT-001`, conv `6afedebe-9950-83ee-93d4-7fd19cf46089`)
dispatched six L2 domain-alignment sessions covering 26 open issues. All six
sessions were read-only alignment reviews: no Git/PR/Issue/assignee writes,
Decision_ID = NOT_CREATED throughout (alignment does not sign on behalf of
Owners).

A（`A-OWNER-ALIGNMENT-001`）派工六场 L2 领域对齐会话覆盖 26 个 open issues。
六场全部只读对齐：零 Git/PR/Issue/assignee 写入，Decision_ID 全程 NOT_CREATED
（对齐不代签）。

## Files / 文件

| File | Issues | Conv ID | SHA-256 |
|---|---|---|---|
| l2-01-receipt.md | #2/#10/#14/#20/#25 | `6afeebc5-d664-83e8-9ea5-266d9b3c18a9` | `db6f1a7b75fd462749748398532603aa2c31037049e6dc0e20733343d24dba19` |
| l2-02-receipt.md | #3/#29 | `6afeee89-3068-83e8-83ff-cfd51c976174` | `191d9d38824609d0ccca23e5d2536217bceccf8418b6d2274302525b0b9621c9` |
| l2-03-receipt.md | #4/#5 | `6afeee91-dba8-83ee-9cde-337b7e32c174` | `bccf8edb5a7ec3e69a322e78bfae8edb176a5ac6eff731815cbc65dca205cbe4` |
| l2-04-receipt.md | #21 | `6afeeecb-be28-83ee-a5c4-e904fd0a143a` | `b23f0c947ca109d1977d1ec1104f73ff56c29adc52929e887b7e850fa8ae2c1c` |
| l2-05-receipt.md | #11/#24/#30/#41/#43/#254/#262-266/#130 | `6afeef2f-5d34-83ee-88f6-5993f71ea46d` | `f9e8c17a58e36c56081d3306677cdbd142b23f8b56938fba59b24aaa167cdfcf` |
| l2-06-receipt.md | #7/#26/#37/#134 | `6afeeef5-0968-83e8-a1c9-35a6bc5c78dc` | `18e9d8f865c08516b65b8f3ff7240245b968cadab90137ab5c547588e101cc2b` |
| a-d3-baseline-candidate.md | baseline increment (AI-PROC-001 §2.1) | authored by A in-session | `09a2359162bd2c85a51c30f92c5f2bfe5d1ad929c98f3a75bd8be101610ef35e` |

## Harvest provenance / 收割来源

All receipts were harvested via raw mapping
(`GET /backend-api/conversation/<id>` over all assistant parts), not the
single-message GET supplement: every conversation produced 2 assistant
messages with tail overlap, and single-GET capture would have truncated each
report at its last message (U-053). Each `*-receipt.md` is the first complete
message, deduplicated at the overlap boundary.

六场全部经 raw mapping 全 parts 收割（U-053：单条 GET 只收末条消息，六场皆为
双消息尾部重叠模式）；`*-receipt.md` 为去重后的首条完整消息。

## Pending / 待并入

- l2-05 batch2 supplement (#43 full-body review, conv `6afeef2f`) — in flight
  at index-writing time; its receipt is to be appended as
  `l2-05b-receipt.md` when harvested.
- L2 verdicts: L2-01 NO-GO (joint contract frozen) / L2-02 HOLD x2 /
  L2-03 HOLD / L2-04 HOLD (not freeze-ready) / L2-05 NOT READY /
  L2-06 PARTIAL (#134 is the single P0). No session claimed completion.
