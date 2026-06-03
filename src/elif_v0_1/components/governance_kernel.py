"""Governance Kernel — Step 9 owner.

Article ties: Articles V, VI, VII. Step 11 absorbed into Step 9 per Step 8
compression: verdict + confidence + unresolved-uncertainty in one output.

Per `notes/elif_v0_1_build_plan.md` §2.5 and `step_8_decision_package_v0_1.md`
§2. Per §8.9 — each LLM call starts fresh (no sub-behavior state retained
between methods). Per §8.8 — offline fixture mode is in scope. Per §8.10 —
Step 9 carries the absorbed-Step-11 confidence + unresolved-uncertainty
fields as separate-outputs-only on the same payload.

Public method signature is pinned by the scaffold:
    verdict_with_confidence_and_uncertainty(roadmap, prior_steps, *,
                                            run_context, max_calls=...)

Behavioral contract:
    * verdict_with_confidence_and_uncertainty: Step 9 — emit
      {verdict, verdict_detail?, confidence, unresolved_uncertainty_sources}.
      Output validates against STEP_9_OUTPUT_SCHEMA (closed-set
      verdict ∈ {constrain, refuse, explicitly_abstain}; confidence is a
      free-text qualifier tied to ≥1 named source; unresolved_uncertainty_sources
      has minItems=1).
        - Article V tie: refusal-capability surfaced through verdict.
        - Article VI tie: coherent convergence requires confidence to be
          tied to ≥1 unresolved-uncertainty source (never an unconditioned
          claim).
        - Article VII tie: every verdict names at least one unresolved
          source so the Memory Logger can attach refutability state.
    * offline_mode (run_context.offline_mode=True) is fixture-driven:
        - verdict_with_confidence_and_uncertainty
              -> fixture `step_09__<case_id_short>`
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
from ..schemas import STEP_8_OUTPUT_SCHEMA, STEP_9_OUTPUT_SCHEMA


# Default cost-cap argument when the orchestrator does not supply one.
# Per Step 8 §8.4: per-run cap is 22.
_DEFAULT_MAX_CALLS: int = 22

# Match the trailing `case_NN` token in any case_id string.
_CASE_TOKEN_RE = re.compile(r"(case_\d+)")

# Closed-set verdict vocabulary. Pinned to STEP_9_OUTPUT_SCHEMA enum
# (frozen at v0.4.0 per §8.7). Cited here so the prompt never invents
# synonyms.
_VERDICT_VOCAB = ("constrain", "refuse", "explicitly_abstain")


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


def _require_step8_roadmap(value: Any) -> Dict[str, Any]:
    """Validate that `value` is a Step 8 roadmap dict.

    The dict must satisfy STEP_8_OUTPUT_SCHEMA — i.e. include `stages` with
    at least one entry. Re-validates so that mid-procedure shape drift halts
    here, not three steps later. Article VI tie: the Governance Kernel
    refuses to adjudicate on an incoherent roadmap.
    """
    if not isinstance(value, Mapping):
        raise ELIFError(
            f"expected Step 8 roadmap dict; got {type(value).__name__}"
        )
    try:
        validate_against_schema(dict(value), STEP_8_OUTPUT_SCHEMA)
    except SchemaValidationError as exc:
        raise ELIFError(
            f"Step 8 roadmap does not satisfy STEP_8_OUTPUT_SCHEMA: {exc}"
        ) from exc
    return dict(value)


def _require_prior_steps(value: Any) -> Dict[str, Any]:
    """Validate that `value` is a dict of prior step outputs.

    `prior_steps` is the orchestrator-maintained dict keyed by step_id
    (e.g. {"step_1": {...}, "step_2": {...}, ...}). The Governance Kernel
    reads it summarily — it does NOT re-validate every prior step here
    (each owner already validated at commit-time). We only enforce that the
    container is a dict so prompt building does not silently get a list.
    """
    if not isinstance(value, Mapping):
        raise ELIFError(
            f"expected prior_steps dict; got {type(value).__name__}"
        )
    return dict(value)


# ---- Prompt builders -------------------------------------------------------
def _summarize_roadmap(roadmap: Mapping[str, Any]) -> str:
    """Render a short bulleted summary of the Step 8 roadmap for the prompt."""
    lines = []
    for stage in roadmap.get("stages") or []:
        if not isinstance(stage, Mapping):
            continue
        sid = stage.get("stage_id", "?")
        desc = stage.get("description", "")
        gate = stage.get("continuation_gate", "")
        lines.append(f"  - {sid}: {desc} (gate: {gate})")
    return "\n".join(lines) if lines else "  (none)"


def _summarize_prior_steps(prior: Mapping[str, Any]) -> str:
    """Render a one-line-per-step summary of the prior committed outputs.

    Per Step 8 §8.9 each LLM call starts fresh, so the kernel cannot rely
    on hidden state. The summary is intentionally lossy — Article VI
    requires the kernel to converge on the load-bearing structure of the
    run, not regurgitate every field.
    """
    lines = []
    # Stable order: walk step_1..step_8 if present.
    for step_id in (
        "step_1",
        "step_2",
        "step_3",
        "step_4",
        "step_5",
        "step_6",
        "step_7",
        "step_8",
    ):
        if step_id not in prior:
            continue
        payload = prior.get(step_id)
        marker = _one_line_marker(step_id, payload)
        if marker:
            lines.append(f"  - {step_id}: {marker}")
    return "\n".join(lines) if lines else "  (none)"


def _one_line_marker(step_id: str, payload: Any) -> str:
    """Return a one-line marker characterising `payload` for the prompt.

    The kernel does not need full payloads — it needs the load-bearing
    signal (verdict, axis count, hypothesis count, etc.). This is a
    deliberately lossy summarisation; the LLM has the Step 8 roadmap in
    full alongside.
    """
    if not isinstance(payload, Mapping):
        return ""
    if step_id == "step_1":
        verdict = payload.get("verdict", "?")
        return f"frame verdict={verdict}"
    if step_id == "step_2":
        axes = payload.get("axes") or []
        return f"{len(axes)} family axes"
    if step_id == "step_3":
        assumptions = payload.get("assumptions") or []
        return f"{len(assumptions)} assumptions surfaced"
    if step_id == "step_4":
        hyps = payload.get("hypotheses") or []
        return f"{len(hyps)} hypotheses"
    if step_id == "step_5":
        conds = payload.get("failure_conditions") or []
        return f"{len(conds)} failure conditions"
    if step_id == "step_6":
        scales = payload.get("scales") or []
        rels = payload.get("cross_scale_relations") or []
        return f"{len(scales)} scales / {len(rels)} cross-scale relations"
    if step_id == "step_7":
        trajs = payload.get("trajectories") or []
        return f"{len(trajs)} outside-frame trajectories"
    if step_id == "step_8":
        stages = payload.get("stages") or []
        return f"{len(stages)} stage-gated roadmap entries"
    return ""


def _build_step9_prompt(
    roadmap: Mapping[str, Any],
    prior_steps: Mapping[str, Any],
) -> str:
    """Build the Step 9 governance adjudication prompt.

    The prompt instructs the LLM to emit a closed-set verdict + a
    confidence qualifier + at least one unresolved-uncertainty source.
    Articles V/VI/VII tie: refusal-capability + coherent convergence +
    generative reconstruction all converge in this single output.
    """
    return (
        "You are operating as the ELIF v0.1 Governance Kernel at Step 9 "
        "(verdict with confidence and unresolved uncertainty).\n\n"
        "Article V tie (refusal-capability): the verdict you emit MUST be "
        f"drawn from the closed set {list(_VERDICT_VOCAB)}. Do not invent "
        "synonyms.\n"
        "  * 'constrain' — proceed only under explicit constraints; the "
        "constraints must be readable in `verdict_detail`.\n"
        "  * 'refuse' — refuse to authorize the proposed action; the "
        "refusal reason must be readable in `verdict_detail`.\n"
        "  * 'explicitly_abstain' — refuse to issue a verdict at all "
        "(distinct from refusal); the abstention rationale must be "
        "readable in `verdict_detail`.\n\n"
        "Article VI tie (coherent convergence): the `confidence` qualifier "
        "MUST be tied to at least one named entry in "
        "`unresolved_uncertainty_sources`. Do not assert confidence without "
        "naming what remains unresolved.\n\n"
        "Article VII tie (generative reconstruction): every verdict carries "
        "an unresolved-uncertainty list (minItems=1) so the Memory Logger "
        "can attach refutability state and the next run can compose on top.\n\n"
        "STEP 8 STAGE-GATED ROADMAP (the proposed forward path):\n"
        f"{_summarize_roadmap(roadmap)}\n\n"
        "PRIOR PROCEDURE OUTPUTS (load-bearing markers):\n"
        f"{_summarize_prior_steps(prior_steps)}\n\n"
        "Output requirements:\n"
        "  * `verdict`: one of "
        f"{list(_VERDICT_VOCAB)}.\n"
        "  * `verdict_detail` (optional but recommended): one paragraph "
        "naming the constraints / refusal reason / abstention rationale.\n"
        "  * `confidence`: a short qualifier (e.g. 'High on refusal of "
        "bundle-as-structured; medium on track-boundary definitions').\n"
        "  * `unresolved_uncertainty_sources`: at least 1 entry; each entry "
        "names something the run could not resolve and which would, if "
        "resolved, materially update the verdict.\n"
        "Emit nothing outside the structured tool output."
    )


# ---- Component -------------------------------------------------------------
class GovernanceKernel:
    """Owner of Step 9 (verdict, confidence, unresolved-uncertainty sources).

    Per architecture/05_governance_kernel.md and step_8_decision_package §2.
    Articles V/VI/VII ties. Step 11 absorbed into Step 9 (separate-outputs
    only on the same payload) per Step 8 §8.10.
    """

    component_id = "governance_kernel"
    article_ties = ("V", "VI", "VII")

    # ------------------------------------------------------------------
    # Step 9 — verdict + confidence + unresolved-uncertainty
    # ------------------------------------------------------------------
    def verdict_with_confidence_and_uncertainty(
        self,
        roadmap: Any,
        prior_steps: Any,
        *,
        run_context: RunContext,
        max_calls: int = _DEFAULT_MAX_CALLS,
    ) -> Dict[str, Any]:
        """Step 9: closed-set verdict + confidence + unresolved-uncertainty.

        `roadmap` must be a Step 8 output dict; `prior_steps` is a dict of
        prior committed step outputs keyed by step_id. Both are re-validated
        at the boundary for defence-in-depth (Article VI tie: refuse to
        adjudicate on an incoherent roadmap).

        Returns the parsed LLM output as a dict matching STEP_9_OUTPUT_SCHEMA:
            {
                "verdict": <enum: constrain|refuse|explicitly_abstain>,
                "verdict_detail": <str>,                # optional
                "confidence": <str>,                    # tied to >=1 source
                "unresolved_uncertainty_sources": [<str>, ...]  # minItems=1
            }

        Raises:
            ELIFError              — input is not a Step 8 dict or prior dict
            SchemaValidationError  — LLM response violates the pinned schema
            LLMAdapterError        — transport/parsing failure (live mode)
            LLMCallCapError        — per-run cap exhausted
        """
        rm = _require_step8_roadmap(roadmap)
        prior = _require_prior_steps(prior_steps)
        ctx = _require_run_context(run_context)

        prompt = _build_step9_prompt(rm, prior)
        fixture_id = (
            f"step_09__{_extract_case_token(ctx.case_id)}"
            if ctx.offline_mode
            else ""
        )

        payload = complete_structured(
            prompt=prompt,
            output_schema=STEP_9_OUTPUT_SCHEMA,
            max_calls=max_calls,
            offline_mode=ctx.offline_mode,
            offline_fixture_id=fixture_id,
            model_id=ctx.model_id,
        )

        # Defence-in-depth: the adapter already validated, but a malformed
        # live response or a tampered fixture should fail here too.
        validate_against_schema(payload, STEP_9_OUTPUT_SCHEMA)
        _enforce_step9_semantics(payload)
        return payload


# ---- Semantic post-validation (Articles V/VI/VII tie) ----------------------
def _enforce_step9_semantics(payload: Mapping[str, Any]) -> None:
    """Verify Step 9 semantics beyond what JSON Schema can express.

    Schema already requires the three load-bearing keys (verdict +
    confidence + unresolved_uncertainty_sources) with verdict in the closed
    set. We re-check explicitly so a malformed fixture or jsonschema-absent
    fallback path still halts here. Article VI tie: confidence must be tied
    to ≥1 named source (schema enforces minItems=1; we re-assert here).
    """
    verdict = payload.get("verdict")
    if verdict not in _VERDICT_VOCAB:
        raise SchemaValidationError(
            f"Step 9 output: `verdict` must be one of {list(_VERDICT_VOCAB)}; "
            f"got {verdict!r}"
        )
    confidence = payload.get("confidence")
    if not isinstance(confidence, str) or not confidence.strip():
        raise SchemaValidationError(
            "Step 9 output: `confidence` must be a non-empty string "
            "(Article VI: confidence must be tied to >=1 unresolved source)"
        )
    sources = payload.get("unresolved_uncertainty_sources")
    if not isinstance(sources, list) or len(sources) < 1:
        raise SchemaValidationError(
            "Step 9 output: `unresolved_uncertainty_sources` must be a "
            "non-empty list (Article VII: every verdict names >=1 "
            "unresolved source so Memory Logger can attach refutability)"
        )
    for i, src in enumerate(sources):
        if not isinstance(src, str) or not src.strip():
            raise SchemaValidationError(
                f"Step 9 output: unresolved_uncertainty_sources[{i}] must "
                "be a non-empty string"
            )


__all__ = ["GovernanceKernel"]
