"""Operative Truth Separator — Step 10 owner.

Article tie: Article IV. Separates scientific / theoretical plausibility
from operational viability.

Per `notes/elif_v0_1_build_plan.md` §2.6 and `step_8_decision_package_v0_1.md`
§2. Per §8.9 — each LLM call starts fresh (no sub-behavior state retained
between methods). Per §8.8 — offline fixture mode is in scope.

Public method signature is pinned by the scaffold:
    separate_operative_from_theoretical(prior_steps, *, run_context, max_calls=...)

Behavioral contract:
    * separate_operative_from_theoretical: Step 10 — emit
      {operative: list[str], theoretical: list[str], absence_log?: str}.
      Output validates against STEP_10_OUTPUT_SCHEMA. Article IV tie:
      operative ≠ theoretical; both are partial; if either strand is
      genuinely empty, the absence must be logged with reason.
    * offline_mode (run_context.offline_mode=True) is fixture-driven:
        - separate_operative_from_theoretical
              -> fixture `step_10__<case_id_short>`
      where <case_id_short> is the trailing `case_NN` segment of
      run_context.case_id. Determinism is inherited from the LLM adapter
      fixture loader (Step 8 §8.8).

Per Step 8 §8.9 each LLM call starts fresh — this component holds no
inter-call state and the prompt is rebuilt every invocation.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Mapping

from ..base import (
    ELIFError,
    get_language_prompt,
    SchemaValidationError,
)
from ..llm_adapter import complete_structured, validate_against_schema
from ..run_context import RunContext
from ..schemas import STEP_10_OUTPUT_SCHEMA


# Default cost-cap argument when the orchestrator does not supply one.
_DEFAULT_MAX_CALLS: int = 22

# Match the trailing `case_NN` token in any case_id string.
_CASE_TOKEN_RE = re.compile(r"(case_\d+)")


def _extract_case_token(case_id: str) -> str:
    """Pull the canonical `case_NN` token from a RunContext.case_id string."""
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


def _require_prior_steps(value: Any) -> Dict[str, Any]:
    """Validate that `value` is a dict of prior step outputs."""
    if not isinstance(value, Mapping):
        raise ELIFError(
            f"expected prior_steps dict; got {type(value).__name__}"
        )
    return dict(value)


def _summarize_prior_steps(prior: Mapping[str, Any]) -> str:
    """Render a short bulleted summary of prior steps for the prompt."""
    lines = []
    step9 = prior.get("step_9")
    if isinstance(step9, Mapping):
        verdict = step9.get("verdict", "?")
        confidence = step9.get("confidence", "?")
        lines.append(f"  - step_9 verdict={verdict}; confidence={confidence}")
    step8 = prior.get("step_8")
    if isinstance(step8, Mapping):
        stages = step8.get("stages") or []
        lines.append(f"  - step_8: {len(stages)} stage-gated entries")
    step4 = prior.get("step_4")
    if isinstance(step4, Mapping):
        hyps = step4.get("hypotheses") or []
        lines.append(f"  - step_4: {len(hyps)} hypotheses")
    return "\n".join(lines) if lines else "  (none)"


def _build_step10_prompt(
    prior_steps: Mapping[str, Any],
    run_context: RunContext | None = None,
) -> str:
    """Build the Step 10 operative-vs-theoretical separation prompt."""
    return (
        "You are operating as the ELIF v0.1 Operative Truth Separator at "
        "Step 10 (operative vs theoretical strand separation).\n\n"
        "Article IV tie: operative truth (what can be done now under named "
        "constraints) is distinct from theoretical truth (what would resolve "
        "the substantive scientific or structural question). Both are "
        "partial. Refuse to merge them into a single 'truth' strand. If one "
        "strand is genuinely empty for this case, populate `absence_log` "
        "naming the reason; do not pad either list to avoid logging "
        "absence.\n\n"
        f"{get_language_prompt(run_context)}"
        "PRIOR PROCEDURE OUTPUTS (load-bearing markers):\n"
        f"{_summarize_prior_steps(prior_steps)}\n\n"
        "Output requirements:\n"
        "  * `operative`: list of strings; each entry is one operationally "
        "actionable instruction the governance verdict authorizes. "
        "Each instruction must be highly detailed and non-trivial.\n"
        "  * `theoretical`: list of strings; each entry is one substantive "
        "scientific or structural question that, if resolved, would "
        "materially update the verdict. Provide deep architectural and "
        "logic insights.\n"
        "  * `absence_log`: short string explaining why one strand is empty, "
        "OR a non-empty confirmation when both strands are populated.\n"
        "Emit nothing outside the structured tool output."
    )


# Post-refusal closure constants — operative bundle constrained to the
# refusal itself per G0 adjudication 2026-05-30 (Position B) and operator's
# verbatim reading: "operative output under refusal remains constrained to
# the refusal itself; theoretical output records what remains unresolved."
_REFUSAL_OPERATIVE_TOKEN = "refuse bundle"
_REFUSAL_ABSENCE_LOG_DEFAULT = (
    "Post-refusal closure (G0 Position B): operative bucket is constrained "
    "to the refusal itself; theoretical bucket carries forward unresolved "
    "uncertainty sources from Step 9 for future-capacity contribution. "
    "Refusal is not transformed by this closure."
)


class OperativeTruthSeparator:
    """Owner of Step 10 (operative vs theoretical).

    Per architecture/06_operative_truth_separator.md and
    step_8_decision_package §2. Article IV tie.
    """

    component_id = "operative_truth_separator"
    article_ties = ("IV",)

    def separate_for_refusal(
        self,
        prior_steps: Any,
        *,
        run_context: RunContext,
    ) -> Dict[str, Any]:
        """Step 10 — post-refusal closure path (G0 Position B, 2026-05-30).

        Deterministic, no LLM call. Returns a constrained Step 10 payload
        when Step 9 verdict is `refuse`:

            operative:   ["refuse bundle"]
            theoretical: <unresolved_uncertainty_sources from step_9, verbatim>
            absence_log: post-refusal closure marker

        The verdict itself is NOT modified here — the orchestrator preserves
        `verdict="refuse"` end-to-end. This method exists so Step 10 can
        fire on refuse-cases without violating Article V's first-clause
        halt-discipline (the halt remains, it is just relocated to
        post-closure) and without consuming an LLM call on a path whose
        operative output is structurally pre-determined.
        """
        prior = _require_prior_steps(prior_steps)
        _require_run_context(run_context)

        step9 = prior.get("step_9") or {}
        uncertainty_sources = []
        if isinstance(step9, Mapping):
            raw = step9.get("unresolved_uncertainty_sources") or []
            if isinstance(raw, list):
                uncertainty_sources = [
                    str(s) for s in raw if isinstance(s, str) and s.strip()
                ]

        payload = {
            "operative": [_REFUSAL_OPERATIVE_TOKEN],
            "theoretical": uncertainty_sources,
            "absence_log": _REFUSAL_ABSENCE_LOG_DEFAULT,
        }
        # Schema + semantic enforcement is identical to the live path; reuse
        # so any future schema drift surfaces on refuse-cases too.
        from ..llm_adapter import validate_against_schema as _validate
        _validate(payload, STEP_10_OUTPUT_SCHEMA)
        _enforce_step10_semantics(payload)
        return payload

    def separate_operative_from_theoretical(
        self,
        prior_steps: Any,
        *,
        run_context: RunContext,
        max_calls: int = _DEFAULT_MAX_CALLS,
    ) -> Dict[str, Any]:
        """Step 10: two-bucket output (operative vs theoretical).

        `prior_steps` is the orchestrator-maintained dict of prior committed
        step outputs keyed by step_id (e.g. {"step_1": {...}, ...}).

        Returns the parsed LLM output as a dict matching STEP_10_OUTPUT_SCHEMA:
            {
                "operative": [<str>, ...],
                "theoretical": [<str>, ...],
                "absence_log": <str>,    # optional but recommended
            }

        Raises:
            ELIFError              — input is not a prior_steps dict
            SchemaValidationError  — LLM response violates the pinned schema
            LLMAdapterError        — transport/parsing failure (live mode)
            LLMCallCapError        — per-run cap exhausted
        """
        prior = _require_prior_steps(prior_steps)
        ctx = _require_run_context(run_context)

        prompt = _build_step10_prompt(prior, ctx)
        fixture_id = (
            f"step_10__{_extract_case_token(ctx.case_id)}"
            if ctx.offline_mode
            else ""
        )

        payload = complete_structured(
            prompt=prompt,
            output_schema=STEP_10_OUTPUT_SCHEMA,
            max_calls=max_calls,
            offline_mode=ctx.offline_mode,
            offline_fixture_id=fixture_id,
            model_id=ctx.model_id,
        )

        validate_against_schema(payload, STEP_10_OUTPUT_SCHEMA)
        _enforce_step10_semantics(payload)
        return payload


def _enforce_step10_semantics(payload: Mapping[str, Any]) -> None:
    """Verify Step 10 semantics beyond JSON Schema.

    Schema already requires the two list keys + optional absence_log.
    Article IV tie: XOR-soft — when both strands are empty, absence_log
    must be populated to surface the absence loudly.
    """
    operative = payload.get("operative")
    theoretical = payload.get("theoretical")
    if not isinstance(operative, list):
        raise SchemaValidationError(
            "Step 10 output: `operative` must be a list"
        )
    if not isinstance(theoretical, list):
        raise SchemaValidationError(
            "Step 10 output: `theoretical` must be a list"
        )
    if not operative and not theoretical:
        absence = payload.get("absence_log")
        if not isinstance(absence, str) or not absence.strip():
            raise SchemaValidationError(
                "Step 10 output: both strands empty requires non-empty "
                "`absence_log` (Article IV: absence must be named)"
            )


__all__ = ["OperativeTruthSeparator"]
