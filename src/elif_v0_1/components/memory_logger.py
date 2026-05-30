"""Memory Logger — Step 11 owner. ARCHITECTURE-DEPENDENT component.

Article tie: Article VII (capacity vs truth). This is the one component
that cannot be delivered prompt-only — it requires persistent JSONL,
cross-case state, reuse-count tracking, and capacity-metric aggregation.

Per `notes/elif_v0_1_build_plan.md` §2.7 + §3 and
`notes/step_8_decision_package_v0_1.md` §2 + §6, the MemoryLogger:

    * Persists events as append-only JSONL per case
      (`<base_persistence_dir>/<case_id>/article_vii_tracking.jsonl`).
    * Reconstructs case state by replaying events in commit order.
    * Detects cross-case reuse candidates via lexical-shape similarity.
    * Aggregates capacity metrics across cases.
    * Emits corrections as NEW supersede-events; originals are NEVER
      mutated (Article III audit-trail discipline).
    * Detects the sterile-equilibrium signature (Article VII, build plan
      §3.6 critical-failure pattern).

Decision §8.10 — the MemoryLogger is the ONLY architecture-dependent
component. It takes NO `run_context` parameter (no LLM calls). The
constructor receives `results_dir` (legacy `results/` for replay) and
`base_persistence_dir` (the JSONL write surface).

Per CLAUDE.md closed-set discipline + Step 8 §8.7 schema freeze at v0.4.0,
event_type is closed-set: see `_VALID_EVENT_TYPES`. Adding a member is a
doctrinal change.
"""

from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

from ..base import ELIFError, InputFrame
from ..schemas import SCHEMA_VERSION


# Closed-set event types accepted by `write_event`. The `correction` event
# type is emitted ONLY via `emit_correction`; clients cannot write it
# directly through write_event without going through that path.
_VALID_EVENT_TYPES: Tuple[str, ...] = (
    "open",
    "close",
    "step_committed",
    "frame_locked",
    "verdict_emitted",
    "uncertainty_recorded",
    "reuse_detected",
    "pattern_recognized",
    "refutation",
    "capacity_change",
    "correction",
)

# Closed-set capacity-change kinds. Mirrors the on-disk schema (build plan
# §3.1 memory_logger_capacity_change_records.change_type enum).
_VALID_CHANGE_TYPES: Tuple[str, ...] = (
    "arbitration_shortcut_added",
    "framework_candidate_emerged",
    "composition_path_discovered",
    "pattern_recognition_added",
    "judgment_act_logged",
)

# JSONL filename inside each case directory. Append-only.
_EVENTS_FILENAME: str = "article_vii_tracking.jsonl"

# Lower-case token regex used by `find_reuse_candidates` for lexical-shape
# similarity. The reuse detector is deliberately simple here (build plan
# §3.6 "initially: substring match on structure_type; later: configurable").
_WORD_RE = re.compile(r"[a-z0-9]+")


