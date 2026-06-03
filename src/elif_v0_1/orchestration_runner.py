"""Procedure Runner — thin orchestration over the 7 components.

Per `notes/step_8_decision_package_v0_1.md` §6 + §8 and
`notes/elif_v0_1_build_plan.md` §4: sequential 11-step execution, commits
per step, no revision once committed. Calls components in the order fixed
by `procedure/elif_mode_procedure_v1.0.md`.

The runner replaces the scaffold's NonSelfPropagationError stub. Build plan
§4 non-self-propagation discipline is preserved through the explicit-parameter
contract on `ProcedureRunner.run` itself (the caller must declare case_id,
condition, input_frame, and offline_mode / max_llm_calls before execution).

Halt modes (build plan §4.4):
    FrameInvalidError       -> exit code 10
    GovernanceRefuseError   -> exit code 20
    SchemaValidationError   -> exit code 30

Returns a `RunReport` whose `step_outputs` carries one StepOutputEnvelope per
committed step.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .base import (
    FrameInvalidError,
    GovernanceRefuseError,
    InputFrame,
    LLMCallCapError,
    PROCEDURE_STEP_IDS,
    SchemaValidationError,
)
from .components import (
    BranchingRoadmapEngine,
    FrameValidator,
    GovernanceKernel,
    HypothesisValidator,
    MemoryLogger,
    ObjectDecomposer,
    OperativeTruthSeparator,
)
from .llm_adapter import reset_call_counter, _call_counter
from .run_context import RunContext, RunReport, StepOutputEnvelope


# Step -> owning component for the 11-step procedure (build plan §4.1 table).
STEP_OWNER: Tuple[Tuple[str, str], ...] = (
    ("step_1", "frame_validator"),
    ("step_2", "object_decomposer"),
    ("step_3", "frame_validator"),
    ("step_4", "hypothesis_validator"),
    ("step_5", "hypothesis_validator"),
    ("step_6", "object_decomposer"),
    ("step_7", "branching_roadmap_engine"),  # mode A; mode B is FrameValidator
    ("step_8", "branching_roadmap_engine"),
    ("step_9", "governance_kernel"),
    ("step_10", "operative_truth_separator"),
    ("step_11", "memory_logger"),
)


def _utc_now_iso() -> str:
    """ISO-8601 UTC timestamp string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _new_run_id() -> str:
    """Stable per-run identifier."""
    return f"run_{uuid.uuid4().hex}"


