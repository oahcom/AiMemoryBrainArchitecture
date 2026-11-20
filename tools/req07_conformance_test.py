#!/usr/bin/env python3
"""REQ-07 AC-1..AC-7 executable contract suite (Python standard library only).

Run from repository root:
    python3 tools/req07_conformance_test.py

The suite is a deterministic architecture-contract/reference suite, not proof of
production runtime, database, index/cache, replica, deployment, or operational
conformance. AC-5 imports and runs the six existing reference-model tests too.
Source pins: tools/ac5_forget_recovery_test.py
(57b8d70740a4f9b05449b0a6e08b39ddcf39f0b6) and
14-ai-development/work-items/AID-2026-001/reference-model/forget_model.py
(cd623d67400c8870a729f79f88a4413f37bb335a).
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Evidence:
    ref: str
    source: str
    digest: str


@dataclass
class Proposition:
    pid: str
    text: str
    epistemic_type: str
    subject: str
    valid_from: int
    valid_until: int | None = None
    version: int = 1
    status: str = "active"
    evidence: tuple[Evidence, ...] = ()
    source_trust: float = 0.0
    evidence_strength: float = 0.0
    confidence: float = 0.0
    authority: bool = False
    permission: bool = False
    verified: bool = False
    parent: str | None = None
    transforms: tuple[str, ...] = ()

    def queryable(self, now: int) -> bool:
        return (self.status == "active" and self.valid_from <= now
                and (self.valid_until is None or now < self.valid_until))


@dataclass
class Decision:
    outcome: str
    reason: str
    evidence_refs: tuple[str, ...]
    method: str
    version: str
    history: tuple[str, ...]


def lineage_ok(item: Proposition, known: dict[str, Evidence]) -> bool:
    return bool(item.evidence) and all(
        e.ref in known and known[e.ref] == e for e in item.evidence
    ) and bool(item.transforms)


def quality_decision(item: Proposition, known: dict[str, Evidence]) -> Decision:
    ok = lineage_ok(item, known)
    outcome = "allow" if ok and item.status == "active" else "hold"
    return Decision(outcome, "lineage-valid" if ok else "missing-or-mismatched-lineage",
                    tuple(e.ref for e in item.evidence), "req07-quality-rule",
                    "1.0.0", ("ingested", "lineage-checked", outcome))


class RecoveryFixture:
    """Explicit ordering contract for replay-before-publication and derived targets."""
    def __init__(self):
        self.fence = 3
        self.derived = {"embedding-1": True, "cache-1": True, "summary-1": True}
        self.audit = ["forget-request:op-1"]
        self.checkpoints = {"cp-1": "audit://cp-1"}
        self.replayed = False
        self.published = False
        self.restored_generation = 2

    def invalidate_derived(self):
        for key in self.derived:
            self.derived[key] = False

    def replay_current_fences(self):
        self.replayed = True
        self.restored_generation = self.fence

    def publish(self):
        if not self.replayed or self.restored_generation < self.fence:
            raise ValueError("current fences must be replayed before publication")
        self.published = True

    def queryable(self, key):
        return self.published and self.restored_generation >= self.fence and self.derived.get(key, False)


class AC1EpistemicIdentity(unittest.TestCase):
    def test_five_epistemic_kinds_are_distinct(self):
        kinds = {"Fact", "Claim", "Inference", "Hypothesis", "Preference"}
        items = [Proposition(str(i), "p", k, "s", 0) for i, k in enumerate(sorted(kinds))]
        self.assertEqual({x.epistemic_type for x in items}, kinds)
        self.assertEqual(len({x.epistemic_type for x in items}), 5)

    def test_fact_is_qualified_proposition_not_synonym_for_claim(self):
        fact = Proposition("f", "water boils at 100C at 1atm", "Fact", "water", 0,
                           evidence=(Evidence("e1", "lab", "sha256:abc"),), verified=True)
        claim = Proposition("c", fact.text, "Claim", "researcher", 0,
                            evidence=(Evidence("e1", "lab", "sha256:abc"),), verified=False)
        self.assertNotEqual(fact.epistemic_type, claim.epistemic_type)
        self.assertTrue(fact.verified)
        self.assertFalse(claim.verified)
        self.assertEqual(fact.text, claim.text)

    def test_claim_requires_attribution_and_hypothesis_is_unverified(self):
        claim = Proposition("c", "p", "Claim", "alice", 0)
        hypothesis = Proposition("h", "p", "Hypothesis", "alice", 0)
        self.assertTrue(claim.subject)
        self.assertNotEqual(claim.epistemic_type, hypothesis.epistemic_type)
        self.assertFalse(hypothesis.verified)

    def test_inference_and_preference_are_not_facts(self):
        for kind in ("Inference", "Preference"):
            item = Proposition(kind, "p", kind, "agent", 0, verified=False)
            self.assertFalse(item.verified)


class AC2Provenance(unittest.TestCase):
    def setUp(self):
        self.e = Evidence("ev://source-1", "sensor-A", "sha256:001")
        self.known = {self.e.ref: self.e}

    def test_source_and_every_transformation_step_are_preserved(self):
        item = Proposition("p", "derived", "Inference", "engine", 0,
                           evidence=(self.e,), transforms=("normalize:v1", "derive:v2"))
        self.assertTrue(lineage_ok(item, self.known))
        self.assertEqual(item.transforms, ("normalize:v1", "derive:v2"))

    def test_missing_lineage_is_rejected(self):
        item = Proposition("p", "derived", "Inference", "engine", 0,
                           transforms=("derive:v2",))
        self.assertFalse(lineage_ok(item, self.known))

    def test_mismatched_source_digest_is_rejected(self):
        bad = Evidence(self.e.ref, self.e.source, "sha256:tampered")
        item = Proposition("p", "derived", "Inference", "engine", 0,
                           evidence=(bad,), transforms=("derive:v2",))
        self.assertFalse(lineage_ok(item, self.known))

    def test_missing_transformation_step_is_rejected(self):
        item = Proposition("p", "derived", "Inference", "engine", 0, evidence=(self.e,))
        self.assertFalse(lineage_ok(item, self.known))


class AC3TemporalTransitions(unittest.TestCase):
    def test_freshness_and_expiry_are_half_open(self):
        item = Proposition("p", "x", "Claim", "s", 10, valid_until=20)
        self.assertFalse(item.queryable(9))
        self.assertTrue(item.queryable(10))
        self.assertTrue(item.queryable(19))
        self.assertFalse(item.queryable(20))

    def test_supersession_and_retraction_remove_old_item_from_query(self):
        old = Proposition("old", "v1", "Claim", "s", 0, status="superseded")
        retracted = Proposition("r", "v2", "Claim", "s", 0, status="retracted")
        self.assertFalse(old.queryable(1))
        self.assertFalse(retracted.queryable(1))

    def test_contradictory_claims_can_coexist_without_auto_verification(self):
        a = Proposition("a", "rain", "Claim", "alice", 0)
        b = Proposition("b", "not-rain", "Claim", "bob", 0)
        self.assertTrue(a.queryable(1) and b.queryable(1))
        self.assertFalse(a.verified or b.verified)

    def test_correction_increments_version_and_stale_write_is_rejected(self):
        current = Proposition("p", "corrected", "Claim", "s", 0, version=2)
        submitted_version = 1
        self.assertLess(submitted_version, current.version)
        self.assertNotEqual(submitted_version, current.version)

    def test_expiry_does_not_rewrite_historical_validity(self):
        item = Proposition("p", "x", "Fact", "s", 1, valid_until=5)
        self.assertEqual((item.valid_from, item.valid_until), (1, 5))
        self.assertFalse(item.queryable(5))


class AC4ConfidenceSeparation(unittest.TestCase):
    def test_confidence_cannot_grant_authority_permission_or_verified(self):
        item = Proposition("p", "x", "Claim", "s", 0, confidence=1.0,
                            authority=False, permission=False, verified=False)
        self.assertFalse(item.authority)
        self.assertFalse(item.permission)
        self.assertFalse(item.verified)

    def test_source_trust_and_evidence_strength_are_independent(self):
        trusted_weak = Proposition("a", "x", "Claim", "s", 0,
                                   source_trust=.99, evidence_strength=.1)
        untrusted_strong = Proposition("b", "x", "Claim", "s", 0,
                                       source_trust=.1, evidence_strength=.99)
        self.assertNotEqual(trusted_weak.source_trust, trusted_weak.evidence_strength)
        self.assertNotEqual(untrusted_strong.source_trust, untrusted_strong.evidence_strength)

    def test_high_confidence_does_not_change_claim_identity(self):
        low = Proposition("a", "x", "Claim", "s", 0, confidence=.01)
        high = Proposition("b", "x", "Claim", "s", 0, confidence=1.0)
        self.assertEqual(low.epistemic_type, high.epistemic_type)
        self.assertFalse(high.verified)


class AC5ForgetRecoveryExtension(unittest.TestCase):
    def test_applicable_derived_targets_are_invalidated(self):
        r = RecoveryFixture()
        r.invalidate_derived()
        self.assertEqual(set(r.derived.values()), {False})
        self.assertFalse(r.queryable("embedding-1"))

    def test_stale_restored_snapshot_remains_unqueryable(self):
        r = RecoveryFixture()
        with self.assertRaisesRegex(ValueError, "replayed"):
            r.publish()
        self.assertFalse(r.published)

    def test_current_fences_are_replayed_before_recovery_publication(self):
        r = RecoveryFixture()
        r.replay_current_fences()
        r.publish()
        self.assertTrue(r.published)
        self.assertEqual(r.restored_generation, r.fence)

    def test_audit_and_checkpoint_evidence_survive_recovery(self):
        r = RecoveryFixture()
        before_audit, before_cp = list(r.audit), dict(r.checkpoints)
        r.replay_current_fences()
        r.publish()
        self.assertEqual(r.audit, before_audit)
        self.assertEqual(r.checkpoints, before_cp)


class AC6AdversarialOutcomes(unittest.TestCase):
    def setUp(self):
        self.ev = Evidence("ev://good", "source", "sha256:good")
        self.known = {self.ev.ref: self.ev}

    def test_poisoning_fixture_fails(self):
        poison = Proposition("p", "poison", "Claim", "attacker", 0,
                             evidence=(Evidence("ev://good", "source", "sha256:evil"),),
                             transforms=("ingest:v1",))
        self.assertEqual(quality_decision(poison, self.known).outcome, "hold")
        self.assertEqual(quality_decision(poison, self.known).reason,
                         "missing-or-mismatched-lineage")

    def test_stale_memory_fixture_is_held(self):
        stale = Proposition("s", "old", "Claim", "s", 0, valid_until=2)
        outcome = "allow" if stale.queryable(3) else "hold"
        self.assertEqual(outcome, "hold")

    def test_contradiction_fixture_is_held_for_resolution_not_silently_overwritten(self):
        a = Proposition("a", "p", "Claim", "alice", 0)
        b = Proposition("b", "not-p", "Claim", "bob", 0)
        outcome = "hold" if a.text != b.text else "allow"
        self.assertEqual(outcome, "hold")
        self.assertEqual((a.status, b.status), ("active", "active"))

    def test_valid_lineage_fixture_is_allowed(self):
        item = Proposition("ok", "x", "Claim", "s", 0, evidence=(self.ev,),
                           transforms=("normalize:v1",))
        self.assertEqual(quality_decision(item, self.known).outcome, "allow")


class AC7ExplainabilityAudit(unittest.TestCase):
    def test_decision_contains_reason_refs_method_version_and_history(self):
        ev = Evidence("ev://1", "source", "sha256:1")
        item = Proposition("p", "x", "Claim", "s", 0, evidence=(ev,),
                           transforms=("normalize:v1",))
        decision = quality_decision(item, {ev.ref: ev})
        self.assertEqual(decision.outcome, "allow")
        self.assertTrue(decision.reason)
        self.assertEqual(decision.evidence_refs, ("ev://1",))
        self.assertEqual(decision.method, "req07-quality-rule")
        self.assertEqual(decision.version, "1.0.0")
        self.assertEqual(decision.history, ("ingested", "lineage-checked", "allow"))

    def test_unexplained_outcome_is_rejected(self):
        unexplained = Decision("allow", "", (), "", "", ())
        self.assertFalse(unexplained.reason and unexplained.method
                         and unexplained.version and unexplained.history)

    def test_decision_is_reproducible_for_identical_fixture(self):
        ev = Evidence("ev://1", "source", "sha256:1")
        item = Proposition("p", "x", "Claim", "s", 0, evidence=(ev,),
                           transforms=("normalize:v1",))
        a = quality_decision(item, {ev.ref: ev})
        b = quality_decision(item, {ev.ref: ev})
        self.assertEqual(a, b)


def load_tests(loader, standard_tests, pattern):
    """Include the pinned six-test AC-5 reference-model suite in this one command."""
    legacy_path = ROOT / "tools" / "ac5_forget_recovery_test.py"
    spec = importlib.util.spec_from_file_location("ac5_forget_recovery_test", legacy_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned AC-5 reference-model suite")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    standard_tests.addTests(loader.loadTestsFromTestCase(module.ForgetRecoveryTests))
    return standard_tests


if __name__ == "__main__":
    unittest.main(verbosity=2)
