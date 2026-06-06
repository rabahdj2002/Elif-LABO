"""ELIF v0.1 run-context dataclasses.

Three frozen dataclasses pin the orchestrator-to-component contract for
a single procedure run. They are intentionally narrow — no behavior, no
I/O, no mutation. Construction-time validation only.

Per `notes/elif_v0_1_build_plan.md` §1.2 + Step 8 §8 decision package:
    * RunContext         — per-run invariants (case_id, condition, ...)
    * StepOutputEnvelope — what a single procedure step commits
    * RunReport          — what the orchestrator returns at the end

Closed-set membership (condition, time_box_status) is enforced at
construction; runtime-broken contracts fail loud here rather than
silently leaking through the rest of the system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

from .base import PROCEDURE_STEP_IDS

# Closed set: which condition column of the 3-case benchmark this run is
# producing. Step 6 cross-case analysis fixed these.
CONDITION_IDS: Tuple[str, ...] = ("a", "b", "c")

# Closed set: per-step time-box outcome. Matches PROCEDURE_STEP_OUTPUT_SCHEMA.
TIME_BOX_STATUSES: Tuple[str, ...] = (
    "within_budget",
    "exceeded_budget",
    "aborted",
)


def _ensure_str_nonempty(field_name: str, value: Any) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be a non-empty str; got {value!r}")


@dataclass(frozen=True)
class RunContext:
    """Per-run invariants. Constructed once at run start; never mutated.

    Fields:
        case_id            — e.g. "case_01_electroculture"
        condition          — one of {"a","b","c"} (CONDITION_IDS)
        procedure_version  — e.g. "v1.0" (Step 8 §8.2 — v1.0 only at v0.1)
        offline_mode       — fixtures-only run (no network)
        max_llm_calls      — per-run cost cap (Step 8 §8.4 default: 22)
        model_id           — e.g. "claude-3-5-sonnet-20240620" (Override default model)
        started_at_iso     — ISO 8601 start timestamp (UTC recommended)
        run_id             — unique per-run identifier
        language_instruction — Optional language hint for output.
    """

    case_id: str
    condition: str
    procedure_version: str
    offline_mode: bool
    max_llm_calls: int
    model_id: str
    started_at_iso: str
    run_id: str
    language_instruction: str = ""

    def __post_init__(self) -> None:
        _ensure_str_nonempty("case_id", self.case_id)
        _ensure_str_nonempty("procedure_version", self.procedure_version)
        _ensure_str_nonempty("started_at_iso", self.started_at_iso)
        _ensure_str_nonempty("run_id", self.run_id)
        if self.condition not in CONDITION_IDS:
            raise ValueError(
                f"condition must be one of {CONDITION_IDS}; got {self.condition!r}"
            )
        if not isinstance(self.offline_mode, bool):
            raise ValueError(
                f"offline_mode must be bool; got {type(self.offline_mode).__name__}"
            )
        if not isinstance(self.max_llm_calls, int) or self.max_llm_calls < 1:
            raise ValueError(
                f"max_llm_calls must be a positive int; got {self.max_llm_calls!r}"
            )


@dataclass(frozen=True)
class StepOutputEnvelope:
    """One committed step output.

    Fields:
        step_id                — closed-set member of PROCEDURE_STEP_IDS
        content                — opaque per-step content (dict | str | list)
        committed_at_iso       — ISO 8601 commit timestamp
        llm_calls_used         — int >= 0; LLM calls this step consumed
        time_box_status        — closed-set member of TIME_BOX_STATUSES
        structured_output_dict — full structured payload returned by the LLM
    """

    step_id: str
    content: Any
    committed_at_iso: str
    llm_calls_used: int
    time_box_status: str
    structured_output_dict: Dict[str, Any]
    usage_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.step_id not in PROCEDURE_STEP_IDS:
            raise ValueError(
                f"step_id must be one of PROCEDURE_STEP_IDS; got {self.step_id!r}"
            )
        _ensure_str_nonempty("committed_at_iso", self.committed_at_iso)
        if (
            not isinstance(self.llm_calls_used, int)
            or self.llm_calls_used < 0
        ):
            raise ValueError(
                f"llm_calls_used must be a non-negative int; got "
                f"{self.llm_calls_used!r}"
            )
        if self.time_box_status not in TIME_BOX_STATUSES:
            raise ValueError(
                f"time_box_status must be one of {TIME_BOX_STATUSES}; "
                f"got {self.time_box_status!r}"
            )
        if not isinstance(self.structured_output_dict, dict):
            raise ValueError("structured_output_dict must be a dict")


@dataclass(frozen=True)
class RunReport:
    """Per-run report. Returned by the orchestrator.

    Fields:
        run_context                  — the RunContext for the run
        step_outputs                 — tuple of committed step envelopes
        memory_logger_entries_written — count of MemoryLogger events written
        exit_code                    — 0 = success; non-zero = governance halt
        completed_at_iso             — ISO 8601 completion timestamp
    """

    run_context: RunContext
    step_outputs: Tuple[StepOutputEnvelope, ...] = field(default_factory=tuple)
    memory_logger_entries_written: int = 0
    exit_code: int = 0
    completed_at_iso: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.run_context, RunContext):
            raise ValueError("run_context must be a RunContext instance")
        if not isinstance(self.step_outputs, tuple):
            raise ValueError("step_outputs must be a tuple")
        for i, env in enumerate(self.step_outputs):
            if not isinstance(env, StepOutputEnvelope):
                raise ValueError(
                    f"step_outputs[{i}] must be a StepOutputEnvelope"
                )
        if (
            not isinstance(self.memory_logger_entries_written, int)
            or self.memory_logger_entries_written < 0
        ):
            raise ValueError(
                "memory_logger_entries_written must be a non-negative int"
            )
        if not isinstance(self.exit_code, int):
            raise ValueError("exit_code must be an int")
        if not isinstance(self.completed_at_iso, str):
            raise ValueError("completed_at_iso must be a str")


__all__ = [
    "CONDITION_IDS",
    "TIME_BOX_STATUSES",
    "RunContext",
    "StepOutputEnvelope",
    "RunReport",
]
