"""Branching Roadmap Engine — Step 7-modeA + Step 8 owner.

Article ties: Articles V, VI, VII. Produces outside-frame trajectories
(BRE-feed) and the stage-gated roadmap.

Per `notes/elif_v0_1_build_plan.md` §2.4 and `step_8_decision_package_v0_1.md`
§2. Per §8.9 — each LLM call starts fresh (no sub-behavior state retained
between methods). Per §8.8 — offline fixture mode is in scope. Per §8.10 —
Step 7 split (mode A here, mode B in FrameValidator) keeps the two surfaces
fully separate; this component never emits mode B (`deeper-frame-rejection`)
trajectories.

Public method signatures are pinned by the scaffold:
    outside_frame_trajectories_bre_feed(hypotheses, failures)
    stage_gated_roadmap(trajectories)

Run-context (offline_mode, max_llm_calls, case_id) is injected via the
constructor so the pinned method shapes are not altered. The orchestrator
constructs BranchingRoadmapEngine() with no args during scaffold-mode
wiring; the production wiring passes a RunContext.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Mapping, Optional

from ..base import ELIFError, SchemaValidationError
from ..llm_adapter import complete_structured, validate_against_schema
from ..run_context import RunContext
from ..schemas import (
    STEP_4_OUTPUT_SCHEMA,
    STEP_5_OUTPUT_SCHEMA,
    STEP_7_OUTPUT_SCHEMA,
    STEP_8_OUTPUT_SCHEMA,
)

# Default cap used when the component is constructed without a RunContext.
# Operator-locked at v0.1 §8.4 == 22 calls per run.
_DEFAULT_MAX_LLM_CALLS = 22

# Match the trailing `case_NN` token in any case_id string.
_CASE_TOKEN_RE = re.compile(r"(case_\d+)")

# The Step 7-modeA tag is closed-set; this component emits ONLY this tag.
# Mode B (`deeper-frame-rejection`) is owned by FrameValidator (§8.10 split).
_MODE_A_TAG = "outside-original-frame"

# Article V/VI/VII framing reused across both methods. Closed-set discipline:
# the trajectory tag and stage vocabulary live in the schemas; we cite them
# here so the model never invents synonyms.
_SYSTEM_PREFACE = (
    "You are the ELIF v0.1 Branching Roadmap Engine. Your responsibility "
    "spans Articles V (refusal-capability), VI (coherent convergence), and "
    "VII (generative reconstruction). You never invent vocabulary outside "
    "the closed-set enums declared in the structured-output schema. You "
    "never retain state between calls (decision package §8.9). You own "
    "Step 7 mode A only — emit the tag 'outside-original-frame' and never "
    "'deeper-frame-rejection' (the modeB tag belongs to the Frame Validator)."
)


def _extract_case_token(case_id: str) -> str:
    """Pull the canonical `case_NN` token from a RunContext.case_id string.

    Accepts both the short form ("case_01") and the prose form
    ("case_01_electroculture"). Raises ELIFError on no match so that bad
    case_ids surface immediately at the component boundary rather than
    silently mis-resolving fixtures.
    """
    match = _CASE_TOKEN_RE.search(case_id)
    if not match:
        raise ELIFError(
            f"case_id does not contain a `case_NN` token: {case_id!r}"
        )
    return match.group(1)


def _require_run_context(value: Any) -> RunContext:
    if not isinstance(value, RunContext):
        raise ELIFError(
            f"expected RunContext; got {type(value).__name__}"
        )
    return value


def _require_step4_hypotheses(value: Any) -> Dict[str, Any]:
    """Validate that `value` is a Step 4 hypotheses dict.

    The dict must satisfy STEP_4_OUTPUT_SCHEMA — i.e. include `hypotheses`
    with at least one entry. Re-validates so that mid-procedure shape drift
    halts here, not three steps later.
    """
    if not isinstance(value, Mapping):
        raise ELIFError(
            f"expected Step 4 hypotheses dict; got {type(value).__name__}"
        )
    try:
        validate_against_schema(dict(value), STEP_4_OUTPUT_SCHEMA)
    except SchemaValidationError as exc:
        raise ELIFError(
            f"Step 4 hypotheses do not satisfy STEP_4_OUTPUT_SCHEMA: {exc}"
        ) from exc
    return dict(value)


def _require_step5_failures(value: Any) -> Dict[str, Any]:
    """Validate that `value` is a Step 5 failure-conditions dict."""
    if not isinstance(value, Mapping):
        raise ELIFError(
            f"expected Step 5 failures dict; got {type(value).__name__}"
        )
    try:
        validate_against_schema(dict(value), STEP_5_OUTPUT_SCHEMA)
    except SchemaValidationError as exc:
        raise ELIFError(
            f"Step 5 failures do not satisfy STEP_5_OUTPUT_SCHEMA: {exc}"
        ) from exc
    return dict(value)


def _require_step7_trajectories(value: Any) -> Dict[str, Any]:
    """Validate that `value` is a Step 7 trajectories dict."""
    if not isinstance(value, Mapping):
        raise ELIFError(
            f"expected Step 7 trajectories dict; got {type(value).__name__}"
        )
    try:
        validate_against_schema(dict(value), STEP_7_OUTPUT_SCHEMA)
    except SchemaValidationError as exc:
        raise ELIFError(
            f"Step 7 trajectories do not satisfy STEP_7_OUTPUT_SCHEMA: {exc}"
        ) from exc
    return dict(value)


# ---- Prompt builders -------------------------------------------------------
def _summarize_hypotheses(hypotheses: Mapping[str, Any]) -> str:
    """Render a short bulleted summary of Step 4 hypotheses for the prompt."""
    lines = []
    for h in hypotheses.get("hypotheses") or []:
        if not isinstance(h, Mapping):
            continue
        hid = h.get("hypothesis_id", "?")
        stmt = h.get("statement", "")
        pred = h.get("distinguishing_prediction", "")
        lines.append(
            f"  - {hid}: {stmt} (distinguishing prediction: {pred})"
        )
    return "\n".join(lines) if lines else "  (none)"


def _summarize_failures(failures: Mapping[str, Any]) -> str:
    """Render a short bulleted summary of Step 5 failure conditions."""
    lines = []
    for f in failures.get("failure_conditions") or []:
        if not isinstance(f, Mapping):
            continue
        hid = f.get("hypothesis_id", "?")
        cond = f.get("fails_if", "")
        lines.append(f"  - {hid} fails if: {cond}")
    return "\n".join(lines) if lines else "  (none)"


def _summarize_trajectories(trajectories: Mapping[str, Any]) -> str:
    """Render a bulleted summary of Step 7-modeA trajectories for Step 8."""
    lines = []
    for t in trajectories.get("trajectories") or []:
        if not isinstance(t, Mapping):
            continue
        tid = t.get("trajectory_id", "?")
        tag = t.get("tag", "?")
        reason = t.get("reason", "")
        lines.append(f"  - {tid} [{tag}]: {reason}")
    return "\n".join(lines) if lines else "  (none)"


def _build_step7_modeA_prompt(
    hypotheses: Mapping[str, Any],
    failures: Mapping[str, Any],
) -> str:
    """Build the Step 7 mode A (outside-frame trajectories) prompt."""
    return (
        f"{_SYSTEM_PREFACE}\n\n"
        "TASK: Step 7 mode A — Outside-original-frame trajectories.\n"
        "Emit trajectories that step OUTSIDE the original frame as posed: "
        "reframings of the question itself, structural decompositions that "
        "refuse the bundle, comparison-case reframings, actor-mix "
        "considerations, or any move that the original frame did not "
        "anticipate. Each trajectory MUST be tagged "
        f"'{_MODE_A_TAG}' (closed-set; mode B trajectories are owned by "
        "the Frame Validator and must not appear here). Emit AT LEAST ONE "
        "trajectory with a one-line `reason`.\n\n"
        "STEP 4 HYPOTHESES (in-frame candidates already enumerated):\n"
        f"{_summarize_hypotheses(hypotheses)}\n\n"
        "STEP 5 FAILURE CONDITIONS (per-hypothesis falsification triggers):\n"
        f"{_summarize_failures(failures)}\n\n"
        "Emit nothing outside the structured tool output."
    )


def _build_step8_prompt(trajectories: Mapping[str, Any]) -> str:
    """Build the Step 8 stage-gated roadmap prompt."""
    return (
        f"{_SYSTEM_PREFACE}\n\n"
        "TASK: Step 8 — Stage-gated roadmap.\n"
        "Read the Step 7-modeA outside-frame trajectories and synthesize "
        "them into a stage-gated roadmap. Each stage MUST declare:\n"
        "  * `stage_id` — short token (e.g. 'A1', 'R2', 'P1');\n"
        "  * `description` — what the stage does;\n"
        "  * `continuation_gate` — a TESTABLE condition under which the "
        "next stage may begin. Refuse to emit ceremonial gates "
        "('once we have learned more'); every gate must name an "
        "observable signal whose presence or absence is decidable.\n\n"
        "STEP 7 MODE A TRAJECTORIES:\n"
        f"{_summarize_trajectories(trajectories)}\n\n"
        "Emit at least one stage. Prefer 3-5 when the trajectories "
        "support a multi-stage roadmap. Emit nothing outside the "
        "structured tool output."
    )


# ---- Component -------------------------------------------------------------
class BranchingRoadmapEngine:
    """Owner of Step 7 mode A (outside-frame trajectories that feed Step 8)
    and Step 8 (stage-gated roadmap).

    Per architecture/04_branching_roadmap_engine.md and
    step_8_decision_package §2. Articles V/VI/VII ties.
    """

    component_id = "branching_roadmap_engine"
    article_ties = ("V", "VI", "VII")

    def __init__(self, run_context: Optional[RunContext] = None) -> None:
        # run_context may be None during scaffold construction; the
        # orchestrator passes a RunContext at run-start. Each method is
        # individually robust to a None context (offline_mode defaults to
        # False; tests that need offline behavior pass an explicit ctx).
        self._run_context = run_context

    # ------------------------------------------------------------------
    # Step 7 mode A — outside-frame trajectories (BRE-feed for Step 8)
    # ------------------------------------------------------------------
    def outside_frame_trajectories_bre_feed(
        self,
        hypotheses: Any,
        failures: Any,
    ) -> Dict[str, Any]:
        """Step 7-modeA: outside-original-frame trajectories.

        `hypotheses` must be a Step 4 output dict; `failures` must be a
        Step 5 output dict. Both are re-validated against their schemas for
        defence-in-depth.

        Returns the structured-output dict matching STEP_7_OUTPUT_SCHEMA:
            { "trajectories": [
                {"trajectory_id": <str>,
                 "tag": "outside-original-frame",
                 "reason": <str>},
                ...
            ] }

        Raises:
            ELIFError              — input is not a Step 4/5 dict
            SchemaValidationError  — LLM response violates the pinned schema
            LLMAdapterError        — transport/parsing failure (live mode)
            LLMCallCapError        — per-run cap exhausted
        """
        hyps = _require_step4_hypotheses(hypotheses)
        fails = _require_step5_failures(failures)

        prompt = _build_step7_modeA_prompt(hyps, fails)
        payload = self._call_llm(
            prompt=prompt,
            schema=STEP_7_OUTPUT_SCHEMA,
            step_number=7,
        )
        # Defence-in-depth: adapter validated, but a malformed live response
        # or a tampered fixture should fail here too.
        validate_against_schema(payload, STEP_7_OUTPUT_SCHEMA)
        _enforce_step7_modeA_semantics(payload)
        return payload

    # ------------------------------------------------------------------
    # Step 8 — stage-gated roadmap
    # ------------------------------------------------------------------
    def stage_gated_roadmap(self, trajectories: Any) -> Dict[str, Any]:
        """Step 8: stage-gated roadmap with continuation gates.

        `trajectories` must be a Step 7 output dict (re-validated against
        STEP_7_OUTPUT_SCHEMA for defence-in-depth).

        Returns the structured-output dict matching STEP_8_OUTPUT_SCHEMA:
            { "stages": [
                {"stage_id": <str>,
                 "description": <str>,
                 "continuation_gate": <str>},
                ...
            ] }
        """
        trajs = _require_step7_trajectories(trajectories)

        prompt = _build_step8_prompt(trajs)
        payload = self._call_llm(
            prompt=prompt,
            schema=STEP_8_OUTPUT_SCHEMA,
            step_number=8,
        )
        validate_against_schema(payload, STEP_8_OUTPUT_SCHEMA)
        _enforce_step8_semantics(payload)
        return payload

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _call_llm(
        self,
        *,
        prompt: str,
        schema: Dict[str, Any],
        step_number: int,
    ) -> Dict[str, Any]:
        """Single boundary for invoking the LLM adapter.

        Honors decision §8.9 (each call starts fresh — no caching here).
        Honors §8.8 (offline_mode via fixture id derived from run_context).
        Honors §8.4 (max_calls passed through to adapter cap enforcement).
        """
        offline_mode = (
            self._run_context.offline_mode if self._run_context else False
        )
        max_calls = (
            self._run_context.max_llm_calls
            if self._run_context
            else _DEFAULT_MAX_LLM_CALLS
        )
        model_id = (
            self._run_context.model_id if self._run_context else "sonnet"
        )
        fixture_id = ""
        if offline_mode:
            if self._run_context is None:
                # Unreachable in practice — offline_mode is read off
                # self._run_context above — but defend explicitly anyway.
                fixture_id = f"step_{step_number:02d}__case_01"
            else:
                case_token = _extract_case_token(self._run_context.case_id)
                fixture_id = f"step_{step_number:02d}__{case_token}"
        return complete_structured(
            prompt=prompt,
            output_schema=schema,
            max_calls=max_calls,
            offline_mode=offline_mode,
            offline_fixture_id=fixture_id,
            model_id=model_id,
        )


# ---- Semantic post-validation (Article V/VI/VII tie) -----------------------
def _enforce_step7_modeA_semantics(payload: Mapping[str, Any]) -> None:
    """Verify Step 7-modeA semantics beyond what JSON Schema can express.

    Schema already requires >= 1 trajectory with tag in the closed set
    (`outside-original-frame` | `deeper-frame-rejection`). This component
    OWNS mode A only — surface drift loudly if a `deeper-frame-rejection`
    tag leaks through here (it belongs to FrameValidator per §8.10).
    """
    trajectories = payload.get("trajectories")
    if not isinstance(trajectories, list) or len(trajectories) < 1:
        raise SchemaValidationError(
            "Step 7 mode A output: `trajectories` must be a non-empty list"
        )
    for i, traj in enumerate(trajectories):
        if not isinstance(traj, Mapping):
            raise SchemaValidationError(
                f"Step 7 mode A output: trajectories[{i}] must be an object"
            )
        tag = traj.get("tag")
        if tag != _MODE_A_TAG:
            raise SchemaValidationError(
                f"Step 7 mode A output: trajectories[{i}].tag must be "
                f"{_MODE_A_TAG!r}; got {tag!r}. Mode B "
                f"('deeper-frame-rejection') is owned by FrameValidator."
            )
        if not traj.get("reason"):
            raise SchemaValidationError(
                f"Step 7 mode A output: trajectories[{i}].reason is required"
            )


def _enforce_step8_semantics(payload: Mapping[str, Any]) -> None:
    """Verify Step 8 semantics beyond JSON Schema.

    Schema already requires >= 1 stage with stage_id + description +
    continuation_gate. We re-check explicitly so a malformed fixture or
    a jsonschema-absent fallback path still halts here.
    """
    stages = payload.get("stages")
    if not isinstance(stages, list) or len(stages) < 1:
        raise SchemaValidationError(
            "Step 8 output: `stages` must be a non-empty list"
        )
    for i, stage in enumerate(stages):
        if not isinstance(stage, Mapping):
            raise SchemaValidationError(
                f"Step 8 output: stages[{i}] must be an object"
            )
        if not stage.get("stage_id"):
            raise SchemaValidationError(
                f"Step 8 output: stages[{i}].stage_id is required"
            )
        if not stage.get("continuation_gate"):
            raise SchemaValidationError(
                f"Step 8 output: stages[{i}].continuation_gate is required"
            )


__all__ = ["BranchingRoadmapEngine"]
