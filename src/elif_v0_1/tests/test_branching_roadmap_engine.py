"""Tests for the BranchingRoadmapEngine component (Step 7-modeA + Step 8).

All tests run in offline_mode using the 3-case fixture matrix shipped in
`offline_fixtures/`. No network call is ever made.

Coverage targets:
    * outside_frame_trajectories_bre_feed returns a schema-valid Step 7
      payload (offline).
    * stage_gated_roadmap returns a schema-valid Step 8 payload (offline).
    * offline mode is deterministic (same case_id -> same payload).
    * invalid inputs raise ELIFError before any LLM call.
    * SchemaValidationError surfaces when the adapter returns a malformed
      payload (simulated by monkeypatching `complete_structured`).
    * fixture routing maps `case_NN_*` -> `case_NN` correctly.
    * mode-B contamination (deeper-frame-rejection tags leaking into
      mode-A output) is rejected.
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

from elif_v0_1.base import (  # noqa: E402
    ELIFError,
    SchemaValidationError,
)
from elif_v0_1.components import branching_roadmap_engine as bre_module  # noqa: E402
from elif_v0_1.components.branching_roadmap_engine import (  # noqa: E402
    BranchingRoadmapEngine,
)
from elif_v0_1.llm_adapter import reset_call_counter  # noqa: E402
from elif_v0_1.run_context import RunContext  # noqa: E402


def _make_ctx(
    case_id: str = "case_01_electroculture",
    offline: bool = True,
    max_calls: int = 22,
) -> RunContext:
    return RunContext(
        case_id=case_id,
        condition="c",
        procedure_version="v1.0",
        offline_mode=offline,
        max_llm_calls=max_calls,
        started_at_iso="2026-05-29T12:00:00+00:00",
        run_id="run_test_bre",
    )


def _sample_step4_hypotheses() -> dict:
    """A minimal Step 4 dict satisfying STEP_4_OUTPUT_SCHEMA."""
    return {
        "hypotheses": [
            {
                "hypothesis_id": "H1",
                "statement": "Family A techniques have a measurable effect.",
                "distinguishing_prediction": (
                    "Yield change > 5% vs control plots."
                ),
            },
            {
                "hypothesis_id": "H2",
                "statement": "Family B techniques are mechanism-unspecified.",
                "distinguishing_prediction": (
                    "No coherent protocol exists across proposers."
                ),
            },
        ]
    }


def _sample_step5_failures() -> dict:
    """A minimal Step 5 dict satisfying STEP_5_OUTPUT_SCHEMA."""
    return {
        "failure_conditions": [
            {
                "hypothesis_id": "H1",
                "fails_if": (
                    "Pre-registered replication studies show null effect."
                ),
            },
            {
                "hypothesis_id": "H2",
                "fails_if": (
                    "Independent reviewers report mechanism plausibility."
                ),
            },
        ]
    }


class TestBranchingRoadmapEngineArticleAndId(unittest.TestCase):
    """Doctrinal pins — component_id + Article ties are closed-set anchors."""

    def test_component_id(self) -> None:
        self.assertEqual(
            BranchingRoadmapEngine.component_id, "branching_roadmap_engine"
        )

    def test_article_ties_are_V_VI_VII(self) -> None:
        self.assertEqual(
            BranchingRoadmapEngine.article_ties, ("V", "VI", "VII")
        )

    def test_constructs_with_no_args(self) -> None:
        # Orchestrator constructs `BranchingRoadmapEngine()` in scaffold wiring.
        BranchingRoadmapEngine()

    def test_constructs_with_run_context(self) -> None:
        BranchingRoadmapEngine(_make_ctx())


class TestOutsideFrameTrajectoriesOffline(unittest.TestCase):
    """Step 7 mode A — outside-original-frame trajectories (offline)."""

    def setUp(self) -> None:
        reset_call_counter()

    def test_returns_valid_shape(self) -> None:
        bre = BranchingRoadmapEngine(_make_ctx("case_01_electroculture"))
        result = bre.outside_frame_trajectories_bre_feed(
            _sample_step4_hypotheses(),
            _sample_step5_failures(),
        )
        self.assertIsInstance(result, dict)
        self.assertIn("trajectories", result)
        self.assertIsInstance(result["trajectories"], list)
        self.assertGreaterEqual(len(result["trajectories"]), 1)
        for traj in result["trajectories"]:
            self.assertIn("trajectory_id", traj)
            self.assertIn("tag", traj)
            self.assertIn("reason", traj)
            # mode A only — fixture-driven content must be mode A.
            self.assertEqual(traj["tag"], "outside-original-frame")

    def test_offline_is_deterministic(self) -> None:
        ctx = _make_ctx("case_01_electroculture")
        hyps = _sample_step4_hypotheses()
        fails = _sample_step5_failures()
        reset_call_counter()
        first = BranchingRoadmapEngine(ctx).outside_frame_trajectories_bre_feed(
            hyps, fails
        )
        reset_call_counter()
        second = BranchingRoadmapEngine(ctx).outside_frame_trajectories_bre_feed(
            hyps, fails
        )
        self.assertEqual(first, second)

    def test_resolves_all_three_cases(self) -> None:
        """Each of the 3 cases must yield a Step 7 fixture without drift."""
        for case_token in ("case_01", "case_02", "case_03"):
            with self.subTest(case=case_token):
                reset_call_counter()
                bre = BranchingRoadmapEngine(_make_ctx(case_token))
                result = bre.outside_frame_trajectories_bre_feed(
                    _sample_step4_hypotheses(),
                    _sample_step5_failures(),
                )
                self.assertIn("trajectories", result)


class TestOutsideFrameInputValidation(unittest.TestCase):
    """Input-shape guards must fire BEFORE consuming an LLM call slot."""

    def setUp(self) -> None:
        reset_call_counter()
        self.bre = BranchingRoadmapEngine(_make_ctx())

    def test_non_dict_hypotheses_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.bre.outside_frame_trajectories_bre_feed(
                "not a dict", _sample_step5_failures()
            )

    def test_non_dict_failures_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.bre.outside_frame_trajectories_bre_feed(
                _sample_step4_hypotheses(), 42
            )

    def test_malformed_step4_input_raises(self) -> None:
        """Step 4 dict missing `hypotheses` must halt at the component boundary."""
        with self.assertRaises(ELIFError):
            self.bre.outside_frame_trajectories_bre_feed(
                {"something_else": []}, _sample_step5_failures()
            )

    def test_malformed_step5_input_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.bre.outside_frame_trajectories_bre_feed(
                _sample_step4_hypotheses(), {"not_failure_conditions": []}
            )


class TestStageGatedRoadmapOffline(unittest.TestCase):
    """Step 8 — stage-gated roadmap (offline)."""

    def setUp(self) -> None:
        reset_call_counter()

    def _step7_for(self, case_id: str) -> dict:
        reset_call_counter()
        bre = BranchingRoadmapEngine(_make_ctx(case_id))
        return bre.outside_frame_trajectories_bre_feed(
            _sample_step4_hypotheses(),
            _sample_step5_failures(),
        )

    def test_returns_valid_shape(self) -> None:
        step7 = self._step7_for("case_01_electroculture")
        reset_call_counter()
        bre = BranchingRoadmapEngine(_make_ctx("case_01_electroculture"))
        result = bre.stage_gated_roadmap(step7)
        self.assertIn("stages", result)
        self.assertGreaterEqual(len(result["stages"]), 1)
        for stage in result["stages"]:
            self.assertIn("stage_id", stage)
            self.assertIn("description", stage)
            self.assertIn("continuation_gate", stage)

    def test_offline_is_deterministic(self) -> None:
        step7 = self._step7_for("case_01_electroculture")
        ctx = _make_ctx("case_01_electroculture")
        reset_call_counter()
        first = BranchingRoadmapEngine(ctx).stage_gated_roadmap(step7)
        reset_call_counter()
        second = BranchingRoadmapEngine(ctx).stage_gated_roadmap(step7)
        self.assertEqual(first, second)

    def test_rejects_non_dict_trajectories(self) -> None:
        bre = BranchingRoadmapEngine(_make_ctx())
        with self.assertRaises(ELIFError):
            bre.stage_gated_roadmap("not a dict")

    def test_rejects_malformed_step7_input(self) -> None:
        """Step 7 dict missing `trajectories` must halt at the boundary."""
        bre = BranchingRoadmapEngine(_make_ctx())
        with self.assertRaises(ELIFError):
            bre.stage_gated_roadmap({"not_trajectories": []})


class TestSchemaValidationOnMalformedResponse(unittest.TestCase):
    """If the adapter returns a malformed payload, BranchingRoadmapEngine
    must surface SchemaValidationError rather than silently passing drift."""

    def setUp(self) -> None:
        reset_call_counter()
        self._original = bre_module.complete_structured

    def tearDown(self) -> None:
        bre_module.complete_structured = self._original

    def test_malformed_step7_response_raises(self) -> None:
        """Inject a payload missing the required `trajectories` key."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {"not_trajectories": []}

        bre_module.complete_structured = _bad_complete
        bre = BranchingRoadmapEngine(_make_ctx())
        with self.assertRaises(SchemaValidationError):
            bre.outside_frame_trajectories_bre_feed(
                _sample_step4_hypotheses(),
                _sample_step5_failures(),
            )

    def test_step7_with_modeB_tag_raises(self) -> None:
        """A `deeper-frame-rejection` tag in mode-A output violates §8.10."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "trajectories": [
                    {
                        "trajectory_id": "T1",
                        "tag": "deeper-frame-rejection",
                        "reason": "leaked mode-B tag",
                    }
                ]
            }

        bre_module.complete_structured = _bad_complete
        bre = BranchingRoadmapEngine(_make_ctx())
        with self.assertRaises(SchemaValidationError):
            bre.outside_frame_trajectories_bre_feed(
                _sample_step4_hypotheses(),
                _sample_step5_failures(),
            )

    def test_malformed_step8_response_raises(self) -> None:
        """A Step 8 payload missing required `stages` violates the schema."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {"no_stages_here": []}

        bre_module.complete_structured = _bad_complete
        bre = BranchingRoadmapEngine(_make_ctx())
        trajectories = {
            "trajectories": [
                {
                    "trajectory_id": "T1",
                    "tag": "outside-original-frame",
                    "reason": "any",
                }
            ]
        }
        with self.assertRaises(SchemaValidationError):
            bre.stage_gated_roadmap(trajectories)

    def test_step8_with_missing_continuation_gate_raises(self) -> None:
        """A stage missing `continuation_gate` violates Step 8 semantics."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "stages": [
                    {
                        "stage_id": "A1",
                        "description": "do stuff",
                        # missing continuation_gate
                    }
                ]
            }

        bre_module.complete_structured = _bad_complete
        bre = BranchingRoadmapEngine(_make_ctx())
        trajectories = {
            "trajectories": [
                {
                    "trajectory_id": "T1",
                    "tag": "outside-original-frame",
                    "reason": "any",
                }
            ]
        }
        with self.assertRaises(SchemaValidationError):
            bre.stage_gated_roadmap(trajectories)


class TestCaseTokenExtraction(unittest.TestCase):
    """Fixture routing must tolerate prose-form case_ids."""

    def test_extracts_case_01_from_prose_id(self) -> None:
        self.assertEqual(
            bre_module._extract_case_token("case_01_electroculture"),
            "case_01",
        )

    def test_extracts_bare_case_token(self) -> None:
        self.assertEqual(
            bre_module._extract_case_token("case_03"),
            "case_03",
        )

    def test_raises_on_unparseable_id(self) -> None:
        with self.assertRaises(ELIFError):
            bre_module._extract_case_token("no_token_here")


if __name__ == "__main__":
    unittest.main()
