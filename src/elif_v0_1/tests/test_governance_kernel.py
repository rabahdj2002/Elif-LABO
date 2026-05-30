"""Tests for the GovernanceKernel component (Step 9).

All tests run in offline_mode using the 3-case fixture matrix shipped in
`offline_fixtures/`. No network call is ever made.

Coverage targets:
    * verdict_with_confidence_and_uncertainty returns a schema-valid Step 9
      payload (offline).
    * offline mode is deterministic (same case_id -> same payload).
    * invalid inputs raise ELIFError before any LLM call.
    * SchemaValidationError surfaces when the adapter returns a malformed
      payload (simulated by monkeypatching `complete_structured`).
    * fixture routing maps `case_NN_*` -> `case_NN` correctly.
    * verdict drift (out-of-closed-set values) is rejected.
    * Article VI tie (confidence tied to unresolved sources) is enforced.
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
from elif_v0_1.components import governance_kernel as gk_module  # noqa: E402
from elif_v0_1.components.governance_kernel import (  # noqa: E402
    GovernanceKernel,
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
        run_id="run_test_gk",
    )


def _sample_step8_roadmap() -> dict:
    """A minimal Step 8 dict satisfying STEP_8_OUTPUT_SCHEMA."""
    return {
        "stages": [
            {
                "stage_id": "A1",
                "description": "Family A research-only pilot.",
                "continuation_gate": (
                    "Replicable yield delta > 5% across >= 3 sites."
                ),
            },
            {
                "stage_id": "B1",
                "description": "Protocol specification for Family B.",
                "continuation_gate": (
                    "Cross-proposer protocol agreement signed."
                ),
            },
        ]
    }


def _sample_prior_steps() -> dict:
    """A minimal prior-step dict with markers across step_1..step_7."""
    return {
        "step_1": {"verdict": "needs_decomposition", "reasoning": "bundle"},
        "step_2": {
            "axes": [
                {
                    "axis_name": "mechanism",
                    "families": [
                        {"family_id": "A", "description": "established"},
                        {"family_id": "B", "description": "unspecified"},
                    ],
                }
            ]
        },
        "step_3": {"assumptions": ["a1", "a2"]},
        "step_4": {
            "hypotheses": [
                {
                    "hypothesis_id": "H1",
                    "statement": "A works.",
                    "distinguishing_prediction": "yield > 5%",
                }
            ]
        },
        "step_5": {
            "failure_conditions": [
                {"hypothesis_id": "H1", "fails_if": "yield <= 5%"}
            ]
        },
        "step_6": {
            "scales": ["organism", "field"],
            "cross_scale_relations": ["organism does not aggregate to field"],
        },
        "step_7": {
            "trajectories": [
                {
                    "trajectory_id": "T1",
                    "tag": "outside-original-frame",
                    "reason": "reframe bundle as separable tracks",
                }
            ]
        },
    }


class TestGovernanceKernelArticleAndId(unittest.TestCase):
    """Doctrinal pins — component_id + Article ties are closed-set anchors."""

    def test_component_id_is_governance_kernel(self) -> None:
        self.assertEqual(GovernanceKernel.component_id, "governance_kernel")

    def test_article_ties_are_v_vi_vii(self) -> None:
        self.assertEqual(GovernanceKernel.article_ties, ("V", "VI", "VII"))

    def test_constructs_with_no_args(self) -> None:
        # Orchestrator constructs `GovernanceKernel()` in scaffold wiring.
        GovernanceKernel()


class TestVerdictOffline(unittest.TestCase):
    """Step 9 verdict emission (offline / fixture-driven)."""

    def setUp(self) -> None:
        reset_call_counter()
        self.kernel = GovernanceKernel()

    def test_returns_valid_shape(self) -> None:
        result = self.kernel.verdict_with_confidence_and_uncertainty(
            _sample_step8_roadmap(),
            _sample_prior_steps(),
            run_context=_make_ctx("case_01_electroculture"),
        )
        self.assertIsInstance(result, dict)
        self.assertIn("verdict", result)
        self.assertIn(
            result["verdict"],
            {"constrain", "refuse", "explicitly_abstain"},
        )
        self.assertIn("confidence", result)
        self.assertIsInstance(result["confidence"], str)
        self.assertIn("unresolved_uncertainty_sources", result)
        self.assertIsInstance(result["unresolved_uncertainty_sources"], list)
        self.assertGreaterEqual(
            len(result["unresolved_uncertainty_sources"]), 1
        )

    def test_offline_is_deterministic(self) -> None:
        ctx = _make_ctx("case_01_electroculture")
        reset_call_counter()
        first = self.kernel.verdict_with_confidence_and_uncertainty(
            _sample_step8_roadmap(),
            _sample_prior_steps(),
            run_context=ctx,
        )
        reset_call_counter()
        second = self.kernel.verdict_with_confidence_and_uncertainty(
            _sample_step8_roadmap(),
            _sample_prior_steps(),
            run_context=ctx,
        )
        self.assertEqual(first, second)

    def test_resolves_all_three_cases(self) -> None:
        """Each of the 3 cases must yield a Step 9 fixture without drift."""
        for case_token in ("case_01", "case_02", "case_03"):
            with self.subTest(case=case_token):
                reset_call_counter()
                result = self.kernel.verdict_with_confidence_and_uncertainty(
                    _sample_step8_roadmap(),
                    _sample_prior_steps(),
                    run_context=_make_ctx(case_token),
                )
                self.assertIn("verdict", result)
                self.assertIn(
                    result["verdict"],
                    {"constrain", "refuse", "explicitly_abstain"},
                )


class TestVerdictInputValidation(unittest.TestCase):
    """Input-shape guards must fire BEFORE consuming an LLM call slot."""

    def setUp(self) -> None:
        reset_call_counter()
        self.kernel = GovernanceKernel()

    def test_non_dict_roadmap_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.kernel.verdict_with_confidence_and_uncertainty(
                "not a roadmap dict",  # type: ignore[arg-type]
                _sample_prior_steps(),
                run_context=_make_ctx(),
            )

    def test_malformed_roadmap_missing_stages_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.kernel.verdict_with_confidence_and_uncertainty(
                {"something_else": []},
                _sample_prior_steps(),
                run_context=_make_ctx(),
            )

    def test_non_dict_prior_steps_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.kernel.verdict_with_confidence_and_uncertainty(
                _sample_step8_roadmap(),
                "not a prior-steps dict",  # type: ignore[arg-type]
                run_context=_make_ctx(),
            )

    def test_non_run_context_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.kernel.verdict_with_confidence_and_uncertainty(
                _sample_step8_roadmap(),
                _sample_prior_steps(),
                run_context="not a RunContext",  # type: ignore[arg-type]
            )

    def test_bad_case_id_raises(self) -> None:
        ctx = _make_ctx("totally_malformed_no_case_token")
        with self.assertRaises(ELIFError):
            self.kernel.verdict_with_confidence_and_uncertainty(
                _sample_step8_roadmap(),
                _sample_prior_steps(),
                run_context=ctx,
            )

    def test_empty_prior_steps_dict_is_accepted(self) -> None:
        """An empty prior-steps dict is structurally valid; the kernel can
        adjudicate even on a Step 8 roadmap without prior-step markers
        (the load-bearing input is the roadmap, not the history)."""
        result = self.kernel.verdict_with_confidence_and_uncertainty(
            _sample_step8_roadmap(),
            {},
            run_context=_make_ctx(),
        )
        self.assertIn("verdict", result)


class TestSchemaValidationOnMalformedResponse(unittest.TestCase):
    """If the adapter returns a malformed payload, GovernanceKernel must
    surface SchemaValidationError rather than silently passing drift on."""

    def setUp(self) -> None:
        reset_call_counter()
        self.kernel = GovernanceKernel()
        self._original = gk_module.complete_structured

    def tearDown(self) -> None:
        gk_module.complete_structured = self._original

    def test_malformed_response_missing_verdict_raises(self) -> None:
        """A payload missing the required `verdict` key fails at the schema."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "confidence": "high",
                "unresolved_uncertainty_sources": ["x"],
            }

        gk_module.complete_structured = _bad_complete
        with self.assertRaises(SchemaValidationError):
            self.kernel.verdict_with_confidence_and_uncertainty(
                _sample_step8_roadmap(),
                _sample_prior_steps(),
                run_context=_make_ctx(),
            )

    def test_out_of_closed_set_verdict_raises(self) -> None:
        """A verdict outside the closed set must be rejected."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "verdict": "recommend",  # not in closed set
                "confidence": "high",
                "unresolved_uncertainty_sources": ["x"],
            }

        gk_module.complete_structured = _bad_complete
        with self.assertRaises(SchemaValidationError):
            self.kernel.verdict_with_confidence_and_uncertainty(
                _sample_step8_roadmap(),
                _sample_prior_steps(),
                run_context=_make_ctx(),
            )

    def test_empty_unresolved_sources_raises(self) -> None:
        """An empty unresolved_uncertainty_sources list violates Article VII."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "verdict": "refuse",
                "confidence": "high",
                "unresolved_uncertainty_sources": [],
            }

        gk_module.complete_structured = _bad_complete
        with self.assertRaises(SchemaValidationError):
            self.kernel.verdict_with_confidence_and_uncertainty(
                _sample_step8_roadmap(),
                _sample_prior_steps(),
                run_context=_make_ctx(),
            )

    def test_empty_confidence_raises(self) -> None:
        """An empty `confidence` string violates Article VI (no unconditioned
        confidence claim)."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "verdict": "refuse",
                "confidence": "",
                "unresolved_uncertainty_sources": ["x"],
            }

        gk_module.complete_structured = _bad_complete
        with self.assertRaises(SchemaValidationError):
            self.kernel.verdict_with_confidence_and_uncertainty(
                _sample_step8_roadmap(),
                _sample_prior_steps(),
                run_context=_make_ctx(),
            )


class TestCaseTokenExtraction(unittest.TestCase):
    """Fixture routing must tolerate prose-form case_ids."""

    def test_extracts_case_01_from_prose_id(self) -> None:
        self.assertEqual(
            gk_module._extract_case_token("case_01_electroculture"),
            "case_01",
        )

    def test_extracts_bare_case_token(self) -> None:
        self.assertEqual(
            gk_module._extract_case_token("case_03"),
            "case_03",
        )

    def test_raises_on_unparseable_id(self) -> None:
        with self.assertRaises(ELIFError):
            gk_module._extract_case_token("no_token_here")


if __name__ == "__main__":
    unittest.main()
