import json, unittest
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError, RefResolver

ROOT=Path(__file__).resolve().parents[3]
SCHEMA=ROOT/"schemas"/"bmcp.recovery-join-1.0.2.schema.json"

def proof():
    d="a"*64
    return {
      "proof_ref":"proof:I:entry:7","owner_kind":"I","owner_authority_ref":"I:pd:1",
      "issuer_ref":"I:issuer:1","subject_ref":"I:entry:7","audience_ref":"COC:recovery-validator",
      "purpose":"COC_RECOVERY_CUTOFF_MANIFEST_MEMBERSHIP",
      "owner_ledger_ref":"I:admission-ledger:1","owner_ledger_version":"v9",
      "owner_entry_ref":"I:entry:7","owner_entry_digest":d,"owner_admission_ref":"I:admission:7",
      "owner_sequence_namespace":"I:pd:1/admission","owner_local_sequence":"7","owner_high_water":"12",
      "owner_ledger_root":d,"owner_snapshot_ref":"I:snapshot:9","owner_snapshot_digest":d,
      "owner_snapshot_attestation_ref":"I:attestation:9","owner_snapshot_attestation_digest":d,
      "owner_gate_ref":"I:gate:1","owner_gate_generation":"4","scope_ref":"scope:1","scope_generation":"2",
      "scope_binding_digest":d,"operation_identity_ref":"op:7","operation_digest":d,"request_digest":d,
      "anti_rollback_anchor_ref":"I:anchor:9","key_status_generation":"key-status:5",
      "signature_profile_ref":"I:profile:1","key_id":"I:key:1","key_version":"v3",
      "canonicalization_profile_ref":"I:jcs:1","digest_profile_ref":"I:sha256:1",
      "proof_digest":d,"signature_ref":"I:sig:7"
    }

class RecoveryJoin102Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.validator=Draft202012Validator(cls.schema["$defs"]["ownerSnapshotMembershipProof"],resolver=RefResolver.from_schema(cls.schema))

    def test_RJ102_01_schema_meta_validates(self):
        Draft202012Validator.check_schema(self.schema)

    def test_RJ102_02_exact_owner_membership_proof_is_valid(self):
        self.validator.validate(proof())

    def test_RJ102_03_missing_snapshot_attestation_digest_rejected(self):
        p=proof(); p.pop("owner_snapshot_attestation_digest")
        with self.assertRaises(ValidationError): self.validator.validate(p)

    def test_RJ102_04_missing_anti_rollback_anchor_rejected(self):
        p=proof(); p.pop("anti_rollback_anchor_ref")
        with self.assertRaises(ValidationError): self.validator.validate(p)

    def test_RJ102_05_wrong_purpose_rejected(self):
        p=proof(); p["purpose"]="GENERIC_SIGNATURE"
        with self.assertRaises(ValidationError): self.validator.validate(p)

    def test_RJ102_06_admission_join_requires_membership_proof_binding(self):
        required=set(self.schema["$defs"]["admissionJoin"]["required"])
        self.assertIn("owner_snapshot_membership_proof_ref",required)
        self.assertIn("owner_snapshot_membership_proof_digest",required)

    def test_RJ102_07_no_participant_disposition_requires_membership_proof_binding(self):
        required=set(self.schema["$defs"]["noParticipantDisposition"]["required"])
        self.assertIn("owner_snapshot_membership_proof_ref",required)
        self.assertIn("owner_snapshot_membership_proof_digest",required)

    def test_RJ102_08_top_level_requires_owner_proof_inventory(self):
        self.assertIn("owner_snapshot_membership_proofs",self.schema["required"])

if __name__=="__main__": unittest.main()