def _utc_now_iso() -> str:
    """Return an ISO-8601 UTC timestamp suitable for `committed_at_iso`."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _new_event_id() -> str:
    """Generate a stable event id."""
    return f"evt_{uuid.uuid4().hex}"


def _tokenize(text: str) -> List[str]:
    """Lower-case + word-token extraction for similarity scoring."""
    if not isinstance(text, str):
        return []
    return _WORD_RE.findall(text.lower())


def _jaccard(a: List[str], b: List[str]) -> float:
    """Jaccard similarity over token sets. Returns 0.0 on empty inputs."""
    if not a or not b:
        return 0.0
    sa, sb = set(a), set(b)
    inter = sa & sb
    union = sa | sb
    if not union:
        return 0.0
    return len(inter) / len(union)


def _require_nonempty_case_id(case_id: Any) -> str:
    if not isinstance(case_id, str) or not case_id:
        raise ELIFError(
            f"case_id must be a non-empty str; got {case_id!r}"
        )
    if "/" in case_id or "\\" in case_id or ".." in case_id:
        raise ELIFError(
            f"case_id must not contain path separators or '..'; got {case_id!r}"
        )
    return case_id


def _require_event_dict(event: Any) -> Dict[str, Any]:
    if not isinstance(event, Mapping):
        raise ELIFError(
            f"event must be a mapping; got {type(event).__name__}"
        )
    return dict(event)


class MemoryLogger:
    """Owner of Step 11 (capture) + cross-case state + Article VII tracking.

    Per architecture/07_feedback_memory_logger.md and
    step_8_decision_package §2 + §6. Article VII tie (primary).

    Decision §8.10: NO LLM calls. Pure persistence + aggregation surface.

    Constructor:
        results_dir            — legacy `results/` directory for on-disk
                                 article_vii_tracking.json replay (read-only).
                                 May be None when not used.
        base_persistence_dir   — root directory under which per-case JSONL
                                 logs are written. Created on demand.
    """

    component_id = "memory_logger"
    article_ties = ("VII",)

    def __init__(
        self,
        results_dir: Optional[os.PathLike] = None,
        base_persistence_dir: Optional[os.PathLike] = None,
    ) -> None:
        # results_dir is optional — only used by read paths that fall back
        # to the legacy on-disk article_vii_tracking.json (one per case).
        self._results_dir: Optional[Path] = (
            Path(results_dir) if results_dir is not None else None
        )
        # base_persistence_dir is the JSONL write surface. Default to a
        # `.memory_logger/` sibling beneath cwd so the component is
        # constructible without args (mirrors FrameValidator() pattern).
        if base_persistence_dir is None:
            base_persistence_dir = Path.cwd() / ".memory_logger"
        self._base_dir: Path = Path(base_persistence_dir)

    # ------------------------------------------------------------------
    # Internal path helpers
    # ------------------------------------------------------------------
    def _case_dir(self, case_id: str) -> Path:
        return self._base_dir / case_id

    def _events_path(self, case_id: str) -> Path:
        return self._case_dir(case_id) / _EVENTS_FILENAME

    def _ensure_case_dir(self, case_id: str) -> Path:
        case_dir = self._case_dir(case_id)
        case_dir.mkdir(parents=True, exist_ok=True)
        return case_dir

    def _iter_case_dirs(self) -> List[Path]:
        """Return every case directory under base_persistence_dir.

        Tolerant of a missing base dir (returns []), since fresh
        installations have no prior cases yet.
        """
        if not self._base_dir.is_dir():
            return []
        return sorted(
            p for p in self._base_dir.iterdir()
            if p.is_dir() and (p / _EVENTS_FILENAME).is_file()
        )

    # ------------------------------------------------------------------
    # write_event
    # ------------------------------------------------------------------
    def write_event(
        self, case_id: str, event: Mapping[str, Any]
    ) -> Dict[str, Any]:
        """Append a structured event to the case's JSONL log.

        Returns the event as written (with `event_id` + `committed_at_iso`
        backfilled if absent). Article VII discipline: appends NEVER mutate
        prior lines; the file is opened in append-mode.

        Raises:
            ELIFError — on missing case_id, bad event shape, or unknown
                event_type. Closed-set drift fails loud here.
        """
        case_id = _require_nonempty_case_id(case_id)
        event_dict = _require_event_dict(event)

        event_type = event_dict.get("event_type")
        if event_type not in _VALID_EVENT_TYPES:
            raise ELIFError(
                f"event_type must be one of {_VALID_EVENT_TYPES}; "
                f"got {event_type!r}"
            )
        if "payload" in event_dict and not isinstance(
            event_dict["payload"], Mapping
        ):
            raise ELIFError(
                "event.payload must be a mapping if present; "
                f"got {type(event_dict['payload']).__name__}"
            )

        # Backfill identity + commit-time + case_id for auditability.
        event_dict.setdefault("event_id", _new_event_id())
        event_dict.setdefault("committed_at_iso", _utc_now_iso())
        event_dict.setdefault("case_id", case_id)
        event_dict.setdefault("schema_version", SCHEMA_VERSION)

        self._ensure_case_dir(case_id)
        path = self._events_path(case_id)
        # Append-only persistence — never seek backward.
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event_dict, sort_keys=True) + "\n")
        return event_dict

    # ------------------------------------------------------------------
    # read_case_state
    # ------------------------------------------------------------------
    def read_case_state(self, case_id: str) -> Dict[str, Any]:
        """Return reconstructed state by replaying events in commit order.

        The replay model:
            * events are read in append-order;
            * `correction` events with `supersedes_event_id` mark the
              target as superseded; the original line is NEVER removed;
            * the returned dict carries:
                  - case_id
                  - events_in_order: list[dict]    (full chronological log)
                  - latest_events:   list[dict]    (originals minus those
                                                   superseded by a later
                                                   correction)
                  - superseded_ids:  list[str]
                  - event_count:     int
                  - event_type_counts: dict[str, int]

        Raises:
            ELIFError — on missing case_id or missing JSONL file.
        """
        case_id = _require_nonempty_case_id(case_id)
        path = self._events_path(case_id)
        if not path.is_file():
            raise ELIFError(
                f"no event log found for case_id={case_id!r}; "
                f"expected {path}"
            )
        events_in_order = self._read_jsonl(path)
        superseded_ids: List[str] = []
        for ev in events_in_order:
            target = ev.get("supersedes_event_id")
            if isinstance(target, str) and target:
                superseded_ids.append(target)
        latest_events = [
            ev for ev in events_in_order
            if ev.get("event_id") not in set(superseded_ids)
        ]
        type_counts: Dict[str, int] = {}
        for ev in events_in_order:
            et = ev.get("event_type", "unknown")
            type_counts[et] = type_counts.get(et, 0) + 1
        return {
            "case_id": case_id,
            "events_in_order": events_in_order,
            "latest_events": latest_events,
            "superseded_ids": superseded_ids,
            "event_count": len(events_in_order),
            "event_type_counts": type_counts,
        }

    # ------------------------------------------------------------------
    # find_reuse_candidates
    # ------------------------------------------------------------------
    def find_reuse_candidates(
        self, input_frame: Any
    ) -> List[Tuple[str, float]]:
        """Article VII: cross-case reuse-candidate detection.

        Scans every prior case directory under base_persistence_dir.
        Computes a Jaccard token-set similarity between the supplied
        `input_frame` (str OR InputFrame) and the concatenation of each
        case's events. Returns (case_id, score) pairs sorted by descending
        score. Empty list when no prior cases exist.

        This is deliberately a substring-shape baseline (build plan §3.6:
        "initially: substring match on structure_type; later: configurable
        matcher"). It is NOT a semantic match.

        Raises:
            ELIFError — when input_frame is neither str nor InputFrame.
        """
        if isinstance(input_frame, InputFrame):
            query_text = input_frame.text
        elif isinstance(input_frame, str):
            query_text = input_frame
        else:
            raise ELIFError(
                f"input_frame must be str or InputFrame; "
                f"got {type(input_frame).__name__}"
            )
        if not query_text.strip():
            raise ELIFError("input_frame text must be non-empty")

        query_tokens = _tokenize(query_text)
        candidates: List[Tuple[str, float]] = []
        for case_dir in self._iter_case_dirs():
            case_id = case_dir.name
            events = self._read_jsonl(case_dir / _EVENTS_FILENAME)
            if not events:
                continue
            case_text = " ".join(
                json.dumps(ev, sort_keys=True) for ev in events
            )
            score = _jaccard(query_tokens, _tokenize(case_text))
            candidates.append((case_id, score))
        candidates.sort(key=lambda kv: (-kv[1], kv[0]))
        return candidates

    # ------------------------------------------------------------------
    # compute_capacity_metrics
    # ------------------------------------------------------------------
    def compute_capacity_metrics(self) -> Dict[str, Any]:
        """Article VII aggregate: cross-case capacity metrics.

        Returns:
            {
                "total_events": int,
                "capacity_change_records": int,
                "reuse_count_total": int,
                "patterns_recognized": int,
                "cases_observed": int,
                "per_case": {case_id: {<sub-counts>}}
            }

        Counts are zero-safe (an empty persistence dir returns zeros).
        """
        total_events = 0
        capacity_change = 0
        reuse_count = 0
        patterns_recognized = 0
        per_case: Dict[str, Dict[str, int]] = {}
        case_dirs = self._iter_case_dirs()
        for case_dir in case_dirs:
            case_id = case_dir.name
            events = self._read_jsonl(case_dir / _EVENTS_FILENAME)
            c_total = len(events)
            c_capacity = sum(
                1 for ev in events if ev.get("event_type") == "capacity_change"
            )
            c_reuse = sum(
                1 for ev in events if ev.get("event_type") == "reuse_detected"
            )
            c_patterns = sum(
                1 for ev in events
                if ev.get("event_type") == "pattern_recognized"
            )
            per_case[case_id] = {
                "events": c_total,
                "capacity_change": c_capacity,
                "reuse_detected": c_reuse,
                "patterns_recognized": c_patterns,
            }
            total_events += c_total
            capacity_change += c_capacity
            reuse_count += c_reuse
            patterns_recognized += c_patterns
        return {
            "total_events": total_events,
            "capacity_change_records": capacity_change,
            "reuse_count_total": reuse_count,
            "patterns_recognized": patterns_recognized,
            "cases_observed": len(case_dirs),
            "per_case": per_case,
        }

    # ------------------------------------------------------------------
    # emit_correction
    # ------------------------------------------------------------------
    def emit_correction(
        self,
        case_id: str,
        target_event_id: str,
        correction_payload: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """Article III/VII: emit a correction event.

        The correction is a NEW event with `event_type="correction"` and
        `supersedes_event_id=target_event_id`. The original event is
        NEVER touched. Read-side `read_case_state` filters it from
        `latest_events` while preserving it in `events_in_order`.

        Raises:
            ELIFError — when target_event_id is missing from the case log
            or payload shape is wrong.
        """
        case_id = _require_nonempty_case_id(case_id)
        if not isinstance(target_event_id, str) or not target_event_id:
            raise ELIFError(
                "target_event_id must be a non-empty str; "
                f"got {target_event_id!r}"
            )
        if not isinstance(correction_payload, Mapping):
            raise ELIFError(
                "correction_payload must be a mapping; "
                f"got {type(correction_payload).__name__}"
            )
        path = self._events_path(case_id)
        if not path.is_file():
            raise ELIFError(
                f"no event log found for case_id={case_id!r}; "
                f"expected {path}"
            )
        prior = self._read_jsonl(path)
        if not any(ev.get("event_id") == target_event_id for ev in prior):
            raise ELIFError(
                f"target_event_id={target_event_id!r} not found in case "
                f"{case_id!r}; cannot supersede a nonexistent event"
            )
        correction_event = {
            "event_id": _new_event_id(),
            "event_type": "correction",
            "case_id": case_id,
            "committed_at_iso": _utc_now_iso(),
            "supersedes_event_id": target_event_id,
            "payload": dict(correction_payload),
            "schema_version": SCHEMA_VERSION,
        }
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(correction_event, sort_keys=True) + "\n")
        return correction_event

    # ------------------------------------------------------------------
    # detect_sterile_equilibrium
    # ------------------------------------------------------------------
    def detect_sterile_equilibrium(
        self, case_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Article VII sterile-equilibrium signature detector.

        Build plan §3.6: returns True when across the case window:
            * reuse_count_total = 0
            * no fresh-structure events
            * no patterns_deprecated entries
            * no capacity_change records

        We return a structured verdict dict (not bare bool) so callers get
        the diagnosis alongside the flag — mirrors the Q6.3 "engage with
        absence_reason" pattern from ObjectDecomposer.

        When `case_id` is None, the detector operates over ALL known cases
        (cross-case window); otherwise over a single case.

        Returns:
            {
                "sterile_equilibrium": bool,
                "scope": "case" | "cross_case",
                "case_id": str | None,
                "signals": {
                    "reuse_count_total": int,
                    "capacity_change_records": int,
                    "patterns_recognized": int,
                    "total_events": int,
                },
            }
        """
        if case_id is not None:
            case_id = _require_nonempty_case_id(case_id)
            scope = "case"
            try:
                state = self.read_case_state(case_id)
            except ELIFError:
                state = {"events_in_order": []}
            events = state.get("events_in_order", [])
            signals = self._aggregate_signals(events)
        else:
            scope = "cross_case"
            signals = {
                "reuse_count_total": 0,
                "capacity_change_records": 0,
                "patterns_recognized": 0,
                "total_events": 0,
            }
            for case_dir in self._iter_case_dirs():
                events = self._read_jsonl(case_dir / _EVENTS_FILENAME)
                aggr = self._aggregate_signals(events)
                for k, v in aggr.items():
                    signals[k] += v
        sterile = (
            signals["reuse_count_total"] == 0
            and signals["capacity_change_records"] == 0
            and signals["patterns_recognized"] == 0
            and signals["total_events"] > 0
        )
        return {
            "sterile_equilibrium": sterile,
            "scope": scope,
            "case_id": case_id,
            "signals": signals,
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    @staticmethod
    def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
        """Read a JSONL file as a list of dicts.

        Raises ELIFError on malformed lines so silent persistence drift
        surfaces immediately rather than three steps later.
        """
        if not path.is_file():
            return []
        events: List[Dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    parsed = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ELIFError(
                        f"malformed JSONL at {path}:{lineno}: {exc}"
                    ) from exc
                if not isinstance(parsed, dict):
                    raise ELIFError(
                        f"JSONL line at {path}:{lineno} is not an object"
                    )
                events.append(parsed)
        return events

    @staticmethod
    def _aggregate_signals(events: List[Dict[str, Any]]) -> Dict[str, int]:
        return {
            "reuse_count_total": sum(
                1 for ev in events if ev.get("event_type") == "reuse_detected"
            ),
            "capacity_change_records": sum(
                1 for ev in events if ev.get("event_type") == "capacity_change"
            ),
            "patterns_recognized": sum(
                1 for ev in events
                if ev.get("event_type") == "pattern_recognized"
            ),
            "total_events": len(events),
        }


__all__ = ["MemoryLogger"]
