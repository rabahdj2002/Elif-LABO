"""Shared helpers for the viewer modules.

Strict reveal-vs-build discipline: every helper here either extracts data
from existing artifacts or formats strings. None computes new ELIF state.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional


def _normalize_run_report(rr: Any) -> Dict[str, Any]:
    """Accept either a RunReport dataclass instance or a JSON-derived dict.

    Returns the dict shape used by all viewer functions:
        {
            "run_context": {case_id, condition, run_id, ...},
            "step_outputs": [<envelope dicts>],
            "exit_code": int,
            "memory_logger_entries_written": int,
            "completed_at_iso": str,
        }
    """
    if isinstance(rr, Mapping):
        return dict(rr)
    # Dataclass instance — extract fields by attribute access. We avoid
    # importing dataclasses.asdict here so the viewers stay decoupled from
    # the dataclass definition.
    return {
        "run_context": {
            "case_id": rr.run_context.case_id,
            "condition": rr.run_context.condition,
            "procedure_version": rr.run_context.procedure_version,
            "offline_mode": rr.run_context.offline_mode,
            "max_llm_calls": rr.run_context.max_llm_calls,
            "started_at_iso": rr.run_context.started_at_iso,
            "run_id": rr.run_context.run_id,
        },
        "step_outputs": [
            {
                "step_id": env.step_id,
                "structured_output_dict": dict(env.structured_output_dict),
                "committed_at_iso": env.committed_at_iso,
                "llm_calls_used": env.llm_calls_used,
                "time_box_status": env.time_box_status,
            }
            for env in rr.step_outputs
        ],
        "exit_code": rr.exit_code,
        "memory_logger_entries_written": rr.memory_logger_entries_written,
        "completed_at_iso": rr.completed_at_iso,
    }


def _step_output(rr_dict: Mapping[str, Any], step_id: str) -> Optional[Dict[str, Any]]:
    """Find the structured_output_dict for `step_id` in the run-report dict.

    Returns None if the step is not present (e.g. an early-halt run).
    """
    for env in rr_dict.get("step_outputs", []):
        if env.get("step_id") == step_id:
            return env.get("structured_output_dict") or {}
    return None


def _step_envelope(rr_dict: Mapping[str, Any], step_id: str) -> Optional[Dict[str, Any]]:
    """Find the full envelope (including committed_at_iso, llm_calls_used)."""
    for env in rr_dict.get("step_outputs", []):
        if env.get("step_id") == step_id:
            return dict(env)
    return None


def _bullets(items: Optional[List[Any]], indent: str = "") -> str:
    """Render an iterable as Markdown bullets. Empty input -> '(none)'."""
    if not items:
        return f"{indent}_(none)_"
    out = []
    for item in items:
        if isinstance(item, str):
            out.append(f"{indent}- {item}")
        elif isinstance(item, Mapping):
            # Render dict items as JSON-ish key:value lines
            inner = ", ".join(f"{k}={v!r}" for k, v in item.items())
            out.append(f"{indent}- {inner}")
        else:
            out.append(f"{indent}- {item!r}")
    return "\n".join(out)


def _kv_table(rows: List[tuple], col_a: str = "Field", col_b: str = "Value") -> str:
    """Render a list of (key, value) tuples as a 2-column Markdown table."""
    lines = [f"| {col_a} | {col_b} |", "|---|---|"]
    for k, v in rows:
        # Markdown tables: escape pipes and newlines
        v_str = str(v).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {k} | {v_str} |")
    return "\n".join(lines)


def _header(title: str, level: int = 1) -> str:
    return f"{'#' * level} {title}"


def _hr() -> str:
    return "\n---\n"
