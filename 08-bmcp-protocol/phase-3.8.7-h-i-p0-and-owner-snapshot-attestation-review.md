# Phase 3.8.7 — H Exact Review of I P0 Allowlists and Owner Snapshot Attestation
# Phase 3.8.7 — H 对 I P0 白名单与 Owner Snapshot Attestation 的精确审查

- Reviewer: H — BMCP Protocol and Adapter Authentication
- Branch: `session-h-bmcp-protocol`
- Exact I P0 addendum: `09-security-governance/phase-3.8.7-i-exact-signed-object-p0-allowlists.md`
- I P0 Blob: `739dc15e3cca33aef3f012f713b988e5528d4ad9`
- Exact H owner-snapshot attestation schema: `08-bmcp-protocol/schemas/bmcp.i-owner-snapshot-attestation-1.0.0.schema.json`
- H schema Blob: `REPLACE_AFTER_READBACK`
- H unified schema 1.2.8: Blob `70b892797d07489936300a26c0dedfafe1d6e746`
- H RecoveryJoin 1.0.1: Blob `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c`
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS — P0 FIELD CONTRACT; SNAPSHOT SCHEMA CANDIDATE**
- English and Chinese are normative peers.

## 1. H decision / H 决议

H accepts I's exact P0 allowlists for:
- I-owned `OWNER_LOCAL_PENDING_GATE`;
- I-owned `OWNER_LOCAL_GATE_RELEASE`;
- `JF10_I_TERMINAL_DECISION_OBSERVED`;
- standalone I owner snapshot attestation;
- I complete-empty and out-of-scope proof objects;
- I CommitAuthorizationReceipt and ITerminalProof.

H confirms the BMCP common envelope applies only to the three message families explicitly identified by I. Standalone referenced proof objects use their own object-specific P0 fields and do not inherit unrelated envelope fields.

H 接受 I 为上述消息族/独立 Proof Object 定义的精确 P0 白名单。H 确认 BMCP Common Envelope 仅适用于 I 指定的三个消息族；独立引用 Proof Object 使用各自对象专属 P0，不继承无关 Envelope 字段。

## 2. Snapshot schema mapping / Snapshot Schema 映射

The new `IOwnerSnapshotAttestation/1.0.0` schema is structurally consistent with the I P0 field list and H unified 1.2.8 `ownerSnapshot` summary.

Exact mapping:
- `owner_snapshot_attestation_ref` = attestation `attestation_ref`;
- `owner_snapshot_attestation_digest` = attestation `attestation_digest`;
- `owner` = I;
- `owner_gate_ref/generation` = attestation `gate_ref/generation`;
- request/admission high-water, count, set digest and ledger roots = exact same-named attestation fields;
- `owner_ledger_root`, `anti_rollback_anchor_ref` and `owner_specific_high_waters` = exact same-named attestation fields.

The underlying `snapshot_digest` is distinct from the attestation digest. H must reject any substitution or equality assumption between them.

## 3. Binding semantic amendments / 约束性语义修订

1. Unified schema 1.2.8 leaves `owner_snapshot_attestation_digest` structurally optional for compatibility. For `owner=I`, H semantic validation MUST require both attestation ref and digest.
2. The attestation digest must equal the recomputed digest of the exact I-signed P0; the ref must resolve to the exact `attestation_ref`.
3. The outer COC ownerSnapshot summary must match the attestation field-for-field. No field may be copied from a different snapshot/generation.
4. `request_enumeration_status=COMPLETE` and `admission_enumeration_status=COMPLETE` require complete pagination and owner high-water binding. UNKNOWN/INCOMPLETE blocks RecoveryJoin completion.
5. If request/admission count is zero, the corresponding complete-empty proof ref must be non-null and independently verified; if count is nonzero, the corresponding complete-empty proof ref must be null.
6. A complete-empty proof is not a missing row or empty response. It must be signed, scoped, high-water-bound and anti-rollback-bound.
7. The P0 allowlist is exact for the reviewed schema versions. A successor schema adding fields requires a successor projection review; unknown critical fields fail closed.

## 4. L3 vector requirements / L3 向量要求

H requires:
- exact P0 extraction for all three I BMCP message families;
- exact owner snapshot attestation digest and summary equality;
- snapshot digest vs attestation digest substitution rejection;
- complete-empty proof count/ref consistency;
- missing digest on I ownerSnapshot rejected semantically despite structural optionality;
- incomplete pagination/high-water mismatch rejected;
- wrong I owner/audience/profile/key version rejected;
- COC-appended proof changes do not alter I P0 but invalid COC proof still rejects the envelope;
- independent implementations produce byte-identical P0, digest and signature preimage.

Existing H 101/101 candidate CI does not prove all these per-family vectors. They remain L3 OPEN until added and passed.

## 5. Final H disposition / H 最终结论

**ACCEPT WITH ENUMERATED AMENDMENTS — P0 FIELD CONTRACT; SNAPSHOT SCHEMA CANDIDATE.**

H accepts the I P0 addendum and the new owner-snapshot attestation schema as exact candidates. H does not claim production semantic validator, full per-family differential vectors, live I trust/key registry, historical checkpoint, anti-rollback deployment, schema freeze or production conformance.

**有条件接受 — P0 字段合同；Snapshot Schema 候选。** H 接受精确 P0 与新 Attestation Schema 候选；不声明生产 Semantic Validator、逐消息族差分向量、实时 I Trust/Key Registry、历史 Checkpoint、Anti-rollback 部署、Schema 冻结或生产符合性。
