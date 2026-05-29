"""Tests for run_context dataclasses — shape, immutability, closed-set guards."""

from __future__ import annotations

import os
import sys
import unittest
from dataclasses import FrozenInstanceError

# Path shim so `elif_v0_1` resolves under `python3 -m unittest discover`.
_SRC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from elif_v0_1.run_context import (  # noqa: E402
    CONDITION_IDS,
    TIME_BOX_STATUSES,
    RunContext,
    RunReport,
    StepOutputEnvelope,
)


def _make_run_context(**overrides) -> RunContext:
    base = dict(
        case_id="case_01_electroculture",
        condition="c",
        procedure_version="v1.0",
        offline_mode=True,
        max_llm_calls=22,
        started_at_iso="2026-05-29T12:00:00Z",
        run_id="run_2026-05-29T12-00-00Z_abc",
    )
    base.update(overrides)
    return RunContext(**base)  # type: ignore[arg-type]


def _make_step_env(**overrides) -> StepOutputEnvelope:
    base = dict(
        step_id="step_1",
        content={"verdict": "valid"},
        committed_at_iso="2026-05-29T12:00:01Z",
        llm_calls_used=1,
        time_box_status="within_budget",
        structured_output_dict={"verdict": "valid", "reasoning": "ok"},
    )
    base.update(overrides)
    return StepOutputEnvelope(**base)  # type: ignore[arg-type]


class TestRunContext(unittest.TestCase):
    def test_construction_happy_path(self) -> None:
        ctx = _make_run_context()
        self.assertEqual(ctx.case_id, "case_01_electroculture")
        self.assertEqual(ctx.condition, "c")
        self.assertEqual(ctx.procedure_version, "v1.0")
        self.assertTrue(ctx.offline_mode)
        self.assertEqual(ctx.max_llm_calls, 22)

    def test_frozen_dataclass_rejects_mutation(self) -> None:
        ctx = _make_run_context()
        with self.assertRaises(FrozenInstanceError):
            ctx.case_id = "case_02"  # type: ignore[misc]

    def test_invalid_condition_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _make_run_context(condition="z")

    def test_empty_case_id_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _make_run_context(case_id="")

    def test_negative_max_calls_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _make_run_context(max_llm_calls=0)

    def test_condition_closed_set_size(self) -> None:
        self.assertEqual(set(CONDITION_IDS), {"a", "b", "c"})


class TestStepOutputEnvelope(unittest.TestCase):
    def test_construction_happy_path(self) -> None:
        env = _make_step_env()
        self.assertEqual(env.step_id, "step_1")
        self.assertEqual(env.llm_calls_used, 1)
        self.assertEqual(env.time_box_status, "within_budget")

    def test_invalid_step_id_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _make_step_env(step_id="step_99")

    def test_invalid_time_box_status_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _make_step_env(time_box_status="meh")

    def test_negative_llm_calls_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _make_step_env(llm_calls_used=-1)

    def test_time_box_status_closed_set(self) -> None:
        self.assertEqual(
            set(TIME_BOX_STATUSES),
            {"within_budget", "exceeded_budget", "aborted"},
        )

    def test_frozen_dataclass(self) -> None:
        env = _make_step_env()
        with self.assertRaises(FrozenInstanceError):
            env.step_id = "step_2"  # type: ignore[misc]


class TestRunReport(unittest.TestCase):
    def test_empty_report_construction(self) -> None:
        ctx = _make_run_context()
        report = RunReport(
            run_context=ctx,
            step_outputs=tuple(),
            memory_logger_entries_written=0,
            exit_code=0,
            completed_at_iso="2026-05-29T12:05:00Z",
        )
        self.assertIs(report.run_context, ctx)
        self.assertEqual(report.step_outputs, tuple())
        self.assertEqual(report.exit_code, 0)

    def test_report_with_step_outputs(self) -> None:
        ctx = _make_run_context()
        env = _make_step_env()
        report = RunReport(
            run_context=ctx,
            step_outputs=(env,),
            memory_logger_entries_written=1,
            exit_code=0,
            completed_at_iso="2026-05-29T12:05:00Z",
        )
        self.assertEqual(len(report.step_outputs), 1)
        self.assertIs(report.step_outputs[0], env)

    def test_invalid_run_context_type_rejected(self) -> None:
        with self.assertRaises(ValueError):
            RunReport(
                run_context="not-a-context",  # type: ignore[arg-type]
                step_outputs=tuple(),
            )

    def test_step_outputs_must_be_tuple(self) -> None:
        ctx = _make_run_context()
        with self.assertRaises(ValueError):
            RunReport(
                run_context=ctx,
                step_outputs=[_make_step_env()],  # type: ignore[arg-type]
            )

    def test_frozen_report(self) -> None:
        ctx = _make_run_context()
        report = RunReport(run_context=ctx)
        with self.assertRaises(FrozenInstanceError):
            report.exit_code = 1  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
