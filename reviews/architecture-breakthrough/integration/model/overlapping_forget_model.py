#!/usr/bin/env python3
"""Bounded two-operation Forget overlap model. Python standard library only.

Run:
  python3 overlapping_forget_model.py
"""
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    durable_generation: int = 0
    op1_installed: bool = False
    op1_generation: int = 0
    op1_targets: frozenset = frozenset()
    # (target, source_operation, claimed_operation)
    op1_terminal_evidence: frozenset = frozenset()
    op1_barrier_closed: bool = False
    op1_receipt_generation: int = 0

    op2_installed: bool = False
    op2_generation: int = 0
    op2_targets: frozenset = frozenset()
    op2_terminal_evidence: frozenset = frozenset()
    op2_barrier_closed: bool = False
    op2_receipt_generation: int = 0


ACTIONS = (
    "install_op1", "install_op2",
    "terminalize_op1_a", "terminalize_op1_shared",
    "terminalize_op2_shared", "terminalize_op2_b",
    "close_op1", "close_op2", "receipt_op1", "receipt_op2",
    "discover_late_op1", "discover_late_op2",
)

EXPECTED_COUNTEREXAMPLES = {
    "overwrite_generation": ["install_op1", "install_op2"],
    "close_other_barrier": [
        "install_op1", "install_op2", "terminalize_op1_a",
        "terminalize_op1_shared", "close_op1",
    ],
    "cross_op_shared_evidence": [
        "install_op1", "install_op2", "terminalize_op2_shared",
    ],
    "late_target_no_reopen": [
        "install_op1", "terminalize_op1_a", "terminalize_op1_shared",
        "close_op1", "discover_late_op1",
    ],
    "receipt_closes_other_barrier": [
        "install_op1", "install_op2", "terminalize_op1_a",
        "terminalize_op1_shared", "close_op1", "receipt_op1",
    ],
}


def step(s: State, action: str, mutant: str | None = None):
    d = dict(s.__dict__)

    if action == "install_op1":
        if s.op1_installed:
            return None
        generation = s.durable_generation + 1
        d.update(
            durable_generation=generation,
            op1_installed=True,
            op1_generation=generation,
            op1_targets=frozenset({"a", "shared"}),
            op1_terminal_evidence=frozenset(),
        )

    elif action == "install_op2":
        if s.op2_installed:
            return None
        generation = s.durable_generation + 1
        if mutant == "overwrite_generation" and s.op1_installed:
            generation = s.op1_generation
        d.update(
            durable_generation=max(s.durable_generation, generation),
            op2_installed=True,
            op2_generation=generation,
            op2_targets=frozenset({"shared", "b"}),
            op2_terminal_evidence=frozenset(),
        )

    elif action == "terminalize_op1_a":
        if not s.op1_installed:
            return None
        d.update(op1_terminal_evidence=s.op1_terminal_evidence | {("a", "op1", "op1")})

    elif action == "terminalize_op1_shared":
        if not s.op1_installed:
            return None
        d.update(op1_terminal_evidence=s.op1_terminal_evidence | {("shared", "op1", "op1")})

    elif action == "terminalize_op2_shared":
        if not s.op2_installed:
            return None
        d.update(op2_terminal_evidence=s.op2_terminal_evidence | {("shared", "op2", "op2")})
        if mutant == "cross_op_shared_evidence" and s.op1_installed:
            d.update(op1_terminal_evidence=s.op1_terminal_evidence | {("shared", "op2", "op1")})

    elif action == "terminalize_op2_b":
        if not s.op2_installed:
            return None
        d.update(op2_terminal_evidence=s.op2_terminal_evidence | {("b", "op2", "op2")})

    elif action == "close_op1":
        if not s.op1_installed or s.op1_barrier_closed:
            return None
        complete = all((target, "op1", "op1") in s.op1_terminal_evidence for target in s.op1_targets)
        if not complete:
            return None
        d.update(op1_barrier_closed=True)
        if mutant == "close_other_barrier" and s.op2_installed:
            d.update(op2_barrier_closed=True)

    elif action == "close_op2":
        if not s.op2_installed or s.op2_barrier_closed:
            return None
        complete = all((target, "op2", "op2") in s.op2_terminal_evidence for target in s.op2_targets)
        if not complete:
            return None
        d.update(op2_barrier_closed=True)

    elif action == "receipt_op1":
        if not s.op1_barrier_closed:
            return None
        d.update(op1_receipt_generation=s.op1_generation)
        if mutant == "receipt_closes_other_barrier" and s.op2_installed:
            d.update(op2_barrier_closed=True)

    elif action == "receipt_op2":
        if not s.op2_barrier_closed:
            return None
        d.update(op2_receipt_generation=s.op2_generation)

    elif action == "discover_late_op1":
        if not s.op1_installed or "late" in s.op1_targets:
            return None
        generation = s.durable_generation + 1
        d.update(
            durable_generation=generation,
            op1_generation=generation,
            op1_targets=s.op1_targets | {"late"},
            op1_barrier_closed=(s.op1_barrier_closed if mutant == "late_target_no_reopen" else False),
        )

    elif action == "discover_late_op2":
        if not s.op2_installed or "late" in s.op2_targets:
            return None
        generation = s.durable_generation + 1
        d.update(
            durable_generation=generation,
            op2_generation=generation,
            op2_targets=s.op2_targets | {"late"},
            op2_barrier_closed=(s.op2_barrier_closed if mutant == "late_target_no_reopen" else False),
        )

    else:
        raise ValueError(action)

    return State(**d)


