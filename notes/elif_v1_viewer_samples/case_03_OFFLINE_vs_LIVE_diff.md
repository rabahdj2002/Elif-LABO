# Offline-vs-Live Structural Diff — case_03_operational_organizational

> **The Viewer renders the comparison; it does not adjudicate it.** Both sides are valid procedural outputs. For substantive interpretation, see [notes/elif_post_e2_divergence_audit.md] and [notes/elif_post_e2_object_drift_audit.md]. The 'same?' column is a literal `==` comparison — not a judgment about which side is correct.

| Field | Offline | Live | Same? |
|---|---|---|---|
| `exit_code` | `20` | `0` | **NO** |
| `envelope_count` | `11` | `11` | yes |
| `memory_logger_entries_written` | `15` | `14` | **NO** |
| `step_9.verdict` | `refuse` | `constrain` | **NO** |
| `step_9.unresolved_uncertainty_count` | `3` | `5` | **NO** |
| `step_10.operative_count` | `1` | `7` | **NO** |
| `step_10.theoretical_count` | `3` | `5` | **NO** |
| `step_11.post_refusal_closure` | `True` | `False` | **NO** |
| `step_11.final_verdict` | `refuse` | `constrain` | **NO** |


---


_No aggregate verdict is emitted. Per-row 'same?' annotations are literal comparisons only._