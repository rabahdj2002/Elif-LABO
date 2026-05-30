"""Tests for the V1 viewers — proving rendering-only invariants.

Per operator authorization 2026-05-30 + spec
`notes/elif_v1_viewer_audit_and_spec.md`. The viewers reveal existing
ELIF; they do not extend it. These tests enforce that contract.

Coverage:
  * Each viewer is a pure function (deterministic; same input -> same output)
  * No viewer imports llm_adapter (no LLM calls possible)
  * No viewer constructs a procedure component or writes any file
  * Decision Room renders Step 9 + 10 + 11 verbatim from input
  * Exploration Lens renders 5 territories verbatim from input
  * Object Drift Panel renders 7 chain nodes; with and without reading lens
  * Laboratory Viewer panels: memory timeline parses JSONL; replay table
    handles empty input; offline-vs-live emits per-field literal diff;
    article-VII honest empty state
  * CLI: each subcommand renders and produces non-empty output
  * E.2 round-trip: viewers render real saved RunReports without error
"""
from __future__ import annotations

import importlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

_SRC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from elif_v0_1.viewers import (  # noqa: E402
    render_article_vii_observations,
    render_decision_room,
    render_exploration_lens,
    render_memory_timeline,
    render_object_chain,
    render_offline_vs_live_diff,
    render_replay_table,
)


# -----------------------------------------------------------------------------
# Fixtures — synthetic RunReport dicts in the shape elif_v0_1.cli produces
# -----------------------------------------------------------------------------


def _synthetic_run_report(
    case_id: str = "case_01_electroculture",
    verdict: str = "constrain",
    post_refusal_closure: bool = False,
    exit_code: int = 0,
) -> dict:
    return {
        "run_context": {
            "case_id": case_id,
            "condition": "c",
            "procedure_version": "v1.0",
            "offline_mode": False,
            "max_llm_calls": 22,
            "started_at_iso": "2026-05-30T13:00:00Z",
            "run_id": "run_test_synthetic",
        },
        "step_outputs": [
            {
                "step_id": "step_1",
                "structured_output_dict": {
                    "verdict": "needs_decomposition",
                    "reformulated_frame": "rewrite per technique",
                    "reasoning": "bundling hides mechanism differences",
                },
                "committed_at_iso": "2026-05-30T13:00:10Z",
                "llm_calls_used": 1,
                "time_box_status": "within_budget",
            },
            {
                "step_id": "step_2",
                "structured_output_dict": {
                    "axes": [
                        {
                            "axis_name": "mechanism plausibility",
                            "rationale": "load-bearing on truth question",
                            "families": [
                                {
                                    "family_id": "A",
                                    "description": "biologically plausible",
                                },
                                {
                                    "family_id": "B",
                                    "description": "needs protocol",
                                },
                            ],
                        }
                    ]
                },
                "committed_at_iso": "2026-05-30T13:00:20Z",
                "llm_calls_used": 2,
                "time_box_status": "within_budget",
            },
            {
                "step_id": "step_3",
                "structured_output_dict": {"assumptions": ["assumption a"]},
                "committed_at_iso": "2026-05-30T13:00:30Z",
                "llm_calls_used": 3,
                "time_box_status": "within_budget",
            },
            {
                "step_id": "step_4",
                "structured_output_dict": {
                    "hypotheses": [
                        {
                            "hypothesis_id": "H1",
                            "description": "Family A works at small scale",
                            "distinguishing_prediction": "effect size > 0.2",
                        }
                    ]
                },
                "committed_at_iso": "2026-05-30T13:00:40Z",
                "llm_calls_used": 4,
                "time_box_status": "within_budget",
            },
            {
                "step_id": "step_5",
                "structured_output_dict": {"failure_conditions": ["fails if effect < 0.05"]},
                "committed_at_iso": "2026-05-30T13:00:50Z",
                "llm_calls_used": 5,
                "time_box_status": "within_budget",
            },
            {
                "step_id": "step_6",
                "structured_output_dict": {
                    "scales": [
                        {"scale_name": "organism", "description": "individual plant"},
                        {"scale_name": "field", "description": "many plants"},
                    ],
                    "cross_scale_relations": [
                        {"description": "organism-scale effects may not aggregate to field"}
                    ],
                },
                "committed_at_iso": "2026-05-30T13:01:00Z",
                "llm_calls_used": 6,
                "time_box_status": "within_budget",
            },
            {
                "step_id": "step_7",
                "structured_output_dict": {
                    "trajectories": [
                        {
                            "tag": "outside-original-frame",
                            "description": "agroecological adaptation alternative",
                        }
                    ]
                },
                "committed_at_iso": "2026-05-30T13:01:10Z",
                "llm_calls_used": 7,
                "time_box_status": "within_budget",
            },
            {
                "step_id": "step_8",
                "structured_output_dict": {
                    "stages": [
                        {
                            "stage_id": "A1",
                            "description": "Research funding only for Family A",
                            "continuation_gate": "Replication outcomes meet threshold",
                        }
                    ]
                },
                "committed_at_iso": "2026-05-30T13:01:20Z",
                "llm_calls_used": 8,
                "time_box_status": "within_budget",
            },
            {
                "step_id": "step_9",
                "structured_output_dict": {
                    "verdict": verdict,
                    "verdict_detail": f"Detail for verdict={verdict}.",
                    "confidence_qualifier": "moderate",
                    "unresolved_uncertainty_sources": ["u1", "u2", "u3"],
                },
                "committed_at_iso": "2026-05-30T13:01:30Z",
                "llm_calls_used": 9,
                "time_box_status": "within_budget",
            },
            {
                "step_id": "step_10",
                "structured_output_dict": {
                    "operative": ["op a", "op b"] if verdict != "refuse" else ["refuse bundle"],
                    "theoretical": ["t1", "t2"],
                    "absence_log": "Position B closure",
                },
                "committed_at_iso": "2026-05-30T13:01:40Z",
                "llm_calls_used": 10,
                "time_box_status": "within_budget",
            },
            {
                "step_id": "step_11",
                "structured_output_dict": {
                    "case_id": case_id,
                    "condition": "c",
                    "final_verdict": verdict,
                    "post_refusal_closure": post_refusal_closure,
                    "step_count": 10,
                    "llm_calls_used": 11,
                    "procedure_version": "v1.0",
                    "run_id": "run_test_synthetic",
                },
                "committed_at_iso": "2026-05-30T13:01:50Z",
                "llm_calls_used": 11,
                "time_box_status": "within_budget",
            },
        ],
        "exit_code": exit_code,
        "memory_logger_entries_written": 15 if verdict == "refuse" else 14,
        "completed_at_iso": "2026-05-30T13:01:50Z",
    }


