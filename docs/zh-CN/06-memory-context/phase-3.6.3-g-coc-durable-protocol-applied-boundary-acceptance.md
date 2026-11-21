# G Owner — 精确 COC Durable Protocol Applied-Evidence Boundary 验收

- 精确 Storage protocol Blob：`4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- A COC architecture Blob：`a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- G JF-10 Applied evidence acceptance Blob：`25c1da1f6769165881d217bb0bb492a997e0e14c`
- G Applied/Forget contract Blob：`aa3afa73d8a76cc6f025839c52bfbff6a983046a`
- 决策：**ACCEPT WITH G-OWNED APPLIED / CURRENT-USE CONDITIONS**
- 模式：按照用户指示进行的委派式 G 边界评审；不是独立的人类签署。

G 接受 COC protocol 作为一项必需证据来源，而不是 Applied 权限主体：

1. Full Applied 要求精确的 CSubmitOutcome、有效的 H evidence、I terminal authorization、D complete-lineage barrier/clearance、Storage same-XID resolution，以及绑定到同一不可变 tuple 的确定性 CausalOrderTerminalProof。
2. COC log commit、recovery batch、quorum position、I COMMIT_WON、D clearance、Storage prepared receipt、H ACK 或 reservation 单独存在时，绝不满足 Full Applied。
3. 缺失/过期的 COC prefix、未解决的 recovery batch、缺失 participant、owner high-water mismatch、未知的 I/D/Storage outcome 或 provider UNKNOWN，会阻止新的 Full Applied 和受保护的 current use。
4. 历史 Applied 只有在其原始提交时有效才保持不可变；current-use 必须针对当前 Context head、authorization、fence、scope、environment、session 和 capability 单独重新计算。
5. COC 不能签发 Owner 决策，也不能比较 COC/I/D/Storage positions。

例外：G Applied validator/persistence 和集成的 COC/JF-10 lookup 尚未实现/验证；G-CO race suites 仍为 NOT RUN。这只是设计验收，不代表 Global Forget completion 或 physical erasure。
