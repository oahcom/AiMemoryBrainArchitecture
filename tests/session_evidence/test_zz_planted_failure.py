import unittest


class PlantedFailure(unittest.TestCase):
    def test_planted_failure(self):
        self.fail("planted: the PR-head self-test must surface this and the trusted-base one must not")
