# AID-2026-003 T2 dispatch anchors

Source note: the four conversation identifiers and delivery windows below were supplied by the coordinating layer in the 2026-11-18 remediation handoff. The executing ChatGPT session interface does not expose the underlying conversation/message API mapping or independently retrieve those conversations. These identifiers are coordinator-supplied anchors, not independently observed metadata. No message IDs, epoch create_time values, or hashes are inferred or fabricated.

Stable account-scoped conversation permalink format:
https://chatgpt.com/c/<conversation_id>

| Session | conversation_id | Dispatch prompt | Role | Delivery window (+08:00) | Stable permalink |
|---|---|---|---|---|---|
| Independent review | 6afd8d4d-295c-83ee-80f3-dbf879b134a1 | 独立审查会话提示词-PR256.md (3988 字) | T2 dispatch | 19:34–19:45 | https://chatgpt.com/c/6afd8d4d-295c-83ee-80f3-dbf879b134a1 |
| Owner acceptance | 6afd9026-3e0c-83ec-8a4f-36b87e68437d | Owner会话提示词-PR256.md (8533 字) | T2 dispatch | 19:46–19:53 | https://chatgpt.com/c/6afd9026-3e0c-83ec-8a4f-36b87e68437d |
| Remediation round 1 | 6afd9f7f-d544-83ee-98d1-92d7aafb3bcf | 修复会话提示词-PR256.md (9807 字) | T2 dispatch; full snapshot target | 20:52–21:03 | https://chatgpt.com/c/6afd9f7f-d544-83ee-98d1-92d7aafb3bcf |
| Exact-Head re-verification | 6afdaea6-e428-83ec-96b6-0ca8fb5c0291 | Owner复验会话提示词-PR256.md (9682 字) | T2 dispatch | 21:56–22:21 | https://chatgpt.com/c/6afdaea6-e428-83ec-96b6-0ca8fb5c0291 |

## Snapshot availability and limits

- The remediation round-1 prompt text is supplied as the “修复一轮派工提示词全文” appendix in the coordinator's handoff message. The requested verbatim full snapshot is tracked at `t2-snapshot-fix-prompt.md`.
- The other three prompt snapshots are not included in the handoff message. Only their filenames, reported character counts, conversation IDs and delivery windows are available; their full text is not reconstructed.
- The coordinator states that the account/API mapping interface is not exposed to the executing session. Consequently no message_id, epoch create_time, or message-level export is claimed beyond the dispatch role/window metadata supplied above.
- Conversation links are account-scoped and may require the same authenticated account. A link is not proof that the target content has been independently fetched.
