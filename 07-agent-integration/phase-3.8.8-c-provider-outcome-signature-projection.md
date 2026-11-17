# Phase 3.8.8 — C Provider Outcome Exact Signature Projection

- Owner perspective: C — Provider Outcome semantic authority
- Status: PROPOSED C-owned projection contract; not cryptographically registered or frozen.
- Exact dependencies:
  - C semantic amendment Phase 3.8.6 Blob `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4`
  - C review of I candidate Phase 3.8.7 Blob `794d1dc49f034152407e3a42ba5ac937ea3539f8`
  - I candidate profile addendum Blob `1bcddbaaa4a9ca730d492a6554941becac305668`
  - H schema artifact 1.2.11 Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
  - H semantic validator contract current Blob `d1ab8c102f097100ed3948c5283dabc4e5e8690e`
- Provenance: delegated C-role simulation at user's direction; not independent human C Owner approval.

## 1. Projection model and authority boundary

C owns the semantic projection of the immutable CSubmitOutcome object. H owns the BMCP wire envelope and its exact projection mapping. I owns cryptographic suite governance and key-trust policy. These responsibilities are not interchangeable.

Define two independently validated projections:

- **C-P0**: exhaustive C-owned immutable semantic payload, excluding only the derived `payload_digest` and `signature` fields.
- **BMCP-C-WIRE-P0**: the H-defined message-family projection. It MUST bind the exact schema artifact revision, wire family, message identity, and immutable C object reference/digest. H MUST NOT silently replace C-P0 or assume that every C-P0 field is inline in the 1.2.11 envelope.

The immutable C object is the source of truth for C-owned semantics. Any duplicated wire field is a consistency assertion: it MUST equal the dereferenced C object exactly. A missing required field in both locations is INVALID if the contract requires its existence; unavailable dereference/currentness is UNKNOWN.

## 2. Exhaustive C-P0 field groups

The following is the required semantic allowlist. Every field is either present as a typed value or represented by an explicit schema-defined absent/null state. No wildcard omission, serializer default, implicit normalization or "non-semantic metadata" exclusion is permitted.

| Group | Required signed members |
|---|---|
| Profile and schema binding | profile bundle ID/version; schema ID; wire family version; exact schema artifact revision; message type |
| Record identity | CSubmitOutcomeRef; immutable record ID; message ID; nonce; creation time; validity interval; supersession/reconciliation parent ref where applicable |
| Authority and routing | C issuer/owner authority ref; sender; subject; audience; purpose; authenticated key ID/version; profile ID |
| Admission provenance | CAdmissionRef; CAdmissionDigest; C owner ledger ID/version; owner-local sequence; high-water mark; ledger root/checkpoint ref and digest |
| Gate commitment | CGateRef; CGateGeneration; gate state at commit; gate CAS/serialization authority ref; EGRESS_COMMITTED record ref/digest |
| Provider attempt | ProviderAttemptRef; ProviderAttemptGeneration; provider ref; provider account/tenant ref; adapter ref/build; API operation; endpoint ref; region ref |
| Idempotency | idempotency namespace ref; key ref or protected key commitment; provider capability record ref/version/digest; key retention boundary |
| Request boundary | FinalRequestBoundaryRef; exact request digest; content/media type; method/operation; canonical request commitment; transport invocation identity |
| Outcome | exact outcome enum; outcome-specific terminality; provider request/receipt refs and digests; no-handoff/not-invoked proof refs and digests; same-key lookup proof ref/digest; reason code |
| COC correlation | ParticipantIntentRef and ParticipantReservationRef as a complete pair, OR explicit null plus schema-defined reason; COC operation/transaction correlation ref; exact request-digest join |
| Append-only linkage | prior observation ref/digest; reconciliation/supersession ref/digest; observed-at time; source authority; immutable sequence |

### 2.1 Secret and high-entropy values

Signing a projection does not require exposing raw provider credentials or raw idempotency secrets. Where a secret cannot be serialized, the projection MUST include a stable authority-issued opaque reference or a cryptographic commitment whose algorithm, scope, key version and equality semantics are specified. A plain truncated hash is not an acceptable substitute. The same opaque reference/commitment must be used consistently by the C owner ledger, adapter and lookup proof.

