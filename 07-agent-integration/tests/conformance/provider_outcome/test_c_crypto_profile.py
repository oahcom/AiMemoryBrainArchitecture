"""Candidate-only Python JCS/SHA-256/Ed25519 vectors for C Provider Outcome."""
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
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "c_submit_outcome_1_0_0_vectors.json"
SCHEMA = ROOT.parents[2] / "schemas" / "c-submit-outcome-1.0.0.schema.json"
VECTOR = ROOT / "c_crypto_profile_vector.json"
NODE_ORACLE = ROOT / "c_crypto_profile_reference.mjs"


def build(record, seed):
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
    public = private.public_key()
    public_raw = public.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    public.verify(signature, preimage)
    return {
        "id": record["record_id"],
        "p0_canonical_utf8": p0_bytes.decode("utf-8"),
        "digest": digest,
        "signed_projection_canonical_utf8": signed_bytes.decode("utf-8"),
        "signature_preimage_hex": preimage.hex(),
        "public_key_hex": public_raw.hex(),
        "signature_base64url": base64.urlsafe_b64encode(signature).decode("ascii").rstrip("="),
        "signed_member_count": len(p0),
    }, public, signature


class CProviderOutcomeCryptoCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(VECTOR.read_text(encoding="utf-8"))
        cls.fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.records = {v["id"]: v["record"] for v in cls.fixtures["vectors"]}
        cls.seed = bytes.fromhex(cls.manifest["seed_hex"])
        cls.outputs = []
        cls.material = []
        for vector_id in cls.manifest["vector_ids"]:
            output, public, signature = build(cls.records[vector_id], cls.seed)
            cls.outputs.append(output)
            cls.material.append((vector_id, public, signature))

    def test_CRYPTO_C01_five_outcome_families_have_valid_test_only_signatures(self):
        self.assertEqual(len(self.outputs), 5)
        self.assertEqual(self.manifest["profile_status"], "PROPOSED_NOT_REGISTERED")
        self.assertIn("NEVER REUSE", self.manifest["seed_disclaimer"])
        for output, (vector_id, public, signature) in zip(self.outputs, self.material):
            preimage = bytes.fromhex(output["signature_preimage_hex"])
            public.verify(signature, preimage)
            record = self.records[vector_id]
            signed_record = dict(record)
            signed_record["payload_digest"] = output["digest"]
            signed_record["signature"] = output["signature_base64url"]
            Draft202012Validator(self.schema, format_checker=FormatChecker()).validate(signed_record)

    def test_CRYPTO_C02_every_present_p0_member_is_signature_covered(self):
        for vector_id, public, signature in self.material:
            record = self.records[vector_id]
            p0 = {k: v for k, v in record.items() if k not in ("payload_digest", "signature")}
            original, _, _ = build(record, self.seed)
            for key, value in p0.items():
                mutated = dict(record)
                mutated[key] = value + "-mutated" if isinstance(value, str) else "mutated"
                new_output, _, _ = build(mutated, self.seed)
                mutated_preimage = bytes.fromhex(new_output["signature_preimage_hex"])
                with self.assertRaises(InvalidSignature, msg=f"{vector_id}:{key}"):
                    public.verify(signature, mutated_preimage)

    def test_CRYPTO_C03_python_and_node_candidate_bytes_and_signatures_match(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js 22 is required")
        proc = subprocess.run(
            [node, str(NODE_ORACLE)], cwd=ROOT, check=True,
            capture_output=True, text=True, encoding="utf-8"
        )
        self.assertEqual(self.outputs, json.loads(proc.stdout))
        summaries = []
        for output in self.outputs:
            p0_bytes = output["p0_canonical_utf8"].encode("utf-8")
            signed_bytes = output["signed_projection_canonical_utf8"].encode("utf-8")
            preimage = bytes.fromhex(output["signature_preimage_hex"])
            summaries.append({
                "id": output["id"],
                "p0_sha256": hashlib.sha256(p0_bytes).hexdigest(),
                "payload_digest": output["digest"],
                "signed_projection_sha256": hashlib.sha256(signed_bytes).hexdigest(),
                "signature_preimage_sha256": hashlib.sha256(preimage).hexdigest(),
                "public_key_hex": output["public_key_hex"],
                "signature_base64url": output["signature_base64url"],
            })
        print("C_CRYPTO_EXPECTED_BEGIN")
        print(json.dumps(summaries, separators=(",", ":")))
        print("C_CRYPTO_EXPECTED_END")


if __name__ == "__main__":
    unittest.main(verbosity=2)
