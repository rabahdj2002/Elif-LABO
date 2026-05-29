"""Schema tests — verify the load-bearing JSON contracts.

If `jsonschema` is installed, performs a Draft 2020-12 validation against
sample documents. Otherwise falls back to a structural check that the
schema objects are well-formed dicts with required keys.
"""

from __future__ import annotations

import os
import sys
import unittest

# Path shim: make `elif_v0_1` importable when run via
# `python3 -m unittest discover -s src/elif_v0_1/tests`.
_SRC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from elif_v0_1.schemas import (  # noqa: E402
    ARTICLE_VII_TRACKING_SCHEMA,
    INPUT_FRAME_SCHEMA,
    JSON_SCHEMA_DIALECT,
    MEMORY_LOGGER_CORRECTION_SCHEMA,
    MEMORY_LOGGER_EVENT_SCHEMA,
    PROCEDURE_STEP_OUTPUT_SCHEMA,
)


try:
    import jsonschema  # type: ignore

    _HAS_JSONSCHEMA = True
except ImportError:  # pragma: no cover
    _HAS_JSONSCHEMA = False


ALL_SCHEMAS = (
    ("INPUT_FRAME_SCHEMA", INPUT_FRAME_SCHEMA),
    ("PROCEDURE_STEP_OUTPUT_SCHEMA", PROCEDURE_STEP_OUTPUT_SCHEMA),
    ("ARTICLE_VII_TRACKING_SCHEMA", ARTICLE_VII_TRACKING_SCHEMA),
    ("MEMORY_LOGGER_EVENT_SCHEMA", MEMORY_LOGGER_EVENT_SCHEMA),
    ("MEMORY_LOGGER_CORRECTION_SCHEMA", MEMORY_LOGGER_CORRECTION_SCHEMA),
)


class TestSchemaStructure(unittest.TestCase):
    """Structural sanity — required keys present, dialect declared."""

    def test_dialect_constant_set(self) -> None:
        self.assertIn("json-schema.org", JSON_SCHEMA_DIALECT)

    def test_every_schema_declares_dialect(self) -> None:
        for name, schema in ALL_SCHEMAS:
            with self.subTest(schema=name):
                self.assertEqual(schema.get("$schema"), JSON_SCHEMA_DIALECT)

    def test_every_schema_has_title_and_type_object(self) -> None:
        for name, schema in ALL_SCHEMAS:
            with self.subTest(schema=name):
                self.assertIn("title", schema)
                self.assertEqual(schema.get("type"), "object")

    def test_every_schema_pins_required_fields(self) -> None:
        for name, schema in ALL_SCHEMAS:
            with self.subTest(schema=name):
                self.assertIn("required", schema)
                self.assertIsInstance(schema["required"], list)
                self.assertGreater(len(schema["required"]), 0)

    def test_procedure_step_output_enum_eleven_steps(self) -> None:
        step_enum = PROCEDURE_STEP_OUTPUT_SCHEMA["properties"]["step_id"][
            "enum"
        ]
        self.assertEqual(len(step_enum), 11)

    def test_memory_logger_event_enum_closed_set(self) -> None:
        event_enum = MEMORY_LOGGER_EVENT_SCHEMA["properties"]["event_type"][
            "enum"
        ]
        self.assertEqual(
            set(event_enum),
            {
                "step_committed",
                "frame_locked",
                "verdict_emitted",
                "uncertainty_recorded",
                "reuse_detected",
            },
        )


@unittest.skipUnless(_HAS_JSONSCHEMA, "jsonschema not installed")
class TestSchemaValidatesSample(unittest.TestCase):
    """Round-trip validation when jsonschema is available."""

    def test_input_frame_sample_validates(self) -> None:
        sample = {
            "id": "case_01",
            "text": "Sample frame text",
            "locked_at_iso": "2026-05-29T00:00:00Z",
            "doctrinal_scope_tag": "elif_v0_1",
            "companion_case": "case_01",
        }
        jsonschema.validate(sample, INPUT_FRAME_SCHEMA)  # type: ignore[name-defined]

    def test_procedure_step_output_sample_validates(self) -> None:
        sample = {
            "step_id": "step_1",
            "content": {"verdict": "valid"},
            "committed_at_iso": "2026-05-29T00:00:00Z",
            "time_box_status": "within_budget",
        }
        jsonschema.validate(  # type: ignore[name-defined]
            sample, PROCEDURE_STEP_OUTPUT_SCHEMA
        )

    def test_article_vii_sample_validates(self) -> None:
        sample = {
            "case_id": "case_01",
            "prior_structures_referenced": ["case_00"],
            "reuse_count_total": 1,
            "patterns_recognized": ["frame_collapse"],
            "time_delta_vs_prior_similar": 0.0,
        }
        jsonschema.validate(  # type: ignore[name-defined]
            sample, ARTICLE_VII_TRACKING_SCHEMA
        )


if __name__ == "__main__":
    unittest.main()
