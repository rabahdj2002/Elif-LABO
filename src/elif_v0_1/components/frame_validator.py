"""Frame Validator — Step 1 owner.

Article tie: Article II (the frame must survive scrutiny before reasoning
proceeds) and Article V (refusal-capability). Sub-behaviors:
    * Step 3 — surface_assumptions
    * Step 7 mode B — surface_deeper_frame_rejection (deeper-frame-rejection
      trajectories; the modeA cousin is owned by BranchingRoadmapEngine)

Per `notes/elif_v0_1_build_plan.md` §2.1 and `step_8_decision_package_v0_1.md`
§2. Per §8.9 — each LLM call starts fresh (no sub-behavior state retained
between methods). Per §8.8 — offline fixture mode is in scope.

Public method signatures are pinned by the scaffold:
    validate(input_frame)
    surface_assumptions(input_frame)
    surface_deeper_frame_rejection(input_frame)

Run-context (offline_mode, max_llm_calls, case_id) is injected via the
constructor so the pinned method shapes are not altered. The orchestrator
constructs FrameValidator() with no args during scaffold-mode wiring; the
production wiring passes a RunContext.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..base import ELIFError, InputFrame
from ..llm_adapter import complete_structured
from ..run_context import RunContext
from ..schemas import schema_for

# Default cap used when the component is constructed without a RunContext.
# Operator-locked at v0.1 §8.4 == 22 calls per run.
_DEFAULT_MAX_LLM_CALLS = 22

# Article-II framing reused across all three sub-behaviors. Closed-set
# discipline: the verdict vocabulary lives in the schema; we cite it here so
# the model never invents synonyms.
_SYSTEM_PREFACE = (
    "You are the ELIF v0.1 Frame Validator. Your sole responsibility is "
    "Article II: refuse to let reasoning proceed until the input frame has "
    "survived structural scrutiny. You never invent vocabulary outside the "
    "closed-set enums declared in the structured-output schema. You never "
    "retain state between calls (decision package §8.9)."
)


def _case_suffix(run_context: Optional[RunContext]) -> str:
    """Derive the fixture case suffix (e.g. 'case_01') from the run context.

    Fixtures are named `step_NN__case_MM.json`. The case_id on RunContext is
    typically of the form 'case_01_electroculture'; we extract the canonical
    'case_MM' stem. If no run_context is provided, falls back to 'case_01'
    so unit tests have a deterministic default.
    """
    if run_context is None:
        return "case_01"
    cid = run_context.case_id
    # Accept the canonical 'case_NN_*' form.
    parts = cid.split("_")
    if len(parts) >= 2 and parts[0] == "case":
        # Pad to 2 digits to match fixture naming.
        try:
            n = int(parts[1])
            return f"case_{n:02d}"
        except ValueError:
            pass
    return cid


def _validate_input_frame(input_frame: Any) -> None:
    """Reject anything that is not an InputFrame dataclass.

    Doctrinal: structural-shape errors are loud at the boundary, not
    silently coerced. Uses ELIFError so the runner can route uniformly.
    """
    if not isinstance(input_frame, InputFrame):
        raise ELIFError(
            f"FrameValidator requires an InputFrame instance; got "
            f"{type(input_frame).__name__}"
        )


class FrameValidator:
    """Owner of Step 1 + sub-behaviors Step 3 and Step 7-modeB.

    Per architecture/01_frame_validator.md and step_8_decision_package §2.
    Article II tie: refuses to proceed until frame survives inspection.
    Article V tie: refusal-capability surfaced through `verdict=invalid`.
    """

    component_id = "frame_validator"
    article_ties = ("II", "V")

    def __init__(self, run_context: Optional[RunContext] = None) -> None:
        # run_context may be None during scaffold construction; the
        # orchestrator passes a RunContext at run-start. Each method is
        # individually robust to a None context (offline_mode defaults to
        # False, fixture suffix defaults to case_01 for tests).
        self._run_context = run_context

    # ------------------------------------------------------------------
    # Step 1 — validate (closed-set verdict)
    # ------------------------------------------------------------------
    def validate(self, input_frame: InputFrame) -> Dict[str, Any]:
        """Step 1: emit verdict in {valid, invalid, needs_decomposition}.

        Returns the structured-output dict matching STEP_1_OUTPUT_SCHEMA:
            {
                "verdict": <enum>,
                "reasoning": <str>,
                "reformulated_frame": <str>  # optional; required when
                                              # verdict != "valid"
            }

        Raises:
            ELIFError           — input is not an InputFrame
            SchemaValidationError — LLM response violates the pinned schema
            LLMAdapterError     — transport/parsing failure (live mode)
            LLMCallCapError     — per-run cap exhausted
        """
        _validate_input_frame(input_frame)
        schema = schema_for("step_1")
        prompt = self._build_step1_prompt(input_frame)
        payload = self._call_llm(
            prompt=prompt,
            schema=schema,
            step_number=1,
        )
        return payload

    # ------------------------------------------------------------------
    # Step 3 — surface_assumptions
    # ------------------------------------------------------------------
    def surface_assumptions(self, input_frame: InputFrame) -> Dict[str, Any]:
        """Step 3: enumerate hidden assumptions in the frame.

        Returns the structured-output dict matching STEP_3_OUTPUT_SCHEMA:
            { "assumptions": [<declarative str>, ...] }  # >= 2 entries

        Per build plan §2.1: each entry must be a declarative statement
        (no '?' as final character). The system prompt instructs the model;
        schema-side validation catches structural drift.
        """
        _validate_input_frame(input_frame)
        schema = schema_for("step_3")
        prompt = self._build_step3_prompt(input_frame)
        payload = self._call_llm(
            prompt=prompt,
            schema=schema,
            step_number=3,
        )
        return payload

    # ------------------------------------------------------------------
    # Step 7 mode B — deeper-frame-rejection trajectories
    # ------------------------------------------------------------------
    def surface_deeper_frame_rejection(
        self, input_frame: InputFrame
    ) -> Dict[str, Any]:
        """Step 7-modeB: deeper-frame-rejection trajectories.

        Returns the structured-output dict matching STEP_7_OUTPUT_SCHEMA:
            { "trajectories": [
                {"trajectory_id": <str>,
                 "tag": "deeper-frame-rejection" | "outside-original-frame",
                 "reason": <str>},
                ...
            ] }

        The Frame Validator emits modeB (deeper-frame-rejection) trajectories;
        modeA (outside-original-frame) is owned by BranchingRoadmapEngine.
        Per build plan §2.1, modeB may be empty (>= 0 entries); the schema
        enforces minItems=1 on `trajectories` at the cohort level, so this
        method always emits at least one trajectory or, in genuinely empty
        cases, the orchestrator routes around modeB rather than producing a
        zero-item array (handled at the runner level, not here).
        """
        _validate_input_frame(input_frame)
        schema = schema_for("step_7")
        prompt = self._build_step7_modeB_prompt(input_frame)
        payload = self._call_llm(
            prompt=prompt,
            schema=schema,
            step_number=7,
        )
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
            self._run_context.model_id
            if self._run_context
            else "sonnet"
        )
        fixture_id = ""
        if offline_mode:
            fixture_id = (
                f"step_{step_number:02d}__{_case_suffix(self._run_context)}"
            )
        return complete_structured(
            prompt=prompt,
            output_schema=schema,
            max_calls=max_calls,
            offline_mode=offline_mode,
            offline_fixture_id=fixture_id,
            model_id=model_id,
        )

    def _build_step1_prompt(self, input_frame: InputFrame) -> str:
        return (
            f"{_SYSTEM_PREFACE}\n\n"
            "TASK: Step 1 — Frame validation.\n"
            "Emit a verdict from the closed set: "
            "{valid, invalid, needs_decomposition}.\n"
            "  * 'valid' — the frame is well-posed and reasoning may proceed.\n"
            "  * 'invalid' — the frame fails Article II; reasoning must halt.\n"
            "  * 'needs_decomposition' — the frame bundles distinct decisions "
            "and must be reformulated before reasoning proceeds.\n"
            "If verdict is not 'valid', you MUST emit a `reformulated_frame` "
            "rewriting the frame so it is decidable.\n\n"
            f"INPUT FRAME (id={input_frame.id}, "
            f"scope_tag={input_frame.doctrinal_scope_tag}):\n"
            f"{input_frame.text}\n"
        )

    def _build_step3_prompt(self, input_frame: InputFrame) -> str:
        return (
            f"{_SYSTEM_PREFACE}\n\n"
            "TASK: Step 3 — Surface the hidden assumptions in the frame.\n"
            "Emit AT LEAST TWO assumptions. Each assumption MUST be a "
            "declarative statement (no question marks). Do not restate the "
            "frame; surface what the frame takes for granted.\n\n"
            f"INPUT FRAME (id={input_frame.id}):\n"
            f"{input_frame.text}\n"
        )

    def _build_step7_modeB_prompt(self, input_frame: InputFrame) -> str:
        return (
            f"{_SYSTEM_PREFACE}\n\n"
            "TASK: Step 7 mode B — Deeper-frame-rejection trajectories.\n"
            "Emit trajectories that REJECT the deeper frame (the implicit "
            "assumption that the proposed framing is itself the right one). "
            "Each trajectory must include a one-line `reason`. Use the tag "
            "'deeper-frame-rejection' when emitting modeB content; "
            "'outside-original-frame' is reserved for the Branching Roadmap "
            "Engine.\n\n"
            f"INPUT FRAME (id={input_frame.id}):\n"
            f"{input_frame.text}\n"
        )


__all__ = ["FrameValidator"]
