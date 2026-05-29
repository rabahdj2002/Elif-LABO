"""ELIF v0.1 scaffold package.

This package encodes the architecture decided in
`notes/step_8_decision_package_v0_1.md`. It is a SCAFFOLD — every component
method raises NotImplementedError. Operator authorization is required to
convert scaffold to implementation (planning != build authorization).

Public API surface:
    COMPONENT_IDS, PROCEDURE_STEP_IDS, ARTICLE_IDS, FAILURE_MODE_POLES
    ELIFError, FrameInvalidError, GovernanceRefuseError, NonSelfPropagationError
    InputFrame, ProcedureStepOutput
    assert_consistent()
    VERSION
"""

from __future__ import annotations

from .base import (
    ARTICLE_IDS,
    COMPONENT_IDS,
    ELIFError,
    FAILURE_MODE_POLES,
    FrameInvalidError,
    GovernanceRefuseError,
    InputFrame,
    NonSelfPropagationError,
    PROCEDURE_STEP_IDS,
    ProcedureStepOutput,
)

VERSION = "0.1.0-scaffold"

__all__ = [
    "ARTICLE_IDS",
    "COMPONENT_IDS",
    "ELIFError",
    "FAILURE_MODE_POLES",
    "FrameInvalidError",
    "GovernanceRefuseError",
    "InputFrame",
    "NonSelfPropagationError",
    "PROCEDURE_STEP_IDS",
    "ProcedureStepOutput",
    "VERSION",
    "assert_consistent",
]


def assert_consistent() -> None:
    """Closed-set guard — fires at import. Pure cardinality / uniqueness check.

    No I/O, no recursion into components, no side effects. If any closed-set
    drifts from doctrine, import fails loudly rather than silently expanding.
    """
    if len(COMPONENT_IDS) != 7:
        raise AssertionError(
            f"COMPONENT_IDS must be exactly 7 (Step 8 §1 no 8th component); "
            f"got {len(COMPONENT_IDS)}"
        )
    if len(set(COMPONENT_IDS)) != len(COMPONENT_IDS):
        raise AssertionError("COMPONENT_IDS must be unique")
    if len(PROCEDURE_STEP_IDS) != 11:
        raise AssertionError(
            f"PROCEDURE_STEP_IDS must be exactly 11 (Step 8 compression); "
            f"got {len(PROCEDURE_STEP_IDS)}"
        )
    if len(set(PROCEDURE_STEP_IDS)) != len(PROCEDURE_STEP_IDS):
        raise AssertionError("PROCEDURE_STEP_IDS must be unique")
    if ARTICLE_IDS != ("I", "II", "III", "IV", "V", "VI", "VII"):
        raise AssertionError(
            "ARTICLE_IDS must be the v0.4 LOCKED 7 Articles (I-VII)"
        )
    if len(FAILURE_MODE_POLES) != 4:
        raise AssertionError(
            f"FAILURE_MODE_POLES must be exactly 4 (v0.4 four-pole taxonomy); "
            f"got {len(FAILURE_MODE_POLES)}"
        )


# Fire the guard at import — drift fails imports, not runtime calls.
assert_consistent()
