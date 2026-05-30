"""ELIF V1 Viewer — read-only rendering layer over existing substrate.

Per `notes/elif_v1_viewer_audit_and_spec.md` (operator-authorized 2026-05-30
post-G0/E.2/Object-Drift-Audit). The viewers reveal existing ELIF; they do
NOT extend it.

Discipline (enforced at module level — verified by tests):

1. **No LLM calls.** No viewer imports `llm_adapter`. No call_counter is
   incremented. The viewers operate purely over `RunReport` instances and
   MemoryLogger JSONL paths.

2. **No substrate modifications.** No component is constructed. No
   MemoryLogger event is written. No fixture is read. No schema is touched.
   No closed-set vocabulary is consulted.

3. **No reasoning layer.** Each viewer is a pure function from
   {RunReport, optional auxiliary artifacts} to a Markdown string. No
   aggregation across runs except literal per-field cell comparisons.

4. **Two tests per rendering — applied per viewer:**
   - Reveal Test: every rendered field can be extracted from an existing
     artifact by a determined reader
   - Truth Test: the rendering claims only what the artifact already claims

Viewers:
    render_decision_room(run_report)               — Step 9/10/11 surface
    render_exploration_lens(run_report)            — 5-territory map
    render_object_chain(run_report, input_frame?)  — Step 1→9 chain
    Laboratory Viewer (4 panels):
        render_memory_timeline(case_id, jsonl_path)
        render_replay_table(acceptance_report)
        render_offline_vs_live_diff(offline, live)
        render_article_vii_observations(jsonl_paths)

Input shape: each viewer accepts either a `RunReport` dataclass instance
OR a dict matching the serialized RunReport JSON shape (as produced by
`elif_v0_1.cli`). The `_normalize_run_report` helper bridges these.

Output shape: Markdown string. Renderers produce no side effects.
"""
from __future__ import annotations

from .decision_room import render_decision_room
from .exploration_lens import render_exploration_lens
from .laboratory_viewer import (
    render_article_vii_observations,
    render_memory_timeline,
    render_offline_vs_live_diff,
    render_replay_table,
)
from .object_drift_panel import render_object_chain

__all__ = [
    "render_decision_room",
    "render_exploration_lens",
    "render_object_chain",
    "render_memory_timeline",
    "render_replay_table",
    "render_offline_vs_live_diff",
    "render_article_vii_observations",
]
