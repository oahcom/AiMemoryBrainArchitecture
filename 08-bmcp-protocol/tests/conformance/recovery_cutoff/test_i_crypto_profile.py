"""Independent Python RFC 8785 + Ed25519 candidate verifier.

The deterministic private seed in the vector is TEST-ONLY. Never reuse it outside tests.
"""
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


def payload_and_signature(p0, seed):
    p0_bytes = rfc8785.dumps(p0)
    payload_digest = hashlib.sha256(
        b"AIMBA-I-PAYLOAD-v1\0" + p0_bytes
    ).hexdigest()
    signed_projection = dict(p0)
    signed_projection["payload_digest"] = payload_digest
    signed_bytes = rfc8785.dumps(signed_projection)
    preimage = (
        b"AIMBA-I-SIGNATURE-v1\0"
        + b"AIMBA-I-CRYPTO-1.0\0"
        + p0["message_type"].encode("ascii")
        + b"\0"
        + signed_bytes
    )
    private_key = Ed25519PrivateKey.from_private_bytes(seed)
    signature = private_key.sign(preimage)
    public_key = private_key.public_key()
    public_raw = public_key.public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    public_key.verify(signature, preimage)
    return {
        "p0_canonical_utf8": p0_bytes.decode("utf-8"),
        "payload_digest": payload_digest,
        "signed_projection_canonical_utf8": signed_bytes.decode("utf-8"),
        "signature_preimage_hex": preimage.hex(),
        "public_key_hex": public_raw.hex(),
        "signature_base64url": __import__("base64").urlsafe_b64encode(signature).decode("ascii").rstrip("="),
    }


class IProfileCrossLanguageVectors(unittest.TestCase):
    def test_CRYPTO_01_python_rfc8785_and_ed25519_match_node_independent_oracle(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js 22 is required")
        vector = json.loads(VECTOR.read_text(encoding="utf-8"))
        seed = bytes.fromhex(vector["seed_hex"])
        python_result = payload_and_signature(vector["p0"], seed)
        proc = subprocess.run(
            [node, str(NODE_ORACLE)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        node_result = json.loads(proc.stdout)
        self.assertEqual(python_result, node_result)

    def test_CRYPTO_02_jcs_object_order_is_irrelevant_but_array_order_is_not(self):
        left = {"z": 1, "a": [1, 2], "é": "café"}
        right = {"é": "café", "a": [1, 2], "z": 1}
        changed_array = {"a": [2, 1], "z": 1, "é": "café"}
        self.assertEqual(rfc8785.dumps(left), rfc8785.dumps(right))
        self.assertNotEqual(rfc8785.dumps(left), rfc8785.dumps(changed_array))

    def test_CRYPTO_03_unicode_is_not_implicitly_normalized(self):
        composed = {"value": "\u00e9"}
        decomposed = {"value": "e\u0301"}
        self.assertNotEqual(rfc8785.dumps(composed), rfc8785.dumps(decomposed))

    def test_CRYPTO_04_non_finite_number_is_rejected(self):
        with self.assertRaises(Exception):
            rfc8785.dumps({"value": float("nan")})


if __name__ == "__main__":
    unittest.main(verbosity=2)
