"""Tests for the ObjectDecomposer component (Step 2 + Step 6 sub-behavior).

All tests run in offline_mode using the 11x3 fixture matrix shipped in
`offline_fixtures/`. No network call is ever made.

Coverage targets:
    * decompose returns a schema-valid Step 2 payload (offline).
    * multi_scale_relate returns a schema-valid Step 6 payload (offline).
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
    InputFrame,
    SchemaValidationError,
)
from elif_v0_1.components import object_decomposer as od_module  # noqa: E402
from elif_v0_1.components.object_decomposer import (  # noqa: E402
    ObjectDecomposer,
)
from elif_v0_1.llm_adapter import reset_call_counter  # noqa: E402
from elif_v0_1.run_context import RunContext  # noqa: E402


def _make_frame(text: str = "Should we authorize bundled electroculture pilots?") -> InputFrame:
    return InputFrame(
        id="frame_001",
        text=text,
        locked_at_iso="2026-05-29T12:00:00+00:00",
        doctrinal_scope_tag="agricultural_authorization",
        companion_case="case_01_electroculture",
    )


def _make_ctx(case_id: str = "case_01_electroculture", offline: bool = True) -> RunContext:
    return RunContext(
        case_id=case_id,
        condition="c",
        procedure_version="v1.0",
        offline_mode=offline,
        max_llm_calls=22,
        started_at_iso="2026-05-29T12:00:00+00:00",
        run_id="run_test_001",
    )


class TestObjectDecomposerArticleAndId(unittest.TestCase):
    """Doctrinal pins — component_id + Article tie are closed-set anchors."""

    def test_component_id_is_object_decomposer(self) -> None:
        self.assertEqual(ObjectDecomposer.component_id, "object_decomposer")

    def test_article_tie_is_iv(self) -> None:
        self.assertEqual(ObjectDecomposer.article_ties, ("IV",))


class TestDecomposeOffline(unittest.TestCase):
    """Step 2 family-axis decomposition (offline / fixture-driven)."""

    def setUp(self) -> None:
        reset_call_counter()
        self.decomposer = ObjectDecomposer()

    def test_returns_valid_shape(self) -> None:
        result = self.decomposer.decompose(
            _make_frame(),
            run_context=_make_ctx("case_01_electroculture"),
        )
        self.assertIsInstance(result, dict)
        self.assertIn("axes", result)
        self.assertGreaterEqual(len(result["axes"]), 1)
        for axis in result["axes"]:
            self.assertIn("axis_name", axis)
            self.assertIn("families", axis)
            self.assertGreaterEqual(len(axis["families"]), 2)

    def test_offline_is_deterministic(self) -> None:
        ctx = _make_ctx("case_01_electroculture")
        reset_call_counter()
        first = self.decomposer.decompose(_make_frame(), run_context=ctx)
        reset_call_counter()
        second = self.decomposer.decompose(_make_frame(), run_context=ctx)
        self.assertEqual(first, second)

    def test_resolves_all_three_cases(self) -> None:
        """Each of the 3 cases must yield a Step 2 fixture without drift."""
        for case_token in ("case_01", "case_02", "case_03"):
            with self.subTest(case=case_token):
                reset_call_counter()
                result = self.decomposer.decompose(
                    _make_frame(),
                    run_context=_make_ctx(case_token),
                )
                self.assertIn("axes", result)


class TestDecomposeInputValidation(unittest.TestCase):
    """Input-shape guards must fire BEFORE consuming an LLM call slot."""

    def setUp(self) -> None:
        reset_call_counter()
        self.decomposer = ObjectDecomposer()

    def test_non_input_frame_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.decomposer.decompose(
                "not an InputFrame",  # type: ignore[arg-type]
                run_context=_make_ctx(),
            )

    def test_non_run_context_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.decomposer.decompose(
                _make_frame(),
                run_context="not a RunContext",  # type: ignore[arg-type]
            )

    def test_bad_case_id_raises(self) -> None:
        ctx = _make_ctx("totally_malformed_no_case_token")
        with self.assertRaises(ELIFError):
            self.decomposer.decompose(_make_frame(), run_context=ctx)


class TestMultiScaleRelateOffline(unittest.TestCase):
    """Step 6 cross-scale-axis sub-behavior."""

    def setUp(self) -> None:
        reset_call_counter()
        self.decomposer = ObjectDecomposer()

    def _step2_for(self, case_id: str) -> dict:
        reset_call_counter()
        return self.decomposer.decompose(
            _make_frame(),
            run_context=_make_ctx(case_id),
        )

    def test_returns_valid_shape(self) -> None:
        step2 = self._step2_for("case_01_electroculture")
        reset_call_counter()
        result = self.decomposer.multi_scale_relate(
            step2,
            run_context=_make_ctx("case_01_electroculture"),
        )
        self.assertIn("scales", result)
        self.assertIn("cross_scale_relations", result)
        self.assertGreaterEqual(len(result["scales"]), 2)
        self.assertGreaterEqual(len(set(result["scales"])), 2)
        self.assertGreaterEqual(len(result["cross_scale_relations"]), 1)

    def test_rejects_non_dict_decomposition(self) -> None:
        with self.assertRaises(ELIFError):
            self.decomposer.multi_scale_relate(
                "not a dict",
                run_context=_make_ctx(),
            )

    def test_rejects_malformed_step2_input(self) -> None:
        """Step 2 dict missing `axes` must halt at the component boundary."""
        with self.assertRaises(ELIFError):
            self.decomposer.multi_scale_relate(
                {"something_else": []},
                run_context=_make_ctx(),
            )


class TestSchemaValidationOnMalformedResponse(unittest.TestCase):
    """If the adapter returns a malformed payload, ObjectDecomposer must
    surface SchemaValidationError rather than silently passing drift on."""

    def setUp(self) -> None:
        reset_call_counter()
        self.decomposer = ObjectDecomposer()
        self._original = od_module.complete_structured

    def tearDown(self) -> None:
        od_module.complete_structured = self._original

    def test_malformed_step2_response_raises(self) -> None:
        """Inject a payload missing the required `axes` key."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {"not_axes": []}

        od_module.complete_structured = _bad_complete
        with self.assertRaises(SchemaValidationError):
            self.decomposer.decompose(
                _make_frame(),
                run_context=_make_ctx(),
            )

    def test_step2_with_single_family_axis_raises(self) -> None:
        """An axis with < 2 families violates Step 2 semantics."""

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "axes": [
                    {
                        "axis_name": "x",
                        "families": [{"family_id": "A", "description": "lone"}],
                    }
                ]
            }

        od_module.complete_structured = _bad_complete
        with self.assertRaises(SchemaValidationError):
            self.decomposer.decompose(
                _make_frame(),
                run_context=_make_ctx(),
            )

    def test_step6_with_single_scale_raises(self) -> None:
        """A Step 6 payload with only one scale violates semantics."""
        step2_payload = {
            "axes": [
                {
                    "axis_name": "x",
                    "families": [
                        {"family_id": "A", "description": "a"},
                        {"family_id": "B", "description": "b"},
                    ],
                }
            ]
        }

        def _bad_complete(prompt, output_schema, *, max_calls,  # noqa: ANN001
                          offline_mode, offline_fixture_id, model_id=None):
            return {
                "scales": ["only-one"],
                "cross_scale_relations": ["x relates to nothing"],
            }

        od_module.complete_structured = _bad_complete
        with self.assertRaises(SchemaValidationError):
            self.decomposer.multi_scale_relate(
                step2_payload,
                run_context=_make_ctx(),
            )


class TestCaseTokenExtraction(unittest.TestCase):
    """Fixture routing must tolerate prose-form case_ids."""

    def test_extracts_case_01_from_prose_id(self) -> None:
        self.assertEqual(
            od_module._extract_case_token("case_01_electroculture"),
            "case_01",
        )

    def test_extracts_bare_case_token(self) -> None:
        self.assertEqual(
            od_module._extract_case_token("case_03"),
            "case_03",
        )

    def test_raises_on_unparseable_id(self) -> None:
        with self.assertRaises(ELIFError):
            od_module._extract_case_token("no_token_here")


if __name__ == "__main__":
    unittest.main()
