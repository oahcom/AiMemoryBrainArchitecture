import unittest
from pathlib import Path

import yaml
from yaml.constructor import ConstructorError

from scripts.validate_aid_2026_001_manifest import (
    MANIFEST_PATH,
    load_yaml_unique,
    validate_manifest,
)


class ManifestUniqueKeyValidationTests(unittest.TestCase):
    def test_actual_manifest_parses_and_required_paths_exist(self):
        data = validate_manifest()
        self.assertEqual(data["work_item_id"], "AID-2026-001")
        self.assertEqual(data["class"], "ARCH")
        self.assertEqual(data["risk"], "R3")

    def test_duplicate_top_level_key_is_rejected(self):
        text = "work_item_id: AID-2026-001\nrisk: R3\nrisk: R2\n"
        with self.assertRaises(ConstructorError):
            load_yaml_unique(text)

    def test_duplicate_nested_key_is_rejected(self):
        text = "outer:\n  owner: D\n  owner: I\n"
        with self.assertRaises(ConstructorError):
            load_yaml_unique(text)

    def test_valid_nested_mapping_is_accepted(self):
        text = "outer:\n  owner: D\n  risk: R3\n"
        self.assertEqual(load_yaml_unique(text), {"outer": {"owner": "D", "risk": "R3"}})


if __name__ == "__main__":
    unittest.main(verbosity=2)
