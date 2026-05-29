"""Closed-set discipline tests — doctrinal cardinality enforcement.

Per CLAUDE.md "Closed-set discipline (DOCTRINAL)" and Step 8 §1.
These tests fail loudly if any closed-set drifts from doctrine.
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

from elif_v0_1 import (  # noqa: E402
    ARTICLE_IDS,
    COMPONENT_IDS,
    FAILURE_MODE_POLES,
    PROCEDURE_STEP_IDS,
    assert_consistent,
)


class TestComponentIDsClosedSet(unittest.TestCase):
    def test_component_ids_exactly_seven(self) -> None:
        self.assertEqual(
            len(COMPONENT_IDS),
            7,
            "COMPONENT_IDS must be exactly 7 — Step 8 §1 no 8th component",
        )

    def test_component_ids_unique(self) -> None:
        self.assertEqual(len(set(COMPONENT_IDS)), len(COMPONENT_IDS))

    def test_component_ids_canonical_set(self) -> None:
        expected = {
            "frame_validator",
            "object_decomposer",
            "hypothesis_validator",
            "branching_roadmap_engine",
            "governance_kernel",
            "operative_truth_separator",
            "memory_logger",
        }
        self.assertEqual(set(COMPONENT_IDS), expected)

    def test_no_eighth_component_snuck_in(self) -> None:
        forbidden = {
            "assumption_surfacer",
            "cross_scale_relator",
            "world_model",
            "continuity_layer",
            "memory_corridor",
        }
        self.assertEqual(
            forbidden.intersection(COMPONENT_IDS),
            set(),
            "Step 8 §1 Q3.1+Q6.1: 8th component is permanently rejected",
        )


class TestProcedureStepIDsClosedSet(unittest.TestCase):
    def test_procedure_step_ids_exactly_eleven(self) -> None:
        self.assertEqual(
            len(PROCEDURE_STEP_IDS),
            11,
            "PROCEDURE_STEP_IDS must be exactly 11 — Step 8 compression",
        )

    def test_procedure_step_ids_unique(self) -> None:
        self.assertEqual(
            len(set(PROCEDURE_STEP_IDS)), len(PROCEDURE_STEP_IDS)
        )

    def test_procedure_step_ids_canonical_naming(self) -> None:
        expected = tuple(f"step_{i}" for i in range(1, 12))
        self.assertEqual(PROCEDURE_STEP_IDS, expected)

    def test_no_twelfth_step(self) -> None:
        self.assertNotIn("step_12", PROCEDURE_STEP_IDS)


class TestArticleIDsClosedSet(unittest.TestCase):
    def test_article_ids_exactly_seven(self) -> None:
        self.assertEqual(
            len(ARTICLE_IDS),
            7,
            "ARTICLE_IDS must be 7 — Constitutional Layer v0.4 LOCKED",
        )

    def test_article_ids_roman_one_through_seven(self) -> None:
        self.assertEqual(
            ARTICLE_IDS, ("I", "II", "III", "IV", "V", "VI", "VII")
        )


class TestFailureModePolesClosedSet(unittest.TestCase):
    def test_failure_mode_poles_exactly_four(self) -> None:
        self.assertEqual(
            len(FAILURE_MODE_POLES),
            4,
            "FAILURE_MODE_POLES must be 4 — v0.4 four-pole taxonomy",
        )

    def test_failure_mode_poles_canonical(self) -> None:
        expected = {
            "absolutization",
            "false_closure",
            "fragmentation",
            "sterile_equilibrium",
        }
        self.assertEqual(set(FAILURE_MODE_POLES), expected)


class TestAssertConsistentGuard(unittest.TestCase):
    def test_assert_consistent_passes_at_import(self) -> None:
        # If import succeeded, this is already true; call it again to confirm
        # the function is exposed and idempotent.
        assert_consistent()


if __name__ == "__main__":
    unittest.main()
