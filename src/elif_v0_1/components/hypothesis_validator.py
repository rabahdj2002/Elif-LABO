"""Hypothesis Validator — Steps 4 + 5 owner.

Article ties: Articles I and III. Highest signal-per-cost per Step 6 §3.

Per `notes/elif_v0_1_build_plan.md` §2.3 and `step_8_decision_package_v0_1.md` §2.

Public surface (signatures pinned by scaffold):
    enumerate_hypotheses_with_distinguishing_predictions(
        decomposition, *, run_context, max_calls=...
    ) -> dict
    failure_conditions_per_hypothesis(
        hypotheses, *, run_context, max_calls=...
    ) -> dict

Behavioral contract:
    * enumerate_hypotheses_with_distinguishing_predictions: Step 4 — emit
      a list of hypotheses each carrying a `distinguishing_prediction` that
      separates this hypothesis from its siblings. Output validates against
      STEP_4_OUTPUT_SCHEMA.
        - Article I tie: a hypothesis without a distinguishing prediction
          is a "concern" masquerading as a hypothesis; refuse silently
          by way of schema-required `distinguishing_prediction` field.
        - Article III tie: hypotheses live in the decomposed object space
          (Step 2), so the decomposition is a load-bearing input.
    * failure_conditions_per_hypothesis: Step 5 — for each Step 4 hypothesis,
      emit one explicit `fails_if` failure condition. Output validates against
      STEP_5_OUTPUT_SCHEMA.
        - Article I tie: a hypothesis without a falsification condition
          is unscientific; refuse by way of schema-required `fails_if`.

    * offline_mode (run_context.offline_mode=True) is fixture-driven:
        - enumerate_hypotheses_with_distinguishing_predictions
              -> fixture `step_04__<case_id_short>`
        - failure_conditions_per_hypothesis
              -> fixture `step_05__<case_id_short>`
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
    SchemaValidationError,
)
from ..llm_adapter import complete_structured, validate_against_schema
from ..run_context import RunContext
from ..schemas import STEP_2_OUTPUT_SCHEMA, STEP_4_OUTPUT_SCHEMA, STEP_5_OUTPUT_SCHEMA


# Default cost-cap argument when the orchestrator does not supply one.
# Per Step 8 §8.4: per-run cap is 22.
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


def _require_run_context(value: Any) -> RunContext:
    if not isinstance(value, RunContext):
        raise ELIFError(
            f"expected RunContext; got {type(value).__name__}"
        )
    return value


def _require_step2_decomposition(value: Any) -> Dict[str, Any]:
    """Validate that `value` is a Step 2 decomposition dict.

    Step 4 hypotheses are anchored in the Step 2 family-axis decomposition;
    refusing a malformed decomposition here prevents downstream hypothesis
    drift (Article III tie: hypotheses live in decomposed object space).
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


def _require_step4_hypotheses(value: Any) -> Dict[str, Any]:
    """Validate that `value` is a Step 4 hypotheses payload.

    Step 5 failure conditions are anchored per-hypothesis; refusing a
    malformed Step 4 payload here prevents downstream id-mismatch.
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


# ---- Prompt builders -------------------------------------------------------
def _build_step4_prompt(decomposition: Mapping[str, Any]) -> str:
    """Build the Step 4 hypotheses-with-distinguishing-predictions prompt.

    The prompt instructs the LLM to enumerate >= 1 hypothesis and to attach
    a `distinguishing_prediction` to each. Article I tie: a hypothesis
    without a distinguishing prediction is a "concern" masquerading as a
    hypothesis and is refused at the schema boundary.
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
        "You are operating as the ELIF v0.1 Hypothesis Validator at Step 4 "
        "(hypotheses with distinguishing predictions).\n\n"
        "Article I tie: refuse to emit 'concerns' masquerading as "
        "hypotheses. Each emitted hypothesis MUST carry a "
        "`distinguishing_prediction` — an observable outcome that "
        "separates this hypothesis from its siblings. If you cannot name "
        "a distinguishing prediction for a candidate hypothesis, drop it; "
        "do not pad the list.\n\n"
        "Article III tie: hypotheses live in the decomposed object space "
        "established at Step 2. Use the family axes below as the structural "
        "anchor for the hypotheses you propose.\n\n"
        "STEP 2 DECOMPOSITION (axes already surfaced):\n"
        f"{axes_summary}\n\n"
        "Output requirements:\n"
        "  * `hypotheses`: at least 1 entry; prefer 2-4 hypotheses spanning "
        "the load-bearing axes.\n"
        "  * Each hypothesis: `hypothesis_id` (short token like 'H1'), "
        "`statement` (one declarative sentence), and "
        "`distinguishing_prediction` (one sentence naming a separable "
        "observable).\n"
        "Emit nothing outside the structured tool output."
    )


