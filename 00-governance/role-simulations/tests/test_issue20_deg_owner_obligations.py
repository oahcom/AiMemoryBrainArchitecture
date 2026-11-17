"""Additional D/E/G Owner-obligation tests; coordinator reference model only."""
import unittest
from issue20_reference_model import DAuthority, EDerivation, GContextVersion, ProtocolError, UnknownOutcome


class DProducerWorkObligationTests(unittest.TestCase):
    def test_late_derivative_reopens_fence_and_advances_high_water(self):
        d = DAuthority()
        d.admit("producer-work-1", "request-1")
        captured = d.install_fence()
        derivative = d.admit_late_derivative("producer-work-1", "derivative-1", "derived-1")
        self.assertEqual(derivative["late_derivative_of"], "producer-work-1")
        self.assertGreater(derivative["sequence"], captured["high_water"])
        self.assertIn("derivative-1", d.unresolved)
        with self.assertRaises(ProtocolError):
            d.release_fence(captured["generation"], captured["high_water"])

    def test_late_derivative_requires_known_parent_and_immutable_join(self):
        d = DAuthority()
        with self.assertRaises(ProtocolError):
            d.admit_late_derivative("unknown-parent", "child", "digest")
        d.admit("parent", "parent-digest")
        first = d.admit_late_derivative("parent", "child", "child-digest")
        self.assertEqual(first, d.admit_late_derivative("parent", "child", "child-digest"))
        with self.assertRaises(ProtocolError):
            d.admit_late_derivative("other-parent", "child", "child-digest")

    def test_release_requires_refreshed_hwm_after_late_derivative_terminal(self):
        d = DAuthority()
        d.admit("parent", "parent-digest")
        snap = d.install_fence()
        child = d.admit_late_derivative("parent", "child", "child-digest")
        d.terminalize("parent", "PUBLISHED")
        d.terminalize("child", "NO_PUBLICATION")
        with self.assertRaises(ProtocolError):
            d.release_fence(snap["generation"], snap["high_water"])
        self.assertTrue(d.release_fence(snap["generation"], child["sequence"])["released"])

    def test_fence_release_rejects_unresolved_publication_and_stale_hwm(self):
        d = DAuthority()
        d.admit("work", "digest")
        snap = d.install_fence()
        with self.assertRaises(ProtocolError):
            d.release_fence(snap["generation"], snap["high_water"])
        d.terminalize("work", "NO_PUBLICATION")
        with self.assertRaises(ProtocolError):
            d.release_fence(snap["generation"], snap["high_water"] - 1)


class EAttemptLeaseAndReplayObligationTests(unittest.TestCase):
    def test_d_producer_registration_must_precede_first_attempt(self):
        e = EDerivation("work-unregistered", "request-digest")
        with self.assertRaises(ProtocolError):
            e.retry("request-digest")
        e.register_producer("d-registration:work-unregistered")
        self.assertEqual(e.retry("request-digest"), 1)

    def test_expiry_is_exact_attempt_bound_and_preserves_work_identity(self):
        e = EDerivation("work-1", "request-digest")
        e.register_producer("d-registration:" + e.work_item_id)
        e.retry("request-digest")
        lease1 = e.lease_id
        expired = e.expire_lease(lease1)
        self.assertEqual(expired["state"], "LEASE_EXPIRED")
        self.assertEqual(e.retry("request-digest"), 2)
        self.assertEqual(e.work_item_id, "work-1")
        with self.assertRaises(ProtocolError):
            e.expire_lease(lease1)

    def test_expired_attempt_can_enter_dlq_and_replay_with_same_work_identity(self):
        e = EDerivation("work-2", "request-digest")
        e.register_producer("d-registration:" + e.work_item_id)
        e.retry("request-digest")
        e.expire_lease(e.lease_id)
        self.assertEqual(e.move_to_dlq(), "DLQ")
        self.assertEqual(e.replay_dlq("request-digest"), 2)
        self.assertEqual(e.work_item_id, "work-2")

    def test_dlq_is_not_a_terminal_no_publication_proof(self):
        e = EDerivation("work-3", "request-digest")
        e.register_producer("d-registration:" + e.work_item_id)
        e.retry("request-digest")
        e.expire_lease(e.lease_id)
        e.move_to_dlq()
        self.assertIsNone(e.terminal_outcome)
        with self.assertRaises(ProtocolError):
            e.resolve("NO_PUBLICATION")

    def test_inflight_or_unknown_publication_cannot_spawn_new_attempt(self):
        for state in ("PRIVATE_STAGED", "STORAGE_PREPARED_HIDDEN", "D_ADMITTED", "UNKNOWN_IN_DOUBT"):
            e = EDerivation("work-4", "request-digest")
        e.register_producer("d-registration:" + e.work_item_id)
            e.retry("request-digest")
            e.state = state
            with self.assertRaises(ProtocolError, msg=state):
                e.retry("request-digest")

    def test_dlq_replay_with_changed_request_digest_is_rejected(self):
        e = EDerivation("work-5", "request-digest")
        e.register_producer("d-registration:" + e.work_item_id)
        e.retry("request-digest")
        e.expire_lease(e.lease_id)
        e.move_to_dlq()
        with self.assertRaises(ProtocolError):
            e.replay_dlq("changed-digest")


class GReconnectAndLineageObligationTests(unittest.TestCase):
    def test_reconnect_requires_current_snapshot_and_fragment_lineage(self):
        g = GContextVersion()
        g.materialize("fragment-1", ["memory-1", "memory-parent"], 3)
        self.assertTrue(g.validate_reconnect(1, {"memory-1", "memory-parent"}, 3))
        with self.assertRaises(ProtocolError):
            g.validate_reconnect(1, {"memory-1"}, 3)
        with self.assertRaises(ProtocolError):
            g.validate_reconnect(1, {"memory-1", "memory-parent"}, 4)

    def test_reconnect_rejects_stale_snapshot_after_context_version_change(self):
        g = GContextVersion()
        g.materialize("fragment-1", ["memory-1"], 3)
        g.apply_delta(1, "fragment-2", ["memory-2"], 3)
        with self.assertRaises(ProtocolError):
            g.validate_reconnect(1, {"memory-1", "memory-2"}, 3)
        self.assertTrue(g.validate_reconnect(2, {"memory-1", "memory-2"}, 3))

    def test_old_delivery_cannot_replay_after_context_version_changes(self):
        g = GContextVersion()
        g.materialize("fragment-1", ["memory-1"], 3)
        g.create_delivery("delivery-1", 1, 3)
        g.apply_delta(1, "fragment-2", ["memory-2"], 3)
        with self.assertRaises(ProtocolError):
            g.replay_delivery("delivery-1", 3)

    def test_forget_invalidates_reconnect_even_if_old_refs_are_present(self):
        g = GContextVersion()
        g.materialize("fragment-1", ["memory-1"], 3)
        g.forget({"memory-1"}, 4)
        with self.assertRaises(ProtocolError):
            g.validate_reconnect(g.version, {"memory-1"}, 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
