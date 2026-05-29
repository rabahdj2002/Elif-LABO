"""Frame Validator — Step 1 owner.

Article tie: Article II (the frame must survive scrutiny before reasoning
proceeds). Sub-behaviors: Step 3 assumption surfacing, Step 7 deeper-frame
rejection trajectories.

SCAFFOLD: methods raise NotImplementedError. Do not call.
"""

from __future__ import annotations

from typing import Any

from ..base import InputFrame


class FrameValidator:
    """Owner of Step 1 + sub-behaviors Step 3 and Step 7 (deeper-frame side).

    Per architecture/01_frame_validator.md and step_8_decision_package §2.
    Article II tie: refuses to proceed until frame survives inspection.
    """

    component_id = "frame_validator"
    article_ties = ("II",)

    def validate(self, input_frame: InputFrame) -> Any:
        """Step 1: emit verdict {valid | invalid | needs_decomposition}."""
        raise NotImplementedError("scaffold: validate not implemented")

    def surface_assumptions(self, input_frame: InputFrame) -> Any:
        """Step 3 sub-behavior: enumerate hidden assumptions in the frame."""
        raise NotImplementedError(
            "scaffold: surface_assumptions not implemented"
        )

    def surface_deeper_frame_rejection(self, input_frame: InputFrame) -> Any:
        """Step 7 sub-behavior: deeper-frame-rejection trajectories."""
        raise NotImplementedError(
            "scaffold: surface_deeper_frame_rejection not implemented"
        )
