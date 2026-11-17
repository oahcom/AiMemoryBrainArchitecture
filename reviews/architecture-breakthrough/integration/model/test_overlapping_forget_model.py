import unittest

from overlapping_forget_model import (
    EXPECTED_COUNTEREXAMPLES,
    State,
    apply_actions,
    bfs,
    run_checks,
)


class OverlappingForgetModelTests(unittest.TestCase):
    def test_safe_graph_has_no_counterexample(self):
        trace, violations, _, count = bfs(None, 12)
        self.assertIsNone(trace)
        self.assertIsNone(violations)
        self.assertEqual(count, 2425)

    def test_all_mutants_have_expected_shortest_counterexample(self):
        for mutant, expected in EXPECTED_COUNTEREXAMPLES.items():
            with self.subTest(mutant=mutant):
                trace, violations, _, _ = bfs(mutant, 12)
                self.assertEqual(trace, expected)
                self.assertTrue(violations)

    def test_both_installation_orders_allocate_distinct_generations(self):
        a = apply_actions(State(), "install_op1", "install_op2")
        b = apply_actions(State(), "install_op2", "install_op1")
        self.assertNotEqual(a.op1_generation, a.op2_generation)
        self.assertNotEqual(b.op1_generation, b.op2_generation)

    def test_closing_one_operation_does_not_close_the_other(self):
        state = apply_actions(
            State(), "install_op1", "install_op2",
            "terminalize_op1_a", "terminalize_op1_shared", "close_op1", "receipt_op1"
        )
        self.assertTrue(state.op1_barrier_closed)
        self.assertFalse(state.op2_barrier_closed)

    def test_shared_target_evidence_is_operation_scoped(self):
        state = apply_actions(State(), "install_op1", "install_op2", "terminalize_op2_shared")
        self.assertNotIn(("shared", "op1", "op1"), state.op1_terminal_evidence)
        self.assertIn(("shared", "op2", "op2"), state.op2_terminal_evidence)

    def test_late_target_reopens_only_affected_operation(self):
        state = apply_actions(
            State(), "install_op1", "install_op2",
            "terminalize_op1_a", "terminalize_op1_shared", "close_op1", "receipt_op1",
            "terminalize_op2_shared", "terminalize_op2_b", "close_op2", "receipt_op2",
            "discover_late_op1"
        )
        self.assertFalse(state.op1_barrier_closed)
        self.assertLess(state.op1_receipt_generation, state.op1_generation)
        self.assertTrue(state.op2_barrier_closed)
        self.assertEqual(state.op2_receipt_generation, state.op2_generation)

    def test_run_all_assertions(self):
        run_checks()


if __name__ == "__main__":
    unittest.main()
