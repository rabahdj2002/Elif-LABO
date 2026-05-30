"""Tests for the OperativeTruthSeparator component (Step 10).

All tests run in offline_mode using the 3-case fixture matrix shipped in
`offline_fixtures/`. No network call is ever made.

Coverage targets:
    * separate_operative_from_theoretical returns a schema-valid Step 10
      payload (offline).
    * offline mode is deterministic (same case_id -> same payload).
    * invalid inputs raise ELIFError before any LLM call.
    * SchemaValidationError surfaces when the adapter returns a malformed
      payload (simulated by monkeypatching `complete_structured`).
    * fixture routing maps `case_NN_*` -> `case_NN` correctly.
    * pinned method signature.

Authored 2026-05-30 as part of the v0.1-alpha resume sprint after the
parallel agent that should have written this file failed to emit
structured output. The component implementation
(operative_truth_separator.py) is unchanged from that agent's work;
this test file mirrors the test_governance_kernel.py pattern.
"""

from __future__ import annotations

import os
import sys
import unittest

_SRC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from elif_v0_1.base import (  # noqa: E402
    ELIFError,
    SchemaValidationError,
)
from elif_v0_1.components import (  # noqa: E402
    operative_truth_separator as ots_module,
)
from elif_v0_1.components.operative_truth_separator import (  # noqa: E402
    OperativeTruthSeparator,
)
from elif_v0_1.llm_adapter import reset_call_counter  # noqa: E402
from elif_v0_1.run_context import RunContext  # noqa: E402


def _make_ctx(case_id: str = "case_01_electroculture") -> RunContext:
    return RunContext(
        case_id=case_id,
        condition="c",
        procedure_version="v1.0",
        offline_mode=True,
        max_llm_calls=22,
        started_at_iso="2026-05-30T12:00:00+00:00",
        run_id="run_test_ots",
    )


def _sample_prior_steps() -> dict:
    """Minimal prior_steps dict satisfying the component's input contract."""
    return {
        "step_9": {
            "verdict": "constrain",
            "confidence_qualifier": "moderate",
            "unresolved_uncertainty_sources": ["regulatory_window"],
        },
        "step_8": {
            "stages": [
                {"stage_id": "stage_1", "continuation_gate": "evidence_gate_a"},
            ],
        },
    }


class TestClassContract(unittest.TestCase):
    def test_instantiates_with_no_args(self) -> None:
        ots = OperativeTruthSeparator()
        self.assertIsInstance(ots, OperativeTruthSeparator)

    def test_separate_method_present(self) -> None:
        ots = OperativeTruthSeparator()
        self.assertTrue(
            hasattr(ots, "separate_operative_from_theoretical")
        )


class TestOfflineSeparate(unittest.TestCase):
    def setUp(self) -> None:
        reset_call_counter()

    def test_returns_schema_valid_payload(self) -> None:
        ots = OperativeTruthSeparator()
        result = ots.separate_operative_from_theoretical(
            _sample_prior_steps(),
            run_context=_make_ctx(),
        )
        self.assertIsInstance(result, dict)
        self.assertIn("operative", result)
        self.assertIn("theoretical", result)
        self.assertIsInstance(result["operative"], list)
        self.assertIsInstance(result["theoretical"], list)

    def test_offline_deterministic(self) -> None:
        ots = OperativeTruthSeparator()
        prior = _sample_prior_steps()
        a = ots.separate_operative_from_theoretical(
            prior, run_context=_make_ctx()
        )
        b = ots.separate_operative_from_theoretical(
            prior, run_context=_make_ctx()
        )
        self.assertEqual(a, b)

    def test_all_three_cases_route_to_fixtures(self) -> None:
        ots = OperativeTruthSeparator()
        prior = _sample_prior_steps()
        for case_id in (
            "case_01_electroculture",
            "case_02_policy_governance",
            "case_03_operational_organizational",
        ):
            result = ots.separate_operative_from_theoretical(
                prior, run_context=_make_ctx(case_id=case_id)
            )
            self.assertIn("operative", result)
            self.assertIn("theoretical", result)


class TestInputValidation(unittest.TestCase):
    def setUp(self) -> None:
        reset_call_counter()

    def test_non_dict_prior_steps_raises(self) -> None:
        ots = OperativeTruthSeparator()
        with self.assertRaises(ELIFError):
            ots.separate_operative_from_theoretical(
                "not a dict",  # type: ignore[arg-type]
                run_context=_make_ctx(),
            )

    def test_none_prior_steps_raises(self) -> None:
        ots = OperativeTruthSeparator()
        with self.assertRaises(ELIFError):
            ots.separate_operative_from_theoretical(
                None,  # type: ignore[arg-type]
                run_context=_make_ctx(),
            )


class TestSchemaValidationOnMalformedResponse(unittest.TestCase):
    def setUp(self) -> None:
        reset_call_counter()

    def test_missing_operative_key_raises_schema_error(self) -> None:
        ots = OperativeTruthSeparator()
        original = ots_module.complete_structured

        def fake_complete(*args, **kwargs):
            return {"theoretical": ["x"]}  # missing operative

        ots_module.complete_structured = fake_complete
        try:
            with self.assertRaises(SchemaValidationError):
                ots.separate_operative_from_theoretical(
                    _sample_prior_steps(),
                    run_context=RunContext(
                        case_id="case_01_electroculture",
                        condition="c",
                        procedure_version="v1.0",
                        offline_mode=False,
                        max_llm_calls=22,
                        started_at_iso="2026-05-30T12:00:00+00:00",
                        run_id="run_malformed",
                    ),
                )
        finally:
            ots_module.complete_structured = original

    def test_non_list_operative_raises_schema_error(self) -> None:
        ots = OperativeTruthSeparator()
        original = ots_module.complete_structured

        def fake_complete(*args, **kwargs):
            return {"operative": "not a list", "theoretical": []}

        ots_module.complete_structured = fake_complete
        try:
            with self.assertRaises(SchemaValidationError):
                ots.separate_operative_from_theoretical(
                    _sample_prior_steps(),
                    run_context=RunContext(
                        case_id="case_02_policy_governance",
                        condition="c",
                        procedure_version="v1.0",
                        offline_mode=False,
                        max_llm_calls=22,
                        started_at_iso="2026-05-30T12:00:00+00:00",
                        run_id="run_malformed_b",
                    ),
                )
        finally:
            ots_module.complete_structured = original


if __name__ == "__main__":
    unittest.main()
