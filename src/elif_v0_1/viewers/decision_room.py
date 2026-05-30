"""Decision Room — render Step 9 + 10 + 11 from a single RunReport.

Per spec §2 in `notes/elif_v1_viewer_audit_and_spec.md`. Read-only.
Pure function. No LLM calls. No side effects.

The Decision Room is the smallest viewer surface. It deliberately omits
Steps 1-8 (that is the procedure-arc surface, not the decision surface).
It renders the verdict, its detail + confidence, its uncertainty sources,
the operative/theoretical split, and the run summary.
"""
from __future__ import annotations

from typing import Any

from ._common import (
    _bullets,
    _header,
    _hr,
    _kv_table,
    _normalize_run_report,
    _step_envelope,
    _step_output,
)


def render_decision_room(run_report: Any) -> str:
    """Render the Decision Room as Markdown.

    Args:
        run_report: RunReport dataclass instance OR dict from saved JSON

    Returns:
        Markdown string.
    """
    rr = _normalize_run_report(run_report)
    ctx = rr.get("run_context", {})

    s9 = _step_output(rr, "step_9") or {}
    s10 = _step_output(rr, "step_10") or {}
    s11 = _step_output(rr, "step_11") or {}
    s11_env = _step_envelope(rr, "step_11") or {}

    out = [
        _header(f"Decision Room — {ctx.get('case_id', '?')}", level=1),
        "",
        "> _Read-only rendering of Step 9 verdict, Step 10 operative/theoretical, Step 11 summary._  ",
        "> _See `src/elif_v0_1/viewers/` for source; see "
        "[notes/elif_v1_viewer_audit_and_spec.md] for spec._",
        "",
        _header("Run header", level=2),
        _kv_table(
            [
                ("case_id", ctx.get("case_id", "?")),
                ("condition", ctx.get("condition", "?")),
                ("run_id", ctx.get("run_id", "?")),
                ("procedure_version", ctx.get("procedure_version", "?")),
                ("offline_mode", ctx.get("offline_mode", "?")),
                ("started_at_iso", ctx.get("started_at_iso", "?")),
            ]
        ),
        "",
        _header("Step 9 — Verdict", level=2),
        _kv_table(
            [
                ("verdict", s9.get("verdict", "?")),
                (
                    "confidence",
                    s9.get("confidence_qualifier")
                    or s9.get("confidence")
                    or "?",
                ),
            ]
        ),
        "",
        _header("verdict_detail", level=3),
        "",
        s9.get("verdict_detail") or "_(no verdict_detail emitted)_",
        "",
        _header("Unresolved uncertainty sources", level=3),
        "",
        _bullets(s9.get("unresolved_uncertainty_sources")),
        "",
        _header("Step 10 — Operative vs Theoretical", level=2),
        "",
        _header(
            f"Operative ({len(s10.get('operative', []) or [])} entries — what the verdict authorizes)",
            level=3,
        ),
        "",
        _bullets(s10.get("operative")),
        "",
        _header(
            f"Theoretical ({len(s10.get('theoretical', []) or [])} entries — unresolved questions)",
            level=3,
        ),
        "",
        _bullets(s10.get("theoretical")),
        "",
    ]

    absence_log = s10.get("absence_log")
    if absence_log:
        out.extend(
            [
                _header("Absence log", level=3),
                "",
                str(absence_log),
                "",
            ]
        )

    out.extend(
        [
            _header("Step 11 — Run Summary", level=2),
            _kv_table(
                [
                    ("final_verdict", s11.get("final_verdict", "?")),
                    ("step_count", s11.get("step_count", "?")),
                    ("llm_calls_used", s11.get("llm_calls_used", "?")),
                    (
                        "post_refusal_closure",
                        s11.get("post_refusal_closure", "?"),
                    ),
                ]
            ),
            "",
            _header("Run footer", level=2),
            _kv_table(
                [
                    ("exit_code", rr.get("exit_code", "?")),
                    ("completed_at_iso", rr.get("completed_at_iso", "?")),
                    (
                        "memory_logger_entries_written",
                        rr.get("memory_logger_entries_written", "?"),
                    ),
                ]
            ),
            "",
            _hr(),
            "",
            "_This rendering claims only what the artifact already claims. "
            "The Decision Room does not validate, score, or recommend; it "
            "renders. See `notes/elif_post_e2_divergence_audit.md` for "
            "substantive interpretation of any verdict shown above._",
        ]
    )

    return "\n".join(out)


__all__ = ["render_decision_room"]