class ProcedureRunner:
    """Thin sequential orchestrator over the 7 components.

    The runner is constructible without arguments. Components are
    instantiated lazily per-run inside `run` so that each call begins
    with a fresh component-side run_context (decision §8.9: each LLM call
    starts fresh; the runner does not carry any inter-run state).
    """

    def __init__(self) -> None:
        # Structural assertions on closed-set wiring. These fire at
        # construction so an 8th step or out-of-order owner table fails
        # loudly here rather than three steps into a run.
        assert len(STEP_OWNER) == len(PROCEDURE_STEP_IDS) == 11
        assert STEP_OWNER[-1] == ("step_11", "memory_logger")
        assert tuple(s for s, _ in STEP_OWNER) == PROCEDURE_STEP_IDS

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------
    def run(
        self,
        case_id: str,
        condition: str,
        input_frame: InputFrame,
        *,
        offline_mode: bool = False,
        max_llm_calls: int = 22,
        model_id: str = "claude-sonnet-4-6",
        procedure_version: str = "v1.0",
        results_dir: Optional[Path] = None,
    ) -> RunReport:
        """Execute the 11-step procedure sequentially.

        Args:
            case_id            — canonical case id (e.g. "case_01_electroculture")
            condition          — one of {"a","b","c"}
            input_frame        — frozen `InputFrame` instance
            offline_mode       — load fixtures instead of calling Anthropic
            max_llm_calls      — per-run hard cap (default 22 per §8.4)
            model_id           — e.g. "claude-sonnet-4-6" (Step 8 §8.4)
            procedure_version  — "v1.0" (the only authorized v0.1 version)
            results_dir        — optional path for MemoryLogger persistence;
                                 defaults to .memory_logger/ under cwd

        Returns:
            RunReport          — step outputs + exit_code + meta

        Halts:
            FrameInvalidError       -> RunReport.exit_code = 10
            GovernanceRefuseError   -> RunReport.exit_code = 20
            SchemaValidationError   -> RunReport.exit_code = 30
            LLMCallCapError         -> RunReport.exit_code = 30 (governance
                                       signal per §8.4; treated as schema-class
                                       halt for downstream forensics)
        """
        # Reset the per-process call counter so each run begins at 0 against
        # its own max_llm_calls cap.
        reset_call_counter()

        run_context = RunContext(
            case_id=case_id,
            condition=condition,
            procedure_version=procedure_version,
            offline_mode=offline_mode,
            max_llm_calls=max_llm_calls,
            model_id=model_id,
            started_at_iso=_utc_now_iso(),
            run_id=_new_run_id(),
        )

        # Construct components fresh per run. FrameValidator + BRE take
        # run_context via ctor; the other LLM-using components take it as
        # a keyword argument to the per-step methods. MemoryLogger takes
        # neither (architecture-dependent; no LLM calls).
        frame_validator = FrameValidator(run_context=run_context)
        object_decomposer = ObjectDecomposer()
        hypothesis_validator = HypothesisValidator()
        branching_roadmap_engine = BranchingRoadmapEngine(
            run_context=run_context
        )
        governance_kernel = GovernanceKernel()
        operative_truth_separator = OperativeTruthSeparator()
        memory_logger = MemoryLogger(base_persistence_dir=results_dir)

        prior_outputs: Dict[str, Dict[str, Any]] = {}
        step_envelopes: List[StepOutputEnvelope] = []

        # Initial open event for the run.
        try:
            memory_logger.write_event(
                case_id=run_context.case_id,
                event={
                    "event_type": "open",
                    "payload": {
                        "run_id": run_context.run_id,
                        "case_id": run_context.case_id,
                        "condition": run_context.condition,
                        "procedure_version": run_context.procedure_version,
                        "offline_mode": run_context.offline_mode,
                        "max_llm_calls": run_context.max_llm_calls,
                        "started_at_iso": run_context.started_at_iso,
                    },
                },
            )
        except Exception:
            # MemoryLogger persistence failures must not silently swallow a
            # run; re-raise so the operator sees the storage problem.
            raise

        # ------------------------------------------------------------------
        # Step dispatcher
        # ------------------------------------------------------------------
        def commit_step(step_id: str, payload: Dict[str, Any]) -> None:
            """Capture a committed step output + write a step_committed event."""
            print(f"[COMMIT] {step_id}: {STEP_OWNER[int(step_id.split('_')[1])-1][1].upper()} logic finalized.")
            current_calls = _call_counter()
            envelope = StepOutputEnvelope(
                step_id=step_id,
                content=payload,
                committed_at_iso=_utc_now_iso(),
                llm_calls_used=current_calls,
                time_box_status="within_budget",
                structured_output_dict=payload,
            )
            step_envelopes.append(envelope)
            prior_outputs[step_id] = payload
            memory_logger.write_event(
                case_id=run_context.case_id,
                event={
                    "event_type": "step_committed",
                    "payload": {
                        "step_id": step_id,
                        "llm_calls_used": current_calls,
                        "committed_at_iso": envelope.committed_at_iso,
                    },
                },
            )

        # ------------------------------------------------------------------
        # 11-step execution
        # ------------------------------------------------------------------
        try:
            # Step 1 — Frame validation.
            print(f"[PROCESS] Initializing Step 1: Frame Validator...")
            step_1 = frame_validator.validate(input_frame)
            commit_step("step_1", step_1)
            if step_1.get("verdict") == "invalid":
                # Article II tie: refuse to let reasoning proceed.
                self._emit_refutation(
                    memory_logger,
                    run_context,
                    trigger="frame_invalid",
                    halt_reason="Step 1 returned verdict=invalid",
                )
                self._emit_close(
                    memory_logger, run_context, exit_code=10
                )
                raise FrameInvalidError(
                    "Step 1 returned verdict=invalid; halting run"
                )

            # Step 2 — Family-axis decomposition.
            print(f"[PROCESS] Transitioning to Step 2: Object Decomposer...")
            step_2 = object_decomposer.decompose(
                input_frame,
                run_context=run_context,
                max_calls=run_context.max_llm_calls,
            )
            commit_step("step_2", step_2)

            # Step 3 — Surface assumptions.
            step_3 = frame_validator.surface_assumptions(input_frame)
            commit_step("step_3", step_3)

            # Step 4 — Hypotheses with distinguishing predictions.
            step_4 = (
                hypothesis_validator
                .enumerate_hypotheses_with_distinguishing_predictions(
                    step_2,
                    run_context=run_context,
                    max_calls=run_context.max_llm_calls,
                )
            )
            commit_step("step_4", step_4)

            # Step 5 — Failure conditions per hypothesis.
            step_5 = hypothesis_validator.failure_conditions_per_hypothesis(
                step_4,
                run_context=run_context,
                max_calls=run_context.max_llm_calls,
            )
            commit_step("step_5", step_5)

            # Step 6 — Multi-scale relations.
            step_6 = object_decomposer.multi_scale_relate(
                step_2,
                run_context=run_context,
                max_calls=run_context.max_llm_calls,
            )
            commit_step("step_6", step_6)

            # Step 7 — split: mode A (BRE) commits as step_7; mode B
            # (FrameValidator deeper-frame-rejection) is generated alongside
            # but the canonical committed envelope tracks mode A per
            # build plan §4.1 (Step 8 reads mode A only).
            step_7_modeA = (
                branching_roadmap_engine
                .outside_frame_trajectories_bre_feed(step_4, step_5)
            )
            # Mode B is executed for Article II / Article V continuity but
            # not committed as a separate envelope (decision §8.10: Step 7
            # split is "separate outputs only" — the mode-B payload is
            # logged as a memory event for forensics).
            try:
                step_7_modeB = (
                    frame_validator.surface_deeper_frame_rejection(input_frame)
                )
                memory_logger.write_event(
                    case_id=run_context.case_id,
                    event={
                        "event_type": "step_committed",
                        "payload": {
                            "step_id": "step_7_modeB",
                            "note": (
                                "frame-validator deeper-frame-rejection "
                                "trajectories"
                            ),
                            "trajectories_count": len(
                                step_7_modeB.get("trajectories", [])
                            ),
                        },
                    },
                )
            except SchemaValidationError:
                # Mode B is permitted to be empty in practice (build plan
                # §2.1). A schema fail here would re-surface in mode A, so
                # we re-raise to halt rather than swallow.
                raise
            commit_step("step_7", step_7_modeA)

            # Step 8 — Stage-gated roadmap.
            print(f"[PROCESS] Transitioning to Step 8: Branching Roadmap Engine...")
            step_8 = branching_roadmap_engine.stage_gated_roadmap(step_7_modeA)
            commit_step("step_8", step_8)

            # Step 9 — Governance verdict + confidence + uncertainty.
            print(f"[PROCESS] Transitioning to Step 9: Governance Kernel (Article VI Adjudication)...")
            step_9 = (
                governance_kernel
                .verdict_with_confidence_and_uncertainty(
                    step_8,
                    prior_outputs,
                    run_context=run_context,
                    max_calls=run_context.max_llm_calls,
                )
            )
            commit_step("step_9", step_9)
            # G0 Position B (adjudicated 2026-05-30): refusal is sovereign
            # but is not a silent termination. On verdict=refuse, the
            # refutation event is preserved (refusal stays refusal), then
            # Step 10 fires with a constrained refusal-closure payload and
            # Step 11 records the closing summary. The close event is
            # emitted at end-of-run with exit_code=20. The verdict itself
            # is NOT modified; the closed-set verdict vocabulary stays
            # frozen at {constrain, refuse, explicitly_abstain}.
            refuse_branch = step_9.get("verdict") == "refuse"
            if refuse_branch:
                self._emit_refutation(
                    memory_logger,
                    run_context,
                    trigger="governance_refuse",
                    halt_reason=str(step_9.get("verdict_detail") or "refuse"),
                )
                # Step 10 — constrained post-refusal closure (no LLM call).
                step_10 = operative_truth_separator.separate_for_refusal(
                    prior_outputs,
                    run_context=run_context,
                )
                commit_step("step_10", step_10)
            else:
                # Step 10 — Operative vs theoretical separation (live path).
                print(f"[PROCESS] Transitioning to Step 10: Operative Truth Separator (Final Verdict)...")
                step_10 = (
                    operative_truth_separator
                    .separate_operative_from_theoretical(
                        prior_outputs,
                        run_context=run_context,
                        max_calls=run_context.max_llm_calls,
                    )
                )
                commit_step("step_10", step_10)

            # Step 11 — Memory Logger summary. No LLM call; we record the
            # closing summary as a structured event payload + commit a
            # synthesized envelope so the procedure step is represented in
            # RunReport.step_outputs.
            run_summary = {
                "run_id": run_context.run_id,
                "case_id": run_context.case_id,
                "condition": run_context.condition,
                "procedure_version": run_context.procedure_version,
                "step_count": len(step_envelopes),
                "final_verdict": step_9.get("verdict"),
                "llm_calls_used": _call_counter(),
                "post_refusal_closure": refuse_branch,
            }
            memory_logger.write_event(
                case_id=run_context.case_id,
                event={
                    "event_type": "step_committed",
                    "payload": {
                        "step_id": "step_11",
                        "run_summary": run_summary,
                    },
                },
            )
            step_11_envelope = StepOutputEnvelope(
                step_id="step_11",
                content=run_summary,
                committed_at_iso=_utc_now_iso(),
                llm_calls_used=_call_counter(),
                time_box_status="within_budget",
                structured_output_dict=run_summary,
            )
            step_envelopes.append(step_11_envelope)
            prior_outputs["step_11"] = run_summary

            # End-of-run close. exit_code=20 on refuse-branch (G0 Position B);
            # exit_code=0 on clean runs. The verdict itself remains in
            # step_9; the exit code carries the halt-class signal forward.
            final_exit_code = 20 if refuse_branch else 0
            self._emit_close(
                memory_logger, run_context, exit_code=final_exit_code
            )
            return RunReport(
                run_context=run_context,
                step_outputs=tuple(step_envelopes),
                memory_logger_entries_written=self._count_memory_events(
                    memory_logger, run_context.case_id
                ),
                exit_code=final_exit_code,
                completed_at_iso=_utc_now_iso(),
            )

        except FrameInvalidError:
            return RunReport(
                run_context=run_context,
                step_outputs=tuple(step_envelopes),
                memory_logger_entries_written=self._count_memory_events(
                    memory_logger, run_context.case_id
                ),
                exit_code=10,
                completed_at_iso=_utc_now_iso(),
            )
        except GovernanceRefuseError:
            return RunReport(
                run_context=run_context,
                step_outputs=tuple(step_envelopes),
                memory_logger_entries_written=self._count_memory_events(
                    memory_logger, run_context.case_id
                ),
                exit_code=20,
                completed_at_iso=_utc_now_iso(),
            )
        except SchemaValidationError as exc:
            self._emit_refutation(
                memory_logger,
                run_context,
                trigger="schema_violation",
                halt_reason=str(exc),
            )
            self._emit_close(memory_logger, run_context, exit_code=30)
            return RunReport(
                run_context=run_context,
                step_outputs=tuple(step_envelopes),
                memory_logger_entries_written=self._count_memory_events(
                    memory_logger, run_context.case_id
                ),
                exit_code=30,
                completed_at_iso=_utc_now_iso(),
            )
        except LLMCallCapError as exc:
            self._emit_refutation(
                memory_logger,
                run_context,
                trigger="llm_call_cap_exceeded",
                halt_reason=str(exc),
            )
            self._emit_close(memory_logger, run_context, exit_code=30)
            return RunReport(
                run_context=run_context,
                step_outputs=tuple(step_envelopes),
                memory_logger_entries_written=self._count_memory_events(
                    memory_logger, run_context.case_id
                ),
                exit_code=30,
                completed_at_iso=_utc_now_iso(),
            )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    @staticmethod
    def _emit_refutation(
        memory_logger: MemoryLogger,
        run_context: RunContext,
        *,
        trigger: str,
        halt_reason: str,
    ) -> None:
        memory_logger.write_event(
            case_id=run_context.case_id,
            event={
                "event_type": "refutation",
                "payload": {
                    "run_id": run_context.run_id,
                    "trigger": trigger,
                    "halt_reason": halt_reason,
                },
            },
        )

    @staticmethod
    def _emit_close(
        memory_logger: MemoryLogger,
        run_context: RunContext,
        *,
        exit_code: int,
    ) -> None:
        memory_logger.write_event(
            case_id=run_context.case_id,
            event={
                "event_type": "close",
                "payload": {
                    "run_id": run_context.run_id,
                    "exit_code": exit_code,
                    "completed_at_iso": _utc_now_iso(),
                },
            },
        )

    @staticmethod
    def _count_memory_events(
        memory_logger: MemoryLogger, case_id: str
    ) -> int:
        try:
            state = memory_logger.read_case_state(case_id)
            return int(state.get("event_count", 0))
        except Exception:
            return 0


__all__ = ["ProcedureRunner", "RunReport", "STEP_OWNER"]