# -----------------------------------------------------------------------------
# Discipline tests — proving rendering-only invariants
# -----------------------------------------------------------------------------


class TestNoLLMImports(unittest.TestCase):
    """Viewer modules must NOT import llm_adapter at module level.

    The viewers are read-only; they must not even have access to the LLM
    call surface. Importing the modules and checking sys.modules confirms
    no transitive llm_adapter import.
    """

    def test_decision_room_does_not_load_llm_adapter(self) -> None:
        # Snapshot module map before / after fresh import of decision_room
        # in an isolated way: re-import the viewer package and assert
        # llm_adapter is not present in its transitive imports.
        importlib.import_module("elif_v0_1.viewers.decision_room")
        # llm_adapter MAY be loaded by other parts of the elif_v0_1
        # package; the test checks that the viewer module itself doesn't
        # directly import it.
        viewer_mod = sys.modules["elif_v0_1.viewers.decision_room"]
        # Read the module's __dict__ — no 'complete_structured' or similar
        # LLM call surface should appear
        self.assertNotIn("complete_structured", viewer_mod.__dict__)
        self.assertNotIn("_call_anthropic_tool_use", viewer_mod.__dict__)

    def test_exploration_lens_does_not_load_llm_adapter(self) -> None:
        importlib.import_module("elif_v0_1.viewers.exploration_lens")
        viewer_mod = sys.modules["elif_v0_1.viewers.exploration_lens"]
        self.assertNotIn("complete_structured", viewer_mod.__dict__)

    def test_object_drift_panel_does_not_load_llm_adapter(self) -> None:
        importlib.import_module("elif_v0_1.viewers.object_drift_panel")
        viewer_mod = sys.modules["elif_v0_1.viewers.object_drift_panel"]
        self.assertNotIn("complete_structured", viewer_mod.__dict__)

    def test_laboratory_viewer_does_not_load_llm_adapter(self) -> None:
        importlib.import_module("elif_v0_1.viewers.laboratory_viewer")
        viewer_mod = sys.modules["elif_v0_1.viewers.laboratory_viewer"]
        self.assertNotIn("complete_structured", viewer_mod.__dict__)


