import unittest

from strict_json_parser import (DuplicateKeyError, ProtocolParseError,
                                UnknownCriticalExtension, parse_strict_json,
                                validate_critical_extensions)


class StrictJsonParserTests(unittest.TestCase):
    def test_valid_object_parses(self):
        self.assertEqual(parse_strict_json(b'{"message_type":"X","n":1}')["n"], 1)

    def test_duplicate_top_level_key_rejected(self):
        with self.assertRaises(DuplicateKeyError):
            parse_strict_json('{"message_type":"A","message_type":"B"}')

    def test_duplicate_nested_key_rejected(self):
        with self.assertRaises(DuplicateKeyError):
            parse_strict_json('{"outer":{"x":1,"x":2}}')

    def test_non_finite_number_rejected(self):
        with self.assertRaises(ProtocolParseError):
            parse_strict_json('{"value":NaN}')

    def test_invalid_utf8_rejected(self):
        with self.assertRaises(ProtocolParseError):
            parse_strict_json(b'{"x":"\xff"}')

    def test_oversized_message_rejected(self):
        with self.assertRaises(ProtocolParseError):
            parse_strict_json('{"x":"123456"}', max_bytes=5)

    def test_excessive_nesting_rejected(self):
        with self.assertRaises(ProtocolParseError):
            parse_strict_json('{"a":{"b":{"c":1}}}', max_depth=2)

    def test_non_object_root_rejected(self):
        with self.assertRaises(ProtocolParseError):
            parse_strict_json('["not","an","envelope"]')

    def test_unknown_noncritical_extension_is_preserved_opaque(self):
        message = {"message_type": "X", "x_vendor": {"opaque": True}}
        opaque = validate_critical_extensions(message, known_fields={"message_type"})
        self.assertEqual(opaque, {"x_vendor": {"opaque": True}})

    def test_unknown_critical_extension_is_rejected(self):
        message = {"message_type": "X", "critical_extensions": ["x_unknown"],
                   "x_unknown": {"must_understand": True}}
        with self.assertRaises(UnknownCriticalExtension):
            validate_critical_extensions(message, known_fields={"message_type"})

    def test_supported_critical_extension_is_accepted(self):
        message = {"message_type": "X", "critical_extensions": ["x_known"],
                   "x_known": {"value": 1}}
        opaque = validate_critical_extensions(message, known_fields={"message_type"},
                                              known_extensions={"x_known"})
        self.assertEqual(opaque, {"x_known": {"value": 1}})

    def test_critical_extensions_type_and_duplicates_rejected(self):
        with self.assertRaises(ProtocolParseError):
            validate_critical_extensions({"critical_extensions": "x"}, known_fields=set())
        with self.assertRaises(ProtocolParseError):
            validate_critical_extensions({"critical_extensions": ["x", "x"]}, known_fields=set())


if __name__ == "__main__":
    unittest.main()