def _build_step5_prompt(hypotheses_payload: Mapping[str, Any]) -> str:
    """Build the Step 5 failure-conditions-per-hypothesis prompt.

    The prompt instructs the LLM to attach one explicit `fails_if` to every
    hypothesis emitted at Step 4. Article I tie: a hypothesis without a
    falsification condition is unscientific.
    """
    hyps = hypotheses_payload.get("hypotheses") or []
    hyp_summary_lines = []
    for h in hyps:
        if not isinstance(h, Mapping):
            continue
        hid = h.get("hypothesis_id", "?")
        statement = h.get("statement", "?")
        hyp_summary_lines.append(f"  - {hid}: {statement}")
    hyp_summary = (
        "\n".join(hyp_summary_lines) if hyp_summary_lines else "  (none)"
    )

    return (
        "You are operating as the ELIF v0.1 Hypothesis Validator at Step 5 "
        "(failure conditions per hypothesis).\n\n"
        "Article I tie: every hypothesis MUST be falsifiable. Emit exactly "
        "one `fails_if` per hypothesis — an observable condition that, if "
        "met, would falsify that hypothesis. The `fails_if` statement must "
        "be testable, not merely 'turns out to be wrong'.\n\n"
        "STEP 4 HYPOTHESES (one falsification condition each):\n"
        f"{hyp_summary}\n\n"
        "Output requirements:\n"
        "  * `failure_conditions`: at least 1 entry; ideally one per "
        "hypothesis above.\n"
        "  * Each entry: `hypothesis_id` matching a Step 4 id, and "
        "`fails_if` (one sentence naming a testable falsification "
        "condition).\n"
        "Emit nothing outside the structured tool output."
    )


# ---- Component -------------------------------------------------------------
class HypothesisValidator:
    """Owner of Step 4 (hypotheses + distinguishing predictions) and
    Step 5 (failure conditions per hypothesis).

    Per architecture/03_hypothesis_validator.md and step_8_decision_package §2.
    Articles I + III tie: rejects "concerns" masquerading as hypotheses.
    """

    component_id = "hypothesis_validator"
    article_ties = ("I", "III")

    # ---- Step 4 ------------------------------------------------------------
    def enumerate_hypotheses_with_distinguishing_predictions(
        self,
        decomposition: Any,
        *,
        run_context: RunContext,
        max_calls: int = _DEFAULT_MAX_CALLS,
    ) -> Dict[str, Any]:
        """Step 4: hypotheses with distinguishing predictions, closed-set shape.

        Returns the parsed LLM output as a dict matching STEP_4_OUTPUT_SCHEMA.
        Raises:
            ELIFError on invalid input shape.
            SchemaValidationError on LLM output that drifts from the schema
              (raised by the adapter; re-validated here for defence-in-depth).
        """
        decomp = _require_step2_decomposition(decomposition)
        ctx = _require_run_context(run_context)

        prompt = _build_step4_prompt(decomp)
        fixture_id = (
            f"step_04__{_extract_case_token(ctx.case_id)}"
            if ctx.offline_mode
            else ""
        )

        payload = complete_structured(
            prompt=prompt,
            output_schema=STEP_4_OUTPUT_SCHEMA,
            max_calls=max_calls,
            offline_mode=ctx.offline_mode,
            offline_fixture_id=fixture_id,
        )

        # Defence-in-depth: the adapter already validated, but a malformed
        # live response or a tampered fixture should fail here too.
        validate_against_schema(payload, STEP_4_OUTPUT_SCHEMA)
        _enforce_step4_semantics(payload)
        return payload

    # ---- Step 5 ------------------------------------------------------------
    def failure_conditions_per_hypothesis(
        self,
        hypotheses: Any,
        *,
        run_context: RunContext,
        max_calls: int = _DEFAULT_MAX_CALLS,
    ) -> Dict[str, Any]:
        """Step 5: one explicit failure condition per hypothesis.

        `hypotheses` must be a Step 4 output dict (re-validated against
        STEP_4_OUTPUT_SCHEMA for defence-in-depth).

        Returns the parsed LLM output as a dict matching STEP_5_OUTPUT_SCHEMA.
        """
        hyp_payload = _require_step4_hypotheses(hypotheses)
        ctx = _require_run_context(run_context)

        prompt = _build_step5_prompt(hyp_payload)
        fixture_id = (
            f"step_05__{_extract_case_token(ctx.case_id)}"
            if ctx.offline_mode
            else ""
        )

        payload = complete_structured(
            prompt=prompt,
            output_schema=STEP_5_OUTPUT_SCHEMA,
            max_calls=max_calls,
            offline_mode=ctx.offline_mode,
            offline_fixture_id=fixture_id,
        )

        validate_against_schema(payload, STEP_5_OUTPUT_SCHEMA)
        _enforce_step5_semantics(payload)
        return payload