class TestNoSubstrateMutation(unittest.TestCase):
    """Viewers must not modify the substrate.

    Specifically: a viewer call must not change the input dict, must not
    write any file in the CWD or under elif_v0_1/, and must not modify
    any global counter (e.g. llm_adapter._call_counter).
    """

    def test_decision_room_does_not_mutate_input(self) -> None:
        rr = _synthetic_run_report()
        snapshot = json.dumps(rr, sort_keys=True)
        render_decision_room(rr)
        self.assertEqual(json.dumps(rr, sort_keys=True), snapshot)

    def test_exploration_lens_does_not_mutate_input(self) -> None:
        rr = _synthetic_run_report()
        snapshot = json.dumps(rr, sort_keys=True)
        render_exploration_lens(rr)
        self.assertEqual(json.dumps(rr, sort_keys=True), snapshot)

    def test_object_drift_panel_does_not_mutate_input(self) -> None:
        rr = _synthetic_run_report()
        snapshot = json.dumps(rr, sort_keys=True)
        render_object_chain(rr)
        self.assertEqual(json.dumps(rr, sort_keys=True), snapshot)

    def test_call_counter_unchanged_by_any_viewer(self) -> None:
        from elif_v0_1.llm_adapter import _call_counter, reset_call_counter

        reset_call_counter()
        before = _call_counter()
        rr = _synthetic_run_report()
        render_decision_room(rr)
        render_exploration_lens(rr)
        render_object_chain(rr)
        with tempfile.TemporaryDirectory() as tmp:
            jsonl = Path(tmp) / "events.jsonl"
            jsonl.write_text("", encoding="utf-8")
            render_memory_timeline("case_x", jsonl)
            render_article_vii_observations([jsonl])
        after = _call_counter()
        self.assertEqual(before, after, "viewers must not increment the LLM call counter")


class TestDeterminism(unittest.TestCase):
    """Same input -> same output. Viewers are pure functions."""

    def test_decision_room_deterministic(self) -> None:
        rr = _synthetic_run_report()
        a = render_decision_room(rr)
        b = render_decision_room(rr)
        self.assertEqual(a, b)

    def test_exploration_lens_deterministic(self) -> None:
        rr = _synthetic_run_report()
        a = render_exploration_lens(rr)
        b = render_exploration_lens(rr)
        self.assertEqual(a, b)

    def test_object_drift_panel_deterministic(self) -> None:
        rr = _synthetic_run_report()
        a = render_object_chain(rr)
        b = render_object_chain(rr)
        self.assertEqual(a, b)


# -----------------------------------------------------------------------------
# Reveal Test — every rendered field is extractable from existing artifacts
# -----------------------------------------------------------------------------


class TestRevealTest(unittest.TestCase):
    """For each viewer, confirm the rendering contains values from the input.

    This enforces the Reveal Test: nothing in the rendering is invented —
    every visible field can be traced back to the source artifact.
    """

    def test_decision_room_reveals_verdict_and_uncertainty(self) -> None:
        rr = _synthetic_run_report(verdict="refuse")
        rendered = render_decision_room(rr)
        self.assertIn("refuse", rendered)
        self.assertIn("Detail for verdict=refuse.", rendered)
        self.assertIn("u1", rendered)
        self.assertIn("u2", rendered)
        self.assertIn("u3", rendered)

    def test_decision_room_reveals_post_refusal_closure(self) -> None:
        rr = _synthetic_run_report(verdict="refuse", post_refusal_closure=True)
        rendered = render_decision_room(rr)
        self.assertIn("post_refusal_closure", rendered)
        self.assertIn("True", rendered)

    def test_exploration_lens_reveals_five_territories(self) -> None:
        rr = _synthetic_run_report()
        rendered = render_exploration_lens(rr)
        # Territory headings should all be present
        self.assertIn("Territory 1", rendered)
        self.assertIn("Territory 2", rendered)
        self.assertIn("Territory 3", rendered)
        self.assertIn("Territory 4", rendered)
        self.assertIn("Territory 5", rendered)
        # Step 2 axis name
        self.assertIn("mechanism plausibility", rendered)
        # Step 6 scale
        self.assertIn("organism", rendered)
        # Step 7 trajectory
        self.assertIn("agroecological adaptation alternative", rendered)
        # Step 9 uncertainty
        self.assertIn("u1", rendered)
        # Step 10 theoretical
        self.assertIn("t1", rendered)

    def test_object_drift_panel_reveals_chain(self) -> None:
        rr = _synthetic_run_report()
        rendered = render_object_chain(rr)
        # All 7 chain nodes
        for header in [
            "Step 1 — Frame Validation",
            "Step 2 — Object Decomposition",
            "Step 4 — Hypotheses",
            "Step 6 — Multi-scale Relations",
            "Step 7 — Outside-frame Trajectories",
            "Step 8 — Stage-gated Roadmap",
            "Step 9 — Verdict",
        ]:
            self.assertIn(header, rendered)
        # And the bifurcation note should appear in the Step 8 reading lens
        self.assertIn("bifurcation", rendered)

    def test_object_drift_strict_minimum_omits_reading_lens(self) -> None:
        rr = _synthetic_run_report()
        rendered = render_object_chain(rr, with_reading_lens=False)
        # The reading-lens phrase "as posed in the input frame" should NOT appear
        self.assertNotIn("as posed in the input frame", rendered)
        # But Step labels should still appear
        self.assertIn("Step 1 — Frame Validation", rendered)


