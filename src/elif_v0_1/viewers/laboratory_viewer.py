"""Laboratory Viewer — four panels over multi-run + memory-log substrate.

Per spec §3 in `notes/elif_v1_viewer_audit_and_spec.md`. Read-only.
Pure functions. No LLM calls. No side effects.

The four panels:
    A) render_memory_timeline      — MemoryLogger event sequence per case
    B) render_replay_table         — Per-cohort replay results
    C) render_offline_vs_live_diff — Per-field literal comparison
    D) render_article_vii_observations — capacity_change events (honest empty)

Discipline: observation, not conclusion. The diff panel renders cell-level
comparisons but does NOT emit an aggregate "diverged: yes/no" judgment. The
load-bearing header on the diff panel must remain explicit (see §3.6 of
the spec).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List, Mapping, Optional

from ._common import (
    _header,
    _hr,
    _normalize_run_report,
)


# =============================================================================
# Panel A — MemoryLogger event timeline
# =============================================================================


def render_memory_timeline(
    case_id: str,
    jsonl_path: Path,
) -> str:
    """Render the MemoryLogger JSONL as a chronological event table.

    Reads the append-only JSONL file at `jsonl_path`, renders one row per
    event in commit order. No aggregation. No annotation beyond the
    literal event content.

    Args:
        case_id: which case label to display in the header
        jsonl_path: path to article_vii_tracking.jsonl for this case

    Returns:
        Markdown string.
    """
    events: List[dict] = []
    if jsonl_path.exists():
        try:
            with jsonl_path.open() as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except OSError:
            pass

    out = [
        _header(f"Memory Timeline — {case_id}", level=1),
        "",
        f"> _Read-only rendering of `{jsonl_path}`. {len(events)} event(s) total._  ",
        "> _One row per event in commit order. No aggregation. No interpretation._",
        "",
    ]

    if not events:
        out.append("_(no events on disk; file empty or missing)_")
        return "\n".join(out)

    out.extend(
        [
            "| # | event_type | step_id / payload markers |",
            "|---|---|---|",
        ]
    )
    for i, ev in enumerate(events, start=1):
        ev_type = ev.get("event_type", "?")
        payload = ev.get("payload", {}) or {}
        markers: List[str] = []
        for marker_key in (
            "step_id",
            "exit_code",
            "trigger",
            "halt_reason",
            "run_id",
            "condition",
        ):
            if marker_key in payload:
                val = str(payload[marker_key])[:60]
                markers.append(f"{marker_key}={val}")
        # Use literal newlines + special-case the run_summary marker
        rs = payload.get("run_summary")
        if isinstance(rs, Mapping):
            verdict = rs.get("final_verdict")
            prc = rs.get("post_refusal_closure")
            if verdict is not None:
                markers.append(f"final_verdict={verdict}")
            if prc is not None:
                markers.append(f"post_refusal_closure={prc}")
        marker_str = "; ".join(markers) or "_(no markers)_"
        marker_str = marker_str.replace("|", "\\|")
        out.append(f"| {i} | `{ev_type}` | {marker_str} |")

    return "\n".join(out)


# =============================================================================
# Panel B — Replay result table
# =============================================================================


def render_replay_table(acceptance_report: Any) -> str:
    """Render per-cohort replay results as a table.

    Args:
        acceptance_report: AcceptanceReport instance OR list of
            ReplayResult-shaped dicts. Each result must have at minimum:
            case_id, structural_similarity_score, runner_path, verdict.

    Returns:
        Markdown string.
    """
    # Normalize: accept either an AcceptanceReport dataclass with
    # `per_case_results` attribute, or a list of dicts/objects.
    results: List[Any]
    if hasattr(acceptance_report, "per_case_results"):
        results = list(acceptance_report.per_case_results)
    elif isinstance(acceptance_report, list):
        results = acceptance_report
    elif isinstance(acceptance_report, Mapping) and "per_case_results" in acceptance_report:
        results = list(acceptance_report["per_case_results"])
    else:
        results = []

    out = [
        _header("Replay Results — per-cohort", level=1),
        "",
        f"> _Read-only rendering of {len(results)} ReplayResult instance(s). "
        "No aggregation beyond literal listing._",
        "",
    ]

    if not results:
        out.append("_(no replay results provided)_")
        return "\n".join(out)

    out.extend(
        [
            "| Case | verdict | similarity | runner_path | missing_count |",
            "|---|---|---|---|---|",
        ]
    )

    for r in results:
        get = (
            (lambda key, default=None: getattr(r, key, default))
            if not isinstance(r, Mapping)
            else (lambda key, default=None: r.get(key, default))
        )
        case_id = get("case_id", "?")
        verdict = get("verdict", "?")
        sim = get("structural_similarity_score", "?")
        path = get("runner_path", "?")
        missing = get("missing_behaviors", ()) or ()
        missing_count = len(missing) if not isinstance(missing, str) else "?"
        out.append(f"| `{case_id}` | `{verdict}` | {sim} | {path} | {missing_count} |")

    return "\n".join(out)


# =============================================================================
# Panel C — Offline vs live diff
# =============================================================================


# Structural anchors compared per-field. Each entry is
# (label, extract_fn) where extract_fn takes a normalized rr_dict and
# returns a primitive value. The diff renders all rows as literal
# comparisons; equality is computed by ==.
def _diff_extract(rr: dict, key_path: List[str], default: Any = None) -> Any:
    cur: Any = rr
    for k in key_path:
        if isinstance(cur, Mapping):
            cur = cur.get(k)
        elif isinstance(cur, list):
            try:
                cur = cur[int(k)]
            except (ValueError, IndexError, TypeError):
                return default
        else:
            return default
        if cur is None:
            return default
    return cur


def _step_output_diff(rr: dict, step_id: str) -> dict:
    for env in rr.get("step_outputs", []) or []:
        if env.get("step_id") == step_id:
            return env.get("structured_output_dict") or {}
    return {}


def render_offline_vs_live_diff(
    offline_report: Any,
    live_report: Any,
) -> str:
    """Render per-field literal comparison of offline vs live runs.

    No aggregate verdict. No "diverged: yes/no." Each row is a literal
    comparison plus a literal "same?" annotation.

    Args:
        offline_report: RunReport instance OR dict (offline-mode run)
        live_report: RunReport instance OR dict (live-mode run)

    Returns:
        Markdown string.
    """
    off = _normalize_run_report(offline_report)
    live = _normalize_run_report(live_report)

    s9_off = _step_output_diff(off, "step_9")
    s9_live = _step_output_diff(live, "step_9")
    s10_off = _step_output_diff(off, "step_10")
    s10_live = _step_output_diff(live, "step_10")
    s11_off = _step_output_diff(off, "step_11")
    s11_live = _step_output_diff(live, "step_11")

    rows: List[tuple] = [
        ("exit_code", off.get("exit_code"), live.get("exit_code")),
        ("envelope_count", len(off.get("step_outputs", [])), len(live.get("step_outputs", []))),
        (
            "memory_logger_entries_written",
            off.get("memory_logger_entries_written"),
            live.get("memory_logger_entries_written"),
        ),
        ("step_9.verdict", s9_off.get("verdict"), s9_live.get("verdict")),
        (
            "step_9.unresolved_uncertainty_count",
            len(s9_off.get("unresolved_uncertainty_sources") or []),
            len(s9_live.get("unresolved_uncertainty_sources") or []),
        ),
        (
            "step_10.operative_count",
            len(s10_off.get("operative") or []),
            len(s10_live.get("operative") or []),
        ),
        (
            "step_10.theoretical_count",
            len(s10_off.get("theoretical") or []),
            len(s10_live.get("theoretical") or []),
        ),
        (
            "step_11.post_refusal_closure",
            s11_off.get("post_refusal_closure"),
            s11_live.get("post_refusal_closure"),
        ),
        (
            "step_11.final_verdict",
            s11_off.get("final_verdict"),
            s11_live.get("final_verdict"),
        ),
    ]

    case_id = off.get("run_context", {}).get("case_id") or live.get(
        "run_context", {}
    ).get("case_id") or "?"

    out = [
        _header(f"Offline-vs-Live Structural Diff — {case_id}", level=1),
        "",
        "> **The Viewer renders the comparison; it does not adjudicate it.** "
        "Both sides are valid procedural outputs. For substantive "
        "interpretation, see [notes/elif_post_e2_divergence_audit.md] and "
        "[notes/elif_post_e2_object_drift_audit.md]. The 'same?' column is a "
        "literal `==` comparison — not a judgment about which side is correct.",
        "",
        "| Field | Offline | Live | Same? |",
        "|---|---|---|---|",
    ]

    for label, off_val, live_val in rows:
        same = "yes" if off_val == live_val else "**NO**"
        out.append(
            f"| `{label}` | `{off_val}` | `{live_val}` | {same} |"
        )

    out.extend(
        [
            "",
            _hr(),
            "",
            "_No aggregate verdict is emitted. Per-row 'same?' annotations "
            "are literal comparisons only._",
        ]
    )

    return "\n".join(out)


# =============================================================================
# Panel D — Article VII observations
# =============================================================================


def render_article_vii_observations(jsonl_paths: List[Path]) -> str:
    """Render capacity_change events from one or more MemoryLogger JSONLs.

    Per spec §3.4: as of commit 9397006, no consumer writes capacity_change
    events under Position B. The Panel renders an honest empty state when
    no such events exist.

    Args:
        jsonl_paths: list of paths to article_vii_tracking.jsonl files

    Returns:
        Markdown string.
    """
    capacity_events: List[tuple] = []  # (jsonl_path, event)
    for path in jsonl_paths:
        if not path.exists():
            continue
        try:
            with path.open() as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        ev = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if ev.get("event_type") == "capacity_change":
                        capacity_events.append((str(path), ev))
        except OSError:
            continue

    out = [
        _header("Article VII Capacity Observations", level=1),
        "",
        f"> _Searched {len(jsonl_paths)} MemoryLogger JSONL file(s) for "
        "`capacity_change` events. Read-only._",
        "",
    ]

    if not capacity_events:
        out.extend(
            [
                "**No `capacity_change` events found across the searched files.**",
                "",
                "Per spec §3.4 — Position B (commit `44b3e6e`) made the surface "
                "emitable on refuse-cases, but no MemoryLogger consumer currently "
                "writes `capacity_change` events. This panel will populate when "
                "consumers exist. Empty state is honest, not hidden.",
            ]
        )
        return "\n".join(out)

    out.extend(
        [
            f"**{len(capacity_events)} capacity_change event(s) found across the searched files.**",
            "",
            "| # | source jsonl | change_type | payload markers |",
            "|---|---|---|---|",
        ]
    )
    for i, (src, ev) in enumerate(capacity_events, start=1):
        payload = ev.get("payload", {}) or {}
        ct = payload.get("change_type") or payload.get("kind") or "?"
        markers: List[str] = []
        for marker_key in ("case_id", "run_id", "step_id", "structure_type"):
            if marker_key in payload:
                markers.append(f"{marker_key}={payload[marker_key]}")
        marker_str = ("; ".join(markers) or "_(no markers)_").replace("|", "\\|")
        out.append(f"| {i} | `{src}` | `{ct}` | {marker_str} |")

    return "\n".join(out)


__all__ = [
    "render_memory_timeline",
    "render_replay_table",
    "render_offline_vs_live_diff",
    "render_article_vii_observations",
]
