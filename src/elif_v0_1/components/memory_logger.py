"""Memory Logger — Step 11 owner. ARCHITECTURE-DEPENDENT component.

Article tie: Article VII (capacity vs truth). This is the one component
that cannot be delivered prompt-only — it requires persistent JSONL,
cross-case state, reuse-count tracking, and capacity-metric aggregation.

Per step_8_decision_package §6, this is the entire architecture-dependent
surface area of v0.1. All other components are prompt-portable.

SCAFFOLD: methods raise NotImplementedError. Do not call.
"""

from __future__ import annotations

from typing import Any

from ..base import InputFrame


class MemoryLogger:
    """Owner of Step 11 (capture) + cross-case state + Article VII tracking.

    Per architecture/07_feedback_memory_logger.md and
    step_8_decision_package §2 + §6. Article VII tie (primary).
    """

    component_id = "memory_logger"
    article_ties = ("VII",)

    def write_event(self, case_id: str, event: Any) -> None:
        """Append a structured event to the case's JSONL log."""
        raise NotImplementedError("scaffold: write_event not implemented")

    def read_case_state(self, case_id: str) -> Any:
        """Return reconstructed state from the case's JSONL log."""
        raise NotImplementedError("scaffold: read_case_state not implemented")

    def find_reuse_candidates(self, input_frame: InputFrame) -> Any:
        """Article VII: cross-case reuse-candidate detection (compositional)."""
        raise NotImplementedError(
            "scaffold: find_reuse_candidates not implemented"
        )

    def compute_capacity_metrics(self) -> Any:
        """Article VII: prior_structures_referenced, reuse_count_total,
        patterns_recognized, time_delta_vs_prior_similar.
        """
        raise NotImplementedError(
            "scaffold: compute_capacity_metrics not implemented"
        )