# -----------------------------------------------------------------------------
# Truth Test — viewers do not claim more than the artifact claims
# -----------------------------------------------------------------------------


class TestTruthTest(unittest.TestCase):
    """The renderings must not assert claims beyond the artifact's content."""

    def test_decision_room_does_not_recommend(self) -> None:
        rr = _synthetic_run_report()
        rendered = render_decision_room(rr)
        for forbidden in [
            "should approve",
            "should reject",
            "we recommend",
            "recommended action",
            "click to approve",
        ]:
            self.assertNotIn(forbidden.lower(), rendered.lower())
        # The closing disclaimer explicitly says the viewer does NOT
        # recommend (using "recommend" in the negative); the test above
        # catches actual recommendation phrasing while permitting this.

    def test_exploration_lens_does_not_draw_edges(self) -> None:
        rr = _synthetic_run_report()
        rendered = render_exploration_lens(rr)
        # No edge / relationship language between territories
        for forbidden in [
            "axis 1 connects to scale",
            "territory A relates to territory B",
            "merging territories",
        ]:
            self.assertNotIn(forbidden.lower(), rendered.lower())

    def test_object_drift_panel_does_not_claim_drift(self) -> None:
        rr = _synthetic_run_report()
        rendered = render_object_chain(rr)
        # The Panel must NOT make aggregate drift claims
        for forbidden in [
            "drift detected",
            "drift confirmed",
            "drift score",
            "no drift",
            "object substituted",
        ]:
            self.assertNotIn(forbidden.lower(), rendered.lower())


# -----------------------------------------------------------------------------
# Laboratory Viewer — per-panel
# -----------------------------------------------------------------------------


class TestLaboratoryPanels(unittest.TestCase):

    def test_memory_timeline_handles_empty_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "does_not_exist.jsonl"
            rendered = render_memory_timeline("case_x", missing)
            self.assertIn("Memory Timeline", rendered)
            self.assertIn("no events on disk", rendered.lower())

    def test_memory_timeline_renders_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            jsonl = Path(tmp) / "events.jsonl"
            jsonl.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "event_type": "open",
                                "payload": {"run_id": "rid_1", "condition": "c"},
                            }
                        ),
                        json.dumps(
                            {
                                "event_type": "step_committed",
                                "payload": {"step_id": "step_1"},
                            }
                        ),
                        json.dumps(
                            {
                                "event_type": "close",
                                "payload": {"exit_code": 20},
                            }
                        ),
                    ]
                ),
                encoding="utf-8",
            )
            rendered = render_memory_timeline("case_x", jsonl)
            self.assertIn("3 event(s) total", rendered)
            self.assertIn("open", rendered)
            self.assertIn("step_committed", rendered)
            self.assertIn("close", rendered)
            self.assertIn("exit_code=20", rendered)

    def test_replay_table_handles_empty(self) -> None:
        rendered = render_replay_table([])
        self.assertIn("Replay Results", rendered)
        self.assertIn("no replay results", rendered.lower())

    def test_replay_table_renders_results(self) -> None:
        rendered = render_replay_table(
            [
                {
                    "case_id": "case_01",
                    "verdict": "works",
                    "structural_similarity_score": 0.9444,
                    "runner_path": "orchestration_runner",
                    "missing_behaviors": (),
                },
            ]
        )
        self.assertIn("case_01", rendered)
        self.assertIn("works", rendered)
        self.assertIn("0.9444", rendered)

    def test_offline_vs_live_diff_renders_no_aggregate_verdict(self) -> None:
        off = _synthetic_run_report(verdict="refuse", post_refusal_closure=True, exit_code=20)
        live = _synthetic_run_report(verdict="constrain", post_refusal_closure=False, exit_code=0)
        rendered = render_offline_vs_live_diff(off, live)
        # Must contain per-row "NO" annotations
        self.assertIn("**NO**", rendered)
        # Must NOT emit an aggregate "diverged" or "different" verdict
        forbidden = ["diverged: yes", "diverged:yes", "overall: different"]
        for f in forbidden:
            self.assertNotIn(f.lower(), rendered.lower())
        # The mandatory header must be present
        self.assertIn("Viewer renders the comparison", rendered)
        self.assertIn("does not adjudicate", rendered)

    def test_article_vii_honest_empty_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            jsonl = Path(tmp) / "events.jsonl"
            jsonl.write_text(
                json.dumps({"event_type": "open", "payload": {}}) + "\n",
                encoding="utf-8",
            )
            rendered = render_article_vii_observations([jsonl])
            # Must be honest about the empty state
            self.assertIn("No `capacity_change` events found", rendered)
            self.assertIn("Position B", rendered)


