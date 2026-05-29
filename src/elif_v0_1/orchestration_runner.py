"""Procedure Runner — thin orchestration over the 7 components.

Per step_8_decision_package §6 + §8: sequential 11-step execution, commits
per step, no revision, time-box enforced. Calls components in the order
fixed by procedure/elif_mode_procedure_v1.0.md.

SCAFFOLD: ProcedureRunner.run raises NotImplementedError. Non-self-propagation
constraint applies — nothing autonomous proceeds without operator authorization.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from .base import (
    InputFrame,
    NonSelfPropagationError,
    PROCEDURE_STEP_IDS,
    ProcedureStepOutput,
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


@dataclass(frozen=True)
class RunReport:
    """Per-case run report — committed step outputs + meta."""

    case_id: str
    condition: str
    procedure_version: str
    step_outputs: Tuple[ProcedureStepOutput, ...] = field(default_factory=tuple)


# Step → owning component for the 11-step procedure (Step 8 §2.2 table).
STEP_OWNER: Tuple[Tuple[str, str], ...] = (
    ("step_1", "frame_validator"),
    ("step_2", "object_decomposer"),
    ("step_3", "frame_validator"),
    ("step_4", "hypothesis_validator"),
    ("step_5", "hypothesis_validator"),
    ("step_6", "object_decomposer"),
    ("step_7", "branching_roadmap_engine"),
    ("step_8", "branching_roadmap_engine"),
    ("step_9", "governance_kernel"),
    ("step_10", "operative_truth_separator"),
    ("step_11", "memory_logger"),
)


class ProcedureRunner:
    """Thin sequential orchestrator. Scaffold; does not run."""

    def __init__(self) -> None:
        self.frame_validator = FrameValidator()
        self.object_decomposer = ObjectDecomposer()
        self.hypothesis_validator = HypothesisValidator()
        self.branching_roadmap_engine = BranchingRoadmapEngine()
        self.governance_kernel = GovernanceKernel()
        self.operative_truth_separator = OperativeTruthSeparator()
        self.memory_logger = MemoryLogger()
        # Consistency: 11 step entries, last owned by memory_logger.
        assert len(STEP_OWNER) == len(PROCEDURE_STEP_IDS) == 11
        assert STEP_OWNER[-1] == ("step_11", "memory_logger")

    def run(
        self,
        case_id: str,
        condition: str,
        input_frame: InputFrame,
        procedure_version: str = "v1.0",
    ) -> RunReport:
        """Execute the 11-step procedure sequentially. SCAFFOLD: refuses."""
        raise NonSelfPropagationError(
            "scaffold: ProcedureRunner.run is not authorized to execute. "
            "Operator build authorization required (planning != build)."
        )
