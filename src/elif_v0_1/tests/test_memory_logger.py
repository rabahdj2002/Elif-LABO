"""Tests for the MemoryLogger component — Step 11 + Article VII.

MemoryLogger is the ONLY architecture-dependent component in v0.1
(decision §8.10). No LLM calls, no fixtures: behavior is JSONL persistence
+ cross-case aggregation. Tests use tempfile for an isolated persistence
surface so they cannot collide with the on-disk `results/` directory.

Coverage targets (mirroring test_frame_validator + test_object_decomposer):
    * returns_valid_shape — write_event, read_case_state, metrics
    * append_is_deterministic + replay is in commit order
    * invalid_input_raises — bad case_id / bad event_type / non-InputFrame
    * correction model — supersession marks event; original NEVER mutated
    * reuse candidates — cross-case Jaccard scoring sorts descending
    * sterile-equilibrium signature — flagged on empty-capacity windows
    * closed-set discipline on event_type
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Path shim so `elif_v0_1` resolves under `python3 -m unittest discover`.
_SRC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from elif_v0_1.base import ELIFError, InputFrame  # noqa: E402
from elif_v0_1.components.memory_logger import (  # noqa: E402
    MemoryLogger,
    _VALID_EVENT_TYPES,
)


def _make_input_frame(text: str = "Authorize bundled electroculture pilots in drought regions?") -> InputFrame:
    return InputFrame(
        id="frame_001",
        text=text,
        locked_at_iso="2026-05-30T00:00:00Z",
        doctrinal_scope_tag="case_01_electroculture",
        companion_case="condition_c",
    )


class TestMemoryLoggerClassContract(unittest.TestCase):
    """Pinned scaffold contract — component_id + article tie + ctor shape."""

    def test_component_id_is_memory_logger(self) -> None:
        self.assertEqual(MemoryLogger.component_id, "memory_logger")

    def test_article_tie_is_vii(self) -> None:
        self.assertEqual(MemoryLogger.article_ties, ("VII",))

    def test_constructs_with_no_args(self) -> None:
        # Orchestrator constructs `MemoryLogger()` in scaffold wiring.
        MemoryLogger()

    def test_constructs_with_explicit_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as base:
            MemoryLogger(
                results_dir=base,
                base_persistence_dir=os.path.join(base, "events"),
            )


class _TempPersistenceBase(unittest.TestCase):
    """Mixin: every test gets an isolated persistence dir."""

    def setUp(self) -> None:
        self._tempdir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self._tempdir.name) / "events"
        self.logger = MemoryLogger(base_persistence_dir=self.base_dir)

    def tearDown(self) -> None:
        self._tempdir.cleanup()


class TestWriteEvent(_TempPersistenceBase):
    """write_event: shape validation + append-only persistence."""

    def test_returns_event_dict_with_backfilled_ids(self) -> None:
        out = self.logger.write_event(
            "case_01",
            {"event_type": "step_committed", "payload": {"step_id": "step_1"}},
        )
        self.assertIn("event_id", out)
        self.assertIn("committed_at_iso", out)
        self.assertEqual(out["case_id"], "case_01")
        self.assertEqual(out["event_type"], "step_committed")

    def test_persists_jsonl_one_line_per_call(self) -> None:
        self.logger.write_event(
            "case_01",
            {"event_type": "step_committed", "payload": {"step_id": "step_1"}},
        )
        self.logger.write_event(
            "case_01",
            {"event_type": "step_committed", "payload": {"step_id": "step_2"}},
        )
        path = self.base_dir / "case_01" / "article_vii_tracking.jsonl"
        with path.open("r", encoding="utf-8") as fh:
            lines = [line for line in fh if line.strip()]
        self.assertEqual(len(lines), 2)
        # Both lines must parse to dicts.
        for line in lines:
            self.assertIsInstance(json.loads(line), dict)

    def test_invalid_event_type_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.logger.write_event(
                "case_01",
                {"event_type": "totally_made_up", "payload": {}},
            )

    def test_invalid_case_id_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.logger.write_event(
                "",
                {"event_type": "step_committed", "payload": {}},
            )

    def test_path_traversal_case_id_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.logger.write_event(
                "../escape",
                {"event_type": "step_committed", "payload": {}},
            )

    def test_non_mapping_event_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.logger.write_event("case_01", "not a mapping")  # type: ignore[arg-type]

    def test_non_mapping_payload_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.logger.write_event(
                "case_01",
                {"event_type": "step_committed", "payload": "not a dict"},
            )


class TestReadCaseState(_TempPersistenceBase):
    """read_case_state replays events deterministically."""

    def test_returns_valid_shape(self) -> None:
        self.logger.write_event(
            "case_01",
            {"event_type": "step_committed", "payload": {"step_id": "step_1"}},
        )
        self.logger.write_event(
            "case_01",
            {"event_type": "capacity_change", "payload": {}},
        )
        state = self.logger.read_case_state("case_01")
        self.assertEqual(state["case_id"], "case_01")
        self.assertEqual(state["event_count"], 2)
        self.assertEqual(len(state["events_in_order"]), 2)
        self.assertEqual(state["event_type_counts"]["step_committed"], 1)
        self.assertEqual(state["event_type_counts"]["capacity_change"], 1)

    def test_missing_case_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.logger.read_case_state("does_not_exist")

    def test_replay_order_is_append_order(self) -> None:
        for step_id in ("step_1", "step_2", "step_3"):
            self.logger.write_event(
                "case_01",
                {"event_type": "step_committed", "payload": {"step_id": step_id}},
            )
        state = self.logger.read_case_state("case_01")
        steps_seen = [
            ev["payload"]["step_id"] for ev in state["events_in_order"]
        ]
        self.assertEqual(steps_seen, ["step_1", "step_2", "step_3"])


class TestEmitCorrection(_TempPersistenceBase):
    """Correction model: new event supersedes; original is NEVER mutated."""

    def test_correction_appends_new_event_and_marks_supersession(self) -> None:
        original = self.logger.write_event(
            "case_01",
            {"event_type": "verdict_emitted", "payload": {"verdict": "valid"}},
        )
        original_line = self._read_raw_line("case_01", 0)

        correction = self.logger.emit_correction(
            "case_01",
            original["event_id"],
            {"new_verdict": "invalid", "rationale": "missed Article II tie"},
        )
        self.assertEqual(correction["event_type"], "correction")
        self.assertEqual(
            correction["supersedes_event_id"], original["event_id"]
        )

        # Original line on disk MUST be byte-identical after correction.
        original_line_after = self._read_raw_line("case_01", 0)
        self.assertEqual(original_line, original_line_after)

        # read_case_state filters superseded id from latest_events but
        # preserves it in events_in_order.
        state = self.logger.read_case_state("case_01")
        latest_ids = [ev["event_id"] for ev in state["latest_events"]]
        self.assertNotIn(original["event_id"], latest_ids)
        self.assertIn(correction["event_id"], latest_ids)
        in_order_ids = [ev["event_id"] for ev in state["events_in_order"]]
        self.assertIn(original["event_id"], in_order_ids)

    def test_correction_with_unknown_target_raises(self) -> None:
        self.logger.write_event(
            "case_01",
            {"event_type": "step_committed", "payload": {}},
        )
        with self.assertRaises(ELIFError):
            self.logger.emit_correction(
                "case_01", "evt_nonexistent_id", {"k": "v"}
            )

    def test_correction_on_missing_case_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.logger.emit_correction("case_99", "evt_x", {"k": "v"})

    def test_correction_payload_must_be_mapping(self) -> None:
        original = self.logger.write_event(
            "case_01",
            {"event_type": "step_committed", "payload": {}},
        )
        with self.assertRaises(ELIFError):
            self.logger.emit_correction(
                "case_01", original["event_id"], "not a mapping"  # type: ignore[arg-type]
            )

    def _read_raw_line(self, case_id: str, line_index: int) -> str:
        path = self.base_dir / case_id / "article_vii_tracking.jsonl"
        with path.open("r", encoding="utf-8") as fh:
            return fh.readlines()[line_index]


class TestFindReuseCandidates(_TempPersistenceBase):
    """Cross-case Jaccard reuse detection."""

    def test_returns_empty_list_when_no_prior_cases(self) -> None:
        out = self.logger.find_reuse_candidates(_make_input_frame())
        self.assertEqual(out, [])

    def test_scores_descending(self) -> None:
        # Case A: events mentioning electroculture (high token overlap).
        self.logger.write_event(
            "case_01",
            {
                "event_type": "pattern_recognized",
                "payload": {
                    "pattern_id": "p1",
                    "description": "Authorize bundled electroculture pilots drought",
                },
            },
        )
        # Case B: events mentioning unrelated content.
        self.logger.write_event(
            "case_02",
            {
                "event_type": "pattern_recognized",
                "payload": {
                    "pattern_id": "p2",
                    "description": "carbon capture sequestration governance",
                },
            },
        )
        out = self.logger.find_reuse_candidates(
            "electroculture pilots drought authorize"
        )
        self.assertEqual(len(out), 2)
        # Descending sort: case_01 first.
        self.assertEqual(out[0][0], "case_01")
        self.assertGreaterEqual(out[0][1], out[1][1])

    def test_accepts_input_frame_or_str(self) -> None:
        self.logger.write_event(
            "case_01",
            {"event_type": "step_committed", "payload": {"step_id": "step_1"}},
        )
        out_str = self.logger.find_reuse_candidates("step_committed step_1")
        out_frame = self.logger.find_reuse_candidates(
            _make_input_frame(text="step_committed step_1")
        )
        # Same case_id appears in both; scores need not match because
        # tokenization treats the frame text equally — just assert shape.
        self.assertEqual([c[0] for c in out_str], [c[0] for c in out_frame])

    def test_non_str_non_frame_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.logger.find_reuse_candidates(42)  # type: ignore[arg-type]

    def test_empty_text_raises(self) -> None:
        with self.assertRaises(ELIFError):
            self.logger.find_reuse_candidates("   ")


class TestComputeCapacityMetrics(_TempPersistenceBase):
    """Capacity metrics aggregate across all known cases."""

    def test_empty_dir_returns_zeros(self) -> None:
        out = self.logger.compute_capacity_metrics()
        self.assertEqual(out["total_events"], 0)
        self.assertEqual(out["capacity_change_records"], 0)
        self.assertEqual(out["reuse_count_total"], 0)
        self.assertEqual(out["patterns_recognized"], 0)
        self.assertEqual(out["cases_observed"], 0)

    def test_counts_event_types_per_case(self) -> None:
        self.logger.write_event(
            "case_01",
            {"event_type": "capacity_change", "payload": {}},
        )
        self.logger.write_event(
            "case_01",
            {"event_type": "reuse_detected", "payload": {}},
        )
        self.logger.write_event(
            "case_02",
            {"event_type": "pattern_recognized", "payload": {}},
        )
        out = self.logger.compute_capacity_metrics()
        self.assertEqual(out["total_events"], 3)
        self.assertEqual(out["capacity_change_records"], 1)
        self.assertEqual(out["reuse_count_total"], 1)
        self.assertEqual(out["patterns_recognized"], 1)
        self.assertEqual(out["cases_observed"], 2)
        self.assertIn("case_01", out["per_case"])
        self.assertIn("case_02", out["per_case"])


class TestDetectSterileEquilibrium(_TempPersistenceBase):
    """Article VII sterile-equilibrium signature."""

    def test_flag_set_when_only_neutral_events(self) -> None:
        # Three step_committed events; no capacity_change, no reuse, no patterns.
        for step_id in ("step_1", "step_2", "step_3"):
            self.logger.write_event(
                "case_01",
                {
                    "event_type": "step_committed",
                    "payload": {"step_id": step_id},
                },
            )
        verdict = self.logger.detect_sterile_equilibrium("case_01")
        self.assertTrue(verdict["sterile_equilibrium"])
        self.assertEqual(verdict["scope"], "case")

    def test_flag_clears_when_capacity_change_present(self) -> None:
        self.logger.write_event(
            "case_01",
            {"event_type": "capacity_change", "payload": {}},
        )
        verdict = self.logger.detect_sterile_equilibrium("case_01")
        self.assertFalse(verdict["sterile_equilibrium"])
        self.assertEqual(verdict["signals"]["capacity_change_records"], 1)

    def test_cross_case_scope_when_no_case_id(self) -> None:
        self.logger.write_event(
            "case_01",
            {"event_type": "step_committed", "payload": {"s": 1}},
        )
        self.logger.write_event(
            "case_02",
            {"event_type": "step_committed", "payload": {"s": 1}},
        )
        verdict = self.logger.detect_sterile_equilibrium()
        self.assertEqual(verdict["scope"], "cross_case")
        self.assertIsNone(verdict["case_id"])
        self.assertEqual(verdict["signals"]["total_events"], 2)

    def test_no_flag_on_empty_log_window(self) -> None:
        # Zero events → cannot diagnose sterile equilibrium.
        verdict = self.logger.detect_sterile_equilibrium()
        self.assertFalse(verdict["sterile_equilibrium"])


class TestClosedSetDiscipline(unittest.TestCase):
    """Doctrinal: the closed-set tuple is stable + non-empty."""

    def test_valid_event_types_includes_documented_set(self) -> None:
        # The Build Plan §3.3 lists these as the minimum required.
        # Adding entries is a doctrinal change; removing entries here
        # silently would break write_event for prior runs.
        for required in (
            "open",
            "close",
            "pattern_recognized",
            "refutation",
            "capacity_change",
            "correction",
        ):
            self.assertIn(required, _VALID_EVENT_TYPES)


if __name__ == "__main__":
    unittest.main()
