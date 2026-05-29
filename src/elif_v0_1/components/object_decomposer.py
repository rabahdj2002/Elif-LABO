"""Object Decomposer — Step 2 owner.

Article tie: Article IV (refuse collapsed heterogeneous objects).
Sub-behavior: Step 6 multi-scale relations.

SCAFFOLD: methods raise NotImplementedError. Do not call.
"""

from __future__ import annotations

from typing import Any

from ..base import InputFrame


class ObjectDecomposer:
    """Owner of Step 2 + sub-behavior Step 6 (multi-scale relations).

    Per architecture/02_object_decomposer.md and step_8_decision_package §2.
    Article IV tie: separate mechanism / category families before reasoning.
    """

    component_id = "object_decomposer"
    article_ties = ("IV",)

    def decompose(self, input_frame: InputFrame) -> Any:
        """Step 2: family-axis decomposition tree."""
        raise NotImplementedError("scaffold: decompose not implemented")

    def multi_scale_relate(self, decomposition: Any) -> Any:
        """Step 6 sub-behavior: cross-scale relations among decomposed objects."""
        raise NotImplementedError(
            "scaffold: multi_scale_relate not implemented"
        )
