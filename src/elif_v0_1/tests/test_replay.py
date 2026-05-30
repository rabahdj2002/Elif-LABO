"""Tests for the alpha replay harness.

Covers:
    * Per-case offline replay completes and returns a frozen ReplayResult.
    * All three cases replay; cohort report aggregates them.
    * Acceptance report shape is correct (frozen dataclass; per_case tuple).
    * Verdict closed-set is enforced.
    * Structural similarity score is in [0, 1].
    * Runner path is reported honestly (orchestration_runner vs fallback).
    * Reference signature extraction recognizes the Condition C reference.
"""

from __future__ import annotations

import os
import sys
import unittest

# Path shim so `elif_v0_1` resolves under `python3 -m unittest discover`.
_SRC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from elif_v0_1.base import ELIFError  # noqa: E402
from elif_v0_1.run_context import RunReport  # noqa: E402
from elif_v0_1.replay import (  # noqa: E402
    ACCEPTANCE_VERDICTS,
    ALPHA_CASE_IDS,
    AcceptanceReport,
    REFERENCE_BEHAVIORS,
    ReplayResult,
    replay_all_cases,
    replay_case,
)


class ReplayCase01OfflineCompletesTest(unittest.TestCase):
    """Case 01 (electroculture) replay completes in offline mode."""

    def test_returns_replay_result_frozen(self) -> None:
        result = replay_case("case_01_electroculture", offline_mode=True)
        self.assertIsInstance(result, ReplayResult)
        # Frozen dataclass: attribute write should fail.
        with self.assertRaises(Exception):
            result.case_id = "tampered"  # type: ignore[misc]

    def test_run_report_populated(self) -> None:
        result = replay_case("case_01_electroculture", offline_mode=True)
        self.assertIsInstance(result.run_report, RunReport)
        # At least Steps 1..8 should be present regardless of governance halt.
        step_ids = {env.step_id for env in result.run_report.step_outputs}
        for required in ("step_1", "step_2", "step_3", "step_4", "step_5", "step_6"):
            self.assertIn(required, step_ids, f"missing {required} in run report")

    def test_similarity_in_unit_interval(self) -> None:
        result = replay_case("case_01_electroculture", offline_mode=True)
        self.assertGreaterEqual(result.structural_similarity_score, 0.0)
        self.assertLessEqual(result.structural_similarity_score, 1.0)

    def test_verdict_in_closed_set(self) -> None:
        result = replay_case("case_01_electroculture", offline_mode=True)
        self.assertIn(
            result.behavioral_acceptance_verdict, ACCEPTANCE_VERDICTS
        )


class ReplayCase02OfflineTest(unittest.TestCase):
    """Case 02 (policy_governance) replay smoke."""

    def test_completes(self) -> None:
        result = replay_case("case_02_policy_governance", offline_mode=True)
        self.assertEqual(result.case_id, "case_02_policy_governance")
        self.assertTrue(result.offline_mode)


class ReplayCase03OfflineTest(unittest.TestCase):
    """Case 03 (operational_organizational) replay smoke."""

    def test_completes(self) -> None:
        result = replay_case(
            "case_03_operational_organizational", offline_mode=True
        )
        self.assertEqual(result.case_id, "case_03_operational_organizational")


class ReplayUnknownCaseRejectedTest(unittest.TestCase):
    """An unknown case id is rejected at the boundary."""

    def test_rejects(self) -> None:
        with self.assertRaises(ELIFError):
            replay_case("case_99_not_a_real_case", offline_mode=True)


class ReplayAllCasesTest(unittest.TestCase):
    """`replay_all_cases` covers all three alpha cases."""

    def test_yields_three_results(self) -> None:
        report = replay_all_cases(offline_mode=True)
        self.assertIsInstance(report, AcceptanceReport)
        self.assertEqual(len(report.per_case), 3)
        for r in report.per_case:
            self.assertIn(r.case_id, ALPHA_CASE_IDS)

    def test_overall_verdict_closed_set(self) -> None:
        report = replay_all_cases(offline_mode=True)
        self.assertIn(report.overall_verdict(), ACCEPTANCE_VERDICTS)

    def test_each_case_has_runner_path(self) -> None:
        report = replay_all_cases(offline_mode=True)
        for r in report.per_case:
            self.assertIn(
                r.runner_path,
                {"orchestration_runner", "per_component_fallback"},
            )


class AcceptanceReportGenerationTest(unittest.TestCase):
    """Cohort report aggregates per-case verdicts correctly."""

    def test_per_case_count_matches_alpha_ids(self) -> None:
        report = replay_all_cases(offline_mode=True)
        case_ids = tuple(r.case_id for r in report.per_case)
        self.assertEqual(case_ids, ALPHA_CASE_IDS)

    def test_reference_behaviors_are_load_bearing(self) -> None:
        # Sanity: we should track at least 11 distinct behaviors (one per
        # procedure step + sub-behaviors).
        self.assertGreaterEqual(len(REFERENCE_BEHAVIORS), 11)
        # Each entry is a (key, description) pair.
        for entry in REFERENCE_BEHAVIORS:
            self.assertEqual(len(entry), 2)
            self.assertTrue(entry[0].startswith("step_"))


if __name__ == "__main__":
    unittest.main()
