"""Tests for the LLM adapter — offline fixture mode + cap + schema validation.

These tests never touch the network. Live-mode coverage requires the
Anthropic SDK + an API key and is intentionally out of unit-test scope.
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

# Path shim so `elif_v0_1` resolves under `python3 -m unittest discover`.
_SRC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from elif_v0_1.base import (  # noqa: E402
    LLMAdapterError,
    LLMCallCapError,
    SchemaValidationError,
)
from elif_v0_1.llm_adapter import (  # noqa: E402
    DEFAULT_MODEL_ID,
    complete_structured,
    reset_call_counter,
    validate_against_schema,
)
from elif_v0_1.schemas import (  # noqa: E402
    STEP_SCHEMAS,
    schema_for,
)


_FIXTURE_DIR = Path(__file__).resolve().parents[1] / "offline_fixtures"


class TestOfflineFixtureLoading(unittest.TestCase):
    """Offline mode must be 100% deterministic and fixture-driven."""

    def setUp(self) -> None:
        reset_call_counter()

    def test_loads_step_01_case_01_fixture(self) -> None:
        schema = schema_for("step_1")
        result = complete_structured(
            prompt="ignored in offline mode",
            output_schema=schema,
            max_calls=22,
            offline_mode=True,
            offline_fixture_id="step_01__case_01",
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(result["verdict"], "needs_decomposition")
        self.assertIn("reasoning", result)

    def test_offline_mode_is_deterministic_across_calls(self) -> None:
        schema = schema_for("step_2")
        reset_call_counter()
        first = complete_structured(
            prompt="anything", output_schema=schema, max_calls=22,
            offline_mode=True, offline_fixture_id="step_02__case_02",
        )
        reset_call_counter()
        second = complete_structured(
            prompt="anything else", output_schema=schema, max_calls=22,
            offline_mode=True, offline_fixture_id="step_02__case_02",
        )
        self.assertEqual(first, second)

    def test_missing_fixture_id_raises(self) -> None:
        with self.assertRaises(LLMAdapterError):
            complete_structured(
                prompt="x", output_schema=schema_for("step_1"),
                max_calls=22, offline_mode=True, offline_fixture_id="",
            )

    def test_path_escaping_fixture_id_refused(self) -> None:
        with self.assertRaises(LLMAdapterError):
            complete_structured(
                prompt="x", output_schema=schema_for("step_1"),
                max_calls=22, offline_mode=True,
                offline_fixture_id="../../../etc/passwd",
            )

    def test_nonexistent_fixture_raises(self) -> None:
        with self.assertRaises(LLMAdapterError):
            complete_structured(
                prompt="x", output_schema=schema_for("step_1"),
                max_calls=22, offline_mode=True,
                offline_fixture_id="step_99__case_99",
            )

    def test_all_thirtythree_fixtures_present(self) -> None:
        """11 steps × 3 cases = 33 fixtures."""
        fixtures = sorted(_FIXTURE_DIR.glob("*.json"))
        self.assertEqual(len(fixtures), 33,
                         f"expected 33 fixtures; found {len(fixtures)}")

    def test_every_fixture_validates_against_its_step_schema(self) -> None:
        for step_num in range(1, 12):
            for case_num in ("01", "02", "03"):
                fid = f"step_{step_num:02d}__case_{case_num}"
                with self.subTest(fixture=fid):
                    path = _FIXTURE_DIR / f"{fid}.json"
                    self.assertTrue(path.is_file(), f"missing {path}")
                    with path.open() as fh:
                        payload = json.load(fh)
                    # Should not raise.
                    validate_against_schema(payload, schema_for(f"step_{step_num}"))


class TestCallCap(unittest.TestCase):
    """Step 8 §8.4: hard cap on per-run LLM calls."""

    def setUp(self) -> None:
        reset_call_counter()

    def test_call_counter_increments_on_each_call(self) -> None:
        schema = schema_for("step_1")
        for _ in range(3):
            complete_structured(
                prompt="x", output_schema=schema, max_calls=22,
                offline_mode=True, offline_fixture_id="step_01__case_01",
            )
        # 4th call still under cap; 22nd is the limit.
        complete_structured(
            prompt="x", output_schema=schema, max_calls=22,
            offline_mode=True, offline_fixture_id="step_01__case_01",
        )

    def test_call_cap_raises_when_exceeded(self) -> None:
        schema = schema_for("step_1")
        for _ in range(3):
            complete_structured(
                prompt="x", output_schema=schema, max_calls=3,
                offline_mode=True, offline_fixture_id="step_01__case_01",
            )
        # 4th call must raise.
        with self.assertRaises(LLMCallCapError):
            complete_structured(
                prompt="x", output_schema=schema, max_calls=3,
                offline_mode=True, offline_fixture_id="step_01__case_01",
            )

    def test_cap_of_one_allows_exactly_one_call(self) -> None:
        schema = schema_for("step_1")
        complete_structured(
            prompt="x", output_schema=schema, max_calls=1,
            offline_mode=True, offline_fixture_id="step_01__case_01",
        )
        with self.assertRaises(LLMCallCapError):
            complete_structured(
                prompt="x", output_schema=schema, max_calls=1,
                offline_mode=True, offline_fixture_id="step_01__case_01",
            )

    def test_invalid_max_calls_raises(self) -> None:
        schema = schema_for("step_1")
        with self.assertRaises(LLMAdapterError):
            complete_structured(
                prompt="x", output_schema=schema, max_calls=0,
                offline_mode=True, offline_fixture_id="step_01__case_01",
            )


class TestSchemaValidation(unittest.TestCase):
    """Schema validation is the structured-output contract enforcement."""

    def setUp(self) -> None:
        reset_call_counter()

    def test_valid_payload_passes(self) -> None:
        validate_against_schema(
            {"verdict": "valid", "reasoning": "trivial frame"},
            schema_for("step_1"),
        )

    def test_missing_required_key_raises(self) -> None:
        with self.assertRaises(SchemaValidationError):
            validate_against_schema({"verdict": "valid"}, schema_for("step_1"))

    def test_non_dict_payload_raises(self) -> None:
        with self.assertRaises(SchemaValidationError):
            validate_against_schema(["not", "a", "dict"], schema_for("step_1"))  # type: ignore[arg-type]


class TestModuleConstants(unittest.TestCase):
    """Doctrinal pins — model ID + schema coverage."""

    def test_default_model_is_claude_sonnet_4_6(self) -> None:
        # Step 8 §8.1 operator-approved model.
        self.assertEqual(DEFAULT_MODEL_ID, "claude-sonnet-4-6")

    def test_step_schemas_cover_all_eleven_steps(self) -> None:
        for i in range(1, 12):
            self.assertIn(f"step_{i}", STEP_SCHEMAS)
        self.assertEqual(len(STEP_SCHEMAS), 11)


if __name__ == "__main__":
    unittest.main()