### 2.2 Absent, null and empty are distinct

- Absent means the member is not present in the serialized object.
- Null means the member is explicitly present with JSON null.
- Empty string/array/object are distinct values.
- A required member cannot be satisfied by any of these unless the exact field rule explicitly permits it.
- A null ParticipantIntent/Reservation pair requires an explicit reason and cannot erase C owner-local admission evidence.
- One member of the pair without the other is INVALID.

## 3. Projection construction

Subject to I approval of the algorithm suite and H approval of exact wire mapping:

1. Parse strict UTF-8 JSON; reject duplicate keys before materialization.
2. Validate the exact schema artifact revision 1.2.11 and wire family 1.3.0.
3. Construct C-P0 using the exact allowlist and deterministic field-presence rules.
4. Canonicalize C-P0 with the registered canonicalization profile; no Unicode normalization beyond that profile.
5. Compute the domain-separated payload digest using the registered digest construction.
6. Add the digest field, canonicalize the complete signed projection, and construct the domain-separated signature preimage with exact profile ID and message type.
7. Verify the signature against authenticated C key-status evidence and the exact audience/purpose.
8. Independently validate referenced C ledger, gate, attempt, provider evidence and COC joins. A valid signature is not proof that the signed assertions are true.

The candidate construction in I Phase 3.8.4 remains a proposal until I issues an exact approval and profile registration. No implementation is implied by this document.

## 4. Exclusion policy

Only the following may be outside C-P0, and only because they are independently authenticated and joined by H:

- COC quorum certificate, participant ordering and manifest position;
- transport channel-binding/session metadata;
- validator execution metadata and local diagnostic annotations.

Each exclusion MUST have an explicit owner, exact schema path, independent verification rule and immutable join key. If an excluded value changes the meaning, identity, audience, target, request bytes, provider attempt, gate generation or outcome, it is not excludable and MUST be added to the signed projection.

No generic `additionalProperties`, wildcard ignore list, mutable display label, or "transport-only" blanket exclusion is permitted.

## 5. Required field-mutation vectors

For every signed member in Section 2, H/C conformance vectors MUST mutate exactly that member and prove signature verification fails. Also require:

- absent vs null vs empty vs populated;
- changed schema artifact revision or wire family;
- changed audience, purpose, sender, issuer, subject, nonce or message ID;
- changed CAdmissionDigest, ledger sequence/high-water/root;
- changed gate generation or ProviderAttemptGeneration;
- changed provider/account/endpoint/region/API operation;
- changed namespace/key reference, final request boundary or request digest;
- changed outcome enum or evidence ref/digest;
- ParticipantIntent/Reservation pair mismatch and null-without-reason;
- changed supersession parent or reconciliation link;
- duplicate JSON keys, unknown critical fields, malformed UTF-8 and non-canonical encoding;
- cross-owner signature replay and cross-message replay;
- old profile/key version after revocation or anti-rollback checkpoint advance.

Every vector must state expected parse/schema/crypto/semantic layer and expected VALID/INVALID/UNKNOWN result. A signature failure is INVALID; inability to retrieve current key status or authoritative referenced evidence is UNKNOWN.

## 6. H wire mapping obligations

H MUST publish a separate exact mapping table containing, for every BMCP 1.2.11 field:

- JSON Pointer and schema type/requiredness;
- whether it is inline, dereferenced or independently verified;
- exact C-P0 member(s) it duplicates or binds;
- equality/normalization rule;
- authority that issues the referenced object;
- behavior on absent/null/mismatch/unavailable;
- whether the field is covered by C-P0, BMCP-C-WIRE-P0 or another authority's proof.

Do not infer JSON Pointer names from prose. The mapping must be derived from the exact schema blob and the actual immutable C object contract. If a required semantic value is not represented inline, H MUST point to the typed immutable C object reference and validate its digest and contents.

## 7. Decision

C publishes this as the exact semantic projection proposal and accepts responsibility for the C-owned field inventory. It does not claim I approval, H wire conformance, signature implementation, key registration, test execution, adapter certification, production readiness or exactly-once delivery.

**Disposition: PROPOSED — C projection defined; I profile approval, H schema mapping, executable vectors and independent execution remain open.**
