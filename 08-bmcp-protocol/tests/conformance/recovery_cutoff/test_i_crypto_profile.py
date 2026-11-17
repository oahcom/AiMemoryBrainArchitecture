"""Independent Python RFC 8785 + Ed25519 candidate verifier for all I P0 families.

The deterministic private seed in the vector is TEST-ONLY. Never reuse it outside tests.
"""
import base64
import hashlib
import json
import shutil
import subprocess
import unittest
from pathlib import Path

import rfc8785
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parent
VECTOR = ROOT / "i_crypto_profile_vector.json"
NODE_ORACLE = ROOT / "i_crypto_profile_reference.mjs"


def payload_and_signature(vector, seed):
    p0 = vector["p0"]
    message_type = vector["message_type"]
    digest_field = vector["digest_field"]
    p0_bytes = rfc8785.dumps(p0)
    digest = hashlib.sha256(b"AIMBA-I-PAYLOAD-v1\0" + p0_bytes).hexdigest()
    signed_projection = dict(p0)
    signed_projection[digest_field] = digest
    signed_bytes = rfc8785.dumps(signed_projection)
    preimage = (
        b"AIMBA-I-SIGNATURE-v1\0"
        + b"AIMBA-I-CRYPTO-1.0\0"
        + message_type.encode("ascii")
        + b"\0"
        + signed_bytes
    )
    private_key = Ed25519PrivateKey.from_private_bytes(seed)
    signature = private_key.sign(preimage)
    public_raw = private_key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    private_key.public_key().verify(signature, preimage)
    return {
        "id": vector["id"],
        "p0_canonical_utf8": p0_bytes.decode("utf-8"),
        "digest": digest,
        "signed_projection_canonical_utf8": signed_bytes.decode("utf-8"),
        "signature_preimage_hex": preimage.hex(),
        "public_key_hex": public_raw.hex(),
        "signature_base64url": base64.urlsafe_b64encode(signature).decode("ascii").rstrip("="),
    }


class IProfileCrossLanguageVectors(unittest.TestCase):
    def test_CRYPTO_01_all_i_p0_families_match_node_rfc8785_and_ed25519(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js 22 is required")
        vector = json.loads(VECTOR.read_text(encoding="utf-8"))
        seed = bytes.fromhex(vector["seed_hex"])
        python_results = [payload_and_signature(v, seed) for v in vector["vectors"]]
        proc = subprocess.run(
            [node, str(NODE_ORACLE)], cwd=ROOT, check=True,
            capture_output=True, text=True, encoding="utf-8"
        )
        self.assertEqual(python_results, json.loads(proc.stdout))
        self.assertEqual(
            {v["message_type"] for v in vector["vectors"]},
            {"OWNER_LOCAL_PENDING_GATE", "OWNER_LOCAL_GATE_RELEASE",
             "JF10_I_TERMINAL_DECISION_OBSERVED", "I_COMPLETE_EMPTY_PROOF",
             "I_OUT_OF_SCOPE_PROOF", "I_ADMISSION_SNAPSHOT_MEMBERSHIP_PROOF"}
        )

    def test_CRYPTO_02_jcs_object_order_is_irrelevant_but_array_order_is_not(self):
        left = {"z": 1, "a": [1, 2], "é": "café"}
        right = {"é": "café", "a": [1, 2], "z": 1}
        changed_array = {"a": [2, 1], "z": 1, "é": "café"}
        self.assertEqual(rfc8785.dumps(left), rfc8785.dumps(right))
        self.assertNotEqual(rfc8785.dumps(left), rfc8785.dumps(changed_array))

    def test_CRYPTO_03_unicode_is_not_implicitly_normalized(self):
        self.assertNotEqual(
            rfc8785.dumps({"value": "\u00e9"}),
            rfc8785.dumps({"value": "e\u0301"})
        )

    def test_CRYPTO_04_non_finite_number_is_rejected(self):
        with self.assertRaises(Exception):
            rfc8785.dumps({"value": float("nan")})

    def test_CRYPTO_05_unified_p0_binds_exact_artifact_and_wire_versions(self):
        vector = json.loads(VECTOR.read_text(encoding="utf-8"))
        unified = [v for v in vector["vectors"] if v["message_type"] in {
            "OWNER_LOCAL_PENDING_GATE", "OWNER_LOCAL_GATE_RELEASE",
            "JF10_I_TERMINAL_DECISION_OBSERVED"
        }]
        self.assertEqual(len(unified), 3)
        for v in unified:
            self.assertEqual(v["p0"]["schema_artifact_revision"], "1.2.11")
            self.assertEqual(v["p0"]["schema_version"], "1.3.0")

    def test_CRYPTO_06_gate_release_distinguishes_manifest_content_and_record_digest(self):
        vector = json.loads(VECTOR.read_text(encoding="utf-8"))
        release = next(v["p0"] for v in vector["vectors"] if v["message_type"] == "OWNER_LOCAL_GATE_RELEASE")
        self.assertIn("manifest_content_digest", release)
        self.assertIn("manifest_record_entry_digest", release)
        self.assertNotIn("manifest_digest", release)

    def test_CRYPTO_07_membership_proof_p0_binds_exact_owner_snapshot_and_row(self):
        vector = json.loads(VECTOR.read_text(encoding="utf-8"))
        proof = next(v["p0"] for v in vector["vectors"] if v["message_type"] == "I_ADMISSION_SNAPSHOT_MEMBERSHIP_PROOF")
        required = {"owner_authority_ref","owner_ledger_ref","owner_ledger_version","owner_entry_ref",
            "owner_entry_digest","owner_admission_ref","owner_sequence_namespace","owner_local_sequence",
            "owner_high_water","owner_ledger_root","owner_snapshot_ref","owner_snapshot_digest",
            "owner_snapshot_attestation_ref","owner_snapshot_attestation_digest","owner_gate_ref",
            "owner_gate_generation","scope_ref","scope_generation","scope_binding_digest",
            "operation_identity_ref","operation_digest","request_digest","anti_rollback_anchor_ref",
            "key_status_generation","signature_profile_ref","key_id","key_version",
            "canonicalization_profile_ref","digest_profile_ref"}
        self.assertTrue(required.issubset(proof))
        self.assertNotIn("proof_digest", proof)
        self.assertNotIn("signature_ref", proof)
        self.assertEqual(proof["purpose"], "COC_RECOVERY_CUTOFF_MANIFEST_MEMBERSHIP")


if __name__ == "__main__":
    unittest.main(verbosity=2)
