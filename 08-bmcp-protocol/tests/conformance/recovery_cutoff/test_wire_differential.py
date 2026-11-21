"""Cross-language differential vectors for the TEST-ONLY HRC-TEST-v1 profile."""
import hashlib
import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VECTORS = ROOT / "wire_interop_vectors.json"
JS_ORACLE = ROOT / "wire_interop_reference.mjs"


def python_canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


class CrossLanguageWireDifferential(unittest.TestCase):
    def test_XLANG_01_python_and_node_match_fixed_utf8_and_digest_vectors(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js 22 must be installed by the CI workflow")
        vectors = json.loads(VECTORS.read_text(encoding="utf-8"))
        expected = []
        for vector in vectors:
            canonical = python_canonical(vector["value"])
            digest = hashlib.sha256(
                vector["domain"].encode("utf-8") + b"\0" + canonical.encode("utf-8")
            ).hexdigest()
            self.assertEqual(canonical, vector["expected_canonical_utf8"])
            self.assertEqual(digest, vector["expected_digest_sha256"])
            expected.append({
                "id": vector["id"],
                "canonical_utf8": canonical,
                "digest_sha256": digest,
            })

        result = subprocess.run(
            [node, str(JS_ORACLE)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(json.loads(result.stdout), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