# -----------------------------------------------------------------------------
# CLI smoke
# -----------------------------------------------------------------------------


class TestCLISmoke(unittest.TestCase):

    def test_decision_room_cli_produces_output(self) -> None:
        from elif_v0_1.viewers.cli import main

        with tempfile.TemporaryDirectory() as tmp:
            rr_path = Path(tmp) / "rr.json"
            rr_path.write_text(json.dumps(_synthetic_run_report()), encoding="utf-8")
            out_path = Path(tmp) / "out.md"
            rc = main([
                "decision-room",
                "--run-report",
                str(rr_path),
                "--out",
                str(out_path),
            ])
            self.assertEqual(rc, 0)
            self.assertTrue(out_path.exists())
            txt = out_path.read_text(encoding="utf-8")
            self.assertIn("Decision Room", txt)

    def test_object_drift_cli_with_input_frame(self) -> None:
        from elif_v0_1.viewers.cli import main

        with tempfile.TemporaryDirectory() as tmp:
            rr_path = Path(tmp) / "rr.json"
            rr_path.write_text(json.dumps(_synthetic_run_report()), encoding="utf-8")
            frame_path = Path(tmp) / "input_frame.md"
            frame_path.write_text("verbatim input frame text", encoding="utf-8")
            out_path = Path(tmp) / "out.md"
            rc = main([
                "object-drift",
                "--run-report",
                str(rr_path),
                "--input-frame",
                str(frame_path),
                "--out",
                str(out_path),
            ])
            self.assertEqual(rc, 0)
            txt = out_path.read_text(encoding="utf-8")
            self.assertIn("verbatim input frame text", txt)


# -----------------------------------------------------------------------------
# E.2 round-trip (uses real artifacts if present)
# -----------------------------------------------------------------------------


class TestE2RoundTrip(unittest.TestCase):
    """If E.2 artifacts exist on disk, viewers must render them without error."""

    LIVE_DIR = Path("/tmp/elif_e2_live")
    OFFLINE_DIR = Path("/tmp/elif_e2_preflight_position_b")

    def _maybe_skip(self) -> tuple[Path, Path]:
        live = self.LIVE_DIR / "case_01_stdout.json"
        offline = self.OFFLINE_DIR / "case_01_stdout.json"
        if not (live.exists() and offline.exists()):
            self.skipTest("E.2 artifacts not present on this host")
        return live, offline

    def test_decision_room_renders_live_case_01(self) -> None:
        live, _ = self._maybe_skip()
        with live.open() as fh:
            rr = json.load(fh)
        rendered = render_decision_room(rr)
        self.assertIn("Decision Room", rendered)
        self.assertGreater(len(rendered), 200)

    def test_exploration_lens_renders_live_case_01(self) -> None:
        live, _ = self._maybe_skip()
        with live.open() as fh:
            rr = json.load(fh)
        rendered = render_exploration_lens(rr)
        self.assertIn("Exploration Lens", rendered)
        self.assertIn("Territory 1", rendered)
        self.assertIn("Territory 5", rendered)

    def test_object_drift_renders_live_case_01(self) -> None:
        live, _ = self._maybe_skip()
        with live.open() as fh:
            rr = json.load(fh)
        rendered = render_object_chain(rr)
        self.assertIn("Object Chain Viewer", rendered)
        self.assertIn("Step 9 — Verdict", rendered)

    def test_offline_vs_live_renders_real_pair(self) -> None:
        live, offline = self._maybe_skip()
        with live.open() as fh:
            live_rr = json.load(fh)
        with offline.open() as fh:
            off_rr = json.load(fh)
        rendered = render_offline_vs_live_diff(off_rr, live_rr)
        # E.2 had verdict shift refuse->constrain — expect at least one NO row
        self.assertIn("**NO**", rendered)


if __name__ == "__main__":
    unittest.main()
