"""Object Decomposer — Step 2 owner.

Article tie: Article IV (refuse collapsed heterogeneous objects).
Sub-behavior: Step 6 multi-scale relations (cross-scale-axis).

Per `notes/elif_v0_1_build_plan.md` §2.2 and `step_8_decision_package_v0_1.md` §2.

Public surface (signatures pinned by scaffold):
    decompose(input_frame, *, run_context, max_calls=...) -> dict
    multi_scale_relate(decomposition, *, run_context, max_calls=...) -> dict

Behavioral contract:
    * decompose: Step 2 family-axis decomposition. Output validates against
      STEP_2_OUTPUT_SCHEMA. At least 1 axis; each axis carries >= 2 families.
    * multi_scale_relate: Step 6 cross-scale-axis. Output validates against
      STEP_6_OUTPUT_SCHEMA. At least 2 scales + 1 cross-scale relation in
      the engaged path; collapsed Q6.3 ceremony-risk path (scale_axis_engaged
      false) is currently out of v0.1 schema scope so we always engage the
      axis here and let the LLM (or fixture) populate both fields.
    * offline_mode (run_context.offline_mode=True) is fixture-driven:
        - decompose          -> fixture `step_02__<case_id_short>`
        - multi_scale_relate -> fixture `step_06__<case_id_short>`
      where <case_id_short> is the trailing `case_NN` segment of
      run_context.case_id (e.g. "case_01" extracted from
      "case_01_electroculture"). Determinism is inherited from the LLM
      adapter fixture loader (Step 8 §8.8).

Per Step 8 §8.9 each LLM call starts fresh — this component holds no
inter-call state and the prompt is rebuilt every invocation.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Mapping

from ..base import (
    ELIFError,
    InputFrame,
    SchemaValidationError,
)
from ..llm_adapter import complete_structured, validate_against_schema
from ..run_context import RunContext
from ..schemas import STEP_2_OUTPUT_SCHEMA, STEP_6_OUTPUT_SCHEMA


# Default cost-cap argument when the orchestrator does not supply one.
# Per Step 8 §8.4: per-run cap is 22; per-call we just need a non-zero
# ceiling that the cap counter actually enforces process-wide.
_DEFAULT_MAX_CALLS: int = 22

# Match the trailing `case_NN` token in any case_id string.
_CASE_TOKEN_RE = re.compile(r"(case_\d+)")


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


def _require_input_frame(value: Any) -> InputFrame:
    """Raise ELIFError if `value` is not a real InputFrame."""
    if not isinstance(value, InputFrame):
        raise ELIFError(
            f"expected InputFrame; got {type(value).__name__}"
        )
    return value


def _require_run_context(value: Any) -> RunContext:
    if not isinstance(value, RunContext):
        raise ELIFError(
            f"expected RunContext; got {type(value).__name__}"
        )
    return value


def _require_step2_decomposition(value: Any) -> Dict[str, Any]:
    """Validate that `value` is a Step 2 decomposition dict.

    The dict must satisfy STEP_2_OUTPUT_SCHEMA — i.e. include `axes` with at
    least one axis carrying at least two families. Re-validates so that
    mid-procedure shape drift halts here, not three steps later.
    """
    if not isinstance(value, Mapping):
        raise ELIFError(
            f"expected Step 2 decomposition dict; got {type(value).__name__}"
        )
    try:
        validate_against_schema(dict(value), STEP_2_OUTPUT_SCHEMA)
    except SchemaValidationError as exc:
        raise ELIFError(
            f"Step 2 decomposition does not satisfy STEP_2_OUTPUT_SCHEMA: {exc}"
        ) from exc
    return dict(value)


# ---- Prompt builders -------------------------------------------------------
def _build_step2_prompt(input_frame: InputFrame) -> str:
    """Build the Step 2 family-axis decomposition prompt.

    The prompt instructs the LLM to enumerate >= 1 axis and >= 2 families
    per axis. Article IV tie: refuse to collapse heterogeneous objects;
    name the axis (mechanism / category / scale / decision-type) and give
    a rationale that makes the axis load-bearing.
    """
    return (
        "You are operating as the ELIF v0.1 Object Decomposer at Step 2 "
        "(family-axis decomposition).\n\n"
        "Article IV constraint: every model is a partial projection. "
        "Refuse to treat the input frame as a single homogeneous object. "
        "Surface the load-bearing axes along which the input frame "
        "decomposes into distinct families, and emit them as a structured "
        "tree.\n\n"
        f"INPUT FRAME (locked at {input_frame.locked_at_iso}, "
        f"doctrinal_scope_tag={input_frame.doctrinal_scope_tag!r}, "
        f"companion_case={input_frame.companion_case!r}):\n"
        f"{input_frame.text}\n\n"
        "Output requirements:\n"
        "  * `axes`: at least 1 axis; prefer 2-3 axes when the frame "
        "supports them.\n"
        "  * Each axis: `axis_name` (short noun phrase), `rationale` "
        "(one sentence naming why the axis is load-bearing), and "
        "`families` (at least 2 entries).\n"
        "  * Each family: `family_id` (single letter or short token) and "
        "`description` (one phrase).\n"
        "Emit nothing outside the structured tool output."
    )


def _build_step6_prompt(decomposition: Mapping[str, Any]) -> str:
    """Build the Step 6 multi-scale-axis prompt.

    Reads the Step 2 decomposition and asks for >= 2 distinct scales and
    >= 1 cross-scale relation. Q6.3 ceremony-risk note: the prompt
    instructs the LLM to engage scale-axis only when the content actually
    spans multiple scales; the schema requires both lists populated.
    """
    axes = decomposition.get("axes") or []
    axes_summary_lines = []
    for axis in axes:
        if not isinstance(axis, Mapping):
            continue
        name = axis.get("axis_name", "?")
        fams = axis.get("families") or []
        fam_ids = ", ".join(
            str(f.get("family_id", "?"))
            for f in fams
            if isinstance(f, Mapping)
        )
        axes_summary_lines.append(f"  - {name}: families [{fam_ids}]")
    axes_summary = (
        "\n".join(axes_summary_lines) if axes_summary_lines else "  (none)"
    )

    return (
        "You are operating as the ELIF v0.1 Object Decomposer at Step 6 "
        "(cross-scale-axis sub-behavior).\n\n"
        "Article IV tie: name the scales at which the decomposed families "
        "operate, then identify load-bearing cross-scale relations "
        "(how does the behavior at one scale constrain, enable, or "
        "obscure the behavior at another?).\n\n"
        "STEP 2 DECOMPOSITION (axes already surfaced):\n"
        f"{axes_summary}\n\n"
        "Output requirements:\n"
        "  * `scales`: at least 2 distinct scales (e.g. molecular, "
        "organism, field, farm-economic, research-system, "
        "public-funding, civilizational).\n"
        "  * `cross_scale_relations`: at least 1 statement of the form "
        "'X at scale A does not aggregate to Y at scale B' or "
        "'A operates on a slower timescale than B'.\n"
        "Engage the scale-axis only if the content genuinely spans "
        "multiple scales; do not invent scales the frame does not touch.\n"
        "Emit nothing outside the structured tool output."
    )


# ---- Component -------------------------------------------------------------
class ObjectDecomposer:
    """Owner of Step 2 + sub-behavior Step 6 (multi-scale relations).

    Per architecture/02_object_decomposer.md and step_8_decision_package §2.
    Article IV tie: separate mechanism / category families before reasoning.
    """

    component_id = "object_decomposer"
    article_ties = ("IV",)

    # ---- Step 2 ------------------------------------------------------------
    def decompose(
        self,
        input_frame: InputFrame,
        *,
        run_context: RunContext,
        max_calls: int = _DEFAULT_MAX_CALLS,
    ) -> Dict[str, Any]:
        """Step 2: family-axis decomposition tree.

        Returns the parsed LLM output as a dict matching STEP_2_OUTPUT_SCHEMA.
        Raises:
            ELIFError on invalid input shape.
            SchemaValidationError on LLM output that drifts from the schema
              (raised by the adapter; re-validated here for defence-in-depth).
        """
        frame = _require_input_frame(input_frame)
        ctx = _require_run_context(run_context)

        prompt = _build_step2_prompt(frame)
        fixture_id = (
            f"step_02__{_extract_case_token(ctx.case_id)}"
            if ctx.offline_mode
            else ""
        )

        payload = complete_structured(
            prompt=prompt,
            output_schema=STEP_2_OUTPUT_SCHEMA,
            max_calls=max_calls,
            offline_mode=ctx.offline_mode,
            offline_fixture_id=fixture_id,
            model_id=ctx.model_id,
        )

        # Defence-in-depth: the adapter already validated, but a malformed
        # live response or a tampered fixture should fail here too.
        validate_against_schema(payload, STEP_2_OUTPUT_SCHEMA)
        _enforce_step2_semantics(payload)
        return payload

    # ---- Step 6 ------------------------------------------------------------
    def multi_scale_relate(
        self,
        decomposition: Any,
        *,
        run_context: RunContext,
        max_calls: int = _DEFAULT_MAX_CALLS,
    ) -> Dict[str, Any]:
        """Step 6 sub-behavior: cross-scale relations among decomposed objects.

        `decomposition` must be a Step 2 output dict (re-validated against
        STEP_2_OUTPUT_SCHEMA for defence-in-depth).
        """
        decomp = _require_step2_decomposition(decomposition)
        ctx = _require_run_context(run_context)

        prompt = _build_step6_prompt(decomp)
        fixture_id = (
            f"step_06__{_extract_case_token(ctx.case_id)}"
            if ctx.offline_mode
            else ""
        )

        payload = complete_structured(
            prompt=prompt,
            output_schema=STEP_6_OUTPUT_SCHEMA,
            max_calls=max_calls,
            offline_mode=ctx.offline_mode,
            offline_fixture_id=fixture_id,
            model_id=ctx.model_id,
        )

        validate_against_schema(payload, STEP_6_OUTPUT_SCHEMA)
        _enforce_step6_semantics(payload)
        return payload


# ---- Semantic post-validation (Article IV tie) -----------------------------
def _enforce_step2_semantics(payload: Mapping[str, Any]) -> None:
    """Verify Step 2 semantics beyond what JSON Schema can express.

    Schema already requires >= 1 axis and >= 2 families per axis (minItems).
    We re-check explicitly so a malformed fixture or jsonschema-absent
    fallback path still halts here.
    """
    axes = payload.get("axes")
    if not isinstance(axes, list) or len(axes) < 1:
        raise SchemaValidationError(
            "Step 2 output: `axes` must be a non-empty list"
        )
    for i, axis in enumerate(axes):
        if not isinstance(axis, Mapping):
            raise SchemaValidationError(
                f"Step 2 output: axes[{i}] must be an object"
            )
        if not axis.get("axis_name"):
            raise SchemaValidationError(
                f"Step 2 output: axes[{i}].axis_name is missing"
            )
        families = axis.get("families")
        if not isinstance(families, list) or len(families) < 2:
            raise SchemaValidationError(
                f"Step 2 output: axes[{i}].families must have >= 2 entries"
            )


def _enforce_step6_semantics(payload: Mapping[str, Any]) -> None:
    """Verify Step 6 semantics beyond JSON Schema."""
    scales = payload.get("scales")
    if not isinstance(scales, list) or len(scales) < 2:
        raise SchemaValidationError(
            "Step 6 output: `scales` must contain >= 2 distinct entries"
        )
    if len(set(s for s in scales if isinstance(s, str))) < 2:
        raise SchemaValidationError(
            "Step 6 output: `scales` must contain >= 2 DISTINCT string entries"
        )
    relations = payload.get("cross_scale_relations")
    if not isinstance(relations, list) or len(relations) < 1:
        raise SchemaValidationError(
            "Step 6 output: `cross_scale_relations` must have >= 1 entry"
        )


__all__ = ["ObjectDecomposer"]
