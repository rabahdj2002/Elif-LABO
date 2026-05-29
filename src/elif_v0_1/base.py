"""ELIF v0.1 base: closed-set IDs, errors, frozen data shapes.

This module is LOAD-BEARING: every closed-set tuple below is doctrinal.
Adding entries requires formal doctrine revision + operator approval
(see CLAUDE.md "Closed-set discipline (DOCTRINAL)").

Step 8 §1 Q3.1 + Q6.1 explicitly rejected adding an 8th component.
The Constitutional Layer v0.4 is LOCKED at 7 Articles (I-VII).
The four failure-mode poles are doctrinal per v0.4.

Scaffold-stage: data classes are frozen but business logic lives elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


# ---- Closed-set component IDs (7, no 8th) ---------------------------------
# Anchored in notes/step_8_decision_package_v0_1.md §2 + architecture/.
COMPONENT_IDS: Tuple[str, ...] = (
    "frame_validator",
    "object_decomposer",
    "hypothesis_validator",
    "branching_roadmap_engine",
    "governance_kernel",
    "operative_truth_separator",
    "memory_logger",
)


# ---- Closed-set procedure step IDs (11, post-Step-8 compression) ----------
# Step 11 absorbed into Step 9; renumber per step_8_decision_package_v0_1.md §2.
PROCEDURE_STEP_IDS: Tuple[str, ...] = (
    "step_1",
    "step_2",
    "step_3",
    "step_4",
    "step_5",
    "step_6",
    "step_7",
    "step_8",
    "step_9",
    "step_10",
    "step_11",
)


# ---- Closed-set Article IDs (7, Constitutional Layer v0.4 LOCKED) ---------
ARTICLE_IDS: Tuple[str, ...] = ("I", "II", "III", "IV", "V", "VI", "VII")


# ---- Closed-set failure-mode poles (4, v0.4 four-pole taxonomy) -----------
FAILURE_MODE_POLES: Tuple[str, ...] = (
    "absolutization",
    "false_closure",
    "fragmentation",
    "sterile_equilibrium",
)


# ---- Errors ---------------------------------------------------------------
class ELIFError(Exception):
    """Base for all ELIF v0.1 errors."""


class FrameInvalidError(ELIFError):
    """Raised when the Frame Validator refuses a frame (Article II tie)."""


class GovernanceRefuseError(ELIFError):
    """Raised when the Governance Kernel refuses to proceed (Articles V/VI/VII)."""


class NonSelfPropagationError(ELIFError):
    """Raised if scaffold attempts autonomous progression without authorization."""


class LLMCallCapError(ELIFError):
    """Raised when an LLM call would exceed the per-run call cap.

    Step 8 §8.4: cost cap is `--max-llm-calls=22`. Cap is a hard halt;
    no silent retry on cap exhaustion. The runner observes this as a
    governance signal, not a transient error.
    """


class LLMAdapterError(ELIFError):
    """Raised on transport / API failure inside the LLM adapter.

    Distinct from `LLMCallCapError` (governance) — this is plumbing.
    """


class SchemaValidationError(ELIFError):
    """Raised when a structured-output dict fails its declared JSON Schema.

    Pinned schemas are doctrinal; drift in shape is a governance fail,
    not a soft warning. v0.4.0 schema_version is frozen per Step 8 §8.7.
    """


# ---- Frozen data shapes ---------------------------------------------------
@dataclass(frozen=True)
class InputFrame:
    """Input frame, locked at ingestion-time per non-self-propagation."""

    id: str
    text: str
    locked_at_iso: str
    doctrinal_scope_tag: str
    companion_case: str


@dataclass(frozen=True)
class ProcedureStepOutput:
    """One procedure-step output, committed sequentially (no revision)."""

    step_id: str
    content: object
    committed_at_iso: str
    time_box_status: str
