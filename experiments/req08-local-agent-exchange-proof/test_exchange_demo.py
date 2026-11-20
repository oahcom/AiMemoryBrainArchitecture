import copy, hashlib, json, unittest
from exchange_demo import Agent, authorize, build_envelope, make_fixture, receive

class ExchangeProofTests(unittest.TestCase):
    def setUp(self):
        self.sender, self.receiver, self.memory, self.grant = make_fixture()
        self.envelope = build_envelope(self.sender, self.memory, self.grant)

    def test_cross_agent_provider_exchange_preserves_provenance(self):
        result = receive(self.envelope, self.receiver)
        self.assertEqual(result["status"], "ACCEPTED")
        self.assertEqual((result["source_agent"], result["recipient_agent"]), ("agent.alpha", "agent.beta"))
        self.assertEqual((result["source_provider"], result["recipient_provider"]), ("provider-a", "provider-b"))
        self.assertEqual((result["source_model"], result["recipient_model"]), ("model-alpha", "model-beta"))
        self.assertEqual(result["source_record_id"], "record.alpha.001")

    def test_cross_tenant_exchange_is_denied(self):
        other = Agent("agent.beta", "provider-b", "model-beta", "tenant.blue")
        with self.assertRaisesRegex(PermissionError, "TENANT_MISMATCH"):
            receive(self.envelope, other)

    def test_wrong_grantee_is_denied(self):
        other = Agent("agent.gamma", "provider-c", "model-gamma", "tenant.red")
        with self.assertRaisesRegex(PermissionError, "GRANTEE_MISMATCH"):
            receive(self.envelope, other)

    def test_wrong_audience_is_denied_even_for_named_grantee(self):
        altered = copy.deepcopy(self.envelope)
        altered["grant"]["audience"] = "agent.gamma"
        with self.assertRaisesRegex(PermissionError, "AUDIENCE_MISMATCH"):
            receive(altered, self.receiver)

    def test_revoked_grant_is_denied(self):
        altered = copy.deepcopy(self.envelope)
        altered["grant"]["revoked"] = True
        with self.assertRaisesRegex(PermissionError, "GRANT_REVOKED"):
            receive(altered, self.receiver)

    def test_tampered_payload_is_denied(self):
        altered = copy.deepcopy(self.envelope)
        altered["memory"]["content"] = "tampered"
        with self.assertRaisesRegex(ValueError, "PAYLOAD_DIGEST_MISMATCH"):
            receive(altered, self.receiver)

    def test_transport_sender_cannot_spoof_source_agent(self):
        altered = copy.deepcopy(self.envelope)
        altered["transport_sender"] = "agent.evil"
        with self.assertRaisesRegex(ValueError, "TRANSPORT_SOURCE_MISMATCH"):
            receive(altered, self.receiver)

    def test_resource_substitution_is_denied(self):
        altered = copy.deepcopy(self.envelope)
        altered["memory"]["resource_id"] = "memory.other"
        altered["payload_sha256"] = hashlib.sha256(json.dumps(
            altered["memory"], ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")).hexdigest()
        with self.assertRaisesRegex(PermissionError, "RESOURCE_MISMATCH"):
            receive(altered, self.receiver)

    def test_ungranted_action_is_denied(self):
        with self.assertRaisesRegex(PermissionError, "ACTION_NOT_GRANTED"):
            authorize(self.grant, self.receiver, self.memory, action="delete")

    def test_missing_delegation_chain_is_denied(self):
        altered = copy.deepcopy(self.envelope)
        altered["grant"]["delegation_chain"] = []
        with self.assertRaisesRegex(PermissionError, "INVALID_DELEGATION_CHAIN"):
            receive(altered, self.receiver)

if __name__ == "__main__":
    unittest.main(verbosity=2)
