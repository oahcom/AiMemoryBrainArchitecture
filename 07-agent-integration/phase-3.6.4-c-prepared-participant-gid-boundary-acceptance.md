# C Owner — Exact JF-10 Prepared Participant Identity / GID Boundary Acceptance

- Storage protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A integration mapping Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- B typed-reference registry Blob: `b5a169a1f2c2e6db4b7c8f96b127af971ff53f1f`
- H BMCP schema 1.1.1 candidate Blob: `c0bbfc7611a8d88a39cee209831db32b62601fde`
- Decision: **ACCEPT WITH C-OWNED PROVIDER-SIDE-EFFECT CONDITIONS**
- Mode: delegated C-boundary review under user instruction; not independent human sign-off.

C accepts the new Storage identity mapping subject to these boundaries:

1. `PreparedParticipantRef` and `PreparedTransactionGID` are Storage-owned participant identity/handle values. C MUST consume the exact pair from the authenticated Storage/COC evidence; C MUST NOT mint, rotate or replace them on retry.
2. `EngineNativeTransactionXIDRef` is Storage/engine evidence only. C MUST NOT use it as a provider idempotency key, Agent operation ID, authorization token or participant identity.
3. C's `ProviderIdempotencyKey` is a separate C-owned type and namespace. It MUST remain stable across retries for the same provider side effect and MUST NOT be derived by casting/reusing PreparedTransactionGID.
4. C may invoke the protected provider side effect only after the exact COC prepare intent is committed, Storage's PreparedParticipantReceipt is authoritative, I's terminal COMMIT decision is valid, D's required barrier/fence conditions are complete, and the final request boundary/digest is frozen.
5. CSubmitOutcome binds the exact provider request digest, ProviderIdempotencyKey, provider receipt and actual InferenceRequestId. Neither GID nor native XID proves provider success.
6. Provider timeout, process death, lost response or contradictory provider evidence remains UNKNOWN/IN_DOUBT. Retry queries the same provider key and same logical participant; it never allocates a new Storage GID or provider key.
7. If a D cutoff wins before the COC prepare-intent append, no Storage PREPARE and no provider side effect may occur. If the COC intent committed before cutoff, D must include the same PreparedParticipantRef in its barrier even if the Storage prepared receipt is not yet observed.

Exceptions: provider-specific same-key idempotency and authoritative outcome lookup remain unverified; no C production provider adapter or real COC/Storage integration is implemented; C-CO/JF10 runtime suites remain NOT RUN. The single-I-PolicyDomain restriction remains; this acceptance does not approve multi-domain atomicity or production activation.