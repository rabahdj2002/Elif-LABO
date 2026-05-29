"""Governance Kernel — Step 9 owner.

Article ties: Articles V, VI, VII. Step 11 absorbed into Step 9 per Step 8
compression: verdict + confidence + unresolved-uncertainty in one output.

SCAFFOLD: methods raise NotImplementedError. Do not call.
"""

from __future__ import annotations

from typing import Any


class GovernanceKernel:
    """Owner of Step 9 (verdict, confidence, unresolved-uncertainty sources).

    Per architecture/05_governance_kernel.md and step_8_decision_package §2.
    Articles V/VI/VII ties. Immutable refusal conditions override the
    answering layer.
    """

    component_id = "governance_kernel"
    article_ties = ("V", "VI", "VII")

    def verdict_with_confidence_and_uncertainty(
        self, roadmap: Any, prior_steps: Any
    ) -> Any:
        """Step 9: structured (verdict, confidence_value, unresolved_uncertainty_sources[])."""
        raise NotImplementedError(
            "scaffold: verdict_with_confidence_and_uncertainty not implemented"
        )
