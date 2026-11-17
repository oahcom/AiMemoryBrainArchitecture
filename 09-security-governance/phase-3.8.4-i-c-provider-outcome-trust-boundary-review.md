# Phase 3.8.4 — I Exact Review of C Provider Outcome Trust Boundary
# Phase 3.8.4 — I 对 C Provider Outcome 信任边界的精确审查

- Reviewer: I — Security, Identity and Governance
- Branch: `session-i-security-governance-2026-11-16`
- Exact C source reviewed: `07-agent-integration/phase-3.8.4-c-normative-provider-submit-outcome-contract.md`
- C source Blob: `819705037da89834e10b6dd2ec6e66c1b8c70886`
- Exact H schema: unified COC/JF-10/Provider Outcome 1.2.8, Blob `70b892797d07489936300a26c0dedfafe1d6e746`
- I crypto profile candidate: `AIMBA-I-CRYPTO-1.0`, Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS — AUTHORITY / TRUST BOUNDARY ONLY**
- Review provenance: delegated I-role simulation; not an independent human I Owner signature.
- English and Chinese are normative peers.

## 1. I decision / I 决议

I accepts C's semantic ownership of Provider Outcome and the five-value outcome algebra. I confirms that I authorization/revocation proof is an independent prerequisite for provider side effects; C cannot infer authorization from provider status, and I cannot infer provider outcome from COMMIT_WON.

I owns authenticated Principal/Issuer/Workload trust, issuer/key status and historical trust validation. C owns the CSubmitOutcome content, provider evidence truth, provider-specific idempotency semantics and C-owned signature projection/profile. H owns wire envelope and semantic/wire validation. The authorities are conjunctive but not interchangeable.

I 接受 C 对 Provider Outcome 的语义所有权及五值结果代数。I 确认 Provider 副作用前必须满足独立的 I 授权/撤销证明；C 不能从 Provider 状态推断授权，I 也不能从 COMMIT_WON 推断 Provider Outcome。

I 拥有认证 Principal/Issuer/Workload Trust、Issuer/Key Status 与历史信任验证。C 拥有 CSubmitOutcome 内容、Provider 证据真实性、Provider 专属幂等语义及 C 自有签名投影/配置。H 拥有 Wire Envelope 与语义/Wire 验证。各权威必须同时满足，但不能互相替代。

## 2. Binding trust requirements / 约束信任要求

1. C's protected signed outcome MUST carry an exact C-approved `signature_profile_id`, canonicalization profile, digest algorithm and immutable key ID/version. The common envelope's optional structural field is not a semantic waiver.
2. I resolves authenticated issuer identity and key-status evidence (ACTIVE/RETIRED/REVOKED/COMPROMISED/UNKNOWN) under the authoritative I trust registry and historical checkpoints. H/C must not trust payload-supplied key status or cache a stale ACTIVE result.
3. C defines the C-specific P0 allowlist and immutable outcome projection. I does not sign, rewrite or synthesize C's provider evidence.
4. C's profile MUST NOT silently inherit `AIMBA-I-CRYPTO-1.0`. A common cryptographic construction may be reused only through an explicit C profile decision and exact I/H/C/Storage acceptance, while I retains issuer/key trust authority.
5. A valid C signature proves only that the trusted C authority signed the stated outcome; it does not prove the provider receipt itself is truthful unless the evidence profile binds the authoritative provider response/lookup source and its verification semantics.
6. If I key status, historical checkpoint, anti-rollback anchor or issuer binding is missing/stale/unavailable, the dependent protected gate remains UNKNOWN/closed.

## 3. Authorization-to-provider ordering / 授权与 Provider 顺序

- Provider side effect is forbidden until the exact I owner-final-gate operation is terminalized as COMMIT_WON and the required D participant/fence/lineage predicates and C causal-order reservation are valid for the same immutable tuple.
- REVOCATION_WON forbids provider invocation and requires the applicable same-XID/participant abort or no-publication reconciliation.
- UNKNOWN/IN_DOUBT keeps the participant and affected revocation/fence gates held; C must not retry under a new provider key or new transaction.
- COMMIT_WON is not provider success and does not permit G Full Applied without C's actual HANDOFF_ACCEPTED evidence.

## 4. Exact semantic amendments / 精确语义修订

- `HANDOFF_REJECTED` is terminal only when authoritative provider evidence proves rejection with no accepted side effect. If provider may have accepted or executed the request, classify as `IN_DOUBT`.
- `NOT_INVOKED` requires positive evidence from C's serialized egress boundary; absence of provider receipt or timeout is not enough.
- `UNKNOWN` and `IN_DOUBT` are nonterminal, non-expiring, and must preserve the same immutable request/attempt/provider-key identity.
- C's owner signature reference must be assigned before signing, immutable and not derived from signature bytes; exact P0 projection must include every immutable C-authored semantic field and exclude only explicitly declared external proof locators/coordinator additions.
- C's provider evidence source and lookup consistency model must be provider-specific. No universal exactly-once or authoritative absence guarantee is implied.

## 5. L3 reference obligations / L3 参考义务

I requires reference-model coverage of:
- I COMMIT_WON vs REVOCATION_WON vs UNKNOWN interleaved with C gate-close/send;
- key status retired/revoked/compromised and historical verification;
- wrong owner/audience/purpose/PolicyDomain/message type;
- C signature profile downgrade/missing/unknown and key-version substitution;
- C HANDOFF_REJECTED vs IN_DOUBT distinction under ambiguous side effect;
- provider lookup unavailable or stale;
- COC quorum valid but I proof invalid, and I proof valid but C provider evidence invalid;
- restore with stale key-status generation or missing anti-rollback checkpoint.

## 6. Final I disposition / I 最终结论

**ACCEPT WITH ENUMERATED AMENDMENTS — AUTHORITY / TRUST BOUNDARY ONLY.**

I accepts C Blob `819705037da89834e10b6dd2ec6e66c1b8c70886` as the C-owned normative Provider Outcome semantic source candidate. I does not approve a C cryptographic profile, C trust root, key custody, provider adapter, provider truth, production key lifecycle or deployment. I's profile remains I-only and candidate until its own exact P0, trust and approval obligations are closed.

**有条件接受 — 仅权威/信任边界。** I 接受 C 合同作为 C 自有 Provider Outcome 语义源候选，但不批准 C 密码学配置、Trust Root、Key Custody、Provider Adapter、Provider 事实、生产 Key Lifecycle 或部署。I Profile 仍仅适用于 I 自身，且其 P0/Trust/批准义务仍待闭环。
