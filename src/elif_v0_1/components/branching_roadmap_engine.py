"""Branching Roadmap Engine — Steps 7 + 8 owner.

Article ties: Articles V, VI, VII. Produces outside-frame trajectories
(BRE-feed) and the stage-gated roadmap.

SCAFFOLD: methods raise NotImplementedError. Do not call.
"""

from __future__ import annotations

from typing import Any


class BranchingRoadmapEngine:
    """Owner of Step 7 (BRE-feed: outside-frame trajectories) and
    Step 8 (stage-gated roadmap).

    Per architecture/04_branching_roadmap_engine.md and
    step_8_decision_package §2. Articles V/VI/VII ties.
    """

    component_id = "branching_roadmap_engine"
    article_ties = ("V", "VI", "VII")

    def outside_frame_trajectories_bre_feed(
        self, hypotheses: Any, failures: Any
    ) -> Any:
        """Step 7: enumerate trajectories outside the current frame."""
        raise NotImplementedError(
            "scaffold: outside_frame_trajectories_bre_feed not implemented"
        )

    def stage_gated_roadmap(self, trajectories: Any) -> Any:
        """Step 8: stage-gated roadmap with continuation thresholds."""
        raise NotImplementedError(
            "scaffold: stage_gated_roadmap not implemented"
        )