def invariant_violations(s: State):
    bad = []
    if s.op1_installed and s.op1_generation > s.durable_generation:
        bad.append("op1-generation-ahead-of-durable")
    if s.op2_installed and s.op2_generation > s.durable_generation:
        bad.append("op2-generation-ahead-of-durable")
    if s.op1_installed and s.op2_installed and s.op1_generation == s.op2_generation:
        bad.append("duplicate-operation-generation")
    if s.op1_barrier_closed and not all(
        (target, "op1", "op1") in s.op1_terminal_evidence for target in s.op1_targets
    ):
        bad.append("op1-premature-close")
    if s.op2_barrier_closed and not all(
        (target, "op2", "op2") in s.op2_terminal_evidence for target in s.op2_targets
    ):
        bad.append("op2-premature-close")
    if any(
        source_operation != claimed_operation
        for _, source_operation, claimed_operation
        in s.op1_terminal_evidence | s.op2_terminal_evidence
    ):
        bad.append("cross-operation-evidence-reuse")
    if (s.op1_receipt_generation == s.op1_generation and s.op1_receipt_generation > 0
            and not s.op1_barrier_closed):
        bad.append("op1-current-receipt-without-closed-barrier")
    if (s.op2_receipt_generation == s.op2_generation and s.op2_receipt_generation > 0
            and not s.op2_barrier_closed):
        bad.append("op2-current-receipt-without-closed-barrier")
    return bad


def bfs(mutant=None, max_depth=12):
    queue = deque([(State(), [])])
    seen = {(State(), 0)}
    while queue:
        state, trace = queue.popleft()
        violations = invariant_violations(state)
        if violations:
            return trace, violations, state, len(seen)
        if len(trace) >= max_depth:
            continue
        for action in ACTIONS:
            nxt = step(state, action, mutant)
            if nxt is None:
                continue
            key = (nxt, len(trace) + 1)
            if key not in seen:
                seen.add(key)
                queue.append((nxt, trace + [action]))
    return None, None, None, len(seen)


def apply_actions(state, *actions):
    for action in actions:
        state = step(state, action)
        if state is None:
            raise AssertionError(f"illegal safe transition: {action}")
    return state


def run_checks():
    trace, violations, _, count = bfs(None, 12)
    assert trace is None and violations is None
    assert count == 2425, count

    for mutant, expected in EXPECTED_COUNTEREXAMPLES.items():
        trace, violations, _, _ = bfs(mutant, 12)
        assert trace == expected, (mutant, trace, expected)
        assert violations, mutant

    # Both installation orders produce distinct generations.
    op1_then_op2 = apply_actions(State(), "install_op1", "install_op2")
    op2_then_op1 = apply_actions(State(), "install_op2", "install_op1")
    assert op1_then_op2.op1_generation != op1_then_op2.op2_generation
    assert op2_then_op1.op1_generation != op2_then_op1.op2_generation

    # Closing one operation does not close the other, even with a shared target.
    state = apply_actions(
        State(), "install_op1", "install_op2",
        "terminalize_op1_a", "terminalize_op1_shared", "close_op1", "receipt_op1"
    )
    assert state.op1_barrier_closed and not state.op2_barrier_closed
    assert state.op1_generation == 1 and state.op2_generation == 2

    # Shared-target terminal evidence is operation-scoped.
    state = apply_actions(state, "terminalize_op2_shared", "terminalize_op2_b", "close_op2", "receipt_op2")
    assert state.op2_barrier_closed and state.op2_receipt_generation == 2

    # Late target discovery reopens only the affected operation; old receipt is stale.
    state = apply_actions(state, "discover_late_op1")
    assert not state.op1_barrier_closed
    assert state.op1_receipt_generation < state.op1_generation
    assert state.op2_barrier_closed and state.op2_receipt_generation == state.op2_generation

    print(f"SAFE TWO-OP MODEL: no invariant violation through depth 12 ({count} state/depth pairs)")
    for mutant, expected in EXPECTED_COUNTEREXAMPLES.items():
        print(f"COUNTEREXAMPLE {mutant}: {' -> '.join(expected)}")
    print("ORDER PERMUTATIONS / SHARED TARGET / LATE DISCOVERY: PASS")
    print("TWO-OP MODEL CHECK COMPLETE (bounded abstraction only)")


if __name__ == "__main__":
    run_checks()
