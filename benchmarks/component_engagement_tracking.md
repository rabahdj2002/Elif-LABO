# Component Engagement Tracking Schema

Per case, capture engagement state for each of the 7 canonical components plus all current B-tagged candidates.

| Field | Description |
|---|---|
| `component_id` | e.g., `frame_validator`, `governance_kernel`, `hidden_assumption_extraction` |
| `tag` | A / B / C / D |
| `engaged` | true / false |
| `evidence` | line refs in Condition C output |
| `collapses_into` | if engaged but reducible to another component, name it |
| `prompting_portable` | yes / no / uncertain |
| `frequency_across_cases` | 0/3, 1/3, 2/3, 3/3 (updated after each case) |
| `current_classification_pressure` | engaged / dormant / collapses into X / emerges as distinct / unresolved |

## Reclassification rule

After case 3, components and candidates are reclassified per `procedure/abcd_classification_system.md` retention bars. The new component list (possibly smaller than 7) is then frozen for the contract pack decision.
