"""H-side independent verification of C's candidate JCS/Ed25519 vectors."""
import base64
import hashlib
import json
import shutil
import subprocess
import unittest
from pathlib import Path

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"
RECORDS = FIXTURES / "c_submit_outcome_1_0_0_vectors.json"
MANIFEST = FIXTURES / "c_crypto_profile_vector.json"
EXPECTED = FIXTURES / "c_crypto_profile_expected_vectors.json"
NODE_ORACLE = ROOT / "c_crypto_profile_h_reference.mjs"


def candidate(record, seed):
    p0 = {k: v for k, v in record.items() if k not in ("payload_digest", "signature")}
    p0_bytes = rfc8785.dumps(p0)
    digest = hashlib.sha256(b"AIMBA-C-PAYLOAD-v1\0" + p0_bytes).hexdigest()
    signed = dict(p0)
    signed["payload_digest"] = digest
    signed_bytes = rfc8785.dumps(signed)
    preimage = (
        b"AIMBA-C-SIGNATURE-v1\0"
        + b"AIMBA-C-CRYPTO-1.0\0"
        + record["message_type"].encode("ascii")
        + b"\0"
        + signed_bytes
    )
    private = Ed25519PrivateKey.from_private_bytes(seed)
    signature = private.sign(preimage)
    public_raw = private.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    summary = {
        "id": record["record_id"],
        "p0_sha256": hashlib.sha256(p0_bytes).hexdigest(),
        "payload_digest": digest,
        "signed_projection_sha256": hashlib.sha256(signed_bytes).hexdigest(),
        "signature_preimage_sha256": hashlib.sha256(preimage).hexdigest(),
        "public_key_hex": public_raw.hex(),
        "signature_base64url": base64.urlsafe_b64encode(signature).decode("ascii").rstrip("="),
    }
    return summary, private.public_key(), signature, preimage


class HIndependentCCryptoInterop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
        cls.fixture = json.loads(RECORDS.read_text(encoding="utf-8"))
        cls.records = {v["id"]: v["record"] for v in cls.fixture["vectors"]}
        cls.seed = bytes.fromhex(cls.manifest["seed_hex"])
        cls.built = [candidate(cls.records[i], cls.seed) for i in cls.manifest["vector_ids"]]

    def test_CI01_h_recomputes_five_static_candidate_vectors(self):
        summaries = [x[0] for x in self.built]
        self.assertEqual(summaries, self.expected["vectors"])
        self.assertEqual(self.expected["status"], "CANDIDATE_TEST_ONLY_NOT_REGISTERED")

    def test_CI02_h_verifies_all_ed25519_signatures_and_every_field_mutation(self):
        for vector_id, (summary, public, signature, preimage) in zip(self.manifest["vector_ids"], self.built):
            public.verify(signature, preimage)
            record = self.records[vector_id]
            p0 = {k: v for k, v in record.items() if k not in ("payload_digest", "signature")}
            for key, value in p0.items():
                mutated = dict(record)
                mutated[key] = value + "-mutated" if isinstance(value, str) else "mutated"
                _, _, _, mutated_preimage = candidate(mutated, self.seed)
                with self.assertRaises(InvalidSignature, msg=f"{vector_id}:{key}"):
                    public.verify(signature, mutated_preimage)

    def test_CI03_h_node_and_python_independent_implementations_match_expected(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js 22 is required")
        proc = subprocess.run([node, str(NODE_ORACLE)], cwd=ROOT, check=True,
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(json.loads(proc.stdout), self.expected["vectors"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
