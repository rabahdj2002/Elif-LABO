"""Operative Truth Separator — Step 10 owner.

Article tie: Article IV. Separates scientific / theoretical plausibility
from operational viability.

SCAFFOLD: methods raise NotImplementedError. Do not call.
"""

from __future__ import annotations

from typing import Any


class OperativeTruthSeparator:
    """Owner of Step 10 (operative vs theoretical).

    Per architecture/06_operative_truth_separator.md and
    step_8_decision_package §2. Article IV tie.
    """

    component_id = "operative_truth_separator"
    article_ties = ("IV",)

    def separate_operative_from_theoretical(self, verdict: Any) -> Any:
        """Step 10: two-bucket output (operative-true vs theoretically-plausible)."""
        raise NotImplementedError(
            "scaffold: separate_operative_from_theoretical not implemented"
        )
