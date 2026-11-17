# H Owner — Exact COC Durable Protocol Wire-Boundary Acceptance

- Exact Storage protocol Blob: `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- H protocol source Blob: `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- H JF-10 schema candidate Blob: `a8a945cc3623c2907003b93625e3c79742150944`
- Decision: **ACCEPT WITH H-OWNED WIRE / AUTHENTICATION CONDITIONS**
- Mode: delegated H-boundary review under user instruction; not independent human sign-off.

H accepts the protocol's message/authority separation:
1. COCCommitReceipt and COC positions are typed COC evidence; I sequencer, D fence and Storage XID/transaction positions remain distinct opaque references.
2. H preserves owner-issued references and signatures; it does not mint, infer, compare or upgrade I authorization, D clearance, Storage visibility, C provider outcome or G Applied.
3. JF-10 and recovery-batch message families use the authenticated 1.1.0 envelope, exact immutable tuple, SHA-256 digest fields, issuer/signer binding and replay/idempotency rules.
4. Unknown critical fields, duplicate JSON keys, malformed refs, wrong issuer/signer, digest mismatch and tuple conflicts must be rejected before consumer delivery.
5. A COC append or H ACK is not owner terminality. Unknown/missing owner evidence remains UNKNOWN.

Exceptions: JSON Schema is a documentation-derived candidate, not generated from a normative IDL; signature/channel-binding verification, duplicate-key canonical parser, SDK interoperability and runtime conformance remain NOT RUN. Schema is not production-frozen.