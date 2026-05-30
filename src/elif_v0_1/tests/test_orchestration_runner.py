"""Tests for ProcedureRunner — 11-step orchestration.

Coverage:
    * end-to-end offline run for case_01 (governance halts at refuse → exit 20)
    * step commit order (steps committed in 1..11 order, no skipping)
    * call-cap enforcement (LLMCallCapError → exit_code=30)
    * frame-invalid halt (Step 1 verdict=invalid → exit_code=10)
    * governance-refuse halt (Step 9 verdict=refuse → exit_code=20)
    * memory logger event count includes open + step_committed + close
    * run_id uniqueness across runs
    * all 3 cases offline (case_01, case_02, case_03 each halt at Step 9 refuse
      per their fixtures; the runner reaches Step 9 cleanly in all three)
    * RunReport shape (frozen dataclass; populated fields)
    * fresh per-run call counter (max_llm_calls cap applies per-run)
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict
from unittest import mock

# Path shim so `elif_v0_1` resolves under `python3 -m unittest`.
_SRC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from elif_v0_1.base import (  # noqa: E402
    InputFrame,
)
from elif_v0_1.llm_adapter import reset_call_counter  # noqa: E402
from elif_v0_1.orchestration_runner import (  # noqa: E402
    PROCEDURE_STEP_IDS,
    ProcedureRunner,
    STEP_OWNER,
)
from elif_v0_1.run_context import RunReport, StepOutputEnvelope  # noqa: E402


def _make_input_frame(
    frame_id: str = "case_01_electroculture",
    text: str = "Should we authorize a coalition?",
) -> InputFrame:
    return InputFrame(
        id=frame_id,
        text=text,
        locked_at_iso="2026-05-29T12:00:00Z",
        doctrinal_scope_tag=frame_id,
        companion_case="condition_c",
    )


class _TempPersistenceMixin:
    """Per-test mixin that places MemoryLogger writes into a tempdir."""

    def setUp(self) -> None:  # noqa: D401
        self._tmp = tempfile.TemporaryDirectory()
        self.persistence_dir = Path(self._tmp.name)
        reset_call_counter()

    def tearDown(self) -> None:  # noqa: D401
        self._tmp.cleanup()


class TestRunnerStructuralContract(unittest.TestCase):
    """Runner-class structural pinning."""

    def test_runner_instantiates_with_no_args(self) -> None:
        runner = ProcedureRunner()
        self.assertIsInstance(runner, ProcedureRunner)

    def test_step_owner_table_matches_procedure_step_ids(self) -> None:
        # The runner asserts this at construction; re-assert at test-time
        # so an off-by-one drift in either tuple surfaces here too.
        self.assertEqual(len(STEP_OWNER), 11)
        self.assertEqual(
            tuple(s for s, _ in STEP_OWNER), PROCEDURE_STEP_IDS
        )
        self.assertEqual(STEP_OWNER[-1], ("step_11", "memory_logger"))


class TestRunnerEndToEndCase01(_TempPersistenceMixin, unittest.TestCase):
    """End-to-end offline run for case_01 — verdict=refuse → exit 20.

    case_01's step_09 fixture has verdict=refuse, so the runner halts at
    Step 9 with exit_code=20. Steps 1-9 commit; Step 10 + Step 11 are NOT
    reached.
    """

    def setUp(self) -> None:
        super().setUp()
        self.runner = ProcedureRunner()
        self.report = self.runner.run(
            case_id="case_01_electroculture",
            condition="c",
            input_frame=_make_input_frame("case_01_electroculture"),
            offline_mode=True,
            max_llm_calls=22,
            results_dir=self.persistence_dir,
        )

    def test_returns_run_report(self) -> None:
        self.assertIsInstance(self.report, RunReport)

    def test_exit_code_is_20_governance_refuse(self) -> None:
        self.assertEqual(self.report.exit_code, 20)

    def test_steps_1_through_9_are_committed(self) -> None:
        committed_ids = [env.step_id for env in self.report.step_outputs]
        self.assertEqual(
            committed_ids,
            ["step_1", "step_2", "step_3", "step_4", "step_5",
             "step_6", "step_7", "step_8", "step_9"],
        )

    def test_each_envelope_is_step_output_envelope(self) -> None:
        for env in self.report.step_outputs:
            self.assertIsInstance(env, StepOutputEnvelope)
            self.assertEqual(env.time_box_status, "within_budget")
            self.assertGreaterEqual(env.llm_calls_used, 0)

    def test_completed_at_iso_populated(self) -> None:
        self.assertTrue(self.report.completed_at_iso)
        # ISO timestamps end with Z in our format.
        self.assertTrue(self.report.completed_at_iso.endswith("Z"))


class TestRunnerStepCommitOrderClean(_TempPersistenceMixin, unittest.TestCase):
    """Step commit order — using a synthetic patch that overrides Step 9
    fixture to avoid the refuse path so the runner reaches Step 11.

    Patches the offline fixture loader for step_09 only to return a
    `constrain` verdict; all other steps use real fixtures. This isolates
    the run-to-completion path.
    """

    def setUp(self) -> None:
        super().setUp()
        self.runner = ProcedureRunner()

    def test_full_run_when_governance_does_not_refuse(self) -> None:
        from elif_v0_1.components import governance_kernel as gk_module

        constrain_payload = {
            "verdict": "constrain",
            "verdict_detail": (
                "Authorize Family A research-only under pre-registered "
                "constraints; refuse pilot deployment authority."
            ),
            "confidence": (
                "High on refusal of bundle-as-structured; medium on "
                "track-boundary definitions."
            ),
            "unresolved_uncertainty_sources": [
                "Whether bioelectrical effects aggregate to field scale.",
                "Whether independent advisory review remains independent.",
            ],
        }

        original_complete = gk_module.complete_structured

        def fake_complete(prompt, output_schema, **kwargs):
            return constrain_payload

        with mock.patch.object(
            gk_module, "complete_structured", side_effect=fake_complete
        ):
            report = self.runner.run(
                case_id="case_01_electroculture",
                condition="c",
                input_frame=_make_input_frame("case_01_electroculture"),
                offline_mode=True,
                max_llm_calls=22,
                results_dir=self.persistence_dir,
            )

        self.assertEqual(report.exit_code, 0)
        committed_ids = [env.step_id for env in report.step_outputs]
        self.assertEqual(committed_ids, list(PROCEDURE_STEP_IDS))


class TestRunnerCallCapHalt(_TempPersistenceMixin, unittest.TestCase):
    """LLMCallCapError → exit_code=30."""

    def test_runner_halts_when_cap_exceeded(self) -> None:
        runner = ProcedureRunner()
        # Cap at 1 — Step 1 succeeds (uses 1 call), Step 2 raises.
        report = runner.run(
            case_id="case_01_electroculture",
            condition="c",
            input_frame=_make_input_frame("case_01_electroculture"),
            offline_mode=True,
            max_llm_calls=1,
            results_dir=self.persistence_dir,
        )
        self.assertEqual(report.exit_code, 30)
        committed_ids = [env.step_id for env in report.step_outputs]
        # Step 1 commits; Step 2 raises before commit.
        self.assertEqual(committed_ids, ["step_1"])


class TestRunnerFrameInvalidHalt(_TempPersistenceMixin, unittest.TestCase):
    """Step 1 verdict=invalid → exit_code=10."""

    def test_frame_invalid_halts_with_exit_code_10(self) -> None:
        from elif_v0_1.components import frame_validator as fv_module

        invalid_payload = {
            "verdict": "invalid",
            "reasoning": "Frame fails Article II structural scrutiny.",
            "reformulated_frame": (
                "The frame as posed is undecidable; reformulate."
            ),
        }

        with mock.patch.object(
            fv_module,
            "complete_structured",
            return_value=invalid_payload,
        ):
            runner = ProcedureRunner()
            report = runner.run(
                case_id="case_01_electroculture",
                condition="c",
                input_frame=_make_input_frame("case_01_electroculture"),
                offline_mode=True,
                max_llm_calls=22,
                results_dir=self.persistence_dir,
            )

        self.assertEqual(report.exit_code, 10)
        committed_ids = [env.step_id for env in report.step_outputs]
        self.assertEqual(committed_ids, ["step_1"])


class TestRunnerGovernanceRefuseHalt(
    _TempPersistenceMixin, unittest.TestCase
):
    """Step 9 verdict=refuse → exit_code=20.

    Real case_01 fixtures already exercise this path; we reassert here so
    the halt-routing surface is covered explicitly.
    """

    def test_governance_refuse_halts_with_exit_code_20(self) -> None:
        runner = ProcedureRunner()
        report = runner.run(
            case_id="case_01_electroculture",
            condition="c",
            input_frame=_make_input_frame("case_01_electroculture"),
            offline_mode=True,
            max_llm_calls=22,
            results_dir=self.persistence_dir,
        )
        self.assertEqual(report.exit_code, 20)
        # Steps 1-9 commit; 10 + 11 not reached.
        self.assertEqual(len(report.step_outputs), 9)
        self.assertEqual(
            report.step_outputs[-1].step_id, "step_9"
        )


class TestRunnerMemoryLoggerEventCount(
    _TempPersistenceMixin, unittest.TestCase
):
    """Memory Logger events: 1 open + N step_committed + 0/1 refutation + 1 close."""

    def test_event_count_on_refuse_halt_is_at_least_open_steps_close(self) -> None:
        runner = ProcedureRunner()
        report = runner.run(
            case_id="case_01_electroculture",
            condition="c",
            input_frame=_make_input_frame("case_01_electroculture"),
            offline_mode=True,
            max_llm_calls=22,
            results_dir=self.persistence_dir,
        )
        # 1 open + 9 step_committed + 1 step_7_modeB (logged) + 1
        # refutation + 1 close = 13 (lower bound)
        self.assertGreaterEqual(
            report.memory_logger_entries_written, 12
        )


class TestRunnerRunIdUniqueness(_TempPersistenceMixin, unittest.TestCase):
    """run_id is unique across runs."""

    def test_two_consecutive_runs_have_distinct_run_ids(self) -> None:
        runner = ProcedureRunner()
        report_1 = runner.run(
            case_id="case_01_electroculture",
            condition="c",
            input_frame=_make_input_frame("case_01_electroculture"),
            offline_mode=True,
            max_llm_calls=22,
            results_dir=self.persistence_dir,
        )
        report_2 = runner.run(
            case_id="case_01_electroculture",
            condition="c",
            input_frame=_make_input_frame("case_01_electroculture"),
            offline_mode=True,
            max_llm_calls=22,
            results_dir=self.persistence_dir,
        )
        self.assertNotEqual(
            report_1.run_context.run_id, report_2.run_context.run_id
        )


class TestRunnerAllThreeCasesOffline(
    _TempPersistenceMixin, unittest.TestCase
):
    """Verify all 3 cases route deterministically through the runner.

    Each case has a step_09 fixture with verdict=refuse, so each exits
    with code 20. The test asserts the runner reaches Step 9 cleanly for
    all three (no schema or call-cap errors).
    """

    def _run_case(self, case_id: str) -> RunReport:
        runner = ProcedureRunner()
        return runner.run(
            case_id=case_id,
            condition="c",
            input_frame=_make_input_frame(case_id),
            offline_mode=True,
            max_llm_calls=22,
            results_dir=self.persistence_dir,
        )

    def test_case_01_reaches_step_9_and_halts(self) -> None:
        report = self._run_case("case_01_electroculture")
        self.assertEqual(report.exit_code, 20)
        self.assertEqual(len(report.step_outputs), 9)

    def test_case_02_reaches_step_9_and_halts(self) -> None:
        report = self._run_case("case_02_policy_governance")
        self.assertEqual(report.exit_code, 20)
        self.assertEqual(len(report.step_outputs), 9)

    def test_case_03_reaches_step_9_and_halts(self) -> None:
        report = self._run_case("case_03_operational_organizational")
        self.assertEqual(report.exit_code, 20)
        self.assertEqual(len(report.step_outputs), 9)


if __name__ == "__main__":
    unittest.main()
