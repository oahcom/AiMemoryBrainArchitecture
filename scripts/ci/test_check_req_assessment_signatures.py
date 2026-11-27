import unittest

from scripts.ci.check_req_assessment_signatures import COMMENT_IDS, EXPECTED, inspect


def valid_record(comment_id):
    expected = EXPECTED[comment_id]
    return {
        "id": comment_id,
        "body": (
            f"- assessor: `REQ-01 Risk Assessment Owner — ChatGPT session {expected['assessor_session']}`\n"
            f"- assessed_version: `{expected['assessed_version']}`\n"
            f"- evidence_baseline: `main@{expected['assessed_version']}`\n"
        ),
    }


class SignatureCommentCheckerTests(unittest.TestCase):
    def fetch_all(self, overrides=None):
        records = {comment_id: valid_record(comment_id) for comment_id in COMMENT_IDS}
        records.update(overrides or {})
        return lambda comment_id: records[comment_id]

    def test_all_four_historical_comments_pass(self):
        findings = inspect(self.fetch_all())
        self.assertEqual(4, sum(item.startswith("PASS ") for item in findings))
        self.assertFalse(any(item.startswith("FAIL ") for item in findings))

    def test_each_missing_field_fails(self):
        for name in ("assessor", "assessed_version", "evidence_baseline"):
            with self.subTest(field=name):
                record = valid_record(COMMENT_IDS[0])
                record["body"] = "\n".join(
                    line for line in record["body"].splitlines()
                    if not line.startswith(f"- {name}:")
                )
                findings = inspect(self.fetch_all({COMMENT_IDS[0]: record}))
                self.assertTrue(any(f"missing or empty {name}" in item for item in findings))

    def test_invalid_or_wrong_assessed_version_fails(self):
        for value in ("abc", "g" * 40, "a" * 40):
            with self.subTest(value=value):
                record = valid_record(COMMENT_IDS[0])
                record["body"] = (
                    f"- assessor: `REQ-01 Risk Assessment Owner — ChatGPT session {EXPECTED[COMMENT_IDS[0]]['assessor_session']}`\n"
                    f"- assessed_version: `{value}`\n"
                    f"- evidence_baseline: `main@{EXPECTED[COMMENT_IDS[0]]['assessed_version']}`\n"
                )
                findings = inspect(self.fetch_all({COMMENT_IDS[0]: record}))
                self.assertTrue(any(item.startswith("FAIL ") and "assessed_version" in item for item in findings))

    def test_wrong_assessor_session_fails(self):
        record = valid_record(COMMENT_IDS[0])
        record["body"] = record["body"].replace(
            EXPECTED[COMMENT_IDS[0]]["assessor_session"], "unknown-session"
        )
        findings = inspect(self.fetch_all({COMMENT_IDS[0]: record}))
        self.assertTrue(any("assessor does not identify" in item for item in findings))

    def test_wrong_evidence_baseline_fails(self):
        record = valid_record(COMMENT_IDS[0])
        record["body"] = record["body"].replace(
            f"main@{EXPECTED[COMMENT_IDS[0]]['assessed_version']}", "main@"+("a"*40)
        )
        findings = inspect(self.fetch_all({COMMENT_IDS[0]: record}))
        self.assertTrue(any("evidence_baseline differs" in item for item in findings))

    def test_missing_comment_fails_closed(self):
        def missing(comment_id):
            if comment_id == COMMENT_IDS[0]:
                raise FileNotFoundError("404")
            return valid_record(comment_id)
        findings = inspect(missing)
        self.assertTrue(any("unable to read record" in item for item in findings))

    def test_wrong_returned_comment_id_fails(self):
        record = valid_record(COMMENT_IDS[0])
        record["id"] = -1
        findings = inspect(self.fetch_all({COMMENT_IDS[0]: record}))
        self.assertTrue(any("different comment id" in item for item in findings))

    def test_output_is_deterministic(self):
        fetcher = self.fetch_all()
        self.assertEqual(inspect(fetcher), inspect(fetcher))


if __name__ == "__main__":
    unittest.main()
