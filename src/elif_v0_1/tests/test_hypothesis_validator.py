"""Tests for the HypothesisValidator component (Step 4 + Step 5).

All tests run in offline_mode using the 11x3 fixture matrix shipped in
`offline_fixtures/`. No network call is ever made.

Coverage targets:
    * enumerate_hypotheses_with_distinguishing_predictions returns a
      schema-valid Step 4 payload (offline).
    * failure_conditions_per_hypothesis returns a schema-valid Step 5
      payload (offline).
    * offline mode is deterministic (same case_id -> same payload).
    * invalid inputs raise ELIFError before any LLM call.
    * SchemaValidationError surfaces when the adapter returns a malformed
      payload (simulated by monkeypatching `complete_structured`).
    * fixture routing maps `case_NN_*` -> `case_NN` correctly.
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
from elif_v0_1.components import hypothesis_validator as hv_module  # noqa: E402
from elif_v0_1.components.hypothesis_validator import (  # noqa: E402
    HypothesisValidator,
)
from elif_v0_1.components.object_decomposer import (  # noqa: E402
    ObjectDecomposer,
)
from elif_v0_1.base import InputFrame  # noqa: E402
from elif_v0_1.llm_adapter import reset_call_counter  # noqa: E402
from elif_v0_1.run_context import RunContext  # noqa: E402


def _make_ctx(
    case_id: str = "case_01_electroculture",
    offline: bool = True,
) -> RunContext:
    return RunContext(
        case_id=case_id,
        condition="c",
        procedure_version="v1.0",
        offline_mode=offline,
        max_llm_calls=22,
        started_at_iso="2026-05-29T12:00:00+00:00",
        run_id="run_test_001",
    )


def _make_frame() -> InputFrame:
    return InputFrame(
        id="frame_001",
        text="Should we authorize bundled electroculture pilots?",
        locked_at_iso="2026-05-29T12:00:00+00:00",
        doctrinal_scope_tag="agricultural_authorization",
        companion_case="case_01_electroculture",
    )


def _step2_payload_for(case_id: str = "case_01_electroculture") -> dict:
    """Deterministically resolve a Step 2 fixture for downstream Step 4 input."""
    reset_call_counter()
    return ObjectDecomposer().decompose(
        _make_frame(),
        run_context=_make_ctx(case_id),
    )


class TestHypothesisValidatorClassContract(unittest.TestCase):
    """Pinned scaffold contract — names + article ties."""

    def test_component_id_is_hypothesis_validator(self) -> None:
        self.assertEqual(
            HypothesisValidator.component_id, "hypothesis_validator"
        )

    def test_article_ties_include_i_and_iii(self) -> None:
        self.assertIn("I", HypothesisValidator.article_ties)
        self.assertIn("III", HypothesisValidator.article_ties)

    def test_constructs_with_no_args(self) -> None:
        # Orchestrator constructs `HypothesisValidator()` in scaffold wiring.
        HypothesisValidator()


class TestEnumerateHypothesesOffline(unittest.TestCase):
    """Step 4 hypotheses + distinguishing predictions (offline)."""

    def setUp(self) -> None:
        reset_call_counter()
        self.hv = HypothesisValidator()

    def test_returns_valid_shape(self) -> None:
        step2 = _step2_payload_for("case_01_electroculture")
        reset_call_counter()
        result = self.hv.enumerate_hypotheses_with_distinguishing_predictions(
            step2,
            run_context=_make_ctx("case_01_electroculture"),
        )
        self.assertIsInstance(result, dict)
        self.assertIn("hypotheses", result)
        self.assertIsInstance(result["hypotheses"], list)
        self.assertGreaterEqual(len(result["hypotheses"]), 1)
        for h in result["hypotheses"]:
            self.assertIn("hypothesis_id", h)
            self.assertIn("statement", h)
            self.assertIn("distinguishing_prediction", h)

    def test_offline_is_deterministic(self) -> None:
        step2 = _step2_payload_for("case_01_electroculture")
        ctx = _make_ctx("case_01_electroculture")
        reset_call_counter()
        first = self.hv.enumerate_hypotheses_with_distinguishing_predictions(
            step2, run_context=ctx
        )
        reset_call_counter()
        second = self.hv.enumerate_hypotheses_with_distinguishing_predictions(
            step2, run_context=ctx
        )
        self.assertEqual(first, second)

    def test_resolves_all_three_cases(self) -> None:
        """Each of the 3 cases must yield a Step 4 fixture without drift."""
        for case_token in ("case_01", "case_02", "case_03"):
            with self.subTest(case=case_token):
                step2 = _step2_payload_for(case_token)
                reset_call_counter()
                result = (
                    self.hv
                    .enumerate_hypotheses_with_distinguishing_predictions(
                        step2,
                        run_context=_make_ctx(case_token),
                    )
                )
                self.assertIn("hypotheses", result)


class TestEnumerateHypothesesInputValidation(unittest.TestCase):
    """Input-shape guards must fire BEFORE consuming an LLM call slot."""

    def setUp(self) -> None:
        reset_call_counter()
        self.hv = HypothesisValidator()

    def test_non_dict_decomposition_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.hv.enumerate_hypotheses_with_distinguishing_predictions(
                "not a dict",  # type: ignore[arg-type]
                run_context=_make_ctx(),
            )

    def test_malformed_step2_input_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.hv.enumerate_hypotheses_with_distinguishing_predictions(
                {"something_else": []},
                run_context=_make_ctx(),
            )

    def test_non_run_context_raises(self) -> None:
        step2 = _step2_payload_for("case_01_electroculture")
        with self.assertRaises(ELIFError):
            self.hv.enumerate_hypotheses_with_distinguishing_predictions(
                step2,
                run_context="not a RunContext",  # type: ignore[arg-type]
            )

    def test_bad_case_id_raises(self) -> None:
        step2 = _step2_payload_for("case_01_electroculture")
        ctx = _make_ctx("totally_malformed_no_case_token")
        with self.assertRaises(ELIFError):
            self.hv.enumerate_hypotheses_with_distinguishing_predictions(
                step2, run_context=ctx
            )


class TestFailureConditionsOffline(unittest.TestCase):
    """Step 5 failure conditions per hypothesis (offline)."""

    def setUp(self) -> None:
        reset_call_counter()
        self.hv = HypothesisValidator()

    def _step4_for(self, case_id: str) -> dict:
        step2 = _step2_payload_for(case_id)
        reset_call_counter()
        return self.hv.enumerate_hypotheses_with_distinguishing_predictions(
            step2, run_context=_make_ctx(case_id)
        )

    def test_returns_valid_shape(self) -> None:
        step4 = self._step4_for("case_01_electroculture")
        reset_call_counter()
        result = self.hv.failure_conditions_per_hypothesis(
            step4, run_context=_make_ctx("case_01_electroculture")
        )
        self.assertIsInstance(result, dict)
        self.assertIn("failure_conditions", result)
        self.assertIsInstance(result["failure_conditions"], list)
        self.assertGreaterEqual(len(result["failure_conditions"]), 1)
        for entry in result["failure_conditions"]:
            self.assertIn("hypothesis_id", entry)
            self.assertIn("fails_if", entry)

    def test_offline_is_deterministic(self) -> None:
        step4 = self._step4_for("case_01_electroculture")
        ctx = _make_ctx("case_01_electroculture")
        reset_call_counter()
        first = self.hv.failure_conditions_per_hypothesis(
            step4, run_context=ctx
        )
        reset_call_counter()
        second = self.hv.failure_conditions_per_hypothesis(
            step4, run_context=ctx
        )
        self.assertEqual(first, second)

    def test_rejects_non_dict_hypotheses(self) -> None:
        with self.assertRaises(ELIFError):
            self.hv.failure_conditions_per_hypothesis(
                "not a dict",  # type: ignore[arg-type]
                run_context=_make_ctx(),
            )

    def test_rejects_malformed_step4_input(self) -> None:
        """Step 4 dict missing `hypotheses` must halt at the boundary."""
        with self.assertRaises(ELIFError):
            self.hv.failure_conditions_per_hypothesis(
                {"something_else": []},
                run_context=_make_ctx(),
            )


class TestSchemaValidationOnMalformedResponse(unittest.TestCase):
    """If the adapter returns a malformed payload, HypothesisValidator must
    surface SchemaValidationError rather than silently passing drift on."""

    def setUp(self) -> None:
        reset_call_counter()
        self.hv = HypothesisValidator()
        self._original = hv_module.complete_structured

    def tearDown(self) -> None:
        hv_module.complete_structured = self._original

    def test_malformed_step4_response_raises(self) -> None:
        """Inject a payload missing the required `hypotheses` key."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {"not_hypotheses": []}

        hv_module.complete_structured = _bad_complete
        step2 = _step2_payload_for("case_01_electroculture")
        with self.assertRaises(SchemaValidationError):
            self.hv.enumerate_hypotheses_with_distinguishing_predictions(
                step2, run_context=_make_ctx()
            )

    def test_step4_hypothesis_missing_prediction_raises(self) -> None:
        """A hypothesis without `distinguishing_prediction` violates
        Article I (concern-masquerading-as-hypothesis)."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "hypotheses": [
                    {"hypothesis_id": "H1", "statement": "x"}
                ]
            }

        hv_module.complete_structured = _bad_complete
        step2 = _step2_payload_for("case_01_electroculture")
        with self.assertRaises(SchemaValidationError):
            self.hv.enumerate_hypotheses_with_distinguishing_predictions(
                step2, run_context=_make_ctx()
            )

    def test_step5_missing_fails_if_raises(self) -> None:
        """A failure_condition entry without `fails_if` violates Article I."""
        step4_payload = {
            "hypotheses": [
                {
                    "hypothesis_id": "H1",
                    "statement": "x",
                    "distinguishing_prediction": "y",
                }
            ]
        }

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "failure_conditions": [
                    {"hypothesis_id": "H1"}
                ]
            }

        hv_module.complete_structured = _bad_complete
        with self.assertRaises(SchemaValidationError):
            self.hv.failure_conditions_per_hypothesis(
                step4_payload, run_context=_make_ctx()
            )

    def test_step4_duplicate_hypothesis_id_raises(self) -> None:
        """Two hypotheses sharing an id violates closed-set id discipline."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "hypotheses": [
                    {
                        "hypothesis_id": "H1",
                        "statement": "x",
                        "distinguishing_prediction": "y",
                    },
                    {
                        "hypothesis_id": "H1",
                        "statement": "z",
                        "distinguishing_prediction": "w",
                    },
                ]
            }

        hv_module.complete_structured = _bad_complete
        step2 = _step2_payload_for("case_01_electroculture")
        with self.assertRaises(SchemaValidationError):
            self.hv.enumerate_hypotheses_with_distinguishing_predictions(
                step2, run_context=_make_ctx()
            )


class TestCaseTokenExtraction(unittest.TestCase):
    """Fixture routing must tolerate prose-form case_ids."""

    def test_extracts_case_01_from_prose_id(self) -> None:
        self.assertEqual(
            hv_module._extract_case_token("case_01_electroculture"),
            "case_01",
        )

    def test_extracts_bare_case_token(self) -> None:
        self.assertEqual(
            hv_module._extract_case_token("case_03"),
            "case_03",
        )

    def test_raises_on_unparseable_id(self) -> None:
        with self.assertRaises(ELIFError):
            hv_module._extract_case_token("no_token_here")


if __name__ == "__main__":
    unittest.main()
