# Phase 3.8.6 — G Review of Per-Authority Storage Serialization Anchor
# Phase 3.8.6 — G 对每 Authority Storage Serialization Anchor 的复审

- Owner: G — Memory Context
- Exact Storage ADR Blob: `bb544ba2f346bdc130d524bd5c7310d86f367988`
- Decision: **ACCEPT WITH CONTEXT/APPLIED EVIDENCE CONDITIONS**
- Provenance: delegated G-role review, not independent human G Owner approval.

G accepts the anchor as a physical D/Storage ordering mechanism only. It does not become ContextVersion, ContextGeneration, AppliedCursor, provider outcome or Memory authority.

G 接受 Anchor 作为 D/Storage 物理排序机制，但它不成为 ContextVersion、ContextGeneration、AppliedCursor、Provider Outcome 或 Memory Authority。

1. Context compilation may reference only immutable, owner-authorized visible artifacts; PREPARED_HIDDEN/UNKNOWN never enter a serving Context.
2. G ContextVersion and Applied evidence remain G-owned and must reference exact D/I/C/Storage proofs; the anchor revision is not an Applied proof.
3. Full Applied requires exact recipient-side proof and currentness; a Storage visibility commit alone does not prove recipient application.
4. Forget/restore invalidates or rebuilds Context only from D/I/Storage authoritative outcomes, not anchor counters.
5. G cache/index/context read paths must fail closed on stale visibility pointer or missing owner evidence.

**ACCEPT WITH CONDITIONS.** Context Applied implementation and adversarial stale-cache/forget/restore tests remain L3/L4 OPEN.
