"""Hypothesis Validator — Steps 4 + 5 owner.

Article ties: Articles I and III. Highest signal-per-cost per Step 6 §3.

SCAFFOLD: methods raise NotImplementedError. Do not call.
"""

from __future__ import annotations

from typing import Any


class HypothesisValidator:
    """Owner of Step 4 (hypotheses + distinguishing predictions) and
    Step 5 (failure conditions per hypothesis).

    Per architecture/03_hypothesis_validator.md and step_8_decision_package §2.
    Articles I + III tie: rejects "concerns" masquerading as hypotheses.
    """

    component_id = "hypothesis_validator"
    article_ties = ("I", "III")

    def enumerate_hypotheses_with_distinguishing_predictions(
        self, decomposition: Any
    ) -> Any:
        """Step 4: hypotheses with distinguishing predictions, closed-set shape."""
        raise NotImplementedError(
            "scaffold: enumerate_hypotheses_with_distinguishing_predictions "
            "not implemented"
        )

    def failure_conditions_per_hypothesis(self, hypotheses: Any) -> Any:
        """Step 5: one explicit failure condition per hypothesis."""
        raise NotImplementedError(
            "scaffold: failure_conditions_per_hypothesis not implemented"
        )
