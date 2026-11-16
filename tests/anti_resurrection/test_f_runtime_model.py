"""Deterministic anti-resurrection tests for the F runtime logical reference model."""
import unittest

from f_runtime_model import Blocked, Conflict, RuntimeEntry, RuntimeModel


class RuntimeAntiResurrectionTests(unittest.TestCase):
    def setUp(self):
        self.f = RuntimeModel()
        self.good = RuntimeEntry("mem-1", "scope-A", "env-A", "pd-A", 7, 0, "v1", score=0.9)
        self.other = RuntimeEntry("mem-2", "scope-B", "env-A", "pd-A", 7, 0, "v1", score=0.99)
        self.env_other = RuntimeEntry("mem-3", "scope-A", "env-B", "pd-A", 7, 0, "v1", score=0.98)
        self.f.index.entries = [self.good, self.other, self.env_other]

    def test_stale_index_candidate_suppressed_after_forget(self):
        self.f.apply_forget("forget-1", "d1", ["mem-1"])
        self.assertEqual(self.f.retrieve(), [])
        self.assertEqual(self.f.last_exposed_count, 0)

    def test_stale_cache_hit_is_evicted_not_served(self):
        key = self.f.cache_key(self.good)
        self.f.cache[key] = self.good
        self.f.apply_forget("forget-1", "d1", ["mem-1"])
        self.assertIsNone(self.f.cache_get(key))
        self.assertEqual(self.f.stale_evictions, 1)

    def test_inflight_fill_racing_forget_cannot_publish(self):
        self.f.start_fill("fill-1", self.good)
        self.f.apply_forget("forget-1", "d1", ["mem-1"])
        self.assertFalse(self.f.complete_fill("fill-1"))
        self.assertEqual(self.f.cache, {})

    def test_pre_forget_snapshot_rebuild_does_not_resurrect(self):
        self.f.apply_forget("forget-1", "d1", ["mem-1"])
        self.f.rebuild([self.good], contiguous_replay=True, watermark=100, generation=2)
        self.assertEqual(self.f.retrieve(), [])

    def test_targeted_forget_does_not_expose_affected_entry_or_suppress_unrelated_index_entry(self):
        unrelated = RuntimeEntry("mem-4", "scope-A", "env-A", "pd-A", 7, 0, "v1")
        self.f.index.entries = [self.good, unrelated]
        self.f.apply_forget("forget-1", "d1", ["mem-1"])
        self.assertEqual([x.memory_ref for x in self.f.retrieve()], ["mem-4"])

    def test_global_fence_generation_change_invalidates_old_cache_key(self):
        unrelated = RuntimeEntry("mem-4", "scope-A", "env-A", "pd-A", 7, 0, "v1")
        key = self.f.cache_key(unrelated)
        self.f.cache[key] = unrelated
        self.f.apply_forget("forget-1", "d1", ["mem-1"])
        self.assertIsNone(self.f.cache_get(key))
        self.assertEqual(self.f.stale_evictions, 1)

    def test_watermark_gap_blocks_retrieval(self):
        self.f.index.complete = False
        with self.assertRaises(Blocked):
            self.f.retrieve()

    def test_authority_unavailable_blocks_retrieval_and_cache(self):
        self.f.cache[self.f.cache_key(self.good)] = self.good
        self.f.authorities_available = False
        with self.assertRaises(Blocked):
            self.f.retrieve()
        with self.assertRaises(Blocked):
            self.f.cache_get(self.f.cache_key(self.good))

    def test_scope_filter_precedes_count_and_ranking(self):
        result = self.f.retrieve()
        self.assertEqual([x.memory_ref for x in result], ["mem-1"])
        self.assertEqual(self.f.last_exposed_count, 1)

    def test_environment_filter_precedes_count_and_ranking(self):
        result = self.f.retrieve()
        self.assertNotIn("mem-3", [x.memory_ref for x in result])
        self.assertEqual(self.f.last_exposed_count, 1)

    def test_stale_permission_epoch_blocks_old_entry(self):
        self.f.revoke("pd-A", 8)
        self.assertEqual(self.f.retrieve(), [])

    def test_reconnect_invalidates_old_working_set_before_restore(self):
        self.f.working_set = [self.good]
        self.f.apply_forget("forget-1", "d1", ["mem-1"])
        with self.assertRaises(Blocked):
            self.f.reconnect([self.good], fresh_i_state=True, fresh_d_state=True, checkpoint_reconciled=False)
        self.assertEqual(self.f.working_set, [])

    def test_reconnect_requires_fresh_i_and_d_authority(self):
        self.f.working_set = [self.good]
        with self.assertRaises(Blocked):
            self.f.reconnect([self.good], fresh_i_state=False, fresh_d_state=True, checkpoint_reconciled=True)
        self.assertEqual(self.f.working_set, [])

    def test_duplicate_invalidation_same_digest_is_idempotent(self):
        self.assertEqual(self.f.apply_forget("forget-1", "d1", ["mem-1"]), "APPLIED")
        generation = self.f.fence_generation
        self.assertEqual(self.f.apply_forget("forget-1", "d1", ["mem-1"]), "IDEMPOTENT_REPLAY")
        self.assertEqual(self.f.fence_generation, generation)

    def test_changed_digest_for_same_invalidation_identity_conflicts(self):
        self.f.apply_forget("forget-1", "d1", ["mem-1"])
        with self.assertRaises(Conflict):
            self.f.apply_forget("forget-1", "different", ["mem-2"])

    def test_cache_key_binds_security_and_version_dimensions(self):
        base = self.f.cache_key(self.good)
        changed_scope = RuntimeEntry("mem-1", "scope-B", "env-A", "pd-A", 7, 0, "v1")
        changed_env = RuntimeEntry("mem-1", "scope-A", "env-B", "pd-A", 7, 0, "v1")
        changed_epoch = RuntimeEntry("mem-1", "scope-A", "env-A", "pd-A", 8, 0, "v1")
        changed_version = RuntimeEntry("mem-1", "scope-A", "env-A", "pd-A", 7, 0, "v2")
        self.assertNotEqual(base, self.f.cache_key(changed_scope))
        self.assertNotEqual(base, self.f.cache_key(changed_env))
        self.assertNotEqual(base, self.f.cache_key(changed_epoch))
        self.assertNotEqual(base, self.f.cache_key(changed_version))

    def test_stale_entry_is_distinct_from_cache_miss(self):
        key = self.f.cache_key(self.good)
        self.f.cache[key] = self.good
        self.f.apply_forget("forget-1", "d1", ["mem-1"])
        self.assertIsNone(self.f.cache_get(key))
        self.assertEqual(self.f.stale_evictions, 1)
        self.assertIsNone(self.f.cache_get(("missing",)))
        self.assertEqual(self.f.stale_evictions, 1)

    def test_f_target_evidence_cannot_claim_global_completion(self):
        self.f.apply_forget("forget-1", "d1", ["mem-1"])
        evidence = self.f.report_target_evidence("target-F-1")
        self.assertEqual(evidence["owner"], "F")
        self.assertEqual(evidence["global_completion"], "NOT_AUTHORIZED")

    def test_index_rebuild_requires_contiguous_replay(self):
        with self.assertRaises(Blocked):
            self.f.rebuild([self.good], contiguous_replay=False, watermark=100, generation=2)


if __name__ == "__main__":
    unittest.main()