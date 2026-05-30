"""Object Drift Panel — render Step 1→2→4→6→7→8→9 object chain.

Per spec §5 in `notes/elif_v1_viewer_audit_and_spec.md`. Read-only.
Pure function. No LLM calls. No side effects.

The Panel does NOT claim drift. It renders the chain so the reader sees.
Reading-lens annotations are constant strings describing what each step's
output IS, structurally — not what it MEANS substantively. If even
constant annotations feel like too-much-build, the strict-minimum mode
omits them via `with_reading_lens=False`.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Optional

from ._common import (
    _bullets,
    _header,
    _hr,
    _normalize_run_report,
    _step_output,
)


# Constant reading-lens annotations per step. Authored from the
# object drift audit's findings (commit f7607ac). Each describes what
# the step's output IS structurally — NOT whether drift occurred. Set
# `with_reading_lens=False` in render_object_chain to omit these.
READING_LENS: dict[str, str] = {
    "anchor": (
        "The object as posed in the input frame — the deployment "
        "proposal received from the operator."
    ),
    "step_1": "The object as Step 1 (FrameValidator) reformulates it.",
    "step_2": "The object as a partition across decomposition axes.",
    "step_4": "The object as claims (hypotheses) about its outcomes.",
    "step_6": "The object as a system traced across scales.",
    "step_7": "The object as one element of a space of alternatives.",
    "step_8": (
        "The object as a procedural artifact — a roadmap. "
        "NOTE: per the object drift audit (notes/elif_post_e2_object_drift_audit.md), "
        "Step 8 is the bifurcation point. The roadmap may describe "
        "world-actions OR analytical deliverables; the reader observes which."
    ),
    "step_9": (
        "The verdict's referent — whatever Step 8 produced. The Step 9 "
        "prompt presents Step 8's roadmap AS 'the proposed forward path' "
        "(governance_kernel.py:241-242). The reader observes whether this "
        "referent is still the input frame's deployment question."
    ),
}


def _render_lens(step_key: str, with_lens: bool) -> str:
    if not with_lens:
        return ""
    return f"\n> **Reading lens:** _{READING_LENS[step_key]}_\n"


def _render_step1(s1: Mapping[str, Any]) -> str:
    parts = [f"- **verdict:** `{s1.get('verdict', '?')}`"]
    rf = s1.get("reformulated_frame")
    if rf:
        parts.append(f"- **reformulated_frame:** {rf}")
    reasoning = s1.get("reasoning")
    if reasoning:
        parts.append(f"- **reasoning:** {reasoning}")
    return "\n".join(parts)


def _render_step2(s2: Mapping[str, Any]) -> str:
    axes = s2.get("axes") or []
    if not axes:
        return "_(no axes emitted)_"
    out = []
    for i, axis in enumerate(axes, start=1):
        if isinstance(axis, Mapping):
            name = axis.get("axis_name") or axis.get("name") or f"axis {i}"
            fams = axis.get("families") or []
            fam_names = []
            for f in fams:
                if isinstance(f, Mapping):
                    fam_names.append(
                        f.get("family_id") or f.get("id") or "?"
                    )
                else:
                    fam_names.append(str(f))
            out.append(f"- **{name}** — families: {', '.join(fam_names) or '(none)'}")
        else:
            out.append(f"- {axis}")
    return "\n".join(out)


def _render_step4(s4: Mapping[str, Any]) -> str:
    hyps = s4.get("hypotheses") or []
    if not hyps:
        return "_(no hypotheses emitted)_"
    out = []
    for h in hyps:
        if isinstance(h, Mapping):
            hid = h.get("hypothesis_id") or h.get("id") or "?"
            desc = h.get("description") or h.get("hypothesis") or ""
            pred = h.get("distinguishing_prediction") or ""
            out.append(f"- **{hid}**: {desc}")
            if pred:
                out.append(f"  _prediction:_ {pred}")
        else:
            out.append(f"- {h}")
    return "\n".join(out)


def _render_step6(s6: Mapping[str, Any]) -> str:
    scales = s6.get("scales") or []
    out = []
    if scales:
        out.append("**Scales:**")
        for s in scales:
            if isinstance(s, Mapping):
                out.append(
                    f"- {s.get('scale_name') or s.get('name') or '?'}: "
                    f"{s.get('description') or ''}"
                )
            else:
                out.append(f"- {s}")
    rels = s6.get("cross_scale_relations") or s6.get("relations") or []
    if rels:
        out.append("\n**Cross-scale relations:**")
        for r in rels:
            if isinstance(r, Mapping):
                out.append(f"- {r.get('description') or r}")
            else:
                out.append(f"- {r}")
    return "\n".join(out) if out else "_(no scales / relations emitted)_"


def _render_step7(s7: Mapping[str, Any]) -> str:
    trajs = s7.get("trajectories") or []
    if not trajs:
        return "_(no trajectories emitted)_"
    out = []
    for t in trajs:
        if isinstance(t, Mapping):
            tag = t.get("tag") or "?"
            desc = t.get("description") or ""
            out.append(f"- [{tag}] {desc}")
        else:
            out.append(f"- {t}")
    return "\n".join(out)


def _render_step8(s8: Mapping[str, Any]) -> str:
    stages = s8.get("stages") or []
    if not stages:
        return "_(no stages emitted)_"
    out = []
    for stage in stages:
        if isinstance(stage, Mapping):
            sid = stage.get("stage_id", "?")
            desc = stage.get("description", "")
            gate = stage.get("continuation_gate", "")
            out.append(f"- **{sid}**: {desc}")
            if gate:
                out.append(f"  _gate:_ {gate}")
        else:
            out.append(f"- {stage}")
    return "\n".join(out)


def _render_step9(s9: Mapping[str, Any]) -> str:
    parts = [f"- **verdict:** `{s9.get('verdict', '?')}`"]
    detail = s9.get("verdict_detail")
    if detail:
        parts.append(f"- **verdict_detail:** {detail}")
    return "\n".join(parts)


def render_object_chain(
    run_report: Any,
    input_frame_path: Optional[Path] = None,
    with_reading_lens: bool = True,
) -> str:
    """Render the object chain as Markdown.

    Args:
        run_report: RunReport dataclass instance OR dict from saved JSON.
        input_frame_path: optional path to `cases/<case_id>/input_frame.md`.
            If provided, the anchor section includes the verbatim frame
            text. If None, the anchor section is omitted.
        with_reading_lens: if True (default), constant reading-lens
            annotations from the object drift audit are included. If
            False, strict-minimum mode — no annotations.

    Returns:
        Markdown string with vertical chain.
    """
    rr = _normalize_run_report(run_report)
    ctx = rr.get("run_context", {})

    out = [
        _header(f"Object Chain Viewer — {ctx.get('case_id', '?')}", level=1),
        "",
        "> _Step 1 → 2 → 4 → 6 → 7 → 8 → 9 chain. Renders the chain so the "
        "reader sees whether drift happened. Does NOT claim drift. See "
        "[notes/elif_post_e2_object_drift_audit.md] for the audit that "
        "motivated this Panel._",
        "",
    ]

    if not with_reading_lens:
        out.append(
            "> _Strict-minimum mode: reading-lens annotations omitted. "
            "Pure step-output rendering._\n"
        )

    # Anchor — input frame
    if input_frame_path is not None and input_frame_path.exists():
        try:
            frame_text = input_frame_path.read_text(encoding="utf-8")
        except OSError:
            frame_text = "_(could not read input frame file)_"
        out.extend(
            [
                _hr(),
                "",
                _header("Anchor — Input Frame (verbatim)", level=2),
                _render_lens("anchor", with_reading_lens),
                "```",
                frame_text.strip(),
                "```",
                "",
            ]
        )

    # The seven chain nodes
    for step_key, header_text, renderer in [
        ("step_1", "Step 1 — Frame Validation", _render_step1),
        ("step_2", "Step 2 — Object Decomposition", _render_step2),
        ("step_4", "Step 4 — Hypotheses with Distinguishing Predictions", _render_step4),
        ("step_6", "Step 6 — Multi-scale Relations", _render_step6),
        ("step_7", "Step 7 — Outside-frame Trajectories (mode A)", _render_step7),
        ("step_8", "Step 8 — Stage-gated Roadmap", _render_step8),
        ("step_9", "Step 9 — Verdict", _render_step9),
    ]:
        step_data = _step_output(rr, step_key) or {}
        out.extend(
            [
                _hr(),
                "",
                "↓",
                "",
                _header(header_text, level=2),
                _render_lens(step_key, with_reading_lens),
                renderer(step_data),
                "",
            ]
        )

    out.extend(
        [
            _hr(),
            "",
            "_The Panel renders the chain. It does not claim drift; the "
            "reader observes whether the object at each step is still "
            "recognizably about the object at the anchor. Per the object "
            "drift audit, ELIF v0.1's substrate does not itself enforce "
            "referential integrity from Step 9 back to Step 1._",
        ]
    )

    return "\n".join(out)


__all__ = ["render_object_chain", "READING_LENS"]
