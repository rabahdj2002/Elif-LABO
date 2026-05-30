"""Tests for ProcedureRunner — 11-step orchestration.

Coverage:
    * end-to-end offline run for case_01 (governance refuse → Position B
      post-refusal closure: Step 10 + Step 11 fire; close emitted at
      end-of-run; exit_code=20)
    * step commit order (steps committed in 1..11 order, no skipping)
    * call-cap enforcement (LLMCallCapError → exit_code=30)
    * frame-invalid halt (Step 1 verdict=invalid → exit_code=10)
    * governance-refuse → Position B closure (Step 9 verdict=refuse →
      steps 10 + 11 still committed → exit_code=20)
    * memory logger event count includes open + step_committed + close
    * run_id uniqueness across runs
    * all 3 cases offline (case_01, case_02, case_03 each fire the Position
      B post-refusal closure path; the runner commits 11 envelopes for all
      three)
    * Position B explicit coverage: refutation emitted before step_10,
      close emitted after step_11, step_11 run_summary records
      post_refusal_closure=True on refuse-branch
    * RunReport shape (frozen dataclass; populated fields)
    * fresh per-run call counter (max_llm_calls cap applies per-run)

Position B was adjudicated 2026-05-30 (see notes/elif_g0_decision.md).
Refusal remains sovereign; the verdict in step_9 stays `refuse`; the
closed-set verdict vocabulary {constrain, refuse, explicitly_abstain}
is not modified. What changes is the post-Step-9 control-flow only.
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

    case_01's step_09 fixture has verdict=refuse. Under G0 Position B
    (adjudicated 2026-05-30), Step 10 fires with the constrained
    refusal-closure payload and Step 11 records the run summary; the
    refutation event is preserved and the close event moves to the end
    of the run. Exit code remains 20.
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

    def test_all_eleven_steps_are_committed_under_position_b(self) -> None:
        committed_ids = [env.step_id for env in self.report.step_outputs]
        self.assertEqual(committed_ids, list(PROCEDURE_STEP_IDS))

    def test_each_envelope_is_step_output_envelope(self) -> None:
        for env in self.report.step_outputs:
            self.assertIsInstance(env, StepOutputEnvelope)
            self.assertEqual(env.time_box_status, "within_budget")
            self.assertGreaterEqual(env.llm_calls_used, 0)

    def test_completed_at_iso_populated(self) -> None:
        self.assertTrue(self.report.completed_at_iso)
        # ISO timestamps end with Z in our format.
        self.assertTrue(self.report.completed_at_iso.endswith("Z"))

    def test_step_10_payload_is_constrained_refuse_bundle(self) -> None:
        # Position B: operative bucket is constrained to ["refuse bundle"];
        # theoretical bucket carries forward step_9 uncertainty sources.
        step_10_env = next(
            e for e in self.report.step_outputs if e.step_id == "step_10"
        )
        self.assertEqual(step_10_env.content.get("operative"), ["refuse bundle"])
        self.assertIsInstance(step_10_env.content.get("theoretical"), list)
        self.assertTrue(step_10_env.content.get("absence_log"))

    def test_step_11_run_summary_marks_post_refusal_closure(self) -> None:
        step_11_env = next(
            e for e in self.report.step_outputs if e.step_id == "step_11"
        )
        self.assertEqual(
            step_11_env.content.get("final_verdict"), "refuse"
        )
        self.assertTrue(
            step_11_env.content.get("post_refusal_closure")
        )


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
    """Step 9 verdict=refuse → Position B closure → exit_code=20.

    Real case_01 fixtures exercise this path. Under G0 Position B, all 11
    steps commit (Step 10 with constrained refusal-closure payload, Step 11
    with run summary), then close fires at end-of-run with exit_code=20.
    The verdict in step_9 remains `refuse`; the closed-set vocabulary is
    not expanded.
    """

    def test_governance_refuse_runs_position_b_closure(self) -> None:
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
        # Position B: all 11 steps commit; closure runs after refusal.
        self.assertEqual(len(report.step_outputs), 11)
        self.assertEqual(
            report.step_outputs[-1].step_id, "step_11"
        )
        # Step 9 verdict remains `refuse` — refusal is not transformed.
        step_9_env = next(
            e for e in report.step_outputs if e.step_id == "step_9"
        )
        self.assertEqual(step_9_env.content.get("verdict"), "refuse")


class TestRunnerMemoryLoggerEventCount(
    _TempPersistenceMixin, unittest.TestCase
):
    """Memory Logger events: 1 open + N step_committed + 0/1 refutation + 1 close."""

    def test_event_count_on_refuse_branch_includes_post_closure(self) -> None:
        runner = ProcedureRunner()
        report = runner.run(
            case_id="case_01_electroculture",
            condition="c",
            input_frame=_make_input_frame("case_01_electroculture"),
            offline_mode=True,
            max_llm_calls=22,
            results_dir=self.persistence_dir,
        )
        # Under Position B: 1 open + 11 step_committed + 1 step_7_modeB
        # (logged) + 1 refutation + 1 close = 15 (lower bound).
        self.assertGreaterEqual(
            report.memory_logger_entries_written, 14
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

    Each case has a step_09 fixture with verdict=refuse. Under G0
    Position B all three cases now commit 11 envelopes (Steps 1-9 + the
    post-refusal closure pair Step 10 + Step 11) and exit with code 20.
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

    def test_case_01_runs_position_b_closure(self) -> None:
        report = self._run_case("case_01_electroculture")
        self.assertEqual(report.exit_code, 20)
        self.assertEqual(len(report.step_outputs), 11)

    def test_case_02_runs_position_b_closure(self) -> None:
        report = self._run_case("case_02_policy_governance")
        self.assertEqual(report.exit_code, 20)
        self.assertEqual(len(report.step_outputs), 11)

    def test_case_03_runs_position_b_closure(self) -> None:
        report = self._run_case("case_03_operational_organizational")
        self.assertEqual(report.exit_code, 20)
        self.assertEqual(len(report.step_outputs), 11)


class TestRunnerPositionBEventOrdering(
    _TempPersistenceMixin, unittest.TestCase
):
    """G0 Position B event-ordering pinning (2026-05-30).

    Verifies that on a refuse-branch run the MemoryLogger event sequence is:
        open → step_committed(step_1..step_9) → step_committed(step_7_modeB)
        → refutation → step_committed(step_10) → step_committed(step_11)
        → close

    In particular: refutation precedes the post-closure pair, and the
    close event is the LAST event in the case log.
    """

    def _read_case_events(self) -> list[dict]:
        """Read the case event log written by MemoryLogger."""
        # Discover the case-log file under the temp persistence root.
        events: list[dict] = []
        for path in self.persistence_dir.rglob("*.jsonl"):
            with path.open() as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    events.append(json.loads(line))
        return events

    def test_close_event_is_last_under_position_b(self) -> None:
        runner = ProcedureRunner()
        runner.run(
            case_id="case_01_electroculture",
            condition="c",
            input_frame=_make_input_frame("case_01_electroculture"),
            offline_mode=True,
            max_llm_calls=22,
            results_dir=self.persistence_dir,
        )
        events = self._read_case_events()
        self.assertTrue(events, "expected at least one event written")
        event_types = [ev.get("event_type") for ev in events]
        # Last event is the close (Position B: end-of-run close).
        self.assertEqual(event_types[-1], "close")
        # Close exit_code is 20 on refuse-branch.
        self.assertEqual(events[-1].get("payload", {}).get("exit_code"), 20)

    def test_refutation_precedes_step_10_commit(self) -> None:
        runner = ProcedureRunner()
        runner.run(
            case_id="case_01_electroculture",
            condition="c",
            input_frame=_make_input_frame("case_01_electroculture"),
            offline_mode=True,
            max_llm_calls=22,
            results_dir=self.persistence_dir,
        )
        events = self._read_case_events()
        # Find first refutation event index.
        refutation_idx = next(
            (
                i for i, ev in enumerate(events)
                if ev.get("event_type") == "refutation"
            ),
            None,
        )
        self.assertIsNotNone(
            refutation_idx,
            "expected a refutation event on refuse-branch",
        )
        # Find first step_10 step_committed event index.
        step_10_idx = next(
            (
                i for i, ev in enumerate(events)
                if ev.get("event_type") == "step_committed"
                and ev.get("payload", {}).get("step_id") == "step_10"
            ),
            None,
        )
        self.assertIsNotNone(
            step_10_idx,
            "expected step_10 commit event on refuse-branch (Position B)",
        )
        # Refutation precedes step_10 commit.
        self.assertLess(refutation_idx, step_10_idx)


class TestRunnerCleanRunStillExits0(
    _TempPersistenceMixin, unittest.TestCase
):
    """Position B must not change the non-refuse path.

    When Step 9 returns `constrain` the runner still commits all 11 steps
    and exits with exit_code=0; the step_11 run_summary records
    post_refusal_closure=False.
    """

    def test_constrain_verdict_still_exits_0_and_marks_closure_false(self) -> None:
        from elif_v0_1.components import governance_kernel as gk_module

        constrain_payload = {
            "verdict": "constrain",
            "verdict_detail": "Authorize Family A research-only.",
            "confidence": "Medium",
            "unresolved_uncertainty_sources": ["regulatory_window"],
        }

        with mock.patch.object(
            gk_module,
            "complete_structured",
            side_effect=lambda *a, **kw: constrain_payload,
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

        self.assertEqual(report.exit_code, 0)
        self.assertEqual(len(report.step_outputs), 11)
        step_11_env = next(
            e for e in report.step_outputs if e.step_id == "step_11"
        )
        self.assertFalse(
            step_11_env.content.get("post_refusal_closure"),
            "constrain-branch must NOT mark post_refusal_closure=True",
        )


if __name__ == "__main__":
    unittest.main()
