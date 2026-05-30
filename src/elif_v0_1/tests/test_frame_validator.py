"""Tests for FrameValidator — Step 1 + Step 3 + Step 7-modeB.

Article II tie. Coverage:
    * returns_valid_shape (offline) for all three methods
    * offline_deterministic (same fixture → same output)
    * invalid_input_raises (non-InputFrame → ELIFError)
    * schema_validation_on_malformed_response (fixture drift → SchemaValidationError)
    * case_id routing (run_context drives fixture selection)
    * pinned method signatures + class attributes
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Path shim so `elif_v0_1` resolves under `python3 -m unittest`.
_SRC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from elif_v0_1.base import (  # noqa: E402
    ELIFError,
    InputFrame,
    SchemaValidationError,
)
from elif_v0_1.components.frame_validator import FrameValidator  # noqa: E402
from elif_v0_1.llm_adapter import reset_call_counter  # noqa: E402
from elif_v0_1.run_context import RunContext  # noqa: E402


def _make_input_frame(frame_id: str = "frame_001") -> InputFrame:
    """Build a deterministic InputFrame fixture for tests."""
    return InputFrame(
        id=frame_id,
        text=(
            "Should we authorize a coalition of researchers, agencies, and "
            "private firms to conduct electroculture research with pilot "
            "deployment in drought-prone regions?"
        ),
        locked_at_iso="2026-05-29T12:00:00Z",
        doctrinal_scope_tag="case_01_electroculture",
        companion_case="condition_c",
    )


def _make_run_context(
    case_id: str = "case_01_electroculture",
    offline_mode: bool = True,
    max_calls: int = 22,
) -> RunContext:
    return RunContext(
        case_id=case_id,
        condition="c",
        procedure_version="v1.0",
        offline_mode=offline_mode,
        max_llm_calls=max_calls,
        started_at_iso="2026-05-29T12:00:00Z",
        run_id="run_test_001",
    )


class TestFrameValidatorClassContract(unittest.TestCase):
    """Pinned scaffold contract — names + article ties + ctor shape."""

    def test_component_id_is_frame_validator(self) -> None:
        self.assertEqual(FrameValidator.component_id, "frame_validator")

    def test_article_ties_include_article_ii(self) -> None:
        # Article II is the doctrinal anchor for this component.
        self.assertIn("II", FrameValidator.article_ties)

    def test_constructs_with_no_args(self) -> None:
        # Orchestrator constructs `FrameValidator()` in scaffold wiring.
        FrameValidator()

    def test_constructs_with_run_context(self) -> None:
        FrameValidator(_make_run_context())


class TestValidateStep1(unittest.TestCase):
    """Step 1: verdict emission, offline fixture path."""

    def setUp(self) -> None:
        reset_call_counter()

    def test_returns_valid_shape_offline(self) -> None:
        fv = FrameValidator(_make_run_context())
        result = fv.validate(_make_input_frame())
        self.assertIsInstance(result, dict)
        self.assertIn("verdict", result)
        self.assertIn(
            result["verdict"],
            {"valid", "invalid", "needs_decomposition"},
        )
        self.assertIn("reasoning", result)

    def test_offline_deterministic(self) -> None:
        rc = _make_run_context()
        fv1 = FrameValidator(rc)
        reset_call_counter()
        first = fv1.validate(_make_input_frame())
        reset_call_counter()
        fv2 = FrameValidator(rc)
        second = fv2.validate(_make_input_frame())
        self.assertEqual(first, second)

    def test_invalid_input_raises(self) -> None:
        fv = FrameValidator(_make_run_context())
        with self.assertRaises(ELIFError):
            fv.validate("not an input frame")  # type: ignore[arg-type]

    def test_invalid_input_dict_raises(self) -> None:
        fv = FrameValidator(_make_run_context())
        with self.assertRaises(ELIFError):
            fv.validate({"id": "x", "text": "y"})  # type: ignore[arg-type]


class TestSurfaceAssumptionsStep3(unittest.TestCase):
    """Step 3: hidden-assumption surfacing."""

    def setUp(self) -> None:
        reset_call_counter()

    def test_returns_valid_shape_offline(self) -> None:
        fv = FrameValidator(_make_run_context())
        result = fv.surface_assumptions(_make_input_frame())
        self.assertIsInstance(result, dict)
        self.assertIn("assumptions", result)
        self.assertIsInstance(result["assumptions"], list)
        # Build plan §2.1: at least 2 assumptions.
        self.assertGreaterEqual(len(result["assumptions"]), 2)

    def test_offline_deterministic(self) -> None:
        rc = _make_run_context()
        reset_call_counter()
        first = FrameValidator(rc).surface_assumptions(_make_input_frame())
        reset_call_counter()
        second = FrameValidator(rc).surface_assumptions(_make_input_frame())
        self.assertEqual(first, second)

    def test_invalid_input_raises(self) -> None:
        fv = FrameValidator(_make_run_context())
        with self.assertRaises(ELIFError):
            fv.surface_assumptions(None)  # type: ignore[arg-type]


class TestSurfaceDeeperFrameRejectionStep7(unittest.TestCase):
    """Step 7 mode B: deeper-frame-rejection trajectories."""

    def setUp(self) -> None:
        reset_call_counter()

    def test_returns_valid_shape_offline(self) -> None:
        fv = FrameValidator(_make_run_context())
        result = fv.surface_deeper_frame_rejection(_make_input_frame())
        self.assertIsInstance(result, dict)
        self.assertIn("trajectories", result)
        self.assertIsInstance(result["trajectories"], list)
        self.assertGreaterEqual(len(result["trajectories"]), 1)
        # Each trajectory must have the schema-pinned keys.
        for traj in result["trajectories"]:
            self.assertIn("trajectory_id", traj)
            self.assertIn("tag", traj)
            self.assertIn("reason", traj)

    def test_invalid_input_raises(self) -> None:
        fv = FrameValidator(_make_run_context())
        with self.assertRaises(ELIFError):
            fv.surface_deeper_frame_rejection(42)  # type: ignore[arg-type]


class TestCaseIdRouting(unittest.TestCase):
    """RunContext.case_id drives offline fixture selection."""

    def setUp(self) -> None:
        reset_call_counter()

    def test_case_02_routes_to_case_02_fixture(self) -> None:
        rc = _make_run_context(case_id="case_02_carbon_capture")
        fv = FrameValidator(rc)
        result = fv.validate(_make_input_frame())
        # Should successfully load step_01__case_02 — schema-valid dict.
        self.assertIn("verdict", result)

    def test_case_03_routes_to_case_03_fixture(self) -> None:
        rc = _make_run_context(case_id="case_03_genome_editing")
        fv = FrameValidator(rc)
        result = fv.validate(_make_input_frame())
        self.assertIn("verdict", result)

    def test_no_run_context_defaults_to_case_01(self) -> None:
        # Construction-without-context path falls back deterministically.
        fv = FrameValidator()
        # Default is offline_mode=False, so this would attempt a live call;
        # we cannot exercise it without an API key. The path is tested
        # implicitly by the live-mode integration tests (out of unit scope).
        # Verify only the deterministic case-suffix derivation here via the
        # internal helper.
        from elif_v0_1.components.frame_validator import _case_suffix
        self.assertEqual(_case_suffix(None), "case_01")
        self.assertEqual(
            _case_suffix(_make_run_context(case_id="case_02_x")), "case_02"
        )


class TestSchemaValidationOnMalformedResponse(unittest.TestCase):
    """Fixture drift → SchemaValidationError surfaces through the component."""

    def setUp(self) -> None:
        reset_call_counter()

    def test_malformed_fixture_raises_schema_validation_error(self) -> None:
        # Create a temporary malformed fixture and point the adapter at it
        # by writing it into the fixtures dir under a unique stem, then
        # exercising the live call path through FrameValidator. We assert
        # SchemaValidationError surfaces unwrapped from the LLM adapter.
        fixtures_dir = (
            Path(__file__).resolve().parents[1] / "offline_fixtures"
        )
        malformed_stem = "step_01__case_99_malformed_test"
        malformed_path = fixtures_dir / f"{malformed_stem}.json"
        # Missing the required `reasoning` key — should fail step_1 schema.
        malformed_path.write_text(
            json.dumps({"verdict": "valid"}), encoding="utf-8"
        )
        try:
            # Patch _case_suffix so the component selects our malformed
            # fixture instead of case_01.
            with mock.patch(
                "elif_v0_1.components.frame_validator._case_suffix",
                return_value="case_99_malformed_test",
            ):
                fv = FrameValidator(_make_run_context())
                with self.assertRaises(SchemaValidationError):
                    fv.validate(_make_input_frame())
        finally:
            if malformed_path.exists():
                malformed_path.unlink()


if __name__ == "__main__":
    unittest.main()