# ---- Semantic post-validation (Articles I + III tie) -----------------------
def _enforce_step4_semantics(payload: Mapping[str, Any]) -> None:
    """Verify Step 4 semantics beyond what JSON Schema can express.

    Schema already requires >= 1 hypothesis and the three load-bearing
    keys per entry (minItems + required). We re-check explicitly so a
    malformed fixture or jsonschema-absent fallback path still halts here.
    """
    hypotheses = payload.get("hypotheses")
    if not isinstance(hypotheses, list) or len(hypotheses) < 1:
        raise SchemaValidationError(
            "Step 4 output: `hypotheses` must be a non-empty list"
        )
    seen_ids: set = set()
    for i, h in enumerate(hypotheses):
        if not isinstance(h, Mapping):
            raise SchemaValidationError(
                f"Step 4 output: hypotheses[{i}] must be an object"
            )
        hid = h.get("hypothesis_id")
        if not isinstance(hid, str) or not hid:
            raise SchemaValidationError(
                f"Step 4 output: hypotheses[{i}].hypothesis_id is missing"
            )
        if hid in seen_ids:
            raise SchemaValidationError(
                f"Step 4 output: duplicate hypothesis_id={hid!r}"
            )
        seen_ids.add(hid)
        statement = h.get("statement")
        if not isinstance(statement, str) or not statement.strip():
            raise SchemaValidationError(
                f"Step 4 output: hypotheses[{i}].statement is missing"
            )
        pred = h.get("distinguishing_prediction")
        if not isinstance(pred, str) or not pred.strip():
            raise SchemaValidationError(
                f"Step 4 output: hypotheses[{i}].distinguishing_prediction "
                "is missing (Article I: no concerns-masquerading-as-hypotheses)"
            )


def _enforce_step5_semantics(payload: Mapping[str, Any]) -> None:
    """Verify Step 5 semantics beyond JSON Schema.

    Article I tie: each failure condition must be non-empty and refer to
    a hypothesis_id-shaped token. We do NOT cross-validate against the
    Step 4 payload here because the runner may interleave revisions; the
    orchestrator handles cohort-level consistency at commit time.
    """
    conditions = payload.get("failure_conditions")
    if not isinstance(conditions, list) or len(conditions) < 1:
        raise SchemaValidationError(
            "Step 5 output: `failure_conditions` must be a non-empty list"
        )
    for i, c in enumerate(conditions):
        if not isinstance(c, Mapping):
            raise SchemaValidationError(
                f"Step 5 output: failure_conditions[{i}] must be an object"
            )
        hid = c.get("hypothesis_id")
        if not isinstance(hid, str) or not hid:
            raise SchemaValidationError(
                f"Step 5 output: failure_conditions[{i}].hypothesis_id "
                "is missing"
            )
        fails_if = c.get("fails_if")
        if not isinstance(fails_if, str) or not fails_if.strip():
            raise SchemaValidationError(
                f"Step 5 output: failure_conditions[{i}].fails_if is "
                "missing (Article I: every hypothesis must be falsifiable)"
            )


__all__ = ["HypothesisValidator"]
