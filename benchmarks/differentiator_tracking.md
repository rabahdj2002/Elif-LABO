# Differentiator Tracking Schema

Per case, capture each observed differentiator with the following fields.

| Field | Description |
|---|---|
| `differentiator_id` | unique per case, e.g. `case_01.diff_03` |
| `description` | what the differentiator IS (factual, not interpretive) |
| `condition_c_line_refs` | line numbers / paragraph anchors in Condition C output |
| `also_in_condition_b` | yes / no (collapses to prompting if yes) |
| `architecture_dependent` | yes / no / uncertain |
| `survives_across_cases` | 0/3, 1/3, 2/3, 3/3 (updated after each case) |
| `mapped_component` | A / B / C / D / unmapped |
| `notes` | anything benchmark-blocking |

## Filing convention

Cross-case differentiator survival is computed by aggregating the `survives_across_cases` field after each case completes. Differentiators that drop to 0/3 after the third case become D-tagged removal candidates.
