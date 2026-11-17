# Phase 3.8.2 — C Exact Review: RecoveryJoin and Provider Side-Effect Boundary
# C 精确审查：RecoveryJoin 与 Provider 副作用边界

- Reviewer perspective: C — Agent Integration Architect
- Review mode: delegated C-role simulation at the user's direction; not an independent human Owner signature.
- Decision: **ACCEPT WITH C-OWNED PROVIDER-SIDE-EFFECT AMENDMENTS**
- Status: **CONTRACT COMPOSITION ACCEPTED; RUNTIME / PROVIDER CONFORMANCE NOT VERIFIED**
- Language: English and Chinese are normative peers.

## 1. Exact source bundle / 精确审查源

| Artifact | Branch | Blob |
|---|---|---|
| C Provider Egress Gate adapter contract | `session-c-agent-integration-2026-11-16` | `baf921875e849f3a40aebea9ea089b6425cf213d` |
| C final-request evidence contract | `session-c-agent-integration-2026-11-16` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` |
| C exact Provider Outcome review | `session-c-agent-integration-2026-11-16` | `19519a9dabe8aea66897c01493ab5b65ed8af4aa` |
| C JF-10 PreparedParticipantGID boundary acceptance | `session-c-agent-integration-2026-11-16` | `dd6c28a88aad019fcb513e789dcfffc20934e852` |
| H RecoveryJoin schema 1.0.0 | `session-h-bmcp-protocol` | `dd3234aa1c74caf6d0e335875cd96e0b2b64082f` |
| H semantic validator contract | `session-h-bmcp-protocol` | `b3218298f58cff9b92cb1c38e453af6fd4d0dd50` |
| HRC/JPF suite | `session-h-bmcp-protocol` | `60a2f4db4bd12f2131ecd147db9bbe328da6db50` |
| H wire suite | `session-h-bmcp-protocol` | `1a4e754ba9bfa57eb973c6d39731e9f89443b323` |
| H schema integrity suite | `session-h-bmcp-protocol` | `67aba74c120f2916d768e7b01c45408ee2624f3a` |
| H CI candidate result | GitHub Actions | [44039990464 — 66/66 PASS](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44039990464) |
| Storage bidirectional COC/Owner Admission JoinProof | `session-storage-consistency-forget-atomicity-2026-11-16` | `4520860b28429d35cdb2ca947a56d0ccb64226a3` |
| Storage D/Storage topology ADR | `session-storage-consistency-forget-atomicity-2026-11-16` | `080433f8e13a500522bc2754da64057edb0ae9d8` |
| I RecoveryJoin trust/currentness exact review | `session-i-security-governance-2026-11-16` | `4a72cecd7769be7017b699ab102b127fab516101` |

## 2. C disposition / C 审查结论

C accepts the logical composition of RecoveryJoin only as a durable evidence join. It is not a provider authorization token, provider outcome, inference completion receipt, user-delivery receipt, or permission to reopen a provider gate.

C keeps these nominal identities separate:
- C ParticipantIntentRef / C owner admission row;
- Storage PreparedParticipantRef / PreparedTransactionGID / engine-native XID;
- C ProviderIdempotencyKey;
- C ProviderAttemptRef / CSubmitOutcome;
- I CommitAuthorizationReceipt / ITerminalProof;
- D PublicationParticipantRef / ForgetFence / lineage barrier.

Storage GID MUST NOT be converted into or reused as a provider idempotency key. A retry of the same provider side effect MUST retain the exact same C ProviderIdempotencyKey and request digest.

C 仅接受 RecoveryJoin 作为持久化证据关联，不将其视为 Provider 授权、Provider Outcome、推理完成、用户送达或重新打开 Provider Gate 的许可。

## 3. Required C-side invariants / C 侧强制不变量

1. **Gate and egress share one serialization authority.** The concrete transport adapter that owns the provider send must own the final gate check. No ungated SDK/client handle may escape.
2. **Close-first means zero bytes.** If gate close wins the same authoritative serialization boundary, no provider request bytes may be handed to transport.
3. **Send-first is a captured in-flight participant.** If final send commitment wins first, its exact attempt, request digest, provider idempotency key and participant identity must be durably represented and reconciled.
4. **Ambiguous outcome remains IN_DOUBT.** Timeout, process death, connection reset, lost ACK or uncertain transport handoff cannot be interpreted as no-send or provider success.
5. **Same-key recovery only.** Resolve ambiguity using provider-authoritative lookup on the same ProviderIdempotencyKey. If the provider has no authoritative lookup, keep the attempt IN_DOUBT and keep dependent gates held.
6. **Every physical send re-enters the gate.** SDK retries, redirects, endpoint/region/account/model failover, streaming continuation and reconnect must each revalidate current I/D/COC state and pass the final adapter gate.
7. **C alone owns provider truth.** H schema validity, Storage COMMITTED, I COMMIT_WON, D clearance, COC membership or transport ACK cannot synthesize CSubmitOutcome.
8. **Applied is request-bound.** Full Applied requires the final immutable inference-submit hook and evidence bound to the exact final request after all context/prompt transformations. A pre-transform request hash is insufficient.

## 4. Exact HRC CI interpretation / HRC CI 解释边界

H reports 66/66 candidate tests passing in run 44039990464. C recognizes this as a useful protocol/reference-model gate for typed request/admission/participant joins, wire negative cases and schema shape.

It does NOT test:
- a real C provider adapter or provider API;
- CloseEgressGate versus final transport handoff under concurrency;
- provider idempotency lookup or durable CSubmitOutcome recovery;
- retries, redirects, stream continuation or failover against a real SDK;
- an Agent framework's final immutable submit hook;
- C/G/H end-to-end Full Applied;
- production canonical bytes, signatures or independent language implementations.

## 5. Blocking amendments / 阻断修订

| ID | Required evidence | Status |
|---|---|---|
| C-RJ-01 | C request/admission ledger enumeration and exact bidirectional row joins against the same COC prefix | OPEN |
| C-RJ-02 | Durable C gate generation/currentness CAS after JoinProof creation | OPEN |
| C-RJ-03 | Real adapter close-vs-send race with zero-byte and captured-in-flight assertions | OPEN |
| C-RJ-04 | Provider-specific same-key lookup and durable ambiguous-outcome recovery | OPEN |
| C-RJ-05 | Exact CSubmitOutcome typed schema and H/C joint approval | OPEN |
| C-RJ-06 | Final immutable Agent submit hook with request-bound digest/proof | OPEN |
| C-RJ-07 | Restore/reconnect/retry/redirect/stream/failover conformance | OPEN |
| C-RJ-08 | Exact integrated C/H/I/D/Storage acceptance and real COC runtime | OPEN |

## 6. C final decision / C 最终裁决

**ACCEPT WITH C-OWNED PROVIDER-SIDE-EFFECT AMENDMENTS** for the logical RecoveryJoin composition and identity boundaries.

**NOT ACCEPTED:** provider egress implementation, Full Applied, runtime recovery, production provider behavior, or TAB-001 freeze.

C 以列明修订为条件接受 RecoveryJoin 的逻辑组合及身份边界；不接受 Provider Egress 实现、Full Applied、运行时恢复、生产 Provider 行为或 TAB-001 冻结。

All statements above are delegated role-review findings and are not an independent human C Owner signature.
