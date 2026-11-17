import unittest

from forget_cross_owner_model import (
    EXPECTED_COUNTEREXAMPLES,
    State,
    apply_actions,
    bfs,
    run_checks,
    step,
)


class ForgetCrossOwnerModelTests(unittest.TestCase):
    def test_safe_graph_has_no_counterexample(self):
        trace, violations, _, count = bfs(None, 14)
        self.assertIsNone(trace)
        self.assertIsNone(violations)
        self.assertEqual(count, 27472)

    def test_all_mutants_have_expected_shortest_counterexample(self):
        for mutant, expected in EXPECTED_COUNTEREXAMPLES.items():
            with self.subTest(mutant=mutant):
                trace, violations, _, _ = bfs(mutant, 14)
                self.assertEqual(trace, expected)
                self.assertTrue(violations)

    def test_stale_cache_bytes_without_stale_read_are_not_disclosure(self):
        trace, violations, _, _ = bfs("stale_cache", 14)
        self.assertIsNone(trace)
        self.assertIsNone(violations)

    def test_i_commit_wins_before_revocation(self):
        state = apply_actions(
            State(), "register", "run", "stage", "register_dependencies",
            "i_commit", "revoke"
        )
        self.assertTrue(state.i_participant_open)
        self.assertTrue(state.revocation_pending)
        self.assertFalse(state.revoked)
        state = apply_actions(state, "publish")
        self.assertTrue(state.visible)
        self.assertTrue(state.revoked)
        self.assertFalse(state.i_participant_open)

    def test_revocation_wins_before_i_commit(self):
        state = apply_actions(
            State(), "register", "run", "stage", "register_dependencies", "revoke"
        )
        self.assertEqual(state.i_decision, "REVOCATION_WON")
        self.assertIsNone(step(state, "i_commit"))
        self.assertIsNone(step(state, "publish"))

    def test_fence_wins_before_visibility(self):
        state = apply_actions(
            State(), "register", "run", "stage", "register_dependencies",
            "i_commit", "install_fence"
        )
        self.assertIsNone(step(state, "publish"))
        state = apply_actions(
            state, "resolve_no_publication", "expire_lease", "terminalize", "close_barrier"
        )
        self.assertTrue(state.barrier_closed)

    def test_publication_wins_before_fence_requires_suppression(self):
        state = apply_actions(
            State(), "register", "run", "stage", "register_dependencies",
            "i_commit", "publish", "install_fence"
        )
        self.assertIsNone(step(state, "terminalize"))
        state = apply_actions(state, "suppress", "terminalize", "close_barrier")
        self.assertTrue(state.barrier_closed)

    def test_unknown_i_participant_holds_barrier(self):
        state = apply_actions(
            State(), "register", "run", "stage", "register_dependencies",
            "i_unknown", "install_fence"
        )
        self.assertIsNone(step(state, "close_barrier"))
        state = apply_actions(
            state, "resolve_no_publication", "expire_lease", "terminalize", "close_barrier"
        )
        self.assertTrue(state.barrier_closed)

    def test_lost_ack_does_not_rollback_receipt(self):
        state = apply_actions(State(), "install_fence", "close_barrier", "persist_receipt", "lose_ack")
        self.assertTrue(state.receipt_durable)
        self.assertFalse(state.ack_observed)
        state = apply_actions(state, "retry_forget")
        self.assertTrue(state.receipt_durable)
        self.assertTrue(state.ack_observed)

    def test_inventory_gap_reopens_barrier(self):
        state = apply_actions(State(), "install_fence", "close_barrier")
        state = apply_actions(state, "inventory_gap")
        self.assertFalse(state.barrier_closed)
        self.assertFalse(state.global_complete)

    def test_restore_releases_only_after_current_fence_highwater_replay(self):
        state = apply_actions(State(), "install_fence", "restore_backup", "replay_fence_highwater", "reconcile_restore")
        self.assertTrue(state.restore_released)
        self.assertEqual(state.restored_at_release, state.durable_at_release)

    def test_restore_does_not_release_with_stale_fence_highwater(self):
        state = apply_actions(State(), "install_fence", "restore_backup")
        state = step(state, "reconcile_restore")
        self.assertFalse(state.restore_released)

    def test_run_all_assertions(self):
        run_checks()


if __name__ == "__main__":
    unittest.main()
