"""Exploration Lens — render the 5-territory map from a single RunReport.

Per spec §4 in `notes/elif_v1_viewer_audit_and_spec.md`. Read-only.
Pure function. No LLM calls. No side effects.

The Lens is the doctrinal vindication of the prior emergence audit:
Exploration Room emerges as a re-reading of existing artifacts. The Lens
renders five territories (Step 2 axes, Step 6 scales, Step 7 trajectories,
Step 9 uncertainty, Step 10 theoretical) as a FLAT map. No edges between
territories. No synthesis. No ranking. The reader connects them.
"""
from __future__ import annotations

from typing import Any, Mapping

from ._common import (
    _bullets,
    _header,
    _hr,
    _normalize_run_report,
    _step_output,
)


def _render_axes(step_2: Mapping[str, Any]) -> str:
    axes = step_2.get("axes") or []
    if not axes:
        return "_(no axes emitted)_"
    out = []
    for i, axis in enumerate(axes, start=1):
        if isinstance(axis, Mapping):
            label = axis.get("axis_name") or axis.get("name") or f"axis {i}"
            rationale = axis.get("rationale", "")
            out.append(f"**Axis {i}: {label}**")
            if rationale:
                out.append(f"  _{rationale}_")
            families = axis.get("families") or []
            if families:
                for fam in families:
                    if isinstance(fam, Mapping):
                        fid = fam.get("family_id") or fam.get("id") or "?"
                        desc = (
                            fam.get("description")
                            or fam.get("definition")
                            or ""
                        )
                        out.append(f"    - **{fid}**: {desc}")
                    else:
                        out.append(f"    - {fam}")
            out.append("")
        else:
            out.append(f"- {axis}")
    return "\n".join(out)


def _render_scales(step_6: Mapping[str, Any]) -> str:
    scales = step_6.get("scales") or []
    rels = step_6.get("cross_scale_relations") or step_6.get("relations") or []
    parts = []
    if scales:
        parts.append("**Scales:**\n")
        for s in scales:
            if isinstance(s, Mapping):
                name = s.get("scale_name") or s.get("name") or "?"
                desc = s.get("description") or ""
                parts.append(f"- **{name}**: {desc}")
            else:
                parts.append(f"- {s}")
        parts.append("")
    if rels:
        parts.append("**Cross-scale relations:**\n")
        for r in rels:
            if isinstance(r, Mapping):
                parts.append(f"- {r.get('description') or r}")
            else:
                parts.append(f"- {r}")
    if not parts:
        return "_(no scales / relations emitted)_"
    return "\n".join(parts)


def _render_trajectories(step_7: Mapping[str, Any]) -> str:
    trajs = step_7.get("trajectories") or []
    if not trajs:
        return "_(no trajectories emitted)_"
    out = []
    for i, t in enumerate(trajs, start=1):
        if isinstance(t, Mapping):
            tag = t.get("tag") or t.get("trajectory_tag") or ""
            desc = t.get("description") or ""
            out.append(f"**{i}.** [{tag}] {desc}")
            reason = t.get("reason") or t.get("rationale")
            if reason:
                out.append(f"   _{reason}_")
        else:
            out.append(f"**{i}.** {t}")
    return "\n".join(out)


def render_exploration_lens(run_report: Any) -> str:
    """Render the Exploration Lens as Markdown.

    Args:
        run_report: RunReport dataclass instance OR dict from saved JSON

    Returns:
        Markdown string with five territory panels.
    """
    rr = _normalize_run_report(run_report)
    ctx = rr.get("run_context", {})

    s2 = _step_output(rr, "step_2") or {}
    s6 = _step_output(rr, "step_6") or {}
    s7 = _step_output(rr, "step_7") or {}
    s9 = _step_output(rr, "step_9") or {}
    s10 = _step_output(rr, "step_10") or {}

    out = [
        _header(f"Exploration Lens — {ctx.get('case_id', '?')}", level=1),
        "",
        "> _Five territories rendered flat. No edges between territories. "
        "No synthesis. No ranking. The reader connects them._  ",
        "> _The Lens is a perspectival choice over existing artifacts; it "
        "does not modify the procedure. See `notes/elif_v1_viewer_audit_and_spec.md` §4._",
        "",
        _hr(),
        "",
        _header("Territory 1 — Decomposition Axes (Step 2)", level=2),
        "",
        _render_axes(s2),
        "",
        _hr(),
        "",
        _header("Territory 2 — Multi-scale Relations (Step 6)", level=2),
        "",
        _render_scales(s6),
        "",
        _hr(),
        "",
        _header("Territory 3 — Outside-frame Trajectories (Step 7)", level=2),
        "",
        _render_trajectories(s7),
        "",
        _hr(),
        "",
        _header(
            f"Territory 4 — Unresolved Uncertainty ({len(s9.get('unresolved_uncertainty_sources', []) or [])} entries — Step 9)",
            level=2,
        ),
        "",
        _bullets(s9.get("unresolved_uncertainty_sources")),
        "",
        _hr(),
        "",
        _header(
            f"Territory 5 — Open Theoretical Questions ({len(s10.get('theoretical', []) or [])} entries — Step 10)",
            level=2,
        ),
        "",
        _bullets(s10.get("theoretical")),
        "",
        _hr(),
        "",
        "_This rendering claims only what the artifacts already claim. "
        "Verbatim extraction from Step 2 / 6 / 7 / 9 / 10 outputs. "
        "Convergence (if any) is provided by the Decision Room. The Lens "
        "deliberately stays in pre-convergence territory._",
    ]

    return "\n".join(out)


__all__ = ["render_exploration_lens"]
